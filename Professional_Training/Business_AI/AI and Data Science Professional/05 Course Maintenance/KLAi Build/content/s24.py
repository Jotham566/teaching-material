"""Session 24: Present your course project and plan your path from here. Planning, rehearsal and feedback lab in a Google Sheet (sheet_tasks), no notebook.

Every number on a slide, in a note or in sheet_tasks is computed in facts() with pandas and numpy from the real Nile Microfinance file (loans.csv): a numpy L2 logistic regression
(the same objective scikit-learn minimises) on a seeded 75/25 split. Course-hour figures for other programmes are provider estimates found in the original Benchmark and Design Report
(28 and 29 October 2026) and are hedged on the slides: check current figures.
"""
import importlib.util
import sys
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

BUILD = Path(__file__).resolve().parents[1]
DATA = BUILD.parent.parent / '03 Learner Materials' / 'Practice Files' / 'data'
sys.path.insert(0, str(Path(__file__).resolve().parent))
import loans_canon as LC  # noqa: E402
_spec = importlib.util.spec_from_file_location('s23_for_s24', BUILD / 'content' / 's23.py')
S23 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(S23)

CAT = ['district', 'gender', 'occupation', 'loan_purpose']
NUM = ['age', 'monthly_income_ugx', 'loan_amount_ugx', 'term_months', 'previous_loans', 'previous_late_payments', 'group_loan', 'savings_balance_ugx', 'has_mobile_money', 'distance_to_branch_km']
CUT = 0.2


def n(x):
    return f'{int(x):,}'


@lru_cache(maxsize=None)
def facts():
    """The evidence comes from the canonical loans split (loans_canon.py): 8,000 loans, stratified 6,000 / 2,000, the logistic regression of Sessions 15 and 16 (27 columns, scaled, L2 with C = 1.0)."""
    C = LC.facts()
    T5, T2 = C['thr_27'][0.5], C['thr_27'][0.2]
    nte, dte = C['n_test'], C['test_defaults']
    F = dict(rows=C['rows'], defaults=C['defaults'], rate=C['default_rate'], n_test=nte, d_test=dte, base_acc=C['baseline_accuracy'], auc=C['auc_27'])
    F['acc5'], F['tp5'], F['flag5'] = T5['accuracy'], T5['tp'], T5['flagged']
    F['rec5'] = F['tp5'] / dte
    F['flag2'], F['tp2'], F['fp2'], F['fn2'], F['tn2'] = T2['flagged'], T2['tp'], T2['fp'], T2['fn'], T2['tn']
    F['rec2'], F['prec2'], F['acc2'] = F['tp2'] / dte, F['tp2'] / F['flag2'], (F['tp2'] + F['tn2']) / nte
    F['flag_share2'] = F['flag2'] / nte
    F['per100'] = round(F['prec2'] * 100)
    F['n_missing_income'] = C['income_blank']
    # the gender audit of the SAME model and decision threshold (approve when the predicted probability of default is below CUT), on the 2,000 test loans
    ga = C['gender_audit']['27']
    F['aud_f'], F['aud_m'], F['aud_di'] = ga['F']['approval_rate'], ga['M']['approval_rate'], ga['disparate_impact_ratio']
    # numbers from Session 23 (the proxy variable example), reused in the recall answers
    f23 = S23.facts()
    F['s23_dB'] = S23.di(f23['ruleB'])
    F['s23_B_f'], F['s23_B_m'] = f23['ruleB']['F']['approval'], f23['ruleB']['M']['approval']
    # rehearsal example (illustrative seconds for the five slides) and plan
    F['plan_min'] = [1, 2, 3, 2, 2]
    F['plan_names'] = ['Question', 'Data', 'Evidence', 'Risk', 'Decision']
    F['reh_sec'] = [70, 150, 240, 150, 100]
    F['reh_total'] = sum(F['reh_sec'])
    F['plan_sec'] = [m * 60 for m in F['plan_min']]
    F['over'] = [a - b for a, b in zip(F['reh_sec'], F['plan_sec'])]
    F['over_idx'] = int(np.argmax(F['over']))
    F['peer'] = ['Yes', 'Not yet', 'Yes', 'Yes']
    F['crit'] = ['Question and evidence', 'Metric and baseline', 'Limits and fairness', 'Clarity']
    F['peer_open'] = F['peer'].count('Not yet')
    F['peer_low'] = F['crit'][F['peer'].index('Not yet')]
    F['hours_week'], F['weeks'] = 6, 26
    F['path_hours'] = F['hours_week'] * F['weeks']
    return F


def pct(x, d=1):
    return f'{x * 100:.{d}f}'


def build():
    F = facts()
    assert F['tp2'] + F['fn2'] == F['d_test'] and F['tp2'] + F['fp2'] == F['flag2'] and F['tp5'] / F['d_test'] < 0.21 and F['acc5'] > F['base_acc']
    nt, dt = n(F['n_test']), n(F['d_test'])
    sess = dict(
        num=24, block='Module F: Ship it and present', short_title='Course project and your path',
        title='Present your course project and plan your path from here',
        question='Can you explain what you built, what it can and cannot do, and what you will learn next?',
        outcomes=['Tell a result as a story: the answer, the evidence beside a baseline model, and the limits',
                  'Write an executive summary, present to a manager and answer questions on method and risk',
                  'Name what this course did not cover and choose your next free courses and a portfolio plan'],
        outcome_icons=['chart', 'people', 'pin'],
        outcome_note=('Here is what you can do by the end of today. You can tell a result as a story with three parts: the answer, the evidence beside a baseline model, and the limits. '
                      'You can write an executive summary, present to a manager and answer questions on method and risk. And you can name what this course did not cover, and choose your next free courses and a portfolio plan. '
                      'There is no code today. The lab is a rehearsal in a Google Sheet, where you plan, time and give each other feedback. Nothing is marked.'),
        clock=[(10, 'Recall and the question of the day'), (45, 'Concepts: the story, the summary, presenting, the portfolio'), (10, 'Break'), (45, 'Lab: plan, rehearse, give and receive feedback'), (10, 'Exit check, keep and next')],
        plan_title='Your two hours: concepts first, then a rehearsal lab',
        plan_caption='Ideas first. Then you plan and rehearse your talk in a sheet. Then the checks and what you keep.',
        plan_note=('We have two hours. The first ten minutes bring back Session 23 and set the question for today. Then forty-five minutes of concepts, with no laptops open: how to tell a result as a story, how to write an executive summary, how to present to a manager, how to keep a portfolio, and what this course left out. '
                   'After a ten minute break we open a Google Sheet for a forty-five minute lab. You plan your talk, time a rehearsal, prepare answers to hard questions and give a partner feedback. The last ten minutes are an exit check and what you keep.'),
        recall_from='Session 23',
        recall=[('What is the difference between data drift and concept drift?', 'In data drift the inputs change after training. In concept drift the link between the inputs and the outcome changes.'),
                (f'A rule never uses gender, yet it approves {pct(F["s23_B_f"])}% of women and {pct(F["s23_B_m"])}% of men. What is going on, and what do you measure?', f'A proxy variable (occupation) carries the information. Measure approval and error rates by group and the disparate impact ratio, here {F["s23_dB"]:.3f}.'),
                ('Name two things that never go into a public GitHub repository.', 'Personal data such as names, phone numbers or loan records of real people, and passwords, keys or tokens.')],
        words=[('Course project (capstone)', 'The larger piece of work that ends a course. Yours is a question, data, a model beside a baseline model, its limits and a talk. You keep it.'),
               ('Executive summary', 'A short opening paragraph with the answer, the evidence, the main limit and the decision you ask for. A busy reader may read only this.'),
               ('Limitation', 'Something your result cannot tell you, such as who the data left out. You say it before you show the result.'),
               ('Portfolio', 'A small set of your projects, for example GitHub repositories with a README, that a stranger can open and judge.'),
               ('Project checklist (rubric)', 'A list of the qualities that good work has, one row for each. You use it on your own project and to give a partner feedback. Nothing is scored.')],
        word_icons=['flag', 'doc', 'shield', 'folder', 'check'],
        words_note=('Five words for today. A course project, often called a capstone, is the larger piece of work that ends a course. An executive summary is a short opening paragraph with the answer, the evidence, the main limit and the decision you ask for. '
                    'A limitation is something your result cannot tell you, and you say it first. A portfolio is a small set of your projects that a stranger can open and judge. And a project checklist, which many people call a rubric, lists what good work looks like. You use it for feedback and nothing is scored. '
                    'We use all five in the lab.'),
        keep='Keep your presentation sheet: the five-slide plan with minutes, your rehearsal times, three prepared answers, the feedback from your partner and your six month learning path.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Your lab file', value='A talk plan'), dict(label='Your partner', value='Feedback on 4 rows'), dict(label='What next', value='A 6-month path')]),
        keep_title='Save your sheet, and start your six month path this week',
        next='There is no Session 25. Your six month path starts now. Tell your tutor your first free course and the day you will start.', next_label='What happens next', keep_returns=False,
        keep_note=('Before you go, save your sheet. It holds your talk plan, your rehearsal times, three answers to hard questions, the feedback from your partner and your six month path. '
                   'If a colleague could present your result from it, it is good. This is the last session, so the next step is yours: choose one free course from the list, check its current terms, and write the day you will start. '
                   'Well done for twenty-four sessions of work. When you have finished your course project, you receive a certificate of completion from KLAi Professional Learning. Please send your tutor your course project and your first course.'),
        cover_note=('Welcome to the last session. Over twenty-three sessions you went from a spreadsheet to a tested model, a small app and a fairness audit. Today you learn to present it. '
                    'You will tell a result as an answer, evidence and limits, write an executive summary, and prepare for the questions a manager asks. We also list plainly what this course did not cover, and you choose what to learn next.'),
        use_at_work='Present a model result to a manager with its baseline, limits and risks, and keep a portfolio of work you can show.',
        slides=[])
    S = sess['slides']

    S.append(dict(kind='table', title='Answers to the three questions from Session 23', headers=['Question', 'Short answer'], rows=[[q, a] for q, a in sess['recall']], widths=[5.2, 6.8], icons=['chart', 'people', 'lock'],
                  notes=('Here are the answers to the three warm-up questions. In data drift the inputs change after training. In concept drift the link between inputs and outcome changes. '
                         f'A rule that never uses gender but approves {pct(F["s23_B_f"])} percent of women and {pct(F["s23_B_m"])} percent of men is using a proxy variable, here occupation, and you measure approval rates, error rates and the disparate impact ratio, which was {F["s23_dB"]:.3f}. '
                         'And personal data and passwords never go into a public repository. Today you will say all of this out loud to a manager. Which of the three would you find hardest to explain?')))

    S.append(dict(kind='steps', title='Tell a result as a story in three parts: the answer, the evidence and the limits',
                  steps=[dict(head='The answer', text='Use the model to choose which loans an officer reviews first', icon='pin'),
                         dict(head='The evidence', text=f'It finds {pct(F["rec2"], 0)}% of defaults, beside a baseline model', icon='chart'),
                         dict(head='The limits', text='Fictional data. Checked by group. A person decides', icon='shield')], highlight=None,
                  caption='The same story works for any course project. Put the answer first, so the room knows what the evidence is for.',
                  notes=('Every good result tells a story in three parts. The answer comes first: what you recommend. For our loan model, use it to choose which loans an officer reviews first. '
                         f'The evidence comes next, and it always sits beside a baseline model. Our model finds {pct(F["rec2"], 0)} percent of defaults when it flags about {pct(F["flag_share2"], 0)} percent of loans. The limits close the story: fictional data, a fairness check by group, and a person who decides. '
                         'If one part is missing, the room will not know what to do with your work. What is the answer of your own course project, in one sentence?')))

    S.append(dict(kind='table', title='The evidence behind the loan story, with the baseline model beside it', headers=['Measure', 'Number', 'What it means'],
                  rows=[['Loans, and defaults', f'{n(F["rows"])}; {n(F["defaults"])}', f'{pct(F["rate"])}% of loans defaulted.'],
                        ['Held-out test loans', f'{nt}; {dt} defaults', 'Loans the model never saw.'],
                        ['Baseline model: always repaid', f'{pct(F["base_acc"])}% accurate', 'It finds no defaults at all.'],
                        [f'Model, decision threshold 0.5', f'{pct(F["acc5"])}% accurate', f'Finds {F["tp5"]} of {dt} defaults ({pct(F["rec5"])}%).'],
                        [f'Model, decision threshold {CUT}', f'Flags {n(F["flag2"])} loans', f'Finds {F["tp2"]} of {dt} defaults ({pct(F["rec2"])}%).'],
                        ['Area under the curve (AUC)', f'{F["auc"]:.3f}', 'How well it ranks risky above safe: 0.5 is a coin flip.']],
                  widths=[3.8, 3.2, 5.0], icons=['grid', 'folder', 'cross', 'check', 'flag', 'chart'], note='Same loans and the same split as Sessions 14 to 17 (logistic regression, 27 columns, decision threshold 0.2). Your Session 16 numbers may differ a little if your model or decision threshold differ.',
                  notes=(f'This is the evidence we will use for practice, from the Nile Microfinance loans. There are {n(F["rows"])} loans and {n(F["defaults"])} defaulted, which is {pct(F["rate"])} percent. We held out {nt} loans, with {dt} defaults. '
                         f'The baseline model says repaid every time. It is {pct(F["base_acc"])} percent accurate and finds no defaults. Our model at a decision threshold of one half is {pct(F["acc5"])} percent accurate, but finds only {F["tp5"]} of the {dt} defaults. '
                         f'At a decision threshold of {CUT} it flags {n(F["flag2"])} loans and finds {F["tp2"]}, which is {pct(F["rec2"])} percent. The area under the curve is {F["auc"]:.3f}. These are the same loans, the same split and the same model as Sessions 15 and 16, so your Session 16 numbers may differ a little only if your model or decision threshold differ. Which row is the story?')))

    S.append(dict(kind='compare', title='An accuracy number alone misleads: show the baseline model beside it',
                  left=dict(head='The number alone', points=[f'The model is {pct(F["acc5"])}% accurate.', 'It sounds strong.']),
                  right=dict(head='With the baseline', points=[f'Always saying repaid is {pct(F["base_acc"])}% accurate.', f'At decision threshold 0.5 the model finds {F["tp5"]} of {dt} defaults.']),
                  verdict='Report the baseline, the share of defaults found and the limit in one sentence.',
                  notes=(f'Here is the trap in every project talk. You say the model is {pct(F["acc5"])} percent accurate, and it sounds strong. Then a careful person asks what a model that always says repaid would score. '
                         f'The answer is {pct(F["base_acc"])} percent, so your model is barely ahead. This is the accuracy paradox, and it happens when one answer is much more common. At a decision threshold of one half, the model finds only {F["tp5"]} of {dt} defaults. '
                         'So give three things in one sentence: the baseline, the share of defaults found, and the limit. What would your course project baseline be?')))

    S.append(dict(kind='example', title='An executive summary gives the answer, evidence, limit and request in four sentences',
                  scenario='An executive summary is the short opening paragraph that a busy reader may read alone. Illustrative example for the loan model:',
                  blocks=[dict(label='Answer', text='Use the model to choose which loans a loan officer reviews first.'),
                          dict(label='Evidence', text=f'On {nt} held-out loans it found {pct(F["rec2"], 0)}% of defaults by flagging {pct(F["flag_share2"], 0)}% of loans. The baseline model finds none.'),
                          dict(label='Limit', text='The data is fictional and 379 loans lack income. We have not tested it after the data changes.'),
                          dict(label='Request', text='Approve a three month trial where a person decides, with a fairness check by gender each month.')],
                  notes=(f'This is what an executive summary looks like. Four sentences. The answer: use the model to choose which loans an officer reviews first. The evidence: on {nt} held-out loans it found {pct(F["rec2"], 0)} percent of defaults by flagging {pct(F["flag_share2"], 0)} percent of loans, while the baseline model finds none. '
                         'The limit: the data is fictional, 379 loans lack income, and we have not tested it after the data changes. And the request: approve a three month trial where a person decides, with a fairness check by gender each month. '
                         'A manager can decide from these four sentences alone. Write the four sentences for your course project in the lab.')))

    S.append(dict(kind='wide', title='A ten-minute talk has five slides: question, data, evidence, risk and decision',
                  visual=dict(kind='dl_segments', parts=[(nm, m, 'min') for nm, m in zip(F['plan_names'], F['plan_min'])], total_label='Ten minutes in all. Evidence gets the most time.'),
                  caption='Risk: what could go wrong, and who checks. Decision: what you recommend.',
                  notes=('Here is the shape of your ten minute talk. Five slides. Slide one is the question: the decision someone faces, one minute. Slide two is the data: what it covers and what it leaves out, two minutes. '
                         'Slide three is the evidence, the result beside its baseline, three minutes, the longest. Slide four is the risk: what could go wrong and who checks, two minutes. Slide five is the decision: what you recommend and the next step, two minutes. '
                         'Your executive summary becomes your opening sentence. Rehearse with a timer, because most people run long. Which slide will you be tempted to stretch?')))

    S.append(dict(kind='table', title='Presenting to a manager: say the real term, then what it means for a decision', headers=['Term', 'What you say next'],
                  rows=[['Recall (sensitivity)', 'Of every 100 loans that default, how many we flag.'], ['Precision', 'Of every 100 loans we flag, how many really default.'],
                        ['Area under the curve (AUC)', 'How well the model ranks risky loans above safe ones. 0.5 is a coin flip.'], ['Baseline model', 'The simple rule the model has to beat.'],
                        ['Decision threshold', 'The risk level at which a loan goes to an officer.'], ['Test set', 'Loans the model never saw while learning.']],
                  widths=[4.0, 8.0], icons=['magnifier', 'flag', 'chart', 'check', 'pin', 'folder'], note='Start with the answer. One number per slide. Keep the notebook ready for questions.',
                  notes=('A manager has a few minutes and a decision to make. So start with the answer, give one number per slide, and keep the notebook ready for questions. '
                         'Use the real term, because the manager may hear it again from the data team, and then say what it means. Recall: of every hundred loans that default, how many we flag. Precision: of every hundred loans we flag, how many really default. '
                         'The area under the curve is how well the model ranks risky loans above safe ones. A baseline model is the simple rule to beat. The decision threshold is the risk level at which a loan goes to an officer. And a test set is loans the model never saw. Which term do you tend to use without explaining?')))

    S.append(dict(kind='compare', title='Say the limits before the result, and the room trusts the result',
                  left=dict(head='Result first', points=['Opens with the best number.', 'Limits arrive in the last minute.', 'The claim lands before the caveat.']),
                  right=dict(head='Limits first', points=['Opens with what the data covers.', 'Names what the model cannot do.', 'Then shows the result.']),
                  verdict='A limit you state builds trust. A hidden one costs it.',
                  notes=('Two ways to open. On the left, the result comes first, with the best number. The limits squeeze into the last minute, and the room has already heard the claim, so anything you add sounds like a retreat. '
                         'On the right you open with what the data covers: eight thousand fictional loans, ten districts, almost three years. Then you name what the model cannot do. It cannot say why a borrower defaults, and it knows nothing about borrowers who were refused a loan. Then you show the result. '
                         'People trust a speaker who names the limits first. Try it in your own words in the lab. What is the biggest limit of your course project?')))

    S.append(dict(kind='table', title='Three questions on method, and answers you can give', headers=['Likely question', 'A good answer'],
                  rows=[['How do you know it works on new loans?', f'I kept {nt} loans the model never saw as a test set, and compared the result with a baseline model.'],
                        ['Why that metric and that decision threshold?', f'Missing a default costs more than reviewing a good loan, so I watch recall. At decision threshold {CUT} it finds {pct(F["rec2"], 0)}% of defaults, and about {F["per100"]} of every 100 flagged loans really default.'],
                        ['Could this result be luck?', 'This was one split. I would repeat it with k-fold cross-validation and report the range of scores.']],
                  widths=[4.4, 7.6], icons=['question', 'question', 'question'],
                  notes=('Three questions about method that you should expect. How do you know it works on new loans? Answer: I kept a test set the model never saw and compared it with a baseline model. '
                         f'Why that metric and that decision threshold? Because missing a default costs more than reviewing a good loan, so I watch recall. At a decision threshold of {CUT} the model finds {pct(F["rec2"], 0)} percent of defaults, and about {F["per100"]} of every hundred flagged loans really default. '
                         'Could it be luck? Honest answer: this was one split, so I would repeat it with k-fold cross-validation and report the range. An honest answer that names what is not finished is a good answer. Write your three answers in the lab.')))

    S.append(dict(kind='table', title='Three questions on risk: drift, fairness and data protection', headers=['Likely question', 'A good answer'],
                  rows=[['What could go wrong once people use it?', 'The data could drift after training. I would compare each month of inputs with the training period, compare predicted with actual defaults, and set a review date.'],
                        ['Is it fair, and are we allowed to use this data?', f'I audited approval and error rates by gender: {pct(F["aud_f"])}% of women and {pct(F["aud_m"])}% of men approved. I checked the purpose and data minimisation against the Data Protection and Privacy Act, 2019 (a teaching summary, not legal advice). A person decides.'],
                        ['Who is responsible for it?', '(Example answer for our fictional lender.) The credit manager owns the model card, and the data protection officer reviews each release.']],
                  widths=[4.0, 8.0], icons=['shield', 'people', 'flag'],
                  notes=('Three questions about risk. What could go wrong once people use it? The data could drift after training, so I compare each month of inputs with the training period, compare predicted with actual defaults, and set a review date. '
                         f'Is it fair, and are we allowed to use this data? I audited approval rates by gender, {pct(F["aud_f"])} percent for women and {pct(F["aud_m"])} percent for men, and I checked purpose and data minimisation against the Data Protection and Privacy Act of 2019. A person decides. '
                         'And who is responsible? For our fictional lender, the credit manager owns the model card, and the data protection officer reviews each release. This is a teaching summary and not legal advice. Which of these would your manager ask first?')))

    S.append(dict(kind='idea', title='A portfolio on GitHub is a few repositories a stranger can open in five minutes',
                  visual=dict(kind='dl_file', name='loan-risk-model/', lines=['README.md', 'notebook.ipynb', 'model_card.md', 'requirements.txt', 'app.py', 'loan_model.joblib', 'data/  (generated data only)', '.gitignore'], size=15,
                              gold=[0], notes=[(0, 'Read first: the front page'), (2, 'What it is for and where it fails'), (6, 'Never real customer data'), (7, 'Keeps secrets out')]),
                  lead='Portfolio: a small set of your projects that others can open and judge.',
                  points=['Two or three projects you can explain well.', 'Each notebook runs from the top.', 'Never real customer data.'],
                  notes=('A portfolio is a small set of your projects that a stranger can open and understand in five minutes. On GitHub that means a few repositories, each laid out like this one. The README comes first. '
                         'The notebook runs from the top. The model card says what the model is for and where it fails. The requirements file lets someone repeat your result. The app is optional. '
                         'The data folder holds generated or public data only, never real customer data, and the gitignore file keeps secrets out. Choose two or three projects you can explain best. What would be the name of your first repository?')))

    S.append(dict(kind='table', title='A README answers four questions: what, result, limits and how to run', headers=['Section', 'Loan model example'],
                  rows=[['The question', 'Which loans should an officer review first?'], ['The result', f'At decision threshold {CUT} the model finds {pct(F["rec2"], 0)}% of defaults on {nt} held-out loans. The baseline model finds none.'],
                        ['The limits', 'Fictional data. Not tested after the data changes. Fairness checked by gender only.'], ['How to run', 'Install requirements.txt, then Runtime, Restart session and run all.']],
                  widths=[3.0, 9.0], icons=['question', 'chart', 'shield', 'gear'], note='Write it for a stranger. Say which data is generated.',
                  notes=('The README is the front page of your portfolio. It answers four questions. What is the question? Which loans should an officer review first. What is the result, with its baseline? At a decision threshold of '
                         f'{CUT} the model finds {pct(F["rec2"], 0)} percent of defaults on {nt} held-out loans, and the baseline finds none. What are the limits? Fictional data, not tested after the data changes, fairness checked by gender only. '
                         'And how do you run it? Install the requirements and run the notebook from the top. Write it for a stranger and say which data is generated. Which of the four will you find hardest to write?')))

    S.append(dict(kind='table', title='What a finished project contains: four things, as a checklist for your own work and for partner feedback', headers=['Quality', 'A finished project has', 'A common gap to fix'],
                  rows=[['Question and evidence', 'A one-sentence question. Every claim points to data.', 'No clear question, or claims without data.'],
                        ['Metric and baseline', 'A metric chosen for the cost, on unseen data, beside a baseline model.', 'One accuracy number and no baseline.'],
                        ['Limits and fairness', 'Limits first. Risks named. Groups compared. Data duties checked.', 'Limits missing, or said late.'],
                        ['Clarity', 'Five slides, ten minutes, plain words, one decision.', 'Over time, jargon, no decision.']],
                  widths=[2.8, 5.6, 3.6], icons=['question', 'chart', 'shield', 'clock'], note='The lab asks for one comment on each row. Nothing is scored.',
                  notes=('Many people call a list like this a rubric. Here it is a project checklist: four qualities that a finished project has. You use it on your own project, and you use it to give a partner feedback. Nothing is scored and nothing is weighted. Question and evidence: a finished project has a one sentence question and every claim points to data. '
                         'Metric and baseline: a metric chosen for the cost, on unseen data, beside a baseline model. Limits and fairness: limits first, risks named, groups compared, data duties checked. And clarity: five slides, ten minutes, plain words and one decision. '
                         'The right column names the gap that people most often leave. In the lab you give your partner one comment on every row. Which row do you expect to need the most work on your own project?')))

    S.append(dict(kind='table', title='What this course did not cover: an honest gap list', headers=['Area', 'What that means for you'],
                  rows=[['Mathematics by hand', 'You calculated results by hand but did not prove them.'], ['Data structures and algorithms', 'Interview puzzles need separate practice.'],
                        ['Big data tools', 'Your data fitted in one notebook.'], ['Paid cloud platforms', 'AWS, Azure, Google Cloud. You used free tiers of Colab, GitHub and Streamlit.'],
                        ['Deep learning from scratch', 'One neuron and a small network in numpy. The pretrained model was optional.'],
                        ['Dashboards and BI tools', 'Power BI and Tableau were named, not taught.'], ['Production MLOps', 'No container, automated tests or monitoring.']],
                  widths=[4.0, 8.0], icons=['calculator', 'gear', 'folder', 'cloud', 'bars', 'chart', 'shield'], note='Say these gaps yourself, before anyone asks.',
                  notes=('Being honest about gaps is part of being trusted. Seven things this course did not cover, as I understand the session list. Mathematics by hand: you calculated many results by hand, but you did not prove them. Data structures and algorithms: job interview puzzles need separate practice. '
                         'Big data tools: your data fitted in one notebook. Paid cloud platforms: you used Colab, GitHub and Streamlit Community Cloud, which have free tiers. Deep learning from scratch: you built a neuron and a small network in numpy, and the pretrained model was optional. '
                         'Dashboards and business intelligence tools such as Power BI: we named them as hand-over tools but did not teach them. And production machine learning operations: your app is small, with no container, automated tests or monitoring. '
                         'Say these gaps yourself before anyone asks. Which gap matters most for your job?')))

    S.append(dict(kind='table', title='Free next steps by goal: check the current terms before you start', headers=['Goal', 'Free next step'],
                  rows=[['Python habits', 'Harvard CS50P (Introduction to Programming with Python)'], ['Everyday data work', 'Kaggle Learn: Pandas'], ['Models beyond this course', 'Kaggle Learn: Intermediate Machine Learning'],
                        ['Machine learning basics again', 'Google Machine Learning Crash Course'], ['Deep learning', 'fast.ai Practical Deep Learning for Coders'], ['AI ideas and ethics', 'University of Helsinki: Elements of AI'], ['Language models', 'DeepLearning.AI short courses'],
                        ['Cloud, big data, dashboards, MLOps', 'Search for a free introductory course on the tool your employer uses. Check its terms.']],
                  widths=[4.4, 7.6], icons=['gear', 'chart', 'magnifier', 'notebook', 'bars', 'people', 'doc', 'cloud'], note='Free to learn, but audit, certificate and account rules change. Check each provider page.',
                  notes=('Here is a free next step for each goal. For Python habits, Harvard CS50P. For everyday data work, Kaggle Learn Pandas. For models beyond this course, Kaggle Learn Intermediate Machine Learning. For the basics again, the Google Machine Learning Crash Course. '
                         'For deep learning, fast dot ai Practical Deep Learning for Coders. For AI ideas and ethics, Elements of AI from the University of Helsinki. For language models, the DeepLearning dot AI short courses. '
                         'For the gaps in cloud, big data, dashboards and production, I have not named a course, because I have not checked one. Search for a free introductory course on the tool your employer uses, and read its terms. '
                         'Free audit and certificate rules change, so check each provider page before you start. Which one will you start with?')))

    S.append(dict(kind='wide', title='This course is 48 hours. Well-known programmes list about 3 to 180 hours',
                  visual=dict(kind='bars', items=[dict(label='This course', value=48, hl=True), dict(label='Google ML Crash Course', value=15), dict(label='Elements of AI', value=30),
                                                  dict(label='Kaggle micro-course', value=4, text='3 to 5 h'), dict(label='DeepLearning.AI ML Spec.', value=95), dict(label='IBM Data Science', value=178), dict(label='Google Data Analytics', value=180)], unit=' h', size=16),
                  caption='Provider estimates at the time of writing. Some are marketing figures. They change.',
                  notes=('Where does this course sit? It is forty-eight hours. Next to it are provider estimates as listed in late October 2026. They are the providers own estimates, some are marketing figures, and they change, so check each page. The Google crash course is about fifteen hours, Elements of AI about thirty, and a Kaggle Learn micro-course three to five hours. '
                         'The DeepLearning dot AI Machine Learning Specialization is about ninety-five hours, the IBM Data Science Professional Certificate about one hundred and seventy-eight, and the Google Data Analytics Certificate over one hundred and eighty. '
                         'Across data certificates, one hundred and fifty to two hundred and forty hours is often quoted. So this course gives you a base that later study extends. Which programme will you try next?')))

    S.append(dict(kind='wide', title=f'Your six month path: practice, depth, portfolio, at {F["hours_week"]} hours a week',
                  visual=dict(kind='timeline', items=[dict(when='Months 1 and 2', what='Practice: repeat the labs on new data.'), dict(when='Months 3 and 4', what='Depth: one area from the gap list.'),
                                                      dict(when='Months 5 and 6', what='Portfolio: two projects and one app.', hl=True)], size=18),
                  caption=f'{F["hours_week"]} h a week for {F["weeks"]} weeks is {F["path_hours"]} h.',
                  notes=(f'Here is a six month path. Months one and two are practice: repeat the labs on new data and finish one Kaggle Learn course. Months three and four are depth: pick one area from the gap list and go further. Months five and six are the portfolio: publish two projects and one app, each with a README. '
                         f'Choose a weekly budget you can keep. Six hours a week for twenty-six weeks is {F["path_hours"]} hours, which is about the low end of the hours often quoted for a data certificate. Four hours a week is also fine, as long as you keep it. '
                         'What weekly budget will you set?')))

    S.append(dict(kind='table', title='Where you will use this at work: present a result so a manager can decide', headers=['Your job', 'The presentation', 'What today lets you do'],
                  rows=[['Credit analyst at a bank or SACCO', 'A monthly credit committee', 'Open with the answer and the baseline model, say the limits first, and show approval rates by group.'],
                        ['Officer in a ministry', 'A briefing note for a permanent secretary', 'Write the executive summary in four sentences, with one number and its source.'],
                        ['Data officer at an NGO', 'A donor report', 'State what the data covers and leaves out, and keep a portfolio of reproducible work.'],
                        ['Analyst at a retailer', 'A branch managers meeting', 'Explain recall and precision in plain words, with the cost of a mistake in shillings.']],
                  widths=[3.4, 3.4, 5.2], icons=['coin', 'doc', 'people', 'shop'],
                  notes=('Where will you use this on Monday? Four examples. A credit analyst at a bank or SACCO presenting to the monthly credit committee should open with the answer and the baseline model, say the limits first, and show approval rates by group. '
                         'An officer in a ministry writing a briefing note should write the executive summary in four sentences with one number and its source. A data officer at an NGO writing a donor report should say what the data covers and leaves out. '
                         'And an analyst at a retailer should explain recall and precision in plain words, with the cost of a mistake in shillings. Which of these meetings is closest to yours?')))

    S.append(dict(kind='divider', title='Part 2: rehearsal and feedback', lead='Close the slides. Open the sheet.', section='Lab',
                  notes=('That is the end of the ideas. There is no code today. Open a new Google Sheet and call it Presentation plan. You will make tabs as we go: plan, rehearsal, questions, feedback and path. '
                         'In every task, plan first, then do it, then check your numbers against the table on the screen. You present to a partner, and your partner gives you feedback with the project checklist. Listening to feedback is part of the skill.')))

    S.append(dict(kind='steps', title='The lab has five parts, and you keep a presentation sheet', steps=[dict(head='1 Plan', text='Five slides, minutes', icon='notebook'), dict(head='2 Rehearse', text='Time it aloud', icon='clock'),
                                                                                                         dict(head='3 Prepare', text='Three answers', icon='question'), dict(head='4 Present', text='Feedback to your partner', icon='people'), dict(head='5 Path', text='Six months, hours', icon='pin')], highlight=None,
                  caption='Six tasks in 45 minutes. For each task, plan, do it, then check your numbers.',
                  notes=('Here is the map of the lab, in five parts. Part one, plan your five slides with minutes that add up to ten. Part two, rehearse aloud with a timer and record the time of each slide. Part three, prepare three answers: method, metric and risk. '
                         'Part four, present to a partner for ten minutes and give each other feedback on the four checklist rows, with one comment each. Part five, write your six month path with a weekly hour budget. '
                         'The numbers in the first tasks are illustrative, so you can check your formulas. Please do not skip the rehearsal. It is where talks improve.')))

    S.append(dict(kind='wide', title='Your feedback tab: four checklist rows, Yes or Not yet for each, and one comment on each',
                  visual=dict(kind='sheet', headers=['Quality', 'Present?', 'One comment'], rows=[[F['crit'][0], F['peer'][0], 'Keep: one clear question on slide 1'], [F['crit'][1], F['peer'][1], 'Add the baseline beside the number'],
                                                                                                  [F['crit'][2], F['peer'][2], 'Say the limit before the result'], [F['crit'][3], F['peer'][3], 'Finished in 10 minutes'],
                                                                                                  ['Rows still to improve', f'=COUNTIF(B2:B5,"Not yet") gives {F["peer_open"]}', 'First: ' + F['peer_low']]], hl=[5, 1], size=16),
                  caption='Illustrative entries for the formula check. Your partner fills this in for your talk.',
                  notes=('This is the feedback tab your partner fills in. Four rows from the project checklist, Yes or Not yet for each, and one comment. Each comment should point to a named slide, and at least one should say what to keep. '
                         f'Here the illustrative entries have {F["peer_open"]} row still to improve, which the COUNTIF formula counts. Nothing is scored. Notice the comments: they are specific. Keep, add, say before. A comment such as good job teaches nothing. '
                         'When you receive feedback, write it down and do not defend yourself. You can ask a question to understand it. What kind of comment helps you most?')))

    pm, ps = F['plan_min'], F['reh_sec']
    S.append(dict(kind='table', title='Check your numbers before you move on', headers=['What you compute', 'You should get'],
                  rows=[['Planned minutes (task 1)', f'{" + ".join(str(x) for x in pm)} = {sum(pm)}'], ['Rehearsal total, in seconds and minutes', f'{F["reh_total"]} s = {F["reh_total"] // 60} min {F["reh_total"] % 60} s'],
                        ['Slide that ran longest past its plan', f'{F["plan_names"][F["over_idx"]]}, {F["over"][F["over_idx"]]} s over'], ['Recall at decision threshold 0.2 (task 3)', f'{F["tp2"]} / {dt} = {pct(F["rec2"])}%'],
                        ['Precision at decision threshold 0.2', f'{F["tp2"]} / {F["flag2"]} = {pct(F["prec2"])}%'], ['Feedback entries Yes, Not yet, Yes, Yes: rows still to improve, and which', f'{F["peer_open"]}, and {F["peer_low"]}'],
                        ['Learning path hours', f'{F["hours_week"]} x {F["weeks"]} = {F["path_hours"]}']],
                  widths=[7.0, 5.0], icons=['notebook', 'clock', 'flag', 'chart', 'chart', 'people', 'calendar'], note='If your number differs, find the task that went wrong.',
                  notes=('Use this table as your own self-check. Nobody marks it. If one number does not match, call me, because later tasks use earlier ones. '
                         'The most common cause is a range that includes the header row, or typing minutes where the sheet expects seconds. Your own talk will have different numbers, and that is fine. These check the formulas on the illustrative data. '
                         'Find out why it differs. What does it mean if your rehearsal total is under nine minutes?')))

    S.append(dict(kind='table', title='Five likely mistakes in the lab and how to fix them', headers=['What you see', 'What it means', 'What to do'],
                  rows=[['In the minutes table: 11 where you expected 10', 'The minutes add up to more than the plan.', 'Cut a sentence from the longest slide, then add the minutes again.'],
                        ['#VALUE! in a time formula', 'Text where a number is expected, such as "70 s".', 'Type 70 only. Put the unit in the header.'],
                        ['In the feedback tab: 2 where 1 was expected', 'The range includes the header row, or Not yet is spelled differently.', 'Use B2:B5 and type Not yet exactly.'],
                        ['Every row says Yes', 'The checklist is not showing what to improve.', 'Find one thing to improve on each row.'],
                        ['A path with no named course', 'Without a course and a date, it stays a wish.', 'Name one course, a start date and the hours a week.']],
                  widths=[3.7, 4.2, 4.1], icons=['cross', 'cross', 'cross', 'cross', 'cross'],
                  notes=('Five problems you may meet. A total of eleven instead of ten means your minutes add up to more than the plan, so cut a sentence from the longest slide. A value error in a time formula usually means text in the cell, such as seventy s, so type the number only. '
                         'A count that is too high means the range includes the header row or Not yet is spelled differently, so check the range. If every row says Yes, the checklist is not helping, so find one improvement on each row. '
                         'And a path with no named course is a wish. Name the course, the start date and the weekly hours.')))

    S.append(dict(kind='table', title='Exit check: three questions, then compare with the short answers', headers=['Question', 'Short answer'],
                  rows=[['Which three parts make a result into a story?', 'The answer, the evidence beside a baseline model, and the limits.'],
                        ['Name two things to say before you show a result.', 'What the data covers and leaves out, and what the model cannot do. Name the baseline too.'],
                        ['Where do you confirm the terms of a free course?', 'On the provider page, before you start, because free audit and certificate rules change.']],
                  widths=[5.6, 6.4], icons=['chart', 'shield', 'pin'],
                  notes=('Last, the exit check. Three questions. Write your answers before you look at mine. One, which three parts make a result into a story? Two, name two things to say before you show a result. '
                         'Three, where do you confirm the terms of a free course? The short answers are on the slide. If you got all three, you are ready to present your course project. These questions are a self-check and nobody marks them. '
                         'This is the end of the course. Choose your first free course today, write the start date in your sheet, and send it to me. When you finish your course project you receive a certificate of completion from KLAi Professional Learning. Thank you for twenty-four sessions of hard work.')))

    # ------------------------------------------------------------------ sheet tasks
    sess['sheet_tasks'] = [
        dict(task=f'Open a new Google Sheet and call it Presentation plan. On a tab named plan, list the five slides (Question, Data, Evidence, Risk, Decision) in A2:A6 with these minutes in B2:B6: {", ".join(str(x) for x in pm)}. In B7 add them up. Then write one sentence for each slide about your own course project in C2:C6.',
             answer=f'B7 =SUM(B2:B6) gives {sum(pm)}. The five sentences are the learner\'s own; each answers its slide (question, data covered and left out, result beside baseline, risk with owner, decision).'),
        dict(task=f'Rehearsal tab. In A2:A6 write the slide names, in B2:B6 the planned seconds ({", ".join(str(x) for x in F["plan_sec"])}) and in C2:C6 these illustrative rehearsal seconds: {", ".join(str(x) for x in ps)}. In D2:D6 compute the seconds over plan (=C2-B2). Find the total rehearsal time and the slide that ran longest past its plan.',
             answer=f'D2:D6 give {", ".join(str(x) for x in F["over"])}. The total is =SUM(C2:C6) = {F["reh_total"]} seconds, which is {F["reh_total"] // 60} minutes {F["reh_total"] % 60} seconds, {F["reh_total"] - 600} seconds over ten minutes. '
                    f'The longest overrun is {F["plan_names"][F["over_idx"]]} at {F["over"][F["over_idx"]]} seconds: =INDEX(A2:A6,MATCH(MAX(D2:D6),D2:D6,0)). The fix is to cut one sentence from that slide. Learners then time their own talk.'),
        dict(task=f'Evidence tab. A model at decision threshold {CUT} was tested on {nt} loans with {dt} defaults. It flagged {n(F["flag2"])} loans, and {F["tp2"]} of them really defaulted. Put TP = {F["tp2"]}, FP = {F["fp2"]}, FN = {F["fn2"]}, TN = {n(F["tn2"])} in cells and compute recall, precision and accuracy with formulas. Write one evidence sentence that includes the baseline model (always predicts repaid).',
             answer=f'Recall =TP/(TP+FN) = {F["tp2"]}/{F["d_test"]} = {pct(F["rec2"])}%. Precision =TP/(TP+FP) = {F["tp2"]}/{F["flag2"]} = {pct(F["prec2"])}%, so about {F["per100"]} of every 100 flagged loans really default. Accuracy =(TP+TN)/(TP+FP+FN+TN) = {n(F["tp2"] + F["tn2"])}/{nt} = {pct(F["acc2"])}%. '
                    f'The baseline model is {pct(F["base_acc"])}% accurate and finds no defaults. Sample sentence: At decision threshold {CUT} the model finds {pct(F["rec2"], 0)}% of defaults while the baseline finds none, but only about {F["per100"]} in 100 flagged loans default.'),
        dict(task='Questions tab. Write three questions your manager or a colleague could ask you about your course project: one on method, one on the metric and one on risk. Write a two-sentence answer to each. Fill with gold the answer that says something is not finished.',
             answer='Method: the answer names the test data or the baseline the result was judged against. Metric: it names the cost behind the number, for example what a missed default costs. Risk: it names one risk with an owner and a review date. '
                    'An answer that says a check is not finished is a good answer.'),
        dict(task=f'Feedback tab. Present your talk to a partner for ten minutes, then swap. For each of the four checklist rows write Yes or Not yet for your partner, and one comment. To practise the formulas, type these illustrative entries in B2:B5: {", ".join(F["peer"])}. Count the rows that still say Not yet and find the first one. Nothing is scored.',
             answer=f'Rows still to improve: =COUNTIF(B2:B5,"Not yet") = {F["peer_open"]}. First one: =INDEX(A2:A5,MATCH("Not yet",B2:B5,0)) = {F["peer_low"]}. '
                    'Real feedback: four entries and four comments; each comment points to a named slide and at least one says what to keep.'),
        dict(task=f'Path tab. Write your six month path: three blocks (months 1 and 2, 3 and 4, 5 and 6), one named free course or project in each, and a weekly hour budget of {F["hours_week"]} hours. Compute the total hours over {F["weeks"]} weeks and compare with the 48 hours of this course. Rewrite your business question from Session 1 in one sentence using what you know now.',
             answer=f'Total hours =B1*B2 = {F["hours_week"]} x {F["weeks"]} = {F["path_hours"]}. Compared with this course: =B3/48 = {F["path_hours"] / 48:.2f} times as many hours. Each block names one course from the gap list and a start date, and notes that the current terms were checked. '
                    'The rewritten question is the learner\'s own and should be narrower and name a decision.'),
    ]

    # ------------------------------------------------------------------ facilitator
    sess['facilitator'] = dict(
        prep=['Ask learners to bring the project question, the data they used and the result and limits from Sessions 13 to 23. Learners who have no course project use the Nile Microfinance loan story on the slides.',
              'Pair learners before the break. Each pair needs two timers (phones are fine) and a shared view of one feedback tab.',
              'Write the check table (slide 22 of the deck) on the board before the lab.',
              'Check the free-course list against each provider page the week before. Free audit and certificate rules change.',
              'Plan the last five minutes so that every learner names a first course and a start date aloud.'],
        misconceptions=[('A high accuracy number is enough to present', f'Always give the baseline model beside it. Always saying repaid is {pct(F["base_acc"])}% accurate on the test loans.'),
                        ('Say the strongest result first, and the limits at the end', 'State what the data covers and what the model cannot do before the result. The room then trusts the result.'),
                        ('Technical terms are impressive in a talk to a manager', 'Use the real term once and give its plain meaning, then use the plain meaning if the term is not needed.'),
                        ('A portfolio can include my workplace data if I remove the names', 'Use generated or public data. Workplace data stays in workplace systems unless your employer agrees in writing.'),
                        ('The free courses make me job ready', 'They extend this base. The hours quoted for certificates are far higher than this course, so name the gaps plainly.')],
        probes=[('What are the three parts of the story?', 'The answer, the evidence beside a baseline model, and the limits.'),
                ('What goes in an executive summary?', 'The answer, the evidence, the main limit and the request, in about four sentences.'),
                ('Why say the limits first?', 'The room trusts the result that follows, and nothing is hidden.'),
                ('What does recall mean to a manager?', 'Of every 100 loans that default, how many we flag.'),
                ('What goes in a README?', 'The question, the result, the limits and how to run it.'),
                ('What never goes in a public repository?', 'Personal data and passwords, keys or tokens.'),
                ('Where do you check the terms of a free course?', 'On the provider page, before you start.')],
        lab_steps=[('Task 1: plan', f'Five slides, minutes {", ".join(str(x) for x in pm)}, total {sum(pm)}. Sentences about the learner\'s own course project.'),
                   ('Task 2: rehearsal', f'Total {F["reh_total"]} s on the illustrative data, {F["plan_names"][F["over_idx"]]} longest. Then learners time their own talk and aim for 9 to 11 minutes.'),
                   ('Task 3: evidence', f'Recall {pct(F["rec2"])}%, precision {pct(F["prec2"])}%, accuracy {pct(F["acc2"])}%. The sentence must include the baseline model.'),
                   ('Task 4: questions', 'Three answers. Praise an answer that says a check is not finished.'),
                   ('Task 5: feedback', f'Illustrative: {F["peer_open"]} row still to improve, the first is {F["peer_low"]}. Real entries come from partners, with one comment per row.'),
                   ('Task 6: path', f'{F["path_hours"]} hours. Each block names a course, a start date and the weekly hours.')],
        rescue=['If the concepts run over, shorten the gap list (slide 14) and the hours chart (slide 16). The lab covers the path.',
                'If only 30 minutes of lab remain, do tasks 1, 2, 4 and 5, and set tasks 3 and 6 as homework.',
                'If a learner has no course project, they present the loan story from the slides with the numbers on the evidence table.',
                'If the group is small or odd, one learner presents to the tutor.'],
        after=['Collect each learner\'s course project link and first course by message the same day. The certificate of completion from KLAi Professional Learning goes to learners who finish the course project.', 'Share the deck again for absent learners.', 'Remind learners that their published work is public: check for personal data before pushing.'],
        lab_answer_key=[['Task 1 PREDICT: do your minutes add to 10?', f'They should: {" + ".join(str(x) for x in pm)} = {sum(pm)}.'],
                        ['Task 2 READ: which slide do you cut from, and why?', f'The one that ran longest past its plan, here {F["plan_names"][F["over_idx"]]}, {F["over"][F["over_idx"]]} seconds over.'],
                        ['Task 3 READ: why include the baseline in the sentence?', f'Without it, {pct(F["acc2"])}% accuracy looks weak and {pct(F["base_acc"])}% for doing nothing looks strong. The baseline gives the number meaning.'],
                        ['Task 3 CHANGE: if flagged loans rise to 500 with 140 real defaults, what is precision?', '140 / 500 = 28.0%.'],
                        ['Task 4 READ: which answer says something is not finished, and is that a weakness?', 'It is a strength. A stated limit builds trust.'],
                        ['Task 5 READ: which row still says Not yet, and what does it tell your partner?', f'It is the row to improve first, here {F["peer_low"]}.'],
                        ['Task 6 CHANGE: use 4 hours a week. What is the total?', f'4 x {F["weeks"]} = {4 * F["weeks"]} hours.']])
    return sess
