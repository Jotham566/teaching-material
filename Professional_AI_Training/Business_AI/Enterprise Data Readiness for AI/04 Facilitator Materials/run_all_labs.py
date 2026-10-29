"""Run every solution notebook from top to bottom and report what fails.

Use it once before you teach, on any machine that has the course stack (or in a Colab notebook cell with the data uploaded):

    python3 run_all_labs.py "04 Facilitator Materials/Lab Solutions" "03 Learner Materials/Practice Files/data" [--allow-missing-libs]

Needs: Python 3 with pandas, numpy and matplotlib for most cells, and pypdf, pdfplumber and pytesseract (with the Tesseract program) for Session 5.
The cells that need sentence-transformers, chromadb, pgvector with psycopg2, pandera, great_expectations, presidio, dagster, duckdb with pyarrow, docling or ragas
fail with ModuleNotFoundError when the library is missing. With --allow-missing-libs they are reported as SKIPPED and the run goes on. Run those cells once in Google Colab.
The cells that download a model (sentence-transformers) are skipped unless you pass --with-downloads, because they need internet and several hundred MB.
A cell that needs a library that is not installed is reported as SKIPPED, not as a failure, when you pass --allow-missing-libs. Cells that depend on a skipped cell (a NameError, KeyError or failed assert caused by the missing result) are skipped too.
Exit code 0 means every notebook ran to the end.
"""
import sys, os, json, re, shutil, subprocess, tempfile, argparse
from pathlib import Path
ap = argparse.ArgumentParser(); ap.add_argument('notebooks'); ap.add_argument('data'); ap.add_argument('--with-downloads', action='store_true'); ap.add_argument('--allow-missing-libs', action='store_true'); ap.add_argument('--timeout', type=int, default=900)
a = ap.parse_args()
DOWNLOAD = re.compile(r'sentence_transformers|from transformers|import transformers|SentenceTransformer|(?<![A-Za-z_])pipeline\(')
bad = 0
for nb in sorted(Path(a.notebooks).glob('*.ipynb')):
    cells = json.loads(nb.read_text(encoding='utf-8'))['cells']; code = []
    for c in cells:
        if c['cell_type'] != 'code': continue
        src = ''.join(c['source'])
        if src.lstrip().startswith('# Run this cell first'): continue           # the setup cell uploads or downloads the data; we copy it instead
        if DOWNLOAD.search(src) and not a.with_downloads:
            code.append('__skipped = True\nprint("SKIPPED cell: needs a model download (run with --with-downloads, or run it in Colab)")'); continue   # later cells that need its result are skipped too
        code.append(src)
    work = Path(tempfile.mkdtemp()); shutil.copytree(a.data, work, dirs_exist_ok=True)
    script = work / 'run_lab.py'; body = ['import matplotlib', "matplotlib.use('Agg')", 'import traceback, sys', '__skipped = False']
    for i, src in enumerate(code, 1):
        body.append(f'__cell = {i}')
        body.append('try:\n' + '\n'.join('    ' + l for l in src.split('\n')) + '\n    pass\n'
                    'except ModuleNotFoundError as e:\n    print(f"SKIPPED cell {__cell}: missing library {e.name}")\n    __skipped = True\n    ' + ('pass' if a.allow_missing_libs else 'raise') +
                    '\nexcept (NameError, KeyError, AttributeError, TypeError, ValueError, IndexError, AssertionError) as e:\n    if __skipped:\n        print(f"SKIPPED cell {__cell}: depends on a skipped cell ({type(e).__name__}: {e})")\n    else:\n        print(f"FAILED cell {__cell}: {type(e).__name__}: {e}"); sys.exit(1)'
                    '\nexcept BaseException as e:\n    print(f"FAILED cell {__cell}: {type(e).__name__}: {e}")\n    sys.exit(1)')
    script.write_text('\n'.join(body), encoding='utf-8')
    try:
        r = subprocess.run([sys.executable, str(script)], cwd=work, capture_output=True, text=True, timeout=a.timeout, env={**os.environ, 'MPLBACKEND': 'Agg'})
        out = (r.stdout + r.stderr)
        status = 'OK' if r.returncode == 0 else 'FAILED'
        skipped = out.count('SKIPPED')
    except subprocess.TimeoutExpired: status, out, skipped = 'TIMED OUT', '', 0
    print(f'{status:9} {nb.name}' + (f'  ({skipped} cells skipped for missing libraries)' if skipped else ''))
    if status != 'OK':
        bad += 1; print('          ' + '\n          '.join(l for l in out.strip().split('\n')[-6:]))
    shutil.rmtree(work, ignore_errors=True)
print('\nAll notebooks ran.' if not bad else f'\n{bad} notebook(s) need attention.')
sys.exit(1 if bad else 0)
