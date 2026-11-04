// gradebook.gs and grader/continuous_assessment.py must give the same quiz and assignment totals (35 and 160 marks, 15 percent each)
// AND (3 November 2026) the same provisional line (x of 55) and final total (out of 100) once the project parts are marked.
// 300 seeded random students are scored by both implementations and compared. Run from the repository root.
const fs = require('fs'), vm = require('vm'), assert = require('node:assert/strict'), cp = require('child_process');
const c = {}; vm.createContext(c); vm.runInContext(fs.readFileSync('IUEA_Teaching_Plan/grader/gradebook.gs', 'utf8'), c);
const J2 = x => JSON.parse(JSON.stringify(x));
const pol = JSON.parse(fs.readFileSync('data/assessment_blocks_20261103.json', 'utf8'));
assert.equal(c.weightTotal_(), 100);
assert.deepEqual(JSON.parse(JSON.stringify(c.WEIGHTS)), { quizzes: 15, challenges: 15, dataProject: 10, test1: 15, mlProject: 45 });
const w = pol.weights_percent;
assert.equal(c.WEIGHTS.quizzes, w.quizzes); assert.equal(c.WEIGHTS.challenges, w.assignments); assert.equal(c.WEIGHTS.dataProject, w.data_analysis_project);
assert.equal(c.WEIGHTS.test1, w.practical_test_1); assert.equal(c.WEIGHTS.mlProject, w.engineering_ml_project); assert.ok(!('demonstration' in w) && !('demo' in c.WEIGHTS));
assert.equal(c.ML_PART_A_MAX + c.ML_PART_B_MAX, pol.engineering_ml_project.marks); assert.deepEqual(J2(pol.engineering_ml_project.parts.map(p => [p.part, p.marks])), [['A', c.ML_PART_A_MAX], ['B', c.ML_PART_B_MAX]]);
assert.equal(c.provisionalOutOf_(), pol.provisional_mode.provisional_weight_total); assert.deepEqual(J2(c.PROJECT_INPUT_HEADERS), J2(pol.engineering_ml_project.parts.map(p => p.gradebook_column)));
assert.equal(c.PROVISIONAL_HEADER, pol.provisional_mode.gradebook_columns.provisional_text); assert.equal(c.PROJECT_STATUS_HEADER, pol.provisional_mode.gradebook_columns.project_status);
assert.equal(c.PROJECT_PENDING_TEXT, pol.provisional_mode.project_status_text.pending); assert.equal(c.PROJECT_MARKED_TEXT, pol.provisional_mode.project_status_text.marked);
// the gradebook block columns equal the policy file: quiz columns are Q1..Q12 (index = form number - 1), assignment columns follow CHALLENGE_IDS
const J = x => JSON.parse(JSON.stringify(x));
const quizCols = pol.blocks.map(b => b.quiz_forms.map(q => Number(q.form.slice(1)) - 1));
assert.deepEqual(J(c.COURSEWORK_BLOCKS.quizzes).map(b => b.cols), quizCols);
const ids = J(c.CHALLENGE_IDS);
assert.deepEqual(J(c.COURSEWORK_BLOCKS.challenges).map(b => b.cols.map(i => ids[i])), pol.blocks.map(b => b.assignment_parts.map(p => p.id)));

let seed = 20261103; const rnd = () => (seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296;
const pick = (max) => { const r = rnd(); return r < 0.2 ? '' : r < 0.35 ? 0 : r < 0.6 ? max : Math.floor(rnd() * (max + 1)); };
const students = [];
for (let i = 0; i < 300; i++) students.push({ cohort: ['CML3111', 'CML3112', 'CML3113'][i % 3],
  quizzes: Array.from({ length: 12 }, () => pick(5)), challenges: Array.from({ length: 11 }, () => pick(20)),
  dataProject: pick(100), test1: pick(100), mlProjectA: pick(30), mlProjectB: pick(15) });
// python receipts: weekly Q1..Q6 / W01..W06, then Q8..Q11 for the quiz columns Q7..Q10 (weeks 8 to 11), W08..W12; Q12 and Q13 are the retired columns
const quizIds = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q8', 'Q9', 'Q10', 'Q11', 'Q12', 'Q13'];
const asgIds = ['W01', 'W02', 'W03', 'W04', 'W05', 'W06', 'W08', 'W09', 'W10', 'W11', 'W12'];
const nz = v => (v === '' ? null : v);
const receipts = students.map((s, n) => { const m = {}; s.quizzes.forEach((v, i) => { if (v !== '') m[quizIds[i]] = v; }); s.challenges.forEach((v, i) => { if (v !== '') m[asgIds[i]] = v; });
  return { sid: 'S' + n, cohort: s.cohort, marks: m, da: nz(s.dataProject), t1: nz(s.test1), pa: nz(s.mlProjectA), pb: nz(s.mlProjectB) }; });
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
  assert.equal(q.rawOutOf, 35); assert.equal(a.rawOutOf, 160); compared++;
});
assert.ok(compared > 250, 'only ' + compared + ' students compared');
assert.ok(pendingSeen > 50 && markedSeen > 50, 'both modes must be exercised: pending ' + pendingSeen + ', marked ' + markedSeen);
console.log('PASS gradebook.gs and continuous_assessment.py agree for ' + compared + ' seeded students: quizzes out of 35, assignments out of 160, 15 percent each; provisional (x of 55) for ' + pendingSeen + ' pending and full totals out of 100 for ' + markedSeen + ' marked.');
// TESTS_PATCHED_20261103
