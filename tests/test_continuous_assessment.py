import sys,unittest,json,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'IUEA_Teaching_Plan/grader'))
import continuous_assessment as ca
from continuous_assessment import choose_current,identity_conflicts,quiz_mark,build,field,norm,recover_quiz_ids,resolve_supported_typos,coursework_totals,COURSE_WEIGHTS,round2,semester_totals,write_totals_csv,PROJECT_PARTS,PROJECT_MAX,PROVISIONAL_OUT_OF,PROVISIONAL_KEYS,policy_check,QUIZ_IDS,ASSIGNMENT_IDS,COUNTED_IDS,TOTALS_COLUMNS
ROOT=Path(__file__).resolve().parents[1]

def receipt(**kwargs):
 r=dict(cohort='CML3111',student_id='DEMO-01',email='demo@example.com',assessment='W03',response_id='r1',submitted_at='2026-10-01T08:00:00Z',timing_status='ON_TIME',status='GRADED',score=15)
 r.update(kwargs);return r
def graded(sid,assess,score,cohort='CML3111',status='GRADED',**extra):
 return dict(cohort=cohort,student_id=sid,assessment=assess,score=score,status=status,**extra)
def marks(sid,quizzes=(),assignments=(),test=None,cohort='CML3111'):
 """Graded receipts: quizzes Q1.., assignments W01.. from the given lists, and TEST1."""
 rows=[graded(sid,f'Q{i}',v,cohort) for i,v in enumerate(quizzes,1)]+[graded(sid,f'W{i:02}',v,cohort) for i,v in enumerate(assignments,1)]
 return rows+([graded(sid,'TEST1',test,cohort)] if test is not None else [])
def full(sid,cohort='CML3111'):return marks(sid,[5]*5,[20]*5,100,cohort)

class PolicyFileTests(unittest.TestCase):
 """data/assessment_policy_20261110.json is the source of truth; the module constants must equal it."""
 def setUp(self):self.pol=json.loads((ROOT/'data/assessment_policy_20261110.json').read_text())
 def test_policy_check_reports_no_mismatch(self):self.assertEqual(policy_check(),[])
 def test_policy_check_detects_a_changed_policy(self):
  bad=json.loads(json.dumps(self.pol));bad['weights']['quizzes']=15;bad['counted']['quizzes']['ledger_ids']=['Q1','Q2','Q3']
  with tempfile.TemporaryDirectory() as d:
   (Path(d)/'p.json').write_text(json.dumps(bad));found=policy_check(Path(d)/'p.json')
  self.assertEqual(len(found),2);self.assertTrue(found[0].startswith('weights'))
 def test_constants_equal_policy(self):
  p=self.pol;c=p['counted']
  self.assertEqual(COURSE_WEIGHTS,p['weights']);self.assertEqual(COURSE_WEIGHTS,dict(assignments=20,quizzes=20,practical_test_1=20,engineering_ml_project=40))
  self.assertEqual(sum(COURSE_WEIGHTS.values()),p['course_total']);self.assertEqual(p['course_total'],100)
  self.assertEqual(ASSIGNMENT_IDS,tuple(c['assignments']['ledger_ids']));self.assertEqual(QUIZ_IDS,tuple(c['quizzes']['ledger_ids']))
  self.assertEqual(ASSIGNMENT_IDS,('W01','W02','W03','W04','W05'));self.assertEqual(QUIZ_IDS,('Q1','Q2','Q3','Q4','Q5'));self.assertEqual(ca.TEST_ID,c['practical_test_1']['ledger_id'])
  self.assertEqual(COUNTED_IDS,ASSIGNMENT_IDS+QUIZ_IDS+('TEST1',))
  self.assertEqual((ca.ASSIGNMENT_MAX,ca.QUIZ_MAX,ca.TEST_MAX),(c['assignments']['each_max'],c['quizzes']['each_max'],c['practical_test_1']['max']))
  self.assertEqual(PROJECT_PARTS,tuple(c['engineering_ml_project']['parts'].items()));self.assertEqual(PROJECT_MAX,c['engineering_ml_project']['raw_max']);self.assertEqual(PROJECT_MAX,45)
  self.assertEqual(COURSE_WEIGHTS['engineering_ml_project'],c['engineering_ml_project']['scaled_max'])
  self.assertEqual(PROVISIONAL_OUT_OF,p['provisional']['out_of']);self.assertEqual(PROVISIONAL_OUT_OF,60);self.assertEqual(list(PROVISIONAL_KEYS),p['provisional']['components'])
  self.assertEqual(PROVISIONAL_OUT_OF+COURSE_WEIGHTS['engineering_ml_project'],100)
 def test_retired_machinery_is_gone(self):
  for name in ('BLOCKS','WEEKLY_BEST','WAIVED_WEEKS','WEEKLY_WEEKS','COURSEWORK_WEIGHT','_best_weekly'):self.assertFalse(hasattr(ca,name),name)
  self.assertNotIn('data_analysis_project',COURSE_WEIGHTS);self.assertNotIn('demonstration',COURSE_WEIGHTS)
 def test_old_block_file_points_to_the_new_policy(self):
  old=json.loads((ROOT/'data/assessment_blocks_20261103.json').read_text())
  self.assertEqual(old['superseded_by'],'data/assessment_policy_20261110.json')
  self.assertIn('data/assessment_blocks_20261103.json',' '.join(self.pol['supersedes']))
 def test_registry_weights_equal_policy(self):
  sys.path.insert(0,str(ROOT/'scripts'))
  from assessment_registry import WEIGHTS
  self.assertEqual(sorted(WEIGHTS.values()),sorted(self.pol['weights'].values()));self.assertEqual(sum(WEIGHTS.values()),100)
  self.assertEqual(WEIGHTS['ml_project'],self.pol['weights']['engineering_ml_project'])

class CourseworkTests(unittest.TestCase):
 """Assignments A1 to A5 (W01 to W05, /20) and quizzes Q1 to Q5 (/5), all equal, each worth 4 of the 20 for the component."""
 def test_full_marks_give_twenty_each(self):
  r=coursework_totals(full('S1'))[0]
  self.assertEqual((r['assignments']['earned'],r['assignments']['available'],r['assignments']['weighted']),(100,100,20.0))
  self.assertEqual((r['quizzes']['earned'],r['quizzes']['available'],r['quizzes']['weighted']),(25,25,20.0))
 def test_each_item_is_worth_four(self):
  a=coursework_totals(marks('S1',[],[20]))[0];q=coursework_totals(marks('S1',[5]))[0]
  self.assertEqual(a['assignments']['weighted'],4.0);self.assertEqual(q['quizzes']['weighted'],4.0)
  self.assertEqual(coursework_totals(marks('S1',[],[10]))[0]['assignments']['weighted'],2.0)   # 10/20 x 4
 def test_all_five_count_so_nothing_is_dropped(self):
  r=coursework_totals(marks('S1',[0,5,5,5,2],[20,20,0,20,20]))[0]
  self.assertEqual(r['quizzes']['earned'],17);self.assertEqual(r['quizzes']['weighted'],round2(17/25*20))   # 13.6, the zero and the 2 both count
  self.assertEqual(r['assignments']['earned'],80);self.assertEqual(r['assignments']['weighted'],16.0)
 def test_week_six_has_no_waiver(self):
  # The old rule dropped Week 6 and the two lowest of five. W06 is not counted and W01..W05 are never dropped.
  self.assertEqual(coursework_totals(marks('S1',[],[0,20,20,20,20]+[20]))[0]['assignments']['earned'],80)
 def test_nothing_submitted_scores_zero(self):
  r=coursework_totals([],extra_students=[('CML3112','NOBODY')])[0]
  self.assertEqual((r['cohort'],r['student_id']),('CML3112','NOBODY'))
  for part,top in (('assignments',100),('quizzes',25)):self.assertEqual((r[part]['earned'],r[part]['available'],r[part]['weighted']),(0,top,0.0))
 def test_items_beyond_the_five_are_ignored(self):
  base=marks('S1',[5,5,5],[20,20])
  extra=base+[graded('S1',a,v) for a,v in (('Q6',5),('Q7',5),('Q8',5),('Q9',5),('Q10',5),('Q11',5),('Q12',5),('Q13',5),('W06',20),('W07',20),('W08',20),('W09',20),('W10',20),('W11',20),('W12',20),('DA_PROJECT',100),('TEST2',100),('DEMO',100))]
  a,b=coursework_totals(base)[0],coursework_totals(extra)[0]
  self.assertEqual(a,b);self.assertEqual((b['quizzes']['earned'],b['assignments']['earned']),(15,40))
 def test_only_graded_receipts_add_marks_and_unresolved_are_listed(self):
  cur=marks('S1',[5,5,5,5,5],[20,20,20,20,20])
  cur[1]=graded('S1','Q2',None,status='QUIZ_SCORE_PENDING');cur[7]=graded('S1','W03',15,status='IDENTITY_CONFLICT')   # a stray score on a held receipt must not count
  r=coursework_totals(cur)[0]
  self.assertEqual(r['quizzes']['earned'],20);self.assertEqual(r['quizzes']['unresolved'],['Q2']);self.assertEqual(r['quizzes']['missing'],[])
  self.assertEqual(r['assignments']['earned'],80);self.assertEqual(r['assignments']['unresolved'],['W03'])
 def test_missing_is_not_unresolved(self):
  r=coursework_totals(marks('S1',[5,5],[20]))[0]
  self.assertEqual(r['quizzes']['missing'],['Q3','Q4','Q5']);self.assertEqual(r['quizzes']['unresolved'],[]);self.assertEqual(r['assignments']['missing'],['W02','W03','W04','W05'])
 def test_students_are_kept_apart_by_cohort_and_id(self):
  rows=coursework_totals(full('S1')+marks('S1',[1],[],None,'CML3112')+marks('S2',[5]))
  self.assertEqual([(r['cohort'],r['student_id'],r['quizzes']['earned']) for r in rows],[('CML3111','S1',25),('CML3111','S2',5),('CML3112','S1',1)])

class ScheduleTests(unittest.TestCase):
 """Dates and sittings are scheduling facts recorded in the 3 November file (the policy of 10 November changes marks, not dates)."""
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
   # 13 November 2026: one confirmed online window for all cohorts replaces the proposed per-cohort sittings
   self.assertNotIn('proposed_closes_at',m);self.assertNotIn('proposed_sitting',m);self.assertNotIn('proposed_status',m);self.assertEqual((m['window']['opens_at'],m['window']['closes_at'],m['window']['duration_minutes']),('2026-11-23T00:00:00+03:00','2026-11-25T23:59:00+03:00',180));self.assertIn('confirmed',m['window_status'])
   self.assertEqual(m['grading'],'automatic');self.assertEqual(m['formats'],['ipynb']);self.assertNotIn('take-home',m['delivery_note'].lower().replace('no take-home',''))
   self.assertEqual(m['rehearsal_released_after_class_3'],{'CML3112':'2026-11-17','CML3113':'2026-11-20','CML3111':'2026-11-20'}[code])
 def test_grades_template_has_no_practical_test_2_column(self):
  head=(Path(__file__).resolve().parents[1]/'IUEA_Teaching_Plan/grader/Grades_template.csv').read_text().splitlines()[0].split(',')
  self.assertNotIn('Practical Test 2',head);self.assertIn('Practical Test 1',head)
class SemesterTotalsTests(unittest.TestCase):
 """Policy of 10 November 2026: 20 + 20 + 20 + 40; project = Part A /30 + Part B /15 scaled to 40; provisional x of 60 until both parts are marked."""
 def test_nothing_submitted_is_zero_and_pending(self):
  r=semester_totals([],students=[('CML3112','NOBODY')])[0]
  self.assertEqual((r['cohort'],r['student_id']),('CML3112','NOBODY'));self.assertIsNone(r['final']);self.assertEqual(r['project_status'],'Project: PENDING')
  self.assertEqual((r['provisional']['marks'],r['provisional']['percent']),(0,0));self.assertEqual(r['provisional']['text'],'Semester 1 provisional: 0.00 of 60 marks, 0.00 percent')
  self.assertEqual((r['assignments']['weighted'],r['quizzes']['weighted'],r['practical_test_1']['weighted']),(0,0,0));self.assertIsNone(r['practical_test_1']['mark'])
  self.assertEqual(r['missing'],['W01','W02','W03','W04','W05','Q1','Q2','Q3','Q4','Q5','TEST1']);self.assertEqual(r['unresolved'],[])
  self.assertNotIn('ML_PROJECT',' '.join(r['missing']))   # pending is not missing
  # once the project is marked 0 and 0 the same student has a final of 0
  done=semester_totals([graded('NOBODY','ML_PROJECT',0,cohort='CML3112',part_scores={'A':0,'B':0})])[0];self.assertEqual(done['final'],0.0)
 def test_all_full_marks_are_sixty_provisional_and_a_hundred_with_the_project(self):
  r=semester_totals(full('S1'))[0]
  self.assertIsNone(r['final']);self.assertEqual(r['project_status'],'Project: PENDING');self.assertTrue(r['project']['pending'])
  self.assertEqual((r['provisional']['marks'],r['provisional']['out_of'],r['provisional']['percent']),(60,60,100))
  self.assertEqual(r['provisional']['text'],'Semester 1 provisional: 60.00 of 60 marks, 100.00 percent');self.assertEqual(r['missing'],[]);self.assertEqual(r['unresolved'],[])
  r=semester_totals(full('S1')+[graded('S1','ML_PROJECT',45,part_scores={'A':30,'B':15})])[0]
  self.assertEqual(r['final'],100.0);self.assertEqual(r['project']['weighted'],40.0);self.assertEqual(r['project_status'],'Project: marked');self.assertFalse(r['project']['pending'])
 def test_mixed_marks_by_hand(self):
  # assignments 20+10+0+15+5 = 50 of 100 -> 10.00; quizzes 5+4+3+2+1 = 15 of 25 -> 12.00; Test 1 65 -> 13.00
  cur=marks('S1',[5,4,3,2,1],[20,10,0,15,5],65)
  r=semester_totals(cur)[0]
  self.assertEqual((r['assignments']['weighted'],r['quizzes']['weighted'],r['practical_test_1']['weighted']),(10.0,12.0,13.0))
  self.assertEqual(r['provisional']['marks'],35.0);self.assertEqual(r['provisional']['percent'],58.33);self.assertEqual(r['provisional']['text'],'Semester 1 provisional: 35.00 of 60 marks, 58.33 percent')
  # project Part A 24 + Part B 9 = 33 of 45 -> 33 x 40 / 45 = 29.33; final = 35 + 29.33
  r=semester_totals(cur+[graded('S1','ML_PROJECT',33,part_scores={'A':24,'B':9})])[0]
  self.assertEqual(r['project']['weighted'],29.33);self.assertEqual(r['final'],64.33);self.assertEqual(r['final'],round2(r['provisional']['marks']+r['project']['weighted']))
 def test_project_with_one_part_marked_stays_pending(self):
  cur=marks('S1',[5]*5,[20]*5,65)+[graded('S1','ML_PROJECT',None,status='PART_MARKED',part_scores={'A':27,'B':None})]
  r=semester_totals(cur)[0]
  self.assertIsNone(r['final']);self.assertEqual(r['project_status'],'Project: PENDING');self.assertEqual((r['project']['part_a'],r['project']['part_b']),(27,None));self.assertEqual(r['project']['weighted'],0)
  self.assertEqual(r['provisional']['marks'],53.0);self.assertEqual(r['provisional']['text'],'Semester 1 provisional: 53.00 of 60 marks, 88.33 percent')   # 20 + 20 + 13
  self.assertEqual(r['provisional'],semester_totals(cur[:-1])[0]['provisional'])   # Part A alone changes nothing
  b_only=semester_totals([graded('S1','ML_PROJECT',None,status='PART_MARKED',part_scores={'A':None,'B':12})])[0]
  self.assertIsNone(b_only['final']);self.assertEqual(b_only['project_status'],'Project: PENDING')
 def test_a_held_receipt_cannot_leak_project_marks_in(self):
  cur=full('S1')+[graded('S1','ML_PROJECT',None,status='IDENTITY_CONFLICT',part_scores={'A':30,'B':15})]
  r=semester_totals(cur)[0];self.assertIsNone(r['final']);self.assertIsNone(r['project']['part_a'])
 def test_typed_zero_parts_are_a_mark_of_zero_not_pending(self):
  r=semester_totals(full('S1')+[graded('S1','ML_PROJECT',0,part_scores={'A':0,'B':0})])[0];self.assertEqual(r['final'],60.0);self.assertFalse(r['project']['pending'])
 def test_uncounted_items_are_present_but_ignored(self):
  noise=[graded('S1',a,v) for a,v in (('Q6',5),('Q7',5),('Q8',5),('Q9',5),('Q10',5),('Q11',5),('W06',20),('W07',20),('W08',20),('W09',20),('W10',20),('W11',20),('W12',20),('DA_PROJECT',100),('TEST2',100),('DEMO',100))]
  r=semester_totals(noise)[0]
  self.assertEqual(r['provisional']['marks'],0);self.assertEqual(r['quizzes']['earned'],0);self.assertEqual(r['assignments']['earned'],0);self.assertEqual(r['missing'],['W01','W02','W03','W04','W05','Q1','Q2','Q3','Q4','Q5','TEST1'])
  both=semester_totals(full('S1')+noise)[0];self.assertEqual(both['provisional']['marks'],60);self.assertIsNone(both['final'])
  self.assertEqual(both,semester_totals(full('S1'))[0])
 def test_non_graded_counted_items_are_reported_as_unresolved_and_score_zero(self):
  cur=full('S1')
  cur=[x for x in cur if x['assessment'] not in ('Q2','W04','TEST1')]
  cur+=[graded('S1','Q2',None,status='QUIZ_SCORE_PENDING'),graded('S1','W04',None,status='AWAITING_GRADING'),graded('S1','TEST1',None,status='EQUAL_TIME_CONFLICT')]
  r=semester_totals(cur)[0]
  self.assertEqual(r['unresolved'],['W04','Q2','TEST1']);self.assertEqual(r['missing'],[])
  self.assertEqual((r['assignments']['weighted'],r['quizzes']['weighted'],r['practical_test_1']['weighted']),(16.0,16.0,0.0))   # 80/100, 20/25, no test
  self.assertEqual(r['provisional']['marks'],32.0);self.assertIsNone(r['practical_test_1']['mark'])
  # an unresolved item on one student does not touch another
  other=semester_totals(cur+full('S2'))
  self.assertEqual([x['unresolved'] for x in other],[['W04','Q2','TEST1'],[]])
 def test_unresolved_is_also_a_column_in_the_csv(self):
  import csv as _csv
  rows=semester_totals(marks('S1',[5,5,5,5],[20]*5,100)+[graded('S1','Q5',None,status='AWAITING_GRADING')])
  with tempfile.TemporaryDirectory() as d:
   write_totals_csv(rows,Path(d)/'t.csv');out=list(_csv.DictReader(open(Path(d)/'t.csv')))
  self.assertEqual(out[0]['unresolved'],'Q5');self.assertEqual(out[0]['missing'],'');self.assertEqual(out[0]['provisional_marks'],'56.0')
 def test_rounding_halves_go_up_each_part_and_the_rounded_sum(self):
  self.assertEqual(round2(8.625),8.63);self.assertEqual(round2(8.624),8.62);self.assertEqual(round2(0),0);self.assertEqual(round2(15),15)
  # assignments 43.125 of 100 -> 43.125 x 20 / 100 = 8.625 -> 8.63 (Python round() would give 8.62)
  r=semester_totals([graded('S1','W01',20),graded('S1','W02',20),graded('S1','W03',3.125)])[0]
  self.assertEqual(r['assignments']['weighted'],8.63)
  # Part A 1 + Part B 0 = 1 of 45 -> 40/45 = 0.888.. -> 0.89
  p=semester_totals([graded('S2','ML_PROJECT',1,part_scores={'A':1,'B':0})])[0];self.assertEqual(p['project']['weighted'],0.89);self.assertEqual(p['final'],0.89)
  # the total is the rounded sum of the rounded parts
  cur=[graded('S3','W01',20),graded('S3','W02',20),graded('S3','W03',3.125),graded('S3','Q1',1),graded('S3','TEST1',33)]   # 8.63 + 0.80 + 6.60
  r=semester_totals(cur)[0];self.assertEqual((r['assignments']['weighted'],r['quizzes']['weighted'],r['practical_test_1']['weighted']),(8.63,0.8,6.6));self.assertEqual(r['provisional']['marks'],16.03)
 def test_totals_csv_has_blank_final_while_pending(self):
  import csv as _csv
  rows=semester_totals(full('S1')+full('S2')+[graded('S2','ML_PROJECT',45,part_scores={'A':30,'B':15})])
  with tempfile.TemporaryDirectory() as d:
   write_totals_csv(rows,Path(d)/'t.csv');out={o['student_id']:o for o in _csv.DictReader(open(Path(d)/'t.csv'))}
  self.assertEqual(tuple(next(iter(out.values())).keys()),TOTALS_COLUMNS);self.assertNotIn('data_analysis_project_weighted',TOTALS_COLUMNS)
  self.assertEqual((out['S1']['final_percent'],out['S1']['project_status']),('','Project: PENDING'))
  self.assertEqual((out['S2']['final_percent'],out['S2']['project_status']),('100.0','Project: marked'))
  self.assertEqual((out['S1']['provisional_marks'],out['S1']['provisional_out_of']),('60.0','60'))
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
   self.assertEqual(r['project_status'],'Project: marked');self.assertEqual(b['current'][0]['score'],33.5);self.assertEqual(r['project']['weighted'],29.78)
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
     current=full('S1'))))
   cmd=[sys.executable,'-I','-B',str(Path(__file__).resolve().parents[1]/'IUEA_Teaching_Plan/grader/continuous_assessment.py'),'--from-ledger',str(led),'--totals-out',str(Path(d)/'t.csv')]
   r=subprocess.run(cmd,capture_output=True,text=True);self.assertEqual(r.returncode,0,r.stderr)
   out={o['student_id']:o for o in _csv.DictReader(open(Path(d)/'t.csv'))}
   self.assertEqual(out['S1']['provisional_marks'],'60.0');self.assertEqual(out['S1']['final_percent'],'');self.assertEqual(out['S1']['project_status'],'Project: PENDING')
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
