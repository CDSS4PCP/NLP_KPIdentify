import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import io

# Bidirectional LSTM has known bus error/segmentation fault bugs on PyTorch MPS backend.
# We fall back to CUDA if available, otherwise CPU.
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def set_device(device_obj):
    global DEVICE
    DEVICE = device_obj

class EmbeddingsReader:
    @staticmethod
    def from_text(filename, vocab, unif=0.25):
        def init_embeddings(vocab_size, embed_dim, uniform):
            return np.random.uniform(-uniform, uniform, (vocab_size, embed_dim))

        with io.open(filename, "r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                line = line.rstrip("\n ")
                values = line.split(" ")

                if i == 0:
                    if len(values) == 2:
                        weight = init_embeddings(len(vocab), values[1], unif)
                        continue
                    else:
                        weight = init_embeddings(len(vocab), len(values[1:]), unif)
                word = values[0]
                if word in vocab:
                    vec = np.asarray(values[1:], dtype=np.float32)
                    weight[vocab[word]] = vec
        if '<UNK>' in vocab:
            weight[vocab['<UNK>']] = 0.0
        
        embeddings = nn.Embedding(weight.shape[0], weight.shape[1])
        embeddings.weight = nn.Parameter(torch.from_numpy(weight).float())
        return embeddings, weight.shape[1]
    
    @staticmethod
    def from_binary(filename, vocab, unif=0.25):
        def init_embeddings(vocab_size, embed_dim, uniform):
            return np.random.uniform(-uniform, uniform, (vocab_size, embed_dim))

        def read_word(f):
            s = bytearray()
            ch = f.read(1)
            while ch != b' ':
                s.extend(ch)
                ch = f.read(1)
            s = s.decode('utf-8')
            return s.strip(' \n')

        vocab_size = len(vocab)
        with io.open(filename, "rb") as f:
            header = f.readline()
            file_vocab_size, embed_dim = map(int, header.split())
            weight = init_embeddings(len(vocab), embed_dim, unif)
            if '<UNK>' in vocab:
                weight[vocab['<UNK>']] = 0.0
            width = 4 * embed_dim
            for i in range(file_vocab_size):
                word = read_word(f)
                raw = f.read(width)
                if word in vocab:
                    vec = np.fromstring(raw, dtype=np.float32)
                    weight[vocab[word]] = vec
        embeddings = nn.Embedding(weight.shape[0], weight.shape[1])
        embeddings.weight = nn.Parameter(torch.from_numpy(weight).float())
        return embeddings, embed_dim

class WordLSTM(nn.Module):
    def __init__(self, n_hidden=256, n_layers=4, drop_prob=0.3, lr=0.001, bidirection=False, pretrainedWE=None, vocab={}):
        super().__init__()
        self.drop_prob = drop_prob
        self.n_layers = n_layers
        self.lr = lr
        self.bidirection = bidirection 
        self.num_directional = 2 if bidirection else 1
        self.n_hidden = n_hidden
        self.vocab_size = len(vocab)
        
        if pretrainedWE is None:
            self.emb_layer = nn.Embedding(self.vocab_size, 200)
            self.lstm = nn.LSTM(200, self.n_hidden, n_layers, dropout=drop_prob, batch_first=True, bidirectional=self.bidirection)
        else:
            self.emb_layer, self.emb_dim = EmbeddingsReader.from_binary(pretrainedWE, vocab)
            self.lstm = nn.LSTM(self.emb_dim, self.n_hidden, n_layers, dropout=drop_prob, batch_first=True, bidirectional=self.bidirection)
        
        self.dropout = nn.Dropout(drop_prob)
        self.fc = nn.Linear(n_hidden * self.num_directional, self.vocab_size)      
    
    def forward(self, x, hidden):
        embedded = self.emb_layer(x)     
        lstm_output, hidden = self.lstm(embedded, hidden)
        out = self.dropout(lstm_output)
        out = out.reshape(-1, self.n_hidden * self.num_directional)
        out = self.fc(out)
        return out, hidden
    
    def init_hidden(self, batch_size):
        weight = next(self.parameters()).data
        if torch.cuda.is_available():
            hidden = (weight.new(self.n_layers*self.num_directional, batch_size, self.n_hidden).zero_().cuda(),
                      weight.new(self.n_layers*self.num_directional, batch_size, self.n_hidden).zero_().cuda())
        else:
            hidden = (weight.new(self.n_layers, batch_size, self.n_hidden).zero_(),
                      weight.new(self.n_layers, batch_size, self.n_hidden).zero_())
        return hidden

class WordLSTM_v2(nn.Module):
    def __init__(self, n_hidden=256, n_layers=4, drop_prob=0.3, lr=0.001, bidirection=False, pretrainedWE=None, vocab={}):
        super().__init__()
        self.drop_prob = drop_prob
        self.n_layers = n_layers
        self.lr = lr
        self.bidirection = True 
        self.num_directional = 2 if bidirection else 1
        self.n_hidden = n_hidden
        self.vocab_size = len(vocab)
        
        if pretrainedWE is None:
            self.emb_layer = nn.Embedding(self.vocab_size, 200)
            self.lstm = nn.LSTM(200, self.n_hidden//2, n_layers, dropout=drop_prob, batch_first=True, bidirectional=self.bidirection)
        else:
            self.emb_layer, self.emb_dim = EmbeddingsReader.from_binary(pretrainedWE, vocab)
            self.lstm = nn.LSTM(self.emb_dim, self.n_hidden//2, n_layers, dropout=drop_prob, batch_first=True, bidirectional=self.bidirection)
        
        self.dropout = nn.Dropout(drop_prob)
        self.fc = nn.Linear(n_hidden, self.vocab_size)      
    
    def forward(self, x, hidden):
        embedded = self.emb_layer(x)     
        lstm_output, hidden = self.lstm(embedded, hidden)
        out = self.dropout(lstm_output)
        out = out.reshape(-1, self.n_hidden)
        out = self.fc(out)
        return out, hidden
    
    def init_hidden(self, batch_size):
        return (torch.randn(self.n_layers*2, batch_size, self.n_hidden // 2).to(DEVICE),
                torch.randn(self.n_layers*2, batch_size, self.n_hidden // 2).to(DEVICE))

class LanguageModel:
    def __init__(self, token2int={}):
        self.raw_data = None
        self.processed_data = None
        self.token2int = token2int

    def create_seq(self, sent, seq_len=5):
        sequences = []
        if len(sent) > seq_len:
            for i in range(seq_len, len(sent)):
                seq = sent[i-seq_len:i+1]
                sequences.append(" ".join(seq))
            return sequences
        else:
            return sent + ['<UNK>'] * (len(sent) - seq_len)

    def get_integer_seq(self, seq, tokenized=True):
        unk = self.token2int.get('<UNK>', 1)
        tokens = seq if tokenized else seq.split()
        return [self.token2int.get(w, unk) for w in tokens]
