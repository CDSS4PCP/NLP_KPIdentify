import torch
import torch.nn as nn
import torch.nn.functional as F

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

class WordAttention(nn.Module):
    def __init__(self, feature_dim, step_dim, bias=True):
        super(WordAttention, self).__init__()
        self.bias = bias
        self.feature_dim = feature_dim
        self.step_dim = step_dim
        
        self.weight = nn.Parameter(torch.empty(feature_dim, 1))
        nn.init.kaiming_uniform_(self.weight)
        
        if bias:
            self.b = nn.Parameter(torch.zeros(step_dim))
        
    def forward(self, x, mask=None):
        feature_dim = self.feature_dim
        step_dim = self.step_dim
        
        # Multiply input by weight matrix
        eij = torch.mm(
            x.contiguous().view(-1, feature_dim), 
            self.weight
        ).view(-1, step_dim)

        if self.bias:
            eij = eij + self.b
            
        eij = torch.tanh(eij)
        a = torch.exp(eij)
        
        if mask is not None:
            a = a * mask.float()

        a = a / (torch.sum(a, 1, keepdim=True) + 1e-10)

        weighted_input = x * torch.unsqueeze(a, -1)
        return torch.sum(weighted_input, 1)

class SentAttention(nn.Module):
    def __init__(self, feature_dim, step_dim, bias=False):
        super(SentAttention, self).__init__()
        self.bias = bias
        self.feature_dim = feature_dim
        self.step_dim = step_dim
        
        self.weight = nn.Parameter(torch.empty(feature_dim, step_dim))
        nn.init.kaiming_uniform_(self.weight)
        
        if bias:
            self.b = nn.Parameter(torch.zeros(step_dim))
        
    def _build_block_mask(self, doc_ids, sentence_len, device):
        if doc_ids is None:
            return None
        if doc_ids.dim() != 1:
            doc_ids = doc_ids.view(-1)
        query_doc_ids = doc_ids.repeat_interleave(sentence_len)
        return (query_doc_ids.unsqueeze(1) == doc_ids.unsqueeze(0)).to(device=device, dtype=torch.float)

    def forward(self, h_it, s_i, mask=None, doc_ids=None, use_block_mask=False):
        feature_dim = self.feature_dim
        step_dim = self.step_dim
        
        # Project hidden states
        eij = torch.mm(
            h_it.contiguous().view(-1, feature_dim), 
            self.weight
        ) # [B * L, step_dim]

        # Dot product with sentence context representation s_i
        eij = torch.mm(
            eij,
            s_i.view(step_dim, -1)
        ) # [B * L, B]
        
        if self.bias:
            eij = eij + self.b
            
        eij = torch.tanh(eij)
        a = torch.exp(eij)
        
        if mask is not None:
            a = a * mask.float().view(-1, 1)

        if use_block_mask and doc_ids is not None:
            if doc_ids.numel() != h_it.size(0):
                raise ValueError(f"doc_ids size mismatch: expected {h_it.size(0)}, got {doc_ids.numel()}")
            block_mask = self._build_block_mask(doc_ids.to(a.device), h_it.size(1), a.device)
            a = a * block_mask

        a = a / (torch.sum(a, 1, keepdim=True) + 1e-10)

        # Compute global neural attention representation
        global_neural_attn = torch.mm(a, s_i).view(-1, h_it.size(1), feature_dim)
        return global_neural_attn

class HAN_CRF(nn.Module):
    def __init__(self, vocab_size, tag_to_ix, embedding_dim, hidden_dim=256, dropout=0.2, max_sent_len=128, use_pretrained_embd=None):
        super(HAN_CRF, self).__init__()
        self.embedding_dim = embedding_dim
        self.vocab_size = vocab_size
        self.tag_to_ix = tag_to_ix
        self.tagset_size = len(tag_to_ix)
        self.hidden_dim = hidden_dim
        self.max_sent_len = max_sent_len

        if use_pretrained_embd is None:
            self.word_embeds = nn.Embedding(vocab_size, embedding_dim)
        else:
            self.word_embeds, self.embedding_dim = use_pretrained_embd
            self.word_embeds.requires_grad = True

        self.pos_embeds = nn.Embedding(50, 32)
        self.feature_mapping = nn.Linear(32 + 4, self.hidden_dim // 2)

        self.dropout = nn.Dropout(dropout)
        
        self.lstm = nn.LSTM(self.embedding_dim + self.hidden_dim // 2, self.hidden_dim // 2,
                            num_layers=1, bidirectional=True, batch_first=True, dropout=dropout)

        self.lstm2 = nn.LSTM(self.hidden_dim * 2, self.hidden_dim // 2,
                            num_layers=1, bidirectional=True, batch_first=True, dropout=dropout)

        self.word_attention_layer = WordAttention(self.hidden_dim, self.max_sent_len)
        self.sent_attention_layer = SentAttention(self.hidden_dim, self.hidden_dim)

        self.hidden2tag = nn.Linear(self.hidden_dim, self.tagset_size)

        self.transitions = nn.Parameter(torch.randn(self.tagset_size, self.tagset_size), requires_grad=True)
        self.transitions.data[self.tag_to_ix[START_TAG], :] = IMPOSSIBLE
        self.transitions.data[:, self.tag_to_ix[STOP_TAG]] = IMPOSSIBLE

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

    def _get_lstm_features(self, sentences, masks, feats_pos=None, feats_cont=None, doc_ids=None, use_block_mask=False):
        B, L = sentences.shape
        self.hidden = self.init_hidden(B)
        self.hidden2 = self.init_hidden(B)

        # 1. Embed and apply dropout
        embeds = self.dropout(self.word_embeds(sentences))
        
        if feats_pos is not None and feats_cont is not None:
            pos_emb = self.pos_embeds(feats_pos)
            combined_feats = torch.cat([pos_emb, feats_cont], dim=-1)
            mapped_feats = self.feature_mapping(combined_feats)
            embeds = torch.cat([embeds, mapped_feats], dim=-1)

        # 2. LSTM 1
        lstm1_out, self.hidden = self.lstm(embeds, self.hidden)

        # 3. Word Attention Pooling
        sentence_embedding = self.word_attention_layer(lstm1_out, masks)

        # 4. Sentence Global Neural Attention
        global_attn = self.sent_attention_layer(
            lstm1_out,
            sentence_embedding,
            masks,
            doc_ids=doc_ids,
            use_block_mask=use_block_mask,
        )

        # 5. Concatenate and pass to LSTM 2
        global_info = torch.cat((lstm1_out, global_attn), 2)
        lstm2_out, self.hidden2 = self.lstm2(global_info, self.hidden2)

        # 6. Linear tag projection
        lstm_feats = self.hidden2tag(lstm2_out)
        return lstm_feats

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

    def neg_log_likelihood(self, sentences, tags, masks, feats_pos=None, feats_cont=None, doc_ids=None, use_block_mask=False):
        feats = self._get_lstm_features(sentences, masks, feats_pos, feats_cont, doc_ids=doc_ids, use_block_mask=use_block_mask)
        forward_score = self._forward_alg(feats, masks)
        gold_score = self._score_sentence(feats, tags, masks)
        return (forward_score - gold_score).mean().to(sentences.device)

    def forward(self, sentence, masks, feats_pos=None, feats_cont=None, doc_ids=None, use_block_mask=False):
        lstm_feats = self._get_lstm_features(sentence, masks, feats_pos, feats_cont, doc_ids=doc_ids, use_block_mask=use_block_mask)
        score, tag_seq = self._viterbi_decode(lstm_feats, masks)
        return score.to(sentence.device), tag_seq
