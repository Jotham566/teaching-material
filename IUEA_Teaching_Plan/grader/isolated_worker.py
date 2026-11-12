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
    if isinstance(value, np.dtype):
        return str(value)
    if isinstance(value, np.generic):
        return encode(value.item(), depth+1)
    raise TypeError("Unsupported answer type: " + type(value).__name__)


# Per-cell snapshots of the graded names (fairness mode). states[k] = (cell number,
# {name: value as it was right after that cell}); only cells that changed a watched
# name add a state. Names not yet defined at that cell are absent from the state.
states = []
_last = {}
WATCHED = []


def _fingerprint(value):
    if callable(value):
        return ('f', id(value), id(getattr(value, '__code__', None)))
    try:
        import pandas as pd
        if isinstance(value, (pd.DataFrame, pd.Series)):
            cols = tuple(map(str, getattr(value, 'columns', []))) if isinstance(value, pd.DataFrame) else ()
            return ('p', id(value), cols, value.shape, int(pd.util.hash_pandas_object(value, index=True).sum()))
    except Exception:  # noqa: BLE001
        return ('i', id(value))
    try:
        text = repr(value)
        return ('r', type(value).__name__, text if len(text) < 200000 else id(value))
    except Exception:  # noqa: BLE001
        return ('i', id(value))


def snapshot(watch, cell):
    import copy
    changed = False
    current = dict(states[-1][1]) if states else {}
    for name in watch:
        if name not in ns:
            if name in current:
                del current[name]; changed = True
            _last.pop(name, None)
            continue
        value = ns[name]
        fp = _fingerprint(value)
        if _last.get(name) == fp:
            continue
        _last[name] = fp
        if not callable(value):
            try:
                value = copy.deepcopy(value)
            except Exception:  # noqa: BLE001
                pass
        current[name] = value
        changed = True
    if changed and len(states) < 80:
        states.append((cell, current))


# Reference-input re-runs (Test 1 fairness): rerun key -> separate namespace in which
# one question's own cells ran on the lecturer's reference tables.
CELLS = {}
SHIM = []
reruns = {}


def rerun(request):
    """Run some of the notebook's own cells again in a NEW namespace: a copy of the final
    namespace without the graded names, then the evaluator's trusted preset code (the
    reference raw_data / cleaned_data), then the listed cells in order. The original
    namespace and snapshots are never changed."""
    import copy
    if len(reruns) >= 12:
        raise ValueError('Too many re-runs')
    base = {}
    for k, v in ns.items():
        if k in WATCHED:
            continue
        if isinstance(v, types.ModuleType) or callable(v) or k.startswith('__'):
            base[k] = v
            continue
        try:
            from matplotlib.figure import Figure
            from matplotlib.axes import Axes
            if isinstance(v, (Figure, Axes)):
                base[k] = v
                continue
        except Exception:  # noqa: BLE001
            pass
        try:
            base[k] = copy.deepcopy(v)
        except Exception:  # noqa: BLE001
            base[k] = v
    base['__name__'] = '__main__'
    signal.alarm(request.get('cell_timeout', 20))
    try:
        for code in request.get('preset', []):
            exec(compile(str(code), '<reference input>', 'exec'), base)
    finally:
        signal.alarm(0)
    errors, ran = [], 0
    for index in request.get('cells', []):
        source = CELLS.get(int(index))
        if source is None:
            continue
        ran += 1
        signal.alarm(request.get('cell_timeout', 20))
        try:
            drop = set(request.get('drop_assign') or [])
            tree = None
            if drop:
                # Leave out top-level `name = ...` for the names the evaluator presets.
                import ast
                try:
                    tree = ast.parse(source)
                    tree.body = [n for n in tree.body if not (isinstance(n, ast.Assign) and all(
                        isinstance(t, ast.Name) and t.id in drop for t in n.targets))]
                except SyntaxError:
                    tree = None
            if tree is not None:
                code = compile(tree, '<cell %s>' % (int(index)+1), 'exec')
            elif SHIM:
                code, _ = SHIM[0].compile_cell(source, '<cell %s>' % (int(index)+1))
            else:
                code = compile(source, '<cell %s>' % (int(index)+1), 'exec')
            exec(code, base)
        except BaseException as exc:
            errors.append({'cell': int(index)+1, 'etype': type(exc).__name__, 'emsg': str(exc)[:300]})
        finally:
            signal.alarm(0)
            if SHIM:
                SHIM[0].after_cell()
    reruns[str(request['key'])] = base
    return {'ran': ran, 'errors': errors}


def scope_for(request):
    if request.get('rerun') is not None:
        return reruns[str(request['rerun'])]
    state = request.get('state')
    if state is None:
        return ns
    merged = {k: v for k, v in ns.items() if k not in WATCHED}
    merged.update(states[int(state)][1])
    return merged


def alarm(*_):
    raise TimeoutError("Cell or function exceeded time limit")


def execute(request):
    if request['op'] == 'init':
        fair = bool(request.get('colab_shims'))
        shim = None
        if fair:
            # Colab-like sandbox (display/IPython/drive stubs, CSV aliases, cell dedent,
            # plt.close after each cell). Off unless the trusted evaluator asks for it.
            import importlib.util
            spec = importlib.util.spec_from_file_location('colab_shim', '/colab_shim.py')
            shim = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(shim)
            shim.install(ns, ('/inputs', '/work'))
            SHIM[:] = [shim]
        watch = [n for n in request.get('watch', []) if isinstance(n, str)][:64]
        WATCHED[:] = watch
        nb = json.load(open('/work/submission.ipynb'))
        if not isinstance(nb.get('cells'), list):
            raise ValueError('Notebook has no cells list')
        errors, total, ok, notes = [], 0, 0, []
        for index, cell in enumerate(nb['cells']):
            if cell.get('cell_type') != 'code':
                continue
            source = cell.get('source', '')
            source = ''.join(source) if isinstance(source, list) else source
            tags = cell.get('metadata', {}).get('tags', [])
            # Colab can discard custom tags when saving a notebook. Recognize
            # the supplied controls by their exact paired headers as well.
            headers = source.splitlines()[:10]
            timer_cell = 'iuea-timer' in tags or (
                '#@title Check details and countdown — Do not edit this cell' in headers
                and '# Do not edit this cell: identifies your attempt and preserves your timer.' in headers)
            submit_cell = (
                '#@title Submit your test — Do not edit this cell' in headers
                and '# Do not edit this cell: saves your answers and prepares the submission form.' in headers)
            if 'autograde-skip' in tags or timer_cell or submit_cell:
                if timer_cell:
                    # Read literal identity fields without executing the browser countdown.
                    import ast
                    try:
                        for statement in ast.parse(source).body:
                            if isinstance(statement, ast.Assign) and isinstance(statement.value, ast.Constant) and isinstance(statement.value.value, str):
                                for target in statement.targets:
                                    if isinstance(target, ast.Name) and target.id in ('FULL_NAME','EMAIL','STUDENT_ID','COHORT','TEST_ID'):
                                        ns[target.id] = statement.value.value[:512]
                    except SyntaxError:
                        pass
                continue
            source = '\n'.join('# notebook magic omitted' if line.lstrip().startswith(('%', '!', '?')) else line for line in source.splitlines())
            if not source.strip():
                continue
            total += 1
            CELLS[index] = source
            signal.alarm(request.get('cell_timeout',20))
            try:
                if shim is not None:
                    code, dedented = shim.compile_cell(source, '<cell %s>' % (index+1))
                    if dedented:
                        notes.append({'cell': index+1, 'note': 'cell dedented as IPython does'})
                else:
                    code = compile(source, '<cell %s>' % (index+1), 'exec')
                exec(code, ns)
                ok += 1
            except BaseException as exc:
                errors.append({'cell': index+1, 'etype': type(exc).__name__, 'emsg': str(exc)[:300]})
            finally:
                signal.alarm(0)
                if shim is not None:
                    shim.after_cell()
                if watch:
                    signal.alarm(10)
                    try:
                        snapshot(watch, index+1)
                    except BaseException:  # a snapshot problem never affects the run
                        pass
                    finally:
                        signal.alarm(0)
        return {'cells_total': total, 'cells_ok': ok, 'cell_errors': errors,
                'declared_sid': str(ns.get('STUDENT_ID', ''))[:512], 'cohort': str(ns.get('COHORT', ''))[:30],
                'snapshots': [cell for cell, _ in states],
                'notes': notes[:50] + ([{'shim': e[:200]} for e in shim.EVENTS] if shim is not None else [])}
    if request['op'] == 'rerun':
        return rerun(request)
    if request['op'] == 'names':
        found = set()
        for scope in [ns] + [values for _, values in states]:
            for k, v in scope.items():
                if isinstance(k, str) and not k.startswith('_') and not isinstance(v, types.ModuleType):
                    found.add(k)
        return sorted(found)[:2000]
    if request['op'] == 'get':
        return encode(scope_for(request).get(request['name'], '__MISSING__'))
    if request['op'] == 'call_dataframe':
        import pandas as pd
        signal.alarm(request['timeout'])
        try:
            return encode(scope_for(request)[request['name']](pd.DataFrame(request['rows']),request['column']))
        finally:
            signal.alarm(0)
    if request['op'] == 'call':
        signal.alarm(request['timeout'])
        try:
            before=json.dumps(request['args'],sort_keys=True) if request.get('preserve_arguments') else None
            value=scope_for(request)[request['name']](*request['args'])
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
