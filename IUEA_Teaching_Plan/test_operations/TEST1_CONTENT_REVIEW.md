# Test 1: coding-only review — 23 October 2026

Applies to CML3111, CML3112 and CML3113. Version: `2026.10-test1-coding-v3`.
The lecturer confirmed no real students had started and authorised replacement for all three programmes.

## What students complete

| Task | Marks | Suggested minutes |
|---|---:|---:|
| Inspect raw data: preview, dimensions, missing cells, repeated IDs | 10 | 15 |
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
