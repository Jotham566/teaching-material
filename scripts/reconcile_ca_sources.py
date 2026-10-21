"""Join downloaded Forms receipts to recorded Sheet scores without double counting."""
import argparse
import collections
import json
import shutil
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'IUEA_Teaching_Plan/grader'))
from continuous_assessment import field, norm, stamp, quiz_mark


def reconcile(audit, forms, out, deadlines, historical_windows=None):
    audit, forms, out = map(Path, (audit, forms, out))
    out.mkdir(parents=True, exist_ok=True)
    timing, checks = {}, []
    for audit_path in audit.glob('*_manifest.json'):
        source = forms/audit_path.name
        payload = json.loads((source if source.exists() else audit_path).read_text())
        previous = json.loads(audit_path.read_text())
        for row in previous['records']:
            timing[row['response_id']] = dict(status=row['timing_status'],
                evidence='Original submission audit snapshot; unresolved EARLY/LATE statuses retained.')
            for window in (historical_windows or {}).get(previous['key'], []):
                if not window.get('evidence'):
                    raise ValueError('Historical window requires evidence')
                if stamp(window['open']) <= stamp(row['submitted_at']) <= stamp(window['close']):
                    timing[row['response_id']] = dict(status='ON_TIME', evidence=window['evidence'])
                    break
        (out/audit_path.name).write_text(json.dumps(payload, indent=2))
    if (forms/'files').exists():
        shutil.copytree(forms/'files', out/'files', dirs_exist_ok=True)
    for sheet_file in audit.glob('*_quiz.json'):
        sheet = json.loads(sheet_file.read_text())
        raw_path = forms/sheet_file.name
        if not raw_path.exists():
            payload = sheet
        else:
            payload = json.loads(raw_path.read_text())
            original = payload['quizzes'][0]
            sheet_quiz = sheet['quizzes'][0]
            rows = collections.defaultdict(list)
            for r in sheet_quiz['records']:
                key = (int(stamp(r['submitted_at']).timestamp()), r['email'].strip().lower())
                rows[key].append(r)
            used = set()
            for r in original['records']:
                key = (int(stamp(r['submitted_at']).timestamp()), (r['email'] or '').strip().lower())
                matches = rows.get(key, [])
                score, status = quiz_mark(original, r)
                if len(matches) == 1:
                    match = matches[0]
                    source_fields = {v['title']:v['answer'] for v in r['answers']}
                    sheet_fields = {v['title']:v['answer'] for v in match['answers']}
                    terms = ['registration','student id','student_id','student number']
                    source_id, sheet_id = norm(field(source_fields, terms)), norm(field(sheet_fields, terms))
                    if source_id and sheet_id and source_id != sheet_id:
                        checks.append(dict(key=original['key'], response_id=r['response_id'], issue='REGISTRATION_SOURCE_CONFLICT'))
                        score = None
                    elif status=='GRADED' and match['answers'][0]['score'] is not None and score!=match['answers'][0]['score']:
                        checks.append(dict(key=original['key'], response_id=r['response_id'], issue='SCORE_SOURCE_CONFLICT'))
                        score = None
                    else:
                        score = match['answers'][0]['score']
                        used.add(match['response_id'])
                        if not source_id and sheet_id:
                            r['answers'].append(dict(id='sheet-identity', title='Student Registration Number', answer=sheet_id))
                        r['sheet_receipt'] = match['response_id']
                else:
                    checks.append(dict(key=original['key'], response_id=r['response_id'], issue='NO_UNIQUE_SHEET_MATCH'))
                r['answers'].append(dict(id='recorded-total', title='Recorded Forms total', answer='', score=score))
            original['original_items'] = original['items']
            original['items'] = [dict(id='recorded-total', points=5)]
            # Keep Sheet-only receipts rather than silently dropping student work.
            for rows_at_time in rows.values():
                for r in rows_at_time:
                    if r['response_id'] not in used:
                        if any(int(stamp(x['submitted_at']).timestamp()) == int(stamp(r['submitted_at']).timestamp())
                               and (x['email'] or '').strip().lower() == r['email'].strip().lower()
                               for x in original['records']):
                            continue
                        original['records'].append(r)
                        checks.append(dict(key=original['key'], response_id=r['response_id'], issue='SHEET_ONLY_RECEIPT'))
            payload['sheet_source_sha256'] = sheet['source_sha256']
        for quiz in payload['quizzes']:
            end = deadlines[quiz['key']]['closeAt']
            for r in quiz['records']:
                timing[r['response_id']] = dict(
                    status='ON_TIME' if stamp(r['submitted_at']).timestamp()*1000 <= end else 'LATE',
                    evidence='Live closeAt audit; existing gradebook.gs latest-before-close policy.')
        (out/sheet_file.name).write_text(json.dumps(payload, indent=2))
    (out/'timing.json').write_text(json.dumps(timing, indent=2))
    (out/'reconciliation.json').write_text(json.dumps(checks, indent=2))
    return checks


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('audit','forms','out','deadlines'):p.add_argument('--'+name,required=True)
    p.add_argument('--historical-windows')
    a=p.parse_args()
    checks=reconcile(a.audit,a.forms,a.out,json.loads(Path(a.deadlines).read_text()),
                     json.loads(Path(a.historical_windows).read_text()) if a.historical_windows else None)
    print('Source reconciliation exceptions:',len(checks))
