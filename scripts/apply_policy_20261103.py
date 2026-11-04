"""Apply the decision of 3 November 2026 (data/assessment_blocks_20261103.json): no demo; the Engineering ML project is submitted
(take-home, graded like Practical Test 1, Weeks 1 to 11 only), Part A /30 + Part B /15; weights 15/15/10/15/45; Week 12 is a project clinic.

  * data/assessments.json: DEMO rows retired; ML_PROJECT rows get two parts, maximum 45 and PROPOSED dates. No form window is opened
    (opens_at and closes_at stay null);
  * student_guides/<cohort>/B1.md, B2.md, DEMO.md (retired notice), ML_PROJECT.md;
  * Assignment_Submission_Links.md, Assignment_Instructions_Index.md, grader/README.md, grader/Grades_template.csv,
    scripts/assessment_registry.py, scripts/build_quizops_docx.py (the source of the Quiz Operations Guide);
  * grader/retire_demo_forms_20261103.gs (generated, pure ASCII; for the SUBMISSION Apps Script project);
  * header notes on the 2 November arrangement note, by-hand checklist and verification record;
  * the two 2 November scripts that would overwrite these changes are made to stop with "SUPERSEDED".
Every file is copied to a sibling _backup_2026-11-03 folder first (first copy wins) and every replacement asserts its match count.
Idempotent. Usage: python3 scripts/apply_policy_20261103.py"""
import json, re, sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from backup_20261103 import backup

ROOT = Path(__file__).resolve().parents[1]; BASE = ROOT / "IUEA_Teaching_Plan"; GRADER = BASE / "grader"
POL = json.loads((ROOT / "data" / "assessment_blocks_20261103.json").read_text())
COHORTS = ("CML3111", "CML3112", "CML3113")
MARK = "BLOCK_ASSESSMENT_20261103"
NOTE = "Block_Assessment_Arrangement_2026-11-03.md"
TBC = "to be confirmed by the lecturer"
PROJ = POL["engineering_ml_project"]
DUE_ISO = PROJ["due"]["all_cohorts"]
CLINIC = POL["calendar"]["week_12_project_clinic"]["dates"]
CLASS4 = PROJ["released"]["dates"]


def day(iso):
    d = datetime.fromisoformat(iso); return f"{d.strftime('%A')} {d.day} {d.strftime('%B')}"


def rep(text, old, new, count=1, where=""):
    n = text.count(old)
    assert n == count, f"{where}: expected {count} match(es), found {n}: {old[:80]!r}"
    return text.replace(old, new)


def ascii_only(text, name):
    bad = sorted({c for c in text if ord(c) > 127})
    if bad: raise SystemExit(f"{name}: non-ASCII characters {bad[:8]}; generated .gs must be pure ASCII")
    return text


# ------------------------------------------------------------------------------------------------ registry
def update_registry():
    path = ROOT / "data" / "assessments.json"; rows = json.loads(path.read_text()); before = json.dumps(rows, sort_keys=True)
    backup(path)
    for code in COHORTS:
        d = [x for x in rows if x["key"] == f"{code}|DEMO"]; assert len(d) == 1, (code, "DEMO", len(d))
        d = d[0]
        d.update(status="RETIRED", retired=True, opens_at=None, closes_at=None,
                 delivery_note="The demo was dropped on 3 November 2026. There is no demo and no demonstration mark. Week 12 is a project clinic. No form window is opened and nothing is marked on this form.")
        m = [x for x in rows if x["key"] == f"{code}|ML_PROJECT"]; assert len(m) == 1, (code, "ML_PROJECT", len(m))
        m = m[0]
        m.update(title="Engineering ML project", maximum=PROJ["marks"],
                 formats=PROJ["submission_formats"], grading="rubric", status="DATE_TO_BE_CONFIRMED", opens_at=None, closes_at=None,
                 parts=[dict(part=p["part"], id=p["id"], gradebook_column=p["gradebook_column"], title=p["title"], maximum=p["marks"], marking=p["marking"]) for p in PROJ["parts"]],
                 scope=PROJ["scope"],
                 proposed_released_after_class_4=CLASS4[code],
                 proposed_closes_at=DUE_ISO,
                 proposed_status="proposed, lecturer to confirm",
                 delivery_note=("Take-home project, submitted by the student and graded like Practical Test 1. One submission with two parts: Part A coded project notebook (30), "
                                "Part B one-page decision memo (15). Covers Weeks 1 to 11 only. Release after Class 4 and due Friday 11 December 2026 23:59 Kampala are "
                                "PROPOSED dates, lecturer to confirm. No form window is open: opens_at and closes_at stay null until the lecturer sets them. "
                                "Rubrics, the split inside Part A and whether teams are allowed: " + TBC + "."))
    path.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n")
    return json.dumps(rows, sort_keys=True) != before


# ------------------------------------------------------------------------------------------------ student guides
def block_paragraph(code):
    return (f"There is no Practical Test 2, no demo, and no quiz or assignment after Block 2. Week 12 ({day(CLINIC[code])}) is a project clinic: you work on the project with supervision and ask questions. "
            f"Nobody presents.\n\n"
            f"The Engineering ML project is a take-home that you submit. It covers only what was taught in Weeks 1 to 11. It is released after Class 4 ({day(CLASS4[code])}) "
            f"and is due Friday 11 December 2026, 23:59 Kampala (proposed, lecturer to confirm). It is worth 45 percent of the course: Part A, the coded project notebook (30 marks, "
            f"auto-graded plus a rubric, like Practical Test 1), and Part B, a one-page decision memo (15 marks, rubric).\n\n"
            f"Your Semester 1 result can be published before the project is marked. It then shows as provisional, out of 55 marks, with the project marked PENDING. "
            f"The full total out of 100 appears when the project is marked.")


def patch_guides():
    for code in COHORTS:
        g = BASE / "student_guides" / code
        for bid in ("B1", "B2"):
            p = g / f"{bid}.md"; t = p.read_text()
            if MARK in t: continue
            backup(p)
            old = (f"There is no Practical Test 2 and no quiz or assignment after Block 2. The semester ends with a short project demo in Week 12 ({day(CLINIC[code])}). "
                   f"Its format, marks and the project dates will be confirmed by your lecturer.")
            t = rep(t, old, f"<!-- {MARK} -->\n" + block_paragraph(code), where=str(p))
            p.write_text(t)
        p = g / "DEMO.md"; t = p.read_text()
        if MARK not in t:
            backup(p)
            first, rest = t.split("\n", 1)
            notice = (f"<!-- {MARK} -->\n> **RETIRED on 3 November 2026.** There is no demo. Week 12 is a project clinic and nobody presents. "
                      f"The Engineering ML project is submitted instead: see [ML_PROJECT.md](ML_PROJECT.md). Ignore the instructions below. This form is closed.\n\n")
            p.write_text(first + "\n\n" + notice + rest.lstrip("\n"))
        p = g / "ML_PROJECT.md"; t = p.read_text()
        if MARK not in t:
            backup(p)
            t = rep(t, "**Submit:** TWO files together: your completed notebook (.ipynb) AND one complete report (DOCX or selectable-text PDF).",
                    f"<!-- {MARK} -->\n**Submit:** your project, which has two parts. Part A: the coded project notebook (30 marks, auto-graded plus a rubric, like Practical Test 1). "
                    f"Part B: a one-page decision memo (15 marks, rubric). Together they are worth 45 percent of the course. How you hand it in (one notebook with the memo inside, or a notebook plus a separate memo file) is {TBC}, and the project brief will say.\n\n"
                    f"This is a take-home that you submit. It covers only what was taught in Weeks 1 to 11. There is no demo. Individual or team work, the split of marks inside Part A and the rubrics are {TBC} "
                    f"and will be published when the project is released.", where=str(p))
            t, n = re.subn(r"\*\*Deadline:\*\* to be confirmed by the lecturer\. The semester now ends at Week 12 \(demo day [A-Za-z]+ \d+ [A-Za-z]+\); the 15 December date no longer applies\. The live form shows any later change\.",
                           f"**Deadline (proposed, lecturer to confirm):** released after Class 4 ({day(CLASS4[code])}); due Friday 11 December 2026, 23:59 Kampala. "
                           f"Week 12 ({day(CLINIC[code])}) is a project clinic. The live form shows the deadline that counts.", t)
            assert n == 1, (p, n)
            t = rep(t, "3. Use the **Report checklist** in the notebook to write one report. Include all listed evidence, captions, repository URL and run instructions. A repository link alone is not the report.\n\nInclude the two-page engineering brief, contribution log and AI-use declaration.",
                    f"3. Write Part B, a one-page decision memo for a non-specialist engineer: your recommendation, the evidence for it, and its limits and risks. Add your AI-use declaration. The memo format is {TBC}.", where=str(p))
            p.write_text(t)


# ------------------------------------------------------------------------------------------------ markdown docs
def patch_links_md():
    p = BASE / "Assignment_Submission_Links.md"; t = p.read_text()
    if MARK in t: return
    backup(p)
    t = rep(t, "Major projects, practical tests and DEMO remain held pending complete grading validation.",
            "The project and the practical test remain held pending complete grading validation. The DEMO form is retired (3 November 2026: there is no demo).", where=str(p))
    t = rep(t, "(the 30 October note is superseded).",
            f"(the 30 October note is superseded). **Update of 3 November 2026:** there is no demo. The Engineering ML project is submitted as a take-home (Part A notebook, 30 marks; Part B one-page memo, 15 marks), "
            f"proposed due Friday 11 December 2026, 23:59 Kampala (proposed, lecturer to confirm). Its form stays closed until the lecturer sets a window. See [{NOTE}]({NOTE}). <!-- {MARK} -->", where=str(p))
    t, n = re.subn(r"(?m)^\| ML_PROJECT: Engineering ML project \| to be confirmed by the lecturer \| to be confirmed by the lecturer \|",
                   "| ML_PROJECT: Engineering ML project (Part A notebook /30, Part B memo /15) | after Class 4 (proposed, lecturer to confirm) | Fri 11 Dec 2026 23:59 (proposed, lecturer to confirm) |", t)
    assert n == 3, n
    t, n = re.subn(r"(?m)^\| DEMO: Presentation and individual reflection \| to be confirmed by the lecturer \(demo day is in Week 12\) \| to be confirmed by the lecturer \(demo day is in Week 12\) \|",
                   "| DEMO: RETIRED on 3 November 2026 (no demo) | retired | retired |", t)
    assert n == 3, n
    p.write_text(t)


def patch_index_md():
    p = BASE / "Assignment_Instructions_Index.md"; t = p.read_text()
    if MARK in t: return
    backup(p)
    t, n = re.subn(r"(?m)^(- \[CML31\d\d\|DEMO\]\(student_guides/CML31\d\d/DEMO\.md\))$", r"\1 (retired 3 November 2026)", t)
    assert n == 3, n
    t = rep(t, "Read [Block_Assessment_Arrangement_2026-11-02.md](Block_Assessment_Arrangement_2026-11-02.md).",
            f"Read [{NOTE}]({NOTE}) (3 November 2026: no demo; the Engineering ML project is submitted, Part A /30 and Part B /15; the 2 November note is superseded). <!-- {MARK} -->", where=str(p))
    p.write_text(t)


def patch_readme():
    p = GRADER / "README.md"; t = p.read_text()
    if MARK in t: return
    backup(p)
    t = rep(t, "| ML project | 30% | /100 (due date and mark scheme to be confirmed by the lecturer) |\n| Demo (Week 12) | 15% | /100 (mark scheme to be confirmed by the lecturer) |\n",
            "| Engineering ML project | 45% | Part A coded notebook /30 (column `ML Project Part A`) + Part B decision memo /15 (column `ML Project Part B`). Take-home, Weeks 1 to 11 only. Due date proposed Friday 11 December 2026 23:59 Kampala, lecturer to confirm |\n", where=str(p))
    t = rep(t, "Practical Test 2 was dropped on 2 November 2026. The table above replaces the 10/10/10/15/20/25/10 weights.",
            "Practical Test 2 was dropped on 2 November 2026 and the demo on 3 November 2026. The table above replaces the 10/10/10/15/20/25/10 weights. The weights sum to 100. "
            "Until both project columns hold a mark the sheet shows `Semester 1 provisional: x of 55 marks, y percent` and `Project: PENDING`, and leaves Final % and Band blank; see the 3 November section at the end.", where=str(p))
    t = rep(t, "DOCX, selectable-text PDF and PPTX speaker notes are supported.",
            "(The DEMO rubric is retired from 3 November 2026. The same command can grade the Part B decision memo once its rubric exists.) DOCX, selectable-text PDF and PPTX speaker notes are supported.", where=str(p))
    t = t.rstrip("\n") + f"""

<!-- {MARK} -->
## Grading update of 3 November 2026 (no demo; provisional results)

- Weights: quizzes 15, assignments 15, data analysis project 10, Practical Test 1 15, Engineering ML project 45 (Part A /30, Part B /15). The demonstration is removed. Blocks, best-of rules and the 35 and 160 totals are unchanged.
- Gradebook columns: `ML Project Part A`, `ML Project Part B`, then `Semester 1 provisional` and `Project` (written by the script), then `Final %`, `Band`. Run `prepareGradesColumns()` once on the live sheet to add any that are missing; it never deletes anything. The old `ML Project` and `Demo` columns are ignored.
- Provisional mode: a blank project column means the project is not marked yet. The sheet shows `Semester 1 provisional: x of 55 marks, y percent` (quizzes, assignments, data analysis project and Test 1) and `Project: PENDING`. Final % and Band stay blank. Once both columns hold a number the sheet shows the full total out of 100. Type 0 and 0 for a student who submitted no project.
- A missing quiz or assignment part still scores zero. A blank data analysis project or Practical Test 1 also scores zero and is listed under Missing.
- CA ledger and totals: `python3 IUEA_Teaching_Plan/grader/continuous_assessment.py --source SOURCE_DIR --out LEDGER.json --totals-out TOTALS.csv` (add `--results RESULTS.json`, `--timing TIMING.json` and `--test-ledger LEDGER.json` as before). Project marks go in `results.json` as `part_scores` (`{{"A": 24.5}}` while only Part A is marked, status `PART_MARKED`; both parts and status `GRADED` when finished).
- Source of truth: `../../data/assessment_blocks_20261103.json`. Note: `{NOTE}`. By-hand steps: `Grading_Update_By_Hand_2026-11-03.md`.
- Submission project: `retire_demo_forms_20261103.gs` closes and retires the three DEMO forms (run `retireDemoForms()` once, then `showDemoRetirement()`). It opens no form window.
"""
    p.write_text(t)


def patch_template():
    p = GRADER / "Grades_template.csv"; raw = p.read_bytes(); t = raw.decode("ascii")
    if "ML Project Part A" in t: return
    backup(p)
    t = rep(t, "ML Project,Demo,Final %", "ML Project Part A,ML Project Part B,Semester 1 provisional,Project,Final %", where=str(p))
    p.write_bytes(t.encode("ascii"))


def patch_registry_py():
    p = ROOT / "scripts" / "assessment_registry.py"; t = p.read_text()
    if "20261103" in t: return
    backup(p)
    t = rep(t, "# Weights of 2 November 2026 (no Practical Test 2; data/assessment_blocks_20261102.json is the source of truth).\nWEIGHTS = {'quizzes': 15, 'challenges': 15, 'data_project': 10, 'test1': 15,\n           'ml_project': 30, 'demo': 15}\n",
            "# Weights of 3 November 2026 (no Practical Test 2, no demo; data/assessment_blocks_20261103.json is the source of truth).\n# ml_project = Part A coded notebook /30 + Part B decision memo /15.\nWEIGHTS = {'quizzes': 15, 'challenges': 15, 'data_project': 10, 'test1': 15,\n           'ml_project': 45}\n", where=str(p))
    t = rep(t, "['Data Analysis Project','Practical Test 1','ML Project','Demo','Final %','Band','Missing','Challenges done']",
            "['Data Analysis Project','Practical Test 1','ML Project Part A','ML Project Part B','Semester 1 provisional','Project','Final %','Band','Missing','Challenges done']", where=str(p))
    t = rep(t, "NOTE 2 November 2026:", "NOTE 3 November 2026: the demo is removed and the ML project is submitted (scripts/apply_policy_20261103.py patched assessments.json in place; do not regenerate it here).\nNOTE 2 November 2026:", where=str(p))
    p.write_text(t)


QUIZOPS_OLD = "each component is worth 15% of the course. Use replaceWeek11Questions() to change the live Q10 forms, not rebuildAllForms()."
QUIZOPS_NEW = ("each component is worth 15% of the course. From 3 November 2026 there is no demo: the Engineering ML project (45%) is Part A /30 plus Part B /15, entered in two columns. "
               "Until both columns hold a mark the sheet shows \\'Semester 1 provisional: x of 55 marks, y percent\\' and \\'Project: PENDING\\', and leaves Final % and Band blank. "
               "Run prepareGradesColumns() once to add the new columns. Use replaceWeek11Questions() to change the live Q10 forms, not rebuildAllForms().")


def patch_quizops_source():
    p = ROOT / "scripts" / "build_quizops_docx.py"; t = p.read_text()
    if "From 3 November 2026 there is no demo" in t: return
    backup(p)
    p.write_text(rep(t, QUIZOPS_OLD, QUIZOPS_NEW, where=str(p)))


def patch_arrangement_headers():
    heads = {
        "Block_Assessment_Arrangement_2026-11-02.md": (
            f"> **Superseded in part on 3 November 2026 by `{NOTE}`.** The blocks, deadlines, quiz sittings and the 35 and 160 totals below still stand. "
            f"There is no Week 12 demo, the weights table and the project paragraph below no longer apply, and the Engineering ML project is now submitted (Part A /30, Part B /15, weight 45). "
            f"The source of truth is `data/assessment_blocks_20261103.json`.\n\n"),
        "Block_Assessment_By_Hand_Checklist_2026-11-02.md": (
            "> **Update of 3 November 2026.** Parts A and B below are unchanged. Part C (gradebook) is replaced by `Grading_Update_By_Hand_2026-11-03.md`, "
            "and the project and demo items in part D no longer apply (there is no demo).\n\n"),
        "Block_Assessment_Verification_2026-11-02.md": (
            "> **Update of 3 November 2026.** The checks below were run before the demo was removed. The new checks are listed in `Grading_Update_By_Hand_2026-11-03.md` and the verification section of `Block_Assessment_Arrangement_2026-11-03.md`.\n\n")}
    for name, note in heads.items():
        p = BASE / name; t = p.read_text()
        if "3 November 2026" in t.split("\n", 6)[0:6].__str__(): continue
        backup(p)
        first, rest = t.split("\n", 1)
        assert first.startswith("# "), (name, first)
        p.write_text(first + "\n\n" + note + rest.lstrip("\n"))


STUB = ("import sys\nsys.exit('SUPERSEDED on 3 November 2026 by scripts/{new}. Running this script would overwrite the 3 November changes '\n         '(the demo is removed and the ML project is submitted). The files it generated are still in place.')\n")


def supersede_scripts():
    for old, new in (("apply_block_policy_20261102.py", "apply_policy_20261103.py"), ("patch_block_docs_20261102.py", "apply_policy_20261103.py")):
        p = ROOT / "scripts" / old; t = p.read_text()
        if "SUPERSEDED on 3 November 2026" in t: continue
        backup(p)
        # insert the guard right after the module docstring so importing the module for its helpers still works only if main() is not run
        t = rep(t, "\n\ndef main():", "\n\ndef main():\n    " + STUB.format(new=new).replace("\n", "\n    ").rstrip(" ") , where=str(p))
        p.write_text(t)
    p = ROOT / "scripts" / "build_block_packages_20261102.py"; t = p.read_text()
    if "assessment_blocks_20261103.json" not in t:
        backup(p)
        p.write_text(rep(t, 'ROOT / "data" / "assessment_blocks_20261102.json"', 'ROOT / "data" / "assessment_blocks_20261103.json"', where=str(p)))


# ------------------------------------------------------------------------------------------------ retire the DEMO forms (submission project)
def retire_gs():
    keys = [f"{c}|DEMO" for c in COHORTS]
    text = ascii_only(f"""/** Generated by scripts/apply_policy_20261103.py. Paste into the Apps Script SUBMISSION project (the one that holds submission_forms.gs) as a new file.
 *  There is no demo from 3 November 2026. This file closes and retires the three DEMO forms. It does NOT open any form window.
 *
 *  retireDemoForms()      for each DEMO form: records a release decision of "not released" (this keeps the form closed even if a window is set),
 *                         marks the entry retired, closes the form and shows a closed-form message. Responses are kept. Safe to run twice.
 *  showDemoRetirement()   read-only. Prints one line for each DEMO form. */
var DEMO_FORM_KEYS = {json.dumps(keys)};
var DEMO_RETIRED_EVIDENCE = 'Retired on 3 November 2026: there is no demo this semester, so nothing is collected or marked on this form.';
var DEMO_CLOSED_MESSAGE = 'This form is retired. There is no demo this semester. The Engineering ML project is submitted instead; your lecturer will tell you when it opens.';

function retireDemoForms() {{
  var done = 0, missing = 0;
  DEMO_FORM_KEYS.forEach(function (key) {{
    var state = submissionState_();
    if (!state[key] || !state[key].formId) {{ Logger.log('no form recorded for ' + key); missing++; return; }}
    setAssessmentRelease(key, false, DEMO_RETIRED_EVIDENCE);
    state = submissionState_();
    state[key].retired = true;
    state[key].retiredAt = new Date().toISOString();
    saveSubmissionState_(state, key);
    var form = FormApp.openById(state[key].formId);
    form.setAcceptingResponses(false);
    form.setCustomClosedFormMessage(DEMO_CLOSED_MESSAGE);
    Logger.log('RETIRED ' + key + ', ' + form.getResponses().length + ' responses kept');
    done++;
  }});
  Logger.log('retireDemoForms: ' + done + ' retired, ' + missing + ' not found (expected 3 retired, 0 not found). No form window was opened.');
}}

function showDemoRetirement() {{
  var state = submissionState_(), ok = 0, bad = 0;
  DEMO_FORM_KEYS.forEach(function (key) {{
    var s = state[key];
    if (!s || !s.formId) {{ Logger.log('MISSING ' + key + ': no such form in the submission state'); bad++; return; }}
    var open = FormApp.openById(s.formId).isAcceptingResponses();
    var good = s.retired === true && s.assessmentReleased === false && !open;
    Logger.log((good ? 'OK      ' : 'NOT RETIRED ') + key + '  retired=' + (s.retired === true) + '  released=' + s.assessmentReleased + '  accepting responses=' + open);
    if (good) {{ ok++; }} else {{ bad++; }}
  }});
  Logger.log('showDemoRetirement: ' + ok + ' OK, ' + bad + ' need attention (expected 3 OK).');
}}
""", "retire_demo_forms_20261103.gs")
    p = GRADER / "retire_demo_forms_20261103.gs"
    if not p.exists() or p.read_text() != text:
        p.write_text(text)


def main():
    changed = update_registry()
    patch_guides(); patch_links_md(); patch_index_md(); patch_readme(); patch_template(); patch_registry_py(); patch_quizops_source()
    patch_arrangement_headers(); supersede_scripts(); retire_gs()
    print("done; registry changed:" , changed)


if __name__ == "__main__":
    main()
