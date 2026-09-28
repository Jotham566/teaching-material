"""Select latest on-time files using the server timestamp and roster.
Input: exported 'Submission audit' CSV and a downloaded upload folder.
File names must start with the Drive file ID from the audit (rename during
export). Ambiguous files/IDs stop the batch; original downloads are retained.
"""
import argparse,csv,json,re,shutil
from pathlib import Path
from datetime import datetime
from registration import valid, filename_id


def select(rows,roster,key):
    selected={}
    for row in rows:
        if row['assessment_key']!=key:continue
        if row['status']!='ON_TIME':continue
        sid=row['student_id'].strip().upper()
        if sid not in roster:raise ValueError('Unknown roster ID '+sid)
        if roster[sid].get('cohort')!=key.split('|')[0]:raise ValueError('Missing or mismatched roster cohort '+sid)
        expected=roster[sid].get('email','').strip().lower()
        if not expected:raise ValueError('Missing roster email '+sid)
        if row['email'].strip().lower()!=expected:raise ValueError('Email mismatch '+sid)
        stamp=datetime.fromisoformat(row['submitted_at'].replace('Z','+00:00'))
        deadline=datetime.fromisoformat(row['deadline'].replace('Z','+00:00'))
        if stamp.tzinfo is None or deadline.tzinfo is None:raise ValueError('Timezone missing')
        if row['status']!='ON_TIME' or stamp>deadline:continue
        files=json.loads(row['file_ids'])
        if not files:raise ValueError('No upload for '+sid)
        prev=selected.get(sid)
        if prev and stamp==prev[0] and row['response_id']!=prev[1]['response_id']:raise ValueError('Equal-time conflicting submissions '+sid)
        if prev is None or stamp>prev[0]:selected[sid]=(stamp,row)
    return {sid:r for sid,(_,r) in selected.items()}


def cohort_roster(roster,key):
    records=json.loads((Path(__file__).resolve().parents[2]/'data/assessments.json').read_text())
    if key not in {r['key'] for r in records}:raise ValueError('Unknown assessment key')
    cohorts={r['cohort'] for r in records}
    if any(r.get('cohort') not in cohorts for r in roster.values()):raise ValueError('Every roster row requires a valid cohort')
    return {sid:r for sid,r in roster.items() if r['cohort']==key.split('|')[0]}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    for flag in ('audit','roster','assessment','downloads','out'):ap.add_argument('--'+flag,required=True)
    args=ap.parse_args()
    with open(args.roster) as source:roster_rows=list(csv.DictReader(source))
    roster={}
    for r in roster_rows:
        sid=r['student_id'].strip().upper()
        if sid in roster:raise ValueError('Duplicate roster ID '+sid)
        if not valid(sid, allow_legacy=r.get('cohort')=='DA'):raise ValueError('Invalid Student Registration Number '+sid)
        roster[sid]=r
    eligible=cohort_roster(roster,args.assessment)
    with open(args.audit) as source:selected=select(list(csv.DictReader(source)),roster,args.assessment)
    downloads=Path(args.downloads);out=Path(args.out);plan=[]
    for sid,r in selected.items():
        for file_id in json.loads(r['file_ids']):
            if not re.fullmatch(r'[A-Za-z0-9_-]+',file_id):raise ValueError('Invalid Drive file ID')
            files=[p for p in downloads.iterdir() if p.is_file() and p.name.startswith(file_id+'.')]
            if len(files)!=1:raise ValueError('Expected one downloaded file named '+file_id+'.extension')
            plan.append((sid,files[0],r))
    notebooks={}
    for sid,file,r in plan:
        if file.suffix=='.ipynb':
            if sid in notebooks:raise ValueError('More than one notebook in chosen submission '+sid)
            notebooks[sid]=file
    out.mkdir(parents=True,exist_ok=True)
    if any(out.iterdir()):raise ValueError('Output directory must be empty to prevent stale submissions')
    manifest=[]
    for sid,file,r in plan:
        target=out/(filename_id(sid)+'_'+args.assessment.split('|')[-1]+file.suffix) if file.suffix=='.ipynb' else out/(filename_id(sid)+'_'+file.name)
        shutil.copy2(file,target)
        manifest.append(dict(student_id=sid,file=str(target.resolve()),response_id=r['response_id'],submitted_at=r['submitted_at'],team_id=r.get('team_id','')))
    with (out/'manifest.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=['student_id','file','response_id','submitted_at','team_id']);w.writeheader();w.writerows(manifest)
    missing=sorted(set(eligible)-set(selected))
    with (out/'missing.csv').open('w') as source:
        writer=csv.DictWriter(source,fieldnames=['student_id','assessment','status']);writer.writeheader()
        writer.writerows(dict(student_id=sid,assessment=args.assessment,status='NO_ON_TIME_SUBMISSION') for sid in missing)
    print('Prepared',len(selected),'students;',len(missing),'without an on-time submission in this cohort; no marks assigned to missing submissions')
if __name__=='__main__':main()
