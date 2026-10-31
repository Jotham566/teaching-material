# DA16 Instructor guide

Read the matching student sheet first. Prerequisite: DA15 SQL totals and groups.

Learning objective: Join on a key, check row counts and explain how duplicate keys could inflate revenue.

## Explain and demonstrate

Use the student definition, then type or perform the worked example slowly. Ask learners to predict the result before you run it. Explain punctuation and units aloud. Do not add a new library or formula unless its purpose and inputs are demonstrated. Ask each of the five students to change one value and explain what changed.

Correct worked result: 60 joined rows, one per sale, with a category from the product table.

Specific repair cue: Check unique keys before joining. If the count increases above 60, investigate duplicate product keys instead of accepting the larger total.

## Independent task reference

SELECT p.category, SUM(s.units * s.unit_price_ugx) AS revenue_ugx FROM sales AS s LEFT JOIN products AS p ON s.item = p.item GROUP BY p.category ORDER BY p.category;

## Questions to ask

- What information goes in and what should come out of this particular example?
- Which result would convince you the task is correct?
- What does the example not tell us?

Use the task reference to evaluate their reasoning. If a learner cannot explain the basic operation, repeat the tiny example with different values before assigning the main task. For students who finish early, ask for an edge case or a limitation; do not introduce next week's syntax to the whole group.

## Evidence and feedback

Record complete, needs repair or absent for each learner. Give one concrete repair action. During a five-student class allocate a short individual check to every learner, not only volunteers. Keep instructor answers private. For SQL and numerical work use reference_values.json and the reference scripts. Short explanations and live demonstrations still require instructor judgement; do not describe them as fully auto-graded.

## Suggested three hour pacing

15 minutes retrieval and setup; 20 minutes first explanation; 25 minutes guided attempt; 20 minutes individual variation; 15 minutes away from screens; 20 minutes second demonstration or repair; 40 minutes independent task; 15 minutes feedback and saving; 10 minutes exit check. Total 180 minutes. If an idea takes longer, reduce the optional variation rather than skipping the explanation. Sessions 12 and 18 use most practice time for the checkpoint; sessions 19 to 24 use it for project mentoring and rehearsal.
