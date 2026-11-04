// Offline test of the 2 November 2026 block quiz helpers against in-memory fake Google Forms.
// Run from the repository root: node tests/test_block_sittings_20261102.cjs
const fs = require('fs'), vm = require('vm'), assert = require('node:assert/strict');
const pol = JSON.parse(fs.readFileSync('data/assessment_blocks_20261103.json', 'utf8'));
const GR = 'IUEA_Teaching_Plan/grader/';
const COHORTS = ['CML3111', 'CML3112', 'CML3113'];
const props = {}, forms = {}, logs = [], triggers = [];
const MC = 'MULTIPLE_CHOICE';
const J = x => JSON.parse(JSON.stringify(x));   // vm values live in another realm; compare plain copies
function fakeItem() {
  const it = { type: MC, title: '', choices: [] };
  const self = {
    getType: () => MC, getTitle: () => it.title, setTitle: t => { it.title = t; return self; }, setHelpText: () => self,
    createChoice: (text, correct) => ({ text, correct }), setChoices: c => { it.choices = c; return self; }, setPoints: () => self,
    setRequired: () => self, setFeedbackForCorrect: () => self, setFeedbackForIncorrect: () => self, asMultipleChoiceItem: () => self, raw: it };
  return self;
}
function fakeForm(id, title, nResponses) {
  const f = { id, title, desc: '', items: [], accepting: false, responses: nResponses || 0, closedMsg: '' };
  const api = {
    getId: () => id, getTitle: () => f.title, setTitle: t => { f.title = t; return api; }, setDescription: d => { f.desc = d; return api; }, getDescription: () => f.desc,
    getItems: type => (type ? f.items.filter(i => i.getType() === type) : f.items.slice()), deleteItem: i => { f.items.splice(f.items.indexOf(i), 1); },
    addMultipleChoiceItem: () => { const it = fakeItem(); f.items.push(it); return it; }, getResponses: () => new Array(f.responses).fill({}),
    isAccepting: () => f.accepting, isAcceptingResponses: () => f.accepting, setAcceptingResponses: v => { f.accepting = v; return api; },
    setCustomClosedFormMessage: m => { f.closedMsg = m; return api; }, setPublished: () => api, raw: f };
  return api;
}
const ctx = { console, Logger: { log: m => logs.push(String(m)) } };
vm.createContext(ctx);
ctx.PropertiesService = { getScriptProperties: () => ({ getProperties: () => Object.assign({}, props), getProperty: k => (k in props ? props[k] : null),
  setProperty: (k, v) => { props[k] = v; }, setProperties: (o) => { Object.assign(props, o); }, deleteProperty: k => { delete props[k]; } }) };
ctx.ScriptApp = { getProjectTriggers: () => triggers.slice(), deleteTrigger: t => { triggers.splice(triggers.indexOf(t), 1); },
  newTrigger: fn => ({ timeBased: () => ({ everyMinutes: () => ({ create: () => { triggers.push({ getHandlerFunction: () => fn }); } }), everyHours: () => ({ create: () => { triggers.push({ getHandlerFunction: () => fn }); } }) }) }) };
ctx.FormApp = { ItemType: { MULTIPLE_CHOICE: MC }, openById: id => forms[id], createFeedback: () => ({ setText: () => ({ build: () => ({}) }) }) };
ctx.Utilities = { formatDate: (d, tz, fmt) => (fmt === 'yyyy-MM-dd' ? d.toISOString().slice(0, 10) : d.toISOString()) };
ctx.Session = { getScriptTimeZone: () => 'Africa/Kampala' };
vm.runInContext(fs.readFileSync(GR + 'create_quiz_forms.gs', 'utf8'), ctx);
vm.runInContext(fs.readFileSync(GR + 'block_quiz_sittings_20261102.gs', 'utf8'), ctx);

// ---- the plan in the .gs agrees with the policy file
const plan = J(vm.runInContext('BLOCK_QUIZ_PLAN', ctx));
pol.blocks.forEach(b => {
  assert.deepEqual(plan[b.id].weeks, b.quiz_forms.map(q => q.week));
  assert.deepEqual(plan[b.id].forms, b.quiz_forms.map(q => q.form));
  assert.equal(plan[b.id].sittingClass, b.sitting_class);
  COHORTS.forEach(c => assert.equal(typeof ctx[`open_${b.label.replace(' ', '')}_${c}`], 'function', `open_${b.label}_${c}`));
  COHORTS.forEach(c => assert.equal(typeof ctx[`close_${b.label.replace(' ', '')}_${c}`], 'function'));
});
assert.deepEqual(plan.B1.weeks, [8, 9]); assert.deepEqual(plan.B2.weeks, [10, 11]);
assert.deepEqual(J(vm.runInContext('RETIRED_QUIZ_WEEKS_TO_CLOSE', ctx)), pol.retired_quiz_forms.map(q => q.week));
assert.deepEqual(J(vm.runInContext('RETIRED_QUIZ_WEEKS', ctx)), pol.retired_quiz_forms.map(q => q.week));
console.log('PASS plan in the .gs files matches data/assessment_blocks_20261103.json');

// ---- build the "live" forms the way they stand before the patch: Week 11 carries the OLD questions
const QD = J(vm.runInContext('QUIZ_DATA', ctx));
const OLD11 = ['1. Which values are produced?', '2. Why is this feature invalid for prediction?', '3. What does this error suggest?', '4. What is the improvement?', '5. What makes the comparison meaningful?'];
const links = {};
COHORTS.forEach(c => QD[c].weeks.forEach(w => {
  const id = `form-${c}-${w.week}`; const f = fakeForm(id, w.title);
  w.questions.forEach((q, i) => { const it = f.addMultipleChoiceItem(); it.setTitle(w.week === 11 ? OLD11[i] : q.n + '. ' + q.title); });
  forms[id] = f; links[`${c}|${w.week}`] = { formId: id, title: w.title };
}));
ctx.saveLinks_(links);
const lines = () => logs.splice(0).join('\n');

// ---- before replaceWeek11Questions: check reports 6 problems (3 cohorts x week 11? no: 3) and a sitting refuses to open
ctx.checkBlockQuizForms(); let out = lines();
assert.match(out, /PROBLEM CML3112 B2 Q10 \(week 11\)/); assert.match(out, /9 OK, 3 with problems/);
assert.throws(() => ctx.open_Block2_CML3112(), /NOT OPENED.*Nothing was opened/);
assert.equal(forms['form-CML3112-10'].raw.accepting, false, 'all or nothing: the Week 10 form must stay closed');
console.log('PASS old Week 11 forms are detected and the Block 2 sitting refuses to open (nothing opened)');

// ---- replaceWeek11Questions replaces only week 11, keeps ids and links, skips a form with responses
forms['form-CML3111-11'].raw.responses = 2;
const linksBefore = JSON.stringify(Object.fromEntries(Object.entries(vm.runInContext('loadLinks_()', ctx)).map(([k, v]) => [k, v.formId])));
ctx.replaceWeek11Questions(); out = lines();
assert.match(out, /SKIPPED CML3111 week 11: it already has 2 responses/); assert.match(out, /done: 2 forms replaced, 1 skipped/);
const linksAfter = JSON.stringify(Object.fromEntries(Object.entries(vm.runInContext('loadLinks_()', ctx)).map(([k, v]) => [k, v.formId])));
assert.equal(linksAfter, linksBefore, 'form ids and links must not change');
['CML3112', 'CML3113'].forEach(c => {
  const w = QD[c].weeks.find(x => x.week === 11), f = forms[`form-${c}-11`];
  assert.equal(f.raw.title, w.title); assert.match(f.raw.title, /choosing a model/); assert.equal(f.raw.desc, w.intro);
  assert.deepEqual(f.getItems().map(i => i.getTitle()), w.questions.map(q => q.n + '. ' + q.title));
  f.getItems().forEach((it, i) => assert.deepEqual(J(it.raw.choices).map(ch => ch.text), w.questions[i].choices.map(ch => ch.text)));
  assert.equal(f.getItems().length, 5);
});
assert.deepEqual(forms['form-CML3111-11'].getItems().map(i => i.getTitle()), OLD11, 'a form with responses is left alone');
['CML3112', 'CML3113', 'CML3111'].forEach(c => [8, 9, 10, 12, 13].forEach(wk => assert.equal(forms[`form-${c}-${wk}`].getItems().length, 5)));
console.log('PASS replaceWeek11Questions: Week 11 only, ids unchanged, responded form skipped');
forms['form-CML3111-11'].raw.responses = 0; ctx.replaceWeek11Questions(); lines();
assert.deepEqual(forms['form-CML3111-11'].getItems().map(i => i.getTitle()), QD.CML3111.weeks.find(x => x.week === 11).questions.map(q => q.n + '. ' + q.title));

// ---- all 12 block forms now pass the check
ctx.checkBlockQuizForms(); out = lines(); assert.match(out, /12 OK, 0 with problems/);

// ---- refreshBlockQuizIntros
forms['form-CML3113-9'].raw.responses = 1; forms['form-CML3112-8'].raw.accepting = true;
ctx.refreshBlockQuizIntros(); out = lines();
assert.match(out, /SKIPPED CML3113 week 9: it has 1 responses/); assert.match(out, /SKIPPED CML3112 week 8: it is open/); assert.match(out, /10 updated, 2 skipped/);
assert.match(forms['form-CML3111-8'].raw.desc, /last 20 minutes of Class 2/); assert.match(forms['form-CML3111-10'].raw.desc, /Class 4/);
forms['form-CML3113-9'].raw.responses = 0; forms['form-CML3112-8'].raw.accepting = false;
console.log('PASS refreshBlockQuizIntros skips responded and open forms');

// ---- the sittings
const t0 = Date.parse('2026-11-24T13:40:00+03:00');
ctx.Date = class extends Date { constructor(...a) { super(...(a.length ? a : [t0])); } static now() { return t0; } };
// openQuizFor uses new Date().getTime(); plannedDate check uses Utilities.formatDate mock (UTC date) -> 2026-11-24
ctx.open_Block2_CML3112(); out = lines();
assert.match(out, /OPENED CML3112 Block 2: Q9 and Q10 \(weeks 10 and 11\)/); assert.doesNotMatch(out, /NOTE: today is/);
assert.equal(forms['form-CML3112-10'].raw.accepting, true); assert.equal(forms['form-CML3112-11'].raw.accepting, true);
[8, 9, 12, 13].forEach(wk => assert.equal(forms[`form-CML3112-${wk}`].raw.accepting, false, 'week ' + wk + ' must stay closed'));
const L = vm.runInContext('loadLinks_()', ctx); assert.equal(L['CML3112|10'].closeAt, t0 + 24 * 3600 * 1000); assert.equal(L['CML3112|11'].closeAt, t0 + 24 * 3600 * 1000);
assert.deepEqual(J(Object.keys(vm.runInContext('loadPending_()', ctx))).sort(), ['form-CML3112-10', 'form-CML3112-11']);
assert.ok(triggers.length >= 1, 'a close trigger is installed');
ctx.close_Block2_CML3112(); lines();
assert.equal(forms['form-CML3112-10'].raw.accepting, false); assert.equal(forms['form-CML3112-11'].raw.accepting, false);
ctx.open_Block1_CML3113(); out = lines();
assert.match(out, /NOTE: today is 2026-11-24 in Kampala but CML3113 Block 1 is planned for 2026-11-13/); assert.match(out, /OPENED CML3113 Block 1: Q7 and Q8/);
assert.equal(forms['form-CML3113-8'].raw.accepting, true); assert.equal(forms['form-CML3113-9'].raw.accepting, true); assert.equal(forms['form-CML3113-10'].raw.accepting, false);
console.log('PASS open_Block1 and open_Block2 open exactly their two forms for 24 hours, close_Block closes them');

// ---- retiring Q11 and Q12
assert.throws(() => ctx.openQuizFor(12, 'CML3112'), /retired/); assert.throws(() => ctx.openQuizFor(13, 'CML3111'), /retired/);
forms['form-CML3111-12'].raw.accepting = true; ctx.addPending_('form-CML3111-12', t0 + 1000, 'CML3111|12');
ctx.retireQ11AndQ12Forms(); out = lines();
assert.match(out, /6 forms closed and retired, 0 not found/);
COHORTS.forEach(c => [12, 13].forEach(wk => { const f = forms[`form-${c}-${wk}`].raw; assert.equal(f.accepting, false); assert.match(f.closedMsg, /retired/); assert.equal(vm.runInContext('loadLinks_()', ctx)[`${c}|${wk}`].retired, true); }));
assert.ok(!('form-CML3111-12' in vm.runInContext('loadPending_()', ctx)), 'retired form removed from the pending-close list');
[8, 9, 10, 11].forEach(wk => assert.notEqual(vm.runInContext('loadLinks_()', ctx)[`CML3112|${wk}`].retired, true));
console.log('PASS retireQ11AndQ12Forms closes six forms and the open helper refuses weeks 12 and 13');

// ---- a block form that is marked retired blocks the sitting
const l2 = vm.runInContext('loadLinks_()', ctx); l2['CML3111|10'].retired = true; ctx.saveLinks_(l2);
assert.throws(() => ctx.open_Block2_CML3111(), /marked retired/);
console.log('PASS a retired flag on a block form stops the sitting');

// ---- generated gs files contain no non-ASCII bytes
['create_quiz_forms.gs', 'block_quiz_sittings_20261102.gs', 'apply_block_windows_20261102.gs'].forEach(n => assert.ok(fs.readFileSync(GR + n).every(b => b < 128), n + ' must be pure ASCII'));
console.log('PASS generated .gs files are pure ASCII');
// TESTS_PATCHED_20261103
