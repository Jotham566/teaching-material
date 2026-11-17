"""Session 10: SQL for analysts (relational database, SQLite, SELECT to LIMIT, aggregates, GROUP BY and HAVING, order of execution, INNER and LEFT JOIN, NULL, CASE, subqueries, CTE, aliases). Python lab in content/labs/s10_nb.py.

Every number on a slide, in a note, in the notebook checks or in the facilitator key is computed in facts(): each SQL query is run against lakeside.db (SQLite, read only) and
its answer is asserted equal to a pandas calculation on the CSV files. The output printed on a slide is the real output of the query shown.
"""
import contextlib
import io
import os
import sqlite3
from functools import lru_cache
from pathlib import Path

import pandas as pd

BUILD = Path(__file__).resolve().parents[1]
DATA = BUILD.parent.parent / '03 Learner Materials' / 'Practice Files' / 'data'


def n(x):
    return f'{int(x):,}'


def sq(q):
    con = sqlite3.connect(f'file:{DATA / "lakeside.db"}?mode=ro', uri=True)
    try:
        return pd.read_sql_query(q, con)
    finally:
        con.close()


def show(df):
    """The query result as a plain text table, NULL written as NULL (what a SQL client shows)."""
    d = df.astype(object).where(df.notna(), 'NULL')
    return [l.rstrip() for l in d.to_string(index=False).split('\n')]


Q_SELECT = ("SELECT order_id, order_value_ugx\nFROM orders\nWHERE branch_id = 'B06'\n  AND payment_method = 'Card'\nORDER BY order_value_ugx DESC, order_id\nLIMIT 3;")
Q_AGG = ("SELECT COUNT(*) AS records,\n       COUNT(customer_id) AS filled,\n       SUM(order_value_ugx) AS revenue,\n       MAX(order_value_ugx) AS largest\nFROM orders;")
Q_GROUP = ("SELECT branch_id,\n       COUNT(*) AS orders,\n       SUM(order_value_ugx) AS revenue\nFROM orders\nGROUP BY branch_id\nORDER BY revenue DESC\nLIMIT 4;")
Q_HAVING = ("SELECT reason, COUNT(*) AS n\nFROM returns\nGROUP BY reason\nHAVING COUNT(*) > 450\nORDER BY n DESC;")
Q_BAD = ("SELECT reason, COUNT(*) AS n\nFROM returns\nWHERE COUNT(*) > 450\nGROUP BY reason;")
Q_INNER = ("SELECT b.region, COUNT(*) AS orders,\n       SUM(o.order_value_ugx) AS revenue\nFROM orders AS o\nINNER JOIN branches AS b\n        ON o.branch_id = b.branch_id\nGROUP BY b.region;")
Q_LEFT = ("SELECT c.loyalty_tier,\n       COUNT(*) AS orders\nFROM orders AS o\nLEFT JOIN customers AS c\n       ON o.customer_id = c.customer_id\nGROUP BY c.loyalty_tier\nORDER BY orders DESC;")
Q_NULL = ("SELECT SUM(customer_id <> 'C0495') AS test_true,\n       SUM(customer_id =  'C0495') AS test_false,\n       SUM(customer_id IS NULL)    AS is_null\nFROM orders;")
Q_CASE = ("SELECT CASE\n         WHEN order_value_ugx < 20000 THEN 'Small'\n         WHEN order_value_ugx < 100000 THEN 'Medium'\n         ELSE 'Large'\n       END AS band,\n       COUNT(*) AS orders\nFROM orders\nGROUP BY band\nORDER BY orders DESC;")
Q_SUB = ("SELECT COUNT(*) AS above_average\nFROM products\nWHERE unit_price_ugx >\n      (SELECT AVG(unit_price_ugx) FROM products);")
Q_CTE = ("WITH by_branch AS (\n  SELECT branch_id, SUM(order_value_ugx) AS revenue\n  FROM orders\n  GROUP BY branch_id\n)\nSELECT COUNT(*) AS branches,\n       MAX(revenue) AS best\nFROM by_branch;")
C_PY = ("import sqlite3\ncon = sqlite3.connect('lakeside.db')\nsql = \"SELECT COUNT(*) AS n FROM orders\"\nsql += \" WHERE branch_id = 'B04'\"\n"
        "a = pd.read_sql(sql, con).n[0]\nb = (orders.branch_id == 'B04').sum()\nprint(a, b, a == b)")
PRE = "import pandas as pd\norders = pd.read_csv('orders.csv')\nbranches = pd.read_csv('branches.csv')\n"


def run_py(code):
    old = os.getcwd()
    os.chdir(DATA)
    try:
        ns = {}
        exec(PRE, ns)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            exec(code, ns)
    finally:
        os.chdir(old)
    return [l.rstrip() for l in buf.getvalue().rstrip('\n').split('\n')]


@lru_cache(maxsize=None)
def facts():
    o = pd.read_csv(DATA / 'orders.csv')
    l = pd.read_csv(DATA / 'order_lines.csv')
    p = pd.read_csv(DATA / 'products.csv')
    b = pd.read_csv(DATA / 'branches.csv')
    c = pd.read_csv(DATA / 'customers.csv')
    r = pd.read_csv(DATA / 'returns.csv')
    F = {}
    tabs = sq("SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name").name.tolist()
    F['tables'] = tabs
    F['n_tables'] = len(tabs)
    F['rows'] = {t: int(sq(f'SELECT COUNT(*) AS n FROM {t}').n[0]) for t in tabs}
    F['cols'] = {t: [x for x in sq(f'SELECT * FROM {t} LIMIT 1').columns] for t in tabs}
    csvs = dict(orders=o, order_lines=l, products=p, branches=b, customers=c, returns=r)
    for t, d in csvs.items():
        assert F['rows'][t] == len(d), t
    F['rev'] = int(o.order_value_ugx.sum())
    F['out'] = {}

    def go(key, q):
        df = sq(q)
        F['out'][key] = show(df)
        return df
    # select
    d = go('select', Q_SELECT)
    t3 = o[(o.branch_id == 'B06') & (o.payment_method == 'Card')].sort_values(['order_value_ugx', 'order_id'], ascending=[False, True]).head(3)
    assert d.order_id.tolist() == t3.order_id.tolist() and d.order_value_ugx.tolist() == t3.order_value_ugx.tolist()
    F['n_card_b06'] = int(((o.branch_id == 'B06') & (o.payment_method == 'Card')).sum())
    assert int(sq("SELECT COUNT(*) AS n FROM orders WHERE branch_id = 'B06' AND payment_method = 'Card'").n[0]) == F['n_card_b06']
    F['sel'] = d
    # aggregates
    d = go('agg', Q_AGG)
    assert (d.records[0], d.filled[0], d.revenue[0], d.largest[0]) == (len(o), o.customer_id.count(), o.order_value_ugx.sum(), o.order_value_ugx.max())
    F['records'], F['filled'], F['largest'] = int(d.records[0]), int(d.filled[0]), int(d.largest[0])
    F['walkin'] = F['records'] - F['filled']
    assert F['walkin'] == int(o.customer_id.isna().sum())
    # group by
    d = go('group', Q_GROUP)
    g = o.groupby('branch_id').agg(orders=('order_id', 'count'), revenue=('order_value_ugx', 'sum')).sort_values('revenue', ascending=False).head(4).reset_index()
    assert d.branch_id.tolist() == g.branch_id.tolist() and d.revenue.tolist() == g.revenue.tolist() and d.orders.tolist() == g.orders.tolist()
    F['top_branch'], F['top_rev'], F['top_orders'] = str(d.branch_id[0]), int(d.revenue[0]), int(d.orders[0])
    F['top_branch_name'] = str(b.set_index('branch_id').loc[F['top_branch'], 'branch_name'])
    # having
    d = go('having', Q_HAVING)
    vc = r.reason.value_counts()
    vc = vc[vc > 450]
    assert d.reason.tolist() == vc.index.tolist() and d.n.tolist() == vc.tolist()
    F['reasons'] = list(zip(d.reason, d.n.astype(int)))
    F['reasons_all'] = {k: int(v) for k, v in r.reason.value_counts().items()}
    F['changed_mind'] = int(r.reason.value_counts()['Changed mind'])
    # the aggregate in WHERE error
    con_ = sqlite3.connect(f'file:{DATA / "lakeside.db"}?mode=ro', uri=True)
    try:
        con_.execute(Q_BAD)
        raise AssertionError('expected an error')
    except sqlite3.OperationalError as e:
        msg = str(e)
    finally:
        con_.close()
    F['bad_msg'] = msg
    F['out']['bad'] = ['sqlite3.OperationalError:', msg]
    assert 'aggregate' in msg
    # inner join
    d = go('inner', Q_INNER)
    m = o.merge(b, on='branch_id', how='inner', validate='m:1').groupby('region').agg(orders=('order_id', 'count'), revenue=('order_value_ugx', 'sum'))
    assert {r_: (int(a_), int(v_)) for r_, a_, v_ in zip(d.region, d.orders, d.revenue)} == {r_: (int(x.orders), int(x.revenue)) for r_, x in m.iterrows()}
    F['region_top'] = str(m.revenue.idxmax())
    F['region_top_rev'], F['region_top_orders'] = int(m.revenue.max()), int(m.loc[F['region_top'], 'orders'])
    F['n_regions'] = len(m)
    # left join
    d = go('left', Q_LEFT)
    lm = o.merge(c, on='customer_id', how='left', validate='m:1')
    tiers = lm.groupby('loyalty_tier', dropna=False).size().sort_values(ascending=False)
    got = {('NULL' if pd.isna(k) else k): int(v) for k, v in zip(d.loyalty_tier, d.orders)}
    assert got == {('NULL' if pd.isna(k) else k): int(v) for k, v in tiers.items()}
    F['tier'] = got
    inner = o.merge(c, on='customer_id', how='inner', validate='m:1')
    F['inner_rows'], F['left_rows'] = len(inner), len(lm)
    assert int(sq('SELECT COUNT(*) AS n FROM orders AS o INNER JOIN customers AS c ON o.customer_id = c.customer_id').n[0]) == F['inner_rows']
    assert int(sq('SELECT COUNT(*) AS n FROM orders AS o LEFT JOIN customers AS c ON o.customer_id = c.customer_id').n[0]) == F['left_rows']
    assert got['NULL'] == F['walkin']
    # null logic
    d = go('null', Q_NULL)
    t_true, t_false, t_null = int((o.customer_id.notna() & (o.customer_id != 'C0495')).sum()), int((o.customer_id == 'C0495').sum()), int(o.customer_id.isna().sum())
    assert (int(d.test_true[0]), int(d.test_false[0]), int(d.is_null[0])) == (t_true, t_false, t_null)
    F['t_true'], F['t_false'], F['t_null'] = t_true, t_false, t_null
    assert t_true + t_false + t_null == len(o)
    assert F['reasons_all']['Damaged'] > 470 and F['reasons_all']['Wrong item'] > 470 >= F['reasons_all']['Expired']
    rows3 = [(str(o[o.customer_id == 'C0495'].iloc[0].order_id), 'C0495', 'FALSE')]
    r2 = o[(o.customer_id.notna()) & (o.customer_id != 'C0495')].iloc[0]
    rows3.append((str(r2.order_id), str(r2.customer_id), 'TRUE'))
    r3 = o[o.customer_id.isna()].iloc[0]
    rows3.append((str(r3.order_id), 'NULL', 'UNKNOWN'))
    F['tv_rows'] = sorted(rows3, key=lambda x: x[0])
    # case
    d = go('case', Q_CASE)
    cut = pd.cut(o.order_value_ugx, [0, 20000, 100000, float('inf')], right=False, labels=['Small', 'Medium', 'Large']).value_counts()
    F['n_exact_20000'] = int((o.order_value_ugx == 20000).sum())
    F['cut_default_small'] = int(pd.cut(o.order_value_ugx, [0, 20000, 100000, float('inf')], labels=['Small', 'Medium', 'Large']).value_counts()['Small'])
    assert {k: int(v) for k, v in zip(d.band, d.orders)} == {k: int(v) for k, v in cut.items()}
    F['bands'] = {k: int(v) for k, v in zip(d.band, d.orders)}
    # subquery
    d = go('sub', Q_SUB)
    F['above_avg'] = int((p.unit_price_ugx > p.unit_price_ugx.mean()).sum())
    assert int(d.above_average[0]) == F['above_avg']
    F['avg_price'] = float(p.unit_price_ugx.mean())
    F['below_avg'] = int((p.unit_price_ugx < p.unit_price_ugx.mean()).sum())
    F['equal_avg'] = int((p.unit_price_ugx == p.unit_price_ugx.mean()).sum())
    assert int(sq('SELECT COUNT(*) AS n FROM products WHERE unit_price_ugx < (SELECT AVG(unit_price_ugx) FROM products)').n[0]) == F['below_avg']
    F['n_products'] = len(p)
    # cte
    d = go('cte', Q_CTE)
    rb = o.groupby('branch_id').order_value_ugx.sum()
    assert int(d.branches[0]) == len(rb) and int(d.best[0]) == int(rb.max())
    F['n_branches'], F['best_rev'] = len(rb), int(rb.max())
    # pandas bridge
    F['out']['py'] = run_py(C_PY)
    assert F['out']['py'][0].endswith('True')
    F['b04_orders'] = int((o.branch_id == 'B04').sum())
    # join excerpt, checked with SQL in memory
    oo = pd.concat([o[o.customer_id.notna()].head(2), o[o.customer_id.isna()].head(1)]).sort_values('order_id')
    keys = set(oo.customer_id.dropna())
    cu = pd.concat([c[c.customer_id.isin(keys)], c[~c.customer_id.isin(keys)].head(1)]).sort_values('customer_id')
    F['jt_orders'] = [(str(a), '' if pd.isna(k) else str(k)) for a, k in zip(oo.order_id, oo.customer_id)]
    F['jt_customers'] = [(str(a), str(k)) for a, k in zip(cu.customer_id, cu.loyalty_tier)]
    mem = sqlite3.connect(':memory:')
    oo[['order_id', 'customer_id']].to_sql('orders', mem, index=False)
    cu[['customer_id', 'loyalty_tier']].to_sql('customers', mem, index=False)
    F['jt'] = {}
    for how, kw in (('inner', 'INNER JOIN'), ('left', 'LEFT JOIN')):
        dd = pd.read_sql_query(f'SELECT o.order_id, o.customer_id, c.loyalty_tier FROM orders AS o {kw} customers AS c ON o.customer_id = c.customer_id ORDER BY o.order_id', mem)
        pm = oo[['order_id', 'customer_id']].merge(cu, on='customer_id', how=how).sort_values('order_id')
        assert len(dd) == len(pm)
        F['jt'][how] = [['' if pd.isna(v) else str(v) for v in x] for x in dd.itertuples(index=False, name=None)]
    mem.close()
    # other files for the work slide
    ln = pd.read_csv(DATA / 'loans.csv')
    F['loans_rows'] = len(ln)
    F['loans_default_pct'] = float(ln.default.mean() * 100)
    cv = pd.read_csv(DATA / 'clinic_visits.csv')
    F['clinic_rows'] = len(cv)
    F['feedback_rows'] = F['rows']['feedback']
    # erd spec
    return F


def erd_spec(F):
    tags = {('customers', 'customer_id'): 'PK', ('customers', 'home_branch_id'): 'FK', ('orders', 'order_id'): 'PK', ('orders', 'branch_id'): 'FK', ('orders', 'customer_id'): 'FK',
            ('branches', 'branch_id'): 'PK', ('products', 'product_id'): 'PK', ('order_lines', 'line_id'): 'PK', ('order_lines', 'order_id'): 'FK', ('order_lines', 'product_id'): 'FK',
            ('returns', 'return_id'): 'PK', ('returns', 'order_id'): 'FK'}
    shown = {'customers': (0, 0, ['customer_id', 'home_branch_id', 'signup_date', 'age_band', 'loyalty_tier']), 'orders': (1, 0, ['order_id', 'order_date', 'branch_id', 'customer_id']),
             'branches': (2, 0, ['branch_id', 'branch_name', 'region', 'size', 'opened_year']), 'products': (0, 1, ['product_id', 'product_name', 'category', 'unit_cost_ugx', 'unit_price_ugx']),
             'order_lines': (1, 1, ['line_id', 'order_id', 'product_id', 'quantity']), 'returns': (2, 1, ['return_id', 'order_id', 'product_id', 'reason'])}
    tables = []
    for name, (col, row, cols) in shown.items():
        assert set(cols) <= set(F['cols'][name])
        rows = [(c_, tags.get((name, c_), '')) for c_ in cols]
        more = len(F['cols'][name]) - len(cols)
        if more:
            rows.append((f'+ {more} more variables', 'more'))
        assert len(rows) == 5, name
        tables.append(dict(name=name, col=col, row=row, rows=rows))
    links = [dict(many='orders', many_var='customer_id', one='customers', one_var='customer_id'), dict(many='orders', many_var='branch_id', one='branches', one_var='branch_id'),
             dict(many='order_lines', many_var='order_id', one='orders', one_var='order_id'), dict(many='order_lines', many_var='product_id', one='products', one_var='product_id'),
             dict(many='returns', many_var='order_id', one='orders', one_var='order_id')]
    return tables, links


def build():
    F = facts()
    R = F['rows']
    sess = dict(
        num=10, block='Module C: Analyse and explain', short_title='SQL for analysts',
        title='SQL for analysts: ask a database the questions you ask pandas',
        question='How do we ask a database the same questions in the language every employer uses?',
        outcomes=['Write a query with SELECT, FROM, WHERE, GROUP BY, HAVING, ORDER BY and LIMIT, and explain the order in which the database runs the clauses',
                  'Write an INNER JOIN and a LEFT JOIN, say which records each keeps, and handle NULL correctly',
                  'Use CASE WHEN, a subquery and a CTE, and check every SQL answer against pandas'],
        outcome_icons=['magnifier', 'key', 'check'],
        outcome_note=('Here is what you can do by the end of today. You can write a query with the main clauses, from SELECT to LIMIT, and explain the order in which the database actually runs them. '
                      'You can write an inner join and a left join, say which records each one keeps, and handle NULL without losing rows by accident. '
                      'And you can use CASE WHEN, a subquery and a CTE, and check every SQL answer against pandas. All of it runs on a SQLite copy of Lakeside Mart, inside Google Colab, with nothing to install.'),
        clock=[(10, 'Recall and the question of the day'), (45, 'Concepts: picture, plain words, one example by hand'), (10, 'Break'), (45, 'Lab: predict, run, read, change'), (10, 'Exit check, keep and next')],
        plan_title='Your two hours: concepts first, then a SQL lab in Colab',
        plan_caption='Ideas with pictures first. Then you open the notebook. Then the checks and what you keep.',
        plan_note=('We have two hours. The first ten minutes bring back Session 9 and set the question for today. Then forty-five minutes of concepts with no laptops open, so you can watch the queries and their results. '
                   'After a ten minute break you open the Colab notebook for a forty-five minute lab, where every SQL answer is compared with pandas. The last ten minutes are an exit check and what you keep. '
                   'The lab is where the learning sticks, so please protect that time.'),
        recall_from='Session 9',
        recall=[('A merge ran without an error and revenue became 5.3 times too big. What happened, and what protects you?', 'Fan-out: a one-to-many merge repeated each order once per line. Check row counts before and after, and set validate.'),
                ('Which join type keeps every order, including walk-ins with no customer_id?', 'A left join from orders to customers. An inner join drops the records that have no match.'),
                ('What does pivot_table do that groupby alone does not?', 'It lays the grouped result out as a grid, with one variable down the side and one across the top, which is wide format.')],
        words=[('Relational database (SQLite)', 'Several tables linked by keys, stored in one file. SQLite is a free database that runs inside Python.'),
               ('Query and clause', 'A query is one question in SQL. A clause is one part of it, such as SELECT, WHERE or ORDER BY.'),
               ('Aggregate function, GROUP BY and HAVING', 'COUNT, SUM, AVG, MIN and MAX reduce records to one value. HAVING filters the groups that GROUP BY makes.'),
               ('JOIN (INNER, LEFT)', 'Combines two tables on a key. INNER keeps matches only. LEFT keeps every left record.'),
               ('NULL (three-valued logic)', 'A missing value. A test on NULL is neither true nor false but unknown, so use IS NULL.')],
        word_icons=['folder', 'magnifier', 'calculator', 'key', 'question'],
        words_note=('Five words for today. A relational database is a set of tables linked by keys, and SQLite is a free one that lives in a single file. '
                    'A query is one question written in SQL, and a clause is one part of it. An aggregate function reduces many records to one value, and GROUP BY and HAVING work with it. '
                    'A join combines two tables, and inner and left are the two you use most. And NULL is a missing value, which follows its own logic. We use every one of them before the end of the session.'),
        keep='Keep your Colab query book: ten SQL queries on the Lakeside database, each with a proof table that shows the SQL answer next to the pandas answer.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Your lab file', value='A query book'), dict(label='The habit', value='SQL then pandas'), dict(label='Next session', value='Charts')]),
        keep_title='Save your query book with its proof table',
        next='Session 11: Exploring and visualising with Python. We draw the numbers so that a reader sees the finding.', next_label='Next session',
        keep_note=('Before you go, save your notebook with its proof table. That table is your keepsake: for every query, the SQL answer, the pandas answer and whether they match. '
                   'If a colleague asks how you know a number is right, you can show them. Next session we turn tables into charts that make a finding visible. '
                   'If anything was unclear today, write the question down and bring it.'),
        cover_note=('Welcome back. Last session you grouped and joined tables in pandas and learned to catch a merge that quietly multiplies revenue. '
                    'Today we ask the same questions in SQL, the language of almost every company database. If you can use a PivotTable and a VLOOKUP, you already know the ideas. '
                    'Only the words change. And every answer will be checked against pandas, so you always know it is right.'),
        use_at_work='Query a company database with SQL and prove the answer in pandas.',
        slides=[])
    S = sess['slides']
    tables, links = erd_spec(F)

    # 1
    S.append(dict(kind='table', title='Answers to the three questions from Session 9', headers=['Question', 'Short answer'],
                  rows=[[q, a] for q, a in sess['recall']], widths=[5.2, 6.8], icons=['cross', 'key', 'grid'],
                  notes=('Here are the answers to the three warm-up questions. The merge that made revenue 5.3 times too big was fan-out: a one-to-many merge repeated each order once for every line. Row counts before and after, and the validate option, protect you. '
                         'To keep every order including the walk-ins, use a left join from orders to customers. And pivot table lays a grouped result out as a grid in wide format. '
                         'Today you will meet the same ideas in SQL. Which of the three do you want to see again in SQL?')))

    # 2 database
    S.append(dict(kind='wide', title=f'A relational database holds several tables linked by keys: {F["n_tables"]} tables in one SQLite file',
                  visual=dict(kind='ds_erd', tables=tables, links=links),
                  caption=f'Six of the {F["n_tables"]} tables. PK: primary key. FK: foreign key. Three prongs: the many side.',
                  notes=(f'In Session 2 you saw how the Lakeside tabs link by keys. A database stores such tables together, and a relational database links them with primary keys and foreign keys. '
                         f'Today the database is a single file called lakeside dot db, and it holds {F["n_tables"]} tables. This diagram shows six of them, with orders at the centre: {n(R["orders"])} orders, {n(R["order_lines"])} order lines and {n(R["returns"])} returns. '
                         'The database engine is SQLite. It is free, it needs no server and no account, and it runs inside Python in Colab. Real banks use bigger engines such as PostgreSQL or SQL Server, but the SQL you learn today carries over almost unchanged. Which table would you query to count returns by reason?')))

    # 3 words table
    S.append(dict(kind='table', title='The same question in Excel, in SQL and in pandas',
                  headers=['In Excel', 'In SQL', 'In pandas'],
                  rows=[['Pick columns', 'SELECT', 'df with a list of columns'], ['Which sheet or table', 'FROM', 'the DataFrame'], ['AutoFilter on rows', 'WHERE', 'a boolean filter'],
                        ['PivotTable', 'GROUP BY with COUNT, SUM, AVG', 'groupby and agg'], ['Filter the PivotTable totals', 'HAVING', 'filter the grouped result'],
                        ['Sort', 'ORDER BY, LIMIT', 'sort_values, head'], ['VLOOKUP beside your full list', 'JOIN, LEFT JOIN', 'merge']],
                  widths=[3.6, 4.2, 4.2], icons=['grid', 'folder', 'magnifier', 'chart', 'check', 'clock', 'key'], note='SQL keywords are written in capitals by convention. SQL ignores the difference.',
                  notes=('You already do all of this in Excel, so here is the translation. Pick columns is SELECT. Which table is FROM. AutoFilter on rows is WHERE. A PivotTable is GROUP BY with an aggregate function such as COUNT, SUM or AVG. '
                         'Filtering the PivotTable totals is HAVING. Sorting is ORDER BY, and LIMIT keeps only the first few rows. VLOOKUP is a JOIN, and a lookup column beside your whole list, where the missing ones show blank, is a left join. '
                         'By convention SQL keywords are written in capitals, but the database does not mind. The pandas column shows what you did last session. Which row of this table is the one you use most in Excel?')))

    # 4 select
    S.append(dict(kind='code', title='SELECT, FROM, WHERE, ORDER BY and LIMIT: the three largest card orders at branch B06',
                  code=Q_SELECT, output=F['out']['select'],
                  reads=['SELECT names the variables to return. FROM names the table.', "WHERE keeps the records that pass a test. One equals sign tests equality, and text goes in single quotes.",
                         'ORDER BY sorts. DESC means largest first. A second variable breaks ties.', f'LIMIT 3 keeps three records. B06 has {n(F["n_card_b06"])} card orders in all.'],
                  notes=(f'Here is our first query. A query is one question, written in SQL. SELECT names the variables we want back, and FROM names the table. WHERE keeps only the records that pass a test, here branch B06 and payment by card. '
                         'Notice one equals sign for equality, and single quotes around text. ORDER BY sorts the result, and DESC means largest first. A second variable, order id, breaks ties so the order is always the same. '
                         f'LIMIT keeps the first three. A database table has no built-in row order, so without ORDER BY the word LIMIT gives you any three rows. Branch B06 has {n(F["n_card_b06"])} card orders. What would change if you removed ORDER BY?')))

    # 5 order of execution
    hints = {'FROM': 'choose the table', 'WHERE': 'keep records', 'GROUP BY': 'make groups', 'HAVING': 'keep groups', 'SELECT': 'pick and name', 'ORDER BY': 'sort', 'LIMIT': 'cut'}
    S.append(dict(kind='wide', title='You write SELECT first, but the database runs FROM first and SELECT fifth',
                  visual=dict(kind='ds_sql_order', written=['SELECT', 'FROM', 'WHERE', 'GROUP BY', 'HAVING', 'ORDER BY', 'LIMIT'], executed=['FROM', 'WHERE', 'GROUP BY', 'HAVING', 'SELECT', 'ORDER BY', 'LIMIT'], hints=hints),
                  caption='This order is why standard SQL forbids a SELECT alias in WHERE (SQLite allows it).',
                  notes=('This picture explains most SQL errors. You write the clauses in one order, with SELECT first. The database runs them in another. First FROM chooses the table. Then WHERE keeps records. Then GROUP BY makes groups. '
                         'Then HAVING keeps groups. Only fifth does SELECT pick and name the variables. Then ORDER BY sorts, and LIMIT cuts. This is the logical order of execution. '
                         'So in standard SQL WHERE cannot use a name you created in SELECT, because that name does not exist yet. Many databases, such as SQL Server, refuse it. SQLite is more relaxed and accepts it, but a portable query repeats the expression or uses a CTE. ORDER BY can use the alias, because by then it exists. Why can HAVING use an aggregate but WHERE cannot?')))

    # 6 aggregates
    S.append(dict(kind='code', title='Aggregate functions reduce many records to one value',
                  code=Q_AGG, output=F['out']['agg'],
                  reads=[f'COUNT(*) counts records: {n(F["records"])} orders.', f'COUNT(customer_id) counts filled values and skips NULL: {n(F["filled"])}.', f'The difference, {n(F["walkin"])}, is the walk-in orders.',
                         f'SUM adds up revenue: UGX {n(F["rev"])}. MAX is the largest order: UGX {n(F["largest"])}.', 'AS gives a result variable a name: an alias.'],
                  notes=(f'Aggregate functions reduce many records to one value: COUNT, SUM, AVG, MIN and MAX. COUNT of star counts records, and we get {n(F["records"])} orders. '
                         f'COUNT of a variable counts only the filled values and skips NULL, so COUNT of customer id gives {n(F["filled"])}. The difference of {n(F["walkin"])} is the walk-in orders. You met the same idea last session as size and count in pandas. '
                         f'SUM gives the revenue of the sample, and MAX the largest single order, {n(F["largest"])} shillings. The word AS gives a result a name. That name is called an alias. Which of these would you use to find the smallest order?')))

    # 7 group by
    S.append(dict(kind='code', title='GROUP BY makes one result record per group, like a PivotTable',
                  code=Q_GROUP, output=F['out']['group'],
                  reads=['GROUP BY branch_id makes one group per branch.', 'Each aggregate function runs once per group.', 'ORDER BY can use the alias revenue, because SELECT has run by then.',
                         f'{F["top_branch"]} ({F["top_branch_name"]}) leads with UGX {n(F["top_rev"])} from {n(F["top_orders"])} orders.'],
                  notes=(f'GROUP BY is the PivotTable of SQL. GROUP BY branch id makes one group for each branch, and each aggregate function runs once per group, so we get one result record per branch. '
                         f'We sort by revenue, largest first, and keep four. ORDER BY is allowed to use the alias revenue, because by the time it runs, SELECT has already created that name. '
                         f'Branch {F["top_branch"]}, {F["top_branch_name"]}, leads with {n(F["top_rev"])} shillings from {n(F["top_orders"])} orders. This matches the pandas groupby from last session exactly, and every query today is checked against pandas. '
                         'Which variable would you group by to see revenue per payment method?')))

    # 8 having
    S.append(dict(kind='code', title='HAVING filters the groups after GROUP BY has made them',
                  code=Q_HAVING, output=F['out']['having'],
                  reads=['returns has one record per returned line.', 'GROUP BY reason counts the returns for each reason.', f'HAVING COUNT(*) > 450 keeps only the groups with more than 450 returns.',
                         f'The fourth reason, Changed mind, has {n(F["changed_mind"])} and is filtered out.'],
                  notes=(f'HAVING filters groups. First GROUP BY reason makes one group for each return reason and counts the returns. Then HAVING keeps only the groups whose count is above 450. '
                         f'Three reasons pass: {F["reasons"][0][0]} with {n(F["reasons"][0][1])}, {F["reasons"][1][0]} with {n(F["reasons"][1][1])} and {F["reasons"][2][0]} with {n(F["reasons"][2][1])}. The fourth reason, Changed mind, has {n(F["changed_mind"])}, so it is filtered out. '
                         'The rule of thumb: WHERE filters records before grouping, and HAVING filters groups after. Which clause would you use to count only the returns of one product?')))

    # 9 error
    S.append(dict(kind='code', title='An aggregate function cannot appear in WHERE, because WHERE runs before the groups exist',
                  code=Q_BAD, output=F['out']['bad'],
                  reads=['This query asks WHERE to test a count.', 'WHERE runs second, before GROUP BY has made any group, so there is no count yet.', 'SQLite stops with an error.', 'Move the test to HAVING.'],
                  notes=('Here is the mistake the order of execution predicts. We asked WHERE to test COUNT of star. But WHERE runs second, before GROUP BY has made any group, so there is no count to test. '
                         'SQLite stops with an error that says misuse of aggregate COUNT. The fix is to move the test to HAVING, which runs after GROUP BY. '
                         'When you meet an error message in SQL, read it and then look at the order of execution. It usually points to a clause that runs too early. What would you change in this query to make it run?')))

    # 10 join types picture
    pan = [dict(title='INNER JOIN', rows=F['jt']['inner'], keeps='Only keys found in both tables.'), dict(title='LEFT JOIN', rows=F['jt']['left'], keeps='Every left record. No match gives NULL.')]
    S.append(dict(kind='wide', title='INNER JOIN keeps matches only, and LEFT JOIN keeps every record of the left table',
                  visual=dict(kind='ds_join_types', orders=F['jt_orders'], customers=F['jt_customers'], panels=pan, null='NULL'),
                  caption='A real excerpt joined on customer_id. Gold cells are NULL (missing).',
                  notes=('Here are the two joins you will use most, on a real excerpt. The left table has three orders, and one is a walk-in with a NULL customer id. The right table has three customers, and one of them has no order in the excerpt. '
                         'An inner join keeps only the keys found in both tables, so two records. The walk-in disappears. A left join keeps every record of the left table, so three records, and the walk-in gets NULL for the loyalty tier. '
                         'Full outer and right joins exist, but SQLite added them only in version 3.39. At the time of writing Colab has an older version, 3.37, which lacks them, and you can always swap the tables of a left join. Which join would you use to list every order with its customer tier?')))

    # 11 inner join
    S.append(dict(kind='code', title='INNER JOIN with aliases: revenue by region',
                  code=Q_INNER, output=F['out']['inner'],
                  reads=['FROM orders AS o gives the table a short name, an alias.', 'ON says which variables must match: the join key.', 'Each branch appears once in branches, so the join is many-to-one and keeps every order.',
                         f'{F["region_top"]} leads: UGX {n(F["region_top_rev"])} from {n(F["region_top_orders"])} orders.'],
                  notes=(f'This query joins orders to branches and adds up revenue by region. Notice the aliases: orders AS o and branches AS b. They are short names that make the query easier to read. '
                         'ON says which variables must match, the join key. Each branch appears once in the branches table, so this is a many-to-one join and every order finds exactly one branch. The row count does not change. '
                         f'{F["region_top"]} leads with {n(F["region_top_rev"])} shillings from {n(F["region_top_orders"])} orders. The same fan-out danger from last session applies in SQL: if the right table repeated the key, revenue would be inflated. Which table would you join to get revenue by product category?')))

    # 12 left join
    t = F['tier']
    S.append(dict(kind='code', title='LEFT JOIN keeps the walk-in orders, and their loyalty tier is NULL',
                  code=Q_LEFT, output=F['out']['left'],
                  reads=['Every order is kept, so the counts add up to all orders.', f'The NULL group holds the {n(t["NULL"])} walk-in orders: no customer, so no match.',
                         f'An INNER JOIN to customers would return {n(F["inner_rows"])} rows, which is {n(F["left_rows"] - F["inner_rows"])} fewer than the {n(F["left_rows"])} orders.', 'GROUP BY puts all NULL values into one group.'],
                  notes=(f'Here is the left join in action. We join orders to customers and count orders by loyalty tier. Every order is kept, so the counts add up to {n(F["left_rows"])}. '
                         f'The group with a NULL tier holds {n(t["NULL"])} orders: these are the walk-ins, who have no customer record to match. An inner join would have returned only {n(F["inner_rows"])} rows, and the report would silently lose those sales. '
                         'Notice that GROUP BY puts all the NULL values together into one group. Is a walk-in order a problem to fix, or a fact to report?')))

    # 13 three valued logic
    S.append(dict(kind='idea', title='A test on NULL is neither true nor false, so WHERE drops the record',
                  visual=dict(kind='ds_three_valued', test="customer_id <> 'C0495'", rows=F['tv_rows'],
                              counts=[('TRUE: kept', n(F['t_true'])), ('FALSE: dropped', n(F['t_false'])), ('UNKNOWN: dropped', n(F['t_null']))]),
                  lead='Three-valued logic: a test can be TRUE, FALSE or UNKNOWN.',
                  points=['NULL means unknown, so any comparison with it is UNKNOWN.', 'WHERE keeps only TRUE.', "To find NULL, write IS NULL. To keep it in a test, add OR customer_id IS NULL."],
                  notes=(f'Now NULL, the source of most silent SQL mistakes. NULL means unknown. If you ask whether an unknown value is different from C0495, the answer is unknown: it is neither true nor false. SQL has three values: TRUE, FALSE and UNKNOWN. '
                         f'WHERE keeps only the records where the test is TRUE. So a test for customer id not equal to C0495 keeps {n(F["t_true"])} orders, finds {n(F["t_false"])} that equal C0495, and quietly drops the {n(F["t_null"])} walk-ins, which are UNKNOWN. '
                         'The three numbers add up to every order. To test for NULL write IS NULL, never equals NULL. What would the test return for a walk-in if you wrote customer id equals NULL?')))

    # 14 null counts
    S.append(dict(kind='code', title='IS NULL finds the missing values that an equals test cannot see',
                  code=Q_NULL, output=F['out']['null'],
                  reads=["SUM(customer_id <> 'C0495') adds up the TRUE results: 1 for TRUE, nothing for UNKNOWN.", "SUM(customer_id = 'C0495') adds up the orders of that customer.", 'SUM(customer_id IS NULL) counts the NULL values.',
                         f'The three add up to {n(F["records"])}, every order.'],
                  notes=(f'This query counts the three outcomes of the test. In SQLite a TRUE result counts as one, so a sum of a test counts the records that pass. The first column, not equal to C0495, gives {n(F["t_true"])}. The second, equal to C0495, gives {n(F["t_false"])}. '
                         f'The third, IS NULL, gives {n(F["t_null"])}. Together they make {n(F["records"])}, every order in the file. If you had trusted the not equal test alone, you would have lost the walk-ins. '
                         'A good habit: whenever a variable can be NULL, count the NULL values first. Which variable in the returns table could have NULL values?')))

    # 15 case
    S.append(dict(kind='code', title='CASE WHEN makes a new categorical variable inside a query',
                  code=Q_CASE, output=F['out']['case'],
                  reads=['CASE tests the conditions from top to bottom and returns the first match.', 'ELSE catches everything left.', 'It is the IF function of SQL. The pandas twin is pd.cut with right=False.', 'The bands are in UGX: Small under 20,000, Medium under 100,000, Large the rest.', 'SQLite lets GROUP BY use the alias band. Other databases need the CASE expression repeated.'],
                  notes=(f'CASE WHEN is the IF of SQL. It tests the conditions from top to bottom and returns the value of the first one that is true. ELSE catches everything left. Here we turn the order value into a band: Small under twenty thousand shillings, Medium under a hundred thousand, and Large for the rest. '
                         f'Then GROUP BY band counts the orders in each: {n(F["bands"]["Medium"])} Medium, {n(F["bands"]["Small"])} Small and {n(F["bands"]["Large"])} Large. In pandas the same job is done with pd.cut with right equals False, so that an order of exactly 20,000 falls in Medium as it does in SQL, and then the counts agree. SQLite lets GROUP BY use the alias band. Other databases need the CASE expression written again. '
                         'Why is the order of the WHEN lines important?')))

    # 16 subquery
    S.append(dict(kind='code', title='A subquery is a query inside brackets that supplies a value to another query',
                  code=Q_SUB, output=F['out']['sub'],
                  reads=[f'The inner query computes the average unit price: UGX {F["avg_price"]:,.0f}.', 'The outer query counts the products priced above it.', f'{F["above_avg"]} of {F["n_products"]} products are above average.', 'The inner query runs first.'],
                  notes=(f'A subquery is a query inside brackets that provides a value to another query. The inner query computes the average unit price of all products, about {F["avg_price"]:,.0f} shillings. '
                         f'The outer query then counts the products priced above that average. The answer is {F["above_avg"]} out of {F["n_products"]}. In Excel you would put the average in a helper cell and compare with it. '
                         'The subquery is that helper cell, hidden inside the query. In pandas it is a comparison with the mean. How could you count the products below average?')))

    # 17 CTE
    S.append(dict(kind='code', title='A CTE (WITH) names a subquery first, so the main query reads in order',
                  code=Q_CTE, output=F['out']['cte'],
                  reads=['WITH names a temporary result: a common table expression (CTE).', 'by_branch has one record per branch.', 'The main query then reads it like a table.', f'It finds {F["n_branches"]} branches and a best revenue of UGX {n(F["best_rev"])}.'],
                  notes=(f'A common table expression, or CTE, starts with the word WITH. It gives a name to a subquery, here by branch, which has one record per branch. The main query below then reads it like an ordinary table. '
                         f'We count the branches, {F["n_branches"]}, and find the best revenue, {n(F["best_rev"])} shillings. A CTE does the same job as a subquery, but it reads from top to bottom, which is easier when a query has several steps. '
                         'Analysts at banks and telecoms use CTEs all the time. Which is easier for you to read, a subquery or a CTE?')))

    # 18 sqlite3 and pandas
    S.append(dict(kind='code', title='sqlite3 and pandas.read_sql: run SQL in Colab and compare with pandas',
                  code='# orders is loaded from orders.csv\n' + C_PY, output=F['out']['py'],
                  reads=['sqlite3.connect opens the database file.', 'read_sql runs a SQL query and returns a DataFrame.', f'The pandas filter gives the same answer: {n(F["b04_orders"])} orders at branch B04.', 'a == b prints True when SQL and pandas agree.'],
                  notes=(f'This is the habit for the whole lab. Python talks to SQLite with the sqlite3 library. Connect opens the database file, and pandas read underscore sql runs a query and hands back a DataFrame. '
                         f'The SQL query counts the orders at branch B04, and the pandas filter on the orders file counts the same thing. Both give {n(F["b04_orders"])}, and the last print says True. '
                         'When two independent methods agree, you can trust the number. When they disagree, one of them is wrong, and finding out which teaches you the most. What would you compare next?')))

    # 19 side by side
    S.append(dict(kind='table', title='SQL and pandas side by side: the same answer, written two ways',
                  headers=['Question', 'SQL', 'pandas'],
                  rows=[['Revenue by branch', 'GROUP BY branch_id with SUM', 'groupby then sum'], ['Groups with more than 450 returns', 'HAVING COUNT(*) > 450', 'value_counts, then a filter'],
                        ['Add the region to each order', 'INNER JOIN or LEFT JOIN ... ON', 'merge on the key'], ['Order value in bands', 'CASE WHEN ... END', 'pd.cut(..., right=False)'],
                        ['Walk-in orders', 'WHERE customer_id IS NULL', 'isna().sum()'], ['Products above the average price', 'a subquery with AVG', 'a comparison with mean()']],
                  widths=[4.0, 4.0, 4.0], icons=['chart', 'check', 'key', 'tag', 'person', 'coin'],
                  notes=('Here is a cheat sheet that you will build yourself in the lab. Each row is a question we answered today, with the SQL and the pandas version. Revenue by branch is GROUP BY with SUM, or groupby and sum. '
                         'Groups above a size use HAVING, or value counts and a filter. Adding the region is a join, or a merge. Bands are CASE WHEN, or pd.cut with right equals False. Walk-ins are IS NULL, or isna. '
                         'And products above the average price use a subquery, or a comparison with the mean. The lab asks you to reproduce three SQL answers in pandas and compare them. Which direction is easier for you, SQL or pandas?')))

    # 19b dialects
    S.append(dict(kind='table', title='Your employer\'s database may not be SQLite: four places where the dialect differs',
                  headers=['Task', 'SQLite (the lab)', 'Other databases (check the documentation)'],
                  rows=[['Month of a date', "strftime('%Y-%m', order_date)", 'PostgreSQL: DATE_TRUNC or TO_CHAR. SQL Server: FORMAT or DATEFROMPARTS. MySQL: DATE_FORMAT.'],
                        ['Keep the first rows', 'LIMIT 3', 'SQL Server and Access: SELECT TOP 3. Oracle: FETCH FIRST 3 ROWS ONLY.'],
                        ['A SELECT alias in WHERE', 'Accepted', 'The SQL standard and many databases refuse it. Repeat the expression or use a CTE.'],
                        ['RIGHT and FULL OUTER JOIN', 'Only from version 3.39', 'Available in PostgreSQL, SQL Server, Oracle and MySQL (full outer join in MySQL needs a workaround).']],
                  widths=[2.8, 3.6, 5.6], icons=['calendar', 'clock', 'question', 'key'], note='The ideas carry over. The spelling of a few functions changes, so keep the documentation open at work.',
                  notes=('The lab runs on SQLite, but a bank or a telecom may run PostgreSQL, SQL Server, Oracle or MySQL. The ideas you learned today carry over, and four details change. '
                         'Dates: SQLite uses strftime to cut a month out of a date, and the others have their own functions. To keep the first rows, SQLite uses LIMIT, while SQL Server uses TOP. '
                         'SQLite accepts a SELECT alias in WHERE, and many other databases refuse it, so write the portable version. And right and full outer joins arrived in SQLite only recently. '
                         'Always check the documentation of the database you are given. Which database does your employer use?')))

    # 20 use at work
    S.append(dict(kind='table', title='Where you will use this at work: ask the company database directly',
                  headers=['Your job', 'The tables you meet', 'What today lets you do with your own tables'],
                  rows=[['Credit analyst at a bank in Kampala, using SQL', f'loans: one record per loan. customers: one per borrower.', 'GROUP BY branch and month for arrears. LEFT JOIN to keep borrowers with no loan.'],
                        ['Revenue analyst at a mobile money or telecom company', 'Transactions, agents and regions.', 'Join, group and rank agents with a CTE, then export the result to Excel or Power BI.'],
                        ['Health records officer at a district office', 'Clinic reports: one record per district per month.', 'COUNT the blank months with IS NULL before totalling a district.'],
                        ['Data analyst at a retailer or an NGO', 'Orders, products, branches or beneficiaries.', 'Answer a manager question in minutes, and prove it with a pandas check.']],
                  widths=[3.4, 4.2, 4.4], icons=['coin', 'phone', 'clinic', 'chart'],
                  notes=('Where will you use this on Monday? Four examples. A credit analyst at a bank in Kampala uses SQL to group loans by branch and month, and a left join to keep borrowers who have no loan. '
                         'A revenue analyst at a mobile money or telecom company joins transactions to agents and regions and ranks the agents with a CTE, then exports the result to Excel or Power BI. '
                         'A health records officer counts the blank months with IS NULL before totalling a district. And an analyst at a retailer or an NGO answers a manager in minutes and proves it with a pandas check. '
                         'Employers often list SQL in job adverts for exactly these roles. Which example is closest to your job?')))

    # 21 bridge
    S.append(dict(kind='code', title='Read the recipe before the lab: one query with every clause',
                  code=("SELECT b.region,\n       SUM(o.order_value_ugx) AS revenue\nFROM orders AS o\nLEFT JOIN branches AS b\n       ON o.branch_id = b.branch_id\nWHERE o.promo_week = 0\nGROUP BY b.region\nHAVING SUM(o.order_value_ugx) > 1e8\nORDER BY revenue DESC\nLIMIT 3;"),
                  reads=['SELECT and FROM name what to return and where from.', 'LEFT JOIN ... ON adds the region and keeps every order.', 'WHERE filters records before grouping.', 'GROUP BY and HAVING make groups and filter them.', 'ORDER BY and LIMIT sort and cut.'],
                  notes=('Before the lab, read one query that uses every clause. SELECT and FROM say what to return and from where. LEFT JOIN with ON adds the region and keeps every order. WHERE filters records before grouping. '
                         'GROUP BY and HAVING make groups and filter the groups. ORDER BY and LIMIT sort and cut. Remember the order of execution: FROM and JOIN, WHERE, GROUP BY, HAVING, SELECT, ORDER BY, LIMIT. '
                         'In the lab you write ten steps of queries, and for four of them you run the pandas twin and compare. Which clause in this query runs first?')))

    # 22 divider
    S.append(dict(kind='divider', title='Part 2: the SQL lab', lead='Close the slides. Open the notebook.', section='Lab',
                  notes=('That is the end of the ideas. Everything you need is on the slides you have just seen, and the notebook repeats each step. '
                         'Open the notebook for Session 10 in Google Colab. Run the first cell, which puts the course data files and the database next to the notebook, and then the check cell. '
                         'In every step, write your prediction before you run the query. Then read the result, and change one thing.')))

    # 23 lab map
    S.append(dict(kind='steps', title='The lab has ten steps and ends with a proof table you keep',
                  steps=[dict(head='1 Look', text='List tables, count rows', icon='folder'), dict(head='2 to 4 Group', text='WHERE, GROUP BY, HAVING', icon='chart'),
                         dict(head='5 to 6 Join', text='INNER and LEFT JOIN', icon='key'), dict(head='7 to 9 More SQL', text='NULL, CASE, subquery, CTE', icon='question'),
                         dict(head='10 Prove', text='SQL against pandas', icon='check')], highlight=None,
                  caption='Ten steps in 45 minutes. For each: predict, run, read, change. Four answers are rebuilt in pandas, and your proof table (a reconciliation of the SQL answer against the pandas answer) records the match.',
                  notes=('Here is the map of the lab, in ten steps. Step one, connect to the database, list the tables and count rows. Steps two to four, filter with WHERE, group with GROUP BY and filter groups with HAVING. '
                         'Steps five and six, write an inner join and a left join and see what each keeps. Steps seven to nine, handle NULL, write a CASE WHEN, a subquery and a CTE. Step ten, compare the four SQL answers you rebuilt in pandas in a proof table. '
                         'Each task has a check that tells you whether your number matches. If it says not yet, read the output again before you ask me. Please do not skip the predictions.')))

    # 24 check numbers
    S.append(dict(kind='table', title='Check your numbers before you move on', headers=['What you compute', 'You should get'],
                  rows=[['Tables in the database, and records in orders', f'{F["n_tables"]} and {n(R["orders"])}'], ['Card orders at branch B06', n(F['n_card_b06'])],
                        ['Top branch by revenue in SQL', f'{F["top_branch"]}, UGX {n(F["top_rev"])}'], ['Return reasons with more than 450 records', ', '.join(f'{a} {n(b_)}' for a, b_ in F['reasons'])],
                        ['Inner join to customers: rows, against the left join', f'{n(F["inner_rows"])} against {n(F["left_rows"])}'], ['Walk-in orders (IS NULL)', n(F['t_null'])],
                        ['Medium, Small and Large orders', f'{n(F["bands"]["Medium"])}, {n(F["bands"]["Small"])} and {n(F["bands"]["Large"])}'], ['Products above the average price', f'{F["above_avg"]} of {F["n_products"]}']],
                  widths=[7.0, 5.0], icons=['folder', 'tag', 'chart', 'cross', 'key', 'person', 'calculator', 'coin'], note='If your number differs, find the task that went wrong. Do not change a number to match.',
                  notes=('Use this table as your own self-check. Nobody marks it. If your numbers match, carry on. If one does not, stop and call me. '
                         'The most common causes are a missing quote around text, a count taken from the wrong table, and a join on the wrong variable. Do not change a number to make it match. Find out why it is different. '
                         'Remember that SQL and pandas must agree, so if your SQL answer is different from your pandas answer, one of them has a mistake. Where would you look first?')))

    # 25 error cards
    S.append(dict(kind='table', title='Five likely mistakes in the lab and how to fix them', headers=['What you see', 'What it means', 'What to do'],
                  rows=[['no such column: branch_name', 'The variable is in another table, or misspelt.', 'Check the table with SELECT * FROM table LIMIT 3.'],
                        ['misuse of aggregate: COUNT()', 'An aggregate is in WHERE.', 'Move the test to HAVING.'],
                        ['A WHERE test returns fewer records than expected', 'NULL values make the test UNKNOWN.', 'Count IS NULL first, and add OR variable IS NULL if needed.'],
                        ['Revenue much bigger after a JOIN', 'The right table repeats the key: fan-out.', 'Count the rows before and after. Summarise the right table first.'],
                        ['The result order changes between runs', 'No ORDER BY, so the order is not defined.', 'Add ORDER BY, with a second variable to break ties.']],
                  widths=[3.8, 4.0, 4.2], icons=['cross', 'cross', 'question', 'cross', 'clock'],
                  notes=('Five messages and symptoms you may meet. No such column means the variable is in another table or misspelt, so look at the first rows of the table. '
                         'Misuse of aggregate means you put an aggregate in WHERE, so move it to HAVING. A test that returns fewer records than you expected is usually NULL, so count the NULL values first. '
                         'Revenue much bigger after a join is fan-out, so count the rows before and after. And a result that changes order between runs has no ORDER BY. Read the message first. It usually tells you the answer.')))

    # 26 exit
    S.append(dict(kind='table', title='Exit check: three questions, then compare with the short answers', headers=['Question', 'Short answer'],
                  rows=[['Which clause runs first in a SQL query, and which runs fifth?', 'FROM runs first. SELECT runs fifth, after WHERE, GROUP BY and HAVING. That is why the SQL standard does not let WHERE use an alias made in SELECT. SQLite allows it, many databases do not.'],
                        [f'An INNER JOIN of orders to customers returns {n(F["inner_rows"])} rows and a LEFT JOIN returns {n(F["left_rows"])}. Why?', f'{n(F["t_null"])} orders have a NULL customer_id, so they have no match. The inner join drops them and the left join keeps them.'],
                        ["Why does WHERE customer_id <> 'C0495' not return the walk-in orders?", 'A comparison with NULL is UNKNOWN, and WHERE keeps only TRUE. Add OR customer_id IS NULL.']],
                  widths=[5.2, 6.8], icons=['clock', 'key', 'question'],
                  notes=('Last, the exit check. Three questions. Write your answers before you look at mine. One, which clause runs first in a SQL query, and which runs fifth? '
                         f'Two, an inner join of orders to customers returns {n(F["inner_rows"])} rows and a left join returns {n(F["left_rows"])}. Why? Three, why does a WHERE test for customer id not equal to C0495 not return the walk-in orders? '
                         'The short answers are on the slide. If you got all three, you are ready for charts next session. If one surprised you, look at that part of your notebook again tonight.')))

    # ------------------------------------------------------------------ facilitator
    sess['facilitator'] = dict(
        prep=['Open the Session 10 notebook in Colab on your own account and run it top to bottom once. Confirm that every check passes.',
              'Make sure data.zip contains lakeside.db. The notebook builds the database from the CSV files if lakeside.db is missing, so either works.',
              'Write the check table (slide 24) on the board before the lab.', 'Concepts run with laptops closed. Ask learners to open Colab only after the Part 2 divider.',
              'SQLite is free and needs no account. SQLite before version 3.39 (Colab at the time of writing has 3.37) has no RIGHT JOIN or FULL OUTER JOIN: teach INNER and LEFT, and swap the tables if a right join is needed. SQLite accepts a SELECT alias in WHERE and GROUP BY; say that the standard and many databases do not.'],
        misconceptions=[('SQL runs the clauses in the order I write them', 'The logical order is FROM, WHERE, GROUP BY, HAVING, SELECT, ORDER BY, LIMIT. It explains why the SQL standard forbids a SELECT alias in WHERE (SQLite is the exception).'),
                        ('WHERE and HAVING are the same', 'WHERE filters records before grouping. HAVING filters groups after. Only HAVING can test an aggregate.'),
                        ('customer_id <> X keeps every customer who is not X', f'It drops NULL as well. {n(F["t_null"])} walk-in orders disappear unless you add OR customer_id IS NULL.'),
                        ('COUNT(*) and COUNT(variable) are the same', f'COUNT(*) counts records: {n(F["records"])}. COUNT(customer_id) skips NULL: {n(F["filled"])}.'),
                        ('A table has a first row and a last row', 'A database table is a set of records. Without ORDER BY the order is not defined, so LIMIT alone returns any rows.')],
        probes=[('What is a relational database?', 'Several tables linked by keys, stored together.'), ('What does GROUP BY do?', 'Makes one group per value, so each aggregate function returns one value per group.'),
                ('Which clause filters groups?', 'HAVING.'), ('What does an INNER JOIN keep?', 'Only the records whose key is found in both tables.'),
                ('What does a LEFT JOIN do with a record that has no match?', 'Keeps it and fills the right-hand variables with NULL.'), ('How do you find missing values in SQL?', 'IS NULL, never equals NULL.'),
                ('What is a CTE?', 'A named temporary result created with WITH, so a multi-step query reads from top to bottom.'), ('How do you know a SQL answer is right?', 'Rebuild it in pandas and compare.')],
        lab_steps=[('Step 1: tables and counts', f'{F["n_tables"]} tables. {n(R["orders"])} orders. B06 card orders: {n(F["n_card_b06"])}.'),
                   ('Step 2: GROUP BY, HAVING', f'{F["top_branch"]} leads with {n(F["top_rev"])}. HAVING returns {len(F["reasons"])} reasons. Watch for HAVING written as WHERE.'),
                   ('Step 3: joins', f'Region revenue: {F["region_top"]} leads with {n(F["region_top_rev"])}. Left join {n(F["left_rows"])} rows against inner {n(F["inner_rows"])}.'),
                   ('Step 4: NULL, CASE, subquery, CTE', f'Walk-ins {n(F["t_null"])}. Bands {n(F["bands"]["Medium"])}, {n(F["bands"]["Small"])}, {n(F["bands"]["Large"])}. {F["above_avg"]} products above average. CTE best revenue {n(F["best_rev"])}.'),
                   ('Step 5: proof table', 'Every row shows SQL answer, pandas answer and True. A False row means a mistake in one of them. Praise the learner who finds it.')],
        rescue=['If the concepts run over, shorten slide 3 (the translation table) and slide 17 (CTE). The lab repeats both.', 'If only 30 minutes of lab remain, do steps 1, 2 and 3 and set the rest as homework.',
                'If Colab cannot find lakeside.db, the notebook builds it from the CSV files. Run the first cell again.', 'If a learner has no laptop, pair them with a neighbour: one types, one predicts aloud.'],
        after=['Share the notebook and the deck again for learners who were absent.', 'Ask each learner to save the proof table and bring one question from their own database to Session 11.', 'Note any question you could not answer and open the next session with it.'],
        lab_answer_key=[['Step 1 PREDICT: how many tables are in the database?', f'{F["n_tables"]}: ' + ', '.join(F['tables']) + '.'],
                        ['Step 2 READ: which branch leads, and does the pandas groupby agree?', f'{F["top_branch"]} ({F["top_branch_name"]}), UGX {n(F["top_rev"])}. Yes, the two are identical.'],
                        ['Step 2 CHANGE: use HAVING COUNT(*) > 470 instead of 450.', f'Damaged ({n(F["reasons_all"]["Damaged"])}) and Wrong item ({n(F["reasons_all"]["Wrong item"])}) stay. Expired has {n(F["reasons_all"]["Expired"])}, so it drops out.'],
                        ['Step 3 PREDICT: which join returns more rows, INNER or LEFT?', f'LEFT: {n(F["left_rows"])} against {n(F["inner_rows"])}, because it keeps the walk-ins.'],
                        ['Step 4 PREDICT: does customer_id <> C0495 return the walk-ins?', f'No. It returns {n(F["t_true"])} orders. The {n(F["t_null"])} NULL records are UNKNOWN and dropped.'],
                        ['Step 4 READ: which band is largest?', f'Medium with {n(F["bands"]["Medium"])}.'],
                        ['Step 4 CHANGE: count products below average.', f'{F["below_avg"]} of {F["n_products"]}. Together with the {F["above_avg"]} above average and {F["equal_avg"]} equal to it they make {F["n_products"]}.'],
                        ['Step 5 READ: what does a False in the proof table mean?', 'The SQL and pandas answers differ. One of them has a mistake: check the join type, a NULL test or a missing filter.']])
    return sess
