# Terminology rule for every slide, note, notebook and guide

**Use the real industry term as the name. Explain it in simple words next to it. Never replace it by a friendlier invented name.**
The lecturer's reason: students will meet these terms in textbooks, documentation, interviews and later courses. If a slide called a baseline 'the plain guess', the next time they hear 'baseline model' they are confused. So the slide says 'baseline model' and then explains: 'a baseline model is the simplest possible prediction. Here it predicts the average of the training targets for every row. Every other model has to beat it.'

Pattern on a slide: **Term (plain-words explanation, with the units or an example).** Define it the first time it appears in the deck, and again in the Words table or the formula slide if it matters. After that use the term, not a paraphrase.

## Canonical terms (use these; the left column is what must disappear as a NAME)

| Do not use as a name | Use this term | Plain-words explanation to give once |
|---|---|---|
| plain guess, the average guess | baseline model (a mean predictor; scikit-learn: DummyRegressor) | the simplest possible model: predicts the mean of the training target for every row |
| load-only line, the line, straight line | simple linear regression (one feature) and multiple linear regression (two or more features) ; linear regression model | a model that predicts the target as an intercept plus weighted features |
| the line using both inputs | multiple linear regression | same idea with two features |
| invented misses, invented example | illustrative example (hypothetical data) / worked example | numbers made up to show the arithmetic |
| the miss, the gap, error of a row | prediction error, or residual (actual minus predicted) | e = y - y-hat |
| average miss, typical miss | mean absolute error (MAE) ; root mean squared error (RMSE) ; mean squared error (MSE) | as defined on the formula slides |
| scoreboard, report card | model comparison table (evaluation metrics on the validation set) | |
| hidden rows, sealed group | held-out data: validation set and test set (hold-out set) | rows not used to fit the model |
| training rows | training set | |
| empty cell, blank | missing value (NaN in pandas) | |
| filling blanks | imputation (SimpleImputer, median imputation) | |
| inputs, readings | features (input variables, predictors) | |
| the answer column | target variable (label when it is a class) | |
| the setting(s), the numbers the model learned | parameters; for linear models the coefficients (weights) and the intercept (bias) | |
| box at the bottom of a tree, question in a tree | leaf node ; internal node (a split on a feature and a threshold) | |
| memorising | overfitting (the model fits noise in the training set) ; underfitting | |
| gap between the two scores | generalisation gap (validation error minus training error) | |
| the S curve | sigmoid (logistic) function | |
| yes or no model | binary classification ; positive class and negative class | |
| caught, missed, false alarm | true positive (TP), false negative (FN), false positive (FP), true negative (TN) | |
| always-say-no baseline | majority-class baseline | |
| cut-off, the line on the probability | decision threshold (classification threshold) | |
| the trade-off curve | ROC curve (receiver operating characteristic) and AUC (area under the curve) | |
| spread | standard deviation | |
| folds, rounds | K-fold cross-validation; each part is a fold; GroupKFold for grouped data | |
| leak, leaking | data leakage | |
| the recipe | workflow or pipeline (a scikit-learn Pipeline chains preprocessing and a model) | |
| scaler | StandardScaler (standardisation: z-score) | |
| ladder / easiest to explain | model selection; parsimony (prefer the simpler model when scores are close) | |
| decision memo | decision memo (keep) ; model card is a related industry term | |
| step of learning, downhill walk | gradient descent; loss function; gradient; learning rate | |
| interaction column | interaction feature (product of two features) | |
| removing or adding one input to test it | ablation study (feature ablation) | |
| neighbours | k-nearest neighbours (k-NN) | |
| penalty | regularisation (ridge regression: L2 penalty; alpha is the regularisation strength) | |
| fitting a model | training (fitting) the model: model.fit(X_train, y_train) | |
| using a model | inference (prediction): model.predict(X) | |
| a hyperparameter | hyperparameter (keep; setting chosen before training, e.g. max_depth) | |
| test run on hidden rows | evaluation on the validation set | |

Notes
- Simple linear regression (one feature) is also called univariate linear regression. Multiple linear regression has two or more features. Multivariate regression strictly means several target variables, so say 'multiple', and mention 'multivariate' only to warn about it.
- 'Illustrative' and 'hypothetical' are the right words for made-up numbers; always label them so.
- Keep scikit-learn class and function names exactly (DummyRegressor, LinearRegression, DecisionTreeRegressor, LogisticRegression, SimpleImputer, StandardScaler, make_pipeline, GroupKFold, mean_absolute_error ...). Variable names in notebooks should be the conventional ones: X_train, y_train, X_valid, y_valid, baseline_model, linear_model, tree_model, y_pred, mae, rmse, cv_scores, results (a DataFrame comparing models), not cute names (scoreboard, line_guess).
- Plain-words explanations stay; they follow the term. The beginner must still understand every slide without the notes.
- Mathematical notation: y (actual), y-hat (predicted), x_1 ... x_p (features), b_0 (intercept), b_1 ... b_p (coefficients), n (rows), e_i or r_i (residual), as already used.
