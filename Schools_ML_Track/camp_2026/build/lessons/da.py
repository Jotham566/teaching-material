"""Python for Data Analysis: all 24 sessions, assembled from the week files."""
from .da_weeks_1_2 import W1
from .da_weeks_3_4 import W2
from .da_weeks_5_6 import W3
from .da_weeks_7_8 import W4

DA = W1 + W2 + W3 + W4
assert len(DA) == 24
