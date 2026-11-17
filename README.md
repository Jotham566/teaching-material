# Teaching material

Everything I teach, in three programmes, plus the build engine that generates the slides, notebooks and documents.

## Start here

| I want to... | Go to |
|---|---|
| Teach IUEA Machine Learning (CML3111, CML3112, CML3113) | [IUEA_Teaching_Plan/](IUEA_Teaching_Plan/README.md) |
| See where the IUEA course is now | [Teaching progress](IUEA_Teaching_Plan/Teaching_Progress.md) |
| Run the final ML project (23 to 25 November 2026) | [IUEA_Teaching_Plan/Weeks_08-12/Project/](IUEA_Teaching_Plan/Weeks_08-12/Project/README.md) |
| Teach the high school holiday camp (S.4 to S.6) | [High_School_Camp/](High_School_Camp/README.md) |
| Teach professional and corporate classes | [Professional_Training/](Professional_Training/README.md) |
| Rebuild or verify anything | [scripts/](scripts/) and the sections below |

## Layout

```
README.md                      this map
IUEA_Teaching_Plan/            University: IUEA Machine Learning for Engineers (Year 3)
  README.md                      index of the course folder
  Teaching_Progress.md           where each class is now
  Plans_and_Syllabi/             master plan, the three syllabi, roadmap, curriculum maps
  Lecturer_Guides/               teaching guides, checklists, runsheets, the quiz timer
  Weeks_01-07/                   decks, guided practice, practicals, setup, student packages
  Weeks_08-12/                   the second half: slides, labs, lecturer guides, and Project/ (the final ML project)
  Assessments/                   assignments, quizzes, tests, the grader, the test portal, marks policy
  _archive/                      dated logs, old notebooks and backups
High_School_Camp/              the KLAi Holiday Data and AI Camp for S.4 to S.6 students (camp_2026/)
Professional_Training/         professional and corporate classes
  Business_AI/                   AI courses for professionals and executives
  BIK_Capital/                   client programme
  Data_Analysis_Course/          the 5-week data analysis course for adults in work
  KLAi Logo/                     brand files
scripts/  tests/               the shared build engine and its tests
figs/  data/  qr/              figures, notes data and quiz QR codes used by the builds
_archive/                      old backups and the September to October reviews
```

The IUEA course and the data analysis course share `scripts/pptxkit.py` and `scripts/docxkit.py`, so a change to either affects both
and both validation harnesses should be run.

**Weeks 1 to 7:** use the PowerPoints in [Weeks_01-07/decks](IUEA_Teaching_Plan/Weeks_01-07/decks/README.md) with Presenter View, the
[lecturer guide](IUEA_Teaching_Plan/Lecturer_Guides/Beginner_Lecturer_Guide.md) and the matching student ZIP. Rebuild with
`scripts/build_decks.py`; practice notebooks with `scripts/build_beginner_pathway.py --verify`, then student ZIPs with
`scripts/build_student_packages.py --beginner-update`.

**Weeks 8 to 12:** four classes in [Weeks_08-12/](IUEA_Teaching_Plan/Weeks_08-12/README.md) (slides, lab notebooks, lecturer guides,
student packages, the plan PDF), then the individual, timed, automatically marked ML project.

## Setting up

This Mac has a Python 3.12 environment with the pinned dependencies installed:

```bash
source .iuea-grader-env/bin/activate
python --version
```

Use it for the build and grading commands below. The older `.iuea-env` uses
Python 3.9 and is retained separately; it is not the supported grading environment.
To recreate the environment on another machine, use a Python 3.11-or-newer
interpreter, for example:

```bash
python3.12 -m venv .iuea-grader-env
source .iuea-grader-env/bin/activate
python -m pip install -r requirements.txt
```

LibreOffice and Poppler render documents and decks for visual review. Instructor
notebook grading requires Docker and the pinned grading image. Local report/slide
grading uses Ollama with cloud access disabled. See
[assessment operations](IUEA_Teaching_Plan/Assessments/grader/README.md) for timed submission
forms, complete-cohort grading and gradebook imports.

## Rebuilding

**IUEA PowerPoint teaching edition**, from the repository root:

```bash
python3 scripts/build_decks.py
python3 scripts/build_beginner_pathway.py --verify
python3 scripts/build_student_packages.py --beginner-update
python3 scripts/build_beginner_lecturer_docx.py
```

Use the bundled Python runtime for Word generation. `build_decks.py` locates the bundled Artifact Tool runtime and preserves the four completed teaching decks. It creates QR images and hyperlinks within the revised decks using the existing link registry, so do not run the legacy QR insertion or legacy weekly deck builders afterwards. The older `pptxkit` builders and their notes belong to the previous teaching edition.

**Data Analysis track**: see `Professional_Training/Data_Analysis_Course/README.md`, which has its
own ordered list. Start with `data/build_teaching_data.py`, because
everything downstream reads the answer key it writes.

## Verifying

Run the relevant validators before release. They check quiz arithmetic, selected SQL/pandas examples, dataset-derived claims, QR links and slide structure. Read their coverage and inspect rendered layouts; passing validators does not certify all teaching or assessment behaviour.

```bash
python3 scripts/verify_quiz_arithmetic.py        # re-runs every quiz snippet
python3 scripts/verify_da_track.py               # 41 checks
python3 scripts/verify_da_decks.py               # 24 checks
python3 scripts/verify_da_workbook.py
python3 scripts/validation/overflow_scan.py      # both courses, 60 decks
python3 scripts/validation/claim_check.py
python3 scripts/validation/segref_check.py
python3 scripts/qrgen_selftest.py                # needs OpenCV for the part
                                                 # that actually proves it
python3 scripts/verify_beginner_pathway.py      # revised PPTX and student packages
```

## Legacy deck implementation notes

**Slide type sizes come from a ramp, not from the numbers in the code.**
`pptxkit._scaled()` lifts text of 13pt and below by 1.32 and tapers to no
change at 30pt, so body text projects to the back of a hundred-seat room
while display type is untouched. It applies in `tb()` and `theight()` only,
which is what keeps the shrink-to-fit loops measuring what they draw. Change
`LIFT` and you must rebuild every deck and re-run `overflow_scan.py`.

**A bounds check cannot see a collision.** Two paragraphs printed over each
other are both inside the slide, so the scanner reports nothing. The only
way to know a deck is right is to render it and look at it, which is why
several verification steps do exactly that.

**Never accept a round trip through your own code as proof.** The QR encoder
passed thirteen round-trip tests, a byte-for-byte image check and a visual
inspection while producing codes that no phone could read, because the
encoder and the decoder shared the same wrong convention. It took an
independent implementation (OpenCV) to find it. The same rule applies to the
HMAC tokens in the grader.

## Review

`_archive/review/2026-09-14/REVIEW.md` is an independent review of both courses. Two
of its findings have been fixed: a documented build command that overwrote
twelve live decks with an older implementation, and a Power BI average that
divided delivered revenue by all orders and read 19% low in silence. Both now
have a verifier check so they cannot return.

The follow-up [rework status](_archive/review/2026-09-14/REWORK_STATUS.md) records the
current fixes and remaining work. Challenge-week aggregation, isolated
notebook execution and Week 2 delivery instructions have been corrected.
Week 2 has a calibrated local grader; later assessments require their own
validation before release. The original review describes the pre-change state.

The review's evidence folder is not committed. It is 18 MB of extracted deck
text and tool output, all of it regenerable from this repository.

For weekly delivery, use [Before each class](IUEA_Teaching_Plan/Lecturer_Guides/Before_Each_Class_Checklist.md). [Today’s CML3112 student links](IUEA_Teaching_Plan/_archive/Week2_CML3112_Student_Links.md) include the authorized Week 1 catch-up window.

## Repository size and generated files

Keep current teaching deliverables, editable sources, original assets and required build baselines in Git. Temporary render images, staging copies, `.build/`, `.qa/`, `.chart-data-*/`, Python caches and duplicate handoff exports are disposable. Older School Track flyer editions are available in Git history; use the current files linked from the marketing README.

The Business AI course keeps approved illustration bytes, its small hash-checked rebuild baseline and observed-run evidence. Synthetic voice transcripts and measured timings stay versioned; large regenerated recordings are optional local outputs. See its authoring README before rebuilding.

Private assessment records and local Python environments stay outside version control. Written review findings and authoring records are retained; superseded render media may be removed. Use normal `git gc` to compact local Git objects. Deleting a tracked export reduces the checkout, while its historical versions remain recoverable in Git.
