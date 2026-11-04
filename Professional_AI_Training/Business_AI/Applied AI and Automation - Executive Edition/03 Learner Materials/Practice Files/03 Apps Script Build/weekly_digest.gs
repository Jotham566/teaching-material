/**
 * weekly_digest.gs
 * KLAi | Applied AI and Automation | Session 8
 *
 * Reads a sheet of weekly sales, works out the totals and the week-on-week change
 * for each group (for example each region) in plain code, and saves a DRAFT email
 * in your Gmail. It never sends anything. You read the draft and send it yourself.
 *
 * Needs ai_helper.gs in the same project (shared helpers and the run log).
 * The AI is optional and only writes a three-sentence comment.
 *
 * Expected columns (as in weekly_sales.csv): week_start, region, product, units, revenue_ugx
 */

// ---------------------------------------------------------------------------
// CHANGE THESE THREE LINES to match your own sheet
// ---------------------------------------------------------------------------
var SALES_SHEET_NAME = 'weekly_sales';  // CHANGE 1: the name of the tab that holds your data
var GROUP_COLUMN = 'region';            // CHANGE 2: the heading of the column to group by
var VALUE_COLUMN = 'revenue_ugx';       // CHANGE 3: the heading of the column to add up

// ---------------------------------------------------------------------------
// Other settings
// ---------------------------------------------------------------------------
var PERIOD_COLUMN = 'week_start';       // heading of the column with the week (yyyy-mm-dd)
var DIGEST_DRY_RUN = true;              // true: calculate and log only, no draft. Set false to create the draft.
var USE_AI_COMMENTARY = false;          // true: ask Gemini for three sentences (sample data only)
var DIGEST_RECIPIENT = '';              // blank means your own address
var DIGEST_WEEKDAY = 'MONDAY';          // day the trigger runs
var DIGEST_HOUR = 7;                    // hour of the day (0 to 23) in your script time zone; Google runs the trigger at some point inside that hour (7 means between 7:00 and 8:00)

// ---------------------------------------------------------------------------
// Calculation (no AI, no Google services: easy to test)
// ---------------------------------------------------------------------------

/** Turns a cell into a yyyy-mm-dd text, whether Sheets gave a date or a text. */
function normaliseWeek(value) {
  if (Object.prototype.toString.call(value) === '[object Date]') {
    return Utilities.formatDate(value, Session.getScriptTimeZone(), 'yyyy-MM-dd');
  }
  return String(value).trim().slice(0, 10);
}

/** Builds the digest from a list of row objects: the totals for each week, and for the latest week the value of each group against the week before, with the change and percent change. */
function buildDigest(rows) {
  var byWeek = {};      // week -> group -> total
  var weekTotals = {};  // week -> total
  var skipped = 0;

  rows.forEach(function (row) {
    var week = normaliseWeek(row[PERIOD_COLUMN]);
    var group = String(row[GROUP_COLUMN]).trim();
    var value = toNumber(row[VALUE_COLUMN]);
    if (week === '' || group === '' || isNaN(value)) {
      skipped = skipped + 1;
      return;
    }
    if (!byWeek[week]) { byWeek[week] = {}; weekTotals[week] = 0; }
    byWeek[week][group] = (byWeek[week][group] || 0) + value;
    weekTotals[week] = weekTotals[week] + value;
  });

  var weeks = Object.keys(byWeek).sort();  // yyyy-mm-dd sorts in date order
  var digest = {
    weeks: weeks,
    latestWeek: weeks.length > 0 ? weeks[weeks.length - 1] : null,
    previousWeek: weeks.length > 1 ? weeks[weeks.length - 2] : null,
    weeklyTotals: weeks.map(function (w) { return { week: w, total: weekTotals[w] }; }),
    table: [],
    totalLatest: 0,
    totalPrevious: null,
    totalChange: null,
    totalChangePct: null,
    biggestRise: null,
    biggestFall: null,
    skippedRows: skipped
  };
  if (digest.latestWeek === null) {
    return digest;
  }

  var latest = byWeek[digest.latestWeek];
  var previous = digest.previousWeek ? byWeek[digest.previousWeek] : null;
  var groupNames = {};
  Object.keys(latest).forEach(function (g) { groupNames[g] = true; });
  if (previous) { Object.keys(previous).forEach(function (g) { groupNames[g] = true; }); }

  Object.keys(groupNames).forEach(function (g) {
    var now = latest[g] || 0;
    var before = previous ? (previous[g] || 0) : null;
    digest.table.push({
      group: g,
      latest: now,
      previous: before,
      change: before === null ? null : now - before,
      changePct: percentChange(now, before)
    });
  });
  digest.table.sort(function (a, b) { return b.latest - a.latest; });

  digest.totalLatest = weekTotals[digest.latestWeek];
  if (previous) {
    digest.totalPrevious = weekTotals[digest.previousWeek];
    digest.totalChange = digest.totalLatest - digest.totalPrevious;
    digest.totalChangePct = percentChange(digest.totalLatest, digest.totalPrevious);
    var withChange = digest.table.filter(function (t) { return t.change !== null; });
    withChange.sort(function (a, b) { return b.change - a.change; });
    if (withChange.length > 0) {
      digest.biggestRise = withChange[0].group;
      digest.biggestFall = withChange[withChange.length - 1].group;
    }
  }
  return digest;
}

/** Returns the percent change from before to now, rounded to one decimal, or null if before is missing or zero. */
function percentChange(now, before) {
  if (before === null || before === 0) {
    return null;
  }
  return Math.round(((now - before) / before) * 1000) / 10;
}

/** Writes a change as text, for example "+1,200 (+4.5%)" or "n/a". */
function describeChange(change, pct) {
  if (change === null) { return 'n/a'; }
  var sign = change > 0 ? '+' : '';
  var pctText = pct === null ? 'n/a' : sign + pct.toFixed(1) + '%';
  return sign + formatNumber(change) + ' (' + pctText + ')';
}

/** Builds the plain-text body of the draft email from the digest and an optional comment. */
function buildEmailBody(digest, commentary) {
  var lines = [];
  lines.push('Weekly sales digest (DRAFT for your review)');
  lines.push('');
  if (digest.latestWeek === null) {
    lines.push('No usable rows were found in the sheet.');
    return lines.join('\n');
  }
  lines.push('Latest week starting: ' + digest.latestWeek);
  lines.push('Compared with: ' + (digest.previousWeek ? digest.previousWeek : 'no earlier week in the data'));
  lines.push('');
  lines.push(GROUP_COLUMN + ' | this week | last week | change');
  digest.table.forEach(function (t) {
    lines.push(t.group + ' | ' + formatNumber(t.latest) + ' | ' +
      (t.previous === null ? 'n/a' : formatNumber(t.previous)) + ' | ' +
      describeChange(t.change, t.changePct));
  });
  lines.push('TOTAL | ' + formatNumber(digest.totalLatest) + ' | ' +
    (digest.totalPrevious === null ? 'n/a' : formatNumber(digest.totalPrevious)) + ' | ' +
    describeChange(digest.totalChange, digest.totalChangePct));
  lines.push('');
  lines.push('Total for every week in the sheet (week starting | total):');
  digest.weeklyTotals.forEach(function (w) {
    lines.push(w.week + ' | ' + formatNumber(w.total));
  });
  if (digest.biggestRise) {
    lines.push('');
    lines.push('Biggest rise: ' + digest.biggestRise + '. Biggest fall: ' + digest.biggestFall + '.');
  }
  if (digest.skippedRows > 0) {
    lines.push('');
    lines.push('Rows skipped because a week, group or value was missing: ' + digest.skippedRows);
  }
  if (commentary) {
    lines.push('');
    lines.push('AI comment (written by an AI model from the table above; check it before you use it):');
    lines.push(commentary);
  }
  lines.push('');
  lines.push('All figures above were calculated by the script from your sheet.');
  return lines.join('\n');
}

/** Builds the instruction that asks the AI for a three-sentence comment on the table (aggregates only). */
function buildCommentaryPrompt(digest) {
  var lines = digest.table.map(function (t) {
    return t.group + ': this week ' + formatNumber(t.latest) + ', last week ' +
      (t.previous === null ? 'n/a' : formatNumber(t.previous)) + ', change ' + describeChange(t.change, t.changePct);
  });
  return 'You are helping a manager read a weekly sales table. Write exactly three sentences. ' +
    'Use only the numbers below. Do not guess causes. Do not give advice.\n\n' + lines.join('\n') +
    '\nTotal this week: ' + formatNumber(digest.totalLatest);
}

// ---------------------------------------------------------------------------
// The run (talks to Google services)
// ---------------------------------------------------------------------------

/** Main function: reads the sheet, builds the digest, logs the run and (unless dry run) saves a Gmail draft. */
function createWeeklyDigest() {
  var mode = DIGEST_DRY_RUN ? 'dry-run' : 'live';
  resetAiCallCount();
  try {
    var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = spreadsheet.getSheetByName(SALES_SHEET_NAME);
    if (!sheet) {
      throw new Error('There is no sheet named "' + SALES_SHEET_NAME + '". Check CHANGE 1 at the top of weekly_digest.gs.');
    }
    var rows = valuesToObjects(sheet.getDataRange().getValues());
    if (rows.length > 0 && rows[0][GROUP_COLUMN] === undefined) {
      throw new Error('There is no column headed "' + GROUP_COLUMN + '". Check CHANGE 2.');
    }
    if (rows.length > 0 && rows[0][VALUE_COLUMN] === undefined) {
      throw new Error('There is no column headed "' + VALUE_COLUMN + '". Check CHANGE 3.');
    }
    var digest = buildDigest(rows);

    var commentary = '';
    var aiNote = 'AI off';
    if (USE_AI_COMMENTARY && !DIGEST_DRY_RUN) {
      var answer = askGemini(buildCommentaryPrompt(digest), {});
      if (answer.ok) {
        commentary = answer.text;
        aiNote = 'AI comment added';
      } else {
        aiNote = 'AI skipped (' + answer.reason + ')';
      }
    } else if (USE_AI_COMMENTARY && DIGEST_DRY_RUN) {
      aiNote = 'AI not called in dry run';
    }

    var body = buildEmailBody(digest, commentary);
    var summary = 'Rows read: ' + rows.length + '. Latest week: ' + digest.latestWeek +
      '. Total: ' + formatNumber(digest.totalLatest) + '. ' + aiNote + '.';

    if (DIGEST_DRY_RUN) {
      Logger.log(body);
      logRun('createWeeklyDigest', mode, summary + ' No draft created.');
      return body;
    }

    var to = DIGEST_RECIPIENT || Session.getEffectiveUser().getEmail();
    GmailApp.createDraft(to, 'Weekly sales digest (draft): week of ' + digest.latestWeek, body);  // draft only, never sends
    logRun('createWeeklyDigest', mode, summary + ' Draft saved in Gmail.');
    return body;
  } catch (err) {
    logRun('createWeeklyDigest', 'error', err.message);
    throw err;
  }
}

/** Run once: makes ONE weekly trigger for createWeeklyDigest (replacing any older one). Turn it off with turnEverythingOff. */
function setupWeeklyTrigger() {
  var existing = ScriptApp.getProjectTriggers();
  for (var i = 0; i < existing.length; i++) {
    if (existing[i].getHandlerFunction() === 'createWeeklyDigest') {
      ScriptApp.deleteTrigger(existing[i]);
    }
  }
  ScriptApp.newTrigger('createWeeklyDigest')
    .timeBased()
    .onWeekDay(ScriptApp.WeekDay[DIGEST_WEEKDAY])
    .atHour(DIGEST_HOUR)
    .create();
  logRun('setupWeeklyTrigger', 'live', 'One trigger set: createWeeklyDigest every ' + DIGEST_WEEKDAY + ', running between ' + DIGEST_HOUR + ':00 and ' + ((DIGEST_HOUR + 1) % 24) + ':00.');
}
