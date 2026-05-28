import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
import random
import os
from torch.utils.data import DataLoader, TensorDataset

# Bidirectional LSTM has known bus error/segmentation fault bugs on PyTorch MPS backend.
# We fall back to CUDA if available, otherwise CPU.
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def set_device(device_obj):
    global DEVICE
    DEVICE = device_obj

class Trainer:

    def __init__(self, token2int={}, X_train=[], y_train=[], X_test=[], y_test=[]):
        self.token2int = token2int
        self.X_train = X_train
        self.y_train = y_train
        self.X_Test = X_test
        self.y_test = y_test

    def get_batches(self, arr_x, arr_y, batch_size):
        prv = 0
        for n in range(batch_size, arr_x.shape[0], batch_size):
            x = arr_x[prv:n, :]
            y = arr_y[prv:n, :]
            prv = n
            yield (x, y)

    def train(self, net, epochs=10, batch_size=32, lr=0.001, clip=1, num_workers=None):
        import time
        opt = torch.optim.Adam(net.parameters(), lr=lr)
        criterion = nn.CrossEntropyLoss()
        net.to(DEVICE)
        net.train()

        use_cuda = DEVICE.type == "cuda"
        if use_cuda:
            torch.backends.cudnn.benchmark = True
            torch.backends.cuda.matmul.allow_tf32 = True
            torch.backends.cudnn.allow_tf32 = True
            torch.set_float32_matmul_precision("high")

        x_train_t = torch.from_numpy(self.X_train).long()
        y_train_t = torch.from_numpy(self.y_train).long()
        x_test_t = torch.from_numpy(self.X_Test).long()
        y_test_t = torch.from_numpy(self.y_test).long()

        if num_workers is None:
            # WSL often performs worse with many worker processes for in-memory numpy datasets.
            if os.environ.get("WSL_DISTRO_NAME"):
                num_workers = 0
            else:
                num_workers = min(4, max(0, (os.cpu_count() or 1) - 1))
        else:
            num_workers = max(0, int(num_workers))

        pin_mem = use_cuda
        loader_kwargs = {
            "batch_size": batch_size,
            "num_workers": num_workers,
            "pin_memory": pin_mem,
        }
        if num_workers > 0:
            loader_kwargs["persistent_workers"] = True

        train_loader = DataLoader(
            TensorDataset(x_train_t, y_train_t),
            shuffle=True,
            drop_last=True,
            **loader_kwargs,
        )
        test_loader = DataLoader(
            TensorDataset(x_test_t, y_test_t),
            shuffle=False,
            drop_last=True,
            **loader_kwargs,
        )

        if use_cuda:
            if hasattr(torch.cuda.amp, 'GradScaler'):
                scaler = torch.cuda.amp.GradScaler(enabled=True)
            else:
                scaler = torch.amp.GradScaler("cuda", enabled=True)
        else:
            scaler = None
        if use_cuda:
            dev_name = torch.cuda.get_device_name(torch.cuda.current_device())
            print(f"CUDA device: {dev_name}")
        print(f"DataLoader workers: {num_workers} | pin_memory: {pin_mem}")
        print(f"Starting Bi-Language Model training on device: {DEVICE}...")
        total_train_start = time.time()
        epoch_times = []
        for e in range(epochs):
            losses = []
            h = net.init_hidden(batch_size)
            epoch_start = time.time()
            for inputs, targets in train_loader:
                inputs = inputs.to(DEVICE, non_blocking=pin_mem)
                targets = targets.to(DEVICE, non_blocking=pin_mem)
                h = tuple([each.data for each in h])
                opt.zero_grad(set_to_none=True)

                if use_cuda:
                    with torch.autocast(device_type="cuda", dtype=torch.float16):
                        output, h = net(inputs, h)
                        loss = criterion(output, targets.view(-1))
                else:
                    with torch.autocast(device_type="cpu", dtype=torch.bfloat16):
                        output, h = net(inputs, h)
                        loss = criterion(output, targets.view(-1))

                losses.append(loss.detach().item())

                if use_cuda:
                    scaler.scale(loss).backward()
                    scaler.unscale_(opt)
                    nn.utils.clip_grad_norm_(net.parameters(), clip)
                    scaler.step(opt)
                    scaler.update()
                else:
                    loss.backward()
                    nn.utils.clip_grad_norm_(net.parameters(), clip)
                    opt.step()

            if use_cuda:
                torch.cuda.synchronize()
            epoch_time = time.time() - epoch_start
            epoch_times.append(epoch_time)
            print(f"Epoch: {e + 1}/{epochs}... Completed in {epoch_time:.2f}s | mean_loss : {np.mean(losses):.2f} | Perplexity : {np.exp(np.mean(losses)):.2f}")
        total_train_time = time.time() - total_train_start
        print(f"Total BiLM training time: {total_train_time:.2f}s (Avg per epoch: {np.mean(epoch_times) if epoch_times else 0.0:.2f}s)")
        
        net.eval()
        losses = []
        h = net.init_hidden(batch_size)
        test_eval_start = time.time()
        with torch.no_grad():
            for inputs, targets in test_loader:
                inputs = inputs.to(DEVICE, non_blocking=pin_mem)
                targets = targets.to(DEVICE, non_blocking=pin_mem)
                h = tuple([each.data for each in h])

                if use_cuda:
                    with torch.autocast(device_type="cuda", dtype=torch.float16):
                        output, h = net(inputs, h)
                        loss = criterion(output, targets.view(-1))
                else:
                    with torch.autocast(device_type="cpu", dtype=torch.bfloat16):
                        output, h = net(inputs, h)
                        loss = criterion(output, targets.view(-1))

                losses.append(loss.detach().item())
        test_eval_time = time.time() - test_eval_start
        print(f"Test Perplexity: {np.exp(np.mean(losses)):.2f} (Evaluated in {test_eval_time:.2f}s)")

    def predict(self, net, tkn, h=None):
        x = np.array([[self.token2int[tkn]]])
        inputs = torch.from_numpy(x)
        inputs = inputs.to(DEVICE)
        h = tuple([each.data for each in h])
        (out, h) = net(inputs, h)
        p = F.softmax(out, dim=1).data
        p = p.cpu()
        p = p.numpy()
        p = p.reshape(p.shape[1])
        top_n_idx = p.argsort()[-3:][::-1]
        sampled_token_index = top_n_idx[random.sample([0, 1, 2], 1)[0]]
        return (int2token[sampled_token_index], h)

    def sample(self, net, size, prime='it is'):
        net.to(DEVICE)
        net.eval()
        h = net.init_hidden(1)
        toks = prime.split()
        for t in prime.split():
            (token, h) = self.predict(net, t, h, self.token2int)
        toks.append(token)
        for i in range(size - 1):
            (token, h) = self.predict(net, toks[-1], h, self.token2int)
            toks.append(token)
        return ' '.join(toks)

    def saveModel(self, net, file_path):
        torch.save(net.state_dict(), file_path)