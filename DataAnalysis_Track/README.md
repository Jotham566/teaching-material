# Data Analysis with Python, SQL and Power BI

**Five weeks, fifteen sessions of three hours, forty-five hours**, for people
already in work who are **confident in a spreadsheet and have never written
code**.

Excel is the anchor, not a topic. Every new idea arrives beside the
spreadsheet thing it replaces: GROUP BY is your pivot table written down, a
join is a VLOOKUP that returns every match, a measure is a pivot table value
field. **Sessions 1 and 2 contain no code at all** — the vocabulary of data,
grain and keys, with the six tables mapped by clicking. That looks slow and
it is the reason the rest is not.

Hours: Foundations 6, SQL 9, Python 12, Statistics 6, Charts 3,
Investigation 3, Power BI 6. Statistics, charts and the investigation are all
taught in Python, so the Python total is 24 of the 45.

## What is here

| File | What it is |
|---|---|
| `decks/DA_S01…S15.pptx` | The fifteen session decks, 357 slides. Each runs the same shape: title, where tonight sits, outcomes, the question, block one, break, block two, the trap on its own slide, check and answers, the lab brief, and the closing line. Speaker notes are participant-safe, because the decks are handed out after each session. |
| `DataAnalysis_Glossary.docx` | The handout. 92 terms in plain language with the spreadsheet equivalent, generated from the sessions themselves. Printed once in session 1 and kept. 49 of the terms have no spreadsheet equivalent, and those are the new ideas. |
| `figs/` | 12 explainer figures: table anatomy, grain, joins, distribution shapes, the real skew, percentiles, the four charts, chart anatomy, axis honesty, rate against count, the star schema, seasonality. Built from real data and asserted against the answer key. |
| `DataAnalysis_Lecturer_Guide.docx` | Stage directions, generated FROM the decks. Timing per session and, slide by slide, what the instructor does. Lecturer only: this is the half of each note that is deliberately not in the decks. |
| `DataAnalysis_Track_Plan.docx` | The instructor plan: the fifteen sessions in full with their vocabulary, the projects and feedback, the glossary summary, datasets with licences, what was cut and why, what to do before session 1, and where this departs from the roadmap.sh path. |
| `DataAnalysis_Track_Workbook.xlsx` | Session grid, the three-hour block, the projects, a participant progress and projects tracker (no marks or weights, two working formulas per row), the dataset register and the answer key. |
| `labs/lab_sql.md` | Sessions 3, 4 and 5. Eight questions with their queries and answers, then the rep revenue report as named steps. No window functions: those were cut, and the ranking is done in the spreadsheet. |
| `labs/lab_python.md` | Sessions 7, 8 and 9. Profile, clean eight seeded defects, keep a log, reconcile against SQL. |
| `labs/lab_powerbi.md` | Sessions 14 and 15. Model, three measures, one dashboard, with the browser path for Mac participants. |
| `data/build_teaching_data.py` | Generates the course dataset. Standard library only. |
| `data/riverside.db` | The clean SQLite database the SQL sessions use. |
| `data/*_raw.csv` | The same business exported badly. This is what week two cleans. |
| `data/*.csv` | Clean CSVs for the Power BI sessions and the browser path. |
| `data/answer_key.json` | Every lab answer, computed from the data at generation time. |

## Rebuild order

```bash
python3 data/build_teaching_data.py          # dataset, CSVs, answer key
python3 ../scripts/build_da_labs.py          # labs, numbers from the key
python3 ../scripts/build_da_plan_docx.py
python3 ../scripts/build_da_xlsx.py
python3 ../scripts/build_da_glossary_docx.py
python3 ../scripts/make_da_figures.py        # the 12 explainer figures
python3 ../scripts/build_da_teaching_guide.py   # the guide; it ALSO rewrites the fifteen decks, see below
python3 ../scripts/verify_da_track.py        # 44 checks; must be green
python3 ../scripts/verify_da_decks.py        # 26 checks; must be green
python3 ../scripts/verify_da_workbook.py
python3 ../scripts/validation/overflow_scan.py
```

`scripts/da_content.py` is the single source of truth for the curriculum:
session titles, outcomes, the traps, the five projects and datasets. Slide content
lives in `scripts/da_deck_w1.py` through `da_deck_w5.py`. Change a session in
either place and the documents, the workbook, the decks and the guide all
follow.

Numbers come from `data/answer_key.json` through `scripts/da_keys.py`, so no
figure in any handout or on any slide is typed by hand. `verify_da_decks.py`
enforces that: it executes every SQL block and every pandas block that
appears on a slide against the real data, and traces every UGX figure on
every slide back to a value in the answer key.

Slide placeholders are written `<<name>>` rather than `{name}` because the
slides carry Python dicts, DAX measures and f-strings, all of which contain
braces.

## The course dataset

Riverside Distributors: a wholesale distributor with 401 customers, 120
products, 12 reps, 6,000 orders and 20,234 order lines across 2024 and 2025,
plus returns and a daily FX series.

It is generated rather than downloaded because the datasets with the right
shape fail on licence. Tableau's Superstore is internal-use-only under the
Tableau EULA; Olist is CC BY-NC-SA, and NonCommercial is a problem the moment
the course is paid for. Generating it also means the defects are deliberate
and the answers are known exactly.

The database is clean, so the SQL sessions are about SQL. The `_raw.csv`
files carry eight seeded defects, so session 8 is about cleaning:
duplicate rows, returns as negative quantities, one category priced in
dollars, discounts typed as percentages, two date formats in one column,
messy customer names, missing customer ids on walk-in trade, and one customer
under two ids.

**The reconciliation does not come out exact, on purpose.** Revenue on
delivered orders is UGX 8,751,705,520 in the database. A correct clean of the
raw CSVs lands on UGX 8,751,672,145, which is UGX 33,374.58 lower, because
the dollar-priced lines were recorded to the cent and 3,780 shillings a
dollar cannot be undone exactly. Naming that residual is part of the lab.

## The other datasets

All CC BY 4.0 or ODbL, none needing an account, so the track is safe for
commercial delivery:

- **Online Retail II** (UCI 502) — the first real file, and the first too big for Excel, in session 7
- **Bank Marketing** (UCI 222) — banking, finance and telecom investigation
- **AI4I 2020 Predictive Maintenance** (UCI 601) — energy and manufacturing
- **World Bank indicators API** — public sector, and the API lesson
- **Uganda Healthsites** (HDX, ODbL) — the local dataset, and the Power BI map

Section 4 of the plan lists what was rejected and why, so the same options do
not get proposed again.

## Before you teach it

Section 5 of the plan is the checklist. The three that matter most: run both
verifiers and do not teach from the pack unless they are green; work the SQL
lab yourself from cold, because question 3 is where your room will stick; and
build the Power BI model yourself on the machine you will teach from, because
session 14 is the one most likely to lose the room.

Also ask, in writing, how many participants are on a Mac. It changes week
five: Power BI Desktop requires Windows. The browser teaching route depends on the account and workspace capabilities verified during setup; retain the supplied clean CSV fallback for participants without transformation permissions.


## Decks: do not rebuild over the speaker notes

`build_da_decks.py` writes the slides and a short set of notes. The decks on disk
carry later layers of speaker notes (lecturer cues, checks with expected answers,
recovery notes) that it does not regenerate, and `build_da_teaching_guide.py`
runs the deck builder as a side effect. Running either overwrites those notes.
So the live decks were changed on 4 November 2026 by
`scripts/patch_da_no_assessment_20261104.py` (it changes slide and note text in
place, is safe to run twice, and also patches `decks/lecturer_notes/*.md`),
and the same wording changes were made in the sources. If you rebuild the decks
from source, run `patch_da_no_assessment_20261104.py` afterwards only if the
notes you want are the layered ones, and restore them from your backup first.

`decks/MANIFEST.txt` lists the fifteen current decks, and `verify_da_decks.py`
FAILS while anything else is in the folder.

## No exam, no marks

Lecturer decision, 4 November 2026: none of the KLAi professional programs has an
exam or any assessment. There are no marks, grades, pass marks, weights, mark
sheets, graded labs or capstones, and no quizzes that count. Learners build five
projects and keep them: the SQL revenue report (session 5), the cleaned dataset
with its cleaning log (9), the statistics notes page (11), the investigation
write-up (13) and the Power BI dashboard (15). The investigation and the dashboard
are the final project, shown in session 15 with peer feedback. Practice feedback
stays: checks inside the labs, the check-and-answers slide in each deck, and
recall questions that are self-checks and never marked. The certificate is a
certificate of completion from KLAi Professional Learning for completing the
course and its project.

The retired material (assessment banks, student guides, the S09 package, the
roster, the mark-sheet workbook, the old plan, the two bank generators) is in
`archive/assessment_retired_2026-11-04/`, with a README. The workbook now has a
Projects sheet and a Progress tracker sheet in place of the mark sheet.
`../IUEA_Teaching_Plan/grader/` still holds Data Analysis grader code shared with
the university course. It is not used by this course.

The [sector snapshots](data/sector_snapshots/README.md) (Bank Marketing, synthetic
AI4I and a fixed Uganda GDP series) are the data for the session 13 investigation.
Verify their hashes with `python scripts/verify_sector_snapshots.py` from the
repository root.
