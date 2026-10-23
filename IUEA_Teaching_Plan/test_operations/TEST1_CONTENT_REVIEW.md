# Test 1: coding-only review — 23 October 2026

Applies to CML3111, CML3112 and CML3113. Version: `2026.10-test1-coding-v3`.
The lecturer confirmed no real students had started and authorised replacement for all three programmes.

## What students complete

| Task | Marks | Suggested minutes |
|---|---:|---:|
| Read CSV with pandas; preview, dimensions, missing cells, repeated IDs | 10 | 15 |
| Scatter chart before cleaning | 10 | 15 |
| Deduplicate, exclude invalid rows, fill missing ambient temperature | 20 | 25 |
| Scatter chart after cleaning | 10 | 10 |
| Mean, sum, median, count, sample standard deviation and equipment mode | 15 | 20 |
| Group equipment and aggregate target mean, sum and count | 15 | 15 |
| User-defined load classification with conditions | 10 | 15 |
| Loop through the cleaned dataset's loads and count categories | 10 | 20 |

Allow 10 minutes for setup, 135 for coding, 15 for checking and 20 for submission. This is a workload estimate, not a timed student pilot. All tasks use the same assigned CSV. Only pandas, matplotlib and ordinary Python are required. There are no interpretation choices, written judgements or ML models.

## Alignment with the taught material

The three programmes share these foundations, with programme-specific targets and units:

- Week 3, slides 36–48: conditions and comparisons; slides 49–62: functions, arguments and return values. Loop practice is also in Week 3.
- Week 5, slides 6–16: table inspection, selecting columns, missing values, averages and totals; slides 17–19: grouping.
- Week 6, slides 5–12 and 17–22: inspection, missing entries and duplicate IDs; slides 24–35: row filters and median filling; slides 36–38: grouping and `agg`; slides 42–45: plotting; slide 51: a function accepting record dictionaries and creating a DataFrame.
- The Week 6 guided notebooks provide the same raw → EDA → cleaning → summary → chart workflow.

Mode and standard deviation were not explicitly demonstrated in the Weeks 1–6 practice notebooks. The test therefore supplies their meaning, exact pandas syntax, sample-standard-deviation convention, and a tied-mode example. These are supported application questions, not recall of an untaught formula. The combined `groupby(...).agg(...)` syntax is supplied as a reference too.

The data conversion, function headers, return-dictionary keys and demonstration calls are supplied. Students complete the calculations and charts. Every new technical instruction specifies its input, output, column names, units and boundary rules. Cleaning rules match Week 6. Mean/sum/etc use cleaned target values; mode uses equipment labels so it is meaningful even with continuous target measurements. Multiple modes must all be returned.

## Grading and verification

- Eight deterministic checks total 100 marks; no Ollama grading.
- Hidden data differ from the visible CSV but use the same columns and rules.
- Numeric answers accept normal floating-point tolerance and unrounded results.
- Cleaning has partial credit by correctly retained column; index numbers are ignored.
- Statistics and grouped outputs earn independent partial marks.
- Plots must be real matplotlib figures. The grader checks points, title, labels and units, not colours or styling. Missing plot coordinates are handled correctly; duplicate points remain in the before chart.
- Conditional boundaries include 0, 40, 75 and 100. Loop checks include an empty list and the cleaned data. These questions require the requested Python control structure in the submitted function.
- Tested all nine completed Test 1 packets in Docker: 100/100. Blank packet: 0/100. Missing cleaning with other complete functions: 80/100. Wrong statistics and grouped columns lose only their component marks. Fake figure dictionaries are rejected.
- All nine Test 2 reference packets remain 100/100; their content was not changed.
- Portal regression checks cover all nine Test 1 packets, exact CSV injection, same-file resume, stable deadlines, personal expiry and final cutoff. Submission and intake regressions pass.

Existing recorded marks and submissions are not rewritten. New Test 1 results record the new grader version. Before grading on the Mac mini, pull the public teaching repository so it uses the matching grader.

## Timing retained

- CML3111 and CML3113: 23 October 2026, 19:00 to 29 October, 23:59 Kampala.
- CML3112: 27 October 2026, 19:00 to 2 November, 23:59 Kampala.
- Personal deadline: the earlier of three hours after Start test or the class closing time.

## Release verification

Published to the existing student portal as Apps Script version 11 on 23 October 2026 at 21:19 Kampala. Existing QR codes and URLs are unchanged. A separate synthetic Google workbook verified creation and repeated opening of the new coding-only notebook for each programme, without changing the production schedules or student marks. Private rehearsal evidence is excluded from Git.

The test intake builds the matching eight-question dispatch from the installed grader code. An older private snapshot's five-question Test 1 dispatch cannot silently override this release. Duplicate receipt handling and previously recorded results are preserved.

## Student workflow refinement

Task 1 now requires students to write their own pandas CSV-reading statement using `file_path`, storing the result in `raw_data`. This earns 2 marks within its existing 10 marks; the four EDA components earn 2 marks each. The final cleaned table is consistently `cleaned_data`. The supplied CSV preparation cell no longer imports pathlib or reads the file with pandas for the learner.

Setup, countdown, conversion, demonstration and submission cells are labelled and collapsed as forms. Colab hiding is not an edit lock; students can reveal or change code. The guide tells students to edit answer cells only and use Edit → Undo if they accidentally damage a support cell. The server still enforces the recorded deadline and allocation. Automatic submission necessarily uses hidden Colab/Google support libraries; those are not assessed student code.

The isolated grader reads literal identity fields from the skipped countdown cell without running browser code. A regression test now completes and grades an actual portal-generated packet, checking both identity and the CSV-reading task.

Deployment update: Apps Script version 12 was published successfully on 23 October 2026 at 21:46 Kampala time. It includes student-written CSV loading, concise instructions and collapsed support cells for all three programmes. Existing entry URLs, schedules and deadlines are unchanged.

## Superseding revision: ordinary notebook workflow (23 October 2026)

The lecturer confirmed that no real students had started and authorised replacement for all three programmes. Version `2026.10-test1-notebook-v4` replaces the function-heavy v3 layout:

| Task | Marks | Student work |
|---|---:|---|
| Read and inspect | 20 | CSV reading, head/tail, shape/len, column dtype, info, describe, missing counts, duplicate IDs, invalid rows |
| Before chart | 10 | Original-data scatter with `figure, axes` |
| Cleaning | 20 | Duplicate IDs, invalid/missing observations, median temperature fill |
| After chart | 10 | Cleaned-data scatter with `figure, axes` |
| Statistics | 15 | Mean, sum, median, count, standard deviation and all modes |
| Grouping | 10 | Equipment target mean and count using groupby/agg |
| One reusable function | 5 | Reuse mean/sum/median on a supplied table and column |
| Loop and conditions | 10 | Count load categories with for and if/elif/else |

The same assigned CSV is used throughout. `raw_data` is retained; `cleaned_data` is the cleaned result. Only Task 7 is a user-defined function. The two matplotlib scatter styles are accepted. DataFrame `.dtypes` and Series `.dtype` are distinguished; the assessed answer is the target column's `.dtype`.

Instructions explicitly say **Do not edit this cell** for support cells, and protected lines inside answer cells explain their purpose. Learners check their full name, **Student ID/ Registration Number**, and email before starting work and before submitting. These labels do not imply that Colab locks the cells.

Automatic marking reruns notebook cells in Docker against the assigned CSV; saved outputs are not trusted. Task 7 also runs on additional numeric data and different column names. The grader accepts legacy v3 notebooks with their original question weights. In v4, dependent tasks use the student's cleaned table: an incorrect cleaning result can therefore affect subsequent results. Every checked output receives its own partial credit; the whole test is not discarded because one cell fails.

Validation: all nine completed v4 packets scored 100/100 in isolation; all nine Test 2 packets still scored 100/100; blank work scored zero. Regression checks covered missing EDA operations, incorrect standard deviation, hard-coded function results, missing loop syntax, original v3 compatibility, and a real portal-generated notebook with preserved identity. Portal tests cover all allocations, strict personal/global deadlines, stable resume and disabled/future windows. No production windows or marks were altered.

Release verified: Apps Script version 14, 23 October 2026 at 22:41 Kampala time; Cloudflare Worker version `9e2c87be-9291-46b4-832c-4997c803be65`. All three public Test 1 pages returned HTTP 200 and the updated identity wording. Separate synthetic tutor-review notebooks were generated for all three programmes; the CML3111 notebook was opened and visually checked in Colab. No new end-to-end form submission was made in this revision. Pull the teaching repository on the grading Mac before processing v4 submissions.
