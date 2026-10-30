"""Apply the block assessment arrangement to the student-facing documents (idempotent).

Updates the Deadline line and adds a short block note in: student_guides/<cohort>/W08-W12.md, the assessment_banks
ASSIGNMENT_INSTRUCTIONS .md/.txt copies, and the same files plus SUBMIT_HERE.txt inside the Week 8-12 student ZIPs
(and the unzipped W08 folders). Writes student_guides/<cohort>/B1.md and B2.md, the policy document, an index
section, and a note in grader/README.md.   Usage: python3 scripts/patch_block_docs_20261030.py"""
import json, re, shutil, zipfile, tempfile
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]; BASE = ROOT / "IUEA_Teaching_Plan"
POL = json.loads((ROOT / "data" / "assessment_blocks_20261030.json").read_text())
COHORTS = ("CML3111", "CML3112", "CML3113"); MARK = "BLOCK_ASSESSMENT_20261030"
WEEK_BLOCK = {}
for b in POL["blocks"]:
    for p in b["assignment_parts"]: WEEK_BLOCK[int(p["id"][1:])] = (b, p)


def pretty(iso):
    d = datetime.fromisoformat(iso); return f"{d.day} {d.strftime('%B %Y')}, {d.strftime('%H:%M')} Kampala"


def note(code, week):
    b, p = WEEK_BLOCK[week]; n = len(b["assignment_parts"]); labels = ", ".join(x["label"] for x in b["assignment_parts"])
    weeks = f"Weeks {b['weeks'][0]} to {b['weeks'][-1]}"
    return (f"**Block assessment:** this is part {p['part']} of {n} of the {b['label']} assignment ({weeks}; parts {labels}). "
            f"All parts close together at the time above, and each part is marked out of {p['marks']}. "
            f"The {b['label']} quiz is one sitting: {b['quiz_sitting']} See [B{b['id'][1]}.md](B{b['id'][1]}.md).")


def patch_text(text, code, week, link_prefix=True):
    b, p = WEEK_BLOCK[week]; close = pretty(b["assignment_closes"][code])
    text = re.sub(r"(\*\*Deadline:\*\*) [^\n]*?Kampala\.", rf"\1 {close}.", text, count=1)
    if MARK in text: return text
    n = note(code, week)
    if not link_prefix: n = re.sub(r" See \[B\d\.md\]\(B\d\.md\)\.", "", n)
    return re.sub(r"(\*\*Deadline:\*\*[^\n]*\n)", rf"\1\n<!-- {MARK} -->\n{n}\n", text, count=1)


def patch_zip(path, code, week):
    b, p = WEEK_BLOCK[week]; close = b["assignment_closes"][code]; tmp = Path(tempfile.mkdtemp()) / path.name
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for it in zin.infolist():
            data = zin.read(it.filename)
            if it.filename in ("ASSIGNMENT_INSTRUCTIONS.md", "ASSIGNMENT_INSTRUCTIONS.txt"):
                data = patch_text(data.decode(), code, week, link_prefix=False).encode()
            elif it.filename == "SUBMIT_HERE.txt":
                t = data.decode(); t = re.sub(r"Closes: \S+", f"Closes: {close}", t)
                if MARK not in t:
                    t += (f"\n{MARK}: part {p['part']} of the {b['label']} assignment. All parts of the block close at the time above. "
                          f"The {b['label']} quiz is one sitting; your lecturer announces it in class.\n")
                data = t.encode()
            zout.writestr(it, data)
    shutil.move(str(tmp), path)


def patch_dir(d, code, week):
    for name in ("ASSIGNMENT_INSTRUCTIONS.md", "ASSIGNMENT_INSTRUCTIONS.txt"):
        f = d / name
        if f.exists(): f.write_text(patch_text(f.read_text(), code, week, link_prefix=False))
    f = d / "SUBMIT_HERE.txt"
    if f.exists():
        b, p = WEEK_BLOCK[week]; t = re.sub(r"Closes: \S+", f"Closes: {b['assignment_closes'][code]}", f.read_text())
        if MARK not in t: t += f"\n{MARK}: part {p['part']} of the {b['label']} assignment. All parts close at the time above.\n"
        f.write_text(t)


def block_guide(code, b):
    n = b["id"][1]; rows = "\n".join(f"| {x['label']} (Week {int(x['id'][1:])}) | {x['title']} | {x['marks']} |" for x in b["assignment_parts"])
    forms = ", ".join(f"Week {q['week']} quiz ({q['form']})" for q in b["quiz_forms"])
    return f"""# {code} {b['label']}: what you hand in and when

{b['label']} covers Weeks {b['weeks'][0]} to {b['weeks'][-1]}: {b['topics']}.

## Assignment

You do the same assignment notebooks as before. They now close together, so you can plan the block as one piece of work.

| Part | Topic | Marks |
|---|---|---|
{rows}
| Total | | {b['assignment_marks']} |

**All parts close:** {pretty(b['assignment_closes'][code])}. Each part has its own submission form, listed in the Assignment Submission Links file. A part you do not submit scores zero, so submit every part. You may submit the early parts as soon as you finish them.

## Quiz

One quiz sitting for the whole block: {forms}. {b['quiz_sitting']} Each form is worth 5 marks, so the block quiz is out of {b['quiz_marks']}.

## How it counts

Weeks 1 to 5 stay weekly, and Week 6 is waived. For those weeks your best 3 weekly quizzes and best 3 weekly assignments count. The two blocks always count in full. Quizzes are marked out of 45 and assignments out of 160. The quiz component is worth 10 percent of the course and the assignment component 10 percent.

The guided practice notebook for each week is for practice in class and is not submitted.
"""


def main():
    for code in COHORTS:
        for w in WEEK_BLOCK:
            g = BASE / "student_guides" / code / f"W{w:02d}.md"
            if g.exists(): g.write_text(patch_text(g.read_text(), code, w))
            d = BASE / "assessment_banks" / f"W{w:02d}" / code / "A"
            if d.exists(): patch_dir(d, code, w)
            z = BASE / "student_packages" / f"{code}_W{w:02d}_student.zip"
            if z.exists(): patch_zip(z, code, w)
            u = BASE / "student_packages" / f"{code}_W{w:02d}_student"
            if u.is_dir(): patch_dir(u, code, w)
        for b in POL["blocks"]:
            (BASE / "student_guides" / code / f"{b['id']}.md").write_text(block_guide(code, b))
    idx = BASE / "Assignment_Instructions_Index.md"; t = idx.read_text()
    if MARK not in t:
        add = (f"\n<!-- {MARK} -->\n## Block arrangement from Week 8\n\nFrom Week 8 there is one assignment pack and one quiz sitting after every three classes. "
               "Read [Block_Assessment_Arrangement_2026-10-30.md](Block_Assessment_Arrangement_2026-10-30.md). Student block guides: "
               + "; ".join(f"{c} [B1]({'student_guides/'+c+'/B1.md'}), [B2]({'student_guides/'+c+'/B2.md'})" for c in COHORTS) + ".\n")
        idx.write_text(t.rstrip() + "\n" + add)
    rd = ROOT / "IUEA_Teaching_Plan" / "grader" / "README.md"; t = rd.read_text()
    if MARK not in t:
        rd.write_text(t.rstrip() + f"\n\n<!-- {MARK} -->\n## Block arrangement from Week 8\n\nThe best-7-of-10 and best-9-of-11 rules above apply to Weeks 1 to 6 only. From Week 8 the A7 to A11 submissions and the Q7 to Q12 quizzes are combined per block (Block 1 = Weeks 8 to 10, Block 2 = Weeks 11 to 13) and are never dropped. Each part is still graded by the same grader and form. See `../Block_Assessment_Arrangement_2026-10-30.md` and `../../data/assessment_blocks_20261030.json`.\n")
    print("done")


if __name__ == "__main__":
    main()
