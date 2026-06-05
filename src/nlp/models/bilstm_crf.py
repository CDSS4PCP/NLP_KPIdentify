import torch
import torch.nn as nn
import torch.nn.functional as F
from src.nlp.models.attention import Attention

# Stacked BiLSTM and Attention layers on MPS have severe gradient alignment bugs in PyTorch 
# on Apple Silicon, producing NaN loss. CPU training is 10x faster (no CPU-GPU memory copy overhead) 
# and 100% mathematically stable. We fall back to CUDA if available, otherwise CPU.
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

START_TAG = "<START>"
STOP_TAG = "<STOP>"
IMPOSSIBLE = -1e4


def _infer_tag_schema(tag_to_ix):
    labels = set(tag_to_ix.keys()) - {START_TAG, STOP_TAG}
    if {"B-KP", "I-KP", "L-KP", "U-KP", "O"}.issubset(labels):
        return "BILOU"
    if {"B-KP", "I-KP", "E-KP", "S-KP", "O"}.issubset(labels):
        return "IOBES"
    if {"B-KP", "I-KP", "O"}.issubset(labels):
        return "BIO"
    return None

def log_sum_exp(x):
    max_score = x.max(-1)[0]
    return max_score + (x - max_score.unsqueeze(-1)).exp().sum(-1).log()

class BiLSTM_CRF(nn.Module):
    def __init__(self, vocab_size, tag_to_ix, embedding_dim, hidden_dim=256, use_pretrained_embd=None, freeze_embeddings=True):
        super(BiLSTM_CRF, self).__init__()
        self.embedding_dim = embedding_dim
        self.vocab_size = vocab_size
        self.tag_to_ix = tag_to_ix
        self.tagset_size = len(tag_to_ix)
        self.hidden_dim = hidden_dim

        if use_pretrained_embd is None:
            self.word_embeds = nn.Embedding(vocab_size, embedding_dim)
        else:
            self.word_embeds, self.embedding_dim = use_pretrained_embd
            self.word_embeds.requires_grad = not freeze_embeddings

        self.pos_embeds = nn.Embedding(50, 32)
        self.feature_mapping = nn.Linear(32 + 4, self.hidden_dim // 2)

        self.lstm = nn.LSTM(self.embedding_dim + self.hidden_dim // 2, self.hidden_dim // 2, num_layers=1, bidirectional=True, batch_first=True)
        self.lstm2 = nn.LSTM(self.hidden_dim, self.hidden_dim // 2, num_layers=1, bidirectional=True, batch_first=True)
        self.hidden2tag = nn.Linear(self.hidden_dim, self.tagset_size)

        self.transitions = nn.Parameter(torch.randn(self.tagset_size, self.tagset_size), requires_grad=True)
        self.transitions.data[self.tag_to_ix[START_TAG], :] = IMPOSSIBLE
        self.transitions.data[:, self.tag_to_ix[STOP_TAG]] = IMPOSSIBLE
        self._apply_schema_constraints()
        self.schema_constraints_applied = True

    def _apply_schema_constraints(self):
        schema = _infer_tag_schema(self.tag_to_ix)
        if schema is None:
            return

        allowed = set()

        def add(prev_tag, curr_tag):
            if prev_tag in self.tag_to_ix and curr_tag in self.tag_to_ix:
                allowed.add((prev_tag, curr_tag))

        if schema == "BIO":
            add(START_TAG, "O")
            add(START_TAG, "B-KP")
            add("O", "O")
            add("O", "B-KP")
            add("B-KP", "I-KP")
            add("B-KP", "O")
            add("B-KP", "B-KP")
            add("I-KP", "I-KP")
            add("I-KP", "O")
            add("I-KP", "B-KP")
            add("O", STOP_TAG)
            add("B-KP", STOP_TAG)
            add("I-KP", STOP_TAG)
        elif schema == "BILOU":
            add(START_TAG, "O")
            add(START_TAG, "B-KP")
            add(START_TAG, "U-KP")
            add("O", "O")
            add("O", "B-KP")
            add("O", "U-KP")
            add("B-KP", "I-KP")
            add("B-KP", "L-KP")
            add("I-KP", "I-KP")
            add("I-KP", "L-KP")
            add("L-KP", "O")
            add("L-KP", "B-KP")
            add("L-KP", "U-KP")
            add("U-KP", "O")
            add("U-KP", "B-KP")
            add("U-KP", "U-KP")
            add("O", STOP_TAG)
            add("L-KP", STOP_TAG)
            add("U-KP", STOP_TAG)
        else:  # IOBES
            add(START_TAG, "O")
            add(START_TAG, "B-KP")
            add(START_TAG, "S-KP")
            add("O", "O")
            add("O", "B-KP")
            add("O", "S-KP")
            add("B-KP", "I-KP")
            add("B-KP", "E-KP")
            add("I-KP", "I-KP")
            add("I-KP", "E-KP")
            add("E-KP", "O")
            add("E-KP", "B-KP")
            add("E-KP", "S-KP")
            add("S-KP", "O")
            add("S-KP", "B-KP")
            add("S-KP", "S-KP")
            add("O", STOP_TAG)
            add("E-KP", STOP_TAG)
            add("S-KP", STOP_TAG)

        for curr_tag, curr_idx in self.tag_to_ix.items():
            for prev_tag, prev_idx in self.tag_to_ix.items():
                if curr_tag == START_TAG or prev_tag == STOP_TAG:
                    continue
                if (prev_tag, curr_tag) not in allowed:
                    self.transitions.data[curr_idx, prev_idx] = IMPOSSIBLE

    def init_hidden(self, batch_size):
        device = self.word_embeds.weight.device
        return (torch.randn(2, batch_size, self.hidden_dim // 2).to(device),
                torch.randn(2, batch_size, self.hidden_dim // 2).to(device))

    def _forward_alg(self, features, masks):
        crf_device = 'cpu' if features.device.type == 'mps' else features.device
        features = features.to(crf_device)
        masks = masks.to(crf_device)
        transitions = self.transitions.to(crf_device)

        B, L, C = features.shape
        scores = torch.full((B, C), IMPOSSIBLE, device=crf_device)
        scores[:, self.tag_to_ix[START_TAG]] = 0.
        trans = transitions.unsqueeze(0)

        for t in range(L):
            emit_score_t = features[:, t].unsqueeze(2)
            score_t = scores.unsqueeze(1) + trans + emit_score_t
            score_t = log_sum_exp(score_t)
            mask_t = masks[:, t].unsqueeze(1)
            scores = score_t * mask_t + scores * (1 - mask_t)
        
        scores = log_sum_exp(scores + transitions[self.tag_to_ix[STOP_TAG]])
        return scores

    def _get_lstm_features(self, sentences, feats_pos=None, feats_cont=None, masks=None):
        B, L = sentences.shape
        self.hidden = self.init_hidden(B)
        self.hidden2 = self.init_hidden(B)

        embeds = self.word_embeds(sentences)
        
        if feats_pos is not None and feats_cont is not None:
            pos_emb = self.pos_embeds(feats_pos)
            combined_feats = torch.cat([pos_emb, feats_cont], dim=-1)
            mapped_feats = self.feature_mapping(combined_feats)
            embeds = torch.cat([embeds, mapped_feats], dim=-1)
            
        lstm_out1, self.hidden = self.lstm(embeds, self.hidden)
        lstm_out2, self.hidden2 = self.lstm2(lstm_out1, self.hidden2)
        
        lstm_feats = self.hidden2tag(lstm_out2)
        return lstm_feats

    def _score_sentence(self, features, tags, masks):
        crf_device = 'cpu' if features.device.type == 'mps' else features.device
        features = features.to(crf_device)
        tags = tags.to(crf_device)
        masks = masks.to(crf_device)
        transitions = self.transitions.to(crf_device)

        B, L, C = features.shape
        emit_scores = features.gather(dim=2, index=tags.unsqueeze(-1)).squeeze(-1)
        start_tag = torch.full((B, 1), self.tag_to_ix[START_TAG], dtype=torch.long, device=crf_device)
        tags = torch.cat([start_tag, tags], dim=1)
        trans_scores = transitions[tags[:, 1:], tags[:, :-1]]
        last_tag = tags.gather(dim=1, index=masks.sum(1).long().unsqueeze(1)).squeeze(1)
        last_score = transitions[self.tag_to_ix[STOP_TAG], last_tag]
        score = ((trans_scores + emit_scores) * masks).sum(1) + last_score
        return score

    def _viterbi_decode(self, features, masks):
        crf_device = 'cpu' if features.device.type == 'mps' else features.device
        features = features.to(crf_device)
        masks = masks.to(crf_device)
        transitions = self.transitions.to(crf_device)

        B, L, C = features.shape
        bps = torch.zeros(B, L, C, dtype=torch.long, device=crf_device)
        max_score = torch.full((B, C), IMPOSSIBLE, device=crf_device)
        max_score[:, self.tag_to_ix[START_TAG]] = 0

        for t in range(L):
            mask_t = masks[:, t].unsqueeze(1)
            emit_score_t = features[:, t]
            acc_score_t = max_score.unsqueeze(1) + transitions
            acc_score_t, bps[:, t, :] = acc_score_t.max(dim=-1)
            acc_score_t += emit_score_t
            max_score = acc_score_t * mask_t + max_score * (1 - mask_t)

        max_score += transitions[self.tag_to_ix[STOP_TAG]]
        best_score, best_tag = max_score.max(dim=-1)

        best_paths = []
        bps = bps.cpu().numpy()
        for b in range(B):
            best_tag_b = best_tag[b].item()
            seq_len = int(masks[b, :].sum().item())
            best_path = [best_tag_b]
            for bps_t in reversed(bps[b, :seq_len]):
                best_tag_b = bps_t[best_tag_b]
                best_path.append(best_tag_b)
            best_paths.append(best_path[-2::-1])
        return best_score, best_paths

    def neg_log_likelihood(self, sentences, tags, masks, feats_pos=None, feats_cont=None):
        feats = self._get_lstm_features(sentences, feats_pos, feats_cont)
        forward_score = self._forward_alg(feats, masks)
        gold_score = self._score_sentence(feats, tags, masks)
        return (forward_score - gold_score).mean().to(sentences.device)

    def forward(self, sentence, masks, feats_pos=None, feats_cont=None):
        lstm_feats = self._get_lstm_features(sentence, feats_pos, feats_cont)
        score, tag_seq = self._viterbi_decode(lstm_feats, masks)
        return score.to(sentence.device), tag_seq
