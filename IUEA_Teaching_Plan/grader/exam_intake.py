"""Trusted test intake and durable marks ledger. Student code only runs in Docker.

The input job must come from the lecturer-controlled form bridge, not a student.
No pre-existing class roster is required. Attendance means a received submission;
absence cannot be inferred until an enrolled roster is supplied.
"""
import argparse,csv,hashlib,json,sqlite3,tempfile,shutil
from datetime import datetime
from pathlib import Path
from batch_grade import grade_one
from registration import normalize,valid,filename_id
from colab_exam_contracts import VERSION,PARTS
from engineering_contracts import DOMAINS
HERE=Path(__file__).resolve().parent
FIELDS=['response_id','cohort','assessment','variant','full_name','email','student_registration_number','submitted_at','status','score','maximum','semester_points','notebook_sha256','grader_version','feedback']

def instant(value):
    date=datetime.fromisoformat(value.replace('Z','+00:00'))
    if date.tzinfo is None:raise ValueError('Timestamp needs a timezone')
    return date

def connect(path):
    db=sqlite3.connect(path)
    db.execute('CREATE TABLE IF NOT EXISTS attempts (response_id TEXT PRIMARY KEY, payload TEXT NOT NULL)')
    return db

def records(db):return [json.loads(r[0]) for r in db.execute('SELECT payload FROM attempts')]

def process(job,notebook,db):
    rid=job['response_id']
    prior=db.execute('SELECT payload FROM attempts WHERE response_id=?',(rid,)).fetchone()
    digest=hashlib.sha256(Path(notebook).read_bytes()).hexdigest()
    if prior:
        old=json.loads(prior[0])
        if old['notebook_sha256']!=digest:raise ValueError('Response ID reused with different file content')
        for field in ('cohort','assessment','variant','submitted_at'):
            if old[field]!=job[field]:raise ValueError('Response ID reused with different receipt metadata')
        if old['email']!=job['email'].strip().lower() or old['student_registration_number']!=normalize(job['student_registration_number']):
            raise ValueError('Response ID reused with different identity')
        return old
    cohort,exam=job['cohort'],job['assessment']
    if cohort not in DOMAINS or exam not in PARTS or job['variant'] not in 'ABC' or len(job['variant'])!=1:raise ValueError('Unknown assigned test, cohort or variant')
    sid=normalize(job['student_registration_number']);email=job['email'].strip().lower();name=job['full_name'].strip()
    if not valid(sid) or not name or '@' not in email:raise ValueError('Name, email and Student Registration Number are required')
    if job.get('email_verified') is not True:raise ValueError('The Google Form must collect verified account email')
    if digest!=job['notebook_sha256']:raise ValueError('Downloaded notebook checksum mismatch')
    out={k:job.get(k,'') for k in FIELDS};out.update(student_registration_number=sid,email=email,full_name=name,status='PENDING',score=None,maximum=100,semester_points=None,notebook_sha256=digest,grader_version=VERSION,feedback='')
    when=instant(job['submitted_at'])
    if not instant(job['opens_at'])<=when<=instant(job['closes_at']):out.update(status='OUTSIDE_WINDOW',feedback='Submission is outside the authorised window. No final mark.')
    else:
        others=records(db)
        conflicts=[r for r in others if r['cohort']==cohort and ((r['student_registration_number']==sid and r['email']!=email) or (r['email']==email and r['student_registration_number']!=sid))]
        if conflicts:
            out.update(status='IDENTITY_CONFLICT',feedback='Registration number and verified email conflict with an earlier submission. Resolve before releasing marks.')
            for r in conflicts:
                r.update(status='IDENTITY_CONFLICT',score=None,semester_points=None,feedback=out['feedback'])
                db.execute('UPDATE attempts SET payload=? WHERE response_id=?',(json.dumps(r),r['response_id']))
        else:
            folder=HERE.parent/'assessment_banks'/exam/cohort/job['variant']
            with tempfile.TemporaryDirectory() as tmp:
                path=Path(tmp)/('submission_'+exam+'.ipynb');shutil.copyfile(notebook,path)
                result=grade_one(str(path),str(HERE/'specs'/f'spec_{exam}.py'),str(HERE/'specs/hidden'/f'spec_{exam}_hidden.py'),exam,cohort,str(folder),20,180,None)
            out['feedback']=json.dumps(dict(questions=result['questions'],cell_errors=result['cell_errors']),ensure_ascii=False)
            if result['status'] not in ('OK','ERRORS'):out['status']=result['status']
            elif normalize(result.get('declared_sid',''))!=sid:out['status']='IDENTITY_MISMATCH'
            elif any(q.get('err') for q in result['questions'].values()):out['status']='GRADER_EXCEPTION'
            else:
                out['status']='GRADED';out['score']=sum(q['awarded'] for q in result['questions'].values());out['semester_points']=out['score']*(.15 if exam=='TEST1' else .20)
    db.execute('INSERT INTO attempts VALUES (?,?)',(rid,json.dumps(out)));db.commit();return out

def current(rows):
    latest={}
    for r in rows:
        if r['status'] not in ('GRADED','IDENTITY_CONFLICT','IDENTITY_MISMATCH','GRADER_EXCEPTION','HARNESS_ERROR','TIMEOUT'):continue
        key=(r['cohort'],r['assessment'],r['student_registration_number'])
        if key not in latest or (instant(r['submitted_at']),r['response_id'])>(instant(latest[key]['submitted_at']),latest[key]['response_id']):latest[key]=r
    return sorted(latest.values(),key=lambda r:(r['cohort'],r['student_registration_number'],r['assessment']))

def export(db,folder):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    rows=records(db)
    for name,items in [('all_attempts',rows),('current_marks',current(rows))]:
        with (folder/(name+'.csv')).open('w',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=FIELDS,extrasaction='ignore');writer.writeheader()
            # Protect spreadsheet consumers against formula injection in identity text.
            for row in items:writer.writerow({k:("'"+v if isinstance(v,str) and v.startswith(('=','+','-','@')) else v) for k,v in row.items()})
    (folder/'workbook_data.json').write_text(json.dumps(dict(attempts=rows,current=current(rows)),indent=2)+'\n')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--job',required=True);p.add_argument('--notebook',required=True);p.add_argument('--ledger',required=True);p.add_argument('--out',required=True);a=p.parse_args()
    with connect(a.ledger) as db:
        r=process(json.loads(Path(a.job).read_text()),a.notebook,db);export(db,a.out);print(r['status'],r['score'])
