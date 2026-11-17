"""Grade Test 1 notebooks that the collection system rejected (proposals only).

Same pipeline as the 10 Nov 2026 Test 1 re-run: batch_grade.grade_one ->
isolated_grading.evaluate -> test1_fairness (original grader first, then the
fairness run, per question the higher). Student code runs only in the Docker
sandbox (iuea-notebooks:2026.09, --network=none). Writes nothing except the
JSON-lines output file given on the command line.

Usage:
  python grade_collection_errors.py JOBS.json OUT.jsonl
JOBS.json: [{"path": ..., "cohort": "CML3113", "variant": "A", "tag": ...}, ...]
"""
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from batch_grade import grade_one  # noqa: E402
from test1_coding_contracts import hidden_spec_source  # noqa: E402

BANK = HERE.parent / 'assessment_banks' / 'TEST1'


def grade(job):
    with tempfile.TemporaryDirectory() as tmp:
        nb = Path(tmp) / 'submission_TEST1.ipynb'
        shutil.copyfile(job['path'], nb)
        hidden = Path(tmp) / 'test1_current_hidden.py'
        hidden.write_text(hidden_spec_source())
        try:
            res = grade_one(str(nb), str(HERE / 'specs' / 'spec_TEST1.py'), str(hidden), 'TEST1',
                            job['cohort'], str(BANK / job['cohort'] / job['variant']), 20, 180, None)
        except Exception as exc:  # noqa: BLE001
            res = {'status': 'EXC', 'error': repr(exc)}
    q = res.get('questions', {})
    return dict(job, status=res.get('status'),
                questions={k: v['awarded'] for k, v in q.items()},
                marks={k: v.get('marks') for k, v in q.items()},
                msgs={k: v.get('msg') for k, v in q.items()},
                cell_errors=res.get('cell_errors'), fairness=res.get('fairness'),
                error=res.get('error') or res.get('stdout_tail'))


def main(jobs_path, out_path):
    jobs = json.loads(Path(jobs_path).read_text())
    with open(out_path, 'w') as fh:
        for job in jobs:
            r = grade(job)
            fh.write(json.dumps(r, default=str) + '\n')
            fh.flush()
            print(job.get('tag'), r['status'], round(sum(r['questions'].values()), 2), flush=True)


if __name__ == '__main__':
    os.environ.setdefault('IUEA_TEST1_FAIRNESS', '1')
    main(sys.argv[1], sys.argv[2])
