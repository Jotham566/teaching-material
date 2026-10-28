"""Add native PowerPoint click-to-reveal builds without rasterising slide objects."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import xml.etree.ElementTree as ET
import re, sys, json

P='http://schemas.openxmlformats.org/presentationml/2006/main'
A='http://schemas.openxmlformats.org/drawingml/2006/main'
R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
for prefix, uri in [('p',P),('a',A),('r',R)]: ET.register_namespace(prefix,uri)
def el(parent, tag, **attrs): return ET.SubElement(parent,'{'+P+'}'+tag,{k:str(v) for k,v in attrs.items()})
def add_builds(root, groups):
    for tag in ['timing','transition']:
        old=root.find('{'+P+'}'+tag)
        if old is not None: root.remove(old)
    trans=ET.Element('{'+P+'}transition',{'spd':'med','advClick':'1'})
    el(trans,'fade')
    ext=root.find('{'+P+'}extLst')
    root.insert(list(root).index(ext) if ext is not None else len(root),trans)
    if not groups: return
    timing=ET.Element('{'+P+'}timing')
    root.insert(list(root).index(ext) if ext is not None else len(root),timing)
    node=el(el(timing,'tnLst'),'par')
    ct=el(node,'cTn',id=1,dur='indefinite',restart='never',nodeType='tmRoot')
    seq=el(el(ct,'childTnLst'),'seq',concurrent=1,nextAc='seek')
    main=el(seq,'cTn',id=2,dur='indefinite',nodeType='mainSeq')
    children=el(main,'childTnLst'); counter=3
    for group in groups:
        outer=el(children,'par'); o=el(outer,'cTn',id=counter,fill='hold');counter+=1
        el(el(o,'stCondLst'),'cond',delay='indefinite')
        click=el(el(o,'childTnLst'),'par')
        cc=el(click,'cTn',id=counter,fill='hold');counter+=1
        el(el(cc,'stCondLst'),'cond',delay=0)
        effects=el(cc,'childTnLst')
        for spid in group:
            effect=el(effects,'par')
            ec=el(effect,'cTn',id=counter,presetID=10,presetClass='entr',presetSubtype=0,fill='hold',nodeType='clickEffect');counter+=1
            el(el(ec,'stCondLst'),'cond',delay=0)
            runs=el(ec,'childTnLst')
            setter=el(runs,'set');bh=el(setter,'cBhvr')
            tc=el(bh,'cTn',id=counter,dur=1,fill='hold');counter+=1
            el(el(tc,'stCondLst'),'cond',delay=0)
            el(el(bh,'tgtEl'),'spTgt',spid=spid)
            at=el(bh,'attrNameLst');el(at,'attrName').text='style.visibility'
            el(el(setter,'to'),'strVal',val='visible')
            fade=el(runs,'animEffect',transition='in',filter='fade')
            fb=el(fade,'cBhvr');el(fb,'cTn',id=counter,dur=300);counter+=1
            el(el(fb,'tgtEl'),'spTgt',spid=spid)
    for tag,event in [('prevCondLst','onPrev'),('nextCondLst','onNext')]:
        cond=el(el(seq,tag),'cond',evt=event,delay=0);el(el(cond,'tgtEl'),'sldTgt')

def process(src,dst,lesson_path=None):
    lesson=json.loads(Path(lesson_path).read_text()) if lesson_path else None
    summary=[]
    with ZipFile(src) as zi,ZipFile(dst,'w',ZIP_DEFLATED) as zo:
        for f in zi.infolist():
            data=zi.read(f.filename)
            if re.fullmatch(r'ppt/slides/slide\d+\.xml',f.filename):
                root=ET.fromstring(data);groups={}
                number=int(re.search(r'slide(\d+)',f.filename).group(1))
                if lesson:
                    item=lesson['slides'][number-1]
                    if item.get('reference'): root.set('show','0')
                    slide=root.find('{'+P+'}cSld');slide.set('name',item['title'])
                    st=slide.find('{'+P+'}spTree')
                    # Put the visible footer last in the logical object order.
                    for shape in list(st):
                        words=''.join(x.text or '' for x in shape.findall('.//{'+A+'}t'))
                        if words.startswith('KLAi  '):st.remove(shape);st.append(shape)
                        if ' '.join(words.split())==' '.join(item['title'].split()):
                            nv=shape.find('{'+P+'}nvSpPr/{'+P+'}nvPr')
                            if nv is not None and nv.find('{'+P+'}ph') is None:ET.SubElement(nv,'{'+P+'}ph',{'type':'title'})
                    # Text remains native; one diagram object carries its overall explanation.
                    described=False
                    for shape in list(st):
                        if shape.tag not in ['{'+P+'}sp','{'+P+'}cxnSp','{'+P+'}graphicFrame']:continue
                        pr=shape.find('.//{'+P+'}cNvPr')
                        if pr is None or shape.tag=='{'+P+'}pic':continue
                        words=''.join(x.text or '' for x in shape.findall('.//{'+A+'}t'))
                        if words:continue
                        if not described and pr.get('name','').startswith('reveal-'):
                            note=item.get('note','');diagram_summary=note.split('Say: ',1)[-1].split('\n\n',1)[0] if 'Say: ' in note else item.get('definition',item['title'])
                            pr.set('descr',diagram_summary);described=True
                        else:
                            extensions=pr.find('{'+A+'}extLst')
                            if extensions is None:extensions=ET.SubElement(pr,'{'+A+'}extLst')
                            ext=ET.SubElement(extensions,'{'+A+'}ext',{'uri':'{C183D7F6-B498-43B3-948B-1728B52AA6E4}'})
                            ET.SubElement(ext,'{http://schemas.microsoft.com/office/drawing/2017/decorative}decorative',{'val':'1'})

                for pr in root.findall('.//{'+P+'}cNvPr'):
                    m=re.match(r'reveal-(\d+)-',pr.get('name',''))
                    if m:groups.setdefault(int(m[1]),[]).append(pr.get('id'))
                add_builds(root,[groups[k] for k in sorted(groups)])
                data=ET.tostring(root,encoding='utf-8',xml_declaration=True)
                summary.append({'slide':f.filename,'clicks':len(groups),'animated_objects':sum(map(len,groups.values()))})
            if f.filename=='ppt/presentation.xml' and lesson:
                root=ET.fromstring(data)
                old=root.find('{'+P+'}custShowLst')
                if old is not None:root.remove(old)
                ids=root.find('{'+P+'}sldIdLst')
                shows=ET.Element('{'+P+'}custShowLst')
                for sid,label,numbers in [(1,'Core teaching',lesson.get('core_slides',list(range(1,len(lesson['slides'])+1)))),(2,'Reference material',lesson.get('reference_slides',[]))]:
                    if not numbers:continue
                    show=ET.SubElement(shows,'{'+P+'}custShow',{'name':label,'id':str(sid)});lst=ET.SubElement(show,'{'+P+'}sldLst')
                    for number in numbers:ET.SubElement(lst,'{'+P+'}sld',{'{'+R+'}id':ids[number-1].get('{'+R+'}id')})
                # Custom shows follow notes/master/size and precede optional photo/show settings.
                insertion=len(root)
                for ix,ch in enumerate(root):
                    if ch.tag.split('}')[-1] in ['photoAlbum','custDataLst','kinsoku','defaultTextStyle','modifyVerifier','extLst']:insertion=ix;break
                root.insert(insertion,shows)
                data=ET.tostring(root,encoding='utf-8',xml_declaration=True)
            zo.writestr(f,data)
    with ZipFile(dst) as z:
        assert z.testzip() is None
        for f in z.namelist():
            if re.fullmatch(r'ppt/slides/slide\d+\.xml',f):
                rt=ET.fromstring(z.read(f));ids={x.get('id') for x in rt.findall('.//{'+P+'}cNvPr')}
                targets={x.get('spid') for x in rt.findall('.//{'+P+'}spTgt')}
                assert targets<=ids,(f,targets-ids)
                tids=[x.get('id') for x in rt.findall('.//{'+P+'}cTn')]
                assert len(tids)==len(set(tids)),f
    Path(str(dst)+'.animation.json').write_text(json.dumps(summary,indent=2))
    print(json.dumps({'animated_slides':sum(x['clicks']>0 for x in summary),'click_builds':sum(x['clicks'] for x in summary)}))
if __name__=='__main__':process(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]) if len(sys.argv)>3 else None)
