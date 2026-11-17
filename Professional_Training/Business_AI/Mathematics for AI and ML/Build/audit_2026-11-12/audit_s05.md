# Audit: Session 5, Eigenvalues and eigenvectors (deck 33 pages, notebook, workbook)

**Verdict.**
1. The worked numbers are all correct: eigenvalues 3 and 1, C = (66, 48; 48, 38), eigenvalues 102 and 2, e₁ = (0.8, 0.6), 98.1 percent, and the power iteration tables. The notebook (17 checks) and the workbook (22 checks) match the slides.
2. Two statements are wrong or inconsistent. The notes say "a 2 by 2 matrix has at most two such directions". The deck defines variance as an "average" but divides by n − 1 without saying why, before Session 13 teaches variance.
3. The order is good: picture, definition, test, characteristic equation, data, covariance, eigenvectors, power iteration. The notebook's check helper can falsely report "All checks pass" (reproduced: 10 of 17).

## Findings

| ID | Where | Cat | Sev | What is wrong | Fix |
|---|---|---|---|---|---|
| S5-L1 | Notebook cells 21, 24, 34, 44 (learner) | 6 | High | The print lines (`np.round(vectors, 4)`, `round(share, 3)`, `C_flip[0, 1]`) crash with TypeError while the answer is `None`, so the checks in those cells never register. When steps 3, 5 and the step 6 change are skipped, `show_checks()` prints **"All 10 checks pass"** (the full set is 17; reproduced). | Same kit fix as S4-L1: an expected count in `show_checks`, and guarded prints. |
| S5-1 | Slide 9 notes ("Testing four arrows") | 1 | Medium | The notes say "A two by two matrix has at most two such directions, and a symmetric one like this has exactly two". This is false for any multiple of the identity (2I keeps every direction) and for any symmetric matrix with a repeated eigenvalue. | Say "at most two different eigenvalues; when the two eigenvalues differ, there are exactly two directions". |
| S5-2 | Slide 6 (Words) vs slides 16 and 17 | 1/3 | Medium | Words: variance is "its average squared distance from its mean". Every calculation then divides by n − 1 = 7 (462/7 = 66, while the average is 57.75). The slide says only "as np.cov does" and gives no reason. Session 13 later teaches dividing by n as the default. | On slide 16, add one sentence: "Dividing by n − 1 (the sample version) instead of n corrects a small underestimate when the mean comes from the same data; Session 13 returns to this. With n the numbers would be 57.75, 42 and 33.25, and the eigenvectors would not change." Reword the Words entry as "the typical squared distance from the mean". |
| S5-3 | Slide 11 (A − λI has no inverse) | 3 | Medium | The key step "if A − λI had an inverse, v would have to be 0" is only in the notes. On the slide, "So A − λI must have no inverse" does not follow for a reader working from the PDF. | Add to the caption: "If A − λI had an inverse, multiplying (A − λI)v = 0 by it would give v = 0." |
| S5-4 | Slide 18 (cloud figure, "principal component 1") | 2/3 | Medium | "Principal component" is used as a label and in the bullets before it is defined. It is not in the Words list, and it is first explained on slide 29. | Add one line: "The direction of greatest spread is called the first principal component (PCA, next session)." |
| S5-5 | Slide 20 (power iteration formula) | 1/3 | Low | "λ ≈ max\|A gₖ\|" holds only because gₖ is scaled so that its largest entry is 1, and it loses the sign of a negative top eigenvalue. The start g₀ = (1, 0) here and g₀ = (0, 1) on slide 22 can look like a contradiction. | Add "(because gₖ has largest entry 1)". Say that slide 22 starts elsewhere on purpose: any start works. |
| S5-6 | Slide 12 (determinant expansion) | 3 | Low | The step "(2 − λ)(2 − λ) − 1 = λ² − 4λ + 3" skips the expansion 4 − 4λ + λ² − 1. | Show the middle line. |
| S5-7 | Slide 17 ("Sums") | 3 | Low | "Maths squared 462" could be read as the raw marks squared. | Write "Sum of squared centred maths marks: 462". |
| S5-8 | Slide 7 (e₁, e₂) | 3 | Low | e₁ and e₂ conventionally name the axis vectors (1, 0) and (0, 1). Using them for eigenvectors may clash with later reading. | Use v₁ and v₂, as slide 8 does. |
| S5-9 | Slide 22 (power iteration table) and notes | 1 | Low | The notes say convergence needs "one eigenvalue that is clearly the largest... That is the case for the covariance matrices we care about." This is not guaranteed, because a round cloud has equal eigenvalues. | Write "usually the case; when two eigenvalues are nearly equal, it converges slowly". |
| S5-10 | Workbook Work B42:C42 | 6 | Low | The top eigenvector is given as (C31, λ − B31) with no reason, while the slides derive it differently (t = 0.75s). | Add a note: "From row 1 of (C − λI)v = 0: (66 − λ)s + 48t = 0, so (s, t) = (48, λ − 66)." |
| S5-11 | Slide 31 (assistant activity) | 5 | Low | The output box presumes that the assistant "used a different sign". | Write "and any sign differences". |
| S5-12 | Slide 11, steps icon | 5 | Low | The "Start" icon renders as a plain gold dot (same as Session 4, slide 26). | Fix or drop it. |
| S5-13 | Notes | 5 | Low | "Here is" ×6, "Let us" ×3, "exactly" ×6, "Now the payoff". 13 of 32 notes end on a question. | Vary the openers and cut "exactly". |
| S5-14 | Deck length | 2/4 | Low | 17 concept slides in a 35-minute block, with two full worked chains (A, then C). | Tag the four-arrow table (slide 9) and slide 21 as optional. The facilitator rescue plan already partly does this. |

## Category 1 checks (Python, numpy)
```
A=[[2,1],[1,2]]: T=4, D=3, λ²-4λ+3 -> 3, 1; A(1,1)=(3,3), A(1,-1)=(1,-1), A(1,0)=(2,1), A(1,2)=(4,5)   ok
maths 53,55,63,67,48,67,56,71 mean 60; phys 53,52,62,65,49,61,57,65 mean 58
centred: -7,-5,3,7,-12,7,-4,11 / -5,-6,4,7,-9,3,-1,7
Σ ca²=462, Σ cb²=266, Σ ca·cb=336; /7 -> 66, 38, 48 (np.cov ddof=1)  [/8 would give 57.75, 33.25, 42]
T=104, D=66·38-48²=204, √(104²-816)=√10000=100, λ=102, 2
(C-102I) row1: -36s+48t=0 -> (4,3)/5=(0.8,0.6); e2=(0.6,-0.8); 102/104=0.98077
Power on A from (1,0): estimates 2.00, 2.50, 2.80, 2.93, 2.98; g1=(1,0.5), g2=(1,0.8)   ok
Power on C from (0,1): 48.00, 104.00, 102.04, 102.0008, 102.00001, 102.0000003; guess -> (1, 0.75)   ok
100 - phys: cov -48, eigenvalues 102, 2   ok
Counterexample to S5-1: eig(2I) = (2, 2), with every vector an eigenvector.
Solution notebook "All 17 checks pass"; workbook solution formulas match.
```

## Cross-session notes
- **Assumes:** Session 4 (the determinant is 0 exactly when there is no inverse, recalled correctly) and Session 3 (identity, matrix times vector). Mean, variance and covariance have not been taught yet. Session 13 is where they belong, so this deck must teach them inline (it does, briefly) and should flag the n versus n − 1 choice (S5-2).
- **Hands on:** C, 102 and 2, and (0.8, 0.6) are reused in Session 6 for PCA, and the recall covers them. Power iteration is reused in Session 6 for σ₁. Consider a one-line forward link to Session 13: "variance and covariance, properly, in Session 13".
