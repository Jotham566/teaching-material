"""Figures for the Week 8b to 12 slides. Every data-driven figure is drawn from the cohort's own CSV
through week_reference_numpy. Illustrative figures say so on the slide caption."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
import week_reference_numpy as R

INK, ORANGE, TEAL, MUTED = "#1C3144", "#E4572E", "#2E7D6F", "#6B7A8A"
PALE1, PALE2, PALEO = "#EEF3F6", "#E5F1EE", "#FCE9E3"
plt.rcParams.update({"font.family": ["Carlito", "Calibri", "DejaVu Sans"], "font.size": 16,
                     "axes.edgecolor": MUTED, "axes.labelcolor": INK, "text.color": INK,
                     "xtick.color": INK, "ytick.color": INK})
W, H = 12.5, 5.0


def save(fig, path):
    fig.savefig(path, dpi=160, bbox_inches="tight", pad_inches=0.08); plt.close(fig)


def canvas(w=W, h=H):
    fig, ax = plt.subplots(figsize=(w, h)); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off"); return fig, ax


def rbox(ax, x, y, w, h, fc, ec=None, lw=2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.01,rounding_size=0.02", fc=fc, ec=ec or fc, lw=lw))


def arr(ax, p, q, color=MUTED, lw=2.4):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=22, lw=lw, color=color))


def despine(ax):
    for s in ("top", "right"): ax.spines[s].set_visible(False)


# ------------------------------------------------------------------ Week 8b
def fig_blanks(path, code):
    raw, d, tr, va, te = R.load(code)
    miss = tr[tr[R.FEATURES].isna().any(axis=1)].head(1)
    med = tr[R.FEATURES].median()
    others = tr[~tr[R.FEATURES].isna().any(axis=1)].head(2)
    rows = pd.concat([others, miss]); fig, ax = canvas(12.5, 4.4)
    heads = ["record_id", "load_pct", "ambient_c"]; xs = [0.08, 0.26, 0.44]
    ax.text(0.27, 0.95, "Before: one blank", ha="center", fontsize=19, fontweight="bold")
    ax.add_patch(Rectangle((0.0, 0.62), 0.54, 0.09, fc=INK)); ax.add_patch(Rectangle((0.0, 0.26), 0.54, 0.36, fc=PALE1))
    for x, h in zip(xs, heads): ax.text(x + 0.03, 0.665, h, ha="center", va="center", color="white", fontsize=15)
    for i, (_, r) in enumerate(rows.iterrows()):
        y = 0.55 - i * 0.11
        ax.text(xs[0] + 0.03, y, str(int(r.record_id)), ha="center", fontsize=16)
        ax.text(xs[1] + 0.03, y, "" if pd.isna(r.load_pct) else f"{r.load_pct:g}", ha="center", fontsize=16)
        if pd.isna(r.ambient_c):
            ax.add_patch(Rectangle((xs[2] - 0.045, y - 0.04), 0.15, 0.09, fc="white", ec=ORANGE, lw=2.5)); ax.text(xs[2] + 0.03, y, "blank", ha="center", fontsize=15, color=ORANGE, style="italic")
        else:
            ax.text(xs[2] + 0.03, y, f"{r.ambient_c:g}", ha="center", fontsize=16)
    arr(ax, (0.57, 0.45), (0.65, 0.45), TEAL)
    ax.text(0.61, 0.52, "fill with the\ntraining median", ha="center", fontsize=14, color=TEAL)
    ax.text(0.83, 0.95, "After: filled", ha="center", fontsize=19, fontweight="bold")
    ax.add_patch(Rectangle((0.67, 0.62), 0.32, 0.09, fc=INK)); ax.add_patch(Rectangle((0.67, 0.26), 0.32, 0.36, fc=PALE2))
    for x, h in zip((0.72, 0.89), heads[1:]): ax.text(x, 0.665, h, ha="center", va="center", color="white", fontsize=15)
    for i, (_, r) in enumerate(rows.iterrows()):
        y = 0.55 - i * 0.11
        ax.text(0.72, y, f"{r.load_pct:g}", ha="center", fontsize=16)
        v = med["ambient_c"] if pd.isna(r.ambient_c) else r.ambient_c
        ax.text(0.89, y, f"{v:.2f}" if pd.isna(r.ambient_c) else f"{v:g}", ha="center", fontsize=16, color=TEAL if pd.isna(r.ambient_c) else INK, fontweight="bold" if pd.isna(r.ambient_c) else "normal")
    ax.text(0.5, 0.08, f"The median ambient_c of the training rows is {med['ambient_c']:.2f}. The same number fills any blank in later rows.", ha="center", fontsize=16)
    save(fig, path)
    return dict(record_id=int(miss.record_id.iloc[0]) if len(miss) else None, med=float(med["ambient_c"]))


def fig_pipeline(path):
    fig, ax = canvas(12.5, 4.2)
    steps = [("Rows", "load_pct, ambient_c", PALE1, INK), ("Step 1", "Imputer fills blanks", PALE2, TEAL), ("Step 2", "Model makes\nthe prediction", ORANGE, "white"), ("Output", "One prediction\nper row", PALE1, INK)]
    for i, (a, b, fc, fg) in enumerate(steps):
        x = 0.01 + i * 0.255
        rbox(ax, x, 0.42, 0.21, 0.40, fc)
        ax.text(x + 0.105, 0.72, a, ha="center", fontsize=18, fontweight="bold", color=fg)
        ax.text(x + 0.105, 0.55, b, ha="center", va="center", fontsize=15, color=fg)
        if i < 3: arr(ax, (x + 0.215, 0.62), (x + 0.25, 0.62))
    rbox(ax, 0.26, 0.10, 0.48, 0.17, PALE1)
    ax.text(0.50, 0.185, "fit runs both steps on the training rows.  predict runs both steps on new rows.", ha="center", va="center", fontsize=16)
    save(fig, path)


def fig_tree(path, code):
    raw, d, tr, va, te = R.load(code); (trf, vaf), med = R.median_fill(tr, [va])
    t = R.tree_reg_fit(trf, tr.target.to_numpy(), 2); names = R.FEATURES
    fig, ax = canvas(12.5, 5.0)

    def node(x, y, text, fc, fg=INK, w=0.26):
        rbox(ax, x - w / 2, y - 0.07, w, 0.14, fc); ax.text(x, y, text, ha="center", va="center", fontsize=16, color=fg)
    root = f"{names[t[1]]} <= {t[2]:.2f} ?"
    node(0.5, 0.88, root, INK, "white", 0.34)
    for side, x, sub in (("yes", 0.25, t[3]), ("no", 0.75, t[4])):
        arr(ax, (0.5, 0.81), (x, 0.66)); ax.text((0.5 + x) / 2 + (-0.03 if side == "yes" else 0.03), 0.75, side, fontsize=16, color=TEAL, fontweight="bold")
        if sub[0] == "split":
            node(x, 0.60, f"{names[sub[1]]} <= {sub[2]:.2f} ?", PALE1, INK, 0.30)
            for s2, x2, leaf in (("yes", x - 0.12, sub[3]), ("no", x + 0.12, sub[4])):
                arr(ax, (x, 0.53), (x2, 0.33)); ax.text((x + x2) / 2 + (-0.02 if s2 == "yes" else 0.02), 0.45, s2, fontsize=14, color=TEAL)
                node(x2, 0.26, f"predict\n{leaf[1]:.1f}", ORANGE, "white", 0.17)
        else:
            node(x, 0.52, f"predict {sub[1]:.1f}", ORANGE, "white", 0.2)
    ax.text(0.5, 0.04, f"Each leaf predicts the average {unit_of(code)} of the training rows that end there.", ha="center", fontsize=16)
    save(fig, path)


def unit_of(code): return R.COHORT[code]["unit"]


# ------------------------------------------------------------------ Week 9
def fig_cls_vs_reg(path, code):
    raw, d_all, tr, va, te = R.load(code); c = R.COHORT[code]; d = pd.concat([tr, va])
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12.5, 4.8), sharex=True)
    a1.scatter(d.load_pct, d.target, s=45, color=INK)
    a1.set_title("Regression: the answer is a number", fontsize=18, fontweight="bold"); a1.set_xlabel("load_pct"); a1.set_ylabel(f"target ({c['unit']})")
    hi = d.target >= c["limit"]
    a2.scatter(d.load_pct[~hi], d.target[~hi], s=45, color=INK, label="no alert (0)")
    a2.scatter(d.load_pct[hi], d.target[hi], s=60, color=ORANGE, marker="D", label="alert (1)")
    a2.axhline(c["limit"], color=TEAL, ls="--", lw=2.4); a2.text(d.load_pct.min(), c["limit"] + (d.target.max() - d.target.min()) * 0.02, f"limit {c['limit']:g} {c['unit']}", color=TEAL, fontsize=15)
    a2.set_title("Classification: the answer is a class", fontsize=18, fontweight="bold"); a2.set_xlabel("load_pct"); a2.legend(frameon=False, loc="lower right", fontsize=14)
    for a in (a1, a2): despine(a); a.grid(alpha=0.2)
    fig.tight_layout(); save(fig, path)


def fig_counts(path, code):
    o = R.bundle(code); k = o["cls_counts"]; no = k["tr_n"] - k["tr_pos"]
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    ax.bar(["no alert (0)", "alert (1)"], [no, k["tr_pos"]], color=[INK, ORANGE], width=0.55)
    for i, v in enumerate([no, k["tr_pos"]]): ax.text(i, v + 1.5, str(v), ha="center", fontsize=22, fontweight="bold")
    ax.set_ylabel("rows"); ax.set_ylim(0, no + 14); despine(ax); ax.grid(axis="y", alpha=0.2)
    save(fig, path)
    return dict(no=no, pos=k["tr_pos"], n=k["tr_n"], acc=no / k["tr_n"])


def fig_sigmoid(path, code):
    raw, d_all, tr, va, te = R.load(code); c = R.COHORT[code]; d = tr
    y = (d.target >= c["limit"]).astype(int).to_numpy(); x = d.load_pct.to_numpy()
    mu, sd = x.mean(), x.std(); b, w = R.logreg_fit(((x - mu) / sd)[:, None], y)
    xs = np.linspace(x.min() - 3, x.max() + 3, 200); p = R.logreg_proba(b, w, ((xs - mu) / sd)[:, None])
    fig, ax = plt.subplots(figsize=(12.5, 4.8))
    ax.scatter(x[y == 0], y[y == 0], s=55, color=INK, label="no alert (0)", zorder=3); ax.scatter(x[y == 1], y[y == 1], s=70, color=ORANGE, marker="D", label="alert (1)", zorder=3)
    ax.plot(xs, p, color=TEAL, lw=3.4, label="probability of an alert"); ax.axhline(0.5, color=MUTED, ls="--", lw=2); ax.text(xs[-1], 0.53, "threshold 0.5", color=MUTED, fontsize=14, ha="right")
    ax.set_xlabel("load_pct  (equipment load, %)"); ax.set_ylabel("probability of an alert"); ax.legend(frameon=False, loc="upper left", bbox_to_anchor=(0.0, 0.88), fontsize=14); despine(ax); ax.grid(alpha=0.2)
    save(fig, path)
    cross = float(xs[np.argmin(np.abs(p - 0.5))]); p90 = float(R.logreg_proba(b, w, ((np.array([90.0]) - mu) / sd)[:, None])[0])
    return dict(cross=cross, p90=p90, n=len(x))


def fig_confusion(path, code, conf, title="Validation rows"):
    fig, ax = plt.subplots(figsize=(7.2, 4.9)); ax.set_xlim(0, 2); ax.set_ylim(0, 2); ax.axis("off")
    cells = [(0, 1, "tn", "True negative", PALE1, INK), (1, 1, "fp", "False positive", PALEO, INK), (0, 0, "fn", "False negative", PALEO, INK), (1, 0, "tp", "True positive", ORANGE, "white")]
    for x, y, k, name, fc, fg in cells:
        ax.add_patch(Rectangle((x, y), 1, 1, fc=fc, ec="white", lw=4))
        ax.text(x + 0.5, y + 0.58, str(conf[k]), ha="center", va="center", fontsize=40, fontweight="bold", color=fg)
        ax.text(x + 0.5, y + 0.22, name, ha="center", va="center", fontsize=16, color=fg)
    ax.text(0.5, 2.1, "model says no", ha="center", fontsize=16); ax.text(1.5, 2.1, "model says yes", ha="center", fontsize=16)
    ax.text(-0.06, 1.5, "actually no", ha="right", va="center", fontsize=16); ax.text(-0.06, 0.5, "actually yes", ha="right", va="center", fontsize=16)
    save(fig, path)


def fig_roc(path, code):
    o = R.bundle(code); pts = o["roc"]
    fig, ax = plt.subplots(figsize=(6.2, 5.0))
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=ORANGE, lw=3.4, marker="o", ms=6, label=f"our model, AUC = {o['auc']:.2f}")
    ax.plot([0, 1], [0, 1], color=MUTED, ls="--", lw=2, label="guessing, AUC = 0.50")
    ax.set_xlabel("false alarm rate  (FP / all actual no)"); ax.set_ylabel("detection rate  (TP / all actual yes)")
    ax.set_xlim(-0.02, 1.02); ax.set_ylim(-0.02, 1.05); ax.legend(frameon=False, loc="lower right", fontsize=14); despine(ax); ax.grid(alpha=0.2)
    save(fig, path)


# ------------------------------------------------------------------ Week 10
def fig_three_fits(path, code):
    raw, d, tr, va, te = R.load(code); (trf, vaf), med = R.median_fill(tr, [va])
    x = trf[["load_pct"]].to_numpy(); y = tr.target.to_numpy(); xs = np.linspace(x.min(), x.max(), 400)[:, None]
    fig, axs = plt.subplots(1, 3, figsize=(12.5, 4.4), sharey=True)
    for a, depth, title, col in zip(axs, (1, 3, 12), ("Too simple", "About right", "Memorises"), (MUTED, TEAL, ORANGE)):
        t = R.tree_reg_fit(x, y, depth)
        a.scatter(x, y, s=34, color=INK, zorder=3); a.plot(xs, R.tree_predict(t, xs), color=col, lw=3)
        a.set_title(f"{title}\n(tree depth {depth})", fontsize=17, fontweight="bold"); a.set_xlabel("load_pct"); despine(a); a.grid(alpha=0.2)
    axs[0].set_ylabel(f"target ({R.COHORT[code]['unit']})"); fig.tight_layout(); save(fig, path)


def fig_overfit_curve(path, code):
    o = R.bundle(code); cv = o["overfit_curve"]; u = R.COHORT[code]["unit"]
    fig, ax = plt.subplots(figsize=(12.5, 4.8))
    ax.plot([c[0] for c in cv], [c[1] for c in cv], color=INK, lw=3.4, marker="o", label="error on the training rows")
    ax.plot([c[0] for c in cv], [c[2] for c in cv], color=ORANGE, lw=3.4, marker="D", label="error on the validation rows")
    best = min(cv, key=lambda c: c[2]); ax.annotate("validation error stops improving", (best[0], best[2]), xytext=(best[0] + 0.5, best[2] + max(c[2] for c in cv) * 0.30), fontsize=15, color=ORANGE, arrowprops=dict(arrowstyle="-|>", color=ORANGE))
    ax.set_xlabel("tree depth  (how flexible the model is)"); ax.set_ylabel(f"MAE ({u})"); ax.set_xticks(range(1, 11)); ax.legend(frameon=False, fontsize=15); despine(ax); ax.grid(alpha=0.2)
    save(fig, path)


def fig_leak_kinds(path):
    fig, ax = canvas(12.5, 5.0)
    items = [("1  Copies across the split", "The same observation sits in\ntraining and in validation.", "A repeated record_id."),
             ("2  Preparing before splitting", "A median or scale is learned from\nall rows, validation included.", "Fit the imputer on training only."),
             ("3  Same group on both sides", "Rows from one machine appear in\ntraining and in the test.", "Keep whole equipment groups together."),
             ("4  A column that holds the answer", "An input that is only known\nafter the outcome.", "Use inputs available at prediction time.")]
    for i, (t, b, ex) in enumerate(items):
        x = 0.01 + (i % 2) * 0.50; y = 0.52 if i < 2 else 0.04
        rbox(ax, x, y, 0.47, 0.42, PALE1)
        ax.text(x + 0.02, y + 0.34, t, fontsize=18, fontweight="bold", va="center"); ax.text(x + 0.02, y + 0.20, b, fontsize=15, va="center")
        ax.text(x + 0.02, y + 0.06, "Guard: " + ex, fontsize=15, va="center", color=TEAL, fontweight="bold")
    save(fig, path)


# ------------------------------------------------------------------ Week 11 and 12 (illustrative)
def fig_curved_toy(path):
    rng = np.random.default_rng(7); x = np.linspace(1, 9, 40); y = 0.5 * x ** 2 + rng.normal(0, 1.2, x.size)
    b, w = R.linreg_fit(x[:, None], y); b2, w2 = R.linreg_fit(np.column_stack([x, x ** 2]), y); xs = np.linspace(1, 9, 200)
    fig, axs = plt.subplots(1, 2, figsize=(12.5, 4.5), sharey=True)
    for a, ttl, yy in zip(axs, ("Straight line on x", "Line on x and x squared"), (b + w[0] * xs, b2 + w2[0] * xs + w2[1] * xs ** 2)):
        a.scatter(x, y, s=36, color=INK, zorder=3); a.plot(xs, yy, color=ORANGE if a is axs[0] else TEAL, lw=3.4); a.set_title(ttl, fontsize=18, fontweight="bold"); a.set_xlabel("x"); despine(a); a.grid(alpha=0.2)
    axs[0].set_ylabel("y"); fig.tight_layout(); save(fig, path)
    return dict(mae_line=R.mae(y, b + w[0] * x), mae_curve=R.mae(y, b2 + w2[0] * x + w2[1] * x ** 2))


def fig_forest(path):
    fig, ax = canvas(12.5, 4.6)
    ax.text(0.5, 0.95, "Five trees each predict. The forest averages their answers.", ha="center", fontsize=19, fontweight="bold")
    preds = [71.0, 76.5, 69.0, 74.0, 73.5]
    for i, p in enumerate(preds):
        x = 0.04 + i * 0.185; rbox(ax, x, 0.42, 0.15, 0.36, PALE2)
        ax.text(x + 0.075, 0.68, f"Tree {i + 1}", ha="center", fontsize=17, fontweight="bold", color=TEAL); ax.text(x + 0.075, 0.54, f"{p:g}", ha="center", fontsize=26, fontweight="bold")
        arr(ax, (x + 0.075, 0.41), (0.5, 0.27), MUTED, 1.8)
    rbox(ax, 0.34, 0.06, 0.32, 0.20, ORANGE); ax.text(0.5, 0.16, f"Forest: {np.mean(preds):g}", ha="center", va="center", fontsize=24, color="white", fontweight="bold")
    save(fig, path)
    return float(np.mean(preds))


def fig_boosting(path):
    fig, ax = canvas(12.5, 4.6)
    truth = 80.0; stages = [("Stage 1", 70.0), ("Stage 2", 77.0), ("Stage 3", 79.1)]
    ax.text(0.5, 0.95, f"Each new small tree corrects what is still wrong. The true value is {truth:g}.", ha="center", fontsize=19, fontweight="bold")
    for i, (n, p) in enumerate(stages):
        x = 0.03 + i * 0.32; rbox(ax, x, 0.30, 0.28, 0.50, PALE1 if i < 2 else PALE2)
        ax.text(x + 0.14, 0.72, n, ha="center", fontsize=19, fontweight="bold", color=TEAL if i == 2 else INK); ax.text(x + 0.14, 0.56, f"prediction {p:g}", ha="center", fontsize=18)
        ax.text(x + 0.14, 0.40, f"still missing {truth - p:.1f}", ha="center", fontsize=18, color=ORANGE, fontweight="bold")
        if i < 2: arr(ax, (x + 0.285, 0.55), (x + 0.315, 0.55))
    ax.text(0.5, 0.12, "These numbers are invented to show the idea.", ha="center", fontsize=16, color=MUTED)
    save(fig, path)


# ------------------------------------------------------------------ Week 13
def fig_poly_ridge(path, code, degree=6):
    raw, d, tr, va, te = R.load(code); c = R.COHORT[code]
    xt, yt, xv, yv = tr.load_pct.to_numpy(), tr.target.to_numpy(), va.load_pct.to_numpy(), va.target.to_numpy()
    xs = np.linspace(xt.min(), xt.max(), 300); Pt, Ps = R.poly_cols(xt, degree), R.poly_cols(xs, degree)
    fig, axs = plt.subplots(1, 2, figsize=(12.5, 4.6), sharey=True)
    for a, (alpha, title, col) in zip(axs, ((0.0, "No penalty", ORANGE), (1.0, "Penalty alpha = 1", TEAL))):
        m = R.ridge_fit(Pt, yt, alpha)
        a.scatter(xt, yt, s=32, color=INK, zorder=3, label="training rows"); a.scatter(xv, yv, s=60, color=ORANGE, marker="D", zorder=4, label="validation rows")
        a.plot(xs, R.ridge_predict(m, Ps), color=col, lw=3.2); a.set_title(title, fontsize=19, fontweight="bold"); a.set_xlabel("load_pct"); despine(a); a.grid(alpha=0.2)
        lo, hi = np.min(np.r_[yt, yv]), np.max(np.r_[yt, yv]); a.set_ylim(lo - 0.15 * (hi - lo), hi + 0.25 * (hi - lo))
    axs[0].set_ylabel(f"target ({c['unit']})"); axs[0].legend(frameon=False, fontsize=13, loc="upper left")
    fig.tight_layout(); save(fig, path)


def fig_knn(path, code):
    o = R.bundle13(code); raw, d, tr, va, te = R.load(code); ex = o["knn_example"]; (trf, vaf), med = R.median_fill(tr, [va])
    mu, sd = R.scaler_fit(trf); Zt, Zv = R.scaler_apply(trf, mu, sd), R.scaler_apply(vaf, mu, sd); q = Zv[0]; idx = ex["idx"]
    fig, ax = plt.subplots(figsize=(10.5, 4.9)); ax.set_aspect("equal", adjustable="datalim")
    ax.scatter(Zt[:, 0], Zt[:, 1], s=40, color="#B8C4CE", zorder=2, label="training rows")
    for i in idx: ax.plot([q[0], Zt[i, 0]], [q[1], Zt[i, 1]], color=TEAL, lw=2.2, zorder=3)
    ax.scatter(Zt[idx, 0], Zt[idx, 1], s=130, color=TEAL, zorder=4, label="3 nearest neighbours")
    offs = [(10, 10), (10, -20), (-48, 10)]
    for n, i in enumerate(idx): ax.annotate(f"{ex['neighbour_targets'][n]:g}", (Zt[i, 0], Zt[i, 1]), textcoords="offset points", xytext=offs[n], fontsize=15, color=TEAL, fontweight="bold")
    ax.scatter([q[0]], [q[1]], s=260, marker="*", color=ORANGE, zorder=5, label="row to predict")
    ax.set_xlabel("load_pct (scaled)"); ax.set_ylabel("ambient_c (scaled)"); ax.legend(frameon=False, fontsize=13, loc="upper left", bbox_to_anchor=(1.01, 1.0)); despine(ax); ax.grid(alpha=0.2)
    save(fig, path)
    return ex
