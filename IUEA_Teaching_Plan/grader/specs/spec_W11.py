ASSIGNMENT='W11'
TITLE='Features and ablation'
DEFAULT_COHORT=""
QUESTION_ORDER=['q1', 'q2']
QUESTIONS={'q1': {'marks': 5, 'visible': False, 'prompt': 'make_features(feature_records): Return one feature row per input, in order: [load_pct, ambient_c, load_pct/100, load_pct*ambient_c]. Use inputs available at prediction time only.', 'answer_vars': ['make_features']}, 'q2': {'marks': 5, 'visible': False, 'prompt': 'ablation_metrics(training_records, validation_records): Fit two sklearn LinearRegression models on the same training records: base features [load_pct, ambient_c] and extended features adding load_pct*ambient_c. Evaluate both on the same validation records. Return base_mae, extended_mae and improvement=base_mae-extended_mae, without rounding. Inputs are complete; never fit on validation targets.', 'answer_vars': ['ablation_metrics']}}
