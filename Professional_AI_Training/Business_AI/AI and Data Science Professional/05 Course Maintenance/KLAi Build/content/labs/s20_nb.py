"""Session 20 lab notebook: a neuron and a training loop in numpy, TensorFlow Playground, then MLPClassifier against a random forest on the loans.

NEEDS: the authoring sandbox has no scikit-learn MLPClassifier, RandomForestClassifier or LogisticRegression with these settings, so the runner only proves that every cell compiles.
The numpy cells (steps 1 and 2 and the by-hand counts) were run separately in the sandbox. The AUC checks compare scikit-learn results with a numpy reference
(s20.facts(): a numpy logistic regression and a numpy network on the same loans) with wide tolerances, because scikit-learn starts from other random weights."""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'kit'))
sys.path.insert(0, str(HERE.parent))
import nb as NB  # noqa: E402
import s20  # noqa: E402

TITLE = 'A neuron, a training loop and a network on the loans'
NEEDS = ['sklearn']


def build(solution):
    F = s20.facts()
    fw, fl = F['final_w'], F['final_loss']
    n = NB.Notebook()

    def todo(code, hint):
        n.code(code if solution else f'answer = None  # your code here: {hint}')

    def G(code):
        """A cell that only runs and prints what the learner built. In the learner version it prints a friendly line, not an error, while an answer above is still None."""
        if solution:
            n.code(code)
        else:
            body = '\n'.join('    ' + l for l in code.split('\n'))
            n.code('try:\n' + body + '\nexcept Exception as err:\n    print("Not yet: an answer above is still None or incomplete (" + type(err).__name__ + ").")')

    n.md('# Session 20 lab: a neuron, a training loop and a network on the loans\n\n**AI and Data Science Professional** | KLAi Professional Learning\n\n'
         'You build one artificial neuron and a gradient descent loop with numpy, spend ten minutes in TensorFlow Playground, then compare an MLPClassifier with a random forest and logistic regression on the Nile Microfinance loans. '
         'You finish with a results table and a three-sentence recommendation for the credit team.\n\n'
         '**How to use this notebook**\n\n1. Run the cells in order from the top (Shift and Enter).\n2. Every step has the same rhythm: **PREDICT**, run, **READ**, then **CHANGE** one thing.\n'
         '3. Cells that say `answer = None` are yours to fill in. Replace `None` with your code. Then run the check cell under it.\n'
         '4. The neuron and the weights in Step 1 are illustrative (made up to show the arithmetic). The loans are fictional and generated.\n'
         '5. The AUC checks accept a range, because scikit-learn starts from random weights. If a check says NOT YET and your number is close, read the range in the check cell.\n6. If you get an error, read the last line first.')
    n.data_setup()
    n.check_setup()
    n.code('# A helper so that a check never crashes while your answer is still None. You do not need to read it.\nimport numpy as np\nimport pandas as pd\nimport matplotlib.pyplot as plt\n\n'
           'def safe(f):\n    try:\n        return float(f())\n    except Exception:\n        return float("nan")')

    # ---------------------------------------------------------------- step 1
    n.step(1, 'One artificial neuron', 'A neuron is a weighted sum of the inputs plus a bias, passed through an activation function. In a spreadsheet the weighted sum is SUMPRODUCT.')
    n.code('# one loan: late payments, savings (UGX millions), loan size (UGX millions)\nx = np.array([1, 0.8, 0.3])\n'
           'w = np.array([0.9, -1.2, 1.5])   # illustrative weights that were never trained\nb = -1.0                         # the bias\nprint("inputs", x, "weights", w, "bias", b)')
    n.predict('Will the sigmoid score of this loan be above 0.5 or below 0.5? Work out the weighted sum plus bias by hand first.')
    todo('answer = 1 / (1 + np.exp(-(np.dot(x, w) + b)))', 'np.dot(x, w) + b is the weighted sum plus bias. Put it into the sigmoid 1 / (1 + np.exp(-z))')
    G('score = answer\nprint("sigmoid score:", round(float(score), 3))')
    n.code(f'check("Step 1a: neuron score", safe(lambda: answer), {F["lab_score"]:.4f}, 0.001)')
    n.read('Which input pushes the score up and which pushes it down? Where does the weighted sum plus bias come out, and what does that mean for the sigmoid?')
    todo('answer = max(0, np.dot(x, w) + b)', 'ReLU returns 0 for a negative total and the total itself otherwise')
    G('relu_out = answer\nprint("ReLU output:", relu_out)')
    n.code('check("Step 1b: ReLU of a negative total is 0", safe(lambda: answer), 0.0, 0.001)')
    n.change('Make the first weight larger: use w2 = np.array([4.5, -1.2, 1.5]) in the cell below. What does the score become? What does that say about late payments?')
    todo('w2 = np.array([4.5, -1.2, 1.5])\nanswer = 1 / (1 + np.exp(-(np.dot(x, w2) + b)))', 'the same neuron with the first weight 4.5')
    G('new_score = answer\nprint("new score:", round(float(new_score), 3))')
    n.code('check("Step 1c: the score is now above 0.9", safe(lambda: answer > 0.9), 1)')

    # ---------------------------------------------------------------- step 2
    n.step(2, 'A training loop on one weight', 'One weight must learn that 2 times the weight gives 6. The loss is (2w - 6) squared. Gradient descent moves the weight against the slope of the loss.')
    n.predict('Start at w = 0 with a learning rate of 0.05 and run 8 steps. Will w end above 3, below 3, or exactly 3?')
    todo('w, lr = 0.0, 0.05\nfor step in range(8):\n    grad = 2 * (w * 2.0 - 6.0) * 2.0   # the slope of the loss (2w - 6)**2\n    w = w - lr * grad\nanswer = w', 'a loop of 8 steps: find the gradient, then w = w - lr * grad')
    G('w_after = answer\nprint("w after 8 steps:", round(float(w_after), 3))')
    n.code(f'check("Step 2a: w after 8 steps at learning rate 0.05", safe(lambda: answer), {fw[0.05]:.4f}, 0.01)')
    n.read('Is w exactly 3? Why do the steps get smaller as w approaches 3?')
    n.change('Run the same loop with lr = 0.25 and print w at every step. What do you see? Then try lr = 0.5.')
    todo('w, lr = 0.0, 0.5\nfor step in range(8):\n    grad = 2 * (w * 2.0 - 6.0) * 2.0\n    w = w - lr * grad\nanswer = (w * 2.0 - 6.0) ** 2', 'the same loop with lr = 0.5, then the loss (2w - 6) squared at the end')
    G('loss_big = answer\nprint("loss after the 8th update at lr = 0.5:", round(float(loss_big)))')
    n.code('check("Step 2b: the loss blows up (above 100)", safe(lambda: answer > 100), 1)')

    # ---------------------------------------------------------------- step 3
    n.step(3, 'TensorFlow Playground (10 minutes)', 'Open TensorFlow Playground in a new browser tab (search for it: it is free and needs no account). Work through the four challenges on the slide. Record what you see in your own words.')
    n.md('**Challenge 1, circle.** No hidden layer, then one hidden layer with 4 neurons. What changed?\n\n> What I saw: \n\n**Challenge 2, spiral.** Add layers and neurons. Which size was enough?\n\n> What I saw: \n\n'
         '**Challenge 3, overfitting.** Raise the noise, use few training points, train for a long time. When did the training loss and the test loss separate?\n\n> What I saw: \n\n'
         '**Challenge 4, learning rate and activation.** Which settings failed, which were slow, which were fast?\n\n> What I saw: ')

    # ---------------------------------------------------------------- step 4
    n.step(4, 'Prepare the loans', 'The Nile Microfinance loans: each record is one loan and default is 1 when the loan went bad. The preparation is the one from Sessions 14 to 17: the two impossible ages (0 and 199) become the median age, so all 8,000 loans stay, and `collection_calls` is left out because it is recorded only after a loan goes bad. '
            'One difference: a blank income stays blank here, because the imputer inside the Pipeline learns the median from the training records only (leak-free). Sessions 14 to 17 computed it on all loans before the split, on purpose, to keep things simple.')
    n.predict('How many loans will remain, and how many records will train and test with a 75 and 25 split? How many defaults will the stratified test set hold?')
    n.code('from sklearn.model_selection import train_test_split\nfrom sklearn.pipeline import make_pipeline\nfrom sklearn.impute import SimpleImputer\nfrom sklearn.preprocessing import StandardScaler\n'
           'from sklearn.linear_model import LogisticRegression\nfrom sklearn.neural_network import MLPClassifier\nfrom sklearn.ensemble import RandomForestClassifier\nfrom sklearn.metrics import roc_auc_score\n\nloans = pd.read_csv("loans.csv")\nprint(loans.shape)')
    todo('bad_age = (loans.age < 18) | (loans.age > 100)\nloans.loc[bad_age, "age"] = loans.loc[~bad_age, "age"].median()\nanswer = loans', 'replace the two impossible ages (under 18 or over 100) by the median of the valid ages (36). Keep every row')
    G('loans = answer\nloans["income_missing"] = loans["monthly_income_ugx"].isna().astype(int)\n'
           '# instalment_to_income: loan x 1.15 / term / monthly income. The 1.15 (loan plus 15 percent interest and fees) is an ILLUSTRATIVE assumption, not in the data. A blank income gives a blank ratio.\n'
           'loans["instalment_to_income"] = loans["loan_amount_ugx"] * 1.15 / loans["term_months"] / loans["monthly_income_ugx"]\n'
           'cols = ["age", "monthly_income_ugx", "income_missing", "loan_amount_ugx", "term_months", "previous_loans", "previous_late_payments", "group_loan",\n        "savings_balance_ugx", "has_mobile_money", "distance_to_branch_km", "instalment_to_income"]\n'
           'X = loans[cols]          # collection_calls is left out on purpose: it leaks the answer\ny = loans["default"]')
    todo('X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)\nanswer = X_train', 'train_test_split of X and y with test_size=0.25, stratify=y and random_state=42 (assign the four parts; answer is X_train)')
    n.code('X_train = answer')
    G('print(len(X), len(X_train), len(X_test), "defaults in the test records:", y_test.sum())\nprint(X_test.index[:10].tolist())   # the same test rows as Sessions 14 to 17')
    n.code(f'check("Step 4a: loans kept", safe(lambda: len(X)), {F["n_loans"]})\ncheck("Step 4b: training records", safe(lambda: len(X_train)), {F["n_train"]})\n'
           f'check("Step 4c: defaults in the test records", safe(lambda: y_test.sum()), {F["test_defaults"]})\ncheck("Step 4d: same test rows as the course (sum of the row numbers)", safe(lambda: sum(X_test.index)), {F["test_index_sum"]})\n'
           'check("Step 4e: collection_calls is not in X", safe(lambda: "collection_calls" not in X.columns), 1)')
    n.read('How many blank monthly_income_ugx values are there in X_train? Why must the network never see a blank, and why does the imputer sit inside the Pipeline?')
    todo('answer = 12 * 16 + 16 + 16 * 8 + 8 + 8 * 1 + 1', 'weights plus biases of a network with 12 inputs, hidden layers of 16 and 8 neurons and 1 output')
    G('n_params = answer\nprint("parameters:", n_params)')
    n.code(f'check("Step 4f: parameters of the 12-16-8-1 network", safe(lambda: answer), {F["net_params"]})')
    todo('answer = int(np.ceil(len(X_train) / 200))', 'the number of batches of 200 records in one pass over X_train')
    G('n_batches = answer\nprint("batches per epoch:", n_batches)')
    n.code(f'check("Step 4g: batches per epoch", safe(lambda: answer), {F["n_batches"]})')

    # ---------------------------------------------------------------- step 5
    n.step(5, 'Logistic regression, a network and a forest on the same split', 'Every model sees the same training records and is scored on the same test records with the AUC. The imputer and the scaler sit inside the Pipeline, so they learn only from the training records. The logistic regression uses the default C = 1.0 (L2 penalty).')
    n.predict('Which will score the highest AUC on the test records: logistic regression, the MLPClassifier or the random forest? Write the order you expect.')
    todo('answer = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), LogisticRegression(max_iter=1000))', 'make_pipeline with SimpleImputer(strategy="median"), StandardScaler() and LogisticRegression(max_iter=1000)')
    G('logit = answer\nlogit.fit(X_train, y_train)\nauc_logit = roc_auc_score(y_test, logit.predict_proba(X_test)[:, 1])\nprint("logistic regression AUC:", round(auc_logit, 3))')
    n.code(f'check("Step 5a: logistic regression AUC (reference {F["auc_logit_test"]:.3f}, a range of 0.03)", safe(lambda: auc_logit), {F["auc_logit_test"]:.4f}, 0.03)')
    todo('answer = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), MLPClassifier(hidden_layer_sizes=(16, 8), max_iter=500, random_state=42))',
         'make_pipeline with SimpleImputer, StandardScaler and MLPClassifier(hidden_layer_sizes=(16, 8), max_iter=500, random_state=42)')
    G('mlp = answer\nmlp.fit(X_train, y_train)\nauc_mlp = roc_auc_score(y_test, mlp.predict_proba(X_test)[:, 1])\nprint("MLPClassifier AUC:", round(auc_mlp, 3))')
    n.code(f'check("Step 5b: MLPClassifier AUC (reference {F["auc_net_test"]:.3f}, a range of 0.05)", safe(lambda: auc_mlp), {F["auc_net_test"]:.4f}, 0.05)')
    todo('answer = make_pipeline(SimpleImputer(strategy="median"), RandomForestClassifier(n_estimators=200, random_state=42))', 'make_pipeline with SimpleImputer and RandomForestClassifier(n_estimators=200, random_state=42). A forest needs no scaler')
    G('forest = answer\nforest.fit(X_train, y_train)\nauc_rf = roc_auc_score(y_test, forest.predict_proba(X_test)[:, 1])\nprint("random forest AUC:", round(auc_rf, 3))')
    n.code(f'check("Step 5c: random forest AUC (between 0.69 and 0.77)", safe(lambda: auc_rf), 0.73, 0.04)')
    n.read('Does the network beat logistic regression by enough to matter? Does the forest beat both? Is the order the one you predicted? Differences of up to about 0.03 from the slides are expected, because a scikit-learn network starts from random weights and trains with the Adam solver.')
    n.change('Add "collection_calls" to the list of variables, refit logistic regression and look at the AUC. Then remove it again and rerun the cells. Why must this variable stay out?')

    # ---------------------------------------------------------------- step 6
    n.step(6, 'See overfitting in a network', 'Train a larger network on only 300 loans and compare its training AUC with its test AUC.')
    n.predict('A network with 64 and 64 hidden neurons has 300 training loans. Will its training AUC be near 0.7, or near 1.0? And its test AUC?')
    todo('answer = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), MLPClassifier(hidden_layer_sizes=(64, 64), max_iter=1000, random_state=42))',
         'the same kind of Pipeline with MLPClassifier(hidden_layer_sizes=(64, 64), max_iter=1000, random_state=42)')
    G('big = answer\nbig.fit(X_train.iloc[:300], y_train.iloc[:300])\n'
      'auc_train = roc_auc_score(y_train.iloc[:300], big.predict_proba(X_train.iloc[:300])[:, 1])\nauc_test = roc_auc_score(y_test, big.predict_proba(X_test)[:, 1])\n'
      'gap = auc_train - auc_test\nprint("training AUC", round(auc_train, 3), "test AUC", round(auc_test, 3), "gap", round(gap, 3))')
    n.code(f'check("Step 6: the training AUC is far above the test AUC (the numpy reference gap is {F["of_auc_train"] - F["of_auc_test"]:.2f})", safe(lambda: gap > 0.1), 1)')
    n.read('Which of the two numbers would you quote to a manager? Name two ways to reduce this gap.')

    # ---------------------------------------------------------------- step 7
    n.step(7, 'Your results table and recommendation', 'Collect the three models in one table and save it. This file and your three sentences are what you keep. The file is saved in your Colab folder (the Files panel on the left): download it before you close Colab.')
    todo('answer = pd.DataFrame({"model": ["Logistic regression", "MLPClassifier (16, 8)", "Random forest (200 trees)"],\n                        "test AUC": [round(auc_logit, 3), round(auc_mlp, 3), round(auc_rf, 3)],\n'
         '                        "parameters or trees": [13, 353, 200]})', 'a DataFrame with the columns model, test AUC and parameters or trees for the three models')
    G('results = answer\nresults.to_csv("session20_model_comparison.csv", index=False)   # saved in your Colab folder\nprint(results)')
    n.code('check("Step 7: the results table has three models", safe(lambda: len(answer)), 3)')
    n.code('show_checks()')
    n.md('## Your recommendation to the credit team\n\nDouble-click this cell and write three sentences with your own numbers.\n\n1. The three test AUC scores, from the same split.\n'
         '2. Which model you recommend, and why (the simplest model that is good enough is a good answer).\n3. One limit: for example one split only, the loans are fictional, or the AUC does not say how many borrowers you would approve.\n\n> My three sentences: ')

    # ---------------------------------------------------------------- optional
    n.md('## Optional: a pretrained image classifier\n\nOnly if you finish early. The first run downloads the model weights from the Hugging Face Hub. The download is free, but read the model page first: the size and the licence can change. '
         'Upload only photos you are allowed to use, never photos of people or customers. The code is commented out; remove the # signs to run it.')
    n.code('# !pip install -q transformers\n# from transformers import pipeline\n# from google.colab import files\n# name = list(files.upload())[0]\n# classifier = pipeline("image-classification")\n# print(classifier(name)[:3])')
    return n
