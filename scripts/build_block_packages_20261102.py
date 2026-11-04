"""Rebuild the Week 8 to 12 student packages for the four-class arrangement of 2 November 2026
(data/assessment_blocks_20261102.json). Same design as build_block_packages_20261030.py, with the new blocks, deadlines and wording.

Per cohort and assignment week (8 to 12 = A7 to A11) it writes, from one template:
  student_guides/<cohort>/W0X.md                      (the same text, for the web copy)
  assessment_banks/W0X/<cohort>/A/ASSIGNMENT_INSTRUCTIONS.md and .txt
  the workflow cell of the assignment notebook (cell 1)
  student_packages/<cohort>_W0X_student.zip           (notebook, data, guided_practice.ipynb, START_HERE.md)
and moves closeAt in data/submission_links.json to the block deadline.
The graded notebook cells, the graders and the forms are not touched. Every file is backed up first (first copy wins). Idempotent."""
import json, sys, zipfile
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from backup_20261102 import backup

ROOT = Path(__file__).resolve().parents[1]; BASE = ROOT / "IUEA_Teaching_Plan"
POL = json.loads((ROOT / "data" / "assessment_blocks_20261103.json").read_text())
LINKS_PATH = ROOT / "data" / "submission_links.json"; LINKS = json.loads(LINKS_PATH.read_text())
COHORTS = ("CML3111", "CML3112", "CML3113"); WEEKS = (8, 9, 10, 11, 12)
PART = {int(p["id"][1:]): (b, p) for b in POL["blocks"] for p in b["assignment_parts"]}


def pretty(iso):
    d = datetime.fromisoformat(iso); return f"{d.day} {d.strftime('%B %Y')}, {d.strftime('%H:%M')} Kampala"


def day(iso):
    d = datetime.fromisoformat(iso); return f"{d.strftime('%A')} {d.day} {d.strftime('%B')}"


def content_weeks(b):
    w = b["weeks"]; return f"Weeks {w[0]} to {w[-1]}" if len(w) > 2 else f"Weeks {w[0]} and {w[1]}"


def guide(code, week, csvs, url):
    b, p = PART[week]; n = len(b["assignment_parts"])
    files = ", ".join([f"W{week:02}_student.ipynb"] + csvs)
    fname = f"W{week:02}"
    sit = day(b["quiz_sitting_date"][code])
    return f"""# {code} {p['label']}: {p['title']}

**{b['label']}, part {p['part']} of {n}** ({content_weeks(b)} content). Marked out of {p['marks']}. All {n} parts of the block close together.

**Deadline:** {pretty(b['assignment_closes'][code])}. The live form shows any later change.
**Submit:** ONE completed notebook (.ipynb) on this form: {url}
**Block quiz:** one sitting in the last 20 minutes of Class {b['sitting_class']} ({sit}), {len(b['quiz_forms'])} short quizzes, {b['quiz_marks']} marks.

## Do this

1. Keep these files together: {files}. In Colab choose File, then Open notebook, then Upload, and add the CSV files in the Files sidebar.
2. Run the data-loading cell first. Set STUDENT_ID to your Student Registration Number, keeping quotes and slashes. Keep COHORT="{code}".
3. Answer each numbered task under its prompt, keeping the required names. Use pandas inside the functions and return the published types.
4. Answer the written questions in the "My written evidence" cell in your own words. Label any supplied results as supplied.
5. Restart and run all cells from the top, then fix any errors.
6. Save the notebook as your registration number with slashes replaced by underscores, then _{fname}.ipynb.
7. Open the form, enter your Student Registration Number, upload the notebook, press Submit and keep the confirmation.

## Rules

- Submit only the notebook. Do not submit the ZIP, guided_practice.ipynb or the CSV files.
- Leave Team ID blank. The file must be at most 10 MB. A resubmission before the deadline replaces the earlier one and must be the complete notebook.
- guided_practice.ipynb is for practice in class. It is not marked.
- A part that is not submitted scores zero. Submit each part as you finish it.
"""


def patch_notebook(nb, text):
    src = "<!-- assignment-workflow -->\n" + text
    cells = nb["cells"]
    assert "assignment-workflow" in "".join(cells[1]["source"]), "workflow cell moved"
    cells[1]["source"] = src.splitlines(True)
    return nb


def main():
    for code in COHORTS:
        for week in WEEKS:
            b, p = PART[week]; d = BASE / "assessment_banks" / f"W{week:02}" / code / "A"
            csvs = sorted(x.name for x in d.glob("*.csv"))
            key = f"{code}|W{week:02}"; LINKS[key]["closeAt"] = b["assignment_closes"][code]
            text = guide(code, week, csvs, LINKS[key]["url"])
            gp_md = BASE / "student_guides" / code / f"W{week:02}.md"
            nbp = d / f"W{week:02}_student.ipynb"; zp = BASE / "student_packages" / f"{code}_W{week:02}_student.zip"
            targets = [gp_md, d / "ASSIGNMENT_INSTRUCTIONS.md", d / "ASSIGNMENT_INSTRUCTIONS.txt", nbp, zp]
            for t in targets: backup(t)
            gp_md.write_text(text)
            for ext in ("md", "txt"): (d / f"ASSIGNMENT_INSTRUCTIONS.{ext}").write_text(text)
            nb = patch_notebook(json.loads(nbp.read_text()), text)
            nbp.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n")
            clean = json.loads(json.dumps(nb))
            for c in clean["cells"]:
                if c["cell_type"] == "code": c["outputs"] = []; c["execution_count"] = None
            with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
                z.writestr("START_HERE.md", text)
                z.writestr(nbp.name, json.dumps(clean, ensure_ascii=False, indent=1) + "\n")
                for c in csvs: z.write(d / c, c)
                gpn = BASE / "guided_practice" / code / f"W{week:02}" / "guided_practice.ipynb"
                z.write(gpn, "guided_practice.ipynb")
    backup(LINKS_PATH)
    LINKS_PATH.write_text(json.dumps(LINKS, indent=2) + "\n")
    print("built", len(COHORTS) * len(WEEKS), "packages")


if __name__ == "__main__":
    main()
