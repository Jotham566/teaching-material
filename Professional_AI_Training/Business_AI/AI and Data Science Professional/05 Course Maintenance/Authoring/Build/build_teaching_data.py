"""Generate the teaching datasets for AI and Data Science Professional.

  python3 build_teaching_data.py OUTPUT_DATA_FOLDER

numpy and pandas only. Fully seeded, so the same files come out on every machine. Everything is fictional; no real
person, company or patient. Writes CSV files, an answer_key.json computed from the data itself (no number is estimated),
and DATA DICTIONARY.txt.

Datasets
  Lakeside Mart      a chain of eight mini-markets in Uganda: branches, products, customers, orders (a 5 percent
                     sample of till transactions), order lines, returns, weekly branch summaries, a loyalty offer A/B test,
                     customer feedback messages, eight policy documents, and a dirty raw export of the order lines.
  Nile Microfinance  8,000 loans with an outcome (default), one leakage column and ordinary data defects.
  District Clinics   twelve districts by sixty months of clinic visits, malaria cases and rainfall.
"""
import sys, json, math, textwrap
from pathlib import Path
import numpy as np
import pandas as pd

SEED = 20261028
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('data')

def rng(k): return np.random.default_rng(SEED + k)
def r100(x): return (np.round(np.asarray(x) / 100) * 100).astype(int)

# ------------------------------------------------------------------ Lakeside Mart
BRANCHES = [("B01", "Kampala Central", "Central", 1.60, 0.017), ("B02", "Kampala Ntinda", "Central", 1.30, 0.018), ("B03", "Entebbe", "Central", 0.90, 0.019),
            ("B04", "Jinja", "Eastern", 1.00, 0.021), ("B05", "Mbale", "Eastern", 0.80, 0.023), ("B06", "Mbarara", "Western", 1.00, 0.020),
            ("B07", "Fort Portal", "Western", 0.70, 0.030), ("B08", "Gulu", "Northern", 0.80, 0.024)]
CATS = {"Staples": (1500, 9000, 0.34), "Fresh produce": (800, 6000, 0.22), "Beverages": (1000, 7000, 0.14), "Household": (2500, 22000, 0.12),
        "Personal care": (2500, 28000, 0.10), "Phones and electronics": (45000, 450000, 0.03), "Baby and school": (3000, 40000, 0.05)}
SEASON = {1: 0.92, 2: 0.90, 3: 1.00, 4: 1.00, 5: 0.98, 6: 0.97, 7: 0.98, 8: 1.02, 9: 1.04, 10: 1.05, 11: 1.12, 12: 1.40}
WEEK_START = pd.Timestamp('2024-01-01'); N_WEEKS = 104

def build_lakeside(key):
    g = rng(1)
    br = pd.DataFrame(BRANCHES, columns=['branch_id', 'branch_name', 'region', 'size', '_ret']).drop(columns=['_ret'])
    br['opened_year'] = [2016, 2018, 2019, 2017, 2021, 2020, 2022, 2021]
    # products
    rows = []; pid = 1
    for cat, (lo, hi, share) in CATS.items():
        n = int(round(150 * share))
        prices = np.exp(g.uniform(np.log(lo), np.log(hi), n))
        for p in prices:
            price = int(r100(p)); cost = int(r100(p * g.uniform(0.62, 0.84)))
            rows.append((f"P{pid:03d}", f"{cat} item {pid:03d}", cat, cost, max(price, cost + 100))); pid += 1
    prod = pd.DataFrame(rows, columns=['product_id', 'product_name', 'category', 'unit_cost_ugx', 'unit_price_ugx'])
    pop = np.array([CATS[c][2] * (3.0 if c == 'Phones and electronics' else 1.0) for c in prod.category]) * g.pareto(1.6, len(prod)).clip(0.05, 30)
    prod['_w'] = pop / pop.sum()
    # customers
    nc = 2500
    cust = pd.DataFrame({'customer_id': [f"C{i:04d}" for i in range(1, nc + 1)],
                         'home_branch_id': g.choice(br.branch_id, nc, p=br['size'] / br['size'].sum()),
                         'signup_date': (pd.Timestamp('2021-01-01') + pd.to_timedelta(g.integers(0, 1400, nc), unit='D')).strftime('%Y-%m-%d'),
                         'age_band': g.choice(['18-24', '25-34', '35-44', '45-54', '55+'], nc, p=[.16, .33, .26, .15, .10]),
                         'loyalty_tier': g.choice(['Basic', 'Silver', 'Gold'], nc, p=[.62, .28, .10])})
    # weekly branch drivers
    wk = []
    for _, b in br.iterrows():
        for w in range(N_WEEKS):
            d = WEEK_START + pd.Timedelta(weeks=w); m = d.month
            wet = m in (3, 4, 5, 9, 10, 11)
            rain = float(g.gamma(2.2, 18 if wet else 6))
            promo = int(g.random() < 0.22)
            foot = 1800 * b['size'] * SEASON[m] * math.exp(g.normal(0, 0.10))
            wk.append((b.branch_id, d.strftime('%Y-%m-%d'), int(foot), round(rain, 1), promo))
    bw = pd.DataFrame(wk, columns=['branch_id', 'week_start', 'footfall', 'rainfall_mm', 'promo_on'])
    # orders (5 percent sample of till transactions)
    orders = []; lines = []; oid = 1
    price = prod.set_index('product_id').unit_price_ugx
    for (bid, ws), row in bw.set_index(['branch_id', 'week_start']).iterrows():
        n = g.poisson(row.footfall * 0.02 * (1 + 0.18 * row.promo_on) * max(0.3, 1 - 0.0030 * row.rainfall_mm))
        for _ in range(n):
            day = pd.Timestamp(ws) + pd.Timedelta(days=int(g.integers(0, 7)))
            linked = g.random() < 0.70
            cid = g.choice(cust.customer_id) if linked else None
            pay = g.choice(['Cash', 'Mobile money', 'Card'], p=[.46, .47, .07])
            orders.append((f"O{oid:06d}", day.strftime('%Y-%m-%d'), bid, cid, pay, int(row.promo_on)))
            k = 1 + int(g.negative_binomial(1.1, 0.33))
            ps = g.choice(prod.product_id, k, p=prod._w)
            for p in ps:
                q = int(min(1 + g.geometric(0.55) - 1, 8)) or 1
                disc = float(g.choice([0, 0.05, 0.10], p=[.9, .07, .03])) if not row.promo_on else float(g.choice([0, 0.05, 0.10], p=[.5, .25, .25]))
                lines.append((f"O{oid:06d}", p, q, int(price[p]), disc))
            oid += 1
    od = pd.DataFrame(orders, columns=['order_id', 'order_date', 'branch_id', 'customer_id', 'payment_method', 'promo_week'])
    ol = pd.DataFrame(lines, columns=['order_id', 'product_id', 'quantity', 'unit_price_ugx', 'discount'])
    ol['line_revenue_ugx'] = (ol.quantity * ol.unit_price_ugx * (1 - ol.discount)).round().astype(int)
    # returns
    rate = {b[0]: b[4] for b in BRANCHES}
    ol = ol.merge(od[['order_id', 'branch_id']], on='order_id', how='left')
    ol['_ret'] = g.random(len(ol)) < ol.branch_id.map(rate)
    ret = ol[ol._ret][['order_id', 'product_id', 'quantity', 'line_revenue_ugx']].copy()
    ret['reason'] = g.choice(['Damaged', 'Expired', 'Wrong item', 'Changed mind'], len(ret), p=[.34, .22, .24, .20])
    ret.insert(0, 'return_id', [f"R{i:05d}" for i in range(1, len(ret) + 1)])
    ol = ol.drop(columns=['_ret']).reset_index(drop=True); ol.insert(0, 'line_id', [f"L{i:06d}" for i in range(1, len(ol) + 1)])
    # branch-week table gets sales and order counts from the real orders (so the regression is honest)
    od['week_start'] = (pd.to_datetime(od.order_date) - pd.to_timedelta(pd.to_datetime(od.order_date).dt.dayofweek, unit='D')).dt.strftime('%Y-%m-%d')
    rev_by_order = ol.groupby('order_id').line_revenue_ugx.sum().rename('order_value_ugx')
    od = od.merge(rev_by_order, on='order_id')
    agg = od.groupby(['branch_id', 'week_start']).agg(orders=('order_id', 'count'), sales_ugx=('order_value_ugx', 'sum')).reset_index()
    bw = bw.merge(agg, on=['branch_id', 'week_start'], how='left').fillna({'orders': 0, 'sales_ugx': 0}); bw['orders'] = bw.orders.astype(int); bw['sales_ugx'] = bw.sales_ugx.astype(int)
    od = od.drop(columns=['week_start'])
    # loyalty offer A/B test (random assignment, true lift built in)
    n_t = 4000; ids = g.choice(cust.customer_id, 2500, replace=False)
    tid = [f"C{i:04d}" for i in range(1, 2501)]
    ab = pd.DataFrame({'customer_id': tid, 'group': g.choice(['offer', 'control'], 2500)})
    base_val = g.lognormal(math.log(52000), 0.55, 2500)
    lift = np.where(ab.group == 'offer', 1.07, 1.0)
    ab['next_month_spend_ugx'] = r100(base_val * lift * g.lognormal(0, 0.15, 2500))
    p_ret = np.where(ab.group == 'offer', 0.46, 0.41)
    ab['returned_within_30d'] = (g.random(2500) < p_ret).astype(int)
    # feedback messages
    fb = build_feedback(g, br)
    docs = build_policies()
    return dict(branches=br, products=prod.drop(columns=['_w']), customers=cust, orders=od, order_lines=ol.drop(columns=['branch_id']),
                returns=ret, branch_weeks=bw, offer_test=ab, feedback=fb), docs, ol

THINGS = ["rice", "posho", "milk", "cooking oil", "sugar", "bread", "soap", "airtime voucher", "phone charger", "school books", "tomatoes", "bananas", "sodas", "diapers"]
THEMES = {
 'queue': (["Long queue at the till in {branch}, waited more than twenty minutes.", "We waited ages to pay at {branch}. Only one till was open.", "The checkout line at {branch} was very slow today.", "Too many people and not enough cashiers at {branch}, I almost left my basket.", "Spent half an hour in the line on Saturday. Please open more tills.", "Slow service at the counter, it took so long to pay."],
           ["No queue at all at {branch} today, in and out in five minutes.", "Fast checkout at {branch}, the cashier was quick.", "The line moved quickly even on Saturday."]),
 'payment': (["Mobile money payment failed twice and I was charged anyway.", "I paid with Mobile Money but the till said no payment. I lost money.", "The card machine at {branch} was not working so I could not pay.", "The payment went through on my phone but the cashier says nothing came. Please refund.", "Airtel Money kept timing out at the till.", "I was charged twice for one purchase."],
             ["Mobile money payment went through quickly, thank you.", "Paying with my phone was easy and quick.", "The card machine worked well today."]),
 'freshness': (["The {thing} was expired when I opened it. Very disappointed.", "Bought {thing} at {branch} and it was already spoiled.", "The bread was stale and the milk smelled bad.", "Found rotten tomatoes in the bag I took home.", "The expiry date on the {thing} had passed two weeks ago.", "The {thing} was not fresh at all."],
               ["Fresh {thing} and clean shelves. Will come back.", "The vegetables at {branch} were very fresh this morning.", "Good quality {thing} every time."]),
 'price': (["Prices of {thing} keep going up, too expensive.", "Why is {thing} cheaper at the market than here?", "Everything at {branch} costs more than last month.", "The price on the shelf was lower than at the till.", "Too costly for ordinary families.", "I cannot afford to shop here anymore, prices are high."],
           ["Great offer on {thing} this week, saved a lot.", "Good prices on {thing}.", "The promotion made {thing} very affordable."]),
 'staff': (["Staff were rude when I asked about a refund for {thing}.", "The cashier at {branch} shouted at me.", "Nobody was ready to help me find {thing}.", "Unfriendly security guard at the entrance.", "The attendant ignored me for ten minutes.", "Very poor customer care at {branch}."],
           ["Friendly staff at {branch}, they helped me find {thing}.", "Polite cashier and a helpful security guard.", "The manager solved my problem quickly. Thank you."]),
 'stock': (["No {thing} on the shelf again this week. Why?", "{thing} is always out of stock at {branch}.", "I came for {thing} but the shelf was empty.", "Please stock {thing}, I travel far to shop here.", "Out of {thing} for the third time.", "The shelves at {branch} are half empty."],
           ["Good stock of {thing} this week.", "Everything I needed was on the shelf.", "Happy to find {thing} again."]),
 'cleanliness': (["The shop was dirty and the {thing} was damaged.", "The floor at {branch} was wet and nobody cleaned it.", "Bad smell near the fresh produce section.", "Dusty shelves and a sticky floor.", "The toilets at {branch} were not clean.", "Flies near the meat counter."],
                 ["The shop was clean and tidy.", "Very clean shelves at {branch}.", "Neat and well organised store."]),
 'loyalty': (["My loyalty points did not show after the purchase.", "I scanned my card but no points were added.", "The points on my card are wrong.", "Asked about my Gold discount and the cashier knew nothing.", "Lost my points when I changed my phone number.", "Why were my points removed?"],
             ["The loyalty points were added at once. Very good.", "Love the Gold discount on Saturdays.", "Easy to earn points at {branch}."]),
 'delivery': (["Delivery was two hours late and the {thing} was warm.", "The rider never called before arriving.", "My order arrived with items missing.", "The delivery fee was higher than they told me.", "Waited all day for my delivery.", "The driver left the groceries at the gate."],
              ["Delivery was on time and the groceries were cold.", "The rider was polite and quick.", "Same day delivery worked well."])}
FB_NEU = ["I bought {thing} at {branch} on Saturday.", "Do you open on public holidays at {branch}?", "Please tell me the price of {thing}.", "I will pick up the {thing} order tomorrow.", "Is {thing} available in {branch}?", "Does the receipt need my phone number?"]

def build_feedback(g, br):
    rows = []; names = list(THEMES); w = np.array([1.4, 1.2, 1.0, 1.2, 1.0, 1.1, 0.7, 0.8, 0.7]); w = w / w.sum()
    for i in range(1, 801):
        s = g.choice(['positive', 'negative', 'neutral'], p=[.30, .50, .20]); b = g.choice(br.branch_name); th = g.choice(THINGS)
        if s == 'neutral': tpl = g.choice(FB_NEU); theme = 'question'
        else:
            theme = g.choice(names, p=w); tpl = g.choice(THEMES[theme][0 if s == 'negative' else 1])
        msg = tpl.format(thing=th, branch=b)
        pre = g.choice(['', '', '', 'Hello. ', 'Yesterday I shopped at %s. ' % b, 'To the manager: ', 'Feedback: ', 'On Friday evening. '])
        suf = g.choice(['', '', ' Thank you.', ' Keep it up.', ' Will recommend.', ' Please fix this.', ' I am not happy.', ' This has happened before.', ' Do better.', ' Please reply.']) if s != 'neutral' else g.choice(['', ' Thanks.', ' Please reply.'])
        msg = pre + msg + suf
        if g.random() < 0.06: s = g.choice(['positive', 'negative', 'neutral'])
        rating = {'positive': g.choice([4, 5], p=[.4, .6]), 'negative': g.choice([1, 2, 3], p=[.35, .45, .20]), 'neutral': 3}[s]
        rows.append((f"F{i:04d}", b, msg, int(rating), s, theme))
    return pd.DataFrame(rows, columns=['feedback_id', 'branch_name', 'message', 'rating', 'sentiment', 'theme'])

def build_policies():
    P = {
     "returns_policy": """Lakeside Mart Returns Policy. Customers may return an item within 7 days of purchase with the till receipt. Fresh produce and bread can be returned only on the day of purchase and only if damaged or spoiled. Electronics and phones may be exchanged within 14 days if the sealed packaging is intact, and a repair is offered after that under the manufacturer warranty. Refunds are made to the same payment method. Mobile money refunds take up to 3 working days. Items bought on a promotion can be exchanged but not refunded in cash. Opened personal care products cannot be returned for hygiene reasons.""",
     "loyalty_programme": """Lakeside Mart Loyalty Programme. Every customer who gives a phone number at the till joins as Basic. A customer earns 1 point for every UGX 1,000 spent. Silver status starts at 2,000 points in 12 months and Gold at 6,000 points. Silver customers receive 3 percent off selected household items on Saturdays. Gold customers receive 5 percent off, free delivery within 5 kilometres and early notice of offers. Points expire after 12 months. Points are added within one day of purchase. Points cannot be exchanged for cash.""",
     "mobile_money": """Lakeside Mart Mobile Money Payments. Customers can pay with MTN Mobile Money or Airtel Money at all eight branches. A payment request is sent to the customer's phone and must be approved with the customer's PIN. If the money leaves the wallet but the till shows no payment, the customer should keep the transaction message and ask the branch manager, who checks the daily settlement report. Failed payments are reversed by the provider, usually within 24 hours. Lakeside Mart never asks for a customer's PIN. Mobile money limits are set by the provider.""",
     "delivery": """Lakeside Mart Delivery. Delivery is available from Kampala Central, Kampala Ntinda, Entebbe and Jinja for orders above UGX 80,000. The fee is UGX 5,000 within 5 kilometres and UGX 10,000 within 15 kilometres. Gold loyalty customers receive free delivery within 5 kilometres. Orders placed before 2 pm are delivered the same day. Perishable goods are delivered in cooler boxes. A customer who is not present at the address is called twice before the order is returned to the branch. Delivery is not available in Gulu, Mbale, Mbarara or Fort Portal.""",
     "food_safety": """Lakeside Mart Food Safety. Fresh produce is checked each morning and removed if spoiled. Dairy is stored below 5 degrees Celsius and the fridge temperature is recorded every 4 hours. Products past their expiry date are removed from shelves daily and logged. A customer who finds an expired item should return it with the receipt for a full refund and the branch records the incident. Repeated incidents at a branch are reported to the head office within 48 hours. Staff handling food wash their hands and wear clean aprons.""",
     "data_privacy": """Lakeside Mart Customer Data. Lakeside Mart collects a customer's phone number, name, age band and purchases to run the loyalty programme. This follows the principles in the Uganda Data Protection and Privacy Act, 2019, including collecting only what is needed and keeping it secure. A customer may ask to see, correct or delete their data by writing to the data officer. Data is kept for 3 years after the last purchase. Analysts working with the data use customer numbers and not names, and share only summaries outside the company. Customer data is never sold.""",
     "opening_hours": """Lakeside Mart Opening Hours. Branches open from 7 am to 9 pm Monday to Saturday and from 9 am to 6 pm on Sunday. Kampala Central and Kampala Ntinda close at 10 pm on Fridays. On public holidays all branches open from 9 am to 5 pm, except on Christmas Day when all branches are closed. The pharmacy counter in Kampala Central and Entebbe opens from 8 am to 8 pm. Opening hours change during stocktake, which is announced on the notice board a week before.""",
     "supplier_complaints": """Lakeside Mart Supplier Quality. Suppliers must deliver fresh goods with a delivery note and a temperature record. A branch manager inspects every delivery. If more than 5 percent of a delivery is damaged or spoiled, the delivery is rejected and the supplier is told the same day. A supplier with three rejected deliveries in a quarter is placed on review for 60 days. Complaints from customers about a supplier's product are logged by item and branch and reviewed monthly by the buyer. Payment to suppliers is made within 30 days of an accepted delivery."""}
    return P

def dirty_export(ol, od, key):
    g = rng(7)
    br_name = {b[0]: b[1] for b in BRANCHES}
    df = ol.merge(od[['order_id', 'order_date', 'customer_id', 'payment_method']], on='order_id')
    df = df.sample(n=min(len(df), 40000), random_state=3) if len(df) > 40000 else df
    df = df.sort_values('line_id').reset_index(drop=True)
    truth = df.copy()
    truth_rev = int(truth.line_revenue_ugx.sum())
    n = len(df)
    # defect 7: returns appear as negative lines with the original (the return of the same item)
    returned = pd.read_csv(OUT / 'returns.csv')
    # (the returns table is written before this function runs)
    ret_keys = set(zip(returned.order_id, returned.product_id))
    isret = pd.Series([(o, p) in ret_keys for o, p in zip(df.order_id, df.product_id)], index=df.index)
    neg = df[isret].copy(); neg['quantity'] = -neg['quantity']; neg['line_id'] = neg['line_id'] + 'R'
    df = pd.concat([df, neg], ignore_index=True)
    true_net = int((df.quantity * df.unit_price_ugx * (1 - df.discount)).round().sum())
    out = pd.DataFrame({'line_id': df.line_id, 'order_id': df.order_id, 'order_date': df.order_date, 'branch': df.branch_id.map(br_name),
                        'customer_id': df.customer_id.fillna(''), 'payment': df.payment_method, 'product_id': df.product_id,
                        'qty': df.quantity, 'unit_price': df.unit_price_ugx, 'discount_pct': (df.discount * 100).round().astype(int)})
    m = len(out)
    # 2 mixed date formats (30 percent dd/mm/yyyy)
    sel = g.random(m) < 0.30
    out.loc[sel, 'order_date'] = pd.to_datetime(out.loc[sel, 'order_date']).dt.strftime('%d/%m/%Y')
    # 3 price as text with currency and commas on 25 percent
    sel = g.random(m) < 0.25
    out['unit_price'] = out['unit_price'].astype(object)
    out.loc[sel, 'unit_price'] = ['UGX ' + f"{int(v):,}" for v in out.loc[sel, 'unit_price']]
    # 4 payment variants
    var = {'Cash': ['Cash', 'cash', 'CASH', 'Cash '], 'Mobile money': ['Mobile money', 'Mobile Money', 'MM', 'mobile money'], 'Card': ['Card', 'card', 'CARD']}
    out['payment'] = [g.choice(var[p]) for p in out.payment]
    # 5 branch name noise
    def noisy(name):
        r = g.random()
        if r < 0.05: return name.upper()
        if r < 0.09: return name + ' '
        if r < 0.11: return name.replace('Central', 'Cntral').replace('Entebbe', 'Entebe')
        return name
    out['branch'] = [noisy(b) for b in out.branch]
    # 6 blank customers in different spellings
    sel = out.customer_id == ''
    out.loc[sel, 'customer_id'] = g.choice(['', 'N/A', 'NULL', 'walk-in'], int(sel.sum()), p=[.4, .25, .2, .15])
    # 1 duplicate rows (exact copies)
    dup = out.sample(n=80, random_state=5)
    out = pd.concat([out, dup], ignore_index=True)
    # 8 unrecoverable: quantity missing on 12 lines. Their true revenue is the documented residual.
    ids = out[(out.qty > 0) & ~out.line_id.str.endswith('R')].drop_duplicates('line_id').sample(n=12, random_state=11).line_id
    miss_mask = out.line_id.isin(ids) & ~out.duplicated(subset=['line_id'], keep='first')
    resid = int((truth.set_index('line_id').loc[ids].line_revenue_ugx).sum())
    out.loc[miss_mask, 'qty'] = np.nan
    out = out.sample(frac=1, random_state=9).reset_index(drop=True)
    key['dirty_export'] = dict(file='orders_raw.csv', rows=len(out), seeded_defects=8,
                              true_net_revenue_ugx=true_net, unrecoverable_lines=12, residual_ugx=resid,
                              pipeline_net_revenue_ugx=true_net - resid, note='A correct clean lands on true_net minus the 12 lines whose quantity is blank. Naming that gap and its cause is the pass mark.',
                              exact_duplicates=80, mixed_date_share=0.30, price_text_share=0.25, date_rule='A date with slashes is dd/mm/yyyy; a date with dashes is yyyy-mm-dd.')
    return out

# ------------------------------------------------------------------ Nile Microfinance
DISTRICTS = ['Kampala', 'Wakiso', 'Mukono', 'Jinja', 'Mbale', 'Gulu', 'Lira', 'Mbarara', 'Masaka', 'Fort Portal']
OCC = {'Trader': 0.0, 'Farmer': 0.25, 'Boda rider': 0.35, 'Teacher': -0.40, 'Salon owner': -0.10, 'Tailor': -0.05, 'Mechanic': 0.05}
PURPOSE = ['Stock', 'Farm inputs', 'School fees', 'Equipment', 'Rent', 'Medical']

def sigmoid(z): return 1 / (1 + np.exp(-z))

def build_loans(key):
    g = rng(21); n = 8000
    age = np.clip(g.normal(36, 9, n), 20, 68).round().astype(int)
    gender = g.choice(['F', 'M'], n, p=[.58, .42])
    occ = g.choice(list(OCC), n, p=[.28, .22, .12, .08, .10, .08, .12])
    # gender and occupation are linked (as in real portfolios); gender itself has NO direct effect on default
    flip = (gender == 'F') & (g.random(n) < 0.35); occ = np.where(flip, g.choice(['Trader', 'Salon owner', 'Tailor'], n), occ)
    dist = g.choice(DISTRICTS, n, p=[.14, .13, .09, .10, .08, .10, .08, .10, .09, .09])
    income = np.exp(g.normal(np.log(650_000), 0.45, n)) * np.where(occ == 'Teacher', 1.3, 1) * np.where(occ == 'Boda rider', 0.8, 1)
    loan = np.exp(g.normal(np.log(1_200_000), 0.55, n)); loan = np.clip(loan, 200_000, 6_000_000)
    term = g.choice([3, 6, 9, 12], n, p=[.15, .35, .20, .30])
    prev_loans = np.minimum(g.poisson(1.6, n), 8)
    prev_late = np.minimum(g.poisson(0.35 + 0.1 * (prev_loans > 0) * prev_loans / 2, n), 6)
    group = (g.random(n) < 0.34).astype(int)
    savings = np.exp(g.normal(np.log(150_000), 0.9, n)) * (1 + 0.2 * prev_loans)
    momo = (g.random(n) < 0.72).astype(int)
    km = np.clip(g.gamma(2.0, 4.0, n), 0.3, 45)
    purpose = g.choice(PURPOSE, n, p=[.34, .18, .15, .13, .10, .10])
    burden = np.clip((loan * 1.15 / term) / income, 0.02, 2.5)
    z = (-3.6 + 2.0 * burden + 0.38 * prev_late - 0.12 * np.minimum(prev_loans, 5) - 0.55 * group - 0.7 * (savings / loan > 0.25)
         + 0.018 * km + np.array([OCC[o] for o in occ]) - 0.25 * momo + g.normal(0, 0.55, n))
    # calibrate intercept to ~12.5 percent
    lo, hi = -3, 3
    for _ in range(40):
        mid = (lo + hi) / 2
        if sigmoid(z + mid).mean() > 0.125: hi = mid
        else: lo = mid
    p = sigmoid(z + (lo + hi) / 2); default = (g.random(n) < p).astype(int)
    collect = np.where(default == 1, 1 + g.poisson(3.5, n), g.poisson(0.25, n))
    date = pd.Timestamp('2023-01-01') + pd.to_timedelta(g.integers(0, 1000, n), unit='D')
    df = pd.DataFrame({'loan_id': [f"N{i:05d}" for i in range(1, n + 1)], 'disbursed_date': date.strftime('%Y-%m-%d'), 'district': dist, 'age': age, 'gender': gender, 'occupation': occ,
                       'monthly_income_ugx': r100(income), 'loan_amount_ugx': r100(loan), 'term_months': term, 'loan_purpose': purpose, 'previous_loans': prev_loans, 'previous_late_payments': prev_late,
                       'group_loan': group, 'savings_balance_ugx': r100(savings), 'has_mobile_money': momo, 'distance_to_branch_km': km.round(1), 'collection_calls': collect, 'default': default})
    # ordinary defects
    miss = g.random(n) < 0.05; df.loc[miss, 'monthly_income_ugx'] = np.nan
    df.loc[g.choice(n, 2, replace=False), 'age'] = [199, 0]
    messy = g.random(n) < 0.04; df.loc[messy, 'district'] = [d.upper() if g.random() < .5 else d + ' ' for d in df.loc[messy, 'district']]
    key['loans'] = dict(rows=n, default_rate=round(float(df['default'].mean()), 4), missing_income=int(df.monthly_income_ugx.isna().sum()), impossible_ages=2,
                        leakage_column='collection_calls', note='collection_calls exists only after a loan goes bad.')
    return df

# ------------------------------------------------------------------ District Clinics
CLINIC_DIST = ['Kampala', 'Wakiso', 'Mukono', 'Jinja', 'Mbale', 'Soroti', 'Gulu', 'Lira', 'Mbarara', 'Kabale', 'Fort Portal', 'Masaka']

def build_clinics(key):
    g = rng(31); rows = []
    months = pd.date_range('2021-01-01', periods=60, freq='MS')
    for d_i, d in enumerate(CLINIC_DIST):
        pop = int(g.integers(280_000, 1_800_000)); base = pop / 1000 * g.uniform(5.5, 8.0); clinics = int(g.integers(14, 70))
        prev_rain = 60.0
        for t, m in enumerate(months):
            mo = m.month; wet = 1.0 + 0.55 * (mo in (3, 4, 5)) + 0.45 * (mo in (9, 10, 11)) - 0.20 * (mo in (1, 2, 7, 8))
            rain = float(g.gamma(3.0, 22.0 * wet / 1.3))
            malaria = base * 0.22 * (1 + 0.006 * prev_rain) * (1 + 0.002 * t) * math.exp(g.normal(0, 0.08)); prev_rain = rain
            visits = base * (1 + 0.15 * (wet - 1)) * (1 + 0.003 * t) * math.exp(g.normal(0, 0.06))
            rows.append((d, m.strftime('%Y-%m-%d'), pop, clinics, round(rain, 1), int(visits), int(malaria)))
    df = pd.DataFrame(rows, columns=['district', 'month', 'population', 'clinics', 'rainfall_mm', 'total_visits', 'malaria_cases'])
    miss = df.sample(n=18, random_state=4).index; df.loc[miss, 'total_visits'] = np.nan
    key['clinics'] = dict(rows=len(df), districts=len(CLINIC_DIST), months=60, missing_total_visits=int(df.total_visits.isna().sum()))
    return df

# ------------------------------------------------------------------ main
def auc(y, s):
    order = np.argsort(s); y = np.asarray(y)[order]; n1 = y.sum(); n0 = len(y) - n1
    ranks = np.arange(1, len(y) + 1); return float((ranks[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))

def logit_fit(X, y, it=30):
    X = np.c_[np.ones(len(X)), X]; b = np.zeros(X.shape[1])
    for _ in range(it):
        p = sigmoid(X @ b); W = p * (1 - p) + 1e-9
        b = b + np.linalg.solve(X.T @ (X * W[:, None]) + 1e-6 * np.eye(len(b)), X.T @ (y - p))
    return b

def design(df, cols_num):
    X = df[cols_num].astype(float).copy()
    X = X.fillna(X.median())
    return ((X - X.mean()) / X.std()).values

def main():
    OUT.mkdir(parents=True, exist_ok=True); key = {'seed': SEED}
    tables, docs, ol_full = build_lakeside(key)
    for k, df in tables.items(): df.to_csv(OUT / f"{k}.csv", index=False, lineterminator='\n')
    (OUT / 'policies').mkdir(exist_ok=True)
    for k, t in docs.items(): (OUT / 'policies' / f"{k}.txt").write_text(textwrap.fill(t, 100) + "\n", encoding='utf-8')
    od = tables['orders']; ol = tables['order_lines']
    raw = dirty_export(ol.assign(branch_id=ol.order_id.map(od.set_index('order_id').branch_id)), od, key)
    raw.to_csv(OUT / 'orders_raw.csv', index=False, lineterminator='\n')
    loans = build_loans(key); loans.to_csv(OUT / 'loans.csv', index=False, lineterminator='\n')
    clin = build_clinics(key); clin.to_csv(OUT / 'clinic_visits.csv', index=False, lineterminator='\n')

    # ---- properties computed from the data (the verifier asserts all of them)
    ov = ol.groupby('order_id').line_revenue_ugx.sum()
    d = od.assign(value=od.order_id.map(ov), month=pd.to_datetime(od.order_date).dt.month, year=pd.to_datetime(od.order_date).dt.year)
    key['lakeside'] = dict(orders=len(od), order_lines=len(ol), customers=len(tables['customers']), products=len(tables['products']), returns=len(tables['returns']),
                           revenue_ugx=int(ol.line_revenue_ugx.sum()), mean_order_value_ugx=round(float(ov.mean())), median_order_value_ugx=round(float(ov.median())),
                           mean_over_median=round(float(ov.mean() / ov.median()), 2))
    m = d.groupby(['year', 'month']).value.sum()
    key['lakeside']['december_over_february_2024'] = round(float(m[(2024, 12)] / m[(2024, 2)]), 2); key['lakeside']['december_over_february_2025'] = round(float(m[(2025, 12)] / m[(2025, 2)]), 2)
    lines_br = ol.merge(od[['order_id', 'branch_id']], on='order_id'); rr = tables['returns'].merge(od[['order_id', 'branch_id']], on='order_id')
    cnt = rr.groupby('branch_id').size(); rate = (cnt / lines_br.groupby('branch_id').size())
    key['lakeside']['returns_count_by_branch'] = {k: int(v) for k, v in cnt.items()}; key['lakeside']['returns_rate_by_branch'] = {k: round(float(v), 4) for k, v in rate.items()}
    key['lakeside']['most_returns_branch'] = cnt.idxmax(); key['lakeside']['highest_rate_branch'] = rate.idxmax()
    a = tables['offer_test']; o = a[a.group == 'offer']; c = a[a.group == 'control']
    diff = o.next_month_spend_ugx.mean() - c.next_month_spend_ugx.mean(); se = math.sqrt(o.next_month_spend_ugx.var() / len(o) + c.next_month_spend_ugx.var() / len(c))
    pa, pb = o.returned_within_30d.mean(), c.returned_within_30d.mean(); sep = math.sqrt(pa * (1 - pa) / len(o) + pb * (1 - pb) / len(c))
    key['offer_test'] = dict(n_offer=len(o), n_control=len(c), mean_spend_offer=round(float(o.next_month_spend_ugx.mean())), mean_spend_control=round(float(c.next_month_spend_ugx.mean())),
                             difference_ugx=round(float(diff)), ci95_low=round(float(diff - 1.96 * se)), ci95_high=round(float(diff + 1.96 * se)),
                             return_rate_offer=round(float(pa), 4), return_rate_control=round(float(pb), 4), rate_diff=round(float(pa - pb), 4), rate_ci95=[round(float(pa - pb - 1.96 * sep), 4), round(float(pa - pb + 1.96 * sep), 4)])
    bw = tables['branch_weeks']; X = np.c_[np.ones(len(bw)), bw.footfall, bw.promo_on, bw.rainfall_mm]
    for target, name in (('orders', 'regression_weekly_orders'), ('sales_ugx', 'regression_weekly_sales')):
        coef, *_ = np.linalg.lstsq(X, bw[target].values.astype(float), rcond=None); pred = X @ coef
        r2 = 1 - ((bw[target] - pred) ** 2).sum() / ((bw[target] - bw[target].mean()) ** 2).sum()
        key[name] = dict(formula=f'{target} ~ footfall + promo_on + rainfall_mm', intercept=round(float(coef[0]), 2), footfall=round(float(coef[1]), 4), promo_on=round(float(coef[2]), 2), rainfall_mm=round(float(coef[3]), 3), r_squared=round(float(r2), 3))
    # loans
    lo = loans.copy(); y = lo['default'].values; num = ['age', 'monthly_income_ugx', 'loan_amount_ugx', 'term_months', 'previous_loans', 'previous_late_payments', 'group_loan', 'savings_balance_ugx', 'has_mobile_money', 'distance_to_branch_km']
    lo = lo[lo.age.between(18, 80)]; y = lo['default'].values
    lo['burden'] = (lo.loan_amount_ugx * 1.15 / lo.term_months) / lo.monthly_income_ugx.fillna(lo.monthly_income_ugx.median()); lo['save_ratio'] = lo.savings_balance_ugx / lo.loan_amount_ugx
    cols = num + ['burden', 'save_ratio']; Xa = design(lo, cols); idx = np.random.default_rng(1).permutation(len(lo)); tr, te = idx[:int(.75 * len(lo))], idx[int(.75 * len(lo)):]
    b = logit_fit(Xa[tr], y[tr]); s = np.c_[np.ones(len(te)), Xa[te]] @ b
    Xl = np.c_[Xa, (lo.collection_calls.values - lo.collection_calls.mean()) / lo.collection_calls.std()]; bl = logit_fit(Xl[tr], y[tr]); sl = np.c_[np.ones(len(te)), Xl[te]] @ bl
    key['loans'].update(honest_auc_logistic_numpy=round(auc(y[te], s), 3), leaky_auc_logistic_numpy=round(auc(y[te], sl), 3), baseline_accuracy_all_no=round(float(1 - y.mean()), 4),
                        default_rate_by_district={k: round(float(v), 3) for k, v in loans.groupby(loans.district.str.strip().str.title()).default.mean().items()},
                        default_rate_by_gender={k: round(float(v), 3) for k, v in loans.groupby('gender').default.mean().items()})
    # clinics
    cl = clin.copy(); mm = cl.groupby(pd.to_datetime(cl.month).dt.month).malaria_cases.sum()
    key['clinics'].update(peak_month_malaria=int(mm.idxmax()), trough_month_malaria=int(mm.idxmin()))
    cl['rain_lag1'] = cl.groupby('district').rainfall_mm.shift(1)
    key['clinics']['corr_malaria_rain_lag0'] = round(float(cl.malaria_cases.corr(cl.rainfall_mm)), 3); key['clinics']['corr_malaria_rain_lag1'] = round(float(cl.malaria_cases.corr(cl.rain_lag1)), 3)
    L = key['lakeside']; O = key['offer_test']
    assert L['mean_over_median'] >= 1.8, 'order values are not skewed enough'
    assert min(L['december_over_february_2024'], L['december_over_february_2025']) >= 1.4, 'seasonality too weak'
    assert L['most_returns_branch'] != L['highest_rate_branch'], 'the rate-versus-count reversal is missing'
    assert O['ci95_low'] > 0, 'the spend lift is not detectable'
    assert key['regression_weekly_orders']['footfall'] > 0 and key['regression_weekly_orders']['promo_on'] > 0 and key['regression_weekly_orders']['rainfall_mm'] < 0, 'regression signs'
    assert 0.70 <= key['loans']['honest_auc_logistic_numpy'] <= 0.85 and key['loans']['leaky_auc_logistic_numpy'] >= 0.95, 'loan model difficulty'
    assert 0.10 <= key['loans']['default_rate'] <= 0.15, 'default rate'
    assert key['clinics']['corr_malaria_rain_lag1'] > 0.25 > abs(key['clinics']['corr_malaria_rain_lag0']), 'rain lag effect'
    (OUT / 'answer_key.json').write_text(json.dumps(key, indent=1, ensure_ascii=False), encoding='utf-8')
    (OUT / 'DATA DICTIONARY.txt').write_text(DICT, encoding='utf-8')
    print('data written to', OUT); print(json.dumps({k: key[k] for k in ('lakeside', 'offer_test', 'loans')}, indent=1)[:1800])

DICT = """DATA DICTIONARY. Every table is fictional. orders.csv is a random 5 percent sample of till transactions, to keep files small; all revenue figures describe the sample.

LAKESIDE MART (eight mini-markets in Uganda)
branches.csv        grain: one branch. branch_id (key), branch_name, region, size (relative size), opened_year.
products.csv        grain: one product. product_id (key), product_name, category, unit_cost_ugx, unit_price_ugx.
customers.csv       grain: one loyalty customer. customer_id (key), home_branch_id, signup_date, age_band, loyalty_tier.
orders.csv          grain: one till order. order_id (key), order_date, branch_id, customer_id (blank for walk-in), payment_method, promo_week (1 if the branch ran a promotion that week), order_value_ugx (the sum of the order's lines).
order_lines.csv     grain: one product on one order. line_id (key), order_id, product_id, quantity, unit_price_ugx, discount (0 to 0.10), line_revenue_ugx = quantity * unit_price * (1 - discount).
returns.csv         grain: one returned line. return_id (key), order_id, product_id, quantity, line_revenue_ugx, reason.
branch_weeks.csv    grain: one branch in one week. footfall (door counter), rainfall_mm, promo_on, orders (sampled orders that week), sales_ugx (their value). Orders is the cleaner regression target because it is not inflated by a few very large baskets.
offer_test.csv      grain: one loyalty customer in a randomised loyalty-offer test. group (offer or control), next_month_spend_ugx, returned_within_30d (0 or 1).
feedback.csv        grain: one customer message. message, rating (1 to 5), sentiment (positive, negative, neutral; about 6 percent of labels are noisy on purpose), theme (queue, payment, freshness, price, staff, stock, cleanliness, loyalty, delivery, or question). Theme is what the message is about, so it can score a search.
policies/*.txt      eight short policy documents used in Session 22.
orders_raw.csv      the dirty export of order lines used in Session 8, with eight seeded defects. Returns appear as negative quantities.

NILE MICROFINANCE
loans.csv           grain: one loan. default (1 = defaulted). collection_calls is recorded only after a loan goes bad: it leaks the answer. Missing incomes and two impossible ages are seeded.

DISTRICT CLINICS
clinic_visits.csv   grain: one district in one month, January 2021 to December 2025. total_visits has 18 blank months.
"""

if __name__ == '__main__':
    main()
