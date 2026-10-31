"""Figure kit: a small drawing library for the camp's illustrations, in KLAi colours.

Every figure is drawn in inches on a canvas the size of its slide placement, so a 20 pt label in the
figure is a 20 pt label on the slide. Typical use:

    from figkit import Scene, fig_registry
    @fig('da_variable_boxes')
    def da_variable_boxes(w, h, **params):
        s = Scene(w, h)
        s.box(1, 2, 2, 1, '2000', size=28)
        ...
        return s

The registry maps a figure name to a function (w, h) -> Scene. render_figure(name, w, h) saves
FIG_DIR/<name>_<w>x<h>.png and returns its path.

Pictograms (s.icon) are flat drawings in brand colours: person, shop, laptop, notebook, folder, bottle,
book, pen, tag, bag, cloud, rain, magnifier, calculator, clock, coin, bars, bike, receipt, check, cross.
"""
import math
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Polygon, Ellipse, FancyArrowPatch, Wedge

from brand import (INK, BODY, MUTE, GREY, HAIR, PALE, PAPER, RED, GOLD, FONT_DIR, FIG_DIR)

for _f in FONT_DIR.glob('*.ttf'):
    font_manager.fontManager.addfont(str(_f))

FONT = 'Lato'
DPI = 200


def use_style():
    """Chart style for matplotlib code that runs on a slide (the lesson's own plt calls)."""
    plt.rcParams.update({
        'font.family': FONT, 'font.size': 16, 'axes.titlesize': 20, 'axes.titleweight': 'bold', 'axes.labelsize': 17,
        'xtick.labelsize': 15, 'ytick.labelsize': 15, 'axes.edgecolor': INK, 'axes.linewidth': 1.2,
        'axes.spines.top': False, 'axes.spines.right': False, 'axes.prop_cycle': matplotlib.cycler(color=[INK, RED, GOLD, GREY, '#555555']),
        'axes.grid': False, 'figure.facecolor': PAPER, 'axes.facecolor': PAPER, 'savefig.facecolor': PAPER,
        'figure.dpi': 100, 'figure.figsize': (6.4, 3.7), 'savefig.dpi': DPI, 'lines.linewidth': 2.4, 'patch.edgecolor': INK, 'patch.linewidth': 1.0,
        'text.color': INK, 'axes.labelcolor': INK, 'xtick.color': INK, 'ytick.color': INK, 'legend.frameon': False,
    })


use_style()

_REG = {}


def fig(name):
    def deco(fn):
        _REG[name] = fn
        return fn
    return deco


def fig_registry():
    return dict(_REG)


class LayoutError(Exception):
    pass


SMALL_TEXT = []   # (figure, text, size) for text under 14 pt, collected whenever a Scene is audited


class Scene:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.f = plt.figure(figsize=(w, h), dpi=DPI)
        self.ax = self.f.add_axes([0, 0, 1, 1])
        self.ax.set_xlim(0, w)
        self.ax.set_ylim(0, h)
        self.ax.axis('off')
        self.ax.set_aspect('equal')

    # ------------------------------------------------------------ text
    def text(self, x, y, s, size=18, weight='normal', color=INK, ha='center', va='center', mono=False, italic=False, z=6, rot=0, **kw):
        fam = 'DejaVu Sans Mono' if mono else FONT
        return self.ax.text(x, y, s, fontsize=size, fontweight=weight, color=color, ha=ha, va=va, family=fam,
                            style='italic' if italic else 'normal', zorder=z, rotation=rot, linespacing=1.15, **kw)

    # ------------------------------------------------------------ shapes
    def box(self, x, y, w, h, text='', size=18, fill=PAPER, edge=INK, lw=1.6, r=0.07, color=INK, weight='normal', mono=False,
            dash=False, z=2, ha='center', pad=0.12):
        p = FancyBboxPatch((x, y), w, h, boxstyle=f'round,pad=0,rounding_size={r}', fc=fill, ec=edge, lw=lw, zorder=z,
                           ls='--' if dash else '-')
        self.ax.add_patch(p)
        if text != '':
            tx = x + w / 2 if ha == 'center' else x + pad
            self.text(tx, y + h / 2, text, size=size, weight=weight, color=color, mono=mono, ha=ha, z=z + 1)
        return p

    def circle(self, x, y, r, fill=PAPER, edge=INK, lw=1.6, z=2):
        self.ax.add_patch(Circle((x, y), r, fc=fill, ec=edge, lw=lw, zorder=z))

    def rect(self, x, y, w, h, fill=PAPER, edge=INK, lw=1.4, z=2):
        self.ax.add_patch(Rectangle((x, y), w, h, fc=fill, ec=edge, lw=lw, zorder=z))

    def poly(self, pts, fill=PAPER, edge=INK, lw=1.4, z=2):
        self.ax.add_patch(Polygon(pts, closed=True, fc=fill, ec=edge, lw=lw, zorder=z, joinstyle='round'))

    def line(self, x1, y1, x2, y2, color=INK, lw=1.6, dash=False, z=1):
        self.ax.plot([x1, x2], [y1, y2], color=color, lw=lw, ls='--' if dash else '-', zorder=z, solid_capstyle='round')

    def arrow(self, x1, y1, x2, y2, color=INK, lw=2.2, head=16, rad=0.0, z=4, label=None, label_size=15, label_dx=0, label_dy=0.2,
              label_color=None, dash=False):
        a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='-|>', mutation_scale=head, lw=lw, color=color, zorder=z,
                            connectionstyle=f'arc3,rad={rad}', shrinkA=0, shrinkB=0, ls='--' if dash else '-')
        self.ax.add_patch(a)
        if label:
            self.text((x1 + x2) / 2 + label_dx, (y1 + y2) / 2 + label_dy, label, size=label_size, color=label_color or color, z=z + 1)

    def brace(self, x1, x2, y, depth=0.2, color=INK, lw=1.6, up=True):
        """A horizontal bracket spanning x1..x2 at y, hooks pointing towards the content."""
        d = depth if up else -depth
        self.line(x1, y, x2, y, color, lw)
        self.line(x1, y, x1, y + d, color, lw)
        self.line(x2, y, x2, y + d, color, lw)

    def callout(self, text, x, y, tx, ty, size=16, color=RED, w=None, h=None, ha='center'):
        """Text at (tx,ty) with an arrow to (x,y)."""
        self.text(tx, ty, text, size=size, color=color, weight='bold', ha=ha)
        self.arrow(tx, ty - 0.18 if ty > y else ty + 0.18, x, y, color=color, lw=2, head=13)

    # ------------------------------------------------------------ structured pieces
    def table(self, x, y_top, col_w, row_h, rows, header=True, size=16, mono_cols=(), hl_cells=None, hl_rows=(), hl_cols=(),
              hl_fill=GOLD, align=None, edge=INK, lw=1.2, header_weight='bold', row_lines=True, dim_rows=()):
        """Draw a grid. rows is a list of lists of strings. hl_cells: {(r,c): fill}. Row 0 is the header when header=True."""
        hl_cells = hl_cells or {}
        nrows, ncols = len(rows), len(col_w)
        total_w = sum(col_w)
        for r in range(nrows):
            y = y_top - (r + 1) * row_h
            cx = x
            for c in range(ncols):
                w = col_w[c]
                fill = PAPER
                if (r, c) in hl_cells:
                    fill = hl_cells[(r, c)]
                elif r in hl_rows or c in hl_cols:
                    fill = hl_fill
                is_head = header and r == 0
                self.ax.add_patch(Rectangle((cx, y), w, row_h, fc=fill, ec=edge if not is_head else edge, lw=lw, zorder=2))
                txt = rows[r][c]
                al = (align[c] if align else 'center')
                tx = cx + w / 2 if al == 'center' else (cx + 0.1 if al == 'left' else cx + w - 0.1)
                col = MUTE if r in dim_rows else INK
                self.text(tx, y + row_h / 2, str(txt), size=size, weight=header_weight if is_head else 'normal', ha=al,
                          mono=(c in mono_cols and not is_head), color=col, z=3)
                cx += w
        return x + total_w, y_top - nrows * row_h

    def cells(self, x, y, values, w=0.95, h=0.85, size=22, labels=None, label_size=15, hl=(), hl_fill=GOLD, edge=INK, lw=1.8,
              labels_above=False, gap=0.0, mono=False, label_color=MUTE):
        """A row of boxes with labels (such as index numbers) beneath or above."""
        for i, v in enumerate(values):
            bx = x + i * (w + gap)
            self.box(bx, y, w, h, str(v), size=size, fill=hl_fill if i in hl else PAPER, edge=edge, lw=lw, r=0.03, mono=mono)
            if labels is not None:
                ly = y + h + 0.22 if labels_above else y - 0.22
                self.text(bx + w / 2, ly, str(labels[i]), size=label_size, color=label_color)
        return x + len(values) * (w + gap)

    def tag(self, x, y, text, size=16, fill=INK, color=PAPER, h=0.4, pad=0.16):
        """A small label: filled shape with text, width set from the text length."""
        w = 0.13 * len(text) * size / 16 + 2 * pad
        self.box(x, y, w, h, text, size=size, fill=fill, edge=fill, color=color, weight='bold', r=0.06)
        return w

    def code(self, x, y_top, lines, size=15, line_h=0.27, w=None, pad=0.15, hl_lines=(), fill=INK):
        """A dark code panel. lines: list of strings."""
        n = len(lines)
        cw = w or (max(len(l) for l in lines) * size * 0.0087 + 2 * pad)
        h = n * line_h + 2 * pad
        self.box(x, y_top - h, cw, h, '', fill=fill, edge=fill, r=0.08, z=2)
        for i, l in enumerate(lines):
            yy = y_top - pad - (i + 0.5) * line_h
            if i in hl_lines:
                self.ax.add_patch(Rectangle((x + 0.05, yy - line_h / 2), cw - 0.1, line_h, fc='#3A3A3A', ec='none', zorder=3))
            self.text(x + pad, yy, l, size=size, color=PAPER, mono=True, ha='left', z=4)
        return cw, h

    # ------------------------------------------------------------ pictograms
    def icon(self, name, x, y, size=1.0, color=INK, accent=GOLD, **kw):
        """Draw a pictogram centred at (x, y), about `size` inches across."""
        getattr(self, '_i_' + name)(x, y, size, color, accent, **kw)

    def _i_person(self, x, y, s, c, a, shirt=None, label=None):
        self.circle(x, y + 0.30 * s, 0.17 * s, fill=PAPER, edge=c, lw=2)
        self.ax.add_patch(FancyBboxPatch((x - 0.26 * s, y - 0.42 * s), 0.52 * s, 0.56 * s, boxstyle=f'round,pad=0,rounding_size={0.18 * s}',
                                         fc=shirt or a, ec=c, lw=2, zorder=2))
        if label:
            self.text(x, y - 0.62 * s, label, size=15, color=MUTE)

    def _i_shop(self, x, y, s, c, a):
        self.rect(x - 0.45 * s, y - 0.35 * s, 0.9 * s, 0.55 * s, fill=PAPER, edge=c, lw=2)
        self.poly([(x - 0.52 * s, y + 0.2 * s), (x + 0.52 * s, y + 0.2 * s), (x + 0.42 * s, y + 0.42 * s), (x - 0.42 * s, y + 0.42 * s)], fill=a, edge=c, lw=2)
        self.rect(x - 0.1 * s, y - 0.35 * s, 0.2 * s, 0.34 * s, fill=PAPER, edge=c, lw=1.6)
        self.rect(x + 0.18 * s, y - 0.2 * s, 0.2 * s, 0.2 * s, fill=PAPER, edge=c, lw=1.6)
        self.rect(x - 0.38 * s, y - 0.2 * s, 0.2 * s, 0.2 * s, fill=PAPER, edge=c, lw=1.6)

    def _i_laptop(self, x, y, s, c, a):
        self.rect(x - 0.38 * s, y - 0.12 * s, 0.76 * s, 0.5 * s, fill=PAPER, edge=c, lw=2)
        self.rect(x - 0.32 * s, y - 0.06 * s, 0.64 * s, 0.38 * s, fill=INK, edge=INK, lw=1)
        self.poly([(x - 0.5 * s, y - 0.12 * s), (x + 0.5 * s, y - 0.12 * s), (x + 0.42 * s, y - 0.24 * s), (x - 0.42 * s, y - 0.24 * s)], fill=a, edge=c, lw=2)

    def _i_notebook(self, x, y, s, c, a):
        self.rect(x - 0.3 * s, y - 0.4 * s, 0.6 * s, 0.8 * s, fill=PAPER, edge=c, lw=2)
        for i in range(5):
            self.line(x - 0.2 * s, y + 0.26 * s - i * 0.14 * s, x + 0.22 * s, y + 0.26 * s - i * 0.14 * s, color=GREY, lw=1.4)
        for i in range(4):
            self.circle(x - 0.3 * s, y + 0.28 * s - i * 0.2 * s, 0.035 * s, fill=a, edge=c, lw=1.2, z=3)

    def _i_folder(self, x, y, s, c, a):
        self.poly([(x - 0.45 * s, y - 0.3 * s), (x + 0.45 * s, y - 0.3 * s), (x + 0.45 * s, y + 0.22 * s), (x - 0.02 * s, y + 0.22 * s),
                   (x - 0.1 * s, y + 0.32 * s), (x - 0.45 * s, y + 0.32 * s)], fill=a, edge=c, lw=2)

    def _i_bottle(self, x, y, s, c, a):
        self.poly([(x - 0.12 * s, y + 0.45 * s), (x + 0.12 * s, y + 0.45 * s), (x + 0.12 * s, y + 0.28 * s), (x + 0.24 * s, y + 0.12 * s),
                   (x + 0.24 * s, y - 0.45 * s), (x - 0.24 * s, y - 0.45 * s), (x - 0.24 * s, y + 0.12 * s), (x - 0.12 * s, y + 0.28 * s)], fill=PAPER, edge=c, lw=2)
        self.rect(x - 0.22 * s, y - 0.2 * s, 0.44 * s, 0.26 * s, fill=a, edge=c, lw=1.4, z=3)
        self.rect(x - 0.12 * s, y + 0.45 * s, 0.24 * s, 0.07 * s, fill=c, edge=c, lw=1)

    def _i_book(self, x, y, s, c, a):
        self.rect(x - 0.3 * s, y - 0.4 * s, 0.6 * s, 0.8 * s, fill=a, edge=c, lw=2)
        self.rect(x - 0.3 * s, y - 0.4 * s, 0.1 * s, 0.8 * s, fill=c, edge=c, lw=1)
        self.rect(x - 0.1 * s, y + 0.08 * s, 0.32 * s, 0.2 * s, fill=PAPER, edge=c, lw=1.4, z=3)

    def _i_pen(self, x, y, s, c, a):
        self.poly([(x - 0.06 * s, y + 0.45 * s), (x + 0.06 * s, y + 0.45 * s), (x + 0.06 * s, y - 0.25 * s), (x, y - 0.42 * s), (x - 0.06 * s, y - 0.25 * s)], fill=a, edge=c, lw=2)
        self.rect(x - 0.06 * s, y + 0.25 * s, 0.12 * s, 0.2 * s, fill=c, edge=c, lw=1)

    def _i_tag(self, x, y, s, c, a, text=''):
        self.poly([(x - 0.45 * s, y + 0.2 * s), (x + 0.2 * s, y + 0.2 * s), (x + 0.45 * s, y), (x + 0.2 * s, y - 0.2 * s), (x - 0.45 * s, y - 0.2 * s)], fill=a, edge=c, lw=2)
        self.circle(x - 0.33 * s, y, 0.05 * s, fill=PAPER, edge=c, lw=1.4, z=3)
        if text:
            self.text(x, y, text, size=14, weight='bold', z=5)

    def _i_bag(self, x, y, s, c, a):
        self.poly([(x - 0.32 * s, y + 0.2 * s), (x + 0.32 * s, y + 0.2 * s), (x + 0.4 * s, y - 0.4 * s), (x - 0.4 * s, y - 0.4 * s)], fill=a, edge=c, lw=2)
        self.ax.add_patch(Wedge((x, y + 0.2 * s), 0.2 * s, 0, 180, width=0.04 * s, fc=c, ec=c, zorder=3))

    def _i_cloud(self, x, y, s, c, a):
        for dx, dy, r in [(-0.2, 0, 0.2), (0.02, 0.1, 0.26), (0.26, -0.02, 0.18)]:
            self.circle(x + dx * s, y + dy * s, r * s, fill=PAPER, edge=c, lw=2)
        self.rect(x - 0.38 * s, y - 0.2 * s, 0.82 * s, 0.17 * s, fill=PAPER, edge=PAPER, lw=0, z=3)
        self.line(x - 0.38 * s, y - 0.2 * s, x + 0.44 * s, y - 0.2 * s, color=c, lw=2, z=4)

    def _i_rain(self, x, y, s, c, a):
        self._i_cloud(x, y + 0.1 * s, s, c, a)
        for dx in (-0.22, 0, 0.22):
            self.line(x + dx * s, y - 0.25 * s, x + (dx - 0.06) * s, y - 0.42 * s, color=c, lw=2.2, z=4)

    def _i_magnifier(self, x, y, s, c, a):
        self.circle(x - 0.08 * s, y + 0.08 * s, 0.26 * s, fill=PAPER, edge=c, lw=2.6)
        self.line(x + 0.1 * s, y - 0.1 * s, x + 0.4 * s, y - 0.4 * s, color=c, lw=4.5, z=3)

    def _i_calculator(self, x, y, s, c, a):
        self.ax.add_patch(FancyBboxPatch((x - 0.3 * s, y - 0.42 * s), 0.6 * s, 0.84 * s, boxstyle=f'round,pad=0,rounding_size={0.06 * s}', fc=PAPER, ec=c, lw=2, zorder=2))
        self.rect(x - 0.22 * s, y + 0.2 * s, 0.44 * s, 0.16 * s, fill=a, edge=c, lw=1.4, z=3)
        for i in range(3):
            for j in range(3):
                self.circle(x - 0.14 * s + j * 0.14 * s, y + 0.06 * s - i * 0.16 * s, 0.045 * s, fill=c, edge=c, lw=0.5, z=3)

    def _i_clock(self, x, y, s, c, a, hand=(0.0, 0.2)):
        self.circle(x, y, 0.38 * s, fill=PAPER, edge=c, lw=2.4)
        self.line(x, y, x + 0.0, y + 0.24 * s, color=c, lw=2.6, z=4)
        self.line(x, y, x + 0.17 * s, y, color=a if a != GOLD else RED, lw=2.6, z=4)

    def _i_coin(self, x, y, s, c, a, text='UGX'):
        self.circle(x, y, 0.34 * s, fill=a, edge=c, lw=2.2)
        self.text(x, y, text, size=max(9, 11 * s), weight='bold', z=5)

    def _i_bars(self, x, y, s, c, a):
        for i, hgt in enumerate((0.3, 0.55, 0.42)):
            self.rect(x - 0.32 * s + i * 0.24 * s, y - 0.35 * s, 0.18 * s, hgt * s, fill=a if i == 1 else PAPER, edge=c, lw=2)
        self.line(x - 0.4 * s, y - 0.35 * s, x + 0.4 * s, y - 0.35 * s, color=c, lw=2)

    def _i_bike(self, x, y, s, c, a):
        for dx in (-0.3, 0.3):
            self.circle(x + dx * s, y - 0.18 * s, 0.17 * s, fill=PAPER, edge=c, lw=2.2)
        self.poly([(x - 0.3 * s, y - 0.18 * s), (x - 0.05 * s, y + 0.12 * s), (x + 0.2 * s, y + 0.12 * s), (x + 0.3 * s, y - 0.18 * s), (x + 0.1 * s, y - 0.05 * s), (x - 0.15 * s, y - 0.05 * s)], fill=a, edge=c, lw=2)
        self.line(x + 0.18 * s, y + 0.12 * s, x + 0.28 * s, y + 0.3 * s, color=c, lw=2.2)
        self.line(x + 0.2 * s, y + 0.3 * s, x + 0.36 * s, y + 0.3 * s, color=c, lw=2.2)

    def _i_receipt(self, x, y, s, c, a):
        self.poly([(x - 0.25 * s, y + 0.42 * s), (x + 0.25 * s, y + 0.42 * s), (x + 0.25 * s, y - 0.42 * s), (x + 0.17 * s, y - 0.36 * s), (x + 0.08 * s, y - 0.42 * s),
                   (x, y - 0.36 * s), (x - 0.08 * s, y - 0.42 * s), (x - 0.17 * s, y - 0.36 * s), (x - 0.25 * s, y - 0.42 * s)], fill=PAPER, edge=c, lw=2)
        for i in range(4):
            self.line(x - 0.16 * s, y + 0.26 * s - i * 0.14 * s, x + 0.16 * s, y + 0.26 * s - i * 0.14 * s, color=GREY, lw=1.4, z=3)

    def _i_check(self, x, y, s, c, a):
        self.circle(x, y, 0.3 * s, fill=a, edge=c, lw=2)
        self.line(x - 0.14 * s, y, x - 0.04 * s, y - 0.12 * s, color=c, lw=3.4, z=4)
        self.line(x - 0.04 * s, y - 0.12 * s, x + 0.16 * s, y + 0.12 * s, color=c, lw=3.4, z=4)

    def _i_cross(self, x, y, s, c, a):
        self.circle(x, y, 0.3 * s, fill=RED, edge=RED, lw=2)
        self.line(x - 0.12 * s, y - 0.12 * s, x + 0.12 * s, y + 0.12 * s, color=PAPER, lw=3.4, z=4)
        self.line(x - 0.12 * s, y + 0.12 * s, x + 0.12 * s, y - 0.12 * s, color=PAPER, lw=3.4, z=4)

    # ------------------------------------------------------------ output
    def audit(self, name=''):
        """Geometry audit: every text must sit inside the canvas and no two texts may overlap. Raises LayoutError."""
        self.f.canvas.draw()
        rend = self.f.canvas.get_renderer()
        boxes = []
        for t in self.ax.texts:
            if not t.get_text().strip():
                continue
            bb = t.get_window_extent(rend)
            boxes.append((t.get_text().replace('\n', ' ')[:40], bb.x0 / DPI, bb.y0 / DPI, bb.x1 / DPI, bb.y1 / DPI))
        for t in self.ax.texts:
            if t.get_text().strip() and t.get_fontsize() < 14:
                SMALL_TEXT.append((name or '?', t.get_text()[:30], t.get_fontsize()))
        bad = []
        tol = 0.03
        for txt, x0, y0, x1, y1 in boxes:
            if x0 < -tol or y0 < -tol or x1 > self.w + tol or y1 > self.h + tol:
                bad.append(f'outside canvas ({self.w:.1f}x{self.h:.1f} in): {txt!r} at x {x0:.2f}..{x1:.2f}, y {y0:.2f}..{y1:.2f}')
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                a, b = boxes[i], boxes[j]
                ix = min(a[3], b[3]) - max(a[1], b[1])
                iy = min(a[4], b[4]) - max(a[2], b[2])
                if ix > 0.04 and iy > 0.04:
                    area = ix * iy
                    small = min((a[3] - a[1]) * (a[4] - a[2]), (b[3] - b[1]) * (b[4] - b[2]))
                    if small > 0 and area / small > 0.12:
                        bad.append(f'texts overlap: {a[0]!r} and {b[0]!r}')
        if bad:
            raise LayoutError((name + ': ' if name else '') + '; '.join(bad[:6]))

    def save(self, path, name=''):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        try:
            self.audit(name or Path(path).stem)
        except LayoutError:
            plt.close(self.f)
            raise
        self.f.savefig(path, dpi=DPI, facecolor=PAPER)
        plt.close(self.f)
        return path


def render_figure(name, w, h, params=None, force=False):
    """Render a registered figure at w x h inches into FIG_DIR and return the file path.

    A figure function has the signature fn(w, h, **params) and returns a Scene."""
    import hashlib, json
    params = params or {}
    tag = ''
    if params:
        tag = '_' + hashlib.md5(json.dumps(params, sort_keys=True, default=str).encode()).hexdigest()[:8]
    path = FIG_DIR / f'{name}_{w:.2f}x{h:.2f}{tag}.png'
    if name not in _REG:
        raise KeyError(f'figure {name!r} is not registered')
    import inspect, os
    force = force or bool(os.environ.get('FORCE_FIGS'))
    src_mtime = os.path.getmtime(inspect.getsourcefile(_REG[name]))
    if path.exists() and not force and os.path.getmtime(path) >= src_mtime:
        return path
    s = _REG[name](w, h, **params)
    try:
        return s.save(path, name=name)
    except TypeError:
        return s.save(path)


def save_chart(fig_obj, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    fig_obj.savefig(path, dpi=DPI, facecolor=PAPER, bbox_inches='tight', pad_inches=0.15)
    plt.close(fig_obj)
    return path
