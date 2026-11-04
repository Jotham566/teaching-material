// applyBlockWindows() and showBlockWindows() against a fake submission state. Run from the repository root.
const fs = require('fs'), vm = require('vm'), assert = require('node:assert/strict');
const pol = JSON.parse(fs.readFileSync('data/assessment_blocks_20261103.json', 'utf8'));
const reg = JSON.parse(fs.readFileSync('data/assessments.json', 'utf8'));
const logs = [], calls = [];
const state = {};
reg.filter(r => /^CML31\d\d\|W(0[89]|1[0-2])$/.test(r.key)).forEach(r => { state[r.key] = { openAt: r.opens_at, closeAt: '2026-12-10T23:59:00+03:00' }; });  // old, wrong closes
const c = { Logger: { log: m => logs.push(m) }, submissionState_: () => state, setSubmissionWindow: (k, o, cl) => { calls.push([k, o, cl]); state[k].openAt = o; state[k].closeAt = cl; } };
vm.createContext(c); vm.runInContext(fs.readFileSync('IUEA_Teaching_Plan/grader/apply_block_windows_20261102.gs', 'utf8'), c);
assert.equal(JSON.parse(JSON.stringify(c.BLOCK_WINDOW_CALLS)).length, 15);
c.showBlockWindows(); assert.match(logs.pop(), /0 OK, 15 need attention/); logs.length = 0;
c.applyBlockWindows(); assert.equal(calls.length, 15); assert.match(logs.pop(), /15 set, 0 already correct, 0 left/);
// every call carries the closing time in the policy file and leaves the opening time as it was
pol.blocks.forEach(b => b.assignment_parts.forEach(p => Object.entries(b.assignment_closes).forEach(([code, close]) => {
  const call = calls.find(x => x[0] === `${code}|${p.id}`); assert.ok(call, `${code}|${p.id}`); assert.equal(call[2], close);
  assert.equal(call[1], reg.find(r => r.key === call[0]).opens_at);
})));
// A6 and the retired Test 2 are never touched
assert.ok(!calls.some(x => /W06|TEST2/.test(x[0])));
logs.length = 0; c.showBlockWindows(); assert.match(logs.pop(), /15 OK, 0 need attention/);
logs.length = 0; calls.length = 0; c.applyBlockWindows(); assert.equal(calls.length, 0); assert.match(logs.pop(), /0 set, 15 already correct/);
console.log('PASS applyBlockWindows sets 15 windows once, is idempotent, and showBlockWindows confirms them; A6 and Test 2 untouched.');
// TESTS_PATCHED_20261103
