"""W03 hidden tests - LECTURER ONLY. Do not put this file in a handout.

Loaded by batch_grade.py through load_spec(..., include_hidden=True). The
handout spec_W03.py declares q4 and q5 with marks and prompts but no checks.

READINGS is repeated here because the check needs the same list the notebook
gives the student. Change it in one place and change it in the other.
"""

G = 9.81


def _get(ns, name):
    return ns.get(name, "__MISSING__")


def _absent(v):
    return isinstance(v, str) and v == "__MISSING__"


def _num(v):
    if isinstance(v, bool):
        return None
    try:
        return float(v)
    except Exception:                                  # noqa: BLE001
        return None


def _close(a, b, tol=1e-4):
    fa, fb = _num(a), _num(b)
    if fa is None or fb is None:
        return False
    return abs(fa - fb) <= tol * max(1.0, abs(fb))


def _callable_or_reason(ns, name):
    """Return (fn, None) or (None, message) - the standard 'is it a function' check."""
    v = _get(ns, name)
    if _absent(v):
        return None, ("There is no %s in your notebook. The task asks for a "
                      "FUNCTION with exactly that name, defined with "
                      "def %s(...):" % (name, name))
    if callable(v):
        return v, None
    n = _num(v)
    if n is not None:
        return None, ("%s is the number %s, so you calculated one answer "
                      "instead of writing a function. A function takes its "
                      "inputs as arguments and returns the result, so it can "
                      "be re-used on any values: def %s(...): ... return ..."
                      % (name, _num(v), name))
    return None, ("%s is a %s, not a function. Define it with def %s(...):"
                  % (name, type(v).__name__, name))


def _try_call(fn, args):
    """Call a student function. Returns (value, None) or (None, message)."""
    try:
        return fn(*args), None
    except TypeError as exc:
        return None, ("Calling it as %s(%s) raised TypeError: %s. Check how "
                      "many arguments your def line takes, and in which order."
                      % (getattr(fn, "__name__", "f"),
                         ", ".join(repr(a) for a in args), str(exc)[:120]))
    except ZeroDivisionError:
        return None, ("Calling it with %s divided by zero. Guard the case "
                      "before you divide." % (", ".join(repr(a) for a in args),))
    except Exception as exc:                           # noqa: BLE001
        return None, ("Calling it as %s(%s) raised %s: %s"
                      % (getattr(fn, "__name__", "f"),
                         ", ".join(repr(a) for a in args),
                         type(exc).__name__, str(exc)[:120]))


def _no_return(name):
    return ("%s runs but hands back None, so it has no return statement - or "
            "the return is indented inside an if that did not happen. print() "
            "shows a value on screen; return gives it back to the caller, and "
            "the grader can only see what is returned." % name)


# --------------------------------------------------------------------------- #
# q4 - a guarded function (HIDDEN)
# --------------------------------------------------------------------------- #

def check_q4(ns):
    fn, why = _callable_or_reason(ns, "efficiency")
    if fn is None:
        return (False, why)
    for args, want in [((750.0, 1000.0), 75.0), ((45.0, 60.0), 75.0),
                       ((1.0, 8.0), 12.5)]:
        got, why = _try_call(fn, args)
        if why:
            return (False, why)
        if got is None:
            return (False, _no_return("efficiency"))
        f = _num(got)
        if f is None:
            return (False, "efficiency%r returned a %s, not a number."
                    % (args, type(got).__name__))
        if _close(f, want / 100.0):
            return (False,
                    "efficiency%r returned %.6g, the fraction. The task asks "
                    "for a percentage, so multiply by 100." % (args, f))
        if _close(f, 100.0 * args[1] / args[0]):
            return (False,
                    "efficiency%r returned %.6g, which is input over output. "
                    "Efficiency cannot exceed 100 percent, so that is the "
                    "clue: output goes on top." % (args, f))
        if not _close(f, want):
            return (False,
                    "efficiency%r returned %.6g; it should be %.6g. "
                    "Efficiency = 100 * output / input." % (args, f, want))
    # the guard
    for args in [(500.0, 0.0), (500.0, -10.0)]:
        try:
            got = fn(*args)
        except ZeroDivisionError:
            return (False,
                    "efficiency%r raised ZeroDivisionError. The task says to "
                    "return None when the input power is zero or negative, so "
                    "test for that before you divide:  if in_w <= 0: return "
                    "None" % (args,), 0.6)
        except Exception as exc:                       # noqa: BLE001
            return (False,
                    "efficiency%r raised %s. It should quietly return None for "
                    "an input power of zero or less."
                    % (args, type(exc).__name__), 0.6)
        if got is not None:
            return (False,
                    "efficiency%r returned %r. An input power of zero or less "
                    "is not physical, and the task says to return None in "
                    "that case rather than a number." % (args, got), 0.6)
    return (True, "")


# --------------------------------------------------------------------------- #
# q5 - use your own function over a list (HIDDEN)
# --------------------------------------------------------------------------- #

READINGS = [98.5, 103.2, 99.0, 111.4, 94.8, 100.6]
NOMINAL = 100.0
# percent errors: -1.5, +3.2, -1.0, +11.4, -5.2, +0.6
# largest by absolute size is 111.4, at +11.4 percent
WORST_READING = 111.4
WORST_ERROR = 11.4


def check_q5(ns):
    reading = _get(ns, "worst_reading")
    err = _get(ns, "worst_error")
    if _absent(reading) and _absent(err):
        return (False,
                "Neither worst_reading nor worst_error was created. The task "
                "asks for both.")
    parts_ok = 0
    problems = []

    f = _num(reading)
    if _absent(reading):
        problems.append("worst_reading is missing.")
    elif f is None:
        problems.append("worst_reading is a %s, not a number."
                        % type(reading).__name__)
    elif _close(f, WORST_READING):
        parts_ok += 1
    elif _close(f, 94.8):
        problems.append(
            "worst_reading is 94.8, the lowest reading. The largest error by "
            "SIZE is 111.4, at +11.4 percent against 94.8's -5.2 percent. "
            "Compare abs(percent_error(r, 100)), not the reading itself.")
    elif _close(f, 3):
        problems.append(
            "worst_reading is 3, which is the POSITION in the list. Use the "
            "position to look the reading back up: READINGS[3].")
    elif _close(f, WORST_ERROR):
        problems.append(
            "worst_reading is 11.4, which is the error. worst_reading should "
            "be the reading itself, 111.4, and worst_error the 11.4.")
    else:
        problems.append(
            "worst_reading is %.6g; it should be %.6g. Loop over READINGS, "
            "call your own percent_error against 100, and keep the reading "
            "whose absolute error is biggest." % (f, WORST_READING))

    g = _num(err)
    if _absent(err):
        problems.append("worst_error is missing.")
    elif g is None:
        problems.append("worst_error is a %s, not a number."
                        % type(err).__name__)
    elif _close(g, WORST_ERROR):
        parts_ok += 1
    elif _close(g, -5.2):
        problems.append(
            "worst_error is -5.2. That is the most negative error, not the "
            "largest one. Take abs() when you compare, and store the signed "
            "value.")
    elif _close(g, abs(WORST_ERROR) / 100.0):
        problems.append(
            "worst_error is 0.114, the fraction. Give it as a percentage.")
    else:
        problems.append(
            "worst_error is %.6g; it should be %.6g, the signed percent error "
            "of the worst reading." % (g, WORST_ERROR))

    if parts_ok == 2:
        return (True, "")
    return (False, " ".join(problems), 0.5 * parts_ok)


QUESTIONS = {
    "q4": {"check": check_q4},
    "q5": {"check": check_q5},
}
