"""Publish trusted practical-test results into the cumulative grading generation."""
import hashlib
import json
from pathlib import Path
import shutil

import continuous_assessment as ca
import refresh_ca as refresh


def integrate(test_file, private=refresh.PRIVATE, renderer=refresh.render):
    """Standalone entry point; callers already holding the lock use integrate_locked."""
    private = Path(private).resolve()
    with refresh.exclusive(private):
        return integrate_locked(test_file, private, renderer)


def integrate_locked(test_file, private, renderer=refresh.render):
    private = Path(private).resolve()
    refresh.finish_publish(private)
    previous = refresh.active_base(private)
    old = refresh.read(previous/'ledger.json')
    if old is None:
        raise ValueError('Restore the private assessment snapshot before integrating tests. Test results remain saved.')
    if (private/('~$'+refresh.BOOK)).exists():
        raise ValueError('Close the cumulative workbook in Excel and repeat the test command. Test results remain saved.')
    # Ignore presentation-only changes and explicitly labelled rehearsals.
    incoming = refresh.read(test_file)['attempts']
    incoming = [r for r in incoming if r.get('status') != 'REHEARSAL']
    ids = [r['response_id'] for r in incoming]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate test receipt IDs')
    old_by_id = {r['response_id']: r for r in old['attempts']}
    for row in incoming:
        prior = old_by_id.get(row['response_id'])
        if prior and (prior['cohort'] != row['cohort'] or prior['assessment'] != row['assessment']
                      or prior['email'] != row['email'].strip().lower()
                      or ca.norm(prior.get('submitted_student_id', prior['student_id'])) != ca.norm(row['student_registration_number'])
                      or ca.stamp(prior['submitted_at']) != ca.stamp(row['submitted_at'])):
            raise ValueError('Test receipt identity changed; existing cumulative marks retained.')
    fingerprint = hashlib.sha256(json.dumps(incoming, sort_keys=True).encode()).hexdigest()
    if refresh.read(previous/'test_import.json', {}).get('sha256') == fingerprint:
        print('Cumulative test marks already up to date. No duplicate marks added.')
        return previous
    for pending in (private/'batches').glob('*/parent.json'):
        if refresh.read(pending.parent/'status.json', {}).get('state') != 'COMPLETE':
            raise ValueError('An unfinished weekly grading batch exists. Resume it before importing test marks.')
    key = hashlib.sha256((refresh.digest(previous/'ledger.json')+fingerprint).encode()).hexdigest()[:24]
    batch = private/'batches'/('tests-'+key)
    batch.mkdir(parents=True, exist_ok=True)
    if previous == private:
        for name in ('ledger.json', refresh.BOOK):
            backup = private/'before_one_command'/name
            if not backup.exists():
                backup.parent.mkdir(exist_ok=True)
                shutil.copy2(private/name, backup)
    refresh.write(batch/'status.json', {'state': 'IMPORTING_TESTS'})
    try:
        # Carry the coursework context forward so the next weekly refresh can
        # reuse sources, grading checkpoints, review evidence and timing history.
        for name in ('reconciled', 'written_queue', 'written_text'):
            if (previous/name).exists():
                shutil.copytree(previous/name, batch/name, dirs_exist_ok=True)
        for name in ('historical_windows.json', 'quiz_deadlines.json', 'identity_evidence.json', 'identity_file_cache.json'):
            if (previous/name).exists(): shutil.copy2(previous/name, batch/name)
        source = batch/'test_source.json'
        refresh.write(source, {'attempts': incoming})
        empty = batch/'empty_source'; empty.mkdir(exist_ok=True)
        ledger = ca.build(empty, test_ledgers=[source],
                          retained_attempts=[r for r in old['attempts'] if r['response_id'] not in set(ids)])
        new_ids = [r['response_id'] for r in ledger['attempts']]
        if not set(old_by_id) <= set(new_ids) or len(new_ids) != len(set(new_ids)):
            raise ValueError('Receipt history changed unexpectedly; existing cumulative marks retained.')
        ledger['sources'] = old.get('sources', []) + ledger['sources']
        from recover_student_names import apply_evidence
        identity_evidence=refresh.read(batch/'identity_evidence.json',{})
        if identity_evidence: apply_evidence(ledger,identity_evidence,batch/'reconciled')
        refresh.write(batch/'ledger.json', ledger)
        refresh.write(batch/'test_import.json', {'sha256': fingerprint})
        refresh.write(batch/'summary.json', {'test_receipts': len(incoming), 'new_receipts': len(set(new_ids)-set(old_by_id))})
        if renderer is refresh.render: refresh.preflight_workbook()
        renderer(batch)
        refresh.write(batch/'status.json', {'state': 'READY'})
        refresh.publish(private, batch)
    except BaseException as exc:
        if not (private/'refresh_publish.json').exists():
            refresh.write(batch/'status.json', {'state': 'STOPPED', 'error': str(exc)[:1000]})
        raise
    print('Cumulative workbook updated: '+str(private/refresh.BOOK))
    return batch
