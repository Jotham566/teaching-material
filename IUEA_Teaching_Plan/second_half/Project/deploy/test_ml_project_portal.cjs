// Offline proof of the deployment bundle, modelled on tests/test_timed_takehome.cjs (same fakes for Sheets, Drive and Forms).
// usage (from anywhere): node IUEA_Teaching_Plan/second_half/Project/deploy/test_ml_project_portal.cjs [path to write one issued notebook as JSON]
const fs = require('fs'), path = require('path'), vm = require('vm'), assert = require('assert/strict'), crypto = require('crypto');
const deploy = __dirname;
const out = process.argv[2];
let now = Date.parse('2026-11-22T20:59:00Z'), rows = [['headers']], fileCount = 0, driveCalls = [], props = {};
let windowKey = 'CML3112|ML_PROJECT', windowRow = null;
const open = '2026-11-22T21:00:00Z', close = '2026-11-25T20:59:00Z';   // 23 November 00:00 to 25 November 23:59 Kampala, the confirmed window
const H3 = 180 * 60000;
class Clock extends Date { constructor(x) { super(x === undefined ? now : x); } static now() { return now; } }
const range = (row, col = 1, height = 1, width = 1) => ({
  getValues: () => rows.slice(row - 1, row - 1 + height).map(r => r.slice(col - 1, col - 1 + width)),
  setValues(v) { v.forEach((r, i) => { rows[row - 1 + i] ??= []; r.forEach((x, j) => rows[row - 1 + i][col - 1 + j] = x); }); },
  setRichTextValues(v) { this.setValues(v); }, setValue(v) { this.setValues([[v]]); } });
const sheet = { getDataRange: () => ({ getValues: () => rows }), getLastRow: () => rows.length, getRange: range };
let windowRows = [['key', 'open', 'close', 'enabled', 'duration'], [windowKey, open, close, 'YES', 180]];
const windowSheet = { getDataRange: () => ({ getValues: () => windowRows }), getLastRow: () => windowRows.length, appendRow: r => windowRows.push(r),
  getRange: (r, c, h, w) => ({ setValues: v => { v.forEach((row, i) => row.forEach((x, j) => { windowRows[r - 1 + i][c - 1 + j] = x; })); }, setNumberFormat() {} }) };
let receipts = [['headers']];
const book = { getSheetByName: n => n === 'Collection' ? { getDataRange: () => ({ getValues: () => receipts }) } : n === 'Test windows' ? windowSheet : n === 'Test allocations' ? sheet : null };
const formsMade = [];
const chain = () => new Proxy(function () {}, { get: (t, k) => k === 'getId' ? () => 'id-' + Math.random() : k === 'getPublishedUrl' ? () => 'https://forms/viewform' : k === 'toPrefilledUrl' ? () => 'https://forms/viewform?x=PLACEHOLDER' : () => chain(), apply: () => chain() });
const ctx = { Date: Clock, Math, JSON, console, Object, Array, Error, Number, String, isFinite, parseInt,
  SpreadsheetApp: { openById: () => book, newRichTextValue: () => ({ setText(v) { this.v = v; return this; }, build() { return this.v; } }) },
  LockService: { getScriptLock: () => ({ tryLock: () => true, waitLock() {}, releaseLock() {} }) },
  PropertiesService: { getScriptProperties: () => ({ getProperty: k => props[k], setProperty: (k, v) => props[k] = v }) },
  Utilities: { getUuid: () => 'synthetic-code', formatDate: d => d.toISOString(), newBlob: b => b },
  ScriptApp: { getOAuthToken: () => 'never-real', newTrigger: () => ({ forForm: () => ({ onFormSubmit: () => ({ create() {} }) }) }) },
  UrlFetchApp: { fetch: (url, options) => { driveCalls.push({ url, options }); return { getResponseCode: () => 200 }; } },
  FormApp: { create: title => { formsMade.push(title); return chain(); }, DestinationType: { SPREADSHEET: 1 }, ItemType: { TEXT: 2 } },
  HtmlService: { createHtmlOutput: m => ({ message: m }), createTemplateFromFile: f => ({ evaluate() { const o = { file: f, title: '', setTitle(t) { o.title = t; return o; }, addMetaTag() { return o; } }; return o; } }) },
  DriveApp: { createFolder: () => ({ getId: () => 'private-folder' }), getFolderById: () => ({ createFile: () => { const id = 'file-' + (++fileCount); return { getId: () => id }; } }) } };
vm.createContext(ctx);
for (const f of ['Portal.gs', 'PacketsMLProject.gs', 'exam_collection.gs', 'ml_project_collection.gs']) vm.runInContext(fs.readFileSync(path.join(deploy, f), 'utf8'), ctx);
vm.runInContext("var PORTAL_PACKETS = {};", ctx);   // the Test 1 packets are not needed here: the project lookup must work without them
const input = { test: windowKey, registration: 'DEMO / ML 1', email: 'synthetic@example.com', name: 'Synthetic learner' };

// 1. before the window, after the window, wrong keys
assert.throws(() => ctx.requestTestFiles(input), /opens on/);
now = Date.parse(close) + 1000; assert.throws(() => ctx.requestTestFiles(input), /closed/);
assert.throws(() => ctx.requestTestFiles({ ...input, test: 'CML3112|ML_PROJECTX' }), /Use your lecturer/);
assert.throws(() => ctx.requestTestFiles({ ...input, test: 'CML3112|TEST9' }), /Use your lecturer/);
assert.equal(ctx.doGet({ parameter: { test: 'CML3112|ML_PROJECT' } }).title, 'CML3112 ML_PROJECT test files');
assert.match(ctx.doGet({ parameter: { test: 'CML3112|ML_PROJECTX' } }).message, /Use the test link/);

// 2. the personal deadline is the earlier of start + 180 minutes and the window's close
rows = [['headers']]; now = Date.parse('2026-11-24T06:00:00Z');
let result = ctx.requestTestFiles(input);
assert.equal(result.personalDeadline, new Date(now + H3).toISOString(), 'a student starting on Tuesday at 09:00 has until 12:00');
assert.equal(result.workingMode, 'DIRECT'); assert.equal(result.resumed, false); assert.equal(rows.length, 2);
// a start after 20:59 on the last day gets only the time left until the close
rows = [['headers']]; now = Date.parse(close) - 3600000; const late = ctx.requestTestFiles(input);
assert.equal(late.personalDeadline, new Date(close).toISOString(), 'starting at 22:59 on 25 November still ends at 23:59');
// refresh and a second device return the same notebook and deadline, never a new timer
now += 600000; const again = ctx.requestTestFiles(input); assert.equal(again.personalDeadline, late.personalDeadline); assert.equal(again.colabUrl, late.colabUrl); assert.equal(again.resumed, true); assert.equal(fileCount, 2 - 0 > 0 ? fileCount : 0);
// after the deadline nothing restarts
now = Date.parse(close) + 1; assert.throws(() => ctx.requestTestFiles(input), /closed|personal deadline/);

// 3. what the student is issued
const issuedNb = {};
for (const cohort of ['CML3111', 'CML3112', 'CML3113']) for (const variant of ['A', 'B', 'C']) {
  windowKey = cohort + '|ML_PROJECT'; windowRows = [['key', 'open', 'close', 'enabled', 'duration'], [windowKey, open, close, 'YES', 180]];
  now = Date.parse(open) + 60000;
  rows = [['headers'], [windowKey, 'DEMO / ML 1', input.email, 'T-' + cohort + '-' + variant, variant, '2026-11-30T00:00:00Z']];
  const issued = ctx.requestTestFiles({ ...input, test: windowKey }); const nb = JSON.parse(issued.notebook);
  const packet = ctx.PORTAL_PACKETS_ML[windowKey + '|' + variant];
  assert.equal(issued.csv, packet.csv);
  assert(nb.cells[0].source.join ? nb.cells[0].source.join('').includes('Engineering ML project') : nb.cells[0].source.includes('Engineering ML project'));
  assert(String(nb.cells[0].source).includes('Your submission deadline'));
  assert(!String(nb.cells[0].source).includes('Test 1'));
  const identity = nb.cells[1].source; assert(identity.includes('TEST_ID = "ML_PROJECT"') && identity.includes('COHORT = "' + cohort + '"') && identity.includes('_IUEA_DEADLINE' ) === false);
  assert(identity.includes('Test countdown'), 'the countdown is in the identity cell');
  assert(nb.cells[3].source.includes(JSON.stringify(packet.csv)), 'the exact CSV of this variant is restored by the setup cell');
  const last = nb.cells.at(-1).source; assert(last.includes('_IUEA_DEADLINE = ' + JSON.stringify(issued.personalDeadline)) && last.includes('VARIANT = "' + variant + '"') && last.includes("TEST_ID in ('TEST1', 'ML_PROJECT')"));
  assert.equal(nb.metadata.iuea_allocation_code, rows[1][3]);
  assert.equal(issued.personalDeadline, new Date(now + H3).toISOString());
  assert.equal(issued.csv, '', 'the data is inside the notebook; no CSV is sent');
  const base = JSON.parse(packet.notebook);
  for (let i = 4; i < nb.cells.length - 1; i++) if (base.cells[i].cell_type === 'code') assert.deepEqual(nb.cells[i].source, base.cells[i].source);
  if (cohort === 'CML3112') issuedNb[variant] = nb;
}
if (out) fs.writeFileSync(out, JSON.stringify(issuedNb));

// 4. the collector: a late form is refused, an on-time form is collected with the personal timestamps, a missing timer fails closed
windowKey = 'CML3112|ML_PROJECT'; windowRows = [['key', 'open', 'close', 'enabled', 'duration'], [windowKey, open, close, 'YES', 180]];
now = Date.parse(open) + 60000; rows = [['headers']]; const started = ctx.requestTestFiles({ ...input, test: windowKey });
let collected = [], collection = { getLastRow: () => 1, appendRow: r => collected.push(r), getDataRange: () => ({ getValues: () => receipts }) };
const original = book.getSheetByName; book.getSheetByName = n => n === 'Collection' ? collection : original(n);
const vals = { 'Full name': 'Synthetic learner', 'Student Registration Number': 'DEMO / ML 1', 'Test allocation code': rows[1][3] };
const response = { getId: () => 'late', getTimestamp: () => new Date(Date.parse(close) + 1000), getRespondentEmail: () => input.email,
  getItemResponses: () => Object.entries(vals).map(([k, v]) => ({ getItem: () => ({ getTitle: () => k }), getResponse: () => v })) };
ctx.examCollect_(response, windowKey, { bookId: 'book' });
assert.equal(collected[0][10], 'OUTSIDE_WINDOW', 'after the window closes the form is outside the window');
const bytes = Buffer.from(JSON.stringify({ nbformat: 4, cells: [], metadata: { iuea_allocation_code: rows[1][3] } }));
vals['Snapshot file ID'] = 'synthetic-snapshot-id'; vals['Snapshot SHA-256'] = crypto.createHash('sha256').update(bytes).digest('hex');
ctx.Utilities.DigestAlgorithm = { SHA_256: 'sha256' }; ctx.Utilities.computeDigest = (_, b) => [...crypto.createHash('sha256').update(b).digest()];
ctx.DriveApp.getFileById = () => ({ getOwner: () => ({ getEmail: () => input.email }), getSize: () => bytes.length, getBlob: () => ({ getBytes: () => bytes, getDataAsString: () => bytes.toString() }) });
response.getId = () => 'ontime'; response.getTimestamp = () => new Date(now + 120 * 60000);
ctx.examCollect_(response, windowKey, { bookId: 'book', folderId: 'private-folder' });
assert.equal(collected.at(-1)[10], 'COLLECTED'); assert.equal(collected.at(-1)[9], started.personalDeadline);
// a form after the personal 3 hours, while the window is still open, is OUTSIDE_PERSONAL_WINDOW
now = Date.parse(open) + 60000;
rows = [['headers']]; const early = ctx.requestTestFiles({ ...input, test: windowKey, registration: 'DEMO / ML 2', email: 'two@example.com' });
assert.equal(early.personalDeadline, new Date(Date.parse(open) + 60000 + H3).toISOString(), 'the personal 3 hours apply inside the long window');
vals['Student Registration Number'] = 'DEMO / ML 2'; vals['Test allocation code'] = rows[1][3]; response.getId = () => 'late-personal'; response.getRespondentEmail = () => 'two@example.com';
response.getTimestamp = () => new Date(Date.parse(early.personalDeadline) + 60000);
ctx.examCollect_(response, windowKey, { bookId: 'book' }); assert.equal(collected.at(-1)[10], 'OUTSIDE_PERSONAL_WINDOW');
rows[1][7] = ''; rows[1][8] = ''; response.getId = () => 'no-timer'; response.getTimestamp = () => new Date(now + 60000); ctx.examCollect_(response, windowKey, { bookId: 'book' }); assert.equal(collected.at(-1)[10], 'COLLECTION_ERROR');
book.getSheetByName = original;

// 5. the new collector functions
props.IUEA_COLAB_EXAMS_V1 = JSON.stringify({ bookId: 'book', folderId: 'folder', forms: { 'CML3111|TEST1': { formId: 'x' } } });
windowRows = [['key', 'open', 'close', 'enabled', 'duration']];
ctx.installMlProjectCollection();
assert.equal(JSON.stringify(formsMade.slice().sort()), JSON.stringify(['CML3111 ML_PROJECT — Colab test submission', 'CML3112 ML_PROJECT — Colab test submission', 'CML3113 ML_PROJECT — Colab test submission']));
assert.equal(windowRows.length, 4); windowRows.slice(1).forEach(r => { assert.match(r[0], /\|ML_PROJECT$/); assert.equal(r[3], 'NO'); assert.equal(r[4], 180); assert.equal(r[1], ''); });
const saved = JSON.parse(props.IUEA_COLAB_EXAMS_V1); assert.equal(Object.keys(saved.forms).length, 4);
ctx.installMlProjectCollection(); assert.equal(formsMade.length, 3, 'a second run creates nothing');
assert.throws(() => ctx.setMlProjectWindow('CML3112', open, close), /CONFIRMED/);
assert.throws(() => ctx.setMlProjectWindow('CML3112', '2026-11-23T00:00:00+03:00', '2026-11-27T00:00:00+03:00', 'CONFIRMED'), /more than 72 hours/);
assert.throws(() => ctx.setMlProjectWindow('CML3112', '2026-11-23T00:00:00+03:00', '2026-11-23T02:00:00+03:00', 'CONFIRMED'), /shorter than 3 hours/);
ctx.setMlProjectWindow('CML3112', '2026-11-23T00:00:00+03:00', '2026-11-25T23:59:00+03:00', 'CONFIRMED');
assert.equal(JSON.stringify(windowRows.find(r => r[0] === 'CML3112|ML_PROJECT').slice(3)), JSON.stringify(['YES', 180]));
assert.throws(() => ctx.authoriseFreshTestAttempt('CML3112|ML_PROJECT', 'REG1', 'technical failure at 11:30', ''), /No Test allocations sheet|allocation/);
assert.throws(() => ctx.authoriseFreshTestAttempt('CML3112|TEST9', 'REG1', 'technical failure at 11:30', ''), /Use an assessment key/);
// 6. size: the gateway reads at most 4 MiB from Apps Script
const one = JSON.stringify({ notebook: JSON.stringify(issuedNb.A) });
assert(Buffer.byteLength(one) < 2 * 1024 * 1024, 'an issued notebook stays far below the gateway limit: ' + Buffer.byteLength(one));
console.log('PASS ML_PROJECT deployment bundle: window 23 to 25 November, personal deadline (earlier of start+180 and the window close), resume, one notebook per course for the 3 allocation labels (issued size ' + Math.round(Buffer.byteLength(one) / 1024) + ' KiB), collector acceptance and refusal, form creation (closed), window setter guards.');
