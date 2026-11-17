# ML18 Instructor guide

Read the matching student sheet first. Prerequisite: ML17 Mistakes overfitting and fair comparisons.

Learning objective: Produce an auditable train/validation/test comparison and explain the frozen final choice.

## Explain and demonstrate

Use the student definition, then type or perform the worked example slowly. Ask learners to predict the result before you run it. Explain punctuation and units aloud. Do not add a new library or formula unless its purpose and inputs are demonstrated. Ask each of the five students to change one value and explain what changed.

Correct worked result: 90 training, 30 validation and 30 final-test records from iris. A documented choice and separate validation/test results.

Specific repair cue: If final-test results influenced depth choice, mark them as validation and use the instructor-provided alternate holdout for reassessment.

## Independent task reference

Reference implementation is in instructor_materials. Full credit depends on correct separation and explanation, not reaching a particular accuracy.

## Questions to ask

- What information goes in and what should come out of this particular example?
- Which result would convince you the task is correct?
- What does the example not tell us?

Use the task reference to evaluate their reasoning. If a learner cannot explain the basic operation, repeat the tiny example with different values before assigning the main task. For students who finish early, ask for an edge case or a limitation; do not introduce next week's syntax to the whole group.

## Evidence and feedback

Record complete, needs repair or absent for each learner. Give one concrete repair action. During a five-student class allocate a short individual check to every learner, not only volunteers. Keep instructor answers private. For SQL and numerical work use reference_values.json and the reference scripts. Short explanations and live demonstrations still require instructor judgement; do not describe them as fully auto-graded.

## Suggested three hour pacing

15 minutes retrieval and setup; 20 minutes first explanation; 25 minutes guided attempt; 20 minutes individual variation; 15 minutes away from screens; 20 minutes second demonstration or repair; 40 minutes independent task; 15 minutes feedback and saving; 10 minutes exit check. Total 180 minutes. If an idea takes longer, reduce the optional variation rather than skipping the explanation. Sessions 12 and 18 use most practice time for the checkpoint; sessions 19 to 24 use it for project mentoring and rehearsal.
