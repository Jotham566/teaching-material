"""Session 2 lab notebook: vectors, dot product, norm, distance, cosine similarity and a tiny document search."""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'kit'))
sys.path.insert(0, str(HERE.parent))
import nb as NB  # noqa: E402
import s02  # noqa: E402

TITLE = 'Vectors'


def build(solution):
    F = s02.facts()
    n = NB.Notebook()

    def todo(code, hint):
        n.code(code if solution else f'answer = None  # your code here: {hint}')

    n.md('# Session 2 lab: vectors\n\n**Mathematics for AI and Machine Learning** | KLAi Professional Learning\n\n'
         'Today you compute, in Python, the numbers from the slides: add and scale vectors, the dot product, the L2 norm, the Euclidean distance and the cosine similarity. Then you rank six short sentences against a query, a tiny version of document search.\n\n'
         '**How to use this notebook**\n\n1. Run the cells in order from the top (Shift and Enter).\n2. Every step: **PREDICT**, run, **READ**, then **CHANGE** one thing.\n'
         '3. Cells with `answer = None` are yours. Replace `None` with your code, then run the check under it.\n4. The embedding numbers are illustrative (made-up numbers to show the arithmetic).\n'
         '5. In numpy, `*` multiplies entry by entry and `@` is the dot product.')
    n.check_setup()
    n.step(0, 'Load the tools and the data', 'Six short sentences, each with a 4 number embedding (illustrative), and a query.')
    n.code('import numpy as np\nimport pandas as pd\nimport matplotlib.pyplot as plt\n\n'
           'sentences = ["How do I reset my password?", "Steps to change your login password", "Office opening hours on Saturday",\n             "Refund policy for cancelled orders", "How to request a refund", "Our team picnic is on Friday"]\n'
           'E = np.array([[0.9, 0.1, 0.0, 0.1],\n              [0.8, 0.2, 0.1, 0.0],\n              [0.0, 0.1, 0.9, 0.2],\n              [0.1, 0.9, 0.2, 0.0],\n              [0.2, 0.8, 0.1, 0.1],\n              [0.0, 0.1, 0.5, 0.8]])   # one row per sentence: 6 rows, d = 4\n'
           'q = np.array([0.85, 0.15, 0.05, 0.05])          # the query "I forgot my password"\n'
           'pd.DataFrame(E, index=sentences, columns=["d1", "d2", "d3", "d4"])')
    n.step(1, 'Add and scale vectors', 'a = (3, 4) and b = (4, 3).')
    n.code('a = np.array([3, 4])\nb = np.array([4, 3])')
    n.predict('What is a + b?')
    todo('answer = a + b', 'add the two vectors')
    n.code('s = answer\nprint("a + b =", s, "   2a =", 2 * a)\ncheck("Step 1: a + b = (7, 7)", s, [7, 7])')
    n.change('Change b to np.array([1, 2, 3]) and run a + b. Read the error. Why does it happen? Then restore b.')
    n.step(2, 'The dot product and the L2 norm', 'u = (1, 2, 2) and v = (2, 0, 1).')
    n.code('u = np.array([1, 2, 2])\nv = np.array([2, 0, 1])')
    n.predict('What is the dot product of u and v? What is the length of u?')
    todo('answer = np.sum(u * v)', 'multiply the matching entries of u and v, then add the products')
    n.code('dot = answer\nprint("u . v =", dot)\ncheck("Step 2a: u . v = 4", dot, 4)')
    todo('answer = np.sqrt(np.sum(a * a))', 'the L2 norm of a, from the formula on the slide')
    n.code('norm_a = answer\nprint("norm of a =", norm_a, "   norm of u =", np.sqrt(u @ u))\ncheck("Step 2b: the L2 norm of a = (3, 4) is 5", norm_a, 5)')
    n.read('Does np.linalg.norm(a) give the same number? Why is the norm of u exactly 3?')
    n.step(3, 'Euclidean distance', 'P = (1, 1) and R = (4, 5). Subtract, then take the norm of the difference.')
    n.code('point_P = np.array([1, 1])\npoint_R = np.array([4, 5])')
    todo('answer = np.sqrt(np.sum((point_R - point_P) ** 2))', 'the norm of the difference between the two points')
    n.code('dist = answer\nprint("distance =", dist)\ncheck("Step 3: the distance from p to q is 5", dist, 5)')
    n.change('Change point_R to np.array([7, 9]). Predict the distance first. Then restore it to (4, 5).')
    n.step(4, 'Cosine similarity and the angle', 'cos = (a . b) / (norm a * norm b), then arccos gives the angle.')
    n.predict('Is the cosine of a and b close to 1 or close to 0? Look at the picture on the slide.')
    todo('answer = (a @ b) / (np.linalg.norm(a) * np.linalg.norm(b))', 'the formula from the slide: dot product over the two lengths')
    n.code('cos_ab = answer\nprint("cosine similarity =", round(float(cos_ab), 4))\ncheck("Step 4a: cosine similarity of a and b = 0.96", cos_ab, 0.96, 0.001)')
    todo('answer = np.degrees(np.arccos(cos_ab))', 'the angle whose cosine is cos_ab, in degrees (computers work in radians first)')
    n.code('angle = answer\nprint("angle =", round(float(angle), 2), "degrees")\ncheck("Step 4b: the angle is 16.26 degrees", angle, 16.26, 0.01)')
    n.step(5, 'Search: cosine similarity of the query with every sentence', 'E has one sentence per row. You need the dot product of every row with q, then divide by the length of that row and by the length of q.')
    n.predict('Which two sentences will score highest?')
    todo('answer = (E @ q) / (np.linalg.norm(E, axis=1) * np.linalg.norm(q))', 'all six dot products with q, then the two divisions')
    n.code('sims = np.asarray(answer)\nresult = pd.DataFrame({"sentence": sentences, "cosine": sims.round(3)}).sort_values("cosine", ascending=False)\nprint(result.to_string(index=False))\n'
           'check("Step 5: the six cosine similarities", sims, [0.9949, 0.9939, 0.0872, 0.2864, 0.4140, 0.0974], 0.001)')
    n.read('Which sentence is the best match? Do the two refund sentences also score close to each other?')
    n.step(6, 'Pick the best match', 'Find the position of the largest cosine in sims.')
    todo('answer = int(np.argmax(sims))', 'the position (0 to 5) of the largest cosine')
    n.code('best = answer\nprint("best match:", sentences[best] if best is not None else None)\ncheck("Step 6: the best match is sentence 1 (position 0)", best, 0)')
    n.step(7, 'Why not the raw dot product?', 'We stretch the picnic sentence (row 5) to 20 times its length. The direction does not change.')
    n.code('factor = 20\nE2 = E.copy()\nE2[5] = factor * E2[5]                  # a longer picnic vector\ndots = E2 @ q\nsims2 = dots / (np.linalg.norm(E2, axis=1) * np.linalg.norm(q))')
    n.predict('What is the dot product of the stretched picnic vector with q? Compare it with 0.785 for sentence 1.')
    todo('answer = E2[5] @ q', 'the dot product of row 5 of E2 with q')
    n.code('picnic_dot = answer\nprint('"'"'picnic dot product:'"'"', round(float(picnic_dot), 3))\ncheck("Step 7a: the stretched picnic dot product = 1.6", picnic_dot, 1.6, 0.001)')
    todo('answer = sims2[5]', 'the cosine of the stretched picnic vector with q: it is already in sims2')
    n.code('picnic_cos = answer\nprint('"'"'picnic cosine:'"'"', round(float(picnic_cos), 4))\ncheck("Step 7b: the picnic cosine is unchanged = 0.0974", picnic_cos, 0.0974, 0.001)\n'
           'print("sentence with the biggest dot product:", sentences[int(np.argmax(dots))])\nprint("sentence with the biggest cosine:", sentences[int(np.argmax(sims2))])')
    n.read('The picnic sentence has nothing to do with passwords. Why does it win by dot product and not by cosine?')
    n.change('Change factor to 2, run the Step 7 cells again, and watch picnic_dot. Does the picnic sentence still win by dot product? Then set factor back to 20 and run them again so the checks pass.')
    n.md('---\n## Finish\n\nRun the last cell. Every line must say OK. Then restart the session, run all cells in order and save.')
    n.code('show_checks()')
    return n
