# Audit: Session 2, Vectors

Sources read: `Build/content/s02.py`, `Class Slides PDF/02 - Vectors.pdf` (all 32 pages viewed), learner and solution notebooks, `Workbooks/Session 02 - Vectors.xlsx`, `Build/content/labs/s02_xl.py`.
Slide numbers are PDF page numbers (pN). PDF page = outline slide index + 4.

## Verdict
1. The arithmetic is all correct, and the sequence of picture, formula and lab (vector, add, scale, dot, norm, distance, cosine, search) is well built and highly relevant to embeddings and retrieval.
2. The session's main argument for cosine similarity rests on a false claim about its own data: "In our toy data a longer text gives a longer vector". The toy norms are 0.83 to 0.95, unrelated to sentence length, and distance gives the same top four as cosine. The RAG slide also implies the published design ranks by cosine, but Lewis et al. (2020) rank by inner product.
3. For newcomers, ‖·‖, cos θ and arccos appear on p13 before they are taught. Cosine, arccos and radians are assumed from school trigonometry, which the entry requirement (algebra only) does not include.

## Findings

| ID | Where | Cat | Sev | What is wrong | Recommended fix |
|---|---|---|---|---|---|
| S2-01 | p20 verdict; p18 notes; p20 notes | 1 | High | p20 says "In our toy data a longer text gives a longer vector, so cosine says alike and distance says far apart". The p18 notes say "useful in our toy data, where a longer text gives a longer vector". Both are false for this data. The six norms are 0.911, 0.831, 0.927, 0.927, 0.837 and 0.949, with no link to word count (6, 6, 5, 5, 5, 6 words). Ranking by Euclidean distance gives the same top four as cosine (S1, S2, S5, S4); only the two irrelevant sentences, S3 and S6, swap places. The general claim is also false: in real embedding models, vector length does not track text length, and many models normalise to length 1. | Replace with a true reason: "Cosine ignores length, so a vector that is long for any reason (a scaling quirk, or a repeated or very common text) cannot win on length alone. Step 7 makes one vector 20 times longer to show this." Drop "longer text gives a longer vector" from the slide and the notes. |
| S2-02 | p29 caption and notes; p31 Q3; S3 recall Q3 | 1 | Medium | "Published design: retrieval-augmented generation (Lewis et al., 2020)" sits under a flow whose highlighted step is "Cosine", and the notes say "compares ... by cosine similarity". Lewis et al. retrieve by maximum inner product (dot product) of DPR embeddings. Exit question 3 also presumes search tools rank by cosine and not by dot product, but many rank by dot product on normalised vectors. | Caption: "Published design: RAG (Lewis et al., 2020) scores passages by a dot product of embeddings. With vectors of length 1 this equals cosine similarity." Reword exit Q3 to: "When is ranking by the raw dot product risky, and what fixes it?" |
| S2-03 | p13 | 2 | Medium | The "geometric form" u·v = ‖u‖‖v‖cos θ, with θ = 53.4°, uses the norm (taught on p14) and the cosine (taught on p18) before either is defined, and arccos before p19. | Move the geometric form and the 0.596 / 53.4° example to p19 (cosine formula). Keep p13 to the sum of products. |
| S2-04 | p18, p19, workbook Hand B24, notebook Step 4b hint | 3 | Medium | Cosine, arccos, degrees and radians are assumed knowledge ("You may remember cosine from school"). The entry requirement is high school algebra only. The notebook hint mentions radians, and the workbook needs DEGREES(ACOS(...)), but neither radians nor ACOS appears on a slide. | On p18 add one plain line: "cos θ is a number from −1 to 1 that measures how much two arrows point the same way; a calculator or COS gives it from the angle, and arccos (ACOS) goes back." On p19 add: "Computers give angles in radians; DEGREES() or np.degrees() converts." |
| S2-05 | workbook Search B13 | 6 | Medium | The best match needs `INDEX(...MATCH(MAX(...)...))`. INDEX and MATCH are named only in the speaker notes, not on any slide or in the sheet. A spreadsheet newcomer cannot produce this. | Add the formula pattern to the p24 recipe ("Spreadsheet: =INDEX(A4:A9, MATCH(MAX(H4:H9), H4:H9, 0))"), or put a hint in the gold cell's row. |
| S2-06 | p20 compare | 2 | Low | The example "u = (1, 2) and 3u = (3, 6)" introduces new vectors on the comparison slide. The deck's own a = (3, 4) and 2a = (6, 8) would make the same point. | Use a and 2a: distance 5, cosine 1. |
| S2-07 | p21 verdict, p31 answer | 3 | Low | "Many real models scale vectors to length 1" is correct, but the industry term (normalise, unit vector) is never named, and learners will meet it in every embedding API document. | Add "(this is called normalising; the result is a unit vector)". |
| S2-08 | p13, p15 | 3 | Low | The middle dot "·" means ordinary multiplication in "1·2 + 2·0" and the dot product in "u·v" on the same line. | Use × for numbers: 1 × 2 + 2 × 0 + 2 × 1. |
| S2-09 | p7, p8 | 3 | Low | a is (21, 6, 72) on p7 and then (3, 4) from p8 on. | Call Amina's row x or **r**, and keep a = (3, 4). |
| S2-10 | p18 figure | 3 | Low | The label "reference: 1" sits under the 45° arrow and reads as that arrow's label. No angle arcs are drawn. | Put the label at the tip of the horizontal arrow, and draw small arcs marked 45°, 90° and 180°. |
| S2-11 | notebook Step 3 check label | 6 | Low | The check says "the distance from p to q is 5", but the slides deliberately use P and R ("the letter q is kept for the query"). | Change it to "from P to R". |
| S2-12 | notebook Step 7b | 6 | Low | The TODO hint gives the answer ("it is already in sims2"), so the learner computes nothing. | Ask for the cosine of `E2[5]` with q from the formula, or make it a READ step with no TODO. |
| S2-13 | facilitator probe 8 | 1 | Low | "Our toy embeddings have only positive entries": several entries are 0. | Say "no negative entries". |
| S2-14 | notes | 5 | Low | 20 of 26 notes end on a question. The notes contain 9 "Here is/are", "just" ×4, "exactly" ×4, and "simply". The formula titles all follow "X as a formula: Y" (4 slides). | Vary the note endings, cut the fillers, and give the formula slides titles that state their result (e.g. "The L2 norm is the square root of the dot product of a vector with itself"). |

## Python check
```
cos(a,b) = 24/25 = 0.96 ; angle = 16.2602 deg            OK
u.v = 4 ; |u| = 3 ; |v| = 2.2361 ; cos = 0.5963 ; angle = 53.396 deg  OK
dist P->R = 5 ; dist (1,2)->(3,6) = 4.4721                 OK
dots E@q = [0.785 0.715 0.07 0.23 0.30 0.08]
sims = [0.9949 0.9939 0.0872 0.2864 0.4140 0.0974]          OK (slide 0.995 / 0.994 / 0.414 / 0.286 / 0.097 / 0.087)
row norms = [0.911 0.831 0.927 0.927 0.837 0.949]           <- no "longer text, longer vector" (S2-01)
sentence word counts = [6 6 5 5 5 6]
Euclidean distance to q = [0.100 0.100 1.212 1.072 0.922 1.221] -> same top 4 as cosine; only S3 and S6 swap (S2-01)
stretched picnic dot = 1.6 ; factor 2 -> 0.16 ; picnic cosine unchanged 0.0974   OK
exit: (2,3).(4,1) = 11 ; |(6,8)| = 10                        OK
```

## Cross-session notes
- **Assumes, but not taught:** trigonometry (cosine, arccos, degrees and radians) and the Pythagoras rule. Pythagoras is fine for algebra-level adults. Cosine is not, so add the S2-04 line.
- **From S1:** Σ is recalled correctly. The p12 notes link the dot product to "a sigma sum of products", which is good.
- **Hands to S3:** S3 p18 states "By convention a vector is a column", but S2 writes every vector as a row, (3, 4). S2 could add one line: "we write vectors across the page to save space; in matrix work they stand as columns (Session 3)".
- **Hands to S18 (attention):** the dot product as a similarity score is the core of QKᵀ. Fixing S2-01 and S2-02 (dot product versus cosine, and normalisation) matters here, because attention uses a scaled raw dot product, not cosine. A learner told that "the raw dot product is a mistake" will be confused in S18. Add a forward note: "attention (Session 18) uses the dot product divided by √d, and softmax then handles the scale".
