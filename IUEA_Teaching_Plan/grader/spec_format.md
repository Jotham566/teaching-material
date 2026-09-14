# The spec format

One Python file per assignment: `specs/spec_<ASSIGNMENT>.py`. The assignment id
is whatever you pass to `Grader("W05")`, upper case, no spaces.

A spec is a plain Python module. It is imported, never executed as a script, and
it is the only file you write each week. `iuea_grader.py` and `batch_grade.py`
stay untouched all semester.

## The minimum

```python
ASSIGNMENT = "W05"
TITLE = "pandas: load, filter, group"

def check_q1(ns):
    df = ns.get("df", "__MISSING__")
    if not hasattr(df, "columns"):
        return (False, "df is not a DataFrame yet. Run the read_csv cell.")
    return (True, "")

QUESTIONS = {
    "q1": {"marks": 3, "visible": True,
           "prompt": "Load campus_energy.csv into a DataFrame called df.",
           "check": check_q1,
           "answer_vars": ["df"]},
}
```

## Module-level names

| name | required | meaning |
|---|---|---|
| `QUESTIONS` | yes | dict of question id to question dict |
| `QUESTION_ORDER` | no | list of ids, fixing the order shown to the student. Without it, dictionary order is used, which is insertion order in Python 3.7+ |
| `ASSIGNMENT` | no | documentation only; the id comes from the file name |
| `TITLE` | no | printed in the banner and on the feedback sheet |
| `DEFAULT_COHORT` | no | which variant to use when the notebook has no `COHORT` |

## The question dict

| key | default | meaning |
|---|---|---|
| `marks` | `1` | marks for this question |
| `visible` | `True` | `True` means the student can run `g.check(...)` on it. `False` means only `batch_grade.py` ever runs it |
| `prompt` | the id | one sentence, shown in the banner, in `g.tasks()` and on any failure |
| `check` | required | callable, `check(ns)` |
| `answer_vars` | `[]` | variable names whose values go into the answer fingerprint |
| `answer` | none | callable `answer(ns)` returning the value to fingerprint; overrides `answer_vars` |
| `variants` | none | per-cohort overrides, see below |

### `check(ns)`

`ns` is the student's namespace as a dict. Read from it with `ns.get(name)` and
never write to it.

Return one of:

- `True` or `False`
- `(ok, message)`
- `(ok, message, fraction)` where `fraction` is between 0 and 1 and scales the
  marks. `(True, "note", 0.75)` awards three quarters and still reads as a pass.

A check that raises is caught, scored zero, and labelled `CHECK_RAISED` in the
results CSV so you can find your own bug. It never crashes the run and the
student never sees a traceback.

### Feedback that teaches

The rule used in `spec_W05.py` and `spec_W03.py`: **name the value the student
actually produced, say why that value comes out of the mistake they made, then
give the fix.** Check for the specific wrong answers before you fall through to
a generic message.

```python
if f == N_ROWS:
    return (False,
            "n_meters is %d, which is the number of ROWS in the file. Each "
            "meter has one reading per month for three months, so counting "
            "rows counts every meter three times. Use "
            "df[\"meter_id\"].nunique()." % N_ROWS)
```

"Incorrect" is not feedback. Every wrong-answer branch you add is one fewer
student in the corridor on Wednesday.

### Do not import pandas in a spec

Use duck typing: `hasattr(v, "columns")` for a DataFrame, `hasattr(v, "index")`
without `columns` for a Series, `hasattr(v, "tolist")` with a `shape` for a
numpy array. Two reasons. The spec must import on an offline lab machine that
may not have pandas, and a spec that imports pandas at module level will not
load at all if the student's environment is broken, which is exactly when they
need feedback.

### Visible or hidden: two files

The student has to have the spec on their own machine, because `g.check()`
imports it. Anything in that file can be read by them. So each assignment is
two files:

```
specs/spec_W05.py                  handed out with the notebook
specs/hidden/spec_W05_hidden.py    yours, never handed out
```

The handout declares every question, including the hidden ones, with their
marks and prompts but **no `check` key**. The prompts are on the task sheet
anyway, and the banner needs the marks so it can tell the student that ten
further marks are graded later.

The hidden file supplies only the checks:

```python
QUESTIONS = {
    "q4": {"check": check_q4},
    "q5": {"check": check_q5},
    "q6": {"check": check_q6},
}
```

`batch_grade.py` calls `load_spec(..., include_hidden=True)`, which finds
`spec_<A>_hidden.py` in a `hidden/` subfolder and merges its keys over the
handout's. Anything merged in this way is forced to `visible = False`. The
`Grader` a student runs never merges, so a hidden question has no check
function in their copy and `g.check("q4")` prints a sentence saying it is
graded later.

Repeat the few small helpers in the hidden file rather than importing them.
Specs are loaded by path with nothing added to `sys.path`, so an import of a
sibling module will not resolve. Twenty duplicated lines is the cheaper
problem.

If `batch_grade.py` cannot find the hidden file it prints a warning naming the
questions that have no check, and everyone scores zero on them. Read the first
four lines of its output every week.

Visible tests are the teaching. Hidden tests are the marking. Split the marks
roughly in half. Put the tasks with an obvious right answer in the visible half
and the ones with a common near-miss in the hidden half, so a student cannot
brute-force the mark by trying values until the checker goes green.

### Per-cohort variants

```python
QUESTIONS = {
    "q3": {
        "marks": 3, "visible": True,
        "prompt": "Cohort formula - see your task sheet.",
        "check": check_q3_cml3111,        # used if no variant matches
        "variants": {
            "CML3111": {"prompt": "Write power_loss(current, resistance)...",
                        "check": check_q3_cml3111},
            "CML3112": {"prompt": "Write slab_mass(area_m2, thickness_m)...",
                        "check": check_q3_cml3112},
            "CML3113": {"prompt": "Write mud_pressure(depth_m, density)...",
                        "check": check_q3_cml3113},
            "default": {"prompt": "...", "check": check_q3_cml3111},
        },
    },
}
```

The matching variant's keys replace the base question's keys. Marks should be
the same across variants; nothing enforces that, so check it yourself.

The cohort is resolved in this order:

1. `Grader("W03", cohort="CML3112")`
2. a `COHORT`, `cohort` or `COURSE_CODE` string variable in the notebook
3. `DEFAULT_COHORT` in the spec
4. the `"default"` variant, then the base question

When `batch_grade.py` runs, the `COHORT` variable found inside the submitted
notebook wins over `--cohort`, because that is what the student was actually
set. Put `COHORT = "CML3112"` in the setup cell of the notebook you hand out.

### The answer fingerprint

`answer_vars` and `answer` feed a hash that goes into the submission token.
`batch_grade.py` recomputes it from the notebook and compares. A mismatch means
the notebook does not produce the answers the token claims.

Only **visible** questions are fingerprinted. The student's Grader has loaded
the handout spec and cannot see the hidden questions, so a fingerprint over all
of them would never match. Putting `answer_vars` on a hidden question is
harmless and does nothing.

Keep the fingerprint on **values**, not on objects that carry state. Numbers are
rounded to six significant figures and a DataFrame reduces to its shape, its
column names and a per-column digest, so a different pandas version does not
change the hash. Anything unhashable falls back to its type name.

Do not fingerprint something that changes between runs. A timestamp, a
`random` draw without a seed, a dict iteration order from a set, or a model's
fitted weights will all produce a false mismatch for an honest student. When in
doubt, leave `answer_vars` off that question.

## Checklist before you hand a spec out

```
python3 iuea_grader.py --selftest              # the module still works
node gradebook.gs --test                       # the gradebook still works
python3 -c "import sys; sys.path.insert(0,'.'); import iuea_grader as g; \
    s=g.load_spec('W05','specs/spec_W05.py'); print(len(s.QUESTIONS))"
python3 simulate_cohort.py --n 20 --out /tmp/t # fake submissions
python3 batch_grade.py -a W05 -n /tmp/t/notebooks \
    -t /tmp/t/form_responses.csv --data-dir data -o /tmp/t/res
```

Then read three of the feedback files in `/tmp/t/res/feedback/` as if you were
a student. If a message does not tell you what to change, rewrite it.

Two things the simulator has already caught once each, so check for them:

- a task that passes on its own but fails after a later task modifies the same
  object (`q1` checked the column *count* of `df`, which `q3` then changed)
- a notebook whose setup cell cannot find its files inside the grading sandbox,
  which makes every later cell fail on a name that was never defined
