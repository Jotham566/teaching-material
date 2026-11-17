"""Figures for Leadership Edition Session 1, AI that sees and reads: images, documents and speech.  Names: x_l01_*  (content kind 'l01_*').

No maths: pictures, counts and percentages only.  The digit pictures and every demonstration number are read from the recorded run in
demo_runs/s01/ (digits_run.py; scikit-learn 1.9.1; 5 November 2026; results_s01.npz and results_s01.json).  Case figures come from
research/*.md (IDs in the content file).  Leaves, forms, sound pictures and the Nile Valley Foods entry are drawn to teach the idea and are
labelled as illustrations; Nile Valley Foods is fictional.
"""
import numpy as np
from matplotlib.patches import Ellipse

from figkit import Scene, INK, BODY, MUTE, GREY, HAIR, PALE, PAPER, RED, GOLD, fig
import slidekit as K
from diagrams_l02 import _wrap, _fit, _lh, _source
from diagrams_t01 import _res as _r01, _gray


# ------------------------------------------------------------------ small drawing helpers
def _leaf(s, x, y, size, kind='healthy', angle=35):
    """A stylised leaf centred at (x, y), about `size` inches long. kind: healthy, spots, edges."""
    s.ax.add_patch(Ellipse((x, y), size * 0.48, size, angle=angle, fc=PAPER, ec=INK, lw=2, zorder=3))
    import math
    a = math.radians(angle + 90)
    dx, dy = math.cos(a) * size * 0.42, math.sin(a) * size * 0.42
    s.line(x - dx, y - dy, x + dx * 1.25, y + dy * 1.25, color=INK, lw=1.4, z=4)
    if kind == 'spots':
        for fx, fy, r in ((-0.08, 0.12, 0.07), (0.07, -0.05, 0.06), (-0.03, -0.2, 0.05), (0.1, 0.2, 0.045)):
            s.circle(x + fx * size, y + fy * size, r * size, fill=RED, edge=INK, lw=0.8, z=5)
    elif kind == 'edges':
        s.ax.add_patch(Ellipse((x, y), size * 0.48, size, angle=angle, fc='none', ec=GOLD, lw=6, zorder=4))
        s.ax.add_patch(Ellipse((x, y), size * 0.48, size, angle=angle, fc='none', ec=INK, lw=1.4, zorder=5))


def _tag(s, x, y, text, gold=False, w=None, size=14):
    w = w or K.width_in(text, size, 'bold') + 0.3
    s.box(x - w / 2, y - 0.19, w, 0.38, text, size=size, weight='bold', fill=GOLD if gold else PAPER, r=0.06)
    return w


def _form(s, x, y, w, h, rows, title='Delivery form'):
    """A paper form with handwritten-looking entries. rows: (label, value)."""
    s.box(x, y, w, h, '', fill=PAPER, lw=1.8, r=0.04)
    s.text(x + 0.15, y + h - 0.25, title, size=15, weight='bold', ha='left')
    rh = (h - 0.55) / len(rows)
    for i, (lab, val) in enumerate(rows):
        yy = y + h - 0.6 - (i + 0.5) * rh
        s.text(x + 0.15, yy, lab, size=14, ha='left', color=BODY)
        s.text(x + w - 0.15, yy, val, size=16, ha='right', italic=True, color=INK)
        s.line(x + w * 0.45, yy - 0.17, x + w - 0.1, yy - 0.17, color=GREY, lw=1.0, z=3)


def _tiles(s, w, h, tiles, src, top_pad=0.0):
    """Six industry tiles: (icon, industry, use, example)."""
    gap = 0.12
    tw = (w - 0.2 - 2 * gap) / 3
    th = (h - 0.5 - gap - top_pad) / 2
    for i, (ic, ind, use, ex) in enumerate(tiles):
        x = 0.1 + (i % 3) * (tw + gap)
        y = 0.45 + (1 - i // 3) * (th + gap)
        s.box(x, y, tw, th, '', fill=PAPER, lw=1.8, r=0.08)
        s.icon(ic, x + 0.5, y + th - 0.55, 0.75)
        tx, iw, top = x + 1.0, tw - 1.15, y + th - 0.15
        hh = _wrap(s, tx, top, iw, ind, 16, weight='bold', ha='left', va='top')
        top -= hh + 0.1
        uh = _wrap(s, tx, top, iw, use, 15, ha='left', va='top', color=BODY)
        top -= uh + 0.08
        _wrap(s, tx, top, iw, ex, 15, weight='bold', ha='left', va='top', color=MUTE if ex.startswith(('No named', 'No published', 'Typical use')) else RED)
    _source(s, src, y=0.16)


def people_grid(s, w, h, roles, labels=('Less of', 'More of', 'Skill to grow', 'Fears and gains')):
    """Three roles by four rows: what shrinks, what grows, the skill, fears and gains."""
    lab_w = 1.45
    cw = (w - 0.1 - lab_w) / len(roles)
    top = h - 0.85
    rh = (top - 0.1) / len(labels)
    for i, (role, cells) in enumerate(roles):
        x = 0.1 + lab_w + i * cw
        s.icon('person', x + 0.45, h - 0.42, 0.62, accent=GOLD)
        _wrap(s, x + 0.85, h - 0.42, cw - 0.95, role, 17, weight='bold', ha='left')
        for r, txt in enumerate(cells):
            y = top - r * rh
            s.rect(x + 0.05, y - rh + 0.05, cw - 0.1, rh - 0.08, fill=PALE if r == len(labels) - 1 else PAPER, edge=HAIR, lw=1.0, z=1)
            _wrap(s, x + 0.2, y - rh / 2 + 0.02, cw - 0.4, txt, 15, ha='left', color=BODY)
    for r, lab in enumerate(labels):
        y = top - r * rh - rh / 2
        _wrap(s, 0.1, y, lab_w - 0.1, lab, 15, weight='bold', ha='left', color=RED if r == len(labels) - 1 else INK)


def portfolio_entry(s, w, h, rows, head='Nile Valley Foods (fictional): one entry', size=14, gold_last=1):
    s.text(0.05, h - 0.2, head, size=15, weight='bold', ha='left')
    lw_ = 1.85
    vw = w - 0.1 - lw_
    hs = []
    for a, b in rows:
        n = max(len(K.wrap(a, size, 'bold', lw_ - 0.15)), len(K.wrap(b, size, 'regular', vw - 0.15)))
        hs.append(n * _lh(size) + 0.1)
    y = h - 0.42
    for i, ((a, b), rh) in enumerate(zip(rows, hs)):
        gold = i >= len(rows) - gold_last
        s.rect(0.05, y - rh, lw_, rh, fill=GOLD if gold else PALE, edge=INK, lw=1.0)
        s.rect(0.05 + lw_, y - rh, vw, rh, fill=PAPER, edge=INK, lw=1.0)
        _wrap(s, 0.12, y - rh / 2, lw_ - 0.15, a, size, weight='bold', ha='left')
        _wrap(s, 0.12 + lw_, y - rh / 2, vw - 0.15, b, size, ha='left', color=BODY)
        y -= rh


# ------------------------------------------------------------------ bridge: Session 0 to today
@fig('x_l01_bridge')
def x_l01_bridge(w, h, **_):
    s = Scene(w, h)
    pw = 3.65
    # left: Session 0
    x0 = 0.1
    s.text(x0 + 0.05, h - 0.3, 'Session 0: past files', size=18, weight='bold', ha='left')
    s.line(x0, h - 0.55, x0 + pw, h - 0.55, lw=1.6)
    for i, (txt, lab) in enumerate((('Loan file, paid on time', 'repaid'), ('Loan file, 3 late payments', 'not repaid'), ('Loan file, new business', 'repaid'))):
        y = h - 1.05 - i * 0.68
        s.icon('folder', x0 + 0.28, y, 0.45)
        _wrap(s, x0 + 0.62, y, 1.65, txt, 14, ha='left', color=BODY)
        s.box(x0 + 2.35, y - 0.2, 1.28, 0.4, lab, size=14, fill=GOLD if lab == 'not repaid' else PAPER, weight='bold', r=0.06)
    # right: today
    x1 = 3.95
    s.text(x1 + 0.05, h - 0.3, 'Today: pictures, pages, voices', size=18, weight='bold', ha='left')
    s.line(x1, h - 0.55, x1 + pw, h - 0.55, lw=1.6)
    for i, (ic, txt, lab) in enumerate((('plant', 'Photo of a leaf', 'diseased'), ('doc', 'Scanned form', 'its words'), ('speech', 'Recorded speech', 'its words'))):
        y = h - 1.05 - i * 0.68
        if ic == 'plant':
            _leaf(s, x1 + 0.28, y, 0.5, 'spots')
        else:
            s.icon(ic, x1 + 0.28, y, 0.45)
        _wrap(s, x1 + 0.62, y, 1.65, txt, 14, ha='left', color=BODY)
        s.box(x1 + 2.35, y - 0.2, 1.28, 0.4, lab, size=14, fill=GOLD if lab == 'diseased' else PAPER, weight='bold', r=0.06)
    for x, out in ((x0, 'Learns who is likely to repay'), (x1, 'Learns to see, read and hear')):
        s.arrow(x + pw / 2, h - 2.75, x + pw / 2, h - 3.15, lw=2.2)
        s.icon('robot', x + 0.45, h - 3.62, 0.62)
        s.box(x + 0.85, h - 3.98, pw - 0.85, 0.72, '', fill=PAPER, lw=1.8, r=0.08)
        _wrap(s, x + 0.85 + (pw - 0.85) / 2, h - 3.62, pw - 1.05, out, 15, weight='bold')
    return s


# ------------------------------------------------------------------ hook: Makerere cassava app (AGR-02)
@fig('x_l01_makerere')
def x_l01_makerere(w, h, **_):
    s = Scene(w, h)
    s.text(0.1, h - 0.28, 'Makerere University AI Lab, Uganda: cassava diagnosis on a phone', size=17, weight='bold', ha='left')
    y = h - 1.6
    # phone with a leaf
    s.box(0.45, y - 0.8, 0.95, 1.6, '', fill=PAPER, lw=2.2, r=0.12)
    _leaf(s, 0.925, y + 0.05, 0.9, 'spots')
    s.text(0.925, y - 1.03, 'A photo of the plant', size=14, color=BODY)
    s.arrow(1.55, y, 2.15, y, lw=2.2, head=15)
    s.icon('robot', 2.6, y + 0.05, 0.75)
    s.text(2.6, y - 0.75, 'The app', size=14, color=BODY)
    s.arrow(3.05, y, 3.6, y, lw=2.2, head=15)
    s.box(3.7, y - 0.65, 3.9, 1.3, '', fill=GOLD, lw=1.8, r=0.08)
    _wrap(s, 3.7 + 1.95, y + 0.22, 3.6, 'Healthy, or one of the main cassava diseases', 15, weight='bold')
    _wrap(s, 3.7 + 1.95, y - 0.33, 3.6, 'with an estimate of how severe', 15)
    for i, (big, txt) in enumerate((('About 400', 'downloads of the team’s published model'),
                                    ('6 weeks earlier', 'leaf light readings spotted disease, before photos could'))):
        x = 0.1 + i * 3.8
        s.box(x, 0.55, 3.6, 1.25, '', fill=PAPER, lw=1.6, r=0.08)
        s.text(x + 0.2, 1.47, big, size=22, weight='bold', ha='left', color=RED)
        _wrap(s, x + 0.2, 0.92, 3.25, txt, 14, ha='left', color=BODY)
    _source(s, 'Source: AIhub interview, 16 Mar 2023. A research project; no farm result published.')
    return s


# ------------------------------------------------------------------ a photo is a grid of dots, each a number (recorded image 918)
@fig('x_l01_dots')
def x_l01_dots(w, h, **_):
    r = _r01()
    img = r['images'][int(r['img_i'])]
    s = Scene(w, h)
    _gray(s, img, 0.35, 1.25, 2.3)
    s.text(1.5, 1.25 + 2.3 + 0.3, 'What you see', size=17, weight='bold')
    s.text(1.5, 0.95, 'A handwritten 3', size=15, color=BODY)
    s.arrow(2.85, 2.4, 3.4, 2.4, lw=2.2)
    c = 0.48
    gx, gy = 3.55, 0.55
    for i in range(8):
        for j in range(8):
            v = int(img[i, j])
            shade = 1 - 0.9 * v / 16.0
            s.rect(gx + j * c, gy + (7 - i) * c, c, c, fill=(shade, shade, shade), edge=HAIR, lw=0.8, z=2)
            s.text(gx + j * c + c / 2, gy + (7 - i) * c + c / 2, str(v), size=14, color=PAPER if v >= 8 else INK, weight='bold' if v >= 8 else 'normal', z=5)
    s.rect(gx, gy, 8 * c, 8 * c, fill='none', edge=INK, lw=2, z=4)
    s.text(gx + 4 * c, gy + 8 * c + 0.28, 'What the computer gets: 64 numbers', size=17, weight='bold')
    s.text(0.1, 0.2, '0 is blank paper, 16 is full ink. From the recorded run, 5 November 2026.', size=14, color=MUTE, ha='left')
    return s


# ------------------------------------------------------------------ it learns from labelled photos
@fig('x_l01_labelled')
def x_l01_labelled(w, h, **_):
    s = Scene(w, h)
    s.text(0.1, h - 0.3, 'Thousands of photos, each labelled by an expert', size=16, weight='bold', ha='left')
    kinds = ['spots', 'healthy', 'edges', 'healthy', 'spots', 'healthy']
    labs = ['diseased', 'healthy', 'diseased', 'healthy', 'diseased', 'healthy']
    cw = (w - 0.2) / 6
    for i, (k, lab) in enumerate(zip(kinds, labs)):
        cx = 0.1 + cw * (i + 0.5)
        _leaf(s, cx, h - 1.3, 0.85, k, angle=25 + (i % 3) * 15)
        _tag(s, cx, h - 2.05, lab, gold=lab == 'diseased', w=cw - 0.12)
    s.arrow(w / 2, h - 2.35, w / 2, h - 2.75, lw=2.2)
    s.icon('robot', 0.75, 1.05, 0.8)
    s.box(1.3, 0.6, 2.9, 0.95, '', fill=PAPER, lw=1.8, r=0.08)
    _wrap(s, 2.75, 1.07, 2.7, 'Learns which signs go with disease', 15, weight='bold')
    s.arrow(4.3, 1.07, 4.75, 1.07, lw=2.2)
    _leaf(s, 5.15, 1.07, 0.75, 'spots', angle=50)
    s.text(5.15, 0.45, 'a new photo', size=14, color=BODY)
    s.arrow(5.55, 1.07, 5.95, 1.07, lw=2.2)
    s.box(6.0, 0.62, 1.6, 0.9, '', fill=GOLD, lw=1.8, r=0.08)
    _wrap(s, 6.8, 1.07, 1.45, 'diseased, 9 in 10 likely', 15, weight='bold')
    s.text(w - 0.1, 0.15, 'Illustration', size=14, color=MUTE, ha='right')
    return s


# ------------------------------------------------------------------ layers: dots, marks, shapes, answer
@fig('x_l01_layers')
def x_l01_layers(w, h, **_):
    s = Scene(w, h)
    cw = (w - 0.2) / 4
    heads = [('The photo', 'millions of dots'), ('First layer', 'edges and specks'), ('Next layer', 'spots, patches, a leaf edge'), ('Last layer', 'the answer')]
    cy = h - 2.0
    for i, (hd, sub) in enumerate(heads):
        cx = 0.1 + cw * (i + 0.5)
        s.text(cx, h - 0.35, hd, size=17, weight='bold', color=RED if i == 3 else INK)
        _wrap(s, cx, h - 0.75, cw - 0.2, sub, 15, color=BODY)
        if i == 0:
            g = 0.16
            for a in range(8):
                for b in range(8):
                    v = ((a * 3 + b * 5) % 7) / 7
                    shade = 0.35 + 0.6 * v
                    s.rect(cx - 4 * g + b * g, cy - 4 * g + a * g, g, g, fill=(shade, shade, shade), edge=HAIR, lw=0.4)
        elif i == 1:
            for k, (dx, dy, ang) in enumerate(((-0.45, 0.4, 30), (0.3, 0.45, -40), (-0.35, -0.35, 80), (0.4, -0.3, 10))):
                import math
                a = math.radians(ang)
                s.line(cx + dx - 0.22 * math.cos(a), cy + dy - 0.22 * math.sin(a), cx + dx + 0.22 * math.cos(a), cy + dy + 0.22 * math.sin(a), lw=3)
            s.circle(cx, cy, 0.08, fill=RED, edge=INK, lw=0.8)
        elif i == 2:
            for dx, dy in ((-0.3, 0.3), (0.25, 0.1), (-0.05, -0.35)):
                s.circle(cx + dx, cy + dy, 0.14, fill=RED, edge=INK, lw=1)
            s.ax.add_patch(Ellipse((cx + 0.1, cy), 0.7, 1.3, angle=30, fc='none', ec=INK, lw=2, ls='--', zorder=3))
        else:
            s.box(cx - 0.75, cy - 0.35, 1.5, 0.7, 'diseased', size=17, weight='bold', fill=GOLD, r=0.08)
        if i < 3:
            s.arrow(cx + cw / 2 - 0.25, cy, cx + cw / 2 + 0.25, cy, lw=2.2)
    s.box(0.3, 0.45, w - 0.6, 0.9, '', fill=PAPER, lw=1.6, r=0.08)
    _wrap(s, w / 2, 0.9, w - 1.0, 'Nobody writes these steps. The network finds them from the labelled photos.', 16, weight='bold')
    return s


# ------------------------------------------------------------------ reading documents: letters are pictures too (OCR)
@fig('x_l01_documents')
def x_l01_documents(w, h, **_):
    s = Scene(w, h)
    _form(s, 0.1, 1.0, 2.6, h - 1.4, [('Farmer', 'A. Nakato'), ('Bags', '12'), ('Date', '3 / 5'), ('Signed', 'A.N.')])
    s.text(1.4, 0.65, 'A scanned paper form', size=14, color=BODY)
    s.arrow(2.85, h / 2 + 0.2, 3.35, h / 2 + 0.2, lw=2.2)
    # one letter as dots
    g = 0.17
    pat = ['..##..', '.#..#.', '....#.', '...#..', '..#...', '.####.']
    x0, y0 = 3.5, h / 2 - 0.3
    for a, row in enumerate(pat):
        for b, ch in enumerate(row):
            s.rect(x0 + b * g, y0 + (5 - a) * g, g, g, fill=INK if ch == '#' else PAPER, edge=HAIR, lw=0.5)
    s.text(x0 + 3 * g, y0 + 6 * g + 0.5, 'Each letter is', size=14, color=BODY)
    s.text(x0 + 3 * g, y0 + 6 * g + 0.22, 'a small picture', size=14, color=BODY)
    s.text(x0 + 3 * g, y0 - 0.3, 'read as “2”', size=15, weight='bold')
    s.arrow(4.65, h / 2 + 0.2, 5.1, h / 2 + 0.2, lw=2.2)
    rows = [('Farmer', 'A. Nakato', False), ('Bags', '12', False), ('Date', '3 May', False), ('Signed', 'unclear', True)]
    tx, tw, rh = 5.2, 2.4, 0.5
    top = h / 2 + 1.2
    s.text(tx + tw / 2, top + 0.3, 'A row in a table', size=15, weight='bold')
    for i, (a, b, flag) in enumerate(rows):
        y = top - (i + 1) * rh
        s.rect(tx, y, 1.0, rh, fill=PALE, edge=INK, lw=1.0)
        s.rect(tx + 1.0, y, tw - 1.0, rh, fill=GOLD if flag else PAPER, edge=INK, lw=1.0)
        s.text(tx + 0.08, y + rh / 2, a, size=14, weight='bold', ha='left')
        s.text(tx + 1.08, y + rh / 2, b, size=14, ha='left')
    _wrap(s, tx + tw / 2, top - 4 * rh - 0.45, tw + 0.2, 'Gold: not sure, so a person checks', 14, weight='bold', color=RED)
    s.text(w - 0.1, 0.15, 'Illustration', size=14, color=MUTE, ha='right')
    return s


# ------------------------------------------------------------------ speech to text: sound becomes a picture
@fig('x_l01_speech')
def x_l01_speech(w, h, **_):
    s = Scene(w, h)
    import math
    cy = h - 1.6
    s.icon('speech', 0.55, cy, 0.8)
    xs = np.linspace(1.15, 2.95, 160)
    ys = [cy + 0.55 * math.sin(i * 0.9) * (0.35 + 0.65 * abs(math.sin(i * 0.07))) for i in range(160)]
    s.ax.plot(xs, ys, color=INK, lw=1.4, zorder=3)
    s.text(2.05, cy - 0.95, 'The sound wave', size=14, color=BODY)
    s.arrow(3.1, cy, 3.55, cy, lw=2.2)
    g = 0.14
    for a in range(9):
        for b in range(14):
            v = (math.sin(b * 0.8 + a * 0.5) + 1) / 2 * (1 - a / 12)
            shade = 1 - 0.85 * v
            s.rect(3.65 + b * g, cy - 0.63 + a * g, g, g, fill=(shade, shade, shade), edge='none', lw=0)
    s.rect(3.65, cy - 0.63, 14 * g, 9 * g, fill='none', edge=INK, lw=1.4, z=3)
    s.text(3.65 + 7 * g, cy - 0.95, 'A picture of the sound', size=14, color=BODY)
    s.arrow(5.7, cy, 6.1, cy, lw=2.2)
    s.box(6.15, cy - 0.55, 1.45, 1.1, '', fill=GOLD, lw=1.8, r=0.08)
    _wrap(s, 6.875, cy, 1.3, '“The case is adjourned”', 15, weight='bold')
    s.box(0.3, 0.45, w - 0.6, 1.25, '', fill=PAPER, lw=1.6, r=0.08)
    _wrap(s, w / 2, 1.3, w - 1.0, 'It learned from many hours of recordings with typed transcripts.', 16, weight='bold')
    _wrap(s, w / 2, 0.82, w - 1.0, 'Fewer recordings in a language, such as Luganda, means weaker results.', 15, color=BODY)
    s.text(w - 0.1, 0.15, 'Illustration', size=14, color=MUTE, ha='right')
    return s


# ------------------------------------------------------------------ one idea, three inputs
@fig('x_l01_one_idea')
def x_l01_one_idea(w, h, **_):
    s = Scene(w, h)
    cols = [(0.1, 2.6, 'It is given'), (3.2, 5.0, 'It learned from'), (8.7, 3.1, 'It gives back')]
    for x, cw, hd in cols:
        s.text(x + 0.1, h - 0.3, hd, size=18, weight='bold', ha='left', color=INK)
        s.line(x, h - 0.55, x + cw, h - 0.55, lw=1.6)
    rows = [('plant', 'A photo of a leaf', 'Thousands of photos labelled healthy or diseased', 'A label: diseased'),
            ('doc', 'A scanned page', 'Thousands of pages with the right words typed out', 'The words, ready for a table'),
            ('speech', 'A recording', 'Many hours of speech with typed transcripts', 'A transcript')]
    rh = (h - 1.2) / 3
    for i, (ic, a, b, c) in enumerate(rows):
        y = h - 0.75 - (i + 0.5) * rh
        if ic == 'plant':
            _leaf(s, 0.45, y, 0.7, 'spots')
        else:
            s.icon(ic, 0.45, y, 0.65)
        _wrap(s, 0.9, y, 1.8, a, 16, ha='left')
        s.arrow(2.75, y, 3.1, y, lw=2)
        s.box(3.2, y - rh / 2 + 0.12, 5.0, rh - 0.24, '', fill=PAPER, lw=1.6, r=0.08)
        _wrap(s, 3.35, y, 4.7, b, 16, ha='left', color=BODY)
        s.arrow(8.3, y, 8.65, y, lw=2)
        s.box(8.7, y - rh / 2 + 0.12, 3.1, rh - 0.24, '', fill=PAPER, lw=1.6, r=0.08)
        _wrap(s, 8.85, y, 2.8, c, 16, weight='bold', ha='left')
    return s


# ------------------------------------------------------------------ good at, struggles when
@fig('x_l01_good_bad')
def x_l01_good_bad(w, h, **_):
    s = Scene(w, h)
    cols = [('Good at', 'check', ['Thousands of images or pages a day, with the same care', 'Turning paper and speech into data', 'Working on a phone, where experts are few', 'Sorting the clear cases from the doubtful']),
            ('Struggles when', 'cross', ['A new picture differs: camera, light, angle', 'It meets something it never saw', 'Images are blurred, dark or smudged', 'Accents and languages with few recordings'])]
    cw = (w - 0.3) / 2
    for i, (hd, ic, items) in enumerate(cols):
        x = 0.1 + i * (cw + 0.1)
        s.text(x + 0.1, h - 0.35, hd, size=20, weight='bold', ha='left', color=RED if i else INK)
        s.line(x, h - 0.65, x + cw, h - 0.65, lw=1.8)
        for k, it in enumerate(items):
            y = h - 1.25 - k * 0.98
            s.icon(ic, x + 0.35, y, 0.6)
            _wrap(s, x + 0.8, y, cw - 0.95, it, 16, ha='left', color=BODY)
    return s


# ------------------------------------------------------------------ lab versus clinic: Google Health, Thailand (HLT-09)
@fig('x_l01_thailand')
def x_l01_thailand(w, h, **_):
    s = Scene(w, h)
    cw = (w - 0.3) / 2
    # lab
    x = 0.1
    s.box(x, 1.0, cw, h - 1.1, '', fill=PAPER, lw=1.8, r=0.08)
    s.text(x + 0.2, h - 0.4, 'In Google’s own tests', size=19, weight='bold', ha='left')
    s.text(x + cw / 2, h - 1.35, '90%', size=44, weight='bold')
    _wrap(s, x + cw / 2, h - 2.15, cw - 0.4, 'accuracy reported from internal tests', 15, color=BODY)
    s.icon('check', x + cw / 2, 1.55, 0.7)
    # clinic
    x = 0.2 + cw
    s.box(x, 1.0, cw, h - 1.1, '', fill=PAPER, edge=RED, lw=2.2, r=0.08)
    s.text(x + 0.2, h - 0.4, 'In 11 clinics', size=19, weight='bold', ha='left', color=RED)
    items = [('Blurred or dark photos were turned away', 'cross'), ('Uploads took 60 to 90 seconds on slow internet', 'clock'), ('Some nurses discouraged patients from joining', 'person')]
    for k, (t, ic) in enumerate(items):
        y = h - 1.15 - k * 0.85
        s.icon(ic, x + 0.45, y, 0.5)
        _wrap(s, x + 0.85, y, cw - 1.0, t, 15, ha='left', color=BODY)
    _source(s, 'Sources: TechCrunch, 27 Apr 2020; Google study, CHI 2020. An early field study.', y=0.18)
    return s


# ------------------------------------------------------------------ a good system says "not sure" (AGR-02, recall of AGR-01)
@fig('x_l01_unsure')
def x_l01_unsure(w, h, **_):
    s = Scene(w, h)
    s.text(0.1, h - 0.3, 'Makerere’s cassava app, pointed at things that were not plants', size=15, weight='bold', ha='left')
    rows = [('Early version', 'A confident wrong answer', False), ('Rebuilt version', '“Undetermined”: a person looks', True)]
    for i, (who, ans, good) in enumerate(rows):
        y = h - 1.15 - i * 1.15
        s.icon('bottle', 0.45, y, 0.6)
        s.arrow(0.85, y, 1.3, y, lw=2)
        s.icon('robot', 1.65, y, 0.55)
        s.text(1.65, y - 0.48, who, size=14, color=BODY)
        s.arrow(2.05, y, 2.5, y, lw=2)
        s.box(2.6, y - 0.32, 3.9, 0.64, '', fill=GOLD if good else PAPER, edge=INK if good else RED, lw=2, r=0.08)
        _wrap(s, 2.75, y, 3.6, ans, 15, weight='bold', ha='left', color=INK if good else RED)
        s.icon('check' if good else 'cross', 7.0, y, 0.55)
    s.line(0.1, 1.65, w - 0.1, 1.65, color=HAIR, lw=1.2)
    s.text(0.1, 1.35, 'Recall Session 0: PlantVillage Nuru', size=15, weight='bold', ha='left')
    _wrap(s, 0.1, 0.92, w - 0.2, '74 to 88 in 100 right when it looked at six leaves of a plant; 49 in 100 on a single leaf.', 15, ha='left', color=BODY)
    _source(s, 'Sources: AIhub, 16 Mar 2023; Mrisho et al., Frontiers in Plant Science, 18 Dec 2020.', y=0.2)
    return s


# ------------------------------------------------------------------ industry tour
@fig('x_l01_six')
def x_l01_six(w, h, **_):
    s = Scene(w, h)
    tiles = [('calculator', 'Banking and microfinance', 'Reads ID cards and loan forms into the system', 'Typical use; no published case yet'),
             ('phone', 'Telecom and mobile money', 'Speech models for Wolof and Pulaar', 'Orange, West Africa (plans)'),
             ('plant', 'Agriculture and agribusiness', 'Names a crop pest from a phone photo', 'Farmers Companion App, Mbale'),
             ('bottle', 'Manufacturing and FMCG', 'Scores shelves from sales reps’ photos', 'Coca-Cola HBC: 60 to 70% of visits'),
             ('clinic', 'Healthcare and insurance', 'Spots malaria parasites in a blood photo', 'Makerere AI Health Lab, Uganda (testing)'),
             ('people', 'Public sector', 'Transcribes court hearings', 'Judiciary of Uganda: 70 licences')]
    _tiles(s, w, h, tiles, 'Sources: Capacity 2024; Google 2019; Just Drinks 2023; Makerere CoCIS 2025; The Observer 2026. Company and lab figures.')
    return s


# ------------------------------------------------------------------ live receipt demonstration, with its fallback drawn on the slide
@fig('x_l01_receipt')
def x_l01_receipt(w, h, **_):
    s = Scene(w, h)
    steps = [('phone', 'Photo', 'a printed receipt'), ('robot', 'Assistant', 'an approved tool'), ('grid', 'Table', 'date, items, total'), ('check', 'Check', 'each field by hand')]
    gap = 0.3
    bw = (w - 0.2 - 3 * gap) / 4
    top, bh = h - 0.1, 1.95
    for i, (ic, head, txt) in enumerate(steps):
        x = 0.1 + i * (bw + gap)
        s.box(x, top - bh, bw, bh, '', fill=PAPER, lw=1.8, r=0.08)
        s.icon(ic, x + bw / 2, top - 0.5, 0.6)
        s.text(x + bw / 2, top - 1.1, head, size=17, weight='bold')
        _wrap(s, x + bw / 2, top - 1.6, bw - 0.2, txt, 15, color=BODY)
        if i < 3:
            s.arrow(x + bw + 0.03, top - bh / 2, x + bw + gap - 0.03, top - bh / 2, lw=2.0, head=12)
    fy = 0.1
    fh = top - bh - 0.3 - fy
    s.box(0.1, fy, w - 0.2, fh, '', fill=PAPER, edge=RED, lw=2.2, r=0.08)
    s.text(0.3, fy + fh - 0.3, 'If it fails: the fallback', size=16, weight='bold', color=RED, ha='left')
    _wrap(s, 0.3, fy + fh - 0.62, w - 0.6, 'No connection, no approved tool, or a refusal: we fill the table by hand from the receipt. No recording exists.', 15, ha='left', va='top', color=BODY)
    return s


# ------------------------------------------------------------------ demonstration: real predictions on unseen digits (recorded)
@fig('x_l01_gallery')
def x_l01_gallery(w, h, **_):
    r = _r01()
    xte, yte, pred = r['xte'], r['yte'], r['pred']
    wrong = [i for i in range(len(yte)) if pred[i] != yte[i]]
    idx = list(range(8)) + wrong[:4]
    s = Scene(w, h)
    gw = 7.6
    cols = 6
    cw = gw / cols
    isz = 1.0
    for n, i in enumerate(idx):
        row, col = divmod(n, cols)
        cx = 0.1 + col * cw + cw / 2
        top = h - 0.1 - row * 1.85
        ok = pred[i] == yte[i]
        _gray(s, xte[i].reshape(8, 8), cx - isz / 2, top - isz, isz, frame=False)
        s.rect(cx - isz / 2, top - isz, isz, isz, fill='none', edge=INK if ok else RED, lw=2 if ok else 4, z=4)
        s.text(cx, top - isz - 0.25, f'said {pred[i]}', size=15, weight='bold' if not ok else 'normal', color=INK if ok else RED)
        s.text(cx, top - isz - 0.55, f'was {yte[i]}', size=14, color=BODY if ok else RED)
    s.text(0.1, 0.25, 'Top: the first 8 unseen digits. Bottom: 4 of its 14 mistakes, in red.', size=14, color=BODY, ha='left')
    x = 8.1
    s.box(x, 0.6, w - x - 0.1, h - 0.7, '', fill=GOLD, lw=2, r=0.08)
    right = int(round(r['json']['acc'] * 450))
    s.text(x + (w - x - 0.1) / 2, h - 0.8, f'{right} of 450', size=32, weight='bold')
    _wrap(s, x + (w - x - 0.1) / 2, h - 1.55, w - x - 0.5, 'new digits read correctly, about 97 in 100', 16)
    _wrap(s, x + (w - x - 0.1) / 2, 1.5, w - x - 0.5, 'It learned from 1,347 labelled digits it was shown', 15, color=BODY)
    s.text(w - 0.1, 0.25, 'Recorded run, 5 Nov 2026', size=14, color=MUTE, ha='right')
    return s


# ------------------------------------------------------------------ demonstration: practice makes it better (recorded)
@fig('x_l01_practice')
def x_l01_practice(w, h, **_):
    r = _r01()
    curve = r['json']['curve']
    s = Scene(w, h)
    n = len(curve)
    x0, x1, y0, y1 = 0.6, w - 0.15, 0.95, h - 0.55
    bw = (x1 - x0) / n
    s.line(x0, y0, x1, y0, lw=2)
    for i, (passes, acc) in enumerate(curve):
        v = round(acc * 100)
        bh = (y1 - y0 - 0.35) * v / 100
        x = x0 + i * bw + 0.1
        s.rect(x, y0, bw - 0.2, bh, fill=GOLD if i == n - 1 else PAPER, edge=INK, lw=1.4)
        s.text(x + (bw - 0.2) / 2, y0 + bh + 0.2, str(v), size=15, weight='bold', color=RED if i in (0, n - 1) else INK)
        s.text(x + (bw - 0.2) / 2, y0 - 0.25, str(passes), size=14)
    s.text(0.1, h - 0.2, 'Right, out of 100 unseen digits', size=15, weight='bold', ha='left')
    s.text((x0 + x1) / 2, 0.3, 'Passes through the 1,347 practice digits', size=15, color=BODY)
    return s


# ------------------------------------------------------------------ demonstration: move it one dot (recorded)
@fig('x_l01_shift')
def x_l01_shift(w, h, **_):
    r = _r01()
    img = r['images'][int(r['img_i'])]
    acc = r['json']['shift']
    s = Scene(w, h)
    sz = 1.7
    labs = ['As it learned them', 'Moved one dot right', 'Moved two dots right']
    for k in range(3):
        a = np.zeros_like(img)
        a[:, k:] = img[:, :8 - k]
        x = 0.35 + k * 2.5
        _gray(s, a, x, 1.75, sz)
        _wrap(s, x + sz / 2, 4.05, 2.2, labs[k], 15, weight='bold')
        v = round(acc[str(k)] * 100)
        s.text(x + sz / 2, 1.3, f'{v} in 100', size=22, weight='bold', color=INK if k == 0 else RED)
        s.text(x + sz / 2, 0.92, 'right', size=15, color=BODY)
        if k < 2:
            s.arrow(x + sz + 0.15, 2.6, x + 2.5 - 0.15, 2.6, lw=2)
    s.text(0.1, 0.3, 'All 450 unseen digits, moved the same way. Recorded run, 5 Nov 2026.', size=14, color=MUTE, ha='left')
    return s


# ------------------------------------------------------------------ your people
@fig('x_l01_people')
def x_l01_people(w, h, **_):
    s = Scene(w, h)
    roles = [('Radiologist', ['Reading every routine scan', 'The doubtful scans and the patient', 'Knowing when the tool is out of its depth', 'Fear: replaced. Gain: time for hard cases']),
             ('Inspector or field officer', ['Walking every field or shelf', 'Following up what the photos flag', 'Taking photos the tool can read', 'Fear: watched. Gain: wider reach']),
             ('Data-entry clerk', ['Typing every form', 'Checking the fields marked unsure', 'Spotting errors in a filled table', 'Fear: the job goes. Gain: less typing'])]
    people_grid(s, w, h, roles)
    return s


# ------------------------------------------------------------------ a wrong "no" about a person needs an appeal (RTL-07)
@fig('x_l01_appeal')
def x_l01_appeal(w, h, **_):
    s = Scene(w, h)
    steps = [('Selfie check', 'Face compared with account photo', 'phone'),
             ('Mismatches', 'Repeated, for one courier', 'cross'),
             ('Removed', 'Through an automated process', 'lock'),
             ('Claim, 2024', 'Settled; the courier was reinstated', 'stamp')]
    bw, bh = 4.25, 0.72
    gap = (h - 0.2 - 4 * bh) / 3
    for i, (who, what, ic) in enumerate(steps):
        y = h - 0.1 - bh - i * (bh + gap)
        s.box(0.1, y, bw, bh, '', fill=GOLD if i == 2 else PAPER, lw=1.8, r=0.08)
        s.icon(ic, 0.45, y + bh / 2, 0.48)
        s.text(0.8, y + bh / 2 + 0.14, who, size=15, weight='bold', ha='left')
        s.text(0.8, y + bh / 2 - 0.16, what, size=14, ha='left', color=BODY)
        if i < 3:
            s.arrow(0.1 + bw / 2, y - 0.02, 0.1 + bw / 2, y - gap + 0.02, lw=1.8, head=12)
    x = 4.6
    s.box(x, 1.05, w - x - 0.1, h - 1.15, '', fill=PAPER, edge=RED, lw=2.2, r=0.08)
    s.text(x + 0.15, h - 0.4, 'Uber Eats, UK', size=16, weight='bold', color=RED, ha='left')
    hh = _wrap(s, x + 0.15, h - 0.65, w - x - 0.4, 'A discrimination claim was settled in March 2024, without admission.', 15, ha='left', va='top', color=BODY)
    hh += _wrap(s, x + 0.15, h - 0.8 - hh, w - x - 0.4, 'Uber says its checks have human review and the automated check did not cause the removal.', 15, ha='left', va='top', color=BODY)
    _wrap(s, x + 0.15, h - 0.95 - hh, w - x - 0.4, 'The bias question was never tested in court.', 15, weight='bold', ha='left', va='top', color=RED)
    _wrap(s, x + 0.15, 0.62, w - x - 0.3, 'Name the person who reviews each “no”.', 15, weight='bold', ha='left')
    s.text(x + 0.15, 0.2, 'Personnel Today, 26 Mar 2024', size=14, color=MUTE, ha='left')
    return s


# ------------------------------------------------------------------ hands-on: one portfolio entry (fictional company)
@fig('x_l01_portfolio')
def x_l01_portfolio(w, h, **_):
    s = Scene(w, h)
    rows = [('The use', 'Read signed delivery notes into the order system'),
            ('What goes in', 'Phone photos of the notes shops sign'),
            ('What comes out', 'A table row per note, unclear fields marked'),
            ('Who uses it', 'Accounts clerks in Jinja'),
            ('How we would know it works', 'Of 100 notes a clerk checks, how many fields were right'),
            ('Today: what it reads', 'Handwriting and stamps; poor photos go to a clerk')]
    portfolio_entry(s, w, h, rows)
    return s


# ------------------------------------------------------------------ case layouts other than the four-box card (12 November 2026)
# Each case gets the layout its story needs: a headline number, a before and after, a timeline, a small chart of its own figures,
# or two columns, what happened and what it means for you.  Gold marks at most one thing; red only a real failure or warning.
def _org(s, h, org):
    s.text(0.1, h - 0.25, org, size=18, weight='bold', ha='left')


def _col(s, x, top, cw, items, size=17, gap=0.16, color=BODY):
    """Short lines stacked from `top` downwards, each under a hairline. Returns the y reached."""
    y = top
    for i, t in enumerate(items):
        if i:
            s.line(x, y + gap / 2, x + cw, y + gap / 2, color=HAIR, lw=1.0)
        hh = _wrap(s, x, y, cw, t, size, ha='left', va='top', color=color)
        y -= hh + gap
    return y


@fig('x_l01_case_number')
def x_l01_case_number(w, h, org='', big='', big_note='', facts=(), source='', warn=False, **_):
    """A headline number with one line of context on the left; two or three plain facts on the right."""
    s = Scene(w, h)
    _org(s, h, org)
    lw_ = w * 0.42
    bs = 66
    while K.width_in(big, bs, 'bold') > lw_ - 0.2 and bs > 36:
        bs -= 2
    s.text(0.1, h - 1.25, big, size=bs, weight='bold', ha='left', color=RED if warn else INK)
    s.line(0.1, h - 1.95, 0.1 + min(lw_ - 0.3, K.width_in(big, bs, 'bold')), h - 1.95, color=RED if warn else GOLD, lw=5)
    _wrap(s, 0.1, h - 2.2, lw_ - 0.3, big_note, _fit(big_note, lw_ - 0.3, h - 2.8, 20, 16), ha='left', va='top', color=INK)
    x = lw_ + 0.3
    s.line(x - 0.2, 0.55, x - 0.2, h - 0.6, color=HAIR, lw=1.2)
    cw = w - x - 0.1
    sz = 15
    for cand in range(20, 14, -1):
        if sum(len(K.wrap(t, cand, 'regular', cw)) * _lh(cand) + 0.22 for t in facts) <= h - 1.4:
            sz = cand
            break
    _col(s, x, h - 0.7, cw, list(facts), sz, gap=0.22)
    _source(s, source, y=0.2)
    return s


@fig('x_l01_case_twocol')
def x_l01_case_twocol(w, h, org='', left=(), right=(), heads=('What happened', 'What it means for you'), source='', **_):
    """Two columns of short lines, what happened and what it means for you. No boxes."""
    s = Scene(w, h)
    _org(s, h, org)
    cw = (w - 0.2 - 0.6) / 2
    avail = h - 1.6
    sz = 15
    for cand in range(20, 14, -1):
        if all(sum(len(K.wrap(t, cand, 'regular', cw)) * _lh(cand) + 0.2 for t in items) <= avail for items in (left, right)):
            sz = cand
            break
    for i, (hd, items) in enumerate(zip(heads, (left, right))):
        x = 0.1 + i * (cw + 0.6)
        s.text(x, h - 0.85, hd, size=18, weight='bold', ha='left', color=INK)
        s.line(x, h - 1.1, x + cw, h - 1.1, color=INK, lw=2)
        _col(s, x, h - 1.25, cw, list(items), sz, gap=0.2, color=BODY if i == 0 else INK)
    _source(s, source, y=0.2)
    return s


@fig('x_l01_case_beforeafter')
def x_l01_case_beforeafter(w, h, org='', before=('', '', ''), after=('', '', ''), note='', source='', **_):
    """Before and after: a label, a value and one line under each, with an arrow between. The after value is the one in gold."""
    s = Scene(w, h)
    _org(s, h, org)
    pw = (w - 0.2 - 1.2) / 2
    y0, y1 = 0.95 if note else 0.55, h - 0.6
    for i, (lab, val, txt) in enumerate((before, after)):
        x = 0.1 + i * (pw + 1.2)
        s.text(x, y1 - 0.15, lab, size=18, weight='bold', ha='left', color=MUTE if i == 0 else INK)
        vs = 44
        while K.width_in(val, vs, 'bold') > pw - 0.1 and vs > 26:
            vs -= 2
        s.text(x, y1 - 0.95, val, size=vs, weight='bold', ha='left', color=MUTE if i == 0 else INK)
        if i == 1:
            s.line(x, y1 - 1.5, x + K.width_in(val, vs, 'bold'), y1 - 1.5, color=GOLD, lw=5)
        _wrap(s, x, y1 - 1.75, pw, txt, _fit(txt, pw, y1 - 1.75 - y0, 18, 15), ha='left', va='top', color=BODY)
    s.arrow(0.1 + pw + 0.25, y1 - 0.95, 0.1 + pw + 0.95, y1 - 0.95, lw=2.6, head=18)
    if note:
        _wrap(s, 0.1, 0.62, w - 0.2, note, 15, ha='left', color=INK)
    _source(s, source, y=0.2)
    return s


@fig('x_l01_case_timeline')
def x_l01_case_timeline(w, h, org='', events=(), hl=None, warn=None, source='', **_):
    """A short timeline: (when, what) on a line, one event in gold, one optionally in red."""
    s = Scene(w, h)
    _org(s, h, org)
    n = len(events)
    ly = h - 1.35
    s.line(0.25, ly, w - 0.25, ly, color=INK, lw=2)
    cw = (w - 0.3) / n
    sz = min(_fit(t, cw - 0.25, ly - 0.75, 19, 15) for _, t in events)
    for i, (when, txt) in enumerate(events):
        x = 0.15 + i * cw + 0.1
        col = RED if i == warn else INK
        s.circle(x + 0.12, ly, 0.12, fill=GOLD if i == hl else (RED if i == warn else PAPER), edge=col, lw=2, z=5)
        s.text(x, ly + 0.42, when, size=17, weight='bold', ha='left', color=col)
        _wrap(s, x, ly - 0.3, cw - 0.25, txt, sz, ha='left', va='top', color=INK if i in (hl, warn) else BODY)
    _source(s, source, y=0.2)
    return s


@fig('x_l01_case_bars')
def x_l01_case_bars(w, h, org='', bars=(), hl=None, note='', source='', label_w=3.6, **_):
    """A small horizontal bar chart of a case's own figures: (label, value, shown). One bar in gold."""
    s = Scene(w, h)
    _org(s, h, org)
    n = len(bars)
    top, bot = h - 0.7, (1.0 if note else 0.6)
    rh = (top - bot) / n
    bw = min(0.6, rh * 0.62)
    vmax = max(v for _, v, _ in bars)
    x0 = 0.1 + label_w
    span = w - x0 - 0.35 - max(K.width_in(sh, 17, 'bold') for _, _, sh in bars)
    for i, (lab, v, shown) in enumerate(bars):
        y = top - (i + 0.5) * rh
        _wrap(s, 0.1, y, label_w - 0.2, lab, _fit(lab, label_w - 0.2, rh, 17, 14), ha='left', color=INK)
        L = span * v / vmax
        s.rect(x0, y - bw / 2, max(L, 0.03), bw, fill=GOLD if i == hl else PAPER, edge=INK, lw=1.4)
        s.text(x0 + L + 0.12, y, shown, size=17, weight='bold', ha='left')
    s.line(x0, bot - 0.05, x0, top + 0.05, color=INK, lw=1.4)
    if note:
        _wrap(s, 0.1, 0.62, w - 0.2, note, 15, ha='left', color=BODY)
    _source(s, source, y=0.2)
    return s
