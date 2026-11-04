# NOTE (4 November 2026): superseded by apply_policy_20261103.py, patch_docx_20261103.py and patch_project_sitting_20261104.py. It encodes the 2 November policy (Week 12 demo, 30/15 weights); its replacements assert old text that is no longer in the documents.
"""Patch the three syllabi, the master teaching plan (docx and xlsx) and the Weekly Quiz Operations Guide for the
approved arrangement of 2 November 2026 (data/assessment_blocks_20261102.json):

  * the semester ends at Week 12 (short project demo); Practical Test 2 and the Week 13 to 15 events are retired;
  * Weeks 8 to 11 content are Classes 1 to 4 (CML3112 Tue 3, 10, 17, 24 Nov; CML3113 and CML3111 Fri 6, 13, 20, 27 Nov);
  * Block 1 = A7 + A8 (40) and Q7 + Q8 (10), quiz sat in the last 20 minutes of Class 2;
    Block 2 = A9 + A10 + A11 (60) and Q9 + Q10 (10), quiz sat in the last 20 minutes of Class 4; Q11 and Q12 retired;
  * quizzes out of 35 marks, assignments out of 160 marks, weekly best 3 of 5 (Week 6 waived);
  * weights: quizzes 15, assignments 15, data analysis project 10, Practical Test 1 15, Engineering ML project 30,
    demonstration 15 = 100.
Wherever the plan or the policy file gives no mark scheme or date for the project or the demo, the text says
'to be confirmed by the lecturer'.

Safety rules followed here:
  * every original is copied once into a sibling _backup_2026-11-02 folder before it is saved (backup_20261102.py);
  * every string replacement asserts its match count and the run fails loudly (nothing is saved) if one is wrong;
  * a file that already carries the marker below is reported as 'already patched' and left alone (idempotent);
  * dates come from the policy file by the course code read from each document, never by file name.
Usage: python3 scripts/patch_block_docx_20261102.py            (all files)
       python3 scripts/patch_block_docx_20261102.py --dry-run  (run every assertion, save nothing)
"""
import copy
import json
import re
import sys
from datetime import datetime
from pathlib import Path

import docx
import openpyxl
from openpyxl.worksheet.cell_range import CellRange, MultiCellRange

sys.path.insert(0, str(Path(__file__).resolve().parent))
from backup_20261102 import backup  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "IUEA_Teaching_Plan"
POL = json.loads((ROOT / "data" / "assessment_blocks_20261102.json").read_text())
MARK = "BLOCK_DOCX_20261102"
TBC = "to be confirmed by the lecturer"
TBC_CAP = TBC[0].upper() + TBC[1:]
DRY = "--dry-run" in sys.argv

B1, B2 = POL["blocks"]
assert B1["id"] == "B1" and B2["id"] == "B2"
assert POL["weights_percent"] == dict(quizzes=15, assignments=15, data_analysis_project=10, practical_test_1=15,
                                     engineering_ml_project=30, demonstration=15)
assert sum(p["marks"] for p in B1["assignment_parts"]) == 40 and sum(p["marks"] for p in B2["assignment_parts"]) == 60
assert 3 * 5 + B1["quiz_marks"] + B2["quiz_marks"] == 35 and 3 * 20 + 40 + 60 == 160

COURSE = ("CML3112", "CML3113", "CML3111")
DEMO_DAY = {c: datetime.fromisoformat(POL["calendar"]["week_12_demo"]["dates"][c]) for c in COURSE}


def dmt(iso):
    d = datetime.fromisoformat(iso)
    return f"{d.day} {d.strftime('%B')} {d.strftime('%H:%M')}"


def long_day(code):
    d = DEMO_DAY[code]
    return f"{d.strftime('%A')} {d.day} {d.strftime('%B')}"


def short_day(code):
    d = DEMO_DAY[code]
    return f"{d.strftime('%a')} {d.day} {d.strftime('%b')}"


def short_day_of(iso_date):
    d = datetime.fromisoformat(iso_date)
    return f"{d.strftime('%a')} {d.day} {d.strftime('%b')}"


# =====================================================================================================
# docx helpers
# =====================================================================================================
def _runs_text(p):
    return "".join(r.text for r in p.runs)


def para_replace(p, old, new):
    """Replace the first occurrence of `old` in paragraph `p` across runs, keeping the first affected run's format."""
    runs = p.runs
    texts = [r.text for r in runs]
    full = "".join(texts)
    i = full.find(old)
    assert i >= 0, f"not found in paragraph: {old[:60]!r}"
    end = i + len(old)
    pos = 0
    first = last = None
    s_off = e_off = 0
    for idx, t in enumerate(texts):
        a, b = pos, pos + len(t)
        if first is None and i < b:
            first, s_off = idx, i - a
        if first is not None and end <= b:
            last, e_off = idx, end - a
            break
        pos = b
    assert first is not None and last is not None
    if first == last:
        t = texts[first]
        runs[first].text = t[:s_off] + new + t[e_off:]
    else:
        runs[first].text = texts[first][:s_off] + new
        for k in range(first + 1, last):
            runs[k].text = ""
        runs[last].text = texts[last][e_off:]


def set_para(p, text):
    if p.runs:
        p.runs[0].text = text
        for r in p.runs[1:]:
            r.text = ""
    else:
        p.add_run(text)


def set_cell(cell, text):
    ps = cell.paragraphs
    set_para(ps[0], text)
    for extra in ps[1:]:
        extra._p.getparent().remove(extra._p)


def delete_par(p):
    p._p.getparent().remove(p._p)


def delete_row(table, idx, expect_prefix=None):
    row = table.rows[idx]
    if expect_prefix is not None:
        assert row.cells[0].text.strip().startswith(expect_prefix), (row.cells[0].text, expect_prefix)
    row._tr.getparent().remove(row._tr)


def row_index(table, first_cell_text):
    labels = [r.cells[0].text.strip() for r in table.rows]
    assert labels.count(first_cell_text) == 1, (first_cell_text, labels)
    return labels.index(first_cell_text)


class Doc:
    def __init__(self, path):
        self.path = Path(path)
        self.d = docx.Document(self.path)

    @property
    def patched(self):
        return MARK in (self.d.core_properties.keywords or "")

    def paragraphs(self):
        seen = set()  # holds the elements themselves, so a proxy is never garbage-collected and its id reused
        for p in self.d.paragraphs:
            seen.add(p._p)
            yield p
        for t in self.d.tables:
            for row in t.rows:
                for c in row.cells:
                    for p in c.paragraphs:
                        if p._p in seen:
                            continue
                        seen.add(p._p)
                        yield p

    def count(self, old):
        return sum(_runs_text(p).count(old) for p in self.paragraphs())

    def replace(self, old, new, expect=1):
        n = self.count(old)
        assert n == expect, f"{self.path.name}: expected {expect} match(es) of {old[:70]!r}, found {n}"
        done = 0
        for p in list(self.paragraphs()):
            while old in _runs_text(p):
                para_replace(p, old, new)
                done += 1
                if old in new:
                    break
        assert done == expect, (done, expect, old[:60])

    def par_starting(self, prefix):
        hits = [p for p in self.paragraphs() if _runs_text(p).startswith(prefix)]
        assert len(hits) == 1, f"{self.path.name}: {len(hits)} paragraph(s) start with {prefix[:60]!r}"
        return hits[0]

    def set_whole(self, prefix, text):
        set_para(self.par_starting(prefix), text)

    def delete_starting(self, prefix):
        delete_par(self.par_starting(prefix))

    def table_by_header(self, first_cells):
        hits = [t for t in self.d.tables if [c.text.strip() for c in t.rows[0].cells][:len(first_cells)] == first_cells]
        assert len(hits) == 1, f"{self.path.name}: {len(hits)} tables with header {first_cells}"
        return hits[0]

    def save(self):
        self.d.core_properties.keywords = ((self.d.core_properties.keywords or "") + " " + MARK).strip()
        if DRY:
            return
        backup(self.path)
        self.d.save(self.path)


# =====================================================================================================
# 1. Syllabi
# =====================================================================================================
def patch_syllabus(path):
    D = Doc(path)
    if D.patched:
        print(f"{Path(path).name}: already patched")
        return
    t0 = D.d.tables[0]
    code = next(r.cells[1].text.strip() for r in t0.rows if r.cells[0].text.strip() == "Course code")
    assert code in COURSE, code
    day = long_day(code)
    close1, close2 = B1["assignment_closes"][code], B2["assignment_closes"][code]
    sit1, sit2 = B1["quiz_sitting_date"][code], B2["quiz_sitting_date"][code]
    end = f"{DEMO_DAY[code].day} {DEMO_DAY[code].strftime('%B')}"

    D.replace("45 contact hours · one 3-hour session per week · 15 study weeks",
              "36 contact hours (12 sessions of 3 hours) · one 3-hour session per week · 12 study weeks")
    D.replace("7 September – 18 December 2026", f"7 September – {end} 2026 (Week 12 demo day)")
    D.replace("Weeks 7 and 14 are the designated assessment weeks.",
              f"Week 7 is the designated assessment week and Week 12 is the short project demo ({day} for your cohort), "
              "which is where the semester ends. The week number names the content: Weeks 8 to 11 are Classes 1 to 4. "
              "Practical Test 2 and the Week 13 to 15 sessions no longer exist.")
    D.replace("forty per cent of your mark accumulates week by week rather than landing in one or two large events.",
              "fifty-five per cent of your mark (the quizzes, the assignments, the Data Analysis Project and Practical Test 1) "
              "is earned before the project demo rather than landing in one or two large events.")
    D.replace("Sixty-five per cent of the mark is individual. Both practical tests use a dataset you have not seen before, "
              "drawn from your own discipline. There is nothing to memorise for them and no past paper to revise from.",
              "Sixty per cent of the mark is individual (the quizzes, the assignments, Practical Test 1 and the demonstration; "
              f"how the demonstration is marked is {TBC}). Practical Test 1 uses a dataset you have not seen before, "
              "drawn from your own discipline. There is nothing to memorise for it and no past paper to revise from.")
    D.replace("Every teaching session ends with a five-minute quiz. A QR code goes up on the projector in the last five minutes,",
              "Each of Weeks 1 to 5 ends with a five-minute quiz. A QR code goes up on the projector in the last five minutes,")
    D.replace("There are twelve of them, one at the end of each teaching session in Weeks 1 to 6 and Weeks 8 to 13, and your best ten "
              "count at one per cent each. Weeks 7 and 14 are the practical tests and Week 15 is Demo Day, so those three weeks have no quiz.",
              "From Week 8 the quizzes are sat in two blocks of two classes. Block 1 (Q7 and Q8) is sat in the last 20 minutes of "
              f"Class 2 ({short_day_of(sit1)}) and Block 2 (Q9 and Q10) in the last 20 minutes of Class 4 ({short_day_of(sit2)}); "
              "the two forms of a block are opened together and each stays open for 24 hours. Nine quizzes are sat in all "
              "(Week 6 is waived, and Q11 and Q12 no longer exist). Practical Test 1 in Week 7 and the Week 12 demo have no quiz.")
    D.replace("Only your best ten of the twelve count, so two of them can go badly for any reason at all, and that is what covers "
              "illness, travel and a bad day. Third, if the room network fails, that week's quiz becomes a 24-hour asynchronous window "
              "and you will be told so before you leave the room.",
              "Of the five weekly quizzes in Weeks 1 to 5 only your best three count, so two of them can go badly for any reason at "
              "all, and that is what covers illness, travel and a bad day; the two block quizzes always count. Third, every block quiz "
              "form stays open for 24 hours, so if the room network fails you finish in that window and you will be told so before "
              "you leave the room.")
    D.replace("The rubrics for the two practical tests, the Data Analysis Project and the Week 15 demonstration are published at "
              "least one week before each is used.",
              "The rubrics for Practical Test 1 and the Data Analysis Project are published at least one week before each is used. "
              f"The mark scheme for the Week 12 demonstration is {TBC}, and will be published before the demo.")
    D.replace("In Week 15 every student submits two individual typed defence answers about their own contribution and a technical "
              "decision, citing specific repository cells or results. The individual defence and reflection mark is separate from "
              "shared project marks. Live questions and peer comments provide formative feedback.",
              f"Any individual defence or reflection that goes with the Week 12 demo is {TBC}. Whatever is set, an individual mark "
              "stays separate from shared project marks, and live questions and peer comments provide formative feedback.")
    D.replace("In both practical tests, AI assistance is prohibited. Test 1 is a take-home practical followed by an understanding "
              "check, in which you may be asked to explain your code or change it without help. Test 2 follows the invigilator's rules. ",
              "In Practical Test 1, AI assistance is prohibited. Test 1 is a take-home practical followed by an understanding "
              "check, in which you may be asked to explain your code or change it without help. ")
    D.replace("Each quiz is worth one per cent and it exists to tell you, and me, whether you have kept up. Thirty-five per cent of "
              "your mark sits in the two offline tests. If your quiz scores are strong and your test scores are not, the quizzes were "
              "not doing you any good, and we should talk before Week 14 rather than after it.",
              "The quizzes are out of 35 marks and are worth 15 per cent of the course, and they exist to tell you, and me, whether "
              "you have kept up. Fifteen per cent of your mark sits in Practical Test 1, which is unaided. If your quiz scores are "
              "strong and your test score is not, the quizzes were not doing you any good, and we should talk before the project "
              "demo rather than after it.")
    D.replace("The project is set in Week 9 and runs to Week 15, with graded milestones in Weeks 10, 11, 12 and 13, so it is built "
              "continuously rather than in the last fortnight. Your team chooses its own problem, subject to approval, and finds or is "
              "given its own data. Examples of the scope expected:",
              "The project brief is given in Class 4 (Week 11 content) and the work is shown in a short demo in Week 12. The "
              f"milestones, the due date and the mark scheme are {TBC}. The proposal is that teams use the cohort data and the "
              "steps of Classes 1 to 4: clean, split, baseline, two or more models, a fair comparison, open the sealed test group once, "
              f"and write a one-page decision memo. Whether a team may choose its own problem is {TBC}. Examples of the scope expected:")
    D.replace("In Week 15 there are prizes for Best Engineering Reasoning, Best Investigation and Most Honest Limitations. There is "
              "deliberately no prize for the highest accuracy.",
              f"Whether any recognition is given at the Week 12 demo is {TBC}; if it is, there is deliberately no prize for the "
              "highest accuracy.")
    D.replace("Eleven small pieces of work spread across twelve weeks is a manageable load; nine of them attempted in December is not, "
              "and the two practical tests will find you out. The weekly work is the rehearsal for the tests, which is why the best "
              "eight of eleven count.",
              "Five weekly assignments in Weeks 1 to 5 and then two block packs is a manageable load; all of it attempted at the end "
              "is not, and the project demo will find you out. The weekly work is the rehearsal for the test and the project, which "
              "is why the best three of the five weekly assignments count and the two blocks always count.")
    D.replace("and the viva makes the difference visible.", "and the questions at the Week 12 demo make the difference visible.")
    D.replace("you will be unable to answer a single viva question.", "you will be unable to answer a single question at the Week 12 demo.")
    D.replace("The tests certify what you can do unaided.", "The test certifies what you can do unaided.")
    D.replace("Syllabus version 1.0 · drafted 1 September 2026 ·",
              "Syllabus version 1.1 · drafted 1 September 2026 · revised 2 November 2026 for the four-class second half and the Week 12 demo ·")

    # learning-outcome table
    t1 = D.table_by_header(["#", "Outcome", "Mainly assessed by"])
    for row in t1.rows[1:]:
        c = row.cells[2]
        if c.text == "Practical Test 2; Project methodology and validation":
            set_cell(c, "Block 1 and Block 2 assignments and quizzes; Project methodology and validation")
        elif c.text == "Practical Test 2 interpretation questions; Project validation":
            set_cell(c, "A9 (validation and trust) and the Block 2 quiz; Project validation")
        elif c.text == "AI-use declaration; viva":
            set_cell(c, "AI-use declaration; questions at the Week 12 demo")
        elif c.text == "Project; Demonstration and peer review":
            set_cell(c, "Project; Week 12 demonstration")
    assert not any("Practical Test 2" in r.cells[2].text for r in t1.rows)

    # weekly schedule
    tw = D.table_by_header(["Wk", "Date", "Topic", "Challenge segment", "Quiz", "Your deliverable"])
    rows = {r.cells[0].text.strip(): r for r in tw.rows[1:]}
    assert set(rows) == {str(i) for i in range(1, 16)}, sorted(rows)
    set_cell(rows["6"].cells[4], "Quiz 6 (waived)")
    assert rows["6"].cells[5].text.startswith("A6 ·")
    set_cell(rows["6"].cells[5], rows["6"].cells[5].text + " (waived)")
    spec = {
        "8": ("Tue 3 / Fri 6 Nov", "Class 1 · Learning from data: the first model", None,
              "No quiz (Block 1 quiz in Class 2)", "A7 · Regression with a baseline comparison · Block 1, part A"),
        "9": ("Tue 10 / Fri 13 Nov", "Class 2 · Classification: predicting a category", None,
              "Block 1 quiz: Q7, Q8 (one sitting, last 20 minutes)", "A8 · Classifier and cost table · Block 1, part B"),
        "10": ("Tue 17 / Fri 20 Nov", "Class 3 · Can I trust this model? Validation and data leakage", None,
               "No quiz (Block 2 quiz in Class 4)", "A9 · Trust Lab and conditions of use · Block 2, part A"),
        "11": ("Tue 24 / Fri 27 Nov", "Class 4 · Features, choosing a model and the project brief", None,
               "Block 2 quiz: Q9, Q10 (one sitting, last 20 minutes)",
               "A10 · Feature dictionary and ablation table · Block 2, part B; A11 · One-page recommendation · Block 2, part C"),
        "12": ("Tue 1 / Fri 4 Dec", "Short project demo (proposal, not final)", "The demo", "—",
               f"Team demo of about five minutes with questions from the class; mark scheme {TBC}. Block 2 pack (A9, A10, A11) closes "
               f"{dmt(close2)}"),
    }
    for wk, (date, topic, challenge, quiz, deliv) in spec.items():
        cells = rows[wk].cells
        assert re.match(r"^(Tue|Fri)", cells[1].text), cells[1].text
        set_cell(cells[1], date)
        set_cell(cells[2], topic)
        if challenge:
            set_cell(cells[3], challenge)
        set_cell(cells[4], quiz)
        set_cell(cells[5], deliv)
    for wk in ("15", "14", "13"):
        delete_row(tw, row_index(tw, wk))

    # assessment table
    ta = D.table_by_header(["Component", "When", "Mode", "Weight"])
    by = {r.cells[0].text.strip(): r for r in ta.rows[1:]}
    q = by["Quizzes: weekly, then one per block"].cells
    set_cell(q[0], "Quizzes: weekly in Weeks 1–5, then one sitting per block")
    set_cell(q[1], "Weeks 1–5 weekly; Block 1 (Q7, Q8) in the last 20 minutes of Class 2; Block 2 (Q9, Q10) in the last 20 minutes of Class 4")
    set_cell(q[3], "15%")
    set_cell(q[4], "Five multiple-choice questions on your phone per form, auto-marked with immediate feedback. Weeks 1 to 5 are weekly "
             "five-minute quizzes. From Week 8 the two forms of a block are sat together (Block 1: Q7 and Q8; Block 2: Q9 and Q10), each "
             "form open for 24 hours. Week 6 is waived, so the best 3 of the five weekly quizzes count; both blocks always count. Q11 and "
             "Q12 are retired. The total is 35 marks (3 x 5 + 10 + 10) and the component is worth 15%.")
    a = by["Practical challenges and assignments"].cells
    set_cell(a[1], f"Weekly in Weeks 1–5; Block 1 pack (A7, A8) closes {dmt(close1)}; Block 2 pack (A9, A10, A11) closes {dmt(close2)} (Kampala time)")
    set_cell(a[3], "15%")
    set_cell(a[4], "Week 6 is waived, so the best 3 of the five weekly assignments count. Block 1 is two parts (A7, A8; 40 marks) and "
             "Block 2 is three parts (A9, A10, A11; 60 marks); each part uses the same assignment form as before, and a part not "
             "submitted scores zero. Both blocks always count. The total is 160 marks (3 x 20 + 40 + 60) and the component is worth 15%. "
             "Upload the required notebook and report through the assignment form. Visible checks provide practice feedback; final "
             "marks use the submitted files.")
    p = by["Engineering ML Project"].cells
    set_cell(p[1], f"Brief in Class 4 (Week 11 content); short demo in Week 12; due date and milestones {TBC}")
    set_cell(p[3], "30%")
    set_cell(p[4], "Proposal, not final: a repository and a one-page decision memo built on the steps of Classes 1 to 4. Milestones, "
             f"due date and mark scheme are {TBC}.")
    dmo = by["Demonstration, viva and reflection"].cells
    set_cell(dmo[0], "Week 12 short project demonstration")
    set_cell(dmo[1], f"Week 12 ({short_day(code)})")
    set_cell(dmo[2], f"Individual ({TBC})")
    set_cell(dmo[3], "15%")
    set_cell(dmo[4], f"A short team demo of about five minutes, with questions from the class. Mark scheme {TBC}. Live questions are formative.")
    delete_row(ta, row_index(ta, "Practical Test 2 — End-to-End ML"))
    weights = [r.cells[3].text for r in ta.rows[1:]]
    assert sum(int(w.rstrip("%")) for w in weights) == 100, weights

    # tools table: scikit-learn weeks and the Week 13 row
    tt = D.table_by_header(["Week", "Tool", "The problem it solves"])
    for row in tt.rows[1:]:
        if row.cells[0].text.strip() == "8–12":
            set_cell(row.cells[0], "8–11")
        elif row.cells[0].text.strip() == "13":
            set_cell(row.cells[0], f"12 ({TBC})")
    D.save()
    print(f"{Path(path).name}: patched ({code})")


# =====================================================================================================
# 2. Master teaching plan docx
# =====================================================================================================
def patch_master_docx(path):
    D = Doc(path)
    if D.patched:
        print(f"{Path(path).name}: already patched")
        return
    r = D.replace
    r("7 September – 18 December 2026   ·   15 study weeks", "7 September – 4 December 2026   ·   12 study weeks")
    r("45 contact hours each", "36 contact hours each")
    r("Version 1.0  ·  drafted 1 September 2026  ·  for Faculty review",
      "Version 1.1  ·  drafted 1 September 2026  ·  revised 2 November 2026  ·  for Faculty review")
    r("It fixes the architecture of the thirteen teaching weeks and the two assessment weeks.",
      "It fixes the architecture of the twelve weeks, which end with the Week 12 project demo.")
    r("and the two practical tests in Weeks 7 and 14 are computer-based. If one laboratory cannot seat and equip a hundred students "
      "simultaneously, the tests require either",
      "and the practical test in Week 7 is computer-based. If one laboratory cannot seat and equip a hundred students "
      "simultaneously, the test requires either")
    D.set_whole("The semester runs for fifteen study weeks",
                "The semester runs for twelve study weeks from Monday 7 September 2026, ending at the Week 12 project demo (Tuesday "
                "1 December for CML3112, Friday 4 December for CML3113 and CML3111), and thirty-six contact hours in total. The week "
                "number names the content: Weeks 8 to 11 are Classes 1 to 4, taught on Tue 3, 10, 17 and 24 November for CML3112 and "
                "Fri 6, 13, 20 and 27 November for CML3113 and CML3111. The one assessment week is Week 7. Practical Test 2 and the "
                "Week 13 to 15 events were retired on 2 November 2026.")
    r("and four sessions are almost entirely so: the Investigation Lab in Week 4, the Ten Questions round in Week 5, the 97% Trap in "
      "Week 9 and the Engineering AI Challenge in Week 12.",
      "and three sessions are almost entirely so: the Investigation Lab in Week 4, the Ten Questions round in Week 5 and the 97% Trap in Week 9.")
    r("They appear explicitly in Weeks 2, 3, 4, 5, 6, 10 and 13, and they carry marks.",
      "They appear explicitly in Weeks 2, 3, 4, 5, 6 and 10, and they carry marks.")
    r("for each of the fifteen weeks, exactly what is common", "for each of the weeks, exactly what is common")
    r("concentrated almost entirely in Weeks 4 through 7 and in the two assessment weeks, because that is where teaching datasets must "
      "be authored from scratch. Weeks 2 and 13 require no divergent preparation whatsoever.",
      "concentrated almost entirely in Weeks 4 through 7, because that is where teaching datasets must be authored from scratch. "
      "Week 2 requires no divergent preparation whatsoever.")
    D.set_whole("The implication for planning is that the unseen test datasets",
                "The implication for planning is that the unseen test datasets are the largest single item of work in the semester. "
                "Three matched variants per cohort means nine for Practical Test 1, each with a model answer and a mark scheme. They "
                "should be built during the low-divergence weeks, Weeks 2 to 5, rather than in the fortnight before the test, when there "
                "will be no time. Practical Test 2 was dropped on 2 November 2026, so there is no second set.")
    r("The thirteen teaching weeks fall into five blocks.", "The twelve weeks fall into four blocks.")
    r("Block 3 · Weeks 8–10 · The machine learning core", "Block 3 · Weeks 8–11 · The machine learning core (Classes 1 to 4)")
    D.delete_starting("Block 4 · Weeks 11–12 · Practical judgement")
    p92 = D.par_starting("Week 11 is where domain knowledge formally enters the model.")
    set_para(p92, _runs_text(p92) + " Class 4 also teaches choosing between models: ridge and nearest neighbours as previews, a fair "
             "comparison of five candidates under one protocol, the decision memo, the sealed test group and the project brief. "
             "Support vector machines, random forests, boosting, clustering and neural networks are named and moved to next semester.")
    D.delete_starting("Week 12 is the least guided session before the test")
    r("Block 5 · Weeks 13–15 · Project, test and demonstration", "Block 4 · Week 12 · Short project demo")
    D.set_whole("Week 13 treats reproducibility as a professional obligation.",
                "Week 12 (Tuesday 1 December for CML3112, Friday 4 December for CML3113 and CML3111) is a short project demo. This is a "
                "proposal and not final. Each team presents for about five minutes with questions from the class, using the cohort data "
                "and the steps of Classes 1 to 4: clean, split, baseline, two or more models, a fair comparison, the sealed test group "
                "opened once, and a one-page decision memo. The marks, the mark scheme, the running order, the room, the team and "
                f"individual arrangements, any recognition awards and any reproducibility check are {TBC}.")
    D.delete_starting("Week 14 is the second practical test")
    D.delete_starting("Week 15 is Demo Day.")
    D.set_whole("Two tests rather than one is a change from the original curriculum sketch",
                "One practical test rather than two follows from the semester ending at Week 12: Practical Test 2 was dropped on 2 "
                "November 2026. Week 7 certifies data literacy. The end-to-end work of Weeks 8 to 11 is now assessed in the Block 1 and "
                f"Block 2 assignments and quizzes and shown in the Week 12 project demo, whose mark scheme is {TBC}.")
    D.set_whole("Sixty-five per cent of the mark is individual.",
                "Sixty per cent of the mark is individual on the component modes in the table above (the quizzes, the assignments, "
                f"Practical Test 1 and the demonstration; the demonstration mode is {TBC}). With teams of four to five and up to "
                "twenty-two teams in the largest cohort, a team-heavy scheme would allow a weak student to pass on a strong teammate's "
                "work. An individual test, individually marked assignments and quizzes, and individual evidence in the demonstration "
                "make the team component safe to award — and they make the rotating team roles and contribution logs meaningful rather "
                "than decorative.")
    r("Continuous assessment: the twelve weekly quizzes", "Continuous assessment: the quizzes")
    D.set_whole("Every teaching session closes with a five-minute quiz",
                "A quiz is five multiple-choice questions, delivered by a QR code on the projector, taken on the students' own phones, "
                "auto-marked, with the score and a teaching comment released the moment they submit. Weeks 1 to 5 each close with a "
                "five-minute quiz in the last five minutes, and the best three of the five count; Week 6 is waived for all three cohorts. "
                "The Week 2 proof-of-life submission separately verifies that each student can run and save the supplied notebook. From "
                "Week 8 the quizzes and assignments are set in two assessment blocks of two classes. Block 1 (Classes 1 and 2) has the "
                "Q7 and Q8 forms, opened together in the last twenty minutes of Class 2; Block 2 (Classes 3 and 4) has Q9 and Q10, opened "
                "together in the last twenty minutes of Class 4. Each form is five questions and five marks and stays open for 24 hours, "
                "and neither block can be dropped. Q11 and Q12 are retired. The quiz total is 35 marks (3 x 5 + 10 + 10), worth 15% of "
                "the course. Assignments follow the same rule: the best 3 of the five weekly assignments, Block 1 (A7 + A8 = 40 marks) and "
                "Block 2 (A9 + A10 + A11 = 60 marks), a total of 160 marks, worth 15%. Full details: "
                "Block_Assessment_Arrangement_2026-11-02.md.")
    r("The quizzes in Weeks 12 and 13 draw two of their five questions from the Week 1 to Week 10 banks, which is what keeps the set cumulative.",
      "The Week 11 quiz (Q10) takes two of its five questions from the retired Q11 model-comparison bank, which keeps the set cumulative.")
    r("And there are no resits: only the best ten of the twelve count,", "And there are no resits: only the best three of the five weekly quizzes count,")
    r("each quiz is worth one per cent, three parallel versions", "each quiz mark is a small part of the 35-mark quiz total, three parallel versions")
    r("Thirty-five per cent of the mark sits in the two offline tests, and that is where unaided capability is certified.",
      "Fifteen per cent of the mark sits in Practical Test 1, and that is where unaided capability is certified.")
    r("The following mapping produces a forty–sixty split without altering a single teaching session; only the recorded category changes.",
      "Recording each component's category under the new weights gives a fifty-five / forty-five split without altering a single "
      "teaching session. If IUEA mandates a different split, for example forty–sixty, the mapping has to be redrawn, and that is "
      f"{TBC} against IUEA regulations.")
    r("forty per cent of the mark is now genuinely continuous, accumulated across eleven weekly submissions and twelve weekly quizzes rather than concentrated in one or two events.",
      "fifty-five per cent of the mark is now genuinely continuous, accumulated across five weekly assignments, five weekly quizzes, two "
      "block packs, two block quiz sittings, a team project and a practical test, rather than concentrated in one or two events.")
    r("Six rubrics are published in full in the workbook", "Five rubrics are published in full in the workbook")
    r("ten to communication and five to reproducibility.",
      f"ten to communication and five to reproducibility. The rubric for the Week 12 demonstration is {TBC}.")
    r("Use is prohibited in both practical tests, which run in Colab.", "Use is prohibited in Practical Test 1, which runs in Colab.")
    r("the tests certify what you can do unaided.", "the test certifies what you can do unaided.")
    r("which rests on the sixty-five per cent individual mark, the contribution log with repository evidence, and two individual typed "
      "defence answers in Week 15.",
      "which rests on the sixty per cent individual mark, the contribution log with repository evidence, and any individual defence at "
      f"the Week 12 demo ({TBC}).")
    D.set_whole("Two sessions need explicit crowd logistics",
                "One session needs explicit crowd logistics rather than good intentions. The Week 12 project demo, with about twenty-two "
                "teams in Cohort A at five minutes each, is roughly a hundred and ten minutes before a single question is asked, so its "
                f"format, running order and any parallel rooms are {TBC}.")
    r("Gradient boosting is shown for one minute in Week 12 and then explicitly deferred.",
      "Support vector machines, random forests, boosting, clustering and neural networks are named in the class decks and explicitly deferred.")
    r("And each practical test needs three matched unseen variants per cohort — nine per test, eighteen in total, each with a model answer and a mark scheme.",
      "And Practical Test 1 needs three matched unseen variants per cohort — nine in total, each with a model answer and a mark scheme.")
    r("The nine dataset variants for each assessment week — eighteen across the semester — are the largest single item of work and the "
      "easiest to defer. They must be built in the quiet weeks, Weeks 2 to 5 for the first test and Weeks 8 to 12 for the second, because "
      "the fortnight before an assessment week is precisely when there is no capacity to author nine datasets of matched difficulty and "
      "nine mark schemes.",
      "The nine dataset variants for Practical Test 1 are the largest single item of work and the easiest to defer. They had to be built "
      "in the quiet weeks, Weeks 2 to 5, because the fortnight before an assessment week is precisely when there is no capacity to author "
      "nine datasets of matched difficulty and nine mark schemes. There is no second set, because Practical Test 2 is dropped.")
    r("and the Week 15 reflection, which requires each student to name two goals for the second semester, is the natural input to its detailed design.",
      "and an end-of-semester reflection that asks each student to name two goals for the second semester, if the lecturer sets one "
      f"({TBC}), is the natural input to its detailed design.")
    r("Appendix A · The fifteen weeks at a glance", "Appendix A · The twelve weeks at a glance", expect=2)
    r("It is worth putting on a slide in Week 1 and again in Week 15,", "It is worth putting on a slide in Week 1 and again in Week 12,")

    # ---- tables
    cal = D.table_by_header(["Wk", "Commencing", "Tuesday slot", "Friday slots"])
    cr = {row.cells[0].text.strip(): row for row in cal.rows[1:]}
    calspec = {
        "8": ("2 Nov", "Tue 3 Nov", "Fri 6 Nov", "Teaching",
              "Class 1 (Week 8 content). The Friday cohorts were taught the Week 8 concepts without the lab on Fri 30 Oct; for them Class 1 is a "
              "recap and the lab. CML3112 starts Week 8 on Tue 3 Nov."),
        "9": ("9 Nov", "Tue 10 Nov", "Fri 13 Nov", "Teaching", "Class 2 (Week 9 content). Block 1 quiz (Q7, Q8) in the last 20 minutes."),
        "10": ("16 Nov", "Tue 17 Nov", "Fri 20 Nov", "Teaching",
               "Class 3 (Week 10 content). Block 1 assignment (A7, A8) closes: CML3112 Tue 17 Nov 11:00; CML3113 Fri 20 Nov 08:00; CML3111 Fri 20 Nov 11:00."),
        "11": ("23 Nov", "Tue 24 Nov", "Fri 27 Nov", "Teaching", "Class 4 (Week 11 content). Block 2 quiz (Q9, Q10) in the last 20 minutes. Project brief."),
        "12": ("30 Nov", "Tue 1 Dec", "Fri 4 Dec", "Demo",
               "Week 12: short project demo. Block 2 assignment (A9, A10, A11) closes: CML3112 Tue 1 Dec 11:00; CML3113 Fri 4 Dec 08:00; "
               f"CML3111 Fri 4 Dec 11:00. Marks and arrangements: {TBC}."),
    }
    for wk, vals in calspec.items():
        for ci, v in enumerate(vals, start=1):
            set_cell(cr[wk].cells[ci], v)
    for wk in ("15", "14", "13"):
        delete_row(cal, row_index(cal, wk))

    at = D.table_by_header(["Component", "When", "Mode", "Weight"])
    ar = {row.cells[0].text.strip().split(" (")[0]: row for row in at.rows[1:]}
    q = ar["Quizzes"].cells
    set_cell(q[0], "Quizzes (weekly in Weeks 1–5; one sitting per block from Week 8)")
    set_cell(q[1], "W1–W5 weekly; last 20 minutes of Class 2 (Block 1: Q7, Q8) and of Class 4 (Block 2: Q9, Q10)")
    set_cell(q[3], "15%")
    a = ar["Practical challenges and assignments"].cells
    set_cell(a[0], "Practical challenges and assignments (weekly in Weeks 1–5; two block packs from Week 8)")
    set_cell(a[1], "Weeks 1–5; Block 1 (A7, A8); Block 2 (A9, A10, A11)")
    set_cell(a[3], "15%")
    p = ar["Engineering ML Project"].cells
    set_cell(p[1], f"Brief in Class 4 (Week 11 content); demo in W12; due date and milestones: {TBC}")
    set_cell(p[3], "30%")
    dmo = ar["Demonstration, viva and individual reflection"].cells
    set_cell(dmo[0], "Week 12 short project demonstration")
    set_cell(dmo[1], "Week 12")
    set_cell(dmo[2], f"Individual ({TBC})")
    set_cell(dmo[3], "15%")
    ind = [row for row in at.rows if row.cells[0].text.startswith("Individual share")][0]
    team = [row for row in at.rows if row.cells[0].text.startswith("Team share")][0]
    set_cell(ind.cells[3], "60%")
    set_cell(team.cells[3], "40%")
    delete_row(at, row_index(at, "Practical Test 2 — End-to-End Engineering ML"))
    comps = [row for row in at.rows[1:] if row.cells[3].text.strip().endswith("%") and not row.cells[0].text.startswith(("Individual", "Team"))]
    assert sum(int(row.cells[3].text.strip().rstrip("%")) for row in comps) == 100, [row.cells[3].text for row in comps]

    mp = D.table_by_header(["Category", "Components", "Weight"])
    mrows = {row.cells[0].text.split(" (")[0]: row for row in mp.rows[1:]}
    set_cell(mrows["Continuous assessment"].cells[0], "Continuous assessment (55%)")
    set_cell(mrows["Continuous assessment"].cells[1], "Quizzes 15% · Practical challenges and assignments 15% · Data Analysis Project 10% · Practical Test 1 15%")
    set_cell(mrows["Continuous assessment"].cells[2], "55%")
    set_cell(mrows["Final assessment"].cells[0], "Final assessment (45%)")
    set_cell(mrows["Final assessment"].cells[1], "Engineering ML Project 30% · Week 12 demonstration 15%")
    set_cell(mrows["Final assessment"].cells[2], "45%")

    ml = D.table_by_header(["Item", "Volume", "Illustrative human hours", "Automated workflow hours"])
    mlr = {row.cells[0].text.strip(): row for row in ml.rows[1:]}
    set_cell(mlr["Weekly practical challenges"].cells[1], "10 x ~195")
    set_cell(mlr["Weekly practical challenges"].cells[2], "98")
    set_cell(mlr["Weekly quizzes"].cells[1], "9 x ~195")
    dm_ = mlr["Demo and reflection"].cells
    set_cell(dm_[0], "Week 12 short project demo")
    set_cell(dm_[1], "43 teams")
    set_cell(dm_[2], TBC)
    delete_row(ml, row_index(ml, "Practical Test 2"))

    tl = D.table_by_header(["Tool", "Week", "The problem it solves"])
    for row in tl.rows[1:]:
        if row.cells[0].text.strip() == "Hyperparameter search":
            set_cell(row.cells[0], "Fair model comparison")
            set_cell(row.cells[1], "11")
        elif row.cells[0].text.strip().startswith("Environment capture"):
            set_cell(row.cells[1], f"12 ({TBC})")

    rk = D.table_by_header(["ID", "Risk", "Mitigation"])
    for row in rk.rows[1:]:
        idc = row.cells[0].text.strip()
        if idc == "R2":
            set_cell(row.cells[1], "Cohort A (~100) exceeds one lab's capacity, making the Week 7 test unrunnable in a single sitting.")
        elif idc == "R6":
            set_cell(row.cells[2], "Retain individual marks and rotating roles. Require contribution evidence. Any individual defence at the Week 12 demo is "
                     f"{TBC}. Live questioning is formative; repository evidence checks remain a release requirement.")
        elif idc == "R13":
            set_cell(row.cells[2], "The best-3-of-5 rule for the weekly quizzes and the 24-hour block window do not replace a fair attempt opportunity. "
                     "Announce and configure an equivalent replacement window after an outage; retain the change reason and do not silently assign "
                     "a zero. Printed questions support practice while verified collection is restored.")

    nx = D.table_by_header(["#", "Deliverable", "Needed by", "Note"])
    nrows = {row.cells[0].text.strip(): row for row in nx.rows[1:]}
    c = nrows["2c"].cells
    set_cell(c[1], "The remaining quiz banks (Q3 to Q10; Q11 and Q12 are retired), five questions each, built in Forms in three versions")
    set_cell(c[2], "Weeks 3–11")
    c = nrows["7"].cells
    set_cell(c[1], "Lesson plans, slides, notebooks and lecturer guides for Classes 1 to 4 (Weeks 8–11 content)")
    set_cell(c[2], "Before each class")
    set_cell(c[3], "Built; see IUEA_Teaching_Plan/second_half/. Run each notebook once in real Colab before the class.")
    c = nrows["8"].cells
    set_cell(c[2], "Class 4 (Week 11 content)")
    set_cell(c[3], f"The project brief is given in Class 4. Milestones and due dates: {TBC}.")
    c = nrows["9"].cells
    set_cell(c[1], "Week 12 project demo arrangements: format, running order, room, marks and mark scheme")
    set_cell(c[2], TBC_CAP)
    set_cell(c[3], TBC_CAP + ".")
    c = nrows["12"].cells
    set_cell(c[3], "Needed while Semester 1 evidence is fresh, and before the semester ends.")
    for num in ("11", "10"):  # Week 15 viva bank, then Practical Test 2 variants
        delete_row(nx, row_index(nx, num))

    gl = D.table_by_header(["Wk", "Block", "Topic", "Under-guided segment", "Quiz", "Milestone"])
    gr = {row.cells[0].text.strip(): row for row in gl.rows[1:]}
    glance = {
        "8": ("ML core", "Class 1 · Learning from data: the first model", None, "No quiz (Block 1 quiz in Class 2)", "Data Analysis Project due"),
        "9": ("ML core", "Class 2 · Classification: predicting a category", None, "Block 1 quiz: Q7, Q8", "—"),
        "10": ("ML core", "Class 3 · Can I trust this model?", None, "No quiz (Block 2 quiz in Class 4)", "—"),
        "11": ("ML core", "Class 4 · Features, choosing a model and the project brief", None, "Block 2 quiz: Q9, Q10",
               f"Project brief given; milestones and due dates: {TBC}"),
        "12": ("Demo", "Short project demo", "The demo", "—", f"Marks and mark scheme: {TBC}"),
    }
    for wk, (blk, topic, chal, quiz, mile) in glance.items():
        cells = gr[wk].cells
        set_cell(cells[1], blk)
        set_cell(cells[2], topic)
        if chal:
            set_cell(cells[3], chal)
        set_cell(cells[4], quiz)
        set_cell(cells[5], mile)
    for wk in ("15", "14", "13"):
        delete_row(gl, row_index(gl, wk))

    lad = D.table_by_header(["Stage", "The student can say", "Reached by"])
    for row in lad.rows[1:]:
        if row.cells[2].text.startswith("Week 15"):
            set_cell(row.cells[2], "Week 12 — shown in the project demo")
    D.save()
    print(f"{Path(path).name}: patched")


# =====================================================================================================
# 3. Weekly Quiz Operations Guide docx
# =====================================================================================================
def patch_quizops(path):
    D = Doc(path)
    if D.patched:
        print(f"{Path(path).name}: already patched")
        return
    D.replace("The deployment contains 36 quizzes: twelve teaching weeks for each of CML3111, CML3112 and CML3113.",
              "The deployment contains 36 quiz forms: twelve quiz weeks for each of CML3111, CML3112 and CML3113. From 2 November 2026 "
              "nine weeks are sat (Weeks 1 to 5 and the four block forms Q7 to Q10); Week 6 is waived and Q11 and Q12 are retired.")
    D.replace("Quiz teaching weeks are 1–6 and 8–13; the gradebook maps them to Q1–Q12 and applies best ten of twelve.",
              "Quiz teaching weeks are 1–6 and 8–13; the gradebook maps them to Q1–Q12, counts the best 3 of Q1–Q5 and the two blocks "
              "(Q7 + Q8 and Q9 + Q10), and ignores Q6 (waived), Q11 and Q12 (retired).")
    paras = D.d.paragraphs
    heads = [i for i, p in enumerate(paras) if p.text.strip() == "Block quiz sittings from Week 8"]
    assert len(heads) == 1
    i0 = heads[0]
    sect = paras[i0 + 1:i0 + 5]
    assert sect[0].text.startswith("From Week 8 the weekly quiz is replaced"), sect[0].text[:40]
    assert sect[1].text.startswith("In the last twenty minutes of the Week 10 or Week 13 class")
    assert sect[2].text.startswith("Run applyBlockWindows() from grader/apply_block_windows_20261030.gs")
    assert sect[3].text.startswith("Gradebook: Weeks 1 to 5 keep the best 3 of 5")
    set_para(sect[0], "From Week 8 the weekly quiz is replaced by one sitting after every two classes. Block 1 uses the Q7 and Q8 forms (Weeks 8 "
             "and 9 content, Classes 1 and 2) and Block 2 uses the Q9 and Q10 forms (Weeks 10 and 11 content, Classes 3 and 4). Q11 and Q12 are "
             "retired and are never sat. Each form is worth 5 marks, so a block quiz is out of 10. The forms, answer keys and gradebook "
             "columns are unchanged.")
    set_para(sect[1], "In the last twenty minutes of Class 2 (CML3112 Tue 10 Nov; CML3113 and CML3111 Fri 13 Nov) run open_Block1_CML3112, "
             "open_Block1_CML3113 or open_Block1_CML3111. In the last twenty minutes of Class 4 (Tue 24 Nov; Fri 27 Nov) run open_Block2_CML3112, "
             "open_Block2_CML3113 or open_Block2_CML3111. All are in grader/block_quiz_sittings_20261102.gs. Each opens the two forms together; "
             "each stays open for 24 hours from activation. Show one QR code per form, or share the two links. The close_Block1_ and close_Block2_ "
             "wrappers close a block early.")
    set_para(sect[2], "Before the Class 4 sitting run replaceWeek11Questions() once (create_quiz_forms.gs), because Q10 now carries two "
             "model-comparison questions from the retired Q11 bank; it keeps every link, QR code and response sheet. Run retireQ11AndQ12Forms() once to "
             "close the Week 12 and Week 13 forms, refreshBlockQuizIntros() to update the form descriptions, and checkBlockQuizForms() to confirm "
             "all four block forms carry the current questions. Run applyBlockWindows() from grader/apply_block_windows_20261102.gs once, in the "
             "submission project, to move the A7 to A11 closing times to the block deadlines in data/assessments.json.")
    set_para(sect[3], "Gradebook: Weeks 1 to 5 keep the best 3 of 5, because Week 6 is waived for all three cohorts. The two blocks are never "
             "dropped. Quizzes are out of 35 marks (3 x 5 + 10 + 10) and assignments out of 160 marks (3 x 20 + 40 + 60); each component is worth 15% "
             "of the course. Use replaceWeek11Questions() to change the live Q10 forms, not rebuildAllForms().")
    D.save()
    print(f"{Path(path).name}: patched")


# =====================================================================================================
# 4. Master plan workbook
# =====================================================================================================
def X(ws, coord, old, new):
    v = ws[coord].value
    assert isinstance(v, str) and v.count(old) == 1, f"{ws.title}!{coord}: {old[:60]!r} count={v.count(old) if isinstance(v, str) else None}"
    ws[coord].value = v.replace(old, new)


def XSET(ws, coord, prefix, new):
    v = ws[coord].value
    assert isinstance(v, str) and v.startswith(prefix), f"{ws.title}!{coord}: starts {str(v)[:50]!r}, wanted {prefix!r}"
    ws[coord].value = new


def delete_rows_keep(ws, idx, n=1, expect_prefix=None):
    """Delete rows, moving merged ranges and row heights up. Formulas are NOT translated; callers rewrite them."""
    if expect_prefix is not None:
        assert str(ws.cell(idx, 1).value).startswith(expect_prefix), (ws.title, idx, ws.cell(idx, 1).value)
    merges = [CellRange(r.coord) for r in ws.merged_cells.ranges]
    for m in merges:  # a merged range must be wholly above, wholly below or wholly inside the deleted rows
        assert m.max_row < idx or m.min_row >= idx + n or (m.min_row >= idx and m.max_row < idx + n), \
            f"{ws.title}: merged range {m} straddles the deleted rows"
    top = ws.max_row
    heights = {r: ws.row_dimensions[r].height for r in range(1, top + 1)}
    ws.delete_rows(idx, n)
    for r in range(idx, top + 1):
        ws.row_dimensions[r].height = heights.get(r + n)
    new = MultiCellRange()
    for m in merges:
        if idx <= m.min_row < idx + n:
            continue  # merged range was inside the deleted rows
        if m.min_row >= idx + n:
            m = CellRange(min_col=m.min_col, max_col=m.max_col, min_row=m.min_row - n, max_row=m.max_row - n)
        new.add(m)
    ws.merged_cells = new


def hdr_map(ws, row=4):
    return {str(c.value).strip(): c.column_letter for c in ws[row] if c.value is not None}


def col(ws, prefix):
    hits = [letter for h, letter in hdr_map(ws).items() if h.startswith(prefix)]
    assert len(hits) == 1, (ws.title, prefix, hits)
    return hits[0]


def line_op(ws, coord, match, new):
    """Replace (new is str) or delete (new is None) the single line that starts with `match`."""
    v = ws[coord].value
    assert isinstance(v, str), (ws.title, coord)
    out, hits = [], 0
    for line in v.split("\n"):
        if line.startswith(match):
            hits += 1
            if new is not None:
                out.append(new)
        else:
            out.append(line)
    assert hits == 1, f"{ws.title}!{coord}: {hits} line(s) start with {match[:50]!r}"
    ws[coord].value = "\n".join(out)


CLASS_NOTE = ("• UPDATED 2 Nov 2026 (four-class second half): this is {cls}. The class content and clock are in "
              "second_half/Plan_Weeks_8-12.pdf and the {cls} Lecturer Guide in second_half/Lecturer Guides/; where they differ, the "
              "Lecturer Guide governs and the timings below are the earlier design.")


def block_quiz_line(block, forms, opener):
    return (f"LAST 20 MINUTES — BLOCK {block} QUIZ ({forms}). Run {opener} from block_quiz_sittings_20261102.gs, project one QR code per "
            "form, and give the room the last 20 minutes for both forms. Each form stays open for 24 hours and the two together are 10 marks; "
            "a block always counts. If the network is down, the 24-hour window covers it: say so out loud.")


WEEK_ROWS = {8: 12, 9: 13, 10: 14, 11: 15, 12: 16}
DATES = {  # content week -> (Monday, Tuesday, Friday) as in the Calendar sheet
    8: ("Mon 02 Nov 2026", "Tue 03 Nov 2026", "Fri 06 Nov 2026"),
    9: ("Mon 09 Nov 2026", "Tue 10 Nov 2026", "Fri 13 Nov 2026"),
    10: ("Mon 16 Nov 2026", "Tue 17 Nov 2026", "Fri 20 Nov 2026"),
    11: ("Mon 23 Nov 2026", "Tue 24 Nov 2026", "Fri 27 Nov 2026"),
    12: ("Mon 30 Nov 2026", "Tue 01 Dec 2026", "Fri 04 Dec 2026"),
}
CLOSE1 = "Block 1 closes: CML3112 Tue 17 Nov 11:00, CML3113 Fri 20 Nov 08:00, CML3111 Fri 20 Nov 11:00."
CLOSE2 = "Block 2 closes: CML3112 Tue 1 Dec 11:00, CML3113 Fri 4 Dec 08:00, CML3111 Fri 4 Dec 11:00."


def patch_weekly_sheet(ws, code_for_quiz):
    """Master Plan sheet or a Cohort sheet. Weeks are at rows 5..19 (Weeks 1..15)."""
    cohort_sheet = ws.title.startswith("Cohort")
    H = {k: col(ws, k) for k in ("Topic", "Learning objectives", "3-hour session structure", "Concepts introduced", "Tools introduced",
                                "Practical / lab", "Interactive challenge", "Assignment", "Weekly quiz", "Project milestone",
                                "Assessment relevance", "Lecturer preparation", "Required resources")}
    S, K, A, L, M, N, O, J, T = (H["3-hour session structure"], H["Weekly quiz"], H["Assignment"], H["Project milestone"],
                                 H["Assessment relevance"], H["Lecturer preparation"], H["Required resources"], H["Interactive challenge"],
                                 H["Topic"])
    assert str(ws[f"A{WEEK_ROWS[12]}"].value) == "12" and str(ws[f"A{WEEK_ROWS[12] + 3}"].value) == "15"
    # --- Weeks 1 to 7: the numbers that changed (best 3 of 5, 15%, Week 6 waived)
    for wk in range(1, 8):
        r = 4 + wk
        assert str(ws[f"A{r}"].value) == str(wk)
        v = ws[f"{S}{r}"].value
        if "LAST FIVE MINUTES" in v:
            if wk == 6:
                line_op(ws, f"{S}{r}", "• LAST FIVE MINUTES — QUIZ 6",
                        "• QUIZ 6 is WAIVED for all three cohorts: do not run it (see Practical_Revision_Week6_Waiver.md).")
            else:
                assert v.count("Worth 1%, best 10 of 12 count, no resits.") == 1, (ws.title, wk)
                ws[f"{S}{r}"].value = v.replace("Worth 1%, best 10 of 12 count, no resits.",
                                                "Worth 1 of the 35 quiz marks (quizzes are 15% of the course); the best 3 of the five weekly quizzes count, Week 6 is waived, no resits.")
        m = ws[f"{M}{r}"].value
        if wk == 2:
            XSET(ws, f"{M}{r}", "A2 is one of eleven challenges", "A2 is one of the five weekly assignments in Weeks 1 to 5, of which the best three count "
                 "(Week 6 is waived), and the assignments are 15% of the course. The Week 2 quiz is one of the five weekly quizzes, of which the best three "
                 "count, and the quizzes are 15% of the course.")
        elif wk == 6:
            X(ws, f"{M}{r}", "A6 contributes to Practical Challenges & Assignments (10%).", "A6 is waived for all three cohorts and does not count towards the assignments (15%).")
        elif "Practical Challenges & Assignments (10%)" in m:
            ws[f"{M}{r}"].value = m.replace("Practical Challenges & Assignments (10%)", "Practical Challenges & Assignments (15%; best 3 of the five weekly assignments count)")
    # --- Weeks 8 to 11 (Classes 1 to 4)
    cls = {8: "Class 1", 9: "Class 2", 10: "Class 3", 11: "Class 4"}
    for wk in (8, 9, 10, 11):
        r = WEEK_ROWS[wk]
        ws[f"B{r}"].value = "Block 3 - The Machine Learning Core"
        topic = "Features, choosing a model and the project brief" if wk == 11 else ws[f"{T}{r}"].value
        ws[f"{T}{r}"].value = f"{cls[wk]} · {topic}"
        ws[f"{S}{r}"].value = CLASS_NOTE.format(cls=cls[wk]) + "\n" + ws[f"{S}{r}"].value
    r = WEEK_ROWS[8]
    line_op(ws, f"{S}{r}", "• LAST FIVE MINUTES — QUIZ 7", None)
    line_op(ws, f"{S}{r}", "• 2:45-3:00  Data Analysis Project submitted.",
            "• 2:45-3:00  Data Analysis Project submitted. No quiz today: the Block 1 quiz (Q7 and Q8) is sat in the last 20 minutes of Class 2.")
    X(ws, f"{K}{r}", "QUIZ 7 - the first model", "Q7 - the first model (Block 1: sat with Q8 in the last 20 minutes of Class 2)")
    XSET(ws, f"{L}{r}", "DATA ANALYSIS PROJECT DUE (10%).", f"DATA ANALYSIS PROJECT DUE (10%). The Engineering ML Project brief comes in Class 4; dates, milestones and mark scheme are {TBC}.")
    XSET(ws, f"{M}{r}", "A7 contributes to", "A7 is part A of Block 1 (A7 + A8 = 40 marks; the assignments are 15% of the course). Data Analysis Project is submitted and marked (10%). "
         "Regression, metrics and train/test are examined in the Block 1 quiz (Q7) and the Block 1 assignment.")
    line_op(ws, f"{N}{r}", "• Draft the Engineering ML Project brief and rubric", f"• Engineering ML Project brief: given in Class 4. Dates, milestones and mark scheme: {TBC}.")
    ws[f"{A}{r}"].value = ws[f"{A}{r}"].value + " Block 1, part A of 2 (A7 + A8 = 40 marks). " + CLOSE1
    r = WEEK_ROWS[9]
    line_op(ws, f"{S}{r}", "• LAST FIVE MINUTES — QUIZ 8", None)
    line_op(ws, f"{S}{r}", "• 2:40-3:00  ENGINEERING ML PROJECT brief and rubric released.",
            "• 2:40-3:00  " + block_quiz_line(1, "Q7 and Q8", f"open_Block1_{code_for_quiz}"))
    X(ws, f"{K}{r}", "QUIZ 8 - classification", "Q8 - classification (Block 1: sat with Q7 in the last 20 minutes of Class 2)")
    XSET(ws, f"{L}{r}", "ENGINEERING ML PROJECT launched", f"No project milestone this week. The Engineering ML Project (30%) is introduced in Class 4; dates, milestones and mark scheme are {TBC}.")
    XSET(ws, f"{M}{r}", "A8 contributes to", "A8 is part B of Block 1 (A7 + A8 = 40 marks; the assignments are 15% of the course). The Block 1 quiz (Q7 + Q8 = 10 marks) is sat today. "
         "Classification and metric choice are examined in Q8 and the Block 1 assignment.")
    line_op(ws, f"{N}{r}", "• Finalise and publish the Engineering ML Project brief, rubric and milestone schedule.",
            "• Before the Block 1 sitting run checkBlockQuizForms() and open one Q7 and one Q8 form yourself.")
    line_op(ws, f"{O}{r}", "• Engineering ML Project brief and rubric (printed and posted).", "• Block 1 quiz QR codes (Q7 and Q8) for your cohort.")
    ws[f"{A}{r}"].value = ws[f"{A}{r}"].value + " Block 1, part B of 2. " + CLOSE1
    r = WEEK_ROWS[10]
    line_op(ws, f"{S}{r}", "• LAST FIVE MINUTES — QUIZ 9", None)
    line_op(ws, f"{S}{r}", "• 2:40-3:00  Project Milestone 1 review, in team slots.",
            "• 2:40-3:00  Close. A9 (Block 2, part A) is issued. No quiz today: the Block 2 quiz (Q9 and Q10) is sat in the last 20 minutes of Class 4.")
    X(ws, f"{K}{r}", "QUIZ 9 - can I trust this model?", "Q9 - can I trust this model? (Block 2: sat with Q10 in the last 20 minutes of Class 4)")
    X(ws, f"{K}{r}", "The highest-value quiz of the twelve, and worth protecting the five minutes for.", "The highest-value quiz of the nine that are sat.")
    XSET(ws, f"{L}{r}", "PROJECT MILESTONE 1", f"No graded project milestone in the plan. Project milestones, dates and mark scheme are {TBC}.")
    XSET(ws, f"{M}{r}", "A9 contributes to", "A9 is part A of Block 2 (A9 + A10 + A11 = 60 marks; the assignments are 15% of the course). Validation carries 15 of the 100 marks in the "
         "project rubric. Validation and leakage are examined in Q9 and the Block 2 assignment.")
    line_op(ws, f"{N}{r}", "• Prepare the PM1 review slot booking sheet.", None)
    line_op(ws, f"{N}{r}", "• Draft the Practical Test 2 specification now", None)
    line_op(ws, f"{O}{r}", "• Printed PM1 checklist and contribution log template.", None)
    line_op(ws, f"{O}{r}", "• Timer for the PM1 stand-ups.", None)
    ws[f"{A}{r}"].value = ws[f"{A}{r}"].value + " Block 2, part A of 3 (A9 + A10 + A11 = 60 marks). " + CLOSE2
    r = WEEK_ROWS[11]
    line_op(ws, f"{S}{r}", "• LAST FIVE MINUTES — QUIZ 10", None)
    line_op(ws, f"{S}{r}", "• 2:40-3:00  Project Milestone 2 briefing.",
            "• 2:40-3:00  " + block_quiz_line(2, "Q9 and Q10", f"open_Block2_{code_for_quiz}") + f" The project brief is given earlier in the class; dates, milestones and mark scheme are {TBC}.")
    XSET(ws, f"{K}{r}", "QUIZ 10 - features",
         "Q10 - features and choosing a model (Block 2: sat with Q9 in the last 20 minutes of Class 4)\nA feature that uses the answer, an ablation read for the size of the "
         "improvement, a fair-comparison protocol, which candidate meets both limits, and what stops select_model failing on an empty table. Two of the five questions "
         "come from the retired Q11 bank.")
    XSET(ws, f"{L}{r}", "PROJECT MILESTONE 2", f"ENGINEERING ML PROJECT brief given in this class (30%). Short demo in Week 12; milestones, due date and mark scheme are {TBC}.")
    XSET(ws, f"{M}{r}", "A10 contributes to", "A10 and A11 are parts B and C of Block 2 (A9 + A10 + A11 = 60 marks; the assignments are 15% of the course). Engineering reasoning carries 20 of the "
         "100 project marks. Features and model choice are examined in Q10 and the Block 2 assignment. The Block 2 quiz (Q9 + Q10 = 10 marks) is sat today.")
    line_op(ws, f"{N}{r}", "• Publish the Practical Test 2 specification and rubric this week.", f"• Week 12 project demo arrangements (format, order, marks, mark scheme): {TBC}.")
    line_op(ws, f"{O}{r}", "• Practical Test 2 specification and rubric for distribution.", "• Block 2 quiz QR codes (Q9 and Q10) for your cohort.")
    ws[f"{A}{r}"].value = ws[f"{A}{r}"].value + (" Block 2, part B of 3. A11 / W12 (model recommendation, part C) is issued in the same class: submit the issued cohort notebook "
                                                "with selection/error checks and written reasoning about the supplied constraints. ") + CLOSE2
    # --- Week 12 becomes the short project demo
    r = WEEK_ROWS[12]
    ws[f"B{r}"].value = "Block 4 - Short Project Demo"
    new = {
        T: "Short project demo (proposal, not final)",
        H["Learning objectives"]: "• Present a team result in about five minutes and answer questions from the class.\n• Show the steps of Classes 1 to 4 on the cohort data: clean, split, "
                                 f"baseline, two or more models, a fair comparison, the sealed test group opened once.\n• Hand in a one-page decision memo.\nObjectives, marks and mark scheme: {TBC}.",
        S: f"• Running order, room and time per team: {TBC}.\n• Each team presents for about five minutes, with questions from the class (Plan_Weeks_8-12.pdf).\n"
           "• Block 2 assignment (A9, A10, A11) closes on this day: CML3112 Tue 1 Dec 11:00; CML3113 Fri 4 Dec 08:00; CML3111 Fri 4 Dec 11:00.",
        H["Concepts introduced"]: "• No new concepts. Classes 1 to 4 (Weeks 8 to 11 content).",
        H["Tools introduced"]: "• None new.",
        H["Practical / lab"]: TBC_CAP + ".",
        J: f"The demo itself. Format: {TBC}.",
        A: "Block 2 assignment (A9, A10, A11) closes today; see the closing times in the session structure.",
        K: "—",
        L: f"Short project demo. Marks, mark scheme and due date: {TBC}.",
        M: f"Engineering ML Project (30%) and demonstration (15%). Mark scheme: {TBC}.",
        N: f"• Demo arrangements: {TBC}.",
        O: "• " + TBC_CAP + ".",
    }
    for letter, text in new.items():
        ws[f"{letter}{r}"].value = text
    if cohort_sheet:
        ws[f"{col(ws, 'Dataset')}{r}"].value = "The cohort data used in Classes 1 to 4."
        ws[f"{col(ws, 'Shared vs cohort')}{r}"].value = TBC_CAP + "."
        code = ws["F5"].value
        for wk in (8, 9, 10, 11, 12):
            rr = WEEK_ROWS[wk]
            mon, tue, fri = DATES[wk]
            ws[f"C{rr}"].value = mon
            first, _, rest = ws[f"D{rr}"].value.partition("\n")
            assert re.match(r"^(Tue|Fri) \d\d \w{3} 2026$", first), first
            ws[f"D{rr}"].value = (tue if code == "CML3112" else fri) + "\n" + rest
    # --- retire Weeks 13 to 15
    delete_rows_keep(ws, WEEK_ROWS[12] + 1, 3, expect_prefix="13")
    for rr in range(WEEK_ROWS[12] + 1, WEEK_ROWS[12] + 4):
        assert all(c.value is None for c in ws[rr]), (ws.title, rr)
    if cohort_sheet:
        assert "45 contact hours" in ws["A2"].value
        ws["A2"].value = ws["A2"].value.replace("45 contact hours", "36 contact hours")


def patch_workbook(path):
    wb = openpyxl.load_workbook(path)
    if MARK in (wb.properties.keywords or ""):
        print(f"{Path(path).name}: already patched")
        return
    # ---------------- Read Me
    ws = wb["Read Me"]
    X(ws, "A2", "7 September – 18 December 2026 · 15 study weeks", "7 September – 4 December 2026 · 12 study weeks")
    X(ws, "B26", "the Week 7 and Week 14 practical tests", "the Week 7 practical test")
    X(ws, "B30", "the alternative 40/60 mapping on that same sheet satisfies it without changing any teaching. Confirm which model applies before Week 5, because Test 1 falls in Week 7.",
      f"the alternative mapping on that same sheet records a 55/45 split under the new weights without changing any teaching. A different mandated split (for example 40/60) is {TBC}"
      " against IUEA regulations. Confirm which model applies with the Faculty.")
    XSET(ws, "B33", "All 15 weeks", "All 12 weeks with real dates for both the Tuesday and the Friday slots (Weeks 8 to 11 are the four classes of the second half, Week 12 is the short project demo), "
         "teaching, assessment and demo weeks marked, and the public holiday flagged.")
    X(ws, "B37", "and the alternative 40/60 continuous-assessment model.", "and the alternative continuous-assessment / final split.")
    XSET(ws, "B39", "The before-and-after arithmetic", f"The before-and-after arithmetic: about 195 illustrative hours fully human before the Week 12 demo (its marking time is {TBC}); the stack's hours are pilot pending.")
    X(ws, "B40", "All six rubrics", "All five rubrics")
    # ---------------- Calendar
    ws = wb["Calendar"]
    XSET(ws, "A2", "15 study weeks", "12 study weeks from Monday 7 September 2026. Each cohort meets once per week for 3 hours. From Week 8 the week number names the content: Weeks 8 to 11 are Classes 1 to 4, "
         "so their dates run from Monday 2 November. Week 12 is the short project demo.")
    cal_new = {
        12: ("Block 3 - The Machine Learning Core", 8, "Teaching", "Class 1 (Week 8 content). The Friday cohorts were taught the Week 8 concepts without the lab on Fri 30 Oct; for them Class 1 is a recap and the lab. CML3112 starts Week 8 on Tue 3 Nov."),
        13: ("Block 3 - The Machine Learning Core", 9, "Teaching", "Class 2 (Week 9 content). Block 1 quiz (Q7, Q8) in the last 20 minutes."),
        14: ("Block 3 - The Machine Learning Core", 10, "Teaching", "Class 3 (Week 10 content). Block 1 assignment (A7, A8) closes: CML3112 Tue 17 Nov 11:00; CML3113 Fri 20 Nov 08:00; CML3111 Fri 20 Nov 11:00."),
        15: ("Block 3 - The Machine Learning Core", 11, "Teaching", "Class 4 (Week 11 content). Block 2 quiz (Q9, Q10) in the last 20 minutes. Project brief."),
        16: ("Block 4 - Short Project Demo", 12, "Demo", "Week 12: short project demo (proposal, not final). Block 2 assignment (A9, A10, A11) closes: CML3112 Tue 1 Dec 11:00; CML3113 Fri 4 Dec 08:00; CML3111 Fri 4 Dec 11:00. Marks and arrangements: " + TBC + "."),
    }
    assert str(ws["A19"].value) == "15" and ws["G19"].value == "Teaching / Demo"
    for c in "ABCDEFGH":  # the demo row takes the green 'demo day' style of the old Week 15 row
        ws[f"{c}16"]._style = copy.copy(ws[f"{c}19"]._style)
    for r_, (blk, wk, typ, note) in cal_new.items():
        mon, tue, fri = DATES[wk]
        for c, v in zip("ABCDEFGH", (wk, blk, mon, tue, fri, fri, typ, note)):
            ws[f"{c}{r_}"].value = v
    delete_rows_keep(ws, 17, 3, expect_prefix="13")
    XSET(ws, "A18", "Teaching weeks: 13.", "Teaching weeks: 10 (Weeks 1 to 6 and Weeks 8 to 11 content).  Assessment week: 1 (Week 7).  Demo week: 1 (Week 12).  Contact hours per cohort: 36 "
         "(12 sessions of 3 hours; Week 6 is waived for the quiz and assignment).  Total lecturer contact: 9 hours per week — 3 on Tuesday and SIX BACK-TO-BACK ON FRIDAY, 08:00 to 14:00 with a room change "
         "and no gap. See Risk R16.")
    X(ws, "A19", "green = demo day", "green = project demo day")
    # ---------------- weekly sheets
    patch_weekly_sheet(wb["Master Plan (Shared Core)"], "CML31xx")
    for name, code in (("Cohort A", "CML3112"), ("Cohort B", "CML3113"), ("Cohort C", "CML3111")):
        assert wb[name]["F5"].value == code, (name, wb[name]["F5"].value)
        patch_weekly_sheet(wb[name], code)
    # ---------------- Shared vs Divergent
    ws = wb["Shared vs Divergent"]
    X(ws, "C14", " PM1 review.", "")
    ws["B16"].value = "Short project demo (Week 12; proposal, not final)"
    ws["C16"].value = f"Demo format, running order and mark scheme: {TBC}."
    ws["D16"].value = f"The cohort data and the project titles that emerge: {TBC}."
    ws["E16"].value = f"Low — {TBC}"
    ws["F16"].value = ("[A] DIVERGENT: cohort data and project titles. SHARED: demo format.\n[B] DIVERGENT: cohort data and project titles. SHARED: demo format.\n"
                       "[C] DIVERGENT: cohort data and project titles. SHARED: demo format.")
    delete_rows_keep(ws, 17, 3, expect_prefix="13")
    XSET(ws, "A18", "Reading of this sheet", "Reading of this sheet: Weeks 4–7 carry almost all of the triplicated preparation, because that is where the datasets must be authored. Week 2 requires no divergent "
         "preparation at all. Nine unseen test dataset variants are needed in total, for Practical Test 1 (three matched variants per cohort); build them during Weeks 2–5. Practical Test 2 was dropped on "
         "2 November 2026, so there is no second set.")
    # ---------------- Assessment
    ws = wb["Assessment"]
    XSET(ws, "A2", "Entirely practical", "Entirely practical, continuous and project-based. No traditional written examination. 60% of the mark is individual on the component modes below (the demonstration mode is "
         f"{TBC}); automatic grading coverage is validated assessment by assessment.")
    ws["A6"].value = "QUIZZES (weekly in Weeks 1-5, then two block sittings)"
    ws["B6"].value = "W1-W5 weekly (Week 6 waived); Block 1 (Q7, Q8) in the last 20 minutes of Class 2; Block 2 (Q9, Q10) in the last 20 minutes of Class 4"
    ws["D6"].value = 0.15
    ws["E6"].value = ("Five diagnostic questions per form, one mark each. Weeks 1-5: a five-minute QR-code quiz in the last five minutes, best 3 of 5 count. Blocks: two forms sat together, each open for 24 hours, always counted. "
                      "Total 35 marks (3 x 5 + 10 + 10), worth 15%. Instant score and teaching feedback. No resits. A network failure is covered by the 24-hour window.")
    ws["A7"].value = "Practical challenges & assignments (weekly in Weeks 1-5, then two block packs)"
    ws["B7"].value = "Weeks 1-5 weekly (Week 6 waived); Block 1 (A7, A8); Block 2 (A9, A10, A11)"
    ws["D7"].value = 0.15
    X(ws, "E7", "the lecturer batch-grades against hidden tests.", "the lecturer batch-grades against hidden tests. The best 3 of the five weekly assignments count; Block 1 (40 marks) and Block 2 (60 marks) always count; total 160 marks, worth 15%.")
    assert ws["D9"].value == 0.15 and ws["A10"].value.startswith("PRACTICAL TEST 2"), (ws["D9"].value, ws["A10"].value)
    delete_rows_keep(ws, 10, 1, expect_prefix="PRACTICAL TEST 2")      # Model 1 rows now: 10 project, 11 demo, 12 total, 13 individual, 14 team, 15 coverage
    assert ws["A10"].value == "Engineering ML Project" and ws["A11"].value.startswith("Demo, viva")
    ws["B10"].value = f"Brief in Class 4 (Week 11 content); short demo in Week 12; milestones and due date {TBC}"
    ws["D10"].value = 0.3
    ws["E10"].value = f"Proposal, not final: repository, one-page decision memo, AI-use declaration, contribution log. Deliverables, milestones and mark scheme: {TBC}."
    X(ws, "C10", "individual accountability via viva + log", f"individual accountability via log; any individual defence is {TBC}")
    ws["A11"].value = "Week 12 short project demonstration"
    ws["B11"].value = "Week 12 (Tue 1 Dec / Fri 4 Dec)"
    ws["C11"].value = f"Individual ({TBC})"
    ws["D11"].value = 0.15
    ws["E11"].value = f"About five minutes per team, with questions from the class. Mark scheme: {TBC}."
    ws["F11"].value = f"Week 12 demo rubric: {TBC} (see Rubrics sheet)"
    assert ws["A12"].value == "TOTAL" and ws["A13"].value == "Of which individual" and ws["A14"].value == "Of which team"
    ws["D12"].value = "=SUM(D6:D11)"
    ws["D13"].value = "=D6+D7+D9+D11"
    ws["D14"].value = "=D8+D10"
    XSET(ws, "F13", "Weekly quizzes", f"Quizzes, assignments, Practical Test 1 and the demonstration (its mode is {TBC}) are individually assessed.")
    # Model 2
    assert ws["A18"].value.startswith("MODEL 2")
    ws["A20"].value = "CONTINUOUS ASSESSMENT (55%)"
    ws["A21"].value = "Quizzes (weekly W1-W5, then one sitting per block)"
    ws["B21"].value = "W1-W5 weekly; Class 2 (Block 1) and Class 4 (Block 2)"
    ws["D21"].value = 0.15
    ws["E21"].value = "Best 3 of 5 weekly (Week 6 waived) plus both blocks; 35 marks"
    ws["A22"].value = "Practical challenges (weekly W1-W5, then two block packs)"
    ws["B22"].value = "Weeks 1-5; Block 1 (A7, A8); Block 2 (A9, A10, A11)"
    ws["D22"].value = 0.15
    ws["E22"].value = "Best 3 of 5 weekly (Week 6 waived) plus both blocks; 160 marks"
    assert ws["A23"].value == "Data Analysis Project" and ws["A24"].value == "Practical Test 1"
    ws["D24"].value = 0.15
    ws["E24"].value = "As in Model 1"
    assert ws["A25"].value.startswith("FINAL ASSESSMENT") and ws["A26"].value == "Practical Test 2"
    delete_rows_keep(ws, 26, 1, expect_prefix="Practical Test 2")
    ws["A25"].value = "FINAL ASSESSMENT (45%)"
    assert ws["A26"].value == "Engineering ML Project" and ws["A27"].value.startswith("Demo, viva")
    ws["B26"].value = "Week 12"
    ws["D26"].value = 0.3
    ws["E26"].value = "As in Model 1"
    ws["A27"].value = "Week 12 demonstration"
    ws["B27"].value = "Week 12"
    ws["D27"].value = 0.15
    assert ws["A28"].value == "TOTAL"
    ws["D28"].value = "=D21+D22+D23+D24+D26+D27"
    # design notes
    assert ws["A31"].value == "DESIGN NOTES" and ws["A32"].value == "Why two tests, not one"
    ws["A32"].value = "Why one practical test"
    ws["B32"].value = ("Practical Test 2 was dropped on 2 November 2026 because the semester now ends at Week 12. Week 7 still certifies data literacy (can you investigate a dataset?). End-to-end "
                       f"capability is now shown in the Block 2 assignment, the quizzes and the Week 12 project demo, whose mark scheme is {TBC}.")
    assert ws["A33"].value == "Why the tests are unaided"
    ws["A33"].value = "Why the test is unaided"
    X(ws, "B33", "it is excluded from the two tests, which certify unaided capability.", "it is excluded from Practical Test 1, which certifies unaided capability.")
    assert ws["A34"].value == "Why 65% individual"
    ws["A34"].value = "Why 60% individual"
    XSET(ws, "B34", "With teams of 4–5", "With teams of 4–5 and up to 22 teams in Cohort A, a team-heavy mark scheme would let a weak student pass on a strong teammate's work. Individual quizzes, an individual test and "
         f"individually marked assignments provide individual evidence alongside shared project marks; any individual defence at the Week 12 demo is {TBC}.")
    X(ws, "B35", "Twelve auto-graded weekly quizzes plus eleven auto-graded weekly submissions mean 20% of the mark comes from these recurring components.",
      "Nine auto-graded quizzes plus ten graded assignment parts (five weekly, then five block parts) mean 30% of the mark comes from these recurring components.")
    X(ws, "B35", "From Week 8 the quizzes and assignments are set after every three classes (Block 1 = W8-W10, Block 2 = W11-W13) instead of weekly; see Block_Assessment_Arrangement_2026-10-30.md.",
      "From Week 8 the quizzes and assignments are set in two blocks of two classes (Block 1 = Classes 1 and 2, Block 2 = Classes 3 and 4) instead of weekly; see Block_Assessment_Arrangement_2026-11-02.md.")
    X(ws, "B36", "Across all six rubrics", "Across all five rubrics")
    X(ws, "B36", "The Week 15 recognition categories reinforce this: there is no prize for highest accuracy.",
      f"If recognition is given at the Week 12 demo ({TBC}), there is no prize for highest accuracy.")
    # ---------------- Rubrics
    ws = wb["Rubrics"]
    assert ws["A27"].value.startswith("Practical Test 2 - End-to-End")
    delete_rows_keep(ws, 27, 13, expect_prefix="Practical Test 2")        # heading, header, 9 criteria, total, blank
    ws["A4"].value = "Engineering ML Project (30%) - as specified by the lecturer"
    assert ws["A27"].value == "Data Analysis Project (10%)"
    assert ws["A36"].value.startswith("Weekly quizzes (10%)")
    ws["A36"].value = "Quizzes (15%) - how the five questions in each form are marked"
    assert ws["A44"].value.startswith("Demo, viva & individual reflection (10%)")
    ws["A44"].value = f"Week 12 short project demo (15%) - mark scheme {TBC}"
    for rr in range(46, 50):
        ws[f"C{rr}"].value = f"Carried over from the earlier Week 15 rubric for reference; {TBC} for the Week 12 demo. " + ws[f"C{rr}"].value
        ws[f"D{rr}"].value = TBC_CAP
    for formula_row, (a, b) in {13: (6, 12), 25: (17, 24), 34: (29, 33), 42: (38, 41), 50: (46, 49)}.items():
        assert ws[f"A{formula_row}"].value == "TOTAL", (formula_row, ws[f"A{formula_row}"].value)
        ws[f"B{formula_row}"].value = f"=SUM(B{a}:B{b})"
    assert ws["A52"].value.startswith("Apply the published execution")
    # ---------------- Tools Rollout
    ws = wb["Tools Rollout"]
    X(ws, "E7", "not accidentally in Week 14.", "not accidentally later in the semester.")
    assert ws["A23"].value.startswith("XGBoost")
    ws["B23"].value = 11
    ws["D23"].value = "Named in Class 4 only"
    assert ws["A24"].value == "scikit-learn (search)"
    ws["B24"].value = TBC
    assert ws["A25"].value == "Streamlit"
    delete_rows_keep(ws, 25, 1, expect_prefix="Streamlit")
    assert ws["A25"].value.startswith("requirements.txt")
    ws["B25"].value = f"12 ({TBC})"
    # ---------------- Dataset Register
    ws = wb["Dataset Register"]
    assert ws["A23"].value == "COURSE-AUTHORED: Test 2 variants x3"
    delete_rows_keep(ws, 23, 1, expect_prefix="COURSE-AUTHORED: Test 2")
    # ---------------- Marking Load
    ws = wb["Marking Load"]
    assert ws["A5"].value == "Weekly practical challenges" and ws["A8"].value == "Practical Test 2"
    ws["B5"].value = "10 x ~195"
    ws["D5"].value = 98
    ws["B6"].value = "9 x ~195"
    delete_rows_keep(ws, 8, 1, expect_prefix="Practical Test 2")
    assert ws["A10"].value == "Demo and reflection"
    ws["A10"].value = "Week 12 short project demo"
    ws["B10"].value = "43 teams"
    ws["C10"].value = TBC
    ws["D10"].value = TBC
    ws["F10"].value = f"Marking arrangement: {TBC}."
    assert ws["A12"].value.startswith("TOTAL")
    ws["D12"].value = "=SUM(D5:D11)"
    ws["E12"].value = '=IF(COUNT(E5:E11)=ROWS(E5:E11),SUM(E5:E11),"Pilot pending")'
    ws["E13"].value = '=IF(ISNUMBER(E12),D12-E12,"Pilot pending")'
    # ---------------- Risk Register
    ws = wb["Risk Register"]
    X(ws, "B9", "the Week 7 and Week 14 practical tests unrunnable", "the Week 7 practical test unrunnable")
    X(ws, "E11", "The practical tests run in Colab and the submission form, so they need connectivity too. Agree a documented interruption, collection and rescheduling procedure with the Faculty before the tests.",
      "The practical test runs in Colab and the submission form, so it needs connectivity too. Agree a documented interruption, collection and rescheduling procedure with the Faculty before the test.")
    X(ws, "E13", "Week 15 uses submitted individual typed defence answers and reflection; live questioning is formative.",
      f"Any individual defence at the Week 12 demo is {TBC}; live questioning is formative.")
    X(ws, "E16", "Best 10 of 12 provides some flexibility", "Best 3 of the five weekly quizzes and the 24-hour block window provide some flexibility")
    X(ws, "E17", "The two invigilated practical tests assess unaided work.", "Practical Test 1 assesses unaided work.")
    X(ws, "E19", "Both practical tests prohibit AI. Test 1 is a take-home test with an understanding check and Test 2 follows the invigilator's rules.",
      "Practical Test 1 prohibits AI; it is a take-home test with an understanding check.")
    ws["B21"].value = "The four remaining classes slip, and the project demo is squeezed."
    ws["E21"].value = f"If a class runs over, its Lecturer Guide says what to cut and the lab is never cut (Plan_Weeks_8-12.pdf). The Week 12 demo format and milestones are {TBC}."
    X(ws, "E22", "The Week 15 reflection requires two named Semester 2 goals.", f"An end-of-semester reflection naming two Semester 2 goals is {TBC}.")
    wb.properties.keywords = ((wb.properties.keywords or "") + " " + MARK).strip()
    if not DRY:
        backup(path)
        wb.save(path)
    print(f"{Path(path).name}: patched")


def main():
    B = BASE
    for f in ("IUEA_ML_Syllabus_CohortA_Design_and_Infrastructure.docx", "IUEA_ML_Syllabus_CohortB_Mining_and_Petroleum.docx",
              "IUEA_ML_Syllabus_CohortC_Engineering.docx"):
        patch_syllabus(B / f)
    patch_master_docx(B / "IUEA_ML_Semester1_Master_Teaching_Plan.docx")
    patch_quizops(B / "IUEA_ML_Weekly_Quiz_Operations_Guide.docx")
    patch_workbook(B / "IUEA_ML_Semester1_Master_Teaching_Plan.xlsx")
    if DRY:
        print("dry run: nothing saved")


if __name__ == "__main__":
    main()
