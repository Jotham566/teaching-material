"""Write the two import files for the gradebook from the grading output.

    python3 tools/export_for_gradebook.py [--results grading_output/ML_PROJECT_results.csv] [--out grading_output/gradebook]
                                          [--roster Grades.csv] [--zeros-for-no-submission] [--release REG ...]

COLUMN MAPPING (the grading output file ML_PROJECT_results.csv  ->  the gradebook Grades sheet, grader/gradebook.gs importMarkedResults):

    results column   gradebook column        out of   import file written
    ---------------  -----------------------  -------  -------------------------------------------
    registration     student_id                        both files (upper case, trimmed: the roster key)
    part_a           ML Project Part A         30      ML_Project_Part_A_import.csv   (score)
    part_b           ML Project Part B         15      ML_Project_Part_B_import.csv   (score)
    (project_total   not imported: the sheet adds Part A + Part B itself)

FILE FORMAT importMarkedResults expects: a header row with the columns student_id, status, score, maximum (any order, no quoted commas);
one row per student; status OK, ERRORS or AUTO_SCORED (any other status makes the whole import stop with "Unresolved result"); the maximum column
equal to 30 (Part A) or 15 (Part B); score between 0 and the maximum; every student_id on the Grades roster; no duplicates. This script writes exactly that
and checks all of it before it writes, so the import cannot stop half way. Run in the gradebook: importMarkedResults('<Drive file id>', 'ML Project Part A')
and again with the Part B file and 'ML Project Part B'; then recomputeAll().

Students held back (identity mismatch, the grader could not run the notebook; copy suspicions are NOT held back, you decide after the spot check) are NOT in the import files. They are written
to ML_Project_held_back.csv. After you have looked at them, release them with --release <registration> ... (or fix their mark with grade_project.py --overrides).
A student with only one of the two columns filled stays PENDING in the sheet, so holding someone back never produces a wrong total.
--roster takes any CSV with a student_id column (for example an export of the Grades sheet). Students on the roster who submitted nothing get no row, unless
--zeros-for-no-submission is given: then they get 0 and 0 with status AUTO_SCORED (type 0 only when you are sure the project was due and not handed in).
Students in the results who are not on the roster are listed in ML_Project_not_on_roster.csv and NOT imported (the sheet would refuse the whole file).
"""
import argparse
import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
COLUMNS = {'ML Project Part A': ('part_a', 30, 'ML_Project_Part_A_import.csv'), 'ML Project Part B': ('part_b', 15, 'ML_Project_Part_B_import.csv')}
HOLD = {'IDENTITY_MISMATCH', 'GRADER_STATUS'}
ACCEPTED = {'OK', 'ERRORS', 'AUTO_SCORED'}


def key(value):
    return str(value).strip().upper()


def number(x):
    x = round(float(x), 2)
    return str(int(x)) if x == int(x) else str(x)


def validate(rows, maximum, roster=None):
    """The same checks as importMarkedResults, so a bad file is caught here. Returns a list of problems."""
    problems, seen = [], set()
    for r in rows:
        sid = key(r['student_id'])
        if sid in seen:
            problems.append(f'Duplicate result {sid}')
        seen.add(sid)
        if roster is not None and sid not in roster:
            problems.append(f'Result not on roster {sid}')
        if r['status'] not in ACCEPTED:
            problems.append(f'Unresolved result {sid}: {r["status"]}')
        if r['score'] == '' or float(r['maximum']) != maximum:
            problems.append(f'Missing mark or maximum mismatch {sid}')
        if not 0 <= float(r['score']) <= maximum:
            problems.append(f'Invalid mark {r["score"]}; expected 0 to {maximum}')
        if ',' in sid or ',' in r['status']:
            problems.append(f'A comma in {sid}: the CSV parser would split the cell')
    return problems


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--results', default=str(PROJECT / 'grading_output/ML_PROJECT_results.csv'))
    ap.add_argument('--out', default=str(PROJECT / 'grading_output/gradebook'))
    ap.add_argument('--roster', help='CSV with a student_id column (for example the Grades sheet exported as CSV)')
    ap.add_argument('--zeros-for-no-submission', action='store_true', help='Give roster students with no submission 0 and 0 (only when the project was due)')
    ap.add_argument('--release', nargs='*', default=[], help='Registration numbers to release although they were held back, after your spot check')
    a = ap.parse_args(argv)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    with open(a.results, newline='') as f:
        results = list(csv.DictReader(f))
    roster = None
    if a.roster:
        with open(a.roster, newline='') as f:
            roster = {key(r['student_id']) for r in csv.DictReader(f) if r.get('student_id', '').strip()}
    release = {key(x) for x in a.release}
    held, off_roster, usable = [], [], []
    for r in results:
        sid = key(r['registration'].lstrip("'"))
        flags = set(r['flags'].split())
        if (flags & HOLD) and sid not in release:
            held.append(dict(registration=sid, cohort=r['cohort'], part_a=r['part_a'], part_b=r['part_b'], held_for=' '.join(sorted(flags & HOLD))))
            continue
        if roster is not None and sid not in roster:
            off_roster.append(dict(registration=sid, cohort=r['cohort'], part_a=r['part_a'], part_b=r['part_b']))
            continue
        usable.append((sid, r))
    files = {}
    for column, (field, maximum, name) in COLUMNS.items():
        rows = [dict(student_id=sid, status=('ERRORS' if r['status'] == 'ERRORS' else 'OK'), score=number(r[field]), maximum=str(maximum)) for sid, r in usable]
        if a.zeros_for_no_submission and roster is not None:
            have = {row['student_id'] for row in rows} | {h['registration'] for h in held} | {o['registration'] for o in off_roster}
            rows += [dict(student_id=sid, status='AUTO_SCORED', score='0', maximum=str(maximum)) for sid in sorted(roster - have)]
        problems = validate(rows, maximum, roster)
        if problems:
            raise SystemExit('The import file for ' + column + ' would be refused by the gradebook:\n  ' + '\n  '.join(problems))
        with (out / name).open('w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=['student_id', 'status', 'score', 'maximum'], lineterminator='\n')
            w.writeheader()
            w.writerows(rows)
        files[column] = (name, len(rows))
    for name, rows, fields in (('ML_Project_held_back.csv', held, ['registration', 'cohort', 'part_a', 'part_b', 'held_for']), ('ML_Project_not_on_roster.csv', off_roster, ['registration', 'cohort', 'part_a', 'part_b'])):
        if rows or (out / name).exists():
            with (out / name).open('w', newline='') as f:
                w = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
                w.writeheader()
                w.writerows(rows)
    for column, (name, n) in files.items():
        print(f'{column}: {n} rows -> {out / name}')
    print(f'{len(held)} held back, {len(off_roster)} not on the roster. Import with importMarkedResults(<Drive file id>, "ML Project Part A") and "ML Project Part B", then recomputeAll().')
    return 0


if __name__ == '__main__':
    sys.exit(main())
