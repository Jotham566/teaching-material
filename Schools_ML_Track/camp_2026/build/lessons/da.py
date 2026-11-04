"""Python for Data Analysis: all 24 sessions, assembled from the week files."""
from .da_weeks_1_2 import W1
from .da_weeks_3_4 import W2
from .da_weeks_5_6 import W3
from .da_weeks_7_8 import W4

DA = W1 + W2 + W3 + W4
assert len(DA) == 24

from .hooks import HOOKS_DA  # noqa: E402
assert len(HOOKS_DA) == 24
for _l, _h in zip(DA, HOOKS_DA):
    _l['hook'] = _h
