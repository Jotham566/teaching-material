"""Proves every lab workbook: the SOLUTION version recalculated by LibreOffice says 'All N checks pass'; the LEARNER version (gold cells empty) does NOT.
python3 kit/check_workbooks.py [1 2 ...]     needs LibreOffice (soffice). Each content/labs/sNN_xl.py defines build(solution: bool) -> XL."""
import importlib.util
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from openpyxl import load_workbook
HERE = Path(__file__).resolve().parent
BUILD = HERE.parent
sys.path.insert(0, str(HERE))
OUT = BUILD.parent / 'Workbooks'


def recalc(path, tmp):
    __import__('lo_fonts').seed(f'-env:UserInstallation=file:///tmp/lo_{os.getpid()}')   # brand font for the PDF
    subprocess.run(['soffice', f'-env:UserInstallation=file:///tmp/lo_{os.getpid()}', '--headless', '--calc', '--convert-to', 'xlsx', '--outdir', str(tmp), str(path)], capture_output=True, timeout=180)
    return Path(tmp) / Path(path).name


def summary(path):
    wb = load_workbook(str(path), data_only=True)
    ws = wb['Check']
    for row in ws.iter_rows(values_only=True):
        if row and row[0] == 'Summary':
            return row[1], [r[3] for r in ws.iter_rows(min_row=4, values_only=True) if r and r[3] in ('OK', 'NOT YET')]
    return None, []


def main(argv):
    nums = [int(a) for a in argv if a.isdigit()] or sorted(int(p.stem[1:3]) for p in (BUILD / 'content' / 'labs').glob('s[0-9][0-9]_xl.py'))
    bad = 0
    for n in nums:
        spec = importlib.util.spec_from_file_location(f's{n:02d}_xl', BUILD / 'content' / 'labs' / f's{n:02d}_xl.py')
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        with tempfile.TemporaryDirectory() as t:
            sol = m.build(True)
            ps = sol.save(Path(t) / f'S{n:02d}_solution.xlsx')
            s1, r1 = summary(recalc(ps, Path(t) / 'r1'))
            SOLX = BUILD.parent / 'Facilitator Materials' / 'Solution Workbooks'
            SOLX.mkdir(parents=True, exist_ok=True)
            sol.save(SOLX / f'Session {n:02d} - {sol.title.split(": ", 1)[-1]} (solution).xlsx')
            lr = m.build(False)
            lp = lr.save(OUT / f'Session {n:02d} - {sol.title.split(": ", 1)[-1]}.xlsx')
            s2, r2 = summary(recalc(lp, Path(t) / 'r2'))
        ok = s1 == f'All {sol.n_checks} checks pass' and s2 != f'All {sol.n_checks} checks pass'
        print(n, 'OK' if ok else 'PROBLEM', '| solution:', s1, '| learner:', s2)
        bad += 0 if ok else 1
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main(sys.argv[1:])
