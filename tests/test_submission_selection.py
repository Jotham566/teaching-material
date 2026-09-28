import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'IUEA_Teaching_Plan/grader'))
from prepare_submissions import select,cohort_roster
from expand_team_grades import expand
class SelectionTests(unittest.TestCase):
 def row(self,at,id='a',status='ON_TIME'):
  return dict(assessment_key='CML3112|W02',student_id='S12345',email='learner@example.test',submitted_at=at,deadline='2026-09-22T08:00:00Z',status=status,file_ids='["file-id"]',response_id=id)
 def test_latest_on_time(self):
  rows=[self.row('2026-09-21T08:00:00Z'),self.row('2026-09-22T08:00:00Z','b'),self.row('2026-09-22T08:00:01Z','c')]
  got=select(rows,{'S12345':{'email':'learner@example.test','cohort':'CML3112'}},'CML3112|W02')
  self.assertEqual(got['S12345']['response_id'],'b')
 def test_identity_mismatch(self):
  with self.assertRaises(ValueError):select([self.row('2026-09-21T08:00:00Z')],{'S12345':{'email':'another@example.test','cohort':'CML3112'}},'CML3112|W02')
 def test_missing_roster_email(self):
  with self.assertRaisesRegex(ValueError,'Missing roster email'):
   select([self.row('2026-09-21T08:00:00Z')],{'S12345':{'email':' ','cohort':'CML3112'}},'CML3112|W02')
 def test_missing_cohort_is_rejected(self):
  with self.assertRaisesRegex(ValueError,'cohort'):
   select([self.row('2026-09-21T08:00:00Z')],{'S12345':{'email':'learner@example.test'}},'CML3112|W02')
 def test_missing_counts_are_scoped_to_the_assigned_cohort(self):
  roster={'A':{'cohort':'CML3112'},'B':{'cohort':'CML3112'},'C':{'cohort':'CML3113'},'D':{'cohort':'DA'}}
  self.assertEqual(set(cohort_roster(roster,'CML3112|W02'))-{'A'},{'B'})
  with self.assertRaises(ValueError):cohort_roster(roster,'CML3112|W99')
 def test_duplicate_team_member(self):
  with self.assertRaises(ValueError):expand([{'team_id':'T1','student_id':'S1'},{'team_id':'T2','student_id':'S1'}],[])
if __name__=='__main__':unittest.main()
