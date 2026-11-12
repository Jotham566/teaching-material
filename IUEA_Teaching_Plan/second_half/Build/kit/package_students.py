"""Student ZIP per cohort and class: the lab notebook, the CSV and a one-page START_HERE. python3 kit/package_students.py"""
import sys, zipfile
from pathlib import Path
BUILD = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BUILD / 'content'))
import common as C
LAB = BUILD.parent / 'Lab Notebooks'
OUT = BUILD.parent / 'Student Packages'
NAMES = {1: 'First_Model', 2: 'Classification', 3: 'Trust', 4: 'Features_and_Model_Choice'}
OUT.mkdir(exist_ok=True)
for code in ('CML3112', 'CML3113', 'CML3111'):
    c = C.COHORTS[code]
    for n, nm in NAMES.items():
        nbp = LAB / code / f'Class{n}_Lab_{nm}.ipynb'
        if not nbp.exists():
            continue
        text = (f'# {code}, Class {n} (Week {C.WEEK_OF_CLASS[n]}): lab pack\n\n1. Open Google Colab and upload `{nbp.name}`.\n2. In the Files panel (folder icon) upload `engineering_data.csv`.\n'
                '3. Run the cells in order with Shift and Enter. Read the PREDICT, READ and CHANGE boxes and type your answers in the lines that start with `>`.\n'
                '4. At the end choose Runtime, Restart session and run all. If nothing fails, save a copy in Drive.\n\n'
                'This notebook is for learning in class. It is not an upload. Your lecturer shares the block assignment separately: it is practice, collected with feedback, and does not count toward your final mark. The Week 12 project uses the same steps.\n\n'
                f'The data are synthetic teaching data about {c["short"]} ({c["unit"]}).\n')
        with zipfile.ZipFile(OUT / f'{code}_Class{n}_lab_pack.zip', 'w', zipfile.ZIP_DEFLATED) as z:
            z.write(nbp, nbp.name)
            z.write(LAB / code / 'engineering_data.csv', 'engineering_data.csv')
            z.writestr('START_HERE.md', text)
        print('wrote', code, n)
