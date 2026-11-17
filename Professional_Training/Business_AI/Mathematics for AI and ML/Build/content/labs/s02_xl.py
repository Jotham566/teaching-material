"""Session 2 spreadsheet lab: the same numbers as the notebook."""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'kit'))
sys.path.insert(0, str(HERE.parent))
import xl as XL  # noqa: E402
import s02  # noqa: E402


def build(solution):
    x = XL.XL('Session 2: Vectors', 'Dot product, norm, distance, cosine similarity and a tiny search', solution=solution)
    x.start('Compute in cells the numbers from the slides: add and scale vectors, the dot product, the L2 norm, the distance and the cosine similarity. Then rank six sentences against a query. The numbers are the same as in the Python notebook.',
            ['Open the sheet Hand. Gold cells are yours.', 'Predict first, then type the formula in the gold cell.', 'Open the sheet Search and fill the gold cells for the six sentences.', 'Open the sheet Check. Every line must say OK.',
             'Embedding numbers are illustrative (made-up numbers to show the arithmetic).'])
    ws = x.sheet('Hand', {'A': 44, 'B': 12, 'C': 12, 'D': 12, 'E': 44})
    x.band(ws, 1, 'Hand calculations (the same as the slides)', 5)
    x.text(ws, 'A3', 'Step 1. Add vectors', bold=True)
    x.text(ws, 'A4', 'a'); x.formula(ws, 'B4', 3); x.formula(ws, 'C4', 4)
    x.text(ws, 'A5', 'b'); x.formula(ws, 'B5', 4); x.formula(ws, 'C5', 3)
    x.text(ws, 'A6', 'a + b (one formula per entry)', bold=True); x.input(ws, 'B6', answer='=B4+B5'); x.input(ws, 'C6', answer='=C4+C5')
    x.text(ws, 'E6', 'CHANGE: set a to 1 and 2 in row 4. Predict rows 6 and 7, then set a back to 3 and 4.', italic=True, color='666666')
    x.text(ws, 'A7', '2a (given)'); x.formula(ws, 'B7', '=2*B4'); x.formula(ws, 'C7', '=2*C4')
    x.text(ws, 'A9', 'Step 2. Dot product and norm', bold=True)
    x.text(ws, 'A10', 'u'); [x.formula(ws, f'{c}10', v) for c, v in zip('BCD', (1, 2, 2))]
    x.text(ws, 'A11', 'v'); [x.formula(ws, f'{c}11', v) for c, v in zip('BCD', (2, 0, 1))]
    x.text(ws, 'A12', 'u . v', bold=True); x.input(ws, 'B12', answer='=SUMPRODUCT(B10:D10,B11:D11)')
    x.text(ws, 'A13', 'Norm of a (L2 norm)', bold=True); x.input(ws, 'B13', answer='=SQRT(SUMPRODUCT(B4:C4,B4:C4))')
    x.text(ws, 'A14', 'Norm of u'); x.formula(ws, 'B14', '=SQRT(SUMPRODUCT(B10:D10,B10:D10))')
    x.text(ws, 'A16', 'Step 3. Euclidean distance', bold=True)
    x.text(ws, 'A17', 'P'); x.formula(ws, 'B17', 1); x.formula(ws, 'C17', 1)
    x.text(ws, 'A18', 'R'); x.formula(ws, 'B18', 4); x.formula(ws, 'C18', 5)
    x.text(ws, 'A19', 'Distance from P to R', bold=True); x.input(ws, 'B19', answer='=SQRT(SUMXMY2(B17:C17,B18:C18))')
    x.text(ws, 'E19', 'CHANGE: set R to 7 and 9. Predict first, then set it back to 4 and 5.', italic=True, color='666666')
    x.text(ws, 'A21', 'Step 4. Cosine similarity and the angle', bold=True)
    x.text(ws, 'A22', 'Norm of b'); x.formula(ws, 'B22', '=SQRT(SUMPRODUCT(B5:C5,B5:C5))')
    x.text(ws, 'A23', 'Cosine similarity of a and b', bold=True); x.input(ws, 'B23', answer='=SUMPRODUCT(B4:C4,B5:C5)/(B13*B22)')
    x.text(ws, 'A24', 'Angle in degrees', bold=True); x.input(ws, 'B24', answer='=DEGREES(ACOS(B23))')
    x.text(ws, 'E24', 'Hint: ACOS gives the angle in radians; DEGREES converts it.', italic=True, color='666666')
    sh = x.sheet('Search', {'A': 40, 'B': 8, 'C': 8, 'D': 8, 'E': 8, 'F': 14, 'G': 14, 'H': 14})
    x.band(ws if False else sh, 1, 'Step 5 and 6. Rank six sentences against the query', 8)
    for c, h in zip('ABCDEFGH', ('Sentence', 'd1', 'd2', 'd3', 'd4', 'Dot with query', 'Norm', 'Cosine')):
        x.text(sh, f'{c}3', h, bold=True, border=True)
    for i, (t_, row) in enumerate(zip(s02.SENTENCES, s02.E)):
        r = 4 + i
        x.text(sh, f'A{r}', t_, border=True)
        for c, v in zip('BCDE', row):
            x.formula(sh, f'{c}{r}', float(v))
        x.input(sh, f'F{r}', answer=f'=SUMPRODUCT(B{r}:E{r},$B$11:$E$11)')
        x.formula(sh, f'G{r}', f'=SQRT(SUMPRODUCT(B{r}:E{r},B{r}:E{r}))')
        x.input(sh, f'H{r}', answer=f'=F{r}/(G{r}*$G$11)')
    x.text(sh, 'A11', 'Query: I forgot my password', bold=True, border=True)
    for c, v in zip('BCDE', s02.Q):
        x.formula(sh, f'{c}11', float(v))
    x.formula(sh, 'G11', '=SQRT(SUMPRODUCT(B11:E11,B11:E11))')
    x.text(sh, 'A12', 'Hint for B13: =INDEX(A4:A9, MATCH(MAX(H4:H9), H4:H9, 0)). MAX finds the largest cosine, MATCH its row, INDEX the sentence.', italic=True, color='666666')
    x.text(sh, 'A13', 'Best match (the sentence with the largest cosine)', bold=True)
    x.input(sh, 'B13', answer='=INDEX(A4:A9,MATCH(MAX(H4:H9),H4:H9,0))')
    x.text(sh, 'A15', 'Step 7. Stretch the picnic sentence: row 16 is row 9 multiplied by the factor in B14 (20). Compare the dot product with the cosine.', italic=True, color='666666', wrap=True)
    x.text(sh, 'A14', 'Factor for Step 7'); x.formula(sh, 'B14', 20)
    x.text(sh, 'A16', 'Picnic row times the factor'); [x.formula(sh, f'{c}16', f'=$B$14*{c}9') for c in 'BCDE']
    x.text(sh, 'A17', 'Dot with query'); x.input(sh, 'F17', answer='=SUMPRODUCT(B16:E16,$B$11:$E$11)')
    x.text(sh, 'A18', 'Cosine'); x.input(sh, 'F18', answer='=F17/(SQRT(SUMPRODUCT(B16:E16,B16:E16))*$G$11)')
    x.text(sh, 'A19', 'READ: compare F17 with the dot product of sentence 1 in F4. Then compare F18 with H9. CHANGE: set B14 to 2, then back to 20.', italic=True, color='666666')
    x.check('Step 1: a + b, first entry = 7', '=Hand!B6', 7); x.check('Step 1: a + b, second entry = 7', '=Hand!C6', 7)
    x.check('Step 2a: u . v = 4', '=Hand!B12', 4); x.check('Step 2b: the norm of a = 5', '=Hand!B13', 5)
    x.check('Step 3: the distance from P to R = 5', '=Hand!B19', 5)
    x.check('Step 4a: cosine similarity of a and b = 0.96', '=Hand!B23', 0.96, 0.001); x.check('Step 4b: the angle = 16.26 degrees', '=Hand!B24', 16.26, 0.01)
    x.check('Step 5: the dot product of sentence 1 with the query = 0.785', '=Search!F4', 0.785, 0.001)
    x.check('Step 5: cosine of sentence 1 = 0.9949', '=Search!H4', 0.9949, 0.001); x.check('Step 5: cosine of sentence 5 = 0.414', '=Search!H8', 0.414, 0.001)
    x.check('Step 6: the best match', '=Search!B13', s02.SENTENCES[0])
    x.check('Step 7a: the stretched picnic dot product = 1.6', '=Search!F17', 1.6, 0.001)
    x.check('Step 7b: the picnic cosine is unchanged = 0.0974', '=Search!F18', 0.0974, 0.001)
    return x
