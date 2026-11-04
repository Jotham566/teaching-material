"""Shared constants and helpers for the KLAi template generators."""
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
BUILD = HERE.parent
EDITION = BUILD.parent
LOGO = BUILD / 'brand' / 'logos' / 'klai_logo_on_black_cropped.png'

FONT = 'Lato'
BLACK = '000000'
WHITE = 'FFFFFF'
RED = 'AE2525'
GOLD = 'E0BE36'
GREY = '767676'      # example text (4.5:1 on white)
HAIR = 'BFBFBF'      # hairline borders
FOOT = 'KLAi | IUEA Machine Learning for Engineers | '

LOGO_W, LOGO_H = Image.open(LOGO).size
