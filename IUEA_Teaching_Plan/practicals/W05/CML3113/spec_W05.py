"""W05 - pandas: load, filter, groupby, derived column.

Dataset: data/campus_energy.csv - 8 IUEA electricity meters, Jan-Mar 2026.
24 rows, 6 columns: meter_id, building, block, month, kwh, cost_ugx.

20 marks. q1-q3 are visible (10 marks, the student can self-check them).
q4-q6 are hidden (10 marks, graded from the submitted notebook). Their marks
and prompts are declared here because the task sheet states them anyway; their
check functions live in hidden/spec_W05_hidden.py, which is never handed out.
This file IS handed out, so assume every student reads it.

Week 5 falls on Friday 9 October 2026, which is Uganda Independence Day, so the
two Friday cohorts lose the session. This assignment is written to be workable
from the task sheet alone for that reason.

Feedback rule used throughout: name the value the student actually produced,
say why that value comes out of the mistake they made, then give the fix.
"""

ASSIGNMENT = "W05"
TITLE = "pandas: load, filter, group"
DEFAULT_COHORT = ""
QUESTION_ORDER = ["q1", "q2", "q3", "q4", "q5", "q6"]

CSV_NAME = "campus_energy.csv"
N_ROWS = 24
N_COLS = 6
COLS = ["meter_id", "building", "block", "month", "kwh", "cost_ugx"]


# --------------------------------------------------------------------------- #
# helpers. pandas is NOT imported: everything is duck typed so the spec still
# loads on a machine where pandas is missing, and so it does not care which
# pandas version the student has.
# --------------------------------------------------------------------------- #

def _get(ns, name):
    return ns.get(name, "__MISSING__")


def _absent(v):
    return isinstance(v, str) and v == "__MISSING__"


def _is_frame(v):
    return hasattr(v, "columns") and hasattr(v, "shape") and hasattr(v, "iloc")


def _is_series(v):
    return (hasattr(v, "index") and hasattr(v, "shape")
            and not hasattr(v, "columns") and hasattr(v, "tolist"))


def _typename(v):
    return type(v).__name__


def _num(v):
    try:
        return float(v)
    except Exception:                                  # noqa: BLE001
        return None


def _close(a, b, tol=1e-6):
    fa, fb = _num(a), _num(b)
    if fa is None or fb is None:
        return False
    return abs(fa - fb) <= tol * max(1.0, abs(fb))


# --------------------------------------------------------------------------- #
# q1 - load the file
# --------------------------------------------------------------------------- #

def check_q1(ns):
    df = _get(ns, "df")
    if _absent(df):
        return (False,
                "There is no variable called df yet. Run the cell that reads "
                "the file, and make sure the line starts with df = . If you "
                "wrote pd.read_csv(\"%s\") on its own, pandas read the file "
                "and then threw the result away." % CSV_NAME)
    if isinstance(df, str):
        return (False,
                "df is the text %r, so you stored the FILE NAME instead of the "
                "file's contents. Wrap it: df = pd.read_csv(%r)."
                % (df[:40], CSV_NAME))
    if not _is_frame(df):
        return (False,
                "df is a %s. pd.read_csv returns a DataFrame, so either the "
                "read_csv line did not run or something later overwrote df. "
                "Restart the runtime and run every cell from the top."
                % _typename(df))
    rows, cols = df.shape[0], df.shape[1]
    if cols == 1 and rows >= N_ROWS:
        return (False,
                "df has %d rows but only 1 column, which means pandas did not "
                "see the commas as separators. You are probably reading a "
                "different file, or you passed sep=';'. Use the plain call: "
                "pd.read_csv(%r)." % (rows, CSV_NAME))
    if rows == N_ROWS - 1:
        return (False,
                "df has %d rows, one short. The header row has been counted as "
                "data or skipped. Do not pass header=None or skiprows - "
                "%s has a proper header line." % (rows, CSV_NAME))
    if rows != N_ROWS:
        return (False,
                "df has %d rows; %s has %d. Check you opened that file and not "
                "a filtered or saved copy of it."
                % (rows, CSV_NAME, N_ROWS))
    got = [str(c) for c in list(df.columns)]
    missing = [c for c in COLS if c not in got]
    if missing:
        return (False,
                "df has %d rows, which is right, but the column %r is missing. "
                "The columns found were: %s. Check the file you loaded."
                % (rows, missing[0], ", ".join(got)))
    # Extra columns are fine and expected: q3 adds cost_per_kwh to this same
    # DataFrame, so q1 must still pass after the student has done q3.
    return (True, "")


# --------------------------------------------------------------------------- #
# q2 - count distinct meters
# --------------------------------------------------------------------------- #

def check_q2(ns):
    v = _get(ns, "n_meters")
    if _absent(v):
        return (False,
                "There is no variable called n_meters. The task asks for the "
                "count of DISTINCT meters, stored in a variable with exactly "
                "that name - lower case, underscore.")
    if _is_series(v) or _is_frame(v):
        return (False,
                "n_meters is a %s, not a single number. df[\"meter_id\"]"
                ".value_counts() gives you one row per meter; what you want is "
                "how MANY there are: df[\"meter_id\"].nunique()." % _typename(v))
    f = _num(v)
    if f is None:
        return (False,
                "n_meters is a %s and cannot be read as a number. It should be "
                "a whole number." % _typename(v))
    if f == N_ROWS:
        return (False,
                "n_meters is %d, which is the number of ROWS in the file. Each "
                "meter has one reading per month for three months, so counting "
                "rows counts every meter three times. Use "
                "df[\"meter_id\"].nunique()." % N_ROWS)
    if f == N_COLS:
        return (False,
                "n_meters is %d, which is the number of COLUMNS. len(df) and "
                "df.shape[1] are easy to mix up: df.shape is (rows, columns)."
                % N_COLS)
    if f != 8:
        return (False,
                "n_meters is %s. Print df[\"meter_id\"].unique() and count what "
                "comes back - the answer is the length of that list." % v)
    return (True, "")


# --------------------------------------------------------------------------- #
# q3 - derived column
# --------------------------------------------------------------------------- #

def check_q3(ns):
    df = _get(ns, "df")
    if not _is_frame(df):
        return (False,
                "This task builds on df, and df is not a DataFrame yet. Get q1 "
                "passing first.")
    cols = [str(c) for c in list(df.columns)]
    if "cost_per_kwh" not in cols:
        near = [c for c in cols if c.lower().replace(" ", "_") == "cost_per_kwh"]
        if near:
            return (False,
                    "df has a column called %r. The name has to match exactly, "
                    "letter for letter: cost_per_kwh, all lower case. Column "
                    "names in pandas are case sensitive." % near[0])
        added = [c for c in cols if c not in COLS]
        if added:
            return (False,
                    "df has no cost_per_kwh column. You did add %s, so the "
                    "assignment worked but the name is wrong. Use "
                    "df[\"cost_per_kwh\"] = df[\"cost_ugx\"] / df[\"kwh\"]."
                    % ", ".join(repr(c) for c in added))
        return (False,
                "df has no cost_per_kwh column. Add one with "
                "df[\"cost_per_kwh\"] = df[\"cost_ugx\"] / df[\"kwh\"]. Writing "
                "df.cost_per_kwh = ... does not create a column.")
    try:
        col = df["cost_per_kwh"]
        first = _num(col.iloc[0])
        total = _num(col.sum())
    except Exception as exc:                           # noqa: BLE001
        return (False, "cost_per_kwh exists but could not be read: %s"
                % str(exc)[:120])
    if first is None:
        return (False,
                "cost_per_kwh holds text, not numbers. If you built it with "
                "str() or with an f-string, drop that: divide the two numeric "
                "columns directly.")
    if _close(total, 24 * 0.0014545454, 1e-3) or (first and first < 0.01):
        return (False,
                "The first value of cost_per_kwh is %.6f, which is kWh divided "
                "by cost - the division is the wrong way round. Cost per kWh "
                "means cost_ugx / kwh, and should come out near 650-700 UGX."
                % first)
    if not _close(total, 16500.0, 1e-6):
        return (False,
                "cost_per_kwh sums to %s; it should sum to 16500. Every row "
                "should be that row's cost_ugx divided by that row's kwh. "
                "Check you did not divide by a single number such as "
                "df[\"kwh\"].sum() or df[\"kwh\"][0]." % _num(total))
    return (True, "")


# --------------------------------------------------------------------------- #
# the spec
# --------------------------------------------------------------------------- #

QUESTIONS = {
    "q1": {
        "marks": 3, "visible": True,
        "prompt": "Load %s into a DataFrame called df." % CSV_NAME,
        "check": check_q1,
        "answer_vars": ["df"],
    },
    "q2": {
        "marks": 3, "visible": True,
        "prompt": "Set n_meters to the number of distinct meters in the file.",
        "check": check_q2,
        "answer_vars": ["n_meters"],
    },
    "q3": {
        "marks": 4, "visible": True,
        "prompt": "Add a column cost_per_kwh to df, equal to cost_ugx / kwh.",
        "check": check_q3,
        "answer": lambda ns: _column_answer(ns, "cost_per_kwh"),
    },
    "q4": {
        "marks": 4, "visible": False,
        "prompt": "Set high_use to the rows of df where kwh is greater than "
                  "5000. Do this after q3 so the derived column comes along.",
        "answer_vars": ["high_use"],
    },
    "q5": {
        "marks": 3, "visible": False,
        "prompt": "Set mean_cost_per_kwh to the mean of the cost_per_kwh column.",
        "answer_vars": ["mean_cost_per_kwh"],
    },
    "q6": {
        "marks": 3, "visible": False,
        "prompt": "Set peak_building to the name of the building with the "
                  "highest total kwh.",
        "answer_vars": ["peak_building"],
    },
}


def _column_answer(ns, col):
    df = ns.get("df")
    try:
        return df[col]
    except Exception:                                  # noqa: BLE001
        return None
