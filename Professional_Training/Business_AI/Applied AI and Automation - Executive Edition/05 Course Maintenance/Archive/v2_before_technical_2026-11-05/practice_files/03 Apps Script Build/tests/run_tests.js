'use strict';
// Run with:  node tests/run_tests.js   (from the "03 Apps Script Build" folder)
// No network, no packages to install. Uses the hand-written mocks in tests/mocks.js.
//
// The expected numbers below were worked out by hand from the two small fixture files
// in fixtures/. They are NOT produced by the scripts, so the tests are a real check.

const assert = require('assert');
const fs = require('fs');
const path = require('path');
const { loadProject } = require('./mocks');

const ROOT = path.join(__dirname, '..');
const SALES = path.join(ROOT, 'fixtures', 'weekly_sales_small.csv');
const INVOICES = path.join(ROOT, 'fixtures', 'supplier_invoices_small.csv');

// Compares two values by their JSON text (values made inside the vm have a different Array type).
function same(actual, expected) {
  assert.strictEqual(JSON.stringify(actual), JSON.stringify(expected));
}

let passed = 0;
let failed = 0;
function test(name, fn) {
  try {
    fn();
    passed++;
    console.log('  ok    ' + name);
  } catch (err) {
    failed++;
    console.log('  FAIL  ' + name + '\n        ' + String(err.message).split('\n').join('\n        '));
  }
}
function group(title) { console.log('\n' + title); }

// A fresh project with the sales fixture loaded and the digest switched to live mode.
function salesProject() {
  const env = loadProject(ROOT);
  env.loadSheet('weekly_sales', SALES);
  return env;
}
function invoiceProject() {
  const env = loadProject(ROOT);
  env.loadSheet('supplier_invoices', INVOICES);
  return env;
}
function logRows(env) { return env.state.sheets['Run log'].data; }

// ---------------------------------------------------------------------------
group('Weekly digest: the numbers');

test('totals and week-on-week change match the hand calculation', () => {
  const env = salesProject();
  const rows = env.context.valuesToObjects(env.state.sheets['weekly_sales'].data);
  const d = env.context.buildDigest(rows);
  same(Array.from(d.weeks), ['2026-09-07', '2026-09-14', '2026-09-21']);
  assert.strictEqual(d.latestWeek, '2026-09-21');
  assert.strictEqual(d.previousWeek, '2026-09-14');
  same(
    d.weeklyTotals.map((w) => w.total),
    [29700000, 30450000, 31500000]
  );
  assert.strictEqual(d.totalLatest, 31500000);
  assert.strictEqual(d.totalPrevious, 30450000);
  assert.strictEqual(d.totalChange, 1050000);
  assert.strictEqual(d.totalChangePct, 3.4);

  const by = {};
  d.table.forEach((t) => { by[t.group] = t; });
  same(d.table.map((t) => t.group), ['Jinja', 'Mbale', 'Soroti']);
  assert.strictEqual(by.Jinja.latest, 19800000);
  assert.strictEqual(by.Jinja.previous, 16650000);
  assert.strictEqual(by.Jinja.change, 3150000);
  assert.strictEqual(by.Jinja.changePct, 18.9);
  assert.strictEqual(by.Mbale.latest, 9900000);
  assert.strictEqual(by.Mbale.previous, 13800000);
  assert.strictEqual(by.Mbale.change, -3900000);
  assert.strictEqual(by.Mbale.changePct, -28.3);
  assert.strictEqual(by.Soroti.latest, 1800000);
  assert.strictEqual(by.Soroti.previous, 0);
  assert.strictEqual(by.Soroti.change, 1800000);
  assert.strictEqual(by.Soroti.changePct, null);   // cannot divide by a zero week
  assert.strictEqual(d.biggestRise, 'Jinja');
  assert.strictEqual(d.biggestFall, 'Mbale');
});

test('a row with a blank value is skipped and counted, not added as zero', () => {
  const env = salesProject();
  const d = env.context.buildDigest(env.context.valuesToObjects(env.state.sheets['weekly_sales'].data));
  assert.strictEqual(d.skippedRows, 1);
  assert.ok(!d.table.some((t) => t.group === 'Kamuli'));
});

test('dates from Sheets (Date objects) give the same answer as text dates', () => {
  const env = salesProject();
  const sheet = env.state.sheets['weekly_sales'];
  sheet.data.forEach((row, i) => {
    if (i > 0) row[0] = new Date(row[0] + 'T00:00:00Z');
  });
  const d = env.context.buildDigest(env.context.valuesToObjects(sheet.data));
  assert.strictEqual(d.latestWeek, '2026-09-21');
  assert.strictEqual(d.totalLatest, 31500000);
});

test('text numbers such as "9,000,000" and "UGX 9,000,000" are read correctly', () => {
  const env = salesProject();
  assert.strictEqual(env.context.toNumber('9,000,000'), 9000000);
  assert.strictEqual(env.context.toNumber('UGX 9,000,000'), 9000000);
  assert.ok(isNaN(env.context.toNumber('')));
  assert.ok(isNaN(env.context.toNumber('abc')));
});

test('one week of data gives totals and no comparison', () => {
  const env = loadProject(ROOT);
  env.makeSheet('weekly_sales', [
    ['week_start', 'region', 'product', 'units', 'revenue_ugx'],
    ['2026-09-07', 'Jinja', 'Maize flour', 100, 9000000]
  ]);
  const d = env.context.buildDigest(env.context.valuesToObjects(env.state.sheets['weekly_sales'].data));
  assert.strictEqual(d.previousWeek, null);
  assert.strictEqual(d.totalLatest, 9000000);
  assert.strictEqual(d.totalChange, null);
  assert.ok(env.context.buildEmailBody(d, '').indexOf('no earlier week') >= 0);
});

test('an empty sheet gives a clear message and no crash', () => {
  const env = loadProject(ROOT);
  env.makeSheet('weekly_sales', [['week_start', 'region', 'product', 'units', 'revenue_ugx']]);
  const d = env.context.buildDigest([]);
  assert.strictEqual(d.latestWeek, null);
  assert.ok(env.context.buildEmailBody(d, '').indexOf('No usable rows') >= 0);
});

// ---------------------------------------------------------------------------
group('Weekly digest: the run');

test('default settings are safe: dry run on, AI off', () => {
  const env = salesProject();
  assert.strictEqual(env.run('DIGEST_DRY_RUN'), true);
  assert.strictEqual(env.run('USE_AI_COMMENTARY'), false);
  assert.strictEqual(env.run('INVOICE_DRY_RUN'), true);
});

test('dry run creates no draft, sends nothing and writes one line to the Run log', () => {
  const env = salesProject();
  env.context.createWeeklyDigest();
  assert.strictEqual(env.state.drafts.length, 0);
  assert.strictEqual(env.state.sentEmails.length, 0);
  assert.strictEqual(env.state.fetchCalls.length, 0);
  const rows = logRows(env);
  assert.strictEqual(rows.length, 2);   // heading plus one run
  same(rows[0], ['time', 'script', 'mode', 'summary']);
  assert.strictEqual(rows[1][1], 'createWeeklyDigest');
  assert.strictEqual(rows[1][2], 'dry-run');
});

test('live run saves exactly one draft to the owner, with the right figures, and never sends', () => {
  const env = salesProject();
  env.run('DIGEST_DRY_RUN = false');
  env.context.createWeeklyDigest();
  assert.strictEqual(env.state.drafts.length, 1);
  assert.strictEqual(env.state.sentEmails.length, 0);
  const draft = env.state.drafts[0];
  assert.strictEqual(draft.to, 'owner@example.com');
  assert.ok(draft.subject.indexOf('2026-09-21') >= 0);
  assert.ok(draft.body.indexOf('Jinja | 19,800,000 | 16,650,000 | +3,150,000 (+18.9%)') >= 0, draft.body);
  assert.ok(draft.body.indexOf('Mbale | 9,900,000 | 13,800,000 | -3,900,000 (-28.3%)') >= 0, draft.body);
  assert.ok(draft.body.indexOf('Soroti | 1,800,000 | 0 | +1,800,000 (n/a)') >= 0, draft.body);
  assert.ok(draft.body.indexOf('TOTAL | 31,500,000 | 30,450,000 | +1,050,000 (+3.4%)') >= 0, draft.body);
  assert.strictEqual(logRows(env)[1][2], 'live');
});

test('a configured recipient is used instead of the owner', () => {
  const env = salesProject();
  env.run('DIGEST_DRY_RUN = false; DIGEST_RECIPIENT = "boss@example.com"');
  env.context.createWeeklyDigest();
  assert.strictEqual(env.state.drafts[0].to, 'boss@example.com');
});

test('AI off by default: no network call even in a live run', () => {
  const env = salesProject();
  env.run('DIGEST_DRY_RUN = false');
  env.context.createWeeklyDigest();
  assert.strictEqual(env.state.fetchCalls.length, 0);
  assert.ok(env.state.drafts[0].body.indexOf('AI comment') < 0);
});

test('AI on: one call, comment added below the table, figures unchanged', () => {
  const env = salesProject();
  env.state.properties.GEMINI_API_KEY = 'TEST-KEY-123';
  env.fakeGeminiOk('Sales rose in Jinja. Sales fell in Mbale. Soroti is new this week.');
  env.run('DIGEST_DRY_RUN = false; USE_AI_COMMENTARY = true');
  env.context.createWeeklyDigest();
  assert.strictEqual(env.state.fetchCalls.length, 1);
  const body = env.state.drafts[0].body;
  assert.ok(body.indexOf('Sales rose in Jinja.') >= 0);
  assert.ok(body.indexOf('TOTAL | 31,500,000') >= 0);
});

test('AI on in a dry run: still no call', () => {
  const env = salesProject();
  env.state.properties.GEMINI_API_KEY = 'TEST-KEY-123';
  env.fakeGeminiOk('x');
  env.run('USE_AI_COMMENTARY = true');
  env.context.createWeeklyDigest();
  assert.strictEqual(env.state.fetchCalls.length, 0);
});

test('AI failure (server error) does not stop the draft; the reason is logged', () => {
  const env = salesProject();
  env.state.properties.GEMINI_API_KEY = 'TEST-KEY-123';
  env.state.fetchResponder = () => ({ getResponseCode: () => 500, getContentText: () => 'server trouble' });
  env.run('DIGEST_DRY_RUN = false; USE_AI_COMMENTARY = true');
  env.context.createWeeklyDigest();
  assert.strictEqual(env.state.drafts.length, 1);
  assert.ok(env.state.drafts[0].body.indexOf('TOTAL | 31,500,000') >= 0);
  assert.ok(String(logRows(env)[1][3]).indexOf('AI skipped') >= 0);
});

test('a wrong sheet name or column name stops with a plain message and logs an error', () => {
  const env = salesProject();
  env.run('SALES_SHEET_NAME = "nope"');
  assert.throws(() => env.context.createWeeklyDigest(), /no sheet named "nope"/);
  assert.strictEqual(logRows(env)[1][2], 'error');

  const env2 = salesProject();
  env2.run('GROUP_COLUMN = "branch"');
  assert.throws(() => env2.context.createWeeklyDigest(), /no column headed "branch"/);
});

test('setupWeeklyTrigger makes exactly one weekly trigger, even when run twice', () => {
  const env = salesProject();
  env.context.setupWeeklyTrigger();
  env.context.setupWeeklyTrigger();
  assert.strictEqual(env.state.triggers.length, 1);
  const spec = env.state.triggers[0].spec;
  assert.strictEqual(spec.handler, 'createWeeklyDigest');
  assert.strictEqual(spec.kind, 'time');
  assert.strictEqual(spec.weekday, 'MONDAY');
  assert.strictEqual(spec.hour, 7);
});

test('the off switch removes every trigger and logs it', () => {
  const env = salesProject();
  env.context.setupWeeklyTrigger();
  env.context.ScriptApp.newTrigger('somethingElse').timeBased().create();
  assert.strictEqual(env.state.triggers.length, 2);
  const removed = env.context.turnEverythingOff();
  assert.strictEqual(removed, 2);
  assert.strictEqual(env.state.triggers.length, 0);
  const last = logRows(env)[logRows(env).length - 1];
  assert.strictEqual(last[1], 'turnEverythingOff');
});

// ---------------------------------------------------------------------------
group('Invoice check: the flags');

// Expected flags worked out by hand from fixtures/supplier_invoices_small.csv
// (sheet row = line number in the file; row 2 is INV-001).
const EXPECTED_FLAGS = [
  ['3', 'INV-002', 'ZERO_VAT'],
  ['4', 'INV-003', 'WRONG_TOTAL'],     // 50 x 280,000 x 1.18 = 16,520,000 but total says 16,250,000
  ['6', 'INV-005', 'MISSING_PO'],
  ['7', 'INV-006', 'DUPLICATE'],       // same as row 2 under a new id
  ['10', 'INV-009', 'MISSING_PO'],
  ['10', 'INV-009', 'WRONG_TOTAL'],    // 500 x 1,500 x 1.18 = 885,000 but total says 800,000
  ['11', 'INV-008', 'DUPLICATE']       // id INV-008 already used on row 9
];

test('finds exactly the seven expected flags, and no others', () => {
  const env = invoiceProject();
  const rows = env.context.valuesToObjects(env.state.sheets['supplier_invoices'].data);
  const flags = env.context.checkInvoices(rows);
  const got = flags.map((f) => [String(f.row), f.invoice_id, f.flag]);
  const key = (a) => a.join('|');
  same(got.map(key).sort(), EXPECTED_FLAGS.map(key).sort());
});

test('correct invoices carry no flag', () => {
  const env = invoiceProject();
  const flags = env.context.checkInvoices(env.context.valuesToObjects(env.state.sheets['supplier_invoices'].data));
  [2, 5, 8, 9].forEach((row) => {
    assert.ok(!flags.some((f) => f.row === row), 'row ' + row + ' should have no flag');
  });
});

test('wrong-total detail shows the expected total and the difference', () => {
  const env = invoiceProject();
  const flags = env.context.checkInvoices(env.context.valuesToObjects(env.state.sheets['supplier_invoices'].data));
  const f4 = flags.filter((f) => f.row === 4 && f.flag === 'WRONG_TOTAL')[0];
  assert.ok(f4.detail.indexOf('16,520,000') >= 0, f4.detail);
  assert.ok(f4.detail.indexOf('-270,000') >= 0, f4.detail);
  const f10 = flags.filter((f) => f.row === 10 && f.flag === 'WRONG_TOTAL')[0];
  assert.ok(f10.detail.indexOf('885,000') >= 0, f10.detail);
  assert.ok(f10.detail.indexOf('-85,000') >= 0, f10.detail);
});

test('a total that is off by 1 UGX (rounding) is not flagged, 2 UGX is', () => {
  const env = loadProject(ROOT);
  const header = ['invoice_id', 'date', 'supplier', 'description', 'qty', 'unit_price_ugx', 'vat_pct', 'total_ugx', 'po_number'];
  env.makeSheet('supplier_invoices', [
    header,
    ['A1', '2026-09-01', 'S', 'd', 1, 1000, 18, 1181, 'PO1'],   // expected 1,180; off by 1
    ['A2', '2026-09-01', 'S', 'e', 1, 1000, 18, 1182, 'PO2']    // off by 2
  ]);
  const flags = env.context.checkInvoices(env.context.valuesToObjects(env.state.sheets['supplier_invoices'].data));
  same(flags.map((f) => f.row + ':' + f.flag), ['3:WRONG_TOTAL']);
});

test('totals before VAT are checked when TOTAL_INCLUDES_VAT is false', () => {
  const env = loadProject(ROOT);
  env.run('TOTAL_INCLUDES_VAT = false');
  assert.strictEqual(env.context.expectedTotal(10, 90000, 18), 900000);
});

test('unreadable numbers give BAD_NUMBER, not a crash or a false WRONG_TOTAL', () => {
  const env = loadProject(ROOT);
  const header = ['invoice_id', 'date', 'supplier', 'description', 'qty', 'unit_price_ugx', 'vat_pct', 'total_ugx', 'po_number'];
  env.makeSheet('supplier_invoices', [header, ['B1', '2026-09-01', 'S', 'd', 'ten', 1000, 18, 1180, 'PO1']]);
  const flags = env.context.checkInvoices(env.context.valuesToObjects(env.state.sheets['supplier_invoices'].data));
  same(flags.map((f) => f.flag), ['BAD_NUMBER']);
});

group('Invoice check: the run');

test('dry run writes nothing to Flags and logs the counts', () => {
  const env = invoiceProject();
  env.context.runInvoiceCheck();
  assert.strictEqual(env.state.sheets['Flags'], undefined);
  const row = logRows(env)[1];
  assert.strictEqual(row[1], 'runInvoiceCheck');
  assert.strictEqual(row[2], 'dry-run');
  assert.ok(String(row[3]).indexOf('Invoices read: 10') >= 0, row[3]);
  assert.ok(String(row[3]).indexOf('Flags: 7') >= 0, row[3]);
});

test('live run writes a heading and seven flag rows to Flags, and leaves the invoice sheet unchanged', () => {
  const env = invoiceProject();
  const before = JSON.stringify(env.state.sheets['supplier_invoices'].data);
  env.run('INVOICE_DRY_RUN = false');
  env.context.runInvoiceCheck();
  const flags = env.state.sheets['Flags'].data;
  same(flags[0], ['row', 'invoice_id', 'supplier', 'flag', 'detail']);
  assert.strictEqual(flags.length, 8);
  assert.strictEqual(JSON.stringify(env.state.sheets['supplier_invoices'].data), before);
  assert.strictEqual(logRows(env)[1][2], 'live');
});

test('running twice does not pile up flags: Flags is rewritten each time', () => {
  const env = invoiceProject();
  env.run('INVOICE_DRY_RUN = false');
  env.context.runInvoiceCheck();
  env.context.runInvoiceCheck();
  assert.strictEqual(env.state.sheets['Flags'].data.length, 8);
  assert.strictEqual(logRows(env).length, 3);   // heading plus two runs
});

test('a wrong sheet name stops with a plain message and logs an error', () => {
  const env = invoiceProject();
  env.run('INVOICE_SHEET_NAME = "nope"');
  assert.throws(() => env.context.runInvoiceCheck(), /no sheet named "nope"/);
  assert.strictEqual(logRows(env)[1][2], 'error');
});

// ---------------------------------------------------------------------------
group('AI helper: personal data and the call limit');

function aiProject() {
  const env = loadProject(ROOT);
  env.state.properties.GEMINI_API_KEY = 'TEST-KEY-123';
  env.fakeGeminiOk('Three short sentences. Here they are. Done.');
  env.makeSheet('Run log', []);
  return env;
}

test('a normal call works, uses the key header and muteHttpExceptions, and sends the prompt', () => {
  const env = aiProject();
  const r = env.context.askGemini('Summarise: total 31,500,000.', {});
  assert.strictEqual(r.ok, true);
  assert.strictEqual(r.text, 'Three short sentences. Here they are. Done.');
  assert.strictEqual(env.state.fetchCalls.length, 1);
  const call = env.state.fetchCalls[0];
  assert.strictEqual(call.params.muteHttpExceptions, true);
  assert.strictEqual(call.params.method, 'post');
  assert.strictEqual(call.params.headers['x-goog-api-key'], 'TEST-KEY-123');
  assert.ok(call.url.indexOf('TEST-KEY-123') < 0, 'the key must not be in the address');
  assert.ok(call.params.payload.indexOf('Summarise: total 31,500,000.') >= 0);
});

test('the model name constant controls the address', () => {
  const env = aiProject();
  env.run('GEMINI_MODEL = "my-new-model"');
  env.context.askGemini('hello', {});
  assert.ok(env.state.fetchCalls[0].url.indexOf('/models/my-new-model:generateContent') >= 0);
});

test('a row flagged as personal data is never sent', () => {
  const env = aiProject();
  const rows = [
    { name: 'Sample A', note: 'ok', contains_personal_data: 'no' },
    { name: 'Sample B', note: 'ok', contains_personal_data: 'yes' }
  ];
  const r = env.context.askGeminiAboutRows('Summarise these rows.', rows);
  assert.strictEqual(r.ok, false);
  assert.ok(r.reason.indexOf('personal data') >= 0);
  assert.strictEqual(env.state.fetchCalls.length, 0);
});

test('every spelling of yes in the flag column blocks the call', () => {
  ['yes', 'YES', 'Y', 'true', 'TRUE', '1', true, 1].forEach((flag) => {
    const env = aiProject();
    const r = env.context.askGeminiAboutRows('x', [{ contains_personal_data: flag }]);
    assert.strictEqual(r.ok, false, 'flag value ' + flag + ' should block');
    assert.strictEqual(env.state.fetchCalls.length, 0);
  });
});

test('unflagged rows are sent', () => {
  const env = aiProject();
  const r = env.context.askGeminiAboutRows('Summarise.', [{ a: 1, contains_personal_data: 'no' }, { a: 2 }]);
  assert.strictEqual(r.ok, true);
  assert.strictEqual(env.state.fetchCalls.length, 1);
});

test('the containsPersonalData option blocks the call', () => {
  const env = aiProject();
  const r = env.context.askGemini('anything', { containsPersonalData: true });
  assert.strictEqual(r.ok, false);
  assert.strictEqual(env.state.fetchCalls.length, 0);
});

test('text that looks like personal data (email, phone, ID number) is never sent', () => {
  const samples = [
    'Customer amina.k@example.com asked about oil.',
    'Call 0772 123 456 about the order.',
    'Call 0772123456 about the order.',
    'Call +256 772 123456 about the order.',
    'Call +256772123456 about the order.',
    'Her NIN is CF1234567890AB.'
  ];
  samples.forEach((text) => {
    const env = aiProject();
    const r = env.context.askGemini(text, {});
    assert.strictEqual(r.ok, false, 'should refuse: ' + text);
    assert.strictEqual(env.state.fetchCalls.length, 0, 'should not fetch: ' + text);
  });
});

test('ordinary business numbers are not mistaken for phone numbers', () => {
  const env = aiProject();
  assert.strictEqual(env.context.looksLikePersonalData('Total 31,500,000 UGX, up 3.4% on 30,450,000.'), false);
  assert.strictEqual(env.context.looksLikePersonalData('Invoice INV-003 for 16,520,000.'), false);
});

test('the call limit holds: 10 attempts make at most 3 network calls', () => {
  const env = aiProject();
  assert.strictEqual(env.run('AI_MAX_CALLS_PER_RUN'), 3);
  let okCount = 0;
  for (let i = 0; i < 10; i++) {
    if (env.context.askGemini('Summarise item ' + i, {}).ok) okCount++;
  }
  assert.strictEqual(env.state.fetchCalls.length, 3);
  assert.strictEqual(okCount, 3);
  const r = env.context.askGemini('one more', {});
  assert.ok(r.reason.indexOf('call limit') >= 0);
});

test('the limit counts failed calls too (a loop of errors cannot run away)', () => {
  const env = aiProject();
  env.state.fetchResponder = () => ({ getResponseCode: () => 429, getContentText: () => 'rate limited' });
  for (let i = 0; i < 10; i++) env.context.askGemini('try ' + i, {});
  assert.strictEqual(env.state.fetchCalls.length, 3);
});

test('a lower limit set by the learner is respected, and resetAiCallCount starts a new run', () => {
  const env = aiProject();
  env.run('AI_MAX_CALLS_PER_RUN = 1');
  env.context.askGemini('a', {});
  env.context.askGemini('b', {});
  assert.strictEqual(env.state.fetchCalls.length, 1);
  env.context.resetAiCallCount();
  env.context.askGemini('c', {});
  assert.strictEqual(env.state.fetchCalls.length, 2);
});

test('a refused call does not use up the call limit', () => {
  const env = aiProject();
  env.context.askGemini('mail me at a@example.com', {});
  assert.strictEqual(env.run('AI_CALLS_THIS_RUN'), 0);
});

test('a big loop over flagged rows makes zero calls', () => {
  const env = aiProject();
  for (let i = 0; i < 20; i++) {
    env.context.askGeminiAboutRows('x', [{ id: i, contains_personal_data: 'yes' }]);
  }
  assert.strictEqual(env.state.fetchCalls.length, 0);
});

test('more rows than AI_MAX_ROWS are refused', () => {
  const env = aiProject();
  const rows = [];
  for (let i = 0; i < 51; i++) rows.push({ n: i });
  const r = env.context.askGeminiAboutRows('x', rows);
  assert.strictEqual(r.ok, false);
  assert.strictEqual(env.state.fetchCalls.length, 0);
});

group('AI helper: failures never crash and never leak the key');

test('missing key: refuses, makes no call, says where to add it', () => {
  const env = aiProject();
  delete env.state.properties.GEMINI_API_KEY;
  const r = env.context.askGemini('hello', {});
  assert.strictEqual(r.ok, false);
  assert.ok(r.reason.indexOf('Script Properties') >= 0);
  assert.strictEqual(env.state.fetchCalls.length, 0);
});

test('error replies (400, 403, 404, 429, 500) come back as ok=false with the status', () => {
  [400, 403, 404, 429, 500].forEach((code) => {
    const env = aiProject();
    env.state.fetchResponder = () => ({ getResponseCode: () => code, getContentText: () => '{"error":{"message":"problem"}}' });
    const r = env.context.askGemini('hello', {});
    assert.strictEqual(r.ok, false);
    assert.ok(r.reason.indexOf('http ' + code) >= 0, r.reason);
  });
});

test('a thrown fetch error, bad JSON and an empty reply all come back as ok=false', () => {
  const env = aiProject();
  env.state.fetchResponder = () => { throw new Error('DNS error'); };
  assert.strictEqual(env.context.askGemini('a', {}).ok, false);
  env.state.fetchResponder = () => ({ getResponseCode: () => 200, getContentText: () => 'not json' });
  assert.strictEqual(env.context.askGemini('b', {}).ok, false);
  env.state.fetchResponder = () => ({ getResponseCode: () => 200, getContentText: () => '{"candidates":[]}' });
  assert.strictEqual(env.context.askGemini('c', {}).ok, false);
});

test('the key never appears in the log, the Run log or any reason text', () => {
  const env = salesProject();
  env.state.properties.GEMINI_API_KEY = 'TEST-KEY-123';
  env.state.fetchResponder = () => ({ getResponseCode: () => 403, getContentText: () => 'denied' });
  env.run('DIGEST_DRY_RUN = false; USE_AI_COMMENTARY = true');
  env.context.createWeeklyDigest();
  const everything = env.state.logLines.join('\n') + JSON.stringify(env.state.sheets['Run log'].data) +
    JSON.stringify(env.state.drafts);
  assert.ok(everything.indexOf('TEST-KEY-123') < 0);
});

// ---------------------------------------------------------------------------
group('The source files');

const sources = ['ai_helper.gs', 'weekly_digest.gs', 'invoice_check.gs'].map((f) => ({
  file: f,
  text: fs.readFileSync(path.join(ROOT, f), 'utf8')
}));

test('no script can send email: GmailApp.sendEmail and MailApp are not used', () => {
  sources.forEach((s) => {
    assert.ok(!/sendEmail\s*\(/.test(s.text), s.file + ' calls sendEmail');
    assert.ok(!/MailApp/.test(s.text), s.file + ' uses MailApp');
  });
});

test('no API key is written in the code', () => {
  sources.forEach((s) => {
    assert.ok(!/AIza[0-9A-Za-z_\-]{20,}/.test(s.text), s.file + ' contains something that looks like a key');
  });
});

test('every function has a one-line comment directly above it', () => {
  sources.forEach((s) => {
    const lines = s.text.split('\n');
    lines.forEach((line, i) => {
      if (/^function\s+\w+\s*\(/.test(line)) {
        const above = (lines[i - 1] || '').trim();
        assert.ok(/^\/\*\*.*\*\/$/.test(above), s.file + ' line ' + (i + 1) + ': ' + line + ' has no one-line comment above it');
      }
    });
  });
});

test('no em dashes in the code or comments', () => {
  sources.forEach((s) => assert.ok(s.text.indexOf('—') < 0, s.file + ' contains an em dash'));
});

test('no fixture or code uses arrow functions, classes or template strings (plain style for learners)', () => {
  sources.forEach((s) => {
    assert.ok(!/=>/.test(s.text), s.file + ' uses =>');
    assert.ok(!/`/.test(s.text), s.file + ' uses a template string');
    assert.ok(!/\bclass\s+\w+/.test(s.text), s.file + ' uses class');
  });
});

// ---------------------------------------------------------------------------
console.log('\n' + passed + ' passed, ' + failed + ' failed');
process.exit(failed === 0 ? 0 : 1);
