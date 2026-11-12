// 10 November 2026 policy (data/assessment_policy_20261110.json): assignments A1-A5 20 + quizzes Q1-Q5 20 + Practical Test 1 20 + project 40.
// gradebook.gs and grader/continuous_assessment.py must give the same quiz and assignment totals (25 and 100 raw marks, 20 each), the same
// provisional line (x of 60) and the same final total (out of 100) once the project parts are marked.
// 300 seeded random students are scored by gradebook.gs, by a plain-arithmetic oracle written from the policy file, and by Python. Run from the repository root.
const fs = require('fs'), vm = require('vm'), assert = require('node:assert/strict'), cp = require('child_process');
const c = {}; vm.createContext(c); vm.runInContext(fs.readFileSync('IUEA_Teaching_Plan/grader/gradebook.gs', 'utf8'), c);
const J2 = x => JSON.parse(JSON.stringify(x));
const pol = JSON.parse(fs.readFileSync('data/assessment_policy_20261110.json', 'utf8'));
const J = x => JSON.parse(JSON.stringify(x));
// gradebook.gs constants equal the 10 November 2026 policy file
assert.equal(c.weightTotal_(), pol.course_total); assert.equal(pol.course_total, 100);
assert.deepEqual(J(c.WEIGHTS), { quizzes: 20, challenges: 20, test1: 20, mlProject: 40 });
assert.equal(c.WEIGHTS.quizzes, pol.weights.quizzes); assert.equal(c.WEIGHTS.challenges, pol.weights.assignments);
assert.equal(c.WEIGHTS.test1, pol.weights.practical_test_1); assert.equal(c.WEIGHTS.mlProject, pol.weights.engineering_ml_project);
assert.ok(!('demo' in c.WEIGHTS) && !('test2' in c.WEIGHTS) && !('dataProject' in c.WEIGHTS));
const pj = pol.counted.engineering_ml_project;
assert.equal(c.ML_PART_A_MAX, pj.parts.A); assert.equal(c.ML_PART_B_MAX, pj.parts.B); assert.equal(c.ML_PART_A_MAX + c.ML_PART_B_MAX, pj.raw_max); assert.equal(pj.scaled_max, c.WEIGHTS.mlProject);
assert.equal(c.provisionalOutOf_(), pol.provisional.out_of); assert.equal(pol.provisional.out_of, 60);
assert.equal(c.QUIZ_COUNTED, pol.counted.quizzes.ids.length); assert.equal(c.QUIZ_MAX, pol.counted.quizzes.each_max);
assert.equal(c.CHALLENGE_COUNTED, pol.counted.assignments.ids.length); assert.equal(c.CHALLENGE_MAX, pol.counted.assignments.each_max);
assert.deepEqual(J(c.CHALLENGE_IDS).slice(0, c.CHALLENGE_COUNTED), pol.counted.assignments.ledger_ids);
assert.equal(pol.counted.practical_test_1.max, 100); assert.equal(pol.counted.practical_test_1.ledger_id, 'TEST1'); assert.equal(pj.ledger_id, 'ML_PROJECT');
assert.equal(c.PROVISIONAL_HEADER + ': x of 60 marks, y percent', pol.provisional.text.replace('Semester 1 provisional:', c.PROVISIONAL_HEADER + ':').replace('x of 60', 'x of 60'));
assert.deepEqual(J(c.PROJECT_INPUT_HEADERS), ['ML Project Part A', 'ML Project Part B']);
assert.ok(!c.hasOwnProperty('COURSEWORK_BLOCKS') && !c.hasOwnProperty('bestOfComponent_') && !c.hasOwnProperty('courseworkPolicy_'), 'the block / best-of machinery is retired');

let seed = 20261103; const rnd = () => (seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296;
const pick = (max) => { const r = rnd(); return r < 0.2 ? '' : r < 0.35 ? 0 : r < 0.6 ? max : Math.floor(rnd() * (max + 1)); };
const students = [];
for (let i = 0; i < 300; i++) students.push({ cohort: ['CML3111', 'CML3112', 'CML3113'][i % 3],
  quizzes: Array.from({ length: 12 }, () => pick(5)), challenges: Array.from({ length: 11 }, () => pick(20)),
  dataProject: pick(100), test1: pick(100), mlProjectA: pick(30), mlProjectB: pick(15) });
// python receipts (every item, including the ones that no longer count, so Python must ignore them): weekly Q1..Q6 / W01..W06, then Q8..Q11 for the quiz columns Q7..Q10 (weeks 8 to 11), W08..W12; Q12 and Q13 are the retired columns
const quizIds = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q8', 'Q9', 'Q10', 'Q11', 'Q12', 'Q13'];
const asgIds = ['W01', 'W02', 'W03', 'W04', 'W05', 'W06', 'W08', 'W09', 'W10', 'W11', 'W12'];
const nz = v => (v === '' ? null : v);
const receipts = students.map((s, n) => { const m = {}; s.quizzes.forEach((v, i) => { if (v !== '') m[quizIds[i]] = v; }); s.challenges.forEach((v, i) => { if (v !== '') m[asgIds[i]] = v; });
  return { sid: 'S' + n, cohort: s.cohort, marks: m, da: nz(s.dataProject), t1: nz(s.test1), pa: nz(s.mlProjectA), pb: nz(s.mlProjectB) }; });
// oracle written straight from the policy note: no best-of, no blocks, blank = 0
const r2 = x => Math.round(x * 100) / 100, num = v => (v === '' ? 0 : Number(v)), sum5 = a => a.slice(0, 5).reduce((t, v) => t + num(v), 0);
const oracle = s => { const q = r2(sum5(s.quizzes) * 4 / 5), a = r2(sum5(s.challenges) / 5), t = r2(num(s.test1) / 5);
  const done = s.mlProjectA !== '' && s.mlProjectB !== ''; const p = done ? r2((s.mlProjectA + s.mlProjectB) * 40 / 45) : null;
  return { q, a, t, p, prov: r2(a + q + t), final: done ? r2(a + q + t + p) : null }; };
students.forEach((s, n) => { const g = c.computeFinal_(Object.assign({}, s)), O = oracle(s);
  assert.equal(g.components.quizzes.weighted, O.q, 'quizzes vs policy oracle, student ' + n); assert.equal(g.components.challenges.weighted, O.a, 'assignments vs oracle, student ' + n);
  assert.equal(g.components.test1.weighted, O.t, 'test vs oracle'); assert.equal(g.provisional.marks, O.prov, 'provisional vs oracle'); assert.equal(g.final, O.final, 'final vs oracle, student ' + n);
  if (O.p !== null) assert.equal(g.components.mlProject.weighted, O.p); });
console.log('gradebook.gs matches the 10 November policy oracle for 300 seeded students');
const py = `
import json,sys
sys.path.insert(0,'IUEA_Teaching_Plan/grader')
from continuous_assessment import coursework_totals,semester_totals
data=json.load(sys.stdin);cur=[]
for d in data:
  for a,v in d['marks'].items(): cur.append(dict(cohort=d['cohort'],student_id=d['sid'],assessment=a,score=v,status='GRADED'))
  for a,k in (('DA_PROJECT','da'),('TEST1','t1')):
    if d[k] is not None: cur.append(dict(cohort=d['cohort'],student_id=d['sid'],assessment=a,score=d[k],status='GRADED'))
  pa,pb=d['pa'],d['pb']
  if pa is not None or pb is not None:
    full=pa is not None and pb is not None
    cur.append(dict(cohort=d['cohort'],student_id=d['sid'],assessment='ML_PROJECT',score=(pa+pb) if full else None,status='GRADED' if full else 'PART_MARKED',part_scores=dict(A=pa,B=pb)))
out={(r['cohort'],r['student_id']):r for r in coursework_totals(cur)}
tot={(r['cohort'],r['student_id']):r for r in semester_totals(cur,[(d['cohort'],d['sid']) for d in data])}
print(json.dumps([[out.get((d['cohort'],d['sid'])),tot[(d['cohort'],d['sid'])]] for d in data]))`;
const res = cp.spawnSync('python3', ['-I', '-B', '-c', py], { input: JSON.stringify(receipts), encoding: 'utf8' });
assert.equal(res.status, 0, res.stderr); const pyAll = JSON.parse(res.stdout); const pyRows = pyAll.map(x => x[0]); const pyTot = pyAll.map(x => x[1]);
let compared = 0, pendingSeen = 0, markedSeen = 0;
students.forEach((s, n) => {
  const g = c.computeFinal_(Object.assign({}, s));
  // provisional and final agree between the two implementations, to the hundredth
  const T = pyTot[n];
  assert.equal(g.provisional.marks, T.provisional.marks, 'provisional marks, student ' + n); assert.equal(g.provisional.percent, T.provisional.percent, 'provisional percent, student ' + n);
  assert.equal(g.provisional.text, T.provisional.text); assert.equal(g.projectStatus, T.project_status); assert.equal(g.projectPending, T.project.pending);
  assert.equal(g.final, T.final, 'final, student ' + n);
  if (g.projectPending) { pendingSeen++; assert.equal(g.final, null); assert.equal(g.band, null); } else { markedSeen++; assert.ok(g.final >= g.provisional.marks - 0.005 && g.final <= 100.005); }
  const p = pyRows[n]; if (!p) { assert.equal(g.components.quizzes.raw + g.components.challenges.raw, 0); return; }   // python lists only students with a graded mark
  const q = g.components.quizzes, a = g.components.challenges;
  assert.equal(q.raw, p.quizzes.earned, 'quiz earned, student ' + n); assert.equal(q.rawOutOf, p.quizzes.available, 'quiz available');
  assert.equal(a.raw, p.assignments.earned, 'assignment earned, student ' + n); assert.equal(a.rawOutOf, p.assignments.available, 'assignment available');
  assert.ok(Math.abs(q.weighted - p.quizzes.weighted) < 0.006, 'quiz weighted ' + q.weighted + ' vs ' + p.quizzes.weighted);
  assert.ok(Math.abs(a.weighted - p.assignments.weighted) < 0.006, 'assignment weighted ' + a.weighted + ' vs ' + p.assignments.weighted);
  assert.equal(q.rawOutOf, 25); assert.equal(a.rawOutOf, 100); compared++;
});
assert.ok(compared > 250, 'only ' + compared + ' students compared');
assert.ok(pendingSeen > 50 && markedSeen > 50, 'both modes must be exercised: pending ' + pendingSeen + ', marked ' + markedSeen);
console.log('PASS gradebook.gs and continuous_assessment.py agree for ' + compared + ' seeded students: quizzes out of 25, assignments out of 100, 20 percent each; provisional (x of 60) for ' + pendingSeen + ' pending and full totals out of 100 for ' + markedSeen + ' marked.');
// TESTS_PATCHED_20261103
