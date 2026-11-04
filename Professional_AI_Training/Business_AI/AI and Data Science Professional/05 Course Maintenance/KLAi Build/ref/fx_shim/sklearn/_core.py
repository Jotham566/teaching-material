"""A small shim of the scikit-learn pieces that the Session 14, 15 and 16 notebooks use, built on content/loans_canon.py (NumPy replicas of the split, the scaled L2 logistic regression and the CART tree).
It exists ONLY to prove that the notebook cells run in order and that the learner version prints NOT YET instead of stopping. Because the shim calls the same functions that produced the expected numbers,
agreement of the numbers is NOT evidence about real scikit-learn. Re-run the solution notebooks on real scikit-learn in Colab."""
import copy
import sys
from pathlib import Path

import numpy as np
import pandas as pd

BUILD = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(BUILD / 'content'))
import loans_canon as C  # noqa: E402
import h_loans as H  # noqa: E402


def arr(X):
    return np.asarray(X, float)


def take(a, idx):
    return a.iloc[idx] if hasattr(a, 'iloc') else np.asarray(a)[idx]


def sigmoid(z):
    return 1 / (1 + np.exp(-z))
