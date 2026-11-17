"""FICTIONAL data for Session 2: 240 staff expense claims for the made-up company Nile Valley Foods Ltd. Fixed seed 2026.
How it is made (so nobody mistakes it for real data): amounts, receipts and delay are drawn at random; a claim is marked 'queried'
by a rule the author wrote (no receipt over UGX 50,000, or over UGX 800,000, or filed more than 30 days late) with about 8 percent of labels flipped at random
to imitate human inconsistency.  A tree that finds the rule is therefore rediscovering what we put in; the point is to show how a tree reads structured data.
Run: python make_expenses.py -> expenses_fictional.csv"""
import csv
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent
rng = np.random.default_rng(2026)
N = 240
cats = ['fuel', 'meals', 'transport hire', 'airtime', 'repairs', 'stationery']
rows = []
for i in range(N):
    cat = cats[rng.integers(len(cats))]
    amount = int(np.round(rng.lognormal(mean=11.3, sigma=1.0), -3))           # median about UGX 80,000
    amount = int(min(max(amount, 5000), 2_500_000))
    receipt = int(rng.random() < 0.72)
    days = int(min(rng.exponential(12), 90))
    queried = (receipt == 0 and amount > 50_000) or amount > 800_000 or days > 30
    if rng.random() < 0.08:
        queried = not queried
    rows.append(dict(claim_id=f'E{i + 1:03d}', category=cat, amount_ugx=amount, receipt_attached=receipt, days_to_file=days, outcome='queried' if queried else 'paid'))
with open(HERE / 'expenses_fictional.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
print(N, 'fictional claims written;', sum(r['outcome'] == 'queried' for r in rows), 'queried')
