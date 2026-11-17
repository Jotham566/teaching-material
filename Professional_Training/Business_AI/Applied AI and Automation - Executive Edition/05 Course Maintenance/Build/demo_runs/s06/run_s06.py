"""Session 6: the same task on a small open instruct model run locally (Qwen2.5-1.5B-Instruct, transformers, Apple laptop GPU (MPS, float16); falls back to CPU).
Greedy decoding (repeatable), plus 2 sampled runs at temperature 0.7. Writes qwen_runs.json."""
import json, pathlib, time, torch, transformers
from transformers import AutoTokenizer, AutoModelForCausalLM
D = pathlib.Path(__file__).parent
name = 'Qwen/Qwen2.5-1.5B-Instruct'
tok = AutoTokenizer.from_pretrained(name); dev = 'mps' if torch.backends.mps.is_available() else 'cpu'
m = AutoModelForCausalLM.from_pretrained(name, dtype=torch.float16 if dev == 'mps' else torch.float32).to(dev).eval()
task = (D / 'prompts/comparison_task.txt').read_text().strip()
ids = tok.apply_chat_template([{'role': 'user', 'content': task}], add_generation_prompt=True, return_tensors='pt', return_dict=True).to(dev)
runs = []
for label, kw, seed in (('greedy', dict(do_sample=False), 0), ('sampled temp 0.7 seed 1', dict(do_sample=True, temperature=0.7, top_p=1.0, top_k=0), 1), ('sampled temp 0.7 seed 2', dict(do_sample=True, temperature=0.7, top_p=1.0, top_k=0), 2)):
    torch.manual_seed(seed); t = time.time()
    with torch.no_grad():
        out = m.generate(**ids, max_new_tokens=400, **kw)
    runs.append({'setting': label, 'seconds': round(time.time() - t, 1), 'reply': tok.decode(out[0, ids['input_ids'].shape[1]:], skip_special_tokens=True)})
    print(label, runs[-1]['seconds'], 's\n', runs[-1]['reply'], '\n-----')
json.dump({'device': dev, 'model': name, 'transformers': transformers.__version__, 'torch': torch.__version__, 'runs': runs}, open(D / 'qwen_runs.json', 'w'), indent=1)

# base model vs instruct model: GPT-2 (no post-training) given the same task text, greedy, 80 new tokens
g_tok = AutoTokenizer.from_pretrained('gpt2'); g = AutoModelForCausalLM.from_pretrained('gpt2').eval()
gi = g_tok(task, return_tensors='pt')
with torch.no_grad():
    go = g.generate(**gi, max_new_tokens=80, do_sample=False, pad_token_id=g_tok.eos_token_id)
base = g_tok.decode(go[0, gi['input_ids'].shape[1]:])
print('GPT-2 base continuation:\n', base)
d = json.load(open(D / 'qwen_runs.json')); d['gpt2_base_greedy'] = base; json.dump(d, open(D / 'qwen_runs.json', 'w'), indent=1)
