# Teaching material

Two courses and the build engine that generates them. The course builders in `scripts/` generate the teaching artifacts. Numerical examples have executable checks; fictional datasets and teaching assumptions are labelled.

Additional programmes: [School Track camp marketing](Schools_ML_Track/camp_2026/marketing/README.md) and [professional AI training](Professional_AI_Training/README.md).

Current readiness and remaining deployment work: [rework status](review/2026-09-14/REWORK_STATUS.md).

**Teaching materials:** use the updated PowerPoints in [decks](IUEA_Teaching_Plan/decks/README.md). CML3111/CML3113 are revised from Week 2 and CML3112 from Week 3. Open Presenter View for the worked explanations and teaching prompts. Use the [lecturer guide](IUEA_Teaching_Plan/Beginner_Lecturer_Guide.md) and matching student ZIP. Practice notebooks are separate from graded submissions. The HTML lesson route has been retired. Rebuild with `scripts/build_decks.py`; build practice notebooks with `scripts/build_beginner_pathway.py --verify`, then student ZIPs with `scripts/build_student_packages.py --beginner-update`.

| | **IUEA machine learning** | **Data Analysis track** |
|---|---|---|
| Who | Year 3 engineering undergraduates, IUEA | Adults in work, confident in a spreadsheet, no code |
| Shape | 15 weeks, 3 cohorts, 45 contact hours each | 5 weeks, 15 sessions, 45 hours |
| Decks | 45 (15 weeks x 3 cohorts), 1,569 slides | 15, 356 slides |
| Codes | CML3111, CML3112, CML3113 | — |
| Where | `IUEA_Teaching_Plan/` | `DataAnalysis_Track/` |

They share `scripts/pptxkit.py` and `scripts/docxkit.py`, so a change to
either affects both and both validation harnesses should be run.

## Layout

```
IUEA_Teaching_Plan/          the IUEA deliverables — teach from these
  decks/                       45 .pptx, one per week per cohort
  grader/                      notebook autograder, gradebook.gs,
                               create_quiz_forms.gs (36 Google Forms)
  *.docx *.xlsx                master plan, three syllabi, teaching guide,
                               setup guide, runsheet, quiz operations guide,
                               tech build plan, roadmap benchmark, preflight
  quiz_timer.html              the projected countdown for the weekly quiz
  QR_encoder_acceptance_test.png   scan this to prove the QR encoder works

DataAnalysis_Track/          the professional course — its own README
  decks/                       15 .pptx plus MANIFEST.txt
  labs/                        SQL, Python and Power BI lab handouts
  data/                        the generated teaching dataset + answer key
  figs/                        12 explainer figures
  *.docx *.xlsx                plan, lecturer guide, glossary, workbook

scripts/                     the build engine
  pptxkit.py docxkit.py        slide and document primitives, shared
  plan_content.py              the IUEA curriculum: what each week teaches
  da_content.py                the Data Analysis curriculum, and its glossary
  da_keys.py                   every number the DA slides quote, from the
                               generated answer key
  build_*.py                   one builder per deliverable
  make_figures.py              the IUEA figure library -> figs/
  make_da_figures.py           the 12 DA explainer figures
  qrgen.py qrgen_selftest.py   from-scratch QR encoder, and the self-test
                               that checks it against OpenCV
  attach_qr.py                 stamps live QR codes into the 36 quiz decks
  quiz_banks.py                the 12 weekly quiz banks, 60 questions
  verify_*.py                  the verifiers; see below
  validation/                  overflow_scan, claim_check, segref_check

figs/                        the IUEA figure library (input to those decks)
data/                        IUEA lecturer notes (json) and quiz_links.json
qr/                          the 36 quiz QR codes
review/2026-09-14/           an independent review of the whole pack
```

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
[assessment operations](IUEA_Teaching_Plan/grader/README.md) for timed submission
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

**Data Analysis track**: see `DataAnalysis_Track/README.md`, which has its
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

`review/2026-09-14/REVIEW.md` is an independent review of both courses. Two
of its findings have been fixed: a documented build command that overwrote
twelve live decks with an older implementation, and a Power BI average that
divided delivered revenue by all orders and read 19% low in silence. Both now
have a verifier check so they cannot return.

The follow-up [rework status](review/2026-09-14/REWORK_STATUS.md) records the
current fixes and remaining work. Challenge-week aggregation, isolated
notebook execution and Week 2 delivery instructions have been corrected.
Week 2 has a calibrated local grader; later assessments require their own
validation before release. The original review describes the pre-change state.

The review's evidence folder is not committed. It is 18 MB of extracted deck
text and tool output, all of it regenerable from this repository.

For weekly delivery, use [Before each class](IUEA_Teaching_Plan/Before_Each_Class_Checklist.md). [Today’s CML3112 student links](IUEA_Teaching_Plan/Week2_CML3112_Student_Links.md) include the authorized Week 1 catch-up window.

## Repository size and generated files

Keep current teaching deliverables, editable sources, original assets and required build baselines in Git. Temporary render images, staging copies, `.build/`, `.qa/`, `.chart-data-*/`, Python caches and duplicate handoff exports are disposable. Older School Track flyer editions are available in Git history; use the current files linked from the marketing README.

The Business AI course keeps approved illustration bytes, its small hash-checked rebuild baseline and observed-run evidence. Synthetic voice transcripts and measured timings stay versioned; large regenerated recordings are optional local outputs. See its authoring README before rebuilding.

Private assessment records and local Python environments stay outside version control. Written review findings and authoring records are retained; superseded render media may be removed. Use normal `git gc` to compact local Git objects. Deleting a tracked export reduces the checkout, while its historical versions remain recoverable in Git.
