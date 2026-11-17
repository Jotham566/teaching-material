// Word document for one learner's study calendar. Usage: node calendar_docx.js config.json out.docx (config from make_calendar.py)
const fs = require('fs');
const D = require('docx');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun, WidthType, ShadingType, BorderStyle, AlignmentType, VerticalAlign, Footer, PageNumber } = D;
const C = JSON.parse(fs.readFileSync(process.argv[2]));
const FONT = 'Lato', INK = '111111', RED = 'AE2525', GOLD = 'E0BE36', MUTE = '666666', HAIR = 'CFCFCF';
const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'], mons = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
const fmt = s => { const d = new Date(s + 'T12:00:00'); return `${days[d.getDay()]} ${d.getDate()} ${mons[d.getMonth()]}`; };
const none = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
const noB = { top: none, bottom: none, left: none, right: none };
const W = 10466;
const run = (t, o = {}) => new TextRun({ text: t, font: FONT, size: 20, color: INK, ...o });
const para = (children, o = {}) => new Paragraph({ children: Array.isArray(children) ? children : [children], spacing: { after: 0, before: 0 }, ...o });
const isML = C.track === 'ML';

const header = new Table({
  width: { size: W, type: WidthType.DXA }, columnWidths: [3000, 7466],
  rows: [new TableRow({ children: [
    new TableCell({ width: { size: 3000, type: WidthType.DXA }, borders: noB, shading: { type: ShadingType.CLEAR, fill: '000000' }, verticalAlign: VerticalAlign.CENTER, margins: { top: 200, bottom: 200, left: 280, right: 100 },
      children: [para(new ImageRun({ type: 'png', data: fs.readFileSync(C.logo), transformation: { width: 126, height: 40 }, altText: { title: 'KLAi', description: 'KLAi logo', name: 'logo' } }))] }),
    new TableCell({ width: { size: 7466, type: WidthType.DXA }, borders: noB, shading: { type: ShadingType.CLEAR, fill: '000000' }, verticalAlign: VerticalAlign.CENTER, margins: { top: 200, bottom: 200, left: 100, right: 280 },
      children: [para(run('Holiday Data and AI Camp', { color: 'FFFFFF', size: 22, bold: true }), { alignment: AlignmentType.RIGHT }),
                 para(run(C.trackName + ' track', { color: GOLD, size: 20 }), { alignment: AlignmentType.RIGHT })] })] })] });

const title = [
  para(run(C.learner ? `Study calendar for ${C.learner}` : 'Your study calendar', { size: 52, bold: true }), { spacing: { before: 260, after: 40 } }),
  para(run(`Starts ${C.start}. Ends with the parent showcase on ${C.end}.`, { size: 24, color: MUTE }), { spacing: { after: 200 } }),
];
const fact = (label, a, b, wd) => new TableCell({ width: { size: wd, type: WidthType.DXA }, borders: { top: { style: BorderStyle.SINGLE, size: 18, color: GOLD }, bottom: none, left: none, right: none },
  margins: { top: 100, bottom: 60, left: 0, right: 160 },
  children: [para(run(label, { size: 17, bold: true, color: MUTE, allCaps: true }), { spacing: { after: 40 } }), para(run(a, { bold: true, size: 22 })), para(run(b, { size: 19, color: '333333' }))] });
const facts = new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: [3489, 3489, 3488], rows: [new TableRow({ children: [
  fact('Every week', `${C.physicalName} in person, two classes online`, `In person ${C.inTime}. Online ${C.onTime}.`, 3489),
  isML ? fact('Short labs', 'Weeks 1 to 4, online', `${C.labTime}. Dates are in the table.`, 3489) : fact('Your build log', 'One saved thing every class', 'You show it, and keep it in your build log.', 3489),
  fact('In person at', 'The National ICT Innovation Hub, Nakawa', 'Bring your laptop and charger.', 3488)] })] });

const how = [
  para(run('How it works', { bold: true, size: 22 }), { spacing: { before: 220, after: 60 } }),
  para(run('There are no tests and no marks. In every class you build something, save it, and show it. That is the whole course.', { size: 20 }), { spacing: { after: 70 } }),
  para([run(`In person (${C.physicalName}): `, { bold: true, size: 20 }), run('three hours of hands-on building with me and a break in the middle. The first class is also in person, so we can set up your laptop together.', { size: 20, color: '333333' })], { spacing: { after: 70 } }),
  para([run('Online (the other days): ', { bold: true, size: 20 }), run('about 90 minutes live on video with screen sharing, where we learn the idea and try it. After class you finish the build in your own time, about an hour, and send me a photo or your notebook before the next class. A class link is sent before each class. You need your laptop, internet and headphones.', { size: 20, color: '333333' })], { spacing: { after: 70 } }),
  para([run('Your project: ', { bold: true, size: 20 }), run(isML ? 'think from day one about a topic you love, such as football, music or boda-boda fares. In week 4 you choose your question and in weeks 7 and 8 you build it and show your family.'
        : 'think from day one about a topic you love, such as football, music or a shop you know. In week 4 you choose your question and in weeks 7 and 8 you build it and show your family.', { size: 20, color: '333333' })]),
];
const hol = C.holidayText ? [
  para(run('Public holidays: no class', { bold: true, size: 22, color: RED }), { spacing: { before: 240, after: 60 } }),
  para([run(`${C.holidayText}. `, { size: 20 }), run(C.holidayHits ? `No session is lost. A class that would fall on a holiday moves to the next class day.${C.movedText} Your last class is ${C.lastClassText}.` : `None of your class days fall on these dates, so no class moves. Your last class is ${C.lastClassText}.`, { size: 20, color: '333333' })], { spacing: { after: 220 } })] : [para(run(' '), { spacing: { after: 160 } })];

const cw = [1500, 2300, 6666];
const border = { style: BorderStyle.SINGLE, size: 4, color: HAIR };
const cell = (kids, wd, o = {}) => new TableCell({ width: { size: wd, type: WidthType.DXA }, margins: { top: 55, bottom: 55, left: 100, right: 100 }, verticalAlign: VerticalAlign.CENTER,
  borders: { top: none, left: none, right: none, bottom: border, ...(o.borders || {}) }, shading: o.fill ? { type: ShadingType.CLEAR, fill: o.fill } : undefined, children: kids });
const out = [new TableRow({ tableHeader: true, children: ['Date', 'Time', 'What we study'].map((h, i) =>
  cell([para(run(h, { bold: true, size: 18, color: MUTE, allCaps: true }))], cw[i], { borders: { bottom: { style: BorderStyle.SINGLE, size: 12, color: INK } } })) })];
C.weeks.forEach((wk, w) => {
  const sess = C.rows.filter(r => wk.codes.includes(r.code));
  if (w === 7) C.rows.filter(r => r.kind === 'spare').forEach(r => sess.push(r));
  sess.sort((x, y) => x.date.localeCompare(y.date));
  const a = sess[0].date, b = sess[sess.length - 1].date;
  const span = a === b ? fmt(a) : `${fmt(a).slice(4)} to ${fmt(b).slice(4)}`;
  out.push(new TableRow({ cantSplit: true, children: [new TableCell({ columnSpan: 3, width: { size: W, type: WidthType.DXA }, borders: noB, shading: { type: ShadingType.CLEAR, fill: '000000' }, margins: { top: 60, bottom: 60, left: 120, right: 120 },
    children: [para([run(`Week ${w + 1}  `, { bold: true, color: GOLD, size: 21 }), run(wk.theme, { bold: true, color: 'FFFFFF', size: 21 }), run(`    ${span}`, { color: 'B5B5B5', size: 18 }), run(`    Badge: ${wk.badge}`, { color: GOLD, size: 18 })])] })] }));
  for (const r of sess) {
    const phys = r.where === 'person', lab = r.kind === 'lab', spare = r.kind === 'spare';
    const first = cell([para(run(fmt(r.date), { bold: true }))], cw[0], phys ? { borders: { left: { style: BorderStyle.SINGLE, size: 30, color: GOLD } } } : {});
    const tm = [phys ? 'In person' : lab ? 'Online lab' : 'Online', r.timeText];
    const time = cell([para(run(tm[0], { bold: true, size: 19, color: phys ? INK : MUTE })), para(run(tm[1], { size: 18, color: '333333' }))], cw[1]);
    const kids = [para([run(spare ? '' : (lab ? `Lab ${r.code}  ` : `${r.code}  `), { bold: true, color: lab ? INK : RED, size: 19 }), run(r.title, { size: 20, bold: !spare, color: spare ? MUTE : INK })])];
    if (r.build) kids.push(para([run('You build: ', { size: 18, color: RED, bold: true }), run(r.build, { size: 18, color: '333333' })], { spacing: { before: 20 } }));
    out.push(new TableRow({ cantSplit: true, children: [first, time, cell(kids, cw[2])] }));
  }
});
const table = new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: cw, rows: out });
const note = [
  ...(isML ? [para([run('Optional extra. ', { bold: true, size: 19 }), run('ML25, a first neural network, is an optional session after the course. No date is set yet.', { size: 19, color: '333333' })], { spacing: { before: 200, after: 80 } })] : [para(run(' '), { spacing: { before: 120 } })]),
  para(run('Dates assume classes start as planned. If a class is missed, we will agree a catch-up time. Questions: +256 750 990 718  |  jothammartin.wambi@gmail.com', { size: 18, color: MUTE })),
];
const doc = new Document({ creator: 'KLAi', title: `${C.trackName} study calendar, from ${C.start}`, styles: { default: { document: { run: { font: FONT, size: 20 } } } },
  sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 500, bottom: 700, left: 720, right: 720 } } },
    footers: { default: new Footer({ children: [para([run(`KLAi  |  Holiday Data and AI Camp  |  ${C.trackName} study calendar`, { size: 16, color: MUTE }), run('        Page ', { size: 16, color: MUTE }), new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 16, color: MUTE })])] }) },
    children: [header, ...title, facts, ...how, ...hol, table, ...note] }] });
Packer.toBuffer(doc).then(b => { fs.writeFileSync(process.argv[3], b); console.log('ok'); });
