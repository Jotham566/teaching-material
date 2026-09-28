import io,json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
G=Path(__file__).resolve().parents[1]/'IUEA_Teaching_Plan/grader';sys.path.insert(0,str(G))
import artifact_grade as standard
from reasoned_artifact_grade import load_backend,ReasonedHTTP,REQUEST_TIMEOUT,PREDICTION_LIMIT
class ProfileChecks(unittest.TestCase):
 def test_reasoning_profile_reuses_checks_without_mutating_standard(self):
  rubric=dict(id='fixture-v1',maximum=1,criteria=[dict(id='reason',maximum=1,description='A valid reason',binary=True)])
  before=standard.evaluator_fingerprint(rubric);backend=load_backend();calls=[]
  class Transport:
   def open(self,req,timeout=None):
    url=req if isinstance(req,str) else req.full_url
    if url.endswith('/tags'):reply={'models':[{'name':'qwen3.5:4b','digest':'fixture'}]}
    elif url.endswith('/version'):reply={'version':'fixture'}
    else:
     body=json.loads(req.data);calls.append((body,timeout));reply={'message':{'content':json.dumps({'criteria':[dict(id='reason',awarded=1,evidence='Valid reasoning.',feedback='Meets criterion.')],'concerns':[]})}}
    return io.BytesIO(json.dumps(reply).encode())
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'answer.md';p.write_text('Valid reasoning. This explains the engineering decision in the submission.')
   with patch.object(backend,'LOCAL_HTTP',ReasonedHTTP(Transport())):result=backend.grade_packet([p],rubric,'ollama','qwen3.5:4b')
  self.assertEqual(result['score'],1);self.assertEqual(result['status'],'AUTO_SCORED');self.assertEqual(len(calls),2)
  for body,timeout in calls:
   self.assertTrue(body['think']);self.assertEqual(body['options']['num_predict'],PREDICTION_LIMIT);self.assertEqual(timeout,REQUEST_TIMEOUT)
  self.assertEqual(standard.evaluator_fingerprint(rubric),before)
  self.assertNotEqual(result['evaluator_sha256'],before)
 def test_standard_calibration_cannot_authorize_reasoning_profile(self):
  from calibration_record import complete
  import hashlib
  rubric=dict(id='fixture-v1',maximum=1,criteria=[dict(id='reason',maximum=1,description='A valid reason',binary=True)])
  rows=[dict(case=str(i),passed=True,result=dict(status='AUTO_SCORED',model='qwen3.5:4b',model_identity={},rubric_sha256=hashlib.sha256(json.dumps(rubric,sort_keys=True).encode()).hexdigest(),evaluator_sha256=standard.evaluator_fingerprint(rubric))) for i in range(5)]
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'report.json';p.write_text(json.dumps(rows));complete(p,[r['case'] for r in rows])
   with self.assertRaisesRegex(ValueError,'current extraction'):load_backend().validate_calibration(p,rubric,{},'qwen3.5:4b')
