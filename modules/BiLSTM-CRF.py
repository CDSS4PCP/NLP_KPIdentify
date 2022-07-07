import torch
import torch.autograd as autograd
import torch.nn as nn
import torch.optim as optim
from torch.nn.utils.rnn import pad_sequence
# import torch.nn.functional as F

import os
import sys
import utils

import unidecode
import contractions
from nltk import sent_tokenize, word_tokenize
import nltk
import logging
import re
import string

import numpy as np

logger = logging.getLogger(__name__)
stop_words = nltk.corpus.stopwords.words('english')

#deselect 'no' and 'not' from stop words
stop_words.remove('no')
stop_words.remove('not')

english_punctuations = [',', '.', ':', ';', '``','?', '（','）','(', ')',
                '[', ']', '&', '!', '*', '@', '#', '$', '%','\\','\"','}','{','=','/','>','<','|','+','_','~']
english_punctuations_arr= ''.join(english_punctuations)

torch.manual_seed(1)

INTERIM_DATA = 'interim_data/'
START_TAG = "<START>"
STOP_TAG = "<STOP>"
EMBEDDING_DIM = 256
HIDDEN_DIM = 128
EPOCHS = 1
BATCH_SIZE = 64
# Max Sentence Length for padding
MAX_SENT_LEN = 128


def argmax(vec):
    # return the argmax as a python int
    _, idx = torch.max(vec, 1)
    return idx.item()


def prepare_sequence(seq, to_ix):
    idxs = [to_ix[w] for w in seq]
    return torch.tensor(idxs, dtype=torch.long)


# Compute log sum exp in a numerically stable way for the forward algorithm
def log_sum_exp(vec):
    max_score = vec[0, argmax(vec)]
    max_score_broadcast = max_score.view(1, -1).expand(1, vec.size()[1])
    return max_score + \
        torch.log(torch.sum(torch.exp(vec - max_score_broadcast)))

def sent2words(sent):
    '''Pre-process sentence text to words'''
    
    ## Expand Words
    sent = contractions.fix(sent)
    
    ## Convert sentence to lowercase and strip whitespaces
    sent = sent.lower().strip()
    
    ## Convert unicode characters in sentence to ASCII
    sent = unidecode.unidecode(sent)
    sent = sent.encode("ascii", "ignore").decode()
    
    ## Remove URL's from Sentence
    sent = re.sub('http[s]?://\S+', '', sent)
    
    ## Remove words like 2.0-2
    sent = re.sub(' \d*\.*\d*\-+\d*\.*\d* ', ' ', sent)
    
    # Remove punctuation characters
    sent = sent.translate(str.maketrans(english_punctuations_arr,' '*len(english_punctuations_arr)))
    
    pos, length = {}, {}
    words = word_tokenize(sent)
    for i, (w, p) in enumerate(nltk.pos_tag(words)):
        # Computational features
        pos[w] = p
        length[w] = len(w)
    
    # Remove Stop Words
    # words = [word for word in word_tokenize(sent) if not word in stop_words]
    
    # Remove punctuation only strings from sentence
    words = [word for word in words if not all(c in string.punctuation for c in word) and len(word)>1]
    
    # Remove Numericals from sentence
    words = [x for x in words if not all(c.isdigit() for c in x)] 
    
    ## Return words, POS tags, lengths of words, processed sentence
    return words, pos, length, ' '.join(words)

# Mark Keyphrases with BIO Format Labels
def mark_keyword_all_sentences(keywords, sentences):

    sentence_lengths = [len(sent) for sent in sentences]
    logger.debug("Sentence length: %s"%sentence_lengths)

    complete_text = []
    for sent in sentences:
        complete_text.extend(sent)
    logger.debug("Complete Text: %s"%complete_text)

    complete_text_len = len(complete_text)
    mapper = ['O']*complete_text_len
    kws = [sent2words(x)[0] for x in keywords]

    for kw in kws:
        kw_len=len(kw)
        if kw_len == 0:
            continue
        i=0
        while i<complete_text_len-kw_len:
            if complete_text[i:i+kw_len]==kw and mapper[i:i+kw_len]==['O']*kw_len:
                mapper[i:i+kw_len]=['I']*kw_len
                mapper[i]='B'
            i+=1

    final_mapper = []
    final_tokens = []
    start=0

    for slen in sentence_lengths:
        final_mapper.append(mapper[start:start+slen])
        final_tokens.append(complete_text[start:start+slen])
        start+=slen
    
    return complete_text, final_mapper, final_tokens


class BiLSTM_CRF(nn.Module):

    def __init__(self, vocab_size, tag_to_ix, embedding_dim, hidden_dim):
        super(BiLSTM_CRF, self).__init__()
        self.embedding_dim = embedding_dim
        self.hidden_dim = hidden_dim
        self.vocab_size = vocab_size
        self.tag_to_ix = tag_to_ix
        self.tagset_size = len(tag_to_ix)

        self.word_embeds = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim // 2,
                            num_layers=1, bidirectional=True)

        # Maps the output of the LSTM into tag space.
        self.hidden2tag = nn.Linear(hidden_dim, self.tagset_size)

        # Matrix of transition parameters.  Entry i,j is the score of
        # transitioning *to* i *from* j.
        self.transitions = nn.Parameter(
            torch.randn(self.tagset_size, self.tagset_size))

        # These two statements enforce the constraint that we never transfer
        # to the start tag and we never transfer from the stop tag
        self.transitions.data[tag_to_ix[START_TAG], :] = -10000
        self.transitions.data[:, tag_to_ix[STOP_TAG]] = -10000

        self.hidden = self.init_hidden()

    def init_hidden(self):
        ## NLayers, Batch Size, HiddenSize
        return (torch.randn(2, BATCH_SIZE, self.hidden_dim // 2),
                torch.randn(2, BATCH_SIZE, self.hidden_dim // 2))

    def _forward_alg(self, feats):
        # Do the forward algorithm to compute the partition function
        init_alphas = torch.full((1, self.tagset_size), -10000.)
        # START_TAG has all of the score.
        init_alphas[0][self.tag_to_ix[START_TAG]] = 0.

        # Wrap in a variable so that we will get automatic backprop
        forward_var = init_alphas

        # Iterate through the sentence
        for feat in feats:
            alphas_t = []  # The forward tensors at this timestep
            for next_tag in range(self.tagset_size):
                # broadcast the emission score: it is the same regardless of
                # the previous tag
                emit_score = feat[next_tag].view(
                    1, -1).expand(1, self.tagset_size)
                # the ith entry of trans_score is the score of transitioning to
                # next_tag from i
                trans_score = self.transitions[next_tag].view(1, -1)
                # The ith entry of next_tag_var is the value for the
                # edge (i -> next_tag) before we do log-sum-exp
                next_tag_var = forward_var + trans_score + emit_score
                # The forward variable for this tag is log-sum-exp of all the
                # scores.
                alphas_t.append(log_sum_exp(next_tag_var).view(1))
            forward_var = torch.cat(alphas_t).view(1, -1)
        terminal_var = forward_var + self.transitions[self.tag_to_ix[STOP_TAG]]
        alpha = log_sum_exp(terminal_var)
        return alpha

    def _get_lstm_features(self, sentences):
        self.hidden = self.init_hidden()
        print('_get_lstm_features : ',sentences.shape)
        embeds = self.word_embeds(sentences).view(MAX_SENT_LEN, BATCH_SIZE, -1)
        print('embeds: ',embeds.shape)
        lstm_out, self.hidden = self.lstm(embeds, self.hidden)
        print("lstm_out:",lstm_out.shape, ' Hidden0: ',self.hidden[0].shape,' Hidden1: ', self.hidden[1].shape)
        lstm_out = lstm_out.view(BATCH_SIZE, MAX_SENT_LEN, self.hidden_dim)
        print(lstm_out.shape)
        lstm_feats = self.hidden2tag(lstm_out)
        print('lstm_feats', lstm_feats.shape)
        return lstm_feats

    def _score_sentence(self, feats, tags):
        # Gives the score of a provided tag sequence
        score = torch.zeros(1)
        tags = torch.cat([torch.tensor([self.tag_to_ix[START_TAG]], dtype=torch.long), tags])
        for i, feat in enumerate(feats):
            score = score + \
                self.transitions[tags[i + 1], tags[i]] + feat[tags[i + 1]]
        score = score + self.transitions[self.tag_to_ix[STOP_TAG], tags[-1]]
        return score

    def _viterbi_decode(self, feats):
        backpointers = []

        # Initialize the viterbi variables in log space
        init_vvars = torch.full((1, self.tagset_size), -10000.)
        init_vvars[0][self.tag_to_ix[START_TAG]] = 0

        # forward_var at step i holds the viterbi variables for step i-1
        forward_var = init_vvars
        for feat in feats:
            bptrs_t = []  # holds the backpointers for this step
            viterbivars_t = []  # holds the viterbi variables for this step

            for next_tag in range(self.tagset_size):
                # next_tag_var[i] holds the viterbi variable for tag i at the
                # previous step, plus the score of transitioning
                # from tag i to next_tag.
                # We don't include the emission scores here because the max
                # does not depend on them (we add them in below)
                next_tag_var = forward_var + self.transitions[next_tag]
                best_tag_id = argmax(next_tag_var)
                bptrs_t.append(best_tag_id)
                viterbivars_t.append(next_tag_var[0][best_tag_id].view(1))
            # Now add in the emission scores, and assign forward_var to the set
            # of viterbi variables we just computed
            forward_var = (torch.cat(viterbivars_t) + feat).view(1, -1)
            backpointers.append(bptrs_t)

        # Transition to STOP_TAG
        terminal_var = forward_var + self.transitions[self.tag_to_ix[STOP_TAG]]
        best_tag_id = argmax(terminal_var)
        path_score = terminal_var[0][best_tag_id]

        # Follow the back pointers to decode the best path.
        best_path = [best_tag_id]
        for bptrs_t in reversed(backpointers):
            best_tag_id = bptrs_t[best_tag_id]
            best_path.append(best_tag_id)
        # Pop off the start tag (we dont want to return that to the caller)
        start = best_path.pop()
        assert start == self.tag_to_ix[START_TAG]  # Sanity check
        best_path.reverse()
        return path_score, best_path

    def neg_log_likelihood(self, sentences, tags):
        print("neg_log_likelihood: ",sentences.shape, tags.shape)
        feats = self._get_lstm_features(sentences)
        gold_score = self._score_sentence(feats, tags)
        return forward_score - gold_score

    def forward(self, sentence):  # dont confuse this with _forward_alg above.
        # Get the emission scores from the BiLSTM
        lstm_feats = self._get_lstm_features(sentence)

        # Find the best path, given the features.
        score, tag_seq = self._viterbi_decode(lstm_feats)
        return score, tag_seq

print('START >>> Read Data')
## Make up some training data
train_data = utils.read_json_array(os.path.join(INTERIM_DATA, "train.json"))
test_data = utils.read_json_array(os.path.join(INTERIM_DATA, "test.json"))

training_data = []
for article in train_data:
    _, labels, sentences = mark_keyword_all_sentences(article['keywords'], article['sentences'])
    for x,y in zip(sentences, labels):
        if len(x)>3:
            training_data.append((x,y))

testing_data = []
for article in test_data:
    _, labels, sentences = mark_keyword_all_sentences(article['keywords'], article['sentences'])
    for x,y in zip(sentences, labels):
        if len(x)>3:
            testing_data.append((x,y))

## Load Vocab
word_to_ix = utils.read_json_array("token2int.json")

tag_to_ix = {"O": 0, "B": 1, "I": 2, START_TAG: 3, STOP_TAG: 4}
print('END >>> Read Data')

model = BiLSTM_CRF(len(word_to_ix), tag_to_ix, EMBEDDING_DIM, HIDDEN_DIM)
optimizer = optim.SGD(model.parameters(), lr=0.01, weight_decay=1e-4)

# # Check predictions before training
# with torch.no_grad():
#     precheck_sent = prepare_sequence(testing_data[0][0], word_to_ix)
#     precheck_tags = torch.tensor([tag_to_ix[t] for t in testing_data[0][1]], dtype=torch.long)
#     print(model(precheck_sent))

def get_batches(data, batch_size):    
    # iterate through the arrays
    prv = 0
    for n in range(batch_size, len(data), batch_size):
        # print("Prev={}, N={}".format(prv,n))
        data_x = []
        data_masks = []
        data_y = []
        for x,y in data[prv:n]:
            idxs = [word_to_ix[w] for w in x]
            data_masks.append(torch.tensor([1 if idx else 0 for idx in idxs], dtype=torch.long))
            data_x.append(torch.tensor(idxs, dtype=torch.long))
            data_y.append(torch.tensor([tag_to_ix[t] for t in y], dtype=torch.long))

        # pad first seq to desired length
        data_x[0] = nn.ConstantPad1d((0, MAX_SENT_LEN - data_x[0].shape[0]), 0)(data_x[0])
        data_y[0] = nn.ConstantPad1d((0, MAX_SENT_LEN - data_y[0].shape[0]), 0)(data_y[0])
        data_masks[0] = nn.ConstantPad1d((0, MAX_SENT_LEN - data_masks[0].shape[0]), 0)(data_masks[0])
        
        # pad all seqs to desired length
        data_x_pad = pad_sequence(data_x, batch_first= True)
        data_y_pad = pad_sequence(data_y, batch_first= True)
        data_masks_pad = pad_sequence(data_masks, batch_first= True)
        
        # Convert list of tensors to tuple
        data_x_tuple = tuple(data_x_pad)
        data_y_tuple = tuple(data_y_pad)
        data_masks_tuple = tuple(data_masks_pad)
        
        # Convert tuple of tensors to Stack of Tensors
        data_x = torch.stack(data_x_tuple)
        data_y = torch.stack(data_y_tuple)
        data_masks = torch.stack(data_masks_tuple)
        
        prv = n
        
        yield data_x, data_y, data_masks
        
print('START >>> Train')
model.train()

# counter=0
# for inputs, targets, masks in get_batches(training_data, BATCH_SIZE):
#     print(inputs.shape, targets.shape, masks.shape)
#     print(inputs[0], targets[0], masks[0])
#     counter+=1
#     if counter>10:
#         break
# sys.exit(0)

# Make sure prepare_sequence from earlier in the LSTM section is loaded
for epoch in range(EPOCHS):
    losses= []
    for inputs, targets in get_batches(training_data, BATCH_SIZE):
        # Step 1. Remember that Pytorch accumulates gradients.
        # We need to clear them out before each instance
        model.zero_grad()

        # Step 2. Get our inputs ready for the network, that is,
        # turn them into Tensors of word indices.
        # targets = torch.tensor(targets, dtype=torch.long)
        #inputs, targets = inputs.cuda(), targets.cuda()

        # Step 3. Run our forward pass.
        loss = model.neg_log_likelihood(inputs, targets)
        losses.append(loss.detach().item())

        # Step 4. Compute the loss, gradients, and update the parameters by
        # calling optimizer.step()
        loss.backward()
        optimizer.step()
    print("Epoch: {}/{} Loss: {}".format(epoch,EPOCHS,np.mean(losses)))
print('END >>> Train')

print('START >>> Test')
# Check predictions after training
model.eval()
with torch.no_grad():
    precheck_sent = prepare_sequence(testing_data[0][0], word_to_ix)
    print(model(precheck_sent))
    print(testing_data[0])
print('END >>> Test')