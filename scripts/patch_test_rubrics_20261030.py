"""Publish the Test 1 and Test 2 rubrics that the graders and the student notebooks actually use (idempotent).

The syllabi, master plan and lecturer guide described a report-style Test 1 (profiling, cleaning justification,
findings, recommendation) and an end-to-end Test 2 with cross-validation and limitations. The tests that were built,
sat and graded are coding tests in Colab: Test 1 has eight coded tasks (20/10/20/10/15/10/5/10) and Test 2 has three
coded functions plus six interpretation choices (20/30/20/30). The student notebooks, the Week 14 deck and
grader/rubrics/TEST1.json and TEST2.json agree with each other, so the published documents are brought into line.
Usage: python3 scripts/patch_test_rubrics_20261030.py"""
import copy, json, re
from pathlib import Path
import docx, openpyxl

ROOT = Path(__file__).resolve().parents[1]; B = ROOT / "IUEA_Teaching_Plan"
T1 = [("Read and inspect the raw data", 20, "Read the CSV with pandas into raw_data without changing it. Show the first and last rows, shape, row count, column type, info(), describe(), missing counts per column, the repeated record_id count and the invalid records."),
      ("Visualisation before cleaning", 10, "Scatter chart of load_pct against target from the raw data: correct points 4, title 2, horizontal label with % 2, vertical label with unit 2."),
      ("Clean the data", 20, "Keep the first row per record_id, remove rows with missing target or load_pct outside 0 to 100, fill missing ambient_c with the median of the retained rows. 4 marks for each correctly cleaned column."),
      ("Visualisation after cleaning", 10, "The same chart from the cleaned data, with the same four marking parts. No written comparison is required."),
      ("Calculate statistics", 15, "Mean, sum, median, count and sample standard deviation of target, and every most frequent equipment_id. Six answers at 2.5 marks each."),
      ("Group and aggregate", 10, "equipment_summary built with groupby and agg: mean and count of target for each equipment, 5 marks per column."),
      ("Reuse your statistics in one function", 5, "A function that returns the mean, sum and median of any column of any table, checked on other numbers."),
      ("Conditions and a loop", 10, "A for loop with if, elif and else counting loads as low (below 40), medium (40 to 75) or high (above 75): correct counts 6, loop 2, conditions 2.")]
T2 = [("Equipment-group split", 10, "group_split returns the train (E1 to E4), validation (E5) and test (E6) record_id lists in input order, without using target values. Week 10."),
      ("Baseline, linear and tree predictions", 15, "predict_regression fits a training-mean baseline, linear regression and a decision tree (max_depth 4, random_state 17) on load_pct and ambient_c, fits preprocessing on training rows only, and returns three prediction lists. Week 8."),
      ("MAE and RMSE", 5, "regression_errors returns mae and rmse over the same paired observations, unrounded. Week 8."),
      ("Classification and cost", 10, "classification_metrics returns tp, tn, fp, fn, precision, recall and cost (5 per missed warning plus 1 per false alarm), with zero for an undefined ratio. Week 9."),
      ("Group cross-validation", 10, "group_cv_mae holds out E1 to E5 in turn, fits a straight line on the other four groups and returns the five fold MAEs, their mean and their sample standard deviation. E6 is never used. Week 10."),
      ("Feature ablation", 10, "ablation_metrics compares a straight line on load_pct and ambient_c with one that adds load_pct times ambient_c, on the same validation records, and returns both MAEs and the improvement. Week 11."),
      ("Model selection", 10, "select_model keeps the candidates that meet the MAE and latency limits and picks the smallest validation MAE, then the smaller latency, then the name. Week 12."),
      ("Ridge and nearest neighbours", 15, "ridge_and_knn fits a degree-3 ridge curve on load_pct (alpha 1) and a 3-neighbour model on scaled load_pct and ambient_c, using training rows only, and returns both validation MAEs and which is better. Week 13."),
      ("Structured interpretation", 15, "Six scenario choices (A, B or C) on whole-group splits, training-only fill values, cost and threshold, the sealed test rows, choosing a ridge penalty and scaling for nearest neighbours. 2.5 marks each.")]
T1_DESC = ("Take-home Colab practical, 3 hours from the start. Eight coding tasks checked deterministically on other data with the same columns: "
           "reading and inspecting the file, charts before and after cleaning, cleaning, statistics, grouping, a function and a loop with conditions. "
           "No written report. AI assistance is not permitted.")
T2_DESC = ("Colab practical, 180 minutes, covering Weeks 8 to 13. Eight coding tasks (group split 10, baseline, linear and tree predictions 15, MAE and RMSE 5, classification and cost 10, "
           "group cross-validation 10, feature ablation 10, model selection 10, ridge and nearest neighbours 15) re-run by the lecturer's grader on unseen data, plus six interpretation choices (15). "
           "No separate written report. AI assistance is not permitted.")
MODE1, MODE2 = "Individual, timed Colab, 3h", "Individual, timed Colab, 3h"
CAL1 = "Practical Test 1 - Data Investigation (individual, timed Colab practical, 3 hours)."
CAL2 = "Practical Test 2 - End-to-End Engineering ML (individual, timed Colab practical, 3 hours)."


REPL = [
 ("The invigilated lab and approved-materials rules enforce that condition; being offline alone does not prevent a local assistant.",
  "Test 1 is a take-home practical followed by an understanding check, in which you may be asked to explain your code or change it without help. Test 2 follows the invigilator's rules. The grader re-runs your code on other data, so only code you can explain earns marks."),
 ("Why the tests are offline", "Why the tests are unaided"),
 ("Why the tests run offline", "Why the tests are unaided"),
 ("Follow the invigilated test brief and its approved-materials rules, including the prohibition on local as well as online AI assistance.",
  "Follow the test brief and its approved-materials rules, including the prohibition on AI assistance."),
 ("The room runs offline, which removes both internet search and AI assistance, and — this matters — is actually enforceable, unlike a rule against using an assistant on a networked machine.",
  "The tests run in Colab, so no setting can block an AI assistant. Integrity rests on matched variants, a grader that re-runs the submitted code on other data, a signed declaration and an understanding check in which a student may be asked to explain or change their own code."),
 ("Use is prohibited in both practical tests, which run offline.", "Use is prohibited in both practical tests, which run in Colab."),
 ("An invigilated lab and approved-materials rules support the unaided assessment. Offline access alone does not block a local AI model.",
  "Approved-materials rules, hidden-data grading and an understanding check support the unaided assessment. No setting in Colab blocks an AI assistant."),
 ("Pre-provision the offline environment for connectivity failures and the Week 7/14 tests.", "Pre-provision the offline environment for connectivity failures in teaching sessions."),
 ("Practical tests use the prepared offline environment; Colab teaching and Google Forms still require connectivity.", "The practical tests run in Colab and the submission form, so they need connectivity too."),
 ("Offline delivery reduces network communication but does not itself disable local AI tools; maintain invigilated no-AI conditions under Faculty arrangements.",
  "The tests run in Colab, which cannot block AI tools; rely on matched variants, hidden-data grading and the understanding check."),
 ("Collect the notebook and the individual typed Part B evidence with invigilator-controlled timestamps.", "Collect the notebook snapshot and the form confirmation with server timestamps."),
 ("Both practical tests prohibit AI and use invigilated offline arrangements; offline mode alone does not enforce that rule. Individual typed defence and Part B answers assess submitted explanations.",
  "Both practical tests prohibit AI. Test 1 is a take-home test with an understanding check and Test 2 follows the invigilator's rules. Only code a student can explain earns marks, because the grader re-runs it on other data."),
 ("Note that the Week 7 and Week 14 tests run offline on lab machines, so everyone meets a local environment at least once.", "Note that the Week 7 and Week 14 tests run in Colab, so students need no local setup for them."),
 ("mark schemes, offline bundle, auto-check script", "mark schemes, issued notebook bundle, auto-check script"),
 ("mark schemes, offline bundle", "mark schemes, issued notebook bundle"),
]


WEEK14 = {
 "struct": "• 0:00-0:15  Entry page, notebook and CSV downloaded, rules read aloud, identity cell checked.\n• 0:15-2:15  CODING (120 minutes). Individual, in Colab. Eight functions covering Weeks 8 to 13, from group_split to ridge_and_knn. The notebook states the columns, return formats and marks.\n• 2:15-2:40  INTERPRETATION AND CHECKING (25 minutes). Six scenario choices recorded in DECISIONS, then Restart and Run all.\n• 2:40-3:00  FINAL SAVE AND SUBMISSION (20 minutes). Submit test button, generated form link, confirmation. Week 15 demo running order confirmed.",
 "rules": "• Permitted: Colab, the submission form and any other resource the invigilator announces.\n• Prohibited: AI assistants, messaging and copied answers.\n• The notebook explains the columns and return formats, so the test examines judgement rather than memory of parameter names.",
 "prep": "• Author three parallel dataset variants of matched difficulty, each with a reference solution. The grader re-runs submitted code on unseen data.\n• Test the entry page, notebook download, Submit test button and form link with one account for each variant.\n• Confirm sittings, invigilators and Colab capacity with the Faculty. Cohort A is about 100 students.\n• Agree the moderation sample with the Faculty.\n• Prepare the Week 15 demo running order, two typed defence prompts and the digital submission check.",
 "res": "• A room with stable wifi and a Colab-capable laptop for every student; confirmed seat count; power contingency.\n• Entry links or QR codes for each variant.\n• Second invigilator for any sitting above 40 students.\n• Rubric published in Week 11.",
}
WEEK14_COLS = {"Master Plan (Shared Core)": dict(struct="E", rules="G", prep="N", res="O"),
               "Cohort A": dict(struct="J", rules="L", prep="T", res="U"), "Cohort B": dict(struct="J", rules="L", prep="T", res="U"), "Cohort C": dict(struct="J", rules="L", prep="T", res="U")}


WEEK7 = {
 "struct": "• 0:00-0:10  Entry link, private notebook and CSV, rules read aloud, identity cell checked.\n• 0:10-2:25  CODING (135 minutes). Individual, in Colab. Eight coded tasks: read and inspect the file, a chart before cleaning, cleaning, a chart after cleaning, statistics, grouping, one function, and a loop with conditions.\n• 2:25-2:40  CHECKING (15 minutes). Restart the session and Run all.\n• 2:40-3:00  FINAL SAVE AND SUBMISSION (20 minutes). Submit test button, generated form link, confirmation.",
 "rules": "• Permitted: Colab, pandas, matplotlib, ordinary Python, and your lecture slides, revision guide, cheatsheet and personal course notes.\n• Prohibited: AI tools, help from another person and copied work. Colab cannot block an AI assistant, so the rule rests on the declaration, hidden-data grading and an understanding check in which a student may be asked to explain or change their own code.\n• Rationale published to students in Week 6: AI is permitted and encouraged in projects, where the work is explained and defended; it is excluded from the two tests, which certify unaided capability.",
 "prep": "• Author three parallel dataset variants of matched difficulty, and the hidden data the grader uses.\n• Test the entry page, private notebook, countdown, Submit test button and form link with one account for each variant.\n• Confirm that every student has a Google account that works with Colab and the submission form.\n• The deterministic grader marks all eight tasks, so no structural auto-check script is needed.\n• Agree the moderation plan and the late and absent policy with the Faculty in advance.",
 "res": "• A Colab-capable laptop and a stable connection for every student.\n• An entry link or QR code for each variant.\n• Published rubric (issued Week 6).\n• A short understanding check for a sample of students after the test.",
}
WEEK7_COLS = {"Master Plan (Shared Core)": dict(struct="E", rules="G", prep="N", res="O"),
              "Cohort A": dict(struct="J", rules="L", prep="T", res="U"), "Cohort B": dict(struct="J", rules="L", prep="T", res="U"), "Cohort C": dict(struct="J", rules="L", prep="T", res="U")}
OFFLINE_REPL = [
 ("Rehearse the offline environment, public interfaces and saving both notebook and typed Part B before the test. Keep the official assessment timetable. Confirm lab readiness and the separate grading release checks.",
  "Rehearse the function interfaces, saving the notebook and submitting it before the test. Keep the official assessment timetable. Confirm that every student can sign in to Colab and the submission form, and keep the separate grading release checks."),
 ("Nobody leaves without knowing how they are assessed and that both tests are offline.", "Nobody leaves without knowing how they are assessed and that both tests run in Colab and are taken unaided."),
 ("The assessment slide has been shown and the offline-test rule stated.", "The assessment slide has been shown and the test rules stated."),
 ("Before offline tests, practise on the designated lab computer. No online sign-in, internet or AI is used during those tests; follow the invigilator's collection instructions.",
  "Both tests are taken in Colab with your own Google account. Before test day, practise opening Colab, uploading a CSV and submitting. No AI tools are used during the tests; follow the test brief."),
 ("Format, duration, rules, offline bundle, rubric, invigilation plan, auto-check script, moderation plan.", "Format, duration, rules, issued notebook bundle, rubric, moderation plan."),
 ("Format, duration, rules, offline bundle, rubric, invigilation, auto-check script, moderation.", "Format, duration, rules, issued notebook bundle, rubric, moderation."),
 ("SHARED: format, rules, duration, rubric, offline bundle.", "SHARED: format, rules, duration, rubric, issued notebook bundle."),
]


TEXT_BY_START = [
 ("• Independently investigate an unfamiliar engineering dataset", "• Read, inspect and clean an unfamiliar engineering dataset without a prescribed method, and check the result with charts.\n• Calculate summary statistics and group means with pandas and report them accurately.\n• Write a function that works on any table, and a loop with conditions.\n• Explain their own submitted code when asked, without AI or another person's help."),
 ("• Frame an unfamiliar engineering problem as a machine learning task", "• Split data by whole equipment groups and fit models on training rows only.\n• Compare a baseline, a straight line, a tree, a ridge curve and nearest neighbours on the same validation rows.\n• Count classification outcomes and work out a cost, and run cross-validation by group.\n• Test whether an extra input helps, and choose a model inside stated limits.\n• Explain the choices: sealed test rows, training-only fill values, scaling and the ridge penalty."),
 ("The test is the practical. Duration 2h00 practical + 0h25 written.", "The test is a coding practical in Colab, three hours from the start including setup, checking and submission. Three parallel dataset variants are issued by the entry page, and the deterministic grader re-runs the submitted code on other data."),
]


def setp(p, text):
    if not p.runs: p.add_run(text); return
    p.runs[0].text = text
    for r in p.runs[1:]: r.text = ""


def cell_set(c, text):
    setp(c.paragraphs[0], text)
    for p in c.paragraphs[1:]: setp(p, "")


def fix_text(s):
    s = s.replace("(individual, offline, 2h25)", "(individual, timed Colab practical, 3 hours)").replace("(individual, offline)", "(individual, timed Colab practical)")
    s = s.replace("Practical Test 2 written section", "Practical Test 2 interpretation questions")
    for a, b in REPL + OFFLINE_REPL: s = s.replace(a, b)
    s = s.replace("Individual, offline, 2h25", "Individual, timed Colab, 3h").replace("Individual, offline", "Individual, timed Colab")
    return s


def plan_content():
    p = ROOT / "scripts" / "plan_content.py"; s = p.read_text()
    cut = s.find("\n\n# Practical Tests 1 and 2 are the coding tests")
    if cut >= 0: s = s[:cut]
    s += ("\n\n# Practical Tests 1 and 2 are the coding tests that were built, sat and graded (see grader/rubrics/TEST1.json, TEST2.json\n"
          "# and patch_test_rubrics_20261030.py). The descriptions here are short; the exact task wording lives in the notebooks.\n"
          "_grader_checked_tests = True\n"
          'RUBRICS["Practical Test 1 - Data Investigation (15%)"] = ' + repr(T1) + "\n"
          'RUBRICS["Practical Test 2 - End-to-End Engineering ML (20%)"] = ' + repr(T2) + "\n")
    p.write_text(s)


def xlsx():
    f = B / "IUEA_ML_Semester1_Master_Teaching_Plan.xlsx"; wb = openpyxl.load_workbook(f)
    ws = wb["Rubrics"]
    r_da = next(r for r in range(1, ws.max_row + 1) if ws.cell(r, 1).value == "Data Analysis Project (10%)")
    want_da = 31 + len(T2); shift = want_da - r_da
    # style templates from the first Test 1 block (rows 15, 16, 17, 25 and the blank row after the total)
    def snap(r): return [copy.copy(ws.cell(r, c)._style) for c in range(1, 6)], ws.row_dimensions[r].height
    st_title, st_head, st_row, st_blank = snap(15), snap(16), snap(17), snap(26)
    st_tot = snap(25)
    if shift:
        merges = [str(m) for m in ws.merged_cells.ranges]
        low = [m for m in merges if openpyxl.utils.cell.range_boundaries(m)[1] >= r_da]
        for m in low: ws.unmerge_cells(m)
        heights = {r: ws.row_dimensions[r].height for r in range(r_da, ws.max_row + 1)}
        top = ws.max_row
        ws.move_range(f"A{r_da}:E{top}", rows=shift, translate=True)
        for r, h in heights.items(): ws.row_dimensions[r + shift].height = h
        for m in low:
            c1, r1, c2, r2 = openpyxl.utils.cell.range_boundaries(m)
            ws.merge_cells(start_row=r1 + shift, end_row=r2 + shift, start_column=c1, end_column=c2)
    for mr in [str(m) for m in ws.merged_cells.ranges if openpyxl.utils.cell.range_boundaries(str(m))[1] in (15, 25, 27)]: ws.unmerge_cells(mr)
    def put(r, vals, st):
        for c in range(1, 6):
            ws.cell(r, c).value = vals[c - 1] if c - 1 < len(vals) else None; ws.cell(r, c)._style = copy.copy(st[0][c - 1])
        if st[1]: ws.row_dimensions[r].height = st[1]
    r = 15; put(r, ["Practical Test 1 - Data Investigation (15%)"], st_title); ws.merge_cells("A15:D15"); r += 1
    put(r, ["Criterion", "Marks", "What earns the marks", "Marker note"], st_head); r += 1
    first = r
    for t, m, d in T1: put(r, [t, m, d, None], st_row); r += 1
    put(r, ["TOTAL", f"=SUM(B{first}:B{r-1})"], st_tot); r += 1
    put(r, [], st_blank); r += 1
    put(r, ["Practical Test 2 - End-to-End Engineering ML (20%)"], st_title); ws.merge_cells(f"A{r}:D{r}"); r += 1
    put(r, ["Criterion", "Marks", "What earns the marks", "Marker note"], st_head); r += 1
    first = r
    for t, m, d in T2: put(r, [t, m, d, None], st_row); r += 1
    put(r, ["TOTAL", f"=SUM(B{first}:B{r-1})"], st_tot); r += 1
    put(r, [], st_blank); r += 1
    assert r == want_da, (r, want_da)
    for sh in wb:
        for row in sh.iter_rows():
            for c in row:
                v = c.value
                if isinstance(v, str) and sh.title != "Rubrics":
                    n = fix_text(v)
                    n = re.sub(r"(PRACTICAL TEST 1 = 15% of the Semester 1 mark\. Individual\. )Rubric: [^\n]*", r"\1Rubric: reading and inspecting 20, chart before cleaning 10, cleaning 20, chart after cleaning 10, statistics 15, grouping 10, one function 5, conditions and a loop 10.", n)
                    n = re.sub(r"(PRACTICAL TEST 2 = 20% of the Semester 1 mark\. Individual\. )Rubric: [^\n]*", r"\1Rubric: group split 10, baseline, linear and tree predictions 15, MAE and RMSE 5, classification and cost 10, group cross-validation 10, feature ablation 10, model selection 10, ridge and nearest neighbours 15, six interpretation choices 15.", n)
                    if n != v: c.value = n
    for sh, cols in WEEK14_COLS.items():
        for k, col in cols.items():
            c = wb[sh][f"{col}18"]
            if isinstance(c.value, str): c.value = WEEK14[k]
    for sh, cols in WEEK7_COLS.items():
        for k, col in cols.items():
            c = wb[sh][f"{col}11"]
            if isinstance(c.value, str): c.value = WEEK7[k]
    for sh in wb:
        if sh.title in ("Master Plan (Shared Core)", "Cohort A", "Cohort B", "Cohort C"):
            for row in (11, 18):
                for c in sh[row]:
                    if isinstance(c.value, str):
                        for start, new_text in TEXT_BY_START:
                            if c.value.startswith(start): c.value = new_text if not (row == 18 and start.startswith("The test is")) else new_text
    a = wb["Assessment"]
    a["C9"], a["C10"] = MODE1, MODE2
    a["E9"] = T1_DESC; a["E10"] = T2_DESC
    a["F9"] = "Test 1 rubric (see Rubrics sheet). Eight coded tasks, 100 marks, all checked deterministically on other data."
    a["F10"] = "Test 2 rubric (see Rubrics sheet). Eight coded functions (85 marks) and six interpretation choices (15 marks), checked deterministically."
    wb.save(f)


def docs():
    for name in ("IUEA_ML_Syllabus_CohortA_Design_and_Infrastructure", "IUEA_ML_Syllabus_CohortB_Mining_and_Petroleum", "IUEA_ML_Syllabus_CohortC_Engineering", "IUEA_ML_Semester1_Master_Teaching_Plan", "IUEA_ML_Lecturer_Teaching_Guide_W1-W15", "IUEA_ML_Beginner_Teaching_Quick_Guide", "IUEA_ML_Week1_PreFlight_Checklist", "IUEA_ML_Student_Setup_Guide"):
        f = B / f"{name}.docx"; d = docx.Document(f)
        def walk():
            for p in d.paragraphs: yield p
            for t in d.tables:
                for r in t.rows:
                    for c in r.cells:
                        for p in c.paragraphs: yield p
        for p in walk():
            n = fix_text(p.text)
            if n != p.text: setp(p, n)
        for t in d.tables:
            for r in t.rows:
                k = r.cells[0].text.strip()
                if k.startswith("Practical Test 1 — Data Investigation") and len(r.cells) >= 5: cell_set(r.cells[4], T1_DESC)
                if k.startswith("Practical Test 2 — End-to-End ML") and len(r.cells) >= 5: cell_set(r.cells[4], T2_DESC)
        if name == "IUEA_ML_Semester1_Master_Teaching_Plan":
            for p in d.paragraphs:
                if p.text.startswith("The first assessment week certifies data literacy"):
                    setp(p, "The first assessment week certifies data literacy, not modelling. Each student works alone in Colab for three hours on their own assigned dataset from their own domain. Eight coding tasks cover reading and inspecting the file, a chart before cleaning, cleaning with stated rules, a chart after cleaning, statistics, grouping and aggregation, one reusable function, and a loop with conditions. The grader runs the submitted code on other data with the same columns, so stored outputs earn nothing. There is no written report, and the test totals 100 marks.")
                if p.text.startswith("Week 14 is the second practical test"):
                    setp(p, "Week 14 is the second practical test, taken individually in Colab in three hours, and it reaches back over Weeks 8 to 13. Students write eight functions: a split by whole equipment groups, predictions from a baseline, a linear model and a decision tree, MAE and RMSE, classification counts with a cost, cross-validation by equipment group, a feature ablation, a choice between candidate models under two limits, and a ridge curve compared with nearest neighbours. They then answer six interpretation choices on splits, fill values, cost and threshold, the sealed test rows, the ridge penalty and scaling. The grader re-runs the code on unseen data. There are three matched variants of the dataset and no separate written report.")
        if name == "IUEA_ML_Lecturer_Teaching_Guide_W1-W15":
            for p in d.paragraphs:
                t = p.text
                if t.startswith("Slide 1 · Individual · offline"): setp(p, "Slide 1 · Individual · Colab practical · three hours")
                elif t.startswith("read the rules aloud from slide 4") and "no network" in t: setp(p, "read the rules aloud from slide 4 rather than paraphrasing. Students open their private notebook from the entry link and need a working connection and their Google account. Distribute the three dataset variants in a checkerboard pattern before anyone sits down.")
                elif t.startswith("issue this deck in Week 13"): setp(p, "issue this deck in Week 13. On the day, read the rules slide aloud from the screen and confirm that every student can open their entry link and Colab before the test window opens. The three dataset variants are assigned by the entry page.")
                elif t.startswith("read this slide aloud from the screen at the start. Then confirm every machine"): setp(p, "read this slide aloud from the screen at the start. Then confirm that every student has signed in with the same Google account they registered, and that the entry page shows their notebook and CSV.")
        d.save(f)


if __name__ == "__main__":
    plan_content(); xlsx(); docs(); print("done")
