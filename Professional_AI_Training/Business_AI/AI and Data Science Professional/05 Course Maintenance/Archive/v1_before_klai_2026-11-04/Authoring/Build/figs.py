"""Explanatory figures for the decks, drawn from the generated teaching data (numpy, pandas, matplotlib only).

  python3 figs.py DATA_FOLDER OUTPUT_FOLDER

Every figure has a name, a one-line description (for authors) and alt text (for the slide). Real-data figures read the CSVs;
schematics are labelled as such by their subject. No figure shows a number that is not computed from the data.
"""
import sys, json, math
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, FancyArrowPatch, Polygon, Ellipse

INK, LAKE, GOLD, CORAL, LEAF, MUTED, LINE, CARD = '#1F2328', '#4B4640', '#8B8478', '#B04A2B', '#5E7A57', '#6A6F75', '#C9C5BC', '#F5F3EF'   # charcoal (data), warm grey, clay (highlight), moss (good)
FONT = 'Carlito' if any('Carlito' in f.name for f in fm.fontManager.ttflist) else 'DejaVu Sans'
plt.rcParams.update({'font.family': FONT, 'font.size': 15, 'axes.titlesize': 16, 'axes.labelsize': 16, 'xtick.labelsize': 14, 'ytick.labelsize': 14, 'axes.edgecolor': MUTED, 'axes.labelcolor': INK,
                     'xtick.color': INK, 'ytick.color': INK, 'axes.spines.top': False, 'axes.spines.right': False, 'figure.dpi': 100, 'savefig.dpi': 200, 'axes.grid': False,
                     'axes.titleweight': 'bold', 'legend.frameon': False, 'legend.fontsize': 14})
CAT = {}   # name -> (description, alt)
D = {}     # data cache
def fig(name, desc, alt):
    def deco(f): CAT[name] = (desc, alt, f); return f
    return deco
def data(k):
    if k not in D: D[k] = pd.read_csv(Path(DATA) / f'{k}.csv')
    return D[k]
def new(w=7.2, h=4.5): f, ax = plt.subplots(figsize=(w, h)); return f, ax
def ugx_k(x, pos=None): return f'{x/1000:,.0f}k'
def save(f, out, name): f.tight_layout(pad=0.6); f.savefig(Path(out) / f'{name}.png', transparent=False, facecolor='white'); plt.close(f)
def box(ax, x, y, w, h, text, fc=CARD, ec=LINE, fs=15, bold=False, color=INK):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.02,rounding_size=0.06', fc=fc, ec=ec, lw=1.2)); ax.text(x + w / 2, y + h / 2, text, ha='center', va='center', fontsize=fs, fontweight='bold' if bold else 'normal', color=color)
def arrow(ax, x1, y1, x2, y2, color=MUTED, lw=2): ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='-|>', mutation_scale=18, lw=lw, color=color))

# ---- shared computations
def order_values():
    ol = data('order_lines'); return ol.groupby('order_id').line_revenue_ugx.sum()
def sigmoid(z): return 1 / (1 + np.exp(-z))
def logit_fit(X, y, it=30):
    X = np.c_[np.ones(len(X)), X]; b = np.zeros(X.shape[1])
    for _ in range(it):
        p = sigmoid(X @ b); W = p * (1 - p) + 1e-9; b = b + np.linalg.solve(X.T @ (X * W[:, None]) + 1e-6 * np.eye(len(b)), X.T @ (y - p))
    return b
def auc(y, s):
    o = np.argsort(s); y = np.asarray(y)[o]; n1 = y.sum(); n0 = len(y) - n1; r = np.arange(1, len(y) + 1); return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))
def roc_pts(y, s):
    o = np.argsort(-s); y = np.asarray(y)[o]; tp = np.cumsum(y) / y.sum(); fp = np.cumsum(1 - y) / (1 - y).sum(); return np.r_[0, fp], np.r_[0, tp]
def loan_model():
    if 'lm' in D: return D['lm']
    lo = data('loans'); lo = lo[lo.age.between(18, 80)].copy()
    lo['burden'] = (lo.loan_amount_ugx * 1.15 / lo.term_months) / lo.monthly_income_ugx.fillna(lo.monthly_income_ugx.median()); lo['save_ratio'] = lo.savings_balance_ugx / lo.loan_amount_ugx
    cols = ['age', 'monthly_income_ugx', 'loan_amount_ugx', 'term_months', 'previous_loans', 'previous_late_payments', 'group_loan', 'savings_balance_ugx', 'has_mobile_money', 'distance_to_branch_km', 'burden', 'save_ratio']
    X = lo[cols].astype(float); X = X.fillna(X.median()); Z = ((X - X.mean()) / X.std()).values; y = lo['default'].values
    idx = np.random.default_rng(1).permutation(len(lo)); tr, te = idx[:int(.75 * len(lo))], idx[int(.75 * len(lo)):]
    b = logit_fit(Z[tr], y[tr]); s = np.c_[np.ones(len(te)), Z[te]] @ b
    cc = ((lo.collection_calls - lo.collection_calls.mean()) / lo.collection_calls.std()).values[:, None]; Zl = np.c_[Z, cc]; bl = logit_fit(Zl[tr], y[tr]); sl = np.c_[np.ones(len(te)), Zl[te]] @ bl
    D['lm'] = dict(cols=cols, b=b, bl=bl, y_te=y[te], s=s, sl=sl, lo=lo, te=te, tr=tr, Z=Z); return D['lm']
def kmeans(X, k, seed=0, it=60):
    r = np.random.default_rng(seed); C = X[r.choice(len(X), k, replace=False)]
    for _ in range(it):
        d = ((X[:, None, :] - C[None]) ** 2).sum(2); lab = d.argmin(1); C2 = np.array([X[lab == j].mean(0) if (lab == j).any() else C[j] for j in range(k)])
        if np.allclose(C, C2): break
        C = C2
    return lab, C, float(((X - C[lab]) ** 2).sum())
def rfm():
    if 'rfm' in D: return D['rfm']
    od = data('orders'); ov = order_values(); od = od[od.customer_id.notna()].copy(); od['v'] = od.order_id.map(ov); od['d'] = pd.to_datetime(od.order_date)
    end = od.d.max(); g = od.groupby('customer_id').agg(recency=('d', lambda s: (end - s.max()).days), frequency=('order_id', 'count'), spend=('v', 'sum')).reset_index()
    D['rfm'] = g; return g

# ================================================================== FIGURES
@fig('ai_ml_dl', 'Nested circles: AI contains machine learning contains deep learning; data science overlaps.', 'Nested circles showing deep learning inside machine learning inside artificial intelligence, with data science overlapping them.')
def f_ai_ml_dl(out):
    f, ax = plt.subplots(figsize=(7.2, 4.8)); ax.set_xlim(0, 10); ax.set_ylim(0, 6.6); ax.axis('off')
    ax.add_patch(Ellipse((4.2, 3.3), 7.6, 6.2, fc='#F5F3EF', ec=LAKE, lw=2)); ax.text(4.2, 5.85, 'Artificial intelligence', ha='center', fontsize=17, fontweight='bold', color=INK)
    ax.add_patch(Ellipse((4.2, 3.0), 5.4, 4.2, fc='#ECE8E1', ec=LAKE, lw=2)); ax.text(4.2, 4.65, 'Machine learning', ha='center', fontsize=17, fontweight='bold', color=INK)
    ax.add_patch(Ellipse((4.2, 2.5), 3.0, 2.1, fc='#DDD7CC', ec=LAKE, lw=2)); ax.text(4.2, 2.5, 'Deep\nlearning', ha='center', va='center', fontsize=17, fontweight='bold', color=INK)
    ax.add_patch(Ellipse((8.2, 2.2), 3.4, 3.2, fc=(0.69, 0.29, 0.17, 0.18), ec=GOLD, lw=2)); ax.text(8.55, 2.2, 'Data\nscience', ha='center', va='center', fontsize=17, fontweight='bold', color=INK)
    save(f, out, 'ai_ml_dl')

@fig('order_value_hist', 'Histogram of order value with mean and median marked (real, Lakeside orders).', 'Histogram of order values. Most orders are small, a long tail runs right, and the mean lies to the right of the median.')
def f_order_hist(out):
    v = order_values() / 1000; f, ax = new(); ax.hist(v[v <= 300], bins=45, range=(0, 300), color=LAKE, edgecolor='white'); m, md = v.mean(), v.median()
    ax.axvline(md, color=GOLD, lw=3); ax.axvline(m, color=CORAL, lw=3); ax.text(md + 5, ax.get_ylim()[1] * 0.93, f'median {md:,.0f}k', color='#7A3418', ha='left', fontsize=15, fontweight='bold'); ax.text(m + 5, ax.get_ylim()[1] * 0.8, f'mean {m:,.0f}k', color=CORAL, fontsize=15, fontweight='bold')
    ax.set_xlabel('Order value (UGX thousands; orders above 300k not shown)'); ax.set_ylabel('Number of orders'); save(f, out, 'order_value_hist')

@fig('distribution_shapes', 'Three distribution shapes (symmetric, right-skewed, two humps) with mean and median lines (schematic from simulated data).', 'Three histograms: a symmetric one where mean and median match, a right-skewed one where the mean is larger, and a two-peaked one.')
def f_shapes(out):
    r = np.random.default_rng(3); f, axs = plt.subplots(1, 3, figsize=(10.5, 3.9)); sets = [('Symmetric', r.normal(50, 10, 4000)), ('Right-skewed', r.lognormal(3.3, 0.6, 4000)), ('Two humps', np.r_[r.normal(35, 6, 2000), r.normal(70, 6, 2000)])]
    for ax, (t, x) in zip(axs, sets):
        ax.hist(x, bins=36, color=LAKE, edgecolor='white'); ax.axvline(np.median(x), color=GOLD, lw=3); ax.axvline(x.mean(), color=CORAL, lw=3, ls='--'); ax.set_title(t); ax.set_yticks([])
    axs[0].plot([], [], color=GOLD, lw=3, label='median'); axs[0].plot([], [], color=CORAL, lw=3, ls='--', label='mean'); axs[0].legend(loc='upper left'); save(f, out, 'distribution_shapes')

@fig('boxplot_anatomy', 'Annotated box plot: median, quartiles, whiskers, outliers (schematic).', 'A box plot labelled with median, first and third quartile, whiskers and outliers.')
def f_boxanat(out):
    r = np.random.default_rng(5); x = np.r_[r.normal(50, 9, 300), [92, 98, 101]]; f, ax = new(7.2, 4.4); ax.boxplot(x, vert=False, widths=0.5, patch_artist=True, boxprops=dict(facecolor='#ECE8E1', edgecolor=LAKE, lw=2), medianprops=dict(color=CORAL, lw=3), whiskerprops=dict(color=LAKE, lw=2), capprops=dict(color=LAKE, lw=2), flierprops=dict(marker='o', mfc=GOLD, mec=INK, ms=8))
    q1, md, q3 = np.percentile(x, [25, 50, 75]); ax.annotate('median', (md, 1.25), (md, 1.45), ha='center', fontsize=15, fontweight='bold', color=CORAL, arrowprops=dict(arrowstyle='-', color=CORAL)); ax.annotate('quartile 1\n(25% below)', (q1, 0.75), (q1 - 5, 0.55), ha='right', va='center', fontsize=14)
    ax.annotate('quartile 3\n(75% below)', (q3, 0.75), (q3 + 5, 0.55), ha='left', va='center', fontsize=14); ax.annotate('outliers', (97, 1.04), (88, 1.38), fontsize=14, color='#7A3418', fontweight='bold', arrowprops=dict(arrowstyle='-', color=GOLD)); ax.set_yticks([]); ax.set_ylim(0.3, 1.7); ax.set_xlabel('Value'); ax.spines['left'].set_visible(False); save(f, out, 'boxplot_anatomy')

@fig('revenue_by_month', 'Monthly revenue line 2024-2025 with December highlighted (real).', 'Line chart of monthly revenue across two years, peaking sharply every December.')
def f_rev_month(out):
    od = data('orders'); od = od.assign(v=od.order_id.map(order_values()), m=pd.to_datetime(od.order_date).dt.to_period('M').dt.to_timestamp()); s = od.groupby('m').v.sum() / 1e6
    f, ax = new(7.6, 4.4); ax.plot(s.index, s.values, color=LAKE, lw=3, marker='o', ms=6)
    for d in s.index[s.index.month == 12]: ax.scatter([d], [s[d]], s=150, color=GOLD, zorder=5, edgecolor=INK); ax.annotate(f'Dec {d.year}', (d, s[d]), (0, 12), textcoords='offset points', ha='center', fontsize=14, fontweight='bold')
    ax.set_ylabel('Revenue (UGX millions, sample)'); ax.set_ylim(0, s.max() * 1.2); save(f, out, 'revenue_by_month')

@fig('revenue_by_branch', 'Horizontal bars of sample revenue by branch (real).', 'Horizontal bar chart of revenue for each of the eight branches, largest at Kampala Central.')
def f_rev_branch(out):
    od = data('orders'); br = data('branches').set_index('branch_id').branch_name; s = (od.assign(v=od.order_id.map(order_values())).groupby('branch_id').v.sum() / 1e6).rename(index=br).sort_values()
    f, ax = new(); ax.barh(s.index, s.values, color=LAKE); [ax.text(v + 1, i, f'{v:,.0f}', va='center', fontsize=14, fontweight='bold') for i, v in enumerate(s.values)]; ax.set_xlabel('Revenue (UGX millions, sample)'); ax.set_xlim(0, s.max() * 1.15); save(f, out, 'revenue_by_branch')

@fig('box_by_branch', 'Box plot of order value by branch (real).', 'Box plots of order value for each branch; the boxes are similar and many high-value outliers sit above them.')
def f_box_branch(out):
    od = data('orders'); br = data('branches').set_index('branch_id').branch_name; od = od.assign(v=od.order_id.map(order_values()) / 1000); order = list(br.values)
    f, ax = new(7.8, 4.5); ax.boxplot([od[od.branch_id == b].v.clip(upper=250) for b in br.index], tick_labels=[n.replace('Kampala ', 'Kla ') for n in order], patch_artist=True, boxprops=dict(facecolor='#ECE8E1', edgecolor=LAKE), medianprops=dict(color=CORAL, lw=2.5), showfliers=False)
    ax.set_ylabel('Order value (UGX thousands)'); plt.setp(ax.get_xticklabels(), rotation=25, ha='right'); save(f, out, 'box_by_branch')

@fig('returns_count_vs_rate', 'Two panels: returns COUNT by branch and returns RATE by branch; the leaders differ (real).', 'Two bar charts. By count, Kampala Central has the most returns. By rate, Fort Portal is highest.')
def f_ret(out):
    ol = data('order_lines'); rt = data('returns'); od = data('orders').set_index('order_id'); br = data('branches').set_index('branch_id').branch_name
    lb = ol.order_id.map(od.branch_id).value_counts(); rb = rt.order_id.map(od.branch_id).value_counts(); rate = (rb / lb * 100).rename(index=br); cnt = rb.rename(index=br)
    order = list(cnt.sort_values().index); f, axs = plt.subplots(1, 2, figsize=(10.5, 4.4), sharey=True)
    c = cnt.reindex(order); axs[0].barh(order, c.values, color=[GOLD if i == c.idxmax() else LAKE for i in order]); axs[0].set_title('Number of returns'); [axs[0].text(v + 3, i, f'{v}', va='center', fontsize=14) for i, v in enumerate(c.values)]
    r = rate.reindex(order); axs[1].barh(order, r.values, color=[GOLD if i == r.idxmax() else LAKE for i in order]); axs[1].set_title('Returns per 100 lines sold'); [axs[1].text(v + 0.05, i, f'{v:.1f}', va='center', fontsize=14) for i, v in enumerate(r.values)]
    axs[0].set_xlim(0, c.max() * 1.18); axs[1].set_xlim(0, r.max() * 1.2); save(f, out, 'returns_count_vs_rate')

@fig('bad_vs_good_axis', 'The same four bars on a truncated axis and on a zero-based axis (schematic, made-up values).', 'Two bar charts of the same data. With a cut axis the difference looks huge; from zero it is small.')
def f_axis(out):
    f, axs = plt.subplots(1, 2, figsize=(10, 4.2)); v = [96, 97, 98, 100]; n = ['A', 'B', 'C', 'D']
    for ax, lo, t in zip(axs, (94, 0), ('Axis starts at 94', 'Axis starts at 0')): ax.bar(n, v, color=[LAKE] * 3 + [CORAL]); ax.set_ylim(lo, 101.5); ax.set_title(t)
    save(f, out, 'bad_vs_good_axis')

@fig('category_revenue', 'Bars of revenue by product category (real).', 'Bar chart of sample revenue by product category; staples and phones and electronics lead.')
def f_cat(out):
    ol = data('order_lines').merge(data('products')[['product_id', 'category']], on='product_id'); s = (ol.groupby('category').line_revenue_ugx.sum() / 1e6).sort_values()
    f, ax = new(7.6, 4.6); ax.barh(s.index, s.values, color=LAKE); [ax.text(v + 2, i, f'{v:,.0f}', va='center', fontsize=14, fontweight='bold') for i, v in enumerate(s.values)]; ax.set_xlabel('Revenue (UGX millions, sample)'); ax.set_xlim(0, s.max() * 1.15); save(f, out, 'category_revenue')

@fig('payment_split', 'Bars: share of orders by payment method (real).', 'Bar chart of the share of orders paid by cash, mobile money and card.')
def f_pay(out):
    s = data('orders').payment_method.value_counts(normalize=True) * 100; f, ax = new(6.4, 4.2); ax.bar(s.index, s.values, color=[LAKE, GOLD, MUTED]); [ax.text(i, v + 1, f'{v:.0f}%', ha='center', fontsize=16, fontweight='bold') for i, v in enumerate(s.values)]; ax.set_ylim(0, 60); ax.set_ylabel('Share of orders (%)'); save(f, out, 'payment_split')

@fig('sampling_means', '200 sample means of 30 orders each, with the true mean marked (real, seeded simulation).', 'Histogram of 200 sample means, each from 30 random orders, centred near the true mean and spread out around it.')
def f_samp(out):
    v = order_values().values / 1000; r = np.random.default_rng(11); m = np.array([r.choice(v, 30).mean() for _ in range(200)]); f, ax = new(); ax.hist(m, bins=24, color=LAKE, edgecolor='white'); ax.axvline(v.mean(), color=CORAL, lw=3)
    ax.text(v.mean(), ax.get_ylim()[1] * 0.95, f' true mean {v.mean():,.1f}k', color=CORAL, fontsize=15, fontweight='bold', va='top'); ax.set_xlabel('Mean order value in a sample of 30 (UGX thousands)'); ax.set_ylabel('Number of samples'); save(f, out, 'sampling_means')

@fig('sampling_n_compare', 'Sample means for n = 5, 30 and 200 on one axis: bigger samples, narrower spread (real, seeded).', 'Three histograms of sample means for sample sizes 5, 30 and 200. The spread narrows as the sample grows.')
def f_samp_n(out):
    v = order_values().values / 1000; r = np.random.default_rng(12); f, axs = plt.subplots(1, 3, figsize=(10.5, 3.9), sharex=True)
    for ax, n in zip(axs, (5, 30, 200)):
        m = np.array([r.choice(v, n).mean() for _ in range(400)]); ax.hist(m, bins=np.linspace(20, 130, 45), color=LAKE, edgecolor='white'); ax.axvline(v.mean(), color=CORAL, lw=2.5); ax.set_title(f'n = {n}  (spread {m.std():.1f}k)'); ax.set_yticks([]); ax.set_xlim(20, 130)
    axs[1].set_xlabel('Sample mean order value (UGX thousands)'); save(f, out, 'sampling_n_compare')

@fig('footfall_orders_scatter', 'Scatter of weekly footfall vs orders per branch-week with fitted line (real).', 'Scatter plot of weekly orders against footfall for each branch-week with an upward fitted line.')
def f_foot(out):
    bw = data('branch_weeks'); f, ax = new(); ax.scatter(bw.footfall, bw.orders, s=18, color=LAKE, alpha=0.55, edgecolor='none'); b = np.polyfit(bw.footfall, bw.orders, 1); xs = np.linspace(bw.footfall.min(), bw.footfall.max(), 50); ax.plot(xs, np.polyval(b, xs), color=CORAL, lw=3)
    r = np.corrcoef(bw.footfall, bw.orders)[0, 1]; ax.text(0.04, 0.92, f'correlation r = {r:.2f}', transform=ax.transAxes, fontsize=15, fontweight='bold', color=INK); ax.set_xlabel('Footfall in the week (people through the door)'); ax.set_ylabel('Orders in the sample'); save(f, out, 'footfall_orders_scatter')

@fig('rain_orders_scatter', 'Scatter of weekly rainfall vs orders (real); a weaker, downward link.', 'Scatter plot of weekly orders against rainfall with a gently downward fitted line and a lot of scatter.')
def f_rain(out):
    bw = data('branch_weeks'); f, ax = new(); ax.scatter(bw.rainfall_mm, bw.orders, s=18, color=LAKE, alpha=0.5, edgecolor='none'); b = np.polyfit(bw.rainfall_mm, bw.orders, 1); xs = np.linspace(0, bw.rainfall_mm.max(), 50); ax.plot(xs, np.polyval(b, xs), color=CORAL, lw=3)
    r = np.corrcoef(bw.rainfall_mm, bw.orders)[0, 1]; ax.text(0.55, 0.92, f'correlation r = {r:.2f}', transform=ax.transAxes, fontsize=15, fontweight='bold'); ax.set_xlabel('Rainfall in the week (mm)'); ax.set_ylabel('Orders in the sample'); save(f, out, 'rain_orders_scatter')

@fig('confounding', 'Causal diagram: a hidden third factor (season) drives both ice-cream style sales and another measure (schematic).', 'Diagram with a hidden factor, hot weather, pointing to both ice cream sales and drownings, which look linked but are not causal.')
def f_conf(out):
    f, ax = plt.subplots(figsize=(7.2, 4.4)); ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis('off')
    box(ax, 3.5, 4.3, 3, 1.1, 'Hot weather', '#F5F3EF', GOLD, 17, True); box(ax, 0.2, 0.5, 3.2, 1.1, 'Cold drink sales', CARD, LINE, 16); box(ax, 6.6, 0.5, 3.2, 1.1, 'Swimming accidents', CARD, LINE, 16)
    arrow(ax, 4.4, 4.3, 2.2, 1.7, LAKE, 2.5); arrow(ax, 5.6, 4.3, 8.2, 1.7, LAKE, 2.5); ax.annotate('', (6.5, 1.05), (3.5, 1.05), arrowprops=dict(arrowstyle='<->', color=CORAL, lw=2.5, ls='--')); ax.text(5, 1.3, 'looks linked', ha='center', color=CORAL, fontsize=15, fontweight='bold'); ax.text(5, 0.25, 'but neither causes the other', ha='center', color=MUTED, fontsize=14); save(f, out, 'confounding')

@fig('ab_test_ci', 'Mean next-month spend, offer vs control, with 95 percent intervals (real).', 'Two bars with error bars of next-month spend for offer and control groups; the intervals nearly touch.')
def f_ab(out):
    a = data('offer_test'); f, ax = new(6.8, 4.5); xs = []
    for i, (g, c) in enumerate((('control', MUTED), ('offer', LAKE))):
        v = a[a.group == g].next_month_spend_ugx; m = v.mean(); se = v.std() / math.sqrt(len(v)); ax.bar(i, m / 1000, color=c, width=0.55); ax.errorbar(i, m / 1000, yerr=1.96 * se / 1000, color=INK, capsize=9, lw=2.5); ax.text(i, m / 1000 + 1.96 * se / 1000 + 1.5, f'{m/1000:,.1f}k', ha='center', fontsize=16, fontweight='bold')
    ax.set_xticks([0, 1]); ax.set_xticklabels(['Control', 'Offer']); ax.set_ylabel('Next-month spend (UGX thousands)'); ax.set_ylim(0, 80); save(f, out, 'ab_test_ci')

@fig('difference_ci', 'The offer lift as a difference with its 95 percent interval and a zero line (real).', 'A point with an interval showing the spend difference between offer and control, entirely to the right of zero.')
def f_diff(out):
    a = data('offer_test'); o = a[a.group == 'offer'].next_month_spend_ugx; c = a[a.group == 'control'].next_month_spend_ugx; d = o.mean() - c.mean(); se = math.sqrt(o.var() / len(o) + c.var() / len(c))
    f, ax = new(7.2, 3.4); ax.errorbar([d / 1000], [0], xerr=[[1.96 * se / 1000], [1.96 * se / 1000]], fmt='o', color=LAKE, ms=14, capsize=10, lw=3); ax.axvline(0, color=CORAL, lw=3, ls='--'); ax.text(0, 0.35, ' no difference', color=CORAL, fontsize=15, fontweight='bold')
    ax.text(d / 1000, -0.35, f'{d/1000:,.1f}k  ({(d-1.96*se)/1000:,.1f}k to {(d+1.96*se)/1000:,.1f}k)', ha='center', fontsize=16, fontweight='bold'); ax.set_ylim(-0.6, 0.6); ax.set_yticks([]); ax.spines['left'].set_visible(False); ax.set_xlabel('Offer minus control, UGX thousands per customer'); save(f, out, 'difference_ci')

@fig('pvalue_curve', 'Bell curve with the extreme tails shaded: what a p-value measures (schematic, standard normal).', 'A bell curve with both tails shaded to show the chance of a result at least this extreme if nothing is going on.')
def f_p(out):
    x = np.linspace(-4, 4, 400); y = np.exp(-x ** 2 / 2) / math.sqrt(2 * math.pi); f, ax = new(7.2, 4.2); ax.plot(x, y, color=INK, lw=2.5); t = 2.1
    ax.fill_between(x, y, where=x >= t, color=CORAL, alpha=0.6); ax.fill_between(x, y, where=x <= -t, color=CORAL, alpha=0.6); ax.fill_between(x, y, where=abs(x) < t, color='#ECE8E1'); ax.text(0, 0.05, 'if nothing is going on,\nmost results fall here', ha='center', fontsize=15)
    ax.annotate('rare tails\n= the p-value', (2.6, 0.02), (2.8, 0.18), fontsize=15, color=CORAL, fontweight='bold', arrowprops=dict(arrowstyle='-', color=CORAL)); ax.set_yticks([]); ax.set_xlabel('How far a result sits from "no effect"'); ax.spines['left'].set_visible(False); save(f, out, 'pvalue_curve')

@fig('regression_fit', 'Footfall vs orders with the least-squares line and three residuals drawn (real).', 'Scatter with a fitted line and vertical segments from three points to the line showing residuals.')
def f_reg(out):
    bw = data('branch_weeks'); f, ax = new(); ax.scatter(bw.footfall, bw.orders, s=16, color=LAKE, alpha=0.4, edgecolor='none'); b = np.polyfit(bw.footfall, bw.orders, 1); xs = np.linspace(bw.footfall.min(), bw.footfall.max(), 50); ax.plot(xs, np.polyval(b, xs), color=CORAL, lw=3)
    sub = bw.sample(3, random_state=4)
    for _, r in sub.iterrows(): ax.plot([r.footfall] * 2, [r.orders, np.polyval(b, r.footfall)], color=GOLD, lw=4); ax.scatter([r.footfall], [r.orders], s=90, color=GOLD, edgecolor=INK, zorder=5)
    ax.text(0.04, 0.9, 'gold = residual: actual minus line', transform=ax.transAxes, fontsize=15, fontweight='bold', color='#7A3418'); ax.set_xlabel('Footfall'); ax.set_ylabel('Orders'); save(f, out, 'regression_fit')

def ols(X, y):
    X1 = np.c_[np.ones(len(X)), X]; b = np.linalg.lstsq(X1, y, rcond=None)[0]; res = y - X1 @ b; s2 = res @ res / (len(y) - X1.shape[1]); cov = s2 * np.linalg.inv(X1.T @ X1); return b, np.sqrt(np.diag(cov)), res, X1 @ b

@fig('residual_plot', 'Residuals vs fitted values for the weekly orders model (real): a healthy random cloud.', 'Scatter of residuals against fitted values forming an even cloud around zero.')
def f_res(out):
    bw = data('branch_weeks'); b, se, res, fit_ = ols(bw[['footfall', 'promo_on', 'rainfall_mm']].values.astype(float), bw.orders.values.astype(float)); f, ax = new(); ax.scatter(fit_, res, s=16, color=LAKE, alpha=0.5, edgecolor='none'); ax.axhline(0, color=CORAL, lw=3)
    ax.set_xlabel('Fitted orders'); ax.set_ylabel('Residual (actual minus fitted)'); save(f, out, 'residual_plot')

@fig('coef_forest', 'Coefficients of the weekly orders model with 95 percent intervals (real, statsmodels will match).', 'Dot-and-interval plot of three regression coefficients: footfall up, promotion up, rain down.')
def f_coef(out):
    bw = data('branch_weeks'); X = bw[['footfall', 'promo_on', 'rainfall_mm']].values.astype(float); b, se, *_ = ols(X, bw.orders.values.astype(float))
    names = ['Promotion on\n(orders per week)', 'Rain\n(per extra 10 mm)', 'Footfall\n(per 1,000 people)']; est = [b[2], b[3] * 10, b[1] * 1000]; lo = [b[2] - 1.96 * se[2], (b[3] - 1.96 * se[3]) * 10, (b[1] - 1.96 * se[1]) * 1000]; hi = [b[2] + 1.96 * se[2], (b[3] + 1.96 * se[3]) * 10, (b[1] + 1.96 * se[1]) * 1000]
    f, ax = new(7.2, 4.0)
    for i, (e, l, h) in enumerate(zip(est, lo, hi)): ax.errorbar(e, i, xerr=[[e - l], [h - e]], fmt='o', color=LAKE, ms=12, capsize=8, lw=3); ax.text(h + 0.3, i + 0.18, f'{e:+.2f}', fontsize=15, fontweight='bold')
    ax.axvline(0, color=CORAL, lw=2.5, ls='--'); ax.set_yticks(range(3)); ax.set_yticklabels(names); ax.set_xlabel('Change in weekly orders (95% interval)'); save(f, out, 'coef_forest')

@fig('class_imbalance', 'Bars: loans repaid vs defaulted, showing the 87 to 13 imbalance (real).', 'Two bars showing most loans are repaid and about one in eight defaults.')
def f_imb(out):
    s = data('loans')['default'].value_counts().sort_index(); f, ax = new(6.4, 4.2); ax.bar(['Repaid', 'Defaulted'], s.values, color=[LAKE, CORAL]); [ax.text(i, v + 120, f'{v:,}\n({v/s.sum()*100:.1f}%)', ha='center', fontsize=15, fontweight='bold') for i, v in enumerate(s.values)]; ax.set_ylim(0, s.max() * 1.25); ax.set_ylabel('Loans'); save(f, out, 'class_imbalance')

@fig('default_by_occupation', 'Default rate by occupation (real).', 'Bar chart of the share of loans that default for each occupation.')
def f_occ(out):
    s = (data('loans').groupby('occupation')['default'].mean() * 100).sort_values(); f, ax = new(7.2, 4.4); ax.barh(s.index, s.values, color=LAKE); [ax.text(v + 0.2, i, f'{v:.1f}%', va='center', fontsize=14, fontweight='bold') for i, v in enumerate(s.values)]; ax.set_xlabel('Loans defaulted (%)'); ax.set_xlim(0, s.max() * 1.2); save(f, out, 'default_by_occupation')

@fig('default_by_burden', 'Default rate by repayment-burden band (instalment as a share of income) (real).', 'Bar chart showing default rate rising with repayment burden.')
def f_burden(out):
    m = loan_model(); lo = m['lo']; lo['band'] = pd.qcut(lo.burden, 5, labels=['Lowest', '2', '3', '4', 'Highest']); s = lo.groupby('band', observed=True)['default'].mean() * 100
    f, ax = new(7, 4.2); ax.bar(s.index.astype(str), s.values, color=[LAKE] * 4 + [CORAL]); [ax.text(i, v + 0.4, f'{v:.1f}%', ha='center', fontsize=15, fontweight='bold') for i, v in enumerate(s.values)]; ax.set_xlabel('Repayment burden (fifths of borrowers)'); ax.set_ylabel('Loans defaulted (%)'); ax.set_ylim(0, s.max() * 1.25); save(f, out, 'default_by_burden')

@fig('sigmoid_curve', 'The logistic S-curve turning any score into a probability, with a 0.5 threshold (schematic).', 'S-shaped curve from 0 to 1 with a dashed line at 0.5 showing where the model switches from no to yes.')
def f_sig(out):
    x = np.linspace(-6, 6, 300); f, ax = new(7.0, 4.3); ax.plot(x, sigmoid(x), color=LAKE, lw=4); ax.axhline(0.5, color=CORAL, ls='--', lw=2.5); ax.text(-5.8, 0.53, 'threshold 0.5', color=CORAL, fontsize=15, fontweight='bold'); ax.set_xlabel('Model score (any number)'); ax.set_ylabel('Probability of default'); ax.set_ylim(-0.03, 1.05); save(f, out, 'sigmoid_curve')

@fig('threshold_tradeoff', 'Precision and recall as the decision threshold moves, for the loan model (real, numpy logistic regression).', 'Two curves: recall falls and precision rises as the threshold increases.')
def f_thr(out):
    m = loan_model(); p = sigmoid(m['s']); y = m['y_te']; th = np.linspace(0.05, 0.6, 50); pr, rc = [], []
    for t in th: pred = p >= t; tp = (pred & (y == 1)).sum(); pr.append(tp / max(pred.sum(), 1)); rc.append(tp / y.sum())
    f, ax = new(7.2, 4.4); ax.plot(th, rc, color=CORAL, lw=3.5, label='Recall (defaults caught)'); ax.plot(th, pr, color=LAKE, lw=3.5, label='Precision (flags that were right)'); ax.set_xlabel('Threshold: flag a loan when probability is at least this'); ax.set_ylabel('Share'); ax.set_ylim(0, 1.02); ax.legend(loc='center right'); save(f, out, 'threshold_tradeoff')

@fig('roc_honest_vs_leaky', 'ROC curves: honest features (AUC about 0.76) vs the leaked collection_calls column (AUC about 0.99) (real, numpy logistic regression).', 'Two ROC curves. The leaky model hugs the top-left corner, far above the honest model.')
def f_roc(out):
    m = loan_model(); f, ax = new(6.4, 5.2); fp, tp = roc_pts(m['y_te'], m['s']); fl, tl = roc_pts(m['y_te'], m['sl'])
    ax.plot(fp, tp, color=LAKE, lw=3.5, label=f"Honest features  AUC {auc(m['y_te'], m['s']):.3f}"); ax.plot(fl, tl, color=CORAL, lw=3.5, label=f"With leaked column  AUC {auc(m['y_te'], m['sl']):.3f}"); ax.plot([0, 1], [0, 1], color=MUTED, ls='--', lw=2); ax.set_xlabel('False alarm rate'); ax.set_ylabel('Defaults caught (recall)'); ax.legend(loc='lower right'); save(f, out, 'roc_honest_vs_leaky')

@fig('overfit_curve', 'Train and test error as a model gets more flexible; test error eventually shoots up (real weekly orders, polynomial degree 1 to 12).', 'Two curves: training error stays low and flat as flexibility grows, while test error stays close at first and then jumps up and runs off the chart.')
def f_over(out):
    bw = data('branch_weeks'); g = bw[bw.branch_id == 'B04'].sort_values('week_start'); x = ((g.footfall - g.footfall.mean()) / g.footfall.std()).values; y = g.orders.values.astype(float)
    r = np.random.default_rng(2); idx = r.permutation(len(x)); tr, te = idx[:35], idx[35:]; deg = range(1, 13); a, b_ = [], []
    for d in deg:
        c = np.polyfit(x[tr], y[tr], d); a.append(np.sqrt(np.mean((np.polyval(c, x[tr]) - y[tr]) ** 2))); b_.append(np.sqrt(np.mean((np.polyval(c, x[te]) - y[te]) ** 2)))
    f, ax = new(7.2, 4.4); deg = list(deg)[:9]; a = a[:9]; b_ = b_[:9]; top = 40; ax.plot(deg, a, color=LAKE, lw=3.5, marker='o', label='Training error'); ax.plot(deg, np.minimum(b_, top), color=CORAL, lw=3.5, marker='o', label='Test error')
    over = [d for d, v in zip(deg, b_) if v > top]
    if over: ax.annotate('keeps climbing\noff the chart', (over[0], top), (over[0] - 2.6, top - 8), fontsize=14, color=CORAL, fontweight='bold', arrowprops=dict(arrowstyle='-|>', color=CORAL, lw=2))
    ax.set_ylim(0, top + 3); ax.set_xlabel('Model flexibility (polynomial degree)'); ax.set_ylabel('Error in orders per week'); ax.legend(loc='upper left'); save(f, out, 'overfit_curve')

@fig('feature_weights', 'Standardised weights of the honest loan model, biggest first (real, numpy logistic regression).', 'Horizontal bars of the strongest weights in the loan model: repayment burden and late payments push risk up, savings and group loans push it down.')
def f_fw(out):
    m = loan_model(); w = pd.Series(m['b'][1:], index=m['cols']).drop(['monthly_income_ugx', 'loan_amount_ugx']); w = w.reindex(w.abs().sort_values().index)[-8:]; nice = {'burden': 'Repayment burden', 'previous_late_payments': 'Earlier late payments', 'group_loan': 'Group loan', 'save_ratio': 'Savings vs loan', 'distance_to_branch_km': 'Distance to branch', 'term_months': 'Term', 'previous_loans': 'Earlier loans', 'has_mobile_money': 'Mobile money', 'savings_balance_ugx': 'Savings', 'age': 'Age'}
    f, ax = new(7.4, 4.6); ax.barh([nice.get(i, i) for i in w.index], w.values, color=[CORAL if v > 0 else LEAF for v in w.values]); ax.axvline(0, color=INK, lw=1.5); ax.set_xlabel('Weight (red raises default risk, green lowers it)'); save(f, out, 'feature_weights')

@fig('decision_tree_schematic', 'A small decision tree drawn as rules about a borrower (schematic; thresholds illustrative).', 'A three-level decision tree of yes and no questions about repayment burden, late payments and savings that ends in low, medium and high risk.')
def f_tree(out):
    f, ax = plt.subplots(figsize=(7.4, 4.8)); ax.set_xlim(0, 10); ax.set_ylim(0, 6.4); ax.axis('off')
    box(ax, 3, 5.2, 4, 1.0, 'Burden above 0.4?', '#F5F3EF', LAKE, 16, True); box(ax, 0.2, 3.1, 3.8, 1.0, 'Late before?', CARD, LINE, 16, True); box(ax, 6.0, 3.1, 3.8, 1.0, 'Savings above\n25% of loan?', CARD, LINE, 15, True)
    for (x, t, c) in ((0.0, 'Low risk', '#E7EDE4'), (2.3, 'Medium', '#F5F3EF'), (5.7, 'Medium', '#F5F3EF'), (8.0, 'High risk', '#F3E3DB')): box(ax, x, 0.7, 2.0, 1.0, t, c, LINE, 15, True)
    arrow(ax, 4.2, 5.2, 2.1, 4.1, MUTED); arrow(ax, 5.8, 5.2, 7.9, 4.1, MUTED); ax.text(2.6, 4.75, 'no', fontsize=14, color=MUTED); ax.text(7.2, 4.75, 'yes', fontsize=14, color=MUTED)
    arrow(ax, 1.4, 3.1, 1.0, 1.7, MUTED); arrow(ax, 2.8, 3.1, 3.3, 1.7, MUTED); arrow(ax, 7.0, 3.1, 6.7, 1.7, MUTED); arrow(ax, 8.6, 3.1, 9.0, 1.7, MUTED); save(f, out, 'decision_tree_schematic')

@fig('train_test_split', 'One dataset split into training and test parts (schematic bar).', 'A long bar divided into a larger training part and a smaller test part held back.')
def f_tts(out):
    f, ax = plt.subplots(figsize=(7.4, 3.0)); ax.set_xlim(0, 10); ax.set_ylim(0, 3); ax.axis('off'); ax.add_patch(Rectangle((0.2, 1.0), 7.3, 1.1, fc=LAKE)); ax.add_patch(Rectangle((7.5, 1.0), 2.3, 1.1, fc=GOLD))
    ax.text(3.85, 1.55, 'Training data: the model learns here', ha='center', va='center', color='white', fontsize=17, fontweight='bold'); ax.text(8.65, 1.55, 'Test data', ha='center', va='center', fontsize=17, fontweight='bold', color=INK); ax.text(8.65, 0.55, 'locked away until the end', ha='center', fontsize=14, color=MUTED); save(f, out, 'train_test_split')

@fig('cv_folds', 'Five-fold cross-validation: each fold takes a turn as the test part (schematic).', 'Five bars, each with a different fifth highlighted as the test fold.')
def f_cv(out):
    f, ax = plt.subplots(figsize=(7.6, 3.9)); ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis('off')
    for r in range(5):
        for c in range(5): ax.add_patch(Rectangle((1.2 + c * 1.6, 5 - r * 1.0), 1.55, 0.8, fc=GOLD if r == c else LAKE, ec='white'))
        ax.text(0.9, 5.4 - r * 1.0, f'Round {r+1}', ha='right', va='center', fontsize=14)
    ax.text(5.2, -0.05, 'blue = learn, gold = test; average the five scores', ha='center', fontsize=15, color=MUTED); save(f, out, 'cv_folds')

@fig('kmeans_segments', 'Customers on recency and spend, coloured by k-means segment (real, numpy k-means, k = 4).', 'Scatter of customers by days since last order and total spend, coloured in four segments.')
def f_km(out):
    g = rfm().copy(); X = np.c_[np.log1p(g.recency), np.log1p(g.frequency), np.log1p(g.spend)]; Z = (X - X.mean(0)) / X.std(0); lab, C, _ = kmeans(Z, 4, seed=3); g['seg'] = lab
    f, ax = new(7.2, 4.8); cols = [LAKE, GOLD, CORAL, LEAF]
    for k in range(4): s = g[g.seg == k]; ax.scatter(s.recency, s.spend / 1000, s=14, color=cols[k], alpha=0.55, edgecolor='none', label=f'Segment {k+1}')
    ax.set_yscale('log'); ax.set_xlabel('Days since last order'); ax.set_ylabel('Total spend (UGX thousands, log scale)'); ax.legend(markerscale=2.5, loc='upper right'); save(f, out, 'kmeans_segments')

@fig('elbow_plot', 'Within-cluster spread against k for customer segments, to choose k (real, numpy k-means).', 'Line chart of within-cluster error falling as the number of clusters grows, with a bend near four.')
def f_elbow(out):
    g = rfm(); X = np.c_[np.log1p(g.recency), np.log1p(g.frequency), np.log1p(g.spend)]; Z = (X - X.mean(0)) / X.std(0); ks = range(1, 9); inn = [min(kmeans(Z, k, seed=s)[2] for s in range(3)) for k in ks]
    f, ax = new(); ax.plot(list(ks), inn, color=LAKE, lw=3.5, marker='o', ms=9); ax.set_xlabel('Number of clusters k'); ax.set_ylabel('Total within-cluster spread'); ax.scatter([4], [inn[3]], s=250, facecolor='none', edgecolor=CORAL, lw=3); save(f, out, 'elbow_plot')

@fig('pca_view', 'Customer features flattened to two axes with PCA, coloured by segment (real, numpy SVD).', 'Scatter of customers on two principal components, coloured by segment, showing separated groups.')
def f_pca(out):
    g = rfm(); X = np.c_[np.log1p(g.recency), np.log1p(g.frequency), np.log1p(g.spend)]; Z = (X - X.mean(0)) / X.std(0); lab, _, _ = kmeans(Z, 4, seed=3); U, S, Vt = np.linalg.svd(Z, full_matrices=False); P = Z @ Vt[:2].T; ev = S ** 2 / (S ** 2).sum()
    f, ax = new(7.0, 4.8); cols = [LAKE, GOLD, CORAL, LEAF]
    for k in range(4): ax.scatter(P[lab == k, 0], P[lab == k, 1], s=14, color=cols[k], alpha=0.55, edgecolor='none')
    ax.set_xlabel(f'Axis 1 ({ev[0]*100:.0f}% of the variation)'); ax.set_ylabel(f'Axis 2 ({ev[1]*100:.0f}%)'); save(f, out, 'pca_view')

@fig('segment_profile', 'Average recency, frequency and spend per segment, scaled 0 to 1 (real, numpy k-means).', 'Grouped bars comparing recency, frequency and spend across four customer segments.')
def f_seg(out):
    g = rfm().copy(); X = np.c_[np.log1p(g.recency), np.log1p(g.frequency), np.log1p(g.spend)]; Z = (X - X.mean(0)) / X.std(0); lab, _, _ = kmeans(Z, 4, seed=3); g['seg'] = lab; p = g.groupby('seg')[['recency', 'frequency', 'spend']].mean(); p = (p - p.min()) / (p.max() - p.min())
    f, ax = new(7.6, 4.5); w = 0.25; cols = [CORAL, LAKE, GOLD]
    for j, c in enumerate(p.columns): ax.bar(np.arange(4) + (j - 1) * w, p[c], w, color=cols[j], label=c.capitalize())
    ax.set_xticks(range(4)); ax.set_xticklabels([f'Segment {i+1}' for i in range(4)]); ax.set_ylabel('Relative level (0 to 1)'); ax.legend(ncol=3, loc='upper center', bbox_to_anchor=(0.5, 1.12)); save(f, out, 'segment_profile')

@fig('clinic_season', 'Malaria cases by calendar month across all districts (real).', 'Bar chart of malaria cases for each month with peaks after the two rainy seasons.')
def f_cs(out):
    c = data('clinic_visits'); s = c.groupby(pd.to_datetime(c.month).dt.month).malaria_cases.sum() / 1000; f, ax = new(7.6, 4.3); ax.bar(range(12), s.values, color=[GOLD if v == s.max() else LAKE for v in s.values]); ax.set_xticks(range(12)); ax.set_xticklabels(list('JFMAMJJASOND')); ax.set_ylabel('Cases (thousands, all districts, 5 years)'); ax.set_xlabel('Month'); save(f, out, 'clinic_season')

@fig('rain_lag_scatter', 'Malaria cases against rainfall in the same month and the month before (real); the lag fits better.', 'Two scatter plots. Same-month rainfall shows no pattern; last month rainfall shows an upward pattern.')
def f_lag(out):
    c = data('clinic_visits').copy(); c['lag'] = c.groupby('district').rainfall_mm.shift(1); cc = c.dropna(subset=['lag']); f, axs = plt.subplots(1, 2, figsize=(10.5, 4.3), sharey=True)
    for ax, col, t in zip(axs, ('rainfall_mm', 'lag'), ('Rain in the same month', 'Rain in the month before')):
        ax.scatter(cc[col], cc.malaria_cases / 1000, s=12, color=LAKE, alpha=0.4, edgecolor='none'); b = np.polyfit(cc[col], cc.malaria_cases / 1000, 1); xs = np.linspace(0, cc[col].max(), 20); ax.plot(xs, np.polyval(b, xs), color=CORAL, lw=3); ax.set_title(f"{t}\nr = {cc[col].corr(cc.malaria_cases):.2f}"); ax.set_xlabel('Rainfall (mm)')
    axs[0].set_ylabel('Malaria cases (thousands)'); save(f, out, 'rain_lag_scatter')

@fig('ts_decomposition', 'Trend, seasonal pattern and leftover noise of total monthly malaria cases (real).', 'Three stacked panels showing a rising trend, a repeating yearly pattern and small leftover noise.')
def f_dec(out):
    c = data('clinic_visits'); s = c.groupby('month').malaria_cases.sum() / 1000; v = s.values; trend = pd.Series(v).rolling(12, center=True).mean().values; det = v - trend
    seas = np.array([np.nanmean(det[i::12]) for i in range(12)]); seas_full = np.tile(seas, 5); noise = v - trend - seas_full
    f, axs = plt.subplots(3, 1, figsize=(7.6, 5.2), sharex=True)
    for ax, y, t, col in zip(axs, (trend, seas_full, noise), ('Trend', 'Season', 'Noise'), (LAKE, GOLD, MUTED)): ax.plot(np.arange(60), y, color=col, lw=2.5); ax.set_ylabel(t, rotation=0, ha='right', va='center', fontsize=15, fontweight='bold')
    axs[2].set_xlabel('Months since January 2021'); save(f, out, 'ts_decomposition')

@fig('clinic_forecast', 'Seasonal-naive forecast against actual for the last 12 months of one district, with MAE (real).', 'Line chart with actual cases and a seasonal-naive forecast that repeats last year, closely following the pattern.')
def f_fc(out):
    c = data('clinic_visits'); g = c[c.district == 'Mbarara'].sort_values('month'); y = g.malaria_cases.values; ac = y[-12:]; fc = y[-24:-12]; mae = np.abs(ac - fc).mean()
    f, ax = new(7.6, 4.4); ax.plot(range(1, 13), ac, color=LAKE, lw=3.5, marker='o', label='Actual 2025'); ax.plot(range(1, 13), fc, color=CORAL, lw=3.5, ls='--', marker='s', label='Forecast: same month last year'); ax.set_xticks(range(1, 13)); ax.set_xticklabels(list('JFMAMJJASOND'))
    ax.set_ylabel('Malaria cases, Mbarara'); ax.legend(loc='upper left'); ax.text(0.02, 0.80, f'average miss {mae:,.0f} cases', transform=ax.transAxes, ha='left', fontsize=15, fontweight='bold'); save(f, out, 'clinic_forecast')

@fig('time_split', 'Time-ordered train and test split for a time series (schematic).', 'A timeline where the early months are training data and the later months are the test data.')
def f_ts(out):
    f, ax = plt.subplots(figsize=(7.6, 2.9)); ax.set_xlim(0, 10); ax.set_ylim(0, 3); ax.axis('off'); ax.add_patch(Rectangle((0.2, 1.0), 6.6, 1.0, fc=LAKE)); ax.add_patch(Rectangle((6.8, 1.0), 3.0, 1.0, fc=GOLD))
    ax.text(3.5, 1.5, 'Train: the past', ha='center', va='center', color='white', fontsize=17, fontweight='bold'); ax.text(8.3, 1.5, 'Test: the future', ha='center', va='center', fontsize=17, fontweight='bold'); ax.annotate('', (9.8, 0.55), (0.2, 0.55), arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=2)); ax.text(5, 0.1, 'time', ha='center', color=MUTED, fontsize=15); save(f, out, 'time_split')

@fig('activation_functions', 'Sigmoid, tanh and ReLU curves side by side (schematic).', 'Three small plots of the sigmoid, tanh and ReLU activation functions.')
def f_act(out):
    x = np.linspace(-5, 5, 300); f, axs = plt.subplots(1, 3, figsize=(10.2, 3.5), sharex=True)
    for ax, y, t in zip(axs, (sigmoid(x), np.tanh(x), np.maximum(0, x)), ('Sigmoid', 'Tanh', 'ReLU')): ax.plot(x, y, color=LAKE, lw=3.5); ax.axhline(0, color=LINE, lw=1); ax.axvline(0, color=LINE, lw=1); ax.set_title(t)
    save(f, out, 'activation_functions')

@fig('nn_diagram', 'A small feed-forward network: inputs, two hidden layers, one output (schematic).', 'Diagram of a neural network with three input nodes, two hidden layers of four nodes and one output node, all connected.')
def f_nn(out):
    f, ax = plt.subplots(figsize=(7.6, 4.6)); ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis('off'); layers = [3, 4, 4, 1]; xs = [1.2, 3.8, 6.4, 8.8]; pos = []
    for n, x in zip(layers, xs): pos.append([(x, 3 + (i - (n - 1) / 2) * 1.15) for i in range(n)])
    for a, b in zip(pos[:-1], pos[1:]):
        for (x1, y1) in a:
            for (x2, y2) in b: ax.plot([x1, x2], [y1, y2], color=LINE, lw=1.2, zorder=1)
    for li, L in enumerate(pos):
        for (x, y) in L: ax.add_patch(Circle((x, y), 0.34, fc=[PALE if False else '#F5F3EF', '#ECE8E1', '#ECE8E1', '#F5F3EF'][li], ec=LAKE if li < 3 else GOLD, lw=2.5, zorder=3))
    for x, t in zip(xs, ('Inputs', 'Hidden layer 1', 'Hidden layer 2', 'Output')): ax.text(x, 5.55, t, ha='center', fontsize=14, fontweight='bold')
    save(f, out, 'nn_diagram')

@fig('text_map', 'Customer feedback messages placed in 2D from their word counts (real TF-IDF + SVD), coloured by sentiment.', 'Scatter of customer messages positioned by word usage, with positive, negative and neutral messages forming loose groups.')
def f_text(out):
    fb = data('feedback'); import re
    toks = [re.findall(r"[a-z']+", m.lower()) for m in fb.message]; vocab = sorted({w for t in toks for w in t}); ix = {w: i for i, w in enumerate(vocab)}
    M = np.zeros((len(toks), len(vocab)))
    for i, t in enumerate(toks):
        for w in t: M[i, ix[w]] += 1
    df = (M > 0).sum(0); idf = np.log((1 + len(M)) / (1 + df)) + 1; T = M * idf; T /= np.linalg.norm(T, axis=1, keepdims=True) + 1e-9; U, S, Vt = np.linalg.svd(T - T.mean(0), full_matrices=False); P = U[:, :2] * S[:2]
    f, ax = new(7.0, 4.8)
    for s, c in (('positive', LEAF), ('negative', CORAL), ('neutral', MUTED)): m = (fb.sentiment == s).values; ax.scatter(P[m, 0], P[m, 1], s=40, color=c, alpha=0.5, edgecolor='none', label=s)
    lo, hi = np.percentile(P, [1, 99], axis=0); ax.set_xlim(lo[0] - 0.05, hi[0] + 0.05); ax.set_ylim(lo[1] - 0.05, hi[1] + 0.05); ax.legend(markerscale=2.5); ax.set_xlabel('Axis 1'); ax.set_ylabel('Axis 2'); ax.set_xticks([]); ax.set_yticks([]); save(f, out, 'text_map')

@fig('dataframe_anatomy', 'Head of the orders table with its parts named: columns, rows, index, one cell (real values).', 'A small table of the first orders with arrows naming the column names, row index and a single cell.')
def f_anat(out):
    od = data('orders').head(5); f, ax = plt.subplots(figsize=(7.6, 4.6)); ax.axis('off'); cols = ['order_id', 'order_date', 'branch_id', 'payment_method']; ax.set_xlim(0, 10); ax.set_ylim(0, 6)
    x0, y0, cw, rh = 1.2, 4.3, 2.1, 0.62
    for j, c in enumerate(cols): ax.add_patch(Rectangle((x0 + j * cw, y0), cw, rh, fc=INK)); ax.text(x0 + j * cw + cw / 2, y0 + rh / 2, c, color='white', ha='center', va='center', fontsize=13, fontweight='bold')
    for i in range(5):
        ax.add_patch(Rectangle((0.2, y0 - (i + 1) * rh), 1.0, rh, fc='#F5F3EF', ec=LINE)); ax.text(0.7, y0 - (i + 0.5) * rh, str(i), ha='center', va='center', fontsize=13)
        for j, c in enumerate(cols): ax.add_patch(Rectangle((x0 + j * cw, y0 - (i + 1) * rh), cw, rh, fc='white' if i % 2 else CARD, ec=LINE)); ax.text(x0 + j * cw + cw / 2, y0 - (i + 0.5) * rh, str(od.iloc[i][c]), ha='center', va='center', fontsize=13)
    ax.add_patch(Rectangle((x0 + 2 * cw, y0 - 5 * rh), cw, rh, fc='none', ec=CORAL, lw=3)); ax.annotate('one cell', (x0 + 2.5 * cw, y0 - 5 * rh), (x0 + 2.5 * cw, 0.45), fontsize=15, color=CORAL, fontweight='bold', ha='center', arrowprops=dict(arrowstyle='-|>', color=CORAL, lw=2))
    ax.annotate('index\n(row label)', (0.7, y0 - 5 * rh), (0.7, 0.45), fontsize=14, color=LAKE, fontweight='bold', ha='center', arrowprops=dict(arrowstyle='-|>', color=LAKE, lw=2)); ax.annotate('column names', (x0 + 1.5 * cw, y0 + rh), (x0 + 1.5 * cw, 5.5), fontsize=15, color=LAKE, fontweight='bold', ha='center', arrowprops=dict(arrowstyle='-|>', color=LAKE, lw=2)); save(f, out, 'dataframe_anatomy')

@fig('split_apply_combine', 'GROUP BY as split, apply, combine, drawn with real branch totals (schematic of real numbers).', 'Diagram: a table is split into groups by branch, each group is summed, and the sums combine into a small result table.')
def f_sac(out):
    od = data('orders').assign(v=lambda d: d.order_id.map(order_values())); t = (od.groupby('branch_id').v.sum() / 1e6).round(0).astype(int); f, ax = plt.subplots(figsize=(8.0, 4.2)); ax.set_xlim(0, 12); ax.set_ylim(0, 6); ax.axis('off')
    box(ax, 0.1, 1.3, 2.4, 3.4, 'All orders\n\none big table', CARD, LINE, 16, True)
    for i, b in enumerate(['B01', 'B02', 'B03']): box(ax, 4.0, 4.2 - i * 1.4, 2.4, 1.0, f'rows of {b}', '#F5F3EF', LAKE, 15, True); arrow(ax, 2.6, 3.0, 3.9, 4.7 - i * 1.4, MUTED); box(ax, 7.5, 4.2 - i * 1.4, 1.6, 1.0, f'sum {t[b]}M', '#F5F3EF', GOLD, 15, True); arrow(ax, 6.5, 4.7 - i * 1.4, 7.4, 4.7 - i * 1.4, MUTED)
    ax.text(5.2, 5.55, 'split', ha='center', fontsize=16, fontweight='bold', color=LAKE); ax.text(8.3, 5.55, 'apply', ha='center', fontsize=16, fontweight='bold', color='#7A3418'); ax.text(11.0, 5.55, 'combine', ha='center', fontsize=16, fontweight='bold', color=INK); box(ax, 9.8, 1.8, 2.0, 2.6, 'one row\nper branch', INK, INK, 15, True, 'white')
    for i in range(3): arrow(ax, 9.2, 4.7 - i * 1.4, 9.7, 3.4, MUTED)
    save(f, out, 'split_apply_combine')

@fig('join_types', 'Four join types as overlapping circles with the rows each keeps (schematic).', 'Four small Venn diagrams for inner, left, right and outer joins with the kept area shaded.')
def f_join(out):
    f, axs = plt.subplots(1, 4, figsize=(11, 3.4)); names = ['Inner', 'Left', 'Right', 'Full outer']
    for ax, n in zip(axs, names):
        ax.set_xlim(0, 4); ax.set_ylim(0, 3); ax.axis('off'); a = Circle((1.5, 1.5), 1.0, fc='none', ec=LAKE, lw=3); b = Circle((2.5, 1.5), 1.0, fc='none', ec=GOLD, lw=3)
        if n in ('Left', 'Full outer'): ax.add_patch(Circle((1.5, 1.5), 1.0, fc=LAKE, alpha=0.35, ec='none'))
        if n in ('Right', 'Full outer'): ax.add_patch(Circle((2.5, 1.5), 1.0, fc=GOLD, alpha=0.35, ec='none'))
        if n == 'Inner': ax.add_patch(Circle((1.5, 1.5), 1.0, fc=CORAL, alpha=0.0))
        ax.add_patch(a); ax.add_patch(b); ax.set_title(n, fontsize=16); ax.text(0.8, 1.5, 'A', fontsize=16, fontweight='bold', color=LAKE, ha='center'); ax.text(3.2, 1.5, 'B', fontsize=16, fontweight='bold', color='#7A3418', ha='center')
        if n == 'Inner': import matplotlib.patches as mp; lens = Ellipse((2.0, 1.5), 1.0, 1.7, fc=CORAL, alpha=0.5, ec='none'); ax.add_patch(lens)
    save(f, out, 'join_types')

@fig('join_doubling', 'Why a join can double revenue: one order row matched to two rows (schematic with real-looking IDs).', 'Two small tables joined on order_id where a duplicate key in the second table produces two result rows for one order.')
def f_jd(out):
    f, ax = plt.subplots(figsize=(8.2, 4.4)); ax.set_xlim(0, 12); ax.set_ylim(0, 6); ax.axis('off'); box(ax, 0.2, 3.4, 3.2, 1.8, 'orders\nO001  UGX 50,000', '#F5F3EF', LAKE, 15, True); box(ax, 0.2, 0.7, 3.2, 1.8, 'promo_log\nO001  Mon\nO001  Tue', '#F5F3EF', GOLD, 15, True)
    arrow(ax, 3.5, 4.3, 5.2, 3.2, MUTED); arrow(ax, 3.5, 1.6, 5.2, 2.7, MUTED); ax.text(4.35, 3.0, 'join on\norder_id', ha='center', fontsize=14, color=MUTED)
    box(ax, 5.4, 2.0, 4.2, 2.2, 'result\nO001  50,000  Mon\nO001  50,000  Tue', '#F3E3DB', CORAL, 15, True); ax.text(9.9, 3.1, '= 100,000?', fontsize=19, fontweight='bold', color=CORAL, va='center'); ax.text(7.5, 1.2, 'The order is now counted twice.', ha='center', fontsize=15, color=CORAL, fontweight='bold'); save(f, out, 'join_doubling')

@fig('sql_order', 'The order SQL is written in versus the order it runs (schematic).', 'Two lists side by side: the written order of SQL clauses and the order the database actually runs them.')
def f_sqlo(out):
    f, ax = plt.subplots(figsize=(8.0, 4.6)); ax.set_xlim(0, 12); ax.set_ylim(0, 7); ax.axis('off'); W_ = ['SELECT', 'FROM', 'WHERE', 'GROUP BY', 'HAVING', 'ORDER BY']; R = ['FROM', 'WHERE', 'GROUP BY', 'HAVING', 'SELECT', 'ORDER BY']
    ax.text(2.2, 6.5, 'You write', ha='center', fontsize=17, fontweight='bold', color=LAKE); ax.text(9.0, 6.5, 'The database runs', ha='center', fontsize=17, fontweight='bold', color='#7A3418')
    for i, (a, b) in enumerate(zip(W_, R)): y = 5.4 - i * 0.95; box(ax, 0.6, y, 3.2, 0.75, a, '#F5F3EF', LAKE, 16, True); box(ax, 7.4, y, 3.2, 0.75, b, '#F5F3EF', GOLD, 16, True); ax.text(5.6, y + 0.37, f'{i+1}', ha='center', va='center', fontsize=15, color=MUTED)
    save(f, out, 'sql_order')

@fig('ml_workflow', 'The machine learning workflow as a loop (schematic).', 'A loop of steps: question, data, features, split, train, evaluate, then improve or deliver.')
def f_mlw(out):
    f, ax = plt.subplots(figsize=(7.6, 4.6)); ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis('off'); steps = ['Question', 'Data', 'Features', 'Split', 'Train', 'Evaluate']; pts = [(1.4, 4.6), (4.1, 4.6), (6.8, 4.6), (6.8, 1.6), (4.1, 1.6), (1.4, 1.6)]
    for (x, y), s in zip(pts, steps): box(ax, x - 1.0, y - 0.5, 2.1, 1.0, s, '#F5F3EF' if s != 'Evaluate' else '#F5F3EF', LAKE if s != 'Evaluate' else GOLD, 17, True)
    for a, b in zip(range(5), range(1, 6)): (x1, y1), (x2, y2) = pts[a], pts[b]; arrow(ax, x1 + (1.1 if x2 > x1 else (-1.1 if x2 < x1 else 0)), y1 + (-0.55 if y2 < y1 else 0), x2 - (1.1 if x2 > x1 else (-1.1 if x2 < x1 else 0)), y2 + (0.55 if y2 < y1 else 0))
    arrow(ax, 1.4, 2.2, 1.4, 4.0, CORAL); ax.text(0.9, 3.1, 'repeat', fontsize=14, color=CORAL, ha='right', fontweight='bold'); save(f, out, 'ml_workflow')

@fig('sklearn_pipeline', 'A scikit-learn Pipeline as connected blocks (schematic).', 'Blocks in a row: impute missing values, scale numbers, encode categories, then fit a model, all packed into one pipeline.')
def f_pipe(out):
    f, ax = plt.subplots(figsize=(8.4, 3.6)); ax.set_xlim(0, 14); ax.set_ylim(0, 5); ax.axis('off'); items = [('Impute\nmissing', '#F5F3EF'), ('Scale\nnumbers', '#F5F3EF'), ('Encode\ncategories', '#F5F3EF'), ('Model', '#F5F3EF')]
    ax.add_patch(FancyBboxPatch((0.1, 0.5), 13.6, 3.6, boxstyle='round,pad=0.02,rounding_size=0.2', fc='none', ec=LAKE, lw=2.5, ls='--'))
    for i, (t, c) in enumerate(items): box(ax, 0.6 + i * 3.3, 1.3, 2.7, 1.9, t, c, LAKE if i < 3 else GOLD, 17, True)
    for i in range(3): arrow(ax, 3.4 + i * 3.3, 2.25, 3.9 + i * 3.3, 2.25)
    ax.text(7, 4.4, 'Pipeline: the same steps in the same order, for training and for new data', ha='center', fontsize=15, fontweight='bold', color=LAKE); save(f, out, 'sklearn_pipeline')

@fig('drift_chart', 'Average borrower income over time with a shift that makes an old model go stale (schematic, simulated).', 'Line chart of a monthly average that is steady and then drops, with a label showing the point where the model should be re-checked.')
def f_drift(out):
    r = np.random.default_rng(8); y = np.r_[r.normal(100, 3, 18), r.normal(88, 3, 12)]; y = np.r_[y[:18], y[18:]]; f, ax = new(7.6, 4.2); ax.plot(range(1, 31), y, color=LAKE, lw=3.5, marker='o'); ax.axvline(18.5, color=CORAL, ls='--', lw=2.5); ax.text(18.9, y.max() - 1, 'inputs shift:\ncheck the model', color=CORAL, fontsize=15, fontweight='bold', va='top')
    ax.set_xlabel('Month since launch'); ax.set_ylabel('Average income of applicants (index)'); save(f, out, 'drift_chart')

@fig('rag_pipeline', 'Retrieval before answering: question, search the documents, pass the best passages to the model (schematic).', 'Pipeline: a question becomes a vector, the closest document passages are found, and a language model answers using only those passages.')
def f_rag(out):
    f, ax = plt.subplots(figsize=(8.6, 3.8)); ax.set_xlim(0, 14); ax.set_ylim(0, 5); ax.axis('off'); items = [('Question', CARD), ('Turn into\nnumbers', '#F5F3EF'), ('Find closest\npassages', '#F5F3EF'), ('Language\nmodel', '#F5F3EF'), ('Answer\n+ source', '#E7EDE4')]
    for i, (t, c) in enumerate(items): box(ax, 0.2 + i * 2.8, 1.6, 2.3, 1.8, t, c, LINE, 16, True)
    for i in range(4): arrow(ax, 2.55 + i * 2.8, 2.5, 3.0 + i * 2.8, 2.5)
    box(ax, 5.8, 0.1, 2.3, 0.9, 'Your documents', '#F5F3EF', LINE, 14); arrow(ax, 6.95, 1.0, 6.95, 1.55, LAKE); save(f, out, 'rag_pipeline')

@fig('embedding_idea', 'Meaning as position: similar phrases sit close together on a 2D map (schematic with example phrases).', 'A two-dimensional map where phrases about queues sit near each other, away from phrases about prices and about payment.')
def f_emb(out):
    f, ax = plt.subplots(figsize=(7.4, 4.8)); ax.set_xlim(0, 10); ax.set_ylim(0, 6.5); ax.set_xticks([]); ax.set_yticks([]); ax.spines['left'].set_visible(False); ax.spines['bottom'].set_visible(False)
    groups = [('queue', LAKE, [(2.0, 4.8, 'long queue at the till'), (1.4, 3.9, 'waited twenty minutes'), (2.6, 3.7, 'slow checkout')]), ('price', GOLD, [(7.2, 4.9, 'prices keep going up'), (8.0, 4.0, 'too expensive'), (6.3, 3.3, 'cheaper elsewhere')]), ('pay', CORAL, [(4.6, 1.6, 'mobile money failed'), (3.4, 0.9, 'charged twice'), (5.8, 0.8, 'payment error')])]
    for n, c, pts in groups:
        for x, y, t in pts: ax.scatter([x], [y], s=190, color=c, edgecolor=INK, zorder=3); ax.text(x + 0.18, y + 0.2, t, fontsize=14, ha='left' if x < 7.5 else 'right')
    save(f, out, 'embedding_idea')

@fig('token_example', 'A sentence cut into tokens with made-up token numbers (schematic, labelled illustrative).', 'A sentence split into word and word-piece boxes, each with an identification number underneath.')
def f_tok(out):
    f, ax = plt.subplots(figsize=(8.4, 2.8)); ax.set_xlim(0, 14); ax.set_ylim(0, 4); ax.axis('off'); toks = ['The', ' pro', 'vider', ' remains', ' liable', '.']; ids = [101, 5873, 9921, 4417, 8202, 13]; x = 0.3
    for t, i in zip(toks, ids): w = 0.2 * max(len(t), 3) + 0.6; box(ax, x, 1.9, w, 1.1, t.replace(' ', '␣') if False else t, '#F5F3EF', LAKE, 17, True); ax.text(x + w / 2, 1.35, str(i), ha='center', fontsize=15, color=CORAL, fontweight='bold'); x += w + 0.25
    ax.text(0.3, 0.45, 'Token numbers here are illustrative.', fontsize=14, color=MUTED); save(f, out, 'token_example')

@fig('learning_path', 'A six-month learning path after the course, from practice to portfolio (schematic).', 'Three-step path with months one to two, three to four and five to six listing practice, depth and portfolio goals.')
def f_path(out):
    f, ax = plt.subplots(figsize=(9.0, 3.8)); ax.set_xlim(0, 14); ax.set_ylim(0, 5); ax.axis('off'); items = [('Months 1 to 2', 'Repeat the labs on new data. Kaggle Learn: Pandas and Data Cleaning'), ('Months 3 to 4', 'Go deeper in one area. Google ML Crash Course or fast.ai'), ('Months 5 to 6', 'Publish two projects on GitHub and one deployed app')]
    for i, (a, b) in enumerate(items): box(ax, 0.3 + i * 4.6, 0.5, 4.2, 3.4, '', '#F5F3EF' if i < 2 else '#F5F3EF', LAKE if i < 2 else GOLD); ax.text(2.4 + i * 4.6, 3.3, a, ha='center', fontsize=20, fontweight='bold', color=INK); ax.text(2.4 + i * 4.6, 1.8, '\n'.join(__import__('textwrap').wrap(b, 24)), ha='center', va='center', fontsize=16)
    for i in range(2): arrow(ax, 4.55 + i * 4.6, 2.2, 4.85 + i * 4.6, 2.2)
    save(f, out, 'learning_path')

@fig('missing_by_column', 'Count of missing values per column in the loans file (real).', 'Bar chart of missing values per column; only monthly income has missing entries.')
def f_miss(out):
    lo = data('loans'); s = lo.isna().sum(); s = s[s > 0]; f, ax = new(6.4, 3.6); ax.barh(s.index, s.values, color=CORAL, height=0.35); [ax.text(v + 5, i, f'{v}', va='center', fontsize=15, fontweight='bold') for i, v in enumerate(s.values)]; ax.set_xlabel('Missing values'); ax.set_xlim(0, s.max() * 1.2); save(f, out, 'missing_by_column')

@fig('chart_choice', 'Which chart for which question (schematic of four mini charts).', 'Four mini charts with labels: histogram for one number, bar for a comparison, line for change over time, scatter for two numbers.')
def f_cc(out):
    r = np.random.default_rng(1); f, axs = plt.subplots(1, 4, figsize=(11.2, 3.3))
    axs[0].hist(r.lognormal(0, .5, 400), bins=18, color=LAKE, edgecolor='white'); axs[0].set_title('Histogram\none number'); axs[1].bar(list('ABCD'), [5, 8, 3, 6], color=LAKE); axs[1].set_title('Bar\ncompare groups'); axs[2].plot(np.cumsum(r.normal(1, 1, 24)), color=LAKE, lw=3); axs[2].set_title('Line\nchange over time')
    x = r.normal(0, 1, 120); axs[3].scatter(x, x + r.normal(0, .6, 120), s=12, color=LAKE); axs[3].set_title('Scatter\ntwo numbers'); [a.set_xticks([]) for a in axs]; [a.set_yticks([]) for a in axs]; save(f, out, 'chart_choice')

@fig('loop_vs_fill', 'Python loop beside fill-down (schematic).', 'Left: a spreadsheet column with a formula dragged down. Right: a Python for loop doing the same for each item.')
def f_loop(out):
    f, ax = plt.subplots(figsize=(8.2, 3.9)); ax.set_xlim(0, 12); ax.set_ylim(0, 6); ax.axis('off'); ax.text(2.0, 5.5, 'Spreadsheet', fontsize=17, fontweight='bold', color=LAKE, ha='center'); ax.text(9.0, 5.5, 'Python', fontsize=17, fontweight='bold', color='#7A3418', ha='center')
    for i in range(4): box(ax, 0.4, 4.2 - i * 1.0, 3.2, 0.8, f'=B{i+2}*C{i+2}', '#F5F3EF', LAKE, 15, True)
    arrow(ax, 4.0, 3.0, 6.2, 3.0, MUTED); box(ax, 6.4, 1.2, 5.2, 3.6, 'for row in rows:\n    total = qty * price', '#1F2328', '#1F2328', 19, False, '#F3F0EA'); save(f, out, 'loop_vs_fill')

# ---- hero art for title slides (dark background, transparent)
def hero(mod, out, seed=0):
    r = np.random.default_rng(seed + ord(mod)); f, ax = plt.subplots(figsize=(5.2, 5.2)); ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis('off'); f.patch.set_alpha(0); ax.patch.set_alpha(0)
    L, G, W_ = '#5BB6D0', '#F2A900', '#C9D4E8'
    if mod == 'A':
        for i in range(6):
            for j in range(5): hl = (i + j * 2 + seed) % 7 == 0; ax.add_patch(Rectangle((1 + i * 1.3, 1.5 + j * 1.5), 1.2, 1.35, fc=G if hl else 'none', ec=L, lw=2.5, alpha=0.9 if hl else 0.7))
    elif mod == 'B':
        for i in range(8): ax.add_patch(Rectangle((1.2, 8 - i), r.uniform(2, 6.5), 0.45, fc=L if i % 3 else G, alpha=0.85))
        ax.add_patch(Rectangle((5.8, 1.2), 3.4, 3.0, fc='none', ec=W_, lw=2.5)); [ax.plot([5.8, 9.2], [1.2 + k * 0.75] * 2, color=W_, lw=1.5) for k in range(1, 4)]
    elif mod == 'C':
        xs = np.arange(7); ax.bar(xs * 1.2 + 1.1, r.uniform(2, 7.5, 7), 0.8, color=L, alpha=0.85); ax.plot(xs * 1.2 + 1.5, r.uniform(3, 8, 7), color=G, lw=4, marker='o', ms=9)
    elif mod == 'D':
        a = r.normal([3.2, 3.5], 1.0, (45, 2)); b = r.normal([6.8, 6.5], 1.0, (45, 2)); ax.scatter(a[:, 0], a[:, 1], s=90, color=L, alpha=0.9); ax.scatter(b[:, 0], b[:, 1], s=90, color=G, alpha=0.9); ax.plot([1.5, 8.8], [8.4, 1.6], color=W_, lw=3, ls='--')
    elif mod == 'E':
        ls = [3, 5, 5, 2]; pos = [[(1.6 + 2.2 * k, 5 + (i - (n - 1) / 2) * 1.35) for i in range(n)] for k, n in enumerate(ls)]
        for a_, b_ in zip(pos[:-1], pos[1:]):
            for p in a_:
                for q in b_: ax.plot([p[0], q[0]], [p[1], q[1]], color='#6A6F75', lw=1.1, zorder=1)
        for k, Lr in enumerate(pos):
            for p in Lr: ax.add_patch(Circle(p, 0.36, fc=G if k == 3 else L, ec='none', zorder=3))
    else:
        ax.plot([1.2, 3.4, 5.2, 7.4, 8.8], [1.6, 3.2, 3.0, 6.2, 8.4], color=L, lw=5); [ax.scatter([x], [y], s=240, color=G if i == 4 else W_, zorder=3) for i, (x, y) in enumerate(zip([1.2, 3.4, 5.2, 7.4, 8.8], [1.6, 3.2, 3.0, 6.2, 8.4]))]; ax.plot([8.8, 8.8], [8.4, 9.4], color=G, lw=4); ax.add_patch(Polygon([[8.8, 9.4], [9.9, 9.1], [8.8, 8.8]], fc=G))
    f.savefig(Path(out) / f'hero_{mod}.png', transparent=True, dpi=200); plt.close(f)

def main(data_dir, out_dir):
    global DATA; DATA = data_dir; out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    for name, (desc, alt, fn) in CAT.items(): fn(out)
    cat = {n: dict(description=d, alt=a) for n, (d, a, _) in CAT.items()}
    (out / 'catalog.json').write_text(json.dumps(cat, indent=1, ensure_ascii=False), encoding='utf-8')
    print(len(cat), 'figures written to', out)

DATA = None
if __name__ == '__main__': main(sys.argv[1], sys.argv[2])
