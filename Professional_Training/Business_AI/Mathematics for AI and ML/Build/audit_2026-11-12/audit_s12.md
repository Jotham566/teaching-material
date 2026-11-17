# Audit: Session 12, Optimisation in practice

Sources read: `Build/content/s12.py`, `Build/kit/diagrams_math_d.py` (n12, ridge_fit), `Class Slides PDF/12 - Optimisation in practice.pdf` (38 pages, all looked at), learner and solution notebooks (`Session 12 - Session 12 Optimisation in practice*.ipynb`), `Workbooks/Session 12 - Optimisation in practice.xlsx`. Slide references are PDF page numbers.

## Verdict
1. Every number is correct: the ridge sweep, the one-weight ridge, weight decay, the Lagrange example, the float limits, the softmax, LSE, the underflow table, the vanishing factors and clipping. The slides, notebook and workbook agree.
2. Flow is the weak point. The deck has two unrelated halves (regularisation with a Lagrange detour, then floating point, softmax, underflow, fp16, vanishing gradients and clipping), which is far more than 35 minutes. Softmax is introduced here cold, at the overflow case, and is introduced again in S14 and S17.
3. One methodological flaw: lambda is chosen on the same 20 "new points" that report the final error. Newcomer gaps: "badly conditioned", the degree-9 design matrix and Lagrange appear with little build-up.

## Findings

| ID | Where | Cat | Sev | What is wrong | Fix |
|---|---|---|---|---|---|
| 12-01 | p11, p28, p37, card p38 | 1/4 | Medium | Lambda is picked by the error on the 20 held-out points ("the best lambda is the one with the lowest error on held-out points"), and that same error (0.158) is then reported as the result. In practice this leaks the test set. The "best" is also only best among the six values tried: lambda 0.2 gives 0.1569, lower than 0.1584. | Call the 20 points a validation set and add one sentence: "In practice keep a third set, the test set, untouched until lambda is chosen." Title p11 "...lowest at lambda = 0.1 among the six values tried". |
| 12-02 | p7 to p37 | 2 | High | Too much for one 35-minute concept block, in two halves with no bridge: overfitting, ridge loss, the one-weight hand example, the closed form, the ridge sweep, weight decay, constraints (3 slides, Lagrange), then a statement slide, number formats, eˣ limits, stable softmax (2), LSE, underflow (2), 16-bit, vanishing (2) and clipping. That is 22 concept slides. A newcomer cannot absorb both halves, and the title has to join them with "and". | Cut the constraint/Lagrange block (p13 to p15) to one slide, or move it out. Move vanishing/exploding gradients and clipping (p25 to p27) to the end of S11, where the factor a(1 - a) was just computed. Add a bridge slide between the halves: "Part 1 kept the weights sensible; part 2 keeps the numbers inside the computer sensible". |
| 12-03 | p19 to p21 | 2/3 | Medium | Softmax is first defined here, directly on the overflow example (1000, 1001, 1002). There is no picture, no small hand example first and no "what softmax is for". The deck then mentions softmax(2, 1, 0.1) only in a note. S14 (p21) and S17 (p11 to p13) introduce softmax and "subtract the largest logit" again. | Add a short slide before p19: "softmax turns scores into probabilities that add to 1", worked on (2, 1, 0.1) = 0.659, 0.242, 0.099, with a bar picture. Then make S17 p13 a recall of S12 rather than a re-teach. |
| 12-04 | p10, p33 | 3 | Medium | "badly conditioned" is used as the reason for the huge weights and is never defined. The slide says the inverse "exists here but is badly conditioned, so the answer is unreliable". | Add a plain sentence: "Badly conditioned: tiny changes in y (or rounding) cause huge changes in w. Here XᵀX has a condition number of about 2 × 10⁷." |
| 12-05 | p7 to p8, p10 | 2/3 | Medium | The degree-9 polynomial, its ten weights w₀...w₉ and the design matrix with columns 1, x, ..., x⁹ are new ideas. They get one symbol-table row and no picture of a row of X. S4 fitted only a straight line. | Show one row of X with numbers (x = 0.333: 1, 0.333, 0.111, 0.037, ...) and say "a line uses two columns, a degree-9 curve uses ten". |
| 12-06 | p13 to p15 | 4 | Medium | The relevance of constraints/Lagrange to a newcomer building ML is thin. The notes concede "We will not do the full derivation", and the lab step is a 5-point table. The disc picture is the useful part. | Keep only p15 (the penalty as a circle) and fold the hand table into one line, or cut the block (see 12-02). |
| 12-07 | p15 | 3 | Low | The figure's "circle" w1² + w2² ≤ r² is drawn as a tall ellipse because the axes are not equal-aspect. | Draw with equal aspect so the circle looks round. |
| 12-08 | p34 | 3 | Low | "dropout" and "early stopping" are named without definition. | Add four words each: "dropout (randomly switching off units while training)", "early stopping (stop when the held-out loss rises)". |
| 12-09 | p8 / S10 / S11 | 2 | Low | The ridge loss here is the SSE without 1/n. S10 used MSE and S11 used 1/2(ŷ - y)². The note says "There is no division by n", which is good, but lambda values are not comparable with libraries that use the mean. | Add: "Libraries often use the mean; then the same effect needs a lambda n times smaller." |
| 12-10 | p26 note | 1 | Low | "0.25^10, about one millionth, holds if each weight were 1": correct, but 0.25 is the upper bound of the sigmoid slope, so it is the best case for sigmoid layers. That deserves saying. | "...at best: real sigmoid slopes are below 0.25, so the gradient shrinks even faster." |
| 12-11 | Notebook cells 10, 16, 22, 29, 36 | 6 | Low | Every "CHANGE one thing" cell is pre-written, so the learner only runs it. In S10 and S11 the learner edits something. | Leave one value blank, e.g. `lam = None  # try 2`, or say "edit the number in this cell". |
| 12-12 | Notebook layout | 6 | Low | This notebook uses a different template from S10 and S11: Step 0, the check helper after the imports, no "KLAi | ..." header line, and checks inside the TODO cell. File names repeat the prefix, "Session 12 - Session 12 Optimisation in practice.ipynb" (the same for S13 to S15 in both folders). | Rename the files to "Session 12 - Optimisation in practice.ipynb" and align the header and check-cell pattern with S10 and S11. |
| 12-13 | Workbook Ridge D82, D96, D144 | 6 | Low | The expected answers are printed beside the gold cells ("Expected at lambda = 0.1: 1.5473"), so the Check sheet adds nothing. | Move the expected values to the Check sheet only. |
| 12-14 | Workbook Start here A10 | 6 | Low | "...or just Enter in Google Sheets (the file already holds it as an array formula)": in the learner file the gold block is empty, so this is confusing. | "In Google Sheets type the formula in the top-left gold cell and press Enter; it fills the block." |
| 12-15 | Facilitator lab_steps | 6 | Low | "the penalty sheet has the by-hand weights": the sheet is called "Small". | Rename it in the text. |
| 12-16 | p12 | 3 | Low | "Many libraries define a single decay number equal to 2 times lambda" is correct for PyTorch's SGD `weight_decay` (grad + wd·w). It is not true of AdamW, which the same slide mentions, where the decay is decoupled. | "In plain SGD libraries, weight_decay = 2 lambda; in AdamW the decay is applied as a separate shrink." |
| 12-17 | Notes; outcome note | 5 | Low | "Here is/are" (13 times), "just" (6), "simply", "Imagine we ask" (p15), "the quiet tricks", "Notice". The same stock lines as S10 and S11. | Vary or cut them. |
| 12-18 | Titles | 5 | Low | Colon titles: "Overfitting in one picture: ...", "A constraint in plain words: ...", "16-bit numbers: a saving that needs care", plus the shared templated table titles. | State the point without the colon frame. |
| 12-19 | p31, p32, p35 | 5 | Low | Decorative row icons in the check table. The gold "Subtract max" step on p35 is a justified highlight; "4 Ridge" on p31 marks nothing in particular. | Remove the icons and the p31 highlight. |

## Category 1 checks (Python, numpy)
```
data: rng(19), xtr = linspace(-1,1,10), ytr = [-0.65 -0.53 -0.55 -0.53 -0.06 -0.05 0.61 0.78 1.26 1.46] (matches the notebook and workbook)
cond(XᵀX) = 2.14e7
lambda : sum w² (no w0) | train RMSE | test RMSE
0      : 103,994       | 1.7e-14    | 0.6657     OK ("about 104,000")
0.001  : 3.3569        | 0.0890     | 0.1662     OK
0.01   : 2.4827        | 0.0908     | 0.1636     OK
0.1    : 1.5473        | 0.1092     | 0.1584     OK
1      : 0.6144        | 0.2181     | 0.2039     OK
10     : 0.1181        | 0.4549     | 0.4198     OK
finer grid: 0.05 0.1612, 0.2 0.1569 (lower than 0.1), 0.3 0.1594       -> 12-01
one weight: 28.5/14 = 2.0357, /15 = 1.9000, /28 = 1.0179, /154 = 0.1851 (shares 100, 93, 50, 9%)   OK
   (SSE + lambda w²: w = Σxy/(Σx² + lambda)  consistent)
weight decay: (1 - 2·0.1·0.5)·2 - 0.1·1 = 1.7 OK
line w1 + w2 = 2: min at (1, 1), loss 2; ∇f = (2, 2) = 2·(1, 1), multiplier 2 OK
exp(709) = 8.2e307, exp(710) = inf; float32: exp(88) = 1.65e38, exp(89) = inf; float16 max 65504,
   e^11 = 59874 (fits), e^12 = 162755 (inf)                            OK
float16: 1 + 0.0004 -> 1.0 (eps/2 = 0.000488)                          OK
softmax(1000,1001,1002) = 0.0900, 0.2447, 0.6652; sum of shifted exps 1.5032; LSE = 1002.4076;
   log-softmax -2.4076, -1.4076, -0.4076                               OK
softmax(2,1,0.1) = 0.6590, 0.2424, 0.0986                              OK
0.1^323 = 9.88e-324 (subnormal), 0.1^324 = 0; n·ln0.1: -23.026, -230.26, -690.78, -743.73, -746.04, -921.03 OK
0.25^k: 0.25, 0.015625, 0.000977, 9.54e-7; 1.8^k: 1.8, 5.832, 18.90, 357.0   OK
clip (30, 40), c = 5 -> (3, 4)                                          OK
Citations: AdamW (Loshchilov and Hutter, arXiv 2017) OK; mixed precision (Micikevicius et al. 2017) OK
```

## Cross-session notes
- Assumes from earlier sessions: the L2 norm (S2), inverse and normal equation (S4), partial derivatives and gradient (S8, for Lagrange), the update rule (S10), the sigmoid slope ≤ 0.25 (S11, asserted there but not derived; see audit_s11 11-02).
- Not taught before and introduced thinly: softmax (12-03), logits, polynomial features and the design matrix (12-05), conditioning (12-04), Lagrange multipliers.
- Duplication to resolve: the stable softmax and "subtract the max" appear in S12 (p19 to p21), S14 (p21, softmax with temperature) and S17 (p11 to p13, softmax and "subtract the largest logit first"). Decide where softmax is taught (S12 or S17) and make the others recall it. Log-sum-exp and "add logs, do not multiply" also repeat S1 (p13 to p14) and S16 (p7). S12 should recall S1 explicitly ("in Session 1 you saw the sum of logs; here is why computers need it").
- Should hand forward: weight decay to S16 (Gaussian prior as an L2 penalty, which matches this deck's lambda once 2λ/σ² scaling is stated); log-softmax to S17 cross-entropy (the note on p21 does this); vanishing gradients and residual connections to S18 attention/transformers.
- Loss-scale conventions differ across S10 (MSE), S11 (1/2 SE) and S12 (SSE plus λ). See audit_s10.
