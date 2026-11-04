# Student packages: what is current and what is superseded (4 November 2026)

The semester ends at Week 12. Weeks 8 to 11 content is taught in four classes (see `../second_half/Plan_Weeks_8-12.pdf`). The class lab packs are in `../second_half/Student Packages/` (`CML31xx_Class1_lab_pack.zip` to `Class4_lab_pack.zip`). Send those to students after each class.

## The `CML31xx_W08` to `W12` ZIPs in this folder

| What they are | Status |
|---|---|
| Assignment packs for **Block 1** (A7 = W08, A8 = W09) and **Block 2** (A9 = W10, A10 = W11, A11 = W12): the graded notebook, the CSV and a one-page `START_HERE.md` with the block deadline and the form link. Rebuilt on 2 November 2026 by `scripts/build_block_packages_20261102.py`. | **Still current as assignment packs.** The A7 to A11 submissions are unchanged, so these ZIPs are still the files students work from for the block assignments. |
| The old per-week class materials these ZIPs were once sent with (Weeks 8 to 12 decks, `guided_practice.ipynb` for Weeks 8 to 12) | **Superseded** by the four class decks and lab notebooks in `../second_half/`. `guided_practice.ipynb` inside these ZIPs is old practice material; it is not marked and not needed. |
| Any Week 13, 14 or 15 package, a Practical Test 2 revision package, a demo package | **Do not exist or are not used.** The old Test 2 revision resources are in `../test_revision/` and are retired. |

Weeks 2 to 6 ZIPs are unchanged and already used.

## Scripts

- `scripts/build_student_packages.py` writes Weeks 2 to 12 and, for Weeks 8 to 12, would write the OLD `ASSIGNMENT_INSTRUCTIONS.txt` instead of the new `START_HERE.md`. **Do not run it for Weeks 8 to 12.** `tests/test_concise_iuea_assignments.py` expects `START_HERE.md`.
- For the block assignment packs use `scripts/build_block_packages_20261102.py` (it reads `data/assessment_blocks_20261103.json`).
- The class lab packs are built by `second_half/Build/kit/package_students.py`.
- `CML3113_W08_student/` (an unzipped folder) is a working copy of the CML3113 Week 8 pack.
