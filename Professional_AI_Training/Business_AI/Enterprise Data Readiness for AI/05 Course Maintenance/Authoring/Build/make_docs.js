// Builds the Word documents for Enterprise Data Readiness for AI from docs_data.json: Participant Workbook, Course Plan and Tutor Guide, Glossary, Setup Guide.
//   python3 export_docs_data.py && node make_docs.js
const fs = require('fs'), path = require('path');
const D = require('docx');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle, HeadingLevel, AlignmentType, LevelFormat, PageBreak, Footer, PageNumber } = D;
const ROOT = path.resolve(__dirname, '..', '..', '..');
const INK = '1F2328', BODYC = '3B4046', SOFT = '6A6F75', LAKE = 'B04A2B', LINE = 'C9C5BC';   // one ink, one accent (used for links only), hairlines; no fills
const W = 9638;          // A4 with 1.5 cm side margins: 11906 - 2*1134

const run = (t, o = {}) => new TextRun({ text: t, font: 'Calibri', size: 22, color: BODYC, ...o });
const P = (t, o = {}) => new Paragraph({ spacing: { after: 120, line: 276 }, ...o, children: Array.isArray(t) ? t : [run(t)] });
const H1 = t => new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 360, after: 160 }, children: [new TextRun({ text: t, font: 'Cambria', bold: true, size: 36, color: INK })] });
const H2 = t => new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 240, after: 100 }, children: [new TextRun({ text: t, font: 'Cambria', bold: true, size: 28, color: INK })] });
const H3 = t => new Paragraph({ heading: HeadingLevel.HEADING_3, spacing: { before: 160, after: 60 }, children: [new TextRun({ text: t, font: 'Calibri', bold: true, size: 24, color: INK })] });
const B = (t, lvl = 0) => new Paragraph({ numbering: { reference: 'bul', level: lvl }, spacing: { after: 60, line: 264 }, children: Array.isArray(t) ? t : [run(t)] });
const N = t => new Paragraph({ numbering: { reference: 'num', level: 0 }, spacing: { after: 60, line: 264 }, children: Array.isArray(t) ? t : [run(t)] });
const bold = t => run(t, { bold: true });
const none = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
const hair = { style: BorderStyle.SINGLE, size: 4, color: LINE };
const heavy = { style: BorderStyle.SINGLE, size: 12, color: INK };
function cell(t, w, o = {}) {
  const paras = (Array.isArray(t) ? t : [t]).map(x => new Paragraph({ spacing: { after: 40, line: 252 }, children: typeof x === 'string' ? [run(x, { size: o.size || 20, bold: o.bold, color: o.bold ? INK : BODYC })] : x }));
  return new TableCell({ width: { size: w, type: WidthType.DXA }, borders: { top: none, left: none, right: none, bottom: o.head ? heavy : hair }, margins: { top: 80, bottom: 80, left: o.first ? 0 : 120, right: 100 }, children: paras });
}
function table(header, rows, widths, o = {}) {
  const tot = widths.reduce((a, b) => a + b, 0);
  return new Table({ width: { size: tot, type: WidthType.DXA }, columnWidths: widths, rows: [
    new TableRow({ tableHeader: true, children: header.map((h, i) => cell(h, widths[i], { head: true, bold: true, first: i === 0, size: o.size || 20 })) }),
    ...rows.map((r, ri) => new TableRow({ cantSplit: true, children: r.map((c, i) => cell(c, widths[i], { first: i === 0, size: o.size || 20, bold: (i === 0 && o.boldFirst) || (o.hl && o.hl(ri, r)) })) }))] });
}
function callout(t) {
  return new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: [W], rows: [new TableRow({ children: [new TableCell({ width: { size: W, type: WidthType.DXA }, borders: { top: heavy, bottom: hair, left: none, right: none }, margins: { top: 140, bottom: 120, left: 0, right: 0 }, children: (Array.isArray(t) ? t : [t]).map(x => new Paragraph({ spacing: { after: 70, line: 264 }, children: typeof x === 'string' ? [run(x)] : x })) })] })] });
}
const gap = () => new Paragraph({ spacing: { after: 100 }, children: [] });
const save = async (d, rel) => { const p = path.join(ROOT, rel); fs.mkdirSync(path.dirname(p), { recursive: true }); fs.writeFileSync(p, await Packer.toBuffer(d)); console.log('wrote', rel); };

const PORTRAIT = { size: { width: 11906, height: 16838 }, margin: { top: 1134, bottom: 1134, left: 1134, right: 1134 } };
const LANDSCAPE = { size: { width: 11906, height: 16838, orientation: D.PageOrientation.LANDSCAPE }, margin: { top: 1134, bottom: 1134, left: 1134, right: 1134 } };
const WL = 16838 - 2 * 1134;   // landscape content width
// A document is a list of sections: { children, landscape }. A plain array is one portrait section.
function doc2(title, sections, footerText) {
  if (!sections.length || !sections[0].children) sections = [{ children: sections }];
  return new Document({
    creator: 'Jotham Martin Wambi', title,
    styles: { default: { document: { run: { font: 'Calibri', size: 22 } } } },
    numbering: { config: [
      { reference: 'bul', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 270 } } } }, { level: 1, format: LevelFormat.BULLET, text: '–', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 1000, hanging: 270 } } } }] },
      { reference: 'num', levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 340 } } } }] },
      { reference: 'num2', levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 340 } } } }] }] },
    sections: sections.map(s => ({ properties: { page: s.landscape ? LANDSCAPE : PORTRAIT },
      footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [run(`${footerText}   Page `, { size: 18, color: SOFT }), new TextRun({ children: [PageNumber.CURRENT], font: 'Calibri', size: 18, color: SOFT })] })] }) },
      children: s.children })) });
}

const data = JSON.parse(fs.readFileSync(path.join(__dirname, 'docs_data.json'), 'utf8'));
const T = data.totals, S = data.sessions;
const COURSE = 'Enterprise Data Readiness for AI';
const pageBreak = () => new Paragraph({ children: [new PageBreak()] });
const H1p = t => new Paragraph({ heading: HeadingLevel.HEADING_1, pageBreakBefore: true, spacing: { before: 0, after: 160 }, children: [new TextRun({ text: t, font: 'Cambria', bold: true, size: 36, color: INK })] });
const titleBlock = (t, sub) => [new Paragraph({ spacing: { before: 200, after: 60 }, children: [new TextRun({ text: t, font: 'Cambria', bold: true, size: 48, color: INK })] }), ...(sub ? [new Paragraph({ spacing: { after: 200 }, children: [new TextRun({ text: sub, font: 'Calibri', size: 28, color: SOFT })] })] : [])];
const ruled = (n = 3) => [new Table({ width: { size: W - 540, type: WidthType.DXA }, columnWidths: [W - 540], indent: { size: 540, type: WidthType.DXA }, rows: Array.from({ length: n }, () => new TableRow({ cantSplit: true, height: { value: 400, rule: D.HeightRule.EXACT }, children: [new TableCell({ width: { size: W - 540, type: WidthType.DXA }, borders: { top: none, left: none, right: none, bottom: hair }, children: [new Paragraph({ spacing: { after: 0 }, children: [] })] })] })) })];
const N2 = t => new Paragraph({ numbering: { reference: 'num2', level: 0 }, spacing: { after: 60, line: 264 }, children: [run(t)] });
const lead = (a, b, o = {}) => new Paragraph({ spacing: { after: o.after === undefined ? 70 : o.after, line: 264 }, keepNext: !!o.keepNext, children: [bold(a + ' '), run(b)] });
const bl = (a, b) => B([bold(a + ' '), run(b)]);
const joinList = a => a.length <= 1 ? a.join('') : a.slice(0, -1).join(', ') + ' and ' + a[a.length - 1];
const mins = s => `about ${s.minutes_spoken} minutes`;
const hours = (T.words / 130 / 60).toFixed(1);
const plural = (n, w) => `${n} ${w}${n === 1 ? '' : 's'}`;
const BLOCK_TEXT = {
  'Case and recall': 'Recall questions on the last session and the Kitara case for today.',
  'Teaching': 'The concepts, plain words first, with the business consequence.',
  'Live demonstration': 'The tutor runs code on the Kitara data. Leaders follow the result and data colleagues follow the code.',
  'Break': '',
  'Workshop on your organisation': 'Pairs complete the numbered tasks in the Participant Workbook with the named file from Workpiece Templates.',
  'Decision and wrap-up': 'The leader answers the decision question aloud. The tutor reads the summary.',
};

// ============================================================ 1. PARTICIPANT WORKBOOK
async function workbook() {
  const c = [];
  c.push(...titleBlock('Participant Workbook', COURSE));
  c.push(P('Twelve sessions of two hours. This workbook holds the task pages, the decision questions and the vocabulary for every session, and four pages that the slides refer to.'));

  c.push(H1('How to use the course'));
  c.push(H3('The pair'));
  c.push(P('Each organisation sends a decision maker and a data or IT colleague. The pairing rule is that the two attend together where possible. The decision maker is the CIO, CTO, chief data officer, head of operations or a business owner. The colleague works in data, IT or information management.'));
  c.push(B('The decision maker answers the decision question at the end of each session, names the owners, and signs off the three workpieces.'));
  c.push(B('The data or IT colleague runs the team notebook, counts the results and checks the numbers that go on the pages.'));
  c.push(B('Both write the answers to the workshop tasks. Leaders do not write code.'));
  c.push(P('The course runs either as a cohort of organisations or in house for one organisation. The sessions and pages are the same.'));
  c.push(H3('The shape of a session'));
  c.push(table(['Block', 'Minutes', 'What happens'], data.shape.map(([b, m]) => [b, String(m), BLOCK_TEXT[b] || '']), [3000, 1100, 5538], { boldFirst: true }));
  c.push(P(''));
  c.push(H3('What to have open'));
  c.push(B('This workbook, on paper or on screen.'));
  c.push(B('The workbook file named at the top of each session, from the folder Workpiece Templates.'));
  c.push(B('The team notebook for the session in Google Colab. The Setup Guide explains how to open it.'));
  c.push(B('Documents that are not confidential. Personal data stays out of every document and nothing leaves your laptop.'));

  c.push(H1('Five dimensions and five levels'));
  c.push(P('Every score in the course uses these five dimensions and five levels. Each score needs one piece of evidence that someone outside the team could check.'));
  c.push(table(['Dimension', 'What it covers'], [
    ['Use cases and sponsorship', 'Named AI uses, each with a business owner and an executive who backs it.'],
    ['Data: inventory, quality and metadata', 'A list of sources with owners, quality that is measured, and descriptions that make data findable.'],
    ['Platform and pipelines', 'Where data is stored and how it moves, with a check at each step and an owner for each alert.'],
    ['Protection and law', 'Where personal data sits, which law applies and what leaves the country.'],
    ['People and governance', 'Roles, policies, a decision forum, a risk register and review dates.'],
  ], [3200, 6438], { boldFirst: true }));
  c.push(P(''));
  c.push(table(['Level', 'Name', 'What it looks like', 'Evidence you would expect'], data.levels_guide, [700, 1300, 3900, 3738], { size: 19, boldFirst: true }));

  c.push(H1p('The three workpieces'));
  c.push(P('No exam is set. The learning is carried by three workpieces, each built on your own organisation.'));
  c.push(table(['Workpiece', 'What it contains', 'Files'], [
    ['1. Baseline scorecard. Session 2', 'Five dimensions scored 1 to 5. Each score has evidence items and a named person who could verify them. The summary gives each dimension mean, the evidence-adjusted mean, the overall level and the weakest dimension. A target level for each dimension. The name of the executive who signs it off.', 'Readiness Scorecard.xlsx'],
    ['2. Search pilot report. Session 7', 'At least 30 test questions with the right document marked. Recall at 3, 5 and 10 and mean reciprocal rank for each method tested. A failure list with fixes. A permission test. The limits of the test. The named person who approves production.', 'Search Test Sheet.xlsx and the page Search pilot report outline'],
    ['3. Roadmap and board presentation. Session 12', 'A roadmap of up to 20 work items with effort, value, dependency and start month. A target score for each dimension. A board paper with the decision asked, the baseline, the plan, cost lines, risks and measures. A ten-minute presentation.', 'Roadmap Planner.xlsx, Board Paper Outline.docx and the page Board presentation outline'],
  ], [2400, 5300, 1938], { boldFirst: true }));

  c.push(P(''));
  c.push(H3('Pages at the end of this workbook'));
  c.push(B('Pipeline map. Used in Session 8.'));
  c.push(B('Data protection map. Used in Session 9.'));
  c.push(B('Search pilot report outline. Used in Session 7.'));
  c.push(B('Board presentation outline. Used in Session 12.'));

  S.forEach(s => {
    c.push(H1p(`Session ${s.no}. ${s.title}`));
    c.push(lead('Question.', s.question, { after: 60 }));
    c.push(lead('Result you leave with.', s.result, { after: 60 }));
    const files = [...s.workbooks]; const pages = s.pages;
    const open = [];
    if (files.length) open.push('From Workpiece Templates: ' + joinList(files) + '.');
    if (pages.length) open.push('Pages in this workbook: ' + joinList(pages) + '.');
    if (!files.length && !pages.length) open.push('No template file. Task 1 describes the sheet you make.');
    open.push('Team notebook: ' + s.notebook + '.');
    c.push(lead('Open.', open.join(' '), { after: 60 }));
    c.push(H2('Workshop tasks'));
    s.workshop.forEach((w, i) => {
      c.push(new Paragraph({ keepNext: true, keepLines: true, spacing: { before: 140, after: 40, line: 264 }, indent: { left: 540, hanging: 340 }, children: [run(`${i + 1}.  `, { bold: true, color: INK }), run(w.task, { color: INK })] }));
      c.push(...ruled(2));
    });
    c.push(H2('Decide'));
    c.push(new Paragraph({ keepNext: true, keepLines: true, spacing: { after: 40, line: 264 }, children: [bold('Decide. '), run(s.decision.q)] }));
    c.push(...ruled(2));
    c.push(H2('Vocabulary'));
    s.vocab.forEach(v => c.push(new Paragraph({ keepLines: true, spacing: { after: 70, line: 260 }, children: [bold(v.term + '. '), run(v.meaning)] })));
  });

  // ---- pages the slides refer to
  const secs = [{ children: c }];
  const rows8 = n => Array.from({ length: n }, () => null);
  const emptyTable = (header, widths, n, o = {}) => new Table({ width: { size: widths.reduce((a, b) => a + b, 0), type: WidthType.DXA }, columnWidths: widths, rows: [
    new TableRow({ tableHeader: true, cantSplit: true, children: header.map((h, i) => cell(h, widths[i], { head: true, bold: true, first: i === 0, size: o.size || 20 })) }),
    ...rows8(n).map(() => new TableRow({ cantSplit: true, height: { value: o.h || 820, rule: D.HeightRule.ATLEAST }, children: widths.map((w, i) => cell('', w, { first: i === 0 })) }))] });
  const lw = [1500, 2700, 3400, 2900, 4070];   // landscape pipeline map: sums to WL
  secs.push({ landscape: true, children: [
    H1('Pipeline map'),
    P('Session 8. Pick one AI use. Write one row for each step on the path from the source system to the search or model. Name the owner of every alert by role.'),
    emptyTable(['Step', 'Input', 'Check', 'Owner of the alert', 'What happens on failure'], lw, 8, { h: 700 }),
  ] });
  const dw = [1900, 2200, 2300, 2000, 1500, 2600, 2070];
  secs.push({ landscape: true, children: [
    H1('Data protection map'),
    P('Session 9. Copy every source from Data Inventory.xlsx into the first column. Write the registration status with the regulator in the law column. Mark special categories, such as health data, in the personal data kinds column.'),
    emptyTable(['Source', 'Personal data kinds', 'Law that applies', 'Where stored', 'Leaves the country (Y or N)', 'Legal basis or check needed', 'Owner'], dw, 8, { h: 700, size: 19 }),
  ] });
  const pc = [];
  pc.push(H1('Search pilot report outline'));
  pc.push(P('Session 7. One or two pages. The scores and the permission test come from Search Test Sheet.xlsx.'));
  const sec = (h, prompt, n = 3) => { pc.push(H3(h)); pc.push(new Paragraph({ keepNext: true, spacing: { after: 20, line: 252 }, children: [run(prompt, { size: 20, color: SOFT })] })); pc.push(...ruled(n)); };
  sec('1. Question set', 'How many questions, who wrote them, and how many of each kind: plain, old version, other language, restricted.', 2);
  sec('2. Method', 'Which documents and which users the test covered, the date, the search methods compared and their settings, how a hit is counted, and how queries and results are logged and for how long they are kept.', 3);
  pc.push(H3('3. Results by method'));
  pc.push(emptyTable(['Method', 'Recall at 3', 'Recall at 5', 'Recall at 10', 'Mean reciprocal rank'], [2638, 1750, 1750, 1750, 1750], 4, { h: 520 }));
  pc.push(new Paragraph({ spacing: { before: 60, after: 120 }, children: [run('Recall at 10 is the number of questions with a rank filled in, divided by the number of questions.', { size: 19, color: SOFT })] }));
  pc.push(H3('4. Failure list'));
  pc.push(emptyTable(['Question id', 'Failure type', 'What came back', 'Fix'], [1400, 2100, 3300, 2838], 5, { h: 560 }));
  pc.push(new Paragraph({ spacing: { before: 60, after: 120 }, children: [run('Failure types: stale version, paraphrase, other language, wrong passage, missing document.', { size: 19, color: SOFT })] }));
  pc.push(H3('5. Permissions test'));
  pc.push(emptyTable(['User', 'Question', 'Restricted document id', 'In top 5 without the filter (Y or N)', 'In top 5 with the filter (Y or N)'], [1500, 3100, 1700, 1700, 1638], 5, { h: 560, size: 19 }));
  pc.push(new Paragraph({ spacing: { before: 60, after: 120 }, children: [run('A pass is N with the filter on.', { size: 19, color: SOFT })] }));
  sec('6. Limits', 'What the test does not show.', 3);
  sec('7. Recommendation', 'Approve, approve with conditions or do not approve. Name the person who approves production and what that person must have seen.', 3);
  secs.push({ children: pc });
  const bc = [];
  bc.push(H1('Board presentation outline'));
  bc.push(P('Session 12. Ten minutes and six slides. Put the decision first and ask for it again at the end.'));
  const slides = [
    ['1. Decision asked', '1', 'The amount, the period and what it buys, in one sentence.'],
    ['2. Baseline', '2', 'The five scores, the evidence-adjusted mean, and the weakest dimension with what it blocks.'],
    ['3. Plan', '3', 'The one page roadmap. What is done in 30, 90 and 365 days. The items that cannot slip.'],
    ['4. Cost lines', '1', 'People, hosting, licences, evaluation and support. One-off or recurring. What is already funded.'],
    ['5. Measures', '1', 'Three measures, each with a baseline, a target and the date it will be measured.'],
    ['6. Risks, owners and rescore dates', '2', 'The five highest risks, each with an owner, and at least one about personal data. The dates of the rescores.'],
  ];
  slides.forEach(([h, m, p]) => {
    bc.push(new Paragraph({ keepNext: true, spacing: { before: 200, after: 30 }, children: [bold(h + '.  '), run(m + (m === '1' ? ' minute' : ' minutes'), { color: SOFT })] }));
    bc.push(new Paragraph({ keepNext: true, spacing: { after: 20, line: 252 }, children: [run(p, { size: 20, color: SOFT })] }));
    bc.push(...ruled(3));
  });
  secs.push({ children: bc });
  await save(doc2('Participant Workbook', secs, `${COURSE}   Participant Workbook`), '03 Learner Materials/Participant Workbook.docx');
}

// ============================================================ 2. COURSE PLAN AND TUTOR GUIDE
const LIBS = [
  ['sentence-transformers', 'Downloads a small model on first use and needs the internet. Session 6 Task 5 and one demonstration slide.', 'The download is a one-off and it is slow. The stand-in meaning search ran earlier in the notebook and shows the method. The real model is optional for the exercise.'],
  ['chromadb', 'A vector store that writes to a folder. Session 6, shown as syntax only.', 'Say what the code does. It stores the chunks with a status label and asks for the three nearest to the question, keeping only current documents. If it will not run, the point stands without the output.'],
  ['pgvector and psycopg2', 'Needs a running PostgreSQL server with the vector extension. Session 6, shown as syntax only.', 'This slide is for reading. It will not run in Colab, and nobody is expected to run it. The message is that search and the filter can sit in the database the bank already runs.'],
  ['pandera', 'Installed with pip. Session 4, one demonstration slide.', 'The import path has changed between versions, so a colleague installing it checks the current documentation. The rules on the slide are the point, and the six rules in the notebook do the same job with pandas.'],
  ['great_expectations', 'Installed with pip, with an API that changes between versions. Session 4, one demonstration slide.', 'Say that the rule is the point. The company behind it reports that its cloud product closed and that the open Core project continues under a new steward, so the team checks the package and licence before building on it.'],
  ['presidio', 'Installed with pip, plus a language model that its documentation names. Session 9, one demonstration slide and Task 5 in the notebook.', 'Detection is model based and misses some items, so the pattern-based masking in the notebook is the working method. If Presidio will not install, show the slide and keep the check and the sample reading.'],
  ['dagster', 'Installed with pip. Session 8, one demonstration slide.', 'The slide is for reading. It shows the same three steps with a retry policy. Apache Airflow does the same job with a different shape.'],
  ['duckdb and pyarrow', 'Installed with pip install pyarrow duckdb. Session 8, one demonstration slide.', 'The same zones appear in the SQL slide just before it. Say that DuckDB reads a Parquet file in place and answers an ordinary SQL question, and carry on.'],
  ['docling', 'Fetches model files on first use. Session 5, one demonstration slide.', 'The first run is slow. Compare with the pypdf and pdfplumber results already on the screen, and invite teams to try it on their hardest files in their own time.'],
  ['ragas', 'Named in the tool list as optional.', 'No slide or notebook cell uses it. Nothing to say.'],
];
const libSay = (name) => LIBS.find(l => l[0] === name);

async function plan() {
  const c = [];
  c.push(...titleBlock('Course plan and tutor guide', COURSE));
  c.push(callout([[bold(`${data.course.total_hours} hours. ${data.course.sessions} sessions of ${data.course.hours_per_session} hours. Free tools only.`)], data.course.start + ' ' + data.course.end]));

  c.push(H1('1. Course shape and audience'));
  c.push(P(`The audience is a decision maker and a data or IT colleague from the same East African organisation, such as a bank, insurer, telco, manufacturer or government body.`));
  c.push(P(`The course has ${data.course.sessions} sessions. Every session has the same six blocks.`));
  c.push(table(['Block', 'Minutes', 'What happens'], data.shape.map(([b, m]) => [b, String(m), BLOCK_TEXT[b] || '']), [3000, 1100, 5538], { boldFirst: true }));
  c.push(P(''));
  c.push(P('The case is Kitara Group, a fictional bank and insurer in Kampala with a subsidiary in Nairobi and about 1,800 staff. All data in the course is fictional and the currency is UGX. The same case runs through all twelve sessions. The workshops move the work to the participants\' own organisation.'));
  c.push(H3('Modules'));
  data.modules.forEach(([m, name, rng, desc]) => c.push(bl(`Module ${m}, ${name}. Sessions ${rng[0]} to ${rng[rng.length - 1]}.`, desc)));
  c.push(H3('Dimensions, levels and workpieces'));
  c.push(P(`Readiness is scored on five dimensions (${data.dimensions.join('; ')}) and five levels (${data.levels.join(', ').toLowerCase()}). Each score needs one piece of evidence that someone outside the team could check. Three workpieces carry the assessment: ${Object.entries(data.workpieces).map(([k, v]) => `${v.toLowerCase()} in Session ${k}`).join(', ')}. There is no exam. KLAi issues no certificate for the course.`));
  c.push(H3('What was built'));
  c.push(table(['Item', 'Quantity'], [
    ['Class slides', `${T.slides} slides in ${data.course.sessions} decks`],
    ['Animated slides', `${T.animated} slides with ${T.clicks} click reveals`],
    ['Read-aloud notes', `Every slide, about ${hours} hours of script at 130 words a minute`],
    ['Demonstration slides', `${T.code_slides} slides with code`],
    ['Vocabulary', `${T.vocab} terms`],
    ['Workshop tasks', `${T.workshop_tasks} tasks, each with a worked Kitara example in this guide`],
    ['Team notebooks', `${data.course.sessions} student notebooks and ${data.course.sessions} solution notebooks, ${T.notebook_tasks} tasks in all`],
    ['Workbooks and templates', `${data.templates.length} files in Workpiece Templates`],
  ], [3000, 6638], { boldFirst: true }));

  c.push(H1('2. How a pair attends'));
  c.push(P('A decision maker and a data or IT colleague attend together where possible. This is a preference. The course runs either as a cohort of organisations or in house for one organisation, and both ways are acceptable.'));
  c.push(table(['Block', 'Decision maker', 'Data or IT colleague'], [
    ['Case and recall', 'Answers the recall questions aloud.', 'Answers the recall questions aloud.'],
    ['Teaching', 'Follows the plain-word explanation and the business consequence.', 'Follows the same slides and notes the technical word after each plain one.'],
    ['Live demonstration', 'Reads the result on the screen and asks what it means for a decision.', 'Follows the code on a laptop and repeats the steps in the team notebook after the tutor.'],
    ['Workshop', 'Names owners, classes, targets and the decision. Writes the answers on the Participant Workbook page.', 'Counts, runs the notebook and checks the numbers that go on the page.'],
    ['Decision and wrap-up', 'Answers the decision question aloud.', 'Notes the answer and what must be done to support it.'],
  ], [2000, 3800, 3838], { boldFirst: true }));
  c.push(P(''));
  c.push(P('When only one of the two can attend a session, ask that person to brief the other the same day from the Participant Workbook page for the session. Ask in Session 1 who will attend and note which organisations send a pair.'));

  c.push(H1('3. What is in each folder'));
  c.push(table(['Folder', 'Contents', 'Who receives it'], [
    ['00 Start Here.txt', 'Overview of the course, the folders and the steps before class.', 'Tutor'],
    ['01 Course Overview', 'Course Roadmap (one page).pdf, and the editable .pptx.', 'Participants'],
    ['02 Class Slides', `${T.slides} slides in ${data.course.sessions} decks, numbered in teaching order. Every slide has speaker notes written as a script.`, 'Tutor'],
    ['03 Learner Materials', 'Participant Workbook.docx (task pages, decision questions, vocabulary and the four pages that slides refer to). Setup Guide.docx (send before Session 1). Glossary.docx (every vocabulary term). Workpiece Templates (' + data.templates.join(', ') + '). Practice Files: data (the Kitara files and DATA DICTIONARY.txt), data.zip, and notebooks (one student notebook for each session).', 'Participants'],
    ['04 Facilitator Materials', 'Course Plan and Tutor Guide.docx (this guide). Benchmark and Design Report.docx. Playback and Rehearsal Checklist.txt. run_all_labs.py. Lab Solutions (one solution notebook for each session).', 'Tutor only'],
    ['05 Course Maintenance', 'Authoring (sources and build scripts, with README - Read First.txt), Research Notes.txt and Verification Record.txt.', 'Tutor only'],
  ], [2300, 5738, 1600], { size: 19, boldFirst: true }));
  c.push(P(''));
  c.push(P('The file answer_key.json stays in the data folder for the tutor. It is left out of data.zip.'));

  c.push(H1('4. Before the course'));
  [['Host data.zip.', 'Put data.zip (in 03 Learner Materials/Practice Files) where participants can download it. Give them the link to paste between the quotation marks after DATA_ZIP_URL in the first cell of each notebook, or let each participant upload the file when the cell asks.'],
   ['Check Colab accounts.', 'Every participant needs a free Google account. Send the Setup Guide two weeks ahead and ask each person to run the first notebook cell before Session 1. Pair anyone without an account with a colleague who has one.'],
   ['Run the labs.', 'Run run_all_labs.py in 04 Facilitator Materials, then open each solution notebook that uses a heavy library in Colab and run it once. Section 6 lists them. The next section of this guide names which cells need Colab.'],
   ['Rehearse.', 'Read the notes aloud once for each session and change wording that does not sound like you. Play every animated slide in PowerPoint in Slide Show mode. The Playback and Rehearsal Checklist lists each one with its click count.'],
   ['Check licences.', 'Open the licence file or model card of each tool marked check in the Setup Guide list. Read the primary texts named in section 10 of the Benchmark and Design Report before Session 9 and Session 10.'],
   ['Collect document samples.', 'Before Session 5 ask each participant to choose 50 documents from one shared drive. The documents must be non-confidential and hold no personal data. Ask for the written approval of the person who owns the documents, and keep the approvals. The documents stay on the participant\'s laptop.'],
  ].forEach(([a, b]) => c.push(bl(a, b)));

  c.push(H1('5. Timetable'));
  c.push(table(['No.', 'Session and question', 'Result', 'Deck', 'Workbooks'], S.map(s => [String(s.no), [[run(s.title, { bold: true, size: 17, color: INK })], s.question], s.result, `${s.slides} slides, ${s.animated} animated, ${s.clicks} clicks, ${mins(s)} of notes`, s.workbooks.concat(s.pages.map(p => 'Page: ' + p)).join('; ') || 'None']), [500, 2600, 2700, 1900, 1938], { size: 17, boldFirst: true }));

  c.push(H1('6. Heavy-library cells and what to say if one fails'));
  c.push(P('Cells that use these libraries need pip installs, downloads or a server. Run each in Colab once before the course. The notebooks work without them. Cells that depend on a library that did not run are skipped by run_all_labs.py when it runs with --allow-missing-libs.'));
  c.push(table(['Library', 'What it needs, and where it appears', 'What to say if it fails'], LIBS.map(l => [l[0], l[1], l[2]]), [1700, 3400, 4538], { size: 18, boldFirst: true }));
  c.push(P(''));
  c.push(P('The Session 5 notebook installs the Tesseract program and poppler with apt-get, which works in Colab. If the install fails, show the scan results from the slide and give out the OCR confidence list the notebook printed in your own run.'));

  S.forEach(s => {
    c.push(H1p(`Session ${s.no}. ${s.title}`));
    c.push(lead('Question.', s.question, { after: 50 }));
    c.push(lead('Result.', s.result, { after: 50 }));
    c.push(lead('Deck.', `${s.deck_file}. ${s.slides} slides, ${s.animated} animated with ${s.clicks} click reveals. About ${s.minutes_spoken} minutes of read-aloud notes.`, { after: 50 }));
    c.push(lead('Workbooks.', (s.workbooks.concat(s.pages.map(p => 'page ' + p + ' in the Participant Workbook')).join('; ') || 'None. Task 1 describes the sheet the participants make.') + ` Notebook: ${s.notebook}.`, { after: 50 }));
    c.push(H3('Teaching sequence'));
    const demoNos = new Set(s.demo.map(d => d.no));
    const sl = s.slide_list; const half = Math.ceil(sl.length / 2); const rows = [];
    for (let i = 0; i < half; i++) {
      const a = sl[i], b = sl[i + half];
      const f = x => x ? [String(x.no), demoNos.has(x.no) ? [[run(x.title, { bold: true, size: 17, color: INK })]] : x.title] : ['', ''];
      rows.push([...f(a), ...f(b)]);
    }
    c.push(new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: [500, 4319, 500, 4319], rows: rows.map(r => new TableRow({ cantSplit: true, children: r.map((x, i) => cell(x, [500, 4319, 500, 4319][i], { first: i === 0, size: 17 })) })) }));
    c.push(new Paragraph({ spacing: { before: 60, after: 100 }, children: [run('Slides 1 to 3 are the title, outcomes and words slides. Bold titles are the live demonstration.', { size: 18, color: SOFT })] }));
    c.push(H3('Demonstration'));
    s.demo.forEach(d => c.push(B(`Slide ${d.no}. ${d.title}${d.libs.length ? '. Needs ' + d.libs.join(' and ') + (d.syntax_only ? ', shown as syntax only' : '') : ''}.`)));
    c.push(H3('Cells that only run in Colab'));
    const libs = [...new Set([...s.heavy_cells.flatMap(h => h.libs), ...s.demo.flatMap(d => d.libs)])];
    const where = lib => [...s.demo.filter(d => d.libs.includes(lib)).map(d => 'slide ' + d.no), ...s.heavy_cells.filter(h => h.libs.includes(lib)).map(h => 'notebook ' + h.where)];
    if (s.no === 5) c.push(B('The setup of the OCR cells installs Tesseract and poppler with apt-get. This works in Colab and may fail on a laptop.'));
    if (!libs.length && s.no !== 5) c.push(P('None. Every cell in this session runs with pandas, numpy and matplotlib, and the notebook has no library to install.'));
    libs.forEach(lib => { const l = libSay(lib); c.push(B([bold(lib + ' (' + where(lib).join(', ') + '). '), run('If it fails: ' + (l ? l[2] : ''))])); });
    c.push(H3('Workshop answer key'));
    s.workshop.forEach((w, i) => {
      c.push(new Paragraph({ keepNext: true, spacing: { before: 100, after: 30, line: 264 }, indent: { left: 540, hanging: 340 }, children: [run(`${i + 1}.  `, { bold: true, color: INK }), run(w.task, { color: INK })] }));
      c.push(new Paragraph({ keepLines: true, spacing: { after: 60, line: 264 }, indent: { left: 540 }, children: [bold('Kitara example. '), run(w.example)] }));
    });
    c.push(H3('Decision question'));
    c.push(new Paragraph({ keepNext: true, spacing: { after: 40, line: 264 }, children: [run(s.decision.q, { bold: true, color: INK })] }));
    c.push(new Paragraph({ spacing: { after: 60, line: 264 }, children: [bold('A sound answer. '), run(s.decision.a)] }));
  });

  c.push(H1p('7. Workpiece checklists'));
  c.push(P('Mark a workpiece complete when every line under Complete is true. Otherwise mark it needs revision and write which line failed. The participants keep their own work. Look at it on their screen.'));
  const check = (h, ses, files, complete, revise) => {
    c.push(H2(h)); c.push(P(`Session ${ses}. Files: ${files}.`, { keepNext: true }));
    c.push(H3('Complete when')); complete.forEach(x => c.push(B(x)));
    c.push(H3('Needs revision when')); revise.forEach(x => c.push(B(x)));
  };
  check('Workpiece 1. Baseline scorecard', 2, 'Readiness Scorecard.xlsx', [
    'The organisation and the date are entered.',
    'Each of the five dimensions has at least one evidence item, up to six, and each item is scored 1 to 5 against the Levels guide tab.',
    'Every item names who could verify it. Evidence seen is Y only where someone outside the team has seen the evidence.',
    'The summary shows the mean and the evidence-adjusted mean for each dimension, the overall level, and the weakest dimension. Tied dimensions are both named.',
    'A target level is set for each dimension.',
    'One sentence says what the weakest dimension blocks for the first AI use, and a named executive signs off the scorecard.'],
    ['A dimension has no evidence item.', 'An item has no verifier, or Evidence seen is Y for evidence that only the team has seen.', 'The weakest dimension is missing, or the sentence on what it blocks is missing.', 'A target level is missing for any dimension.', 'The sign-off names no executive.']);
  check('Workpiece 2. Search pilot report', 7, 'Search Test Sheet.xlsx and the one page report', [
    'The Tests sheet holds at least 30 questions in the words staff use. Each has a document id and a phrase from the right passage.',
    'At least 3 questions are ones where an old version gives a different answer, and some are ones where staff would use none of the words in the document.',
    'Every question has a rank, or a blank when the right document is not in the top 10. Recall at 3 and 5 and mean reciprocal rank show on the sheet, and recall at 10 is worked out from the ranks.',
    'Every miss has a failure type, and every group of misses has a fix.',
    'The Permission test sheet holds at least 5 questions that the named user must not answer. Each ran with and without the filter.',
    'The report states the scope, the test set, the scores for each method, the failure list, the permission test, logging and retention, the limits and the named person who approves production.'],
    ['Fewer than 30 questions, or every question repeats words from its answer passage.', 'Scores are given for one method and the report does not say that other methods were not tested.', 'A permission row shows Y with the filter on and the report still calls the pilot ready.', 'A hit is counted when the right document appears but the chunk shown does not hold the answer, and the report does not say so.', 'The limits or the approver are missing.']);
  check('Workpiece 3. Roadmap and board presentation', 12, 'Roadmap Planner.xlsx, Readiness Scorecard.xlsx and Board Paper Outline.docx', [
    'The roadmap lists up to 20 work items that close the scorecard gaps. Each has effort in person-days, a value from 1 to 5, a dependency, a start month and a duration.',
    'No row in the Dependency check column shows Starts before dependency ends. The chain of dependent items that sets the end date is named.',
    'The busiest month is found, and either a named person covers it or an item moves.',
    'Each dimension has a target score at month 12 and a driving action. The numbers are labelled as targets, and the date of the first rescore is given.',
    'The board paper has the six core sections: decision asked, baseline, plan, cost lines, risks and measures. Cost lines come from the organisation\'s own quotes. Each benefit is a hypothesis with a baseline and a measure. The five highest risks each have an owner, and one concerns personal data.',
    'The leader presented the paper in ten minutes to another team, with the decision at the start and again at the end.'],
    ['A dependency flag remains.', 'A target is written as if it were a result, or a return on investment is quoted with no baseline.', 'A cost line comes from a web page and has no quote behind it.', 'A risk has no owner.', 'The presentation runs over ten minutes, or the first rescore has no date.']);

  c.push(H1('8. Running the pairing and the room'));
  c.push(table(['', 'Cohort of organisations', 'One organisation in house'], [
    ['Group size', '8 to 12 organisations, with two or three people from each.', 'One organisation, one or more pairs.'],
    ['Seating', 'One table for each organisation, with the pair side by side facing the screen so that the leader can see the colleague\'s laptop.', 'Pairs at tables of two, facing the screen.'],
    ['Document samples', 'Each organisation brings its own 50 non-confidential documents with written approval.', 'The organisation chooses the 50 documents and one person holds the approval.'],
    ['Workshops', 'Each pair works on its own organisation. The tutor visits each table and reads the failure list or the map with the pair.', 'Each pair works on its own area. Pairs may work on different AI uses.'],
    ['Session 12 presentation', 'Two organisations present to each other.', 'Present to another pair, or to a manager from another department.'],
    ['Confidentiality between tables', 'Each organisation shows its own work and no other organisation\'s. Share no document on the main screen.', 'Not applicable between organisations. Keep in-house documents on the participants\' laptops.'],
  ], [2000, 3900, 3738], { size: 19, boldFirst: true }));
  c.push(P(''));
  c.push(P('In the workshop, ask the leader to speak first on each decision line, then ask the colleague to confirm the number. If one of the pair dominates, ask the leader to write the owners and the colleague to read the figures aloud.'));

  c.push(H1('9. Handling confidential material'));
  [['Non-confidential documents only.', 'Participants use documents that are not confidential, with the written approval of the person who owns them.'],
   ['No personal data.', 'No document may hold names, phone numbers, identity numbers, account numbers or health details. If a participant finds personal data in a document, they leave that document out.'],
   ['Nothing leaves the laptop.', 'Participants do not upload their own documents to Colab, to a chat assistant or to the tutor. The team notebooks run on the Kitara files. Participants open their own documents on their own laptop and record the results in a sheet.'],
   ['Kitara data is fictional.', 'The names, phone numbers and identity numbers in the Kitara files do not belong to real people. The phone numbers sit in a block set aside for the course.'],
   ['If a document turns out to be confidential.', 'Ask the participant to close it and continue with a Kitara document.'],
   ['Teaching summary.', 'Everything said about the law in Session 9 is a teaching summary and not legal advice.']]
    .forEach(([a, b]) => c.push(bl(a, b)));

  c.push(H1('10. What is verified and what is not'));
  c.push(P('The Verification Record in 05 Course Maintenance has the full list. In summary:'));
  c.push(H3('Checked'));
  [`All ${data.course.sessions} decks build with every slide fitting its text at the engine's minimum sizes, and each deck passes the PowerPoint validator.`,
   'The notes pass the read-aloud checks, and the course-level check finds no duplicate vocabulary or repeated sentences.',
   'Code on slides and in notebooks that needs only pandas, numpy, matplotlib or SQLite was run on the Kitara data, and the slide output matches.',
   'All solution notebooks ran top to bottom with run_all_labs.py. Cells that need the heavy libraries were skipped.',
   'Counts in this guide were computed from the decks and content files.'].forEach(x => c.push(B(x)));
  c.push(H3('Not checked'));
  ['Code that uses sentence-transformers, chromadb, pgvector with psycopg2, pandera, great_expectations, presidio, dagster, duckdb and docling was never executed. It was read against the documentation.',
   'The primary legal texts and the licence files of the tools were not read. The law and licence statements come from search results and secondary sources.',
   'PowerPoint playback of the animations was not tested.',
   'Nothing was rehearsed aloud.',
   'Google Colab was not used to run the notebooks.'].forEach(x => c.push(B(x)));
  await save(doc2('Course plan and tutor guide', c, `${COURSE}   Course plan and tutor guide`), '04 Facilitator Materials/Course Plan and Tutor Guide.docx');
}

// ============================================================ 3. GLOSSARY
async function glossary() {
  const v = [...data.vocab].sort((a, b) => a.term.localeCompare(b.term, 'en', { sensitivity: 'base' }));
  const c = titleBlock('Glossary', `${v.length} terms from the ${data.course.sessions} sessions, in alphabetical order.`);
  c.push(table(['Term', 'Plain meaning', 'Where you meet it', 'Session'], v.map(x => [x.term, x.meaning, x.example || 'See the session slides.', String(x.session)]), [1800, 3600, 3238, 1000], { size: 19, boldFirst: true }));
  await save(doc2('Glossary', c, `${COURSE}   Glossary`), '03 Learner Materials/Glossary.docx');
}

// ============================================================ 4. SETUP GUIDE
async function setup() {
  const c = [];
  c.push(...titleBlock('Setup Guide', `${COURSE}. Before Session 1`));
  c.push(P('Everything here is free. Allow about thirty minutes.'));
  c.push(H1('What to bring'));
  c.push(B('A laptop with a browser and a charger.'));
  c.push(B('A free Google account. Colab and Google Sheets use it.'));
  c.push(B('A spreadsheet program. Google Sheets, Excel and LibreOffice all work.'));
  c.push(B('50 documents from one shared drive, ready by Session 5. They must be non-confidential, hold no personal data, and have the written approval of the person who owns them. Choose a mix: old and new, long and short, PDFs, scans and Word files.'));
  c.push(B('A pen. The Participant Workbook has ruled space for your answers.'));
  c.push(H3('Approval note'));
  c.push(P('A short email from the document owner is enough. It can follow this wording.'));
  c.push(callout(['I approve the use of the documents listed below in the training Enterprise Data Readiness for AI. They are not confidential and hold no personal data. They stay on the participant\'s laptop.', 'Name and role of the owner:', 'Date:', 'List or folder:']));

  c.push(H1('The team notebook'));
  c.push(P('Each session has one team notebook, in the folder Practice Files/notebooks. The data colleague runs it. Leaders can follow on the shared screen.'));
  [ 'Go to colab.research.google.com and sign in with your Google account.', 'Choose File, then Upload notebook, and pick the notebook file for the session.', 'Run the first cell. Its first line says Run this cell first. It is the setup cell.', 'When the cell asks, choose the file data.zip from your computer. If your tutor gives a link, paste it between the quotation marks after DATA_ZIP_URL and run the cell again.', 'The cell prints Data ready and lists the files. The data and the Kitara documents are now in the notebook folder.', 'Run the other cells from the top. Cells that begin with # Your turn are for your team to complete. The check cell after each task prints Task correct when the answer is right.']
    .forEach(t => c.push(N(t)));
  c.push(callout('Run the setup cell first in every session. Each notebook needs its own copy of the data.'));

  c.push(H1('If Colab disconnects'));
  c.push(P('Google does not publish the limits of free Colab. A session can stop after a period without activity and after a long run. When it stops, the notebook keeps its code and loses its variables and uploaded files.'));
  c.push(B('Choose Connect again, then run the setup cell, then run the cells from the top.'));
  c.push(B('Save a copy to Google Drive with File, then Save a copy in Drive, so that your edits are kept.'));
  c.push(B('Copy each finished table into your workbook as you go.'));
  c.push(B('If a cell reports that a library is not found, install it with pip install followed by the library name, and run the cell again.'));

  c.push(H1('The free tools'));
  c.push(P('Every tool in the course is free for you and for the tutor. Status verified means the free-use terms were confirmed from public sources. Status check means read the licence file on the day you decide to use it.'));
  c.push(table(['Tool', 'Use', 'Cost and terms', 'Status'], data.tools.map(t => [t.name, t.use, t.cost, t.status]), [2300, 2300, 3900, 1138], { size: 18, boldFirst: true, hl: (i, r) => r[3] === 'check' }));
  c.push(P(''));
  c.push(H3('Tools the course avoids'));
  data.avoided.forEach(([a, b]) => c.push(bl(a + '.', b)));

  c.push(H1('How to check a licence'));
  c.push(P('Session 10 uses these three steps for every tool and model on the Licence Register.'));
  ['Open the tool\'s code repository and find the file named LICENSE or COPYING. For a model, open the model card. Read the file itself. A web page about the tool may be out of date.', 'Find the licence name in the first lines, such as MIT, Apache-2.0, AGPL or Elastic License 2.0. Then read the README for extra terms, such as features that need a paid licence or limits on use. Different folders in one repository can carry different licences.', 'Write the licence as the file gives it, where you read it, the date and your name in Licence Register.xlsx. Class it as open, source-available or restricted.']
    .forEach(t => c.push(N2(t)));

  c.push(H1('A data protection note on your own documents'));
  c.push(P('This is a teaching summary and not legal advice.'));
  c.push(B('The Uganda Data Protection and Privacy Act, 2019 applies to anyone who collects, holds, processes or uses personal data in Uganda. Personal data includes names, phone numbers, identity numbers and health details. Kenya, Rwanda and Tanzania have their own laws, which Session 9 compares.'));
  c.push(B('Choose documents that hold no personal data. If a document has some, leave it out of your 50.'));
  c.push(B('Choose documents that are not confidential and that the owner has approved in writing.'));
  c.push(B('Keep your own documents on your laptop. Do not upload them to Colab, to a chat assistant or to the tutor. The team notebooks work on the Kitara files, which are fictional.'));
  c.push(B('Record what you learn from your documents in a spreadsheet, such as the format, the text quality and the version status. The spreadsheet holds summaries and no document text.'));
  await save(doc2('Setup Guide', c, `${COURSE}   Setup Guide`), '03 Learner Materials/Setup Guide.docx');
}

(async () => { await workbook(); await plan(); await glossary(); await setup(); })();
