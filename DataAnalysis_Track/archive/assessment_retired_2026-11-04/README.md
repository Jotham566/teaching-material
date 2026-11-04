# Retired assessment material, 4 November 2026

The lecturer decided on 4 November 2026 that none of the KLAi professional programs has an exam or any assessment. Learners build practical projects and keep them. Everything here belonged to the old assessment design for the Data Analysis course and is kept for the record only. Nothing in the live course uses it.

| Item | What it was |
|---|---|
| `assessment_banks/S09`, `S13`, `S15` | Task sheets, issued notebooks, copies of the course data, assignment instructions and student how-to files for the three marked assignments (Session 9 reconciliation and cleaning log, Session 13 sector investigation, Session 15 capstone numerical evidence). |
| `student_guides/DA/S05.md, S09.md, S13.md, S15.md` | The matching student guides, with submission steps and marking checks. |
| `student_packages/DA_S09_student.zip` | The issued Session 9 student package. |
| `learner_roster_template.csv` | The roster that fed the gradebook. |
| `STUDENT_HOW_TO_assessment_version.md` | The old getting-started file, which was mostly submission instructions. |
| `DataAnalysis_Track_Workbook_with_mark_sheet.xlsx` | The workbook with the Assessment weights sheet (15, 15, 30, 40) and the Mark sheet with working formulas. |
| `DataAnalysis_Track_Plan_with_assessment.docx` | The plan with its Assessment section. |
| `scripts/build_da_assessments.py`, `build_sector_assessment.py` | The generators for the Session 9 and Session 13 banks. They wrote into the shared grader folder as well. |

Not moved, because the university course and its tests share them: the grader code in `IUEA_Teaching_Plan/grader/` (da_gradebook.py, da_contracts.py, da_reference.py, da_sql_grade.py, the S09 and S13 specs and rubrics) and `scripts/build_student_packages.py`, `build_assignment_instructions.py` and `build_submission_forms.py`, which still contain Data Analysis branches. Do not run those for this course.
