"""Build a private, repeatable CA ledger from source receipts and graded results.
Never execute uploaded code here. The existing isolated grader supplies marks.
"""
import argparse,collections,csv,hashlib,json,re
from datetime import datetime,timezone
from pathlib import Path

COHORTS=('CML3111','CML3112','CML3113')
QUIZ_WEEKS=(1,2,3,4,5,6,8,9,10,11,12,13)
ASSIGNMENT_WEEKS=(1,2,3,4,5,6,8,9,10,11,12)

def norm(v):
 """Compare formatting only: retain every letter, digit, slash and hyphen."""
 return re.sub(r'\s+','',str(v or '').upper()).replace('_','/')
def field(fields,terms):
 for term in terms:
  for title,value in fields.items():
   if term in title.lower() and str(value or '').strip():return str(value).strip()
 return ''
def stamp(s):return datetime.fromisoformat(str(s).replace('Z','+00:00'))
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def quiz_mark(quiz,response):
 """Use recorded item scores; never overwrite historical scores with a new key."""
 answers={str(a['id']):a for a in response['answers']};total=0
 questions=[q for q in quiz['items'] if q['points']>0]
 if sum(q['points'] for q in questions)!=5:return None,'QUIZ_MAXIMUM_MISMATCH'
 for q in questions:
  a=answers.get(str(q['id']))
  if a is None:return None,'QUIZ_ITEM_MISSING'
  score=a.get('score')
  if score is None:return None,'QUIZ_SCORE_PENDING'
  if isinstance(score,bool) or not isinstance(score,(float,int)) or not 0<=score<=q['points']:return None,'QUIZ_SCORE_INVALID'
  total+=score
 return total,'GRADED'

def choose_current(attempts):
 grouped=collections.defaultdict(list)
 for a in attempts:grouped[(a['cohort'],a['student_id'],a['assessment'])].append(a)
 chosen=[]
 for key,rows in grouped.items():
  eligible=[r for r in rows if r['timing_status']=='ON_TIME']
  pool=eligible or rows
  ordered=sorted(pool,key=lambda r:(stamp(r['submitted_at']),r['response_id']))
  row=dict(ordered[-1]);row['attempt_count']=len(rows)
  if len(ordered)>1 and stamp(ordered[-1]['submitted_at'])==stamp(ordered[-2]['submitted_at']) and ordered[-1]['response_id']!=ordered[-2]['response_id']:
   row.update(score=None,status='EQUAL_TIME_CONFLICT')
  if row['timing_status']!='ON_TIME':row.update(score=None,status='TIMING_REVIEW')
  chosen.append(row)
 return chosen

def identity_conflicts(attempts):
 by_reg=collections.defaultdict(set);by_email=collections.defaultdict(set);assessments=collections.defaultdict(set)
 for r in attempts:
  if r['student_id'] and r['email']:
   by_reg[(r['cohort'],r['student_id'])].add(r['email']);by_email[(r['cohort'],r['email'])].add(r['student_id'])
   assessments[(r['cohort'],r['email'],r['student_id'])].add(r['assessment'])
 consistent={(c,s) for (c,s),emails in by_reg.items() if len(emails)>1 and
   all(by_email[(c,e)]=={s} and len(assessments[(c,e,s)])>=2 for e in emails)}
 bad={k for k,v in by_reg.items() if len(v)>1 and k not in consistent}
 for r in attempts:
  if (r['cohort'],r['student_id']) in consistent:
   r['identity_evidence']=r.get('identity_evidence','')+' Same registration consistently used across at least two assessments by each account; no account uses another registration in this programme.'
 for (cohort,email),regs in by_email.items():
  if len(regs)>1:bad.update((cohort,r) for r in regs)
 return bad

def recover_quiz_ids(attempts):
 """Recover a blank legacy quiz ID only from a unique same-course account match."""
 accounts=collections.defaultdict(set)
 for r in attempts:
  if r['email'] and r['student_id']:accounts[(r['cohort'],r['email'])].add(r['student_id'])
 for r in attempts:
  known=accounts.get((r['cohort'],r['email']),set())
  if r['assessment'].startswith('Q') and not r['student_id'] and r['email'] and len(known)==1:
   r['student_id']=next(iter(known))
   r['identity_evidence']='Blank legacy quiz number recovered from the unique registration used by this Google-account email in the same programme.'

def resolve_supported_typos(attempts):
 """Use repeated same-account evidence; never merge by similar numbers alone."""
 groups=collections.defaultdict(list);owners=collections.defaultdict(set)
 compact=lambda s:re.sub(r'[^A-Z0-9]','',s)
 for r in attempts:
  if r['email'] and r['student_id']:
   groups[(r['cohort'],r['email'])].append(r)
   owners[(r['cohort'],compact(r['student_id']))].add(r['email'])
 for (cohort,email),rows in groups.items():
  counts=collections.Counter(r['student_id'] for r in rows)
  dominant=counts.most_common(1)[0][0]
  family=[r for r in rows if compact(r['student_id'])==compact(dominant)]
  if owners[(cohort,compact(dominant))]!={email}:continue
  for r in rows:
   sid=r['student_id'];same=compact(sid)==compact(dominant)
   one_digit=(len(compact(sid))==len(compact(dominant)) and
      sum(a!=b for a,b in zip(compact(sid),compact(dominant)))==1 and
      all(a==b or (a.isdigit() and b.isdigit()) for a,b in zip(compact(sid),compact(dominant))))
   later=[x for x in family if stamp(x['submitted_at'])>stamp(r['submitted_at'])]
   typo=(counts[sid]==1 and len(family)>=3 and len(family)/len(rows)>=0.75 and
         len(later)>=3 and one_digit and owners[(cohort,compact(sid))]=={email})
   if sid!=dominant and (same or typo):
    r['identity_evidence']=('Same programme and Google account; '+
      ('punctuation-only variation' if same else 'single early digit typo followed by at least three consistent receipts')+
      '; original registration preserved. No competing account uses the target number.')
    r['student_id']=dominant

def build(source,results=None,timing=None,test_ledgers=None,resolve_identities=True,retained_attempts=None):
 source=Path(source);attempts=[];seen={};sources=[]
 timing=timing or {}
 def append(r):
  rid=r['response_id'];h=hashlib.sha256(json.dumps(r,sort_keys=True).encode()).hexdigest()
  if rid in seen:
   if seen[rid]!=h:raise ValueError('Conflicting copies of a receipt; choose one source snapshot')
   return
  seen[rid]=h;attempts.append(r)
 for p in sorted(source.glob('*_manifest.json')):
  data=json.loads(p.read_text());cohort,assessment=data['key'].split('|')
  if cohort not in COHORTS:continue
  sources.append(dict(file=p.name,sha256=digest(p),exported_at=data['exported_at']))
  for row in data['records']:
   f=row['fields'];sid=norm(field(f,['registration','student id','student_id']));email=row['email'].strip().lower()
   start=stamp(data['window']['open']);end=stamp(data['window']['close']);at=stamp(row['submitted_at'])
   timing_status=row.get('timing_status') or ('ON_TIME' if start<=at<=end else ('EARLY' if at<start else 'LATE'))
   override=timing.get(row['response_id'])
   if override:
    if not override.get('evidence'):raise ValueError('Timing correction requires evidence')
    timing_status=override['status']
   append(dict(cohort=cohort,assessment=assessment,student_id=sid,submitted_student_id=field(f,['registration','student id','student_id']),email=email,full_name=field(f,['full name','student name']),response_id=row['response_id'],submitted_at=row['submitted_at'],timing_status=timing_status,status='AWAITING_GRADING',score=None,maximum=20,file_ids=row['file_ids'],source=p.name))
 for qp in sorted(list(source.glob('*_quiz.json'))+([source/'quizzes.json'] if (source/'quizzes.json').exists() else [])):
  data=json.loads(qp.read_text());sources.append(dict(file=qp.name,sha256=digest(qp),exported_at=data['exported_at']))
  for q in data['quizzes']:
   cohort,week=q['key'].split('|')
   for row in q['records']:
    f={a['title']:a['answer'] for a in row['answers']};score,status=quiz_mark(q,row)
    # A form receipt is not sufficient evidence of timeliness after reopening.
    ts=timing.get(row['response_id'],{})
    if ts and not ts.get('evidence'):raise ValueError('Timing correction requires evidence')
    timing_status=ts.get('status','UNVERIFIED')
    entered_id=field(f,['registration','student id','student_id','student number'])
    append(dict(cohort=cohort,assessment='Q'+week,student_id=norm(entered_id),submitted_student_id=entered_id,email=(row['email'] or '').strip().lower(),full_name=field(f,['full name','student name']),response_id=row['response_id'],submitted_at=row['submitted_at'],timing_status=timing_status,status=status,score=score,maximum=5,file_ids=[],source=qp.name))
 if results:
  graded=json.loads(Path(results).read_text())
  index={r['response_id']:r for r in attempts}
  for g in graded:
   if g['response_id'] not in index:raise ValueError('Mark has no source receipt')
   r=index[g['response_id']]
   if any(g[k]!=r[k] for k in ('cohort','assessment','student_id')):raise ValueError('Mark identity mismatch')
   value=g.get('score')
   if g['status']=='GRADED' and value is None:raise ValueError('Completed mark must be numeric')
   if value is not None and (isinstance(value,bool) or not isinstance(value,(int,float)) or not 0<=value<=r['maximum']):raise ValueError('Mark out of range')
   if g['status']!='GRADED' and value is not None:raise ValueError('Unresolved mark must be blank')
   if value is not None or g.get('code_score') is not None:
    manifest=json.loads((source/r['source']).read_text())
    hashes={f['id']:f['sha256'] for f in manifest['files'] if f['id'] in r['file_ids']}
    if not hashes or set(hashes)!=set(r['file_ids']) or g.get('source_hashes')!=hashes:
     raise ValueError('Grade attachment hashes do not match this source snapshot; regrade')
   r.update(score=value,status=g['status'],code_score=g.get('code_score'),code_maximum=g.get('code_maximum'))
 for test_file in test_ledgers or []:
  test_path=Path(test_file);td=json.loads(test_path.read_text())
  sources.append(dict(file=test_path.name,sha256=digest(test_path),exported_at='Test grading ledger'))
  for t in td['attempts']:
   if t.get('status')=='REHEARSAL':continue
   if t['cohort'] not in COHORTS or t['assessment'] not in ('TEST1','TEST2'):raise ValueError('Unexpected test source')
   if t.get('maximum')!=100:raise ValueError('Test maximum must be 100')
   score=t.get('score') if t['status']=='GRADED' else None
   if t['status']=='GRADED' and (isinstance(score,bool) or not isinstance(score,(int,float)) or not 0<=score<=100):raise ValueError('Invalid completed test score')
   append(dict(cohort=t['cohort'],assessment=t['assessment'],student_id=norm(t['student_registration_number']),submitted_student_id=t['student_registration_number'],email=t['email'].strip().lower(),full_name=t['full_name'],response_id=t['response_id'],submitted_at=t['submitted_at'],timing_status=t['status'] if t['status'] in ('LATE','OUTSIDE_WINDOW') else 'ON_TIME',status=t['status'],score=score,maximum=100,file_ids=[],source=test_path.name))
 # Retain assessments outside this importer (tests/projects/later coursework).
 for original in retained_attempts or []:
  r=dict(original)
  if r['cohort'] not in COHORTS:raise ValueError('Unexpected retained cohort')
  r['student_id']=norm(r.get('submitted_student_id',r['student_id']))
  r['score']=r.get('source_score',r.get('score'))
  r['status']=r.get('source_status',r['status'])
  for k in ('source_score','source_status','identity_evidence','attempt_count'):r.pop(k,None)
  if r['status']=='GRADED' and (isinstance(r['score'],bool) or not isinstance(r['score'],(int,float)) or not 0<=r['score']<=r['maximum']):raise ValueError('Invalid retained mark')
  append(r)
 if resolve_identities:
  resolve_supported_typos(attempts)
  recover_quiz_ids(attempts)
 bad=identity_conflicts(attempts)
 for r in attempts:
  r['source_score']=r['score']
  r['source_status']=r['status']
  if not r['student_id'] or not r['email']:r.update(score=None,status='IDENTITY_MISSING')
  elif (r['cohort'],r['student_id']) in bad:r.update(score=None,status='IDENTITY_CONFLICT')
 current=choose_current(attempts);students={}
 for r in attempts:
  k=(r['cohort'],r['student_id'])
  if not r['student_id']:continue
  s=students.setdefault(k,dict(cohort=r['cohort'],student_id=r['student_id'],full_name='',emails=set()))
  s['emails'].add(r['email'])
  if r['full_name']:s['full_name']=r['full_name']
 for s in students.values():s['email']='; '.join(sorted(s.pop('emails')))
 return dict(updated_at=datetime.now(timezone.utc).isoformat(),students=sorted(students.values(),key=lambda s:(s['cohort'],s['student_id'])),current=current,attempts=attempts,sources=sources)

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--source',required=True);ap.add_argument('--results');ap.add_argument('--timing');ap.add_argument('--out',required=True);ap.add_argument('--test-ledger',action='append',default=[]);a=ap.parse_args()
 data=build(a.source,a.results,json.loads(Path(a.timing).read_text()) if a.timing else None,a.test_ledger)
 p=Path(a.out);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data,indent=2)+'\n')
 print(json.dumps(dict(students=len(data['students']),attempts=len(data['attempts']),current=len(data['current']),statuses=dict(collections.Counter(r['status'] for r in data['current'])))))
if __name__=='__main__':main()
