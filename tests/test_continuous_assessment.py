import sys,unittest,json,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'IUEA_Teaching_Plan/grader'))
from continuous_assessment import choose_current,identity_conflicts,quiz_mark,build,field,norm,recover_quiz_ids,resolve_supported_typos,coursework_totals,BLOCKS,WAIVED_WEEKS,QUIZ_WEEKS,ASSIGNMENT_WEEKS,COURSE_WEIGHTS,COURSEWORK_WEIGHT,RETIRED_QUIZ_WEEKS,round2,semester_totals,write_totals_csv,PROJECT_PARTS,PROJECT_MAX,PROVISIONAL_OUT_OF,PROVISIONAL_KEYS

def receipt(**kwargs):
 r=dict(cohort='CML3111',student_id='DEMO-01',email='demo@example.com',assessment='W03',response_id='r1',submitted_at='2026-10-01T08:00:00Z',timing_status='ON_TIME',status='GRADED',score=15)
 r.update(kwargs);return r
class BlockCourseworkTests(unittest.TestCase):
 """Policy of 2 November 2026: Weeks 1 to 5 weekly (best 3 of 5, Week 6 waived), Block 1 = Q7+Q8 and A7+A8,
 Block 2 = Q9+Q10 and A9+A10+A11. Q11 and Q12 are retired. Quizzes are out of 35, assignments out of 160, 15 percent each."""
 def rows(self,quiz,assign,sid='DEMO-01'):
  return [receipt(student_id=sid,assessment=a,score=v,response_id=f'{sid}-{a}') for a,v in {**quiz,**assign}.items()]
 def test_full_marks_give_fifteen_percent_each(self):
  q={f'Q{w}':5 for w in (1,2,3,4,5,8,9,10,11)};a={f'W{w:02}':20 for w in (1,2,3,4,5,8,9,10,11,12)}
  r=coursework_totals(self.rows(q,a))[0]
  self.assertEqual((r['quizzes']['available'],r['assignments']['available']),(35,160))
  self.assertEqual((r['quizzes']['earned'],r['assignments']['earned']),(35,160))
  self.assertEqual((r['quizzes']['weighted'],r['assignments']['weighted']),(15.0,15.0))
 def test_weekly_drops_two_lowest_of_five_and_blocks_are_never_dropped(self):
  q={'Q1':0,'Q2':5,'Q3':5,'Q4':5,'Q5':2,'Q8':5,'Q9':5}
  r=coursework_totals(self.rows(q,{}))[0]['quizzes']
  self.assertEqual(r['earned'],15+10)   # best 3 of 5 weekly = 5+5+5; Block 1 = 10; Block 2 not sat = 0
  self.assertEqual(r['weighted'],round(25/35*15,2))
 def test_missing_block_part_scores_zero(self):
  a={'W08':20,'W10':20,'W11':20}
  r=coursework_totals(self.rows({},a))[0]['assignments']
  self.assertEqual(r['blocks'][0],dict(block='Block 1',earned=20,available=40,parts_submitted=1))
  self.assertEqual(r['blocks'][1],dict(block='Block 2',earned=40,available=60,parts_submitted=2))
 def test_retired_quizzes_q11_and_q12_never_count(self):
  base={'Q1':5,'Q2':5,'Q3':5,'Q8':5,'Q9':5,'Q10':5,'Q11':5}
  with_retired={**base,'Q12':5,'Q13':5}
  a=coursework_totals(self.rows(base,{}))[0]['quizzes'];b=coursework_totals(self.rows(with_retired,{}))[0]['quizzes']
  self.assertEqual(a,b);self.assertEqual(b['earned'],15+10+10)
 def test_block_one_two_and_weekly_maxima_add_up_to_the_stated_totals(self):
  r=coursework_totals(self.rows({'Q1':1},{'W01':1}))[0]
  self.assertEqual([x['available'] for x in r['quizzes']['blocks']],[10,10])
  self.assertEqual([x['available'] for x in r['assignments']['blocks']],[40,60])
  self.assertEqual(r['quizzes']['available'],3*5+10+10);self.assertEqual(r['assignments']['available'],3*20+40+60)
 def test_constants_match_policy_file(self):
  pol=json.loads((Path(__file__).resolve().parents[1]/'data/assessment_blocks_20261103.json').read_text())
  wk=lambda b:tuple(f'Q{q["week"]}' for q in b['quiz_forms'])
  self.assertEqual(BLOCKS['quizzes'],tuple((b['label'],wk(b)) for b in pol['blocks']))
  self.assertEqual(BLOCKS['assignments'],tuple((b['label'],tuple(p['id'] for p in b['assignment_parts'])) for b in pol['blocks']))
  self.assertEqual(WAIVED_WEEKS,(6,))
  self.assertEqual(sum(pol['weights_percent'].values()),100);self.assertEqual(sum(COURSE_WEIGHTS.values()),100)
  self.assertEqual(COURSE_WEIGHTS,{k:v for k,v in pol['weights_percent'].items()})
  self.assertNotIn('practical_test_2',pol['weights_percent']);self.assertNotIn('demonstration',pol['weights_percent']);self.assertNotIn('demonstration',COURSE_WEIGHTS)
  self.assertEqual(COURSEWORK_WEIGHT,15);self.assertEqual(COURSE_WEIGHTS['engineering_ml_project'],45)
  self.assertEqual(tuple((p['part'],p['marks']) for p in pol['engineering_ml_project']['parts']),PROJECT_PARTS);self.assertEqual(PROJECT_MAX,pol['engineering_ml_project']['marks'])
  self.assertEqual(PROVISIONAL_OUT_OF,pol['provisional_mode']['provisional_weight_total']);self.assertEqual(list(PROVISIONAL_KEYS),pol['provisional_mode']['components_marked_for_provisional'])
  self.assertEqual(RETIRED_QUIZ_WEEKS,tuple(q['week'] for q in pol['retired_quiz_forms']))
  for b in pol['blocks']:
   self.assertEqual(sum(p['marks'] for p in b['assignment_parts']),b['assignment_marks'])
   self.assertEqual(5*len(b['quiz_forms']),b['quiz_marks'])
  self.assertEqual([b['assignment_marks'] for b in pol['blocks']],[40,60]);self.assertEqual([b['quiz_marks'] for b in pol['blocks']],[10,10])
  self.assertEqual(3*5+sum(b['quiz_marks'] for b in pol['blocks']),35);self.assertEqual(3*20+sum(b['assignment_marks'] for b in pol['blocks']),160)
  self.assertEqual(set(QUIZ_WEEKS)&set(RETIRED_QUIZ_WEEKS),set())
 def test_registry_deadlines_match_policy_file(self):
  root=Path(__file__).resolve().parents[1]
  pol=json.loads((root/'data/assessment_blocks_20261103.json').read_text());rows={r['key']:r for r in json.loads((root/'data/assessments.json').read_text())}
  for b in pol['blocks']:
   for p in b['assignment_parts']:
    for code,close in b['assignment_closes'].items():
     r=rows[f'{code}|{p["id"]}'];self.assertEqual(r['closes_at'],close);self.assertEqual(r['label'],p['label']);self.assertEqual(r['block'],b['id'])
  for code in ('CML3111','CML3112','CML3113'):
   self.assertTrue(rows[f'{code}|TEST2'].get('retired'));self.assertIsNone(rows[f'{code}|TEST2']['closes_at'])
   d=rows[f'{code}|DEMO'];self.assertTrue(d.get('retired'));self.assertEqual(d['status'],'RETIRED');self.assertIsNone(d['opens_at']);self.assertIsNone(d['closes_at'])
   m=rows[f'{code}|ML_PROJECT'];self.assertFalse(m.get('retired'));self.assertEqual(m['maximum'],45);self.assertEqual([(p['part'],p['maximum']) for p in m['parts']],list(PROJECT_PARTS))
   self.assertIsNone(m['opens_at']);self.assertIsNone(m['closes_at'])   # no form window is opened by the 3 November decision
   sl=pol['engineering_ml_project']['sitting']['slots'][code];self.assertNotIn('proposed_closes_at',m);self.assertEqual((m['proposed_sitting']['date'],m['proposed_sitting']['start'],m['proposed_sitting']['end']),(sl['date'],sl['start'],sl['end']));self.assertIn('proposed',m['proposed_status'])
   self.assertEqual(m['grading'],'automatic');self.assertEqual(m['formats'],['ipynb']);self.assertNotIn('take-home',m['delivery_note'].lower().replace('no take-home',''))
   self.assertEqual(m['proposed_released_after_class_4'],pol['engineering_ml_project']['released']['dates'][code])
 def test_rounding_halves_go_up_like_the_gradebook(self):
  # Python's round(8.625, 2) is 8.62; gradebook.gs Math.round gives 8.63. The two must not differ by a hundredth.
  self.assertEqual(round2(8.625),8.63);self.assertEqual(round2(8.624),8.62);self.assertEqual(round2(0),0);self.assertEqual(round2(15),15)
 def test_grades_template_has_no_practical_test_2_column(self):
  head=(Path(__file__).resolve().parents[1]/'IUEA_Teaching_Plan/grader/Grades_template.csv').read_text().splitlines()[0].split(',')
  self.assertNotIn('Practical Test 2',head);self.assertIn('Practical Test 1',head)
def graded(sid,assess,score,cohort='CML3111',status='GRADED',**extra):
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
class ContinuousAssessmentTests(unittest.TestCase):
 def test_consistent_alternate_accounts_require_multiple_assessments(self):
  rows=[receipt(email=e,assessment=a) for e in ['one@example.com','two@example.com'] for a in ['W01','Q1']]
  self.assertEqual(identity_conflicts(rows),set())
  self.assertEqual(identity_conflicts([receipt(email='one@example.com'),receipt(email='two@example.com')]),{('CML3111','DEMO-01')})
 def test_early_typo_requires_repeated_same_account_evidence(self):
  rows=[receipt(student_id='99/0001/DEMO-X',submitted_at='2026-10-01T08:00:00Z')]+[receipt(student_id=s,submitted_at=f'2026-10-0{i+2}T08:00:00Z') for i,s in enumerate(['99/0002/DEMO-X','99/0002/DEMOX','99/0002/DEMO-X'])]
  resolve_supported_typos(rows)
  self.assertEqual({r['student_id'] for r in rows},{'99/0002/DEMO-X'})
 def test_typo_resolution_does_not_merge_competing_accounts(self):
  rows=[receipt(student_id='99/0001/DEMO-X')]+[receipt(student_id='99/0002/DEMO-X',submitted_at='2026-10-03T08:00:00Z') for _ in range(3)]
  rows.append(receipt(student_id='99/0002/DEMO-X',email='other@example.com'))
  resolve_supported_typos(rows)
  self.assertEqual(rows[0]['student_id'],'99/0001/DEMO-X')
 def test_blank_quiz_id_requires_unique_same_course_email(self):
  missing=receipt(student_id='',assessment='Q1')
  recover_quiz_ids([missing,receipt()])
  self.assertEqual(missing['student_id'],'DEMO-01')
  ambiguous=receipt(student_id='',assessment='Q1')
  recover_quiz_ids([ambiguous,receipt(),receipt(student_id='DEMO-02')])
  self.assertEqual(ambiguous['student_id'],'')
  other=receipt(student_id='',assessment='Q1',cohort='CML3113')
  recover_quiz_ids([other,receipt()])
  self.assertEqual(other['student_id'],'')
 def test_identity_normalization_does_not_change_digits_or_hyphens(self):
  self.assertEqual(norm(' 99_TEST_000_DEMO-X '),'99/TEST/000/DEMO-X')
  self.assertEqual(norm('99 / TEST / 000 / DEMO-X'),'99/TEST/000/DEMO-X')
  self.assertNotEqual(norm('99/TEST/001/DEMO-X'),norm('99/TEST/000/DEMO-X'))
  self.assertNotEqual(norm('99/TEST/000/DEMOX'),norm('99/TEST/000/DEMO-X'))
 def test_latest_pending_replaces_old_grade(self):
  rows=[receipt(),receipt(response_id='r2',submitted_at='2026-10-02T08:00:00Z',status='AWAITING_GRADING',score=None)]
  current=choose_current(rows);self.assertEqual(current[0]['response_id'],'r2');self.assertIsNone(current[0]['score'])
 def test_late_does_not_erase_eligible(self):
  rows=[receipt(),receipt(response_id='r2',submitted_at='2026-10-02T08:00:00Z',timing_status='LATE',score=20)]
  self.assertEqual(choose_current(rows)[0]['score'],15)
 def test_equal_time_conflict(self):
  self.assertEqual(choose_current([receipt(),receipt(response_id='r2')])[0]['status'],'EQUAL_TIME_CONFLICT')
 def test_same_email_different_registration_flagged(self):
  self.assertEqual(len(identity_conflicts([receipt(),receipt(student_id='DEMO-02')])),2)
 def test_different_cohorts_do_not_collide(self):
  self.assertEqual(identity_conflicts([receipt(),receipt(cohort='CML3113',student_id='DEMO-02')]),set())
 def test_zero_is_valid_recorded_score(self):
  q={'items':[dict(id=i,points=1,correct=['changed answer']) for i in range(5)]};r={'answers':[dict(id=i,answer='earlier answer',score=0) for i in range(5)]}
  self.assertEqual(quiz_mark(q,r),(0,'GRADED'))
 def test_missing_quiz_score_not_silently_zero(self):
  q={'items':[dict(id=i,points=1) for i in range(5)]};r={'answers':[dict(id=i,score=None) for i in range(5)]}
  self.assertEqual(quiz_mark(q,r),(None,'QUIZ_SCORE_PENDING'))
 def test_registration_preferred_over_legacy_and_empty_fallback(self):
  self.assertEqual(field({'Your student number':'old','Student Registration Number':'new'},['registration','student number']),'new')
  self.assertEqual(field({'Your student number':'old','Student Registration Number':''},['registration','student number']),'old')
 def test_build_preserves_source_scores_when_identity_conflicts(self):
  with tempfile.TemporaryDirectory() as directory:
   p=Path(directory)
   records=[]
   for i,sid in enumerate(['DEMO-1','DEMO-2']):
    records.append(dict(response_id=str(i),email='demo@example.com',submitted_at='2026-10-01T08:00:00Z',
     answers=[dict(id='identity',title='Student Registration Number',answer=sid),
              dict(id='total',title='Recorded score',answer='',score=4)]))
   (p/'CML3111_Q1_quiz.json').write_text(json.dumps(dict(exported_at='test',quizzes=[
    dict(key='CML3111|1',items=[dict(id='total',points=5)],records=records)])))
   timing={str(i):dict(status='ON_TIME',evidence='synthetic fixture') for i in range(2)}
   result=build(p,timing=timing)
   self.assertTrue(all(r['status']=='IDENTITY_CONFLICT' and r['score'] is None and r['source_score']==4 for r in result['attempts']))
   again=build(p,timing=timing)
   self.assertEqual(again['attempts'],result['attempts'])
   self.assertEqual(again['current'],result['current'])
 def test_quiz_timing_override_requires_evidence(self):
  with tempfile.TemporaryDirectory() as directory:
   p=Path(directory)
   (p/'CML3111_Q1_quiz.json').write_text(json.dumps(dict(exported_at='test',quizzes=[
    dict(key='CML3111|1',items=[dict(id='total',points=5)],records=[
     dict(response_id='r',email='demo@example.com',submitted_at='2026-10-01T08:00:00Z',answers=[
      dict(id='total',title='score',answer='',score=5)])])])))
   with self.assertRaisesRegex(ValueError,'requires evidence'):
    build(p,timing={'r':dict(status='ON_TIME')})
if __name__=='__main__':unittest.main()
# TESTS_PATCHED_20261103
