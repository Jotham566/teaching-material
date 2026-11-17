"""Persist every distinct collection issue without silently resolving it."""
import hashlib
import json


def _validated(rows, source):
    if not isinstance(rows, list):
        raise ValueError(f'Collection issues in {source} must be a list')
    for row in rows:
        if not isinstance(row, list) or len(row) != 15:
            raise ValueError(f'Invalid collection issue in {source}: expected 15 columns')
    return rows


def store_issues(db, rows, source):
    rows = _validated(rows, source)
    with db:
        db.execute('CREATE TABLE IF NOT EXISTS collection_issue_history '
                   '(sequence INTEGER PRIMARY KEY, digest TEXT NOT NULL UNIQUE, payload TEXT NOT NULL)')
        for row in rows:
            payload = json.dumps(row, ensure_ascii=False, separators=(',', ':'))
            digest = hashlib.sha256(payload.encode('utf-8')).hexdigest()
            existing = db.execute('SELECT payload FROM collection_issue_history WHERE digest=?',
                                  (digest,)).fetchone()
            if existing and existing[0] != payload:
                raise ValueError('Collection issue digest collision')
            db.execute('INSERT OR IGNORE INTO collection_issue_history (digest,payload) VALUES (?,?)',
                       (digest, payload))


def import_existing_issues(db, out):
    issue_file = out / 'collection_issues.json'
    workbook_file = out / 'workbook_data.json'
    if issue_file.exists():
        store_issues(db, json.loads(issue_file.read_text()), str(issue_file))
    if workbook_file.exists():
        data = json.loads(workbook_file.read_text())
        if not isinstance(data, dict):
            raise ValueError('Existing workbook data must be an object')
        if 'collection_issues' in data:
            store_issues(db, data['collection_issues'], str(workbook_file))
    store_issues(db, [], 'initialization')


def read_issues(db):
    return [json.loads(row[0]) for row in
            db.execute('SELECT payload FROM collection_issue_history ORDER BY sequence')]
