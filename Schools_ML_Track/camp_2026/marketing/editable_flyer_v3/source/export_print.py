"""Export PDF and layered SVG from the editable layout data."""
from pathlib import Path
import json,base64,html
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
root=Path(__file__).resolve().parent.parent
layout=json.loads((root/'source/layout.json').read_text());W,H=layout['width'],layout['height']
fonts=Path('/System/Library/Fonts/Supplemental')
fontmap={('Arial',False):'Arial.ttf',('Arial',True):'Arial Bold.ttf',('Arial Black',False):'Arial Black.ttf',('Arial Black',True):'Arial Black.ttf',('Arial Narrow',False):'Arial Narrow.ttf',('Arial Narrow',True):'Arial Narrow Bold.ttf',('Caveat',True):root/'assets/Caveat.ttf'}
for i,(key,file) in enumerate(fontmap.items()):
 name='Font'+str(i);pdfmetrics.registerFont(TTFont(name,str(file if isinstance(file,Path) else fonts/file)));fontmap[key]=name
pw,ph=595.2756,841.8898;scale=ph/H;offset=(pw-W*scale)/2
c=canvas.Canvas(str(root/'output/School_Track_Updated.pdf'),pagesize=(pw,ph));c.setTitle('Holiday Data & AI Camp - School Track');c.setAuthor('Jotham Martin Wambi');c.translate(offset,0);c.scale(scale,scale)
font64=base64.b64encode((root/'assets/Caveat.ttf').read_bytes()).decode()
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',f'<defs><style>@font-face{{font-family:Caveat;src:url(data:font/ttf;base64,{font64});font-weight:100 900;}}</style></defs>','<title>Editable reconstruction of the original School Track flyer</title>']
for e in layout['elements']:
 x,y,w,h=[e[k] for k in ['x','y','w','h']];name=html.escape(e['name'],quote=True)
 if e['kind']=='rect':
  r=e.get('r',0);c.setFillColor(HexColor(e['color']));c.roundRect(x,H-y-h,w,h,r,stroke=0,fill=1)
  svg.append(f'<rect id="{name}" x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{e["color"]}"/>')
 elif e['kind']=='image':
  file=root/e['file'];c.drawImage(str(file),x,H-y-h,w,h,mask='auto',preserveAspectRatio=True,anchor='c')
  mime='image/jpeg' if file.suffix=='.jpeg' else 'image/png';b64=base64.b64encode(file.read_bytes()).decode()
  svg.append(f'<image id="{name}" x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet" xlink:href="data:{mime};base64,{b64}"/>')
 else:
  size=e['size'];rot=e.get('rot',0);font=fontmap[(e.get('font','Arial'),e['bold'])];c.saveState();c.translate(x+w/2,H-y-h/2);c.rotate(-rot);c.translate(-w/2,h/2);c.setFont(font,size);c.setFillColor(HexColor(e['color']))
  align=e.get('align','left');anchor='middle' if align=='center' else 'start';sx=x+w/2 if align=='center' else x
  lines=e['value'].split('\n');svg.append(f'<text id="{name}" font-family="{e.get("font","Arial")}" font-size="{size}" font-weight="{700 if e["bold"] else 400}" fill="{e["color"]}" text-anchor="{anchor}" transform="rotate({rot} {x+w/2} {y+h/2})">')
  for i,line in enumerate(lines):
   baseline=size*.92+i*size*1.2
   if align=='center':c.drawCentredString(w/2,-baseline,line)
   else:c.drawString(0,-baseline,line)
   svg.append(f'<tspan x="{sx}" y="{y+baseline}">{html.escape(line)}</tspan>')
  c.restoreState();svg.append('</text>')
# Working links without altering the visual text style.
for url,rect in [('https://wa.me/256750990718',(522,1260,1005,1455)),('mailto:jothammartin.wambi@gmail.com',(579,1385,830,1420))]:
 x1,y1,x2,y2=rect;c.linkURL(url,(x1,H-y2,x2,H-y1),relative=1,thickness=0)
svg.append('</svg>');(root/'output/School_Track_Updated.svg').write_text('\n'.join(svg));c.showPage();c.save();print('PDF and SVG exported')
