"""Session 3 lab notebook: matrices, products, a shape moved by a matrix, a layer y = Wx + b and a count of parameters."""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'kit'))
sys.path.insert(0, str(HERE.parent))
import nb as NB  # noqa: E402
import s03  # noqa: E402

TITLE = 'Matrices'


def build(solution):
    F = s03.facts()
    n = NB.Notebook()

    def todo(code, hint):
        n.code(code if solution else f'answer = None  # your code here: {hint}')

    n.md('# Session 3 lab: matrices\n\n**Mathematics for AI and Machine Learning** | KLAi Professional Learning\n\n'
         'Today you compute, in Python, the numbers from the slides: the shape of a matrix, matrix times vector, matrix times matrix, the transpose, a shape moved by a matrix, one layer y = W x + b, two layers in a row, and a count of parameters.\n\n'
         '**How to use this notebook**\n\n1. Run the cells in order from the top (Shift and Enter).\n2. Every step: **PREDICT**, run, **READ**, then **CHANGE** one thing.\n'
         '3. Cells with `answer = None` are yours. Replace `None` with your code, then run the check under it.\n4. The weights and the token numbers are illustrative (made-up numbers to show the arithmetic).\n'
         '5. In numpy, `*` multiplies entry by entry and `@` is the matrix product.\n6. A vector is a column in matrix work; numpy prints it across the page to save space.')
    n.check_setup()
    n.step(0, 'Load the tools and the matrices', 'The learner table from Session 2 (age, hours, score), and two small matrices A (2 by 3) and B (3 by 2).')
    n.code('import numpy as np\nimport pandas as pd\nimport matplotlib.pyplot as plt\n\n'
           'L = np.array([[21, 6, 72],\n              [25, 3, 58],\n              [19, 8, 85]])      # one learner per row: age, hours, score\n'
           'A = np.array([[1, 2, 3],\n              [4, 5, 6]])        # 2 rows, 3 columns\n'
           'B = np.array([[7, 8],\n              [9, 10],\n              [11, 12]])         # 3 rows, 2 columns\n'
           'x = np.array([1, 2, 3])\n'
           'pd.DataFrame(L, index=["Amina", "Brian", "Chloe"], columns=["age", "hours", "score"])')
    n.step(1, 'Shape, one entry and the transpose', 'A.shape gives (rows, columns). Python counts from 0.')
    n.predict('What is the shape of L? What is the shape of A.T (the transpose of A)? Which index gives the score of Brian?')
    todo('answer = [L.shape[0], L.shape[1], L[1, 2]]', 'a list of three values: [rows, columns, the entry in row 2 and column 3]')
    n.code('check("Step 1a: L is 3 by 3 and the entry in row 2, column 3 is 58", answer, [3, 3, 58])\nif answer is not None:\n    print("rows, columns, entry:", answer)')
    todo('answer = list(A.T.shape)', 'the shape of the transpose of A, as a list [rows, columns]')
    n.code('check("Step 1b: the transpose of A is 3 by 2", answer, [3, 2])\nif answer is not None:\n    print("shape of A transposed:", answer)')
    n.change('Print L[2, 3]. Read the error. Why does it happen? Then print L[2, 0].')
    n.step(2, 'Matrix times vector', 'Each entry of A x is the dot product of one row of A with x = (1, 2, 3).')
    n.predict('What is the shape of A x? What are its entries?')
    todo('answer = A @ x', 'the matrix times the vector')
    n.code('y = answer\ncheck("Step 2: A x = (14, 32)", y, [14, 32])\nif y is not None:\n    print("A x =", y)')
    n.read('Check row 1 by hand: 1 × 1 + 2 × 2 + 3 × 3. Does it give 14?')
    n.predict('The identity matrix I has 1s on the diagonal and 0s elsewhere. What will I x give for x = (1, 2, 3)?')
    n.code('I = np.eye(3)      # the 3 by 3 identity matrix\nprint(I)\nprint("I x =", I @ x)')
    n.read('Each row of I picks one entry of x. Why is I x always equal to x?')
    n.step(3, 'Matrix times matrix, and the order', 'A B takes dot products of rows of A with columns of B.')
    n.predict('What is the shape of A B? What is the shape of B A?')
    todo('answer = A @ B', 'the product of A and B, in the right order')
    n.code('AB = answer\ncheck("Step 3a: A B = rows (58, 64) and (139, 154)", AB, [[58, 64], [139, 154]])\nif AB is not None:\n    print(AB)')
    todo('answer = list((B @ A).shape)', 'the shape of the product B A, as a list [rows, columns]')
    n.code('check("Step 3b: B A is 3 by 3", answer, [3, 3])\nif answer is not None:\n    print("shape of B A:", answer)')
    n.change('Run A @ A and read the error. Then run A * B and read that error too. Which sign is the matrix product?')
    n.step(4, 'Move a shape with a matrix', 'The L-shaped drawing has 6 corners, one per column of P. A matrix times P moves every corner at once.')
    n.code('P = np.array([[0, 2, 2, 1, 1, 0],\n              [0, 0, 1, 1, 3, 3]])      # row 1: x values, row 2: y values\n'
           'shear = np.array([[1, 1],\n                  [0, 1]])\nrot = np.array([[0, -1],\n                [1, 0]])')
    n.predict('Where does the corner (1, 3) go under the shear? Under the rotation by 90 degrees?')
    todo('answer = shear @ P', 'move all six corners at once')
    n.code('moved = answer\ncheck("Step 4a: the shear sends the corner (1, 3) to (4, 3)", None if moved is None else moved[:, 4], [4, 3])\nif moved is not None:\n    print(moved)')
    todo('answer = (rot @ P)[:, 4]', 'the rotation matrix times P, then only the column of the corner (1, 3)')
    n.code('check("Step 4b: the rotation sends the corner (1, 3) to (-3, 1)", answer, [-3, 1])\nif answer is not None:\n    print("rotated corner:", answer)')
    n.code('if moved is not None:\n    fig, ax = plt.subplots(figsize=(4.5, 3.2))\n    for M, col, name in ((P, "grey", "original"), (moved, "goldenrod", "sheared")):\n'
           '        ax.fill(M[0], M[1], color=col, alpha=0.5, label=name)\n    ax.set_aspect("equal"); ax.legend(); ax.set_xlabel("x"); ax.set_ylabel("y")\n    plt.show()')
    n.read('The shear slides each point sideways by an amount equal to its height y. Which corners did not move, and what do they have in common?')
    n.step(5, 'One layer: y = W x + b', 'W is 4 by 3 and x has 3 entries, so y has 4 entries. The numbers are illustrative.')
    n.code('W1 = np.array([[1, 0, 2],\n               [0, 1, -1],\n               [2, 1, 0],\n               [-1, 1, 1]])\nb1 = np.array([0.5, 0.0, -1.0, 0.5])')
    n.predict('What is the first entry of W x + b? Use row 1 of W and the first bias.')
    todo('answer = W1 @ x + b1', 'the layer rule from the slide')
    n.code('y1 = answer\ncheck("Step 5: y = (7.5, -1, 3, 4.5)", y1, [7.5, -1, 3, 4.5])\nif y1 is not None:\n    print("y =", y1)')
    n.change('In the cell that sets b1, change the first bias from 0.5 to 2.5 and run Step 5 again. Which entries of y move, and by how much? Then change it back to 0.5 and run Step 5 again.')
    n.step(6, 'Two layers in a row', 'Layer 2 has W2 (2 by 4) and b2. Without the biases, two layers equal one matrix W2 W1.')
    n.code('W2 = np.array([[1, 0, 1, 0],\n               [0, 1, 0, 2]])\nb2 = np.array([0.0, 1.0])')
    todo('answer = W2 @ y1 + b2', 'layer 2 applied to the output of layer 1')
    n.code('out = answer\ncheck("Step 6a: layer 2 gives (10.5, 9)", out, [10.5, 9])\nif out is not None:\n    print("output:", out)')
    n.predict('Leave out the biases. Will W2 times (W1 x) equal (W2 W1) times x?')
    todo('answer = (W2 @ W1) @ x', 'multiply the two weight matrices first, then apply the result to x')
    n.code('one = answer\ncheck("Step 6b: W2 W1 x = (11, 7)", one, [11, 7])\nif one is not None:\n    print("W2 W1 =\\n", W2 @ W1)\n    print("one matrix on x:", one, "  two layers in turn:", W2 @ (W1 @ x))')
    n.read('Both ways give the same answer. Why would a network with no nonlinear step between its layers be no more powerful than one layer?')
    n.code('# A batch: two inputs, one per ROW of X. W1 is stored outputs x inputs (4 x 3), so the batch uses W1 transposed.\n'
           'X = np.array([[1, 2, 3],\n              [0, 1, 1]])     # 2 inputs, 3 numbers each\nprint(X @ W1.T + b1)')
    n.read('Row 1 is the y from Step 5. Why does the batch need W1.T? Try X @ W1 and read the error.')
    n.step(7, 'Count the parameters', 'A layer with n inputs and m outputs has m × n weights and m biases.')
    n.predict('How many parameters does the toy network have? And one layer from 1,000 inputs to 1,000 outputs?')
    todo('answer = [W1.size + b1.size + W2.size + b2.size, 1000 * 1000 + 1000]', 'a list of two counts: all numbers of the toy network, then the numbers of the big layer')
    n.code('check("Step 7a: 26 and 1,001,000", answer, [26, 1001000])\nif answer is not None:\n    print("parameters:", answer)')
    todo('answer = 7e9 * 2 / 1e9', 'seven billion numbers, 2 bytes each, in gigabytes (1 gigabyte = 1e9 bytes)')
    n.code('gb = answer\ncheck("Step 7b: 14 gigabytes", gb, 14)\nif gb is not None:\n    print("7 billion numbers at 2 bytes each:", gb, "gigabytes")')
    n.change('Make the hidden layer 5 numbers wide instead of 4: count (5 × 3 + 5) + (2 × 5 + 2) by hand. Does it give 32?')
    n.md('---\n## Finish\n\nRun the last cell. Every line must say OK. Then restart the session, run all cells in order and save.')
    n.code('show_checks()')
    return n
