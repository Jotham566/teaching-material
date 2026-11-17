"""Session 6 lab notebook: Decisions, repeats and functions. Expected numbers come from content/s06.py (pandas on the real orders.csv)."""
import importlib.util
from pathlib import Path

import nb as NB

TITLE = 'Decisions, repeats and functions'
_p = Path(__file__).resolve().parents[1] / 's06.py'
_spec = importlib.util.spec_from_file_location('s06_session', _p)
_m = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_m)
N = _m.lab_numbers()
T, C = N['totals'], N['counts']


def build(solution: bool) -> NB.Notebook:
    nb = NB.Notebook()
    nb.md('# Session 6: Decisions, repeats and functions\n\n**Question of the day:** how do we make Python decide and repeat, so we never copy a formula down thousands of rows?\n\n'
          'The rule we code is the Lakeside Mart loyalty policy: **1 point for every UGX 1,000 spent. Silver starts at 2,000 points in 12 months and Gold at 6,000 points.** Everyone else is Basic.\n\n'
          'Work top to bottom. In every step: **predict**, **run**, **read** the output, **change one thing**. Cells marked `your code here` are yours to fill in. The check line prints OK or NOT YET.\n\n'
          'What you keep: this notebook with a tested `loyalty_tier` function, saved with *File, Save a copy in Drive*.')
    nb.data_setup()
    nb.check_setup()

    # step 1
    nb.step(1, 'Write the function', 'A function is a named set of steps. The parameter `spend_ugx` is the name for the value that comes in. `return` sends the answer back. The docstring says what it does.')
    nb.predict('A customer spent 2,388,850 UGX in 12 months. How many points is that, and which tier should the function return? Work it out by hand first.')
    if solution:
        nb.code('def loyalty_tier(spend_ugx):\n    """Return Basic, Silver or Gold."""\n    points = spend_ugx // 1000   # one point for every UGX 1,000\n'
                '    if points >= 6000:\n        return "Gold"\n    elif points >= 2000:\n        return "Silver"\n    else:\n        return "Basic"\n\nprint(loyalty_tier(2388850))\n'
                'check("46,660 UGX is Basic", loyalty_tier(46660) == "Basic", True)\ncheck("2,388,850 UGX is Silver", loyalty_tier(2388850) == "Silver", True)\ncheck("7,500,000 UGX is Gold", loyalty_tier(7500000) == "Gold", True)')
    else:
        nb.code('def loyalty_tier(spend_ugx):\n    """Return Basic, Silver or Gold."""\n    # your code here: points = the spend divided by 1000, keeping the whole part (use //)\n'
                '    # your code here: if points is 6000 or more, return "Gold"; elif 2000 or more, return "Silver"; else return "Basic"\n    return None\n\nprint(loyalty_tier(2388850))\n'
                'check("46,660 UGX is Basic", loyalty_tier(46660) == "Basic", True)\ncheck("2,388,850 UGX is Silver", loyalty_tier(2388850) == "Silver", True)\ncheck("7,500,000 UGX is Gold", loyalty_tier(7500000) == "Gold", True)')
    nb.read('Does the function print the tier or return it? Run `result = loyalty_tier(2388850)` and `print(result)` to see the difference.')
    nb.predict('A Boolean expression gives True or False. With points = 2450, what does `points >= 2000 and points < 6000` give? And with points = 6000?')
    if solution:
        nb.code('points = 2450\nis_silver_band = points >= 2000 and points < 6000\nprint(is_silver_band)\npoints = 6000\nis_silver_band_6000 = points >= 2000 and points < 6000\nprint(is_silver_band_6000)\n'
                'check("2,450 points is in the Silver band", is_silver_band is True, True)\ncheck("exactly 6,000 points is not", is_silver_band_6000 is False, True)')
    else:
        nb.code('points = 2450\nis_silver_band = None   # your code here: points >= 2000 and points < 6000\nprint(is_silver_band)\npoints = 6000\nis_silver_band_6000 = None   # your code here: the same test with points = 6000\nprint(is_silver_band_6000)\n'
                'check("2,450 points is in the Silver band", is_silver_band is True, True)\ncheck("exactly 6,000 points is not", is_silver_band_6000 is False, True)')
    nb.change('In `loyalty_tier`, change `>= 2000` to `> 2000`. Which input would now give a wrong tier? (Write it down, then change it back.)')

    # step 2
    nb.step(2, 'Test the edges with assert', 'An edge case (boundary value) sits exactly where a rule changes. A test case pairs an input with the output you expect. `assert` stops with an AssertionError when a test fails.')
    nb.predict('Which of the five test cases would fail if someone wrote `>` instead of `>=`?')
    tests = N['tests']
    tl = ',\n    '.join(f'({s}, "{e}")' for s, e in tests)
    if solution:
        nb.code(f'tests = [\n    {tl},\n]\nfailures = []\nfor spend, expected in tests:\n    got = loyalty_tier(spend)\n    if got != expected:\n        failures.append((spend, expected, got))\n'
                'print(len(failures), "failures")\n'
                'check("five test cases", len(tests), 5)\ncheck("no failures", len(failures), 0)')
        nb.md('**Optional: stop at the first failure.** An `assert` stops with an AssertionError at the first test that fails. Run this cell once your tests pass.')
        nb.code('try:\n    for spend, expected in tests:\n        assert loyalty_tier(spend) == expected, f"{spend} should be {expected}"\n    print("All", len(tests), "tests pass")\nexcept AssertionError as problem:\n    print("AssertionError, the first failing test:", problem)')
    else:
        nb.code(f'tests = [\n    (0, "Basic"),\n    # your code here: add the other four pairs (spend, expected tier): 1,999,999 / exactly 2,000,000 / 5,999,999 / exactly 6,000,000\n]\n'
                'failures = []\nfor spend, expected in tests:\n    got = loyalty_tier(spend)\n    if got != expected:\n        failures.append((spend, expected, got))\n'
                'print(len(failures), "failures")\nfor f in failures:\n    print("  fails:", f)\n'
                'check("five test cases", len(tests), 5)\ncheck("no failures", len(failures) if len(tests) == 5 else None, 0)')
    if not solution:
        nb.md('**Optional: stop at the first failure.** An `assert` stops with an AssertionError at the first test that fails. Run the next cell once your function and tests are finished.')
        nb.code('try:\n    for spend, expected in tests:\n        assert loyalty_tier(spend) == expected, f"{spend} should be {expected}"\n    print("All", len(tests), "tests pass")\nexcept AssertionError as problem:\n    print("AssertionError, the first failing test:", problem)')
    nb.change('Add a sixth test case of your own, for a spend of 1 UGX. What tier do you expect? Run it.')

    # step 3
    nb.step(3, 'Total each customer in a loop', 'An accumulator is a variable that starts at 0 and collects a result as the loop goes round. `orders_2025` holds the real 2025 order values of six customers from `orders.csv`. '
            'The file is a 5 percent sample of till transactions, so these totals are far below real annual spending.')
    nb.predict('Customer C1322 has three orders. Roughly what will the total be: thousands, hundreds of thousands, or millions of UGX?')
    od = ',\n    '.join(f"'{c}': {v}" for c, v in N['orders'].items())
    dec = f'orders_2025 = {{\n    {od},\n}}\nprint(len(orders_2025), "customers")'
    nb.code(dec)
    if solution:
        nb.code('totals = {}\nfor customer in orders_2025:\n    total = 0   # restart the accumulator for each customer\n    for value in orders_2025[customer]:\n        total = total + value\n    totals[customer] = total\nprint(totals)\n'
                'grand_total = sum(totals.values())\n'
                'check("C0009 total", totals["C0009"], %d)\ncheck("C1322 total", totals["C1322"], %d)\ncheck("all six together", grand_total, %d)' % (T['C0009'], T['C1322'], N['grand']))
    else:
        nb.code('totals = {}\nfor customer in orders_2025:\n    # your code here: start total at 0, add each order value of this customer, then store it in totals[customer]\n    pass\nprint(totals)\n'
                'grand_total = sum(totals.values()) if totals else None\n'
                'check("C0009 total", totals.get("C0009"), %d)\ncheck("C1322 total", totals.get("C1322"), %d)\ncheck("all six together", grand_total, %d)' % (T['C0009'], T['C1322'], N['grand']))
    nb.read('Why must `total = 0` sit inside the for loop (indented under the `for customer` line), and not above it? Try moving it above and read the totals.')

    # step 4
    nb.step(4, 'Apply the function to every customer', 'One loop and one function: the loop repeats the work, the function holds the rule.')
    nb.predict('Before you run: how many of the six customers do you expect in Basic, Silver and Gold? Use the table of totals you printed.')
    if solution:
        nb.code("tiers = {}\ncounts = {'Basic': 0, 'Silver': 0, 'Gold': 0}\nfor customer in totals:\n    tier = loyalty_tier(totals[customer])\n    tiers[customer] = tier\n    counts[tier] = counts[tier] + 1\nprint(tiers)\nprint(counts)\n"
                'check("Basic customers", counts["Basic"], %d)\ncheck("Silver customers", counts["Silver"], %d)\ncheck("Gold customers", counts["Gold"], %d)' % (C['Basic'], C['Silver'], C['Gold']))
    else:
        nb.code("tiers = {}\ncounts = {'Basic': 0, 'Silver': 0, 'Gold': 0}\nfor customer in totals:\n    # your code here: call loyalty_tier on the total, store it in tiers[customer], and add 1 to counts for that tier\n    pass\nprint(tiers)\nprint(counts)\n"
                'check("Basic customers", counts["Basic"], %d)\ncheck("Silver customers", counts["Silver"], %d)\ncheck("Gold customers", counts["Gold"], %d)' % (C['Basic'], C['Silver'], C['Gold']))
    nb.change('Change the Silver boundary in `loyalty_tier` from 2000 to 2500 points and run steps 1 to 4 again. Which customers change tier? Change it back.')

    # step 5
    nb.step(5, 'Read and trace a colleague\'s function', 'The function below was written by a colleague. It should return Gold for 7,500,000 UGX. Trace it by hand with that value, then write a corrected `tier_v2`.')
    nb.code('def tier_v1(spend_ugx):\n    points = spend_ugx // 1000\n    if points >= 2000:\n        return "Silver"\n    elif points >= 6000:\n        return "Gold"\n    else:\n        return "Basic"\n\nprint(tier_v1(7500000))')
    nb.read('Which line returns first for 7,500 points, and why is the Gold test never reached?')
    if solution:
        nb.code('def tier_v2(spend_ugx):\n    """Return Basic, Silver or Gold for a 12-month spend in UGX (Gold is tested first)."""\n    points = spend_ugx // 1000\n    if points >= 6000:\n        return "Gold"\n    elif points >= 2000:\n        return "Silver"\n    else:\n        return "Basic"\n\n'
                'v1_failures = [s for s, e in tests if tier_v1(s) != e]\nprint("tier_v1 fails", len(v1_failures), "of", len(tests), "test cases")\n'
                'check("tier_v1 gives Silver for 7,500,000", tier_v1(7500000) == "%s", True)\ncheck("tier_v2 passes every test", all(tier_v2(s) == e for s, e in tests), True)' % N['v1_7_5m'])
    else:
        nb.code('def tier_v2(spend_ugx):\n    # your code here: the corrected function, with a docstring\n    return None\n\n'
                'v1_failures = [s for s, e in tests if tier_v1(s) != e]\nprint("tier_v1 fails", len(v1_failures), "of", len(tests), "test cases")\n'
                'check("tier_v1 gives Silver for 7,500,000", tier_v1(7500000) == "%s", True)\ncheck("tier_v2 passes every test", all(tier_v2(s) == e for s, e in tests), True)' % N['v1_7_5m'])
    nb.change('Add `(7500000, "Gold")` to `tests` and count the failures of `tier_v1` again. Does the extra test case find more faults?')
    nb.change('Stretch: the policy says points expire after 12 months. Which input would you need to add to `loyalty_tier` to enforce that? Write it down.')

    # step 6
    nb.step(6, 'A spend that arrives as text', 'From Session 5: a string with commas is not a number. Clean it, convert it, then call the function.')
    nb.predict('What will `loyalty_tier("2,388,850")` do? Which exception, and what does its last line say?')
    if solution:
        nb.code('spend_text = "2,388,850"\nspend_clean = int(spend_text.replace(",", ""))   # remove the commas, then convert to an int\nprint(spend_clean, loyalty_tier(spend_clean))\n'
                'check("cleaned spend", spend_clean, %d)\ncheck("its tier is Silver", loyalty_tier(spend_clean) == "%s", True)' % (N['clean_text'], N['tiers']['C1322']))
    else:
        nb.code('spend_text = "2,388,850"\nspend_clean = None   # your code here: remove the commas with replace, then convert with int()\nprint(spend_clean)\n'
                'check("cleaned spend", spend_clean, %d)\ncheck("its tier is Silver", loyalty_tier(spend_clean) == "%s" if spend_clean else False, True)' % (N['clean_text'], N['tiers']['C1322']))
    nb.md('**Optional: ask a free chat assistant** to list edge cases for `loyalty_tier`. Add each suggestion as a test case with an expected answer worked out from the policy. Your own tests decide whether its suggestion is right. '
          'Never paste personal or confidential data.\n\n> What it suggested, and what my tests said: ')
    nb.md('## Compare with a sheet\n\nPut the six totals in cells A2 to A7 of a Google Sheet. In B2 write `=IF(A2>=6000000,"Gold",IF(A2>=2000000,"Silver","Basic"))` and fill down. Do the six tiers match `tiers`? '
          'If the policy moved Silver to 2,500 points, which version is quicker to change, and why?\n\n> My comparison: ')
    nb.code('show_checks()')
    return nb
