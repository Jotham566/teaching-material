"""W05 hidden tests - LECTURER ONLY. Do not put this file in a handout.

Loaded by batch_grade.py through load_spec(..., include_hidden=True), which
looks for specs/hidden/spec_W05_hidden.py. The student's copy of
specs/spec_W05.py declares q4 to q6 with their marks and prompts but with no
check functions, so nothing here reaches a student machine.

Marks and prompts come from the handout spec; this file supplies only the
checks. The small helpers are repeated rather than imported, so that this file
loads on its own with nothing on sys.path.
"""

CSV_NAME = "campus_energy.csv"
N_ROWS = 24
N_COLS = 6
COLS = ["meter_id", "building", "block", "month", "kwh", "cost_ugx"]


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
# q4 - filter (HIDDEN)
# --------------------------------------------------------------------------- #

def check_q4(ns):
    v = _get(ns, "high_use")
    if _absent(v):
        return (False, "high_use was never created.")
    if not _is_frame(v):
        if _is_series(v):
            return (False,
                    "high_use is a Series of True/False, which is the MASK "
                    "rather than the rows. Pass the mask back into df: "
                    "high_use = df[df[\"kwh\"] > 5000].")
        return (False, "high_use is a %s; the task asks for the matching rows "
                       "of df, which is a DataFrame." % _typename(v))
    rows = v.shape[0]
    if rows == 15:
        return (False,
                "high_use has 15 rows, so a meter reading of exactly 5000 has "
                "been let in - the task says greater than 5000, which is > "
                "and not >=. (There is no row at exactly 5000 in this file, so "
                "check the threshold you typed.)")
    if rows != 14:
        return (False,
                "high_use has %d rows; the correct filter gives 14. Print "
                "df[\"kwh\"].describe() and check the threshold and the column."
                % rows)
    cols = [str(c) for c in list(v.columns)]
    if "cost_per_kwh" not in cols:
        return (True,
                "The 14 rows are right, but high_use has no cost_per_kwh "
                "column, so you filtered before adding it in q3. Order "
                "matters: add the column first, then filter.", 0.75)
    return (True, "")


# --------------------------------------------------------------------------- #
# q5 - mean of the derived column (HIDDEN)
# --------------------------------------------------------------------------- #

def check_q5(ns):
    v = _get(ns, "mean_cost_per_kwh")
    if _absent(v):
        return (False, "mean_cost_per_kwh was never created.")
    f = _num(v)
    if f is None:
        return (False, "mean_cost_per_kwh is a %s, not a number." % _typename(v))
    if _close(f, 687.5):
        return (True, "")
    if _close(f, 16500.0):
        return (False,
                "That is the SUM of cost_per_kwh, not the mean. .sum() and "
                ".mean() got swapped.")
    if _close(f, 693.53, 1e-3):
        return (False,
                "%s is total cost divided by total kWh across the whole file. "
                "That is a defensible figure, but the task asks for the mean "
                "of the per-row column: df[\"cost_per_kwh\"].mean()." % _num(f))
    return (False,
            "mean_cost_per_kwh is %s; it should be 687.5. Take the mean of the "
            "cost_per_kwh column you built in q3, over all 24 rows."
            % _num(f))


# --------------------------------------------------------------------------- #
# q6 - groupby (HIDDEN)
# --------------------------------------------------------------------------- #

def check_q6(ns):
    v = _get(ns, "peak_building")
    if _absent(v):
        return (False, "peak_building was never created.")
    if _is_series(v) or _is_frame(v):
        return (False,
                "peak_building is a %s. You have the grouped totals but not "
                "the answer: .idxmax() gives the label of the largest row, "
                "while .max() gives the number." % _typename(v))
    if not isinstance(v, str):
        f = _num(v)
        if f is not None and _close(f, 29530):
            return (False,
                    "peak_building is 29530, the kWh TOTAL for the top "
                    "building. The task asks for the name. Use .idxmax() "
                    "instead of .max().")
        return (False,
                "peak_building is a %s; the task asks for the building's name "
                "as a string." % _typename(v))
    got = v.strip()
    if got == "Hostel Block C":
        return (True, "")
    if got == "Residence":
        return (False,
                "\"Residence\" is a BLOCK, not a building. Group by "
                "\"building\", not \"block\".")
    if got == "Workshop A":
        return (False,
                "\"Workshop A\" is the highest single monthly reading, not the "
                "highest three-month total. Sum within each building first: "
                "df.groupby(\"building\")[\"kwh\"].sum().idxmax().")
    if got == "M-004":
        return (False,
                "\"M-004\" is the meter id. That meter is on the right "
                "building, but the task asks for the building name, so group "
                "by \"building\".")
    if got in ("Hostel Block D", "Server Room", "Kabojja Lab", "Library",
               "Admin Tower", "Lecture Hall 2"):
        return (False,
                "%r is not the highest total. Print "
                "df.groupby(\"building\")[\"kwh\"].sum().sort_values() and read "
                "off the last row. Check you used .sum() and not .mean() - "
                "every building here has the same number of readings, so mean "
                "and sum rank the same, which means the error is elsewhere."
                % got)
    return (False,
            "peak_building is %r, which is not one of the building names in "
            "the file. Print df[\"building\"].unique() to see them." % got[:40])


QUESTIONS = {
    "q4": {"check": check_q4},
    "q5": {"check": check_q5},
    "q6": {"check": check_q6},
}
