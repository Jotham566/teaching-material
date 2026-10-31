"""Shared constants, paths and the lesson schema for the Holiday Data and AI Camp (revision 2, 31 Oct 2026).

THE SCHEMA (every lesson in lessons/da.py DA and lessons/ml.py ML is a dict)
--------------------------------------------------------------------------------
title        str   Session title. No "X by Y" style titles.
objective    str   "By the end: ..." sentence, observable (what the student can do).
question     str   ONE question about the data or the model, answered in the last 20 minutes.
words        list  1 to 6 tuples (term, plain definition, everyday comparison). A term
                   is defined once per track, ever (the glossary builder raises on repeats).
blocks       list  0 to 2 dicts, one per 50-minute block. Each block:
                     idea         str  short name of the one idea (e.g. "Group and total")
                     intro        str  1 to 3 plain sentences. Terms from `words` appear in
                                       an example before they are defined: put the definition
                                       sentence AFTER the code in `shows`/`intro`, not before.
                     predict      str  the written guess students make BEFORE running
                     code         str|None  runnable Python (or None for a talk-only block)
                     shows        str  what the output should show, in words with the numbers
                     investigate  list of (question, answer), 2 or 3 items
                     modify       dict(instruction=str, answer=str, code=str optional,
                                       check=str optional)
                     check        str  Python expression evaluated after `code` in the session
                                       namespace. REQUIRED when code is present and mode is
                                       'python' unless nocheck=True is set on the block.
make         dict  task=str, reference=str (code when reference_is_code), reference_is_code=bool,
                   check=str optional (evaluated after reference code), evidence=str
errors       list  EXACTLY 2 tuples (what you see, what it means in plain words, the fix)
exit_ticket  str   one sentence the student must be able to say or write
mode         str   'python' (blocks are executed by the verifier) or 'guide' (checkpoint,
                   project or presentation; code is not executed)
libs         list  libraries newly used this session, e.g. ['pandas']
data         list  data files in the student folder the session reads
misconceptions list of str  what students commonly believe wrongly in this session
questions    list of (question, expected answer) for the instructor
pacing       str|None  overrides DEFAULT_CLOCK when the session needs a different 180 minutes
time_note    str|None  one sentence on where the session is most likely to overrun

SESSION CLOCK
-------------
DEFAULT_CLOCK sums to 180. A lesson with a pacing override must also sum to 180; the
verifier parses the minutes.

STYLE (enforced by verify_camp.py)
------------------------------------------
Plain declaratives. No "not X but Y" or "X, not Y" contrasts used as emphasis, no
"genuinely", "honestly", "straightforward". No SQL, DB Browser or sqlite in teen material.
Allowed libraries: pandas, numpy, matplotlib, seaborn, sklearn (plus math).
"""
from pathlib import Path

BUILD = Path(__file__).resolve().parent
ROOT = BUILD.parent                       # camp_2026
REPO = ROOT.parents[1]
CURRICULUM = ROOT / 'curriculum'          # generated: curricula, plans, glossaries, labs
HANDBOOK = ROOT / 'handbook'              # written by hand: policies, rubric, start guide
PROGRAMME = ROOT / 'programme'            # organiser material: decisions, setup, preflight
PACKS = ROOT / 'student_packs'            # the two student ZIPs
DATA = ROOT / 'data'
SUNRISE_DIR = DATA / 'sunrise'

DEFAULT_CLOCK = [
    ('Recall: retrieve yesterday, three questions on paper', 10),
    ('Block A: predict, run, investigate, modify', 50),
    ('Break away from screens', 15),
    ('Block B: predict, run, investigate, modify', 50),
    ('Make: the independent task and the project journal', 40),
    ('Exit ticket, save, and an individual check with each learner', 15),
]
assert sum(m for _, m in DEFAULT_CLOCK) == 180

ALLOWED_IMPORTS = {'pandas', 'numpy', 'matplotlib', 'seaborn', 'sklearn', 'math'}
BANNED_TERMS = ['SQL', 'sqlite', 'DB Browser', 'statistics.mean', 'import statistics']

# Student-folder names of the Sunrise Shops files (the generator writes shorter names).
SUNRISE_FILES = {
    'sales.csv': 'sunrise_sales.csv',
    'products.csv': 'sunrise_products.csv',
    'branches.csv': 'sunrise_branches.csv',
    'daily_summary.csv': 'sunrise_daily_summary.csv',
    'products_practice.csv': 'sunrise_products_practice.csv',
    'sales_raw.csv': 'sunrise_sales_raw.csv',
}
DATA_DA = ['camp_shop.csv'] + list(SUNRISE_FILES.values())
DATA_ML = ['camp_shop.csv', 'synthetic_homes.csv', 'synthetic_fares.csv']

ROADMAP = {
    'Machine Learning': [
        ('1–2', 'Python foundations', 'Values, decisions, lists, functions, and NumPy vectors. A first prediction in session 1.'),
        ('3–4', 'Understand your data', 'pandas tables, cleaning, matplotlib and seaborn charts, mean, median, proportions and weighted sums.'),
        ('5–6', 'Build and test predictions', 'Baselines, regression, decision trees, held-out tests and error measures with scikit-learn.'),
        ('7–8', 'Build your own project', 'Plan, compare, test, explain and demonstrate an individual prediction project.')],
    'Data Analysis': [
        ('1–2', 'Start coding in Python', 'Use Jupyter; values, decisions, lists, loops and functions with checks.'),
        ('3–4', 'Find answers with pandas', 'Read, filter, group, clean and chart real-looking shop data; checkpoint one.'),
        ('5–6', 'Explore and merge', 'NumPy, seaborn exploration, cleaning a messy export, merging two tables; checkpoint two.'),
        ('7–8', 'Build your own project', 'A Python analysis notebook, charts, findings and a five-minute explanation.')],
}
TRACK_NAMES = {'ML': 'Machine Learning', 'DA': 'Python for Data Analysis'}
