"""Session 15: Conditional probability and Bayes. Joint, marginal, conditional, independence, Bayes' theorem, natural frequencies, Naive Bayes spam filter."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'kit'))
import diagrams_math_e  # noqa: E402,F401

# ---------------------------------------------------------------- numbers
N_SPAM, N_HAM = 40, 60
N_ALL = N_SPAM + N_HAM
COUNTS = {'free': (28, 6), 'prize': (20, 0), 'meeting': (4, 30)}       # emails containing the word: (spam, ham)
TABLE = [[28, 12], [6, 54]]                                              # rows spam, ham; columns free, no free
P_FREE = 34 / 100
P_SPAM = 0.4
P_JOINT = 28 / 100
P_SPAM_GIVEN_FREE = 28 / 34
P_FREE_GIVEN_SPAM = 28 / 40
EXP_SPAM_FREE = 40 * 34 / 100
EXP_HAM_FREE = 60 * 34 / 100

PREV, SENS, FPR = 0.01, 0.90, 0.10
SICK_POS, HEALTHY_POS = 9, 99
POST1 = SICK_POS / (SICK_POS + HEALTHY_POS)
POST2 = SENS * POST1 / (SENS * POST1 + FPR * (1 - POST1))


def like(word, cls):
    k = COUNTS[word][cls]
    n = N_SPAM if cls == 0 else N_HAM
    return (k + 1) / (n + 2)


def score(present, absent):
    out = []
    for cls, prior in ((0, N_SPAM / N_ALL), (1, N_HAM / N_ALL)):
        v = prior
        for w in present:
            v *= like(w, cls)
        for w in absent:
            v *= 1 - like(w, cls)
        out.append(v)
    return out


E1 = score(['free', 'prize'], ['meeting'])
E2 = score(['free', 'meeting'], ['prize'])
POST_E1 = E1[0] / sum(E1)
POST_E2 = E2[0] / sum(E2)
LOG_E1 = [float(np.log(v)) for v in E1]


def build():
    s = dict(
        num=15, block='Probability and statistics', short_title='Conditional probability and Bayes',
        title='Conditional probability and Bayes: updating beliefs with evidence',
        question='A test finds 90% of sick people and wrongly flags 10% of healthy people. You test positive. How likely are you sick?',
        outcomes=['Read joint, marginal and conditional probabilities from a table of counts, and test for independence',
                  'Apply Bayes theorem with natural frequencies, naming the prior, likelihood and posterior',
                  'Build a small Naive Bayes spam classifier by hand and in code, and read a model probability with care'],
        outcome_icons=['grid', 'calculator', 'shield'],
        outcome_note=('By the end of today you can do three things. Read joint, marginal and conditional probabilities from a table of counts, and test whether two events are independent. '
                      'Apply Bayes theorem using natural frequencies, and name the prior, the likelihood and the posterior. '
                      'And build a small Naive Bayes spam filter by hand and in code, and then read a probability from a model with care. That includes the caution that a fluent answer from a language model is not a probability that it is true.'),
        clock=[(10, 'Recall and a real question from AI'), (35, 'Concept: a picture, then a hand example'), (10, 'Break'), (45, 'Lab: Python or spreadsheet, predict, run, change one thing'),
               (15, 'Where it appears in AI, plus an exit check'), (5, 'Save the work')],
        plan_title='Your two hours: counts, Bayes, a spam filter, then AI',
        plan_caption='Tables of counts first, then Bayes with natural frequencies, then the spam filter by hand and in the lab.',
        plan_note=('We start with ten minutes of recall from Session 14 and the question about a positive medical test. Then thirty-five minutes of concepts, a picture first and a hand example after it. '
                   'After the break you spend forty-five minutes in the lab, in Python or in a spreadsheet, on the same numbers. We finish with where this appears in AI, an exit check, and saving your work.'),
        recall_from='Session 14',
        recall=[('What does lowering the temperature do to the next-word probabilities?', 'It sharpens them: the top word gets more probability, and answers repeat more.'),
                ('What does a standard error measure?', 'How much a sample mean wanders from sample to sample: sigma divided by the square root of n.'),
                ('An A/B test gives p = 0.039. What does that mean?', 'A gap this large would be rare if there were truly no difference. It is not a 3.9% chance that the feature does nothing.')],
        words=[('Conditional probability', 'P(A | B): the probability of A once we know B happened.'),
               ('Independence', 'Two events are independent when knowing one does not change the probability of the other.'),
               ('Prior, likelihood and posterior', 'The belief before evidence, the chance of the evidence if the hypothesis is true (for a test: its sensitivity), and the updated belief.'),
               ("Bayes' theorem", 'The rule P(H | E) = P(E | H) P(H) / P(E): the posterior from the likelihood, the prior and the evidence.'),
               ('Naive Bayes classifier', 'A classifier that multiplies per-word likelihoods, naively treating the words as independent.')],
        word_icons=['question', 'switch', 'chart', 'calculator', 'shield'],
        words_note=('Five words today. Conditional probability is the probability of one event once we know another has happened. Independence means knowing one tells us nothing about the other. '
                    'Prior, likelihood and posterior are the three parts of an update. Bayes theorem is the rule that connects them. And a Naive Bayes classifier is a small, honest spam filter built from counts. '
                    'We use each of them in a worked example before the break.'),
        keep='Keep your saved lab and these numbers: P(spam given free) = 0.8235, the medical test posterior 0.0833, and the spam posteriors 0.9955 and 0.3304.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Saved lab', value='Notebook or workbook'), dict(label='Key numbers', value='See the check table'),
                                                              dict(label='Next session', value='Maximum likelihood'), dict(label='Bring', value='A question on Bayes')]),
        keep_title='Save the lab and keep your key numbers',
        next='Session 16: maximum likelihood and MAP. We see why squared error and cross-entropy are the right losses.', next_label='Next session',
        keep_note=('Before you go, save your notebook or workbook and keep the key numbers from the check table. Next session is maximum likelihood and MAP. '
                   'Today you met the prior, the likelihood and the posterior, and in Session 16 they become the language for training a model, including why weight decay is a prior. '
                   'If the medical test result is still surprising, write your question down and bring it.'),
        cover_note=('Welcome to Session 15, the last session on probability itself. Today is about updating a belief when evidence arrives. '
                    'We start with a famous surprise: a test that finds 90 percent of sick people, and wrongly flags 10 percent of healthy people, says positive, and the chance you are sick is under 10 percent. Then we turn the same rule into a small spam filter. '
                    'We close with how to read a probability that an AI model gives you.'),
        slides=[])
    S = s['slides']

    S.append(dict(kind='table', title='Answers to the three questions from Session 14', headers=['Question', 'Short answer'], rows=[[q, a] for q, a in s['recall']], widths=[5.2, 6.8], icons=False,
                  note='If an answer surprised you, look back at Session 14 before the lab.',
                  notes=('Here are the short answers. Lowering the temperature sharpens the next-word probabilities, so the top word gets more and answers repeat. '
                         'The standard error measures how much a sample mean wanders from sample to sample, and it is sigma over the square root of n. '
                         'And a p-value of 0.039 says that a gap this large would be rare if there were truly no difference. It does not say there is a 3.9 percent chance that the feature does nothing. Check your own answers against these.')))

    S.append(dict(kind='idea', title='A table of counts shows joint and marginal probabilities',
                  visual=dict(kind='e_table2', row_labels=['Spam', 'Ham (not spam)'], col_labels=['Contains "free"', 'No "free"'], counts=TABLE, hl=[[0, 0]], corner='100 emails'),
                  lead='Illustrative: 100 emails, 40 spam and 60 ham, sorted by whether they contain the word "free".',
                  points=['Joint probability: P(spam and free) = 28 / 100 = 0.28 (gold).', 'Marginal probability: one event on its own, from a row or column total. P(free) = 34 / 100 = 0.34.', 'P(spam) = 40 / 100 = 0.40.'],
                  notes=('Here is a small table of counts. It is illustrative, made up to show the arithmetic. One hundred emails, forty of them spam and sixty ham, and in each row we count how many contain the word free. '
                         'The gold cell is a joint probability: twenty-eight emails are both spam and contain free, so the probability of both is 0.28. '
                         'A marginal probability comes from a total in the margin of the table. Thirty-four emails contain free, so the marginal probability of free is 0.34. Forty are spam, so the marginal probability of spam is 0.40. What is the marginal probability of ham?')))

    S.append(dict(kind='idea', title='A conditional probability looks only at the emails where the condition holds',
                  visual=dict(kind='e_table2', row_labels=['Spam', 'Ham (not spam)'], col_labels=['Contains "free"', 'No "free"'], counts=TABLE, hl=[[0, 0]], hl_total=[['tot', 'col', 0]], corner='100 emails'),
                  lead='Given that an email contains "free", only the 34 emails in the first column matter.',
                  points=[f'P(spam | free) = 28 / 34 = {P_SPAM_GIVEN_FREE:.4f}.', f'P(free | spam) = 28 / 40 = {P_FREE_GIVEN_SPAM:.2f}.', 'The two are different questions with different answers.'],
                  notes=('Now a conditional probability. We write P of A given B, with a vertical bar. It means: restrict attention to the cases where B is true, and ask how often A is true among them. '
                         f'Suppose an email contains the word free. Only the 34 emails in the first column remain, and 28 of them are spam, so P of spam given free is 28 over 34, {P_SPAM_GIVEN_FREE:.4f}. '
                         f'Turn it around. Among the 40 spam emails, 28 contain free, so P of free given spam is {P_FREE_GIVEN_SPAM:.2f}. The two numbers differ, and mixing them up is the commonest mistake in this topic.')))

    S.append(dict(kind='formula', title='Joint, marginal and conditional probability',
                  formulas=[('Conditional', r'$P(A \mid B) = \frac{P(A\ \mathrm{and}\ B)}{P(B)}$'), ('Product rule', r'$P(A\ \mathrm{and}\ B) = P(B)\,P(A \mid B)$')],
                  symbols=[['P(A and B)', 'The joint probability: both events happen.', 'P(spam and free) = 0.28'],
                           ['P(B)', 'The marginal probability of the condition.', 'P(free) = 0.34'],
                           ['P(A | B)', 'The conditional probability: A given B.', f'0.28 / 0.34 = {P_SPAM_GIVEN_FREE:.4f}']],
                  widths=[1.9, 5.9, 4.1], size=22, note='The product rule is the same formula rearranged: 0.34 × 0.8235 = 0.28.',
                  notes=('Here are the formulas. The conditional probability of A given B is the joint probability of A and B, divided by the marginal probability of B. '
                         'That is the same as our counting argument, with the counts divided by 100. For our emails, 0.28 divided by 0.34 gives 0.8235. '
                         'Rearrange it and you get the product rule: the joint probability is P of B times P of A given B. Check it: 0.34 times 0.8235 is 0.28. This rule is the engine behind Bayes theorem.')))

    S.append(dict(kind='idea', title='Independent events do not change each other\'s probability: "free" and spam are not independent',
                  visual=dict(kind='sheet', headers=['', 'Contains "free": observed', 'Expected if independent'], rows=[['Spam', '28', f'{EXP_SPAM_FREE:.1f}'], ['Ham', '6', f'{EXP_HAM_FREE:.1f}']], hl=[0, 1], size=18),
                  lead='Independent means P(A and B) = P(A) × P(B).',
                  points=[f'If independent: P(spam) × P(free) = 0.40 × 0.34 = {0.4 * 0.34:.3f}, so 13.6 emails.', 'Observed: 28 emails. Far more than 13.6.', 'So the word carries information about spam. A filter can use it.'],
                  notes=('Two events are independent when knowing one tells you nothing about the other. Two dice are independent: the first die does not change the second. '
                         'Then the probability of both is the product of the two probabilities. Test it on our emails. If free and spam were independent, we would expect 0.4 times 0.34 of the 100 emails to be spam containing free, which is 13.6. '
                         'We actually observe 28. The gap tells us the word is informative, which is exactly why a spam filter can use it.')))

    S.append(dict(kind='wide', title='Natural frequencies: of 1,000 people, 9 sick people test positive and 99 healthy people test positive',
                  visual=dict(kind='e_natfreq', root='1,000 people', mid=[dict(text='10 have the disease'), dict(text='990 do not')],
                              leaves=[[dict(text='9 test positive', hl=True), dict(text='1 tests negative')], [dict(text='99 test positive', hl=True), dict(text='891 test negative')]],
                              edges=[['1%', '99%'], [['90%', '10%'], ['10%', '90%']]]),
                  caption='Illustrative: 1% sick. Sensitivity 90% (sick found). False positive rate 10% (healthy flagged).',
                  notes=('Now the famous surprise, with natural frequencies. Natural frequencies means we count people instead of juggling percentages. All numbers are illustrative. Take a thousand people. '
                         'One percent are sick, that is ten. The test catches ninety percent of them, a rate called the sensitivity, so nine test positive. Of the 990 healthy people, ten percent are wrongly flagged, which is 99 people. That ten percent is the false positive rate. '
                         'Now you test positive. You are one of the gold boxes: 9 plus 99, 108 people. Only 9 of them are sick. What fraction is that?')))

    S.append(dict(kind='idea', title=f'A positive test moves the belief from 1% to {100 * POST1:.1f}%, and a second positive test to {100 * POST2:.0f}%',
                  visual=dict(kind='bars', items=[dict(label='Before any test (prior)', value=1), dict(label='After one positive test', value=round(100 * POST1, 1), hl=True), dict(label='After two positive tests', value=round(100 * POST2, 1))], unit='%', max_value=50),
                  lead=f'Chance of being sick: 9 / (9 + 99) = {POST1:.4f} after one positive test.',
                  points=['Most positives come from the many healthy people.', 'A second positive test lifts it to 45%, if its error is independent of the first.', 'Evidence updates a belief. It does not replace it.'],
                  notes=(f'Here is the answer as a picture. Before the test, your chance of being sick is the prevalence, 1 percent. After one positive test it is 9 out of 108, which is {100 * POST1:.1f} percent. '
                         'Most positive results come from the huge group of healthy people, even though each has only a ten percent chance of a false alarm. '
                         f'If you take a second, independent test and it is positive too, the belief rises to {100 * POST2:.0f} percent. This assumes the second test makes errors independent of the first. Repeat tests on the same person often do not. Evidence updates a belief. It does not replace the prior. That is Bayes theorem in action.')))

    S.append(dict(kind='formula', title="Bayes' theorem: prior, likelihood, evidence and posterior",
                  formulas=[("Bayes' theorem", r'$P(H \mid E) = \frac{P(E \mid H)\,P(H)}{P(E)}$'), ('Evidence', r'$P(E) = P(E \mid H)\,P(H) + P(E \mid \mathrm{not}\ H)\,P(\mathrm{not}\ H)$')],
                  symbols=[['P(H)', 'Prior: belief in the hypothesis H (sick) before the evidence E (a positive test).', '0.01'],
                           ['P(E | H)', 'Likelihood (here the sensitivity): how likely the evidence is if H is true.', '0.90'],
                           ['P(E)', 'Marginal likelihood of the evidence, also just called the evidence: 0.9 × 0.01 + 0.1 × 0.99.', f'{SENS * PREV + FPR * (1 - PREV):.3f}'],
                           ['P(H | E)', 'Posterior: the updated belief after the evidence.', f'0.009 / 0.108 = {POST1:.4f}']],
                  widths=[1.7, 6.5, 3.7], size=20, note='The same 9 / 108 as the natural frequencies, with probabilities instead of counts.',
                  notes=('Here is the rule with proper names. We want the posterior, P of H given E, the belief after the evidence. It equals the likelihood, P of E given H, times the prior, P of H, divided by the evidence, P of E. '
                         f'The evidence is the overall chance of a positive test: ninety percent of one percent, plus ten percent of ninety-nine percent, which is {SENS * PREV + FPR * (1 - PREV):.3f}. '
                         f'The top is 0.9 times 0.01, which is 0.009. Divide, and you get {POST1:.4f}. It is the same 9 out of 108 you got by counting people.')))

    S.append(dict(kind='compare', title='The most common mistake is to swap P(E | H) and P(H | E)',
                  left=dict(head='P(positive | sick) = 0.90', icon='chart', points=['How well the test finds sick people', 'The likelihood, set by the test maker']),
                  right=dict(head='P(sick | positive) = 0.083', icon='question', points=['What you want to know after a positive result', 'The posterior, which also needs the prior']),
                  verdict='Ignoring the prior (the base rate) is called base rate neglect.',
                  notes=('Here is the mistake in one slide. On the left, ninety percent is the probability of a positive test given that you are sick. That is the likelihood, and it describes the test. '
                         'On the right, 8.3 percent is the probability that you are sick given a positive test. That is the posterior, and it also depends on how rare the disease is. '
                         'People often read the first number as if it were the second. Forgetting the base rate in this way is called base rate neglect. Which one does a patient actually care about?')))

    S.append(dict(kind='idea', title='A tiny table of word counts is all a Naive Bayes spam filter needs',
                  visual=dict(kind='sheet', headers=['Word', 'Spam emails (of 40)', 'Ham emails (of 60)'], rows=[['free', '28', '6'], ['prize', '20', '0'], ['meeting', '4', '30']], hl=[1, 2], size=18),
                  lead='Illustrative training counts: how many emails of each class contain each word.',
                  points=['Prior: P(spam) = 40 / 100 = 0.4 and P(ham) = 0.6.', '"free" and "prize" point to spam. "meeting" points to ham.', 'The gold zero is a problem: no ham email contained "prize".'],
                  notes=('Here is the training data for a tiny spam filter. It is illustrative. Out of 100 training emails, 40 are spam and 60 are ham. For three words we count how many emails of each class contain the word. '
                         'The priors come straight from the class sizes: 0.4 for spam and 0.6 for ham. Free and prize lean to spam, and meeting leans to ham. '
                         'Now look at the gold zero. No ham email contained prize. That sounds harmless, but a zero will wreck a multiplication, as we are about to see.')))

    sm = lambda word, cls: like(word, cls)
    S.append(dict(kind='idea', title='Add-one smoothing turns each count into a likelihood and removes the zero',
                  visual=dict(kind='sheet', headers=['P(word | class)', 'Spam', 'Ham'], rows=[[w, f'{sm(w, 0):.3f}', f'{sm(w, 1):.3f}'] for w in ('free', 'prize', 'meeting')], hl=[1, 2], size=18),
                  lead='Likelihood = (count + 1) / (emails in the class + 2). This is add-one (Laplace) smoothing.',
                  points=['free, spam: (28 + 1) / (40 + 2) = 0.690.', 'prize, ham: (0 + 1) / (60 + 2) = 0.016, not 0.', 'A zero would make it impossible for any email with "prize" to be ham.'],
                  notes=('To turn counts into likelihoods we use a small trick called add-one smoothing, also known as Laplace smoothing. Add one to the count, and add two to the class size. '
                         'For free in spam that gives 29 over 42, which is 0.690. For prize in ham, instead of zero we get 1 over 62, which is 0.016: small but not zero. '
                         'Without smoothing, one unseen word would force the ham probability to exactly zero, and no other evidence could ever win it back. A filter should never be that certain from a few emails.')))

    S.append(dict(kind='formula', title='Naive Bayes: multiply the prior by one likelihood per word',
                  formulas=[('Naive Bayes score', r'$\mathrm{score}(c) = P(c)\prod_{w} q(w, c)$'), ('Posterior', r'$P(\mathrm{spam} \mid \mathrm{words}) = \frac{\mathrm{score}(\mathrm{spam})}{\mathrm{score}(\mathrm{spam}) + \mathrm{score}(\mathrm{ham})}$')],
                  symbols=[['P(c)', 'The prior of the class c (spam or ham).', '0.4 and 0.6'],
                           ['P(w | c)', 'The smoothed likelihood of word w present. For an absent word use 1 - P(w | c).', 'table on the previous slide'],
                           ['q(w, c)', 'The factor for word w: P(w | c) if w is in the email, 1 - P(w | c) if not.', 'one per word'],
                           ['product', 'Multiply over all the words. "Naive": treat the words as independent.', 'three words']],
                  widths=[1.7, 6.7, 3.5], size=18, note='The words are not truly independent, so the method is naive, yet it works well for spam.',
                  notes=('Here is Naive Bayes. For each class, multiply the prior by one likelihood for each word. A word that is present contributes its likelihood. A word that is absent contributes one minus its likelihood. '
                         'The word naive refers to the big simplifying assumption: given the class, the words are treated as independent of each other. That is not true, free and prize often come together, but it makes the arithmetic tiny. '
                         'Then the posterior is the spam score divided by the sum of both scores. The next two slides do it by hand.')))

    ex = lambda present, absent, sc: [['Prior', f'{0.4:.3f}', f'{0.6:.3f}']] + [[f'"{w}" present', f'{like(w, 0):.3f}', f'{like(w, 1):.3f}'] for w in present] + [[f'"{w}" absent', f'{1 - like(w, 0):.3f}', f'{1 - like(w, 1):.3f}'] for w in absent] + \
                                      [['Score (product)', f'{sc[0]:.5f}', f'{sc[1]:.5f}'], ['Posterior', f'{sc[0] / sum(sc):.4f}', f'{sc[1] / sum(sc):.4f}']]
    S.append(dict(kind='idea', title=f'By hand, email 1 has "free" and "prize" but no "meeting": spam with probability {POST_E1:.4f}',
                  visual=dict(kind='sheet', headers=['Step', 'Spam', 'Ham'], rows=ex(['free', 'prize'], ['meeting'], E1), hl=[5, 1], size=16),
                  lead='Multiply down each column, then divide the spam score by the total.',
                  points=[f'Spam score {E1[0]:.5f}. Ham score {E1[1]:.5f}.', f'Posterior = {E1[0]:.5f} / {sum(E1):.5f} = {POST_E1:.4f}.', 'Strong evidence: spam by a wide margin.'],
                  notes=('Email one contains free and prize, but not meeting. Start each column with the prior. Multiply by the likelihood of free, then of prize, then by one minus the likelihood of meeting, because meeting is absent. '
                         f'Spam comes to {E1[0]:.5f}. Ham comes to a tiny {E1[1]:.5f}, dragged down by prize, which almost never appears in ham. '
                         f'Divide the spam score by the total and the posterior is {POST_E1:.4f}. The filter is very sure this one is spam.')))

    S.append(dict(kind='idea', title=f'Email 2 has "free" and "meeting" but no "prize": the filter leans to ham ({100 * POST_E2:.0f}% spam)',
                  visual=dict(kind='sheet', headers=['Step', 'Spam', 'Ham'], rows=ex(['free', 'meeting'], ['prize'], E2), hl=[5, 1], size=16),
                  lead='Same method. The word "meeting" and the missing "prize" now point to ham.',
                  points=[f'Spam score {E2[0]:.5f}. Ham score {E2[1]:.5f}.', f'Posterior = {E2[0]:.5f} / {sum(E2):.5f} = {POST_E2:.4f}.', 'Not sure: about one chance in three of spam.'],
                  notes=('Email two says free lunch at the meeting. It contains free and meeting, but not prize. The same method. Multiply the prior by 0.690 for free, 0.119 for meeting, and one minus 0.5 for the missing prize. '
                         f'Spam scores {E2[0]:.5f}. For ham we have 0.113 for free, 0.5 for meeting and 0.984 for the missing prize, and the score is {E2[1]:.5f}. '
                         f'The posterior for spam is {POST_E2:.4f}. A real filter would use a threshold, say flag above 0.9, so this email goes to the inbox. Which words pushed it towards ham?')))

    S.append(dict(kind='idea', title='Many words multiply many small numbers, so we add logarithms instead',
                  visual=dict(kind='flow', steps=[dict(head='Multiply', text='Hundreds of likelihoods', icon='calculator'), dict(head='Underflow', text='The product is too small for the computer', icon='cross'),
                                                  dict(head='Add logs', text='ln of a product = sum of the ln of the factors', icon='notebook'), dict(head='Softmax', text='Scores back to probabilities', icon='chart')], highlight=2),
                  lead='Session 1 gave us logarithms, and Session 12 gave us the stable softmax. Both are used here.',
                  points=[f'ln(score(spam)) = {LOG_E1[0]:.3f}. ln(score(ham)) = {LOG_E1[1]:.3f}.', f'Softmax of these two numbers gives {POST_E1:.4f}, the same posterior.'],
                  notes=('A real spam filter uses thousands of words, so it multiplies thousands of numbers below one, and the product underflows to zero. The fix uses two tools from earlier sessions. '
                         'The logarithm of a product is the sum of the logarithms, so we add instead of multiplying. Then softmax, in its stable form, turns the log scores back into probabilities. '
                         f'For email one the log scores are {LOG_E1[0]:.3f} and {LOG_E1[1]:.3f}, and softmax gives {POST_E1:.4f}. It is the same posterior, now safe for long emails.')))

    S.append(dict(kind='code', title='Bridge: Naive Bayes from counts in NumPy',
                  code='spam = np.array([28, 20, 4])\nham = np.array([6, 0, 30])\nls = (spam + 1) / 42\nlh = (ham + 1) / 62\nhas = np.array([1, 1, 0])\nps = 0.4 * np.prod(np.where(has == 1, ls, 1 - ls))\nph = 0.6 * np.prod(np.where(has == 1, lh, 1 - lh))\nps / (ps + ph)',
                  reads=['Lines 1 and 2: the word counts for free, prize and meeting.', 'Lines 3 and 4: smoothed likelihoods.', 'Line 5: 1 if the word is in the email, 0 if not.',
                         'Lines 6 and 7: where picks the likelihood if present, one minus it if absent. prod multiplies.', 'Line 8: the posterior of spam.'],
                  notes=('Here is the same filter in code. The counts go into two arrays, and the smoothed likelihoods are one line each. A vector called present records which words are in the email. '
                         'The where function picks the likelihood for a present word and one minus the likelihood for an absent word, and prod multiplies them. Then we multiply by the prior. '
                         'The last line divides the spam score by the total, and for present equal to 1, 1, 0 it gives 0.9955. In the spreadsheet you build the same steps in a table.')))

    S.append(dict(kind='divider', title='Part 2: the lab', lead='Close the slides. Open the notebook or the workbook.', section='Lab',
                  notes=('That is the end of the concepts. Please open either the Python notebook or the spreadsheet workbook. Both use the same counts and the same two emails. '
                         'In each step, predict first, then run, then read the output, then change one thing. I will walk around. Raise your hand if a cell gives an error.')))

    S.append(dict(kind='steps', title='The lab has five stages, in Python and in the spreadsheet',
                  steps=[dict(head='1 Table', text='Joint, marginal and conditional', icon='grid'), dict(head='2 Independence', text='Observed against expected', icon='switch'), dict(head='3 Medical test', text='Bayes and a second test', icon='shield'),
                         dict(head='4 Spam filter', text='Likelihoods and two emails', icon='mail'), dict(head='5 Break it', text='Remove the smoothing', icon='cross')], highlight=3,
                  caption='Python notebook: Session 15. Workbook sheets: Counts, Medical and NaiveBayes. Predict first, run, read, then change one thing.',
                  notes=('Here is the plan. Stage one, joint, marginal and conditional probabilities from the table of counts. Stage two, a check of independence. Stage three, the medical test with Bayes theorem, and a second test. '
                         'Stage four, the Naive Bayes filter: smoothed likelihoods and the posteriors of two emails. Stage five, take away the smoothing and watch the filter become overconfident. '
                         'The workbook has a sheet for each, with gold cells to fill.')))

    S.append(dict(kind='table', title='Check your numbers against these before you move on', headers=['What you compute', 'You should see'],
                  rows=[['P(spam and free), P(free), P(spam | free)', f'0.28, 0.34, {P_SPAM_GIVEN_FREE:.4f}'], ['P(free | spam)', f'{P_FREE_GIVEN_SPAM:.2f}'], ['Expected spam emails with "free" if independent', f'{EXP_SPAM_FREE:.1f}'],
                        ['Medical test: P(E), posterior after one positive test', f'{SENS * PREV + FPR * (1 - PREV):.3f}, {POST1:.4f}'], ['Posterior after a second independent positive test', f'{POST2:.2f}'],
                        ['Smoothed likelihood of "free" in spam and of "prize" in ham', f'{like("free", 0):.4f}, {like("prize", 1):.4f}'], ['Posterior spam probability of email 1 and email 2', f'{POST_E1:.4f}, {POST_E2:.4f}'],
                        ['CHANGE task: email 1 with no smoothing', '1.0000 (overconfident)']],
                  widths=[7.4, 4.4], icons=False, note='If your number differs, stop and find the step that went wrong. Do not change a number to match.',
                  notes=('Use this table as your checkpoint. Each row names what you compute and the number you should see. The conditional probabilities come from the table of counts. '
                         'The medical posterior is 0.0833 after one positive test and 0.45 after two. The two spam posteriors are 0.9955 and 0.3304. '
                         'The last row is the experiment where you remove the smoothing: the filter becomes certain, which is a warning. If a number differs, stop and call me.')))

    S.append(dict(kind='table', title='Errors you will meet, what they mean and what to do', headers=['Where', 'What you see', 'What to do'],
                  rows=[['Both', 'P(spam | free) is 0.7', 'You divided by 40 instead of 34. Divide by the emails with the condition.'],
                        ['Both', 'Posterior 0.0900 instead of 0.0833', 'You used 0.1 as P(E). Add both routes: 0.9 × 0.01 + 0.1 × 0.99 = 0.108. (Forgetting the false positives gives 1.0.)'],
                        ['Python', 'RuntimeWarning: divide by zero in log', 'A likelihood is 0. Use the smoothed likelihood (count + 1) / (n + 2).'],
                        ['Spreadsheet', 'Posterior above 1', 'The ham score was not added to the denominator.'],
                        ['Both', 'Likelihood of an absent word is wrong', 'Use 1 - P(word | class) for a word that is not in the email.']],
                  widths=[2.0, 4.3, 5.7], icons=['cross'] * 5,
                  notes=('Here are the errors you will probably meet. If P of spam given free comes out as 0.7, you divided by the number of spam emails instead of the number of emails with the word. '
                         'If the posterior is 0.09 instead of 0.0833, you used 0.1 as the evidence, so add both routes to a positive test. Forgetting the false positives altogether would give 1.0. A divide by zero warning means an unsmoothed likelihood of zero. '
                         'A posterior above one means the denominator is missing the ham score. And for an absent word, use one minus the likelihood. Read the message first.')))

    S.append(dict(kind='idea', title='Where this appears in AI: spam filters and medical-risk classifiers',
                  visual=dict(kind='flow', steps=[dict(head='Email', text='Words are counted', icon='mail'), dict(head='Model', text='Prior and one likelihood per word', icon='calculator'), dict(head='Probability', text='Posterior of spam', icon='chart'),
                                                  dict(head='Decision', text='Flag above a threshold', icon='flag')], highlight=2),
                  lead='A prior, likelihoods and a posterior run in many classifiers.',
                  points=['Sahami and colleagues published Bayesian junk email filtering in 1998.', 'A medical-risk classifier needs the base rate too.', 'Chat assistants are language models, not Naive Bayes.'],
                  notes=('Here is where today appears. Spam filtering with Bayes rule was published by Sahami and colleagues in 1998, and the pattern of a prior, likelihoods and a posterior sits in many classifiers since. '
                         'A medical-risk classifier works the same way: its probability needs the base rate to mean anything. '
                         'Chat assistants such as ChatGPT, Gemini and Claude are not Naive Bayes classifiers. They are language models, but they still output probabilities, and the next two slides show how to read those.')))

    S.append(dict(kind='idea', title='Where this appears in AI: a stated probability should be checked against how often it is right',
                  visual=dict(kind='sheet', headers=['Stated confidence', 'Cases', 'Actually right', 'Rate'], rows=[['90%', '200', '150', '75%'], ['70%', '300', '216', '72%'], ['50%', '100', '49', '49%']], hl=[0, 3], size=18),
                  lead='Illustrative (made-up) check: the model says 90% but is right 75% of the time.',
                  points=['Calibrated: stated probability equals the hit rate.', 'Guo and colleagues, 2017: many neural networks are over-confident.'],
                  notes=('How should you read a probability from a model? Compare it with how often the model is right. This table is illustrative. Among 200 cases where the model said ninety percent, it was right 150 times, which is 75 percent. That model is over-confident. '
                         'When stated probability matches the observed rate, we say the model is calibrated. Guo and colleagues reported in 2017 that many modern neural networks are over-confident. '
                         'So a ninety percent from a model is not a guarantee. It is a claim to be tested against a record of outcomes.')))

    S.append(dict(kind='compare', title='Where this appears in AI: a fluent answer is not a probability that it is true',
                  left=dict(head='What the model computes', icon='check', points=['The probability of the next token given the text', 'High for a likely wording']),
                  right=dict(head='What it does not give you', icon='cross', points=['The probability that the statement is true', 'A warning that a fluent sentence is false']),
                  verdict='Check important claims against a source or your own calculation.',
                  notes=('A caution that matters for everything you do with language models. A model computes the probability of the next token given the text so far. A high probability means the wording is a likely continuation. '
                         'It does not mean the statement is true. Researchers have documented fluent but false answers, often called hallucinations. '
                         'So the fluency of an answer is not evidence. For important claims, check a source or redo the calculation, just as you did with the medical test. Which of your own uses of an assistant needs this check?')))

    S.append(dict(kind='practice', title='Where this appears in AI: check an assistant on the medical test', minutes=8, label='Check an AI assistant',
                  task='Ask an AI assistant the medical test question with our made-up numbers.',
                  steps=['Say: 1% are sick, 90% of sick people test positive, and 10% of healthy people do too.', 'Ask: I tested positive. How likely am I sick?', f'Compare with 9 / 108 = {POST1:.4f}.', 'Ask how sure it is.'],
                  output='A note: its answer, the correct 8.3%, and what its confidence meant.',
                  notes=('A short activity. Give any AI assistant the medical test numbers, one percent prevalence, ninety percent of sick people found, ten percent of healthy people flagged, and ask how likely you are to be sick after a positive test. '
                         f'The right answer is 9 out of 108, {POST1:.4f}. See whether the assistant gets it, and whether it shows its steps. Then ask how sure it is, and think about what that statement means. '
                         'Use only made-up numbers like these, and never paste confidential data.')))

    S.append(dict(kind='table', title='Exit check: three questions', headers=['Question', 'Short answer'],
                  rows=[['In the 100 emails, P(free | spam) = 0.70 and P(spam | free) = 0.82. Why do they differ?', 'They condition on different groups: 40 spam emails against 34 emails with the word.'],
                        ['A disease affects 1 in 1,000. A test finds 99% of sick people and wrongly flags 1% of healthy people. Roughly how likely is a positive person to be sick?', 'About 9%. Of 1,000 people, about 1 sick positive and about 10 healthy positives: 1 / 11.'],
                        ['A language model gives a fluent answer. Is that the probability that it is true?', 'No. It reflects how likely the wording is. Check the claim.']],
                  widths=[6.6, 5.4], icons=False,
                  notes=('Three questions to finish. First, the two conditional probabilities differ because they restrict to different groups: forty spam emails against 34 emails with the word. '
                         'Second, a disease in one in a thousand, with a test that finds 99 percent and flags one percent of healthy people. Of a thousand people about one sick person tests positive and about ten healthy people do, so roughly one in eleven, about nine percent. '
                         'Third, a fluent answer is not the probability that it is true. Write your answers in your lab file.')))

    s['facilitator'] = dict(
        prep=['Open the deck, one notebook and one workbook. Run the notebook from the top once.', 'Write on the board: 0.8235, 0.0833, 0.45, 0.9955, 0.3304.',
              'Prepare the 1,000 people picture on the board: 10, 9, 99 and 108. Many learners need to count people before the formula makes sense.', 'Have the medical test question ready to ask the room before slide 8, and note the answers.'],
        misconceptions=[('P(A | B) and P(B | A) are about the same', 'They condition on different groups. A test that finds 90% of sick people can still leave a positive person only 8% likely to be sick.'),
                        ('If the test finds 90% of sick people, a positive result means 90% sick', 'The prior (base rate) matters. When the disease is rare, most positives are false alarms.'),
                        ('Independent means mutually exclusive', 'Exclusive events cannot happen together. Independent events do not change each other.'),
                        ('A zero count means the word can never appear', 'It means it was not seen in training. Smoothing keeps a little probability for it.'),
                        ('A model that says 95% is right 95% of the time', 'Only if it is calibrated. Many networks are over-confident. Check against outcomes.'),
                        ('A fluent answer from a chatbot is probably true', 'The model scores likely wording, not truth. Check important claims.')],
        probes=[('Why do the posterior and the likelihood differ so much in the medical test?', 'Because the disease is rare. There are 99 false positives for 9 true positives.'),
                ('What would change the posterior most: a better test or a higher prevalence?', 'Both help. With prevalence 1%, even a 1% false positive rate gives 9 / (9 + 9.9) about 48%. A higher prevalence helps directly.'),
                ('Why do we say naive?', 'It assumes the words are independent given the class. They are not, but the filter still works well.'),
                ('Why does add-one smoothing add 2 to the class size?', 'Each word has two outcomes, present and absent, and we add one pseudo-count to each.'),
                ('Why add logarithms in a real filter?', 'Thousands of small likelihoods multiplied underflow to zero. Logs turn the product into a sum.'),
                ('What does the second positive test assume?', 'That the two tests make independent errors. If the same cause makes both wrong, the posterior is lower.')],
        lab_steps=[('Stage 1: table', 'P(spam and free) 0.28, P(free) 0.34, P(spam | free) 0.8235, P(free | spam) 0.7.'), ('Stage 2: independence', 'Expected spam with free if independent 13.6 against 28 observed.'),
                   ('Stage 3: medical test', 'P(E) 0.108, posterior 0.0833, second test 0.45. Learners who forget the false positives get 1.0, and those who use 0.1 as P(E) get 0.09.'),
                   ('Stage 4: spam filter', 'Smoothed likelihoods 0.6905 and 0.0161. Email 1 posterior 0.9955, email 2 0.3304.'), ('Stage 5: break it', 'Without smoothing email 1 gives ham score 0 and posterior 1.0. Discuss overconfidence.')],
        rescue=['If the concepts overrun, skip the log slide and mention it in one sentence. It returns in Session 17.', 'If learners struggle with Bayes theorem, stay on the natural frequency tree and count people.',
                'If only 30 minutes remain for the lab, do stages 1, 3 and 4.', 'If the spreadsheet product is wrong, check that absent words use 1 minus the likelihood.'],
        after=['Share the lab files again for absent learners.', 'Collect questions about Bayes and open Session 16 with the most common one.', 'Remind the class that Session 16 turns prior, likelihood and posterior into training losses.'],
        lab_answer_key=[['Stage 1 PREDICT: is P(spam | free) larger or smaller than P(spam)?', 'Larger: 0.8235 against 0.40.'], ['Stage 3 READ: why is the posterior only 8.3% after a positive test?', 'Most positives are false alarms from the many healthy people.'],
                        ['Stage 4 READ: which word pushes email 2 towards ham?', 'meeting, and the missing prize.'], ['Stage 5 CHANGE: remove the smoothing.', 'The ham score for email 1 becomes 0 and the posterior becomes 1.0, which is overconfident.'],
                        ['Spreadsheet CHANGE: set prevalence to 10%.', 'The posterior rises to about 0.5 (0.09 / 0.18).']])
    return s
