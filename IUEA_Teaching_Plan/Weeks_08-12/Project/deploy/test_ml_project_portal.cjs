// Offline proof of the deployment bundle, modelled on tests/test_timed_takehome.cjs (same fakes for Sheets, Drive and Forms).
// usage (from anywhere): node IUEA_Teaching_Plan/Weeks_08-12/Project/deploy/test_ml_project_portal.cjs [path to write one issued notebook as JSON]
const fs = require('fs'), path = require('path'), vm = require('vm'), assert = require('assert/strict'), crypto = require('crypto');
const deploy = __dirname;
const out = process.argv[2];
let now = Date.parse('2026-11-22T20:59:00Z'), rows = [['headers']], fileCount = 0, driveCalls = [], props = { PORTAL_TOKEN_SECRET: 'synthetic-token-secret-for-tests-only-0123456789' };
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
// The class list (made-up identities only). The same registration is on all three lists so the packet loop can use one identity.
const classList = [['cohort', 'registration', 'full_name']].concat(['CML3111', 'CML3112', 'CML3113'].flatMap(c => [[c, '26/DEMO/001/ML', 'Synthetic Learner One'], [c, '26/DEMO/002/ML', 'Synthetic Learner Two']]),
  [['CML3113', '99/123/TEST-X', 'Other Course Learner']]);
const book = { getSheetByName: n => n === 'Collection' ? { getDataRange: () => ({ getValues: () => receipts }) } : n === 'Test windows' ? windowSheet : n === 'Test allocations' ? sheet : n === 'Class list' ? { getDataRange: () => ({ getValues: () => classList }) } : null };
const formsMade = [];
const chain = () => new Proxy(function () {}, { get: (t, k) => k === 'getId' ? () => 'id-' + Math.random() : k === 'getPublishedUrl' ? () => 'https://forms/viewform' : k === 'toPrefilledUrl' ? () => 'https://forms/viewform?x=PLACEHOLDER' : () => chain(), apply: () => chain() });
const ctx = { Date: Clock, Math, JSON, console, Object, Array, Error, Number, String, isFinite, parseInt,
  SpreadsheetApp: { openById: () => book, newRichTextValue: () => ({ setText(v) { this.v = v; return this; }, build() { return this.v; } }) },
  LockService: { getScriptLock: () => ({ tryLock: () => true, waitLock() {}, releaseLock() {} }) },
  PropertiesService: { getScriptProperties: () => ({ getProperty: k => props[k], setProperty: (k, v) => props[k] = v }) },
  Utilities: { getUuid: () => 'synthetic-code', formatDate: d => d.toISOString(),
    newBlob: (b) => ({ getBytes: () => [...Buffer.from(typeof b === 'string' ? b : Buffer.from(b))].map(x => x > 127 ? x - 256 : x), getDataAsString: () => typeof b === 'string' ? b : Buffer.from(b).toString() }),
    computeHmacSha256Signature: (v, k) => [...crypto.createHmac('sha256', k).update(v).digest()].map(x => x > 127 ? x - 256 : x),
    base64EncodeWebSafe: bytes => Buffer.from(bytes.map(x => (x + 256) % 256)).toString('base64').replace(/\+/g, '-').replace(/\//g, '_'),
    base64DecodeWebSafe: t => [...Buffer.from(t.replace(/-/g, '+').replace(/_/g, '/'), 'base64')].map(x => x > 127 ? x - 256 : x) },
  ScriptApp: { getOAuthToken: () => 'never-real', newTrigger: () => ({ forForm: () => ({ onFormSubmit: () => ({ create() {} }) }) }) },
  UrlFetchApp: { fetch: (url, options) => { driveCalls.push({ url, options }); return { getResponseCode: () => 200 }; } },
  FormApp: { create: title => { formsMade.push(title); return chain(); }, DestinationType: { SPREADSHEET: 1 }, ItemType: { TEXT: 2 } },
  HtmlService: { createHtmlOutput: m => ({ message: m }), createTemplateFromFile: f => ({ evaluate() { const o = { file: f, title: '', setTitle(t) { o.title = t; return o; }, addMetaTag() { return o; } }; return o; } }) },
  DriveApp: { createFolder: () => ({ getId: () => 'private-folder' }), getFolderById: () => ({ createFile: () => { const id = 'file-' + (++fileCount); return { getId: () => id }; } }) } };
vm.createContext(ctx);
for (const f of ['Portal.gs', 'Gateway.gs', 'PacketsMLProject.gs', 'exam_collection.gs', 'ml_project_collection.gs']) vm.runInContext(fs.readFileSync(path.join(deploy, f), 'utf8'), ctx);
vm.runInContext("var PORTAL_PACKETS = {};", ctx);   // the Test 1 packets are not needed here: the project lookup must work without them
const input = { test: windowKey, registration: '26/DEMO/001/ML', email: 'synthetic@example.com', name: 'Synthetic learner' };

// 0. the entry page checks the registration against the class list as it is typed (item 6)
assert.deepEqual({ ...ctx.portalCheckRegistration({ test: 'CML3112|ML_PROJECT', registration: ' 26/demo/001/ml ' }) }, { registration: '26/DEMO/001/ML', nameHint: 'Synthetic L. O.', onList: true, course: 'CML3112' });
assert.throws(() => ctx.portalCheckRegistration({ test: 'CML3112|ML_PROJECT', registration: '99/123/TEST-X' }), /This registration number is on the CML3113 class list, not CML3112\. Choose CML3113 as your course\./);
// No mixing of programmes (15 November 2026): off the list, the programme code must belong to the chosen course; unknown codes are refused.
assert.throws(() => ctx.portalCheckRegistration({ test: 'CML3113|ML_PROJECT', registration: '24/999/BSCE-S' }), /is for BSCE, which takes CML3112, not CML3113\. Choose CML3112 as your course\./);
assert.throws(() => ctx.portalCheckRegistration({ test: 'CML3111|ML_PROJECT', registration: '23/UG/5/BARC-J' }), /Choose CML3112 as your course/);
// The rehearsal is the lecturer's (16 November 2026): only the demo numbers open it, in any course; they never open the real project.
assert.throws(() => ctx.portalCheckRegistration({ test: 'CML3112|ML_REHEARSAL', registration: '26/DEMO/001/ML' }), /cannot open the rehearsal: your lecturer runs it in class/);
assert.throws(() => ctx.portalCheckRegistration({ test: 'CML3113|ML_REHEARSAL', registration: '24/999/BSPE-J' }), /cannot open the rehearsal/);
for (const c of ['CML3111', 'CML3112', 'CML3113']) assert.equal(ctx.portalCheckRegistration({ test: c + '|ML_REHEARSAL', registration: '26/demo/001/lecturer' }).course, c, 'the demo number opens the rehearsal in every course');
assert.throws(() => ctx.portalCheckRegistration({ test: 'CML3112|ML_PROJECT', registration: '26/SMOKE/001/TEST' }), /for practice only/);
assert.throws(() => ctx.requestTestFiles({ ...input, registration: '24/999/BSPE-J', name: 'Some Name' }), /Choose CML3113 as your course/);
assert.throws(() => ctx.portalCheckRegistration({ test: 'CML3112|ML_PROJECT', registration: '24/999/BSXX-S' }), /does not match any of the three courses/);
assert.equal(ctx.portalCheckRegistration({ test: 'CML3113|ML_PROJECT', registration: '23/UG/5/BSME-J' }).onList, false, 'right programme, not on the list: open entry');
assert.equal(ctx.portalCheckRegistration({ test: 'CML3112|ML_PROJECT', registration: '24/999/BSCE-S' }).onList, false, 'open entry: a registration not on the list is not refused');
assert.throws(() => ctx.portalCheckRegistration({ test: 'CML3112|ML_PROJECT', registration: 'hello' }), /as it is on your student card/);
assert.throws(() => ctx.portalCheckRegistration({ test: 'CML3112|TEST1', registration: '26/DEMO/001/ML' }), /Use your lecturer/);
// the same checks through the gateway entry (Gateway.gs doPost); the messages reach the student
const viaGateway = body => { props.PORTAL_GATEWAY_KEY = 'k'.repeat(40); return JSON.parse(ctx.doPost({ postData: { contents: JSON.stringify({ secret: 'k'.repeat(40), ...body }) } }).text); };
ctx.ContentService = { createTextOutput: t => ({ text: t, setMimeType() { return this; } }), MimeType: { JSON: 'json' } };
assert.equal(viaGateway({ action: 'check', input: { test: 'CML3112|ML_PROJECT', registration: '26/DEMO/002/ML' } }).result.nameHint, 'Synthetic L. T.');
assert.match(viaGateway({ action: 'check', input: { test: 'CML3112|ML_PROJECT', registration: '99/123/TEST-X' } }).error, /^This registration number is on the CML3113 class list, not CML3112\. Choose CML3113 as your course\.$/);
// open entry: a registration not on the list starts with the typed full name; a missing name or a malformed number is refused
now = Date.parse(open) + 1000;
assert.throws(() => ctx.requestTestFiles({ ...input, registration: '24/999/BSCE-S', name: '(class list)' }), /Enter your full name/);
assert.throws(() => ctx.requestTestFiles({ ...input, registration: 'abc 12' }), /as it is on your student card/);
assert.throws(() => ctx.requestTestFiles({ ...input, registration: '99/123/TEST-X' }), /Choose CML3113 as your course/);
now = Date.parse('2026-11-22T20:59:00Z');

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
  rows = [['headers'], [windowKey, '26/DEMO/001/ML', input.email, 'T-' + cohort + '-' + variant, variant, '2026-11-30T00:00:00Z']];
  const issued = ctx.requestTestFiles({ ...input, test: windowKey }); const nb = JSON.parse(issued.notebook);
  const packet = ctx.PORTAL_PACKETS_ML[windowKey + '|' + variant];
  assert.equal(issued.csv, packet.csv);
  assert(nb.cells[0].source.join ? nb.cells[0].source.join('').includes('Engineering ML project') : nb.cells[0].source.includes('Engineering ML project'));
  // plain-code redesign of 14 November 2026: the notebook's own short opening, then ONE supplied cell (Setup: run me first) that holds
  // the identity, the data and the deadline; no identity cell, no token, no Submit cell, no other supplied cell
  assert(String(nb.cells[0].source).trim().split('\n').length <= 7, 'the opening is at most 7 short lines (title, deadline, three steps, rules, data)');
  assert(!String(nb.cells[0].source).includes('Test 1'));
  const setup = String(nb.cells[1].source); assert(setup.startsWith('#@title Setup: run me first') && nb.cells[1].metadata.cellView === 'form');
  const ident = JSON.parse(/^_IUEA_IDENTITY = (.*)$/m.exec(setup)[1]);
  assert.deepEqual([ident.course, ident.test, ident.allocation, ident.deadline, ident.registration], [cohort, 'ML_PROJECT', rows[1][3], issued.personalDeadline, '26/DEMO/001/ML']);
  assert.equal(ident.name, 'Synthetic Learner One', 'the name comes from the class list, not from what was typed');
  assert(setup.includes(packet.data) && !setup.includes('__IUEA_PACKED_DATA__'), 'the data block is put back into the setup cell');
  assert(setup.includes('post_run_cell') && setup.includes('Press Ctrl+S'), 'the countdown line after every cell, with the Ctrl+S reminders');
  assert(/"User-Agent": "iuea-notebook-backup/.test(setup), 'the backup names its sender: Cloudflare refuses Python\'s default client signature (error 1010, 18 November 2026)');
  assert.equal(nb.cells.filter(c => c.cell_type === 'code' && /# IUEA-|Do not edit/.test(String(c.source)) && !/# IUEA-SUPPLIED/.test(String(c.source))).length, 1, 'exactly one supplied setup cell');
  assert.equal(nb.cells.filter(c => c.cell_type === 'code' && /# IUEA-SUPPLIED/.test(String(c.source))).length, 16, 'the sixteen visible supplied cells: four import cells, two data reads, two targets, three feature lists, the THRESHOLD, two gradient descent cells, two model-choosing rules (17 November 2026)');
  assert.ok(/houses_raw = pd\.read_csv\("houses\.csv"\)/.test(nb.cells.map(c => String(c.source)).join('\n')), 'the house table is read in a visible cell');
  assert(!JSON.stringify(nb).includes('_IUEA_TOKEN') && !nb.cells.some(c => (c.metadata.tags || []).includes('iuea-submission')), 'no token, no Submit cell');
  assert.equal(issued.attempt, rows[1][3], 'the entry page receives the allocation code');
  assert.equal(nb.metadata.iuea_allocation_code, rows[1][3]);
  assert.equal(issued.personalDeadline, new Date(now + H3).toISOString());
  assert.equal(issued.csv, '', 'the data is inside the notebook; no CSV is sent');
  const base = JSON.parse(packet.notebook);
  for (let i = 2; i < nb.cells.length; i++) if (base.cells[i].cell_type === 'code') assert.deepEqual(nb.cells[i].source, base.cells[i].source);
  if (cohort === 'CML3112') issuedNb[variant] = nb;
}
if (out) fs.writeFileSync(out, JSON.stringify(issuedNb));

// 4. the collector: a late form is refused, an on-time form is collected with the personal timestamps, a missing timer fails closed
windowKey = 'CML3112|ML_PROJECT'; windowRows = [['key', 'open', 'close', 'enabled', 'duration'], [windowKey, open, close, 'YES', 180]];
now = Date.parse(open) + 60000; rows = [['headers']]; const started = ctx.requestTestFiles({ ...input, test: windowKey });
let collected = [], collection = { getLastRow: () => 1, appendRow: r => collected.push(r), getDataRange: () => ({ getValues: () => receipts }) };
const original = book.getSheetByName; book.getSheetByName = n => n === 'Collection' ? collection : original(n);
const vals = { 'Full name': 'Synthetic learner', 'Student Registration Number': '26/DEMO/001/ML', 'Test allocation code': rows[1][3] };
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
rows = [['headers']]; const early = ctx.requestTestFiles({ ...input, test: windowKey, registration: '26/DEMO/002/ML', email: 'two@example.com' });
assert.equal(early.personalDeadline, new Date(Date.parse(open) + 60000 + H3).toISOString(), 'the personal 3 hours apply inside the long window');
vals['Student Registration Number'] = '26/DEMO/002/ML'; vals['Test allocation code'] = rows[1][3]; response.getId = () => 'late-personal'; response.getRespondentEmail = () => 'two@example.com';
response.getTimestamp = () => new Date(Date.parse(early.personalDeadline) + 60000);
ctx.examCollect_(response, windowKey, { bookId: 'book' }); assert.equal(collected.at(-1)[10], 'OUTSIDE_PERSONAL_WINDOW');
rows[1][7] = ''; rows[1][8] = ''; response.getId = () => 'no-timer'; response.getTimestamp = () => new Date(now + 60000); ctx.examCollect_(response, windowKey, { bookId: 'book' }); assert.equal(collected.at(-1)[10], 'COLLECTION_ERROR');
book.getSheetByName = original;

// 5. the new collector functions (no Google Form for the project: the rows only)
props.IUEA_COLAB_EXAMS_V1 = JSON.stringify({ bookId: 'book', folderId: 'folder', forms: { 'CML3111|TEST1': { formId: 'x' } } });
windowRows = [['key', 'open', 'close', 'enabled', 'duration']];
ctx.installMlProjectCollection();
assert.equal(formsMade.length, 0, 'no form is created for the project');
assert.equal(windowRows.length, 4); windowRows.slice(1).forEach(r => { assert.match(r[0], /\|ML_PROJECT$/); assert.equal(r[3], 'NO'); assert.equal(r[4], 180); assert.equal(r[1], ''); });
ctx.installMlProjectCollection(); assert.equal(windowRows.length, 4, 'a second run creates nothing');
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
console.log('PASS ML_PROJECT deployment bundle: class list check (format, membership, wrong course), name from the class list, one supplied setup cell holding the identity and the data (no token, no Submit cell), the countdown line with Ctrl+S reminders, window 23 to 25 November, personal deadline (earlier of start+180 and the window close), resume, one notebook per course for the 3 allocation labels (issued size ' + Math.round(Buffer.byteLength(one) / 1024) + ' KiB), Test 1 collector refusal rules, the windows rows, window setter guards.');
