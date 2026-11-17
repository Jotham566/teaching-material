"""Scripted protocol regressions, not observed model behaviour. No account or external action."""
import json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import read_only_agent as agent
EVIDENCE=Path(__file__).resolve().parents[1]/"02 Data and Retrieval"
class ProtocolTests(unittest.TestCase):
    def run_fake(self,replies):
        with patch.object(agent,"ask_model",side_effect=[(x,"") for x in replies]) as model:
            result=agent.run(EVIDENCE,"Fictional protocol test",cli="scripted-test")
            return result,model.call_count
    def test_bad_json_after_lookup_is_held(self):
        r,c=self.run_fake([json.dumps(dict(action="lookup",contract_id="CONTRACT-01",clause="KT-1")),'{"action":"answer","text":"bad "quote""}'])
        self.assertEqual(r["lookup_calls"],1)
        self.assertEqual(r["trace"][-1]["host_decision"],"HELD: malformed structured operation")
        self.assertEqual(c,2)
        self.assertEqual(r["external_actions"],0)
    def test_ungrounded_answer_is_held(self):
        r,c=self.run_fake([json.dumps(dict(action="answer",text="unsupported"))])
        self.assertEqual(r["lookup_calls"],0)
        self.assertIn("HELD",r["trace"][-1]["host_decision"])
    def test_valid_escaped_string_is_preserved(self):
        value=dict(action="ask",text='Please supply the "signed" schedule.')
        self.assertEqual(agent.decode(json.dumps(value)),value)
if __name__=="__main__":unittest.main()
