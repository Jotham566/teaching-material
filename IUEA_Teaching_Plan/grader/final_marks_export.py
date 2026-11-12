"""Simplified Semester 1 results workbook: one sheet per course (CML3111, CML3112, CML3113), one row per student.

Columns: Reg Number, Name, Email, Program, Assignment /20, Quiz /20, Test Practical /20, Project /40, Final Mark /100.
The rules are in data/assessment_policy_20261110.json (A1 to A5 and Q1 to Q5 count equally, Practical Test 1 is scaled to 20, the Engineering ML
project is scaled to 40). This file reads only the policy file and the private ledger; it never needs the Google Sheet.

The workbook holds student names and emails: write it OUTSIDE the teaching repository (the default is the Desktop).

  python3 IUEA_Teaching_Plan/grader/final_marks_export.py --ledger ~/Projects/IUEA-Grading-Private/snapshot/IUEA_Teaching_Plan/assessment_operations/private/ledger.json
Optional: --tests PATH/current_marks.csv (extra names), --out PATH.xlsx, --project-marks PATH.csv (student_id,part_a,part_b once the project is marked).
"""
import argparse,collections,csv,json,math,sys
from datetime import datetime
from pathlib import Path

HERE=Path(__file__).resolve().parent
POLICY_PATH=HERE.parent.parent/'data'/'assessment_policy_20261110.json'
COHORTS=('CML3111','CML3112','CML3113')
PLACEHOLDER_NAMES=('','no name extracted','name not captured','none','nan')

def load_policy(path=POLICY_PATH):
 return json.loads(Path(path).read_text(encoding='utf-8'))

def round2(x):
 """Halves upward, as Math.round(x*100)/100 in gradebook.gs and round2 in continuous_assessment.py."""
 return math.floor(x*100+0.5)/100

def rnd(x):
 """Whole marks, halves upward: the workbook shows no decimals."""
 return int(math.floor(x+0.5))

def real_name(n):
 n=' '.join(str(n or '').split())
 return n if n.lower() not in PLACEHOLDER_NAMES else ''

def resolve_names(ledger,tests=()):
 """First real name found per (cohort, student): the student record, then supported identity review rows, then receipts, then the test ledger."""
 pick={}
 def offer(k,n):
  n=real_name(n)
  if n and k not in pick:pick[k]=n
 for s in ledger['students']:offer((s['cohort'],s['student_id']),s.get('full_name') or s.get('name'))
 for r in ledger.get('identity_review',[]):
  if str(r.get('status','')).upper() in ('SUPPORTED','OK','VERIFIED'):offer((r['cohort'],r['student_id']),r.get('name'))
 for r in ledger['current']+ledger.get('attempts',[]):
  if r.get('student_id'):offer((r['cohort'],r['student_id']),r.get('full_name'))
 for r in tests:
  offer((r.get('cohort'),r.get('student_registration_number')),r.get('full_name'))
 return pick

def load_overrides(path):
 """Approved regrade marks: CSV with columns cohort, reg_number, assessment (W01..W05, Q1..Q5, TEST1), mark. They replace the ledger mark for that item."""
 out={}
 if not path:return out
 with open(path,encoding='utf-8',newline='') as f:
  for r in csv.DictReader(f):
   m=num(r.get('mark'))
   if m is not None:out[(r['cohort'],r['reg_number'],r['assessment'])]=m
 return out

def load_override_notes(path):
 """Optional 'student_note' column of the overrides CSV: a sentence shown to the student for that item."""
 out={}
 if not path:return out
 with open(path,encoding='utf-8',newline='') as f:
  for r in csv.DictReader(f):
   if (r.get('student_note') or '').strip():out[(r['cohort'],r['reg_number'],r['assessment'])]=r['student_note'].strip()
 return out

def num(x):
 try:return float(x)
 except (TypeError,ValueError):return None

def _fmt(x):
 return str(rnd(float(x)))

def test_questions(tests,test_detail=None):
 """{(cohort,reg): {'q1':(awarded,max),...}} from the test feedback, with the Test 1 regrade per-question changes applied when given."""
 out={}
 for r in tests:
  try:qs=json.loads(r.get('feedback') or '{}').get('questions',{})
  except ValueError:continue
  out[(r.get('cohort'),r.get('student_registration_number'))]={q:(float(v.get('awarded',0)),float(v.get('marks',0))) for q,v in qs.items()}
 import re
 for (c,reg),chg in (test_detail or {}).items():
  d=out.get((c,reg))
  if not d:continue
  for q,new in re.findall(r'(q\d+):\s*[\d.]+->([\d.]+)',chg):
   if q in d:d[q]=(max(d[q][0],float(new)),d[q][1])
 return out

def coding_questions(folder,detail=None):
 """{(response_id): {'q1':(awarded,max,hint)}} from the notebook grader's per-question results (GRADED records only, newest last), with the A2-A5 re-run changes applied. detail: {(cohort,reg,assessment id): 'q4 0->4; ...'}."""
 import re
 out={}
 for f in sorted(Path(folder).glob('*.json'),key=lambda p:p.stat().st_mtime) if folder else []:
  try:g=json.loads(f.read_text(encoding='utf-8'))
  except ValueError:continue
  if not isinstance(g,dict) or not isinstance(g.get('record'),dict):continue
  qs=g['record'].get('questions')
  if not qs:continue
  out[g.get('response_id')]=dict(cohort=g.get('cohort'),reg=g.get('student_id'),a=g.get('assessment'),q={q:[float(v.get('awarded',0)),float(v.get('marks',0)),str(v.get('msg',''))] for q,v in qs.items()})
 for v in out.values():
  chg=(detail or {}).get((v['cohort'],v['reg'],v['a']))
  for q,new in re.findall(r'(q\d+)\s*[\d.]*\s*->\s*([\d.]+)',chg or ''):
   if q in v['q']:v['q'][q][0]=max(v['q'][q][0],float(new))
 return out

def quiz_misses(folder):
 """{response_id: [missed question numbers]} for each quiz. The answer key is inferred as the only key that reproduces every student's recorded Forms total (skipped when no unique key exists)."""
 import itertools
 out={}
 for f in sorted(Path(folder).glob('*_quiz.json')) if folder else []:
  try:qs=json.loads(f.read_text(encoding='utf-8')).get('quizzes') or []
  except ValueError:continue
  for qz in qs:
   rows=[]
   for r in qz.get('records',[]):
    ans={};tot=None
    for a in r.get('answers',[]):
     t=str(a.get('title',''))
     if t.startswith('Recorded'):tot=a.get('score')
     elif t.split('.')[0].isdigit():ans[int(t.split('.')[0])]=a.get('answer')
    if tot is not None and ans:rows.append((r['response_id'],ans,tot))
   if not rows:continue
   nums=sorted(rows[0][1]);opts=[sorted({str(r[1].get(n)) for r in rows}) for n in nums]
   for_all=1
   for o in opts:for_all*=len(o)
   if for_all>200000:continue
   keys=[k for k in itertools.product(*opts) if all(sum(str(a.get(n))==x for n,x in zip(nums,k))==t for _,a,t in rows)]
   if len(keys)!=1:continue
   for rid,a,t in rows:out[rid]=[n for n,x in zip(nums,keys[0]) if str(a.get(n))!=x]
 return out

def build_status(k,recs,m,orig,counted,a_ids,q_ids,t_id,tq,project_done,cq=None,qm=None,totals=None,notes=None,test_issue=False):
 """Why each mark, short and plain, in the lecturer's voice so it can be shared with the student as it stands."""
 an=lambda i:'Assignment '+i[1:].lstrip('0');qn=lambda i:'Quiz '+i[1:]
 lines=[]
 if totals:lines.append('Assignments %s/20, quizzes %s/20, practical test %s/20.'%totals)
 for i in a_ids+q_ids:
  r=recs.get(i);isq=i in q_ids;name=qn(i) if isq else an(i);mx=float(r['maximum']) if r and r.get('maximum') else (5.0 if isq else 20.0)
  note=((r or {}).get('grading_note') or '').lower()
  if i not in m:
   lines.append(f'{name}: not received, 0/{_fmt(mx)}.' if r is None else f'{name}: received, not marked yet.')
   continue
  sc=m[i]
  if notes and i in notes:
   lines.append(f'{name}: {_fmt(sc)}/{_fmt(mx)}. '+notes[i]);continue
  if sc>=mx:continue
  if sc==0 and not isq and ('no notebook' in note or 'none was submitted' in note):lines.append(f'{name}: no notebook or README in the upload, 0/{_fmt(mx)}. If this was a mistake, send me the right files.');continue
  if sc==0 and not isq and 'empty' in note:lines.append(f'{name}: the uploaded file was empty, 0/{_fmt(mx)}. If this was a mistake, send me the right file.');continue
  txt=f'{name}: {_fmt(sc)}/{_fmt(mx)}.'
  cd=(cq or {}).get(r.get('response_id')) if r else None
  if cd and not isq:
   bad=[(q,h) for q,(a,m_,h) in sorted(cd['q'].items()) if a<m_]
   clean=lambda h:(h.strip().rstrip('.').lower() if h and len(h.strip())<=55 and '. ' not in h.strip() and ';' not in h else '')
   if bad and len(bad)<=2 and any(clean(h) for q,h in bad):txt+=' Code: '+'; '.join(f"question {q[1:]}"+(f" ({clean(h)})" if clean(h) else ' lost marks') for q,h in bad)+'.'
   elif bad:
    nums=[q[1:] for q,h in bad];txt+=(' Code: question '+nums[0]+' lost marks.') if len(nums)==1 else ' Code: questions '+', '.join(nums[:-1])+' and '+nums[-1]+' lost marks.'
   cm,cs=(r.get('code_maximum'),r.get('code_score')) if r else (None,None)
   if cm and cs is not None and mx-cm>0 and i not in orig and sc-cs<mx-cm:txt+=f' Written part {_fmt(sc-cs)}/{_fmt(mx-cm)}.'
  elif r and not isq and r.get('code_maximum') is not None and r.get('code_score') is not None and i not in orig and mx-r['code_maximum']>0:
   txt+=f" Code {_fmt(r['code_score'])}/{_fmt(r['code_maximum'])}, written part {_fmt(sc-r['code_score'])}/{_fmt(mx-r['code_maximum'])}."
  if isq and r and qm and r.get('response_id') in qm and qm[r['response_id']] and len(qm[r['response_id']])==rnd(mx-sc):
   w=qm[r['response_id']];txt+=(' Question '+str(w[0])+' wrong.') if len(w)==1 else (' Questions '+', '.join(str(n) for n in w[:-1])+' and '+str(w[-1])+' wrong.')
  lines.append(txt)
 if t_id in m and notes and t_id in notes:
  lines.append(f'Practical Test 1: {_fmt(m[t_id])}/100. '+notes[t_id])
 elif t_id not in m and notes and t_id in notes:
  lines.append(notes[t_id])
 elif t_id not in m:
  lines.append('Practical Test 1: received, but the upload could not be matched to your registration number and email, so it is not marked yet.' if test_issue else 'Practical Test 1: not received, 0/100.' if recs.get(t_id) is None else 'Practical Test 1: received, not marked yet.')
 else:
  qd=tq.get(k) if tq else None
  low=[f"Q{q[1:]} ({_fmt(a)}/{_fmt(mx)})" for q,(a,mx) in sorted(qd.items()) if a<mx] if qd else []
  lines.append('Practical Test 1: 100/100.' if m[t_id]>=100 else f'Practical Test 1: {_fmt(m[t_id])}/100.'+(' Lost marks on '+', '.join(low)+'.' if low else ''))
 if not project_done:lines.append('Project: to be marked after the Week 12 sittings.')
 return '\n'.join(lines)

def home_cohorts(ledger):
 """{reg: home cohort} for every registration number. The ledger allocates marks by registration number across accounts, but a student who used another cohort's form (for example the shared A1 catch-up form) has a row in two cohorts. The home cohort is the most common cohort of that programme code (BSEE, BSCE, ...) among students who appear in only one cohort; if the programme is unknown, the cohort with most records."""
 import re
 by=collections.defaultdict(set)
 for st in ledger['students']:by[st['student_id']].add(st['cohort'])
 prog=lambda reg:(re.search(r'/([A-Z]+)-?[A-Z]?$',reg.upper()) or [None,reg])[1] if '/' in reg else reg
 votes=collections.defaultdict(collections.Counter)
 for reg,cs in by.items():
  if len(cs)==1:votes[prog(reg)][next(iter(cs))]+=1
 cnt=collections.defaultdict(collections.Counter)
 for r in ledger['current']:
  if r.get('student_id'):cnt[r['student_id']][r['cohort']]+=1
 home={}
 for reg,cs in by.items():
  if len(cs)==1:home[reg]=next(iter(cs));continue
  v=[(votes[prog(reg)][c],cnt[reg][c],c) for c in cs]
  home[reg]=max(v)[2]
 return home

def remap_ids(ledger,idmap):
 """Copy of the ledger with mistyped registration numbers replaced by the real one (idmap {alias: real}) in students, current records and attempts. Distinct emails are kept on the merged student."""
 L=dict(ledger)
 f=lambda x:idmap.get(x,x)
 L['current']=[dict(r,student_id=f(r.get('student_id'))) for r in ledger['current']]
 L['attempts']=[dict(r,student_id=f(r.get('student_id'))) for r in ledger.get('attempts',[])]
 L['identity_review']=[dict(r,student_id=f(r.get('student_id'))) for r in ledger.get('identity_review',[])]
 L['students']=[dict(st,student_id=f(st['student_id'])) for st in ledger['students']]
 return L

def merge_cohorts(ledger):
 """Copy of the ledger with every student and record moved to the student's home cohort and duplicate student rows merged (home row's name and email first)."""
 import copy
 home=home_cohorts(ledger);L=dict(ledger)
 L['current']=[dict(r,cohort=home.get(r.get('student_id'),r['cohort'])) for r in ledger['current']]
 L['attempts']=[dict(r,cohort=home.get(r.get('student_id'),r['cohort'])) for r in ledger.get('attempts',[])]
 seen={};
 for st in sorted(ledger['students'],key=lambda x:x['cohort']!=home.get(x['student_id'],x['cohort'])):
  reg=st['student_id'];h=home.get(reg,st['cohort'])
  if reg in seen:
   o=seen[reg]
   if not real_name(o.get('full_name')) and real_name(st.get('full_name')):o['full_name']=st['full_name']
   have=[e.strip() for e in str(o.get('email') or '').split(';') if e.strip()]
   for e in str(st.get('email') or '').split(';'):
    if e.strip() and e.strip().lower() not in [h.lower() for h in have]:have.append(e.strip())
   o['email']='; '.join(have)
   continue
  seen[reg]=dict(st,cohort=h)
 L['students']=list(seen.values());L['home']=home
 return L

def compute(ledger,policy,project_marks=None,tests=(),overrides=None,test_detail=None,coding_dir=None,coding_detail=None,quiz_dir=None,aliases=(),notes=None,test_issues=()):
 """One dict per student. Only GRADED receipts add marks; any other receipt for a counted item scores 0 and is listed in `unresolved`."""
 idmap=dict(aliases) if aliases else {}
 if idmap:ledger=remap_ids(ledger,idmap)
 home=home_cohorts(ledger);ledger=merge_cohorts(ledger)
 overrides={(home.get(idmap.get(orr,orr),oc),idmap.get(orr,orr),oa):v for (oc,orr,oa),v in (overrides or {}).items()}
 notes={(home.get(idmap.get(rg,rg),c),idmap.get(rg,rg),i):v for (c,rg,i),v in (notes or {}).items()}
 tests=[dict(r,student_registration_number=idmap.get(r.get('student_registration_number'),r.get('student_registration_number')),cohort=home.get(idmap.get(r.get('student_registration_number'),r.get('student_registration_number')),r.get('cohort'))) for r in tests]
 c=policy['counted']
 a_ids,a_max=c['assignments']['ledger_ids'],c['assignments']['each_max']
 q_ids,q_max=c['quizzes']['ledger_ids'],c['quizzes']['each_max']
 t_id,t_max=c['practical_test_1']['ledger_id'],c['practical_test_1']['max']
 w=policy['weights'];pr=c['engineering_ml_project'];pr_a,pr_b=pr['parts']['A'],pr['parts']['B']
 names=resolve_names(ledger,tests)
 marks=collections.defaultdict(dict);bad=collections.defaultdict(list)
 counted=set(a_ids)|set(q_ids)|{t_id}
 for r in ledger['current']:
  if not r.get('student_id') or r['assessment'] not in counted:continue
  k=(r['cohort'],r['student_id'])
  if r['status']=='GRADED' and r.get('score') is not None:marks[k][r['assessment']]=max(float(r['score']),marks[k].get(r['assessment'],0))
  else:bad[k].append((r['assessment'],r['status']))
 out=[];overrides=overrides or {};applied=0
 tq=test_questions(tests,test_detail)
 cq=coding_questions(coding_dir,coding_detail)
 qm=quiz_misses(quiz_dir)
 recs=collections.defaultdict(dict)
 for r in ledger['current']:
  if r.get('student_id') and r['assessment'] in counted and (r['assessment'] not in recs[(r['cohort'],r['student_id'])] or (r.get('score') or 0)>=(recs[(r['cohort'],r['student_id'])][r['assessment']].get('score') or 0)):recs[(r['cohort'],r['student_id'])][r['assessment']]=r
 skip=set()
 best=collections.defaultdict(dict)
 for r in ledger.get('attempts',[]):
  if r.get('student_id') and r['assessment'] in counted and r.get('status')=='GRADED' and r.get('score') is not None and r.get('timing_status') in ('ON_TIME','EARLY'):
   kk=(r['cohort'],r['student_id']);best[kk][r['assessment']]=max(float(r['score']),best[kk].get(r['assessment'],-1))
 for s in ledger['students']:
  if (s['cohort'],s['student_id']) in skip:continue
  k=(s['cohort'],s['student_id']);m=marks[k]
  orig={}
  for (oc,orr,oa),om in overrides.items():
   if (oc,orr)==k and oa in counted:
    if om!=m.get(oa):orig[oa]=m.get(oa)
    m[oa]=om;applied+=1
    bad[k]=[x for x in bad.get(k,[]) if x[0]!=oa]
  for a_,v_ in best[k].items():
   if (k[0],k[1],a_) not in notes and v_>m.get(a_,-1):
    m[a_]=v_;bad[k]=[x for x in bad.get(k,[]) if x[0]!=a_]
  assign=rnd(sum(m.get(i,0) for i in a_ids)/(len(a_ids)*a_max)*w['assignments'])
  quiz=rnd(sum(m.get(i,0) for i in q_ids)/(len(q_ids)*q_max)*w['quizzes'])
  test=rnd(m.get(t_id,0)/t_max*w['practical_test_1'])
  pm=(project_marks or {}).get(s['student_id']);proj=None
  if pm and pm.get('A') is not None and pm.get('B') is not None:proj=rnd((pm['A']+pm['B'])/pr['raw_max']*w['engineering_ml_project'])
  out.append(dict(cohort=s['cohort'],reg=s['student_id'],name=names.get(k,''),email=s.get('email',''),assignment=assign,quiz=quiz,test=test,project=proj,
   final=assign+quiz+test+(proj or 0),unresolved=sorted(bad.get(k,[])),
   submitted=sorted(i for i in m if i in counted),items=dict(m),
   status=build_status(k,recs[k],m,orig,counted,a_ids,q_ids,t_id,tq,proj is not None,cq,qm,(assign,quiz,test),{i:v for (c,rg,i),v in (notes or {}).items() if (c,rg)==k},k[1] in set(test_issues))))
 compute.applied=applied
 return out

def write_workbook(rows,policy,path,ledger_stamp,source_note):
 from openpyxl import Workbook
 from openpyxl.comments import Comment
 from openpyxl.styles import Alignment,Border,Font,PatternFill,Side
 from openpyxl.utils import get_column_letter
 wb=Workbook();wb.remove(wb.active)
 hdr=['Reg Number','Name','Email','Program','Assignment /20','Quiz /20','Test Practical /20','Project /40','Final Mark /100']
 widths=[18,34,46,11,15,11,18,12,16]
 thin=Side(style='thin',color='BFBFBF');box=Border(left=thin,right=thin,top=thin,bottom=thin)
 black=PatternFill('solid',fgColor='000000');pale=PatternFill('solid',fgColor='FFF7D6');warn=PatternFill('solid',fgColor='FBD9C0')
 by=collections.defaultdict(list)
 for r in rows:by[r['cohort']].append(r)
 for cohort in COHORTS:
  ws=wb.create_sheet(cohort);data=sorted(by.get(cohort,[]),key=lambda r:r['reg'])
  ws['A1']=f'{cohort} Semester 1 marks';ws['A1'].font=Font(bold=True,size=14)
  pending=all(r['project'] is None for r in data)
  ws['A2']=('Project marks are not entered yet (Week 12 sittings), so Final Mark is the total so far, out of 60. Type each Project mark (out of 40) and Final Mark updates.' if pending
   else 'Final Mark = Assignment + Quiz + Test Practical + Project.')
  ws['A2'].font=Font(italic=True,color='595959')
  for j,(h,wd) in enumerate(zip(hdr,widths),1):
   c=ws.cell(row=4,column=j,value=h);c.font=Font(bold=True,color='FFFFFF');c.fill=black;c.alignment=Alignment(horizontal='center',vertical='center',wrap_text=True);c.border=box
   ws.column_dimensions[get_column_letter(j)].width=wd
  ws.row_dimensions[4].height=32
  for i,r in enumerate(data,5):
   vals=[r['reg'],r['name'] or 'Name not captured',r['email'],cohort,r['assignment'],r['quiz'],r['test'],r['project'],None]
   for j,v in enumerate(vals,1):
    c=ws.cell(row=i,column=j,value=v);c.border=box
    if j>=5:c.alignment=Alignment(horizontal='center');c.number_format='0'
   ws.cell(row=i,column=9,value=f'=ROUND(SUM(E{i}:H{i}),0)').font=Font(bold=True)
   ws.cell(row=i,column=9).number_format='0';ws.cell(row=i,column=9).alignment=Alignment(horizontal='center');ws.cell(row=i,column=9).border=box
   ws.cell(row=i,column=8).fill=pale
   if not r['name']:ws.cell(row=i,column=2).fill=warn
   col={'W':5,'Q':6,'T':7}
   for aid,status in r['unresolved']:
    cell=ws.cell(row=i,column=col[aid[0]]);cell.fill=warn
    cell.comment=Comment(f'{aid} is {status}: not marked yet, counted as 0 for now.','grader')
  ws.freeze_panes='A5';ws.auto_filter.ref=f'A4:I{4+len(data)}'
  ws.sheet_view.showGridLines=False
  ws.page_setup.orientation='landscape';ws.page_setup.fitToWidth=1;ws.page_setup.fitToHeight=0;ws.sheet_properties.pageSetUpPr.fitToPage=True;ws.print_title_rows='4:4'
 ws=wb.create_sheet('Why these marks')
 ws['A1']='Why these marks';ws['A1'].font=Font(bold=True,size=14)
 ws['A2']='One row per student, written to be shared as it stands. Filter by cohort or search a registration number.';ws['A2'].font=Font(italic=True,color='595959')
 for j,(h,wd) in enumerate(zip(['Cohort','Reg Number','Name','Why these marks'],[11,18,30,120]),1):
  c=ws.cell(row=4,column=j,value=h);c.font=Font(bold=True,color='FFFFFF');c.fill=black;c.alignment=Alignment(horizontal='center',vertical='center');c.border=box
  ws.column_dimensions[get_column_letter(j)].width=wd
 for i,r in enumerate(sorted(rows,key=lambda r:(r['cohort'],r['reg'])),5):
  for j,v in enumerate([r['cohort'],r['reg'],r['name'] or 'Name not captured',r['status']],1):
   c=ws.cell(row=i,column=j,value=v);c.border=box;c.alignment=Alignment(wrap_text=True,vertical='top')
  ws.row_dimensions[i].height=max(30,15*(str(r['status']).count('\n')+1+len(str(r['status']))//120))
 ws.freeze_panes='A5';ws.auto_filter.ref=f'A4:D{4+len(rows)}';ws.sheet_view.showGridLines=False
 ws.page_setup.orientation='landscape';ws.page_setup.fitToWidth=1;ws.page_setup.fitToHeight=0;ws.sheet_properties.pageSetUpPr.fitToPage=True;ws.print_title_rows='4:4'
 rm=wb.create_sheet('Read me',0)
 rm.column_dimensions['A'].width=30;rm.column_dimensions['B'].width=95
 lines=[('IUEA Semester 1 final marks (simplified)',None),
  ('Marks as of',ledger_stamp),('Source',source_note),(None,None),
  ('How the final mark is worked out',None),
  ('Assignment /20','A1 to A5, each /20, all five count equally: sum of the five marks divided by 5, rounded to a whole number.'),
  ('Quiz /20','Q1 to Q5, each /5, all five count equally: sum of the five marks times 4 / 5, rounded to a whole number.'),
  ('Test Practical /20','Practical Test 1 (marked out of 100) divided by 5, rounded to a whole number.'),
  ('Project /40','Engineering ML project: Part A /30 + Part B /15 = 45, scaled to 40. Counts only when both parts are marked (Week 12 sittings).'),
  ('Final Mark /100','Assignment + Quiz + Test Practical + Project, all whole numbers (half a mark rounds up). Until the project is marked it is the total so far, out of 60.'),
  ('Why these marks','Separate sheet with the reasons for each student\'s marks (missing or empty work, items below full marks, test questions that lost marks, marks raised on re-marking).'),
  ('Missing work','A missing or not-yet-marked item scores 0. Cells shaded orange hold an item that was handed in but is not marked yet (hover for the reason); a shaded name means no name was found in any record.'),
  ('Not counted','Q6 onward, A6 onward (Week 8 to 11 blocks), the Data Analysis project, Practical Test 2 and the demonstration.'),
  (None,None)]
 for i,(a,b) in enumerate(lines,1):
  rm.cell(row=i,column=1,value=a);rm.cell(row=i,column=2,value=b)
 rm['A1'].font=Font(bold=True,size=14);rm['A5'].font=Font(bold=True,size=12)
 for i in range(2,14):rm.cell(row=i,column=1).font=Font(bold=True);rm.cell(row=i,column=2).alignment=Alignment(wrap_text=True,vertical='top')
 r0=len(lines)+1
 rm.cell(row=r0,column=1,value='Course summary').font=Font(bold=True,size=12)
 for k,cohort in enumerate(COHORTS):
  d=by.get(cohort,[])
  avg=rnd(sum(r['final'] for r in d)/len(d)) if d else 0
  rm.cell(row=r0+1+k,column=1,value=cohort).font=Font(bold=True)
  rm.cell(row=r0+1+k,column=2,value=f"{len(d)} students. Average {avg} (total so far, out of 60). {sum(1 for r in d if r['unresolved'])} with an item handed in but not marked. {sum(1 for r in d if not r['name'])} with no name found.")
 r1=r0+5
 rm.cell(row=r1,column=1,value='Handed in but not marked yet (counted as 0 for now)').font=Font(bold=True,size=12)
 for j,h in enumerate(['Reg Number','Student / item / status'],1):rm.cell(row=r1+1,column=j,value=h).font=Font(bold=True)
 n=0
 for r in sorted(rows,key=lambda r:(r['cohort'],r['reg'])):
  for aid,status in r['unresolved']:
   n+=1;rm.cell(row=r1+1+n,column=1,value=r['reg']);rm.cell(row=r1+1+n,column=2,value=f"{r['cohort']}  {r['name'] or 'Name not captured'}  {aid}  {status}")
 if not n:rm.cell(row=r1+2,column=1,value='None')
 rm.page_setup.orientation='landscape';rm.page_setup.fitToWidth=1;rm.page_setup.fitToHeight=0;rm.sheet_properties.pageSetUpPr.fitToPage=True
 wb.save(path);return n

def main(argv=None):
 ap=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
 ap.add_argument('--ledger',required=True);ap.add_argument('--tests');ap.add_argument('--project-marks');ap.add_argument('--overrides',help='approved regrade marks CSV (cohort, reg_number, assessment, mark)')
 ap.add_argument('--test-detail',help='Test1_rerun_proposals.csv: applies the per-question regrade changes to the Status column')
 ap.add_argument('--notebook-grades',help='folder of per-notebook grading JSON (assessment_operations/private/notebook_grades)');ap.add_argument('--coding-detail',help='A2-A5_rerun_proposals.csv: applies the coding re-run changes')
 ap.add_argument('--quiz-dir',help='folder of *_quiz.json exports (assessment_operations/private/reconciled)')
 ap.add_argument('--aliases',help='CSV cohort,alias_id,real_id: a mistyped or variant registration number and the real one; the two are merged into one student')
 ap.add_argument('--test-issues',help='collection_issues.json from the test grading output: students whose Test 1 upload could not be collected')
 ap.add_argument('--out',default=str(Path.home()/'Desktop'/'IUEA_Semester1_Final_Marks.xlsx'))
 a=ap.parse_args(argv)
 policy=load_policy();ledger=json.loads(Path(a.ledger).read_text(encoding='utf-8'))
 tests=list(csv.DictReader(open(a.tests,encoding='utf-8'))) if a.tests else []
 pm=None
 if a.project_marks:
  pm={}
  for r in csv.DictReader(open(a.project_marks,encoding='utf-8')):
   pm[r['student_id']]=dict(A=float(r['part_a']) if r.get('part_a') not in (None,'') else None,B=float(r['part_b']) if r.get('part_b') not in (None,'') else None)
 ov=load_overrides(a.overrides) if a.overrides else {}
 td={}
 if a.test_detail:
  for r in csv.DictReader(open(a.test_detail,encoding='utf-8')):
   if r.get('status','').startswith('PROPOSED'):td[(r['cohort'],r['reg_number'])]=r.get('per_question_changes','')
 cd={}
 if a.coding_detail:
  am={'A2':'W02','A3':'W03','A4':'W04','A5':'W05'}
  for r in csv.DictReader(open(a.coding_detail,encoding='utf-8')):cd[(r['cohort'],r['reg_number'],am.get(r['assessment'],r['assessment']))]=r.get('per_question','')
 al=[(r['alias_id'],r['real_id']) for r in csv.DictReader(open(a.aliases,encoding='utf-8'))] if a.aliases else []
 ti=json.load(open(a.test_issues,encoding='utf-8')) if a.test_issues else []
 tests=tests+[dict(cohort=r[1],student_registration_number=r[6],full_name=r[4]) for r in ti]
 rows=compute(ledger,policy,pm,tests,ov,test_detail=td,coding_dir=a.notebook_grades,coding_detail=cd,quiz_dir=a.quiz_dir,aliases=al,notes=load_override_notes(a.overrides) if a.overrides else None,test_issues=[r[6] for r in ti])
 stamp=str(ledger.get('updated_at',''))[:16].replace('T',' ')+' UTC (ledger)'
 n=write_workbook(rows,policy,a.out,stamp,str(a.ledger).split('/')[-1]+' and policy 2026-11-10')
 print(f'{len(rows)} students; {n} items handed in but not marked yet; {getattr(compute,"applied",0)} regrade marks applied; written to {a.out}')
 return rows

if __name__=='__main__':
 main()
