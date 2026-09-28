import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'IUEA_Teaching_Plan/grader'))
from artifact_grade import validate_grade,validate_rubric,group_manifest,extract,validate_calibration
class RubricChecks(unittest.TestCase):
 def setUp(self):self.r={'id':'UNIT-r1','maximum':10,'criteria':[{'id':'a','maximum':10,'description':'Evidence'}]}
 def test_valid(self):self.assertEqual(validate_grade({'criteria':[{'id':'a','awarded':7,'evidence':'supported','feedback':'clear'}],'concerns':[]},self.r,'supported result'),7)
 def test_fabricated_evidence(self):
  with self.assertRaises(ValueError):validate_grade({'criteria':[{'id':'a','awarded':10,'evidence':'invented','feedback':'clear'}],'concerns':[]},self.r,'supported result')
 def test_out_of_range(self):
  with self.assertRaises(ValueError):validate_grade({'criteria':[{'id':'a','awarded':11,'evidence':'supported','feedback':'clear'}],'concerns':[]},self.r,'supported result')
 def test_binary_criterion_rejects_fractional_credit(self):
  self.r['criteria'][0]['binary']=True
  with self.assertRaises(ValueError):validate_grade({'criteria':[{'id':'a','awarded':7,'evidence':'supported','feedback':'clear'}],'concerns':[]},self.r,'supported result')
  self.assertEqual(validate_grade({'criteria':[{'id':'a','awarded':10,'evidence':'supported','feedback':'clear'}],'concerns':[]},self.r,'supported result'),10)
 def test_all_rubrics(self):
  import json
  for p in (Path(__file__).resolve().parents[1]/'IUEA_Teaching_Plan/grader/rubrics').glob('*.json'):validate_rubric(json.loads(p.read_text()))
 def test_packet_preserves_one_response(self):
  rows=[dict(student_id='S12345',file=f,response_id='response-a') for f in ['report.docx','slides.pptx']]
  self.assertEqual(len(group_manifest(rows)['S12345']),2)
  rows[1]['response_id']='response-b'
  with self.assertRaises(ValueError):group_manifest(rows)
 def test_supplied_notebook_prompt_is_not_answer_evidence(self):
  import tempfile,json
  with tempfile.TemporaryDirectory() as tmp:
   path=Path(tmp)/'answer.ipynb'
   path.write_text(json.dumps({'cells':[{'cell_type':'markdown','source':['Question: Restart clears state and Run All gives 17.']},{'cell_type':'markdown','source':['My explanation: ...']}]}))
   extracted=extract(path,'W02')
   self.assertNotIn('Restart clears',extracted)
   self.assertIn('My explanation',extracted)
 def test_failed_calibration_blocks_production(self):
  import tempfile,json
  with tempfile.TemporaryDirectory() as tmp:
   path=Path(tmp)/'report.json';path.write_text(json.dumps([{'case':str(i),'passed':False} for i in range(5)]))
   with self.assertRaises(ValueError):validate_calibration(path,self.r,{},'qwen3:4b')
 def test_later_starter_prompts_are_not_answer_evidence(self):
  import tempfile,json
  with tempfile.TemporaryDirectory() as tmp:
   path=Path(tmp)/'answer.ipynb'
   path.write_text(json.dumps({'cells':[
    {'cell_type':'markdown','source':'Explain why synthetic data cannot prove safety.'},
    {'cell_type':'code','source':'# I preserved raw data and verified every value.'},
    {'cell_type':'markdown','source':'## My written evidence\nMy own answer.'}]}))
   self.assertEqual(extract(path,'W06').strip(),'My own answer.')
 def test_current_evaluator_required(self):
  import tempfile,json,hashlib
  from artifact_grade import evaluator_fingerprint
  rows=[{'case':str(i),'passed':True,'result':dict(status='AUTO_SCORED',model='qwen3:4b',model_identity={},evaluator_sha256=evaluator_fingerprint(),rubric_sha256=hashlib.sha256(json.dumps(self.r,sort_keys=True).encode()).hexdigest())} for i in range(5)]
  with tempfile.TemporaryDirectory() as tmp:
   path=Path(tmp)/'report.json';path.write_text(json.dumps(rows))
   from calibration_record import complete
   with self.assertRaises(ValueError):validate_calibration(path,self.r,{},'qwen3:4b')
   complete(path,[str(i) for i in range(5)])
   self.assertTrue(validate_calibration(path,self.r,{},'qwen3:4b'))
   rows[0]['result']['evaluator_sha256']='outdated';path.write_text(json.dumps(rows))
   with self.assertRaises(ValueError):validate_calibration(path,self.r,{},'qwen3:4b')
 def test_stale_rubric_calibration_blocks_production(self):
  import tempfile,json
  with tempfile.TemporaryDirectory() as tmp:
   path=Path(tmp)/'report.json';path.write_text(json.dumps([{'case':str(i),'passed':True,'result':{'rubric_sha256':'old'}} for i in range(5)]))
   with self.assertRaises(ValueError):validate_calibration(path,self.r,{},'qwen3:4b')
if __name__=='__main__':unittest.main()
