"""Session 3 spreadsheet lab: the same numbers as the notebook."""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'kit'))
sys.path.insert(0, str(HERE.parent))
import xl as XL  # noqa: E402
import s03  # noqa: E402


def block(x, ws, top, left, M):
    """Write a numeric matrix of given values with borders; returns nothing."""
    from openpyxl.utils import get_column_letter
    for i, row in enumerate(M):
        for j, v in enumerate(row):
            x.formula(ws, f'{get_column_letter(left + j)}{top + i}', float(v) if not float(v).is_integer() else int(v))


def build(solution):
    x = XL.XL('Session 3: Matrices', 'Shape, matrix products, a moved shape, a layer y = W x + b and a count of parameters', solution=solution)
    x.start('Compute in cells the numbers from the slides: the shape and the transpose, A x, A B, a shape moved by a matrix, one layer y = W x + b, two layers in a row, and the number of parameters. The numbers are the same as in the Python notebook.',
            ['Open the sheet Products. Gold cells are yours. Predict first, then type the formula.',
             'A matrix answer fills a whole gold range. Excel: select the whole range, type the formula and press Ctrl+Shift+Enter (Cmd+Return on a Mac). Google Sheets: type the formula in the first gold cell and press Enter; MMULT and TRANSPOSE fill the range. If only one cell fills, press Ctrl+Shift+Enter instead, which wraps the formula in ARRAYFORMULA.',
             'Open the sheet Layers and do the same for the layer and the parameters.', 'Open the sheet Check. Every line must say OK.',
             'The weights are illustrative (made-up numbers to show the arithmetic).'])
    ws = x.sheet('Products', {'A': 46, 'B': 9, 'C': 9, 'D': 9, 'E': 9, 'F': 9, 'G': 9, 'H': 40})
    x.band(ws, 1, 'Products by hand and by formula', 8)
    x.text(ws, 'A3', 'Step 1. Shape, one entry and transpose', bold=True)
    x.text(ws, 'A4', 'The learner table L (age, hours, score)')
    block(x, ws, 4, 2, s03.L)
    x.text(ws, 'A7', 'Number of rows of L', bold=True); x.input(ws, 'B7', answer='=ROWS(B4:D6)')
    x.text(ws, 'A8', 'Entry in row 2, column 3', bold=True); x.input(ws, 'B8', answer='=INDEX(B4:D6,2,3)')
    x.text(ws, 'H8', 'CHANGE: ask for row 3, column 1. Predict first.', italic=True, color='666666')
    x.text(ws, 'A9', 'A (2 by 3)')
    block(x, ws, 9, 2, s03.A)
    x.text(ws, 'A12', 'Transpose of A, 3 by 2  (gold range B12:C14)', bold=True); x.array(ws, 'B12:C14', '=TRANSPOSE(B9:D10)', gold=True)
    x.text(ws, 'A16', 'Step 2. Matrix times vector', bold=True)
    x.text(ws, 'A17', 'x (as a column)'); block(x, ws, 17, 2, [[1], [2], [3]])
    x.text(ws, 'A21', 'A x, 2 entries  (gold range B21:B22)', bold=True); x.array(ws, 'B21:B22', '=MMULT(B9:D10,B17:B19)', gold=True)
    x.text(ws, 'D16', 'I (identity)', bold=True); block(x, ws, 17, 4, [[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    x.text(ws, 'G16', 'I x', bold=True); x.array(ws, 'G17:G19', '=MMULT(D17:F19,B17:B19)')
    x.text(ws, 'H17', 'READ: D17:F19 is the identity I, and G17:G19 is I x (given). Is it equal to x?', italic=True, color='666666', wrap=True)
    ws.row_dimensions[17].height = 30
    x.text(ws, 'A24', 'Step 3. Matrix times matrix', bold=True)
    x.text(ws, 'A25', 'B (3 by 2)'); block(x, ws, 25, 2, s03.B)
    x.text(ws, 'A29', 'A B, 2 by 2  (gold range B29:C30)', bold=True); x.array(ws, 'B29:C30', '=MMULT(B9:D10,B25:C27)', gold=True)
    x.text(ws, 'A32', 'Multiplications needed for A B  (m times n times p)', bold=True); x.input(ws, 'B32', answer='=2*3*2')
    x.text(ws, 'H29', 'CHANGE: try =MMULT(B25:C27,B9:D10) over a 3 by 3 range to see B A.', italic=True, color='666666', wrap=True)
    x.text(ws, 'A34', 'Step 4. Move the corners of the L-shaped drawing', bold=True)
    x.text(ws, 'A35', 'P: row 1 is x, row 2 is y, one corner per column'); block(x, ws, 35, 2, [row for row in [[0, 2, 2, 1, 1, 0], [0, 0, 1, 1, 3, 3]]])
    x.text(ws, 'A37', 'Shear matrix M'); block(x, ws, 37, 2, s03.SHEAR)
    x.text(ws, 'A40', 'M P, 2 by 6  (gold range B40:G41)', bold=True); x.array(ws, 'B40:G41', '=MMULT(B37:C38,B35:G36)', gold=True)
    x.text(ws, 'A43', 'Rotation matrix R'); block(x, ws, 43, 2, s03.ROT)
    x.text(ws, 'A46', 'R P, 2 by 6  (gold range B46:G47)', bold=True); x.array(ws, 'B46:G47', '=MMULT(B43:C44,B35:G36)', gold=True)
    x.text(ws, 'H46', 'READ: the corner (1, 3) is column 5. Where does each matrix send it? Compare with the pictures on the slides.', italic=True, color='666666', wrap=True)
    ws.row_dimensions[46].height = 45

    ly = x.sheet('Layers', {'A': 46, 'B': 9, 'C': 9, 'D': 9, 'E': 9, 'F': 40})
    x.band(ly, 1, 'One layer, two layers and parameters', 6)
    x.text(ly, 'A3', 'Step 5. One layer y = W x + b', bold=True)
    x.text(ly, 'A4', 'W1 (4 by 3)'); block(x, ly, 4, 2, s03.W1)
    x.text(ly, 'A8', 'x (as a column)'); block(x, ly, 8, 2, [[1], [2], [3]])
    x.text(ly, 'A12', 'b1 (as a column)'); block(x, ly, 12, 2, [[v] for v in s03.B1])
    x.text(ly, 'B16', 'W1 x', bold=True); x.text(ly, 'C16', 'y1', bold=True)
    x.text(ly, 'A17', 'W1 x in B17:B20 (MMULT), then y1 = W1 x + b1 in C17:C20 (one cell each)', bold=True, wrap=True); x.array(ly, 'B17:B20', '=MMULT(B4:D7,B8:B10)', gold=True)
    for i in range(4):
        x.input(ly, f'C{17 + i}', answer=f'=B{17 + i}+B{12 + i}')
    ly.row_dimensions[17].height = 30
    x.text(ly, 'F17', 'CHANGE: set the first bias to 2.5. Which entries of y1 move? Set it back to 0.5.', italic=True, color='666666', wrap=True)
    x.text(ly, 'A22', 'Step 6. Two layers in a row', bold=True)
    x.text(ly, 'A23', 'W2 (2 by 4)'); block(x, ly, 23, 2, s03.W2)
    x.text(ly, 'A26', 'b2 (as a column)'); block(x, ly, 26, 2, [[v] for v in s03.B2])
    x.text(ly, 'B28', 'W2 y1', bold=True); x.text(ly, 'C28', 'output', bold=True)
    x.text(ly, 'A29', 'W2 y1 in B29:B30 (MMULT), then the output W2 y1 + b2 in C29:C30', bold=True, wrap=True); x.array(ly, 'B29:B30', '=MMULT(B23:E24,C17:C20)', gold=True)
    for i in range(2):
        x.input(ly, f'C{29 + i}', answer=f'=B{29 + i}+B{26 + i}')
    ly.row_dimensions[29].height = 30
    x.text(ly, 'A32', 'W2 W1, 2 by 3  (gold range B32:D33)', bold=True); x.array(ly, 'B32:D33', '=MMULT(B23:E24,B4:D7)', gold=True)
    x.text(ly, 'A35', 'W2 W1 x, 2 entries  (gold range B35:B36)', bold=True); x.array(ly, 'B35:B36', '=MMULT(B32:D33,B8:B10)', gold=True)
    x.text(ly, 'A38', 'Step 7. Parameters', bold=True)
    x.text(ly, 'A39', 'Parameters of the toy network  (weights plus biases of both layers)', bold=True); x.input(ly, 'B39', answer='=ROWS(B4:D7)*COLUMNS(B4:D7)+ROWS(B12:B15)+ROWS(B23:E24)*COLUMNS(B23:E24)+ROWS(B26:B27)')
    x.text(ly, 'A40', 'Parameters of a 1,000 by 1,000 layer  (m times n plus m)', bold=True); x.input(ly, 'B40', answer='=1000*1000+1000')
    x.text(ly, 'A41', 'Gigabytes for 7 billion numbers at 2 bytes each', bold=True); x.input(ly, 'B41', answer='=7000000000*2/1000000000')
    x.text(ly, 'A43', 'Step 6, READ. A batch: two inputs, one per row of X (2 by 3)', bold=True); block(x, ly, 44, 2, [[1, 2, 3], [0, 1, 1]])
    x.text(ly, 'A47', 'X W1ᵀ, 2 by 4 (given): row 1 is W1 x from Step 5', bold=True); x.array(ly, 'B47:E48', '=MMULT(B44:D45,TRANSPOSE(B4:D7))')
    x.text(ly, 'F47', 'READ: W1 is 4 by 3 (outputs by inputs). With one input per row, the layer uses W1 transposed. Why?', italic=True, color='666666', wrap=True)
    ly.row_dimensions[47].height = 45
    x.text(ly, 'F40', 'CHANGE: make the hidden layer 5 numbers wide. Count the parameters by hand and with a formula.', italic=True, color='666666', wrap=True)

    x.check('Step 1a: rows of L = 3', '=Products!B7', 3); x.check('Step 1b: entry in row 2, column 3 = 58', '=Products!B8', 58)
    x.check('Step 1c: transpose of A, row 3, column 1 = 3', '=Products!B14', 3); x.check('Step 1d: transpose of A, row 1, column 2 = 4', '=Products!C12', 4)
    x.check('Step 2: A x = (14, 32), first entry', '=Products!B21', 14); x.check('Step 2: A x, second entry', '=Products!B22', 32)
    x.check('Step 3a: A B, row 1 column 2 = 64', '=Products!C29', 64); x.check('Step 3b: A B, row 2 column 1 = 139', '=Products!B30', 139)
    x.check('Step 3c: multiplications = 12', '=Products!B32', 12)
    x.check('Step 4a: shear sends the corner (1, 3) to x = 4', '=Products!F40', 4); x.check('Step 4b: and y = 3', '=Products!F41', 3)
    x.check('Step 4c: rotation sends it to x = -3', '=Products!F46', -3); x.check('Step 4d: and y = 1', '=Products!F47', 1)
    x.check('Step 5: W1 x = (7, -1, 4, 4), first entry', '=Layers!B17', 7)
    x.check('Step 5: y1 = (7.5, -1, 3, 4.5), first entry', '=Layers!C17', 7.5); x.check('Step 5: y1, third entry', '=Layers!C19', 3); x.check('Step 5: y1, fourth entry', '=Layers!C20', 4.5)
    x.check('Step 6a: layer 2 output, first entry = 10.5', '=Layers!C29', 10.5); x.check('Step 6b: layer 2 output, second entry = 9', '=Layers!C30', 9)
    x.check('Step 6c: W2 W1, row 1 column 1 = 3', '=Layers!B32', 3); x.check('Step 6d: W2 W1 x = (11, 7), first entry', '=Layers!B35', 11)
    x.check('Step 7a: toy parameters = 26', '=Layers!B39', 26); x.check('Step 7b: 1,001,000', '=Layers!B40', 1001000); x.check('Step 7c: 14 gigabytes', '=Layers!B41', 14)
    return x
