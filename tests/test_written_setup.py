import hashlib
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'IUEA_Teaching_Plan/grader'))
from check_written_setup import differences

class WrittenSetupTests(unittest.TestCase):
    def test_identifies_server_version_without_claiming_model_changed(self):
        rubric={'id':'synthetic'}
        saved={'model':'local:4b','model_identity':{'digest':'same','ollama_version':'old'},
               'rubric_sha256':hashlib.sha256(json.dumps(rubric,sort_keys=True).encode()).hexdigest()}
        self.assertEqual(differences(saved,{'digest':'same','ollama_version':'new'},rubric,'local:4b'),
                         [('Ollama version','old','new')])
        self.assertEqual(differences(saved,saved['model_identity'],rubric,'local:4b'),[])

if __name__=='__main__':unittest.main()
