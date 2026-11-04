"""Session 17: information theory (author F). Every number comes from the solution notebook (labs/s17_nb.py)."""
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
    sm = lambda zz, T: [math.exp(v / T) / sum(math.exp(u / T) for u in zz) for v in zz]
    t05, t2 = sm(z, 0.5), sm(z, 2.0)
    four = ['the', 'a', 'one', 'my']

    s = dict(
        num=17, block='Probability and statistics', short_title='Information theory',
        title='Information theory: entropy, cross-entropy, KL divergence, softmax and perplexity',
        question='How does a language model turn raw scores into a probability for every next word, and how do we score it?',
        outcomes=['Compute surprise, entropy, cross-entropy and KL divergence by hand, and show that cross-entropy = entropy + KL',
                  'Compute the softmax of three scores and derive that the gradient of softmax with cross-entropy is prediction minus target',
                  'Compute the cross-entropy and perplexity of a toy language model on a six word sentence'],
        outcome_icons=['bars', 'calculator', 'chart'],
        outcome_note=('By the end of today you can do three things. First, compute surprise, entropy, cross-entropy and KL divergence by hand, and show that cross-entropy equals entropy plus KL. '
                      'Second, compute the softmax of three scores and derive, with numbers, that the gradient of softmax with cross-entropy is simply the prediction minus the target. '
                      'Third, compute the cross-entropy and the perplexity of a toy language model on a six word sentence. The numbers are illustrative, but the arithmetic is exactly what real training does.'),
        clock=[(10, 'Recall, then a real question from AI'), (35, 'Concept: a picture, then one example by hand'), (10, 'Break'), (45, 'Lab in Python or a spreadsheet: predict, run, change one thing'),
               (15, 'Where this appears in AI, and an exit check'), (5, 'Save the work')],
        plan_title='Your two hours: information, softmax, then perplexity',
        plan_caption='Ideas first. Then the lab, in Python or a spreadsheet. Then AI.',
        plan_note=('Today has the usual shape. Ten minutes of recall from Session 16 and the question of the day. Thirty-five minutes of concepts, each with a picture and a hand example. A ten minute break. '
                   'Then forty-five minutes of lab, where you compute entropy, cross-entropy, the softmax and a perplexity yourself. We finish with where this appears in AI, an exit check and saving your work.'),
        recall_from='Session 16',
        recall=[('What does maximum likelihood estimation choose?', 'The parameter value that makes the observed data most probable, which means the largest likelihood.'),
                ('Why do we work with the log-likelihood?', 'A product of many small probabilities underflows to zero. A sum of logarithms is stable, and the maximum stays at the same parameter.'),
                ('Which assumption about the target gives cross-entropy as the loss?', 'A Bernoulli assumption for yes or no, or a categorical assumption for one of many classes. Gaussian noise gives squared error.')],
        words=[('Entropy', 'The average surprise of a distribution, in bits. How uncertain the outcome is.'),
               ('Cross-entropy', 'The average surprise when reality follows P but the model believes Q. The training loss for classification and language models.'),
               ('KL divergence', 'Kullback-Leibler divergence: cross-entropy minus entropy. The extra cost of believing Q instead of P.'),
               ('Softmax', 'A function that turns scores (logits) into probabilities that are positive and add to 1.'),
               ('Perplexity', 'e to the power of the mean negative log-probability. The effective number of equally likely choices the model has at each word.')],
        word_icons=['bars', 'calculator', 'flag', 'chart', 'question'],
        words_note=('Five words for today. Entropy is the average surprise of a distribution. Cross-entropy is the average surprise when reality follows one distribution and the model believes another. '
                    'KL divergence is the difference between the two, the extra cost of believing the wrong distribution. The softmax turns raw scores into probabilities. '
                    'And perplexity is the standard score for language models, the effective number of equally likely words the model chooses between at each step. We use every one of them today.'),
        keep='Keep your notebook or workbook with all checks passing. Keep six numbers: entropy 1.75 bits, cross-entropy 2.000, KL 0.250, softmax 0.659, gradient -0.758 and perplexity 5.21.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Cross-entropy = entropy + KL', value='2.000 = 1.750 + 0.250'), dict(label='Gradient', value='p - y = (0.659, -0.758, 0.099)'),
                                                              dict(label='Toy perplexity', value='5.21'), dict(label='Next session', value='Capstone: five builds')]),
        keep_title='Save your lab and keep six numbers',
        next='Session 18: the capstone. Build linear regression, logistic regression, PCA, a small network and attention from first principles.', next_label='Next session',
        keep_note=('Before you go, run the notebook or the workbook from the top, check that every check passes and save it. Keep the six numbers on the slide. '
                   'Next session is the capstone. You build linear regression, logistic regression, PCA, a small neural network and attention, all from first principles, and the notebook checks your work automatically. '
                   'The softmax and its gradient from today appear in three of the five builds. Bring one question.'),
        cover_note=('Welcome to Session 17. Last time we saw that training a model is maximum likelihood, and that the loss for classification is cross-entropy. Today we look at cross-entropy from the side of information. '
                    'We ask how surprising an outcome is, how uncertain a distribution is, and how far a model is from reality. We also meet the softmax and perplexity, the two tools you will see in every language model paper.'),
        slides=[])
    S = s['slides']

    S.append(dict(kind='table', title='Answers to the three questions from Session 16', headers=['Question', 'Short answer'], rows=[[q, a] for q, a in s['recall']], widths=[5.0, 7.0], icons=False,
                  note='Today the Bernoulli and categorical losses get a new name and a new meaning.',
                  notes=('Here are the short answers. Maximum likelihood estimation chooses the parameter that makes the observed data most probable. We use the logarithm because a product of many small probabilities underflows, and a sum of logs does not. '
                         'And a Bernoulli or categorical assumption gives cross-entropy, while Gaussian noise gives squared error. Today we ask what cross-entropy means in terms of information. Which of the three answers did you find easiest?')))

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
                  size=26, note='Libraries usually use ln, so their losses are in nats. Bits and nats differ by a constant factor.',
                  notes=('Here is the formula. The surprise of an outcome x is minus the log of its probability. With log base two the unit is the bit. With the natural logarithm the unit is called a nat. '
                         'For an eighth, minus log two of one eighth is three bits, and minus the natural log is 2.079 nats. The two differ by the constant factor 0.693, which is ln 2. '
                         'Machine learning libraries use the natural log, so their losses are in nats. In this session we do hand examples in bits and the lab and the language model in nats. Which unit would you pick for a hand example, and why?')))

    S.append(dict(kind='idea', title='Entropy is the average surprise, and it is largest when the outcome is hardest to guess',
                  visual=dict(kind='f_panels_bars', ymax=0.95, panels=[dict(title='Fair coin', note=f'entropy 1 bit', values=[0.5, 0.5], labels=['heads', 'tails'], show=True, fmt='{:.2f}'),
                                                                      dict(title='Biased coin', note=f'entropy {HB:.3f} bits', values=[0.9, 0.1], labels=['heads', 'tails'], show=True, fmt='{:.2f}'),
                                                                      dict(title='Four next words', note=f'entropy {HP:.2f} bits', values=P, labels=four, show=True, fmt='{:.3f}')]),
                  lead='Entropy H(P) is the average surprise of outcomes drawn from the distribution P.',
                  points=['A fair coin is the hardest to predict: 1 bit.', f'A coin that gives heads 90 percent of the time has only {HB:.3f} bits.'],
                  notes=('Entropy is the average surprise. On the left a fair coin, where each outcome has probability one half, so the average surprise is one bit. In the middle a coin that gives heads nine times in ten. '
                         f'Heads is not surprising and tails is very surprising but rare, so the average is only {HB:.3f} bits. On the right a distribution over four next words, with entropy {HP:.2f} bits. '
                         'Entropy also tells you the smallest average number of bits an ideal code needs per outcome. Which of the three distributions is easiest to predict, and does its entropy agree?')))

    S.append(dict(kind='table', title='By hand: the entropy of four next words is the sum of p times surprise, 1.75 bits',
                  headers=['Next word', 'p', 'Surprise (bits)', 'p × surprise'], rows=[[w, f'{p:g}', f'{-math.log2(p):g}', f'{-p * math.log2(p):g}'] for w, p in zip(four, P)] + [['Total', '1', '', f'{HP:g}']],
                  widths=[3.0, 2.0, 3.0, 3.0], icons=False, note='Illustrative (made-up) probabilities. The total of the last column is the entropy.',
                  notes=('Let us compute it by hand. The first word has probability one half, surprise one bit, and contributes a half. The second has a quarter, two bits, and contributes another half. '
                         'The last two each have an eighth, three bits, and contribute three eighths each. Add the last column: 0.5, plus 0.5, plus 0.375, plus 0.375 gives 1.75 bits. '
                         'These probabilities are made up to give clean arithmetic. What would the entropy be if all four words had probability one quarter?')))

    S.append(dict(kind='formula', title='Entropy is the probability-weighted average of the surprise',
                  formulas=[('Entropy', r'$H(P)=-\sum_{i}p_i\log_2 p_i$'), ('Our four words', r'$H(P)=0.5+0.5+0.375+0.375=1.75$ bits')],
                  symbols=[['P', 'A distribution: probabilities that add to 1.', 'the four next words'], ['p_i', 'The probability of outcome i.', '0.5, 0.25, 0.125, 0.125'], ['sum over i', 'Add the terms for every outcome.', 'four terms'],
                           ['H(P)', 'The entropy, in bits when the log is base 2.', '1.75 bits']],
                  size=26, note='Four equally likely words would have the largest entropy: 2 bits.',
                  notes=('The formula is the table you just filled. Entropy of P is minus the sum over outcomes of p times log two of p. Each term is the probability times its surprise. '
                         'For our four words the terms are 0.5, 0.5, 0.375 and 0.375, which add to 1.75 bits. If all four words were equally likely, the entropy would be the maximum, two bits. '
                         'Notice that entropy depends only on the distribution P. No model is involved. It is a property of the data. Read the symbol table and say what each symbol means for our four words.')))

    S.append(dict(kind='idea', title='Cross-entropy is the average surprise when reality follows P but the model believes Q',
                  visual=dict(kind='f_panels_bars', ymax=0.6, labels=four, panels=[dict(title='Reality P', note='what really happens', values=P, show=True, fmt='{:.3f}'),
                                                                                  dict(title='Model A', note='uniform: every word 0.25', values=QA, show=True, fmt='{:.3f}'), dict(title='Model B', note='closer to reality', values=QB, show=True, fmt='{:.3f}')]),
                  lead='Cross-entropy H(P, Q) averages the model\'s surprise over what really happens.',
                  points=[f'Model A: H(P, Q) = {ceA:.3f} bits.', f'Model B: H(P, Q) = {ceB:.3f} bits. Smaller, because Q is closer to P.'],
                  notes=('Now suppose reality is the distribution on the left, but the model believes one of the other two. Model A spreads probability equally. Model B is closer to reality. '
                         'Cross-entropy asks: on average, how surprised is the model by what really happens? Each outcome occurs with its true probability, but the model measures the surprise with its own probability. '
                         f'Model A scores {ceA:.3f} bits and Model B scores {ceB:.3f}. The model that is closer to reality is less surprised. This number is what training minimises.')))

    S.append(dict(kind='formula', title='Cross-entropy weights the model\'s surprise by the true probabilities',
                  formulas=[('Cross-entropy', r'$H(P,Q)=-\sum_{i}p_i\log_2 q_i$'), ('Model A', r'$H(P,Q_A)=(0.5+0.25+0.125+0.125)\times 2=2.000$')],
                  symbols=[['p_i', 'The true probability of outcome i.', '0.5, 0.25, 0.125, 0.125'], ['q_i', 'The probability the model gives to outcome i.', 'A: 0.25 each'], ['log2 q_i', 'The model\'s surprise at outcome i.', 'A: 2 bits for each'],
                           ['H(P, Q)', 'The cross-entropy.', f'A: 2.000, B: {ceB:.3f}']],
                  size=24, note='With a real label, p is 1 on the true class and 0 elsewhere, so the loss is -log q of the true class.',
                  notes=('Here is the formula. Cross-entropy is minus the sum of the true probability times the log of the model probability. For model A every q is a quarter, so every surprise is two bits, and the average is exactly two. '
                         f'For model B the number is {ceB:.3f}. Now the link to Session 16. When we train on a real example, the true distribution puts probability one on the correct class and zero on the rest. '
                         'Then the sum has one term, and the loss is minus the log of the probability the model gave to the correct class. That is the cross-entropy loss you met last time.')))

    S.append(dict(kind='wide', title='Cross-entropy = entropy + KL divergence: the entropy is fixed, the KL is what the model can improve',
                  visual=dict(kind='f_ce_kl', entropy=HP, rows=[dict(label='Reality alone', ce=HP), dict(label='Model B', ce=ceB), dict(label='Model A (uniform)', ce=ceA)]),
                  caption=f'Model A: {HP:.3f} + {klA:.3f} = {ceA:.3f}. Model B: {HP:.3f} + {klB:.3f} = {ceB:.3f}. All in bits.',
                  notes=(f'Here is the key picture. Every bar starts with the entropy of reality, 1.75 bits, in pale grey. No model can go below it, because that is the uncertainty in the data itself. '
                         f'On top of that the model pays a penalty in red, the KL divergence. Model A pays {klA:.3f} bits and Model B only {klB:.3f}. So cross-entropy equals entropy plus KL. '
                         'During training the entropy of the data does not change, so lowering the cross-entropy is exactly the same as lowering the KL divergence, pulling the model closer to reality. Why can the red part never be negative?')))

    S.append(dict(kind='formula', title='KL divergence is never negative and is zero only when the model equals reality',
                  formulas=[('KL divergence', r'$D_{KL}(P\,\|\,Q)=\sum_{i}p_i\log_2\frac{p_i}{q_i}$'), ('The link', r'$H(P,Q)=H(P)+D_{KL}(P\,\|\,Q)$')],
                  symbols=[['D_KL(P || Q)', 'The extra cost of believing Q when reality is P.', f'A: {klA:.3f}, B: {klB:.3f} bits'], ['Never negative', 'It is 0 only when Q = P everywhere.', 'a perfect model'],
                           ['Not symmetric', 'D(P || Q) is usually not D(Q || P).', 'so it is not a distance'], ['H(P)', 'The entropy of reality.', f'{HP:.2f} bits']],
                  size=22, note='Minimising cross-entropy over the model is the same as minimising KL, because H(P) is fixed.',
                  notes=('The formula for KL divergence is the sum of p times the log of p over q. It measures the extra cost of using the wrong distribution. Three facts. It is never negative. It is zero only when the model equals reality. '
                         'And it is not symmetric, so swapping P and Q gives a different number, which is why we do not call it a distance. The second line is the link we just saw. '
                         'Because the entropy is fixed by the data, minimising the cross-entropy over the model minimises the KL. Which of the two numbers is the loss you would print during training?')))

    S.append(dict(kind='wide', title='The softmax turns raw scores (logits) into probabilities that add to 1',
                  visual=dict(kind='f_panels_bars', labels=['cat', 'dog', 'fox'], panels=[dict(title='Logits z', note='raw scores, any size', values=z, show=True, fmt='{:.1f}'),
                                                                                         dict(title='exp(z)', note='step 1: make them positive', values=ez, show=True, fmt='{:.3f}'),
                                                                                         dict(title='Softmax p', note=f'step 2: divide by the sum, {esum:.3f}', values=pr, show=True, hl=0, fmt='{:.3f}')]),
                  caption=f'Illustrative scores for three classes. The probabilities {pr[0]:.3f} + {pr[1]:.3f} + {pr[2]:.3f} add to 1.',
                  notes=(f'A model produces one raw score per class, called a logit. Here are three, 2.0, 1.0 and 0.1. They can be any size, even negative, so they are not probabilities. '
                         f'The softmax does two steps. First it applies the exponential, which makes every score positive. The values are {ez[0]:.3f}, {ez[1]:.3f} and {ez[2]:.3f}. '
                         f'Then it divides by their sum, {esum:.3f}, so that the results add to one. The probabilities are {pr[0]:.3f}, {pr[1]:.3f} and {pr[2]:.3f}. The biggest score gets the biggest probability, but the others keep a share. Which class would get the biggest share if all three logits were equal?')))

    S.append(dict(kind='formula', title='The softmax formula, and how the temperature T reshapes it',
                  formulas=[('Softmax', r'$p_i=\exp(z_i)\,/\,(\exp(z_1)+\exp(z_2)+\cdots+\exp(z_K))$'), ('With temperature T', r'$p_i=\exp(z_i/T)\,/\,(\exp(z_1/T)+\cdots+\exp(z_K/T))$')],
                  symbols=[['z_i', 'The logit (score) of class i.', f'{z[0]:g}, {z[1]:g}, {z[2]:g}'], ['p_i', 'The probability of class i.', f'{pr[0]:.3f}, {pr[1]:.3f}, {pr[2]:.3f}'], ['K', 'The number of classes.', '3'],
                           ['T', 'The temperature. Small T sharpens, large T flattens.', f'T = 0.5 gives {t05[0]:.3f} to the top class']],
                  size=26, note='In the standard definition of temperature sampling, every logit is divided by T before the softmax.',
                  notes=(f'Here is the softmax as a formula. The probability of class i is e to the z i, divided by the sum of e to the z j over all classes. For our scores that gives {pr[0]:.3f}, {pr[1]:.3f} and {pr[2]:.3f}. '
                         f'The second line adds a temperature T. We divide every logit by T before the softmax. With T equal to 0.5 the top class grows from {pr[0]:.3f} to {t05[0]:.3f}. With T equal to 2 it falls to {t2[0]:.3f}. '
                         'So a low temperature sharpens the distribution and a high temperature flattens it. We come back to this when we look at real systems.')))

    S.append(dict(kind='example', title='Subtract the largest logit first, so large scores cannot overflow',
                  scenario='Illustrative: three logits of 1000, 1001 and 1002. The softmax must give the same answer as for 0, 1 and 2.',
                  blocks=[dict(label='Naive', text='e^1000 is too big for a computer, so it gives inf / inf = nan.', red=True), dict(label='Shift', text='Subtract the largest logit, 1002: the scores become -2, -1, 0.'),
                          dict(label='Exponent', text='e^-2 = 0.135, e^-1 = 0.368, e^0 = 1. Their sum is 1.503.'), dict(label='Result', text='0.135 / 1.503 = 0.090, then 0.245 and 0.665.')],
                  notes=('A practical point. With logits of a thousand, the exponential is too large for any computer to store, so the naive softmax gives infinity over infinity, which is not a number. '
                         'The fix is to subtract the largest logit first. That changes every score by the same amount, and the softmax does not care, because the common factor cancels when we divide. '
                         'The scores become minus two, minus one and zero. Their exponentials are 0.135, 0.368 and 1, which sum to 1.503. The probabilities are 0.090, 0.245 and 0.665, the same as for 0, 1 and 2. All real libraries do this. Why does the common factor cancel?')))

    S.append(dict(kind='wide', title='Softmax with cross-entropy has a simple gradient with respect to the logits: prediction minus target',
                  visual=dict(kind='f_panels_bars', labels=['class 1', 'class 2', 'class 3'], panels=[dict(title='Prediction p', note='from the softmax', values=pr, show=True),
                                                                                                   dict(title='Target y', note='class 2 is the true class', values=[0, 1, 0], show=True, fmt='{:.0f}'),
                                                                                                   dict(title='Gradient p - y', note='the update signal', values=gr, show=True, hl=1)]),
                  caption='Illustrative. The gradient for the true class is negative: its logit should go up.',
                  notes=(f'Training needs the gradient of the loss with respect to the logits, and for softmax with cross-entropy it is beautifully simple. It is the prediction minus the target. '
                         f'Here the true class is the second one, but the model gave it only {pr[1]:.3f}. The gradient for class 2 is {gr[1]:.3f}, negative, which tells the optimiser to raise that logit. '
                         f'The other two entries are positive, {gr[0]:.3f} and {gr[2]:.3f}, so those logits should go down, in proportion to how much probability they took. And the three entries add up to zero. Next we derive it.')))

    S.append(dict(kind='formula', title='Derivation: the gradient of softmax with cross-entropy is p minus y',
                  formulas=[('Slopes', r'$\frac{\partial L}{\partial p_k}=-\frac{y_k}{p_k},\qquad\frac{\partial p_k}{\partial z_j}=p_k(\delta_{kj}-p_j)$'), ('Chain rule', r'$\frac{\partial L}{\partial z_j}=-\sum_k\frac{y_k}{p_k}\,p_k(\delta_{kj}-p_j)=-\sum_k y_k(\delta_{kj}-p_j)=p_j-y_j$')],
                  symbols=[['L', 'The loss: L = -sum of y_k ln p_k.', f'{L0:.3f} in our example'], ['delta_kj', '1 when k = j, and 0 otherwise.', 'picks one term'], ['y_k', 'The one-hot target: 1 for the true class.', 'y = (0, 1, 0)'],
                           ['p_j - y_j', 'The gradient for logit j.', f'({gr[0]:.3f}, {gr[1]:.3f}, {gr[2]:.3f})']],
                  size=20, note='The 1 / p_k cancels p_k. The delta part gives y_j. The other part gives p_j, because the y_k add to 1.',
                  notes=('Here is the derivation, which feeds the implementation you will write. The loss is minus the sum of y k times the log of p k. First we need how each probability moves when a logit moves. '
                         'That is p k times delta k j minus p j, where delta k j is one when k equals j and zero otherwise. The slope of the loss with respect to p k is minus y k over p k. Now the chain rule. The derivative of the loss with respect to z j is minus the sum of y k over p k, times that slope. The p k cancels. '
                         'Split the sum. The delta part gives y j. The other part gives p j times the sum of the y k, and the y k add up to one. The result is p j minus y j.')))

    S.append(dict(kind='example', title=f'By hand: logits 2.0, 1.0, 0.1 with class 2 true give a loss of {L0:.3f}',
                  scenario='Illustrative three-class example. The numbers match the lab.',
                  blocks=[dict(label='Softmax, target', text=f'p = ({pr[0]:.3f}, {pr[1]:.3f}, {pr[2]:.3f}) and y = (0, 1, 0)'), dict(label='Loss', text=f'L = -ln {pr[1]:.3f} = {L0:.3f} nats'),
                          dict(label='Gradient', text=f'p - y = ({gr[0]:.3f}, {gr[1]:.3f}, {gr[2]:.3f}). The three entries add to 0.'),
                          dict(label='Check', text='Add 0.001 to the first logit: the loss rises by about 0.00066.', red=True)],
                  notes=(f'Let us put numbers in. The softmax gives {pr[0]:.3f}, {pr[1]:.3f} and {pr[2]:.3f}. The target is the second class. The loss is minus the natural log of {pr[1]:.3f}, which is {L0:.3f}. '
                         f'The gradient is the prediction minus the target: {gr[0]:.3f}, {gr[1]:.3f} and {gr[2]:.3f}. They add up to zero. '
                         'Now a check you can do on any derivation. Nudge the first logit up by one thousandth and the loss should rise by about the first gradient entry times one thousandth, which is 0.00066. In the lab you do exactly this, for every logit, and compare.')))

    S.append(dict(kind='wide', title='Perplexity: e raised to the power of the mean negative log-probability of the real words',
                  visual=dict(kind='f_tokens', tokens=words, probs=tp, base='e', total_label='Illustrative (made-up numbers): the probability a toy model gave to each real word of the sentence.'),
                  caption=f'Mean -ln p = {tot:.2f} / 6 = {mean:.3f}. Perplexity = e^{mean:.3f} = {ppl:.2f}.',
                  notes=(f'Here is a toy language model scoring a six word sentence. For each real word, the model had given it a probability, 0.2, 0.1, 0.25, 0.5, 0.4 and 0.05. These are made up to show the arithmetic. '
                         f'The red row is minus the natural log of each, and the total is {tot:.2f}. That is the negative log-likelihood of the sentence. Divide by six and the mean is {mean:.3f}, the cross-entropy per word in nats. '
                         f'Perplexity is e to that power, {ppl:.2f}. The weakest words are cat and mat, which got only 0.1 and 0.05. Which word hurt the score most?')))

    S.append(dict(kind='formula', title='Perplexity is the exponential of the cross-entropy per token',
                  formulas=[('Perplexity', r'$\mathrm{PPL}=\exp\left(-\frac{1}{N}\sum_{i=1}^{N}\ln p(w_i\mid w_1,\ldots,w_{i-1})\right)$'), ('Our sentence', r'$\mathrm{PPL}=e^{%.3f}=%.2f$' % (mean, ppl))],
                  symbols=[['N', 'The number of words (tokens) scored.', '6'], ['p(w_i | w_1 ... w_(i-1))', 'The probability the model gave to the real word i, given the words before it.', '0.2, 0.1, 0.25, 0.5, 0.4, 0.05'],
                           ['Mean of -ln p', 'The cross-entropy per word, in nats.', f'{mean:.3f}'], ['PPL', 'Perplexity. In bits it is 2 to the power of the bits per word. Same value.', f'{ppl:.2f}']],
                  size=22, note='Lower is better. Perplexity 1 means the model gave probability 1 to every real word.',
                  notes=(f'Here is the formula. Perplexity is the exponential of the average negative log-probability of the real words, where each probability is conditional on the words before it. For our sentence the average is {mean:.3f} nats and the perplexity is {ppl:.2f}. '
                         'If you work in bits you take two to the power of the bits per word, and you get the same number, because the unit and the base match. '
                         'A perplexity of one means the model gave probability one to every real word. Higher is worse. Read the symbol table and say what N is for our sentence.')))

    S.append(dict(kind='idea', title='Perplexity reads as the effective number of equally likely words the model chooses between',
                  visual=dict(kind='bars', items=[dict(label='A perfect model', value=1), dict(label='Our toy model', value=round(ppl, 2), hl=True), dict(label='Guessing among 50 words', value=50)], unit=''),
                  lead='A perplexity of 5.21 means the model is as unsure as if it picked among about five equally likely words.',
                  points=['Illustrative numbers.', 'Compare perplexities only for the same test text and the same tokens.'],
                  notes=(f'How do we read a perplexity? It is the effective number of equally likely choices the model has at each step. A perfect model has perplexity one. A model that guesses uniformly among fifty words has perplexity fifty. '
                         f'Our toy model has {ppl:.2f}, about five equally likely words per step. One caution. Perplexity depends on how the text is cut into tokens, so only compare models on the same test text and the same tokens. '
                         'Is a perplexity of five good? It depends entirely on the text and the tokens.')))

    S.append(dict(kind='compare', title='Three common mistakes about information measures',
                  left=dict(head='The mistake', points=['Cross-entropy and KL divergence are the same thing.', 'Bits and nats give different perplexities.', 'Lower perplexity always means a better model.']),
                  right=dict(head='The fix', points=['They differ by the entropy of the data.', 'Same value if the exponent matches the log base.', 'Only on the same text and tokens.']),
                  verdict='Always say which log base, and which text.',
                  notes=('Three mistakes. First, cross-entropy and KL are not the same. They differ by the entropy of the data, which training cannot change, so they have the same minimiser but different values. '
                         'Second, bits and nats do not change the perplexity, as long as you exponentiate with the matching base. Two to the bits equals e to the nats. '
                         'Third, a lower perplexity is only meaningful when two models are scored on the same text with the same tokens. Which of the three would you have made?')))

    S.append(dict(kind='code', title='Read the recipe before you write it: entropy, KL, softmax, gradient, perplexity',
                  code='H = -np.sum(P * np.log2(P))\nkl = np.sum(P * np.log2(P / Q))\np = np.exp(z - z.max()); p = p / p.sum()\ngrad = p - y\nppl = np.exp(np.mean(-np.log(token_probs)))',
                  reads=['Line 1: entropy in bits.', 'Line 2: KL divergence. Cross-entropy = H + kl.', 'Line 3: stable softmax: shift by the largest logit.', 'Line 4: the gradient with respect to the logits.', 'Line 5: perplexity from the word probabilities.',
                         'Spreadsheet: a column =LOG(q,2), SUMPRODUCT, and =EXP(AVERAGE(...)).'],
                  notes=('Before the lab, read the recipe. Entropy is minus the sum of P times log two of P. KL divergence is the sum of P times log two of P over Q, and cross-entropy is entropy plus that. '
                         'The stable softmax subtracts the largest logit, takes the exponential and divides by the sum. The gradient is the prediction minus the target. Perplexity is the exponential of the mean negative log-probability. '
                         'In a spreadsheet you build a column of logarithms with the LOG function and base two, and use SUMPRODUCT to add them up with weights. Every line is explained again in the notebook and the workbook.')))

    S.append(dict(kind='divider', title='Part 2: the lab', lead='Close the slides. Open the notebook or the workbook.', section='Lab',
                  notes=('That is the end of the concepts. Everything you need is on the slides you have just seen. Open the notebook or the workbook now. '
                         'In Python, run the cells from the top in order. In the spreadsheet, start on the sheet called Start here. Raise your hand if something does not run. '
                         'Keep the rhythm: predict first, run, read, then change one thing.')))

    S.append(dict(kind='steps', title='The lab has six steps: surprise, entropy, cross-entropy, softmax, gradient and perplexity',
                  steps=[dict(head='1 Surprise', text='Bits for three events', icon='flag'), dict(head='2 Entropy', text='Fair, biased and four words', icon='bars'), dict(head='3 CE and KL', text='Two models against reality', icon='calculator'),
                         dict(head='4 Softmax', text='Stable version and temperature', icon='gear'), dict(head='5 Gradient', text='p - y against a numeric check', icon='check'), dict(head='6 Perplexity', text='A six word sentence', icon='chart')],
                  caption='Python: Steps 1 to 6 in the notebook. Spreadsheet: sheets Entropy, Softmax and Perplexity with the same numbers. Predict, run, change one thing.',
                  notes=('Here are the six steps. In the first you compute the surprise of three events in bits. In the second the entropy of a fair coin, a biased coin and four words. '
                         'In the third the cross-entropy and the KL divergence of two models, and you confirm that cross-entropy equals entropy plus KL. In the fourth you build the stable softmax. '
                         'In the fifth you check the gradient p minus y against a numeric gradient made by nudging each logit. In the sixth you compute a perplexity. The spreadsheet has the same numbers on three sheets. Do not skip the predict cells.')))

    S.append(dict(kind='table', title='Check your numbers against these before you move on',
                  headers=['What you compute', 'You should see'],
                  rows=[['Surprise of 1/2, 1/8 and 1/1024 in bits', '1, 3, 10'], ['Entropy of the four-word P, fair coin, 0.9 coin', f'{HP:g}, 1, {HB:.3f} bits'], ['Cross-entropy of model A and model B', f'{ceA:.3f} and {ceB:.3f} bits'],
                        ['KL divergence of model A and model B', f'{klA:.3f} and {klB:.3f} bits'], ['Softmax of 2.0, 1.0, 0.1', f'{pr[0]:.4f}, {pr[1]:.4f}, {pr[2]:.4f}'], ['Loss and gradient p - y (class 2 true)', f'{L0:.4f}; {gr[0]:.4f}, {gr[1]:.4f}, {gr[2]:.4f}'],
                        ['Sum of -ln p, mean, perplexity of the sentence', f'{tot:.3f}, {mean:.4f}, {ppl:.3f}']],
                  widths=[6.4, 5.2], icons=['flag', 'bars', 'calculator', 'chart', 'gear', 'check', 'clock'],
                  note='If your number differs, stop and ask. Find the step that went wrong. Do not change a number to match.',
                  notes=('Use this table as your checkpoint. The surprises are one, three and ten bits. The entropy of the four words is 1.75. Model A has cross-entropy exactly two and model B has 1.8007. '
                         'The softmax of 2, 1 and 0.1 is 0.659, 0.242 and 0.099. The loss is 1.417 and the gradient is 0.659, minus 0.758 and 0.099. The sentence has a perplexity of 5.21. '
                         'If a number is different, stop and call me over. Do not edit a number to make it match. The usual cause is a cell run out of order.')))

    S.append(dict(kind='table', title='Errors you will meet, what they mean and what to do',
                  headers=['What you see', 'What it means', 'What to do'],
                  rows=[['nan from the softmax', 'The exponential overflowed', 'Subtract the largest logit first'], ['TypeError: NoneType', 'An answer cell (marked gold) still says None', 'Replace None with your code and run again'],
                        ['A negative KL divergence', 'P and Q are swapped, or they do not add to 1', 'Check both add to 1 and keep the order P then Q'], ['Spreadsheet shows #DIV/0! or #NUM!', 'A probability of 0 inside a logarithm', 'Use only probabilities above 0']],
                  widths=[3.6, 4.2, 4.2], icons=['bell', 'key', 'cross', 'flag'],
                  notes=('Four errors you may meet. A nan from the softmax means the exponential overflowed, so subtract the largest logit first. A type error about None means a gold cell still holds the placeholder. '
                         'A negative KL divergence is impossible, so check that P and Q both add to one and that you kept P first. And in the spreadsheet, a divide by zero or a number error means a probability of zero is inside a logarithm. '
                         'Read the last line of any error first. It usually tells you what to do.')))

    S.append(dict(kind='idea', title='Where this appears in AI: pre-training by minimising cross-entropy on the next token',
                  visual=dict(kind='flow', steps=[dict(head='Text in', text='Tokens, then embeddings', icon='doc'), dict(head='Logits', text='One score per word in the vocabulary', icon='bars'), dict(head='Softmax', text='Scores become probabilities', icon='gear'),
                                                  dict(head='Loss', text='Cross-entropy against the real next word', icon='check')], highlight=3),
                  lead='Published research describes transformer language models as pre-trained by minimising cross-entropy on the next token.',
                  points=['The p - y gradient from today is the signal that starts backpropagation.', 'Later stages, such as learning from human feedback, use other objectives. Closed products do not publish their internals.'],
                  notes=('Here is a real system, as published research describes transformer language models in pre-training. Text becomes tokens. The network produces one score, a logit, for every word in its vocabulary. A softmax turns the scores into probabilities. '
                         'During training, the cross-entropy against the real next word is the loss, and its gradient with respect to the logits is the prediction minus the target, exactly what you derived. That signal then flows backwards through the network. '
                         'The exact designs of ChatGPT, Gemini and Claude are not published, so I describe the published framework and make no claim about their internals. Where in the picture does the p minus y gradient appear?')))

    S.append(dict(kind='wide', title='Where this appears in AI: the temperature setting reshapes the softmax',
                  visual=dict(kind='f_panels_bars', labels=['cat', 'dog', 'fox'], panels=[dict(title='T = 0.5', note='sharper', values=t05, show=True), dict(title='T = 1', note='the plain softmax', values=pr, show=True),
                                                                                          dict(title='T = 2', note='flatter', values=t2, show=True)]),
                  caption='Illustrative logits 2.0, 1.0, 0.1. Public APIs document temperature and top-p settings.',
                  notes=('The vendors of ChatGPT, Gemini and Claude all document a temperature setting in their public APIs. In the standard definition of temperature sampling, the logits are divided by the temperature before the softmax, which is what you see here. '
                         f'At a low temperature, 0.5, the top class takes {t05[0]:.3f} and the answers become more predictable. At a high temperature, 2, it takes only {t2[0]:.3f} and the choice is more random. '
                         'That is why the same question can give different answers. I am describing the published mathematics. I make no claim about the exact settings of any product. Perplexity, the score you just computed, is also a standard way that published papers report how well a language model predicts held-out text.')))

    S.append(dict(kind='practice', title="Check an AI assistant's answer against your own numbers", minutes=5, label='Optional, with any assistant',
                  task='Ask an assistant for the softmax of the logits 2.0, 1.0, 0.1 and the cross-entropy loss if class 2 is true.',
                  steps=[f'Compare with {pr[0]:.3f}, {pr[1]:.3f}, {pr[2]:.3f} and a loss of {L0:.3f} (natural log).', 'Ask which log base it used. Bits would give 2.04.', 'Never paste confidential data into an assistant.'],
                  output='A note: where the assistant agreed with your numbers, and where it did not.',
                  notes=('Here is an activity with any assistant. Ask it for the softmax of the logits two, one and nought point one, and the cross-entropy loss when the second class is true. '
                         f'Compare with your numbers, {pr[0]:.3f}, {pr[1]:.3f} and {pr[2]:.3f}, and a loss of {L0:.3f}. Then ask which logarithm base it used. With base two the loss would be 2.04 bits instead. '
                         'An assistant can slip on arithmetic or on the unit, and now you can check. Please do not paste confidential data into any assistant.')))

    S.append(dict(kind='table', title='Exit check: three questions and their short answers', headers=['Question', 'Short answer'],
                  rows=[['What is the entropy of a fair coin, in bits?', '1 bit.'], ['What is the gradient of softmax with cross-entropy with respect to the logits?', 'The prediction minus the target: p - y.'],
                        ['A model has a mean negative log-probability of 2.0 nats per word. What is its perplexity?', f'e^2 = {math.exp(2):.2f}.']],
                  widths=[7.0, 5.0], icons=False, note='Answer each in one sentence before you read the right-hand column.',
                  notes=('Three questions to finish. One, the entropy of a fair coin is one bit. Two, the gradient of softmax with cross-entropy with respect to the logits is the prediction minus the target. '
                         'Three, if the mean negative log-probability is two nats per word, the perplexity is e squared, which is 7.39. Cover the right-hand column and answer aloud first. '
                         'If one was shaky, mark it. Next session is the capstone, and these three ideas come back there.')))

    s['facilitator'] = dict(
        prep=['Run the solution notebook once from the top. Key numbers: entropy 1.75, cross-entropy 2.000 and 1.8007, softmax 0.659 0.242 0.099, perplexity 5.21.', 'Open the Session 17 workbook and check that the Check sheet says all checks pass.',
              'Write the identity H(P, Q) = H(P) + KL on the board before concepts.', 'Have a calculator ready to show -log2 of 1/8 on request.'],
        misconceptions=[('Entropy measures disorder in a physical sense.', 'Here it is the average surprise of outcomes drawn from a distribution, in bits.'), ('KL divergence is a distance.', 'It is not symmetric and does not satisfy the triangle inequality, so it is a divergence.'),
                        ('The softmax picks the biggest score.', 'It gives every class a positive probability. Argmax picks the biggest. The softmax is a smooth version.'), ('Perplexity is a percentage.', 'It is an effective number of choices, from 1 upwards.')],
        probes=[('Why does a certain event have zero surprise?', 'Its probability is 1 and -log2(1) = 0. Nothing new was learned.'), ('Why is cross-entropy never below the entropy?', 'KL divergence is never negative, and cross-entropy is entropy plus KL.'),
                ('Why do we subtract the largest logit before the exponential?', 'It prevents overflow and does not change the result, because the common factor cancels in the ratio.'),
                ('If the true class gets probability 1, what is the gradient?', 'Zero for every logit. The model is already right and has nothing to learn from this example.'), ('Does a lower perplexity mean the model is more truthful?', 'No. It means it predicts the held-out text better. Truthfulness is a different property.')],
        lab_steps=[('Step 1: surprise', 'Python and spreadsheet: 1, 3 and 10 bits.'), ('Step 2: entropy', 'Four-word P gives 1.75, fair 1, biased 0.469. The CHANGE (0.99 coin) gives about 0.081.'),
                   ('Step 3: cross-entropy and KL', 'A: 2.000 and 0.250. B: 1.8007 and 0.0507. The identity check passes to six decimals.'), ('Step 4: softmax', 'Stable output for 1000, 1001, 1002 equals softmax of 0, 1, 2. The naive way prints nan.'),
                   ('Step 5: gradient check', 'Formula and numeric gradient agree to five decimals. Entries add to 0.'), ('Step 6: perplexity', 'Sum 9.903, mean 1.6505, perplexity 5.21. The 1/50 CHANGE gives exactly 50, all 1.0 gives 1.')],
        rescue=['If concepts run over, skip the stable softmax example and show it in the lab.', 'If lab time is short, do Steps 3, 4 and 6 and leave the gradient check for home.', 'If logarithm bases confuse people, use bits for hand work and nats in code and show 1 bit = 0.693 nats.'],
        after=['Share the notebook and workbook again for absent learners.', 'Note any question you could not answer and open Session 18 with it.', 'Remind learners that the capstone is individual and auto-graded, and that Session 18 reuses the softmax gradient.'],
        lab_answer_key=[['Step 1 PREDICT: surprises', '1, 3 and 10 bits.'], ['Step 1 READ: halving the probability', 'Adds one bit.'], ['Step 2 PREDICT: which coin has more entropy', 'The fair coin.'],
                        ['Step 2 CHANGE: 0.99 / 0.01 coin', 'Entropy falls to about 0.081 bits: nearly certain outcomes carry little surprise.'], ['Step 3 PREDICT: model B vs A', 'B has the smaller cross-entropy (1.8007 against 2.000).'],
                        ['Step 3 READ: gap to entropy', 'Model A is 0.25 bits above the entropy. That is its KL divergence.'], ['Step 4 PREDICT: biggest probability', 'The first class, and yes they add to 1.'],
                        ['Step 4 READ: why subtract the largest', 'The common factor cancels in the ratio, so the answer is unchanged, and the exponentials stay small.'], ['Step 4 CHANGE: temperature', 'T = 0.5 makes the model more sure of the top class.'],
                        ['Step 5 PREDICT: sign for the second logit', 'Negative: that logit should go up.'], ['Step 5 READ: entries add to 0', 'p and y both add to 1, so p - y adds to 0.'],
                        ['Step 6 PREDICT: perplexity between 1 and 20', 'About 5.2.'], ['Step 6 CHANGE: uniform 1/50 model', 'Perplexity 50. All probabilities 1.0 gives 1.']])
    return s
