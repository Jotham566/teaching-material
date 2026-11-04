"""Scan every text in the executive edition for banned content. Run from Build/: python3 kit/scan_edition.py
Checks: the course price, exam and marks language, em dashes, filler words, 'X, not Y', gendered pronouns for the learner."""
import re, sys, zipfile
from pathlib import Path
EDITION = Path(__file__).resolve().parents[3]
SKIP = {'Archive', 'figures', '_specs', '__pycache__', 'node_modules'}
PRICE = re.compile(r'1,000,000|1 million|course fee|price of (the|this) course|tuition', re.I)
EXAM = re.compile(r'\b(exam|exams|marks|graded|grading|pass mark)\b', re.I)
BAN = re.compile(r'honestly|genuinely|straightforward|dive into|\bunlock|\bjourney\b|embark|game-changer|delve|leverage\b', re.I)
ANTI = re.compile(r',\s+not\s+(a|an|the|just|only|about|because|to|for|in|on|by|with|every|all|any)\b|\bnot\s+just\b', re.I)
PRON = re.compile(r'\b(he|she|his|her)\b', re.I)
DASH = re.compile('—')

def texts(p):
    s = p.suffix.lower()
    try:
        if s in ('.txt', '.csv', '.md', '.gs', '.js', '.py', '.json'):
            yield p.read_text(errors='ignore')
        elif s in ('.docx', '.xlsx', '.pptx'):
            with zipfile.ZipFile(p) as z:
                for n in z.namelist():
                    if n.endswith('.xml') and ('word/' in n or 'xl/sharedStrings' in n or 'ppt/slides/slide' in n or 'ppt/notesSlides' in n or 'xl/worksheets' in n):
                        x = z.read(n).decode('utf8', 'ignore')
                        yield re.sub(r'<[^>]+>', ' ', x)
    except Exception as e:
        print('cannot read', p, e)

bad = 0
for p in sorted(EDITION.rglob('*')):
    if not p.is_file() or any(part in SKIP for part in p.parts) or p.suffix.lower() not in ('.txt', '.csv', '.md', '.gs', '.js', '.py', '.json', '.docx', '.xlsx', '.pptx'):
        continue
    if p.name in ('scan_edition.py', 'lint_content.py', 'COURSE_BIBLE.md', 'make_docs.py', 'brand.py', 'verify_templates.py', 'make_case_data.py', 'customer_messages.csv', 'meeting_actions_key.csv', 'run_tests.js', 'Zapier Build Guide.docx', 'Zapier Rehearsal Checklist.docx', 'Apps Script Build Guide.docx', 'Course Overview.docx', 'Start Here.docx', 'Facilitator Guide.docx') or 'data_gen' in p.parts and p.suffix == '.py' and 'verify' in p.name:
        continue
    for t in texts(p):
        for name, rx in (('price', PRICE), ('exam/marks', EXAM), ('banned word', BAN), ('X, not Y', ANTI), ('em dash', DASH)):
            for m in rx.finditer(t):
                a = max(0, m.start() - 40); bad += 1
                print(f'{p.relative_to(EDITION)}: {name}: ...{t[a:m.end() + 30]!r}')
        if p.suffix.lower() in ('.pptx',):
            for m in PRON.finditer(t):
                a = max(0, m.start() - 30); bad += 1
                print(f'{p.relative_to(EDITION)}: pronoun: ...{t[a:m.end() + 20]!r}')
print(bad, 'findings')
sys.exit(1 if bad else 0)
