# AI and Data Science Professional: KLAi build folder

No assessment (lecturer decision, 4 November 2026): this course has no exam, marks, grades, pass marks, weights or scored rubrics. Learners build projects and keep them. Project milestones (Sessions 8, 13, 19) and the course project (Session 24) are reviewed for feedback and never scored. The check cells, recall questions and exit-check questions are self-checks. The certificate is 'a certificate of completion from KLAi Professional Learning', given for completing the course project. `kit/lint_content.py` and `kit/make_course_docs.py` flag assessment words (checkpoint, marking, graded, pass mark and so on).

Everything needed to rebuild the 24 decks, the lab notebooks and the course documents. The course is 24 sessions of 2 hours for Excel-confident professionals. Generated files are never edited by hand.

| Path | What |
|---|---|
| `AUTHORING_GUIDE.md` | How a session is written (fields, slide kinds, clock, labs, notes). Read first. |
| `TERMS.md`, `TERMS_base.md` | The terminology rule: the real industry term first, a plain explanation beside it. |
| `LOANS_RECIPE.md` | The loans model recipe shared by Sessions 14 to 17, 20 and 23. |
| `content/sNN.py` | One file per session: titles, question, outcomes, words, clock, slides, facilitator notes. The single source for decks, notebooks and documents. |
| `content/labs/sNN_nb.py` | The lab notebook of a Python session (learner and solution versions). |
| `kit/` | The build tools (below), the figure kinds (`diagrams_ds_*.py`) and the slide engine. |
| `templates_gen/` | The KLAi Word kit (`docx_kit.py`) and brand constants. |
| `brand/` | Logos and the Lato fonts. |
| `ref/` | Stand-ins and proofs used where scikit-learn, SciPy or statsmodels are missing. |

## Commands (run from this folder)

```
python3 kit/lint_content.py                # house-style and structure checks (0 problems expected)
python3 kit/deck.py [N ...]                # decks into ../../02 Class Slides (set PPTX_SKILL_SCRIPTS to the pptx skill scripts)
python3 kit/make_notebooks.py [N ...]      # learner and solution notebooks, then runs them (the first cell downloads data.zip from the link in data_zip_url.txt)
python3 kit/make_docs.py                   # Facilitator Guide, Presenter Script, Sheets Lab Sheets and Answers, Glossary, Start Here, checklist
python3 kit/make_course_docs.py [outline|setup|projects|benchmark|all]
                                           # Course Outline, Student Setup Guide, Course Projects Guide, Benchmark and Design Report
python3 kit/make_roadmap_klai.py           # Student Roadmap (one page), .pptx and .pdf
```

`make_course_docs.py` and `make_roadmap_klai.py` read session titles, questions, the project milestone tables and the project checklist from `content/sNN.py`, so they follow the decks. The short lab deliverables on the roadmap and in the outline live in `DELIVERABLE` in `make_roadmap_klai.py`; the roadmap build checks that the file names in them appear in the session text. Every soffice call uses its own `-env:UserInstallation` profile. `make_course_docs.py benchmark` builds every deck specification to count slides and notes, so it takes about 40 seconds.

## Where to change what

- A session title, question or deliverable: `content/sNN.py` (the deliverable short form: `DELIVERABLE` in `kit/make_roadmap_klai.py`).
- Course Projects Guide wording, setup steps, benchmark text: `kit/make_course_docs.py`.
- Terms: `TERMS.md` (shared; do not edit without the lecturer).

## Known limits

See `../Verification Record.txt`: Sessions 12 to 18, 20 and 23 have not run on the real libraries, nothing has run in Colab, and the data.zip Google Drive link in `data_zip_url.txt` is still empty (upload data.zip to Drive with Anyone with the link, paste the link, then regenerate the notebooks).
`templates_gen/docx_kit.py` prints "Mathematics for AI and Machine Learning" in its header and footer defaults. `make_course_docs.py` overrides both for this course. Changing the defaults to a parameter in the kit would remove the override.
