const fs = require('fs');
const D = require('docx');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun, WidthType, ShadingType, BorderStyle, AlignmentType, VerticalAlign, Footer, PageNumber } = D;
const rows = JSON.parse(fs.readFileSync('rows.json'));
const FONT = 'Lato', INK = '111111', RED = 'AE2525', GOLD = 'E0BE36', MUTE = '666666', HAIR = 'CFCFCF';
const days = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'], mons = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
const fmt = s => { const d = new Date(s + 'T12:00:00'); return `${days[d.getDay()]} ${d.getDate()} ${mons[d.getMonth()]}`; };
const weeks = [
  ['Python and a first prediction'], ['Python you need'], ['Tables and statistics'], ['Clean, chart, question'],
  ['Baselines and a line'], ['Trees and fair comparisons'], ['Your project'], ['Hand over']];
const RENAME = { ML12: 'Show your first chart and choose your project question', ML18: 'A fair comparison: does your model beat the plain guess?', ML22: 'The final run: your project, ready to share', ML23: 'Rehearse your showcase talk' };
const BUILD = {
  ML01: 'a computer that guesses the rent of a home', ML02: 'a price calculator that knows numbers from text', ML03: 'a calculator that tells you where you slipped',
  ML04: 'a flower-sorting rule that you write by hand', ML05: 'a loop that reads a whole price list', ML06: 'a function that checks its own answers',
  ML07: 'your first table: open a shop sales file', ML08: 'a revenue column that you calculate yourself', ML09: 'a summary card: typical, spread and chance',
  ML10: 'a clean dataset with a log of every change', ML11: 'three charts that tell the story of the sales', ML12: 'a mini report and your own project question',
  ML13: 'a plain-guess baseline your model must beat', ML14: 'a line that predicts a rent', ML15: 'a full prediction experiment, start to finish',
  ML16: 'a decision tree that sorts flowers', ML17: 'a fair comparison that spots overfitting', ML18: 'your model against data it has never seen',
  ML19: 'your project plan and your data', ML20: 'your project baseline', ML21: 'your best model, explained in plain words',
  ML22: 'your finished project, ready to share', ML23: 'a three-minute talk about what you built', ML24: 'showcase day: you show your family what you made',
  F01: 'a warm-up: guess what Python prints, then check', F02: 'a first tour of NumPy arrays', F03: 'quick maths for data: spread and chance', F04: 'the weighted sum behind a prediction' };
const none = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
const noB = { top: none, bottom: none, left: none, right: none };
const W = 10466; // A4 with 0.5in margins ~ 11906-2*720=10466
const run = (t, o = {}) => new TextRun({ text: t, font: FONT, size: 20, color: INK, ...o });
const para = (children, o = {}) => new Paragraph({ children: Array.isArray(children) ? children : [children], spacing: { after: 0, before: 0 }, ...o });

// ---------- header band
const logo = fs.readFileSync('logo.png');
const header = new Table({
  width: { size: W, type: WidthType.DXA }, columnWidths: [3000, 7466],
  rows: [new TableRow({ children: [
    new TableCell({ width: { size: 3000, type: WidthType.DXA }, borders: noB, shading: { type: ShadingType.CLEAR, fill: '000000' }, verticalAlign: VerticalAlign.CENTER,
      margins: { top: 200, bottom: 200, left: 280, right: 100 },
      children: [para(new ImageRun({ type: 'png', data: logo, transformation: { width: 126, height: 40 }, altText: { title: 'KLAi', description: 'KLAi logo', name: 'logo' } }))] }),
    new TableCell({ width: { size: 7466, type: WidthType.DXA }, borders: noB, shading: { type: ShadingType.CLEAR, fill: '000000' }, verticalAlign: VerticalAlign.CENTER,
      margins: { top: 200, bottom: 200, left: 100, right: 280 },
      children: [para(run('Holiday Data and AI Camp', { color: 'FFFFFF', size: 22, bold: true }), { alignment: AlignmentType.RIGHT }),
                 para(run('Machine Learning track', { color: GOLD, size: 20 }), { alignment: AlignmentType.RIGHT })] }),
  ] })] });

const title = [
  para(run('Your study calendar', { size: 52, bold: true }), { spacing: { before: 260, after: 40 } }),
  para(run('Starts Thursday 3 December 2026. Ends with the parent showcase on Saturday 30 January 2027.', { size: 24, color: MUTE }), { spacing: { after: 200 } }),
];

// ---------- key facts (three plain columns separated by a hairline)
const fact = (label, a, b, wd) => new TableCell({ width: { size: wd, type: WidthType.DXA }, borders: { top: { style: BorderStyle.SINGLE, size: 18, color: GOLD }, bottom: none, left: none, right: none },
  margins: { top: 100, bottom: 60, left: 0, right: 160 },
  children: [para(run(label, { size: 17, bold: true, color: MUTE, allCaps: true }), { spacing: { after: 40 } }), para(run(a, { bold: true, size: 22 })), para(run(b, { size: 19, color: '333333' }))] });
const facts = new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: [3489, 3489, 3488],
  rows: [new TableRow({ children: [
    fact('Every week', 'Saturday in person, two classes online', 'In person 2:00 to 5:00 pm. Online 2:00 to 3:30 pm.', 3489),
    fact('Short labs', 'Weeks 1 to 4, online', '2:00 to 4:00 pm. Dates are in the table.', 3489),
    fact('In person at', 'The National ICT Innovation Hub, Nakawa', 'Bring your laptop and charger.', 3488)] })] });

const how = [
  para(run('How it works', { bold: true, size: 22 }), { spacing: { before: 220, after: 60 } }),
  para(run('There are no tests and no marks. In every class you build something, save it, and show it. That is the whole course.', { size: 20 }), { spacing: { after: 70 } }),
  para([run('In person (Saturday): ', { bold: true, size: 20 }), run('three hours of hands-on building with me and a break in the middle. The first class on Thursday 3 December is also in person, so we can set up your laptop together.', { size: 20, color: '333333' })], { spacing: { after: 70 } }),
  para([run('Online (the other days): ', { bold: true, size: 20 }), run('about 90 minutes live on video with screen sharing, where we learn the idea and try it. After class you finish the build in your own time, about an hour, and send me a photo or your notebook before the next class. A class link is sent before each class. You need your laptop, internet and headphones.', { size: 20, color: '333333' })], { spacing: { after: 70 } }),
  para([run('Your project: ', { bold: true, size: 20 }), run('think from day one about a topic you love, such as football, music or boda-boda fares. In week 4 you choose your question and in weeks 7 and 8 you build it and show your family.', { size: 20, color: '333333' })]),
];
const hol = [
  para(run('Public holidays: no class', { bold: true, size: 22, color: RED }), { spacing: { before: 240, after: 60 } }),
  para([run('Friday 25 December, Saturday 26 December, Friday 1 January and Tuesday 26 January. ', { size: 20 }),
        run('No session is lost. A class that would fall on a holiday moves to the next class day. The online labs that fall on 25 December and 1 January move to Monday 28 December and Monday 4 January. Your last class is Saturday 30 January.', { size: 20, color: '333333' })], { spacing: { after: 220 } }),
];

// ---------- schedule table
const cw = [1500, 2300, 6666];
const border = { style: BorderStyle.SINGLE, size: 4, color: HAIR };
const cell = (kids, wd, o = {}) => new TableCell({ width: { size: wd, type: WidthType.DXA }, margins: { top: 55, bottom: 55, left: 100, right: 100 }, verticalAlign: VerticalAlign.CENTER,
  borders: { top: none, left: none, right: none, bottom: border, ...(o.borders || {}) }, shading: o.fill ? { type: ShadingType.CLEAR, fill: o.fill } : undefined, children: kids });
const head = new TableRow({ tableHeader: true, children: ['Date', 'Time', 'What we study'].map((h, i) =>
  cell([para(run(h, { bold: true, size: 18, color: MUTE, allCaps: true }))], cw[i], { borders: { bottom: { style: BorderStyle.SINGLE, size: 12, color: INK } } })) });
const out = [head];
const cps = { ML12: 'Checkpoint one', ML18: 'Checkpoint two', ML22: 'Final test', ML24: 'Parent showcase' };
for (let w = 0; w < 8; w++) {
  const sess = rows.filter(r => (r[1] === 'core' && Math.floor((parseInt(r[2].slice(2)) - 1) / 3) === w) ||
    (r[1] === 'lab' && ['F01','F02','F03','F04'].indexOf(r[2]) === w));
  const a = sess[0][0], b = sess[sess.length - 1][0];
  const span = a.slice(5) === b.slice(5) ? fmt(a) : `${fmt(a).slice(4)} to ${fmt(b).slice(4)}`;
  out.push(new TableRow({ cantSplit: true, children: [new TableCell({ columnSpan: 3, width: { size: W, type: WidthType.DXA }, borders: noB, shading: { type: ShadingType.CLEAR, fill: '000000' },
    margins: { top: 60, bottom: 60, left: 120, right: 120 },
    children: [para([run(`Week ${w + 1}  `, { bold: true, color: GOLD, size: 21 }), run(weeks[w][0], { bold: true, color: 'FFFFFF', size: 21 }), run(`    ${span}`, { color: 'B5B5B5', size: 18 })])] })] }));
  for (const [d, kind, code, ttl0] of sess) {
    const lab = kind === 'lab';
    const ttl = RENAME[code] || ttl0;
    const phys = !lab && (new Date(d + 'T12:00:00').getDay() === 6 || d === '2026-12-03');
    const first = cell([para(run(fmt(d), { bold: true }))], cw[0], phys ? { borders: { left: { style: BorderStyle.SINGLE, size: 30, color: GOLD } } } : {});
    const tm = phys ? ['In person', '2:00 to 5:00 pm'] : lab ? ['Online lab', '2:00 to 4:00 pm'] : ['Online', '2:00 to 3:30 pm'];
    const time = cell([para(run(tm[0], { bold: true, size: 19, color: phys ? INK : MUTE })), para(run(tm[1], { size: 18, color: '333333' }))], cw[1]);
    const kids1 = para([run(lab ? `Lab ${code}  ` : `${code}  `, { bold: true, color: lab ? INK : RED, size: 19 }), run(ttl, { size: 20, bold: true })]);
    const kids2 = para([run('You build: ', { size: 18, color: RED, bold: true }), run(BUILD[code] || '', { size: 18, color: '333333' })], { spacing: { before: 20 } });
    out.push(new TableRow({ cantSplit: true, children: [first, time, cell([kids1, kids2], cw[2])] }));
  }
}
const table = new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: cw, rows: out });

const note = [
  para([run('Optional extra. ', { bold: true, size: 19 }), run('ML25, a first neural network, is an optional session after the course. No date is set yet.', { size: 19, color: '333333' })], { spacing: { before: 200, after: 80 } }),
  para(run('Dates assume classes start on 3 December as planned. If a class is missed, we will agree a catch-up time. Questions: +256 750 990 718  |  jothammartin.wambi@gmail.com', { size: 18, color: MUTE })),
];

const doc = new Document({
  creator: 'KLAi', title: 'Machine Learning study calendar, from 3 December 2026',
  styles: { default: { document: { run: { font: FONT, size: 20 } } } },
  sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 500, bottom: 700, left: 720, right: 720 } } },
    footers: { default: new Footer({ children: [para([run('KLAi  |  Holiday Data and AI Camp  |  Machine Learning study calendar', { size: 16, color: MUTE }), run('        Page ', { size: 16, color: MUTE }), new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 16, color: MUTE })])] }) },
    children: [header, ...title, facts, ...how, ...hol, table, ...note] }],
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync('KLAi_ML_Study_Calendar_from_3_Dec_2026.docx', b); console.log('ok'); });
