ASSIGNMENT='W10'
TITLE='Validation and trust'
DEFAULT_COHORT=""
QUESTION_ORDER=['q1', 'q2']
QUESTIONS={'q1': {'marks': 6, 'visible': False, 'prompt': 'group_split(records): Assign whole equipment groups: E1–E4 to train, E5 to validation, E6 to test. Return train, validation and test lists of record_id in input order. Do not use target values to choose membership.', 'answer_vars': ['group_split']}, 'q2': {'marks': 4, 'visible': False, 'prompt': 'predict_regression(training_records, feature_records): Fit a training-mean baseline, linear regression and a decision tree (max_depth=4, random_state=17) using load_pct and ambient_c only. Return three prediction lists under baseline, linear and tree. Feature records have no target. Fit preprocessing only on training data.', 'answer_vars': ['predict_regression']}}
