# Mathematics for AI and Machine Learning (KLAi, 36 hours, 18 sessions)

High school algebra is the only entry requirement. Learners choose Python (Google Colab) or a spreadsheet (Excel or Google Sheets); both labs use the same data.

| Folder | What |
|---|---|
| `Course_Outline_Mathematics_for_AI_and_ML.pdf` | The approved outline. |
| `Class Slides/` | 18 KLAi decks with a spoken script in the notes. Concepts, a black "Part 2" slide, the lab slides, then "Where this appears in AI". |
| `Class Slides PDF/` | The same decks as PDF for learners to revise from (no notes). |
| `Notebooks/` | The learner Python notebook for each session, with automatic checks. |
| `Workbooks/` | The learner spreadsheet for each session (Start here, work sheets, Check sheet). |
| `Learner Materials/` | Start Here, Formula Sheet (template), Glossary of Terms. |
| `Facilitator Materials/` | Facilitator Guide, Presenter Script, Solution Notebooks, Autocheck (capstone grader). Keep private. |
| `Build/` | Sources and tools. `Build/AUTHORING_GUIDE.md` explains the pattern. |

Rebuild from `Build/` (set `PPTX_SKILL_SCRIPTS` to the pptx skill scripts folder):
```
python3 kit/lint_content.py          # house-style checks
python3 kit/deck.py                  # all decks (or: kit/deck.py 5)
python3 kit/make_notebooks.py        # writes and proves the notebooks (solution passes all checks, learner does not)
python3 kit/check_workbooks.py       # recalculates every workbook with LibreOffice and proves the same
python3 kit/make_docs.py             # facilitator guide, presenter script, learner documents
```
The capstone (Session 18) is graded with `Facilitator Materials/Autocheck/grade_capstone.py`. Change its secret seeds before real use.

Not yet checked: the labs in real Google Colab, and the workbooks in Microsoft Excel and Google Sheets themselves (they were recalculated with LibreOffice).
