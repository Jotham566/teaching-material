// retireDemoForms() and showDemoRetirement() (grader/retire_demo_forms_20261103.gs) against fake Forms and a fake submission state.
// They must close and retire exactly the three DEMO forms, keep responses, open NO form window, touch no other form, and be safe to run twice.
// Run from the repository root: node tests/test_retire_demo_20261103.cjs
const fs = require('fs'), vm = require('vm'), assert = require('node:assert/strict');
const logs = [], store = {}, forms = {}, ids = {};
const key = k => k;
const mkForm = (id, accepting, responses) => ({ id, accepting, closedMessage: '', description: 'Deadline: 2026-12-15 14:00 (Kampala UTC+03:00)', responses,
  isAcceptingResponses() { return this.accepting; }, setAcceptingResponses(v) { this.accepting = v; return this; }, setCustomClosedFormMessage(m) { this.closedMessage = m; return this; },
  getResponses() { return this.responses; }, getDescription() { return this.description; }, setDescription(d) { this.description = d; } });
const keys = [];
['CML3111', 'CML3112', 'CML3113'].forEach(c => ['DEMO', 'ML_PROJECT', 'W10'].forEach(a => keys.push(`${c}|${a}`)));
keys.forEach((k, i) => {
  const id = 'form-' + i; ids[k] = id;
  forms[id] = mkForm(id, k.endsWith('|W10') /* a normal open form */, k.endsWith('|DEMO') ? [{ getId: () => 'r' + i, getTimestamp: () => new Date('2026-11-03T08:00:00Z'), getItemResponses: () => [] }] : []);
  store['IUEA_SUBMISSIONS_V1:' + k] = JSON.stringify({ formId: id, ready: true, uploadReady: true, openAt: k.endsWith('|DEMO') ? '2026-11-24T11:00:00+03:00' : '2099-01-01T11:00:00+03:00', closeAt: k.endsWith('|DEMO') ? '2026-12-15T14:00:00+03:00' : '2099-02-01T14:00:00+03:00', closedScanned: false });
});
const sheet = { getDataRange: () => ({ getValues: () => [['response_id']] }), appendRow() {}, getRange: () => ({ setValues() {} }) };
const ctx = {
  Logger: { log: m => logs.push(m) }, Date, Object, JSON, Math, Number, String, isFinite, Error, Array,
  PropertiesService: { getScriptProperties: () => ({
    getProperties: () => Object.assign({}, store), getProperty: k => (k === 'IUEA_SUBMISSION_BOOK_ID' ? 'book' : store[k] === undefined ? null : store[k]),
    setProperties: o => Object.assign(store, o), setProperty: (k, v) => { store[k] = v; } }) },
  LockService: { getScriptLock: () => ({ waitLock() {}, tryLock: () => true, releaseLock() {} }) },
  SpreadsheetApp: { openById: () => ({ getSheetByName: () => sheet }) },
  FormApp: { openById: id => { assert.ok(forms[id], 'unknown form ' + id); return forms[id]; } },
};
vm.createContext(ctx);
vm.runInContext(fs.readFileSync('IUEA_Teaching_Plan/grader/submission_forms.gs', 'utf8'), ctx);
vm.runInContext(fs.readFileSync('IUEA_Teaching_Plan/grader/retire_demo_forms_20261103.gs', 'utf8'), ctx);
assert.ok(fs.readFileSync('IUEA_Teaching_Plan/grader/retire_demo_forms_20261103.gs').every(b => b < 128), 'generated .gs must be pure ASCII');
assert.deepEqual(JSON.parse(JSON.stringify(ctx.DEMO_FORM_KEYS)), ['CML3111|DEMO', 'CML3112|DEMO', 'CML3113|DEMO']);

// before: the DEMO forms are not retired
ctx.showDemoRetirement(); assert.match(logs.pop(), /0 OK, 3 need attention/); logs.length = 0;
const before = {}; keys.filter(k => !k.endsWith('|DEMO')).forEach(k => { before[k] = store['IUEA_SUBMISSIONS_V1:' + k]; });
const windowsBefore = keys.map(k => { const s = JSON.parse(store['IUEA_SUBMISSIONS_V1:' + k]); return [k, s.openAt, s.closeAt]; });

ctx.retireDemoForms();
assert.match(logs.pop(), /3 retired, 0 not found .* No form window was opened/);
assert.equal(logs.filter(l => /^RETIRED CML31\d\d\|DEMO, 1 responses kept$/.test(l)).length, 3, JSON.stringify(logs));
['CML3111', 'CML3112', 'CML3113'].forEach(c => {
  const s = JSON.parse(store['IUEA_SUBMISSIONS_V1:' + c + '|DEMO']);
  assert.equal(s.retired, true); assert.equal(s.assessmentReleased, false); assert.ok(s.releaseEvidence.length >= 20); assert.ok(s.retiredAt);
  const f = forms[ids[c + '|DEMO']]; assert.equal(f.accepting, false); assert.match(f.closedMessage, /retired/); assert.equal(f.responses.length, 1);
  assert.equal(ctx.submissionAssessmentReleased_(c + '|DEMO', s), false);
});
// nothing else changed, and no window was opened or moved anywhere
keys.filter(k => !k.endsWith('|DEMO')).forEach(k => assert.equal(store['IUEA_SUBMISSIONS_V1:' + k], before[k], 'changed ' + k));
keys.forEach((k, i) => { const s = JSON.parse(store['IUEA_SUBMISSIONS_V1:' + k]); assert.deepEqual([k, s.openAt, s.closeAt], windowsBefore[i], 'window moved for ' + k); });
assert.equal(forms[ids['CML3112|W10']].accepting, true, 'an ordinary open form must not be closed by this');
assert.equal(forms[ids['CML3112|ML_PROJECT']].accepting, false, 'the project form was never opened');
logs.length = 0; ctx.showDemoRetirement(); assert.match(logs.pop(), /3 OK, 0 need attention/);
// idempotent
logs.length = 0; ctx.retireDemoForms(); assert.match(logs.pop(), /3 retired, 0 not found/);
logs.length = 0; ctx.showDemoRetirement(); assert.match(logs.pop(), /3 OK, 0 need attention/);
// a missing form is reported, not thrown
delete store['IUEA_SUBMISSIONS_V1:CML3111|DEMO']; logs.length = 0; ctx.retireDemoForms(); assert.match(logs.pop(), /2 retired, 1 not found/);
console.log('PASS retireDemoForms closes and retires the three DEMO forms, keeps responses, opens no window, touches nothing else, and is idempotent.');
