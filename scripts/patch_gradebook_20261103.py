"""Patch grader/gradebook.gs for the decision of 3 November 2026 (data/assessment_blocks_20261103.json).
SUPERSEDED 10 November 2026 (data/assessment_policy_20261110.json): gradebook.gs was then edited by hand and now carries the marker
GRADEBOOK_POLICY_20261110; this script refuses to touch such a file. Kept as the record of the 3 November change.

  * no demo; Engineering ML project = Part A (/30) + Part B (/15) in two columns, weight 45;
  * PROVISIONAL mode: until both project columns hold a mark the sheet shows 'Semester 1 provisional: x of 55 marks, y percent'
    and 'Project: PENDING', and Final % and Band stay blank. Once marked, the full total out of 100;
  * prepareGradesColumns() adds the four new columns to the live sheet (never deletes or overwrites anything);
  * importMarkedResults() accepts 'ML Project Part A' (maximum 30) and 'ML Project Part B' (maximum 15) and no longer 'ML Project' or 'Demo'.
Backs the file up first (first copy wins). Every replacement asserts its match count. The result is pure ASCII.
Idempotent: a file that already carries the marker is left alone.
Usage: python3 scripts/patch_gradebook_20261103.py"""
import re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from backup_20261103 import backup

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "IUEA_Teaching_Plan" / "grader" / "gradebook.gs"
MARK = "GRADEBOOK_PATCH_20261103"


def rep(text, old, new, count=1):
    n = text.count(old)
    assert n == count, f"expected {count} match(es), found {n}: {old[:70]!r}"
    return text.replace(old, new)


def between(text, start, end, new, include_end=False):
    """Replace text from `start` up to (not including) `end` with `new`; both markers must occur exactly once."""
    assert text.count(start) == 1, f"start marker count {text.count(start)}: {start[:60]!r}"
    i = text.index(start)
    assert text.count(end, i + len(start)) >= 1, f"end marker missing: {end[:60]!r}"
    j = text.index(end, i + len(start))
    assert text.count(end) == 1 or True
    return text[:i] + new + text[j:]


HEADER = r''' * Revised 3 November 2026 (data/assessment_blocks_20261103.json). There is NO demo and no Practical Test 2.
 * The Engineering ML project stays: students SUBMIT it (take-home, graded like Practical Test 1) and it covers Weeks 1 to 11.
 *
 *   Quizzes                    15 %   Weeks 1-5 weekly (best 3 of 5, Week 6 waived, each out of 5), then
 *                                     Block 1 (Q7+Q8, out of 10) and Block 2 (Q9+Q10, out of 10).
 *                                     Total 3x5 + 10 + 10 = 35 marks. Q11 and Q12 are retired.
 *   Assignments                15 %   Weeks 1-5 weekly (best 3 of 5, each out of 20), then
 *                                     Block 1 (A7+A8, out of 40) and Block 2 (A9+A10+A11, out of 60).
 *                                     Total 3x20 + 40 + 60 = 160 marks.
 *   Data Analysis Project      10 %   out of 100
 *   Practical Test 1           15 %   out of 100
 *   Engineering ML Project     45 %   Part A coded project notebook /30 (auto-graded plus rubric, like Test 1)
 *                                     + Part B one-page decision memo /15 (rubric). Two columns.
 *                             ----
 *                             100 %
 *
 * PROVISIONAL MODE. Semester 1 results can be published before the project is marked. While either project column
 * (ML Project Part A, ML Project Part B) is blank the sheet shows "Semester 1 provisional: x of 55 marks, y percent"
 * (quizzes, assignments, data analysis project and Test 1; 15 + 15 + 10 + 15 = 55) and "Project: PENDING". Final % and
 * Band stay blank: an unmarked project is never counted as zero. Once BOTH columns hold a number (type 0 for a student
 * who submitted nothing) the sheet shows the full total out of 100. A missing quiz or assignment part still scores zero.
'''

CONFIG = r'''var WEIGHTS = {
  quizzes: 15,
  challenges: 15,
  dataProject: 10,
  test1: 15,
  mlProject: 45          // Part A (coded notebook, /30) + Part B (decision memo, /15). There is no demo component.
};

var ML_PART_A_MAX = 30;        // marks for the coded project notebook (auto-graded plus rubric, like Practical Test 1)
var ML_PART_B_MAX = 15;        // marks for the one-page decision memo (rubric)
var PROJECT_INPUT_HEADERS = ["ML Project Part A", "ML Project Part B"];
var PROVISIONAL_HEADER = "Semester 1 provisional";
var PROJECT_STATUS_HEADER = "Project";
var PROJECT_PENDING_TEXT = "Project: PENDING";
var PROJECT_MARKED_TEXT = "Project: marked";

'''

PURE = r'''/** A cell with nothing in it. A typed 0 is NOT blank: it is a mark of zero. */
function isBlankMark_(v) {
  return v === "" || v === null || v === undefined || (typeof v === "string" && v.replace(/\s/g, "") === "");
}

/**
 * The Engineering ML project: Part A (/30) and Part B (/15) are entered as two columns.
 * It counts only when BOTH parts hold a number. If either is blank the project is PENDING: it is not zero, and the
 * gradebook then shows a provisional result instead of a final one. Out-of-range or text marks are rejected loudly.
 */
function projectComponent_(partA, partB) {
  validateMark_(partA, ML_PART_A_MAX);
  validateMark_(partB, ML_PART_B_MAX);
  var aBlank = isBlankMark_(partA), bBlank = isBlankMark_(partB);
  var marked = !aBlank && !bBlank;
  var a = aBlank ? null : Number(partA), b = bBlank ? null : Number(partB);
  var outOfParts = ML_PART_A_MAX + ML_PART_B_MAX;
  return {
    outOf: WEIGHTS.mlProject,
    marked: marked,
    pending: !marked,
    partA: a,
    partB: b,
    partAMarked: !aBlank,
    partBMarked: !bBlank,
    raw: marked ? a + b : null,
    rawOutOf: outOfParts,
    weighted: marked ? round2_((a + b) / outOfParts * WEIGHTS.mlProject) : 0
  };
}

/** Weight of the components that are marked before the project: quizzes + assignments + data analysis project + Test 1 = 55. */
function provisionalOutOf_() {
  return WEIGHTS.quizzes + WEIGHTS.challenges + WEIGHTS.dataProject + WEIGHTS.test1;
}

function fmt2_(x) { return Number(x).toFixed(2); }

'''

COMPUTE = r'''function computeFinal_(row) {
  var policy=courseworkPolicy_(row.cohort);
  var cp = blockComponent_(row.quizzes, QUIZ_MAX, WEIGHTS.quizzes, policy, COURSEWORK_BLOCKS.quizzes);
  var ch = blockComponent_(row.challenges, CHALLENGE_MAX, WEIGHTS.challenges, policy, COURSEWORK_BLOCKS.challenges);
  var dp = percentComponent_(row.dataProject, 100, WEIGHTS.dataProject);
  var t1 = percentComponent_(row.test1, 100, WEIGHTS.test1);
  var pr = projectComponent_(row.mlProjectA, row.mlProjectB);

  // A missing quiz or assignment part, data analysis project or Test 1 scores zero and is listed here.
  // The project is different: unmarked means PENDING, which is not a missing mark and is not listed here.
  var missing = [];
  if (dp.missing) { missing.push("Data Analysis Project"); }
  if (t1.missing) { missing.push("Practical Test 1"); }
  if (cp.submitted < policy.weeklyBest) {
    missing.push("weekly quizzes (Weeks 1-6): " + cp.submitted + " of " + policy.weeklyBest + " that count");
  }
  if (ch.submitted < policy.weeklyBest) {
    missing.push("weekly assignments (Weeks 1-6): " + ch.submitted + " of " + policy.weeklyBest + " that count");
  }
  cp.blocks.forEach(function (b) { if (b.parts === 0) { missing.push(b.id + " quiz"); } });
  ch.blocks.forEach(function (b) { if (b.parts === 0) { missing.push(b.id + " assignment"); } });

  // Provisional result: the four components that are marked before the project, out of 55.
  var provMarks = round2_(cp.weighted + ch.weighted + dp.weighted + t1.weighted);
  var provOut = provisionalOutOf_();
  var provPercent = round2_(provMarks / provOut * 100);
  var provisional = {
    marks: provMarks,
    outOf: provOut,
    percent: provPercent,
    text: "Semester 1 provisional: " + fmt2_(provMarks) + " of " + provOut + " marks, " + fmt2_(provPercent) + " percent"
  };

  // Final result: only when the project is marked. Never a final figure or band that counts an unmarked project as zero.
  var final = pr.pending ? null : round2_(cp.weighted + ch.weighted + dp.weighted + t1.weighted + pr.weighted);
  return {
    components: { quizzes: cp, challenges: ch, dataProject: dp,
                  test1: t1, mlProject: pr },
    final: final,
    band: pr.pending ? null : gradeBand_(final),
    projectPending: pr.pending,
    projectStatus: pr.pending ? PROJECT_PENDING_TEXT : PROJECT_MARKED_TEXT,
    provisional: provisional,
    missing: missing
  };
}

'''

PROGRESS_TAIL_OLD = '''  lines.push("Marks banked so far: " + res.final + " of 100.");
'''
PROGRESS_TAIL_NEW = '''  var pj = res.components.mlProject;
  if (res.projectPending) {
    lines.push(res.provisional.text + ".");
    lines.push(PROJECT_PENDING_TEXT + ". The Engineering ML project is worth " + WEIGHTS.mlProject + " marks and is not marked yet" +
               (pj.partAMarked ? " (Part A is marked, Part B is not)" : (pj.partBMarked ? " (Part B is marked, Part A is not)" : "")) +
               ". Your final total, out of 100, appears when it is marked.");
  } else {
    lines.push("Marks banked: " + res.final + " of 100 (the project is marked).");
  }
'''

PREPARE = r'''/** Headers from `wanted` that the sheet's header row does not have yet (same loose matching as columnIndexByHeader_). */
function missingHeaders_(headers, wanted) {
  return wanted.filter(function (h) { return columnIndexByHeader_(headers, h) < 0; });
}

/**
 * Run once after pasting this file. Adds any of "ML Project Part A", "ML Project Part B", "Semester 1 provisional" and
 * "Project" that the Grades sheet does not have, to the right of the existing columns. It never deletes, moves or
 * overwrites anything: the old "ML Project" and "Demo" columns stay where they are and are ignored.
 */
function prepareGradesColumns() {
  var sh = SpreadsheetApp.getActive().getSheetByName(GRADER_SHEET);
  if (!sh) { throw new Error("No sheet called '" + GRADER_SHEET + "'."); }
  var width = sh.getLastColumn();
  var headers = sh.getRange(1, 1, 1, width).getValues()[0];
  var add = missingHeaders_(headers, PROJECT_INPUT_HEADERS.concat([PROVISIONAL_HEADER, PROJECT_STATUS_HEADER]));
  if (!add.length) {
    SpreadsheetApp.getActive().toast("All four project columns are already there.");
    return;
  }
  sh.getRange(1, width + 1, 1, add.length).setValues([add]);
  SpreadsheetApp.getActive().toast("Added columns: " + add.join(", "));
}

'''

RECORD = '''    mlProjectA: get("ML Project Part A"),
    mlProjectB: get("ML Project Part B")
  };
}
'''

RECOMPUTE = r'''function recomputeAll() {
  var g = readGradesSheet_();
  var iFinal = columnIndexByHeader_(g.headers, "Final %");
  var iBand = columnIndexByHeader_(g.headers, "Band");
  var iMiss = columnIndexByHeader_(g.headers, "Missing");
  var iDone = columnIndexByHeader_(g.headers, "Challenges done");
  var iProv = columnIndexByHeader_(g.headers, PROVISIONAL_HEADER);
  var iProj = columnIndexByHeader_(g.headers, PROJECT_STATUS_HEADER);
  if (iFinal < 0) {
    throw new Error("Add a column headed 'Final %' to the Grades sheet.");
  }
  if (iProv < 0 || iProj < 0) {
    throw new Error("The Grades sheet has no '" + PROVISIONAL_HEADER + "' or '" + PROJECT_STATUS_HEADER + "' column. Run prepareGradesColumns() once, then run this again.");
  }
  var out = [];
  for (var r = 0; r < g.rows.length; r++) {
    var rec = rowToRecord_(g.headers, g.rows[r]);
    if (!rec.studentId) { out.push(null); continue; }
    var res = computeFinal_(rec);
    var line = g.rows[r].slice();
    // Provisional: no final percentage and no band, because the project is not marked. Never an unmarked project as zero.
    line[iFinal] = res.final === null ? "" : res.final;
    if (iBand >= 0) { line[iBand] = res.projectPending ? "No band yet" : (GRADE_BANDS_VERIFIED ? res.band : 'Awaiting Faculty bands'); }
    line[iProv] = res.projectPending ? res.provisional.text : "";
    line[iProj] = res.projectStatus;
    if (iMiss >= 0) { line[iMiss] = res.missing.join("; "); }
    if (iDone >= 0) { line[iDone] = res.components.challenges.submitted; }
    out.push(line);
  }
'''

IMPORT_OLD = '''  // Practical Test 2 was dropped on 2 November 2026; its column is no longer an import target.
  var allowed=CHALLENGE_IDS.concat(['Data Analysis Project','Practical Test 1','ML Project','Demo']);
'''
IMPORT_NEW = '''  // Practical Test 2 was dropped on 2 November 2026 and the demo on 3 November 2026; their columns are no longer import targets.
  var allowed=CHALLENGE_IDS.concat(['Data Analysis Project','Practical Test 1'],PROJECT_INPUT_HEADERS);
'''

MAXFN = r'''/** The maximum a column's marks can have: 20 for an assignment part, 30 and 15 for the two project parts, 100 otherwise. */
function markColumnMax_(columnName) {
  if (CHALLENGE_IDS.indexOf(columnName) >= 0) { return CHALLENGE_MAX; }
  if (columnName === PROJECT_INPUT_HEADERS[0]) { return ML_PART_A_MAX; }
  if (columnName === PROJECT_INPUT_HEADERS[1]) { return ML_PART_B_MAX; }
  return 100;
}

'''

TESTS_WEIGHTS = r'''  // ---- weights ----
  eq("weights total 100", weightTotal_(), 100);
  eq("weights are the 3 November 2026 weights", WEIGHTS, {quizzes: 15, challenges: 15, dataProject: 10, test1: 15, mlProject: 45});
  ok("Practical Test 2 has no weight", !WEIGHTS.hasOwnProperty("test2"));
  ok("the demonstration has no weight", !WEIGHTS.hasOwnProperty("demo"));
  eq("project parts add up to the project weight", ML_PART_A_MAX + ML_PART_B_MAX, WEIGHTS.mlProject);
  eq("the provisional components weigh 55", provisionalOutOf_(), 55);
  eq("provisional plus project is 100", provisionalOutOf_() + WEIGHTS.mlProject, 100);

'''

TESTS_FINAL = r'''  // ---- project component ----
  var pc0 = projectComponent_("", "");
  ok("both project parts blank: pending, not zero", pc0.pending && !pc0.marked && pc0.weighted === 0 && pc0.raw === null);
  var pcA = projectComponent_(24, "");
  ok("only Part A: still pending", pcA.pending && pcA.partAMarked && !pcA.partBMarked && pcA.weighted === 0);
  var pcB = projectComponent_(null, 9);
  ok("only Part B: still pending", pcB.pending && !pcB.partAMarked && pcB.partBMarked);
  var pcAB = projectComponent_(24, 9);
  ok("both parts: marked", pcAB.marked && !pcAB.pending);
  near("both parts: 33 of 45 is 33 of the 45 marks", pcAB.weighted, 33);
  var pcZero = projectComponent_(0, 0);
  ok("typed zeros are a mark of zero, not pending", pcZero.marked && pcZero.weighted === 0);
  ok("a space is blank", projectComponent_(" ", " ").pending);
  var rejected = 0;
  [[31, 0], [0, 16], [-1, 0], ["absent", 0], [0, "x"]].forEach(function (p) { try { projectComponent_(p[0], p[1]); } catch (e) { rejected++; } });
  eq("project marks above the maximum, negative or text are rejected", rejected, 5);

  // ---- computeFinal_ ----
  var ALL5 = [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, "", ""];
  var ALL20 = [20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20];
  var perfect = computeFinal_({
    quizzes: ALL5, challenges: ALL20,
    dataProject: 100, test1: 100, mlProjectA: 30, mlProjectB: 15
  });
  near("perfect student with the project marked -> 100", perfect.final, 100);
  eq("perfect student has nothing missing", perfect.missing, []);
  eq("perfect student's project is not pending", perfect.projectPending, false);
  eq("perfect student's status line", perfect.projectStatus, "Project: marked");
  eq("perfect student gets a band", perfect.band, "A");
  var half = computeFinal_({
    quizzes: [2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, "", ""],
    challenges: [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
    dataProject: 50, test1: 50, mlProjectA: 15, mlProjectB: 7.5
  });
  near("half marks everywhere -> 50", half.final, 50);

  // PROVISIONAL, no project at all
  var provNoProject = computeFinal_({
    quizzes: ALL5, challenges: ALL20,
    dataProject: 100, test1: 100, mlProjectA: "", mlProjectB: ""
  });
  eq("provisional, no project: final is null", provNoProject.final, null);
  eq("provisional, no project: band is null", provNoProject.band, null);
  eq("provisional, no project: pending", provNoProject.projectPending, true);
  eq("provisional, no project: status line", provNoProject.projectStatus, "Project: PENDING");
  near("provisional, no project: 55 marks", provNoProject.provisional.marks, 55);
  near("provisional, no project: 100 percent", provNoProject.provisional.percent, 100);
  eq("provisional, no project: text", provNoProject.provisional.text, "Semester 1 provisional: 55.00 of 55 marks, 100.00 percent");
  eq("provisional, no project: nothing is missing", provNoProject.missing, []);
  var provWeak = computeFinal_({
    cohort: "CML3111",
    quizzes: [4, 5, 3, 5, 4, "", "", "", "", "", "", ""],
    challenges: [16, 18, 14, 20, 12, "", "", "", "", "", ""],
    dataProject: 72, test1: 65, mlProjectA: "", mlProjectB: ""
  });
  // Week 6 not assigned: weekly best 3 of [4,5,3,5,4] = 14 of 35 -> 6.00 ; assignments best 3 of [16,18,14,20,12] = 54 of 160 -> 5.06 ; DA 7.2 ; Test 1 9.75
  near("provisional, mid-semester student: marks", provWeak.provisional.marks, 15 * 14 / 35 + 5.06 + 7.2 + 9.75);
  near("provisional percent is marks over 55", provWeak.provisional.percent, provWeak.provisional.marks / 55 * 100);
  eq("the provisional percent is not diluted by the 45 unmarked project marks", provWeak.provisional.percent > 50, true);
  eq("provisional text carries both numbers", provWeak.provisional.text, "Semester 1 provisional: 28.01 of 55 marks, 50.93 percent");

  // PROVISIONAL, only Part A marked
  var provPartA = computeFinal_({
    quizzes: ALL5, challenges: ALL20,
    dataProject: 100, test1: 100, mlProjectA: 27, mlProjectB: ""
  });
  eq("only Part A: final is still null", provPartA.final, null);
  eq("only Part A: band is still null", provPartA.band, null);
  eq("only Part A: still pending", provPartA.projectPending, true);
  eq("only Part A: provisional line is unchanged by Part A", provPartA.provisional.text, provNoProject.provisional.text);
  var onlyB = computeFinal_({ quizzes: ALL5, challenges: ALL20, dataProject: 100, test1: 100, mlProjectA: "", mlProjectB: 12 });
  eq("only Part B: final is null", onlyB.final, null);

  // FULL total
  var full = computeFinal_({
    quizzes: ALL5, challenges: ALL20,
    dataProject: 80, test1: 60, mlProjectA: 24, mlProjectB: 9
  });
  // 15 + 15 + 8 + 9 + (24+9)/45*45 = 47 + 33 = 80
  near("full total out of 100: 15 + 15 + 8 + 9 + 33", full.final, 80);
  eq("full total: not pending", full.projectPending, false);
  eq("full total: has a band", full.band, "A");
  var projectZero = computeFinal_({ quizzes: ALL5, challenges: ALL20, dataProject: 100, test1: 100, mlProjectA: 0, mlProjectB: 0 });
  near("project typed as 0 and 0: final is 55, project counted as zero because it is marked", projectZero.final, 55);
  eq("project typed as 0 and 0: not pending", projectZero.projectPending, false);

  // A student with NO submissions at all
  var empty = computeFinal_({});
  eq("empty row: final is null (project pending)", empty.final, null);
  near("empty row: provisional marks 0", empty.provisional.marks, 0);
  near("empty row: provisional percent 0", empty.provisional.percent, 0);
  eq("empty row: provisional text", empty.provisional.text, "Semester 1 provisional: 0.00 of 55 marks, 0.00 percent");
  eq("empty row: pending", empty.projectPending, true);
  ok("empty row lists 8 things missing (2 big components, 2 weekly parts, 4 blocks); the project is pending, not missing", empty.missing.length === 8,
     JSON.stringify(empty.missing));
  ok("empty row: the ML project is not in Missing", empty.missing.every(function (m) { return m.indexOf("ML Project") < 0; }), JSON.stringify(empty.missing));
  var emptyAfter = computeFinal_({ mlProjectA: 0, mlProjectB: 0 });
  near("empty row once the project is marked as 0 and 0: final 0", emptyAfter.final, 0);
  eq("empty row once marked: band F", emptyAfter.band, "F");

  var ignoreOld = computeFinal_({
    quizzes: ALL5, challenges: ALL20,
    dataProject: 100, test1: 100, test2: 100, mlProject: 100, demo: 100
  });
  eq("a leftover Practical Test 2, Demo or old ML Project value in a row is ignored (project stays pending)", ignoreOld.final, null);
  near("a leftover Demo or Test 2 value adds nothing to the provisional marks", ignoreOld.provisional.marks, 55);

  var midterm = provWeak;
  ok("Practical Test 2 is never listed as missing", midterm.missing.indexOf("Practical Test 2") < 0, JSON.stringify(midterm.missing));
  ok("Demo is never listed as missing", midterm.missing.indexOf("Demo/viva") < 0 && midterm.missing.indexOf("Demo") < 0);
  ok("mid-semester student is NOT listed as missing the ML project", midterm.missing.indexOf("ML Project") < 0, JSON.stringify(midterm.missing));
  ok("mid-semester student flagged for Block 1 quiz", midterm.missing.indexOf("Block 1 quiz") >= 0, JSON.stringify(midterm.missing));
  ok("mid-semester student flagged for Block 2 assignment", midterm.missing.indexOf("Block 2 assignment") >= 0, JSON.stringify(midterm.missing));
  var noDa = computeFinal_({ quizzes: ALL5, challenges: ALL20, test1: 100 });
  ok("a blank Data Analysis Project is missing and counts as zero", noDa.missing.indexOf("Data Analysis Project") >= 0 && Math.abs(noDa.provisional.marks - 45) < 0.005, JSON.stringify(noDa.provisional));
  var afterBlock1 = computeFinal_({
    cohort: "CML3111",
    quizzes: [5, 5, 5, 5, 5, "", 5, 5, "", "", "", ""],
    challenges: [20, 20, 20, 20, 20, "", 20, 20, "", "", ""],
    dataProject: 0, test1: 0, mlProjectA: "", mlProjectB: ""
  });
  // quizzes: weekly best 3 of 5 = 15, plus Block 1 = 10 -> 25 of 35 ; assignments: weekly 60 + Block 1 40 = 100 of 160
  near("after Block 1: quizzes and assignments (provisional)", afterBlock1.provisional.marks, 15 * 25 / 35 + 15 * 100 / 160);
  eq("after Block 1 only Block 2 and the big components are missing",
     afterBlock1.missing.indexOf("Block 1 quiz") < 0 && afterBlock1.missing.indexOf("Block 2 quiz") >= 0, true);
  var afterBlock2 = computeFinal_({
    cohort: "CML3112",
    quizzes: [5, 5, 5, 5, 5, "", 5, 5, 5, 5, "", ""],
    challenges: [20, 20, 20, 20, 20, "", 20, 20, 20, 20, 20],
    dataProject: 0, test1: 0, mlProjectA: "", mlProjectB: ""
  });
  near("after both blocks the coursework is complete: 15 + 15", afterBlock2.provisional.marks, 30);
  ok("after both blocks no block is missing",
     afterBlock2.missing.every(function (m) { return m.indexOf("Block") < 0; }), JSON.stringify(afterBlock2.missing));

'''

TESTS_PROGRESS_ADD = r'''  var linePend = progressSummary_({
    cohort: "CML3111",
    quizzes: [4, 5, 3, 5, 4, "", 5, 4, "", "", "", ""],
    challenges: [16, 18, "", "", "", "", 19, 11, "", "", ""],
    dataProject: 72, test1: 65
  });
  ok("progress line shows the provisional result", linePend.indexOf("Semester 1 provisional: ") >= 0 && linePend.indexOf(" of 55 marks, ") >= 0, linePend);
  ok("progress line says the project is PENDING", linePend.indexOf("Project: PENDING") >= 0, linePend);
  ok("progress line does not show a banked total while pending", linePend.indexOf("Marks banked") < 0, linePend);
  var linePartA = progressSummary_({ cohort: "CML3111", quizzes: [], challenges: [], dataProject: 72, test1: 65, mlProjectA: 20, mlProjectB: "" });
  ok("progress line says Part A is marked and Part B is not", linePartA.indexOf("Part A is marked, Part B is not") >= 0, linePartA);
  var lineDone = progressSummary_({ cohort: "CML3111", quizzes: [], challenges: [], dataProject: 72, test1: 65, mlProjectA: 20, mlProjectB: 10 });
  ok("progress line shows the full total once the project is marked", lineDone.indexOf("Marks banked:") >= 0 && lineDone.indexOf("Project: PENDING") < 0, lineDone);

  // ---- sheet helpers ----
  eq("missingHeaders_ finds all four on an old sheet",
     missingHeaders_(["student_id", "ML Project", "Demo", "Final %"], PROJECT_INPUT_HEADERS.concat([PROVISIONAL_HEADER, PROJECT_STATUS_HEADER])),
     ["ML Project Part A", "ML Project Part B", "Semester 1 provisional", "Project"]);
  eq("missingHeaders_ does not mistake the old 'ML Project' column for the new ones",
     missingHeaders_(["ML Project"], ["ML Project Part A"]), ["ML Project Part A"]);
  eq("missingHeaders_ finds none when they are there (case and spaces ignored)",
     missingHeaders_(["ml project part a", "ML_Project_Part_B", "semester 1 provisional", "project"], PROJECT_INPUT_HEADERS.concat([PROVISIONAL_HEADER, PROJECT_STATUS_HEADER])), []);
  eq("markColumnMax_ assignment", markColumnMax_("W05"), 20);
  eq("markColumnMax_ Part A", markColumnMax_("ML Project Part A"), 30);
  eq("markColumnMax_ Part B", markColumnMax_("ML Project Part B"), 15);
  eq("markColumnMax_ Test 1", markColumnMax_("Practical Test 1"), 100);

'''


def main():
    text = PATH.read_text()
    if "GRADEBOOK_POLICY_20261110" in text:
        print("gradebook.gs: already on the 10 November 2026 policy (20 / 20 / 20 / 40); this 3 November patch is superseded and is not applied")
        return
    if MARK in text:
        print("gradebook.gs: already patched")
        return
    assert HEADER, "header text missing"
    backup(PATH)
    # header comment
    text = between(text, " * Revised 2 November 2026 for the four-class second half", " *\n * What is here:", HEADER)
    # weights
    text = between(text, "var WEIGHTS = {", "var QUIZ_COUNT = 12;", CONFIG)
    # pure helpers: insert after validateMark_/percentComponent_ block (before round2_)
    text = rep(text, "function round2_(x) { return Math.round(x * 100) / 100; }\n", PURE + "function round2_(x) { return Math.round(x * 100) / 100; }\n")
    # computeFinal_
    text = between(text, "function computeFinal_(row) {", "function gradeBand_(pct) {", COMPUTE)
    # doc comment of computeFinal_ mentions mlProject, demo
    text = rep(text, " * row: { quizzes: [], challenges: [], dataProject, test1,\n *        mlProject, demo }  - marks out of 100 for the four big components.\n",
               " * row: { quizzes: [], challenges: [], dataProject, test1, mlProjectA, mlProjectB }\n *        dataProject and test1 are marks out of 100; mlProjectA is out of 30 and mlProjectB out of 15, blank until marked.\n")
    text = rep(text, "/** Total of the six weights. Should always be 100; the tests assert it. */", "/** Total of the five weights. Should always be 100; the tests assert it. */")
    # progress
    text = rep(text, PROGRESS_TAIL_OLD, PROGRESS_TAIL_NEW)
    # menu and sheet side
    text = rep(text, '    .addItem("Recompute all totals", "recomputeAll")\n',
               '    .addItem("Add the project columns (run once)", "prepareGradesColumns")\n    .addItem("Recompute all totals", "recomputeAll")\n')
    text = rep(text, "function readGradesSheet_(spreadsheet) {", PREPARE + "function readGradesSheet_(spreadsheet) {")
    text = rep(text, '  var required = ["student_id"].concat(CHALLENGE_IDS);\n', '  var required = ["student_id"].concat(CHALLENGE_IDS).concat(PROJECT_INPUT_HEADERS);\n')
    text = rep(text, '  if (missing.length) { throw new Error("Grades sheet missing columns: " + missing.join(", ")); }',
               '  if (missing.length) { throw new Error("Grades sheet missing columns: " + missing.join(", ") + ". If these are the project columns, run prepareGradesColumns() once."); }')
    text = rep(text, '    mlProject: get("ML Project"),\n    demo: get("Demo")\n  };\n}\n', RECORD)
    text = between(text, "function recomputeAll() {", "  // One write for the whole block.", RECOMPUTE)
    # import
    text = rep(text, IMPORT_OLD, IMPORT_NEW)
    text = rep(text, "  var expected=CHALLENGE_IDS.indexOf(columnName)>=0?20:100;\n", "  var expected=markColumnMax_(columnName);\n")
    text = rep(text, "/** Import lecturer-side results by roster ID, atomically after validation.", MAXFN + "/** Import lecturer-side results by roster ID, atomically after validation.")
    # tests
    text = between(text, "  // ---- weights ----\n", "  // ---- bestNOf_ ----", TESTS_WEIGHTS)
    text = between(text, "  // ---- computeFinal_ ----\n", "  // ---- gradeBand_ ----", TESTS_FINAL)
    text = rep(text, '  ok("progress line adds up Block 1 assignment marks", line2.indexOf("Block 1 assignment: 2 of 2 parts submitted, 30 of 40 marks") >= 0, line2);\n',
               '  ok("progress line adds up Block 1 assignment marks", line2.indexOf("Block 1 assignment: 2 of 2 parts submitted, 30 of 40 marks") >= 0, line2);\n' + TESTS_PROGRESS_ADD)
    text = text.rstrip("\n") + f"\n\n// {MARK}: patched 3 November 2026 from data/assessment_blocks_20261103.json\n"
    bad = sorted({c for c in text if ord(c) > 127})
    assert not bad, f"non-ASCII characters {bad[:8]}"
    PATH.write_text(text)
    print("gradebook.gs: patched")


if __name__ == "__main__":
    main()
