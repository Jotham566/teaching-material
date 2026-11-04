"""Add dated correction notes (additive only) to three lecturer notes whose text contradicts the decision of 4 November 2026.

Files: IUEA_Teaching_Plan/Grading_Update_By_Hand_2026-11-03.md, Block_Assessment_Arrangement_2026-11-03.md,
Block_Assessment_By_Hand_Checklist_2026-11-02.md. Nothing already written is changed; each file gets one marked block.
Originals go to a sibling _backup_2026-11-04 (as <name>.pre_audit if the name is taken). Idempotent."""
import shutil
from pathlib import Path
B = Path(__file__).resolve().parents[1] / "IUEA_Teaching_Plan"
MARK = "<!-- AUDIT_20261104 -->"


def backup(p):
    d = p.parent / "_backup_2026-11-04"; d.mkdir(exist_ok=True)
    dest = d / p.name
    if dest.exists(): dest = d / (p.name + ".pre_audit")
    if not dest.exists(): shutil.copy2(p, dest)


GRADING = f"""
{MARK}
> **Corrections of 4 November 2026 (stale-statement audit).** The project decision changed on 4 November: it is an INDIVIDUAL, TIMED (3 hours), fully AUTO-GRADED Colab sitting in Week 12, not a take-home. Read the text below with these corrections:
>
> - **Section 3, step 4 (ML_PROJECT).** The old upload form for ML_PROJECT in the submission project stays closed for good: never set a window on it. The project is collected by the Colab test collector (key `CML311x|ML_PROJECT`), and its window is a `Test windows` row set by `setMlProjectWindow(...)` after you confirm the sitting times. The steps are in `second_half/Project/deploy/DEPLOYMENT_STEPS.md`.
> - **Section 5, item 2 (due date).** There is no due date of Friday 11 December. The proposed sittings are CML3112 Tue 1 Dec 11:00 to 14:00, CML3113 Fri 4 Dec 08:00 to 11:00, CML3111 Fri 4 Dec 11:00 to 14:00. The 11 December value that remains in `data/assessment_blocks_20261103.json` (`engineering_ml_project.due`) is a placeholder that the file itself marks as superseded.
> - **Section 5, item 5 (rubric).** Part A (30) is 24 automatic hidden-check marks plus 6 automatic process-check marks, and Part B (15) is automatic too. There is no rubric and no manual marking; you read a spot-check list.
> - **Section 1, steps 3 and 6 and the arrangement note.** While the project is pending, `Final %` is blank and `Band` shows `No band yet` (that is what `grader/gradebook.gs` writes). The arrangement note says "Final % and Band stay blank" and the Excel copy `IUEA_ML_Gradebook_Semester1.xlsx` shows the word PENDING in both columns. Students see only the provisional line and `Project: PENDING`.
> - **Section 4 (what to tell students).** Use the individual timed sitting wording, which that section already has; the arrangement and the student guides are the same.
"""

ARRANGE = f"""

{MARK}
## Status after the stale-statement audit of 4 November 2026

- The "Not changed, and not verified" list above is out of date in two places. `Before_Each_Class_Checklist.md` and `Teaching_Progress.md` now describe the four-class calendar (updated 4 November), and `second_half/` (Plan_Weeks_8-12.pdf, the Class 4 deck wording, the lecturer guides) now states the individual timed sitting. `grader/rubrics/ML_PROJECT.json`, `rubrics/DEMO.json` and `specs/spec_ML_PROJECT.py` are listed as superseded in `grader/SUPERSEDED_README.md`.
- The sentence "Update of 4 November 2026" in the project section is the current rule. Ignore "take-home" and the 11 December due date wherever they remain in this note (the `due` placeholder in the JSON is superseded).
- The audit table is in `Stale_Documents_Audit_2026-11-04.md`.
"""

CHECK = f"""

{MARK}
> **Update of 4 November 2026.** Items D1 and D5 above are stale. The weights are now 15 / 15 / 10 / 15 / 45 (no demo, no Practical Test 2). The Engineering ML project is an individual, timed, auto-graded 3-hour Colab sitting in the Week 12 class slot, and there is no Week 12 demo. Tell the students that in Class 2 and Class 3 (wording in `Grading_Update_By_Hand_2026-11-03.md`, section 4). In D2, the DEMO and ML_PROJECT upload forms are not used; the project window is set in the collector (`second_half/Project/deploy/DEPLOYMENT_STEPS.md`).
"""

for name, block, where in (("Grading_Update_By_Hand_2026-11-03.md", GRADING, "after_title"),
                           ("Block_Assessment_Arrangement_2026-11-03.md", ARRANGE, "end"),
                           ("Block_Assessment_By_Hand_Checklist_2026-11-02.md", CHECK, "end")):
    p = B / name; t = p.read_text()
    if MARK in t: print("already", name); continue
    backup(p)
    if where == "after_title":
        first, rest = t.split("\n", 1); assert first.startswith("# ")
        t = first + "\n" + block + "\n" + rest.lstrip("\n")
    else:
        t = t.rstrip("\n") + "\n" + block
    p.write_text(t); print("patched", name)
