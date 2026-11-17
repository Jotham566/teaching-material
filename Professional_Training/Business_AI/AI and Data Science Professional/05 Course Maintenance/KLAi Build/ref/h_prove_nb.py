"""Prove the Session 15 and 16 lab notebooks here, with the extra stand-in pieces from sklearn/h_extras.py installed. python3 ref/h_prove_nb.py 15 16
Writes nothing. Prints, for each notebook, the problems and the last check line of the solution and of the learner version."""
import importlib.util
import sys
from pathlib import Path

REF = Path(__file__).resolve().parent
BUILD = REF.parent
sys.path.insert(0, str(REF))
sys.path.insert(0, str(BUILD / 'kit'))
import nb as NB  # noqa: E402
from sklearn import h_extras  # noqa: E402

h_extras.install()
COURSE = BUILD.parent.parent
DATA = COURSE / '03 Learner Materials' / 'Practice Files' / 'data'


def main(argv):
    import tempfile
    for n in [int(a) for a in argv]:
        spec = importlib.util.spec_from_file_location(f's{n:02d}_nb', BUILD / 'content' / 'labs' / f's{n:02d}_nb.py')
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        res = {}
        for sol in (True, False):
            p = Path(tempfile.gettempdir()) / f'h_{n}_{"sol" if sol else "learner"}.ipynb'
            m.build(sol).save(p)
            rs = NB.run(p, DATA)
            errs = [f'cell {i}: {e.strip().splitlines()[-1]}' for i, _, e in rs if e]
            out = '\n'.join(o for _, o, _ in rs)
            last = [l for l in out.splitlines() if 'checks pass' in l][-1:] or ['(no check summary)']
            res[sol] = (errs, last[0], out)
        print(f'Session {n}: solution -> {res[True][1]}; learner -> {res[False][1]}')
        for e in res[True][0]:
            print('   SOLUTION ERROR', e)
        for e in res[False][0]:
            print('   learner error (cells left None may fail)', e)
        for stray in ('loan_risk_scores.csv', 'model_scorecard.csv'):
            (DATA / stray).unlink(missing_ok=True)
        if '-v' in argv or True:
            Path(tempfile.gettempdir(), f'h_{n}_solution_output.txt').write_text(res[True][2])


if __name__ == '__main__':
    main(sys.argv[1:])
