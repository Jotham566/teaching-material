# Audit: Session 18, Course project (five builds)

**Verdict.** Every toy number is correct (weights 1.12, 0.98; logistic table; PCA 1.1556, 0.0442, share 0.9632; network p = 0.3888, delta = -0.6112; attention row 0.401, 0.198, 0.401), and the self-check design (personal data, a second dataset, reference implementations) is sound.
The project does NOT only use what Sessions 1 to 17 taught. Attention (Q, K, V, the square root of d_k, saturation), tanh and its slope 1 - h^2, XOR, and logistic regression as a named model all appear for the first time here, inside a 35-minute tour.
The notebook's Build 1 prints gradient-descent weights far from the normal-equation weights while the slides say "same weights from both". The covariance divisor n is called "the course convention" although Sessions 5 and 6 used n - 1.

## Findings

| ID | Where | Cat | Sev | What is wrong | Fix |
|---|---|---|---|---|---|
| 18-1 | Slides 6, 20 to 23, notebook Build 5 | 2 | High | Attention is new. Before S18 it appears only in passing (S3 notes "attention is built from them", S12 notes "which you will meet"). Queries, keys and values, softmax(QK^T/sqrt(d_k))V, the variance argument for sqrt(d) and "saturation" are all first taught in the project session. Slide 7 says "each one uses mathematics you already know". | Teach attention as a concept in S17 (or extend S14/S17 with 4 slides: QKV picture, formula, hand example, sqrt(d) argument), so that S18 only applies it. At minimum, re-caption slide 7 ("the arithmetic is known; attention itself is new today") and add time. |
| 18-2 | Slides 16, 17, 18; notebook Build 4; workbook Network | 2 | High | tanh is never defined anywhere in S1 to S18 (no formula, no graph), and its slope 1 - h^2 is asserted. S11 taught hidden units with a sigmoid (slope a(1 - a)). | Define tanh(z) = (e^z - e^-z)/(e^z + e^-z) with a graph, and show the slope 1 - tanh^2 with one finite-difference check. Or keep sigmoid hidden units as in S11. |
| 18-3 | Notebook Build 1 (`show("gradient descent, lr 0.005, 400 steps", ...)`); slide 10 | 6 | High | For learner data the 400-step result is far from the normal equation: ALICE 1.627, 2.092 vs 2.456, 1.956; x9z 0.945, 1.500 vs 2.424, 1.234. The TODO hint says "the same weights by repeated small steps", and slides 10 and 11 say "same weights from both" (true for the toy data only after about 5,000 steps at eta 0.02; at 100 steps it is 0.714, 1.075). A newcomer will think their code is wrong even though the check says OK. | Print a converged run (for example 20,000 steps), or add "after 400 steps the intercept has not caught up yet: run more steps and watch it approach". On slide 10 state "after about 5,000 steps". |
| 18-4 | Slides 9, 16, 19 | 2 | Medium | XOR and "a straight line cannot separate XOR" are new and asserted without a picture. | Add the four corners drawn in two colours, with a failed line, beside slide 16. |
| 18-5 | Slide 12 notes, notebook Build 2 | 2 | Medium | Logistic regression is a new named model. The notes say its gradient "you already derived in Session 17". S17 derived softmax + cross-entropy, not sigmoid + binary cross-entropy. | "Session 17's p - y, in its two-class form: a sigmoid is a 2-class softmax." Better, add this link in S17 (see 17-6). |
| 18-6 | Slide 15 notes ("divide by n, the convention of this course"), notebook Build 3 text, workbook PCA!A2 | 1 | Medium | Sessions 5 and 6 built the covariance with n - 1 ("We divide by n - 1, as np.cov does"). The S5 facilitator even flags dividing by n as an error ("A value of 57.75 means dividing by n instead of n - 1"). S18 calls n "the course convention". | "Session 5 divided by n - 1. Here we divide by n. The eigenvectors and the share are unchanged." Or switch S18 to n - 1 (eigenvalues 1.284, 0.049). |
| 18-7 | Slides 11 and 14 (kit `scatter`) | 1 | Medium | The axis tick labels are rounded data extremes placed at the data extremes. On slide 14 the point (0.5, 0.7) sits exactly on ticks "0" and "1", and (3.1, 3.0) on "3", "3". A learner reading the plot gets wrong coordinates. Likely a shared-kit issue (check other decks). | Draw true ticks (0, 1, 2, 3 at their positions) or label the extremes with their true values. |
| 18-8 | Notebook Build 1 text vs check `lin_three_columns` | 6 | Medium | The check calls fit_linear with a 3-column X (1, x, x^2). The step text describes only "the design matrix X has a column of ones first and the hours second". A learner who codes the S4 two-parameter formula gets NOT YET with no explanation until the label appears. | Add to the step: "Write fit_linear for any number of columns; a check uses X with a third column x squared." |
| 18-9 | Clock, slides 26 to 28 | 4 | Medium | 45 minutes to write 12 functions (including backpropagation and a training loop) on new data, for adults with algebra only, some of them non-coders. The facilitator's rescue ("finish Builds 1, 2 and 5 in class") is the realistic plan, but it is hidden. | Make the in-class target Builds 1, 2, 3 and 5, with Build 4 as take-home. Provide a scaffold for mlp_backward (shapes given, two lines blank). |
| 18-10 | Facilitator "after" vs slides 28, 31 | 4 | Medium | "The certificate of completion ... goes to learners who complete the course project", while the slides say nothing is recorded or collected, and spreadsheet learners do a "guided version". It is unclear what counts as complete or who verifies it. | State the rule: for example, "show your Check sheet or the show_checks() line to the facilitator; the guided workbook counts". |
| 18-11 | Slides 21, 32, 33 | 3 | Low | "saturate" is used on slide 21 before slide 22 defines it. "Feed-forward layer", "nonlinearity", "causal mask" and "softmax regression" appear without a plain definition. | Add a one-line gloss for each where it first appears. |
| 18-12 | Slide 33, row 1 | 1 | Low | "Its weights are learned by gradient descent, a different method from least squares" mixes up a method and an objective (least squares can be solved by gradient descent, as Build 1 shows). | "found by gradient descent rather than a direct formula, and usually with a cross-entropy loss rather than squared error". |
| 18-13 | Slide 18 notes | 3 | Low | "the second is twice the first": it is unclear whether this means the second row or the second entry. | "the second entry of each row is twice the first, because the second input is 2". |
| 18-14 | Slides 27, 32 | 3 | Low | The "key" icon for Attention renders as a plain circle (it renders correctly on slide 7). | Fix the icon size or the crop in the steps and stack visuals. |
| 18-15 | Slide 7 caption | 4 | Low | "Each build is about ten lines of numpy": the network build (forward, backward, train) is about 25 lines. | "between 3 and 25 lines". |
| 18-16 | Notes throughout | 5 | Medium | 16 of 31 notes open "Here is/are" (11 and 5). "wonderfully simple" (slide 12). 21 of 36 titles use the "X: Y" pattern. | Vary the openers. Drop the intensifier. Turn some colon titles into plain statements. |

### Python check (category 1 numbers)
```
Build 1 toy: w = (1.12, 0.98), MSE 0.02133, pred(7) = 7.98 ; GD eta .02: 100 steps (0.714, 1.075), 1000 (1.119, 0.980), 5000 (1.12, 0.98); 2/lambda_max = 0.0626
Build 1 learner (ref, 400 steps, lr .005) vs normal eq.: ALICE (1.627, 2.092) vs (2.456, 1.956); BOB 123 (1.583, 2.517) vs (2.404, 2.396); x9z (0.945, 1.500) vs (2.424, 1.234); lr 0.05 diverges (~1e115+) for all 8 IDs tried (facilitator claim ok)
Build 2 toy: step1 w0 = 0 (4 of 8 passed), w5 = (-0.0509, 0.1494), loss 0.6931 -> 0.6232
Build 3 toy: cov/n [[0.5549,0.5539],[0.5539,0.6449]], eig 1.1556, 0.0442, pc1 (0.6779, 0.7352), share 0.9632 ; /(n-1): 1.2840, 0.0491
Build 4 example: h = (-0.0997, 0.9468, 0.1974, -0.9354), 1-h^2 = (0.990, 0.104, 0.961, 0.125), z2 = -0.4522, p = 0.3888, loss 0.9446, delta -0.6112,
  gW2 = (0.0609, -0.5787, -0.1206, 0.5717), gW1 row1 (-0.1815, -0.3631), W2[0] new 0.2695 ; XOR toy 5000 steps: outputs (0.0002, 0.9989, 0.9992, 0.0011), loss 0.706 -> 0.0008
Build 5 toy (by hand): Q rows (1,0),(1,1),(2,1); K (1,1),(0,1),(1,2); V (1,0),(0,2),(1,2); scores row1 (0.707, 0, 0.707); weights (0.4011, 0.1978, 0.4011), out1 (0.802, 1.198); row3 weights (0.306, 0.074, 0.620)
sd of q.k, d=64, 2000 pairs: 7.99 (theory 8)
Learner XOR training (3000 steps) solves XOR for all 8 IDs; logistic accuracy 0.80 to 0.90 (facilitator "below 1" ok)
```

## Does Session 18 only use what Sessions 1 to 17 taught?
| Used in S18 | Taught before? |
|---|---|
| Normal equation, column of ones, design matrix | Yes: S4, S12 |
| Gradient descent, learning rate, divergence | Yes: S10 (matrix form X^T(Xw - y) is new notation, close enough) |
| Sigmoid, binary cross-entropy | Yes: S11, S16 |
| p - y for sigmoid + binary cross-entropy | Partly: S17 derives the softmax case only |
| Logistic regression as a model | **No**, new (assembled from known parts) |
| Covariance, eigenvectors, 2 by 2 eigen formula, eigh, PCA share | Yes: S5, S6 (but with n - 1, see 18-6) |
| Backprop in matrix form, Hadamard product, numeric gradient check | Yes: S9, S11 |
| tanh and its slope 1 - h^2 | **No**, never defined |
| XOR, linear separability | **No** |
| Softmax along rows, stable softmax | Yes: S12, S14, S17 |
| Q, K, V, attention formula, sqrt(d_k), saturation | **No**, first taught here |
| Variance of a sum of independent products (sqrt(d) argument) | Partly: S13 variance and S14 standard error, but not this result |

## Cross-session notes
- S17 should hand over: the sigmoid form of p - y, and ideally the attention concept (or S14/S3 should). Without that, S18 is a teaching session disguised as a project.
- Covariance divisor: settle one course convention (S5 and S6 used n - 1, S13 shows both, S18 uses n) and say it once in the Formula Sheet.
- The scatter tick-label issue (18-7) is in the shared kit and probably affects other decks with `kind='scatter'`.
