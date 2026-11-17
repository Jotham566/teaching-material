"""Session 6: SVD and PCA. Rotate, stretch, rotate; low-rank approximation of an 8 by 8 image; PCA from the covariance matrix; choosing components; LoRA."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'kit'))
import diagrams_math_b as MB  # noqa: E402


def build():
    d = MB.d6()
    p5 = MB.d5()
    A, U, S, Vt, AtA = d['A'], d['U'], d['S'], d['Vt'], d['AtA']
    Sn, cum, energy = d['Sn'], d['cum'], d['energy']
    err_k, err0 = d['err_k'], d['err_noisy']
    C = p5['C']
    lam = p5['lam']
    top = d['top']
    scores = d['scores']
    Xc = d['Xc']
    H, noisy = d['H'], d['noisy']
    g = lambda v, k=2: f'{v:.{k}f}'
    gm = lambda v, k=3: f'{v:.{k}f}'.replace('-', '−')
    dfl = d['defl']
    gi = lambda v: f'{v:.0f}'
    mat = lambda M: [[float(v) for v in row] for row in np.asarray(M)]
    Ld, Lr = d['lora_d'], d['lora_r']
    full, small = d['lora_full'], d['lora_small']
    v1 = Vt[0] if Vt[0][0] > 0 else -Vt[0]
    U_r, Vt_r = U.copy(), Vt.copy()          # print U and V as proper rotations (determinant +1): flip the second pair together, A = U Σ Vᵀ still holds
    if np.linalg.det(U_r) < 0 and np.linalg.det(Vt_r) < 0:
        U_r[:, 1], Vt_r[1] = -U_r[:, 1], -Vt_r[1]
    u1 = A @ v1 / S[0]
    T_ata, D_ata = float(np.trace(AtA)), float(np.linalg.det(AtA))
    root_ata = (T_ata ** 2 - 4 * D_ata) ** 0.5
    pts = [(float(a), float(b)) for a, b in Xc]
    sig_c = np.linalg.svd(Xc, compute_uv=False)
    clock = [(10, 'Recall, then a real question from AI'), (35, 'Concept: picture, then a hand example'), (10, 'Break'), (45, 'Lab: predict, run, change one thing'),
             (15, 'Where it appears in AI, plus an exit check'), (5, 'Save the work')]

    s = dict(
        num=6, block='Linear algebra', short_title='SVD and PCA',
        title='SVD and PCA: rotate, stretch, rotate, and keep only what matters',
        question='How can a huge matrix be squeezed into a few numbers, and how does LoRA fine-tune a large model cheaply?',
        outcomes=['Describe the singular value decomposition (SVD) as rotate, stretch, rotate, and read its singular values',
                  'Build a low-rank approximation of an 8 by 8 image, and choose how many components to keep',
                  'Do principal component analysis (PCA) by hand: centre, covariance, top direction, projection and explained variance'],
        outcome_icons=['gear', 'grid', 'chart'],
        outcome_note=('By the end of today you can describe the singular value decomposition, or SVD, as rotate, stretch, rotate, and read its singular values. '
                      'You can build a low-rank approximation of a small image and choose how many components to keep. '
                      'And you can do principal component analysis by hand: centre the data, build the covariance matrix, find the top direction, project and measure the explained variance. We also meet LoRA, the way large models are fine-tuned cheaply. Which of these sounds most useful for your own work?'),
        clock=clock, plan_title='Your two hours: break a matrix apart, then keep the best terms', plan_caption='Pictures first. Then the lab in Python or in a spreadsheet. Then where it shows up in AI.',
        plan_note=('We have two hours. Ten minutes to bring back Session 5 and set the question of the day. Thirty-five minutes of ideas, each as a picture and then a small calculation by hand. '
                   'A ten minute break. Then forty-five minutes of lab, in Python or a spreadsheet, on the same numbers. We end with where this appears in AI tools, an exit check, and five minutes to save.'),
        recall_from='Session 5',
        recall=[('The covariance matrix of two marks has eigenvalues 102 and 2. What do these two numbers mean?', 'Each eigenvalue is the variance of the data along its eigenvector. Almost all the spread lies along the first direction.'),
                ('In power iteration, why divide by the largest entry, and what does that entry estimate?', 'Dividing keeps the numbers from growing. The largest entry estimates the top eigenvalue.'),
                ('How are the trace and the determinant of a 2 by 2 matrix linked to its eigenvalues?', 'The eigenvalues add up to the trace and multiply to the determinant.')],
        words=[('Singular value decomposition (SVD)', 'Any matrix written as rotate, stretch, rotate: A = UΣVᵀ.'),
               ('Singular value', 'A stretch factor in Σ. The singular values are listed from largest to smallest.'),
               ('Low-rank approximation', 'A matrix rebuilt from only its first few singular values. It needs far fewer numbers to store.'),
               ('Principal component analysis (PCA)', 'Finding the directions of greatest spread in data, then keeping only the first few.'),
               ('Fine-tuning and LoRA', 'Fine-tuning: training an already trained model a little more on new data (training is taught in Sessions 7 to 10). LoRA (low-rank adaptation) does it with two thin matrices.')],
        word_icons=['gear', 'bars', 'grid', 'chart', 'lock'],
        words_note=('Five words. The singular value decomposition, or SVD, writes any matrix as rotate, stretch, rotate. A singular value is one of the stretch factors, listed from largest to smallest. '
                    'A low-rank approximation rebuilds a matrix from only its first few singular values, which needs far fewer numbers. Principal component analysis, or PCA, finds the directions of greatest spread in data. '
                    'Fine-tuning means training an already trained model a little more on new data, and Sessions 7 to 10 show what training is. LoRA is a published method that fine-tunes with two thin matrices.'),
        keep='Keep the saved lab and these numbers: singular values 3 and 2 for the small matrix, 36.8 and 15.1 for the noisy image, and 98.1 percent of the variance of the eight marks on one direction.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Saved lab', value='Notebook or workbook, saved'), dict(label='Small matrix', value='Singular values 3 and 2'),
                                                            dict(label='Eight marks', value='98.1% on one direction'), dict(label='Next session', value='Derivatives')]),
        keep_title='Save the lab and keep the key singular values',
        next='Session 7: derivatives. We leave linear algebra and start calculus, the tool that tells a model which way to improve.', next_label='Next session',
        keep_note=('Before you go, save your work with all checks green. Keep three facts: the singular values three and two of the small matrix, the two big singular values of the noisy image, and the 98.1 percent for the eight marks. '
                   'Next session we begin calculus with derivatives, which tell a model which way to change a number to reduce its error. Write down any question about SVD or PCA and bring it.'),
        cover_note=('Welcome to Session 6, the last session of linear algebra. Last time we found directions that a matrix only stretches. Today every matrix gets the same treatment, even a non-square one. '
                    'We split it into rotate, stretch, rotate, keep the big stretches, and use the idea to compress an image and to reduce data. We end with how a published method called LoRA uses the same idea to fine-tune large models cheaply.'),
        slides=[])
    S_ = s['slides']

    S_.append(dict(kind='table', title='Answers to the three questions from Session 5', headers=['Question', 'Short answer'], rows=[[q, a] for q, a in s['recall']], widths=[5.6, 6.4], icons=False,
                   note='If one surprised you, look back at Session 5 before the lab. Eigenvalues return today.',
                   notes=('The eigenvalues of the covariance matrix, one hundred two and two, are the variances of the data along the two eigenvector directions. Almost all the spread lies along the first one. '
                          'In power iteration we divide by the largest entry to keep the numbers from growing, and that entry estimates the top eigenvalue. '
                          'And the eigenvalues of a two by two matrix add up to its trace and multiply to its determinant. If one of these surprised you, look at Session 5 again before the lab.')))

    S_.append(dict(kind='wide', title='Any matrix acts as rotate, stretch, rotate',
                   visual=dict(kind='svdpic'),
                   caption='A has rows (2, 2) and (−1, 2): rotate, stretch by 3 and 2, rotate (maybe with a mirror flip).',
                   notes=('Take any matrix, here the one with rows two, two and minus one, two. It turns the unit circle into an ellipse, and it always does so in three simple moves. '
                          'First rotate, so that two special directions, the red arrow v one and the black arrow v two, lie along the axes. These two directions are called the right singular vectors. The first two panels are zoomed in so you can see them. '
                          'Second, stretch along the axes, here by three across and by two up. Third, rotate again into the final position. The stretch factors three and two are the singular values. '
                          'For some matrices one of the rotations must include a mirror flip, and that is allowed.')))

    S_.append(dict(kind='formula', title='The singular value decomposition writes A as UΣVᵀ',
                   formulas=[('Definition', r'$A = U\,\Sigma\,V^{T}$'), ('Singular values of our A', r'$\Sigma = \mathrm{diag}(3,\ 2)$')],
                   symbols=[['Vᵀ', 'First rotation. Its rows are the right singular vectors.', f'rows ({gm(Vt_r[0][0])}, {gm(Vt_r[0][1])}) and ({gm(Vt_r[1][0])}, {gm(Vt_r[1][1])})'],
                            ['Σ', 'The stretch. diag(3, 2): 3 and 2 on the diagonal, zeros elsewhere. Not the sum symbol.', '3 and 2'],
                            ['U', 'Last rotation. Its columns are the left singular vectors.', f'columns ({gm(U_r[0][0])}, {gm(U_r[1][0])}) and ({gm(U_r[0][1])}, {gm(U_r[1][1])})'],
                            ['Signs', 'U and V are rotations, sometimes with a mirror flip. Tools may flip a pair.', 'both are correct']],
                   widths=[1.3, 6.6, 4.0], size=22, note='A can be any shape, m by n: U is m by m, Σ m by n, V n by n. Singular values are never negative.',
                   notes=('The decomposition fits on one line: A equals U, times Sigma, times V transpose. Read it from the right, because that is the order the moves happen. '
                          'V transpose rotates first, and its rows are the right singular vectors. Sigma stretches, with the singular values on its diagonal, largest first. This capital Sigma is a matrix of stretch factors, unrelated to the sum symbol from Session 1. U rotates last, and its columns are the left singular vectors. '
                          'A tool may print a pair of singular vectors with both signs flipped, which turns a rotation into a mirror image, and both answers are correct. '
                          'Unlike eigenvalues, the SVD works for a matrix of any shape, and its singular values are never negative.')))

    S_.append(dict(kind='example', title='Worked by hand: singular values from AᵀA',
                   scenario='A has rows (2, 2) and (−1, 2). The singular values are the square roots of the eigenvalues of AᵀA.',
                   blocks=[dict(label='Form AᵀA', text=f'Rows ({gi(AtA[0, 0])}, {gi(AtA[0, 1])}) and ({gi(AtA[1, 0])}, {gi(AtA[1, 1])}). It is symmetric, so Session 5 applies.'),
                           dict(label='Eigenvalues', text=f'T = {gi(T_ata)} and D = {gi(D_ata)}. The root of {gi(T_ata)}² − 4 × {gi(D_ata)} is {gi(root_ata)}. So λ = 9 and 4.'),
                           dict(label='Singular values', text='σ₁ = the square root of 9 = 3 and σ₂ = the square root of 4 = 2.'),
                           dict(label='Vectors', text=f'For λ = 9, v₁ = (1, 2) / the square root of 5 = ({gm(v1[0])}, {gm(v1[1])}). Then u₁ = Av₁ / 3 = ({gm(u1[0])}, {gm(u1[1])}).', red=True)],
                   notes=('Session 5 gives us the singular values by hand. Form A transpose times A. For our matrix it has rows five, two and two, eight. That matrix is symmetric, so we can find its eigenvalues from the trace and the determinant. '
                          'The trace is thirteen and the determinant is thirty-six. The square root part is the square root of one sixty-nine minus one forty-four, which is five. So the eigenvalues are nine and four. '
                          'The singular values are their square roots, three and two. For the vectors, the eigenvector of A transpose A for nine is one, two over root five, and we call it v one. Then u one is A times v one divided by three. '
                          'For a covariance matrix the eigenvalues and the singular values agree, which is why PCA can use either.')))

    S_.append(dict(kind='wide', title='A grey-scale image is a matrix of numbers, and noise spoils its pattern',
                   visual=dict(kind='imgs', numbers=True, items=[dict(title='Clean pattern H', sub='an H shape: cells 1 or 8', m=mat(H)), dict(title='Noisy image N', sub=f'error {g(err0, 2)} from the clean one', m=mat(noisy))]),
                   caption='Illustrative: each cell is 0 (white) to 9 (black). Error = √(sum of the 64 squared cell differences).',
                   notes=('An image is a grid of numbers, so it is a matrix. Our toy image is eight by eight, with each cell between zero for white and nine for black, and you can read every number in the picture. '
                          'On the left is a clean pattern, the letter H, made of cells with values one and eight. On the right is the same image after we added random noise of up to two in each cell. We call the noisy image N, to keep the letter A for the small matrix. The numbers are made up to show the arithmetic. '
                          'The error under the noisy picture is the square root of the sum of the squared differences of all sixty-four cells from the clean one: 8.19.')))

    S_.append(dict(kind='idea', title='A column times a row makes a rank 1 pattern from only 16 numbers',
                   visual=dict(kind='outer', u=[float(v) for v in d['u1']], v=[float(v) for v in d['v_unit']]),
                   lead='A column u of 8 numbers times a row vᵀ of 8 numbers. Cell (i, j) is the i-th number of u times the j-th number of v.',
                   points=['Every row of the result is a multiple of the row vᵀ. That is rank 1.', 'Dark cells appear where both numbers are large.'],
                   notes=('The building block of a low-rank approximation is a column times a row. Take a column of eight numbers, u, and a row of eight numbers, v transpose. Multiply every pair, so that the cell in row i and column j is the i-th number of u times the j-th number of v. '
                          'The result is a grid of sixty-four cells made from only sixteen numbers. Every row of the grid is a multiple of the same row, which is what rank one means. '
                          'Here u and v are the first singular vectors of our noisy image, so the dark pattern is the best single pattern of this shape. The darkest cells sit where both u and v are large.')))

    S_.append(dict(kind='formula', title='SVD adds up rank 1 terms, and a low-rank approximation keeps the first few',
                   formulas=[('Sum of terms', r'$N = \sigma_1\mathbf{u}_1\mathbf{v}_1^{T} + \sigma_2\mathbf{u}_2\mathbf{v}_2^{T} + \cdots$'), ('Rank k approximation', r'$N_k = \sum_{i=1}^{k}\sigma_i\,\mathbf{u}_i\mathbf{v}_i^{T}$')],
                   symbols=[['σᵢ', 'The i-th singular value of N. Big ones carry the pattern.', f'{g(Sn[0], 1)}, {g(Sn[1], 1)}, {g(Sn[2], 1)}, ...'],
                            ['uᵢ, vᵢ', 'The i-th left and right singular vectors, columns of U and V.', 'one pair per term'],
                            ['k', 'How many terms we keep. Rank k means k independent patterns.', 'k = 2'],
                            ['Storage', 'A rank k approximation needs k × (m + n + 1) numbers: u, v and σ for each term.', f'k = 2: 2 × (8 + 8 + 1) = {d["img_k2"]} against {d["img_full"]}']],
                   widths=[1.8, 6.1, 4.0], size=22, note='The first k terms give the closest rank k matrix to N (the Eckart-Young theorem).',
                   notes=('A low-rank approximation is built from the SVD written as a sum of rank one terms, each one a singular value times a column times a row. The big singular values come first. '
                          'To approximate the image, keep only the first k terms and drop the rest. Each kept term costs m plus n plus one numbers: the column, the row and the singular value. '
                          'For an eight by eight image with k equal to two that is thirty-four numbers instead of sixty-four. A known result, the Eckart-Young theorem, says no other rank k matrix is closer to the matrix you have.')))

    ims = [dict(title='Noisy image N', sub=f'error {g(err0, 2)}', m=mat(noisy))]
    for k in (1, 2, 3):
        ims.append(dict(title=f'Rank {k}', sub=f'error {g(err_k[k], 2)}', m=mat(d['approx'](k))))
    S_.append(dict(kind='wide', title='Rank 2 removes most of the noise, and more terms bring the noise back',
                   visual=dict(kind='imgs', items=ims),
                   caption='Error is measured against the clean H. Rank 2 lands closest; rank 3 starts to copy the noise.',
                   notes=(f'The rebuilt images are scored against the clean pattern, so we are checking how well the approximation recovers the truth. The noisy image has error {g(err0, 2)}. '
                          f'With one term, the error is {g(err_k[1], 2)}, worse, because one pattern cannot draw an H. With two terms the error drops to {g(err_k[2], 2)} and the H is clear. '
                          f'With three terms the error rises to {g(err_k[3], 2)}. Rank three is still the closest rank three matrix to the noisy image, but the extra term starts to copy the noise. The clean H has two independent patterns, which is why two is right. '
                          'In real work you do not know the clean image, so you need a rule.')))

    S_.append(dict(kind='idea', title='Singular values show how many terms matter: a few big bars, then a flat tail',
                   visual=dict(kind='scree', values=[float(v) for v in Sn], cum=[float(c) for c in cum], mark=2, label='Singular value'),
                   lead='The 8 singular values of the noisy image, largest first. The cumulative share is the running total of σ² divided by the total.',
                   points=[f'Two terms hold {gi(100 * cum[1])} percent of the total.', 'The pattern lives in the big values. Random noise spreads thinly over all eight.'],
                   notes=(f'The singular values of the noisy image are in this bar chart, a plot often called a scree plot. There are two big bars, {g(Sn[0], 1)} and {g(Sn[1], 1)}, and then a flat tail of small ones. '
                          f'The row of percentages is the cumulative share: the running total of the squared singular values divided by their grand total. Two terms already hold {gi(100 * cum[1])} percent. '
                          'The picture shows why truncation removes noise. The real pattern is concentrated in a few big singular values. Random noise has no preferred direction, so it spreads thinly over all of them.')))

    S_.append(dict(kind='table', title='How many terms to keep: three rules, and what each one needs',
                   headers=['Rule', 'How it works', 'Watch out'],
                   rows=[['Cumulative share', f'Add the shares until you reach a target such as 95 percent. Image: k = {d["k95"]}.', 'The target is a choice. Ask what the next step needs.'],
                         ['Elbow of the scree plot', 'Cut where the bars stop falling steeply. Image: after bar 2.', 'Some plots have no clear elbow.'],
                         ['Test the real task', 'Try k = 1, 2, 3 and score the model on held-out data: rows kept aside, never used for fitting.', 'Needs the full pipeline, but is the most honest.']],
                   widths=[3.0, 5.0, 3.9], icons=['chart', 'bars', 'check'],
                   note=f'Errors from the clean H, for k = 1, 2, 3: {g(err_k[1])}, {g(err_k[2])}, {g(err_k[3])}. We can measure them only because we built the clean image.',
                   notes=('Three rules decide how many terms to keep, and the same rules apply to PCA later today. First, the cumulative share: add up the shares until you reach a target, such as ninety-five percent. For our image that gives two. The target is your choice, so ask what the next step needs. '
                          'Second, the elbow: cut where the bars stop falling steeply. Here that is after bar two. Some plots have no clear elbow. '
                          'Third, test the real task: try one, two and three terms and score the model on held-out data, which means rows you kept aside and never used for fitting. That is the most honest answer.')))

    S_.append(dict(kind='wide', title='A low-rank approximation stores thin matrices instead of the whole matrix',
                   visual=dict(kind='lowrank', m=8, n=8, k=2),
                   caption=f'Here {d["img_k2"]} numbers replace {d["img_full"]}. At 1,000 by 1,000 and rank 20: 40,020 against 1,000,000 (illustrative).',
                   notes=('The saving can be drawn. The big matrix is approximately a thin tall matrix U k, times a small square Sigma k, times a thin wide matrix V k transpose. Only the diagonal numbers of Sigma k are stored, the two gold cells. '
                          'For our image that is thirty-four numbers instead of sixty-four, a modest saving. The saving grows with size. For a matrix with a thousand rows and a thousand columns, a rank twenty approximation stores about forty thousand numbers instead of one million. '
                          'That size is illustrative. This is the heart of compression, and, as we will see at the end, of how large models are fine-tuned cheaply.')))

    S_.append(dict(kind='steps', title='PCA is five steps: centre, covariance, directions, project, measure',
                   steps=[dict(head='1 Centre', text='Subtract each column mean', icon='pin'), dict(head='2 Covariance', text='Build C from the centred data', icon='grid'),
                          dict(head='3 Directions', text='Eigenvectors of C, largest first', icon='magnifier'), dict(head='4 Project', text='One score per row along each direction', icon='chart'),
                          dict(head='5 Measure', text='Explained variance of each direction', icon='calculator')], highlight=3,
                   caption='Principal component analysis (PCA). The directions are the principal components. Steps 1 to 3 are Session 5.',
                   notes=('Principal component analysis, or PCA, is a recipe of five steps, and you already know most of them from Session 5. Centre each column by subtracting its mean. Build the covariance matrix, dividing by n minus one. '
                          'Find its eigenvectors, largest eigenvalue first. These directions are called the principal components. '
                          'Then project: give every row a score, which is how far it sits along a direction. And measure how much of the total variance each direction explains. Steps four and five are new today.')))

    S_.append(dict(kind='idea', title='Projecting onto the first principal component turns 2 numbers per student into 1',
                   visual=dict(kind='cloud', points=pts, axes=[dict(v=tuple(float(t) for t in top), len=12.5, label='principal component 1', at=0.5, ha='left', dx=0.15, dy=-0.45)], project=0, annotate_first=True,
                               xlabel='Centred maths mark (across) and centred physics mark (up)'),
                   lead='The eight centred marks from Session 5. Each dot drops straight onto the red arrow, the first principal component.',
                   points=['The red dots on the arrow are the projections.', 'A score is the position of the red dot along the arrow, in mark points.', 'The dashed lines show what is lost.'],
                   notes=('These are the eight students from Session 5, centred. The red arrow is the first principal component, direction zero point eight, zero point six. Each dot drops straight onto the arrow along a dashed line, and the red dot is its projection. '
                          'The position of the red dot along the arrow is a single number, the score of that student, measured in mark points. The first student sits at minus seven, minus five, and has a score of minus eight point six. So two numbers per student have become one. '
                          'The dashed lines are short, which tells us that very little is lost. In a round blob of dots they would be long.')))

    S_.append(dict(kind='formula', title='A score is a dot product with the principal component, and explained variance is a ratio',
                   formulas=[('Score of student i', r'$z_i = \mathbf{v}_1^{T}\mathbf{x}_i = v_{11}\,m_i + v_{12}\,p_i$'), ('Explained variance ratio', r'$\mathrm{ratio}_1 = \lambda_1\ /\ (\lambda_1 + \lambda_2)$')],
                   symbols=[['v₁', 'Principal component 1: the top eigenvector of C, length 1. Its entries are v₁₁ and v₁₂.', f'({g(top[0], 1)}, {g(top[1], 1)})'],
                            ['xᵢ', 'Centred marks of student i, as a column: maths mᵢ and physics pᵢ.', 'first student: (−7, −5)'],
                            ['zᵢ', 'The score: the dot product v₁ᵀxᵢ.', f'0.8 × (−7) + 0.6 × (−5) = {gm(scores[0], 1)}'],
                            ['λ', 'Eigenvalues of C: the variances along each direction.', f'{gi(lam[0])} and {gi(lam[1])}'],
                            ['Ratio', 'Share of the variance kept by component 1.', f'{gi(lam[0])} / {gi(lam[0] + lam[1])} = {g(100 * lam[0] / lam.sum(), 1)} percent']],
                   widths=[1.5, 6.3, 4.1], size=18, note='Keep the first component and drop the second: 98.1 percent of the variance is kept, 1.9 percent is lost.',
                   notes=('Two formulas do the work. The score of a student is the dot product of the principal component v one with the student\'s centred marks, maths m i and physics p i. For the first student, minus seven and minus five, '
                          'zero point eight times minus seven plus zero point six times minus five is minus eight point six. '
                          'The explained variance ratio is the eigenvalue of the component divided by the total of all eigenvalues. Here one hundred two over one hundred four, which is ninety-eight point one percent. '
                          'So keeping one number per student keeps almost all the information about how the students differ, and one component is enough.')))

    rows = [[f'{i + 1}', gi(Xc[i, 0]).replace('-', '−'), gi(Xc[i, 1]).replace('-', '−'), g(scores[i], 1).replace('-', '−')] for i in range(8)]
    S_.append(dict(kind='table', title='Worked by hand: the eight scores, and the variance they keep',
                   headers=['Student', 'Centred maths', 'Centred physics', 'Score = 0.8 × maths + 0.6 × physics'], rows=rows, widths=[1.6, 2.6, 2.8, 5.0], icons=False,
                   note=f'The scores have mean 0 and variance {gi(d["score_var"])} (sum of squares {gi(np.sum(scores ** 2))}, divided by n − 1 = 7). The squared distances dropped add up to {gi(d["lost"])}, which is 7 × 2.',
                   notes=(f'All eight scores follow the same rule: zero point eight times the centred maths mark plus zero point six times the centred physics mark. The scores run from {g(scores.min(), 1)} to {g(scores.max(), 1)}. '
                          f'Their mean is zero because the data were centred. Their variance, the sum of squares divided by seven, which is n minus one as in Session 5, is {gi(d["score_var"])}, the first eigenvalue. That is the meaning of an eigenvalue of the covariance matrix. '
                          f'The squared distances from the dots to the arrow, the dashed lines, add up to {gi(d["lost"])}, which is seven times the second eigenvalue. So the second eigenvalue measures what we throw away.')))

    S_.append(dict(kind='formula', title='PCA is the SVD of the centred data',
                   formulas=[('SVD of the centred data', r'$X_c = U\,\Sigma\,V^{T}$'), ('Variance along component i', r'$\lambda_i = \sigma_i^{2}\ /\ (n - 1)$')],
                   symbols=[['Xc', 'The centred data, one row per student and one column per mark.', '8 by 2'],
                            ['V', 'Its columns are the principal components, the same as the eigenvectors of C.', f'v₁ = ({g(top[0], 1)}, {g(top[1], 1)})'],
                            ['σᵢ', 'The singular values of Xc.', f'{g(sig_c[0], 2)} and {g(sig_c[1], 2)}'],
                            ['λᵢ', 'Variance along component i: σ² over n − 1, the sample variance of Session 5.', f'{g(sig_c[0] ** 2 / 7, 0)} and {g(sig_c[1] ** 2 / 7, 0)}'],
                            ['Scores', 'The columns of UΣ are the scores of all rows at once.', f'first score {gm(scores[0], 1)}']],
                   widths=[1.5, 6.2, 4.2], size=18, note='Libraries use the SVD because it is more accurate than forming C first. Component signs may differ.',
                   notes=('This links today and last session. Take the centred data matrix X c and compute its SVD. The columns of V are the principal components, the same directions as the eigenvectors of the covariance matrix. '
                          'The variance along component i is sigma i squared divided by n minus one. For our marks the singular values are 26.72 and 3.74, and their squares divided by seven give one hundred two and two. '
                          'Libraries compute PCA this way because it is more accurate than forming the covariance matrix first. Signs of components may differ between tools, and both are correct.')))

    S_.append(dict(kind='table', title='Four habits that keep SVD and PCA honest', headers=['Mistake', 'What is true', 'What to do'],
                   rows=[['Running PCA on data that is not centred', 'The first direction then points at the mean, not at the spread.', 'Subtract the column means first.'],
                         ['Mixing columns on different scales', 'A column in thousands dominates a column in units.', 'Divide each centred column by its standard deviation, the square root of its variance (z-scores, Session 14).'],
                         ['Treating a component as a named feature', 'It is a mix of all columns, and its sign is arbitrary.', 'Read the weights, and expect sign flips.'],
                         ['Keeping the most terms that fit', 'Small singular values often hold only noise.', 'Choose k with a rule, and check on held-out data.']],
                   widths=[3.7, 4.3, 3.9], icons=['cross', 'cross', 'cross', 'cross'],
                   notes=('Four things to remember. First, centre the data before PCA. Without centring, the first direction points towards the mean instead of along the spread. '
                          'Second, mind the scales. A column measured in thousands would dominate a column measured in units, so when the units differ, divide each centred column by its standard deviation, the square root of the variance from Session 5. These are called z-scores, and Session 14 uses them again. '
                          'Third, a component is a mix of all the columns, and its sign is arbitrary, so do not read it as a single named feature. '
                          'Fourth, do not keep every term that fits. Small singular values often hold only noise.')))

    S_.append(dict(kind='code', title='One function, np.linalg.svd, gives the low-rank image and the PCA',
                   code='U, S, Vt = np.linalg.svd(M)\nM2 = (U[:, :2] * S[:2]) @ Vt[:2]\nXc = X - X.mean(axis=0)\nU, S, Vt = np.linalg.svd(Xc, full_matrices=False)\nscores = Xc @ Vt[0]\nratio = S ** 2 / np.sum(S ** 2)',
                   reads=['U, S, Vt = ... svd of any matrix M, such as the noisy image. S is a list, largest first.', 'M2 = ... scales the first 2 columns of U by their singular values, then multiplies by the first 2 rows of Vt.',
                          'Xc = ... centres X. full_matrices=False keeps only the columns of U that are needed (2 here, not 8).', 'scores = ... dots each row with component 1. ratio = ... is the explained variance.'],
                   notes=('The code is six lines. np dot linalg dot svd returns three things: U, the singular values as a plain list from largest to smallest, and V transpose. M is any matrix, for example the noisy image. '
                          'For a low-rank approximation, take the first two columns of U, scale each by its singular value, and multiply by the first two rows of V transpose. '
                          'For PCA, centre the data X, take its SVD, and the first row of V transpose is the first principal component. The setting full matrices equals False keeps only the two columns of U we need instead of eight. Multiply the centred data by the component to get the scores. '
                          'The last line is the explained variance ratio.')))

    S_.append(dict(kind='divider', title='Part 2: the lab', lead='Close the slides. Open the notebook or the workbook.', section='Lab',
                   notes=('That is the end of the ideas. In the lab you compute the SVD of the small matrix, build low-rank images, run PCA on the eight marks, and finish with the LoRA counts. '
                          'Choose the Python notebook or the spreadsheet workbook. The numbers are identical in both, and each step ends with an automatic check. '
                          'Neither Excel nor Google Sheets has an SVD function, so in the spreadsheet you build the singular values with power iteration in cells. Predict, run, read, then change one thing. Raise your hand when a check stays red.')))

    S_.append(dict(kind='steps', title='Six lab steps, from a 2 by 2 SVD to the LoRA count',
                   steps=[dict(head='1 Small SVD', text='Singular values 3 and 2 from AᵀA', icon='gear'), dict(head='2 Image', text='Noisy 8 by 8 pattern', icon='grid'),
                          dict(head='3 Low rank', text='Rank 1, 2, 3 and the errors (Python)', icon='bars'), dict(head='4 PCA', text='Centre, project, explained variance; then by SVD', icon='chart'),
                          dict(head='5 Power', text='σ₁ to σ₃ and the errors, by deflation', icon='clock'), dict(head='6 LoRA', text='Count the numbers saved', icon='lock')], highlight=3,
                   caption='Python uses np.linalg.svd. The spreadsheet uses MMULT, SUMPRODUCT, VAR.S and rows of cells (sheets Small, Image, Deflation, PCA, LoRA). Gold cells are yours.',
                   notes=('The map has six steps, the same in the notebook and the workbook. Step one, the singular values of the small matrix from A transpose A. Step two, the noisy eight by eight image. '
                          'Step three, Python only: low-rank images with the library and their errors. Step four, PCA on the eight marks in both tools, and in Python also by SVD. Step five, power iteration and deflation: singular values one, two and three and the rank one, two and three errors. That is how the spreadsheet manages without an SVD function. '
                          'Step six, count the numbers that LoRA saves.')))

    S_.append(dict(kind='example', title='Step 5 without an SVD function: power iteration on NᵀN, then deflation',
                   scenario='N is the noisy image. M = NᵀN is symmetric, and its top eigenvalue is σ₁².',
                   blocks=[dict(label='Power iteration', text=f'From all ones, ten rounds of multiply by M, divide by the largest entry: {g(dfl[0]["m"], 1)} = σ₁², so σ₁ = {g(dfl[0]["sigma"])}.'),
                           dict(label='Rank 1 term', text='v₁ = final guess at length 1, u₁ = Nv₁ / σ₁. σ₁u₁v₁ᵀ is a column times a row.'),
                           dict(label='Deflation', text=f'M₂ = M − σ₁²v₁v₁ᵀ removes the top eigenvalue. Repeat: σ₂ = {g(dfl[1]["sigma"])}. Once more: σ₃ = {g(dfl[2]["sigma"])}.'),
                           dict(label='Errors', text='Errors from the clean H: ' + ', '.join(g(x['err']) for x in dfl) + ' for ranks 1, 2, 3, as the library gives.', red=True)],
                   notes=(f'Neither Excel nor Google Sheets has an SVD function, so step five gets the singular values with Session 5. M equals N transpose N is symmetric, and its top eigenvalue is the first singular value squared. '
                          f'Run power iteration on M from a start of all ones, ten times. The largest entry settles at {g(dfl[0]["m"], 1)}, so sigma one is {g(dfl[0]["sigma"])}. Scale the guess to length one to get v one, and u one is N times v one over sigma one. '
                          'To get the next one, subtract sigma one squared times v one v one transpose from M, the same column-times-row pattern, and repeat. That is called deflation. '
                          'The errors match the library numbers, so both tracks reach the same answers.')))

    S_.append(dict(kind='table', title='Your numbers should match: 3 and 2, then 36.85 and 15.07, then 102 and 2', headers=['What you compute', 'You should see'],
                   rows=[['Singular values of A with rows (2, 2) and (−1, 2)', '3 and 2'], ['First three singular values of the noisy image', f'{g(dfl[0]["sigma"])}, {g(dfl[1]["sigma"])} and {g(dfl[2]["sigma"])}'],
                         ['Error from the clean image, ranks 1, 2 and 3', f'{g(err_k[1], 2)}, {g(err_k[2], 2)} and {g(err_k[3], 2)}'], ['Eigenvalues of C for the eight marks', f'{gi(lam[0])} and {gi(lam[1])}'],
                         ['Score of the first student', gm(scores[0], 1)], ['Variance of the eight scores, explained variance ratio', f'{gi(d["score_var"])} and {g(lam[0] / lam.sum(), 3)}'],
                         ['Largest entry after 10 power steps on NᵀN (σ₁²)', g(d['its'][-1][1], 1)], ['LoRA numbers for d = 1,000 and r = 8', f'{small:,} instead of {full:,}']],
                   widths=[7.0, 4.2], icons=['gear', 'grid', 'bars', 'magnifier', 'chart', 'calculator', 'clock', 'lock'],
                   note='If a number differs, stop and find the step that went wrong. Signs of singular vectors may differ between tools.',
                   notes=('Use this as your checkpoint. If your numbers match, carry on. If they do not, stop and call me over. The usual causes are forgetting to centre before PCA, dividing by n instead of n minus one when computing the covariance, '
                          'and mixing up U and V transpose. Singular vectors may come out with opposite signs in a different tool, and that is fine, so the notebook checks absolute values for those. '
                          'The ten power steps give the square of the first singular value, 1357.6, and the deflation rounds give the second and third. Please do not type a number just to make a check pass.')))

    S_.append(dict(kind='table', title='Slices, centring and array formulas cause most lab errors', headers=['Error or symptom', 'What it says', 'What to do'],
                   rows=[['S is a plain list of numbers', 'np.linalg.svd returns the singular values as a 1-D array.', 'Use np.diag(S), or scale the columns of U as in the recipe.'],
                         ['Low-rank image looks the same as the noisy one', 'k is too large, or the slice is wrong.', 'Slice the first k columns of U and the first k rows of Vt.'],
                         ['The first component points at the mean', 'The data were not centred.', 'Subtract the column means first.'],
                         ['#SPILL! or #N/A from an array formula', 'Excel 365: cells below are not empty. Older Excel: wrong range size.', 'Clear the cells, or select the exact range. Older Excel: Ctrl+Shift+Enter.']],
                   widths=[3.8, 4.1, 4.0], icons=['key', 'bell', 'cross', 'flag'],
                   notes=('Four things will happen to someone. First, np dot linalg dot svd gives you the singular values as a plain list of numbers. Use np dot diag to turn it into a diagonal matrix, or scale the columns of U as in the recipe. '
                          'Second, if your low-rank image looks the same as the noisy image, check that you sliced U and V transpose with the same k. '
                          'Third, a first component that points at the mean means the data were not centred. And a spill error in Excel 365 means the cells the answer fills are not empty. In older Excel, select the exact range and confirm with control, shift and enter.')))

    S_.append(dict(kind='wide', title='Where this appears in AI: LoRA trains two thin matrices in place of one huge one',
                   visual=dict(kind='lora', d=Ld, r=Lr),
                   caption='Illustrative sizes. LoRA (Hu et al., 2021) keeps W frozen (unchanged) and trains only B and A.',
                   notes=('This is the same mathematics in a published method. Training a model means adjusting its weights in small steps so that its errors shrink, and Sessions 7 to 10 show how. Fine-tuning means training an already trained, or pre-trained, model a little more on new data. '
                          'Large language models of this kind have enormous weight matrices, so fine-tuning every number is expensive. The LoRA paper, by Hu and colleagues in 2021, keeps the weight matrix W frozen and learns the change as a product of two thin matrices, B and A, whose shared inner size r is small. '
                          'A thousand by a thousand matrix has one million numbers, while B and A together have sixteen thousand.')))

    S_.append(dict(kind='formula', title='Where this appears in AI: LoRA in numbers',
                   formulas=[('Updated weights', r"$W' = W + B\,A$"), ('Trainable numbers', r'$2\,d\,r \ \ \mathrm{against}\ \ d^{2}$')],
                   symbols=[['W', 'The pre-trained weight matrix, d by d. Frozen: left unchanged.', f'd = {Ld:,} (illustrative)'], ['B and A', 'Thin, d by r and r by d, trained. A new A, unrelated to today\'s A.', f'r = {Lr}'],
                            ['Count', 'Numbers trained with LoRA against a full update.', f'2 × {Ld:,} × {Lr} = {small:,} ({100 * small / full:.1f}% of {full:,})'],
                            ['Start', 'B starts at zero, so the model begins as the original.', 'published detail']],
                   widths=[1.7, 6.3, 3.9], size=18, note='B and A are learned by training (Sessions 7 to 10); no SVD is computed. Open models such as Llama allow this.',
                   notes=('LoRA in numbers: the updated weights are the frozen weights W plus the product B times A. If W is d by d, then B is d by r and A is r by d. This A is a new matrix, unrelated to the small matrix A from the start of today. Only B and A are trained. '
                          f'With d equal to a thousand and r equal to eight, which are illustrative sizes, that is sixteen thousand trained numbers against one million for a full update, which is {100 * small / full:.1f} percent. '
                          'The paper starts B at zero, so the model begins as the original. B and A are found by the training steps of the coming sessions, and the SVD only explains why a low-rank change can be enough. '
                          'What closed products do internally is not public, so I will not claim it for them.')))

    S_.append(dict(kind='practice', title='Where this appears in AI: ask an assistant for an SVD, then check it', minutes=8, label='Hands-on, with any AI assistant',
                   task='Ask an assistant for an SVD, then check it.',
                   steps=['Ask for the singular values of the matrix with rows (2, 2) and (−1, 2). Expect 3 and 2.', 'Ask how many numbers LoRA trains for a 1,000 by 1,000 matrix with r = 8. Expect 16,000.',
                          'Ask for its working and read for mistakes. Never paste confidential data.'],
                   output='A note of which answers matched, and where the assistant slipped.',
                   notes=('A short activity. Open any assistant you use and ask for the singular values of the matrix with rows two, two and minus one, two. You know the answer: three and two. '
                          'Then ask how many numbers LoRA trains for a thousand by a thousand matrix with r equal to eight. You know that too: sixteen thousand. '
                          'Ask it to show its working and read it for slips. Assistants can make arithmetic errors, and checking against your own numbers is the skill. Never paste confidential data.')))

    S_.append(dict(kind='table', title='Exit check: the three moves, choosing k, and why LoRA is cheap', headers=['Question', 'Short answer'],
                   rows=[['What are the three moves of the SVD?', 'Rotate (Vᵀ), stretch (Σ, the singular values), rotate again (U).'],
                         ['How do you choose how many components to keep?', 'Use the cumulative explained variance, the elbow of the scree plot, or a test on the real task.'],
                         ['Why does LoRA train fewer numbers than a full update?', 'It trains two thin matrices B (d by r) and A (r by d) with small r, instead of one d by d matrix.']],
                   widths=[5.4, 6.6], icons=False, note='Write your own answer first, then compare. Your lab checks are part of the exit check.',
                   notes=('Three questions to finish. What are the three moves of the SVD? Rotate with V transpose, stretch with the singular values in Sigma, and rotate again with U. '
                          'How do you choose how many components to keep? Look at the cumulative explained variance, the elbow of the scree plot, or test on the real task. '
                          'And why does LoRA train fewer numbers than a full update? Because it trains two thin matrices with a small inner size r, instead of one big square matrix. Answer in your own words first.')))

    s['facilitator'] = dict(
        prep=['Run the notebook and the workbook once before class. The workbook has several array formulas, so check that they open in your tool.', 'Write the check numbers on the board: singular values 3 and 2; noisy image 36.85 and 15.07; eigenvalues 102 and 2; score of student 1 is -8.6.',
              'Have a printed 8 by 8 grid ready to show how an image is a matrix. Shade a few cells by hand.', 'Remind learners that signs of singular vectors differ between tools, and that a tool may print U or V with a mirror flip.',
              'LoRA: say only what Hu et al. (2021) publish. Do not describe how any closed product is fine-tuned. Training and fine-tuning get one plain line today; Sessions 7 to 10 teach training.'],
        misconceptions=[('The SVD only works for square matrices', 'It works for any shape. That is its advantage over eigenvalues.'), ('Singular values are the same as eigenvalues', 'The singular values of A are the square roots of the eigenvalues of A^T A. They agree with eigenvalues only for some matrices, such as covariance matrices.'),
                        ('PCA needs no preparation', 'Centre every column, and standardise when columns use different units.'), ('The first principal component is the most important feature', 'It is the direction of greatest spread. Whether spread matters for a task has to be tested.'),
                        ('A larger k is always better', 'Past the real pattern, extra terms copy noise. Our image error rises from rank 2 to rank 3.'),
                        ('LoRA computes B and A with an SVD', 'B and A are trained by gradient steps (Sessions 7 to 10). The SVD explains why a low-rank change can be enough.')],
        probes=[('Why are singular values never negative?', 'They are stretch factors. A flip is carried by the rotations U and V, not by Sigma.'), ('What would the singular values look like for a pure noise image?', 'A slowly falling list with no big gap, so no k stands out.'),
                ('Why does keeping the first terms remove noise?', 'The pattern is concentrated in the big singular values, and random noise is spread thinly over all of them.'), ('What does the SVD of the centred data have to do with the covariance matrix?', 'lambda = sigma squared / (n - 1), and the right singular vectors are the eigenvectors of C.'),
                ('Why can LoRA work with such a small r?', 'My understanding is that the paper hypothesises the change needed in fine-tuning has low intrinsic rank, and reports good results with small r. This is an empirical finding, not a theorem.')],
        lab_steps=[('Step 1: small SVD', 'Singular values 3 and 2. In the sheet they come from A^T A with the trace and determinant formula. Python learners should see np.linalg.svd return S as a list.'),
                   ('Step 2: image', 'The noisy matrix is built from a seeded generator in Python and typed into the sheet. Both show the same 64 numbers.'),
                   ('Step 3: low rank', 'Python library route. Errors 15.40, 4.54 and 6.73 for k = 1, 2, 3. The sheet gets the same three errors in step 5 by deflation.'),
                   ('Step 4: PCA', 'Eigenvalues 102 and 2, scores from -15.0 to 13.0, variance of scores 102, explained ratio 0.981, lost squared distance 14. Python then repeats it by SVD: S squared over 7 gives 102 and 2.'),
                   ('Step 5: power iteration and deflation', 'Largest entry 1357.6 after 10 steps, so sigma1 = 36.85. Rank 1 grid cell in row 4, column 2 is 10.43 (rank1[3, 1] in Python); it may leave the 0 to 9 range. Deflation then gives sigma2 = 15.07 and sigma3 = 4.89, and the errors 15.40, 4.54 and 6.73 in both tools.'),
                   ('Step 6: LoRA', '16,000 against 1,000,000, which is 1.6 percent. Rank of B A is 3 for the small demonstration in Python.')],
        rescue=['If the concepts overrun, go from the SVD formula slide straight to the images, and treat the low-rank storage slide as reading.', 'If only 30 minutes of lab remain, do steps 1, 4 and 6 and leave steps 2, 3 and 5 for practice.',
                'If array formulas cause trouble in the sheet, do sheet Small entry by entry with SUMPRODUCT.'],
        after=['Share the solution notebook after class.', 'Ask learners to bring one question about derivatives for Session 7.', 'Mention that Sessions 1 to 6 close the linear algebra block, and that LoRA\'s B and A are trained by the gradient methods that start in Session 7.'],
        lab_answer_key=[['PREDICT, step 1: the singular values of A?', '3 and 2.'], ['READ, step 2: how many large singular values does the noisy image have?', 'Two, then a flat tail.'],
                        ['READ, step 3: which rank has the smallest error from the clean image?', 'Rank 2. Rank 3 is worse because it copies noise.'], ['READ, step 4: what share of the variance is on component 1?', 'About 98.1 percent (102 out of 104).'],
                        ['CHANGE, step 4: flip physics to 100 minus physics', 'The first component becomes (0.8, -0.6) up to sign. The explained variance is still 0.981.'], ['CHANGE, step 5: deflate M and repeat the power iteration', 'sigma2 = 15.07 and the rank 2 error is 4.54. The given third round gives sigma3 = 4.89 and the rank 3 error 6.73.'], ['READ, step 6: what fraction of the numbers does LoRA train?', '1.6 percent for d = 1,000 and r = 8.']])
    return s
