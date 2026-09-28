# Teaching resources review

This records the original findings. See [REWORK_STATUS.md](REWORK_STATUS.md) for implemented fixes, verification and remaining release work.

**Reviewed 14 September 2026.** Scope: the IUEA engineering course, the independent Data Analysis track, generated teaching materials, Google Forms sources and public links, notebook grading, grade aggregation, and build/validation tools. Week 1 has already been taught; recommendations preserve existing submissions and published assessment commitments.

## Overall assessment

The educational design is substantially better than the operational readiness. Both tracks teach interpretation and judgement alongside code. IUEA's common programming spine with discipline-specific examples is sensible for mixed engineering cohorts; the independent track has a coherent business dataset and a useful spreadsheet-to-SQL-to-Python progression. These are worth retaining.

I would **not yet certify the whole pack for unattended delivery or high-trust automated marking**. The important problems are concrete: Week 2 has conflicting delivery instructions and missing practical assets; a documented build command overwrites current decks with an older implementation; the gradebook selects the wrong challenge weeks; and instructor-side notebook evaluation can be manipulated by notebook code. The Data Analysis capstone also teaches an average-order-value formula with an inconsistent population.

For this week, make a small, complete Week 2 release. Do not attempt to redesign the semester immediately. Resolve the grading defects before importing marks, and fix later teaching material ahead of its delivery date.

### Coverage and limits

- Read the Python/Apps Script sources, course plans, guides, lab instructions, assessment specifications, and both track READMEs. All 60 production Python files parsed successfully.
- Extracted text and speaker notes from all **60 current decks, comprising 1,839 slides**; inspected all 15 DOCX files as text and both workbooks as cells/formulas.
- Rendered and visually inspected the complete CML3112 Week 2 deck, DA Session 15 deck, and Week 2 runsheet. Other decks received text/notes and geometry checks, not a slide-by-slide visual inspection.
- Examined all 12 five-question quiz banks and their three cohort variants. Confirmed the generated Forms payload matches the source and the 36 quiz decks contain their corresponding QR image bytes.
- Opened all 36 public quiz links without submitting responses. All returned the intended cohort/week title and were **closed** at review time. This verifies destinations and closed-state access, not sign-in, answering, response receipt, or grade-release UX.
- Ran existing validators and synthetic notebook/Apps Script edge tests. Tests used review copies and invented students; no real grades or live form settings were changed.

Evidence is retained in [the evidence directory](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/review/2026-09-14/evidence). The initial inventory included 12 obsolete DA decks that disappeared during the review; they are **not an outstanding finding**. A later deck check instead flags an active PowerPoint `~$` lock file; the checker should ignore such files, not delete them while PowerPoint is open.

## Priority findings

**P1** means correct before the affected teaching/marking operation. **P2** means a material improvement to schedule before that material is used. These are review priorities, not institutional severity classifications.

### 1. P1 — Week 2 has several incompatible versions of the practical

The current slides use a Colab-first approach and an A2 repository submission, while the plan/runsheet still describe an offline installation clinic and supporting setup tools. References include `setup/README.md`, `build_offline_bundle.sh`, `check_setup.py`, `hello_engineering`, and four break/fix notebooks that are not delivered in this repository. The runsheet's ungraded eight-question CP0 also differs from the deck's five-question graded quiz.

This is likely to cause confusion at the point where novice students most need one dependable sequence. Across IUEA, the only delivered notebook is the Week 5 grader template and the only delivered CSV is `campus_energy.csv`; the later domain-specific practical filenames are mostly plans rather than available student assets.

**Action:** choose one Week 2 route and make the slides, runsheet, student instructions, quiz and A2 brief agree. Package the actual notebook(s), tiny cohort datasets, download link, expected output, submission instructions and a low-connectivity fallback. Rehearse from a fresh student account. Keep account setup and sign-in outside the quiz's five-minute teaching allowance.

Sources: [Week 2 builder](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/scripts/build_w23.py), [course plan](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/scripts/plan_content.py:124), [runsheet builder](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/scripts/build_runsheet_docx.py), [referenced-file inventory](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/review/2026-09-14/evidence/referenced_teaching_files.json). The file inventory is a candidate list: intentionally broken-path quiz examples are not missing deliverables.

### 2. P1 — The documented rebuild command overwrites current decks with legacy content

The root README describes `build_decks.py` as an orchestrator for all five current builders. It is actually a separate older implementation that generates Weeks 1–4 for the three cohorts and saves to the same output filenames. Running the documented command can replace 12 current decks and does not regenerate all 45.

**Action:** replace that entry point with the real five-builder orchestration, or retire it and correct the instructions. Build to a staging directory and compare the expected manifest before replacing published files. Do not rerun the legacy command as a verification step.

Sources: [documented command](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/README.md:77), [legacy save and loop](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/scripts/build_decks.py:591). The current builders are listed in the [codebase map](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/review/2026-09-14/CODEBASE_MAP.md).

### 3. P1 — The gradebook can omit earned work and silently miss quiz marks

The course plan's 11 challenges are A1–A11 in Weeks 1–6 and 8–12. `CHALLENGE_IDS` instead selects W03, W04, W05, W06, W08, W09, W10, W11, W12, W13 and W14. That excludes the first two assignments and includes weeks whose plan has no weekly challenge. Best-eight arithmetic can therefore be correct while counting the wrong work.

Separately, the grader README tells the lecturer to create `CP1..CP5` columns, but the parser expects `Q1..Q12`. A mocked run with the documented headers yielded twelve blank quiz values. The Forms response workbooks and the separate `Grades` sheet also do not constitute an automatic, student-ID-keyed quiz-to-final-grade import.

**Action:** define one assessment registry with assignment ID, teaching week, quiz sequence number, maximum, weight and submission source. Derive docs and gradebook headers from it. Preserve Week 1 marks. Reject missing required columns rather than converting schema mistakes into missing scores. Import by the roster's stable student ID, with reconciliation and duplicate handling. Quiz 7 corresponds to Week 8, so a sequence/week distinction matters.

Sources: [challenge selection](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/IUEA_Teaching_Plan/grader/gradebook.gs:57), [parser](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/IUEA_Teaching_Plan/grader/gradebook.gs:465), [incorrect header instructions](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/IUEA_Teaching_Plan/grader/README.md:89), [executable edge-test results](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/review/2026-09-14/evidence/edge_checks.json).

The intended weights themselves sum to 100%: quizzes 10, challenges 10, DA project 10, Test 1 15, Test 2 20, ML project 25, demo/viva 10. Preserve these unless an approved course-policy change is required.

### 4. P1 — Instructor-side notebook grading is not a trustworthy marking boundary

Notebook cells execute in the same Python process as the checker. A synthetic notebook containing no assignment answers replaced the check function in memory and received **20/20, including the hidden marks**, with status `OK`. This is a demonstrated marking bypass, distinct from the documented limitation that student-side receipts can be forged.

Temporary directories and timeouts help operationally, but they do not make the evaluator independent of student code. Running the same mutable evaluator inside a container would protect the host better without, by itself, fixing grade integrity.

**Action:** treat notebook execution as untrusted. Keep authoritative specifications and grade decisions outside the namespace/process that student code can modify, and execute student work with constrained resources and host access. Use authenticated execution results and appropriate task-specific evaluation. Until that boundary is implemented, use the batch output as marking assistance with independent review, not an authoritative final mark.

Sources: [execution and checking](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/IUEA_Teaching_Plan/grader/batch_grade.py:181), [synthetic result](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/review/2026-09-14/evidence/checker_integrity_case/results/results.csv). The proof used invented student S99998 in a review copy.

### 5. P1 — Duplicate submissions and incomplete specifications can corrupt marking

Two notebooks for the same invented student produced two result rows with different scores, but only one feedback file. `by_sid` keeps the last record; completion order can decide which duplicate survives downstream. Receipt deduplication does not solve notebook deduplication.

When a hidden check is absent, the batch grader warns that everyone will score zero for that question and continues. A packaging error must not become a cohort-wide penalty.

**Action:** select or quarantine duplicates before execution using a declared resubmission policy and immutable submission metadata. Fail marking preflight if required checks, datasets or dependencies are missing. Require one authoritative result per student and assignment before export.

Sources: [duplicate aggregation](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/IUEA_Teaching_Plan/grader/batch_grade.py:613), [missing-check handling](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/IUEA_Teaching_Plan/grader/batch_grade.py:522), [duplicate proof](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/review/2026-09-14/evidence/duplicate_case/results/results.csv).

Further controls are needed: validate marks against their maxima; the actual Apps Script accepted 500 as a quiz score and awarded 100 weighted points in a component worth 10. Select token-response sheets explicitly by assignment; the reader currently selects the first matching response sheet, even when another week is requested. Reconcile claimed IDs with the roster rather than trusting a filename or receipt alone. See [edge-test results](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/review/2026-09-14/evidence/edge_checks.json).

### 6. P1 for Week 2; P2 for Week 12 — Two quiz explanations contradict their own questions

**Week 2 Q4:** the status output says the notebook changes are unstaged. The correct option identifies the tracked/edited notebook correctly, but its feedback says committing now would save that edit. Another option's feedback correctly says a bare commit captures neither file. A temporary Git reproduction confirmed the bare commit fails with no staged changes.

Correct the feedback to say the notebook edit must first be staged. This can be repaired without changing the intended correct option.

**Week 12 Q4–Q5:** Q4 correctly distinguishes global importance from local attribution and rejects the claim that forests cannot be explained. Q5 then requires students to say a forest cannot provide a per-case reason, without specifying a stricter requirement for an exact, directly readable decision trace. The item confuses model transparency with the availability of local explanation.

Rewrite Q5 around an explicit acceptance requirement, or allow a carefully qualified local explanation. For the mining variant, also distinguish prediction explanation from evidence for a causal intervention.

Sources: [Week 2 feedback](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/scripts/quiz_bank_weeks.py:189), [Week 12 contradiction](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/scripts/quiz_bank_weeks.py:2753), [Git reproduction summary](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/review/2026-09-14/evidence/additional_checks.json).

### 7. P1 before DA Session 15 — Average order value uses inconsistent populations

The taught DAX expression divides delivered revenue by all distinct orders:

```dax
DIVIDE([Delivered Revenue UGX], DISTINCTCOUNT(orders[order_id]))
```

Without an external status filter, the delivered revenue is UGX 8,751,705,520 and the denominator is 6,000 orders, giving about UGX 1,458,618. Delivered orders number 4,837, giving the intended delivered AOV of about UGX 1,809,325. The taught result is approximately 19.4% low. A filter applied inside the numerator measure does not automatically filter its sibling denominator; see Microsoft's [CALCULATE documentation](https://learn.microsoft.com/en-us/dax/calculate-function-dax).

Use an explicit delivered-order measure and divide populations consistently:

```dax
Delivered Orders =
CALCULATE(DISTINCTCOUNT(orders[order_id]), orders[status] = "Delivered")

Avg Order Value UGX =
DIVIDE([Delivered Revenue UGX], [Delivered Orders])
```

Then verify unfiltered, date-filtered and region-filtered results. Define what product slicing should mean for AOV before assessing it, since the model's relationship directions affect which orders enter the denominator.

Sources: [slide source](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/scripts/da_deck_w5.py:382), [lab generator](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/scripts/build_da_labs.py:581), [data/SQL/Python validation](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/review/2026-09-14/evidence/verify_da_track.txt).

## Curriculum, program relevance and student experience

### IUEA

The sequence is defensible: engineering questions and predictions; setup; functions; collections/files; pandas; cleaning/charts; a test; regression; classification; validation; feature engineering; model comparison; reproducibility; final test; project defence. Keeping a common spine supports consistent assessment, while the examples make the purpose of programming visible.

| Cohort | What works | What needs strengthening |
|---|---|---|
| CML3112 — Civil and Architecture | Concrete strength, inspection records and quantities make units and predictions concrete. | Architecture deserves a clearer recurring thread: building performance, occupancy/daylight or material decisions, rather than being represented mostly through civil examples. |
| CML3113 — Mining and Petroleum | Flotation, process variables and operational trade-offs offer useful domain judgement. | Petroleum needs explicit recurring examples and data contracts, rather than depending on mining transfer. Include sampling/time alignment in process data. |
| CML3111 — Electrical, Mechatronics/Robotics and Communications | Energy, motors and maintenance suit electrical/mechatronics students. | Communications is less visible. Add a small recurring network/signal-quality example; robotics can include sensing/control-log interpretation without expanding the whole syllabus. |

Do not create three entirely separate courses. Give each represented program at least one recurring dataset or assignment option while retaining equivalent technical difficulty and marking criteria.

**P2 — Dataset claims must match the data.** AI4I is described in places as machine-hours with next-shift failure labels. The original dataset is synthetic and labels failure for a datapoint; it does not establish a next-shift forecasting task. Present it as a classification teaching dataset unless a genuine time-indexed target is constructed and documented. The concrete dataset includes ages from 1 to 365 days; a model trained across all ages is not simply a 28-day-strength model. Week 5 includes an age filter, but the later regression workflow needs the same explicit target contract or corrected wording. Sources: [UCI AI4I](https://archive.ics.uci.edu/dataset/601/ai4i+2020+predictive+maintenance+dataset), [UCI concrete strength](https://archive.ics.uci.edu/dataset/165/concrete+compressive+strength), [later content source](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/scripts/week_content.py).

Label unmeasured model gains as illustrative. Claims such as the normal improvement after feature engineering need a reproducible fitted example. Likewise, engineering thresholds described as mandatory need a named applicable reference and conditions; otherwise call them hypothetical teaching thresholds.

**P2 — Practical and assessment coverage is incomplete.** Only W03/W05 grader specifications exist, and only W05 has a student notebook. W03 expects collection/loop work before the main Week 4 treatment and does not cleanly mirror the slide challenge. Create an assignment-to-outcome matrix and distinguish automatically checkable outputs from reasoning, plots and professional judgement that require a rubric. Clear saved error output from the distributed template and test it in the declared student environment.

The planned Friday Week 5 disruption on 9 October is already recognized. Turn the proposed recording/package and Week 6 consolidation into actual deliverables for B and C so the three cohorts receive equivalent practice before later assessments.

### Independent Data Analysis track

This is a **five-week, 15-session, 45-hour** course for people with spreadsheet familiarity. It is a reasonable introductory applied track, not a basis for promising broad professional mastery. Its strongest design choice is reusing Riverside distributor data across SQL, Python and BI: joins, cleaning decisions and business measures have continuity. SQL precedes pandas, and the investigation culminates in an explanation rather than only a dashboard.

The source data and checks are unusually useful. The track generates 6,000 orders, 20,234 order lines, 401 customers, 120 products and 12 reps, including deliberate defects. SQL and Python checks pass. The small residual between cleaned raw currency calculations and the clean reference is explained by rounding; teach that reconciliation rather than silently claiming exact equality.

**P2 — Browser Power BI instructions need updating and rehearsal.** The lab says there is no full web Power Query editor. Microsoft's current service documentation supports full Power Query editing, subject to ownership, permissions and administrative settings. The lab also needs an exact route for bringing its five CSVs into one model. Rehearse with the account/license and device a student will actually use, especially on Mac. See [Microsoft's web model-editing documentation](https://learn.microsoft.com/en-us/power-bi/transform-model/service-edit-data-models) and [current lab](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/DataAnalysis_Track/labs/lab_powerbi.md:9).

The illustrated model is a snowflake-style arrangement with `orders` between some dimensions and lines, rather than a simple star. Correct relationship wording: Dates is the one side and orders the many side. Separate relationship cardinality from filter direction; Microsoft's [star-schema guidance](https://learn.microsoft.com/en-us/power-bi/guidance/star-schema) provides the relevant distinction.

**P2 — Session 15 needs its own timetable.** The generic 180-minute design includes a 50-minute lab, while the capstone brief requires 50 minutes to finish, then five minutes per learner plus questions, then 20 minutes on career/application. For 14 learners that is already 140 minutes before questions within that capstone block. Keeping the other generic blocks makes the session overrun substantially. Reserve a longer presentation block, run separate assessment appointments, or define an equivalent small-group format with individual evidence.

The four assessment weights—15% SQL, 15% cleaning, 30% investigation, 40% capstone—are coherent, but require criterion-level rubrics, submission requirements, resubmission rules and a clear completion standard. Evaluate reconciliation, assumptions, reproducibility and communication as well as correct outputs. No wholesale change in course scope is needed.

## Forms, timing and operational reliability

The bank's diagnostic questions and explanatory feedback are a strength. Questions ask learners to interpret failures, units, plots and decisions instead of only recalling definitions. However:

- All 36 links currently lead to closed forms. That can be intentional before class; opening the correct Week 2 form and checking it from a student account is still a release step.
- The five-minute timer is a teaching aid, not a server-enforced per-student timeout. The configured response window is 48 hours. Describe this honestly as a low-stakes open-window assessment if that is the intended policy.
- The operations material promises three versions per seating, but the implementation supplies one form per cohort and deterministic cohort option ordering. It does not supply three independently controlled versions per seating.
- Correct-answer feedback and an extended response window make sharing possible. With quizzes worth 10% and best ten of twelve, that may be an acceptable trade-off, but the policy should agree with the software. Do not retrospectively penalize Week 1 students for an unstated rule.
- Question text plus options spans roughly 310–491 words per quiz; Week 2 is about 415 words plus code interpretation. Pilot the five-minute allowance with representative novices. The word count alone does not establish an appropriate time limit.
- Offer a clickable text link as well as QR, and a declared connectivity/accessibility fallback. Actual form rendering of code alignment, mobile choice selection and feedback still needs student-view verification.

**P2 — Two maintenance paths are unsafe to trust without verification.** On a temporary Forms failure, `autoCloseQuiz` removes the pending close entry anyway, so the automatic retry is lost. Retain failed closures and retry/alert. `updateFeedbackAndIntro()` does not update question stems/help text; a changed title is skipped, and changed help text can remain stale. Its name and documentation overstate its repair scope. Use a targeted, verified update path for future forms and preserve completed Week 1 responses; do not rebuild all 36 indiscriminately.

Sources: [update function](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/scripts/build_quiz_forms_gs.py:1000), [closure cleanup](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/scripts/build_quiz_forms_gs.py:2208), [mocked failures](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/review/2026-09-14/evidence/edge_checks.json), [36 live-link results](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/review/2026-09-14/evidence/all_live_forms.json).

## Visual and document design

The shared palette, navigation and recurring explanation/practice/check rhythm create a recognizable course. The weakness is content density and fixed-height layout, particularly when a slide acts as both a projected prompt and a complete handout.

The rendered Week 2 deck has visible text collisions on slide 31 and an overlong challenge card on slide 33. DA Session 15 has a crowded trap card on slide 19 and overlapping challenge text on slide 22. These are renderer observations; a native PowerPoint check is still appropriate. The geometry scanner reported zero out-of-bounds shapes because text can collide inside valid shape bounds.

Across the 60 decks, 2,498 of 17,176 text runs are below the scanner's 14.4-point target; none are below its 12.4-point hard floor. This includes small labels, so it is not evidence that every affected slide is unreadable. It does justify a back-row projector check, especially for rasterized figure labels that the text scan cannot measure.

**Action:** shorten projected instructions, move reference detail to notes/handouts, and fix shared card layout rather than merely shrinking fonts. Remove character-count truncation in DA summary generation; it cuts some phrases mid-word. Render representative longest-content slides after changes.

The Week 2 runsheet is readable as a printed document, but its ten pages include a table-of-contents placeholder and sparsely filled continuation pages. A compact operational checklist would be easier to use while teaching. Other documents were reviewed as text only; their visual layout remains unverified.

Sources: [slide layout helpers](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/scripts/pptxkit.py:507), [DA deck builder](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/scripts/build_da_decks.py), [geometry/font scan](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/review/2026-09-14/evidence/overflow_scan.txt), [Week 2 renders](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/review/2026-09-14/evidence/render_week2), [DA Session 15 renders](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/review/2026-09-14/evidence/render_da15).

## What the automated checks establish

| Check | Result | Practical limit |
|---|---|---|
| DA data/SQL/Python | 41 checks, zero failures | Does not execute Power BI/DAX. |
| DA workbook | 58 checks passed | Static formula/arithmetic checks, not native spreadsheet-engine validation. |
| DA decks | 20 passed; final failure was a PowerPoint lock file | Ignore lock files in manifest checks. Earlier obsolete-deck issue was resolved during review. |
| Grader self-test | 18 passed | Does not test isolation from hostile notebook code. |
| Gradebook self-test | 73 passed | Misses curriculum/schema mismatch and demonstrated edge cases. |
| Quiz arithmetic | Passed | Several tests recalculate examples independently; they do not establish feedback semantics. |
| QR self-test | Internal checks passed | Independent OpenCV decoding skipped because unavailable. Exact embedded image equality is not a camera scan. |
| Slide scan | No shapes outside bounds | Does not detect all text overflow, overlap or raster readability. |
| Numeric claim check | Six title claims checked, no mismatch | Very narrow coverage. |
| Segment-reference check | Produced a human-readable listing | Not an asserting test suite. |

The larger simulation exercised 195 synthetic students plus one corrupt notebook. It detected a deliberately forged receipt score and caught four infinite loops with a shortened test timeout. All 195 normal notebook runs nevertheless reported cell errors because **matplotlib is absent from the available runtime**. That is an environment limitation, not evidence that all notebooks are defective or that clean end-to-end grading passed. It reinforces the need for a dependency preflight. See [simulation output](/Users/jothamwambi/Projects/IUEA-Teaching-Resources/review/2026-09-14/evidence/simulation_grade.txt).

Add focused tests for the actual failure boundaries: source-bank feedback assertions, assignment registry agreement, delivered-file existence, duplicate submissions, missing hidden checks, invalid mark ranges, keyed quiz imports, and evaluator integrity. Some current validators report findings without a failing exit status, so they are not sufficient build gates.

## Recommended delivery sequence

### Before this week's Week 2 lectures

1. Release one consistent practical kit for each cohort, including working notebooks/data and the agreed Colab/offline route.
2. Correct Week 2 Q4 feedback in source and verify it on the intended live forms.
3. Fix the Week 2 crowded slides and reconcile quiz/A2 instructions with the runsheet.
4. Open only the intended forms at the intended time; verify sign-in, mobile layout, identity fields, submission and feedback with a designated test account. This review did not perform a submission.
5. Preserve existing Week 1 scores and establish the correct challenge/quiz column mapping before entering more marks.

### Before the first batch of notebook marks is finalized

1. Fix the evaluator trust boundary, duplicate handling and missing-check failure policy.
2. Deliver the matching student template/spec/data for the actual assignment; preflight dependencies.
3. Reconcile roster IDs and quiz/challenge imports, with bounded marks and an auditable one-result-per-student export.
4. Perform one end-to-end rehearsal from submission through the final gradebook, including a resubmission and a missing submission.

### Before later modules and DA capstone

Correct dataset/target claims, the Week 12 explanation item, DA DAX, Power BI browser instructions and the capstone timetable. Build the missing practical assets progressively ahead of teaching. Publish concise rubrics and improve program balance through recurring examples rather than more topics.

### Repository maintenance

Establish one authoritative build entry point, one assessment registry, dependency declarations and version control. Separate student handouts from lecturer keys, hidden specifications and administrative scripts. Correct stale references to four weeks/36 hours, unwritten quizzes and twelve DA sessions. Keep generated artifacts reproducible and label current releases clearly.

**Review-only change record:** production materials, quiz settings and student records were not edited. The outputs of this work are this report, the codebase map and the evidence under the dated review directory.
