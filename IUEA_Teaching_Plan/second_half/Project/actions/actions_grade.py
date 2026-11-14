"""Grade or check ONE collected notebook: fetch it from the collector, run it in the Docker sandbox, post the result back.

    python3 actions_grade.py --submission-id S-... [--collector-url URL] [--image iuea-notebooks:colab-2026.11] [--out DIR]

Run by .github/workflows/grade-ml-project.yml on every repository_dispatch from the collector, and by test_actions_e2e.py locally.
The collector URL and the shared secret come from the environment (COLLECTOR_URL, COLLECTOR_SECRET); nothing secret is printed.

Two things are computed, both inside the sandbox (no network, read-only inputs, the same limits as the lecturer's grader):
  1. What the student sees at once: runs from the top (or the first code cell that failed), required functions found, MEMO form found.
     This is the same runner as the notebook's "Check my notebook" cell, so the two always agree.
  2. The marks, with grade_project.py (the own-cell rules included), only for mode "grade" (collected at the deadline or on "I have finished").
     They are stored by the collector and shown only after the release switch. Mode "check" (Check my work, the rehearsal) never marks.
The collector sends the mode and whether the notebook is the issued file; ids are C-... (checks) or S-... (collections).
"""
import argparse
import csv
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
PLAN = PROJECT.parents[1]
sys.path.insert(0, str(PROJECT / 'tools'))
sys.path.insert(0, str(PROJECT / 'grader_spec'))
sys.path.insert(0, str(PLAN / 'grader'))
import pipeline_cells as PL  # noqa: E402
from registration import filename_id  # noqa: E402
sys.path.insert(0, str(PROJECT / 'grader_spec'))
from grade_project import restore_data_block  # noqa: E402

DEFAULT_IMAGE = 'iuea-notebooks:colab-2026.11'


def post(url, body, timeout=120):
    data = json.dumps(body).encode()
    request = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')
    with urllib.request.urlopen(request, timeout=timeout) as reply:       # Apps Script answers with a redirect; urllib follows it as a GET
        answer = json.loads(reply.read().decode())
    if not answer.get('ok'):
        raise RuntimeError('collector refused: ' + str(answer.get('error'))[:200])
    return answer['result']


def sandbox_check(notebook_path, image):
    """The Check my notebook runner, inside the sandbox. Returns its report (cells, failed, missing_functions, memo_found ...)."""
    work = Path(tempfile.mkdtemp(prefix='check_'))
    (work / 'runner.py').write_text(PL.RUNNER)
    (work / 'notebook.json').write_bytes(Path(notebook_path).read_bytes())
    args = json.dumps([PL.SKIP_MARKERS, PL.SELF_CHECK_MARKERS, PL.required_functions(), PL.memo_fields(), PL.CELL_TIMEOUT])
    cmd = ['docker', 'run', '--rm', '-i', '--network=none', '--read-only', '--cap-drop=ALL', '--security-opt=no-new-privileges',
           '--pids-limit=64', '--memory=1g', '--cpus=1', '--user=65534:65534', '--tmpfs=/tmp:rw,noexec,nosuid,size=128m',
           '--tmpfs=/work:rw,nosuid,size=256m,uid=65534,gid=65534', '--mount', f'type=bind,src={work},dst=/inputs,readonly',
           image, 'python', '/inputs/runner.py', '/inputs/notebook.json', args]
    try:
        done = subprocess.run(cmd, capture_output=True, text=True, timeout=PL.TOTAL_TIMEOUT + 60)
    except subprocess.TimeoutExpired:
        return dict(cells=0, failed=[dict(cell='?', first_line='', error='the notebook took more than %d minutes' % (PL.TOTAL_TIMEOUT // 60))],
                    missing_functions=PL.required_functions(), memo_found=False, memo_missing_fields=[])
    lines = [l for l in done.stdout.splitlines() if l.startswith('IUEA-REPORT ')]
    if not lines:
        raise RuntimeError('the sandbox check gave no report (exit %s)' % done.returncode)
    report = json.loads(lines[-1][len('IUEA-REPORT '):])
    report.pop('selfcheck_output', None)
    return report


def marks(notebook_path, registration, cohort, image, out):
    """grade_project.py on this one notebook. Returns (part_a, part_b, total, status, flags)."""
    folder = Path(tempfile.mkdtemp(prefix='one_')) / 'in'
    folder.mkdir()
    (folder / f'{filename_id(registration)}_ML_PROJECT.ipynb').write_bytes(Path(notebook_path).read_bytes())
    env = dict(os.environ, IUEA_NOTEBOOK_IMAGE=image)
    done = subprocess.run([sys.executable, str(PROJECT / 'grader_spec/grade_project.py'), '--folder', str(folder), '--cohort', cohort, '--out', str(out),
                           '--image', image], capture_output=True, text=True, env=env)
    results = Path(out) / 'ML_PROJECT_results.csv'
    if done.returncode or not results.exists():
        raise RuntimeError('grade_project.py failed: ' + (done.stderr or done.stdout)[-400:])
    row = next(csv.DictReader(results.open()))
    return float(row['part_a']), float(row['part_b']), float(row['project_total']), row['status'], row['flags']


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--submission-id', required=True)
    ap.add_argument('--collector-url', default=os.environ.get('COLLECTOR_URL', ''))
    ap.add_argument('--image', default=os.environ.get('IUEA_NOTEBOOK_IMAGE', DEFAULT_IMAGE))
    ap.add_argument('--out', default='')
    a = ap.parse_args(argv)
    import re
    if not re.fullmatch(r'[SC]-[a-f0-9]{20}', a.submission_id):
        raise SystemExit('The submission id must look like S- or C- followed by 20 hexadecimal characters.')
    secret = os.environ.get('COLLECTOR_SECRET', '')
    if not a.collector_url or len(secret) < 32:
        raise SystemExit('Set COLLECTOR_URL and COLLECTOR_SECRET (at least 32 characters).')
    started = time.time()
    job = post(a.collector_url, dict(secret=secret, action='fetch', submission_id=a.submission_id))
    work = Path(tempfile.mkdtemp(prefix='sub_'))
    nb_path = work / 'submission.ipynb'
    nb_path.write_bytes(restore_data_block(job['notebook'].encode()))
    report = dict(grader=os.environ.get('GITHUB_SHA', 'local')[:12])
    mode = job.get('mode', 'grade')
    try:
        check = sandbox_check(nb_path, a.image)
        failed = check['failed']
        report.update(runs_from_top=not failed, first_failed_cell=(f"code cell {failed[0]['cell']} ({failed[0]['first_line']}): {failed[0]['error']}" if failed else ''),
                      failed_cells=[f"code cell {f['cell']}: {f['error']}" for f in failed[:10]], missing_functions=check['missing_functions'], memo_found=check['memo_found'])
        if mode == 'grade' and not job.get('rehearsal'):
            part_a, part_b, total, status, flags = marks(nb_path, job['registration'], job['cohort'], a.image, Path(a.out or work / 'out'))
            report.update(part_a=part_a, part_b=part_b, total=total, detail=f'status {status}; flags {flags or "none"}; {time.time() - started:.0f} s')
        else:
            report.update(detail=f'structural check only ({"the issued file" if job.get("issued_file") else "not the issued file"}); {time.time() - started:.0f} s')
    except Exception as error:          # the student still sees "received"; the lecturer sees why the instant check did not finish
        report.update(detail='instant check did not finish: ' + str(error)[:250])
    post(a.collector_url, dict(secret=secret, action='result', submission_id=a.submission_id, report=report))
    shown = {k: report.get(k) for k in ('runs_from_top', 'missing_functions', 'memo_found', 'detail')}
    print(json.dumps(dict(submission=a.submission_id, mode=mode, seconds=round(time.time() - started), **shown)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
