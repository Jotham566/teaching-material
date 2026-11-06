# Session 4 demonstration runs: words as numbers (recorded 6 November 2026)

**What was run.** `demo_runs/s04/s04_run.py` (everything below), `demo_runs/s04/s04_search.py` (the live search the lecturer types), corpus in `demo_runs/s04/s04_corpus.py`. Tool: Python 3.12.10, scikit-learn 1.9.1, sentence-transformers 6.2.0, model all-MiniLM-L6-v2. Run date: 6 November 2026. Number of runs: `s04_run.py` was run 5 times as outputs were added (bag of words and TF-IDF on four texts, TF-IDF on 40 messages, embeddings of three skins, extra tables); the numbers did not change between runs and the final results are in `results.json`. `s04_search.py` was run twice (contracts Q1, and `--raw` finance Q7) and its output matches `results.json`. Queries and passages were written before the first run and not changed after seeing results.

**All text is invented.** Nile Valley Foods Ltd, its clauses, finance terms and HR paragraphs are fictional. The 40 customer messages are the fictional file `03 Learner Materials/Practice Files/01 Case Company/customer_messages.csv`.

## 1. Bag of words (four invented messages, CountVectorizer)

| Word | A | B | C | D |
|---|---|---|---|---|
| 20 | 1 | 0 | 0 | 0 |
| again | 0 | 0 | 0 | 1 |
| and | 0 | 1 | 0 | 0 |
| bags | 1 | 0 | 0 | 0 |
| call | 0 | 0 | 0 | 1 |
| delivery | 0 | 0 | 0 | 1 |
| flour | 1 | 1 | 0 | 0 |
| for | 0 | 0 | 1 | 0 |
| invoice | 0 | 1 | 1 | 0 |
| is | 0 | 1 | 0 | 0 |
| late | 0 | 1 | 0 | 1 |
| maize | 1 | 1 | 0 | 0 |
| mbale | 1 | 0 | 0 | 0 |
| me | 0 | 0 | 0 | 1 |
| of | 1 | 0 | 0 | 0 |
| order | 0 | 0 | 1 | 0 |
| please | 1 | 0 | 1 | 1 |
| rice | 0 | 0 | 1 | 1 |
| send | 1 | 0 | 1 | 0 |
| the | 0 | 2 | 2 | 0 |
| to | 1 | 0 | 0 | 0 |
| was | 0 | 1 | 0 | 1 |
| wrong | 0 | 1 | 0 | 0 |

Messages: A: "Please send 20 bags of maize flour to Mbale"; B: "The maize flour was late and the invoice is wrong"; C: "Please send the invoice for the rice order"; D: "Rice delivery was late again, please call me"

## 2. TF-IDF on the 40 NVF customer messages (TfidfVectorizer, default settings)

Vocabulary 340 words. Messages containing a word (of 40): the 22, please 17, and 8, to 11, my 15, of 22, bags 11, sugar 3, invoice 4, jerrycans 3, maize 5, flour 5, late 2, wet 1, credit 2, mbale 4.

Message M06 ("Dear Nile Valley Foods, invoice 2305 shows UGX 104,000 for each jerrycan of cooking oil. We agreed UGX 98,000. Please correct the invoice and send us a new one."), by-hand weight = count x 40 / messages containing the word, and the real TF-IDF weight:

| Word | Count | In how many of 40 | Simple weight | Real TF-IDF |
|---|---|---|---|---|
| jerrycan | 1 | 1 | 40 | 0.217 |
| invoice | 2 | 4 | 20 | 0.335 |
| oil | 1 | 6 | 6.7 | 0.149 |
| send | 1 | 8 | 5 | 0.136 |
| please | 1 | 17 | 2.4 | 0.098 |
| the | 1 | 22 | 1.8 | 0.085 |

The by-hand version is a simplification (the real formula uses a logarithm and then scales each message to length 1).

## 3. Embeddings and search by meaning (all-MiniLM-L6-v2, 384 numbers, cosine)

First 8 of 384 numbers: {"query": [-0.008, -0.011, 0.098, 0.065, 0.016, -0.072, 0.025, -0.026], "K1": [0.017, -0.001, 0.047, 0.005, 0.098, 0.033, -0.067, -0.046], "K8": [-0.019, 0.06, -0.028, -0.065, -0.082, -0.081, -0.05, -0.068]} ; cosine between the question and Force majeure 0.361, and Governing law 0.03.

### Contract clauses (10 passages)

| Query | Right answer | Meaning search top 3 (cosine) | Rank of right answer | Word search (TF-IDF) first |
|---|---|---|---|---|
| Q1: What happens if heavy rain floods the road and the delivery cannot get through? | K1 | Force majeure 0.361; Limitation of liability 0.241; Indemnity 0.198 | 1 | no shared word |
| Q2: Who pays us back if the supplier's mistake costs us money? | K2 | Indemnity 0.627; Limitation of liability 0.423; Price adjustment 0.419 | 1 | Indemnity |
| Q3: Can we walk away from the deal without giving any reason? | K4 | Termination for convenience 0.363; Assignment 0.257; Automatic renewal 0.246 | 1 | Termination for convenience |
| Q4: The contract keeps running every year unless we say something in time. | K6 | Automatic renewal 0.539; Termination for convenience 0.378; Limitation of liability 0.287 | 1 | Automatic renewal |

### Finance and invoice terms (10 passages)

| Query | Right answer | Meaning search top 3 (cosine) | Rank of right answer | Word search (TF-IDF) first |
|---|---|---|---|---|
| Q5: The money we still have to pay the maize miller for flour already delivered. | F1 | Depreciation 0.314; Accounts payable 0.293; Accounts receivable 0.224 | 2 | Bad debt write-off |
| Q6: The shop sent back damaged bags and we want to reduce what they owe. | F4 | Accounts receivable 0.450; Bad debt write-off 0.423; Accounts payable 0.420 | 4 | Accounts receivable |
| Q7: Make sure our books match what the bank says. | F5 | Bad debt write-off 0.514; Bank reconciliation 0.461; Three-way match 0.306 | 2 | Bad debt write-off |
| Q8: Before we pay a bill, check that the order, the delivery and the bill all agree. | F9 | Three-way match 0.666; Accrual 0.419; Bad debt write-off 0.368 | 1 | Three-way match |

### HR policy paragraphs (10 passages)

| Query | Right answer | Meaning search top 3 (cosine) | Rank of right answer | Word search (TF-IDF) first |
|---|---|---|---|---|
| Q9: I saw a colleague stealing stock and I am afraid to say so. | H6 | Whistleblowing 0.402; Staff records 0.173; Disciplinary procedure 0.126 | 1 | no shared word |
| Q10: I am unhappy with how my supervisor speaks to me and want to complain. | H4 | Disciplinary procedure 0.363; Grievance procedure 0.350; Resignation and notice 0.301 | 2 | no shared word |
| Q11: I have malaria and cannot come to work tomorrow. | H3 | Sick leave 0.418; Overtime 0.258; Annual leave 0.107 | 1 | Grievance procedure |
| Q12: I want to quit. How much warning do I have to give? | H9 | Disciplinary procedure 0.341; Resignation and notice 0.299; Probation 0.294 | 2 | Disciplinary procedure |

**Over 12 searches:** right answer first 7, in the top three 11; word search (TF-IDF, English stop words removed) first 4. Not a benchmark: 12 searches on 30 short invented passages.

## 4. The four measures on the real vectors

- Default vectors (the model's last step makes every vector length 1): all four measures give the same top answer in 11 of 12 searches (city blocks differs once: finance Q5). Straight line and dot product agree with cosine in 12 of 12.
- Raw vectors (the last step skipped; modules Transformer and Pooling only; vector lengths 3.1 to 6.2): all four agree in 7 of 12; straight line 9, city blocks 8, dot product 11 of 12 agree with cosine.

Finance Q7 ("Make sure our books match what the bank says."), raw vectors, Bank reconciliation (the right term) against Bad debt write-off:

| Measure | Bank reconciliation | Bad debt write-off | Winner |
|---|---|---|---|
| Length of the vector | 4.49 | 5.337 | |
| Straight line | 5.065 | 5.195 | Bank reconciliation |
| City blocks | 77.96 | 80.33 | Bank reconciliation |
| Dot product | 10.753 | 14.251 | Bad debt write-off |
| Cosine | 0.461 | 0.514 | Bad debt write-off |

Also in `results.json` under `pair_examples`: HR Q10 and HR Q12 (the measures split on those as well), with both normalised and raw numbers.

## 5. The map
PCA to 2 numbers over the 30 passages and 12 descriptions: the two components keep 10.5% and 7.7% of the variation, 18.2% together. A t-SNE map (perplexity 8, seed 0) is also stored in `results.json` under `tsne`; the slide uses PCA.

## 6. Hand calculation on the slides (toy vectors, not a run)
a = (3, 4), b = (6, 8), c = (4, 3). Straight line a to b: 3 across, 4 up, 5. City blocks 3 + 4 = 7. Dot product a.b = 3x6 + 4x8 = 50, a.c = 3x4 + 4x3 = 24. Cosine a,b = 50 / (5 x 10) = 1.00; a,c = 24 / (5 x 5) = 0.96, angle about 16 degrees. Straight line a to c about 1.4, city blocks 2.
Hands-on answer key (A (3, 4), B (3, 1), C (6, 0); lengths 5, 3.16, 6): A to B 3, 3, 13, 0.82; A to C 5, 7, 18, 0.60; B to C 3.16, 4, 18, 0.95.

## Files
`demo_runs/s04/`: `s04_corpus.py`, `s04_run.py`, `s04_search.py`, `results.json`, `output_s04_run.txt` (first part of the printed output), `output_s04_search_contracts_Q1.txt`, `output_s04_search_raw_finance_Q7.txt`.
