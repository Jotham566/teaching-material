"""Session 3: Matrices. Every number on the slides is computed here with numpy and reused by the lab files."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'kit'))
import diagrams_math_a  # noqa: E402,F401

# ---------------------------------------------------------------- numbers
NAMES = ['Amina', 'Brian', 'Chloe']
L = np.array([[21, 6, 72], [25, 3, 58], [19, 8, 85]])            # the three learners of Session 2: age, hours, score
A = np.array([[1, 2, 3], [4, 5, 6]])                              # 2 x 3
B = np.array([[7, 8], [9, 10], [11, 12]])                         # 3 x 2
X3 = np.array([1, 2, 3])
SHAPE = np.array([[0, 0], [2, 0], [2, 1], [1, 1], [1, 3], [0, 3]]).T   # the L-shaped drawing as a 2 x 6 matrix, one point per column
SHEAR = np.array([[1, 1], [0, 1]])
SCALE = np.array([[2, 0], [0, 1]])
ROT = np.array([[0, -1], [1, 0]])
W1 = np.array([[1, 0, 2], [0, 1, -1], [2, 1, 0], [-1, 1, 1]])   # 4 x 3
B1 = np.array([0.5, 0.0, -1.0, 0.5])
W2 = np.array([[1, 0, 1, 0], [0, 1, 0, 2]])                      # 2 x 4
B2 = np.array([0.0, 1.0])
XT = np.array([[1, 0, 2], [0, 1, 1], [2, 1, 0], [1, 1, 1]])      # four tokens, three numbers each (illustrative)
WT = np.array([[1, 0, 1], [0, 2, 1]])                            # token layer: 3 inputs -> 2 outputs, stored outputs x inputs (2 x 3)
U3, V3 = np.array([1, 2, 3]), np.array([4, 0, 2])
U7 = np.array([2, 3, 6])


def pc(n_in, n_out):
    return n_in * n_out + n_out


def facts():
    Y1 = W1 @ X3 + B1
    return dict(Ax=A @ X3, AB=A @ B, BA=B @ A, AT=A.T, L23=int(L[1, 2]), shear_pt=(SHEAR @ SHAPE)[:, 4], rot_pt=(ROT @ SHAPE)[:, 4], scale_pt=(SCALE @ SHAPE)[:, 4],
                Y1=Y1, OUT=W2 @ Y1 + B2, W2W1=W2 @ W1, nob=W2 @ (W1 @ X3), nob2=(W2 @ W1) @ X3, XW=XT @ WT.T, XB=np.array([[1, 2, 3], [0, 1, 1]]) @ W1.T + B1, par=pc(3, 4) + pc(4, 2), par1000=pc(1000, 1000), par4096=4096 * 4096,
                gb7=7e9 * 2 / 1e9, mult=2 * 3 * 2, mult4096=4096 ** 3, dot3=int(U3 @ V3), norm7=float(np.linalg.norm(U7)))


def fmt(v):
    return f'{v:g}'


def build():
    F = facts()
    s = dict(
        num=3, block='Linear algebra', short_title='Matrices',
        title='Matrices: tables of numbers that also move vectors, and the core arithmetic of a neural-network layer',
        question='A language model has billions of parameters. What are those numbers, and what does the model do with them?',
        outcomes=['Read a matrix as a table and as a transformation, and state its shape (rows by columns)',
                  'Multiply a matrix by a vector and a matrix by a matrix by hand, and say when the shapes allow it',
                  'Compute a layer y = W x + b, and count the parameters of a small network, in Python and in a spreadsheet'],
        outcome_icons=['grid', 'calculator', 'gear'],
        outcome_note=('By the end of today you can read a matrix as a table of numbers and as a transformation that moves points, and you can state its shape. '
                      'You can multiply a matrix by a vector and a matrix by a matrix by hand, and say when the shapes allow it. '
                      'And you can compute one layer of a neural network, y equals W x plus b, and count its parameters. That last step shows what billions of parameters means.'),
        clock=[(10, 'Recall, then a real question from AI'), (35, 'Concept: a picture, then one example by hand'), (10, 'Break'), (45, 'Lab: predict, run, then change one thing'),
               (15, 'Where it appears in AI, and an exit check'), (5, 'Save the work')],
        plan_title='Your two hours: matrices, then the lab, then parameters',
        plan_caption='Pictures and hand calculations first. Then the lab on products, layers and parameters.',
        plan_note=('The first ten minutes recall Session 2 and pose today question about billions of parameters. Then thirty-five minutes of ideas, each with a picture and a small calculation by hand, a break, and a forty-five minute lab in Python or in a spreadsheet. '
                   'The last fifteen minutes show where matrices appear in language models, and give you an exit check. Then you save your work.'),
        recall_from='Session 2',
        recall=[('What is the dot product of (1, 2, 3) and (4, 0, 2)? Is the result a vector or a number?', f'{F["dot3"]}. It is one number: 1 × 4 + 2 × 0 + 3 × 2.'),
                ('What is the L2 norm (length) of the vector (2, 3, 6)?', '7, because 4 + 9 + 36 = 49 and the square root of 49 is 7.'),
                ('Why does a search tool rank by cosine similarity and not by the raw dot product?', 'Cosine similarity divides by both lengths, so a long vector does not win just for being long. Only the direction counts.')],
        words=[('Matrix', 'A table of numbers with m rows and n columns. Its shape is m × n.'),
               ('Matrix multiplication', 'A rule that combines two matrices. Each entry of the answer is a dot product of a row and a column.'),
               ('Transpose', 'The matrix flipped so that rows become columns. It is written with a small T.'),
               ('Identity matrix', 'A square matrix of 1s on the diagonal and 0s elsewhere. It leaves every vector unchanged.'),
               ('Parameters', 'The numbers inside a model that training sets: its weights W and biases b.')],
        word_icons=['grid', 'calculator', 'switch', 'key', 'gear'],
        words_note=('Five words for today. A matrix is a table of numbers with m rows and n columns. Matrix multiplication combines two matrices, and every entry of the answer is a dot product from Session 2. '
                    'The transpose flips rows into columns. The identity matrix leaves a vector unchanged. And the parameters of a model are the numbers that training sets, the weights W and the biases b. We use all five before the end.'),
        keep='Keep your saved notebook or workbook, with every check on OK. Keep the idea of the day: a layer is y = W x + b, and the parameters of a model are the numbers in its matrices and biases.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Your lab file', value='Saved, all checks OK'), dict(label='The idea', value='y = W x + b'),
                                                                 dict(label='Formula sheet', value='Shape rule; Cᵢₖ = Σ Aᵢⱼ Bⱼₖ; m n + m'), dict(label='Next session', value='Solving linear systems')]),
        keep_title='Save your lab file and add three rules to your sheet',
        next='Session 4: Solving linear systems. We write equations as a matrix, and meet the inverse, the determinant and the rank.', next_label='Next session',
        keep_note=('Before you go, save your notebook or workbook with every check on OK. Add three rules to your one-page sheet: the shape rule for multiplying matrices, the matrix product as a sum of products, and the parameter count of a layer, m times n plus m. '
                   'Next session we use matrices to solve systems of equations, and we meet the inverse, the determinant and the rank. Write down any question that you still have and bring it.'),
        cover_note=('Welcome back. Last session we met vectors, and measured how alike two of them are. Today we stack vectors into a matrix. '
                    'A matrix is a table of numbers, and it is also a machine that moves points. By the end you will know exactly what people mean when they say a model has billions of parameters.'),
        slides=[])
    S = s['slides']

    S.append(dict(kind='table', title='Answers to the three questions from Session 2', headers=['Question', 'Short answer'], rows=[[q, a] for q, a in s['recall']], widths=[5.4, 6.6], icons=False,
                  note='If one answer surprised you, look again at the Session 2 slides before the lab.',
                  notes=('The short answers. First, the dot product of one two three with four zero two is ten, a single number: one times four, plus two times zero, plus three times two. '
                         'Second, the L2 norm of two, three, six is seven, because four plus nine plus thirty-six is forty-nine. '
                         'Third, search tools rank by cosine similarity because it divides by both lengths, so a long vector does not win just for being long. Only the direction counts. Today every entry of a matrix product is one of these dot products.')))

    S.append(dict(kind='idea', title='A matrix is a table of numbers with rows and columns',
                  visual=dict(kind='ma_matgrid', values=L.tolist(), hl=(1, 2), row_labels=NAMES, shape_text='L is a 3 × 3 matrix: 3 rows and 3 columns'),
                  lead='Matrix: a table of numbers. Here L holds three learners from Session 2, one per row: age, hours, score.',
                  points=['Each row is a vector: Amina = (21, 6, 72).', 'Gold entry: row 2, column 3 is 58, Brian\'s score.', 'Illustrative (made-up numbers to show the arithmetic).'],
                  notes=('A matrix is a table of numbers. This one, called L for learners, holds the three learners from last session, with age, hours studied per week and quiz score. These numbers are made up. '
                         'Each row is a vector, so a matrix is also a stack of vectors. Each column holds one kind of measurement. The gold entry is in row two and column three, and it is fifty-eight, the score of Brian. '
                         'Always say the row first, then the column. What is the entry in row three and column one?')))

    S.append(dict(kind='formula', title='A capital letter names the matrix, and two small numbers pick one entry',
                  formulas=[('Shape', r'$A \in \mathbb{R}^{m \times n}$  (A is m × n)'), ('Entry in row i, column j', r'$A_{ij}$'), ('Our table', r'$L \in \mathbb{R}^{3 \times 3}, \qquad L_{23} = 58$')],
                  symbols=[['A, L', 'A matrix is written with a capital letter. A vector is a lowercase bold letter.', 'L = the learner table'],
                           ['m × n', 'The shape: m rows by n columns. Rows are always named first.', '3 × 3'],
                           ['∈ and ℝ', '∈ reads "is a". ℝ is the real numbers: ordinary numbers with decimals.', 'L is a 3 × 3 table of real numbers'],
                           ['Aᵢⱼ', 'The entry in row i, column j of A (small i and j below the A).', 'L₂₃ = 58']],
                  widths=[2.0, 6.5, 3.4], size=22, note='Python counts from 0, so L₂₃ has row index 1 and column index 2. A spreadsheet counts from 1: INDEX(range, 2, 3).',
                  notes=('Matrix notation has three parts. A matrix has a capital letter, such as A. Its shape is written m by n, which means m rows and n columns, and the rows come first. '
                         'Papers write the shape with two symbols you will meet often. The curly e reads is a, and the double-struck R means the real numbers, the ordinary numbers with decimals. An entry has the row number first and the column number second, so L two three is fifty-eight. '
                         'Watch out in Python: it counts from zero, so the same entry has row index one and column index two. A spreadsheet counts from one.')))

    S.append(dict(kind='wide', title='A matrix can also move points: scaling, rotating and shearing a shape',
                  visual=dict(kind='ma_transform', panels=[dict(title='Scale', M=SCALE.tolist(), M_text='rows (2, 0) and (0, 1)', note='doubles every x, keeps y'), dict(title='Rotate', M=ROT.tolist(), M_text='rows (0, −1) and (1, 0)', note='quarter turn anticlockwise'),
                                                           dict(title='Shear', M=SHEAR.tolist(), M_text='rows (1, 1) and (0, 1)', note='slides each point right by its height')]),
                  caption='Grey dashed: the original shape. Gold: the result. The rotation sends the corner (1, 3) to (−3, 1).',
                  notes=('A matrix has a second life. It can move every point of a drawing. The dashed grey shape is an L-shaped drawing. In the first panel the matrix with rows two zero and zero one doubles every x value and keeps y. '
                         'In the second panel the matrix with rows zero minus one and one zero turns the whole shape a quarter turn anticlockwise, so the corner one, three goes to minus three, one. In the third, the matrix with rows one one and zero one shears the shape, which slides each point right by its height. '
                         'In each case the matrix is a small table of four numbers. A transformation is a rule that moves every point. Which one keeps the shape exactly as it was, only turned? The scale also doubles the area, and Session 4 returns to that.')))

    S.append(dict(kind='idea', title='The columns of a matrix show where the two axis arrows land',
                  visual=dict(kind='ma_transform', panels=[dict(title='Shear M', M=SHEAR.tolist(), M_text='red arrow: (1, 0), black arrow: (0, 1)')], axes_arrows=True),
                  lead='M has rows (1, 1) and (0, 1). Red arrow (1, 0) lands on (1, 0). Black arrow (0, 1) lands on (1, 1). These two are the columns of M.',
                  points=['Every other point follows: the grid tilts.', 'Corner (1, 3) lands on (4, 3). The next two slides show the rule and the working.', 'To read a transformation, read the columns.'],
                  notes=('The columns give a quick way to read a transformation. Take the shear matrix with rows one one and zero one. The red arrow pointing along x lands on the first column of the matrix, one zero. '
                         'The black arrow pointing along y lands on the second column, one one. Because a matrix treats the grid evenly, every other point follows these two arrows, and the whole grid is tilted. '
                         'So to see what a matrix does, look at its columns. The corner at one, three of our shape lands on four, three. The calculation comes next.')))

    S.append(dict(kind='idea', title='Matrix times vector: each entry of the answer is a dot product of one row with the vector',
                  visual=dict(kind='ma_matvec', A=A.tolist(), x=X3.tolist(), row=0, work='1 × 1 + 2 × 2 + 3 × 3 = 14'),
                  lead='Multiply A (2 × 3) by x (3 entries). Dot each row of A with x in turn.',
                  points=['Row 1: 1 × 1 + 2 × 2 + 3 × 3 = 14, the gold entry.', 'Row 2: 4 × 1 + 5 × 2 + 6 × 3 = 32.', 'The answer y = (14, 32) has one entry per row of A.'],
                  notes=('Multiplication comes next. A matrix times a vector is built from dot products, which you know from Session 2. Take the first row of A, one two three, and the vector x, one two three. '
                         'Multiply matching entries and add: one, plus four, plus nine, which is fourteen. That is the first entry of the answer. '
                         'The second row, four five six, gives four plus ten plus eighteen, which is thirty-two. So the answer is the vector fourteen, thirty-two, with one entry for every row of A. A third row in A would add a third entry to the answer.')))

    S.append(dict(kind='formula', title='Matrix times vector as a formula, and the same calculation for a point of the shape',
                  formulas=[('Matrix times vector', r'$y_i = \sum_{j=1}^{n} A_{ij}\, x_j$'), ('Shear, corner (1, 3)', r'$1\times 1 + 1\times 3 = 4,\qquad 0\times 1 + 1\times 3 = 3$')],
                  symbols=[['Aᵢⱼ', 'Entry in row i, column j of A.', 'A₁₂ = 2'], ['xⱼ', 'Entry j of the vector x. It meets column j of A.', 'x₂ = 2'],
                           ['yᵢ', 'Entry i of the answer: the dot product of row i of A with x.', 'y₁ = 14'], ['Σ, j, n', 'Add up over j = 1 to n, the columns of A.', 'n = 3'],
                           ['Shear on (1, 3)', 'Row 1 of M with (1, 3), then row 2 of M with (1, 3).', 'The point (1, 3) lands on (4, 3)']],
                  widths=[2.0, 6.4, 3.5], size=19, note='Python: A @ x. Spreadsheet: =MMULT(A, x) as an array formula.',
                  notes=('As a formula, the entry i of the answer is the sum, over j, of the entry in row i and column j of A, times entry j of x. That is the dot product of row i with x. '
                         'We can use it on the shear matrix. The corner one, three of our shape: row one of M is one, one, and gives one times one plus one times three, which is four. Row two is zero, one, and gives three. So the point lands on four, three. '
                         'In Python you write A at x. In a spreadsheet you write MMULT as an array formula.')))

    S.append(dict(kind='idea', title='Matrix times matrix: each entry of the answer is a dot product of a row of A with a column of B',
                  visual=dict(kind='ma_matmul', A=A.tolist(), B=B.tolist(), row=0, col=1, work='1 × 8 + 2 × 10 + 3 × 12 = 64'),
                  lead='Multiply A (2 × 3) by B (3 × 2). Entry (i, k) of the answer is row i of A dotted with column k of B.',
                  points=['Gold: row 1 of A, column 2 of B: 8 + 20 + 36 = 64.', f'C = A B has rows ({F["AB"][0][0]}, {F["AB"][0][1]}) and ({F["AB"][1][0]}, {F["AB"][1][1]}).', 'C has the rows of A and the columns of B: 2 × 2.'],
                  notes=('Multiplying two matrices repeats the same idea. Every entry of the answer is a dot product of one row of A with one column of B. The gold entry sits in row one and column two, so we take row one of A, which is one two three, and column two of B, which is eight, ten, twelve. '
                         'One times eight, plus two times ten, plus three times twelve, is eight plus twenty plus thirty-six, which is sixty-four. Do the same for the other three entries and you get fifty-eight, sixty-four, one hundred thirty-nine, one hundred fifty-four. '
                         'The answer has the rows of A and the columns of B. Row two with column one gives one hundred thirty-nine.')))

    S.append(dict(kind='formula', title='The matrix product as a formula, with a count of the multiplications',
                  formulas=[('Matrix product', r'$C_{ik} = \sum_{j=1}^{n} A_{ij}\, B_{jk}$'), ('Our entry', r'$C_{12} = 1\times 8 + 2\times 10 + 3\times 12 = 64$')],
                  symbols=[['A, B, C', 'A is m × n, B is n × p. Then C = A B is m × p.', 'C is 2 × 2'], ['Σ, j, n', 'Add up over j = 1 to n.', 'j = 1, 2, 3'],
                           ['Cᵢₖ', 'Row i of A dotted with column k of B.', 'C₁₂ = 64'],
                           ['Cost', 'm × p entries, n multiplications each.', f'2 × 3 × 2 = {F["mult"]}']],
                  widths=[2.0, 6.3, 3.6], size=22, note='Python: A @ B. Spreadsheet: =MMULT(A, B) over a 2 × 2 range, entered as an array formula.',
                  notes=('The matrix product as a formula: the entry in row i and column k is the sum over j of A i j times B j k. The index j runs along the row of A and down the column of B, and it disappears in the sum. '
                         f'Our entry C one two is sixty-four. We can count the work too. C has m times p entries, and each entry needs n multiplications, so the total is m times n times p. For our small case that is {F["mult"]} multiplications. '
                         'Remember this count, because it grows fast, and it explains why computers for AI are built the way they are.')))

    S.append(dict(kind='idea', title='Shapes must match: inner numbers agree, outer numbers give the answer\'s shape',
                  visual=dict(kind='ma_shapes'),
                  lead='A (m × n) times B (n × p) works when the columns of A equal the rows of B. The answer is m × p.',
                  points=['2 × 3 times 3 × 4 works: inner 3 and 3. The answer is 2 × 4.', '2 × 3 times 2 × 3 fails: a row has 3 entries, a column 2.', 'Check the shapes first.'],
                  notes=('Not every pair of matrices can be multiplied. Each entry is a dot product of a row of A with a column of B, and a dot product needs two vectors of the same length. '
                         'So the number of columns of A must equal the number of rows of B. In the top picture, two by three times three by four works, because the inner numbers are both three. The answer takes the outer numbers, two by four. '
                         'In the bottom picture the inner numbers are three and two, so a row of three entries meets a column of two entries, and there is no answer. Would three by two times three by two work?')))

    S.append(dict(kind='compare', title='The order matters: A B and B A are different matrices',
                  left=dict(head='A B', points=['A 2 × 3, B 3 × 2.', f'A B is 2 × 2, rows ({F["AB"][0][0]}, {F["AB"][0][1]}) and ({F["AB"][1][0]}, {F["AB"][1][1]}).', 'Works: inner 3 and 3.']),
                  right=dict(head='B A', points=['B 3 × 2, A 2 × 3.', f'B A is 3 × 3, first row {tuple(int(v) for v in F["BA"][0])}.', 'Works: inner 2 and 2.']),
                  verdict='The order matters: A B is usually different from B A.',
                  notes=('With ordinary numbers, three times five equals five times three. Matrices do not behave that way. Here A times B is two by two, with entries fifty-eight, sixty-four, one thirty-nine, one fifty-four. '
                         f'But B times A is three by three, starting with the row {F["BA"][0].tolist()[0]}, {F["BA"][0].tolist()[1]}, {F["BA"][0].tolist()[2]}. Different shape, different numbers. '
                         'Sometimes B times A is not possible at all. So in a formula, the order of the matrices is part of the meaning. In a neural network the order is the order of the layers.')))

    S.append(dict(kind='idea', title='The transpose flips rows into columns',
                  visual=dict(kind='ma_transpose', A=A.tolist()),
                  lead='Transpose: write each row of A as a column. The result is written Aᵀ, with a small T.',
                  points=['A is 2 × 3, so Aᵀ is 3 × 2.', 'Entry (i, j) of A becomes entry (j, i).', 'Dot product: u · v equals uᵀ v.'],
                  notes=('The transpose flips a matrix so that rows become columns. Our A has two rows and three columns. Its transpose has three rows and two columns. The first row of A, one two three, becomes the first column of A transpose. '
                         'In terms of entries, the entry in row i and column j moves to row j and column i. You will see the small T everywhere in machine learning papers. For example, the dot product of two vectors u and v is the product of u transpose, a row, with v, a column. '
                         'The transpose of a three by three matrix such as our learner table is again three by three, with the rows and columns swapped.')))

    S.append(dict(kind='formula', title='The dot product is a matrix product of a row and a column',
                  formulas=[('Dot product as a matrix product', r'$\mathbf{u}\cdot\mathbf{v} = \mathbf{u}^{T}\mathbf{v}$'), ('Our numbers', r'$(1,\ 2,\ 3)\cdot(4,\ 0,\ 2) = 1\times 4 + 2\times 0 + 3\times 2 = 10$')],
                  symbols=[['uᵀ', 'The transpose of u: a row of 3 numbers, a 1 × 3 matrix.', '(1, 2, 3)'], ['v', 'A column of 3 numbers, a 3 × 1 matrix.', '(4, 0, 2)'],
                           ['uᵀ v', 'Shapes: 1 × 3 times 3 × 1. The inner numbers match and the answer is 1 × 1: one number.', f'{F["dot3"]}']],
                  widths=[2.0, 6.7, 3.2], size=22, note='From now on a vector stands as a column; on paper we still write (1, 2, 3) across to save space. A row is written uᵀ.',
                  notes=('From today a vector stands as a column, a matrix with one column. On paper I still write it across the page to save space, as in Session 2, and when I mean a row I write the transpose, u with a small T. '
                         'The dot product of u and v is the matrix product of u transpose and v. Check the shapes: one by three, times three by one. The inner numbers match, and the answer is one by one, which is a single number. '
                         'With one, two, three and four, zero, two we get ten, as at the start of the session. So a matrix product is a whole table of dot products, computed at once.')))

    S.append(dict(kind='idea', title='The identity matrix leaves every vector unchanged',
                  visual=dict(kind='ma_matvec', A=[[1, 0, 0], [0, 1, 0], [0, 0, 1]], x=[3, 4, 5], row=1, work='0 × 3 + 1 × 4 + 0 × 5 = 4', names=('I', 'x', 'I x = x'), caption='The gold row of I picks the gold entry of x'),
                  lead='Identity matrix I: 1s on the diagonal, 0s everywhere else. For any vector x, I x = x.',
                  points=['Each row of I picks one entry of x. Row 2 picks 4.', 'It is the matrix version of multiplying by 1.', 'Session 4 uses it to define the inverse.'],
                  notes=('The identity matrix has ones on the diagonal and zeros everywhere else. Multiply it by any vector and you get the same vector back. In the picture, row two of the identity is zero, one, zero. '
                         'Its dot product with three, four, five is zero plus four plus zero, which is four, the second entry. Each row picks out one entry. '
                         'It is the matrix version of multiplying a number by one. It matters in Session 4, where the inverse of a matrix is the matrix that gives the identity when you multiply by it.')))

    S.append(dict(kind='idea', title='A linear layer computes y = W x + b; real layers then apply an activation function',
                  visual=dict(kind='ma_layer', x=X3.tolist(), y=F['Y1'].tolist(), hl=0, wrow=W1[0].tolist()),
                  lead='A neural network is a chain of layers. This layer turns 3 inputs x into 4 outputs y. W is the weight matrix (4 × 3), b the bias vector.',
                  points=['Illustrative: x = (1, 2, 3).', 'Output 1 (dark lines): 1 × 1 + 0 × 2 + 2 × 3 = 7, plus bias 0.5 gives 7.5. The weight from x₂ is 0 (dashed).', 'Training sets W and b: the parameters.'],
                  notes=('This is the most important use of a matrix in AI. A neural network is a chain of layers, and one linear layer turns a vector x of inputs into a vector y of outputs. The rule is y equals W x plus b. '
                         'W is a matrix of weights, one weight on every line in the picture, and b is a vector of biases, one for each output. Our numbers are illustrative: x is one, two, three. '
                         'The dark lines are row one of W. Its weights one, zero and two give one plus zero plus six, which is seven. Add the bias, zero point five, and the first output is seven point five. The values of W and b are what training sets, so they are the parameters. A real layer then also applies an activation function, which we meet in Session eleven.')))

    S.append(dict(kind='formula', title='The layer y = W x + b, with every symbol named and worked in full',
                  formulas=[('One linear layer', r'$\mathbf{y} = W\mathbf{x} + \mathbf{b}$'), ('Our numbers', r'$\mathbf{y} = (7.5,\ -1,\ 3,\ 4.5)$')],
                  symbols=[['x', 'The input vector, 3 entries.', '(1, 2, 3)'], ['W', 'The weight matrix, 4 × 3: 4 outputs, 3 inputs.', 'rows (1, 0, 2), (0, 1, −1), (2, 1, 0), (−1, 1, 1)'],
                           ['W x', 'Four dot products: 7, −1, 4 and 4.', '(7, −1, 4, 4)'], ['b', 'The bias vector. It is added entry by entry.', '(0.5, 0, −1, 0.5)'],
                           ['y', 'The output: W x + b.', f'({fmt(F["Y1"][0])}, {fmt(F["Y1"][1])}, {fmt(F["Y1"][2])}, {fmt(F["Y1"][3])})'.replace('-', '−')]],
                  widths=[1.6, 5.2, 5.1], size=21, note='A real layer then applies an activation function to each output (Session 11). Python: W @ x + b.',
                  notes=('Every symbol of the layer, named. x has three entries. W is four by three, and the shapes match, because the inner numbers are three and three. '
                         'W times x is four dot products, giving seven, minus one, four and four. Then we add the bias b entry by entry: zero point five, zero, minus one and zero point five. The output y is seven point five, minus one, three and four point five. '
                         'The shape rule gave us the shape of y before we calculated anything: four by three times three gives four. A real layer then adds one more step, an activation function, which we meet in Session eleven.')))

    S.append(dict(kind='formula', title='Layer 2 takes the 4 outputs of layer 1 as its inputs',
                  formulas=[('Layer 2', r'$\mathbf{y}_2 = W_2\,\mathbf{y}_1 + \mathbf{b}_2$'), ('Our numbers', r'$W_2\,\mathbf{y}_1 = (10.5,\ 8),\qquad \mathbf{y}_2 = (10.5,\ 9)$')],
                  symbols=[['y₁', 'The output of layer 1, which is the input of layer 2.', '(7.5, −1, 3, 4.5)'], ['W₂', 'The weight matrix of layer 2, 2 × 4.', 'rows (1, 0, 1, 0) and (0, 1, 0, 2)'],
                           ['b₂', 'The bias vector of layer 2, 2 entries.', '(0, 1)'], ['y₂', 'The output of layer 2: W₂ y₁ + b₂.', '(10.5, 9)']],
                  widths=[1.6, 5.2, 5.1], size=22, note='Activation: a nonlinear function (graph not a straight line, e.g. max(0, x)) on each output (Session 11).',
                  notes=('A second layer follows. Its input is the output of the first layer, the four numbers seven point five, minus one, three and four point five. Its weight matrix W two has two rows and four columns: one, zero, one, zero, and zero, one, zero, two. '
                         'The first dot product gives seven point five plus three, which is ten point five. The second gives minus one plus nine, which is eight. Add the bias b two, zero and one, and the output is ten point five and nine. '
                         'An activation function is a fixed nonlinear function that a real layer applies to each output. Nonlinear means its graph is not a straight line: max of zero and x, for example, turns every negative number into zero. We meet it in Session eleven.')))

    S.append(dict(kind='idea', title='Stacking two layers is a matrix times a matrix',
                  visual=dict(kind='ma_matmul', A=W2.tolist(), B=W1.tolist(), row=0, col=2, work='1 × 2 + 0 × (−1) + 1 × 0 + 0 × 1 = 2', names=('W2 (2 × 4)', 'W1 (4 × 3)', 'W2 W1 (2 × 3)'),
                              caption='Gold row of W2 with gold column of W1 gives the gold entry'),
                  lead='With no biases, layer 2 after layer 1 is W2 (W1 x) = (W2 W1) x. Multiply the weights first.',
                  points=['W2 W1 is 2 × 3: rows (3, 1, 2) and (−2, 3, 1).', f'On x = (1, 2, 3) it gives {tuple(int(v) for v in F["nob2"])}, as two layers in turn do.', 'With no activation function (nonlinear step), two layers collapse into one.'],
                  notes=('Real models have many layers one after another. Take a second layer W2 that turns four numbers into two. Skip the biases for a moment. Feeding x into layer one and the result into layer two is the same as multiplying W2 by W1 first, and then by x. '
                         f'W2 is two by four and W1 is four by three, so the product is two by three. Applied to x, it gives {F["nob2"].tolist()[0]} and {F["nob2"].tolist()[1]}, exactly the same as doing the two layers in turn. '
                         'That also shows why real networks add an activation function between the layers. Without it, a hundred layers would collapse into a single matrix.')))

    S.append(dict(kind='wide', title='A whole sentence goes through a layer at once: tokens as rows, so the layer is X Wᵀ',
                  visual=dict(kind='ma_matmul', A=XT.tolist(), B=WT.T.tolist(), row=0, col=1, work='1 × 0 + 0 × 2 + 2 × 1 = 2', names=('X (4 tokens × 3)', 'Wᵀ (3 × 2)', 'X Wᵀ (4 × 2)'),
                              caption='Gold row of X (token 1), gold column of Wᵀ (row 2 of W): the gold entry'),
                  caption='Illustrative. W is 2 outputs × 3 inputs. Tokens as rows: X Wᵀ (as in PyTorch).',
                  notes=('A token is a piece of text, often a word or part of a word, and each token has a vector, its embedding from Session 2. Stack four token vectors as the rows of a matrix X, four by three. These numbers are illustrative. '
                         'The layer W turns three inputs into two outputs, so it is two by three. For one column vector x we computed W x. With a token in each row, the shapes force a change: four by three times two by three does not work, but four by three times W transpose, three by two, does. '
                         'Each row of X W transpose is W x for one token, written as a row. The gold entry is two. Libraries such as PyTorch store W as outputs by inputs and compute exactly X W transpose.')))

    S.append(dict(kind='idea', title='Counting the numbers in the matrices gives the parameters of a small network',
                  visual=dict(kind='ma_params'),
                  lead='Parameters: the numbers a model learns. Toy network: 3 inputs, a hidden layer of 4 (between input and output), 2 outputs.',
                  points=['Layer 1: W1 is 4 × 3 = 12 weights, plus 4 biases.', 'Layer 2: W2 is 2 × 4 = 8 weights, plus 2 biases.', f'Total: 12 + 4 + 8 + 2 = {F["par"]} parameters.'],
                  notes=('Counting comes next. Take a toy network with three inputs, a hidden layer of four numbers and two outputs. The first layer has a four by three weight matrix, which is twelve numbers, and four biases. '
                         'The second layer has a two by four weight matrix, which is eight numbers, and two biases. Add them up: twelve, plus four, plus eight, plus two, is twenty-six. '
                         'Those twenty-six numbers are the parameters of this toy model. Training will set each of them. What would change if the hidden layer had five numbers instead of four?')))

    S.append(dict(kind='formula', title='Parameters of a layer: m × n weights plus m biases',
                  formulas=[('Parameters of one layer', r'$\mathrm{parameters} = m \times n + m$'), ('Our network', r'$(4 \times 3 + 4) + (2 \times 4 + 2) = 16 + 10 = 26$')],
                  symbols=[['n', 'Number of inputs of the layer, which is the number of columns of W.', 'layer 1: n = 3'], ['m', 'Number of outputs, which is the number of rows of W and the length of b.', 'layer 1: m = 4'],
                           ['m × n', 'The weights in W.', '12'], ['+ m', 'The biases in b.', '4'],
                           ['Bigger', 'A layer from 1,000 inputs to 1,000 outputs.', f'1,000 × 1,000 + 1,000 = {F["par1000"]:,}']],
                  widths=[1.6, 6.4, 3.9], size=21, note='Python: W.size + b.size. Spreadsheet: ROWS(W) * COLUMNS(W) + ROWS(b).',
                  notes=('The rule has two parts. A layer with n inputs and m outputs has a weight matrix with m rows and n columns, so m times n weights, and m biases. In total, m times n plus m. '
                         f'Layer one of the toy network has four times three plus four, which is sixteen. Layer two has two times four plus two, which is ten. Sixteen plus ten is twenty-six. '
                         f'Now scale up. One layer from a thousand inputs to a thousand outputs already has {F["par1000"]:,} parameters, more than a million, in just one layer. That is how the numbers climb so fast.')))

    S.append(dict(kind='idea', title='Billions of parameters means billions of numbers in matrices like these',
                  visual=dict(kind='ma_logbars', items=[('Our toy network', 26, '26'), ('One 1,000 × 1,000 layer', F['par1000'], f'{F["par1000"]:,}'),
                                                        ('One 4,096 × 4,096 matrix', F['par4096'], f'{F["par4096"]:,}'), ('An open model with 7 billion parameters', 7e9, '7 billion')]),
                  lead='Open models publish their size: Llama 2 has 7, 13 and 70 billion parameters (Touvron et al., 2023).',
                  points=['Logarithmic scale, as in Session 1.', f'A byte is 8 bits. A 16-bit number takes 2 bytes, so 7 billion numbers fill {F["gb7"]:.0f} gigabytes.', 'Training sets every one.'],
                  notes=('How big is big? The bars use a logarithmic scale, like the logarithms in Session one: each tick to the right is a hundred times bigger. Our toy network has twenty-six parameters. One layer from a thousand to a thousand has just over a million. '
                         f'A single weight matrix of four thousand ninety-six by four thousand ninety-six has {F["par4096"]:,} numbers, and open models use matrices of this kind of size. Open models also publish their total size. The Llama 2 models come in 7, 13 and 70 billion parameters. '
                         f'A byte is eight bits. If each number is stored in sixteen bits, which is two bytes, seven billion numbers need {F["gb7"]:.0f} gigabytes. The sizes of closed models are not published, so I will not quote them.')))

    S.append(dict(kind='compare', title='Common mistake: multiplying two matrices entry by entry instead of row by column',
                  left=dict(head='Wrong', icon='cross', points=['Multiply matching entries of A and B.', 'Python: A * B, entry by entry. For our 2 × 3 and 3 × 2 it fails.']),
                  right=dict(head='Right', icon='check', points=['Dot products of rows of A with columns of B.', 'Python: A @ B. Spreadsheet: MMULT.', 'Check the shapes first.']),
                  verdict='The star (*) multiplies entry by entry. The at sign (@) gives the matrix product.',
                  notes=('A common mistake is to multiply two matrices entry by entry. That is a different operation, called the elementwise product, and in Python it uses the star. '
                         'The matrix product combines a whole row of A with a whole column of B, and in Python it uses the at sign. Our two by three and three by two matrices make the point: the star gives an error, because the shapes differ, and the at sign gives the two by two answer. '
                         'In a spreadsheet, the sign for times between two ranges also works entry by entry. You need MMULT.')))

    S.append(dict(kind='code', title='Read the recipe before you run it: matrices in NumPy',
                  code='A = np.array([[1, 2, 3], [4, 5, 6]])\nx = np.array([1, 2, 3])\ny = A @ x\nC = A @ B\nAt = A.T\nI = np.eye(3)\nz = W @ x + b\nZ = X @ W.T + b\nn = W.size + b.size',
                  reads=['Line 1: a matrix from a list of rows. A.shape gives (2, 3).', 'Lines 3 and 4: the at sign is the matrix product. Spreadsheet: MMULT.', 'Line 5: the transpose. Spreadsheet: TRANSPOSE.',
                         'Line 6: the identity matrix of size 3 × 3.', 'Lines 7 and 8: one layer, for one column x, then for one row per input. Line 9: the parameters.'],
                  notes=('Read the recipe before the lab. Line one builds a matrix from a list of rows, and the shape tells you rows and columns. The at sign in lines three and four is the matrix product. '
                         'Line five gives the transpose, and line six gives the identity matrix. Line seven is a whole layer, W times x plus b. Line eight is the same layer for a matrix X with one input per row, so it uses W transpose. Line nine counts the parameters. '
                         'In a spreadsheet, MMULT replaces the at sign, TRANSPOSE gives the transpose, and ROWS and COLUMNS give the shape.')))

    S.append(dict(kind='divider', title='Part 2: the lab', lead='Close the slides. Open the notebook or the workbook.', section='Lab',
                  notes=('That is the end of the ideas. Open the notebook in Colab or the workbook in Excel or Google Sheets. The numbers are the same in both. '
                         'Run the cells in order from the top, and in every step predict first. In the spreadsheet, matrix answers are array formulas: in Excel select the gold range, type the formula and press Control Shift Enter. In Google Sheets type it in the first cell and press Control Shift Enter, which wraps it in ARRAYFORMULA. I will walk around.')))

    S.append(dict(kind='steps', title='Seven lab steps take you from a table to a count of parameters',
                  steps=[dict(head='1 Table', text='Shape, entry, transpose', icon='grid'), dict(head='2 A x', text='Then I x', icon='calculator'), dict(head='3 A B', text='A B and B A', icon='switch'),
                         dict(head='4 Move', text='Shear and rotate a shape', icon='pin'), dict(head='5 Layer', text='y = W x + b', icon='gear'), dict(head='6 Two layers', text='W2 W1, X Wᵀ', icon='folder'),
                         dict(head='7 Count', text='The parameters', icon='bars')], highlight=4,
                  caption='Predict, run, read, change one thing. Workbook: Steps 1 to 4 on Products, 5 to 7 on Layers.',
                  notes=('The lab has seven steps, the same in the notebook and the workbook. Step one is the learner table, its shape, one entry and the transpose. Step two multiplies A by x and checks that the identity changes nothing. Step three multiplies A by B, and B by A. '
                         'Step four moves the L-shaped drawing with a shear and a rotation. Step five computes the layer y equals W x plus b. Step six adds a second layer, and runs a batch of inputs as rows. Step seven counts parameters. '
                         'In every step predict first, run, read, then change one thing.')))

    S.append(dict(kind='table', title='Check your numbers before you move on', headers=['What you compute', 'You should get'],
                  rows=[['Learner table: shape, and entry in row 2, column 3', '3 × 3 and 58'], ['Shape of the transpose of A (2 × 3)', '3 × 2'], ['A x for x = (1, 2, 3)', f'{tuple(int(v) for v in F["Ax"])}'],
                        ['A B, rows 1 and 2; shape of B A', f'({F["AB"][0][0]}, {F["AB"][0][1]}), ({F["AB"][1][0]}, {F["AB"][1][1]}); 3 × 3'], ['Shear moves the corner (1, 3) to', f'{tuple(int(v) for v in F["shear_pt"])}'],
                        ['Layer 1: y1 = W1 x + b1', '(' + ', '.join(fmt(v) for v in F['Y1']).replace('-', '−') + ')'], ['Layer 2: W2 y1 + b2', '(' + ', '.join(fmt(v) for v in F['OUT']) + ')'], ['Parameters: toy network; 1,000 × 1,000 layer', f'{F["par"]}; {F["par1000"]:,}']],
                  widths=[7.4, 4.6], icons=['grid', 'switch', 'calculator', 'gear', 'pin', 'magnifier', 'check', 'key'], note='If your number differs, find the step that went wrong. Do not change a number to match.',
                  notes=('Use this table as your checkpoint. If your numbers match, carry on. If one does not, call me, because the later steps use the earlier ones. '
                         'The usual causes are a cell run out of order, using the star instead of the at sign, or forgetting to add the bias. Do not change a number to make it match. Find out why it is different.')))

    S.append(dict(kind='table', title='Four messages you may meet, what they mean and what to do', headers=['What you see', 'What it means', 'What to do'],
                  rows=[['ValueError: matmul mismatch in the core dimension', 'The inner numbers of the shapes differ.', 'Print A.shape and B.shape. They must match inside.'],
                        ['A * B gives an error or the wrong table', 'The star multiplies entry by entry.', 'Use A @ B for the matrix product.'],
                        ['#VALUE! or only one cell filled in a spreadsheet', 'The formula was not an array over the whole answer range.', 'Excel: select the gold range, type, press Ctrl Shift Enter. Google Sheets: the same keys in the first cell.'],
                        ['IndexError for entry 2, 3', 'Python counts from 0, so row 2 and column 3 is entry 1, 2.', 'Subtract 1 from the row and the column number.']],
                  widths=[3.8, 4.2, 4.0], icons=['cross', 'chart', 'key', 'magnifier'],
                  notes=('Four messages you may meet. A mismatch in the core dimension means the inner numbers of the shapes differ, so print the shapes. The star gives the wrong table, because it multiplies entry by entry. '
                         'In a spreadsheet, a matrix product fills a whole range, and Control Shift Enter makes sure it does in both Excel and Google Sheets. And an index error comes from Python counting from zero. Read the message first. It usually tells you the answer.')))

    S.append(dict(kind='wide', title='Where this appears in AI: most of the arithmetic in each layer is matrix multiplication',
                  visual=dict(kind='flow', steps=[dict(head='Text', text='Cut into tokens', icon='doc'), dict(head='Embeddings', text='Stacked as X', icon='grid'),
                                                  dict(head='Layers', text='X Wᵀ, again and again', icon='gear'), dict(head='Scores', text='One per token', icon='chart'),
                                                  dict(head='Next word', text='One is chosen', icon='speech')], highlight=2),
                  caption='Published transformer design (Vaswani et al., 2017): most arithmetic is matrix products.',
                  notes=('Language models of this kind are transformers, a design published in 2017. Text is cut into tokens, each token becomes a vector, and the vectors for a whole text are stacked into a matrix. '
                         'The published design then multiplies that matrix by weight matrices, layer after layer. Softmax, normalisation and other steps also appear, but most of the arithmetic is matrix products, and attention is built from them. At the end, the model produces a score for each possible next token. '
                         'I cannot tell you how a specific product is built inside, because that is not published. But the mathematics you did today is the core of the published design, and the gold step is the one in your lab.')))

    S.append(dict(kind='idea', title='Where this appears in AI: why graphics processors (GPUs) run models',
                  visual=dict(kind='card', title='Why matrix products suit a GPU', fields=[dict(label='Each entry is independent', value='One dot product per entry of the answer'), dict(label='Work can be shared', value='A GPU has thousands of small units working at once'),
                                                                                     dict(label='Two 4,096 × 4,096 matrices', value=f'{F["mult4096"]:,} multiplications (about 69 billion)'), dict(label='Published training reports', value='Describe clusters of GPUs or similar accelerators')]),
                  lead='A GPU (graphics processing unit) was first made to draw images, which needs many simple products.',
                  points=['m × n × p multiplications grow fast with size.', 'Many dot products at once suit a GPU.', 'Training and running large models need fast matrix products.'],
                  notes=('Why are graphics processors, or GPUs, used for AI? Remember the count from earlier: a matrix product needs m times n times p multiplications. '
                         f'Two matrices of size four thousand ninety-six need {F["mult4096"]:,} of them, about sixty-nine billion. But every entry of the answer is an independent dot product. So the work can be shared out. A GPU has thousands of small arithmetic units that work at the same time. '
                         'It was first built to draw images, which also needs vast numbers of simple products. That match is why training and running large models depend on GPUs. Hardware details of specific products are not something I will claim.')))

    S.append(dict(kind='practice', title='Where this appears in AI: check an assistant with your numbers', minutes=8, label='Hands-on activity',
                  task='Ask an AI assistant to multiply our two matrices.',
                  steps=['Give it A with rows (1, 2, 3), (4, 5, 6) and B with rows (7, 8), (9, 10), (11, 12). Ask for A B.', 'Compare: rows (58, 64) and (139, 154).',
                         'Ask for the parameters of a 1,000 by 1,000 layer: expect 1,001,000.'],
                  output='A note: the assistant answers, your lab numbers, and whether they agree.',
                  notes=('A short activity. Open any AI assistant and give it our two matrices, A and B, and ask it for the product A times B. Compare with your lab: fifty-eight, sixty-four, one thirty-nine, one fifty-four. '
                         'Then ask how many parameters a layer has with a thousand inputs and a thousand outputs, with biases. The answer should be one million one thousand. Did it get both right? '
                         'Did it show its steps? Never paste confidential data into an assistant. These numbers are public maths, so they are safe. Note what you found for the exit check.')))

    S.append(dict(kind='table', title='Exit check: three questions, then compare with the short answers', headers=['Question', 'Short answer'],
                  rows=[['Can a 3 × 4 matrix multiply a 4 × 2 matrix? If yes, what is the shape of the answer?', 'Yes. The inner numbers are 4 and 4. The answer is 3 × 2.'],
                        ['What is (1, 2; 3, 4) times the vector (1, 1)? Write the matrix as rows (1, 2) and (3, 4).', 'Row 1: 1 + 2 = 3. Row 2: 3 + 4 = 7. The answer is (3, 7).'],
                        ['How many parameters does a layer have with 10 inputs and 5 outputs, with biases?', '5 × 10 + 5 = 55.']],
                  widths=[6.2, 5.8], icons=['switch', 'calculator', 'key'],
                  notes=('Last, the exit check. Write your answers in your notes first. One, can a three by four matrix multiply a four by two matrix, and what is the shape of the answer? Two, take the matrix with rows one two and three four, and multiply it by the vector one one. '
                         'Three, how many parameters does a layer have with ten inputs and five outputs, with biases? The short answers are on the slide. If you got all three, you are ready for solving linear systems next session. If one surprised you, look at that part of the lab again tonight.')))

    s['facilitator'] = dict(
        prep=['Open the deck, the Python notebook in Colab and the workbook before anyone arrives. Run the notebook once from the top.',
              'Write the "check your numbers" table on the board before the lab.', 'Draw the L-shaped drawing on squared paper and have a few learners move one corner by hand with the shear matrix.',
              'In the workbook, matrix answers are array formulas. Practise selecting the gold range, typing the formula and pressing Ctrl Shift Enter (Excel) so you can show it quickly. Google Sheets accepts the same formulas.',
              'Do not quote the size of any closed model. Use only the open models named on the slide.'],
        misconceptions=[('With tokens as rows a layer is X W with the same W', 'It is X Wᵀ: W is stored outputs × inputs (as in PyTorch), so a batch with one input per row needs the transpose. Each row of X Wᵀ is W x for that row.'),
                        ('A matrix product multiplies matching entries', 'That is the elementwise product (A * B). The matrix product takes dot products of rows with columns (A @ B).'),
                        ('A B equals B A', 'Not in general. The shapes can differ, and even for square matrices the numbers differ. The lab shows B A is 3 × 3 while A B is 2 × 2.'),
                        ('Any two matrices can be multiplied', 'The number of columns of the first must equal the number of rows of the second.'),
                        ('Parameters are the data the model sees', 'Parameters are the numbers the model learns: weights and biases. Data goes through them.'),
                        ('More parameters always means a better model', 'Not necessarily. It means more capacity and more cost. Quality depends on data, training and design.')],
        probes=[('What is the shape of the product of a 5 × 2 matrix and a 2 × 7 matrix?', '5 × 7. The inner numbers 2 and 2 match and disappear.'), ('Why can we not multiply a 2 × 3 matrix by a 2 × 3 matrix?', 'A row of A has 3 entries and a column of B has 2, so no dot product exists.'),
                ('What does the identity matrix do to a vector?', 'Nothing: I x = x.'), ('How many multiplications does a 2 × 3 by 3 × 2 product need?', '2 × 3 × 2 = 12.'),
                ('What does a shear matrix do to the point (1, 3)?', 'It moves it to (4, 3): the x value is increased by the y value.'), ('Where in a layer y = W x + b do the parameters live?', 'In W (m × n numbers) and in b (m numbers).'),
                ('Why do language models need GPUs?', 'Their layers are huge matrix products, whose entries are independent dot products that can be computed at the same time.'), ('Why would two layers with no nonlinear step collapse into one?', 'Because W2 (W1 x) = (W2 W1) x, which is a single matrix times x.')],
        lab_steps=[('Step 1: table, shape, entry, transpose', 'Shape 3 × 3, entry 58 at L[1, 2]. Python learners often write L[2, 3] and get an IndexError. Spreadsheet: INDEX(range, 2, 3). Transpose of A is 3 × 2.'),
                   ('Step 2: A x and the identity', 'A x = (14, 32). I x gives (1, 2, 3) back (np.eye(3) @ x, or the given MMULT on the Products sheet).'),
                   ('Step 3: A B and B A', 'A B = [[58, 64], [139, 154]]. B A is 3 × 3. Python: @ not *. Spreadsheet: array formula over the whole range.'),
                   ('Step 4: move a shape', 'Shear sends (1, 3) to (4, 3). Rotation by 90 degrees sends it to (-3, 1). The picture is in the notebook. In the workbook read the moved points in the table.'),
                   ('Step 5: one layer', 'y1 = (7.5, -1, 3, 4.5). In the workbook W1 x comes first (an MMULT range), then each entry of y1 adds its bias in its own cell.'),
                   ('Step 6: two layers, and a batch as rows', 'Layer 2 gives (10.5, 9). Without biases W2 W1 is [[3, 1, 2], [-2, 3, 1]] and gives (11, 7) on x. The batch X W1ᵀ + b1 has one input per row: row 1 is y1 again, row 2 is (2.5, 0, 0, 2.5).'),
                   ('Step 7: count parameters', '26 for the toy network, 1,001,000 for the 1,000 × 1,000 layer, 14 gigabytes for 7 billion numbers at 2 bytes each.')],
        rescue=['If the concepts run over, skip the identity slide and show it in the lab only. Keep the layer slides.', 'If only thirty minutes of lab remain, do steps 1, 2, 3 and 5. Steps 4, 6 and 7 can be shown on the projector.',
                'If a learner has no laptop, pair them with a neighbour.', 'If a workbook array formula fills only one cell in Google Sheets, press Ctrl+Shift+Enter in the first cell so Sheets wraps it in ARRAYFORMULA, or use the notebook.'],
        after=['Share the lab files again.', 'Ask learners to add the shape rule, the matrix product and the parameter count to the one-page sheet.', 'Note any question you could not answer and open Session 4 with it.'],
        lab_answer_key=[['Step 1 PREDICT: which entry is L[1, 2]?', 'Row 2, column 3: 58.'], ['Step 2 READ: what does I x give?', 'x itself, (1, 2, 3): each row of I picks one entry.'],
                        ['Step 3 PREDICT: what is the shape of A B? And of B A?', '2 × 2 and 3 × 3.'],
                        ['Step 3 CHANGE: run A @ A and read the error.', 'The inner numbers are 3 and 2, so the product does not exist.'],
                        ['Step 4 PREDICT: where does the rotation send the corner (1, 3)?', 'To (-3, 1).'], ['Step 5 CHANGE: first bias 0.5 to 2.5. What moves?', 'Only the first entry of y, by 2: 7.5 becomes 9.5.'],
                        ['Step 6 READ: why does W2 W1 have shape 2 × 3?', 'W2 is 2 × 4 and W1 is 4 × 3. The 4s match and disappear.'],
                        ['Step 6 READ: why X @ W1.T and not X @ W1?', 'X is 2 × 3 (one input per row) and W1 is 4 × 3. The inner numbers must agree, so W1 is transposed to 3 × 4. Row 1 of the answer is W1 x + b1 for the first input.'],
                        ['Step 7 CHANGE: set the hidden layer to 5. How many parameters?', '(5 × 3 + 5) + (2 × 5 + 2) = 20 + 12 = 32.']])
    return s
