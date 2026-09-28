"""Container-only document rendering, with no network or writable host mount."""
import base64,json,subprocess,sys
from pathlib import Path
from PIL import Image
source=next(Path('/input').glob('submission.*'))
profile=Path('/tmp/profile/user');profile.mkdir(parents=True)
(profile/'registrymodifications.xcu').write_text('''<?xml version="1.0" encoding="UTF-8"?><oor:items xmlns:oor="http://openoffice.org/2001/registry"><item oor:path="/org.openoffice.Office.Common/Security/Scripting"><prop oor:name="MacroSecurityLevel" oor:op="fuse"><value>3</value></prop></item></oor:items>''')
out=Path('/tmp/render');out.mkdir()
if source.suffix.lower()=='.pdf':pdf=source
else:
 subprocess.run(['libreoffice','-env:UserInstallation=file:///tmp/profile','--headless','--convert-to','pdf','--outdir',str(out),str(source)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=90)
 pdf=out/'submission.pdf'
info=subprocess.check_output(['pdfinfo',str(pdf)],text=True,timeout=10)
pages=int(next(line.split(':',1)[1].strip() for line in info.splitlines() if line.startswith('Pages:')))
if not 1<=pages<=30:raise ValueError('Submit 1–30 pages/slides for supported visual assessment')
subprocess.run(['pdftocairo','-scale-to','1280','-png',str(pdf),str(out/'page')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=90)
for i,path in enumerate(sorted(out.glob('page-*.png'),key=lambda p:int(p.stem.rsplit('-',1)[1])),1):
 with Image.open(path) as image:
  if image.width*image.height>2000000:raise ValueError('Unexpected render size')
 print(json.dumps(dict(page=i,png=base64.b64encode(path.read_bytes()).decode())),flush=True)
