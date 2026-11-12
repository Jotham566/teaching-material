"""Tests for grader/final_marks_export.py with synthetic students (no real data): the 10 November 2026 policy."""
import json,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'IUEA_Teaching_Plan'/'grader'))
import final_marks_export as fx

def rec(cohort,sid,assessment,score,status='GRADED',name=''):
 return dict(cohort=cohort,assessment=assessment,student_id=sid,score=score,status=status,full_name=name,email='')

def ledger(current,students):
 return dict(updated_at='2026-11-07T00:00:00+00:00',students=students,current=current,attempts=[],identity_review=[])

def student(cohort,sid,name='',email='x@example.com'):
 return dict(cohort=cohort,student_id=sid,full_name=name,email=email)

class Policy(unittest.TestCase):
 def setUp(self):self.p=fx.load_policy()
 def test_weights_total_100(self):
  self.assertEqual(self.p['weights'],dict(assignments=20,quizzes=20,practical_test_1=20,engineering_ml_project=40))
  self.assertEqual(sum(self.p['weights'].values()),100)
  self.assertEqual(self.p['provisional']['out_of'],60)
 def test_counted_items(self):
  c=self.p['counted']
  self.assertEqual(c['assignments']['ledger_ids'],['W01','W02','W03','W04','W05'])
  self.assertEqual(c['quizzes']['ledger_ids'],['Q1','Q2','Q3','Q4','Q5'])
  self.assertEqual(c['engineering_ml_project']['raw_max'],45)

class Compute(unittest.TestCase):
 def setUp(self):self.p=fx.load_policy()
 def one(self,current,sid='S1',name='Ada'):
  L=ledger(current,[student('CML3112',sid,name)])
  return fx.compute(L,self.p)[0]
 def test_full_marks_is_sixty_without_project(self):
  cur=[rec('CML3112','S1',i,20) for i in ('W01','W02','W03','W04','W05')]+[rec('CML3112','S1',i,5) for i in ('Q1','Q2','Q3','Q4','Q5')]+[rec('CML3112','S1','TEST1',100)]
  r=self.one(cur);self.assertEqual((r['assignment'],r['quiz'],r['test'],r['project'],r['final']),(20,20,20,None,60))
 def test_nothing_submitted_is_zero(self):
  r=self.one([]);self.assertEqual((r['assignment'],r['quiz'],r['test'],r['final']),(0,0,0,0))
 def test_all_five_count_equally_no_best_three(self):
  cur=[rec('CML3112','S1','W01',20),rec('CML3112','S1','W02',20),rec('CML3112','S1','W03',20)]  # three full, two missing
  self.assertEqual(self.one(cur)['assignment'],12)  # 60 / 5, not 20
 def test_quizzes_each_worth_four(self):
  cur=[rec('CML3112','S1','Q1',5),rec('CML3112','S1','Q2',2.5)]
  self.assertEqual(self.one(cur)['quiz'],6)  # (5 + 2.5) * 4 / 5
 def test_later_items_are_ignored(self):
  cur=[rec('CML3112','S1',i,5) for i in ('Q6','Q8','Q9','Q10','Q11')]+[rec('CML3112','S1',i,20) for i in ('W06','W08','W09','W10','W11','W12')]+[rec('CML3112','S1','DA_PROJECT',100)]
  r=self.one(cur);self.assertEqual((r['assignment'],r['quiz'],r['final']),(0,0,0))
 def test_test_scaled_to_twenty_with_halves_up(self):
  self.assertEqual(self.one([rec('CML3112','S1','TEST1',67)])['test'],13)
  self.assertEqual(self.one([rec('CML3112','S1','TEST1',0.25)])['test'],0)
 def test_unmarked_receipt_scores_zero_and_is_listed(self):
  cur=[rec('CML3112','S1','W01',None,'WRITTEN_REVIEW'),rec('CML3112','S1','W02',20)]
  r=self.one(cur);self.assertEqual(r['assignment'],4);self.assertEqual(r['unresolved'],[('W01','WRITTEN_REVIEW')])
 def test_project_scaled_to_forty_and_needs_both_parts(self):
  L=ledger([],[student('CML3112','S1','Ada')])
  both=fx.compute(L,self.p,{'S1':dict(A=30,B=15)})[0];self.assertEqual((both['project'],both['final']),(40,40))
  half=fx.compute(L,self.p,{'S1':dict(A=24,B=None)})[0];self.assertIsNone(half['project'])
  mid=fx.compute(L,self.p,{'S1':dict(A=18,B=9)})[0];self.assertEqual(mid['project'],24)  # 27 of 45 -> 24 of 40
 def test_name_filled_from_a_receipt_and_placeholder_rejected(self):
  L=ledger([rec('CML3112','S1','Q1',5,name='Real Name')],[student('CML3112','S1','No name extracted')])
  self.assertEqual(fx.compute(L,self.p)[0]['name'],'Real Name')

class Overrides(unittest.TestCase):
 def test_override_replaces_a_mark_and_clears_unresolved(self):
  p=fx.load_policy()
  L=ledger([rec('CML3112','S1','W01',None,'WRITTEN_REVIEW'),rec('CML3112','S1','W02',10)],[student('CML3112','S1','Ada')])
  base=fx.compute(L,p)[0];self.assertEqual((base['assignment'],base['unresolved']),(2,[('W01','WRITTEN_REVIEW')]))
  r=fx.compute(L,p,overrides={('CML3112','S1','W01'):16,('CML3112','S1','W02'):12})[0]
  self.assertEqual((r['assignment'],r['unresolved']),(6,[]))  # (16 + 12) / 5
 def test_load_overrides_reads_csv(self):
  with tempfile.TemporaryDirectory() as d:
   f=Path(d)/'o.csv';f.write_text('cohort,reg_number,assessment,mark,original,source\nCML3112,S1,W01,16,,x\n')
   self.assertEqual(fx.load_overrides(f),{('CML3112','S1','W01'):16.0})

class Workbook(unittest.TestCase):
 def test_workbook_columns_and_formula(self):
  from openpyxl import load_workbook
  p=fx.load_policy()
  L=ledger([rec('CML3111','S1','TEST1',50)],[student('CML3111','S1','Ada','a@example.com'),student('CML3113','S2','Bob','b@example.com')])
  rows=fx.compute(L,p)
  with tempfile.TemporaryDirectory() as d:
   path=Path(d)/'m.xlsx';fx.write_workbook(rows,p,path,'stamp','src')
   wb=load_workbook(path)
   self.assertEqual(wb.sheetnames,['Read me','CML3111','CML3112','CML3113','Why these marks'])
   ws=wb['CML3111']
   self.assertEqual([c.value for c in ws[4]],['Reg Number','Name','Email','Program','Assignment /20','Quiz /20','Test Practical /20','Project /40','Final Mark /100'])
   self.assertEqual([c.value for c in ws[5]][:7],['S1','Ada','a@example.com','CML3111',0,0,10])
   self.assertEqual(ws['I5'].value,'=ROUND(SUM(E5:H5),0)')

class AgreesWithContinuousAssessment(unittest.TestCase):
 def test_export_matches_semester_totals_on_random_students(self):
  import random,continuous_assessment as ca
  rnd=random.Random(20261110);p=fx.load_policy();cur=[];studs=[]
  for n in range(120):
   sid=f'R{n}';studs.append(student('CML3111',sid,f'S{n}'))
   for i in ('W01','W02','W03','W04','W05'):
    if rnd.random()<0.8:cur.append(rec('CML3111',sid,i,rnd.choice([0,5,12.5,20])))
   for i in ('Q1','Q2','Q3','Q4','Q5'):
    if rnd.random()<0.8:cur.append(rec('CML3111',sid,i,rnd.choice([0,1,2.5,5])))
   if rnd.random()<0.9:cur.append(rec('CML3111',sid,'TEST1',rnd.choice([0,33,66.7,100])))
   for i in ('Q6','Q8','W06','W08','DA_PROJECT'):cur.append(rec('CML3111',sid,i,rnd.choice([0,5,20])))
  mine={r['reg']:r for r in fx.compute(ledger(cur,studs),p)}
  py={r['student_id']:r for r in ca.semester_totals(cur,students=[('CML3111',s['student_id']) for s in studs])}
  for sid,r in mine.items():
   t=py[sid]
   self.assertEqual(r['assignment'],fx.rnd(t['assignments']['weighted']))  # the export shows whole marks
   self.assertEqual(r['quiz'],fx.rnd(t['quizzes']['weighted']))
   self.assertEqual(r['test'],fx.rnd(t['practical_test_1']['weighted']))
   self.assertEqual(r['final'],r['assignment']+r['quiz']+r['test'])

if __name__=='__main__':unittest.main()
