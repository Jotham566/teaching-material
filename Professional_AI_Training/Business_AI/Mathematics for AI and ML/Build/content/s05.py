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
               ('Covariance matrix', 'A table of how every pair of features varies together. The diagonal holds each feature\'s variance, its average squared distance from its mean.'),
               ('Power iteration', 'Multiplying by a matrix again and again to find its top eigenvector.')],
        word_icons=['magnifier', 'flag', 'calculator', 'grid', 'gear'],
        words_note=('Five words. An eigenvector is a direction that a matrix only stretches, flips or squashes, so it stays on its own line. The eigenvalue is the factor, written with the Greek letter lambda. '
                    'The trace is the sum of the diagonal entries. A covariance matrix is a table of how every pair of features varies together. And power iteration means multiplying by a matrix again and again to find its top eigenvector. '
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
                  notes=('Here are the answers. A determinant of zero means the matrix squashes the plane onto a line or a point, so it has no inverse and its rank is below full. '
                         'The normal equation is X transpose X times w equals X transpose y, and it gives the weights with the smallest squared error. '
                         'The matrix with rows one, two and two, four has rank one, because its second column is twice the first, so the columns give only a single direction. '
                         'If one of these surprised you, look at Session 4 again before the lab.')))

    S.append(dict(kind='idea', title='Most arrows turn when a matrix acts on them, but a few directions only stretch',
                  visual=dict(kind='eigpic', A=((2, 1), (1, 2))),
                  lead='The matrix with rows (2,\u00a01) and (1,\u00a02) turns a circle into an ellipse. The grey arrow v turns.',
                  points=['e₁ points along (1, 1) and becomes 3 times longer.', 'e₂ points along (1, −1) and keeps its length.', 'Such directions are eigenvectors.'],
                  notes=('Picture a matrix acting on every arrow that starts at the origin and has length one, the unit circle. Our matrix has rows two, one and one, two. It turns the circle into an ellipse. '
                         'Most arrows, like the grey one, get turned to a new direction. But two special directions stay on their own lines. The red arrow e one, along one, one, becomes three times longer. The black arrow e two, along one, minus one, keeps its length. '
                         'Those special directions are called eigenvectors. Look at the dashed lines: the ellipse is longest along one dashed line and shortest along the other. Why do you think that is?')))

    S.append(dict(kind='formula', title='An eigenvector v and its eigenvalue λ satisfy Av = λv',
                  formulas=[('Definition', r'$A\mathbf{v} = \lambda\mathbf{v}$'), ('Our first pair', r'$A\,(1,1) = (3,3) = 3\,(1,1)$')],
                  symbols=[['A', 'A square matrix. Here the rows are (2, 1) and (1, 2).', '2 by 2'],
                           ['v', 'An eigenvector: a nonzero vector whose direction A keeps.', '(1, 1) or (1, −1)'],
                           ['λ', 'The eigenvalue (Greek letter lambda): the factor by which A stretches v.', '3 for (1, 1), and 1 for (1, −1)'],
                           ['Av', 'Matrix times vector. For (1, 1): (2 + 1, 1 + 2).', '(3, 3)']],
                  widths=[1.7, 6.0, 4.2], size=26, note='A negative λ flips v. A λ of 0 squashes it to the origin. Any multiple of v is an eigenvector too.',
                  notes=('Here is the definition as one line. A times v equals lambda times v. It says: when A acts on v, the result is the same vector scaled by a number. That number lambda is the eigenvalue. '
                         'For our matrix, take v equal to one, one. A times v gives two plus one, which is three, and one plus two, which is three. So A v is three, three, which is three times v. The eigenvalue is three. '
                         'Any multiple of v works as well, so we care about the direction. Check the table row by row, and say each symbol aloud.')))

    S.append(dict(kind='table', title='Testing four arrows: only some keep their direction', headers=['Arrow v', 'Av', 'Same line as v?', 'Stretch factor'],
                  rows=[['(1, 0)', '(2, 1)', 'No, it turned', 'none'], ['(1, 1)', '(3, 3)', 'Yes', '3'], ['(1, −1)', '(1, −1)', 'Yes', '1'], ['(1, 2)', '(4, 5)', 'No, it turned', 'none']],
                  widths=[2.6, 2.6, 3.8, 2.8], icons=False,
                  note='A has rows (2, 1) and (1, 2). Compute Av with a dot product for each row: for (1, 2) it is 2 + 2 = 4 and 1 + 4 = 5.',
                  notes=('Try four arrows by hand. For one, zero, A v is two, one, a new direction, so it turned. For one, one we get three, three: same line, stretched by three. '
                         'For one, minus one we get one, minus one: the same arrow, a stretch of one. For one, two we get four, five, which is not a multiple of one, two, so it turned. '
                         'Exactly two directions survive. A two by two matrix has at most two such directions, and a symmetric one like this has exactly two. Which arrow would you test next?')))

    S.append(dict(kind='wide', title='The eigenvalue says whether the arrow is stretched, shrunk, flipped or squashed',
                  visual=dict(kind='lambdas'),
                  caption='Grey arrow: an eigenvector. Red arrow: what A turns it into. λ (lambda) is the multiplier.',
                  notes=('Here is how to read an eigenvalue. The grey arrow is an eigenvector. The red arrow is what A turns it into, and lambda is the multiplier. '
                         'Lambda two doubles the arrow. Lambda one half halves it. Lambda one leaves it alone. Lambda minus one flips it to the opposite direction, but keeps its length. '
                         'And lambda zero squashes it to nothing, which is exactly the determinant zero case from last session. In fact the determinant is the product of the eigenvalues, as we will see. What lambda would a rotation have?')))

    S.append(dict(kind='steps', title='To find eigenvalues, ask when A − λI has no inverse',
                  steps=[dict(head='Start', text='Av = λv', icon='key'), dict(head='Rearrange', text='(A − λI)v = 0', icon='gear'),
                         dict(head='Need v not zero', text='So A − λI must have no inverse', icon='lock'), dict(head='Result', text='det(A − λI) = 0', icon='check')], highlight=3,
                  caption='I is the identity matrix, so λI has λ on the diagonal. No inverse means determinant 0, the singular case from Session 4.',
                  notes=('Now how to find the eigenvalues. Start with A v equals lambda v. Move everything to one side: A minus lambda I, times v, equals zero, where I is the identity matrix. '
                         'We want a v that is not the zero vector. If A minus lambda I had an inverse, multiplying by it would force v to be zero. So A minus lambda I must have no inverse, and from Session 4 that means its determinant is zero. '
                         'The determinant of A minus lambda I equals zero is called the characteristic equation. Why is the identity matrix needed there?')))

    S.append(dict(kind='example', title='Writing det(A − λI) = 0 out for our matrix',
                  scenario='A has rows (2, 1) and (1, 2). We subtract λ from each diagonal entry and take the determinant.',
                  blocks=[dict(label='A − λI', text='Rows (2 − λ, 1) and (1, 2 − λ).'),
                          dict(label='Determinant', text='(2 − λ)(2 − λ) − 1 × 1 = λ² − 4λ + 3.'),
                          dict(label='Set it to 0', text='λ² − 4λ + 3 = (λ − 3)(λ − 1) = 0, so λ = 3 or λ = 1.'),
                          dict(label='Any 2 by 2', text='The same steps give λ² − Tλ + D = 0, with T the sum of the diagonal and D the determinant.', red=True)],
                  notes=('Let us write it out for our matrix. Subtract lambda from each diagonal entry. The rows become two minus lambda, one, and one, two minus lambda. '
                         'The determinant is two minus lambda, times two minus lambda, minus one times one. Expand it and you get lambda squared, minus four lambda, plus three. '
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
                         'In the spreadsheet you will type exactly this formula.')))

    S.append(dict(kind='example', title='Worked example: eigenvalues and eigenvectors of our matrix',
                  scenario='A has rows (2, 1) and (1, 2). We find λ first, then an eigenvector (s, t) for each λ.',
                  blocks=[dict(label='Eigenvalues', text='λ² − 4λ + 3 = 0. So λ = (4 + 2) / 2 = 3 or λ = (4 − 2) / 2 = 1.'),
                          dict(label='For λ = 3', text='A − 3I has rows (−1, 1) and (1, −1). The equation −s + t = 0 gives s = t, so e₁ = (1, 1).'),
                          dict(label='For λ = 1', text='A − I has rows (1, 1) and (1, 1). The equation s + t = 0 gives e₂ = (1, −1).'),
                          dict(label='Check', text='A (1, 1) = (3, 3) and A (1, −1) = (1, −1). Both match.', red=True)],
                  notes=('Let us run the whole recipe. The quadratic is lambda squared, minus four lambda, plus three, so lambda is three or one. '
                         'We look for an eigenvector with entries s and t. For lambda three, subtract three from the diagonal, giving rows minus one, one and one, minus one. Both rows say minus s plus t equals zero, so s equals t, and e one is one, one. '
                         'For lambda one, subtract one from the diagonal, giving rows one, one and one, one, so s plus t is zero, and e two is one, minus one. The last line checks both by multiplying. '
                         'Why are the two rows identical each time?')))

    S.append(dict(kind='wide', title='Centring: subtract each feature\'s mean so the cloud sits on the origin',
                  visual=dict(kind='centre', raw=[(float(a), float(b)) for a, b in zip(d['maths'], d['phys'])], mean=(mm, mp)),
                  caption=f'Eight students (illustrative). Mean maths {gi(mm)}, mean physics {gi(mp)}. Each mark minus its mean.',
                  notes=(f'Now real data. Eight students, each with a maths mark and a physics mark, invented to show the arithmetic. The left picture shows the raw marks, with the mean of maths at {gi(mm)} and the mean of physics at {gi(mp)}. '
                         'The first step of almost every method in this part of the course is centring: subtract each feature\'s mean from its column. The shape of the cloud does not change, but now its centre sits at the origin. '
                         'The cloud runs from bottom left to top right, which says high maths marks go with high physics marks. How would you describe that tilt with a single direction?')))

    S.append(dict(kind='formula', title='The covariance matrix collects how every pair of features varies together',
                  formulas=[('Covariance of x and y', r'$\mathrm{cov}(x,y) = \frac{1}{n-1}\sum_{i=1}^{n}(x_i-\bar{x})(y_i-\bar{y})$'), ('Covariance matrix', r'$C = \frac{1}{n-1}\,X_c^{T}X_c$')],
                  symbols=[['n', 'The number of rows, here students.', f'{n} students'], ['xᵢ, yᵢ, x-bar, y-bar', 'The two marks of student i, and the two means. Σ adds up over i = 1 to n.', f'means {gi(mm)} and {gi(mp)}'],
                           ['X_c', 'The centred data: a row per student, a column per mark.', f'{n} by 2'],
                           ['C', 'Variances on the diagonal, covariance off it. Symmetric: entry (i, j) equals entry (j, i).', '2 by 2']],
                  widths=[2.6, 5.9, 3.4], size=18, note='We divide by n − 1, as np.cov does. A feature replaced by 100 minus itself flips its covariance sign.',
                  notes=('Covariance measures how two features move together. For each student, multiply the centred maths mark by the centred physics mark, add up over all students, and divide by n minus one. '
                         'A positive result means they rise together. Do this for every pair of features and arrange the results in a matrix, the covariance matrix C. In matrix form it is X c transpose X c over n minus one, '
                         'where X c is the centred data. The diagonal holds the variances, which are the covariances of a feature with itself, and the matrix is symmetric, because the covariance of maths with physics equals that of physics with maths. '
                         'If you replace physics by one hundred minus physics, the sign of the covariance flips and its size stays. Which entries of C do you expect to be largest?')))

    S.append(dict(kind='example', title='Worked by hand: the covariance matrix of the eight marks',
                  scenario='Illustrative marks. Centred = mark minus its mean.',
                  blocks=[dict(label='Maths marks', text=f'{fmt_raw(d["maths"])}. Mean {gi(mm)}. Centred: {fmt_i(ca)}.'), dict(label='Physics marks', text=f'{fmt_raw(d["phys"])}. Mean {gi(mp)}. Centred: {fmt_i(cb)}.'),
                          dict(label='Sums', text=f'Maths squared {gi(sa2)}. Physics squared {gi(sb2)}. Maths times physics {gi(sab)}.'),
                          dict(label='Divide', text=f'Divide by n − 1 = {n - 1}. Variances {gi(C[0, 0])} and {gi(C[1, 1])}. Covariance {gi(C[0, 1])}. So C has rows ({gi(C[0, 0])}, {gi(C[0, 1])}) and ({gi(C[1, 0])}, {gi(C[1, 1])}).', red=True)],
                  notes=(f'Let us do it once by hand. The raw marks are on the slide. The mean of the maths marks is {gi(mm)} and the mean of the physics marks is {gi(mp)}. Subtract each mean from its column, giving the two lists of centred values. '
                         f'Square each maths value and add: {gi(sa2)}. Do the same for physics: {gi(sb2)}. Multiply each pair and add: {gi(sab)}. Divide each by seven, which is n minus one. '
                         f'The variances are {gi(C[0, 0])} and {gi(C[1, 1])}, and the covariance is {gi(C[0, 1])}. So the covariance matrix has rows {gi(C[0, 0])}, {gi(C[0, 1])} and {gi(C[1, 0])}, {gi(C[1, 1])}. '
                         'The positive covariance matches the tilt we saw in the picture.')))

    S.append(dict(kind='idea', title='The eigenvectors of the covariance matrix are the directions of the cloud',
                  visual=dict(kind='cloud', points=pts, axes=[dict(v=tuple(float(t) for t in v1), len=12.5, label='principal component 1', at=0.5, ha='left', dx=0.15, dy=-0.45), dict(v=tuple(float(t) for t in v2), len=9, label='component 2', color=MB.INK, dy=0.3)],
                              xlabel='Centred maths mark (across) and centred physics mark (up)'),
                  lead='Each dot is a student, centred. The red arrow is the first eigenvector of C (direction 1), the black arrow the second.',
                  points=[f'e₁ = ({gm(v1[0])}, {gm(v1[1])}): principal component 1, variance {gi(lam[0])}.', f'e₂ = ({gm(v2[0])}, {gm(v2[1])}): variance only {gi(lam[1])}.', 'For a unit-length eigenvector the eigenvalue is the variance along it.'],
                  notes=('Now the payoff. Draw the centred students, and draw the eigenvectors of their covariance matrix. The red arrow, e one, points along the long axis of the cloud. That is the direction in which the data vary most, called the first principal component. '
                         f'The black arrow, e two, is at right angles, along the short axis, where the dots barely spread. And for an eigenvector of length one, the eigenvalue tells you how much spread: along the red direction the variance is {gi(lam[0])}, and along the black one only {gi(lam[1])}. '
                         'So the eigenvectors of the covariance matrix are the natural axes of the data. This is the core of principal component analysis. Which direction would you keep if you could keep only one?')))

    S.append(dict(kind='example', title='Worked by hand: eigenvalues and top eigenvector of C',
                  scenario='C has rows (66, 48) and (48, 38). We use the 2 by 2 formulas from earlier.',
                  blocks=[dict(label='Trace and determinant', text=f'T = 66 + 38 = {gi(T)}. D = 66 × 38 − 48 × 48 = {gi(D)}.'),
                          dict(label='Eigenvalues', text=f'The square root of {gi(T)}² − 4 × {gi(D)} is {gi(root)}. So λ = ({gi(T)} + {gi(root)}) / 2 = {gi(lam[0])} or ({gi(T)} − {gi(root)}) / 2 = {gi(lam[1])}.'),
                          dict(label='Top eigenvector', text='C − 102I has rows (−36, 48) and (48, −64). So −36s + 48t = 0, which gives t = 0.75s. Take (4, 3). Length 5, so e₁ = (0.8, 0.6).'),
                          dict(label='Share of variance', text=f'{gi(lam[0])} / {gi(lam[0] + lam[1])} = {g(100 * d["explained"], 1)} percent of all the variance lies along direction 1.', red=True)],
                  notes=(f'Now the same recipe on the covariance matrix. Trace {gi(T)}, determinant {gi(D)}. The square root part is the square root of {gi(T * T - 4 * D)}, which is exactly {gi(root)}. So the eigenvalues are {gi(lam[0])} and {gi(lam[1])}. '
                         'For the top eigenvector, subtract one hundred two from the diagonal. The first row says minus thirty-six s plus forty-eight t equals zero, so t is three quarters of s. Take four, three, and divide by its length five to get zero point eight, zero point six. '
                         f'Finally one hundred two out of one hundred four is {g(100 * d["explained"], 1)} percent. Almost all the spread of the eight students lies along one direction.')))

    S.append(dict(kind='formula', title='Power iteration finds the top eigenvector by repeated multiplying',
                  formulas=[('Update', r'$\mathbf{g}_{k+1} = \frac{A\,\mathbf{g}_k}{\max|A\,\mathbf{g}_k|}$'), ('Eigenvalue estimate', r'$\lambda \approx \max|A\,\mathbf{g}_k|$')],
                  symbols=[['gₖ', 'The current guess for the eigenvector, after k steps.', 'g₀ = (1, 0) to start'], ['Agₖ', 'Multiply the guess by the matrix.', 'one matrix times vector product'],
                           ['max |.|', 'The entry with the largest size. Dividing by it keeps the numbers small.', 'g then has largest entry 1'], ['λ', 'The top eigenvalue, the one largest in size.', 'estimate tends to 3']],
                  widths=[1.8, 5.8, 4.3], size=22, note='It works when one eigenvalue is largest in size and the start is not exactly along another eigenvector.',
                  notes=('Power iteration is the simplest way to find the top eigenvector by computer, and it only needs matrix times vector. Start with any guess, called g zero. Multiply it by A. '
                         'Divide the result by its largest entry so the numbers do not grow. Repeat. The guess swings towards the eigenvector with the largest eigenvalue. '
                         'Each multiplication stretches the top direction a little more than the others, so after a few rounds the top direction wins. The largest entry before you divide estimates the eigenvalue. '
                         'It needs one eigenvalue that is clearly the largest in size. That is the case for the covariance matrices we care about.')))

    S.append(dict(kind='idea', title='Each multiplication swings the arrow closer to the top eigen-direction',
                  visual=dict(kind='power', A=((2, 1), (1, 2)), v0=(1, 0), nsteps=4),
                  lead='Matrix with rows (2, 1) and (1, 2). Start at g₀ = (1, 0). Multiply, then divide by the largest entry.',
                  points=[f'g₁ = (1, {g(pa[1][1][1])}), g₂ = (1, {g(pa[2][1][1])}), g₄ is almost (1, 1).', f'The estimates of λ are {", ".join(g(r[3], 2) for r in pa)}. They head to 3.'],
                  notes=(f'Watch it happen on the small matrix. Start at the arrow g zero, one, zero. Multiplying by A gives two, one. Divide by two: g one is one, and one half. Multiply again: two point five, two. Divide: g two is one, point eight. '
                         f'The arrows swing towards the one, one direction, which is the eigenvector for lambda three. The estimates of the eigenvalue, the largest entries before dividing, are {", ".join(g(r[3], 2) for r in pa)}, heading to three. '
                         'After a handful of steps the arrow is almost on the dashed line. Why does the first step move the arrow so much more than the last one?')))

    S.append(dict(kind='table', title='Power iteration by hand on the covariance matrix C', headers=['Step k', 'Guess gₖ', 'C gₖ', 'Largest entry'],
                  rows=[[str(r[0]), f'({g(r[1][0], 3)}, {g(r[1][1], 3)})', f'({g(r[2][0], 1)}, {g(r[2][1], 1)})', g(r[3], 2)] for r in pc],
                  widths=[1.6, 3.4, 3.8, 3.0], icons=False,
                  note=f'Start g₀ = (0, 1). The next guess is C gₖ divided by the largest entry. After 6 multiplications (row k = 5) the estimate is {g(pc[-1][3], 1)}, close to {gi(lam[0])}, and the guess is near (1, 0.75), which is (0.8, 0.6) at length 1.',
                  notes=('Here is power iteration on the covariance matrix. We start at g zero, zero, one. Multiplying by C gives forty-eight, thirty-eight, and we divide by forty-eight. '
                         'The next guess is one, point seven nine. Multiply again, divide again, and by step three the guess is already very close to one, point seven five. '
                         'The largest entry, our estimate of the eigenvalue, settles near one hundred two. Here the second eigenvalue is only two, so each step shrinks the unwanted part by a factor of about fifty, and convergence is fast. '
                         'In the spreadsheet you will build exactly this table in rows of cells.')))

    S.append(dict(kind='table', title='Common mistake: four things to remember about eigenvectors', headers=['Mistake', 'What is true', 'What to do'],
                  rows=[['Treating an eigenvector as one fixed arrow', 'Any multiple, and the opposite arrow, is also an eigenvector.', 'Quote a unit-length version. Expect sign flips between tools.'],
                        ['Looking for eigenvalues of a non-square matrix', 'Only square matrices have them.', 'Use the SVD for other shapes (Session 6).'],
                        ['Expecting real eigenvalues always', 'A quarter-turn rotation has no real eigenvalues, because every arrow turns.', 'Covariance matrices are symmetric and always give real ones.'],
                        ['Mixing up the two outputs', 'For a covariance matrix, the eigenvalue is the spread along its eigenvector.', 'Quote both together.']],
                  widths=[3.7, 4.3, 3.9], icons=['cross', 'cross', 'cross', 'cross'],
                  notes=('Four things to remember. First, an eigenvector is a direction, not one fixed arrow. Any multiple of it works, and so does the opposite arrow, so two tools can give the same eigenvector with opposite signs, and both are right. '
                         'Second, eigenvalues belong to square matrices only. For other shapes we use the singular value decomposition next session. '
                         'Third, a quarter-turn rotation has no real eigenvalues, because every arrow turns. Covariance matrices are symmetric, which guarantees real eigenvalues. '
                         'Fourth, keep the roles straight: for a covariance matrix the eigenvalue is how much spread, the eigenvector is which direction.')))

    S.append(dict(kind='code', title='Read the recipe before you write it: covariance, then eigenvectors',
                  code='Xc = X - X.mean(axis=0)\nC = Xc.T @ Xc / (len(X) - 1)\nvalues, vectors = np.linalg.eigh(C)\ng = np.array([0.0, 1.0])\nfor k in range(6):\n    Cg = C @ g\n    est = np.max(np.abs(Cg))\n    g = Cg / est',
                  reads=['Xc = ... centres each column by subtracting its mean.', 'C = ... is the covariance matrix, as in the formula.', 'eigh is for symmetric matrices. It lists eigenvalues from smallest to largest, with eigenvectors in the columns.',
                         'The loop from g = ... is power iteration. est holds the eigenvalue estimate.'],
                  notes=('Here is the code. Subtract the column means to centre. Form the covariance matrix with X c transpose times X c over n minus one. '
                         'Then np dot linalg dot eigh returns the eigenvalues and the eigenvectors. The letters e, i, g, h are for symmetric matrices, which covariance matrices always are. '
                         'Note that it lists the eigenvalues from smallest to largest, and the eigenvectors are the columns. Below is power iteration in a short loop: multiply, find the largest entry, divide. '
                         'You do not need to memorise it, since the notebook explains every line.')))

    S.append(dict(kind='divider', title='Part 2: the lab', lead='Close the slides. Open the notebook or the workbook.', section='Lab',
                  notes=('That is the end of the ideas. In the lab you compute eigenvalues three ways: by the formula, with a library, and by power iteration. Choose the Python notebook or the spreadsheet workbook. '
                         'The numbers are identical in both, and each step ends with an automatic check. A spreadsheet has no eigenvalue function in Excel or Google Sheets, so there you build the formula and the iteration rows yourself. '
                         'Predict, run, read, then change one thing. Raise your hand when a check stays red.')))

    S.append(dict(kind='steps', title='The lab has six steps, in the notebook and in the workbook',
                  steps=[dict(head='1 Test', text='Does A keep the direction of (1, 1)?', icon='magnifier'), dict(head='2 Formula', text='Eigenvalues from trace and determinant', icon='calculator'),
                         dict(head='3 Library', text='eigh in Python. The sheet has no such function.', icon='gear'), dict(head='4 Covariance', text='Centre the marks, build C', icon='grid'),
                         dict(head='5 Top direction', text='Eigenvalues, eigenvector, share of variance', icon='chart'), dict(head='6 Power', text='Repeat C v and watch the guess settle', icon='clock')], highlight=4,
                  caption='Python uses numpy. The spreadsheet uses MMULT, VAR.S, COVARIANCE.S, SQRT and rows of cells. Gold cells are yours.',
                  notes=('Here is the map. Step one, test whether A keeps the direction of one, one. Step two, find the eigenvalues from trace and determinant. '
                         'Step three, Python only: check with a library function. The spreadsheet has none, so the formula is the tool. '
                         'Step four, centre the eight marks and build the covariance matrix. Step five, find its eigenvalues, the top eigenvector and the share of variance. Step six, power iteration in rows of cells. '
                         'Predict each answer before you look.')))

    S.append(dict(kind='table', title='Check your numbers against these before you move on', headers=['What you compute', 'You should see'],
                  rows=[['A times (1, 1) for the small matrix', '(3, 3)'], ['Eigenvalues of the small matrix', '3 and 1'], ['Covariance matrix C of the eight marks', f'rows ({gi(C[0, 0])}, {gi(C[0, 1])}) and ({gi(C[1, 0])}, {gi(C[1, 1])})'],
                        ['Eigenvalues of C', f'{gi(lam[0])} and {gi(lam[1])}'], ['Top eigenvector of C, unit length', f'({g(v1[0], 1)}, {g(v1[1], 1)})'], ['Share of variance along direction 1', f'{g(d["explained"], 3)}'],
                        ['Power iteration after 6 multiplications (row k = 5): largest entry', g(pc[-1][3], 1)], ['Covariance if physics is replaced by 100 minus physics', f'−{gi(C[0, 1])}: the sign flips, the size stays']],
                  widths=[7.0, 4.2], icons=['calculator', 'flag', 'grid', 'chart', 'chart', 'bars', 'gear', 'switch'],
                  note='If a number differs, stop and find the step that went wrong. The sign of an eigenvector may differ between tools.',
                  notes=('Here is your checkpoint. If your numbers match, carry on. If they do not, stop and call me over. The usual causes are dividing by n instead of n minus one, forgetting to centre, and mixing up the order of the two features. '
                         'Remember that an eigenvector may come out with the opposite sign in a different tool, and that is fine. '
                         'The notebook checks the absolute values for that reason. Please do not type a number just to make a check pass.')))

    S.append(dict(kind='table', title='Four errors you will meet, what they say and what to do', headers=['Error or symptom', 'What it says', 'What to do'],
                  rows=[['The eigenvector has a minus sign', 'The opposite arrow is also an eigenvector.', 'Compare absolute values, or flip the sign.'], ['Eigenvalues come out in the wrong order', 'eigh lists smallest first.', 'Reverse the list or sort it.'],
                        ['Covariance far too large', 'The data were not centred first.', 'Subtract the column means.'], ['#NUM! in the spreadsheet', 'The square root of a negative number.', 'Check T² − 4D. For covariance it is never negative.']],
                  widths=[3.8, 4.1, 4.0], icons=['cross', 'key', 'bell', 'flag'],
                  notes=('Four things that will happen. A minus sign on an eigenvector is not an error, because the opposite arrow is also an eigenvector. '
                         'If the eigenvalues come out in the wrong order, remember that eigh lists the smallest first. '
                         'If your covariance is far too big, you did not centre the data. And a number error in the spreadsheet means a negative number under the square root, so check T squared minus four D. '
                         'Read the last line of any message first. It usually tells you the answer.')))

    S.append(dict(kind='wide', title='Where this appears in AI: PCA turns embeddings into a map you can look at',
                  visual=dict(kind='embedmap'),
                  caption='PCA (principal component analysis) of made-up 4-number vectors. Real embeddings are far longer.',
                  notes=('Language models of this kind turn words and passages into embeddings, which are lists of numbers. To look at them, people project them down to two directions. '
                         'The method is principal component analysis, or PCA, and it is the one you just learned: centre the vectors, form the covariance matrix, take the two eigenvectors with the largest eigenvalues, and plot each vector\'s position along them. '
                         'On the right, three clusters appear, animals, vehicles and foods. The vectors here are made up to show the idea, with four numbers each. Real embeddings are much longer, but the mathematics is identical. '
                         'What would you look for on such a map?')))

    S.append(dict(kind='list', title='Where this appears in AI: looking at what models learn',
                  items=['PCA keeps the top eigenvectors of the covariance matrix of the data.', 'The Embedding Projector, published by Google researchers in 2016, offers PCA to view embeddings.',
                         'Open-weight models such as Llama publish their weights, so this analysis can be run on them.', 'Closed assistants do not publish their internal embedding tables. The vectors a public embedding service returns for your own text can be projected the same way.'],
                  icons=['chart', 'magnifier', 'folder', 'lock'],
                  notes=('Three facts about where this shows up. First, principal component analysis is just the top eigenvectors of the covariance matrix, which you have now computed by hand. '
                         'Second, published tools such as the Embedding Projector, described by Google researchers in 2016, offer PCA to look at embeddings in two or three dimensions. '
                         'Third, open-weight models such as Llama publish their weights, so anyone can run this analysis on them. The internal embedding tables of closed assistants are not published, so we cannot draw them. But the vectors that a public embedding service returns for your own text can be projected in the same way. '
                         'Which open model would you like to try this on?')))

    S.append(dict(kind='practice', title='Where this appears in AI: check an assistant with your numbers', minutes=8, label='Hands-on, with any AI assistant',
                  task='Ask an assistant for eigenvalues, then check them.',
                  steps=['Ask for the eigenvalues and eigenvectors of the matrix with rows (2, 1) and (1, 2). Expect 3 and 1.', 'Ask again for the covariance matrix with rows (66, 48) and (48, 38). Expect 102 and 2.', 'Ask it to show the characteristic equation. Never paste confidential data.'],
                  output='A note of which answers matched, and one where the assistant used a different sign.',
                  notes=('A short activity. Open any assistant you use and ask it for the eigenvalues and eigenvectors of the small matrix, then of the covariance matrix with rows sixty-six, forty-eight and forty-eight, thirty-eight. '
                         'You know the answers: three and one, and one hundred two and two. Ask it to show its characteristic equation, and read it for mistakes. '
                         'Assistants can slip on arithmetic, and checking against your own numbers is the skill. Never paste confidential company data. What differed from your answers?')))

    S.append(dict(kind='table', title='Exit check: three questions with short answers', headers=['Question', 'Short answer'],
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
              'Have two coloured pens ready to draw the circle and the ellipse by hand on the board.', 'Remind learners that eigenvector signs can differ between tools.'],
        misconceptions=[('An eigenvector is one particular arrow', 'It is a direction. Any nonzero multiple, including the negative, is also an eigenvector.'), ('A large eigenvalue means an important feature', 'It means a lot of spread along that direction. Whether the spread is useful depends on the task.'),
                        ('Every matrix has real eigenvalues', 'A rotation has none. Symmetric matrices such as covariance matrices always have real ones.'), ('Eigenvalues and singular values are the same thing', 'They agree for some matrices but are not the same. Session 6 explains the link.')],
        probes=[('Why do the two eigenvectors of C meet at right angles?', 'C is symmetric. My understanding is that eigenvectors of a symmetric matrix with different eigenvalues are always at right angles.'), ('What do the eigenvalues add up to?', 'The trace. For C that is 104, the total variance.'),
                ('Why divide by the largest entry in power iteration?', 'To stop the numbers from growing, and its size estimates the eigenvalue.'), ('What would power iteration do if we started exactly along the second eigenvector?', 'It would stay there, because that part never gets mixed with the top direction. In practice rounding errors move it away.')],
        lab_steps=[('Step 1: test', 'A times (1, 1) is (3, 3). In the sheet, A v is an array formula in two cells.'), ('Step 2: formula', 'Eigenvalues 3 and 1. A common slip is forgetting the square root.'),
                   ('Step 3: library', 'Python only. eigh lists 1 before 3. The eigenvector may carry a minus sign.'), ('Step 4: covariance', 'C is 66, 48, 38. A value of 57.75 or similar means dividing by n instead of n - 1, and a very different value means no centring.'),
                   ('Step 5: top direction', 'Eigenvalues 102 and 2, share 0.981, eigenvector (0.8, 0.6). In the sheet the vector is (the covariance, the eigenvalue minus the first variance) before it is scaled to length 1.'),
                   ('Step 6: power iteration', 'The estimate reaches about 102 after 6 steps. The change task: replace physics by 100 minus physics. The covariance flips sign, the eigenvalues stay 102 and 2.')],
        rescue=['If the concepts overrun, skip the table of four test arrows and go straight to the characteristic equation.', 'If only 30 minutes of lab remain, do steps 1, 2, 4 and 5 and leave step 6 for practice.',
                'If array formulas cause trouble, do the 2 by 2 product entry by entry with SUMPRODUCT.'],
        after=['Share the solution notebook after class.', 'Ask learners to bring a question about the covariance matrix for Session 6.'],
        lab_answer_key=[['PREDICT, step 1: is (1, 1) an eigenvector of A?', 'Yes, with eigenvalue 3.'], ['READ, step 2: what is lambda squared minus 4 lambda plus 3?', 'Zero at lambda = 3 and 1.'],
                        ['READ, step 5: how much of the total variance is on direction 1?', 'About 98.1 percent (102 out of 104).'], ['CHANGE, step 6: physics replaced by 100 minus physics', 'The covariance is -48. Eigenvalues are still 102 and 2.'],
                        ['READ, power iteration: why does the guess settle quickly?', 'The second eigenvalue (2) is tiny compared with the first (102).']])
    return s
