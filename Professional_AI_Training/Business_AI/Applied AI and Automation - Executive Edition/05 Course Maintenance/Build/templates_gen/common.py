"""Shared constants and helpers for the KLAi template generators."""
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
BUILD = HERE.parent
EDITION = BUILD.parent.parent
LOGO = BUILD / 'brand' / 'logos' / 'klai_logo_on_black_cropped.png'
TEMPLATES = EDITION / '03 Learner Materials' / 'Templates'
FOLLOWUP = EDITION / '03 Learner Materials' / 'Follow-up Kit'

FONT = 'Lato'
BLACK = '000000'
WHITE = 'FFFFFF'
RED = 'AE2525'
GOLD = 'E0BE36'
GREY = '767676'      # example text (4.5:1 on white)
HAIR = 'BFBFBF'      # hairline borders
FOOT = 'KLAi | Applied AI and Automation | '

LOGO_W, LOGO_H = Image.open(LOGO).size
