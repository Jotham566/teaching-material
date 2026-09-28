"""Verify S15 reported measure values; never claim to execute a Power BI model.

Read a plain numeric appendix from a supported document in the isolated
renderer. This supplies a 20-mark component, not a final assessment result.
"""
import argparse,csv,hashlib,json,math,re
from pathlib import Path
HERE=Path(__file__).resolve().parent
DATA=HERE.parents[1]/'DataAnalysis_Track/data'
CONTEXTS={'ALL':(None,None),'2024':('2024',None),'2025':('2025',None),'2025_CENTRAL':('2025','Central'),'2025_WESTERN':('2025','Western')}

def reference(orders,lines,reps):
 regions={r['rep_id']:r['region'] for r in reps};result={}
 for context,(year,region) in CONTEXTS.items():
  selected={o['order_id'] for o in orders if o['status']=='Delivered' and (year is None or o['order_date'][:4]==year) and (region is None or regions[o['rep_id']]==region)}
  amount=sum(float(r['quantity'])*float(r['unit_price_ugx'])*(1-float(r['discount'])) for r in lines if r['order_id'] in selected)
  if not selected:raise ValueError('The issued reference context has no delivered orders')
  result[context]=dict(revenue=amount,orders=len(selected),aov=amount/len(selected))
 return result

def load_reference():
 manifest=json.loads((HERE/'specs/hidden/S15_source_hashes.json').read_text());tables=[]
 for name in ('orders.csv','order_items.csv','reps.csv'):
  raw=(DATA/name).read_bytes()
  if hashlib.sha256(raw).hexdigest()!=manifest[name]:raise ValueError('S15 source changed; version and revalidate the assessment')
  with (DATA/name).open(newline='') as f:tables.append(list(csv.DictReader(f)))
 return reference(*tables)

def assess_text(text,expected):
 # One line per context. No expressions, path names or executable SQL accepted.
 rows={}
 for line in text.splitlines():
  line=line.strip()
  if not line.startswith('S15CHECK '):continue
  match=re.fullmatch(r'S15CHECK ([A-Z0-9_]+) revenue=([0-9]+(?:\.[0-9]+)?) orders=([0-9]+) aov=([0-9]+(?:\.[0-9]+)?)',line)
  if not match:raise ValueError('Malformed S15CHECK appendix line')
  context,revenue,orders,aov=match.groups()
  if context not in CONTEXTS or context in rows:raise ValueError('Unknown or duplicate S15CHECK context')
  rows[context]=dict(revenue=float(revenue),orders=int(orders),aov=float(aov))
 if set(rows)!=set(CONTEXTS):raise ValueError('Appendix must contain each of the five required contexts once')
 details=[]
 for key,want in expected.items():
  got=rows[key];passed=all(math.isfinite(v) for v in got.values()) and got['orders']==want['orders'] and abs(got['revenue']-want['revenue'])<=1 and abs(got['aov']-want['aov'])<=1
  details.append(dict(context=key,awarded=4 if passed else 0,maximum=4,feedback='Matches the issued context.' if passed else 'Check delivered population, year/region filters and the AOV denominator.'))
 return dict(status='COMPONENT_ONLY',assessment='S15',score=sum(r['awarded'] for r in details),maximum=20,assessment_maximum=100,checks=details,limitation='Checks reported values only. Relationships, live slicers, design and interpretation remain separate release requirements.')

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--file',required=True);p.add_argument('--out',required=True);a=p.parse_args()
 source=Path(a.file)
 if source.suffix.lower() not in ('.docx','.pdf','.pptx') or not source.is_file() or source.stat().st_size>20*1024*1024:raise ValueError('Use an accessible DOCX/PDF/PPTX evidence document up to 20 MiB')
 from artifact_grade import extract
 expected=load_reference()
 try:result=assess_text(extract(source),expected)
 except (ValueError,OSError,RuntimeError,TimeoutError) as exc:result=dict(status='EXCEPTION',score=None,maximum=20,error=str(exc))
 result['source_sha256']=hashlib.sha256(source.read_bytes()).hexdigest()
 out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=2)+'\n');print(result['status'],result.get('score'))
if __name__=='__main__':main()
