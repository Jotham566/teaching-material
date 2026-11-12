# Terms and examples brief (6 November 2026)

The lecturer's feedback after reading the finished decks: (1) many examples are hard to comprehend, even for him, so they will be harder for students; (2) do not oversimplify words or reword concepts: use the INDUSTRY-STANDARD term, then explain it properly. This brief applies to every slide, figure, spoken note, take-away sheet, workbook page and facilitator text of Sessions 0 to 14.

Read first: `V3_AUTHORING_BRIEF.md`, `REVIEW_BRIEF.md` (render and check workflow), `FLOW_BRIEF.md`, `CONCEPT_FLOW_BRIEF.md`. Setup: `. /private/tmp/claude-501/-Users-jothamwambi-Projects-IUEA-Teaching-Resources/64326435-6d94-43f3-a671-3bf5787b895f/scratchpad/env.sh; cd "$B"`.

## Rule 1: industry term first, then a proper explanation
- Slide titles, labels, figure text, table headers, 'Words we use today' and take-away sheets use the STANDARD term used in industry, papers, model cards and vendor documents (see the table below). Do not coin or substitute friendlier names ("squash", "dials", "pieces", "lazy model", "four boxes", "cut-off", "librarian", "badges", "coaching", "brief" for prompt) as the name of a thing.
- The first time a term appears in a session, explain it properly in plain words in the same breath: one or two sentences that are accurate, not a rewording that changes the meaning. Keep the formal name visible after that.
- An analogy may stay as a memory aid, introduced as an analogy ("think of it like..."), never as the name. Keep the explanation correct: state where the analogy breaks if it could mislead.
- Abbreviations are expanded at first use (k-NN: k-nearest neighbours; ReLU: rectified linear unit; TF-IDF: term frequency times inverse document frequency; RAG: retrieval-augmented generation; LoRA: low-rank adaptation; MCP: Model Context Protocol; GGUF; AUC: area under the curve).
- Do not drop standard maths names for the three-number calculations: show the real formula in words and symbols once (for example weighted sum: output = w1x1 + w2x2 + w3x3 + b) next to the worked numbers, then explain each symbol. Lawyers can follow it if each symbol is named.
- The lint rules still hold (word limits, no em dashes, no "X, not Y", banned words, no he or she for the learner).

### Standard terms to use (replace our coined wording everywhere)
| Use this term | Explain it in plain words (accurately) | Replace |
|---|---|---|
| weighted sum | multiply each input by its weight and add the results | checklist points total |
| weight | a number that says how much one input counts | dial, how much a question counts |
| bias | a number added to the weighted sum that shifts when the neuron switches on | cut-off, offset |
| parameters | all the weights and biases of a model, the numbers training adjusts | settings, dials |
| activation function (for example ReLU, sigmoid) | a simple function applied to the weighted sum that adds non-linearity; ReLU outputs 0 for negative values and the value itself otherwise | squash |
| neuron (unit) | computes a weighted sum, adds a bias and applies an activation function | checklist |
| layer, hidden layer, output layer | a set of neurons that take the same inputs; hidden layers sit between input and output | row of clerks |
| loss (loss function, error) | a number measuring how wrong the model's predictions are; training tries to make it small | miss, score of the miss |
| gradient, gradient descent, learning rate | gradient: which direction and how steeply the loss changes with a weight; gradient descent: repeated small steps against the gradient; learning rate: the size of each step | nudge, step |
| backpropagation | the method that works out the gradient for every weight, layer by layer from the output back | blame sharing |
| epoch | one full pass over the training data | pass |
| training, validation and test sets | training: the model learns from it; validation: used to tune; test: used once at the end | train, check, test |
| overfitting | the model fits the training data, including its noise, and does worse on new data | memorising (use overfitting, and say memorising as the plain explanation) |
| confusion matrix; true positive, false positive, false negative, true negative | the table that counts the four kinds of outcome of a classifier | four boxes |
| precision, recall, F1 score, accuracy | keep the formulas in words and numbers | unchanged |
| threshold, ROC curve, AUC | unchanged | cut-off line |
| baseline; majority-class baseline | a simple reference model to beat; predicting the most common class always | lazy model |
| cross-validation (k-fold) | split the data into k parts, train on k-1, test on the held-out part, rotate, average | taking turns to hide data |
| supervised, unsupervised, reinforcement, self-supervised learning | standard four types | unchanged |
| classification, regression | predict a category; predict a number | unchanged |
| feature, label, example (training example) | an input measurement; the correct answer; one row of data | unchanged |
| decision tree; split; leaf; depth | a model made of yes-or-no questions on features; the question at a node; the final answer; number of questions in a path | unchanged |
| k-nearest neighbours (k-NN), distance metric | predict from the k most similar training examples, using a distance metric | precedent, ruler |
| Euclidean distance; Manhattan distance; dot product; cosine similarity | the four standard measures; give the formula in words and a worked example | straight line, city block (as plain explanation only) |
| bag of words, TF-IDF, embedding, vector, dimension, vector space | standard terms; an embedding is a vector (list of numbers) that represents the meaning of text | map of meaning |
| token, tokenizer, vocabulary, context window | pieces of text the model reads (words or sub-words); the program that splits text; the set of tokens; how many tokens fit at once | pieces, bricks |
| next-token prediction; logits; softmax; probability distribution | the model scores every token (logits), softmax turns scores into probabilities that sum to 1 | next-word list |
| temperature, top-k, top-p, sampling, greedy decoding | settings for choosing the next token | unchanged, define each |
| self-attention, attention head, query, key, value | each token weighs the other tokens by relevance; (query, key, value as in the original paper: explain simply and honestly) | which earlier words matter |
| transformer, transformer block (self-attention + feed-forward network) | the architecture of modern language models: a stack of identical blocks | block of attention and neurons |
| embedding matrix (lookup table), positional encoding | one row of numbers per token; numbers that tell the model the position | piece table, position table |
| pretraining, post-training (supervised fine-tuning, instruction tuning, RLHF), base model, instruction-tuned model | the standard stages | coaching |
| foundation model, large language model (LLM), small language model, mixture of experts (MoE), reasoning model, multimodal model, diffusion model | standard families | unchanged |
| benchmark (MMLU, GSM8K, HumanEval), model card | unchanged | unchanged |
| open weights, open source (OSI definition), licence | unchanged | unchanged |
| quantisation (INT8, 4-bit), precision (FP32, FP16), file formats (safetensors, GGUF, ONNX) | quantisation lowers the number of bits per weight | rounding to fewer values |
| inference, latency, throughput | using a trained model | unchanged |
| prompt (system prompt, user prompt), few-shot prompting, zero-shot, chain-of-thought, structured output (JSON), delimiters | standard prompting terms | brief, example prompt |
| retrieval-augmented generation (RAG), retriever, chunking, vector database, context | the standard RAG pipeline | librarian |
| fine-tuning, LoRA, adapter | unchanged | training a new hire |
| hallucination, prompt injection, bias, data leakage | standard failure terms | unchanged |
| agent, tool use (function calling), agent loop (plan, act, observe), Model Context Protocol (MCP), human-in-the-loop, guardrails, least privilege, permissions (scopes), audit log | standard agent terms | badges, gate, boundary: use permissions, approval step (human-in-the-loop), guardrails |
| data governance, data lineage, data quality dimensions, personal data (Data Protection and Privacy Act, 2019) | unchanged | unchanged |

## Rule 2: examples must be easy to comprehend, everyday first
- The lecturer chose: EVERYDAY LIFE FIRST. For every concept, the first example (the one that carries the picture and the small calculation) is a situation anyone knows without any business or legal background, then the business application follows as 'where you will see it at work'. Good everyday scenarios: predicting a house price from floor area and bedrooms; deciding whether to carry an umbrella; spam or not spam in an inbox; sorting mail into piles; recommending a film or a song from what you watched; a school timetable; a taxi fare from distance and waiting time; the price of a second-hand car from age and mileage; a shop till and prices; mobile money SMS (a text like 'You have received UGX 20,000'). Choose the simplest scenario that shows the concept. One scenario per concept, introduced in a sentence, with real-looking, round numbers (no invented scoring schemes, no points systems, no obscure local metaphors such as nets, crows or boda riders).
- Numbers: round, few, believable. Show the calculation line by line with the formula named. Do not invent unexplained constants.
- A single running example per session where possible (carry it from the first concept to the last slide of the ideas block), then the business application and the recorded demonstration (real data stays as recorded; the demonstration data and recorded numbers must not change).
- Keep Nile Valley Foods and the recorded demonstration data for the 'at work' slides and the demonstrations, but each business example is explained in one plain sentence first ('A customer message is a short text, such as an order or a complaint; we want the machine to sort it').
- Replace any example that needs domain knowledge to follow (insurance claims, payroll internals, legal clauses, supply contracts) with an everyday one when used to TEACH a concept; the demonstration may still use those data, introduced simply.
- Remove invented scoring checklists with points (the 'payment-risk checklist' used in Sessions 0 to 3 and its worksheet) as the teaching example for the neuron: use a weighted sum that people already understand (a house price or a taxi fare), then the decision with an activation (carry an umbrella: yes or no).

## What to change, per session
Rewrite every slide's title, text, figures, table content, notes (spoken script, keep the flow, bridges and the 'How today connects' consistency in `kit/chain.py`: update chain phrases to the standard terms), `words`, `recall`, `keep`, `workbook`, `facilitator` (prep, demo_steps, probes, misconceptions, questions, takeaway) of YOUR sessions so that terms follow the table and examples follow Rule 2. Redraw figures whose example changes (modules `kit/diagrams_tNN.py`; keep real recorded data figures unchanged; look at every changed slide). Keep slide kinds, the clock, the recorded numbers, and the lint at 0 problems; spoken notes stay 45 to 150 words. Where an exercise's numbers change (paper exercises, worksheets), note the new numbers in the session's `facilitator['prep']` and `workbook` so the worksheet generator (`kit/worksheets.py`, updated afterwards by someone else) can follow: describe the exercise rows, columns and answers explicitly.

Do not weaken accuracy: if a term's definition is subtle (for example 'attention', 'RLHF', 'embedding'), say what it really is and what is simplified. Do not invent facts; use the sources in `demo_runs/sources_sNN.md`.

## Report (under 250 words)
Terms replaced (the main ones), examples replaced (old to new, per slide group), figures redrawn, exercise numbers that changed (so worksheets can follow), anything you left because it is a recorded run or a quoted source, and doubts.
