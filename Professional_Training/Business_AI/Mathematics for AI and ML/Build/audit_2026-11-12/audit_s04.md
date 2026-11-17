# Audit: Session 4, Solving linear systems (deck 32 pages, notebook, workbook)

**Verdict.**
1. Every number on the slides, in the notebook and in the workbook is correct and the three agree (15 notebook checks and 14 workbook checks pass with the solution).
2. The flow from lines, to Ax = b, to the inverse, the determinant, rank and least squares is sound. The weak points are notation clashes (x, b, w) with Sessions 1, 3, 8 and 10, and two steps the PDF skips: back substitution, and why multiplying by Xᵀ gives least squares.
3. One check-helper bug: the notebook can print "All N checks pass" with work missing. This affects the whole course (see S4-L1).

## Findings

| ID | Where | Cat | Sev | What is wrong | Fix |
|---|---|---|---|---|---|
| S4-L1 | Notebook cells 12, 24, 27 (learner) | 6 | High | The print lines run before `check()` and crash with TypeError when the answer is still `None` (`A_inv[0, 0]`, `"{:.2f}".format(w[0])`, `format(sse)`). The checks in that cell then never register. If a learner skips cells 23 and 26, `show_checks()` prints **"All 8 checks pass"**, but the full set is 15 (reproduced). | In kit/nb.py, give `show_checks(expected=N)` the total and print "N of M" against it. Guard every print with `None if x is None else ...`, as Session 6 already does. |
| S4-1 | Slides 7 to 16, then 17 to 22 | 2/3 | Medium | Notation changes without warning. **x** is first the vector of unknowns (x₁, x₂), then X is the data (spend) and **w** holds the unknowns. **b** is the right-hand side here, but it was the bias in Session 1 (f(x) = wx + b) and Session 3 (y = Wx + b), and it is the intercept again in Sessions 8 and 10. The intercept is w₀ here, while Sessions 8 and 10 call it b. | Add one line on slide 17: "From now on the unknowns are the weights w, and X holds the data; x and b on the earlier slides were the general names in Ax = b." In the closing notes, map w₀ → b and w₁ → w for Session 8. |
| S4-2 | Slide 10 (elimination) | 3 | Medium | The figure stops at "row 2 now says x₂ = 1". The back substitution that gives x₁ = 2 appears only in the notes, yet the caption claims the slide shows "back substitution reads upwards". | Add a fourth panel or a line: "Row 1: 2x₁ + 1 = 5, so x₁ = 2." |
| S4-3 | Slide 11 (inverse formula) | 3 | Medium | `A⁻¹ = 1/det A × (swap a₁₁, a₂₂; negate a₁₂, a₂₁)` is an instruction in words, not a matrix. A newcomer cannot see where each entry goes. | Show the matrix: rows (a₂₂, −a₁₂) and (−a₂₁, a₁₁), all divided by det A. |
| S4-4 | Slide 19 (normal equation) | 3/2 | Medium | The reason given for multiplying by Xᵀ, "makes the errors meet every column of X at right angles", is stated without support. It does not recall Session 2, where right angles mean a dot product of 0. The words "key formula" also appear in the notes. | Add: "Xᵀ(y − Xw) = 0 says that each column of X has dot product 0 with the error vector (Session 2: dot product 0 means right angles)." Then show that this rearranges to XᵀX w = Xᵀy. |
| S4-5 | Slide 20 (worked normal equation) | 3 | Medium | The formulas for w₀ and w₁ (155 × 221 − 29 × 1105, and so on) appear without showing that they come from the inverse of XᵀX (slide 11) times Xᵀy. | Add one block: "Inverse of XᵀX = (1/244) × rows (155, −29) and (−29, 7). Multiply by (221, 1105)." |
| S4-6 | Slide 29, "Where this appears in AI" | 1 | Low | "Most arithmetic in a layer is matrix multiplication (Vaswani et al., 2017)" credits the paper with a claim it does not make in those words. | Write: "Transformer layers (Vaswani et al., 2017) are built mainly from matrix multiplications." |
| S4-7 | Slides 28 and 31; workbook Start sheet | 6 | Low | "#VALUE! ... or Enter was used" and "press Ctrl+Shift+Enter in Excel" describe legacy Excel. In Excel 365, Enter spills an array, and a result range of the wrong size shows #N/A or #SPILL!, not #VALUE!. | Write: "In older Excel, confirm with Ctrl+Shift+Enter. In Excel 365 and Google Sheets, Enter works. #SPILL! means the cells below are not empty." |
| S4-8 | Workbook Check A6 and A7; facilitator answer key | 6 | Low | The labels "x is 2" and "y is 1" use y for x₂, which clashes with y = sales two steps later. | Use "x₁ is 2" and "x₂ is 1". |
| S4-9 | Notebook cells 11, 16, 34 | 6 | Low | The recipe slide shows only `solve` and `lstsq`, but learners must find `det`, `inv` and `matrix_rank` by pressing Tab. A non-coder may stall here. | Add the three names to the recipe slide, or put them in the cell comments. |
| S4-10 | Workbook Work, rows 45 to 47 | 6 | Low | The sheet asks for RMSE (B45) before the total squared error (B47) that RMSE is built from. | Swap the order, or have B45 refer to B47. |
| S4-11 | Slide 26 (lab map, step 2) | 5 | Low | The "key" icon renders as a plain gold dot. The same happens on Session 5, slide 11. | Fix the icon in the steps layout, or remove it. |
| S4-12 | Exit check, slide 31 | 5 | Low | "intercept w0" is written in plain text, while the rest of the deck uses w₀. | Use w₀. |
| S4-13 | Notes, many slides | 5 | Low | Stock openers ("Here is" ×4, "Let us", "Now the"), "exactly" ×5, "Here is the key formula of the session". | Vary the openers and cut "key" and "exactly". |

## Category 1 checks (Python, numpy)
```
A=[[2,1],[1,-1]], b=(5,1): solve -> (2, 1); det = -3; inv = [[1/3,1/3],[1/3,-2/3]]  (matches slides 11-12)
Row2 - 0.5*Row1 -> (0, -1.5 | -1.5)   ok
S=[[1,2],[2,4]]: det 0, rank 1   ok
x=1,2,3,4,5,6,8  y=14,19,27,30,38,41,52
Σx=29 Σx²=155 Σy=221 Σxy=1105  det XᵀX = 7·155-29² = 244
w0=(155·221-29·1105)/244 = 2210/244 = 9.0574   w1=(7·1105-29·221)/244 = 1326/244 = 5.4344
residuals -0.49,-0.93,1.64,-0.80,1.77,-0.66,-0.53 (bar labels on slide 18 match)
SSE 8.2787, RMSE √(8.28/7) = 1.0875, prediction at 7 = 47.098
One row (1,4): XᵀX=[[1,4],[4,16]], det 0, rank 1   ok
cond(XᵀX) = 105.5 (well conditioned; fine for the inverse route)
Solution notebook: "All 15 checks pass". Workbook formulas (MDETERM/MINVERSE/MMULT/TRANSPOSE/SUMSQ) reproduce the same values.
```
Nothing is numerically wrong.

## Cross-session notes
- **Assumes:** Session 1 (weight and bias), Session 2 (dot product, and that right angles mean a dot product of 0; this is used but not recalled), Session 3 (matrix times vector, transpose, identity). All were taught. The notation for b and x conflicts with Sessions 1 and 3 (S4-1).
- **Hands on:** the normal equation is reused correctly by Session 8 ("the least-squares line from Session 4") and Session 12 (ridge, "the normal equation from Session 4 with one change"). Align w₀/w₁ here with w and b in Sessions 8 and 10. The notes promise regularisation "in later sessions", and Sessions 12 and 16 deliver it. Rank and the determinant are needed in Session 5 (det(A − λI) = 0), and the recall covers both.
