"""Prove the cell flow of the Session 14, 15 and 16 notebooks (learner and solution) against the small scikit-learn shim in ref/fx_shim (built on content/loans_canon.py).
python3 ref/fx_prove_nb.py 14 15 16        Writes nothing into the course folders. Prints, for each notebook: errors, and the last check line of the solution and of the learner version.
What this proves: every cell runs in order; the solution ends 'All N checks pass'; the learner version reaches show_checks and says NOT YET without a traceback.
What this does NOT prove: what real scikit-learn prints. The shim uses the same replica functions as the expected numbers, so agreement of numbers is circular. Re-run on real scikit-learn."""
import importlib.util
import sys
import tempfile
from pathlib import Path

REF = Path(__file__).resolve().parent
BUILD = REF.parent
sys.path.insert(0, str(REF / 'fx_shim'))
sys.path.insert(0, str(BUILD / 'kit'))
sys.path.insert(0, str(BUILD / 'content'))
import nb as NB  # noqa: E402
NB.REF = REF / 'fx_shim'   # nb.run() puts this folder first on sys.path, so 'import sklearn' finds the shim

COURSE = BUILD.parent.parent
DATA = COURSE / '03 Learner Materials' / 'Practice Files' / 'data'


def main(argv):
    import shutil
    work = Path(tempfile.mkdtemp(prefix='fxnb_')) / 'data'
    shutil.copytree(DATA, work)
    bad = 0
    orig_path = list(sys.path)
    for n in [int(a) for a in argv if a.isdigit()]:
        spec = importlib.util.spec_from_file_location(f's{n:02d}_nb', BUILD / 'content' / 'labs' / f's{n:02d}_nb.py')
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        res = {}
        for sol in (True, False):
            p = Path(tempfile.gettempdir()) / f'fx_{n}_{"sol" if sol else "learner"}.ipynb'
            m.build(sol).save(p)
            for k in [k for k in sys.modules if k == 'sklearn' or k.startswith('sklearn.')]:
                del sys.modules[k]
            rs = NB.run(p, work)
            errs = [f'cell {i}: {e.strip().splitlines()[-1]}' for i, _, e in rs if e]
            out = '\n'.join(o for _, o, _ in rs)
            last = [l for l in out.splitlines() if 'checks pass' in l][-1:] or ['(no check summary)']
            res[sol] = (errs, last[0], out)
        print(f'Session {n}: solution -> {res[True][1]}; learner -> {res[False][1]}')
        for e in res[True][0]:
            print('   SOLUTION ERROR', e)
            bad += 1
        for e in res[False][0]:
            print('   LEARNER ERROR', e)
            bad += 1
        if not res[True][1].startswith('All '):
            bad += 1
        if res[False][1].startswith('All '):
            print('   learner passes all checks without work')
            bad += 1
        Path(tempfile.gettempdir(), f'fx_{n}_solution_output.txt').write_text(res[True][2])
        Path(tempfile.gettempdir(), f'fx_{n}_learner_output.txt').write_text(res[False][2])
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main(sys.argv[1:])
