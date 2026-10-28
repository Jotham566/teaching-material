"""Slide-content patch between the builder output and the teaching edition.

The deck builder (PowerPoint/build_course.mjs) needs a runtime that exists only on the
author's Mac. The corrections made afterwards (the new agreement wording, rewritten
slide text, replaced pictures) are therefore kept as a reviewable patch that can be
re-applied to the builder output on any machine with python-pptx.

  python3 edition_patch.py make  BASE_FOLDER EDITED_FOLDER PATCH_FOLDER
  python3 edition_patch.py apply BASE_FOLDER PATCH_FOLDER OUT_FOLDER

BASE_FOLDER is the builder output (Authoring/Baseline/Final Decks). EDITED_FOLDER
is a copy of the decks after the text and picture corrections and before notes and
illustrations. The patch stores, for each changed slide, the new text of each changed
paragraph (all runs and their font sizes), the new text of each changed table cell and
each replaced picture file. Notes come from Documents/lesson_notes.json and pictures
from Illustrations/, which have their own scripts.
"""
import sys, json, hashlib, shutil
from pathlib import Path
from pptx import Presentation
from pptx.util import Pt


def walk(shapes):
    for sh in shapes:
        yield sh
        if sh.shape_type == 6:
            yield from walk(sh.shapes)


def paragraphs(sh):
    if sh.has_text_frame:
        for i, p in enumerate(sh.text_frame.paragraphs): yield ('t', i), p
    elif getattr(sh, 'has_table', False) and sh.has_table:
        for r, row in enumerate(sh.table.rows):
            for c, cell in enumerate(row.cells):
                for i, p in enumerate(cell.text_frame.paragraphs): yield ('c', r, c, i), p


def runs_of(p): return [(r.text, r.font.size.pt if r.font.size else None) for r in p.runs]


def image_of(sh):
    try:
        return sh.image.blob if sh.shape_type == 13 else None
    except Exception:
        return None


def make(base, edited, out):
    out = Path(out); (out / 'images').mkdir(parents=True, exist_ok=True)
    patch = {}
    for f in sorted(Path(base).glob('[0-1][0-9] - *.pptx')):
        a = Presentation(str(f)); b = Presentation(str(Path(edited) / f.name)); deck = {}
        for n, (sa, sb) in enumerate(zip(a.slides, b.slides), 1):
            A = {sh.shape_id: sh for sh in walk(sa.shapes)}; B = {sh.shape_id: sh for sh in walk(sb.shapes) if not sh.name.startswith('illustration-')}
            assert set(A) == set(B), (f.name, n, set(A) ^ set(B))
            items = []
            for sid in A:
                pa = dict(paragraphs(A[sid])); pb = dict(paragraphs(B[sid]))
                for key in pb:
                    if runs_of(pa[key]) != runs_of(pb[key]):
                        items.append(dict(shape=sid, key=list(key), runs=runs_of(pb[key])))
                ia, ib = image_of(A[sid]), image_of(B[sid])
                if ia is not None and ia != ib:
                    h = hashlib.sha256(ib).hexdigest()[:16]; (out / 'images' / f'{h}.bin').write_bytes(ib)
                    items.append(dict(shape=sid, image=h))
            if items: deck[str(n)] = items
        patch[f.name[:2]] = deck
    (out / 'slide_patch.json').write_text(json.dumps(patch, indent=1, ensure_ascii=False), encoding='utf-8')
    print('slides patched:', sum(len(d) for d in patch.values()), 'items:', sum(len(v) for d in patch.values() for v in d.values()))


def apply(base, patch_folder, out):
    patch = json.loads((Path(patch_folder) / 'slide_patch.json').read_text(encoding='utf-8'))
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    for f in sorted(Path(base).glob('[0-1][0-9] - *.pptx')):
        prs = Presentation(str(f)); deck = patch.get(f.name[:2], {})
        for n, items in deck.items():
            slide = prs.slides[int(n) - 1]; shapes = {sh.shape_id: sh for sh in walk(slide.shapes)}
            for it in items:
                sh = shapes[it['shape']]
                if 'image' in it:
                    blob = (Path(patch_folder) / 'images' / f"{it['image']}.bin").read_bytes()
                    rid = sh._element.blipFill.blip.rEmbed; sh.part.related_part(rid)._blob = blob
                    continue
                key = it['key']; para = dict(paragraphs(sh))[tuple(key)]
                for r, (txt, size) in zip(para.runs, it['runs']):
                    r.text = txt
                    if size: r.font.size = Pt(size)
        prs.save(str(out / f.name))
    print('decks written to', out)


if __name__ == '__main__':
    cmd = sys.argv[1]
    (make if cmd == 'make' else apply)(*sys.argv[2:5])
