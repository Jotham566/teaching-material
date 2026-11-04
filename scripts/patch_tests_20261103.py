"""Update tests/test_continuous_assessment.py, tests/test_assessment_waivers.cjs, tests/test_coursework_agreement_20261102.cjs
and the two block tests for the decision of 3 November 2026. Originals are copied to tests/_backup_2026-11-03 first (first copy wins).
Every replacement asserts its match count. Idempotent (a marker line is added). Usage: python3 scripts/patch_tests_20261103.py"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from backup_20261103 import backup

TESTS = ROOT / "tests"
MARK = "TESTS_PATCHED_20261103"


class T:
    def __init__(self, name):
        self.path = TESTS / name
        self.text = self.path.read_text()
        self.skip = MARK in self.text
        if not self.skip:
            backup(self.path)

    def rep(self, old, new, count=1):
        if self.skip:
            return
        n = self.text.count(old)
        assert n == count, f"{self.path.name}: expected {count} match(es), found {n}: {old[:70]!r}"
        self.text = self.text.replace(old, new)

    def save(self, comment):
        if self.skip:
            print(f"{self.path.name}: already patched")
            return
        self.text = self.text.rstrip("\n") + f"\n{comment} {MARK}\n"
        self.path.write_text(self.text)
        print(f"{self.path.name}: patched")


# ----------------------------------------------------------------------------------------------------------------- python
PY_NEW_CLASSES = r'''def graded(sid,assess,score,cohort='CML3111',status='GRADED',**extra):
 return dict(cohort=cohort,student_id=sid,assessment=assess,score=score,status=status,**extra)
FULL_QUIZ={f'Q{w}':5 for w in (1,2,3,4,5,8,9,10,11)};FULL_ASSIGN={f'W{w:02}':20 for w in (1,2,3,4,5,8,9,10,11,12)}
def full_coursework(sid,cohort='CML3111'):
 return [graded(sid,a,v,cohort) for a,v in {**FULL_QUIZ,**FULL_ASSIGN}.items()]
class SemesterTotalsTests(unittest.TestCase):
 """Decision of 3 November 2026: no demo; project = Part A /30 + Part B /15, weight 45; provisional x of 55 until both parts are marked."""
 def test_weights_sum_to_100_and_provisional_is_55(self):
  self.assertEqual(sum(COURSE_WEIGHTS.values()),100);self.assertEqual(PROVISIONAL_OUT_OF,55);self.assertEqual(PROVISIONAL_OUT_OF+COURSE_WEIGHTS['engineering_ml_project'],100)
  self.assertEqual(PROJECT_MAX,45);self.assertEqual(sum(m for _,m in PROJECT_PARTS),COURSE_WEIGHTS['engineering_ml_project'])
  self.assertEqual(set(COURSE_WEIGHTS),{'quizzes','assignments','data_analysis_project','practical_test_1','engineering_ml_project'})
 def test_provisional_with_no_project(self):
  cur=full_coursework('S1')+[graded('S1','DA_PROJECT',100),graded('S1','TEST1',100)]
  r=semester_totals(cur)[0]
  self.assertIsNone(r['final']);self.assertEqual(r['project_status'],'Project: PENDING');self.assertTrue(r['project']['pending'])
  self.assertEqual((r['provisional']['marks'],r['provisional']['out_of'],r['provisional']['percent']),(55,55,100))
  self.assertEqual(r['provisional']['text'],'Semester 1 provisional: 55.00 of 55 marks, 100.00 percent');self.assertEqual(r['missing'],[])
 def test_provisional_with_only_part_a(self):
  cur=full_coursework('S1')+[graded('S1','DA_PROJECT',72),graded('S1','TEST1',65),graded('S1','ML_PROJECT',None,status='PART_MARKED',part_scores={'A':27,'B':None})]
  r=semester_totals(cur)[0]
  self.assertIsNone(r['final']);self.assertEqual(r['project_status'],'Project: PENDING');self.assertEqual((r['project']['part_a'],r['project']['part_b']),(27,None))
  self.assertEqual(r['provisional']['marks'],round2(15+15+7.2+9.75));self.assertEqual(r['provisional']['text'],'Semester 1 provisional: 46.95 of 55 marks, 85.36 percent')
  # Part A alone changes nothing in the provisional line
  without=semester_totals(full_coursework('S1')+[graded('S1','DA_PROJECT',72),graded('S1','TEST1',65)])[0]
  self.assertEqual(r['provisional'],without['provisional'])
 def test_a_held_receipt_cannot_leak_project_marks_in(self):
  cur=full_coursework('S1')+[graded('S1','ML_PROJECT',None,status='IDENTITY_CONFLICT',part_scores={'A':30,'B':15})]
  r=semester_totals(cur)[0];self.assertIsNone(r['final']);self.assertIsNone(r['project']['part_a'])
 def test_full_total_once_both_parts_are_marked(self):
  cur=full_coursework('S1')+[graded('S1','DA_PROJECT',80),graded('S1','TEST1',60),graded('S1','ML_PROJECT',33,part_scores={'A':24,'B':9})]
  r=semester_totals(cur)[0]
  self.assertEqual(r['final'],80.0);self.assertEqual(r['project_status'],'Project: marked');self.assertFalse(r['project']['pending'])
  self.assertEqual(r['project']['weighted'],33.0);self.assertEqual(r['provisional']['marks'],47.0)   # 15 + 15 + 8 + 9
  self.assertEqual(r['final'],round2(r['provisional']['marks']+r['project']['weighted']))
 def test_typed_zero_parts_are_a_mark_of_zero_not_pending(self):
  cur=full_coursework('S1')+[graded('S1','DA_PROJECT',100),graded('S1','TEST1',100),graded('S1','ML_PROJECT',0,part_scores={'A':0,'B':0})]
  r=semester_totals(cur)[0];self.assertEqual(r['final'],55.0);self.assertFalse(r['project']['pending'])
 def test_student_with_no_submissions(self):
  r=semester_totals([],students=[('CML3112','NOBODY')])[0]
  self.assertEqual((r['cohort'],r['student_id']),('CML3112','NOBODY'));self.assertIsNone(r['final']);self.assertEqual(r['project_status'],'Project: PENDING')
  self.assertEqual((r['provisional']['marks'],r['provisional']['percent']),(0,0));self.assertEqual(r['provisional']['text'],'Semester 1 provisional: 0.00 of 55 marks, 0.00 percent')
  self.assertEqual((r['quizzes']['earned'],r['quizzes']['available'],r['assignments']['earned'],r['assignments']['available']),(0,35,0,160))
  self.assertEqual(r['missing'],['Data Analysis Project','Practical Test 1','Block 1 quiz','Block 2 quiz','Block 1 assignment','Block 2 assignment'])
  self.assertNotIn('ML Project',' '.join(r['missing']))   # pending is not missing
  # once the project is marked as 0 and 0 the same student has a final of 0
  done=semester_totals([graded('NOBODY','ML_PROJECT',0,cohort='CML3112',part_scores={'A':0,'B':0})])[0];self.assertEqual(done['final'],0.0)
 def test_missing_quiz_or_assignment_part_still_scores_zero(self):
  cur=[graded('S1','W08',20),graded('S1','W10',20),graded('S1','W11',20),graded('S1','DA_PROJECT',100),graded('S1','TEST1',100)]
  r=semester_totals(cur)[0];self.assertEqual(r['assignments']['blocks'][0]['earned'],20);self.assertEqual(r['assignments']['blocks'][1]['earned'],40)
  self.assertEqual(r['quizzes']['earned'],0);self.assertIn('Block 1 quiz',r['missing']);self.assertEqual(r['provisional']['marks'],round2(60/160*15+10+15))
 def test_leftover_demo_and_test2_receipts_are_ignored(self):
  cur=full_coursework('S1')+[graded('S1','DA_PROJECT',100),graded('S1','TEST1',100),graded('S1','DEMO',100),graded('S1','TEST2',100)]
  r=semester_totals(cur)[0];self.assertEqual(r['provisional']['marks'],55);self.assertIsNone(r['final'])
 def test_totals_csv_has_blank_final_while_pending(self):
  import csv as _csv
  rows=semester_totals(full_coursework('S1')+[graded('S1','DA_PROJECT',100),graded('S1','TEST1',100)]+full_coursework('S2')+[graded('S2','DA_PROJECT',100),graded('S2','TEST1',100),graded('S2','ML_PROJECT',45,part_scores={'A':30,'B':15})])
  with tempfile.TemporaryDirectory() as d:
   write_totals_csv(rows,Path(d)/'t.csv');out={o['student_id']:o for o in _csv.DictReader((Path(d)/'t.csv').open())}
  self.assertEqual((out['S1']['final_percent'],out['S1']['project_status']),('','Project: PENDING'))
  self.assertEqual((out['S2']['final_percent'],out['S2']['project_status']),('100.0','Project: marked'))
  self.assertEqual(out['S1']['provisional_marks'],'55.0')
 def test_build_accepts_part_scores_and_rejects_bad_ones(self):
  def manifest(p):
   (p/'CML3111_ML_PROJECT_manifest.json').write_text(json.dumps(dict(key='CML3111|ML_PROJECT',exported_at='test',window=dict(open='2026-11-24T00:00:00Z',close='2026-12-11T20:59:00Z'),
    files=[dict(id='f1',sha256='aa')],records=[dict(response_id='r1',email='demo@example.com',submitted_at='2026-12-01T08:00:00Z',file_ids=['f1'],fields={'Student Registration Number':'DEMO-01','Full name':'Demo Student'})])))
  def run(p,**g):
   (p/'results.json').write_text(json.dumps([dict(response_id='r1',cohort='CML3111',assessment='ML_PROJECT',student_id='DEMO-01',source_hashes={'f1':'aa'},**g)]))
   return build(p,str(p/'results.json'),timing={})
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);manifest(p)
   a=run(p,status='PART_MARKED',score=None,part_scores={'A':24.5});r=semester_totals(a['current'])[0]
   self.assertEqual(r['project_status'],'Project: PENDING');self.assertEqual(r['project']['part_a'],24.5);self.assertEqual(a['current'][0]['maximum'],45)
   b=run(p,status='GRADED',score=None,part_scores={'A':24.5,'B':9});r=semester_totals(b['current'])[0]
   self.assertEqual(r['project_status'],'Project: marked');self.assertEqual(b['current'][0]['score'],33.5);self.assertEqual(r['project']['weighted'],33.5)
   for bad in (dict(status='GRADED',score=None,part_scores={'A':31,'B':9}),dict(status='GRADED',score=None,part_scores={'A':24,'B':16}),dict(status='GRADED',score=None,part_scores={'A':24}),
               dict(status='PART_MARKED',score=None,part_scores={'A':24,'B':9}),dict(status='GRADED',score=40,part_scores={'A':24,'B':9}),dict(status='PART_MARKED',score=10,part_scores={'A':24}),
               dict(status='PART_MARKED',score=None,part_scores={'C':1}),dict(status='GRADED',score=33,part_scores={'A':'x','B':9})):
    with self.assertRaises(ValueError,msg=str(bad)):run(p,**bad)
class CommandLineTotalsTests(unittest.TestCase):
 def test_totals_from_an_existing_ledger(self):
  import subprocess,csv as _csv
  with tempfile.TemporaryDirectory() as d:
   led=Path(d)/'ledger.json'
   led.write_text(json.dumps(dict(students=[dict(cohort='CML3111',student_id='S1'),dict(cohort='CML3111',student_id='NOBODY')],attempts=[],
     current=full_coursework('S1')+[graded('S1','DA_PROJECT',100),graded('S1','TEST1',100)])))
   cmd=[sys.executable,'-I','-B',str(Path(__file__).resolve().parents[1]/'IUEA_Teaching_Plan/grader/continuous_assessment.py'),'--from-ledger',str(led),'--totals-out',str(Path(d)/'t.csv')]
   r=subprocess.run(cmd,capture_output=True,text=True);self.assertEqual(r.returncode,0,r.stderr)
   out={o['student_id']:o for o in _csv.DictReader((Path(d)/'t.csv').open())}
   self.assertEqual(out['S1']['provisional_marks'],'55.0');self.assertEqual(out['S1']['final_percent'],'');self.assertEqual(out['S1']['project_status'],'Project: PENDING')
   self.assertEqual(out['NOBODY']['provisional_marks'],'0.0')
   bad=subprocess.run(cmd[:-2],capture_output=True,text=True);self.assertNotEqual(bad.returncode,0)   # --from-ledger without --totals-out is refused
class PolicyFilesInStepTests(unittest.TestCase):
 def test_blocks_calendar_and_rules_of_20261102_equal_20261103(self):
  root=Path(__file__).resolve().parents[1]
  old=json.loads((root/'data/assessment_blocks_20261102.json').read_text());new=json.loads((root/'data/assessment_blocks_20261103.json').read_text())
  for k in ('blocks','retired_quiz_forms','coursework_rule','forms_in_use'):self.assertEqual(old[k],new[k],k)
  self.assertEqual(old['calendar']['class_dates'],new['calendar']['class_dates']);self.assertEqual(old['calendar']['week_12_demo']['dates'],new['calendar']['week_12_project_clinic']['dates'])
  self.assertEqual(new['supersedes'],'data/assessment_blocks_20261102.json');self.assertNotIn('week_12_demo',new['calendar'])
 def test_project_dates_are_proposed_and_due_is_11_december_2359_kampala(self):
  new=json.loads((Path(__file__).resolve().parents[1]/'data/assessment_blocks_20261103.json').read_text())['engineering_ml_project']
  self.assertEqual(new['due']['all_cohorts'],'2026-12-11T23:59:00+03:00');self.assertIn('proposed',new['due']['status']);self.assertIn('proposed',new['released']['status'])
class ContinuousAssessmentTests(unittest.TestCase):'''


def patch_python():
    t = T("test_continuous_assessment.py")
    t.rep("coursework_totals,BLOCKS,WAIVED_WEEKS,QUIZ_WEEKS,ASSIGNMENT_WEEKS,COURSE_WEIGHTS,COURSEWORK_WEIGHT,RETIRED_QUIZ_WEEKS,round2",
          "coursework_totals,BLOCKS,WAIVED_WEEKS,QUIZ_WEEKS,ASSIGNMENT_WEEKS,COURSE_WEIGHTS,COURSEWORK_WEIGHT,RETIRED_QUIZ_WEEKS,round2,semester_totals,write_totals_csv,PROJECT_PARTS,PROJECT_MAX,PROVISIONAL_OUT_OF,PROVISIONAL_KEYS")
    t.rep("data/assessment_blocks_20261102.json').read_text())\n  wk=", "data/assessment_blocks_20261103.json').read_text())\n  wk=")
    t.rep("pol=json.loads((root/'data/assessment_blocks_20261102.json').read_text());rows=", "pol=json.loads((root/'data/assessment_blocks_20261103.json').read_text());rows=")
    t.rep("""  self.assertEqual(COURSE_WEIGHTS,{k:v for k,v in pol['weights_percent'].items()})
  self.assertNotIn('practical_test_2',pol['weights_percent']);self.assertEqual(COURSEWORK_WEIGHT,15)""",
          """  self.assertEqual(COURSE_WEIGHTS,{k:v for k,v in pol['weights_percent'].items()})
  self.assertNotIn('practical_test_2',pol['weights_percent']);self.assertNotIn('demonstration',pol['weights_percent']);self.assertNotIn('demonstration',COURSE_WEIGHTS)
  self.assertEqual(COURSEWORK_WEIGHT,15);self.assertEqual(COURSE_WEIGHTS['engineering_ml_project'],45)
  self.assertEqual(tuple((p['part'],p['marks']) for p in pol['engineering_ml_project']['parts']),PROJECT_PARTS);self.assertEqual(PROJECT_MAX,pol['engineering_ml_project']['marks'])
  self.assertEqual(PROVISIONAL_OUT_OF,pol['provisional_mode']['provisional_weight_total']);self.assertEqual(list(PROVISIONAL_KEYS),pol['provisional_mode']['components_marked_for_provisional'])""")
    t.rep("""   self.assertTrue(rows[f'{code}|TEST2'].get('retired'));self.assertIsNone(rows[f'{code}|TEST2']['closes_at'])""",
          """   self.assertTrue(rows[f'{code}|TEST2'].get('retired'));self.assertIsNone(rows[f'{code}|TEST2']['closes_at'])
   d=rows[f'{code}|DEMO'];self.assertTrue(d.get('retired'));self.assertEqual(d['status'],'RETIRED');self.assertIsNone(d['opens_at']);self.assertIsNone(d['closes_at'])
   m=rows[f'{code}|ML_PROJECT'];self.assertFalse(m.get('retired'));self.assertEqual(m['maximum'],45);self.assertEqual([(p['part'],p['maximum']) for p in m['parts']],list(PROJECT_PARTS))
   self.assertIsNone(m['opens_at']);self.assertIsNone(m['closes_at'])   # no form window is opened by the 3 November decision
   self.assertEqual(m['proposed_closes_at'],pol['engineering_ml_project']['due']['all_cohorts']);self.assertIn('proposed',m['proposed_status'])
   self.assertEqual(m['proposed_released_after_class_4'],pol['engineering_ml_project']['released']['dates'][code])""")
    t.rep("class ContinuousAssessmentTests(unittest.TestCase):", PY_NEW_CLASSES)
    t.save("#")


# ----------------------------------------------------------------------------------------------------------------- waivers
def patch_waivers():
    t = T("test_assessment_waivers.cjs")
    t.rep("dataProject:100,test1:100,mlProject:100,demo:100};", "dataProject:100,test1:100,mlProjectA:30,mlProjectB:15,mlProject:100,demo:100};")
    t.rep("const only={cohort,quizzes:['','','','','',5],challenges:['','','','','',20]};assert.equal(c.computeFinal_(only).final,0);",
          "const only={cohort,quizzes:['','','','','',5],challenges:['','','','','',20]};assert.equal(c.computeFinal_(only).final,null);assert.equal(c.computeFinal_(only).provisional.marks,0);")
    t.rep("assert.equal(c.computeFinal_({cohort:'CML3111',quizzes:['','','','','',5],challenges:['','','','','',20]}).final,0);",
          "assert.equal(c.computeFinal_({cohort:'CML3111',quizzes:['','','','','',5],challenges:['','','','','',20]}).provisional.marks,0);")
    t.save("//")


# ----------------------------------------------------------------------------------------------------------------- readers repointed
def patch_block_tests():
    t = T("test_block_sittings_20261102.cjs")
    t.rep("data/assessment_blocks_20261102.json', 'utf8'", "data/assessment_blocks_20261103.json', 'utf8'")
    t.rep("console.log('PASS plan in the .gs files matches data/assessment_blocks_20261102.json');", "console.log('PASS plan in the .gs files matches data/assessment_blocks_20261103.json');")
    t.save("//")
    t = T("test_block_windows_20261102.cjs")
    t.rep("data/assessment_blocks_20261102.json', 'utf8'", "data/assessment_blocks_20261103.json', 'utf8'")
    t.save("//")


# ----------------------------------------------------------------------------------------------------------------- agreement
def patch_agreement():
    t = T("test_coursework_agreement_20261102.cjs")
    t.rep("// gradebook.gs and grader/continuous_assessment.py must give the same quiz and assignment totals (35 and 160 marks, 15 percent each).",
          "// gradebook.gs and grader/continuous_assessment.py must give the same quiz and assignment totals (35 and 160 marks, 15 percent each)\n// AND (3 November 2026) the same provisional line (x of 55) and final total (out of 100) once the project parts are marked.")
    t.rep("data/assessment_blocks_20261102.json', 'utf8'", "data/assessment_blocks_20261103.json', 'utf8'")
    t.rep("assert.deepEqual(JSON.parse(JSON.stringify(c.WEIGHTS)), { quizzes: 15, challenges: 15, dataProject: 10, test1: 15, mlProject: 30, demo: 15 });",
          "assert.deepEqual(JSON.parse(JSON.stringify(c.WEIGHTS)), { quizzes: 15, challenges: 15, dataProject: 10, test1: 15, mlProject: 45 });")
    t.rep("assert.equal(c.WEIGHTS.test1, w.practical_test_1); assert.equal(c.WEIGHTS.mlProject, w.engineering_ml_project); assert.equal(c.WEIGHTS.demo, w.demonstration);",
          "assert.equal(c.WEIGHTS.test1, w.practical_test_1); assert.equal(c.WEIGHTS.mlProject, w.engineering_ml_project); assert.ok(!('demonstration' in w) && !('demo' in c.WEIGHTS));\n"
          "assert.equal(c.ML_PART_A_MAX + c.ML_PART_B_MAX, pol.engineering_ml_project.marks); assert.deepEqual(J2(pol.engineering_ml_project.parts.map(p => [p.part, p.marks])), [['A', c.ML_PART_A_MAX], ['B', c.ML_PART_B_MAX]]);\n"
          "assert.equal(c.provisionalOutOf_(), pol.provisional_mode.provisional_weight_total); assert.deepEqual(J2(c.PROJECT_INPUT_HEADERS), J2(pol.engineering_ml_project.parts.map(p => p.gradebook_column)));\n"
          "assert.equal(c.PROVISIONAL_HEADER, pol.provisional_mode.gradebook_columns.provisional_text); assert.equal(c.PROJECT_STATUS_HEADER, pol.provisional_mode.gradebook_columns.project_status);\n"
          "assert.equal(c.PROJECT_PENDING_TEXT, pol.provisional_mode.project_status_text.pending); assert.equal(c.PROJECT_MARKED_TEXT, pol.provisional_mode.project_status_text.marked);")
    t.rep("const pol = JSON.parse(", "const J2 = x => JSON.parse(JSON.stringify(x));\nconst pol = JSON.parse(")
    t.rep("let seed = 20261102;", "let seed = 20261103;")
    # students: add DA, Test 1 and the two project parts (blank with some probability, so pending is exercised)
    t.rep("  quizzes: Array.from({ length: 12 }, () => pick(5)), challenges: Array.from({ length: 11 }, () => pick(20)) });",
          "  quizzes: Array.from({ length: 12 }, () => pick(5)), challenges: Array.from({ length: 11 }, () => pick(20)),\n"
          "  dataProject: pick(100), test1: pick(100), mlProjectA: pick(30), mlProjectB: pick(15) });")
    t.rep("const py = `\nimport json,sys\nsys.path.insert(0,'IUEA_Teaching_Plan/grader')\nfrom continuous_assessment import coursework_totals\ndata=json.load(sys.stdin);cur=[]\nfor d in data:\n  for a,v in d['marks'].items(): cur.append(dict(cohort=d['cohort'],student_id=d['sid'],assessment=a,score=v,status='GRADED'))\nout={(r['cohort'],r['student_id']):r for r in coursework_totals(cur)}\nprint(json.dumps([out.get((d['cohort'],d['sid'])) for d in data]))`;",
          "const py = `\nimport json,sys\nsys.path.insert(0,'IUEA_Teaching_Plan/grader')\nfrom continuous_assessment import coursework_totals,semester_totals\ndata=json.load(sys.stdin);cur=[]\nfor d in data:\n  for a,v in d['marks'].items(): cur.append(dict(cohort=d['cohort'],student_id=d['sid'],assessment=a,score=v,status='GRADED'))\n"
          "  for a,k in (('DA_PROJECT','da'),('TEST1','t1')):\n    if d[k] is not None: cur.append(dict(cohort=d['cohort'],student_id=d['sid'],assessment=a,score=d[k],status='GRADED'))\n"
          "  pa,pb=d['pa'],d['pb']\n  if pa is not None or pb is not None:\n    full=pa is not None and pb is not None\n    cur.append(dict(cohort=d['cohort'],student_id=d['sid'],assessment='ML_PROJECT',score=(pa+pb) if full else None,status='GRADED' if full else 'PART_MARKED',part_scores=dict(A=pa,B=pb)))\n"
          "out={(r['cohort'],r['student_id']):r for r in coursework_totals(cur)}\n"
          "tot={(r['cohort'],r['student_id']):r for r in semester_totals(cur,[(d['cohort'],d['sid']) for d in data])}\n"
          "print(json.dumps([[out.get((d['cohort'],d['sid'])),tot[(d['cohort'],d['sid'])]] for d in data]))`;")
    t.rep("const receipts = students.map((s, n) => { const m = {}; s.quizzes.forEach((v, i) => { if (v !== '') m[quizIds[i]] = v; }); s.challenges.forEach((v, i) => { if (v !== '') m[asgIds[i]] = v; }); return { sid: 'S' + n, cohort: s.cohort, marks: m }; });",
          "const nz = v => (v === '' ? null : v);\nconst receipts = students.map((s, n) => { const m = {}; s.quizzes.forEach((v, i) => { if (v !== '') m[quizIds[i]] = v; }); s.challenges.forEach((v, i) => { if (v !== '') m[asgIds[i]] = v; });\n"
          "  return { sid: 'S' + n, cohort: s.cohort, marks: m, da: nz(s.dataProject), t1: nz(s.test1), pa: nz(s.mlProjectA), pb: nz(s.mlProjectB) }; });")
    t.rep("const pyRows = JSON.parse(res.stdout);", "const pyAll = JSON.parse(res.stdout); const pyRows = pyAll.map(x => x[0]); const pyTot = pyAll.map(x => x[1]);")
    t.rep("let compared = 0;", "let compared = 0, pendingSeen = 0, markedSeen = 0;")
    t.rep("  const g = c.computeFinal_(Object.assign({}, s, { dataProject: '', test1: '', mlProject: '', demo: '' }));",
          "  const g = c.computeFinal_(Object.assign({}, s));\n"
          "  // provisional and final agree between the two implementations, to the hundredth\n"
          "  const T = pyTot[n];\n"
          "  assert.equal(g.provisional.marks, T.provisional.marks, 'provisional marks, student ' + n); assert.equal(g.provisional.percent, T.provisional.percent, 'provisional percent, student ' + n);\n"
          "  assert.equal(g.provisional.text, T.provisional.text); assert.equal(g.projectStatus, T.project_status); assert.equal(g.projectPending, T.project.pending);\n"
          "  assert.equal(g.final, T.final, 'final, student ' + n);\n"
          "  if (g.projectPending) { pendingSeen++; assert.equal(g.final, null); assert.equal(g.band, null); } else { markedSeen++; assert.ok(g.final >= g.provisional.marks - 0.005 && g.final <= 100.005); }")
    t.rep("assert.ok(compared > 250, 'only ' + compared + ' students compared');", "assert.ok(compared > 250, 'only ' + compared + ' students compared');\nassert.ok(pendingSeen > 50 && markedSeen > 50, 'both modes must be exercised: pending ' + pendingSeen + ', marked ' + markedSeen);")
    t.rep("console.log('PASS gradebook.gs and continuous_assessment.py agree for ' + compared + ' seeded students: quizzes out of 35, assignments out of 160, 15 percent each.');",
          "console.log('PASS gradebook.gs and continuous_assessment.py agree for ' + compared + ' seeded students: quizzes out of 35, assignments out of 160, 15 percent each; provisional (x of 55) for ' + pendingSeen + ' pending and full totals out of 100 for ' + markedSeen + ' marked.');")
    t.save("//")


if __name__ == "__main__":
    patch_python()
    patch_waivers()
    patch_block_tests()
    patch_agreement()
