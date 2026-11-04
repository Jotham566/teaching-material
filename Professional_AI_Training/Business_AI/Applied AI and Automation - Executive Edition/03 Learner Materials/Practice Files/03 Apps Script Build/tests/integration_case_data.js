'use strict';
// Run with:  node tests/integration_case_data.js   (from the "03 Apps Script Build" folder)
// Loads the FULL case-company CSVs into the mocked spreadsheet, runs the scripts end to end and
// compares the output with the answer key and the true figures held in verify_case_data.py.
// Needs the facilitator folders (04 and 05) to be present, so it is for the instructor only.

const assert = require('assert');
const fs = require('fs');
const path = require('path');
const { loadProject, readCsvValues } = require('./mocks');

const ROOT = path.join(__dirname, '..');
const EDITION = path.join(ROOT, '..', '..', '..');
const CASE = path.join(EDITION, '03 Learner Materials', 'Practice Files', '01 Case Company');
const KEY = path.join(EDITION, '04 Facilitator Materials', 'Answer Keys', 'invoice_errors_key.csv');
const PY = path.join(EDITION, '05 Course Maintenance', 'Build', 'data_gen', 'verify_case_data.py');

let passed = 0, failed = 0;
function test(name, fn) {
  try { fn(); passed++; console.log('  ok    ' + name); }
  catch (e) { failed++; console.log('  FAIL  ' + name + '\n        ' + String(e.message).split('\n').join('\n        ')); }
}
const J = (x) => JSON.stringify(x);
function same(a, b) { assert.strictEqual(J(a), J(b)); }

// ---- expected values, read from the Python file so they cannot drift ----
const py = fs.readFileSync(PY, 'utf8');
function pyList(name) {
  const m = py.match(new RegExp('^' + name + ' = \\[([^\\]]*)\\]', 'm'));
  assert.ok(m, 'cannot find ' + name + ' in verify_case_data.py');
  return m[1].replace(/\s+/g, ' ').split(',').map((s) => s.trim().replace(/^"|"$/g, '')).filter((s) => s !== '');
}
function pyDict(name) {
  const m = py.match(new RegExp('^' + name + ' = \\{([^}]*)\\}', 'm'));
  assert.ok(m, 'cannot find ' + name);
  const out = {};
  m[1].replace(/"([^"]+)":\s*(\d+)/g, (_, k, v) => { out[k] = Number(v); return ''; });
  return out;
}
const WEEKS = pyList('WEEKS');
const WEEK_REV = pyList('EXPECTED_WEEK_REVENUE').map(Number);
const WOW = pyList('EXPECTED_WOW_PCT').map(Number);
const MBALE = pyDict('EXPECTED_MBALE_REVENUE');
const OIL = pyDict('EXPECTED_OIL_UNITS');

// ---- answer key ----
const keyRows = readCsvValues(KEY);
const keyObjs = keyRows.slice(1).map((r) => { const o = {}; keyRows[0].forEach((h, i) => { o[h] = r[i]; }); return o; });
const TYPE_MAP = { wrong_total: 'WRONG_TOTAL', missing_po: 'MISSING_PO', vat_zero: 'ZERO_VAT', duplicate: 'DUPLICATE' };
// Expected flags as "row|FLAG". For a duplicate the script flags the second occurrence only.
const expectedFlags = [];
keyObjs.forEach((k) => {
  const rows = String(k.data_row_numbers).split(';').map((s) => Number(s.trim()) + 1); // data row n is sheet row n+1
  if (k.error_type === 'duplicate') expectedFlags.push(rows[rows.length - 1] + '|DUPLICATE');
  else rows.forEach((r) => expectedFlags.push(r + '|' + TYPE_MAP[k.error_type]));
});
expectedFlags.sort();

// ---- helpers ----
function withDates(values) { // Sheets turns 2026-08-03 into a Date; mimic that (UTC midnight)
  return values.map((row, r) => row.map((c, i) => (r > 0 && i === 0 && /^\d{4}-\d\d-\d\d$/.test(c) ? new Date(c + 'T00:00:00Z') : c)));
}
function invoiceEnv(asDates) {
  const env = loadProject(ROOT);
  const vals = readCsvValues(path.join(CASE, 'supplier_invoices.csv'));
  if (asDates) vals.forEach((row, r) => { if (r > 0) row[1] = new Date(row[1] + 'T00:00:00Z'); });
  env.makeSheet('supplier_invoices', vals);
  return env;
}
function salesEnv(rowFilter, asDates) {
  const env = loadProject(ROOT);
  let vals = readCsvValues(path.join(CASE, 'weekly_sales.csv'));
  if (rowFilter) vals = vals.filter((r, i) => i === 0 || rowFilter(r));
  if (asDates) vals = withDates(vals);
  env.makeSheet('weekly_sales', vals);
  return env;
}
const fmt = (n) => String(Math.round(Math.abs(n))).replace(/\B(?=(\d{3})+(?!\d))/g, ',');

console.log('\nInvoices: full supplier_invoices.csv against invoice_errors_key.csv');
const sheetFlags = (flags) => flags.map((f) => f.row + '|' + f.flag).sort();

test('sheet has 60 invoices and the key lists 8 planted errors', () => {
  const env = invoiceEnv(false);
  assert.strictEqual(env.state.sheets.supplier_invoices.data.length, 61);
  assert.strictEqual(keyObjs.length, 8);
  assert.strictEqual(expectedFlags.length, 8); // 4 wrong totals + 2 PO + 1 VAT + 1 duplicate
});
test('TOTAL_INCLUDES_VAT is true and right for the real file (every clean row matches qty x price x (1+VAT))', () => {
  const env = invoiceEnv(false);
  assert.strictEqual(env.run('TOTAL_INCLUDES_VAT'), true);
  const rows = env.context.valuesToObjects(env.state.sheets.supplier_invoices.data);
  const bad = rows.filter((r) => env.context.expectedTotal(r.qty, r.unit_price_ugx, r.vat_pct) !== r.total_ugx).length;
  assert.strictEqual(bad, 4); // only the 4 planted wrong totals
  env.run('TOTAL_INCLUDES_VAT = false');
  const badEx = rows.filter((r) => Math.abs(env.context.expectedTotal(r.qty, r.unit_price_ugx, r.vat_pct) - r.total_ugx) > 1).length;
  assert.ok(badEx > 40, 'with the wrong setting most rows would be flagged, got ' + badEx);
});
[false, true].forEach((asDates) => {
  test('flags are exactly the planted errors, no false positives (dates as ' + (asDates ? 'Date cells' : 'text') + ')', () => {
    const env = invoiceEnv(asDates);
    const flags = env.run('runInvoiceCheck()');
    same(sheetFlags(flags), expectedFlags);
  });
});
test('wrong-total details carry the key amounts', () => {
  const env = invoiceEnv(false);
  const flags = env.run('runInvoiceCheck()');
  keyObjs.filter((k) => k.error_type === 'wrong_total').forEach((k) => {
    const row = Number(k.data_row_numbers) + 1;
    const f = flags.find((x) => x.row === row && x.flag === 'WRONG_TOTAL');
    assert.strictEqual(f.invoice_id, k.invoice_id);
    assert.ok(f.detail.indexOf('Total is ' + fmt(k.total_ugx_in_file)) === 0, f.detail);
    assert.ok(f.detail.indexOf('plus VAT is ' + fmt(k.correct_total_ugx)) > 0, f.detail);
  });
  const vz = keyObjs.find((k) => k.error_type === 'vat_zero');
  assert.strictEqual(flags.find((x) => x.flag === 'ZERO_VAT').invoice_id, vz.invoice_id);
});
test('live run writes a Flags sheet with a heading and 8 rows; invoice sheet untouched', () => {
  const env = invoiceEnv(false);
  const before = J(env.state.sheets.supplier_invoices.data);
  env.run('INVOICE_DRY_RUN = false');
  env.run('runInvoiceCheck()');
  const fl = env.state.sheets.Flags.data;
  assert.strictEqual(fl.length, 9);
  same(fl.slice(1).map((r) => r[0] + '|' + r[3]).sort(), expectedFlags);
  assert.strictEqual(J(env.state.sheets.supplier_invoices.data), before);
  assert.strictEqual(env.state.sentEmails.length, 0);
});
test('dry run writes no Flags sheet', () => {
  const env = invoiceEnv(false);
  env.run('runInvoiceCheck()');
  assert.strictEqual(env.state.sheets.Flags, undefined);
});

console.log('\nWeekly digest: full weekly_sales.csv against verify_case_data.py');
test('sheet has 360 rows over 12 weeks', () => {
  const env = salesEnv(null, false);
  assert.strictEqual(env.state.sheets.weekly_sales.data.length, 361);
  same(WEEKS.length, 12);
});
[false, true].forEach((asDates) => {
  test('weekly revenue totals match the true values (dates as ' + (asDates ? 'Date cells' : 'text') + ')', () => {
    const env = salesEnv(null, asDates);
    const d = env.context.buildDigest(env.context.valuesToObjects(env.state.sheets.weekly_sales.data));
    same(Array.from(d.weeks), WEEKS);
    same(d.weeklyTotals.map((w) => w.total), WEEK_REV);
    assert.strictEqual(d.skippedRows, 0);
  });
});
test('week-on-week change of the total is right for every week, using the digest itself', () => {
  WEEKS.slice(1).forEach((w, i) => {
    const env = salesEnv((r) => r[0] <= w, false);
    const d = env.context.buildDigest(env.context.valuesToObjects(env.state.sheets.weekly_sales.data));
    assert.strictEqual(d.latestWeek, w);
    assert.strictEqual(d.totalLatest, WEEK_REV[i + 1]);
    assert.strictEqual(d.totalPrevious, WEEK_REV[i]);
    // the script rounds to 1 decimal, the key to 2
    assert.ok(Math.abs(d.totalChangePct - WOW[i]) <= 0.051, w + ': ' + d.totalChangePct + ' vs ' + WOW[i]);
  });
});
test('real latest week (2026-10-19): email body shows total, change and the Mbale row', () => {
  const env = salesEnv(null, false);
  const body = env.run('createWeeklyDigest()');
  assert.ok(body.indexOf('Latest week starting: 2026-10-19') >= 0);
  assert.ok(body.indexOf('TOTAL | ' + fmt(WEEK_REV[11]) + ' | ' + fmt(WEEK_REV[10]) + ' | +' + fmt(WEEK_REV[11] - WEEK_REV[10])) >= 0, body);
  assert.ok(body.indexOf('+' + WOW[10].toFixed(1) + '%') > 0 || body.indexOf('+' + (Math.round(WOW[10] * 10) / 10).toFixed(1) + '%') > 0, body);
  ['Jinja', 'Mbale', 'Iganga', 'Tororo', 'Soroti', 'Kamuli'].forEach((r) => assert.ok(body.indexOf('\n' + r + ' | ') >= 0, r));
});
test('Mbale drop is visible in the digest for the week of 2026-09-21', () => {
  const env = salesEnv((r) => r[0] <= '2026-09-21', false);
  const body = env.run('createWeeklyDigest()');
  const line = body.split('\n').find((l) => l.indexOf('Mbale | ') === 0);
  const pct = Math.round((MBALE['2026-09-21'] - MBALE['2026-09-14']) / MBALE['2026-09-14'] * 1000) / 10;
  assert.strictEqual(line, 'Mbale | ' + fmt(MBALE['2026-09-21']) + ' | ' + fmt(MBALE['2026-09-14']) + ' | -' + fmt(MBALE['2026-09-14'] - MBALE['2026-09-21']) + ' (' + pct.toFixed(1) + '%)');
  assert.ok(pct < -50);
  assert.ok(body.indexOf('Biggest fall: Mbale.') > 0, body);
});
test('Mbale recovers in the digest for 2026-10-05', () => {
  const env = salesEnv((r) => r[0] <= '2026-10-05', false);
  const d = env.context.buildDigest(env.context.valuesToObjects(env.state.sheets.weekly_sales.data));
  const m = d.table.find((t) => t.group === 'Mbale');
  assert.strictEqual(m.latest, MBALE['2026-10-05']);
  assert.strictEqual(m.previous, MBALE['2026-09-28']);
  assert.strictEqual(d.biggestRise, 'Mbale');
});
test('cooking oil spike is visible when the digest is grouped by product and summed on units (week of 2026-09-07)', () => {
  const env = salesEnv((r) => r[0] <= '2026-09-07', false);
  env.run("GROUP_COLUMN = 'product'");
  env.run("VALUE_COLUMN = 'units'");
  const body = env.run('createWeeklyDigest()');
  const oil = OIL['2026-09-07'], prev = OIL['2026-08-31'];
  const pct = Math.round((oil - prev) / prev * 1000) / 10;
  const line = body.split('\n').find((l) => l.indexOf('Cooking oil 20L jerrycan | ') === 0);
  assert.strictEqual(line, 'Cooking oil 20L jerrycan | ' + fmt(oil) + ' | ' + fmt(prev) + ' | +' + fmt(oil - prev) + ' (+' + pct.toFixed(1) + '%)');
  assert.ok(body.indexOf('Biggest rise: Cooking oil 20L jerrycan.') > 0, body);
  // and it falls back the week after
  const env2 = salesEnv((r) => r[0] <= '2026-09-14', false);
  env2.run("GROUP_COLUMN = 'product'"); env2.run("VALUE_COLUMN = 'units'");
  const line2 = env2.run('createWeeklyDigest()').split('\n').find((l) => l.indexOf('Cooking oil') === 0);
  assert.ok(line2.indexOf('| ' + fmt(OIL['2026-09-14']) + ' | ' + fmt(oil) + ' | -') > 0, line2);
});
test('live digest on the full data saves exactly one draft and sends nothing', () => {
  const env = salesEnv(null, false);
  env.run('DIGEST_DRY_RUN = false');
  env.run('createWeeklyDigest()');
  assert.strictEqual(env.state.drafts.length, 1);
  assert.strictEqual(env.state.sentEmails.length, 0);
  assert.strictEqual(env.state.fetchCalls.length, 0);
});

test('the hand-made summary differs from the digest weekly totals in exactly two weeks, and the digest email lists every week', () => {
  const env = salesEnv(null, false);
  const d = env.context.buildDigest(env.context.valuesToObjects(env.state.sheets.weekly_sales.data));
  const hand = readCsvValues(path.join(ROOT, 'last_month_summary_by_hand.csv'));
  same(hand[0], ['week_start', 'total_revenue_ugx']);
  same(hand.slice(1).map((r) => r[0]), WEEKS);
  const handTotals = hand.slice(1).map((r) => Number(r[1]));
  const wrongWeeks = d.weeklyTotals.filter((w, i) => w.total !== handTotals[i]).map((w) => w.week);
  assert.strictEqual(wrongWeeks.length, 2, 'weeks that differ: ' + wrongWeeks.join(', '));
  // the learner reads these totals in the digest, so each true total must appear in the email text
  const body = env.run('createWeeklyDigest()');
  WEEKS.forEach((w, i) => assert.ok(body.indexOf(w + ' | ' + fmt(WEEK_REV[i])) >= 0, 'week line missing for ' + w));
});

console.log('\n' + passed + ' passed, ' + failed + ' failed');
process.exit(failed === 0 ? 0 : 1);
