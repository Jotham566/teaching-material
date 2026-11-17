"""Session 17: information theory (author F). Every number comes from the solution notebook (labs/s17_nb.py).
Session 17 recalls the softmax and its stable form from Session 12, and owns temperature, top-p, cross-entropy, log-softmax and the sigmoid form of prediction minus target (which Session 18 cites)."""
import importlib.util
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent


def _ns():
    spec = importlib.util.spec_from_file_location('s17_nb_deck', HERE / 'labs' / 's17_nb.py')
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.namespace()


def build():
    N = _ns()
    f = lambda a: [float(v) for v in a]
    P, QA, QB = f(N['P']), f(N['Q_A']), f(N['Q_B'])
    HP, HB = float(N['H_P']), float(N['H_biased'])
    ceA, ceB, klA, klB = float(N['ce_A']), float(N['ce_B']), float(N['kl_A']), float(N['kl_B'])
    z = f(N['z'])
    pr = f(N['probs'])
    gr = f(N['grad'])
    L0 = float(N['L0'])
    tp = f(N['token_probs'])
    words = list(N['words'])
    tot, mean, ppl = float(N['total_nll']), float(N['mean_nll']), float(N['perplexity'])
    ez = [math.exp(v) for v in z]
    esum = sum(ez)
    lse = math.log(esum)
    pT = np.array(N['p_T'])
    t05, t2 = [float(v) for v in pT[0]], [float(v) for v in pT[2]]
    e2 = [math.exp(v / 2) for v in z]
    w5, p5, pn = list(N['words5']), f(N['p5']), f(N['p_nucleus'])
    cum5 = np.cumsum(p5)
    # how each probability moves when the cat logit moves (the Jacobian column for z1), and a finite-difference check
    d11, d21 = pr[0] * (1 - pr[0]), -pr[1] * pr[0]
    zz = np.array(z)
    zz[0] += 0.001
    pz = np.exp(zz - zz.max())
    pz = pz / pz.sum()
    fd1, fd2 = float(pz[0] - pr[0]), float(pz[1] - pr[1])
    s_z = 0.5
    s_p = 1 / (1 + math.exp(-s_z))
    four = ['the', 'a', 'one', 'my']
    ce16 = 0.2990011586691898   # Session 16's binary cross-entropy, in nats

    s = dict(
        num=17, block='Probability and statistics', short_title='Information theory',
        title='Surprise, entropy and cross-entropy measure how well a model predicts what really happens',
        question='How does a language model turn raw scores into a probability for every next word, and how do we score it?',
        outcomes=['Compute surprise, entropy, cross-entropy and KL divergence by hand, and show that cross-entropy = entropy + KL',
                  'Reshape a softmax with temperature and top-p, and derive that the gradient of softmax with cross-entropy is prediction minus target (also for a sigmoid)',
                  'Compute the cross-entropy and perplexity of a toy language model on a six word sentence'],
        outcome_icons=['bars', 'calculator', 'chart'],
        outcome_note=('By the end of today you can do three things. First, compute surprise, entropy, cross-entropy and KL divergence by hand, and show that cross-entropy equals entropy plus KL. '
                      'Second, take the softmax of Session 12, reshape it with temperature and trim it with top-p, and derive with numbers that the gradient of softmax with cross-entropy is the prediction minus the target, for a sigmoid too. '
                      'Third, compute the cross-entropy and the perplexity of a toy language model on a six word sentence. The numbers are illustrative, and the arithmetic is the same as in real training.'),
        clock=[(10, 'Recall, then a real question from AI'), (35, 'Concept: a picture, then one example by hand'), (10, 'Break'), (45, 'Lab in Python or a spreadsheet: predict, run, change one thing'),
               (15, 'Where this appears in AI, and an exit check'), (5, 'Save the work')],
        plan_title='Your two hours: information, sampling settings, then perplexity',
        plan_caption='Ideas first. Then the lab, in Python or a spreadsheet. Then AI.',
        plan_note=('Today has the usual shape. Ten minutes of recall from Session 16 and the question of the day. Thirty-five minutes of concepts, each with a picture and a hand example. A ten minute break. '
                   'Then forty-five minutes of lab, where you compute entropy, cross-entropy, a temperature and top-p cut, a gradient and a perplexity yourself. We finish with where this appears in AI, an exit check and saving your work.'),
        recall_from='Session 16',
        recall=[('What does maximum likelihood estimation choose?', 'The parameter value that makes the observed data most probable, which means the largest likelihood.'),
                ('Why do we work with the log-likelihood?', 'A product of many small probabilities underflows to zero. A sum of logarithms is stable, and the maximum stays at the same parameter.'),
                ('Which assumption about the target gives cross-entropy as the loss?', 'A Bernoulli assumption for yes or no, or a categorical assumption for one of many classes. Gaussian noise gives squared error.')],
        words=[('Entropy', 'The average surprise of a distribution, in bits with log2 or nats with ln. How uncertain the outcome is.'),
               ('Cross-entropy', 'The average surprise when reality follows P but the model believes Q. The training loss for classification and language models.'),
               ('KL divergence', 'Kullback-Leibler divergence: cross-entropy minus entropy. The extra cost of believing Q instead of P.'),
               ('Temperature and top-p', 'Sampling settings. Temperature divides the logits before the softmax. Top-p keeps only the most likely words.'),
               ('Perplexity', 'e to the power of the mean negative log-probability. The effective number of equally likely choices the model has at each word.')],
        word_icons=['bars', 'calculator', 'flag', 'gear', 'question'],
        words_note=('Five words for today. Entropy is the average surprise of a distribution. Cross-entropy is the average surprise when reality follows one distribution and the model believes another. '
                    'KL divergence is the difference between the two, the extra cost of believing the wrong distribution. Temperature and top-p are the two sampling settings that reshape and trim the softmax of Session 12 before a word is drawn. '
                    'Perplexity is the standard score for language models, the effective number of equally likely words the model chooses between at each step.'),
        keep='Keep your notebook or workbook with all checks passing. Keep six numbers: entropy 1.75 bits, cross-entropy 2.000 bits, KL 0.250 bits, top class 0.864 at T = 0.5, gradient -0.758 and perplexity 5.21.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Cross-entropy = entropy + KL', value='2.000 = 1.750 + 0.250 bits'), dict(label='Gradient', value='p - y = (0.659, -0.758, 0.099)'),
                                                              dict(label='Toy perplexity', value='5.21'), dict(label='Next session', value='Course project: five builds')]),
        keep_title='Save your lab and keep six numbers',
        next='Session 18: the course project. Build linear regression, logistic regression, PCA, a small network and attention from first principles.', next_label='Next session',
        keep_note=('Before you go, run the notebook or the workbook from the top, check that every check passes and save it. Keep the six numbers on the slide. '
                   'Next session is the course project. You build linear regression, logistic regression, PCA, a small neural network and attention, and the notebook shows you OK or NOT YET for each build. There are no marks. '
                   'The sigmoid form of p minus y trains two of the builds, and the softmax you reshaped today sits inside attention. Bring one question.'),
        cover_note=('Welcome to Session 17. Last time we saw that training a model is maximum likelihood, and that the loss for classification is cross-entropy. Today we look at cross-entropy from the side of information. '
                    'We ask how surprising an outcome is, how uncertain a distribution is, and how far a model is from reality. We also see how temperature and top-p reshape a model\'s choices, and meet perplexity, the score you will see in every language model paper.'),
        slides=[])
    S = s['slides']

    S.append(dict(kind='table', title='Answers to the three questions from Session 16', headers=['Question', 'Short answer'], rows=[[q, a] for q, a in s['recall']], widths=[5.0, 7.0], icons=False,
                  note='Today the Bernoulli and categorical losses get a second meaning, measured in bits as well as nats.',
                  notes=('Maximum likelihood estimation chooses the parameter that makes the observed data most probable. We use the logarithm because a product of many small probabilities underflows, and a sum of logs does not. '
                         'A Bernoulli or categorical assumption gives cross-entropy, while Gaussian noise gives squared error. Today we ask what cross-entropy means in terms of information, and why the same loss can be quoted in bits or in nats.')))

    S.append(dict(kind='idea', title='Surprise: a rare event carries more information than a common one',
                  visual=dict(kind='f_bits_bars', items=[dict(label='A fair coin shows heads', p='p = 1/2', bits=1), dict(label='A random letter from A to H', p='p = 1/8', bits=3), dict(label='One of 1,024 equal tickets wins', p='p = 1/1024', bits=10, hl=True)]),
                  lead='The surprise (self-information) of an event with probability p is -log2(p) bits.',
                  points=['A bit is the answer to one yes or no question.', 'Every time the probability is cut in half, the surprise grows by one bit.'],
                  notes=('Start with surprise. If I tell you a fair coin showed heads, you learn little, because it was a coin flip. The bar is one bit. If I tell you a random letter from A to H was a particular one, that is one in eight, three bits. '
                         'If I tell you which of one thousand and twenty four tickets won, that is ten bits. A bit is the answer to one yes or no question, and you would need ten of them to find the winning ticket. '
                         'Rare events carry more information. What would the surprise be for an event that is certain?')))

    S.append(dict(kind='formula', title='Surprise is the negative logarithm of the probability',
                  formulas=[('Surprise in bits', r'$I(x)=-\log_2 p(x)$'), ('Surprise in nats', r'$I(x)=-\ln p(x)$')],
                  symbols=[['x', 'One outcome, such as one word.', 'a random letter from A to H'], ['p(x)', 'The probability of that outcome.', '1/8'], ['I(x)', 'The surprise (self-information) of that outcome.', '3 bits = 2.079 nats'],
                           ['nat', 'The unit when we use ln. One bit is 0.693 nats.', 'libraries use ln']],
                  size=26, note=f'Bits = nats / 0.693. Session 16\'s cross-entropy of {ce16:.3f} nats is {ce16 / math.log(2):.3f} bits.',
                  notes=('The surprise of an outcome x is minus the log of its probability. With log base two the unit is the bit. With the natural logarithm the unit is the nat. '
                         'For an eighth, minus log two of one eighth is three bits, and minus the natural log is 2.079 nats. The two differ by the constant factor 0.693, which is ln 2. '
                         f'Libraries use the natural log, so their losses are in nats. Session 16 gave a cross-entropy of {ce16:.3f} nats, which is {ce16 / math.log(2):.3f} bits. Today the hand examples are in bits and the softmax, the loss and the language model are in nats, and every number says which.')))

    S.append(dict(kind='idea', title='Entropy is the average surprise, and it is largest when every outcome is equally likely',
                  visual=dict(kind='f_panels_bars', ymax=0.95, panels=[dict(title='Fair coin', note='entropy 1 bit', values=[0.5, 0.5], labels=['heads', 'tails'], show=True, fmt='{:.2f}'),
                                                                      dict(title='Biased coin', note=f'entropy {HB:.3f} bits', values=[0.9, 0.1], labels=['heads', 'tails'], show=True, fmt='{:.2f}'),
                                                                      dict(title='Four next words', note=f'entropy {HP:.2f} bits', values=P, labels=four, show=True, fmt='{:.3f}')]),
                  lead='Entropy H(P) is the average surprise of outcomes drawn from the distribution P.',
                  points=['Among two-outcome distributions the fair coin is hardest to predict: 1 bit. The 0.9 coin has only ' + f'{HB:.3f} bits.',
                          f'With K equally likely outcomes the entropy is log2 K: 2 bits for 4 words. Our uneven four words have {HP:.2f} bits.'],
                  notes=('Entropy is the average surprise. On the left a fair coin, where each outcome has probability one half, so the average surprise is one bit. In the middle a coin that gives heads nine times in ten. '
                         f'Heads is not surprising and tails is very surprising but rare, so the average is only {HB:.3f} bits. Among all coins, the fair one is hardest to predict. '
                         f'On the right are four next words with entropy {HP:.2f} bits. Four outcomes can hold more uncertainty than two: four equally likely words would give two bits, the most possible for four outcomes. The more outcomes and the more even they are, the higher the entropy.')))

    S.append(dict(kind='table', title='By hand: the entropy of four next words is the sum of p times surprise, 1.75 bits',
                  headers=['Next word', 'p', 'Surprise (bits)', 'p × surprise'], rows=[[w, f'{p:g}', f'{-math.log2(p):g}', f'{-p * math.log2(p):g}'] for w, p in zip(four, P)] + [['Total', '1', '', f'{HP:g}']],
                  widths=[3.0, 2.0, 3.0, 3.0], icons=False, note='Illustrative (made-up) probabilities. The total of the last column is the entropy.',
                  notes=('Work it by hand. The first word has probability one half, surprise one bit, and contributes a half. The second has a quarter, two bits, and contributes another half. '
                         'The last two each have an eighth, three bits, and contribute three eighths each. Add the last column: 0.5, plus 0.5, plus 0.375, plus 0.375 gives 1.75 bits. '
                         'These probabilities are made up to give clean arithmetic. If all four words had probability one quarter, each term would be a half and the entropy two bits.')))

    S.append(dict(kind='formula', title='Entropy is the probability-weighted average of the surprise',
                  formulas=[('Entropy', r'$H(P)=-\sum_{i}p_i\log_2 p_i$'), ('Our four words', r'$H(P)=0.5+0.5+0.375+0.375=1.75$ bits')],
                  symbols=[['P', 'A distribution: probabilities that add to 1.', 'the four next words'], ['p_i', 'The probability of outcome i.', '0.5, 0.25, 0.125, 0.125'], ['sum over i', 'Add the terms for every outcome.', 'four terms'],
                           ['H(P)', 'The entropy, in bits when the log is base 2.', '1.75 bits']],
                  size=26, note='Four equally likely words would have the largest entropy: 2 bits.',
                  notes=('The formula is the table you just filled. Entropy of P is minus the sum over outcomes of p times log two of p. Each term is the probability times its surprise, so entropy is the expectation of the surprise, in the sense of Session 13. '
                         'For our four words the terms are 0.5, 0.5, 0.375 and 0.375, which add to 1.75 bits. Entropy depends only on the distribution P. No model is involved, so it is a property of the data. Read the symbol table and say what each symbol means for our four words.')))

    S.append(dict(kind='idea', title='Cross-entropy is the average surprise when reality follows P but the model believes Q',
                  visual=dict(kind='f_panels_bars', ymax=0.6, labels=four, panels=[dict(title='Reality P', note='what really happens', values=P, show=True, fmt='{:.3f}'),
                                                                                  dict(title='Model A', note='uniform: every word 0.25', values=QA, show=True, fmt='{:.3f}'), dict(title='Model B', note='closer to reality', values=QB, show=True, fmt='{:.3f}')]),
                  lead='Cross-entropy H(P, Q) averages the model\'s surprise over what really happens.',
                  points=[f'Model A: H(P, Q) = {ceA:.3f} bits.', f'Model B: H(P, Q) = {ceB:.3f} bits. Smaller, because Q is closer to P.'],
                  notes=('Suppose reality is the distribution on the left, but the model believes one of the other two. Model A spreads probability equally. Model B is closer to reality. '
                         'Cross-entropy asks how surprised the model is, on average, by what really happens. Each outcome occurs with its true probability, but the model measures the surprise with its own probability. '
                         f'Model A scores {ceA:.3f} bits and Model B scores {ceB:.3f}. The model that is closer to reality is less surprised, and this number is what training minimises.')))

    S.append(dict(kind='formula', title='Cross-entropy weights the model\'s surprise by the true probabilities',
                  formulas=[('Cross-entropy', r'$H(P,Q)=-\sum_{i}p_i\log_2 q_i$'), ('Model A', r'$H(P,Q_A)=(0.5+0.25+0.125+0.125)\times 2=2.000$')],
                  symbols=[['p_i', 'The true probability of outcome i.', '0.5, 0.25, 0.125, 0.125'], ['q_i', 'The probability the model gives to outcome i.', 'A: 0.25 each'], ['log2 q_i', 'The model\'s surprise at outcome i is minus this.', 'A: 2 bits for each'],
                           ['H(P, Q)', 'The cross-entropy, in bits.', f'A: 2.000, B: {ceB:.3f}']],
                  size=24, note='With a real label, p is 1 on the true class and 0 elsewhere, so the loss is -log q of the true class.',
                  notes=('Cross-entropy is minus the sum of the true probability times the log of the model probability. For model A every q is a quarter, so every surprise is two bits, and the average is exactly two. '
                         f'For model B the number is {ceB:.3f}. The link to Session 16 comes when we train on a real example. The true distribution puts probability one on the correct class and zero on the rest. '
                         'Then the sum has one term, and the loss is minus the log of the probability the model gave to the correct class, the cross-entropy loss you met last time.')))

    S.append(dict(kind='wide', title='Cross-entropy is entropy plus KL divergence: the entropy is fixed, the KL is what the model can improve',
                  visual=dict(kind='f_ce_kl', entropy=HP, rows=[dict(label='Reality alone', ce=HP), dict(label='Model B', ce=ceB), dict(label='Model A (uniform)', ce=ceA)]),
                  caption=f'Model A: {HP:.3f} + {klA:.3f} = {ceA:.3f}. Model B: {HP:.3f} + {klB:.3f} = {ceB:.3f}. All in bits.',
                  notes=('Every bar starts with the entropy of reality, 1.75 bits, in pale grey. No model can go below it, because that is the uncertainty in the data itself. '
                         f'On top of that the model pays a penalty in red, the KL divergence. Model A pays {klA:.3f} bits and Model B only {klB:.3f}. So cross-entropy equals entropy plus KL. '
                         'During training the entropy of the data does not change, so lowering the cross-entropy is the same as lowering the KL divergence, pulling the model closer to reality. Why can the red part never be negative?')))

    S.append(dict(kind='formula', title='KL divergence is never negative and is zero only when the model equals reality',
                  formulas=[('KL divergence', r'$D_{KL}(P\,\|\,Q)=\sum_{i}p_i\log_2\frac{p_i}{q_i}$'), ('The link', r'$H(P,Q)=H(P)+D_{KL}(P\,\|\,Q)$')],
                  symbols=[['D_KL(P || Q)', 'The extra cost of believing Q when reality is P.', f'A: {klA:.3f}, B: {klB:.3f} bits'], ['Never negative', 'It is 0 only when Q = P everywhere.', 'a perfect model'],
                           ['Not symmetric', 'D(P || Q) is usually not D(Q || P).', 'so it is not a distance'], ['H(P)', 'The entropy of reality.', f'{HP:.2f} bits']],
                  size=22, note='Minimising cross-entropy over the model is the same as minimising KL, because H(P) is fixed.',
                  notes=('KL divergence is the sum of p times the log of p over q. It measures the extra cost of using the wrong distribution. Three facts. It is never negative. It is zero only when the model equals reality. '
                         'It is not symmetric, so swapping P and Q gives a different number, which is why we do not call it a distance. The second line is the link from the picture. '
                         'Because the entropy is fixed by the data, minimising the cross-entropy over the model minimises the KL. During training you print the cross-entropy, since the entropy of real text is unknown.')))

    S.append(dict(kind='wide', title='Recall from Session 12: the softmax turns logits into probabilities, and the stable form subtracts the largest logit',
                  visual=dict(kind='f_panels_bars', labels=['cat', 'dog', 'fox'], panels=[dict(title='Logits z', note='raw scores, any size', values=z, show=True, fmt='{:.1f}'),
                                                                                         dict(title='exp(z)', note='make them positive', values=ez, show=True, fmt='{:.3f}'),
                                                                                         dict(title='Softmax p', note=f'divide by the sum, {esum:.3f}', values=pr, show=True, hl=0, fmt='{:.3f}')]),
                  caption='Illustrative logits. Stable form (Session 12): subtract the largest logit first. Same p.',
                  notes=(f'You met the softmax in Session 12, so this is a recall. A model produces one raw score per class, called a logit: 2.0 for cat, 1.0 for dog and 0.1 for fox. The softmax takes the exponential of each, {ez[0]:.3f}, {ez[1]:.3f} and {ez[2]:.3f}, and divides by their sum, {esum:.3f}. '
                         f'The probabilities are {pr[0]:.3f}, {pr[1]:.3f} and {pr[2]:.3f}. Session 12 also gave the stable form: subtract the largest logit before the exponential, so that logits like a thousand cannot overflow. The answer does not change. Today adds three things to it: temperature, top-p and its gradient.')))

    S.append(dict(kind='wide', title='Temperature divides the logits before the softmax: a low T sharpens, a high T flattens',
                  visual=dict(kind='f_panels_bars', labels=['cat', 'dog', 'fox'], panels=[dict(title='T = 0.5', note='sharper', values=t05, show=True, hl=0), dict(title='T = 1', note='the plain softmax', values=pr, show=True, hl=0),
                                                                                          dict(title='T = 2', note='flatter', values=t2, show=True, hl=0)]),
                  caption='Each panel adds to 1. T near 0: the top class takes all (greedy). Large T: equal shares.',
                  notes=('In Session 14 you drew a next word by cutting the line from 0 to 1 into slices, one per word, sized by its probability. Temperature changes the slices before the draw. Divide every logit by T, then take the softmax. '
                         f'With T equal to 0.5 the logits double, and cat grows from {pr[0]:.3f} to {t05[0]:.3f}. With T equal to 2 they halve, and cat falls to {t2[0]:.3f} while fox rises. '
                         'So a low temperature makes the model more predictable and a high temperature spreads the choice. As T goes towards zero the top class takes everything, which is called greedy decoding.')))

    S.append(dict(kind='formula', title='Softmax with temperature: one division, then the same softmax',
                  formulas=[('Softmax with temperature', r'$p_i=\frac{e^{z_i/T}}{\sum_{j}e^{z_j/T}}$'), ('Cat at T = 2', r'$\frac{e^{1}}{e^{1}+e^{0.5}+e^{0.05}}=\frac{%.3f}{%.3f}=%.3f$' % (e2[0], sum(e2), t2[0]))],
                  symbols=[['z_i', 'The logit (score) of class i.', f'{z[0]:g}, {z[1]:g}, {z[2]:g}'], ['T', 'The temperature, above 0. T = 1 is the plain softmax.', 'T = 2 halves every logit'],
                           ['p_i', 'The probability of class i at temperature T.', f'cat at T = 2: {t2[0]:.3f}'], ['Sum over j', 'All classes, the same T in every term.', '3 terms']],
                  size=20, note='Use the stable form of Session 12 here too: subtract the largest z_j / T first.',
                  notes=(f'Divide each logit by the temperature T, take e to that power, and divide by the sum over all classes. Work the cat at T equal to two. The logits become 1, 0.5 and 0.05. e to the 1 is {e2[0]:.3f}, and the three terms add up to {sum(e2):.3f}. '
                         f'So cat gets {e2[0]:.3f} over {sum(e2):.3f}, which is {t2[0]:.3f}. The sum must use the same T in every term, otherwise the probabilities will not add to one. With T equal to one you are back at the plain softmax.')))

    S.append(dict(kind='idea', title='Top-p (nucleus) sampling keeps the smallest set of likely words, then rescales them',
                  visual=dict(kind='f_topp', words=w5, probs=p5, top_p=0.8),
                  lead='Top-p = 0.8: keep the most likely words until their running total reaches 0.8, then rescale them.',
                  points=[f'Tea, coffee and water reach {cum5[2]:.3f}. Milk and soup are cut. The draw of Session 14 then uses only the kept slices.', f'Divide by {cum5[2]:.3f}: tea {pn[0]:.3f}, coffee {pn[1]:.3f}, water {pn[2]:.3f}.'],
                  notes=('Top-p sampling, also called nucleus sampling, was published by Holtzman and colleagues in 2020. It removes the thin slices of Session 14 before the draw. These five drinks have illustrative logits, already sorted. '
                         f'With p equal to 0.8, tea gives {cum5[0]:.3f}, coffee brings the running total to {cum5[1]:.3f}, and water brings it to {cum5[2]:.3f}, past 0.8, so we stop. Milk and soup are cut. '
                         f'The kept probabilities are divided by {cum5[2]:.3f} so they add to one again: tea {pn[0]:.3f}, coffee {pn[1]:.3f}, water {pn[2]:.3f}. The next word is drawn at random from those three only.')))

    S.append(dict(kind='formula', title='Cross-entropy straight from the logits: log-softmax is log-sum-exp minus the true logit',
                  formulas=[('Log-softmax', r'$\ln p_k=z_k-\ln\sum_{j}e^{z_j}$'), ('Loss, dog true', r'$L=-\ln p_{dog}=\ln(%.3f)-1.0=%.3f-1.0=%.3f$ nats' % (esum, lse, L0))],
                  symbols=[['z_k', 'The logit of class k.', 'dog: 1.0'], ['ln sum of e^z', 'The log-sum-exp of Session 12.', f'ln {esum:.3f} = {lse:.3f}'],
                           ['L', 'The cross-entropy loss for one example, in nats.', f'{L0:.3f}'], ['In bits', 'Divide by ln 2 = 0.693.', f'{L0 / math.log(2):.3f} bits']],
                  size=24, note='Session 12 promised this link: libraries compute the loss this way, so no tiny probability is ever formed and logged.',
                  notes=('Training does not compute the probability and then its log. It goes straight from the logits. Take the log of the softmax: the log of e to the z k over the sum is z k minus the log of the sum. That log of a sum of exponentials is the log-sum-exp of Session 12. '
                         f'For our logits the sum is {esum:.3f} and its log is {lse:.3f}. Dog is the true word with logit one, so the loss is {lse:.3f} minus one, {L0:.3f} nats. In bits that would be {L0 / math.log(2):.3f}. '
                         'Libraries use this form, with the largest logit subtracted, so a tiny probability is never formed and then logged.')))

    S.append(dict(kind='wide', title='Softmax with cross-entropy has a simple gradient with respect to the logits: prediction minus target',
                  visual=dict(kind='f_panels_bars', labels=['cat', 'dog', 'fox'], panels=[dict(title='Prediction p', note='from the softmax', values=pr, show=True),
                                                                                         dict(title='Target y', note='dog is the true word', values=[0, 1, 0], show=True, fmt='{:.0f}'),
                                                                                         dict(title='Gradient p - y', note='the update signal', values=gr, show=True, hl=1)]),
                  caption='Illustrative. Dog, the true word, has a negative gradient: its logit should go up.',
                  notes=(f'Training needs the gradient of the loss with respect to the logits, and for softmax with cross-entropy it is the prediction minus the target. '
                         f'Dog is the true word, but the model gave it only {pr[1]:.3f}. The gradient for dog is {gr[1]:.3f}, negative, which tells the optimiser to raise that logit. '
                         f'The other two entries are positive, {gr[0]:.3f} for cat and {gr[2]:.3f} for fox, so those logits should go down, in proportion to how much probability they took. The three entries add up to zero. The next two slides derive it.')))

    S.append(dict(kind='formula', title='Derivation: the gradient of softmax with cross-entropy is p minus y',
                  formulas=[('Slopes', r'$\frac{\partial L}{\partial p_k}=-\frac{y_k}{p_k},\qquad\frac{\partial p_k}{\partial z_j}=p_k(\delta_{kj}-p_j)$'), ('Chain rule', r'$\frac{\partial L}{\partial z_j}=-\sum_k\frac{y_k}{p_k}\,p_k(\delta_{kj}-p_j)=-\sum_k y_k(\delta_{kj}-p_j)=p_j-y_j$')],
                  symbols=[['L', 'The loss: L = -sum of y_k ln p_k.', f'{L0:.3f} nats in our example'], ['delta_kj', '1 when k = j, else 0. Not the error signal of backpropagation.', 'picks one term'], ['y_k', 'The one-hot target: 1 for the true class.', 'y = (0, 1, 0)'],
                           ['p_j - y_j', 'The gradient for logit j.', f'({gr[0]:.3f}, {gr[1]:.3f}, {gr[2]:.3f})']],
                  size=20, note='The 1 / p_k cancels p_k. The delta part gives y_j. The other part gives p_j, because the y_k add to 1.',
                  notes=('The loss is minus the sum of y k times the log of p k. First we need how each probability moves when a logit moves: p k times delta k j minus p j. Delta k j is one when k equals j and zero otherwise. It shares a letter with the error signal of Session 11, but here it is only a switch. '
                         'The slope of the loss with respect to p k is minus y k over p k. The chain rule with a sum over paths, from Session 9, multiplies and adds them. The p k cancels. '
                         'Split the sum. The delta part gives y j. The other part gives p j times the sum of the y k, and the y k add up to one. The result is p j minus y j.')))

    S.append(dict(kind='example', title='By hand: how cat and dog move when the cat logit rises by 0.001',
                  scenario=f'The middle slope of the derivation, p_k(delta_kj - p_j), with numbers. Softmax p = ({pr[0]:.3f}, {pr[1]:.3f}, {pr[2]:.3f}). Move only the cat logit, z1.',
                  blocks=[dict(label='Same class', text=f'dp1/dz1 = p1(1 - p1) = {pr[0]:.3f} × {1 - pr[0]:.3f} = {d11:.3f}. The quotient rule of Session 7 gives this.'),
                          dict(label='Other class', text=f'dp2/dz1 = -p2 p1 = -{pr[1]:.3f} × {pr[0]:.3f} = {d21:.3f}'),
                          dict(label='Check', text=f'Recompute the softmax with z1 = 2.001: p1 rises by {fd1:.6f} and p2 falls by {-fd2:.6f}. Divide by 0.001: {fd1 / 0.001:.3f} and {fd2 / 0.001:.3f}.', red=True)],
                  notes=(f'The step that makes or breaks the derivation is how each probability moves when one logit moves. Nudge the cat logit. Cat\'s own probability moves at the rate p one times one minus p one, {pr[0]:.3f} times {1 - pr[0]:.3f}, which is {d11:.3f}. You can get that from the quotient rule of Session 7. '
                         f'Dog\'s probability moves the other way, at minus p two times p one, {d21:.3f}, because the probabilities must still add to one. '
                         f'Now check it. Recompute the softmax with the cat logit at 2.001. Cat rises by {fd1:.6f} and dog falls by {-fd2:.6f}. Divided by one thousandth those match the formula.')))

    S.append(dict(kind='example', title=f'By hand: logits 2.0, 1.0, 0.1 with dog true give a loss of {L0:.3f} nats',
                  scenario='Illustrative three-class example. The numbers match the lab.',
                  blocks=[dict(label='Softmax, target', text=f'p = ({pr[0]:.3f}, {pr[1]:.3f}, {pr[2]:.3f}) for cat, dog, fox and y = (0, 1, 0)'), dict(label='Loss', text=f'L = -ln {pr[1]:.3f} = {L0:.3f} nats'),
                          dict(label='Gradient', text=f'p - y = ({gr[0]:.3f}, {gr[1]:.3f}, {gr[2]:.3f}). The three entries add to 0.'),
                          dict(label='Check', text='Add 0.001 to the cat logit: the loss rises by about 0.659 × 0.001 = 0.00066.', red=True)],
                  notes=(f'Put numbers in. The softmax gives {pr[0]:.3f}, {pr[1]:.3f} and {pr[2]:.3f}. The target is dog. The loss is minus the natural log of {pr[1]:.3f}, which is {L0:.3f} nats. '
                         f'The gradient is the prediction minus the target: {gr[0]:.3f}, {gr[1]:.3f} and {gr[2]:.3f}. They add up to zero. '
                         'A check you can do on any derivation: nudge the cat logit up by one thousandth, and the loss should rise by about the first gradient entry times one thousandth, which is 0.00066. In the lab you do this for every logit and compare.')))

    S.append(dict(kind='formula', title='With two classes the softmax is a sigmoid, so sigmoid with binary cross-entropy also gives p minus y',
                  formulas=[('Two classes', r'$\frac{e^{z_1}}{e^{z_1}+e^{z_2}}=\frac{1}{1+e^{-(z_1-z_2)}}=\sigma(z_1-z_2)$'),
                            ('Gradient for one logit z', r'$p=\sigma(z),\ \ \frac{\partial L}{\partial z}=\left(-\frac{y}{p}+\frac{1-y}{1-p}\right)p(1-p)=p-y$')],
                  symbols=[['sigma', 'The sigmoid (Session 11). Slope p(1 - p).', f'sigma(0.5) = {s_p:.3f}'], ['z', 'One logit: the score for class 1.', 'z = 0.5'],
                           ['L', 'Binary cross-entropy (Session 16).', 'y = 1: L = -ln p'], ['p - y', 'The gradient for z.', f'{s_p:.3f} - 1 = {s_p - 1:.3f}']],
                  size=20, note='Session 18 uses this form in logistic regression and in the output of its small network.',
                  notes=('Divide the top and the bottom of a two-class softmax by e to the z one, and you get one over one plus e to the minus z one minus z two, which is the sigmoid of Session 11. So a sigmoid is a two-class softmax. '
                         'Directly: the slope of binary cross-entropy with respect to p is minus y over p plus one minus y over one minus p. Multiply by the sigmoid slope, p times one minus p. The terms cancel to p minus y. '
                         f'With z equal to 0.5 and y equal to one, p is {s_p:.3f} and the gradient is {s_p - 1:.3f}. Session 18 relies on this form.')))

    S.append(dict(kind='wide', title='Perplexity: e raised to the power of the mean negative log-probability of the real words',
                  visual=dict(kind='f_tokens', tokens=words, probs=tp, base='e', total_label='Illustrative (made-up numbers): the probability a toy model gave to each real word of the sentence.'),
                  caption=f'Mean -ln p = {tot:.2f} / 6 = {mean:.3f} nats. Perplexity = e^{mean:.3f} = {ppl:.2f}.',
                  notes=(f'A toy language model scores a six word sentence. For each real word, the model had given it a probability, 0.2, 0.1, 0.25, 0.5, 0.4 and 0.05. These are made up to show the arithmetic. '
                         f'The red row is minus the natural log of each, and the total is {tot:.2f} nats. That is the negative log-likelihood of the sentence. Divide by six and the mean is {mean:.3f}, the cross-entropy per word in nats. '
                         f'Perplexity is e to that power, {ppl:.2f}. The weakest words are cat and mat, which got only 0.1 and 0.05, so they add the most to the total.')))

    S.append(dict(kind='formula', title='Perplexity is the exponential of the cross-entropy per token',
                  formulas=[('Perplexity', r'$\mathrm{PPL}=\exp\left(-\frac{1}{N}\sum_{i=1}^{N}\ln p(w_i\mid w_1,\ldots,w_{i-1})\right)$'), ('Our sentence', r'$\mathrm{PPL}=e^{%.3f}=%.2f$' % (mean, ppl))],
                  symbols=[['N', 'The number of words (tokens) scored.', '6'], ['p(w_i | w_1 ... w_(i-1))', 'The probability the model gave to the real word i, given the words before it.', '0.2, 0.1, 0.25, 0.5, 0.4, 0.05'],
                           ['Mean of -ln p', 'The cross-entropy per word, in nats.', f'{mean:.3f}'], ['PPL', 'Perplexity. In bits it is 2 to the power of the bits per word. Same value.', f'{ppl:.2f}']],
                  size=22, note='Lower is better. Perplexity 1 means the model gave probability 1 to every real word.',
                  notes=(f'Perplexity is the exponential of the average negative log-probability of the real words, where each probability is conditional on the words before it, as in Session 15. For our sentence the average is {mean:.3f} nats and the perplexity is {ppl:.2f}. '
                         'If you work in bits you take two to the power of the bits per word, and you get the same number, because the unit and the base match. '
                         'A perplexity of one means the model gave probability one to every real word. Higher is worse. Read the symbol table and say what N is for our sentence.')))

    S.append(dict(kind='idea', title='Perplexity reads as the effective number of equally likely words the model chooses between',
                  visual=dict(kind='bars', items=[dict(label='A perfect model', value=1), dict(label='Our toy model', value=round(ppl, 2), hl=True), dict(label='Guessing among 50 words', value=50)], unit=''),
                  lead='A perplexity of 5.21 means the model is as unsure as if it picked among about five equally likely words.',
                  points=['Illustrative numbers.', 'Compare perplexities only for the same test text and the same tokens.'],
                  notes=(f'Perplexity is the effective number of equally likely choices the model has at each step. A perfect model has perplexity one. A model that guesses uniformly among fifty words has perplexity fifty. '
                         f'Our toy model has {ppl:.2f}, about five equally likely words per step. One caution. Perplexity depends on how the text is cut into tokens, so only compare models on the same test text and the same tokens. '
                         'Whether five is good depends entirely on the text and the tokens.')))

    S.append(dict(kind='compare', title='Three common mistakes about information measures',
                  left=dict(head='The mistake', points=['Cross-entropy and KL divergence are the same thing.', 'Bits and nats give different perplexities.', 'A higher temperature makes the model smarter.']),
                  right=dict(head='The fix', points=['They differ by the entropy of the data.', 'Same value if the exponent matches the log base.', 'It only flattens the probabilities.']),
                  verdict='Always say which log base, which text and which sampling settings.',
                  notes=('Three mistakes. First, cross-entropy and KL are not the same. They differ by the entropy of the data, which training cannot change, so they have the same minimiser but different values. '
                         'Second, bits and nats do not change the perplexity, as long as you exponentiate with the matching base. Two to the bits equals e to the nats. '
                         'Third, a higher temperature does not make a model cleverer. It only flattens the probabilities, so rarer words are drawn more often, which can read as varied or as wrong. Which of the three would you have made?')))

    S.append(dict(kind='code', title='Read the recipe before you write it: entropy, KL, temperature, top-p, gradient, perplexity',
                  code='H = -np.sum(P * np.log2(P))\nkl = np.sum(P * np.log2(P / Q))\np = softmax(z / T)\nkeep = np.searchsorted(np.cumsum(p5), 0.8) + 1\ngrad = p - y\nppl = np.exp(np.mean(-np.log(token_probs)))',
                  reads=['Line 1: entropy in bits.', 'Line 2: KL divergence. Cross-entropy = H + kl.', 'Line 3: softmax with temperature T.', 'Line 4: how many words top-p keeps.',
                         'Line 5: the gradient for the logits.', 'Line 6: perplexity.', 'Spreadsheet: LOG(q, 2), SUMPRODUCT, a growing SUM, EXP.'],
                  notes=('Read the recipe before the lab. Entropy is minus the sum of P times log two of P. KL divergence is the sum of P times log two of P over Q, and cross-entropy is entropy plus that. '
                         'The softmax with temperature divides the logits by T and then uses the stable softmax. For top-p, cumsum gives the running total of the sorted probabilities, and searchsorted finds where it first reaches 0.8. '
                         'The gradient is the prediction minus the target, and perplexity is the exponential of the mean negative log-probability. In a spreadsheet a running total is a SUM whose range grows by one row each time.')))

    S.append(dict(kind='divider', title='Part 2: the lab', lead='Close the slides. Open the notebook or the workbook.', section='Lab',
                  notes=('That is the end of the concepts. Everything you need is on the slides you have seen. Open the notebook or the workbook now. '
                         'In Python, run the cells from the top in order. In the spreadsheet, start on the sheet called Start here. Raise your hand if something does not run. '
                         'Keep the rhythm: predict first, run, read, then change one thing.')))

    S.append(dict(kind='steps', title='The lab has seven steps, from surprise to perplexity',
                  steps=[dict(head='1 Surprise', text='Bits for three events', icon='flag'), dict(head='2 Entropy', text='Fair, biased and four words', icon='bars'), dict(head='3 CE and KL', text='Two models against reality', icon='calculator'),
                         dict(head='4 Softmax', text='The stable form', icon='gear'), dict(head='5 Sampling', text='T and top-p', icon='speech'), dict(head='6 Gradient', text='p - y against a numeric check', icon='check'), dict(head='7 Perplexity', text='A six word sentence', icon='chart')],
                  caption='Python: Steps 1 to 7. Spreadsheet: sheets Entropy (Steps 1 to 3), Softmax (4 and 6), Sampling (5) and Perplexity (7). Predict, run, change one thing.',
                  notes=('The lab has seven steps. In the first you compute the surprise of three events in bits. In the second the entropy of a fair coin, a biased coin and four words. '
                         'In the third the cross-entropy and the KL divergence of two models, and you confirm that cross-entropy equals entropy plus KL. In the fourth you rebuild the stable softmax of Session 12. In the fifth you apply a temperature and a top-p cut. '
                         'In the sixth you check the gradient p minus y against a numeric gradient. In the seventh you compute a perplexity. The spreadsheet has the same numbers on four sheets. Do not skip the predict cells.')))

    S.append(dict(kind='table', title='Check your numbers against these before you move on',
                  headers=['What you compute', 'You should see'],
                  rows=[['Surprise of 1/2, 1/8, 1/1024 (bits)', '1, 3, 10'], ['Entropy of P, fair coin, 0.9 coin', f'{HP:g}, 1, {HB:.3f} bits'], ['Cross-entropy and KL of model A and model B', f'{ceA:.3f}, {ceB:.4f}; {klA:.3f}, {klB:.4f} bits'],
                        ['Softmax of 2.0, 1.0, 0.1 (cat, dog, fox)', f'{pr[0]:.4f}, {pr[1]:.4f}, {pr[2]:.4f}'], ['Cat at T = 0.5 and 2; top-p keeps; tea rescaled', f'{t05[0]:.4f}, {t2[0]:.4f}; 3 drinks; {pn[0]:.4f}'],
                        ['Loss and gradient p - y (dog true)', f'{L0:.4f} nats; {gr[0]:.4f}, {gr[1]:.4f}, {gr[2]:.4f}'],
                        ['Sum of -ln p, mean, perplexity', f'{tot:.3f}, {mean:.4f} nats, {ppl:.3f}']],
                  widths=[6.4, 5.2], icons=['flag', 'bars', 'calculator', 'chart', 'gear', 'check', 'clock'],
                  note='If your number differs, stop and ask. Find the step that went wrong. Do not change a number to match.',
                  notes=('Use this table as your checkpoint. The surprises are one, three and ten bits. The entropy of the four words is 1.75. Model A has cross-entropy exactly two and model B has 1.8007, with KL divergences 0.25 and 0.0507. '
                         f'The softmax of 2, 1 and 0.1 is 0.659, 0.242 and 0.099. Cat gets {t05[0]:.3f} at temperature 0.5 and {t2[0]:.3f} at temperature 2. Top-p keeps three drinks and tea becomes {pn[0]:.3f}. The loss is 1.417 nats and the sentence has a perplexity of 5.21. '
                         'If a number is different, stop and call me over. Do not edit a number to make it match.')))

    S.append(dict(kind='table', title='Errors you will meet, what they mean and what to do',
                  headers=['What you see', 'What it means', 'What to do'],
                  rows=[['nan from the softmax', 'The exponential overflowed', 'Subtract the largest logit first'], ['NOT YET: write your code in the cell above', 'An answer cell (marked gold) still says None', 'Replace None with your code and run both cells again'],
                        ['A negative KL divergence', 'P and Q are swapped, or they do not add to 1', 'Check both add to 1 and keep the order P then Q'], ['Spreadsheet shows #DIV/0! or #NUM!', 'A probability of 0 inside a logarithm', 'Use only probabilities above 0']],
                  widths=[3.6, 4.2, 4.2], icons=['bell', 'key', 'cross', 'flag'],
                  notes=('Four errors you may meet. A nan from the softmax means the exponential overflowed, so subtract the largest logit first. A message saying not yet, write your code, means a gold cell still holds the placeholder. '
                         'A negative KL divergence is impossible, so check that P and Q both add to one and that you kept P first. In the spreadsheet, a divide by zero or a number error means a probability of zero is inside a logarithm. '
                         'Read the last line of any error first. It usually tells you what to do.')))

    S.append(dict(kind='idea', title='Where this appears in AI: pre-training by minimising cross-entropy on the next token',
                  visual=dict(kind='flow', steps=[dict(head='Text in', text='Tokens, then embeddings', icon='doc'), dict(head='Logits', text='One score per word in the vocabulary', icon='bars'), dict(head='Softmax', text='Scores become probabilities', icon='gear'),
                                                  dict(head='Loss', text='Cross-entropy against the real next word', icon='check')], highlight=3),
                  lead='Published research: transformer language models are pre-trained by minimising next-token cross-entropy.',
                  points=['The p - y gradient from today is the signal that starts backpropagation.', 'Later stages, such as learning from human feedback, use other objectives. Closed products do not publish their internals.'],
                  notes=('Published research describes how transformer language models are pre-trained. Text becomes tokens. The network produces one score, a logit, for every word in its vocabulary. A softmax turns the scores into probabilities. '
                         'During training, the cross-entropy against the real next word is the loss, computed from the logits with log-softmax, and its gradient with respect to the logits is the prediction minus the target, as you derived. That signal then flows backwards through the network. '
                         'The exact designs of ChatGPT, Gemini and Claude are not published, so I describe the published framework and make no claim about their internals.')))

    S.append(dict(kind='idea', title='Where this appears in AI: temperature and top-p are settings in public APIs',
                  visual=dict(kind='card', title='Sampling settings in public APIs (names only)', fields=[dict(label='temperature', value='Documented by OpenAI, Gemini, Anthropic'),
                                                                                                      dict(label='top_p (nucleus)', value='Documented by the same three APIs'), dict(label='top_k', value='Documented by some providers')]),
                  lead='The next word is drawn at random, so answers can differ. Temperature and top-p set how much.',
                  points=['Low temperature: steadier answers. High: more varied.', 'Nucleus sampling: Holtzman and colleagues, 2020.', 'Products may add steps we cannot see.'],
                  notes=('The public APIs of OpenAI, Google Gemini and Anthropic all document a temperature setting and a top-p setting, and some providers document top-k as well. In the standard definition, temperature divides the logits before the softmax, as you computed. '
                         'The next word is then drawn at random, so at any temperature above zero the same question can give different answers. Temperature and top-p set how much they can differ. '
                         'I am describing the published mathematics. What a product does beyond these settings is not public, so I make no claim about it. Perplexity is also a standard way that published papers report how well a model predicts held-out text.')))

    S.append(dict(kind='practice', title="Check an AI assistant's answer against your own numbers", minutes=5, label='Optional, with any assistant',
                  task='Ask an assistant for the softmax of the logits 2.0, 1.0, 0.1, the same at temperature 0.5, and the cross-entropy loss if the second class is true.',
                  steps=[f'Compare: {pr[0]:.3f}, {pr[1]:.3f}, {pr[2]:.3f}; {t05[0]:.3f} at T = 0.5; loss {L0:.3f} nats.', 'Ask which log base it used (bits: 2.04).', 'Never paste confidential data into an assistant.'],
                  output='A note: where it agreed with you, and where not.',
                  notes=('Try this with any assistant. Ask it for the softmax of the logits two, one and nought point one, the same at temperature 0.5, and the cross-entropy loss when dog is the true word. '
                         f'Compare with your numbers: {pr[0]:.3f}, {pr[1]:.3f} and {pr[2]:.3f}, then {t05[0]:.3f} for cat at the lower temperature, and a loss of {L0:.3f} nats. Ask which logarithm base it used. With base two the loss would be 2.04 bits. '
                         'An assistant can slip on arithmetic or on the unit, and now you can check. Please do not paste confidential data into any assistant.')))

    S.append(dict(kind='idea', title='Next session: attention puts today\'s softmax on top of dot products',
                  visual=dict(kind='flow', steps=[dict(head='Dot products', text='How well two tokens match (Session 2)', icon='calculator'), dict(head='Scale', text='Divide by the spread (Sessions 13, 14)', icon='bars'),
                                                  dict(head='Softmax', text='Scores become weights (Session 12, today)', icon='gear'), dict(head='Weighted average', text='Mix the tokens (Session 3)', icon='chart')], highlight=2),
                  lead='Session 18 teaches attention, the core of a transformer, from parts you have.',
                  points=['Each token scores every other token, turns the scores into weights with a softmax, and takes a weighted average.', 'The new part is how the pieces fit together. You build it by hand.'],
                  notes=('A preview of next time. Attention is the core step of a transformer, and Session 18 teaches it as a new idea. Every piece is already yours. A dot product from Session 2 says how well two tokens match. '
                         'Dividing by the spread of those scores, as in Sessions 13 and 14, keeps them a sensible size. The softmax of Session 12 and today turns the scores into weights that add to one. And a matrix product from Session 3 takes the weighted average. '
                         'What is new is how the pieces fit together, and you will build it by hand.')))

    S.append(dict(kind='table', title='Exit check: three questions and their short answers', headers=['Question', 'Short answer'],
                  rows=[['What is the entropy of a fair coin, in bits?', '1 bit.'], ['What is the gradient of softmax with cross-entropy with respect to the logits?', 'The prediction minus the target: p - y. The same holds for a sigmoid with binary cross-entropy.'],
                        ['A model has a mean negative log-probability of 2.0 nats per word. What is its perplexity?', f'e^2 = {math.exp(2):.2f}.']],
                  widths=[7.0, 5.0], icons=False, note='Answer each in one sentence before you read the right-hand column.',
                  notes=('Three questions to finish. One, the entropy of a fair coin is one bit. Two, the gradient of softmax with cross-entropy with respect to the logits is the prediction minus the target, and the sigmoid with binary cross-entropy gives the same form. '
                         'Three, if the mean negative log-probability is two nats per word, the perplexity is e squared, which is 7.39. Cover the right-hand column and answer aloud first. '
                         'If one was shaky, mark it. Next session is the course project, and these three ideas come back there.')))

    s['facilitator'] = dict(
        prep=['Run the solution notebook once from the top. Key numbers: entropy 1.75 bits, cross-entropy 2.000 and 1.8007 bits, softmax 0.659 0.242 0.099, cat 0.864 at T = 0.5, top-p keeps 3 drinks, loss 1.417 nats, perplexity 5.21.', 'Open the Session 17 workbook and check that the Check sheet says all checks pass.',
              'Write the identity H(P, Q) = H(P) + KL on the board before concepts.', 'Temperature and top-p are taught here (Session 14 no longer does). The softmax and its stable form are a recall from Session 12.'],
        misconceptions=[('Entropy measures disorder in a physical sense.', 'Here it is the average surprise of outcomes drawn from a distribution, in bits or nats.'), ('KL divergence is a distance.', 'It is not symmetric and does not satisfy the triangle inequality, so it is a divergence.'),
                        ('A higher temperature makes the model more creative on purpose.', 'It only flattens the probabilities, so rarer words are chosen more often.'), ('The same question gives different answers because the model changed.', 'The next word is drawn at random. Temperature and top-p set how much the answers can differ.'),
                        ('Perplexity is a percentage.', 'It is an effective number of choices, from 1 upwards.')],
        probes=[('Why does a certain event have zero surprise?', 'Its probability is 1 and -log2(1) = 0. Nothing new was learned.'), ('Why is cross-entropy never below the entropy?', 'KL divergence is never negative, and cross-entropy is entropy plus KL.'),
                ('Why does top-p rescale the kept words?', 'So that they add to 1 again and can be sampled as a distribution.'),
                ('If the true class gets probability 1, what is the gradient?', 'Zero for every logit. The model is already right and has nothing to learn from this example.'), ('Why is a sigmoid a two-class softmax?', 'Divide top and bottom by e^z1: e^z1 / (e^z1 + e^z2) = 1 / (1 + e^-(z1 - z2)).')],
        lab_steps=[('Step 1: surprise', 'Python and spreadsheet: 1, 3 and 10 bits.'), ('Step 2: entropy', 'Four-word P gives 1.75, fair 1, biased 0.469 bits. The CHANGE (0.99 coin) gives about 0.081.'),
                   ('Step 3: cross-entropy and KL', 'A: 2.000 and 0.250. B: 1.8007 and 0.0507 bits. The identity check passes to six decimals.'), ('Step 4: softmax', 'Stable output for 1000, 1001, 1002 equals softmax of 0, 1, 2. The naive way prints nan.'),
                   ('Step 5: temperature and top-p', 'Cat 0.8638, 0.6590, 0.5017 at T = 0.5, 1, 2. Top-p 0.8 keeps tea, coffee and water; rescaled 0.4992, 0.3346, 0.1662. Spreadsheet: sheet Sampling. The CHANGE (T = 2) keeps 4 drinks.'),
                   ('Step 6: gradient check', 'Formula and numeric gradient agree to five decimals. Entries add to 0. The log-sum-exp form and the two-class sigmoid checks pass. Spreadsheet: B13 and B14 agree for any T.'), ('Step 7: perplexity', 'Sum 9.903, mean 1.6506 nats, perplexity 5.21. The 1/50 CHANGE gives exactly 50, all 1.0 gives 1.')],
        rescue=['If concepts run over, show the derivation slide quickly and spend the time on the by-hand check of the slopes.', 'If lab time is short, do Steps 3, 5 and 7 and leave the gradient check for home.', 'If logarithm bases confuse people, use bits for hand work and nats in code and show 1 bit = 0.693 nats.'],
        after=['Share the notebook and workbook again for absent learners.', 'Note any question you could not answer and open Session 18 with it.', 'Remind learners that the course project has self-checks and no marks, that Session 18 uses the sigmoid form of p - y, and that attention is taught there.'],
        lab_answer_key=[['Step 1 PREDICT: surprises', '1, 3 and 10 bits.'], ['Step 1 READ: halving the probability', 'Adds one bit.'], ['Step 2 PREDICT: which coin has more entropy', 'The fair coin.'],
                        ['Step 2 CHANGE: 0.99 / 0.01 coin', 'Entropy falls to about 0.081 bits: nearly certain outcomes carry little surprise.'], ['Step 3 PREDICT: model B vs A', 'B has the smaller cross-entropy (1.8007 against 2.000 bits).'],
                        ['Step 3 READ: gap to entropy', 'Model A is 0.25 bits above the entropy. That is its KL divergence.'], ['Step 4 PREDICT: biggest probability', 'Cat, and yes they add to 1.'],
                        ['Step 4 READ: why subtract the largest', 'The common factor cancels in the ratio, so the answer is unchanged, and the exponentials stay small.'], ['Step 5 PREDICT: T = 0.5 and top-p', 'More than 0.659 (it is 0.864). Top-p keeps 3 drinks.'],
                        ['Step 5 READ: milk or soup after the cut', 'No. Their probability is set to 0.'], ['Step 5 CHANGE: T = 2', 'The probabilities flatten, so the running total reaches 0.8 later and top-p keeps 4 drinks.'],
                        ['Step 6 PREDICT: sign for the dog logit', 'Negative: that logit should go up.'], ['Step 6 READ: entries add to 0', 'p and y both add to 1, so p - y adds to 0.'],
                        ['Step 7 PREDICT: perplexity between 1 and 20', 'About 5.2.'], ['Step 7 CHANGE: uniform 1/50 model', 'Perplexity 50. All probabilities 1.0 gives 1.']])
    return s
