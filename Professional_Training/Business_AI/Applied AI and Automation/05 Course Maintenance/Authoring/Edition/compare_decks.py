"""Compare two folders of decks part by part (canonical XML, media bytes).
Usage: python3 compare_decks.py FOLDER_A FOLDER_B
Ignores docProps (timestamps). Exit code 1 when anything differs."""
import sys, zipfile, hashlib
from pathlib import Path
from lxml import etree

def parts(path):
    out = {}
    with zipfile.ZipFile(path) as z:
        for n in z.namelist():
            if n.startswith('docProps/'): continue
            data = z.read(n)
            if n.endswith('.xml') or n.endswith('.rels'):
                try: data = etree.tostring(etree.fromstring(data), method='c14n')
                except Exception: pass
            out[n] = hashlib.sha256(data).hexdigest()
    return out

def main(a, b):
    bad = 0
    for f in sorted(Path(a).glob('[0-1][0-9] - *.pptx')):
        g = Path(b) / f.name
        if not g.exists(): print('MISSING', f.name); bad += 1; continue
        pa, pb = parts(f), parts(g)
        diff = sorted(k for k in set(pa) | set(pb) if pa.get(k) != pb.get(k))
        print(f.name[:2], 'identical' if not diff else f'{len(diff)} parts differ: {diff[:6]}')
        bad += bool(diff)
    return 1 if bad else 0

if __name__ == '__main__': sys.exit(main(*sys.argv[1:3]))
