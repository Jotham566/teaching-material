"""Session 1: a small colour image made by this script (own work, no licence issue): sunrise over a hill, 8 x 8 pixels.
Every pixel is three numbers (red, green, blue), each 0 to 255.  Run: python rgb_image.py  -> rgb_image.npy and the numbers below."""
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent
img = np.zeros((8, 8, 3), dtype=int)
for r in range(8):                                   # sky: pale gold at the horizon to blue at the top
    t = r / 5.0
    img[r, :] = [int(80 + 160 * min(t, 1)), int(130 + 90 * min(t, 1)), int(220 - 150 * min(t, 1))]
img[2:4, 3:5] = [224, 190, 54]                       # the sun (gold)
img[3, 3:5] = [230, 120, 40]
for c in range(8):                                   # a dark green hill rising to the right
    top = 6 - (1 if c > 3 else 0) - (1 if c > 5 else 0)
    img[top:, c] = [30, 90, 40]
np.save(HERE / 'rgb_image.npy', img)
print('shape', img.shape, '= 8 x 8 pixels x 3 numbers =', img.size, 'numbers')
for (r, c) in [(0, 0), (2, 3), (7, 6)]:
    print(f'pixel row {r} col {c}: (R,G,B) = {tuple(int(v) for v in img[r, c])}')
print('all rows (R,G,B):')
for r in range(8):
    print(r, [tuple(int(v) for v in img[r, c]) for c in range(8)])
print('a 1000 x 1000 pixel photo has', 1000 * 1000 * 3, 'numbers')
