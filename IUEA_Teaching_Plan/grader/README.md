# grader/ - auto-grading for CML3111 / CML3112 / CML3113

One system, replacing the loose scripts in `assessment-tools/`. A student runs a
check cell and gets told what is wrong. They run a submit cell and get a code to
paste into a Google Form. One command grades the week and one gradebook holds
the weighted total.

Python standard library only. No server, no JupyterHub, no Docker, no pip
install, no network. Everything runs on the lecturer's own Google account and on
the students' Colab sessions or laptops.

## Files

| file | what it is |
|---|---|
| `iuea_grader.py` | the module students import. Checks, feedback, submission codes, `verify_token()` |
| `specs/spec_W05.py` | W05 handout spec: pandas load, filter, groupby, derived column. 6 questions, 20 marks |
| `specs/spec_W03.py` | W03 handout spec: variables and functions from engineering formulas. 5 questions, 20 marks, one question per cohort |
| `specs/hidden/spec_W05_hidden.py` | the W05 hidden checks. Never handed out |
| `specs/hidden/spec_W03_hidden.py` | the W03 hidden checks. Never handed out |
| `spec_format.md` | how to write next week's spec |
| `batch_grade.py` | the weekly command. Grades notebooks, verifies Form codes, audits a sample |
| `gradebook.gs` | Apps Script for the Google Sheet: weighted total, best-of rules, code ingestion, progress line |
| `student_template.ipynb` | the notebook to copy each week |
| `simulate_cohort.py` | makes a fake cohort so you can load-test before Tuesday |
| `data/campus_energy.csv` | the W05 dataset, 8 meters, Jan-Mar 2026 |
| `_run_one_notebook.py` | generated. `batch_grade.py` writes it on every run and it is the thing that executes one student's notebook in a subprocess. Do not edit it; edit `RUNNER_SOURCE` in `batch_grade.py` |

## What the student does

1. Opens the notebook in Colab from the link in the course folder, or on their
   own laptop in Jupyter.
2. Runs the setup cell. It finds `iuea_grader.py`, the spec and the CSV next to
   the notebook, in `/content`, or on the shared Drive folder. On Colab with
   none of them present it asks them to upload the three files.
3. Does a task, runs `g.check("q1")`, reads the sentence, fixes it, runs it
   again.
4. Runs `g.check_all()` for the progress summary.
5. Puts their student number in the last cell and runs `g.submit("S24001")`,
   which prints a code around 110 characters long.
6. Pastes that code into the week's Google Form and uploads the notebook to the
   same Form.

Both halves are needed. The code carries the self-checked marks; the notebook is
what the real mark comes from.

## What the lecturer does, once a week

Download the Form's file uploads into one folder and its responses as CSV, then:

```bash
cd grader
python3 batch_grade.py -a W05 \
    -n ~/Downloads/W05_submissions \
    -t ~/Downloads/W05_responses.csv \
    --data-dir data \
    -o results/W05
```

That writes `results/W05/results.csv`, `results/W05/summary.txt`, and one
feedback file per student in `results/W05/feedback/`. Paste the
`notebook_total` column into the week's column in the Google Sheet, and mail the
feedback files out.

Read four numbers in the summary: `tokens UNVERIFIED`, `answer-hash mismatch`,
`SCORE DISCREPANCIES`, and `student id in doubt`. Everything else is routine.

Once a week, on a different day, audit:

```bash
python3 batch_grade.py -a W05 -n ~/Downloads/W05_submissions \
    -t ~/Downloads/W05_responses.csv --data-dir data \
    --sample 20 --seed $RANDOM -o results/W05_audit
```

## Setting it up, once

1. Open `iuea_grader.py` and change `SIGNING_KEY`. Put the same string in
   `gradebook.gs` as `SIGNING_KEY`. Do this before Week 3 and never again:
   changing it invalidates every code already collected.
2. Make a Google Drive folder, share it read-only with the class, and put
   `iuea_grader.py`, that week's `spec_W0n.py` and the data file in it, along
   with the notebook. `specs/hidden/` stays on your machine.
3. Make one Google Form per week with three questions: student number, the
   submission code, and a file upload for the notebook. Link it to the
   gradebook spreadsheet, which creates the "Form responses 1" sheet that
   `ingestTokenCsv()` reads.
4. In the Sheet, make a `Grades` sheet with these headers in row 1:
   `student_id, name, email, cohort, CP1..CP5, W03, W04, W05, W06, W08, W09,
   W10, W11, W12, W13, W14, Data Analysis Project, Practical Test 1,
   Practical Test 2, ML Project, Demo, Final %, Band, Challenges done, Missing`.
   Order does not matter; the script finds columns by header name and ignores
   case, spaces and underscores.
5. Paste `gradebook.gs` into Extensions > Apps Script, save, reload the sheet.
6. Run the checks below.

## Checks you can run yourself

```bash
python3 iuea_grader.py --selftest        # 18 checks on tokens and hashing
node gradebook.gs --test                 # 73 checks on the gradebook maths
python3 simulate_cohort.py --n 195 --out /tmp/fake
python3 batch_grade.py -a W05 -n /tmp/fake/notebooks \
    -t /tmp/fake/form_responses.csv --data-dir data --sample 20 --seed 1 \
    -o /tmp/fake/audit
python3 iuea_grader.py --verify IUEA1-...-...
```

`simulate_cohort.py` plants a corrupted code, a code signed with the wrong key,
a validly signed code with inflated marks, a Form row with no code, and a
resubmission. If a change you made stops the summary reporting all five, the
change broke something.

Measured on a 4-core Linux machine: 196 notebooks graded against all six tests
in **84 seconds**, 0.43 s per notebook. Four of those notebooks contain infinite
loops and each burns its full 20-second cell timeout, which is about 20 seconds
of the total. On a 2-core laptop expect three to four minutes. Budget five.

## The weights

| component | weight | rule |
|---|---|---|
| Block checkpoints | 10 % | best 4 of 5, each out of 10 |
| Weekly challenges | 10 % | best 8 of 11, each out of 20 |
| Data Analysis Project | 10 % | |
| Practical Test 1 | 15 % | offline, invigilated |
| Practical Test 2 | 20 % | offline, invigilated |
| Engineering ML Project | 25 % | |
| Demo / viva / reflection | 10 % | |

`node gradebook.gs --test` asserts these sum to 100 and that a student with full
marks everywhere scores exactly 100.

---

# LIMITATIONS

Read this before you rely on any number the system produces.

## Client-side grading cannot be made tamper-proof without a server

`SIGNING_KEY` is a string inside `iuea_grader.py`, and the student has that file
on their machine, because `g.check()` cannot work otherwise. A student who opens
it can read the key, import the module, and call `make_token()` with any marks
they like. The signature will be valid. **A determined student can forge a code
that verifies.** There is no version of this design that fixes that. Anyone who
tells you a client-side grader is secure has not read their own code.

What the mitigations actually buy:

- **The code is not the mark.** `batch_grade.py` grades the notebook, from a
  clean interpreter, against all six tests. That number is what goes in the
  gradebook. Forging a code changes a provisional figure and nothing else. The
  forgery only pays if you accept a code without a notebook, which is a
  temptation on a week when uploads fail.
- **The signature raises the effort.** Editing a character in a code is caught
  immediately. To forge, a student has to find the key, understand the token
  format, and call the function. That is a real filter, and a student who can do
  it has learned more than the assignment was teaching.
- **Sampling catches it statistically, and slowly.** `--sample 20` re-grades a
  random fifth. A student who forges one week is caught that week with
  probability 0.2. A student who forges all eleven weekly challenges is caught
  with probability 1 - 0.8^11, about 0.91. One forgery is very likely to get
  through. That is the honest number. Verified in practice: on the 195-student
  simulation, seed 1 caught the planted forger and seed 7 missed them.
- **The weight is small on purpose.** Weekly challenges are 10 % of the final
  mark, and only the best 8 of 11 count. Forging every challenge to full marks
  moves the final mark by at most 10 points, and only if the notebook is also
  faked. 35 % sits in two offline invigilated tests, and 35 % more in a project
  and a viva where the student has to explain their own work.
- **The answer fingerprint ties the code to the notebook.** A forged code keeps
  whatever hash the notebook produced, so `answer_hash_match` stays `yes` while
  the scores disagree. That is what the score comparison is for.

Do not present the token as a security control to the Faculty. It is a
tamper-evident receipt, and it works as one.

## Colab needs internet

A Colab session will not open, run or submit without a connection. On a bad
bandwidth day the class cannot submit. Three consequences:

- Keep the local Jupyter path alive. The same three files on a USB stick give
  identical behaviour with no network. `iuea_grader.py --selftest` passes
  offline, and so does everything else in this folder.
- Both practical tests run offline on lab machines. That is deliberate and it is
  what makes the AI policy enforceable.
- Friday 9 October 2026 is Uganda Independence Day and lands in Week 5, the
  pandas session, so the two Friday cohorts lose that class. `spec_W05.py` and
  the task sheet are written to be workable without the session.

## Everything else worth knowing

**Student code runs with your permissions.** `batch_grade.py` executes each
notebook in a subprocess in a scratch directory, which stops a runaway loop and
keeps files tidy. It is not a sandbox. A notebook containing `shutil.rmtree` or
`os.system` will do exactly what it says, as you. Grade on a machine that does
not hold the only copy of the gradebook, or in a throwaway VM. Nothing here
checks what the code does before running it.

**The per-cell timeout is Unix-only.** It uses `SIGALRM`. On Windows only the
120-second whole-notebook timeout applies, so one bad notebook costs two
minutes instead of twenty seconds. Grade on Linux or macOS.

**A cell timeout reports the wrong line.** There is no traceback to read, so the
feedback file names the first line of the cell rather than the loop. Four
students hit this in the simulation and the message was misleading each time.

**The answer hash can be wrong about an honest student.** It matches values, not
work. It changes if the student re-runs the notebook after submitting, edits a
number, or has a pandas version whose column sums differ in the sixth
significant figure. Treat `answer_hash_match = NO` as something to look at.
Across 189 real comparisons in the simulation it produced zero false positives,
which is reassuring and is not a guarantee.

**Marks depend on exact variable names.** `n_meters` and `nMeters` are a pass and
a fail. Every task sheet has to state the name, in a code font, and the
notebook's task cell has to repeat it.

**Nothing here marks a plot, a paragraph or a choice.** The grader compares
values. Judgement is what the project, the viva and the human half of the tests
are for. Do not let the auto-marked share grow past the current 35 %.

**Nothing here detects plagiarism.** On shared wifi, near-identical notebooks
will happen. The `answer_hash` column makes identical *answers* visible if you
sort by it, which is a weak signal, because the correct answer is the same for
everybody. Only the viva and the offline tests catch copying.

**Student identity comes from two unreliable places.** Google Forms renames an
uploaded file to `<original> - <Responder Name>`, so the file name often has no
student number in it. The grader falls back to the `STUDENT_ID` variable inside
the notebook, and flags any disagreement in the `id_source` column. A student
who mistypes their number in both places becomes an orphan row you fix by hand.

**Google Forms has no timer and cannot work offline.** You open the form and
switch off "Accepting responses" by hand. On a free `@gmail.com` account you
cannot restrict it to one response per person, so collect the student number and
de-duplicate in Sheets.

**Apps Script has hard caps.** A single execution stops at 6 minutes.
`recomputeAll()` and `ingestTokenCsv()` therefore write the whole block in one
`setValues()` call instead of one call per student; the per-row version does not
finish 195 rows. A free `@gmail.com` account sends to about 100 recipients a
day, so `emailStandings()` stops at 90 and resumes the next day.

**`GRADE_BANDS` in `gradebook.gs` is a placeholder.** Replace it with the IUEA
regulations before any student sees a letter.

**The token ingestion writes provisional marks.** `ingestTokenCsv()` writes the
code's visible-test total, which is not the assignment mark. Overwrite that
column with `notebook_total` from `results.csv` once you have run the batch.

**Nothing was tested on Google Colab or in Apps Script.** Both are behind a
network this build could not reach. The Python side was proven in a namespace
built exactly the way ipykernel builds a notebook's namespace, and the
gradebook's pure functions were proven under node. The two untested paths are
Colab's `files.upload()` in the setup cell and Apps Script's
`Utilities.computeHmacSha256Signature`. Both need ten minutes on the real thing
before Week 3.

**One Google account holds all of it.** That risk belongs to the teaching plan
rather than to this folder, and it has not gone away. Export `results.csv` and
the gradebook to the course share at the end of every block, so the
authoritative record is a file the university holds.
