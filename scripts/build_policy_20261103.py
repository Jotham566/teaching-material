"""Write data/assessment_blocks_20261103.json from data/assessment_blocks_20261102.json (idempotent; never edits the 2 Nov file).

Decision of the lecturer, 3 November 2026: there is NO demo. The Engineering ML project stays, but students SUBMIT it
(take-home, graded like Practical Test 1) and it covers only Weeks 1 to 11. Semester 1 results can be published before
the project is marked, with the project shown as PENDING.
New weights (sum 100): quizzes 15, assignments 15, data analysis project 10, Practical Test 1 15, Engineering ML project 45
(Part A the coded notebook 30, auto-graded plus rubric like Test 1; Part B a one-page decision memo 15, rubric).
Blocks, closing times, quiz sittings, the best-of rules, the 35 and 160 totals are copied unchanged from the 2 Nov file.
Usage: python3 scripts/build_policy_20261103.py"""
import json, copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD = json.loads((ROOT / "data" / "assessment_blocks_20261102.json").read_text())
COHORTS = ("CML3111", "CML3112", "CML3113")
TBC = "proposed, lecturer to confirm"

p = copy.deepcopy(OLD)
class4 = {c: OLD["calendar"]["class_dates"][c]["4"] for c in COHORTS}
clinic = OLD["calendar"]["week_12_demo"]["dates"]

# ---- header
p["effective_from"] = "3 November 2026 (lecturer decision). Block dates, closing times and quiz sittings are exactly those of the 2 November arrangement."
p["supersedes"] = "data/assessment_blocks_20261102.json"
p["decided"] = "2026-11-03"
p["decision"] = (
    "There is no demo. Practical Test 2 stays removed. The Engineering ML project stays but students SUBMIT it: it is a take-home, "
    "graded like Practical Test 1, and it covers only what was taught this semester (Weeks 1 to 11). Semester 1 results can be published "
    "BEFORE the project is marked, with the project shown as PENDING. Teaching is four classes (Weeks 8 to 11 content) in two blocks; "
    "Week 12 is a project clinic (supervised work and questions, no demo). Weeks 1 to 5 stay weekly (best 3 of 5, Week 6 waived). "
    "The quizzes, assignments, blocks, deadlines and quiz sittings are unchanged from 2 November 2026.")

# ---- calendar: Week 12 is a clinic, not a demo
cal = p["calendar"]
del cal["week_12_demo"]
cal["week_12_project_clinic"] = {
    "dates": clinic,
    "dates_status": "Same Week 12 class dates as before (CML3112 Tue 1 Dec, CML3113 and CML3111 Fri 4 Dec).",
    "what": "Project clinic: supervised work on the project, and questions. No demo and no presentation.",
    "marks": "none; the clinic carries no marks",
    "time_and_room": "to be confirmed by the lecturer"}
cal["semester_ends"] = "Week 12 (project clinic). The project itself is due on the proposed date below."
cal["retired_events"] = OLD["calendar"]["retired_events"] + ["Week 12 short project demo (retired 3 November 2026: there is no demo)"]

# ---- the project
due = "2026-12-11T23:59:00+03:00"
p["engineering_ml_project"] = {
    "what": "Take-home project, submitted by the student and graded like Practical Test 1. One submission with two parts.",
    "scope": "Only what was taught this semester, Weeks 1 to 11 (Classes 1 to 4 of the second half included).",
    "marks": 45,
    "parts": [
        {"part": "A", "id": "ML_PROJECT_A", "gradebook_column": "ML Project Part A", "title": "Coded project notebook", "marks": 30,
         "marking": "Auto-graded checks plus a rubric, as for Practical Test 1. The split between automatic checks and rubric marks is to be confirmed by the lecturer."},
        {"part": "B", "id": "ML_PROJECT_B", "gradebook_column": "ML Project Part B", "title": "One-page decision memo", "marks": 15,
         "marking": "Rubric."}],
    "submission_key": "ML_PROJECT",
    "submission_formats": ["ipynb", "pdf", "docx"],
    "hand_in": "to be confirmed by the lecturer: one notebook with the memo written inside it, handed in like Practical Test 1, or a notebook plus a separate memo file (PDF or DOCX). The draft project in IUEA_Teaching_Plan/second_half/Project builds the first of these.",
    "submission_note": "ML_PROJECT stays the single project submission in data/assessments.json, with two parts. No form window is opened by this decision: opens_at and closes_at stay null until the lecturer sets them.",
    "released": {
        "rule": "After Class 4 (Week 11 content)",
        "dates": class4,
        "status": TBC},
    "due": {
        "all_cohorts": due,
        "text": "Friday 11 December 2026, 23:59 Kampala, for all three cohorts",
        "status": TBC},
    "team_or_individual": "to be confirmed by the lecturer",
    "rubric_and_marks_detail": "to be confirmed by the lecturer and published before the project is released"}

# ---- weights (sum 100); demonstration removed
p["weights_percent"] = {"quizzes": 15, "assignments": 15, "data_analysis_project": 10, "practical_test_1": 15, "engineering_ml_project": 45}
assert sum(p["weights_percent"].values()) == 100
p["weights_status"] = "Decided by the lecturer on 3 November 2026. Still to be checked against IUEA regulations."
p["demonstration"] = {"status": "REMOVED on 3 November 2026", "note": "There is no demo and no demonstration component. The DEMO row in data/assessments.json is retired."}

# ---- provisional mode (gradebook.gs and continuous_assessment.py implement this; tests keep them in step)
marked = ["quizzes", "assignments", "data_analysis_project", "practical_test_1"]
p["provisional_mode"] = {
    "purpose": "Semester 1 results can be published before the project is marked.",
    "components_marked_for_provisional": marked,
    "provisional_weight_total": sum(p["weights_percent"][k] for k in marked),
    "pending_components": ["engineering_ml_project"],
    "gradebook_columns": {"project_part_a": "ML Project Part A", "project_part_b": "ML Project Part B",
                          "provisional_text": "Semester 1 provisional", "project_status": "Project", "final": "Final %", "band": "Band"},
    "provisional_text": "Semester 1 provisional: {x} of 55 marks, {y} percent",
    "project_status_text": {"pending": "Project: PENDING", "marked": "Project: marked"},
    "project_is_pending_when": "either project column is blank. A blank is unmarked; a typed 0 is a mark of zero.",
    "project_is_marked_when": "both ML Project Part A and ML Project Part B hold a number. Enter 0 for a student who submitted nothing once marking is finished.",
    "while_pending": "Final % and Band are blank. The sheet shows the provisional line and 'Project: PENDING'. A final percentage or grade band is never shown that treats an unmarked project as zero.",
    "once_marked": "Final % is the full total out of 100: quizzes + assignments + data analysis project + Practical Test 1 + project Part A + Part B. The provisional line is cleared.",
    "not_pending": "A student with a missing quiz or assignment part still scores zero for it. A blank data analysis project or Practical Test 1 also counts as zero and is listed under Missing. Only the project can be pending.",
    "x": "marks earned over the four marked components, out of 55 (the weighted points, 15 + 15 + 10 + 15)",
    "y": "x divided by 55, times 100, rounded half up to two places"}

# ---- coursework rule unchanged; record what changed
p["unchanged"] = OLD["unchanged"] + [
    "Quizzes: weekly Q1 to Q5 best 3 of 5, plus Block 1 (Q7 + Q8) and Block 2 (Q9 + Q10); out of 35; 15 percent",
    "Assignments: weekly A1 to A5 best 3 of 5, plus Block 1 (A7 + A8) and Block 2 (A9 + A10 + A11); out of 160; 15 percent",
    "All block dates, assignment closing times and quiz sittings of 2 November 2026"]
p["changed"] = [
    "Demonstration removed everywhere (weight 15 gone).",
    "Engineering ML Project: weight 30 to 45. It is a take-home submission, not a demo. Part A coded notebook 30 (auto-graded plus rubric), Part B one-page decision memo 15 (rubric). Covers Weeks 1 to 11 only.",
    "Week 12 is a project clinic (supervised work and questions, no demo).",
    "Project released after Class 4; proposed due date Friday 11 December 2026 23:59 Kampala for all cohorts (proposed, lecturer to confirm).",
    "Semester 1 results can be published before the project is marked: provisional line out of 55 plus 'Project: PENDING'."]
p["retired_assessments"] = OLD["retired_assessments"][:3] + [
    "Demonstration and the Week 12 short project demo (retired 3 November 2026)"]
p["open_items"] = [
    "Whether the project is done individually or in teams, the split of Part A between automatic checks and rubric, and the Part A and Part B rubrics: to be confirmed by the lecturer.",
    "Release date (after Class 4) and due date (Friday 11 December 2026 23:59 Kampala): proposed, lecturer to confirm. No form window is opened until the lecturer sets one.",
    "The Week 11 quiz form (Q10) must be replaced in place with replaceWeek11Questions() before the Class 4 sitting. See Block_Assessment_Arrangement_2026-11-02.md.",
    "Weights need checking against IUEA regulations.",
    "Grade bands are still a placeholder in gradebook.gs (GRADE_BANDS_VERIFIED is false)."]

out = ROOT / "data" / "assessment_blocks_20261103.json"
text = json.dumps(p, indent=2, ensure_ascii=False) + "\n"
if not out.exists() or out.read_text() != text:
    out.write_text(text)
print("wrote", out.name)
