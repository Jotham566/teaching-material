"""Session 9 demonstration: a tiny LoRA fine-tune that teaches a house style.
Base model: GPT-2 (124 million parameters, open weights). Method: LoRA (peft 0.21.2), rank 8, on the attention layers.
Data: 48 invented NVF customer messages with replies written in one fixed house style (greeting, one sentence, fixed sign-off), built from templates in this file.
Test: 6 NEW customer messages. We count how many replies end with the house sign-off before and after. Greedy decoding, so a re-run gives the same text.
Run:  python lora_style.py     (about 2 minutes on a laptop CPU; writes lora_results.json)
"""
import json, random, time
from pathlib import Path
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import LoraConfig, get_peft_model
import peft, transformers

torch.manual_seed(0); random.seed(0)
HERE = Path(__file__).parent
SIGN = 'Thank you for choosing Nile Valley Foods. Customer Care, Jinja'
items = [('my maize flour order has not arrived', 'We are sorry your maize flour is late. We will tell you the new delivery time today.'),
         ('please send me the price of 20L cooking oil', 'The price list for cooking oil is on its way to you by email today.'),
         ('I was charged twice for my last invoice', 'We are sorry about the double charge. Finance will check it and refund any extra amount.'),
         ('can I change my delivery from Tuesday to Friday', 'Yes, we can move your delivery to Friday. We will confirm the time today.'),
         ('one bag of rice was damaged', 'We are sorry about the damaged rice. We will replace the bag on the next delivery.'),
         ('do you deliver sugar to Soroti', 'Yes, we deliver sugar to Soroti every Wednesday. We can add your shop to the route.'),
         ('I need a receipt for last week', 'We will email you the receipt for last week today.'),
         ('how do I pay with Airtel Money', 'You can pay with Airtel Money on delivery. The driver will show you the number to use.')]
names = ['Mr Okello', 'Ms Nabirye', 'Mr Kato', 'Ms Akello', 'Mr Mugisha', 'Ms Namukasa']
train = []
for i in range(48):
    msg, rep = items[i % len(items)]
    n = names[(i * 5) % len(names)]
    train.append((f'Customer: {msg}\nReply:', f' Hello {n}. {rep} {SIGN}.'))
test = ['can you deliver beans to Mbale next week', 'the invoice shows the wrong quantity of sugar', 'I want to cancel my order for rice',
        'when will my cooking oil arrive', 'please change my phone number on the account', 'my truck delivery was two hours late']

tok = AutoTokenizer.from_pretrained('gpt2'); tok.pad_token = tok.eos_token
model = AutoModelForCausalLM.from_pretrained('gpt2')

def gen(m, prompt):
    ids = tok(prompt, return_tensors='pt')
    with torch.no_grad():
        out = m.generate(**ids, max_new_tokens=45, do_sample=False, pad_token_id=tok.eos_token_id)
    txt = tok.decode(out[0][ids['input_ids'].shape[1]:], skip_special_tokens=True)
    return txt.split('\nCustomer:')[0].strip()

def run(m):
    return [gen(m, f'Customer: {t}\nReply:') for t in test]

before = run(model)
total = sum(p.numel() for p in model.parameters())
cfg = LoraConfig(r=8, lora_alpha=16, target_modules=['c_attn'], lora_dropout=0.0, fan_in_fan_out=True, task_type='CAUSAL_LM')
pm = get_peft_model(model, cfg)
trainable = sum(p.numel() for p in pm.parameters() if p.requires_grad)
print(f'total {total:,}  trainable {trainable:,}  = {100 * trainable / total:.2f} percent')
opt = torch.optim.AdamW([p for p in pm.parameters() if p.requires_grad], lr=2e-3)
pm.train(); t0 = time.time(); losses = []
for epoch in range(4):
    random.shuffle(train)
    for k in range(0, len(train), 8):
        batch = train[k:k + 8]
        enc = tok([a + b + tok.eos_token for a, b in batch], return_tensors='pt', padding=True)
        labels = enc['input_ids'].clone(); labels[enc['attention_mask'] == 0] = -100
        loss = pm(**enc, labels=labels).loss
        loss.backward(); opt.step(); opt.zero_grad(); losses.append(float(loss))
    print('epoch', epoch + 1, 'loss', round(sum(losses[-6:]) / 6, 3))
pm.eval()
after = run(pm)
ok = lambda L: sum(SIGN in x for x in L)
print(f'training time {time.time() - t0:.0f} s')
print(f'house sign-off present: before {ok(before)} of {len(test)}, after {ok(after)} of {len(test)}')
for t, b, a in zip(test, before, after):
    print('\nCUSTOMER:', t, '\nBEFORE:', b, '\nAFTER:', a)
json.dump({'versions': {'peft': peft.__version__, 'transformers': transformers.__version__, 'torch': torch.__version__},
           'total_params': total, 'trainable_params': trainable, 'epochs': 4, 'train_examples': len(train), 'losses': losses,
           'signoff': SIGN, 'before': before, 'after': after, 'tests': test}, open(HERE / 'lora_results.json', 'w'), indent=1)
