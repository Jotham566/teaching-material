"""Read recorded Google Forms scores from private XLSX snapshots.

Row IDs are explicitly spreadsheet references, not invented Forms response IDs.
Replace these snapshots with the Forms receipt export when available; never
combine both representations of the same quiz.
"""
import argparse
import hashlib
import json
from datetime import timezone, timedelta
from pathlib import Path
import openpyxl


def import_sheet(path, cohort, out, deadlines):
    workbook = openpyxl.load_workbook(path, read_only=True, data_only=True)
    provenance = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    timing = {}
    for week in range(1, 6):
        sheet = workbook[f'Form Responses {week}']
        rows = iter(sheet.values)
        headers = next(rows)
        records = []
        for row_number, values in enumerate(rows, 2):
            row = dict(zip(headers, values))
            if not row.get('Timestamp'):
                continue
            at = row['Timestamp']
            if at.tzinfo is None:
                at = at.replace(tzinfo=timezone(timedelta(hours=3)))
            score = row.get('Score')
            receipt = f'sheet:{cohort}:Q{week}:row{row_number}'
            answers = [
                dict(id='recorded-total', title='Recorded Forms score', answer='', score=score),
                *[dict(id=str(i), title=h, answer=v, score=None)
                  for i, (h, v) in enumerate(zip(headers, values))
                  if h and ('registration' in h.lower() or 'student number' in h.lower())],
            ]
            records.append(dict(response_id=receipt, email=row.get('Email Address') or '',
                                submitted_at=at.isoformat(), answers=answers))
            end = deadlines[f'{cohort}|{week}']['closeAt']
            timing[receipt] = dict(
                status='ON_TIME' if at.timestamp()*1000 <= end else 'LATE',
                evidence='Live quiz loadLinks_ closeAt export; gradebook.gs imports latest receipt before close, including previous openings.')
        payload = dict(exported_at=Path(path).stat().st_mtime,
                       source_kind='recorded_sheet_scores',
                       source_sha256=provenance,
                       quizzes=[dict(key=f'{cohort}|{week}', items=[
                           dict(id='recorded-total', points=5)], records=records)])
        (out/f'{cohort}_Q{week}_quiz.json').write_text(json.dumps(payload, indent=2))
    return timing


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--private', required=True)
    parser.add_argument('--out', required=True)
    parser.add_argument('--deadlines', required=True)
    parser.add_argument('--timing', required=True)
    args = parser.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    deadlines = json.loads(Path(args.deadlines).read_text())
    timing = {}
    for cohort in ('CML3111', 'CML3112', 'CML3113'):
        timing.update(import_sheet(Path(args.private)/f'{cohort}_quiz_source.xlsx',
                                   cohort, out, deadlines))
    Path(args.timing).write_text(json.dumps(timing, indent=2))
    print(f'Imported {len(timing)} recorded quiz scores.')
