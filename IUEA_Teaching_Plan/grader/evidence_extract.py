"""Recover written evidence from attachments the strict extractor rejects.

This wraps artifact_grade.extract without editing it (editing it would change
the calibration fingerprint). Every route ends in artifact_grade.extract, so
identifier removal and length limits still apply. Nothing uploaded is executed.
"""
import re
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path
import artifact_grade as grading
import attachment_expand

TEXT_SUFFIXES=('.md','.txt','.sql','.py')
DOC_SUFFIXES=('.pdf','.docx','.pptx')
ZIP_MEMBERS=TEXT_SUFFIXES+DOC_SUFFIXES+('.ipynb',)
MAX_MEMBER=5*1024*1024
MAX_TOTAL=30*1024*1024
MAX_MEMBERS=20
OCR_PAGES=12
OCR_NOTE='[Recovered by OCR; recognition errors are possible.]\n'


def decode(data):
    """Decode text uploaded from Windows editors (UTF-8/16 with or without BOM)."""
    if data.startswith((b'\xff\xfe',b'\xfe\xff')):return data.decode('utf-16')
    if data.startswith(b'\xef\xbb\xbf'):return data.decode('utf-8-sig')
    try:return data.decode('utf-8')
    except UnicodeDecodeError:return data.decode('cp1252',errors='replace')


def sniff(path):
    """Real file type from its content, for uploads saved as .bin or with a wrong extension."""
    head=Path(path).read_bytes()[:4]
    if head==b'%PDF':return '.pdf'
    if head[:2]==b'PK':
        try:
            with zipfile.ZipFile(path) as z:names=z.namelist()
        except zipfile.BadZipFile:return ''
        if 'word/document.xml' in names:return '.docx'
        if any(n.startswith('ppt/slides/') for n in names):return '.pptx'
        return '.zip'
    return ''


def _through_extract(text,assessment,name):
    with tempfile.TemporaryDirectory() as d:
        target=Path(d)/(name+'.txt');target.write_text(text,encoding='utf-8')
        return grading.extract(target,assessment)


def _docx_text(path):
    with zipfile.ZipFile(path) as z:
        info=z.getinfo('word/document.xml')
        if info.file_size>MAX_MEMBER:raise ValueError('Document too large to read')
        xml=z.read('word/document.xml').decode('utf-8',errors='replace')
    xml=re.sub(r'</w:p>','\n',xml)
    xml=re.sub(r'<w:tab/>','\t',xml)
    text=re.sub(r'<[^>]+>','',xml)
    return re.sub(r'&amp;','&',re.sub(r'&lt;','<',re.sub(r'&gt;','>',text)))


def _render_pages(path,d):
    """Page images for OCR: pypdfium2 (pip) if present, otherwise poppler's pdftoppm."""
    try:
        import pypdfium2
        pdf=pypdfium2.PdfDocument(str(path))
        pages=[]
        for i in range(min(len(pdf),OCR_PAGES)):
            target=Path(d)/f'p{i:03d}.png'
            pdf[i].render(scale=2).to_pil().save(target);pages.append(target)
        return pages
    except ImportError:
        if not shutil.which('pdftoppm'):raise ValueError('No PDF page renderer: pip install pypdfium2 (or brew install poppler)')
        subprocess.run(['pdftoppm','-r','150','-l',str(OCR_PAGES),'-png',str(path),str(Path(d)/'p')],
                       check=True,capture_output=True,timeout=180)
        return sorted(Path(d).glob('p*.png'))


def _ocr_image(page):
    """Apple Vision through ocrmac when available (best on this Mac); Tesseract otherwise."""
    try:
        from ocrmac import ocrmac
    except ImportError:
        if not shutil.which('tesseract'):raise ValueError('No OCR engine: pip install ocrmac (or brew install tesseract)')
        return subprocess.run(['tesseract',str(page),'stdout','-l','eng'],check=True,capture_output=True,text=True,timeout=90).stdout
    lines=ocrmac.OCR(str(page),recognition_level='accurate').recognize()
    # Vision returns (text, confidence, bounding box); the box origin is bottom-left.
    lines=sorted(lines,key=lambda x:-x[2][1])
    return '\n'.join(x[0] for x in lines)


def _ocr_pdf(path):
    with tempfile.TemporaryDirectory() as d:
        pages=_render_pages(path,d)
        if not pages:raise ValueError('No pages could be rendered for OCR')
        return OCR_NOTE+'\n'.join(_ocr_image(p) for p in pages)


def _pdf_fallback(path,assessment):
    text=''
    if shutil.which('pdftotext'):
        try:text=subprocess.run(['pdftotext','-layout','-l',str(OCR_PAGES*3),str(path),'-'],check=True,capture_output=True,text=True,timeout=120).stdout
        except Exception:text=''
    if len(text.strip())<40:text=_ocr_pdf(path)
    if len(text.strip())<80:raise ValueError('OCR found no readable text; the document needs manual review')
    return _through_extract(text,assessment,'ocr')


def _zip_text(path,assessment):
    parts=[]
    with zipfile.ZipFile(path) as z:
        infos=[i for i in z.infolist() if not i.is_dir()]
        if len(infos)>200 or sum(i.file_size for i in infos)>MAX_TOTAL*4:raise ValueError('ZIP is too large to read safely')
        used=0
        for info in infos:
            name=Path(info.filename)
            if '__MACOSX' in name.parts or name.name.startswith('.') or name.is_absolute() or '..' in name.parts:continue
            if name.suffix.lower() not in ZIP_MEMBERS or info.file_size>MAX_MEMBER:continue
            used+=info.file_size
            if len(parts)>=MAX_MEMBERS or used>MAX_TOTAL:break
            with tempfile.TemporaryDirectory() as d:
                target=Path(d)/('member'+name.suffix.lower());target.write_bytes(z.read(info))
                try:parts.append('### '+name.name+'\n'+extract(target,assessment))
                except ValueError:continue
    if not parts:raise ValueError('ZIP contains no readable report, README or notebook')
    return '\n\n'.join(parts)


def extract(original,assessment=None):
    path=Path(original);ext=path.suffix.lower()
    real=sniff(path) if ext not in TEXT_SUFFIXES+('.ipynb','.csv') else ''
    if real and real!=ext:ext=real
    if ext=='.ipynb' and path.read_bytes()[:2] in (b'\xff\xfe',b'\xfe\xff'):
        with tempfile.TemporaryDirectory() as d:
            copy=Path(d)/'nb.ipynb';copy.write_text(decode(path.read_bytes()),encoding='utf-8')
            return grading.extract(copy,assessment)
    if ext=='.zip':return _zip_text(path,assessment)
    if ext in ('.html','.htm'):
        parts=[]
        for m in attachment_expand.html_members(path):
            try:parts.append('### '+m['original_name']+'\n'+extract(m['path'],assessment))
            except ValueError:continue
        if not parts:raise ValueError('The HTML file has no readable GitHub README or notebook')
        return '\n\n'.join(parts)
    if ext in TEXT_SUFFIXES:return _through_extract(decode(path.read_bytes()),assessment,'text')
    if ext in DOC_SUFFIXES:
        with tempfile.TemporaryDirectory() as d:
            copy=Path(d)/('submission'+ext);copy.write_bytes(path.read_bytes())
            try:return grading.extract(copy,assessment)
            except Exception as first:
                try:
                    if ext=='.docx':return _through_extract(_docx_text(copy),assessment,'docx')
                    if ext=='.pdf':return _pdf_fallback(copy,assessment)
                except Exception as second:
                    raise ValueError(f'{first} | fallback: {second}'[:400])
                raise
    return grading.extract(path,assessment)
