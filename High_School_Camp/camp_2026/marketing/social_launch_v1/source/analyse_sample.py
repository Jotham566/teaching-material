"""Reproduce the fictional shop example. No real customer or student data."""
from pathlib import Path
import csv,json
from collections import defaultdict
r=Path(__file__).resolve().parent
rows=[('Notebook',12,3000),(' notebook ',8,3000),('Pen',30,1000),('pen',10,1000),('Juice',15,2000),('juice',5,2000)]
with (r/'sample_sales_raw.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['product','quantity','unit_price_ugx']);w.writerows(rows)
totals=defaultdict(lambda:{'units':0,'revenue_ugx':0})
for name,q,p in rows:
 key=name.strip().title();totals[key]['units']+=q;totals[key]['revenue_ugx']+=q*p
assert totals=={'Notebook':{'units':20,'revenue_ugx':60000},'Pen':{'units':40,'revenue_ugx':40000},'Juice':{'units':20,'revenue_ugx':40000}}
(r/'sample_sales_summary.json').write_text(json.dumps(totals,indent=2))
print(json.dumps(totals))
