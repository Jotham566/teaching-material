"""Patch grader/continuous_assessment.py for the decision of 3 November 2026 (data/assessment_blocks_20261103.json).

Weights now quizzes 15, assignments 15, data analysis project 10, Practical Test 1 15, Engineering ML project 45; no demonstration.
Adds semester_totals() (provisional x of 55 until both project parts are marked, then the full total out of 100, the same rules and
rounding as gradebook.gs), project part scores on ML_PROJECT receipts, and a --totals-out CSV option on the command line.
Backs the file up first (first copy wins); every replacement asserts its match count. Idempotent.
Usage: python3 scripts/patch_continuous_assessment_20261103.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from backup_20261103 import backup

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "IUEA_Teaching_Plan" / "grader" / "continuous_assessment.py"
MARK = "SEMESTER_TOTALS_20261103"


def rep(text, old, new, count=1):
    n = text.count(old)
    assert n == count, f"expected {count} match(es), found {n}: {old[:70]!r}"
    return text.replace(old, new)


WEIGHTS_OLD = "COURSE_WEIGHTS=dict(quizzes=15,assignments=15,data_analysis_project=10,practical_test_1=15,engineering_ml_project=30,demonstration=15)  # sums to 100; no Practical Test 2\n"
WEIGHTS_NEW = '''# Decision of 3 November 2026 (data/assessment_blocks_20261103.json is the source of truth; a test keeps this in step): no demo, no Practical Test 2.
# The Engineering ML project is a take-home submission graded like Practical Test 1: Part A coded notebook /30 + Part B decision memo /15.
COURSE_WEIGHTS=dict(quizzes=15,assignments=15,data_analysis_project=10,practical_test_1=15,engineering_ml_project=45)  # sums to 100
PROJECT_PARTS=(('A',30),('B',15))  # (part, maximum); the project counts only when BOTH parts are marked
PROJECT_MAX=sum(m for _,m in PROJECT_PARTS)
PROVISIONAL_KEYS=('quizzes','assignments','data_analysis_project','practical_test_1')  # marked before the project
PROVISIONAL_OUT_OF=sum(COURSE_WEIGHTS[k] for k in PROVISIONAL_KEYS)  # 55
'''

HEADER_OLD = "# Block arrangement of 2 November 2026 (data/assessment_blocks_20261102.json is the source of truth; a test keeps this in step).\n"
HEADER_NEW = "# Block arrangement of 2 November 2026 (unchanged on 3 November; data/assessment_blocks_20261103.json is the source of truth and a test keeps this in step).\n"

BUILD_MAX_OLD = "status='AWAITING_GRADING',score=None,maximum=20,file_ids=row['file_ids'],source=p.name))"
BUILD_MAX_NEW = "status='AWAITING_GRADING',score=None,maximum=(PROJECT_MAX if assessment=='ML_PROJECT' else 20),file_ids=row['file_ids'],source=p.name))"

RESULTS_OLD = """   value=g.get('score')
   if g['status']=='GRADED' and value is None:raise ValueError('Completed mark must be numeric')
"""
RESULTS_NEW = """   value=g.get('score')
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
"""
RESULTS_OLD2 = "   if g['status']!='GRADED' and value is not None:raise ValueError('Unresolved mark must be blank')\n"
RESULTS_NEW2 = "   if g['status'] not in ('GRADED','PART_MARKED') and value is not None:raise ValueError('Unresolved mark must be blank')\n"

TOTALS = '''
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

def main():'''

MAIN_OLD = """def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--source',required=True);ap.add_argument('--results');ap.add_argument('--timing');ap.add_argument('--out',required=True);ap.add_argument('--test-ledger',action='append',default=[]);a=ap.parse_args()
 data=build(a.source,a.results,json.loads(Path(a.timing).read_text()) if a.timing else None,a.test_ledger)
 p=Path(a.out);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data,indent=2)+'\\n')
"""
MAIN_NEW = """def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--source');ap.add_argument('--results');ap.add_argument('--timing');ap.add_argument('--out');ap.add_argument('--test-ledger',action='append',default=[])
 ap.add_argument('--totals-out',help='also write a CSV of Semester 1 totals: provisional out of 55 until the project is marked, then the full total')
 ap.add_argument('--from-ledger',help='skip the rebuild: read an existing ledger.json and write only the --totals-out CSV');a=ap.parse_args()
 if a.from_ledger:
  if not a.totals_out:ap.error('--from-ledger needs --totals-out')
  data=json.loads(Path(a.from_ledger).read_text())
 else:
  if not a.source or not a.out:ap.error('--source and --out are required unless --from-ledger is used')
  data=build(a.source,a.results,json.loads(Path(a.timing).read_text()) if a.timing else None,a.test_ledger)
  p=Path(a.out);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data,indent=2)+'\\n')
 if a.totals_out:
  t=Path(a.totals_out);t.parent.mkdir(parents=True,exist_ok=True)
  write_totals_csv(semester_totals(data['current'],[(s['cohort'],s['student_id']) for s in data['students']]),t)
"""


def main():
    text = PATH.read_text()
    if MARK in text:
        print("continuous_assessment.py: already patched")
        return
    backup(PATH)
    text = rep(text, HEADER_OLD, HEADER_NEW)
    text = rep(text, WEIGHTS_OLD, WEIGHTS_NEW)
    text = rep(text, BUILD_MAX_OLD, BUILD_MAX_NEW)
    text = rep(text, RESULTS_OLD, RESULTS_NEW)
    text = rep(text, RESULTS_OLD2, RESULTS_NEW2)
    text = rep(text, "def coursework_totals(current,waived_weeks=WAIVED_WEEKS):", "def coursework_totals(current,waived_weeks=WAIVED_WEEKS,extra_students=()):")
    text = rep(text, "  if r['status']=='GRADED' and r['score'] is not None and r['student_id']:\n   marks[(r['cohort'],r['student_id'])][r['assessment']]=r['score']\n",
               "  if r['status']=='GRADED' and r['score'] is not None and r['student_id']:\n   marks[(r['cohort'],r['student_id'])][r['assessment']]=r['score']\n for k in extra_students:marks[tuple(k)]\n")
    text = rep(text, "\ndef main():", TOTALS)
    text = rep(text, MAIN_OLD, MAIN_NEW)
    text = text.rstrip("\n") + f"\n# {MARK}: patched 3 November 2026\n"
    PATH.write_text(text)
    print("continuous_assessment.py: patched")


if __name__ == "__main__":
    main()
