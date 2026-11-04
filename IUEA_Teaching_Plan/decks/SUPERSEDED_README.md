# Old Weeks 8 to 15 decks: superseded (4 November 2026)

**Do not teach from the Week 8 to Week 15 decks in this folder.** They were written for a 15-week semester that ended in Practical Test 2 and a Week 15 Demo Day. That plan is gone.

## What is current

- The semester ends at **Week 12**. The content of Weeks 8 to 11 is taught in **four classes**, concepts first and then the lab. The decks, lab notebooks, lecturer guides and student packs are in `../second_half/`:
  - `../second_half/Slides/<cohort>/` the four class decks per cohort (use these, not `CML31xx_Week08` to `Week11`)
  - `../second_half/Lab Notebooks/`, `../second_half/Lecturer Guides/`, `../second_half/Student Packages/`, `../second_half/Student Slides PDF/`
  - `../second_half/Plan_Weeks_8-12.pdf` the plan, the calendar and the assessment in one place
- **Week 12** is the Engineering ML project: an individual, timed (3-hour), fully auto-graded Colab sitting. See `../second_half/Project/README.md`. There is no demo, no Practical Test 2 and no Week 13, 14 or 15.
- The assessment rules are in `../Block_Assessment_Arrangement_2026-11-03.md` (and `../data/assessment_blocks_20261103.json`).

## What stays in this folder

| Files | Status |
|---|---|
| `CML31xx_Week01` to `Week07` decks and their lecturer notes | Current. Already taught. Keep for reference. |
| `CML31xx_Week08` to `Week11` decks | Superseded by the four class decks in `second_half/Slides/`. Not deleted, not edited. |
| `CML31xx_Week12` deck | Superseded: Week 12 is the project sitting, not a class. |
| `CML31xx_Week13`, `Week14`, `Week15` decks | Superseded and not used (no Week 13 class, no Practical Test 2, no Demo Day). |
| `lecturer_notes/` for Weeks 8 to 15 | Superseded with their decks. Use `second_half/Lecturer Guides/`. |
| `README.md`, `LECTURER_NOTES_INDEX.md`, `READ_BEFORE_TEACHING.md` | The first two carry a 4 November note; the rows for Weeks 8 to 15 are marked superseded. |

## Scripts that rebuild or publish these decks

These scripts still exist and still write the **old** Weeks 8 to 15 decks. They are not the default path any more. Do not run them for Weeks 8 to 15; running them would regenerate superseded material and could overwrite notes:

`scripts/build_decks.py`, `scripts/build_beginner_decks.mjs`, `scripts/publish_beginner_decks.py`, `scripts/build_w78910.py`, `scripts/build_w1115.py`, `scripts/wk_8b_9_20261030.py`, `scripts/wk_10_12_20261030.py`, `scripts/wk_13_20261030.py`, `scripts/patch_week8_20261030.py`, `scripts/patch_weeks8b_12_20261030.py`, `scripts/patch_test2_deck_20261030.py`, `scripts/publish_slide_specific_notes.py`, `scripts/apply_spoken_notes_20261030.py`, `scripts/publish_csv_examples.py`, `scripts/publish_pandas_*.py`.

To rebuild the new decks use the kit in `../second_half/Build/` (`AUTHORING_GUIDE.md`; `python3 kit/make_plan.py` for the plan). Source data for the old decks stays in `../../data/` (`iuea_deck_content.json`, `lecturer_notes_build_w*.json`, `spoken_notes_w8_12_20261030.json` and similar) and is also superseded for Weeks 8 to 15.
