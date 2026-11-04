"""Session 18 lab: finding structure without labels on the Lakeside Mart loyalty customers (author i).

Expected values come from content/s18_facts.py (NumPy: RFM in pandas, k-means with a k-means++ start, PCA by singular value decomposition, an isolation forest). The pandas steps match exactly.
PCA matches scikit-learn exactly (up to the sign of a component). KMeans matches on the inertia and closely on the segment sizes, so those checks allow the spread we measured over 60 random starts.
IsolationForest uses random numbers: the number flagged is set by the contamination (arithmetic), and the nature of the flagged customers is checked loosely.
NEEDS lists the libraries the sandbox lacks: the runner then proves only that every cell compiles and prints UNVERIFIED."""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parents[1] / 'kit'))
import nb as NB  # noqa: E402
import s18_facts as SF  # noqa: E402

TITLE = 'Finding structure without labels'
NEEDS = ['sklearn']


def build(solution: bool):
    F = SF.facts()
    st = F['rfm_stats']
    inert = F['inertia']
    rng = F['k4_size_range']
    pr = F['profile']
    ratio = F['pca']['ratio']
    rule = F['rule']
    iso = F['iso']
    nb = NB.Notebook()

    def cell(sol, learner):
        if solution:
            nb.code(sol)
        else:   # learner version: report instead of stopping when an answer is still None
            body = '\n'.join('    ' + l if l else l for l in learner.split('\n'))
            nb.code('try:\n' + body + '\nexcept Exception as e:\n    print("Finish the cells above first. (" + type(e).__name__ + ")")')

    def chk(code):
        """A check cell. In the learner version every line is guarded, so an unfinished answer shows NOT YET and never stops the notebook."""
        if solution:
            nb.code(code)
            return
        out = []
        for line in code.split('\n'):
            m = re.match(r'check\((["\'])(.*?)\1', line)
            if m:
                out.append('try:\n    ' + line + '\nexcept Exception:\n    check(' + repr(m.group(2)) + ', float("nan"), 0, 0)')
            else:
                out.append('try:\n    ' + line + '\nexcept Exception:\n    pass')
        nb.code('\n'.join(out))

    nb.md('# Session 18 lab: finding structure without labels\n\nYou will turn the Lakeside Mart orders into customer segments with RFM analysis and k-means, name each segment, and flag unusual orders and customers.\n\n'
          'Rhythm for every step: **PREDICT** first, **run** the cell, **READ** the output, then **CHANGE** one thing. Cells that say `None  # your code here` are yours to fill in. After each answer a `check` line tells you whether your number is right. '
          'There is no answer column today, so the checks cover the numbers and your own judgement covers the names. k-means uses random starts, so a few checks accept a range.')
    nb.data_setup()
    nb.check_setup()

    # ------------------------------------------------------------------ 1 loyalty orders
    nb.step(1, 'Keep the loyalty orders', 'A walk-in order has a blank `customer_id`, so we cannot follow that person over time. Segments are built from loyalty orders only, and we say so in the report.')
    nb.predict('About 30 percent of orders are walk-ins. How many customers will the loyalty orders cover: fewer than, equal to, or more than the 2,500 rows in customers.csv?')
    cell('import os\nimport numpy as np\nimport pandas as pd\n\nos.makedirs("keep", exist_ok=True)   # the folder where you save what you keep\norders = pd.read_csv("orders.csv", parse_dates=["order_date"])\nloyal = orders.dropna(subset=["customer_id"])   # drop the walk-ins\n'
         'print(len(orders), "orders;", len(orders) - len(loyal), "walk-ins left out;", len(loyal), "loyalty orders;", loyal["customer_id"].nunique(), "customers")',
         'import os\nimport numpy as np\nimport pandas as pd\n\nos.makedirs("keep", exist_ok=True)   # the folder where you save what you keep\norders = pd.read_csv("orders.csv", parse_dates=["order_date"])\nloyal = None   # your code here: the orders that have a customer_id (dropna on customer_id)\n'
         'print(len(orders), "orders;", len(orders) - len(loyal), "walk-ins left out;", len(loyal), "loyalty orders;", loyal["customer_id"].nunique(), "customers")')
    chk(f'check("loyalty orders", len(loyal), {F["loyal_orders"]}, 0)\ncheck("customers with a loyalty order", loyal["customer_id"].nunique(), {F["n_cust"]}, 0)')
    nb.read('Why is it honest to tell the reader that walk-in shoppers are not in the segments?')

    # ------------------------------------------------------------------ 2 RFM
    nb.step(2, 'Build recency, frequency and monetary value (RFM)', 'One record per customer: days since the last order (recency), number of orders (frequency) and total spend (monetary value). The end date is the last date in the file, so the numbers do not change when you reopen the notebook.')
    nb.predict(f'Customer C0001 made {len(F["c1_orders"])} orders. Will C0001 have a higher or a lower frequency than the average customer (about {st["frequency"]["mean"]:.1f} orders)?')
    cell('end_date = orders["order_date"].max()   # "today" is the last date in the file\nrfm = loyal.groupby("customer_id").agg(\n    last_order=("order_date", "max"),\n    frequency=("order_id", "count"),\n    spend=("order_value_ugx", "sum"))\n'
         'rfm["recency"] = (end_date - rfm["last_order"]).dt.days\nrfm = rfm[["recency", "frequency", "spend"]]\nprint(end_date.date())\nrfm.head(3)',
         'end_date = orders["order_date"].max()   # "today" is the last date in the file\nrfm = None   # your code here: group loyal by customer_id; last_order = max of order_date, frequency = count of order_id, spend = sum of order_value_ugx\n'
         'rfm["recency"] = None   # your code here: (end_date - rfm["last_order"]).dt.days\nrfm = rfm[["recency", "frequency", "spend"]]\nprint(end_date.date())\nrfm.head(3)')
    chk(f'check("C0001 recency", rfm.loc["C0001", "recency"], {F["rfm_head"][0][1]}, 0)\ncheck("C0001 frequency", rfm.loc["C0001", "frequency"], {F["rfm_head"][0][2]}, 0)\n'
            f'check("C0001 spend", rfm.loc["C0001", "spend"], {F["rfm_head"][0][3]}, 0)\ncheck("mean spend", rfm["spend"].mean(), {st["spend"]["mean"]:.2f}, 1)')
    nb.read('The mean spend is above the median spend (print rfm["spend"].median()). What does that tell you about the shape of spend?')
    nb.change('Replace end_date by pd.Timestamp.today(). What happens to recency, and why would that be a bad idea in a shared notebook?')

    # ------------------------------------------------------------------ 3 log and scale
    nb.step(3, 'Log transform and standardise', 'The log transform squeezes the long right tail. Standardisation (z-score) puts the three variables on one scale: mean 0, standard deviation 1. Use ddof=0, the same as scikit-learn\'s StandardScaler.')
    nb.predict('Spend has a skewness near 3. After log1p, will its skewness be near 3, near 1 or near 0?')
    cell('logged = np.log1p(rfm)   # log(1 + x), so a value of 0 does not break the logarithm\nscaled = (logged - logged.mean()) / logged.std(ddof=0)\n'
         'print("skewness before:", rfm.skew().round(2).to_dict())\nprint("skewness after log:", logged.skew().round(2).to_dict())\nprint("scaled standard deviations:", scaled.std(ddof=0).round(3).to_dict())',
         'logged = None   # your code here: np.log1p of rfm\nscaled = None   # your code here: (logged - logged.mean()) / logged.std(ddof=0)\n'
         'print("skewness before:", rfm.skew().round(2).to_dict())\nprint("skewness after log:", logged.skew().round(2).to_dict())\nprint("scaled standard deviations:", scaled.std(ddof=0).round(3).to_dict())')
    chk(f'check("skewness of spend before", rfm["spend"].skew(), {st["spend"]["skew"]:.4f}, 0.005)\ncheck("skewness of spend after log", logged["spend"].skew(), {F["skew_log"]["spend"]:.4f}, 0.005)\n'
            f'check("z-score of C0001 spend", scaled.loc["C0001", "spend"], {F["c1"]["z_spend"]:.4f}, 0.001)\ncheck("scaled standard deviation", scaled.std(ddof=0).mean(), 1.0, 0.0001)')
    nb.read('Which of the three variables was most skewed before the log? Which two numbers on the slide told you that scaling was needed?')

    # ------------------------------------------------------------------ 4 kmeans
    nb.step(4, 'k-means with four clusters', 'StandardScaler does the same z-score step inside scikit-learn. KMeans repeats assign and update until nobody changes cluster. n_init=10 means ten random starts, and the best (lowest inertia) is kept.')
    nb.predict('The segment numbers 0 to 3 are only labels. Will segment 0 here be the same group as segment 0 on the slides? Roughly how many customers will the largest segment hold?')
    cell('from sklearn.preprocessing import StandardScaler\nfrom sklearn.cluster import KMeans\n\nX = StandardScaler().fit_transform(logged)\nkmeans = KMeans(n_clusters=4, n_init=10, random_state=42)\nrfm["segment"] = kmeans.fit_predict(X)\n'
         'sizes = np.sort(rfm["segment"].value_counts().values)\nprint("inertia:", round(kmeans.inertia_, 1))\nprint("segment sizes, smallest to largest:", sizes)',
         'from sklearn.preprocessing import StandardScaler\nfrom sklearn.cluster import KMeans\n\nX = None   # your code here: StandardScaler().fit_transform(logged)\nkmeans = None   # your code here: KMeans with n_clusters=4, n_init=10, random_state=42\n'
         'rfm["segment"] = None   # your code here: kmeans.fit_predict(X)\nsizes = np.sort(rfm["segment"].value_counts().values)\nprint("inertia:", round(kmeans.inertia_, 1))\nprint("segment sizes, smallest to largest:", sizes)')
    size_checks = '\n'.join(f'check("segment size {i + 1} of 4 (smallest to largest)", sizes[{i}], {(a + b) / 2:.1f}, {(b - a) / 2 + 20:.1f})' for i, (a, b) in enumerate(rng))
    chk(f'check("inertia, k = 4", kmeans.inertia_, {F["k4_inertia"]:.1f}, 4)\n{size_checks}')
    nb.read('Which segment is the largest? Do the segment sizes add up to the number of customers?')
    nb.change('Optional: add `from sklearn.metrics import silhouette_score` and print `silhouette_score(X, kmeans.labels_)`. A score nearer 1 means tighter, better separated clusters. Compare k = 3, 4 and 5. Remember that k-means assumes round clusters of similar size.')
    nb.change('Change random_state from 42 to 7 and run Step 4 again. Which numbers move, and by how much? What does that say about quoting a segment size to the last customer?')

    # ------------------------------------------------------------------ 5 elbow
    nb.step(5, 'Choose k with the elbow method', 'Inertia is the sum of squared distances from each customer to its centroid. It always falls as k grows. We look for the bend.')
    nb.predict('The inertia for k = 1 is the sum of squares around a single centre. With three standardised variables and 2,499 customers, what number should it be? (Hint: each standardised variable has variance 1.)')
    cell('inertias = []\nfor k in range(1, 9):\n    model = KMeans(n_clusters=k, n_init=10, random_state=42)\n    model.fit(X)\n    inertias.append(model.inertia_)\nprint([round(v) for v in inertias])\n\n'
         'import matplotlib.pyplot as plt\nplt.plot(range(1, 9), inertias, marker="o")\nplt.xlabel("k: number of clusters")\nplt.ylabel("inertia")\nplt.show()',
         'inertias = []\nfor k in range(1, 9):\n    model = None   # your code here: KMeans with n_clusters=k, n_init=10, random_state=42, fitted on X\n    inertias.append(None)   # your code here: the model\'s inertia_\n'
         'print([round(v) for v in inertias])\n\nimport matplotlib.pyplot as plt\nplt.plot(range(1, 9), inertias, marker="o")\nplt.xlabel("k: number of clusters")\nplt.ylabel("inertia")\nplt.show()')
    chk(f'check("inertia, k = 1", inertias[0], {inert[1]:.1f}, 0.5)\ncheck("inertia, k = 4", inertias[3], {inert[4]:.1f}, 5)\ncheck("inertia, k = 8", inertias[7], {inert[8]:.1f}, 40)\ncheck("inertia always falls", bool(np.all(np.diff(inertias) < 0)), 1, 0)')
    nb.read('Where does the line bend? Is the bend sharp or gentle? Would you still choose k = 4, and what is your business reason?')

    # ------------------------------------------------------------------ 6 PCA
    nb.step(6, 'PCA: a flat picture of three variables', 'Principal component analysis (PCA) is a dimensionality reduction method. Each principal component is a weighted mix of the three variables, ordered by how much variance it keeps.')
    nb.predict('If recency, frequency and spend were completely unrelated, how much variance would each component keep? Here they are related, so will PC1 keep more or less than a third?')
    cell('from sklearn.decomposition import PCA\n\npca = PCA(n_components=3)\ncomponents = pca.fit_transform(X)\nratio = pca.explained_variance_ratio_\nprint("explained variance:", ratio.round(3), "first two:", round(ratio[:2].sum(), 3))\n\n'
         'plt.scatter(components[:, 0], components[:, 1], c=rfm["segment"], s=6, cmap="viridis")\nplt.xlabel("PC1")\nplt.ylabel("PC2")\nplt.show()',
         'from sklearn.decomposition import PCA\n\npca = None   # your code here: PCA with n_components=3\ncomponents = None   # your code here: pca.fit_transform(X)\nratio = None   # your code here: pca.explained_variance_ratio_\n'
         'print("explained variance:", ratio.round(3), "first two:", round(ratio[:2].sum(), 3))\n\nplt.scatter(components[:, 0], components[:, 1], c=rfm["segment"], s=6, cmap="viridis")\nplt.xlabel("PC1")\nplt.ylabel("PC2")\nplt.show()')
    chk(f'check("PC1 explained variance", ratio[0], {ratio[0]:.4f}, 0.001)\ncheck("PC2 explained variance", ratio[1], {ratio[1]:.4f}, 0.001)\ncheck("PC3 explained variance", ratio[2], {ratio[2]:.4f}, 0.001)')
    nb.read('How much of the variance do two components keep? Do the colours (the k-means segments) separate in the picture?')

    # ------------------------------------------------------------------ 7 names
    nb.step(7, 'Profile, name and act', 'A segment is only useful if it has a name a manager understands and an action. Read the averages in real units, then choose the names. Your names may differ from the slides.')
    nb.predict('Which segment will hold the most spend per customer? Will it also have the lowest recency?')
    cell('profile = rfm.groupby("segment").agg(\n    customers=("spend", "size"), recency=("recency", "mean"), orders=("frequency", "mean"), spend=("spend", "mean")).round(0)\nprofile["share_of_spend_pct"] = (rfm.groupby("segment")["spend"].sum() / rfm["spend"].sum() * 100).round(0)\nprint(profile)',
         'profile = None   # your code here: group rfm by segment; customers = size, recency = mean of recency, orders = mean of frequency, spend = mean of spend; round to 0 places\n'
         'profile["share_of_spend_pct"] = (rfm.groupby("segment")["spend"].sum() / rfm["spend"].sum() * 100).round(0)\nprint(profile)')
    cell('# Names by rule, because the segment numbers change between runs. Your own words are better: edit them.\nbest = profile["spend"].idxmax()\nlapsed = profile["recency"].idxmax()\nrecent = profile["recency"].idxmin()\n'
         'assert len({best, lapsed, recent}) == 3, "two rules picked the same segment: name the segments by hand"\ndrifting = [s for s in profile.index if s not in (best, lapsed, recent)][0]\n'
         'segment_names = {best: "Best customers", drifting: "Drifting regulars", recent: "Recent regulars", lapsed: "Lapsed low spenders"}\n'
         'rfm["segment_name"] = rfm["segment"].map(segment_names)\nrfm.reset_index().to_csv("keep/customer_segments.csv", index=False)   # your keepsake\nprint(rfm["segment_name"].value_counts())',
         'segment_names = None   # your code here: a dict that maps each segment number in profile to a name in business words, for example {0: "Best customers", ...}\n'
         'rfm["segment_name"] = rfm["segment"].map(segment_names)\nrfm.reset_index().to_csv("keep/customer_segments.csv", index=False)   # your keepsake\nprint(rfm["segment_name"].value_counts())')
    chk(f'check("four segments", len(profile), 4, 0)\ncheck("customers add up", profile["customers"].sum(), {F["n_cust"]}, 0)\ncheck("best segment: average spend", profile["spend"].max(), {pr[0]["spend"]:.0f}, 70000)\n'
            f'check("best segment: average recency in days", profile.loc[profile["spend"].idxmax(), "recency"], {pr[0]["recency"]:.1f}, 12)\ncheck("four different names", len(set(segment_names.values())), 4, 0)')
    nb.read('Write one action for each segment in the cell below. Which action would cost the least to test?')
    nb.md('## Your segment actions\n\nDouble click and fill in the table.\n\n| Segment name | Who they are | What I would do |\n|---|---|---|\n| | | |\n| | | |\n| | | |\n| | | |')

    # ------------------------------------------------------------------ 8 anomalies
    nb.step(8, 'Flag unusual orders and customers', 'Rule one is the percentile rule on order value (all orders, walk-ins included). Rule two is an IsolationForest on the scaled RFM variables, which isolates odd customers with few random cuts.')
    nb.predict('The percentile rule flags the top 1 percent of 30,229 orders. How many orders is that? Will the median of the flagged orders be 2, 10 or 35 times the median of all orders?')
    cell('p99 = orders["order_value_ugx"].quantile(0.99)\nbig = orders[orders["order_value_ugx"] > p99]\nprint("99th percentile:", round(p99), "UGX;", len(big), "orders flagged;", big["customer_id"].isna().sum(), "of them walk-ins")\n'
         'print("median of flagged:", big["order_value_ugx"].median(), "median of all:", orders["order_value_ugx"].median())\n\nfrom sklearn.ensemble import IsolationForest\n\n'
         'iso_model = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)\nrfm["anomaly"] = iso_model.fit_predict(X) == -1   # -1 means flagged\nflagged = rfm[rfm["anomaly"]]\nprint(len(flagged), "customers flagged")\nprint(flagged[["recency", "frequency", "spend"]].median())\n'
         'big.to_csv("keep/unusual_orders.csv", index=False)   # your list to review',
         'p99 = None   # your code here: the 99th percentile of order_value_ugx in orders (quantile(0.99))\nbig = None   # your code here: the orders with order_value_ugx above p99\nprint("99th percentile:", round(p99), "UGX;", len(big), "orders flagged;", big["customer_id"].isna().sum(), "of them walk-ins")\n'
         'print("median of flagged:", big["order_value_ugx"].median(), "median of all:", orders["order_value_ugx"].median())\n\nfrom sklearn.ensemble import IsolationForest\n\n'
         'iso_model = None   # your code here: IsolationForest(n_estimators=100, contamination=0.01, random_state=42)\nrfm["anomaly"] = None   # your code here: iso_model.fit_predict(X) == -1 (the value -1 means flagged)\nflagged = rfm[rfm["anomaly"]]\n'
         'print(len(flagged), "customers flagged")\nprint(flagged[["recency", "frequency", "spend"]].median())\nbig.to_csv("keep/unusual_orders.csv", index=False)   # your list to review')
    chk(f'check("99th percentile of order value", p99, {rule["p99"]:.1f}, 1)\ncheck("orders above it", len(big), {rule["n"]}, 0)\ncheck("customers flagged (1 percent of 2,499)", len(flagged), {iso["n"]}, 2)\n'
            f'unusual = ((flagged["recency"] > 100) & (flagged["spend"] < 100000)) | (flagged["spend"] > 800000)\ncheck("most flagged customers are lapsed low spenders or heavy spenders", unusual.mean() >= 0.5, 1, 0)')
    nb.code('show_checks()   # run this to see how many checks pass')
    nb.read('Look at the flagged customers. Which are the lapsed low spenders and which are heavy spenders? Name one thing you would check before treating any of them as an error.')
    nb.change('Change contamination to 0.05. How many customers are flagged now? What does that tell you about the rule?')
    nb.md('## Keep\n\nSave the notebook. Keep `keep/customer_segments.csv` (every loyalty customer with RFM, a segment name) and `keep/unusual_orders.csv` (orders to review). Bring one question about forecasting to Session 19.')
    return nb
