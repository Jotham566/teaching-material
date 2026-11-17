"""Session 15 Python lab: conditional probability from counts, independence, Bayes with natural frequencies, Naive Bayes from counts."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'kit'))
import nb as NB  # noqa: E402

TITLE = 'Session 15: Conditional probability and Bayes'


def build(solution: bool):
    n = NB.Notebook()

    def todo(sol, learner):
        n.code(sol if solution else learner)

    n.md('# Session 15: Conditional probability and Bayes (Python lab)\n\n'
         'You will read conditional probabilities from a table of counts, test independence, update a belief with Bayes theorem, and build a small Naive Bayes spam filter from word counts.\n\n'
         '**How to work.** In each step: read the idea, write a PREDICT guess, run the cell, READ the output, then CHANGE one thing in the experiment cell. Cells with `None  # your code here` are yours to fill. '
         'The automatic checks print OK or NOT YET. Run the cells from the top, in order. All numbers are illustrative (made up to show the arithmetic).')
    n.step(0, 'Set up', 'Only numpy is needed.')
    n.code('import numpy as np\nprint("ready")')
    n.check_setup()

    n.step(1, 'A table of counts: joint, marginal and conditional', '100 emails. Rows: spam, ham. Columns: contains "free", does not contain "free".')
    n.predict('Is P(spam | free) bigger or smaller than P(spam) = 0.4? Is P(free | spam) the same number as P(spam | free)?')
    todo('table = np.array([[28, 12], [6, 54]])        # rows spam, ham; columns free, no free\n'
         'total = table.sum()\n'
         'p_joint = table[0, 0] / total                       # P(spam and free)\n'
         'p_free = table[:, 0].sum() / total                  # P(free), a marginal\n'
         'p_spam_given_free = p_joint / p_free                # conditional = joint / marginal\n'
         'p_free_given_spam = table[0, 0] / table[0].sum()\n'
         'print(p_joint, p_free, round(p_spam_given_free, 4), p_free_given_spam)\n'
         'check("P(spam and free)", p_joint, 0.28, 0.0001)\n'
         'check("P(free)", p_free, 0.34, 0.0001)\n'
         'check("P(spam | free)", p_spam_given_free, 0.8235, 0.0001)\n'
         'check("P(free | spam)", p_free_given_spam, 0.70, 0.0001)',
         'table = np.array([[28, 12], [6, 54]])        # rows spam, ham; columns free, no free\n'
         'total = table.sum()\n'
         '# Hint: the conditional probability is a joint probability divided by a marginal one. Column 0 of the table is the emails with "free".\n'
         'p_joint = None  # your code here\n'
         'p_free = None  # your code here\n'
         'p_spam_given_free = None  # your code here\n'
         'p_free_given_spam = None  # your code here\n'
         'check("P(spam and free)", p_joint, 0.28, 0.0001)\n'
         'check("P(free)", p_free, 0.34, 0.0001)\n'
         'check("P(spam | free)", p_spam_given_free, 0.8235, 0.0001)\n'
         'check("P(free | spam)", p_free_given_spam, 0.70, 0.0001)')
    n.read('Why are P(spam | free) and P(free | spam) different numbers? Which groups of emails does each one divide by?')
    n.change('Run the experiment cell: P(ham | free). Predict it first. It must add up with P(spam | free) to 1.')
    n.code('print("P(ham | free) =", round(6 / 34, 4))')

    n.step(2, 'Independence (recall Session 13)', 'Independent events satisfy P(A and B) = P(A) × P(B). If "free" and spam were independent, the count of spam emails with "free" would be total × P(spam) × P(free).')
    n.predict('Will the expected count be bigger or smaller than the observed 28?')
    todo('expected = total * 0.4 * p_free                  # expected spam emails with "free" if independent\n'
         'print(expected, "expected against", table[0, 0], "observed")\n'
         'check("expected count if independent", expected, 13.6, 0.0001)',
         '# Hint: the independence rule from the slides, scaled up to all the emails. P(spam) = 0.4.\n'
         'expected = None  # your code here\n'
         'check("expected count if independent", expected, 13.6, 0.0001)')
    n.read('Observed is much larger than expected. What does that say about the word "free" and spam?')

    n.step(3, 'Bayes theorem with a medical test', 'Prior P(H) = 0.01. Likelihood (sensitivity) P(positive | sick) = 0.90. False positive rate P(positive | healthy) = 0.10.')
    n.predict('After one positive test, will the chance of being sick be about 90%, 50% or under 10%?')
    todo('def bayes(prior, like, fpr):\n'
         '    evidence = like * prior + fpr * (1 - prior)          # P(positive), both routes\n'
         '    return like * prior / evidence, evidence\n'
         'post1, p_e = bayes(0.01, 0.90, 0.10)\n'
         'post2, _ = bayes(post1, 0.90, 0.10)                      # second independent positive test: the posterior becomes the new prior\n'
         'print(round(p_e, 3), round(post1, 4), round(post2, 3), "natural frequencies:", 9 / (9 + 99))\n'
         'check("P(positive), the evidence", p_e, 0.108, 0.0001)\n'
         'check("posterior after one positive test", post1, 0.0833, 0.0001)\n'
         'check("posterior after two positive tests", post2, 0.45, 0.0001)',
         'def bayes(prior, like, fpr):\n'
         '    # Hint: the evidence adds up both routes to a positive test (sick and positive, healthy and positive). The posterior is the sick-and-positive route divided by the evidence.\n'
         '    return None, None  # your code here\n'
         'post1, p_e = bayes(0.01, 0.90, 0.10)\n'
         'post2 = None  # your code here: use post1 as the new prior\n'
         'check("P(positive), the evidence", p_e, 0.108, 0.0001)\n'
         'check("posterior after one positive test", post1, 0.0833, 0.0001)\n'
         'check("posterior after two positive tests", post2, 0.45, 0.0001)')
    n.read('Most positive results come from healthy people. How many of 1,000 people are in each group (the tree on the slides)?')
    n.change('Run the experiment cell: a prevalence of 10% instead of 1%. Predict the posterior first.')
    n.code('print(round(0.9 * 0.1 / (0.9 * 0.1 + 0.1 * 0.9), 4))')

    n.step(4, 'Naive Bayes spam filter from counts', 'Counts: how many of the 40 spam and 60 ham emails contain the words free, prize and meeting. Smoothed likelihood = (count + 1) / (class size + 2).')
    n.predict('Email 1 has "free" and "prize" but not "meeting". Email 2 has "free" and "meeting" but not "prize". Which is more likely spam?')
    n.code('spam_counts = np.array([28, 20, 4])      # free, prize, meeting\nham_counts = np.array([6, 0, 30])\nn_spam, n_ham = 40, 60\nemail1 = np.array([1, 1, 0])           # 1 = the word is in the email\nemail2 = np.array([1, 0, 1])')
    todo('def posterior(has, smooth=True):\n'
         '    add = 1 if smooth else 0\n'
         '    like_s = (spam_counts + add) / (n_spam + 2 * add)\n'
         '    like_h = (ham_counts + add) / (n_ham + 2 * add)\n'
         '    score_s = (n_spam / 100) * np.prod(np.where(has == 1, like_s, 1 - like_s))\n'
         '    score_h = (n_ham / 100) * np.prod(np.where(has == 1, like_h, 1 - like_h))\n'
         '    return score_s / (score_s + score_h)\n'
         'like_free_spam = (28 + 1) / (40 + 2)\n'
         'like_prize_ham = (0 + 1) / (60 + 2)\n'
         'p1, p2 = posterior(email1), posterior(email2)\n'
         'print(round(like_free_spam, 4), round(like_prize_ham, 4), round(p1, 4), round(p2, 4))\n'
         'check("smoothed likelihood of free in spam", like_free_spam, 0.6905, 0.0001)\n'
         'check("smoothed likelihood of prize in ham", like_prize_ham, 0.0161, 0.0001)\n'
         'check("posterior spam probability of email 1", p1, 0.9955, 0.0001)\n'
         'check("posterior spam probability of email 2", p2, 0.3304, 0.0001)',
         'def posterior(has, smooth=True):\n'
         '    add = 1 if smooth else 0                                   # add = 1 smooths; add = 0 uses plain counts\n'
         '    like_s = (spam_counts + add) / (n_spam + 2 * add)          # likelihood of each word in spam\n'
         '    like_h = None  # your code here: the same line for ham\n'
         '    score_s = (n_spam / 100) * np.prod(np.where(has == 1, like_s, 1 - like_s))   # prior times one factor per word\n'
         '    score_h = None  # your code here: the same line for ham\n'
         '    if like_h is None or score_h is None:\n'
         '        return None\n'
         '    return score_s / (score_s + score_h)\n'
         '# Hint: copy the spam lines and change spam to ham (60 ham emails). Then fill the two single likelihoods below by hand: (count + 1) / (class size + 2).\n'
         'like_free_spam = None  # your code here\n'
         'like_prize_ham = None  # your code here\n'
         'p1, p2 = posterior(email1), posterior(email2)\n'
         'check("smoothed likelihood of free in spam", like_free_spam, 0.6905, 0.0001)\n'
         'check("smoothed likelihood of prize in ham", like_prize_ham, 0.0161, 0.0001)\n'
         'check("posterior spam probability of email 1", p1, 0.9955, 0.0001)\n'
         'check("posterior spam probability of email 2", p2, 0.3304, 0.0001)')
    todo('# Long emails: add logarithms (no underflow), then the two-class softmax, which is the sigmoid of the gap (Session 11).\n'
         'log_s = np.log(0.4) + np.log(np.where(email1 == 1, (spam_counts + 1) / 42, 1 - (spam_counts + 1) / 42)).sum()\n'
         'log_h = np.log(0.6) + np.log(np.where(email1 == 1, (ham_counts + 1) / 62, 1 - (ham_counts + 1) / 62)).sum()\n'
         'p_log = 1 / (1 + np.exp(log_h - log_s))              # softmax of two scores = sigmoid of log_s - log_h\n'
         'check("log score of ham for email 1", log_h, -7.5123, 0.0005)\n'
         'check("posterior of email 1 computed with logs", p_log, 0.9955, 0.0001)\n'
         'print(round(log_s, 3), round(log_h, 3), round(p_log, 4))',
         '# Long emails: add logarithms (no underflow), then the two-class softmax, which is the sigmoid of the gap (Session 11).\n'
         'log_s = np.log(0.4) + np.log(np.where(email1 == 1, (spam_counts + 1) / 42, 1 - (spam_counts + 1) / 42)).sum()   # given: the spam log score\n'
         '# Hint: copy the line above for ham (prior 0.6, 60 ham emails, so divide by 62). Then p_log = 1 / (1 + np.exp(log_h - log_s)).\n'
         'log_h = None  # your code here\n'
         'p_log = None  # your code here\n'
         'check("log score of ham for email 1", log_h, -7.5123, 0.0005)\n'
         'check("posterior of email 1 computed with logs", p_log, 0.9955, 0.0001)')
    n.read('Which words pushed email 2 towards ham? Is the filter sure about it?')

    n.step(5, 'Break it: remove the smoothing', 'Set smooth=False so the zero count of "prize" in ham stays zero.')
    n.predict('What will the posterior of email 1 become if the ham likelihood of "prize" is exactly 0?')
    todo('p1_raw = posterior(email1, smooth=False)\n'
         'print(p1_raw)\n'
         'check("posterior of email 1 without smoothing", p1_raw, 1.0, 0.0001)',
         '# Hint: use your posterior function on email 1 with the smoothing switched off.\n'
         'p1_raw = None  # your code here\n'
         'check("posterior of email 1 without smoothing", p1_raw, 1.0, 0.0001)')
    n.read('The filter now says 100% spam from three words. Is that sensible? What does it say about reading a stated probability from any model?')
    n.change('Run the experiment cell: the effect of the prior. Use a prior of 0.01 for spam (a rare-spam mailbox) with the smoothed likelihoods of email 1 and see how far the posterior moves.')
    n.code('ls = (spam_counts + 1) / 42\nlh = (ham_counts + 1) / 62\nss = 0.01 * np.prod(np.where(email1 == 1, ls, 1 - ls))\nsh = 0.99 * np.prod(np.where(email1 == 1, lh, 1 - lh))\nprint(round(ss / (ss + sh), 4))')

    n.step(6, 'Show the checks', 'Run this last cell. A learner who has filled every answer sees "All 15 checks pass".')
    n.code('show_checks()')
    return n
