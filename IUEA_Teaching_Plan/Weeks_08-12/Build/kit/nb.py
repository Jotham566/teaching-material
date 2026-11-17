"""Tiny notebook toolkit: build a .ipynb (nbformat 4) from cells written in Python, and run its code cells here with the scikit-learn stand-in.

    nb = Notebook(); nb.md('# Title'); nb.code('print(1)'); nb.save(path)
    run(path, workdir)  -> list of (cell_index, stdout, error or None)
"""
import contextlib
import io
import json
import os
import sys
import traceback
from pathlib import Path

REF = Path(__file__).resolve().parents[1] / 'ref'


def _src(t):
    lines = t.strip('\n').split('\n')
    return [l + '\n' for l in lines[:-1]] + [lines[-1]]


class Notebook:
    def __init__(self):
        self.cells = []

    def md(self, text):
        self.cells.append({'cell_type': 'markdown', 'metadata': {}, 'source': _src(text)})

    def code(self, text):
        self.cells.append({'cell_type': 'code', 'metadata': {}, 'execution_count': None, 'outputs': [], 'source': _src(text)})

    def step(self, n, title, why):
        self.md(f'---\n## Step {n}: {title}\n\n{why}')

    def predict(self, question):
        self.md(f'**PREDICT first.** {question}\n\nWrite your guess here before you run the next cell:\n\n> My prediction: ')

    def read(self, question):
        self.md(f'**READ the output.** {question}\n\n> My answer: ')

    def change(self, instruction):
        self.md(f'**CHANGE one thing.** {instruction}\n\n> What I saw: ')

    def save(self, path):
        nb = {'cells': self.cells, 'metadata': {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}, 'language_info': {'name': 'python'}},
              'nbformat': 4, 'nbformat_minor': 5}
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(json.dumps(nb, indent=1), encoding='utf-8')


def run(path, workdir):
    """Execute every code cell in order in one namespace. Returns [(index, stdout, error)]. Uses the NumPy scikit-learn stand-in in ref/."""
    import matplotlib
    matplotlib.use('Agg')
    sys.path.insert(0, str(REF))
    nb = json.loads(Path(path).read_text(encoding='utf-8'))
    ns = {'__name__': '__main__'}
    out = []
    old = os.getcwd()
    os.chdir(workdir)
    try:
        for i, c in enumerate(nb['cells']):
            if c['cell_type'] != 'code':
                continue
            buf = io.StringIO()
            err = None
            try:
                with contextlib.redirect_stdout(buf):
                    code = ''.join(c['source'])
                    lines = code.rstrip().split('\n')
                    # show the value of a final bare expression, like Jupyter does
                    try:
                        import ast
                        tree = ast.parse(code)
                        if tree.body and isinstance(tree.body[-1], ast.Expr):
                            last = ast.Expression(tree.body[-1].value)
                            body = ast.Module(tree.body[:-1], type_ignores=[])
                            exec(compile(body, '<cell>', 'exec'), ns)
                            val = eval(compile(last, '<cell>', 'eval'), ns)
                            if val is not None:
                                print(repr(val) if not hasattr(val, 'to_string') else val.to_string())
                        else:
                            exec(compile(tree, '<cell>', 'exec'), ns)
                    except SyntaxError:
                        raise
            except Exception:
                err = traceback.format_exc(limit=3)
            out.append((i, buf.getvalue(), err))
    finally:
        os.chdir(old)
    return out
