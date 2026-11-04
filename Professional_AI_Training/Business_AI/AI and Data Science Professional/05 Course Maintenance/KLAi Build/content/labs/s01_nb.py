"""Session 1 notebook: your first cells (print, a sum, a list, and a first look at orders.csv). Expected values come from the real data / the prices below."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'kit'))
sys.path.insert(0, str(HERE.parent))
import nb as NB  # noqa: E402
import b_facts as BF  # noqa: E402

TITLE = 'First notebook'
RICE, SUGAR = 4500, 2800


def build(solution: bool):
    B = BF.base()
    nb = NB.Notebook()
    nb.md('# Session 1: your first notebook\n\nA notebook is made of cells. A **text cell** holds words you read. A **code cell** holds Python: press the play button beside it to run it, and the output appears under it.\n\n'
          'For every task: **predict**, **run**, **read**, then **change one thing**. Run the cells from the top, one after the other.')
    nb.data_setup()
    nb.check_setup()

    nb.step(1, 'Print a sentence', 'A name (here `message`) holds a value. `print()` shows it under the cell.')
    nb.predict('You will store a sentence in `message` and print it. What will appear under the cell?')
    nb.code("# Put a sentence between quotes into message. Then run the cell.\n"
            + ("message = 'Hello from Lakeside Mart analytics'" if solution else "message = None   # your code here: a sentence between quotes")
            + "\nprint(message)")
    nb.code("check('message is a sentence', isinstance(message, str) and len(message) > 0, True)")
    nb.change('Change the words inside the quotes and run the two cells again.')

    nb.step(2, 'Add two numbers', f'A kilo of rice costs {RICE} UGX and a kilo of sugar costs {SUGAR} UGX (illustrative prices). Store the sum in `total`.')
    nb.predict('What is the total? Work it out in your head first.')
    nb.code("# Add the two prices and store the answer in total.\n"
            + ("total = 4500 + 2800" if solution else "total = None   # your code here: add 4500 and 2800")
            + "\nprint(total)")
    nb.code(f"check('total', total, {RICE + SUGAR}, tol=0)")
    nb.read('Python printed a number with no UGX. Where is the unit stored?')

    nb.step(3, 'Store a list', 'A list holds several items in order, inside square brackets, separated by commas.')
    nb.predict('How many items will `len(branches)` show for three branch names?')
    nb.code("# Write three branch names as text in quotes inside [ ]: Kampala Central, Jinja and Gulu.\n"
            + ("branches = ['Kampala Central', 'Jinja', 'Gulu']" if solution else "branches = None   # your code here: a list of three names in quotes")
            + "\nprint(branches)\nprint(len(branches) if branches else 0)")
    nb.code("check('three branches including Jinja', isinstance(branches, list) and len(branches) == 3 and 'Jinja' in branches, True)")

    nb.step(4, 'A first look at the full orders file', 'The setup cell put orders.csv next to this notebook. It is the full file the workbook was sampled from. We meet pandas properly in Session 7, so just run these lines.')
    nb.predict('The workbook has 2,000 orders. Will the full file have fewer, the same, or more records?')
    nb.code("import pandas as pd\norders = pd.read_csv('orders.csv')\n"
            + ("n_orders = len(orders)" if solution else "n_orders = None   # your code here: the number of records, len(orders)")
            + "\nprint(n_orders)")
    nb.code(f"check('records in orders.csv', n_orders, {B['full_n']}, tol=0)")
    nb.read('Why does orders.csv have more records than the workbook?')

    nb.md('## Step 5: save and reflect\n\nChoose **File, Save a copy in Drive**. Then double-click this text cell and write two things:\n\n'
          '1. One sentence on which CRISP-DM phase was hardest to picture, and why.\n2. One line each on what data science, machine learning and AI produce.\n\n> My notes: ')
    nb.code('show_checks()')
    return nb
