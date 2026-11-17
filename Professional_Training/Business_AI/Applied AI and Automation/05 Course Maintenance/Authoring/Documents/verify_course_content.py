"""Verify source/deck alignment and the classroom fixtures in the private build."""
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as E
import hashlib, json, re
from legal_tax_course import COURSE, CLAUSE
from course_paths import SOURCE

B=SOURCE.parent/'.build/legal_tax_rebuild'
A_NS='{http://schemas.openxmlformats.org/drawingml/2006/main}'
P_NS='{http://schemas.openxmlformats.org/presentationml/2006/main}'

def text_of(xml):
    root=E.fromstring(xml)
    return '\n'.join(''.join(p.itertext()) for p in root.iter(A_NS+'t'))

def verify():
    manifest=json.loads((B/'New Deck Manifest.json').read_text())
    assert len(manifest)==len(COURSE)==12
    index=json.loads((B/'Practice Index.json').read_text())
    for key,rel in index.items():
        assert (B/'Practice Files'/rel).is_file(), (key,rel)
    total=optional=concepts=clicks=0
    for d,m in zip(COURSE,manifest):
        assert d['session']==m['session'] and d['title']==m['title']
        assert len(d['slides'])==m['slides']
        assert sum(v for _,v in d['timing'])==120
        assert sum(r['minutes'] for r in d['run_sheet'])==120
        essential=set(d['core_slides']); extra=set(d['optional_slides'])
        assert not essential&extra
        assert essential|extra==set(range(1,len(d['slides'])+1))
        scheduled={s for r in d['run_sheet'] for s in r['slides']}
        assert scheduled==essential
        assert set(d['concept_slides'])<=essential
        for f in d['files']: assert f in index,f
        p=B/'Final Decks'/Path(m['file']).name
        receipt=json.loads((B/'Slides'/f"{d['session']:02}"/'validation.json').read_text())
        assert hashlib.sha256(p.read_bytes()).hexdigest()==receipt['finalSha256']
        assert receipt['packageIntegrity']['finding_count']==0
        assert receipt['presentationLayout']['finding_count']==0
        animations=json.loads((B/'Slides'/f"{d['session']:02}"/'animated.pptx.animation.json').read_text())
        with ZipFile(p) as z:
            assert z.testzip() is None
            assert len([n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml',n)])==len(d['slides'])
            for n,x in enumerate(d['slides'],1):
                xml=z.read(f'ppt/slides/slide{n}.xml')
                root=E.fromstring(xml)
                assert root.get('show','1')!='0'
                visible=text_of(xml)
                assert x['title'] in visible,(d['session'],n,x['title'])
                assert ('OPTIONAL EXPLORATION' in visible)==(n in extra)
                note_xml=E.fromstring(z.read(f'ppt/notesSlides/notesSlide{n}.xml'))
                body=next(v for v in note_xml.findall('.//'+P_NS+'sp') if v.find('.//'+P_NS+'ph').get('type')=='body')
                paras=[''.join(t.text or '' for t in par.iter(A_NS+'t')) for par in body.iter(A_NS+'p')]
                note='\n'.join(paras)
                assert note.startswith(x['note']), (d['session'],n,'speaker notes drift')
                stage=animations[n-1]
                cue=f"Playback: {stage['clicks']} native click reveals." if stage['clicks'] else 'Playback: Static slide.'
                assert cue in note,(d['session'],n,'playback cue')
                timing=root.find(P_NS+'timing')
                assert (timing is not None)==bool(stage['clicks'])
                ids={el.get('id') for el in root.iter(P_NS+'cNvPr')}
                if timing is not None:
                    assert all(el.get('spid') in ids for el in timing.iter(P_NS+'spTgt'))
                clicks+=stage['clicks']
        total+=len(d['slides']);optional+=len(extra);concepts+=len(d['concept_slides'])
    assert (total,optional,concepts)==(285,52,88)
    clause=json.loads((B/'Practice Files'/index['Clause Record.json']).read_text())
    assert CLAUSE in json.dumps(clause,ensure_ascii=False)
    observed=B/'Facilitator Resources/Observed Runs'
    assert len(list(observed.glob('*Agent*Trace*.json')))>=1
    assert (B/'PowerPoint Probability Playback.png').is_file()
    assert (B/'Workflow Stale Approval Browser.png').is_file()
    result={'sessions':12,'visible_slides':total,'essential_slides':total-optional,'optional_slides':optional,'concept_explanation_slides':concepts,'native_click_stages':clicks,'indexed_practice_files':len(index),'checks':'Source/deck titles, notes, timings, optional flags, referenced files, receipts, animation targets and supplied-clause fidelity passed.'}
    (B/'Content Verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))

if __name__=='__main__':verify()
