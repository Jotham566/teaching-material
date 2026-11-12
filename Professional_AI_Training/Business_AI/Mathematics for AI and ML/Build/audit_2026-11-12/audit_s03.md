# Audit: Session 3, Matrices

Sources read: `Build/content/s03.py`, `Class Slides PDF/03 - Matrices.pdf` (all 38 pages viewed; p20 zoomed), learner and solution notebooks, `Workbooks/Session 03 - Matrices.xlsx`, `Build/content/labs/s03_xl.py`.
Slide numbers are PDF page numbers (pN). PDF page = outline slide index + 4.

## Verdict
1. Every product, layer output and parameter count is correct. The line from the S2 dot product to the matrix product, the layer y = Wx + b and parameter counting answers the session's question well. The open-model facts (Llama 2 at 7, 13 and 70 billion; Vaswani 2017) are within the facts discipline.
2. The figures often disagree with their slides. The identity, the stacked layers and the X W picture are all labelled with generic A, B and C = AB. The layer picture highlights the weights into y₂ while the text works y₁. The letter A means two different matrices.
3. The switch from W x to X W is presented as the same W, which is wrong (it is the transpose). The lab map says five steps, but the notebook and workbook have seven, and the facilitator answer key uses the slide numbering.

## Findings

| ID | Where | Cat | Sev | What is wrong | Recommended fix |
|---|---|---|---|---|---|
| S3-01 | p24 caption and notes | 1 | Medium | "One token per row, so the product is X W, where one vector used W x" and "Frameworks ... compute X W instead of W x" imply the same W. With tokens as rows, the weight matrix in X W is the transpose (inputs × outputs) of the W in W x (outputs × inputs). PyTorch's Linear layer stores W as outputs × inputs and computes X Wᵀ + b. The square 3 × 3 example hides the shape change. | "With one token per row we compute X Wᵀ: the same weights, transposed (W x per column becomes X Wᵀ per row). Libraries such as PyTorch do exactly this." Use a non-square W (e.g. 3 inputs → 2 outputs) so the shapes force the point. |
| S3-02 | p7, p8 vs p11 onward; recipe p29 | 3 | Medium | A is the 3 × 3 learner table on p7 and p8 ("A₂₃ = 58", "A ∈ ℝ^{3×3}"), then the 2 × 3 matrix [[1,2,3],[4,5,6]] from p11 on. The notebook and workbook call the table L. | Rename the table L on p7 and p8 (L₂₃ = 58), matching the lab. |
| S3-03 | p19 figure | 3 | Medium | The identity slide's figure is labelled "A" and "y = A x", but the matrix is I and the text says I x = x. A is already a 2 × 3 matrix on this deck. | Label the figure I and "I x = x". |
| S3-04 | p23 figure | 3 | Medium | "Stacking two layers" shows the matrices labelled A, B and "C = A B". The slide is about W2, W1 and W2 W1. | Label them W2 (2 × 4), W1 (4 × 3) and W2 W1 (2 × 3). |
| S3-05 | p24 figure | 3 | Medium | The token matrix and the weights are labelled A, B and C = AB. The caption talks about X and W. | Label them X (4 tokens × 3) and W, and give the answer as X W (or X Wᵀ after S3-01). |
| S3-06 | p20 figure | 3 | Medium | The text works output 1 (1 × 1 + 0 × 2 + 2 × 3 = 7, plus 0.5 gives 7.5). The dark lines in the figure run from x₁, x₂ and x₃ into y₂ = −1. The picture shows a different row from the one explained. | Highlight the three lines into y₁ (and mark the zero weight from x₂). |
| S3-07 | p8 | 3 | Medium | "A ∈ ℝ^{m×n}" names neither ∈ nor ℝ. The table only paraphrases the whole formula. A newcomer cannot read the symbol when it next appears. | Add rows: "∈: 'is a member of' / 'is a'" and "ℝ: the real numbers (ordinary numbers with decimals)". Or drop the set notation and write "A is m × n". |
| S3-08 | p18 note; S2 | 2 | Medium | "By convention a vector is a column" arrives without warning. S2 drew and wrote every vector as a row (3, 4), and p7 says "each row is a vector". | Add: "On paper we write (1, 2, 3) across the page to save space. In a matrix product a vector stands as a column, and the transpose makes it a row." |
| S3-09 | p31 lab map; facilitator lab_steps and lab_answer_key | 6 | Medium | The slide says "The lab has five steps" (1 Table, 2 Multiply, 3 Move, 4 Layer, 5 Count). The notebook and workbook have Steps 1 to 7: Step 2 is A x, Step 3 is A B, Step 4 is the shape, Steps 5 and 6 are the layers, Step 7 is the parameters. The answer key says "Step 3 CHANGE: rotation", "Step 4 READ: W2 W1" and "Step 5 CHANGE: hidden layer 5", which are Steps 4, 6 and 7 in the files. | Make the lab map list the 7 notebook steps, and renumber the facilitator lab_steps and answer key to match. |
| S3-10 | workbook Layers B17:B20, B29:B30 | 6 | Medium (unverified) | `=MMULT(B4:D7,B8:B10)+B12:B15`, typed by a learner in Google Sheets "in the first gold cell and press Enter", may not spill. Range addition in Sheets normally needs ARRAYFORMULA (or Ctrl+Shift+Enter). The README says the workbooks were never opened in Google Sheets. | Test in Google Sheets. If it does not spill, tell Sheets users to press Ctrl+Shift+Enter (which adds ARRAYFORMULA), or to write `=ARRAYFORMULA(MMULT(...)+B12:B15)`. |
| S3-11 | p22, p23, notebook Step 6 READ | 3 | Low | "a fixed nonlinear function" and "no nonlinear step" use "nonlinear", which is not defined. | Add "nonlinear: its graph is not a straight line, e.g. max(0, x)". One example makes the collapse argument concrete. |
| S3-12 | p9 notes | 1 | Low | "Which of the three keeps the shape the same size?" Both the rotation and the shear keep the area (determinant 1). Only the scale changes it. The intended answer (rotation) is ambiguous. | Ask "Which of the three keeps the shape exactly as it was, only turned?", or accept both and plant the determinant for S4 (area factors 2, 1 and 1). |
| S3-13 | p35 card, notes | 1 | Low | "about 68,719,476,736 multiplications" puts "about" before an exact count. | Say "68,719,476,736 (about 69 billion)". |
| S3-14 | p27 | 3 | Low | "At 2 bytes each" and "sixteen bits" assume the learner knows bits and bytes. | Add "(a byte is 8 bits; 16-bit numbers take 2 bytes)". |
| S3-15 | notebook Step 1, lab map notes | 6 | Low | The notes say Step 1 covers "the transpose and the identity", but neither the notebook nor the workbook touches the identity. | Add `np.eye(3) @ x` as a READ step, or drop "identity" from the notes. |
| S3-16 | p31 | 3 | Low | The icon for step 5 "Count" renders as a plain circle. The other steps have proper icons. | Fix the icon name (the 'key' icon is missing at this size). |
| S3-17 | p38 Take away | 3 | Low | "Formula sheet: Three new rules" does not say which three. | List them: "shape rule; C_ik = Σ A_ij B_jk; parameters = m n + m". |
| S3-18 | cover title | 5 | Low | "the heart of every AI layer" is a slogan. Attention and normalisation layers are not only matrix products, and the deck itself says so on p34. | "...and the core arithmetic of a neural-network layer". |
| S3-19 | notes | 5 | Low | 11 notes start "Here is". The notes also contain "simply" ×2, "just" ×5, "you can think of a matrix as". Some titles run very long (p11, p15). | Vary the openers and cut fillers. Shorten the long titles (e.g. p15: "Shapes must match: inner numbers agree, outer numbers give the answer's shape"). |

## Python check
```
L[1,2] = 58 ; A x = (14, 32) ; A B = [[58,64],[139,154]] ; B A first row = (39, 54, 69), shape 3x3     OK
shear(1,3) = (4,3) ; rotation(1,3) = (-3,1) ; scale(1,3) = (2,3) ; det: shear 1, rot 1, scale 2   (S3-12)
W1 x = (7,-1,4,4) ; y1 = (7.5,-1,3,4.5) ; W2 y1 = (10.5,8) ; y2 = (10.5,9)                            OK
W2 W1 = [[3,1,2],[-2,3,1]] ; W2 W1 x = (11,7) = W2 (W1 x)                                            OK
X W (token example) = [[3,2,1],[1,3,0],[2,2,2],[2,3,1]] ; gold entry (1,2) = 2                         OK
params: 26 ; 1,001,000 ; 4096^2 = 16,777,216 ; 4096^3 = 68,719,476,736 ; 7e9*2 B = 14 GB (13.04 GiB)   OK
exit: (1,2;3,4)(1,1) = (3,7) ; 10->5 layer = 55 ; hidden 5 -> 32                                      OK
recall: (1,2,3).(4,0,2) = 10 ; |(2,3,6)| = 7                                                         OK
```
No wrong numbers. The category 1 items are conventions and wording (S3-01, S3-12, S3-13).

## Cross-session notes
- **Assumes from earlier sessions:** the dot product and norm (S2, recalled, good) and the bias b (S1). It also assumes "vector = column", which S2 did not set up (S3-08). "Token" and "embedding" are defined again in the notes, which is good, but p24 does not define "token" on the slide itself.
- **Hands to later sessions:**
  - S4 receives the identity (used for the inverse) and should recall it. The area-scaling seed (shear and rotation keep area, scale doubles it) is a free lead-in to the S4 determinant.
  - S9 (Jacobian, "multiplies by J transposed") and S18 (QKᵀ) depend on the row and column convention. Settle S3-01 and S3-08 here, or the transpose in S9 and S18 will look arbitrary.
  - S11 is promised for the activation function (outline S11 has "Sigmoid"). Check that S9 and S10 do not use activations before S11.
- **Facilitator materials (all sessions):** `Facilitator Materials/` contains Solution Notebooks but no solution workbooks. A facilitator helping a spreadsheet learner has no model answer file (it exists only as `content/labs/sNN_xl.py` with `solution=True`). Ship `Solution Workbooks/` next to the notebooks.
