# Individual project marking rubric

The project contributes 30 points to the 100-point course total. The live demonstration is a separate 15-point component. This expands the existing weights; it does not create extra marks. Grade evidence and understanding, not visual polish, AI use, or a high model score.

For each two-point check: 2 = correct, reproducible and explained; 1 = relevant partial evidence with a specific fix needed; 0 = absent, incorrect or not reproducible. For the four one-point question checks, award 1 only when the evidence is present and correct. Record the file/cell/query supporting each mark and one repair action where needed.

## Question and data origin — 4 points

One point each: a narrow question; the intended reader/use; the named source with synthetic/teaching-data limits; and quantities/units or target/features that match the question. A question needing absent data receives no point for the unsupported measure, but can still earn the other points.

## Reproducible preparation — 6 points

- Raw data preserved, with the correct file path and schema: 0–2.
- Missing values, duplicates and types checked; cleaning decisions logged: 0–2.
- Notebook runs from a restarted kernel without hidden state: 0–2.

A justified “no changes needed” cleaning log can earn full marks. Do not reward unnecessary alterations to a clean dataset.

## Correct workflow — 8 points

ML, four checks at 0–2 each: training/validation/test roles and no leakage; baseline fitted only on training data; candidate model fitted on training data and chosen using validation evidence; final metric appropriate to the target and computed on the reserved final test. A model can earn full marks even if it does not beat the baseline, when the method and interpretation are correct.

DA, four checks at 0–2 each: Python calculations answer the stated questions; saved SQL filters/groups answer matching questions; any required join uses the stated keys without inflating rows; charts accurately display the calculated results with labels and units. Restrict requirements to the taught methods; no interactive dashboard or untaught library is required.

## Checks and honest limitations — 6 points

ML: one independently checked prediction/error (0–2); fair baseline/model comparison and inspected errors (0–2); a clear limitation of the data/model and cautious conclusion (0–2).

DA: reconciled row counts and totals (0–2); labelled agreement between SQL and pandas results, or a documented repair of a discrepancy (0–2); a supported finding and clear limitation without unsupported causal claims (0–2).

Use instructor_materials/reference_values.json for the supplied sales data. Do not transfer those sales totals to another approved dataset. Fixed worked examples check mechanics, not generalisation or understanding.

## Complete handover — 6 points

- Required files open and include executable notebook, report and the taught SQL evidence for DA: 0–2.
- The report ties the question to traceable results and a cautious conclusion: 0–2.
- Data dictionary/source instructions and assistance declaration are complete: 0–2.

Every learner includes AI_USE_LOG.md recording permitted supervised assistance or “No AI assistance used.” A declaration earns credit for transparent evidence, not for using AI. Apply AI_USE_POLICY.md if the learner cannot explain an element; do not infer misconduct from a style detector.

## Unaided demonstration — separate 15 points

Question and audience clarity: 0–3. Working demonstration or verified backup: 0–4. Explain one calculation/model decision and make a small instructor-selected modification without AI: 0–4. Explain a limitation and answer questions: 0–4.

For a four-point item: 4 = complete and correct independently; 3 = correct with a minor omission; 2 = partial understanding with prompts; 1 = an attempt with a substantial unresolved error; 0 = no demonstrated evidence. For clarity: 3 = clear question and audience, 2 = one unclear element, 1 = both require substantial prompting, 0 = absent. Do not grade accent or confidence as technical mastery.

Use the same difficulty of code change across learners. Examples: change a filter boundary and predict which rows remain (DA), or explain how a changed feature affects one prediction and rerun only that prediction (ML). Do not ask students to train a new model or use untaught syntax during a short demonstration.

## Record and return feedback

Record project marks as Q/4, P/6, W/8, C/6, H/6, total /30; keep demo /15 separate. Point to submitted evidence. Offer the repair arrangements already published in the programme policy; do not invent extra penalties or change weights after submission. Written and live evidence still needs instructor review until a calibrated assessment service is deployed.
