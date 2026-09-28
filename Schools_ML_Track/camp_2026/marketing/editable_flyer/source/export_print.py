"""Export standalone editable SVG and vector-text PDF from source/layout.json."""
from pathlib import Path
import json,base64,html
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
root=Path(__file__).resolve().parent.parent
layout=json.loads((root/'source/layout.json').read_text())
W,H=layout['width'],layout['height']
fonts=Path('/System/Library/Fonts/Supplemental')
pdfmetrics.registerFont(TTFont('FlyerArial',str(fonts/'Arial.ttf')))
pdfmetrics.registerFont(TTFont('FlyerArialBold',str(fonts/'Arial Bold.ttf')))
# A4 page with the original 2:3 composition centred. Text remains vector text.
pw,ph=595.2756,841.8898
scale=ph/H; offset=(pw-W*scale)/2
c=canvas.Canvas(str(root/'output/School_Track_Flyer.pdf'),pagesize=(pw,ph))
c.setTitle('School Track | Holiday Data & AI Camp | December 2026')
c.setAuthor('Jotham Martin Wambi')
c.translate(offset,0);c.scale(scale,scale)
c.setFillColor(HexColor('#FAFBFD')); c.rect(0,0,W,H,fill=1,stroke=0)
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}">', '<title>School Track: Holiday Data &amp; AI Camp</title>',f'<rect width="{W}" height="{H}" fill="#FAFBFD"/>']
for e in layout['elements']:
 x,y,w,h=(e[k] for k in ['x','y','w','h']);name=html.escape(e['name'],quote=True)
 if e['kind']=='rect':
  c.setFillColor(HexColor(e['color']));c.rect(x,H-y-h,w,h,fill=1,stroke=0)
  svg.append(f'<rect id="{name}" x="{x}" y="{y}" width="{w}" height="{h}" fill="{e["color"]}"/>')
 elif e['kind']=='text':
  font='FlyerArialBold' if e['bold'] else 'FlyerArial'; baseline=y+e['size']*.92
  c.setFont(font,e['size']);c.setFillColor(HexColor(e['color']));c.drawString(x,H-baseline,e['value'])
  if e.get('link'):c.linkURL(e['link'],(x,H-y-h,x+w,H-y),relative=1,thickness=0)
  st=f'<text id="{name}" x="{x}" y="{baseline}" font-family="Arial, sans-serif" font-size="{e["size"]}" font-weight="{700 if e["bold"] else 400}" fill="{e["color"]}">{html.escape(e["value"])}</text>'
  if e.get('link'):st=f'<a xlink:href="{html.escape(e["link"],quote=True)}">{st}</a>'
  svg.append(st)
 else:
  file=root/e['file'];c.drawImage(str(file),x,H-y-h,w,h,mask='auto',preserveAspectRatio=True,anchor='c')
  mime='image/jpeg' if file.suffix=='.jpeg' else 'image/png'
  b64=base64.b64encode(file.read_bytes()).decode()
  svg.append(f'<image id="{name}" x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet" xlink:href="data:{mime};base64,{b64}"/>')
svg.append('</svg>');(root/'output/School_Track_Flyer.svg').write_text('\n'.join(svg))
c.showPage();c.save()
print('Created A4 PDF and standalone editable SVG')
