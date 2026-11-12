"""Session 12: Optimisation in practice. Author D.

Part A keeps the weights sensible (ridge penalty, weight decay, a weight limit).
Part B keeps the numbers inside the computer sensible (softmax taught here, overflow, the stable form, log-sum-exp, underflow, vanishing gradients, clipping)."""
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'kit'))
import diagrams_math_d as D  # noqa: E402


def build():
    n = D.n12()
    R = {r['lam']: r for r in n['rows']}
    r0, r3, r5 = R[0.0], R[0.1], R[10.0]
    xg, f = n['xg'], n['f']
    sb, ss, lse, es = n['soft_big'], n['soft_small'], n['lse_big'], n['exp_small']
    lam_b, rt = n['lam_best'], n['rmse_test']
    xr = n['xrow']
    cond = n['cond0']

    def panel(lam, title, note):
        return dict(title=title, note=note, x=xg, y=n['curves'][lam], xt=n['xtr'], yt=n['ytr'], xf=xg, yf=f(xg))

    s = dict(
        num=12, block='Calculus and optimisation', short_title='Optimisation in practice',
        title='Optimisation in practice: keep the weights small, then keep the numbers in range',
        question='How do we limit memorising in a model with billions of numbers, and why does a very long answer not overflow the computer?',
        outcomes=['Fit a curve with a ridge (L2) penalty, choose lambda on validation points, and report the test error once',
                  'Explain weight decay and a limit on the size of the weights as two faces of the same penalty',
                  'Compute a softmax by hand, then compute it and a log-sum-exp without overflow by subtracting the maximum'],
        outcome_icons=['chart', 'key', 'check'],
        outcome_note=('By the end of today you can do three things. Fit a curve with a ridge penalty, choose its strength on validation points, and report the error on test points once. '
                      'Explain weight decay and a limit on the weights as the same penalty seen two ways. '
                      'And compute a softmax, first by hand and then without overflow, by subtracting the maximum. The first part keeps the weights sensible; the second keeps the numbers inside the computer sensible.'),
        clock=[(10, 'Recall and a real question from AI'), (35, 'Concept: a picture, then a hand example'), (10, 'Break'), (45, 'Lab: Python or spreadsheet, predict, run, change'),
               (15, 'Where it appears in AI, plus an exit check'), (5, 'Save the work')],
        plan_title='Your two hours: sensible weights first, then sensible numbers',
        plan_caption='Part A: a penalty against overfitting. Part B: softmax and arithmetic that stays in range. Then the lab.',
        plan_note=('We have two hours. The first ten minutes recall backpropagation and ask the question of the day. The thirty-five minutes of concepts come in two parts. Part A keeps the weights sensible: the ridge penalty, weight decay and a limit on the weights. '
                   'Part B keeps the numbers sensible: softmax, overflow and its fix, sums of logs, and gradients that vanish or explode. After the break, forty-five minutes of lab, then where these ideas appear in large language models.'),
        recall_from='Session 11',
        recall=[('In our tiny network, what is delta(2) and what value did it have?', 'delta(2) is the slope of the loss with respect to the prediction, y-hat - y. It was 0.1733 - 1 = -0.8267.'),
                ('Why does the hidden delta contain a × (1 minus a)?', 'a × (1 - a) is the slope of the sigmoid. The chain rule multiplies it into the slope that arrives from the output.'),
                ('Which values from the forward pass does the backward pass reuse?', 'The hidden outputs a(1) and the inputs x, which multiply the deltas to give the gradients. They are stored during the forward pass.')],
        words=[('Regularisation', 'Any change to training that discourages a model from memorising its training data.'),
               ('L2 penalty (ridge) and weight decay', 'Lambda times the sum of the squared weights, added to the loss. In plain gradient descent it shrinks every weight a little at each update.'),
               ('Softmax', 'Turns a list of scores (logits) into probabilities that are positive and add up to 1.'),
               ('Overflow and underflow', 'A result too large or too small for the number format: it becomes inf or 0.'),
               ('Log-sum-exp', 'm + ln(sum of e^(z - m)) with m the largest score: the log of a sum of exponentials, computed safely.')],
        word_icons=['gear', 'calculator', 'chart', 'bell', 'key'],
        words_note=('Five words for today. Regularisation is anything that discourages memorising. The L2 penalty, also called ridge, adds lambda times the sum of squared weights to the loss, and in plain gradient descent that is the same as weight decay, a small shrink at every update. '
                    'Softmax turns scores into probabilities. Overflow and underflow mean a result too large or too small for the number format. And log-sum-exp is the safe way to take the log of a sum of exponentials.'),
        keep='Keep your saved notebook or workbook, with the ridge fit for several values of lambda, the test error, and the stable softmax. Write down the rule: subtract the maximum before you exponentiate.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Penalty', value='lambda × sum of w^2'), dict(label='Chosen lambda', value=f'{lam_b:g}, test error {rt:.3f}'),
                                                              dict(label='Stable softmax', value='subtract the maximum'), dict(label='Next session', value='Probability basics')]),
        keep_title='Save your lab and keep the two rules',
        next='Session 13: probability basics: random variables, expectation and variance.', next_label='Next session',
        keep_note=('Before you go, save your notebook or workbook. Keep the ridge fit for the different values of lambda, the test error you reported once, and the stable softmax. Keep one rule in your head: subtract the maximum before you exponentiate. '
                   'Next session starts a new block, probability. The softmax you met today comes straight back, because it turns scores into probabilities.'),
        cover_note=('Welcome to Session 12. So far we found gradients and took steps along them. Today we ask what goes wrong in practice, in two parts. '
                    'In Part A, a model with enough numbers memorises its training data, and a penalty on the weights controls that. In Part B, a perfectly correct formula overflows on a computer, and a one-line trick fixes it. '
                    'Both ideas are inside every large language model.'),
        slides=[])
    S = s['slides']

    S.append(dict(kind='table', title='Answers to the three questions from Session 11', headers=['Question', 'Short answer'], rows=[[q, a] for q, a in s['recall']], widths=[5.6, 6.4], icons=False,
                  note='Check your answers. If one surprised you, look at Session 11 before the lab.',
                  notes=('Delta two, written delta in brackets two, is the slope of the loss with respect to the prediction. It equals the prediction minus the target, and in our network it was minus point eight two six seven. '
                         'The hidden delta contains a times one minus a because that is the slope of the sigmoid, derived last time, and the chain rule multiplies it into the slope arriving from the output. '
                         'And the backward pass reuses the hidden outputs and the inputs, stored during the forward pass. Today we look at what can go wrong around those passes.')))

    # ------------------------------------------------------------------ Part A: keep the weights sensible
    S.append(dict(kind='wide', title='A curve with too much freedom chases the noise: that is overfitting',
                  visual=dict(kind='d_ridge', panels=[panel(0.0, 'No penalty (lambda = 0)', 'Swings between the points'),
                                                     panel(0.1, 'Small penalty (lambda = 0.1)', 'Smooth and close to truth'),
                                                     panel(10.0, 'Large penalty (lambda = 10)', 'Too stiff: misses the pattern')]),
                  caption='Part A. Dots: 10 training points. Dashed: true curve. Red: the degree 9 fit. Illustrative data.',
                  notes=('Part A is about keeping the weights sensible. Ten training points, the black dots, come from a curve with a little noise; the dashed line is the true curve. We fit a polynomial of degree nine: a sum of ten terms, a constant, x, x squared and so on up to x to the ninth, each with its own weight. '
                         'On the left there is no penalty, and the red curve passes through every dot but swings wildly between them. That is overfitting: the model has memorised the noise. '
                         'In the middle a small penalty gives a smooth curve close to the truth. On the right a large penalty makes the curve too stiff.')))

    S.append(dict(kind='formula', title='The L2 (ridge) penalty adds the size of the weights to the loss',
                  formulas=[('Ridge loss (sum of squared errors plus penalty)', r'$L(w) = \sum_{i=1}^{n}(\hat{y}_i - y_i)^2 + \lambda\sum_{j=1}^{d} w_j^2$'),
                            ('Prediction', r'$\hat{y} = b + w_1 x + w_2 x^2 + \dots + w_9 x^9$')],
                  symbols=[['lambda', 'The penalty strength, chosen by us. Larger means smaller weights.', '0, 0.001, 0.01, 0.1, 1, 10'],
                           ['sum of w^2', 'The squared L2 norm of the weights (Session 2). The intercept b is left out.', 'about 104,000 at lambda = 0'],
                           ['n, d', 'Number of training points; number of penalised weights.', 'n = 10, d = 9'],
                           ['First term', 'The sum of squared errors, SSE (Session 10). Libraries often use the mean: then the same effect needs a lambda n times smaller.', 'SSE, no division by n']],
                  size=20, widths=[1.9, 6.6, 3.4], note='First term: fit the data. Second term: keep the weights small. Lambda sets the balance.',
                  notes=('The ridge loss has two terms. The first is the sum of squared errors on the training points. Session 10 showed that the sum and the mean have the same minimum, and every number today uses the sum. The second term is lambda times the sum of the squared weights, the squared L2 norm from Session 2. '
                         'Lambda is a number we choose. With lambda zero we fit the data and ignore the weights. With a large lambda the weights are squeezed towards zero. '
                         'The intercept b is left out of the penalty, so that the whole curve can still shift up or down. A library that uses the mean needs a lambda ten times smaller here for the same effect.')))

    S.append(dict(kind='table', title='By hand: one weight, three points, and what lambda does to it',
                  headers=['lambda', 'Formula: w = sum(x y) / (sum(x^2) plus lambda)', 'Weight w', 'Share of the plain fit'],
                  rows=[['0', '28.5 / 14', f'{28.5 / 14:.4f}', '100%'], ['1', '28.5 / 15', f'{28.5 / 15:.4f}', f'{100 * 14 / 15:.0f}%'], ['14', '28.5 / 28', f'{28.5 / 28:.4f}', '50%'], ['140', '28.5 / 154', f'{28.5 / 154:.4f}', f'{100 * 14 / 154:.0f}%']],
                  widths=[1.4, 5.4, 2.4, 2.8], icons=False,
                  note='Data (illustrative): x = 1, 2, 3 and y = 2.1, 3.9, 6.2, so sum(x y) = 2.1 + 7.8 + 18.6 = 28.5 and sum(x^2) = 1 + 4 + 9 = 14. Model: y-hat = w x.',
                  notes=('A hand example with one weight. Three points: x is one, two, three, and y is two point one, three point nine, six point two. The sum of x times y is twenty-eight point five, and the sum of x squared is fourteen. '
                         'With lambda zero the best weight is twenty-eight point five over fourteen, which is two point zero three six. With lambda one the denominator grows to fifteen and the weight shrinks to one point nine. '
                         'When lambda equals fourteen the weight is exactly halved, and with lambda one hundred forty it is almost zero. The penalty shrinks the weight smoothly towards zero.')))

    S.append(dict(kind='formula', title='Ridge has a closed-form answer: add lambda to the diagonal, then solve',
                  formulas=[('Closed form', r'$w = \left(X^{T}X + \lambda P\right)^{-1} X^{T} y$')],
                  symbols=[['X', 'Design matrix: one row per point, columns 1, x, ..., x^9. A line (Session 4) uses two columns.', f'x = 0.333: {xr[0]:.0f}, {xr[1]:.3f}, {xr[2]:.3f}, {xr[3]:.3f}, ...'],
                           ['X^T X', 'The square matrix of the normal equation (Session 4).', '10 × 10'],
                           ['lambda P', 'Lambda on the diagonal. P is the identity with first entry 0: no penalty on the intercept.', 'lambda = 0.1'],
                           ['Badly conditioned', 'Tiny changes in y or rounding cause huge changes in w (condition number).', f'about {cond / 1e7:.0f} × 10^7 at lambda = 0']],
                  size=24, widths=[2.0, 6.3, 3.6], note='In practice a solver is used instead of an explicit inverse. Adding lambda makes the matrix well behaved.',
                  notes=('The ridge problem has a closed-form answer, the normal equation from Session 4 with one change: add lambda times a matrix P to X transpose X. P is the identity with its first entry set to zero, so lambda lands on the diagonal except for the intercept. '
                         'X has one row per training point, with the powers of x as its columns. For x equal to a third, the row starts one, point three three three, point one one one, and the powers shrink fast. '
                         f'Without the penalty the matrix is badly conditioned, with a condition number of about {cond / 1e7:.0f} times ten to the seven, so tiny changes in the data give huge changes in the weights. Adding lambda calms that down.')))

    rows = [[f'{r["lam"]:g}', f'{r["norm2"]:.4f}' if r['norm2'] < 1000 else f'{r["norm2"]:,.0f}', f'{r["rmse_tr"]:.4f}', f'{r["rmse_te"]:.4f}'] for r in n['rows']]
    S.append(dict(kind='table', title='Choose lambda on validation points: among six values, 0.1 gives the lowest validation error',
                  headers=['lambda', 'Sum of the squared weights', 'Training error (RMSE)', 'Validation error, 20 points (RMSE)'], rows=rows, widths=[1.6, 3.7, 3.1, 3.8], icons=False,
                  note=f'RMSE = root mean squared error. Validation points choose lambda; 20 test points, unused until then, give {rt:.3f} once. A finer grid finds 0.2 slightly lower ({n["rmse_val_02"]:.4f}).',
                  notes=(f'The second column shows the weights shrinking: the sum of squared weights falls from about {r0["norm2"]:,.0f} with no penalty to {r3["norm2"]:.2f} at lambda point one. '
                         f'The training error rises as lambda grows, because the curve fits the training points less closely. The validation error is {r0["rmse_te"]:.2f} with no penalty, falls to {r3["rmse_te"]:.3f} at lambda point one, then rises again, so we choose point one. '
                         f'Because we used the validation points to choose, their error flatters us. So we keep a third set, the test points, untouched until the choice is made, and report its error once: {rt:.3f}, a little worse, as it usually is.')))

    S.append(dict(kind='formula', title='Weight decay: every update first shrinks the weights by a small factor',
                  formulas=[('L2 penalty in the update', r'$w \leftarrow w - \eta\left(\frac{\partial L}{\partial w} + 2\lambda w\right)$'),
                            ('Weight decay form', r'$w \leftarrow (1 - 2\eta\lambda)\,w - \eta\,\frac{\partial L}{\partial w}$')],
                  symbols=[['eta', 'The learning rate (Session 10).', 'eta = 0.1'],
                           ['dL/dw', 'The slope of the loss without the penalty.', 'illustrative: 1'],
                           ['lambda', 'The penalty strength. In plain SGD libraries the weight_decay setting equals 2 lambda.', 'lambda = 0.5'],
                           ['1 minus 2 eta lambda', 'The shrink factor applied to w before the gradient step.', '1 - 2 × 0.1 × 0.5 = 0.9']],
                  size=18, widths=[2.2, 5.6, 4.1], note='Worked: w = 2 gives 0.9 × 2 - 0.1 × 1 = 1.7. AdamW (Loshchilov and Hutter, 2017) shrinks in a separate step.',
                  notes=('The penalty has a simple effect on the update rule. The derivative of lambda times w squared is two lambda w, so each step subtracts eta times the usual gradient plus two lambda w. '
                         'Collect the w terms and you get the second line: first multiply w by a number slightly below one, then take the usual gradient step. That is why it is called weight decay: every update shrinks the weights a little. '
                         'With eta point one, lambda point five, w equal to two and a gradient of one, the new weight is one point seven. With Adam the two forms differ, and the published variant called AdamW applies the shrink separately.')))

    S.append(dict(kind='idea', title='A penalty and a limit on the weights are two ways to say: keep the weights small',
                  visual=dict(kind='d_lagrange', which='disc'),
                  lead='Ridge = the best weights inside a circle. Larger lambda, smaller circle.',
                  points=['The best allowed point is where a loss ring just touches the circle.',
                          'On the line w1 + w2 = 2, the smallest w1^2 + w2^2 is 2, at (1, 1).'],
                  notes=('The penalty has a second face. Ask for the best weights, but only inside a circle: the sum of squared weights must not exceed a limit. That is called a constraint. '
                         'The best fit with no limit lies outside the circle, so the best allowed point sits on the circle, where a ring of equal loss just touches it. A larger lambda corresponds to a smaller circle; the equivalence is standard in statistics texts. '
                         'The lab tries the same idea on a straight line: walk along w one plus w two equals two, and the loss w one squared plus w two squared is lowest at one comma one, where it equals two.')))

    S.append(dict(kind='statement', title='From sensible weights to sensible numbers: a correct formula can still fail on a computer',
                  lead='Part A kept the weights sensible. Part B keeps the numbers sensible.',
                  points=['A computer stores each number in a fixed number of bits.', 'A result too large becomes inf (overflow); too small becomes 0 (underflow).', 'inf / inf gives nan, short for not a number.'], icons=['gear', 'bell', 'cross'],
                  notes=('That closes Part A. Part B asks a different question with the same aim, keeping training reliable. Everything so far was mathematics on paper. A computer stores each number with a fixed number of bits. A result that is too large becomes infinity, and a result that is too small becomes zero. '
                         'Infinity divided by infinity is not a number, which the computer writes as nan. So a formula that is correct on paper can fail in a program. The fixes are small algebra tricks, and the first place we need them is softmax.')))

    # ------------------------------------------------------------------ Part B: keep the numbers sensible
    S.append(dict(kind='idea', title='Softmax turns any list of scores into probabilities that add up to 1',
                  visual=dict(kind='d_softmax_bars', scores=[2.0, 1.0, 0.1]),
                  lead='Raise e to each score (logit), then divide by the total.',
                  points=['softmax(z)_i = e^(z_i) / sum of e^(z_j).', f'Scores 2, 1, 0.1: e^z = {es[0]:.3f}, {es[1]:.3f}, {es[2]:.3f}; total {es.sum():.3f}.',
                          f'Divide: {ss[0]:.3f}, {ss[1]:.3f}, {ss[2]:.3f}, adding to 1.'],
                  notes=('Softmax is the step that turns a model\'s raw scores into probabilities. The raw scores are called logits, and they can be any numbers, negative or large. '
                         f'Softmax takes e to the power of each score, which makes every one positive, then divides by the total so they add up to one. For the scores two, one and point one, the exponentials are {es[0]:.3f}, {es[1]:.3f} and {es[2]:.3f}, with total {es.sum():.3f}. '
                         f'Dividing gives {ss[0]:.3f}, {ss[1]:.3f} and {ss[2]:.3f}. The order of the scores is kept. Session 17 builds on this with temperature and cross-entropy.')))

    S.append(dict(kind='idea', title='Each number format has a largest value, and e^z passes it quickly',
                  visual=dict(kind='d_precision'),
                  lead='Fewer bits mean a smaller range and fewer digits.',
                  points=['e^z is inf from z = 710 (float64), 89 (float32), 12 (float16).',
                          'float16 keeps about 3 digits: 1 + 0.0004 is stored as 1.',
                          '16-bit training keeps a 32-bit weight copy and scales the loss (Micikevicius et al., 2017).'],
                  notes=('Each number is stored as a sign, an exponent and a mantissa. The exponent sets the range; the mantissa sets how many digits are kept. Float sixty-four, the numpy default, reaches about ten to the three hundred and eight. Float thirty-two reaches about three times ten to the thirty-eight. Float sixteen stops at sixty-five thousand five hundred and four. '
                         'So e to the twelve already overflows in float sixteen, and softmax needs the exponential of every score. Sixteen-bit numbers halve the memory, which is why published training uses them with care. Bfloat sixteen keeps the float thirty-two range with fewer digits.')))

    S.append(dict(kind='formula', title='Subtracting the largest score keeps softmax exact and stops the overflow',
                  formulas=[('Shift by a constant c', r'$\frac{e^{z_i - c}}{\sum_j e^{z_j - c}} = \frac{e^{z_i}\,e^{-c}}{\sum_j e^{z_j}\,e^{-c}} = \mathrm{softmax}(z)_i$')],
                  symbols=[['z (logits)', 'Three large scores. The naive way: e^1000 is inf, and inf / inf is nan.', '(1000, 1001, 1002): nan, nan, nan'],
                           ['c = the maximum', 'Any c cancels top and bottom. With the maximum every exponent is 0 or less.', 'z - 1002 = -2, -1, 0'],
                           ['e^(z minus c) and sum', 'Each is at most 1, so nothing overflows; the largest is exactly 1, so the sum is at least 1.', f'{np.exp(-2):.4f} + {np.exp(-1):.4f} + 1 = {np.exp(-2) + np.exp(-1) + 1:.4f}'],
                           ['Result', 'Divide each by the sum. It equals softmax(0, 1, 2): only differences matter.', f'{sb[0]:.4f}, {sb[1]:.4f}, {sb[2]:.4f}']],
                  size=22, widths=[2.3, 6.0, 3.6],
                  notes=('Softmax on the scores one thousand, one thousand and one, and one thousand and two. The naive way exponentiates each score, every one overflows to infinity, and infinity over infinity is nan. '
                         'Now subtract any constant c from every score. The factor e to the minus c appears in the top and in every term of the bottom, so it cancels, and the answer is unchanged. Choose c to be the maximum. '
                         f'The shifted scores are minus two, minus one and zero, their exponentials add up to {np.exp(-2) + np.exp(-1) + 1:.4f}, and the probabilities are {sb[0]:.4f}, {sb[1]:.4f} and {sb[2]:.4f}. Every library computes softmax this way.')))

    S.append(dict(kind='formula', title='Log-sum-exp computes the log of a sum of exponentials without overflow',
                  formulas=[('Log-sum-exp', r'$\mathrm{LSE}(z) = \ln\sum_j e^{z_j} = m + \ln\sum_j e^{z_j - m}, \quad m = \max_j z_j$'),
                            ('Log-softmax', r'$\ln \mathrm{softmax}(z)_i = z_i - \mathrm{LSE}(z)$')],
                  symbols=[['m', 'The maximum of the scores. The shift keeps every exponent at most 0.', '1002'],
                           ['LSE(z)', 'The log-sum-exp, in nats (natural log).', f'1002 + ln(1.5032) = {lse:.4f}'],
                           ['ln softmax', 'The log of each probability, computed directly without ever forming the probability.', f'{1000 - lse:.4f}, {1001 - lse:.4f}, {1002 - lse:.4f}']],
                  size=22, widths=[1.9, 6.3, 3.7], note='Session 1 added logs in place of multiplying probabilities. Session 17 computes cross-entropy from log-softmax.',
                  notes=('A closely related trick is log-sum-exp. We often need the natural log of a sum of exponentials. Written naively it overflows. Pull out the maximum m and it becomes m plus the log of the sum of e to the z minus m, which is safe. '
                         f'For our scores, m is one thousand and two, the shifted sum is one point five zero three two, and the result is {lse:.4f}. '
                         f'The log of each softmax probability is then z minus that number: {1000 - lse:.4f}, {1001 - lse:.4f} and {1002 - lse:.4f}. In Session 17 cross-entropy is computed from exactly this quantity.')))

    S.append(dict(kind='wide', title='A product of many probabilities underflows to zero, but the sum of their logs does not',
                  visual=dict(kind='d_longprod'),
                  caption=f'Tokens of probability 0.1. The product is 0 from n = 324; the sum of logs at n = 400 is {400 * np.log(0.1):.2f}.',
                  notes=('Underflow is the opposite problem. Suppose every token in an answer had probability point one. The probability of the whole sequence is the product, point one to the power n, and the red line shows its logarithm falling in a straight line. '
                         'Float sixty-four cannot store a number below about five times ten to the minus three hundred and twenty-four, the dashed line. Near that limit it keeps fewer and fewer digits, and from three hundred and twenty-four tokens the stored product is exactly zero. '
                         'The sum of the logs is n times the natural log of point one, minus two point three zero two six each. At four hundred tokens that is about minus nine hundred and twenty-one, an ordinary number. So keep the sum of logs, as Session 1 did.')))

    S.append(dict(kind='idea', title='Vanishing and exploding gradients: a product of many factors heads to 0 or to infinity',
                  visual=dict(kind='d_vanish'),
                  lead='The backward pass multiplies one factor per layer.',
                  points=['Factor 0.25, the largest sigmoid slope (Session 11): 0.25^10 is about 0.00000095. Vanishing.',
                          'Factor 1.8: 1.8^10 is about 357. Exploding.',
                          'Fixes: ReLU, normalisation, residual connections, clipping.'],
                  notes=('The same repeated multiplication happens in the backward pass. Each layer multiplies the gradient by a factor. A factor of a quarter, the largest slope the sigmoid can have, leaves about one millionth after ten layers, and that is the best case: real sigmoid slopes are below a quarter, so the gradient shrinks even faster. That is vanishing. '
                         'A factor of one point eight grows to about three hundred and fifty-seven after ten layers and keeps growing. That is exploding. The vertical axis is a power of ten. '
                         'Published fixes include ReLU units, which have slope one for positive inputs, normalisation layers, and residual connections that let the gradient skip layers.')))

    S.append(dict(kind='formula', title='Clipping a gradient limits its length when it explodes',
                  formulas=[('Clip by norm', r'$g \leftarrow g\cdot\frac{c}{\Vert g\Vert_2} \quad \text{if } \Vert g\Vert_2 > c$')],
                  symbols=[['g', 'The gradient: the column of all the slopes.', 'g = (30, 40)'],
                           ['norm of g', 'The L2 norm (Session 2): the length of the vector.', 'sqrt(900 + 1600) = 50'],
                           ['c', 'The largest length we allow, chosen by us.', 'c = 5'],
                           ['New g', 'Multiply g by c / norm = 5 / 50 = 0.1. The direction stays the same.', '(3, 4), length 5']],
                  size=26, note='Clipping changes the length of the step but not its direction. Gradient clipping is common in published training recipes.',
                  notes=('A simple guard against exploding gradients is clipping. If the length of the gradient, its L2 norm, is more than a limit c, multiply the gradient by c divided by its length. '
                         'Take a gradient of thirty comma forty. Its length is fifty. With a limit of five we multiply by five over fifty, which is point one, and get three comma four, which has length exactly five. '
                         'The direction is unchanged, only the step is shorter. Published training recipes often use it together with the learning-rate schedule from Session 10.')))

    S.append(dict(kind='table', title='Four practical slips, from lambda to logs, and how to spot each one',
                  headers=['Mistake', 'What you see', 'Fix'],
                  rows=[['Pick lambda by the training error', 'The best lambda is always 0', 'Pick lambda by the error on validation points'],
                        ['Choose lambda and report the error on the same points', 'A reported error that new data will not match', 'Keep test points apart and report their error once'],
                        ['Exponentiate large scores directly', 'inf or nan in the softmax', 'Subtract the maximum first, or use log-softmax'],
                        ['Multiply many probabilities', 'The result is 0 for long sequences', 'Add log-probabilities instead']],
                  widths=[4.1, 3.9, 3.9], icons=False,
                  notes=('Choosing lambda by the training error always prefers lambda zero, because the training error only rises with lambda, so choose it on validation points. '
                         'Choosing on some points and reporting the error on the same points flatters the model; keep test points apart and look at them once. '
                         'Exponentiating large scores directly gives infinity or nan, fixed by subtracting the maximum. And multiplying many probabilities underflows to zero, fixed by adding logs. The first two belong to Part A, the last two to Part B.')))

    S.append(dict(kind='code', title='Read the stable softmax before you write it',
                  code='z = np.array([1000., 1001., 1002.])\nm = z.max()\ne = np.exp(z - m)\nprobs = e / e.sum()\nlse = m + np.log(e.sum())\nlogprobs = z - lse',
                  reads=['m is the largest score. z - m is at most 0.', 'Every entry of e is at most 1, so it cannot overflow.', 'probs adds up to 1 and equals softmax(0, 1, 2).', 'lse is the log-sum-exp. logprobs are the log of each probability, with no probability formed.'],
                  notes=('The stable softmax takes six lines. M is the largest score, so z minus m is at most zero. E is the vector of exponentials of those shifted scores, all at most one. '
                         'Probs divides by the sum, and adds up to one. Then lse is m plus the log of the sum, and log probs is z minus lse, which gives the log of each probability without ever forming the probabilities. '
                         'In the lab you will first break the naive version on purpose and then write this one.')))

    S.append(dict(kind='divider', title='Part 2: the lab', lead='Close the slides. Open the notebook or the workbook.', section='Lab',
                  notes=('That is the end of the concepts. Please close the slides and open the Python notebook or the spreadsheet workbook. Both hold the same numbers as the slides. '
                         'You will break a softmax on purpose, fix it, and then fit a curve with a ridge penalty for several values of lambda. For each step, write your prediction first, then run, then read, then change one thing.')))

    S.append(dict(kind='steps', title='Five lab steps: break a softmax, fix it, then fit and test a ridge curve',
                  steps=[dict(head='1 Overflow', text='Break the naive softmax on purpose', icon='bell'), dict(head='2 Fix it', text='Subtract the maximum, then log-sum-exp', icon='check'),
                         dict(head='3 Formats', text='float16 limits and a long product', icon='calculator'), dict(head='4 Ridge', text='Closed form, lambda on validation, test once', icon='chart'),
                         dict(head='5 Decay', text='Weight decay, a weight limit, clipping', icon='flag')], highlight=1,
                  caption='The notebook has the same five steps; the workbook uses the sheets Softmax, Formats, Ridge and Small. Predict, run, read, change one thing.',
                  notes=('The lab has five steps. One, break the naive softmax with scores of one thousand and see the nan. Two, fix it by subtracting the maximum, and compute the log-sum-exp. Three, meet the limits of float sixteen and a long product that underflows. '
                         'Four, fit the degree nine curve with the closed-form ridge solution, choose lambda on the validation points, and only then compute the test error. Five, take a weight-decay step, find the best point on a line, and clip a gradient. In the spreadsheet, the ridge uses MMULT and MINVERSE.')))

    S.append(dict(kind='table', title='The numbers your lab should reach, from the softmax to the test error',
                  headers=['What you compute', 'You should see'],
                  rows=[['Stable softmax of (1000, 1001, 1002)', f'{sb[0]:.4f}, {sb[1]:.4f}, {sb[2]:.4f}'], ['Log-sum-exp of (1000, 1001, 1002)', f'{lse:.4f}'], ['Largest float16 number', '65504'],
                        ['Sum of squared weights, lambda = 0.1', f'{r3["norm2"]:.4f}'], ['Validation error, lambda = 0 and 0.1', f'{r0["rmse_te"]:.4f} and {r3["rmse_te"]:.4f}'],
                        [f'Test error, once, at the chosen lambda = {lam_b:g}', f'{rt:.4f}'], ['Weight after one step with decay (w = 2)', '1.7']],
                  widths=[6.2, 5.6], icons=False,
                  note='If your number differs, find the step that went wrong. Do not change a number to match.',
                  notes=(f'The stable softmax should give point zero nine zero zero, point two four four seven and point six six five two, and the log-sum-exp is one thousand two point four zero seven six. The largest float sixteen number is sixty-five thousand five hundred and four. '
                         f'For ridge at lambda point one, the sum of squared weights is {r3["norm2"]:.4f}, and the validation error is {r3["rmse_te"]:.4f}, against {r0["rmse_te"]:.4f} with no penalty. The test error, computed once at the end, is {rt:.4f}. '
                         'Every later step builds on the earlier ones, so stop at the first number that differs and fix it there.')))

    S.append(dict(kind='table', title='Warnings and errors in this lab, and which of them are on purpose',
                  headers=['What you see', 'What it means', 'What to do'],
                  rows=[['RuntimeWarning: overflow in exp, and nan', 'The naive softmax overflowed. This is expected in step 1', 'Continue to step 2 and subtract the maximum'],
                        ['Huge or jumpy weights at lambda = 0', 'X^T X is badly conditioned, so the answer is unreliable', 'Use lambda > 0 in the closed form'],
                        ['Weights look huge', 'lambda is too small', 'Raise lambda and compare the norm'],
                        ['#NUM! in a sheet', 'EXP of a large number overflowed', 'Subtract the maximum first']],
                  widths=[4.0, 3.9, 4.0], icons=False,
                  notes=('A runtime warning about overflow, and nan, is expected in step one, because we break the softmax on purpose. Huge or jumpy weights at lambda zero mean the matrix is badly conditioned, so the answer is unreliable. Numpy raises a singular-matrix error only if the matrix is exactly singular. '
                         'Huge weights at other values mean lambda is too small. And in the spreadsheet, a number error means EXP got a large number, so subtract the maximum first.')))

    S.append(dict(kind='idea', title='Where this appears in AI: how overfitting is watched and controlled',
                  visual=dict(kind='d_loop', items=['Update the weights, with weight decay', 'Measure the loss on text held out from training', 'Compare it with the training loss', 'Gap growing? Penalise more or stop earlier', 'Next batch of text'], center='monitoring overfitting', highlight=3),
                  lead='The loss on held-out text tells us whether the model memorises.',
                  points=['Published work describes weight decay, dropout (randomly switching off units while training) and early stopping (stop when the held-out loss rises).', 'Closed products do not publish their settings.'],
                  notes=('This is how overfitting is controlled in the training of large models, as described in published work. After updates, the loss is measured on text that was held out from training. If the training loss keeps falling but the held-out loss stops falling or rises, the model is starting to memorise. '
                         'Published remedies include weight decay, which is today\'s penalty applied inside the optimiser, dropout, which switches off random units during training, and early stopping. The makers of ChatGPT, Gemini and Claude have not published their exact settings.')))

    S.append(dict(kind='steps', title='Where this appears in AI: why a very long answer does not overflow',
                  steps=[dict(head='Logits', text='One raw score per candidate next token', icon='chart'), dict(head='Subtract max', text='Every exponent is at most 0', icon='key'), dict(head='Exponentiate', text='Values between 0 and 1', icon='gear'),
                         dict(head='Normalise', text='Divide by the sum: probabilities', icon='calculator'), dict(head='Add logs', text='Sequence score = sum of log-probabilities', icon='check')], highlight=1,
                  caption='Published practice for models of this kind: softmax computed in a stable way, and sequence scores kept as sums of logs.',
                  notes=('At every position the model produces a score for each candidate next token, the logits. The softmax turns them into probabilities, and a stable implementation subtracts the maximum first, so nothing overflows. '
                         'The score of a whole sequence is kept as a sum of log-probabilities, never as a product, so a thousand tokens do not underflow to zero. The same stable softmax sits inside the attention step of the published transformer design, which Session 18 builds. '
                         'This describes published practice; the internal code of closed products is not public.')))

    S.append(dict(kind='practice', title='Check an AI assistant with your own numbers', minutes=10, label='Hands-on, with no private data',
                  task='Ask any AI assistant to compute a softmax that overflows. Then compare with your table.',
                  steps=['Type: "Compute softmax of the scores 1000, 1001 and 1002 without overflow. Show every step."', f'Expected result: {sb[0]:.4f}, {sb[1]:.4f}, {sb[2]:.4f}.', 'Did it subtract the maximum? If its answer differs, find the first number that differs from yours.', 'Never paste confidential data.'],
                  output='A note: did the assistant match your table?',
                  notes=('Ask any assistant to compute the softmax of one thousand, one thousand and one, and one thousand and two, without overflow, and to show every step. '
                         f'The result should be {sb[0]:.4f}, {sb[1]:.4f} and {sb[2]:.4f}. Look at whether it subtracts the maximum, and find the first number that differs from your table. '
                         'Assistants sometimes slip on arithmetic, so use the assistant to explain and your own calculation to check. Please never paste confidential data into an assistant.')))

    S.append(dict(kind='table', title='Exit check: three questions with short answers',
                  headers=['Question', 'Short answer'],
                  rows=[['What does the L2 penalty do to the weights, and which points choose lambda?', 'It shrinks the weights towards zero. Validation points choose lambda; test points are used once, afterwards.'],
                        ['Why does subtracting the maximum not change the softmax?', 'The factor e^(-c) appears in the top and in every term of the bottom, so it cancels. It only keeps the exponents at most 0.'],
                        ['Why are log-probabilities added instead of probabilities multiplied?', 'A product of many probabilities underflows to 0. The sum of their logs is an ordinary number.']],
                  widths=[5.2, 6.8], icons=False,
                  notes=('First, the L2 penalty shrinks the weights towards zero, lambda is chosen on validation points, and the test points are used once at the end. '
                         'Second, subtracting the maximum does not change the softmax because the factor e to the minus c appears in the top and in every term of the bottom, so it cancels. It only keeps the exponents at or below zero. '
                         'Third, we add log-probabilities because a product of many probabilities underflows to zero, while the sum of the logs is an ordinary number. Write your own answers first.')))

    s['facilitator'] = dict(
        prep=['Run the notebook and the workbook once. Check that the stable softmax gives 0.0900, 0.2447, 0.6652 and that the ridge table matches the slide.',
              'Warn learners that the naive softmax cell prints RuntimeWarning and nan on purpose in step 1.',
              'Have a calculator ready for the by-hand ridge (28.5 / 14 and 28.5 / 15) and the softmax of (2, 1, 0.1).'],
        misconceptions=[('A larger lambda always gives a better model', 'It lowers the training fit. The validation error falls and then rises again; lambda 0.1 is best of the six on our data.'),
                        ('The error used to choose lambda is a fair estimate for new data', f'It flatters the model. Here validation gives {r3["rmse_te"]:.3f} but the untouched test points give {rt:.3f}.'),
                        ('Subtracting the maximum changes the probabilities', 'The probabilities are identical. Only the intermediate numbers are smaller.'),
                        ('16-bit numbers are just a little less accurate', 'They also have a much smaller range (float16 stops at 65,504), which is why scaling and 32-bit copies are used.')],
        probes=[('If the training error is zero, is the model good?', 'No. On our data the unpenalised curve has zero training error and the largest validation error (0.67).'),
                ('Why does subtracting the maximum also stop underflow of the whole sum?', 'The largest entry becomes e^0 = 1, so the sum is at least 1.'),
                ('What does a vanishing gradient mean for the early layers?', 'Their updates are almost zero, so they barely learn.'),
                ('How is weight decay different from clipping?', 'Weight decay shrinks the weights at every step. Clipping limits the length of the gradient only when it is too long.')],
        lab_steps=[('Python: overflow and the stable softmax (steps 1 and 2)', 'Naive softmax gives nan with a warning. Stable result 0.0900, 0.2447, 0.6652. Spreadsheet: the naive column shows "overflow", the gold cells fill the stable column.'),
                   ('Python: float formats (step 3)', 'float16 max is 65504; 400 tokens give a product of 0 but a log sum of -921.03.'),
                   ('Python: ridge (step 4)', f'Sum of squared weights {r3["norm2"]:.4f} and validation RMSE {r3["rmse_te"]:.4f} at lambda 0.1; test RMSE {rt:.4f}, computed once. Spreadsheet: MINVERSE then MMULT; the 10 × 10 inverse is the gold block.'),
                   ('Python: decay, constraint and clipping (step 5)', 'New w 1.7, lowest loss 2 at w1 = 1, clipped gradient (3, 4). Spreadsheet: the Small sheet has the by-hand weights 2.0357, 1.9, 1.0179 and the same three parts.')],
        rescue=['If the matrix part takes too long, use the by-hand one-weight ridge and show the table of the lambda sweep.', 'If a learner has no Python, do the spreadsheet: it has the same values.',
                'If time runs short, skip the weight-decay, constraint and clipping cells: the stable softmax and the ridge sweep are the core.'],
        after=['Share the solution notebook with absent learners.', 'Ask learners to bring one example of a probability from daily life for Session 13.'],
        lab_answer_key=[['PREDICT: what does the naive softmax of (1000, 1001, 1002) return?', 'nan, nan, nan, because exp overflows to inf and inf / inf is nan.'],
                        ['CHANGE (step 2): shift the scores to 6000', 'The stable softmax does not change: 0.0900, 0.2447, 0.6652.'],
                        ['READ: why does the unpenalised curve have enormous weights?', 'X^T X is badly conditioned, so the solution uses large weights of opposite signs to pass through every point.'],
                        ['CHANGE: use lambda = 10', 'The curve is too stiff: the training and the validation errors both rise (validation 0.4198).'],
                        ['CHANGE: use float16 for exp(12)', 'The result is inf.'], ['CHANGE (step 5): lambda = 2', 'w_new = 0.6 × 2 - 0.1 = 1.1, below 1.7: a stronger shrink.']])
    return s
