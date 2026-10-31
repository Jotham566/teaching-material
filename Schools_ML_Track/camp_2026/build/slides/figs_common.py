"""Shared illustrations for the Python foundations of both tracks (figure names start with c_).

Every figure is drawn in inches on a canvas the size of its slide placement and returns a Scene.
Data-driven numbers are computed from camp_2026/data, never typed.
"""
import re

import numpy as np
import pandas as pd

from brand import CAMP, INK, BODY, MUTE, GREY, HAIR, PALE, PAPER, RED, GOLD
from figkit import Scene, fig

DATA = CAMP / 'data'
MONO_EM = 0.602

KEYWORDS = {'def', 'if', 'else', 'elif', 'for', 'in', 'return', 'import', 'from', 'as', 'and', 'or', 'not', 'while', 'assert', 'True', 'False', 'None'}
_TOK = re.compile(r'(#.*$)|("(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')|(\b[A-Za-z_][A-Za-z0-9_]*\b)|(\s+)|(.)')


def fit_mono(text, box_w, size, pad=0.25):
    """Largest font size (at most `size`) at which monospaced text fits inside a box of width box_w."""
    return max(11, min(size, int((box_w - pad) * 72 / (MONO_EM * len(text)))))


def shop():
    d = pd.read_csv(DATA / 'camp_shop.csv')
    d['revenue'] = d['units'] * d['unit_price_ugx']
    return d


def fmt(n):
    return f'{int(n):,}'


class Code:
    """A black code panel with syntax colours and helpers to point at characters."""

    def __init__(self, s, x, y_top, lines, size=18, pad=0.2, w=None, lead=1.5, hl_lines=()):
        self.s, self.x0, self.ytop, self.lines, self.size, self.pad = s, x, y_top, lines, size, pad
        self.cw = size * MONO_EM / 72.0
        self.lh = size * lead / 72.0
        longest = max(len(l) for l in lines)
        self.w = w or (longest * self.cw + 2 * pad)
        self.h = len(lines) * self.lh + 2 * pad
        s.box(x, y_top - self.h, self.w, self.h, '', fill=INK, edge=INK, r=0.08, z=2)
        for i, line in enumerate(lines):
            if i in hl_lines:
                s.ax.add_patch(__import__('matplotlib').patches.Rectangle((x + 0.06, self.y(i) - self.lh / 2), self.w - 0.12, self.lh, fc='#3A3A3A', ec='none', zorder=3))
            for m in _TOK.finditer(line):
                com, st, word, ws, other = m.groups()
                if ws:
                    continue
                t = m.group(0)
                col, wt = PAPER, 'normal'
                if com:
                    col = '#A8A8A8'
                elif st:
                    col = GOLD
                elif word in KEYWORDS:
                    wt = 'bold'
                s.text(self.px(m.start()), self.y(i), t, size=size, color=col, weight=wt, mono=True, ha='left', z=5)

    def px(self, col):
        return self.x0 + self.pad + col * self.cw

    def y(self, line):
        return self.ytop - self.pad - (line + 0.5) * self.lh

    def span(self, line, c0, c1):
        return self.px(c0), self.px(c1)

    def mark(self, line, c0, c1, color=GOLD, lw=2.2):
        """Outline characters c0..c1 of a line."""
        x0, x1 = self.span(line, c0, c1)
        self.s.ax.add_patch(__import__('matplotlib').patches.FancyBboxPatch((x0 - 0.005, self.y(line) - self.lh * 0.42), x1 - x0 + 0.01, self.lh * 0.84,
                            boxstyle='round,pad=0,rounding_size=0.04', fc='none', ec=color, lw=lw, zorder=6))

    @property
    def bottom(self):
        return self.ytop - self.h


def label_under(s, code, line, c0, c1, text, y_off=0.5, size=18, color=INK, sub=None):
    """A bracket under characters with a label beneath it. Returns the label y."""
    x0, x1 = code.span(line, c0, c1)
    yb = code.bottom - 0.22 if line == len(code.lines) - 1 else code.y(line) - code.lh / 2 - 0.02
    s.brace(x0, x1, yb, depth=0.14, color=color, lw=1.8)
    ly = yb - y_off
    s.text((x0 + x1) / 2, ly, text, size=size, weight='bold', color=color)
    if sub:
        s.text((x0 + x1) / 2, ly - 0.32, sub, size=16, color=MUTE)
    return ly


def axes_xy(s, x, y, w, h, xlim, ylim, xticks=None, yticks=None, xlabel='', ylabel='', size=16, grid=False, xfmt=None, yfmt=None):
    """Draw simple x/y axes in scene inches and return mappers px(v), py(v)."""
    px = lambda v: x + (v - xlim[0]) / (xlim[1] - xlim[0]) * w
    py = lambda v: y + (v - ylim[0]) / (ylim[1] - ylim[0]) * h
    s.line(x, y, x + w, y, color=INK, lw=1.8)
    s.line(x, y, x, y + h, color=INK, lw=1.8)
    for t in (xticks or []):
        s.line(px(t), y, px(t), y - 0.07, color=INK, lw=1.4)
        s.text(px(t), y - 0.28, xfmt(t) if xfmt else str(t), size=size, color=BODY)
        if grid:
            s.line(px(t), y, px(t), y + h, color=HAIR, lw=0.8, z=0)
    for t in (yticks or []):
        s.line(x - 0.07, py(t), x, py(t), color=INK, lw=1.4)
        s.text(x - 0.14, py(t), yfmt(t) if yfmt else str(t), size=size, color=BODY, ha='right')
        if grid:
            s.line(x, py(t), x + w, py(t), color=HAIR, lw=0.8, z=0)
    if xlabel:
        s.text(x + w / 2, y - 0.62, xlabel, size=size + 1, color=INK)
    if ylabel:
        s.text(x - 0.95, y + h / 2, ylabel, size=size + 1, color=INK, rot=90)
    return px, py


def key_cap(s, x, y, label, w=None, size=18):
    w = w or max(0.6, 0.14 * len(label) + 0.3)
    s.box(x, y, w, 0.5, label, size=size, fill=PAPER, weight='bold', r=0.07, lw=2.0)
    return w


# ============================================================ session 1: notebook, files, tables
@fig('c_notebook_anatomy')
def c_notebook_anatomy(w, h, code_lines=('print("Hello, data")', 'print(3 + 2)'), out_lines=('Hello, data', '5'), text_cell='My first notebook'):
    s = Scene(w, h)
    fx, fw = 0.1, w * 0.6
    s.box(fx, 0.8, fw, h - 0.95, '', fill=PAPER, edge=INK, lw=2.0, r=0.1, z=1)
    # text cell
    ty, th = h - 1.35, 0.8
    s.box(fx + 0.25, ty, fw - 0.5, th, text_cell, size=22, weight='bold', fill=PAPER, edge=HAIR, lw=1.4, ha='left', pad=0.2)
    # code cell
    cy_top = ty - 0.25
    ch = 0.5 + 0.34 * len(code_lines)
    s.box(fx + 0.25, cy_top - ch, fw - 0.5, ch, '', fill=PAPER, edge=INK, lw=2.2, r=0.05)
    s.text(fx + 0.45, cy_top - 0.28, '[ 1 ]', size=15, color=MUTE, mono=True, ha='left')
    for i, l in enumerate(code_lines):
        s.text(fx + 1.15, cy_top - 0.3 - i * 0.34, l, size=17, mono=True, ha='left')
    # output
    oy_top = cy_top - ch - 0.12
    oh = 0.22 + 0.34 * len(out_lines)
    for i, l in enumerate(out_lines):
        s.text(fx + 1.15, oy_top - 0.26 - i * 0.34, l, size=17, mono=True, ha='left', color=INK)
    s.line(fx + 0.25, oy_top + 0.02, fx + fw - 0.25, oy_top + 0.02, color=HAIR, lw=1.2)
    # key caps
    kx = fx + 0.25
    wk = key_cap(s, kx, 0.08, 'Shift')
    s.text(kx + wk + 0.25, 0.33, '+', size=22, weight='bold')
    key_cap(s, kx + wk + 0.5, 0.08, 'Enter')
    s.text(kx + wk + 1.55, 0.33, 'runs the cell', size=18, color=BODY, ha='left')
    # labels
    lx = fx + fw + 0.55
    def lab(yc, head, sub, ty_):
        s.arrow(lx - 0.1, yc, fx + fw - 0.05, ty_, color=RED, lw=2.0, head=14)
        s.text(lx, yc + 0.14, head, size=22, weight='bold', ha='left')
        s.text(lx, yc - 0.2, sub, size=17, color=MUTE, ha='left')
    lab(ty + th / 2, 'text cell', 'words for people', ty + th / 2)
    lab(cy_top - ch / 2, 'code cell', 'Python runs it', cy_top - ch / 2)
    lab(oy_top - oh / 2, 'output', 'the answer', oy_top - oh / 2)
    return s


@fig('c_folder_files')
def c_folder_files(w, h, folder='HolidayCamp', files=(('DA01.ipynb', 'notebook'), ('camp_shop.csv', 'table')), mismatch=False):
    s = Scene(w, h)
    big = w > 7
    fs = 20 if big else 15
    if not mismatch:
        s.icon('folder', w * 0.2, h * 0.62, 1.9 if big else 1.5)
        s.text(w * 0.2, h * 0.3, folder, size=24 if big else 20, weight='bold')
        s.text(w * 0.2, h * 0.16, 'a folder on the laptop', size=16, color=MUTE)
        for i, (name, kind) in enumerate(files):
            y = h * (0.78 - i * 0.3)
            s.arrow(w * 0.34, h * 0.62, w * 0.45, y, color=INK, lw=1.8, head=14)
            s.icon('notebook' if kind == 'notebook' else 'receipt', w * 0.5, y, 0.75)
            s.text(w * 0.56, y + 0.02, name, size=fs, mono=True, ha='left')
        s.box(w * 0.4, 0.12, w * 0.56, 0.7, 'Same folder: Python finds the file' if big else 'Same folder: file found', size=19 if big else 16, fill=GOLD, weight='bold', r=0.05)
    else:
        for i, (fold, (name, kind)) in enumerate(zip(('Downloads', 'Documents'), files)):
            cx = w * (0.2 + 0.58 * i)
            s.icon('folder', cx, h * 0.68, 1.6 if big else 1.3)
            s.text(cx, h * 0.42, fold, size=22 if big else 18, weight='bold')
            s.icon('notebook' if kind == 'notebook' else 'receipt', cx, h * 0.26, 0.6)
            s.text(cx, h * 0.07, name, size=max(14, fs - 2), mono=True, va='bottom')
        s.arrow(w * 0.33, h * 0.68, w * 0.65, h * 0.68, color=RED, lw=2.2, dash=True)
        s.icon('cross', w * 0.49, h * 0.68, 0.8)
        s.text(w * 0.49, h * 0.9, 'FileNotFoundError', size=19 if big else 16, weight='bold', color=RED)
    return s


@fig('c_csv_to_table')
def c_csv_to_table(w, h, rows=5):
    d = pd.read_csv(DATA / 'camp_shop.csv').head(rows)
    s = Scene(w, h)
    fw = w * 0.4
    s.box(0.1, h * 0.2, fw, h * 0.62, '', fill=PAPER, edge=INK, lw=1.8, r=0.05)
    s.text(0.1 + fw / 2, h * 0.9, 'camp_shop.csv', size=22, weight='bold')
    lines = [','.join(str(v) for v in d.columns)] + [','.join(str(v) for v in r) for r in d.itertuples(index=False)]
    for i, l in enumerate(lines):
        s.text(0.28, h * 0.77 - i * 0.42, l, size=14, mono=True, ha='left')
    s.text(0.1 + fw / 2, h * 0.09, 'plain text, commas between values', size=17, color=MUTE)
    ax0, ax1 = 0.1 + fw + 0.12, 0.1 + fw + 1.25
    s.arrow(ax0, h * 0.5, ax1, h * 0.5, color=RED, lw=2.6, head=20)
    s.text((ax0 + ax1) / 2, h * 0.63, 'read_csv', size=18, weight='bold', color=RED, mono=True)
    cols = ['sale_id', 'date', 'item', 'units', 'unit_price_ugx']
    cw = [0.95, 1.5, 0.9, 0.9, 1.65]
    tx = ax1 + 0.15
    scale = (w - tx - 0.1) / sum(cw)
    cw = [c * scale for c in cw]
    rr = [cols] + [[str(v) for v in r] for r in d.itertuples(index=False)]
    rh = 0.4
    ytop = h * 0.82
    s.table(tx, ytop, cw, rh, rr, size=14, hl_cells={(2, c): GOLD for c in range(5)})
    s.text(tx + sum(cw) / 2, h * 0.9, 'a table: rows and columns', size=20, weight='bold')
    yb = ytop - len(rr) * rh - 0.28
    s.box(tx, yb - 0.12, 0.36, 0.3, '', fill=GOLD, lw=1.4, r=0.02)
    s.text(tx + 0.5, yb + 0.03, 'one row is one sale', size=18, ha='left')
    s.text(tx, yb - 0.5, 'the top line names each column', size=18, ha='left')
    return s


@fig('c_print_anatomy')
def c_print_anatomy(w, h):
    s = Scene(w, h)
    c1 = Code(s, 0.2, h - 0.25, ['print("Hello, data")'], size=22)
    label_under(s, c1, 0, 0, 5, 'print', size=20, sub='the instruction')
    label_under(s, c1, 0, 6, 19, 'goes inside ( )', size=20)
    ox = c1.x0 + c1.w + 0.3
    s.arrow(ox, c1.y(0), ox + 0.7, c1.y(0), color=RED, lw=2.6)
    s.box(ox + 0.8, c1.y(0) - 0.32, 2.1, 0.64, 'Hello, data', size=19, mono=True, fill=PAPER, lw=1.8)
    c2 = Code(s, 0.2, h * 0.50, ['print(3 + 2)'], size=22)
    label_under(s, c2, 0, 6, 11, '3 + 2', size=20, sub='no quotation marks: Python works it out')
    ox = c1.x0 + c1.w + 0.3
    s.arrow(ox, c2.y(0), ox + 0.7, c2.y(0), color=RED, lw=2.6)
    s.box(ox + 0.8, c2.y(0) - 0.32, 0.9, 0.64, '5', size=24, mono=True, fill=PAPER, lw=1.8)
    s.text(0.2 + 0.0, h - 0.0, '', size=1)
    return s


@fig('c_hero_week_of_sales')
def c_hero_week_of_sales(w, h):
    d = shop()
    day = d.groupby('date')['revenue'].sum().head(7)
    s = Scene(w, h)
    s.icon('shop', 1.15, h - 1.35, 1.7)
    s.text(1.15, h - 2.35, 'a small shop', size=20, weight='bold')
    s.text(1.15, h - 2.7, '60 sales on 20 days', size=16, color=MUTE)
    s.icon('receipt', 1.15, 0.95, 1.1)
    s.arrow(1.15, 1.55, 1.15, 1.9, color=INK, lw=1.6, head=12)
    px, py = axes_xy(s, 3.3, 0.95, w - 3.9, h - 1.9, (0, 7), (0, 50000), xticks=[], yticks=[0, 10000, 20000, 30000, 40000, 50000],
                     yfmt=lambda v: f'{int(v / 1000)}k', size=16)
    bw = (w - 3.9) / 7 * 0.6
    for i, (dt, v) in enumerate(day.items()):
        x = px(i + 0.5) - bw / 2
        s.box(x, 0.95, bw, py(v) - 0.95, '', fill=GOLD, edge=INK, lw=1.6, r=0.01)
        s.text(px(i + 0.5), 0.62, dt[-5:], size=15, color=BODY)
        s.text(px(i + 0.5), py(v) + 0.22, f'{int(v / 1000)}k', size=16, weight='bold')
    s.text(3.3 + (w - 3.9) / 2, h - 0.4, 'Money taken each day, first seven days (UGX)', size=20, weight='bold')
    return s


# ============================================================ session 2: values, names, types
@fig('c_sale_parts_types')
def c_sale_parts_types(w, h):
    s = Scene(w, h)
    d = shop().iloc[2]
    cells = [('item', d['item'], 'string', 'text'), ('units', int(d['units']), 'integer', 'a whole number'),
             ('unit_price_ugx', int(d['unit_price_ugx']), 'integer', 'a whole number'), ('date', d['date'], 'string', 'text')]
    bw, gap = (w - 0.3 - 3 * 0.35) / 4, 0.35
    for i, (name, val, typ, plain) in enumerate(cells):
        x = 0.15 + i * (bw + gap)
        s.text(x + bw / 2, h - 0.5, name, size=19, color=MUTE)
        shown = f'"{val}"' if typ == 'string' else str(val)
        s.box(x, h - 2.2, bw, 1.25, shown, size=34 if len(shown) < 9 else 24, weight='bold', fill=GOLD if typ == 'string' else PAPER, lw=2.2, r=0.05, mono=False)
        s.arrow(x + bw / 2, h - 2.35, x + bw / 2, h - 3.0, color=RED, lw=2.2)
        s.text(x + bw / 2, h - 3.3, typ, size=28, weight='bold')
        s.text(x + bw / 2, h - 3.75, plain, size=18, color=BODY)
    s.text(w / 2, 0.3, 'One sale in the shop table: every part has a type', size=20, color=MUTE)
    return s


def run_lines(lines):
    """Execute code lines one at a time; return [(line, {name: value}, printed_text_or_None)]."""
    import io, contextlib
    ns, out = {}, []
    for ln in lines:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            exec(ln, ns)
        vals = {k: v for k, v in ns.items() if not k.startswith('__')}
        out.append((ln, vals, buf.getvalue().strip() or None))
    return out


def vstr(v):
    if isinstance(v, float):
        return f'{v:g}' if v != int(v) else f'{v:.1f}'
    return str(v)


@fig('c_labelled_boxes')
def c_labelled_boxes(w, h, code=('price = 2000', 'units = 3', 'revenue = price * units'), names=('price', 'units', 'revenue')):
    steps = run_lines(code)
    final = steps[-1][1]
    s = Scene(w, h)
    cb = Code(s, 0.15, h - 0.2, list(code), size=20)
    tx = cb.x0 + cb.w + 0.3
    for i, t in enumerate(['Python works out', 'the right side first,', 'then stores the answer', 'under the name at left.']):
        s.text(tx, h - 0.55 - i * 0.4, t, size=18, ha='left', color=BODY)
    n = len(names)
    bw = min(2.1, (w - 0.4 - (n - 1) * 0.5) / n)
    x0 = (w - (n * bw + (n - 1) * 0.5)) / 2
    for i, nm in enumerate(names):
        x = x0 + i * (bw + 0.5)
        s.box(x, 0.3, bw, 1.35, '', fill=GOLD if i == n - 1 and n > 2 else PAPER, lw=2.0, r=0.04)
        s.text(x + bw / 2, 2.0, nm, size=24, weight='bold', mono=True)
        s.text(x + bw / 2, 0.97, vstr(final[nm]), size=34, weight='bold', mono=True)
    s.text(w / 2, 2.62, 'each name is a label on a box that holds a value', size=20, color=BODY)
    return s


@fig('c_types_bins')
def c_types_bins(w, h):
    s = Scene(w, h)
    bins = [('integer', 'a whole number', ['3', '2000', '12'], "<class 'int'>"), ('float', 'has a decimal point', ['2500.5', '12.5', '0.25'], "<class 'float'>"),
            ('string', 'text in quotes', ['"2000"', '"Juice"', '"3"'], "<class 'str'>")]
    bw = (w - 0.3 - 2 * 0.3) / 3
    for i, (nm, plain, ex, cls) in enumerate(bins):
        x = 0.15 + i * (bw + 0.3)
        s.box(x, 1.0, bw, h - 1.2, '', fill=PAPER, lw=2.0, r=0.05)
        s.text(x + bw / 2, h - 0.55, nm, size=28, weight='bold')
        s.text(x + bw / 2, h - 1.0, plain, size=17, color=BODY)
        for k, e in enumerate(ex):
            s.box(x + 0.35, h - 2.15 - k * 0.78, bw - 0.7, 0.6, e, size=22, mono=True, fill=GOLD if nm == 'string' and k == 0 else PAPER, lw=1.6, r=0.05)
        s.text(x + bw / 2, 0.58, cls, size=18, mono=True, color=RED, weight='bold')
    s.text(w / 2, 0.15, 'type(...) reports the type', size=17, color=MUTE) if False else None
    return s


@fig('c_text_vs_number')
def c_text_vs_number(w, h, number=2000):
    s = Scene(w, h)
    for i, (txt, typ, cap, what) in enumerate([(str(number), 'int', 'an amount', 'Python can calculate with it'),
                                                  (f'"{number}"', 'str', 'text', 'just characters, like a name')]):
        x = 0.2 + i * (w / 2)
        s.box(x + 0.2, h * 0.5, w / 2 - 0.9, 1.3, txt, size=44, weight='bold', mono=True, fill=PAPER if i == 0 else GOLD, lw=2.2, r=0.05)
        s.text(x + (w / 2 - 0.5) / 2, h * 0.5 + 1.75, cap, size=26, weight='bold')
        s.text(x + (w / 2 - 0.5) / 2, h * 0.5 - 0.35, f'type is {typ}', size=20, mono=True, color=RED)
        s.text(x + (w / 2 - 0.5) / 2, h * 0.5 - 0.95, what, size=19, color=BODY)
    s.text(w / 2, h * 0.5 + 0.65, '', size=1)
    return s


@fig('c_reassign_trace')
def c_reassign_trace(w, h, code=('price = 2500.5', 'quantity = 2', 'total = price * quantity', 'print(total)', 'quantity = 4', 'print(total)', 'total = price * quantity', 'print(total)'),
                     names=('price', 'quantity', 'total')):
    steps = run_lines(code)
    s = Scene(w, h)
    nrow = len(code) + 1
    rh = min(0.5, (h - 0.5) / nrow)
    cwid = [max(len(c) for c in code) * 15 * MONO_EM / 72 + 0.25] + [1.0] * len(names) + [1.1]
    sc = (w - 0.2) / sum(cwid)
    if sc < 1:
        cwid = [c * sc for c in cwid]
    rows = [['code line'] + list(names) + ['printed']]
    prev = {}
    hl = {}
    for r, (ln, vals, pr) in enumerate(steps, start=1):
        row = [ln]
        for c, nm in enumerate(names, start=1):
            v = vals.get(nm)
            row.append('' if v is None else vstr(v))
            if v is not None and prev.get(nm) != v:
                hl[(r, c)] = GOLD
        row.append(pr or '')
        rows.append(row)
        prev = vals
    s.table(0.1, h - 0.1, cwid, rh, rows, size=15, mono_cols=(0, len(names) + 1), hl_cells=hl, align=['left'] + ['center'] * (len(names) + 1))
    return s


@fig('c_stale_total')
def c_stale_total(w, h):
    s = Scene(w, h)
    st = run_lines(['price = 2500.5', 'quantity = 2', 'total = price * quantity', 'quantity = 4', 'total = price * quantity'])
    snaps = [('after the first calculation', st[2][1]), ('after quantity = 4', st[3][1]), ('after calculating again', st[4][1])]
    colw = (w - 0.3) / 3
    for i, (cap, v) in enumerate(snaps):
        x = 0.15 + i * colw
        s.text(x + colw / 2, h - 0.4, cap, size=18, color=BODY)
        for k, nm in enumerate(['price', 'quantity', 'total']):
            yy = h - 1.6 - k * 1.2
            fill = GOLD if (i == 1 and nm == 'quantity') or (i == 2 and nm == 'total') else PAPER
            s.box(x + 0.25, yy, colw - 0.5, 1.05, '', fill=fill, lw=1.8, r=0.04)
            s.text(x + 0.4, yy + 0.9, nm, size=16, mono=True, ha='left', va='top')
            s.text(x + colw / 2, yy + 0.38, vstr(v[nm]), size=26, weight='bold', mono=True)
        if i == 1:
            s.text(x + colw / 2, 0.3, 'total is still the old answer', size=18, color=RED, weight='bold')
    return s


# ============================================================ session 3: arithmetic, conversion, errors
@fig('c_operators')
def c_operators(w, h):
    s = Scene(w, h)
    rows = [('+', 'add', 'two sales together', '3000 + 2000'), ('-', 'subtract', 'take off a discount', '3000 - 500'),
            ('*', 'multiply', '4 items at 3000 each', '4 * 3000'), ('/', 'divide', 'share 3000 by 4', '3000 / 4')]
    rh = (h - 0.4) / len(rows)
    for i, (sym, name, story, expr) in enumerate(rows):
        y = h - 0.2 - (i + 1) * rh
        s.line(0.15, y, w - 0.15, y, color=HAIR, lw=1.2)
        yc = y + rh / 2
        s.box(0.25, yc - 0.38, 0.76, 0.76, sym, size=34, weight='bold', fill=GOLD, lw=2.0, r=0.05)
        s.text(1.25, yc + 0.17, name, size=24, weight='bold', ha='left')
        s.text(1.25, yc - 0.22, story, size=17, color=MUTE, ha='left')
        s.text(3.75, yc, expr, size=20, mono=True, ha='left')
        s.arrow(5.7, yc, 6.1, yc, color=RED, lw=2.0, head=14)
        s.text(w - 0.2, yc, vstr(eval(expr)), size=22, weight='bold', mono=True, ha='right')
    return s


@fig('c_precedence')
def c_precedence(w, h, left=('3000 - 500 * 2', '500 * 2', 'multiply first'), right=('(3000 - 500) * 2', '(3000 - 500)', 'brackets first')):
    s = Scene(w, h)
    colw = w / 2
    for i, (expr, first, why) in enumerate([left, right]):
        x = i * colw + 0.15
        val_first = eval(first)
        after = expr.replace(first, vstr(val_first))
        res = eval(expr)
        cx = x + (colw - 0.3) / 2
        s.text(cx, h - 0.4, expr, size=24, weight='bold', mono=True)
        s.box(cx - 1.65, h - 1.5, 3.3, 0.6, f'{first} = {vstr(val_first)}', size=17, mono=True, fill=GOLD, lw=1.8, r=0.05)
        s.text(cx, h - 1.8, why, size=17, color=RED, weight='bold')
        s.arrow(cx, h - 1.95, cx, h - 2.45, color=INK, lw=2.0)
        s.text(cx, h - 2.8, after, size=24, mono=True)
        s.arrow(cx, h - 3.1, cx, h - 3.6, color=INK, lw=2.0)
        s.box(cx - 1.0, h - 4.5, 2.0, 0.8, vstr(res), size=34, weight='bold', mono=True, fill=PAPER, lw=2.2, r=0.05)
    s.line(colw, 0.3, colw, h - 0.3, color=HAIR, lw=1.2)
    return s


@fig('c_error_anatomy')
def c_error_anatomy(w, h, error='ZeroDivisionError', message='division by zero', code='print(10 / 0)', line=1, hint='no number answers 10 divided by 0'):
    s = Scene(w, h)
    bx, bw = 0.15, w * 0.74
    s.box(bx, 0.55, bw, h - 0.85, '', fill=PAPER, edge=RED, lw=2.4, r=0.05)
    s.text(bx + 0.25, h - 0.7, 'Traceback (most recent call last)', size=14, mono=True, color=MUTE, ha='left')
    s.text(bx + 0.25, h - 1.35, f'Cell In[1], line {line}', size=15, mono=True, color=BODY, ha='left')
    s.text(bx + 0.25, h - 2.0, f'----> {line}  {code}', size=15, mono=True, ha='left')
    s.line(bx + 0.2, h - 2.5, bx + bw - 0.2, h - 2.5, color=HAIR, lw=1.2)
    last = f'{error}: {message}'
    es = 17 if len(last) <= 34 else 15
    s.text(bx + 0.25, h - 3.1, error, size=es, mono=True, weight='bold', color=RED, ha='left')
    s.text(bx + 0.25 + len(error) * es * MONO_EM / 72, h - 3.1, f': {message}', size=es, mono=True, color=INK, ha='left')
    s.box(bx + 0.12, h - 3.55, bw - 0.24, 0.9, '', fill='none', edge=GOLD, lw=3.0, r=0.04, z=4) if False else None
    ax = bx + bw + 0.0
    s.arrow(ax + 0.45, h - 3.1, bx + bw + 0.02, h - 3.1, color=RED, lw=2.4, head=17)
    s.text(ax + 0.55, h - 2.93, 'read this', size=19, weight='bold', ha='left')
    s.text(ax + 0.55, h - 3.27, 'line first', size=19, weight='bold', ha='left')
    s.arrow(ax + 0.45, h - 1.35, bx + bw + 0.02, h - 1.35, color=RED, lw=2.4, head=17)
    s.text(ax + 0.55, h - 1.18, 'then the', size=18, ha='left', color=BODY)
    s.text(ax + 0.55, h - 1.52, 'line number', size=18, ha='left', color=BODY)
    s.text(bx + 0.25, 0.28, hint, size=17, color=MUTE, ha='left')
    return s


@fig('c_divide_by_zero')
def c_divide_by_zero(w, h, coins=10, people=5):
    s = Scene(w, h)
    half = w / 2
    s.text(half / 2, h - 0.35, f'{coins} / {people}', size=30, weight='bold', mono=True)
    for i in range(people):
        x = 0.7 + i * (half - 1.2) / (people - 1)
        s.icon('person', x, h - 1.75, 0.95)
        for k in range(coins // people):
            s.icon('coin', x - 0.17 + k * 0.34, h - 3.05, 0.5, text='')
    s.text(half / 2, h - 3.85, f'each person gets {coins // people}', size=22, weight='bold')
    s.line(half, 0.3, half, h - 0.3, color=HAIR, lw=1.2)
    cx = half + half / 2
    s.text(cx, h - 0.35, f'{coins} / 0', size=30, weight='bold', mono=True)
    for k in range(coins):
        s.icon('coin', half + 0.6 + (k % 5) * 0.55, h - 1.5 - (k // 5) * 0.55, 0.5, text='')
    s.box(half + 0.6, h - 3.2, half - 1.2, 0.9, 'nobody to share with', size=17, fill=PAPER, lw=1.8, r=0.05, dash=True)
    s.icon('cross', cx, h - 3.9, 0.7)
    s.text(cx, 0.3, 'no answer, so Python stops', size=19, weight='bold', color=RED)
    return s


@fig('c_text_to_number')
def c_text_to_number(w, h, text='12.5', mult=4, name='price'):
    s = Scene(w, h)
    val = float(text)
    bw, gap = 2.4, 0.15
    arrow_l = (w - 0.4 - 3 * bw - 4 * gap) / 2
    y = h * 0.5
    xs = [0.2, 0.2 + bw + 2 * gap + arrow_l, 0.2 + 2 * (bw + 2 * gap + arrow_l)]
    s.box(xs[0], y - 0.55, bw, 1.1, f'"{text}"', size=fit_mono(f'"{text}"', bw, 34), weight='bold', mono=True, fill=GOLD, lw=2.2, r=0.05)
    s.text(xs[0] + bw / 2, y - 1.0, 'text', size=22, weight='bold')
    s.text(xs[0] + bw / 2, y - 1.4, 'in quotation marks', size=17, color=MUTE)
    s.arrow(xs[0] + bw + gap, y, xs[1] - gap, y, color=RED, lw=2.6, head=20)
    s.text(xs[0] + bw + gap + arrow_l / 2, y + 0.42, 'float()', size=22, weight='bold', color=RED, mono=True)
    s.box(xs[1], y - 0.55, bw, 1.1, vstr(val), size=fit_mono(vstr(val), bw, 34), weight='bold', mono=True, fill=PAPER, lw=2.2, r=0.05)
    s.text(xs[1] + bw / 2, y - 1.0, 'number', size=22, weight='bold')
    s.text(xs[1] + bw / 2, y - 1.4, 'Python can calculate', size=17, color=MUTE)
    s.arrow(xs[1] + bw + gap, y, xs[2] - gap, y, color=INK, lw=2.6, head=20)
    s.text(xs[1] + bw + gap + arrow_l / 2, y + 0.42, f'* {mult}', size=22, weight='bold', mono=True)
    s.box(xs[2], y - 0.55, bw, 1.1, vstr(val * mult), size=fit_mono(vstr(val * mult), bw, 34), weight='bold', mono=True, fill=GOLD, lw=2.2, r=0.05)
    s.text(xs[2] + bw / 2, y - 1.0, 'the total', size=22, weight='bold')
    s.text(w / 2, h - 0.45, 'Text that looks like a number has to be converted first', size=20, weight='bold')
    return s


@fig('c_first_three_sales')
def c_first_three_sales(w, h):
    d = shop().head(3)
    icons = {'Book': 'book', 'Pen': 'pen', 'Juice': 'bottle'}
    s = Scene(w, h)
    rh = (h - 2.0) / 3
    for i, r in enumerate(d.itertuples(index=False)):
        yc = h - 0.4 - (i + 0.5) * rh
        s.icon(icons[r.item], 0.9, yc, 0.9)
        s.text(1.8, yc, r.item, size=26, weight='bold', ha='left')
        s.text(4.2, yc, f'{r.units} * {r.unit_price_ugx}', size=26, mono=True, ha='left')
        s.arrow(7.0, yc, 7.7, yc, color=RED, lw=2.2, head=15)
        s.box(7.9, yc - 0.38, 1.9, 0.76, fmt(r.revenue), size=26, weight='bold', mono=True, fill=PAPER, lw=1.8, r=0.05)
    s.line(0.5, 1.3, w - 0.5, 1.3, color=INK, lw=2.0)
    s.text(1.8, 0.75, 'The three sales together', size=24, weight='bold', ha='left')
    s.box(7.9, 0.4, 1.9, 0.76, fmt(d.revenue.sum()), size=26, weight='bold', mono=True, fill=GOLD, lw=2.0, r=0.05)
    s.text(10.0, 0.78, 'UGX', size=20, color=MUTE, ha='left')
    s.text(w - 0.3, h - 0.45, '', size=1)
    return s


# ============================================================ session 4: decisions
@fig('c_edge_numberline')
def c_edge_numberline(w, h, threshold=5000, values=(4999, 5000, 5001), op='>=', yes='Buy', no='Save', var='budget'):
    s = Scene(w, h)
    ly = h * 0.5
    s.line(0.4, ly, w - 0.4, ly, color=INK, lw=2.4)
    xs = [w * (0.2 + 0.3 * i) for i in range(len(values))]
    cmp = {'>=': lambda a, b: a >= b, '>': lambda a, b: a > b, '<=': lambda a, b: a <= b, '<': lambda a, b: a < b}[op]
    mid = xs[1]
    s.line(mid, ly - 0.35, mid, ly + 0.35, color=RED, lw=2.8, z=3)
    s.text(mid, ly + 1.35, f'edge: {threshold}', size=20, weight='bold', color=RED)
    for x, v in zip(xs, values):
        ok = cmp(v, threshold)
        s.circle(x, ly, 0.22, fill=GOLD if v == threshold else PAPER, edge=INK, lw=2.4, z=4)
        s.text(x, ly - 0.55, str(v), size=24, weight='bold', mono=True)
        s.text(x, ly - 1.0, f'{var} {op} {threshold}', size=15, mono=True, color=MUTE)
        s.box(x - 0.6, ly - 2.0, 1.2, 0.6, str(ok), size=22, weight='bold', mono=True, fill=GOLD if ok else PAPER, lw=1.8, r=0.05)
        s.text(x, ly + 0.8, yes if ok else no, size=22, weight='bold')
    s.text(w / 2, 0.2, f'{op} includes the edge value itself', size=19, color=BODY) if op in ('>=', '<=') else None
    return s


@fig('c_decision_flow')
def c_decision_flow(w, h, conds=(('budget >= 5000', 'Buy'),), else_text='Save', code=('if budget >= 5000:', '    print("Buy")', 'else:', '    print("Save")'), size=18):
    """A question ladder. For a single condition the code sits on top; longer ladders stand alone."""
    s = Scene(w, h)
    n = len(conds)
    top = h - 0.15
    if code and n == 1:
        cb = Code(s, 0.15, h - 0.15, list(code), size=size)
        top = cb.bottom - 0.3
    longest = max([len(c[1]) for c in conds] + [len(else_text)])
    ow = min(3.4, max(2.0, longest * size * MONO_EM / 72 + 0.5))
    fx = 0.2
    qw = w - fx - ow - 1.3
    qh = 0.72
    avail = top - 0.1 - (n + 1) * qh
    gap = max(0.42, min(0.7, avail / n))
    ytop = top - 0.1
    for i, (cond, out) in enumerate(conds):
        yb = ytop - i * (qh + gap) - qh
        s.box(fx, yb, qw, qh, cond + ' ?', size=fit_mono(cond + ' ?', qw, size), weight='bold', mono=True, fill=PAPER, lw=2.2, r=0.06)
        s.arrow(fx + qw, yb + qh / 2, fx + qw + 1.0, yb + qh / 2, color=INK, lw=1.8, head=13)
        s.text(fx + qw + 0.5, yb + qh / 2 + 0.22, 'True', size=18, color=INK, weight='bold')
        s.box(fx + qw + 1.05, yb + 0.04, ow, qh - 0.08, out, size=fit_mono(out, ow, size - 1), weight='bold', mono=True, fill=GOLD, lw=1.8, r=0.05)
        s.arrow(fx + qw / 2, yb, fx + qw / 2, yb - gap, color=INK, lw=1.8, head=13)
        s.text(fx + qw / 2 + 0.12, yb - gap / 2, 'False', size=18, color=INK, weight='bold', ha='left')
    ye = ytop - n * (qh + gap)
    s.box(fx, ye - qh, qw, qh, else_text, size=fit_mono(else_text, qw, size - 1), weight='bold', mono=True, fill=GOLD, lw=1.8, r=0.05)
    return s


@fig('c_indentation')
def c_indentation(w, h, code=('if cost <= budget:', '    message = "Within budget"', 'else:', '    message = "Over budget"', 'print(message)'), blocks=((1, 1, 'runs when True'), (3, 3, 'runs when False'), (4, 4, 'runs every time'))):
    s = Scene(w, h)
    cb = Code(s, 0.15, h - 0.25, list(code), size=18, lead=1.8)
    for i, (a, b, lab) in enumerate(blocks):
        y0 = cb.y(a) - cb.lh * 0.42
        y1 = cb.y(b) + cb.lh * 0.42
        x0 = cb.px(4 if i < 2 else 0) - 0.08
        s.ax.add_patch(__import__('matplotlib').patches.Rectangle((x0, y0), cb.x0 + cb.w - 0.12 - x0, y1 - y0, fc='none', ec=GOLD, lw=2.4, zorder=6))
        s.arrow(cb.x0 + cb.w + 0.6, (y0 + y1) / 2, cb.x0 + cb.w + 0.05, (y0 + y1) / 2, color=RED, lw=2.2, head=15)
        s.text(cb.x0 + cb.w + 0.7, (y0 + y1) / 2, lab, size=18, weight='bold', ha='left')
    s.text(0.15, cb.bottom - 0.5, 'Four spaces mark the lines that belong to the if or the else.', size=18, ha='left', color=BODY)
    return s


@fig('c_and_or_table')
def c_and_or_table(w, h, a=('large', 'units >= 5', 6), b=('expensive', 'price >= 2000', 1000)):
    s = Scene(w, h)
    units, price = a[2], b[2]
    av = units >= 5
    bv = price >= 2000
    s.text(w / 2, h - 0.35, f'units = {units}   price = {price}', size=24, weight='bold', mono=True)
    s.text(w / 2, h - 0.8, f'{a[0]} is {av}    {b[0]} is {bv}', size=19, color=BODY)
    rows = [['large', 'expensive', 'and', 'or']]
    hl = {}
    for i, (x, y) in enumerate([(True, True), (True, False), (False, True), (False, False)], start=1):
        rows.append([str(x), str(y), str(x and y), str(x or y)])
        if (x, y) == (av, bv):
            for c in range(4):
                hl[(i, c)] = GOLD
    cw = [(w - 0.4) / 4] * 4
    s.table(0.2, h - 1.25, cw, 0.62, rows, size=20, mono_cols=(0, 1, 2, 3), hl_cells=hl)
    s.text(w / 2, 0.35, 'and needs both True. or needs at least one True.', size=19, color=BODY)
    return s


@fig('c_flower_zones')
def c_flower_zones(w, h, flowers=((1.4, 'setosa'), (1.4, 'setosa'), (4.7, 'versicolor'), (4.5, 'versicolor'), (4.9, 'versicolor'), (6.0, 'virginica'), (5.1, 'virginica'), (5.9, 'virginica')),
                   cuts=(2.5, 4.8), names=('setosa', 'versicolor', 'virginica'), verdict=False):
    s = Scene(w, h)
    x0, x1 = 0.7, w - 0.5
    vmin, vmax = 0.0, 7.0
    px = lambda v: x0 + (v - vmin) / (vmax - vmin) * (x1 - x0)
    ly = h * 0.36
    s.line(x0, ly, x1, ly, color=INK, lw=2.4)
    for t in range(0, 8):
        s.line(px(t), ly, px(t), ly - 0.1, color=INK, lw=1.6)
        s.text(px(t), ly - 0.36, str(t), size=17, color=BODY)
    s.text((x0 + x1) / 2, ly - 0.8, 'petal length (cm)', size=19)
    bounds = [vmin, cuts[0], cuts[1], vmax]
    guess = lambda v: names[0] if v < cuts[0] else (names[1] if v < cuts[1] else names[2])
    for i, nm in enumerate(names):
        a, b = px(bounds[i]), px(bounds[i + 1])
        s.box(a + 0.03, ly + 0.05, b - a - 0.06, 0.5, nm + (' zone' if False else ''), size=19, weight='bold', fill=PAPER, lw=1.6, r=0.03)
    for c in cuts:
        s.line(px(c), ly - 0.05, px(c), ly + 2.3, color=RED, lw=2.4, dash=True)
        s.text(px(c), ly + 2.58, str(c), size=19, weight='bold', color=RED)
    fills = {names[0]: PAPER, names[1]: GREY, names[2]: INK}
    levels = []
    right = 0
    for v, sp in sorted(flowers):
        lvl = next((i for i, lx_ in enumerate(levels) if px(v) - lx_ > 0.42), None)
        if lvl is None:
            levels.append(px(v))
            lvl = len(levels) - 1
        else:
            levels[lvl] = px(v)
        cy = ly + 0.95 + lvl * 0.42
        ok = guess(v) == sp
        right += ok
        s.circle(px(v), cy, 0.16, fill=fills[sp], edge=INK if ok else RED, lw=2.0 if ok else 3.4, z=4)
        if verdict and not ok:
            s.text(px(v) + 0.35, cy, 'wrong', size=16, color=RED, weight='bold', z=6, ha='left')
    lx = 0.7
    for i, nm in enumerate(names):
        s.circle(lx + i * 2.8, 0.28, 0.14, fill=fills[nm], edge=INK, lw=1.8)
        s.text(lx + i * 2.8 + 0.25, 0.28, f'true species: {nm}', size=15, ha='left', color=BODY)
    if verdict:
        s.text(w - 0.4, h - 0.4, f'{right} of {len(flowers)} right', size=30, weight='bold', ha='right')
    return s


@fig('c_large_order_bars')
def c_large_order_bars(w, h, n=12, threshold=5):
    d = shop().head(n)
    s = Scene(w, h)
    px, py = axes_xy(s, 1.1, 0.95, w - 1.5, h - 1.9, (0, n), (0, 10), xticks=[], yticks=[0, 2, 4, 6, 8, 10], ylabel='units', size=16)
    bw = (w - 1.5) / n * 0.62
    for i, r in enumerate(d.itertuples(index=False)):
        big = r.units >= threshold
        s.box(px(i + 0.5) - bw / 2, 0.95, bw, py(r.units) - 0.95, '', fill=GOLD if big else PAPER, lw=1.6, r=0.01)
        s.text(px(i + 0.5), py(r.units) + 0.2, str(r.units), size=16, weight='bold')
        s.text(px(i + 0.5), 0.65, str(r.sale_id), size=14, color=MUTE)
    s.line(1.1, py(threshold), w - 0.4, py(threshold), color=RED, lw=2.4, dash=True)
    s.text(w - 0.4, h - 0.8, f'dashed line: {threshold} units or more is a large order', size=18, color=RED, weight='bold', ha='right')
    s.text(1.1 + (w - 1.5) / 2, 0.3, 'sale number', size=16, color=BODY)
    s.text(w / 2, h - 0.35, f'The first {n} sales: gold bars pass the line', size=20, weight='bold')
    return s


# ============================================================ session 5: lists, dictionaries, loops
@fig('c_bus_seats')
def c_bus_seats(w, h, values=None, name='units', pointer=3, code_ex=None):
    if values is None:
        values = [int(v) for v in shop().units.head(6)]
    s = Scene(w, h)
    n = len(values)
    cb = Code(s, 0.15, h - 0.2, [f'{name} = {values}'.replace("'", '"'), f'{name}[{pointer}]'], size=19)
    s.arrow(cb.x0 + cb.w + 0.15, cb.y(1), cb.x0 + cb.w + 0.9, cb.y(1), color=RED, lw=2.4, head=16)
    s.box(cb.x0 + cb.w + 1.0, cb.y(1) - 0.3, 1.1, 0.6, str(values[pointer]), size=24, weight='bold', mono=True, fill=GOLD, lw=2.0, r=0.05)
    bw = min(1.05, (w - 0.6) / n)
    x0 = (w - n * bw) / 2
    by = 1.0
    s.box(x0 - 0.2, by - 0.2, n * bw + 0.4, bw + 0.9, '', fill=PAPER, lw=2.2, r=0.18, z=1)
    s.text(x0 - 0.05, by + bw + 0.45, 'the bus', size=16, color=MUTE, ha='left')
    for i, v in enumerate(values):
        s.box(x0 + i * bw + 0.05, by + 0.35, bw - 0.1, bw - 0.1, str(v), size=26, weight='bold', mono=True, fill=GOLD if i == pointer else PAPER, lw=2.0, r=0.05, z=3)
        s.text(x0 + i * bw + bw / 2, by + 0.0, str(i), size=22, weight='bold', color=RED if i == pointer else INK)
    s.text(w / 2, 0.38, 'seats are numbered from 0, so the first value sits at seat 0', size=18, color=BODY)
    return s


@fig('c_dict_board')
def c_dict_board(w, h, mapping=None, key='Pen', name='prices'):
    if mapping is None:
        mapping = {'Book': 3000, 'Pen': 1000, 'Juice': 2000}
    s = Scene(w, h)
    code_line = f'{name}["{key}"]'
    cb = Code(s, 0.15, h - 0.2, [code_line], size=22)
    s.arrow(cb.x0 + cb.w + 0.15, cb.y(0), cb.x0 + cb.w + 0.9, cb.y(0), color=RED, lw=2.4, head=16)
    s.box(cb.x0 + cb.w + 1.0, cb.y(0) - 0.3, 1.3, 0.6, str(mapping[key]), size=24, weight='bold', mono=True, fill=GOLD, lw=2.0, r=0.05)
    n = len(mapping)
    rh = min(0.75, (h - 2.3) / n)
    bx, bw = w * 0.15, w * 0.7
    top = h - 1.2
    s.box(bx, top - n * rh - 0.7, bw, n * rh + 0.7, '', fill=PAPER, lw=2.4, r=0.05, z=1)
    s.text(bx + bw / 2, top - 0.3, 'price board', size=20, weight='bold')
    s.text(bx + 0.5, top - 0.3 - 0.0, '', size=1)
    for i, (k, v) in enumerate(mapping.items()):
        yy = top - 0.7 - (i + 1) * rh
        hit = k == key
        s.line(bx + 0.2, yy + rh, bx + bw - 0.2, yy + rh, color=HAIR, lw=1.2, z=2)
        s.box(bx + 0.3, yy + 0.1, bw * 0.4, rh - 0.2, f'"{k}"', size=20, mono=True, fill=GOLD if hit else PAPER, lw=1.8, r=0.04, z=3)
        s.text(bx + 0.3 + bw * 0.4 + 0.25, yy + rh / 2, 'is', size=17, color=MUTE, ha='left')
        s.text(bx + bw - 0.4, yy + rh / 2, str(v), size=22, weight='bold', mono=True, ha='right', z=3)
    s.text(0.2, 0.25, 'a dictionary finds a value by its name (the key), not by a seat number', size=17, color=BODY, ha='left') if False else None
    s.text(w / 2, 0.22, 'a dictionary finds a value by its key', size=18, color=BODY)
    return s


@fig('c_loop_trace')
def c_loop_trace(w, h, values=None, var='u'):
    if values is None:
        values = [int(v) for v in shop().units.head(6)]
    s = Scene(w, h)
    cum = list(np.cumsum(values))
    rows = [['pass', var, 'total before', 'total after']]
    prev = 0
    for i, (v, c) in enumerate(zip(values, cum), start=1):
        rows.append([str(i), str(v), str(prev), str(int(c))])
        prev = int(c)
    cw = [0.8, 0.8, 1.55, 1.5]
    rh = 0.52
    hl = {(i, 3): GOLD for i in range(1, len(rows))}
    s.table(0.1, h - 0.45, cw, rh, rows, size=17, hl_cells=hl)
    s.text(0.1 + sum(cw) / 2, h - 0.2, 'what the loop does, pass by pass', size=18, weight='bold')
    bx0 = 0.1 + sum(cw) + 0.7
    bw = w - bx0 - 0.15
    px, py = axes_xy(s, bx0, 0.9, bw, h - 2.0, (0, len(values)), (0, max(cum) * 1.05), xticks=[], yticks=[0, int(max(cum))], size=15)
    for i, c in enumerate(cum):
        bwid = bw / len(values) * 0.6
        s.box(px(i + 0.5) - bwid / 2, 0.9, bwid, py(c) - 0.9, '', fill=GOLD if i == len(values) - 1 else PAPER, lw=1.6, r=0.01)
        s.text(px(i + 0.5), 0.62, str(i + 1), size=15, color=BODY)
    s.text(bx0 + bw / 2, h - 0.55, 'total after each pass', size=16, color=BODY) if False else None
    s.text(bx0 + bw / 2, 0.25, 'pass', size=15, color=MUTE)
    s.text(bx0 + bw / 2, h - 0.85, 'the total grows', size=17, weight='bold')
    return s


@fig('c_loop_anatomy')
def c_loop_anatomy(w, h, code=('total = 0', 'for u in units:', '    total = total + u', 'print(total)'), var='u'):
    s = Scene(w, h)
    cb = Code(s, 0.15, h - 0.2, list(code), size=18, lead=1.9)
    right = cb.x0 + cb.w
    notes = ['start the counter at 0', f'one at a time, called {var}', 'repeats for every value', 'runs once, at the end']
    for i, text in enumerate(notes):
        yy = cb.y(i)
        s.arrow(right + 0.55, yy, right + 0.05, yy, color=RED, lw=2.0, head=14)
        s.text(right + 0.65, yy, text, size=16, ha='left')
    c0 = code[1].index(var)
    cb.mark(1, c0, c0 + len(var))
    return s


@fig('c_reset_pair')
def c_reset_pair(w, h, inside=False, values=None):
    if values is None:
        values = [int(v) for v in shop().units.head(6)]
    s = Scene(w, h)
    code = ['for u in units:', '    total = 0', '    total = total + u'] if inside else ['total = 0', 'for u in units:', '    total = total + u']
    cb = Code(s, 0.1, h - 0.15, code, size=16)
    totals, t = [], 0
    for u in values:
        if inside:
            t = 0
        t = t + u
        totals.append(t)
    s.text(0.15, cb.bottom - 0.4, 'total after each pass', size=17, ha='left', color=BODY)
    n = len(values)
    bw = (w - 0.3) / n
    for i, v in enumerate(totals):
        s.box(0.15 + i * bw + 0.04, cb.bottom - 1.45, bw - 0.08, 0.7, str(v), size=22, weight='bold', mono=True, fill=GOLD if i == n - 1 else PAPER, lw=1.8, r=0.04)
    s.text(w / 2, cb.bottom - 1.9, f'final total: {totals[-1]}', size=24, weight='bold', color=RED if inside else INK)
    return s


@fig('c_six_sales_total')
def c_six_sales_total(w, h):
    d = shop().head(6)
    icons = {'Book': 'book', 'Pen': 'pen', 'Juice': 'bottle'}
    s = Scene(w, h)
    n = len(d)
    step = (w - 2.6) / n
    for i, r in enumerate(d.itertuples(index=False)):
        x = 0.7 + i * step
        s.icon('receipt', x + 0.0, h - 1.5, 1.15)
        s.icon(icons[r.item], x + 0.0, h - 1.5, 0.0) if False else None
        s.text(x, h - 2.45, r.item, size=18, color=MUTE)
        s.box(x - 0.4, h - 3.6, 0.8, 0.8, str(r.units), size=28, weight='bold', mono=True, fill=PAPER, lw=2.0, r=0.05)
        if i < n - 1:
            s.text(x + step / 2, h - 3.2, '+', size=28, weight='bold')
    s.text(w - 1.3, h - 3.2, '=', size=34, weight='bold')
    s.box(w - 1.0, h - 3.65, 0.9, 0.9, str(int(d.units.sum())), size=32, weight='bold', mono=True, fill=GOLD, lw=2.2, r=0.05)
    s.text(w - 0.55, h - 2.45, 'units in all', size=17, color=MUTE)
    s.text(w / 2, h - 0.4, 'The units of the first six sales', size=22, weight='bold')
    s.text(w / 2, 0.45, 'Adding them one at a time is what a loop will do for us', size=20, color=BODY)
    return s


@fig('c_repeat_machine')
def c_repeat_machine(w, h, values=(1000, 2000, 3000), op='* 2', name='price'):
    s = Scene(w, h)
    n = len(values)
    mx, mw = w * 0.38, w * 0.24
    s.box(mx, h * 0.18, mw, h * 0.6, '', fill=PAPER, lw=2.6, r=0.1)
    s.text(mx + mw / 2, h * 0.58, op, size=40, weight='bold', mono=True)
    s.text(mx + mw / 2, h * 0.36, 'the same\nstep every time', size=18, color=BODY)
    for i, v in enumerate(values):
        yy = h * 0.8 - i * (h * 0.58 / max(1, n - 1)) if n > 1 else h * 0.5
        s.icon('tag', 1.2, yy, 0.0) if False else None
        s.box(0.4, yy - 0.32, 1.6, 0.64, str(v), size=24, weight='bold', mono=True, fill=GOLD, lw=1.8, r=0.05)
        s.arrow(2.1, yy, mx - 0.05, yy, color=INK, lw=1.8, head=13)
        s.arrow(mx + mw + 0.05, yy, w - 2.1, yy, color=INK, lw=1.8, head=13)
        s.box(w - 2.0, yy - 0.32, 1.6, 0.64, str(eval(f'{v} {op}')), size=24, weight='bold', mono=True, fill=PAPER, lw=1.8, r=0.05)
    s.text(1.2, h - 0.2, 'one at a time in', size=18, color=BODY, va='top')
    s.text(w - 1.2, h - 0.2, 'one at a time out', size=18, color=BODY, va='top')
    s.text(w / 2, 0.3, f'for {name} in {name}s:  the loop feeds each item through the machine', size=19, mono=False)
    return s


# ============================================================ session 6: functions
@fig('c_function_machine')
def c_function_machine(w, h, name='revenue', params=('units', 'price'), args=(3, 2000), body='units * price', result=None, show_code=True,
                       code=('def revenue(units, price):', '    return units * price')):
    s = Scene(w, h)
    if result is None:
        result = vstr(eval(body, dict(zip(params, args))))
    cy0 = (1.9 if show_code else 0.4)
    mh = h - cy0 - 0.35
    mx, mw = w * 0.31, w * 0.4
    s.box(mx, cy0, mw, mh, '', fill=PAPER, lw=2.6, r=0.1)
    s.text(mx + mw / 2, cy0 + mh * 0.68, name, size=22 if w < 9 else 28, weight='bold', mono=True)
    s.text(mx + mw / 2, cy0 + mh * 0.35, f'return {body}' if len(body) < 22 else body, size=15 if w < 9 else 19, mono=True, color=BODY)
    n = len(params)
    for i, (pn, av) in enumerate(zip(params, args)):
        yy = cy0 + mh * (0.5 + (0.22 if n > 1 else 0) * (1 - 2 * i / max(1, n - 1)) if n > 1 else 0.5)
        s.box(0.2, yy - 0.32, w * 0.13, 0.64, vstr(av) if not isinstance(av, str) else av, size=20, weight='bold', mono=True, fill=GOLD, lw=1.8, r=0.05)
        s.arrow(0.25 + w * 0.13, yy, mx - 0.02, yy, color=INK, lw=2.0, head=14)
        s.text((0.25 + w * 0.13 + mx) / 2, yy + 0.28, pn, size=16, mono=True, color=RED, weight='bold')
    s.text(0.1, cy0 + mh * 0.5, 'arguments in', size=16, color=BODY, ha='left')
    s.arrow(mx + mw + 0.02, cy0 + mh / 2, w - 0.2 - w * 0.17, cy0 + mh / 2, color=INK, lw=2.0, head=14)
    s.box(w - 0.2 - w * 0.17, cy0 + mh / 2 - 0.4, w * 0.17, 0.8, result, size=20 if len(result) > 6 else 24, weight='bold', mono=True, fill=PAPER, lw=2.0, r=0.05)
    s.text(w - 0.2 - w * 0.085, cy0 + mh / 2 + 0.55, 'answer back', size=16, color=MUTE)
    if show_code:
        Code(s, 0.15, 1.45, list(code), size=16)
    return s


def under(s, code, line, c0, c1):
    """A thick gold bar under characters c0..c1 of a code line (never touches neighbouring characters)."""
    x0, x1 = code.span(line, c0, c1)
    yy = code.y(line) - code.lh * 0.36
    s.line(x0 + 0.02, yy, x1 - 0.02, yy, color=GOLD, lw=5.0, z=7)


@fig('c_function_anatomy')
def c_function_anatomy(w, h, name='revenue', params=('units', 'price'), args=(3, 2000), body='units * price'):
    s = Scene(w, h)
    d0 = f'def {name}({", ".join(params)}):'
    c3 = f'result = {name}({", ".join(str(a) for a in args)})'
    code = [d0, f'    return {body}', '', c3]
    cb = Code(s, 0.15, h - 0.3, code, size=18, lead=2.8)
    right = cb.x0 + cb.w
    p0 = len(f'def {name}(')
    under(s, cb, 0, p0, p0 + len(', '.join(params)))
    a0 = len(f'result = {name}(')
    under(s, cb, 3, a0, a0 + len(', '.join(str(a) for a in args)))
    items = [(0, 'parameters', 'names for the inputs'), (1, 'return', 'sends the answer back'), (3, 'arguments', 'the real values')]
    for line, head, sub in items:
        yy = cb.y(line)
        s.arrow(right + 0.7, yy, right + 0.05, yy, color=RED, lw=2.2, head=15)
        s.text(right + 0.8, yy + 0.14, head, size=20, weight='bold', ha='left')
        s.text(right + 0.8, yy - 0.2, sub, size=16, color=MUTE, ha='left')
    s.text(0.15, cb.bottom - 0.45, 'The def line describes the machine. The last line uses it.', size=18, ha='left', color=BODY)
    return s


@fig('c_return_vs_print')
def c_return_vs_print(w, h):
    s = Scene(w, h)
    colw = w / 2
    specs = [('return', ['def f(x):', '    return x * 2', 'a = f(4)'], 'a'), ('print', ['def g(x):', '    print(x * 2)', 'b = g(4)'], 'b')]
    for i, (kind, code, var) in enumerate(specs):
        x = i * colw + 0.1
        cb = Code(s, x, h - 0.15, code, size=16)
        ns = {}
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            exec('\n'.join(code), ns)
        shown = buf.getvalue().strip()
        s.text(x + 0.05, cb.bottom - 0.4, 'on the screen:', size=16, color=MUTE, ha='left')
        s.box(x + 1.75, cb.bottom - 0.65, 1.2, 0.5, shown, size=20, mono=True, fill=PAPER if not shown else GOLD, lw=1.6, r=0.04)
        s.text(x + 0.05, cb.bottom - 1.2, f'{var} holds:', size=16, color=MUTE, ha='left')
        s.box(x + 1.75, cb.bottom - 1.45, 1.2, 0.5, str(ns[var]), size=20, mono=True, fill=GOLD if ns[var] is not None else PAPER, lw=1.6, r=0.04, edge=INK if ns[var] is not None else RED)
        s.text(x + colw / 2 - 0.1, 0.45, 'return gives the value back' if kind == 'return' else 'print only shows it', size=18, weight='bold', color=INK if kind == 'return' else RED)
    s.line(colw, 0.3, colw, h - 0.3, color=HAIR, lw=1.2)
    return s


@fig('c_assert_checks')
def c_assert_checks(w, h, name='revenue', argnames=('units', 'price'), cases=(((3, 2000), 6000), ((0, 2000), 0), ((5, 1000), 5000)), good='units * price', bad='units + price', show_fail=True):
    s = Scene(w, h)
    rows = [['call', 'expected', 'got', 'passes?']]
    marks = []
    allc = list(cases)
    for (args, exp) in allc:
        got = eval(good, dict(zip(argnames, args)))
        rows.append([f'{name}({", ".join(str(a) for a in args)})', str(exp), vstr(got), ''])
        marks.append(got == exp)
    if show_fail:
        args, exp = allc[0]
        got = eval(bad, dict(zip(argnames, args)))
        rows.append([f'{name}({", ".join(str(a) for a in args)}) bug', str(exp), vstr(got), ''])
        marks.append(got == exp)
    cw = [w * 0.42, w * 0.19, w * 0.19, w * 0.2 - 0.0]
    cw = [c * (w - 0.3) / sum(cw) for c in cw]
    rh = min(0.7, (h - 1.4) / len(rows))
    hl = {(len(rows) - 1, c): PAPER for c in range(4)}
    s.table(0.15, h - 0.2, cw, rh, rows, size=18 if w > 9 else 16, mono_cols=(0, 1, 2), align=['left', 'center', 'center', 'center'])
    x_icon = 0.15 + sum(cw[:3]) + cw[3] / 2
    for i, ok in enumerate(marks, start=1):
        s.icon('check' if ok else 'cross', x_icon, h - 0.2 - (i + 0.5) * rh, 0.5)
    s.text(w / 2, 0.55, 'A passing assert says nothing. A failing assert stops with AssertionError.', size=19 if w > 9 else 17, color=BODY)
    return s


@fig('c_flower_scoreboard')
def c_flower_scoreboard(w, h, flowers=((1.4, 'setosa'), (1.4, 'setosa'), (4.7, 'versicolor'), (4.5, 'versicolor'), (4.9, 'versicolor'), (6.0, 'virginica'), (5.1, 'virginica'), (5.9, 'virginica'))):
    def guess_species(p):
        return 'setosa' if p < 2.5 else ('versicolor' if p < 4.8 else 'virginica')
    s = Scene(w, h)
    n = len(flowers)
    labw = 1.9
    cw = (w - labw - 0.3) / n
    rows = ['petal length', 'true species', 'rule says', 'right?']
    rh = (h - 1.2) / 4
    right = 0
    for r, lab in enumerate(rows):
        y = h - 0.3 - (r + 1) * rh
        s.text(0.2, y + rh / 2, lab, size=19, weight='bold', ha='left')
        s.line(0.15, y, w - 0.15, y, color=HAIR, lw=1.2)
    for i, (p, sp) in enumerate(flowers):
        x = 0.15 + labw + i * cw
        g = guess_species(p)
        ok = g == sp
        right += ok
        vals = [str(p), sp, g, '']
        for r, v in enumerate(vals):
            y = h - 0.3 - (r + 1) * rh
            if r == 3:
                s.icon('check' if ok else 'cross', x + cw / 2, y + rh / 2, 0.55)
            else:
                s.text(x + cw / 2, y + rh / 2, v, size=17 if r else 20, color=INK if (r != 2 or ok) else RED, weight='bold' if r == 2 else 'normal', mono=(r == 0))
    s.text(w / 2, 0.4, f'{right} of {n} flowers named correctly', size=26, weight='bold')
    return s


# ============================================================ machine learning session 1 and the labs
def draw_house(s, x, y, size=1.0, fill=PAPER):
    s.poly([(x - 0.5 * size, y - 0.1 * size), (x, y + 0.42 * size), (x + 0.5 * size, y - 0.1 * size)], fill=GOLD, edge=INK, lw=2)
    s.rect(x - 0.4 * size, y - 0.45 * size, 0.8 * size, 0.38 * size, fill=fill, edge=INK, lw=2)
    s.rect(x - 0.09 * size, y - 0.45 * size, 0.18 * size, 0.3 * size, fill=PAPER, edge=INK, lw=1.6)


def homes():
    return pd.read_csv(DATA / 'synthetic_homes.csv')


def fit_line():
    d = homes()
    m, b = np.polyfit(d.area_m2, d.rent_ugx, 1)
    return d, m, b


def scatter_axes(s, x, y, w, h, line=False, mark=None, size=15, ylab=True, xlab=True):
    d, m, b = fit_line()
    px, py = axes_xy(s, x, y, w, h, (0, 200), (0, 800000), xticks=[0, 50, 100, 150, 200], yticks=[0, 200000, 400000, 600000, 800000],
                     xlabel='floor area (m²)' if xlab else '', ylabel='rent (UGX)' if ylab else '', size=size, yfmt=lambda v: f'{int(v / 1000)}k')
    for a, r in zip(d.area_m2, d.rent_ugx):
        s.circle(px(a), py(r), 0.045, fill=GREY, edge=INK, lw=0.6, z=3)
    if line:
        s.line(px(0), py(b), px(200), py(m * 200 + b), color=RED, lw=3.0, z=5)
    if mark is not None:
        pred = m * mark + b
        s.line(px(mark), y, px(mark), py(pred), color=INK, lw=1.8, dash=True, z=4)
        s.line(x, py(pred), px(mark), py(pred), color=INK, lw=1.8, dash=True, z=4)
        s.circle(px(mark), py(pred), 0.13, fill=GOLD, edge=INK, lw=2.4, z=7)
        return px, py, pred
    return px, py, None


@fig('c_prediction_guess')
def c_prediction_guess(w, h):
    d = homes().head(6)
    s = Scene(w, h)
    s.text(1.7, h - 0.3, 'homes we know', size=22, weight='bold')
    rows = [['area_m2', 'rent_ugx']] + [[str(a), f'{r:,}'] for a, r in zip(d.area_m2, d.rent_ugx)]
    s.table(0.2, h - 0.6, [1.4, 1.9], 0.46, rows, size=16)
    s.text(1.7, h - 0.6 - 7 * 0.46 - 0.25, '... and 114 more homes', size=17, color=MUTE)
    s.arrow(3.75, h * 0.5, 4.9, h * 0.5, color=RED, lw=2.6, head=18)
    s.text(4.33, h * 0.5 + 0.55, 'look for', size=17, color=BODY)
    s.text(4.33, h * 0.5 + 0.3, 'a pattern', size=17, color=BODY)
    draw_house(s, 6.3, h * 0.62, 1.5)
    s.text(6.3, h * 0.62 - 0.85, 'a new home', size=20, weight='bold')
    s.text(6.3, h * 0.62 - 1.2, '50 m²', size=20, mono=True)
    s.box(5.6, 0.5, 1.4, 0.8, 'rent?', size=24, weight='bold', fill=GOLD, lw=2.2, r=0.06)
    s.arrow(6.3, h * 0.62 - 1.5, 6.3, 1.35, color=INK, lw=1.8, head=14)
    return s


@fig('c_scatter_line')
def c_scatter_line(w, h, area=50, with_line=True):
    s = Scene(w, h)
    px, py, pred = scatter_axes(s, 1.35, 0.95, w - 1.75, h - 1.5, line=with_line, mark=area)
    s.text(px(area) + 0.4, py(pred) - 0.55, f'{area} m²: UGX {round(pred):,}', size=19, weight='bold', ha='left', color=INK)
    s.text(w / 2 + 0.4, h - 0.25, '120 homes and the line drawn through them', size=19, weight='bold')
    return s


@fig('c_prediction_pipeline')
def c_prediction_pipeline(w, h):
    s = Scene(w, h)
    cw = (w - 0.4) / 3
    stages = [('120 homes we know', False, None), ('the computer learns a line', True, None), ('a guess for a new home', True, 50)]
    for i, (cap, line, mark) in enumerate(stages):
        x = 0.2 + i * cw
        if i < 2:
            scatter_axes(s, x + 0.95, 0.95, cw - 1.45, h - 2.05, line=line, mark=None, size=13, ylab=False, xlab=False)
            s.text(x + 0.95 + (cw - 1.45) / 2, 0.38, 'area  to  rent', size=15, color=MUTE)
        else:
            cx = x + cw / 2
            draw_house(s, cx, h - 1.55, 1.4)
            s.text(cx, h - 2.5, '50 m²', size=22, mono=True, weight='bold')
            s.arrow(cx, h - 2.75, cx, h - 3.1, color=RED, lw=2.4, head=16)
            d, m, b = fit_line()
            s.box(cx - 1.15, h - 3.85, 2.3, 0.8, f'{round(m * 50 + b):,}', size=22, weight='bold', mono=True, fill=GOLD, lw=2.2, r=0.06)
            s.text(cx, h - 4.2, 'UGX a month', size=16, color=MUTE)
        s.text(x + cw / 2, h - 0.3, cap, size=20, weight='bold')
        if i < 2:
            s.arrow(x + cw - 0.45, h * 0.5, x + cw + 0.15, h * 0.5, color=RED, lw=2.6, head=18)
    return s


@fig('c_model_code_map')
def c_model_code_map(w, h):
    code = ['import pandas as pd', 'from sklearn.linear_model import LinearRegression', 'homes = pd.read_csv("synthetic_homes.csv")',
            'model = LinearRegression().fit(homes[["area_m2"]], homes["rent_ugx"])', 'pred = model.predict(pd.DataFrame({"area_m2": [50]}))[0]',
            'print("Estimated rent for 50 square metres:", round(pred))']
    s = Scene(w, h)
    cb = Code(s, 2.55, h - 0.2, code, size=15, lead=2.6)
    jobs = [((0, 1), 'get the tools'), ((2, 2), 'read the data'), ((3, 3), 'learn'), ((4, 4), 'guess'), ((5, 5), 'show it')]
    for (a, b), lab in jobs:
        y0, y1 = cb.y(a) + cb.lh * 0.4, cb.y(b) - cb.lh * 0.4
        s.line(2.4, y0, 2.4, y1, color=RED, lw=3.0)
        s.text(2.25, (y0 + y1) / 2, lab, size=18, weight='bold', ha='right')
    return s


@fig('c_three_pens')
def c_three_pens(w, h, n=3, price=1000):
    s = Scene(w, h)
    step = (w - 3.0) / n
    for i in range(n):
        x = 0.9 + i * step
        s.icon('pen', x, h - 1.55, 1.5)
        s.box(x - 0.55, h - 2.85, 1.1, 0.6, f'{price:,}', size=19, weight='bold', mono=True, fill=GOLD, lw=1.8, r=0.05)
        if i < n - 1:
            s.text(x + step / 2, h - 2.55, '+', size=30, weight='bold')
    s.text(w - 1.75, h - 2.55, '=', size=34, weight='bold')
    s.box(w - 1.4, h - 2.95, 1.3, 0.8, f'{n * price:,}', size=22, weight='bold', mono=True, fill=GOLD, lw=2.2, r=0.05)
    s.text(w / 2, h - 0.3, f'{n} pens at UGX {price:,} each', size=22, weight='bold')
    s.text(w / 2, 1.05, f'{n} * {price} = {n * price}', size=30, mono=True, weight='bold')
    s.text(w / 2, 0.45, 'multiplying is a quick way to add the same number again and again', size=18, color=BODY)
    return s


@fig('c_predict_paper')
def c_predict_paper(w, h, code=('units = 3', 'price = 1000', 'total = units * price', 'print(total)', 'print(total / units)', 'print("1000")', 'units = 4', 'print(total)', 'total = units * price', 'print(total)'), filled=2):
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec('\n'.join(code), {})
    outs = buf.getvalue().strip().split('\n')
    s = Scene(w, h)
    cb = Code(s, 0.1, h - 0.15, list(code), size=15, lead=1.45)
    px0 = cb.x0 + cb.w + 0.4
    pw = w - px0 - 0.1
    s.box(px0, 0.35, pw, h - 0.65, '', fill=PAPER, lw=2.2, r=0.04)
    s.text(px0 + pw / 2, h - 0.65, 'my prediction on paper', size=20, weight='bold')
    n = len(outs)
    rh = (h - 1.6) / n
    for i in range(n):
        yy = h - 1.2 - (i + 0.5) * rh
        s.line(px0 + 0.25, yy - rh / 2 + 0.05, px0 + pw - 0.25, yy - rh / 2 + 0.05, color=HAIR, lw=1.2)
        s.text(px0 + 0.4, yy, f'{i + 1}', size=16, color=MUTE, ha='left')
        if i < filled:
            s.text(px0 + 1.0, yy, outs[i], size=19, mono=True, ha='left')
    s.icon('pen', px0 + pw - 0.55, 0.9, 0.9)
    return s


@fig('c_vector_order')
def c_vector_order(w, h):
    s = Scene(w, h)
    half = w / 2
    for i, (vals, ok) in enumerate([((40, 2), True), ((2, 40), False)]):
        cx = i * half + half / 2
        draw_house(s, cx, h - 1.2, 1.4)
        s.text(cx, h - 2.05, 'a home with' if ok else 'swap the numbers', size=19, color=MUTE)
        for k, v in enumerate(vals):
            bx = cx - 1.55 + k * 1.6
            s.text(bx + 0.65, h - 2.45, ['area_m2', 'rooms'][k], size=17, mono=True, color=BODY)
            s.box(bx, h - 3.55, 1.3, 0.8, str(v), size=30, weight='bold', mono=True, fill=GOLD if ok else PAPER, lw=2.2, r=0.04, edge=INK if ok else RED)
        s.icon('check' if ok else 'cross', cx - 2.0, 0.6, 0.6)
        s.text(cx + 0.2, 0.6, '40 m² and 2 rooms' if ok else '2 m² and 40 rooms', size=19, color=INK if ok else RED, weight='bold')
    s.line(half, 0.3, half, h - 0.3, color=HAIR, lw=1.2)
    return s


@fig('c_list_vs_array_add')
def c_list_vs_array_add(w, h, mode='list'):
    s = Scene(w, h)
    a, b = [40, 2], [10, 1]
    bh = 0.6
    if mode == 'list':
        s.text(w / 2, h - 0.3, '[40, 2] + [10, 1]', size=22, mono=True, weight='bold')
        res = a + b
        x0 = w / 2 - 2 * 0.95
        for i, v in enumerate(a + b):
            s.box(x0 + i * 0.95 + (0.3 if i >= 2 else 0), h - 1.35, 0.85, bh, str(v), size=21, weight='bold', mono=True, lw=2.0, r=0.04)
        s.text(w / 2, h - 1.75, 'the lists are joined', size=18, color=BODY)
        s.arrow(w / 2, h - 1.95, w / 2, h - 2.35, color=RED, lw=2.2)
        for i, v in enumerate(res):
            s.box(x0 + i * 0.95, h - 3.0, 0.85, bh, str(v), size=21, weight='bold', mono=True, fill=GOLD, lw=2.0, r=0.04)
        s.text(w / 2, 0.35, f'{len(res)} values: nothing was added', size=19, weight='bold', color=RED)
    else:
        s.text(w / 2, h - 0.3, 'array([40, 2]) + array([10, 1])', size=18, mono=True, weight='bold')
        res = list(np.array(a) + np.array(b))
        for i in range(2):
            x = w / 2 - 1.3 + i * 1.5
            s.box(x, h - 1.1, 1.1, 0.55, str(a[i]), size=21, weight='bold', mono=True, lw=2.0, r=0.04)
            s.text(x + 0.55, h - 1.27, '+', size=22, weight='bold')
            s.box(x, h - 2.0, 1.1, 0.55, str(b[i]), size=21, weight='bold', mono=True, lw=2.0, r=0.04)
            s.arrow(x + 0.55, h - 2.1, x + 0.55, h - 2.45, color=RED, lw=2.2)
            s.box(x, h - 3.1, 1.1, 0.55, str(res[i]), size=21, weight='bold', mono=True, fill=GOLD, lw=2.0, r=0.04)
        s.text(w / 2, 0.3, 'matching places are added', size=19, weight='bold')
    return s


@fig('c_array_scale')
def c_array_scale(w, h):
    s = Scene(w, h)
    a = np.array([40, 2])
    s.text(w / 2, h - 0.3, 'home_array * 2', size=26, mono=True, weight='bold')
    for i, v in enumerate(a):
        x = w / 2 - 2.1 + i * 2.5
        s.box(x, h - 1.8, 1.3, 0.85, str(v), size=28, weight='bold', mono=True, lw=2.2, r=0.04)
        s.text(x + 0.65, h - 2.3, ['area_m2', 'rooms'][i], size=16, mono=True, color=MUTE)
        s.arrow(x + 0.65, h - 2.65, x + 0.65, h - 3.15, color=RED, lw=2.4, label='* 2', label_dx=0.55, label_dy=0, label_size=18)
        s.box(x, h - 4.1, 1.3, 0.85, str(int(v * 2)), size=28, weight='bold', mono=True, fill=GOLD, lw=2.2, r=0.04)
    s.text(w / 2, 0.3, f'shape {a.shape}: one row of {a.shape[0]} numbers; every number is doubled', size=18, color=BODY)
    return s


@fig('c_units_mismatch')
def c_units_mismatch(w, h):
    s = Scene(w, h)
    y = h - 1.9
    s.box(0.2, y, 2.0, 1.0, '40 m²', size=28, weight='bold', fill=PAPER, lw=2.2, r=0.05)
    s.text(2.5, y + 0.5, '+', size=36, weight='bold')
    s.box(2.8, y, 2.0, 1.0, '2 rooms', size=28, weight='bold', fill=PAPER, lw=2.2, r=0.05)
    s.text(5.1, y + 0.5, '=', size=36, weight='bold')
    s.box(5.4, y, 1.8, 1.0, '42 ?', size=28, weight='bold', fill=PAPER, lw=2.2, r=0.05, edge=RED, color=RED)
    s.text(w / 2, h - 3.0, 'Add area to area and rooms to rooms.', size=22, weight='bold')
    s.text(w / 2, h - 3.65, 'Write the unit beside every number you store.', size=19, color=BODY)
    return s


@fig('c_comment_demo')
def c_comment_demo(w, h):
    s = Scene(w, h)
    code = ['# The price came in as text', 'text_price = "12.5"', 'price = float(text_price)', 'total = price * 4', 'print(total)']
    cb = Code(s, 0.15, h - 0.25, code, size=18, lead=1.8)
    right = cb.x0 + cb.w
    s.arrow(right + 0.7, cb.y(0), right + 0.05, cb.y(0), color=RED, lw=2.2, head=15)
    s.text(right + 0.8, cb.y(0) + 0.14, 'comment', size=20, weight='bold', ha='left')
    s.text(right + 0.8, cb.y(0) - 0.2, 'a note for people', size=16, color=MUTE, ha='left')
    s.text(0.15, cb.bottom - 0.4, 'Python skips everything after the #', size=19, ha='left', color=BODY)
    s.box(0.15, 0.3, 1.9, 0.75, '50.0', size=26, weight='bold', mono=True, fill=GOLD, lw=2.0, r=0.05)
    s.text(2.25, 0.68, 'is what the cell prints', size=18, ha='left', color=BODY)
    return s


# ---------------------------------------------------------------- small word icons, drawn for 1.3 x 1.3
@fig('c_icon_grid')
def c_icon_grid(w, h):
    s = Scene(w, h)
    for r in range(3):
        for c in range(3):
            s.box(0.18 + c * 0.32, 0.18 + r * 0.32, 0.3, 0.3, '', fill=GOLD if r == 0 else PAPER, lw=1.6, r=0.01)
    return s


@fig('c_icon_cell')
def c_icon_cell(w, h):
    s = Scene(w, h)
    s.box(0.15, 0.3, w - 0.3, h - 0.6, '', fill=PAPER, lw=2.2, r=0.06)
    for i in range(3):
        s.line(0.3, h - 0.5 - i * 0.22, w - 0.3 - i * 0.2, h - 0.5 - i * 0.22, color=INK, lw=2.4)
    return s


@fig('c_icon_run')
def c_icon_run(w, h):
    s = Scene(w, h)
    s.circle(w / 2, h / 2, 0.52, fill=GOLD, edge=INK, lw=2.4)
    s.poly([(w / 2 - 0.15, h / 2 - 0.25), (w / 2 - 0.15, h / 2 + 0.25), (w / 2 + 0.27, h / 2)], fill=INK, edge=INK, lw=1)
    return s


@fig('c_icon_output')
def c_icon_output(w, h):
    s = Scene(w, h)
    s.box(0.12, 0.7, 0.55, 0.4, '', fill=PAPER, lw=2, r=0.04)
    s.arrow(0.4, 0.68, 0.4, 0.4, color=RED, lw=2.4, head=12)
    s.box(0.12, 0.1, w - 0.24, 0.3, '', fill=GOLD, lw=2, r=0.04)
    return s


@fig('c_icon_box')
def c_icon_box(w, h):
    s = Scene(w, h)
    s.box(0.2, 0.15, w - 0.4, 0.62, '', fill=PAPER, lw=2.2, r=0.04)
    s.box(0.32, 0.88, w - 0.64, 0.3, '', fill=GOLD, lw=1.8, r=0.03)
    return s


@fig('c_icon_quotes')
def c_icon_quotes(w, h):
    s = Scene(w, h)
    s.box(0.1, 0.25, w - 0.2, h - 0.5, '', fill=GOLD, lw=2.2, r=0.05)
    s.text(w / 2, h / 2 - 0.02, '"ab"', size=24, weight='bold', mono=True)
    return s


@fig('c_icon_branch')
def c_icon_branch(w, h):
    s = Scene(w, h)
    s.circle(w / 2, 1.1, 0.1, fill=INK, edge=INK)
    s.line(w / 2, 1.0, w / 2, 0.7, color=INK, lw=2.4)
    s.line(w / 2, 0.7, 0.3, 0.35, color=INK, lw=2.4)
    s.line(w / 2, 0.7, w - 0.3, 0.35, color=INK, lw=2.4)
    s.box(0.1, 0.1, 0.4, 0.25, '', fill=GOLD, lw=1.8, r=0.02)
    s.box(w - 0.5, 0.1, 0.4, 0.25, '', fill=PAPER, lw=1.8, r=0.02)
    return s


@fig('c_icon_list')
def c_icon_list(w, h):
    s = Scene(w, h)
    for i in range(3):
        s.box(0.12 + i * 0.36, 0.45, 0.34, 0.4, '', fill=GOLD if i == 0 else PAPER, lw=1.8, r=0.02)
        s.text(0.29 + i * 0.36, 0.25, str(i), size=14, color=MUTE)
    return s


@fig('c_icon_loop')
def c_icon_loop(w, h):
    s = Scene(w, h)
    s.arrow(0.25, 0.45, 0.25, 0.9, color=INK, lw=2.6, head=14, rad=-0.9)
    s.arrow(1.05, 0.85, 1.05, 0.4, color=INK, lw=2.6, head=14, rad=-0.9)
    s.box(0.45, 0.45, 0.4, 0.4, '', fill=GOLD, lw=2, r=0.03)
    return s


@fig('c_icon_function')
def c_icon_function(w, h):
    s = Scene(w, h)
    s.arrow(0.05, h / 2, 0.38, h / 2, color=INK, lw=2.4, head=12)
    s.box(0.4, 0.3, 0.5, 0.7, '', fill=GOLD, lw=2.2, r=0.04)
    s.arrow(0.92, h / 2, w - 0.05, h / 2, color=INK, lw=2.4, head=12)
    return s


@fig('c_icon_key')
def c_icon_key(w, h):
    s = Scene(w, h)
    s.circle(0.4, h / 2, 0.22, fill=GOLD, edge=INK, lw=2.2)
    s.line(0.62, h / 2, 1.15, h / 2, color=INK, lw=3.4)
    s.line(1.0, h / 2, 1.0, h / 2 - 0.2, color=INK, lw=3.4)
    s.line(0.85, h / 2, 0.85, h / 2 - 0.15, color=INK, lw=3.4)
    return s
