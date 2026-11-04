"""Build and check the lab notebooks. python3 kit/make_labs.py [1 2 3 4]   (class numbers; none = all that exist).
For each cohort: writes `Lab Notebooks/<code>/Class<N>_Lab_<name>.ipynb` plus the CSV the lab reads, then runs every code cell with the NumPy stand-in and
reports errors. Class files may define CHECK(code, outputs, facts) -> list of problems, to compare printed numbers with the reference values."""
import importlib.util
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUILD = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(BUILD / 'content'))
import nb as NB  # noqa: E402
OUT = BUILD.parent / 'Lab Notebooks'
NAMES = {1: 'First_Model', 2: 'Classification', 3: 'Trust', 4: 'Features_and_Model_Choice'}
CODES = ['CML3112', 'CML3113', 'CML3111']


def main(argv):
    nums = [int(a) for a in argv if a.isdigit()] or [n for n in NAMES if (BUILD / 'content' / f'lab{n}.py').exists()]
    bad = 0
    for n in nums:
        spec = importlib.util.spec_from_file_location(f'lab{n}', BUILD / 'content' / f'lab{n}.py')
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        for code in CODES:
            d = OUT / code
            d.mkdir(parents=True, exist_ok=True)
            shutil.copy(BUILD / 'data' / code / 'engineering_data.csv', d / 'engineering_data.csv')
            path = d / f'Class{n}_Lab_{NAMES[n]}.ipynb'
            m.build(code).save(path)
            res = NB.run(path, d)
            errs = [(i, e) for i, _, e in res if e]
            probs = [f'cell {i}: {e.strip().splitlines()[-1]}' for i, e in errs]
            if hasattr(m, 'CHECK'):
                import common as C
                probs += m.CHECK(code, res, C.facts(code))
            print(n, code, len(res), 'code cells,', 'OK' if not probs else f'{len(probs)} problems')
            for p in probs:
                print('   ', p)
            bad += len(probs)
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main(sys.argv[1:])
