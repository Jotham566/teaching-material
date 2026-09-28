ASSIGNMENT='W12'
TITLE='Model recommendation'
DEFAULT_COHORT=""
QUESTION_ORDER=['q1', 'q2']
QUESTIONS={'q1': {'marks': 5, 'visible': False, 'prompt': 'select_model(candidates, max_mae, max_ms): Candidates have name, validation_mae and latency_ms. Keep those meeting both inclusive constraints; select smallest validation_mae, then latency_ms, then name alphabetically. Return the selected name or None. Never use test scores for selection.', 'answer_vars': ['select_model']}, 'q2': {'marks': 3, 'visible': False, 'prompt': 'regression_errors(actual, predicted): Return mae and rmse, calculated over the same paired observations, with full precision.', 'answer_vars': ['regression_errors']}}
