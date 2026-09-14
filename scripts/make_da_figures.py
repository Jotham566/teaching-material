# -*- coding: utf-8 -*-
"""Explainer figures for the Data Analysis track.

Audience: adults who are confident in Excel and have never written a line of
code. Every figure has to teach one idea and survive a projector, so nothing
here is smaller than 11pt and nothing that carries meaning is light grey.

House style, palette, DPI and the _HERE/_ROOT pattern are taken from
make_figures.py so the two courses look like one programme. Numbers come from
da_keys (the answer key) or are recomputed from the course CSVs, and every
figure that is not real data says so in its own caption.

Data is read from the CSVs with pandas on purpose: sqlite3 raises
"disk I/O error" against riverside.db on a mounted folder. check_against_key()
proves the CSV route reproduces the answer key before any figure is drawn.
"""
import math
import os
import random
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyArrowPatch, FancyBboxPatch, Rectangle
from matplotlib.ticker import FuncFormatter
import pandas as pd

import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_HERE)
sys.path.insert(0, _HERE)
import da_keys  # noqa: E402  (needs _HERE on the path first)

OUT = _ROOT + "/DataAnalysis_Track/figs"
DATA = _ROOT + "/DataAnalysis_Track/data"
os.makedirs(OUT, exist_ok=True)

INK = "#1C3144"; ORANGE = "#E4572E"; TEAL = "#2E7D6F"
MUTED = "#6B7A8A"; STEEL = "#E8EDF2"; PAPER = "#FFFFFF"
BODY = "#33465A"          # body copy: dark enough to project, unlike MUTED
SLATE = "#4A6B84"         # mid steel, for bars and second-rank boxes
EDGE = "#CDD8E2"
FADE = "#FDEDE8"          # pale orange wash
FADE_T = "#E4F0ED"        # pale teal wash
FADE_B = "#E9EFF5"        # pale steel wash
GRID = "#E3E9EF"
MONO = "DejaVu Sans Mono"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 12,
    "axes.edgecolor": MUTED, "axes.labelcolor": INK, "text.color": INK,
    "xtick.color": BODY, "ytick.color": BODY,
    "xtick.labelsize": 11, "ytick.labelsize": 11,
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.facecolor": PAPER, "savefig.facecolor": PAPER,
})

DPI = 200
CPAD = 0.14               # savefig pad for canvas() diagrams


# ------------------------------------------------------------------ plumbing
def save(fig, name, dpi=DPI, pad=0.22):
    p = os.path.join(OUT, name)
    fig.savefig(p, dpi=dpi, bbox_inches="tight", pad_inches=pad)
    plt.close(fig)
    return p


def save_exact(fig, name, dpi=DPI):
    """Save at exactly figsize. Charts set their own margins, so a tight box
    would let one long caption stretch the slide out of 16:9."""
    p = os.path.join(OUT, name)
    fig.savefig(p, dpi=dpi)
    plt.close(fig)
    return p


def canvas(w, h, y0=0.0):
    """Blank canvas where one data unit == one inch, as in make_figures.py."""
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_position([0, 0, 1, 1])
    ax.set_xlim(0, w)
    ax.set_ylim(y0, y0 + h)
    ax.axis("off")
    ax.scatter([0, w], [y0, y0 + h], s=0.1, alpha=0)
    return fig, ax


def save_c(fig, name):
    return save(fig, name, pad=CPAD)


def panel(ax, x, y, w, h, face=STEEL, edge=EDGE, lw=1.4, r=0.10, z=1, ls="solid"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                                facecolor=face, edgecolor=edge, lw=lw, zorder=z,
                                linestyle=ls))


def arrow(ax, p0, p1, col=MUTED, lw=2.0, style="-|>", ms=18, z=4, **kw):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle=style, mutation_scale=ms,
                                 color=col, lw=lw, zorder=z, **kw))


def title(ax, x, y, s, fs=13.5):
    return ax.text(x, y, s, fontsize=fs, fontweight="bold", color=INK, va="center")


def label(ax, x, y, s, col=INK, fs=11.5, ha="left", bold=True):
    return ax.text(x, y, s, ha=ha, va="center", fontsize=fs, color=col,
                   fontweight="bold" if bold else "normal", linespacing=1.5,
                   zorder=8)


def caption(ax, x, y, s, fs=11.0, col=BODY, **kw):
    return ax.text(x, y, s, ha="left", va="center", fontsize=fs, color=col,
                   linespacing=1.45, **kw)


def table(ax, x, y_top, colw, rowh, heads, rows, *, head_bg=INK, head_fs=11.0,
          cell_fs=11.0, zebra=True, cell_col=None, head_col=None, z=2, mono_from=1):
    """Draw a plain grid table downwards from y_top. Returns (right_x, bottom_y).

    cell_col(i, j, value) -> (facecolor, textcolor, bold) overrides one cell.
    """
    for j, h in enumerate(heads):
        hb = (head_col(j) if head_col else None) or head_bg
        ax.add_patch(Rectangle((x + sum(colw[:j]), y_top - rowh), colw[j], rowh,
                               facecolor=hb, edgecolor=PAPER, lw=1.6, zorder=z))
        ax.text(x + sum(colw[:j]) + colw[j] / 2, y_top - rowh / 2, h, ha="center",
                va="center", color=PAPER, fontsize=head_fs, fontweight="bold",
                zorder=z + 1, linespacing=1.3)
    for i, row in enumerate(rows):
        yy = y_top - (i + 2) * rowh
        for j in range(len(heads)):
            face = STEEL if (zebra and i % 2) else PAPER
            tcol, bold = INK, False
            over = cell_col(i, j, row[j]) if cell_col else None
            if over:
                face, tcol, bold = over
            ax.add_patch(Rectangle((x + sum(colw[:j]), yy), colw[j], rowh,
                                   facecolor=face, edgecolor=EDGE, lw=1.0, zorder=z))
            ax.text(x + sum(colw[:j]) + colw[j] / 2, yy + rowh / 2, str(row[j]),
                    ha="center", va="center", color=tcol, fontsize=cell_fs,
                    fontweight="bold" if bold else "normal", zorder=z + 1,
                    family=MONO if j >= mono_from else None)
    return x + sum(colw), y_top - (len(rows) + 1) * rowh


# ------------------------------------------------------------------ real data
_CACHE = {}


def d(name):
    if name not in _CACHE:
        _CACHE[name] = pd.read_csv(os.path.join(DATA, name + ".csv"))
    return _CACHE[name]


def items():
    """order_items with the line value the answer key uses."""
    if "items_valued" not in _CACHE:
        oi = d("order_items").copy()
        oi["line_ugx"] = oi.quantity * oi.unit_price_ugx * (1 - oi.discount)
        _CACHE["items_valued"] = oi
    return _CACHE["items_valued"]


def order_values():
    """Value of every order, all 6,000 of them."""
    if "order_values" not in _CACHE:
        _CACHE["order_values"] = items().groupby("order_id").line_ugx.sum()
    return _CACHE["order_values"]


def monthly():
    """Delivered revenue by month — the answer key's revenue_by_month_ugx."""
    if "monthly" not in _CACHE:
        j = items().merge(d("orders")[["order_id", "order_date", "status"]],
                          on="order_id")
        j = j[j.status == "Delivered"].copy()
        j["m"] = j.order_date.str[:7]
        _CACHE["monthly"] = j.groupby("m").line_ugx.sum().sort_index()
    return _CACHE["monthly"]


def pct_nearest(sorted_vals, p):
    """The answer key's percentile: nearest rank, no interpolation."""
    n = len(sorted_vals)
    return float(sorted_vals[min(n - 1, int(p / 100.0 * n))])


def mn(x):
    """UGX millions, for an axis tick."""
    return f"{x / 1e6:,.0f}"


def ugx(x):
    return "UGX {:,.0f}".format(x)


def grid(ax, axis="y"):
    ax.grid(axis=axis, color=GRID, lw=1.2)
    ax.set_axisbelow(True)


# =========================================================== 1. table anatomy
def fig_table_anatomy():
    """The Week 1 visual: the five words for the parts of a table."""
    o = d("orders").head(5)
    rows = [(int(r.order_id), int(r.customer_id), r.order_date, r.channel, r.status)
            for r in o.itertuples()]

    fig, ax = canvas(9.2, 4.95)
    title(ax, 0.18, 4.76, "One table. Five words you will hear all term.")

    colw = [1.05, 1.30, 1.25, 1.05, 1.05]      # 5.70 in
    TX, TY, RH = 3.30, 3.82, 0.38
    heads = ["order_id", "customer_id", "order_date", "channel", "status"]
    KEYCOL, CELLROW, CELLCOL, COLCOL = 0, 4, 2, 4

    def cc(i, j, v):
        if (i, j) == (CELLROW, CELLCOL):
            return (FADE_T, TEAL, True)
        if j == KEYCOL:
            return (FADE, ORANGE, True)
        if j == COLCOL:
            return (FADE_B, INK, False)
        return None

    def hc(j):
        return ORANGE if j == KEYCOL else (SLATE if j == COLCOL else None)

    table(ax, TX, TY, colw, RH, heads, rows, cell_col=cc, head_col=hc)
    x_key = TX + colw[0] / 2
    x_cell = TX + sum(colw[:CELLCOL]) + colw[CELLCOL] / 2
    x_col = TX + sum(colw[:COLCOL]) + colw[COLCOL] / 2
    y_bot = TY - 6 * RH

    # ---- above the table
    label(ax, 0.18, 4.18, "HEADER ROW = the FIELD NAMES\nExcel: your top row of labels")
    arrow(ax, (2.80, 4.04), (3.72, 3.86), col=INK, lw=2.0, ms=17)

    label(ax, 5.55, 4.18, "COLUMN = one FIELD\nExcel says column too", col=SLATE)
    arrow(ax, (7.62, 4.06), (x_col, 3.86), col=SLATE, lw=2.0, ms=17)

    # ---- left of the table
    label(ax, 0.18, 2.58, "ROW = one RECORD\nExcel says row too.\nHere: one whole "
                          "order.")
    arrow(ax, (2.30, 2.11), (TX - 0.04, 2.11), col=INK, lw=2.0, ms=17)

    # ---- below the table
    label(ax, 0.18, 1.02, "PRIMARY KEY = an ID never repeated\n"
                          "Excel: the column you would VLOOKUP on", col=ORANGE)
    arrow(ax, (3.28, 1.14), (x_key, y_bot - 0.02), col=ORANGE, lw=2.0, ms=17,
          connectionstyle="arc3,rad=-0.18")

    label(ax, 6.05, 1.00, "CELL = one VALUE\nExcel says cell too", col=TEAL,
          ha="right")
    arrow(ax, (6.12, 1.08), (x_cell, y_bot - 0.02), col=TEAL, lw=2.0, ms=17,
          connectionstyle="arc3,rad=-0.18")

    caption(ax, 0.18, 0.24, "The first five real rows of orders.csv. It is the same "
                            "object you already use in Excel — only the words change.")
    return save_c(fig, "fig_table_anatomy.png")


# =================================================================== 2. grain
def fig_grain():
    """Grain: what one row means, and the double-counting trap."""
    oi = items()
    counts = oi.groupby("order_id").size()
    vals = order_values()
    # three real orders whose line counts are 2, 3, 2 — seven lines in total
    want, chosen = [2, 3, 2], []
    for oid in counts.index:
        if len(chosen) < 3 and counts[oid] == want[len(chosen)]:
            chosen.append(int(oid))
    lines = oi[oi.order_id.isin(chosen)].sort_values(["order_id", "line_no"])
    prod = d("products").set_index("product_id").product_name

    order_rows = [(o, f"{vals[o]:,.0f}") for o in chosen]
    line_rows = [(int(r.order_id), int(r.line_no),
                  prod[r.product_id].replace(" item ", " #"), f"{r.line_ugx:,.0f}")
                 for r in lines.itertuples()]

    right_sum = sum(vals[o] for o in chosen)
    wrong_sum = sum(vals[r[0]] for r in line_rows)
    factor = wrong_sum / right_sum

    fig, ax = canvas(9.2, 5.00)
    title(ax, 0.18, 4.80, "What does ONE ROW mean? Answer that before you add "
                          "anything up.")

    RH = 0.32
    TY = 4.14

    # ---- left: order grain
    L, LW = 0.18, 2.55
    panel(ax, L - 0.06, TY + 0.06, LW, 0.44, face=INK, edge="none", r=0.10, z=1)
    ax.text(L - 0.06 + LW / 2, TY + 0.28, "one row is one ORDER", ha="center",
            va="center", fontsize=12, fontweight="bold", color=PAPER, zorder=3)
    table(ax, L, TY, [1.05, 1.38], RH, ["order_id", "order total"], order_rows)
    label(ax, L, 2.58, f"3 rows. Add the totals:\n{ugx(right_sum)}")

    # ---- right: order-line grain
    R, RW = 3.30, 5.78
    panel(ax, R - 0.06, TY + 0.06, RW, 0.44, face=TEAL, edge="none", r=0.10, z=1)
    ax.text(R - 0.06 + RW / 2, TY + 0.28, "one row is one ORDER LINE", ha="center",
            va="center", fontsize=12, fontweight="bold", color=PAPER, zorder=3)

    def cc(i, j, v):
        return (FADE_T, TEAL, True) if j == 0 else None

    table(ax, R, TY, [1.00, 0.82, 2.60, 1.24], RH,
          ["order_id", "line_no", "product", "line value"], line_rows, cell_col=cc)

    arrow(ax, (2.85, 3.06), (3.24, 3.06), col=MUTED, lw=2.2, ms=20)
    label(ax, R, 1.32, "7 rows, the SAME 3 orders.\norder_id repeats once per line.",
          col=TEAL)

    # ---- the trap
    panel(ax, 0.18, 0.20, 8.84, 0.80, face=FADE, edge=ORANGE, lw=2.0, r=0.10)
    ax.text(0.40, 0.83, f"THE TRAP:  join orders to order lines, add ORDER TOTAL, "
                        f"and you get {ugx(wrong_sum)}",
            ha="left", va="center", fontsize=11.5, fontweight="bold", color=ORANGE,
            zorder=3)
    ax.text(0.40, 0.58, f"{factor:.2f}x too much. Each order total was counted once "
                        "for every line that order has.",
            ha="left", va="center", fontsize=11, color=INK, zorder=3)
    ax.text(0.40, 0.35, "Add a value at the grain it was measured at, or add the line "
                        "values instead.",
            ha="left", va="center", fontsize=11, color=INK, zorder=3)
    return save_c(fig, "fig_grain.png")


# ==================================================================== 3. join
def fig_join():
    """INNER JOIN silently drops the walk-ins. Real counts."""
    o = d("orders")
    c = d("customers")
    walk = o[o.customer_id.isna()].head(1)
    walk_id = int(walk.order_id.iloc[0])
    keep = o[o.customer_id.notna()].head(3)

    rows = [(int(r.order_id), f"{int(r.customer_id)}", r.status)
            for r in keep.itertuples()]
    rows.insert(2, (walk_id, "(blank)", walk.status.iloc[0]))

    cust = c[c.customer_id.isin([int(x) for x in keep.customer_id])]
    crows = [(int(r.customer_id), r.customer_name[:19], r.region)
             for r in cust.itertuples()]

    fig, ax = canvas(9.2, 5.15)
    title(ax, 0.18, 4.98, "A join looks up a value in another table. One kind of join "
                          "throws rows away.", fs=13.0)

    TY, RH = 4.42, 0.38
    panel(ax, 0.12, TY + 0.04, 3.42, 0.42, face=INK, edge="none", r=0.10, z=1)
    ax.text(1.83, TY + 0.25, "orders   (6,000 rows)", ha="center", va="center",
            fontsize=11.5, fontweight="bold", color=PAPER, zorder=3)

    def cc_o(i, j, v):
        return (FADE, ORANGE, True) if i == 2 else None

    table(ax, 0.18, TY, [1.05, 1.30, 0.95], RH,
          ["order_id", "customer_id", "status"], rows, cell_col=cc_o)

    panel(ax, 4.94, TY + 0.04, 4.18, 0.42, face=TEAL, edge="none", r=0.10, z=1)
    ax.text(7.03, TY + 0.25, "customers   (401 rows)", ha="center", va="center",
            fontsize=11.5, fontweight="bold", color=PAPER, zorder=3)
    table(ax, 5.00, TY, [1.30, 1.75, 1.00], RH,
          ["customer_id", "customer_name", "region"], crows, head_bg=TEAL)

    arrow(ax, (3.58, 3.30), (4.93, 3.30), col=TEAL, lw=2.2, ms=20)
    label(ax, 4.25, 3.56, "match on\ncustomer_id", col=TEAL, ha="center")

    label(ax, 0.18, 2.28, f"The third order has no customer_id — it was a walk-in. "
                          f"{da_keys.n(da_keys.WALKINS)} of the 6,000 look like this.",
          col=ORANGE)

    def box(x, w, head, col, face, lines, foot):
        panel(ax, x, 0.62, w, 1.44, face=face, edge=col, lw=2.2, r=0.12)
        ax.text(x + w / 2, 1.86, head, ha="center", va="center", fontsize=12.5,
                fontweight="bold", color=col, zorder=3)
        for k, (a, b) in enumerate(lines):
            y = 1.54 - k * 0.27
            ax.text(x + 0.24, y, a, ha="left", va="center", fontsize=11, color=INK,
                    zorder=3)
            ax.text(x + w - 0.24, y, b, ha="right", va="center", fontsize=11,
                    color=INK, fontweight="bold", zorder=3)
        ax.text(x + w / 2, 0.80, foot, ha="center", va="center", fontsize=11,
                fontweight="bold", color=col, zorder=3)

    box(0.18, 4.34, "INNER JOIN — keeps only matches", ORANGE, FADE,
        [("orders that go in", f"{da_keys.n(da_keys.COUNT_STAR)}"),
         ("rows that come out", f"{da_keys.n(da_keys.COUNT_COL)}"),
         ("dropped, in silence", f"{da_keys.n(da_keys.WALKINS)} walk-ins")],
        f"and {da_keys.m(da_keys.REV_WALKIN)} of trade leaves the report")
    box(4.84, 4.34, "LEFT JOIN — keeps every order", TEAL, FADE_T,
        [("orders that go in", f"{da_keys.n(da_keys.COUNT_STAR)}"),
         ("rows that come out", f"{da_keys.n(da_keys.COUNT_STAR)}"),
         ("region for a walk-in", "blank, and visibly so")],
        "nothing disappears; the gap is on the page")

    caption(ax, 0.18, 0.24, "Real counts. COUNT(*) counts rows; COUNT(customer_id) "
                            f"counts only the filled ones — "
                            f"{da_keys.n(da_keys.COUNT_STAR)} against "
                            f"{da_keys.n(da_keys.COUNT_COL)}.")
    return save_c(fig, "fig_join.png")


# ====================================================== 4. distribution shapes
def fig_distribution_shapes():
    """Three shapes, three verdicts. Simulated, and the caption says so."""
    rng = random.Random(11)
    sym = [rng.gauss(50, 9) for _ in range(4000)]
    skew = [v for v in (math.exp(rng.gauss(0, 0.85)) * 18 for _ in range(4000))
            if v < 260]
    bim = ([rng.gauss(28, 6) for _ in range(2000)]
           + [rng.gauss(72, 7) for _ in range(2000)])

    fig, axes = plt.subplots(1, 3, figsize=(9.5, 4.6))
    spec = [(sym, "SYMMETRIC", INK, "one hump, even sides",
             "mean and median agree\nquote the MEAN"),
            (skew, "RIGHT-SKEWED", ORANGE, "a long tail of big values",
             "the mean is dragged right\nquote the MEDIAN"),
            (bim, "BIMODAL", TEAL, "two humps, so two groups",
             "one average describes neither\nSPLIT them, describe each")]

    for ax, (data, head, col, what, verdict) in zip(axes, spec):
        ax.hist(data, bins=34, color="#8FA6BC", edgecolor=PAPER, lw=0.5)
        srt = sorted(data)
        ax.axvline(sum(srt) / len(srt), color=ORANGE, lw=2.8, ls="--")
        ax.axvline(srt[len(srt) // 2], color=TEAL, lw=2.8, ls=":")
        ax.set_title(head, fontsize=12.5, fontweight="bold", color=col, pad=10)
        ax.set_xlabel(what, fontsize=11, color=BODY, labelpad=8)
        ax.set_yticks([])
        ax.spines["left"].set_visible(False)
        ax.text(0.5, -0.235, verdict, transform=ax.transAxes, ha="center", va="top",
                fontsize=11.5, fontweight="bold", color=col, linespacing=1.45)

    fig.text(0.045, 0.935, "orange dashed = MEAN", fontsize=11.5, color=ORANGE,
             fontweight="bold", va="center")
    fig.text(0.30, 0.935, "teal dotted = MEDIAN", fontsize=11.5, color=TEAL,
             fontweight="bold", va="center")
    fig.text(0.012, 0.028, "Simulated data, drawn to make the three shapes obvious. "
                           "The real course data is the middle shape.",
             fontsize=11, color=BODY, ha="left")
    fig.subplots_adjust(left=0.04, right=0.99, top=0.845, bottom=0.295, wspace=0.14)
    return save_exact(fig, "fig_distribution_shapes.png")


# =============================================================== 5. real skew
def fig_skew_real():
    """The real order-value distribution, with mean and median on it."""
    v = order_values().sort_values()
    mean = float(v.mean())
    med = pct_nearest(v.values, 50)
    CUT = 8e6
    above = int((v > CUT).sum())
    below_mean = float((v < mean).mean()) * 100
    mx = float(v.max())

    fig, ax = plt.subplots(figsize=(9.5, 4.6))
    ax.hist(v[v <= CUT].values, bins=64, color=SLATE, edgecolor=PAPER, lw=0.4)
    ax.axvline(med, color=TEAL, lw=3.0)
    ax.axvline(mean, color=ORANGE, lw=3.0, ls="--")

    top = ax.get_ylim()[1]
    ax.annotate(f"MEDIAN  {ugx(med)}\nhalf of all orders are smaller than this",
                xy=(med, top * 0.52), xytext=(CUT * 0.28, top * 0.80),
                fontsize=11.5, fontweight="bold", color=TEAL, ha="left", va="center",
                linespacing=1.45,
                bbox=dict(boxstyle="round,pad=0.34", fc=PAPER, ec=TEAL, lw=1.6),
                arrowprops=dict(arrowstyle="->", color=TEAL, lw=2.0,
                                connectionstyle="arc3,rad=0.18"))
    ax.annotate(f"MEAN  {ugx(mean)}\n{da_keys.SKEW:.2f}x the median, and bigger than\n"
                f"{below_mean:.0f}% of the orders it is meant to describe",
                xy=(mean, top * 0.22), xytext=(CUT * 0.40, top * 0.42),
                fontsize=11.5, fontweight="bold", color=ORANGE, ha="left",
                va="center", linespacing=1.45,
                bbox=dict(boxstyle="round,pad=0.34", fc=PAPER, ec=ORANGE, lw=1.6),
                arrowprops=dict(arrowstyle="->", color=ORANGE, lw=2.0,
                                connectionstyle="arc3,rad=-0.18"))

    ax.set_xlim(0, CUT)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: mn(x)))
    ax.set_xlabel("Order value (UGX millions)", fontsize=11.5, color=INK, labelpad=8)
    ax.set_ylabel("Number of orders", fontsize=11.5, color=INK)
    ax.set_title("Every order Riverside took in two years, counted into value bands",
                 fontsize=12.5, fontweight="bold", color=INK, loc="left", pad=12)
    grid(ax)
    fig.text(0.012, 0.028,
             f"Real data: all {da_keys.n(len(v))} orders. The chart stops at UGX 8m; "
             f"{above} orders are bigger, the largest being {ugx(mx)}.",
             fontsize=11, color=BODY, ha="left")
    fig.subplots_adjust(left=0.088, right=0.985, top=0.90, bottom=0.215)
    return save_exact(fig, "fig_skew_real.png")


# ============================================================= 6. percentiles
def fig_percentiles():
    """A number line for p10, median, p90 and the max, in plain words."""
    p10, med, p90 = da_keys.P10_ORDER, da_keys.MEDIAN_ORDER, da_keys.P90_ORDER
    mx = da_keys.MAX_ORDER

    fig, ax = canvas(9.2, 4.40)
    title(ax, 0.18, 4.20, "Where does one order sit? Four landmarks in the real data.")

    X0, X1, TOP, Y = 0.60, 6.60, 4.0e6, 2.38

    def sx(v):
        return X0 + (v / TOP) * (X1 - X0)

    ax.plot([X0, X1], [Y, Y], color=INK, lw=4.0, solid_capstyle="butt", zorder=2)
    for v in (1e6, 2e6, 3e6, 4e6):
        ax.plot([sx(v)] * 2, [Y - 0.12, Y], color=MUTED, lw=1.6, zorder=2)
        ax.text(sx(v), Y - 0.30, f"{mn(v)}m", ha="center", va="center", fontsize=11,
                color=BODY)
    ax.text((X0 + X1) / 2, Y - 0.60, "order value, UGX millions", ha="center",
            va="center", fontsize=11.5, color=INK)

    def landmark(x_val, box_x, above, head, words, col):
        x = sx(x_val) if x_val is not None else box_x
        ax.plot([x, x], [Y - 0.20, Y + 0.20], color=col, lw=3.2, zorder=5)
        by = 3.30 if above else 1.12
        ax.plot([x, box_x], [Y + 0.22 if above else Y - 0.22,
                             by - 0.40 if above else by + 0.40],
                color=col, lw=1.6, ls=(0, (3, 3)), zorder=3)
        ax.text(box_x, by, f"{head}\n{words}", ha="center", va="center", fontsize=11.5,
                color=col, fontweight="bold", linespacing=1.5, zorder=6,
                bbox=dict(boxstyle="round,pad=0.30", fc=PAPER, ec=col, lw=1.8))

    landmark(p10, 1.05, True, f"p10   {ugx(p10)}",
             "one order in ten is\nsmaller than this", ORANGE)
    landmark(med, 1.80, False, f"MEDIAN   {ugx(med)}",
             "half the orders are\nsmaller than this", TEAL)
    landmark(p90, 5.55, True, f"p90   {ugx(p90)}",
             "nine orders in ten are\nsmaller than this", SLATE)

    # the axis has to break: the largest order is twelve times the right-hand end
    BX = X1 + 0.16
    for dx in (0.0, 0.15):
        ax.plot([BX + dx - 0.06, BX + dx + 0.06], [Y - 0.16, Y + 0.16], color=PAPER,
                lw=6, zorder=6)
        ax.plot([BX + dx - 0.06, BX + dx + 0.06], [Y - 0.16, Y + 0.16], color=INK,
                lw=2.0, zorder=7)
    ax.plot([BX + 0.28, 8.05], [Y, Y], color=INK, lw=4.0, zorder=2)
    ax.text(BX + 0.06, Y + 0.34, "axis breaks", ha="left", va="center", fontsize=11,
            color=ORANGE, fontweight="bold")
    ax.plot([8.05, 8.05], [Y - 0.20, Y + 0.20], color=INK, lw=3.2, zorder=5)
    ax.plot([8.05, 7.20], [Y - 0.22, 1.52], color=INK, lw=1.6, ls=(0, (3, 3)),
            zorder=3)
    ax.text(7.20, 1.12, f"BIGGEST ORDER   {ugx(mx)}\n{mx / p90:.0f}x the p90 order, "
                        f"{mx / med:.0f}x the median",
            ha="center", va="center", fontsize=11.5, color=INK, fontweight="bold",
            linespacing=1.5, zorder=6,
            bbox=dict(boxstyle="round,pad=0.30", fc=PAPER, ec=INK, lw=1.8))

    caption(ax, 3.30, 1.15, "p10 and the median are\ncrushed into the far left.\n"
                            "That crowding IS the skew.")

    caption(ax, 0.18, 0.36, "Real data: all 6,000 orders. A percentile is a position "
                            "in the queue when you line every")
    caption(ax, 0.18, 0.14, "order up smallest to largest — there is no average in "
                            "it.")
    return save_c(fig, "fig_percentiles.png")


# =========================================================== 7. four charts
def fig_four_charts():
    """Four questions, four chart types, all on the real course data."""
    ms = monthly()
    xs = list(range(len(ms)))
    reg = da_keys.REV_BY_REGION

    cust = d("orders").join(order_values().rename("val"), on="order_id")
    cust = cust[(cust.status == "Delivered") & cust.customer_id.notna()]
    g = cust.groupby("customer_id").agg(n=("order_id", "size"), rev=("val", "sum"))

    v = order_values()

    fig, axes = plt.subplots(2, 2, figsize=(9.5, 5.6))
    (a, b), (c, e) = axes

    a.plot(xs, ms.values / 1e6, color=INK, lw=2.4, marker="o", ms=3.5)
    a.set_title("LINE  —  “is revenue changing over time?”", fontsize=11.5,
                fontweight="bold", color=INK, loc="left", pad=8)
    a.set_xticks([0, 6, 12, 18, 23])
    a.set_xticklabels(["Jan 24", "Jul 24", "Jan 25", "Jul 25", "Dec 25"])
    a.set_ylabel("UGX millions", fontsize=11)
    a.set_ylim(0, 680)
    grid(a)

    names = [r[0] for r in reg][::-1]
    vals = [r[1] / 1e6 for r in reg][::-1]
    b.barh(range(len(vals)), vals, color=["#8FA6BC", "#6B8CA6", SLATE, ORANGE],
           height=0.62)
    b.set_yticks(range(len(vals)))
    b.set_yticklabels(names, fontsize=11)
    for i, val in enumerate(vals):
        b.text(val + 45, i, f"{val:,.0f}m", va="center", fontsize=11, color=INK,
               fontweight="bold")
    b.set_xlim(0, 3050)
    b.set_xticks([])
    b.spines["bottom"].set_visible(False)
    b.spines["left"].set_visible(False)
    b.set_title("BAR  —  “which region sells most?”", fontsize=11.5,
                fontweight="bold", color=INK, loc="left", pad=8)

    c.hist(v[v <= 8e6].values / 1e6, bins=44, color=SLATE, edgecolor=PAPER, lw=0.3)
    c.set_title("HISTOGRAM  —  “what size is a normal order?”", fontsize=11.5,
                fontweight="bold", color=INK, loc="left", pad=8)
    c.set_xlabel("order value, UGX millions", fontsize=11)
    c.set_ylabel("orders", fontsize=11)
    grid(c)

    e.scatter(g.n, g.rev / 1e6, s=26, color=TEAL, alpha=0.62, edgecolors="none")
    e.set_title("SCATTER  —  “more orders, more money?”", fontsize=11.5,
                fontweight="bold", color=INK, loc="left", pad=8)
    e.set_xlabel("delivered orders placed", fontsize=11)
    e.set_ylabel("UGX millions", fontsize=11)
    grid(e)

    fig.text(0.012, 0.020, "All four are real course data: revenue by month, revenue "
                           "by region, all 6,000 order values, one dot per customer.",
             fontsize=11, color=BODY, ha="left")
    fig.subplots_adjust(left=0.088, right=0.985, top=0.945, bottom=0.145,
                        hspace=0.62, wspace=0.30)
    return save_exact(fig, "fig_four_charts.png")


# =========================================================== 8. chart anatomy
def fig_chart_anatomy():
    """Every part of a chart, named, with a numbered key beside it."""
    ms = monthly()
    y24 = [v / 1e6 for k, v in ms.items() if k.startswith("2024")]
    y25 = [v / 1e6 for k, v in ms.items() if k.startswith("2025")]
    mlab = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct",
            "Nov", "Dec"]

    FW, FH = 9.5, 4.7
    fig = plt.figure(figsize=(FW, FH))
    ax = fig.add_axes([0.105, 0.215, 0.475, 0.655])
    ax.plot(range(12), y24, color="#8FA6BC", lw=2.4, marker="o", ms=4, label="2024")
    ax.plot(range(12), y25, color=ORANGE, lw=2.8, marker="o", ms=4, label="2025")
    ax.set_xticks(range(12))
    ax.set_xticklabels(mlab, fontsize=11)
    ax.set_ylim(0, 700)
    ax.set_xlabel("Month of order", fontsize=11.5, color=INK)
    ax.set_ylabel("Delivered revenue (UGX millions)", fontsize=11.5, color=INK)
    ax.set_title("Revenue peaks in December, both years", fontsize=12.5,
                 fontweight="bold", color=INK, loc="left", pad=10)
    ax.legend(frameon=False, fontsize=11, loc="upper left", ncol=2,
              bbox_to_anchor=(0.10, 1.0))
    grid(ax)
    ax.annotate("December is the peak\nin both years", xy=(11, y25[11]),
                xytext=(3.3, 545), fontsize=11, fontweight="bold", color=ORANGE,
                ha="left", va="center", linespacing=1.4,
                bbox=dict(boxstyle="round,pad=0.26", fc=PAPER, ec=ORANGE, lw=1.4),
                arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.8,
                                connectionstyle="arc3,rad=-0.25"))

    # badges beside the part they name, never on top of it
    def chip(bx, by, n):
        ax.add_patch(Ellipse((bx, by), 0.052, 0.075, transform=ax.transAxes,
                             facecolor=INK, edgecolor=PAPER, lw=1.2, zorder=9,
                             clip_on=False))
        ax.text(bx, by, str(n), transform=ax.transAxes, ha="center", va="center",
                fontsize=11, fontweight="bold", color=PAPER, zorder=10, clip_on=False)

    chip(-0.035, 1.085, 1)        # left of the title
    chip(0.0, 0.74, 2)            # on the y axis spine
    chip(-0.155, 0.90, 3)         # above the y axis label
    chip(1.02, 0.0, 4)            # right end of the x axis spine
    chip(-0.045, -0.075, 5)       # left of the first tick label
    chip(0.845, 0.40, 6)          # beside the 2025 series
    chip(0.30, 0.145, 7)          # on the 100m gridline
    chip(0.275, 0.815, 8)         # left of the annotation box
    chip(0.045, 0.955, 9)         # left of the legend

    # the key: its own inch-for-inch axes so the badges stay circular
    kx, ky, kw, kh = 0.615, 0.055, 0.375, 0.885
    axk = fig.add_axes([kx, ky, kw, kh])
    axk.set_xlim(0, kw * FW)
    axk.set_ylim(0, kh * FH)
    axk.axis("off")
    axk.text(0.0, kh * FH - 0.06, "The nine parts. If one is missing,\nsomeone will "
                                  "misread the chart.", fontsize=12,
             fontweight="bold", color=INK, va="top", linespacing=1.45)

    parts = [("TITLE", "what the chart shows, in words"),
             ("Y AXIS", "the thing being measured"),
             ("AXIS LABEL + UNITS", "always state the units"),
             ("X AXIS", "time runs left to right"),
             ("TICKS", "the labelled positions you read off"),
             ("DATA SERIES", "one line is one thing tracked"),
             ("GRIDLINE", "a faint guide for reading across"),
             ("ANNOTATION", "the sentence you want remembered"),
             ("LEGEND", "which line is which; drop if only one")]
    y = kh * FH - 0.86
    for i, (nm, why) in enumerate(parts):
        axk.add_patch(Ellipse((0.16, y), 0.30, 0.30, facecolor=INK, edgecolor="none",
                              zorder=5))
        axk.text(0.16, y, str(i + 1), ha="center", va="center", fontsize=11,
                 fontweight="bold", color=PAPER, zorder=6)
        axk.text(0.42, y + 0.105, nm, fontsize=11.5, fontweight="bold", color=INK,
                 va="center")
        axk.text(0.42, y - 0.105, why, fontsize=11, color=BODY, va="center")
        y -= 0.385

    fig.text(0.012, 0.022, "Real data: delivered revenue by month, 2024 against 2025.",
             fontsize=11, color=BODY, ha="left")
    return save_exact(fig, "fig_chart_anatomy.png")


# =========================================================== 9. axis honesty
def fig_axis_honesty():
    """Same real series, two y axes. One of them lies."""
    ms = monthly()
    y25 = [v / 1e6 for k, v in ms.items() if k.startswith("2025")]
    mlab = ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"]
    jan, feb = y25[0], y25[1]
    fall = (jan - feb) / jan * 100

    fig, axes = plt.subplots(1, 2, figsize=(9.5, 4.7))
    for ax, (lo, head, verdict, col) in zip(axes, [
            (220, "Y AXIS STARTS AT 220m",
             "MISLEADING — the fall fills the\nframe, so it reads as a collapse",
             ORANGE),
            (0, "Y AXIS STARTS AT ZERO",
             "HONEST — you can see how much of\nthe business the fall really was",
             TEAL)]):
        ax.plot(range(12), y25, color=INK, lw=2.8, marker="o", ms=5)
        ax.fill_between(range(12), lo, y25, color=STEEL, alpha=0.7)
        ax.set_ylim(lo, 640)
        ax.set_xticks(range(12))
        ax.set_xticklabels(mlab, fontsize=11)
        ax.set_ylabel("UGX millions", fontsize=11.5, color=INK)
        ax.set_title(head, fontsize=12.5, fontweight="bold", color=col, loc="left",
                     pad=10)
        ax.text(0.5, -0.16, verdict, transform=ax.transAxes, ha="center", va="top",
                fontsize=11.5, fontweight="bold", color=col, linespacing=1.45)
        grid(ax)
        ax.annotate("Feb", xy=(1, feb), xytext=(2.0, lo + (640 - lo) * 0.10),
                    fontsize=11, fontweight="bold", color=ORANGE,
                    arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.8))

    axes[1].text(0.52, 0.80, f"January {jan:,.0f}m → February {feb:,.0f}m\n"
                             f"a fall of {fall:.0f}%",
                 transform=axes[1].transAxes, ha="center", va="center", fontsize=11.5,
                 fontweight="bold", color=INK, linespacing=1.5,
                 bbox=dict(boxstyle="round,pad=0.34", fc=PAPER, ec=INK, lw=1.6))

    fig.text(0.012, 0.024, "Both panels plot exactly the same real numbers: delivered "
                           "revenue by month, 2025. Only the y axis changed.",
             fontsize=11, color=BODY, ha="left")
    fig.subplots_adjust(left=0.085, right=0.985, top=0.89, bottom=0.245, wspace=0.26)
    return save_exact(fig, "fig_axis_honesty.png")


# ========================================================= 10. rate vs count
def fig_rate_vs_count():
    """Counts and rates rank the regions differently. Both are real."""
    cnt = {r[0]: r[1] for r in da_keys.RETURN_COUNT}
    rate = {r[0]: r[1] for r in da_keys.RETURN_RATE}
    order = [r[0] for r in da_keys.RETURN_COUNT]       # ranked by count, descending
    names = order[::-1]
    top_count, top_rate = da_keys.RETURN_COUNT[0][0], da_keys.RETURN_RATE[0][0]

    fig, axes = plt.subplots(1, 2, figsize=(9.5, 4.7))
    a, b = axes

    a.barh(range(4), [cnt[k] for k in names], height=0.6,
           color=[ORANGE if k == top_count else "#8FA6BC" for k in names])
    for i, k in enumerate(names):
        a.text(cnt[k] + 3, i, f"{cnt[k]}", va="center", fontsize=11.5,
               fontweight="bold", color=INK)
    a.set_xlim(0, 152)
    a.set_title("HOW MANY returns  —  a COUNT", fontsize=12.5, fontweight="bold",
                color=INK, loc="left", pad=26)
    a.text(0.0, 1.045, f"{top_count} leads", transform=a.transAxes, fontsize=11.5,
           color=ORANGE, fontweight="bold")

    b.barh(range(4), [rate[k] * 100 for k in names], height=0.6,
           color=[TEAL if k == top_rate else "#8FA6BC" for k in names])
    for i, k in enumerate(names):
        b.text(rate[k] * 100 + 0.06, i, f"{rate[k] * 100:.2f}%", va="center",
               fontsize=11.5, fontweight="bold", color=INK)
    b.set_xlim(0, 3.5)
    b.set_title("HOW OFTEN they return  —  a RATE", fontsize=12.5, fontweight="bold",
                color=INK, loc="left", pad=26)
    b.text(0.0, 1.045, f"{top_rate} leads", transform=b.transAxes, fontsize=11.5,
           color=TEAL, fontweight="bold")

    for ax in axes:
        ax.set_yticks(range(4))
        ax.set_yticklabels(names, fontsize=11.5)
        ax.set_xticks([])
        ax.spines["bottom"].set_visible(False)
        ax.spines["left"].set_visible(False)

    fig.text(0.012, 0.135, f"{top_count} has the most returns — it also has the most "
                           f"order lines. {top_rate} returns most OFTEN,",
             fontsize=11.5, fontweight="bold", color=INK, ha="left")
    fig.text(0.012, 0.088, f"and {top_count} comes LAST on that measure. Same data, "
                           "opposite league table.",
             fontsize=11.5, fontweight="bold", color=INK, ha="left")
    fig.text(0.012, 0.030, "Real data: returns joined to order lines and customers. "
                           "Decide which question you are asking before you pick.",
             fontsize=11, color=BODY, ha="left")
    fig.subplots_adjust(left=0.095, right=0.985, top=0.855, bottom=0.215, wspace=0.30)
    return save_exact(fig, "fig_rate_vs_count.png")


# ============================================================ 11. star schema
def fig_star_schema():
    """One table of events in the middle, lookup tables around it."""
    fig, ax = canvas(9.2, 4.80)
    title(ax, 0.18, 4.62, "How the six tables fit together: one table of events, "
                          "five of labels", fs=13.0)

    BW, BH = 2.40, 0.92
    CX, CY = 4.60, 2.40

    def box(x, y, nm, rows, note, col, face=PAPER, tcol=None, w=BW):
        panel(ax, x - w / 2, y - BH / 2, w, BH, face=face, edge=col, lw=2.2, r=0.12,
              z=3)
        if face is PAPER:
            ax.add_patch(Rectangle((x - w / 2, y - BH / 2), w, 0.055, facecolor=col,
                                   edgecolor="none", zorder=4))
        t = tcol or col
        ax.text(x, y + 0.26, nm, ha="center", va="center", fontsize=12.5,
                fontweight="bold", color=t, zorder=5, family=MONO)
        ax.text(x, y + 0.01, f"{da_keys.n(rows)} rows", ha="center", va="center",
                fontsize=11.5, fontweight="bold", color=t if face is not PAPER else INK,
                zorder=5)
        ax.text(x, y - 0.26, note, ha="center", va="center", fontsize=11,
                color="#FDE4DB" if face is not PAPER else BODY, zorder=5,
                linespacing=1.3)

    box(CX, CY, "order_items", da_keys.ITEMS, "one row = one product on one order",
        ORANGE, face=ORANGE, tcol=PAPER, w=2.95)
    box(CX, 3.83, "orders", da_keys.ORDERS, "one row = one order", TEAL)
    box(CX, 0.97, "products", da_keys.PRODUCTS, "one row = one product", TEAL)
    box(1.10, 3.83, "customers", da_keys.CUSTOMERS, "one row = one customer", SLATE,
        w=2.00)
    box(8.10, 3.83, "reps", da_keys.REPS, "one row = one sales rep", SLATE, w=2.00)
    box(1.10, 2.40, "Dates", 731, "one row = one day", MUTED, w=2.00)

    MO = "many → one"
    arrow(ax, (CX, CY + 0.50), (CX, 3.83 - BH / 2 - 0.04), col=ORANGE, lw=2.2)
    label(ax, CX + 0.16, 3.14, MO, col=ORANGE, fs=11)
    arrow(ax, (CX, CY - 0.50), (CX, 0.97 + BH / 2 + 0.04), col=ORANGE, lw=2.2)
    label(ax, CX + 0.16, 1.70, MO, col=ORANGE, fs=11)

    arrow(ax, (CX - 1.24, 3.83), (2.14, 3.83), col=SLATE, lw=2.2)
    label(ax, 2.75, 4.14, MO, col=SLATE, fs=11, ha="center")
    arrow(ax, (CX + 1.24, 3.83), (7.06, 3.83), col=SLATE, lw=2.2)
    label(ax, 6.45, 4.14, MO, col=SLATE, fs=11, ha="center")
    arrow(ax, (3.46, 3.38), (2.16, 2.78), col=MUTED, lw=2.2)
    label(ax, 2.10, 3.12, MO, col=MUTED, fs=11, ha="right")

    label(ax, 6.20, 1.36, "Arrows point from the MANY\nside to the ONE side.")
    label(ax, 6.20, 0.78, "customers, reps and Dates hang\noff orders — not off "
                          "order_items.", bold=False)

    caption(ax, 0.18, 0.22, "Real row counts from the course data. The Dates table is "
                            "the one you build: 731 days, 1 Jan 2024 to 31 Dec 2025.")
    return save_c(fig, "fig_star_schema.png")


# ============================================================ 12. seasonality
def fig_seasonality():
    """Two Decembers and a rolling average: the pattern, not the wobble."""
    ms = monthly()
    keys = list(ms.index)
    vals = [v / 1e6 for v in ms.values]
    roll = pd.Series(vals).rolling(3).mean()
    dec = [i for i, k in enumerate(keys) if k.endswith("-12")]
    base = sum(v for i, v in enumerate(vals) if i not in dec) / (len(vals) - 2)

    fig, ax = plt.subplots(figsize=(9.5, 4.7))
    ax.bar(range(len(vals)), vals, width=0.72,
           color=[ORANGE if i in dec else "#9FB3C4" for i in range(len(vals))],
           label="delivered revenue in the month")
    ax.plot(range(len(vals)), roll, color=INK, lw=3.0, label="3-month rolling average")

    for i in dec:
        ax.text(i, vals[i] + 14, f"{vals[i]:,.0f}m", ha="center", va="bottom",
                fontsize=11.5, fontweight="bold", color=ORANGE)
        ax.text(i, 24, "DEC", ha="center", va="bottom", fontsize=11,
                fontweight="bold", color=PAPER, rotation=90)

    ax.set_xticks(range(0, len(vals), 3))
    ax.set_xticklabels([keys[i] for i in range(0, len(vals), 3)], fontsize=11)
    ax.set_ylim(0, 700)
    ax.set_ylabel("Delivered revenue (UGX millions)", fontsize=11.5, color=INK)
    ax.set_title("December is the peak in both years — the rest is noise around a "
                 "flat line", fontsize=12.5, fontweight="bold", color=INK, loc="left",
                 pad=12)
    ax.legend(frameon=False, fontsize=11, loc="upper left",
              bbox_to_anchor=(0.005, 1.0), ncol=2)
    ax.text(3.4, 505, f"Both Decembers are about\n"
                      f"{(vals[dec[0]] + vals[dec[1]]) / 2 / base:.1f}x a normal "
                      f"month ({base:,.0f}m)",
            ha="left", va="center", fontsize=11.5, fontweight="bold", color=ORANGE,
            linespacing=1.5,
            bbox=dict(boxstyle="round,pad=0.30", fc=PAPER, ec=ORANGE, lw=1.6))

    grid(ax)
    fig.text(0.012, 0.024, "Real data: delivered revenue by month, all 24 months. The "
                           "rolling average is blank for the first two months.",
             fontsize=11, color=BODY, ha="left")
    fig.subplots_adjust(left=0.088, right=0.985, top=0.885, bottom=0.16)
    return save_exact(fig, "fig_seasonality.png")


# ==================================================================== main
EXPECTED = ["fig_table_anatomy.png", "fig_grain.png", "fig_join.png",
            "fig_distribution_shapes.png", "fig_skew_real.png",
            "fig_percentiles.png", "fig_four_charts.png", "fig_chart_anatomy.png",
            "fig_axis_honesty.png", "fig_rate_vs_count.png", "fig_star_schema.png",
            "fig_seasonality.png"]


def check_against_key():
    """The real-data figures must reproduce the answer key, or they are decoration."""
    v = order_values().sort_values()
    assert len(v) == 6000, len(v)
    assert round(float(v.mean()), 2) == da_keys.MEAN_ORDER
    assert pct_nearest(v.values, 50) == da_keys.MEDIAN_ORDER
    assert pct_nearest(v.values, 10) == da_keys.P10_ORDER
    assert pct_nearest(v.values, 90) == da_keys.P90_ORDER
    assert round(float(v.max()), 2) == da_keys.MAX_ORDER
    ms = monthly()
    key = dict(da_keys.BY_MONTH)
    assert list(ms.index) == sorted(key), "month labels differ from the key"
    for k, val in ms.items():
        assert round(float(val), 2) == key[k], (k, val, key[k])
    assert len(d("orders")) == da_keys.ORDERS
    assert len(d("order_items")) == da_keys.ITEMS
    assert len(d("customers")) == da_keys.CUSTOMERS
    assert len(d("products")) == da_keys.PRODUCTS
    assert len(d("reps")) == da_keys.REPS
    assert len(d("returns")) == da_keys.RETURNS
    assert int(d("orders").customer_id.isna().sum()) == da_keys.WALKINS


def main():
    check_against_key()
    made = [fig_table_anatomy(), fig_grain(), fig_join(),
            fig_distribution_shapes(), fig_skew_real(), fig_percentiles(),
            fig_four_charts(), fig_chart_anatomy(), fig_axis_honesty(),
            fig_rate_vs_count(), fig_star_schema(), fig_seasonality()]

    print(f"{len(made)} figures written to {OUT}\n")
    for p in made:
        with open(p, "rb") as fh:
            head = fh.read(33)
        w = int.from_bytes(head[16:20], "big")
        h = int.from_bytes(head[20:24], "big")
        kb = os.path.getsize(p) / 1024
        print(f"  {os.path.basename(p):<32} {w:>5} x {h:<5} px  "
              f"{w / DPI:>5.2f} x {h / DPI:<4.2f} in  {kb:>7.1f} KB")

    bad = []
    for name in EXPECTED:
        p = os.path.join(OUT, name)
        if not os.path.exists(p):
            bad.append(f"missing: {name}")
        elif os.path.getsize(p) < 10 * 1024:
            bad.append(f"under 10 KB: {name} ({os.path.getsize(p)} bytes)")
    extra = sorted(set(os.path.basename(p) for p in made) - set(EXPECTED))
    if extra:
        bad.append(f"built but not expected: {extra}")
    if bad:
        print("\nFAILED")
        for b in bad:
            print("  -", b)
        return 1
    print(f"\nall {len(EXPECTED)} expected figures present and over 10 KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
