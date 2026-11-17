# Audit: Session 14, Distributions and sampling

**Verdict.**
The arithmetic holds throughout. The binomial (0.2668), the normal areas (0.9332, 0.6827), SE 0.3118, the CI of the 60 rolls (3.515 to 4.418, t version 3.506 to 4.428), the A/B test (z 2.060, p 0.0394, gap interval 0.0010 to 0.0390), the temperature rows, top-p 0.4992 and the eight draws all recompute. The one wrong set of numbers is in the facilitator lab steps.
The session is badly overloaded: 23 concept slides in a 35 minute concept block, covering Bernoulli, binomial, Gaussian, multivariate Gaussian, the covariance matrix, LLN, CLT, SE, CI, A/B testing, p-values, sampling, temperature and top-p. A newcomer cannot absorb that in one sitting.
Newcomer gaps: "independent" is used before S15 defines it, the factorial n! is never defined, and 1.96 is never tied to the "95% within 2 sigma" picture. Two notations also clash on the page: Gaussian(μ, σ²/n) puts the variance second, while Normal(60, 10) puts the standard deviation second.

Files read: `Build/content/s14.py`, `Class Slides PDF/14 - Distributions and sampling.pdf` (38 pages, all viewed; slide 12 zoomed), the learner and solution notebooks, `Workbooks/Session 14 - Distributions and sampling.xlsx`.

## Findings

| ID | Where | Cat | Sev | What is wrong | Fix |
|---|---|---|---|---|---|
| 14-1 | Whole deck (slides 7 to 29, plus the 35 minute clock) | 2, 4 | High | 23 concept slides and about 14 new ideas in 35 minutes, roughly 1.5 minutes per idea. That breaks the guide's "12 to 16 concept slides" and means a newcomer gets no hand example for most of them. | Cut or move material. (a) The multivariate Gaussian and covariance matrix (slides 12 and 13) repeat S5 and S6, so make them one recall slide. (b) The temperature formula is taught again in S17 (s17.py slide 12, "The second line adds a temperature T"), so keep temperature and top-p here and turn S17's slide into a recall, or the reverse. (c) Consider giving A/B testing more room in place of the binomial formula slide. |
| 14-2 | Facilitator lab_steps, Stage 6 | 1 | Medium | "Renormalised 0.4995, 0.3349, 0.1657." The correct values are 0.4992, 0.3346, 0.1662, matching slide 27 and the notebook check of 0.4992. The figures were computed from probabilities rounded to three decimals. | Replace them with 0.4992, 0.3346, 0.1662. |
| 14-3 | Slides 8 (title), 6 (words), 15, 16 | 2, 3 | High | "n independent Bernoulli trials" and "averages of many independent values" rely on independence, which S15 (slide 10) defines for the first time. A newcomer has no definition here. | Add a one-line definition on slide 8: "Independent: the result of one trial does not change the probability of another (two dice, two users)." Then S15 can recall it. |
| 14-4 | Slide 9 (binomial formula) | 3 | Medium | "n! / (k! (n-k)!)": the factorial is never defined in the course before this slide, and the (n over k) bracket notation is new too. | Add a row: "n! (n factorial) = n × (n-1) × ... × 1, for example 3! = 6", and show 10!/(3! 7!) = 120 worked out. |
| 14-5 | Slide 16 vs slide 32 (check table) and the Normal sheet | 3 | Medium | The CLT line writes Gaussian(μ, σ²/n), with the variance as the second number. The check table writes "Normal(60, 10)", with the standard deviation as the second number. NORM.DIST also takes the standard deviation. A newcomer will read σ²/n as a standard deviation. | Choose one convention and state it. For example, write "Gaussian with mean μ and standard deviation σ/√n" on slide 16, and "Normal(mean 60, sd 10)" in the check table. |
| 14-6 | Slides 10, 17, 18 | 2, 3 | Medium | Slide 10 says "95% within 2 sigma", while the CI slides use 1.96 without saying where it comes from. That explanation exists only in the facilitator probe. | Add a line to slide 18: "1.96 is the exact 2 sigma: 95% of a Gaussian lies within 1.96 standard deviations." |
| 14-7 | Slide 13 (covariance matrix) and slide 18 (CI) | 1, 2 | Medium | Slide 13 says "this course divides by n", contradicting S5's n - 1 (see 13-1). Five slides later the CI uses the sample s with n - 1. Two conventions sit in one deck with no bridging sentence. | On slide 18, say: "For a confidence interval we estimate σ from a sample, and statisticians divide by n - 1 here (STDEV.S)." Fix the S13 statement as in 13-1. |
| 14-8 | Slide 12 (multivariate Gaussian) | 3, 1 | Low | The 150 simulated points include impossible values: scores above 10 on a "quiz score out of 10" axis, negative study hours, and a score near 0. The notes also say "red arrows ... along the long and short axes", but the slide text speaks of one "Red arrow". | Clip or rescale the simulation, or relabel the axes as an illustrative Gaussian, not scores. Match "arrow" and "arrows". |
| 14-9 | Slide 13 visual | 5 | Low | The gold cell highlights the 4.667 variance only, which marks nothing in particular. | Highlight both diagonal cells (the variances) or the off-diagonal pair, matching the bullets. |
| 14-10 | Slide 23 (p-value compare) | 3 | Medium | The "A p-value is not" column ends with "Proof: test 20 useless features and about 1 passes at p < 0.05 by luck". That is a separate warning (multiple testing), not a misreading. The 0.05 threshold is also used here for the first time and never introduced as a convention. | Put the 20-tests line in the verdict or on its own line, headed "Testing many features". Introduce "a common (arbitrary) threshold is p < 0.05" on slide 20. |
| 14-11 | Slide 10 figure | 3 | Low | The "95% within 2 sigma" arrow points into the light band between 1σ and 2σ only. | Bracket the whole band from -2 to 2. |
| 14-12 | Slide 11 note, notebook Step 0 | 3 | Low | "math.erf in Python gives the areas": erf is a black box, and the formula Φ(z) = ½(1 + erf(z/√2)) is never shown on a slide. | Show the one-line Phi definition on slide 11, or on the bridge slide, as "the area to the left of z". |
| 14-13 | Notebook Step 3 (running average) and Step 6 (top-p, draws) | 6 | Medium | The learner TODOs need `np.cumsum`, `np.argsort`, `np.searchsorted` and a list comprehension, none of which appears on the bridge slide. Step 6 asks for `k`, `p_nuc` and `tea_counts` from a one-line hint. That is too steep for newcomers. | Add cumsum and searchsorted to the bridge slide, give `cum = np.cumsum(p1)` as starter code, or pre-write a `draw(p)` helper and leave only the counting as the TODO. |
| 14-14 | Notebook Step 4 cell 24 | 6 | Low | One TODO cell holds seven unknowns (CI and A/B test) with no intermediate checks. A wrong `pooled` only shows up as a wrong z. | Split it into two cells (CI, then A/B), with a check on `pooled` and `se_ab`. |
| 14-15 | Workbook Sampling sheet | 6 | Low | The standard deviation of the 12 averages is 0.3589, while the formula SE is 0.3118. The sheet and Start here never say why they differ, which is that only 12 samples are used. | Add a note: "12 averages are too few to show 0.3118 exactly. The notebook's 20,000 give 0.311." |
| 14-16 | Workbook Binomial sheet | 6 | Low | `B4:B14` already holds `BINOM.DIST(k,10,0.3,FALSE)` for every k, so the gold cell "P(X=3) with BINOM.DIST" can be copied from B7. | Leave B4:B14 for the learner, or make the gold cell the COMBIN formula only. |
| 14-17 | Notes, whole deck | 5 | Medium | 16 of 30 notes open with "Here is/are/Now/Let us". "just" appears 9 times, and "simply" and "actually" also appear. | Vary the openers and remove the fillers. |
| 14-18 | Slide 34 card | 1 | Low | "Above T = 0, words are drawn at random" is fine, but the card reads as if T = 0 is fully deterministic. The facilitator note correctly hedges that it is not always. | Add "(T = 0 is usually, not always, repeatable)". |

### Python checks (category 1)
```
binomial(10,0.3): [0.0282 0.1211 0.2335 0.2668 0.2001 0.1029 0.0368 0.009 0.0014 0.0001 0.0]; P(X<=3)=0.6496; sd=1.4491
Phi(1.5)=0.93319; Phi(1)-Phi(-1)=0.68269
60 rolls: mean 3.96667, s(n-1)=1.78474, SE=0.230409, CI 3.5151..4.4183; t(59)=2.00100 -> 3.5056..4.4277
A/B: pA .12, pB .14, pool .13, SE .0097082, z 2.06010, p two-sided 0.039389 (one-sided 0.019694)
     unpooled SE .0097040, gap CI 0.00098..0.03902
softmax T=0.5 [0.6278 0.2821 0.0696 0.0172 0.0035]; T=1 [0.4459 ...]; T=2 [0.3252 0.2663 0.1876 0.1322 0.0886]
   e^1.5=4.48169, sum e^(z/2)=13.78022 -> 0.3252; T=0.2 tea 0.8775
cumsum T=1: 0.4459 0.7448 0.8932 0.9669 1.0; top-p 0.8 renorm [0.49920 0.33463 0.16617]  (facilitator says 0.4995 0.3349 0.1657: wrong)
top-p 0.95: 4 words, tea 0.4612
u (seed 19) = .420 .926 .274 .060 .311 .718 .781 .539 ; tea counts T=1/0.5/2 = 4/5/3 (matches slide 28 and notebook)
cov matrix eig = 1.5064, 10.1603; SE(30)=0.311805; simulated sd of 20,000 means (seed 14)=0.31074
first 12 averages: mean 3.39722, sd 0.35887 (matches workbook check)
```
Facts checked: Holtzman et al. (nucleus sampling, ICLR 2020), correct. Kohavi, Tang and Xu (2020 book), correct. temperature and top_p in the OpenAI, Gemini and Anthropic APIs and top_k in some, correct and phrased by name only.

## Cross-session notes
- **Assumed but not taught:** independence (S15), the factorial, the (n over k) notation, and a CLT-based "95%" figure (1.96).
- **Duplicates:** the multivariate Gaussian and covariance matrix duplicate S5 and S6. Temperature softmax is taught again almost word for word in S17 (slides 12 and 27) with no recall of S14.
- **Conflict:** the divide-by-n claim versus S5 (n - 1), and the sample s (n - 1) inside this same deck.
- **Hands forward:** the binomial value 0.2668 is reused by S16 (7 heads at p = 0.7, by symmetry), which works. The Gaussian density and "many small effects" are used by S16's Gaussian noise. The Bernoulli feeds S16's cross-entropy. S17 should open its temperature slide with "Recall Session 14".
