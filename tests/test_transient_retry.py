import sys,unittest
from pathlib import Path
from unittest.mock import Mock
from urllib.error import URLError
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'IUEA_Teaching_Plan/grader'))
from transient_retry import run

class TransportRetryChecks(unittest.TestCase):
 def test_timeout_retries_complete_evaluation_once(self):
  for error in [TimeoutError('slow'),URLError(TimeoutError('slow'))]:
   operation=Mock(side_effect=[error,dict(status='AUTO_SCORED',score=4)])
   result=run(operation)
   self.assertEqual(result['score'],4);self.assertEqual(result['inference_attempts'],2)
   self.assertEqual(operation.call_count,2);self.assertTrue(result['prior_transport_timeouts'])
 def test_does_not_retry_disagreement_or_a_low_score(self):
  for result in [dict(status='EXCEPTION',score=None),dict(status='AUTO_SCORED',score=0)]:
   operation=Mock(return_value=result);self.assertEqual(run(operation)['score'],result['score']);operation.assert_called_once()
 def test_persistent_timeout_is_bounded(self):
  operation=Mock(side_effect=TimeoutError('slow'))
  with self.assertRaisesRegex(TimeoutError,'both attempts'):run(operation)
  self.assertEqual(operation.call_count,2)
 def test_other_errors_do_not_retry(self):
  for error in [ValueError('invalid evidence'),URLError('connection refused')]:
   operation=Mock(side_effect=error)
   with self.assertRaises(type(error)):run(operation)
   operation.assert_called_once()

if __name__=='__main__':unittest.main()
