# Audit: Session 7, Derivatives

Sources read: `Build/content/s07.py`, `Class Slides PDF/07 - Derivatives.pdf` (all 36 pages viewed), the learner notebook and the solution notebook (both executed: the solution gives "All 16 checks pass"; the learner version gives 0 of 15 and two cells raise TypeError until they are filled in), and `Workbooks/Session 07 - Derivatives.xlsx` (formulas read with openpyxl).

## Verdict (3 lines)
The maths is correct, and the ordering works well for a newcomer: slope of a line, tangent, secant to limit, rules, loss, sign of the slope, slope set to zero, finite-difference check. Every headline number recomputes exactly: 11.75, 0.75, 4.75, -18.5, -3.5, +11.5, 2.233, 0.342, 3e = 8.155, 0.75 and 2.367.
The real defects are small. One table shows a rounded f(3.001) that does not give the slope printed beside it. The claim about what h = 1e-12 does is false. One cross-reference to Session 4 promises something Session 4 never did. The step that sets the slope to zero skips its algebra.
The notes lean on a template: many open with "Here is" or "Now", and 14 of 35 end on a question. The labs match the slides closely.

## Findings

| ID | Where | Cat | Sev | What is wrong | Fix |
|---|---|---|---|---|---|
| 7-1 | Slide 10 (table "slopes settle on 6"), last row | 1 | Medium | The f(3 + h) column is printed with `.6g`, so h = 0.001 shows "9.006". A learner who checks (9.006 - 9)/0.001 gets 6.000, but the row prints 6.001. The true value is 9.006001. | Print f(3 + h) in full, e.g. `f'{sq(3+h):.7g}'` or a fixed 6 decimals, so the row reads 9.006001. |
| 7-2 | Slide 32 error table "Slope is 0.0 or full of noise / h is far too small, for example 1e-12"; lab answer key "CHANGE: use h = 1e-12 → Noise or 0.0"; notebook Step 2 CHANGE | 1, 6 | Medium | With h = 1e-12 the forward slope of x² at 3 is **6.0005**, which is neither 0.0 nor visibly noisy. A learner who does the CHANGE sees almost nothing happen and concludes the slide is wrong. You only get 0.0 at h = 1e-16. | Use h = 1e-15 (it gives 5.33, clearly wrong) or 1e-16 (it gives 0.0) in the CHANGE task, the error card and the answer key. Change the wording to "far from 6 or exactly 0". The workbook CHANGE (A12 = 1e-11) has the same problem. |
| 7-3 | Slide 24 note "This is the Session 4 least-squares answer for a line through the origin" | 2 | Medium | Session 4 used different data (advertising, 7 rows) and always fitted an intercept; it never did a line through the origin. A learner who looks back will not find this. | Change it to: "It is the Session 4 normal equation XᵀX w = Xᵀy with X a single column of distances: XᵀX = 30, Xᵀy = 67." |
| 7-4 | Slide 24 formula "dL/dw = 0 ⇒ w* = Σxᵢyᵢ / Σxᵢ²" | 3 | Medium | It jumps from the derivative straight to the answer. The middle step is only in the speaker notes, and a newcomer cannot rebuild it from the PDF. | Add one line: (2/n)(w Σxᵢ² - Σxᵢyᵢ) = 0, so w Σxᵢ² = Σxᵢyᵢ. |
| 7-5 | Slide 21 symbol table "The 2 comes from the power rule on the square" and "x_i appears because w is multiplied by x_i" | 2, 3 | Low | The derivative of (wxᵢ - yᵢ)² uses the chain rule, which comes in Session 9, but the slide calls it the power rule. The deferral is honest, but the attribution is wrong. | Say: "The 2 and the xᵢ both come from the chain rule (Session 9). Today we check the formula with numbers." |
| 7-6 | Slide 15 (product-rule rectangle) | 3 | Low | It uses df and dg to mean small changes, two slides after df/dx was defined as the derivative. A newcomer may read df as a derivative. | Label the strips Δf and Δg ("a small change in f") on this slide. |
| 7-7 | Slide 13 "With a constant inside, e to the 2x has slope 2 times e to the 2x" | 2 | Low | It states a chain-rule result before the chain rule, which is acceptable because Session 9 closes the loop. | Keep it; Session 9 slide 11 already refers back. No change needed. |
| 7-8 | Slide 26 caption "Professionals check every hand-derived derivative this way"; notes "People who build machine learning libraries run this check on every new derivative" | 4 | Low | Overclaim. Gradient checking is common practice but not universal. | Say "Library developers routinely test derivatives this way (gradient checking)." |
| 7-9 | Slide 11 note "Papers and library manuals use df/dx" | 3 | Low | Both notations are common in papers, and f′ is common too. | Say "You will meet both." |
| 7-10 | Slide 13 notes "This is why the exponential shows up everywhere in growth and in probabilities" | 4 | Low | Vague causal claim: being its own derivative is not why e^x appears in probabilities. | Say "This tidy rule is one reason e^x is convenient in growth models and in softmax (Session 17)." |
| 7-11 | Notes (speaker script) | 5 | Medium | 9 of 35 notes open with "Here is/are". Many others open "Now ...", 14 end on a question, and there is one "This is the key picture of the session". "Two mistakes catch almost everyone" is a template shared with Sessions 8 and 9. | Vary the openers: start from the content ("Start with...", "The table shows..."). Drop "the key picture". Keep the questions only where an answer is expected. |
| 7-12 | Deck structure (slides 25, 28, 31, 32, 35) | 5 | Low | The titles are word for word the same as in Sessions 8 and 9 ("Two mistakes to avoid...", "Read the recipe before you write it: ...", "Errors you will meet...", "The lab has four stages..."). | This is acceptable as navigation, but give the "Two mistakes" slide a content title, e.g. "Read the sign the right way, and do not assume a minimum". |
| 7-13 | Notebook Step 7 CHANGE and workbook Loss!A29 | 6 | Low | The CHANGE prompt prints the answer ("Answer: w goes up to 2.367"), which defeats predict-first. The same happens in Session 8 Step 6 and Session 9 Steps 4 and 6. | Move the answers to the facilitator key, or put them behind a "reveal" line after the prompt. |
| 7-14 | Learner notebook cells 28 and 33 | 6 | Low | If `dloss` or `w_star` is still None, the cells raise TypeError (float(None), None*float) instead of printing NOT YET. A newcomer sees a traceback. | Guard them with `if w_star is not None:` around the plot and the `round(float(...))` calls. |
| 7-15 | Workbook Check B21 (direction at w = 1 must equal "raise") | 6 | Low | Too strict: column E of the same sheet displays "raise w", so a learner who types "raise w" fails. | Accept both: `=IF(OR(B21="raise",B21="raise w"),"OK","NOT YET")`. |
| 7-16 | Workbook Check B20 "Slope at the best w is zero" | 6 | Low | Too loose: typing 0 in Loss!B25 passes without any formula. | Compare Loss!B25 with the SUMPRODUCT slope recomputed in the Check sheet from Loss!B23. |
| 7-17 | Facilitator misconception "Below about 1e-8 ... rounding noise dominates" | 1 | Low | For the forward difference at h = 1e-8 the error is about 4e-8. Noise only dominates from about 1e-13. | Say "Below about 1e-10 rounding error starts to grow, and by 1e-15 it swamps the answer." |

### Python check (category 1)
```
f(3+h) table: h=0.001 -> f = 9.006001, slope 6.001 (slide prints f as 9.006; (9.006-9)/0.001 = 6.000)
forward slope of x^2 at 3: h=1e-8 5.99999996, 1e-10 6.0000005, 1e-12 6.0005334, 1e-14 6.0396, 1e-15 5.3291, 1e-16 0.0
forward/central at h=1e-3: x^2 -> 6.001 / 6.000; e^x at 1 -> 2.71964 / 2.71828 (slide OK)
3e = 8.154845; quotient at 1 = 0.75
L(1), L(2), L(3) = 11.75, 0.75, 4.75; dL/dw at 1, 2, 3 = -18.5, -3.5, +11.5
w* = 67/30 = 2.2333; L(w*) = 0.34167; L(1.001) = 11.7315, FD = -18.4925 (slide: -18.49 OK)
CHANGE (last fee 10): w* = 71/30 = 2.3667
exit check: d/dx 5x^3 at 2 = 60
```

### Labs
The notebook (7 steps, 16 checks) and the workbook (Shrink, Rules, Loss, 18 checks) teach the same thing with the same numbers as the slides. Lab map, check table and sheet names all agree.

## Cross-session notes
- **Assumes:** ln and e from Session 1 (taught there); the Session 4 normal equation (taught, but see 7-3); the chain rule, used without proof in two places and flagged correctly as Session 9.
- **Hands on:** the delivery data (x = 1..4, y = 3, 5, 6, 9), L(1) = 11.75 and dL/dw(1) = -18.5. Sessions 8 and 9 reuse them consistently.
- **Should hand on (missing):** (a) a one-line preview of why e^x and ln matter for the sigmoid (Session 11) and softmax/cross-entropy (Session 17); (b) the habit "check gradients with a central difference", which is carried forward well.
