/* Render one camp deck from a JSON spec written by build_slides.py.
 *
 *   node render_deck.js spec.json
 *
 * The Python side decides every position, size and run of text (it measures text with the real Lato files),
 * so this file only draws. Layouts are defined once per deck: LIGHT (white content slide with logo, session
 * label and slide number), DARK (black title/divider slide). Titles are real title placeholders, so the outline
 * view and screen readers see them.
 */
const fs = require('fs');
const path = require('path');
const pptxgen = require('pptxgenjs');
const { applyTheme } = require(process.env.PPTX_SKILL_SCRIPTS + '/apply_theme.js');

const spec = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const F = spec.fonts;           // {head, body, mono}
const BRAND = spec.brand;       // {ink, red, gold, ...}
const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE';    // 13.333 x 7.5 in
pres.title = spec.title;
pres.author = 'KLAi';
pres.company = 'KLAi';
pres.subject = spec.subject || '';

const THEME = {
  name: 'KLAi camp',
  headFontFace: F.head,
  bodyFontFace: F.body,
  colors: { dk1: '111111', lt1: 'FFFFFF', dk2: '333333', lt2: 'F1F1F1', accent1: 'AE2525', accent2: 'E0BE36', accent3: '8C8C8C',
            accent4: '555555', accent5: 'CFCFCF', accent6: '000000', hlink: 'AE2525', folHlink: '666666' },
};

const logoW = spec.logo.w_small, logoH = spec.logo.h_small;
pres.defineSlideMaster({
  title: 'KLAI_LIGHT',
  background: { color: 'FFFFFF' },
  objects: [
    { image: { path: spec.logo.on_white, x: 0.7, y: 7.02, w: logoW, h: logoH } },
    { text: { text: spec.footer, options: { x: 0.7 + logoW + 0.25, y: 7.0, w: 9.0, h: 0.3, fontFace: F.body, fontSize: 12, color: '666666', margin: 0, valign: 'middle' } } },
    { placeholder: { options: { name: 'title', type: 'title', x: 0.7, y: 0.42, w: 11.9, h: 1.15, fontFace: F.head, bold: true, color: '111111', margin: 0, valign: 'top', align: 'left' }, text: '' } },
  ],
  slideNumber: { x: 11.6, y: 7.0, w: 1.03, h: 0.3, fontFace: F.body, fontSize: 12, color: '666666', align: 'right' },
});
pres.defineSlideMaster({
  title: 'KLAI_DARK',
  background: { color: '000000' },
  objects: [
    { image: { path: spec.logo.on_black, x: 0.7, y: 0.6, w: spec.logo.w_large, h: spec.logo.h_large } },
    { placeholder: { options: { name: 'title', type: 'title', x: 0.7, y: 2.3, w: 11.6, h: 2.5, fontFace: F.head, bold: true, color: 'FFFFFF', margin: 0, valign: 'top', align: 'left' }, text: '' } },
  ],
});

let lastSection = null;
for (const sl of spec.slides) {
  if (sl.section && sl.section !== lastSection) { pres.addSection({ title: sl.section }); lastSection = sl.section; }
  const slide = pres.addSlide({ masterName: sl.layout === 'dark' ? 'KLAI_DARK' : 'KLAI_LIGHT', sectionTitle: sl.section || undefined });
  if (sl.title) {
    slide.addText(sl.title.text, { placeholder: 'title', fontSize: sl.title.size, lineSpacing: sl.title.lead, fit: 'none' });
  }
  for (const o of sl.objects) {
    if (o.type === 'text') {
      const opts = { x: o.x, y: o.y, w: o.w, h: o.h, margin: 0, isTextBox: true, fontFace: o.font || F.body, fontSize: o.size, color: o.color || '111111',
                     bold: !!o.bold, italic: !!o.italic, align: o.align || 'left', valign: o.valign || 'top', fit: 'none', wrap: true };
      if (o.lead) opts.lineSpacing = o.lead;
      if (o.para) opts.paraSpaceAfter = o.para;
      slide.addText(o.runs ? o.runs.map(r => ({ text: r.text, options: Object.assign({}, r.o || {}) })) : o.text, opts);
    } else if (o.type === 'image') {
      slide.addImage({ path: o.path, x: o.x, y: o.y, w: o.w, h: o.h, altText: o.alt || '' });
    } else if (o.type === 'rect') {
      const so = { x: o.x, y: o.y, w: o.w, h: o.h, fill: o.fill ? { color: o.fill } : { type: 'none' }, line: o.line ? { color: o.line, width: o.lineW || 1 } : { type: 'none' } };
      if (o.radius) { so.rectRadius = o.radius; slide.addShape(pres.ShapeType.roundRect, so); } else slide.addShape(pres.ShapeType.rect, so);
    } else if (o.type === 'line') {
      slide.addShape(pres.ShapeType.line, { x: Math.min(o.x1, o.x2), y: Math.min(o.y1, o.y2), w: Math.abs(o.x2 - o.x1), h: Math.abs(o.y2 - o.y1),
                                            line: { color: o.color || 'CFCFCF', width: o.w || 1, dashType: o.dash ? 'dash' : 'solid' } });
    }
  }
  if (sl.notes) slide.addNotes(sl.notes);
}

(async () => {
  fs.mkdirSync(path.dirname(spec.out), { recursive: true });
  await pres.writeFile({ fileName: spec.out });
  await applyTheme(spec.out, THEME);
  console.log('wrote ' + spec.out + ' (' + spec.slides.length + ' slides)');
})();
