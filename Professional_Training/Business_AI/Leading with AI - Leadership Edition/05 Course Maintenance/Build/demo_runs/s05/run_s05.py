"""Session 5 real runs. GPT-2 small (124M), transformers, run on a laptop CPU. Writes results.json next to this file.
Run:  python run_s05.py   (first run downloads gpt2)"""
import json, math, pathlib, torch, tiktoken, transformers
from transformers import AutoTokenizer, AutoModelForCausalLM
OUT = pathlib.Path(__file__).parent
torch.manual_seed(5)
tok = AutoTokenizer.from_pretrained('gpt2')
model = AutoModelForCausalLM.from_pretrained('gpt2', attn_implementation='eager').eval()
enc = tiktoken.get_encoding('gpt2')
res = {'versions': {'transformers': transformers.__version__, 'torch': torch.__version__, 'tiktoken': tiktoken.__version__}}

# 1 tokenisation
sents = ['Nile Valley Foods delivers maize flour to Mbale.',
         'Invoice INV-2041 for UGX 1,250,000 is overdue.',
         'Busoga Oils Ltd renewed the supply agreement automatically.',
         'Unbelievably, the warehouse was reorganised.',
         'Habari, tunataka sukari magunia kumi.']
res['tokens'] = []
for s in sents:
    ids = tok(s)['input_ids']
    assert ids == enc.encode(s)
    res['tokens'].append({'text': s, 'pieces': [tok.decode([i]) for i in ids], 'ids': ids, 'n_words': len(s.split())})

# 2 next-word probabilities
def next_probs(prompt, k=10, temp=1.0):
    ids = tok(prompt, return_tensors='pt')
    with torch.no_grad():
        logits = model(**ids).logits[0, -1]
    p = torch.softmax(logits / temp, -1)
    top = torch.topk(p, k)
    return logits, [(tok.decode([i]), float(v)) for v, i in zip(top.values, top.indices)]
prompts = ['The capital of Uganda is', 'Please pay the invoice within thirty', 'Nile Valley Foods is a food distributor based in',
           'The customer was angry because the delivery was']
res['next'] = []
for p in prompts:
    lg, top = next_probs(p)
    res['next'].append({'prompt': p, 'top10': top, 'top10_mass': sum(v for _, v in top)})

# 3 temperature
tp = 'The customer was angry because the delivery was'
lg, _ = next_probs(tp)
res['temp'] = {'prompt': tp, 'settings': []}
for T in (0.2, 1.0, 1.8):
    pr = torch.softmax(lg / T, -1)
    top = torch.topk(pr, 8)
    ids = tok(tp, return_tensors='pt')
    samples = []
    for i in range(6):
        torch.manual_seed(100 + i)
        out = model.generate(**ids, do_sample=True, temperature=T, top_k=0, top_p=1.0, max_new_tokens=14, pad_token_id=tok.eos_token_id)
        samples.append(tok.decode(out[0, ids['input_ids'].shape[1]:]).replace('\n', ' '))
    res['temp']['settings'].append({'T': T, 'top8': [(tok.decode([i]), float(v)) for v, i in zip(top.values, top.indices)], 'samples': samples})

# 4 attention
ap = 'The supplier sent the invoice to the manager because she needed it'
ids = tok(ap, return_tensors='pt')
with torch.no_grad():
    o = model(**ids, output_attentions=True)
att = torch.stack([a[0] for a in o.attentions])  # layers, heads, q, k
res['attn_tokens'] = [tok.decode([i]) for i in ids['input_ids'][0]]
# choose head: print last-token row for each layer/head, store layer 5 head 1 plus a search for a head where last token attends to 'manager'/'supplier'
res['attn_all_last'] = {}
mi = res['attn_tokens'].index(' manager'); si = res['attn_tokens'].index(' supplier'); inv = res['attn_tokens'].index(' invoice')
cands = []
for L in range(12):
    for H in range(12):
        row = att[L, H, -1]
        # ignore first token sink
        rest = row[1:]
        cands.append((float(row[mi]), L, H, float(row[si]), float(row[inv]), float(row[0])))
cands.sort(reverse=True)
res['attn_cands'] = cands[:12]
json.dump(res, open(OUT / 'results.json', 'w'), indent=1)
print(json.dumps({k: res[k] for k in ('tokens', 'next', 'attn_tokens', 'attn_cands')}, indent=1)[:6000])
print(json.dumps(res['temp'], indent=1))

# 5 attention: the chosen head (found by searching all 144 heads for one where ' it' looks mostly at ' invoice')
L, H = 4, 3
res['attn_head'] = {'layer_index0': L, 'head_index0': H, 'matrix': [[round(float(x), 3) for x in r] for r in att[L, H]]}
last = att[:, :, -1, :]
res['attn_stats'] = {'heads': 144, 'first_word_over_half': int((last[:, :, 0] > 0.5).sum()), 'it_on_invoice_over_30pct': int((last[:, :, 4] > 0.3).sum())}
res['attn_grid_first'] = [[round(float(last[l, h, 0]), 2) for h in range(12)] for l in range(12)]
res['attn_grid_invoice'] = [[round(float(last[l, h, 4]), 2) for h in range(12)] for l in range(12)]
res['gpt2_config'] = {'layers': model.config.n_layer, 'heads': model.config.n_head, 'context': model.config.n_positions, 'vocab': model.config.vocab_size, 'parameters': sum(p.numel() for p in model.parameters())}
print(res['attn_stats'], res['gpt2_config'])
json.dump(res, open(OUT / 'results.json', 'w'), indent=1)
