"""Flat illustrations for the Applied AI and Automation decks.

Every picture is drawn here with Pillow, so it can be regenerated and edited. No
photographs and no third-party artwork are used. Run:

  python3 illustrations.py OUTPUT_FOLDER

It writes one transparent PNG per motif (light theme, for white slides) and one hero
PNG per session (dark theme, for the navy title slides). Colours follow the decks.
Drawing happens in a 100 x 100 unit square; units are scaled and supersampled.
"""
import sys, math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

PX = 900            # output size in pixels
SS = 2              # supersampling factor
# Lato Bold (SIL Open Font License 1.1) is bundled so the pictures render identically on any machine.
FONT = Path(__file__).resolve().parent / 'fonts' / 'Lato-Bold.ttf'
if not FONT.exists(): raise SystemExit(f'Bundled font missing: {FONT}')

LIGHT = dict(ink='#1C3144', teal='#246E63', orange='#C94E29', pale='#E9F3F0', line='#C9D5DA', paper='#F1F5F6', white='#FFFFFF', soft='#9CC5BC')
DARK = dict(ink='#E9F3F0', teal='#5DB5A6', orange='#F08A5D', pale='#2B4A5F', line='#4B6A7E', paper='#25455A', white='#1C3144', soft='#3A7F75')


class C:
    def __init__(self, theme):
        self.t = theme
        self.s = PX * SS / 100.0
        self.im = Image.new('RGBA', (PX * SS, PX * SS), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)

    def u(self, v): return v * self.s
    def col(self, c): return self.t.get(c, c)

    def rect(self, x, y, w, h, fill=None, outline=None, r=0, wd=1.1):
        self.d.rounded_rectangle([self.u(x), self.u(y), self.u(x + w), self.u(y + h)], radius=self.u(r),
                                 fill=self.col(fill) if fill else None, outline=self.col(outline) if outline else None, width=int(self.u(wd)))

    def circ(self, x, y, r, fill=None, outline=None, wd=1.1):
        self.d.ellipse([self.u(x - r), self.u(y - r), self.u(x + r), self.u(y + r)], fill=self.col(fill) if fill else None,
                       outline=self.col(outline) if outline else None, width=int(self.u(wd)))

    def line(self, pts, color='ink', wd=1.1, dash=None):
        P = [(self.u(a), self.u(b)) for a, b in pts]
        if dash:
            for (x1, y1), (x2, y2) in zip(P, P[1:]):
                L = math.hypot(x2 - x1, y2 - y1); n = int(L / self.u(dash));
                for i in range(0, n, 2):
                    a = i / max(n, 1); b = min((i + 1) / max(n, 1), 1)
                    self.d.line([(x1 + (x2 - x1) * a, y1 + (y2 - y1) * a), (x1 + (x2 - x1) * b, y1 + (y2 - y1) * b)], fill=self.col(color), width=int(self.u(wd)))
        else:
            self.d.line(P, fill=self.col(color), width=int(self.u(wd)), joint='curve')
            r = self.u(wd) / 2
            for x, y in (P[0], P[-1]): self.d.ellipse([x - r, y - r, x + r, y + r], fill=self.col(color))

    def poly(self, pts, fill=None, outline=None, wd=1.1):
        P = [(self.u(a), self.u(b)) for a, b in pts]
        if fill: self.d.polygon(P, fill=self.col(fill))
        if outline: self.d.line(P + [P[0]], fill=self.col(outline), width=int(self.u(wd)), joint='curve')

    def arrow(self, x1, y1, x2, y2, color='teal', wd=1.3, head=3.2):
        self.line([(x1, y1), (x2, y2)], color, wd)
        a = math.atan2(y2 - y1, x2 - x1)
        p = [(x2, y2), (x2 - head * math.cos(a - 0.45), y2 - head * math.sin(a - 0.45)), (x2 - head * math.cos(a + 0.45), y2 - head * math.sin(a + 0.45))]
        self.poly(p, fill=color)

    def text(self, x, y, s, size=5, color='ink', anchor='la'):
        f = ImageFont.truetype(str(FONT), int(self.u(size)))
        self.d.text((self.u(x), self.u(y)), s, font=f, fill=self.col(color), anchor=anchor)

    def arc(self, cx, cy, r, a0, a1, color='teal', wd=1.3):
        self.d.arc([self.u(cx - r), self.u(cy - r), self.u(cx + r), self.u(cy + r)], a0, a1, fill=self.col(color), width=int(self.u(wd)))

    def save(self, path):
        im = self.im.resize((PX, PX), Image.LANCZOS)
        im.save(path)


# ---------- shared parts ----------
def doc(c, x, y, w, h, lines=4, fill='white', accent=None, mark=None):
    fold = min(w, h) * 0.22
    c.poly([(x, y), (x + w - fold, y), (x + w, y + fold), (x + w, y + h), (x, y + h)], fill=fill, outline='ink', wd=1.0)
    c.poly([(x + w - fold, y), (x + w - fold, y + fold), (x + w, y + fold)], fill='line', outline='ink', wd=0.8)
    for i in range(lines):
        ly = y + fold + 3 + i * (h - fold - 7) / max(lines, 1)
        lw = (w - 10) * (0.55 if i == lines - 1 else 1.0)
        col = 'orange' if accent is not None and i == accent else 'line'
        c.line([(x + 5, ly), (x + 5 + lw, ly)], col, 1.4 if col == 'orange' else 1.2)
    if mark == 'check': check(c, x + w - 2, y + h - 2, 7)
    if mark == 'x': xmark(c, x + w - 2, y + h - 2, 7)

def check(c, cx, cy, r, color='teal'):
    c.circ(cx, cy, r, fill=color)
    c.line([(cx - r * .45, cy), (cx - r * .1, cy + r * .38), (cx + r * .5, cy - r * .35)], 'white', max(1.0, r * .25))

def xmark(c, cx, cy, r, color='orange'):
    c.circ(cx, cy, r, fill=color)
    c.line([(cx - r * .4, cy - r * .4), (cx + r * .4, cy + r * .4)], 'white', max(1.0, r * .25))
    c.line([(cx - r * .4, cy + r * .4), (cx + r * .4, cy - r * .4)], 'white', max(1.0, r * .25))

def person(c, x, y, s=1.0, body='teal', head='soft'):
    c.circ(x, y, 5 * s, fill=head, outline='ink', wd=0.9)
    c.poly([(x - 8 * s, y + 20 * s), (x - 6 * s, y + 8 * s), (x + 6 * s, y + 8 * s), (x + 8 * s, y + 20 * s)], fill=body, outline='ink', wd=0.9)

def building(c, x, y, w, h, fill, label=None):
    c.rect(x, y, w, h, fill=fill, outline='ink', r=1, wd=1.0)
    c.poly([(x - 2, y), (x + w / 2, y - 7), (x + w + 2, y)], fill='ink')
    cols = 3; rows = max(2, int(h // 14))
    for i in range(cols):
        for j in range(rows - 1):
            c.rect(x + 4 + i * (w - 8) / cols, y + 6 + j * 12, (w - 8) / cols - 3, 7, fill='white', outline=None, r=0.5)
    c.rect(x + w / 2 - 3, y + h - 8, 6, 8, fill='ink', r=0.5)

def gear(c, cx, cy, r, color='teal', teeth=8):
    pts = []
    for i in range(teeth * 2):
        a = math.pi * i / teeth
        rr = r if i % 2 == 0 else r * 0.8
        for da in (-0.12, 0.12) if i % 2 == 0 else (-0.12, 0.12):
            pts.append((cx + rr * math.cos(a + da), cy + rr * math.sin(a + da)))
    c.poly(pts, fill=color, outline='ink', wd=0.9)
    c.circ(cx, cy, r * 0.35, fill='white', outline='ink', wd=0.9)


# ---------- motifs ----------
def parties(c):
    building(c, 8, 38, 30, 46, 'pale'); building(c, 62, 30, 30, 54, 'paper')
    c.text(23, 90, 'Victoria', 5, 'teal', 'ma'); c.text(77, 90, 'Equator', 5, 'ink', 'ma')
    doc(c, 40, 34, 20, 26, lines=3, accent=1)
    c.line([(38, 70), (62, 70)], 'orange', 1.1, dash=2.5)

def docstack(c):
    doc(c, 24, 20, 46, 58, lines=0, fill='paper'); doc(c, 18, 14, 46, 58, lines=0, fill='pale')
    doc(c, 12, 8, 46, 58, lines=6, accent=2)
    c.circ(66, 70, 11, fill='orange', outline='ink', wd=0.9); c.line([(61, 70), (65, 74), (72, 65)], 'white', 2.2)
    c.poly([(60, 78), (58, 92), (66, 87), (74, 92), (72, 78)], fill='orange', outline='ink', wd=0.9)

def magnifier(c):
    doc(c, 14, 14, 50, 66, lines=7, accent=3)
    c.circ(62, 58, 16, fill=None, outline='ink', wd=2.2); c.circ(62, 58, 14, fill='#FFFFFF33')
    c.line([(73, 70), (88, 88)], 'ink', 3.4)
    c.circ(62, 58, 4, fill='orange')

def cogs(c):
    gear(c, 38, 48, 22, 'teal'); gear(c, 70, 66, 15, 'orange', 7)
    check(c, 78, 26, 9)

def network(c):
    xs = [16, 40, 64, 86]; layers = [[34, 66], [22, 50, 78], [22, 50, 78], [50]]
    for a in range(3):
        for y1 in layers[a]:
            for y2 in layers[a + 1]: c.line([(xs[a], y1), (xs[a + 1], y2)], 'soft', 0.7)
    for i, ys in enumerate(layers):
        for y in ys: c.circ(xs[i], y, 5.2, fill='orange' if i == 3 else 'white', outline='teal', wd=1.0)
    c.text(50, 92, 'learned connections', 4.6, 'teal', 'ma')

def tokens(c):
    words = [('The', 103), ('provider', 285), ('remains', 914)]
    y = 18
    for i, (w, n) in enumerate(words):
        c.rect(12, y + i * 26, 50, 16, fill='pale', outline='teal', r=3); c.text(37, y + i * 26 + 8, w, 7, 'ink', 'mm')
        c.arrow(64, y + i * 26 + 8, 74, y + i * 26 + 8, 'teal', 1.0, 2.5)
        c.rect(76, y + i * 26, 16, 16, fill='orange', r=3); c.text(84, y + i * 26 + 8, str(n), 5.2, 'white', 'mm')

def vecmap(c):
    c.line([(12, 86), (12, 12)], 'ink', 1.0); c.line([(12, 86), (90, 86)], 'ink', 1.0)
    pts = [(62, 30, 'soft'), (70, 38, 'soft'), (58, 42, 'soft'), (30, 66, 'line'), (78, 74, 'line'), (24, 28, 'line')]
    for x, y, col in pts: c.circ(x, y, 4.2, fill=col, outline='ink', wd=0.8)
    c.circ(48, 46, 5.2, fill='orange', outline='ink', wd=0.9); c.circ(48, 46, 15, outline='orange', wd=0.9)
    c.line([(48, 46), (62, 30)], 'orange', 0.9, dash=2)

def cycle(c):
    cx, cy, r = 50, 50, 28
    for i in range(4):
        a0 = -90 + i * 90 + 14; a1 = a0 + 62
        c.arc(cx, cy, r, a0, a1, 'teal', 1.6)
        a = math.radians(a1); x = cx + r * math.cos(a); y = cy + r * math.sin(a)
        tx, ty = -math.sin(a), math.cos(a)
        c.poly([(x + tx * 4, y + ty * 4), (x - ty * 3.0, y + tx * 3.0), (x + ty * 3.0, y - tx * 3.0)], fill='teal')
    for i, col in enumerate(['orange', 'teal', 'teal', 'ink']):
        a = math.radians(-90 + i * 90 - 22 + 22); x = cx + r * math.cos(math.radians(-45 + i * 90)); y = cy + r * math.sin(math.radians(-45 + i * 90))
    for i, (x, y) in enumerate([(50, 20), (80, 50), (50, 80), (20, 50)]):
        c.circ(x, y, 7, fill=['orange', 'teal', 'teal', 'ink'][i], outline='ink', wd=0.9); c.text(x, y, str(i + 1), 6, 'white', 'mm')

def scales(c):
    c.rect(46, 20, 8, 66, fill='ink', r=1); c.rect(30, 84, 40, 6, fill='ink', r=1.5)
    c.line([(16, 28), (84, 28)], 'ink', 1.8); c.circ(50, 24, 4, fill='orange', outline='ink', wd=0.8)
    for x in (16, 84):
        c.line([(x, 28), (x - 10, 54)], 'ink', 0.7); c.line([(x, 28), (x + 10, 54)], 'ink', 0.7)
        c.poly([(x - 14, 54), (x + 14, 54), (x + 9, 62), (x - 9, 62)], fill='teal', outline='ink', wd=0.9)

def shield(c):
    c.poly([(50, 10), (82, 20), (80, 56), (50, 90), (20, 56), (18, 20)], fill='pale', outline='ink', wd=1.4)
    c.rect(38, 44, 24, 20, fill='teal', outline='ink', r=3, wd=1.0); c.arc(50, 44, 8, 180, 360, 'ink', 1.8)
    c.circ(50, 54, 2.6, fill='white')

def deskperson(c):
    c.rect(10, 70, 80, 6, fill='ink', r=1.5); c.line([(18, 76), (18, 92)], 'ink', 1.6); c.line([(82, 76), (82, 92)], 'ink', 1.6)
    person(c, 32, 30, 1.5)
    doc(c, 54, 38, 30, 36, lines=4, accent=1); check(c, 80, 40, 7)

def funnel(c):
    for i, x in enumerate((14, 34, 54)): doc(c, x, 6 + i * 3, 18, 22, lines=2, fill='paper' if i != 1 else 'pale')
    c.poly([(10, 38), (90, 38), (58, 66), (58, 80), (42, 80), (42, 66)], fill='pale', outline='ink', wd=1.3)
    c.line([(24, 46), (76, 46)], 'soft', 1.0); c.line([(34, 54), (66, 54)], 'soft', 1.0)
    doc(c, 40, 82, 20, 16, lines=1, accent=0);

def database(c):
    for i in range(3):
        y = 22 + i * 20
        c.rect(14, y, 40, 20, fill='pale', outline='ink', r=3, wd=1.0); c.circ(24, y + 10, 2.6, fill='teal')
        c.line([(32, y + 10), (48, y + 10)], 'soft', 1.2)
    c.poly([(60, 40), (62, 32), (78, 32), (80, 38), (90, 38), (90, 72), (60, 72)], fill='orange', outline='ink', wd=1.0)
    c.text(75, 56, 'M-01', 6, 'white', 'mm')

def scanpage(c):
    doc(c, 18, 10, 50, 72, lines=0)
    for i, (w, col) in enumerate([(34, 'ink'), (30, 'ink'), (34, 'line'), (22, 'line'), (30, 'line')]):
        c.line([(24, 30 + i * 9), (24 + w, 30 + i * 9)], col, 1.3)
    c.rect(14, 44, 58, 6, fill='#C94E2988', r=1)
    c.text(78, 40, '?', 22, 'orange', 'mm'); c.text(24, 18, 'That c0nsent n0t', 4.2, 'ink')

def bars(c):
    c.line([(10, 86), (92, 86)], 'ink', 1.2)
    data = [(14, 18, 'teal'), (34, 30, 'soft'), (54, 38, 'soft'), (74, 60, 'orange')]
    for x, top, col in data: c.rect(x, top + 12, 14, 74 - top - 12 + 0, fill=col, outline='ink', r=1.2, wd=0.9)
    c.arrow(20, 12, 82, 54, 'ink', 1.0, 3)

def ledger(c):
    doc(c, 10, 14, 46, 64, lines=0)
    for i in range(6):
        c.line([(15, 26 + i * 9), (51, 26 + i * 9)], 'line', 1.0); c.line([(35, 22), (35, 74)], 'line', 0.8)
    c.line([(15, 68), (51, 68)], 'ink', 1.4); c.circ(46, 60, 4, outline='orange', wd=1.0)
    c.rect(58, 42, 32, 46, fill='ink', r=4)
    c.rect(62, 46, 24, 10, fill='pale', r=1)
    for i in range(3):
        for j in range(3): c.rect(62 + j * 8.4, 60 + i * 8, 6.4, 6, fill='teal' if (i, j) != (2, 2) else 'orange', r=1)

def agent(c):
    c.line([(50, 14), (50, 24)], 'ink', 1.5); c.circ(50, 12, 3.6, fill='orange', outline='ink', wd=0.9)
    c.rect(24, 24, 52, 38, fill='pale', outline='ink', r=9, wd=1.3)
    c.circ(39, 42, 5, fill='white', outline='ink', wd=1.0); c.circ(61, 42, 5, fill='white', outline='ink', wd=1.0); c.circ(40, 43, 2, fill='ink'); c.circ(62, 43, 2, fill='ink')
    c.line([(40, 54), (60, 54)], 'ink', 1.2)
    c.rect(32, 64, 36, 22, fill='teal', outline='ink', r=5, wd=1.2)
    for i, x in enumerate((8, 76)):
        c.line([(32 if i == 0 else 68, 70), (x + 8, 76)], 'ink', 1.6)
    c.rect(78, 70, 14, 14, fill='orange', outline='ink', r=3, wd=0.9)

def flow(c):
    boxes = [(6, 38), (40, 38)]
    c.rect(6, 38, 22, 20, fill='pale', outline='ink', r=3); c.arrow(28, 48, 38, 48, 'teal', 1.0, 2.5)
    c.poly([(50, 36), (62, 48), (50, 60), (38, 48)], fill='orange', outline='ink', wd=1.0); c.arrow(62, 48, 70, 48, 'teal', 1.0, 2.5)
    c.rect(72, 38, 22, 20, fill='pale', outline='ink', r=3); c.line([(50, 60), (50, 82)], 'teal', 1.2)
    c.rect(38, 80, 24, 12, fill='paper', outline='ink', r=3)
    c.text(17, 48, 'in', 5, 'ink', 'mm'); c.text(83, 48, 'out', 5, 'ink', 'mm'); c.text(50, 86, 'review', 4.6, 'ink', 'mm')

def stopgate(c):
    c.rect(8, 56, 84, 8, fill='orange', outline='ink', r=1.5)
    for i in range(5): c.poly([(14 + i * 16, 56), (22 + i * 16, 56), (18 + i * 16, 64), (10 + i * 16, 64)], fill='white')
    c.rect(8, 40, 8, 52, fill='ink', r=1.5)
    c.poly([(36, 12), (64, 12), (80, 28), (80, 44) ,(64, 44), (36, 44), (20, 28)], fill=None)
    c.circ(66, 28, 14, fill='orange', outline='ink', wd=1.2); c.line([(66, 20), (66, 30)], 'white', 2.4); c.circ(66, 36, 1.8, fill='white')

def envelope(c):
    c.rect(10, 28, 64, 46, fill='white', outline='ink', r=3, wd=1.2)
    c.line([(10, 30), (42, 54), (74, 30)], 'ink', 1.2)
    c.poly([(74, 46), (92, 76), (56, 76)], fill='orange', outline='ink', wd=1.1)
    c.line([(74, 55), (74, 66)], 'white', 2.2); c.circ(74, 71, 1.5, fill='white')

def timeline(c):
    c.line([(8, 60), (92, 60)], 'ink', 1.6)
    for x, lab, col in ((18, '0', 'ink'), (42, '30', 'teal'), (66, '60', 'teal'), (88, '90', 'orange')):
        c.circ(x, 60, 3.4, fill=col, outline='ink', wd=0.8)
        if x > 20: c.line([(x, 60), (x, 36)], 'ink', 1.0); c.poly([(x, 36), (x + 12, 40), (x, 44)], fill=col, outline='ink', wd=0.8)
        c.text(x, 70, lab, 6, 'ink', 'ma')
    c.text(50, 88, 'days after approval', 5, 'teal', 'ma')

def team(c):
    for x, y, s, b in ((26, 40, 1.15, 'teal'), (74, 40, 1.15, 'orange'), (50, 34, 1.4, 'ink')): person(c, x, y, s, b)
    c.line([(12, 82), (88, 82)], 'line', 1.0)

def hourglass(c):
    c.rect(24, 12, 34, 5, fill='ink', r=1.5); c.rect(24, 78, 34, 5, fill='ink', r=1.5)
    c.poly([(28, 17), (54, 17), (45, 47), (54, 78), (28, 78), (37, 47)], fill='pale', outline='ink', wd=1.2)
    c.poly([(32, 70), (50, 70), (46, 62), (36, 62)], fill='orange'); c.poly([(36, 24), (46, 24), (41, 36)], fill='orange')
    for i, (x, y) in enumerate(((72, 66), (80, 56), (72, 46))): c.circ(x, y, 7, fill='orange', outline='ink', wd=0.9)

def stairs(c):
    for i in range(4): c.rect(10 + i * 20, 70 - i * 15, 20, 20 + i * 15, fill=['line', 'soft', 'teal', 'pale'][i], outline='ink', wd=0.9)
    c.line([(80, 28), (80, 8)], 'ink', 1.4); c.poly([(80, 8), (94, 13), (80, 18)], fill='orange', outline='ink', wd=0.8)

def books(c):
    for i, (w, col) in enumerate(((54, 'teal'), (48, 'orange'), (58, 'ink'))):
        y = 62 - i * 17; c.rect(14, y, w, 15, fill=col, outline='ink', r=2, wd=0.9); c.line([(20, y + 7), (14 + w - 8, y + 7)], 'white', 1.0)
    c.poly([(74, 14), (90, 14), (90, 50), (82, 44), (74, 50)], fill='orange', outline='ink', wd=0.9)

def warn(c):
    doc(c, 12, 26, 46, 60, lines=5, accent=2)
    c.poly([(70, 16), (94, 58), (46, 58)], fill='orange', outline='ink', wd=1.3); c.line([(70, 28), (70, 44)], 'white', 2.8); c.circ(70, 51, 2, fill='white')

def clipboard(c):
    c.rect(18, 14, 56, 74, fill='white', outline='ink', r=4, wd=1.2); c.rect(34, 8, 24, 12, fill='ink', r=3)
    for i in range(4):
        y = 28 + i * 14; c.rect(26, y, 8, 8, fill='pale', outline='ink', r=1, wd=0.8)
        c.line([(40, y + 4), (66, y + 4)], 'line', 1.4)
        if i < 3: c.line([(27, y + 4), (30, y + 7), (34, y + 1)], 'teal', 1.4)
    check(c, 76, 76, 9, 'orange')

def cloud(c):
    c.circ(36, 44, 14, fill='pale', outline='ink', wd=1.2); c.circ(54, 36, 18, fill='pale', outline='ink', wd=1.2); c.circ(72, 46, 13, fill='pale', outline='ink', wd=1.2)
    c.rect(34, 44, 40, 16, fill='pale'); c.line([(26, 58), (82, 58)], 'ink', 1.2)
    c.arrow(54, 80, 54, 52, 'orange', 1.6, 4); c.rect(36, 82, 36, 10, fill='ink', r=2)

def chat(c):
    c.rect(8, 12, 54, 32, fill='pale', outline='ink', r=7, wd=1.2); c.poly([(18, 44), (18, 54), (30, 44)], fill='pale', outline='ink', wd=1.0)
    for i in range(2): c.line([(16, 24 + i * 9), (52 - i * 10, 24 + i * 9)], 'soft', 1.4)
    c.rect(38, 50, 54, 34, fill='teal', outline='ink', r=7, wd=1.2); c.poly([(80, 84), (80, 94), (68, 84)], fill='teal', outline='ink', wd=1.0)
    for i in range(3): c.line([(46, 60 + i * 8), (82 - i * 10, 60 + i * 8)], 'white', 1.4)

def bulb(c):
    c.circ(50, 40, 22, fill='pale', outline='ink', wd=1.3); c.rect(42, 62, 16, 12, fill='ink', r=2); c.rect(44, 76, 12, 5, fill='ink', r=2)
    c.line([(44, 44), (50, 34), (56, 44)], 'orange', 1.4)
    for a in (-60, -30, 0, 30, 60, 150, 180, 210):
        r1, r2 = 28, 36; x1 = 50 + r1 * math.cos(math.radians(a - 90)); y1 = 40 + r1 * math.sin(math.radians(a - 90)); x2 = 50 + r2 * math.cos(math.radians(a - 90)); y2 = 40 + r2 * math.sin(math.radians(a - 90))
        c.line([(x1, y1), (x2, y2)], 'orange', 1.2)

def tree(c):
    c.rect(36, 10, 28, 14, fill='ink', r=3)
    for i, x in enumerate((16, 50, 84)):
        c.line([(50, 24), (x, 48)], 'ink', 1.2); c.rect(x - 11, 48, 22, 14, fill=['pale', 'teal', 'orange'][i], outline='ink', r=3, wd=0.9)
        c.line([(x, 62), (x, 76)], 'ink', 1.0); c.circ(x, 82, 5, fill='white', outline='ink', wd=0.9)

def puzzle(c):
    c.rect(10, 28, 38, 38, fill='teal', outline='ink', r=3, wd=1.1); c.circ(48, 47, 7, fill='teal', outline='ink', wd=1.1); c.rect(42, 40, 8, 14, fill='teal')
    c.rect(52, 28, 38, 38, fill='orange', outline='ink', r=3, wd=1.1); c.circ(52, 47, 7, fill='white', outline='ink', wd=1.1); c.rect(48, 41, 6, 12, fill='orange')
    c.text(29, 47, 'words', 6, 'white', 'mm'); c.text(72, 47, 'meaning', 6, 'white', 'mm')

def key(c):
    doc(c, 40, 16, 44, 58, lines=4, accent=0)
    c.circ(24, 62, 12, fill='orange', outline='ink', wd=1.2); c.circ(24, 62, 4.4, fill='white', outline='ink', wd=0.9)
    c.line([(35, 70), (62, 90)], 'ink', 3.2); c.line([(52, 84), (52, 92)], 'ink', 2.4); c.line([(60, 88), (60, 94)], 'ink', 2.4)

def gap(c):
    c.poly([(12, 12), (46, 12), (46, 44), (12, 44)], fill='white', outline='ink', wd=1.0)
    c.poly([(48, 12), (82, 12), (82, 44), (48, 44)], fill=None, outline='orange', wd=1.0)
    c.line([(48, 12), (82, 12), (82, 44), (48, 44), (48, 12)], 'orange', 1.1, dash=2.4)
    doc(c, 12, 50, 70, 38, lines=0, fill='white')
    for i in range(3): c.line([(18, 62 + i * 8), (60, 62 + i * 8)], 'line', 1.3)
    c.text(65, 26, '?', 26, 'orange', 'mm')

def dice(c):
    c.rect(14, 28, 40, 40, fill='white', outline='ink', r=7, wd=1.4)
    for x, y in ((24, 38), (34, 48), (44, 58)): c.circ(x, y, 3.2, fill='ink')
    c.poly([(60, 40), (82, 28), (92, 54), (70, 66)], fill='orange', outline='ink', wd=1.3)
    for x, y in ((70, 42), (82, 52), (76, 48), (70, 58), (80, 62)): c.circ(x - 4, y - 3, 1.7, fill='white')

def window(c):
    c.rect(8, 10, 66, 76, fill='paper', outline='ink', r=5, wd=1.4); c.text(41, 16, 'in the window', 4.6, 'teal', 'ma')
    for i, (lab, col) in enumerate((('instructions', 'soft'), ('evidence', 'teal'), ('conversation', 'soft'), ('answer', 'orange'))):
        c.rect(14, 26 + i * 15, 54, 11, fill=col, r=2.5); c.text(41, 31.5 + i * 15, lab, 5, 'white' if col != 'soft' else 'ink', 'mm')
    doc(c, 78, 40, 16, 22, lines=2, fill='white'); c.line([(76, 52), (74, 52)], 'ink', 1.0)
    c.text(86, 68, 'file', 4.6, 'ink', 'ma')

def stamp(c):
    c.rect(34, 12, 32, 12, fill='ink', r=3); c.rect(42, 24, 16, 22, fill='ink', r=2); c.rect(26, 46, 48, 16, fill='teal', outline='ink', r=3, wd=1.0)
    c.rect(10, 70, 80, 20, fill='white', outline='ink', r=2, wd=1.0); check(c, 50, 80, 7, 'orange')

def rewind(c):
    c.circ(50, 50, 30, fill='pale', outline='ink', wd=1.4); c.line([(50, 50), (50, 30)], 'ink', 2.0); c.line([(50, 50), (64, 56)], 'orange', 2.0)
    c.arc(50, 50, 38, 200, 340, 'teal', 1.8); c.poly([(18, 34), (10, 46), (26, 44)], fill='teal')

def laptop(c):
    c.rect(18, 20, 64, 44, fill='white', outline='ink', r=3, wd=1.4); c.poly([(8, 70), (92, 70), (84, 64), (16, 64)], fill='ink')
    c.rect(8, 70, 84, 5, fill='ink', r=2)
    for i in range(3):
        y = 28 + i * 11; c.rect(24, y, 6, 6, fill='pale', outline='teal', r=1, wd=0.8); c.line([(36, y + 3), (70, y + 3)], 'line', 1.4)
        if i < 2: c.line([(25, y + 3), (27, y + 5), (30, y + 1)], 'teal', 1.2)
    c.circ(78, 24, 6, fill='orange')

def target(c):
    for r, col in ((34, 'pale'), (24, 'soft'), (14, 'teal'), (5, 'orange')): c.circ(46, 54, r, fill=col, outline='ink', wd=0.9)
    c.line([(46, 54), (84, 16)], 'ink', 1.6); c.poly([(84, 16), (92, 14), (90, 22)], fill='ink')
    c.poly([(80, 10), (92, 8), (86, 20)], fill='orange')

def signpost(c):
    c.rect(46, 14, 8, 78, fill='ink', r=1.5)
    c.poly([(54, 22), (84, 22), (92, 30), (84, 38), (54, 38)], fill='teal', outline='ink', wd=1.0)
    c.poly([(46, 46), (16, 46), (8, 54), (16, 62), (46, 62)], fill='orange', outline='ink', wd=1.0)
    c.text(68, 30, 'go', 6, 'white', 'mm'); c.text(28, 54, 'stop', 6, 'white', 'mm')

def question(c):
    c.rect(16, 12, 68, 52, fill='pale', outline='ink', r=10, wd=1.4); c.poly([(30, 64), (30, 80), (46, 64)], fill='pale', outline='ink', wd=1.2)
    c.text(50, 38, '?', 40, 'orange', 'mm')

def compass(c):
    c.circ(50, 50, 36, fill='pale', outline='ink', wd=1.6)
    c.poly([(50, 18), (58, 50), (50, 82), (42, 50)], fill='soft', outline='ink', wd=1.0); c.poly([(50, 18), (58, 50), (42, 50)], fill='orange', outline='ink', wd=1.0)
    c.circ(50, 50, 3.2, fill='ink')

def gauge(c):
    c.arc(50, 64, 34, 180, 360, 'line', 5); c.arc(50, 64, 34, 180, 245, 'orange', 5); c.arc(50, 64, 34, 245, 300, 'soft', 5); c.arc(50, 64, 34, 300, 360, 'teal', 5)
    c.line([(50, 64), (34, 40)], 'ink', 2.0); c.circ(50, 64, 4.6, fill='ink')
    c.rect(30, 76, 40, 12, fill='white', outline='ink', r=3, wd=0.9); c.text(50, 82, 'minutes per result', 4.0, 'ink', 'mm')

def sources(c):
    doc(c, 8, 18, 28, 38, lines=3); doc(c, 36, 8, 28, 38, lines=3, accent=1); doc(c, 64, 18, 28, 38, lines=3)
    c.line([(22, 58), (22, 70)], 'teal', 1.2); c.line([(50, 48), (50, 70)], 'teal', 1.2); c.line([(78, 58), (78, 70)], 'teal', 1.2); c.line([(22, 70), (78, 70)], 'teal', 1.2)
    c.rect(30, 74, 40, 16, fill='orange', r=3); c.text(50, 82, 'register', 6, 'white', 'mm')

def sidebyside(c):
    c.rect(8, 22, 38, 52, fill='white', outline='ink', r=3); c.rect(54, 22, 38, 52, fill='pale', outline='ink', r=3)
    for i in range(4): c.line([(14, 34 + i * 9), (40, 34 + i * 9)], 'line', 1.4)
    for i in range(4): c.line([(60, 34 + i * 9), (86 - (10 if i == 2 else 0), 34 + i * 9)], 'orange' if i == 2 else 'line', 1.4)
    check(c, 27, 80, 6); xmark(c, 73, 80, 6)

def people_ai(c):
    person(c, 28, 34, 1.4, 'teal'); c.rect(54, 26, 34, 34, fill='pale', outline='ink', r=6, wd=1.2)
    c.circ(65, 40, 3, fill='ink'); c.circ(77, 40, 3, fill='ink'); c.line([(64, 51), (78, 51)], 'ink', 1.2)
    c.arrow(40, 72, 70, 72, 'teal', 1.2, 3); c.arrow(70, 84, 40, 84, 'orange', 1.2, 3)

def folder_lock(c):
    c.poly([(10, 30), (10, 82), (90, 82), (90, 36), (46, 36), (40, 28), (14, 28)], fill='pale', outline='ink', wd=1.3)
    c.rect(38, 50, 24, 22, fill='teal', outline='ink', r=3); c.arc(50, 50, 8, 180, 360, 'ink', 1.8); c.circ(50, 61, 2.6, fill='white')

def calendar(c):
    c.rect(14, 18, 72, 66, fill='white', outline='ink', r=5, wd=1.3); c.rect(14, 18, 72, 16, fill='orange', outline='ink', r=5, wd=1.3)
    for i in range(3): c.circ(32 + i * 18, 14, 3, fill='ink')
    for r_ in range(3):
        for k in range(5):
            col = 'teal' if (r_, k) == (1, 2) else 'pale'
            c.rect(20 + k * 12.4, 40 + r_ * 14, 9.4, 10, fill=col, r=1.5)

MOTIFS = {k: v for k, v in dict(
    parties=parties, docstack=docstack, magnifier=magnifier, cogs=cogs, network=network, tokens=tokens, vecmap=vecmap, cycle=cycle,
    scales=scales, shield=shield, deskperson=deskperson, funnel=funnel, database=database, scanpage=scanpage, bars=bars, ledger=ledger,
    agent=agent, flow=flow, stopgate=stopgate, envelope=envelope, timeline=timeline, team=team, hourglass=hourglass, stairs=stairs,
    books=books, warn=warn, clipboard=clipboard, cloud=cloud, chat=chat, bulb=bulb, tree=tree, puzzle=puzzle, key=key, gap=gap, dice=dice,
    window=window, stamp=stamp, rewind=rewind, laptop=laptop, target=target, signpost=signpost, question=question, compass=compass,
    gauge=gauge, sources=sources, sidebyside=sidebyside, people_ai=people_ai, folder_lock=folder_lock, calendar=calendar).items()}

ALT = dict(
    parties='Two company buildings, Victoria and Equator, with a contract between them', docstack='A stack of agreement versions with a version seal',
    magnifier='A magnifying glass over one line of a contract', cogs='Two cogs and a completed check', network='Layers of connected nodes in a neural network',
    tokens='Words converted into numbered tokens', vecmap='Points on a map with a query point and its near neighbours', cycle='A four-step loop that repeats',
    scales='Scales of justice', shield='A shield with a padlock', deskperson='A reviewer at a desk checking a document', funnel='A funnel filtering documents',
    database='A collection of records and a matter folder', scanpage='A scanned page with garbled text', bars='A bar chart with a downward step',
    ledger='A ledger sheet and a calculator', agent='A small software agent with a tool', flow='A workflow with a review gate', stopgate='A barrier gate and a warning sign',
    envelope='An envelope with a warning', timeline='A timeline marked at days 0, 30, 60 and 90', team='Three people forming a team', hourglass='An hourglass and coins',
    stairs='Steps leading to a flag', books='A stack of books with a bookmark', warn='A document with a warning triangle', clipboard='A clipboard checklist',
    cloud='A cloud service and a server', chat='Two speech bubbles, a question and an answer', bulb='A light bulb', tree='A decision tree with three branches',
    puzzle='Two puzzle pieces joining words and meaning', key='A key and a document', gap='A document with a missing piece and a question mark', dice='Dice showing chance',
    window='A context window holding instructions, evidence, conversation and answer', stamp='A stamp marking approval', rewind='A clock with a rewind arrow',
    laptop='A laptop with a checklist', target='A target with an arrow', signpost='A signpost with go and stop', question='A speech bubble with a question mark',
    compass='A compass', gauge='A gauge with minutes per result', sources='Three sources feeding a register', sidebyside='Two texts side by side, one correct and one flawed',
    people_ai='A person and an AI system exchanging requests', folder_lock='A locked folder', calendar='A calendar')


def render(name, theme, path):
    c = C(theme); MOTIFS[name](c); c.save(path)


def hero(path, names):
    """A dark-theme scene for the title slide: up to three motifs on one canvas."""
    big = Image.new('RGBA', (PX, PX), (0, 0, 0, 0))
    spots = {1: [(0.0, 0.0, 1.0)], 2: [(0.0, 0.18, 0.62), (0.38, -0.02, 0.62)], 3: [(0.0, 0.28, 0.52), (0.46, 0.34, 0.52), (0.22, -0.04, 0.6)]}[len(names)]
    for n, (x, y, s) in zip(names, spots):
        c = C(DARK); MOTIFS[n](c); im = c.im.resize((PX, PX), Image.LANCZOS)
        im = im.resize((int(PX * s), int(PX * s)), Image.LANCZOS); big.alpha_composite(im, (int(PX * x), int(PX * y)))
    big.save(path)


if __name__ == '__main__':
    out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    for n in MOTIFS: render(n, LIGHT, out / f'{n}.png')
    print(len(MOTIFS), 'motifs written to', out)
