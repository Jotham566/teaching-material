import sys,unittest,json,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'IUEA_Teaching_Plan/grader'))
from continuous_assessment import choose_current,identity_conflicts,quiz_mark,build,field,norm,recover_quiz_ids,resolve_supported_typos,coursework_totals,BLOCKS,WAIVED_WEEKS,QUIZ_WEEKS,ASSIGNMENT_WEEKS

def receipt(**kwargs):
 r=dict(cohort='CML3111',student_id='DEMO-01',email='demo@example.com',assessment='W03',response_id='r1',submitted_at='2026-10-01T08:00:00Z',timing_status='ON_TIME',status='GRADED',score=15)
 r.update(kwargs);return r
class BlockCourseworkTests(unittest.TestCase):
 def rows(self,quiz,assign,sid='DEMO-01'):
  return [receipt(student_id=sid,assessment=a,score=v,response_id=f'{sid}-{a}') for a,v in {**quiz,**assign}.items()]
 def test_full_marks_give_ten_percent_each(self):
  q={f'Q{w}':5 for w in (1,2,3,4,5,8,9,10,11,12,13)};a={f'W{w:02}':20 for w in (1,2,3,4,5,8,9,10,11,12)}
  r=coursework_totals(self.rows(q,a))[0]
  self.assertEqual((r['quizzes']['available'],r['assignments']['available']),(45,160))
  self.assertEqual((r['quizzes']['weighted'],r['assignments']['weighted']),(10.0,10.0))
 def test_weekly_drops_two_lowest_of_five_and_blocks_are_never_dropped(self):
  q={'Q1':0,'Q2':5,'Q3':5,'Q4':5,'Q5':2,'Q8':5,'Q9':5,'Q10':5}
  r=coursework_totals(self.rows(q,{}))[0]['quizzes']
  self.assertEqual(r['earned'],15+15)   # best 3 of 5 weekly = 5+5+5; Block 1 = 15; Block 2 not sat = 0
  self.assertEqual(r['weighted'],round(30/45*10,2))
 def test_missing_block_part_scores_zero(self):
  a={'W08':20,'W09':20}
  r=coursework_totals(self.rows({},a))[0]['assignments']
  self.assertEqual(r['blocks'][0],dict(block='Block 1',earned=40,available=60,parts_submitted=2))
  self.assertEqual(r['blocks'][1]['earned'],0)
 def test_constants_match_policy_file(self):
  pol=json.loads((Path(__file__).resolve().parents[1]/'data/assessment_blocks_20261030.json').read_text())
  wk=lambda b:tuple(f'Q{q["week"]}' for q in b['quiz_forms'])
  self.assertEqual(BLOCKS['quizzes'],tuple((b['label'],wk(b)) for b in pol['blocks']))
  self.assertEqual(BLOCKS['assignments'],tuple((b['label'],tuple(p['id'] for p in b['assignment_parts'])) for b in pol['blocks']))
  self.assertEqual(pol['weights_percent']['quizzes'],10);self.assertEqual(WAIVED_WEEKS,(6,))
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
