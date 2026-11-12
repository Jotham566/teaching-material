"""Industry Use-Case Atlas and Questions to Ask (Leading with AI, 12 November 2026).

Run from Build/: python kit/make_atlas.py   (also called by make_docs.py).
Atlas: every case in research/*.md grouped by industry, with what the AI does, the result, the catch and the source, and the sessions that use it (kit/sessions_plan.py).
Questions to Ask: every 'Questions to ask' table slide of the session files, grouped by session.
Writes 03 Learner Materials/Industry Use-Case Atlas.docx and Questions to Ask.docx (+ .pdf)."""
import glob
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUILD = HERE.parent
EDITION = BUILD.parent.parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(BUILD / 'templates_gen'))
from docx_kit import *  # noqa
from sessions_plan import S as PLAN

IND = [('BNK', 'Banking and microfinance'), ('TEL', 'Telecom and mobile money'), ('AGR', 'Agriculture and agribusiness'), ('MFG', 'Manufacturing and FMCG'),
       ('HLT', 'Healthcare and insurance'), ('PUB', 'Public sector'), ('ENR', 'Energy, mining, oil and gas'), ('RTL', 'Retail, logistics and transport'),
       ('EDU', 'Education'), ('LGL', 'Legal and professional services'), ('GAP', 'Search, African-language models and Uganda'),
       ('PPL', 'People and work (all industries)'), ('ADO', 'Adoption (all industries)'), ('GOV', 'Governance and law')]
FIELDS = {'what': r'What (?:the AI does|happened|the system did|it is)', 'result': r'Result[^:]*', 'source': r'Source[^:]*', 'caution': r'Caution', 'conf': r'Confidence', 'org': r'Organisation[^:]*'}


def cases():
    out = {}
    for f in sorted(glob.glob(str(BUILD / 'research' / '*.md'))):
        cur = None
        for line in open(f):
            m = re.match(r'#{2,4} ([A-Z]{3}-\d+)[ :.\-–]+(.*)', line)
            if m:
                cur = out.setdefault(m.group(1), {'title': m.group(2).strip()})
                continue
            if cur is None:
                continue
            for k, pat in FIELDS.items():
                mm = re.match(r'- (?:\*\*)?(' + pat + r'):?(?:\*\*)?:?\s*(.*)', line.strip())
                if mm and k not in cur:
                    cur[k] = mm.group(2).replace('**', '').strip()
    return out


_TEXT = {}


def _session_text(n):
    if n not in _TEXT:
        try:
            _TEXT[n] = (BUILD / 'content' / f's{n:02d}.py').read_text().lower()
        except OSError:
            _TEXT[n] = ''
    return _TEXT[n]


def sessions_using(cid, title=''):
    """Sessions whose content names the case's organisation (the title before any colon, without brackets)."""
    key = re.sub(r'\(.*?\)', '', title.split(':')[0]).strip().lower()
    key = re.sub(r'\s+(failure|mixed|people|regulator|measure).*$', '', key)
    key = key.replace('"', '').replace('“', '').replace('”', '')
    words = key.split()
    keys = [key] + ([' '.join(words[:2])] if len(words) > 2 and len(' '.join(words[:2])) >= 8 else []) + ([words[0]] if words and len(words[0]) >= 6 and words[0] not in GENERIC else [])
    keys = [k for k in keys if len(k) >= 3 and k not in GENERIC]
    pats = [re.compile(r'(?<![a-z])' + re.escape(k) + r'(?![a-z])') for k in keys]
    return ', '.join(str(n) for n in range(15) if any(p.search(_session_text(n)) for p in pats))


GENERIC = {'uganda', 'uganda\'s', 'kenya', 'nigeria', 'national', 'microsoft', 'google', 'african', 'customer-support', 'generative', 'government', 'copilot', 'south', 'commonwealth', 'digital', 'customer', 'national', 'african union', 'rising', 'farmers'}


def clip(t, n=420):
    t = re.sub(r'https?://\S+', '', t or '').strip()
    return t if len(t) <= n else t[:n].rsplit(' ', 1)[0] + ' ...'


def to_pdf(path):
    subprocess.run(['soffice', '-env:UserInstallation=file:///tmp/lo_atlas', '--headless', '--convert-to', 'pdf', '--outdir', str(path.parent), str(path)], capture_output=True)


def atlas():
    C = cases()
    name = 'Industry Use-Case Atlas'
    d = new_doc(name)
    title(d, 'Industry Use-Case Atlas', f'Leading with AI. {len(C)} named, sourced cases by industry: what the AI does, the result, the catch, and the session that teaches it. Researched 11 November 2026.')
    box(d, 'How to read this atlas', [
        'Each case names a real organisation. Figures are quoted as the source states them; many are the company’s own claims, and the catch says so. Check a figure again before you quote it in your organisation.',
        'Sessions: where the case is taught in the course. Cases with no session are extra reading for your industry.',
        'Full blocks with links, confidence and cautions are in 05 Course Maintenance/Build/research.'], size=9)
    for code, label in IND:
        ids = sorted((k for k in C if k.startswith(code)), key=lambda k: int(k.split('-')[1]))
        if not ids:
            continue
        page_break(d)
        h2(d, f'{label}  ({len(ids)} cases)', 0)
        rows = []
        for k in ids:
            c = C[k]
            ttl = c['title']
            src = clip(c.get('source', ''), 160)
            rows.append([f'{ttl}', clip(c.get('what', ''), 300), clip(c.get('result', ''), 360), clip(c.get('caution', ''), 260) + (f'\nSource: {src}' if src else ''), sessions_using(k, c['title'])])
        grid(d, rows, [3.4, 3.8, 4.0, 4.6, 1.6], header=['Case', 'What the AI does', 'Result', 'The catch, and the source', 'Sessions'], size=7, hdr_size=7.5)
    out = EDITION / '03 Learner Materials' / (name + '.docx')
    save(d, out); to_pdf(out)


def questions():
    import deck
    name = 'Questions to Ask'
    d = new_doc(name)
    title(d, 'Questions to Ask', 'Leading with AI. The questions from every session, for your vendors, your IT and data teams, and your board. Take this page to the next AI proposal.')
    for n in range(0, deck.NSESS + 1):
        try:
            s = deck.load(n)
        except Exception:
            continue
        rows = []
        for sl in s['slides']:
            if 'question' in sl.get('title', '').lower() and sl.get('rows'):
                rows += [[r[0], r[1] if len(r) > 1 else ''] for r in sl['rows']]
        if not rows:
            continue
        h2(d, f'Session {n}: {s["title"]}')
        grid(d, rows, [8.2, 9.2], header=['Ask', 'Why it matters'], size=8.5, label_cols=(0,))
    out = EDITION / '03 Learner Materials' / (name + '.docx')
    save(d, out); to_pdf(out)


def build():
    atlas(); questions()


if __name__ == '__main__':
    build()
