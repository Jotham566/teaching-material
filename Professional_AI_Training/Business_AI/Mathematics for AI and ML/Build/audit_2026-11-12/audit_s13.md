# Audit: Session 13, Probability basics

**Verdict.**
Every worked number on the slides, in the notebook, the workbook and the check table recomputes exactly (dice, die variance 35/12, softmax list, E(length) 4.3003, covariance 25/6, r 0.7290, the 60 seeded rolls).
The main problem is a course-level contradiction: the deck says "This course divides by n", but Session 5 taught covariance with n - 1 (`np.cov` default), and nothing reconciles the two. The NumPy default is also misdescribed in the notes.
For a newcomer the deck flows well (sample space, pmf, pdf, E, Var, Cov, r). The weak points are a jump from random variables (pmf) to data columns with no bridge, and lab cells that already contain the variance step.

Files read: `Build/content/s13.py`, `Class Slides PDF/13 - Probability basics.pdf` (34 pages, all viewed), the learner and solution notebooks, `Workbooks/Session 13 - Probability basics.xlsx` (formulas via openpyxl).

## Findings

| ID | Where | Cat | Sev | What is wrong | Fix |
|---|---|---|---|---|---|
| 13-1 | Slide 20 note, slide 23 ("This course uses this version"), slide 13 of S14 | 1, 2 | High | "This course divides by n (population form)." Session 5 (s05.py, slides 11 and 12) defined `cov = 1/(n-1) Σ...`, `C = X_cᵀX_c/(n-1)` and said "We divide by n − 1, as np.cov does." A learner who kept S5 notes gets two definitions of covariance, each called "the" course convention. | Change the S13 wording to "From today the labs divide by n. Session 5 divided by n - 1 (the np.cov default). Both are correct; they differ by the factor n/(n-1)." Add a recall line on slide 18 pointing back to the S5 covariance matrix. |
| 13-2 | Slide 23 notes | 1 | Medium | "NumPy divides by n by default, but pandas divides by n minus one". This is true for `np.var` but false for `np.cov`, which divides by n - 1 by default (that is why `bias=True` is needed on slide 24). | "np.var and np.std divide by n by default; np.cov and pandas divide by n - 1 unless told otherwise." |
| 13-3 | Slides 17 to 20 | 2, 3 | Medium | The deck moves from E(X) and Var(X) of a random variable (sums weighted by p(x)) to the covariance of six data rows (1/n Σ over rows), with no sentence linking them. x̄ appears for the first time with no definition beside μ. A newcomer cannot tell why the die uses p(x) and the learners use 1/n. | Add one line to slide 18 or 20: "For a list of n data rows, each row gets probability 1/n, so E becomes the plain average x̄ and Cov(X,Y) = E[(X-μX)(Y-μY)] becomes (1/n) Σ (xᵢ-x̄)(yᵢ-ȳ)." |
| 13-4 | Slide 19 (covariance by hand) and slide 20 | 2 | Low | Covariance is presented as new, with no recall that S5 built a covariance matrix from eight marks and S6 used it for PCA. | Add "Recall Session 5: the covariance matrix holds these numbers" on slide 18 or 20. |
| 13-5 | Slide 12 (pmf vs pdf) | 3 | Low | The symbol table labels the rows "sum" and "integral", but the formulas show Σ and ∫ and also the "dx" piece, none of which is named. The "Σ_x" subscript is also unexplained (S1 introduced Σ with i = 1..n, not Σ over x). | Name the symbols: "Σ (sigma, from S1): add over every value x", "∫ ... dx: the area under f between a and b; dx marks the variable along the axis". |
| 13-6 | Slide 18 (covariance scatter) | 3 | Low | The plot has no axis tick values, so a reader of the PDF cannot match the six dots to the six (x, y) pairs. | Add ticks at 0, 2, 4, 6, 8 (x) and 0, 2, 4, 6, 8, 10 (y), or label each dot with its pair. |
| 13-7 | Slide 17 notes | 3 | Low | "A typical roll lands about 1.7 away from 3.5." The mean absolute distance is 1.5. The standard deviation is a root-mean-square distance, so "typical" overstates the reading. | "The standard deviation, 1.71, is a root-mean-square distance from 3.5 (the plain average distance is 1.5)." Or drop the sentence. |
| 13-8 | Slide 20 symbol row r | 3 | Low | "(rho: same, for a population.)" introduces ρ, which appears in no formula, and then the slide uses population σ with r. | Drop the ρ remark, or show ρ in the formula line. |
| 13-9 | Slide 16 symbol table | 3 | Low | "E(X^2)" uses a caret in the table while the formula line uses a superscript. | Write E(X²). |
| 13-10 | Slide 25 code bridge vs notebook Step 3 | 6 | Low | On the slide, `big` is drawn from the same generator after the 60 rolls (mean 3.4977, var 2.9018). The notebook re-seeds before drawing `big` (3.5024, 2.9062). The slide prints no numbers, but a learner who types the slide code gets different values from a neighbour. | Make the slide code re-seed (`rng = np.random.default_rng(13)`) before line 4, as the notebook does. |
| 13-11 | Workbook sheet Die, column D | 6 | Medium | `D4:D9 = (x - SUMPRODUCT(x,p))^2 * p` is pre-filled, so the gold "Var(X)" cell is only `=SUM(D4:D9)`. The spreadsheet learner never builds the variance, while the Python learner does. | Make column D gold (the learner writes the squared-distance term), or leave it blank with a hint. |
| 13-12 | Notebook Step 1, cell 7 | 6 | Low | `p_2_or_12` is a TODO in the main cell, but the prompt that explains it comes after the cell, in the CHANGE text. A newcomer meets an unexplained variable. | Move the sentence "also compute P(sum is 2 or 12), the two extreme sums" into the hint above the cell. |
| 13-13 | Notes, whole deck | 5 | Medium | 14 of 28 slide notes open with "Here is/Here are/Now/Let us". There is also one "Imagine" (slide 14). | Vary the openers. Start with the content ("Two fair dice give 36 outcomes..."). |
| 13-14 | Slide 13 lead | 4 | Low | E(length of next word) is a made-up use with no AI meaning, and it is the only expectation example besides the die. | Swap it for an expectation with an AI meaning, for example the expected loss -E[ln p] of the next word, which sets up S16 and S17. |

### Python checks (category 1)
```
softmax([3,2.6,1.9,1.2,0.4]) = [0.4459 0.2989 0.1484 0.0737 0.0331], sum 1.0; E(len) = 4.30030
die: E=3.5, E(X^2)=15.1667, Var=2.91667, sd=1.70783
x,y: means 4,6; products [6 8 -2 -1 2 12] sum 25; cov(n)=4.16667, var x 4.66667, var y 7.0,
     r=0.729015; cov(n-1)=5.0; var_y(n-1)=8.4
rng(13) 60 rolls = the typed list; mean 3.96667, var 3.13222
slide code (continuing rng) big: 3.4977 / 2.9018; notebook (re-seeded) big: 3.5024 / 2.9062
np.cov default (no bias) = 5.0  -> contradicts "NumPy divides by n by default"
Workbook Check tolerances: all expected values within tolerance of the true values (checked).
```
Facts checked: Llama 2 vocabulary of 32,000 (correct); layer normalisation from Ba, Kiros and Hinton 2016, used in the original transformer (correct); RMSNorm in Llama (correct); fp16 maximum 65,504 (correct).

## Cross-session notes
- **Assumed but not taught:** "independent" is used in the facilitator misconceptions and is used heavily in S14 (Bernoulli trials, CLT) but is defined only in S15. S13 is the natural place for a one-line definition with two dice.
- **Assumed:** softmax and logits (S12, correctly recalled); Σ (S1); square root and sigma notation. ∫ is new and handled as "area".
- **Conflict:** the S5 n - 1 convention (13-1).
- **Hands forward:** pmf over the vocabulary (to S14 sampling and S17); mean and std (to S14 z-scores); the covariance matrix (to S14 multivariate Gaussian). S16 needs "expectation of a function", E[g(X)]. Only E(X²) shows it, so a sentence on E[g(X)] = Σ g(x) p(x) would prepare cross-entropy as -E[ln q].
