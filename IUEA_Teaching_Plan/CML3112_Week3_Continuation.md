# CML3112 Week 3 continuation

Use **CML3112_Week03_Design_Infrastructure.pptx**, starting at **slide 13**. Slides 1–12 contain the already taught material. CML3111 and CML3113 start their Week 3 decks at slide 1.

## Before the class

- Open Presenter View and the matching slide-by-slide lecturer companion.
- Open the refreshed CML3112_W03_student.zip and guided_practice.ipynb. The guided notebook is for demonstrations and revision, not submission.
- A3 remains due **29 September 2026 at 11:00 Kampala**. Students were told to read the final slides and complete it. Continuing the lesson does not reopen or extend the form.
- Keep Quiz 3 on its existing schedule; this material update does not reactivate it. A quiz availability window remains 24 hours from activation.

## Suggested 90-minute demonstration route

This is a pacing guide, not a requirement to rush. Show the complete example before advancing. No live partner tasks are required.

| Time | Slides | Lecturer explanation |
|---|---|---|
| 5 min | 13–14 | Recall the previous output: 7.0 and float. Explain parentheses and operation order. |
| 10 min | 15–18 | Name length, width, area and their units. Trace the calculation and explain the last line of an error message. |
| 15 min | 19–23 | Read each comparison aloud. Trace only the selected branch. Explain colon, indentation and elif before using them. |
| 25 min | 24–33 | Separate defining from calling. Point to the parameter, supplied argument, returned result and printed output. Demonstrate the zero-input guard. |
| 20 min | 34–43 | Explain the four collection types. Trace positions 0, 1 and 2. Explain abs, max and index before comparing errors. |
| 10 min | 44–49 | Demonstrate the revision answer. Connect units and percentage error to the published task without issuing a new assignment. |
| 5 min | 50–58 | Use the final assignment slides only to clarify previously issued requirements. A3 still closes 29 September at 11:00 Kampala. Do not announce an extension. |

## Explanations to keep ready

**Variable:** a name referring to a value. Assignment calculates the right side and gives its result to the name on the left.

**Function:** a named set of instructions. `def` stores the definition. Calling runs it with inputs. `return` sends a result back; `print` displays something. A function can return an answer without printing it.

**List:** an ordered collection. With `[98, 105, 92]`, index 0 retrieves 98. `len` is 3, but 3 is not a valid index here.

**Dictionary:** values found by keys, such as `record["reading"]`. **Tuple:** ordered positions that cannot be reassigned. **Set:** distinct items checked with `in`, with no positional index. Detailed operations follow in Week 4.

**Method:** an operation called through a value with a dot. `readings.index(105)` searches for 105 and returns its first position, 1. `readings[1]` instead retrieves the value at position 1.

**Signed error versus magnitude:** the sign tells direction. `abs(-8)` is 8, the size only. Find the position of the largest size, then retrieve the original reading and its signed error at that position.

## What students should revise afterwards

Repeat the worked examples individually in guided_practice.ipynb and compare outputs with the slides. Use the final optional video if helpful. Keep the already issued W03_student.ipynb separate. Do not submit the practice notebook or ZIP.

## Readiness for Week 4

Before moving on, learners should be able to explain a function input and return value, trace an if branch, and retrieve a list item by its index. Week 4 recaps lists, then teaches loops, dictionary records, tuples, sets and CSV reading in that order.
