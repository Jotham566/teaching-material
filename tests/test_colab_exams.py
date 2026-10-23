import json,sys,tempfile,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];G=ROOT/'IUEA_Teaching_Plan/grader';sys.path.insert(0,str(G))
from batch_grade import grade_one
from colab_exam_contracts import PARTS,decision_keys,assess
from engineering_contracts import DOMAINS
import engineering_pandas_reference as ref
class ExamTests(unittest.TestCase):
 def test_packets(self):
  for exam,parts in PARTS.items():
   self.assertEqual(sum(m for _,m in parts),100)
   for cohort in DOMAINS:
    for variant in 'ABC':
     folder=G.parent/'assessment_banks'/exam/cohort/variant
     nb=json.loads((folder/(exam+'_student.ipynb')).read_text());text='\n'.join(''.join(c['source']) for c in nb['cells'])
     self.assertNotIn('offline',text.lower());self.assertNotIn('My written evidence',text)
     self.assertEqual('DECISIONS' in text, exam=='TEST2');self.assertIn('Submit test',text);self.assertNotIn('File → Download',text)
     self.assertIn('autograde-skip',nb['cells'][-1]['metadata']['tags'])
     with zipfile.ZipFile(folder.parent.parent/f'{cohort}_{exam}_{variant}_student.zip') as z:self.assertEqual(set(z.namelist()),{exam+'_student.ipynb','engineering_data.csv','ASSIGNMENT_INSTRUCTIONS.txt'})
 def test_decisions_partial(self):
  class NS:
   def get(self,k,default=None):return {'D1':'B','D2':'C'}
  verdict=assess(NS(),'TEST1','decisions');self.assertAlmostEqual(verdict[2],2/6)
 def test_all_completed_packets_in_isolation(self):
  legacy_source=Path(ref.__file__).read_text()
  coding_source=(G/'test1_coding_reference.py').read_text()
  for exam in PARTS:
   source=coding_source if exam=='TEST1' else legacy_source
   for cohort in DOMAINS:
    for variant in 'ABC':
     folder=G.parent/'assessment_banks'/exam/cohort/variant
     nb=json.loads((folder/(exam+'_student.ipynb')).read_text())
     for c in nb['cells']:
      text=''.join(c['source'])
      if c['cell_type']!='code':continue
      if 'iuea-read-csv' in c.get('metadata',{}).get('tags',[]):c['source']='file_path = "engineering_data.csv"\nraw_data = pd.read_csv(file_path)\n'
      if 'STUDENT_ID =' in text:c['source']=text.replace('STUDENT_ID = ""','STUDENT_ID = "99/TEST/000/DEMO-X"')
      if 'raise NotImplementedError' in text or (exam=='TEST1' and text.startswith('def ')):c['source']=source
      if text.startswith('DECISIONS ='):c['source']='DECISIONS = '+repr(decision_keys()[exam])
     if exam=='TEST1':
      from test1_coding_reference import complete_notebook
      complete_notebook(nb)
     with tempfile.TemporaryDirectory() as tmp:
      path=Path(tmp)/('99_TEST_000_DEMO-X_'+exam+'.ipynb');path.write_text(json.dumps(nb))
      result=grade_one(str(path),str(G/'specs'/f'spec_{exam}.py'),str(G/'specs/hidden'/f'spec_{exam}_hidden.py'),exam,cohort,str(folder),20,180,None)
      self.assertEqual(result['status'],'OK',(exam,cohort,variant,result))
      self.assertEqual(sum(q['awarded'] for q in result['questions'].values()),100,(exam,cohort,variant,result))
      print(exam,cohort,variant,'100/100',flush=True)
 def test_blank_submission_cannot_score(self):
  folder=G.parent/'assessment_banks/TEST1/CML3111/A'
  result=grade_one(str(folder/'TEST1_student.ipynb'),str(G/'specs/spec_TEST1.py'),str(G/'specs/hidden/spec_TEST1_hidden.py'),'TEST1','CML3111',str(folder),15,90,None)
  self.assertEqual(sum(q['awarded'] for q in result['questions'].values()),0,result)
if __name__=='__main__':unittest.main()
