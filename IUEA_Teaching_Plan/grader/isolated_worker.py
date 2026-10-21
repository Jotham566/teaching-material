"""Untrusted notebook execution service. Contains NO grading decisions or keys.
Only bounded JSON values cross to the trusted evaluator. Never use pickle.
"""
import contextlib
import io
import json
import signal
import sys
import math
import shutil
import types
from pathlib import Path
shutil.copytree("/inputs", "/work", dirs_exist_ok=True)
sys.path.insert(0, "/work")

# The lecturer has already supplied the CSVs in this isolated directory.
# Reproduce Colab's upload return value without opening a browser or network.
google_module=types.ModuleType('google')
google_module.__path__=[]
colab_module=types.ModuleType('google.colab')
files_module=types.ModuleType('google.colab.files')
def supplied_csv_upload():
    return {p.name:p.read_bytes() for p in sorted(Path('/inputs').glob('*.csv'))}
def no_browser_download(filename):
    if not Path(filename).is_file():raise FileNotFoundError(filename)
files_module.upload=supplied_csv_upload
files_module.download=no_browser_download
colab_module.files=files_module
google_module.colab=colab_module
sys.modules['google']=google_module
sys.modules['google.colab']=colab_module
sys.modules['google.colab.files']=files_module

protocol = sys.stdout
ns = {"__name__": "__main__"}


def encode(value, depth=0):
    if depth > 12:
        raise ValueError("Answer nesting exceeds limit")
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        return value if math.isfinite(value) else {"type": "nonfinite", "value": str(value)}
    if callable(value):
        return {"type": "callable"}
    if isinstance(value, (list, tuple)):
        if len(value) > 200000:
            raise ValueError("Answer exceeds limit")
        return [encode(v, depth + 1) for v in value]
    if isinstance(value, dict):
        return {"type": "mapping", "items": [[encode(k, depth + 1), encode(v, depth + 1)] for k, v in value.items()]}
    import pandas as pd
    import numpy as np
    if isinstance(value, pd.DataFrame):
        return {"type": "frame", "columns": encode(list(value.columns), depth+1),
                "index": encode(list(value.index), depth+1), "data": encode(value.to_numpy().tolist(), depth+1)}
    if isinstance(value, pd.Series):
        return {"type": "series", "index": encode(list(value.index), depth+1), "data": encode(value.tolist(), depth+1)}
    if isinstance(value, np.ndarray):
        return {"type": "array", "data": encode(value.tolist(), depth+1)}
    from matplotlib.figure import Figure
    if isinstance(value, Figure):
        axes=[]
        for ax in value.axes:
            axes.append(dict(title=ax.get_title(),xlabel=ax.get_xlabel(),ylabel=ax.get_ylabel(),
                lines=[dict(x=line.get_xdata().tolist() if hasattr(line.get_xdata(),'tolist') else list(line.get_xdata()),y=line.get_ydata().tolist() if hasattr(line.get_ydata(),'tolist') else list(line.get_ydata())) for line in ax.lines],
                scatter=[collection.get_offsets().tolist() for collection in ax.collections if hasattr(collection,'get_offsets')],
                bars=[dict(x=patch.get_x(),width=patch.get_width(),height=patch.get_height()) for patch in ax.patches if hasattr(patch,'get_height')],
                xticklabels=[t.get_text() for t in ax.get_xticklabels()]))
        return {'type':'figure','axes':encode(axes,depth+1)}
    if isinstance(value, np.generic):
        return encode(value.item(), depth+1)
    raise TypeError("Unsupported answer type: " + type(value).__name__)


def alarm(*_):
    raise TimeoutError("Cell or function exceeded time limit")


def execute(request):
    if request['op'] == 'init':
        nb = json.load(open('/work/submission.ipynb'))
        if not isinstance(nb.get('cells'), list):
            raise ValueError('Notebook has no cells list')
        errors, total, ok = [], 0, 0
        for index, cell in enumerate(nb['cells']):
            if cell.get('cell_type') != 'code' or 'autograde-skip' in cell.get('metadata', {}).get('tags', []):
                continue
            source = cell.get('source', '')
            source = ''.join(source) if isinstance(source, list) else source
            source = '\n'.join('# notebook magic omitted' if line.lstrip().startswith(('%', '!', '?')) else line for line in source.splitlines())
            if not source.strip():
                continue
            total += 1
            signal.alarm(request.get('cell_timeout',20))
            try:
                exec(compile(source, '<cell %s>' % (index+1), 'exec'), ns)
                ok += 1
            except BaseException as exc:
                errors.append({'cell': index+1, 'etype': type(exc).__name__, 'emsg': str(exc)[:300]})
            finally:
                signal.alarm(0)
        return {'cells_total': total, 'cells_ok': ok, 'cell_errors': errors,
                'declared_sid': str(ns.get('STUDENT_ID', ''))[:512], 'cohort': str(ns.get('COHORT', ''))[:30]}
    if request['op'] == 'get':
        return encode(ns.get(request['name'], '__MISSING__'))
    if request['op'] == 'call':
        signal.alarm(request['timeout'])
        try:
            before=json.dumps(request['args'],sort_keys=True) if request.get('preserve_arguments') else None
            value=ns[request['name']](*request['args'])
            if before is not None and json.dumps(request['args'],sort_keys=True)!=before:
                raise ValueError('This interface must preserve its input records')
            return encode(value)
        finally:
            signal.alarm(0)
    raise ValueError('Unknown operation')

signal.signal(signal.SIGALRM, alarm)
for line in sys.stdin:
    try:
        request = json.loads(line)
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            result = execute(request)
        response = {'value': result}
    except BaseException as exc:
        response = {'error': type(exc).__name__ + ': ' + str(exc)[:300]}
    protocol.write(json.dumps(response, allow_nan=False) + '\n')
    protocol.flush()
