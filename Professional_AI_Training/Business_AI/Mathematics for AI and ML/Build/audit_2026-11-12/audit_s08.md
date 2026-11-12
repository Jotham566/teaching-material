# Audit: Session 8, Partial derivatives and the gradient

Sources read: `Build/content/s08.py`, `Class Slides PDF/08 - Partial derivatives and the gradient.pdf` (all 30 pages viewed; slide 9 zoomed), the learner notebook and the solution notebook (both executed: the solution gives "All 9 checks pass"; the learner version gives 0 of 7 and three cells raise errors until they are filled in), and `Workbooks/Session 08 - Partial derivatives and the gradient.xlsx` (formulas read).

## Verdict (3 lines)
The numbers are all correct. (-18.5, -6.5), length 19.61, 19.4 degrees, L(1.9, 1) = 0.175, the zero gradient at (1.9, 1) and the 0.25 tie on the grid all recompute.
The build from Session 7's one-parameter loss works well. Two pictures get in the way of a newcomer: the contour map's labels sit on the far side from the start point, and the "N parameters" figure uses θ without ever defining it.
Two things do not hold together. The lab's "steepest direction in degrees" step uses trigonometry the course never taught, and the deck says learners "found" this line in Session 4, which used different data.

## Findings

| ID | Where | Cat | Sev | What is wrong | Fix |
|---|---|---|---|---|---|
| 8-1 | Slides 9 and 16 (contour map of L(w, b)) | 3 | Medium | The level labels 1, 3, 10, 20 appear only on the right-hand branches. The start dot (1, 0) sits among unlabelled left-hand curves, so it looks as if it lies to the left of the "1" curve, while the text says "between the curves 10 and 20". No closed loop is visible around the best point, so the "centre of the map" cannot be seen. | Label the contours on both branches, or put the level label right next to the start. Widen the window (e.g. w from -1 to 4.5, b from -3 to 5) so that at least the 1 and 3 ellipses close around (1.9, 1). |
| 8-2 | Slide 20 figure (∂L/∂θ₁ ... ∂L/∂θ_N), reused in Session 9 slide 29 | 3 | Medium | θ is never defined in Sessions 1 to 8, and the only earlier θ (Session 2) means an **angle**. A newcomer reading the PDF cannot decode θ₁. | Either define θ in a caption ("θ₁ ... θ_N: the N parameters; machine learning papers often call parameters θ") or draw ∂L/∂w, ∂L/∂b, ... instead. |
| 8-3 | Slide 17 "This is the least-squares line from Session 4"; notes "the least-squares line you found in Session 4" | 2 | Medium | Session 4 fitted advertising data (7 rows), not these deliveries, so the learner never found (1.9, 1). The underlying claim is true: the normal equation on this data gives b = 1, w = 1.9. | Say: "It is the line the Session 4 normal equation gives for these four deliveries: XᵀX = [[4, 10], [10, 30]], Xᵀy = (23, 67), so (b, w) = (1, 1.9)." |
| 8-4 | Check table "Steepest downhill direction ... 19.4 degrees"; notebook Step 6 (cos, sin, radians, arctan2); workbook Gradient!B30 (ATAN2, DEGREES) | 2, 3 | Medium | Angles and inverse tangent are not taught anywhere before this, and the entry level is algebra only. Step 6 PREDICT asks for "the angle of a right triangle with sides 18.5 and 6.5". No concept slide explains how the angle is found. | Either add one slide (direction as a unit vector, angle = arctan(6.5/18.5)) or replace the angle with a unit vector, (0.943, 0.331), which slide 13 already uses for (4, 6). Then check "the best of 360 directions is close to minus the gradient divided by its length". |
| 8-5 | Cover question "How does one step change all of them at once?" | 2 | Low | Session 8 does not take a step; the update rule is in Session 10. The question is not answered today. | Use "Which way should each of billions of numbers move to lower the loss?" or add a closing line: "the step itself is Session 10". |
| 8-6 | Slides 11 and 13: "∂ ... read 'partial' (also 'del')" and "∇f read grad f or del f" | 3 | Low | Two different symbols are both given the reading "del". | Read ∂ as "partial" and ∇ as "nabla" or "grad". Drop "del" from one of them. |
| 8-7 | Slides 14 (∂L/∂w) and 15, 17, 25 (dL/dw, dL/db) | 3 | Low | The notation switches between ∂ and d for the same partial derivative without warning. | Use ∂L/∂w consistently once two parameters exist, or add a footnote: "we write dL/dw in tables for short". |
| 8-8 | Slide 13 "length of nabla f ... square root of 4² + 6²" | 2 | Low | No link to the Session 2 L2 norm, which is exactly this. | Add "the L2 norm ‖∇f‖ from Session 2". |
| 8-9 | Slide 14 note "2/n comes from the power rule. Session 9 explains x_i and 1 (chain rule)" | 2 | Low | Same misattribution as 7-5: the 2 also comes through the chain rule. | Say "2/n, xᵢ and 1 all come from the chain rule (Session 9)". |
| 8-10 | Slide 18 drawn sheet (columns A-E, rows 1-4, w = 1 ... 2.5, b = 0 ... 1.5) vs slide 26 error card "Write w as B$3 and b as $A4" | 6 | Low | The workbook grid runs w = 0 ... 3.5 in B3:I3 and b = -1 ... 3 in A4:A12. The slide picture's letters and row numbers do not match the workbook, so the $ advice cannot be checked against it. | Draw the slide grid with the workbook's real addresses (header row 3, first b in row 4), or drop the letters and row numbers from the picture. |
| 8-11 | Slide 27 "Many training setups keep more bits than that" | 4 | Low | Vague. | Say "Published mixed-precision training keeps a 32-bit copy of the weights and optimiser state, so memory is several times larger." This is within the guide's allowed facts. |
| 8-12 | Lab answer key "CHANGE: start at (3, 0) → The gradient changes sign for w" | 1 | Low | At (3, 0) the gradient is (11.5, 3.5), so **both** entries change sign. | Say "both entries turn positive; downhill points left and down". |
| 8-13 | Lab answer key PREDICT "the errors are mostly negative" | 1 | Low | All four errors are negative (-2, -3, -3, -5). | Say "all four errors are negative". |
| 8-14 | Notes | 5 | Medium | 10 of 29 notes open with "Here is/are", 11 end on a question, "simply" appears 3 times, and there is a repeated "Two mistakes catch many people". | Vary the openers and cut "simply". |
| 8-15 | Learner notebook cells 20, 24 and 28 | 6 | Low | They raise TypeError when the earlier gold cells are empty (Zf of None, contour, -g0). | Guard them with `if Z is not None` and `if g0[0] is not None`. |
| 8-16 | Notebook Step 6 CHANGE "(Answer: left and down ...)" and workbook Grid!A18 "The true minimum 0.175 lies ... at w = 1.9 and b = 1" | 6 | Low | The answer is printed in the prompt, before the learner predicts. | Move it to the facilitator key. |
| 8-17 | "Where" section | 4 | Low | Only one "Where" slide plus the practice slide, and the practice title does not contain "Where". The Llama 3 sizes (8B, 70B) are published and correct. | Optional: add a second slide showing that a training step updates every entry of this gradient (it leads into Session 10). |

### Python check (category 1)
```
L(1,0) = 11.75; L(1.9,1) = 0.175; grad(1,0) = (-18.5, -6.5); grad(1.9,1) = (-2e-15, -7e-16)
|grad(1,0)| = 19.6087; angle of -grad = atan2(6.5, 18.5) = 19.359 deg
grid w 0..3.5, b -1..3 step 0.5: min 0.25 at (w=2, b=0.5) and (w=2, b=1)  [slide/workbook OK]
slide 18 grid values: [[11.75 4.375 0.75 0.875] [8.75 2.625 0.25 1.625] [6.25 1.375 0.25 2.875] [4.25 0.625 0.75 4.625]] OK
grad(3,0) = (11.5, 3.5)  -> both entries flip sign (answer key says only w)
f = x^2 + 3y^2: grad(2,1) = (4,6), |.| = 7.211, unit (0.555, 0.832) OK
normal equation on the delivery data: [[4,10],[10,30]] (b,w) = (23,67) -> (b, w) = (1, 1.9)
8e9 entries x 2 bytes = 16 GB OK
```

### Labs
The notebook (6 steps, 9 checks) and the workbook (Gradient and Grid, 14 checks) match the slides. The Grid sheet's $-anchoring instruction is correct for the workbook layout. The angle step is the weak point (see 8-4).

## Cross-session notes
- **Assumes, not taught:** trigonometry (angles, arctan, cos/sin in the notebook) and θ as the symbol for a parameter. Partly assumes the Session 4 normal equation on this data (see 8-3).
- **Assumes, taught:** the vector and L2 norm (Session 2, link not stated), the central difference (Session 7) and the power rule (Session 7).
- **Hands on:** the gradient (-18.5, -6.5) and the best line (1.9, 1). Sessions 9 and 10 use both consistently.
- **Should hand on:** the row versus column convention for a gradient. Session 9 multiplies Jᵀ by a gradient treated as a column, but Session 8 writes it as a row tuple. Also: a gradient for a model with a weight matrix, which Session 11 needs.
