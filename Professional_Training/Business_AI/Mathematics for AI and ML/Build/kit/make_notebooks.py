"""Build and prove the Python lab notebooks. python3 kit/make_notebooks.py [1 2 ...]
Each content/labs/sNN_nb.py defines build(solution: bool) -> nb.Notebook. The learner version is written to ../Notebooks (TODO cells empty, checks say NOT YET);
the solution version (model answers filled in) is written to ../Facilitator Materials/Solution Notebooks and MUST run end to end and finish with 'All N checks pass'.
The learner version must NOT finish with 'All N checks pass'. Only numpy, pandas and matplotlib are used (no scikit-learn)."""
import importlib.util
import re
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
BUILD = HERE.parent
sys.path.insert(0, str(HERE))
import nb as NB  # noqa: E402
OUT = BUILD.parent / 'Notebooks'
SOL = BUILD.parent / 'Facilitator Materials' / 'Solution Notebooks'
DATA = BUILD / 'data'


def main(argv):
    nums = [int(a) for a in argv if a.isdigit()] or sorted(int(p.stem[1:3]) for p in (BUILD / 'content' / 'labs').glob('s[0-9][0-9]_nb.py'))
    bad = 0
    DATA.mkdir(exist_ok=True)
    for n in nums:
        spec = importlib.util.spec_from_file_location(f's{n:02d}_nb', BUILD / 'content' / 'labs' / f's{n:02d}_nb.py')
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        title = getattr(m, 'TITLE', f'Lab {n}')
        title = re.sub(r'^Session\s*\d+\s*[:\-]?\s*', '', title)   # the file name adds 'Session NN - ' itself
        name = f'Session {n:02d} - {re.sub(chr(58) + "|/", "", title)}.ipynb'
        lp = OUT / name
        sp = SOL / name.replace('.ipynb', ' (solution).ipynb')
        sol_nb = m.build(True)
        sol_nb.save(sp)
        rs0 = NB.run(sp, DATA)
        mm = [re.search(r'All (\d+) checks pass', o) for _, o, _ in rs0 if o]
        total = next((int(x.group(1)) for x in mm if x), None)
        if total:   # every learner and solution notebook knows its full count
            sol_nb.set_total(total); sol_nb.save(sp)
        ln = m.build(False)
        if total:
            ln.set_total(total)
        ln.save(lp)
        rs = NB.run(sp, DATA)
        errs = [f'cell {i}: {e.strip().splitlines()[-1]}' for i, _, e in rs if e]
        out_s = '\n'.join(o for _, o, _ in rs)
        last_s = [l for l in out_s.splitlines() if 'checks pass' in l][-1:] or ['(no check summary)']
        rl = NB.run(lp, DATA)
        out_l = '\n'.join(o for _, o, _ in rl)
        last_l = [l for l in out_l.splitlines() if 'checks pass' in l][-1:] or ['(no check summary)']
        probs = errs[:]
        if not last_s[0].startswith('All '):
            probs.append('solution does not end with All N checks pass: ' + last_s[0])
        if last_l[0].startswith('All '):
            probs.append('LEARNER version passes all checks without any work')
        if hasattr(m, 'CHECK'):
            probs += m.CHECK(rs)
        print(n, 'OK' if not probs else f'{len(probs)} problems', '| solution:', last_s[0], '| learner:', last_l[0])
        for p in probs:
            print('    ', p)
        bad += len(probs)
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main(sys.argv[1:])
