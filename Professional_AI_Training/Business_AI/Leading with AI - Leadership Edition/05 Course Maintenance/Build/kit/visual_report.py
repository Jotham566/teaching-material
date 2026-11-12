"""How many slides carry a real visual? Run from Build/ after kit/deck.py. Counts diagram images (x_*), pictogram rows (3 or more icons) and tables with icons."""
import json, glob, collections
from pathlib import Path
tot = collections.Counter()
for f in sorted(glob.glob(str(Path(__file__).resolve().parent.parent / '_specs' / '[0-9][0-9]_-_*.json'))):
    d = json.load(open(f)); n = Path(f).name[:2]; c = collections.Counter(); bad = []
    for i, s in enumerate(d['slides'], 1):
        paths = [o['path'].split('/')[-1] for o in s['objects'] if o['type'] == 'image']
        icons = [p for p in paths if p.startswith('icon_')]
        if s['layout'] == 'dark': cls = 'cover'
        elif any(p.startswith('x_') for p in paths): cls = 'diagram'
        elif len(icons) >= 3: cls = 'icon rows'
        elif icons: cls = 'one icon'
        else: cls = 'text only'; bad.append(i)
        c[cls] += 1; tot[cls] += 1
    print(n, dict(c), 'text-only slides:', bad)
print(dict(tot))
