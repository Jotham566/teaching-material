"""Merge the regrade proposal CSVs (A1 and A2 written) into one consistent table and summarise what 'higher of the original and the regrade' would change.

The CSVs hold student data and live OUTSIDE the repositories (the lecturer's Desktop folder IUEA_Regrade). This file contains no data.

  python3 IUEA_Teaching_Plan/grader/regrade_merge.py --dir ~/Desktop/IUEA_Regrade [--out ~/Desktop/IUEA_Regrade/Regrade_proposals_merged.csv]

Rule applied (lecturer, 10 November 2026): a student's regraded mark is the HIGHER of the original and the lenient regrade; a regrade of 'cannot judge' (blank) leaves the original mark; a receipt with no original mark takes the regrade.
"""
import argparse,collections,csv,glob
from pathlib import Path

def num(x):
 try:return float(x)
 except (TypeError,ValueError):return None

def read(path):
 """Rows normalised by position, because each part-file used slightly different column names."""
 with open(path,encoding='utf-8',newline='') as f:
  rows=list(csv.reader(f))
 head=[h.strip().lower() for h in rows[0]];out=[]
 flag_i=next((i for i,h in enumerate(head) if h=='flags'),None)
 just_i=next((i for i,h in enumerate(head) if h=='justification'),None)
 assess=Path(path).name.split('_')[0]  # A1 or A2w
 for r in rows[1:]:
  if len(r)<7 or not r[1]:continue
  d=dict(cohort=r[0],reg=r[1],name=r[2],response_id=r[3],assessment=r[4],original=num(r[5]),proposed=num(r[6]),
   flags=r[flag_i] if flag_i is not None and flag_i<len(r) else '',justification=r[just_i] if just_i is not None and just_i<len(r) else '',source=Path(path).name)
  if assess=='A2w':
   oi=next((i for i,h in enumerate(head) if 'original' in h and 'total' in h),None);pi=next((i for i,h in enumerate(head) if 'proposed' in h and 'total' in h),None)
   d['original_total']=num(r[oi]) if oi is not None and oi<len(r) else None;d['proposed_total']=num(r[pi]) if pi is not None and pi<len(r) else None
  out.append(d)
 return out

def apply_rule(d):
 """The final regraded mark under 'higher of original and regrade'."""
 o,p=d['original'],d['proposed']
 if p is None:return o
 if o is None:return p
 return max(o,p)

def summarise(rows,label):
 up=down=same=blank=noorig=0;gain=0.0;students=0
 for d in rows:
  o,p=d['original'],d['proposed']
  if p is None:blank+=1;continue
  if o is None:noorig+=1;gain+=p;continue
  if p>o:up+=1;gain+=p-o;students+=1
  elif p<o:down+=1
  else:same+=1
 print(f'{label}: {len(rows)} receipts | raised {up} | regrade lower, original kept {down} | same {same} | cannot judge {blank} | no original mark {noorig} | marks added {gain:.1f} (mean per receipt {gain/max(len(rows),1):.2f})')
 return gain

def write_overrides(a1,a2,path):
 """CSV for final_marks_export.py --overrides. A1: the higher mark. A2: coding marks stay; only the written part may rise, so mark = original total + (higher written - original written)."""
 n=0
 with open(path,'w',encoding='utf-8',newline='') as f:
  w=csv.writer(f);w.writerow(['cohort','reg_number','assessment','mark','original','source'])
  for d in a1:
   if d['proposed'] is not None and (d['original'] is None or d['proposed']>d['original']):
    w.writerow([d['cohort'],d['reg'],'W01',d['proposed'],d['original'],d['source']]);n+=1
  for d in a2:
   o,p=d['original'],d['proposed'];ot=d.get('original_total')
   if p is None:continue
   if o is None:
    if d.get('proposed_total') is not None:w.writerow([d['cohort'],d['reg'],'W02',d['proposed_total'],ot,d['source']]);n+=1
   elif p>o and ot is not None:
    w.writerow([d['cohort'],d['reg'],'W02',round(ot+(p-o),2),ot,d['source']]);n+=1
 print('wrote',n,'override rows to',path)

def main(argv=None):
 ap=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
 ap.add_argument('--dir',required=True);ap.add_argument('--out');ap.add_argument('--write-overrides',help='write the approved-marks CSV (higher of original and regrade) to this path')
 a=ap.parse_args(argv);folder=Path(a.dir).expanduser()
 a1=[d for f in sorted(glob.glob(str(folder/'A1_regrade_*.csv'))) for d in read(f)]
 a2=[d for f in sorted(glob.glob(str(folder/'A2w_regrade_*.csv'))) for d in read(f)]
 for d in a1+a2:d['final']=apply_rule(d)
 summarise(a1,'A1 (of 20)');summarise(a2,'A2 written (of 6)')
 flags=collections.Counter()
 for d in a1+a2:
  for fl in (x.strip() for x in d['flags'].replace(';',',').split(',')):
   if fl and fl!='NONE':flags[(d['assessment'],fl)]+=1
 print('flags:',dict(sorted(flags.items())))
 out=Path(a.out).expanduser() if a.out else folder/'Regrade_proposals_merged.csv'
 with open(out,'w',encoding='utf-8',newline='') as f:
  w=csv.writer(f);w.writerow(['cohort','reg_number','name','response_id','assessment','original','proposed_lenient','final_higher_of','flags','justification','source_file'])
  for d in sorted(a1+a2,key=lambda d:(d['assessment'],d['cohort'],d['reg'])):
   w.writerow([d['cohort'],d['reg'],d['name'],d['response_id'],d['assessment'],d['original'],d['proposed'],d['final'],d['flags'],d['justification'],d['source']])
 print('wrote',out)
 if a.write_overrides:write_overrides(a1,a2,a.write_overrides)
 return a1,a2

if __name__=='__main__':
 main()
