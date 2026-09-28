"""Render untrusted student documents in a network-isolated Docker container."""
import argparse,base64,hashlib,json,os,selectors,subprocess,tempfile,time,uuid
from pathlib import Path
IMAGE='iuea-document-renderer:2026.09'
HERE=Path(__file__).resolve().parent

def bounded_output(cmd,timeout=210,limit=100*1024*1024):
 """Bound output while reading, rather than after allocating arbitrary output."""
 proc=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
 chunks=[];size=0;deadline=time.monotonic()+timeout
 try:
  with selectors.DefaultSelector() as selector:
   selector.register(proc.stdout,selectors.EVENT_READ)
   while True:
    remaining=deadline-time.monotonic()
    if remaining<=0 or not selector.select(remaining):raise TimeoutError('Document rendering exceeded time limit')
    chunk=os.read(proc.stdout.fileno(),65536)
    if not chunk:break
    size+=len(chunk)
    if size>limit:raise ValueError('Render output exceeds limit')
    chunks.append(chunk)
  status=proc.wait(timeout=max(.01,deadline-time.monotonic()))
  if status:raise RuntimeError('Document could not be rendered')
  return b''.join(chunks).decode('utf-8')
 finally:
  if proc.poll() is None:proc.kill()
  proc.wait(timeout=10);proc.stdout.close()

def render(source,out):
 source=Path(source);out=Path(out)
 if source.suffix.lower() not in ('.pdf','.docx','.pptx') or source.stat().st_size>20*1024*1024:raise ValueError('Supported: PDF/DOCX/PPTX up to 20 MiB')
 out.mkdir(parents=True,exist_ok=True)
 if any(out.iterdir()):raise ValueError('Use an empty rendering directory')
 name='iuea-render-'+uuid.uuid4().hex
 identity=subprocess.check_output(['docker','image','inspect','--format={{.Id}}',IMAGE],text=True,timeout=15).strip()
 with tempfile.TemporaryDirectory() as d:
  temp=Path(d);target=temp/('submission'+source.suffix.lower());target.write_bytes(source.read_bytes());temp.chmod(0o755);target.chmod(0o644)
  cmd=['docker','run','--rm','--name',name,'--network=none','--read-only','--cap-drop=ALL','--security-opt=no-new-privileges','--memory=2g','--cpus=1','--pids-limit=128','--tmpfs=/tmp:rw,nosuid,size=256m,uid=65534,gid=65534','--mount',f'type=bind,src={temp.resolve()},dst=/input,readonly','--mount',f'type=bind,src={HERE}/document_renderer/render.py,dst=/render.py,readonly',identity,'python3','/render.py']
  try:output=bounded_output(cmd)
  finally:subprocess.run(['docker','rm','-f',name],capture_output=True,timeout=15)
  files=[]
  for line in output.splitlines():
   row=json.loads(line);page=row['page']
   if type(page) is not int or page!=len(files)+1 or page>30:raise ValueError('Invalid page sequence')
   path=out/f'page-{page:02}.png';path.write_bytes(base64.b64decode(row['png'],validate=True));files.append(path.name)
  if not files:raise ValueError('Document contains no rendered pages')
  (out/'render_manifest.json').write_text(json.dumps(dict(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),renderer_image=IMAGE,renderer_image_id=identity,pages=files),indent=2))
  return files

def extract_document(source):
 source=Path(source)
 if source.suffix.lower() not in ('.pdf','.docx','.pptx') or source.stat().st_size>20*1024*1024:raise ValueError('Supported: PDF/DOCX/PPTX up to 20 MiB')
 identity=subprocess.check_output(['docker','image','inspect','--format={{.Id}}',IMAGE],text=True,timeout=15).strip()
 name='iuea-extract-'+uuid.uuid4().hex
 with tempfile.TemporaryDirectory() as d:
  temp=Path(d);target=temp/('submission'+source.suffix.lower());target.write_bytes(source.read_bytes());temp.chmod(0o755);target.chmod(0o644)
  cmd=['docker','run','--rm','--name',name,'--network=none','--read-only','--cap-drop=ALL','--security-opt=no-new-privileges','--memory=1g','--cpus=1','--pids-limit=64','--tmpfs=/tmp:rw,nosuid,size=128m,uid=65534,gid=65534','--mount',f'type=bind,src={temp.resolve()},dst=/input,readonly','--mount',f'type=bind,src={HERE}/document_renderer/extract.py,dst=/extract.py,readonly',identity,'python3','/extract.py']
  try:output=bounded_output(cmd,timeout=90,limit=100000)
  finally:subprocess.run(['docker','rm','-f',name],capture_output=True,timeout=15)
  result=json.loads(output)
  if not isinstance(result.get('text'),str) or len(result['text'])>12000:raise ValueError('Invalid extracted text')
  return result['text']
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('source');p.add_argument('--out',required=True);a=p.parse_args();print(render(a.source,a.out))
