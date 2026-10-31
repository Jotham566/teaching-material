"""Package the two student ZIPs (revision 2). Run after build_camp.py and verify_camp.py."""
import re
import shutil
import zipfile
from common import ROOT, HANDBOOK, PROGRAMME, PACKS
import build_pdfs

POLICY = ['AI_USE_POLICY.md', 'AI_CODING_ASSISTANTS_LAB.md', 'PROJECT_RUBRIC.md', 'ASSESSMENT_AND_SHOWCASE.md', 'MODERN_AI_ORIENTATION.md']


def resolve(text, code):
    """Keep the marked block for this track and drop the other track's block."""
    other = 'DA' if code == 'ML' else 'ML'
    text = re.sub(r'<!--%s-->.*?<!--/%s-->\n?' % (other, other), '', text, flags=re.S)
    return re.sub(r'<!--/?%s-->' % code, '', text)


for code in ['ML', 'DA']:
    folder = ROOT / 'student_materials' / code
    (folder / 'START_HERE.md').write_text(resolve((HANDBOOK / 'START_HERE.md').read_text(), code), encoding='utf-8')
    for f in POLICY:
        shutil.copy2(HANDBOOK / f, folder / f)
    shutil.copy2(PROGRAMME / 'requirements-tested.txt', folder / 'requirements-tested.txt')
    shutil.copy2(PROGRAMME / 'preflight_stack.py', folder / 'preflight_stack.py')
    PACKS.mkdir(exist_ok=True)
    build_pdfs.student(code)          # PDFs are what students receive; the Markdown stays in the repository
    zpath = PACKS / f'{code}_Beginner_Student_Pack.zip'
    with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED) as z:
        for p in sorted(folder.rglob('*')):
            if p.is_file() and p.name != '.DS_Store' and p.suffix != '.md':
                z.write(p, code + '/' + str(p.relative_to(folder)))
    with zipfile.ZipFile(zpath) as z:
        names = z.namelist()
        assert not any('instructor' in n or 'reference_values' in n or n.endswith('_guide.md') or 'keras_demo' in n for n in names), 'instructor file in student zip'
        assert f'{code}/PDF/START_HERE.pdf' in names
        assert not any(n.endswith('.md') for n in names), 'Markdown source in a student zip'
        sheets = [n for n in names if re.fullmatch(code + r'/PDF/' + code + r'\d\d\.pdf', n)]
        books = [n for n in names if re.fullmatch(code + r'/' + code + r'\d\d\.ipynb', n)]
        assert len(sheets) == 24 and len(books) == 24, (len(sheets), len(books))
        text = (folder / 'START_HERE.md').read_text()
        assert '<!--' not in text, 'unresolved track marker'
        assert not any(n.endswith('.sqlite') or n.endswith('.sql') for n in names), 'SQL file in a student zip'
        if code == 'ML':
            assert all(f'ML/F{i:02}.ipynb' in names and f'ML/PDF/F{i:02}.pdf' in names for i in range(1, 5))
            assert 'ML/ML25_Extension.ipynb' in names
            assert 'ML/synthetic_fares.csv' in names and 'ML/synthetic_homes.csv' in names
        else:
            assert all(f'DA/{n}' in names for n in ['sunrise_sales.csv', 'sunrise_sales_raw.csv', 'sunrise_products.csv', 'sunrise_products_practice.csv', 'sunrise_branches.csv', 'sunrise_daily_summary.csv', 'camp_shop.csv'])
        print(code, len(names), 'student-only files')
