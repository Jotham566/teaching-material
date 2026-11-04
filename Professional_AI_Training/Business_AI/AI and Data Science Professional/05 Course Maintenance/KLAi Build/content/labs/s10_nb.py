"""Session 10 lab notebook: SQL for analysts. Expected numbers come from content/s10.py facts() (SQL on lakeside.db asserted equal to pandas on the CSV files)."""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
BUILD = HERE.parents[2]
sys.path.insert(0, str(BUILD / 'kit'))
import nb as NB  # noqa: E402

_sp = importlib.util.spec_from_file_location('s10_facts', BUILD / 'content' / 's10.py')
_m = importlib.util.module_from_spec(_sp)
_sp.loader.exec_module(_m)
F = _m.facts()

TITLE = 'SQL for analysts'


def merge_checks(nb):
    out = []
    for c in nb.cells:
        src = ''.join(c['source'])
        if c['cell_type'] == 'code' and src.startswith('check(') and out and out[-1]['cell_type'] == 'code':
            prev = ''.join(out[-1]['source'])
            out[-1]['source'] = NB._src(prev + '\n\n# Automatic check\n' + src)
        else:
            out.append(c)
    nb.cells = out


def build(solution: bool):
    nb = NB.Notebook()
    R = F['rows']
    nb.md('# Session 10 lab: SQL for analysts\n\n**Question of the day:** How do we ask a database the same questions in the language every employer uses?\n\n'
          'In every step: **predict** first, run the query, **read** the result, then **change** one thing. For four queries you rebuild the answer in pandas, and a proof table records whether SQL and pandas agree. '
          'You keep this notebook as your query book.\n\nData: Lakeside Mart (fictional, generated), in a free SQLite database. Revenue describes a 5 percent sample of till orders.')
    nb.data_setup()
    nb.check_setup()
    nb.code('import os\nimport sqlite3\nimport pandas as pd\n\n'
            '# If lakeside.db did not arrive with the data files, build it from the CSV files (same tables).\n'
            'TABLES = ["branches", "products", "customers", "orders", "order_lines", "returns", "branch_weeks", "offer_test", "feedback"]\n'
            'if not os.path.exists("lakeside.db"):\n'
            '    _con = sqlite3.connect("lakeside.db")\n'
            '    for t in TABLES:\n'
            '        pd.read_csv(t + ".csv").to_sql(t, _con, index=False)\n'
            '    _con.close()\n'
            'con = sqlite3.connect("lakeside.db")\n\n'
            'def q(sql):\n'
            '    """Run a SQL query and return a DataFrame."""\n'
            '    return pd.read_sql_query(sql, con)\n\n'
            'orders = pd.read_csv("orders.csv")\nbranches = pd.read_csv("branches.csv")\ncustomers = pd.read_csv("customers.csv")\n'
            'returns = pd.read_csv("returns.csv")\nproducts = pd.read_csv("products.csv")\n\n'
            '# The proof table: one row for every SQL answer that you rebuild in pandas. Run this cell once.\n'
            'proof = []\n'
            'def compare(name, sql_value, pandas_value):\n'
            '    proof.append(dict(query=name, sql=sql_value, pandas=pandas_value, match=bool(sql_value == pandas_value)))\n'
            'def safe(f):\n'
            '    try:\n        return f()\n    except Exception:\n        return -1   # lets a check say NOT YET instead of stopping\n')

    # step 1
    nb.step(1, 'Look at the database', 'A relational database is several tables linked by keys. SQLite keeps its list of tables in sqlite_master.')
    nb.predict('How many tables does the database hold? How many records does orders have?')
    if solution:
        nb.code("tables = q(\"SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name\")\nn_orders = q('SELECT COUNT(*) AS n FROM orders').n[0]\nprint(tables.name.tolist(), n_orders)")
    else:
        nb.code("tables = None    # SELECT name FROM sqlite_master WHERE type = 'table'\nn_orders = None  # SELECT COUNT(*) AS n FROM orders, then take the number with .n[0]")
    nb.code(f"check('tables in the database', safe(lambda: len(tables)), {F['n_tables']})\ncheck('records in orders', safe(lambda: n_orders), {R['orders']})")
    nb.change('Run SELECT * FROM branches LIMIT 3. Which variable is the primary key?')

    # step 2
    nb.step(2, 'SELECT, WHERE, ORDER BY, LIMIT', 'WHERE keeps records. ORDER BY sorts. LIMIT keeps the first few.')
    nb.predict('How many orders were paid by Card at branch B06? What would change if you removed ORDER BY from the second query?')
    if solution:
        nb.code("n_card = q(\"SELECT COUNT(*) AS n FROM orders WHERE branch_id = 'B06' AND payment_method = 'Card'\").n[0]\n"
                "top3 = q(\"\"\"SELECT order_id, order_value_ugx FROM orders\n          WHERE branch_id = 'B06' AND payment_method = 'Card'\n          ORDER BY order_value_ugx DESC, order_id LIMIT 3\"\"\")\nprint(n_card)\ntop3")
    else:
        nb.code("n_card = None   # SELECT COUNT(*) AS n ... WHERE branch_id = 'B06' AND payment_method = 'Card'\n"
                "top3 = None     # the three largest of those orders: order_id, order_value_ugx, ORDER BY ... DESC, LIMIT 3")
    nb.code(f"check('B06 card orders', safe(lambda: n_card), {F['n_card_b06']})\ncheck('top three order values', safe(lambda: list(top3.order_value_ugx)), {[int(v) for v in F['sel'].order_value_ugx]})")
    nb.read('Why do we add order_id after order_value_ugx in ORDER BY?')

    # step 3
    nb.step(3, 'GROUP BY, and the pandas twin', 'GROUP BY makes one result record per group. Then rebuild the same answer with groupby and compare.')
    nb.predict('Which branch will have the largest revenue? Will pandas groupby give exactly the same number?')
    if solution:
        nb.code("by_branch = q(\"\"\"SELECT branch_id, COUNT(*) AS orders, SUM(order_value_ugx) AS revenue\n                FROM orders GROUP BY branch_id ORDER BY revenue DESC\"\"\")\n"
                "twin = orders.groupby('branch_id')['order_value_ugx'].sum().sort_values(ascending=False)\n"
                "compare('revenue of the top branch', int(by_branch.revenue[0]), int(twin.iloc[0]))\nprint(by_branch.head(3))")
    else:
        nb.code("by_branch = None   # SELECT branch_id, COUNT(*) AS orders, SUM(order_value_ugx) AS revenue ... GROUP BY ... ORDER BY revenue DESC\n"
                "twin = None        # the same revenue per branch with groupby, sorted largest first\n# then: compare('revenue of the top branch', sql_value, pandas_value)")
    nb.code(f"check('top branch revenue', safe(lambda: by_branch.revenue[0]), {F['top_rev']})\ncheck('pandas twin agrees', safe(lambda: twin.iloc[0]), {F['top_rev']})")
    nb.read('Do the SQL and pandas answers agree? What does the match column of the proof table say?')

    # step 4
    nb.step(4, 'HAVING filters groups', 'WHERE filters records before grouping. HAVING filters groups after.')
    nb.predict('Which return reasons have more than 450 returns?')
    if solution:
        nb.code("common = q(\"\"\"SELECT reason, COUNT(*) AS n FROM returns\n             GROUP BY reason HAVING COUNT(*) > 450 ORDER BY n DESC\"\"\")\ncommon")
    else:
        nb.code("common = None   # GROUP BY reason, then HAVING COUNT(*) > 450")
    nb.code(f"check('reasons above 450', safe(lambda: len(common)), {len(F['reasons'])})\ncheck('largest reason count', safe(lambda: common.n[0]), {F['reasons'][0][1]})")
    nb.change('Change 450 to 470. Which reasons remain? Then write the same filter with WHERE and see the error message.')

    # step 5
    nb.step(5, 'INNER JOIN with aliases', 'ON names the join key. An alias such as o or b is a short name for a table.')
    nb.predict('Joining orders to branches adds the region. Will the row count of the join change? Which region leads?')
    if solution:
        nb.code("by_region = q(\"\"\"SELECT b.region, COUNT(*) AS orders, SUM(o.order_value_ugx) AS revenue\n                FROM orders AS o INNER JOIN branches AS b ON o.branch_id = b.branch_id\n                GROUP BY b.region ORDER BY revenue DESC\"\"\")\n"
                "twin_region = orders.merge(branches, on='branch_id', validate='m:1').groupby('region')['order_value_ugx'].sum().sort_values(ascending=False)\n"
                "compare('revenue of the top region', int(by_region.revenue[0]), int(twin_region.iloc[0]))\nby_region")
    else:
        nb.code("by_region = None    # JOIN orders AS o to branches AS b ON the branch_id, GROUP BY b.region, SUM, ORDER BY revenue DESC\n"
                "twin_region = None  # the pandas twin: merge (validate='m:1'), groupby region, sum, sort\n# then compare(...)")
    nb.code(f"check('top region revenue', safe(lambda: by_region.revenue[0]), {F['region_top_rev']})\ncheck('top region orders', safe(lambda: by_region.orders[0]), {F['region_top_orders']})")
    nb.read('Add up the four region revenues. What number should you get? Why?')

    # step 6
    nb.step(6, 'LEFT JOIN keeps the walk-ins', 'A left join keeps every record of the left table. Records with no match get NULL.')
    nb.predict('Count orders by loyalty tier with a LEFT JOIN to customers. How many orders will have a NULL tier?')
    if solution:
        nb.code("tiers = q(\"\"\"SELECT c.loyalty_tier, COUNT(*) AS orders\n             FROM orders AS o LEFT JOIN customers AS c ON o.customer_id = c.customer_id\n             GROUP BY c.loyalty_tier ORDER BY orders DESC\"\"\")\n"
                "n_inner = q(\"\"\"SELECT COUNT(*) AS n FROM orders AS o INNER JOIN customers AS c ON o.customer_id = c.customer_id\"\"\").n[0]\n"
                "null_tier = int(tiers.loc[tiers.loyalty_tier.isna(), 'orders'].iloc[0])\nprint(tiers)\nprint(n_inner)")
    else:
        nb.code("tiers = None       # LEFT JOIN customers AS c ON the customer_id, GROUP BY c.loyalty_tier, COUNT(*)\nn_inner = None     # the same join with INNER JOIN, just COUNT(*)\nnull_tier = None   # the number of orders whose tier is NULL")
    nb.code(f"check('orders with a NULL tier', safe(lambda: null_tier), {F['t_null']})\ncheck('rows of the inner join', safe(lambda: n_inner), {F['inner_rows']})")
    nb.change('Replace LEFT JOIN with INNER JOIN in the first query. Which group disappears?')

    # step 7
    nb.step(7, 'NULL and three-valued logic', "A test on NULL is UNKNOWN, and WHERE keeps only TRUE. Use IS NULL to find missing values.")
    nb.predict("How many orders have customer_id <> 'C0495'? Will the walk-in orders be among them?")
    if solution:
        nb.code("not_c0495 = q(\"SELECT COUNT(*) AS n FROM orders WHERE customer_id <> 'C0495'\").n[0]\nwalk_in = q('SELECT COUNT(*) AS n FROM orders WHERE customer_id IS NULL').n[0]\nprint(not_c0495, walk_in, not_c0495 + walk_in)")
    else:
        nb.code("not_c0495 = None   # COUNT(*) ... WHERE customer_id <> 'C0495'\nwalk_in = None     # COUNT(*) ... WHERE customer_id IS NULL")
    nb.code(f"check('not C0495', safe(lambda: not_c0495), {F['t_true']})\ncheck('walk-ins', safe(lambda: walk_in), {F['t_null']})")
    nb.read('Add the two counts and the number of orders that equal C0495. Do they make every order?')

    # step 8
    nb.step(8, 'CASE WHEN, and the pandas twin', 'CASE returns the value of the first condition that is true.')
    nb.predict('Bands: Small under 20,000, Medium under 100,000, Large the rest. Which band will have the most orders?')
    if solution:
        nb.code("bands = q(\"\"\"SELECT CASE WHEN order_value_ugx < 20000 THEN 'Small'\n                       WHEN order_value_ugx < 100000 THEN 'Medium'\n                       ELSE 'Large' END AS band,\n                  COUNT(*) AS orders\n           FROM orders GROUP BY band ORDER BY orders DESC\"\"\").set_index('band').orders\n"
                "cut = pd.cut(orders['order_value_ugx'], [0, 20000, 100000, float('inf')], right=False, labels=['Small', 'Medium', 'Large']).value_counts()\n"
                "compare('orders in the Medium band', int(bands['Medium']), int(cut['Medium']))\nprint(bands)")
    else:
        nb.code("bands = None   # CASE WHEN ... THEN ... ELSE ... END AS band, COUNT(*), GROUP BY band; keep band and orders (set_index('band').orders)\n"
                "cut = None     # the pandas twin: pd.cut on order_value_ugx with three labels, then value_counts\n# then compare(...)")
    nb.code(f"check('Medium orders', safe(lambda: bands['Medium']), {F['bands']['Medium']})\ncheck('Large orders', safe(lambda: bands['Large']), {F['bands']['Large']})")
    nb.change('Move the Small limit from 20000 to 10000. Which band changes most? Then add WHERE band = \'Small\' (an alias in WHERE) to the query. SQLite accepts it, but the SQL standard and many databases refuse it. How would you write it so that it runs everywhere?')

    # step 9
    nb.step(9, 'Subquery and CTE', 'A subquery is a query in brackets that supplies a value. A CTE (WITH) names a step so the query reads in order.')
    nb.predict('How many of the 150 products cost more than the average unit price?')
    if solution:
        nb.code("n_dear = q('SELECT COUNT(*) AS n FROM products WHERE unit_price_ugx > (SELECT AVG(unit_price_ugx) FROM products)').n[0]\n"
                "twin_n = int((products['unit_price_ugx'] > products['unit_price_ugx'].mean()).sum())\n"
                "compare('products above the average price', int(n_dear), twin_n)\n"
                "cte = q(\"\"\"WITH by_branch AS (SELECT branch_id, SUM(order_value_ugx) AS revenue FROM orders GROUP BY branch_id)\n           SELECT COUNT(*) AS branches, MAX(revenue) AS best FROM by_branch\"\"\")\nprint(n_dear, twin_n)\ncte")
    else:
        nb.code("n_dear = None   # COUNT(*) FROM products WHERE unit_price_ugx > (a subquery with AVG(unit_price_ugx))\ntwin_n = None   # the pandas twin with mean()\n"
                "cte = None      # WITH by_branch AS (...) SELECT COUNT(*) AS branches, MAX(revenue) AS best FROM by_branch\n# then compare(...)")
    nb.code(f"check('products above average', safe(lambda: n_dear), {F['above_avg']})\ncheck('best branch revenue from the CTE', safe(lambda: cte.best[0]), {F['best_rev']})")
    nb.read('Which is easier to read, the subquery or the CTE? Write one sentence.')

    # step 10
    nb.step(10, 'Keep: the proof table', 'Every row shows the SQL answer, the pandas answer and whether they match. A False means a mistake in one of them.')
    if solution:
        nb.code("proof_table = pd.DataFrame(proof)\nprint(proof_table.to_string(index=False))\nall_match = bool(proof_table.match.all())\nprint('All answers match:', all_match)")
    else:
        nb.code("proof_table = None   # pd.DataFrame(proof), then print it\nall_match = None     # True when every row of the match column is True")
    nb.code("check('proof table has four rows', safe(lambda: len(proof_table)), 4)\ncheck('every SQL answer matches pandas', safe(lambda: int(all_match)), 1)")
    nb.md('**Keep this notebook** as your query book. Save a copy to your Drive (File, Save a copy in Drive). Bring one question from your own database to Session 11.')
    merge_checks(nb)
    nb.code('show_checks()')
    return nb
