"""Install Artifact Tool-authored notes without reflowing original slide artwork.

Only note-body XML and explicit reviewed text replacements may change. All other
ZIP entries, including media, masters, themes, relationships and code, are checked.
"""
from pathlib import Path
import copy, hashlib, json, re, zipfile, xml.etree.ElementTree as E
from presentation_teaching_support import correct, title
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'review/2026-09-21/presentation-notes'
A='{http://schemas.openxmlformats.org/drawingml/2006/main}';P='{http://schemas.openxmlformats.org/presentationml/2006/main}'
E.register_namespace('', 'http://schemas.openxmlformats.org/package/2006/content-types');E.register_namespace('a',A[1:-1]);E.register_namespace('p',P[1:-1]);E.register_namespace('r','http://schemas.openxmlformats.org/officeDocument/2006/relationships')
def body(root):
 for sp in root.iter(P+'sp'):
  ph=sp.find('.//'+P+'ph')
  if ph is not None and ph.get('type')=='body':return sp
 raise ValueError('Missing note body placeholder')
def paragraphs(root):return '\n'.join(''.join(t.text or '' for t in p.iter(A+'t')) for p in root.iter(A+'p'))
def sha(data):return hashlib.sha256(data).hexdigest()
def replace_paragraphs(root,deck_path):
 edits=[]
 for p in root.iter(A+'p'):
  runs=list(p.iter(A+'t'));before=''.join(t.text or '' for t in runs);after=correct(before,deck_path)
  if before!=after:
   # Keep all original run formatting, replace text over the smallest affected span.
   prefix=0
   while prefix<min(len(before),len(after)) and before[prefix]==after[prefix]:prefix+=1
   suffix=0
   while suffix<min(len(before),len(after))-prefix and before[-suffix-1]==after[-suffix-1]:suffix+=1
   stop=len(before)-suffix;replacement=after[prefix:len(after)-suffix if suffix else len(after)];offset=0;inserted=False
   for t in runs:
    text=t.text or '';start=offset;end=start+len(text);offset=end
    if end<=prefix or start>=stop:continue
    left=text[:max(0,prefix-start)];right=text[max(0,stop-start):] if end>stop else ''
    t.text=left+(replacement if not inserted else '')+right;inserted=True
   assert ''.join(t.text or '' for t in runs)==after,(before,after)
   edits.append({'before':before,'after':after})
 return edits

def main():
 plan=json.loads((OUT/'notes-plan.json').read_text());report=[]
 previous={d['path']:d['sha256'] for d in json.loads((OUT/'installation.json').read_text())} if (OUT/'installation.json').exists() else {}
 for deck in plan:
  dest=ROOT/deck['path']; original=OUT/'originals'/dest.name;changed={};visible=[]
  assert sha(dest.read_bytes()) in {deck['before_sha256'],previous.get(deck['path'])},f'New edits found: refresh review inventory before changing {dest}'
  with zipfile.ZipFile(original) as base,zipfile.ZipFile(OUT/'authored'/dest.name) as authored:
   for s in deck['slides']:
    np=s['notes_part']
    if np is None:
     existing=[n for n in base.namelist() if re.fullmatch(r'ppt/notesSlides/notesSlide\d+.xml',n)]
     template=existing[0];num=10000+s['number'];np=f'ppt/notesSlides/notesSlide{num}.xml'
     target=E.fromstring(base.read(template))
     relpart=f'ppt/slides/_rels/slide{s["number"]}.xml.rels';rel=E.fromstring(base.read(relpart));ns='{http://schemas.openxmlformats.org/package/2006/relationships}'
     used={r.get('Id') for r in rel};rid=1
     while f'rId{rid}' in used:rid+=1
     E.SubElement(rel,ns+'Relationship',Id=f'rId{rid}',Type='http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesSlide',Target=f'../notesSlides/notesSlide{num}.xml')
     changed[relpart]=E.tostring(rel,encoding='utf-8',xml_declaration=True)
     note_rel=E.fromstring(base.read(template.replace('notesSlides/','notesSlides/_rels/')+'.rels'))
     for r in note_rel:
      if r.get('Type','').endswith('/slide'):r.set('Target',f'../slides/slide{s["number"]}.xml')
     changed[f'ppt/notesSlides/_rels/notesSlide{num}.xml.rels']=E.tostring(note_rel,encoding='utf-8',xml_declaration=True)
     ct=E.fromstring(changed.get('[Content_Types].xml',base.read('[Content_Types].xml')))
     E.SubElement(ct,'{http://schemas.openxmlformats.org/package/2006/content-types}Override',PartName='/'+np,ContentType='application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml')
     changed['[Content_Types].xml']=E.tostring(ct,encoding='utf-8',xml_declaration=True)
    else:target=E.fromstring(base.read(np))
    new=E.fromstring(authored.read(f'ppt/notesSlides/notesSlide{s["number"]}.xml'))
    dst=body(target);src=body(new);tx=dst.find(P+'txBody');dst.remove(tx);dst.append(copy.deepcopy(src.find(P+'txBody')))
    assert paragraphs(body(target)).strip()==s['notes'].strip()
    changed[np]=E.tostring(target,encoding='utf-8',xml_declaration=True)
    part=f'ppt/slides/slide{s["number"]}.xml';slide=E.fromstring(base.read(part));edits=replace_paragraphs(slide,deck['path'])
    if edits:
     changed[part]=E.tostring(slide,encoding='utf-8',xml_declaration=True);visible.append({'slide':s['number'],'edits':edits})
   temp=dest.with_suffix('.notes-review.tmp')
   with zipfile.ZipFile(temp,'w',compression=zipfile.ZIP_DEFLATED) as out:
    for entry in base.infolist():out.writestr(entry,changed.get(entry.filename,base.read(entry.filename)))
    for name,data in changed.items():
     if name not in base.namelist():out.writestr(name,data)
  with zipfile.ZipFile(temp) as final,zipfile.ZipFile(original) as base:
   assert final.testzip() is None
   assert set(base.namelist()).issubset(final.namelist())
   assert len(final.namelist())==len(set(final.namelist()))
   unchanged=[n for n in base.namelist() if n not in changed]
   assert all(final.read(n)==base.read(n) for n in unchanged)
   for n in final.namelist():
    if n.endswith('.xml') or n.endswith('.rels'):E.fromstring(final.read(n))
  temp.replace(dest)
  notesdir=dest.parent/'lecturer_notes';notesdir.mkdir(exist_ok=True)
  content=['# '+dest.stem.replace('_',' '),'','Private lecturer companion. These same notes are embedded in the PowerPoint. Use Presenter View; keep the student display on slides only.','']
  for s in deck['slides']:content += [f'## Slide {s["number"]} — {title(s["visible_after"])}','',s['notes'],'']
  (notesdir/(dest.stem+'.md')).write_text('\n'.join(content)+'\n')
  report.append({'path':deck['path'],'slides':len(deck['slides']),'sha256':sha(dest.read_bytes()),'notes_replaced':len(deck['slides']),'visible_edits':visible,'other_zip_parts_byte_identical':True})
 (OUT/'installation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
 print(f'Installed {len(report)} decks; {sum(len(d["visible_edits"]) for d in report)} slides have visible wording corrections. All other artwork unchanged.')
if __name__=='__main__':main()
