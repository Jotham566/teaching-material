"""Tests for picture handling:  python3 test_compare_edition.py
1 Comparison is exact for every image: evidence images, scans, screenshots and generated illustrations.
2 Regression with the actual Session 12 title illustration (ppt/media/image1.png in deck 12): a drift of 0.1221 percent
  of pixels, the size seen between two machines' drawings, is a difference in a comparison, so builds must not draw.
3 The live deck pictures are the approved assets, byte for byte, and re-running the illustration step on the
  live Session 12 deck reproduces the deck exactly."""
import io, shutil, subprocess, sys, tempfile, zipfile
from pathlib import Path
from PIL import Image, ImageDraw
sys.path.insert(0, str(Path(__file__).resolve().parent))
import compare_edition as ce

LIVE = ce.LIVE / '02 Class Slides'; AUTH = Path(__file__).resolve().parents[1]

def rewrite(src, dst, edit):
    with zipfile.ZipFile(src) as zi, zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as zo:
        for it in zi.infolist(): zo.writestr(it, edit(it.filename, zi.read(it.filename)))

def mark(data, size=14):
    im = Image.open(io.BytesIO(data)).convert('RGBA'); ImageDraw.Draw(im).rectangle([5, 5, 5 + size, 5 + size], fill=(0, 0, 0, 255)); b = io.BytesIO(); im.save(b, 'PNG'); return b.getvalue()

def drift(data, fraction):
    """Change `fraction` of the pixels strongly, spread evenly (as a renderer difference would along edges)."""
    im = Image.open(io.BytesIO(data)).convert('RGBA'); px = im.load(); w, h = im.size; total = w * h; target = int(total * fraction); step = max(1, total // target); n = 0
    for k in range(0, total, step):
        x, y = k % w, k // w; r, g, b, a = px[x, y]; px[x, y] = (255 - r, 255 - g, 255 - b, a) if (r, g, b) != (255 - r, 255 - g, 255 - b) else (0, 0, 0, a); n += 1
    out = io.BytesIO(); im.save(out, 'PNG'); return out.getvalue()

def run():
    fails = 0
    def expect(name, got, want):
        nonlocal fails; ok = got == want; fails += not ok; print(('PASS ' if ok else 'FAIL ') + name)
    deck5 = next(LIVE.glob('05 - *.pptx')); deck12 = next(LIVE.glob('12 - *.pptx'))
    with tempfile.TemporaryDirectory() as t:
        t = Path(t)
        with zipfile.ZipFile(deck5) as z: big = max((n for n in z.namelist() if n.startswith('ppt/media/') and n.lower().endswith('.png')), key=lambda n: z.getinfo(n).file_size)
        a = t / 'evidence_mark.pptx'; rewrite(deck5, a, lambda n, d: mark(d) if n == big else d)
        expect('a small black mark on an image in deck 05 is a difference', ce.decks_equal(deck5, a), False)
        f = t / 'same.pptx'; shutil.copy(deck5, f)
        expect('identical decks are equal', ce.decks_equal(deck5, f), True)
        # Session 12 title illustration
        with zipfile.ZipFile(deck12) as z: image1 = z.read('ppt/media/image1.png')
        im = Image.open(io.BytesIO(image1)); print(f'     Session 12 image1.png {im.size[0]}x{im.size[1]}')
        d = t / 's12_drift.pptx'; rewrite(deck12, d, lambda n, x: drift(x, 0.001221) if n == 'ppt/media/image1.png' else x)
        expect('Session 12 image1.png drifting by 0.1221 percent of pixels is a difference', ce.decks_equal(deck12, d), False)
        # live pictures are the approved assets
        import json, hashlib
        man = json.loads((AUTH / 'Illustrations/Approved Assets.json').read_text(encoding='utf-8'))['files']
        approved = AUTH / 'Illustrations/approved'
        expect('Session 12 title picture equals approved hero_12.png byte for byte', image1 == (approved / 'hero_12.png').read_bytes(), True)
        expect('hero_12.png matches its manifest hash', hashlib.sha256(image1).hexdigest() == man['hero_12.png']['sha256'], True)
        # rebuild the pictures on the live deck 12 in a scratch folder and compare
        s = t / 'decks'; s.mkdir(); shutil.copy(deck12, s / deck12.name)
        r = subprocess.run([sys.executable, str(AUTH / 'Illustrations/add_illustrations.py'), str(s)], capture_output=True, text=True)
        expect('the illustration step runs on the live Session 12 deck', r.returncode, 0)
        expect('re-running the illustration step reproduces the live Session 12 deck exactly', ce.decks_equal(deck12, s / deck12.name), True)
    return fails

if __name__ == '__main__':
    sys.exit(1 if run() else 0)
