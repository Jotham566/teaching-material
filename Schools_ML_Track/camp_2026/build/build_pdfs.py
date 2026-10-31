"""Render the Markdown sources into KLAi-branded PDFs (A4).

  python3 build_pdfs.py instructor     # Instructor_Guide_DA.pdf, Instructor_Guide_ML.pdf (one bookmarked file per track)
  python3 build_pdfs.py student        # one print sheet per session, plus handbook and glossary PDFs, per track
  python3 build_pdfs.py all

Sources are never edited. A student session sheet adds a ruled "Your guess" box after every Predict line, because the
guess is written on paper before anything runs.
Output:
  instructor_materials/PDF/Instructor_Guide_{DA,ML}.pdf
  student_materials/{DA,ML}/PDF/*.pdf
"""
import re
import sys
import textwrap
from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether,
                                PageBreak, Flowable, NextPageTemplate, CondPageBreak)
from xml.sax.saxutils import escape

CAMP = Path(__file__).resolve().parents[1]
FONTS = CAMP / 'brand' / 'fonts'
LOGO_BLACK = str(CAMP / 'brand' / 'logos' / 'klai_logo_on_black_cropped.png')
LOGO_WHITE = str(CAMP / 'brand' / 'logos' / 'klai_logo_on_white_cropped.png')
for n, f in [('Lato', 'Lato-Regular.ttf'), ('LatoB', 'Lato-Bold.ttf'), ('LatoBlack', 'Lato-Black.ttf'), ('LatoI', 'Lato-Italic.ttf')]:
    pdfmetrics.registerFont(TTFont(n, str(FONTS / f)))
pdfmetrics.registerFontFamily('Lato', normal='Lato', bold='LatoB', italic='LatoI', boldItalic='LatoB')
MONO = 'Courier'
MONO_EM = 0.6
for p in ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/System/Library/Fonts/Supplemental/Courier New.ttf']:
    if Path(p).exists():
        pdfmetrics.registerFont(TTFont('Mono', p))
        MONO = 'Mono'
        MONO_EM = 0.602 if 'DejaVu' in p else 0.6
        break

INK = HexColor('#111111'); BODY = HexColor('#222222'); MUTE = HexColor('#666666'); HAIR = HexColor('#CFCFCF')
RED = HexColor('#AE2525'); GOLD = HexColor('#E0BE36'); BLACK = HexColor('#000000')
W, H = A4
MX, MT, MB = 20 * mm, 24 * mm, 20 * mm
CW = W - 2 * MX

ST = {
    'body': ParagraphStyle('body', fontName='Lato', fontSize=10.5, leading=15, textColor=BODY, spaceAfter=6),
    'h1': ParagraphStyle('h1', fontName='LatoBlack', fontSize=22, leading=26, textColor=INK, spaceBefore=0, spaceAfter=10),
    'h2': ParagraphStyle('h2', fontName='LatoB', fontSize=14, leading=18, textColor=INK, spaceBefore=14, spaceAfter=6, keepWithNext=1),
    'h3': ParagraphStyle('h3', fontName='LatoB', fontSize=11.5, leading=15, textColor=INK, spaceBefore=10, spaceAfter=4, keepWithNext=1),
    'li': ParagraphStyle('li', fontName='Lato', fontSize=10.5, leading=15, textColor=BODY, leftIndent=16, bulletIndent=4, spaceAfter=3),
    'cell': ParagraphStyle('cell', fontName='Lato', fontSize=9.2, leading=12, textColor=BODY),
    'cellh': ParagraphStyle('cellh', fontName='LatoB', fontSize=9.2, leading=12, textColor=INK),
    'code': ParagraphStyle('code', fontName=MONO, fontSize=8.6, leading=11.6, textColor=white),
    'note': ParagraphStyle('note', fontName='LatoI', fontSize=9.5, leading=13, textColor=MUTE, spaceAfter=6),
}


# ------------------------------------------------------------------ inline markdown
STUDENT_MODE = [False]


def inline(t):
    if STUDENT_MODE[0]:
        # the student pack ships PDFs, so a named handout points at its PDF; AI_USE_LOG.md is a file the learner makes
        t = re.sub(r'\b((?!AI_USE_LOG)[A-Z][A-Z0-9_]+)\.md\b', r'\1.pdf', t)
    t = escape(t)
    t = re.sub(r'`([^`]+)`', lambda m: f'<font name="{MONO}" size="9">{m.group(1)}</font>', t)
    t = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'(?<![\w*])\*([^*\s][^*]*)\*(?![\w*])', r'<i>\1</i>', t)
    t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1', t)       # links: keep the words, the printed sheet cannot click
    return t


class CodeBox(Flowable):
    """Black panel with the code in white monospace, like the slides. Long lines wrap with a hanging indent."""
    def __init__(self, code, width=CW, size=8.6):
        super().__init__()
        self.size = size
        self.pad = 7
        self.width = width
        maxc = int((width - 2 * self.pad) / (size * MONO_EM)) - 1
        lines = []
        for l in code.rstrip('\n').split('\n'):
            l = l.replace('\t', '    ')
            if len(l) <= maxc:
                lines.append(l)
            else:
                ind = len(l) - len(l.lstrip())
                lines += textwrap.wrap(l, maxc, subsequent_indent=' ' * (ind + 4), break_long_words=True, replace_whitespace=False)
        self.lines = lines
        self.lead = size * 1.35
        self.height = len(lines) * self.lead + 2 * self.pad

    def wrap(self, aw, ah):
        return self.width, self.height

    def split(self, aw, ah):
        n = int((ah - 2 * self.pad) / self.lead)
        if n < 3 or n >= len(self.lines):
            return []
        a = CodeBox('', self.width, self.size); a.lines = self.lines[:n]; a.height = n * self.lead + 2 * self.pad
        b = CodeBox('', self.width, self.size); b.lines = self.lines[n:]; b.height = len(b.lines) * self.lead + 2 * self.pad
        return [a, b]

    def draw(self):
        c = self.canv
        c.setFillColor(HexColor('#111111')); c.roundRect(0, 0, self.width, self.height, 3, fill=1, stroke=0)
        c.setFillColor(white); c.setFont(MONO, self.size)
        y = self.height - self.pad - self.size * 0.95
        for l in self.lines:
            c.drawString(self.pad, y, l); y -= self.lead


class GuessBox(Flowable):
    """Ruled box for the written guess before running code."""
    def __init__(self, label='Your guess, written before you run it', h=26 * mm):
        super().__init__(); self.label = label; self.h = h
    def wrap(self, aw, ah):
        return CW, self.h + 4
    def draw(self):
        c = self.canv
        c.setStrokeColor(INK); c.setLineWidth(1); c.roundRect(0, 0, CW, self.h, 3, fill=0, stroke=1)
        c.setFillColor(MUTE); c.setFont('LatoI', 8.5); c.drawString(8, self.h - 12, self.label)
        c.setStrokeColor(HAIR); c.setLineWidth(0.6)
        y = self.h - 26
        while y > 8:
            c.line(8, y, CW - 8, y); y -= 15


class Bookmark(Flowable):
    def __init__(self, title, level, key):
        super().__init__(); self.title = title; self.level = level; self.key = key
    def wrap(self, aw, ah):
        return 0, 0
    def draw(self):
        self.canv.bookmarkPage(self.key)
        self.canv.addOutlineEntry(self.title, self.key, self.level, closed=self.level > 0)


# ------------------------------------------------------------------ markdown -> flowables
def md_to_flow(md, student=False, bookmark_levels=None, key_prefix='k', h1_break=False, shift=0):
    """bookmark_levels: map markdown heading depth -> outline level (None: no outline entries)."""
    out = []
    lines = md.split('\n')
    i = 0
    n_key = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith('```'):
            j = i + 1
            while j < len(lines) and not lines[j].startswith('```'):
                j += 1
            out.append(CodeBox('\n'.join(lines[i + 1:j])))
            out.append(Spacer(1, 7))
            i = j + 1
            continue
        m = re.match(r'^(#{1,4})\s+(.*)$', ln)
        if m:
            d = len(m.group(1)) + shift
            txt = m.group(2).strip()
            d = max(1, min(3, d))
            if bookmark_levels and d in bookmark_levels:
                n_key += 1
                out.append(Bookmark(re.sub(r'[*`]', '', txt), bookmark_levels[d], f'{key_prefix}{n_key}'))
            out.append(Paragraph(inline(txt), ST[f'h{d}']))
            i += 1
            continue
        if ln.startswith('|') and i + 1 < len(lines) and re.match(r'^\|[\s:|-]+\|?$', lines[i + 1]):
            rows = []
            j = i
            while j < len(lines) and lines[j].startswith('|'):
                if not re.match(r'^\|[\s:|-]+\|?$', lines[j]):
                    rows.append([c.strip() for c in lines[j].strip().strip('|').split('|')])
                j += 1
            ncol = len(rows[0])
            data = [[Paragraph(inline(c), ST['cellh' if r == 0 else 'cell']) for c in row + [''] * (ncol - len(row))] for r, row in enumerate(rows)]
            # column widths from content length, bounded
            lens = [max(len(re.sub(r'[*`]', '', rw[c])) if c < len(rw) else 0 for rw in rows) for c in range(ncol)]
            longest = [max((len(w) for rw in rows for w in re.sub(r'[*`]', '', rw[c] if c < len(rw) else '').split()), default=4) for c in range(ncol)]
            raw = [max(min(max(l, 6), 60), lw + 3) for l, lw in zip(lens, longest)]
            tot = sum(raw)
            ws = [CW * r / tot for r in raw]
            t = Table(data, colWidths=ws, repeatRows=1)
            t.setStyle(TableStyle([('LINEBELOW', (0, 0), (-1, 0), 1.2, INK), ('LINEBELOW', (0, 1), (-1, -1), 0.5, HAIR),
                                   ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('TOPPADDING', (0, 0), (-1, -1), 4), ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                                   ('LEFTPADDING', (0, 0), (-1, -1), 4), ('RIGHTPADDING', (0, 0), (-1, -1), 6)]))
            out.append(t); out.append(Spacer(1, 8))
            i = j
            continue
        m = re.match(r'^(\s*)([-*]|\d+\.)\s+(.*)$', ln)
        if m:
            bullet = '•' if m.group(2) in '-*' else m.group(2)
            ind = len(m.group(1)) // 2
            st = ParagraphStyle('li2', parent=ST['li'], leftIndent=16 + 14 * ind, bulletIndent=4 + 14 * ind,
                                bulletFontName='LatoB', bulletColor=RED if bullet != '•' else INK)
            txt = m.group(3)
            # join wrapped continuation lines
            while i + 1 < len(lines) and lines[i + 1].startswith('  ') and not re.match(r'^\s*([-*]|\d+\.)\s', lines[i + 1]) and lines[i + 1].strip():
                i += 1; txt += ' ' + lines[i].strip()
            out.append(Paragraph(inline(txt), st, bulletText=bullet))
            i += 1
            continue
        if not ln.strip():
            i += 1
            continue
        # paragraph
        para = [ln.strip()]
        while i + 1 < len(lines) and lines[i + 1].strip() and not re.match(r'^(#{1,4}\s|```|\||\s*([-*]|\d+\.)\s)', lines[i + 1]):
            i += 1; para.append(lines[i].strip())
        txt = ' '.join(para)
        out.append(Paragraph(inline(txt), ST['body']))
        if student and txt.startswith('**Predict.**'):
            out.append(GuessBox()); out.append(Spacer(1, 8))
        i += 1
    return out


# ------------------------------------------------------------------ document
class Doc(BaseDocTemplate):
    def __init__(self, path, title, runhead, subtitle='', **kw):
        super().__init__(str(path), pagesize=A4, leftMargin=MX, rightMargin=MX, topMargin=MT, bottomMargin=MB,
                         title=title, author='KLAi', **kw)
        self.runhead = runhead
        fr = Frame(MX, MB, CW, H - MT - MB, id='f', leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([PageTemplate(id='cover', frames=[Frame(MX, MB, CW, H - 2 * MB, id='c')], onPage=self.cover),
                               PageTemplate(id='body', frames=[fr], onPage=self.page)])
        self.cover_title = title; self.cover_sub = subtitle

    def cover(self, c, doc):
        c.saveState()
        c.setFillColor(BLACK); c.rect(0, 0, W, H, fill=1, stroke=0)
        c.drawImage(LOGO_BLACK, MX, H - 38 * mm, width=34 * mm, height=15 * mm, mask='auto', preserveAspectRatio=True)
        c.setFillColor(white); c.setFont('LatoBlack', 30)
        y = H - 100 * mm
        for l in textwrap.wrap(self.cover_title, 26):
            c.drawString(MX, y, l); y -= 36
        c.setFillColor(GOLD); c.setFont('LatoI', 14)
        y -= 6
        for l in textwrap.wrap(self.cover_sub, 60):
            c.drawString(MX, y, l); y -= 20
        c.setFillColor(HexColor('#B5B5B5')); c.setFont('Lato', 9.5)
        c.drawString(MX, 28 * mm, 'Holiday Data and AI Camp  |  The National ICT Innovation Hub, Nakawa')
        c.drawString(MX, 22 * mm, 'Jotham Martin Wambi, main tutor')
        c.restoreState()

    def page(self, c, doc):
        c.saveState()
        c.drawImage(LOGO_WHITE, MX, H - 15 * mm, width=15 * mm, height=7 * mm, mask='auto', preserveAspectRatio=True)
        c.setFillColor(MUTE); c.setFont('Lato', 8.5)
        c.drawRightString(W - MX, H - 12 * mm, self.runhead)
        c.setStrokeColor(HAIR); c.setLineWidth(0.5); c.line(MX, MB - 5 * mm, W - MX, MB - 5 * mm)
        c.drawRightString(W - MX, MB - 10 * mm, str(doc.page))
        c.restoreState()


def build_doc(path, title, runhead, flow, subtitle='', cover=True):
    path.parent.mkdir(parents=True, exist_ok=True)
    d = Doc(path, title, runhead, subtitle)
    story = ([NextPageTemplate('body'), PageBreak()] if cover else [NextPageTemplate('body')]) if True else []
    if not cover:
        d.pageTemplates = [t for t in d.pageTemplates if t.id == 'body']
        story = []
    d.build(story + flow)


# ------------------------------------------------------------------ targets
def ids(track):
    d = CAMP / 'instructor_materials' / track
    return sorted(p.stem.replace('_guide', '') for p in d.glob('*_guide.md'))


def title_of(md):
    m = re.match(r'#\s+(.*)', md)
    return m.group(1).strip() if m else ''


def instructor(track):
    name = 'Python for Data Analysis' if track == 'DA' else 'Machine Learning'
    flow = [Bookmark('Contents', 0, 'toc'), Paragraph('Contents', ST['h1'])]
    flow.append(Paragraph('Private to the instructor. Each guide has the 180-minute plan, the answers, the code and the common errors for one session. Use the bookmarks panel to jump to a session.', ST['body']))
    rows = []
    guides = {}
    for i in ids(track):
        md = (CAMP / 'instructor_materials' / track / f'{i}_guide.md').read_text()
        guides[i] = md
        rows.append([Paragraph(f'<b>{i}</b>', ST['cell']), Paragraph(inline(re.sub(rf'^{i}\s+Instructor guide:\s*', '', title_of(md))), ST['cell'])])
    t = Table(rows, colWidths=[22 * mm, CW - 22 * mm])
    t.setStyle(TableStyle([('LINEBELOW', (0, 0), (-1, -1), 0.5, HAIR), ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3)]))
    flow += [t]
    for i, md in guides.items():
        flow.append(PageBreak())
        short = re.sub(r'^' + i + r'\s+Instructor guide:\s*', '', title_of(md))
        flow.append(Bookmark(i + '  ' + short, 0, 'g_' + i))
        body = md.split('\n', 1)[1] if md.startswith('# ') else md
        flow.append(Paragraph(inline(i + ': ' + short), ST['h1']))
        flow += md_to_flow(body, bookmark_levels={2: 1}, key_prefix=f'{i}_', shift=0)
    out = CAMP / 'instructor_materials' / 'PDF' / f'Instructor_Guide_{track}.pdf'
    build_doc(out, f'{name}: instructor guide', f'{name}  |  Instructor guide  |  private', flow,
              'Session-by-session plans, answers and checks for all 24 classes' + (', the four labs and the optional extension.' if track == 'ML' else '.'))
    print('wrote', out.relative_to(CAMP))


def student(track):
    sm = CAMP / 'student_materials' / track
    outdir = sm / 'PDF'
    name = 'Python for Data Analysis' if track == 'DA' else 'Machine Learning'
    made = 0
    STUDENT_MODE[0] = True
    for p in sorted(sm.glob('*.md')):
        stem = p.stem
        md = p.read_text()
        is_session = bool(re.match(r'^(DA|ML|F)\d\d$', stem))
        flow = md_to_flow(md, student=is_session, bookmark_levels={2: 0} if not is_session else None, key_prefix='s')
        build_doc(outdir / f'{stem}.pdf', title_of(md) or stem, f'{name}  |  {stem.replace("_", " ").title() if not is_session else stem}', flow, cover=False)
        made += 1
    STUDENT_MODE[0] = False
    print(track, 'student PDFs', made, '->', outdir.relative_to(CAMP))


if __name__ == '__main__':
    what = sys.argv[1] if len(sys.argv) > 1 else 'all'
    for tr in ('DA', 'ML'):
        if what in ('instructor', 'all'):
            instructor(tr)
        if what in ('student', 'all'):
            student(tr)
