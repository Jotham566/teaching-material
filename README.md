# Teaching material

Two courses and the build engine that generates them. Every deck, document,
workbook, figure and dataset in this repository is produced by a script in
`scripts/`, and every number in them is computed rather than typed.

| | **IUEA machine learning** | **Data Analysis track** |
|---|---|---|
| Who | Year 3 engineering undergraduates, IUEA | Adults in work, confident in a spreadsheet, no code |
| Shape | 15 weeks, 3 cohorts, 45 contact hours each | 5 weeks, 15 sessions, 45 hours |
| Decks | 45 (15 weeks x 3 cohorts), 1,488 slides | 15, 351 slides |
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

```bash
python3 -m venv .iuea-env
source .iuea-env/bin/activate
pip install -r requirements.txt
```

Python 3.10 or newer. LibreOffice and Poppler are needed only to render a
deck and look at it, which the verification steps do. The notebook grader and
the teaching-data generator are standard library only, on purpose, so they
run on a locked-down work laptop.

## Rebuilding

**IUEA course**, from `scripts/`:

```bash
python3 make_figures.py            # figure library -> ../figs/
python3 build_decks.py             # runs the five deck builders: 45 decks
python3 attach_qr.py               # live QR codes into the 36 quiz decks
python3 build_teaching_guide.py    # reads the builders' lecturer notes
python3 build_master_docx.py build_syllabi.py     # ... and the other docs
python3 build_quiz_forms_gs.py     # -> grader/create_quiz_forms.gs
python3 build_quizops_docx.py
```

**Data Analysis track**: see `DataAnalysis_Track/README.md`, which has its
own ordered list. Start with `data/build_teaching_data.py`, because
everything downstream reads the answer key it writes.

## Verifying

Nothing ships unless these are green. They do more than lint: they execute
every SQL and pandas snippet that appears on a slide or in a handout against
the real data, and trace every currency figure back to a computed value.

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
python3 scripts/attach_qr.py --check             # 36 live QR codes
```

## Three things worth knowing before you change anything

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

Its remaining findings are open, and they are about assessment rather than
teaching material: the gradebook selects the wrong challenge weeks,
instructor-side notebook evaluation can be manipulated by notebook code, and
Week 2 has conflicting delivery instructions. Read that file before relying
on automated marking.

The review's evidence folder is not committed. It is 18 MB of extracted deck
text and tool output, all of it regenerable from this repository.
