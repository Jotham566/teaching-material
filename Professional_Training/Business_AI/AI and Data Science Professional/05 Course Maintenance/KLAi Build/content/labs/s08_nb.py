"""Session 8 Python lab (Project milestone 1): pandas II, cleaning the mess. Expected values come from content/s08.py facts() (the same pipeline run with pandas)."""
import importlib.util
import sys
from pathlib import Path

BUILD = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BUILD / 'kit'))
import nb as NB  # noqa: E402

_spec = importlib.util.spec_from_file_location('s08', BUILD / 'content' / 's08.py')
S8 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(S8)

TITLE = 'pandas II cleaning the mess'


def todo(b, solution, hint, learner, model):
    b.code(('# Hint: ' + hint + '\n' if hint else '') + (model if solution else learner))


ATTEMPT = (
    '# Helper for the checks. Run this cell once. You do not need to read it.\n'
    '# attempt() runs a check on your answer. If the answer is not written yet it says NOT YET instead of stopping with an error.\n'
    'def attempt(label, expr, expected, tol=0.01):\n'
    '    try:\n'
    '        value = eval(expr)\n'
    '        want = eval(expected) if isinstance(expected, str) else expected\n'
    '    except Exception:\n'
    '        value, want = None, 0\n'
    '    check(label, value, want, tol)')


def guard(text):
    """Wrap display lines in try/except so an unfinished answer above gives a hint and not a traceback."""
    body = '\n'.join('    ' + l for l in text.split('\n'))
    return 'try:\n' + body + '\nexcept Exception:\n    print("Not yet: finish the cell above, then run this cell again.")'


def chk(label, expr, expected, tol=0):
    return f'attempt({label!r}, {expr!r}, {expected!r}, {tol})'


def build(solution):
    F = S8.facts()
    n = S8.n
    b = NB.Notebook()
    b.md('# Session 8: pandas II, cleaning the mess (Project milestone 1)\n\n**KLAi | AI and Data Science Professional**\n\n'
         'You clean a raw export of Lakeside Mart order lines (fictional, generated data) with eight planted defects. After each cleaning step you add a row to the data cleaning log. '
         'At the end you reconcile your cleaned total to the control total and name the reconciliation difference. '
         'Each step has the same rhythm: **PREDICT**, run, **READ**, then **CHANGE one thing**. A cell that says `None  # your code here` is yours to fill. The check cells say OK or NOT YET, and they keep running while an answer is still `None`.')
    b.data_setup()
    b.check_setup()
    b.code(ATTEMPT)

    b.step(1, 'Load the raw file, copy it and set up the log', 'This first cell is given, so every later step has a `raw` and a `df` to work on. We never edit the raw file. We clean a copy called `df`. The helper `note` adds one row to the data cleaning log: the step, the rows before, the rows after and the reason.')
    b.predict(f'The raw export has one record for each product on an order. How many rows do you expect: hundreds, thousands or tens of thousands?')
    b.code("import pandas as pd\n\nraw = pd.read_csv('orders_raw.csv')   # given: the raw file, never changed\ndf = raw.copy()                       # given: the copy that you clean\n\n"
           'log = []\ndef note(step, before, after, why):\n    log.append({"step": step, "rows_before": before, "rows_after": after, "why": why})\n\n'
           'print(raw.shape)\nprint(raw.dtypes)\n'
           f'check("raw rows", raw.shape[0], {F["raw_rows"]}, 0)\ncheck("df is a copy of raw", len(df), len(raw), 0)')
    b.read('Which columns are stored as object? Which of them should be a number or a date?')

    b.step(2, 'Duplicates', 'An exact duplicate repeats another record in every variable. drop_duplicates keeps the first copy. line_id is the primary key, so it must be unique afterwards.')
    b.predict('Roughly how many exact duplicate lines do you expect in 41 thousand lines: none, tens or thousands?')
    todo(b, solution, 'remember len(df) in before; df.duplicated().sum() counts the repeats; then df.drop_duplicates()',
         'before = len(df)\nn_dupes = None  # your code here: the number of duplicate lines\ndf = df  # your code here: drop the duplicates\nnote("Drop exact duplicates", before, len(df), str(n_dupes) + " identical lines")',
         'before = len(df)\nn_dupes = df.duplicated().sum()\ndf = df.drop_duplicates()\nnote("Drop exact duplicates", before, len(df), str(n_dupes) + " identical lines")')
    b.code(guard('print(n_dupes, len(df), df["line_id"].is_unique)') + '\n'
           + chk('duplicates found', 'n_dupes', F['n_dupes']) + '\n' + chk('rows after', 'len(df)', F['rows_dedup']) + '\n' + chk('line_id is unique', 'df["line_id"].is_unique', 1))
    b.change('Run df.duplicated(subset=["line_id"]).sum() before dropping (use raw). Is it the same number? Why?')

    b.step(3, 'Data types: prices and dates', 'to_numeric converts text to numbers, so remove the text UGX and the comma first. to_datetime reads dates: give it a format and errors="coerce", read each style on its own, then fillna joins the two. Dates with slashes are day/month/year.')
    b.predict('After to_numeric, what data type will unit_price have? After the two readings, how many dates should still be missing?')
    todo(b, solution, "str.replace('UGX', '') then str.replace(',', '') then pd.to_numeric. Formats: '%Y-%m-%d' and '%d/%m/%Y'",
         'p = None  # your code here: unit_price with UGX and the comma removed\ndf["unit_price"] = None  # your code here: convert p to numbers\n'
         'iso = None  # your code here: order_date read as year-month-day, errors="coerce"\nuk = None   # your code here: order_date read as day/month/year, errors="coerce"\ndf["order_date"] = None  # your code here: iso, with the gaps filled from uk',
         'p = df["unit_price"].str.replace("UGX", "").str.replace(",", "")\ndf["unit_price"] = pd.to_numeric(p)\n'
         'iso = pd.to_datetime(df["order_date"], format="%Y-%m-%d", errors="coerce")\nuk = pd.to_datetime(df["order_date"], format="%d/%m/%Y", errors="coerce")\ndf["order_date"] = iso.fillna(uk)')
    b.code('note("Price text to number", len(df), len(df), "UGX and commas removed, to_numeric")\nnote("Two date formats to dates", len(df), len(df), "slashes read day first")\n'
           + guard('print(df["unit_price"].dtype, df["order_date"].isna().sum(), df["order_date"].min().date(), df["order_date"].max().date())') + '\n'
           + chk('prices are numbers', 'df["unit_price"].dtype.kind in "iuf"', 1) + '\n' + chk('dates missing', 'df["order_date"].isna().sum()', F['n_date_nat']) + '\n'
           + chk('slash dates', 'iso.isna().sum()', F['n_iso_nat']) + '\n' + chk('latest date is 28 Dec 2025', f'df["order_date"].max() == pd.Timestamp("{F["date_max"]}")', 1))
    b.read('iso is missing for the slash dates and uk for the dash dates. Why do the two numbers add up to more than the number of rows?')
    b.change('Read the dates month first, format "%m/%d/%Y", into a new Series called us. How many become NaT? Do not store it in df.')

    b.step(4, 'Text: branch and payment', 'String methods fix text: strip, lower, title, capitalize and replace with a dictionary. Do strip and lower or title first, then the dictionary.')
    b.predict('The raw branch has 26 spellings and payment has 11. After cleaning, how many do you expect of each?')
    todo(b, solution, "branch: str.strip().str.title() then replace({'Kampala Cntral': 'Kampala Central', 'Entebe': 'Entebbe'}). payment: str.strip().str.lower(), replace({'mm': 'mobile money'}), str.capitalize()",
         'df["branch"] = None   # your code here\ndf["payment"] = None  # your code here',
         'b = df["branch"].str.strip().str.title()\ndf["branch"] = b.replace({"Kampala Cntral": "Kampala Central", "Entebe": "Entebbe"})\n'
         'pay = df["payment"].str.strip().str.lower()\ndf["payment"] = pay.replace({"mm": "mobile money"}).str.capitalize()')
    b.code('note("Branch and payment text", len(df), len(df), "26 branch spellings to 8, 11 payment spellings to 3")\n'
           + guard('print(df["payment"].value_counts())') + '\n'
           + chk('branches', 'df["branch"].nunique()', F['branch_n']) + '\n' + chk('payment methods', 'df["payment"].nunique()', F['pay_n']) + '\n'
           + chk('Mobile money lines', 'df["payment"].value_counts()["Mobile money"]', F['pay_counts']['Mobile money']))
    b.read('Which spelling had a trailing space in the raw file? Which string method removed it?')

    b.step(5, 'Missing values: flag, fill and drop', 'Flag first (an indicator variable), then fill the blank customers with the constant walk-in. The 12 lines with a blank qty cannot be recovered, so drop only those, with subset.')
    b.predict('What would happen to the row count if you called df.dropna() on the whole table instead of using subset? Write a guess, then try it in a new cell, without storing it.')
    todo(b, solution, "df['customer_id'].isna() gives the flag; fillna('walk-in'); dropna(subset=['qty'])",
         'df["customer_missing"] = None  # your code here: True where customer_id is missing\ndf["customer_id"] = None  # your code here: fill the blanks with "walk-in"\nlost = None  # your code here: the lines with a blank qty\ndf = df  # your code here: drop those lines',
         'df["customer_missing"] = df["customer_id"].isna()\ndf["customer_id"] = df["customer_id"].fillna("walk-in")\nlost = df[df["qty"].isna()]\nbefore = len(df)\ndf = df.dropna(subset=["qty"])')
    b.code(guard('note("Flag and fill blank customers", len(df) + len(lost), len(df) + len(lost), "blanks flagged, then labelled walk-in")\nnote("Drop lines with blank qty", len(df) + len(lost), len(df), str(len(lost)) + " lines, quantity cannot be recovered")\n'
                 'print(df["customer_missing"].sum(), (df["customer_id"] == "walk-in").sum(), len(lost), len(df))') + '\n'
           + chk('customers flagged', 'df["customer_missing"].sum()', F['n_flag']) + '\n' + chk('walk-in lines', '(df["customer_id"] == "walk-in").sum()', int((F['df'].customer_id == 'walk-in').sum())) + '\n'
           + chk('lines dropped', 'len(lost)', F['n_lost']) + '\n' + chk('rows left', 'len(df)', F['rows_clean']))
    b.read('Why is the walk-in count larger than the flag count?')
    b.change('In a new cell, run len(df.dropna()) and compare it with len(df). Why is it so much smaller? Delete the cell afterwards.')

    b.step(6, 'Outliers: check before you remove', 'Returns are lines with a negative qty. The IQR rule flags a value beyond 1.5 times the interquartile range from the quartiles. A flag is a question, so check each kind of flag and write down what you decide.')
    b.predict('Will any unit_price differ from the price list in products.csv? Will the IQR rule flag any revenue values?')
    todo(b, solution, 'merge on product_id, compare unit_price with unit_price_ugx. revenue = qty * unit_price * (1 - discount_pct / 100). quantile(0.25) and quantile(0.75)',
         'prod = pd.read_csv("products.csv")\nn_mismatch = None  # your code here: lines whose unit_price differs from the price list\nn_returns = None   # your code here: lines with a negative qty\n'
         'df["revenue"] = None  # your code here: qty * unit_price * (1 - discount_pct / 100)\nq1 = None  # your code here\nq3 = None  # your code here\nupper_fence = None  # your code here: q3 + 1.5 * (q3 - q1)\nn_flagged = None  # your code here: revenue values above the upper fence\nlower_fence = None  # your code here: q1 - 1.5 * (q3 - q1)\nn_flagged_low = None  # your code here: revenue values below the lower fence',
         'prod = pd.read_csv("products.csv")\nchk = df.merge(prod, on="product_id")\nn_mismatch = (chk["unit_price"] != chk["unit_price_ugx"]).sum()\nn_returns = (df["qty"] < 0).sum()\n'
         'df["revenue"] = df["qty"] * df["unit_price"] * (1 - df["discount_pct"] / 100)\nq1 = df["revenue"].quantile(0.25)\nq3 = df["revenue"].quantile(0.75)\nupper_fence = q3 + 1.5 * (q3 - q1)\nn_flagged = (df["revenue"] > upper_fence).sum()\nlower_fence = q1 - 1.5 * (q3 - q1)\nn_flagged_low = (df["revenue"] < lower_fence).sum()')
    b.code(guard('note("Check outliers, keep returns", len(df), len(df), str(n_returns) + " returns kept. IQR rule on revenue: " + str(n_flagged) + " high and " + str(n_flagged_low) + " low lines, all kept")\n'
                 'print(n_mismatch, n_returns, round(upper_fence), n_flagged, n_flagged_low)') + '\n'
           + chk('price mismatches', 'n_mismatch', F['n_mismatch']) + '\n' + chk('returns', 'n_returns', F['n_returns']) + '\n' + chk('upper fence', 'upper_fence', round(F['rev_hi'], 2), 0.5) + '\n'
           + chk('lines above the fence', 'n_flagged', F['n_rev_hi']) + '\n' + chk('lines below the lower fence', 'n_flagged_low', F['n_rev_lo']))
    b.read('Are the flagged lines errors? The low flags are mostly returns: why? What would you check before removing a flagged line?')

    b.step(7, 'Reconcile to the control total', f'The till system reports a control total of {n(F["control_total"])} UGX for the same lines. Your cleaned total is the sum of revenue. The reconciliation difference is the control total minus the cleaned total. Do not call it a residual: that word belongs to models.')
    b.predict('Do you expect the reconciliation difference to be zero? What could make it differ?')
    todo(b, solution, 'cleaned_total = round(df["revenue"].sum()); difference = control_total - cleaned_total',
         f'control_total = {F["control_total"]}\ncleaned_total = None  # your code here: the sum of revenue, rounded to a whole number\nreconciliation_difference = None  # your code here',
         f'control_total = {F["control_total"]}\ncleaned_total = round(df["revenue"].sum())\nreconciliation_difference = control_total - cleaned_total')
    b.code(guard('lost_unit_value = (lost["unit_price"] * (1 - lost["discount_pct"] / 100)).sum()\nunits_each = reconciliation_difference / lost_unit_value\nprint(cleaned_total, reconciliation_difference, round(units_each, 1))') + '\n'
           + chk('cleaned total', 'cleaned_total', F['net']) + '\n' + chk('reconciliation difference', 'reconciliation_difference', F['diff']) + '\n' + chk('units per dropped line', 'units_each', round(F['units_each'], 3), 0.01))
    b.read('The difference divided by the value of one unit of each dropped line is about 2. What does that suggest about the cause? Why is it an estimate and not proof?')
    b.md('**Your reconciliation note (Project milestone 1).** In one or two sentences, in your own words, say what the reconciliation difference is and what most likely causes it.\n\n> My note: ')

    b.step(8, 'Read the log and save the cleaned file', 'The log is the audit trail. It should have seven rows and the last row should end at the number of rows you keep. The next cell saves the cleaned data as orders_clean.csv and the log as cleaning_log.csv with to_csv.')
    todo(b, solution, 'pd.DataFrame(log) turns the list into a table. df.to_csv(name, index=False) saves the file',
         'log_table = None  # your code here: the log as a DataFrame, from pd.DataFrame(log)',
         'log_table = pd.DataFrame(log)')
    b.code(guard('df.to_csv("orders_clean.csv", index=False)\nlog_table.to_csv("cleaning_log.csv", index=False)\nprint(log_table.to_string())') + '\n'
           + chk('log rows', 'len(log_table)', len(F['log'])) + '\n' + chk('last log row ends at', 'log_table["rows_after"].iloc[-1]', F['rows_clean']))
    b.change('Add a one-line manager summary as a comment in the cell above: what changed, and what the reconciliation difference is.')
    b.md('---\n## Finish\n\nRun the cell below. It should say **All 26 checks pass**. Then download `orders_clean.csv` and `cleaning_log.csv`, save the notebook to your Drive, and keep the notebook with your log and your reconciliation note. Show them to your tutor for feedback. Nothing here is marked.')
    b.code('show_checks()')
    return b
