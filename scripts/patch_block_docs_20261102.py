"""Student-facing and lecturer-facing text for the four-class arrangement of 2 November 2026 (idempotent).

  * student_guides/<cohort>/B1.md and B2.md are rewritten from data/assessment_blocks_20261102.json;
  * student_guides/<cohort>/TEST2.md gets a RETIRED notice, DEMO.md and ML_PROJECT.md lose the 15 December deadline;
  * Assignment_Instructions_Index.md and grader/README.md point to the new arrangement note.
Every file is backed up first (first copy wins) and every replacement asserts its match count.
Usage: python3 scripts/patch_block_docs_20261102.py"""
import json, re, sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from backup_20261102 import backup

ROOT = Path(__file__).resolve().parents[1]; BASE = ROOT / "IUEA_Teaching_Plan"
POL = json.loads((ROOT / "data" / "assessment_blocks_20261102.json").read_text())
COHORTS = ("CML3111", "CML3112", "CML3113"); MARK = "BLOCK_ASSESSMENT_20261102"
NOTE = "Block_Assessment_Arrangement_2026-11-02.md"


def pretty(iso):
    d = datetime.fromisoformat(iso); return f"{d.day} {d.strftime('%B %Y')}, {d.strftime('%H:%M')} Kampala"


def day(iso):
    d = datetime.fromisoformat(iso); return f"{d.strftime('%A')} {d.day} {d.strftime('%B')}"


def block_guide(code, b):
    rows = "\n".join(f"| {x['label']} (Class {3 if x['id'] == 'W10' else (b['classes'][-1] if b['id'] == 'B2' else b['weeks'].index(int(x['id'][1:])) + 1)}) | {x['title']} | {x['marks']} |" for x in b["assignment_parts"])
    forms = " and ".join(f"{q['form']} (Week {q['week']} content)" for q in b["quiz_forms"])
    c1, c2 = b["classes"]
    sit = day(b["quiz_sitting_date"][code]); demo = day(POL["calendar"]["week_12_demo"]["dates"][code])
    return f"""# {code} {b['label']}: what you hand in and when

<!-- {MARK} -->
{b['label']} covers Classes {c1} and {c2} of the second half of the semester: {b['topics']}.

## Assignment

You do the same assignment notebooks as before. They close together, so you can plan the block as one piece of work.

| Part | Topic | Marks |
|---|---|---|
{rows}
| Total | | {b['assignment_marks']} |

**All parts close:** {pretty(b['assignment_closes'][code])}. Each part has its own submission form, listed in the Assignment Submission Links file. A part you do not submit scores zero, so submit every part. You may submit the early parts as soon as you finish them.

## Quiz

One quiz sitting for the whole block: {forms}. It takes place in the last 20 minutes of Class {b['sitting_class']} ({sit}). The lecturer opens the two quiz forms together, and each stays open for 24 hours. Each form is worth 5 marks, so the block quiz is out of {b['quiz_marks']}.

## How it counts

Weeks 1 to 5 stay weekly, and Week 6 is waived. For those weeks your best 3 weekly quizzes and best 3 weekly assignments count. The two blocks always count in full. Quizzes are marked out of 35 (3 x 5 + 10 + 10) and assignments out of 160 (3 x 20 + 40 + 60). The quiz component is worth 15 percent of the course and the assignment component 15 percent.

There is no Practical Test 2 and no quiz or assignment after Block 2. The semester ends with a short project demo in Week 12 ({demo}). Its format, marks and the project dates will be confirmed by your lecturer.

The guided practice notebook for each class is for practice and is not submitted.
"""


def replace_once(text, old, new, where):
    assert text.count(old) == 1, f"{where}: expected exactly one match, found {text.count(old)}: {old[:60]!r}"
    return text.replace(old, new)


def patch_retired_notice(path, code):
    backup(path); t = path.read_text()
    if MARK in t: return
    notice = (f"<!-- {MARK} -->\n> **RETIRED on 2 November 2026.** There is no Practical Test 2. The semester now ends at Week 12 with a short project demo, "
              f"and the weights have changed. Ignore the instructions below. See [B2.md](B2.md) and your lecturer.\n\n")
    first, rest = t.split("\n", 1)
    path.write_text(first + "\n\n" + notice + rest.lstrip("\n"))


def patch_deadline(path, code):
    backup(path); t = path.read_text()
    if MARK in t: return
    t = re.sub(r"\*\*Deadline:\*\* \d+ December 2026, \d\d:\d\d Kampala\. The live form shows any later change\.",
               f"<!-- {MARK} -->\n**Deadline:** to be confirmed by the lecturer. The semester now ends at Week 12 (demo day {day(POL['calendar']['week_12_demo']['dates'][code])}); "
               "the 15 December date no longer applies. The live form shows any later change.", t, count=1)
    assert MARK in t, f"{path}: deadline line not found"
    path.write_text(t)


def main():
    import sys
    sys.exit('SUPERSEDED on 3 November 2026 by scripts/apply_policy_20261103.py. Running this script would overwrite the 3 November changes '
             '(the demo is removed and the ML project is submitted). The files it generated are still in place.')

    for code in COHORTS:
        for b in POL["blocks"]:
            p = BASE / "student_guides" / code / f"{b['id']}.md"; backup(p); p.write_text(block_guide(code, b))
        patch_retired_notice(BASE / "student_guides" / code / "TEST2.md", code)
        patch_deadline(BASE / "student_guides" / code / "DEMO.md", code)
        patch_deadline(BASE / "student_guides" / code / "ML_PROJECT.md", code)
    idx = BASE / "Assignment_Instructions_Index.md"; backup(idx); t = idx.read_text()
    m = re.search(r"(?s)<!-- BLOCK_ASSESSMENT_20261030 -->\n## Block arrangement from Week 8\n.*?(?=\n## |\Z)", t)
    add = (f"<!-- {MARK} -->\n## Block arrangement from Week 8 (updated 2 November 2026)\n\nTwo blocks of two classes: one assignment pack and one quiz sitting per block. "
           f"The semester ends at Week 12 and there is no Practical Test 2. Read [{NOTE}]({NOTE}). Student block guides: "
           + "; ".join(f"{c} [B1]({'student_guides/'+c+'/B1.md'}), [B2]({'student_guides/'+c+'/B2.md'})" for c in COHORTS) + ".\n")
    if MARK in t:
        t = re.sub(rf"(?s)<!-- {MARK} -->\n## Block arrangement.*?(?=\n## |\Z)", lambda _m: add, t, count=1)
    else:
        assert m, "old block section not found in the index"
        t = t[:m.start()] + add + t[m.end():]
    idx.write_text(t.rstrip() + "\n")
    rd = BASE / "grader" / "README.md"; backup(rd); t = rd.read_text()
    addr = (f"<!-- {MARK} -->\n## Block arrangement from Week 8 (updated 2 November 2026)\n\nThe best-of rules above apply to Weeks 1 to 5 only (best 3 of 5; Week 6 is waived). "
            "From Week 8 the A7 to A11 submissions and the Q7 to Q10 quizzes are combined per block and are never dropped: Block 1 = A7 + A8 (40 marks) and Q7 + Q8 (10); "
            "Block 2 = A9 + A10 + A11 (60 marks) and Q9 + Q10 (10). Q11 and Q12 are retired. Quizzes are out of 35 and assignments out of 160, 15 percent of the course each; "
            "Practical Test 2 is dropped. Each part is still graded by the same grader and form. "
            f"See `../{NOTE}` and `../../data/assessment_blocks_20261102.json`. Apps Script files: `apply_block_windows_20261102.gs`, `block_quiz_sittings_20261102.gs`, `create_quiz_forms.gs`.\n")
    if MARK in t:
        t = re.sub(rf"(?s)<!-- {MARK} -->\n## Block arrangement.*\Z", lambda _m: addr, t, count=1)
    else:
        old = re.search(r"(?s)<!-- BLOCK_ASSESSMENT_20261030 -->\n## Block arrangement from Week 8\n.*\Z", t)
        assert old, "old README block section not found"
        t = t[:old.start()] + addr
    rd.write_text(t.rstrip() + "\n")
    print("done")


if __name__ == "__main__":
    main()
