"""KLAi brand constants for the camp slides, figures and PDFs.

The KLAi logo is black and white with a red dot and a gold A. The brand font is Lato.
Red (#AE2525) marks what needs attention. Gold (#E0BE36) marks the thing to look at; it has weak
contrast on white (about 1.8:1), so it is used as a fill behind black text or on black, and never
as text on white. Everything else is black, greys and white.

Design rules (also in ../../brand/BRAND.md):
  hairline outlines and type, almost no tinted fill; one idea per slide; titles state the finding;
  no kicker labels above titles, no numbered step cards, no accent stripes or lines under titles,
  no repeated stat-tile rows; every concept slide carries a drawn figure.
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
CAMP = HERE.parents[1]
BRAND_DIR = CAMP / 'brand'
FONT_DIR = BRAND_DIR / 'fonts'
LOGO_ON_BLACK = BRAND_DIR / 'logos' / 'klai_logo_on_black_cropped.png'
LOGO_ON_WHITE = BRAND_DIR / 'logos' / 'klai_logo_on_white_cropped.png'
FIG_DIR = CAMP / 'figures'

INK = '#111111'
BODY = '#333333'
MUTE = '#666666'
GREY = '#8C8C8C'
HAIR = '#CFCFCF'
PALE = '#F1F1F1'      # used only inside figures for a quiet fill behind data, never as a slide panel
PAPER = '#FFFFFF'
RED = '#AE2525'
GOLD = '#E0BE36'
BLACK = '#000000'

HEAD_FONT = 'Lato'
BODY_FONT = 'Lato'
MONO_FONT = 'Courier New'

# slide geometry (inches), 16:9
SW, SH = 13.333, 7.5
MARGIN_X = 0.7
TITLE_Y, TITLE_H = 0.42, 1.15
BODY_Y = 1.75
BODY_H = 5.05
FOOT_Y = 7.05
