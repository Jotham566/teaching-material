"""Combine independent-track marks by learner ID; never mix in IUEA marks.

Missing or unresolved assessments remain blank and prevent a final percentage.
No letter bands are inferred. Inputs must be authoritative 100-point results.
"""
import argparse,csv,json,math,re
from pathlib import Path
WEIGHTS={'S05':15,'S09':15,'S13':30,'S15':40}

def combine(roster,results):
    students={}
    for row in roster:
        sid=row['student_id'].strip().upper()
        if not re.fullmatch(r'S[0-9]{4,8}',sid) or sid in students:raise ValueError('Missing or duplicate learner ID')
        if row.get('cohort')!='DA':raise ValueError('Independent-track roster must use cohort DA')
        students[sid]=dict(student_id=sid,name=row.get('name',''),**{s:'' for s in WEIGHTS})
    for session,rows in results.items():
        if session not in WEIGHTS:raise ValueError('Unknown independent-track session '+session)
        seen=set()
        for row in rows:
            sid=row['student_id'].strip().upper()
            if sid not in students or sid in seen:raise ValueError('Unknown or duplicate result ID '+sid)
            seen.add(sid)
            if row.get('status') not in ('AUTO_SCORED','OK','ERRORS') or row.get('score','')=='':continue
            value=float(row['score']);maximum=float(row['maximum'])
            if maximum!=100 or not math.isfinite(value) or not 0<=value<=100:raise ValueError('Invalid final component '+sid)
            students[sid][session]=value
    for row in students.values():
        missing=[s for s in WEIGHTS if row[s]=='']
        row['missing']='; '.join(missing)
        row['final_percent']='' if missing else round(sum(row[s]*weight/100 for s,weight in WEIGHTS.items()),2)
    return list(students.values())

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--roster',required=True);p.add_argument('--out',required=True)
    for session in WEIGHTS:p.add_argument('--'+session.lower())
    a=p.parse_args()
    with open(a.roster) as f:roster=list(csv.DictReader(f))
    results={}
    for session in WEIGHTS:
        file=getattr(a,session.lower())
        if file:
            with open(file) as f:results[session]=list(csv.DictReader(f))
    rows=combine(roster,results);out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    with (out/'DA_gradebook.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=['student_id','name',*WEIGHTS,'final_percent','missing']);w.writeheader()
        for row in rows:
            safe=dict(row)
            if safe['name'].startswith(('=','+','-','@','\t','\r')):safe['name']="'"+safe['name']
            w.writerow(safe)
    (out/'weights.json').write_text(json.dumps(WEIGHTS,indent=2)+'\n')
    print(len(rows),'learners;',sum(r['final_percent']!='' for r in rows),'complete final percentages')
if __name__=='__main__':main()
