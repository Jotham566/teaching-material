"""Live demonstration for Session 5. Usage:
  python live_s05.py "Please pay the invoice within thirty"            # tokens and top 10 next pieces
  python live_s05.py "The customer was angry because the delivery was" 0.2 1.0 1.8   # also sample 4 completions at each temperature
Model: GPT-2 small (124M), CPU, a few seconds."""
import sys, torch
from transformers import AutoTokenizer, AutoModelForCausalLM
tok = AutoTokenizer.from_pretrained('gpt2'); m = AutoModelForCausalLM.from_pretrained('gpt2').eval()
prompt = sys.argv[1]; temps = [float(t) for t in sys.argv[2:]]
ids = tok(prompt, return_tensors='pt')
print('TOKENS:', [tok.decode([i]) for i in ids['input_ids'][0]], len(ids['input_ids'][0]), 'tokens')
with torch.no_grad():
    p = torch.softmax(m(**ids).logits[0, -1], -1)
top = torch.topk(p, 10)
print('TOP 10 NEXT PIECES:')
for v, i in zip(top.values, top.indices):
    print(f'  {tok.decode([i])!r:14} {100 * float(v):5.1f}%')
for T in temps:
    print(f'--- temperature {T}')
    for k in range(4):
        torch.manual_seed(k)
        out = m.generate(**ids, do_sample=True, temperature=T, top_k=0, max_new_tokens=14, pad_token_id=tok.eos_token_id)
        print('  ', repr(tok.decode(out[0, ids['input_ids'].shape[1]:])))
