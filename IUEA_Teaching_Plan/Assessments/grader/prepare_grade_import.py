"""Separate completed marks from exceptions without editing CSVs by hand."""
import argparse,csv,math
from pathlib import Path

def partition(rows):
    ready=[];exceptions=[];seen=set()
    for row in rows:
        sid=row['student_id']
        if not sid or sid in seen:raise ValueError('Duplicate or missing student registration number')
        seen.add(sid)
        raw=row.get('score',row.get('notebook_total',''))
        maximum=row.get('maximum',row.get('max_total',''))
        status=row['status']
        if status not in ('OK','ERRORS','AUTO_SCORED') or raw=='':
            exceptions.append(dict(student_id=sid,status=status,reason='Resolve the original feedback before importing a mark.'));continue
        value=float(raw);maximum=float(maximum)
        if maximum not in (20,100) or not math.isfinite(value) or not 0<=value<=maximum:
            raise ValueError('Invalid final mark or incomplete component for '+sid)
        ready.append(dict(student_id=sid,status=status,score=value,maximum=maximum))
    return ready,exceptions

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('results');ap.add_argument('--out',required=True);args=ap.parse_args()
    ready,exceptions=partition(list(csv.DictReader(open(args.results))))
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    for name,rows,fields in [('import_ready.csv',ready,['student_id','status','score','maximum']),('exceptions.csv',exceptions,['student_id','status','reason'])]:
        with (out/name).open('w') as f:
            writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(rows)
    print(len(ready),'marks ready;',len(exceptions),'exceptions remain ungraded. Original results retained.')

if __name__=='__main__':main()
