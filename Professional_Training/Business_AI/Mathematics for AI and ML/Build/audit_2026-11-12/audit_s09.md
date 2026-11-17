# Audit: Session 9, The chain rule and the Jacobian

Sources read: `Build/content/s09.py`, `Class Slides PDF/09 - The chain rule and the Jacobian.pdf` (all 32 pages viewed), the learner notebook and the solution notebook (both executed: the solution gives "All 15 checks pass"; the learner version gives 0 of 13 and one cell raises TypeError until it is filled in), and `Workbooks/Session 09 - The chain rule and the Jacobian.xlsx` (formulas read).

## Verdict (3 lines)
The calculations are correct: 42, 14.778, 1, 150, -3, the backward values -6, -18 and the row slopes -4, -12, -18, -40 with mean -18.5, J = [[3, 2], [1, 6]], Jᵀ(11, 6) = (39, 58), and the CHANGE answer (12, 13). The Llama 3 layer counts (32 and 80) match the published paper.
The chain rule and the computation graph are taught very well. The Jacobian-transpose backward step is the weak point for a newcomer. It brings in subscripted ∇ notation and a column-vector convention, and it states "multiply by Jᵀ" without saying why.
The labs mostly match the slides. The workbook's CHANGE points at the wrong cell, and the learner notebook prints the nudged answers before the learner predicts.

## Findings

| ID | Where | Cat | Sev | What is wrong | Fix |
|---|---|---|---|---|---|
| 9-1 | Slide 21 "∇ₓ s = Jᵀ ∇₍ᵤ,ᵥ₎ s" | 3 | High | It is the hardest slide in the session and it is too compressed for a newcomer. ∇ with a subscript is never explained, the gradient is now a column (in Session 8 it was a row tuple), and why it is the transpose is not shown on the slide. A learner revising from the PDF sees a rule, not a reason. | Insert one slide before it: "ds/dx₁ = ds/du · du/dx₁ + ds/dv · dv/dx₁ (two paths, add them)", worked as 11·3 + 6·1 = 39. Then show that this pattern is "column 1 of J dotted with (11, 6)", that is Jᵀ times the column. Define ∇ₓ s as "the gradient of s with respect to the inputs x". |
| 9-2 | Slides 3 to 7 and the "Many steps" slide 22 | 2 | Medium | The deck never states the multi-path rule ("when a value feeds several boxes, add the slopes along each path"). Slide 21 relies on it silently, and Session 11 (a network with several weights) needs it. | Add the sum-over-paths rule as a picture with two arrows meeting (it can be the same slide as 9-1). |
| 9-3 | Slide 10 (finite-difference table), row h = 0.001 | 1 | Medium | y(2.001) is printed as "49.042" (`.6g`) next to the slope 42.0090. From the shown value, (49.042 - 49)/0.001 = 42.000. The true value is 49.042009. This is the same defect as 7-1. | Print 49.042009 (7 or more significant figures). |
| 9-4 | Slide 29 "Libraries run the chain rule for you" | 3, 4 | Medium | The drawn figure is the Session 8 list ∂L/∂θ₁ ... ∂L/∂θ_N (θ undefined, see 8-2). It does not show what the title says, which is recording a graph and running it backwards. | Draw the tiny graph w → p → L with "recorded during forward" and "replayed backward" labels, and mention `loss.backward()` / `jax.grad` by name in the caption. |
| 9-5 | Workbook Chain!A21 "CHANGE ... set the inner function to 5x by editing B8 and the formulas for u" | 6 | Medium | B8 is example 1's inner slope (3, for 3x + 1). The 5x change belongs to example 2 (e^{2x}), whose u is B15 and inner slope B17. A learner who follows this edits the wrong example, and Check!B5 and B6 go NOT YET. | Change it to "edit B15 to =5*B14 and B17 to 5; predict 5e^5 = 742.07". |
| 9-6 | Learner notebook cells 6, 14, 22 and 26 | 6 | Medium | The nudged answers (42.0, -18.0, the Jacobian [[3, 2], [1, 6]] and (39, 58)) are printed from given code **before** the learner fills in the gold cell, so PREDICT is spoiled. | Move each nudged check into a cell after the TODO, or compute it only `if chain is not None`. |
| 9-7 | Learner notebook cell 10 | 6 | Low | `round(chain_exp, 3)` raises TypeError while `chain_exp` is None, so the two checks in that cell never run. | Use `print('chain rule slope:', chain_exp)` or guard it. |
| 9-8 | Slide 11 "Three more chain rule examples" | 3 | Low | Row 1 is the same function as the slides before (now at x = 1), so there are only two new examples. | Retitle "The chain rule on three functions at x = 1", or swap row 1 for the sigmoid-like 1/(1 + e^{-x}), which helps Session 11. |
| 9-9 | Slide 18 note "Row 1: du/dx1 ... Row 2: dv/dx1" vs the ∂ symbols in the formula and on slide 19 | 3 | Low | The same partials are written with d and with ∂ on adjacent slides. | Use ∂ throughout the Jacobian slides. |
| 9-10 | Slide 28 title "the chain rule is used once for every layer" vs notes "through every step inside each layer" | 4 | Low | The title understates it: the chain rule is applied at every operation inside each layer (attention, normalisation, MLP), not once per layer. | Title: "the chain rule runs backwards through every layer, and every step inside it". The Llama 3 caption (32 and 80 layers, 2024 paper) is correct and within the facts discipline. |
| 9-11 | Slide 21 note "This one line is the backward step of every layer of a neural network" | 4 | Low | Slight overclaim: libraries compute vector-Jacobian products, often without forming Jᵀ. Slide 29 says this correctly. | Say "This is the backward step of a layer, written with a matrix; libraries compute the same product without building J." |
| 9-12 | Slide 17 picture (square to parallelogram) | 3 | Low | It does not say that the sides are h times the columns of J, or that the picture is local. The caption "A very small square becomes almost a parallelogram with the columns of J as sides" is fine for an expert but sounds as if the output side equals (3, 1). | Say "...with sides h × (3, 1) and h × (2, 6), where h is the tiny step". |
| 9-13 | Notes | 5 | Low | 8 of 31 notes open with "Here is/are". The phrasings "That is the whole idea of backpropagation" and "Never trust a derivative you have not checked" are slogans that repeat the slide, and 14 notes end with a question. | Trim the slogans and vary the openers. |
| 9-14 | Workbook Check (22 checks) vs notebook (15 checks) | 6 | Low | Same content, different counts. That is fine, but the facilitator prep text says only "All checks pass". | No change, or state both counts in the prep. |

### Python check (category 1)
```
y=(3x+1)^2 at 2: FD h=1,0.1,0.01,0.001 -> 51.0, 42.9, 42.09, 42.009; y(2.001)=49.042009 (slide shows 49.042)
e^{2x} at 1: 2e^2 = 14.7781; ln(x^2+1) at 1: 1.0
tiny graph: p=3, L=9, dL/dp=-6, dL/dw=-18; L(1.001)=8.982009, L(0.999)=9.018009 -> CD -18
rows dL/dw = [-4, -12, -18, -40], mean -18.5
J at (2,3) = [[3,2],[1,6]]; J^T (11,6) = (39, 58); direct CD of s = x1^2 x2 + x1 x2^3 -> 39.000, 58.000
CHANGE (1,2): J = [[2,1],[1,4]], grad s = J^T (5,2) = (12, 13)
nudge x2 3 -> 3.001: dv = 0.006001 OK
exit: (2x+5)^3 at 0 -> 3*25*2 = 150; 2*(-3)*0.5 = -3; J of (2x1, x1+x2) = [[2,0],[1,1]]
```

### Labs
The notebook (6 steps, 15 checks) and the workbook (Chain, Backward, Jacobian, 22 checks) teach the same numbers as the slides, and the Check sheet expectations are correct. The faults are 9-5, 9-6 and 9-7.

## Cross-session notes
- **Assumes, taught:** the transpose and the @ operator (Session 3), the gradient (Session 8), the central difference (Session 7) and the rules for e^x and ln x (Session 7).
- **Assumes, not taught:** ∇ with a subscript, the gradient as a column vector, θ (in the reused figure), and the sum-over-paths form of the chain rule.
- **Hands on:** -18 / -18.5 (consistent with Sessions 7 and 8), J = [[3, 2], [1, 6]] and "multiply by Jᵀ".
- **Should hand on (missing for Session 11):** (a) the derivative of the sigmoid via the chain rule; (b) the multi-path add rule; (c) for a layer z = W x, the local slope with respect to W is the input x, so ∂L/∂W = δ xᵀ (an outer product). Session 11 should either teach (c) or Session 9 should preview it.
