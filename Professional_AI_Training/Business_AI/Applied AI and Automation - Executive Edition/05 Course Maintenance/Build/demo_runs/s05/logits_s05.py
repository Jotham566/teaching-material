"""Session 5, explain-before-use rework (11 November 2026).
Records the RAW logits (scores) GPT-2 small gives to the most likely next tokens, so the slides can show the score
for each possible next token before softmax. The course venv on 11 November 2026 had no torch, so this script runs
GPT-2 small with numpy only, reading the same downloaded weights (Hugging Face 'gpt2', model.safetensors) and the
same tokenizer files (vocab.json, merges.txt). Check: it reproduces the token ids and the softmax probabilities that
run_s05.py recorded with transformers on 6 November 2026 (see the CHECK lines it prints).
Usage: python logits_s05.py     (writes logits_run_2026-11-11.json next to this file)"""
import json, re, platform
from pathlib import Path
import numpy as np

SNAP = sorted((Path.home() / '.cache/huggingface/hub/models--gpt2/snapshots').iterdir())[0]
HERE = Path(__file__).resolve().parent

# ---------------- weights (safetensors: 8-byte header length, JSON header, raw little-endian data)
raw = (SNAP / 'model.safetensors').read_bytes()
n = int.from_bytes(raw[:8], 'little'); hdr = json.loads(raw[8:8 + n]); base = 8 + n
W = {}
for k, v in hdr.items():
    if k == '__metadata__':
        continue
    a, b = v['data_offsets']; assert v['dtype'] == 'F32'
    W[k.replace('transformer.', '')] = np.frombuffer(raw[base + a:base + b], dtype='<f4').reshape(v['shape'])
cfg = json.loads((SNAP / 'config.json').read_text()); L, H = cfg['n_layer'], cfg['n_head']

# ---------------- byte-level BPE tokenizer (GPT-2)
def bytes_to_unicode():
    bs = list(range(ord('!'), ord('~') + 1)) + list(range(ord('¡'), ord('¬') + 1)) + list(range(ord('®'), ord('ÿ') + 1))
    cs = bs[:]; k = 0
    for b in range(256):
        if b not in bs:
            bs.append(b); cs.append(256 + k); k += 1
    return dict(zip(bs, map(chr, cs)))
B2U = bytes_to_unicode()
ENC = json.loads((SNAP / 'vocab.json').read_text()); DEC = {v: k for k, v in ENC.items()}
U2B = {v: k for k, v in B2U.items()}
RANK = {tuple(l.split()): i for i, l in enumerate((SNAP / 'merges.txt').read_text().split('\n')[1:]) if l.strip()}
PAT = re.compile(r"""'s|'t|'re|'ve|'m|'ll|'d| ?[^\W\d_]+| ?\d+| ?[^\s\w]+|\s+(?!\S)|\s+""")

def bpe(word):
    parts = list(word)
    while len(parts) > 1:
        pairs = [(RANK.get((parts[i], parts[i + 1]), 1e18), i) for i in range(len(parts) - 1)]
        r, i = min(pairs)
        if r == 1e18:
            break
        a, b = parts[i], parts[i + 1]; new = []; j = 0
        while j < len(parts):
            if j < len(parts) - 1 and parts[j] == a and parts[j + 1] == b:
                new.append(a + b); j += 2
            else:
                new.append(parts[j]); j += 1
        parts = new
    return parts

def encode(text):
    return [ENC[t] for w in PAT.findall(text) for t in bpe(''.join(B2U[c] for c in w.encode('utf-8')))]

def decode(ids):
    return bytes(U2B[c] for i in ids for c in DEC[i]).decode('utf-8', errors='replace')

# ---------------- GPT-2 forward pass
def ln(x, g, b, eps=1e-5):
    m = x.mean(-1, keepdims=True); v = x.var(-1, keepdims=True)
    return g * (x - m) / np.sqrt(v + eps) + b

def gelu(x):
    return 0.5 * x * (1 + np.tanh(np.sqrt(2 / np.pi) * (x + 0.044715 * x ** 3)))

def softmax(x):
    e = np.exp(x - x.max(-1, keepdims=True)); return e / e.sum(-1, keepdims=True)

def logits(ids):
    T = len(ids); x = W['wte.weight'][ids] + W['wpe.weight'][:T]
    mask = np.triu(np.full((T, T), -1e10, dtype=np.float32), 1)
    for l in range(L):
        p = 'h.%d.' % l
        a = ln(x, W[p + 'ln_1.weight'], W[p + 'ln_1.bias'])
        qkv = a @ W[p + 'attn.c_attn.weight'] + W[p + 'attn.c_attn.bias']
        q, k, v = np.split(qkv, 3, -1); d = q.shape[-1] // H
        heads = []
        for h in range(H):
            sl = slice(h * d, (h + 1) * d)
            heads.append(softmax(q[:, sl] @ k[:, sl].T / np.sqrt(d) + mask) @ v[:, sl])
        x = x + np.hstack(heads) @ W[p + 'attn.c_proj.weight'] + W[p + 'attn.c_proj.bias']
        a = ln(x, W[p + 'ln_2.weight'], W[p + 'ln_2.bias'])
        x = x + gelu(a @ W[p + 'mlp.c_fc.weight'] + W[p + 'mlp.c_fc.bias']) @ W[p + 'mlp.c_proj.weight'] + W[p + 'mlp.c_proj.bias']
    x = ln(x, W['ln_f.weight'], W['ln_f.bias'])
    return (x[-1] @ W['wte.weight'].T).astype(np.float64)

# ---------------- check against the 6 November record, then record the logits
REC = json.loads((HERE / 'results.json').read_text())
for t in REC['tokens']:
    ok = encode(t['text']) == t['ids']
    print('CHECK token ids', 'match' if ok else 'DIFFER', '|', t['text'])
prompts = ['Please pay the invoice within thirty', 'Thank you for your', 'The customer was angry because the delivery was']
out = dict(date='11 November 2026', model='GPT-2 small (124M), Hugging Face gpt2 weights, snapshot ' + SNAP.name,
           engine='numpy %s, Python %s (no torch in the venv); forward pass written out in this file' % (np.__version__, platform.python_version()), runs=[])
for pr in prompts:
    ids = encode(pr); z = logits(ids); p = softmax(z)
    top = np.argsort(-z)[:10]
    rows = [dict(token=decode([int(i)]), id=int(i), logit=round(float(z[i]), 3), prob=round(float(p[i]), 5)) for i in top]
    out['runs'].append(dict(prompt=pr, tokens=[decode([i]) for i in ids], token_ids=ids, vocab=int(z.shape[0]),
                            logit_min=round(float(z.min()), 3), logit_max=round(float(z.max()), 3), top10=rows))
    rec = [r for r in REC['next'] if r['prompt'] == pr]
    if rec:
        diff = max(abs(a['prob'] - b[1]) for a, b in zip(rows, rec[0]['top10']))
        same = [a['token'] for a in rows] == [b[0] for b in rec[0]['top10']]
        print('CHECK against 6 Nov record: same top-10 tokens:', same, '| largest probability difference %.5f' % diff)
    print(pr, '| ids', ids)
    for r in rows[:5]:
        print('   %-12r logit %8.3f  prob %6.2f%%' % (r['token'], r['logit'], 100 * r['prob']))
    print('   lowest logit %.2f, highest %.2f over %d tokens' % (z.min(), z.max(), z.shape[0]))
# ---------------- chain of probabilities for a short sentence (each token given the ones before it)
out['chains'] = []
for sent in ['Thank you for your support', 'Please pay the invoice within thirty days']:
    ids = encode(sent); chain = []
    for t in range(1, len(ids)):
        p = softmax(logits(ids[:t]))
        chain.append(dict(given=decode(ids[:t]), token=decode([ids[t]]), prob=round(float(p[ids[t]]), 5), loss=round(float(-np.log(p[ids[t]])), 4)))
    prod = float(np.prod([c['prob'] for c in chain]))
    out['chains'].append(dict(sentence=sent, first_token_given=decode(ids[:1]), steps=chain, product=prod,
                              average_loss=round(float(np.mean([c['loss'] for c in chain])), 4)))
    print('CHAIN', sent); [print('   P(%r | %r) = %.4f  loss %.3f' % (c['token'], c['given'], c['prob'], c['loss'])) for c in chain]
    print('   product %.8f, average loss %.3f' % (prod, out['chains'][-1]['average_loss']))
# ---------------- embedding row plus position row for " invoice" at position 4 of "Please pay the invoice"
ids = encode('Please pay the invoice'); t = 3
E = W['wte.weight'][ids[t]][:4]; P = W['wpe.weight'][t][:4]
out['lookup'] = dict(sentence='Please pay the invoice', token=decode([ids[t]]), token_id=ids[t], position_index0=t, position_counted_from_1=t + 1,
                     E_first4=[round(float(v), 4) for v in E], P_first4=[round(float(v), 4) for v in P], sum_first4=[round(float(v), 4) for v in E + P],
                     numbers_per_row=int(W['wte.weight'].shape[1]), token_rows=int(W['wte.weight'].shape[0]), position_rows=int(W['wpe.weight'].shape[0]))
print('LOOKUP', out['lookup'])
# ---------------- size of one block and of the feed-forward network (Session 1 neurons)
blk = {k: v.size for k, v in W.items() if k.startswith('h.0.') and k not in ('h.0.attn.bias', 'h.0.attn.masked_bias')}   # attn.bias is the stored causal mask, not a parameter
out['block0'] = dict(total=int(sum(blk.values())), attention=int(sum(v for k, v in blk.items() if '.attn.' in k)),
                     feed_forward=int(sum(v for k, v in blk.items() if '.mlp.' in k)), layer_norm=int(sum(v for k, v in blk.items() if '.ln_' in k)),
                     ff_hidden_neurons=int(W['h.0.mlp.c_fc.weight'].shape[1]), ff_inputs=int(W['h.0.mlp.c_fc.weight'].shape[0]))
print('BLOCK0', out['block0'])
(HERE / 'logits_run_2026-11-11.json').write_text(json.dumps(out, indent=1))
