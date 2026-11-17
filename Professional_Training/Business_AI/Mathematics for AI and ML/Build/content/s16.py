"""Session 16: maximum likelihood and MAP (author F). Every number comes from the solution notebook (labs/s16_nb.py), so slides and lab agree."""
import importlib.util
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _ns():
    spec = importlib.util.spec_from_file_location('s16_nb_deck', HERE / 'labs' / 's16_nb.py')
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.namespace()


def build():
    N = _ns()
    pg = [float(v) for v in N['theta_grid']]
    lik = [float(v) for v in N['likelihood']]
    ll = [float(v) for v in N['log_likelihood']]
    post = [float(v) for v in N['posterior']]
    prior = [float(v) for v in N['prior']]
    mu = [float(v) for v in N['mu_grid']]
    sse = [float(v) for v in N['sse']]
    llmu = [float(v) for v in N['log_lik_mu']]
    ybar = float(N['y'].mean())
    b2 = {d: N['bias2'][d] for d in N['degrees']}
    var = {d: N['variance'][d] for d in N['degrees']}
    tot = {d: N['expected_error'][d] for d in N['degrees']}
    wr = [float(v) for v in N['w_ridge']]
    bce, cat = float(N['bce']), float(N['cat_loss'])
    const = n8 = 8 / 2 * math.log(2 * math.pi)
    L5 = lik[4]
    degrees = list(N['degrees'])
    tok = ['The', 'cat', 'sat', 'down']
    tp = [0.2, 0.1, 0.25, 0.05]
    tnll = sum(-math.log(p) for p in tp)
    fl = lambda a: f'{a:.6f}' if a >= 1e-4 else f'{a:.2e}'      # tiny likelihoods in scientific notation, so they do not read as 0

    s = dict(
        num=16, block='Probability and statistics', short_title='Maximum likelihood and MAP',
        title='Squared error and cross-entropy follow from one question: which parameters make the data most likely?',
        question='When a language model is trained, what exactly is it trying to make as large as possible?',
        outcomes=['Find the parameter that makes the data most likely (maximum likelihood estimation, MLE) for a coin and for a Gaussian mean, by hand and by scanning',
                  'Show that squared error comes from Gaussian noise (with the same sigma for every row) and cross-entropy from a Bernoulli or categorical assumption',
                  'Explain MAP as likelihood times a prior, its link to weight decay, and the trade-off between bias and variance'],
        outcome_icons=['chart', 'doc', 'check'],
        outcome_note=('By the end of today you can do three things. First, find the parameter that makes the data most likely, which is maximum likelihood estimation, for a coin and for a Gaussian mean, by hand and by scanning in Python or a spreadsheet. '
                      'Second, show that squared error and cross-entropy follow from probability assumptions about the noise or the labels, and are not arbitrary choices. '
                      'Third, explain MAP estimation as likelihood times a prior, see why it matches weight decay, and describe the trade-off between bias and variance with a simulation.'),
        clock=[(10, 'Recall, then a real question from AI'), (35, 'Concept: a picture, then one example by hand'), (10, 'Break'), (45, 'Lab in Python or a spreadsheet: predict, run, change one thing'),
               (15, 'Where this appears in AI, and an exit check'), (5, 'Save the work')],
        plan_title='Your two hours: likelihood, loss functions, then AI',
        plan_caption='Ideas first. Then the lab, in Python or a spreadsheet. Then AI.',
        plan_note=('Today has the usual shape. Ten minutes of recall from Session 15 and the question of the day. Thirty-five minutes of concepts, each with a picture and a hand example. A ten minute break. '
                   'Then forty-five minutes of lab, where you scan a likelihood yourself in Python or in a spreadsheet. We finish with where this appears in AI, an exit check and saving your work.'),
        recall_from='Session 15',
        recall=[('What does P(A | B) mean, in words?', 'The probability of A given that B has happened. Look only at the cases where B is true, and take the fraction of them in which A is also true.'),
                ("State Bayes' theorem in words.", 'The posterior equals the likelihood times the prior, divided by the evidence: P(A | B) = P(B | A) × P(A) / P(B).'),
                ('Why can a positive result from an accurate test still mean a small chance of disease?', 'Because the disease is rare. The prior is small, so most positive results are false alarms. The prior matters.')],
        words=[('Likelihood', 'How probable the exact data we saw are, for one chosen value theta of the parameter. Written p(data | theta).'),
               ('Maximum likelihood estimation (MLE)', 'Choose the parameter value with the largest likelihood.'),
               ('Log-likelihood', 'l(theta) = ln p(data | theta), in nats. A product becomes a sum. (L stays the loss.)'),
               ('Prior and MAP', 'The prior is what we believe before the data. Maximum a posteriori (MAP) estimation maximises likelihood times prior.'),
               ('Bias and variance', 'Bias: the error of the average prediction. Variance: how much the prediction moves between training sets.')],
        word_icons=['magnifier', 'chart', 'calculator', 'flag', 'bars'],
        words_note=('Five words for today. Likelihood is how probable the data are for one value of the parameter, and we write it p of data given theta. Maximum likelihood estimation chooses the value with the largest likelihood. '
                    'The log-likelihood is its natural logarithm, written with a curly l, and it turns a product into a sum. Capital L stays the loss, as in every session before. The prior is what we believe before seeing data, and MAP estimation maximises likelihood times prior. '
                    'Bias and variance describe two different ways a model can be wrong. Each word gets a picture before the break.'),
        keep='Keep your notebook or workbook with all checks passing. Keep these numbers: MLE 0.7, MAP 0.6, best mu 10.25, cross-entropy 0.299 nats, and the expected errors 0.319, 0.127 and 0.915 of the bias-variance simulation.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='MLE and MAP', value='0.7 and 0.6'), dict(label='Best mu', value='10.25'), dict(label='Cross-entropy', value='0.299 nats'),
                                                              dict(label='Next session', value='Information theory')]),
        keep_title='Save your lab and keep these numbers',
        next='Session 17: information theory. Entropy, cross-entropy, KL divergence, temperature and top-p, and perplexity.', next_label='Next session',
        keep_note=('Before you go, run the notebook or the workbook from the top and check that every check passes, then save it. Keep the numbers on the slide. '
                   'Next session takes the cross-entropy you met today and looks at it from the side of information. You will meet entropy and KL divergence, see how temperature and top-p reshape a model\'s probabilities, and compute the loss of a toy language model on a six word sentence. Bring one question.'),
        cover_note=('Welcome to Session 16. Until now we used loss functions such as squared error because they worked. Today you find out where they come from. '
                    'Each loss is what you get when you ask which parameters make the data most likely, once you say how you think the data arise. We also meet MAP, which adds a prior belief, and the trade-off between bias and variance.'),
        slides=[])
    S = s['slides']

    S.append(dict(kind='table', title='Answers to the three questions from Session 15', headers=['Question', 'Short answer'], rows=[[q, a] for q, a in s['recall']], widths=[5.0, 7.0], icons=False,
                  note='Today we use the prior and the likelihood from the third answer.',
                  notes=('P of A given B means the probability of A once we know B has happened, so we look only at the cases where B is true. '
                         "Bayes' theorem says the posterior equals the likelihood times the prior, divided by the evidence. "
                         'An accurate test can still give mostly false alarms when the disease is rare, because the prior is small. Two of those words, likelihood and prior, become the engine of training today. Which answer did you find harder to explain?')))

    S.append(dict(kind='idea', title='Training means choosing the parameter values that make the data we saw most probable',
                  visual=dict(kind='flow', steps=[dict(head='Data', text='10 coin flips: 7 heads and 3 tails', icon='folder'), dict(head='Model', text='A coin with an unknown chance of heads, theta', icon='gear'),
                                                  dict(head='Likelihood', text='How probable the data are for each theta', icon='calculator'), dict(head='Choice', text='Keep the largest', icon='check')], highlight=3),
                  lead='Maximum likelihood estimation (MLE) picks the parameter that makes the observed data most probable.',
                  points=['A parameter is a number the model learns. Theta (Session 8) stands for all of them. Here theta is the chance of heads (Session 14: p).',
                          'Today: a coin, a Gaussian curve, a classifier.'],
                  notes=('The whole of today fits in one picture. We have data, ten coin flips with seven heads. We have a model, a coin with an unknown chance of heads. In Session 14 that chance was called p. Today it is the number we learn, so it gets theta, the letter Session 8 gave to a model\'s numbers. '
                         'For every possible theta we ask how probable our data would be. That number is the likelihood. Then we keep the theta with the largest likelihood. That recipe is maximum likelihood estimation, and most loss functions in machine learning can be read this way.')))

    S.append(dict(kind='idea', title='The likelihood fixes the data and varies the parameter',
                  visual=dict(kind='f_coin_curve', mode='lik', marks=[0.5, 0.7, 0.9], best=0.7),
                  lead='The likelihood p(data | theta): how probable our exact 10 flips (7 heads, 3 tails, in this order) are if the chance of heads is theta.',
                  points=['The height is the likelihood of the same data. It peaks at theta = 0.7: 7 heads out of 10.',
                          'L stays the loss, so the likelihood is p(data | theta) and its log l(theta).'],
                  notes=('The horizontal axis is theta, the chance of heads, from zero to one. The height is the likelihood of our exact sequence of ten flips if the coin had that theta. '
                         'At theta equal to one half the height is about 0.001. At 0.9 it is lower, and at 0.7 it is the highest, about 0.0022. The data never change. Only the candidate theta changes. '
                         'That is the difference between probability, where the parameter is fixed and the data vary, and likelihood, where the data are fixed and the parameter varies. A word on letters: capital L has meant the loss since Session 7, so the likelihood gets the written form p of data given theta.')))

    S.append(dict(kind='example', title='By hand: the likelihood of one sequence with 7 heads and 3 tails, for three values of theta',
                  scenario='Flips are independent, so the likelihood of this exact sequence is a product: theta for each head, 1 - theta for each tail.',
                  blocks=[dict(label='theta = 0.5', text='0.5^7 × 0.5^3 = 0.000977'), dict(label='theta = 0.7', text='0.7^7 × 0.3^3 = 0.0823543 × 0.027 = ' + f'{lik[6]:.6f}', red=True),
                          dict(label='theta = 0.9', text='0.9^7 × 0.1^3 = 0.4782969 × 0.001 = ' + f'{lik[8]:.6f}'),
                          dict(label='Any order', text=f'× 120 (10 choose 7) = {120 * lik[6]:.4f}: Session 14\'s P(X = 3) at p = 0.3, since 7 heads at 0.7 is 3 tails at 0.3.')],
                  notes=('Seven heads and three tails in one particular order means seven factors of theta and three factors of one minus theta. For theta equal to 0.5 that is 0.5 to the tenth, 0.000977. '
                         f'For theta equal to 0.7 it is 0.0823543 times 0.027, which is {lik[6]:.6f}. For 0.9 the seven heads are cheap but the three tails cost a lot, and the product is only {lik[8]:.6f}. So among these three, 0.7 wins. '
                         f'For seven heads in any order we multiply by 120 and get {120 * lik[6]:.4f}. You met that number in Session 14 as three successes at 0.3. Seven heads at 0.7 is the same event as three tails at 0.3. Since 120 does not depend on theta, the winner does not change.')))

    S.append(dict(kind='table', title='Scan a grid of theta values: the likelihood of our exact sequence and its log are both largest at theta = 0.7', split=True,
                  headers=['theta', 'Likelihood p(data | theta)', 'Log-likelihood l(theta), nats'], rows=[[f'{p:.1f}', fl(a), f'{b:.3f}'] for p, a, b in zip(pg, lik, ll)], widths=[1.4, 2.9, 2.9], icons=False,
                  note='The exact sequence 1, 1, 0, 1, 1, 1, 0, 1, 0, 1. 7.29e-08 means 7.29 × 10^-8 = 0.0000000729: small, but not zero.',
                  notes=('This table is the lab in miniature. Nine candidate values of theta, and for each one the likelihood and, in the last column, its natural logarithm. '
                         f'The likelihood is largest at 0.7, with {lik[6]:.6f}. The log-likelihood is largest at 0.7 too, with {ll[6]:.3f} nats. The smallest likelihoods are written in scientific notation, because six decimals would show them as zero, and they are not zero. '
                         'This scanning method works for any model, even when no neat formula exists. In the lab you build this table in Python or in a spreadsheet.')))

    S.append(dict(kind='formula', title='For a coin the MLE has a closed form: the fraction of heads',
                  formulas=[('Likelihood of the exact sequence', r'$p(\mathrm{data}\mid\theta)=\theta^{k}(1-\theta)^{n-k}$'), ('Maximum likelihood estimate', r'$\hat{\theta}=\frac{k}{n}=\frac{7}{10}=0.7$')],
                  symbols=[['theta', 'The chance of heads. This is the unknown parameter.', 'tried from 0.1 to 0.9'], ['k', 'The number of heads.', '7'], ['n', 'The number of flips.', '10'],
                           ['theta-hat', 'The maximum likelihood estimate of theta.', '0.7']],
                  size=24, note='Why: the slope of l(theta), k/theta - (n - k)/(1 - theta), is zero at theta = k/n. The factor 120 does not move the peak.',
                  notes=('The likelihood is theta to the power k times one minus theta to the power n minus k, where k is the number of heads and n the number of flips. '
                         'Take the natural log, find its slope with the rules of Session 7, and set the slope to zero. The answer is theta-hat equals k over n. For us that is seven over ten, 0.7, so the scan and the formula agree. '
                         'The hat on theta means an estimate computed from data. Read the symbol table and say what each symbol means in our coin data.')))

    S.append(dict(kind='idea', title='A product of many small probabilities vanishes, so we add logarithms instead',
                  visual=dict(kind='f_underflow'),
                  lead='The log-likelihood l(theta) is the natural logarithm (ln) of the likelihood, measured in nats.',
                  points=['A logarithm turns a product into a sum, and the maximum stays at the same theta.', '0.5 to the power 1,100 is stored as 0.0 by a computer. But 1,100 × ln(0.5) = -762.46 is a normal number.'],
                  notes=('Each fair coin flip multiplies the likelihood by one half, so its natural log falls by 0.693 per flip. That is the straight black line. After ten flips we have about one in a thousand. After a hundred flips about ten to the minus thirty. '
                         'The red dashed line is the limit: a likelihood whose log is below about minus 744 is too small for a computer to store, and Python prints zero. After eleven hundred flips we are below it. '
                         'The logarithm of the product is a sum, eleven hundred times ln of one half, which is minus 762.46. Language models score thousands of tokens, so they always work with sums of logarithms.')))

    S.append(dict(kind='wide', title='The log-likelihood curve peaks at the same theta as the likelihood curve',
                  visual=dict(kind='f_coin_curve', mode='both', marks=[0.7], best=0.7),
                  caption='Left: likelihood. Right: log-likelihood. Same maximum, theta = 0.7.',
                  notes=('Put the two curves side by side. On the left is the likelihood and on the right the log-likelihood of the same ten flips. The shapes differ: the log curve is flatter on top and falls steeply near zero and one. '
                         'The highest point sits at the same theta, 0.7, in both. The logarithm always goes up when its input goes up, so it cannot move the maximum. '
                         'So it is safe to maximise the log-likelihood instead. Any function that keeps the order of values keeps the location of the maximum.')))

    S.append(dict(kind='formula', title='The log-likelihood is a sum, and training minimises its negative',
                  formulas=[('Log-likelihood', r'$\ell(\theta)=\ln p(\mathrm{data}\mid\theta)=\sum_{i=1}^{n}\ln p(y_i\mid\theta)$'), ('Loss (negative log-likelihood)', r'$L(\theta)=\mathrm{NLL}(\theta)=-\ell(\theta)$')],
                  symbols=[['theta', 'All the numbers of the model together (Session 8).', 'one number for the coin'], ['y_i', 'The i-th data point.', 'one flip or one measurement'],
                           ['p(y_i | theta)', 'The probability the model gives to y_i.', 'theta or 1 - theta for a flip'], ['l(theta)', 'The log-likelihood, in nats.', f'{ll[6]:.3f} at theta = 0.7']],
                  size=22, note='Minimising the NLL gives the same theta as maximising the likelihood. The NLL is the loss L of earlier sessions.',
                  notes=('The log-likelihood, written with a curly l, is the sum over all data points of the log of the probability the model gives that point. The independence of the flips is what lets the product split into a sum. '
                         'Machine learning libraries like to minimise a loss, so we put a minus sign in front and call it the negative log-likelihood, or NLL. That is the loss L you have used since Session 10. '
                         'Minimising it and maximising the likelihood pick exactly the same parameters. Theta stands for all the parameters, one number or billions.')))

    S.append(dict(kind='idea', title='Gaussian noise: each target sits near the prediction, with bell-shaped scatter',
                  visual=dict(kind='f_gauss_noise'),
                  lead='Assume y = y-hat plus noise, where the noise follows a Gaussian (normal) distribution with mean 0 and standard deviation sigma.',
                  points=['Small residuals (y minus y-hat) are likely. Large ones are rare.', 'The yellow bells are the Gaussian probability density function drawn around the line.'],
                  notes=('The second assumption is about numbers. The model gives a prediction y-hat, the red line, and the real target is that prediction plus noise. '
                         'The noise follows a Gaussian, the bell curve, centred on the line. The yellow bells show it at two places. Most real points land close to the line, and the dashed residuals are short. Few land far away. '
                         'Is that a reasonable assumption for measurement errors? Often it is, because many small independent effects add up to a bell shape, which is the central limit theorem from Session 14.')))

    S.append(dict(kind='formula', title='Gaussian noise turns the negative log-likelihood into a squared error plus a constant',
                  formulas=[('Gaussian density', r'$p(y\mid\hat{y})=\frac{1}{\sqrt{2\pi\sigma^{2}}}\exp\left(-\frac{(y-\hat{y})^{2}}{2\sigma^{2}}\right)$'),
                            ('Negative log-likelihood', r'$-\ell=\frac{1}{2\sigma^{2}}\sum_{i=1}^{n}(y_i-\hat{y}_i)^{2}+\frac{n}{2}\ln(2\pi\sigma^{2})$')],
                  symbols=[['y_i - y-hat_i', 'The residual of row i.', 'actual minus predicted'], ['sigma', 'The standard deviation of the noise.', '1 mm in the lab'],
                           ['Sum of squares', 'The sum of squared errors (SSE).', f'{sse[5]:.2f} at mu = {mu[5]:g}'], ['Last term', 'A constant that does not depend on the model.', f'{const:.2f} for n = 8, sigma = 1']],
                  size=22, note='Only the squared-error part depends on the model. With the same sigma for every row, squared error is Gaussian MLE.',
                  notes=('Write down the Gaussian density for one point, then take minus its natural log. The exponential and the log cancel. What is left is the squared residual divided by two sigma squared, plus a constant. '
                         'Add that over all n points. The constant on the right does not depend on the model, so it cannot affect which parameters win. '
                         f'Minimising the sum of squared errors is therefore the same as maximising the likelihood, when the noise is Gaussian with the same sigma for every row. For our eight measurements with sigma equal to one, the constant is {const:.2f}. Squared error is a probability assumption in disguise.')))

    sel = [0, 2, 4, 5, 6, 8, 10]
    S.append(dict(kind='table', title='Eight measurements: the mu with the smallest squared error has the largest likelihood',
                  headers=['mu (mm)', 'Sum of squared errors', 'Log-likelihood (nats)'], rows=[[f'{mu[i]:.2f}', f'{sse[i]:.2f}', f'{llmu[i]:.4f}'] for i in sel], widths=[2.4, 4.0, 4.0], icons=False,
                  note=f'The simplest model predicts the same width mu for every part, so y-hat_i = mu. Widths (mm, illustrative): 9.8, 10.4, 11.2, 9.1, 10.7, 10.1, 11.5, 9.2. Sigma = 1. Mean {ybar:g}. Every row: -(log-likelihood) = SSE / 2 + {const:.2f}.',
                  notes=('Eight measurements of a part width, in millimetres, with sigma equal to one. The model is the simplest possible: it predicts the same width, mu, for every part. So y-hat is mu in every row, and the line of the last slide is flat. '
                         f'For each candidate mu we compute the sum of squared errors and the log-likelihood. Both are best at mu equal to {mu[5]:g}, which is exactly the average of the eight numbers. Check one row: at mu equal to {mu[5]:g}, the sum of squares {sse[5]:.2f}, divided by two, plus {const:.2f}, gives minus the log-likelihood, {-llmu[5]:.3f}. '
                         'The average is the maximum likelihood estimate of a Gaussian mean.')))

    S.append(dict(kind='idea', title='Cross-entropy: the loss -ln(p) grows steeply when the true answer gets a small probability',
                  visual=dict(kind='f_ce_curve', marks=[0.9, 0.5, 0.1]),
                  lead='A Bernoulli model gives probability p to class 1 and 1 - p to class 0. Here p is the model\'s predicted probability.',
                  points=['The negative log-likelihood of one label is the binary cross-entropy loss, in nats.', 'With many classes, the loss is -ln of the probability given to the true class.'],
                  notes=('The third assumption is for classification. A Bernoulli model says the answer is yes with probability p and no with probability one minus p. From here on p is the probability the model predicts, the letter Sessions 17 and 18 also use. '
                         'The negative log of the probability the model gave to the true answer is the cross-entropy loss. Give the true answer probability 0.9 and the loss is only 0.11 nats. Give it 0.5 and the loss is 0.69. '
                         'Give it 0.1 and the loss is 2.30. A confident wrong answer is punished hard, which gives training a strong signal exactly where the model is most wrong.')))

    S.append(dict(kind='formula', title='A Bernoulli or categorical assumption gives the cross-entropy loss',
                  formulas=[('Binary cross-entropy', r'$-\left[\,y\ln p+(1-y)\ln(1-p)\,\right]$'), ('Categorical cross-entropy', r'$-\ln p_{c}$')],
                  symbols=[['y', 'The true label, 0 or 1.', 'four rows: 1, 0, 1, 1'], ['p', 'The probability the model gives to class 1.', 'four rows: 0.8, 0.3, 0.6, 0.9'], ['c', 'The index of the true class.', 'the first of three classes'],
                           ['p_c', 'The probability given to the true class.', '0.7']],
                  size=24, note=f'Illustrative. The four rows give a mean loss of {bce:.3f} nats. Classes 0.7, 0.2, 0.1 with the first true: {cat:.3f} nats.',
                  notes=('For a yes or no label y, the loss is minus y times ln p, minus one minus y times ln of one minus p. Only one of the two terms is active, because y is either one or zero. '
                         'If y is one and the model said 0.8, the loss is 0.223. If y is zero and the model said 0.8, the loss is 1.609. '
                         f'With several classes the model gives a probability to each, and the loss is minus ln of the probability of the true class. With 0.7, 0.2 and 0.1 and the first class true, that is {cat:.3f}. '
                         f'The four illustrative rows average {bce:.3f} nats. Session 17 measures the same quantity in bits.')))

    S.append(dict(kind='table', title='Each common loss is a probability assumption in disguise',
                  headers=['Task', 'Assumption about the target', 'Loss that follows'],
                  rows=[['Regression', 'Gaussian noise around the prediction, the same sigma for every row', 'Squared error (mean squared error)'], ['Yes or no', 'Bernoulli: yes with probability p', 'Binary cross-entropy'],
                        ['One of K classes, such as the next token', 'Categorical: K probabilities that add to 1', 'Categorical cross-entropy']],
                  widths=[3.4, 4.6, 4.0], icons=['chart', 'check', 'speech'],
                  note='Change the assumption and the right loss changes with it. For noise with heavy tails the log-likelihood gives a different loss.',
                  notes=('Put the three together. If the target is a number and we think the noise is Gaussian, maximum likelihood gives squared error. If the target is yes or no, a Bernoulli assumption gives binary cross-entropy. '
                         'If the target is one of many classes, such as the next token of a sentence, a categorical assumption gives categorical cross-entropy. '
                         'So the losses are not arbitrary. Each is the negative log-likelihood of a model of how the data arise. If you believe a different noise shape, the right loss changes. Which row matches the problems at your workplace?')))

    S.append(dict(kind='wide', title='MAP: the posterior is the likelihood times a prior, and the prior pulls the estimate',
                  visual=dict(kind='f_panels_bars', labels=[f'{p:.1f}' for p in pg],
                              panels=[dict(title='Likelihood', note='7 heads in 10 flips', values=lik, hl=6, best_label='0.7'), dict(title='Prior weight', note='near fair; total 25', values=prior, hl=4, best_label='0.5'),
                                      dict(title='Likelihood × prior', note='the posterior, unscaled', values=post, hl=5, best_label='0.6')]),
                  caption='MLE 0.7, MAP 0.6. Dividing every weight by 25 gives probabilities and the same MAP.',
                  notes=("Maximum a posteriori estimation, or MAP, adds what we believed before the data. On the left is the likelihood, which peaks at 0.7. In the middle is a prior, a weight for each theta. I chose weights from one to five that favour a coin close to fair. "
                         'They add to 25, so dividing each by 25 would make them probabilities. That scales every product by the same factor and cannot change the winner. '
                         'On the right is their product, which is proportional to the posterior from Bayes theorem in Session 15. It peaks at 0.6. The prior pulled the estimate towards a fair coin. Which way would the answer move with a thousand flips?')))

    S.append(dict(kind='table', title='By hand: likelihood times prior weight is largest at theta = 0.6, so MAP is 0.6 and MLE is 0.7', split=True,
                  headers=['theta', 'Likelihood', 'Prior weight', 'Product'], rows=[[f'{p:.1f}', fl(a), f'{int(round(w))}', fl(c)] for p, a, w, c in zip(pg, lik, prior, post)], widths=[1.0, 2.2, 1.9, 2.2], icons=False,
                  notes=(f'Take the row for 0.6. The likelihood is {lik[5]:.6f} and the prior weight is 4, which gives {post[5]:.6f}. At 0.7 the likelihood is higher but the prior weight is only 3, so the product is {post[6]:.6f}. '
                         'That is smaller than at 0.6, so MAP picks 0.6. I did not divide by the evidence. It is the same number for every theta, so it cannot change which theta wins. '
                         'With more flips the likelihood would become sharper and the prior would matter less.')))

    S.append(dict(kind='formula', title='A Gaussian prior on the weights adds an L2 penalty, the idea behind weight decay',
                  formulas=[('MAP loss', r'$-\ln p(\mathrm{data}\mid w)-\ln p(w)=\frac{1}{2\sigma^{2}}\mathrm{SSE}+\frac{1}{2\tau^{2}}\sum_{j}w_j^{2}+\mathrm{constant}$'), ('Multiply by 2 sigma^2: same minimum as', r'$\mathrm{SSE}+\lambda\sum_{j}w_j^{2},\qquad\lambda=\frac{\sigma^{2}}{\tau^{2}}$')],
                  symbols=[['w_j', 'The j-th weight of the model.', 'one weight in our example'], ['tau', 'Standard deviation of the Gaussian prior on each weight. Small tau means a strong belief that w is near 0.', 'prior mean 0'],
                           ['lambda', 'The weight decay strength (L2 regularisation strength).', 'sigma squared over tau squared'], ['SSE', 'The sum of squared errors.', 'from the Gaussian noise slide']],
                  size=18, note='Small tau, large lambda, smaller weights: the ridge penalty of Session 12.',
                  notes=('Take the MAP loss, which is the negative log-likelihood plus the negative log of the prior. If the noise is Gaussian the first part is the sum of squared errors over two sigma squared. '
                         'If the prior on each weight is a Gaussian centred at zero with standard deviation tau, the second part is the sum of squared weights over two tau squared. Constants that do not depend on the weights drop out. Multiply everything by two sigma squared and you get squared error plus lambda times the sum of squared weights, the ridge penalty of Session 12. '
                         'Lambda equals sigma squared over tau squared. An L2 penalty corresponds to a Gaussian prior, which is the idea behind weight decay, exactly so for plain gradient descent.')))

    S.append(dict(kind='idea', title='By hand: the penalty pulls the best weight towards 0',
                  visual=dict(kind='f_penalty', lam=5),
                  lead=f'Fit y = w x on x = 1, 2, 3 and y = 2.1, 3.9, 6.2 (illustrative). The best w is 28.5 divided by (14 plus lambda).',
                  points=[f'lambda = 0, 1, 5, 14 gives w = {wr[0]:.3f}, {wr[1]:g}, {wr[2]:g}, {wr[3]:.3f}.', 'The sum of the two curves has its lowest point to the left of the squared-error minimum.'],
                  notes=(f'Check it with numbers. We fit a line through the origin, y equals w x, to three points. The sum of x times y is 28.5 and the sum of x squared is 14. With no penalty the best w is {wr[0]:.3f}. '
                         f'With lambda equal to one it is {wr[1]:g}. With lambda equal to five it is {wr[2]:g}. With lambda equal to fourteen it is {wr[3]:.3f}, half of the first. '
                         'The picture shows why. The black curve is squared error, the grey dashed one is the penalty, and the red sum has its lowest point between zero and the black minimum. What would a huge lambda do?')))

    S.append(dict(kind='wide', title='Bias and variance: refit the same model on 300 fresh noisy training sets',
                  visual=dict(kind='f_bv_sim'),
                  caption='Smooth wave plus noise 0.3. Right: high variance, as in Session 12\'s degree-9 fit.',
                  notes=('A simulation makes the two kinds of error visible. The true curve, in red, is a smooth wave. Each time I draw ten noisy points around it and fit a model, then repeat three hundred times. Thirty of the fitted curves are in grey, and the dashed line is their average. '
                         'On the left a straight line is too stiff. Its average is far from the red curve, and that gap is the bias. On the right a degree nine polynomial passes through every point, so it wobbles wildly from one training set to the next. That wobble is the variance, the same overfitting you saw in Session 12. '
                         'The cubic in the middle is close on both counts.')))

    S.append(dict(kind='idea', title='Expected error splits into bias squared, variance and noise',
                  visual=dict(kind='f_bv_stack', degrees=degrees, bias2=[b2[d] for d in degrees], variance=[var[d] for d in degrees], noise=0.09),
                  lead=f'The cubic has the smallest expected error, {tot[3]:.3f}. It balances bias and variance.',
                  points=[f'Degree 1: bias squared {b2[1]:.3f}, variance {var[1]:.3f}.', f'Degree 9: bias squared {b2[9]:.3f}, variance {var[9]:.3f}.', 'The noise, 0.3 squared = 0.09, stays in every bar.'],
                  notes=(f'Each bar is the expected squared error on new data, split into bias squared in red, variance in gold and noise in grey. '
                         f'Degree one is mostly bias, {b2[1]:.3f}. Degree nine is almost all variance, {var[9]:.3f}, which makes its total {tot[9]:.3f}. The cubic has a little of each and the smallest total, {tot[3]:.3f}. '
                         'The grey noise, nought point three squared, is 0.09 in every bar. No model can remove it. This is the bias-variance trade-off: flexible models cut bias and raise variance.')))

    S.append(dict(kind='formula', title='Expected squared error is bias squared plus variance plus noise',
                  formulas=[('Decomposition', r'$\mathrm{Error}=\mathrm{Bias}^{2}+\mathrm{Variance}+\sigma^{2}$'), ('Cubic, from the simulation', r'$%.3f=%.3f+%.3f+0.09$' % (tot[3], b2[3], var[3]))],
                  symbols=[['Bias squared', 'The squared gap between the average prediction and the truth.', f'degree 1: {b2[1]:.3f}'], ['Variance', 'How much the prediction moves between training sets.', f'degree 9: {var[9]:.3f}'],
                           ['sigma squared', 'The variance of the noise. It cannot be removed.', '0.3 squared = 0.09'], ['Error', 'The expected squared error on new data.', f'cubic: {tot[3]:.3f}']],
                  size=24, note='Larger lambda: less variance, more bias. Choose lambda on a validation split (Session 12).',
                  notes=('The expected squared error on new data is the bias squared plus the variance plus the noise variance. For the cubic the numbers are 0.007, 0.030 and 0.09, which add up to 0.127. '
                         'This links back to MAP. A larger lambda shrinks the weights, which lowers variance but raises bias. Weight decay is a dial between the two. '
                         'We choose lambda on a validation split, as in Session 12, and report the test error once at the end.')))

    S.append(dict(kind='compare', title='Three common mistakes about likelihood and MAP',
                  left=dict(head='The mistake', points=['The likelihood at theta = 0.7 is the probability that theta is 0.7.', '3 heads in 3 flips proves theta = 1.', 'Squared error assumes nothing.']),
                  right=dict(head='The fix', points=['It is how probable the data are if theta is 0.7.', 'Little data makes MLE extreme. A prior tempers it.', 'It assumes Gaussian noise.']),
                  verdict='Every loss hides a probability model. Name it.',
                  notes=('Three mistakes I see often. First, the likelihood is not the probability that theta equals 0.7. It is how probable the data are if theta equals 0.7. Those are different questions, and Bayes theorem links them through the prior. '
                         'Second, with three flips and three heads the maximum likelihood estimate is theta equal to one, which says tails is impossible. That is overconfident, and a prior fixes it. '
                         'Third, squared error does carry an assumption, Gaussian noise. When the noise has heavy tails, another loss may be better. Which of the three would you have made?')))

    S.append(dict(kind='code', title='Read the recipe before you write it: grid, likelihood, logarithm, argmax',
                  code='k, n = 7, 10\nprior = np.array([1, 2, 3, 4, 5, 4, 3, 2, 1])\ntheta = np.linspace(0.1, 0.9, 9)\nlik = theta**k * (1 - theta)**(n - k)\nloglik = k*np.log(theta) + (n - k)*np.log(1 - theta)\ntheta_hat = theta[np.argmax(loglik)]\ntheta_map = theta[np.argmax(lik * prior)]',
                  reads=['Lines 1, 2: the data and the prior weights.', 'Line 3: nine candidate values of theta.', 'Line 4: the likelihood for every theta.', 'Line 5: the log-likelihood, a sum.', 'Line 6: argmax gives the position of the largest value: the MLE.', 'Line 7: times the prior: the MAP estimate.',
                         'Spreadsheet: INDEX and MATCH on MAX return the theta.'],
                  notes=('Read the recipe before the lab. First make a grid of candidate values of theta. Then compute the likelihood for all of them at once, using numpy arrays, and the log-likelihood as a sum. '
                         'The function argmax returns the position of the largest value, so indexing theta with it gives the maximum likelihood estimate. Multiply the likelihood by a prior before the argmax and you get MAP. '
                         'In a spreadsheet the same step is MAX to find the largest value, and INDEX with MATCH to read the theta beside it. You do not need to memorise any of it, because the notebook and the workbook explain every line.')))

    S.append(dict(kind='divider', title='Part 2: the lab', lead='Close the slides. Open the notebook or the workbook.', section='Lab',
                  notes=('That is the end of the concepts. Everything you need is on the slides you have seen, and each term is explained again inside the notebook and the workbook. '
                         'Open one of them now. If you use Python, run the cells from the top in order. If you use the spreadsheet, start on the sheet called Start here. '
                         'Raise your hand if something does not run. Keep the rhythm: predict first, then run, then change one thing.')))

    S.append(dict(kind='steps', title='The lab has five parts: coin, Gaussian, cross-entropy, MAP and bias-variance',
                  steps=[dict(head='1 Coin', text='Steps 1 and 2: likelihood and log-likelihood over a grid of theta', icon='calculator'), dict(head='2 Gaussian', text='Steps 3 and 4: scan mu and compare with squared error', icon='chart'),
                         dict(head='3 Cross-entropy', text='Step 5: the loss of four labels', icon='check'), dict(head='4 MAP', text='Step 6: prior, posterior and weight decay', icon='lock'), dict(head='5 Bias-variance', text='Step 7: 300 training sets, three models', icon='gear')],
                  caption='Python: Steps 1 to 7. Spreadsheet: sheets Coin, Gaussian, Shrink (cross-entropy and weight decay) and Bias-variance. Predict, run, then change one thing.',
                  notes=('The lab has five parts, which are Steps 1 to 7 in the notebook. In the first you scan the likelihood of the coin and find theta-hat. In the second you scan the Gaussian mean and show that squared error picks the same mu. '
                         'In the third you compute a cross-entropy by hand and with numpy. In the fourth you add a prior and watch the estimate move, then shrink a weight. In the fifth you run the bias-variance simulation in Python, and spreadsheet learners add up its three results. '
                         'The spreadsheet has the same numbers on four sheets. Do not skip the predict cells. Guessing first is how you learn what you understood.')))

    S.append(dict(kind='table', title='Check your numbers against these before you move on',
                  headers=['What you compute', 'You should see'],
                  rows=[['Likelihood of this exact sequence (7 heads, 3 tails) at theta = 0.7', f'{lik[6]:.6f}'], ['Probability of 7 heads in any order at theta = 0.7', f'{120 * lik[6]:.4f}'], ['Log-likelihood of the exact sequence at theta = 0.7', f'{ll[6]:.4f} nats'],
                        ['Best mu for the eight widths, and its log-likelihood', f'{mu[5]:g} and {llmu[5]:.4f} nats'], ['Binary cross-entropy of the four labels (1, 0, 1, 1; p = 0.8, 0.3, 0.6, 0.9)', f'{bce:.4f} nats'],
                        ['MAP estimate of theta', '0.6'], ['Weights for lambda = 0, 1, 5, 14', ', '.join(f'{v:.4g}' for v in wr)], ['Expected error, degrees 1, 3 and 9 (Python)', ', '.join(f'{tot[d]:.3f}' for d in degrees)]],
                  widths=[7.2, 4.4], icons=['calculator', 'bars', 'chart', 'check', 'flag', 'pin', 'lock', 'gear'],
                  note='If your number differs, stop and ask. Find the step that went wrong. Do not change a number to match.',
                  notes=('Use this table as your checkpoint. The likelihood of the exact sequence at 0.7 is 0.002224, which is 0.2668 for seven heads in any order, and the log-likelihood is minus 6.1086 nats. The best mu is 10.25 and the sum of squared errors there is 5.34. '
                         'The cross-entropy of the four labels is 0.299 nats, the MAP estimate is 0.6, and the four shrunk weights are in the table. The last row, the three expected errors, is for the notebook. '
                         'If a number is different, stop and call me over. Do not edit a number to make it match. The most common reason is a cell that ran out of order.')))

    S.append(dict(kind='table', title='Errors you will meet, what they mean and what to do',
                  headers=['What you see', 'What it means', 'What to do'],
                  rows=[['NameError', 'A name from a cell you have not run yet', 'Run all cells from the top, in order'], ['NOT YET: write your code in the cell above', 'An answer cell (marked gold) still says None', 'Replace None with your code and run both cells again'],
                        ['likelihood prints 0.0 or nan', 'A product underflowed, or log of 0', 'Work with the log-likelihood and keep theta between 0 and 1'], ['Spreadsheet shows #NAME?', 'A function name is mistyped', 'Check the spelling, such as NORM.DIST']],
                  widths=[3.4, 4.4, 4.2], icons=['bell', 'key', 'cross', 'flag'],
                  notes=('Errors are normal, and these are the four you will most likely meet. A name error means you skipped a cell, so run all cells from the top. '
                         'A message saying not yet, write your code, means a gold answer cell still holds the placeholder. Replace it with your code. A likelihood of zero or nan means a product underflowed, or you took the log of zero, so use the log-likelihood and keep theta strictly between zero and one. '
                         'In the spreadsheet a hash name error means a mistyped function. Read the last line of any error first. It usually tells you what to do.')))

    S.append(dict(kind='wide', title='Where this appears in AI: the likelihood of the next token',
                  visual=dict(kind='f_tokens', tokens=tok, probs=tp, base='e', total_label='Illustrative (made-up numbers to show the arithmetic): a 4-token sentence.'),
                  caption=f'Published research: training minimises the sum of -ln p. Here the sum is {tnll:.2f} nats.',
                  notes=('A language model gives every possible next word a probability. For the sentence the cat sat down, suppose it gave 0.2, 0.1, 0.25 and 0.05 to the four words that actually came next. These numbers are made up. '
                         f'The likelihood of the sentence is the product, and the negative log-likelihood is the sum of the red numbers, {tnll:.2f} nats. Published research describes training this kind of model by minimising exactly this quantity, averaged over a huge amount of text. '
                         'That is maximum likelihood of the next token. The exact internals of ChatGPT, Gemini and Claude are not published, but this is the published framework for models of this kind.')))

    S.append(dict(kind='idea', title='Where this appears in AI: weight decay and the Gaussian prior',
                  visual=dict(kind='flow', steps=[dict(head='Prior', text='Weights are probably small, near 0', icon='flag'), dict(head='Penalty', text='lambda times the sum of squared weights', icon='lock'),
                                                  dict(head='Training', text='Minimise the loss plus the penalty', icon='gear'), dict(head='Effect', text='Smaller weights, less variance', icon='chart')], highlight=1),
                  lead='The Llama 1 and 2 papers (Touvron et al., 2023) report AdamW with weight decay 0.1.',
                  points=['With plain gradient descent, weight decay equals an L2 penalty (MAP, Gaussian prior). AdamW (Loshchilov and Hutter, 2019) decays separately: an analogy.', 'ChatGPT, Gemini and Claude do not publish theirs: no claim.'],
                  notes=('Weight decay is a standard setting in published work on training neural networks, and the textbook explanation is the one you saw today: a Gaussian prior on the weights. '
                         'The Llama 1 and Llama 2 papers by Touvron and colleagues in 2023 report the AdamW optimiser with weight decay 0.1. With plain gradient descent, weight decay equals an L2 penalty, which is MAP with a Gaussian prior. With Adam the decay is applied separately, in the AdamW method, so the link to MAP is an analogy there. '
                         'For the closed products, ChatGPT, Gemini and Claude, the vendors do not publish the details, so I will not tell you what they use. Models of this kind are trained with a log-likelihood loss, and regularisation is the standard tool against variance.')))

    S.append(dict(kind='practice', title="Check an AI assistant's answer against your own numbers", minutes=5, label='Optional, with any assistant',
                  task='Ask an assistant for the MLE of the chance of heads after 7 heads in 10 flips, and the likelihood of that sequence.',
                  steps=['Compare with 0.7 and 0.002224 (any order: 0.2668).', 'Ask for the MAP estimate on today\'s grid and prior weights. Compare with 0.6.', 'Never paste confidential data into an assistant.'],
                  output='A note: where the assistant agreed with your numbers, and where it did not.',
                  notes=('Try this with any assistant. Ask it for the maximum likelihood estimate of a coin that gave seven heads in ten flips, and the likelihood at that value. Compare with your own numbers, 0.7 and 0.002224 for the exact sequence, or 0.2668 for seven heads in any order. '
                         'Then ask for the MAP estimate on the grid of nine values with the prior weights from today and compare with 0.6. Assistants can make arithmetic slips, and you now have the tools to check them. '
                         'Please do not paste confidential data into any assistant. Write down where it agreed with you and where it did not.')))

    S.append(dict(kind='table', title='Exit check: three questions and their short answers',
                  headers=['Question', 'Short answer'],
                  rows=[['A coin gives 9 heads in 12 flips. What is the MLE of its chance of heads?', 'k / n = 9 / 12 = 0.75.'], ['Which probability assumption turns maximum likelihood into squared error?', 'Gaussian noise around the prediction.'],
                        ['What does a Gaussian prior on the weights add to the loss?', 'An L2 penalty, lambda times the sum of squared weights (weight decay).']],
                  widths=[6.0, 6.0], icons=False, note='Answer each in one sentence before you read the right-hand column.',
                  notes=('Three questions to finish. One, a coin gives nine heads in twelve flips, so the maximum likelihood estimate of its chance of heads is nine over twelve, 0.75. '
                         'Two, the probability assumption that turns maximum likelihood into squared error is Gaussian noise around the prediction. '
                         'Three, a Gaussian prior on the weights adds an L2 penalty, which deep learning calls weight decay. Cover the right-hand column and answer each one aloud first. '
                         'If one was shaky, mark it, and look at the slide again before Session 17.')))

    s['facilitator'] = dict(
        prep=['Run the solution notebook once from the top so you know the numbers: MLE 0.7, MAP 0.6, best mu 10.25, cross-entropy 0.299.', 'Open the workbook for Session 16 in Excel or Google Sheets and check that the Check sheet says all checks pass.',
              'Have the slide "Check your numbers" ready to project for the lab.', 'Write the three loss assumptions on the board before the concepts: Gaussian, Bernoulli, categorical.'],
        misconceptions=[('The likelihood is the probability that the parameter has that value.', 'It is the probability of the data given the parameter. The probability of the parameter given the data needs a prior and Bayes theorem.'),
                        ('We take logarithms to make the numbers look nicer.', 'Products of many small numbers underflow to 0, and sums are easier to differentiate. The maximum does not move.'),
                        ('Squared error is just a convenient choice.', 'It is exactly the Gaussian negative log-likelihood, up to a constant. The choice hides an assumption.'),
                        ('A prior is a bias in the bad sense.', 'A prior is stated openly, and with enough data the likelihood outweighs it. Bias in bias-variance is a different thing: the error of the average prediction.')],
        probes=[('Why is the likelihood at theta = 0.7 only 0.0022 although it is the best?', 'It is the probability of one exact sequence of flips, and there are 1,024 sequences. A small value is normal.'),
                ('If we had 700 heads in 1,000 flips, would MAP and MLE differ more or less?', 'Less. The likelihood becomes sharp and outweighs the prior.'),
                ('What would a heavy-tailed noise assumption do to the loss?', 'The loss would grow slower than squared for large errors, so outliers would count less.'),
                ('Why does the lab constant, 7.35, not matter?', 'It is n/2 ln(2 pi sigma squared) and does not depend on mu, so it shifts every log-likelihood equally and cannot change which mu is best.'),
                ('Is weight decay the same as L2 regularisation?', 'For plain gradient descent they match. For some optimisers such as Adam they differ, and the published decoupled weight decay (AdamW) is a separate method. Say you are not sure if pressed on details.')],
        lab_steps=[('Step 1: coin scan', 'Python: likelihood of the exact sequence at theta = 0.7 is 0.002224 (0.2668 for any order) and the maximum is at 0.7. Spreadsheet: the MAX and INDEX/MATCH cells give 0.7. Anyone who gets theta = 7 forgot to divide, or used 7 heads as a probability. The letter: theta is the chance of heads (Session 14 called it p), and L stays the loss.'),
                   ('Step 2: log-likelihood', 'Both tracks: -6.1086 nats at 0.7. Python prints 0.0 for 0.5**1100 and -762.46 for the sum of logs. Ask why the second works.'),
                   ('Step 3 and 4: Gaussian mean and squared error', 'Best mu 10.25, log-likelihood -10.0215, SSE 5.34, constant 7.3515 (sigma = 1). The gap now divides by 2 sigma squared, so it stays the same in every row for any sigma: 12.8967 at sigma = 2. Make sure learners set sigma back to 1.'),
                   ('Step 5: cross-entropy', 'Binary cross-entropy 0.2990. The spreadsheet computes it row by row. The CHANGE task (0.3 to 0.9) raises the loss sharply.'),
                   ('Step 6: MAP and shrinkage', 'MAP is 0.6 and the unnormalised posterior at 0.6 is 0.0071664. Weights 2.0357, 1.9, 1.5, 1.0179.'),
                   ('Step 7: bias-variance (Python only)', 'Expected errors 0.319, 0.127, 0.915. Degree 9 has the largest variance. Spreadsheet learners add up the three results on the Bias-variance sheet.')],
        rescue=['If concepts run over, skip the table of eight measurements and say that the best mu equals the average.', 'If lab time is short, do Steps 1 to 4 and the MAP step. Leave the bias-variance simulation for home.',
                'If the log of a product confuses someone, show 0.5 ** 1100 in Python and let the number speak.'],
        after=['Share the notebook and the workbook again for absent learners.', 'Note any question you could not answer and open Session 17 with it.', 'Remind learners that Session 17 uses the cross-entropy from today.'],
        lab_answer_key=[['Python Step 1 PREDICT: which theta is most likely?', '0.7, because 7 heads in 10 flips.'], ['Step 1 READ: same as k / n?', 'Yes: 7 / 10 = 0.7.'],
                        ['Step 1 CHANGE: all heads', 'The maximum moves to the last grid value, 0.9, because the grid stops there (k / n would be 1). MLE trusts the data too much when there are few of them.'],
                        ['Step 2 PREDICT: 0.5 ** 1100', '0.0, the product underflows.'], ['Step 3 READ: why the average?', 'The average minimises the sum of squared deviations, which is what the Gaussian log-likelihood measures.'],
                        ['Step 3 CHANGE: sigma = 2', 'The best mu does not move. The curve gets flatter and wider, and the Step 4 gap is 12.8967 in every row. Then sigma goes back to 1.'], ['Step 4 READ: what does the constant say?', 'The two curves differ only by a constant, so they peak at the same mu.'],
                        ['Step 5 CHANGE: 0.3 to 0.9', 'The loss rises from 0.299 to about 0.786 nats: a confident wrong answer is expensive.'],
                        ['Step 6 PREDICT: where does the posterior peak?', 'Below 0.7, at 0.6, because the prior favours a fair coin.'], ['Step 6 READ: as lambda grows?', 'w gets smaller. A very sure prior near zero shrinks w to about 0.'],
                        ['Step 7 PREDICT: bias and variance', 'Degree 1 has the largest bias, degree 9 the largest variance.'], ['Step 7 CHANGE: noise 0.6', 'Degree 9 gets worse fastest because it follows the noise.']])
    return s
