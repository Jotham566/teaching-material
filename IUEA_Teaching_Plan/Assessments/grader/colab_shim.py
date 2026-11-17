"""Make the isolated sandbox behave like Google Colab for beginners' notebooks.

Imported by isolated_worker.py INSIDE the Docker sandbox (mounted read-only at
/colab_shim.py) and importable on the host for unit tests. It contains no
grading decisions and no keys. Every helper only changes what would otherwise
be an error caused by the sandbox differing from Colab; code that already runs
behaves exactly as before.

Reusable pieces (Test 1 and later assessments can import them):

* install(ns, supplied_dirs)   google.colab (files/drive), IPython and display stubs,
                               and the CSV alias resolver for open()/pandas readers.
* resolve_data_path(path, supplied_dirs)
                               'campus_energy (1).csv', 'campus_energy[2].csv',
                               '/content/sample_data/campus_energy.csv',
                               '/content/drive/MyDrive/x/campus_energy.csv' ... -> the supplied CSV.
* ipython_cell_source(source)  IPython's leading-indent and leading-blank-line cleanup.
* compile_cell(source, name)   compile, retrying with the IPython cleanup only on SyntaxError.
* after_cell()                 plt.close('all'), as Colab's inline backend does after each cell.
* colab_py_to_notebook(text)   a Colab "Download .py" export -> notebook dict (one cell per
                               top-level statement, markdown docstrings dropped).
"""
import ast
import builtins
import io
import os
import re
import sys
import textwrap
import types
from pathlib import Path

DATA_SUFFIXES = ('.csv', '.tsv', '.xlsx', '.xls')
# Colab/Drive/browser rename patterns: 'name (1).csv', 'name(1).csv', 'name[1].csv',
# 'name-1.csv' is NOT accepted (could be a genuinely different file), 'Copy of name.csv'.
_COPY_SUFFIX = re.compile(r'(?:\s*\(\d+\)|\s*\[\d+\])+$')
_COPY_PREFIX = re.compile(r'^(?:copy of\s+)+', re.I)
# What the shims did, reported back to the trusted evaluator as plain text.
EVENTS = []


def _event(text):
    if text not in EVENTS and len(EVENTS) < 40:
        EVENTS.append(text)


def _normal_stem(name):
    stem, dot, ext = str(name).rpartition('.')
    if not dot:
        stem, ext = str(name), ''
    stem = _COPY_PREFIX.sub('', _COPY_SUFFIX.sub('', stem.strip())).strip()
    return (stem.lower(), ext.lower())


def supplied_files(supplied_dirs):
    out = {}
    for d in supplied_dirs:
        try:
            for p in sorted(Path(d).iterdir()):
                if p.is_file() and p.suffix.lower() in DATA_SUFFIXES:
                    out.setdefault(_normal_stem(p.name), p)
        except OSError:
            continue
    return out


def resolve_data_path(path, supplied_dirs):
    """Return a supplied data file for a path that does not exist, else None.

    Only the base name matters, after removing Colab's re-upload suffixes
    ' (1)', '(2)', '[1]' and a 'Copy of ' prefix (case-insensitive). The folder
    part ('/content/', 'sample_data/', '/content/drive/MyDrive/...', '/') is ignored
    because the sandbox has only the supplied copy."""
    try:
        p = os.fspath(path)
    except TypeError:
        return None
    if not isinstance(p, str) or not p or os.path.exists(p):
        return None
    if p.startswith(('http://', 'https://')):
        return None
    base = p.replace('\\', '/').rstrip('/').rsplit('/', 1)[-1]
    key = _normal_stem(base)
    if not key[1] or ('.' + key[1]) not in DATA_SUFFIXES:
        return None
    return supplied_files(supplied_dirs).get(key)


def ipython_cell_source(source):
    """IPython's cleanup before compiling a cell: drop leading blank lines and remove
    the first line's indentation from every line that starts with it."""
    lines = source.splitlines(True)
    while lines and not lines[0].strip():
        lines.pop(0)
    if not lines:
        return ''
    m = re.match(r'^[ \t]+', lines[0])
    if not m:
        return ''.join(lines)
    space = m.group(0)
    fixed = ''.join(l[len(space):] if l.startswith(space) else l for l in lines)
    try:
        compile(fixed, '<dedent-check>', 'exec')
        return fixed
    except SyntaxError:
        return textwrap.dedent(''.join(lines))


def compile_cell(source, name):
    """Compile as the sandbox always did; only if that is a SyntaxError (for example an
    IndentationError from a cell that starts with a space) retry the IPython-cleaned
    source, which Colab would have run."""
    try:
        return compile(source, name, 'exec'), False
    except SyntaxError:
        fixed = ipython_cell_source(source)
        if fixed and fixed != source:
            try:
                code = compile(fixed, name, 'exec')
                _event('%s dedented as IPython does' % name.strip('<>'))
                return code, True
            except SyntaxError:
                pass
        raise


def after_cell():
    plt = sys.modules.get('matplotlib.pyplot')
    if plt is not None:
        try:
            plt.close('all')
        except Exception:  # noqa: BLE001
            pass


def _display(*objs, **_kw):
    """Colab's display(): a no-op for grading (output is not marked)."""
    _event('display() shim used')
    return None


class _Dummy:
    """Stand-in for IPython display objects (HTML, Markdown, Image ...)."""
    def __init__(self, *a, **k):
        self.data = a[0] if a else None

    def __repr__(self):
        return '<display object>'


class _FakeShell:
    def run_line_magic(self, *a, **k):
        return None

    def run_cell_magic(self, *a, **k):
        return None

    def system(self, *a, **k):
        return None

    def __getattr__(self, _name):
        return lambda *a, **k: None


def _module(name, **attrs):
    m = types.ModuleType(name)
    m.__dict__.update(attrs)
    return m


def install_colab_modules(supplied_dirs):
    """google.colab with files.upload (returns the supplied CSVs), files.download,
    drive.mount/flush_and_unmount (no-ops), output and data_table stubs."""
    def supplied_csv_upload():
        return {p.name: p.read_bytes() for p in sorted(Path(supplied_dirs[0]).glob('*.csv'))}

    def no_browser_download(filename):
        if not Path(filename).is_file():
            raise FileNotFoundError(filename)

    def mount(mountpoint='/content/drive', force_remount=False, **_kw):
        _event('google.colab.drive.mount() shim used')
        return None

    google = _module('google'); google.__path__ = []
    colab = _module('google.colab'); colab.__path__ = []
    files = _module('google.colab.files', upload=supplied_csv_upload, download=no_browser_download)
    drive = _module('google.colab.drive', mount=mount, flush_and_unmount=lambda *a, **k: None)
    output = _module('google.colab.output', clear=lambda *a, **k: None, enable_custom_widget_manager=lambda *a, **k: None)
    data_table = _module('google.colab.data_table', enable_dataframe_formatter=lambda *a, **k: None,
                         disable_dataframe_formatter=lambda *a, **k: None, DataTable=_Dummy)
    colab.files, colab.drive, colab.output, colab.data_table = files, drive, output, data_table
    google.colab = colab
    for m in (google, colab, files, drive, output, data_table):
        sys.modules[m.__name__] = m


def install_ipython_stub():
    """Only when the real IPython is not installed (it is not in the grader image)."""
    try:
        import IPython  # noqa: F401
        return
    except ImportError:
        pass
    disp = _module('IPython.display', display=_display, clear_output=lambda *a, **k: None,
                   HTML=_Dummy, Markdown=_Dummy, Image=_Dummy, Math=_Dummy, Latex=_Dummy,
                   JSON=_Dummy, SVG=_Dummy, Javascript=_Dummy, IFrame=_Dummy, Audio=_Dummy, Video=_Dummy)
    core = _module('IPython.core'); core.__path__ = []
    core_disp = _module('IPython.core.display', **{k: v for k, v in disp.__dict__.items() if not k.startswith('__')})
    core.display = core_disp
    # IPython.get_ipython() returns None, as in plain Python: matplotlib and pandas look
    # for IPython in sys.modules and would otherwise try to hook into a fake shell
    # (Test 1 fix, 10 Nov 2026: plotting cells failed with "no attribute 'register'").
    # A notebook that calls get_ipython() itself still gets the no-op shell from install().
    ip = _module('IPython', display=disp, core=core, get_ipython=lambda: None,
                 version_info=(8, 24, 0), __version__='8.24.0')
    ip.__path__ = []
    for m in (ip, disp, core, core_disp):
        sys.modules[m.__name__] = m


def install_data_resolver(supplied_dirs):
    """Wrap open() and the pandas/numpy readers so that a missing path whose base name
    matches a supplied data file (after Colab's renames) reads that file."""
    real_open = builtins.open

    def fix(p):
        hit = resolve_data_path(p, supplied_dirs)
        if hit is None:
            return p
        _event('data path %r read as the supplied %s' % (str(p)[:120], hit.name))
        return str(hit)

    def colab_open(file, mode='r', *a, **k):
        if isinstance(mode, str) and not any(c in mode for c in 'wax+'):
            file = fix(file)
        return real_open(file, mode, *a, **k)

    builtins.open = colab_open
    io.open = colab_open
    try:
        import pandas as pd
    except Exception:  # noqa: BLE001
        pd = None
    if pd is not None:
        for name in ('read_csv', 'read_table', 'read_excel'):
            real = getattr(pd, name, None)
            if real is None:
                continue

            def wrapped(filepath_or_buffer=None, *a, _real=real, **k):
                if filepath_or_buffer is None and 'filepath_or_buffer' in k:
                    filepath_or_buffer = k.pop('filepath_or_buffer')
                return _real(fix(filepath_or_buffer), *a, **k)
            wrapped.__name__ = name
            wrapped.__doc__ = real.__doc__
            setattr(pd, name, wrapped)
    try:
        import numpy as np
        for name in ('loadtxt', 'genfromtxt'):
            real = getattr(np, name)

            def wrapped_np(fname, *a, _real=real, **k):
                return _real(fix(fname), *a, **k)
            setattr(np, name, wrapped_np)
    except Exception:  # noqa: BLE001
        pass


def install(ns, supplied_dirs=('/inputs', '/work')):
    """All Colab shims for one notebook namespace."""
    supplied_dirs = tuple(str(d) for d in supplied_dirs)
    install_colab_modules(supplied_dirs)
    install_ipython_stub()
    builtins.display = _display
    ns.setdefault('display', _display)
    ns.setdefault('get_ipython', lambda: _FakeShell())
    install_data_resolver(supplied_dirs)


# --------------------------------------------------------------------------- #
# Intake helpers: Colab .py exports (pure text processing, nothing is executed)
# --------------------------------------------------------------------------- #

def _comment_magics(text):
    return '\n'.join('# ' + l if l.lstrip().startswith(('!', '%')) else l for l in text.splitlines())


def code_cells_from_python(text):
    """Split Python text into cells: one per top-level statement, dropping bare string
    expressions (Colab writes markdown cells as module-level docstrings)."""
    text = _comment_magics(text.replace('\r\n', '\n'))
    lines = text.split('\n')
    try:
        tree = ast.parse(text)
    except SyntaxError:
        # Fall back to blank-line separated blocks; each runs (or fails) on its own.
        return [b for b in re.split(r'\n\s*\n', text) if b.strip()]
    cells, pending = [], 0  # comment lines before a statement stay with it (evidence, not run)
    for node in tree.body:
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            lead = [l for l in lines[pending:node.lineno - 1] if l.strip() and not l.startswith('# -*-')]
            if lead:
                cells.append('\n'.join(lead))  # a comment-only cell (e.g. '# Your answer here ...')
            pending = node.end_lineno
            continue
        start = node.lineno - 1
        if getattr(node, 'decorator_list', None):
            start = min(d.lineno for d in node.decorator_list) - 1
        lead = [l for l in lines[pending:start] if l.strip()]
        cells.append('\n'.join(lead + lines[start:node.end_lineno]))
        pending = node.end_lineno
    tail = [l for l in lines[pending:] if l.strip()]
    if tail:
        cells.append('\n'.join(tail))
    return cells


def notebook_from_cells(cells, origin):
    return {'nbformat': 4, 'nbformat_minor': 5, 'metadata': {'iuea_converted_from': origin},
            'cells': [{'cell_type': 'code', 'metadata': {}, 'execution_count': None, 'outputs': [],
                       'source': c} for c in cells]}


def colab_py_to_notebook(text):
    return notebook_from_cells(code_cells_from_python(text), 'colab .py export')


_CODE_START = re.compile(r'^\s*(import |from \S+ import |[A-Za-z_]\w*\s*=|def |with |for |if |print\()')


def code_spans(text, min_lines=3):
    """Longest runs of lines that parse as Python, for documents with pasted code."""
    lines = text.replace('\r\n', '\n').split('\n')
    spans, i = [], 0
    while i < len(lines):
        if not _CODE_START.match(lines[i]):
            i += 1
            continue
        best = None
        for j in range(len(lines), i, -1):
            chunk = '\n'.join(lines[i:j])
            try:
                tree = ast.parse(chunk)
            except SyntaxError:
                continue
            if any(isinstance(n, (ast.Assign, ast.AugAssign, ast.FunctionDef, ast.With, ast.For, ast.Import, ast.ImportFrom)) for n in tree.body):
                best = j
            break
        if best:
            # Drop trailing prose that happens to parse (a bare word or sentence-like name).
            while best > i:
                try:
                    tail = ast.parse('\n'.join(lines[i:best])).body[-1]
                except SyntaxError:
                    break
                if isinstance(tail, ast.Expr) and isinstance(tail.value, (ast.Name, ast.Constant)) and tail.lineno == tail.end_lineno and best - 1 >= i and lines[best - 1].strip() and tail.lineno == best - i:
                    best -= 1
                else:
                    break
        if best and best - i >= min_lines:
            spans.append('\n'.join(lines[i:best]).strip('\n'))
            i = best
        else:
            i += 1
    return spans
