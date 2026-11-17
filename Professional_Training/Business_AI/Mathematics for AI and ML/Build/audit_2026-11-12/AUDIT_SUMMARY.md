# Mathematics for AI and ML: audit summary (12 November 2026)

Scope: all 18 sessions (decks, speaker notes, facilitator notes, learner and solution notebooks, workbooks), read as a complete newcomer with high school algebra only. Six auditors recomputed every worked number in Python and looked at every slide. Per-session findings with the Python checks are in `audit_s01.md` to `audit_s18.md` beside this file. No course file was changed.

**Totals: 12 High, 98 Medium, 168 Low.** Every worked number on the slides recomputes correctly. The problems are false or loose statements, conventions that change between sessions, ideas used before they are taught, overloaded sessions, lab mechanics, and templated writing.

## 1. Lab integrity (fix first)
- **Notebooks can say "All checks pass" when tasks were skipped** (all sessions; confirmed in `kit/nb.py`). `show_checks()` counts only checks that ran; a print line that crashes on an unanswered `None` stops its checks from registering. Session 5 skipping three tasks prints "All 10 checks pass" of 17. Fix in the shared kit: tell each notebook its total, and make print lines safe on `None`.
- **Session 18, Build 1:** 400 gradient-descent steps end far from the normal-equation weights for learner data (1.63, 2.09 against 2.46, 1.96), but the slide and hint say the two agree. Learners with correct code will think they are wrong.
- Lab maps and notebooks disagree on step counts (S3: 5 vs 7; S6: 6 vs 7, σ₁ to σ₃ vs stops at σ₂); S9 workbook "change one thing" points at the wrong cell; learner notebooks print answers before the PREDICT step; S10 to S12 hand out the loop, the answers in hints and pre-filled "change" cells; notebook file names repeat "Session 12 - Session 12" (S12 to S15); no solution workbooks in Facilitator Materials.

## 2. Statements that are wrong or too strong
| Session | Statement | Correct |
|---|---|---|
| 2 | "In our toy data a longer text gives a longer vector" (also implied of real embeddings) | False: toy lengths 0.83 to 0.95, unrelated to text length; distance and cosine rank the same top four |
| 2 | RAG (Lewis et al. 2020) ranks passages by cosine | It uses the dot product (maximum inner product search) |
| 3 | "compute X W instead of W x" | With one token per row it is X Wᵀ (as in PyTorch `Linear`); the square example hides it |
| 5 | "a 2 by 2 matrix has at most two such directions" | False for 2I (every direction); say "at most two distinct eigenvalues" |
| 6 | U and Vᵀ called rotations | The printed matrices are reflections (determinant −1); the figure silently flips signs |
| 7 | h = 1e-12 gives 0.0 or noise | It gives 6.0005; 0.0 only at about 1e-16 |
| 7, 9 | Finite-difference tables round f(x+h), so hand checks give 6.000 and 42.000, not 6.001 and 42.009 | Show more digits |
| 12 | λ chosen on the 20 "new points" whose error (0.158) is then reported; and λ = 0.2 gives 0.1569 | Choose on a validation split; report the test once; fix the minimum |
| 13 | Notes: NumPy divides by n by default | `np.cov` divides by n − 1 |
| 14 | Top-p values 0.4995, 0.3349, 0.1657 (facilitator) | 0.4992, 0.3346, 0.1662 |
| 11 | Update note: "two parameters go down" | Three |

## 3. Conventions that change between sessions (choose one each)
- **Covariance and variance divisor:** S5 and S6 divide by n − 1; S13, S14 and S18 say "this course divides by n". Recommendation: n − 1 for sample data from now on, explained once (S5), with n for a whole known distribution (S13), and every later slide says which.
- **Vectors:** written as rows in S2, "a vector is a column" in S3, gradient a row in S8 and a column in S9. Recommendation: column vectors from S3 onward, said once, with xᵀ for rows.
- **Letters:** b is bias (S1, S3), right-hand side (S4), intercept (S8, S10); intercept and slope are w₀, w₁ (S4) then b, w (S8, S10); L is likelihood (S16) and loss elsewhere; θ appears undefined in S8 and S9. Recommendation: b = bias/intercept only, w = weights, L = loss, likelihood written in words or as p(data | θ), θ defined in S8.
- **Loss:** MSE (S10), ½ squared error (S11), sum of squared errors (S12) without reconciling. Recommendation: one slide in S10 that shows the three differ only by a constant factor.
- **Logs:** S1 entropy 1.133 is in nats without saying so; S17 works in bits. Name the unit each time.

## 4. Ideas used before they are taught
School trigonometry (cosine, arccos, radians in S2; the angle in the S8 lab); variance and covariance in S5 (taught in S13); training and fine-tuning in S6 (taught S7 to S10); the 2 and xᵢ in the loss slope credited to the power rule (it is the chain rule, S9); the rule that slopes along different paths add (needed in S9 slide 21 and S11); forward and backward pass and cross-entropy in S10 and S11; the sigmoid slope a(1 − a) asserted in S11 (S12 relies on its 0.25 maximum); independence in S14 (defined in S15); factorial and the origin of 1.96 (S14); tanh, XOR, logistic regression as a model and the whole of attention in S18, which claims "each one uses mathematics you already know". Softmax and "subtract the max" are taught three times (S12, S14, S17) without recall.

## 5. Sessions that are too full
S12 (about 22 concept slides in 35 minutes, two unrelated halves: regularisation, then floating point and stability), S14 (23 concept slides, about 14 new ideas), S6 (too many slides for 35 minutes). S18 teaches attention new in the project session.

## 6. Newcomer clarity (examples)
Steps skipped: S4 elimination stops before x₁ = 2, the inverse formula is given only in words, why multiply by Xᵀ; S9 slide 21 (∇ₓ s = Jᵀ ∇ s with an undefined subscripted ∇). Figures: the letters A, B, C = AB reused for different matrices (S3), the layer figure highlights y₂ while the text works y₁ (S3), the S8 contour labels make the start look lower than it is, scatter-plot tick labels show rounded data extremes (shared kit; S18 slide 14 puts (0.5, 0.7) on ticks 0 and 1).

## 7. AI-like writing
About 40 to 50% of speaker notes open with "Here is", "Here are", "Now" or "Let us"; table and slide titles repeat templates across decks; notes end on questions by habit. The style lint used for the two executive editions would catch these.

## Recommended fix plan
1. Shared kit: notebook check totals and `None`-safe prints; scatter ticks; notebook file names; build solution workbooks.
2. Correct the statements in section 2 and the S18 Build 1 lab.
3. Apply one convention for each item in section 3 across all 18 sessions, labs included, with a one-line "notation" note where each is first set.
4. Close the gaps in section 4: short taught slides where each idea first appears (a trigonometry refresher in S2, the sum-over-paths rule in S9, the sigmoid slope and tanh in S11, independence in S13, factorial and 1.96 in S14, attention taught in S17 so S18 only recalls it), and one owner for softmax (S17) with recalls elsewhere.
5. Rebalance S6, S12 and S14 (move or cut slides; S12's floating-point half becomes its own clearly bridged part).
6. Newcomer clarity fixes per session file.
7. De-slop titles and notes with the style lint.
