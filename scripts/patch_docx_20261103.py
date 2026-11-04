"""Patch the three syllabi, the master teaching plan (docx and xlsx) and the Weekly Quiz Operations Guide for the decision of
3 November 2026 (data/assessment_blocks_20261103.json):

  * there is NO demo; Week 12 is a project clinic (supervised work and questions);
  * the Engineering ML project is submitted (take-home, graded like Practical Test 1, Weeks 1 to 11 only), Part A coded notebook /30
    (auto-graded plus rubric) and Part B one-page decision memo /15 (rubric), weight 45;
  * weights: quizzes 15, assignments 15, data analysis project 10, Practical Test 1 15, Engineering ML project 45 = 100;
  * released after Class 4, due Friday 11 December 2026 23:59 Kampala for all cohorts, always written 'proposed, lecturer to confirm';
  * Semester 1 results can be published before the project is marked (provisional out of 55, project PENDING).

Safety rules (as in patch_block_docx_20261102.py): every original is copied once into a sibling _backup_2026-11-03 folder before it is saved;
every string replacement asserts its match count and nothing is saved if one is wrong; a file that carries the marker is left alone;
dates come from the policy file by the course code read from each document, never by file name.
Usage: python3 scripts/patch_docx_20261103.py            (all files)
       python3 scripts/patch_docx_20261103.py --dry-run  (run every assertion, save nothing)
"""
import json
import re
import sys
from datetime import datetime
from pathlib import Path

import docx
import openpyxl
from openpyxl.worksheet.cell_range import CellRange, MultiCellRange

sys.path.insert(0, str(Path(__file__).resolve().parent))
from backup_20261103 import backup  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "IUEA_Teaching_Plan"
POL = json.loads((ROOT / "data" / "assessment_blocks_20261103.json").read_text())
MARK = "BLOCK_DOCX_20261103"
TBC = "to be confirmed by the lecturer"
TBC_CAP = TBC[0].upper() + TBC[1:]
PROPOSED = "proposed, lecturer to confirm"
DRY = "--dry-run" in sys.argv
assert POL["weights_percent"] == dict(quizzes=15, assignments=15, data_analysis_project=10, practical_test_1=15, engineering_ml_project=45)
assert POL["engineering_ml_project"]["due"]["all_cohorts"] == "2026-12-11T23:59:00+03:00"
COURSE = ("CML3112", "CML3113", "CML3111")
CLINIC = {c: datetime.fromisoformat(POL["calendar"]["week_12_project_clinic"]["dates"][c]) for c in COURSE}
DUE = f"Friday 11 December 2026, 23:59 Kampala ({PROPOSED})"
DUE_SHORT = f"Fri 11 Dec 2026 23:59 ({PROPOSED})"
PARTS = "Part A, the coded project notebook (30 marks, auto-graded plus a rubric, like Practical Test 1), and Part B, a one-page decision memo (15 marks, rubric)"


def long_day(code):
    d = CLINIC[code]
    return f"{d.strftime('%A')} {d.day} {d.strftime('%B')}"


# =====================================================================================================
# docx helpers (same behaviour as patch_block_docx_20261102.py, own marker and backup folder)
# =====================================================================================================
def _runs_text(p):
    return "".join(r.text for r in p.runs)


def para_replace(p, old, new):
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
        seen = set()
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

    def table_by_header(self, first_cells):
        hits = [t for t in self.d.tables if [c.text.strip() for c in t.rows[0].cells][:len(first_cells)] == first_cells]
        assert len(hits) == 1, f"{self.path.name}: {len(hits)} tables with header {first_cells}"
        return hits[0]

    def find_row(self, first_cell, second_cell_prefix=None):
        """The one table row whose first cell is `first_cell` (and second cell starts with `second_cell_prefix`)."""
        hits = []
        for t in self.d.tables:
            for r in t.rows:
                cells = r.cells
                if cells[0].text.strip() == first_cell and (second_cell_prefix is None or cells[1].text.strip().startswith(second_cell_prefix)):
                    hits.append((t, r))
        assert len(hits) == 1, f"{self.path.name}: {len(hits)} rows start with {first_cell!r}/{second_cell_prefix!r}"
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
    code = None
    for t in D.d.tables:
        for r in t.rows:
            if r.cells[0].text.strip() == "Course code":
                code = r.cells[1].text.strip()
    assert code in COURSE, code
    day = long_day(code)
    D.replace("(Week 12 demo day)", "(Week 12 project clinic)")
    D.replace("Project; Week 12 demonstration", "Project, Part A and Part B")
    D.replace("AI-use declaration; questions at the Week 12 demo", "AI-use declaration in the project")
    D.replace(f"Week 12 is the short project demo ({day} for your cohort), which is where the semester ends.",
              f"Week 12 is a project clinic ({day} for your cohort), with supervised work and questions and no demo, which is where the semester ends. "
              f"The Engineering ML project is released after Class 4 and is due {DUE}.")
    # calendar row 12
    t, r = D.find_row("12", "Tue 1 / Fri 4 Dec")
    cells = r.cells
    assert cells[2].text.strip().startswith("Short project demo") and cells[3].text.strip() == "The demo", [c.text for c in cells]
    closes = re.search(r"Block 2 pack \(A9, A10, A11\) closes [^.]*$", cells[5].text.strip())
    assert closes, cells[5].text
    set_cell(cells[2], "Project clinic (supervised work and questions; no demo)")
    set_cell(cells[3], "The clinic")
    set_cell(cells[5], f"Supervised work on the Engineering ML project, and questions. {closes.group(0)}. The project is due {DUE_SHORT}.")
    D.replace("is earned before the project demo rather than landing in one or two large events.",
              "is earned, and can be published, before the project is marked rather than landing in one or two large events.")
    # weights table
    t = D.table_by_header(["Component", "When", "Mode", "Weight", "What you submit"])
    i = row_index(t, "Engineering ML Project")
    c = t.rows[i].cells
    assert c[3].text.strip() == "30%", c[3].text
    set_cell(c[1], f"Brief in Class 4 (Week 11 content); released after Class 4; due {DUE_SHORT}")
    set_cell(c[2], f"Take-home submission; individual or team: {TBC}")
    set_cell(c[3], "45%")
    set_cell(c[4], f"{PARTS[0].upper()}{PARTS[1:]}. It covers only what was taught in Weeks 1 to 11. Rubrics and the split of Part A between automatic checks and rubric marks are {TBC}. "
                   "Your Semester 1 result can be published before it is marked: it is shown as provisional, out of 55 marks, with the project PENDING.")
    j = row_index(t, "Week 12 short project demonstration")
    delete_row(t, j, "Week 12 short project demonstration")
    D.replace(f"Sixty per cent of the mark is individual (the quizzes, the assignments, Practical Test 1 and the demonstration; how the demonstration is marked is {TBC}).",
              f"Forty-five per cent of the mark is individual: the quizzes, the assignments and Practical Test 1. The Engineering ML project (45 per cent) is a take-home graded like Practical Test 1; "
              f"whether it is done individually or in teams is {TBC}.")
    D.replace("Practical Test 1 in Week 7 and the Week 12 demo have no quiz.", "Practical Test 1 in Week 7 and the Week 12 project clinic have no quiz.")
    # project marking
    D.set_whole("The project rubric is published here and applied without variation.",
                "The project is marked out of 45. Part A, the coded project notebook (30 marks), is auto-graded and also marked against a rubric, in the way Practical Test 1 is marked. "
                "Part B, a one-page decision memo (15 marks), is marked against a rubric. "
                f"The criterion-level rubrics and the split of Part A between automatic checks and rubric marks are {TBC} and will be published before the project is released. "
                "A model with a mediocre score that you have understood, validated and honestly reported will out-score a better score you cannot account for.")
    t = D.table_by_header(["Criterion", "Marks", "What earns them"])
    assert [r.cells[0].text.strip() for r in t.rows][:3] == ["Criterion", "Problem definition", "Data understanding"]
    set_cell(t.rows[0].cells[0], "Part")
    a, b = t.rows[1].cells, t.rows[2].cells
    set_cell(a[0], "Part A: coded project notebook")
    set_cell(a[1], "30")
    set_cell(a[2], f"Auto-graded checks on your code plus rubric marks, as for Practical Test 1. Covers Weeks 1 to 11 only. The split between checks and rubric marks is {TBC}.")
    set_cell(b[0], "Part B: one-page decision memo")
    set_cell(b[1], "15")
    set_cell(b[2], f"Rubric: a clear recommendation, the evidence for it, and its limits and risks, written for a non-specialist engineer. The marks for each criterion are {TBC}.")
    for k in range(len(t.rows) - 1, 2, -1):
        delete_row(t, k)
    D.replace(f"The mark scheme for the Week 12 demonstration is {TBC}, and will be published before the demo.",
              f"The project rubrics are {TBC} and will be published before the project is released.")
    D.replace("The two projects are done in teams of four to five, formed in Week 1 and kept for the semester.",
              f"The Data Analysis Project is done in a team of four to five, formed in Week 1 and kept for the semester. Whether the Engineering ML project is done in teams or individually is {TBC}.")
    D.set_whole("Any individual defence or reflection that goes with the Week 12 demo",
                f"There is no demo, no live defence and no reflection mark. If the project is done in teams, how each member's contribution is recorded is {TBC}. "
                "Whatever is set, an individual mark stays separate from shared project marks.")
    D.replace("you will be unable to answer a single question at the Week 12 demo.", "you will be unable to explain a single line of your own project.")
    D.set_whole("The project brief is given in Class 4 (Week 11 content) and the work is shown in a short demo in Week 12.",
                "The project brief is given in Class 4 (Week 11 content). You submit the project as a take-home, graded like Practical Test 1. It covers only what was taught in Weeks 1 to 11. "
                f"It is released after Class 4 and is due {DUE}. Week 12 is a project clinic: supervised work and questions, and no demo. The project has two parts: {PARTS}. "
                "The proposal is that you use the cohort data and the steps of Classes 1 to 4: clean, split, baseline, two or more models, a fair comparison, open the sealed test group once, and write the memo. "
                f"Whether you work alone or in a team, and whether you may choose your own problem, is {TBC}. Examples of the scope expected:")
    D.replace(f"Whether any recognition is given at the Week 12 demo is {TBC}; if it is, there is deliberately no prize for the highest accuracy.",
              "If the lecturer gives any recognition for projects, there is deliberately no prize for the highest accuracy.")
    D.replace("and the project demo will find you out.", "and the project will find you out.")
    D.replace("revised 2 November 2026 for the four-class second half and the Week 12 demo",
              "revised 2 November 2026 for the four-class second half and 3 November 2026 to remove the demo and make the project a submission")
    D.save()
    print(f"{Path(path).name}: patched ({code})")


# =====================================================================================================
# 2. Master teaching plan (docx)
# =====================================================================================================
def patch_master_docx(path):
    D = Doc(path)
    if D.patched:
        print(f"{Path(path).name}: already patched")
        return
    D.replace("which end with the Week 12 project demo.", "which end with the Week 12 project clinic.")
    D.replace("ending at the Week 12 project demo (Tuesday 1 December", "ending at the Week 12 project clinic (Tuesday 1 December")
    D.replace("Practical Test 2 and the Week 13 to 15 events were retired on 2 November 2026.",
              f"Practical Test 2 and the Week 13 to 15 events were retired on 2 November 2026. The demo was removed on 3 November 2026; the Engineering ML project is submitted instead, due {DUE}.")
    D.replace("in the last 20 minutes. Project brief.", f"in the last 20 minutes. Project brief given; project released (due {DUE_SHORT}).")
    t, r = D.find_row("12", "30 Nov")
    c = r.cells
    assert c[4].text.strip() == "Demo" and c[5].text.strip().startswith("Week 12: short project demo."), [x.text for x in c]
    text5 = c[5].text.strip()
    closes = text5[text5.index("Block 2 assignment"):text5.index(". Marks and arrangements")]
    assert closes.endswith("CML3111 Fri 4 Dec 11:00"), closes
    set_cell(c[4], "Clinic")
    set_cell(c[5], f"Week 12: project clinic (supervised work and questions; no demo). {closes}. The Engineering ML project is due {DUE_SHORT}.")
    D.replace("Block 4 · Week 12 · Short project demo", "Block 4 · Week 12 · Project clinic")
    D.set_whole("Week 12 (Tuesday 1 December for CML3112, Friday 4 December for CML3113 and CML3111) is a short project demo.",
                "Week 12 (Tuesday 1 December for CML3112, Friday 4 December for CML3113 and CML3111) is a project clinic. There is no demo and nobody presents. Students work on the Engineering ML project with supervision and ask questions. "
                f"The project is a take-home that they submit, graded like Practical Test 1. It covers only Weeks 1 to 11, is released after Class 4 and is due {DUE}. It has two parts: {PARTS}. "
                "The proposal is that students use the cohort data and the steps of Classes 1 to 4: clean, split, baseline, two or more models, a fair comparison, the sealed test group opened once, and the memo. "
                f"The rubrics, the split inside Part A, whether students work alone or in teams, the clinic room and helpers, and any reproducibility check are {TBC}.")
    # weighting table
    t = D.table_by_header(["Component", "When", "Mode", "Weight"])
    i = row_index(t, "Engineering ML Project")
    c = t.rows[i].cells
    assert c[3].text.strip() == "30%"
    set_cell(c[1], f"Brief in Class 4 (Week 11 content); released after Class 4; due {DUE_SHORT}")
    set_cell(c[2], f"Take-home submission, graded like Practical Test 1 (Part A /30, Part B /15); individual or team: {TBC}")
    set_cell(c[3], "45%")
    delete_row(t, row_index(t, "Week 12 short project demonstration"), "Week 12 short project demonstration")
    i = row_index(t, "Individual share of the total mark")
    assert t.rows[i].cells[3].text.strip() == "60%"
    set_cell(t.rows[i].cells[3], "45% (the project is not counted here)")
    i = row_index(t, "Team share of the total mark")
    assert t.rows[i].cells[3].text.strip() == "40%"
    set_cell(t.rows[i].cells[3], "10% (the Data Analysis Project; the project is not counted here)")
    D.replace("and shown in the Week 12 project demo, whose mark scheme is to be confirmed by the lecturer.",
              "and in the Engineering ML project, a take-home that students submit.")
    D.set_whole("Sixty per cent of the mark is individual on the component modes",
                "Forty-five per cent of the mark is individual on the component modes in the table above (the quizzes, the assignments and Practical Test 1). The Data Analysis Project (10 per cent) is a team mark. "
                f"The Engineering ML project (45 per cent) is a take-home graded like Practical Test 1, and whether it is done individually or in teams is {TBC}. "
                "With teams of four to five and up to twenty-two teams in the largest cohort, a team-heavy scheme would allow a weak student to pass on a strong teammate's work. "
                "An individual test, individually marked assignments and quizzes, and a project that is submitted and partly auto-graded make the team component safe to award — "
                "and they make the rotating team roles and contribution logs meaningful rather than decorative.")
    D.replace("Engineering ML Project 30% · Week 12 demonstration 15%", "Engineering ML Project 45% (Part A 30, Part B 15)")
    D.replace("Five rubrics are published in full in the workbook", "Four rubrics are published in full in the workbook")
    D.replace("The project rubric allocates fifteen marks to problem definition, fifteen to data understanding, twenty to methodology, twenty to engineering reasoning, fifteen to validation, ten to communication and five to reproducibility. "
              f"The rubric for the Week 12 demonstration is {TBC}.",
              "The project is marked out of 45: Part A, the coded notebook, 30 marks (auto-graded checks plus a rubric), and Part B, the one-page decision memo, 15 marks (rubric). "
              f"The criterion-level rubrics are {TBC} and will be published before the project is released.")
    D.replace("Individual typed defence and reflection are separate from shared project marks. Live questioning and peer comments are formative.",
              "There is no demo and no live defence. Peer comments are formative.")
    # workload table
    t = D.table_by_header(["Item", "Volume", "Illustrative human hours", "Automated workflow hours"])
    i = row_index(t, "Engineering ML Project + milestones")
    c = t.rows[i].cells
    set_cell(c[0], "Engineering ML Project (Part A and Part B)")
    set_cell(c[1], TBC_CAP)
    set_cell(c[2], TBC_CAP)
    delete_row(t, row_index(t, "Week 12 short project demo"), "Week 12 short project demo")
    D.replace("Faculty grade bands remain unconfigured.",
              "Faculty grade bands remain unconfigured. Until both project columns are marked it shows a provisional Semester 1 result out of 55 marks with the project PENDING, and no final percentage or band.")
    D.replace("which rests on the sixty per cent individual mark, the contribution log with repository evidence, and any individual defence at the Week 12 demo (to be confirmed by the lecturer). Shared project and individual marks remain separate; a live response does not silently rescale a team mark.",
              f"which rests on the forty-five per cent individual mark (the quizzes, the assignments and Practical Test 1), the contribution log with repository evidence, and the way individual work on the project is recorded ({TBC}). "
              "There is no demo and no live defence. Shared and individual marks remain separate.")
    D.replace("The Week 12 project demo, with about twenty-two teams in Cohort A at five minutes each, is roughly a hundred and ten minutes before a single question is asked, so its format, running order and any parallel rooms are to be confirmed by the lecturer.",
              f"The Week 12 project clinic brings a whole cohort, up to about a hundred students in Cohort A, into one session of supervised work and questions, so its room, helpers and running arrangements are {TBC}.")
    D.replace("Any individual defence at the Week 12 demo is to be confirmed by the lecturer. Live questioning is formative; repository evidence checks remain a release requirement.",
              "There is no demo and no live defence; repository evidence checks remain a release requirement.")
    # next steps
    t, r = D.find_row("8", "Project briefs, milestone checklists and the contribution log template")
    c = r.cells
    set_cell(c[1], "Project brief, Part A notebook and checks, Part B memo template, and the rubrics")
    set_cell(c[3], f"The project is released after Class 4 and is due {DUE}. The rubrics, the split inside Part A and team or individual work are {TBC}.")
    t, r = D.find_row("9", "Week 12 project demo arrangements")
    set_cell(r.cells[1], "Week 12 project clinic arrangements: room, helpers and supervision")
    # appendix A
    t, r = D.find_row("11", "ML core")
    assert "Project brief given; milestones and due dates: to be confirmed by the lecturer" in r.cells[5].text, r.cells[5].text
    set_cell(r.cells[5], f"Project brief given; project released (due {DUE_SHORT})")
    t, r = D.find_row("12", "Demo")
    c = r.cells
    set_cell(c[1], "Clinic")
    set_cell(c[2], "Project clinic (no demo)")
    set_cell(c[3], "Supervised work")
    set_cell(c[5], f"No demo. The Engineering ML project is due {DUE_SHORT}")
    D.replace("Week 12 — shown in the project demo", "Week 12 — shown in the project submission")
    D.save()
    print(f"{Path(path).name}: patched")


# =====================================================================================================
# 3. Weekly Quiz Operations Guide
# =====================================================================================================
def patch_quizops(path):
    D = Doc(path)
    if D.patched:
        print(f"{Path(path).name}: already patched")
        return
    D.replace("each component is worth 15% of the course. Use replaceWeek11Questions() to change the live Q10 forms, not rebuildAllForms().",
              "each component is worth 15% of the course. From 3 November 2026 there is no demo: the Engineering ML project (45%) is Part A /30 plus Part B /15, entered in two columns. "
              "Until both columns hold a mark the sheet shows 'Semester 1 provisional: x of 55 marks, y percent' and 'Project: PENDING', and leaves Final % and Band blank. "
              "Run prepareGradesColumns() once to add the new columns. Use replaceWeek11Questions() to change the live Q10 forms, not rebuildAllForms().")
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


def row_of(ws, text, col=1, exact=True):
    hits = [r for r in range(1, ws.max_row + 1) if isinstance(ws.cell(r, col).value, str) and (ws.cell(r, col).value == text if exact else ws.cell(r, col).value.startswith(text))]
    assert len(hits) == 1, f"{ws.title}: {len(hits)} rows with {text!r} in column {col}"
    return hits[0]


def delete_rows_keep(ws, idx, n=1, expect_prefix=None):
    """Delete rows, moving merged ranges and row heights up. Formulas are NOT translated; callers rewrite them."""
    if expect_prefix is not None:
        assert str(ws.cell(idx, 1).value).startswith(expect_prefix), (ws.title, idx, ws.cell(idx, 1).value)
    merges = [CellRange(r.coord) for r in ws.merged_cells.ranges]
    for m in merges:
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
            continue
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


def patch_weekly_sheet(ws):
    """Master Plan (Shared Core) and the three cohort sheets: project milestone (L or R), relevance (M or S), preparation (N or T)."""
    B, MIL, REL, PREP = col(ws, "Block"), col(ws, "Project milestone"), col(ws, "Assessment relevance"), col(ws, "Lecturer preparation")
    topic = col(ws, "Topic")
    challenge = col(ws, "Interactive challenge")
    for r, wk in ((12, "8"), (13, "9"), (14, "10"), (15, "11"), (16, "12")):
        assert str(ws.cell(r, 1).value).strip() == wk, (ws.title, r, ws.cell(r, 1).value)
    X(ws, f"{MIL}12", "The Engineering ML Project brief comes in Class 4; dates, milestones and mark scheme are to be confirmed by the lecturer.",
      f"The Engineering ML Project brief comes in Class 4; the project is released after Class 4 and due {DUE}.")
    XSET(ws, f"{MIL}13", "No project milestone this week.", f"No project milestone this week. The Engineering ML Project (45%) is introduced in Class 4 and released after it; it is due {DUE}.")
    XSET(ws, f"{MIL}15", "ENGINEERING ML PROJECT brief given in this class (30%).",
         f"ENGINEERING ML PROJECT brief given in this class (45%): Part A coded notebook 30, Part B decision memo 15. Released after this class; due {DUE}. Week 12 is a project clinic.")
    X(ws, f"{REL}14", " Validation carries 15 of the 100 marks in the project rubric.", "")
    X(ws, f"{REL}15", " Engineering reasoning carries 20 of the 100 project marks.", "")
    assert ws[f"{B}16"].value == "Block 4 - Short Project Demo", ws[f"{B}16"].value
    ws[f"{B}16"].value = "Block 4 - Project Clinic"
    ws[f"{topic}16"].value = "Project clinic (no demo)"
    ws[f"{challenge}16"].value = f"The clinic: supervised work on the project, and questions. No demo. Room and helpers: {TBC}."
    ws[f"{MIL}16"].value = f"Project clinic. The Engineering ML Project is due {DUE}."
    ws[f"{REL}16"].value = f"Engineering ML Project (45%): Part A coded notebook 30, Part B decision memo 15. Rubrics: {TBC}."
    ws[f"{PREP}16"].value = f"• Clinic arrangements (room, helpers): {TBC}."


def patch_workbook(path):
    wb = openpyxl.load_workbook(path)
    if MARK in (wb.properties.keywords or ""):
        print(f"{Path(path).name}: already patched")
        return
    # ---------------- Read Me
    ws = wb["Read Me"]
    X(ws, "B33", "Week 12 is the short project demo), teaching, assessment and demo weeks marked,", "Week 12 is the project clinic), teaching, assessment and clinic weeks marked,")
    XSET(ws, "B39", "The before-and-after arithmetic",
         f"The before-and-after arithmetic: about 152 illustrative hours fully human for the weekly challenges, Practical Test 1, the Data Analysis Project and gradebook reconciliation (the Engineering ML project's marking time is {TBC}); the stack's hours are pilot pending.")
    X(ws, "B40", "All five rubrics", "All four rubrics")
    # ---------------- Calendar
    ws = wb["Calendar"]
    X(ws, "A2", "Week 12 is the short project demo.", "Week 12 is the project clinic (no demo).")
    assert ws["B16"].value == "Block 4 - Short Project Demo" and ws["G16"].value == "Demo"
    ws["B16"].value = "Block 4 - Project Clinic"
    ws["G16"].value = "Clinic"
    X(ws, "H16", "Week 12: short project demo (proposal, not final).", "Week 12: project clinic (supervised work and questions; no demo).")
    X(ws, "H16", "Marks and arrangements: to be confirmed by the lecturer.", f"The Engineering ML Project is due {DUE}. Clinic arrangements: {TBC}.")
    X(ws, "H15", "Project brief.", f"Project brief given; project released (due {DUE_SHORT}).")
    X(ws, "A18", "Demo week: 1 (Week 12).", "Clinic week: 1 (Week 12).")
    X(ws, "A19", "green = project demo day.", "green = project clinic week.")
    # ---------------- Weekly sheets
    for name in ("Master Plan (Shared Core)", "Cohort A", "Cohort B", "Cohort C"):
        patch_weekly_sheet(wb[name])
    # ---------------- Assessment (delete bottom-up: Model 2 demonstration row, then Model 1 row)
    ws = wb["Assessment"]
    XSET(ws, "A2", "Entirely practical", "Entirely practical, continuous and project-based. No traditional written examination. 45% of the mark is individual on the component modes below (quizzes, assignments and Practical Test 1); "
         f"the Engineering ML project is a take-home graded like Practical Test 1 and whether it is individual or in teams is {TBC}; automatic grading coverage is validated assessment by assessment.")
    m2 = row_of(ws, "Week 12 demonstration")
    delete_rows_keep(ws, m2, 1, expect_prefix="Week 12 demonstration")
    m1 = row_of(ws, "Week 12 short project demonstration")
    delete_rows_keep(ws, m1, 1, expect_prefix="Week 12 short project demonstration")
    return_rows = [x for x in range(1, ws.max_row + 1) if ws.cell(x, 1).value == "Engineering ML Project"]
    assert len(return_rows) == 2, return_rows
    p1, p2 = return_rows
    assert ws.cell(p1, 4).value == 0.3 and ws.cell(p2, 4).value == 0.3
    ws.cell(p1, 2).value = f"Brief in Class 4 (Week 11 content); released after Class 4; due {DUE_SHORT}"
    ws.cell(p1, 3).value = f"Individual or team: {TBC}"
    ws.cell(p1, 4).value = 0.45
    ws.cell(p1, 5).value = (f"Take-home submission covering Weeks 1 to 11 only. Part A: coded project notebook, 30 marks, auto-graded plus rubric, like Practical Test 1. "
                            f"Part B: one-page decision memo, 15 marks, rubric. Rubrics and the split inside Part A: {TBC}. No demo.")
    ws.cell(p2, 2).value = f"Due {DUE_SHORT}"
    ws.cell(p2, 3).value = f"Individual or team: {TBC}"
    ws.cell(p2, 4).value = 0.45
    totals = [x for x in range(1, ws.max_row + 1) if ws.cell(x, 1).value == "TOTAL"]
    assert len(totals) == 2, totals
    t1, t2 = totals
    ind, team, cov = row_of(ws, "Of which individual"), row_of(ws, "Of which team"), row_of(ws, "Automatic grading coverage")
    assert (ind, team, cov) == (t1 + 1, t1 + 2, t1 + 3), (t1, ind, team, cov)
    # Model 1 rows are 6..p1 ; Model 2 component rows
    first_component = 6
    ws.cell(t1, 4).value = f"=SUM(D{first_component}:D{t1 - 1})"
    ws.cell(ind, 1).value = "Of which individual (quizzes, assignments, Practical Test 1)"
    ws.cell(ind, 4).value = f"=D{first_component}+D{first_component + 1}+D{first_component + 3}"
    ws.cell(team, 1).value = "Of which team (Data Analysis Project)"
    ws.cell(team, 4).value = f"=D{first_component + 2}"
    assert ws.cell(first_component, 1).value.startswith("QUIZZES") and ws.cell(first_component + 2, 1).value == "Data Analysis Project" and ws.cell(first_component + 3, 1).value.startswith("PRACTICAL TEST 1")
    ws.cell(ind, 6).value = (f"Quizzes, assignments and Practical Test 1 are individually assessed. The Engineering ML project (45%) is counted in neither line: individual or team is {TBC}.")
    ws.cell(team, 6).value = "The Data Analysis Project is the team component."
    # Model 2 total: quizzes, practical challenges, DA, Test 1, project
    q2 = row_of(ws, "Quizzes (weekly W1-W5, then one sitting per block)")
    assert [ws.cell(q2 + k, 1).value for k in (1, 2, 3)] == ["Practical challenges (weekly W1-W5, then two block packs)", "Data Analysis Project", "Practical Test 1"], [ws.cell(q2 + k, 1).value for k in (1, 2, 3)]
    assert ws.cell(q2 + 4, 1).value.startswith("FINAL ASSESSMENT") and q2 + 5 == p2 and t2 == p2 + 1, (q2, p2, t2)
    ws.cell(t2, 4).value = f"=D{q2}+D{q2 + 1}+D{q2 + 2}+D{q2 + 3}+D{p2}"
    # design notes
    n = row_of(ws, "Why one practical test")
    X(ws, f"B{n}", "End-to-end capability is now shown in the Block 2 assignment, the quizzes and the Week 12 project demo, whose mark scheme is to be confirmed by the lecturer.",
      "End-to-end capability is now shown in the Block 2 assignment, the quizzes and the Engineering ML project, a take-home that students submit.")
    n = row_of(ws, "Why 60% individual")
    ws.cell(n, 1).value = "Why 45% individual"
    X(ws, f"B{n}", "provide individual evidence alongside shared project marks; any individual defence at the Week 12 demo is to be confirmed by the lecturer.",
      f"provide individual evidence alongside shared project marks. The project is a take-home graded like Practical Test 1; individual or team is {TBC}.")
    n = row_of(ws, "Why nothing rewards accuracy alone")
    X(ws, f"B{n}", "Across all five rubrics", "Across all four rubrics")
    X(ws, f"B{n}", "If recognition is given at the Week 12 demo (to be confirmed by the lecturer), there is no prize for highest accuracy.",
      "If the lecturer gives recognition for projects, there is no prize for highest accuracy.")
    # ---------------- Rubrics
    ws = wb["Rubrics"]
    a4 = row_of(ws, "Engineering ML Project (30%) - as specified by the lecturer")
    ws.cell(a4, 1).value = f"Engineering ML Project (45%) - Part A coded notebook 30, Part B decision memo 15; criterion marks {TBC}"
    first = row_of(ws, "Problem definition")
    last = row_of(ws, "Reproducibility & documentation")
    assert last - first == 6 and ws.cell(last + 1, 1).value == "TOTAL"
    ws.cell(first, 1).value = "Part A: coded project notebook"
    ws.cell(first, 2).value = 30
    ws.cell(first, 3).value = f"Auto-graded checks on your code plus rubric marks, as for Practical Test 1. Covers Weeks 1 to 11 only. The split between automatic checks and rubric marks is {TBC}."
    ws.cell(first, 4).value = TBC_CAP
    ws.cell(first + 1, 1).value = "Part B: one-page decision memo"
    ws.cell(first + 1, 2).value = 15
    ws.cell(first + 1, 3).value = f"Rubric: a clear recommendation, the evidence for it, and its limits and risks, written for a non-specialist engineer. The marks for each criterion are {TBC}."
    ws.cell(first + 1, 4).value = TBC_CAP
    delete_rows_keep(ws, first + 2, 5)                 # the five other old criterion rows
    # demo rubric block: title row to the blank row after its TOTAL
    d0 = row_of(ws, f"Week 12 short project demo (15%) - mark scheme {TBC}")
    assert ws.cell(d0 + 6, 1).value == "TOTAL" and ws.cell(d0 + 7, 1).value is None, (ws.cell(d0 + 6, 1).value, ws.cell(d0 + 7, 1).value)
    delete_rows_keep(ws, d0, 8)
    note = row_of(ws, "Apply the published execution", exact=False)
    X(ws, f"A{note}", "Individual typed defence and reflection are separate from shared project marks. Live and peer feedback are formative.",
      "There is no demo and no live defence. Peer feedback is formative.")
    # rewrite every TOTAL formula from the header row above it
    for rr in range(1, ws.max_row + 1):
        if ws.cell(rr, 1).value == "TOTAL":
            h = rr - 1
            while ws.cell(h, 1).value not in ("Criterion",):
                h -= 1
                assert h > 0
            ws.cell(rr, 2).value = f"=SUM(B{h + 1}:B{rr - 1})"
    # ---------------- Assessment Tech Stack
    ws = wb["Assessment Tech Stack"]
    X(ws, "B8", "flag missing work.", "flag missing work. Until both project columns are marked it shows a provisional Semester 1 result out of 55 marks with the project PENDING, and no final percentage or band.")
    # ---------------- Marking Load
    ws = wb["Marking Load"]
    r9 = row_of(ws, "Engineering ML Project + milestones")
    ws.cell(r9, 1).value = "Engineering ML Project (Part A and Part B)"
    ws.cell(r9, 2).value = TBC
    ws.cell(r9, 3).value = TBC
    ws.cell(r9, 4).value = TBC
    ws.cell(r9, 6).value = f"Take-home project, Part A auto-graded plus rubric, Part B rubric. Marking time: {TBC} (teams or individuals)."
    r10 = row_of(ws, "Week 12 short project demo")
    delete_rows_keep(ws, r10, 1, expect_prefix="Week 12 short project demo")
    tot = row_of(ws, "TOTAL (hours per semester)")
    ws.cell(tot, 4).value = f"=SUM(D5:D{tot - 1})"
    ws.cell(tot, 5).value = f'=IF(COUNT(E5:E{tot - 1})=ROWS(E5:E{tot - 1}),SUM(E5:E{tot - 1}),"Pilot pending")'
    ws.cell(tot + 1, 5).value = f'=IF(ISNUMBER(E{tot}),D{tot}-E{tot},"Pilot pending")'
    # ---------------- Risk Register
    ws = wb["Risk Register"]
    X(ws, "E13", f"Any individual defence at the Week 12 demo is {TBC}; live questioning is formative.", "There is no demo and no live defence.")
    ws["B21"].value = "The four remaining classes slip, and the project work is squeezed."
    X(ws, "E21", f"The Week 12 demo format and milestones are {TBC}.", "Week 12 is a project clinic, which gives one more session of supervised project work.")
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
