"""After the window: ONE command re-grades every submission on the Mac and checks it against the instant results from GitHub Actions.

    python3 actions/final_regrade.py --zip IUEA-ml-project-batch-<date>.zip [--roster Grades.csv] [--out grading_output]

It runs, in order, with Docker and the Colab-matching image:
  1. grade_project.py --zip  (all fairness rules: own cells count, the latest on-time submission, identity and copy checks)
     -> ML_PROJECT_results.xlsx/.csv, the spot-check list, feedback/ and memos/
  2. export_for_gradebook.py -> the two gradebook import files (and the held-back list)
  3. a comparison with the instant results stored by the collector (manifest.json, instant_results): for the submission that is marked
     (the latest on time), Part A and Part B must be the same. Every difference is written to actions_vs_final.csv and printed.
The marks that count are the final run's. Exit code 1 if any difference is found, so it cannot go unnoticed.
"""
import argparse
import csv
import json
import subprocess
import sys
import zipfile
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
PLAN = PROJECT.parents[1]
sys.path.insert(0, str(PLAN / 'grader'))
from registration import normalize  # noqa: E402


def when(value):
    return datetime.fromisoformat(str(value).replace('Z', '+00:00'))


def compare(zip_path, results_csv, out_csv):
    """Rows (registration, receipt, actions A, B, final A, B, verdict). The receipt compared is the one the final run marks."""
    with zipfile.ZipFile(zip_path) as z:
        manifest = json.loads(z.read('manifest.json'))
    instant = {r['submission_id']: r for r in manifest.get('instant_results', [])}
    latest = {}
    for job in manifest['jobs']:
        if job.get('assessment') != 'ML_PROJECT' or not when(job['opens_at']) <= when(job['submitted_at']) <= when(job['closes_at']):
            continue
        who = normalize(job['student_registration_number'])
        if who not in latest or when(job['submitted_at']) > when(latest[who]['submitted_at']):
            latest[who] = job
    final = {normalize(r['registration']): r for r in csv.DictReader(open(results_csv))}
    rows = []
    for who, job in sorted(latest.items()):
        i, f = instant.get(job['response_id'], {}), final.get(who)
        a_i, b_i = i.get('part_a', ''), i.get('part_b', '')
        if f is None:
            verdict = 'NOT IN FINAL RUN'
        elif a_i in ('', None):
            verdict = 'NO INSTANT RESULT'
        elif abs(float(a_i) - float(f['part_a'])) < 1e-6 and abs(float(b_i) - float(f['part_b'])) < 1e-6:
            verdict = 'SAME'
        else:
            verdict = 'DIFFERENT'
        rows.append(dict(registration=who, receipt=job['response_id'], actions_part_a=a_i, actions_part_b=b_i,
                         final_part_a=f['part_a'] if f else '', final_part_b=f['part_b'] if f else '', verdict=verdict))
    with open(out_csv, 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]) if rows else ['registration'])
        w.writeheader()
        w.writerows(rows)
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--zip', required=True)
    ap.add_argument('--roster', help='Grades sheet as CSV (student_id column); without it the gradebook files list only graded students')
    ap.add_argument('--out', default=str(PROJECT / 'grading_output'))
    ap.add_argument('--image', default='iuea-notebooks:colab-2026.11')
    a = ap.parse_args(argv)
    out = Path(a.out)
    rc = subprocess.run([sys.executable, str(PROJECT / 'grader_spec/grade_project.py'), '--zip', a.zip, '--out', str(out), '--image', a.image]).returncode
    if rc:
        raise SystemExit(f'grade_project.py stopped (exit {rc}). Nothing else was done.')
    export = [sys.executable, str(PROJECT / 'tools/export_for_gradebook.py'), '--results', str(out / 'ML_PROJECT_results.csv'), '--out', str(out / 'gradebook')]
    if a.roster:
        export += ['--roster', a.roster, '--zeros-for-no-submission']
    if subprocess.run(export).returncode:
        raise SystemExit('export_for_gradebook.py stopped. The results are in ' + str(out))
    rows = compare(a.zip, out / 'ML_PROJECT_results.csv', out / 'actions_vs_final.csv')
    counts = {}
    for r in rows:
        counts[r['verdict']] = counts.get(r['verdict'], 0) + 1
    print('Instant (GitHub Actions) against final run:', ', '.join(f'{k} {v}' for k, v in sorted(counts.items())) or 'no submissions')
    for r in rows:
        if r['verdict'] != 'SAME':
            print(f"  {r['verdict']}: {r['registration']} receipt {r['receipt']}: Actions A {r['actions_part_a']} B {r['actions_part_b']}, final A {r['final_part_a']} B {r['final_part_b']}")
    print('Final marks:', out / 'ML_PROJECT_results.xlsx', '| gradebook files:', out / 'gradebook', '| comparison:', out / 'actions_vs_final.csv')
    return 1 if any(r['verdict'] == 'DIFFERENT' for r in rows) else 0


if __name__ == '__main__':
    sys.exit(main())
