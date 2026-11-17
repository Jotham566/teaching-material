"""Patch the editable PowerPoint for the revision 2 wording, without the Codex runtime.

Edits the named shapes in output/previous/School_Track_Registration_Editable.pptx to match layout.json and
swaps the third logo for the charts icon. Run source/export_powerpoint.mjs instead where that runtime exists.
"""
import json
from pathlib import Path
from pptx import Presentation
R = Path(__file__).resolve().parent.parent
el = {e['name']: e for e in json.loads((R / 'source/layout.json').read_text())['elements']}
prs = Presentation(str(R / 'output/previous/School_Track_Registration_Editable.pptx'))
slide = prs.slides[0]
by = {}
for sh in slide.shapes:
    by.setdefault(sh.name or '', []).append(sh)
renames = {'SQL label 349': 'Charts label 349', 'SQL logo 349': 'Charts logo 349'}
TEXT = ['DA description', 'DA learning 2', 'DA learning 4', 'ML learning 5', 'DA project examples', 'ML project examples', 'Outcome 2']
done = []
for sh in slide.shapes:
    n = renames.get(sh.name, sh.name)
    if sh.name in renames:
        sh.name = n
    if n in TEXT + ['Charts label 349'] and sh.has_text_frame:
        lines = el[n]['value'].split('\n')
        paras = sh.text_frame.paragraphs
        # keep the first run's formatting; put one line in each existing paragraph, add paragraphs by copying
        import copy
        while len(paras) < len(lines):
            sh.text_frame._txBody.append(copy.deepcopy(paras[-1]._p)); paras = sh.text_frame.paragraphs
        for p, line in zip(paras, lines):
            runs = p.runs
            runs[0].text = line
            for r in runs[1:]:
                r._r.getparent().remove(r._r)
        for p in paras[len(lines):]:
            p._p.getparent().remove(p._p)
        done.append(n)
    if sh.shape_type == 13:
        k = prs.slide_width / 1024.0
        t = el['Charts logo 349']
        if abs(sh.top - t['y'] * k) < 3 * k and t['x'] * k - 2 * k <= sh.left <= (t['x'] + t['w']) * k:   # pictures carry no names, so match by position
            img_part, rid = slide.part.get_or_add_image_part(str(R / t['file']))
            sh._element.blipFill.blip.rEmbed = rid
            # the icon is square, so fit it inside the 52 x 48 slot the way the exporter does ('contain')
            side = min(t['w'], t['h'])
            sh.left = int((t['x'] + (t['w'] - side) / 2) * k); sh.top = int((t['y'] + (t['h'] - side) / 2) * k)
            sh.width = int(side * k); sh.height = int(side * k)
            c = sh._element.nvPicPr.cNvPr
            c.set('name', 'Charts logo 349'); c.set('descr', 'Charts logo 349')
            done.append('Charts logo 349')
prs.save(str(R / 'output/School_Track_Registration_Editable.pptx'))
print('patched', sorted(set(done)))
