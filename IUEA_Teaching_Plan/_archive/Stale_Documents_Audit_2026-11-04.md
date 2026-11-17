<!-- SUPERSEDED_20261110 -->
> **Superseded on 10 November 2026 by `Grading_Policy_2026-11-10.md`.** The weights, the best-3-of-5 rule, the Week 6 waiver, the block rule and the provisional total out of 55 recorded below are history. From 10 November only A1 to A5 and Q1 to Q5 count: the final mark is assignments 20 + quizzes 20 + Practical Test 1 20 + Engineering ML project 40, and provisional results are out of 60. The body below is left unchanged as a record.

# Stale documents audit, 4 November 2026

What I checked: every md, json, py, gs, js, docx, xlsx, pptx and notebook text file under `IUEA_Teaching_Plan/`, `data/`, `scripts/`, `tests/` and the top-level README (excluding backups, virtual environments and the new `second_half/` build sources, which were written from the current plan). I searched for the old facts: Practical Test 2, the demo and Demo Day, Weeks 13 to 15, the take-home project, the project clinic, the 11 and 15 December dates, team projects, the old weights, the old blocks, Q11 and Q12 as live, and the old contact hours.

## The current truth every file must agree with
Four classes (Weeks 8 to 11 content), semester ends at Week 12, Week 12 is the individual, timed (3 hours), auto-graded Engineering ML project (proposed Tue 1 Dec for CML3112, Fri 4 Dec for CML3113 and CML3111). No Test 2, no demo. Weights quizzes 15, assignments 15, data analysis project 10, Practical Test 1 15, project 45. Block 1 = A7 + A8 and Q7 + Q8. Block 2 = A9 + A10 + A11 and Q9 + Q10. Q11 and Q12 retired. Provisional Semester 1 results out of 55 while the project is pending.

## Result
| Area | Files | Status |
|---|---|---|
| Policy source of truth | `data/assessment_blocks_20261103.json`, `Block_Assessment_Arrangement_2026-11-03.md` | Current. The 20261030 and 20261102 versions carry a superseded header. |
| Registry | `data/assessments.json`, `data/iuea_assignment_form_briefs.json`, `data/submission_links.json`, `data/test_portal_config.json` | TEST2 and DEMO are marked RETIRED; ML_PROJECT is a two-part, individual, timed sitting with no open window set. |
| Gradebook and grader | `grader/gradebook.gs`, `grader/continuous_assessment.py`, `IUEA_ML_Gradebook_Semester1.xlsx` | Current (2 Nov block rule, 3 Nov weights and provisional mode, 4 Nov project parts). |
| Syllabi (3), master plan docx and xlsx | `IUEA_ML_Syllabus_*.docx`, `IUEA_ML_Semester1_Master_Teaching_Plan.docx/.xlsx` | Current: calendar to Week 12, 36 contact hours, project sitting, weights. Remaining mentions of Practical Test 2 or the demo say they were dropped. |
| Student guides | `student_guides/<cohort>/B1.md`, `B2.md`, `ML_PROJECT.md` | Current. `DEMO.md` and `TEST2.md` open with a RETIRED notice. |
| Test material | `test_portal/README.md`, `test_revision/README.md`, `test_revision/*/Test2/` | Marked NOT USED at the top. Left in place as a record. |
| Old decks and ZIPs | `decks/` Weeks 8 to 15, `student_packages/` W08 to W12, `guided_practice/` | Unaltered, each folder has a `SUPERSEDED_README.md` pointing to `second_half/`. |
| New material | `second_half/` | Built from the current plan. Decks, notebooks, guides and student PDFs rebuilt on 4 November. |

## Left as history (not edited on purpose)
Build scripts under `scripts/` (including the `patch_*` scripts that made these changes), tests that check the retirement of the demo, `test_operations/private/` evidence and rehearsal logs, `test_operations/grading_output/` from the Test 1 rehearsals, the lecturer-notes JSON for old Weeks 11 to 15 (`data/lecturer_notes_build_w1115.json`, `slide_specific_lecturer_notes.json`, `spoken_notes_w1_7_13_15_20261030.json`) which feed only the old decks, and `test_portal/Packets.gs` which still holds the old Test 2 packet keys next to the new ML_PROJECT keys (the portal ignores a key that has no open window). Originals of every changed file are in the sibling `_backup_2026-11-04` (or `_backup_2026-11-03`, `_backup_2026-11-02`) folders.

## Not verified
- Word and Excel files were opened and converted with LibreOffice only, not with Microsoft Office.
- Nothing on Google was touched. Live forms, sheets and Apps Script projects change only when you run the by-hand lists.
- A text search finds words, not meaning. Two earlier checking agents were cut off by an API error, so I re-checked the live files myself by reading the passages around each remaining hit.

## Needs your decision
1. The project sitting dates and the 3-hour length (proposed).
2. Whether to move the old Weeks 8 to 15 decks and Test 2 revision folders into an Archive folder. I left them in place so old links still work.
3. The 36 contact hours figure in the syllabi (12 weeks of 3 hours, derived by me).
