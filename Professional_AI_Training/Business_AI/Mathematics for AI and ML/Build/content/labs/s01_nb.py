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
    n.code('total = answer\nprint("sum of p:", total)\ncheck("Step 1: the five probabilities add up to 1", total, 1.0)')
    n.read('Why must the total be exactly 1?')
    n.step(2, 'A function and its graph', 'The function f(x) = w x + b with w = 2 and b = 1. You compute f(3), then draw the graph.')
    n.predict('What is f(3) when w = 2 and b = 1?')
    todo('w = 2\nb = 1\nx = 3\nanswer = w * x + b', 'compute the output of the rule for x = 3')
    n.code('f3 = answer\nprint("f(3) =", f3)\ncheck("Step 2: f(3) = 7", f3, 7)\n\n'
           'xs = np.linspace(0, 5, 50)\nplt.plot(xs, 2 * xs + 1)\nplt.plot([3], [7], "o")\nplt.xlabel("input x"); plt.ylabel("f(x)"); plt.title("f(x) = 2x + 1")\nplt.show()')
    n.change('Change w to 3 in your cell and run it again. What is f(3) now, and how does the line on the graph change? Then change w back to 2.')
    n.step(3, 'Exponentials and logarithms', 'np.exp(x) is e to the power x. np.log(x) is the natural logarithm ln x. They undo each other.')
    n.predict('Will ln 6 be larger or smaller than ln 2 + ln 3? Guess before you run.')
    todo('answer = np.log(6)', 'the natural logarithm of 6')
    n.code('ln6 = answer\nprint("ln 6      =", round(float(ln6), 4))\ncheck("Step 3a: ln 6 = 1.7918", ln6, 1.7918, 0.001)')
    todo('answer = np.log(2) + np.log(3)', 'ln 2 and ln 3 added together')
    n.code('ln2_plus_ln3 = answer\nprint("ln 2 + ln 3 =", round(float(ln2_plus_ln3), 4))\ncheck("Step 3b: ln 2 + ln 3 = ln 6 (the product rule)", ln2_plus_ln3, 1.7918, 0.001)\n'
           'print("exp(ln 6) =", round(float(np.exp(np.log(6))), 4), " (exp undoes ln)")')
    n.read('Are the two numbers equal? Which log rule is this?')
    n.change('Try np.log(2 + 3) and np.log(2) + np.log(3). Are they equal? What does this tell you about the log of a sum?')
    n.step(4, 'Negative log-probability of each candidate word', 'Minus ln p is positive when p is below 1, and it grows as p shrinks. Training uses it as the loss for the word that really came next.')
    n.predict('Which word will have the largest minus ln p, and which the smallest?')
    todo('answer = -np.log(p)', 'minus the natural log of every probability, all at once')
    n.code('neg_log_p = np.asarray(answer)\ntable["minus_ln_p"] = neg_log_p.round(3)\nprint(table)\n'
           'check("Step 4: minus ln p of the five words", neg_log_p, [0.478, 1.715, 2.303, 2.813, 3.219], 0.001)')
    n.change('In a new cell run p[0] = 0.9, then run the Step 4 cells again. What happens to the minus ln p of Kampala? The five numbers no longer add up to 1; that is fine for this experiment. Then run p[0] = 0.62 and Step 4 again to restore it.')
    n.step(5, 'Average negative log-probability with a dot product', 'Weight each minus ln p by its own probability and add: sum of p times (minus ln p). This weighted average is the entropy of the five probabilities (Session 17). In a spreadsheet it is SUMPRODUCT.')
    todo('answer = np.sum(p * neg_log_p)', 'weight each minus ln p by its own probability, then add them all')
    n.code('avg = answer\nprint("sum of p * (-ln p) =", round(float(avg), 3))\ncheck("Step 5: sum of p times minus ln p = 1.133", avg, 1.133, 0.001)')
    n.step(6, 'A sentence: product against sum of logarithms', 'Six words, each with the probability the model gave it given the words before it (made up).')
    n.code('words = ["The", "capital", "of", "Uganda", "is", "Kampala"]\nword_p = np.array([0.30, 0.20, 0.50, 0.40, 0.70, 0.62])\nprint(dict(zip(words, word_p)))')
    n.predict('Is the probability of the whole sentence bigger or smaller than the smallest word probability?')
    todo('answer = np.prod(word_p)', 'multiply all six probabilities together')
    n.code('sentence_p = answer\nprint("product:", round(float(sentence_p), 6))\ncheck("Step 6a: product of the six probabilities = 0.005208", sentence_p, 0.005208, 0.000001)')
    todo('answer = np.sum(np.log(word_p))', 'add up the natural logarithms of the six probabilities')
    n.code('log_sum = answer\nprint("sum of ln p:", round(float(log_sum), 4))\ncheck("Step 6b: sum of the logs = -5.2576", log_sum, -5.2576, 0.001)\n'
           'print("exp of the sum:", round(float(np.exp(log_sum)), 6), "  equals the product")')
    n.read('How does exp of the sum of logs compare with the product?')
    n.predict('The training score for the sentence is the average of minus ln p per word. Is it closer to 0.1 or to 1?')
    todo('answer = -log_sum / 6', 'the average of minus ln p per word of the sentence')
    n.code('sent_avg = answer\nprint("average minus ln p per word:", round(float(sent_avg), 4))\ncheck("Step 6c: average minus ln p per word = 0.8763", sent_avg, 0.8763, 0.0005)')
    n.step(7, 'A long text: why we use logarithms', 'A text of 1000 words, each with probability 0.2.')
    n.code('long_p = np.full(1000, 0.2)\nprint("product of 1000 probabilities:", np.prod(long_p))')
    n.predict('That product is not really 0. Why does the computer print 0.0? What will the sum of the logs be?')
    todo('answer = np.sum(np.log(long_p))', 'add up the natural logarithms of all 1000 probabilities')
    n.code('long_log_sum = answer\nprint("sum of logs:", round(float(long_log_sum), 2))\ncheck("Step 7: sum of the logs for 1000 words = -1609.44", long_log_sum, -1609.44, 0.01)')
    n.change('Change 0.2 to 0.5 and run Step 7 again. Does the product still print 0.0? Try 2000 words.')
    n.md('---\n## Finish\n\nRun the last cell. Every line must say OK. Then restart the session, run all cells in order and save the notebook.')
    n.code('show_checks()')
    return n
