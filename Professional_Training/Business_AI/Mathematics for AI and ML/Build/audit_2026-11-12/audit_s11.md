# Audit: Session 11, Backpropagation by hand

Sources read: `Build/content/s11.py`, `Build/kit/diagrams_math_d.py` (n11), `Class Slides PDF/11 - Backpropagation by hand.pdf` (33 pages, all looked at), learner and solution notebooks, `Workbooks/Session 11 - Backpropagation by hand.xlsx`. Slide references are PDF page numbers.

## Verdict
1. All the arithmetic is correct and consistent across the slides, notebook and workbook: the forward pass, deltas, nine gradients, update, loss 0.3417 to 0.0085 to 0.0002, and the finite difference. One spoken note miscounts the parameters that go down.
2. This is the strongest of the three decks for build-up: a network picture, every number, a scalar table, then matrix form, then shapes, then a finite-difference check. It leans directly on S9 and S10.
3. Gaps: the sigmoid slope a(1 - a) is asserted and never derived; the ∇W notation clashes with ∇L from S8 and S10; the notebook's TODO hints contain the full answers; the AI slide overclaims "only the sizes differ".

## Findings

| ID | Where | Cat | Sev | What is wrong | Fix |
|---|---|---|---|---|---|
| 11-01 | p16 notes | 1 | Medium | The notes say "Every parameter with a negative gradient goes up, and the two with positive gradients go down." Three gradients are positive: W(1) row 2 input 1 (0.0794), W(1) row 2 input 2 (0.1589) and b(1) unit 2 (0.0794). The table on the same slide shows three values going down. | "...and the three with positive gradients, all belonging to hidden unit 2, go down." |
| 11-02 | p12, p14, p32 | 2/3 | Medium | "da/dz = a × (1 - a)" is stated as a fact ("a neat derivative" in the notes) and is never derived or checked. S7 taught the derivative of eˣ and the quotient rule, so the derivation is within reach. It also feeds the S12 claim that "0.25 is the largest slope". | Add one line or a small box: "σ(z) = 1/(1+e^-z); by the quotient rule (S7), σ'(z) = e^-z/(1+e^-z)² = σ(z)(1 - σ(z)). Check at z = -0.3: 0.4256 × 0.5744 = 0.2445." |
| 11-03 | p18, p19, p20 | 3 | Medium | "∇W(2) = δ(2) a(1)ᵀ": in S8 and S10, ∇L means "the gradient of L". Here ∇W means "the gradient of the loss with respect to W", and a newcomer reads it as "the gradient of W". | Write ∂L/∂W(2) (or ∇_W L) on these three slides, and say in the symbol table "the gradient of the loss L with respect to the matrix W". |
| 11-04 | p29 | 1/4 | Medium | "Only the sizes differ" overclaims. Language models also differ in architecture (attention, normalisation, a softmax output and a cross-entropy loss in place of squared error) as well as size. Also, "cross-entropy" is not defined on the slide. | "The steps are the same; the model, its loss (cross-entropy, Session 17) and its size differ." |
| 11-05 | Notebook cell 10 (learner) | 6 | Medium | Each TODO line carries the full answer as a comment, e.g. `d1 = None  # your code here: (W2.T @ d2) * a1 * (1 - a1), shape (2,)` and `gW1 = None  # your code here: np.outer(d1, x)`. The learner copies text and does not think it through. | Give words only: "send d2 back through W2 transposed, then multiply by the sigmoid slope entry by entry"; "the gradient of W1 is delta(1) times the input, transposed". |
| 11-06 | p9 | 3 | Low | σ appears in the formula but is not in the symbol table. W(2)_j, b(2), x_i and y are also missing from the table, though W(1) is listed. | Add a row "σ (sigma): the sigmoid, 1/(1+e^-z)" and a row for W(2), b(2). |
| 11-07 | p6 words | 3 | Low | "Delta: the gradient of the loss with respect to the input of a unit". delta(2) is then defined as dL/d(y-hat), the output. The two agree only because the output unit has no activation, which is never said. | Add to p13's note: "The output unit has no sigmoid, so its input and its output are the same number, y-hat." |
| 11-08 | p22 note | 3 | Low | "A relative difference below about 1e-6": "relative difference" is not defined, and the slide shows an absolute difference (3.5e-12). | "relative difference = |a - b| / max(|a|, |b|)", or speak of the absolute difference consistently. |
| 11-09 | p26 vs notebook | 6 | Low | The slide says "five stages". The notebook has 6 steps (Step 6, eta = 5, is extra). The facilitator answer key says "CHANGE: use eta = 5 ... The loss jumps or oscillates". In fact it explodes: 0.34, 16.3, 317, 5078, 81240. | Mention Step 6 on p26. Change the key to "the loss grows about 16-fold every step". |
| 11-10 | Notebook cell 26 | 6 | Low | "falling by a roughly constant factor at each step. About what factor: 2, 10 or 50?" The ratios are 40, 54, 64, 65.6..., so the factor is not constant at first and settles near 66. | "...settles near which factor: 2, 10 or 60?" and add the answer to `lab_answer_key`. |
| 11-11 | Workbook Train chart | 6 | Low | The loss chart uses a linear y-axis. After step 1 the line is flat at zero, so "look at the chart" (Start here step 5) shows nothing. The notebook uses a log scale. | Set a log y-axis (`logBase=10`), or chart only steps 0 to 5. |
| 11-12 | Workbook Check rows 21 and 22 | 6 | Low | The Train sheet is computed from the given parameters, so its two checks pass without learner work. | Label them "(given)", or have Train row 1 reference the learner's Network!B34:D36. |
| 11-13 | p7, p15 | 3 | Low | The weight labels on the two crossing lines (0.4 and -0.3, then 0.079 and -0.202) sit next to the crossing point. Which line each belongs to is guessable but not obvious. | Put each crossing-line label near its source input end, or draw the crossing edges in two greys. |
| 11-14 | p12 | 5 | Low | The gold highlight on the "Sigmoid" step marks nothing explained on the slide. | Remove the highlight, or add a caption saying why: "the step learners most often forget". |
| 11-15 | Notes | 5 | Low | "Here is/are" (12 times), "Now" (5), "simply", "just", "neat derivative". The same stock lines as S10 and S12 ("Four mistakes to watch for.", "A hands-on check.", "Three questions to finish.", "Use this table as your checkpoint."). | Vary or cut them. |
| 11-16 | p30 | 4 | Low | "a training step costs roughly three times as much as one answer on the same text" (notes) is fine, but generation runs one forward pass per new token. Learners may think answering a 500-token reply costs one forward pass. | Keep the wording on the slide ("one forward pass per token") and repeat it in the exit answer. |

## Category 1 checks (Python, numpy)
```
x = (1, 2), y = 1, W1 = [[0.2,-0.3],[0.4,0.1]], b1 = (0.1,-0.2), W2 = [0.5,-0.4], b2 = 0.2, eta 0.5
z1 = (-0.3, 0.4); a1 = (0.425557, 0.598688); y-hat = 0.173304; L = 0.341713     OK
delta2 = -0.826696; gW2 = (-0.351807, -0.494933); gb2 = -0.8267                 OK
sigmoid slopes = (0.244458, 0.240261); delta1 = (-0.101046, 0.079449)           OK
gW1 = [[-0.101046,-0.202093],[0.079449,0.158898]]                               OK
positive gradients: gW1[1,0], gW1[1,1], gb1[1]  -> THREE (notes say two)        11-01
new W1 = [[0.250523,-0.198954],[0.360275,0.020551]]; b1 = (0.150523,-0.239725);
new W2 = (0.675903,-0.152534); b2 = 0.613348                                    OK
L after 1 = 0.0085265 (97.5% removed -> "98%"); y-hat 0.869413; after 2 = 0.00015668   OK
finite difference W1[0,0], h = 1e-5: -0.1010463936302 vs -0.1010463936336, diff 3.5e-12   OK
eta 5, 1 step: 16.2753 (notebook check) OK; eta 10 grows ~ 66.5 after 1 step
50 steps eta 0.5: ~0 (below 1e-20)                                              OK
Kaplan et al. 2020: forward ~2N FLOPs/token, backward ~4N -> "backward about twice forward" OK
```

## Cross-session notes
- Assumes from earlier sessions: the chain rule (S9), the update rule and eta (S10), transpose and matrix product (S3), the central difference (S7), eˣ (S1/S7). Not taught before: the derivative of the sigmoid (11-02) and the Hadamard product (defined here, fine).
- Loss is 1/2 (ŷ - y)² here, against MSE in S10. The slide gives the reason for the 1/2, which is good, but say once that the minimum is the same.
- Hands to S12: the sigmoid slope ≤ 0.25 (S12 p26 relies on it, so 11-02 matters); the forward/backward pass for vanishing gradients. Hands to S17/S18: cross-entropy replaces squared error, and the S18 2-4-1 network reuses exactly these formulas. A sentence on p32 or p33 pointing to S18 Build 4 would close the loop.
