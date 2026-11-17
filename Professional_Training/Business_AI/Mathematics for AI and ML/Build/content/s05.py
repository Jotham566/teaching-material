"""Session 5: Eigenvalues and eigenvectors. Directions a matrix only stretches, the 2 by 2 characteristic equation, the covariance matrix, power iteration."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'kit'))
import diagrams_math_b as MB  # noqa: E402


def build():
    d = MB.d5()
    C, lam, v1, v2 = d['C'], d['lam'], d['v1'], d['v2']
    ca, cb = d['ca'], d['cb']
    mm, mp = d['mm'], d['mp']
    n = d['n']
    g = lambda v, k=2: f'{v:.{k}f}'
    gm = lambda v, k=1: f'{v:.{k}f}'.replace('-', '−')
    gi = lambda v: f'{v:.0f}'
    pts = [(float(a), float(b)) for a, b in zip(ca, cb)]
    sa2, sb2, sab = float((ca ** 2).sum()), float((cb ** 2).sum()), float((ca * cb).sum())
    T, D = d['T'], d['D']
    root = (T * T - 4 * D) ** 0.5
    pa, pc = d['pa'], d['pc']
    fmt_i = lambda arr: ', '.join(gi(v).replace('-', '−') for v in arr)
    fmt_raw = lambda arr: ', '.join(gi(v) for v in arr)
    clock = [(10, 'Recall, then a real question from AI'), (35, 'Concept: picture, then a hand example'), (10, 'Break'), (45, 'Lab: predict, run, change one thing'),
             (15, 'Where it appears in AI, plus an exit check'), (5, 'Save the work')]

    s = dict(
        num=5, block='Linear algebra', short_title='Eigenvalues and eigenvectors',
        title='Eigenvalues and eigenvectors: the directions a matrix only stretches',
        question='In a table with many columns, which directions do the data vary along most, and how do we look at embeddings with hundreds of numbers?',
        outcomes=['Say what an eigenvector and an eigenvalue are, with a picture of a matrix acting on a circle',
                  'Find the eigenvalues and eigenvectors of a 2 by 2 matrix by hand and check them with trace and determinant',
                  'Build a covariance matrix, find its top direction, and use power iteration to find it by repeated multiplying'],
        outcome_icons=['magnifier', 'calculator', 'chart'],
        outcome_note=('By the end of today you can say what an eigenvector and an eigenvalue are, using a picture of a matrix acting on a circle. '
                      'You can find them by hand for a two by two matrix, and check them with the trace and the determinant. '
                      'And you can build a covariance matrix from data, find the direction in which the data varies most, and find it again by repeated multiplication, called power iteration. Which of those three sounds the hardest to you?'),
        clock=clock, plan_title='Your two hours: stretch directions, then data', plan_caption='Ideas first, with pictures. Then the lab in Python or in a spreadsheet. Then where it shows up in AI.',
        plan_note=('We have two hours. Ten minutes to bring back Session 4 and set the question of the day. Thirty-five minutes of ideas, each as a picture and then a small calculation by hand. '
                   'A ten minute break. Then forty-five minutes of lab, in Python or a spreadsheet, on the same numbers. We end with where this appears in AI tools, an exit check, and five minutes to save.'),
        recall_from='Session 4',
        recall=[('What does a determinant of 0 tell you about a matrix?', 'It squashes the plane onto a line or a point. It has no inverse and its rank is below full.'),
                ('Write the normal equation for fitting a line.', 'XᵀX w = Xᵀy. It gives the weights w with the smallest squared error.'),
                ('What is the rank of the matrix with rows (1, 2) and (2, 4)?', '1. The second column is twice the first, so the columns give only one direction.')],
        words=[('Eigenvector', 'A direction that a matrix only stretches, flips or squashes. It stays on its own line.'),
               ('Eigenvalue', 'The factor by which an eigenvector is stretched. Written with the Greek letter lambda (λ).'),
               ('Trace', 'The sum of the diagonal entries of a square matrix.'),
               ('Covariance matrix', 'A table of how every pair of features varies together. The diagonal holds each feature\'s variance, the typical squared distance from its mean.'),
               ('Power iteration', 'Multiplying by a matrix again and again to find its top eigenvector.')],
        word_icons=['magnifier', 'flag', 'calculator', 'grid', 'gear'],
        words_note=('Five words. An eigenvector is a direction that a matrix only stretches, flips or squashes, so it stays on its own line. The eigenvalue is the factor, written with the Greek letter lambda. '
                    'The trace is the sum of the diagonal entries. A covariance matrix is a table of how every pair of features varies together, and we build it by hand today, starting from the mean and the variance. And power iteration means multiplying by a matrix again and again to find its top eigenvector. '
                    'These are the real names you will meet in documentation, so we use them from now on.'),
        keep='Keep the saved lab and four numbers: eigenvalues 3 and 1 for the small matrix, and 102 and 2 for the covariance matrix of the eight marks.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Saved lab', value='Notebook or workbook, saved'), dict(label='Small matrix', value='Eigenvalues 3 and 1'),
                                                            dict(label='Covariance matrix', value='Eigenvalues 102 and 2'), dict(label='Next session', value='SVD and PCA')]),
        keep_title='Save the lab and keep the four eigenvalues',
        next='Session 6: singular value decomposition and PCA, which build on today.', next_label='Next session',
        keep_note=('Before you go, save your work with all checks green. Keep four numbers: eigenvalues three and one for the small matrix, and one hundred two and two for the covariance matrix of the eight marks. '
                   'Next session we break any matrix into rotate, stretch, rotate, and we use the covariance matrix you built today to reduce two dimensions to one. Write down any question for next time.'),
        cover_note=('Welcome to Session 5. Last time we solved systems and learned that a determinant of zero is a warning. Today we ask a gentler question about a matrix: are there directions it only stretches? '
                    'The answer turns out to describe where data varies most, and that is the idea behind principal component analysis, which we meet next session.'),
        slides=[])
    S = s['slides']

    S.append(dict(kind='table', title='Answers to the three questions from Session 4', headers=['Question', 'Short answer'], rows=[[q, a] for q, a in s['recall']], widths=[5.6, 6.4], icons=False,
                  note='If one surprised you, look back at Session 4 before the lab. Rank and determinant return today.',
                  notes=('A determinant of zero means the matrix squashes the plane onto a line or a point, so it has no inverse and its rank is below full. '
                         'The normal equation is X transpose X times w equals X transpose y, and it gives the weights with the smallest squared error. '
                         'The matrix with rows one, two and two, four has rank one, because its second column is twice the first, so the columns give only a single direction. '
                         'If one of these surprised you, look at Session 4 again before the lab.')))

    S.append(dict(kind='idea', title='Most arrows turn when a matrix acts on them, but a few directions only stretch',
                  visual=dict(kind='eigpic_v', A=((2, 1), (1, 2))),
                  lead='The matrix with rows (2,\u00a01) and (1,\u00a02) turns a circle into an ellipse. The grey arrow u turns.',
                  points=['v₁ points along (1, 1) and becomes 3 times longer.', 'v₂ points along (1, −1) and keeps its length.', 'Such directions are eigenvectors.'],
                  notes=('Picture a matrix acting on every arrow that starts at the origin and has length one, the unit circle. Our matrix has rows two, one and one, two. It turns the circle into an ellipse. '
                         'Most arrows, like the grey arrow u, get turned to a new direction. But two special directions stay on their own lines. The red arrow v one, along one, one, becomes three times longer. The black arrow v two, along one, minus one, keeps its length. '
                         'Those special directions are called eigenvectors. The ellipse is longest along one dashed line and shortest along the other, and that is no accident: the longest stretch happens along an eigenvector.')))

    S.append(dict(kind='formula', title='An eigenvector v and its eigenvalue λ satisfy Av = λv',
                  formulas=[('Definition', r'$A\mathbf{v} = \lambda\mathbf{v}$'), ('Our first pair', r'$A\,(1,1) = (3,3) = 3\,(1,1)$')],
                  symbols=[['A', 'A square matrix. Here the rows are (2, 1) and (1, 2).', '2 by 2'],
                           ['v', 'An eigenvector: a nonzero vector whose direction A keeps.', '(1, 1) or (1, −1)'],
                           ['λ', 'The eigenvalue (Greek letter lambda): the factor by which A stretches v.', '3 for (1, 1), and 1 for (1, −1)'],
                           ['Av', 'Matrix times vector. For (1, 1): (2 + 1, 1 + 2).', '(3, 3)']],
                  widths=[1.7, 6.0, 4.2], size=26, note='A negative λ flips v. A λ of 0 squashes it to the origin. Any multiple of v is an eigenvector too.',
                  notes=('The definition fits on one line: A times v equals lambda times v. It says: when A acts on v, the result is the same vector scaled by a number. That number lambda is the eigenvalue. '
                         'For our matrix, take v equal to one, one. A times v gives two plus one, which is three, and one plus two, which is three. So A v is three, three, which is three times v. The eigenvalue is three. '
                         'Any multiple of v works as well, so we care about the direction. Check the table row by row, and say each symbol aloud.')))

    S.append(dict(kind='table', title='Testing four arrows by hand: only two directions survive', headers=['Arrow v', 'Av', 'Same line as v?', 'Stretch factor'],
                  rows=[['(1, 0)', '(2, 1)', 'No, it turned', 'none'], ['(1, 1)', '(3, 3)', 'Yes', '3'], ['(1, -1)', '(1, −1)', 'Yes', '1'], ['(1, 2)', '(4, 5)', 'No, it turned', 'none']],
                  widths=[2.6, 2.6, 3.8, 2.8], icons=False,
                  note='A has rows (2, 1) and (1, 2). Compute Av with a dot product for each row: for (1, 2) it is 2 + 2 = 4 and 1 + 4 = 5.',
                  notes=('Try four arrows by hand. For one, zero, A v is two, one, a new direction, so it turned. For one, one we get three, three: same line, stretched by three. '
                         'For one, minus one we get one, minus one: the same arrow, a stretch of one. For one, two we get four, five, which is not a multiple of one, two, so it turned. '
                         'Two directions survive. A two by two matrix has at most two different eigenvalues, and when the two eigenvalues differ, as here, there are two eigen-directions. A matrix like two times the identity keeps every direction, so do not say at most two directions.')))

    S.append(dict(kind='wide', title='The eigenvalue says whether the arrow is stretched, shrunk, flipped or squashed',
                  visual=dict(kind='lambdas'),
                  caption='Grey arrow: an eigenvector. Red arrow: what A turns it into. λ (lambda) is the multiplier.',
                  notes=('Reading an eigenvalue takes one look. The grey arrow is an eigenvector. The red arrow is what A turns it into, and lambda is the multiplier. '
                         'Lambda two doubles the arrow. Lambda one half halves it. Lambda one leaves it alone. Lambda minus one flips it to the opposite direction, but keeps its length. '
                         'And lambda zero squashes it to nothing, which is the determinant zero case from last session. In fact the determinant is the product of the eigenvalues, as we will see shortly.')))

    S.append(dict(kind='steps', title='To find eigenvalues, ask when A - λI has no inverse',
                  steps=[dict(head='Start', text='Av = λv', icon='flag'), dict(head='Rearrange', text='(A − λI)v = 0', icon='gear'),
                         dict(head='Need v not zero', text='So A − λI must have no inverse', icon='lock'), dict(head='Result', text='det(A − λI) = 0', icon='check')], highlight=3,
                  caption='λI has λ on the diagonal. If A − λI had an inverse, multiplying (A − λI)v = 0 by it would give v = 0. So no inverse: determinant 0 (Session 4).',
                  notes=('Finding the eigenvalues starts from the definition. Start with A v equals lambda v. Move everything to one side: A minus lambda I, times v, equals zero, where I is the identity matrix. '
                         'We want a v that is not the zero vector. If A minus lambda I had an inverse, multiplying by it would force v to be zero. So A minus lambda I must have no inverse, and from Session 4 that means its determinant is zero. '
                         'The determinant of A minus lambda I equals zero is called the characteristic equation. The identity is there because we cannot subtract a number from a matrix: lambda I puts lambda on the diagonal.')))

    S.append(dict(kind='example', title='Writing det(A - λI) = 0 out for our matrix',
                  scenario='A has rows (2, 1) and (1, 2). We subtract λ from each diagonal entry and take the determinant.',
                  blocks=[dict(label='A - λI', text='Rows (2 − λ, 1) and (1, 2 − λ).'),
                          dict(label='Determinant', text='(2 − λ)(2 − λ) − 1 × 1 = 4 − 4λ + λ² − 1 = λ² − 4λ + 3.'),
                          dict(label='Set it to 0', text='λ² − 4λ + 3 = (λ − 3)(λ − 1) = 0, so λ = 3 or λ = 1.'),
                          dict(label='Any 2 by 2', text='The same steps give λ² − Tλ + D = 0, with T the sum of the diagonal and D the determinant.', red=True)],
                  notes=('Write it out for our matrix. Subtract lambda from each diagonal entry. The rows become two minus lambda, one, and one, two minus lambda. '
                         'The determinant is two minus lambda, times two minus lambda, minus one times one. Expand the brackets: four, minus four lambda, plus lambda squared, then minus one. That tidies to lambda squared, minus four lambda, plus three. '
                         'Set that to zero. It factors as lambda minus three, times lambda minus one, so lambda is three or one. These are the same eigenvalues we found by testing arrows. '
                         'The last line says the same steps work for any two by two matrix, and the general form comes straight after this.')))

    S.append(dict(kind='formula', title='For any 2 by 2 matrix the characteristic equation is a quadratic',
                  formulas=[('Characteristic equation', r'$\lambda^{2} - T\lambda + D = 0$'), ('Eigenvalues', r'$\lambda = \frac{T \pm \sqrt{T^{2} - 4D}}{2}$')],
                  symbols=[['T', 'The trace: the sum of the diagonal entries, a₁₁ + a₂₂.', '2 + 2 = 4'], ['D', 'The determinant: a₁₁a₂₂ − a₁₂a₂₁ (aᵢⱼ is row i, column j of A).', '2 × 2 − 1 × 1 = 3'],
                           ['±', 'Plus gives one eigenvalue, minus gives the other.', '(4 + 2) / 2 and (4 − 2) / 2'], ['λ', 'The two eigenvalues.', '3 and 1']],
                  widths=[1.4, 6.4, 4.1], size=26, note='Check: the eigenvalues add up to the trace (3 + 1 = 4) and multiply to the determinant (3 × 1 = 3).',
                  notes=('Expanding the determinant of A minus lambda I for any two by two matrix gives the quadratic you just saw: lambda squared, minus T lambda, plus D equals zero. '
                         'T is the trace, the sum of the diagonal, a one one plus a two two, and D is the determinant, a one one times a two two, minus a one two times a two one. The quadratic formula then gives lambda equals T plus or minus the square root of T squared minus four D, all over two. '
                         'For our matrix T is four and D is three, so the square root is two and lambda is three or one. Notice the check at the bottom: the eigenvalues add to the trace and multiply to the determinant. '
                         'In the spreadsheet you will type this formula into cells.')))

    S.append(dict(kind='example', title='Worked example: eigenvalues and eigenvectors of our matrix',
                  scenario='A has rows (2, 1) and (1, 2). We find λ first, then an eigenvector (s, t) for each λ.',
                  blocks=[dict(label='Eigenvalues', text='λ² − 4λ + 3 = 0. So λ = (4 + 2) / 2 = 3 or λ = (4 − 2) / 2 = 1.'),
                          dict(label='For λ = 3', text='A − 3I has rows (−1, 1) and (1, −1). The equation −s + t = 0 gives s = t, so v₁ = (1, 1).'),
                          dict(label='For λ = 1', text='A − I has rows (1, 1) and (1, 1). The equation s + t = 0 gives v₂ = (1, −1).'),
                          dict(label='Check', text='A (1, 1) = (3, 3) and A (1, −1) = (1, −1). Both match.', red=True)],
                  notes=('The whole recipe runs in three moves. The quadratic is lambda squared, minus four lambda, plus three, so lambda is three or one. '
                         'We look for an eigenvector with entries s and t. For lambda three, subtract three from the diagonal, giving rows minus one, one and one, minus one. Both rows say minus s plus t equals zero, so s equals t, and v one is one, one. '
                         'For lambda one, subtract one from the diagonal, giving rows one, one and one, one, so s plus t is zero, and v two is one, minus one. The last line checks both by multiplying. '
                         'The two rows are multiples of each other every time, because A minus lambda I has no inverse at an eigenvalue. That was the whole point of the last two slides.')))

    S.append(dict(kind='wide', title='Centring: subtract each feature\'s mean so the cloud sits on the origin',
                  visual=dict(kind='centre', raw=[(float(a), float(b)) for a, b in zip(d['maths'], d['phys'])], mean=(mm, mp)),
                  caption=f'Eight students (illustrative). Mean maths {gi(mm)}, mean physics {gi(mp)}. Each mark minus its mean.',
                  notes=(f'Real data next. Eight students, each with a maths mark and a physics mark, invented to show the arithmetic. The left picture shows the raw marks, with the mean of maths at {gi(mm)} and the mean of physics at {gi(mp)}. '
                         'The first step of almost every method in this part of the course is centring: subtract each feature\'s mean from its column. The shape of the cloud does not change, but now its centre sits at the origin. '
                         'The cloud runs from bottom left to top right, which says high maths marks go with high physics marks. The next slides turn that tilt into numbers.')))

    S.append(dict(kind='formula', title='Mean, variance and covariance measure the centre, the spread and the tilt',
                  formulas=[('Variance (sample)', r'$\mathrm{var}(x) = \frac{1}{n-1}\sum_{i=1}^{n}(x_i-\bar{x})^{2}$'),
                            ('Covariance (sample)', r'$\mathrm{cov}(x,y) = \frac{1}{n-1}\sum_{i=1}^{n}(x_i-\bar{x})(y_i-\bar{y})$')],
                  symbols=[['n, xᵢ, yᵢ', 'n students; xᵢ and yᵢ are the marks of student i. Σ adds them up.', f'{n} students'],
                           ['x̄ (x-bar)', 'The mean: (x₁ + ... + xₙ) / n. Later sessions also write it μ.', f'{gi(mm)} and {gi(mp)}'],
                           ['var, cov', 'Variance: typical squared distance from the mean. Covariance: positive when both rise together.', '66, 38; 48'],
                           ['n - 1', 'Distances to a mean taken from the same data come out a little small; n − 1 corrects that.', 'divide by 7']],
                  widths=[2.0, 6.6, 3.3], size=18, note='Sample version: np.cov, VAR.S, COVARIANCE.S. Dividing by n gives 57.75, 33.25, 42. Session 13 returns to this.',
                  notes=('Three short formulas describe a cloud of data. The mean is the centre: add the values and divide by n. The variance is the spread: square each distance from the mean, add, and divide by n minus one. '
                         'The covariance is the tilt: multiply the two distances for each student, add, and divide by n minus one. It is positive when the two marks rise together. '
                         'Why n minus one? The mean was worked out from the same eight marks, so the data sit a little closer to it than to the true centre, and the squared distances come out a little small. Dividing by n minus one corrects that. This is called the sample version, and it is what numpy and the dot S spreadsheet functions use. Session 13 returns to it.')))

    S.append(dict(kind='example', title='Worked by hand: the covariance matrix of the eight marks',
                  scenario='Illustrative marks. Centred = mark minus its mean. In matrix form C = Xcᵀ Xc / (n − 1), with Xc the centred marks.',
                  blocks=[dict(label='Maths marks', text=f'{fmt_raw(d["maths"])}. Mean {gi(mm)}. Centred: {fmt_i(ca)}.'), dict(label='Physics marks', text=f'{fmt_raw(d["phys"])}. Mean {gi(mp)}. Centred: {fmt_i(cb)}.'),
                          dict(label='Sums', text=f'Squared centred maths marks add to {gi(sa2)}, physics to {gi(sb2)}. Maths times physics: {gi(sab)}.'),
                          dict(label='Divide', text=f'Divide by n − 1 = {n - 1}. Variances {gi(C[0, 0])} and {gi(C[1, 1])}. Covariance {gi(C[0, 1])}. So C has rows ({gi(C[0, 0])}, {gi(C[0, 1])}) and ({gi(C[1, 0])}, {gi(C[1, 1])}).', red=True)],
                  notes=(f'Do it once by hand. The mean of the maths marks is {gi(mm)} and the mean of the physics marks is {gi(mp)}. Subtract each mean from its column, giving the two lists of centred values. '
                         f'Square each centred maths value and add: {gi(sa2)}. Do the same for physics: {gi(sb2)}. Multiply each pair and add: {gi(sab)}. Divide each by seven, which is n minus one. '
                         f'The variances are {gi(C[0, 0])} and {gi(C[1, 1])}, and the covariance is {gi(C[0, 1])}. Arranged in a table, these give the covariance matrix C, with variances on the diagonal and the covariance off it. '
                         'C is symmetric, and its positive covariance matches the tilt we saw in the picture.')))

    S.append(dict(kind='idea', title='The eigenvectors of the covariance matrix are the directions of the cloud',
                  visual=dict(kind='cloud', points=pts, axes=[dict(v=tuple(float(t) for t in v1), len=12.5, label='principal component 1', at=0.5, ha='left', dx=0.15, dy=-0.45), dict(v=tuple(float(t) for t in v2), len=9, label='component 2', color=MB.INK, dy=0.3)],
                              xlabel='Centred maths mark (across) and centred physics mark (up)'),
                  lead='Centred students. Red: the top eigenvector v₁ of C. Black: v₂.',
                  points=[f'v₁ = ({gm(v1[0])}, {gm(v1[1])}), variance {gi(lam[0])}: the direction of greatest spread, called the first principal component (Session 6).', f'v₂ = ({gm(v2[0])}, {gm(v2[1])}): variance {gi(lam[1])}.', 'Each eigenvalue is the variance along its eigenvector.'],
                  notes=('This is the payoff. Draw the centred students, and draw the eigenvectors of their covariance matrix. The red arrow, v one, points along the long axis of the cloud. That is the direction in which the data vary most, and it has a name: the first principal component. Principal component analysis, next session, is built on it. '
                         f'The black arrow, v two, is at right angles, along the short axis, where the dots barely spread. For an eigenvector of length one, the eigenvalue tells you how much spread: along the red direction the variance is {gi(lam[0])}, and along the black one only {gi(lam[1])}. '
                         'So the eigenvectors of the covariance matrix are the natural axes of the data.')))

    S.append(dict(kind='example', title='Worked by hand: eigenvalues and top eigenvector of C',
                  scenario='C has rows (66, 48) and (48, 38). We use the 2 by 2 formulas from earlier.',
                  blocks=[dict(label='Trace and determinant', text=f'T = 66 + 38 = {gi(T)}. D = 66 × 38 − 48 × 48 = {gi(D)}.'),
                          dict(label='Eigenvalues', text=f'The square root of {gi(T)}² − 4 × {gi(D)} is {gi(root)}. So λ = ({gi(T)} + {gi(root)}) / 2 = {gi(lam[0])} or ({gi(T)} − {gi(root)}) / 2 = {gi(lam[1])}.'),
                          dict(label='Top eigenvector', text='C − 102I has rows (−36, 48) and (48, −64). So −36s + 48t = 0, which gives t = 0.75s. Take (4, 3). Length 5, so v₁ = (0.8, 0.6).'),
                          dict(label='Share of variance', text=f'{gi(lam[0])} / {gi(lam[0] + lam[1])} = {g(100 * d["explained"], 1)} percent of all the variance lies along direction 1.', red=True)],
                  notes=(f'The same recipe works on the covariance matrix. Trace {gi(T)}, determinant {gi(D)}. The square root part is the square root of {gi(T * T - 4 * D)}, which is {gi(root)}. So the eigenvalues are {gi(lam[0])} and {gi(lam[1])}. '
                         'For the top eigenvector, subtract one hundred two from the diagonal. The first row says minus thirty-six s plus forty-eight t equals zero, so t is three quarters of s. Take four, three, and divide by its length five to get zero point eight, zero point six. '
                         f'Finally one hundred two out of one hundred four is {g(100 * d["explained"], 1)} percent. Almost all the spread of the eight students lies along one direction.')))

    S.append(dict(kind='formula', title='Power iteration finds the top eigenvector by repeated multiplying',
                  formulas=[('Update', r'$\mathbf{g}_{k+1} = \frac{A\,\mathbf{g}_k}{\max|A\,\mathbf{g}_k|}$'), ('Eigenvalue estimate', r'$\lambda \approx \max|A\,\mathbf{g}_k|$')],
                  symbols=[['gₖ', 'The guess after k steps. Almost any start works.', 'g₀ = (1, 0) here'], ['Agₖ', 'Multiply the guess by the matrix.', 'one matrix times vector product'],
                           ['max |.|', 'The entry with the largest size. Dividing by it keeps numbers small.', 'gₖ has largest entry 1'], ['λ', 'Top eigenvalue: max|Agₖ| estimates it because gₖ has largest entry 1.', 'estimate tends to 3']],
                  widths=[1.8, 6.4, 3.7], size=22, note='It works when one eigenvalue is largest in size. When the top two are nearly equal in size, it converges slowly.',
                  notes=('Power iteration is the simplest way to find the top eigenvector by computer, and it only needs matrix times vector. Start with any guess, called g zero. Multiply it by A. '
                         'Divide the result by its largest entry so the numbers do not grow. Repeat. Each multiplication stretches the top direction a little more than the others, so after a few rounds the top direction wins. '
                         'Because the guess always has largest entry one, the largest entry after multiplying estimates the eigenvalue. '
                         'It needs one eigenvalue that is clearly the largest in size. That is usually the case for covariance matrices, and when the top two are nearly equal it is slow.')))

    S.append(dict(kind='idea', title='Each multiplication swings the arrow closer to the top eigen-direction',
                  visual=dict(kind='power', A=((2, 1), (1, 2)), v0=(1, 0), nsteps=4),
                  lead='Matrix with rows (2, 1) and (1, 2). Start at g₀ = (1, 0). Multiply, then divide by the largest entry.',
                  points=[f'g₁ = (1, {g(pa[1][1][1])}), g₂ = (1, {g(pa[2][1][1])}), g₄ is almost (1, 1).', f'The estimates of λ are {", ".join(g(r[3], 2) for r in pa)}. They head to 3.'],
                  notes=(f'Watch it happen on the small matrix. Start at the arrow g zero, one, zero. Multiplying by A gives two, one. Divide by two: g one is one, and one half. Multiply again: two point five, two. Divide: g two is one, point eight. '
                         f'The arrows swing towards the one, one direction, which is the eigenvector for lambda three. The estimates of the eigenvalue, the largest entries before dividing, are {", ".join(g(r[3], 2) for r in pa)}, heading to three. '
                         'The first step moves the arrow most, because that is when the unwanted direction is largest. After a handful of steps the arrow is almost on the dashed line.')))

    S.append(dict(kind='table', title='Power iteration by hand on the covariance matrix C', headers=['Step k', 'Guess gₖ', 'C gₖ', 'Largest entry'],
                  rows=[[str(r[0]), f'({g(r[1][0], 3)}, {g(r[1][1], 3)})', f'({g(r[2][0], 1)}, {g(r[2][1], 1)})', g(r[3], 2)] for r in pc],
                  widths=[1.6, 3.4, 3.8, 3.0], icons=False,
                  note=f'This time the start is g₀ = (0, 1), to show that any start works. After 6 multiplications (row k = 5) the estimate is {g(pc[-1][3], 1)}, close to {gi(lam[0])}, and the guess is near (1, 0.75), which is (0.8, 0.6) at length 1.',
                  notes=('Power iteration on the covariance matrix starts somewhere else on purpose, at g zero equal to zero, one, to show that the start does not matter. Multiplying by C gives forty-eight, thirty-eight, and we divide by forty-eight. '
                         'The next guess is one, point seven nine. Multiply again, divide again, and by step three the guess is already very close to one, point seven five. '
                         'The largest entry, our estimate of the eigenvalue, settles near one hundred two. The second eigenvalue is only two, so each step shrinks the unwanted part by a factor of about fifty, and convergence is fast. '
                         'In the spreadsheet you will build this table in rows of cells.')))

    S.append(dict(kind='table', title='Four things people get wrong about eigenvectors', headers=['Mistake', 'What is true', 'What to do'],
                  rows=[['Treating an eigenvector as one fixed arrow', 'Any multiple, and the opposite arrow, is also an eigenvector.', 'Quote a unit-length version. Expect sign flips between tools.'],
                        ['Looking for eigenvalues of a non-square matrix', 'Only square matrices have them.', 'Use the SVD for other shapes (Session 6).'],
                        ['Expecting real eigenvalues always', 'A quarter-turn rotation has no real eigenvalues, because every arrow turns.', 'Covariance matrices are symmetric and always give real ones.'],
                        ['Mixing up the two outputs', 'For a covariance matrix, the eigenvalue is the spread along its eigenvector.', 'Quote both together.']],
                  widths=[3.7, 4.3, 3.9], icons=['cross', 'cross', 'cross', 'cross'],
                  notes=('Four things to remember. First, an eigenvector is a direction, and any multiple of it works, including the opposite arrow. So two tools can give the same eigenvector with opposite signs, and both are right. '
                         'Second, eigenvalues belong to square matrices only. For other shapes we use the singular value decomposition next session. '
                         'Third, a quarter-turn rotation has no real eigenvalues, because every arrow turns. Covariance matrices are symmetric, which guarantees real eigenvalues. '
                         'Fourth, keep the roles straight: for a covariance matrix the eigenvalue is how much spread, the eigenvector is which direction.')))

    S.append(dict(kind='code', title='Centre, divide by n - 1, then eigh: the covariance route in five lines',
                  code='Xc = X - X.mean(axis=0)\nC = Xc.T @ Xc / (len(X) - 1)\nvalues, vectors = np.linalg.eigh(C)\ng = np.array([0.0, 1.0])\nfor k in range(6):\n    Cg = C @ g\n    est = np.max(np.abs(Cg))\n    g = Cg / est',
                  reads=['Xc = ... centres each column by subtracting its mean.', 'C = ... is the covariance matrix, dividing by n − 1 (the same as np.cov(X.T)).', 'eigh is for symmetric matrices. It lists eigenvalues from smallest to largest, with eigenvectors in the columns.',
                         'The loop from g = ... is power iteration. est holds the eigenvalue estimate.'],
                  notes=('The code follows the slides line by line. Subtract the column means to centre. Form the covariance matrix with X c transpose times X c over n minus one, which is what np dot cov gives too. '
                         'Then np dot linalg dot eigh returns the eigenvalues and the eigenvectors. The letters e, i, g, h are for symmetric matrices, which covariance matrices always are. '
                         'It lists the eigenvalues from smallest to largest, and the eigenvectors are the columns. Below is power iteration in a short loop: multiply, find the largest entry, divide. '
                         'You do not need to memorise it, since the notebook explains every line.')))

    S.append(dict(kind='divider', title='Part 2: the lab', lead='Close the slides. Open the notebook or the workbook.', section='Lab',
                  notes=('That is the end of the ideas. In the lab you compute eigenvalues three ways: by the formula, with a library, and by power iteration. Choose the Python notebook or the spreadsheet workbook. '
                         'The numbers are identical in both, and each step ends with an automatic check. A spreadsheet has no eigenvalue function in Excel or Google Sheets, so there you build the formula and the iteration rows yourself. '
                         'Predict, run, read, then change one thing. Raise your hand when a check stays red.')))

    S.append(dict(kind='steps', title='Six lab steps: one arrow, two formulas, then the marks of eight students',
                  steps=[dict(head='1 Test', text='Does A keep the direction of (1, 1)?', icon='magnifier'), dict(head='2 Formula', text='Eigenvalues from trace and determinant', icon='calculator'),
                         dict(head='3 Library', text='eigh in Python. The sheet has no such function.', icon='gear'), dict(head='4 Covariance', text='Centre the marks, build C', icon='grid'),
                         dict(head='5 Top direction', text='Eigenvalues, eigenvector, share of variance', icon='chart'), dict(head='6 Power', text='Repeat C v and watch the guess settle', icon='clock')], highlight=4,
                  caption='Python uses numpy. The spreadsheet uses MMULT, VAR.S, COVARIANCE.S, SQRT and rows of cells. Gold cells are yours.',
                  notes=('The map has six steps. Step one, test whether A keeps the direction of one, one. Step two, find the eigenvalues from trace and determinant. '
                         'Step three, Python only: check with a library function. The spreadsheet has none, so the formula is the tool. '
                         'Step four, centre the eight marks and build the covariance matrix. Step five, find its eigenvalues, the top eigenvector and the share of variance. Step six, power iteration in rows of cells. '
                         'Predict each answer before you look.')))

    S.append(dict(kind='table', title='Check your lab against 3 and 1, then C, then 102 and 2', headers=['What you compute', 'You should see'],
                  rows=[['A times (1, 1) for the small matrix', '(3, 3)'], ['Eigenvalues of the small matrix', '3 and 1'], ['Covariance matrix C of the eight marks (divide by n − 1)', f'rows ({gi(C[0, 0])}, {gi(C[0, 1])}) and ({gi(C[1, 0])}, {gi(C[1, 1])})'],
                        ['Eigenvalues of C', f'{gi(lam[0])} and {gi(lam[1])}'], ['Top eigenvector of C, unit length', f'({g(v1[0], 1)}, {g(v1[1], 1)})'], ['Share of variance along direction 1', f'{g(d["explained"], 3)}'],
                        ['Power iteration after 6 multiplications (row k = 5): largest entry', g(pc[-1][3], 1)], ['Covariance if physics is replaced by 100 minus physics', f'−{gi(C[0, 1])}: the sign flips, the size stays']],
                  widths=[7.0, 4.2], icons=['calculator', 'flag', 'grid', 'chart', 'chart', 'bars', 'gear', 'switch'],
                  note='If a number differs, stop and find the step that went wrong. The sign of an eigenvector may differ between tools.',
                  notes=('Use this as your checkpoint. If your numbers match, carry on. If they do not, stop and call me over. The usual causes are dividing by n instead of n minus one, forgetting to centre, and mixing up the order of the two features. '
                         'An eigenvector may come out with the opposite sign in a different tool, and that is fine. '
                         'The notebook checks the absolute values for that reason. Please do not type a number just to make a check pass.')))

    S.append(dict(kind='table', title='Minus signs, ordering and centring explain most lab surprises', headers=['Error or symptom', 'What it says', 'What to do'],
                  rows=[['The eigenvector has a minus sign', 'The opposite arrow is also an eigenvector.', 'Compare absolute values, or flip the sign.'], ['Eigenvalues come out in the wrong order', 'eigh lists smallest first.', 'Reverse the list or sort it.'],
                        ['Covariance far too large', 'The data were not centred first.', 'Subtract the column means.'], ['#NUM! in the spreadsheet', 'The square root of a negative number.', 'Check T² − 4D. For covariance it is never negative.']],
                  widths=[3.8, 4.1, 4.0], icons=['cross', 'key', 'bell', 'flag'],
                  notes=('Four things will happen to someone in the room. A minus sign on an eigenvector is not an error, because the opposite arrow is also an eigenvector. '
                         'If the eigenvalues come out in the wrong order, remember that eigh lists the smallest first. '
                         'If your covariance is far too big, you did not centre the data. And a number error in the spreadsheet means a negative number under the square root, so check T squared minus four D. '
                         'Read the last line of any message first.')))

    S.append(dict(kind='wide', title='Where this appears in AI: PCA turns embeddings into a map you can look at',
                  visual=dict(kind='embedmap'),
                  caption='PCA (principal component analysis) of made-up 4-number vectors. Real embeddings are far longer.',
                  notes=('Language models of this kind turn words and passages into embeddings, which are lists of numbers. To look at them, people project them down to two directions. '
                         'The method is principal component analysis, or PCA, and it is the one you just learned: centre the vectors, form the covariance matrix, take the two eigenvectors with the largest eigenvalues, and plot each vector\'s position along them. '
                         'On the right, three clusters appear, animals, vehicles and foods. The vectors here are made up to show the idea, with four numbers each. Real embeddings are much longer, but the mathematics is the same.')))

    S.append(dict(kind='list', title='Where this appears in AI: looking at what models learn',
                  items=['PCA keeps the top eigenvectors of the covariance matrix of the data.', 'The Embedding Projector, published by Google researchers in 2016, offers PCA to view embeddings.',
                         'Open-weight models such as Llama publish their weights, so this analysis can be run on them.', 'Closed assistants do not publish their internal embedding tables. The vectors a public embedding service returns for your own text can be projected the same way.'],
                  icons=['chart', 'magnifier', 'folder', 'lock'],
                  notes=('Three facts about where this shows up. First, principal component analysis is the top eigenvectors of the covariance matrix, which you have now computed by hand. '
                         'Second, published tools such as the Embedding Projector, described by Google researchers in 2016, offer PCA to look at embeddings in two or three dimensions. '
                         'Third, open-weight models such as Llama publish their weights, so anyone can run this analysis on them. The internal embedding tables of closed assistants are not published, so we cannot draw them. But the vectors that a public embedding service returns for your own text can be projected in the same way.')))

    S.append(dict(kind='practice', title='Where this appears in AI: ask an assistant for eigenvalues you already know', minutes=8, label='Hands-on, with any AI assistant',
                  task='Ask an assistant for eigenvalues, then check them.',
                  steps=['Ask for the eigenvalues and eigenvectors of the matrix with rows (2, 1) and (1, 2). Expect 3 and 1.', 'Ask again for the covariance matrix with rows (66, 48) and (48, 38). Expect 102 and 2.', 'Ask it to show the characteristic equation. Never paste confidential data.'],
                  output='A note of which answers matched, and any sign differences.',
                  notes=('A short activity. Open any assistant you use and ask it for the eigenvalues and eigenvectors of the small matrix, then of the covariance matrix with rows sixty-six, forty-eight and forty-eight, thirty-eight. '
                         'You know the answers: three and one, and one hundred two and two. Ask it to show its characteristic equation, and read it for mistakes. '
                         'Assistants can slip on arithmetic, and checking against your own numbers is the skill. Never paste confidential company data. What differed from your answers?')))

    S.append(dict(kind='table', title='Exit check: Av = λv, two eigenvalues, and the top direction of data', headers=['Question', 'Short answer'],
                  rows=[['What does Av = λv say in words?', 'A only stretches, flips or squashes the vector v. λ is the factor.'],
                        ['What are the eigenvalues of the matrix with rows (2, 1) and (1, 2)?', 'T = 4 and D = 3, so λ = 3 and 1.'],
                        ['What does the top eigenvector of a covariance matrix tell you?', 'The direction in which the data vary most. Its eigenvalue is the variance there.']],
                  widths=[5.4, 6.6], icons=False, note='Write your own answer first, then compare. Your lab checks are part of the exit check.',
                  notes=('Three questions to finish. What does A v equals lambda v say? A only stretches, flips or squashes v, and lambda is the factor. '
                         'What are the eigenvalues of the matrix with rows two, one and one, two? The trace is four and the determinant is three, so three and one. '
                         'And what does the top eigenvector of a covariance matrix tell you? The direction in which the data vary most, with the eigenvalue as the variance there. '
                         'Answer in your own words first.')))

    s['facilitator'] = dict(
        prep=['Run the notebook and the workbook once before class. The workbook uses array formulas, so check that they open in your tool.', 'Write the check numbers on the board: 3 and 1; C rows (66, 48) and (48, 38); 102 and 2; (0.8, 0.6).',
              'Have two coloured pens ready to draw the circle and the ellipse by hand on the board.', 'Remind learners that eigenvector signs can differ between tools.',
              'This session owns mean, variance and covariance for the course (sample version, divide by n − 1). Session 13 recalls it and adds the population version.'],
        misconceptions=[('An eigenvector is one particular arrow', 'It is a direction. Any nonzero multiple, including the negative, is also an eigenvector.'), ('A large eigenvalue means an important feature', 'It means a lot of spread along that direction. Whether the spread is useful depends on the task.'),
                        ('Every matrix has real eigenvalues', 'A rotation has none. Symmetric matrices such as covariance matrices always have real ones.'), ('Eigenvalues and singular values are the same thing', 'They agree for some matrices but are not the same. Session 6 explains the link.'),
                        ('Variance is the plain average of the squared distances', 'For sample data we divide by n − 1 (VAR.S, np.cov). Dividing by n (VAR.P) treats the list as the whole population; Session 13 compares the two.')],
        probes=[('Why do the two eigenvectors of C meet at right angles?', 'C is symmetric. Eigenvectors of a symmetric matrix with different eigenvalues are always at right angles.'), ('What do the eigenvalues add up to?', 'The trace. For C that is 104, the total variance.'),
                ('Why divide by the largest entry in power iteration?', 'To stop the numbers from growing, and its size estimates the eigenvalue.'), ('What would power iteration do if we started exactly along the second eigenvector?', 'It would stay there, because that part never gets mixed with the top direction. In practice rounding errors move it away.')],
        lab_steps=[('Step 1: test', 'A times (1, 1) is (3, 3). In the sheet, A v is an array formula in two cells.'), ('Step 2: formula', 'Eigenvalues 3 and 1. A common slip is forgetting the square root.'),
                   ('Step 3: library', 'Python only. eigh lists 1 before 3. The eigenvector may carry a minus sign.'), ('Step 4: covariance', 'C is 66, 48, 38. A value of 57.75 or similar means dividing by n instead of n - 1, and a very different value means no centring.'),
                   ('Step 5: top direction', 'Eigenvalues 102 and 2, share 0.981, eigenvector (0.8, 0.6). In the sheet the vector (48, λ − 66) comes from row 1 of (C − λI)v = 0, then is scaled to length 1.'),
                   ('Step 6: power iteration', 'The estimate reaches about 102 after 6 steps. The change task: replace physics by 100 minus physics. The covariance flips sign, the eigenvalues stay 102 and 2.')],
        rescue=['The deck has 17 concept slides. If the concepts overrun, treat the table of four test arrows and the power-iteration picture on the small matrix as optional, and go straight to the characteristic equation and the table on C.',
                'If only 30 minutes of lab remain, do steps 1, 2, 4 and 5 and leave step 6 for practice.',
                'If array formulas cause trouble, do the 2 by 2 product entry by entry with SUMPRODUCT.'],
        after=['Share the solution notebook after class.', 'Ask learners to bring a question about the covariance matrix for Session 6.'],
        lab_answer_key=[['PREDICT, step 1: is (1, 1) an eigenvector of A?', 'Yes, with eigenvalue 3.'], ['READ, step 2: what is lambda squared minus 4 lambda plus 3?', 'Zero at lambda = 3 and 1.'],
                        ['READ, step 5: how much of the total variance is on direction 1?', 'About 98.1 percent (102 out of 104).'], ['CHANGE, step 6: physics replaced by 100 minus physics', 'The covariance is -48. Eigenvalues are still 102 and 2.'],
                        ['READ, power iteration: why does the guess settle quickly?', 'The second eigenvalue (2) is tiny compared with the first (102).']])
    return s
