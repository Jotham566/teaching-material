# CML3112 Week 3 continuation

Use **CML3112_Week03_Design_Infrastructure.pptx**, starting at **slide 13**. Slides 1–12 contain the already taught material. CML3111 and CML3113 start their Week 3 decks at slide 1.

## Before the class

- Open Presenter View and the matching slide-by-slide lecturer companion.
- Open the refreshed CML3112_W03_student.zip and guided_practice.ipynb. The guided notebook is for demonstrations and revision, not submission.
- A3 remains due **29 September 2026 at 11:00 Kampala**. Students were told to read the final slides and complete it. Continuing the lesson does not reopen or extend the form.
- Keep Quiz 3 on its existing schedule; this material update does not reactivate it. A quiz availability window remains 24 hours from activation.

## Teaching route for the expanded foundation sequence

These slide ranges refer to the explicit-foundations edition. Resume at slide 13. Each small step has its own slide so that students can revise it without guessing. Do not treat the increased slide count as a reason to move faster.

| Slides | Explain and demonstrate |
|---|---|
| 13–14 | Recall values and names; distinguish a typed instruction from its output. |
| 15–27 | All seven arithmetic operators, signs, powers, remainder, operation order, updates and numeric text. Run each tiny example and read the output. |
| 28–31 | Connect the already explained operations to the cohort formula and show how to read an error. |
| 32–44 | Boolean values and all six comparisons; trace if, if/else and if/elif/else on both matching and nonmatching values. Explain every colon and indentation level. |
| 45–48 | and, or and not; trace a range check and explain why a zero guard precedes division. |
| 49–62 | Define and call a function. Trace parameter values, return, named arguments, None and both paths through the zero guard. |
| 63–73 | Introduce collections and list positions; distinguish len from an index and a function from a method; then compare signed errors. |
| 74–79 | Read the worked revision answer and connect units to the issued assignment. |
| 80–89 | Previously issued task requirements, submission and quiz references, and optional revision video. |

**Pacing:** reserve roughly 35 minutes for arithmetic, 40 for conditions, 30 for functions and 25 for collections, plus a break and transitions. These are estimates, not a deadline to finish the deck. If time runs out, record the exact slide and continue the explanation next class; do not move an unexplained syntax topic into assessed practice.

**Already issued A3:** students were told to read the final slides and complete it. The deadline remains 29 September 2026 at 11:00 Kampala. This teaching revision does not change the issued assignment, marks or submission window. Use its final slides to clarify existing requirements, not to announce a new assignment or extension.

**Loops follow in Week 4:** for and while each receive a definition, complete example and trace table before record processing. Week 4 also demonstrates range, counters, continue, break and nested indentation. They are not prerequisites for the no-loop A3 examples.

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
