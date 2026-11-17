"""Place the illustrations on the class decks.

  python3 add_illustrations.py "<folder with the 12 decks>"

The pictures are the approved PNGs in approved/, checked against Approved Assets.json. Nothing is drawn during a
build, so every machine embeds the same bytes. To change a picture, edit illustrations.py or the plan and run
approve_illustrations.py render (see that file).

The plan is in illustration_plan.json (session, slide, motif). For a content slide the
body text boxes are narrowed to the left 63 percent and the picture goes on the right.
For a title slide a dark-theme scene goes on the right. The script is repeatable: it
removes any picture whose name starts with "illustration-" before adding it again.
Only slides without tables, pictures, diagrams or click animations are touched.
"""
import sys, json, argparse, tempfile
from pathlib import Path
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import illustrations as ill

BODY_RIGHT = 7_850_000           # text boxes end here on illustrated slides
PIC = dict(left=8_050_000, top=1_850_000, size=3_700_000)
HERO = dict(left=6_950_000, top=1_000_000, size=4_700_000)
TITLE_RIGHT = 6_700_000


def clear(slide):
    for sh in list(slide.shapes):
        if sh.name.startswith('illustration-'):
            sh._element.getparent().remove(sh._element)


def two_column(slide):
    """True when body text sits in a second column; such slides keep their layout."""
    return any(sh.has_text_frame and sh.text_frame.text.strip() and sh.left >= 4_000_000 and 1_700_000 <= sh.top < 5_600_000 for sh in slide.shapes)


def _size(sh):
    for p in sh.text_frame.paragraphs:
        for r in p.runs:
            if r.font.size: return r.font.size.pt
    return 24.0


def _fit(sh, avail_h):
    """Shrink the font until the estimated wrapped text fits the space below the shape's top."""
    import math
    text = sh.text_frame.text; size = _size(sh); wpt = sh.width / 12700.0
    def need(s):
        cpl = max(8, int(wpt / (0.50 * s)))
        lines = sum(max(1, math.ceil(len(par) / cpl)) for par in text.split('\n'))
        return lines * s * 1.22 * 12700
    new = size
    while new > 15 and need(new) > avail_h: new -= 1
    if new < size:
        for p in sh.text_frame.paragraphs:
            for r in p.runs: r.font.size = Pt(new)


def narrow(slide, right, top_min, top_max):
    shapes = [sh for sh in slide.shapes if sh.has_text_frame and sh.text_frame.text.strip() and sh.top is not None and top_min <= sh.top < top_max]
    narrowed = []
    for sh in shapes:
        if sh.left + sh.width > right:
            sh.width = Emu(max(right - sh.left, 1_500_000)); narrowed.append(sh)
    below = sorted({s.top for s in slide.shapes if s.has_text_frame and s.text_frame.text.strip() and s.top is not None})
    for sh in narrowed:
        nxt = [t for t in below if t > sh.top + 200_000]
        limit = (nxt[0] if nxt else 6_300_000) - 60_000
        if sh.text_frame.text.strip() in ('01', '02', '03', '04'): continue
        _fit(sh, limit - sh.top)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('decks')
    a = ap.parse_args()
    plan = json.loads((HERE / 'illustration_plan.json').read_text(encoding='utf-8'))
    import hashlib
    man = json.loads((HERE / 'Approved Assets.json').read_text(encoding='utf-8'))['files']
    png = HERE / 'approved'
    for e in plan:
        if e['kind'] not in ('hero', 'side'): continue
        name = f"hero_{e['session']:02d}.png" if e['kind'] == 'hero' else f"{e['motif']}.png"
        rec = man.get(name)
        if rec is None or not (png / name).exists(): sys.exit(f'{name} is in the plan but not approved. Run approve_illustrations.py render.')
        if hashlib.sha256((png / name).read_bytes()).hexdigest() != rec['sha256']: sys.exit(f'{name} differs from Approved Assets.json.')
        if e['kind'] == 'hero' and rec['motifs'] != e['motifs']: sys.exit(f'{name}: the plan now lists {e["motifs"]} but the approved scene was drawn from {rec["motifs"]}. Run approve_illustrations.py render.')
    done = 0
    for f in sorted(Path(a.decks).glob('[0-1][0-9] - *.pptx')):
        n = int(f.name[:2]); prs = Presentation(str(f)); touched = False
        for item in [p for p in plan if p['session'] == n]:
            slide = prs.slides[item['slide'] - 1]; clear(slide)
            if item['kind'] == 'side' and two_column(slide): continue
            if item['kind'] == 'shot':
                from PIL import Image as _I
                shot = HERE / 'screenshots' / item['file']
                narrow(slide, BODY_RIGHT, 1_700_000, 5_600_000)
                w = PIC['size']; h = int(w * _I.open(shot).height / _I.open(shot).width); top = 2_200_000
                pic = slide.shapes.add_picture(str(shot), Emu(PIC['left']), Emu(top), Emu(w), Emu(h))
                pic.line.color.rgb = RGBColor(0xC9, 0xD5, 0xDA); pic.line.width = Pt(1)
                pic.name = 'illustration-shot'; pic._element.nvPicPr.cNvPr.set('descr', item['alt'])
                cap = slide.shapes.add_textbox(Emu(PIC['left']), Emu(top + h + 60_000), Emu(w), Emu(300_000)); cap.name = 'illustration-shot-caption'
                cap.text_frame.text = item['caption']; r = cap.text_frame.paragraphs[0].runs[0]; r.font.size = Pt(14); r.font.color.rgb = RGBColor(0x5A, 0x6B, 0x77)
                touched = True; done += 1; continue
            if item['kind'] == 'hero':
                path = png / f'hero_{n:02d}.png'
                narrow(slide, TITLE_RIGHT, 900_000, 6_300_000)
                pic = slide.shapes.add_picture(str(path), Emu(HERO['left']), Emu(HERO['top']), Emu(HERO['size']), Emu(HERO['size']))
                alt = 'Illustration: ' + '; '.join(ill.ALT[x].lower() for x in item['motifs'])
            else:
                path = png / f"{item['motif']}.png"
                narrow(slide, BODY_RIGHT, 1_700_000, 5_600_000)
                pic = slide.shapes.add_picture(str(path), Emu(PIC['left']), Emu(PIC['top']), Emu(PIC['size']), Emu(PIC['size']))
                alt = 'Illustration: ' + ill.ALT[item['motif']].lower()
            pic.name = f"illustration-{item['motif'] if item['kind'] != 'hero' else 'hero'}"
            pic._element.nvPicPr.cNvPr.set('descr', alt)
            touched = True; done += 1
        if touched: prs.save(str(f))
    print('illustrations placed:', done)


if __name__ == '__main__':
    main()
