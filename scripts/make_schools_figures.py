# -*- coding: utf-8 -*-
"""Figures for the S.5 / S.6 Machine Learning Track syllabus.

DRAWN AT PRINT SIZE, NOT AT SLIDE SIZE
--------------------------------------
The roadmap keeps the approved slide figure's design: the same palette
constants, the same card anatomy, the same legend, copied from
make_figures.fig_roadmap_journey() rather than chosen again.

What it does not keep is the slide's dimensions. That figure is 13in wide for
a projector. Placed in an A4 document at 6.7in, every size in it halves, and
the first build of this syllabus printed 7.7pt annotation on the page at
under 4pt. So each figure is now drawn close to the width it is placed at,
the placement widths live in schools_content.FIG_PLACEMENT, and
pt_on_paper() asserts that nothing lands under the stated floor.

That check is the point of this module. A figure that is illegible on paper
looks perfectly fine on screen at 200 dpi, which is how the first version
passed a visual inspection.
"""
import os
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyBboxPatch, Rectangle

import os as _os
import sys
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_HERE)
sys.path.insert(0, _HERE)

import schools_content as C                                # noqa: E402

OUT = _ROOT + "/Schools_ML_Track/archive/original_ml_syllabus/figs"
os.makedirs(OUT, exist_ok=True)

# Copied verbatim from make_figures.py rather than chosen again.
INK = "#1C3144"; ORANGE = "#E4572E"; TEAL = "#2E7D6F"
MUTED = "#6B7A8A"; STEEL = "#E8EDF2"; PAPER = "#FFFFFF"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 12,
    "axes.edgecolor": MUTED, "axes.labelcolor": INK, "text.color": INK,
    "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.facecolor": PAPER, "savefig.facecolor": PAPER,
})

# Four teaching bands instead of the original's two semesters. The two
# non-teaching bands keep the original's colours and meaning exactly: the
# steel blue is what the student already has, the grey is what this course
# does not teach.
GOLD = "#B07A10"
PLUM = "#6B4E8C"
COL = {
    C.B12: ORANGE,
    C.B34: TEAL,
    C.B56: GOLD,
    C.B78: PLUM,
    C.HAVE: "#4A6B84",
    C.LATER: "#9AA9B6",
}


def pt_on_paper(fig, name, smallest_in_figure):
    """What the smallest type in this figure measures once placed.

    Raises if it lands under the floor, so a figure redrawn at a different
    width cannot quietly become unreadable in print.
    """
    drawn_w, drawn_h = fig.get_size_inches()
    placed_w = C.FIG_PLACEMENT[name]
    placed_h = placed_w * drawn_h / drawn_w
    if placed_h > C.FIG_MAX_H:
        raise SystemExit(
            "%s: placed at %.1fin wide it is %.2fin tall, over the %.1fin "
            "the page has room for. It will be pushed onto a page of its "
            "own, away from its heading."
            % (name, placed_w, placed_h, C.FIG_MAX_H))
    on_paper = smallest_in_figure * placed_w / drawn_w
    if on_paper < C.FIG_MIN_PT:
        raise SystemExit(
            "%s: smallest type is %.1fpt drawn at %.1fin, which is %.1fpt "
            "once placed at %.1fin, under the %.1fpt floor. Draw the figure "
            "closer to the width it is placed at."
            % (name, smallest_in_figure, drawn_w, on_paper, placed_w,
               C.FIG_MIN_PT))
    return on_paper


def save(fig, name, smallest, dpi=300, pad=0.16):
    on_paper = pt_on_paper(fig, name, smallest)
    p = os.path.join(OUT, name + ".png")
    fig.savefig(p, dpi=dpi, bbox_inches="tight", pad_inches=pad)
    plt.close(fig)
    return p, on_paper


# =============================================================== the roadmap
def fig_roadmap():
    """The approved slide roadmap, redrawn for a printed portrait page.

    Same three-by-five grid, same card anatomy, same legend construction,
    same colour meanings, copied from the slide version. Two changes forced
    by paper:

    the figure is drawn 7.3in wide against a 7.0in placement, so type on the
    page is within four per cent of type in the file; and the week label sits
    at the TOP RIGHT of each card rather than the bottom right, because at
    this width the third line of detail ran straight into it. Two cards in
    the first build printed "Week 4" over "writing down what you changed".
    """
    FS_NAME, FS_SUB, FS_NUM, FS_WHEN, FS_LEG = 9.4, 8.6, 8.8, 8.6, 8.6
    fig, ax = plt.subplots(figsize=(7.3, 7.9))
    ax.set_xlim(0, 15); ax.set_ylim(-0.10, 8.05); ax.axis("off")
    # The axes must FILL the figure, or data units do not map to the
    # inches the placement check assumes: the default leaves 22% of the
    # width as margin and every card came out a fifth too narrow.
    ax.set_position([0, 0, 1, 1])
    nrow = 5
    cw, chh, gx, gy = 4.72, 1.40, 0.22, 0.11
    cards = []
    for i, (num, name, subs, band, when) in enumerate(C.STAGES):
        c, r = divmod(i, nrow)
        x = 0.05 + c * (cw + gx)
        y = 7.40 - (r + 1) * (chh + gy)
        col = COL[band]
        ax.add_patch(FancyBboxPatch(
            (x, y), cw, chh, boxstyle="round,pad=0.02,rounding_size=0.10",
            facecolor="#F5F8FB", edgecolor=col, lw=1.8))
        ax.add_patch(Rectangle((x, y), 0.09, chh, facecolor=col,
                               edgecolor="none"))
        ax.add_patch(Ellipse((x + 0.46, y + chh - 0.30), 0.50, 0.30,
                             facecolor=col))
        ax.text(x + 0.46, y + chh - 0.30, num, ha="center", va="center",
                color=PAPER, fontsize=FS_NUM, fontweight="bold")
        t_name = ax.text(x + 0.86, y + chh - 0.17, name, ha="left", va="top",
                         fontsize=FS_NAME, fontweight="bold", color=INK)
        # Bottom right, as in the approved slide figure. It works here
        # because the card is taller than the slide's: at the slide's
        # height the third detail line ran into it.
        t_when = ax.text(x + cw - 0.12, y + 0.10, when, ha="right",
                         va="bottom", fontsize=FS_WHEN, color=col,
                         fontweight="bold", style="italic")
        t_subs = ax.text(x + 0.86, y + chh - 0.56, subs, ha="left", va="top",
                         fontsize=FS_SUB, color="#4A5B6B", linespacing=1.44)
        cards.append((x, y, t_name, t_when, t_subs))

    # The legend is laid out BY MEASUREMENT, not by a character count. The
    # slide version spaced entries with 0.72 + len(label) * 0.108, which was
    # tuned for a 13in figure; at 7.3in the text is relatively wider and
    # every swatch printed on top of the previous label.
    inv = ax.transData.inverted()

    def text_width(label, size):
        probe = ax.text(0, -5, label, fontsize=size, fontweight="bold")
        fig.canvas.draw()
        b = probe.get_window_extent(renderer=fig.canvas.get_renderer())
        probe.remove()
        return inv.transform((b.x1, 0))[0] - inv.transform((b.x0, 0))[0]

    SW, PAD, GAP = 0.26, 0.14, 0.46
    rows = [(C.B12, C.B34, C.B56), (C.B78, C.HAVE, C.LATER)]
    swatches = []
    for ri, row in enumerate(rows):
        yy = 7.72 - ri * 0.26
        hx = 0.05
        for band in row:
            ax.add_patch(Rectangle((hx, yy), SW, 0.185,
                                   facecolor=COL[band], edgecolor="none"))
            t = ax.text(hx + SW + PAD, yy + 0.09, band, ha="left",
                        va="center", fontsize=FS_LEG, fontweight="bold",
                        color=COL[band])
            swatches.append((hx, t))
            hx += SW + PAD + text_width(band, FS_LEG) + GAP
        if hx > 15.0:
            raise SystemExit("legend row %d is %.2f wide, over the figure"
                             % (ri + 1, hx))
    # Reads left to right, top to bottom, and each card lists the three
    # things taught inside it. Stated on the figure because the figure
    # travels on its own: it goes into the slide deck and into the parents'
    # WhatsApp group without the caption that explains it.
    attr = ax.text(14.95, 7.94,
                   "read left to right - each card lists what you learn in it",
                   ha="right", va="center", fontsize=FS_WHEN, color=MUTED,
                   style="italic")

    # Three measured checks, each for a defect a read-through missed once.
    fig.canvas.draw()
    r = fig.canvas.get_renderer()

    bad = []
    for x, y, t_name, t_when, t_subs in cards:
        nb = t_name.get_window_extent(renderer=r)
        wb = t_when.get_window_extent(renderer=r)
        sb = t_subs.get_window_extent(renderer=r)
        right = ax.transData.transform((x + cw, 0))[0]
        bottom = ax.transData.transform((0, y))[1]
        # the detail block sits above the week label and inside the card
        if sb.y0 < wb.y1 + 2:
            bad.append(("detail meets week label", t_name.get_text()))
        if sb.x1 > right - 2 or sb.y0 < bottom + 2:
            bad.append(("detail leaves the card", t_name.get_text()))
        if nb.x1 > right - 2:
            bad.append(("title leaves the card", t_name.get_text()))
    if bad:
        raise SystemExit("roadmap cards have colliding text: %r" % bad[:5])

    # No legend label may reach the next swatch. This is the defect the
    # character-count formula produced, and it survived a read-through.
    clash = []
    for i in range(len(swatches) - 1):
        _, t = swatches[i]
        nx, nt = swatches[i + 1]
        if nt.get_window_extent(renderer=r).y0 != \
                t.get_window_extent(renderer=r).y0:
            continue                      # different row
        label_right = t.get_window_extent(renderer=r).x1
        next_swatch_left = ax.transData.transform((nx, 0))[0]
        if label_right > next_swatch_left - 2:
            clash.append((t.get_text(), nt.get_text()))
    if clash:
        raise SystemExit("legend labels run into the next swatch: %r" % clash)
    return save(fig, "roadmap_schools", FS_WHEN)


# =============================================================== the 8 weeks
def fig_timeline():
    """The eight weeks, two rows of four, at the width it is placed.

    A parent reads one picture. The label at the bottom of each card is the
    thing that exists on the laptop rather than the topic name, because that
    is the question a parent is actually asking.
    """
    FS_WEEK, FS_TITLE, FS_OUT, FS_NOTE = 10.0, 8.6, 8.4, 8.6
    fig, ax = plt.subplots(figsize=(7.0, 4.15))
    ax.set_xlim(0, 10); ax.set_ylim(0, 6.0); ax.axis("off")
    # The axes must FILL the figure, or data units do not map to the
    # inches the placement check assumes: the default leaves 22% of the
    # width as margin and every card came out a fifth too narrow.
    ax.set_position([0, 0, 1, 1])

    band_of = {}
    for w in C.WEEKS_PLAN:
        first = str(w["stages"][0])
        band_of[w["n"]] = next(s[3] for s in C.STAGES if s[0] == first)

    short = {
        1: "Python working on\nyour own laptop",
        2: "A marks program\nthat runs",
        3: "A real dataset, and\nfive answers from it",
        4: "Three charts and\nfive findings",
        5: "Two trained models",
        6: "A model you can\ndefend",
        7: "A neural network,\nand a project plan",
        8: "A finished project,\npublished",
    }
    cw, gap, ch = 2.34, 0.18, 1.92
    cards, titles = [], []
    for w in C.WEEKS_PLAN:
        col_i = (w["n"] - 1) % 4
        row_i = (w["n"] - 1) // 4
        x = 0.05 + col_i * (cw + gap)
        y = 3.30 - row_i * (ch + 0.55)
        col = COL[band_of[w["n"]]]
        ax.add_patch(FancyBboxPatch(
            (x, y), cw, ch, boxstyle="round,pad=0.02,rounding_size=0.08",
            facecolor="#F5F8FB", edgecolor=col, lw=1.6))
        ax.add_patch(Rectangle((x, y + ch - 0.08), cw, 0.08, facecolor=col,
                               edgecolor="none"))
        ax.text(x + cw / 2, y + ch - 0.30, "WEEK %d" % w["n"], ha="center",
                va="center", fontsize=FS_WEEK, fontweight="bold", color=col)
        t = ax.text(x + cw / 2, y + ch - 0.52,
                    textwrap.fill(w["title"], 16), ha="center", va="top",
                    fontsize=FS_TITLE, fontweight="bold", color=INK,
                    linespacing=1.32)
        ax.text(x + cw / 2, y + 0.46, short[w["n"]], ha="center",
                va="center", fontsize=FS_OUT, color="#4A5B6B",
                linespacing=1.36)
        cards.append((x, x + cw))
        titles.append(t)

    ax.text(0.05, 5.78, "What exists at the end of each week",
            fontsize=FS_NOTE + 0.6, fontweight="bold", color=INK, va="top")
    ax.text(9.95, 5.78, "%d hours  -  %d sessions  -  %d hours each"
            % (C.TOTAL_HOURS, C.SESSIONS, C.HOURS_PER_SESSION),
            ha="right", va="top", fontsize=FS_NOTE, color=MUTED,
            style="italic")

    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    over = []
    for (x0, x1), t in zip(cards, titles):
        box = t.get_window_extent(renderer=r)
        left = ax.transData.transform((x0, 0))[0]
        right = ax.transData.transform((x1, 0))[0]
        if box.x0 < left + 2 or box.x1 > right - 2:
            over.append((t.get_text().replace("\n", " ")[:26],
                         round(box.x0 - left, 1), round(box.x1 - right, 1)))
    if over:
        raise SystemExit("week titles overflow their cards: %r" % over)
    return save(fig, "timeline_schools", FS_OUT)


# =============================================================== the marks
def fig_marks():
    """Where the marks come from. A sorted horizontal bar, because a pie with
    five slices cannot be ranked by eye."""
    FS_NAME, FS_VAL, FS_TITLE = 9.2, 9.0, 10.4
    fig, ax = plt.subplots(figsize=(6.9, 3.0))
    fig.subplots_adjust(left=0.30, right=0.99, top=0.86, bottom=0.04)
    rows = list(reversed(C.ASSESSMENT))
    names = [textwrap.fill(r[0], 30) for r in rows]
    vals = [r[1] for r in rows]
    whens = [r[2] for r in rows]
    cols = [ORANGE if v >= 30 else (GOLD if v >= 20 else TEAL) for v in vals]

    y = list(range(len(rows)))
    ax.barh(y, vals, color=cols, height=0.60)
    for i, (v, w) in enumerate(zip(vals, whens)):
        ax.text(v + 0.8, i, "%d%%   %s" % (v, w), va="center",
                fontsize=FS_VAL, color=INK)
    ax.set_yticks(y)
    ax.set_yticklabels(names, fontsize=FS_NAME)
    ax.set_xlim(0, 46)
    ax.set_xticks([])
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.set_title("Marks come from work. Attendance is expected and is not a "
                 "grade.", loc="left", fontsize=FS_TITLE, fontweight="bold",
                 color=INK, pad=10)
    return save(fig, "marks_schools", FS_VAL)


def main():
    made = [fig_roadmap(), fig_timeline(), fig_marks()]
    print("saved %d figures to %s" % (len(made), OUT))
    small = []
    for p, on_paper in made:
        name = os.path.basename(p)
        kb = os.path.getsize(p) / 1024.0
        print("  %-24s %6.0f KB   smallest type on paper %.1fpt"
              % (name, kb, on_paper))
        if kb < 10:
            small.append(name)
    if small:
        raise SystemExit("figures too small to contain anything: %r" % small)


if __name__ == "__main__":
    main()
