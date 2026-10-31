"""Patch the registration flyer PNG in place for the revision 2 wording, without the Codex runtime.

The PNG was exported by a runtime that is not installed everywhere. This script repaints only the
elements whose text or icon changed in layout.json, over the flat background beneath each one, and
leaves every other pixel as exported. It starts from output/previous/School_Track_Registration.png.
Fonts: Liberation Sans, which has Arial's metrics. Re-exporting with the full exporter replaces this.
"""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
R = Path(__file__).resolve().parent.parent
old = Image.open(R / 'output/previous/School_Track_Registration.png').convert('RGB')
new = old.copy(); dr = ImageDraw.Draw(new)
el = {e['name']: e for e in json.loads((R / 'source/layout.json').read_text())['elements']}
S = 2
LIB = '/usr/share/fonts/truetype/'
F = {('Arial', False): LIB + 'liberation2/LiberationSans-Regular.ttf', ('Arial', True): LIB + 'liberation2/LiberationSans-Bold.ttf',
     ('Arial Narrow', False): LIB + 'liberation/LiberationSansNarrow-Regular.ttf', ('Arial Narrow', True): LIB + 'liberation/LiberationSansNarrow-Bold.ttf'}


def redraw(name):
    e = el[name]; x, y, w, h = [int(e[k] * S) for k in 'xywh']
    bg = old.getpixel((x + 4, y + 4)) if e['align'] == 'center' else old.getpixel((x + w - 10, y + 4))
    lines = e['value'].split('\n'); size = e['size']
    fill_h = min(h, int((len(lines) * size * 1.2 + 4) * S))
    dr.rectangle((x, y + 2, x + w, y + fill_h - 2), fill=bg)
    f = ImageFont.truetype(F[(e.get('font', 'Arial'), e['bold'])], size * S)
    for i, line in enumerate(lines):
        base = y + (size * 0.92 + 2 + i * size * 1.2) * S   # +2 matches the exporter's baseline, measured on an unchanged line
        if e['align'] == 'center':
            dr.text((x + w / 2, base), line, font=f, fill=e['color'], anchor='ms')
        else:
            dr.text((x, base), line, font=f, fill=e['color'], anchor='ls')


for n in ['DA description', 'Charts label 349', 'DA learning 2', 'DA learning 4', 'ML learning 5', 'DA project examples', 'ML project examples', 'Outcome 2']:
    redraw(n)
ic = el['Charts logo 349']; x, y, w, h = [int(ic[k] * S) for k in 'xywh']
dr.rectangle((x, y, x + w, y + h), fill=old.getpixel((x - 6, y + 4)))
img = Image.open(R / ic['file']).convert('RGBA'); sc = min(w / img.width, h / img.height)
img = img.resize((max(1, int(img.width * sc)), max(1, int(img.height * sc))), Image.LANCZOS)
new.paste(img, (x + (w - img.width) // 2, y + (h - img.height) // 2), img)
new.save(R / 'output/School_Track_Registration.png')
print('patched PNG')
