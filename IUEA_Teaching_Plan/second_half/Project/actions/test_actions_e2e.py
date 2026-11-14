"""End-to-end proof of the collection design of 14 November 2026 (no Submit step), with no network.

    python3 actions/test_actions_e2e.py        (Docker running, image iuea-notebooks:colab-2026.11 built; node on PATH or NODE=...)

The portal, gateway and collector are the REAL deploy/ files, run by local_stack.mjs on in-memory fakes of Sheets and Drive (files,
permissions, revisions with modifiedTime). Colab is simulated: an autosave is a new Drive revision by the student's account (refused without
edit rights), and a backup is what the setup cell's thread sends (the notebook on screen without its data block, and the address of the open
file). The every-minute trigger is called at chosen times. The Actions job is the real actions_grade.py in Docker. Identities are made up.
"""
import json
import os
import secrets
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
import zipfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
sys.path.insert(0, str(PROJECT / 'tools'))
NODE = os.environ.get('NODE', shutil.which('node') or '/Users/jothamwambi/.nvm/versions/node/v24.14.0/bin/node')
IMAGE = os.environ.get('IUEA_NOTEBOOK_IMAGE', 'iuea-notebooks:colab-2026.11')
P12, P13 = 'CML3112|ML_PROJECT', 'CML3113|ML_PROJECT'
PEOPLE = {   # registration: (course, name, email)
    'A': ('26/E2E/001/AAA', 'CML3112', 'Test Learner Alpha', 'alpha@example.org'),     # ordinary: saves, checks, collected at the deadline
    'B': ('26/E2E/002/BBB', 'CML3112', 'Test Learner Beta', 'beta@example.org'),       # saved a copy and worked in it
    'C': ('26/E2E/003/CCC', 'CML3112', 'Test Learner Gamma', 'gamma@example.org'),     # laptop died at minute 170
    'D': ('26/E2E/004/DDD', 'CML3112', 'Test Learner Delta', 'delta@example.org'),     # never pressed anything
    'E': ('26/E2E/005/EEE', 'CML3112', 'Test Learner Epsilon', 'eps@example.org'),     # pressed Start, then nothing
    'F': ('26/E2E/006/FFF', 'CML3112', 'Test Learner Zeta', 'zeta@example.org'),       # a backup after the deadline
    'G': ('26/E2E/007/GGG', 'CML3112', 'Test Learner Eta', 'eta@example.org'),         # stopped the backup thread; later a one-student extension
    'H': ('26/E2E/008/HHH', 'CML3112', 'Test Learner Theta', 'theta@example.org'),     # the wrong Google account
    'I': ('26/E2E/009/III', 'CML3112', 'Test Learner Iota', 'iota@example.org'),       # I have finished
    'K': ('26/E2E/011/KKK', 'CML3113', 'Test Learner Kappa', 'kappa@example.org'),     # whole-class (course) extension
    'R': ('26/E2E/010/JJJ', 'CML3112', 'Test Learner Rho', 'rho@example.org'),         # the rehearsal
}
results = []


def check(name, ok, detail=''):
    results.append((name, bool(ok), str(detail)[:220]))
    print(('PASS  ' if ok else 'FAIL  ') + name + (f'  [{str(detail)[:220]}]' if detail else ''))


class Stack:
    def __init__(self, port, env):
        self.base = f'http://127.0.0.1:{port}'
        self.proc = subprocess.Popen([NODE, str(HERE / 'local_stack.mjs'), str(port)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
        assert 'LOCAL STACK READY' in self.proc.stdout.readline()

    def call(self, route, body=None, origin=True):
        headers = {'Content-Type': 'application/json'}
        if origin:
            headers['Origin'] = self.base
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(self.base + route, data=data, headers=headers, method='POST' if data is not None else 'GET')
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return r.status, json.loads(r.read())
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read() or b'{}')

    def at(self, minutes):
        self.call('/admin/clock', dict(offset_ms=int(minutes * 60000)))


def solved(issued, code, broken=False):
    sol = json.loads((PROJECT / 'grader_spec/solutions' / code / 'ML_PROJECT_solution.ipynb').read_text())
    nb = json.loads(json.dumps(issued))
    assert len(nb['cells']) == len(sol['cells']), (len(nb['cells']), len(sol['cells']))
    for i, (a, b) in enumerate(zip(nb['cells'], sol['cells'])):
        if i in (0, 1, 3) or i >= len(nb['cells']) - 1:
            continue
        a['source'] = b['source']
        if broken and ''.join(b['source']).startswith('def regression_errors'):
            a['source'] = [''.join(b['source']).replace('float(np.sqrt(np.mean(residuals ** 2)))', 'float(np.mean(residuals ** 2))')]   # RMSE without the root
    return nb


def as_backup(nb):
    """What the setup cell's thread sends: the notebook on screen with the data block left out."""
    import project_content as PC
    packed = PC.packed_data()
    out = json.loads(json.dumps(nb))
    for c in out['cells']:
        text = ''.join(c['source']) if isinstance(c['source'], list) else c['source']
        if '# IUEA-SETUP-CELL' in text:
            c['source'] = text.replace(packed, '__IUEA_PACKED_DATA__')
    return json.dumps(out)


def main():
    with socket.socket() as s:
        s.bind(('127.0.0.1', 0))
        port = s.getsockname()[1]
    env = dict(os.environ, COLLECTOR_SECRET=secrets.token_hex(24), IUEA_NOTEBOOK_IMAGE=IMAGE)
    st = Stack(port, env)
    graded = set()

    def run_jobs():
        state = st.call('/admin/state')[1]
        for d in state['dispatches']:
            sid = d['payload']['client_payload']['submission_id']
            if sid in graded:
                continue
            graded.add(sid)
            done = subprocess.run([sys.executable, str(HERE / 'actions_grade.py'), '--submission-id', sid, '--collector-url', st.base + '/collector', '--image', IMAGE],
                                  capture_output=True, text=True, env=env)
            if done.returncode:
                print(done.stdout[-800:], done.stderr[-800:])
        return st.call('/admin/state')[1]

    try:
        t0 = datetime.now(timezone.utc)
        roster_rows = [[c, r, n] for r, c, n, _ in PEOPLE.values()] + [['CML3113', '99/999/OTHER-X', 'Other Course Learner']]
        st.call('/admin/setup', dict(open=(t0 - timedelta(hours=1)).isoformat(), close=(t0 + timedelta(days=2)).isoformat(), classList=[]))
        csv_text = 'student_id,name,course\n' + '\n'.join(f'{r},{n},{c}' for c, r, n in roster_rows)
        _, r = st.call('/admin/classlist', dict(csv=csv_text))
        check('class list: loaded by the script function from a gradebook CSV (made-up rows)', len(r['rows']) == len(roster_rows) + 1)
        state = st.call('/admin/state')[1]
        check('setup: the every-minute deadline trigger is installed once', state['triggers'] == ['mlpSweep'])

        # the entry page
        _, r = st.call('/api/check', dict(test=P12, registration='26/e2e/001/aaa'))
        check('entry page: a registration on the list shows the name to confirm', r.get('ok') and r['result']['nameHint'] == 'Test L. A.', r)
        _, r = st.call('/api/check', dict(test=P12, registration='26/E2E/011/KKK'))
        check('wrong-course registration: refused with the right course named', not r.get('ok') and 'CML3113 class list' in r['error'], r.get('error'))
        _, r = st.call('/api/files', dict(test=P12, name='x', email='kappa@example.org', registration='26/E2E/011/KKK'))
        check('wrong-course registration: no notebook is issued', not r.get('ok') and 'CML3113' in r.get('error', ''), r.get('error'))

        issued, attempt, fileid = {}, {}, {}
        st.at(0)
        for k, (reg, course, name, mail) in PEOPLE.items():
            if k == 'D':
                continue
            key = course + ('|ML_REHEARSAL' if k == 'R' else '|ML_PROJECT')
            _, r = st.call('/api/files', dict(test=key, name='typed name ignored', email=mail, registration=reg))
            assert r.get('ok'), (k, r)
            issued[k] = json.loads(r['result']['notebook'])
            attempt[k] = r['result']['attempt']
            fileid[k] = r['result']['colabUrl'].rsplit('/', 1)[1]
        state = st.call('/admin/state')[1]
        a_row = [x for x in state['allocations'] if x[3] == attempt['A']][0]
        check('Start: the notebook is a Drive file shared with the Google email as an editor, recorded against the allocation',
              a_row[9] == fileid['A'] and state['perms'][fileid['A']] == [{'email': 'alpha@example.org', 'role': 'writer'}])
        ident = ''.join(issued['A']['cells'][1]['source'])
        check('the identity cell is information only: name from the class list, the allocation code, no token, no deadline logic',
              'FULL_NAME = "Test Learner Alpha"' in ident and '_IUEA_ALLOCATION = ' in ident and '_IUEA_TOKEN' not in json.dumps(issued['A'])
              and not any('iuea-submission' in c['metadata'].get('tags', []) for c in issued['A']['cells']))
        check('the countdown reminds the student to press Ctrl+S at 30 and 10 minutes', '30 minutes or less left: press Ctrl+S now' in ident and '10 minutes or less left' in ident)

        # the wrong Google account
        _, r = st.call('/api/files', dict(test=P12, name='x', email='someone.else@example.org', registration=PEOPLE['H'][0]))
        check('wrong account: the same registration with another Google email is refused', not r.get('ok') and 'do not match' in r.get('error', ''), r.get('error'))
        code, r = st.call('/admin/save', dict(file=fileid['H'], email='someone.else@example.org', notebook=json.dumps(issued['H'])))
        check('wrong account: Colab signed in as another account cannot save to the issued notebook', code == 403)

        _, r = st.call('/collector', dict(action='bootstrap', key='guess', properties=dict(GITHUB_TOKEN='x')), origin=False)
        check('bootstrap: without the one-time file pushed by the setup script the route refuses', not r.get('ok'), r)
        # the wrong account, fixed by the lecturer in one line: a fresh attempt with the right email
        _, r = st.call('/admin/fresh', dict(registration=PEOPLE['H'][0], reason='typed the wrong Google account (test)', email='theta.right@example.org'))
        _, r2 = st.call('/api/files', dict(test=P12, name='x', email='theta.right@example.org', registration=PEOPLE['H'][0]))
        state = st.call('/admin/state')[1]
        new_file = r2['result']['colabUrl'].rsplit('/', 1)[1] if r2.get('ok') else ''
        check('wrong account: one call gives a fresh attempt; the new notebook is shared with the right account and the old one is read only',
              r['changed'] == 1 and r2.get('ok') and state['perms'][new_file] == [{'email': 'theta.right@example.org', 'role': 'writer'}] and state['perms'][fileid['H']][0]['role'] == 'reader', r2.get('error'))
        if r2.get('ok'):
            attempt['H'], fileid['H'], issued['H'] = r2['result']['attempt'], new_file, json.loads(r2['result']['notebook'])

        # minute 10: B saves a copy and works in it
        st.at(10)
        _, r = st.call('/admin/copy', dict(file=fileid['B'], email='beta@example.org'))
        copy_b = r['file']
        # minute 50 to 55: I finishes early
        st.at(50)
        st.call('/admin/save', dict(file=fileid['I'], email='iota@example.org', notebook=json.dumps(solved(issued['I'], 'CML3112'))))
        code, r = st.call('/api/finish', dict(attempt=attempt['I']), origin=False)
        check('I have finished: only the entry page itself can ask (same origin)', code == 403)
        st.at(55)
        _, r = st.call('/api/finish', dict(attempt=attempt['I']))
        check('I have finished: collected at once, from the saved notebook', r.get('ok') and r['result']['state'] == 'collected' and 'saved notebook' in r['result']['collected']['source'], r)
        code, _ = st.call('/admin/save', dict(file=fileid['I'], email='iota@example.org', notebook=json.dumps(issued['I'])))
        state = st.call('/admin/state')[1]
        check('I have finished: editing stops (read only), so a later save is refused', code == 403 and state['perms'][fileid['I']][0]['role'] == 'reader')

        # minute 60: A saves, backs up and uses Check my work
        st.at(60)
        a_nb = solved(issued['A'], 'CML3112')
        st.call('/admin/save', dict(file=fileid['A'], email='alpha@example.org', notebook=json.dumps(a_nb)))
        code, r = st.call('/api/backup', dict(attempt=attempt['A'], href='https://colab.research.google.com/drive/' + fileid['A'] + '#scrollTo=x', notebook=as_backup(a_nb)), origin=False)
        check('backup: sent from Colab (no Origin), timestamped by the server, the issued file', code == 200 and r['result']['on_time'] and not r['result']['other_file'], r)
        _, r = st.call('/api/mywork', dict(attempt=attempt['A']))
        check('Check my work: the saved notebook is sent for the structural checks', r.get('ok') and r['result']['pending'], r)
        _, r2 = st.call('/api/mywork', dict(attempt=attempt['A']))
        check('Check my work: at most one check every two minutes', not r2.get('ok') and 'two minutes' in r2.get('error', ''), r2.get('error'))
        state = run_jobs()
        _, r = st.call('/api/status', dict(attempt=attempt['A']))
        ca = r['result']['checks'] or {}
        check('Check my work: the page shows runs from the top, functions and MEMO found, the issued file, and no mark',
              ca.get('runs_from_top') and not ca.get('missing_functions') and ca.get('memo_found') and ca.get('issued_file') and r['result']['mark'] is None, ca)

        # minute 90: G works with the backup thread stopped (no backups at all)
        st.at(90)
        st.call('/admin/save', dict(file=fileid['G'], email='eta@example.org', notebook=json.dumps(solved(issued['G'], 'CML3112'))))
        # minute 100: B in the copy; F's work has one broken cell
        st.at(100)
        b_nb = solved(issued['B'], 'CML3112')
        st.call('/admin/save', dict(file=copy_b, email='beta@example.org', notebook=json.dumps(b_nb)))
        _, r = st.call('/api/backup', dict(attempt=attempt['B'], href='https://colab.research.google.com/drive/' + copy_b, notebook=as_backup(b_nb)), origin=False)
        check('saved a copy: the backup still arrives and the server says it is another file (the cell shows the warning)', r.get('ok') and r['result']['other_file'], r)
        f_nb = solved(issued['F'], 'CML3112', broken=True)
        st.call('/admin/save', dict(file=fileid['F'], email='zeta@example.org', notebook=json.dumps(f_nb)))
        st.call('/api/backup', dict(attempt=attempt['F'], href='https://colab.research.google.com/drive/' + fileid['F'], notebook=as_backup(f_nb)), origin=False)
        # minute 160 to 165: C's last save and last backup, then the laptop dies
        st.at(160)
        c_nb = solved(issued['C'], 'CML3112')
        st.call('/admin/save', dict(file=fileid['C'], email='gamma@example.org', notebook=json.dumps(c_nb)))
        st.at(165)
        st.call('/api/backup', dict(attempt=attempt['C'], href='https://colab.research.google.com/drive/' + fileid['C'], notebook=as_backup(c_nb)), origin=False)
        # K works normally in CML3113; minute 170: the lecturer extends the whole CML3113 class by 30 minutes
        st.call('/admin/save', dict(file=fileid['K'], email='kappa@example.org', notebook=json.dumps(solved(issued['K'], 'CML3113'))))
        st.at(170)
        _, r = st.call('/admin/extend', dict(who='CML3113', minutes=30, reason='portal outage at 14:00 (test)'))
        state = st.call('/admin/state')[1]
        win13 = [w for w in state['windows'] if w[0] == P13][0]
        check('whole-class extension: one call moves every CML3113 deadline and the window close, and is logged', r['changed'] == 1 and any(x[1] == 'CML3113' for x in state['extensions'])
              and datetime.fromisoformat(win13[2].replace('Z', '+00:00')) > t0 + timedelta(days=2), r)

        # minute 181: the trigger collects everyone past the deadline
        st.at(181)
        _, r = st.call('/admin/sweep', {})
        state = st.call('/admin/state')[1]
        rows = {x[6]: x for x in state['collection'][1:] if x[10] == 'COLLECTED'}
        reg = lambda k: PEOPLE[k][0]
        check('deadline: the trigger collects every project attempt past its deadline and none before',
              set(rows) == {reg(k) for k in 'ABCEFGHI'} and reg('K') not in rows and reg('R') not in rows, sorted(rows))
        check('deadline: editing stops (read only); the newer of the last save and the last backup is used', state['perms'][fileid['A']][0]['role'] == 'reader' and rows[reg('A')][13] in ('drive-revision', 'backup'), rows[reg('A')][14])
        check('saved a copy: the newest on-time backup is marked, with the source on the row', rows[reg('B')][13] == 'backup' and 'another file' in rows[reg('B')][14], rows[reg('B')][14])
        check('laptop died at minute 170: the newest of the last save (minute 160) and the last backup (minute 165) is collected',
              rows[reg('C')][13] == 'backup' and 'last saved' in rows[reg('C')][14], rows[reg('C')][14])
        check('stopped the backup thread: the last Drive save is collected', rows[reg('G')][13] == 'drive-revision')
        check('pressed Start and nothing else: the issued notebook is collected (it will mark 0)', rows[reg('E')][13] == 'drive-revision')
        check('never pressed anything: no allocation, nothing collected', reg('D') not in rows and not any(x[1] == reg('D') for x in state['allocations']))
        # minute 185: F's late backup with the fixed cell
        st.at(185)
        _, r = st.call('/api/backup', dict(attempt=attempt['F'], href='https://colab.research.google.com/drive/' + fileid['F'], notebook=as_backup(solved(issued['F'], 'CML3112'))), origin=False)
        check('a backup after the deadline is kept and not used', r.get('ok') and r['result']['on_time'] is False and r['result']['closed'], r)
        # minute 186: a one-student extension for G after collection; G keeps working; collected again at the new deadline
        st.at(186)
        st.call('/admin/extend', dict(who=reg('G'), minutes=20, reason='laptop failure reported with a screenshot (test)'))
        state = st.call('/admin/state')[1]
        check('one-student extension: the attempt is opened again (editing restored) without touching any sheet by hand',
              state['perms'][fileid['G']][0]['role'] == 'writer' and any(x[6] == reg('G') and x[10] == 'SUPERSEDED' for x in state['collection']))
        st.call('/admin/save', dict(file=fileid['G'], email='eta@example.org', notebook=json.dumps(solved(issued['G'], 'CML3112'))))
        st.at(201)
        st.call('/admin/sweep', {})
        st.at(211)
        st.call('/admin/sweep', {})
        state = run_jobs()
        rows = {x[6]: x for x in state['collection'][1:] if x[10] == 'COLLECTED'}
        check('whole-class extension: K is collected only after the extended deadline', reg('K') in rows and rows[reg('K')][7] > rows[reg('A')][7])
        check('one-student extension: G is collected again at the new deadline', reg('G') in rows)

        # the rehearsal: never locked, never marked, checks always shown
        st.at(60)
        r_nb = issued['R']        # the rehearsal has its own target; the unfinished notebook is enough to practise the flow
        st.call('/admin/save', dict(file=fileid['R'], email='rho@example.org', notebook=json.dumps(r_nb)))
        st.at(300)
        st.call('/admin/sweep', {})
        _, r = st.call('/api/finish', dict(attempt=attempt['R']))
        state = run_jobs()
        _, r = st.call('/api/status', dict(attempt=attempt['R']))
        check('rehearsal: never locked (still an editor after the deadline and after I have finished) and nothing in Collection',
              state['perms'][fileid['R']][0]['role'] == 'writer' and not any(x[6] == reg('R') for x in state['collection']))
        check('rehearsal: the checks are shown at once and there is never a mark', (r['result']['checks'] or {}).get('runs_from_top') and r['result']['mark'] is None and r['result']['rehearsal'], r['result'])

        # marks hidden until release and the window close
        _, r = st.call('/api/status', dict(attempt=attempt['A']))
        check('no mark before the release switch', r['result']['mark'] is None and r['result']['state'] == 'collected')
        st.call('/admin/release', {})
        _, r = st.call('/api/status', dict(attempt=attempt['A']))
        check('release switch on, window still open: still no mark', r['result']['mark'] is None)
        st.at(3 * 24 * 60)
        _, r = st.call('/api/status', dict(attempt=attempt['A']))
        check('release switch on and window closed: the mark is shown', r['result']['mark'] and 'total 45' in r['result']['mark'], r['result']['mark'])

        # the final run on the Mac, from the real exportMlProjectBatch
        _, ex = st.call('/admin/export')
        work = Path(tempfile.mkdtemp(prefix='final_'))
        with zipfile.ZipFile(work / 'batch.zip', 'w') as z:
            for f in ex['files']:
                z.writestr(f['name'], f['text'])
        (work / 'roster.csv').write_text('student_id\n' + '\n'.join(p[0] for p in PEOPLE.values() if p[1] in ('CML3112', 'CML3113')) + '\n')
        done = subprocess.run([sys.executable, str(HERE / 'final_regrade.py'), '--zip', str(work / 'batch.zip'), '--out', str(work / 'out'), '--image', IMAGE, '--roster', str(work / 'roster.csv')],
                              capture_output=True, text=True, env=env)
        print(done.stdout[-900:])
        res = {r_['registration']: r_ for r_ in __import__('csv').DictReader(open(work / 'out/ML_PROJECT_results.csv'))} if (work / 'out/ML_PROJECT_results.csv').exists() else {}
        total = lambda k: float(res[reg(k)]['project_total']) if reg(k) in res else None
        flags = lambda k: res[reg(k)]['flags'].split() if reg(k) in res else []
        check('final run: one command re-grades, writes the gradebook files and agrees with Actions', done.returncode == 0 and 'DIFFERENT' not in done.stdout and (work / 'out/gradebook').is_dir(), done.stderr[-300:])
        check('marks: full work collected from a save or a backup earns 45 (A, B, C, G, I, K)', all(total(k) == 45 for k in 'ABCGIK'), {k: total(k) for k in 'ABCGIK'})
        check('marks: the mistake collected at the deadline costs marks; the corrected late backup does not count (F)', total('F') is not None and total('F') < 45, total('F'))
        check('marks: Start and nothing else earns 0 and is flagged NO_WORK (E, H)', total('E') == 0 and 'NO_WORK' in flags('E') and total('H') == 0, (total('E'), total('H')))
        check('spot-check list: the source and time are listed with no action needed (backup, other file, late backup)',
              'COLLECTED_FROM_BACKUP' in flags('B') and 'WORKED_IN_OTHER_FILE' in flags('B') and 'COLLECTED_FROM_BACKUP' in flags('C') and 'LATE_BACKUP_IGNORED' in flags('F') and res[reg('B')]['source'] == 'backup',
              {k: flags(k) for k in 'BCF'})
        gb = {r_['student_id']: r_ for r_ in __import__('csv').DictReader(open(work / 'out/gradebook/ML_Project_Part_A_import.csv'))} if (work / 'out/gradebook/ML_Project_Part_A_import.csv').exists() else {}
        check('never pressed anything: 0 and 0 in the gradebook files (no submission)', gb.get(reg('D'), {}).get('score') == '0', gb.get(reg('D')))
    finally:
        st.proc.terminate()
    bad = [n for n, ok, _ in results if not ok]
    print(f'\n{len(results) - len(bad)} of {len(results)} pipeline checks pass.')
    (HERE / 'e2e_results.txt').write_text('\n'.join(('PASS  ' if ok else 'FAIL  ') + n + (f'  [{d}]' if d else '') for n, ok, d in results) +
                                          f'\n\n{len(results) - len(bad)} of {len(results)} pipeline checks pass (image {IMAGE}).\n')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
