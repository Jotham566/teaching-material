"""Session 12: Optimisation in practice. Author D."""
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'kit'))
import diagrams_math_d as D  # noqa: E402


def build():
    n = D.n12()
    R = {r['lam']: r for r in n['rows']}
    r0, r1, r2, r3, r4, r5 = (R[k] for k in (0.0, 0.001, 0.01, 0.1, 1.0, 10.0))
    xg, f = n['xg'], n['f']
    sb, ss, lse = n['soft_big'], n['soft_small'], n['lse_big']

    def panel(lam, title, note):
        return dict(title=title, note=note, x=xg, y=n['curves'][lam], xt=n['xtr'], yt=n['ytr'], xf=xg, yf=f(xg))

    s = dict(
        num=12, block='Calculus and optimisation', short_title='Optimisation in practice',
        title='Optimisation in practice: a penalty against overfitting, and numbers that must not overflow',
        question='How do we limit memorising in a model with billions of numbers, and why does a very long answer not overflow the computer?',
        outcomes=['Fit a curve with a ridge (L2) penalty, and read what the penalty does to the weights and to the error on new points',
                  'Explain a constraint as the best point on a boundary, and weight decay as the same idea written as a penalty',
                  'Compute a softmax and a log-sum-exp without overflow, by subtracting the maximum, and say why vanishing and exploding gradients happen'],
        outcome_icons=['chart', 'key', 'check'],
        outcome_note=('By the end of today you can do three things. Fit a curve with a ridge penalty and see what the penalty does to the weights and to the error on new points. '
                      'Explain a constraint as the best point on a boundary, and weight decay as the same idea written as a penalty. '
                      'And compute a softmax and a log-sum-exp without overflow, by subtracting the maximum. These are the quiet tricks that make training and answering reliable. Which of the three sounds the most surprising to you?'),
        clock=[(10, 'Recall and a real question from AI'), (35, 'Concept: a picture, then a hand example'), (10, 'Break'), (45, 'Lab: Python or spreadsheet, predict, run, change'),
               (15, 'Where it appears in AI, plus an exit check'), (5, 'Save the work')],
        plan_title='Your two hours: a penalty first, then numbers that break',
        plan_caption='Pictures and hand calculations first. Then the lab: numpy, or cells in the spreadsheet.',
        plan_note=('We have two hours. The first ten minutes recall backpropagation and ask the question of the day. Then thirty-five minutes of concepts: the ridge penalty and weight decay, constraints as a best point on a boundary, and then the numerical side: overflow, the stable softmax, log-sum-exp, 16-bit numbers and vanishing gradients. '
                   'After the break, forty-five minutes of lab where you break a softmax on purpose and fix it, and fit a curve with a penalty. The last fifteen minutes show where these ideas appear in large language models.'),
        recall_from='Session 11',
        recall=[('In our tiny network, what is delta(2) and what value did it have?', 'delta(2) is the slope of the loss with respect to the prediction, y-hat - y. It was 0.1733 - 1 = -0.8267.'),
                ('Why does the hidden delta contain a × (1 - a)?', 'a × (1 - a) is the slope of the sigmoid. The chain rule multiplies it into the slope that arrives from the output.'),
                ('Which values from the forward pass does the backward pass reuse?', 'The hidden outputs a(1) and the inputs x, which multiply the deltas to give the gradients. They are stored during the forward pass.')],
        words=[('Regularisation', 'Any change to training that discourages a model from memorising its training data.'),
               ('L2 penalty (ridge)', 'An extra term, lambda times the sum of the squared weights, added to the loss.'),
               ('Weight decay', 'Shrinking every weight a little at each update. For plain gradient descent it is the L2 penalty.'),
               ('Overflow and underflow', 'A result too large or too small for the number format: it becomes inf or 0.'),
               ('Log-sum-exp', 'The number m + ln(sum of e^(z - m)) with m the maximum. It computes ln(sum of e^z) safely.')],
        word_icons=['gear', 'calculator', 'clock', 'bell', 'chart'],
        words_note=('Five words for today. Regularisation is anything that discourages memorising. The L2 penalty, also called ridge, adds lambda times the sum of squared weights to the loss. '
                    'Weight decay shrinks every weight a little at each update, and for plain gradient descent it is the same thing as the L2 penalty. Overflow and underflow mean a result too large or too small for the number format, so the computer shows infinity or zero. '
                    'And log-sum-exp is the safe way to compute the log of a sum of exponentials. We use each of them before the break.'),
        keep='Keep your saved notebook or workbook, with the ridge fit for several values of lambda and the stable softmax. Write down the one-line rule: subtract the maximum before you exponentiate.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Penalty', value='lambda × sum of w^2'), dict(label='Best lambda here', value='0.1 (test error %.3f)' % r3['rmse_te']),
                                                              dict(label='Stable softmax', value='subtract the maximum'), dict(label='Next session', value='Probability basics')]),
        keep_title='Save your lab and keep the two rules',
        next='Session 13: probability basics: random variables, expectation and variance.', next_label='Next session',
        keep_note=('Before you go, save your notebook or workbook. Keep the ridge fit for the different values of lambda, and the stable softmax. Keep one rule in your head: subtract the maximum before you exponentiate. '
                   'Next session starts a new block, probability. Everything you built today comes back there, because softmax turns scores into probabilities. Bring any question about the penalty today.'),
        cover_note=('Welcome to Session 12. So far we found gradients and took steps along them. Today we ask what goes wrong in practice. '
                    'A model with enough numbers can memorise its training data, and a penalty on the weights controls that. And a perfectly correct formula can overflow on a computer, which the stable softmax fixes. '
                    'Both ideas are inside every large language model.'),
        slides=[])
    S = s['slides']

    S.append(dict(kind='table', title='Answers to the three questions from Session 11', headers=['Question', 'Short answer'], rows=[[q, a] for q, a in s['recall']], widths=[5.6, 6.4], icons=False,
                  note='Check your answers. If one surprised you, look at Session 11 before the lab.',
                  notes=('Here are the short answers. Delta two, written delta in brackets two, is the slope of the loss with respect to the prediction. It equals the prediction minus the target, and in our network it was minus point eight two six seven. '
                         'The hidden delta contains a times one minus a because that is the slope of the sigmoid, and the chain rule multiplies it into the slope arriving from the output. '
                         'And the backward pass reuses the hidden outputs and the inputs, which are stored during the forward pass. Today we look at what can go wrong with the numbers in those passes.')))

    S.append(dict(kind='wide', title='Overfitting in one picture: a curve with too much freedom chases the noise',
                  visual=dict(kind='d_ridge', panels=[panel(0.0, 'No penalty (lambda = 0)', 'Swings between the points'),
                                                     panel(0.1, 'Small penalty (lambda = 0.1)', 'Smooth and close to truth'),
                                                     panel(10.0, 'Large penalty (lambda = 10)', 'Too stiff: misses the pattern')]),
                  caption='Dots: 10 training points. Dashed: true curve. Red: degree 9 fit, with its penalty above. Illustrative data.',
                  notes=('Here are ten training points, drawn as black dots, from a curve with a little noise. The dashed line is the true curve. We fit a polynomial of degree nine, which has ten weights, one for each point. '
                         'On the left there is no penalty, and the red curve passes through every dot, but between the dots it swings wildly. That is overfitting: the model has memorised the noise. '
                         'In the middle a small penalty gives a smooth curve close to the truth. On the right a large penalty makes the curve too stiff. Which panel would you trust for a new point?')))

    S.append(dict(kind='formula', title='The L2 (ridge) penalty adds the size of the weights to the loss',
                  formulas=[('Ridge loss (sum of squared errors plus penalty)', r'$L(w) = \sum_{i=1}^{n}(\hat{y}_i - y_i)^2 + \lambda\sum_{j=1}^{d} w_j^2$'),
                            ('Prediction', r'$\hat{y} = w_0 + w_1 x + w_2 x^2 + \dots + w_9 x^9$')],
                  symbols=[['lambda', 'The penalty strength, chosen by us. Larger means smaller weights.', '0, 0.001, 0.01, 0.1, 1, 10'],
                           ['sum of w^2', 'The squared L2 norm of the weights (Session 2), without w_0.', 'about 104,000 at lambda = 0, 1.55 at 0.1'],
                           ['n, d', 'Number of training points; number of penalised weights.', 'n = 10, d = 9'],
                           ['y-hat', 'The prediction of the polynomial for a value x.', 'one number per point']],
                  size=20, widths=[1.9, 6.1, 3.9], note='First term: fit the data. Second term: keep the weights small. Lambda sets the balance. There is no division by n.',
                  notes=('The ridge loss has two terms. The first is the sum of the squared errors on the training points, with no division by n, and every number today uses that form: fit the training points. The second is lambda times the sum of the squared weights, which is the squared L2 norm from Session 2. '
                         'It says: keep the weights small. Lambda is a number we choose, and it sets the balance. With lambda zero we fit the data and ignore the weights. With a large lambda the weights are squeezed towards zero. '
                         'The intercept w zero is usually left out of the penalty, so that the whole curve can still shift up or down. Why would small weights give a smoother curve?')))

    S.append(dict(kind='table', title='By hand: one weight, three points, and what lambda does to it',
                  headers=['lambda', 'Formula: w = sum(x y) / (sum(x^2) + lambda)', 'Weight w', 'Share of the plain fit'],
                  rows=[['0', '28.5 / 14', f'{28.5 / 14:.4f}', '100%'], ['1', '28.5 / 15', f'{28.5 / 15:.4f}', f'{100 * 14 / 15:.0f}%'], ['14', '28.5 / 28', f'{28.5 / 28:.4f}', '50%'], ['140', '28.5 / 154', f'{28.5 / 154:.4f}', f'{100 * 14 / 154:.0f}%']],
                  widths=[1.4, 5.4, 2.4, 2.8], icons=False,
                  note='Data (illustrative): x = 1, 2, 3 and y = 2.1, 3.9, 6.2, so sum(x y) = 2.1 + 7.8 + 18.6 = 28.5 and sum(x^2) = 1 + 4 + 9 = 14. Model: y-hat = w x.',
                  notes=('A hand example with one weight. Three points: x is one, two, three, and y is two point one, three point nine, six point two. The sum of x times y is twenty-eight point five, and the sum of x squared is fourteen. '
                         'With lambda zero the best weight is twenty-eight point five over fourteen, which is two point zero three six. With lambda one the denominator grows to fifteen and the weight shrinks to one point nine. '
                         'When lambda equals fourteen the weight is exactly halved, and with lambda one hundred forty it is almost zero. So the penalty shrinks the weight smoothly towards zero. How would you pick the value of lambda?')))

    S.append(dict(kind='formula', title='Ridge has a closed-form answer: add lambda to the diagonal, then solve',
                  formulas=[('Closed form', r'$w = \left(X^{T}X + \lambda P\right)^{-1} X^{T} y$'),
                            ('Without penalty', r'$w = \left(X^{T}X\right)^{-1} X^{T} y \qquad (\lambda = 0)$')],
                  symbols=[['X', 'The design matrix: one row per training point, columns 1, x, x^2, ..., x^9.', '10 × 10 here'],
                           ['X^T X', 'A square matrix built from X (the normal equation of Session 4).', '10 × 10'],
                           ['lambda P', 'Lambda times P, added to the diagonal. P is the identity matrix with its first entry 0, so w_0 is not penalised.', 'lambda = 0.1'],
                           ['(...)^-1', 'The inverse (Session 4). At lambda = 0 it exists here but is badly conditioned, so the answer is unreliable.', 'MINVERSE in the sheet']],
                  size=24, widths=[1.9, 6.4, 3.6], note='In practice a solver is used instead of an explicit inverse. The formula shows what is computed.',
                  notes=('The ridge problem has a closed-form answer, and it is the normal equation from Session 4 with one change: add lambda times a matrix P to X transpose X, where P is the identity matrix with its first entry set to zero. '
                         'That adds lambda to the diagonal. Here X has one row per training point and one column for each power of x, so with ten points and degree nine it is a ten by ten matrix. '
                         'Without the penalty, that matrix can still be inverted, but it is badly conditioned, so tiny changes in the data give huge changes in the weights. That is why the unpenalised weights are so large. Adding lambda makes the inverse well behaved. In practice we use a solver rather than an explicit inverse, but the formula shows what is computed.')))

    rows = [[f'{r["lam"]:g}', f'{r["norm2"]:.4f}' if r['norm2'] < 1000 else f'{r["norm2"]:,.0f}', f'{r["rmse_tr"]:.4f}', f'{r["rmse_te"]:.4f}'] for r in n['rows']]
    S.append(dict(kind='table', title='Ridge on our ten points: the weights shrink, and the error on new points is lowest at lambda = 0.1',
                  headers=['lambda', 'Sum of the squared weights', 'Training error (RMSE)', 'Error on 20 new points (RMSE)'], rows=rows, widths=[1.6, 3.9, 3.2, 3.5], icons=False,
                  note='RMSE is the root of the mean squared error, in the units of y. The 20 new points are held out: they are never used to fit. Illustrative data.',
                  notes=(f'Here are the numbers behind the picture. Look at the second column: the sum of squared weights falls from about {r0["norm2"]:,.0f} with no penalty to {r3["norm2"]:.2f} at lambda point one, and {r5["norm2"]:.2f} at lambda ten. '
                         f'The training error rises as lambda grows, from zero to {r5["rmse_tr"]:.2f}, because the curve fits the training points less closely. But the error on the twenty new points is {r0["rmse_te"]:.2f} with no penalty and falls to {r3["rmse_te"]:.3f} at lambda point one, then rises again. '
                         'So the best lambda is the one with the lowest error on held-out points, here point one. A penalty trades a little training accuracy for much better behaviour on new data.')))

    S.append(dict(kind='formula', title='Weight decay: every update first shrinks the weights by a small factor',
                  formulas=[('L2 penalty in the update', r'$w \leftarrow w - \eta\left(\frac{\partial L}{\partial w} + 2\lambda w\right)$'),
                            ('Weight decay form', r'$w \leftarrow (1 - 2\eta\lambda)\,w - \eta\,\frac{\partial L}{\partial w}$')],
                  symbols=[['eta', 'The learning rate (Session 10).', 'eta = 0.1'],
                           ['dL/dw', 'The slope of the loss without the penalty.', 'illustrative: 1'],
                           ['lambda', 'The penalty strength. Many libraries define a single decay number equal to 2 times lambda.', 'lambda = 0.5'],
                           ['1 - 2 eta lambda', 'The shrink factor applied to w before the gradient step.', '1 - 2 × 0.1 × 0.5 = 0.9']],
                  size=18, widths=[2.2, 5.6, 4.1], note='Worked: w = 2 gives 0.9 × 2 - 0.1 × 1 = 1.7. AdamW (Loshchilov and Hutter, 2017) shrinks in a separate step.',
                  notes=('The penalty has a simple effect on the update rule. The derivative of lambda times w squared is two lambda w, so each step subtracts eta times the usual gradient plus two lambda w. '
                         'Collect the w terms and you get the second line: first multiply w by a number slightly below one, then take the usual gradient step. That is why it is called weight decay: every update shrinks the weights a little. '
                         'With eta point one, lambda point five, w equal to two and a gradient of one, the new weight is one point seven. Published work on Adam applies this shrinking separately from the Adam step, and that variant is called AdamW.')))

    S.append(dict(kind='idea', title='A constraint in plain words: the best point on a boundary',
                  visual=dict(kind='d_lagrange', which='line'),
                  lead='We want the lowest loss, but we must stay on the red line.',
                  points=['Grey rings: points with the same loss w1^2 + w2^2. The loss grows as the rings grow.',
                          'The best allowed point is where a ring just touches the line: (1, 1). The loss there is 2.'],
                  notes=('Now a different idea, constraints. Suppose we want the lowest loss, w one squared plus w two squared, but the two weights must add up to two. That is the red line. '
                         'The grey rings are points with the same loss, and the loss grows as the rings grow. Walk along the red line and you cross rings. The best allowed point is where the line just touches a ring, here at one comma one. '
                         'At that point the ring and the line have the same direction, and that is the whole idea behind the method of Lagrange multipliers. We will not do the full derivation. What would you see if the line crossed the ring instead of touching it?')))

    S.append(dict(kind='table', title='Check it by hand: walk along the line w1 + w2 = 2 and compute the loss',
                  headers=['w1', 'w2 = 2 - w1', 'Loss w1^2 + w2^2', 'Calculation'],
                  rows=[['0', '2', '4', '0 + 4'], ['0.5', '1.5', '2.5', '0.25 + 2.25'], ['1', '1', '2', '1 + 1  (the lowest)'], ['1.5', '0.5', '2.5', '2.25 + 0.25'], ['2', '0', '4', '4 + 0']],
                  widths=[1.8, 3.0, 3.2, 3.9], icons=False,
                  note='At the best point the gradient of the loss, (2 w1, 2 w2) = (2, 2), points in the same direction as the gradient of the constraint w1 + w2, which is (1, 1) (Session 8).',
                  notes=('Check it by hand. Take points on the line: w one is zero, then w two is two, and the loss is four. At half and one and a half the loss is two point five. At one and one it is two, the lowest. '
                         'Then it climbs back to two point five and four. At the best point the gradient of the loss is two comma two, and the gradient of the constraint, w one plus w two, is one comma one. They point in the same direction. '
                         'That is the Lagrange condition: at the best point on the boundary, the two gradients are parallel. The number that scales one into the other is called the Lagrange multiplier, here equal to two.')))

    S.append(dict(kind='idea', title='A constraint on the size of the weights: the same idea as a penalty',
                  visual=dict(kind='d_lagrange', which='disc'),
                  lead='Ridge can be read as: find the best weights inside a circle.',
                  points=['The best fit with no limit lies outside the circle.', 'The best allowed point is on the circle, where a loss ring just touches it.',
                          'A larger lambda means a smaller circle.'],
                  notes=('Here is how constraints connect to ridge. Imagine we ask for the best weights, but only inside a circle: the sum of squared weights must not exceed a limit. '
                         'The best fit with no limit lies outside the circle, so the best allowed point sits on the circle, where a ring of equal loss just touches it. That is exactly the picture from the last slide. '
                         'The penalty form and the circle form describe the same trade, and a larger lambda corresponds to a smaller circle. The equivalence is standard in statistics texts. So a constraint and a penalty are two ways to say: keep the weights small.')))

    S.append(dict(kind='statement', title='A correct formula can still give nonsense on a computer',
                  lead='A computer stores each number in a fixed number of bits. Too large becomes inf, too small becomes 0, and inf / inf is nan (not a number).',
                  notes=('Now the second half of today. Everything so far was mathematics. But a computer stores each number with a fixed number of bits. A result that is too large for the format becomes infinity, and a result that is too small becomes zero. '
                         'Infinity divided by infinity is not a number, which the computer writes as nan. So a formula that is correct on paper can fail in a program. The fixes are small algebra tricks, and every library uses them. Have you ever seen nan in a notebook output?')))

    S.append(dict(kind='idea', title='Number formats: the bits set the range and the number of digits',
                  visual=dict(kind='d_precision'),
                  lead='Fewer bits mean a smaller range and fewer digits.',
                  points=['The exponent bits set how large or small a number can be. The mantissa bits set how many digits it keeps.', 'bfloat16 keeps the range of float32 with fewer digits. float16 has a small range: nothing above 65,504.'],
                  notes=('Each number is stored as a sign, an exponent and a mantissa. The exponent sets the range, how large or small the number can be. The mantissa sets how many digits are kept. '
                         'The common format float sixty-four has about sixteen digits and a largest value near ten to the three hundred and eight. Float thirty-two has about seven digits and a largest value near three times ten to the thirty-eight. '
                         'Float sixteen has about three digits, and its largest value is only sixty-five thousand five hundred and four. Bfloat sixteen keeps the range of float thirty-two but only two to three digits. These facts decide what can go wrong.')))

    S.append(dict(kind='table', title='The exponential overflows quickly: e^z in three formats',
                  headers=['Format', 'Largest value', 'e^z is fine at', 'e^z is inf at'],
                  rows=[['float64 (numpy default)', 'about 1.8e308', 'z = 709: 8.2e307', 'z = 710'], ['float32', 'about 3.4e38', 'z = 88: 1.65e38', 'z = 89'], ['float16', '65,504', 'z = 11: about 59,874', 'z = 12: 162,755 is too large']],
                  widths=[3.3, 2.5, 3.3, 3.3], icons=False,
                  note='Logits (the raw scores of a model) of 100 or more are rare but possible, and a sum of exponentials is even larger than one exponential.',
                  notes=('How soon does the exponential overflow? In float sixty-four, e to the power seven hundred and nine is still fine at about eight times ten to the three hundred and seven, but seven hundred and ten gives infinity. '
                         'In float thirty-two the limit is eighty-eight. In float sixteen it is eleven, because e to the twelve is about a hundred and sixty-three thousand, above the largest float sixteen value. '
                         'So even scores of twelve, which are perfectly ordinary, overflow in float sixteen. And softmax needs the exponential of every score. How can we avoid exponentiating large numbers?')))

    S.append(dict(kind='formula', title='The stable softmax subtracts the maximum, and the answer does not change',
                  formulas=[('Softmax', r'$\mathrm{softmax}(z)_i = \frac{e^{z_i}}{\sum_{j} e^{z_j}}$'),
                            ('Shift by a constant c', r'$\frac{e^{z_i - c}}{\sum_j e^{z_j - c}} = \frac{e^{z_i}\,e^{-c}}{\sum_j e^{z_j}\,e^{-c}} = \mathrm{softmax}(z)_i$')],
                  symbols=[['z', 'The logits (raw scores), one per class or candidate token.', '(1000, 1001, 1002)'],
                           ['c', 'Any constant. The factor e^(-c) cancels top and bottom. Choose c = the maximum score.', 'c = 1002'],
                           ['e^(z - c)', 'At most 1 when c is the maximum: no overflow.', '0.1353, 0.3679, 1']],
                  size=22, widths=[1.7, 6.5, 3.7],
                  notes=('Here is the fix. The softmax of a vector z divides each exponential by the sum of all of them. Now subtract any constant c from every score. The factor e to the minus c appears in the top and in every term of the bottom, so it cancels, and the answer is unchanged. '
                         'Now choose c to be the maximum score. Every exponent is then zero or negative, so every exponential is at most one, and nothing can overflow. The largest entry gives exactly one, so the sum is at least one and cannot underflow to zero either. '
                         'That one line is how every library computes softmax.')))

    S.append(dict(kind='table', title='Softmax of (1000, 1001, 1002): the naive way fails, the stable way works',
                  headers=['Step', 'Naive softmax', 'Stable softmax'],
                  rows=[['Scores z', '1000, 1001, 1002', '1000, 1001, 1002'], ['Shift by the maximum', 'none', 'z - 1002 = -2, -1, 0'], ['Exponentials', 'inf, inf, inf (overflow)', f'{np.exp(-2):.4f}, {np.exp(-1):.4f}, 1'],
                        ['Sum', 'inf', f'{(np.exp(-2) + np.exp(-1) + 1):.4f}'], ['Result', 'inf / inf = nan, nan, nan', f'{sb[0]:.4f}, {sb[1]:.4f}, {sb[2]:.4f}']],
                  widths=[3.2, 4.2, 4.5], icons=False,
                  note=f'The stable result equals softmax(0, 1, 2), because only the differences between scores matter. For small scores both ways agree: softmax(2, 1, 0.1) = {ss[0]:.4f}, {ss[1]:.4f}, {ss[2]:.4f}.',
                  notes=('Here are the two methods on the scores one thousand, one thousand and one, and one thousand and two. The naive way exponentiates each score, and every one overflows to infinity. The sum is infinity, and infinity over infinity is nan. '
                         f'The stable way first subtracts the maximum, one thousand and two, which gives minus two, minus one and zero. The exponentials are {np.exp(-2):.4f}, {np.exp(-1):.4f} and one. They add up to {(np.exp(-2) + np.exp(-1) + 1):.4f}, and the probabilities are {sb[0]:.4f}, {sb[1]:.4f} and {sb[2]:.4f}. '
                         'Notice this equals the softmax of zero, one, two, because only the differences between scores matter. For small scores, the two methods agree.')))

    S.append(dict(kind='formula', title='Log-sum-exp computes the log of a sum of exponentials without overflow',
                  formulas=[('Log-sum-exp', r'$\mathrm{LSE}(z) = \ln\sum_j e^{z_j} = m + \ln\sum_j e^{z_j - m}, \quad m = \max_j z_j$'),
                            ('Log-softmax', r'$\ln \mathrm{softmax}(z)_i = z_i - \mathrm{LSE}(z)$')],
                  symbols=[['m', 'The maximum of the scores. The shift keeps every exponent at most 0.', '1002'],
                           ['LSE(z)', 'The log-sum-exp.', f'1002 + ln(1.5032) = {lse:.4f}'],
                           ['ln softmax', 'The log of each probability, computed directly without ever forming the probability.', f'{1000 - lse:.4f}, {1001 - lse:.4f}, {1002 - lse:.4f}']],
                  size=22, widths=[1.9, 6.3, 3.7], note='Cross-entropy (Session 17) is the negative log-probability of the correct token, so it is computed from log-softmax this way.',
                  notes=('A closely related trick is log-sum-exp. We often need the logarithm of a sum of exponentials. Written naively it overflows. Pull out the maximum m and it becomes m plus the log of the sum of e to the z minus m, which is safe. '
                         f'For our scores, m is one thousand and two, the shifted sum is one point five zero three two, and the result is {lse:.4f}. '
                         f'The log of each softmax probability is then simply z minus that number, here {1000 - lse:.4f}, {1001 - lse:.4f} and {1002 - lse:.4f}. We never form the probability itself. '
                         'In Session 17 we will see that cross-entropy is computed from exactly this quantity.')))

    S.append(dict(kind='wide', title='A product of many probabilities underflows to zero, but the sum of their logs does not',
                  visual=dict(kind='d_longprod'),
                  caption='Each token has probability 0.1, so n tokens give 0.1^n. Float64 stores 0 from n = 324.',
                  notes=('Underflow is the opposite problem. Suppose every token in an answer had probability point one. The probability of the whole sequence is the product, point one to the power n. The red line shows its logarithm, which falls in a straight line. '
                         'But float sixty-four cannot store a number smaller than about five times ten to the minus three hundred and twenty-four, the dashed line. Below the smallest ordinary number, ten to the minus three hundred and eight, it keeps fewer and fewer digits, and from three hundred and twenty-four tokens on the stored product is exactly zero. '
                         'So for a sequence of a few hundred tokens the product becomes zero, and then the logarithm of the product is minus infinity. The fix: never form the product. Add the logarithms instead.')))

    S.append(dict(kind='table', title='Products and sums of logs: the same quantity, one fails and one works',
                  headers=['Number of tokens n', 'Product 0.1^n', 'Sum of logs: n × ln(0.1)'],
                  rows=[['10', '1e-10', f'{10 * np.log(0.1):.3f}'], ['100', '1e-100', f'{100 * np.log(0.1):.2f}'], ['300', '1e-300', f'{300 * np.log(0.1):.2f}'], ['323', f'{0.1 ** 323:g}  (few digits left)', f'{323 * np.log(0.1):.2f}'], ['324', f'{0.1 ** 324:g}  (underflow)', f'{324 * np.log(0.1):.2f}'], ['400', f'{0.1 ** 400:g}  (underflow)', f'{400 * np.log(0.1):.2f}']],
                  widths=[3.4, 4.2, 4.3], icons=False,
                  note='ln(0.1) = -2.3026. The sum of logs is a perfectly ordinary number. The log-probability of a sequence is the sum of the log-probabilities of its tokens.',
                  notes=('The same quantity two ways. The product point one to the n is fine for ten tokens, one in ten billion. It is still fine at three hundred, about ten to the minus three hundred, and stored with few digits at three hundred and twenty-three. From three hundred and twenty-four it underflows to exactly zero. '
                         'The sum of logs is just n times the natural log of point one, which is minus two point three zero two six. At four hundred tokens that is minus nine hundred twenty-one, an ordinary number. '
                         'So the log-probability of a sequence is the sum of the log-probabilities of its tokens, and this is what is used in practice. Which is easier to compare between two answers?')))

    S.append(dict(kind='compare', title='16-bit numbers: a saving that needs care',
                  left=dict(head='The gain', icon='gear', points=['Half the memory of 32-bit numbers', 'Faster arithmetic on suitable hardware', 'Good results in published work']),
                  right=dict(head='The risk', icon='bell', points=['Overflow above 65,504', 'A small update is lost: 1 + 0.0004 is stored as 1.0', 'Remedy: a 32-bit weight copy and loss scaling (Micikevicius et al., 2017)']),
                  verdict='bfloat16 keeps the float32 range.',
                  notes=('Why use sixteen-bit numbers at all? They halve the memory and run faster on hardware designed for them, and published training work reports good results with sixteen-bit arithmetic for most of the operations. '
                         'But the format has a narrow range. Float sixteen overflows above sixty-five thousand five hundred and four, and tiny gradients can round to zero. A small update can also be lost: one plus point zero zero zero four is stored as exactly one. '
                         'The published remedy, from Micikevicius and colleagues in 2017, keeps a thirty-two-bit copy of the weights and scales the loss. Bfloat sixteen avoids most of this trouble by keeping the range. The exact formats of closed products are not published.')))

    S.append(dict(kind='idea', title='Vanishing and exploding gradients: a product of many factors goes to zero or to infinity',
                  visual=dict(kind='d_vanish'),
                  lead='The backward pass multiplies one factor per layer.',
                  points=['Factors below 1 shrink the gradient layer by layer: it vanishes and the early layers stop learning.', 'Factors above 1 grow it: it explodes and the loss becomes nan.'],
                  notes=('Here is the same idea of repeated multiplication, in the backward pass. Each layer multiplies the gradient by a factor. If the factor is below one, say a quarter, the gradient shrinks layer by layer and the early layers barely learn. That is vanishing. '
                         'If the factor is above one, say one point eight, the gradient grows layer by layer, and the numbers eventually overflow. That is exploding. Only when the factors stay near one does the gradient arrive at the early layers at a useful size. '
                         'The vertical axis is a power of ten, so each gridline is a factor of a thousand.')))

    S.append(dict(kind='table', title='The numbers behind the picture: a gradient after k layers, with a factor of 0.25 or 1.8',
                  headers=['Layers k', 'Factor 0.25: 0.25^k', 'Factor 1.8: 1.8^k'],
                  rows=[['1', '0.25', '1.8'], ['3', '0.0156', '5.83'], ['5', '0.00098', '18.9'], ['10', '0.00000095', '357']],
                  widths=[3.0, 4.5, 4.4], icons=False,
                  note='0.25 is the largest slope a × (1 - a) of the sigmoid (Session 11). Each layer\'s factor also contains its weight, so 0.25^10, about one millionth, holds if each weight were 1.',
                  notes=('The numbers for the picture. A factor of a quarter gives a quarter after one layer, about one and a half hundredths after three, about one thousandth after five, and about one millionth after ten layers. '
                         'A factor of one point eight gives about three hundred and fifty-seven after ten. The factor a quarter is not arbitrary: the sigmoid slope a times one minus a is at most one quarter, as you saw in Session 11. '
                         'Published fixes include ReLU units, which have slope one for positive inputs, careful choice of the starting weights, normalisation layers, and residual connections that let the gradient skip layers. Which of these have you heard about before?')))

    S.append(dict(kind='formula', title='Clipping a gradient limits its length when it explodes',
                  formulas=[('Clip by norm', r'$g \leftarrow g\cdot\frac{c}{\Vert g\Vert_2} \quad \text{if } \Vert g\Vert_2 > c$')],
                  symbols=[['g', 'The gradient vector of all the parameters.', 'g = (30, 40)'],
                           ['norm of g', 'The L2 norm (Session 2): the length of the vector.', 'sqrt(900 + 1600) = 50'],
                           ['c', 'The largest length we allow, chosen by us.', 'c = 5'],
                           ['New g', 'Multiply g by c / norm = 5 / 50 = 0.1. The direction stays the same.', '(3, 4), length 5']],
                  size=26, note='Clipping changes the length of the step but not its direction. Gradient clipping is common in published training recipes.',
                  notes=('A simple guard against exploding gradients is clipping. If the length of the gradient, its L2 norm, is more than a limit c, multiply the gradient by c divided by its length. '
                         'Take a gradient of thirty comma forty. Its length is fifty. With a limit of five we multiply by five over fifty, which is point one, and get three comma four, which has length exactly five. '
                         'The direction is unchanged, only the step is shorter. This is common in published training recipes, together with the learning-rate schedule from Session 10.')))

    S.append(dict(kind='table', title='Four mistakes in practice, what you see, and the fix',
                  headers=['Mistake', 'What you see', 'Fix'],
                  rows=[['Exponentiate large scores directly', 'inf or nan in the softmax', 'Subtract the maximum first, or use log-softmax'],
                        ['Pick lambda by the training error', 'The best lambda is always 0', 'Pick lambda by the error on held-out data'],
                        ['Penalise the intercept too', 'The whole curve is pulled towards 0', 'Leave w_0 out of the penalty'],
                        ['Multiply many probabilities', 'The result is 0 for long sequences', 'Add log-probabilities instead']],
                  widths=[4.1, 3.9, 3.9], icons=['cross', 'flag', 'key', 'bell'],
                  notes=('Four mistakes to watch for. Exponentiating large scores directly, which shows up as infinity or nan, fixed by subtracting the maximum. '
                         'Choosing lambda by the training error, which always prefers lambda zero, because the training error only rises with lambda. Choose it by the error on held-out data. '
                         'Penalising the intercept as well, which pulls the whole curve towards zero. And multiplying many probabilities, which underflows to zero, fixed by adding logs. Which of these could you make in your own project?')))

    S.append(dict(kind='code', title='Read the stable softmax before you write it',
                  code='z = np.array([1000., 1001., 1002.])\nm = z.max()\ne = np.exp(z - m)\nprobs = e / e.sum()\nlse = m + np.log(e.sum())\nlogprobs = z - lse',
                  reads=['m is the largest score. z - m is at most 0.', 'Every entry of e is at most 1, so it cannot overflow.', 'probs adds up to 1 and equals softmax(0, 1, 2).', 'lse is the log-sum-exp. logprobs are the log of each probability, with no probability formed.'],
                  notes=('Here is the stable softmax in six lines. M is the largest score, so z minus m is at most zero. E is the vector of exponentials of those shifted scores, all at most one. '
                         'Probs divides by the sum, and adds up to one. Then lse is m plus the log of the sum, and log probs is z minus lse, which gives the log of each probability without ever forming the probabilities. '
                         'In the lab you will first break the naive version on purpose and then write this one.')))

    S.append(dict(kind='divider', title='Part 2: the lab', lead='Close the slides. Open the notebook or the workbook.', section='Lab',
                  notes=('That is the end of the concepts. Please close the slides and open the Python notebook or the spreadsheet workbook. Both hold the same numbers as the slides. '
                         'You will break a softmax on purpose, fix it, and then fit a curve with a ridge penalty for several values of lambda. For each step, write your prediction first, then run, then read, then change one thing.')))

    S.append(dict(kind='steps', title='The lab in five stages, in Python and in the spreadsheet',
                  steps=[dict(head='1 Overflow', text='Break the naive softmax on purpose', icon='bell'), dict(head='2 Fix it', text='Subtract the maximum, then log-sum-exp', icon='check'),
                         dict(head='3 Formats', text='float16 limits and a long product', icon='calculator'), dict(head='4 Ridge', text='Closed form for several lambdas', icon='chart'),
                         dict(head='5 Compare', text='Held-out error, weight decay, a constraint', icon='flag')], highlight=3,
                  caption='Predict first, run, read, then change one thing. The check cells tell you when a number is right.',
                  notes=('Here is the lab in five stages. One, break the naive softmax with scores of one thousand and see the nan. Two, fix it by subtracting the maximum, and compute the log-sum-exp. '
                         'Three, meet the limits of float sixteen and a long product that underflows. Four, fit the degree nine curve with the closed-form ridge solution for several values of lambda. '
                         'Five, compare the errors on held-out points, take a weight-decay step, and find the best point on a boundary. In the spreadsheet, the ridge uses MMULT and MINVERSE. Predict before you run.')))

    S.append(dict(kind='table', title='Check your numbers against these before you move on',
                  headers=['What you compute', 'You should see'],
                  rows=[['Stable softmax of (1000, 1001, 1002)', f'{sb[0]:.4f}, {sb[1]:.4f}, {sb[2]:.4f}'], ['Log-sum-exp of (1000, 1001, 1002)', f'{lse:.4f}'], ['Largest float16 number', '65504'],
                        ['Sum of squared weights, lambda = 0.1', f'{r3["norm2"]:.4f}'], ['Error on the 20 new points, lambda = 0 and 0.1', f'{r0["rmse_te"]:.4f} and {r3["rmse_te"]:.4f}'],
                        ['Weight after one step with decay (w = 2)', '1.7'], ['Best point on the line w1 + w2 = 2', 'w1 = 1 and w2 = 1']],
                  widths=[6.2, 5.6], icons=['pin', 'chart', 'bell', 'gear', 'flag', 'check', 'key'],
                  note='If your number differs, find the step that went wrong. Do not change a number to match.',
                  notes=('Use this table as your checkpoint. The stable softmax should give point zero nine zero zero, point two four four seven and point six six five two. The log-sum-exp is one thousand two point four zero seven six. '
                         f'The largest float sixteen number is sixty-five thousand five hundred and four. For ridge at lambda point one, the sum of squared weights is {r3["norm2"]:.4f}, and the error on the twenty new points is {r3["rmse_te"]:.4f}, against {r0["rmse_te"]:.4f} with no penalty. '
                         'Every later step builds on the earlier ones, so stop at the first number that differs and fix it there.')))

    S.append(dict(kind='table', title='Errors you will meet in the lab, what they mean and what to do',
                  headers=['What you see', 'What it means', 'What to do'],
                  rows=[['RuntimeWarning: overflow in exp, and nan', 'The naive softmax overflowed. This is expected in step 1', 'Continue to step 2 and subtract the maximum'],
                        ['Huge or jumpy weights at lambda = 0', 'lambda is 0: X^T X is badly conditioned and the answer is unreliable (numpy raises LinAlgError only if the matrix is exactly singular)', 'Use lambda > 0 in the closed form'],
                        ['Weights look huge', 'lambda is too small', 'Raise lambda and compare the norm'],
                        ['#NUM! in a sheet', 'EXP of a large number overflowed', 'Subtract the maximum first']],
                  widths=[4.0, 3.9, 4.0], icons=['bell', 'key', 'flag', 'cross'],
                  notes=('Four things you may meet. A runtime warning about overflow, and nan, is expected in step one, because we break the softmax on purpose. Huge or jumpy weights at lambda zero mean the matrix is badly conditioned, so the answer is unreliable. Numpy raises a singular-matrix error only if the matrix is exactly singular. Use lambda above zero in the closed form. '
                         'Huge weights mean lambda is too small. And in the spreadsheet, a number error means EXP got a large number, so subtract the maximum first. Read the last line of any message first.')))

    S.append(dict(kind='idea', title='Where this appears in AI: how overfitting is watched and controlled',
                  visual=dict(kind='d_loop', items=['Update the weights, with weight decay', 'Measure the loss on text held out from training', 'Compare it with the training loss', 'Gap growing? Penalise more or stop earlier', 'Next batch of text'], center='monitoring overfitting', highlight=3),
                  lead='The loss on held-out text is the signal that tells us whether the model memorises.',
                  points=['Published work describes weight decay, dropout and early stopping for models of this kind.', 'The settings used by closed products are not published.'],
                  notes=('Here is how overfitting is controlled in the training of large models, as described in published work. After updates, the loss is measured on text that was held out from training. If the training loss keeps falling but the held-out loss stops falling or rises, the model is starting to memorise. '
                         'Published remedies include weight decay, which is today\'s penalty applied inside the optimiser, dropout, and stopping training earlier. The makers of ChatGPT, Gemini and Claude have not published their exact settings, so we describe only the method. '
                         'It is the same loop as our curve, with the held-out error telling us the right lambda.')))

    S.append(dict(kind='steps', title='Where this appears in AI: why a very long answer does not overflow',
                  steps=[dict(head='Logits', text='One raw score per candidate next token', icon='chart'), dict(head='Subtract max', text='Every exponent is at most 0', icon='key'), dict(head='Exponentiate', text='Values between 0 and 1', icon='gear'),
                         dict(head='Normalise', text='Divide by the sum: probabilities', icon='calculator'), dict(head='Add logs', text='Sequence score = sum of log-probabilities', icon='check')], highlight=1,
                  caption='Published practice for models of this kind: softmax computed in a stable way, and sequence scores kept as sums of logs.',
                  notes=('Why does a very long answer not overflow? At every position the model produces a score for each candidate next token, called logits. The softmax turns them into probabilities, and a stable implementation subtracts the maximum first, so nothing overflows. '
                         'Then the score of a whole sequence is kept as a sum of log-probabilities, never as a product, so a thousand tokens do not underflow to zero. The same stable softmax is used inside the attention step, which you will meet in the published transformer design. '
                         'This describes published practice. We do not know the internal code of closed products. Where else might a sum of logs be useful?')))

    S.append(dict(kind='practice', title='Check an AI assistant with your own numbers', minutes=10, label='Hands-on, with no private data',
                  task='Ask any AI assistant to compute a softmax that overflows. Then compare with your table.',
                  steps=['Type: "Compute softmax of the scores 1000, 1001 and 1002 without overflow. Show every step."', f'Expected result: {sb[0]:.4f}, {sb[1]:.4f}, {sb[2]:.4f}.', 'Did it subtract the maximum? If its answer differs, find the first number that differs from yours.', 'Never paste confidential data.'],
                  output='A note: did the assistant match your table?',
                  notes=('A hands-on check. Ask any assistant to compute the softmax of one thousand, one thousand and one, and one thousand and two, without overflow, and to show every step. '
                         f'The result should be {sb[0]:.4f}, {sb[1]:.4f} and {sb[2]:.4f}. Look at whether it subtracts the maximum, and find the first number that differs from your table. '
                         'Assistants sometimes slip on arithmetic, so use the assistant to explain and your own calculation to check. Please never paste confidential data into an assistant.')))

    S.append(dict(kind='table', title='Exit check: three questions with short answers',
                  headers=['Question', 'Short answer'],
                  rows=[['What does the L2 penalty do to the weights, and how do you choose lambda?', 'It shrinks the weights towards zero. Choose lambda by the error on held-out data only.'],
                        ['Why does subtracting the maximum not change the softmax?', 'The factor e^(-c) appears in the top and in every term of the bottom, so it cancels. It only keeps the exponents at most 0.'],
                        ['Why are log-probabilities added instead of probabilities multiplied?', 'A product of many probabilities underflows to 0. The sum of their logs is an ordinary number.']],
                  widths=[5.2, 6.8], icons=False,
                  notes=('Three questions to finish. First, the L2 penalty shrinks the weights towards zero, and lambda is chosen by the error on held-out data. '
                         'Second, subtracting the maximum does not change the softmax because the factor e to the minus c appears in the top and in every term of the bottom, so it cancels. It only keeps the exponents at or below zero. '
                         'Third, we add log-probabilities because a product of many probabilities underflows to zero, while the sum of the logs is an ordinary number. Write your own answers first.')))

    s['facilitator'] = dict(
        prep=['Run the notebook and the workbook once. Check that the stable softmax gives 0.0900, 0.2447, 0.6652 and that the ridge table matches the slide.',
              'Warn learners that the naive softmax cell prints RuntimeWarning and nan on purpose in step 1.',
              'Have a calculator ready for the by-hand ridge: 28.5 / 14 and 28.5 / 15.'],
        misconceptions=[('A larger lambda always gives a better model', 'It lowers the training fit. The held-out error falls and then rises again; lambda 0.1 is best on our data.'),
                        ('Subtracting the maximum changes the probabilities', 'The probabilities are identical. Only the intermediate numbers are smaller.'),
                        ('Lagrange multipliers need heavy calculus', 'The idea is geometric: at the best point on the boundary, the loss slope and the boundary slope are parallel. No derivation is needed today.'),
                        ('16-bit numbers are just a little less accurate', 'They also have a much smaller range (float16 stops at 65,504), which is why scaling and 32-bit copies are used.')],
        probes=[('If the training error is zero, is the model good?', 'No. On our data the unpenalised curve has zero training error and the largest error on new points (0.67).'),
                ('Why does subtracting the maximum also stop underflow of the whole sum?', 'The largest entry becomes e^0 = 1, so the sum is at least 1.'),
                ('What does a vanishing gradient mean for the early layers?', 'Their updates are almost zero, so they barely learn.'),
                ('How is weight decay different from clipping?', 'Weight decay shrinks the weights at every step. Clipping limits the length of the gradient only when it is too long.')],
        lab_steps=[('Python: overflow and the stable softmax (steps 1 and 2)', 'Naive softmax gives nan with a warning. Stable result 0.0900, 0.2447, 0.6652. Spreadsheet: the naive column shows "overflow", the gold cells fill the stable column.'),
                   ('Python: float formats (step 3)', 'float16 max is 65504; 400 tokens give a product of 0 but a log sum of -921.03.'),
                   ('Python: ridge (step 4)', f'Sum of squared weights {r3["norm2"]:.4f} and test RMSE {r3["rmse_te"]:.4f} at lambda 0.1. Spreadsheet: MINVERSE then MMULT; the 10 × 10 inverse is the gold block.'),
                   ('Python: compare and constraint (step 5)', 'Test error is lowest at lambda 0.1 in the table. Spreadsheet: the penalty sheet has the by-hand weights 2.0357, 1.9, 1.0179.')],
        rescue=['If the matrix part takes too long, use the by-hand one-weight ridge and show the table of the lambda sweep.', 'If a learner has no Python, do the spreadsheet: it has the same values.',
                'If time runs short, skip the weight-decay and constraint cells: the stable softmax and the ridge sweep are the core.'],
        after=['Share the solution notebook with absent learners.', 'Ask learners to bring one example of a probability from daily life for Session 13.'],
        lab_answer_key=[['PREDICT: what does the naive softmax of (1000, 1001, 1002) return?', 'nan, nan, nan, because exp overflows to inf and inf / inf is nan.'],
                        ['READ: why does the unpenalised curve have enormous weights?', 'X^T X is badly conditioned, so the solution uses large weights of opposite signs to pass through every point.'],
                        ['CHANGE: use lambda = 10', 'The curve is too stiff: the training and the test errors both rise.'],
                        ['CHANGE: use float16 for exp(12)', 'The result is inf.']])
    return s
