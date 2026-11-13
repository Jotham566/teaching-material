"""Copy the project notebooks into the folder the test portal and the collector read. python3 tools/install_project_bank.py [--dry-run]

Run this ONLY at deployment, after build_project_notebooks.py --require-forms. It writes IUEA_Teaching_Plan/assessment_banks/ML_PROJECT/<cohort>/A/
(ML_PROJECT_student.ipynb and the instruction files, the same layout as TEST1; every student has the same notebook, so there is one folder,
and the data is inside the notebook) and keeps any older files in _backup_2026-11-04/.
It never touches a grader. The portal itself reads deploy/PacketsMLProject.gs (built by tools/build_deploy_bundle.py), so this copy is for the
collector's reference and for scripts that read assessment_banks.
"""
import argparse
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import project_content as PC  # noqa: E402

INSTRUCTIONS = """{code} ML_PROJECT: Engineering ML project, online, 3 hours from Start test. The window {window}.

1. Open the entry page, enter your name, Google email and Student Registration Number, and press Start test. Your 3 hours start then.
   Start by {last} to get the full 3 hours.
2. Press Open my test in Colab. Run the countdown cell, then the setup cell. The data file is inside the notebook: no upload or download.
3. Complete Tasks 1 to 7 and the Part B memo form (Task 8). Choose Runtime, then Restart session and run all.
4. Run the last cell, click Submit test, open the form link, check your details and press Submit before your personal deadline.
Rules: the same as Practical Test 1. Individual work. No AI or outside help. {own}
Help: the class channel, {support}. A technical failure: report it at once on the class channel with a screenshot.
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    bank = PC.PLAN / 'assessment_banks/ML_PROJECT'
    for code in PC.CODES:
        dest = bank / code / 'A'
        backup = dest / '_backup_2026-11-04'
        print(('would install ' if a.dry_run else 'installing ') + str(dest))
        if a.dry_run:
            continue
        dest.mkdir(parents=True, exist_ok=True)
        if not backup.exists():
            backup.mkdir()
            for f in dest.iterdir():
                if f.is_file():
                    shutil.copyfile(f, backup / f.name)
        (dest / 'engineering_data.csv').unlink(missing_ok=True)       # the synthetic file of 3 November; the data is now inside the notebook
        shutil.copyfile(PC.PROJECT / 'Notebooks' / code / 'ML_PROJECT_student.ipynb', dest / 'ML_PROJECT_student.ipynb')
        text = INSTRUCTIONS.format(code=code, window=PC.WINDOW_TEXT, last=PC.WINDOW['last_full_start'], own=PC.OWN_CELLS, support=PC.SUPPORT_HOURS)
        for name in ('ASSIGNMENT_INSTRUCTIONS.md', 'ASSIGNMENT_INSTRUCTIONS.txt', 'STUDENT_HOW_TO.md', 'TASKS.md'):
            (dest / name).write_text(text)


if __name__ == '__main__':
    main()
