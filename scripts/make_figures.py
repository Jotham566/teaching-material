# -*- coding: utf-8 -*-
"""Teaching figures for the IUEA ML decks. All generated, all labelled honestly."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyBboxPatch, FancyArrowPatch, Rectangle
import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_HERE)

OUT = _ROOT + "/figs"
os.makedirs(OUT, exist_ok=True)

INK = "#1C3144"; ORANGE = "#E4572E"; TEAL = "#2E7D6F"
MUTED = "#6B7A8A"; STEEL = "#E8EDF2"; PAPER = "#FFFFFF"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 12,
    "axes.edgecolor": MUTED, "axes.labelcolor": INK, "text.color": INK,
    "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.facecolor": PAPER, "savefig.facecolor": PAPER,
})


def save(fig, name, dpi=200, pad=0.22):
    p = os.path.join(OUT, name)
    fig.savefig(p, dpi=dpi, bbox_inches="tight", pad_inches=pad)
    plt.close(fig)
    return p


# --------------------------------------------------------------- cohort data
def cohort_data(code, n=90, seed=7):
    """Illustrative data in the shape of each cohort's anchor dataset."""
    rng = np.random.default_rng(seed)
    if code == "CML3112":            # concrete: cement -> strength
        x = rng.uniform(140, 520, n)
        y = 4.5 + 0.098 * x + rng.normal(0, 6.2, n)
        return x, np.clip(y, 3, 85), "Cement content (kg/m³)", "28-day compressive strength (MPa)", "MPa"
    if code == "CML3113":            # flotation: iron feed -> silica concentrate
        x = rng.uniform(43, 65, n)
        y = 14.5 - 0.20 * x + rng.normal(0, 0.55, n)
        return x, np.clip(y, 0.4, 6.0), "Iron content in feed (%)", "Silica in concentrate (%)", "% silica"
    x = rng.uniform(1200, 2800, n)   # machine: speed -> torque
    y = 78 - 0.021 * x + rng.normal(0, 4.2, n)
    return x, np.clip(y, 3, 78), "Rotational speed (rpm)", "Torque (N·m)", "N·m"


LABELS = {
    "CML3112": ("Concrete mixes", "Illustrative data shaped like the Concrete Compressive Strength dataset "
                                  "(UCI 165). You meet the real file in Week 5."),
    "CML3113": ("Flotation batches", "Illustrative data shaped like the froth flotation process dataset "
                                     "(Kaggle). You meet the real file in Week 5."),
    "CML3111": ("Machine-hours", "Illustrative data shaped like the AI4I 2020 Predictive Maintenance dataset "
                                 "(UCI 601). You meet the real file in Week 5."),
}


# =============================================================== 1. data table
def fig_data_table(code):
    """The single most important Week 1 visual: what 'data' means."""
    x, y, xl, yl, unit = cohort_data(code, n=8, seed=3)
    heads = {"CML3112": ["Mix", "Cement\n(kg/m³)", "Water\n(kg/m³)", "Age\n(days)", "STRENGTH\n(MPa)"],
             "CML3113": ["Batch", "Iron feed\n(%)", "Starch\n(m³/h)", "Pulp pH", "SILICA\n(%)"],
             "CML3111": ["Hour", "Speed\n(rpm)", "Torque\n(N·m)", "Tool wear\n(min)", "FAILED?"]}[code]
    rng = np.random.default_rng(11)
    c2 = {"CML3112": rng.uniform(150, 200, 8), "CML3113": rng.uniform(2200, 3200, 8),
          "CML3111": rng.uniform(10, 70, 8)}[code]
    c3 = {"CML3112": rng.choice([7, 28, 28, 56, 90], 8), "CML3113": rng.uniform(9.2, 10.4, 8),
          "CML3111": rng.uniform(0, 250, 8)}[code]
    tgt = ["yes" if v < 40 else "no" for v in y] if code == "CML3111" else [f"{v:.1f}" for v in y]

    fig, ax = plt.subplots(figsize=(11.2, 4.6))
    ax.axis("off")
    ncol, nrow = 5, 9
    cw, ch = 1.0 / ncol, 1.0 / nrow

    for j, h in enumerate(heads):
        is_t = (j == 4)
        ax.add_patch(Rectangle((j * cw, 1 - ch), cw, ch, facecolor=ORANGE if is_t else INK,
                               edgecolor=PAPER, lw=2, transform=ax.transAxes))
        ax.text(j * cw + cw / 2, 1 - ch / 2, h, ha="center", va="center", color=PAPER,
                fontsize=10.5, fontweight="bold", transform=ax.transAxes, linespacing=1.35)

    for i in range(8):
        row = [str(i + 1), f"{x[i]:.0f}", f"{c2[i]:.0f}" if code != "CML3113" else f"{c2[i]:.0f}",
               f"{c3[i]:.1f}" if code == "CML3113" else f"{c3[i]:.0f}", tgt[i]]
        for j, v in enumerate(row):
            is_t = (j == 4)
            ax.add_patch(Rectangle((j * cw, 1 - (i + 2) * ch), cw, ch,
                                   facecolor="#FDEDE8" if is_t else (STEEL if i % 2 else PAPER),
                                   edgecolor="#CDD8E2", lw=1, transform=ax.transAxes))
            ax.text(j * cw + cw / 2, 1 - (i + 1.5) * ch, v, ha="center", va="center",
                    color=ORANGE if is_t else INK, fontsize=11,
                    fontweight="bold" if is_t else "normal", transform=ax.transAxes)

    ax.annotate("one ROW = one example",
                xy=(-0.02, 1 - 3.5 * ch), xytext=(-0.285, 1 - 4.6 * ch),
                xycoords=ax.transAxes, textcoords=ax.transAxes, fontsize=11, color=TEAL,
                fontweight="bold", ha="left", va="center", linespacing=1.4,
                arrowprops=dict(arrowstyle="->", color=TEAL, lw=2.0,
                                connectionstyle="arc3,rad=-0.25"))
    ax.annotate("these columns are the FEATURES\nwhat we know beforehand",
                xy=(0.4, 1.03), xytext=(0.06, 1.20),
                xycoords=ax.transAxes, textcoords=ax.transAxes, fontsize=11, color=INK,
                fontweight="bold", ha="left", va="center", linespacing=1.4,
                arrowprops=dict(arrowstyle="->", color=INK, lw=2.0))
    ax.annotate("this column is the TARGET\nwhat we want to predict",
                xy=(0.9, 1.03), xytext=(0.66, 1.20),
                xycoords=ax.transAxes, textcoords=ax.transAxes, fontsize=11, color=ORANGE,
                fontweight="bold", ha="left", va="center", linespacing=1.4,
                arrowprops=dict(arrowstyle="->", color=ORANGE, lw=2.0))
    return save(fig, f"data_table_{code}.png")


# =============================================================== 2. nested sets
def fig_nested():
    fig, ax = plt.subplots(figsize=(10.6, 5.6))
    ax.set_xlim(0, 10); ax.set_ylim(0, 5.6); ax.axis("off")
    rings = [(5.0, 2.8, 9.4, 5.0, "#DCE4EC", "ARTIFICIAL INTELLIGENCE", 4.9),
             (4.6, 2.6, 7.0, 3.9, "#B9C8D8", "MACHINE LEARNING", 4.05),
             (4.3, 2.45, 4.4, 2.7, "#8FA6BC", "DEEP LEARNING", 3.45),
             (4.15, 2.35, 2.3, 1.5, ORANGE, "GENERATIVE AI", 2.35)]
    for cx, cy, w, h, col, lab, ly in rings:
        ax.add_patch(Ellipse((cx, cy), w, h, facecolor=col, edgecolor=PAPER, lw=2.5))
        ax.text(cx, ly, lab, ha="center", va="center", fontsize=11.5, fontweight="bold",
                color=PAPER if col == ORANGE else INK)
    ax.add_patch(Ellipse((8.05, 1.55), 3.5, 2.5, facecolor=TEAL, alpha=0.30,
                         edgecolor=TEAL, lw=2.5, linestyle="--"))
    ax.text(8.75, 0.62, "DATA SCIENCE", ha="center", va="center", fontsize=11.5,
            fontweight="bold", color=TEAL)
    ax.text(5.0, 0.12, "Data science overlaps all of it and is not contained by any of it — it is the craft of "
                       "getting an answer out of data at all.",
            ha="center", va="center", fontsize=10.5, color=MUTED, style="italic")
    return save(fig, "nested_ai.png")


# =============================================================== 3. rules vs learning
def fig_rules_vs_learning():
    fig, axes = plt.subplots(1, 2, figsize=(12.4, 4.9))
    for ax, (title, boxes, col, foot) in zip(axes, [
        ("TRADITIONAL PROGRAMMING\nwhat you already know",
         ["DATA\nthe crack is 0.42 mm wide", "RULE  ← you write this\nIF width > 0.30 THEN flag",
          "ANSWER\nflag it for repair"], INK,
         "You must know the rule.\nMost engineering works like this."),
        ("MACHINE LEARNING\nwhat is new",
         ["DATA\n4,000 past inspections", "ANSWERS\nwhat the engineer decided each time",
          "RULE  ← the computer works this out"], ORANGE,
         "You do NOT know the rule.\nYou have examples instead.")]):
        ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
        ax.text(5, 9.5, title, ha="center", va="top", fontsize=12.5, fontweight="bold",
                color=col, linespacing=1.5)
        ys = [6.6, 4.3, 2.0]
        for b, y in zip(boxes, ys):
            emph = "←" in b
            ax.add_patch(FancyBboxPatch((0.7, y), 8.6, 1.55, boxstyle="round,pad=0.12,rounding_size=0.2",
                                        facecolor=col if emph else STEEL,
                                        edgecolor=col, lw=2 if emph else 1.2))
            ax.text(5, y + 0.78, b, ha="center", va="center", fontsize=10.8,
                    color=PAPER if emph else INK, fontweight="bold" if emph else "normal",
                    linespacing=1.45)
        for y in (6.35, 4.05):
            ax.add_patch(FancyArrowPatch((5, y), (5, y - 0.42), arrowstyle="-|>",
                                         mutation_scale=20, color=MUTED, lw=2))
        ax.text(5, 0.75, foot, ha="center", va="center", fontsize=10.5, color=MUTED,
                style="italic", linespacing=1.5)
    return save(fig, "rules_vs_learning.png")


# =============================================================== 4. hand prediction
def fig_hand_prediction(code, reveal=False):
    x, y, xl, yl, unit = cohort_data(code, n=12, seed=5)
    order = np.argsort(x); x, y = x[order], y[order]
    xq = float(np.mean(x) * 1.06)
    true = float(np.polyval(np.polyfit(x, y, 1), xq))
    xr = x.max() - x.min()
    yr = y.max() - y.min()

    fig, ax = plt.subplots(figsize=(10.6, 5.4))
    ax.scatter(x, y, s=110, color=INK, zorder=3, label="12 cases you were given")

    # Put annotations in the emptier half of the plot, worked out from the data
    # rather than guessed, so nothing lands on a marker.
    up = (y > true).sum() < (y < true).sum()          # is there more room above?
    ytxt = true + (0.30 if up else -0.30) * yr
    xtxt = xq + 0.16 * xr
    if xtxt + 0.22 * xr > x.max():
        xtxt = xq - 0.34 * xr

    if reveal:
        xs = np.linspace(x.min(), x.max(), 50)
        ax.plot(xs, np.polyval(np.polyfit(x, y, 1), xs), color=TEAL, lw=2.4, ls="--",
                zorder=2, label="the pattern you were sensing")
        guess = true + 0.13 * abs(true)
        ax.scatter([xq], [true], s=300, marker="*", color=ORANGE, zorder=6,
                   label=f"the true answer: {true:.1f} {unit}")
        ax.scatter([xq], [guess], s=130, marker="o", facecolor=PAPER, edgecolor=ORANGE,
                   lw=2.5, zorder=6, label="a typical guess")
        ax.annotate("", xy=(xq, true), xytext=(xq, guess),
                    arrowprops=dict(arrowstyle="<->", color=ORANGE, lw=2.2))
        ax.annotate(f"YOUR ERROR\n{abs(guess - true):.1f} {unit}",
                    xy=(xq, (true + guess) / 2), xytext=(xtxt, ytxt),
                    fontsize=12, fontweight="bold", color=ORANGE, ha="left", va="center",
                    linespacing=1.4,
                    bbox=dict(boxstyle="round,pad=0.32", fc=PAPER, ec=ORANGE, lw=1.4),
                    arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.8,
                                    connectionstyle="arc3,rad=-0.18"))
    else:
        ax.scatter([xq], [true], s=320, marker="o", facecolor=PAPER, edgecolor=ORANGE,
                   lw=2.8, zorder=6)
        ax.text(xq, true, "?", ha="center", va="center", fontsize=15, fontweight="bold",
                color=ORANGE, zorder=7)
        ax.annotate("case 13\nwhat is this value?", xy=(xq, true), xytext=(xtxt, ytxt),
                    fontsize=12, fontweight="bold", color=ORANGE, linespacing=1.4,
                    ha="left", va="center",
                    bbox=dict(boxstyle="round,pad=0.32", fc=PAPER, ec=ORANGE, lw=1.4),
                    arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.8,
                                    connectionstyle="arc3,rad=-0.18"))

    ax.set_xlabel(xl, fontsize=12); ax.set_ylabel(yl, fontsize=12)
    ax.set_xlim(x.min() - 0.09 * xr, x.max() + 0.09 * xr)
    ax.set_ylim(y.min() - 0.16 * yr, y.max() + 0.20 * yr)
    # Legend OUTSIDE the axes so no key can be mistaken for a datum.
    ax.legend(frameon=False, fontsize=10.5, loc="upper center",
              bbox_to_anchor=(0.5, -0.16), ncol=2 if reveal else 1)
    ax.grid(axis="y", color="#E3E9EF", lw=1)
    ax.set_axisbelow(True)
    ax.set_title(LABELS[code][1], fontsize=9.5, color=MUTED, style="italic", loc="left", pad=10)
    return save(fig, f"hand_pred_{'after' if reveal else 'before'}_{code}.png")


# =============================================================== 5. reg vs class
def fig_reg_vs_class(code):
    x, y, xl, yl, unit = cohort_data(code, n=70, seed=9)
    yr = y.max() - y.min()
    fig, axes = plt.subplots(1, 2, figsize=(12.4, 5.0))

    a = axes[0]
    a.scatter(x, y, s=48, color=INK, alpha=0.75)
    xs = np.linspace(x.min(), x.max(), 50)
    a.plot(xs, np.polyval(np.polyfit(x, y, 1), xs), color=ORANGE, lw=2.6)
    a.set_title("REGRESSION — predict a NUMBER", fontsize=12.5, fontweight="bold",
                color=ORANGE, pad=12)
    a.set_xlabel(xl); a.set_ylabel(yl)
    a.text(0.5, -0.20, f'the answer is a quantity: "how many {unit}?"', transform=a.transAxes,
           fontsize=11, style="italic", color=MUTED, ha="center")

    b = axes[1]
    thr = float(np.median(y))
    hi, lo = y >= thr, y < thr
    b.scatter(x[hi], y[hi], s=48, color=TEAL, label="acceptable")
    b.scatter(x[lo], y[lo], s=48, color=ORANGE, marker="X", label="not acceptable")
    b.axhline(thr, color=INK, ls="--", lw=2)
    # label sits clear ABOVE the dashed line, in a white box, so the line cannot
    # read as a strikethrough
    b.text(x.min() + 0.02 * (x.max() - x.min()), thr + 0.055 * yr,
           "the line you must not cross", va="bottom", ha="left", fontsize=10.5, color=INK,
           bbox=dict(boxstyle="round,pad=0.22", fc=PAPER, ec="none", alpha=0.92))
    b.set_title("CLASSIFICATION — predict a CATEGORY", fontsize=12.5, fontweight="bold",
                color=TEAL, pad=12)
    b.set_xlabel(xl); b.set_ylabel(yl)
    b.legend(frameon=False, fontsize=10.5, loc="upper center",
             bbox_to_anchor=(0.5, -0.12), ncol=2)
    b.text(0.5, -0.28, 'the answer is a label: "pass or fail?"', transform=b.transAxes,
           fontsize=11, style="italic", color=MUTED, ha="center")

    for ax in axes:
        ax.set_ylim(y.min() - 0.10 * yr, y.max() + 0.16 * yr)
        ax.grid(axis="y", color="#E3E9EF", lw=1); ax.set_axisbelow(True)
    return save(fig, f"reg_vs_class_{code}.png")


# =============================================================== 6. four limits
def fig_four_limits():
    items = [("NO DATA", "Nobody measured it.\nMuch engineering data was\nnever recorded, or was\nrecorded on paper.", INK),
             ("NO SIGNAL", "The inputs genuinely do not\nrelate to the outcome.\nA model will still produce\nnumbers. That is the danger.", "#4A6B84"),
             ("PHYSICS IS BETTER", "A validated equation exists.\nUse the equation. ML is for\nwhen the relationship is\nunknown or too messy.", TEAL),
             ("THE FUTURE CHANGED", "A model learns yesterday.\nChange the process, material\nor plant and it may quietly\nstop being true.", ORANGE)]
    fig, ax = plt.subplots(figsize=(11.6, 5.3))
    ax.set_xlim(0, 10); ax.set_ylim(0, 5.3); ax.axis("off")
    for i, (t, b, col) in enumerate(items):
        cx, cy = (i % 2) * 5.05, 2.65 - (i // 2) * 2.65
        ax.add_patch(FancyBboxPatch((cx + 0.12, cy + 0.12), 4.75, 2.35,
                                    boxstyle="round,pad=0.06,rounding_size=0.16",
                                    facecolor=STEEL, edgecolor=col, lw=2.2))
        ax.add_patch(Ellipse((cx + 0.62, cy + 1.92), 0.62, 0.44, facecolor=col))
        ax.text(cx + 0.62, cy + 1.92, str(i + 1), ha="center", va="center", color=PAPER,
                fontsize=12, fontweight="bold")
        ax.text(cx + 1.12, cy + 1.92, t, ha="left", va="center", fontsize=12.5,
                fontweight="bold", color=col)
        ax.text(cx + 0.38, cy + 1.42, b, ha="left", va="top", fontsize=10.3, color=INK,
                linespacing=1.55)
    return save(fig, "four_limits.png")


# =============================================================== 7. assessment
def fig_assessment():
    comp = [("Weekly quizzes", 10), ("Weekly challenges", 10), ("Data Analysis Project", 10),
            ("Practical Test 1", 15), ("Practical Test 2", 20), ("Engineering ML Project", 25),
            ("Demo, viva, reflection", 10)]
    labels = [c[0] for c in comp][::-1]
    vals = [c[1] for c in comp][::-1]
    cols = [ORANGE, "#8FA6BC", INK, "#4A6B84", TEAL, "#5E8C7F", "#B9C8D8"][::-1]
    fig, ax = plt.subplots(figsize=(10.6, 4.6))
    ypos = np.arange(len(vals))
    ax.barh(ypos, vals, color=cols, height=0.66)
    for i, v in enumerate(vals):
        ax.text(v + 0.55, i, f"{v}%", va="center", fontsize=12, fontweight="bold", color=INK)
    ax.set_yticks(ypos); ax.set_yticklabels(labels, fontsize=11.5)
    ax.set_xlim(0, 30); ax.set_xticks([])
    ax.spines["bottom"].set_visible(False); ax.spines["left"].set_visible(False)
    ax.set_title("No written examination. 65% of the mark is individual.",
                 fontsize=12, color=MUTED, loc="left", pad=14)
    return save(fig, "assessment.png")


# =============================================================== 8. ladder
def fig_ladder():
    steps = [("Week 1", '"I have never programmed."'),
             ("Week 4", '"I can write and run Python, and read an error."'),
             ("Week 7", '"I can load, clean, analyse and visualise engineering data."'),
             ("Week 10", '"I can train a model and say whether to trust it."'),
             ("Week 12", '"I can choose an approach and defend the choice."'),
             ("Week 15", '"Give me an engineering problem with data and I know how to start."')]
    fig, ax = plt.subplots(figsize=(12.4, 5.2))
    # Bars widen to show progress but are CAPPED, so the label column has a
    # fixed left edge and long text cannot run off the canvas.
    BAR_MAX, TEXT_X = 3.9, 4.25
    ax.set_xlim(0, 12.4); ax.set_ylim(0, 6.9); ax.axis("off")
    for i, (wk, txt) in enumerate(steps):
        y = 0.45 + i * 0.95
        wdt = 1.5 + i * (BAR_MAX - 1.5) / (len(steps) - 1)
        col = ORANGE if i == len(steps) - 1 else ("#B9C8D8" if i < 2 else "#4A6B84")
        ax.add_patch(FancyBboxPatch((0.30, y), wdt, 0.74,
                                    boxstyle="round,pad=0.03,rounding_size=0.12",
                                    facecolor=col, edgecolor="none"))
        ax.text(0.52, y + 0.37, wk, ha="left", va="center", fontsize=10.5,
                fontweight="bold", color=PAPER)
        ax.text(TEXT_X, y + 0.37, txt, ha="left", va="center", fontsize=11.5,
                color=INK, fontweight="bold" if i == len(steps) - 1 else "normal")
    ax.text(0.30, 6.45, "Where this course takes you", fontsize=13, fontweight="bold", color=INK)
    return save(fig, "ladder.png")


# =============================================================== 9. week arc
def fig_arc():
    blocks = [("Weeks 1–4", "Thinking and\nPython", "#B9C8D8"),
              ("Weeks 5–6", "Engineering\ndata", "#8FA6BC"),
              ("Week 7", "TEST 1", ORANGE),
              ("Weeks 8–10", "Machine\nlearning", "#4A6B84"),
              ("Weeks 11–12", "Judgement", TEAL),
              ("Week 13", "Reproducible\nwork", "#5E8C7F"),
              ("Week 14", "TEST 2", ORANGE),
              ("Week 15", "Demo Day", INK)]
    fig, ax = plt.subplots(figsize=(12.6, 3.0))
    ax.set_xlim(0, 10); ax.set_ylim(0, 3.0); ax.axis("off")
    x = 0.1
    for wk, lab, col in blocks:
        w = 1.42 if "TEST" not in lab and "Demo" not in lab else 0.92
        ax.add_patch(FancyBboxPatch((x, 0.75), w - 0.09, 1.55,
                                    boxstyle="round,pad=0.03,rounding_size=0.12",
                                    facecolor=col, edgecolor="none"))
        ax.text(x + (w - 0.09) / 2, 1.93, wk, ha="center", va="center", fontsize=9,
                fontweight="bold", color=PAPER, alpha=0.85)
        ax.text(x + (w - 0.09) / 2, 1.32, lab, ha="center", va="center", fontsize=10,
                fontweight="bold", color=PAPER, linespacing=1.35)
        x += w
    ax.annotate("", xy=(x - 0.05, 0.45), xytext=(0.1, 0.45),
                arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=2.2, mutation_scale=22))
    ax.text(0.1, 0.12, "zero programming experience", fontsize=10, color=MUTED, style="italic")
    ax.text(x - 0.05, 0.12, "an engineering ML practitioner", fontsize=10, color=MUTED,
            style="italic", ha="right")
    return save(fig, "arc.png")


# =============================================================== 10. session clock
def fig_clock():
    segs = [("Welcome and how\nthis course works", 15, "#B9C8D8"),
            ("The whole field,\nstart to finish", 15, "#4A6B84"),
            ("What this course\nis about", 15, "#8FA6BC"),
            ("Two ways to make\na computer decide", 25, "#4A6B84"),
            ("HANDS-ON: predict\ncase 13 on paper", 25, ORANGE),
            ("Break", 10, "#DCE4EC"),
            ("Two kinds\nof question", 15, TEAL),
            ("What ML\ncannot do", 15, "#5E8C7F"),
            ("CHALLENGE:\nProblem Hunt", 30, ORANGE),
            ("Gallery walk\n+ assignment", 10, "#8FA6BC"),
            ("Revision\nmaterial", 5, INK)]
    fig, ax = plt.subplots(figsize=(11.8, 4.4))
    ax.set_xlim(0, 180); ax.set_ylim(0, 2.6); ax.axis("off")
    x = 0
    for i, (lab, mins, col) in enumerate(segs):
        ax.add_patch(Rectangle((x + 0.6, 1.15), mins - 1.2, 0.8, facecolor=col, edgecolor="none"))
        ax.text(x + mins / 2, 1.55, f"{mins}", ha="center", va="center", fontsize=9.5,
                fontweight="bold", color=PAPER if col != "#DCE4EC" else INK)
        ax.text(x + mins / 2, 1.02 if i % 2 == 0 else 0.62, lab, ha="center", va="top",
                fontsize=7.6, color=INK, linespacing=1.3)
        x += mins
    ax.text(0, 2.28, "Three hours, eleven segments — the same shape every week",
            fontsize=12.5, fontweight="bold", color=INK)
    ax.text(0, 2.02, "Numbers are minutes. Nothing here is a lecture longer than 25 minutes.",
            fontsize=10, color=MUTED, style="italic")
    return save(fig, "clock.png")


# =============================================================== 11. roadmap
# Stages taken from the roadmap.sh Machine Learning roadmap, grouped for teaching.
SEM1, SEM2, NOTCOV, HAVE = "SEM 1", "SEM 2", "NOT IN THIS COURSE", "YOU ALREADY HAVE THIS"
COL = {SEM1: ORANGE, SEM2: TEAL, NOTCOV: "#9AA9B6", HAVE: "#4A6B84"}

STAGES = [
    ("1", "Python fundamentals",
     "syntax · variables · data structures\nloops · conditionals · functions\nexceptions", SEM1, "Weeks 2–4"),
    ("2", "Mathematical\nfoundations",
     "calculus · linear algebra\nstatistics · probability", HAVE, "your degree"),
    ("3", "Essential libraries",
     "NumPy · pandas\nMatplotlib · seaborn", SEM1, "Weeks 5–6"),
    ("4", "Data collection",
     "data sources · databases · APIs\nCSV · Excel · JSON · Parquet", SEM1, "Week 5"),
    ("5", "Data cleaning & prep",
     "cleaning · scaling & normalisation\nfeature engineering · selection", SEM1, "Weeks 6, 11"),
    ("6", "What machine\nlearning is",
     "types of ML · supervised\nunsupervised · reinforcement", SEM1, "Weeks 1, 8"),
    ("7", "scikit-learn\nworkflow",
     "data loading · train-test split\nmodel selection · tuning · predict", SEM1, "Weeks 8–12"),
    ("8", "Supervised learning",
     "regression: linear, polynomial\nclassification: KNN, logistic, SVM\ntrees, random forest, boosting", SEM1, "Weeks 8–9, 12"),
    ("9", "Model evaluation",
     "accuracy · precision · recall · F1\nROC-AUC · confusion matrix\nk-fold cross-validation", SEM1, "Week 10"),
    ("10", "Unsupervised learning",
     "clustering · PCA\ndimensionality reduction", SEM2, "Semester 2"),
    ("11", "Deep learning basics",
     "perceptron · MLP · activation\nforward & back propagation\nPyTorch", SEM2, "Semester 2"),
    ("12", "CNNs & computer vision",
     "convolution · pooling · strides\nimage classification\ntransfer learning", SEM2, "Semester 2"),
    ("13", "Sequences & attention",
     "RNN · LSTM · time series\nself-attention · transformers", SEM2, "Semester 2, in part"),
    ("14", "NLP & generative AI",
     "tokenisation · embeddings\nLLMs · retrieval · explainable AI", SEM2, "Semester 2, bounded"),
    ("15", "Reinforcement learning",
     "Q-learning · deep-Q networks\npolicy gradient · actor-critic", NOTCOV, "a later course"),
]


def fig_roadmap_journey():
    fig, ax = plt.subplots(figsize=(13.0, 6.6))
    ax.set_xlim(0, 15); ax.set_ylim(-0.12, 7.5); ax.axis("off")
    ncol, nrow = 3, 5
    cw, chh, gx, gy = 4.72, 1.27, 0.18, 0.105
    for i, (num, name, subs, band, when) in enumerate(STAGES):
        c, r = divmod(i, nrow)
        x = 0.05 + c * (cw + gx)
        y = 6.98 - (r + 1) * (chh + gy)
        col = COL[band]
        ax.add_patch(FancyBboxPatch((x, y), cw, chh, boxstyle="round,pad=0.02,rounding_size=0.10",
                                    facecolor="#F5F8FB", edgecolor=col, lw=2.0))
        ax.add_patch(Rectangle((x, y), 0.085, chh, facecolor=col, edgecolor="none"))
        ax.add_patch(Ellipse((x + 0.42, y + chh - 0.30), 0.44, 0.30, facecolor=col))
        ax.text(x + 0.42, y + chh - 0.30, num, ha="center", va="center", color=PAPER,
                fontsize=9.5, fontweight="bold")
        ax.text(x + 0.75, y + chh - 0.18, name.replace("\n", " "), ha="left", va="top",
                fontsize=10.2, fontweight="bold", color=INK)
        ax.text(x + 0.75, y + chh - 0.56, subs, ha="left", va="top", fontsize=7.7,
                color="#4A5B6B", linespacing=1.42)
        ax.text(x + cw - 0.10, y + 0.09, when, ha="right", va="bottom", fontsize=7.6,
                color=col, fontweight="bold", style="italic")
    hx = 0.05
    for band in (SEM1, SEM2, HAVE, NOTCOV):
        ax.add_patch(Rectangle((hx, 7.15), 0.26, 0.19, facecolor=COL[band], edgecolor="none"))
        ax.text(hx + 0.36, 7.245, band, ha="left", va="center", fontsize=9,
                fontweight="bold", color=COL[band])
        hx += 1.05 + len(band) * 0.105
    ax.text(14.95, 7.245, "structure follows the roadmap.sh Machine Learning roadmap",
            ha="right", va="center", fontsize=8.2, color=MUTED, style="italic")
    return save(fig, "roadmap_journey.png")


def fig_roadmap_coverage():
    rows = [("Programming fundamentals", 100, 0, 0), ("Essential libraries", 100, 0, 0),
            ("Data collection & formats", 85, 15, 0), ("Data cleaning & preprocessing", 90, 10, 0),
            ("What ML is, types of ML", 100, 0, 0), ("scikit-learn workflow", 95, 5, 0),
            ("Supervised learning", 80, 20, 0), ("Model evaluation & validation", 90, 10, 0),
            ("Unsupervised learning", 0, 70, 30), ("Deep learning & CNNs", 0, 65, 35),
            ("Sequences, attention, NLP", 0, 45, 55), ("Reinforcement learning", 0, 0, 100),
            ("MLOps & deployment", 0, 30, 70)]
    labels = [r[0] for r in rows][::-1]
    s1 = np.array([r[1] for r in rows][::-1], float)
    s2 = np.array([r[2] for r in rows][::-1], float)
    no = np.array([r[3] for r in rows][::-1], float)
    fig, ax = plt.subplots(figsize=(12.2, 5.6))
    yp = np.arange(len(labels))
    ax.barh(yp, s1, color=ORANGE, height=0.62, label="Semester 1")
    ax.barh(yp, s2, left=s1, color=TEAL, height=0.62, label="Semester 2")
    ax.barh(yp, no, left=s1 + s2, color="#D6DEE6", height=0.62, label="Not covered")
    ax.set_yticks(yp); ax.set_yticklabels(labels, fontsize=11)
    ax.set_xlim(0, 100); ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xticklabels(["0", "25%", "50%", "75%", "100%"])
    ax.legend(frameon=False, fontsize=10.5, ncol=3, loc="upper center",
              bbox_to_anchor=(0.5, 1.13))
    ax.spines["left"].set_visible(False)
    ax.grid(axis="x", color="#EDF1F5", lw=1); ax.set_axisbelow(True)
    ax.set_title("Honest coverage against the roadmap.sh ML roadmap — the grey is what we do not teach",
                 fontsize=10.5, color=MUTED, loc="left", pad=34, style="italic")
    return save(fig, "roadmap_coverage.png")


def fig_career_paths():
    paths = [("MACHINE LEARNING\nENGINEER",
              "Builds and ships models.\nThis course points here.", ORANGE, True),
             ("AI & DATA\nSCIENTIST", "Finds the answer in the data.\nHeavier statistics.", "#4A6B84", False),
             ("AI ENGINEER", "Builds products on top of\nexisting models and APIs.", TEAL, False),
             ("MLOps ENGINEER", "Keeps models running\nreliably in production.", "#5E8C7F", False)]
    fig, ax = plt.subplots(figsize=(12.6, 4.5))
    ax.set_xlim(0, 12.6); ax.set_ylim(0, 4.5); ax.axis("off")
    ax.text(0.1, 4.25, "Four roles this field splits into — roadmap.sh has a separate roadmap for each",
            fontsize=11.5, fontweight="bold", color=INK)
    w = 2.95
    for i, (t, d, col, main) in enumerate(paths):
        x = 0.1 + i * (w + 0.18)
        ax.add_patch(FancyBboxPatch((x, 0.95), w, 2.85, boxstyle="round,pad=0.03,rounding_size=0.14",
                                    facecolor=col if main else "#F2F6F9",
                                    edgecolor=col, lw=2.2))
        ax.text(x + w / 2, 3.32, t, ha="center", va="center", fontsize=11.5, fontweight="bold",
                color=PAPER if main else col, linespacing=1.4)
        ax.text(x + w / 2, 2.10, d, ha="center", va="center", fontsize=9.6,
                color=PAPER if main else "#41525F", linespacing=1.55)
        if main:
            ax.text(x + w / 2, 1.28, "◆ YOU ARE HERE", ha="center", va="center", fontsize=9,
                    fontweight="bold", color=PAPER)
    ax.text(0.1, 0.42, "An engineer who can do this in their own discipline is rarer, and more useful, "
                       "than a generalist who can do it in none.",
            fontsize=10, color=MUTED, style="italic")
    return save(fig, "career_paths.png")


# ===============================================================================
# WEEKS 2-6 TECHNICAL FIGURES
# ===============================================================================
# Shared helpers -----------------------------------------------------------------
MONO = "DejaVu Sans Mono"
MONO_EM = 0.60205          # advance width of one DejaVu Sans Mono glyph, in em
GREY = "#9AA9B6"           # house colour for "not covered / inactive"
STEEL2 = "#4A6B84"         # mid steel: neutral structure that needs to read as a line
INK2 = "#3A4C5C"           # softer ink for body copy inside a panel
CODE_BG = "#F2F6F9"        # light code panel
CELL_BG = "#FBFCFD"        # notebook cell fill
EDGE = "#CDD8E2"           # light panel border
OUT_BG = "#EDF2F6"         # notebook output strip
DARK = "#16202B"           # terminal panel
RED = "#C0392B"            # ONLY for reproducing Python's own red error text
FADE = "#FDEDE8"           # pale orange wash, matches fig_data_table
FADE_T = "#E4F0ED"         # pale teal wash


def mono_w(nchars, fs):
    """Width in inches of `nchars` characters of DejaVu Sans Mono at `fs` points."""
    return nchars * MONO_EM * fs / 72.0


def mono_x(x0, i, fs):
    """x of the CENTRE of character index `i` (0-based) in a mono run starting at x0."""
    return x0 + (i + 0.5) * MONO_EM * fs / 72.0


CPAD = 0.14   # savefig pad used for canvas() diagrams


def canvas(w, h, y0=0.0):
    """Blank landscape canvas where one data unit == one inch.

    The two invisible corner points anchor the tight bounding box, so the saved
    PNG is always exactly (w + 2*CPAD) x (h + 2*CPAD) inches. That is what keeps
    every diagram inside the 11-13 x 4.5-6.5 in slide budget instead of letting
    bbox_inches="tight" crop to whatever the artists happened to cover.

    y0 shifts the visible window up without touching any drawing coordinate, so
    dead space at the bottom of a layout can be trimmed after inspecting it.
    """
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_position([0, 0, 1, 1])
    ax.set_xlim(0, w)
    ax.set_ylim(y0, y0 + h)
    ax.axis("off")
    ax.scatter([0, w], [y0, y0 + h], s=0.1, alpha=0)
    return fig, ax


def save_c(fig, name):
    """save() for canvas() diagrams: keeps the canvas size, since canvas() already
    builds in its own generous internal margin."""
    return save(fig, name, pad=CPAD)


def panel(ax, x, y, w, h, face=CODE_BG, edge=EDGE, lw=1.4, r=0.10, z=1, ls="solid"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                                facecolor=face, edgecolor=edge, lw=lw, zorder=z,
                                linestyle=ls))


def code(ax, x, y, s, fs=10.5, color=INK, z=3, **kw):
    kw.setdefault("ha", "left")
    kw.setdefault("va", "center")
    return ax.text(x, y, s, fontsize=fs, color=color, family=MONO, zorder=z, **kw)


def badge(ax, x, y, n, col=ORANGE, r=0.125, fs=9.0):
    ax.add_patch(Ellipse((x, y), 2 * r, 2 * r, facecolor=col, edgecolor=PAPER,
                         lw=1.0, zorder=6))
    ax.text(x, y, str(n), ha="center", va="center", fontsize=fs, fontweight="bold",
            color=PAPER, zorder=7)


def arrow(ax, p0, p1, col=MUTED, lw=2.0, style="-|>", ms=18, z=4, **kw):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle=style, mutation_scale=ms,
                                 color=col, lw=lw, zorder=z, **kw))


def caption(ax, x, y, s, fs=10.0, col=MUTED, italic=True, **kw):
    return ax.text(x, y, s, ha="left", va="center", fontsize=fs, color=col,
                   style="italic" if italic else "normal", linespacing=1.5, **kw)


# =============================================================== W2.1 notebook
def fig_notebook_anatomy():
    fig, ax = canvas(12.6, 5.45, y0=0.85)
    ax.text(0.25, 5.98, "What a notebook actually is", fontsize=13.5,
            fontweight="bold", color=INK, va="center")

    # ---- the notebook window
    NB_L, NB_R = 3.15, 8.55
    GUT_L, BODY_L, BODY_R = 3.25, 3.91, 8.42
    panel(ax, NB_L, 1.85, NB_R - NB_L, 3.80, face=PAPER, edge=MUTED, lw=1.8, r=0.12)
    ax.add_patch(FancyBboxPatch((NB_L, 5.25), NB_R - NB_L, 0.40,
                                boxstyle="round,pad=0,rounding_size=0.12",
                                facecolor="#E4EAF0", edgecolor=MUTED, lw=1.8, zorder=2))
    for i, dx in enumerate((0.20, 0.38, 0.56)):
        ax.add_patch(Ellipse((NB_L + dx, 5.45), 0.11, 0.11, facecolor=GREY, zorder=3))
    code(ax, NB_L + 0.78, 5.45, "concrete_week2.ipynb", fs=9.6, color=INK)

    # markdown cell (shown rendered, as it looks after you run it)
    panel(ax, BODY_L, 4.62, BODY_R - BODY_L, 0.53, face="#FCFDFE", edge="#E4EAF0",
          lw=1.2, r=0.06, z=2)
    ax.text(BODY_L + 0.14, 5.00, "Mix trial 1 — cement and water", fontsize=11.5,
            fontweight="bold", color=INK, va="center", zorder=3)
    ax.text(BODY_L + 0.14, 4.76, "We record the mix, then work out the water/cement ratio.",
            fontsize=8.8, color="#44586A", va="center", zorder=3)

    # code cell 1 + its output
    panel(ax, BODY_L, 3.85, BODY_R - BODY_L, 0.70, face=CODE_BG, edge=EDGE, lw=1.2,
          r=0.06, z=2)
    code(ax, GUT_L + 0.05, 4.42, "In [1]:", fs=8.5, color="#3F6D9E")
    for k, ln in enumerate(("cement = 380      # kg/m3",
                            "water  = 175      # kg/m3",
                            'print("loaded")')):
        code(ax, BODY_L + 0.14, 4.40 - k * 0.21, ln, fs=8.8)
    ax.add_patch(Rectangle((BODY_L, 3.40), BODY_R - BODY_L, 0.40, facecolor=OUT_BG,
                           edgecolor="none", zorder=2))
    ax.add_patch(Rectangle((BODY_L, 3.40), 0.035, 0.40, facecolor=GREY,
                           edgecolor="none", zorder=3))
    code(ax, BODY_L + 0.14, 3.60, "loaded", fs=8.8, color="#3A4C5C")

    # code cell 2 + its output
    panel(ax, BODY_L, 2.62, BODY_R - BODY_L, 0.58, face=CODE_BG, edge=EDGE, lw=1.2,
          r=0.06, z=2)
    code(ax, GUT_L + 0.05, 3.08, "In [2]:", fs=8.5, color="#3F6D9E")
    for k, ln in enumerate(("wc = water / cement",
                            'print("w/c ratio:", round(wc, 3))')):
        code(ax, BODY_L + 0.14, 3.06 - k * 0.21, ln, fs=8.8)
    ax.add_patch(Rectangle((BODY_L, 2.06), BODY_R - BODY_L, 0.42, facecolor=OUT_BG,
                           edgecolor="none", zorder=2))
    ax.add_patch(Rectangle((BODY_L, 2.06), 0.035, 0.42, facecolor=GREY,
                           edgecolor="none", zorder=3))
    code(ax, BODY_L + 0.14, 2.27, "w/c ratio: 0.461", fs=8.8, color="#3A4C5C")

    # ---- the kernel
    KL, KR = 9.15, 12.35
    panel(ax, KL, 2.60, KR - KL, 2.70, face="#FEF6F3", edge=ORANGE, lw=2.0, r=0.12)
    ax.text((KL + KR) / 2, 5.06, "THE KERNEL", ha="center", va="center", fontsize=12.5,
            fontweight="bold", color=ORANGE, zorder=3)
    ax.text((KL + KR) / 2, 4.75, "one Python memory, shared by\nevery cell on the page",
            ha="center", va="center", fontsize=9.0, color="#8A5B49", zorder=3,
            linespacing=1.45)
    for k, (nm, val) in enumerate((("cement", "380"), ("water", "175"), ("wc", "0.461"))):
        yy = 4.24 - k * 0.42
        panel(ax, KL + 0.32, yy - 0.15, 2.66, 0.30, face=PAPER, edge="#E8C4B7", lw=1.2,
              r=0.05, z=2)
        code(ax, KL + 0.46, yy, nm, fs=9.6, color=INK)
        code(ax, KL + 2.86, yy, val, fs=9.6, color=ORANGE, ha="right")
    ax.text((KL + KR) / 2, 2.90, "Restart the kernel and every one\nof these boxes empties.",
            ha="center", va="center", fontsize=8.8, color=ORANGE, style="italic",
            zorder=3, linespacing=1.45)

    arrow(ax, (8.62, 4.20), (9.10, 4.20), col=ORANGE, lw=1.8)
    ax.text(8.86, 4.36, "writes", ha="center", va="center", fontsize=7.2, color=ORANGE)
    arrow(ax, (8.62, 2.92), (9.10, 3.36), col=ORANGE, lw=1.8)
    ax.text(8.86, 2.70, "reads &\nwrites", ha="center", va="center", fontsize=7.2,
            color=ORANGE, linespacing=1.4)

    # ---- annotations, ordered so no two leader lines cross
    ann = [(5.10, (BODY_L, 4.88), "MARKDOWN CELL\nYour words, headings, reasoning.\nIt is never run as code.", INK),
           (4.30, (3.26, 4.42), "EXECUTION COUNTER\n[1] means “this was the 1st cell\nactually run” — not the 1st on\nthe page.", ORANGE),
           (3.44, (BODY_L, 4.05), "CODE CELL\nPython. Shift+Enter runs it.", INK),
           (2.30, (BODY_L, 2.27), "OUTPUT AREA\nWhat that cell printed, shown\ndirectly underneath it.", INK)]
    for ty, tgt, txt, col in ann:
        head, body = txt.split("\n", 1)
        ax.annotate(head + "\n" + body, xy=tgt, xytext=(0.25, ty), xycoords="data",
                    textcoords="data", ha="left", va="center", fontsize=9.4,
                    color=col, fontweight="bold", linespacing=1.5,
                    arrowprops=dict(arrowstyle="->", color=col, lw=1.7,
                                    shrinkA=4, shrinkB=3))

    caption(ax, 0.25, 1.48, "A notebook is code, its output and your reasoning in one file. That is why you "
                            "hand in the notebook, not a screenshot.", fs=10.2, col=INK, italic=False)
    caption(ax, 0.25, 1.14, "Illustrative cell contents. The kernel is the part beginners do not see, and the "
                            "part that causes almost every confusing result.", fs=9.4)
    return save_c(fig, "notebook_anatomy.png")


# =============================================================== W2.2 exec trap
def fig_execution_trap():
    fig, ax = canvas(12.6, 4.72, y0=0.42)
    ax.text(0.25, 4.78, "The same cell, run three times", fontsize=13.5,
            fontweight="bold", color=INK, va="center")
    ax.text(0.25, 4.44, "Earlier in the notebook, one cell had already set   readings = 12",
            fontsize=9.8, color=MUTED, va="center")

    cw, gap = 2.80, 0.26
    runs = [("In [3]:", "readings is now 17", "1st press of Shift+Enter"),
            ("In [4]:", "readings is now 22", "2nd press — same cell, again"),
            ("In [5]:", "readings is now 27", "3rd press — same cell, again")]

    def card(x, counter, out, col, face=CODE_BG):
        panel(ax, x, 1.90, cw, 1.90, face=PAPER, edge=col, lw=2.0, r=0.10)
        code(ax, x + 0.16, 3.58, counter, fs=9.0, color="#3F6D9E")
        panel(ax, x + 0.10, 2.86, cw - 0.20, 0.56, face=face, edge="none", lw=0, r=0.05, z=2)
        code(ax, x + 0.20, 3.24, "readings = readings + 5", fs=8.5)
        code(ax, x + 0.20, 3.00, 'print("readings is now", readings)', fs=8.5)
        ax.plot([x + 0.16, x + cw - 0.16], [2.72, 2.72], color=EDGE, lw=1.2, zorder=2)
        ax.text(x + 0.16, 2.58, "Out:", fontsize=7.8, color=MUTED, va="center", zorder=3)
        panel(ax, x + 0.10, 2.00, cw - 0.20, 0.42, face=OUT_BG, edge="none", lw=0, r=0.05, z=2)
        code(ax, x + 0.24, 2.21, out, fs=9.6, color=col, fontweight="bold")

    for i, (counter, out, lab) in enumerate(runs):
        x = 0.25 + i * (cw + gap)
        card(x, counter, out, ORANGE)
        ax.text(x + cw / 2, 3.98, lab, ha="center", va="center", fontsize=8.6, color=MUTED)
        if i < 2:
            # no label here: the 0.26 in gap is too narrow for text without it
            # colliding with the code in the cards either side.
            arrow(ax, (x + cw + 0.03, 2.86), (x + cw + gap - 0.03, 2.86), col=GREY,
                  lw=1.8, ms=14)

    ax.plot([9.30, 9.30], [1.80, 4.14], color=GREY, lw=1.4, ls=(0, (4, 4)), zorder=1)
    card(9.43, "In [2]:", "readings is now 17", TEAL, face=FADE_T)
    ax.text(9.43 + cw / 2, 3.98, "Runtime → Restart and run all", ha="center",
            va="center", fontsize=8.6, color=TEAL, fontweight="bold")
    ax.text(9.43 + cw / 2, 1.74, "back to 17, because the setup cell\nran again first",
            ha="center", va="top", fontsize=8.4, color=TEAL, linespacing=1.45)

    ax.text(0.25, 1.34, "The code never changed. Not one character.",
            fontsize=11.5, fontweight="bold", color=ORANGE, va="center")
    caption(ax, 0.25, 1.02, "The only thing that changed is how many times you pressed the button. The order "
                            "of cells on the page is not the order Python ran them in.", fs=9.8, col=INK,
            italic=False)
    caption(ax, 0.25, 0.70, "Before you submit anything: Restart and run all. If it does not reproduce, it is "
                            "not a result.", fs=9.6)
    return save_c(fig, "execution_trap.png")


# =============================================================== W2.3 git states
def fig_git_states():
    fig, ax = canvas(12.6, 4.30, y0=0.38)
    ax.text(0.25, 4.52, "Four places your work can be. Three commands move it along.",
            fontsize=13.0, fontweight="bold", color=INK, va="center")

    boxes = [("WORKING DIRECTORY", "your files exactly as they\nare right now on this machine", INK),
             ("STAGING AREA", "the changes you have chosen\nto put in the next commit", INK),
             ("LOCAL REPOSITORY", "committed history, still\nonly on this machine", INK),
             ("GITHUB", "the same history on a server,\nwith a URL and a timestamp", ORANGE)]
    cmds = ["git add", "git commit", "git push"]
    bw, bg = 2.45, 0.77
    xs = [0.25 + i * (bw + bg) for i in range(4)]

    for x, (t, d, col) in zip(xs, boxes):
        panel(ax, x, 2.05, bw, 1.70, face=FADE if col is ORANGE else STEEL,
              edge=col, lw=2.0, r=0.12)
        ax.text(x + bw / 2, 3.28, t, ha="center", va="center", fontsize=11.0,
                fontweight="bold", color=col, zorder=3)
        ax.text(x + bw / 2, 2.60, d, ha="center", va="center", fontsize=9.0,
                color="#3A4C5C", linespacing=1.5, zorder=3)

    for i, cmd in enumerate(cmds):
        gx = xs[i] + bw + bg / 2
        arrow(ax, (xs[i] + bw + 0.06, 2.90), (xs[i + 1] - 0.06, 2.90), col=TEAL, lw=2.2, ms=20)
        ax.plot([gx, gx], [3.96, 3.02], color=TEAL, lw=1.0, ls=(0, (2, 3)), zorder=2)
        ax.text(gx, 4.10, cmd, ha="center", va="center", fontsize=10.5, family=MONO,
                fontweight="bold", color=TEAL, zorder=3)

    # git status inspects the first two states only: ring them, don't draw a
    # dashed line that a beginner could read as another flow of work.
    x0, x1 = xs[0] - 0.13, xs[1] + bw + 0.13
    ax.add_patch(FancyBboxPatch((x0, 1.92), x1 - x0, 1.96,
                                boxstyle="round,pad=0,rounding_size=0.16",
                                facecolor="none", edgecolor=ORANGE, lw=1.8,
                                linestyle=(0, (5, 3)), zorder=0))
    mid = (x0 + x1) / 2
    ax.add_patch(Ellipse((mid, 1.92), 0.34, 0.34, facecolor=ORANGE,
                         edgecolor=PAPER, lw=1.5, zorder=4))
    ax.text(mid, 1.92, "?", ha="center", va="center", fontsize=13,
            fontweight="bold", color=PAPER, zorder=5)
    ax.text(mid, 1.57, "git status  —  what have I changed,\nand what have I staged?",
            ha="center", va="top", fontsize=9.4, color=ORANGE, fontweight="bold",
            linespacing=1.5, zorder=3)

    caption(ax, 0.25, 0.88, "Committing does not publish anything. Until you run git push, the work exists on "
                            "one machine only — and one machine is not a backup.", fs=9.8, col=INK,
            italic=False)
    caption(ax, 0.25, 0.56, "git status is free and answers the only two questions you ever have. Run it "
                            "before and after every other command.", fs=9.4)
    return save_c(fig, "git_states.png")


# =============================================================== W2.4 tool map
def fig_tool_map():
    fig, ax = canvas(12.4, 5.32, y0=0.20)
    ax.text(0.25, 5.16, "Four questions, four tools. That is the whole toolkit for now.",
            fontsize=13.0, fontweight="bold", color=INK, va="center")

    pairs = [("Where do I write and run code?", "Google Colab",
              "A notebook that runs on Google's computer,\nnot yours. Nothing to install."),
             ("Where do I see what it did?", "The notebook itself",
              "Code, output and your reasoning in one file.\nThis is what you hand in."),
             ("How do I keep versions and\nprove the work is mine?", "Git  +  GitHub",
              "Version history on your machine, then a\ntimestamped public record of it."),
             ("Where do I find data?", "Kaggle  +  UCI",
              "Free, documented, real engineering datasets.\nYou will use both.")]
    ql, qr = 0.25, 5.55
    tl, tr = 7.45, 12.15
    ys = [4.40, 3.30, 2.20, 1.10]

    for (q, tool, what), y in zip(pairs, ys):
        panel(ax, ql, y - 0.38, qr - ql, 0.76, face=STEEL, edge=MUTED, lw=1.6, r=0.12)
        ax.text(ql + 0.28, y, q, ha="left", va="center", fontsize=11.2, color=INK,
                linespacing=1.45, zorder=3)
        panel(ax, tl, y - 0.44, tr - tl, 0.88, face=FADE, edge=ORANGE, lw=2.0, r=0.12)
        ax.text(tl + 0.28, y + 0.22, tool, ha="left", va="center", fontsize=11.8,
                fontweight="bold", color=ORANGE, zorder=3)
        ax.text(tl + 0.28, y - 0.18, what, ha="left", va="center", fontsize=8.8,
                color="#3A4C5C", linespacing=1.5, zorder=3)
        arrow(ax, (qr + 0.14, y), (tl - 0.14, y), col=MUTED, lw=1.8, ms=17)

    caption(ax, 0.25, 0.36, "Nothing here needs to be installed and nothing here costs money. All four are "
                            "open in a browser tab.", fs=9.8, col=INK, italic=False)
    return save_c(fig, "tool_map.png")


# =============================================================== W3.1 variables
def fig_variable_box():
    fig, ax = canvas(12.4, 4.85, y0=0.45)
    ax.text(0.25, 5.10, "“=” does not mean “equals”.", fontsize=14.5,
            fontweight="bold", color=ORANGE, va="center")
    ax.text(0.25, 4.76, "It means: take the value on the right, and put it in the box named on the left.",
            fontsize=11.0, color=INK, va="center")

    FS, X0 = 26, 0.55                          # the dissected line, in monospace
    cx = lambda a, b: X0 + ((a + b + 1) / 2) * MONO_EM * FS / 72.0
    ex = lambda i: X0 + i * MONO_EM * FS / 72.0

    ax.text(0.28, 4.24, "STEP 1", fontsize=9.0, fontweight="bold", color=MUTED, va="center")
    code(ax, X0, 3.72, "thickness = 0.15", fs=FS, color=INK)
    for a, b in ((0, 8), (10, 10), (12, 15)):
        ax.plot([ex(a) + 0.02, ex(b + 1) - 0.02], [3.46, 3.46], color=ORANGE, lw=2.6,
                solid_capstyle="butt", zorder=3)
    for x, lab, ly in ((cx(0, 8), "the NAME\nof the box", 3.10),
                       (cx(12, 15), "the VALUE\nto store", 3.10),
                       (cx(10, 10), "an instruction, not\na statement of fact", 2.62)):
        ax.plot([x, x], [3.42, ly + 0.21], color=ORANGE, lw=1.0, zorder=2)
        ax.text(x, ly, lab, ha="center", va="center", fontsize=9.4, color=ORANGE,
                fontweight="bold", linespacing=1.5)

    ax.text(0.28, 2.36, "STEP 2", fontsize=9.0, fontweight="bold", color=MUTED, va="center")
    code(ax, X0, 2.03, "thickness = 0.20", fs=FS, color=INK)

    # the box in memory, before and after
    BL, BW = 7.60, 2.80
    ax.text(6.95, 4.58, "the box in memory", fontsize=9.4, color=MUTED, style="italic",
            va="center")
    for y, val in ((3.35, "0.15"), (1.66, "0.20")):
        ax.add_patch(FancyBboxPatch((BL, y + 0.70), 1.55, 0.30,
                                    boxstyle="round,pad=0,rounding_size=0.05",
                                    facecolor=INK, edgecolor="none", zorder=2))
        code(ax, BL + 0.14, y + 0.85, "thickness", fs=10.0, color=PAPER, z=3)
        panel(ax, BL, y, BW, 0.70, face=PAPER, edge=INK, lw=2.2, r=0.06, z=2)
        ax.text(BL + BW / 2, y + 0.35, val, ha="center", va="center", fontsize=20,
                family=MONO, fontweight="bold", color=ORANGE, zorder=3)

    for y, lab in ((3.70, "put this value INTO that box"),
                   (2.01, "put THIS value into the SAME box")):
        arrow(ax, (4.18, y), (BL - 0.08, y), col=ORANGE, lw=2.2, ms=20)
        ax.text((4.18 + BL) / 2, y + 0.19, lab, ha="center", va="center", fontsize=9.4,
                color=ORANGE, fontweight="bold")
    arrow(ax, (11.05, 3.30), (11.05, 2.42), col=INK, lw=2.0, ms=18)
    ax.text(11.20, 2.86, "overwritten", ha="left", va="center", fontsize=8.8, color=INK,
            fontweight="bold")

    caption(ax, 0.25, 1.05, "The box keeps only the latest value. Python does not remember the 0.15 — a "
                            "variable has no history.", fs=10.0, col=INK, italic=False)
    caption(ax, 0.25, 0.72, "Which is why the ORDER of your lines is the whole meaning of your program.", fs=9.6)
    return save_c(fig, "variable_box.png")


# =============================================================== W3.2 functions
def fig_function_anatomy():
    fig, ax = canvas(12.6, 5.10, y0=0.75)
    ax.text(0.30, 5.68, "Anatomy of a function", fontsize=13.5, fontweight="bold",
            color=INK, va="center")

    FS, X0 = 12.5, 0.95
    cw = MONO_EM * FS / 72.0
    ex = lambda i: X0 + i * cw
    cx = lambda a, b: X0 + ((a + b + 1) / 2) * cw

    # ---- the definition
    panel(ax, 0.30, 3.62, 7.90, 1.70, face=CODE_BG, edge=EDGE, lw=1.6, r=0.10)
    code(ax, X0, 4.86, "def slab_volume(length_m, width_m, thickness_m):", fs=FS)
    code(ax, X0, 4.44, '    """Volume of a rectangular slab, in cubic metres."""', fs=FS,
         color=TEAL)
    code(ax, X0, 4.06, "    return length_m * width_m * thickness_m", fs=FS)
    for n, (a, b) in enumerate(((0, 2), (4, 14), (15, 46)), start=1):
        ax.plot([ex(a) + 0.02, ex(b + 1) - 0.03], [4.68, 4.68], color=ORANGE, lw=2.4,
                solid_capstyle="butt", zorder=3)
        badge(ax, cx(a, b), 5.14, n)
    # 4: the docstring line, marked like the tokens above it
    ax.plot([ex(4) + 0.02, ex(56) - 0.03], [4.28, 4.28], color=ORANGE, lw=2.4,
            solid_capstyle="butt", zorder=3)
    badge(ax, ex(56) + 0.16, 4.28, 4)
    # 5: the body is BOTH indented lines, so bracket both of them
    ax.plot([0.86, 0.78, 0.78, 0.86], [4.62, 4.62, 3.92, 3.92], color=ORANGE, lw=2.0,
            solid_capstyle="butt", zorder=3)
    badge(ax, 0.55, 4.27, 5)
    # 6: the return keyword only
    ax.plot([ex(4) + 0.02, ex(10) - 0.03], [3.92, 3.92], color=ORANGE, lw=2.4,
            solid_capstyle="butt", zorder=3)
    badge(ax, cx(4, 9), 3.78, 6)
    caption(ax, 0.30, 3.36, "Python reads these three lines and remembers them. It runs NOTHING yet.",
            fs=10.0, col=ORANGE)

    # ---- the call
    panel(ax, 0.30, 1.30, 7.90, 1.82, face="#FDF3EF", edge=ORANGE, lw=1.8, r=0.10)
    code(ax, X0, 2.68, "v = slab_volume(4.0, 3.0, 0.25)", fs=FS)
    ax.plot([ex(15) + 0.02, ex(31) - 0.03], [2.52, 2.52], color=ORANGE, lw=2.4,
            solid_capstyle="butt", zorder=3)
    badge(ax, cx(15, 30), 2.94, 7)
    code(ax, X0, 2.24, "print(v)", fs=FS)
    ax.text(X0, 1.98, "Out:", fontsize=8.2, color=MUTED, va="center", zorder=3)
    panel(ax, 0.55, 1.44, 2.20, 0.42, face=OUT_BG, edge="none", lw=0, r=0.05, z=2)
    code(ax, 0.72, 1.65, "3.0", fs=FS, color=INK)

    # ---- the numbered legend
    parts = ["def — the keyword. It means: I am defining a\nfunction, not running one.",
             "slab_volume — the NAME. This is what you type\nto use it later.",
             "(length_m, width_m, thickness_m) — the\nPARAMETERS. Empty boxes waiting for values.",
             "The docstring — one line saying what it does\nand in what units. Write this first.",
             "The BODY — the indented lines. Indentation is\nhow Python knows what belongs inside.",
             "return — hands the answer back to whoever\ncalled it. No return hands back None.",
             "The CALL — the ARGUMENTS 4.0, 3.0, 0.25 drop\ninto the parameters, in that order."]
    for i, txt in enumerate(parts):
        y = 5.10 - i * 0.60
        badge(ax, 8.62, y, i + 1)
        ax.text(8.92, y, txt, ha="left", va="center", fontsize=9.4, color=INK,
                linespacing=1.5)

    caption(ax, 0.30, 1.00, "The names in the definition and the values in the call are matched by POSITION. "
                            "4.0 becomes length_m because it is first.", fs=9.6, col=INK, italic=False)
    return save_c(fig, "function_anatomy.png")


# =============================================================== W3.3 traceback
# The panel below reproduces, character for character, the output of running:
#
#   $ python3 site_survey.py
#
# where site_survey.py is
#
#   def mean_reading(rows):
#       total = 0
#       for r in rows:
#           total = total + r
#       return total / len(rows)
#
#   readings = ["12.4", "13.1", "11.8"]
#   print(mean_reading(readings))
#
# Python 3.10.12. The only edit is the folder part of the two File paths, which
# has been trimmed to the bare file name so the lines fit on a slide.
TRACEBACK = [
    "Traceback (most recent call last):",
    '  File "site_survey.py", line 9, in <module>',
    "    print(mean_reading(readings))",
    '  File "site_survey.py", line 4, in mean_reading',
    "    total = total + r",
    "TypeError: unsupported operand type(s) for +: 'int' and 'str'",
]


def fig_traceback_anatomy():
    fig, ax = canvas(12.6, 5.28, y0=0.72)
    ax.text(0.30, 5.85, "Read a traceback from the BOTTOM UP", fontsize=13.5,
            fontweight="bold", color=INK, va="center")

    PL, PR = 0.95, 8.35
    panel(ax, PL, 2.62, PR - PL, 2.90, face=DARK, edge=DARK, lw=1.0, r=0.08)
    FS, X0 = 11.0, 1.20
    ys = [5.22 - k * 0.44 for k in range(6)]
    for y, shade in ((ys[3], "#243444"), (ys[4], "#243444"), (ys[5], "#33465C")):
        ax.add_patch(Rectangle((PL + 0.10, y - 0.19), 7.00, 0.38, facecolor=shade,
                               edgecolor="none", zorder=2))
    for y, ln in zip(ys, TRACEBACK):
        code(ax, X0, y, ln, fs=FS, color="#E6EDF3", z=3)

    arrow(ax, (0.55, 2.95), (0.55, 5.15), col=ORANGE, lw=2.4, ms=20)
    ax.text(0.28, 4.05, "read upwards", rotation=90, ha="center", va="center",
            fontsize=9.0, fontweight="bold", color=ORANGE)

    # the error-type token, boxed and called out below the panel
    cwid = MONO_EM * FS / 72.0
    tk_l, tk_r = X0 - 0.04, X0 + 9 * cwid + 0.02
    ax.add_patch(Rectangle((tk_l, ys[5] - 0.17), tk_r - tk_l, 0.34, facecolor="none",
                           edgecolor=ORANGE, lw=1.8, zorder=4))
    arrow(ax, ((tk_l + tk_r) / 2, 2.28), ((tk_l + tk_r) / 2, ys[5] - 0.20),
          col=ORANGE, lw=1.7, ms=15)
    badge(ax, 0.62, 2.10, 2)
    ax.text(0.85, 2.10, "TypeError names the error TYPE — the kind of\nmistake, not the cause.",
            ha="left", va="center", fontsize=9.4, color=ORANGE, fontweight="bold",
            linespacing=1.5)

    notes = [(2.80, ys[5], 1, "START HERE. The last line says WHAT went wrong,\nin plain words."),
             (3.46, ys[4], 3, "This is the line of code that actually failed."),
             (4.05, ys[3], 4, "This is WHERE — the file, and the line number in it."),
             (4.90, ys[1], 5, "Above that is the chain of calls that got you there.\nRead it only if the bottom two lines are not enough.")]
    for ty, tgt_y, n, txt in notes:
        badge(ax, PR - 0.20, tgt_y, n)
        ax.annotate(txt, xy=(PR - 0.02, tgt_y), xytext=(8.90, ty), xycoords="data",
                    textcoords="data", ha="left", va="center", fontsize=9.4,
                    color=INK, linespacing=1.5,
                    arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.6,
                                    shrinkA=4, shrinkB=2))

    caption(ax, 0.30, 1.42, "The rule: read the last line, then the line above it. Those two answer it nine "
                            "times out of ten.", fs=10.0, col=INK, italic=False)
    caption(ax, 0.30, 1.02, "Real output, copied from actually running the file on Python 3.10.12. Only the "
                            "folder part of the two paths has\nbeen trimmed to fit the slide. Python 3.11 and "
                            "later also print a ^^^^ marker under the exact expression that failed.", fs=9.0)
    return save_c(fig, "traceback_anatomy.png")


# =============================================================== W3.4 silent wrong
def fig_silent_wrong():
    fig, ax = canvas(12.6, 5.03, y0=0.42)
    ax.text(0.25, 5.30, "Two kinds of mistake. Only one of them tells you.",
            fontsize=13.5, fontweight="bold", color=INK, va="center")

    L0, L1 = 0.25, 6.20
    R0, R1 = 6.65, 12.35

    # ---------------- panel 1: it crashes
    panel(ax, L0, 0.95, L1 - L0, 3.95, face=PAPER, edge=MUTED, lw=1.8, r=0.12)
    ax.add_patch(FancyBboxPatch((L0, 4.35), L1 - L0, 0.55,
                                boxstyle="round,pad=0,rounding_size=0.12",
                                facecolor=MUTED, edgecolor="none", zorder=2))
    ax.text(L0 + 0.28, 4.62, "1.   IT CRASHES", fontsize=12.0, fontweight="bold",
            color=PAPER, va="center", zorder=3)
    panel(ax, L0 + 0.20, 3.28, L1 - L0 - 0.40, 0.86, face=CODE_BG, edge=EDGE, lw=1.2,
          r=0.06, z=2)
    code(ax, L0 + 0.36, 3.85, 'readings = "12.4"        # text, straight from a file', fs=8.8)
    code(ax, L0 + 0.36, 3.57, "total = 0 + readings", fs=8.8)
    panel(ax, L0 + 0.20, 1.98, L1 - L0 - 0.40, 1.20, face="#FCEEEC", edge=RED, lw=1.4,
          r=0.06, z=2)
    for k, ln in enumerate(["Traceback (most recent call last):",
                            '  File "check.py", line 2, in <module>',
                            "    total = 0 + readings",
                            "TypeError: unsupported operand type(s) for +: 'int' and 'str'"]):
        code(ax, L0 + 0.34, 3.00 - k * 0.27, ln, fs=8.0, color=RED)
    ax.text(L0 + 0.28, 1.62, "SAFE.  Python refuses to go on.", fontsize=11.2,
            fontweight="bold", color=TEAL, va="center", zorder=3)
    ax.text(L0 + 0.28, 1.30, "Annoying, and you will find it in seconds. It cannot\nreach a report.",
            fontsize=9.2, color="#3A4C5C", va="center", linespacing=1.5, zorder=3)

    # ---------------- panel 2: it answers, wrongly
    panel(ax, R0, 0.95, R1 - R0, 3.95, face=FADE, edge=ORANGE, lw=2.6, r=0.12)
    ax.add_patch(FancyBboxPatch((R0, 4.35), R1 - R0, 0.55,
                                boxstyle="round,pad=0,rounding_size=0.12",
                                facecolor=ORANGE, edgecolor="none", zorder=2))
    ax.text(R0 + 0.28, 4.62, "2.   IT ANSWERS, AND THE ANSWER IS WRONG",
            fontsize=12.0, fontweight="bold", color=PAPER, va="center", zorder=3)
    panel(ax, R0 + 0.20, 3.28, R1 - R0 - 0.40, 0.86, face=PAPER, edge=EDGE, lw=1.2,
          r=0.06, z=2)
    code(ax, R0 + 0.36, 3.98, "thickness_m = 250        # 250 mm, in a metres box", fs=8.8)
    code(ax, R0 + 0.36, 3.71, "volume_m3 = 4.0 * 3.0 * thickness_m", fs=8.8)
    code(ax, R0 + 0.36, 3.44, "print(volume_m3)", fs=8.8)
    panel(ax, R0 + 0.20, 1.98, R1 - R0 - 0.40, 1.20, face=PAPER, edge=EDGE, lw=1.4,
          r=0.06, z=2)
    code(ax, R0 + 0.34, 2.92, "3000.0", fs=15.0, color=INK, fontweight="bold")
    ax.text(R0 + 0.34, 2.40, "No error. No warning. Nothing red.\nJust a number, ready to be copied into a report.",
            fontsize=9.2, color=MUTED, va="center", linespacing=1.55, zorder=3,
            style="italic")
    ax.text(R0 + 0.28, 1.62, "DANGEROUS.  It is out by a factor of 1000.", fontsize=11.2,
            fontweight="bold", color=ORANGE, va="center", zorder=3)
    ax.text(R0 + 0.28, 1.30, "The slab is 3.0 m³ — about 7 tonnes at 2,400 kg/m³.\n3000 m³ would be 7,200 tonnes. Somebody would order it.",
            fontsize=9.2, color="#3A4C5C", va="center", linespacing=1.5, zorder=3)

    caption(ax, 0.25, 0.60, "The one that crashes is not the dangerous one. Put the unit in every variable "
                            "name, and check every result against a number you already know.", fs=10.0,
            col=INK, italic=False)
    return save_c(fig, "silent_wrong.png")


# --------------------------------------------------- Week 4 shared trace values
# One set of readings used by accumulator_trace and accumulator_bug, so the two
# figures agree with each other. Every total below is computed, never typed.
TRACE = [12.4, 13.1, 11.8, 12.9, 13.5, 12.7]


def _accumulate(vals, reset_inside):
    """Return the per-iteration trace of the loop, correct or buggy."""
    rows, total, count = [], 0, 0
    for i, v in enumerate(vals, start=1):
        if reset_inside:
            total = 0
        total = total + v
        count = count + 1
        rows.append((i, v, total, count))
    return rows, total, count


def _table(ax, x, y, colw, rowh, heads, rows, *, head_bg=INK, fs=10.0, head_fs=9.4,
           cell_fs=10.0, zebra=True, cell_col=None, head_col=None, z=2):
    """Draw a plain grid table. Returns (right_x, bottom_y).

    cell_col(i, j, value) may return a (facecolor, textcolor, bold) triple to
    override one cell; head_col(j) may return a facecolor for one header.
    """
    ncol = len(heads)
    for j, h in enumerate(heads):
        hb = (head_col(j) if head_col else None) or head_bg
        ax.add_patch(Rectangle((x + sum(colw[:j]), y - rowh), colw[j], rowh,
                               facecolor=hb, edgecolor=PAPER, lw=1.6, zorder=z))
        ax.text(x + sum(colw[:j]) + colw[j] / 2, y - rowh / 2, h, ha="center",
                va="center", color=PAPER, fontsize=head_fs, fontweight="bold",
                zorder=z + 1, linespacing=1.3)
    for i, row in enumerate(rows):
        yy = y - (i + 2) * rowh
        for j in range(ncol):
            face = (STEEL if (zebra and i % 2) else PAPER)
            txt, bold = str(row[j]), False
            over = cell_col(i, j, row[j]) if cell_col else None
            tcol = INK
            if over:
                face, tcol, bold = over
            ax.add_patch(Rectangle((x + sum(colw[:j]), yy), colw[j], rowh,
                                   facecolor=face, edgecolor="#CDD8E2", lw=1.0, zorder=z))
            ax.text(x + sum(colw[:j]) + colw[j] / 2, yy + rowh / 2, txt, ha="center",
                    va="center", color=tcol, fontsize=cell_fs,
                    fontweight="bold" if bold else "normal", zorder=z + 1,
                    family=MONO if j else None)
    return x + sum(colw), y - (len(rows) + 1) * rowh


# =============================================================== W4.1 list/dict
def fig_list_vs_dict():
    fig, ax = canvas(12.5, 5.15, y0=0.30)
    ax.text(0.25, 5.22, "Two ways to hold more than one number", fontsize=13.5,
            fontweight="bold", color=INK, va="center")

    vals = [12.4, 13.1, 11.8, 12.9]
    wear = [("UNIT_07", 143), ("UNIT_12", 88), ("UNIT_21", 201)]

    # ---------------- a LIST: found by position
    L0, L1 = 0.25, 6.05
    panel(ax, L0, 1.30, L1 - L0, 3.55, face=PAPER, edge=INK, lw=1.8, r=0.12)
    ax.add_patch(FancyBboxPatch((L0, 4.30), L1 - L0, 0.55,
                                boxstyle="round,pad=0,rounding_size=0.12",
                                facecolor=INK, edgecolor="none", zorder=2))
    ax.text(L0 + 0.26, 4.57, "A LIST  —  found by POSITION", fontsize=11.8,
            fontweight="bold", color=PAPER, va="center", zorder=3)
    code(ax, L0 + 0.26, 3.98, "readings = [12.4, 13.1, 11.8, 12.9]", fs=10.0, z=3)
    bw, gap = 1.06, 0.16
    bx = L0 + 0.42
    for i, v in enumerate(vals):
        x = bx + i * (bw + gap)
        ax.text(x + bw / 2, 3.52, f"[{i}]", ha="center", va="center", fontsize=10.5,
                family=MONO, fontweight="bold", color=ORANGE, zorder=3)
        panel(ax, x, 2.80, bw, 0.56, face=STEEL, edge=MUTED, lw=1.4, r=0.06, z=2)
        ax.text(x + bw / 2, 3.08, f"{v}", ha="center", va="center", fontsize=11.5,
                family=MONO, color=INK, zorder=3)
    ax.text(bx, 2.56, "the positions are not stored — they are just where things sit",
            fontsize=8.4, color=MUTED, style="italic", va="center", zorder=3)
    panel(ax, L0 + 0.26, 1.52, 3.10, 0.52, face=FADE, edge=ORANGE, lw=1.5, r=0.06, z=2)
    code(ax, L0 + 0.42, 1.78, "readings[1]   →   13.1", fs=10.5, color=ORANGE, z=3)
    ax.text(L0 + 3.58, 1.78, "counting starts at 0,\nso [1] is the SECOND one",
            fontsize=8.8, color=ORANGE, fontweight="bold", va="center",
            linespacing=1.5, zorder=3)

    # ---------------- a DICT: found by name
    R0, R1 = 6.45, 12.25
    panel(ax, R0, 1.30, R1 - R0, 3.55, face=PAPER, edge=TEAL, lw=1.8, r=0.12)
    ax.add_patch(FancyBboxPatch((R0, 4.30), R1 - R0, 0.55,
                                boxstyle="round,pad=0,rounding_size=0.12",
                                facecolor=TEAL, edgecolor="none", zorder=2))
    ax.text(R0 + 0.26, 4.57, "A DICTIONARY  —  found by NAME", fontsize=11.8,
            fontweight="bold", color=PAPER, va="center", zorder=3)
    code(ax, R0 + 0.26, 3.98,
         'wear = {"UNIT_07": 143, "UNIT_12": 88, "UNIT_21": 201}', fs=10.0, z=3)
    kw, kgap = 1.66, 0.18
    kx = R0 + 0.30
    for i, (k, v) in enumerate(wear):
        x = kx + i * (kw + kgap)
        ax.text(x + kw / 2, 3.52, f'["{k}"]', ha="center", va="center", fontsize=9.4,
                family=MONO, fontweight="bold", color=TEAL, zorder=3)
        panel(ax, x, 2.80, kw, 0.56, face=FADE_T, edge=TEAL, lw=1.4, r=0.06, z=2)
        ax.text(x + kw / 2, 3.08, str(v), ha="center", va="center", fontsize=11.5,
                family=MONO, color=INK, zorder=3)
    ax.text(kx, 2.56, "the name IS stored — it is half of the data",
            fontsize=8.4, color=MUTED, style="italic", va="center", zorder=3)
    panel(ax, R0 + 0.26, 1.52, 3.10, 0.52, face=FADE_T, edge=TEAL, lw=1.5, r=0.06, z=2)
    code(ax, R0 + 0.42, 1.78, 'wear["UNIT_07"] → 143', fs=10.5, color=TEAL, z=3)
    ax.text(R0 + 3.58, 1.78, "no counting, and the\norder does not matter",
            fontsize=8.8, color=TEAL, fontweight="bold", va="center",
            linespacing=1.5, zorder=3)

    ax.text(0.25, 0.96, "Choose a LIST when the order is the meaning: a column of readings, "
                        "a time series, a set of samples in the order taken.",
            fontsize=9.8, color=INK, va="center")
    ax.text(0.25, 0.66, "Choose a DICTIONARY when you look things up by a label: a machine ID, "
                        "a mix code, a borehole name.",
            fontsize=9.8, color=INK, va="center")
    return save_c(fig, "list_vs_dict.png")


# =============================================================== W4.2 acc trace
def fig_accumulator_trace():
    rows, total, count = _accumulate(TRACE, reset_inside=False)
    fig, ax = canvas(12.5, 4.92, y0=0.66)
    ax.text(0.25, 5.36, "What the loop is actually doing, one line at a time",
            fontsize=13.5, fontweight="bold", color=INK, va="center")

    panel(ax, 0.25, 2.04, 5.05, 2.62, face=CODE_BG, edge=EDGE, lw=1.6, r=0.10)
    for k, ln in enumerate(["readings = [12.4, 13.1, 11.8,",
                            "            12.9, 13.5, 12.7]",
                            "",
                            "total = 0",
                            "count = 0",
                            "for r in readings:",
                            "    total = total + r",
                            "    count = count + 1",
                            "",
                            "mean = total / count"]):
        code(ax, 0.48, 4.42 - k * 0.245, ln, fs=10.0,
             color=ORANGE if ln.strip().startswith(("total =", "count =")) else INK)
    ax.text(0.25, 1.76, "Nothing magic happens. The two boxes are just overwritten, six times.",
            fontsize=9.6, color=MUTED, style="italic", va="center")

    heads = ["iteration", "r\n(the value read)", "total\nafter this line",
             "count\nafter this line"]
    colw = [1.28, 1.72, 1.72, 1.72]
    TX, TY = 5.70, 4.66
    body = [(i, f"{v:.1f}", f"{t:.1f}", c) for i, v, t, c in rows]

    def cc(i, j, v):
        if j == 2:
            return ("#FDEDE8", ORANGE, True)
        return None

    rx, by = _table(ax, TX, TY, colw, 0.42, heads, body, cell_col=cc, head_fs=8.4,
                    cell_fs=10.0)
    ax.add_patch(Rectangle((TX, by - 0.50), sum(colw), 0.50, facecolor=TEAL,
                           edgecolor=PAPER, lw=1.6, zorder=2))
    ax.text(TX + 0.22, by - 0.25, "mean  =  total / count", ha="left", va="center",
            fontsize=10.0, family=MONO, color=PAPER, zorder=3)
    ax.text(rx - 0.22, by - 0.25, f"=  {total / count:.2f}", ha="right", va="center",
            fontsize=11.0, family=MONO, fontweight="bold", color=PAPER, zorder=3)
    ax.text(TX, by - 0.76, f"Totals shown to 1 d.p. In full, total = {total!r} — "
                           "binary cannot store 12.4 exactly.",
            fontsize=8.4, color=MUTED, style="italic", va="center")
    return save_c(fig, "accumulator_trace.png")


# =============================================================== W4.3 acc bug
def fig_accumulator_bug():
    ok_rows, ok_total, n = _accumulate(TRACE, reset_inside=False)
    bad_rows, bad_total, _ = _accumulate(TRACE, reset_inside=True)
    fig, ax = canvas(12.6, 5.88, y0=0.28)
    ax.text(0.25, 5.98, "One line in the wrong place. The same loop, two different answers.",
            fontsize=13.5, fontweight="bold", color=INK, va="center")

    def side(x0, w, tag, tagcol, lines, hl, rows, tot, verdict, vsub):
        ax.add_patch(FancyBboxPatch((x0, 5.10), w, 0.50,
                                    boxstyle="round,pad=0,rounding_size=0.10",
                                    facecolor=tagcol, edgecolor="none", zorder=2))
        ax.text(x0 + 0.22, 5.35, tag, fontsize=11.5, fontweight="bold", color=PAPER,
                va="center", zorder=3)
        panel(ax, x0, 3.84, w, 1.24, face=CODE_BG, edge=EDGE, lw=1.4, r=0.08)
        for k, ln in enumerate(lines):
            emph = (k == hl)
            if emph:
                ax.add_patch(Rectangle((x0 + 0.10, 4.84 - k * 0.26 - 0.13), w - 0.20,
                                       0.26, facecolor=FADE if tagcol is ORANGE else FADE_T,
                                       edgecolor="none", zorder=2))
            code(ax, x0 + 0.24, 4.84 - k * 0.26, ln, fs=9.6,
                 color=tagcol if emph else INK,
                 fontweight="bold" if emph else "normal", z=3)
        body = [(i, f"{v:.1f}", f"{t:.1f}") for i, v, t, _ in rows]
        _table(ax, x0 + 0.28, 3.68, [1.05, 1.60, 1.95], 0.32,
               ["iter", "r", "total after"], body, cell_fs=9.6, head_fs=8.8,
               head_bg=INK,
               cell_col=lambda i, j, v: ("#FDEDE8" if tagcol is ORANGE else FADE_T,
                                         tagcol, True) if j == 2 else None)
        ax.add_patch(FancyBboxPatch((x0 + 0.28, 0.68), 4.60, 0.66,
                                    boxstyle="round,pad=0,rounding_size=0.08",
                                    facecolor=tagcol, edgecolor="none", zorder=2))
        ax.text(x0 + 0.50, 1.12, verdict, fontsize=10.5, fontweight="bold",
                color=PAPER, va="center", zorder=3)
        ax.text(x0 + 0.50, 0.88, vsub, fontsize=9.0, color=PAPER, va="center", zorder=3)

    ok_lines = ["total = 0            ← BEFORE the loop",
                "for r in readings:",
                "    total = total + r",
                "mean = total / len(readings)"]
    bad_lines = ["for r in readings:",
                 "    total = 0        ← INSIDE the loop",
                 "    total = total + r",
                 "mean = total / len(readings)"]
    side(0.25, 5.15, "CORRECT   —   total = 0 sits BEFORE the loop", TEAL,
         ok_lines, 0, ok_rows, ok_total,
         f"total = {ok_total:.1f}      mean = {ok_total / n:.2f}",
         "every reading has been added in")
    side(7.20, 5.15, "WRONG   —   total = 0 sits INSIDE the loop", ORANGE,
         bad_lines, 1, bad_rows, bad_total,
         f"total = {bad_total:.1f}      mean = {bad_total / n:.2f}",
         "only the LAST reading survived")

    arrow(ax, (5.52, 2.90), (7.08, 2.90), col=MUTED, lw=2.2, ms=20)
    ax.text(6.30, 3.18, "same data,\nsame six values", ha="center", va="center",
            fontsize=9.0, color=MUTED, style="italic", linespacing=1.5)
    ax.text(6.30, 2.56, "The bug does\nnot crash. It\njust quietly\nresets the box\non every pass.",
            ha="center", va="top", fontsize=9.0, color=ORANGE, fontweight="bold",
            linespacing=1.6)

    ax.text(0.25, 0.40, f"The mean is out by a factor of {ok_total / bad_total:.0f}, and Python "
                        "never says a word. This is the Week 3 silent wrong answer, in loop form.",
            fontsize=9.8, color=INK, va="center")
    return save_c(fig, "accumulator_bug.png")


# =============================================================== W4.4 files
def fig_file_pipeline():
    fig, ax = canvas(12.7, 4.95, y0=0.32)
    ax.text(0.25, 5.02, "Everything you read from a file arrives as TEXT",
            fontsize=13.5, fontweight="bold", color=INK, va="center")

    stages = [("1.  THE FILE", "on disk", ["UNIT_07,12.4", "UNIT_12,13.1"],
               'open("readings.csv")', INK, PAPER),
              ("2.  ONE LINE", "a single string", ["'UNIT_07,12.4\\n'"],
               "for line in f:", INK, CODE_BG),
              ("3.  SPLIT UP", "a list of strings", ["['UNIT_07', '12.4']"],
               'line.strip().split(",")', INK, CODE_BG),
              ("4.  CONVERTED", "now a number", ["12.4"],
               "float(parts[1])", TEAL, FADE_T),
              ("5.  ADDED UP", "arithmetic works", ["total  →  25.5"],
               "total = total + value", TEAL, FADE_T)]

    bw, gap = 2.22, 0.24
    for i, (title, sub, body, call, col, face) in enumerate(stages):
        x = 0.25 + i * (bw + gap)
        panel(ax, x, 2.05, bw, 2.36, face=face, edge=col, lw=1.8, r=0.10)
        ax.text(x + bw / 2, 4.18, title, ha="center", va="center", fontsize=10.2,
                fontweight="bold", color=col, zorder=3)
        ax.text(x + bw / 2, 3.94, sub, ha="center", va="center", fontsize=8.4,
                color=MUTED, style="italic", zorder=3)
        panel(ax, x + 0.12, 3.06, bw - 0.24, 0.66, face=PAPER if face != PAPER else STEEL,
              edge="none", lw=0, r=0.05, z=2)
        for k, ln in enumerate(body):
            code(ax, x + bw / 2, (3.51 - k * 0.24) if len(body) > 1 else 3.39, ln,
                 fs=8.6, color=col, z=3, ha="center")
        ax.text(x + bw / 2, 2.62, "in code:", ha="center", va="center", fontsize=7.6,
                color=MUTED, zorder=3)
        code(ax, x + bw / 2, 2.34, call, fs=8.4, color=INK, z=3, ha="center")
        if i < 4:
            arrow(ax, (x + bw + 0.03, 3.23), (x + bw + gap - 0.03, 3.23), col=MUTED,
                  lw=2.0, ms=16)

    # the crash lives in the gap between stage 3 and stage 4
    gx = 0.25 + 3 * bw + 2.5 * gap
    ax.plot([gx, gx], [2.05, 1.66], color=ORANGE, lw=1.6, ls=(0, (3, 3)), zorder=2)
    panel(ax, 2.60, 0.90, 9.00, 0.76, face=FADE, edge=ORANGE, lw=2.0, r=0.10)
    ax.text(2.82, 1.44, "THIS is where Week 4 crashes. Until float() is called, "
                        "\"12.4\" is text, not a number.",
            fontsize=10.2, fontweight="bold", color=ORANGE, va="center", zorder=3)
    code(ax, 2.82, 1.12, '0 + "12.4"  →  TypeError        but      "12.4" + "13.1"  →  "12.413.1"',
         fs=9.0, color=INK, z=3)

    ax.text(0.25, 0.50, "The first one stops you. The second one does not — it glues the text together "
                        "and carries on. Convert on the way in, every time.",
            fontsize=9.6, color=INK, va="center")
    return save_c(fig, "file_pipeline.png")


# --------------------------------------------------- Week 5/6 shared small frame
def machine_frame():
    """The five-row engineering table used across the Week 5 figures.

    Built with pandas so the dtypes and shape printed on the slides are read
    back from the real object, not typed in by hand.
    """
    import pandas as pd
    return pd.DataFrame({
        "machine_id": ["UNIT_07", "UNIT_07", "UNIT_12", "UNIT_21", "UNIT_12"],
        "speed_rpm": [1450, 1512, 1388, 1602, 1471],
        "torque_nm": [42.1, 38.6, 39.4, 44.8, 41.0],
        "tool_wear_min": [108, 111, 96, 132, 124],
        "failed": [False, False, False, True, False],
    })


def grade_frame():
    import pandas as pd
    return pd.DataFrame({
        "grade": ["L", "M", "H", "L", "M", "H", "L", "M", "H"],
        "torque_nm": [31.2, 40.5, 48.9, 33.8, 39.1, 51.4, 29.6, 42.0, 49.7],
    })


# =============================================================== W5.1 vectorised
# MEASURED, not asserted. The two code blocks drawn on this figure were timed
# against each other on a real 1,000,000-row CSV with timeit, best of 3:
#
#   stdlib answer : 42.122506427394775
#   pandas answer : 42.1225064273958        (agree to < 1e-9)
#   stdlib loop   : 0.724 s
#   pandas        : 0.117 s   -> about 6x
#   Python 3.10.12, numpy 2.2.6, pandas 2.3.3, aarch64 Linux
#
# The two answers are not bit-identical because the additions happen in a
# different order. Do not restate these numbers anywhere without re-measuring.
BENCH = dict(rows=1_000_000, loop_s=0.724, pandas_s=0.117, answer="42.122506427",
             py="3.10.12", pd="2.3.3", reps=3)


def fig_loops_vs_vectorised():
    fig, ax = canvas(12.6, 5.36, y0=0.36)
    ax.text(0.25, 5.55, "The same job, written twice", fontsize=13.5,
            fontweight="bold", color=INK, va="center")
    ax.text(0.25, 5.22, "Read a CSV of machine readings and find the mean torque of every "
                        "row above 35 N·m.", fontsize=11.0, color=INK, va="center")

    L0, L1 = 0.25, 6.10
    R0, R1 = 6.50, 12.35
    stdlib = ["import csv", "",
              "total = 0.0", "count = 0", "",
              'with open("machine.csv") as f:',
              "    for row in csv.DictReader(f):",
              '        torque = float(row["torque_nm"])',
              "        if torque > 35.0:",
              "            total = total + torque",
              "            count = count + 1", "",
              "mean = total / count"]
    vec = ["import pandas as pd", "",
           'df = pd.read_csv("machine.csv")', "",
           'mean = df.loc[df["torque_nm"] > 35.0, "torque_nm"].mean()']

    n_std = sum(1 for ln in stdlib if ln.strip())
    n_vec = sum(1 for ln in vec if ln.strip())
    for x0, x1, tag, sub, lines, col in ((L0, L1, "THE STANDARD LIBRARY", f"{n_std} lines of code", stdlib, MUTED),
                                         (R0, R1, "PANDAS", f"{n_vec} lines of code", vec, ORANGE)):
        ax.add_patch(FancyBboxPatch((x0, 4.50), x1 - x0, 0.50,
                                    boxstyle="round,pad=0,rounding_size=0.10",
                                    facecolor=col, edgecolor="none", zorder=2))
        ax.text(x0 + 0.24, 4.75, tag, fontsize=11.5, fontweight="bold", color=PAPER,
                va="center", zorder=3)
        ax.text(x1 - 0.24, 4.75, sub, fontsize=10.0, color=PAPER, va="center",
                ha="right", zorder=3)
        panel(ax, x0, 1.85, x1 - x0, 2.49, face=CODE_BG if col is MUTED else "#FDF3EF",
              edge=EDGE if col is MUTED else ORANGE, lw=1.4, r=0.08)
        for k, ln in enumerate(lines):
            code(ax, x0 + 0.26, 4.14 - k * 0.185, ln, fs=9.4)

    # unpack the one pandas line, in the space the short version leaves free
    ax.plot([R0 + 0.26, R1 - 0.26], [3.22, 3.22], color="#EBD3C8", lw=1.2, zorder=2)
    ax.text(R0 + 0.26, 3.02, "that one line, read from the inside out:", fontsize=8.8,
            color=MUTED, style="italic", va="center", zorder=3)
    for k, ln in enumerate(('df["torque_nm"] > 35.0    →  a True/False mask',
                            '.loc[mask, "torque_nm"]   →  only those rows',
                            '.mean()                   →  one number')):
        code(ax, R0 + 0.42, 2.72 - k * 0.28, ln, fs=8.8, color="#3A4C5C")

    panel(ax, L0, 1.15, R1 - L0, 0.53, face=FADE_T, edge=TEAL, lw=1.8, r=0.08)
    ax.text(L0 + 0.26, 1.415, f"Both give the same answer:  {BENCH['answer']} N·m", fontsize=11.0,
            fontweight="bold", color=TEAL, va="center", zorder=3)
    ax.text(R1 - 0.26, 1.415, "agreeing to nine decimal places", fontsize=9.4,
            color=TEAL, va="center", ha="right", style="italic", zorder=3)

    ax.text(0.25, 0.80, f"Measured, not guessed: the two blocks above, timed against each other on a real "
                        f"{BENCH['rows']:,}-row CSV with timeit",
            fontsize=9.6, color=INK, va="center")
    ax.text(0.25, 0.50, f"(best of {BENCH['reps']}) — the loop {BENCH['loop_s']:.2f} s, pandas "
                        f"{BENCH['pandas_s']:.2f} s, about "
                        f"{BENCH['loop_s'] / BENCH['pandas_s']:.0f}x. Python {BENCH['py']}, pandas "
                        f"{BENCH['pd']}, on one Linux machine. Yours will differ.",
            fontsize=9.6, color=MUTED, va="center", style="italic")
    return save_c(fig, "loops_vs_vectorised.png")


# =============================================================== W5.2 dataframe
def fig_dataframe_anatomy():
    df = machine_frame()
    fig, ax = canvas(12.6, 5.05, y0=0.40)
    ax.text(0.25, 5.30, "Anatomy of a DataFrame", fontsize=13.5, fontweight="bold",
            color=INK, va="center")

    TX, TOP = 2.30, 4.34
    colw = [1.10] + [1.38] * 5
    HL = 3                                     # the column shown as a Series
    heads = ["", "machine\n_id", "speed\n_rpm", "torque\n_nm", "tool_wear\n_min", "failed"]
    dtypes = [""] + [str(t) for t in df.dtypes]
    body = df.astype(object).values.tolist()

    def x(j):
        return TX + sum(colw[:j])

    # header
    for j, h in enumerate(heads):
        face = ORANGE if j == HL else (PAPER if j == 0 else INK)
        ax.add_patch(Rectangle((x(j), 3.90), colw[j], 0.44, facecolor=face,
                               edgecolor=PAPER, lw=1.6, zorder=2))
        if h:
            ax.text(x(j) + colw[j] / 2, 4.12, h, ha="center", va="center", color=PAPER,
                    fontsize=8.8, fontweight="bold", family=MONO, zorder=3,
                    linespacing=1.3)
    # dtype strip
    for j, d in enumerate(dtypes):
        face = "#F6DED6" if j == HL else ("#F5F8FB" if j else PAPER)
        ax.add_patch(Rectangle((x(j), 3.56), colw[j], 0.34, facecolor=face,
                               edgecolor="#CDD8E2", lw=1.0, zorder=2))
        if d:
            ax.text(x(j) + colw[j] / 2, 3.73, d, ha="center", va="center",
                    color=ORANGE if j == HL else MUTED, fontsize=8.4, family=MONO,
                    fontweight="bold", zorder=3)
    # body
    for i, row in enumerate(body):
        yy = 3.16 - i * 0.40
        ax.add_patch(Rectangle((x(0), yy), colw[0], 0.40, facecolor=STEEL,
                               edgecolor=PAPER, lw=1.6, zorder=2))
        ax.text(x(0) + colw[0] / 2, yy + 0.20, str(i), ha="center", va="center",
                color=INK, fontsize=10.0, fontweight="bold", family=MONO, zorder=3)
        for j, v in enumerate(row, start=1):
            hlt = (j == HL)
            ax.add_patch(Rectangle((x(j), yy), colw[j], 0.40,
                                   facecolor=FADE if hlt else (STEEL if i % 2 else PAPER),
                                   edgecolor="#CDD8E2", lw=1.0, zorder=2))
            ax.text(x(j) + colw[j] / 2, yy + 0.20, str(v), ha="center", va="center",
                    color=ORANGE if hlt else INK, fontsize=9.6, family=MONO,
                    fontweight="bold" if hlt else "normal", zorder=3)

    # shape, read off the real object
    panel(ax, 10.50, 4.62, 1.85, 0.40, face=FADE_T, edge=TEAL, lw=1.6, r=0.06)
    code(ax, 10.66, 4.82, f"df.shape → {df.shape}", fs=9.4, color=TEAL, z=3)

    ax.annotate("the COLUMN NAMES — you use these as strings, in quotes",
                xy=(x(2) + 0.4, 4.38), xytext=(2.30, 4.82), fontsize=9.4, color=INK,
                fontweight="bold", ha="left", va="center",
                arrowprops=dict(arrowstyle="->", color=INK, lw=1.6, shrinkA=4, shrinkB=2))
    ax.annotate("the INDEX\npandas' own row\nlabels. Here 0–4, but\nit could be dates or\nmachine IDs.",
                xy=(TX - 0.04, 2.60), xytext=(0.25, 2.60), fontsize=9.2, color=INK,
                fontweight="bold", ha="left", va="center", linespacing=1.5,
                arrowprops=dict(arrowstyle="->", color=INK, lw=1.6, shrinkA=4, shrinkB=2))
    ax.annotate("the DTYPE\nwhat pandas thinks\nis in the column.\nGet this wrong and\nnothing else works.",
                xy=(x(6) + 0.04, 3.73), xytext=(10.55, 3.66), fontsize=9.2, color=INK,
                fontweight="bold", ha="left", va="center", linespacing=1.5,
                arrowprops=dict(arrowstyle="->", color=INK, lw=1.6, shrinkA=4, shrinkB=2))
    ax.annotate('one column on its own is a SERIES  —  df["torque_nm"]',
                xy=(x(HL) + colw[HL] / 2, 1.50), xytext=(x(HL) + colw[HL] / 2, 1.02),
                fontsize=9.4, color=ORANGE, fontweight="bold", ha="center", va="center",
                arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.8, shrinkA=4, shrinkB=2))

    caption(ax, 0.25, 0.50, "A DataFrame is a table that knows its own row labels, column names and column "
                            "types. Everything else in pandas is built on those three.", fs=9.8,
            col=INK, italic=False)
    return save_c(fig, "dataframe_anatomy.png")


# =============================================================== W5.3 groupby
def fig_split_apply_combine():
    g = grade_frame()
    means = g.groupby("grade")["torque_nm"].mean()
    order = ["L", "M", "H"]
    names = {"L": "grade = L", "M": "grade = M", "H": "grade = H"}

    fig, ax = canvas(12.7, 5.43, y0=0.34)
    ax.text(0.25, 5.62, "Split, apply, combine — what groupby actually does",
            fontsize=13.5, fontweight="bold", color=INK, va="center")
    for cx, lab in ((1.68, "1.   SPLIT\nby the grade column"),
                    (5.85, "2.   APPLY\n.mean() to each group"),
                    (10.45, "3.   COMBINE\ninto one smaller table")):
        ax.text(cx, 5.05, lab, ha="center", va="center", fontsize=10.8,
                fontweight="bold", color=ORANGE, linespacing=1.6)

    GCOL = {"L": "#4A6B84", "M": "#5E8C7F", "H": INK}

    # ---- stage 1: the whole table
    _table(ax, 0.35, 4.50, [1.10, 1.55], 0.30, ["grade", "torque_nm"],
           [(r.grade, f"{r.torque_nm:.1f}") for r in g.itertuples()],
           cell_fs=9.4, head_fs=8.8, zebra=False,
           cell_col=lambda i, j, v: (PAPER, GCOL[g.grade[i]], True) if j == 0 else None)
    arrow(ax, (3.20, 3.00), (3.85, 3.00), col=MUTED, lw=2.2, ms=20)

    # ---- stage 2: one small table per group, each with its own mean
    top = 4.50
    for k in order:
        vals = g.loc[g.grade == k, "torque_nm"].tolist()
        ax.add_patch(FancyBboxPatch((4.15, top - 0.24), 2.50, 0.24,
                                    boxstyle="round,pad=0,rounding_size=0.04",
                                    facecolor=GCOL[k], edgecolor="none", zorder=2))
        ax.text(4.28, top - 0.12, names[k], fontsize=8.8, fontweight="bold",
                color=PAPER, va="center", family=MONO, zorder=3)
        for i, v in enumerate(vals):
            yy = top - 0.24 - (i + 1) * 0.24
            ax.add_patch(Rectangle((4.15, yy), 1.05, 0.24, facecolor=PAPER,
                                   edgecolor="#CDD8E2", lw=1.0, zorder=2))
            ax.add_patch(Rectangle((5.20, yy), 1.45, 0.24, facecolor=PAPER,
                                   edgecolor="#CDD8E2", lw=1.0, zorder=2))
            ax.text(4.675, yy + 0.12, k, ha="center", va="center", fontsize=9.0,
                    family=MONO, color=GCOL[k], fontweight="bold", zorder=3)
            ax.text(5.925, yy + 0.12, f"{v:.1f}", ha="center", va="center",
                    fontsize=9.0, family=MONO, color=INK, zorder=3)
        mid = top - 0.24 - 1.5 * 0.24
        arrow(ax, (6.75, mid), (7.20, mid), col=GCOL[k], lw=1.8, ms=15)
        ax.text(7.28, mid, f"{means[k]:.2f}", fontsize=10.5, family=MONO,
                fontweight="bold", color=GCOL[k], va="center", zorder=3)
        top -= 0.94 + 0.22
    arrow(ax, (8.15, 3.00), (8.75, 3.00), col=MUTED, lw=2.2, ms=20)

    # ---- stage 3: the combined result
    _table(ax, 8.90, 3.62, [1.50, 1.80], 0.34, ["grade", "mean torque_nm"],
           [(k, f"{means[k]:.2f}") for k in order], cell_fs=10.0, head_fs=8.8,
           zebra=False, head_bg=ORANGE,
           cell_col=lambda i, j, v: (FADE, ORANGE, True))

    panel(ax, 0.35, 0.62, 11.90, 0.50, face=CODE_BG, edge=EDGE, lw=1.4, r=0.08)
    code(ax, 0.55, 0.87, 'df.groupby("grade")["torque_nm"].mean()', fs=11.0, z=3)
    ax.text(4.60, 0.87, "one line, and it does all three stages", fontsize=9.4,
            color=MUTED, style="italic", va="center", zorder=3)
    caption(ax, 0.35, 0.28, "Nine rows in, three rows out. Every summary table you will ever build is this "
                            "shape.", fs=9.6, col=INK, italic=False)
    return save_c(fig, "split_apply_combine.png")


# =============================================================== W5.4 masks
def fig_boolean_mask():
    import pandas as pd
    s = pd.Series([42.1, 38.6, 39.4, 44.8, 41.0, 36.2, 45.9, 37.8], name="torque_nm")
    mask = s > 40.0
    kept = s[mask]

    fig, ax = canvas(12.4, 5.17, y0=0.34)
    ax.text(0.25, 5.36, "Filtering with a mask", fontsize=13.5, fontweight="bold",
            color=INK, va="center")
    panel(ax, 0.25, 4.34, 6.15, 0.68, face=CODE_BG, edge=EDGE, lw=1.4, r=0.08)
    code(ax, 0.45, 4.82, 'mask = df["torque_nm"] > 40.0', fs=10.5, z=3)
    code(ax, 0.45, 4.56, 'df.loc[mask, "torque_nm"]', fs=10.5, z=3)

    CW, RH, TOP = 1.70, 0.33, 3.88
    cols = [(1.30, 'df["torque_nm"]', INK), (3.95, "mask", TEAL), (6.60, "the result", ORANGE)]
    for cx, lab, col in cols:
        ax.text(cx + CW / 2, 4.06, lab, ha="center", va="center", fontsize=9.6,
                family=MONO, fontweight="bold", color=col)

    for i, v in enumerate(s):
        yy = TOP - (i + 1) * RH
        ax.text(1.22, yy + RH / 2, str(i), ha="right", va="center", fontsize=8.4,
                family=MONO, color=MUTED)
        ax.add_patch(Rectangle((1.30, yy), CW, RH, facecolor=STEEL if i % 2 else PAPER,
                               edgecolor="#CDD8E2", lw=1.0, zorder=2))
        ax.text(1.30 + CW / 2, yy + RH / 2, f"{v:.1f}", ha="center", va="center",
                fontsize=9.6, family=MONO, color=INK, zorder=3)
        keep = bool(mask.iloc[i])
        ax.add_patch(Rectangle((3.95, yy), CW, RH,
                               facecolor=FADE_T if keep else "#F2F4F6",
                               edgecolor="#CDD8E2", lw=1.0, zorder=2))
        ax.text(3.95 + CW / 2, yy + RH / 2, "True" if keep else "False", ha="center",
                va="center", fontsize=9.4, family=MONO,
                color=TEAL if keep else GREY, fontweight="bold" if keep else "normal",
                zorder=3)
        arrow(ax, (3.10, yy + RH / 2), (3.85, yy + RH / 2), col="#B9C8D8", lw=1.2, ms=10)

    for i, (idx, v) in enumerate(kept.items()):
        yy = TOP - (i + 1) * RH
        ax.text(6.52, yy + RH / 2, str(idx), ha="right", va="center", fontsize=8.4,
                family=MONO, color=ORANGE)
        ax.add_patch(Rectangle((6.60, yy), CW, RH, facecolor=FADE, edgecolor=ORANGE,
                               lw=1.2, zorder=2))
        ax.text(6.60 + CW / 2, yy + RH / 2, f"{v:.1f}", ha="center", va="center",
                fontsize=9.6, family=MONO, color=ORANGE, fontweight="bold", zorder=3)
    arrow(ax, (5.75, 3.30), (6.50, 3.30), col=ORANGE, lw=2.0, ms=16)

    notes = [(3.50, "The mask is exactly as long as the\ncolumn — one True or False per row."),
             (2.55, "Only the rows where the mask is True\nsurvive. Nothing is deleted from df."),
             (1.60, f"The result is SHORTER: {int(mask.sum())} of {len(s)} rows.\n"
                    "The original index comes with it.")]
    for y, txt in notes:
        ax.text(8.70, y, txt, ha="left", va="center", fontsize=9.6, color=INK,
                linespacing=1.55)

    caption(ax, 0.25, 0.60, "A mask is not a question, it is a column of answers. Build it once, then use "
                            "it to select, to count, or to overwrite.", fs=9.8, col=INK, italic=False)
    return save_c(fig, "boolean_mask.png")


# =============================================================== W6.1 defects
def fig_defect_types():
    fig, ax = canvas(12.7, 5.21, y0=0.36)
    ax.text(0.25, 5.42, "Six things wrong with one small table", fontsize=13.5,
            fontweight="bold", color=INK, va="center")
    ax.text(0.25, 5.10, "Eight hours of readings off one production line. Find all six before "
                        "you compute a single average.", fontsize=10.5, color=INK, va="center")

    heads = ["reading\n_id", "machine\n_id", "speed\n_rpm", "torque\n_nm",
             "tool_wear\n_min", "ambient\n_C"]
    rows = [["R001", "UNIT_07", "1450", "42.1", "108", "24.6"],
            ["R002", "UNIT_07", "1512", "NaN", "111", "25.1"],
            ["R003", "UNIT_12", "1388", "39.4", "96", "0.0"],
            ["R004", "UNIT_21", "1602", "44.8", "132", "24.9"],
            ["R004", "UNIT_21", "1602", "44.8", "132", "24.9"],
            ["R006", "UNIT_12", "1471", "41.0", "-37", "25.4"],
            ["R007", "UNIT_07", '"1450"', "43.2", "118", "24.2"],
            ["R008", "UNIT_21", "1536", "402.0", "124", "25.0"]]
    defects = {(1, 3): 1, (2, 5): 2, (4, 0): 3, (5, 4): 4, (6, 2): 5, (7, 3): 6}

    TX, CW, RH, TOP = 0.30, 1.275, 0.40, 4.60
    for j, h in enumerate(heads):
        ax.add_patch(Rectangle((TX + j * CW, TOP - 0.50), CW, 0.50, facecolor=INK,
                               edgecolor=PAPER, lw=1.6, zorder=2))
        ax.text(TX + j * CW + CW / 2, TOP - 0.25, h, ha="center", va="center",
                color=PAPER, fontsize=8.4, fontweight="bold", family=MONO, zorder=3,
                linespacing=1.3)
    for i, row in enumerate(rows):
        yy = TOP - 0.50 - (i + 1) * RH
        dupe = i in (3, 4)
        for j, v in enumerate(row):
            bad = (i, j) in defects
            face = FADE if bad else ("#FBF0EC" if dupe else (STEEL if i % 2 else PAPER))
            ax.add_patch(Rectangle((TX + j * CW, yy), CW, RH, facecolor=face,
                                   edgecolor="#CDD8E2", lw=1.0, zorder=2))
            ax.text(TX + j * CW + CW / 2, yy + RH / 2, v, ha="center", va="center",
                    color=ORANGE if bad else (GREY if v == "NaN" else INK),
                    fontsize=9.4, family=MONO,
                    fontweight="bold" if bad else "normal",
                    style="italic" if v == "NaN" else "normal", zorder=3)
            if bad:
                ax.add_patch(Rectangle((TX + j * CW, yy), CW, RH, facecolor="none",
                                       edgecolor=ORANGE, lw=2.0, zorder=4))
                badge(ax, TX + j * CW + CW - 0.16, yy + RH - 0.14, defects[(i, j)],
                      r=0.115, fs=8.4)
    # the duplicate is a pair of rows, not one cell: bracket them
    ytop = TOP - 0.50 - 3 * RH
    ax.plot([TX - 0.10, TX - 0.18, TX - 0.18, TX - 0.10],
            [ytop, ytop, ytop - 2 * RH, ytop - 2 * RH], color=ORANGE, lw=2.0, zorder=3)

    legend = [
        "MISSING VALUE — the cell is empty. pandas calls it\nNaN. Decide: drop the row or fill it, and say which.",
        "ZERO MEANING “NO READING” — 0.0 °C in Kampala is\nimpossible. The logger writes 0 when the probe is off.",
        "DUPLICATED ROW — the same reading logged twice. It\ndoubles that machine's weight in every average.",
        "IMPOSSIBLE VALUE — tool wear cannot be negative.\nA range check finds this. A mean will not.",
        "NUMBER STORED AS TEXT — “1450”, with quotes. The\nwhole column becomes dtype object and maths fails.",
        "OUTLIER — 402 N·m among readings of 38 to 45. Real,\nor a decimal point in the wrong place? Go and ask.",
    ]
    for i, txt in enumerate(legend):
        y = 4.30 - i * 0.62
        badge(ax, 8.42, y, i + 1, r=0.135, fs=9.0)
        ax.text(8.70, y, txt, ha="left", va="center", fontsize=9.0, color=INK,
                linespacing=1.55)

    caption(ax, 0.25, 0.58, "Every one of these is survivable if you find it. None of them is survivable if "
                            "you do not. Look at the table before you trust it.", fs=9.8, col=INK,
            italic=False)
    return save_c(fig, "defect_types.png")


# =============================================================== W6.2 missingness
def fig_missingness_map():
    n, fields = 40, ["reading\n_id", "machine\n_id", "speed\n_rpm", "torque\n_nm",
                     "vibration\n_mm_s", "ambient\n_C"]
    rng = np.random.default_rng(4)
    present = np.ones((n, len(fields)), dtype=bool)
    SENSOR_FITTED = 22
    present[:SENSOR_FITTED, 4] = False                 # sensor added part-way through
    present[rng.choice(n, 4, replace=False), 5] = False   # scattered, at random
    present[[9, 27], 3] = False

    fig, ax = canvas(12.7, 5.03, y0=0.42)
    ax.text(0.25, 5.30, "Where the holes are — and whether they are random",
            fontsize=13.5, fontweight="bold", color=INK, va="center")

    MX, CW, TOP = 1.95, 0.90, 4.30
    RH = 3.12 / n
    for j, f in enumerate(fields):
        ax.text(MX + j * CW + CW / 2, 4.44, f, ha="center", va="bottom", fontsize=7.6,
                color=INK, fontweight="bold", family=MONO, linespacing=1.3)
        for i in range(n):
            yy = TOP - (i + 1) * RH
            # no vertical gap between rows: a 10% gap on a 0.078 in cell reads as
            # horizontal stripes and hides the single-row gaps entirely.
            ax.add_patch(Rectangle((MX + j * CW + 0.03, yy), CW - 0.06, RH,
                                   facecolor="#4A6B84" if present[i, j] else "#F0F3F6",
                                   edgecolor="none", zorder=2))
    for i in range(0, n + 1, 5):
        ax.text(MX - 0.10, TOP - i * RH, str(i), ha="right", va="center", fontsize=7.0,
                color=MUTED, family=MONO)
    ax.text(1.42, (TOP + TOP - n * RH) / 2, "record, in the order it was logged",
            rotation=90, ha="center", va="center", fontsize=8.6, color=MUTED)

    for k, (lab, col) in enumerate((("present", "#4A6B84"), ("missing", "#F0F3F6"))):
        ax.add_patch(Rectangle((MX + k * 1.30, 4.82), 0.24, 0.16, facecolor=col,
                               edgecolor=EDGE, lw=1.0, zorder=2))
        ax.text(MX + k * 1.30 + 0.32, 4.90, lab, fontsize=8.6, color=MUTED,
                va="center", zorder=3)

    bx = MX + 4 * CW
    by = TOP - SENSOR_FITTED * RH
    ax.add_patch(Rectangle((bx, by), CW, TOP - by, facecolor="none", edgecolor=ORANGE,
                           lw=2.4, zorder=5))
    ax.annotate("Empty for the first 22 records, then full.\nThe vibration sensor was only fitted in March.",
                xy=(bx + CW + 0.02, by + (TOP - by) / 2), xytext=(7.90, 3.72),
                fontsize=9.4, color=ORANGE, fontweight="bold", ha="left", va="center",
                linespacing=1.55,
                arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.8, shrinkA=5, shrinkB=9))
    ax.text(7.90, 2.66, "This is MISSING NOT AT RANDOM. Whether a value is\nthere depends on WHEN the reading was taken.",
            fontsize=9.4, color=INK, fontweight="bold", ha="left", va="center",
            linespacing=1.55)
    ax.text(7.90, 1.72, "So drop every row with a missing value and you delete\nevery record from before March — the whole early "
                        "period\nyou were trying to compare against.",
            fontsize=9.4, color=MUTED, ha="left", va="center", linespacing=1.55)
    n_rand = int((~present[:, 3]).sum() + (~present[:, 5]).sum())
    ax.text(7.90, 1.00, f"The {n_rand} gaps in torque_nm and ambient_C really are scattered\n"
                        "at random. Those are a different problem, with a different fix.",
            fontsize=9.4, color=MUTED, ha="left", va="center", linespacing=1.55,
            style="italic")

    caption(ax, 0.25, 0.60, "Illustrative missingness, built to show one pattern. Always draw this map before "
                            "you decide what to do about missing data.", fs=9.6)
    return save_c(fig, "missingness_map.png")


# =============================================================== W6.3 boxplot
# Three data-entry errors are planted on purpose so the boxplot has something to
# flag. cohort_data("CML3112") on its own has no points beyond 1.5*IQR.
PLANTED = (88.6, 96.2, 102.4)


def fig_boxplot_annotated():
    y = cohort_data("CML3112")[1]
    d = np.concatenate([y, np.array(PLANTED)])
    q1, med, q3 = np.percentile(d, [25, 50, 75])
    iqr = q3 - q1
    f_lo, f_hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    inl = d[(d >= f_lo) & (d <= f_hi)]
    out = np.sort(d[(d < f_lo) | (d > f_hi)])
    w_lo, w_hi = inl.min(), inl.max()

    fig, axes = plt.subplots(1, 2, figsize=(12.4, 5.3),
                             gridspec_kw=dict(width_ratios=[1.5, 1], wspace=0.22))
    a, b = axes
    a.bxp([dict(med=med, q1=q1, q3=q3, whislo=w_lo, whishi=w_hi, fliers=out)],
          positions=[0], vert=False, widths=0.5, showfliers=True, patch_artist=True,
          boxprops=dict(facecolor=STEEL, edgecolor=INK, lw=1.8),
          medianprops=dict(color=ORANGE, lw=3.0),
          whiskerprops=dict(color=INK, lw=1.8), capprops=dict(color=INK, lw=1.8),
          flierprops=dict(marker="o", markerfacecolor=ORANGE, markeredgecolor=ORANGE,
                          markersize=8, alpha=0.9))
    a.set_xlim(0, 116)
    a.set_ylim(-1.68, 1.98)
    a.set_yticks([])
    a.spines["left"].set_visible(False)

    # stop the fence line short of its own label, rather than running through it
    a.plot([f_hi, f_hi], [-1.60, 1.44], color=MUTED, ls=(0, (5, 3)), lw=1.6, zorder=1)
    a.text(f_hi, 1.70, f"the upper fence\nQ3 + 1.5×IQR = {f_hi:.1f}", ha="center",
           va="center", fontsize=8.6, color=MUTED, linespacing=1.5)
    a.plot([q1, q1, q3, q3], [0.30, 0.50, 0.50, 0.30], color=TEAL, lw=1.8)
    a.text((q1 + q3) / 2, 0.66, f"IQR = {iqr:.1f} MPa   (the middle half)", ha="center",
           va="center", fontsize=9.4, color=TEAL, fontweight="bold")
    # The whisker caps are labelled in place: any leader line from this note to a
    # cap has to cross the IQR label sitting above the box.
    a.text(2.0, 1.32, f"the WHISKERS stop at the last real data point within\n"
                      f"1.5×IQR of the box — here {w_lo:.1f} and {w_hi:.1f} MPa. They are\n"
                      f"NOT drawn at 1.5×IQR itself.",
           fontsize=8.8, color=INK, ha="left", va="center", linespacing=1.55)
    for wx in (w_lo, w_hi):
        a.text(wx, 0.40, f"{wx:.1f}", ha="center", va="center", fontsize=8.6,
               color=INK, fontweight="bold")
    a.annotate(f"median\n{med:.1f}", xy=(med, -0.27), xytext=(med, -0.66),
               fontsize=9.4, color=ORANGE, fontweight="bold", ha="center", va="center",
               linespacing=1.4,
               arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.8, shrinkA=3, shrinkB=2))
    a.annotate(f"Q1\n{q1:.1f}", xy=(q1, -0.27), xytext=(q1 - 9.0, -1.32), fontsize=9.4,
               color=INK, ha="center", va="center", linespacing=1.4,
               arrowprops=dict(arrowstyle="->", color=INK, lw=1.5, shrinkA=3, shrinkB=2))
    a.annotate(f"Q3\n{q3:.1f}", xy=(q3, -0.27), xytext=(q3 + 9.0, -1.32), fontsize=9.4,
               color=INK, ha="center", va="center", linespacing=1.4,
               arrowprops=dict(arrowstyle="->", color=INK, lw=1.5, shrinkA=3, shrinkB=2))
    a.annotate(f"{len(out)} points\nbeyond the fence", xy=(out[1], -0.20),
               xytext=(out.mean(), -0.72), fontsize=9.4, color=ORANGE,
               fontweight="bold", ha="center", va="center", linespacing=1.4,
               arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.5, shrinkA=3, shrinkB=3))
    a.set_xlabel("28-day compressive strength (MPa)", fontsize=11)
    a.set_title("A BOXPLOT tells you WHERE", fontsize=12.5, fontweight="bold",
                color=INK, loc="left", pad=10)

    counts, edges, _ = b.hist(d, bins=14, color="#4A6B84", edgecolor=PAPER, lw=1.0)
    b.set_xlim(0, 116)
    b.set_ylim(0, counts.max() * 1.95)
    b.set_xlabel("28-day compressive strength (MPa)", fontsize=11)
    b.set_ylabel("number of mixes", fontsize=11)
    b.set_title("A HISTOGRAM tells you WHAT SHAPE", fontsize=12.5, fontweight="bold",
                color=ORANGE, loc="left", pad=10)
    b.grid(axis="y", color="#E3E9EF", lw=1)
    b.set_axisbelow(True)
    b.text(0.035, 0.965, f"The same {len(d)} values. The box said “middle half\n"
                         f"between {q1:.0f} and {q3:.0f}”. The histogram says the bulk is a\n"
                         "broad plateau from about 13 to 54 MPa, not one\n"
                         "peak — and that the three high values sit beyond\n"
                         "a wide empty gap. A box cannot show either.",
           transform=b.transAxes, fontsize=8.8, color=INK, va="top", ha="left",
           linespacing=1.6, zorder=6,
           bbox=dict(facecolor=PAPER, edgecolor=EDGE, boxstyle="round,pad=0.45"))

    for p in (a, b):
        p.set_xticks([0, 20, 40, 60, 80, 100])
    fig.text(0.008, 0.012,
             f"Illustrative data shaped like the UCI Concrete Compressive Strength dataset "
             f"(n = {len(y)}), plus three planted data-entry errors\n"
             f"({PLANTED[0]}, {PLANTED[1]}, {PLANTED[2]} MPa — the test load typed into the "
             f"strength column) so the boxplot has something to flag. The lower fence sits\n"
             f"at {f_lo:.1f} MPa, off the scale, so nothing here is flagged as unusually low. "
             f"Every number annotated above is computed from the data, none is typed in.",
             fontsize=8.4, color=MUTED, style="italic", va="bottom", linespacing=1.5)
    fig.subplots_adjust(left=0.045, right=0.988, top=0.90, bottom=0.20)
    return save(fig, "boxplot_annotated.png", pad=0.12)


# =============================================================== W6.4 chooser
def fig_chart_chooser():
    x3112, y3112, _, _, _ = cohort_data("CML3112", n=60, seed=13)
    g = grade_frame().groupby("grade")["torque_nm"].mean().reindex(["L", "M", "H"])
    rng = np.random.default_rng(31)
    hours = np.arange(0, 49)
    wear = np.cumsum(np.abs(rng.normal(2.1, 0.9, hours.size)))
    import pandas as pd
    corr = pd.DataFrame({
        "cement": x3112, "strength": y3112,
        "water": 220 - 0.11 * x3112 + rng.normal(0, 9, x3112.size),
        "age": rng.uniform(7, 90, x3112.size),
    }).corr().values

    fig, ax = canvas(12.6, 5.70, y0=0.22)
    ax.text(0.25, 5.72, "Start from the question, not from the chart",
            fontsize=13.5, fontweight="bold", color=INK, va="center")

    rows = [("How is one variable spread out?", "HISTOGRAM",
             "one column, cut into bins"),
            ("Do two variables move together?", "SCATTER PLOT",
             "one dot per row, two columns"),
            ("How does it change over time?", "LINE CHART",
             "only when the x axis is ordered"),
            ("Which group is bigger?", "BAR CHART",
             "one bar per category, from a groupby"),
            ("Which variables are related, all at once?", "CORRELATION HEATMAP",
             "every pair of columns, in one square")]
    ys = [5.00, 3.98, 2.96, 1.94, 0.92]

    for k, ((q, name, how), y) in enumerate(zip(rows, ys)):
        panel(ax, 0.25, y - 0.43, 5.35, 0.86, face=STEEL, edge=MUTED, lw=1.6, r=0.12)
        ax.text(0.50, y, q, ha="left", va="center", fontsize=11.2, color=INK, zorder=3)
        arrow(ax, (5.72, y), (5.98, y), col=MUTED, lw=1.8, ms=15)
        panel(ax, 7.80, y - 0.43, 4.55, 0.86, face=FADE, edge=ORANGE, lw=2.0, r=0.12)
        ax.text(8.02, y + 0.20, name, ha="left", va="center", fontsize=11.5,
                fontweight="bold", color=ORANGE, zorder=3)
        ax.text(8.02, y - 0.17, how, ha="left", va="center", fontsize=8.8,
                color="#3A4C5C", zorder=3)

        t = ax.inset_axes([6.10, y - 0.40, 1.52, 0.80], transform=ax.transData)
        t.set_xticks([]); t.set_yticks([])
        for s in t.spines.values():
            s.set_visible(True); s.set_color(EDGE); s.set_linewidth(1.0)
        t.set_facecolor("#FCFDFE")
        if k == 0:
            t.hist(y3112, bins=11, color="#4A6B84", edgecolor=PAPER, lw=0.5)
        elif k == 1:
            t.scatter(x3112, y3112, s=5, color="#4A6B84", alpha=0.8)
        elif k == 2:
            t.plot(hours, wear, color="#4A6B84", lw=1.6)
        elif k == 3:
            # no tick labels: at thumbnail size they would fall below the 8pt floor
            t.bar([0, 1, 2], g.values, color=["#8FA6BC", "#4A6B84", INK], width=0.62)
            t.set_ylim(0, g.max() * 1.18)
        else:
            t.imshow(corr, cmap="BrBG", vmin=-1, vmax=1, aspect="auto")

    caption(ax, 0.25, 0.28, "Every one of these thumbnails is a real plot of real numbers, drawn by the same "
                            "code you will write. None of them is a drawing of a chart.", fs=9.6)
    return save_c(fig, "chart_chooser.png")



# =============================================================== per-week clocks
WEEK_SEGS = {
 1: [("Welcome and how\nthis course works", 15, "#B9C8D8"), ("The whole field,\nstart to finish", 15, "#4A6B84"),
     ("What this course\nis about", 15, "#8FA6BC"), ("Two ways to make\na computer decide", 25, "#4A6B84"),
     ("HANDS-ON: predict\ncase 13 on paper", 25, ORANGE), ("Break", 10, "#DCE4EC"),
     ("Two kinds\nof question", 15, TEAL), ("What ML\ncannot do", 15, "#5E8C7F"),
     ("CHALLENGE:\nProblem Hunt", 25, ORANGE), ("Gallery walk\n+ assignment", 10, "#8FA6BC"),
     ("Revision\nmaterial", 5, INK), ("QUIZ\n5 questions", 5, "#5E8C7F")],
 2: [("Where we\ngot to", 10, "#B9C8D8"), ("Four questions,\nfour tools", 20, "#8FA6BC"),
     ("HANDS-ON: your\nfirst notebook", 30, ORANGE), ("What a notebook\nactually is", 20, "#4A6B84"),
     ("The execution\ntrap", 20, TEAL), ("Break", 10, "#DCE4EC"),
     ("Why versions,\nnot backups", 25, "#4A6B84"), ("HANDS-ON: repo,\ncommit, push", 25, ORANGE),
     ("CHALLENGE:\nBreak and Fix", 10, ORANGE), ("Assignment\n+ close", 5, INK), ("QUIZ\n5 questions", 5, "#5E8C7F")],
 3: [("Where we\ngot to", 10, "#B9C8D8"), ("Why code a formula\nyou already know?", 15, "#8FA6BC"),
     ("Variables\nand types", 25, "#4A6B84"), ("HANDS-ON: formula\nto function", 25, ORANGE),
     ("Break", 10, "#DCE4EC"), ("Encoding a\ndecision rule", 15, TEAL),
     ("Reading\nan error", 15, "#5E8C7F"), ("PRACTICAL: function\nlibrary", 35, ORANGE),
     ("CHALLENGE: Wrong\nAnswer Hunt", 20, ORANGE), ("Assignment\n+ close", 5, INK), ("QUIZ\n5 questions", 5, "#5E8C7F")],
 4: [("Where we\ngot to", 10, "#B9C8D8"), ("The question you\ncannot do by hand", 10, "#8FA6BC"),
     ("Lists and\ndictionaries", 20, "#4A6B84"), ("The\naccumulator", 25, TEAL),
     ("HANDS-ON: reading\na real file", 25, ORANGE), ("Break", 10, "#DCE4EC"),
     ("When a row\nis broken", 10, "#5E8C7F"), ("PRACTICAL: reading\nreport", 30, ORANGE),
     ("INVESTIGATION\nLAB 1", 30, ORANGE), ("Assignment\n+ close", 5, INK), ("QUIZ\n5 questions", 5, "#5E8C7F")],
 5: [("Where we\ngot to", 10, "#B9C8D8"), ("Sixty lines\nbecomes three", 20, "#8FA6BC"),
     ("NumPy: many\nnumbers at once", 20, "#4A6B84"), ("The\nDataFrame", 25, TEAL),
     ("Break", 10, "#DCE4EC"), ("Select, filter,\ngroup", 30, ORANGE),
     ("Judging a\ndataset", 20, "#5E8C7F"), ("PRACTICAL: Twelve\nQuestions", 25, ORANGE),
     ("CHALLENGE: Ten\nQuestions", 10, ORANGE), ("Project brief\n+ close", 5, INK), ("QUIZ\n5 questions", 5, "#5E8C7F")],
 7: [("Setup, seating,\nrules read out", 15, "#B9C8D8"), ("PART A — the practical\non an unseen dataset", 120, ORANGE),
     ("PART B — typed\nreasoning, no code", 25, "#4A6B84"), ("Collect and\ncheck", 20, INK)],
 8: [("Where we\ngot to", 10, "#B9C8D8"), ("Today's\nquestion", 10, "#8FA6BC"),
     ("From a line by eye\nto least squares", 25, "#4A6B84"), ("Train and\ntest", 25, TEAL),
     ("Break", 10, "#DCE4EC"), ("HANDS-ON: your\nfirst model", 30, ORANGE),
     ("Reading the error\nin real units", 25, "#5E8C7F"), ("Residuals: where\nis it worst?", 20, "#8FA6BC"),
     ("CHALLENGE: beat\nthe baseline", 15, ORANGE), ("Project brief\n+ close", 5, INK), ("QUIZ\n5 questions", 5, "#5E8C7F")],
 9: [("Where we\ngot to", 10, "#B9C8D8"), ("The two\nmistakes", 15, "#8FA6BC"),
     ("A boundary, and\nwhere to put it", 25, "#4A6B84"), ("Trees and\nforests", 25, TEAL),
     ("Break", 10, "#DCE4EC"), ("HANDS-ON: three\nclassifiers", 30, ORANGE),
     ("The confusion\nmatrix", 20, "#5E8C7F"), ("Precision, recall\nand the threshold", 15, "#8FA6BC"),
     ("CHALLENGE: the\n97% trap", 20, ORANGE), ("Project launch\n+ close", 5, INK), ("QUIZ\n5 questions", 5, "#5E8C7F")],
 10: [("Where we\ngot to", 10, "#B9C8D8"), ("Three error\nstories", 15, "#8FA6BC"),
      ("Overfitting, and\nthe curve", 25, "#4A6B84"), ("Cross-\nvalidation", 25, TEAL),
      ("Break", 10, "#DCE4EC"), ("HANDS-ON: the\nTrust Lab", 30, ORANGE),
      ("Data leakage:\nfour kinds", 25, "#5E8C7F"),
      ("CHALLENGE: too\ngood to be true", 25, ORANGE), ("Milestone 1\nreview", 10, INK), ("QUIZ\n5 questions", 5, "#5E8C7F")],
 11: [("Where we\ngot to", 10, "#B9C8D8"), ("A feature is\nknowledge encoded", 15, "#8FA6BC"),
      ("Encoding and\nscaling", 25, "#4A6B84"), ("Building a domain\nfeature", 25, TEAL),
      ("Break", 10, "#DCE4EC"), ("HANDS-ON: the\nFeature Workshop", 30, ORANGE),
      ("Measuring what\nhelped: ablation", 25, "#5E8C7F"),
      ("CHALLENGE: Domain\nAdvantage", 25, ORANGE), ("Milestone 2\nbriefing", 10, INK), ("QUIZ\n5 questions", 5, "#5E8C7F")],
 # Every teaching session closes with a five-minute weekly quiz. Twelve of
 # them cost 60 minutes across the semester, which is what the four
 # fifteen-minute block checkpoints used to cost in-room.
 12: [("Where we\ngot to", 10, "#B9C8D8"), ("A fair comparison\nprotocol", 20, "#8FA6BC"),
      ("Tuning inside\ncross-validation", 15, "#4A6B84"), ("Break", 10, "#DCE4EC"),
      ("ENGINEERING AI CHALLENGE — choose a model and defend it", 100, ORANGE),
      ("Defence\nround", 15, TEAL),
      ("Milestone 3\nbriefing", 5, INK), ("QUIZ\n5 questions", 5, "#5E8C7F")],
 13: [("Where we\ngot to", 10, "#B9C8D8"), ("Reproducibility as\nan obligation", 20, "#8FA6BC"),
      ("From messy notebook\nto clean repository", 20, "#4A6B84"), ("Break", 10, "#DCE4EC"),
      ("STUDIO — build, with clinic slots", 95, ORANGE),
      ("Peer review\nround", 15, TEAL),
      ("Test 2\nbriefing", 5, INK), ("QUIZ\n5 questions", 5, "#5E8C7F")],
 14: [("Setup, seating,\nrules read out", 15, "#B9C8D8"),
      ("PART A — end-to-end ML on an unseen dataset", 120, ORANGE),
      ("PART B — typed\nreasoning, no code", 25, "#4A6B84"), ("Collect and\ncheck", 20, INK)],
 # The viva is sampled while the fair is running, so it is inside the fair
 # block rather than beside it. Counting it separately made the day 210
 # minutes long while every slide said the viva happens during the fair.
 15: [("Running order\nand rules", 10, "#B9C8D8"),
      ("DEMO FAIR — two rounds, with formative feedback", 130, ORANGE),
      ("Shortlisted\ndemos", 20, "#4A6B84"),
      ("Recognition, feedback\nand reflection", 20, INK)],
 6: [("Where we got to\n(+ W5 catch-up)", 15, "#B9C8D8"), ("Real data\nis broken", 15, "#8FA6BC"),
     ("Six ways data\ngoes wrong", 25, "#4A6B84"), ("Charts as\ninstruments", 25, TEAL),
     ("Break", 10, "#DCE4EC"), ("PRACTICAL: the\nData Clinic", 40, ORANGE),
     ("Error, or\nreality?", 15, "#5E8C7F"), ("CHALLENGE: Outlier\nArgument", 20, ORANGE),
     ("Test 1\nbrief", 10, INK), ("QUIZ\n5 questions", 5, "#5E8C7F")],
}


def fig_clock_week(wk):
    segs = WEEK_SEGS[wk]
    total = sum(m for _, m, _ in segs)
    assert total == 180, f"week {wk} sums to {total}, not 180"
    fig, ax = plt.subplots(figsize=(11.8, 4.4))
    ax.set_xlim(0, 180); ax.set_ylim(0, 2.6); ax.axis("off")
    x = 0
    for i, (lab, mins, col) in enumerate(segs):
        ax.add_patch(Rectangle((x + 0.6, 1.15), mins - 1.2, 0.8, facecolor=col, edgecolor="none"))
        ax.text(x + mins / 2, 1.55, f"{mins}", ha="center", va="center", fontsize=9.5,
                fontweight="bold", color=PAPER if col != "#DCE4EC" else INK)
        ax.text(x + mins / 2, 1.02 if i % 2 == 0 else 0.62, lab, ha="center", va="top",
                fontsize=7.6, color=INK, linespacing=1.3)
        x += mins
    ax.text(0, 2.28, f"Three hours, {len(segs)} segments \u2014 scheduled teaching and practice",
            fontsize=12.5, fontweight="bold", color=INK)
    ax.text(0, 2.02, ("Numbers are minutes. Practical work and reasoning are timed separately." if wk in (7, 14) else "Numbers are minutes. Nothing here is a lecture longer than 35 minutes."),
            fontsize=10, color=MUTED, style="italic")
    return save(fig, f"clock_w{wk}.png")

# ===============================================================================
# WEEKS 8-13:  THE MACHINE-LEARNING CORE
# ===============================================================================
# scikit-learn is NOT installed in this environment. Checked:
#     $ python3 -c "import sklearn"  ->  ModuleNotFoundError: No module named 'sklearn'
# So every fit, split, score, threshold and tree split below is computed with
# numpy alone:
#     least squares      np.polyfit / np.polynomial.Polynomial.fit / normal equations
#     ridge              normal equations with a lambda*I penalty (intercept exempt)
#     logistic           batch gradient descent on standardised features
#     decision trees     exhaustive threshold search minimising Gini (or SSE)
#     bagging, boosting  loops over the above
# Nothing annotated on any of these figures is typed in by hand: every number is
# recomputed at draw time from the data drawn in the same figure.

# ------------------------------------------------------------------ regression
def reg_metrics(y, yhat):
    """(MAE, RMSE, R2). R2 is 1 - SS_res/SS_tot against the mean of `y`."""
    y = np.asarray(y, float)
    yhat = np.asarray(yhat, float)
    e = yhat - y
    ss_res = float((e ** 2).sum())
    ss_tot = float(((y - y.mean()) ** 2).sum())
    return (float(np.abs(e).mean()), float(np.sqrt((e ** 2).mean())),
            1.0 - ss_res / ss_tot)


def holdout(n, test_frac=0.2, seed=42):
    """Shuffled index split. Returns (train_idx, test_idx)."""
    idx = np.random.default_rng(seed).permutation(n)
    ntest = int(round(n * test_frac))
    return idx[ntest:], idx[:ntest]


def ols(X, y, lam=0.0):
    """Normal equations with an intercept column. lam > 0 gives ridge."""
    X = np.atleast_2d(np.asarray(X, float))
    A = np.column_stack([np.ones(len(X)), X])
    P = lam * np.eye(A.shape[1])
    P[0, 0] = 0.0
    return np.linalg.solve(A.T @ A + P, A.T @ np.asarray(y, float))


def ols_pred(w, X):
    X = np.atleast_2d(np.asarray(X, float))
    return np.column_stack([np.ones(len(X)), X]) @ w


def polyfit(x, y, deg):
    """Least-squares polynomial. Uses the numpy Polynomial class because it maps
    x into [-1, 1] internally, so degree 14 does not fall over on a badly
    conditioned Vandermonde matrix the way np.polyfit does."""
    return np.polynomial.Polynomial.fit(np.asarray(x, float),
                                        np.asarray(y, float), deg)


# --------------------------------------------------------------- classification
def logistic_fit(X, y, iters=8000, lr=0.5):
    """Batch gradient descent on the log-loss, features standardised for
    conditioning. Returns (w, b, proba) with w and b in ORIGINAL feature units
    so a boundary can be drawn straight onto the raw axes."""
    X = np.atleast_2d(np.asarray(X, float))
    y = np.asarray(y, float)
    mu, sd = X.mean(0), X.std(0)
    sd = np.where(sd == 0, 1.0, sd)
    Z = (X - mu) / sd
    w = np.zeros(Z.shape[1])
    b = 0.0
    for _ in range(iters):
        p = 1.0 / (1.0 + np.exp(-(Z @ w + b)))
        g = p - y
        w -= lr * (Z.T @ g) / len(y)
        b -= lr * g.mean()
    w_o = w / sd
    b_o = float(b - np.sum(w * mu / sd))

    def proba(Xn):
        Xn = np.atleast_2d(np.asarray(Xn, float))
        return 1.0 / (1.0 + np.exp(-(Xn @ w_o + b_o)))

    return w_o, b_o, proba


def conf_counts(y_true, y_pred):
    """(TN, FP, FN, TP) with 1 = the positive, actionable class."""
    y_true = np.asarray(y_true).astype(int)
    y_pred = np.asarray(y_pred).astype(int)
    return (int(((y_pred == 0) & (y_true == 0)).sum()),
            int(((y_pred == 1) & (y_true == 0)).sum()),
            int(((y_pred == 0) & (y_true == 1)).sum()),
            int(((y_pred == 1) & (y_true == 1)).sum()))


def clf_metrics(tn, fp, fn, tp):
    """(accuracy, precision, recall, F1). NaN where the denominator is zero —
    which is the honest answer, and the whole point of fig_imbalance_trap."""
    tot = tn + fp + fn + tp
    acc = (tp + tn) / tot if tot else float("nan")
    prec = tp / (tp + fp) if (tp + fp) else float("nan")
    rec = tp / (tp + fn) if (tp + fn) else float("nan")
    f1 = (2 * prec * rec / (prec + rec)
          if (tp + fp) and (tp + fn) and (prec + rec) > 0 else float("nan"))
    return acc, prec, rec, f1


# ----------------------------------------------------------------------- trees
def _gini(y):
    if len(y) == 0:
        return 0.0
    p = float(np.mean(y))
    return 2.0 * p * (1.0 - p)


def _thresholds(col, cap=60):
    """Midpoints between consecutive distinct values, thinned to at most `cap`
    candidates so an exhaustive search stays quick."""
    v = np.unique(col)
    if len(v) < 2:
        return np.empty(0)
    mid = (v[:-1] + v[1:]) / 2.0
    if len(mid) > cap:
        mid = mid[np.linspace(0, len(mid) - 1, cap).astype(int)]
    return mid


def _best_split(X, y, min_leaf, feats, kind):
    """Exhaustive search. kind='gini' for classification, 'sse' for regression.
    Returns (score, feature, threshold) for the lowest score, or None."""
    best = None
    for j in feats:
        for t in _thresholds(X[:, j]):
            L = X[:, j] <= t
            nL, nR = int(L.sum()), int((~L).sum())
            if nL < min_leaf or nR < min_leaf:
                continue
            if kind == "gini":
                s = (nL * _gini(y[L]) + nR * _gini(y[~L])) / len(y)
            else:
                s = float(((y[L] - y[L].mean()) ** 2).sum()
                          + ((y[~L] - y[~L].mean()) ** 2).sum())
            if best is None or s < best[0] - 1e-12:
                best = (s, j, float(t))
    return best


def grow_tree(X, y, depth, min_leaf=1, kind="gini", feats=None, rng=None,
              max_feats=None):
    """One tree, as nested dicts. Leaves carry the counts the figures print."""
    X = np.atleast_2d(np.asarray(X, float))
    y = np.asarray(y, float)
    node = {"n": len(y), "pos": int(np.sum(y == 1)) if kind == "gini" else 0,
            "value": float(np.mean(y)) if len(y) else 0.0}
    node["cls"] = int(node["value"] >= 0.5)
    if depth <= 0 or len(y) < 2 * min_leaf or np.all(y == y[0]):
        return node
    if feats is None:
        feats = list(range(X.shape[1]))
    use = feats
    if max_feats is not None and max_feats < len(feats) and rng is not None:
        use = list(rng.choice(feats, size=max_feats, replace=False))
    b = _best_split(X, y, min_leaf, use, kind)
    if b is None:
        return node
    parent = _gini(y) if kind == "gini" else float(((y - y.mean()) ** 2).sum())
    if b[0] >= parent - 1e-9:
        return node
    _, j, t = b
    L = X[:, j] <= t
    node.update(feat=j, thr=t,
                left=grow_tree(X[L], y[L], depth - 1, min_leaf, kind, feats,
                               rng, max_feats),
                right=grow_tree(X[~L], y[~L], depth - 1, min_leaf, kind, feats,
                                rng, max_feats))
    return node


def tree_predict(node, X, key="cls"):
    X = np.atleast_2d(np.asarray(X, float))
    out = np.empty(len(X))
    for i, row in enumerate(X):
        nd = node
        while "feat" in nd:
            nd = nd["left"] if row[nd["feat"]] <= nd["thr"] else nd["right"]
        out[i] = nd[key]
    return out


def grow_forest(X, y, n_trees, depth, min_leaf=2, kind="gini", seed=0,
                max_feats=None):
    """Bootstrap aggregation. This is what makes it a forest and not a tree."""
    X = np.atleast_2d(np.asarray(X, float))
    y = np.asarray(y, float)
    rng = np.random.default_rng(seed)
    trees = []
    for _ in range(n_trees):
        b = rng.integers(0, len(y), len(y))
        trees.append(grow_tree(X[b], y[b], depth, min_leaf, kind, rng=rng,
                               max_feats=max_feats))
    return trees


def forest_predict(trees, X, kind="gini"):
    key = "cls" if kind == "gini" else "value"
    P = np.array([tree_predict(t, X, key) for t in trees])
    return (P.mean(0) >= 0.5).astype(float) if kind == "gini" else P.mean(0)


def boost_fit(X, y, n_rounds=120, lr=0.1, depth=1, min_leaf=4):
    """Gradient boosting on squared loss: fit each stump to what is left over."""
    X = np.atleast_2d(np.asarray(X, float))
    y = np.asarray(y, float)
    f0 = float(y.mean())
    resid = y - f0
    stumps = []
    for _ in range(n_rounds):
        t = grow_tree(X, resid, depth, min_leaf, kind="sse")
        step = tree_predict(t, X, "value")
        resid = resid - lr * step
        stumps.append(t)
    return f0, lr, stumps


def boost_predict(model, X):
    f0, lr, stumps = model
    out = np.full(len(np.atleast_2d(X)), f0)
    for t in stumps:
        out = out + lr * tree_predict(t, X, "value")
    return out


def knn1_predict(Xtr, ytr, Xte):
    """1-nearest neighbour. Deliberately memory-like, which is what makes it the
    clearest demonstration of a leaking split."""
    Xtr = np.atleast_2d(np.asarray(Xtr, float))
    Xte = np.atleast_2d(np.asarray(Xte, float))
    ytr = np.asarray(ytr, float)
    d = ((Xte[:, None, :] - Xtr[None, :, :]) ** 2).sum(-1)
    return ytr[d.argmin(1)]


# ------------------------------------------------------- illustrative datasets
def curved_strength(n=64, seed=17):
    """Strength against curing age. Genuinely curved (strength gain is roughly
    logarithmic in age), so a straight line is visibly the wrong model."""
    rng = np.random.default_rng(seed)
    age = rng.uniform(3.0, 120.0, n)
    y = 8.0 + 13.5 * np.log(age) + rng.normal(0, 3.6, n)
    return age, y


def concrete_table(n=300, seed=23):
    """Four real mix variables plus one that is only a label. Strength follows
    an Abrams-like fall with water/cement, a logarithmic gain with age, and a
    mild interaction (a lean mix gains less from curing) — so the relationship
    is genuinely non-linear and a tree or an ensemble has something to find."""
    rng = np.random.default_rng(seed)
    cement = rng.uniform(160, 500, n)
    water = rng.uniform(140, 235, n)
    age = rng.uniform(3, 120, n)
    batch = rng.integers(1000, 9999, n).astype(float)   # a label, not a feature
    wc = water / cement
    y = (34.0 - 52.0 * wc + 9.5 * np.log(age)
         + 7.0 * np.log(age) * (0.52 - wc) + rng.normal(0, 3.0, n))
    X = np.column_stack([cement, water, age, wc, batch])
    names = ["cement (kg/m³)", "water (kg/m³)", "age (days)",
             "water/cement ratio", "batch number"]
    return X, np.clip(y, 4, 90), names


def machine_sensors(n=900, seed=29, base=-6.2):
    """Two sensor channels and a failure flag. Failure risk rises with the
    PRODUCT of torque and tool wear, which is how overstrain failure is defined
    in the AI4I 2020 dataset (wear x torque above a limit in min·N·m). Lower
    `base` for a rarer failure. Returns (X[:, torque, wear], y)."""
    rng = np.random.default_rng(seed)
    torque = rng.uniform(18, 74, n)
    wear = rng.uniform(5, 250, n)
    p = 1.0 / (1.0 + np.exp(-(base + 0.00088 * torque * wear)))
    return np.column_stack([torque, wear]), (rng.random(n) < p).astype(int)


SENSOR_NAMES = ["Shaft torque (N·m)", "Tool wear (min)"]


def flotation_table(n=400, seed=41):
    """Three control variables and the silica that comes out. Silica falls with
    the depressant dose per tonne of feed and with a higher pulp pH."""
    rng = np.random.default_rng(seed)
    feed = rng.uniform(300, 700, n)        # t/h of ore into the circuit
    reagent = rng.uniform(200, 900, n)     # g/min of depressant
    ph = rng.uniform(9.0, 10.6, n)
    silica = (3.4 - 0.0215 * (reagent * 60.0 / feed) - 0.35 * (ph - 9.8)
              + rng.normal(0, 0.30, n))
    X = np.column_stack([feed, reagent, ph])
    names = ["Ore feed rate (t/h)", "Reagent flow (g/min)", "Pulp pH"]
    return X, np.clip(silica, 0.35, 6.5), names


def domain_pair(code, n=110, seed=31):
    """(raw feature, engineered feature, target, labels). Built so the engineered
    domain feature genuinely is the stronger predictor: the target is driven by
    the ratio (or the product), and the raw column only inherits part of it
    because the other quantity in the ratio also varies."""
    rng = np.random.default_rng(seed)
    if code == "CML3112":
        cement = rng.uniform(260, 420, n)
        water = rng.uniform(145, 240, n)
        wc = water / cement
        y = 100.0 - 98.0 * wc + rng.normal(0, 3.4, n)
        return (cement, wc, np.clip(y, 5, 90),
                "Cement content (kg/m³)", "Water/cement ratio (–)",
                "28-day compressive strength (MPa)",
                "the same mixes, one engineered column")
    if code == "CML3113":
        feed = rng.uniform(300, 700, n)          # t/h of ore
        reagent = rng.uniform(200, 900, n)       # g/min of depressant
        dose = reagent * 60.0 / feed             # g per tonne of feed
        y = 5.05 - 0.0215 * dose + rng.normal(0, 0.26, n)
        return (reagent, dose, np.clip(y, 0.35, 6.0),
                "Reagent flow (g/min)", "Reagent dose (g per tonne of feed)",
                "Silica in concentrate (%)",
                "the same batches, one engineered column")
    torque = rng.uniform(20, 70, n)
    speed = rng.uniform(1200, 2900, n)           # rpm
    power = torque * speed * 2.0 * np.pi / 60.0  # watts
    y = 4.0 + 0.00205 * power + rng.normal(0, 2.3, n)
    return (torque, power / 1000.0, np.clip(y, 0.5, 60),
            "Shaft torque (N·m)", "Mechanical power  T × ω  (kW)",
            "Motor winding temperature rise (°C)",
            "the same machine-hours, one engineered column")


def replicate_batches(n_batch=44, reps=3, seed=37):
    """One physical batch, measured `reps` times. The replicates are nearly
    identical, so if they land on both sides of a random row split the model can
    look up the answer instead of predicting it. Returns (X, y, group)."""
    rng = np.random.default_rng(seed)
    cement = rng.uniform(180, 480, n_batch)
    water = rng.uniform(145, 235, n_batch)
    truth = 92.0 - 98.0 * (water / cement) + rng.normal(0, 5.5, n_batch)
    X, y, g = [], [], []
    for b in range(n_batch):
        for _ in range(reps):
            X.append([cement[b] + rng.normal(0, 0.8),
                      water[b] + rng.normal(0, 0.4)])
            y.append(truth[b] + rng.normal(0, 0.35))
            g.append(b)
    return np.array(X), np.array(y), np.array(g)


# Say which discipline the worked example comes from. These figures are
# shown to all three cohorts, and a caption that leaves the discipline
# unstated invites students to read concrete numbers as their own.
ILLUS = ("Worked example from civil engineering: illustrative data shaped like the "
         "UCI Concrete Compressive Strength dataset. The mechanism it shows is the "
         "same in every discipline; the numbers are not yours.")


def wrapped(s, width=185):
    """Hard-wrap a one-line caption. A single long caption is the most common way
    text runs off the right edge of a landscape figure."""
    import textwrap
    return "\n".join(textwrap.wrap(s, width))


def _grid(ax, axis="y"):
    ax.grid(axis=axis, color="#E3E9EF", lw=1)
    ax.set_axisbelow(True)


def _keyline(ax, x, y, col, txt, fs=9.8, sw=0.16, **kw):
    """A colour swatch and a sentence, drawn in a text block well away from the
    diagram so the swatch cannot be read as a datum. Coordinates are data units."""
    ax.add_patch(Rectangle((x, y - sw / 2), sw, sw, facecolor=col, edgecolor="none",
                           zorder=3))
    return ax.text(x + sw + 0.16, y, txt, ha="left", va="center", fontsize=fs,
                   color=INK, zorder=3, **kw)


# =============================================================== W8.1 fit by eye
def fig_fit_by_eye():
    """The bridge from Week 1's hand prediction to a fitted model: several lines
    are defensible, exactly one minimises the sum of squared residuals."""
    x, y, xl, yl, unit = cohort_data("CML3112", n=26, seed=21)
    o = np.argsort(x)
    lo, hi = o[:9], o[-9:]
    ends = [int(x.argmin()), int(x.argmax())]

    def ssr(c):
        return float(((np.polyval(c, x) - y) ** 2).sum())

    eyed = [("A", np.polyfit(x[lo], y[lo], 1), "#4A6B84"),
            ("B", np.polyfit(x[hi], y[hi], 1), "#8FA6BC"),
            ("C", np.polyfit(x[ends], y[ends], 1), MUTED)]
    c_ls = np.polyfit(x, y, 1)
    xs = np.linspace(x.min(), x.max(), 120)
    xr, yr = x.max() - x.min(), y.max() - y.min()

    # Where to draw the "they disagree by this much" bracket. House rule: an
    # annotation may not sit on a data marker, so instead of guessing an x, take
    # the round cement value in the middle of the range whose bracket is
    # FURTHEST from every plotted point, measured in normalised axis units.
    def _at(v):
        return [float(np.polyval(c, v)) for _, c, _ in eyed]

    def _clear(v):
        vals = _at(v)
        near_y = np.clip(y, min(vals), max(vals))     # closest point on the bracket
        return float(np.min(np.hypot((x - v) / xr, (y - near_y) / yr)))

    cands = np.arange(np.ceil((x.min() + 0.18 * xr) / 25.0) * 25.0,
                      x.max() - 0.18 * xr, 25.0)
    xq = float(cands[int(np.argmax([_clear(v) for v in cands]))])
    at_q = _at(xq)
    spread = max(at_q) - min(at_q)
    ylo, yhi = y.min() - 0.10 * yr, y.max() + 0.30 * yr

    fig, (a, b) = plt.subplots(1, 2, figsize=(12.8, 5.5))

    # ---------------- left: three defensible lines
    a.scatter(x, y, s=62, color=INK, zorder=4)
    for lab, c, col in eyed:
        a.plot(xs, np.polyval(c, xs), color=col, lw=2.4, zorder=3)
        a.text(xs[-1] + 0.022 * xr, float(np.polyval(c, xs[-1])), lab, ha="left",
               va="center", fontsize=12.5, fontweight="bold", color=col, zorder=5)
    a.plot([xq, xq], [min(at_q), max(at_q)], color=ORANGE, lw=2.4, zorder=5)
    for v in (min(at_q), max(at_q)):
        a.plot([xq - 0.012 * xr, xq + 0.012 * xr], [v, v], color=ORANGE, lw=2.4,
               zorder=5)
    a.annotate(f"at {xq:.0f} kg/m³ the three\nlines disagree by {spread:.1f} {unit}",
               xy=(xq, float(np.mean(at_q))),
               xytext=(x.min() + 0.30 * xr, ylo + 0.10 * yr),
               fontsize=10.2, color=ORANGE, fontweight="bold", ha="left",
               va="center", linespacing=1.5, zorder=6,
               bbox=dict(boxstyle="round,pad=0.30", fc=PAPER, ec=ORANGE, lw=1.4),
               arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.7, shrinkA=5,
                               shrinkB=4, connectionstyle="arc3,rad=-0.20"))
    a.text(0.035, 0.965,
           "Three engineers, three straight edges.\n"
           f"A  through the {len(lo)} leanest mixes — slope {eyed[0][1][0]:.3f}\n"
           f"B  through the {len(hi)} richest mixes — slope {eyed[1][1][0]:.3f}\n"
           f"C  through the two end mixes — slope {eyed[2][1][0]:.3f}\n"
           "Every one of them is defensible. They do not agree.",
           transform=a.transAxes, fontsize=9.6, color=INK, va="top", ha="left",
           linespacing=1.6, zorder=6,
           bbox=dict(boxstyle="round,pad=0.38", fc=PAPER, ec=EDGE, lw=1.2))
    a.set_title("BY EYE — every line here is arguable", fontsize=12.5,
                fontweight="bold", color=INK, loc="left", pad=10)

    # ---------------- right: least squares, with the residuals drawn
    yhat = np.polyval(c_ls, x)
    for xi, yi, hi_ in zip(x, y, yhat):
        b.plot([xi, xi], [yi, hi_], color=MUTED, lw=1.3, zorder=2)
    b.scatter(x, y, s=62, color=INK, zorder=4)
    b.plot(xs, np.polyval(c_ls, xs), color=ORANGE, lw=3.0, zorder=3)
    b.text(xs[-1] + 0.022 * xr, float(np.polyval(c_ls, xs[-1])), "LS", ha="left",
           va="center", fontsize=11.5, fontweight="bold", color=ORANGE, zorder=5)
    b.text(0.035, 0.965,
           "THE LEAST-SQUARES LINE\n"
           "Each grey drop-line is one residual: how far\n"
           "that mix sits from the line, measured straight\n"
           "up or straight down.\n"
           "Square all 26 lengths, add them up, and make\n"
           "that total as small as it will go.",
           transform=b.transAxes, fontsize=9.6, color=INK, va="top", ha="left",
           linespacing=1.6, zorder=6,
           bbox=dict(boxstyle="round,pad=0.38", fc=PAPER, ec=ORANGE, lw=1.4))
    b.set_title("LEAST SQUARES — exactly one line wins", fontsize=12.5,
                fontweight="bold", color=ORANGE, loc="left", pad=10)

    for p in (a, b):
        p.set_xlim(x.min() - 0.06 * xr, x.max() + 0.11 * xr)
        p.set_ylim(ylo, yhi)
        p.set_xlabel(xl, fontsize=11)
        p.set_ylabel(yl, fontsize=11)
        _grid(p)

    parts = "   ".join(f"{lab} {ssr(c):,.0f}" for lab, c, _ in eyed)
    fig.text(0.008, 0.075,
             f"Sum of squared residuals over all {len(x)} mixes:   {parts}   "
             f"least squares {ssr(c_ls):,.0f} {unit}²   ← the smallest of the four.",
             fontsize=10.2, color=INK, va="bottom")
    fig.text(0.008, 0.018,
             f"{ILLUS} Every slope and every total above is computed from these "
             f"{len(x)} points at draw time.\nNo line drawn by hand can beat the last "
             f"total — that is the whole content of the phrase “least squares”.",
             fontsize=8.8, color=MUTED, style="italic", va="bottom", linespacing=1.6)
    fig.subplots_adjust(left=0.055, right=0.985, top=0.90, bottom=0.20, wspace=0.20)
    return save(fig, "fit_by_eye.png", pad=0.10)


# =========================================================== W8.2 train/test
def fig_train_test_split():
    x, y, *_ = cohort_data("CML3112", n=160, seed=21)
    n = len(y)
    tr, te = holdout(n, 0.2, seed=42)

    fig, ax = canvas(12.6, 5.30, y0=0.30)
    ax.text(0.25, 5.44, "The model sees one pile of rows. It is scored on the other.",
            fontsize=13.5, fontweight="bold", color=INK, va="center")

    # ---- the whole dataset
    D0, D1, DB, DT = 0.30, 3.20, 3.05, 4.85
    panel(ax, D0, DB, D1 - D0, DT - DB, face=STEEL, edge=INK, lw=2.0, r=0.10)
    for k in range(1, 12):
        yy = DB + k * (DT - DB) / 12.0
        ax.plot([D0 + 0.12, D1 - 0.12], [yy, yy], color="#C3CFDA", lw=1.0, zorder=3)
    ax.text((D0 + D1) / 2, DT + 0.24, "THE WHOLE DATASET", ha="center", va="center",
            fontsize=11.5, fontweight="bold", color=INK)
    ax.text((D0 + D1) / 2, (DB + DT) / 2, f"{n} mixes\n{n} rows", ha="center",
            va="center", fontsize=12.5, fontweight="bold", color=INK,
            linespacing=1.5, zorder=4,
            bbox=dict(boxstyle="round,pad=0.30", fc=PAPER, ec="none", alpha=0.93))

    arrow(ax, (D1 + 0.12, 3.95), (3.98, 3.95), col=TEAL, lw=2.4, ms=20)
    ax.text(3.62, 4.30, "SHUFFLE,\nthen cut", ha="center", va="center", fontsize=9.4,
            fontweight="bold", color=TEAL, linespacing=1.45)

    # ---- train and test, widths in proportion to the row counts
    L, R = 4.20, 12.25
    span = R - L - 0.14
    wtr = span * len(tr) / n
    panel(ax, L, DB, wtr, DT - DB, face="#DCE4EC", edge=INK, lw=2.0, r=0.10)
    panel(ax, L + wtr + 0.14, DB, span - wtr, DT - DB, face=FADE, edge=ORANGE,
          lw=2.2, r=0.10)
    ax.text(L + wtr / 2, DT + 0.24, "TRAIN", ha="center", va="center", fontsize=11.5,
            fontweight="bold", color=INK)
    ax.text(L + wtr + 0.14 + (span - wtr) / 2, DT + 0.24, "TEST", ha="center",
            va="center", fontsize=11.5, fontweight="bold", color=ORANGE)
    ax.text(L + wtr / 2, (DB + DT) / 2, f"80%\n{len(tr)} rows", ha="center",
            va="center", fontsize=13.5, fontweight="bold", color=INK, linespacing=1.5)
    ax.text(L + wtr + 0.14 + (span - wtr) / 2, (DB + DT) / 2, f"20%\n{len(te)}\nrows",
            ha="center", va="center", fontsize=11.5, fontweight="bold", color=ORANGE,
            linespacing=1.5)

    _keyline(ax, 0.30, 2.62, INK,
             "TRAIN — the model sees the features AND the answers. It fits its numbers "
             "here, and nowhere else.")
    _keyline(ax, 0.30, 2.22, ORANGE,
             "TEST — locked in a drawer. The model never sees these answers until the "
             "day you score it.")

    panel(ax, 0.30, 0.55, 11.95, 1.35, face=PAPER, edge=ORANGE, lw=2.0, r=0.10)
    ax.text(0.55, 1.62, "THE FAILURE MODE", fontsize=11.2, fontweight="bold",
            color=ORANGE, va="center", zorder=3)
    ax.text(0.55, 1.20,
            "Score the model on rows it has already seen and you are marking its "
            "memory, not its ability. A model that has\n"
            f"memorised all {n} mixes can score perfectly on those {n} and be "
            "worthless on the 161st — which is the only one that matters.",
            fontsize=9.8, color=INK, va="center", linespacing=1.6, zorder=3)
    ax.text(0.55, 0.76,
            "Shuffle before you cut. If the file arrived sorted by strength, taking the "
            "bottom 20% hands the model only the weak mixes.",
            fontsize=9.2, color=MUTED, style="italic", va="center", zorder=3)
    return save_c(fig, "train_test_split.png")


# ======================================================= W8.3 predicted vs actual
def fig_pred_vs_actual():
    x, y, xl, yl, unit = cohort_data("CML3112", n=160, seed=21)
    tr, te = holdout(len(y), 0.2, seed=42)
    c = np.polyfit(x[tr], y[tr], 1)
    yt, yp = y[te], np.polyval(c, x[te])
    mae, rmse, r2 = reg_metrics(yt, yp)
    worst = int(np.abs(yp - yt).argmax())

    fig, (a, t) = plt.subplots(1, 2, figsize=(12.4, 5.4),
                              gridspec_kw={"width_ratios": [1.12, 1.0]})
    lo = min(yt.min(), yp.min()) - 3.0
    hi = max(yt.max(), yp.max()) + 3.0
    a.plot([lo, hi], [lo, hi], color=TEAL, lw=2.4, ls="--", zorder=2)
    a.scatter(yt, yp, s=64, color=INK, alpha=0.85, zorder=4)
    a.scatter([yt[worst]], [yp[worst]], s=150, facecolor="none", edgecolor=ORANGE,
              lw=2.6, zorder=5)
    a.set_xlim(lo, hi)
    a.set_ylim(lo, hi)
    a.set_aspect("equal", adjustable="box")
    a.set_xlabel(f"ACTUAL 28-day strength ({unit})", fontsize=11)
    a.set_ylabel(f"PREDICTED 28-day strength ({unit})", fontsize=11)
    _grid(a, axis="both")
    # The label needs a leader, or a reader cannot tell which line it names. Put
    # the tip at whichever point on the 45-degree line is furthest from every
    # plotted test mix, so the arrowhead never lands on a datum.
    cand = lo + np.linspace(0.55, 0.95, 60) * (hi - lo)
    clear = [np.min(np.hypot(yt - v, yp - v)) for v in cand]
    tie = float(cand[int(np.argmax(clear))])
    a.annotate("perfect prediction\nlives on this line", xy=(tie, tie),
               xytext=(0.045, 0.955), textcoords=a.transAxes,
               fontsize=9.8, color=TEAL, fontweight="bold",
               va="top", ha="left", linespacing=1.5, zorder=6,
               bbox=dict(boxstyle="round,pad=0.30", fc=PAPER, ec=TEAL, lw=1.3),
               arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.7, shrinkA=6,
                               shrinkB=3, connectionstyle="arc3,rad=-0.18"))
    a.annotate(f"the worst miss:\nout by {abs(yp[worst] - yt[worst]):.1f} {unit}",
               xy=(yt[worst], yp[worst]), xytext=(0.52, 0.10),
               textcoords=a.transAxes, fontsize=9.8, color=ORANGE,
               fontweight="bold", ha="left", va="center", linespacing=1.5, zorder=6,
               bbox=dict(boxstyle="round,pad=0.30", fc=PAPER, ec=ORANGE, lw=1.3),
               arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.7, shrinkA=4,
                               shrinkB=6, connectionstyle="arc3,rad=0.20"))
    a.set_title(f"{len(te)} test mixes the model had never seen", fontsize=12.0,
                fontweight="bold", color=INK, loc="left", pad=10)

    # ---- the three scores, each with what it actually means
    t.set_xlim(0, 1)
    t.set_ylim(0, 1)
    t.axis("off")
    t.text(0.0, 0.985, "THREE WAYS TO SAY HOW WRONG IT IS", fontsize=12.0,
           fontweight="bold", color=ORANGE, va="top")
    cards = [(f"MAE = {mae:.2f} {unit}",
              "Mean absolute error. On a typical test mix the\n"
              "prediction is out by this much. Same units as\n"
              "the target, so you can hand it to a client."),
             (f"RMSE = {rmse:.2f} {unit}",
              "Root mean squared error. The same idea, but a\n"
              "big miss counts far more than several small\n"
              "ones. RMSE is never smaller than MAE."),
             (f"R² = {r2:.3f}",
              "The fit removes this share of the variation the\n"
              "strengths had to begin with. 1.0 is perfect, 0.0 is\n"
              "no better than the mean, and it can go negative.")]
    yy = 0.885
    for head, body in cards:
        t.add_patch(FancyBboxPatch((0.0, yy - 0.235), 1.0, 0.225,
                                   boxstyle="round,pad=0.006,rounding_size=0.02",
                                   transform=t.transAxes, facecolor="#F5F8FB",
                                   edgecolor=EDGE, lw=1.3, clip_on=False))
        t.text(0.028, yy - 0.045, head, fontsize=12.5, fontweight="bold",
               color=INK, va="center")
        t.text(0.028, yy - 0.155, body, fontsize=9.0, color="#3A4C5C", va="center",
               linespacing=1.6)
        yy -= 0.265
    t.text(0.0, 0.055,
           f"All three are computed from the {len(te)} points plotted on the left, "
           f"using a\nstraight-line fit made on the other {len(tr)} rows only.",
           fontsize=9.2, color=MUTED, style="italic", va="center", linespacing=1.6)

    fig.text(0.008, 0.018, ILLUS + " The 80/20 split is a shuffled index split with a "
                           "fixed seed, so this figure is the same every time it is built.",
             fontsize=8.8, color=MUTED, style="italic", va="bottom")
    fig.subplots_adjust(left=0.065, right=0.985, top=0.91, bottom=0.165, wspace=0.16)
    return save(fig, "pred_vs_actual.png", pad=0.10)


# =============================================================== W8.4 residuals
def fig_residuals():
    # left: a straight line on a genuinely straight relationship
    x1, y1, _, _, unit = cohort_data("CML3112", n=110, seed=21)
    c1 = np.polyfit(x1, y1, 1)
    p1 = np.polyval(c1, x1)
    r1 = p1 - y1
    # right: the same straight line on a curved relationship
    age, y2 = curved_strength(n=110, seed=17)
    c2 = np.polyfit(age, y2, 1)
    p2 = np.polyval(c2, age)
    r2 = p2 - y2

    def binned(pred, res, nb=9):
        edges = np.linspace(pred.min(), pred.max(), nb + 1)
        cx, cy = [], []
        for k in range(nb):
            m_ = (pred >= edges[k]) & (pred <= edges[k + 1])
            if m_.sum() >= 3:
                cx.append(pred[m_].mean())
                cy.append(res[m_].mean())
        return np.array(cx), np.array(cy)

    fig, (a, b) = plt.subplots(1, 2, figsize=(12.8, 5.4))
    lim = 1.18 * max(np.abs(r1).max(), np.abs(r2).max())

    for ax, pred, res, col, title in (
            (a, p1, r1, TEAL, "WHAT YOU HOPE TO SEE — no pattern left"),
            (b, p2, r2, ORANGE, "WHAT TELLS YOU THE MODEL IS WRONG")):
        ax.axhline(0, color=INK, lw=2.0, zorder=3)
        ax.scatter(pred, res, s=52, color=INK, alpha=0.75, zorder=4)
        bx, by = binned(pred, res)
        ax.plot(bx, by, color=col, lw=3.0, zorder=5)
        ax.scatter(bx, by, s=46, color=col, zorder=6)
        # headroom above the cloud, so every note sits in empty space instead of
        # on top of a residual
        ax.set_ylim(-lim, lim * 1.95)
        ax.set_xlabel(f"PREDICTED strength ({unit})", fontsize=11)
        ax.set_ylabel(f"residual = predicted − actual ({unit})", fontsize=11)
        ax.set_title(title, fontsize=12.0, fontweight="bold", color=col, loc="left",
                     pad=10)
        _grid(ax)

    w1 = int(np.abs(r1).argmax())
    a.scatter([p1[w1]], [r1[w1]], s=160, facecolor="none", edgecolor=ORANGE, lw=2.4,
              zorder=6)
    a.annotate(f"the worst single mix,\nout by {r1[w1]:+.1f} {unit}",
               xy=(p1[w1], r1[w1]), xytext=(0.985, 0.965), textcoords=a.transAxes,
               fontsize=9.6, color=ORANGE, fontweight="bold", ha="right", va="top",
               linespacing=1.5, zorder=7,
               bbox=dict(boxstyle="round,pad=0.30", fc=PAPER, ec=ORANGE, lw=1.3),
               arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.7, shrinkA=5,
                               shrinkB=6, connectionstyle="arc3,rad=0.22"))
    a.text(0.035, 0.965,
           "Cement content against strength really is close\n"
           "to straight, so the leftovers scatter either side\n"
           "of zero and the teal average line stays flat.",
           transform=a.transAxes, fontsize=9.4, color=INK, va="top", ha="left",
           linespacing=1.6, zorder=7,
           bbox=dict(boxstyle="round,pad=0.34", fc=PAPER, ec=TEAL, lw=1.3))
    b.text(0.035, 0.965,
           "Curing age against strength is NOT straight — the gain is roughly\n"
           "logarithmic in age. Fit a line anyway and the leftovers hold a smile:\n"
           "over-predicted at both ends, under-predicted in the middle. That\n"
           "curve is physics the straight line threw away.",
           transform=b.transAxes, fontsize=9.4, color=INK, va="top", ha="left",
           linespacing=1.6, zorder=7,
           bbox=dict(boxstyle="round,pad=0.34", fc=PAPER, ec=ORANGE, lw=1.3))

    fig.text(0.008, 0.150,
             "Plot residuals against the PREDICTED value, not against the actual value. "
             "Against the actual you get a downward slope even from a perfect model, "
             "because the same measurement noise sits in\nboth axes with opposite signs — "
             "you would diagnose a fault that is not there.",
             fontsize=9.4, color=INK, va="bottom", linespacing=1.6)
    fig.text(0.008, 0.016,
             "Illustrative data. Left: strength against cement content. Right: strength "
             "against curing age, both shaped like the UCI Concrete Compressive Strength "
             "dataset. The thick line is the mean residual in each of nine\nequal bins of "
             "the prediction, computed at draw time — that is the instrument, and it is "
             "the first thing to plot after any fit.",
             fontsize=8.8, color=MUTED, style="italic", va="bottom", linespacing=1.6)
    fig.subplots_adjust(left=0.055, right=0.985, top=0.90, bottom=0.315, wspace=0.20)
    return save(fig, "residuals.png", pad=0.10)


# ========================================================= W8.5 baseline vs model
def fig_baseline_vs_model():
    x, y, xl, _, unit = cohort_data("CML3112", n=160, seed=21)
    tr, te = holdout(len(y), 0.2, seed=42)
    base_val = float(y[tr].mean())
    base_mae = float(np.abs(np.full(len(te), base_val) - y[te]).mean())
    c = np.polyfit(x[tr], y[tr], 1)
    mod_mae = float(np.abs(np.polyval(c, x[te]) - y[te]).mean())
    cut = 100.0 * (base_mae - mod_mae) / base_mae

    fig, ax = plt.subplots(figsize=(11.8, 4.9))
    labs = [f"THE FITTED MODEL\nstraight line on cement content",
            f"THE BASELINE\npredict {base_val:.1f} {unit} every time — the mean of the "
            f"training rows"]
    vals = [mod_mae, base_mae]
    cols = [ORANGE, GREY]
    ax.barh([0, 1], vals, color=cols, height=0.52, zorder=3)
    for i, v in enumerate(vals):
        ax.text(v + base_mae * 0.02, i, f"{v:.2f} {unit}", va="center", ha="left",
                fontsize=13, fontweight="bold", color=cols[i], zorder=4)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(labs, fontsize=10.5, linespacing=1.5)
    ax.set_xlim(0, base_mae * 1.34)
    ax.set_xlabel(f"Mean absolute error on the {len(te)} held-out test mixes ({unit}) "
                  f"— lower is better", fontsize=11)
    ax.set_ylim(-0.62, 1.72)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    _grid(ax, axis="x")

    ax.annotate("", xy=(mod_mae, 1.42), xytext=(base_mae, 1.42),
                arrowprops=dict(arrowstyle="<->", color=TEAL, lw=2.2))
    ax.text((mod_mae + base_mae) / 2, 1.58,
            f"{base_mae - mod_mae:.2f} {unit} better  —  a {cut:.0f}% cut in average error",
            ha="center", va="center", fontsize=11.0, fontweight="bold", color=TEAL)
    for v in (mod_mae, base_mae):
        ax.plot([v, v], [1.30, 1.42], color=TEAL, lw=1.2, ls=(0, (2, 2)), zorder=2)

    ax.set_title("Did the model earn its keep?", fontsize=13.5, fontweight="bold",
                 color=INK, loc="left", pad=14)
    fig.text(0.008, 0.135,
             "The baseline is not a strawman. It is the best answer available with no "
             "model at all, and any model that cannot beat it is not a model.",
             fontsize=10.2, color=INK, va="bottom")
    fig.text(0.008, 0.018,
             f"{ILLUS} Both bars are scored on the same {len(te)} test rows.\nThe "
             f"baseline value {base_val:.1f} {unit} is the mean of the {len(tr)} "
             f"TRAINING rows — taking the mean of the test rows would itself be leakage.",
             fontsize=8.8, color=MUTED, style="italic", va="bottom", linespacing=1.6)
    fig.subplots_adjust(left=0.325, right=0.985, top=0.86, bottom=0.295)
    return save(fig, "baseline_vs_model.png", pad=0.10)


# =========================================================== W8.6 error metrics
def fig_error_metrics():
    x, y, xl, yl, unit = cohort_data("CML3112", n=8, seed=44)
    o = np.argsort(x)
    x, y = x[o], y[o]
    y = y.copy()
    odd = 5
    y[odd] -= 15.0                      # one mix well below its cement content
    c = np.polyfit(x, y, 1)
    yhat = np.polyval(c, x)
    res = yhat - y
    sq = res ** 2
    mae = float(np.abs(res).mean())
    rmse = float(np.sqrt(sq.mean()))
    ybar = float(y.mean())
    ss_tot = float(((y - ybar) ** 2).sum())
    ss_res = float(sq.sum())
    r2 = 1.0 - ss_res / ss_tot
    share = 100.0 * sq[odd] / sq.sum()
    xs = np.linspace(x.min(), x.max(), 60)
    xr = x.max() - x.min()
    ylo = min(y.min(), yhat.min()) - 8.0
    yhi = max(y.max(), yhat.max()) + 16.0

    fig, (a, b, c3) = plt.subplots(1, 3, figsize=(12.9, 5.3))

    # ---- 1. MAE.  The average residual length is shown as a band of exactly
    # +/- MAE either side of the fit, because a 3.6 MPa scale bar on a 60 MPa
    # axis is too small to read.
    a.fill_between(xs, np.polyval(c, xs) - mae, np.polyval(c, xs) + mae,
                   color=ORANGE, alpha=0.16, lw=0, zorder=1)
    for xi, yi, hi_ in zip(x, y, yhat):
        a.plot([xi, xi], [yi, hi_], color=ORANGE, lw=2.0, zorder=3)
    a.plot(xs, np.polyval(c, xs), color=INK, lw=2.4, zorder=4)
    a.scatter(x, y, s=76, color=INK, zorder=5)
    a.scatter([x[odd]], [y[odd]], s=110, color=ORANGE, zorder=6)
    a.set_ylim(ylo, yhi)
    a.set_xlim(x.min() - 0.10 * xr, x.max() + 0.10 * xr)
    a.text(x[odd] + 0.035 * xr, y[odd], f"mix {odd + 1}", ha="left", va="center",
           fontsize=9.4, fontweight="bold", color=ORANGE, zorder=7)
    a.set_title("1 · MAE — average length", fontsize=11.8, fontweight="bold",
                color=ORANGE, loc="left", pad=10)
    a.text(0.035, 0.965,
           f"Add the {len(x)} orange lengths, divide\n"
           f"by {len(x)}. Every mix counts the same.\n"
           f"MAE = {mae:.2f} {unit} — the shaded band\n"
           f"is the fit ± that, the size of a\n"
           f"typical miss.",
           transform=a.transAxes, fontsize=9.2, color=INK, va="top", ha="left",
           linespacing=1.6, zorder=7,
           bbox=dict(boxstyle="round,pad=0.30", fc=PAPER, ec=ORANGE, lw=1.3))
    a.set_ylabel(f"28-day strength ({unit})", fontsize=10.5)
    a.set_xlabel("Cement content (kg/m³)", fontsize=10.5)

    # ---- 2. RMSE
    cols = [ORANGE if i == odd else "#B9C8D8" for i in range(len(x))]
    b.bar(np.arange(1, len(x) + 1), sq, color=cols, width=0.62, zorder=3)
    b.set_xticks(np.arange(1, len(x) + 1))
    b.set_xlabel("mix number, ordered by cement content", fontsize=10.5)
    b.set_ylabel(f"squared residual ({unit}²)", fontsize=10.5)
    b.set_ylim(0, sq.max() * 1.62)
    b.set_title("2 · RMSE — a big miss counts more", fontsize=11.8,
                fontweight="bold", color=ORANGE, loc="left", pad=10)
    b.annotate(f"mix {odd + 1} alone is {share:.0f}% of the\ntotal, though it is only "
               f"{100 * abs(res[odd]) / np.abs(res).sum():.0f}% of\nthe orange length "
               f"in panel 1",
               xy=(odd + 1, sq[odd]), xytext=(0.035, 0.50), textcoords=b.transAxes,
               fontsize=9.2, color=ORANGE, fontweight="bold", ha="left", va="center",
               linespacing=1.6, zorder=6,
               bbox=dict(boxstyle="round,pad=0.30", fc=PAPER, ec=ORANGE, lw=1.3),
               arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.7, shrinkA=6,
                               shrinkB=4, connectionstyle="arc3,rad=-0.18"))
    b.text(0.035, 0.965, f"RMSE = √(mean of these bars)\n     = {rmse:.2f} {unit}",
           transform=b.transAxes, fontsize=9.6, color=INK, va="top", ha="left",
           fontweight="bold", linespacing=1.7, zorder=6,
           bbox=dict(boxstyle="round,pad=0.30", fc=PAPER, ec=EDGE, lw=1.1))
    _grid(b)

    # ---- 3. R-squared
    for xi, yi in zip(x, y):
        c3.plot([xi, xi], [yi, ybar], color=GREY, lw=2.0, zorder=3)
    c3.plot([x.min() - 0.10 * xr, x.max() + 0.10 * xr], [ybar, ybar], color=INK,
            lw=2.2, ls="--", zorder=4)
    c3.plot(xs, np.polyval(c, xs), color=ORANGE, lw=2.4, zorder=4)
    c3.scatter(x, y, s=76, color=INK, zorder=5)
    c3.set_ylim(ylo, yhi)
    # A left margin with no data in it, so the mean line can be named without
    # the label landing on a grey segment.
    c3.set_xlim(x.min() - 0.34 * xr, x.max() + 0.10 * xr)
    c3.text(x.min() - 0.31 * xr, ybar, f"mean\n{ybar:.1f}", ha="left", va="center",
            fontsize=9.0, color=INK, fontweight="bold", linespacing=1.4, zorder=6)
    c3.set_title("3 · R² — measured against the mean", fontsize=11.8,
                 fontweight="bold", color=ORANGE, loc="left", pad=10)
    c3.text(0.035, 0.965,
            f"grey, to the mean line:\n"
            f"   SS$_{{tot}}$ = {ss_tot:,.0f} {unit}²\n"
            f"orange, to the fitted line\n(panel 1):\n"
            f"   SS$_{{res}}$ = {ss_res:,.0f} {unit}²\n"
            f"R² = 1 − {ss_res:,.0f}/{ss_tot:,.0f} = {r2:.3f}",
            transform=c3.transAxes, fontsize=9.2, color=INK, va="top", ha="left",
            linespacing=1.65, zorder=6,
            bbox=dict(boxstyle="round,pad=0.30", fc=PAPER, ec=ORANGE, lw=1.3))
    c3.set_xlabel("Cement content (kg/m³)", fontsize=10.5)
    c3.set_ylabel(f"28-day strength ({unit})", fontsize=10.5)

    fig.text(0.008, 0.018,
             f"The same {len(x)} mixes and the same least-squares line in all three "
             f"panels. Illustrative data shaped like the UCI Concrete Compressive "
             f"Strength dataset, with mix {odd + 1} placed 15 {unit} below the line on "
             f"purpose so that\nthe difference between MAE and RMSE has something to "
             f"show. Every number above is recomputed from these eight points at draw "
             f"time.",
             fontsize=8.8, color=MUTED, style="italic", va="bottom", linespacing=1.6)
    fig.subplots_adjust(left=0.052, right=0.988, top=0.90, bottom=0.215, wspace=0.28)
    return save(fig, "error_metrics.png", pad=0.10)


# ===============================================================================
# WEEK 9 — CLASSIFICATION
# ===============================================================================
AI4I = ("Worked example from mechanical maintenance: illustrative data shaped like the "
        "AI4I 2020 Predictive Maintenance dataset, in which overstrain failure is defined "
        "by tool wear times torque. The reasoning transfers to any discipline; the numbers "
        "are not yours.")
SHORT = ["torque", "tool wear"]
SUNIT = ["N·m", "min"]


def _rule(feat, thr, op="≤"):
    return f"{SHORT[feat]} {op} {thr:.0f} {SUNIT[feat]}"


# ======================================================== W9.1 decision boundary
def fig_decision_boundary():
    X, y = machine_sensors(n=170, seed=53)
    w, b, proba = logistic_fit(X, y)
    p = proba(X)

    def counts_at(thr):
        return conf_counts(y, (p >= thr).astype(int))

    T_LO, T_HI = 0.50, 0.20
    c_hi, c_lo = counts_at(T_LO), counts_at(T_HI)
    m_hi, m_lo = clf_metrics(*c_hi), clf_metrics(*c_lo)

    tg = np.linspace(X[:, 0].min() - 2, X[:, 0].max() + 2, 100)

    def wear_at(thr):
        # w0*T + w1*W + b = log(thr/(1-thr))  ->  solve for W
        return (np.log(thr / (1 - thr)) - b - w[0] * tg) / w[1]

    fig, (a, t) = plt.subplots(1, 2, figsize=(12.6, 5.6),
                              gridspec_kw={"width_ratios": [1.10, 1.0]})
    # Empty bands above and below the cloud so each region can be named inside
    # the region it names, without a label landing on a machine-hour. The tick
    # list is set explicitly so the padding never shows a negative tool wear.
    ylo, yhi = -58.0, 336.0
    a.fill_between(tg, wear_at(T_LO), yhi, color=ORANGE, alpha=0.11, lw=0, zorder=1)
    a.fill_between(tg, ylo, wear_at(T_LO), color=TEAL, alpha=0.10, lw=0, zorder=1)
    ok, bad = y == 0, y == 1
    a.scatter(X[ok, 0], X[ok, 1], s=52, color=TEAL, zorder=4,
              label=f"ran fine ({int(ok.sum())} hours)")
    a.scatter(X[bad, 0], X[bad, 1], s=62, color=ORANGE, marker="X", zorder=4,
              label=f"failed ({int(bad.sum())} hours)")
    a.plot(tg, wear_at(T_LO), color=INK, lw=3.0, zorder=5,
           label="boundary at p = 0.50")
    a.plot(tg, wear_at(T_HI), color=ORANGE, lw=2.4, ls="--", zorder=5,
           label="boundary at p = 0.20")
    a.set_xlim(tg.min(), tg.max())
    a.set_ylim(ylo, yhi)
    a.set_yticks([0, 50, 100, 150, 200, 250])
    a.set_xlabel(SENSOR_NAMES[0], fontsize=11)
    a.set_ylabel(SENSOR_NAMES[1], fontsize=11)
    a.text(0.030, 0.975, "above the solid line the model calls it a FAILURE",
           transform=a.transAxes, fontsize=9.6, color=ORANGE, fontweight="bold",
           va="top", ha="left", zorder=6)
    a.text(0.970, 0.020, "below it, FINE", transform=a.transAxes, fontsize=9.6,
           color=TEAL, fontweight="bold", va="bottom", ha="right", zorder=6)
    # legend outside the axes: two of its four keys are marker shapes that would
    # otherwise read as data points
    a.legend(frameon=False, fontsize=9.6, loc="upper center",
             bbox_to_anchor=(0.5, -0.145), ncol=2)
    _grid(a, axis="both")
    a.set_title(f"{len(y)} machine-hours, two sensors", fontsize=12.0,
                fontweight="bold", color=INK, loc="left", pad=10)

    t.set_xlim(0, 1)
    t.set_ylim(0, 1)
    t.axis("off")
    t.text(0.0, 0.995, "THE LINE IS A CHOICE, NOT A FACT", fontsize=12.5,
           fontweight="bold", color=ORANGE, va="top")
    t.text(0.0, 0.915,
           "Logistic regression does not hand you a line. It hands\n"
           "you a probability of failure for every machine-hour.\n"
           "The line is only the place where that probability\n"
           "crosses a number that YOU picked.",
           fontsize=9.6, color=INK, va="top", linespacing=1.65)
    rows = [("p = 0.50  —  the default nobody chose", INK, c_hi, m_hi,
             "You stop the line only when the model is more sure\n"
             "than not. Fewer false alarms, more failures missed."),
            ("p = 0.20  —  a cautious plant", ORANGE, c_lo, m_lo,
             "You stop the line on a one-in-five suspicion. You\n"
             "catch more failures and you cry wolf more often.")]
    yy = 0.700
    for head, col, (tn, fp, fn, tp), (acc, pre, rec, f1), note in rows:
        t.add_patch(FancyBboxPatch((0.0, yy - 0.27), 1.0, 0.26,
                                   boxstyle="round,pad=0.006,rounding_size=0.02",
                                   transform=t.transAxes, facecolor="#F5F8FB",
                                   edgecolor=col, lw=1.6, clip_on=False))
        t.text(0.025, yy - 0.045, head, fontsize=10.6, fontweight="bold", color=col,
               va="center")
        t.text(0.025, yy - 0.130,
               f"caught {tp} of {tp + fn} failures · {fp} false alarms · "
               f"accuracy {acc:.0%}",
               fontsize=9.4, color=INK, va="center", fontweight="bold")
        t.text(0.025, yy - 0.213, note, fontsize=9.0, color="#3A4C5C", va="center",
               linespacing=1.6)
        yy -= 0.300
    t.text(0.0, 0.005,
           "Nothing in the data tells you 0.5. Only the cost of each kind of\n"
           "mistake does — an engineering decision, not a modelling one.",
           fontsize=9.4, color=ORANGE, style="italic", va="bottom", linespacing=1.65)

    fig.text(0.008, 0.018, wrapped(AI4I + " The boundary is straight because the "
                                    "model is linear — that is a second choice, made "
                                    "before the first."),
             fontsize=8.8, color=MUTED, style="italic", va="bottom", linespacing=1.6)
    fig.subplots_adjust(left=0.062, right=0.988, top=0.91, bottom=0.275, wspace=0.14)
    return save(fig, "decision_boundary.png", pad=0.10)


# ============================================================= W9.2 decision tree
def fig_decision_tree():
    X, y = machine_sensors(n=900, seed=29)
    tr, te = holdout(len(y), 0.3, seed=3)
    node = grow_tree(X[tr], y[tr], 2, min_leaf=25)
    acc = float((tree_predict(node, X[te]) == y[te]).mean())
    L, R = node["left"], node["right"]
    leaves = [L["left"], L["right"], R["left"], R["right"]]

    fig, ax = canvas(12.7, 6.18, y0=0.05)
    ax.text(0.25, 6.12, "A decision tree is a rule an engineer can follow",
            fontsize=13.5, fontweight="bold", color=INK, va="center")

    def box(x, yb, w, h, face, edge, lw=2.0):
        panel(ax, x, yb, w, h, face=face, edge=edge, lw=lw, r=0.10)

    # ---- root
    RW, RX, RY, RH = 3.60, 4.55, 4.85, 0.90
    box(RX, RY, RW, RH, STEEL, INK)
    ax.text(RX + RW / 2, RY + RH - 0.30, _rule(node["feat"], node["thr"]) + " ?",
            ha="center", va="center", fontsize=12.0, fontweight="bold", color=INK,
            zorder=3)
    ax.text(RX + RW / 2, RY + 0.26,
            f"{node['n']} machine-hours · {node['pos']} failed",
            ha="center", va="center", fontsize=9.2, color=MUTED, zorder=3)

    # ---- the two second questions
    MW, MH, MY = 3.60, 0.90, 3.20
    mid_x = [1.35, 7.75]
    for k, (nd, mx) in enumerate(zip((L, R), mid_x)):
        box(mx, MY, MW, MH, STEEL, INK)
        ax.text(mx + MW / 2, MY + MH - 0.30, _rule(nd["feat"], nd["thr"]) + " ?",
                ha="center", va="center", fontsize=12.0, fontweight="bold", color=INK,
                zorder=3)
        ax.text(mx + MW / 2, MY + 0.26,
                f"{nd['n']} machine-hours · {nd['pos']} failed", ha="center",
                va="center", fontsize=9.2, color=MUTED, zorder=3)
        arrow(ax, (RX + RW / 2 + (0.55 if k else -0.55), RY - 0.04),
              (mx + MW / 2, MY + MH + 0.04), col=INK, lw=2.0, ms=17)
    ax.text(3.55, 4.42, "YES", ha="center", va="center", fontsize=10.0,
            fontweight="bold", color=TEAL, zorder=5,
            bbox=dict(boxstyle="round,pad=0.20", fc=PAPER, ec="none"))
    ax.text(9.15, 4.42, "NO", ha="center", va="center", fontsize=10.0,
            fontweight="bold", color=TEAL, zorder=5,
            bbox=dict(boxstyle="round,pad=0.20", fc=PAPER, ec="none"))

    # ---- four leaves
    LW, LH, LY = 2.86, 1.16, 1.30
    lx = [0.25, 3.35, 6.45, 9.55]
    for k, (nd, x0) in enumerate(zip(leaves, lx)):
        rate = nd["pos"] / nd["n"]
        alarm = nd["cls"] == 1
        box(x0, LY, LW, LH, FADE if alarm else FADE_T, ORANGE if alarm else TEAL,
            lw=2.4 if alarm else 1.8)
        ax.text(x0 + LW / 2, LY + LH - 0.26,
                "EXPECT FAILURE" if alarm else "EXPECT FINE", ha="center",
                va="center", fontsize=11.2, fontweight="bold",
                color=ORANGE if alarm else TEAL, zorder=3)
        ax.text(x0 + LW / 2, LY + 0.58, f"{nd['pos']} of {nd['n']} failed",
                ha="center", va="center", fontsize=10.4, color=INK, zorder=3)
        ax.text(x0 + LW / 2, LY + 0.26, f"{rate:.0%} of the hours in this leaf",
                ha="center", va="center", fontsize=8.8, color=MUTED, zorder=3)
        parent_x = mid_x[k // 2] + MW / 2
        arrow(ax, (parent_x + (0.55 if k % 2 else -0.55), MY - 0.04),
              (x0 + LW / 2, LY + LH + 0.04), col=INK, lw=1.8, ms=15)
    for xx in (1.90, 4.50, 8.30, 10.90):
        ax.text(xx, 2.80, "yes" if xx in (1.90, 8.30) else "no", ha="center",
                va="center", fontsize=8.8, color=MUTED, zorder=5,
                bbox=dict(boxstyle="round,pad=0.16", fc=PAPER, ec="none"))

    worst = leaves[int(np.argmax([nd["pos"] / nd["n"] for nd in leaves]))]
    ax.text(0.25, 0.86,
            f"Read the orange leaf as a maintenance rule:  IF "
            f"{_rule(node['feat'], node['thr'], '>')}  AND  "
            f"{_rule(R['feat'], R['thr'], '>')}  THEN take the machine off line.",
            fontsize=10.6, color=INK, va="center", fontweight="bold")
    ax.text(0.25, 0.52,
            f"{worst['pos']} of the {worst['n']} training hours that met both "
            f"conditions did fail. The whole tree gets {acc:.0%} of the "
            f"{len(te)} held-out hours right.",
            fontsize=9.8, color=INK, va="center")
    caption(ax, 0.25, 0.24, wrapped(AI4I + " Both split thresholds were found by "
                                    "searching every candidate cut and keeping the "
                                    "one that lowered Gini impurity most.", 175),
            fs=9.0)
    return save_c(fig, "decision_tree.png")


# =============================================================== W9.3 forest vote
def fig_forest_vote():
    X, y = machine_sensors(n=900, seed=29)
    tr, te = holdout(len(y), 0.3, seed=3)
    Xtr, ytr, Xte, yte = X[tr], y[tr], X[te], y[te]
    rng = np.random.default_rng(1)
    trees = []
    for _ in range(5):
        bs = rng.integers(0, len(ytr), len(ytr))
        trees.append(grow_tree(Xtr[bs], ytr[bs], 2, 25, "gini", rng=rng, max_feats=1))
    accs = [float((tree_predict(t, Xte) == yte).mean()) for t in trees]
    P = np.array([tree_predict(t, Xte) for t in trees])
    ens = (P.mean(0) >= 0.5).astype(float)
    ens_acc = float((ens == yte).mean())
    # the case to trace: the trees must disagree AND the vote must be right
    split = [i for i in range(len(yte))
             if 1 <= P[:, i].sum() <= 4 and ens[i] == yte[i]]
    case = int(split[1])
    votes = P[:, case].astype(int)
    n_pos = int(votes.sum())

    fig, ax = canvas(12.70, 5.62, y0=0.04)
    ax.text(0.25, 5.50, "Five trees, five opinions, one answer", fontsize=13.5,
            fontweight="bold", color=INK, va="center")

    # ---- the one machine-hour being asked about, top centre
    QX, QW = 4.30, 4.20
    panel(ax, QX, 4.36, QW, 0.80, face=STEEL, edge=INK, lw=2.0, r=0.10)
    ax.text(QX + QW / 2, 4.98, "ONE MACHINE-HOUR", ha="center", va="center",
            fontsize=10.0, fontweight="bold", color=INK, zorder=3)
    ax.text(QX + QW / 2, 4.70,
            f"torque {Xte[case, 0]:.0f} N·m · tool wear {Xte[case, 1]:.0f} min",
            ha="center", va="center", fontsize=10.2, color=INK, zorder=3)
    ax.text(QX + QW / 2, 4.48,
            f"it actually {'FAILED' if yte[case] else 'ran fine'}", ha="center",
            va="center", fontsize=10.0, fontweight="bold",
            color=ORANGE if yte[case] else TEAL, zorder=3)

    # ---- five trees, fed from one bus so it is clear all five see the same hour
    TW, TG, TX, TY, TH = 2.32, 0.14, 0.25, 2.32, 1.62
    centres = [TX + k * (TW + TG) + TW / 2 for k in range(5)]
    ax.plot([QX + QW / 2, QX + QW / 2], [4.36, 4.20], color=GREY, lw=1.6, zorder=2)
    ax.plot([centres[0], centres[-1]], [4.20, 4.20], color=GREY, lw=1.6, zorder=2)
    for cx in centres:
        arrow(ax, (cx, 4.20), (cx, TY + TH + 0.04), col=GREY, lw=1.6, ms=13)

    for k, (t, acc, v) in enumerate(zip(trees, accs, votes)):
        x0 = TX + k * (TW + TG)
        right = (v == yte[case])
        # Border says RIGHT OR WRONG (teal = correct, per the house palette).
        # The chip inside says WHICH CLASS the tree voted for. The two are not
        # the same thing, and colouring the border by the vote would make a
        # wrong tree look like the good case.
        panel(ax, x0, TY, TW, TH, face=PAPER, edge=TEAL if right else ORANGE,
              lw=2.2, r=0.10)
        ax.text(x0 + TW / 2, TY + TH - 0.24, f"TREE {k + 1}", ha="center",
                va="center", fontsize=10.2, fontweight="bold", color=INK, zorder=3)
        ax.text(x0 + TW / 2, TY + TH - 0.60,
                f"starts by asking\n{_rule(t['feat'], t['thr'])} ?", ha="center",
                va="center", fontsize=8.8, color="#3A4C5C", linespacing=1.5, zorder=3)
        ax.add_patch(FancyBboxPatch((x0 + 0.20, TY + 0.34), TW - 0.40, 0.36,
                                    boxstyle="round,pad=0,rounding_size=0.06",
                                    facecolor=ORANGE if v else "#4A6B84",
                                    edgecolor="none", zorder=2))
        ax.text(x0 + TW / 2, TY + 0.52, "FAILURE" if v else "FINE", ha="center",
                va="center", fontsize=10.6, fontweight="bold", color=PAPER, zorder=3)
        ax.text(x0 + TW / 2, TY + 0.16,
                f"{'right' if right else 'WRONG'} here · {acc:.0%} overall",
                ha="center", va="center", fontsize=8.6,
                color=TEAL if right else ORANGE, fontweight="bold", zorder=3)
        arrow(ax, (x0 + TW / 2, TY - 0.04), (x0 + TW / 2, 2.06), col=GREY, lw=1.6,
              ms=13)

    # ---- the vote, underneath, because that is the direction the work flows
    panel(ax, 0.25, 1.16, 12.20, 0.90, face=FADE, edge=ORANGE, lw=2.2, r=0.10)
    ax.text(0.50, 1.83, "THE VOTE", fontsize=10.0, fontweight="bold", color=ORANGE,
            va="center", zorder=3)
    ax.text(2.05, 1.83,
            f"{n_pos} say FAILURE, {5 - n_pos} say FINE  →  the forest answers "
            f"{'FAILURE' if n_pos >= 3 else 'FINE'}, which is correct.",
            fontsize=11.0, fontweight="bold", color=INK, va="center", zorder=3)
    ax.text(0.50, 1.44,
            f"{5 - n_pos if n_pos >= 3 else n_pos} of the five got this hour wrong. "
            f"The majority did not. Over all {len(yte)} held-out hours the five score "
            f"{min(accs):.0%} to {max(accs):.0%} on their own, {np.mean(accs):.0%} on "
            f"average; voting together, {ens_acc:.0%}.",
            fontsize=9.4, color=INK, va="center", zorder=3)

    ax.text(0.25, 0.83,
            "You cannot tell in advance which tree got lucky. That is the argument "
            "for asking all of them — a random forest is this, with hundreds of trees.",
            fontsize=10.2, fontweight="bold", color=INK, va="center")
    caption(ax, 0.25, 0.50,
            "Each tree is grown on its own bootstrap resample of the training rows and "
            "may consider only one randomly chosen sensor at each split, which is why "
            "they disagree at all. Each asks two", fs=9.0)
    caption(ax, 0.25, 0.22,
            "questions, not one; only its first is printed above, and the chip is the "
            "whole tree's answer. Worked example from mechanical maintenance, shaped like the "
            "AI4I 2020 set.",
            fs=9.0)
    return save_c(fig, "forest_vote.png")


# ========================================================== W9.4 confusion matrix
CM = {
    "CML3112": dict(
        pos="mix will FAIL the spec", neg="mix is FINE",
        aff="mix was below spec", ann="mix was fine",
        tp="You rejected a weak mix before it\nwas poured. Correct, and cheap.",
        fp="You scrapped concrete that would\nhave passed. Money, and a lost day.",
        fn="Weak concrete went into a structure\nand nobody knew. This is the cell\nthat matters.",
        tn="The mix was poured and it held.\nCorrect.",
        title="CML3112  ·  concrete mixes  ·  positive class = 28-day strength "
              "below the 32 MPa spec"),
    "CML3113": dict(
        pos="batch is OFF-SPEC", neg="batch is IN SPEC",
        aff="batch was off-spec", ann="batch was in spec",
        tp="The batch was re-floated before it\nleft the plant. Correct.",
        fp="You re-processed good concentrate.\nLost throughput and reagent.",
        fn="Off-spec concentrate was shipped.\nThe customer finds it, not you.",
        tn="The batch was shipped and it met\nspec. Correct.",
        title="CML3113  ·  froth flotation batches  ·  positive class = silica in "
              "concentrate above the 3% spec"),
    "CML3111": dict(
        pos="machine will FAIL", neg="machine is FINE",
        aff="machine failed", ann="machine was fine",
        tp="You stopped the machine and it was\nabout to go. Correct.",
        fp="A false alarm. You stopped a healthy\nline and lost the shift's output.",
        fn="You said fine, it failed. This is the\none that destroys the machine.",
        tn="You said fine and it was. The line\nkept running. Correct.",
        title="CML3111  ·  machine-hours  ·  positive class = failure in the next "
              "interval"),
}


def _cohort_clf(code):
    """Fit one honest classifier per cohort and return the held-out counts."""
    if code == "CML3112":
        X, y, _ = concrete_table(400, seed=23)
        yc = (y < 35).astype(int)
        cols, seed = [0, 1], 13
        src = ("Illustrative data shaped like the UCI Concrete Compressive Strength "
               "dataset. Logistic regression on cement and water content.")
    elif code == "CML3113":
        X, silica, _ = flotation_table(400, seed=41)
        yc = (silica > 2.5).astype(int)
        cols, seed = [0, 1, 2], 7
        src = ("Illustrative data shaped like the froth flotation process dataset "
               "(Kaggle). Logistic regression on feed rate, reagent flow and pulp pH.")
    else:
        X, yc = machine_sensors(900, seed=29)
        cols, seed = [0, 1], 3
        src = AI4I + " Logistic regression on torque and tool wear."
    tr, te = holdout(len(yc), 0.3, seed=seed)
    _, _, proba = logistic_fit(X[tr][:, cols], yc[tr])
    pred = (proba(X[te][:, cols]) >= 0.5).astype(int)
    return conf_counts(yc[te], pred), len(te), src


def fig_confusion_matrix(code):
    (tn, fp, fn, tp), n_te, src = _cohort_clf(code)
    acc, pre, rec, f1 = clf_metrics(tn, fp, fn, tp)
    d = CM[code]

    fig, ax = canvas(12.70, 5.90, y0=0.26)
    ax.text(0.25, 6.06, "Four outcomes, and they do not cost the same",
            fontsize=13.5, fontweight="bold", color=INK, va="center")
    ax.text(0.25, 5.74, d["title"], fontsize=9.8, color=MUTED, style="italic",
            va="center")

    CX, CW, CH = 1.85, 3.28, 1.62
    xs_ = [CX, CX + CW + 0.12]
    ys_ = [3.32, 1.58]          # top row = things that really were positive
    heads = [f"PREDICTED:\n{d['neg']}", f"PREDICTED:\n{d['pos']}"]
    for j, h in enumerate(heads):
        ax.text(xs_[j] + CW / 2, 5.22, h, ha="center", va="center", fontsize=9.6,
                fontweight="bold", color=INK, linespacing=1.5)
    for i, lab in enumerate([f"ACTUAL:\n{d['aff']}", f"ACTUAL:\n{d['ann']}"]):
        ax.text(CX - 0.22, ys_[i] + CH / 2, lab, ha="center", va="center",
                fontsize=9.6, fontweight="bold", color=INK, rotation=90,
                linespacing=1.4)

    cells = [(0, 0, fn, "FALSE NEGATIVE", d["fn"], ORANGE, True),
             (0, 1, tp, "TRUE POSITIVE", d["tp"], TEAL, False),
             (1, 0, tn, "TRUE NEGATIVE", d["tn"], TEAL, False),
             (1, 1, fp, "FALSE POSITIVE", d["fp"], ORANGE, False)]
    for i, j, cnt, name, note, col, solid in cells:
        x0, y0_ = xs_[j], ys_[i]
        panel(ax, x0, y0_, CW, CH, face=col if solid else (FADE if col is ORANGE
                                                           else FADE_T),
              edge=col, lw=2.6 if solid else 1.8, r=0.10)
        txt = PAPER if solid else col
        ax.text(x0 + 0.24, y0_ + CH - 0.30, name, ha="left", va="center",
                fontsize=9.6, fontweight="bold", color=txt, zorder=3)
        ax.text(x0 + CW - 0.24, y0_ + CH - 0.36, f"{cnt}", ha="right", va="center",
                fontsize=21, fontweight="bold", color=txt, zorder=3)
        ax.text(x0 + 0.24, y0_ + 0.52, note, ha="left", va="center", fontsize=8.6,
                color=PAPER if solid else "#33454F", linespacing=1.55, zorder=3)

    # ---- the four scores, each with the question it answers
    MX = 8.85
    panel(ax, MX, 1.50, 3.80, 3.44, face="#F5F8FB", edge=EDGE, lw=1.4, r=0.10)
    ax.text(MX + 0.24, 4.68, "WHAT THE COUNTS ADD UP TO", fontsize=10.2,
            fontweight="bold", color=ORANGE, va="center", zorder=3)
    sc = [(f"Accuracy  {acc:.1%}",
           f"({tp}+{tn}) / {n_te}\nhow often it is right at all"),
          (f"Precision  {pre:.1%}",
           f"{tp} / ({tp}+{fp})\nof the ones it flagged, how many really were"),
          (f"Recall  {rec:.1%}",
           f"{tp} / ({tp}+{fn})\nof the ones that really were, how many it caught"),
          (f"F1  {f1:.1%}",
           "the harmonic mean of precision and recall")]
    yy = 4.28
    for head, body in sc:
        ax.text(MX + 0.24, yy, head, fontsize=11.0, fontweight="bold", color=INK,
                va="center", zorder=3)
        ax.text(MX + 0.24, yy - 0.38, body, fontsize=8.6, color="#3A4C5C",
                va="center", linespacing=1.55, zorder=3)
        yy -= 0.76
    caption(ax, 0.25, 1.12, "Precision and recall answer different questions. Ask "
                            "which mistake your client can least afford, then quote "
                            "the one that measures it.", fs=10.0, col=INK,
            italic=False)
    caption(ax, 0.25, 0.78, f"Every count above comes from {n_te} held-out rows the "
                            f"model never saw, and all four scores are computed from "
                            f"those four counts at draw time.", fs=9.0)
    caption(ax, 0.25, 0.44, src, fs=9.0)
    return save_c(fig, f"confusion_matrix_{code}.png")


# ======================================================= W9.5 threshold trade-off
def fig_threshold_tradeoff():
    X, y = machine_sensors(n=1500, seed=29)
    tr, te = holdout(len(y), 0.3, seed=3)
    _, _, proba = logistic_fit(X[tr], y[tr])
    p = proba(X[te])
    yte = y[te]
    ts = np.arange(0.05, 0.96, 0.01)
    pre, rec = [], []
    for t_ in ts:
        c = conf_counts(yte, (p >= t_).astype(int))
        _, pr, rc, _ = clf_metrics(*c)
        pre.append(pr)
        rec.append(rc)
    pre, rec = np.array(pre), np.array(rec)

    def at(t_):
        c = conf_counts(yte, (p >= t_).astype(int))
        return c, clf_metrics(*c)

    T1, T2 = 0.20, 0.70
    c1, m1 = at(T1)
    c2, m2 = at(T2)

    fig, (a, t) = plt.subplots(1, 2, figsize=(12.6, 5.4),
                              gridspec_kw={"width_ratios": [1.18, 1.0]})
    a.plot(ts, 100 * rec, color=ORANGE, lw=3.0, zorder=4, label="RECALL — share of "
                                                                "real failures caught")
    a.plot(ts, 100 * pre, color=TEAL, lw=3.0, zorder=4, label="PRECISION — share of "
                                                              "alarms that were real")
    for t_, col in ((T1, ORANGE), (T2, TEAL)):
        a.axvline(t_, color=INK, lw=1.4, ls=(0, (4, 3)), zorder=2)
    a.scatter([T1, T1], [100 * m1[1], 100 * m1[2]], s=95, color=INK, zorder=6)
    a.scatter([T2, T2], [100 * m2[1], 100 * m2[2]], s=95, color=INK, zorder=6)
    a.set_xlim(0.05, 0.95)
    a.set_ylim(0, 108)
    a.set_xlabel("threshold — the probability above which you call it a failure",
                 fontsize=11)
    a.set_ylabel("per cent", fontsize=11)
    a.text(T1, 104, "A", ha="center", va="center", fontsize=12, fontweight="bold",
           color=INK, zorder=7,
           bbox=dict(boxstyle="circle,pad=0.22", fc=PAPER, ec=INK, lw=1.6))
    a.text(T2, 104, "B", ha="center", va="center", fontsize=12, fontweight="bold",
           color=INK, zorder=7,
           bbox=dict(boxstyle="circle,pad=0.22", fc=PAPER, ec=INK, lw=1.6))
    a.legend(frameon=False, fontsize=9.8, loc="upper center",
             bbox_to_anchor=(0.5, -0.145), ncol=1)
    _grid(a)
    a.set_title("They move in opposite directions. Always.", fontsize=12.0,
                fontweight="bold", color=INK, loc="left", pad=10)

    t.set_xlim(0, 1)
    t.set_ylim(0, 1)
    t.axis("off")
    t.text(0.0, 0.995, "TWO OPERATING POINTS", fontsize=12.5, fontweight="bold",
           color=ORANGE, va="top")
    for k, (lab, thr, (tn, fp, fn, tp), mm, note) in enumerate([
            ("A", T1, c1, m1,
             "Stop the line on a one-in-five suspicion. You miss\n"
             "almost nothing and most of your alarms are wrong.\n"
             "Right when a failure destroys the machine."),
            ("B", T2, c2, m2,
             "Only stop when the model is nearly sure. Almost every\n"
             "alarm is real, and failures get through. Right when\n"
             "stopping the line costs more than the repair.")]):
        yy = 0.900 - k * 0.445
        t.add_patch(FancyBboxPatch((0.0, yy - 0.400), 1.0, 0.390,
                                   boxstyle="round,pad=0.006,rounding_size=0.02",
                                   transform=t.transAxes, facecolor="#F5F8FB",
                                   edgecolor=INK, lw=1.8, clip_on=False))
        t.text(0.028, yy - 0.052, f"{lab} · threshold {thr:.2f}", fontsize=11.2,
               fontweight="bold", color=INK, va="center")
        # recall in orange and precision in teal, the same way round as the two
        # curves, so a colour never means two different things on one figure
        t.text(0.028, yy - 0.122, f"recall {mm[2]:.0%}", fontsize=10.0,
               fontweight="bold", color=ORANGE, va="center")
        t.text(0.235, yy - 0.122, f"·  precision {mm[1]:.0%}", fontsize=10.0,
               fontweight="bold", color=TEAL, va="center")
        t.text(0.028, yy - 0.185,
               f"caught {tp} of {tp + fn} failures, raised {tp + fp} alarms, "
               f"{fp} of them false", fontsize=8.8, color=INK, va="center")
        t.text(0.028, yy - 0.300, note, fontsize=8.8, color="#3A4C5C", va="center",
               linespacing=1.6)

    fig.text(0.008, 0.018,
             wrapped(AI4I + f" Both curves are swept over the same {len(te)} held-out "
                            f"machine-hours; every point is a fresh confusion matrix "
                            f"at that threshold. The model never changes — only the "
                            f"cut-off does."),
             fontsize=8.8, color=MUTED, style="italic", va="bottom", linespacing=1.6)
    fig.subplots_adjust(left=0.058, right=0.988, top=0.91, bottom=0.285, wspace=0.13)
    return save(fig, "threshold_tradeoff.png", pad=0.10)


# =========================================================== W9.6 imbalance trap
def fig_imbalance_trap():
    X, y = machine_sensors(n=300, seed=101, base=-13.0)
    n = len(y)
    npos = int(y.sum())
    # the model: predict "never fails", for every row
    tn, fp, fn, tp = conf_counts(y, np.zeros(n, int))
    acc, pre, rec, f1 = clf_metrics(tn, fp, fn, tp)

    fig, ax = canvas(12.70, 5.65, y0=0.28)
    ax.text(0.25, 5.82, "The most dangerous score in machine learning",
            fontsize=13.5, fontweight="bold", color=INK, va="center")

    # ---- 300 machine-hours as 300 dots.  25 x 12 so the block clears the key
    # line underneath it and the note beneath that.
    NC, NR, SP = 25, 12, 0.235
    GX, GY = 0.32, 4.58
    slots = set(np.linspace(2, n - 3, npos).astype(int).tolist())
    for i in range(n):
        r_, c_ = divmod(i, NC)
        bad = i in slots
        ax.add_patch(Ellipse((GX + c_ * SP + 0.12, GY - r_ * SP),
                             0.175 if bad else 0.135, 0.175 if bad else 0.135,
                             facecolor=ORANGE if bad else "#C9D4DE",
                             edgecolor=PAPER if bad else "none", lw=0.8, zorder=3))
    ax.text(GX, 5.02, f"{n} machine-hours  ·  {npos} of them ended in failure  "
                      f"({npos / n:.1%})", fontsize=11.0, fontweight="bold",
            color=INK, va="center")
    _keyline(ax, GX + 0.02, 1.28, ORANGE, f"{npos} failures", fs=9.6, sw=0.15)
    _keyline(ax, GX + 1.72, 1.28, "#C9D4DE", f"{n - npos} uneventful hours", fs=9.6,
             sw=0.15)

    # ---- the useless model and its confusion matrix
    MX = 6.55
    panel(ax, MX, 3.30, 6.10, 1.62, face=FADE, edge=ORANGE, lw=2.4, r=0.10)
    ax.text(MX + 0.28, 4.62, "THE MODEL", fontsize=10.0, fontweight="bold",
            color=ORANGE, va="center", zorder=3)
    code(ax, MX + 0.28, 4.24, 'def predict(row):', fs=11.0, z=3)
    code(ax, MX + 0.28, 3.94, '    return "no failure"', fs=11.0, color=ORANGE, z=3)
    ax.text(MX + 0.28, 3.56, "It has no features, no fit and no parameters.",
            fontsize=9.4, color="#3A4C5C", va="center", zorder=3)
    ax.text(MX + 4.30, 4.30, f"{acc:.1%}", ha="center", va="center", fontsize=30,
            fontweight="bold", color=ORANGE, zorder=3)
    ax.text(MX + 4.30, 3.74, "ACCURATE", ha="center", va="center", fontsize=11.0,
            fontweight="bold", color=ORANGE, zorder=3)

    cw, ch = 1.86, 0.82
    bx, by = MX + 0.50, 1.42
    labels = [("predicted fine\nactually failed", fn, ORANGE),
              ("predicted failure\nactually failed", tp, ORANGE),
              ("predicted fine\nactually fine", tn, TEAL),
              ("predicted failure\nactually fine", fp, TEAL)]
    for k2, (lab, cnt, col) in enumerate(labels):
        i2, j2 = divmod(k2, 2)
        x0 = bx + j2 * (cw + 0.10)
        y0_ = by + (1 - i2) * (ch + 0.10)
        panel(ax, x0, y0_, cw, ch, face=PAPER, edge=col, lw=1.8, r=0.06)
        ax.text(x0 + 0.18, y0_ + ch / 2, f"{cnt}", ha="left", va="center",
                fontsize=15, fontweight="bold", color=col, zorder=3)
        ax.text(x0 + cw - 0.14, y0_ + ch / 2, lab, ha="right", va="center",
                fontsize=7.6, color="#3A4C5C", linespacing=1.5, zorder=3)
    ax.text(bx + 2 * cw + 0.32, by + ch + 0.10 + ch / 2,
            "NOT ONE\nTRUE POSITIVE", fontsize=10.2, fontweight="bold",
            color=ORANGE, va="center", linespacing=1.5, zorder=3)
    ax.text(bx + 2 * cw + 0.32, by + ch / 2,
            f"recall {rec:.0%}\nprecision 0/0,\nundefined", fontsize=9.0,
            color=INK, va="center", linespacing=1.5, zorder=3)

    ax.text(0.25, 0.60, f"It has never once predicted a failure, and it is "
                        f"{acc:.1%} accurate. Accuracy is the wrong instrument "
                        f"whenever one class is rare.",
            fontsize=11.0, fontweight="bold", color=ORANGE, va="center")
    caption(ax, 0.25, 0.33, wrapped(AI4I + f" The real AI4I set fails in 3.39% of "
                                    f"rows; this draw came out at {npos / n:.2%}. "
                                    f"Quote recall, or the confusion matrix itself — "
                                    f"never accuracy alone.", 175), fs=9.0)
    return save_c(fig, "imbalance_trap.png")


# ===============================================================================
# WEEK 10 — CAN I TRUST THIS MODEL?
# ===============================================================================
AGE_ILLUS = ("Synthetic civil-engineering example: strength at the recorded curing age, illustrating the relationship in the "
             "UCI Concrete Compressive Strength dataset.")


def _complexity_curves(n=64, seed=17, test_frac=0.35, split_seed=11, dmax=14):
    age, y = curved_strength(n=n, seed=seed)
    tr, te = holdout(len(y), test_frac, seed=split_seed)
    degs = np.arange(1, dmax + 1)
    trn, tst = [], []
    for d in degs:
        p = polyfit(age[tr], y[tr], d)
        trn.append(reg_metrics(y[tr], p(age[tr]))[1])
        tst.append(reg_metrics(y[te], p(age[te]))[1])
    return age, y, tr, te, degs, np.array(trn), np.array(tst)


# ============================================================ W10.1 overfit curve
def fig_overfit_curve():
    age, y, tr, te, degs, trn, tst = _complexity_curves()
    best = int(degs[tst.argmin()])
    sweet = degs[tst <= 1.05 * tst.min()]
    s0, s1 = int(sweet.min()), int(sweet.max())
    assert np.all(np.diff(trn) <= 1e-9), "training error must fall monotonically"

    fig, ax = plt.subplots(figsize=(12.5, 5.4))
    bands = [(0.4, s0 - 0.5, "#E4EAF0", "UNDERFITTING",
              "too simple to hold the\nshape of the data — it is\nwrong on the rows it\n"
              "was trained on"),
             (s0 - 0.5, s1 + 0.5, "#DCEAE6", "THE SWEET SPOT",
              "as good on rows it has\nnever seen as it will get"),
             (s1 + 0.5, degs.max() + 0.6, FADE, "OVERFITTING",
              "it is learning this sample's\nnoise. Training error keeps\nfalling and the "
              "model keeps\ngetting worse")]
    for x0, x1, col, name, note in bands:
        ax.axvspan(x0, x1, color=col, zorder=0)
        ax.text((x0 + x1) / 2, 42.0, name, ha="center", va="center", fontsize=11.2,
                fontweight="bold", color=INK, zorder=5)
        ax.text((x0 + x1) / 2, 26.0, note, ha="center", va="top", fontsize=8.8,
                color="#3A4C5C", linespacing=1.6, zorder=5)

    ax.plot(degs, trn, color=STEEL2, lw=3.0, marker="o", ms=7, zorder=4,
            label="TRAINING error — on the rows it was fitted to")
    ax.plot(degs, tst, color=ORANGE, lw=3.0, marker="o", ms=7, zorder=4,
            label="VALIDATION error — held-out rows used to choose")
    ax.scatter([best], [tst.min()], s=260, marker="*", color=INK, zorder=6)
    ax.annotate(f"degree {best}\n{tst.min():.2f} MPa",
                xy=(best, tst.min()), xytext=(best + 1.5, 6.3), fontsize=9.8,
                fontweight="bold", color=INK, ha="left", va="center",
                linespacing=1.5, zorder=7,
                bbox=dict(boxstyle="round,pad=0.28", fc=PAPER, ec=INK, lw=1.3),
                arrowprops=dict(arrowstyle="->", color=INK, lw=1.7, shrinkA=4,
                                shrinkB=8, connectionstyle="arc3,rad=0.25"))
    ax.set_yscale("log")
    ax.set_xlim(0.4, degs.max() + 0.6)
    ax.set_ylim(2.6, 70.0)
    ax.set_xticks(degs)
    ax.set_yticks([3, 5, 10, 20, 50])
    ax.set_yticklabels(["3", "5", "10", "20", "50"])
    ax.set_xlabel("model complexity — degree of the fitted polynomial", fontsize=11)
    ax.set_ylabel("RMSE (MPa, log scale)", fontsize=11)
    ax.legend(frameon=False, fontsize=10.2, loc="upper center",
              bbox_to_anchor=(0.5, -0.145), ncol=2)
    ax.grid(axis="y", color="#FFFFFF", lw=1.2)
    ax.set_axisbelow(False)
    ax.set_title("Training error only ever falls. That is why it cannot be your judge.",
                 fontsize=13.0, fontweight="bold", color=INK, loc="left", pad=12)
    fig.text(0.008, 0.018,
             wrapped(AGE_ILLUS + f" Fitted on {len(tr)} rows and scored on the same "
                                 f"{len(te)} held-out rows at every degree. Both curves "
                                 f"are computed at draw time; the star is the smallest "
                                 f"validation RMSE. Final testing requires separate untouched rows."),
             fontsize=8.8, color=MUTED, style="italic", va="bottom", linespacing=1.6)
    fig.subplots_adjust(left=0.062, right=0.988, top=0.885, bottom=0.265)
    return save(fig, "overfit_curve.png", pad=0.10)


# ========================================================== W10.2 three fits
def fig_fit_three_panel():
    age, y, tr, te, degs, trn, tst = _complexity_curves()
    best = int(degs[tst.argmin()])
    picks = [(1, "TOO SIMPLE", STEEL2),
             (best, "ABOUT RIGHT", TEAL),
             (int(degs.max()), "FAR TOO FLEXIBLE", ORANGE)]
    g = np.linspace(age[tr].min(), age[tr].max(), 500)
    ylo, yhi = 14.0, 92.0

    fig, axes = plt.subplots(1, 3, figsize=(12.9, 5.3))
    for ax, (d, name, col) in zip(axes, picks):
        p = polyfit(age[tr], y[tr], d)
        rtr = reg_metrics(y[tr], p(age[tr]))[1]
        rte = reg_metrics(y[te], p(age[te]))[1]
        ax.plot(g, p(g), color=col, lw=3.0, zorder=3)
        ax.scatter(age[tr], y[tr], s=42, color=INK, zorder=4,
                   label=f"train ({len(tr)} rows) — the model saw these")
        ax.scatter(age[te], y[te], s=52, facecolor=PAPER, edgecolor=INK, lw=1.8,
                   zorder=5, label=f"validation ({len(te)} rows) — used to choose")
        ax.set_xlim(age.min() - 4, age.max() + 4)
        ax.set_ylim(ylo, yhi)
        ax.set_xlabel("Curing age (days)", fontsize=10.5)
        ax.set_title(f"{name}  ·  degree {d}", fontsize=11.8, fontweight="bold",
                     color=col, loc="left", pad=10)
        ax.text(0.035, 0.965,
                f"train RMSE  {rtr:.2f} MPa\nvalid RMSE  {rte:.2f} MPa",
                transform=ax.transAxes, fontsize=10.0, fontweight="bold",
                color=INK if d == best else (INK if d == 1 else ORANGE),
                va="top", ha="left", linespacing=1.7, zorder=6,
                bbox=dict(boxstyle="round,pad=0.30", fc=PAPER, ec=col, lw=1.4))
        _grid(ax)
    axes[0].set_ylabel("Strength at recorded curing age (MPa)", fontsize=10.5)
    axes[0].text(0.965, 0.045, "a straight line cannot bend,\nso it is wrong at "
                               "both ends",
                 transform=axes[0].transAxes, fontsize=8.8, color=INK2,
                 va="bottom", ha="right", linespacing=1.6, zorder=6)
    axes[2].text(0.965, 0.045, "it goes through the training points\nand dives off "
                               "the bottom of the\npanel between them",
                 transform=axes[2].transAxes, fontsize=8.8, color=ORANGE,
                 va="bottom", ha="right", linespacing=1.6, zorder=6)

    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, frameon=False, fontsize=10.0, loc="lower center",
               bbox_to_anchor=(0.5, 0.085), ncol=2)
    fig.text(0.008, 0.018,
             wrapped(AGE_ILLUS + " The same rows, the same split and the same "
                                 "least-squares machinery in all three panels — only "
                                 "the degree changes. Every RMSE is computed at draw "
                                 "time."),
             fontsize=8.8, color=MUTED, style="italic", va="bottom", linespacing=1.6)
    fig.subplots_adjust(left=0.055, right=0.988, top=0.90, bottom=0.235, wspace=0.16)
    return save(fig, "fit_three_panel.png", pad=0.10)


# =================================================================== W10.3 k-fold
def fig_kfold():
    x, y, _, _, unit = cohort_data("CML3112", n=50, seed=7)
    n = len(y)
    K = 5
    idx = np.random.default_rng(3).permutation(n)
    folds = np.array_split(idx, K)
    scores = []
    for f in folds:
        trf = np.setdiff1d(idx, f)
        p = polyfit(x[trf], y[trf], 1)
        scores.append(reg_metrics(y[f], p(x[f]))[0])
    scores = np.array(scores)
    # Summarise the ROUNDED fold scores, which are the numbers actually
    # printed on the slide, so anyone who checks the mean and spread by hand
    # reproduces the figure exactly. numpy's default (population) standard
    # deviation is used, which is what scores.std() prints in their notebook.
    shown = np.round(scores, 2)
    mean, sd = float(shown.mean()), float(shown.std())

    fig, ax = canvas(12.7, 5.50, y0=0.16)
    ax.text(0.25, 5.52, "Five fits, five scores, one honest number", fontsize=13.5,
            fontweight="bold", color=INK, va="center")
    ax.text(0.25, 5.19, f"{n} mixes cut into {K} equal folds of {len(folds[0])} rows. "
                        f"Every row is held out exactly once.",
            fontsize=9.8, color=MUTED, va="center")

    BX, BW, BG, BH = 1.70, 1.60, 0.09, 0.50
    rows_y = [4.36 - k * 0.66 for k in range(K)]
    for k, ry in enumerate(rows_y):
        ax.text(0.25, ry + BH / 2, f"round {k + 1}", ha="left", va="center",
                fontsize=10.4, fontweight="bold", color=INK)
        for j in range(K):
            held = (j == k)
            x0 = BX + j * (BW + BG)
            panel(ax, x0, ry, BW, BH, face=FADE if held else "#E4EAF0",
                  edge=ORANGE if held else MUTED, lw=2.2 if held else 1.2, r=0.06)
            ax.text(x0 + BW / 2, ry + BH / 2, "SCORE ON" if held else "train",
                    ha="center", va="center",
                    fontsize=9.2 if held else 9.0,
                    fontweight="bold" if held else "normal",
                    color=ORANGE if held else MUTED, zorder=3)
        ax.text(BX + K * (BW + BG) + 0.22, ry + BH / 2,
                f"MAE {scores[k]:.2f} {unit}", ha="left", va="center", fontsize=10.6,
                fontweight="bold", color=INK)

    for j in range(K):
        ax.text(BX + j * (BW + BG) + BW / 2, 4.98, f"fold {j + 1}", ha="center",
                va="center", fontsize=9.4, color=MUTED)

    panel(ax, 1.70, 1.02, 8.03, 0.62, face=FADE_T, edge=TEAL, lw=2.0, r=0.08)
    ax.text(1.92, 1.33, f"the cross-validated score:  {mean:.2f} ± {sd:.2f} {unit}",
            fontsize=12.0, fontweight="bold", color=TEAL, va="center", zorder=3)
    ax.text(10.05, 1.33, f"spread {scores.max() - scores.min():.2f} {unit}",
            fontsize=10.4, fontweight="bold", color=INK, va="center")

    ax.text(0.25, 0.66,
            f"One split would have handed you any single number between "
            f"{scores.min():.2f} and {scores.max():.2f} {unit}, at random. A single "
            f"split is itself a noisy measurement.",
            fontsize=10.6, fontweight="bold", color=INK, va="center")
    caption(ax, 0.25, 0.30,
            wrapped(f"{ILLUS} Each round is a complete refit of the straight line on "
                    f"{n - len(folds[0])} rows and a score on the {len(folds[0])} it "
                    f"never saw. Quote the mean AND the spread: a model whose folds "
                    f"disagree has not been measured.", 175), fs=9.0)
    return save_c(fig, "kfold.png")


# ============================================================ W10.4 leakage types
def fig_leakage_types():
    fig, ax = canvas(12.70, 5.90, y0=0.14)
    ax.text(0.25, 5.90, "Four ways the test set gets into the training set",
            fontsize=13.5, fontweight="bold", color=INK, va="center")
    ax.text(0.25, 5.58, "Every one of them makes the score go UP. That is what makes "
                        "them hard to notice.",
            fontsize=9.8, color=MUTED, va="center")

    PW, PH, PGX, PGY = 6.08, 2.16, 0.18, 0.18
    for i in range(4):
        c, r = i % 2, i // 2
        px = 0.25 + c * (PW + PGX)
        py = 3.14 - r * (PH + PGY)
        panel(ax, px, py, PW, PH, face="#F7FAFC", edge=ORANGE, lw=2.0, r=0.10)
        badge(ax, px + 0.36, py + PH - 0.34, i + 1, col=ORANGE, r=0.185, fs=10.5)

        if i == 0:
            ax.text(px + 0.66, py + PH - 0.34, "TRAIN-TEST CONTAMINATION",
                    fontsize=11.0, fontweight="bold", color=INK, va="center", zorder=3)
            ax.text(px + 0.34, py + PH - 0.72,
                    "You scaled, or filled gaps, or picked features, using the whole "
                    "file — then split it.",
                    fontsize=9.0, color="#3A4C5C", va="center", zorder=3)
            bx, bw, byy = px + 0.34, 5.20, py + 0.62
            panel(ax, bx, byy, bw * 0.78, 0.40, face="#DCE4EC", edge=INK, lw=1.2,
                  r=0.05, z=2)
            panel(ax, bx + bw * 0.78 + 0.06, byy, bw * 0.22 - 0.06, 0.40, face=FADE,
                  edge=ORANGE, lw=1.6, r=0.05, z=2)
            ax.text(bx + bw * 0.39, byy + 0.20, "train", ha="center", va="center",
                    fontsize=8.6, color=INK, zorder=3)
            ax.text(bx + bw * 0.89, byy + 0.20, "test", ha="center", va="center",
                    fontsize=8.6, color=ORANGE, fontweight="bold", zorder=3)
            ax.plot([bx, bx, bx + bw, bx + bw], [byy + 0.50, byy + 0.62,
                                                 byy + 0.62, byy + 0.50],
                    color=ORANGE, lw=1.8, zorder=3)
            ax.text(bx + bw / 2, py + 0.30,
                    "the mean and standard deviation were computed across ALL of this",
                    ha="center", va="center", fontsize=8.4, color=ORANGE,
                    fontweight="bold", zorder=3)

        elif i == 1:
            ax.text(px + 0.66, py + PH - 0.34, "TARGET LEAKAGE", fontsize=11.0,
                    fontweight="bold", color=INK, va="center", zorder=3)
            ax.text(px + 0.34, py + PH - 0.72,
                    "A column that only exists once the outcome is already known.",
                    fontsize=9.0, color="#3A4C5C", va="center", zorder=3)
            cols = [("torque", 1.24, INK), ("tool_wear", 1.36, INK),
                    ("repair_cost", 1.50, ORANGE), ("FAILED", 1.20, ORANGE)]
            cx = px + 0.42
            for nm, cwd, col in cols:
                head = col is ORANGE
                panel(ax, cx, py + 0.72, cwd, 0.38, face=FADE if head else "#DCE4EC",
                      edge=ORANGE if head else INK, lw=1.6 if head else 1.2, r=0.05,
                      z=2)
                ax.text(cx + cwd / 2, py + 0.91, nm, ha="center", va="center",
                        fontsize=8.4, family=MONO, color=col,
                        fontweight="bold" if head else "normal", zorder=3)
                cx += cwd + 0.06
            ax.text(px + 0.34, py + 0.34,
                    "Nothing has a repair cost until it has already broken.",
                    fontsize=8.4, color=ORANGE, fontweight="bold", va="center",
                    zorder=3)

        elif i == 2:
            ax.text(px + 0.66, py + PH - 0.34, "TEMPORAL LEAKAGE", fontsize=11.0,
                    fontweight="bold", color=INK, va="center", zorder=3)
            ax.text(px + 0.34, py + PH - 0.72,
                    "A random split puts next month in the training set and last month "
                    "in the test set.",
                    fontsize=9.0, color="#3A4C5C", va="center", zorder=3)
            tx, tw, tyy = px + 0.40, 5.10, py + 0.74
            arrow(ax, (tx, tyy), (tx + tw, tyy), col=MUTED, lw=1.6, ms=14)
            for frac, lab, col in ((0.16, "TEST\nJan", ORANGE),
                                   (0.50, "TRAIN\nJun", INK),
                                   (0.84, "TRAIN\nDec", INK)):
                ax.add_patch(Ellipse((tx + frac * tw, tyy), 0.16, 0.16,
                                     facecolor=col, zorder=4))
                ax.text(tx + frac * tw, tyy + 0.34, lab, ha="center", va="center",
                        fontsize=8.2, color=col, fontweight="bold", linespacing=1.4,
                        zorder=3)
            ax.text(px + 0.34, py + 0.32,
                    "You used December to predict January. In service you will not "
                    "have December.",
                    fontsize=8.4, color=ORANGE, fontweight="bold", va="center",
                    zorder=3)

        else:
            ax.text(px + 0.66, py + PH - 0.34, "GROUP LEAKAGE", fontsize=11.0,
                    fontweight="bold", color=INK, va="center", zorder=3)
            ax.text(px + 0.34, py + PH - 0.72,
                    "The same machine, batch or specimen has rows on both sides of the "
                    "split.",
                    fontsize=9.0, color="#3A4C5C", va="center", zorder=3)
            for side, sx, lab, col in ((0, px + 0.42, "TRAIN", INK),
                                       (1, px + 3.20, "TEST", ORANGE)):
                panel(ax, sx, py + 0.60, 2.50, 0.62, face="#DCE4EC" if not side
                      else FADE, edge=col, lw=1.6, r=0.05, z=2)
                ax.text(sx + 0.14, py + 1.05, lab, ha="left", va="center",
                        fontsize=8.4, fontweight="bold", color=col, zorder=3)
                for j, nm in enumerate(("UNIT_07", "UNIT_12") if not side
                                       else ("UNIT_07", "UNIT_21")):
                    hot = nm == "UNIT_07"
                    ax.text(sx + 0.14 + j * 1.20, py + 0.78, nm, ha="left",
                            va="center", fontsize=8.2, family=MONO,
                            color=ORANGE if hot else MUTED,
                            fontweight="bold" if hot else "normal", zorder=3)
            ax.text(px + 0.34, py + 0.26,
                    "UNIT_07 is in both. The model recognises the machine instead of "
                    "learning the physics.",
                    fontsize=8.4, color=ORANGE, fontweight="bold", va="center",
                    zorder=3)

    caption(ax, 0.25, 0.42,
            "Target and temporal leakage are caught by one question: at the moment I "
            "would really have to make this prediction, would I have had this number? "
            "Contamination and group leakage survive that question, because you do have "
            "every number. Those two are caught by checking how the rows were split.",
            fs=10.0, col=INK, italic=False)
    return save_c(fig, "leakage_types.png")


# ============================================================ W10.5 leakage score
def fig_leakage_score():
    X, y, g = replicate_batches()
    n, K = len(y), 3
    ub = np.unique(g)
    # (a) the leaking split: shuffle ROWS, so a batch's replicates land on both sides
    tr, te = holdout(n, 0.25, seed=9)
    leak = reg_metrics(y[te], knn1_predict(X[tr], y[tr], X[te]))
    # (b) the honest split: shuffle BATCHES, so a batch is wholly in or wholly out
    pb = np.random.default_rng(9).permutation(ub)
    held = set(pb[:int(round(len(ub) * 0.25))].tolist())
    mask = np.array([gi in held for gi in g])
    hon = reg_metrics(y[mask], knn1_predict(X[~mask], y[~mask], X[mask]))

    fig, ax = plt.subplots(figsize=(12.2, 5.0))
    labs = ["THE HONEST SCORE\nsplit by batch — a batch is wholly in, or wholly out",
            "THE SCORE YOU WOULD HAVE REPORTED\nsplit by row — the same batch lands on "
            "both sides"]
    vals = [hon[2], leak[2]]
    cols = [TEAL, ORANGE]
    ax.barh([0, 1], vals, color=cols, height=0.50, zorder=3)
    for i, v in enumerate(vals):
        ax.text(v + 0.012, i, f"R² = {v:.3f}", va="center", ha="left", fontsize=14,
                fontweight="bold", color=cols[i], zorder=4)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(labs, fontsize=10.2, linespacing=1.5)
    ax.set_xlim(0, 1.14)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xlabel("R² on the held-out rows — same data, same model, only the split "
                  "changed", fontsize=11)
    ax.set_ylim(-0.62, 1.74)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    _grid(ax, axis="x")
    ax.annotate("", xy=(hon[2], 1.44), xytext=(leak[2], 1.44),
                arrowprops=dict(arrowstyle="<->", color=INK, lw=2.2))
    ax.text((hon[2] + leak[2]) / 2, 1.60,
            f"{leak[2] - hon[2]:.3f} of pure illusion", ha="center", va="center",
            fontsize=11.5, fontweight="bold", color=INK)
    for v in vals:
        ax.plot([v, v], [1.32, 1.44], color=INK, lw=1.2, ls=(0, (2, 2)), zorder=2)
    ax.set_title("A very good score is a reason for suspicion",
                 fontsize=13.5, fontweight="bold", color=INK, loc="left", pad=14)

    fig.text(0.008, 0.135,
             f"Nothing about the model changed. It is the same 1-nearest-neighbour "
             f"regressor on the same {n} rows. Only the way the rows were divided "
             f"changed.",
             fontsize=10.2, color=INK, va="bottom")
    fig.text(0.008, 0.018,
             wrapped(f"Illustrative data: {len(ub)} concrete batches, each tested three "
                     f"times, so every batch has three nearly identical rows "
                     f"({n} rows in total). Under the row split, most test rows have "
                     f"one of their own replicates sitting in the training set, so the "
                     f"model looks the answer up instead of predicting it. Both "
                     f"numbers are computed at draw time."),
             fontsize=8.8, color=MUTED, style="italic", va="bottom", linespacing=1.6)
    fig.subplots_adjust(left=0.335, right=0.985, top=0.855, bottom=0.295)
    return save(fig, "leakage_score.png", pad=0.10)


# ===============================================================================
# WEEK 11 — FEATURES
# ===============================================================================
def fig_onehot():
    import pandas as pd
    df = pd.DataFrame({"machine_id": ["UNIT_07", "UNIT_12", "UNIT_21", "UNIT_07"],
                       "type": ["L", "H", "M", "H"],
                       "torque_nm": [42.1, 39.4, 44.8, 41.0]})
    wide = pd.get_dummies(df, columns=["type"], prefix="type", dtype=int)
    order = ["machine_id", "type_L", "type_M", "type_H", "torque_nm"]
    wide = wide[order]

    fig, ax = canvas(12.70, 5.05, y0=0.20)
    ax.text(0.25, 5.10, "A model does arithmetic. It cannot do arithmetic on the "
                        "letter H.",
            fontsize=13.5, fontweight="bold", color=INK, va="center")

    rowh = 0.40
    heads_b = ["machine_id", "type", "torque_nm"]
    rows_b = [[r.machine_id, r.type, f"{r.torque_nm:.1f}"]
              for r in df.itertuples()]
    _table(ax, 0.25, 4.42, [1.62, 1.00, 1.34], rowh, heads_b, rows_b, head_fs=8.6,
           cell_fs=9.4,
           head_col=lambda j: ORANGE if j == 1 else INK,
           cell_col=lambda i, j, v: (FADE, ORANGE, True) if j == 1 else None)
    ax.text(0.25, 4.62, "BEFORE", fontsize=10.6, fontweight="bold", color=INK,
            va="center")

    arrow(ax, (4.62, 3.30), (5.48, 3.30), col=TEAL, lw=2.4, ms=20)
    code(ax, 5.05, 3.66, "pd.get_dummies", fs=9.4, color=TEAL, ha="center")

    heads_a = ["machine_id", "type_L", "type_M", "type_H", "torque_nm"]
    rows_a = [[r.machine_id, r.type_L, r.type_M, r.type_H, f"{r.torque_nm:.1f}"]
              for r in wide.itertuples()]
    _table(ax, 5.62, 4.42, [1.62, 0.94, 0.94, 0.94, 1.34], rowh, heads_a, rows_a,
           head_fs=8.6, cell_fs=9.4,
           head_col=lambda j: ORANGE if j in (1, 2, 3) else INK,
           cell_col=lambda i, j, v: ((FADE, ORANGE, True) if (j in (1, 2, 3) and v == 1)
                                     else (PAPER, "#9AA9B6", False) if j in (1, 2, 3)
                                     else None))
    ax.text(5.62, 4.62, "AFTER", fontsize=10.6, fontweight="bold", color=ORANGE,
            va="center")
    ax.text(5.62 + (0.94 * 3) / 2 + 1.62, 4.92,
            "one column per value · exactly one 1 in every row", ha="center",
            va="center", fontsize=9.0, color=ORANGE, fontweight="bold")

    ax.text(0.25, 2.14, "Why not just write L = 1, M = 2, H = 3 ?", fontsize=11.5,
            fontweight="bold", color=INK, va="center")
    ax.text(0.25, 1.78,
            "Because a straight-line model would then be forced to believe that H is "
            "three times L, that M sits exactly halfway between them, and that\n"
            "H − M equals M − L. None of that is true of a product grade. The "
            "indicator columns say only “this row is H, and is not L or M”.",
            fontsize=9.8, color=INK, va="top", linespacing=1.65)
    ax.text(0.25, 1.06,
            "Where an order really does exist — L, M, H tool grades by hardness, or "
            "sieve sizes — a single ordered number is the better feature. Ask whether\n"
            "the spacing between the levels means anything before you choose.",
            fontsize=9.8, color=INK, va="top", linespacing=1.65)
    caption(ax, 0.25, 0.46,
            wrapped("Illustrative rows in the shape of the AI4I 2020 dataset, whose "
                    "product type really is L / M / H. The AFTER table is what "
                    "pd.get_dummies(df, columns=[\"type\"]) actually returns for the "
                    "BEFORE table — it is not typed out.", 175), fs=9.0)
    return save_c(fig, "onehot.png")


def fig_scaling_effect():
    rng = np.random.default_rng(19)
    n = 60
    torque = rng.uniform(20, 70, n)
    speed = rng.uniform(1200, 2900, n)
    X = np.column_stack([speed, torque])
    mu, sd = X.mean(0), X.std(0)
    Z = (X - mu) / sd

    # find a machine-hour whose nearest neighbour CHANGES when the columns are
    # put on a common scale -- the whole reason scale matters to a distance
    def nn(A, i):
        d = ((A - A[i]) ** 2).sum(1)
        d[i] = np.inf
        return int(d.argmin())

    # Of every point whose neighbour flips, take the one whose two candidates are
    # furthest apart in BOTH panels, so the A and B labels cannot collide.
    span = X.max(0) - X.min(0)
    q = a = b = None
    best_gap = -1.0
    for i in range(n):
        ra, rb = nn(X, i), nn(Z, i)
        if ra == rb:
            continue
        gap = min(float(np.hypot(*((X[ra] - X[rb]) / span))),
                  float(np.hypot(*(Z[ra] - Z[rb])) / 6.4))
        if gap > best_gap:
            best_gap, q, a, b = gap, i, ra, rb

    # Both axes of a panel carry the SAME numeric range, which is the point:
    # that is the only range a Euclidean distance knows about. Equal aspect is
    # deliberately not used — two square panels cannot fill a landscape frame,
    # and set_aspect fights bbox_inches="tight". The claim is carried by the
    # matching limits and by the computed distances, not by the box shape.
    fig, (p1, p2) = plt.subplots(1, 2, figsize=(12.6, 5.5))
    for ax, A, lim, xl, yl, ttl, col in (
            (p1, X, (0, 3050), "Rotational speed (rpm)", "Shaft torque (N·m)",
             "RAW — both axes run 0 to 3050, the only range a distance knows", INK),
            (p2, Z, (-3.2, 3.2), "Rotational speed (standard deviations)",
             "Shaft torque (standard deviations)",
             "AFTER STANDARDISATION — both axes run −3.2 to 3.2", TEAL)):
        ax.scatter(A[:, 0], A[:, 1], s=46, color="#8FA6BC", zorder=3)
        if ax is p2:
            # Only the standardised panel is marked here. On the raw shared scale
            # the three markers land inside a sliver a few units thick and cannot
            # be told apart, so that panel gets a magnified inset instead.
            ax.scatter([A[q, 0]], [A[q, 1]], s=230, marker="*", color=ORANGE,
                       zorder=6)
            off = 0.055 * (lim[1] - lim[0])
            for k, lab in ((a, "A"), (b, "B")):
                ax.scatter([A[k, 0]], [A[k, 1]], s=100, facecolor=PAPER,
                           edgecolor=INK, lw=2.0, zorder=6)
                ax.text(A[k, 0] + off, A[k, 1] + off, lab, ha="left", va="bottom",
                        fontsize=10.5, fontweight="bold", color=INK, zorder=7)
        ax.set_xlim(*lim)
        ax.set_ylim(*lim)
        ax.set_xlabel(xl, fontsize=10.2)
        ax.set_ylabel(yl, fontsize=10.2)
        ax.set_title(ttl, fontsize=10.8, fontweight="bold", color=col, loc="left",
                     pad=10)
        _grid(ax, axis="both")

    d_raw = lambda k: float(np.hypot(*(X[k] - X[q])))
    d_std = lambda k: float(np.hypot(*(Z[k] - Z[q])))
    # Both notes are kept to a couple of lines and sit in the band above the
    # cloud. A standardised uniform column only reaches about +/-1.73, so
    # anything above y = 2 in the right-hand panel is guaranteed empty.
    p1.text(0.045, 0.955,
            f"torque spans {torque.max() - torque.min():.0f} units, speed spans "
            f"{speed.max() - speed.min():.0f}. On one\nnumeric scale the torque "
            f"column is a flat line, and\nthe distance formula never hears it.",
            transform=p1.transAxes, fontsize=9.0, color=INK, va="top", ha="left",
            linespacing=1.6, zorder=7,
            bbox=dict(boxstyle="round,pad=0.30", fc=PAPER, ec=INK, lw=1.3))
    p2.text(0.045, 0.955,
            "Each column minus its own mean, divided by its\nown standard deviation. "
            "Now both get a vote.",
            transform=p2.transAxes, fontsize=9.0, color=TEAL, va="top", ha="left",
            linespacing=1.6, zorder=7,
            bbox=dict(boxstyle="round,pad=0.30", fc=PAPER, ec=TEAL, lw=1.3))

    # On the raw shared scale every point lands inside a sliver a few units
    # thick, so ★, A and B are unreadable there. Magnify that sliver into the
    # empty upper half of the panel rather than pretend the labels fit.
    INS_H = 0.30
    ins = p1.inset_axes([0.10, 0.30, 0.84, INS_H], transform=p1.transAxes)
    ins.scatter(X[:, 0], X[:, 1], s=34, color="#8FA6BC", zorder=3)
    ins.scatter([X[q, 0]], [X[q, 1]], s=200, marker="*", color=ORANGE, zorder=6)
    for k, lab in ((a, "A"), (b, "B")):
        ins.scatter([X[k, 0]], [X[k, 1]], s=90, facecolor=PAPER, edgecolor=INK,
                    lw=1.8, zorder=6)
        ins.text(X[k, 0], X[k, 1] + 3.2, lab, ha="center", va="bottom", fontsize=10.0,
                 fontweight="bold", color=INK, zorder=7)
    ins.set_xlim(0, 3050)
    ins_lo, ins_hi = torque.min() - 6, torque.max() + 14
    ins.set_ylim(ins_lo, ins_hi)
    # the magnification is worked out, not guessed: units per inch on the main
    # panel divided by units per inch inside the inset
    mag = (3050.0 / 1.0) / ((ins_hi - ins_lo) / INS_H)
    ins.set_yticks([int(torque.min()), int(torque.max())])
    ins.set_xticks([])
    ins.tick_params(labelsize=8.2)
    for sp in ins.spines.values():
        sp.set_color(MUTED)
    ins.set_facecolor("#FBFCFD")
    p1.text(0.10, 0.615,
            f"the same points, with the torque axis magnified {mag:.0f}× so ★, A and "
            f"B can be told apart",
            transform=p1.transAxes, fontsize=8.6, color=MUTED, style="italic",
            va="bottom", ha="left", zorder=7)

    fig.text(0.008, 0.200,
             f"The ★ machine-hour's nearest neighbour is A before scaling "
             f"({d_raw(a):.0f} away against B's {d_raw(b):.0f}) and B after scaling "
             f"({d_std(b):.2f} against A's {d_std(a):.2f}). Only the units changed.",
             fontsize=10.2, color=INK, va="bottom")
    fig.text(0.008, 0.135,
             "CARES ABOUT SCALE: k-nearest neighbours · k-means · SVM · PCA · neural "
             "networks · any regression with a ridge or lasso penalty.",
             fontsize=9.4, color=ORANGE, fontweight="bold", va="bottom")
    fig.text(0.008, 0.018,
             wrapped("DOES NOT: decision trees, random forests, gradient boosting — a "
                     "tree splits one column at a time, and “torque ≤ 47” means the "
                     "same thing whatever the other columns do. Illustrative data in "
                     "the shape of the AI4I 2020 dataset."),
             fontsize=8.8, color=MUTED, style="italic", va="bottom", linespacing=1.6)
    fig.subplots_adjust(left=0.058, right=0.988, top=0.92, bottom=0.345, wspace=0.22)
    return save(fig, "scaling_effect.png", pad=0.10)


def fig_ablation():
    X, y, names = concrete_table(300, seed=23)
    tr, te = holdout(len(y), 0.25, seed=5)
    base = reg_metrics(y[te], ols_pred(ols(X[tr], y[tr]), X[te]))[0]
    out = []
    for j, nm in enumerate(names):
        keep = [c for c in range(X.shape[1]) if c != j]
        mae = reg_metrics(y[te], ols_pred(ols(X[tr][:, keep], y[tr]),
                                          X[te][:, keep]))[0]
        out.append((nm, mae, mae - base))
    out.sort(key=lambda r: r[1])
    matters = 0.10 * base
    worst = max(out, key=lambda r: r[2])
    dead = [r for r in out if r[2] < 0.02 * base]

    fig, ax = plt.subplots(figsize=(12.4, 5.3))
    yp = np.arange(len(out))
    vals = [r[1] for r in out]
    cols = [ORANGE if r[2] >= matters else GREY for r in out]
    ax.barh(yp, vals, color=cols, height=0.56, zorder=3)
    # every value label starts at the same x, past the longest bar, so none of
    # them lands on the dashed reference line
    lab_x = max(vals) * 1.045
    for i, (nm, mae, dl) in enumerate(out):
        ax.text(lab_x, i, f"{mae:.2f}   ({dl:+.2f})", va="center",
                ha="left", fontsize=10.4, fontweight="bold", color=cols[i], zorder=4)
    ax.set_yticks(yp)
    ax.set_yticklabels([f"drop  {r[0]}" for r in out], fontsize=10.8)
    ax.set_xlim(0, max(vals) * 1.34)
    ax.set_xlabel("Test MAE with that column removed (MPa) — and the change against "
                  "the full model", fontsize=11)
    ax.set_ylim(-0.62, len(out) + 0.42)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    _grid(ax, axis="x")

    ax.axvline(base, color=INK, lw=2.4, ls=(0, (5, 3)), zorder=5)
    ax.text(base, len(out) - 0.34, f"all five columns\n{base:.2f} MPa", ha="center",
            va="bottom", fontsize=10.0, fontweight="bold", color=INK, zorder=6,
            linespacing=1.45,
            bbox=dict(boxstyle="round,pad=0.24", fc=PAPER, ec=INK, lw=1.3))

    ax.set_title("Take one column away at a time and watch what happens",
                 fontsize=13.5, fontweight="bold", color=INK, loc="left", pad=14)
    fig.text(0.008, 0.145,
             f"Losing {worst[0]} costs {worst[2]:+.2f} MPa — that column is carrying "
             f"the model. Dropping "
             f"{', '.join(r[0] for r in dead)} changes nothing measurable.",
             fontsize=10.2, color=INK, va="bottom")
    fig.text(0.008, 0.018,
             wrapped(f"{ILLUS} One multiple linear regression by normal equations per "
                     f"bar, all fitted on the same {len(tr)} training rows and scored "
                     f"on the same {len(te)} test rows. Batch number is an identifier, "
                     f"not a measurement, and it never could have helped. Water and "
                     f"cement look useless only because the water/cement ratio already "
                     f"carries both — a column can be essential and still be "
                     f"droppable."),
             fontsize=8.8, color=MUTED, style="italic", va="bottom", linespacing=1.6)
    fig.subplots_adjust(left=0.215, right=0.985, top=0.865, bottom=0.315)
    return save(fig, "ablation.png", pad=0.10)


DOM_SRC = {"CML3112": "the UCI Concrete Compressive Strength dataset",
           "CML3113": "the froth flotation process dataset (Kaggle)",
           "CML3111": "the AI4I 2020 Predictive Maintenance dataset"}
# (headline for the figure, the rest for the caption). Kept as two strings rather
# than one string split on ". " at draw time, which silently ate a full stop.
DOM_WHY = {
    "CML3112": ("Abrams' law: strength is governed by the water per unit of cement, "
                "not by the cement on its own.",
                "Two mixes with 380 kg/m³ of cement behave nothing alike if one of "
                "them is soaking wet."),
    "CML3113": ("What a reagent does depends on how much ore it has to coat.",
                "600 g/min into a heavy feed is a weak dose; the same flow into a "
                "light feed is a strong one. Divide by the feed rate and the two "
                "become comparable."),
    "CML3111": ("Heating follows mechanical power, and power is torque times angular "
                "velocity.",
                "The same 45 N·m at 1,300 rpm and at 2,800 rpm are two completely "
                "different duties for the motor."),
}


def fig_domain_feature(code):
    raw, eng, y, rl, el, yl, _ = domain_pair(code)

    def fit(f):
        p = polyfit(f, y, 1)
        return p, reg_metrics(y, p(f))[2]

    p_raw, r2_raw = fit(raw)
    p_eng, r2_eng = fit(eng)

    fig, (a, b) = plt.subplots(1, 2, figsize=(12.8, 5.75))
    for ax, f, p, r2, xl, ttl, col in (
            (a, raw, p_raw, r2_raw, rl, "THE COLUMN THAT CAME IN THE FILE", STEEL2),
            (b, eng, p_eng, r2_eng, el, "THE COLUMN YOU BUILD FROM THE PHYSICS",
             ORANGE)):
        g = np.linspace(f.min(), f.max(), 80)
        ax.scatter(f, y, s=50, color=INK, alpha=0.75, zorder=3)
        ax.plot(g, p(g), color=col, lw=3.0, zorder=4)
        ax.set_xlabel(xl, fontsize=11)
        ax.set_ylabel(yl, fontsize=11)
        ax.set_title(ttl, fontsize=11.5, fontweight="bold", color=col, loc="left",
                     pad=10)
        yr = y.max() - y.min()
        ax.set_ylim(y.min() - 0.10 * yr, y.max() + 0.24 * yr)
        ax.text(0.5, 0.965, f"R² = {r2:.3f}", transform=ax.transAxes, fontsize=15,
                fontweight="bold", color=col, ha="center", va="top", zorder=6,
                bbox=dict(boxstyle="round,pad=0.30", fc=PAPER, ec=col, lw=1.6))
        _grid(ax)

    gain = r2_eng - r2_raw
    fig.text(0.008, 0.225,
             f"Same {len(y)} rows, same target, same straight-line fit. One engineered "
             f"column raises R² from {r2_raw:.3f} to {r2_eng:.3f} — "
             f"{gain:+.3f}, and no new measurements were taken.",
             fontsize=10.4, color=INK, va="bottom")
    head, detail = DOM_WHY[code]
    fig.text(0.008, 0.155, head, fontsize=9.6, color=ORANGE, fontweight="bold",
             va="bottom")
    fig.text(0.008, 0.018,
             wrapped(f"Illustrative data shaped like {DOM_SRC[code]}, built so the "
                     f"engineered column really is the stronger predictor — the target "
                     f"is driven by it, and the raw column only inherits part of the "
                     f"signal because the other quantity in the expression varies too. "
                     f"Both R² values are computed at draw time. " + detail),
             fontsize=8.8, color=MUTED, style="italic", va="bottom", linespacing=1.6)
    fig.subplots_adjust(left=0.062, right=0.988, top=0.915, bottom=0.375, wspace=0.20)
    return save(fig, f"domain_feature_{code}.png", pad=0.10)


# ===============================================================================
# WEEK 12 — COMPARISON AND JUDGEMENT
# ===============================================================================
def fig_comparison_protocol():
    fig, ax = canvas(12.70, 5.60, y0=0.18)
    ax.text(0.25, 5.62, "Change one thing. Hold everything else still.",
            fontsize=13.5, fontweight="bold", color=INK, va="center")
    ax.text(0.25, 5.30, "This is the whole of fair model comparison, and it is the "
                        "part people skip.",
            fontsize=9.8, color=MUTED, va="center")

    fixed = [("the same split", "identical train and test rows, from one\n"
                                "shuffle with one fixed random seed"),
             ("the same preprocessing", "scaling and gap-filling fitted INSIDE\n"
                                        "each fold, never before the split"),
             ("the same metric", "one number, chosen before you looked\n"
                                 "at any result"),
             ("the same folds", "the same 5 folds in the same order for\n"
                                "every candidate")]
    FX, FW = 0.25, 4.55
    panel(ax, FX, 1.02, FW, 3.90, face=FADE_T, edge=TEAL, lw=2.2, r=0.10)
    ax.text(FX + 0.28, 4.66, "HELD CONSTANT", fontsize=11.8, fontweight="bold",
            color=TEAL, va="center", zorder=3)
    yy = 4.14
    for name, note in fixed:
        ax.text(FX + 0.30, yy, "✓", fontsize=13, fontweight="bold", color=TEAL,
                va="center", ha="center", zorder=3)
        ax.text(FX + 0.58, yy, name, fontsize=10.6, fontweight="bold", color=INK,
                va="center", zorder=3)
        ax.text(FX + 0.58, yy - 0.36, note, fontsize=8.8, color="#3A4C5C",
                va="center", linespacing=1.55, zorder=3)
        yy -= 0.86

    arrow(ax, (FX + FW + 0.10, 2.96), (FX + FW + 0.72, 2.96), col=MUTED, lw=2.2,
          ms=18)

    VX, VW = 5.62, 6.93
    panel(ax, VX, 1.02, VW, 3.90, face="#F7FAFC", edge=ORANGE, lw=2.2, r=0.10)
    ax.text(VX + 0.28, 4.66, "THE ONE THING THAT VARIES", fontsize=11.8,
            fontweight="bold", color=ORANGE, va="center", zorder=3)
    runs = [("RUN 1", "LinearRegression()", "MAE 3.58 MPa"),
            ("RUN 2", "DecisionTreeRegressor(max_depth=8)", "MAE 4.28 MPa"),
            ("RUN 3", "RandomForestRegressor(n_estimators=300)", "MAE 2.91 MPa")]
    yy = 4.06
    for tag, mdl, _score in runs:
        ax.text(VX + 0.32, yy, tag, fontsize=9.6, fontweight="bold", color=MUTED,
                va="center", zorder=3)
        panel(ax, VX + 1.10, yy - 0.26, 5.55, 0.52, face=FADE, edge=ORANGE, lw=1.6,
              r=0.06, z=2)
        code(ax, VX + 1.26, yy, mdl, fs=9.6, color=ORANGE, z=3)
        yy -= 0.86
    ax.text(VX + 0.32, 1.48,
            "Everything to the left of this box is byte-for-byte identical across the\n"
            "three runs. That is what makes the three numbers comparable at all.",
            fontsize=9.2, color=INK, va="center", linespacing=1.6, zorder=3)

    ax.text(0.25, 0.66,
            "Change the model AND the split and you have learned nothing about either. "
            "You cannot tell which change moved the number.",
            fontsize=10.6, fontweight="bold", color=INK, va="center")
    caption(ax, 0.25, 0.36,
            wrapped("The class names above are scikit-learn's, and the point of a "
                    "Pipeline is exactly this: it makes “fitted inside the fold” the "
                    "default instead of something you have to remember.", 175), fs=9.0)
    return save_c(fig, "comparison_protocol.png")


def fig_gridsearch():
    X, y, names = concrete_table(300, seed=23)
    Xr = X[:, :3]
    K = 5
    idx = np.random.default_rng(5).permutation(len(y))
    folds = np.array_split(idx, K)
    depths = (2, 3, 4, 5, 6, 8, 10)
    leaves = (1, 4, 16, 50)
    G = np.zeros((len(depths), len(leaves)))
    for i, d in enumerate(depths):
        for j, ml in enumerate(leaves):
            s = []
            for f in folds:
                trf = np.setdiff1d(idx, f)
                t = grow_tree(Xr[trf], y[trf], d, ml, kind="sse")
                s.append(reg_metrics(y[f], tree_predict(t, Xr[f], "value"))[0])
            G[i, j] = np.mean(s)
    bi, bj = np.unravel_index(int(G.argmin()), G.shape)

    fig, ax = canvas(12.7, 5.55, y0=0.16)
    ax.text(0.25, 5.56, "A grid search is a table you fill in, then read",
            fontsize=13.5, fontweight="bold", color=INK, va="center")
    ax.text(0.25, 5.23, f"{len(depths)} depths × {len(leaves)} leaf sizes × {K} folds "
                        f"= {len(depths) * len(leaves) * K} trees fitted to produce "
                        f"this one table.",
            fontsize=9.8, color=MUTED, va="center")

    CW, CH, GX, GY = 1.16, 0.44, 2.05, 4.34
    lo, hi = float(G.min()), float(G.max())
    for j, ml in enumerate(leaves):
        ax.text(GX + j * CW + CW / 2, GY + 0.44, f"{ml}", ha="center", va="center",
                fontsize=10.6, fontweight="bold", color=INK)
    ax.text(GX - 0.16, GY + 0.44, "min_samples_leaf", ha="right", va="center",
            fontsize=10.4, fontweight="bold", color=INK)
    ax.text(GX - 0.52, GY - len(depths) * CH / 2, "max_depth", ha="center",
            va="center", fontsize=10.4, fontweight="bold", color=INK, rotation=90)
    for i, d in enumerate(depths):
        cy = GY - (i + 1) * CH
        ax.text(GX - 0.16, cy + CH / 2, f"{d}", ha="right", va="center",
                fontsize=10.6, fontweight="bold", color=INK)
        for j in range(len(leaves)):
            v = G[i, j]
            t_ = (v - lo) / (hi - lo)
            shade = 0.10 + 0.72 * (1.0 - t_)        # darker = better
            face = (1 - 0.62 * shade, 1 - 0.50 * shade, 1 - 0.34 * shade)
            best = (i, j) == (bi, bj)
            ax.add_patch(Rectangle((GX + j * CW, cy), CW, CH,
                                   facecolor=FADE if best else face,
                                   edgecolor=PAPER, lw=1.4, zorder=2))
            if best:
                ax.add_patch(FancyBboxPatch((GX + j * CW + 0.02, cy + 0.02),
                                            CW - 0.04, CH - 0.04,
                                            boxstyle="round,pad=0,rounding_size=0.04",
                                            facecolor="none", edgecolor=ORANGE,
                                            lw=3.0, zorder=5))
            ax.text(GX + j * CW + CW / 2, cy + CH / 2, f"{v:.2f}", ha="center",
                    va="center", fontsize=10.0,
                    fontweight="bold" if best or shade > 0.55 else "normal",
                    color=ORANGE if best else (PAPER if shade > 0.55 else INK),
                    zorder=6)

    # No leader line to the best cell: any arrow reaching it from the right has
    # to cross three other cells and reads as a strikethrough. The orange ring
    # is the identification.
    NX = GX + len(leaves) * CW + 0.70
    ax.text(NX, GY - 0.28,
            f"THE RINGED CELL\nmax_depth {depths[bi]}, min_samples_leaf {leaves[bj]}\n"
            f"cross-validated MAE {G[bi, bj]:.2f} MPa",
            fontsize=10.4, fontweight="bold", color=ORANGE, va="top", ha="left",
            linespacing=1.6, zorder=6,
            bbox=dict(boxstyle="round,pad=0.30", fc=PAPER, ec=ORANGE, lw=1.5))
    ax.text(NX, GY - 1.36,
            "Every cell is the mean of the same 5 folds.\n"
            "Darker is lower error. Read the shape, not\n"
            "just the winner: depth is doing nearly all\n"
            "the work here, and a leaf size of 16 or 50\n"
            "cripples the tree whatever the depth.",
            fontsize=9.2, color=INK, va="top", ha="left", linespacing=1.65)

    ax.text(0.25, 0.86,
            "The search happens INSIDE cross-validation. The test set takes no part in "
            "choosing this cell — otherwise the winner is chosen by\nthe very rows you "
            "were going to use to check it, and the score you report is the score of a "
            "lucky guess.",
            fontsize=10.4, fontweight="bold", color=INK, va="center", linespacing=1.7)
    caption(ax, 0.25, 0.30,
            wrapped(f"{ILLUS} Regression trees on cement, water and age, grown by "
                    f"exhaustive threshold search on the sum of squared errors.", 175),
            fs=9.0)
    return save_c(fig, "gridsearch.png")


def fig_tradeoff_map():
    X, y, names = concrete_table(300, seed=23)
    # water/cement is left out on purpose: hand a linear model the engineered
    # ratio and it wins by construction, which is a different lesson.
    Xr = X[:, [0, 1, 2, 4]]
    tr, te = holdout(len(y), 0.25, seed=5)

    w = ols(Xr[tr], y[tr])
    r_lin = reg_metrics(y[te], ols_pred(w, Xr[te]))[2]
    t3 = grow_tree(Xr[tr], y[tr], 3, 8, kind="sse")
    r_tree = reg_metrics(y[te], tree_predict(t3, Xr[te], "value"))[2]
    frt = grow_forest(Xr[tr], y[tr], 300, 7, 3, kind="sse", seed=1, max_feats=3)
    r_for = reg_metrics(y[te], forest_predict(frt, Xr[te], "sse"))[2]
    bst = boost_fit(Xr[tr], y[tr], 200, 0.08, depth=2, min_leaf=6)
    r_bst = reg_metrics(y[te], boost_predict(bst, Xr[te]))[2]

    # All four markers are neutral INK. Nothing here is "the answer" — that is
    # the argument of the figure, so no marker gets the orange.
    pts = [("Linear regression", 4.0, r_lin, -1,
            "one equation, one\ncoefficient per column"),
           ("Decision tree, depth 3", 3.0, r_tree, +1,
            "a flowchart you can\nread out loud"),
           ("Random forest", 2.0, r_for, -1,
            "300 trees voting. It ranks\ncolumns; it explains no case"),
           ("Gradient boosting", 1.0, r_bst, -1,
            "usually the winner on\ntabular data")]

    fig, ax = plt.subplots(figsize=(12.4, 5.9))
    lo = min(p[2] for p in pts)
    hi = max(p[2] for p in pts)
    pad = (hi - lo) * 0.34
    for nm, ix, r2, up, note in pts:
        ax.scatter([ix], [r2], s=230, color=STEEL2, zorder=5)
        # Each label block sits directly above or below its own marker and is
        # centred on it, so it can never be read against a neighbour's dot.
        ax.text(ix, r2 + up * pad * 0.16, f"{nm}\nR² = {r2:.3f}", ha="center",
                va="bottom" if up > 0 else "top", fontsize=10.4, fontweight="bold",
                color=INK, linespacing=1.5, zorder=6)
        # 0.96 clears the full height of the two-line name block above it
        ax.text(ix, r2 + up * pad * (0.16 + 0.96), note, ha="center",
                va="bottom" if up > 0 else "top", fontsize=8.8, color=INK2,
                linespacing=1.6, zorder=6)
    ax.set_xlim(0.45, 4.60)
    ax.set_ylim(lo - pad, hi + pad)
    ax.set_xticks([1, 2, 3, 4])
    ax.set_xticklabels(["a black box", "you can rank\nthe columns",
                        "a rule you can\nread aloud", "one equation,\nwith units"],
                       fontsize=9.6)
    ax.set_xlabel("How much of it you can explain to the client  →  "
                  "(this ordering is a teaching judgement)", fontsize=10.6)
    ax.set_ylabel("Test R² on this dataset  (measured)", fontsize=11)
    _grid(ax)
    ax.set_title("There is no best model. There is a best model for the constraint "
                 "you were given.",
                 fontsize=13.0, fontweight="bold", color=INK, loc="left", pad=14)

    fig.text(0.008, 0.205,
             wrapped(f"On this data the single tree is beaten on BOTH axes — linear "
                     f"regression is more accurate ({r_lin:.3f} against "
                     f"{r_tree:.3f}) and easier to explain. A depth-3 tree is not "
                     f"automatically the safe middle choice.", 160),
             fontsize=10.2, color=INK, va="bottom", linespacing=1.6)
    fig.text(0.008, 0.130,
             f"Boosting buys {r_bst - r_lin:+.3f} of R² over the equation. If the "
             f"client has to sign off on why one mix was rejected, that trade is not "
             f"obviously worth making.",
             fontsize=10.2, color=ORANGE, fontweight="bold", va="bottom")
    fig.text(0.008, 0.018,
             wrapped(f"{ILLUS} The vertical axis is measured: four models, all fitted "
                     f"on the same {len(tr)} rows and scored on the same {len(te)} "
                     f"held-out rows, with cement, water, age and batch number as features "
                     f"(the water/cement ratio is deliberately withheld, since handing the "
                     f"linear model the engineered ratio would decide the comparison by "
                     f"construction). The horizontal axis is a teaching judgement about "
                     f"explainability and carries no units — do not read distances "
                     f"along it as quantities."),
             fontsize=8.8, color=MUTED, style="italic", va="bottom", linespacing=1.6)
    fig.subplots_adjust(left=0.068, right=0.988, top=0.885, bottom=0.385)
    return save(fig, "tradeoff_map.png", pad=0.10)


# ===============================================================================
# WEEK 13 — REPRODUCIBILITY
# ===============================================================================
def fig_repo_structure():
    fig, ax = canvas(12.7, 5.95, y0=0.10)
    ax.text(0.25, 5.95, "What a reviewer opens, and in what order",
            fontsize=13.5, fontweight="bold", color=INK, va="center")
    ax.text(0.25, 5.62, "The folder itself is part of the answer. A notebook with no "
                        "repository around it cannot be checked by anyone.",
            fontsize=9.8, color=MUTED, va="center")

    rows = [(0, "concrete-strength/", "", "the project — one folder, one job", INK, 0),
            (1, "README.md", "1", "What is this, what data, how do I run it, what did "
                                  "you find. Half a page.", ORANGE, 1),
            (1, "requirements.txt", "2", "The exact package versions. Without it your "
                                         "results are not reproducible, only lucky.",
             ORANGE, 2),
            (1, "data/", "", "", INK, 0),
            (2, "raw/", "", "Exactly as it arrived. NEVER edited, never overwritten, "
                            "and usually not committed.", TEAL, 0),
            (2, "processed/", "", "Rebuilt from raw/ by code in src/, so it can always "
                                  "be thrown away and remade.", TEAL, 0),
            (1, "notebooks/", "", "Where you thought. Numbered in the order they are "
                                  "meant to be read.", INK, 0),
            (1, "src/", "3", "The functions the notebooks call. Code you would defend "
                             "lives here, not in a cell.", ORANGE, 3),
            (1, ".gitignore", "", "Keeps the 400 MB CSV and your secrets out of the "
                                  "history.", MUTED, 0)]

    y0 = 5.05
    RH = 0.42
    for lvl, name, order, note, col, ordn in rows:
        x = 0.42 + lvl * 0.62
        is_dir = name.endswith("/")
        if lvl > 0:
            ax.plot([x - 0.30, x - 0.10], [y0 + 0.16, y0 + 0.16], color="#C3CFDA",
                    lw=1.4, zorder=1)
            ax.plot([x - 0.30, x - 0.30], [y0 + 0.16 + RH * 0.55, y0 + 0.16],
                    color="#C3CFDA", lw=1.4, zorder=1)
        code(ax, x, y0 + 0.16, name, fs=11.5,
             color=col if col is not MUTED else MUTED)
        if is_dir:
            ax.add_patch(Rectangle((x - 0.24, y0 + 0.06), 0.14, 0.16,
                                   facecolor="#B9C8D8", edgecolor="none", zorder=3))
        if ordn:
            badge(ax, 5.42, y0 + 0.16, ordn, col=ORANGE, r=0.155, fs=9.5)
        if note:
            ax.text(5.78, y0 + 0.16, note, fontsize=9.4, color=INK, va="center",
                    zorder=3)
        y0 -= RH

    panel(ax, 0.25, 0.98, 12.20, 0.60, face=FADE_T, edge=TEAL, lw=2.0, r=0.08)
    ax.text(0.50, 1.28,
            "The test:  clone it onto a machine that has never seen it, install "
            "requirements.txt, run the notebooks in order — do you get the same "
            "numbers?",
            fontsize=10.6, fontweight="bold", color=TEAL, va="center", zorder=3)

    ax.text(0.25, 0.70,
            "The numbered items are the order a marker or a reviewer actually reads in. "
            "None of them is your model.",
            fontsize=10.4, fontweight="bold", color=INK, va="center")
    caption(ax, 0.25, 0.34,
            wrapped("A raw folder that is never edited is what lets you answer “where "
                    "did this number come from?” a month later. It is also the only "
                    "defence against quietly cleaning the same file twice, in two "
                    "different ways.", 175), fs=9.0)
    return save_c(fig, "repo_structure.png")


if __name__ == "__main__":
    made = [fig_nested(), fig_rules_vs_learning(), fig_four_limits(), fig_assessment(),
            fig_ladder(), fig_arc(), fig_clock(),
            *[fig_clock_week(w) for w in range(1, 16)],
            fig_roadmap_journey(), fig_roadmap_coverage(), fig_career_paths(),
            # Week 2 — Colab, notebooks, version control
            fig_notebook_anatomy(), fig_execution_trap(), fig_git_states(), fig_tool_map(),
            # Week 3 — Python as an engineering calculator
            fig_variable_box(), fig_function_anatomy(), fig_traceback_anatomy(),
            fig_silent_wrong(),
            # Week 4 — collections, loops, files
            fig_list_vs_dict(), fig_accumulator_trace(), fig_accumulator_bug(),
            fig_file_pipeline(),
            # Week 5 — NumPy and pandas
            fig_loops_vs_vectorised(), fig_dataframe_anatomy(),
            fig_split_apply_combine(), fig_boolean_mask(),
            # Week 6 — dirty data, and seeing it
            fig_defect_types(), fig_missingness_map(), fig_boxplot_annotated(),
            fig_chart_chooser(),
            # Week 8 — the first model
            fig_fit_by_eye(), fig_train_test_split(), fig_pred_vs_actual(),
            fig_residuals(), fig_baseline_vs_model(), fig_error_metrics(),
            # Week 9 — classification
            fig_decision_boundary(), fig_decision_tree(), fig_forest_vote(),
            fig_threshold_tradeoff(), fig_imbalance_trap(),
            # Week 10 — can I trust this model?
            fig_overfit_curve(), fig_fit_three_panel(), fig_kfold(),
            fig_leakage_types(), fig_leakage_score(),
            # Week 11 — features
            fig_onehot(), fig_scaling_effect(), fig_ablation(),
            # Week 12 — comparison and judgement
            fig_comparison_protocol(), fig_gridsearch(), fig_tradeoff_map(),
            # Week 13 — reproducibility
            fig_repo_structure()]
    for code in ("CML3111", "CML3112", "CML3113"):
        made += [fig_data_table(code), fig_hand_prediction(code, False),
                 fig_hand_prediction(code, True), fig_reg_vs_class(code),
                 fig_confusion_matrix(code), fig_domain_feature(code)]
    print(f"{len(made)} figures written to {OUT}")
    for m in made:
        print("  ", os.path.basename(m), os.path.getsize(m) // 1024, "KB")
