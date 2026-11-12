"""Session 1 lab notebook: sums, functions, logarithms and log-probabilities."""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'kit'))
sys.path.insert(0, str(HERE.parent))
import nb as NB  # noqa: E402
import s01  # noqa: E402

TITLE = 'Functions and logarithms'


def build(solution):
    F = s01.facts()
    n = NB.Notebook()

    def todo(code, hint):
        n.code(code if solution else f'answer = None  # your code here: {hint}')

    n.md('# Session 1 lab: functions, notation and logarithms\n\n**Mathematics for AI and Machine Learning** | KLAi Professional Learning\n\n'
         'Today you compute, in Python, the numbers from the slides: a sigma sum, a function, logarithms, and the log-probability of a word and of a sentence.\n\n'
         '**How to use this notebook**\n\n1. Run the cells in order from the top (Shift and Enter).\n2. Every step has the same rhythm: **PREDICT**, run, **READ**, then **CHANGE** one thing.\n'
         '3. Cells that say `answer = None` are yours to fill in. Replace `None` with your code. Then run the check cell under it.\n'
         '4. All numbers here are illustrative (made-up numbers to show the arithmetic).\n5. If you get an error, read the last line first.')
    n.check_setup()
    n.step(0, 'Load the tools and the table', 'numpy does maths on lists of numbers. The table has five candidate next words for the text "The capital of Uganda is", each with a probability (a number from 0 to 1).')
    n.code('import numpy as np\nimport pandas as pd\nimport matplotlib.pyplot as plt\n\n'
           'table = pd.DataFrame({"word": ["Kampala", "Entebbe", "a", "the", "Nairobi"],\n                      "p": [0.62, 0.18, 0.10, 0.06, 0.04]})\n'
           'p = table["p"].to_numpy()      # the probabilities as a numpy array\ntable')
    n.step(1, 'Sigma notation: add up the probabilities', 'The sigma sum of p from i = 1 to 5 means add all five numbers.')
    n.predict('What will the five probabilities add up to?')
    todo('answer = np.sum(p)', 'add up all five numbers in p')
    n.code('total = answer\ncheck("Step 1: the five probabilities add up to 1", total, 1.0)\nif total is not None:\n    print("sum of p:", round(float(total), 4))')
    n.read('Why must the total be exactly 1?')
    n.step(2, 'A function and its graph', 'The function f(x) = w x + b with w = 2 and b = 1 (b is the bias). You compute f(3), then draw the graph.')
    n.code('w = 2      # the weight (slope)\nb = 1      # the bias (intercept)\nx = 3      # the input')
    n.predict('What is f(3) when w = 2 and b = 1?')
    todo('answer = w * x + b', 'use w, x and b from the cell above')
    n.code('f3 = answer\ncheck("Step 2: f(3) = 7", f3, 7)\nif f3 is not None:\n    print("f(3) =", f3)\n\n'
           'xs = np.linspace(0, 5, 50)\nplt.plot(xs, w * xs + b)\nplt.plot([x], [w * x + b], "o")\nplt.xlabel("input x"); plt.ylabel("f(x)"); plt.title(f"f(x) = {w}x + {b}")\nplt.show()')
    n.change('In the cell with w = 2, change w to 3 and run the three cells of Step 2 again. What is f(3) now, and how does the line change? The check will say NOT YET while w = 3. Then set w back to 2 and run them again.')
    n.step(3, 'Exponentials and logarithms', 'np.exp(x) is e to the power x. np.log(x) is the natural logarithm ln x. They undo each other.')
    n.predict('Will ln 6 be larger or smaller than ln 2 + ln 3? Guess before you run.')
    todo('answer = np.log(6)', 'the natural logarithm of 6')
    n.code('ln6 = answer\ncheck("Step 3a: ln 6 = 1.7918", ln6, 1.7918, 0.001)\nif ln6 is not None:\n    print("ln 6        =", round(float(ln6), 4))')
    todo('answer = np.log(2) + np.log(3)', 'ln 2 and ln 3 added together')
    n.code('ln2_plus_ln3 = answer\ncheck("Step 3b: ln 2 + ln 3 = ln 6 (the product rule)", ln2_plus_ln3, 1.7918, 0.001)\nif ln2_plus_ln3 is not None:\n    print("ln 2 + ln 3 =", round(float(ln2_plus_ln3), 4))\n'
           'print("exp(ln 6)   =", round(float(np.exp(np.log(6))), 4), " (exp undoes ln)")')
    n.read('Are the two numbers equal? Which log rule is this?')
    n.change('Try np.log(2 + 3) and np.log(2) + np.log(3). Are they equal? What does this tell you about the log of a sum?')
    n.step(4, 'Negative log-probability of each candidate word', 'Minus ln p is positive when p is below 1, and it grows as p shrinks. Training uses it as the loss for the word that really came next.')
    n.predict('Which word will have the largest minus ln p, and which the smallest?')
    todo('answer = -np.log(p)', 'minus the natural log of every probability, all at once')
    n.code('neg_log_p = answer\ncheck("Step 4: minus ln p of the five words", neg_log_p, [0.478, 1.715, 2.303, 2.813, 3.219], 0.001)\n'
           'if neg_log_p is not None:\n    table["minus_ln_p"] = np.round(neg_log_p, 3)\n    print(table)\n    print("sum of minus ln p:", round(float(np.sum(neg_log_p)), 3))')
    n.change('In a new cell run p[0] = 0.9, then run the Step 4 cells again. What happens to the minus ln p of Kampala? The five numbers no longer add up to 1; that is fine for this experiment. Then run p[0] = 0.62 and Step 4 again to restore it.')
    n.step(5, 'Entropy: each p times its minus ln p, added up', 'Multiply each minus ln p by its own probability and add: the sum of p times (minus ln p). This p-weighted sum over the five candidate words is called the entropy (Session 17). Its unit is nats, because we used ln. In a spreadsheet it is SUMPRODUCT.')
    n.predict('Will the entropy be closer to 0.5 or to 3? Look at which words have most of the probability.')
    todo('answer = np.sum(p * neg_log_p)', 'multiply the two arrays entry by entry, then add')
    n.code('entropy = answer\ncheck("Step 5: entropy = sum of p times minus ln p = 1.133", entropy, 1.133, 0.001)\nif entropy is not None:\n    print("entropy =", round(float(entropy), 3), "nats")\n    print("the same in bits (log base 2):", round(float(np.sum(p * -np.log2(p))), 3), "bits")')
    n.read('The same entropy is 1.133 in nats and 1.634 in bits. Why does the number change when the base of the logarithm changes?')
    n.step(6, 'A sentence: product against sum of logarithms', 'Six words, each with the probability the model gave it given the words before it (made up).')
    n.code('words = ["The", "capital", "of", "Uganda", "is", "Kampala"]\nword_p = np.array([0.30, 0.20, 0.50, 0.40, 0.70, 0.62])\nprint(dict(zip(words, word_p)))')
    n.predict('Is the probability of the whole sentence bigger or smaller than the smallest word probability?')
    todo('answer = np.prod(word_p)', 'multiply all six probabilities together')
    n.code('sentence_p = answer\ncheck("Step 6a: product of the six probabilities = 0.005208", sentence_p, 0.005208, 0.000001)\nif sentence_p is not None:\n    print("product:", round(float(sentence_p), 6))')
    todo('answer = np.sum(np.log(word_p))', 'add up the natural logarithms of the six probabilities')
    n.code('log_sum = answer\ncheck("Step 6b: sum of the logs = -5.2576", log_sum, -5.2576, 0.001)\nif log_sum is not None:\n    print("sum of ln p:", round(float(log_sum), 4))\n'
           '    print("exp of the sum:", round(float(np.exp(log_sum)), 6), "  compare it with the product")')
    n.read('How does exp of the sum of logs compare with the product?')
    n.predict('The training loss of the sentence is the plain average of minus ln p over its six words (cross-entropy, Session 17). Is it closer to 0.1 or to 1?')
    todo('answer = -log_sum / 6', 'flip the sign of the sum of logs, then share it equally over the six words')
    n.code('sent_avg = answer\ncheck("Step 6c: plain average of minus ln p per word = 0.8763", sent_avg, 0.8763, 0.0005)\nif sent_avg is not None:\n    print("average minus ln p per word:", round(float(sent_avg), 4), "nats")')
    n.step(7, 'A long text: why we use logarithms', 'A text of 1000 words, each with probability 0.2.')
    n.code('long_p = np.full(1000, 0.2)\nprint("product of 1000 probabilities:", np.prod(long_p))')
    n.read('The true product is about 10 to the power -699, not 0. Why does the computer print 0.0?')
    n.predict('What will the sum of the 1000 logarithms be? Use ln 0.2 = -1.609.')
    todo('answer = np.sum(np.log(long_p))', 'add up the natural logarithms of all 1000 probabilities')
    n.code('long_log_sum = answer\ncheck("Step 7: sum of the logs for 1000 words = -1609.44", long_log_sum, -1609.44, 0.01)\nif long_log_sum is not None:\n    print("sum of logs:", round(float(long_log_sum), 2))')
    n.change('Change 0.2 to 0.5 in the first cell of Step 7 and run Step 7 again. Does the product still print 0.0? Try 2000 words. Then set it back to 1000 words and 0.2.')
    n.md('---\n## Finish\n\nRun the last cell. Every line must say OK. Then restart the session, run all cells in order and save the notebook.')
    n.code('show_checks()')
    return n
