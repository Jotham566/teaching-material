"""Copy the project notebooks into the folder the test portal and the collector read. python3 tools/install_project_bank.py [--dry-run]

Run this ONLY at deployment, after build_project_notebooks.py --require-forms. It writes IUEA_Teaching_Plan/assessment_banks/ML_PROJECT/<cohort>/<A|B|C>/
(ML_PROJECT_student.ipynb, engineering_data.csv and the instruction files, the same layout as TEST1) and keeps any older files in _backup_2026-11-04/.
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
import project_contracts as K  # noqa: E402

INSTRUCTIONS = """{code} ML_PROJECT: Engineering ML project, supervised timed sitting ({sitting}).

1. Open the entry page, enter your name, Google email and Student Registration Number, and press Start test. Your 3 hours start then.
2. Press Open my test in Colab. Run the countdown cell, then the setup cell. The notebook creates your CSV; no upload is needed.
3. Complete Tasks 1 to 8 and the Part B memo form (Task 9). Choose Runtime, then Restart session and run all.
4. Run the last cell, click Submit test, open the form link, check your details and press Submit before your personal deadline.
Rules: the same as Practical Test 1. Individual work. No AI or outside help.
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    bank = PC.PLAN / 'assessment_banks/ML_PROJECT'
    for code in PC.CODES:
        for v in K.MARKED_VARIANTS:
            dest = bank / code / v
            backup = bank / code / '_backup_2026-11-04' / v
            print(('would install ' if a.dry_run else 'installing ') + str(dest))
            if a.dry_run:
                continue
            if dest.exists() and not backup.exists():
                shutil.copytree(dest, backup)
            dest.mkdir(parents=True, exist_ok=True)
            src = PC.PROJECT / 'Notebooks' / code / v
            for name in ('ML_PROJECT_student.ipynb', 'engineering_data.csv'):
                shutil.copyfile(src / name, dest / name)
            text = INSTRUCTIONS.format(code=code, sitting=PC.SITTING_TEXT[code])
            for name in ('ASSIGNMENT_INSTRUCTIONS.md', 'ASSIGNMENT_INSTRUCTIONS.txt', 'STUDENT_HOW_TO.md', 'TASKS.md'):
                (dest / name).write_text(text)


if __name__ == '__main__':
    main()
