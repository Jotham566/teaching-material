# Audit: Session 17, Information theory

**Verdict.** All numbers are correct (entropy 1.75, cross-entropy 2.000 and 1.8007, KL 0.250 and 0.0507, softmax 0.659, 0.242, 0.099, loss 1.417, perplexity 5.21), and the claims about AI products are phrased as the guide requires.
The deck teaches the softmax, temperature and the stable softmax as new, with no recall of Sessions 12 and 14 where they were taught. It does not deliver the log-softmax link that Session 12 promised, and it derives only the softmax gradient, which Session 18 needs in its sigmoid form.
One misleading statement ("a fair coin is the hardest to predict" next to a 1.75-bit distribution), a dense unproved derivation step, and a workbook gradient check that breaks under its own CHANGE.

## Findings

| ID | Where | Cat | Sev | What is wrong | Fix |
|---|---|---|---|---|---|
| 17-1 | Slides 16 to 18, 32; words slide | 2 | Medium | The softmax is listed as a new word and taught from scratch. Temperature (taught in S14, with the same T = 0.5 / 2 demo) and the stable softmax (S12 slides 14 and 15, with the same 1000, 1001, 1002 example) are repeated with no recall. Session 17 cites no session before 16. | Open the softmax part with "You met the softmax with temperature in Session 14 and its stable form in Session 12. Today we add its gradient." Cut the repeated stable-softmax example to one line. |
| 17-2 | Whole deck vs S12 slide 16 note | 2 | Medium | S12 says "Cross-entropy (Session 17) ... is computed from log-softmax this way" (log-sum-exp). Session 17 never shows loss = logsumexp(z) - z_true. The workbook (Softmax!B12) then needs exactly that identity. | Add one line on slide 21: "-ln p_true = ln(sum of e^z) - z_true, the log-sum-exp of Session 12". |
| 17-3 | Slide 9 lead and title | 1 | Medium | "A fair coin is the hardest to predict: 1 bit" sits beside a four-word distribution with 1.75 bits, which is harder to predict. The title says entropy "is largest when the outcome is hardest to guess". A newcomer gets two conflicting messages. | "Among two-outcome distributions the fair coin is hardest to predict (1 bit). With K equally likely outcomes the entropy is log2 K (2 bits for 4 words)." |
| 17-4 | Slide 20 (derivation) | 3 | Medium | The step dp_k/dz_j = p_k(delta_kj - p_j) is stated with no derivation or check. It needs the quotient rule (S7) and the chain rule with a sum (S9). For a newcomer it is the step that makes or breaks the result. | Add the two cases with numbers: dp1/dz1 = p1(1 - p1) = 0.659 × 0.341 = 0.225, and dp2/dz1 = -p2 p1 = -0.160. Or show a finite-difference check of one entry. |
| 17-5 | Workbook Softmax!B12:B13 | 6 | Medium | The perturbed loss `=LN(EXP(B4+0.001)+EXP(C4)+EXP(D4))-C4` ignores the temperature T in B10, while B11 uses the T-dependent p. After the sheet's own CHANGE (T = 0.5) the "numeric gradient" B13 is meaningless. The learner also has to invent the log-sum-exp identity, which the slides never show. | Give B12 as a given formula that divides by $B$10. Or build a second shifted-softmax row with logit 1 + 0.001 and take -LN of its class-2 entry. |
| 17-6 | Hand-off to S18 (Build 2 and Build 4) | 2 | Medium | S18 says the sigmoid with binary cross-entropy gradient p - y was "already derived in Session 17". S17 derives only the softmax version and never says that a sigmoid is a 2-class softmax. | Add one line or a small box: "With two classes the softmax is the sigmoid of z1 - z2, so sigmoid + binary cross-entropy also gives p - y." |
| 17-7 | Notebook Step 3 checks | 6 | Low | Expected 1.8006 and 0.0506. True values are 1.80069 and 0.05069, and the slides say 1.8007 and 0.0507 (pass only through the 0.0005 tolerance). | Use 1.8007 and 0.0507. |
| 17-8 | Slides 6, 8, 21; S16 keep | 3 | Low | Entropy, cross-entropy and KL are in bits, while the loss and perplexity are in nats. S16's cross-entropy 0.299 was in nats and is never converted. | Add a one-line bridge: "Session 16's 0.299 nats is 0.431 bits". |
| 17-9 | Slides 16 vs 19 | 3 | Low | The same logits are labelled cat, dog, fox on slide 16 and class 1, 2, 3 on slide 19. "Class 2 true" is dog, but this is unstated. | Keep the labels cat, dog, fox and say "dog is the true word". |
| 17-10 | Slide 20 (delta_kj) | 2 | Low | delta_kj (the Kronecker delta) shares the letter with S11's "delta" error signal and S18's delta = p - y, with no warning. | "Not the delta of backpropagation: here delta_kj is just 1 or 0." |
| 17-11 | Slide 32 notes | 1 | Low | "That is why the same question can give different answers" follows the temperature picture. The variation comes from random sampling at any T > 0. Temperature only sets how much. | "Sampling is random, so answers can differ. Temperature sets how much they differ." |
| 17-12 | Notes throughout | 5 | Medium | 11 of 29 notes open "Here is/are". "Here is the key picture" (slide 14), "beautifully simple" (slide 19), "simply the prediction minus the target" (outcome note), "really" 3 times, "just" 4 times. | Lead with the content. Delete the intensifiers. |

### Python check (category 1 numbers)
```
H(P) = 1.75 ; H(0.9,0.1) = 0.46900 ; H(0.99,0.01) = 0.0808
CE A = 2.0 ; CE B = 1.800687 ; KL A = 0.25 ; KL B = 0.050687 ; KL(Q_B||P) = 0.0536 (asymmetry claim ok)
3 bits = 2.0794 nats ; 1 bit = ln2 = 0.6931 nats
softmax(2,1,.1) = 0.659001, 0.242433, 0.098566 ; sum e^z = 11.213 ; T=0.5 -> 0.8638 ; T=2 -> 0.5017
stable (1000,1001,1002) -> 0.0900, 0.2447, 0.6652 ; e^-2+e^-1+1 = 1.5032
loss -ln 0.2424 = 1.41703 nats (2.0443 bits) ; grad p-y = (0.6590, -0.7576, 0.0986)
nudge logit 1 by 0.001: loss rises 0.000659 (slide 0.00066 ok)
sentence -ln p sum 9.9035, mean 1.65058, PPL 5.2100 ; e^2 = 7.389
```
All correct. API temperature statement and "published research" phrasing comply with the guide.

## Cross-session notes
- **Assumes:** S1 (ln, log2), S7 (quotient rule, for the unproved dp/dz), S9 (chain rule with several paths), S12 (stable softmax, log-sum-exp), S14 (softmax with temperature), S15 (conditional probability in the perplexity formula) and S16 (cross-entropy loss). Only S16 is recalled.
- **Hands to S18:** p - y for softmax. S18 needs it for **sigmoid** + binary cross-entropy (Builds 2 and 4). Make that link here (17-6).
- S1 promised entropy "Session 17", and the session delivers it. S12 promised the log-softmax link, and the session does not deliver it (17-2).
