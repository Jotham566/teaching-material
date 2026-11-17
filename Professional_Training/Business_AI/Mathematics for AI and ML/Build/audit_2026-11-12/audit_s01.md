# Audit: Session 1, Functions, notation and logarithms

Sources read: `Build/content/s01.py`, `Class Slides PDF/01 - Functions and logarithms.pdf` (all 29 pages viewed), learner and solution notebooks, `Workbooks/Session 01 - Functions and logarithms.xlsx` (formulas read with openpyxl), `Build/content/labs/s01_xl.py`.
Slide numbers are PDF page numbers (pN). PDF page = outline slide index + 4.

## Verdict
1. Every number is correct, and the session builds cleanly from Σ to f(x) = wx + b to exp/ln to the product rule and log-probabilities. It is the strongest of Sessions 1 to 3.
2. The main weaknesses are for newcomers. The letter b means three different things across four slides. "Loss" is used before it is defined. Two different "averages of minus ln p" (entropy and per-word loss) sit side by side with nothing to tell them apart.
3. The labs match the slides number for number. The learner notebook asks for np.prod (and the workbook for PRODUCT) without showing it anywhere, and one CHANGE prompt refers to a variable that the learner cell does not contain.

## Findings

| ID | Where | Cat | Sev | What is wrong | Recommended fix |
|---|---|---|---|---|---|
| S1-01 | p9, p12, p14 | 3 | Medium | The letter b changes meaning without warning: "b: the bias (intercept)" (p9), then "b: the base" in log_b (p12), then "a and b: any two numbers above 0" (p14). | Keep b only for the bias. On p12 write the base as a different letter, e.g. `log_B(y) = x ⇔ B^x = y`, or say "here b is the base, not the bias". On p14, use `ln(m × n)` or `ln(u × v)`. |
| S1-02 | p13 (point 3), notebook Step 4 intro | 2 | Medium | "Training uses it for the correct word as the loss." The word "loss" is not defined until p26. | Add "(the loss: the number training tries to make small; p26 shows it)", or move the sentence to p26. |
| S1-03 | p20 line 4, p22 step 5, p23 row 5, notebook Step 5 vs Step 6c | 3 | Medium | There are two different "averages of minus ln p". One is Σ p·(−ln p) = 1.133 over the five candidate words, called "the average ... weighted by p" and "the entropy". The other is the plain mean over six sentence positions, 0.8763, called "the training score" and, on p26, "cross-entropy". Nothing tells the newcomer they are different quantities. | Name them on the slides: "weighted by p over the candidates = entropy (Session 17)" and "plain average over the words of a real text = the training loss (cross-entropy, Session 17)". Use the word "average" for only one of them. |
| S1-04 | p20 line 4, notebook Step 5 | 1 | Medium | 1.133 is called "the entropy" without its unit. It is in nats (natural log). Session 17 computes entropy in bits (outline S17 slide 5: "1.75 bits"). The same distribution in bits is 1.634. A learner who compares the two will think one is wrong. | Add "(in nats, because we used ln; Session 17 uses log base 2 and bits)". |
| S1-05 | p10, p12, p4 (Words) | 1 | Low | "e = 2.71828" is written as an equality. e is irrational. | Write "e ≈ 2.71828 (about 2.718)". |
| S1-06 | p10 | 3 | Low | The graph plots 2⁰ = 1, but "x copies of 2 multiplied together" gives no meaning for x = 0 or for fractional x. | Add one line: "2⁰ = 1 by definition: each step left halves the height, so 2⁰ = 2¹ ÷ 2 = 1." |
| S1-07 | p14 | 2 | Low | The power rule ln(aᵏ) = k ln a is stated with k = 2 but never worked, and it is not used again in this session. | Add a worked example (ln 9 = 2 ln 3 = 2.1972), or drop it to the facilitator rescue as the deck already allows. |
| S1-08 | p28 (exit check) | 3 | Low | "the sum from i = 1 to 3 of p_i, when p_1 = 0.5 ..." uses raw underscore notation, which was never shown. | Use subscripts (p₁, p₂, p₃) or write the Σ form as on p6. |
| S1-09 | p8 | 3 | Low | The label "(0, 1)" overlaps the line and the gold dot. | Move the label left or above the point. |
| S1-10 | notebook Step 2 (learner) | 6 | Medium | The CHANGE prompt says "Change w to 3 in your cell", but the learner cell is only `answer = None` and contains no w, b or x. Only the solution defines w = 2, b = 1, x = 3. | Put `w = 2`, `b = 1`, `x = 3` in a given cell above the TODO, and make the TODO `answer = None  # use w, x and b`. |
| S1-11 | notebook Step 6a, workbook B33 | 6 | Medium | The learner must multiply six numbers, but np.prod (Python) and PRODUCT (spreadsheet) appear on no slide, in no recipe line and in no hint. A newcomer will type six multiplications or get stuck. | Add `np.prod(word_p)` / `=PRODUCT(B27:B32)` to the p20 recipe, or to the hint text. |
| S1-12 | workbook Check sheet | 6 | Low | Step 4 checks only C5 (Kampala) and C9 (Nairobi). C6 to C8 can be wrong and still pass. | Check all five, or check the column sum (Σ −ln p = 10.528). |
| S1-13 | workbook Work C27:C32 | 6 | Low | LN(p) for the six words is pre-filled, so Step 6b is only a SUM. The notebook makes the learner take the logs. | Make C27:C32 gold, so both tracks do the same work. |
| S1-14 | workbook Work layout | 6 | Low | The Step 4 instruction sits in E4 inside the Step 1 block, above Steps 2 and 3. The order on the sheet is 1, 4, 2, 3, 5. | Put a "Step 4" label in C4, or move the minus-LN column below Step 3. |
| S1-15 | notes, 19 of 24 | 5 | Low | 19 of 24 notes end on a question. 7 start "Here is". The notes contain "simply", "just" ×3, "really" ×2, "the key property", "Imagine a model", and "That is no accident". | Vary the endings (end about half on a statement). Cut the fillers and "Imagine". |
| S1-16 | p25 | 4 | Low | The claim "Open models publish vocabularies of 32,000 to over 250,000 tokens" is true (Llama 2 has 32,000; Gemma has 256,000) but names no model. | Name them: "e.g. Llama 2: 32,000; Gemma: 256,000". |

## Python check (category 1 and all worked numbers)
```
sum p = 1.0
-ln p = [0.478 1.7148 2.3026 2.8134 3.2189]            (slides: 0.478 ... 3.219, OK)
sum p*(-ln p) = 1.1329 nats ; same in bits = 1.6344        (slides: 1.133, unit not stated -> S1-04)
ln2, ln3, ln6 = 0.6931, 1.0986, 1.7918 ; ln5 = 1.6094      (OK)
sentence product = 0.005208 ; sum ln = -5.25756 ; avg = 0.87626   (OK; perplexity e^0.876 = 2.40)
rounded terms sum to -5.257 (slide note says terms are rounded, OK)
1000*ln0.2 = -1609.438 ; log10(0.2^1000) = -698.97 -> "about 10^-699" OK ; np.prod -> 0.0
0.5^1000 = 9.33e-302 (does not underflow), 0.5^2000 = 0.0 -> the notebook CHANGE prompt works as intended
smallest normal double 2.2e-308 ("about 10^-308" OK)
ln .5/.1/.01 = -0.693, -2.303, -4.605 (OK) ; -ln 0.9 = 0.105 (answer key OK) ; ln12 - ln3 = ln4 (OK)
```
No wrong numbers found.

## Cross-session notes
- **Assumes:** nothing beyond high school algebra. Good.
- **Hands to later sessions:**
  - S2 and S3 reuse Σ, the bias b and f(x) = wx + b. Fix S1-01 so that b reaches S3 meaning "bias" only.
  - S12 (outline slide 17) re-teaches underflow with the same idea. S12 should recall S1's 1000-word example rather than rebuild it.
  - S17 needs the S1 numbers to carry over. Say now that 1.133 is entropy in nats and 0.876 is the per-word cross-entropy of a real sentence, and that perplexity = e^0.876 ≈ 2.40. This gives S17 a ready recall hook.
  - S14 (temperature) and S17 (softmax) will need exp of negative numbers. Optionally add one point on p10: e⁻¹ ≈ 0.37, and eˣ is always positive.
