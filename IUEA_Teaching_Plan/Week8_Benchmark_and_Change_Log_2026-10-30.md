# Week 8 changes, benchmark and plan for Weeks 9 to 12

30 October 2026. Companion to [Week8_Onwards_Deck_Review_2026-10-29.md](Week8_Onwards_Deck_Review_2026-10-29.md).

## 1. Recommendations on the three questions

**Tree and imputer as a brief demonstration in Week 8: yes.** The assignment stays as issued, so students still write `predict_regression` with the baseline, the line and the depth-4 tree. The teaching time goes to the baseline, the line, error and the vocabulary, because those are the ideas every later week reuses. The tree needs one picture and one slide. The imputer needs one slide, and the data justifies the short treatment: the training rows hold a single missing input cell and the validation rows hold none. To keep the assignment fair, give students the `make_pipeline(SimpleImputer(...), model)` pattern as a ready-made line they copy, and mark the understanding in the written evidence.

**Week 9 should fit a classifier: yes.** Your own Week 1 roadmap promises it. The benchmark document lists "Classification: logistic regression, decision trees, random forest" and "ROC-AUC introduced" against Week 9, and says probability outputs and class imbalance appear that week. The built deck covers none of these. The recommendation is to derive a yes/no label from the motor, cooling or crusher data the students already know (for example "target above a stated limit"), fit `LogisticRegression` and `DecisionTreeClassifier`, show `predict_proba`, move the threshold, and keep the six-row file as the by-hand confusion-matrix drill. The assignment function `classification_metrics(actual, predicted)` needs no change.

**Small Week 8 fixes now, pause before the larger rebuild: done.** Details in section 4.

## 2. Benchmark

Sources checked on 30 October 2026. The Google pages could not be opened directly from this environment, so the Google entries rest on the search summaries of those pages.

| Idea | What the references do | What Week 8 now does |
|---|---|---|
| Order of ideas | [DeepLearning.AI, Machine Learning Specialization, Course 1](https://www.deeplearning.ai/specializations/machine-learning): Week 1 covers supervised and unsupervised learning, linear regression, the cost function, then gradient descent and the learning rate. Classification arrives in Week 3 | Kinds of ML, then vocabulary, then the line, then loss and gradient descent, then error measures. Classification follows in Week 9 |
| Regression, loss, gradient descent | [Google Machine Learning Crash Course, Linear regression](https://developers.google.com/machine-learning/crash-course/linear-regression): about 80 minutes covering the linear equation, loss (mean squared error), gradient descent and hyperparameters such as the learning rate | Two slides: the loss bowl with five tries, and a nine-line NumPy loop whose printed output is computed from the code on the slide |
| Estimator vocabulary | [scikit-learn Getting Started](https://scikit-learn.org/stable/getting_started.html): estimators are fitted with `fit`; supervised learning links observed data X to a target y; y is real numbers for regression and discrete for classification | A vocabulary table with `fit` and `predict` shown beside Training and Prediction, plus a slide showing X as a table and y as a column |
| Plain meaning plus a familiar anchor | The KLAi AI and Data Science Professional course opens each session with a vocabulary slide of 6 to 8 words, each with a plain meaning and an everyday equivalent, and keeps all 161 terms in a glossary | Two vocabulary slides of five words each, with an example from the student's own data in the third column |
| Baseline before a model | Professional course Session 14: a guesser first, with the baseline score printed beside every model score | Already present in Week 8; the scatter slide now draws the average as a dashed line beside the fitted line |
| One toy training loop | Professional course Session 20 trains one weight in a loop and prints the loss falling | Same idea, on data where the answer is visibly 2, so students can check it |

Where the Professional course differs by design: its learners are working adults who anchor on Excel. IUEA students are engineers who already hold the calculus, so the gradient slide names that link and leaves the derivation out.

## 3. What Week 1 promised, and what the built decks deliver

The Week 1 roadmap and the benchmark document set the Semester 1 and Semester 2 plan. Several Semester 1 items are in the plan and absent from the decks.

| Promised in the benchmark | Where promised | In the decks today |
|---|---|---|
| Types of machine learning, formal treatment | Week 8 | Added in this patch |
| fit / predict / score named as the pattern every model reuses | Week 8 | Added: the Training and Prediction rows of the vocabulary table; `score` is not shown anywhere |
| Polynomial regression demonstrated | Week 8 | Absent |
| Logistic regression, decision tree and random forest classification | Week 9 | Absent. No classifier appears in any deck |
| Accuracy, precision, recall, F1 and the confusion matrix "in full" | Week 9, 10 | Confusion matrix, precision, recall and cost are present. F1 is absent, and accuracy appears only in the assignment prompt ("why accuracy alone is insufficient"), with no slide that teaches it |
| ROC-AUC introduced | Week 9, 10 | Absent |
| Class imbalance and probability outputs | Week 9 | One text slide on thresholds; no imbalance example |
| Overfitting as a named session topic | Week 10 | The word appears once in Weeks 8 to 15 |
| k-fold cross-validation, reported as mean with spread | Week 10 | Present |
| Feature engineering and feature scaling inside a Pipeline | Week 11 | Feature engineering present. `StandardScaler` absent |
| Random forest and a sixty-second look at gradient boosting | Week 12 | Both absent |

Students were shown this roadmap in Week 1, so these are visible promises. The recommended order of repair is Week 9 classifier, Week 10 overfitting, Week 11 scaling, Week 12 forest and boosting.

**Semester 2, as planned** (benchmark document and CML3111 syllabus): regularisation (Ridge, Lasso), K-nearest neighbours and support vector machines, gradient boosting in depth, clustering (k-means, hierarchical), PCA, neural networks with PyTorch and back-propagation, convolutional networks with transfer learning, time series (classical methods first, then RNN and LSTM), explainable AI, text and embeddings, deployment basics, and data ingestion (SQL and an API call). Reinforcement learning, object-oriented programming, TensorFlow/Keras, autoencoders and GANs are outside both semesters. The benchmark itself flags regularisation, KNN/SVM and data ingestion as the weakest omissions.

The gradient descent slides in Week 8 are written as a preview of the Semester 2 neural network work, and the kinds-of-ML map labels clustering and PCA "Semester 2" and reinforcement learning "Not in this course", matching Week 1.

## 4. What changed in Week 8 (all three cohorts)

Decks are now 64 slides (60 before). Originals are in `decks/_backup_2026-10-30/`.

1. **Removed** the six-slide Data Analysis Project block. The last assignment slide is now the Week 8 form (A7), followed by the quiz.
2. **Repaired text damage** in prose and notes in seven places (for example "squared vertical baseline_errors" is now "squared vertical errors").
3. **Rewrote "Today's learning"** with outcomes for this week, using each cohort's target and unit.
4. **Added ten slides**, each with a spoken-script note:
   - Slide 3, Today's model is supervised regression (map of ML kinds)
   - Slides 4 and 5, Words for the whole field; Words for the data and the task
   - Slide 11, Some rows stay hidden while the model learns
   - Slide 22, A line through the points beats the average (the cohort's own data)
   - Slides 24 and 25, Training walks downhill on the loss; Gradient descent in a few lines of NumPy
   - Slides 31 and 32, scikit-learn reads X as a table and y as a column; NumPy arrays and their shape
   - Slide 44, Four misses, measured three ways (MAE, MSE, RMSE)
5. Footers renumbered. The form links were checked: Week 8 form, quiz and video are the only links left, and all are valid.

Numbers on the new slides are computed, not typed: the correlation on slide 22, the loop outputs on slide 25, the array outputs on slide 32 and the MAE/MSE/RMSE on slide 44 (the script asserts 2.75, 12.25 and 3.5).

## 5. Limits you should know about

- **The `.pptx` files were edited directly.** The normal build (`build_decks.py`) needs the Mac-only Artifact Tool runtime, which is not available here. The next full rebuild will overwrite these edits. Re-apply them with `python3 scripts/patch_week8_20261030.py` after any rebuild; the script skips a deck that is already patched and backs up before writing.
- **Not updated:** the lecturer-notes Markdown for Week 8 (`decks/lecturer_notes/…Week08…md`), the guided-practice notebook, and the student ZIPs. Slide numbers in those no longer match the deck. The new slides carry their own spoken notes in the deck.
- **Rendering was checked in LibreOffice**, on slides in all three cohorts. PowerPoint itself was not available; open the three decks once and click through them before class.
- **CML3112 taught Week 8 on 27 October.** For that cohort the new material fits best as a recap at the start of Week 9.
- **Still not changed:** the existing slides 7 to 9 and 13 to 15 (repeated import/read_csv cards), and the order of the imputer, pipeline and fit slides. Those belong to the larger rebuild.

## 6. Terms to teach in Weeks 9 to 12, for review before the rebuild

| Week | Words, each with a plain meaning and an example from the cohort's data |
|---|---|
| 9 | class, label, binary, probability, threshold, accuracy, confusion matrix, true/false positive and negative, precision, recall, F1, class imbalance, ROC curve and AUC (introduced), logistic regression (a line bent into a probability), decision tree classifier |
| 10 | overfitting, underfitting, generalisation, validation set, test set, cross-validation, fold, hyperparameter, data leakage, group split, spread |
| 11 | feature engineering, derived feature, interaction, scaling, standardisation, ablation, pipeline |
| 12 | model selection, constraint, latency, random forest (many trees voting), gradient boosting (sixty seconds, named only), trade-off |

Each week would open with a six-to-eight-word vocabulary slide in the same format as slides 4 and 5, and close with the same words in the exit check.
