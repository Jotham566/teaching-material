"""Week 2 deterministic component: 14 marks; the local rubric adds 6."""
ASSIGNMENT='W02'
TITLE='Proof of life: execution checks'
DEFAULT_COHORT='CML3111'
QUESTION_ORDER=['q1','q2','q3','q4']
QUESTIONS={
 'q1':dict(marks=2,visible=False,prompt='Set your roster student registration number.',answer_vars=['STUDENT_ID']),
 'q2':dict(marks=4,visible=False,prompt='Compute proof_sum = 2 + 2.',answer_vars=['proof_sum']),
 'q3':dict(marks=4,visible=False,prompt='Fresh-run readings after one increment.',answer_vars=['readings']),
 'q4':dict(marks=4,visible=False,prompt='Load the four CSV rows into rows.',answer_vars=['rows']),
}
