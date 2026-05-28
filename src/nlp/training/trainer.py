import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import random

class Trainer:
    def __init__(self, token2int={}, int2token={}, X_train=[], y_train=[], X_test=[], y_test=[]):
        self.token2int = token2int
        self.int2token = int2token
        self.X_train = X_train
        self.y_train = y_train
        self.X_Test = X_test
        self.y_test = y_test

    def get_batches(self, arr_x, arr_y, batch_size):    
        prv = 0
        for n in range(batch_size, arr_x.shape[0], batch_size):
            x = arr_x[prv:n,:]
            y = arr_y[prv:n,:]
            prv = n
            yield x, y  

    def train(self, net, epochs=10, batch_size=32, lr=0.001, clip=1):
        opt = torch.optim.Adam(net.parameters(), lr=lr)
        criterion = nn.CrossEntropyLoss()
        net.cuda()
        net.train()
        
        for e in range(epochs):
            losses = []
            h = net.init_hidden(batch_size)
            
            for x, y in self.get_batches(self.X_train, self.y_train, batch_size):
                inputs, targets = torch.from_numpy(x), torch.from_numpy(y)
                targets = targets.type(torch.LongTensor)
                inputs, targets = inputs.cuda(), targets.cuda()

                h = tuple([each.data for each in h])
                net.zero_grad()
                
                output, h = net(inputs, h)
                loss = criterion(output, targets.view(-1))
                losses.append(loss.detach().item())

                loss.backward()
                nn.utils.clip_grad_norm_(net.parameters(), clip)
                opt.step()            
                
            print("Epoch: {}/{}...".format(e+1, epochs),"mean_loss : %0.2f, Perplexity : %0.2f"%(np.mean(losses), np.exp(np.mean(losses))))

        net.eval()
        losses = []
        h = net.init_hidden(batch_size)
        for x, y in self.get_batches(self.X_Test, self.y_test, batch_size):
            inputs, targets = torch.from_numpy(x), torch.from_numpy(y)
            targets = targets.type(torch.LongTensor)
            inputs, targets = inputs.cuda(), targets.cuda()
            h = tuple([each.data for each in h])
            net.zero_grad()
            output, h = net(inputs, h)
            loss = criterion(output, targets.view(-1))
            losses.append(loss.detach().item())

        print("Test Perplexity: %0.2f"%(np.exp(np.mean(losses))))

    def predict(self, net, tkn, h=None):
        x = np.array([[self.token2int[tkn]]])
        inputs = torch.from_numpy(x).cuda()
        h = tuple([each.data for each in h])
        out, h = net(inputs, h)
        p = F.softmax(out, dim=1).data.cpu().numpy()
        p = p.reshape(p.shape[1],)
        top_n_idx = p.argsort()[-3:][::-1]
        sampled_token_index = top_n_idx[random.sample([0,1,2],1)[0]]
        return self.int2token[sampled_token_index], h

    def sample(self, net, size, prime='it is'):
        net.cuda()
        net.eval()
        h = net.init_hidden(1)
        toks = prime.split()
        for t in prime.split():
            token, h = self.predict(net, t, h)
        toks.append(token)
        for i in range(size-1):
            token, h = self.predict(net, toks[-1], h)
            toks.append(token)
        return ' '.join(toks)

    def saveModel(self, net, file_path):
        torch.save(net.state_dict(),file_path)
