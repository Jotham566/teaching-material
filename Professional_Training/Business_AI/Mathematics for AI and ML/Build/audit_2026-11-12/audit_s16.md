# Audit: Session 16, Maximum likelihood and MAP

**Verdict.** Every worked number on the 38 slides, in the notebook and in the workbook recomputes correctly, and the facts about Llama, AdamW and weight decay are published and phrased with care.
The weak points are notation and joins: L stands for the likelihood here but for the loss in Sessions 7 to 12, 17 and 18; y-hat becomes mu without a word; and one figure uses log10.
One lab defect: the "same constant in every row" step assumes sigma = 1, so it breaks after the lab's own CHANGE (sigma = 2).

## Findings

| ID | Where | Cat | Sev | What is wrong | Fix |
|---|---|---|---|---|---|
| 16-1 | Slides 6, 8, 11, 14, 29 (code `L = p**k...`) | 2 | Medium | The likelihood is written L(p) and L(theta). In Sessions 7 to 12, 17 and 18, L is the loss (for example "L(w) = (w - 3)^2" in S10, and "L: the loss" on S17 slide 20). The deck never warns about the switch, and the code slide has `L = p**k * (1 - p)**(n - k)`. | Write the likelihood as Lik(p) or a script L, or add one line on slide 6: "In this session L is the likelihood, not the loss. The loss is the NLL." Rename the code variable to `lik`. |
| 16-2 | Notebook Step 4 (`gap = -log_lik_mu - sse / 2`), workbook Gaussian!L8:L18 (`=-J-K/2`) | 6 | Medium | The gap formula assumes sigma = 1. The Step 3 CHANGE (and the workbook's "set sigma (B4) to 2") makes the gap different in every row, so the READ ("the same number for every mu") is false and the check "leftover constant 7.3515" fails. | Use `gap = -log_lik_mu - sse / (2 * sigma**2)` and the constant n/2 ln(2 pi sigma^2). In the workbook use `=-J8-K8/(2*$B$4^2)`. |
| 16-3 | Slides 15, 16, then 17 and lab Step 3 | 3 | Medium | The derivation is written with y-hat_i ("Assume y = y-hat + noise"). The table and the lab then use mu, and nothing says that the model predicts the same number mu for every part (y-hat_i = mu). A newcomer cannot connect "squared error of a line" to "best mu = the average". | Add to slide 17: "Here the model is the simplest possible: it predicts the same width mu for every part, so y-hat_i = mu." |
| 16-4 | Slide 12 figure (`f_underflow`) | 3 | Medium | The y axis is "log10 of the likelihood", but the slide defines the log-likelihood with ln, and the course uses ln throughout. Base 10 appears with no explanation. | Plot ln, or label it "log base 10, used here only to count the zeros after the decimal point". |
| 16-5 | Slides 9, 32 ("the Session 14 value") | 1 | Low | 0.2668 in Session 14 was P(X = 3) for p = 0.3, which is 3 successes and not 7 heads at 0.7. The number matches only by symmetry (3 tails at 0.3), which the slide does not say. | "the same number as Session 14's P(X = 3) with p = 0.3: 7 heads at 0.7 is 3 tails at 0.3". |
| 16-6 | Slides 10, 22 (rows p = 0.1) | 1 | Low | The likelihood 7.29e-8 and the product are shown as 0.000000, on the slides that argue the product underflows. That reads as "the likelihood is zero". | Use scientific notation (7.3e-8) or 8 decimals for the small rows. |
| 16-7 | Slide 25 caption, lab Step 7 | 3 | Low | "Truth y = sin(2 pi x)": the sine function is never taught in the course. | "a smooth wave (the sine curve, sin(2 pi x))" and do not ask the learner to use it. |
| 16-8 | Slides 25 to 27 | 2 | Low | Bias and variance come with no recall of the Session 12 overfitting picture or its lambda table. The notes say only "as in earlier sessions". | One line on slide 25: "Session 12's degree-9 curve that chased the noise is the high-variance model". |
| 16-9 | Slides 21, 22 (prior weights 1 to 5) | 3 | Low | A prior is a probability, but the weights add up to 25. It is not said that scaling them does not change the winner. | Note: "divide by 25 to make them probabilities; the MAP p does not change". |
| 16-10 | Slides 19 and 23 ("p" for the predicted probability; p(y \| y-hat) for the density) | 3 | Low | The note on slide 14 says "The letter p stays the coin", but p then means the model's class-1 probability (slide 19) and a density (slides 16, 23). | Use q or p-hat for the predicted probability, or drop the "stays the coin" note. |
| 16-11 | Notebook Step 2 check | 6 | Low | `check(..., log_fair_1100, -762.4623, 0.001)`: the true value is -762.4619 (passes only through the tolerance). The slide says -762.46. | Expected value -762.4619. |
| 16-12 | Slide 38 keep | 2 | Low | "Keep the five numbers" lists MLE, MAP, mu, cross-entropy and three expected errors (seven numbers). The card shows four. | "Keep these numbers" or trim to five. |
| 16-13 | Notes throughout | 5 | Medium | 12 of 32 notes open "Here is/are", 3 open "Now the...", "Let us" 3 times. "This is the key derivation" (slide 16). "just" 3 times. | Open with the content ("Seven heads and three tails in one order means..."). Remove "the key". |

### Python check (category 1 numbers)
```
likelihood p=0.1..0.9: [7.29e-08, 6.55e-06, 7.50e-05, 3.54e-04, 9.77e-04, 1.792e-03, 2.2236e-03, 1.678e-03, 4.78e-04]  (peak 0.7, x120 = 0.2668)
log-likelihood at 0.7: -6.108643 ; 1100*ln 0.5 = -762.4619 (slide -762.46 ok; notebook expects -762.4623) ; 0.5**1100 -> 0.0 ; 0.5**100 = 7.9e-31
posterior p=0.6: 0.007166 > p=0.7: 0.006671 -> MAP 0.6
mu grid: best 10.25 = mean, SSE 5.34, loglik -10.0215, constant 4*ln(2pi) = 7.3515
BCE (1,0,1,1; .8,.3,.6,.9) = 0.29900 ; categorical -ln 0.7 = 0.35667 ; change 0.3->0.9 gives 0.7855
-ln .9/.5/.1 = 0.105, 0.693, 2.303 ; y=1,p=.8: 0.223 ; y=0,p=.8: 1.609
ridge w = 28.5/(14+lam): 2.0357, 1.9, 1.5, 1.0179
bias^2/var/total (seed 16): deg1 0.2106/0.0183/0.3189 ; deg3 0.0069/0.0301/0.1270 ; deg9 0.0008/0.8240/0.9148
token NLL 0.2,0.1,0.25,0.05 -> 8.294
MAP algebra: (1/2s^2)SSE + (1/2t^2)sum w^2, times 2s^2 -> SSE + (s^2/t^2) sum w^2  (correct)
```
All slide, notebook and workbook numbers agree. Facts: Llama 1 and 2 report AdamW with weight decay 0.1, and AdamW is Loshchilov and Hutter (ICLR 2019). Both correct.

## Cross-session notes
- **Assumes:** S13 and S14 (Gaussian density, binomial 0.2668, Bernoulli, CLT), S15 (posterior proportional to likelihood times prior), S12 (lambda, ridge, degree-9 overfitting) and S7 (derivative of ln). All of these were taught, but S12 is not recalled. Sine is never taught.
- **Hands to S17:** cross-entropy in nats (0.299). S17 works in bits and never converts S16's value. Add "0.299 nats = 0.431 bits".
- **Notation debt:** fix L (likelihood vs loss) and p (three meanings) before S17 and S18, which use L for the loss again.
