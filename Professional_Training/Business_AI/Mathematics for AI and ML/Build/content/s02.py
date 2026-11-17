"""Session 2: Vectors. Every number on the slides is computed here with numpy and reused by the lab files."""
import numpy as np

SENTENCES = ['How do I reset my password?', 'Steps to change your login password', 'Office opening hours on Saturday', 'Refund policy for cancelled orders', 'How to request a refund', 'Our team picnic is on Friday']
E = np.array([[0.9, 0.1, 0.0, 0.1], [0.8, 0.2, 0.1, 0.0], [0.0, 0.1, 0.9, 0.2], [0.1, 0.9, 0.2, 0.0], [0.2, 0.8, 0.1, 0.1], [0.0, 0.1, 0.5, 0.8]])
Q = np.array([0.85, 0.15, 0.05, 0.05])
A = np.array([3, 4]); B = np.array([4, 3])
U = np.array([1, 2, 2]); V = np.array([2, 0, 1])
PP = np.array([1, 1]); QQ = np.array([4, 5])


def cos(a, b):
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))


def facts():
    sims = E @ Q / (np.linalg.norm(E, axis=1) * np.linalg.norm(Q))
    return dict(add=A + B, scale=2 * A, dot=int(U @ V), norm_a=float(np.linalg.norm(A)), norm_u=float(np.linalg.norm(U)), dist=float(np.linalg.norm(QQ - PP)), cos_ab=cos(A, B),
                angle_ab=float(np.degrees(np.arccos(cos(A, B)))), dots=E @ Q, sims=sims, best=int(np.argmax(sims)), order=list(np.argsort(-sims)),
                dist_u3u=float(np.linalg.norm(np.array([1, 2]) - np.array([3, 6]))), norm_q=float(np.linalg.norm(Q)), norms=np.linalg.norm(E, axis=1), cos_uv=cos(U, V), angle_uv=float(np.degrees(np.arccos(cos(U, V)))))


def build():
    F = facts()
    sims = F['sims']
    order = F['order']
    s = dict(
        num=2, block='Linear algebra', short_title='Vectors',
        title='Vectors: how AI measures that two pieces of data are alike',
        question='When an assistant searches your documents, how does it find the passage that fits your question?',
        outcomes=['Write a row of data as a vector, and add, scale and compare vectors by hand',
                  'Calculate the dot product (inner product), the L2 norm, the Euclidean distance and the cosine similarity',
                  'Rank six short sentences against a query with cosine similarity, in Python and in a spreadsheet'],
        outcome_icons=['grid', 'calculator', 'magnifier'],
        outcome_note=('By the end of today you can write a row of data as a vector, and add, scale and compare vectors by hand. You can calculate the dot product, which is also called the inner product, the L2 norm, the Euclidean distance and the cosine similarity. '
                      'And you can rank six short sentences against a query using cosine similarity, in Python and in a spreadsheet. That last step is a small version of how an AI assistant finds the right passage in your documents.'),
        clock=[(10, 'Recall, then a real question from AI'), (35, 'Concept: a picture, then one example by hand'), (10, 'Break'), (45, 'Lab: predict, run, then change one thing'),
               (15, 'Where it appears in AI, and an exit check'), (5, 'Save the work')],
        plan_title='Your two hours: vectors, then the lab, then AI search',
        plan_note=('The first ten minutes recall last session and pose the question of the day. Then thirty-five minutes of ideas, each with a picture and a small calculation by hand, a break, and a forty-five minute lab in Python or in a spreadsheet. '
                   'The last fifteen minutes show where today appears in AI document search, and give you an exit check. Then you save your work.'),
        recall_from='Session 1',
        recall=[('What does the symbol Σ (sigma) mean?', 'Add up everything that follows it, from the start index to the stop index.'),
                ('What does the logarithm of a product equal?', 'The sum of the logarithms: ln(u × v) = ln u + ln v.'),
                ('Why do AI programs add log-probabilities?', 'A product of many small probabilities underflows to 0. A sum of logs stays an ordinary number.')],
        words=[('Vector', 'A list of d numbers in a fixed order. A row of data is a vector. d is its dimension.'),
               ('Dot product (inner product)', 'Multiply matching entries of two vectors, then add. The result is one number.'),
               ('L2 norm (Euclidean norm)', 'The length of a vector: the square root of the sum of its squared entries.'),
               ('Cosine similarity', 'The cosine of the angle between two vectors: 1 for the same direction, 0 at a right angle.'),
               ('Embedding', 'A vector that represents a piece of text so that similar meanings get similar vectors.')],
        word_icons=['grid', 'calculator', 'bars', 'magnifier', 'doc'],
        words_note=('Five words for today. A vector is a list of numbers in a fixed order, and a row of data is a vector. The dot product, also called the inner product, multiplies matching entries and adds. '
                    'The L2 norm, also called the Euclidean norm, is the length of a vector. Cosine similarity is the cosine of the angle between two vectors. And an embedding is a vector that represents a piece of text. We use all five before the end.'),
        keep='Keep your saved notebook or workbook, with every check on OK. Keep the one idea of the day: cosine similarity compares the direction of two vectors, and that is how AI finds a passage that means the same.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Your lab file', value='Saved, all checks OK'), dict(label='The idea', value='cosine = a·b / (‖a‖ ‖b‖)'),
                                                                 dict(label='Formula sheet', value='dot, norm, distance, cosine'), dict(label='Next session', value='Matrices')]),
        keep_title='Save your lab file and add four formulas to your sheet',
        next='Session 3: Matrices. A table of numbers that can also move and reshape vectors.', next_label='Next session',
        keep_note=('Before you go, save your notebook or workbook with every check on OK. Add four formulas to your one-page sheet: the dot product, the L2 norm, the Euclidean distance and the cosine similarity, each with its industry name. '
                   'Next session we stack vectors into a matrix, and we see that a matrix can also move and reshape vectors. Write down any question that you still have and bring it.'),
        cover_note=('Welcome back. Last session we met sums, functions and logarithms. Today we meet vectors, the list of numbers that sits behind every row of data. '
                    'By the end you will be able to measure how alike two things are with a single number. That is exactly what an AI assistant does when it searches your documents for the passage that answers your question.'),
        slides=[])
    S = s['slides']

    S.append(dict(kind='table', title='Answers to the three questions from Session 1', headers=['Question', 'Short answer'], rows=[[q, a] for q, a in s['recall']], widths=[5.0, 7.0], icons=False,
                  note='If one answer surprised you, look again at the Session 1 slides before the lab.',
                  notes=('The short answers first. Sigma means add up everything that follows it, from the start index to the stop index. The logarithm of a product equals the sum of the logarithms. '
                         'And AI programs add log-probabilities because a product of many small probabilities becomes too small for the computer and rounds to zero, while a sum of logs stays an ordinary number. If you got all three, you are ready for vectors.')))

    S.append(dict(kind='wide', title='A row of data is a vector: a list of numbers in a fixed order',
                  visual=dict(kind='ma_rowvec', headers=['Learner', 'Age', 'Hours', 'Score'], rows=[['Amina', 21, 6, 72], ['Brian', 25, 3, 58], ['Chloe', 19, 8, 85]], row=0, vec_label='x'),
                  caption='Years, hours a week, score of 100: x = (21, 6, 72), d = 3. Written across to save space.',
                  notes=('A table of data has rows, and every row is a vector. Here are three learners, with age, hours studied per week and a quiz score. These numbers are made up. '
                         'The gold row is Amina, and written as a vector called x it is the list twenty-one, six, seventy-two. The number of entries is called the dimension, written d, and here d is three. '
                         'A table with n rows is n vectors. The order matters, so age always comes first. Today I write vectors across the page to save space. In Session 3 they stand up as columns, which is how matrix work writes them.')))

    S.append(dict(kind='idea', title='A vector with two numbers is an arrow from the origin to a point',
                  visual=dict(kind='ma_vec2d', arrows=[dict(v=(3, 4), label='a = (3, 4)', dx=0.1, dy=0.2), dict(v=(4, 3), label='b = (4, 3)', color='red', dx=0.12, dy=-0.05)], xlim=(0, 6), ylim=(0, 6)),
                  lead='The origin is the point (0, 0). The vector a = (3, 4) is the arrow from the origin to the point 3 across and 4 up.',
                  points=['b = (4, 3) is a second vector: 4 across and 3 up.', 'With 4 or more numbers we cannot draw the arrow, but the rules stay the same.'],
                  notes=('With two numbers we can draw a vector. It is an arrow that starts at the origin, the point zero zero, and ends at the point given by the numbers. For a equals three, four, go three across and four up. '
                         'The red arrow is b, which is four across and three up. They point in different directions, and we will measure exactly how different in a few slides. '
                         'With four or more numbers we cannot draw the arrow on paper, but every rule you see today works unchanged in higher dimensions. That matters, because real data often has hundreds of columns.')))

    S.append(dict(kind='idea', title='Adding vectors places one arrow at the tip of the other',
                  visual=dict(kind='ma_vec2d', arrows=[dict(v=(3, 4), label='a', dx=-0.3, dy=0.15), dict(v=(4, 3), o=(3, 4), label='b', color='grey', dash=True, dx=0.1, dy=0.15),
                                                       dict(v=(7, 7), label='a + b = (7, 7)', color='red', dx=-0.2, dy=0.25, ha='right')], xlim=(0, 8), ylim=(0, 8)),
                  lead='Vector addition: add the matching entries. (3, 4) + (4, 3) = (7, 7).',
                  points=['Draw b starting at the tip of a. The red arrow from the origin to the end is a + b.', 'Both vectors must have the same number of entries.'],
                  notes=('To add two vectors, add the matching entries. Three plus four is seven, and four plus three is seven, so a plus b is seven, seven. '
                         'In the picture, draw b starting at the tip of a. The red arrow from the origin to the new tip is the sum. This works only when both vectors have the same number of entries. '
                         'Try one, two, three plus ten, ten, ten: the answer is eleven, twelve, thirteen.')))

    S.append(dict(kind='idea', title='Scaling a vector by a number stretches or shrinks the arrow',
                  visual=dict(kind='ma_vec2d', arrows=[dict(v=(6, 8), label='2a = (6, 8)', color='red', dx=0.15, dy=0.0), dict(v=(3, 4), label='a = (3, 4)', dx=0.15, dy=-0.1), dict(v=(1.5, 2), label='0.5a', color='grey', dx=0.15, dy=0.0)],
                              xlim=(0, 8), ylim=(0, 9)),
                  lead='Scaling: multiply every entry by one number c, called a scalar. 2 × (3, 4) = (6, 8).',
                  points=['A scalar above 1 stretches the arrow. A scalar between 0 and 1 shrinks it.', 'A positive scalar keeps the direction. A negative scalar reverses it.'],
                  notes=('To scale a vector, multiply every entry by one number, called a scalar. Twice three four is six eight. In the picture the red arrow is twice as long as a and points the same way. The grey arrow is half of a. '
                         'A scalar above one stretches the arrow, and a scalar between zero and one shrinks it. A negative scalar flips the arrow around, and a positive scalar keeps the direction. Cosine similarity, later today, depends on that fact. '
                         'What is three times the vector one, two?')))

    S.append(dict(kind='formula', title='Vectors add entry by entry, and a scalar multiplies every entry',
                  formulas=[('Addition', r'$\mathbf{a}+\mathbf{b}=(a_1+b_1,\; a_2+b_2)$'), ('Scaling', r'$c\,\mathbf{a}=(c\,a_1,\; c\,a_2)$'), ('Our numbers', r'$(3,4)+(4,3)=(7,7),\qquad 2\,(3,4)=(6,8)$')],
                  symbols=[['a and b', 'Two vectors with the same number of entries. Bold letters mean vectors.', 'a = (3, 4), b = (4, 3)'], ['a₁, a₂', 'Entry 1 and entry 2 of a. The subscript is the position.', 'a₁ = 3, a₂ = 4'],
                           ['c', 'A single number, called a scalar.', 'c = 2']],
                  size=22, note='Written across to save space; Session 3 stands vectors up as columns. Python: a + b, 2 * a.',
                  notes=('The two operations as formulas. Bold letters are vectors, and the small numbers are positions. To add, add position by position. To scale, multiply every position by the scalar c. '
                         'With our numbers, three four plus four three is seven seven, and two times three four is six eight. In Python you write a plus b and two times a, and numpy does it entry by entry. '
                         'A vector with two entries cannot be added to one with three, because the third entry has no partner.')))

    S.append(dict(kind='idea', title='The dot product multiplies matching entries and adds the results',
                  visual=dict(kind='ma_dot', u=[1, 2, 2], v=[2, 0, 1]),
                  lead='Dot product (also called inner product): multiply matching entries, then add.',
                  points=['u = (1, 2, 2) and v = (2, 0, 1).', 'The products are 2, 0 and 2, and they add up to 4.', 'The result is a single number.'],
                  notes=('The dot product, also called the inner product, is the most important operation in this course. Take two vectors of the same length. Multiply the entries that sit in the same position, then add the products. '
                         'For u equals one, two, two and v equals two, zero, one, the products are two, zero and two, and the total is four. Two vectors go in and one single number comes out. '
                         'You already know the pattern from Session one, because it is a sigma sum of products. What is the dot product of u with itself?')))

    S.append(dict(kind='formula', title='Written with sigma, the dot product is a sum of d products',
                  formulas=[('Dot product', r'$\mathbf{u}\cdot\mathbf{v}=\sum_{i=1}^{d} u_i\,v_i$'), ('Our numbers', r'$1\times 2+2\times 0+2\times 1=4$')],
                  symbols=[['Σ and d', 'Add up over the d entries. d is the number of entries.', 'd = 3'], ['uᵢ, vᵢ', 'Entry i of u and of v.', 'u = (1, 2, 2), v = (2, 0, 1)'],
                           ['u · v', 'The dot product: one number. The raised dot is kept for this; × multiplies two numbers.', '4']],
                  size=22, note='Python: u @ v or np.dot(u, v). Spreadsheet: =SUMPRODUCT(u, v). The cosine slides later link this number to the angle.',
                  notes=('The dot product as a formula is a sigma sum. For each position i from one to d, multiply entry i of u by entry i of v, then add. '
                         'With our numbers that is one times two, plus two times zero, plus two times one, which is four. I write the times sign between plain numbers and keep the raised dot for the dot product of two vectors. '
                         'In Python you write u at v, and in a spreadsheet SUMPRODUCT. Later today the same number turns up again inside cosine similarity.')))

    S.append(dict(kind='idea', title='The L2 norm is the length of the arrow, from the Pythagoras rule',
                  visual=dict(kind='ma_vec2d', arrows=[dict(v=(3, 4), label='length 5', dx=-0.15, dy=0.2, ha='right')], segments=[dict(a=(0, 0), b=(3, 0), label='3', dy=0.25, color='grey'), dict(a=(3, 0), b=(3, 4), label='4', dx=0.3, color='grey')],
                              xlim=(0, 6), ylim=(0, 6)),
                  lead='L2 norm (Euclidean norm): the length of a vector. It is written ‖a‖.',
                  points=['For a = (3, 4): 3² + 4² = 9 + 16 = 25.', 'The square root of 25 is 5, so ‖a‖ = 5.', 'A longer arrow has a bigger norm.'],
                  notes=('The L2 norm, also called the Euclidean norm, is the length of the arrow. In two dimensions it is the Pythagoras rule you know from school. The arrow for three, four makes a right-angled triangle with sides three and four. '
                         'Three squared is nine, four squared is sixteen, the total is twenty-five and the square root is five. The same recipe works for any number of entries: square each entry, add, take the square root. '
                         'For one, two, two that gives the square root of nine, which is three.')))

    S.append(dict(kind='formula', title='The L2 norm is the square root of a vector dotted with itself',
                  formulas=[('L2 norm (length)', r'$\Vert\mathbf{a}\Vert_2=\sqrt{\sum_{i=1}^{d} a_i^{2}}=\sqrt{\mathbf{a}\cdot\mathbf{a}}$'), ('Our numbers', r'$\sqrt{3^2+4^2}=5,\qquad \sqrt{1^2+2^2+2^2}=3$')],
                  symbols=[['‖a‖₂', 'The L2 norm. The subscript 2 means squares and a square root.', '5 for (3, 4)'], ['Σ and d', 'Add up over the d entries of a.', 'd = 2'], ['aᵢ', 'Entry i of the vector a.', '3 and 4'], ['a · a', 'The dot product of a with itself: the squared length.', '25']],
                  size=22, note='Python: np.linalg.norm(a). Spreadsheet: =SQRT(SUMPRODUCT(a, a)).',
                  notes=('As a formula, the norm says: square every entry, add them, take the square root. The subscript two says we use squares, and that is why it is called the L2 norm. '
                         'The sum of squares is the dot product of a with itself, so the norm is the square root of a dot a. For three, four we get five, and for one, two, two we get three. '
                         'In Python, np dot linalg dot norm does it. In a spreadsheet use SQRT of SUMPRODUCT of the range with itself, which is the formula written in cells.')))

    S.append(dict(kind='idea', title='Euclidean distance is the length of the arrow between two points',
                  visual=dict(kind='ma_vec2d', dots=[dict(p=(1, 1), label='P = (1, 1)', dx=-0.1, dy=-0.4), dict(p=(4, 5), label='R = (4, 5)', dx=0.15, dy=0.1)], segments=[dict(a=(1, 1), b=(4, 5), label='distance 5', color='red', dx=-0.2, dy=0.2, ha='right'),
                              dict(a=(1, 1), b=(4, 1), label='3', dy=0.25, color='grey'), dict(a=(4, 1), b=(4, 5), label='4', dx=0.3, color='grey')], xlim=(0, 6), ylim=(0, 6)),
                  lead='Euclidean distance between the points P and R: the L2 norm of their difference, R − P.',
                  points=['R − P = (3, 4), so the distance is 5.', 'A small distance means the two rows are close, so they are alike.'],
                  notes=('To measure how far apart two points are, subtract them and take the norm of the difference. Take the point P equals one, one and the point R equals four, five. The difference is three, four, and we already know its length is five. '
                         'This is the Euclidean distance. If each row of a table is a point, the distance tells you how alike two rows are. A small distance means similar, which is how you might find customers who look like a given customer.')))

    S.append(dict(kind='formula', title='Distance subtracts entry by entry, squares, adds and takes the root',
                  formulas=[('Euclidean distance', r'$\mathrm{dist}(\mathbf{P},\mathbf{R})=\Vert\mathbf{R}-\mathbf{P}\Vert_2=\sqrt{\sum_{i=1}^{d}(R_i-P_i)^2}$'), ('Our numbers', r'$\sqrt{(4-1)^2+(5-1)^2}=\sqrt{9+16}=5$')],
                  symbols=[['P and R', 'Two points, each written as a vector with d entries.', 'P = (1, 1), R = (4, 5)'], ['Pᵢ, Rᵢ', 'Entry i of P and of R.', 'R₁ − P₁ = 3, R₂ − P₂ = 4'], ['Σ and d', 'Add up over the d entries.', 'd = 2'],
                           ['dist(P, R)', 'The distance: the length of the arrow from P to R.', '5']],
                  size=22, note='Python: np.linalg.norm(R - P). Spreadsheet: =SQRT(SUMXMY2(P, R)). The letter q is kept for the query vector.',
                  notes=('The distance formula has four moves. Subtract the two points entry by entry, square every difference, add them up and take the square root. That is the L2 norm of the difference. '
                         'With P equal to one, one and R equal to four, five, the differences are three and four, the squares are nine and sixteen, and the root of twenty-five is five. '
                         'I call the points P and R, because the letter q is kept for the query vector that we meet in the search. In Python you write the norm of R minus P. Swapping P and R changes every sign, but the squares remove the signs, so the distance is the same.')))

    S.append(dict(kind='idea', title='The cosine of an angle tells how far an arrow of length 1 reaches along the horizontal',
                  visual=dict(kind='ma_trig', deg=60),
                  lead='Trigonometry refresher. θ (theta) is an angle. An arrow of length 1 at angle θ reaches cos θ sideways.',
                  points=['cos θ: 1 at 0°, 0 at 90°, −1 at 180°.', 'arccos goes back to the angle: ACOS, np.arccos.', 'Computers give radians: 180° = π ≈ 3.142. DEGREES() or np.degrees() converts.'],
                  notes=('Cosine similarity needs one idea from trigonometry, so here it is from the start. Take an angle theta between two arrows. Draw an arrow of length one at that angle. How far it reaches along the horizontal is the cosine of theta. '
                         'At sixty degrees it reaches halfway, so cos sixty degrees is zero point five. Straight along, it reaches one. Straight up, zero. Pointing backwards, minus one. '
                         'Going back from a cosine to its angle is called arccos, ACOS in a spreadsheet. One trap: computers measure angles in radians, where one hundred and eighty degrees is pi, about three point one four, so you convert with DEGREES.')))

    S.append(dict(kind='idea', title='Cosine similarity compares directions and ignores the lengths of the vectors',
                  visual=dict(kind='ma_vec2d', arrows=[dict(v=(3, 0), label='cosine 1', dx=0.1, dy=0.28, ha='left'), dict(v=(2.12, 2.12), label='cosine 0.71', color='red', dx=0.1, dy=0.1), dict(v=(0, 3), label='cosine 0', dx=0.1, dy=0.1),
                                                       dict(v=(-3, 0), label='cosine −1', color='grey', dx=0.0, dy=0.55, ha='center')],
                              arcs=[dict(a=(1, 0), b=(1, 1), r=0.75, label='45°', color='red', lr=0.3, at=20, size=15), dict(a=(1, 0), b=(0, 1), r=1.35, label='90°', color='ink', lr=-0.32, at=68, size=15),
                                    dict(a=(1, 0), b=(-1, 0), r=1.95, label='180°', color='grey', lr=0.35, at=135, size=15)], xlim=(-4, 5), ylim=(0, 4), grid=False),
                  lead='Cosine similarity: the cosine of the angle θ between two vectors.',
                  points=['Angles are measured from the horizontal arrow (cosine 1).', 'Same direction: 1. At right angles: 0. Opposite directions: −1.', 'The lengths do not matter.'],
                  notes=('Cosine similarity is the cosine of the angle between two vectors, the idea from the last slide. For the same direction the angle is zero and the cosine is one. At a right angle the cosine is zero. For opposite directions it is minus one. '
                         'Because it only looks at the angle, the lengths of the vectors do not change the result. A vector that is long for any reason, a scaling quirk or a very common text, cannot win on length alone. '
                         'Which is more alike, an angle of ten degrees or an angle of eighty?')))

    S.append(dict(kind='formula', title='Divide the dot product by both lengths and the cosine is left',
                  formulas=[('Cosine similarity', r'$\cos\theta=\frac{\mathbf{a}\cdot\mathbf{b}}{\Vert\mathbf{a}\Vert\,\Vert\mathbf{b}\Vert}\quad\text{so}\quad \mathbf{a}\cdot\mathbf{b}=\Vert\mathbf{a}\Vert\,\Vert\mathbf{b}\Vert\cos\theta$'),
                            ('a, b and u, v', r'$\frac{24}{5\times 5}=0.96 \to \theta=16.26^{\circ};\quad \frac{4}{3\times 2.236}=0.596 \to \theta=53.4^{\circ}$')],
                  symbols=[['a · b', 'The dot product: 3 × 4 + 4 × 3 = 24.', '24'], ['‖a‖, ‖b‖', 'The L2 norms of the two vectors.', '5 and 5'], ['θ', 'The angle between the arrows. arccos undoes cosine.', '16.26 degrees']],
                  size=20, note='Angle: np.degrees(np.arccos(cos)) or =DEGREES(ACOS(cos)). ACOS alone gives radians.',
                  notes=('Cosine similarity is the dot product divided by the product of the two lengths. Turned around, the dot product equals length times length times the cosine, which is why it measures alignment. '
                         'For a equals three four and b equals four three, the dot product is twenty-four, and both lengths are five, so the cosine is zero point nine six and the angle is about sixteen point three degrees. '
                         'For u and v from the dot product slide, four over three times two point two three six gives zero point five nine six, an angle of fifty-three degrees. The cosine can never go above one.')))

    S.append(dict(kind='compare', title='Distance and cosine similarity answer different questions',
                  left=dict(head='Euclidean distance', points=['Compares positions.', 'a = (3, 4) and 2a = (6, 8): distance 5.', 'Small means similar.']),
                  right=dict(head='Cosine similarity', points=['Compares directions.', 'The same two vectors: cosine 1.', 'Large means similar.']),
                  verdict='A vector stretched for any reason keeps its cosine but moves away in distance.',
                  notes=('Distance and cosine answer different questions. Take a equals three, four and two a equals six, eight. The second vector is the first stretched to twice the length. '
                         'The distance between them is five, which sounds far apart. The cosine similarity is exactly one, because they point the same way. '
                         'For our six sentences the two measures happen to pick the same top four, so the choice will not change today\'s search. It matters when lengths differ for reasons unrelated to meaning, and the lab stretches one vector to show it. For two customers compared by age and spend, distance is often the better choice.')))

    S.append(dict(kind='compare', title='Common mistake: trusting the biggest dot product as the best match',
                  left=dict(head='Wrong', points=['The largest dot product is the closest match.', 'A vector 10 times longer scores 10 times higher.']),
                  right=dict(head='Right', points=['Divide by both lengths first: that is cosine similarity.', 'Lab: picnic vector × 20. Dot product 1.6 beats 0.785; cosine stays 0.097.']),
                  verdict='Normalising scales every vector to length 1 (a unit vector). Then dot product equals cosine.',
                  notes=('A common mistake is to rank by the raw dot product. The dot product grows with the lengths. If you multiply a vector by ten, all its dot products grow by ten, even though it points the same way. '
                         'So a long vector can jump to the top of the ranking for no good reason. Dividing by both lengths removes that effect, and the result is the cosine similarity. '
                         'In the lab you stretch the picnic vector by twenty, and its dot product of one point six beats zero point seven eight five. Many embedding models scale every vector to length one, called normalising, and then the dot product equals the cosine. Attention in Session 18 uses a raw dot product scaled by a fixed number, so the raw dot product has its place.')))

    S.append(dict(kind='idea', title='An embedding turns a piece of text into a vector',
                  visual=dict(kind='sheet', headers=['Sentence', 'd1', 'd2', 'd3', 'd4'], rows=[[f'S{i + 1} {t}'] + [f'{v:g}' for v in E[i]] for i, t in enumerate(SENTENCES)], size=16),
                  lead='An embedding is a vector that represents text, so that similar meanings get similar vectors.',
                  points=['Each row is one short sentence with d = 4 numbers.', 'These numbers are illustrative (made-up numbers). Real embeddings have hundreds of numbers.'],
                  notes=('An embedding is a vector that represents a piece of text, so that texts with similar meaning get similar vectors. Here are six short sentences, each with four numbers. These numbers are made up to show the arithmetic. '
                         'Look at the first two rows. Both are about passwords, and their numbers are similar. The refund sentences are similar to each other too, and different from the password ones. '
                         'In a real system a trained model produces the numbers, there are hundreds of them per text, and no single number has a name. Ranking by cosine similarity finds which sentence is closest to a question.')))

    S.append(dict(kind='idea', title='Ranking by cosine similarity finds the sentence closest to the query',
                  visual=dict(kind='ma_rank', items=[(f'S{i + 1} {SENTENCES[i]}', float(sims[i])) for i in order], best=0, vmax=1.0, fmt='{:.3f}', header='Query "I forgot my password": cosine similarity', size=16, lab_w=4.6),
                  lead='The query is also turned into a vector: (0.85, 0.15, 0.05, 0.05). Compare it with every sentence.',
                  points=['S1 and S2, the password sentences, score 0.995 and 0.994.', 'The picnic and opening hours score below 0.1.'],
                  notes=('The search itself is short. The query, I forgot my password, is turned into a vector with the same four numbers. We compute the cosine similarity between the query and every sentence, and sort. '
                         'The two password sentences come out on top, with zero point nine nine five and zero point nine nine four. The refund sentences are in the middle, and the picnic and opening hours are near zero. '
                         'The system returns the top sentence or the top few. In the lab you do exactly this, and you can check every number. The top two are close because both are about passwords.')))

    S.append(dict(kind='code', title='Read the recipe before you run it: dot product, norm and cosine',
                  code='dot = np.sum(u * v)\nnorm_a = np.sqrt(np.sum(a * a))\ncos = a @ b / (norm_a * norm_b)\nnorms = np.linalg.norm(E, axis=1)\nnorm_q = np.linalg.norm(q)\nsims = E @ q / (norms * norm_q)\nbest = np.argmax(sims)',
                  reads=['Line 1: dot product. Spreadsheet: SUMPRODUCT.', 'Line 2: L2 norm. Spreadsheet: SQRT(SUMPRODUCT(a, a)).', 'Line 3: cosine of a and b.',
                         'Lines 4 to 6: one norm per row of E (axis=1), the norm of q, all six cosines.', 'Line 7: position of the largest. Spreadsheet: =INDEX(A4:A9, MATCH(MAX(H4:H9), H4:H9, 0)).'],
                  notes=('Read the recipe before the lab. Line one is the dot product as a sum of products. Line two is the norm, the square root of a vector dotted with itself. '
                         'Line three is cosine similarity for two vectors. Line four finds one norm per row of E, because axis equals one means go along each row, and line five finds the norm of the query. Line six gives all six cosines at once. '
                         'Line seven finds the position of the biggest value. In a spreadsheet, MAX finds the biggest cosine, MATCH finds its row, and INDEX reads the sentence in that row. With a thousand sentences, no line would change.')))

    S.append(dict(kind='divider', title='Part 2: the lab', lead='Close the slides. Open the notebook or the workbook.', section='Lab',
                  notes=('That is the end of the ideas. Open the notebook in Colab or the workbook in Excel or Google Sheets. The numbers are the same in both. '
                         'Run the cells in order from the top, and in every step predict first. If a check says not yet, look at the check slide and find the step that went wrong. I will walk around.')))

    S.append(dict(kind='steps', title='The lab has seven steps, from a hand calculation to a search',
                  steps=[dict(head='1 Add, scale', text='a + b and 2a', icon='calculator'), dict(head='2 Dot, norm', text='u · v and ‖a‖', icon='gear'), dict(head='3 Distance', text='From P to R', icon='pin'),
                         dict(head='4 Cosine', text='Angle of a and b', icon='chart'), dict(head='5 Search', text='Rank six', icon='magnifier'), dict(head='6 Best', text='Pick the top one', icon='check'), dict(head='7 Stretch', text='Dot product fails', icon='clock')], highlight=4,
                  caption='Predict, run, read, change. Step 7 stretches one vector by 20 to see the dot product fail.',
                  notes=('The lab follows the slides. Steps one to four are the hand calculations from the slides: add and scale, dot product and norm, distance, and cosine with the angle. '
                         'Step five computes the cosine similarity of the query with all six sentences. Step six picks the best match. Step seven stretches one vector by twenty and shows why the dot product alone can mislead. '
                         'In every step predict first, run, read, then change one thing.')))

    S.append(dict(kind='table', title='Check your numbers before you move on', headers=['What you compute', 'You should get'],
                  rows=[['a + b for a = (3, 4), b = (4, 3)', '(7, 7)'], ['Dot product of u = (1, 2, 2) and v = (2, 0, 1)', '4'], ['L2 norm of a = (3, 4)', '5'], ['Distance from P = (1, 1) to R = (4, 5)', '5'],
                        ['Cosine similarity of a and b', f'{F["cos_ab"]:.2f}'], ['Angle between a and b, in degrees', f'{F["angle_ab"]:.2f}'], ['Cosine of the query with sentence 1', f'{sims[0]:.3f}'], ['Best match for the query', 'S1 How do I reset my password?']],
                  widths=[7.2, 4.0], icons=['calculator', 'gear', 'bars', 'pin', 'chart', 'clock', 'magnifier', 'check'], note='If your number differs, find the step that went wrong. Do not change a number to match.',
                  notes=('Use this table as your checkpoint. If your numbers match, carry on. If one does not, call me, because the later steps use the earlier ones. '
                         'The usual causes are a cell run out of order, a missing square root in the norm, forgetting to divide by both lengths, or an angle left in radians. Do not change a number to make it match. Find out why it is different.')))

    S.append(dict(kind='table', title='Four messages you may meet, what they mean and what to do', headers=['What you see', 'What it means', 'What to do'],
                  rows=[['ValueError: operands could not be broadcast together', 'You combined two vectors with different numbers of entries.', 'Print a.shape and b.shape. They must match.'],
                        ['My cosine is larger than 1', 'A division is missing, or the wrong norm was used.', 'Divide by both norms, each from its own vector.'],
                        ['#VALUE! in a spreadsheet', 'The two ranges in SUMPRODUCT have different sizes.', 'Select ranges with the same number of cells.'],
                        ['The angle shows 0.284', 'ACOS and np.arccos give radians.', 'Wrap it: DEGREES(ACOS(...)) or np.degrees(...).']],
                  widths=[3.6, 4.4, 4.0], icons=['cross', 'chart', 'key', 'magnifier'],
                  notes=('Four messages you may meet. A value error about broadcasting means two vectors have different numbers of entries, so print the shapes. A cosine above one means a division is missing. '
                         'Hash VALUE in a spreadsheet usually means two ranges of different sizes. And an angle of zero point two eight four is the right angle in radians, so convert it to degrees. Read the message first, because it usually tells you the answer.')))

    S.append(dict(kind='wide', title='Where this appears in AI: finding the right passage',
                  visual=dict(kind='flow', steps=[dict(head='Question', text='Becomes an embedding', icon='speech'), dict(head='Passages', text='Embedded earlier', icon='folder'),
                                                  dict(head='Score', text='Dot product with each', icon='magnifier'), dict(head='Top few', text='Highest scores', icon='check'),
                                                  dict(head='Answer', text='The assistant reads them', icon='doc')], highlight=2),
                  caption='RAG (Lewis et al., 2020) scores by dot product; for length-1 vectors that is the cosine.',
                  notes=('When an assistant searches your documents, the common design is this. Your question is turned into an embedding. The passages in your documents have been turned into embeddings earlier and stored. '
                         'The system scores the question against every passage, takes the highest few, and gives them to the language model, which writes the answer. '
                         'Published research calls this retrieval-augmented generation. The 2020 paper scores by a dot product, and many search tools normalise vectors to length one first, which makes it the cosine. Several vendors publish embedding services that return a vector for text you send, but how a given assistant searches inside is not published, so I only describe the standard published pattern. '
                         'Open embedding models publish their size, for example 768 numbers per text for BERT base. Our four numbers are a toy version, and the gold step is the one you just built.')))

    S.append(dict(kind='practice', title='Where this appears in AI: check an assistant with your numbers', minutes=8, label='Hands-on activity',
                  task='Ask any AI assistant: "What is the cosine similarity of (3, 4) and (4, 3)?"',
                  steps=['Use only public maths. Never paste confidential data.', 'Compare its answer with your lab number, 0.96.', 'Ask it to show the dot product and lengths. Do they match 24, 5 and 5?', 'Ask for the angle: about 16.26 degrees?'],
                  output='A note: the assistant answer, your lab number, and whether they agree.',
                  notes=('A short activity. Open any AI assistant you like and ask it for the cosine similarity of three four and four three. Compare its answer with your lab number, zero point nine six. '
                         'Then ask it to show the dot product and both lengths, and check them against twenty-four, five and five. Ask for the angle too. Did it get everything right? '
                         'Never paste confidential data into an assistant. These numbers are public maths, so they are safe. Write down what you found, and keep it for the exit check.')))

    S.append(dict(kind='table', title='Exit check: three questions, then compare with the short answers', headers=['Question', 'Short answer'],
                  rows=[['What is the dot product of (2, 3) and (4, 1)?', '11, because 2 × 4 + 3 × 1 = 8 + 3.'],
                        ['What is the L2 norm of (6, 8)?', '10, because 36 + 64 = 100 and the square root of 100 is 10.'],
                        ['When is ranking by the raw dot product risky, and what fixes it?', 'When vector lengths differ: a long vector can win on length alone. Divide by both lengths (cosine), or normalise every vector to length 1 first.']],
                  widths=[5.4, 6.6], icons=['calculator', 'bars', 'magnifier'],
                  notes=('Last, the exit check. Write your answers in your notes first. One, what is the dot product of two three and four one? Two, what is the L2 norm of six eight? '
                         'Three, when is ranking by the raw dot product risky, and what fixes it? The short answers are on the slide. If you got all three, you are ready for matrices next session. If one surprised you, look at that part of the lab again tonight.')))

    s['facilitator'] = dict(
        prep=['Open the deck, the Python notebook in Colab and the workbook before anyone arrives. Run the notebook once from the top.',
              'Write the "check your numbers" table on the board before the lab.', 'Draw the arrows (3, 4) and (4, 3) on the board with squared paper. Learners should see the angle with their own eyes.',
              'Remind learners that Session 1 files are not needed today. Everything is built again from the given numbers.'],
        misconceptions=[('A longer text gives a longer vector, so cosine is needed for that reason', 'Not in our data, and not in general: vector length is unrelated to text length here, and many models normalise to length 1. Cosine protects against vectors that are long for any reason.'),
                        ('The dot product is a vector', 'The dot product of two vectors is a single number. Multiplying matching entries gives a vector of products, and the sum of those gives the dot product.'),
                        ('A bigger dot product always means more similar', 'It also grows with the lengths. Cosine similarity divides the lengths out.'),
                        ('Cosine similarity is the angle', 'It is the cosine of the angle. 0.96 corresponds to 16.26 degrees. 1 means the same direction.'),
                        ('The embedding numbers have meaning, such as d1 is money', 'In real embeddings no single number has a name. Only the whole vector carries meaning.')],
        probes=[('What is the dimension of the vector (21, 6, 72)?', '3.'), ('What is the dot product of u with itself, and how does it relate to the norm?', 'It is the squared norm. The norm is the square root of u dot u.'),
                ('Why can we not add (1, 2) and (1, 2, 3)?', 'The vectors have different numbers of entries.'), ('What is the cosine similarity of (1, 2) and (3, 6)?', '1, because they point the same way.'),
                ('What is the cosine similarity of (1, 0) and (0, 1)?', '0, because they are at a right angle.'), ('What is the distance between (1, 2) and (3, 6)?', 'The square root of 20, about 4.47.'),
                ('Why does an AI search need an embedding step?', 'Computers compare numbers. The embedding turns text into numbers so that similar meanings are close.'),
                ('Can the cosine similarity be negative?', 'Yes, down to −1 for opposite directions. Our toy embeddings have no negative entries, so it stays at or above 0.'),
                ('Does a longer text give a longer embedding vector?', 'No. In our toy data the lengths (0.83 to 0.95) have nothing to do with word count, and many real models normalise every vector to length 1.')],
        lab_steps=[('Steps 1 and 2: add, scale, dot, norm', 'a + b = (7, 7), 2a = (6, 8), u·v = 4, norm of a = 5. Python learners may mix up * (entry by entry) and @ (dot product).'),
                   ('Step 3: distance', 'Distance 5. Check they subtract first and then take the norm. Spreadsheet: SQRT(SUMXMY2(P, R)).'),
                   ('Step 4: cosine and angle', '0.96 and 16.26 degrees. ACOS and np.arccos give radians (0.284), so wrap them in DEGREES or np.degrees.'),
                   ('Step 5: all six cosines', 'Python: one line with E @ q and the norms. Spreadsheet: one row per sentence, three formulas. Values 0.995, 0.994, 0.087, 0.286, 0.414, 0.097.'),
                   ('Step 6: best match', 'Sentence 1 (index 0). Python: np.argmax. Spreadsheet: INDEX and MATCH on the maximum.'),
                   ('Step 7: stretch', 'After multiplying the picnic sentence by 20, its dot product becomes 1.6 and beats 0.785, but its cosine stays 0.097. Learners compute that cosine themselves from the formula. Many real embedding models normalise vectors to length 1, where the two agree.')],
        rescue=['If the concepts run over, skip the Euclidean distance formula slide and treat distance in the lab only.', 'If only thirty minutes of lab remain, do steps 1 to 6 and skip step 7, which you can show on the projector.',
                'If a learner has no laptop, pair them with a neighbour.', 'If the notebook will not open, use the workbook, which has the same numbers.'],
        after=['Share the lab files again.', 'Ask learners to add four formulas to the one-page sheet.', 'Note any question you could not answer and open Session 3 with it.'],
        lab_answer_key=[['Step 1 PREDICT: what is a + b?', '(7, 7).'], ['Step 2 PREDICT: what is the norm of u = (1, 2, 2)?', '3.'], ['Step 4 READ: is the cosine near 1 or near 0, and why?', 'Near 1 (0.96). The arrows point almost the same way.'],
                        ['Step 5 READ: which two sentences score highest, and why?', 'S1 and S2, both about passwords.'], ['Step 7 PREDICT: the stretched picnic dot product?', '1.6, twenty times 0.08, which beats 0.785.'],
                        ['Step 7 CHANGE: change the factor 20 to 2. What happens to the dot product?', 'It is 0.16, below 0.785, so sentence 1 wins again. The cosine stays 0.097 for any factor.'],
                        ['Step 3 CHANGE: set R to (7, 9). What is the distance from P?', '10, because the difference is (6, 8).']])
    return s
