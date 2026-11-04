"""Session 12 lab notebook: Inference, is the difference real? Expected values come from content/f12_facts.py (numpy and pandas only).
The notebook also calls SciPy and statsmodels, which are not installed where it was written, so the runner only proves that every cell compiles (NEEDS)."""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[2] / 'kit'))
import nb as NB  # noqa: E402

_spec = importlib.util.spec_from_file_location('f12_facts', HERE.parents[1] / 'f12_facts.py')
f12 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(f12)

TITLE = 'Inference'
NEEDS = ['scipy', 'statsmodels']


def build(solution):
    F = f12.facts()
    sol = solution

    def pick(answer, hint):
        return answer if sol else f'# your code here: {hint}'

    nb = NB.Notebook()
    nb.md('# Session 12 lab: is the difference real?\n\n'
          'Did the Lakeside Mart loyalty offer raise spend? You will answer it five ways: the formula, the bootstrap, the permutation test, the Welch t-test and a test of two proportions. '
          'You compute each number by hand with NumPy first, then check it against SciPy or statsmodels.\n\n'
          'Rhythm for every step: **PREDICT**, **RUN**, **READ**, **CHANGE**. Cells with `# your code here` are yours to fill. The check cells say OK when your answer is right.\n\n'
          '*Random seeds: use `np.random.default_rng(42)` exactly as written, and make the random calls in the order shown. Bootstrap and permutation checks allow a small tolerance.*')
    nb.data_setup()
    nb.check_setup()
    nb.code('import numpy as np\nimport pandas as pd\nimport matplotlib.pyplot as plt\nfrom scipy import stats\nfrom statsmodels.stats.proportion import proportions_ztest')

    # step 1
    nb.step(1, 'Split the test into offer and control', 'Random assignment makes the two groups alike in everything except the offer (an A/B test).')
    nb.predict('The offer group averaged 66,704 UGX and the control group about 61,660. How big a gap will you find, and is it big enough to trust?')
    nb.code("test = pd.read_csv('offer_test.csv')\ntest.head()")
    nb.code(pick("offer = test[test['group'] == 'offer']['next_month_spend_ugx'].to_numpy()\ncontrol = test[test['group'] == 'control']['next_month_spend_ugx'].to_numpy()",
                 'offer and control are NumPy arrays of next_month_spend_ugx for each group') +
            ("" if sol else "\noffer = control = np.array([np.nan])") +
            f"\nprint(len(offer), len(control))\ncheck('customers in offer', len(offer), {F['n_o']}, 0)\ncheck('customers in control', len(control), {F['n_c']}, 0)")
    nb.read('Each record is one loyalty customer. Which group is the treatment group?')
    nb.change('Print offer.mean() and control.mean(). Which one is larger, and by how much?')

    # step 2
    nb.step(2, 'The lift, its standard error and the formula interval', 'Standard error of a mean = s / sqrt(n). The lift has a standard error that combines both groups. A 95 percent interval is the lift plus or minus 1.96 standard errors.')
    nb.predict('Will the 95 percent interval for the lift include zero?')
    nb.code(pick("lift = offer.mean() - control.mean()\nv_o = offer.var(ddof=1) / len(offer)\nv_c = control.var(ddof=1) / len(control)\nse = np.sqrt(v_o + v_c)\nci_low = lift - 1.96 * se\nci_high = lift + 1.96 * se",
                 'lift = offer mean minus control mean; se = sqrt(var/n of each group, added); the interval is lift plus or minus 1.96 se (use ddof=1 for the variance)') +
            ("" if sol else "\nlift = se = ci_low = ci_high = np.nan") +
            f"\nprint(np.round(lift), np.round(se), np.round(ci_low), np.round(ci_high))\ncheck('lift (UGX)', lift, {F['lift']:.4f}, 0.5)\ncheck('standard error of the lift', se, {F['se_lift']:.4f}, 1)\n"
            f"check('interval low end', ci_low, {F['ci_lift'][0]:.4f}, 1)\ncheck('interval high end', ci_high, {F['ci_lift'][1]:.4f}, 1)")
    nb.read('Is zero inside the interval? What does that say about the lift?')
    nb.change('Change 1.96 to 2.58. You now have a 99 percent interval. Is it wider or narrower? Why?')

    # step 3
    nb.step(3, 'The bootstrap', 'Resample each group with replacement, at its own size, and recompute the lift. Repeat 5,000 times.')
    nb.predict('Will the bootstrap interval be close to the formula interval, or very different?')
    nb.code(pick("rng = np.random.default_rng(42)\nboot = np.array([rng.choice(offer, len(offer)).mean() - rng.choice(control, len(control)).mean() for _ in range(5000)])\nboot_se = boot.std(ddof=1)\nboot_low, boot_high = np.percentile(boot, [2.5, 97.5])",
                 'make rng once with seed 42; in a loop of 5000, resample offer then control with rng.choice and keep the difference of the means; then the std and the 2.5 and 97.5 percentiles') +
            ("" if sol else "\nboot_se = boot_low = boot_high = np.nan") +
            f"\nprint(np.round(boot_se), np.round(boot_low), np.round(boot_high))\ncheck('bootstrap standard error', boot_se, {F['boot_se']:.4f}, 100)\n"
            f"check('bootstrap interval low end', boot_low, {F['boot_ci'][0]:.4f}, 150)\ncheck('bootstrap interval high end', boot_high, {F['boot_ci'][1]:.4f}, 150)")
    nb.read('Compare boot_se with se from Step 2. Compare the two intervals.')
    nb.change('Draw plt.hist(boot, bins=30) with a vertical line at the lift. Does the histogram look like a bell?')

    # step 4
    nb.step(4, 'The permutation test', 'Under the null hypothesis the group labels carry no information. Shuffle them 5,000 times and count how often chance gives a gap at least as big as the lift.')
    nb.predict('How many of 5,000 shuffled gaps will be as big as the real lift? Think about the histogram of shuffled gaps.')
    nb.code(pick("values = test['next_month_spend_ugx'].to_numpy()\nis_offer = (test['group'] == 'offer').to_numpy()\nrng = np.random.default_rng(42)\ngaps = []\nfor _ in range(5000):\n    s = rng.permutation(is_offer)\n    gaps.append(values[s].mean() - values[~s].mean())\nhits = (np.abs(gaps) >= abs(lift)).sum()\np_perm = hits / 5000",
                 'shuffle is_offer with rng.permutation 5000 times, keep the gap in mean spend each time; hits = how many gaps are at least as big as the lift (absolute values); p_perm = hits / 5000') +
            ("" if sol else "\nhits = p_perm = np.nan") +
            f"\nprint(hits, p_perm)\ncheck('shuffled gaps as big as the lift', hits, {F['perm_hits']}, 3)\ncheck('permutation p-value', p_perm, {F['p_perm']}, 0.001)")
    nb.read('What does the p-value say? What does it NOT say?')
    nb.change('Count only gaps at least as big as the lift in the positive direction. How does the p-value change? Which version is a one-sided test?')

    # step 5
    nb.step(5, 'The Welch t-test and the test of two proportions', 'First by hand, then with SciPy and statsmodels. The numbers should agree.')
    nb.predict('The t statistic is the lift divided by its standard error. Roughly what value do you expect, given the interval you found?')
    nb.code(pick("t_hand = lift / se\nres = stats.ttest_ind(offer, control, equal_var=False)\nt_stat, p_t = res.statistic, res.pvalue\nprint(round(t_hand, 3), round(t_stat, 3), round(p_t, 5))",
                 't_hand = lift / se; res = stats.ttest_ind(offer, control, equal_var=False); take res.statistic and res.pvalue') +
            ("" if sol else "\nt_hand = t_stat = p_t = np.nan") +
            f"\ncheck('t statistic (SciPy)', t_stat, {F['t']:.4f}, 0.001)\ncheck('t by hand equals SciPy', t_hand - t_stat, 0, 0.001)\ncheck('Welch p-value', p_t, {F['p_t']:.6f}, 0.00005)")
    nb.read('Does the t-test p-value agree with the permutation p-value? Both are small. Which is more precise: p_t or p_perm?')
    nb.predict('Did more offer customers come back within 30 days (returned_within_30d)? Will the test find a real gap?')
    nb.code(pick("counts = [test[test['group'] == 'offer']['returned_within_30d'].sum(), test[test['group'] == 'control']['returned_within_30d'].sum()]\nnobs = [len(offer), len(control)]\nz_stat, p_z = proportions_ztest(counts, nobs)\nprint(counts, nobs, round(z_stat, 3), round(p_z, 3))",
                 'counts of returners in offer then control; nobs = group sizes; proportions_ztest(counts, nobs)') +
            ("" if sol else "\nz_stat = p_z = np.nan") +
            f"\ncheck('z statistic', z_stat, {F['z']:.4f}, 0.01)\ncheck('p-value of the two-proportion test', p_z, {F['p_z']:.4f}, 0.005)")
    nb.read('Is p_z below 0.05? Does the data show the offer brings customers back?')
    nb.change('Change the proportion test to compare ONLY the first 500 customers of each group. What happens to the p-value, and why?')

    # step 6
    nb.step(6, 'Effect size, and the decision note', 'A small p-value says the gap is real. The effect size says how big it is. Practical significance asks whether that size matters.')
    nb.predict("Cohen's d is the lift divided by the pooled standard deviation. Will it be near 0.1, 0.5 or 1?")
    nb.code(pick("n1, n2 = len(offer), len(control)\nsd_pooled = np.sqrt(((n1 - 1) * offer.var(ddof=1) + (n2 - 1) * control.var(ddof=1)) / (n1 + n2 - 2))\ncohens_d = lift / sd_pooled\nlift_pct = lift / control.mean() * 100",
                 "the pooled standard deviation, then Cohen's d = lift / sd_pooled, and the lift as a percent of the control mean") +
            ("" if sol else "\ncohens_d = lift_pct = np.nan") +
            f"\nprint(round(cohens_d, 3), round(lift_pct, 1))\ncheck(\"Cohen's d\", cohens_d, {F['d']:.4f}, 0.005)\ncheck('lift as percent of the control mean', lift_pct, {F['lift_pct']:.3f}, 0.05)")
    nb.read('Where does your d sit against the usual guide (0.2 small, 0.5 medium, 0.8 large)? Is it above the small mark?')
    nb.code((f"note = ('The offer raised next-month spend by {F['lift']:,.0f} UGX per customer (95 percent interval {F['ci_lift'][0]:,.0f} to {F['ci_lift'][1]:,.0f}; Welch t-test p = {F['p_t']:.5f}). '\n"
             f"        'The effect is small (Cohen d = {F['d']:.2f}, {F['lift_pct']:.1f} percent of the control mean). It did not detect a change in the share who came back (p = {F['p_z']:.2f}). '\n"
             "        'Limit: one month of spend for 2,500 loyalty customers; the offer cost is not in the data.')\nprint(note)") if sol else
            "note = 'Your turn: write three sentences for a manager. Give the lift, its interval, the p-value, the effect size, and one limit.'\nprint(note)")
    nb.code("check('decision note has numbers', any(ch.isdigit() for ch in note) and 'Your turn' not in note, 1)")
    nb.change('Suppose the offer costs 3,000 UGX per customer and the shop keeps 20 percent of each extra shilling spent (both hypothetical). Compute 0.20 * lift - 3000. Is it a gain or a loss? What about 0.20 * ci_high - 3000?')

    # step 7
    nb.step(7, 'False positives: fake tests and many tests', 'Split the control group at random into two halves. The true gap is zero, so every p-value below 0.05 is a false positive (Type I error).')
    nb.predict('Out of 100 such fake tests, how many will have p below 0.05?')
    nb.code(pick("rng = np.random.default_rng(42)\nalarms = 0\nfor _ in range(100):\n    idx = rng.permutation(len(control))\n    a, b = control[idx[:627]], control[idx[627:]]\n    if stats.ttest_ind(a, b, equal_var=False).pvalue < 0.05:\n        alarms += 1\nfamily = 1 - 0.95 ** 20\nprint(alarms, round(family, 3))",
                 'rng with seed 42; 100 times: permute the control indices, split at 627, Welch t-test the halves, count p below 0.05; family = chance of at least one false alarm in 20 tests') +
            ("" if sol else "\nalarms = family = np.nan") +
            f"\ncheck('false alarms in 100 fake tests', alarms, {len(F['aa_alarms'])}, 3)\ncheck('chance of at least one false alarm in 20 tests', family, {F['family'][20]:.4f}, 0.001)\nshow_checks()")
    nb.read('About 5 of 100 fake tests raised an alarm. What happens to the chance of at least one false alarm when you run 20 tests? What would the Bonferroni cut-off be for 20 tests?')
    nb.change('Extra, if time allows: peeking. Repeat the 100 fake tests, but look at the p-value after every batch of 100 customers in each half and stop at the first p below 0.05. Skeleton: for k in range(100, 628, 100): test a[:k] against b[:k]. Does the false alarm rate stay near 5 percent?')
    nb.md('**You keep this notebook.** Save a copy to your Drive or download it as .ipynb. It holds the offer test done five ways and a decision note. Next session: regression.')
    return nb
