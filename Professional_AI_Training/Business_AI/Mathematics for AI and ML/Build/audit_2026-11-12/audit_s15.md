# Audit: Session 15, Conditional probability and Bayes

**Verdict.**
This is the strongest deck of the three. Every number recomputes: 0.8235, 0.70, 13.6, P(E) 0.108, posterior 0.0833, the second test 0.45, smoothed likelihoods, email posteriors 0.9955 and 0.3304, log scores -2.107 and -7.512, the unsmoothed result 1.0, the exit answer of about 9%, and the facilitator probe of 48%.
The flow is clean: counts, then conditional, then independence, then natural frequencies, then Bayes, then Naive Bayes. It has a good common-mistake slide and honest "Where in AI" slides (calibration, fluency is not truth).
The main gaps: independence arrives here although S14 already relied on it, and Naive Bayes relies on *conditional* independence, which is never defined. The lab's key function is a large jump for non-coders.

Files read: `Build/content/s15.py`, `Class Slides PDF/15 - Conditional probability and Bayes.pdf` (31 pages, all viewed), the learner and solution notebooks, `Workbooks/Session 15 - Conditional probability and Bayes.xlsx`.

## Findings

| ID | Where | Cat | Sev | What is wrong | Fix |
|---|---|---|---|---|---|
| 15-1 | Slide 10 (independence) | 2 | Medium | Independence is defined here as new, but S14 used "independent Bernoulli trials" and "independent values" (CLT) a session earlier. | Move the definition to S13 or S14 (see 14-3) and make this slide a recall plus the table test. |
| 15-2 | Slide 17 (Naive Bayes formula), words list, slide 12 | 2, 3 | Medium | "Naive: treat the words as independent" (the words definition says "naively treating the words as independent"). The assumption is conditional independence *given the class*, which appears only in the notes. Slide 10 teaches unconditional independence, so the slide wording invites the wrong idea, since the words are clearly dependent overall. Slide 12 also introduces "if its error is independent of the first" without defining it. | On slide 17, write "Naive: within spam (and within ham) the words are treated as independent: P(free and prize given spam) = P(free given spam) × P(prize given spam)." |
| 15-3 | Slide 17 symbol table | 3 | Low | The formula uses ∏ (product symbol) but the table row is called "product" and never shows or names ∏. The P(w given c) row and the q(w,c) row both define the same factor. | Name it: "∏ (capital pi): multiply over all the words, like Σ adds". Merge the two rows. |
| 15-4 | Slide 21 (bridge) notes | 3 | Low | The notes say "A vector called present", but the code names it `has`. | Use the same name in both. |
| 15-5 | Slide 20 and notebook cell 24 | 2, 3 | Low | "Softmax of these two numbers gives 0.9955". The solution computes `1/(1+exp(log_h-log_s))`, the sigmoid form from S11, labelled "softmax of two scores" with no link shown. | Add: "With two classes the softmax is the sigmoid of the difference: 1/(1 + e^(ln ham − ln spam))". This is a useful bridge to S11 and to logistic regression. |
| 15-6 | Slide 16 (smoothing) | 3, 4 | Low | "(count + 1) / (emails in the class + 2)" is correct for this present/absent (Bernoulli) model. Text classifiers usually use the word-count (multinomial) version, which adds the vocabulary size instead. The "+2" is explained only in a facilitator probe. | Add to the slide: "+2 because each word has two outcomes, present or absent, and each gets one extra count." |
| 15-7 | Slide 12 bar chart | 3 | Low | The prior bar (1%) is almost invisible, and the 45% bar is white while the 8.3% bar is gold. The colours read oddly. | Use gold for the posterior bars, or label the colours. |
| 15-8 | Notebook Step 4, cell 23 | 6 | Medium | The learner must write the whole `posterior(has, smooth)` function (smoothing switch, np.where, np.prod, priors) from a one-line hint. It is the hardest coding step in the three sessions, and a non-coder is likely to stall here and lose Steps 4 and 5. | Give the function skeleton with two TODO lines (`like_s = ...`, `score_s = ...`), or pre-write the like_* lines. |
| 15-9 | Notebook cell 24 | 6 | Low | `p_log` is one TODO with no hint at the variable level, and the bridge slide does not show the log version. | Provide `log_s = np.log(0.4) + ...` as a template, and leave only the ham line and the final probability for the learner. |
| 15-10 | Error table slide 25 | 6 | Low | "RuntimeWarning: divide by zero in log" cannot happen in the lab as written, because the unsmoothed run uses np.prod and no log. | Keep it only if the lab's log cell can meet it, otherwise replace it with a realistic error (for example, using `has == 0` the wrong way round). |
| 15-11 | Words (slide 6) and notes | 5 | Low | "a small, honest spam filter". "honest" is filler, and "actually" appears 3 times. 13 of 24 notes open with "Here is/are/Now/Let us". | Remove the filler and vary the openers. |
| 15-12 | Slide 28 | 4 | Low | "Researchers have documented ... hallucinations" (notes) has no source, while the other AI slides cite Sahami 1998 and Guo 2017. | Cite one survey, for example Ji et al. 2023 (ACM Computing Surveys), or keep the claim generic on the slide as it is now. |
| 15-13 | Workbook | 6 | Low | It has no log-score step and no prior-change experiment, while the notebook has both, so the spreadsheet learners miss the underflow lesson. The other numbers match. | Add two cells: LN of each score, then the posterior from them. |

### Python checks (category 1)
```
P(spam|free)=28/34=0.823529; P(free|spam)=0.70; expected if indep 0.4*0.34*100=13.6 (ham 20.4)
P(E)=0.9*0.01+0.1*0.99=0.108; post1=0.083333; post2=0.45; 0.009/0.1=0.09 (error row); prevalence 10% -> 0.5
probe: 1% FPR -> 0.009/(0.009+0.0099)=0.4762 (slide says about 48%)
exit: 1 in 1000, 99%/1% -> 0.0902
smoothed: free .6905/.1129, prize .5000/.0161, meeting .1190/.5000
email1 scores 0.121655 / 0.000546 -> 0.995529; ln = -2.1066, -7.5123
email2 scores 0.016440 / 0.033325 -> 0.330354
no smoothing email1: ham score 0 -> 1.0
calibration table: 150/200=.75, 216/300=.72, 49/100=.49
```
Facts checked: Sahami, Dumais, Heckerman and Horvitz 1998 (Bayesian junk email filtering), correct. Guo et al. 2017 (calibration of modern neural networks, over-confidence), correct. "Chat assistants are language models, not Naive Bayes", correct and suitably hedged.

## Cross-session notes
- **Assumed:** logarithms (S1, recalled), the stable softmax (S12, recalled), sigmoid (S11, used implicitly in the notebook, not recalled).
- **Should own:** independence belongs earlier (S13 or S14). This session should then define conditional independence, which Naive Bayes needs.
- **Hands forward:** prior, likelihood and posterior go to S16 (MAP; S16 recalls "proportional to the posterior from Bayes theorem in Session 15", which works). Calibration and "probability is not truth" set up S17's cross-entropy and perplexity. One gap: S16 treats likelihood as a function of the parameter, while S15 uses "likelihood" as P(evidence given hypothesis). A one-line forward note here ("next session the same word is used with the data fixed and the parameter varying") would prevent confusion.
