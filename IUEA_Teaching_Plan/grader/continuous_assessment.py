"""Build a private, repeatable CA ledger from source receipts and graded results.
Never execute uploaded code here. The existing isolated grader supplies marks.
"""
import argparse,collections,csv,hashlib,json,math,re
from datetime import datetime,timezone
from pathlib import Path

COHORTS=('CML3111','CML3112','CML3113')
QUIZ_WEEKS=(1,2,3,4,5,6,8,9,10,11)    # Weeks 12 and 13 (Q11, Q12) are retired and never sat
RETIRED_QUIZ_WEEKS=(12,13)
ASSIGNMENT_WEEKS=(1,2,3,4,5,6,8,9,10,11,12)

# Block arrangement of 2 November 2026 (unchanged on 3 November; data/assessment_blocks_20261103.json is the source of truth and a test keeps this in step).
# Receipts are named by teaching week here: Q8 is the Week 8 quiz (called Q7 in the gradebook columns) and W08 is A7.
# Weeks 1 to 6 stay weekly and the best WEEKLY_BEST of the assigned weeks count. Week 6 is waived for every cohort.
# A block adds the marks of its parts, is never dropped, and a part that was not submitted scores zero.
# Block 1 = Classes 1 and 2: quizzes of Weeks 8 and 9 (Q7, Q8; 10 marks), assignments A7 and A8 (40 marks).
# Block 2 = Classes 3 and 4: quizzes of Weeks 10 and 11 (Q9, Q10; 10 marks), assignments A9, A10, A11 (60 marks).
# Quizzes are out of 3 x 5 + 10 + 10 = 35 and assignments out of 3 x 20 + 40 + 60 = 160 when Week 6 is waived.
WEEKLY_WEEKS=(1,2,3,4,5,6)
WAIVED_WEEKS=(6,)
WEEKLY_BEST=4  # of the six weekly items; one fewer for each waived week
QUIZ_MAX=5
ASSIGNMENT_MAX=20
# Decision of 3 November 2026 (data/assessment_blocks_20261103.json is the source of truth; a test keeps this in step): no demo, no Practical Test 2.
# The Engineering ML project is an individual, timed, fully auto-graded Colab sitting (Week 12) like Practical Test 1: Part A coded notebook /30 + Part B decision memo form /15.
COURSE_WEIGHTS=dict(quizzes=15,assignments=15,data_analysis_project=10,practical_test_1=15,engineering_ml_project=45)  # sums to 100
PROJECT_PARTS=(('A',30),('B',15))  # (part, maximum); the project counts only when BOTH parts are marked
PROJECT_MAX=sum(m for _,m in PROJECT_PARTS)
PROVISIONAL_KEYS=('quizzes','assignments','data_analysis_project','practical_test_1')  # marked before the project
PROVISIONAL_OUT_OF=sum(COURSE_WEIGHTS[k] for k in PROVISIONAL_KEYS)  # 55
COURSEWORK_WEIGHT=COURSE_WEIGHTS['quizzes']  # percent of the course, for quizzes and for assignments alike (both 15)
BLOCKS=dict(
 quizzes=(('Block 1',('Q8','Q9')),('Block 2',('Q10','Q11'))),
 assignments=(('Block 1',('W08','W09')),('Block 2',('W10','W11','W12'))))

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

def _best_weekly(marks,ids,best):
 """Sum of the best `best` marks among the weekly ids; an item not submitted scores zero."""
 return sum(sorted((marks.get(i,0) for i in ids),reverse=True)[:best])

def coursework_totals(current,waived_weeks=WAIVED_WEEKS,extra_students=()):
 """Quiz and assignment totals under the block arrangement, one row per (cohort, student).

 `current` is the list that build() returns under 'current'. Only GRADED receipts add marks.
 Returns marks earned, marks available and the weighted percentage of the course for each component.
 """
 marks=collections.defaultdict(dict)
 for r in current:
  if r['status']=='GRADED' and r['score'] is not None and r['student_id']:
   marks[(r['cohort'],r['student_id'])][r['assessment']]=r['score']
 for k in extra_students:marks[tuple(k)]
 weeks=[w for w in WEEKLY_WEEKS if w not in waived_weeks];best=WEEKLY_BEST-(len(WEEKLY_WEEKS)-len(weeks))
 spec=dict(quizzes=('Q%d',QUIZ_MAX),assignments=('W%02d',ASSIGNMENT_MAX))
 out=[]
 for (cohort,sid),m in sorted(marks.items()):
  row=dict(cohort=cohort,student_id=sid)
  for part,(fmt,top) in spec.items():
   earned=_best_weekly(m,[fmt%w for w in weeks],best);available=best*top;detail=[]
   for label,ids in BLOCKS[part]:
    got=sum(m.get(i,0) for i in ids);earned+=got;available+=len(ids)*top
    detail.append(dict(block=label,earned=got,available=len(ids)*top,parts_submitted=sum(i in m for i in ids)))
   row[part]=dict(earned=earned,available=available,weighted=round2(earned/available*COURSEWORK_WEIGHT),blocks=detail)
  out.append(row)
 return out

def _weighted(mark,top,weight):
 """A mark out of `top` as points of the course; a missing mark scores zero. Rounded like gradebook.gs."""
 return 0 if mark is None else round2(mark/top*weight)

def semester_totals(current,students=(),waived_weeks=WAIVED_WEEKS):
 """Semester 1 totals, one row per (cohort, student), with the same rules as gradebook.gs.

 Provisional mode: until BOTH project parts are marked, `final` is None, `project_status` is 'Project: PENDING' and the row carries
 `provisional` = 'Semester 1 provisional: x of 55 marks, y percent' over the four components marked before the project (quizzes,
 assignments, data analysis project, Practical Test 1). An unmarked project is never counted as zero. Once both parts are marked the
 row carries the full total out of 100. A missing quiz or assignment part, data analysis project or Test 1 still scores zero.
 `current` is build()['current'];
 `students` adds (cohort, student_id) pairs that have no receipts at all (they score zero)."""
 marks=collections.defaultdict(dict);parts=collections.defaultdict(dict)
 for r in current:
  if not r['student_id']:continue
  k=(r['cohort'],r['student_id'])
  if r['status']=='GRADED' and r['score'] is not None and r['assessment'] in ('DA_PROJECT','TEST1'):marks[k][r['assessment']]=r['score']
  if r['assessment']=='ML_PROJECT' and r['status'] in ('GRADED','PART_MARKED') and r.get('part_scores'):
   for p,_ in PROJECT_PARTS:
    if r['part_scores'].get(p) is not None:parts[k][p]=r['part_scores'][p]
 keys=sorted({(r['cohort'],r['student_id']) for r in current if r['student_id']}|set(marks)|set(parts)|{(c,s) for c,s in students})
 base={(r['cohort'],r['student_id']):r for r in coursework_totals(current,waived_weeks,keys)}
 out=[]
 for k in keys:
  cohort,sid=k;cw=base[k]
  q,a=cw['quizzes'],cw['assignments']
  da=marks[k].get('DA_PROJECT');t1=marks[k].get('TEST1')
  daw=_weighted(da,100,COURSE_WEIGHTS['data_analysis_project']);t1w=_weighted(t1,100,COURSE_WEIGHTS['practical_test_1'])
  pa,pb=parts[k].get('A'),parts[k].get('B');marked=pa is not None and pb is not None
  prw=round2((pa+pb)/PROJECT_MAX*COURSE_WEIGHTS['engineering_ml_project']) if marked else 0
  pm=round2(q['weighted']+a['weighted']+daw+t1w);pp=round2(pm/PROVISIONAL_OUT_OF*100)
  missing=[]
  if da is None:missing.append('Data Analysis Project')
  if t1 is None:missing.append('Practical Test 1')
  for part,label in (('quizzes','quiz'),('assignments','assignment')):
   for b in (cw[part]['blocks'] or []):
    if b['parts_submitted']==0:missing.append(f"{b['block']} {label}")
  out.append(dict(cohort=cohort,student_id=sid,quizzes=q,assignments=a,
   data_analysis_project=dict(mark=da,weighted=daw),practical_test_1=dict(mark=t1,weighted=t1w),
   project=dict(part_a=pa,part_b=pb,marked=marked,pending=not marked,weighted=prw),
   provisional=dict(marks=pm,out_of=PROVISIONAL_OUT_OF,percent=pp,text=f"Semester 1 provisional: {pm:.2f} of {PROVISIONAL_OUT_OF} marks, {pp:.2f} percent"),
   final=round2(pm+prw) if marked else None,
   project_status='Project: marked' if marked else 'Project: PENDING',missing=missing))
 return out

TOTALS_COLUMNS=('cohort','student_id','quizzes_earned','quizzes_out_of','quizzes_weighted','assignments_earned','assignments_out_of','assignments_weighted',
 'data_analysis_project_weighted','practical_test_1_weighted','provisional_marks','provisional_out_of','provisional_percent','project_part_a','project_part_b',
 'project_status','final_percent','missing')
def write_totals_csv(rows,path):
 """Private working file for the lecturer. While the project is pending final_percent is blank, never zero."""
 with open(path,'w',newline='',encoding='utf-8') as f:
  w=csv.writer(f);w.writerow(TOTALS_COLUMNS)
  for r in rows:
   w.writerow([r['cohort'],r['student_id'],r['quizzes']['earned'],r['quizzes']['available'],r['quizzes']['weighted'],r['assignments']['earned'],r['assignments']['available'],r['assignments']['weighted'],
    r['data_analysis_project']['weighted'],r['practical_test_1']['weighted'],r['provisional']['marks'],r['provisional']['out_of'],r['provisional']['percent'],
    '' if r['project']['part_a'] is None else r['project']['part_a'],'' if r['project']['part_b'] is None else r['project']['part_b'],
    r['project_status'],'' if r['final'] is None else r['final'],'; '.join(r['missing'])])

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--source');ap.add_argument('--results');ap.add_argument('--timing');ap.add_argument('--out');ap.add_argument('--test-ledger',action='append',default=[])
 ap.add_argument('--totals-out',help='also write a CSV of Semester 1 totals: provisional out of 55 until the project is marked, then the full total')
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
# SEMESTER_TOTALS_20261103: patched 3 November 2026
