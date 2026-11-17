"""Approved illustration assets: the PNGs the decks are built from.

Normal builds do NOT draw pictures. add_illustrations.py reads the PNGs in approved/ and checks each against
Approved Assets.json, so the same bytes reach every deck on every machine. (Drawing with Pillow can differ by a
few edge pixels between Pillow and FreeType versions, which is why drawing is a separate, deliberate step.)

  python3 approve_illustrations.py render      draw every motif and title scene in the plan with Pillow, write them to
                                               approved/ and rewrite Approved Assets.json. Run this only when you change
                                               illustrations.py or illustration_plan.json, then look at the result,
                                               rebuild, compare and commit the PNGs with the manifest.
  python3 approve_illustrations.py drift       draw fresh into a temporary folder and report how far each differs from the
                                               approved PNG on this machine (informational; changes nothing).
  python3 approve_illustrations.py extract DECKS_FOLDER
                                               adopt the pictures already in a folder of decks as the approved assets
                                               (used once, in October 2026, to approve the pictures in the live decks).
"""
import sys, json, hashlib, tempfile
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
APPROVED = HERE / 'approved'; MANIFEST = HERE / 'Approved Assets.json'

def plan(): return json.loads((HERE / 'illustration_plan.json').read_text(encoding='utf-8'))
def sha(b): return hashlib.sha256(b).hexdigest()

def wanted():
    """File name -> what it is, for every picture the plan needs."""
    out = {}
    for e in plan():
        if e['kind'] == 'hero': out[f"hero_{e['session']:02d}.png"] = {'kind': 'hero', 'session': e['session'], 'motifs': e['motifs']}
        elif e['kind'] == 'side': out[f"{e['motif']}.png"] = {'kind': 'motif', 'motif': e['motif']}
    return out

def write_manifest(note):
    import PIL
    files = {}
    for name, what in sorted(wanted().items()):
        files[name] = dict(what, sha256=sha((APPROVED / name).read_bytes()))
    MANIFEST.write_text(json.dumps({'about': note, 'drawn_with_pillow': PIL.__version__, 'files': files}, indent=1, ensure_ascii=False), encoding='utf-8')
    print('manifest written:', len(files), 'assets')

def render_all(folder):
    import illustrations as ill
    folder.mkdir(parents=True, exist_ok=True)
    for name, what in wanted().items():
        if what['kind'] == 'hero': ill.hero(folder / name, what['motifs'])
        else: ill.render(what['motif'], ill.LIGHT, folder / name)

def cmd_render():
    render_all(APPROVED)
    write_manifest('Drawn by approve_illustrations.py render. Edit illustrations.py or illustration_plan.json, run render, inspect, then commit the PNGs and this file.')

def cmd_drift():
    from PIL import Image, ImageChops
    with tempfile.TemporaryDirectory() as t:
        t = Path(t); render_all(t); worst = 0
        for name in sorted(wanted()):
            a, b = Image.open(APPROVED / name).convert('RGBA'), Image.open(t / name).convert('RGBA')
            if a.size != b.size: print(name, 'SIZE DIFFERS'); continue
            d = ImageChops.difference(a, b).convert('L'); strong = sum(1 for p in d.getdata() if p > 96) / (a.size[0] * a.size[1])
            worst = max(worst, strong)
            if strong: print(f'{name}: {strong * 100:.4f}% of pixels differ strongly')
        print('worst drift', f'{worst * 100:.4f}%', '(0 means this machine draws the approved pictures exactly)')

def cmd_extract(folder):
    from pptx import Presentation
    pm = {(e['session'], e['slide']): e for e in plan()}; seen = {}
    APPROVED.mkdir(exist_ok=True)
    for f in sorted(Path(folder).glob('[0-1][0-9] - *.pptx')):
        n = int(f.name[:2])
        for i, sl in enumerate(Presentation(str(f)).slides, 1):
            e = pm.get((n, i))
            if not e or e['kind'] not in ('hero', 'side'): continue
            for sh in sl.shapes:
                if sh.shape_type == 13 and sh.name.startswith('illustration-') and not sh.name.startswith('illustration-shot'):
                    name = f"hero_{n:02d}.png" if e['kind'] == 'hero' else f"{e['motif']}.png"
                    blob = sh.image.blob
                    if name in seen and seen[name] != sha(blob): sys.exit(f'{name} differs between slides; cannot adopt')
                    seen[name] = sha(blob); (APPROVED / name).write_bytes(blob)
    missing = set(wanted()) - set(seen)
    if missing: sys.exit(f'plan needs pictures not found in the decks: {sorted(missing)[:5]}')
    write_manifest('Adopted from the live decks on 27 October 2026 (drawn by illustrations.py with the Pillow version below). Approved assets are the pictures teachers see.')

if __name__ == '__main__':
    c = sys.argv[1] if len(sys.argv) > 1 else ''
    if c == 'render': cmd_render()
    elif c == 'drift': cmd_drift()
    elif c == 'extract' and len(sys.argv) > 2: cmd_extract(sys.argv[2])
    else: print(__doc__)
