"""Holiday Data and AI Camp, revision 2: loader for the authored lessons.

Lessons live in lessons/da.py (Python for Data Analysis, assembled from four week files) and
lessons/ml.py (Machine Learning, labs and the optional extension). The schema and shared
constants and paths are in common.py.
"""
from common import ROOT, ROADMAP, TRACK_NAMES  # noqa: F401
from lessons.da import DA  # noqa: F401
from lessons.ml import ML, LABS, EXTENSION  # noqa: F401

assert len(ML) == len(DA) == 24
assert len(LABS) == 4
