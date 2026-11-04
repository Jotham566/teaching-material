"""My_Progress_Map.pdf: one A4 page per track for the learner (KLAi brand).

  python3 build_progress_map.py            # both tracks
Output: student_materials/{ML,DA}/PDF/My_Progress_Map.pdf (build_pdfs.student() also calls build()).

Eight week rows, each with a badge name, the week's product and three stamp circles (ML adds a small fourth
stamp for the lab in weeks 1 to 4), then a finish line for the showcase and a big 'My project' box.
Badge names are in common.BADGES; the week products are WEEKLY_PRODUCT in build_camp.py.
"""
import math
import textwrap
from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from common import BADGES, TRACK_NAMES
from build_camp import WEEKLY_PRODUCT, WEEK_THEMES

CAMP = Path(__file__).resolve().parents[1]
FONTS = CAMP / 'brand' / 'fonts'
LOGO_BLACK = str(CAMP / 'brand' / 'logos' / 'klai_logo_on_black_cropped.png')
for n, f in [('Lato', 'Lato-Regular.ttf'), ('LatoB', 'Lato-Bold.ttf'), ('LatoBlack', 'Lato-Black.ttf'), ('LatoI', 'Lato-Italic.ttf')]:
    pdfmetrics.registerFont(TTFont(n, str(FONTS / f)))

INK = HexColor('#111111'); BODY = HexColor('#333333'); MUTE = HexColor('#666666'); HAIR = HexColor('#CFCFCF')
RED = HexColor('#AE2525'); GOLD = HexColor('#E0BE36'); BLACK = HexColor('#000000')
W, H = A4
MX = 36


def wrap(c, text, font, size, width):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if c.stringWidth(t, font, size) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def hexagon(c, cx, cy, r, fill, stroke=INK):
    p = c.beginPath()
    for k in range(6):
        a = math.radians(60 * k + 30)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        p.moveTo(x, y) if k == 0 else p.lineTo(x, y)
    p.close()
    c.setFillColor(fill); c.setStrokeColor(stroke); c.setLineWidth(1.6)
    c.drawPath(p, fill=1, stroke=1)


def build(code):
    out = CAMP / 'student_materials' / code / 'PDF' / 'My_Progress_Map.pdf'
    out.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(out), pagesize=A4)
    c.setTitle(f'My Progress Map: {TRACK_NAMES[code]}')
    c.setAuthor('KLAi')
    ml = code == 'ML'
    # ---- header
    hh = 84
    c.setFillColor(BLACK); c.rect(0, H - hh, W, hh, fill=1, stroke=0)
    c.drawImage(LOGO_BLACK, MX, H - 58, width=44, height=20, mask='auto', preserveAspectRatio=True)
    c.setFillColor(white); c.setFont('LatoBlack', 27)
    c.drawString(MX + 62, H - 55, 'My Progress Map')
    c.setFillColor(GOLD); c.setFont('LatoI', 11.5)
    c.drawString(MX + 62, H - 73, f'{TRACK_NAMES[code]}  |  Holiday Data and AI Camp  |  8 weeks, 8 badges')
    c.setFillColor(white); c.setFont('Lato', 9.5)
    c.drawRightString(W - MX, H - 36, 'My name or nickname:')
    c.setStrokeColor(white); c.setLineWidth(0.8); c.line(W - MX - 150, H - 56, W - MX, H - 56)
    # ---- instructions
    y = H - hh - 18
    c.setFillColor(BODY); c.setFont('Lato', 9.5)
    c.drawString(MX, y, 'Colour in a stamp when you finish a class and show what you built. Three stamps win the week\'s badge.')
    # ---- rows
    top = y - 10
    rh = 52
    stamp_x0 = 392
    c.setFont('LatoB', 8); c.setFillColor(MUTE)
    labs = ['Class 1', 'Class 2', 'Class 3'] + (['Lab'] if ml else [])
    for k, lab in enumerate(labs):
        cx = stamp_x0 + k * 46 if k < 3 else stamp_x0 + 3 * 46 - 2
        c.drawCentredString(cx, top - 6, lab)
    top -= 10
    c.setStrokeColor(INK); c.setLineWidth(1.2); c.line(MX, top, W - MX, top)
    for w in range(8):
        ytop = top - w * rh
        cy = ytop - rh / 2
        # badge hexagon with the week number
        hexagon(c, MX + 22, cy, 19, GOLD if w == 7 else white)
        c.setFillColor(INK); c.setFont('LatoBlack', 15)
        c.drawCentredString(MX + 22, cy - 5.5, str(w + 1))
        # badge name and product
        tx = MX + 54
        c.setFillColor(INK); c.setFont('LatoBlack', 13.5)
        c.drawString(tx, cy + 10, BADGES[code][w])
        c.setFillColor(BODY); c.setFont('Lato', 8.8)
        lines = wrap(c, WEEKLY_PRODUCT[code][w] + '.', 'Lato', 8.8, 270)[:2]
        for j, ln in enumerate(lines):
            c.drawString(tx, cy - 3 - j * 11, ln)
        # stamps
        for k in range(3):
            c.setStrokeColor(INK); c.setLineWidth(1.4); c.setFillColor(white)
            cx = stamp_x0 + k * 46
            c.circle(cx, cy, 14.5, fill=1, stroke=1)
            c.setFillColor(MUTE); c.setFont('Lato', 7)
            c.drawCentredString(cx, cy - 23.5, f'{code}{w * 3 + k + 1:02}')
        if ml and w < 4:
            cx = stamp_x0 + 3 * 46 - 2
            c.setStrokeColor(RED); c.setLineWidth(1.2); c.setFillColor(white)
            c.circle(cx, cy, 9, fill=1, stroke=1)
            c.setFillColor(MUTE); c.setFont('Lato', 7)
            c.drawCentredString(cx, cy - 23.5, f'F{w + 1:02}')
        c.setStrokeColor(HAIR); c.setLineWidth(0.6)
        c.line(MX, ytop - rh, W - MX, ytop - rh)
    bottom = top - 8 * rh
    # ---- finish line
    fy = bottom - 8
    sq = 7
    n = int((W - 2 * MX) / sq)
    for r in range(2):
        for k in range(n):
            c.setFillColor(BLACK if (r + k) % 2 == 0 else white)
            c.rect(MX + k * sq, fy - (r + 1) * sq, sq, sq, fill=1, stroke=0)
    c.setStrokeColor(INK); c.setLineWidth(0.6); c.rect(MX, fy - 2 * sq, n * sq, 2 * sq, fill=0, stroke=1)
    tag = 'FINISH LINE: the parent showcase'
    c.setFont('LatoBlack', 10.5)
    tw = c.stringWidth(tag, 'LatoBlack', 10.5) + 24
    c.setFillColor(GOLD); c.setStrokeColor(INK); c.setLineWidth(1.2)
    c.roundRect((W - tw) / 2, fy - 2 * sq - 9, tw, 19, 4, fill=1, stroke=1)
    c.setFillColor(INK); c.drawCentredString(W / 2, fy - 2 * sq - 3, tag)
    # ---- project box
    by_top = fy - 2 * sq - 22
    by_bot = 32
    c.setStrokeColor(INK); c.setLineWidth(1.6)
    c.roundRect(MX, by_bot, W - 2 * MX, by_top - by_bot, 6, fill=0, stroke=1)
    c.setFillColor(BLACK)
    c.roundRect(MX, by_top - 22, W - 2 * MX, 22, 6, fill=1, stroke=0)
    c.rect(MX, by_top - 22, W - 2 * MX, 10, fill=1, stroke=0)
    c.setFillColor(white); c.setFont('LatoBlack', 12.5)
    c.drawString(MX + 12, by_top - 15.5, 'My project')
    c.setFillColor(GOLD); c.setFont('LatoI', 9.5)
    c.drawRightString(W - MX - 12, by_top - 15, 'It starts in class 1 and grows every class.')
    yy = by_top - 40
    sections = [('A topic I love (class 1):', 1), ('My project idea:', 3), ('My project question (week 4):', 3)]
    avail = yy - by_bot - 8
    need = sum(14 + k * 19 for _, k in sections)
    gap = max(2, (avail - need) / 3)
    for lab, k in sections:
        c.setFillColor(INK); c.setFont('LatoB', 10.5)
        c.drawString(MX + 12, yy, lab)
        yy -= 6
        c.setStrokeColor(HAIR); c.setLineWidth(0.8)
        for _ in range(k):
            yy -= 19
            c.line(MX + 12, yy, W - MX - 12, yy)
        yy -= gap + 8
    c.setFillColor(MUTE); c.setFont('Lato', 8)
    c.drawString(MX, 20, 'KLAi  |  Holiday Data and AI Camp  |  The National ICT Innovation Hub, Nakawa')
    c.showPage()
    c.save()
    print('wrote', out.relative_to(CAMP))
    return out


if __name__ == '__main__':
    for code in ('ML', 'DA'):
        build(code)
