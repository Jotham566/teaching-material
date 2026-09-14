# Codebase map and maintenance guide

Reviewed 14 September 2026. Companion to the [findings report](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/review/2026-09-14/REVIEW.md).

## What this repository is

This is a teaching-material generation repository with two separate course products. It is not a deployed learning-management system. Python builds PowerPoint, Word, Excel, figures, labs and Apps Script; Google Forms/Sheets supply part of the live assessment workflow; notebook grading runs locally.

| Area | Purpose |
|---|---|
| [scripts](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/scripts) | Shared document/slide machinery, both curricula, builders, validators. |
| [IUEA_Teaching_Plan](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/IUEA_Teaching_Plan) | Engineering course outputs, video references and grader/forms code. |
| [DataAnalysis_Track](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/DataAnalysis_Track) | Independent course outputs, labs, generated teaching data and answer key. |
| [data](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/data) | IUEA quiz-link map and generated lecturer-note JSON. |
| [review/2026-09-14](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/review/2026-09-14) | This review and reproducible evidence; not student course material. |

The important distinction is **source versus generated output**. Fixing a generated slide or lab alone will not survive its next build. However, some outputs depend on generated intermediate files, so rebuilding an outer document does not necessarily refresh its content sources.

## IUEA course

### Teaching structure

| Cohort | Programs | Scheduled teaching |
|---|---|---|
| CML3112 / A | Civil Engineering and Architecture | Tuesday 11:00–14:00, Room 106; approximately 100 learners. |
| CML3113 / B | Mining and Petroleum | Friday 08:00–11:00, Room 105; approximately 40–50 learners. |
| CML3111 / C | Electrical, Mechatronics/Robotics and Communications | Friday 11:00–14:00, Room 115; approximately 50 learners. |

These are repository planning values, not independently checked timetable records. Week 1 is complete. Under the stored calendar, Week 2 falls on 15/18 September 2026. The Friday Week 5 interruption is already acknowledged in the course material.

| Weeks | Shared progression |
|---|---|
| 1–4 | Engineering problem framing; environment; functions; collections/files. |
| 5–7 | DataFrames; cleaning/visualization; Test 1. |
| 8–10 | Regression; classification; validation and leakage. |
| 11–13 | Feature engineering; model comparison; reproducibility/project work. |
| 14–15 | Test 2; demonstration and viva. |

The intended design is roughly 70% shared spine and 30% contextual adaptation. The actual representation is split across several modules rather than centralized completely.

### Source ownership and build flow

- [plan_content.py](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/scripts/plan_content.py): overall weekly plan, cohort metadata and assignments. This drives planning documents but is not the sole source of slide content.
- [week_content.py](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/scripts/week_content.py): later worked examples, labs and cohort-specific content.
- [build_week1.py](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/scripts/build_week1.py): current Week 1 decks and shared cohort helpers.
- [build_w23.py](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/scripts/build_w23.py): current Weeks 2–3 decks.
- [build_w456.py](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/scripts/build_w456.py): Weeks 4–6.
- [build_w78910.py](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/scripts/build_w78910.py): Weeks 7–10.
- [build_w1115.py](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/scripts/build_w1115.py): Weeks 11–15.
- [pptxkit.py](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/scripts/pptxkit.py), [make_figures.py](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/scripts/make_figures.py): slide primitives/theme and raster figures.
- [docxkit.py](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/scripts/docxkit.py), the plan/setup/runsheet/platform/quiz-operations builders, and [build_xlsx.py](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/scripts/build_xlsx.py): supporting Word/Excel materials.
- [build_teaching_guide.py](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/scripts/build_teaching_guide.py): teaching guide consuming lecturer-note JSON produced by deck builds.

The current five deck builders cover 3 cohorts × 15 weeks = **45 decks**. **Do not use the currently documented `build_decks.py` as their orchestrator:** it is an older competing implementation that overwrites Weeks 1–4. See finding 2 in the report.

Conceptual dependencies:

```text
plan_content + week_content + cohort dictionaries
                    │
figures + pptxkit ───┼──► five current deck builders ──► 45 decks
                    │                         └───────► lecturer-note JSON
                    └──► planning documents                │
                                                           ▼
                                                   teaching guide
```

Metadata and narrative duplication explain several current drifts. A small shared course/assessment registry would help more than adding another build script.

### Quizzes and live Forms

[quiz_banks.py](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/scripts/quiz_banks.py) defines schema/helpers and Week 1, then incorporates [quiz_bank_weeks.py](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/scripts/quiz_bank_weeks.py). There are 12 quiz weeks: 1–6 and 8–13. Each has five conceptual items, rendered for three cohorts.

```text
quiz banks
   ├──► slides / offline quiz timer
   └──► build_quiz_forms_gs.py
             └──► grader/create_quiz_forms.gs
                         └──► live Forms and cohort response workbooks
                                      │
                           exported/configured links
                                      ▼
                            data/quiz_links.json
                                      ▼
                              attach_qr.py
                                      └──► QR images + current deck rebuilds
```

The generated Apps Script contains the payload and operational functions: creation, feedback, open/close, checks and scheduling. A Python source change does not change a live form automatically. A source-to-generated-payload check also cannot prove that the deployed script or form has been updated.

The exact QR bytes in each current quiz deck match the intended generated image. The public link test found all 36 forms closed; live response behavior remains to be rehearsed. `build_quiz_timer.py` supplies an offline classroom timer, not a Forms response-time enforcement mechanism.

### Grading

| Component | Responsibility | Boundary/limitation |
|---|---|---|
| [iuea_grader.py](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/IUEA_Teaching_Plan/grader/iuea_grader.py) | Visible checks, result objects, receipt signing and answer fingerprints. | Student-side code and signing material are inspectable. Receipt verification alone is not proof of authorship or correctness. |
| [batch_grade.py](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/IUEA_Teaching_Plan/grader/batch_grade.py) | Copies submissions/resources to temporary directories, executes cells, performs visible/hidden checks and exports CSV/feedback. | Current checker executes in a process the student's code can modify. Duplicate notebook selection is unresolved. |
| [specs](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/IUEA_Teaching_Plan/grader/specs) | Assignment expectations and public/hidden checks. | Only W03 and W05 implemented. |
| [student_template.ipynb](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/IUEA_Teaching_Plan/grader/student_template.ipynb) | Student-facing notebook scaffold. | W05 only; not a generic template for every assignment. |
| [gradebook.gs](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/IUEA_Teaching_Plan/grader/gradebook.gs) | Token ingestion, best-of components, weights, final scores and feedback. | Expected headers/challenge IDs diverge from documentation and plan. No complete automatic quiz-to-final import. |
| [simulate_cohort.py](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/IUEA_Teaching_Plan/grader/simulate_cohort.py) | Synthetic normal/error/tampering scenarios. | Useful regression fixture; not a security assurance. |

The intended path is student practice/check → submission/receipt → instructor notebook regrade → reconciled gradebook. Every arrow needs an explicit student/assignment key. Treat graded output as provisional until the trust-boundary and reconciliation issues are resolved.

## Independent Data Analysis track

### Teaching structure

The actual current product is **15 sessions, three hours each, over five weeks**. It assumes spreadsheet familiarity. Content allocation in the plan is foundations 6 hours, SQL 9, Python 12, statistics 6, charts 3, investigation 3 and Power BI 6; Python-based work spans several of those categories.

Assessment: Session 5 SQL 15%; Session 9 cleaning 15%; Session 13 investigation 30%; Session 15 capstone 40%. The two courses' assessment systems should remain separate even where they share generation utilities.

### Data and source flow

- [da_content.py](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/scripts/da_content.py): course/session structure.
- [build_teaching_data.py](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/DataAnalysis_Track/data/build_teaching_data.py): deterministic Riverside business data, intentional defects and reference outputs.
- [answer_key.json](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/DataAnalysis_Track/data/answer_key.json), [da_keys.py](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/scripts/da_keys.py): computed reference values and formatted values used in teaching.
- `da_deck_w1.py` through `da_deck_w5.py` in [scripts](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/scripts): authored session content.
- [build_da_decks.py](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/scripts/build_da_decks.py), [make_da_figures.py](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/scripts/make_da_figures.py): render the 15 decks and figures.
- [build_da_labs.py](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/scripts/build_da_labs.py): generates SQL, Python and Power BI lab Markdown.
- DA plan, guide, glossary and workbook builders in [scripts](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/scripts): supporting artifacts.

```text
teaching-data generator ──► CSV/database data + answer_key.json
                                                │
                                             da_keys
                                                │
                 session definitions ───────────┼──► decks / figures
                                                ├──► labs
                                                └──► reference values in support materials
```

When data or a KPI changes, regenerate the dependent key, labs, figures and decks together. A SQL/Python validator does not establish DAX equivalence. Keep the answer key in lecturer materials rather than unintentionally treating the entire output directory as a student handout package.

## Validation and release discipline

Useful existing validators cover DA data, deck manifests, workbook arithmetic, quiz arithmetic, QR internals, gradebook calculations and grader checks. They have different scopes and do not all fail the process on findings. The report records exact results and limitations.

A practical future release order is:

1. Update the relevant authoritative content/data and assessment definitions.
2. Generate dependent figures, current decks, note intermediates, guides and labs into staging.
3. Check manifest completeness, referenced assets, semantic calculations and assignment mappings.
4. Render dense/changed slides and documents; inspect native application behavior where needed.
5. For Forms, apply targeted changes and verify the deployed student view separately.
6. Publish a clearly dated student package and retain the lecturer package and previous release.

This is a proposed maintenance sequence, **not a claim that a reliable single command already exists**. The repository currently lacks a dependable unified entry point, a locked runtime and Git history in this workspace.
