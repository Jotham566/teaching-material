"""One-command, checkpointed Week 1–5 refresh. All working data stays private."""
import argparse
import collections
import contextlib
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shutil
import shlex
import subprocess
import sys
import time
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'scripts'))
import continuous_assessment as ca
from import_ca_audit import import_audit
from import_ca_quiz_sheets import import_sheet
from reconcile_ca_sources import reconcile
from recover_ca_file_extensions import recover
from unpack_ca_export import unpack
from ca_bundle import bundle_header, verify_bundle

PRIVATE = ROOT/'IUEA_Teaching_Plan/assessment_operations/private'
EARLY = {f'Q{i}' for i in range(1, 6)} | {f'W{i:02}' for i in range(1, 6)}
COHORTS = ca.COHORTS
BOOK = 'IUEA_Continuous_Assessment.xlsx'


def read(path, default=None):
    return json.loads(Path(path).read_text()) if Path(path).exists() else default


def write(path, value):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name+'.tmp')
    tmp.write_text(json.dumps(value, indent=2)+'\n'); os.replace(tmp, path)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


@contextlib.contextmanager
def exclusive(private):
    private.mkdir(parents=True, exist_ok=True)
    with (private/'refresh.lock').open('a+') as lock:
        try: fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise RuntimeError('A grading refresh is already running. Wait for it to finish.')
        # Older launchers do not share our lock. Refuse overlap with them too.
        processes = subprocess.check_output(['ps', '-axo', 'pid=,command='], text=True)
        names={'run_ca_written_queue.py','finish_ca_refresh.py','grade_ca_batch.py',
               'grade_ca_written.py','batch_grade.py','refresh_ca.py'}
        for line in processes.splitlines():
            parts=line.strip().split(None,1)
            if len(parts)!=2 or int(parts[0])==os.getpid(): continue
            try: args=shlex.split(parts[1])
            except ValueError: continue
            if any(Path(arg).name in names for arg in args):
                raise RuntimeError('Another grading process is running. Finish it before refreshing.')
        yield


def inventory(download):
    download = Path(download).expanduser().resolve()
    if download.is_file() and download.suffix.lower()=='.zip':
        verify_bundle(download)
        return {download.name:digest(download)}
    if not download.is_dir(): raise ValueError('Give the downloaded grading ZIP, or a legacy download folder.')
    expected = {f'{c}_quiz_source.xlsx' for c in COHORTS} | {'assignment_source.xlsx'}
    files = {p.name: p for p in download.iterdir() if p.is_file() and not p.name.startswith('.')}
    if len(files)==1:
        only=next(iter(files.values()))
        if only.suffix.lower()=='.zip' and bundle_header(only):
            verify_bundle(only);return {only.name:digest(only)}
    missing = expected - files.keys()
    if missing: raise ValueError('Missing downloads: '+', '.join(sorted(missing)))
    zips = [p for p in files.values() if p.suffix.lower()=='.zip']
    if not zips: raise ValueError('No submission export ZIP found. Include every Drive download part.')
    allowed = expected | {p.name for p in zips} | {'quiz_deadlines.json', 'historical_windows.json'}
    unexpected = files.keys() - allowed
    if unexpected: raise ValueError('Use a dedicated batch folder. Unexpected files: '+', '.join(sorted(unexpected)))
    return {name: digest(path) for name, path in sorted(files.items())}


def active_base(private):
    state = read(private/'refresh_active.json')
    if not state: return private
    base = (private/state['generation']).resolve()
    if not base.is_relative_to(private.resolve()): raise ValueError('Invalid active snapshot path')
    if not (base/'ledger.json').exists(): raise ValueError('Active snapshot is missing; restore private backup first.')
    if digest(private/'ledger.json')!=digest(base/'ledger.json'):
        raise ValueError('Marks were updated outside this runner. Reconcile the newer ledger before refreshing; it will not be overwritten.')
    return base


def merge_rows(old, fresh, identity):
    rows = {r['response_id']: r for r in old}
    for r in fresh:
        prior = rows.get(r['response_id'])
        if prior and identity(prior) != identity(r):
            raise ValueError('A receipt identity or timestamp changed; review the batch before importing.')
        rows[r['response_id']] = r
    return list(rows.values())


def merge_sources(previous, incoming, out):
    """Union receipts, never erase attempts omitted from a later download."""
    if out.resolve() in (previous.resolve(), incoming.resolve()): raise ValueError('Cannot overwrite source snapshot')
    # A stopped batch may contain a partial merge. Rebuild only its staging copy.
    if out.exists(): shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)
    for source in (previous, incoming):
        if (source/'files').exists(): shutil.copytree(source/'files', out/'files', dirs_exist_ok=True)
        for p in sorted(list(source.glob('*_manifest.json'))+list(source.glob('*_quiz.json'))):
            current = read(p); old = read(out/p.name)
            if old:
                if isinstance(old.get('exported_at'),str) and isinstance(current.get('exported_at'),str):
                    if ca.stamp(current['exported_at']) < ca.stamp(old['exported_at']):
                        raise ValueError('This export is older than the saved source snapshot. Download the latest batch.')
                if p.name.endswith('_manifest.json'):
                    if current['key'] != old['key']: raise ValueError('Assessment source mismatch')
                    current['records'] = merge_rows(old['records'], current['records'],
                        lambda r: (r['assessment_key'], r['email'].lower(), r['submitted_at'], r['fields']))
                    files = {f['id']: f for f in old['files']}; files.update({f['id']: f for f in current['files']})
                    current['files'] = list(files.values())
                else:
                    a, b = old['quizzes'][0], current['quizzes'][0]
                    if a['key'] != b['key']: raise ValueError('Quiz source mismatch')
                    old_rows = {r['response_id']: r for r in a['records']}
                    for r in b['records']:
                        prior = old_rows.get(r['response_id'])
                        if prior and ca.quiz_mark(a, prior)[1]=='GRADED' and ca.quiz_mark(b, r)[1]!='GRADED':
                            raise ValueError('A previously recorded quiz score is missing in the new download. Refresh the quiz spreadsheets.')
                    b['records'] = merge_rows(a['records'], b['records'],
                        lambda r: (r['email'].lower(), r['submitted_at']))
            write(out/p.name, current)
    # Check the complete union, including earlier attempts, before grading.
    for p in out.glob('*_manifest.json'):
        meta = read(p); files = {f['id']: f for f in meta['files']}
        for row in meta['records']:
            for fid in row['file_ids']:
                f = files.get(fid)
                if not f or not (out/'files'/f['export_name']).is_file():
                    raise ValueError('An attachment is missing. Download all ZIP parts again.')
                if digest(out/'files'/f['export_name']) != f['sha256']:
                    raise ValueError('An attachment checksum changed unexpectedly.')


def prepare_batch(download, batch, previous):
    forms, audit, fresh = batch/'forms', batch/'audit', batch/'fresh'
    # Idempotent after interruption; extraction rejects conflicting ZIP parts.
    for p in sorted((batch/'downloads').glob('*.zip')): unpack(p, forms)
    expected = {f'{c}_W{i:02}_manifest.json' for c in COHORTS for i in range(1,6)}
    expected |= {f'{c}_Q{i}_quiz.json' for c in COHORTS for i in range(1,6)}
    if not all((forms/n).is_file() for n in expected): raise ValueError('Incomplete export: require all 15 assignment and 15 quiz manifests.')
    for p in forms.glob('*_manifest.json'):
        meta=read(p)
        if meta['key'].replace('|','_')+'_manifest.json' != p.name: raise ValueError('Invalid manifest identity')
        for f in meta['files']:
            if Path(f['export_name']).name!=f['export_name'] or '/' in f['id'] or not isinstance(f['sha256'],str) or len(f['sha256'])!=64:
                raise ValueError('Invalid attachment metadata')
        if meta.get('errors'): raise ValueError('The export reports attachment errors. Re-export before grading.')
    bundled=read(forms/'ca_bundle.json')
    history=read(batch/'downloads/historical_windows.json', read(previous/'historical_windows.json', {}))
    write(batch/'historical_windows.json',history)
    if bundled:
        deadlines=read(forms/'quiz_deadlines.json')
        write(batch/'quiz_deadlines.json',deadlines)
        shutil.copytree(forms,fresh,dirs_exist_ok=True)
        timing={};checks=[];cutoff=ca.stamp(bundled['cutoff'])
        for p in fresh.glob('*_manifest.json'):
            meta=read(p)
            for r in meta['records']:
                if ca.stamp(r['submitted_at'])>cutoff:raise ValueError('Receipt after bundle cutoff')
                status=r.get('timing_status','UNVERIFIED')
                if status not in ('ON_TIME','LATE','EARLY'):status='UNVERIFIED'
                timing[r['response_id']]={'status':status,'evidence':'Assignment audit captured in the verified one-ZIP export.'}
                for window in history.get(meta['key'],[]):
                    if not window.get('evidence'):raise ValueError('Historical window requires evidence')
                    if ca.stamp(window['open'])<=ca.stamp(r['submitted_at'])<=ca.stamp(window['close']):
                        timing[r['response_id']]={'status':'ON_TIME','evidence':window['evidence']};break
        for p in fresh.glob('*_quiz.json'):
            payload=read(p)
            if payload.get('source_kind')!='recorded_sheet_scores_with_form_receipts':raise ValueError('Bundle lacks recorded quiz scores')
            for q in payload['quizzes']:
                end=deadlines.get(q['key'],{}).get('closeAt')
                if isinstance(end,bool) or not isinstance(end,(int,float)):raise ValueError('Bundle quiz deadline missing')
                for r in q['records']:
                    at=ca.stamp(r['submitted_at'])
                    if at>cutoff:raise ValueError('Receipt after bundle cutoff')
                    timing[r['response_id']]={'status':'ON_TIME' if at.timestamp()*1000<=end else 'LATE','evidence':'Quiz timing mirror captured in the verified one-ZIP export.'}
        write(fresh/'timing.json',timing)
    else:
        deadlines = read(batch/'downloads/quiz_deadlines.json', read(previous/'quiz_deadlines.json'))
        if not deadlines: raise ValueError('No verified quiz deadlines are available. Restore the private grading snapshot.')
        for c in COHORTS:
            for i in range(1,6):
                if not isinstance(deadlines.get(f'{c}|{i}', {}).get('closeAt'), (float,int)):
                    raise ValueError('Quiz deadline audit is incomplete.')
        write(batch/'quiz_deadlines.json', deadlines)
        audit.mkdir(exist_ok=True)
        import_audit(batch/'downloads/assignment_source.xlsx', audit)
        for c in COHORTS: import_sheet(batch/'downloads'/f'{c}_quiz_source.xlsx', c, audit, deadlines)
        # Require fresh form and audit exports to describe the same assignment receipts.
        for name in expected:
            if not name.endswith('_manifest.json'): continue
            f = read(forms/name); a = read(audit/name, {'records': []})
            if {r['response_id'] for r in f['records']} != {r['response_id'] for r in a['records']}:
                raise ValueError('Assignment audit and ZIP cover different receipts for '+f['key']+'. Download matching snapshots.')
            # Empty cohorts still need a manifest for reconciliation.
            if not (audit/name).exists(): write(audit/name, f)
        history = read(batch/'downloads/historical_windows.json', read(previous/'historical_windows.json', {}))
        write(batch/'historical_windows.json', history)
        checks = reconcile(audit, forms, fresh, deadlines, history)
        if any(x['issue']=='SHEET_ONLY_RECEIPT' for x in checks):
            raise ValueError('Quiz spreadsheets contain receipts absent from the ZIP. Re-export matching snapshots.')
    recover(fresh)
    merge_sources(previous/'reconciled', fresh, batch/'reconciled')
    timing = read(fresh/'timing.json', {})
    if not bundled and not (batch/'downloads/quiz_deadlines.json').exists():
        for p in fresh.glob('*_quiz.json'):
            for q in read(p)['quizzes']:
                for r in q['records']:
                    t=timing[r['response_id']]
                    if t['status']=='LATE': t['status']='UNVERIFIED'
                    t['evidence']='Saved verified quiz deadline; later receipts need a fresh deadline audit before allocation.'
    # Previously verified timing decisions survive reopening and audit relabelling.
    for rid, decision in read(previous/'reconciled/timing.json', {}).items():
        if decision.get('status')=='ON_TIME' or rid not in timing:
            timing[rid]=decision
    # A fresh explicit deadline audit can establish new quiz receipts; otherwise
    # after the saved deadline they stay pending until the lecturer verifies it.
    write(batch/'reconciled/timing.json', timing)
    write(batch/'reconciliation.json', checks)


def select_work(source, ledger, old_results):
    by_id = {r['response_id']: r for r in old_results}
    retained, todo = [], []
    for r in ledger['attempts']:
        if r['assessment'] not in EARLY or r['assessment'].startswith('Q'): continue
        old = by_id.get(r['response_id'])
        meta = read(source/r['source']); files = {f['id']: f['sha256'] for f in meta['files']}
        hashes = {fid: files[fid] for fid in r['file_ids'] if fid in files}
        same = old and all(old.get(k)==r[k] for k in ('cohort','assessment','student_id')) and old.get('source_hashes')==hashes and bool(hashes)
        # Do not silently rerun already-awarded or review-held AI judgements.
        if same and old['status'] in ('GRADED','WRITTEN_REVIEW'):
            retained.append(old)
        else: todo.append(r)
    return retained, todo


def ensure_docker():
    if subprocess.run(['docker','info'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode==0: return
    if sys.platform!='darwin': raise RuntimeError('Start Docker before notebook grading.')
    subprocess.run(['docker','desktop','start'], check=True, timeout=120)
    for _ in range(30):
        if subprocess.run(['docker','info'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode==0: return
        time.sleep(2)
    raise RuntimeError('Docker did not start. Start Docker Desktop and repeat the command.')


def grade(batch, todo):
    import grade_ca_batch, grade_ca_written, prepare_ca_written
    from reconcile_ca_notebook_identity import reconcile as reconcile_identity
    from local_ai_resources import ensure_docker_stopped
    from run_ca_written_queue import unload
    from calibration_record import model_for_report
    if not todo: return []
    source = batch/'reconciled'; ledger = batch/'grading_input.json'
    write(ledger, {'current': todo})
    # Unload a previously resident model before the Docker phase.
    models = []
    for report in (PRIVATE/'W01_calibration_isolated.json', ROOT/'review/2026-09-14/rework/local_calibration_v10.json'):
        if report.exists():
            model = model_for_report(report); models.append(model)
            try: unload(model)
            except OSError: pass  # The Ollama server may not be started yet.
    ensure_docker()
    coding_dir = batch/'notebook_grades'; coding_dir.mkdir(exist_ok=True)
    coding = reconcile_identity(grade_ca_batch.run(source, ledger, coding_dir))
    coding_file = coding_dir/'identity_checked_results.json'; write(coding_file, coding)
    prepare_ca_written.prepare(source, ledger, batch/'written_text')
    ensure_docker_stopped()
    merged = {r['response_id']: r for r in coding}
    for assessment, report in [('W01', PRIVATE/'W01_calibration_isolated.json'), ('W02', ROOT/'review/2026-09-14/rework/local_calibration_v10.json')]:
        if not any(r['assessment']==assessment and r['timing_status']=='ON_TIME' for r in todo): continue
        print('Written grading '+assessment+' (native Ollama; Docker stopped)', flush=True)
        try:
            results = grade_ca_written.run(source, ledger, coding_file, report, assessment,
                batch/'written_queue'/assessment, batch/'written_text/prepared.json')
            merged.update({r['response_id']: r for r in results})
        finally:
            try: unload(model_for_report(report))
            except Exception: pass
    return list(merged.values())


def preflight_workbook():
    from run_ca_written_queue import NODE
    runtime=Path(os.environ.get('IUEA_ARTIFACT_NODE_MODULES',str(Path.home()/'.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules')))
    if not NODE.is_file() and not shutil.which(str(NODE)): raise RuntimeError('Workbook Node runtime missing. Open Codex on this Mac and complete the setup preflight.')
    probe="require('module').createRequire(require('path').join(process.argv[1],'package.json'))('@oai/artifact-tool')"
    result=subprocess.run([str(NODE),'-e',probe,str(runtime)],capture_output=True,text=True)
    if result.returncode: raise RuntimeError('Workbook runtime unavailable. Open Codex and ask it to initialize the bundled spreadsheet dependencies, then repeat this command.')


def render(batch):
    from run_ca_written_queue import NODE
    subprocess.run([str(NODE), str(ROOT/'scripts/build_continuous_assessment.mjs'),
                    str(batch/'ledger.json'), str(batch/BOOK)], check=True)
    # Validate the generated XML and cached formula values before publication.
    with zipfile.ZipFile(batch/BOOK) as z:
        if z.testzip() or 'xl/workbook.xml' not in z.namelist(): raise ValueError('Workbook validation failed')
        import xml.etree.ElementTree as ET
        ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
        for name in z.namelist():
            if name.startswith('xl/worksheets/sheet') and name.endswith('.xml'):
                if any(c.get('t')=='e' for c in ET.fromstring(z.read(name)).findall('.//s:c',ns)):
                    raise ValueError('Workbook contains an Excel error; previous workbook retained')


def publish(private, batch):
    """Journal a completed generation; retry finishes an interrupted publication."""
    relative = str(batch.relative_to(private))
    write(private/'refresh_publish.json', {'generation': relative})
    finish_publish(private)


def finish_publish(private):
    pending = read(private/'refresh_publish.json')
    if not pending: return
    batch = (private/pending['generation']).resolve()
    if not batch.is_relative_to(private.resolve()) or read(batch/'status.json', {}).get('state') not in ('READY','COMPLETE'):
        raise ValueError('Invalid publication journal')
    # Copies are replaced atomically, and the old generation remains immutable.
    for name in ('ledger.json', BOOK):
        tmp = private/(name+'.publishing'); shutil.copy2(batch/name, tmp); os.replace(tmp, private/name)
    write(private/'refresh_active.json', pending)
    write(batch/'status.json', {'state':'COMPLETE','summary':read(batch/'summary.json')})
    (private/'refresh_publish.json').unlink()


def refresh(download, private=PRIVATE, check_only=False, grader=grade, renderer=render):
    private = Path(private).resolve()
    with exclusive(private):
        finish_publish(private)
        inputs = inventory(download)
        key = hashlib.sha256(json.dumps(inputs, sort_keys=True).encode()).hexdigest()[:24]
        batch = private/'batches'/key
        previous = active_base(private)
        state = read(batch/'status.json', {})
        if state.get('state')=='COMPLETE':
            print('This download batch is already graded. No marks were added again.'); return read(batch/'summary.json')
        batch.mkdir(parents=True, exist_ok=True)
        if not (batch/'parent.json').exists():
            write(batch/'parent.json', {'generation':str(previous.relative_to(private)), 'ledger_sha256':digest(previous/'ledger.json')})
        parent = read(batch/'parent.json')
        if str(previous.relative_to(private))!=parent['generation'] or digest(previous/'ledger.json')!=parent['ledger_sha256']:
            raise ValueError('The marks changed since this batch started. Finish or review that batch before resuming.')
        if (private/('~$'+BOOK)).exists(): raise ValueError('Close the marks workbook in Excel before refreshing.')
        downloads = batch/'downloads'; downloads.mkdir(exist_ok=True)
        for name, expected in inputs.items():
            target = downloads/name
            if not target.exists():
                source_download=Path(download).expanduser()
                shutil.copy2(source_download if source_download.is_file() else source_download/name, target)
            if digest(target)!=expected: raise ValueError('A downloaded file changed while importing.')
        write(batch/'inputs.json', inputs)
        # Save the legacy outputs once before the first publication.
        if previous==private:
            for name in ('ledger.json', BOOK):
                backup = private/'before_one_command'/name
                if not backup.exists(): backup.parent.mkdir(exist_ok=True); shutil.copy2(private/name, backup)
        def status(stage):
            write(batch/'status.json', {'state':stage}); print(stage.replace('_',' ').capitalize(), flush=True)
        try:
            status('CHECKING_DOWNLOADS')
            prepare_batch(download, batch, previous)
            old_ledger = read(previous/'ledger.json')
            timing = read(batch/'reconciled/timing.json')
            raw = ca.build(batch/'reconciled', timing=timing, resolve_identities=False)
            old_results = read(previous/'written_queue/combined_results.json', [])
            retained, todo = select_work(batch/'reconciled', raw, old_results)
            print(f'{len(retained)} existing assignment results retained; {len(todo)} new/unfinished receipts to check.', flush=True)
            if check_only:
                status('CHECKED'); return {'retained':len(retained), 'to_check':len(todo)}
            if renderer is render: preflight_workbook()
            status('GRADING')
            new_results = grader(batch, todo)
            results = {r['response_id']:r for r in retained}
            results.update({r['response_id']:r for r in new_results})
            write(batch/'written_queue/combined_results.json', list(results.values()))
            # Review context for retained AI decisions remains available.
            old_text = read(previous/'written_text/prepared.json', {})
            old_text.update(read(batch/'written_text/prepared.json', {})); write(batch/'written_text/prepared.json', old_text)
            raw_ids = {r['response_id'] for r in raw['attempts']}
            extras = [r for r in old_ledger['attempts'] if r['assessment'] not in EARLY and r['response_id'] not in raw_ids]
            ledger = ca.build(batch/'reconciled', batch/'written_queue/combined_results.json', timing, retained_attempts=extras)
            old_ids = {r['response_id'] for r in old_ledger['attempts']}
            new_ids = {r['response_id'] for r in ledger['attempts']}
            if not old_ids <= new_ids: raise ValueError('Receipt history would shrink; existing workbook preserved.')
            if len(new_ids)!=len(ledger['attempts']): raise ValueError('Duplicate receipt in rebuilt ledger')
            write(batch/'ledger.json', ledger)
            summary = {'new_receipts':len(new_ids-old_ids), 'retained_assignment_results':len(retained),
                       'checked_assignment_receipts':len(todo), 'current_statuses':dict(collections.Counter(r['status'] for r in ledger['current']))}
            write(batch/'summary.json', summary)
            status('BUILDING_WORKBOOK'); renderer(batch)
            status('READY'); publish(private, batch)
            print('Complete. Workbook: '+str(private/BOOK), flush=True)
            return summary
        except BaseException as exc:
            # READY publication has its own recoverable journal; do not invalidate it.
            if not (private/'refresh_publish.json').exists(): write(batch/'status.json', {'state':'STOPPED','error':str(exc)[:1000]})
            print('Stopped safely. Previous published marks are retained. Fix the error and repeat the same command.', file=sys.stderr)
            raise


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('download_folder',help='One grading ZIP (or legacy download folder)');p.add_argument('--check',action='store_true',help='Validate downloads without running graders or replacing marks')
    args=p.parse_args()
    try:
        summary=refresh(args.download_folder, check_only=args.check)
        if not args.check:
            pending=sum(n for state,n in summary['current_statuses'].items() if state!='GRADED')
            print(f"New receipts: {summary['new_receipts']}. Current submitted records needing review: {pending}. See Review needed in Excel.")
    except Exception as exc: print('ERROR: '+str(exc), file=sys.stderr); return 1
    return 0

if __name__=='__main__': sys.exit(main())
