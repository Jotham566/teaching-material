import csv,json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];G=ROOT/'IUEA_Teaching_Plan/grader';sys.path.insert(0,str(G))
import artifact_grade as grader
class ArtifactCacheChecks(unittest.TestCase):
 def test_runtime_and_staging_path_do_not_regrade_but_marks_do(self):
  with tempfile.TemporaryDirectory() as folder:
   d=Path(folder);submission=d/'answer.md';submission.write_text('Synthetic answer')
   manifest=d/'manifest.csv'
   with manifest.open('w') as f:
    w=csv.DictWriter(f,fieldnames=['student_id','file']);w.writeheader();w.writerow(dict(student_id='S12345',file=str(submission)))
   marks=d/'marks.csv';out=d/'out'
   row=dict(student_id='S12345',notebook='/tmp/first.ipynb',seconds=1,status='OK',notebook_total=14,max_total=14,q1_marks=2)
   def save():
    with marks.open('w') as f:
     w=csv.DictWriter(f,fieldnames=list(row));w.writeheader();w.writerow(row)
   args=['artifact_grade.py','--submissions',str(manifest),'--rubric',str(G/'rubrics/W02.json'),'--model','qwen3:4b','--calibration-report',str(d/'calibration.json'),'--deterministic-results',str(marks),'--out',str(out)]
   with patch.object(sys,'argv',args),patch.object(grader,'local_model_identity',return_value={'digest':'fixture'}),patch.object(grader,'validate_calibration',return_value='fixture'),patch.object(grader,'grade_packet',side_effect=lambda *a:dict(status='AUTO_SCORED',score=6,maximum=6)) as infer:
    save();grader.main()
    row.update(notebook='/tmp/second.ipynb',seconds=9);save();grader.main();self.assertEqual(infer.call_count,1)
    row.update(notebook_total=13,q1_marks=1);save();grader.main();self.assertEqual(infer.call_count,2)
   self.assertEqual(json.loads((out/'S12345.json').read_text())['score'],19)
