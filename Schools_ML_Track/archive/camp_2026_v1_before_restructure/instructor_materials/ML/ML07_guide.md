# ML07 Instructor guide

Read the matching student sheet first. Prerequisite: ML06 Reusable functions and a first check.

Learning objective: Build a small DataFrame, identify rows/columns and round-trip it through CSV.

## Explain and demonstrate

Use the student definition, then type or perform the worked example slowly. Ask learners to predict the result before you run it. Explain punctuation and units aloud. Do not add a new library or formula unless its purpose and inputs are demonstrated. Ask each of the five students to change one value and explain what changed.

Correct worked result: Three rows and two columns; shape is (3, 2). my_sales.csv contains headers and three records.

Specific repair cue: FileNotFoundError means the file is not at that path. Look in the notebook folder. ModuleNotFoundError requires the prepared environment; do not install random packages.

## Independent task reference

import pandas as pd
prices = pd.DataFrame({"item": ["Book", "Pen"], "price_ugx": [3000, 1000]})
prices.to_csv("prices.csv", index=False)
print(pd.read_csv("prices.csv"))

## Questions to ask

- What information goes in and what should come out of this particular example?
- Which result would convince you the task is correct?
- What does the example not tell us?

Use the task reference to evaluate their reasoning. If a learner cannot explain the basic operation, repeat the tiny example with different values before assigning the main task. For students who finish early, ask for an edge case or a limitation; do not introduce next week's syntax to the whole group.

## Evidence and feedback

Record complete, needs repair or absent for each learner. Give one concrete repair action. During a five-student class allocate a short individual check to every learner, not only volunteers. Keep instructor answers private. For SQL and numerical work use reference_values.json and the reference scripts. Short explanations and live demonstrations still require instructor judgement; do not describe them as fully auto-graded.

## Suggested three hour pacing

15 minutes retrieval and setup; 20 minutes first explanation; 25 minutes guided attempt; 20 minutes individual variation; 15 minutes away from screens; 20 minutes second demonstration or repair; 40 minutes independent task; 15 minutes feedback and saving; 10 minutes exit check. Total 180 minutes. If an idea takes longer, reduce the optional variation rather than skipping the explanation. Sessions 12 and 18 use most practice time for the checkpoint; sessions 19 to 24 use it for project mentoring and rehearsal.
