ASSIGNMENT='W08'
TITLE='Regression and baseline'
DEFAULT_COHORT=""
QUESTION_ORDER=['q1', 'q2']
QUESTIONS={'q1': {'marks': 7, 'visible': False, 'prompt': 'predict_regression(training_records, feature_records): Fit a training-mean baseline, linear regression and a decision tree (max_depth=4, random_state=17) using load_pct and ambient_c only. Return three prediction lists under baseline, linear and tree. Feature records have no target. Fit preprocessing only on training data.', 'answer_vars': ['predict_regression']}, 'q2': {'marks': 3, 'visible': False, 'prompt': 'regression_errors(actual, predicted): Return mae and rmse, calculated over the same paired observations, with full precision.', 'answer_vars': ['regression_errors']}}
