# IUEA Machine Learning: second half of Semester 1 (Weeks 8 to 12)

Four classes, concepts first, then the lab. Read `Plan_Weeks_8-12.pdf` first.

| Folder | What |
|---|---|
| `Slides/<cohort>/` | One KLAi deck per class (spoken script in the notes). Concepts, then a "Part 2" divider, then the lab slides. |
| `Lab Notebooks/<cohort>/` | The lab notebook for each class and the CSV it reads. |
| `Student Slides PDF/` | The decks as PDF without notes, for students to revise from. |
| `Student Packages/` | ZIP per cohort and class: notebook, CSV, START_HERE. |
| `Lecturer Guides/` | One guide per class: clock (Tuesday and Friday), slide map, questions to ask, numbers per cohort, rescue plans. |
| `Build/` | Sources and tools. `AUTHORING_GUIDE.md` explains the pattern. |
| `Project/` | The Engineering ML project (45 percent of the course): student briefs, Part A notebooks, hidden grader specification with proofs, marking guide. Start with `Project/README.md`. |

Rebuild from `Build/` (set `PPTX_SKILL_SCRIPTS` to the pptx skill scripts folder):

```
python3 kit/lint_content.py
python3 kit/deck.py          # all decks, or: kit/deck.py 2 CML3112
python3 kit/make_labs.py     # writes and runs the notebooks
python3 kit/make_guides.py
python3 kit/package_students.py
python3 kit/make_plan.py
```

Every number on a slide comes from `Build/ref/week_reference_numpy.py` run on the cohort's CSV. The notebooks are run against a NumPy stand-in for scikit-learn (`Build/ref/sklearn`); run each once in real Colab before class.
The older decks for Weeks 8 to 15 in `../decks` are unchanged and superseded for Weeks 8 to 12.
