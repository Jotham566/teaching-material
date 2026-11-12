"""Session 7: measure real file sizes of one small open model (SmolLM2-135M-Instruct, Apache 2.0) stored at 32, 16, 8 and 4 bits per number.
Run:  python measure_sizes.py            (downloads about 270 MB from Hugging Face on first run; writes files to ./work, results to sizes_result.json)
Method: load the published weights, convert every number to 32-bit float, then save four safetensors files:
  fp32: 4 bytes per number.  fp16: 2 bytes.  int8: one signed byte per number plus one 16-bit scale per row of each matrix.
  int4: two numbers per byte, one 16-bit scale per group of 32 numbers. Vectors (norm weights) stay 16-bit in int8 and int4 files.
This is plain round-to-nearest quantisation written for teaching. Real tools (GGUF Q4_K_M, GPTQ, AWQ) are cleverer and keep some parts at higher precision.
"""
import json, os, math, torch
from pathlib import Path
from safetensors.torch import save_file
from transformers import AutoModelForCausalLM, AutoTokenizer

REPO = 'HuggingFaceTB/SmolLM2-135M-Instruct'
W = Path(__file__).parent / 'work'
W.mkdir(exist_ok=True)
torch.manual_seed(0)
model = AutoModelForCausalLM.from_pretrained(REPO, torch_dtype=torch.float32)
tok = AutoTokenizer.from_pretrained(REPO)
sd = {k: v.detach().clone().contiguous() for k, v in model.state_dict().items()}
# tied embedding: keep one copy only
if 'lm_head.weight' in sd and torch.equal(sd['lm_head.weight'], sd['model.embed_tokens.weight']):
    del sd['lm_head.weight']
n_params = sum(v.numel() for v in sd.values())
print('stored numbers:', n_params)

def q8(t):
    s = t.abs().amax(dim=1, keepdim=True).clamp(min=1e-8) / 127
    q = torch.round(t / s).clamp(-127, 127).to(torch.int8)
    return q, s.to(torch.float16)

def q4(t, g=32):
    r, c = t.shape
    pad = (-c) % g
    tp = torch.nn.functional.pad(t, (0, pad))
    tg = tp.reshape(r, -1, g)
    s = tg.abs().amax(dim=2, keepdim=True).clamp(min=1e-8) / 7
    q = torch.round(tg / s).clamp(-8, 7).to(torch.int16) + 8      # 0..15
    q = q.reshape(-1).to(torch.uint8)
    packed = (q[0::2] | (q[1::2] << 4)).contiguous()
    return packed, s.to(torch.float16).reshape(r, -1), (r, c, pad)

def deq8(q, s): return q.float() * s.float()
def deq4(packed, s, shape, g=32):
    r, c, pad = shape
    lo = (packed & 0xF).to(torch.int16) - 8; hi = (packed >> 4).to(torch.int16) - 8
    q = torch.stack([lo, hi], 1).reshape(r, -1, g).float()
    return (q * s.float().reshape(r, -1, 1)).reshape(r, -1)[:, :c]

out = {'repo': REPO, 'stored_numbers': n_params, 'files': {}}
save_file(sd, W / 'fp32.safetensors')
save_file({k: v.to(torch.float16) for k, v in sd.items()}, W / 'fp16.safetensors')
t8, t4, d8, d4 = {}, {}, {}, {}
for k, v in sd.items():
    if v.ndim == 2:
        q, s = q8(v); t8[k] = q; t8[k + '.scale'] = s; d8[k] = deq8(q, s)
        p, s4, shp = q4(v); t4[k] = p; t4[k + '.scale'] = s4; d4[k] = deq4(p, s4, shp)
    else:
        t8[k] = v.to(torch.float16); t4[k] = v.to(torch.float16); d8[k] = d4[k] = v.to(torch.float16).float()
save_file(t8, W / 'int8.safetensors')
save_file(t4, W / 'int4.safetensors')
for name in ('fp32', 'fp16', 'int8', 'int4'):
    out['files'][name] = os.path.getsize(W / f'{name}.safetensors')
    print(name, out['files'][name], 'bytes', round(out['files'][name] / 1e6, 1), 'MB')

# Quality check: average next-word loss on three fixed sentences, using the converted numbers (dequantised back to float to run).
texts = ['Nile Valley Foods delivers maize flour, sugar and cooking oil to shops in Jinja and Kampala every week.',
         'The invoice was paid by mobile money and the customer asked us to confirm that we had received it.',
         'A model with fewer bits per number is smaller, and it can make slightly more mistakes.']
def loss_with(state):
    m = AutoModelForCausalLM.from_pretrained(REPO, torch_dtype=torch.float32)
    full = dict(state)
    if 'lm_head.weight' not in full: full['lm_head.weight'] = full['model.embed_tokens.weight']
    m.load_state_dict({k: v.float() for k, v in full.items()}, strict=False)
    m.eval(); tot = 0; n = 0
    with torch.no_grad():
        for t in texts:
            ids = tok(t, return_tensors='pt').input_ids
            tot += m(ids, labels=ids).loss.item() * (ids.shape[1] - 1); n += ids.shape[1] - 1
    nxt = None
    with torch.no_grad():
        ids = tok('The capital city of Uganda is', return_tensors='pt').input_ids
        p = torch.softmax(m(ids).logits[0, -1], -1); top = torch.topk(p, 3)
        nxt = [(tok.decode(i), round(float(v), 4)) for v, i in zip(top.values, top.indices)]
    return round(tot / n, 4), nxt
out['quality'] = {}
for name, st in (('fp32', sd), ('fp16', {k: v.to(torch.float16) for k, v in sd.items()}), ('int8', d8), ('int4', d4)):
    l, nx = loss_with(st); out['quality'][name] = {'avg_loss': l, 'top3_next_word_capital_city_of_Uganda_is': nx}
    print(name, l, nx)
json.dump(out, open(Path(__file__).parent / 'sizes_result.json', 'w'), indent=1)
