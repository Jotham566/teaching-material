"""Week 4 reading report. See the cohort practical README. 20 marks."""
ASSIGNMENT='W04'
TITLE='Reading report with collections and CSV'
DEFAULT_COHORT='CML3111'
QUESTION_ORDER=['q1','q2','q3','q4']
QUESTIONS={qid:dict(marks=5,visible=False,prompt='Compute '+var+' from the supplied cohort CSV.',answer_vars=[var]) for qid,var in zip(QUESTION_ORDER,['valid_count','mean_reading','above_limit','group_means'])}
