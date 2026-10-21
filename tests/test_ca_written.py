import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'IUEA_Teaching_Plan/grader'))
import grade_ca_written as written
import prepare_ca_written as preparation
import run_ca_written_queue as queue


class WrittenTests(unittest.TestCase):
    def test_queue_replaces_receipt_without_double_counting(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            row=dict(response_id='r',cohort='CML3111',assessment='W02',
                     student_id='SYNTHETIC',score=None,status='PARTIAL_CODE_ONLY')
            (root/'code.json').write_text(json.dumps([row]))
            finished=dict(row,score=18,status='GRADED')
            (root/'written.json').write_text(json.dumps([finished]))
            self.assertEqual(queue.merged_results([root/'code.json',root/'written.json']),[finished])
            (root/'written.json').write_text(json.dumps([dict(finished,student_id='OTHER')]))
            with self.assertRaisesRegex(ValueError,'Conflicting result identities'):
                queue.merged_results([root/'code.json',root/'written.json'])

    def test_failed_calibration_prevents_student_inference(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(written,'model_for_report',return_value='local-fixture'), \
                 patch.object(written,'profile_for_report',return_value='standard'), \
                 patch.object(written.artifact_grade,'local_model_identity',return_value={}), \
                 patch.object(written.artifact_grade,'validate_calibration',side_effect=ValueError('Calibration failed')), \
                 patch.object(written.artifact_grade,'grade_packet') as infer:
                with self.assertRaisesRegex(ValueError,'Calibration failed'):
                    written.run(directory,'not-read','not-read','fixture','W01',directory,'not-read')
                infer.assert_not_called()

    def test_prepared_text_stays_linked_to_original_attachment(self):
        import hashlib
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);source=root/'source';(source/'files').mkdir(parents=True)
            document=source/'files/report.md'
            document.write_text('A synthetic report with enough text to test extraction and source integrity.')
            sha=hashlib.sha256(document.read_bytes()).hexdigest()
            (source/'manifest.json').write_text(json.dumps(dict(files=[
                dict(id='f',export_name='report.md',sha256=sha)])))
            ledger=root/'ledger.json'
            ledger.write_text(json.dumps(dict(current=[dict(response_id='r',assessment='W01',
                timing_status='ON_TIME',source='manifest.json',file_ids=['f'])])))
            preparation.prepare(source,ledger,root/'out')
            prepared=json.loads((root/'out/prepared.json').read_text())['r']
            self.assertFalse(prepared['errors'])
            self.assertEqual(prepared['files'][0]['source_sha256'],sha)
            self.assertEqual(hashlib.sha256(Path(prepared['files'][0]['path']).read_bytes()).hexdigest(),
                             prepared['files'][0]['text_sha256'])
            with patch.object(preparation.grading,'evaluator_fingerprint',return_value=prepared['extractor_fingerprint']), \
                 patch.object(preparation.grading,'extract',side_effect=AssertionError('Should reuse verified text')):
                preparation.prepare(source,ledger,root/'out')


if __name__=='__main__':unittest.main()
