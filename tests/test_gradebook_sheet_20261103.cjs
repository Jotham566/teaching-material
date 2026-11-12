// The sheet side of gradebook.gs (10 November 2026 policy: 20 + 20 + 20 + 40, provisional out of 60): prepareGradesColumns(), recomputeAll() in provisional and full mode,
// and importMarkedResults() for the two project columns. A fake Grades sheet stands in for Google Sheets. Run from the repository root.
const fs = require('fs'), vm = require('vm'), assert = require('node:assert/strict');
const toasts = [];
let grid;   // array of rows; row 0 is the header row
const sheet = {
  getDataRange: () => ({ getValues: () => grid.map(r => r.slice()) }),
  getLastColumn: () => grid[0].length,
  getRange: (r, c, nr, nc) => ({
    getValues: () => { const out = []; for (let i = 0; i < nr; i++) { out.push(grid[r - 1 + i].slice(c - 1, c - 1 + nc)); } return out; },
    setValues: v => { for (let i = 0; i < v.length; i++) { while (grid[r - 1 + i].length < c - 1 + v[i].length) grid[r - 1 + i].push(''); for (let j = 0; j < v[i].length; j++) grid[r - 1 + i][c - 1 + j] = v[i][j]; }
      const w = Math.max.apply(null, grid.map(x => x.length)); grid.forEach(x => { while (x.length < w) x.push(''); }); }   // a real sheet is rectangular
  })
};
let csvById = {};
const ss = { getSheetByName: n => (n === 'Grades' ? sheet : null), toast: m => toasts.push(m), getActiveRange: () => ({ getRow: () => 2 }) };
const ctx = { SpreadsheetApp: { getActive: () => ss, getUi: () => ({ createMenu: () => ({ addItem() { return this; }, addSeparator() { return this; }, addToUi() {} }), alert() {} }) },
  DriveApp: { getFileById: id => ({ getBlob: () => ({ getDataAsString: () => csvById[id] }) }) },
  Utilities: { parseCsv: s => s.trim().split('\n').map(l => l.split(',')) }, console, Math, Number, String, JSON, Array, Object, Error, isFinite, isNaN, parseInt };
vm.createContext(ctx); vm.runInContext(fs.readFileSync('IUEA_Teaching_Plan/grader/gradebook.gs', 'utf8'), ctx);

const template = fs.readFileSync('IUEA_Teaching_Plan/grader/Grades_template.csv', 'utf8').split(/\r?\n/)[0].split(',');
// 1. the shipped template has the new columns and not the old ones
['ML Project Part A', 'ML Project Part B', 'Semester 1 provisional', 'Project', 'Final %', 'Band', 'Missing'].forEach(h => assert.ok(template.includes(h), h));
['ML Project', 'Demo', 'Practical Test 2', 'Data Analysis Project'].forEach(h => assert.ok(!template.includes(h), h));

// 2. an OLD live sheet (before this change): old ML Project and Demo columns, no project columns
const oldHeaders = template.filter(h => !['ML Project Part A', 'ML Project Part B', 'Semester 1 provisional', 'Project'].includes(h));
const at = oldHeaders.indexOf('Final %'); oldHeaders.splice(at, 0, 'ML Project', 'Demo');
function row(id, cohort, marks) { const r = oldHeaders.map(() => ''); r[oldHeaders.indexOf('student_id')] = id; r[oldHeaders.indexOf('cohort')] = cohort; Object.entries(marks).forEach(([k, v]) => { r[oldHeaders.indexOf(k)] = v; }); return r; }
const full = { Q1: 5, Q2: 5, Q3: 5, Q4: 5, Q5: 5, W01: 20, W02: 20, W03: 20, W04: 20, W05: 20, 'Practical Test 1': 100 };
// S4 holds only work that no longer counts (Q6 onward, W06 onward) and S5 has a full set plus a mix of non-counted zeros
const uncounted = { Q6: 5, Q7: 5, Q8: 5, Q9: 5, Q10: 5, W06: 20, W08: 20, W09: 20, W10: 20, W11: 20, W12: 20 };
grid = [oldHeaders.slice(), row('S1', 'CML3111', Object.assign({}, full, uncounted, { 'ML Project': 100, Demo: 100 })), row('S2', 'CML3112', {}), row('S3', 'CML3113', Object.assign({}, full)), row('S4', 'CML3111', uncounted)];
assert.throws(() => ctx.recomputeAll(), /missing columns: ML Project Part A, ML Project Part B.*prepareGradesColumns/);
ctx.prepareGradesColumns();
assert.match(toasts.pop(), /Added columns: ML Project Part A, ML Project Part B, Semester 1 provisional, Project/);
assert.deepEqual(grid[0].slice(-4), ['ML Project Part A', 'ML Project Part B', 'Semester 1 provisional', 'Project']);
assert.ok(grid[0].includes('ML Project') && grid[0].includes('Demo'), 'old columns must stay');
ctx.prepareGradesColumns(); assert.match(toasts.pop(), /already there/); assert.equal(grid[0].length, oldHeaders.length + 4);

// 3. provisional: nobody has project marks yet; leftover ML Project = 100 and Demo = 100 for S1 must be ignored
const H = n => grid[0].indexOf(n), cell = (r, n) => grid[r][H(n)];
ctx.recomputeAll();
assert.match(toasts.pop(), /Recomputed 4 rows/);
assert.equal(cell(1, 'Final %'), '', 'no final percentage while the project is pending');
assert.equal(cell(1, 'Band'), 'No band yet');
assert.equal(cell(1, 'Semester 1 provisional'), 'Semester 1 provisional: 60.00 of 60 marks, 100.00 percent');
assert.equal(cell(1, 'Project'), 'Project: PENDING');
assert.equal(cell(2, 'Semester 1 provisional'), 'Semester 1 provisional: 0.00 of 60 marks, 0.00 percent');   // a student with no submissions
assert.equal(cell(4, 'Semester 1 provisional'), 'Semester 1 provisional: 0.00 of 60 marks, 0.00 percent');   // Q6 onward and A6 onward add nothing
assert.equal(cell(2, 'Final %'), ''); assert.equal(cell(2, 'Project'), 'Project: PENDING');
assert.equal(cell(2, 'Missing'), 'Practical Test 1; quizzes: Q1, Q2, Q3, Q4, Q5; assignments: A1, A2, A3, A4, A5');
assert.ok(!/project/i.test(cell(2, 'Missing')), 'pending is not listed as missing');
assert.equal(cell(1, 'Missing'), ''); assert.equal(cell(1, 'Challenges done'), 5);
// 4. only Part A marked for S3: still provisional
grid[3][H('ML Project Part A')] = 26;
ctx.recomputeAll();
assert.equal(cell(3, 'Final %'), ''); assert.equal(cell(3, 'Project'), 'Project: PENDING'); assert.match(cell(3, 'Semester 1 provisional'), /^Semester 1 provisional: 60\.00 of 60 marks, 100\.00 percent$/);
// 5. both parts marked for S3 (26 + 10 = 36 raw -> 32 of 40): 60 + 32 = 92, full total out of 100, provisional line cleared
grid[3][H('ML Project Part B')] = 10;
ctx.recomputeAll();
assert.equal(cell(3, 'Final %'), 92); assert.equal(cell(3, 'Project'), 'Project: marked'); assert.equal(cell(3, 'Semester 1 provisional'), '');
assert.equal(cell(3, 'Band'), 'Awaiting Faculty bands');   // bands are placeholders until the Faculty rules are entered
// 6. S2 marked 0 and 0: counted as zero because the project IS marked
grid[2][H('ML Project Part A')] = 0; grid[2][H('ML Project Part B')] = 0;
ctx.recomputeAll(); assert.equal(cell(2, 'Final %'), 0); assert.equal(cell(2, 'Project'), 'Project: marked');
// 7. a bad project mark stops the run loudly and writes nothing
const snapshot = JSON.stringify(grid); grid[1][H('ML Project Part A')] = 31;
assert.throws(() => ctx.recomputeAll(), /Invalid mark 31; expected 0 to 30/); grid[1][H('ML Project Part A')] = '';
assert.equal(JSON.stringify(grid), snapshot);
// 8. importMarkedResults accepts the two project columns with their own maxima, and refuses the old ones
csvById.A = 'student_id,status,score,maximum\nS1,OK,24,30\nS2,OK,18.5,30\n';
ctx.importMarkedResults('A', 'ML Project Part A'); assert.equal(cell(1, 'ML Project Part A'), 24); assert.equal(cell(2, 'ML Project Part A'), 18.5);
csvById.B = 'student_id,status,score,maximum\nS1,OK,12,15\n';
ctx.importMarkedResults('B', 'ML Project Part B'); assert.equal(cell(1, 'ML Project Part B'), 12);
csvById.WRONG = 'student_id,status,score,maximum\nS1,OK,12,100\n';
assert.throws(() => ctx.importMarkedResults('WRONG', 'ML Project Part B'), /maximum mismatch/);
assert.throws(() => ctx.importMarkedResults('A', 'ML Project'), /Unknown assessment column/);
assert.throws(() => ctx.importMarkedResults('A', 'Demo'), /Unknown assessment column/);
assert.throws(() => ctx.importMarkedResults('A', 'Data Analysis Project'), /Unknown assessment column/);
assert.throws(() => ctx.importMarkedResults('A', 'Practical Test 2'), /Unknown assessment column/);
// S1 now has Part A 24 and Part B 12: 36 * 40 / 45 = 32 on top of 60
ctx.recomputeAll(); assert.equal(cell(1, 'Final %'), 92); assert.equal(cell(1, 'Project'), 'Project: marked');
// 9. pure ASCII
assert.ok(fs.readFileSync('IUEA_Teaching_Plan/grader/gradebook.gs').every(b => b < 128));
console.log('PASS gradebook sheet: prepareGradesColumns, provisional mode, Part A only, full total, zero-marked project, bad marks, project imports; 10 November 2026 weights.');
