"""Build a private, repeatable CA ledger from source receipts and graded results.
Never execute uploaded code here. The existing isolated grader supplies marks.
"""
import argparse,collections,csv,hashlib,json,math,re
from datetime import datetime,timezone
from pathlib import Path

COHORTS=('CML3111','CML3112','CML3113')

# Semester 1 grading policy of 10 November 2026. data/assessment_policy_20261110.json is the source of truth and policy_check() / a unit test keep these constants in step with it.
# Final mark /100 = assignments 20 + quizzes 20 + Practical Test 1 20 + Engineering ML project 40.
# Assignments A1 to A5 (ledger ids W01 to W05, each /20) and quizzes Q1 to Q5 (each /5) all count equally; each is worth 4. Nothing else counts:
# Q6 and later, the block quizzes, A6 onward, the block assignments, the Data Analysis project, Practical Test 2 and the demo add nothing (their receipts are still kept in the ledger).
# There is no best-N rule and no waived week. A missing or not-yet-GRADED counted item scores 0 (and is reported in `unresolved` when a receipt exists).
QUIZ_IDS=('Q1','Q2','Q3','Q4','Q5')
ASSIGNMENT_IDS=('W01','W02','W03','W04','W05')   # A1 to A5 in the ledger
TEST_ID='TEST1'
QUIZ_MAX=5
ASSIGNMENT_MAX=20
TEST_MAX=100
COUNTED_IDS=ASSIGNMENT_IDS+QUIZ_IDS+(TEST_ID,)
COURSE_WEIGHTS=dict(assignments=20,quizzes=20,practical_test_1=20,engineering_ml_project=40)  # sums to 100
# The Engineering ML project is an individual, timed, fully auto-graded Colab sitting (Week 12): Part A coded notebook /30 + Part B decision memo form /15.
PROJECT_PARTS=(('A',30),('B',15))  # (part, maximum); the project counts only when BOTH parts are marked
PROJECT_MAX=sum(m for _,m in PROJECT_PARTS)
PROVISIONAL_KEYS=('assignments','quizzes','practical_test_1')  # marked before the project
PROVISIONAL_OUT_OF=sum(COURSE_WEIGHTS[k] for k in PROVISIONAL_KEYS)  # 60
POLICY_FILE=Path(__file__).resolve().parents[2]/'data'/'assessment_policy_20261110.json'

def policy_check(path=None):
 """Compare this module's constants with the policy JSON; return a list of mismatch descriptions (empty = in step)."""
 pol=json.loads(Path(path or POLICY_FILE).read_text());c=pol['counted'];bad=[]
 def eq(name,mine,theirs):
  if mine!=theirs:bad.append(f'{name}: module {mine!r} != policy {theirs!r}')
 eq('weights',COURSE_WEIGHTS,pol['weights']);eq('course_total',sum(COURSE_WEIGHTS.values()),pol['course_total'])
 eq('assignment ledger ids',ASSIGNMENT_IDS,tuple(c['assignments']['ledger_ids']));eq('assignment max',ASSIGNMENT_MAX,c['assignments']['each_max'])
 eq('quiz ids',QUIZ_IDS,tuple(c['quizzes']['ledger_ids']));eq('quiz max',QUIZ_MAX,c['quizzes']['each_max'])
 eq('test id',TEST_ID,c['practical_test_1']['ledger_id']);eq('test max',TEST_MAX,c['practical_test_1']['max'])
 eq('project parts',PROJECT_PARTS,tuple(c['engineering_ml_project']['parts'].items()));eq('project raw max',PROJECT_MAX,c['engineering_ml_project']['raw_max'])
 eq('project scaled max',COURSE_WEIGHTS['engineering_ml_project'],c['engineering_ml_project']['scaled_max'])
 eq('provisional out of',PROVISIONAL_OUT_OF,pol['provisional']['out_of']);eq('provisional components',PROVISIONAL_KEYS,tuple(pol['provisional']['components']))
 return bad

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

def identity_conflicts(attempts, supported_accounts=()):
 by_reg=collections.defaultdict(set);by_email=collections.defaultdict(set);assessments=collections.defaultdict(set)
 for r in attempts:
  if r['student_id'] and r['email']:
   by_reg[(r['cohort'],r['student_id'])].add(r['email']);by_email[(r['cohort'],r['email'])].add(r['student_id'])
   assessments[(r['cohort'],r['email'],r['student_id'])].add(r['assessment'])
 consistent={(c,s) for (c,s),emails in by_reg.items() if len(emails)>1 and
   all(by_email[(c,e)]=={s} and len(assessments[(c,e,s)])>=2 for e in emails)}
 bad={k for k,v in by_reg.items() if len(v)>1 and k not in consistent and k not in set(supported_accounts)}
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
   append(dict(cohort=cohort,assessment=assessment,student_id=sid,submitted_student_id=field(f,['registration','student id','student_id']),email=email,full_name=field(f,['full name','student name']),response_id=row['response_id'],submitted_at=row['submitted_at'],timing_status=timing_status,status='AWAITING_GRADING',score=None,maximum=(PROJECT_MAX if assessment=='ML_PROJECT' else 20),file_ids=row['file_ids'],source=p.name))
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
   if g.get('part_scores') is not None:
    # Engineering ML project: Part A (/30) and Part B (/15). Both marked -> GRADED and the total is A+B; one marked -> PART_MARKED.
    if r['assessment']!='ML_PROJECT':raise ValueError('Part scores belong to the ML project only')
    parts=g['part_scores']
    if not isinstance(parts,dict) or not parts or set(parts)-{p for p,_ in PROJECT_PARTS}:raise ValueError('Part scores must be a dict of A and/or B')
    for p,top in PROJECT_PARTS:
     v=parts.get(p)
     if v is not None and (isinstance(v,bool) or not isinstance(v,(int,float)) or not 0<=v<=top):raise ValueError('Project part mark out of range')
    full=all(parts.get(p) is not None for p,_ in PROJECT_PARTS)
    if g['status']=='GRADED' and not full:raise ValueError('A completed project needs both parts')
    if g['status']=='PART_MARKED' and full:raise ValueError('Both parts marked: status must be GRADED')
    if g['status'] not in ('GRADED','PART_MARKED'):raise ValueError('Part scores need status GRADED or PART_MARKED')
    if full:
     total=sum(parts[p] for p,_ in PROJECT_PARTS)
     if value is not None and abs(value-total)>1e-9:raise ValueError('Project total must equal Part A + Part B')
     value=total;g=dict(g,score=total)
    elif value is not None:raise ValueError('Total must be blank until both project parts are marked')
    r['part_scores']={p:parts.get(p) for p,_ in PROJECT_PARTS}
   elif g['status']=='PART_MARKED':raise ValueError('PART_MARKED needs part_scores')
   if g['status']=='GRADED' and value is None:raise ValueError('Completed mark must be numeric')
   if value is not None and (isinstance(value,bool) or not isinstance(value,(int,float)) or not 0<=value<=r['maximum']):raise ValueError('Mark out of range')
   if g['status'] not in ('GRADED','PART_MARKED') and value is not None:raise ValueError('Unresolved mark must be blank')
   if value is not None or g.get('code_score') is not None:
    manifest=json.loads((source/r['source']).read_text())
    hashes={f['id']:f['sha256'] for f in manifest['files'] if f['id'] in r['file_ids']}
    if not hashes or set(hashes)!=set(r['file_ids']) or g.get('source_hashes')!=hashes:
     raise ValueError('Grade attachment hashes do not match this source snapshot; regrade')
   r.update(score=value,status=g['status'],code_score=g.get('code_score'),code_maximum=g.get('code_maximum'))
   if g.get('grading_note'):r['grading_note']=g['grading_note']
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
 return finalize(attempts,sources)

# The lecturer's own test submissions must never appear in the compiled marks.
LECTURER_EMAILS={'jothammartin.wambi@gmail.com','wirmbeesubs@gmail.com'}
LECTURER_NAME_PARTS={'JOTHAM','MARTIN','WAMBI'}
def is_lecturer_test(r):
 sid=norm(r.get('submitted_student_id') or r.get('student_id'));cur=norm(r.get('student_id'))
 if re.match(r'^TEST\d*$',sid) or re.match(r'^TEST\d*$',cur):return True
 if (r.get('email') or '').strip().lower() in LECTURER_EMAILS:return True
 words=set(re.findall(r'[A-Z]+',(r.get('full_name') or '').upper()))
 return len(words&LECTURER_NAME_PARTS)>=2

def finalize(attempts,sources,extra_conflicts=(),supported_accounts=(),registration_authoritative=False):
 """Rebuild current attempts and students after supported identity corrections."""
 attempts[:]=[r for r in attempts if not is_lecturer_test(r)]
 bad=(set() if registration_authoritative else identity_conflicts(attempts,supported_accounts))|set(extra_conflicts)
 for r in attempts:
  r['source_score']=r['score']
  r['source_status']=r['status']
  if not r['student_id'] or (not registration_authoritative and not r['email']):r.update(score=None,status='IDENTITY_MISSING')
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

def round2(x):
 """Round to two places, halves upward, exactly as Math.round(x*100)/100 does in gradebook.gs (Python's round() goes to even)."""
 return math.floor(x*100+0.5)/100

def _receipts(current):
 """{(cohort, student): {assessment: current receipt}} for every receipt that has a student id."""
 out=collections.defaultdict(dict)
 for r in current:
  if r['student_id']:out[(r['cohort'],r['student_id'])][r['assessment']]=r
 return out

def _component(rec,ids,top,weight):
 """One equal-weight component. Only GRADED receipts add marks; a missing or unresolved item scores zero.
 `unresolved` = ids whose current receipt exists but is not GRADED; `missing` = ids with no receipt at all."""
 got=0;unresolved=[];missing=[]
 for i in ids:
  r=rec.get(i)
  if r is None:missing.append(i)
  elif r['status']=='GRADED' and r['score'] is not None:got+=r['score']
  else:unresolved.append(i)
 available=len(ids)*top
 return dict(earned=got,available=available,weighted=round2(got/available*weight),missing=missing,unresolved=unresolved)

def coursework_totals(current,extra_students=()):
 """Assignment and quiz components (each out of 20), one row per (cohort, student).

 `current` is the list that build() returns under 'current'. Counted items are A1 to A5 (W01 to W05, each /20) and Q1 to Q5 (each /5),
 all equal; anything else is ignored. `extra_students` adds (cohort, student_id) pairs with no receipts (they score zero)."""
 rec=_receipts(current)
 for k in extra_students:rec[tuple(k)]
 return [dict(cohort=c,student_id=s,
   assignments=_component(m,ASSIGNMENT_IDS,ASSIGNMENT_MAX,COURSE_WEIGHTS['assignments']),
   quizzes=_component(m,QUIZ_IDS,QUIZ_MAX,COURSE_WEIGHTS['quizzes'])) for (c,s),m in sorted(rec.items())]

def semester_totals(current,students=()):
 """Semester 1 totals under the policy of 10 November 2026, one row per (cohort, student), with the same rules as gradebook.gs.

 Final = assignments /20 + quizzes /20 + Practical Test 1 /20 + Engineering ML project /40, each part rounded (halves up), the total the rounded sum.
 Provisional mode: until BOTH project parts are marked, `final` is None, `project_status` is 'Project: PENDING' and the row carries
 `provisional` = 'Semester 1 provisional: x of 60 marks, y percent' over assignments, quizzes and Practical Test 1. An unmarked project is
 never counted as zero. A counted item that is missing or not GRADED scores zero; `missing` lists counted items with no receipt and
 `unresolved` lists counted items (Q1 to Q5, W01 to W05, TEST1) whose current receipt exists but is not GRADED, so the lecturer can resolve them.
 `current` is build()['current']; `students` adds (cohort, student_id) pairs that have no receipts at all (they score zero)."""
 rec=_receipts(current);parts=collections.defaultdict(dict)
 for k,m in rec.items():
  r=m.get('ML_PROJECT')
  if r and r['status'] in ('GRADED','PART_MARKED') and r.get('part_scores'):
   for p,_ in PROJECT_PARTS:
    if r['part_scores'].get(p) is not None:parts[k][p]=r['part_scores'][p]
 keys=sorted(set(rec)|{tuple(k) for k in students})
 base={(r['cohort'],r['student_id']):r for r in coursework_totals(current,keys)}
 out=[]
 for k in keys:
  cohort,sid=k;cw=base[k];q,a=cw['quizzes'],cw['assignments'];m=rec.get(k,{})
  t=_component(m,(TEST_ID,),TEST_MAX,COURSE_WEIGHTS['practical_test_1']);rt=m.get(TEST_ID);t1=rt['score'] if rt and rt['status']=='GRADED' else None
  pa,pb=parts[k].get('A'),parts[k].get('B');marked=pa is not None and pb is not None
  prw=round2((pa+pb)/PROJECT_MAX*COURSE_WEIGHTS['engineering_ml_project']) if marked else 0
  pm=round2(a['weighted']+q['weighted']+t['weighted']);pp=round2(pm/PROVISIONAL_OUT_OF*100)
  missing=[*a['missing'],*q['missing'],*t['missing']];unresolved=[*a['unresolved'],*q['unresolved'],*t['unresolved']]
  out.append(dict(cohort=cohort,student_id=sid,assignments=a,quizzes=q,
   practical_test_1=dict(mark=t1,weighted=t['weighted']),
   project=dict(part_a=pa,part_b=pb,marked=marked,pending=not marked,weighted=prw),
   provisional=dict(marks=pm,out_of=PROVISIONAL_OUT_OF,percent=pp,text=f"Semester 1 provisional: {pm:.2f} of {PROVISIONAL_OUT_OF} marks, {pp:.2f} percent"),
   final=round2(pm+prw) if marked else None,
   project_status='Project: marked' if marked else 'Project: PENDING',missing=missing,unresolved=unresolved))
 return out

TOTALS_COLUMNS=('cohort','student_id','assignments_earned','assignments_out_of','assignments_weighted','quizzes_earned','quizzes_out_of','quizzes_weighted',
 'practical_test_1_weighted','provisional_marks','provisional_out_of','provisional_percent','project_part_a','project_part_b',
 'project_status','final_percent','missing','unresolved')
def write_totals_csv(rows,path):
 """Private working file for the lecturer. While the project is pending final_percent is blank, never zero. `unresolved` names counted items that have a receipt but are not GRADED."""
 with open(path,'w',newline='',encoding='utf-8') as f:
  w=csv.writer(f);w.writerow(TOTALS_COLUMNS)
  for r in rows:
   w.writerow([r['cohort'],r['student_id'],r['assignments']['earned'],r['assignments']['available'],r['assignments']['weighted'],r['quizzes']['earned'],r['quizzes']['available'],r['quizzes']['weighted'],
    r['practical_test_1']['weighted'],r['provisional']['marks'],r['provisional']['out_of'],r['provisional']['percent'],
    '' if r['project']['part_a'] is None else r['project']['part_a'],'' if r['project']['part_b'] is None else r['project']['part_b'],
    r['project_status'],'' if r['final'] is None else r['final'],'; '.join(r['missing']),'; '.join(r['unresolved'])])

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--source');ap.add_argument('--results');ap.add_argument('--timing');ap.add_argument('--out');ap.add_argument('--test-ledger',action='append',default=[])
 ap.add_argument('--totals-out',help='also write a CSV of Semester 1 totals: provisional out of 60 until the project is marked, then the full total')
 ap.add_argument('--from-ledger',help='skip the rebuild: read an existing ledger.json and write only the --totals-out CSV');a=ap.parse_args()
 if a.from_ledger:
  if not a.totals_out:ap.error('--from-ledger needs --totals-out')
  data=json.loads(Path(a.from_ledger).read_text())
 else:
  if not a.source or not a.out:ap.error('--source and --out are required unless --from-ledger is used')
  data=build(a.source,a.results,json.loads(Path(a.timing).read_text()) if a.timing else None,a.test_ledger)
  p=Path(a.out);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data,indent=2)+'\n')
 if a.totals_out:
  t=Path(a.totals_out);t.parent.mkdir(parents=True,exist_ok=True)
  write_totals_csv(semester_totals(data['current'],[(s['cohort'],s['student_id']) for s in data['students']]),t)
 print(json.dumps(dict(students=len(data['students']),attempts=len(data['attempts']),current=len(data['current']),statuses=dict(collections.Counter(r['status'] for r in data['current'])))))
if __name__=='__main__':main()
