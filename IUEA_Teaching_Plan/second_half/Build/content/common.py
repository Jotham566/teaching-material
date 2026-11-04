"""Shared helpers for the IUEA second-half class files: cohort facts, reference numbers from real data, and the standard automatic-slide fields.

Every number that appears on a slide comes from `ref/week_reference_numpy.py` (NumPy re-implementations of the scikit-learn pieces, checked against
scikit-learn on the lecturer's Mac) run on the cohort's own engineering_data.csv, so a slide never carries a typed result.
"""
import sys
from pathlib import Path

BUILD = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BUILD / 'ref'))
import numpy as np  # noqa: E402
import week_reference_numpy as R  # noqa: E402

COHORTS = {
    'CML3112': dict(b1_close='Tuesday 17 November, 11:00', b2_close='Tuesday 1 December, 11:00', name='CML3112  |  Civil Engineering and Architecture', slot='11:00 to 14:00', room='Room 106', thing='building', short='cooling load', unit='kW',
                    entity='building plant', dates={1: 'Tuesday 3 November 2026', 2: 'Tuesday 10 November 2026', 3: 'Tuesday 17 November 2026', 4: 'Tuesday 24 November 2026'},
                    friday=False, example_input='how hard the plant is working'),
    'CML3113': dict(b1_close='Friday 20 November, 08:00', b2_close='Friday 4 December, 08:00', name='CML3113  |  Mining and Petroleum Engineering', slot='08:00 to 11:00', room='Room 105', thing='crusher', short='crusher energy demand', unit='kWh/t',
                    entity='crusher', dates={1: 'Friday 6 November 2026', 2: 'Friday 13 November 2026', 3: 'Friday 20 November 2026', 4: 'Friday 27 November 2026'},
                    friday=True, example_input='how hard the crusher is working'),
    'CML3111': dict(b1_close='Friday 20 November, 11:00', b2_close='Friday 4 December, 11:00', name='CML3111  |  Electrical, Mechatronics, Robotics and Communications', slot='11:00 to 14:00', room='Room 115', thing='motor', short='motor winding temperature',
                    unit='deg C', entity='motor', dates={1: 'Friday 6 November 2026', 2: 'Friday 13 November 2026', 3: 'Friday 20 November 2026', 4: 'Friday 27 November 2026'},
                    friday=True, example_input='how hard the motor is working'),
}

WEEK_OF_CLASS = {1: 8, 2: 9, 3: 10, 4: 11}


def facts(code):
    """Everything numeric a class needs for one cohort, from the reference module."""
    c = dict(COHORTS[code])
    b = R.bundle(code)
    raw, d, tr, va, te = R.load(code)
    (trf, vaf), med = R.median_fill(tr, [va])
    c.update(code=code, b=b, raw=raw, clean=d, tr=tr, va=va, te=te, trf=trf, vaf=vaf, med=med)
    return c


def fmt(x, n=2):
    return f'{x:.{n}f}'


def gd_steps(n=5, lr=0.05):
    """The five gradient-descent steps on x = 1,2,3 and y = 2,4,6 shown in class (w starts at 0)."""
    x = np.array([1, 2, 3.0])
    y = np.array([2, 4, 6.0])
    w = 0.0
    rows = []
    for k in range(1, n + 1):
        g = 2 * np.mean(x * (w * x - y))
        w = w - lr * g
        rows.append((k, round(float(w), 3), round(float(np.mean((w * x - y) ** 2)), 3)))
    return rows


def tree_node(tree, names, unit, nd=1):
    """Turn the reference tree tuple into the dict the `tree` diagram draws."""
    if tree[0] == 'leaf':
        return {'v': f'{tree[1]:.{nd}f} {unit}'}
    return {'q': f'{names[tree[1]]} <= {tree[2]:.1f}?', 'yes': tree_node(tree[3], names, unit, nd), 'no': tree_node(tree[4], names, unit, nd)}
