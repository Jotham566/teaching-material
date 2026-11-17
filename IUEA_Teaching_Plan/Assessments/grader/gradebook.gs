/**
 * gradebook.gs - Google Apps Script gradebook for CML3111 / CML3112 / CML3113.
 * Revised 10 November 2026 (data/assessment_policy_20261110.json). There is NO demo, no Practical Test 2 and no Data Analysis project mark.
 * The Engineering ML project stays: one individual, timed 3-hour Colab sitting in Week 12 (like Practical Test 1), fully auto-graded, Weeks 1 to 11 only.
 *
 *   Assignments                20 %   A1 to A5 (columns W01 to W05), each out of 20. All five count equally, each worth 4.
 *   Quizzes                    20 %   Q1 to Q5, each out of 5. All five count equally, each worth 4.
 *   Practical Test 1           20 %   out of 100, scaled to 20
 *   Engineering ML Project     40 %   Part A coded project notebook /30 + Part B decision memo /15 = 45 raw, scaled to 40.
 *                                     Two columns. Counts only when BOTH parts are marked.
 *                             ----
 *                             100 %
 *
 * NOT COUNTED: Q6 onward and the block quizzes, A6 onward (W06, W08 ...) and the block assignments, the Data Analysis project,
 * Practical Test 2 and the demo. Their columns may stay in the sheet and their receipts are kept; they add nothing to the mark.
 * There is no best-3-of-5 rule and no Week 6 waiver any more. A missing or not-yet-marked item scores 0.
 *
 * PROVISIONAL MODE. Semester 1 results can be published before the project is marked. While either project column
 * (ML Project Part A, ML Project Part B) is blank the sheet shows "Semester 1 provisional: x of 60 marks, y percent"
 * (assignments, quizzes and Test 1; 20 + 20 + 20 = 60) and "Project: PENDING". Final % and
 * Band stay blank: an unmarked project is never counted as zero. Once BOTH columns hold a number (type 0 for a student
 * who submitted nothing) the sheet shows the full total out of 100.
 *
 * Rounding: each component is rounded to two decimals (Math.round(x*100)/100); the total is the rounded sum of the rounded components.
 *
 * What is here:
 *   recomputeAll()        weighted totals, missing flags
 *   ingestTokenCsv()      read a Form token export, verify each signature,
 *                         write the verified mark into the right challenge
 *                         column, and log everything that failed
 *   progressSummary()     the Coursera-style "you have completed 7 of 10" line
 *   emailStandings()      one email per student, resumable across days


 * The pure functions in the first half are unit tested. Run them with:
 *     node gradebook.gs --test
 * Apps Script ignores the node-only branches, which are all guarded by
 * `typeof Utilities === "undefined"`.
 *
 * VERIFIED LIMITS, unchanged from the previous version:
 *   - a free @gmail.com account sends to about 100 recipients a day, so a
 *     195-student mail-out runs over two days; emailStandings() checkpoints
 *     its progress in a script property and resumes
 *   - Apps Script stops a single execution at 6 minutes
 *   - GRADE_BANDS below is a PLACEHOLDER. Replace it with the IUEA regulations
 *     before you show a letter grade to anybody.
 */

/* eslint no-var: 0 */

// --------------------------------------------------------------------------
// configuration
// --------------------------------------------------------------------------

var WEIGHTS = {
  quizzes: 20,           // Q1 to Q5, each /5, scaled to 4 each
  challenges: 20,        // A1 to A5 (W01 to W05), each /20, scaled to 4 each
  test1: 20,             // Practical Test 1, /100 scaled to 20
  mlProject: 40          // Part A (coded notebook, /30) + Part B (decision memo, /15) = 45 raw, scaled to 40. There is no demo component.
};

var ML_PART_A_MAX = 30;        // marks for the coded project notebook (fully automatic)
var ML_PART_B_MAX = 15;        // marks for the decision memo form (fully automatic)
var PROJECT_INPUT_HEADERS = ["ML Project Part A", "ML Project Part B"];
var PROVISIONAL_HEADER = "Semester 1 provisional";
var PROJECT_STATUS_HEADER = "Project";
var PROJECT_PENDING_TEXT = "Project: PENDING";
var PROJECT_MARKED_TEXT = "Project: marked";

var QUIZ_COUNT = 12;           // columns Q1-Q12 may stay in the sheet, but only the first QUIZ_COUNTED feed the mark
var QUIZ_COUNTED = 5;          // Q1 to Q5 count; Q6 onward and the block quizzes do not
var QUIZ_MAX = 5;              // marks per quiz form, one per question

var CHALLENGE_COUNT = 11;      // columns W01-W06 and W08-W12 may stay in the sheet, but only the first CHALLENGE_COUNTED feed the mark
var CHALLENGE_COUNTED = 5;     // A1 to A5 (W01 to W05) count; A6 onward and the block assignments do not
var CHALLENGE_MAX = 20;        // marks per assignment

// Which assignment id maps to which challenge column. Edit this, not the code.
var CHALLENGE_IDS = ["W01", "W02", "W03", "W04", "W05", "W06", "W08", "W09", "W10", "W11", "W12"];

// Must match SIGNING_KEY in iuea_grader.py, byte for byte.
var SIGNING_KEY = "IUEA-CML31xx-2026S1-change-me";

var TOKEN_PREFIX = "IUEA1";
var SIG_BYTES = 10;

// PLACEHOLDER. Set against IUEA regulations before use.
var GRADE_BANDS = [
  [80, "A"], [70, "B+"], [60, "B"], [50, "C"], [45, "D"], [0, "F"]
];
var GRADE_BANDS_VERIFIED = false;

var GRADER_SHEET = "Grades";
var LOG_SHEET = "Token log";

// --------------------------------------------------------------------------
// pure helpers - all unit tested below
// --------------------------------------------------------------------------

/**
 * A component where the first `counted` items all count equally and a missing or blank item scores 0.
 * Component mark = sum * weight / (counted * perItemMax), rounded to two decimals. Items after the counted ones are ignored.
 */
function equalItemsComponent_(scores, counted, perItemMax, weight) {
  scores = scores || [];
  var total = 0, sat = 0, absent = [];
  for (var i = 0; i < counted; i++) {
    var v = scores[i];
    validateMark_(v, perItemMax);
    if (isBlankMark_(v)) { absent.push(i); continue; }
    total += Number(v); sat++;
  }
  var denom = counted * perItemMax;
  return {
    weighted: round2_(denom > 0 ? total * weight / denom : 0),
    outOf: weight,
    counted: counted,
    submitted: sat,
    absent: absent,
    raw: total,
    rawOutOf: denom
  };
}

/** A straight percentage component, e.g. a test marked out of 100. */
function validateMark_(mark, maximum) {
  if (mark === "" || mark === null || mark === undefined) { return; }
  if (typeof mark === "boolean" || !isFinite(Number(mark)) || Number(mark) < 0 || Number(mark) > maximum) {
    throw new Error("Invalid mark " + mark + "; expected 0 to " + maximum);
  }
}

function percentComponent_(mark, outOf, weight) {
  validateMark_(mark, outOf || 100);
  if (mark === "" || mark === null || mark === undefined || isNaN(Number(mark))) {
    return { weighted: 0, outOf: weight, missing: true, raw: null };
  }
  return { weighted: round2_(Number(mark) * weight / (outOf || 100)), outOf: weight, missing: false,
           raw: Number(mark) };
}

/** A cell with nothing in it. A typed 0 is NOT blank: it is a mark of zero. */
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
    weighted: marked ? round2_((a + b) * WEIGHTS.mlProject / outOfParts) : 0
  };
}

/** Weight of the components that are marked before the project: assignments + quizzes + Test 1 = 60. */
function provisionalOutOf_() {
  return WEIGHTS.quizzes + WEIGHTS.challenges + WEIGHTS.test1;
}

function fmt2_(x) { return Number(x).toFixed(2); }

function round2_(x) { return Math.round(x * 100) / 100; }

/**
 * Everything for one student.
 * row: { quizzes: [], challenges: [], test1, mlProjectA, mlProjectB }
 *        quizzes are Q1.. (only Q1 to Q5 count), challenges are W01.. (only W01 to W05 = A1 to A5 count);
 *        test1 is a mark out of 100; mlProjectA is out of 30 and mlProjectB out of 15, blank until marked.
 */
function computeFinal_(row) {
  var cp = equalItemsComponent_(row.quizzes, QUIZ_COUNTED, QUIZ_MAX, WEIGHTS.quizzes);
  var ch = equalItemsComponent_(row.challenges, CHALLENGE_COUNTED, CHALLENGE_MAX, WEIGHTS.challenges);
  var t1 = percentComponent_(row.test1, 100, WEIGHTS.test1);
  var pr = projectComponent_(row.mlProjectA, row.mlProjectB);

  // A missing quiz, assignment or Test 1 scores zero and is listed here.
  // The project is different: unmarked means PENDING, which is not a missing mark and is not listed here.
  var missing = [];
  if (t1.missing) { missing.push("Practical Test 1"); }
  if (cp.absent.length) { missing.push("quizzes: " + cp.absent.map(function (i) { return "Q" + (i + 1); }).join(", ")); }
  if (ch.absent.length) { missing.push("assignments: " + ch.absent.map(function (i) { return "A" + (i + 1); }).join(", ")); }

  // Provisional result: the three components that are marked before the project, out of 60.
  var provMarks = round2_(ch.weighted + cp.weighted + t1.weighted);
  var provOut = provisionalOutOf_();
  var provPercent = round2_(provMarks / provOut * 100);
  var provisional = {
    marks: provMarks,
    outOf: provOut,
    percent: provPercent,
    text: "Semester 1 provisional: " + fmt2_(provMarks) + " of " + provOut + " marks, " + fmt2_(provPercent) + " percent"
  };

  // Final result: only when the project is marked. Never a final figure or band that counts an unmarked project as zero.
  var final = pr.pending ? null : round2_(ch.weighted + cp.weighted + t1.weighted + pr.weighted);
  return {
    components: { quizzes: cp, challenges: ch,
                  test1: t1, mlProject: pr },
    final: final,
    band: pr.pending ? null : gradeBand_(final),
    projectPending: pr.pending,
    projectStatus: pr.pending ? PROJECT_PENDING_TEXT : PROJECT_MARKED_TEXT,
    provisional: provisional,
    missing: missing
  };
}

function gradeBand_(pct) {
  for (var i = 0; i < GRADE_BANDS.length; i++) {
    if (pct >= GRADE_BANDS[i][0]) { return GRADE_BANDS[i][1]; }
  }
  return "F";
}

/** Total of the weights. Should always be 100; the tests assert it. */
function weightTotal_() {
  var t = 0;
  for (var k in WEIGHTS) { if (WEIGHTS.hasOwnProperty(k)) { t += WEIGHTS[k]; } }
  return t;
}

/** The student-facing progress line. */
function progressSummary_(row) {
  var res = computeFinal_(row);
  var ch = res.components.challenges;
  var cp = res.components.quizzes;
  var lines = [];
  lines.push("Assignments A1 to A5: " + ch.submitted + " of " + ch.counted + " done. All five count equally; each is worth 4 marks.");
  lines.push("Quizzes Q1 to Q5: " + cp.submitted + " of " + cp.counted + " sat. All five count equally; each is worth 4 marks.");
  var pj = res.components.mlProject;
  if (res.projectPending) {
    lines.push(res.provisional.text + ".");
    lines.push(PROJECT_PENDING_TEXT + ". The Engineering ML project is worth " + WEIGHTS.mlProject + " marks and is not marked yet" +
               (pj.partAMarked ? " (Part A is marked, Part B is not)" : (pj.partBMarked ? " (Part B is marked, Part A is not)" : "")) +
               ". Your final total, out of 100, appears when it is marked.");
  } else {
    lines.push("Marks banked: " + res.final + " of 100 (the project is marked).");
  }
  if (res.missing.length) {
    lines.push("Not yet recorded (scores 0 until it is): " + res.missing.join("; ") + ".");
  }
  return lines.join("\n");
}

// --------------------------------------------------------------------------
// token verification - the same format iuea_grader.py writes
// --------------------------------------------------------------------------

var B32_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567";

/** base32 (RFC 4648, no padding) to an array of bytes 0-255. */
function b32Decode_(text) {
  var s = String(text).toUpperCase().replace(/[=\s]/g, "");
  var bits = 0, value = 0, out = [];
  for (var i = 0; i < s.length; i++) {
    var idx = B32_ALPHABET.indexOf(s.charAt(i));
    if (idx < 0) { return null; }
    value = (value << 5) | idx;
    bits += 5;
    if (bits >= 8) {
      out.push((value >>> (bits - 8)) & 255);
      bits -= 8;
    }
  }
  return out;
}

/**
 * Bytes to a string. Token bodies are ASCII by construction (student ids,
 * assignment ids, digits and separators), so a plain char map is enough and
 * behaves the same in Apps Script and in node.
 */
function bytesToAscii_(bytes) {
  var out = "";
  for (var i = 0; i < bytes.length; i++) {
    out += String.fromCharCode(bytes[i] & 255);
  }
  return out;
}

function asciiToBytes_(text) {
  var out = [];
  for (var i = 0; i < text.length; i++) { out.push(text.charCodeAt(i) & 255); }
  return out;
}

/** HMAC-SHA256 as unsigned bytes. Apps Script in production, node in tests. */
function hmacSha256Bytes_(keyStr, msgBytes) {
  if (typeof Utilities !== "undefined" &&
      Utilities.computeHmacSha256Signature) {
    var signed = [];
    for (var i = 0; i < msgBytes.length; i++) {
      signed.push(msgBytes[i] > 127 ? msgBytes[i] - 256 : msgBytes[i]);
    }
    var raw = Utilities.computeHmacSha256Signature(
      signed, Utilities.newBlob(keyStr).getBytes());
    var out = [];
    for (var j = 0; j < raw.length; j++) {
      out.push(raw[j] < 0 ? raw[j] + 256 : raw[j]);
    }
    return out;
  }
  // node, for `node gradebook.gs --test`
  var crypto = require("crypto");
  var h = crypto.createHmac("sha256", Buffer.from(keyStr, "utf8"));
  h.update(Buffer.from(msgBytes));
  return Array.prototype.slice.call(h.digest());
}

function base36ToInt_(s) {
  var n = parseInt(String(s), 36);
  return isNaN(n) ? 0 : n;
}

/** Split a decoded token body into fields. Pure, no crypto. */
function parseTokenBody_(body) {
  var parts = String(body).split("|");
  if (parts.length !== 6) { return null; }
  var scores = {}, total = 0;
  var items = parts[3] ? parts[3].split(",") : [];
  for (var i = 0; i < items.length; i++) {
    if (!items[i]) { continue; }
    var kv = items[i].split("=");
    var v = Number(kv.length > 1 ? kv[1] : 0);
    if (isNaN(v)) { v = 0; }
    scores[kv[0]] = v;
    total += v;
  }
  return {
    studentId: parts[0],
    assignment: parts[1],
    cohort: parts[2] === "-" ? "" : parts[2],
    scores: scores,
    claimedTotal: round2_(total),
    fingerprint: parts[4],
    timestamp: base36ToInt_(parts[5])
  };
}

/** Verify a submission code. Returns { ok, reason, ...fields }. */
function verifyToken_(token, key) {
  var out = { ok: false, reason: "", token: String(token || "").trim() };
  var text = out.token.replace(/\s/g, "");
  if (!text) { out.reason = "empty"; return out; }
  var parts = text.split("-");
  if (parts.length !== 3 || parts[0].toUpperCase() !== TOKEN_PREFIX) {
    out.reason = "not an IUEA submission code";
    return out;
  }
  var raw = b32Decode_(parts[1]);
  var sig = b32Decode_(parts[2]);
  if (raw === null || sig === null) {
    out.reason = "code is corrupted (bad base32) - probably a bad paste";
    return out;
  }
  var expect = hmacSha256Bytes_(key || SIGNING_KEY, raw).slice(0, SIG_BYTES);
  if (sig.length !== SIG_BYTES) {
    out.reason = "signature is the wrong length - the paste was cut short";
    return out;
  }
  var same = 0;
  for (var i = 0; i < SIG_BYTES; i++) { same |= (sig[i] ^ expect[i]); }
  if (same !== 0) { out.reason = "signature does not match"; return out; }
  var fields = parseTokenBody_(bytesToAscii_(raw));
  if (!fields) { out.reason = "signature valid but body unreadable"; return out; }
  out.ok = true;
  out.reason = "ok";
  for (var k in fields) {
    if (fields.hasOwnProperty(k)) { out[k] = fields[k]; }
  }
  return out;
}

/**
 * Parse CSV text. Handles quoted fields and embedded commas, which a Google
 * Forms export produces as soon as one question title has a comma in it.
 */
function parseCsv_(text) {
  var rows = [], row = [], field = "", inQuotes = false;
  var s = String(text).replace(/\r\n/g, "\n").replace(/\r/g, "\n");
  for (var i = 0; i < s.length; i++) {
    var c = s.charAt(i);
    if (inQuotes) {
      if (c === '"') {
        if (s.charAt(i + 1) === '"') { field += '"'; i++; }
        else { inQuotes = false; }
      } else { field += c; }
    } else if (c === '"') {
      inQuotes = true;
    } else if (c === ",") {
      row.push(field); field = "";
    } else if (c === "\n") {
      row.push(field); rows.push(row); row = []; field = "";
    } else {
      field += c;
    }
  }
  if (field !== "" || row.length) { row.push(field); rows.push(row); }
  return rows;
}

/** Find the token in a Form response row, wherever the column happens to be. */
function tokenInRow_(row) {
  for (var i = 0; i < row.length; i++) {
    var c = String(row[i] || "").trim();
    if (c.toUpperCase().indexOf(TOKEN_PREFIX + "-") === 0) { return c; }
  }
  return "";
}

/**
 * Turn a Form export into verified rows.
 * Returns { verified: [...], rejected: [...] }. One row per student, the
 * latest verified code winning, which is what "I count your last submission"
 * means in practice.
 */
function ingestTokenText_(csvText, assignment, key) {
  var rows = parseCsv_(csvText);
  var verified = {}, rejected = [];
  for (var i = 0; i < rows.length; i++) {
    var tok = tokenInRow_(rows[i]);
    if (!tok) {
      if (i > 0 && rows[i].join("").trim()) {
        rejected.push({ row: i + 1, studentId: "", reason: "no code in this row" });
      }
      continue;
    }
    var info = verifyToken_(tok, key);
    if (!info.ok) {
      rejected.push({ row: i + 1, studentId: "", reason: info.reason,
                      token: tok.slice(0, 40) });
      continue;
    }
    if (assignment && info.assignment !== String(assignment).toUpperCase()) {
      rejected.push({ row: i + 1, studentId: info.studentId,
                      reason: "code is for " + info.assignment + ", not " +
                              assignment });
      continue;
    }
    var prev = verified[info.studentId];
    if (!prev || info.timestamp >= prev.timestamp) {
      info.row = i + 1;
      verified[info.studentId] = info;
    }
  }
  var list = [];
  for (var sid in verified) {
    if (verified.hasOwnProperty(sid)) { list.push(verified[sid]); }
  }
  list.sort(function (a, b) { return a.studentId < b.studentId ? -1 : 1; });
  return { verified: list, rejected: rejected };
}

/**
 * Header name to zero-based column index. Spaces and underscores are ignored
 * and case does not matter, so "student_id", "Student Registration Number" and "studentid" all
 * find the same column. This is deliberate: the header row gets retyped every
 * year and a hard-coded column letter breaks silently.
 */
function columnIndexByHeader_(headers, name) {
  function norm(x) {
    var value=String(x).toLowerCase().replace(/[\s_]+/g, "");
    return ['studentregistrationnumber','registrationnumber','yourregistrationnumber'].indexOf(value)>=0 ? 'studentid' : value;
  }
  var want = norm(name);
  for (var i = 0; i < headers.length; i++) {
    if (norm(headers[i]) === want) { return i; }
  }
  return -1;
}

// --------------------------------------------------------------------------
// spreadsheet side - Apps Script only, not unit tested
// --------------------------------------------------------------------------

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu("CML3111-3 gradebook")
    .addItem("Add the project columns (run once)", "prepareGradesColumns")
    .addItem("Recompute all totals", "recomputeAll")
    .addItem("Ingest submission codes...", "ingestTokenCsv")
    .addItem("Show my progress line for the selected row", "showProgress")
    .addSeparator()
    .addItem("Email standings (resumable)", "emailStandings")
    .addToUi();
}

/** Headers from `wanted` that the sheet's header row does not have yet (same loose matching as columnIndexByHeader_). */
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

function readGradesSheet_(spreadsheet) {
  var sh = (spreadsheet||SpreadsheetApp.getActive()).getSheetByName(GRADER_SHEET);
  if (!sh) { throw new Error("No sheet called '" + GRADER_SHEET + "'."); }
  var values = sh.getDataRange().getValues();
  var required = ["student_id"].concat(CHALLENGE_IDS).concat(PROJECT_INPUT_HEADERS);
  for (var q = 1; q <= QUIZ_COUNT; q++) { required.push("Q" + q); }
  var missing = required.filter(function (h) { return columnIndexByHeader_(values[0], h) < 0; });
  if (missing.length) { throw new Error("Grades sheet missing columns: " + missing.join(", ") + ". If these are the project columns, run prepareGradesColumns() once."); }
  return { sheet: sh, headers: values[0], rows: values.slice(1) };
}

function rowToRecord_(headers, row) {
  function get(name) {
    var i = columnIndexByHeader_(headers, name);
    return i < 0 ? "" : row[i];
  }
  var cps = [], chs = [];
  for (var i = 1; i <= QUIZ_COUNT; i++) { cps.push(get("Q" + i)); }
  for (var j = 0; j < CHALLENGE_IDS.length; j++) {
    chs.push(get(CHALLENGE_IDS[j]));
  }
  return {
    studentId: String(get("student_id")).trim().toUpperCase(),
    name: get("name"),
    cohort: get("cohort"),
    quizzes: cps,
    challenges: chs,
    test1: get("Practical Test 1"),
    mlProjectA: get("ML Project Part A"),
    mlProjectB: get("ML Project Part B")
  };
}

function recomputeAll() {
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
  // One write for the whole block. 195 separate setValues calls is the
  // difference between two seconds and the six-minute execution cap.
  var width = g.headers.length;
  var block = [];
  for (var k = 0; k < out.length; k++) {
    var line = out[k] || g.rows[k].slice();
    while (line.length < width) { line.push(""); }
    block.push(line.slice(0, width));
  }
  if (block.length) {
    g.sheet.getRange(2, 1, block.length, width).setValues(block);
  }
  SpreadsheetApp.getActive().toast("Recomputed " + block.length + " rows.");
}

/**
 * Ask for the assignment id and the token CSV, verify every code, and write
 * the verified mark into that assignment's column.
 *
 * The mark written is the token's VISIBLE total, which is what the student
 * could self-check. It is a provisional figure. batch_grade.py produces the
 * real mark from the notebook, including the hidden tests, and that number
 * overwrites this one when you paste the results.csv column in.
 */
/**
 * Turn a sheet's values into CSV text, so the linked Form responses sheet and
 * a downloaded CSV go through exactly the same code path.
 */
function sheetToCsvText_(values) {
  var lines = [];
  for (var r = 0; r < values.length; r++) {
    var cells = [];
    for (var c = 0; c < values[r].length; c++) {
      var v = String(values[r][c] === null ? "" : values[r][c]);
      cells.push(/[",\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v);
    }
    lines.push(cells.join(","));
  }
  return lines.join("\n");
}

/**
 * Where the codes come from, in order of preference:
 *   1. a sheet in this spreadsheet whose name starts with "Form responses",
 *      which is what linking the Form to the sheet creates
 *   2. a .csv file in Drive, named in the prompt
 * Pasting 195 rows into an Apps Script prompt box does not work in practice,
 * which is why there is no paste option.
 */
function readTokenCsvText_(assignment) {
  var ss = SpreadsheetApp.getActive();
  var sh = ss.getSheetByName("Responses_" + assignment);
  if (sh) {
    return { text: sheetToCsvText_(sh.getDataRange().getValues()), source: sh.getName() };
  }
  var fname = SpreadsheetApp.getUi()
    .prompt("No linked Form responses sheet found.\n\n" +
            "Name of the CSV file in your Drive:").getResponseText();
  if (!fname) { return null; }
  var it = DriveApp.getFilesByName(fname.trim());
  if (!it.hasNext()) {
    throw new Error("No file called '" + fname + "' in your Drive.");
  }
  var f = it.next();
  return { text: f.getBlob().getDataAsString(),
           source: "Drive file '" + f.getName() + "'" };
}

function ingestTokenCsv() {
  var ui = SpreadsheetApp.getUi();
  var a = ui.prompt("Which assignment? e.g. W05").getResponseText();
  if (!a) { return; }
  a = a.trim().toUpperCase();
  var src = readTokenCsvText_(a);
  if (!src) { return; }

  var res = ingestTokenText_(src.text, a, SIGNING_KEY);
  var ss = SpreadsheetApp.getActive();
  var practice = ss.getSheetByName("Practice receipts") || ss.insertSheet("Practice receipts");
  if (!practice.getLastRow()) { practice.appendRow(["assignment", "student_id", "claimed_visible", "verified_at"]); }
  res.verified.forEach(function(v) { practice.appendRow([a,v.studentId,v.claimedTotal,new Date()]); });
  ui.alert("Verified " + res.verified.length + " practice receipts. Final grade columns were not changed. Import instructor-side grading results for marks.");
}

function showProgress() {
  var g = readGradesSheet_();
  var r = SpreadsheetApp.getActive().getActiveRange().getRow() - 2;
  if (r < 0 || r >= g.rows.length) {
    SpreadsheetApp.getUi().alert("Select a student's row first.");
    return;
  }
  var rec = rowToRecord_(g.headers, g.rows[r]);
  SpreadsheetApp.getUi().alert(rec.studentId + "\n\n" + progressSummary_(rec));
}

/**
 * One email per student. A free @gmail.com account is capped near 100
 * recipients a day, so this stops at DAILY_CAP and remembers where it got to.
 * Run it again the next day to finish.
 */
function emailStandings() {
  var DAILY_CAP = 90;
  var props = PropertiesService.getScriptProperties();
  var start = Number(props.getProperty("emailCursor") || 0);
  var g = readGradesSheet_();
  var iEmail = columnIndexByHeader_(g.headers, "email");
  if (iEmail < 0) { throw new Error("No 'email' column."); }
  var sent = 0, i = start;
  for (; i < g.rows.length && sent < DAILY_CAP; i++) {
    var rec = rowToRecord_(g.headers, g.rows[i]);
    var to = String(g.rows[i][iEmail] || "").trim();
    if (!rec.studentId || !to) { continue; }
    MailApp.sendEmail(to,
      "Your standing in " + (rec.cohort || "Introduction to ML"),
      rec.studentId + "\n\n" + progressSummary_(rec) +
      "\n\nThis is where you stand today, not a final mark.\n");
    sent++;
  }
  props.setProperty("emailCursor", i >= g.rows.length ? "0" : String(i));
  SpreadsheetApp.getActive().toast(
    "Sent " + sent + ". " + (i >= g.rows.length
      ? "That was everybody."
      : "Stopped at row " + (i + 2) + "; run again tomorrow."));
}

// --------------------------------------------------------------------------
// unit tests: node gradebook.gs --test
// --------------------------------------------------------------------------

function runUnitTests_() {
  var pass = 0, fail = 0, failures = [];

  function ok(name, cond, detail) {
    if (cond) { pass++; console.log("  pass  " + name); }
    else {
      fail++;
      failures.push(name);
      console.log("  FAIL  " + name + (detail ? "   " + detail : ""));
    }
  }
  function eq(name, got, want) {
    ok(name, JSON.stringify(got) === JSON.stringify(want),
       "got " + JSON.stringify(got) + " want " + JSON.stringify(want));
  }
  function near(name, got, want) {
    ok(name, Math.abs(got - want) < 0.005, "got " + got + " want " + want);
  }

  // ---- weights (10 November 2026 policy: 20 + 20 + 20 + 40) ----
  eq("weights total 100", weightTotal_(), 100);
  eq("weights are the 10 November 2026 weights", WEIGHTS, {quizzes: 20, challenges: 20, test1: 20, mlProject: 40});
  ok("Practical Test 2 has no weight", !WEIGHTS.hasOwnProperty("test2"));
  ok("the demonstration has no weight", !WEIGHTS.hasOwnProperty("demo"));
  ok("the Data Analysis project has no weight", !WEIGHTS.hasOwnProperty("dataProject"));
  eq("project raw marks are 30 + 15 = 45", ML_PART_A_MAX + ML_PART_B_MAX, 45);
  eq("the provisional components weigh 60", provisionalOutOf_(), 60);
  eq("provisional plus project is 100", provisionalOutOf_() + WEIGHTS.mlProject, 100);
  eq("five quizzes and five assignments count", [QUIZ_COUNTED, CHALLENGE_COUNTED], [5, 5]);
  eq("the counted assignment columns are W01 to W05 (A1 to A5)", CHALLENGE_IDS.slice(0, CHALLENGE_COUNTED), ["W01", "W02", "W03", "W04", "W05"]);

  // ---- equalItemsComponent_: all five count, a missing one scores 0 ----
  var eqFull = equalItemsComponent_([20, 20, 20, 20, 20], 5, 20, 20);
  near("assignments: five full marks -> 20", eqFull.weighted, 20);
  eq("assignments: raw 100 of 100", [eqFull.raw, eqFull.rawOutOf, eqFull.submitted], [100, 100, 5]);
  near("assignments: 16+18+14+20+12 = 80 of 100 -> 16", equalItemsComponent_([16, 18, 14, 20, 12], 5, 20, 20).weighted, 16);
  near("quizzes: 4+5+3+5+4 = 21 of 25 -> 16.8", equalItemsComponent_([4, 5, 3, 5, 4], 5, 5, 20).weighted, 16.8);
  near("a missing item scores 0: four 5s and a blank -> 16", equalItemsComponent_([5, 5, 5, 5, ""], 5, 5, 20).weighted, 16);
  near("nothing at all -> 0", equalItemsComponent_([], 5, 5, 20).weighted, 0);
  near("undefined scores -> 0", equalItemsComponent_(undefined, 5, 20, 20).weighted, 0);
  eq("submitted counts only the numbers among the five", equalItemsComponent_([5, "", 0, null, 3], 5, 5, 20).submitted, 3);
  eq("absent lists the blank positions, a typed 0 is not absent", equalItemsComponent_([5, "", 0, null, 3], 5, 5, 20).absent, [1, 3]);
  near("items after the fifth are ignored", equalItemsComponent_([5, 5, 5, 5, 5, 0, 0, 5, 5], 5, 5, 20).weighted, 20);
  near("a high sixth item adds nothing", equalItemsComponent_([0, 0, 0, 0, 0, 5, 5, 5], 5, 5, 20).weighted, 0);
  near("17.5 of 25 -> 14", equalItemsComponent_([3.5, 3.5, 3.5, 3.5, 3.5], 5, 5, 20).weighted, 14);
  var badMark = false; try { equalItemsComponent_([21, 0, 0, 0, 0], 5, 20, 20); } catch (e) { badMark = true; }
  ok("a mark above the maximum is rejected", badMark);
  var badText = false; try { equalItemsComponent_([5, "absent", 0, 0, 0], 5, 5, 20); } catch (e) { badText = true; }
  ok("text in a mark cell is rejected", badText);
  var badNeg = false; try { equalItemsComponent_([-1, 0, 0, 0, 0], 5, 5, 20); } catch (e) { badNeg = true; }
  ok("a negative mark is rejected", badNeg);


  // ---- percentComponent_ ----
  near("test1 at 60/100 -> 12 of 20", percentComponent_(60, 100, 20).weighted, 12);
  ok("blank test flagged missing", percentComponent_("", 100, 20).missing);
  var rejectedText=false;
  try{percentComponent_("absent",100,20);}catch(e){rejectedText=true;}
  ok("text in a test cell is rejected",rejectedText);
  near("blank test scores 0", percentComponent_("", 100, 20).weighted, 0);

  // ---- project component ----
  var pc0 = projectComponent_("", "");
  ok("both project parts blank: pending, not zero", pc0.pending && !pc0.marked && pc0.weighted === 0 && pc0.raw === null);
  var pcA = projectComponent_(24, "");
  ok("only Part A: still pending", pcA.pending && pcA.partAMarked && !pcA.partBMarked && pcA.weighted === 0);
  var pcB = projectComponent_(null, 9);
  ok("only Part B: still pending", pcB.pending && !pcB.partAMarked && pcB.partBMarked);
  var pcAB = projectComponent_(24, 9);
  ok("both parts: marked", pcAB.marked && !pcAB.pending);
  near("both parts: 33 of 45 raw is 29.33 of 40", pcAB.weighted, 29.33);
  var pcZero = projectComponent_(0, 0);
  ok("typed zeros are a mark of zero, not pending", pcZero.marked && pcZero.weighted === 0);
  ok("a space is blank", projectComponent_(" ", " ").pending);
  var rejected = 0;
  [[31, 0], [0, 16], [-1, 0], ["absent", 0], [0, "x"]].forEach(function (p) { try { projectComponent_(p[0], p[1]); } catch (e) { rejected++; } });
  eq("project marks above the maximum, negative or text are rejected", rejected, 5);

  // ---- computeFinal_ ----
  var Q5S = [5, 5, 5, 5, 5], A5S = [20, 20, 20, 20, 20];
  var perfect = computeFinal_({
    quizzes: Q5S, challenges: A5S,
    test1: 100, mlProjectA: 30, mlProjectB: 15
  });
  near("perfect student with the project marked -> 100", perfect.final, 100);
  eq("perfect student has nothing missing", perfect.missing, []);
  eq("perfect student's project is not pending", perfect.projectPending, false);
  eq("perfect student's status line", perfect.projectStatus, "Project: marked");
  eq("perfect student gets a band", perfect.band, "A");
  var half = computeFinal_({
    quizzes: [2.5, 2.5, 2.5, 2.5, 2.5], challenges: [10, 10, 10, 10, 10],
    test1: 50, mlProjectA: 15, mlProjectB: 7.5
  });
  // 10 + 10 + 10 + 22.5 * 40 / 45 = 20 -> 50
  near("half marks everywhere -> 50", half.final, 50);

  // PROVISIONAL, no project at all
  var provNoProject = computeFinal_({
    quizzes: Q5S, challenges: A5S,
    test1: 100, mlProjectA: "", mlProjectB: ""
  });
  eq("provisional, no project: final is null", provNoProject.final, null);
  eq("provisional, no project: band is null", provNoProject.band, null);
  eq("provisional, no project: pending", provNoProject.projectPending, true);
  eq("provisional, no project: status line", provNoProject.projectStatus, "Project: PENDING");
  near("provisional, no project: 60 marks", provNoProject.provisional.marks, 60);
  near("provisional, no project: 100 percent", provNoProject.provisional.percent, 100);
  eq("provisional, no project: text", provNoProject.provisional.text, "Semester 1 provisional: 60.00 of 60 marks, 100.00 percent");
  eq("provisional, no project: nothing is missing", provNoProject.missing, []);
  var provWeak = computeFinal_({
    quizzes: [4, 5, 3, 5, 4, "", "", "", "", "", "", ""],
    challenges: [16, 18, 14, 20, 12, "", "", "", "", "", ""],
    test1: 65, mlProjectA: "", mlProjectB: ""
  });
  // quizzes 21 of 25 -> 16.80 ; assignments 80 of 100 -> 16.00 ; Test 1 65 -> 13.00 ; provisional 45.80 of 60 = 76.33 percent
  near("provisional, mid-semester student: marks", provWeak.provisional.marks, 45.8);
  near("provisional percent is marks over 60", provWeak.provisional.percent, 76.33);
  eq("provisional text carries both numbers", provWeak.provisional.text, "Semester 1 provisional: 45.80 of 60 marks, 76.33 percent");
  eq("mid-semester student has no missing item", provWeak.missing, []);

  // PROVISIONAL, only Part A marked
  var provPartA = computeFinal_({ quizzes: Q5S, challenges: A5S, test1: 100, mlProjectA: 27, mlProjectB: "" });
  eq("only Part A: final is still null", provPartA.final, null);
  eq("only Part A: band is still null", provPartA.band, null);
  eq("only Part A: still pending", provPartA.projectPending, true);
  eq("only Part A: provisional line is unchanged by Part A", provPartA.provisional.text, provNoProject.provisional.text);
  var onlyB = computeFinal_({ quizzes: Q5S, challenges: A5S, test1: 100, mlProjectA: "", mlProjectB: 12 });
  eq("only Part B: final is null", onlyB.final, null);

  // FULL total
  var full = computeFinal_({
    quizzes: Q5S, challenges: A5S,
    test1: 60, mlProjectA: 24, mlProjectB: 9
  });
  // 20 + 20 + 12 + 33 * 40 / 45 (= 29.33) = 81.33
  near("full total out of 100: 20 + 20 + 12 + 29.33", full.final, 81.33);
  eq("full total: not pending", full.projectPending, false);
  eq("full total: has a band", full.band, "A");
  var projectZero = computeFinal_({ quizzes: Q5S, challenges: A5S, test1: 100, mlProjectA: 0, mlProjectB: 0 });
  near("project typed as 0 and 0: final is 60, project counted as zero because it is marked", projectZero.final, 60);
  eq("project typed as 0 and 0: not pending", projectZero.projectPending, false);

  // rounding: each component to 2 decimals, total is the rounded sum of the rounded components
  var rnd = computeFinal_({
    quizzes: [3.5, 3.5, 3.5, 3.5, 3.5], challenges: [7, 7, 7, 7, 9.5],
    test1: 77, mlProjectA: 29, mlProjectB: 14
  });
  // quizzes 17.5 of 25 -> 14 ; assignments 7+7+7+7+9.5 = 37.5 of 100 -> 7.5 ; Test 1 77 -> 15.4 ; project 43 * 40 / 45 = 38.2222 -> 38.22
  eq("rounding: quizzes", rnd.components.quizzes.weighted, 14);
  eq("rounding: assignments", rnd.components.challenges.weighted, 7.5);
  eq("rounding: test", rnd.components.test1.weighted, 15.4);
  eq("rounding: project", rnd.components.mlProject.weighted, 38.22);
  eq("rounding: total is the sum of the rounded components", rnd.final, 75.12);

  // A student with NO submissions at all
  var empty = computeFinal_({});
  eq("empty row: final is null (project pending)", empty.final, null);
  near("empty row: provisional marks 0", empty.provisional.marks, 0);
  near("empty row: provisional percent 0", empty.provisional.percent, 0);
  eq("empty row: provisional text", empty.provisional.text, "Semester 1 provisional: 0.00 of 60 marks, 0.00 percent");
  eq("empty row: pending", empty.projectPending, true);
  eq("empty row lists the test, five quizzes and five assignments as missing; the project is pending, not missing", empty.missing,
     ["Practical Test 1", "quizzes: Q1, Q2, Q3, Q4, Q5", "assignments: A1, A2, A3, A4, A5"]);
  var emptyAfter = computeFinal_({ mlProjectA: 0, mlProjectB: 0 });
  near("empty row once the project is marked as 0 and 0: final 0", emptyAfter.final, 0);
  eq("empty row once marked: band F", emptyAfter.band, "F");

  // things that no longer count
  var ignoreOld = computeFinal_({
    quizzes: [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], challenges: [20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20],
    dataProject: 100, test1: 100, test2: 100, mlProject: 100, demo: 100
  });
  eq("a leftover Practical Test 2, Demo, Data Analysis or old ML Project value in a row is ignored (project stays pending)", ignoreOld.final, null);
  near("those leftovers add nothing to the provisional marks: exactly 60", ignoreOld.provisional.marks, 60);
  var lateOnly = computeFinal_({
    quizzes: ["", "", "", "", "", 5, 5, 5, 5, 5, 5, 5], challenges: ["", "", "", "", "", 20, 20, 20, 20, 20, 20],
    test1: "", mlProjectA: "", mlProjectB: ""
  });
  near("Q6 onward and A6 onward (W06, W08 to W12) add nothing when Q1-Q5 and A1-A5 are blank", lateOnly.provisional.marks, 0);
  eq("and Q1-Q5, A1-A5 and Test 1 are listed as missing", lateOnly.missing,
     ["Practical Test 1", "quizzes: Q1, Q2, Q3, Q4, Q5", "assignments: A1, A2, A3, A4, A5"]);
  var weakLate = computeFinal_({
    quizzes: [5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0], challenges: [20, 20, 20, 20, 20, 0, 0, 0, 0, 0, 0],
    test1: 100, mlProjectA: "", mlProjectB: ""
  });
  near("zeros in Q6 onward and A6 onward do not hurt a full Q1-Q5 and A1-A5", weakLate.provisional.marks, 60);
  eq("and nothing is missing", weakLate.missing, []);
  var gaps = computeFinal_({
    quizzes: [5, 5, "", 5, 5], challenges: [20, "", 20, 20, 20], test1: 100, mlProjectA: "", mlProjectB: ""
  });
  // quizzes 20 of 25 -> 16 ; assignments 80 of 100 -> 16 ; Test 1 -> 20 ; provisional 52
  near("one missing quiz and one missing assignment each score 0", gaps.provisional.marks, 52);
  eq("the gaps are named", gaps.missing, ["quizzes: Q3", "assignments: A2"]);
  var typedZero = computeFinal_({ quizzes: [0, 5, 5, 5, 5], challenges: A5S, test1: 100, mlProjectA: "", mlProjectB: "" });
  eq("a typed 0 quiz mark is a mark, not a missing item", typedZero.missing, []);
  var noTest = computeFinal_({ quizzes: Q5S, challenges: A5S });
  ok("a blank Practical Test 1 is missing and counts as zero", noTest.missing.indexOf("Practical Test 1") >= 0 && Math.abs(noTest.provisional.marks - 40) < 0.005, JSON.stringify(noTest.provisional));
  var anyCohort = computeFinal_({ cohort: "CML3112", quizzes: Q5S, challenges: A5S, test1: 100, mlProjectA: 30, mlProjectB: 15 });
  eq("the cohort makes no difference: no Week 6 waiver any more", anyCohort.final, 100);
  var inputs = { quizzes: Q5S.slice(), challenges: A5S.slice(), test1: 100 }; var before = JSON.stringify(inputs); computeFinal_(inputs);
  eq("computeFinal_ does not change its input", JSON.stringify(inputs), before);
  var badQuiz = false; try { computeFinal_({ quizzes: [6, 0, 0, 0, 0] }); } catch (e) { badQuiz = true; }
  ok("a quiz mark above 5 is rejected", badQuiz);


  // ---- gradeBand_ ----
  eq("band 85 -> A", gradeBand_(85), "A");
  eq("band 80 -> A on the boundary", gradeBand_(80), "A");
  eq("band 79.99 -> B+", gradeBand_(79.99), "B+");
  eq("band 0 -> F", gradeBand_(0), "F");

  // ---- progressSummary_ ----
  var line = progressSummary_({
    quizzes: [4, 5, 3, 5, 4, "", "", "", "", "", "", ""],
    challenges: [16, 18, 14, 20, 12, "", "", "", "", "", ""]
  });
  ok("progress line counts 5 of 5 assignments", line.indexOf("Assignments A1 to A5: 5 of 5 done") >= 0, line);
  ok("progress line counts 5 of 5 quizzes", line.indexOf("Quizzes Q1 to Q5: 5 of 5 sat") >= 0, line);
  ok("progress line says all five count", line.indexOf("All five count equally") >= 0, line);
  ok("progress line has no best-of or block wording", !/best|Block|Week 6|waive|not assigned/i.test(line), line);
  var line2 = progressSummary_({
    quizzes: [4, 5, "", "", "", "", 5, 4], challenges: [16, 18, "", "", "", "", 19, 11], test1: 65
  });
  ok("progress line counts only Q1 to Q5", line2.indexOf("Quizzes Q1 to Q5: 2 of 5 sat") >= 0, line2);
  ok("progress line counts only A1 to A5", line2.indexOf("Assignments A1 to A5: 2 of 5 done") >= 0, line2);
  ok("progress line says what is not recorded", line2.indexOf("Not yet recorded (scores 0 until it is): quizzes: Q3, Q4, Q5; assignments: A3, A4, A5.") >= 0, line2);
  var linePend = progressSummary_({ quizzes: Q5S, challenges: A5S, test1: 65 });
  ok("progress line shows the provisional result", linePend.indexOf("Semester 1 provisional: 53.00 of 60 marks, 88.33 percent") >= 0, linePend);
  ok("progress line says the project is PENDING", linePend.indexOf("Project: PENDING") >= 0, linePend);
  ok("progress line says the project is worth 40", linePend.indexOf("worth 40 marks") >= 0, linePend);
  ok("progress line does not show a banked total while pending", linePend.indexOf("Marks banked") < 0, linePend);
  var linePartA = progressSummary_({ quizzes: [], challenges: [], test1: 65, mlProjectA: 20, mlProjectB: "" });
  ok("progress line says Part A is marked and Part B is not", linePartA.indexOf("Part A is marked, Part B is not") >= 0, linePartA);
  var lineDone = progressSummary_({ quizzes: [], challenges: [], test1: 65, mlProjectA: 20, mlProjectB: 10 });
  ok("progress line shows the full total once the project is marked", lineDone.indexOf("Marks banked: 39.67 of 100") >= 0 && lineDone.indexOf("Project: PENDING") < 0, lineDone);


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


  // ---- base32 ----
  eq("b32Decode_ NBSWY3DP -> hello",
     bytesToAscii_(b32Decode_("NBSWY3DP")), "hello");
  eq("b32Decode_ is case insensitive",
     bytesToAscii_(b32Decode_("nbswy3dp")), "hello");
  eq("b32Decode_ rejects bad characters", b32Decode_("N!SWY3DP"), null);
  eq("base36ToInt_ T43HC0", base36ToInt_("T43HC0"), 1760400000);

  // ---- tokens: a real one, produced by iuea_grader.py ----
  var TOK = "IUEA1-KMZDIMBUGJ6FOMBVPRBU2TBTGEYTE7DRGE6TGLDRGI6TGLDRGM6TI7CNIZ" +
            "JEOR22IRDE2WSUK5IXYVBUGNEEGMA-CXHTNY7NGNAPJD3L";
  var v = verifyToken_(TOK, "IUEA-CML31xx-2026S1-change-me");
  ok("real token verifies", v.ok, v.reason);
  eq("token student id", v.studentId, "S24042");
  eq("token assignment", v.assignment, "W05");
  eq("token cohort", v.cohort, "CML3112");
  eq("token scores", v.scores, { q1: 3, q2: 3, q3: 4 });
  eq("token claimed total", v.claimedTotal, 10);
  eq("token fingerprint", v.fingerprint, "MFRGGZDFMZTWQ");
  eq("token timestamp", v.timestamp, 1760400000);
  eq("token under 200 chars", TOK.length < 200, true);

  ok("wrong key rejected",
     !verifyToken_(TOK, "some-other-key").ok);
  var mangled = TOK.slice(0, 40) + (TOK.charAt(40) === "A" ? "B" : "A") +
                TOK.slice(41);
  ok("one changed character rejected", !verifyToken_(mangled).ok);
  ok("truncated code rejected", !verifyToken_(TOK.slice(0, TOK.length - 6)).ok);
  ok("empty rejected", !verifyToken_("").ok);
  ok("null rejected", !verifyToken_(null).ok);
  ok("junk rejected", !verifyToken_("hello world").ok);
  eq("non-IUEA string gives a clear reason",
     verifyToken_("ABC-DEF-GHI").reason, "not an IUEA submission code");

  // ---- parseTokenBody_ ----
  eq("parseTokenBody_ wrong field count", parseTokenBody_("a|b|c"), null);
  var pb = parseTokenBody_("S1|W03|-|q1=2.5,q2=0|ZZZ|T43HC0");
  eq("parseTokenBody_ blank cohort", pb.cohort, "");
  eq("parseTokenBody_ fractional marks", pb.scores, { q1: 2.5, q2: 0 });
  eq("parseTokenBody_ total", pb.claimedTotal, 2.5);

  // ---- CSV ----
  var csv = 'Timestamp,Student number,Code\n' +
            '2026/10/12 08:00:00,S24042,' + TOK + '\n' +
            '2026/10/12 08:01:00,S24043,IUEA1-AAAA-BBBB\n' +
            '2026/10/12 08:02:00,S24044,\n';
  var rows = parseCsv_(csv);
  eq("parseCsv_ row count", rows.length, 4);
  eq("parseCsv_ finds the token", tokenInRow_(rows[1]), TOK);
  eq("parseCsv_ handles quoted commas",
     parseCsv_('a,"b,c",d\n')[0], ["a", "b,c", "d"]);
  eq("parseCsv_ handles a doubled quote",
     parseCsv_('a,"say ""hi""",c\n')[0], ["a", 'say "hi"', "c"]);

  var ing = ingestTokenText_(csv, "W05", "IUEA-CML31xx-2026S1-change-me");
  eq("ingest verified one", ing.verified.length, 1);
  eq("ingest verified the right student", ing.verified[0].studentId, "S24042");
  eq("ingest rejected two", ing.rejected.length, 2);
  ok("ingest reports the empty row",
     ing.rejected[1].reason === "no code in this row",
     JSON.stringify(ing.rejected));

  var wrongWeek = ingestTokenText_(csv, "W03",
                                   "IUEA-CML31xx-2026S1-change-me");
  eq("ingest refuses a code for another week", wrongWeek.verified.length, 0);
  ok("ingest says which week the code was for",
     wrongWeek.rejected[0].reason.indexOf("code is for W05") >= 0,
     JSON.stringify(wrongWeek.rejected[0]));

  // resubmission: the later timestamp wins
  var later = "IUEA1-" + "KMZDIMBUGJ6FOMBVPRBU2TBTGEYTE7DRGE6TGLDRGI6TGLDRGM6" +
              "TI7CNIZJEOR22IRDE2WSUK5IXYVBUGNEEGMA-CXHTNY7NGNAPJD3L";
  var twice = ingestTokenText_(
    'h1,h2\nx,' + TOK + '\ny,' + later + '\n', "W05",
    "IUEA-CML31xx-2026S1-change-me");
  eq("the same code twice collapses to one student", twice.verified.length, 1);

  // ---- columnIndexByHeader_ ----
  var H = ["student_id", "name", "cohort", "CP1", "W05", "Final %"];
  eq("header lookup exact", columnIndexByHeader_(H, "W05"), 4);
  eq("header lookup ignores case", columnIndexByHeader_(H, "final %"), 5);
  eq("header lookup ignores spaces", columnIndexByHeader_(H, "student id"), 0);
  eq("header lookup registration number", columnIndexByHeader_(H, "Student Registration Number"), 0);
  eq("header lookup misses cleanly", columnIndexByHeader_(H, "W99"), -1);

  console.log("");
  console.log("  " + pass + " passed, " + fail + " failed");
  if (fail) { console.log("  failures: " + failures.join(", ")); }
  return fail;
}

if (typeof module !== "undefined" && typeof process !== "undefined" &&
    process.argv && process.argv.indexOf("--test") >= 0) {
  process.exit(runUnitTests_() === 0 ? 0 : 1);
}

/** The maximum a column's marks can have: 20 for an assignment part, 30 and 15 for the two project parts, 100 otherwise. */
function markColumnMax_(columnName) {
  if (CHALLENGE_IDS.indexOf(columnName) >= 0) { return CHALLENGE_MAX; }
  if (columnName === PROJECT_INPUT_HEADERS[0]) { return ML_PART_A_MAX; }
  if (columnName === PROJECT_INPUT_HEADERS[1]) { return ML_PART_B_MAX; }
  return 100;
}

/** Import lecturer-side results by roster ID, atomically after validation.
 * CSV must contain student_id,status plus score,maximum (artifact grader)
 * or notebook_total,max_total (isolated notebook grader). No token-only rows.
 */
function importMarkedResults(fileId, columnName, spreadsheet) {
  // Practical Test 2, the demo and the Data Analysis project do not count from 10 November 2026; their columns are no longer import targets.
  var allowed=CHALLENGE_IDS.concat(['Practical Test 1'],PROJECT_INPUT_HEADERS);
  if (allowed.indexOf(columnName)<0) { throw new Error('Unknown assessment column'); }
  var rows=Utilities.parseCsv(DriveApp.getFileById(fileId).getBlob().getDataAsString());
  var h=rows.shift(), index=function(name){return h.indexOf(name);};
  var sid=index('student_id'), status=index('status');
  var score=index('score')<0?index('notebook_total'):index('score');
  var maximum=index('maximum')<0?index('max_total'):index('maximum');
  if ([sid,status,score,maximum].some(function(i){return i<0;})) { throw new Error('Invalid result CSV schema'); }
  var g=readGradesSheet_(spreadsheet), target=columnIndexByHeader_(g.headers,columnName), rosterId=columnIndexByHeader_(g.headers,'student_id');
  if(target<0){throw new Error('Missing target grade column');}
  var rowOf={}, seen={}, marks=g.rows.map(function(r,i){
    var id=String(r[rosterId]).trim().toUpperCase();
    if(id&&rowOf[id]!==undefined){throw new Error('Duplicate roster ID '+id);}
    if(id){rowOf[id]=i;}return [r[target]];
  });
  var expected=markColumnMax_(columnName);
  rows.filter(function(r){return r.join('').trim();}).forEach(function(r){
    var id=String(r[sid]).trim().toUpperCase();
    if(seen[id]){throw new Error('Duplicate result '+id);}seen[id]=true;
    if(rowOf[id]===undefined){throw new Error('Result not on roster '+id);}
    if(['OK','ERRORS','AUTO_SCORED'].indexOf(r[status])<0){throw new Error('Unresolved result '+id+': '+r[status]);}
    if(r[score]===''||Number(r[maximum])!==expected){throw new Error('Missing mark or maximum mismatch '+id);}
    validateMark_(r[score],expected);
    if(columnName==='W01' && marks[rowOf[id]][0]!=='' && marks[rowOf[id]][0]!==null){return;}
    marks[rowOf[id]]=[Number(r[score])];
  });
  if(marks.length){g.sheet.getRange(2,target+1,marks.length,1).setValues(marks);}
}

/** Configure existing quiz IDs using an exported JSON object.
 * Keys: cohort|teachingWeek. Values: {formId, closeAt}. Never rebuild Forms.
 */
function configureQuizImports(sourcesJson) {
  var sources=JSON.parse(sourcesJson);
  Object.keys(sources).forEach(function(k){if(!sources[k].formId){throw new Error('Missing form ID '+k);} if(!sources[k].closeAt||!isFinite(Date.parse(sources[k].closeAt))){throw new Error('A valid quiz deadline is required '+k);}});
  PropertiesService.getScriptProperties().setProperty('QUIZ_IMPORT_SOURCES',JSON.stringify(sources));
}
function importQuizScores(spreadsheet) {
  var sources=JSON.parse(PropertiesService.getScriptProperties().getProperty('QUIZ_IMPORT_SOURCES')||'{}');
  if(!Object.keys(sources).length){throw new Error('Configure quiz import source IDs first.');}
  var g=readGradesSheet_(spreadsheet), sidCol=columnIndexByHeader_(g.headers,'student_id'), cohortCol=columnIndexByHeader_(g.headers,'cohort');
  var emailCol=columnIndexByHeader_(g.headers,'email'), roster={};
  if(sidCol<0||cohortCol<0||emailCol<0){throw new Error('Quiz imports require registration number, cohort and verified-account email columns.');}
  g.rows.forEach(function(r,i){var id=String(r[sidCol]).trim().toUpperCase();if(id){if(roster[id]!==undefined){throw new Error('Duplicate roster ID');}roster[id]=i;}});
  var weeks=[1,2,3,4,5,6,8,9,10,11,12,13], pending=[];
  Object.keys(sources).forEach(function(key){
    if(!sources[key].closeAt||!isFinite(Date.parse(sources[key].closeAt))){throw new Error('A valid quiz deadline is required '+key);}
    var parts=key.split('|'), week=Number(parts[1]), qi=weeks.indexOf(week)+1;
    if(qi===0){throw new Error('Unknown quiz week '+key);}
    var col=columnIndexByHeader_(g.headers,'Q'+qi), data=g.rows.map(function(r){return [r[col]];}), latest={};
    if(col<0){throw new Error('Missing quiz destination column Q'+qi);}
    FormApp.openById(sources[key].formId).getResponses().forEach(function(response){
      var at=response.getTimestamp().getTime();
      if(at>Date.parse(sources[key].closeAt)){return;}
      var id='';response.getItemResponses().forEach(function(ir){
        if(/student.*(number|id)|registration/i.test(ir.getItem().getTitle())){id=String(ir.getResponse()).trim().toUpperCase();}
      });
      if(roster[id]===undefined){throw new Error('Unknown quiz respondent '+id);}
      var r=g.rows[roster[id]];
      if(String(r[cohortCol]).trim()!==parts[0]){throw new Error('Quiz cohort mismatch '+id);}
      var email=response.getRespondentEmail();
      if(!r[emailCol]||!email||String(r[emailCol]).trim().toLowerCase()!==String(email).trim().toLowerCase()){throw new Error('Missing or mismatched verified email '+id);}
      var total=0,count=0;response.getGradableItemResponses().forEach(function(ir){
        if(ir.getItem().getType()!==FormApp.ItemType.MULTIPLE_CHOICE){return;}
        if(ir.getItem().asMultipleChoiceItem().getPoints()!==1){throw new Error('Quiz question must be worth one mark');}
        var v=ir.getScore();if(v!==0&&v!==1){throw new Error('Ungraded or invalid quiz item '+id);}total+=v;count++;
      });
      if(count!==5){throw new Error('Expected five graded quiz questions '+id);}
      validateMark_(total,5);
      if(!latest[id]||at>latest[id].at){latest[id]={at:at,score:total};}
    });
    Object.keys(latest).forEach(function(id){
      var existing=g.rows[roster[id]][col];
      if(week===1&&existing!==''&&existing!==null&&Number(existing)!==latest[id].score){throw new Error('Existing Week 1 quiz mark is protected '+id);}
      data[roster[id]]=[latest[id].score];
    });
    pending.push({col:col,data:data});
  });
  // Merge cohort-specific updates to the same quiz column before writing.
  var merged={};pending.forEach(function(p){
    if(!merged[p.col]){merged[p.col]=g.rows.map(function(r){return [r[p.col]];});}
    p.data.forEach(function(v,i){if(v[0]!==g.rows[i][p.col]){merged[p.col][i]=v;}});
  });
  Object.keys(merged).forEach(function(col){if(g.rows.length){g.sheet.getRange(2,Number(col)+1,g.rows.length,1).setValues(merged[col]);}});
}

// GRADEBOOK_PATCH_20261103: patched 3 November 2026 from data/assessment_blocks_20261103.json
// GRADEBOOK_POLICY_20261110: 20 + 20 + 20 + 40, provisional out of 60, from data/assessment_policy_20261110.json
