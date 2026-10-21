import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from reconcile_ca_sources import reconcile


class ReconciliationTests(unittest.TestCase):
    def test_matching_receipt_keeps_recorded_score_and_no_duplicate(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            audit=root/'audit'; forms=root/'forms'
            audit.mkdir(); forms.mkdir()
            sheet=dict(exported_at='test',source_sha256='fixture',quizzes=[dict(key='CML3111|1',
                items=[dict(id='recorded-total',points=5)],records=[dict(
                    response_id='sheet:row2',email='demo@example.com',submitted_at='2026-10-01T11:00:00+03:00',
                    answers=[dict(id='recorded-total',title='score',answer='',score=0),
                             dict(id='identity',title='Student Registration Number',answer='DEMO-1')])])])
            raw=dict(exported_at='test',quizzes=[dict(key='CML3111|1',
                items=[dict(id='old',points=5)],records=[dict(
                    response_id='forms-real-id',email='demo@example.com',submitted_at='2026-10-01T08:00:00.123Z',
                    answers=[dict(id='old',title='question',answer='old answer',score=None),
                             dict(id='identity',title='Student Registration Number',answer='DEMO-1')])])])
            for folder,payload in ((audit,sheet),(forms,raw)):
                (folder/'CML3111_Q1_quiz.json').write_text(json.dumps(payload))
            self.assertEqual(reconcile(audit,forms,root/'out',{'CML3111|1':{'closeAt':1790900000000}}),[])
            result=json.loads((root/'out/CML3111_Q1_quiz.json').read_text())['quizzes'][0]['records']
            self.assertEqual(len(result),1)
            self.assertEqual(result[0]['response_id'],'forms-real-id')
            self.assertEqual(result[0]['answers'][-1]['score'],0)
            self.assertEqual(result[0]['sheet_receipt'],'sheet:row2')


if __name__=='__main__':unittest.main()
