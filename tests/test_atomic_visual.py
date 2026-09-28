import io,json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import Mock,patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'IUEA_Teaching_Plan/grader'))
import atomic_visual_grade as grader

class AtomicVisualChecks(unittest.TestCase):
 def evaluate(self,decisions):
  calls=[]
  def open_request(request,**kwargs):
   body=json.loads(request.data);calls.append(body)
   return io.BytesIO(json.dumps({'message':{'content':json.dumps({'met':decisions[len(calls)-1],'evidence':'Visible fixture evidence'})}}).encode())
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'render.png';p.write_bytes(b'fixture')
   with patch.object(grader,'local_model_identity',return_value={'digest':'fixture'}),patch.object(grader.LOCAL_HTTP,'open',side_effect=open_request):result=grader.evaluate(p)
  return result,calls
 def test_independent_ids_and_reversed_review(self):
  result,calls=self.evaluate([True,False,True,True,True,True,False,True])
  self.assertEqual(result['score'],3);self.assertEqual(result['status'],'AUTO_SCORED');self.assertEqual(len(calls),8)
  self.assertEqual(calls[0]['messages'][1]['content'],calls[-1]['messages'][1]['content'])
  self.assertTrue(all('images' in c['messages'][1] and c['think'] is False for c in calls))
 def test_disagreement_leaves_mark_blank(self):
  result,_=self.evaluate([True,False,True,True,True,True,True,True])
  self.assertEqual(result['status'],'EXCEPTION');self.assertIsNone(result['score'])
 def test_non_boolean_decision_is_rejected(self):
  with self.assertRaisesRegex(ValueError,'Invalid visual'):self.evaluate(['true']*8)

if __name__=='__main__':unittest.main()
