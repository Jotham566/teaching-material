"""Session 4: Solving linear systems. Ax = b, elimination, inverse, determinant, rank, least squares and the normal equation."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'kit'))
import diagrams_math_b as MB  # noqa: E402


def build():
    d = MB.d4()
    sol = d['sol']
    bi, ws = float(d['w'][0]), float(d['w'][1])      # intercept b and slope w of the fitted line
    x, y, n = d['x'], d['y'], d['n']
    pts = [(float(a), float(c)) for a, c in zip(x, y)]
    sx, sx2, sy, sxy = float(x.sum()), float((x ** 2).sum()), float(y.sum()), float((x * y).sum())
    det_x = float(d['detXtX'])
    rmse = d['rmse']
    p7 = d['pred7']
    g = lambda v, k=2: f'{v:.{k}f}'
    clock = [(10, 'Recall, then a real question from AI'), (35, 'Concept: picture, then a hand example'), (10, 'Break'), (45, 'Lab: predict, run, change one thing'),
             (15, 'Where it appears in AI, plus an exit check'), (5, 'Save the work')]

    s = dict(
        num=4, block='Linear algebra', short_title='Solving linear systems',
        title='Solving linear systems: from Ax = b to the best-fitting line',
        question='How does a computer find the best straight line through data in one step, and why does a model with more features than rows break?',
        outcomes=['Write a system of equations as Ax = b and solve it by elimination and with the inverse',
                  'Say what the determinant and the rank tell you, and when a system has no solution or many',
                  'Fit a line ŷ = b + w x by least squares with the normal equation, in Python and in a spreadsheet'],
        outcome_icons=['calculator', 'magnifier', 'chart'],
        outcome_note=('By the end of today you can write a system of equations in matrix form, as A x equals b, and solve it by elimination and with the inverse. '
                      'You can say what the determinant and the rank tell you, and why some systems have no solution or many. '
                      'And you can fit a straight line to data using the normal equation, in Python and in a spreadsheet, with the same numbers in both tools. The line is written y hat equals b plus w x, the same letters the rest of the course uses.'),
        clock=clock, plan_title='Your two hours: equations, then a fitted line', plan_caption='Ideas first, with pictures. Then the lab in Python or in a spreadsheet. Then where it shows up in AI.',
        plan_note=('We have two hours. The first ten minutes bring back Session 3 on matrices and set our question for the day. Then thirty-five minutes of ideas, each as a picture and then a small calculation by hand. '
                   'After a ten minute break comes the lab, forty-five minutes, in Python or in a spreadsheet, on the same numbers. We finish with where this appears in AI tools, an exit check and five minutes to save your work.'),
        recall_from='Session 3',
        recall=[('A is a 3 by 2 matrix and B is a 2 by 4 matrix. Can you multiply A times B, and what is the shape of the result?', 'Yes. The inner numbers match (2 and 2). The result is 3 by 4.'),
                ('What does the matrix with rows (2, 0) and (0, 3) do to the vector (1, 1)?', 'It gives (2, 3). It stretches the first direction by 2 and the second by 3.'),
                ('What does the identity matrix I do to any vector x?', 'Nothing. I times x equals x. It is the matrix version of the number 1.')],
        words=[('Linear system', 'Several equations in the same unknowns, written together as Ax = b.'),
               ('Inverse', 'The matrix A⁻¹ that undoes A: A⁻¹ times A is the identity matrix.'),
               ('Determinant', 'One number from a square matrix. Its size is the factor by which A scales areas.'),
               ('Rank', 'How many independent directions the columns of a matrix give: no chosen column can be built from the others.'),
               ('Least squares', 'Choosing the line whose squared errors add up to the smallest total.')],
        word_icons=['grid', 'key', 'calculator', 'flag', 'chart'],
        words_note=('Five words today, and they are the real names, so you will meet them in every textbook and library manual. A linear system is several equations written together as A x equals b. '
                    'The inverse is the matrix that undoes A. The determinant is one number that tells you how A scales areas. Rank counts the independent directions in the columns. '
                    'And least squares means choosing the line whose squared errors add up to the smallest total. We use each of them before the break.'),
        keep=f'Keep your saved notebook or workbook, and the fitted line for the advertising data: intercept b = {g(bi)} and slope w = {g(ws)}.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Saved lab', value='Notebook or workbook, saved'), dict(label='Fitted line', value=f'ŷ = {g(bi)} + {g(ws)} × spend'),
                                                            dict(label='Next session', value='Eigenvalues and eigenvectors'), dict(label='Bring', value='One question about today')]),
        keep_title='Save the lab and keep the fitted line',
        next='Session 5: eigenvalues and eigenvectors, the directions a matrix only stretches.', next_label='Next session',
        keep_note=(f'Before you go, save your notebook or workbook with all the checks green. Keep the fitted line: intercept b equal to {g(bi)} and slope w equal to {g(ws)}. Sessions 8 and 10 fit the same kind of line with the same letters, by a different method. '
                   'Next session asks which directions a matrix only stretches, and that leads to the idea behind principal component analysis. If anything was unclear today, write your question down and bring it.'),
        cover_note=('Welcome to Session 4. Last time we used matrices to move and mix numbers. Today we run that machinery backwards: given the result, find the input. '
                    'That is solving a linear system, and fitting a line to data turns out to be the same job. By the end you will fit a line with one equation, in Python and in a spreadsheet.'),
        slides=[])
    S = s['slides']

    S.append(dict(kind='table', title='Answers to the three questions from Session 3', headers=['Question', 'Short answer'], rows=[[q, a] for q, a in s['recall']], widths=[6.0, 6.0], icons=False,
                  note='If one surprised you, look back at Session 3 before the lab. The identity matrix returns today as part of the inverse.',
                  notes=('The short answers are on the slide. First, a three by two times a two by four works, because the inner numbers match, and the result is three by four. '
                         'Second, the matrix with rows two zero and zero three gives two and three, so it stretches the first direction by two and the second by three. '
                         'Third, the identity matrix does nothing: I times x equals x. That last one matters today, because the inverse is defined using it. If one of these surprised you, look at Session 3 again before the lab.')))

    S.append(dict(kind='idea', title='A system of equations is a set of lines, and the solution is where they cross',
                  visual=dict(kind='sysrows', panels=[dict(title='', lines=[dict(abc=(2, 1, 5), label='2x₁ + x₂ = 5', at=(1.0, 3.9), color=MB.INK), dict(abc=(1, -1, 1), label='x₁ − x₂ = 1', at=(4.3, 2.4), color=MB.RED)],
                                                           pt=(2, 1), pt_label='(2, 1)', pt_dx=0.2, pt_dy=-0.3, pt_ha='left', range=((-1.5, 6.5), (-2.5, 4.5)), ticks=True, xt=[1, 2, 3, 4], yt=[-2, -1, 1, 2, 3, 4])]),
                  lead='Two equations, two unknowns, x₁ (across) and x₂ (up). Each equation draws one line.',
                  points=['The gold dot lies on both lines, so it satisfies both equations.', 'It is the pair x₁ = 2, x₂ = 1.', 'Check: 2 × 2 + 1 = 5 and 2 − 1 = 1.'],
                  notes=('Start with a puzzle you could do in school. Two equations, two unknowns, which we call x one and x two. Two x one plus x two equals five, and x one minus x two equals one. Each equation is a straight line when you draw it. '
                         'A point on the first line satisfies the first equation. A point on the second line satisfies the second. The one point on both lines, the gold dot, satisfies both, and that is the solution: x one equals two, x two equals one. '
                         'Check it in the first equation: two times two plus one is five. How would a computer find that dot without drawing anything?')))

    S.append(dict(kind='formula', title='The same system in matrix form is Ax = b',
                  formulas=[('Matrix form', r'$A\,\mathbf{x} = \mathbf{b}$'), ('Our system', r'$2x_1 + x_2 = 5 \qquad x_1 - x_2 = 1$')],
                  symbols=[['A', 'The matrix of coefficients. Row 1 is (2, 1) and row 2 is (1, −1).', '2 by 2 matrix'],
                           ['x', 'The vector of unknowns, a column (Session 3). Its entries are x₁ and x₂.', '(x₁, x₂)'],
                           ['b', 'The vector of right-hand sides. Here b is the right-hand side; from the line fit on, b is the intercept.', '(5, 1)'],
                           ['Ax', 'Matrix times vector from Session 3: each row of A takes a dot product with x.', '(2x₁ + x₂, x₁ − x₂)']],
                  widths=[1.4, 6.6, 3.9], size=26, note='Ax = b says: apply A to the unknown x and you get b. Solving means running A backwards.',
                  notes=('Machine learning libraries want the system written this way. Put the coefficients in a matrix A, the unknowns in a column vector x, and the right-hand sides in a vector b. '
                         'The product A times x, from Session 3, takes each row of A and forms a dot product with x. That gives two x one plus x two in the first slot and x one minus x two in the second. '
                         'Setting that equal to b gives our two equations. One warning about letters: in A x equals b, the letter b is the right-hand side. From the line fit later today, b will mean the intercept, as it does in the rest of the course. Solving the system means running A backwards.')))

    S.append(dict(kind='idea', title='The column picture: b is a mix of the columns of A',
                  visual=dict(kind='colpic', cols=[(2, 1), (1, -1)], coef=[2, 1]),
                  lead='The columns of A are the arrows (2, 1) and (1, -1). How much of each adds up to b?',
                  points=['2 of column 1 reaches (4, 2). Then 1 of column 2 moves on to (5, 1).', 'That is b. So the solution (x₁, x₂) = (2, 1) lists how much of each column to use.'],
                  notes=('There is a second way to see the same system, and machine learning uses it most. Read the columns of A as arrows. Column one is the arrow two, one. Column two is the arrow one, minus one. '
                         'The question becomes: how much of each arrow do I add to reach b? Two lots of column one take me to four, two. One lot of column two then takes me to five, one, which is b. '
                         'So the solution, x one equals two and x two equals one, is the recipe: two of the first column and one of the second. Some people find the lines easier, others the arrows. Keep both pictures.')))

    S.append(dict(kind='wide', title='Elimination solves the system by making zeros, then reading the answer from the bottom',
                  visual=dict(kind='elim', stages=[dict(title='Start: the augmented matrix', rows=[['2', '1', '5'], ['1', '−1', '1']], op='The dashed line separates A from b. Each row is one equation'),
                                                   dict(title='Row 2 minus half of row 1', rows=[['2', '1', '5'], ['0', '−1.5', '−1.5']], op='a row operation: the 1 under the 2 becomes 0', hl=1),
                                                   dict(title='Divide row 2 by −1.5', rows=[['2', '1', '5'], ['0', '1', '1']], op='row 2 says x₂ = 1. Then row 1 says 2x₁ + 1 = 5, so x₁ = 2')]),
                  caption='Making zeros, then back substitution (bottom row first): together, Gaussian elimination.',
                  notes=('Elimination is what you do by hand, and it is how computers solve systems too. We write the coefficients and the right-hand sides together, with a dashed line between them. That layout is called an augmented matrix. '
                         'Then we subtract half of row one from row two. That is a row operation, and it makes the one under the two become zero. Row two now says minus one point five x two equals minus one point five. Divide, and x two equals one. '
                         'Then go back up: row one says two x one plus one equals five, so two x one is four and x one equals two. Making zeros and reading upwards is called Gaussian elimination, with back substitution for the last part.')))

    S.append(dict(kind='formula', title='The inverse undoes A, so x = A⁻¹b',
                  formulas=[('Inverse and solution', r'$A^{-1}A = I \qquad \mathbf{x} = A^{-1}\mathbf{b}$'),
                            ('For a 2 by 2 matrix', r'$A^{-1} = \frac{1}{\det A}\left(\genfrac{}{}{0}{}{a_{22}}{-a_{21}}\ \ \ \genfrac{}{}{0}{}{-a_{12}}{a_{11}}\right)$')],
                  symbols=[['A⁻¹', 'The inverse of A: the matrix that undoes A.', 'exists only if det A is not 0'],
                           ['I', 'The identity matrix, which leaves every vector unchanged.', 'rows (1, 0) and (0, 1)'],
                           ['a₁₁ to a₂₂', 'The entries of A: row 1 is (a₁₁, a₁₂) and row 2 is (a₂₁, a₂₂). The inverse swaps a₁₁ and a₂₂ and puts a minus sign on the other two.', '2, 1, 1, −1'],
                           ['det A', 'The determinant of A: a₁₁a₂₂ − a₁₂a₂₁.', '2 × (−1) − 1 × 1 = −3']],
                  widths=[2.0, 6.4, 3.5], size=22, note='If x = A⁻¹b, then Ax = AA⁻¹b = Ib = b. The answer undoes the system.',
                  notes=('Multiplying by A turns x into b. So there should be a matrix that turns b back into x. That matrix is the inverse, written A to the minus one. '
                         'It is defined by one rule: A inverse times A gives the identity matrix. Then x equals A inverse times b. '
                         'For a two by two matrix the inverse has a short recipe, drawn as a matrix on the slide. Swap the two diagonal entries, put a minus sign on the other two, and divide everything by the determinant, a one one times a two two, minus a one two times a two one. '
                         'The inverse fails if that number is zero, because you cannot divide by zero.')))

    S.append(dict(kind='example', title='Worked example: the inverse of our A, and the solution from it',
                  scenario='A has rows (2, 1) and (1, −1). We find the inverse, then multiply it by b = (5, 1).',
                  blocks=[dict(label='Determinant', text='det A = 2 × (−1) − 1 × 1 = −3. It is not 0, so the inverse exists.'),
                          dict(label='Inverse', text='Swap 2 and −1, negate the other two: rows (−1, −1) and (−1, 2). Divide by −3: rows (1/3, 1/3) and (1/3, −2/3).'),
                          dict(label='Solution', text='x = A⁻¹b: first entry (5 + 1) / 3 = 2. Second entry (5 − 2) / 3 = 1.'),
                          dict(label='Check', text='A times (2, 1) gives (2 × 2 + 1, 2 − 1) = (5, 1). It equals b.', red=True)],
                  notes=('Run the recipe on our matrix. The determinant is two times minus one, minus one times one, which is minus three. It is not zero, so the inverse exists. '
                         'Swap the diagonal entries and negate the other two, giving rows minus one, minus one and minus one, two. Divide by minus three. '
                         'Multiply by b, which is five, one. The first entry is five plus one, over three, which is two. The second is five minus two, over three, which is one. '
                         'We got back x one equals two, x two equals one. Always finish with a check, as in the last block.')))

    S.append(dict(kind='idea', title='The determinant is the factor by which A scales areas',
                  visual=dict(kind='unitsq', A=((2, 1), (1, -1)), area='area 3', note_before='Unit square: area 1', note_after='A turns it into this: area 3'),
                  lead='The two red and black arrows are the columns of A. A sends the unit square onto the gold parallelogram.',
                  points=['Its area is 3, so A scales areas by 3.', 'det A = −3. The size is the area factor.', 'The minus sign means the picture is also flipped, like a mirror.'],
                  notes=('The picture behind that number starts with the unit square, area one, with sides along the two basic directions. Apply A. The sides become the columns of A, and the square becomes this gold parallelogram. '
                         'Its area is three. So A multiplies every area by three, and the determinant is minus three. The size three is the area factor. '
                         'The minus sign tells us orientation flipped, like looking in a mirror. This picture explains why a determinant of zero is special. What would an area of zero look like?')))

    S.append(dict(kind='idea', title='When the determinant is 0, A squashes the plane flat and has no inverse',
                  visual=dict(kind='unitsq', A=((1, 2), (2, 4)), area='', note_before='Unit square: area 1', note_after='A turns it into a line: area 0'),
                  lead='This matrix has columns (1, 2) and (2, 4). Both arrows point the same way.',
                  points=['The square collapses onto one line, so the area is 0.', 'det = 1 × 4 − 2 × 2 = 0.', 'Many inputs land on the same output, so nothing can undo it: no inverse. Such a matrix is called singular.'],
                  notes=('Change the matrix so that its columns are one, two and two, four. The second column is twice the first. Both arrows point the same way, so the unit square gets squashed onto a single line. '
                         'The area is zero, and the determinant is one times four minus two times two, which is zero. '
                         'Once many different inputs land on the same output, no matrix can send them back, because it would not know which input to return. So there is no inverse. We call such a matrix singular. '
                         'Keep this case in mind for the equations A x equals b: it is where things go wrong.')))

    S.append(dict(kind='table', title='Rank counts how many independent directions the columns give',
                  headers=['Matrix', 'Determinant', 'Rank', 'What the columns can reach'],
                  rows=[['Our A: columns (2, 1) and (1, -1)', '−3', '2', 'The whole plane'], ['Singular: columns (1, 2) and (2, 4)', '0', '1', 'Only one line'], ['Zero matrix: all entries 0', '0', '0', 'Only the origin']],
                  widths=[4.6, 1.9, 1.2, 4.2], icons=False,
                  note='Rank = the largest number of columns you can choose so that none of them can be built from the others. A 2 by 2 matrix has an inverse exactly when its rank is 2.',
                  notes=('Rank is the next word. It is the largest number of columns you can choose so that none of the chosen columns can be built from the others. '
                         'Our matrix has rank two, because its two arrows point in different directions and together they can reach the whole plane. '
                         'The singular matrix has rank one, because the second column is a copy of the first, stretched, so everything lands on one line. The zero matrix has rank zero. '
                         'For a two by two matrix, rank two means a nonzero determinant and an inverse. Rank less than two means determinant zero and no inverse.')))

    S.append(dict(kind='idea', title='A system has one solution, none, or many, and rank and b decide which',
                  visual=dict(kind='sysrows', panels=[dict(title='One solution', lines=[dict(abc=(1, 1, 3), color=MB.INK), dict(abc=(1, -1, 1), color=MB.RED)], pt=(2, 1), caption='x₁ + x₂ = 3\nx₁ − x₂ = 1'),
                                                      dict(title='No solution', lines=[dict(abc=(1, 1, 3), color=MB.INK), dict(abc=(1, 1, 5), color=MB.RED)], caption='x₁ + x₂ = 3\nx₁ + x₂ = 5'),
                                                      dict(title='Many solutions', lines=[dict(abc=(1, 1, 3), color=MB.INK), dict(abc=(2, 2, 6), color=MB.RED)], caption='x₁ + x₂ = 3\n2x₁ + 2x₂ = 6')]),
                  lead='Lines that cross once give one solution. Parallel lines never meet. The same line twice meets everywhere.',
                  points=['Full rank: exactly one solution.', 'Rank below full: no solution or infinitely many, depending on b.'],
                  notes=('Putting it together, a linear system has three possible outcomes. If the lines cross once, there is one solution, and the matrix has full rank. '
                         'If the lines are parallel, they never meet and there is no solution. If the second equation is the first one doubled, the two lines sit on top of each other, and every point on the line is a solution, so there are infinitely many. '
                         'In the last two cases the matrix has rank one, below full, and the right-hand side b decides between none and many.')))

    S.append(dict(kind='idea', title='Fitting a line to 7 data points is 7 equations with only 2 unknowns',
                  visual=dict(kind='designmat_bw', xs=[float(v) for v in x], ys=[float(v) for v in y], xname='spend', yname='sales'),
                  lead='Each row says b + w × spend = sales, for one month. Seven rows, two unknowns: the intercept b and the slope w.',
                  points=['From here on, b and w are the unknowns and X holds the data.', 'The column of ones in X carries b.', 'The points are not on one line, so no exact solution exists.'],
                  notes=('The real problem from machine learning: seven months of advertising spend and sales, both in millions of Uganda shillings, invented to illustrate the arithmetic. '
                         'We want a line, predicted sales y hat equals b plus w times spend. Here b is the intercept, which Session 1 called the bias, and w is the slope, the weight. Every month gives one equation. '
                         'From this slide on, the unknowns are b and w, and the capital X holds the data. X has a column of ones, which carries b, and a column of spend values. That is seven equations and two unknowns, a tall system. '
                         'The points do not lie on one line, so no choice of b and w satisfies all seven.')))

    S.append(dict(kind='idea', title='Least squares picks the line with the smallest sum of squared errors',
                  visual=dict(kind='fitline', points=pts, xlabel='advertising spend (UGX million)', ylabel='sales (UGX million)', line=(bi, ws)),
                  lead='Each dot is one month. The gold bars show its error, also called the residual: actual sales y minus the line\'s prediction ŷ.',
                  points=[f'Line: ŷ = {g(bi)} + {g(ws)} × spend.', f'Least squares makes the sum of squared errors smallest: {g(d["sse"])}.',
                          f'RMSE (root mean squared error) = √({g(d["sse"])} ÷ {n}) = {g(rmse)}.'],
                  notes=('If no line is perfect, choose the best one. For each month, the error is the actual sales y minus the value the line predicts, y hat. It is also called the residual. The gold bars below the picture show them on a larger scale, with their signed size. '
                         'Square each error, so that plus and minus cannot cancel, and big misses count more. Add them up. Least squares chooses the intercept and slope that make this total as small as possible. '
                         f'For our illustrative data the answer is the line y hat equals {g(bi)} plus {g(ws)} times spend, with a total squared error of {g(d["sse"])}. '
                         f'Divide by seven, take the square root, and you get the root mean squared error, RMSE, of {g(rmse)} million: the size of a typical miss.')))

    S.append(dict(kind='formula', title='Errors at right angles to the columns of X give the normal equation',
                  formulas=[('Errors at right angles', r'$X^{T}(\mathbf{y} - X\mathbf{w}) = \mathbf{0}$'), ('Normal equation', r'$(X^{T}X)\,\mathbf{w} = X^{T}\mathbf{y}$')],
                  symbols=[['X', 'The data: a column of ones, then spend. Tall: more rows than unknowns.', f'{n} rows, 2 columns'],
                           ['y, w', 'y: the sales. w (bold): the unknowns in a column, b on top, w below.', '7 sales; (b, w)'],
                           ['y - Xw', 'The errors: actual minus predicted.', '7 errors'],
                           ['Xᵀ(...) = 0', 'Each column of X has dot product 0 with the errors: right angles (Session 2).', '2 equations'],
                           ['XᵀX', 'Square, one row per unknown. If it has an inverse, w = (XᵀX)⁻¹Xᵀy.', '2 by 2']],
                  widths=[1.8, 6.6, 3.5], size=20, note='Multiply out line 1: Xᵀy − XᵀXw = 0, so XᵀXw = Xᵀy.',
                  notes=('Why multiply by X transpose? Picture all the predictions the line could make as a flat surface spanned by the columns of X. The best prediction is the point on that surface closest to y, and the shortest way from a point to a flat surface is at right angles. '
                         'So the error vector, y minus X w, must be at right angles to every column of X. From Session 2, right angles mean a dot product of zero. X transpose times the errors lists those dot products, and we set them to zero. '
                         'Multiply out: X transpose y minus X transpose X w is zero, which rearranges to the normal equation. X transpose X is square, two by two, so we can solve it with the inverse from earlier.')))

    S.append(dict(kind='example', title='Worked by hand: the normal equation for 7 points',
                  scenario='Spend 1, 2, 3, 4, 5, 6, 8 and sales 14, 19, 27, 30, 38, 41, 52 (UGX million, illustrative).',
                  blocks=[dict(label='XᵀX and Xᵀy', text=f'XᵀX: rows ({n}, {sx:.0f}) and ({sx:.0f}, {sx2:.0f}), count, sums of spend and spend squared. Xᵀy = ({sy:.0f}, {sxy:.0f}).'),
                          dict(label='Inverse', text=f'det = {n} × {sx2:.0f} − {sx:.0f} × {sx:.0f} = {det_x:.0f}. Swap and negate: (1/{det_x:.0f}) × rows ({sx2:.0f}, −{sx:.0f}) and (−{sx:.0f}, {n}).'),
                          dict(label='Multiply', text=f'Times ({sy:.0f}, {sxy:.0f}): b = ({sx2:.0f} × {sy:.0f} − {sx:.0f} × {sxy:.0f}) / {det_x:.0f} = {g(bi)}. w = (−{sx:.0f} × {sy:.0f} + {n} × {sxy:.0f}) / {det_x:.0f} = {g(ws)}.'),
                          dict(label='Meaning', text=f'Each extra million of spend goes with {g(ws)} million more sales. At spend 7: {g(p7, 1)}.', red=True)],
                  notes=(f'Do it by hand once. X transpose X works out to rows seven, twenty-nine and twenty-nine, one hundred fifty-five: the count, the sum of spend, and the sum of spend squared. '
                         f'X transpose y is two hundred twenty-one and one thousand one hundred five. The determinant is seven times one fifty-five minus twenty-nine squared, which is two hundred forty-four. '
                         f'The inverse uses the same swap and negate recipe as before. Multiplying it by X transpose y gives b equal to {g(bi)} and w equal to {g(ws)}. So each extra million of spend goes with about {g(ws)} million more sales in this made-up data. '
                         'Be careful with the words goes with. A fitted line shows an association, and it does not by itself prove that spending causes sales.')))

    S.append(dict(kind='compare', title='Two ways to solve: the inverse, or a solver',
                  left=dict(head='Inverse', icon='key', points=['x = A⁻¹b is the idea to understand.', 'Computing the whole inverse takes more work.', 'For large matrices it is usually less accurate.']),
                  right=dict(head='Solvers', icon='gear', points=['solve(A, b) factorises A, a form of elimination.', 'lstsq(X, y) fits by least squares, using the SVD (Session 6).']),
                  verdict='Learn the inverse to understand it. Use a solver to compute.',
                  notes=('After elimination by hand, a computer gives you two more routes. The inverse is the cleanest idea, x equals A inverse times b. '
                         'But computing a whole inverse takes more work and is usually less accurate for large matrices. A solver is the other way. You give the computer A and b, and the function solve factorises A, which is a form of elimination. '
                         'For a least squares fit you can use lstsq directly on X and y. It is based on the singular value decomposition, which we meet in Session 6. In practice people use the solver, and in the lab you will try both and compare.')))

    S.append(dict(kind='idea', title='Too many unknowns and too few rows: infinitely many lines fit perfectly',
                  visual=dict(kind='manyfits', pt=(4, 30), slopes=[1, 3, 5.4, 8, -2], xlabel='advertising spend', ylabel='sales'),
                  lead='One data point and two unknowns, the intercept b and the slope w. Every red line through the point fits it exactly.',
                  points=['With spend 4: XᵀX has rows (1, 4) and (4, 16), and determinant 1 × 16 − 4 × 4 = 0.', 'The rank of X is at most its number of rows, here 1, so the rank of XᵀX is at most 1. No inverse, so the normal equation has many answers.'],
                  notes=('The warning from the real question of the day comes next. Suppose we had a single month of data. One equation, two unknowns. Any line through that point fits perfectly. '
                         'The data cannot choose between them. The rank of X is at most its number of rows, here one, so X transpose X also has rank at most one. Its rows are one, four and four, sixteen, and its determinant is sixteen minus sixteen, which is zero. '
                         'It has no inverse, so the normal equation has many answers. The same happens whenever there are more unknowns than rows. A model with more weights than data points can fit anything, and the fit means nothing. '
                         'Session 12 shows a standard fix, called regularisation.')))

    S.append(dict(kind='table', title='Four mistakes that break a solve, and what to do instead',
                  headers=['Mistake', 'Why it fails', 'What to do'],
                  rows=[['Dividing by a matrix', 'There is no matrix division.', 'Multiply by the inverse, on the left: A⁻¹b.'], ['Inverting when the determinant is 0', 'A singular matrix has no inverse.', 'Check the determinant or the rank first.'],
                        ['Leaving out the column of ones', 'The line is forced through the origin.', 'Add a column of 1s to X for the intercept b.'], ['Swapping the order of a product', 'AB and BA usually differ.', 'Keep A⁻¹ on the left of b.']],
                  widths=[3.7, 4.1, 4.1], icons=['cross', 'cross', 'cross', 'cross'],
                  notes=('Four mistakes come up again and again. First, dividing by a matrix. There is no such operation. You multiply by the inverse, on the left. '
                         'Second, trying to invert a matrix with determinant zero. Check the determinant or the rank first. '
                         'Third, forgetting the column of ones in X. Without it, the intercept is stuck at zero, the line must pass through the origin, and your fit will be poor. '
                         'Fourth, changing the order of a product. A times B is usually not B times A, so keep the inverse on the left.')))

    S.append(dict(kind='code', title='Six NumPy names cover today: solve, det, inv, matrix_rank, lstsq and the transpose',
                  code='x = np.linalg.solve(A, b)\nd = np.linalg.det(A)\nA_inv = np.linalg.inv(A)\nr = np.linalg.matrix_rank(S)\nX = np.column_stack([np.ones(7), spend])\nbw = np.linalg.solve(X.T @ X, X.T @ sales)\nbw2 = np.linalg.lstsq(X, sales, rcond=None)[0]',
                  reads=['solve, det, inv and matrix_rank do what their names say: solve Ax = b, the determinant, the inverse, the rank.', 'X = ... puts a column of ones next to spend.', 'bw = ... is the normal equation. X.T is the transpose, @ is matrix multiplication. bw holds b, then w.',
                         'bw2 = ... is least squares in one call. rcond=None silences a warning, and the final 0 picks the weights.'],
                  notes=('This is the code you will use, seven short lines. The first four come from the same family, np dot linalg: solve returns x, det gives the determinant, inv the inverse, and matrix rank the rank. '
                         'To fit a line, build X by putting a column of ones next to the spend array. The normal equation is X dot T times X, solved against X dot T times sales, and the answer holds b first, then w. '
                         'np dot linalg dot lstsq does the whole least squares problem in one call and should give the same two numbers. The zero in square brackets picks the weights. The notebook explains every line again.')))

    S.append(dict(kind='divider', title='Part 2: the lab', lead='Close the slides. Open the notebook or the workbook.', section='Lab',
                  notes=('That is the end of the ideas. In the lab you do the same calculations on real arrays and cells. Choose the Python notebook or the spreadsheet workbook. The numbers are identical in both, and every step ends with an automatic check. '
                         'For each step, predict first, then run it, then read the output, then change one thing. I will walk around, so raise your hand when a check stays red.')))

    S.append(dict(kind='steps', title='Five lab steps take you from a 2 by 2 solve to a fitted line',
                  steps=[dict(head='1 Solve', text='Solve the 2 by 2 system', icon='calculator'), dict(head='2 Inverse and rank', text='Determinant, inverse, a singular matrix', icon='magnifier'),
                         dict(head='3 The data', text='Seven points and the matrix X with a column of ones', icon='folder'), dict(head='4 Normal equation', text='Compute b and w, then check them', icon='chart'),
                         dict(head='5 Too few rows', text='One row and two unknowns: watch it break', icon='cross')], highlight=3,
                  caption='Python uses np.linalg. The spreadsheet uses MMULT, MINVERSE, MDETERM and TRANSPOSE as array formulas. Gold cells are yours.',
                  notes=('The lab follows the same order as the slides. Step one, solve the two by two system. Step two, find the determinant and the inverse, and meet a singular matrix. '
                         'Step three, load the seven data points and build X. Step four, the main event: solve the normal equation and get the intercept b and the slope w. Step five, break it on purpose with too few rows. '
                         'In Python you use numpy. In the spreadsheet you use array formulas such as MMULT and MINVERSE. Predict before you run each step.')))

    S.append(dict(kind='table', title=f'Your numbers should match: 2 and 1, then b = {g(bi)} and w = {g(ws)}',
                  headers=['What you compute', 'You should see'],
                  rows=[['Solution x₁ and x₂ of the 2 by 2 system', f'{g(sol[0], 0)} and {g(sol[1], 0)}'], ['Determinant of A', f'{d["det"]:.0f}'.replace('-', '−')], ['Top-left entry of the inverse of A', '0.33 (that is 1/3)'],
                        ['Rank of the singular matrix (rows (1, 2) and (2, 4))', str(d['rankS'])], ['XᵀX for the seven points', f'rows ({n}, {sx:.0f}) and ({sx:.0f}, {sx2:.0f})'],
                        ['Intercept b and slope w', f'{g(bi)} and {g(ws)}'], ['Total squared error, then RMSE', f'{g(d["sse"])}, then {g(rmse)} (UGX million)'], ['Determinant of XᵀX with one row', '0']],
                  widths=[7.2, 4.0], icons=['calculator', 'key', 'key', 'flag', 'grid', 'chart', 'chart', 'cross'],
                  note='If a number differs, stop and find the step that went wrong. Do not type a number to make a check green.',
                  notes=('Use this table as your checkpoint. If your numbers match, carry on. If they do not, stop and call me over, because every later step uses the earlier ones. '
                         'The usual causes are a missing column of ones, X transpose typed as X, or a range that is one row too short in the spreadsheet. '
                         'The root mean squared error comes from the total squared error: divide by seven, then take the square root. Please do not edit a number just to make a check pass. '
                         'Finding out why it differs is the skill you take away.')))

    S.append(dict(kind='table', title='Singular matrices, shapes and array formulas cause most lab errors',
                  headers=['Error or symptom', 'What it says', 'What to do'],
                  rows=[['LinAlgError: Singular matrix', 'The matrix has determinant 0, so no inverse.', 'Check the rank. Use lstsq instead.'], ['ValueError: shapes not aligned', 'The inner sizes of a product do not match.', 'Print .shape of both and compare.'],
                        ['#SPILL! or #N/A from an array formula', 'Excel 365: cells below are not empty. Older Excel: the selected range has the wrong size.', 'Clear the cells, or select the exact range. Older Excel: Ctrl+Shift+Enter. Excel 365 and Sheets: Enter.'], ['Intercept b comes out 0', 'The column of ones is missing from X.', 'Add the column of ones.']],
                  widths=[3.4, 4.2, 4.4], icons=['cross', 'key', 'bell', 'flag'],
                  notes=('Errors are normal, and these four are the likely ones. Singular matrix means the determinant is zero, so check the rank and use lstsq. '
                         'Shapes not aligned means a product has mismatched inner sizes, so print the shape of both sides. '
                         'In the spreadsheet, a spill error in Excel 365 means the cells the answer wants to fill are not empty. In older Excel you select the exact range and confirm with control, shift and enter. Google Sheets and Excel 365 only need enter. '
                         'And an intercept of zero means the column of ones is missing. Read the last line of any error first.')))

    S.append(dict(kind='idea', title='Where this appears in AI: solving in one step, or improving in small steps',
                  visual=dict(kind='versus', left=dict(head='Linear regression', big='Direct', unit='one formula', icon='calculator'),
                              right=dict(head='Neural networks', big='Many', unit='small steps', icon='gear'), middle='when no direct formula exists'),
                  lead='Linear regression has a closed-form answer. Models of this kind learn in many small updates.',
                  points=['Published work trains them with Adam, in small steps.', 'Transformer layers (Vaswani et al., 2017) are mostly matrix multiplications.',
                          'Too many unknowns: add a penalty (ridge, Session 12).'],
                  notes=('So where does today appear in ChatGPT, Gemini, Claude and other AI? Fitting a line has a direct solution, the normal equation you just used, and it is still a workhorse for small models. '
                         'The big language models are different. Published research describes training them with gradient-based optimisation, usually the Adam family, which makes many small updates, because no single formula gives the answer. '
                         'The layers of a transformer, as described by Vaswani and colleagues in 2017, are built mainly from matrix multiplications. When there are more unknowns than rows, many fits are exact, and published remedies add a penalty, called ridge regression. '
                         'Gradient methods start in Session 10.')))

    S.append(dict(kind='practice', title='Where this appears in AI: ask an assistant for the line, then check it', minutes=8, label='Hands-on, with any AI assistant',
                  task='Ask an assistant to fit the line, then check it against yours.',
                  steps=['Type the seven spend and sales values from the worked example. Never paste confidential data.', 'Ask for a least squares line with the normal equation steps.', f'Compare its intercept and slope with {g(bi)} and {g(ws)}.', 'Compare its determinant of XᵀX with 244.'],
                  output='A note of where the assistant agrees with your numbers, and where it differs.',
                  notes=('A short activity. Open any AI assistant that you use. Type in our seven made-up values and ask for the least squares line with the normal equation steps. '
                         f'Then compare its intercept and slope with ours, {g(bi)} and {g(ws)}, and its determinant with two hundred forty-four. Assistants can make arithmetic slips, and checking is the skill. '
                         'Please never paste confidential company data into an assistant. Use only the invented numbers on the slide, and note where its working differs from yours.')))

    S.append(dict(kind='table', title='Exit check: the determinant, the column of ones, and too few rows',
                  headers=['Question', 'Short answer'],
                  rows=[['What does a determinant of 0 tell you about Ax = b?', 'A has no inverse. There is no solution or infinitely many, depending on b.'],
                        ['Why do we need a column of ones in X?', 'It carries the intercept b. Without it the line passes through the origin.'],
                        ['Why does one data point and two unknowns break the normal equation?', 'XᵀX has determinant 0 and rank 1, so many lines fit equally well.']],
                  widths=[5.4, 6.6], icons=False, note='Write your own answer first, then compare. Your lab checks are part of the exit check.',
                  notes=('Three questions to finish. What does a determinant of zero tell you? A has no inverse, so the system has no solution or infinitely many, depending on b. '
                         'Why a column of ones in X? It carries the intercept b. Without it the line is forced through the origin. '
                         'And why does one data point with two unknowns break the normal equation? Because X transpose X then has determinant zero and rank one, so many lines fit equally well. '
                         'Answer in your own words before you look at these.')))

    s['facilitator'] = dict(
        prep=['Open the deck in slide show mode, and the notebook and the workbook, and run both once so you know they work on your account.',
              'Share the notebook link and the workbook file before the break. Learners choose one track; the numbers are identical.',
              f'Write the check numbers on the board: 2 and 1; determinant -3; intercept b {g(bi)}; slope w {g(ws)}.',
              'Have a ruler or a printed grid ready for the determinant picture if the room is small.',
              'Letters: in Ax = b, b is the right-hand side. From the line fit on, b is the intercept and w the slope, as in Sessions 1, 8 and 10.'],
        misconceptions=[('Solving Ax = b means dividing by A', 'There is no division of matrices. We multiply by the inverse, on the left, or use a solver.'),
                        ('A bigger determinant means a better matrix', 'The size of the determinant is an area factor. Zero is the case to worry about, and tiny values make the solve unreliable.'),
                        ('More features always make the fit better', 'On training data they can only lower the error, but with too few rows the fit is not unique and does not generalise.'),
                        ('The fitted slope proves advertising causes sales', 'It shows an association in these (illustrative) numbers. Causation needs more than a line.')],
        probes=[('Draw the two lines for x₁ + x₂ = 3 and x₁ + x₂ = 5. What does rank tell you here?', 'The lines are parallel, so rank is 1 and there is no solution.'),
                ('Why is XᵀX always square?', 'X is n by d, so Xᵀ is d by n, and the product is d by d.'),
                ('Why does multiplying by Xᵀ give the best fit?', 'Xᵀ(y − Xw) = 0 says the errors have dot product 0 with every column of X: they are at right angles, which is the shortest miss.'),
                ('What would happen to the fit if we added a column of random numbers to X?', 'The training error cannot go up, but the extra weight is fitted to noise, and with too few rows XᵀX can become singular.')],
        lab_steps=[('Step 1: solve', 'Python: array (2., 1.). Sheet: MINVERSE then MMULT. Both give 2 and 1. If a learner gets 1 and 2, they swapped the order of the unknowns.'),
                   ('Step 2: determinant, inverse, rank', 'Determinant -3 and inverse top-left 0.33. The singular matrix gives rank 1 in Python and determinant 0 in the sheet (no rank function in both tools).'),
                   ('Step 3: the data and X', 'X is 7 by 2. In the sheet the ones column is easy to forget. Intercept zero is the symptom.'),
                   ('Step 4: the normal equation', f'b {g(bi)}, w {g(ws)}; total squared error {g(d["sse"])}, RMSE {g(rmse)}. Python also compares with lstsq. The sheet reads off the same numbers from MMULT and MINVERSE.'),
                   ('Step 5: too few rows', 'One row: determinant of XᵀX is 0 and the rank is 1. Ask what the data cannot decide.')],
        rescue=['If the concepts overrun, skip the compare slide and say: use a solver in practice.', 'If only 30 minutes of lab remain, do steps 1, 3 and 4 and set step 2 and 5 as practice.',
                'If array formulas cause trouble in a spreadsheet, show the 2 by 2 solution by the formula for the inverse, entry by entry.'],
        after=['Share the solution notebook after class, not before.', 'Ask learners to bring one question about Session 5, which builds on rank and the determinant.'],
        lab_answer_key=[['PREDICT, step 1: what are x₁ and x₂?', '2 and 1'], ['READ, step 2: what does the determinant -3 mean?', 'Areas are scaled by 3 and flipped.'],
                        ['CHANGE, step 2: rows (1, 2) and (2, 4), what is the rank?', '1, and the determinant is 0.'], ['READ, step 4: what is the slope w?', f'{g(ws)} million of sales per million of spend (illustrative).'],
                        ['CHANGE, step 5: use only one data row', 'XᵀX has determinant 0; many lines fit.']])
    return s
