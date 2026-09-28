"""Trusted evaluator and Docker boundary for untrusted notebook execution.

The container receives only notebook/data/public practice code. Hidden specs,
marks, output files, Docker socket and host credentials are never mounted.
Student responses are data, not trusted grade reports. No Python object
serialization or execution occurs in the parent.
"""
import json
import os
from pathlib import Path
import selectors
import shutil
import subprocess
import sys
import time
import uuid

IMAGE = 'iuea-notebooks:2026.09'
HERE = Path(__file__).resolve().parent
MAX_MESSAGE = 8 * 1024 * 1024


def preflight():
    if not shutil.which('docker'):
        raise RuntimeError('Install/start Docker Desktop, then build the grader image.')
    result = subprocess.run(['docker', 'image', 'inspect', IMAGE], capture_output=True, timeout=20)
    if result.returncode:
        raise RuntimeError('Start Docker, then run: docker build -t %s %s' % (IMAGE, HERE))
    import pandas  # trusted reconstruction of bounded DataFrame/Series data


class PlotEvidence(dict):
    """Marker for a Figure extracted by the worker, not a submitted metadata dict."""


def decode(value, depth=0):
    if depth > 16:
        raise ValueError('Answer nesting exceeds limit')
    if isinstance(value, list):
        return [decode(v, depth+1) for v in value]
    if not isinstance(value, dict):
        return value
    kind = value.get('type')
    if kind == 'nonfinite':
        if value.get('value') not in ('nan', 'inf', '-inf'):
            raise ValueError('Invalid numeric encoding')
        return float(value['value'])
    if kind == 'figure':
        return PlotEvidence(plot_axes=decode(value['axes'],depth+1))
    if kind == 'mapping':
        return {decode(k, depth+1): decode(v, depth+1) for k, v in value['items']}
    import pandas as pd
    if kind == 'frame':
        return pd.DataFrame(decode(value['data'], depth+1), columns=decode(value['columns'], depth+1), index=decode(value['index'], depth+1))
    if kind == 'series':
        return pd.Series(decode(value['data'], depth+1), index=decode(value['index'], depth+1))
    if kind == 'array':
        import numpy as np
        return np.array(decode(value['data'], depth+1))
    raise ValueError('Unsupported answer encoding')


class Worker:
    def __init__(self, work, timeout):
        self.deadline = time.monotonic() + timeout
        self.name = 'iuea-' + uuid.uuid4().hex
        self.buffer = b''
        self.proc = subprocess.Popen([
            'docker', 'run', '--rm', '--name', self.name, '-i', '--network=none',
            '--read-only', '--cap-drop=ALL', '--security-opt=no-new-privileges',
            '--pids-limit=64', '--memory=1g', '--cpus=1', '--user=65534:65534',
            '--tmpfs=/tmp:rw,noexec,nosuid,size=128m',
            '--tmpfs=/work:rw,nosuid,size=256m,uid=65534,gid=65534',
            '--mount', 'type=bind,src=%s,dst=/inputs,readonly' % Path(work).resolve(),
            '--mount', 'type=bind,src=%s,dst=/worker.py,readonly' % (HERE/'isolated_worker.py'),
            IMAGE, 'python', '-u', '/worker.py'], stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=0)
        self.selector = selectors.DefaultSelector()
        self.selector.register(self.proc.stdout, selectors.EVENT_READ)

    def request(self, **request):
        self.proc.stdin.write((json.dumps(request, allow_nan=False)+'\n').encode())
        deadline = min(self.deadline, time.monotonic() + request.get('timeout', 20) + 10)
        while b'\n' not in self.buffer:
            remaining = deadline - time.monotonic()
            if remaining <= 0 or not self.selector.select(remaining):
                raise TimeoutError('Notebook execution exceeded time limit')
            chunk = os.read(self.proc.stdout.fileno(), 65536)
            if not chunk:
                raise RuntimeError('Notebook worker stopped without an answer')
            self.buffer += chunk
            if len(self.buffer) > MAX_MESSAGE:
                raise ValueError('Notebook response exceeds 8 MiB')
        line, self.buffer = self.buffer.split(b'\n', 1)
        reply = json.loads(line, parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
        if not isinstance(reply, dict):
            raise ValueError('Invalid worker response')
        if 'error' in reply:
            raise RuntimeError(str(reply['error'])[:500])
        return reply['value']

    def close(self):
        subprocess.run(['docker', 'rm', '-f', self.name], capture_output=True, timeout=20)
        self.proc.kill()
        self.proc.wait(timeout=10)
        self.selector.close()
        self.proc.stdin.close()
        self.proc.stdout.close()


class Namespace:
    def __init__(self, worker, per_call):
        self.worker, self.per_call = worker, per_call
        self.cache = {}

    def get(self, name, default=None):
        if name not in self.cache:
            value = self.worker.request(op='get', name=name)
            if isinstance(value, dict) and value.get('type') == 'callable':
                def remote(*args):
                    return decode(self.worker.request(op='call', name=name, args=args, timeout=self.per_call,
                        preserve_arguments=name in ('clean_records','normalise_orders','clean_line_items','audit_cleaning')))
                self.cache[name] = remote
            else:
                self.cache[name] = decode(value)
        value = self.cache[name]
        return default if isinstance(value, str) and value == '__MISSING__' else value


def evaluate(work, spec_path, hidden_path, assignment, cohort, per_cell, total_timeout):
    import iuea_grader as ig
    spec = ig.load_spec(assignment, spec_path, include_hidden=True, hidden_path=hidden_path)
    worker = Worker(work, total_timeout)
    try:
        meta = worker.request(op='init', timeout=total_timeout, cell_timeout=per_cell)
        if not isinstance(meta, dict):
            raise ValueError('Invalid execution metadata')
        declared = str(meta.get('cohort', ''))
        if cohort and declared and cohort != declared:
            raise ValueError('Submitted COHORT differs from selected cohort')
        use_cohort = cohort or declared or getattr(spec, 'DEFAULT_COHORT', '')
        questions = ig.resolve_questions(spec, use_cohort)
        if any(not callable(q.get('check')) for _, q in questions):
            raise ValueError('Incomplete marking specification')
        ns = Namespace(worker, per_cell)
        ns.cache['COHORT'] = use_cohort
        result = {k: meta.get(k, default) for k, default in [
            ('cells_total', 0), ('cells_ok', 0), ('cell_errors', []), ('declared_sid', '')]}
        result.update(cohort=use_cohort, status='ERRORS' if result['cell_errors'] else 'OK', questions={})
        for qid, question in questions:
            checked = ig.run_check(qid, question, ns)
            result['questions'][qid] = dict(ok=checked.ok, awarded=checked.awarded,
                marks=checked.marks, msg=checked.message, visible=bool(question.get('visible', True)), err=checked.error)
        result['fingerprint'] = ig.answer_fingerprint(questions, ns)
        return result
    finally:
        worker.close()
