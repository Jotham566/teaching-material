# Teach before use — current IUEA sequence

Use this alongside the PowerPoint and its matching lecturer companion. These are teaching checkpoints, not extra graded tasks. A previously mentioned word is not proof that students can use it.

For each new idea: define it in everyday language, identify its notation, demonstrate a complete example, trace the result, and only then show the combined example. Do not skip the definition because the same term appeared in Week 1 or Week 2. Explain a student question directly; no partner activity is required.

| Week | Explanation before combined examples | Evidence shown in the slides |
|---|---|---|
| 3 | Values, numeric text, expressions, assignment and all seven arithmetic operators | Separate calculations, printed outputs, operation-order traces and an update trace |
| 3 | Booleans; ==, !=, >, >=, <, <=; colon and indentation | Comparison outputs and true/false paths through if |
| 3 | else, elif, and, or, not | Branch traces, boundary values, Boolean truth table and range check |
| 3 | def, parameters, calls, return, named arguments and None | One function call traced step by step; both paths through a zero guard |
| 3 | Lists, dictionaries, tuples and sets; len, index, methods, abs and max | Collection comparison, list creation and selection, signed error versus magnitude |
| 4 | for, current item, body, iteration and numeric updates | First print each item, then count items, then calculate a running total |
| 4 | while, test-before-body, update and termination | Count 0, 1, 2; test false at 3; explain a missing update without running an endless loop |
| 4 | range, continue, break and nested indentation | Stop-exclusive range, contrasting skip/exit examples and their traces |
| 4 | Dictionary keys and get; tuples/unpacking; sets/membership | Worked updates, fallback result, unpacked values and repeated-ID check |
| 4 | CSV, import, with/open/as, text conversion and named exceptions | Read a supplied file, then process records; trace conversion success and failure |
| 5 | pandas constructor, columns, Series, masks, groups and method chains | Build the small table; separate selection from summarising; hand-calculate group totals before groupby |
| 6 | Median including even counts; None identity; copies and duplicate rules | Ordered middle values, keep/skip trace, preserved original data |
| 6 | Plot objects, axes, bar categories and histogram bins | Labelled scatter example; group values versus interval counts; full loop before optional comprehension |
| 7 | Previously taught notebook/data handling and saving | Rehearsal only; no new syntax introduced during the test |
| 8 | Features/targets, rows/columns, arrays, model objects, fit and predict | Small numerical data, shape explanation, baseline and tree paths |
| 8 | Imputation and pipeline order; paired lists; absolute and squared error | Training-only fill trace, zip pairs, hand-calculated MAE/RMSE steps before combined code |
| 9 | Labels, outcomes, probability, threshold and separate counters | Boundary-inclusive threshold examples and a four-observation counter trace |
| 10 | Groups, leakage, folds, hyperparameters and spread | Train/validation separation and a three-turn validation table |
| 11 | Ratios, interactions, consistent transformations and scaling | Trace a new row; create and fit models on separate lines; numerical scaling example |
| 12 | Eligibility, tuple comparison, sorting keys and empty results | Ranked candidates, the meaning of passing a function, then the full selection example |
| 13 | Fresh session, working folder, relative path, README and dependencies | Defined path operations, run instructions and independent reproduction check |
| 14–15 | Previously taught modelling, evidence and explanation | Assessment/reference material; use the published requirements without introducing surprise tools |

CML3112 resumes Week 3 at slide 13. Its expanded route and exact ranges are in [Week 3 continuation](CML3112_Week3_Continuation.md). The continuation now spends more time on foundations; pause at an explicit slide if needed rather than assigning unexplained syntax as practice.

The updated PPTX files and guided notebooks share one content source. Use the current student ZIPs. The issued assignment notebooks, required function names, marks and autograding remain unchanged. CML3112 A3’s deadline remains **29 September 2026 at 11:00 Kampala**.

Python reference checks used the official [calculator and value tutorial](https://docs.python.org/3/tutorial/introduction.html), [control-flow tutorial](https://docs.python.org/3/tutorial/controlflow.html), [data-structure tutorial](https://docs.python.org/3/tutorial/datastructures.html) and [expression reference](https://docs.python.org/3/reference/expressions.html). The small teaching examples are original and their printed outputs are checked by execution.
