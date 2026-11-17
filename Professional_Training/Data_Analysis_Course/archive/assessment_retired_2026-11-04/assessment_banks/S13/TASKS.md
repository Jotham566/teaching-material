# S13 — sector investigation: numerical evidence

**DRAFT: component validation only. This is not a released assignment or a final-grade specification.** The assessment remains 30% of the independent track and 100 marks: Question 20, Analysis 40, Judgement 25, Communication 15. The checks below supply the Analysis component. The remaining 60 marks require calibrated reasoning and chart evidence before release.

Choose bank, machine or development. Use the matching fixed file in ../../data/sector_snapshots and read its README for provenance, units and limits. Compute the five findings below in your notebook; show the analysis and a relevant chart with a caption for each. Present the five numbered findings, limitations and recommendation in a concise accessible report. Marks concern the findings, not coding style. Do not replace missing values silently or infer causation from these comparisons.

Keep STUDENT_ID as your DA roster ID and COHORT="DA". Set SECTOR to your choice. Save a FINDINGS dictionary keyed by the question IDs; each item contains a numeric value and the exact published unit. Example structure (not an answer): `FINDINGS={"subscription_rate":{"value":0.0,"unit":"percent"}, ...}`. Prefer full precision; values rounded to two decimals are accepted. GDP accepts 1 USD rounding difference; the ending year must be exact. Each finding is worth 8 numerical marks. Fractions are not percentages, and a percentage-point difference is not a relative percentage change.

## bank

1. `subscription_rate` — What percentage of all campaign records have y=yes? Unit: `percent`.

2. `housing_rate_gap` — What is the subscription-rate difference: housing=yes minus housing=no? Each rate uses its own housing group denominator. Unit: `percentage points`.

3. `previous_success_rate` — Among records with poutcome=success, what percentage have y=yes? Unit: `percent`.

4. `subscribed_campaign_median` — What is the median campaign contact count among records with y=yes? Unit: `contacts`.

5. `subscribed_age_gap` — What is mean age among y=yes minus mean age among y=no? Unit: `years`.

## machine

1. `failure_rate` — What percentage of all observations have Machine failure=1? Unit: `percent`.

2. `type_rate_gap` — What is the failure-rate difference: Type H minus Type L, each with its own type denominator? Unit: `percentage points`.

3. `torque_gap` — What is mean Torque [Nm] among failed observations minus the mean among non-failed observations? Unit: `Nm`.

4. `no_failure_accuracy` — What percentage of all observations would an always-no-failure rule classify correctly? Unit: `percent`.

5. `failed_tool_wear_median` — What is median Tool wear [min] among observations with Machine failure=1? Unit: `minutes`.

## development

1. `latest_gdp` — What is Uganda GDP in current US dollars in 2023? Unit: `current USD`.

2. `window_change` — What is the percentage change in nominal current-USD GDP from 2000 to 2023, using 2000 as denominator? Unit: `percent`.

3. `change_2020` — What is the percentage change from 2019 to 2020, using 2019 as denominator? Unit: `percent`.

4. `median_annual_change` — What is the median of the 23 consecutive-year percentage changes during 2000–2023? Unit: `percent`.

5. `largest_increase_year` — Which ending year has the largest consecutive-year percentage increase in current-USD GDP? Break an exact tie by earliest ending year. Unit: `year`.

## Submission and limits

Submit one notebook and one accessible PDF/DOCX report together. The numerical component checks values against the chosen snapshot; it cannot establish whether a recommendation is justified or a chart communicates well. Its 40-mark output must not be imported as a final 100-mark assessment. The S13 form stays closed until the full rubric and packet workflow pass release checks and actual dates are supplied.
