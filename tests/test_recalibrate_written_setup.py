import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'IUEA_Teaching_Plan/grader'))
import recalibrate_written_setup as setup

class ActivationTests(unittest.TestCase):
    def test_both_must_pass_before_either_report_is_replaced(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);reports={};candidates={}
            for label in ('A1','A2'):
                target=root/(label+'active.json');target.write_text('old')
                Path(str(target)+'.complete.json').write_text('old-marker')
                rubric=root/(label+'rubric.json');rubric.write_text('{}')
                candidate=root/(label+'candidate.json');candidate.write_text('new')
                Path(str(candidate)+'.complete.json').write_text('new-marker')
                reports[label]=(target,rubric);candidates[label]=candidate
            with patch.object(setup,'model_for_report',return_value='model'), \
                 patch.object(setup,'profile_for_report',return_value='standard'), \
                 patch.object(setup.artifact_grade,'local_model_identity',return_value={}), \
                 patch.object(setup.artifact_grade,'validate_calibration',side_effect=[None,ValueError('failed A2')]):
                with self.assertRaisesRegex(ValueError,'failed A2'):setup.activate(candidates,reports)
            self.assertTrue(all(p.read_text()=='old' for p,_ in reports.values()))
            with patch.object(setup,'model_for_report',return_value='model'), \
                 patch.object(setup,'profile_for_report',return_value='standard'), \
                 patch.object(setup.artifact_grade,'local_model_identity',return_value={}), \
                 patch.object(setup.artifact_grade,'validate_calibration'):
                setup.activate(candidates,reports)
            self.assertTrue(all(p.read_text()=='new' for p,_ in reports.values()))
            self.assertEqual((root/'previous_reports/A1.json').read_text(),'old')
            self.assertEqual((root/'previous_reports/A2.json.complete.json').read_text(),'old-marker')

if __name__=='__main__':unittest.main()
