/**
 * gradebook.gs - Google Apps Script gradebook for CML3111 / CML3112 / CML3113.
 * Revised September 2026 for the current weights.
 *
 *   Weekly quizzes             10 %   best 10 of 12, each out of 5
 *   Weekly challenges          10 %   best 8 of 11, each out of 20
 *   Data Analysis Project      10 %
 *   Practical Test 1           15 %
 *   Practical Test 2           20 %
 *   Engineering ML Project     25 %
 *   Demo / viva / reflection   10 %
 *                             ----
 *                             100 %
 *
 * What is here:
 *   recomputeAll()        weighted totals, best-of rules, missing flags
 *   ingestTokenCsv()      read a Form token export, verify each signature,
 *                         write the verified mark into the right challenge
 *                         column, and log everything that failed
 *   progressSummary()     the Coursera-style "you have completed 7 of 11" line
 *   emailStandings()      one email per student, resumable across days
 *
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
  quizzes: 10,
  challenges: 10,
  dataProject: 10,
  test1: 15,
  test2: 20,
  mlProject: 25,
  demo: 10
};

var QUIZ_COUNT = 12;           // Weeks 1-6 and 8-13
var QUIZ_BEST = 10;            // the two lowest are dropped; there are no resits
var QUIZ_MAX = 5;              // marks per quiz, one per question

var CHALLENGE_COUNT = 11;      // Weeks 1–6 and 8–12, A1–A11
var CHALLENGE_BEST = 8;
var CHALLENGE_MAX = 20;        // marks per weekly challenge

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

/** Sum of the best n entries of a list, ignoring blanks and non-numbers. */
function bestNOf_(scores, n) {
  var clean = [];
  for (var i = 0; i < scores.length; i++) {
    var v = scores[i];
    if (v === "" || v === null || v === undefined) { continue; }
    var f = Number(v);
    if (isNaN(f)) { continue; }
    clean.push(f);
  }
  clean.sort(function (a, b) { return b - a; });
  var taken = clean.slice(0, n);
  var total = 0;
  for (var j = 0; j < taken.length; j++) { total += taken[j]; }
  return { total: total, counted: taken.length, submitted: clean.length };
}

/**
 * A best-of component as a percentage of the whole course.
 * Marks not yet earned count as zero, which is the whole point of the rule:
 * a student who skips three challenges is not penalised, one who skips six is.
 */
function bestOfComponent_(scores, best, perItemMax, weight) {
  scores.forEach(function (v) { validateMark_(v, perItemMax); });
  var b = bestNOf_(scores, best);
  var denom = best * perItemMax;
  var fraction = denom > 0 ? b.total / denom : 0;
  return {
    weighted: round2_(fraction * weight),
    outOf: weight,
    counted: b.counted,
    submitted: b.submitted,
    raw: b.total,
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
  var f = Number(mark) / (outOf || 100);
  return { weighted: round2_(f * weight), outOf: weight, missing: false,
           raw: Number(mark) };
}

function round2_(x) { return Math.round(x * 100) / 100; }

/**
 * Everything for one student.
 * row: { quizzes: [], challenges: [], dataProject, test1, test2,
 *        mlProject, demo }  - marks out of 100 for the four big components.
 */
/** A6/Q6 are not assigned to these cohorts. Keep the same drop allowance. */
function courseworkPolicy_(cohort) {
  var waived = ['CML3112','CML3113'].indexOf(String(cohort||'').trim().toUpperCase()) >= 0;
  return {waived:waived,quizBest:QUIZ_BEST-(waived?1:0),challengeBest:CHALLENGE_BEST-(waived?1:0),
          quizCount:QUIZ_COUNT-(waived?1:0),challengeCount:CHALLENGE_COUNT-(waived?1:0)};
}
function assignedScores_(scores, policy) {
  return (scores||[]).filter(function(v,i){return !policy.waived || i!==5;});
}
function computeFinal_(row) {
  var policy=courseworkPolicy_(row.cohort);
  var cp = bestOfComponent_(assignedScores_(row.quizzes,policy), policy.quizBest,
                            QUIZ_MAX, WEIGHTS.quizzes);
  var ch = bestOfComponent_(assignedScores_(row.challenges,policy), policy.challengeBest,
                            CHALLENGE_MAX, WEIGHTS.challenges);
  var dp = percentComponent_(row.dataProject, 100, WEIGHTS.dataProject);
  var t1 = percentComponent_(row.test1, 100, WEIGHTS.test1);
  var t2 = percentComponent_(row.test2, 100, WEIGHTS.test2);
  var pr = percentComponent_(row.mlProject, 100, WEIGHTS.mlProject);
  var dm = percentComponent_(row.demo, 100, WEIGHTS.demo);

  var missing = [];
  if (dp.missing) { missing.push("Data Analysis Project"); }
  if (t1.missing) { missing.push("Practical Test 1"); }
  if (t2.missing) { missing.push("Practical Test 2"); }
  if (pr.missing) { missing.push("ML Project"); }
  if (dm.missing) { missing.push("Demo/viva"); }
  if (cp.submitted < policy.quizBest) {
    missing.push("quizzes: " + cp.submitted + " of " + policy.quizBest +
                 " that count");
  }
  if (ch.submitted < policy.challengeBest) {
    missing.push("challenges: " + ch.submitted + " of " + policy.challengeBest +
                 " that count");
  }

  var final = round2_(cp.weighted + ch.weighted + dp.weighted + t1.weighted +
                      t2.weighted + pr.weighted + dm.weighted);
  return {
    components: { quizzes: cp, challenges: ch, dataProject: dp,
                  test1: t1, test2: t2, mlProject: pr, demo: dm },
    final: final,
    band: gradeBand_(final),
    missing: missing
  };
}

function gradeBand_(pct) {
  for (var i = 0; i < GRADE_BANDS.length; i++) {
    if (pct >= GRADE_BANDS[i][0]) { return GRADE_BANDS[i][1]; }
  }
  return "F";
}

/** Total of the seven weights. Should always be 100; the tests assert it. */
function weightTotal_() {
  var t = 0;
  for (var k in WEIGHTS) { if (WEIGHTS.hasOwnProperty(k)) { t += WEIGHTS[k]; } }
  return t;
}

/** The student-facing progress line. */
function progressSummary_(row) {
  var policy=courseworkPolicy_(row.cohort);
  var res = computeFinal_(row);
  var ch = res.components.challenges;
  var cp = res.components.quizzes;
  var lines = [];
  lines.push("You have completed " + ch.submitted + " of " + policy.challengeCount +
             " weekly challenges. The best " + policy.challengeBest + " count.");
  if (ch.submitted < policy.challengeBest) {
    lines.push("You need " + (policy.challengeBest - ch.submitted) + " more before " +
               "this part of your mark stops being capped.");
  } else {
    lines.push("You have enough for this part of your mark to count in full.");
  }
  lines.push("You have sat " + cp.submitted + " of " + policy.quizCount +
             " weekly quizzes. The best " + policy.quizBest + " count.");
  lines.push("Marks banked so far: " + res.final + " of 100.");
  if (res.missing.length) {
    lines.push("Not yet recorded: " + res.missing.join("; ") + ".");
  }
  if(policy.waived)lines.push("A6 and Quiz 6: not assigned; excluded from totals and missing work.");
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
    .addItem("Recompute all totals", "recomputeAll")
    .addItem("Ingest submission codes...", "ingestTokenCsv")
    .addItem("Show my progress line for the selected row", "showProgress")
    .addSeparator()
    .addItem("Email standings (resumable)", "emailStandings")
    .addToUi();
}

function readGradesSheet_(spreadsheet) {
  var sh = (spreadsheet||SpreadsheetApp.getActive()).getSheetByName(GRADER_SHEET);
  if (!sh) { throw new Error("No sheet called '" + GRADER_SHEET + "'."); }
  var values = sh.getDataRange().getValues();
  var required = ["student_id"].concat(CHALLENGE_IDS);
  for (var q = 1; q <= QUIZ_COUNT; q++) { required.push("Q" + q); }
  var missing = required.filter(function (h) { return columnIndexByHeader_(values[0], h) < 0; });
  if (missing.length) { throw new Error("Grades sheet missing columns: " + missing.join(", ")); }
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
    dataProject: get("Data Analysis Project"),
    test1: get("Practical Test 1"),
    test2: get("Practical Test 2"),
    mlProject: get("ML Project"),
    demo: get("Demo")
  };
}

function recomputeAll() {
  var g = readGradesSheet_();
  var iFinal = columnIndexByHeader_(g.headers, "Final %");
  var iBand = columnIndexByHeader_(g.headers, "Band");
  var iMiss = columnIndexByHeader_(g.headers, "Missing");
  var iDone = columnIndexByHeader_(g.headers, "Challenges done");
  if (iFinal < 0) {
    throw new Error("Add a column headed 'Final %' to the Grades sheet.");
  }
  var out = [];
  for (var r = 0; r < g.rows.length; r++) {
    var rec = rowToRecord_(g.headers, g.rows[r]);
    if (!rec.studentId) { out.push(null); continue; }
    var res = computeFinal_(rec);
    var line = g.rows[r].slice();
    line[iFinal] = res.final;
    if (iBand >= 0) { line[iBand] = GRADE_BANDS_VERIFIED ? res.band : 'Awaiting Faculty bands'; }
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

  // ---- weights ----
  eq("weights total 100", weightTotal_(), 100);

  // ---- bestNOf_ ----
  eq("bestNOf_ picks the top 4",
     bestNOf_([10, 2, 8, 6, 4], 4), { total: 28, counted: 4, submitted: 5 });
  eq("bestNOf_ ignores blanks",
     bestNOf_([10, "", 8, null, undefined], 4),
     { total: 18, counted: 2, submitted: 2 });
  eq("bestNOf_ ignores text",
     bestNOf_([10, "absent", 5], 4), { total: 15, counted: 2, submitted: 2 });
  eq("bestNOf_ on nothing", bestNOf_([], 4),
     { total: 0, counted: 0, submitted: 0 });
  eq("bestNOf_ with fewer than n", bestNOf_([7], 4),
     { total: 7, counted: 1, submitted: 1 });
  eq("bestNOf_ handles a zero score", bestNOf_([0, 0, 0, 0, 0], 4),
     { total: 0, counted: 4, submitted: 5 });

  // ---- best-of components ----
  var cpFull = bestOfComponent_([5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], 10, 5, 10);
  near("quizzes all full -> 10%", cpFull.weighted, 10);
  var cpDrop = bestOfComponent_([5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0], 10, 5, 10);
  near("quizzes best 10 of 12 drops the two zeros", cpDrop.weighted, 10);
  var cpHalf = bestOfComponent_([2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5,
                                 2.5, 2.5], 10, 5, 10);
  near("quizzes all half -> 5%", cpHalf.weighted, 5);
  var cpEight = bestOfComponent_([5, 5, 5, 5, 5, 5, 5, 5], 10, 5, 10);
  near("only 8 quizzes of 12 sat -> 8%", cpEight.weighted, 8);
  var chFull = bestOfComponent_([20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20],
                                8, 20, 10);
  near("challenges all full -> 10%", chFull.weighted, 10);
  var chNine = bestOfComponent_([20, 20, 20, 20, 20, 20, 20, 20, 0, 0, 0],
                                8, 20, 10);
  near("challenges best 8 of 11 ignores three zeroes", chNine.weighted, 10);
  var chSix = bestOfComponent_([20, 20, 20, 20, 20, 20], 8, 20, 10);
  near("six challenges of 11 -> 7.5%", chSix.weighted, 7.5);
  eq("challenges counts submissions", chSix.submitted, 6);

  // ---- percentComponent_ ----
  near("test1 at 60/100 -> 9 of 15", percentComponent_(60, 100, 15).weighted, 9);
  ok("blank test flagged missing", percentComponent_("", 100, 15).missing);
  var rejectedText=false;
  try{percentComponent_("absent",100,15);}catch(e){rejectedText=true;}
  ok("text in a test cell is rejected",rejectedText);
  near("blank test scores 0", percentComponent_("", 100, 15).weighted, 0);

  // ---- computeFinal_ ----
  var perfect = computeFinal_({
    quizzes: [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    challenges: [20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20],
    dataProject: 100, test1: 100, test2: 100, mlProject: 100, demo: 100
  });
  near("perfect student -> 100", perfect.final, 100);
  eq("perfect student has nothing missing", perfect.missing, []);
  var half = computeFinal_({
    quizzes: [2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5],
    challenges: [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
    dataProject: 50, test1: 50, test2: 50, mlProject: 50, demo: 50
  });
  near("half marks everywhere -> 50", half.final, 50);
  var empty = computeFinal_({});
  near("empty row -> 0", empty.final, 0);
  ok("empty row lists 7 things missing", empty.missing.length === 7,
     JSON.stringify(empty.missing));
  var midterm = computeFinal_({
    quizzes: [4, 5, 3, 5, "", "", "", "", "", "", "", ""],
    challenges: [16, 18, 14, 20, "", "", "", "", "", "", ""],
    dataProject: 72, test1: 65, test2: "", mlProject: "", demo: ""
  });
  // quizzes best10 of [4,5,3,5] = 17/50 -> 3.4 ; ch best8 of [16,18,14,20] = 68/160 -> 4.25
  // dp 7.2 ; t1 9.75 ; rest 0
  near("mid-semester student", midterm.final, 3.4 + 4.25 + 7.2 + 9.75);
  ok("mid-semester student flagged for test 2",
     midterm.missing.indexOf("Practical Test 2") >= 0);

  // ---- gradeBand_ ----
  eq("band 85 -> A", gradeBand_(85), "A");
  eq("band 80 -> A on the boundary", gradeBand_(80), "A");
  eq("band 79.99 -> B+", gradeBand_(79.99), "B+");
  eq("band 0 -> F", gradeBand_(0), "F");

  // ---- progressSummary_ ----
  var line = progressSummary_({
    quizzes: [4, 5, 3, 5, 4, "", "", "", "", "", "", ""],
    challenges: [16, 18, 14, 20, 12, 15, 19, "", "", "", ""]
  });
  ok("progress line counts 7 of 11",
     line.indexOf("completed 7 of 11") >= 0, line);
  ok("progress line says one more needed",
     line.indexOf("need 1 more") >= 0, line);
  ok("progress line counts quizzes sat",
     line.indexOf("sat 5 of 12") >= 0, line);
  var line2 = progressSummary_({
    quizzes: [4, 5, 3, 5, 4, 5, 4, 3, "", "", "", ""],
    challenges: [16, 18, 14, 20, 12, 15, 19, 11, "", "", ""]
  });
  ok("progress line stops nagging at 8",
     line2.indexOf("count in full") >= 0, line2);

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

/** Import lecturer-side results by roster ID, atomically after validation.
 * CSV must contain student_id,status plus score,maximum (artifact grader)
 * or notebook_total,max_total (isolated notebook grader). No token-only rows.
 */
function importMarkedResults(fileId, columnName, spreadsheet) {
  var allowed=CHALLENGE_IDS.concat(['Data Analysis Project','Practical Test 1','Practical Test 2','ML Project','Demo']);
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
  var expected=CHALLENGE_IDS.indexOf(columnName)>=0?20:100;
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
