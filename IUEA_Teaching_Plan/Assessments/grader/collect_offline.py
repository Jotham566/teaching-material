"""Timestamp an invigilator-controlled offline collection and prepare grading files.

Run on the lecturer's computer as files are collected, not on student machines.
The invigilator controls the clock and intake folder. No timestamps supplied
inside student files are trusted. Later transport does not change this receipt.
"""
import argparse,csv,hashlib,json,shutil
from datetime import datetime,timezone
from pathlib import Path
from batch_grade import student_id_from_name
from registration import valid,filename_id

def collect(intake,roster,assessment,cohort,deadline,out,now=None):
    now=now or datetime.now(timezone.utc);end=datetime.fromisoformat(deadline.replace('Z','+00:00'))
    if end.tzinfo is None or now.tzinfo is None:raise ValueError('Timezone required')
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    if any(out.iterdir()):raise ValueError('Use a new collection directory; receipts are never overwritten')
    mapping={}
    for row in roster:
        sid=row['student_id'].strip().upper()
        if not valid(sid) or sid in mapping:raise ValueError('Invalid or duplicate roster registration number')
        if row.get('cohort')!=cohort:continue
        mapping[sid]=row
    plan=[];seen=set()
    for file in sorted(p for p in Path(intake).rglob('*') if p.is_file() and p.suffix.lower()=='.ipynb'):
        sid=student_id_from_name(str(file))
        if sid not in mapping:
            suffix='_'+assessment
            stem=file.stem.upper()
            prefix=stem[:-len(suffix)] if stem.endswith(suffix) else ''
            matches=[key for key in mapping if key.replace('/','_')==prefix]
            if len(matches)==1:sid=matches[0]
        if sid not in mapping or sid in seen:raise ValueError('Unknown or duplicate collected registration number '+sid)
        seen.add(sid);plan.append((sid,file))
    if not plan:raise ValueError('No named notebooks found')
    receipts=[];manifest=[]
    for sid,file in plan:
        target=out/(filename_id(sid)+'_'+assessment+'.ipynb');shutil.copy2(file,target);digest=hashlib.sha256(target.read_bytes()).hexdigest()
        response='offline:'+digest
        receipts.append(dict(student_id=sid,assessment_key=cohort+'|'+assessment,collected_at=now.isoformat(),deadline=end.isoformat(),status='ON_TIME' if now<=end else 'LATE',sha256=digest,file=target.name))
        if now<=end:manifest.append(dict(student_id=sid,file=str(target.resolve()),response_id=response,submitted_at=now.isoformat(),team_id=''))
    (out/'collection_receipts.json').write_text(json.dumps(receipts,indent=2))
    with (out/'manifest.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=['student_id','file','response_id','submitted_at','team_id']);w.writeheader();w.writerows(manifest)
    return receipts

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('intake','roster','assessment','cohort','deadline','out'):p.add_argument('--'+name,required=True)
    a=p.parse_args()
    if a.assessment not in ('TEST1','TEST2'):raise ValueError('Use the normal submission audit for online assignments')
    with open(a.roster) as f:roster=list(csv.DictReader(f))
    receipts=collect(a.intake,roster,a.assessment,a.cohort,a.deadline,a.out)
    print(len(receipts),'receipts;',sum(r['status']=='ON_TIME' for r in receipts),'on time; originals retained')
if __name__=='__main__':main()
