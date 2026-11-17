// Builds the Word documents for AI and Data Science Professional from docs_data.json.
//   node make_docs.js
const fs = require('fs'), path = require('path');
const D = require('docx');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle, HeadingLevel, AlignmentType, LevelFormat, PageBreak, Footer, PageNumber } = D;
const data = JSON.parse(fs.readFileSync(path.join(__dirname, 'docs_data.json'), 'utf8'));
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
function doc(title, children, footerText) {
  return new Document({
    creator: 'Jotham Martin Wambi', title,
    styles: { default: { document: { run: { font: 'Calibri', size: 22 } } } },
    numbering: { config: [
      { reference: 'bul', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 270 } } } }, { level: 1, format: LevelFormat.BULLET, text: '–', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 1000, hanging: 270 } } } }] },
      { reference: 'num', levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 340 } } } }] }] },
    sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1134, bottom: 1134, left: 1134, right: 1134 } } },
      footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [run(`${footerText}   Page `, { size: 18, color: SOFT }), new TextRun({ children: [PageNumber.CURRENT], font: 'Calibri', size: 18, color: SOFT })] })] }) },
      children }] });
}
const save = async (d, rel) => { const p = path.join(ROOT, rel); fs.mkdirSync(path.dirname(p), { recursive: true }); fs.writeFileSync(p, await Packer.toBuffer(d)); console.log('wrote', rel); };
const T = data.totals, S = data.sessions;

// ============================================================ 1. BENCHMARK AND DESIGN REPORT
async function benchmark() {
  const c = [];
  c.push(new Paragraph({ spacing: { before: 400, after: 80 }, children: [new TextRun({ text: 'AI and Data Science Professional', font: 'Cambria', bold: true, size: 52, color: INK })] }));
  c.push(new Paragraph({ spacing: { after: 240 }, children: [new TextRun({ text: 'Benchmark and design report', font: 'Calibri', size: 32, color: SOFT })] }));
  c.push(P('Prepared 28 October 2026 for Jotham Martin Wambi, KLAi Professional Learning. A 48-hour course for working professionals who know Excel and have never coded.', { }));
  c.push(H1('1. The verdict'));
  c.push(callout([[bold('A good fit for working professionals who start from Excel. It is far shorter than a 150-hour certificate.')], 'The course teaches one path from data to a deployed app (data, Python, SQL, inference, regression, machine learning, text and language models, responsible use) in 48 live hours, with free tools only, an Excel starting point and Ugandan data. It is shorter and shallower than the Google and IBM certificates, and Session 24 lists what it leaves out. Those programmes offer more depth, more mathematics, more tools and a recognised credential. This course offers live teaching, no cost, a start for non-technical learners, local context, and newer topics such as embeddings, retrieval, small local language models and data protection law.']));
  c.push(gap());
  c.push(H2('What was compared'));
  c.push(P('The course was set against the AI and Data Scientist roadmap on roadmap.sh and against the programmes most employers and learners already know: the IBM Data Science Professional Certificate, the Google Data Analytics and Advanced Data Analytics certificates, the DeepLearning.AI Machine Learning Specialization and AI for Everyone, Google\'s Machine Learning Crash Course, Kaggle Learn, fast.ai, Harvard\'s CS50P and the University of Helsinki\'s Elements of AI. Facts come from public pages found by web search on 28 October 2026 and checked again on 29 October 2026. Where sources disagree on hours, course counts or prices, the table gives the range and says so. The roadmap.sh page itself could not be fetched from the build environment, so its stages were taken from the roadmap PDF and curricula that follow it. Re-check the live page before quoting it.'));
  c.push(H1('2. The comparators'));
  const cw = [1850, 1600, 1150, 2800, 2238];
  c.push(table(['Programme', 'Length', 'Cost', 'What it teaches', 'Gap against this course'], [
    ['IBM Data Science Professional Certificate (Coursera)', 'About 178 hours, 12 courses; roughly 4 months at 10 hours a week (Coursera)', 'USD 49 to 59 a month, depending on source and date', 'Methodology, Python, SQL, Jupyter, GitHub, RStudio, pandas, NumPy, scikit-learn, matplotlib, browser labs; a generative AI course and career guide added', 'Self-paced, no live tutor, paid. One reviewer notes classical data science only, no retrieval or agents. Much deeper and longer.'],
    ['Google Data Analytics Professional Certificate', 'Nine courses, over 180 hours (Coursera); older reviews describe eight courses and R; under 6 months at under 10 hours a week', 'About USD 49 a month (reported)', 'Spreadsheets, SQL, Tableau, Python (the Python course is 27 hours), and a last course on job searching with AI', 'Analytics only; no modelling. Paid. Tableau is outside our free set.'],
    ['Google Advanced Data Analytics Certificate', 'Seven courses; Coursera says about 6 months at 10 hours a week, third parties say about 200 hours', 'Coursera subscription (about USD 49 a month reported)', 'Python, statistics, regression, supervised machine learning, Tableau; no deep learning listed', 'Needs analytics background first. Paid. No text or language models.'],
    ['DeepLearning.AI Machine Learning Specialization', 'Three courses, about 95 hours (DeepLearning.AI)', 'Coursera subscription', 'Supervised learning, neural networks, trees, unsupervised learning, recommenders, reinforcement learning, in NumPy, scikit-learn and TensorFlow', 'Assumes programming comfort. Deeper theory.'],
    ['AI for Everyone (DeepLearning.AI)', 'About 7 hours', 'Coursera', 'What AI is, how to run AI projects, AI in a company, society. No code.', 'No hands-on data work.'],
    ['Google Machine Learning Crash Course', 'About 15 hours by Google\'s estimate; learners report 10 to 30', 'Free', 'Regression, classification, data, neural networks, embeddings, large language models, production and fairness; exercises in Colab', 'Assumes Python, pandas and NumPy. No live teaching.'],
    ['Kaggle Learn micro-courses', 'About 3 to 5 hours each (Python 5, Pandas 4, Intro to Machine Learning 3, Intro to SQL 3)', 'Free, free certificates', 'Hands-on notebooks', 'Short and disconnected; best as free follow-up.'],
    ['fast.ai Practical Deep Learning for Coders', 'Part 1 lists 9 lessons of about 90 minutes (the announcement post lists 8)', 'Free', 'Image, text, tabular deep learning and deployment', 'Needs a year of coding. Deep learning only.'],
    ['Harvard CS50P', '9 or 10 weeks (sources differ) at 3 to 9 hours a week', 'Free to take; free certificate through Harvard OpenCourseWare, or a paid edX certificate', 'Python programming', 'Python only; no data science.'],
    ['Elements of AI (University of Helsinki)', 'University of Helsinki says about 30 hours; other sources say 10 to 50', 'Free', 'What AI is and is not, no maths or code', 'No hands-on skills.'],
  ], cw, { size: 18, boldFirst: true }));
  c.push(P(''));
  c.push(H1('3. Coverage against the roadmap.sh stages'));
  c.push(P('The stage list below is the one in the roadmap.sh AI and Data Scientist PDF and the curricula built on it. The right-hand column says how deeply this course goes. "Light" means the course keeps it short for non-technical learners.'));
  const cov = data.coverage.map(([stage, how, ses, depth]) => [stage, how, ses.join(', '), depth]);
  c.push(table(['Roadmap stage', 'What this course does', 'Sessions', 'Depth'], cov, [1900, 5000, 1500, 1238], { size: 19, boldFirst: true, hl: (i, r) => r[3] === 'light' }));
  c.push(P(''));
  c.push(callout([[bold('Left out on purpose. ')], 'Proofs and hand calculation in linear algebra and calculus, data structures and interview algorithms, big-data engines, cloud platforms, containers and training deep networks from scratch. Session 24 lists each gap with a free next step.']));
  c.push(H1('4. Where the course is competitive'));
  const pts = [
    ['Live teaching with a script.', `Every programme above is self-paced. This course puts a tutor in the room, with ${T.slides} slides, ${T.clicks} click reveals on ${T.animated} animated slides, and read-aloud notes for every slide (about ${(T.words / 130 / 60).toFixed(1)} hours of spoken script), so the tutor does not have to improvise.`],
    ['A start for people who are not technical.', 'The design assumes beginners drop out because of overload (code, mathematics and tools at once), fear of mathematics, and getting stuck early. This is a design assumption and no source for it was checked. Excel is the anchor (Sessions 1 to 4 have no code), statistics is learned through simulation and pictures, every session begins with recall and ends with a check, and a first error is read and fixed in Session 5.'],
    ['No cost for the learner or the tutor.', 'Every tool is free, and several common choices were avoided for cost or compatibility reasons (see section 6). No lab needs a paid account, a key or a GPU.'],
    ['Modern topics most certificates add late or leave out.', 'Text as numbers, embeddings, retrieval over a company\'s own documents and a test sheet for a small language model run inside Colab (Sessions 21 and 22). The Google Advanced Data Analytics outline lists no deep learning, and the IBM certificate added generative AI as a later course.'],
    ['Local data and local law.', 'The practicals use fictional Uganda businesses (a supermarket chain, a microfinance lender, district clinics) in shillings, and Session 23 teaches the principles and rights in the Data Protection and Privacy Act, 2019 as a teaching summary that is not legal advice.'],
    ['Checks built into every session.', 'Every number in the practicals comes from generated data with an answer key, the solution notebooks were run wherever the libraries allowed (see section 9), and the sessions teach the habits that catch wrong numbers: grain, join traps, leakage, residuals you name, and the row count beside every figure.'],
  ];
  pts.forEach(([a, b]) => c.push(B([bold(a + ' '), run(b)])));
  c.push(H1('5. Where it is not competitive'));
  [['Depth and hours.', '48 hours against roughly 150 to 240 for the certificates. A graduate can do junior analyst work and can build and test a first model. A finished data scientist needs more.'],
   ['Credential.', 'No external credential. A certificate from KLAi or a university partner would need to be arranged. The capstone and a public GitHub portfolio are the proof of skill.'],
   ['Mathematics.', 'Intuition and simulation only. Learners who want machine learning research or engineering roles need linear algebra, calculus and probability next.'],
   ['Engineering practice.', 'Version control, one deployed app and a model card, but no containers, testing frameworks, pipelines or monitoring tools.'],
   ['Free-tool limits.', 'Google does not publish Colab\'s free limits. Reports give an idle disconnect of about 90 minutes and a longest session of about 12 hours. Streamlit Community Cloud apps sleep after 12 hours without visitors. Both suit learning and neither suits a business-critical service.']]
    .forEach(([a, b]) => c.push(B([bold(a + ' '), run(b)])));
  c.push(H1('6. Tools and licences'));
  c.push(P('Status "verified" means the free-use terms were confirmed from public sources on 28 October 2026. Status "check" means confirm on the day before class.'));
  c.push(table(['Tool', 'Use', 'Cost and terms', 'Status'], data.tools.map(t => [t.name, t.use, t.cost + (t.note ? ' ' + t.note : ''), t.status]), [2300, 2400, 3900, 1038], { size: 18, boldFirst: true, hl: (i, r) => r[3] === 'check' }));
  c.push(P(''));
  c.push(H3('Avoided, and why'));
  data.avoided.forEach(([a, b]) => c.push(B([bold(a + '. '), run(b)])));
  c.push(callout([[bold('Hosted model services changed in October 2026. ')], 'Several sources report that Hugging Face stopped including monthly inference credits for free accounts on 7 October 2026, and its pricing page now says free users buy credits or upgrade to PRO. The date rests on a forum thread and a GitHub issue, not an official notice, and some roundups still list the credits. The course downloads small open models once and runs them inside Colab, so nothing is sent to a vendor and no key is needed. Check the current terms and the model card licence before teaching Session 22.']));
  c.push(H1('7. Market and local relevance'));
  c.push(B('The World Economic Forum Future of Jobs Report 2025 ranks AI and big data as the fastest-growing skills, and analytical thinking as the most sought-after core skill (about seven in ten employers).'));
  c.push(B('The Stack Overflow Developer Survey 2025 reports Python used extensively by 57.9 percent of all respondents (51 percent a year earlier). That is fourth, behind JavaScript, HTML and CSS, and SQL. Among respondents who are learning to code, Python comes first (secondary sources give about 69 to 72 percent). The 2024 Python Developers Survey by JetBrains and the Python Software Foundation puts pandas at 80 percent of the respondents who do data exploration and processing.'));
  c.push(B('For Uganda, third-party career guides describe a shortage of applied AI skills among computer science graduates, and universities (for example Makerere) are building AI and data science capacity. These guides are secondary sources that were not checked; treat their pay figures as unverified.'));
  c.push(H1('8. What was built'));
  c.push(table(['Item', 'Quantity'], [['Sessions', '24 sessions of 2 hours (48 hours)'], ['Slide decks', `${T.slides} slides in 24 decks`], ['Animated slides', `${T.animated} slides with ${T.clicks} click reveals`], ['Read-aloud speaker notes', `Every slide, about ${(T.words / 130 / 60).toFixed(1)} hours of script`], ['Vocabulary', `${T.vocab} terms, each with a spreadsheet equivalent where one exists`], ['Lab notebooks', '20 coding sessions (student and solution versions)'], ['Task sheets', 'Sessions 1 to 4 (Google Sheets) and Session 24 (presentation preparation), with a tutor copy of the answers'], ['Handouts', 'Student Setup Guide, Sheets Lab Sheets, Glossary, Assessment and Capstone Guide'], ['Datasets', 'Lakeside Mart (retail), Nile Microfinance (loans), District Clinics, 800 feedback messages, 8 policy documents, a dirty export with 8 seeded defects'], ['Figures', '60 explanatory charts and diagrams drawn from the data']], [3000, 6638], { boldFirst: true }));
  c.push(H1('9. What is verified, and what is not'));
  c.push(P([bold('Verified here: '), run('every slide fits its text at readable sizes; every notes script passes a read-aloud lint (no stage directions, with one paragraph per click); every pandas, NumPy, matplotlib, seaborn and SQL block on a slide or in a lab solution was executed against the generated data and its printed output compared with the slide; the answer key properties (skew, seasonality, the rate-versus-count reversal, the offer lift, the loan model\'s difficulty and the leakage column) are asserted by the data generator; every vocabulary term is defined once.')]));
  c.push(P([bold('Not verified here: '), run('the authoring machine has no scikit-learn, SciPy, statsmodels, PyTorch, Transformers, sentence-transformers or Streamlit and no internet. Code that uses them was syntax-checked only, and no slide shows an output from them that was not computed with NumPy. The first job before teaching is to run the lab notebooks end to end in Colab, or to run run_all_labs.py in 04 Facilitator Materials on a machine that has the libraries. Nothing was rehearsed aloud, and PowerPoint playback of the animations has not been tested; LibreOffice rendered them correctly. The external facts in sections 2, 6 and 7 were checked against public pages on 28 and 29 October 2026; the Verification Record lists what changed.')]));
  c.push(H1('10. Decisions for you'));
  [['Hosting the data.', 'Put data.zip somewhere students can reach (a public GitHub release, Google Drive link or WhatsApp). The setup cell accepts a link or an upload.'],
   ['A credential.', 'Decide whether KLAi or a university partner issues a certificate, and what the capstone pass mark is.'],
   ['The capstone dataset.', 'Four are offered (Lakeside, Nile loans, clinics, feedback). Add one drawn from students\' own workplaces if their employers permit and data protection allows.'],
   ['Account policy.', 'Every student needs a free Google account for Colab. Ask in Session 1 who has none and plan a local-install route (VS Code and Python) for them.'],
   ['Screenshots.', 'No tool screenshots are included because none could be captured here. Add them for the tools you demonstrate (Colab, GitHub, Streamlit Community Cloud) as full-width figures.']]
    .forEach(([a, b]) => c.push(B([bold(a + ' '), run(b)])));
  c.push(H1('Sources'));
  [['IBM Data Science Professional Certificate, Coursera', 'https://www.coursera.org/professional-certificates/ibm-data-science'],
   ['Google Data Analytics Professional Certificate', 'https://www.coursera.org/professional-certificates/google-data-analytics'],
   ['Google Advanced Data Analytics Professional Certificate', 'https://www.coursera.org/professional-certificates/google-advanced-data-analytics'],
   ['DeepLearning.AI Machine Learning Specialization', 'https://www.deeplearning.ai/specializations/machine-learning'],
   ['AI for Everyone', 'https://www.deeplearning.ai/courses/ai-for-everyone'],
   ['Google Machine Learning Crash Course', 'https://developers.google.com/machine-learning/crash-course'],
   ['Kaggle Learn', 'https://www.kaggle.com/learn'],
   ['fast.ai Practical Deep Learning for Coders', 'https://course.fast.ai/'],
   ['Harvard CS50P', 'https://cs50.harvard.edu/python/'],
   ['roadmap.sh AI and Data Scientist (PDF)', 'https://roadmap.sh/pdfs/roadmaps/ai-data-scientist.pdf'],
   ['WEF Future of Jobs Report 2025', 'https://reports.weforum.org/docs/WEF_Future_of_Jobs_Report_2025.pdf'],
   ['Uganda Data Protection and Privacy Act, 2019 (ULII)', 'https://media.ulii.org/media/legislation/18002/source_file/b6ae5cce4290322a/2019-9.pdf'],
   ['Streamlit Community Cloud status and limits', 'https://docs.streamlit.io/deploy/streamlit-community-cloud/status'],
   ['TensorFlow Playground', 'https://playground.tensorflow.org/'],
   ['Anaconda terms of service for academia and research', 'https://www.anaconda.com/blog/update-on-anacondas-terms-of-service-for-academia-and-research'],
   ['Hugging Face inference providers pricing', 'https://huggingface.co/docs/inference-providers/pricing'],
   ['Stack Overflow Developer Survey 2025', 'https://survey.stackoverflow.co/2025/'],
   ['Python Developers Survey 2024 (JetBrains and the Python Software Foundation)', 'https://lp.jetbrains.com/python-developers-survey-2024/'],
   ['Elements of AI', 'https://www.elementsofai.com/'],
   ['Google Colab FAQ', 'https://research.google.com/colaboratory/faq.html']]
    .forEach(([a, u]) => c.push(B([bold(a + '. '), run(u, { color: LAKE })])));
  await save(doc('Benchmark and design report', c, 'AI and Data Science Professional   Benchmark and design report'), '04 Facilitator Materials/Benchmark and Design Report.docx');
}

// ============================================================ 2. COURSE PLAN AND TUTOR GUIDE
async function plan() {
  const c = [];
  c.push(new Paragraph({ spacing: { before: 400, after: 80 }, children: [new TextRun({ text: 'AI and Data Science Professional', font: 'Cambria', bold: true, size: 52, color: INK })] }));
  c.push(new Paragraph({ spacing: { after: 240 }, children: [new TextRun({ text: 'Course plan and tutor guide', font: 'Calibri', size: 32, color: SOFT })] }));
  c.push(callout([[bold('48 hours. 24 sessions of 2 hours. Free tools only.')], 'Students start confident in Excel or Google Sheets, with no code and no statistics. They finish able to take a business question from raw data to a tested model or analysis, explain it to a manager, and run it as a small app.']));
  c.push(H1('1. How each session runs'));
  c.push(table(['Block', 'Minutes', 'What happens'], [['Recall and warm-up', '10', 'Two questions on the last session. Students answer aloud first.'], ['Concepts and explanation', '30', 'Slides and the read-aloud notes. One idea per slide, spreadsheet word first.'], ['Live demonstration', '25', 'You type the code live in Colab or Sheets. Errors are part of the teaching.'], ['Break', '5', ''], ['Guided lab', '40', 'The student notebook. Each task has a blank and a check cell that tells students if they are right.'], ['Check and wrap-up', '10', 'The three-question exit check, then the summary.']], [2800, 1100, 5738], { boldFirst: true }));
  c.push(H1('2. The six modules'));
  data.modules.forEach(([m, name, rng, desc]) => c.push(B([bold(`Module ${m}, ${name} (sessions ${rng[0]} to ${rng[rng.length - 1]}). `), run(desc)])));
  c.push(H1('3. The 24 sessions'));
  c.push(P('Each entry gives the question the session answers and the result students leave with. "Lab" is the 40-minute practical.'));
  S.forEach(s => {
    c.push(H3(`Session ${s.no}. ${s.title}`));
    c.push(P([bold('Question: '), run(s.question)], { spacing: { after: 40 } }));
    c.push(P([bold('Result: '), run(s.checkpoint ? s.result.replace(/ Checkpoint \d\.$/, '') + ' ' + s.checkpoint + '.' : s.result)], { spacing: { after: 40 } }));
    c.push(P([bold('Lab: '), run(s.lab)], { spacing: { after: 40 } }));
    c.push(P([bold('Data and tools: '), run(`${s.dataset}. ${s.tools.join(', ')}.`)], { spacing: { after: 40 } }));
    c.push(P([bold('Words taught: '), run(s.vocab.join(', ') + '.')], { spacing: { after: 40 } }));
    c.push(P([bold('Deck: '), run(`${s.slides} slides, ${s.animated} animated with ${s.clicks} reveals; about ${s.minutes_spoken} minutes of read-aloud notes.`)], { spacing: { after: 100 } }));
  });
  c.push(H1('4. Assessment'));
  c.push(table(['Part', 'Weight'], data.assessment.map(([a, b]) => [a, b]), [6400, 3238], { boldFirst: true }));
  c.push(P(''));
  c.push(P('Weekly checks give instant feedback and are not graded. Checkpoint 1 (Session 8) is a cleaned file reconciled to a known total, with the residual named. Checkpoint 2 (Session 13) is a one-page analysis report. Checkpoint 3 (Session 19) is a tested model with a baseline. The capstone is a question, cleaned data, one analysis, one model with a metric chosen for the cost of a mistake, limits, a small app and a ten-minute presentation. The capstone steps are fixed: Session 13 write and scope the question, Session 14 choose the dataset, Session 19 baseline and tested model, Session 23 publish the app and model card, Session 24 present for ten minutes. The presentation rubric is in Session 24 and in the Assessment and Capstone Guide, which students receive in Session 1. Marks are a proposal, to be adjusted to your institution\'s rules.'));
  c.push(H1('5. Before the course starts'));
  [['Hand out the learner documents.', 'Send the Student Setup Guide before Session 1. In Session 1 give out the Sheets Lab Sheets, the Glossary and the Assessment and Capstone Guide. Keep Sheets Lab Answers and the Lab Solutions for yourself.'],
   ['Host the data.', 'Upload data.zip (in 03 Learner Materials/Practice Files) where students can download it, and paste the link into DATA_ZIP_URL in the notebook setup cell, or keep it empty so each student uploads the file.'],
   ['Google accounts.', 'Every student needs a free Google account for Colab and Sheets. Ask in Session 1. For anyone without one, use VS Code and Python from python.org on their laptop.'],
   ['Run every lab once.', 'Run run_all_labs.py (in 04 Facilitator Materials) on a machine that has the libraries, or open each solution notebook in Colab and choose Runtime, Run all. The authoring machine could not run the scikit-learn, SciPy, statsmodels, sentence-transformers and Streamlit cells. If a cell fails, fix the content file and rebuild (see the Authoring README).'],
   ['Check the licence of the small language model.', 'Session 22 names Qwen2.5-0.5B-Instruct as an example. Read its model card before class, or use retrieval alone.'],
   ['Play every animated slide.', 'Open each deck in PowerPoint in Slide Show mode and click through. Editing view shows the finished slide. The Playback and Rehearsal Checklist lists each animated slide with its click count.'],
   ['Read the notes aloud once per session.', 'Change wording that does not sound like you. The notes are written to be read as they stand.']]
    .forEach(([a, b]) => c.push(B([bold(a + ' '), run(b)])));
  c.push(H1('6. The tools'));
  c.push(table(['Tool', 'Use', 'Cost and terms', 'Status'], data.tools.map(t => [t.name, t.use, t.cost + (t.note ? ' ' + t.note : ''), t.status]), [2300, 2400, 3900, 1038], { size: 18, boldFirst: true, hl: (i, r) => r[3] === 'check' }));
  c.push(H1('7. The data'));
  c.push(P('All data is fictional and generated by a seeded script, so every number in a slide or a lab can be traced to an answer key. Files are in 03 Learner Materials/Practice Files/data. DATA DICTIONARY.txt defines every column.'));
  c.push(table(['Dataset', 'Contents', 'Used in'], [
    ['Lakeside Mart', 'Eight mini-markets in Uganda: branches, 150 products, 2,500 loyalty customers, a 5 percent sample of till orders (30,229 orders, 98,066 lines), returns, weekly branch summaries, a loyalty offer test, 800 feedback messages, eight policy documents, and a dirty export with eight seeded defects', 'Sessions 1 to 13, 18, 19, 21, 22'],
    ['Nile Microfinance', '8,000 loans with a default outcome (1,004 defaults, about 12.5 percent), a column that leaks the answer, missing values and impossible ages', 'Sessions 14 to 17, 20, 23'],
    ['District Clinics', 'Twelve districts by 60 months of visits, malaria cases and rainfall (18 blank visit counts)', 'Session 19'],
    ['lakeside_for_sheets.xlsx', 'A 2,000-order sample (6,590 order lines) for the Google Sheets sessions, with a READ ME tab', 'Sessions 1 to 4']], [2100, 5700, 1838], { boldFirst: true }));
  c.push(P(''));
  c.push(P('Any of the four datasets (Lakeside Mart, Nile Microfinance, District Clinics or the Lakeside feedback messages) can be a capstone dataset. Students choose in Session 14.'));
  c.push(H1('8. Rebuilding the materials'));
  c.push(P('Everything is generated from the files in 05 Course Maintenance/Authoring. The content of each session is one file, Content/sNN.json. Run these from the Build folder. After any edit run:'));
  c.push(P([run('python3 build_course.py check N', { font: 'Courier New', size: 20 })]));
  c.push(P('which fits every slide, lints every note, executes the code that can run, and lists problems. Then python3 build_course.py build all writes every deck and notebook. python3 check_course.py checks the whole course for duplicate vocabulary terms, repeated sentences, figure names and titles. python3 build_course.py data regenerates the data and figures.'));
  c.push(P('To rebuild the Word documents, the roadmap and the checklist after a change, run:'));
  c.push(P([run('python3 export_docs_data.py && node make_docs.js && python3 make_roadmap.py && python3 make_playback_checklist.py', { font: 'Courier New', size: 20 })]));
  c.push(P('Fix wording in the generators (make_docs.js, curriculum.py, the Content files), never in a generated file. Authoring/README - Read First.txt has the full list.'));
  c.push(H1('9. What is in each folder'));
  [['01 Course Overview.', 'Student Roadmap (one page).pdf, the page to share with students, and the editable .pptx.'],
   ['02 Class Slides.', `${T.slides} slides in 24 decks, numbered in teaching order. Every slide has speaker notes written as a script.`],
   ['03 Learner Materials.', 'Student Setup Guide.docx (send before Session 1). Sheets Lab Sheets.docx (task lists for Sessions 1 to 4 and 24). Glossary.docx (every vocabulary term with its spreadsheet equivalent). Assessment and Capstone Guide.docx (marks, checkpoints, capstone, presentation, working rules). Practice Files/data (the datasets, DATA DICTIONARY.txt, lakeside.db, lakeside_for_sheets.xlsx, answer_key.json), Practice Files/data.zip, and Practice Files/notebooks (the student lab notebook for each coding session).'],
   ['04 Facilitator Materials.', 'This guide. Sheets Lab Answers.docx (tutor only: answers to the Sheets tasks). Lab Solutions (tutor only: one solution notebook per coding session). run_all_labs.py. Playback and Rehearsal Checklist.txt. Benchmark and Design Report.docx.'],
   ['05 Course Maintenance.', 'Authoring (the sources and the build scripts), Research Notes.txt and Verification Record.txt.']]
    .forEach(([a, b]) => c.push(B([bold(a + ' '), run(b)])));
  await save(doc('Course plan and tutor guide', c, 'AI and Data Science Professional   Course plan and tutor guide'), '04 Facilitator Materials/Course Plan and Tutor Guide.docx');
}

// ============================================================ 3. STUDENT SETUP GUIDE
async function setup() {
  const c = [];
  c.push(new Paragraph({ spacing: { before: 200, after: 60 }, children: [new TextRun({ text: 'Get ready for AI and Data Science Professional', font: 'Cambria', bold: true, size: 44, color: INK })] }));
  c.push(P('Do these four things before Session 1. They take about twenty minutes and cost nothing.'));
  c.push(H2('1. A Google account'));
  c.push(P('Google Colab (where you will run Python) and Google Sheets both use a free Google account. If you have a Gmail address, you have one. If not, make one at accounts.google.com and write the password somewhere safe.'));
  c.push(H2('2. Open Google Colab once'));
  [ 'Go to colab.research.google.com and sign in.', 'Choose New notebook.', 'In the first cell type: print("Hello from Colab")', 'Press the play button beside the cell. You should see Hello from Colab under it.', 'Choose File, then Save a copy in Drive.'].forEach(t => c.push(N(t)));
  c.push(callout('Free Colab sessions stop after you leave them idle for a while and after about twelve hours. Colab does not publish its limits. Save your notebooks to Google Drive or GitHub, and never leave your only copy of the work inside an open session.'));
  c.push(H2('3. Open the workbook in Google Sheets'));
  c.push(P('Your tutor will give you lakeside_for_sheets.xlsx. Upload it to Google Drive, open it, and choose File, then Save as Google Sheets. Look at the tabs along the bottom. In Session 2 you will describe each one.'));
  c.push(H2('4. Get the data file'));
  c.push(P('Your tutor will give you data.zip or a link to it. Keep it somewhere you can find it. Each lab notebook starts with a setup cell that asks you to choose this file, and unpacks it for you.'));
  c.push(H2('Your other documents'));
  c.push(P('Your tutor will also give you three documents in Session 1. The Sheets Lab Sheets hold the task lists for Sessions 1 to 4 and the presentation preparation in Session 24. The Glossary explains every word the course teaches, with the spreadsheet idea it matches. The Assessment and Capstone Guide says what you hand in, when, and how it is marked.'));
  c.push(H2('If something goes wrong'));
  c.push(B('Colab will not open: try another browser (Chrome or Edge), and turn off any extension that blocks pages.'));
  c.push(B('You have no Google account and do not want one: tell your tutor before Session 1. There is a route using Python on your own laptop.'));
  c.push(B('A cell shows red text: read the last line first. It says what went wrong. We practise this in Session 5.'));
  c.push(B('Use only the fictional course data. Never put real customer or patient data into a notebook, a chat assistant or an app you share.'));
  c.push(H2('What you need to bring'));
  c.push(P('A laptop (Windows or Mac) with a browser and a charger. A notebook and pen. A question from your own work that you would like data to answer.'));
  await save(doc('Student setup guide', c, 'AI and Data Science Professional   Student setup guide'), '03 Learner Materials/Student Setup Guide.docx');
}

// ============================================================ 4. SHEETS LAB SHEETS (students) AND ANSWERS (tutor)
const titleBlock = (t, sub) => [new Paragraph({ spacing: { before: 200, after: 60 }, children: [new TextRun({ text: t, font: 'Cambria', bold: true, size: 44, color: INK })] }), ...(sub ? [new Paragraph({ spacing: { after: 200 }, children: [new TextRun({ text: sub, font: 'Calibri', size: 26, color: SOFT })] })] : [])];
const answerLine = () => new Paragraph({ spacing: { before: 60, after: 120 }, border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: LINE, space: 14 } }, children: [] });
async function sheets() {
  for (const withAnswers of [false, true]) {
    const c = titleBlock(withAnswers ? 'Sheets lab answers' : 'Sheets lab sheets', withAnswers ? 'Tutor copy for Sessions 1 to 4 and 24. Do not hand out.' : 'Sessions 1 to 4 and 24. In Sessions 1 to 4 work in Google Sheets with lakeside_for_sheets.xlsx unless a task says otherwise. Session 24 needs no spreadsheet.');
    if (withAnswers) c.push(P('Answers for the Sheets tasks come from the 2,000-order workbook, not the full file, so they differ from the full-file numbers quoted in the slides. Random answers (Session 4) are given as ranges.'));
    for (const [n, s] of Object.entries(data.sheets)) {
      const sess = S[Number(n) - 1];
      const intro = withAnswers ? s.intro : s.intro.replace('Part two is this notebook', 'Part two is the Session 1 notebook in Google Colab').replace('Check each task against the answer given.', 'Your tutor will give you the answers to check against.').replace('Check yours against the ranges given.', 'Your tutor will give you ranges to check yours against.');
      c.push(H1(`Session ${n}. ${sess.title}`)); c.push(P(intro));
      s.tasks.forEach((tk, i) => {
        c.push(new Paragraph({ keepNext: true, spacing: { before: 140, after: 60, line: 264 }, indent: { left: 360, hanging: 360 }, children: [run(`${i + 1}.  `, { bold: true, color: LAKE }), run(tk.task, { color: INK })] }));
        if (withAnswers) c.push(new Paragraph({ spacing: { after: 100, line: 264 }, indent: { left: 360 }, children: [run('Answer. ', { bold: true, color: INK }), run(tk.answer)] }));
        else { c.push(answerLine()); c.push(answerLine()); }
      });
    }
    await save(doc(withAnswers ? 'Sheets lab answers' : 'Sheets lab sheets', c, withAnswers ? 'AI and Data Science Professional   Sheets lab answers (tutor)' : 'AI and Data Science Professional   Sheets lab sheets'),
      withAnswers ? '04 Facilitator Materials/Sheets Lab Answers.docx' : '03 Learner Materials/Sheets Lab Sheets.docx');
  }
}

// ============================================================ 5. GLOSSARY
async function glossary() {
  const v = [...data.vocab].sort((a, b) => a.term.localeCompare(b.term, 'en', { sensitivity: 'base' }));
  const c = titleBlock('Glossary', `${v.length} words from the course, with the spreadsheet idea each one matches where there is one.`);
  c.push(table(['Word', 'Plain meaning', 'In a spreadsheet', 'Session'], v.map(x => [x.term, x.meaning, x.sheet || 'No equivalent. A new idea.', String(x.session)]), [1900, 4300, 2600, 838], { size: 19, boldFirst: true }));
  await save(doc('Glossary', c, 'AI and Data Science Professional   Glossary'), '03 Learner Materials/Glossary.docx');
}

// ============================================================ 6. ASSESSMENT AND CAPSTONE GUIDE
async function assessment() {
  const c = titleBlock('Assessment and capstone guide', 'What you hand in, when, and how it is marked.');
  c.push(callout([[bold('These are proposed rules. ')], 'Your tutor or institution may change the weights and dates.']));
  c.push(H1('1. How the marks are made'));
  c.push(table(['Part', 'Weight'], data.assessment.map(([a, b]) => [a, b]), [6400, 3238], { boldFirst: true }));
  c.push(P(''));
  c.push(P('Weekly checks are the three questions at the end of each session. They are not marked. They show you what to revisit. Notebook completion means each lab notebook is run to its last task with the check cells passing. How attendance counts is for your tutor to decide.'));
  c.push(H1('2. The three checkpoints'));
  c.push(H3('Checkpoint 1, Session 8: clean a raw file and reconcile it'));
  c.push(P('Hand in the notebook. It must hold the cleaning log (every change with the row count before and after), the cleaned net revenue, and the gap between that figure and the known total with its cause named. A gap you can explain scores higher than one you have hidden.'));
  c.push(H3('Checkpoint 2, Session 13: a one-page analysis report'));
  c.push(P('One page. The question, the data, the model, one sentence for each coefficient, R squared in words, and one limit. A manager who has never seen the data should understand it.'));
  c.push(H3('Checkpoint 3, Session 19: a tested model'));
  c.push(P('A model scored on data it has not seen, beside a simple baseline, with a metric chosen for the cost of a mistake. State whether it beats the baseline, show you checked for leakage, and give the error in business units.'));
  c.push(H1('3. The capstone'));
  c.push(P('You choose one of four datasets, write one question about it, and carry it through the second half of the course.'));
  if (data.capstone) c.push(table(data.capstone.header, data.capstone.rows, [1700, 3200, 4738], { boldFirst: true }));
  c.push(P(''));
  c.push(H3('What you hand in'));
  ['A one-sentence question and the decision it serves.', 'The data cleaned, with a cleaning log.', 'One analysis that answers part of the question.', 'One model with a baseline and a metric chosen for the cost of a mistake.', 'The limits: what the data cannot show, who could be harmed by an error, and which groups you compared.', 'A small app (Session 23) with a model card and a data-protection checklist.', 'A ten-minute presentation (Session 24).'].forEach((x, i) => c.push(new Paragraph({ spacing: { after: 60 }, indent: { left: 360, hanging: 360 }, children: [run(`${i + 1}.  `, { bold: true, color: LAKE }), run(x, { color: INK })] })));
  c.push(H1('4. The presentation'));
  c.push(P('Five slides in ten minutes. In the Session 24 lab your partner scores you from 1 to 3 on each of the four rows below and writes one comment per row.'));
  c.push(table(['Slide', 'What it says', 'Minutes'], [['1. Question', 'The decision someone faces', '1'], ['2. Data', 'What the data covers and leaves out', '2'], ['3. Evidence', 'The result beside its baseline', '3'], ['4. Risk', 'What could go wrong and who checks', '2'], ['5. Decision', 'What you recommend and the next step', '2']], [2000, 6438, 1200], { boldFirst: true }));
  c.push(P(''));
  if (data.rubric) c.push(table(data.rubric.header, data.rubric.rows, [3000, 6638], { boldFirst: true }));
  c.push(H1('5. Working rules'));
  ['Use the course data. If you want to use data from your workplace, ask your employer in writing, remove names and phone numbers first, and never put it in a public repository.', 'A free chat assistant may explain an error or suggest code. Keep a short use log: what you asked, what it gave, how you checked it, and whether you kept it. You must be able to explain every line you hand in.', 'List what you did not check. A stated limit loses no marks. A hidden one does.', 'Your published work is public. Check it for personal data before you push it.']
    .forEach(x => c.push(B(x)));
  await save(doc('Assessment and capstone guide', c, 'AI and Data Science Professional   Assessment and capstone guide'), '03 Learner Materials/Assessment and Capstone Guide.docx');
}
(async () => { await benchmark(); await plan(); await setup(); await sheets(); await glossary(); await assessment(); })();
