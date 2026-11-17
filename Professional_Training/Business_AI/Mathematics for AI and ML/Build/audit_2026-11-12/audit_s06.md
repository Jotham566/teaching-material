# Audit: Session 6, SVD and PCA (deck 37 pages, notebook, workbook)

**Verdict.**
1. The numbers are right: singular values 3 and 2, the image singular values 36.85, 15.07 and 4.89, errors 8.19, 15.40, 4.54 and 6.73, PCA 102 and 2, scores, 14 lost, and LoRA 16,000. The notebook (28 checks) and the workbook (33 checks) pass with the solution.
2. The U and Vᵀ printed on slide 8 are reflections, not the "rotations" the slide calls them, and they disagree in sign with the figure on slide 7. The lab map (6 steps, σ₁ to σ₃) does not match the notebook (7 steps, no σ₃).
3. The deck is overloaded for 35 minutes: SVD, low rank, scree, power iteration, deflation, PCA, PCA as an SVD, choosing k, then LoRA. "Fine-tune", "pre-trained" and "frozen" are never defined.

## Findings

| ID | Where | Cat | Sev | What is wrong | Fix |
|---|---|---|---|---|---|
| S6-L1 | Notebook cells 15 and 24 (learner) | 6 | High | The same check-helper flaw as S4-L1 and S5-L1. `np.round(S2, 2)` crashes on `None` before its three checks register. With cell 14 skipped, `show_checks()` prints **"All 21 checks pass"** (the full set is 28; reproduced). | Kit fix in nb.py: give `show_checks` the expected count. |
| S6-1 | Slide 8 table vs slide 7 figure | 1 | Medium | The slide labels Vᵀ "First rotation" with rows (0.447, 0.894) and (0.894, −0.447), and U "Last rotation" with columns (0.894, 0.447) and (0.447, −0.894). Both have determinant −1, so they are reflections. The figure on slide 7 silently flips v₂ and u₂ to draw proper rotations, so the table and the picture disagree on the sign of v₂ and u₂. | Print the flipped pair: v₂ = (−0.894, 0.447) and u₂ = (−0.447, 0.894). Both are then rotations and A = UΣVᵀ still holds. Add one line: "U and V are rotations, sometimes with a mirror flip; tools may return the flipped version." |
| S6-2 | Lab map slide 29, check table slide 30, facilitator step 5 vs notebook | 6 | Medium | The slides say "six steps" and step 5 is "σ₁ to σ₃ and the errors, by deflation". The notebook has **7** steps (PCA by SVD is a separate step 5). Its deflation stops at σ₂ and the rank 2 error, so σ₃ = 4.89 and the rank 3 error from deflation exist only in the workbook. | Either add round 3 to notebook step 6 and renumber the lab map to 7 steps, or change the slides to say "σ₁ and σ₂ (σ₃ in the workbook)". |
| S6-3 | Notebook cell 43 | 6 | Medium | "Look at cell (4, 2) of rank1" uses counting from 1 (row 4, column 2 = 10.43, which the facilitator guide quotes). A Python learner will type `rank1[4, 2]` and get 4.23. | Write `rank1[3, 1]` (row 4, column 2, because Python counts from 0). |
| S6-4 | Slides 2, 6, 32 and 33 | 3/2 | Medium | "Fine-tune", "pre-trained", "frozen" and "trains" are used without definition. Training by gradient steps is not taught until Sessions 7 to 10. | Add a one-line definition on slide 32: "Fine-tuning: taking a model that is already trained (pre-trained) and adjusting its weights a little on new data. Frozen: left unchanged." State that B and A are learned by the training steps of Sessions 7 to 10, not computed with an SVD. |
| S6-5 | Whole concept block (slides 7 to 26, 20 slides) | 2/4 | Medium | There is too much for 35 minutes. Power iteration on an 8 by 8 matrix plus deflation (slides 18 and 19) exists mainly so the spreadsheet can work without an SVD function. It is heavy for newcomers and only loosely tied to AI use. | Make slides 18 and 19 a spreadsheet-track appendix, or move them to the lab. Keep SVD, low rank, scree, PCA, choosing k and LoRA. |
| S6-6 | Slides 8, 18 and 32 | 3 | Medium | The letter A means three things: the 2 by 2 matrix, the noisy image ("AᵀA for the noisy image A"), and LoRA's r by d matrix. | Call the image N (or M_img) on slides 18 and 19. Keep A for LoRA, as in the paper, and say "a new A". |
| S6-7 | Slide 7 ("Any matrix acts as rotate, stretch, rotate") | 1 | Low | For a matrix with negative determinant, a reflection cannot be avoided, so the title overstates the claim. | Add "(a rotation may include a mirror flip)" to the caption. |
| S6-8 | Slide 19 (deflation) | 3 | Low | "v₁v₁ᵀ" is the column-times-row product from slide 12, but it is not named as such here. | Add "(the column-times-row pattern from slide 12)". |
| S6-9 | Slide 8, Σ = diag(3, 2); slide 27, `full_matrices=False` | 3 | Low | `diag(...)` and `full_matrices=False` are not explained on the slides. | "diag(3, 2): the 2 by 2 matrix with 3 and 2 on the diagonal and zeros elsewhere." "full_matrices=False keeps only the columns of U that are needed." |
| S6-10 | Slide 26 (z-scores, Session 14) | 2 | Low | A forward reference uses a term ("spread") that has not been taught yet. | Write "divide by its standard deviation, defined in Session 14". The current wording is acceptable. |
| S6-11 | Workbook Image R25:R34 and Deflation R27 onwards | 6 | Low | The "Largest" column uses `MAX(...)`, while the slides and the notebook use max\|…\|. It gives the same results here, because M has positive entries and the deflation rounds converge either way. It is still inconsistent with the formula on the slide. | Use `MAX(ABS(...))` as an array formula, or `MAX(MAX(J25:Q25),-MIN(J25:Q25))`. |
| S6-12 | Workbook Check A14 / facilitator | 6 | Low | The rank 1 cell value 10.43 is above the 0 to 9 image scale, which may puzzle learners. | Add a note: "values can leave the 0 to 9 range; it is an approximation". |
| S6-13 | Notes | 5 | Low | "Here is/are" opens 13 of 36 notes. Also "The remarkable fact", "Here is the big idea of today", "Imagine the dots...", and "exactly" ×6. | Vary the openers and cut the slogans. |

## Category 1 checks (Python, numpy)
```
A=[[2,2],[-1,2]]: AᵀA=[[5,2],[2,8]], T=13, D=36, √(169-144)=5 -> 9, 4 -> σ=3, 2   ok
v1=(1,2)/√5=(0.447,0.894); u1=Av1/3=(0.894,0.447)   ok
numpy U=[[.894,.447],[.447,-.894]] det=-1 ; Vt=[[.447,.894],[.894,-.447]] det=-1  (reflections)
flip 2nd pair -> det(U)=det(V)=+1 and U Σ Vᵀ = A still (S6-1)
Noisy image: ‖noisy-H‖=8.185; σ = 36.85,15.07,4.89,3.46,2.30,1.92,1.15,0.39; cum σ² 0.832,0.972,... k95=2
errors rank1..4 vs clean: 15.40, 4.54, 6.73, 7.53   storage k(8+8+1): 17,34,51 (27%,53%,80%)   ok
1000×1000 rank 20: 20·2001 = 40,020   ok
Power on NᵀN, 10 steps from ones: 1357.604 -> σ1=36.846 (SVD 36.8457)   ok
Deflation: 227.11 -> 15.070; 23.889 -> 4.8877 (SVD 4.8880); errors 15.40, 4.54, 6.73   ok
rank1 1-based (4,2)=10.43; Python rank1[4,2]=4.23 (S6-3)
PCA: Xc SVD σ=26.721, 3.742; σ²/7 = 102, 2; scores -8.6,-7.6,4.8,9.8,-15,7.4,-3.8,13; Σz²=714, /7=102; lost=14=7·2   ok
LoRA d=1000 r=8: 2dr=16,000 vs 1,000,000 = 1.6%; B initialised to 0 (Hu et al. 2021)   ok
Solution notebook "All 28 checks pass"; workbook 33 checks per LibreOffice build.
```
The facts are within the guide's discipline: LoRA, Hu et al. 2021, B = 0 at the start, the low intrinsic rank hypothesis, and no claims about closed products. Eckart–Young is stated correctly.

## Cross-session notes
- **Assumes:** Session 5 (C, the eigenvalues 102 and 2, power iteration; recalled well), Session 3 (transpose, column times row), Session 1 (the Σ symbol, which the deck explicitly separates from the capital Sigma matrix: good). LoRA assumes training and fine-tuning, which come only in Sessions 7 to 10 (S6-4).
- **Hands on:** "held-out data" is defined here and should be reused when Sessions 12 and 16 discuss over-fitting. z-scores are promised for Session 14, and Session 14 does define them. The Session 7 cover note should recall that LoRA's B and A are trained by the gradient methods now starting.
