/**
 * ai_helper.gs
 * KLAi | Applied AI and Automation | Session 8
 *
 * Shared helpers for the three scripts in this project:
 *   1. A safe wrapper for ONE call to the Gemini API (askGemini, askGeminiAboutRows).
 *   2. The run log, the off switch and a few small sheet helpers.
 *
 * All arithmetic and all flagging in this project is done by plain code in
 * weekly_digest.gs and invoice_check.gs. The AI is used only for an optional
 * three-sentence comment. If the AI is off, unavailable or refused, the
 * scripts still work.
 *
 * USE ONLY FAKE OR SAMPLE DATA with a free Gemini key. Content sent on the free
 * tier may be used by Google to improve its products.
 */

// ---------------------------------------------------------------------------
// Settings you may change
// ---------------------------------------------------------------------------

// Model name. Google renames and retires models, so this is the line to change
// if a call fails with "model not found". Check the current names in Google AI Studio.
var GEMINI_MODEL = 'gemini-2.5-flash';

// Start of the Gemini REST address. The full address is this text, then the
// model name, then ":generateContent". INSTRUCTOR: confirm this format against
// the current Gemini API documentation before teaching.
var GEMINI_BASE_URL = 'https://generativelanguage.googleapis.com/v1beta/models/';

// The name under which you store the key in Project Settings > Script Properties.
var KEY_PROPERTY_NAME = 'GEMINI_API_KEY';

// The most AI calls one run may make. Stops loops from spending your quota.
var AI_MAX_CALLS_PER_RUN = 3;

// The most rows, and the most characters, one call may carry.
var AI_MAX_ROWS = 50;
var AI_MAX_PROMPT_CHARS = 8000;

// If a row has "yes" (or true, y, 1) in this column, it is never sent to the AI.
var PERSONAL_DATA_COLUMN = 'contains_personal_data';

// Sheet where every run is recorded.
var RUN_LOG_SHEET_NAME = 'Run log';

// Counts the AI calls made so far in this run. Apps Script starts it at 0 each run.
var AI_CALLS_THIS_RUN = 0;

// ---------------------------------------------------------------------------
// The AI wrapper
// ---------------------------------------------------------------------------

/** Sets the call counter back to zero (used at the start of a run and in tests). */
function resetAiCallCount() {
  AI_CALLS_THIS_RUN = 0;
}

/** Returns true if the text contains an email address, a Ugandan phone number or a national ID number. */
function looksLikePersonalData(text) {
  var s = String(text);
  var emailPattern = /[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}/;
  var phonePattern = /(?:\+?256|\b0)[\s\-]?[37]\d{2}[\s\-]?\d{3}[\s\-]?\d{3}\b/;
  var ninPattern = /\b(?:CM|CF)[0-9A-Z]{12}\b/i;
  return emailPattern.test(s) || phonePattern.test(s) || ninPattern.test(s);
}

/** Returns true if a cell value means "yes" (yes, y, true, 1). */
function isYesValue(value) {
  var v = String(value).trim().toLowerCase();
  return v === 'yes' || v === 'y' || v === 'true' || v === '1';
}

/** Sends one prompt to Gemini and returns {ok, text, reason}. Set options.containsPersonalData to true to make the helper refuse the call. It also refuses text that looks like personal data, stops at the call limit, and never throws: the caller checks result.ok. */
function askGemini(promptText, options) {
  var opts = options || {};

  if (opts.containsPersonalData === true) {
    return { ok: false, text: '', reason: 'refused: data is flagged as personal data' };
  }
  var text = String(promptText);
  if (looksLikePersonalData(text)) {
    return { ok: false, text: '', reason: 'refused: text looks like personal data (email, phone or ID number)' };
  }
  if (text.length > AI_MAX_PROMPT_CHARS) {
    return { ok: false, text: '', reason: 'refused: prompt is longer than ' + AI_MAX_PROMPT_CHARS + ' characters' };
  }
  if (AI_CALLS_THIS_RUN >= AI_MAX_CALLS_PER_RUN) {
    return { ok: false, text: '', reason: 'refused: call limit of ' + AI_MAX_CALLS_PER_RUN + ' reached for this run' };
  }

  // The key lives in Script Properties, never in the code.
  var key = PropertiesService.getScriptProperties().getProperty(KEY_PROPERTY_NAME);
  if (!key) {
    return { ok: false, text: '', reason: 'no key: add ' + KEY_PROPERTY_NAME + ' in Project Settings > Script Properties' };
  }

  // Count the call before making it, so a crash cannot hide a call.
  AI_CALLS_THIS_RUN = AI_CALLS_THIS_RUN + 1;

  var url = GEMINI_BASE_URL + GEMINI_MODEL + ':generateContent';
  var body = {
    contents: [{ parts: [{ text: text }] }],
    generationConfig: { temperature: 0.2, maxOutputTokens: 600 }
  };
  var request = {
    method: 'post',
    contentType: 'application/json',
    headers: { 'x-goog-api-key': key },   // the key travels in a header and stays out of the address
    payload: JSON.stringify(body),
    muteHttpExceptions: true               // lets us read error replies instead of crashing
  };

  // Timeout: UrlFetchApp has no setting to shorten its wait, so plan for about
  // 20 seconds per call. We measure the time and log a warning if it is slower.
  // Apps Script stops the whole run at 6 minutes.
  var started = new Date().getTime();
  var response;
  try {
    response = UrlFetchApp.fetch(url, request);
  } catch (err) {
    return { ok: false, text: '', reason: 'fetch failed: ' + err.message };
  }
  var seconds = (new Date().getTime() - started) / 1000;
  if (seconds > 20) {
    Logger.log('Warning: the AI call took ' + seconds + ' seconds. Consider stopping the AI step.');
  }

  var code = response.getResponseCode();
  var raw = response.getContentText();
  if (code !== 200) {
    // Show the status and the start of the reply. The key is never part of it.
    return { ok: false, text: '', reason: 'http ' + code + ': ' + String(raw).slice(0, 200) };
  }

  var data;
  try {
    data = JSON.parse(raw);
  } catch (parseErr) {
    return { ok: false, text: '', reason: 'reply was not valid JSON' };
  }
  var answer = '';
  if (data && data.candidates && data.candidates.length > 0) {
    var content = data.candidates[0].content;
    if (content && content.parts) {
      for (var i = 0; i < content.parts.length; i++) {
        if (content.parts[i].text) {
          answer = answer + content.parts[i].text;
        }
      }
    }
  }
  if (!answer) {
    return { ok: false, text: '', reason: 'reply had no text (it may have been blocked)' };
  }
  return { ok: true, text: answer.trim(), reason: '' };
}

/** Sends an instruction plus a list of row objects to Gemini. Refuses if any row is flagged "yes" in PERSONAL_DATA_COLUMN, or has too many rows. */
function askGeminiAboutRows(instruction, rows) {
  var list = rows || [];
  if (list.length > AI_MAX_ROWS) {
    return { ok: false, text: '', reason: 'refused: more than ' + AI_MAX_ROWS + ' rows' };
  }
  for (var i = 0; i < list.length; i++) {
    if (isYesValue(list[i][PERSONAL_DATA_COLUMN])) {
      return { ok: false, text: '', reason: 'refused: row ' + (i + 1) + ' is flagged as personal data' };
    }
  }
  return askGemini(instruction + '\n\n' + JSON.stringify(list), {});
}

// ---------------------------------------------------------------------------
// Shared helpers: run log, off switch, small sheet tools
// ---------------------------------------------------------------------------

/** Returns the sheet with this name, creating it if it does not exist. */
function getOrCreateSheet(spreadsheet, name) {
  var sheet = spreadsheet.getSheetByName(name);
  if (!sheet) {
    sheet = spreadsheet.insertSheet(name);
  }
  return sheet;
}

/** Adds one line to the 'Run log' sheet: time, script, mode (dry-run, live, error) and a summary. */
function logRun(scriptName, mode, summary) {
  var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = getOrCreateSheet(spreadsheet, RUN_LOG_SHEET_NAME);
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(['time', 'script', 'mode', 'summary']);
  }
  sheet.appendRow([new Date(), scriptName, mode, summary]);
  Logger.log(scriptName + ' | ' + mode + ' | ' + summary);
}

/** THE OFF SWITCH: deletes every trigger in this project and returns how many it removed. */
function turnEverythingOff() {
  var triggers = ScriptApp.getProjectTriggers();
  for (var i = 0; i < triggers.length; i++) {
    ScriptApp.deleteTrigger(triggers[i]);
  }
  logRun('turnEverythingOff', 'live', 'Removed ' + triggers.length + ' trigger(s). Nothing will run by itself now.');
  return triggers.length;
}

/** Turns the rows of a sheet (a 2D array with headings in row 1) into a list of objects keyed by heading. */
function valuesToObjects(values) {
  var out = [];
  if (!values || values.length < 2) {
    return out;
  }
  var headers = values[0].map(function (h) { return String(h).trim(); });
  for (var r = 1; r < values.length; r++) {
    var obj = {};
    for (var c = 0; c < headers.length; c++) {
      obj[headers[c]] = values[r][c];
    }
    out.push(obj);
  }
  return out;
}

/** Reads a number from a cell. Accepts 1500, "1,500" and "UGX 1,500". Returns NaN if it is blank or not a number. */
function toNumber(value) {
  if (typeof value === 'number') {
    return value;
  }
  var s = String(value === null || value === undefined ? '' : value).replace(/UGX/gi, '').replace(/[,\s]/g, '');
  if (s === '') {
    return NaN;
  }
  return Number(s);
}

/** Writes a number with thousands separators, for example 1234567 becomes "1,234,567". */
function formatNumber(n) {
  var rounded = Math.round(n);
  var sign = rounded < 0 ? '-' : '';
  return sign + String(Math.abs(rounded)).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}
