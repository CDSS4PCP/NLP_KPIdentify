"""Quick OOV / vocabulary-coverage diagnostic: public-corpus vocab vs CDSS GS.

Measures what fraction of tokens (and keyphrase tokens) in each dataset are
covered by the trained token2int vocabulary. High OOV on GS but low OOV on the
public test set would confirm a train/test domain mismatch.
"""
import json
import os
import re

ROOT = "/home/rohangoli/remote_mount"
VOCAB = json.load(open(os.path.join(ROOT, "interim_data/token2int.json")))
vocab_set = set(VOCAB.keys())


def simple_tokens(text):
    # Mirror the rough whitespace/lowercasing the pipeline applies post-normalization.
    return [t for t in re.findall(r"[A-Za-z0-9\-]+", (text or "").lower()) if t]


def coverage(path, label):
    arr = json.load(open(path))
    all_tok, oov_tok = 0, 0
    kp_tok, kp_oov = 0, 0
    for a in arr:
        text = (a.get("title", "") or "") + " " + (a.get("abstract", "") or "")
        toks = simple_tokens(text)
        for t in toks:
            all_tok += 1
            if t not in vocab_set:
                oov_tok += 1
        for kw in a.get("keywords", []):
            for t in simple_tokens(kw):
                kp_tok += 1
                if t not in vocab_set:
                    kp_oov += 1
    print(f"\n[{label}] docs={len(arr)}")
    print(f"  token OOV: {oov_tok}/{all_tok} = {100*oov_tok/max(1,all_tok):.1f}%")
    print(f"  keyphrase-token OOV: {kp_oov}/{kp_tok} = {100*kp_oov/max(1,kp_tok):.1f}%")


print(f"vocab_size = {len(vocab_set)}")
base = os.path.join(ROOT, "data/pubmed_data/json_data_kpbiomed")
coverage(os.path.join(base, "testgs42.json"), "GS42 (CDSS)")
coverage(os.path.join(base, "testgs91.json"), "GS91 (CDSS)")
coverage(os.path.join(base, "test.json"), "kpbiomed in-domain test")
