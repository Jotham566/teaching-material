# Audit: Session 10, Gradient descent

Sources read: `Build/content/s10.py`, `Build/kit/diagrams_math_d.py` (n10), `Class Slides PDF/10 - Gradient descent.pdf` (35 pages, all looked at), learner and solution notebooks, `Workbooks/Session 10 - Gradient descent for a line fit.xlsx` (formulas via openpyxl). Slide references are PDF page numbers.

## Verdict
1. Every worked number is correct: I recomputed all of them (bowl steps, line-fit gradient, 30-step losses for four rates, Adam table, momentum, the schedule) and the slides, notebook and workbook all agree.
2. The order is mostly sound (picture, rule, hand table, line fit, learning rate, batches, momentum, Adam, convexity, schedules). The 35-minute concept block is overloaded (22 concept slides), and the "why centre x" idea is promised but never explained on a slide.
3. Main weaknesses: the lab hands the learner the whole loop although the slides say they will write it; forward/backward pass and cross-entropy appear on the AI slide before they are taught; the notes and table titles are templated in the same way as S11 and S12.

## Findings

| ID | Where | Cat | Sev | What is wrong | Fix |
|---|---|---|---|---|---|
| 10-01 | p27 notes; notebook Step 4 | 6 | Medium | The notes say "In the lab you will wrap this loop in a function, call it for four learning rates", and outcome 3 says "Fit a line with gradient descent in Python". But notebook cell 19 gives `gradient_descent()` fully written. The learner only fills one-liners (the mean, loss0/dw0/db0, w1/b1, the last losses, polyfit). | Make the loop body a TODO (keep the `def` line and the `losses.append`, blank out the 4 update lines with a hint in words), or change the slide note to "read and run the loop". |
| 10-02 | p10 notes; p25 | 2/3 | Medium | Centring x is used from p10 on. The notes say "Why do we subtract the average distance? We come back to that in the lab." No slide ever explains it, and the lab only asks "Why do the centred distances run from -3.5 to +3.5?". A reader of the PDF learns only "as the lab does" (p25). | Add one line to p10 or p25: "Centring makes the two slopes independent: dL/dw no longer depends on b, so one eta suits both (here eta must stay below 0.19 for w and below 1 for b; uncentred, below 0.038)." Numbers are in the check below. |
| 10-03 | p32 | 2/3 | Medium | The AI slide's loop uses "Forward pass", "Backward pass: the gradient", "Loss: cross-entropy", "token". Forward/backward pass is taught in S11 and cross-entropy in S17, and none of them is defined here. | Add a caption: "Forward and backward pass: Session 11. Cross-entropy, the loss for next-token prediction: Session 17." Or replace "cross-entropy" with "loss: how wrong the next-word probabilities were". |
| 10-04 | p7 to p24 | 2 | Medium | Too much for 35 minutes: the update rule, two hand tables, the line-fit gradient, learning rates (2 slides), batches (2), momentum (2), Adam (3), convexity, schedules (2), mistakes and a compare slide. Adam's bias correction and the cosine formula are the least needed by a newcomer. | Move "Warm-up followed by cosine decay" (p24) and the Adam part 1 correction detail into an optional/appendix slide. Keep Adam as the update plus its hand table. |
| 10-05 | p19 | 3 | Low | β₁ᵗ (a power) is a new kind of superscript right next to subscripts m_t, v_t. The slide names t "the step number" but never says that β₁ᵗ means β₁ raised to the power t. | Add to the t row: "β₁ᵗ is β₁ to the power t: 0.9, 0.81, 0.729 for t = 1, 2, 3". |
| 10-06 | p21 | 3 | Low | The "Step" column shows -0.1000 while w rises from 0 to 0.1. A newcomer reads "step -0.1" as "w goes down". | Rename the header "Amount subtracted (alpha × m-hat / sqrt(v-hat))", or show "+0.1000 (w moves right)". |
| 10-07 | p9, p21 | 3 | Low | "These are illustrative numbers" appears under exact, computed tables. The guide reserves "illustrative" for made-up data, so the label suggests the numbers are approximate. | Drop the label from p9 and p21. Keep it only for the made-up trip data (p10). |
| 10-08 | p11 | 3 | Low | The symbol column writes "dL/dw" while the formula above it uses ∂L/∂w. The "sum" row shows only -44.10, though there are two sums. | Write "∂L/∂w (partial derivative, Session 8)". Split the row: "sum of error × x = -44.10; sum of errors = -54.4". |
| 10-09 | p8 note | 3 | Low | "The minus sign sends w downhill": w moves to the right (up). It is the loss that goes downhill. | "The minus sign moves w the way that lowers the loss." |
| 10-10 | p24 notes | 1 | Low | The notes put the transformer paper's 4000 warm-up steps next to the cosine schedule. That paper used warm-up then inverse-square-root decay, not cosine. The slide's wording is not false, but the pairing misleads. | Add "(followed by a decay proportional to 1/sqrt(step), not cosine)". |
| 10-11 | p25 | 4 | Low | "Centre and scale the inputs, as the lab does": the lab only centres. | "Centre (and, with several inputs, scale) the inputs; the lab centres the distance." |
| 10-12 | p30 | 6 | Low | The check table omits the eta = 0.05 result (0.1650), which the notebook and workbook both check. | Add a row: "Loss after 30 steps, eta = 0.05: 0.1650". |
| 10-13 | p29 vs notebook | 6 | Low | The slide says "five stages". The notebook has 7 steps (Step 6 least squares and Step 7 "which curve grew" are extra). | Say "five stages (the notebook splits them into seven steps)", or merge Steps 6 and 7 into Step 5. |
| 10-14 | Notebook Step 1, Workbook Data!F3 | 6 | Low | The learner's `mean_distance` and Data!F3 are checked but not used: `xc = x - x.mean()` and Data!D3 `=B3-AVERAGE(...)` compute the mean again. A wrong answer does not propagate, so the step teaches nothing. | Use `xc = x - mean_distance` and `=B3-$F$3`. |
| 10-15 | Workbook Check rows 11 to 13 | 6 | Low | The losses for eta 0.01, 0.05 and 0.2 come from blocks that are fully given, so 3 of the 13 checks pass with no learner work. | Either make the learner fill row 7 of one more block, or label these rows "(given: read only)". |
| 10-16 | Notes throughout | 5 | Low | Templated openers and closers shared with S11 and S12: "Four mistakes to watch for." "Use this table as your checkpoint." "Four things you may meet." "A hands-on check." "Three questions to finish." "Read the last line of any message first." Also "Here is/are" (7 times), "Notice" (3), "the heart of training", "Think of a ball rolling down" (p17), "simply", "just". | Vary or cut the stock openers. Remove "Think of", "the heart of", "simply" and "just". |
| 10-17 | Titles | 5 | Low | "X: Y" titles are heavy: "Adam, part 1: ...", "Adam, part 2: ...", "Convexity in plain words: ...". The table titles are identical across S10 to S12 ("Four mistakes with ..., what you see, and the fix", "The lab in five stages, in Python and in the spreadsheet"). | Rewrite the titles to state each slide's own point, e.g. "Adam keeps two running averages and corrects them at the start". |
| 10-18 | p30, p25, p31 | 5 | Low | Row icons (chart, calculator, pin, check, clock, cross, flag) in the check table are decorative and mark nothing. | Remove them (`icons=False`), as on the other tables. |

## Category 1 checks (Python, numpy)
```
x = 1..8, y = [3.2 4.1 5.4 5.9 7.6 8.0 9.9 10.3], xc = x - 4.5
loss0 = mean(y^2) = 52.11                     slide 52.11  OK
sum(xc*y) = 44.10, sum(y) = 54.4
dL/dw0 = -2/8*44.10 = -11.025, dL/db0 = -13.600   OK
w1 = 1.1025, b1 = 1.3600 (eta 0.1)          OK
30 steps: eta 0.01 -> 13.8482; 0.05 -> 0.16497; 0.1 -> 0.081946; 0.2 -> 1762.46   OK
least squares (polyfit): w = 1.05, b = 6.80, loss 0.081875   OK (GD 0.0819)
stability: w needs eta < 1/mean(xc^2) = 0.1905 ("about 0.19") OK; b needs eta < 1
uncentred x: largest stable eta = 0.038; with eta 0.05, 0.1, 0.2 the loss explodes (answer key "slow or unstable") OK
bowl L=(w-3)^2, eta 0.1: 0, 0.6, 1.08, 1.464, 1.7712, 2.017 (gap x0.8 each step = "one fifth") OK
eta 0.01: 0.06 .. 0.2882, loss 7.354; eta 1.1: 6.6, -1.32, 8.184, -3.2208, 10.465, loss 55.726 OK
eta 1.0: w -> 6 - w, bounces 0, 6 OK
momentum u = 2, 3.8, 5.42, limit 2/(1-0.9) = 20 OK
Adam (alpha 0.1): t1 g -6, m -0.6, v 0.036, m-hat -6, sqrt(v-hat) 6, w 0.1000
                  t2 g -5.8, m -1.12, v 0.069604, m-hat -5.8947, sqrt 5.9008, w 0.19990
                  t3 g -5.6002, m -1.56802, v 0.10090, m-hat -5.7861, sqrt 5.8022, w 0.29962 OK
schedule: t=50 0.0005, t=100 0.001, t=550 0.0005, t=1000 0.0 OK
exit: 1 - 0.1*(-4) = 1.4 OK; recall 6(3x+1) OK
```

## Cross-session notes
- Assumes from earlier sessions: Σ (S1), ∂ and ∇ (S8, recalled on p8 and p11), the chain rule (S9), least squares (S4: the slides call it "Session 4", but S4 used other data. Say "the least squares method of Session 4, on these eight trips").
- Used before it is taught: forward/backward pass (S11), cross-entropy and token (S17, S13). See 10-03.
- Loss conventions drift: S10 uses MSE with 1/n, S11 uses 1/2 (ŷ - y)², S12 uses SSE without 1/n. Each session states its own form, but no slide puts them side by side. One "same minimum, different scale" slide in S11 or S12 would stop learners comparing gradients across sessions by mistake.
- Should hand to S11: the update rule (used), eta too large (S11 Step 6 uses it). To S12: weight decay builds on the update rule. To S16: Adam and weight decay link to MAP. The forward link on p35 ("Next session") is good.
- Datasets change every session (S4 spend/sales, S8 four deliveries, S10 eight boda trips). That is acceptable, but S10 could note that the S8 gradient idea is now reused on new data.
