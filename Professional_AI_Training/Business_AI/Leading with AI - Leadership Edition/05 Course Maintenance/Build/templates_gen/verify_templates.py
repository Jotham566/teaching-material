"""Verify the templates: recalculate every workbook with LibreOffice (on a copy), check for formula errors,
check each docx opens and carries the KLAi footer, and scan all text for banned wording.
Run: python3 verify_templates.py"""
import re, shutil, subprocess, sys, tempfile, zipfile
from pathlib import Path
from openpyxl import load_workbook
from docx import Document
from common import *

XLSX = ['Use-Case Scorecard', 'Information Inventory', 'Document Review Table', 'Automation Test Log', 'Risk Register',
        'Vendor Question List', 'Business Case Workbook', '90-Day Roadmap']
DOCX = ['Task Card', 'Reliability Test Record', 'Reusable Brief Template', 'Tool Boundary Sheet', 'AI Use Policy Template']
KIT_X = ['Results Tracker']
KIT_D = ['30-60-90 Check-in Form', 'Sponsor Briefing']
ERRS = ('#REF!', '#NAME?', '#VALUE!', '#DIV/0!', '#N/A', '#NUM!', '#NULL!', 'Err:')
BANNED = [(r'—', 'em dash'), (r'–', 'en dash'), (r',\s+not\s', '", not" construction'), (r'\b(exam|exams|marks|grading|graded|grade)\b', 'exam or marks language'),
          (r'\b(fee|fees|tuition)\b', 'course price word'), (r'\bhonestly|genuinely|straightforward|dive into|unlock|journey|embark|game-changer|leverage\b', 'banned word'),
          (r'\bnot (a|an|the)\b[^.]{0,40}\bbut\b', 'not-but construction')]
problems = []


def bad(msg):
    problems.append(msg); print('PROBLEM:', msg)


def scan(text, label):
    for pat, what in BANNED:
        for m in re.finditer(pat, text, re.I):
            if what == 'course price word' and label.startswith(('Vendor', 'Document Review')) or (what == 'course price word' and 'fee' in m.group(0).lower() and False):
                continue
            ctx = text[max(0, m.start() - 30): m.end() + 30].replace('\n', ' ')
            bad(f'{label}: {what}: "...{ctx}..."')


BUILD_TERMS = r'apps script|zapier|turneverythingoff|\btriggers?\b|\bscripts?\b|google script|we built|you built|build guide'


def scan_build(text, label):
    """Learners no longer build automations: templates and the follow-up kit must not say or imply it."""
    for m in re.finditer(BUILD_TERMS, text, re.I):
        ctx = text[max(0, m.start() - 30): m.end() + 30].replace('\n', ' ')
        bad(f'{label}: build wording: "...{ctx}..."')


def recalc(src, outdir):
    dst = Path(outdir) / src.name
    shutil.copy(src, dst)
    conv = Path(outdir) / 'conv'; conv.mkdir(exist_ok=True)
    subprocess.run(['soffice', '--headless', '--convert-to', 'xlsx', '--outdir', str(conv), str(dst)], capture_output=True, timeout=180)
    return conv / src.name


def check_xlsx(path):
    with tempfile.TemporaryDirectory() as td:
        out = recalc(path, td)
        if not out.exists():
            bad(f'{path.name}: LibreOffice conversion failed'); return
        wf = load_workbook(path)                 # formulas (original)
        wv = load_workbook(out, data_only=True)  # values after recalculation
        nform = nerr = nnone = 0
        text = []
        for ws in wf.worksheets:
            wsv = wv[ws.title]
            for row in ws.iter_rows():
                for c in row:
                    v = c.value
                    if isinstance(v, str):
                        text.append(v)
                    if isinstance(v, str) and v.startswith('='):
                        nform += 1
                        val = wsv[c.coordinate].value
                        if isinstance(val, str) and val.startswith(ERRS):
                            nerr += 1; bad(f'{path.name}!{ws.title}!{c.coordinate}: {val}')
        if nform == 0 and path.stem not in ('Vendor Question List',):
            print(f'  note: {path.name} has no formulas')
        scan('\n'.join(text), path.name); scan_build('\n'.join(text), path.name)
        if path.stem == 'Document Review Table':
            check_review_quotes(wf)
        print(f'OK  {path.name}: {nform} formulas, {nerr} errors, sheets: {", ".join(w.title for w in wf.worksheets)}')
        return wv


def check_review_quotes(wf):
    """Example rows quote the Busoga Oils agreement word for word, with the clause number that holds the quote."""
    agr = ' '.join((EDITION / '03 Learner Materials' / 'Practice Files' / '01 Case Company' / 'supplier_agreement_busoga_oils.txt').read_text(encoding='utf-8').split())
    ws = wf['Review']
    n = 0
    for r in range(4, 7):
        quote = ' '.join(str(ws.cell(r, 8).value or '').strip('"').split())
        clause = str(ws.cell(r, 4).value or '')
        n += 1
        if quote not in agr:
            bad(f'Document Review Table row {r}: quote is not in the agreement: {quote[:60]}')
        m = re.search(r'(\d+)\. [^\n]*?' + re.escape(quote[:30]), agr)
        num = re.search(r'\d+', clause)
        # find the clause whose text holds the quote
        pos = agr.find(quote)
        heads = [(mm.start(), int(mm.group(1))) for mm in re.finditer(r'(?:(?<=\s)|^)(\d{1,2})\. [A-Z][a-z]', agr)]
        holder = max((h for h in heads if h[0] < pos), default=(0, 0))[1]
        if not num or int(num.group()) != holder:
            bad(f'Document Review Table row {r}: clause says "{clause}" but the quote is in clause {holder}')
    print(f'   Review table: {n} example quotes found word for word in the agreement')


def check_docx(path):
    try:
        d = Document(str(path))
    except Exception as e:
        bad(f'{path.name}: does not open: {e}'); return
    ft = ' '.join(p.text for s in d.sections for p in s.footer.paragraphs)
    want = FOOT + path.stem
    if want not in ft:
        bad(f'{path.name}: footer "{ft}" lacks "{want}"')
    sec = d.sections[0]
    if abs(sec.page_width.cm - 21.0) > 0.05 or abs(sec.page_height.cm - 29.7) > 0.05:
        bad(f'{path.name}: page is not A4')
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        if not any(n.startswith('word/media/') for n in names):
            bad(f'{path.name}: no logo image in the header')
    body = '\n'.join(p.text for p in d.paragraphs)
    for t in d.tables:
        for r in t.rows:
            for c in r.cells:
                body += '\n' + c.text
    scan(body, path.name); scan_build(body, path.name)
    check_docx_sections(path, d, body)
    print(f'OK  {path.name}: opens, footer ok, A4, logo present')


GUIDES = []   # the Zapier and Apps Script build guides moved to Archive/v2_before_technical_2026-11-05/practice_files on 6 Nov 2026


def check_docx_sections(path, d, body):
    """Session 11 permissions table and Session 13 policy sections must match the slides."""
    if path.stem == 'Tool Boundary Sheet':
        for must in ('It may', 'A person approves', 'It must never', 'Read', 'Write', 'Send', 'Spend', 'Limits', 'Stop conditions', 'Off switch', 'Review date', 'Owner', 'Reviewed with', 'Level of freedom'):
            if must not in body:
                bad(f'Tool Boundary Sheet: lacks "{must}" from the Session 11 permissions table')
    if path.stem == 'AI Use Policy Template':
        heads = [p.text for p in d.paragraphs if re.match(r'\d+\. ', p.text)]
        want = ['Purpose', 'Scope', 'Approved tools', 'What data may and may not go in', 'Human review and records', 'Disclosure', 'Accounts and ownership', 'Incidents', 'Training and AI literacy', 'Review date', 'Approval']
        got = [re.sub(r'^\d+\. ', '', h) for h in heads]
        if got != want:
            bad(f'AI Use Policy Template: sections {got} differ from {want}')
        for must in ('Data class', 'Personal flag', 'Public', 'Internal', 'Confidential', 'Questions to take to my lawyer', 'stop or switch off', 'record what happened'):
            if must not in body:
                bad(f'AI Use Policy Template: lacks "{must}"')


def check_guides():
    """The four build documents: open, KLAi footer, no [confirm] in the learner guides, required wording, banned words."""
    base = EDITION / '03 Learner Materials'
    for sub, n, learner in GUIDES:
        p = base / sub / f'{n}.docx'
        if not p.exists():
            bad(f'missing {p.name}'); continue
        d = Document(str(p))
        ft = ' '.join(x.text for sec in d.sections for x in sec.footer.paragraphs)
        if FOOT + n not in ft:
            bad(f'{n}: footer lacks "{FOOT + n}"')
        body = '\n'.join(x.text for x in d.paragraphs)
        for t in d.tables:
            for r in t.rows:
                for c in r.cells:
                    body += '\n' + c.text
        scan(body, n)
        low = body.lower()
        if learner and '[confirm]' in low:
            bad(f'{n}: the learner guide still has a [confirm] marker')
        if re.search(r'need to write code|do not need to code|no coding needed', low):
            bad(f'{n}: says the learner does not write code')
        if learner:
            if 'Your screen may use slightly different names. Follow what you see.' not in body:
                bad(f'{n}: lacks the standard screen sentence')
            if re.search(r'\bconfirm(ed)?\b', low) and 'confirm' in low.replace('confirm which way', '').replace('confirm that', '').replace('confirm the', ''):
                pass
        if n == 'Apps Script Build Guide':
            for must in ('read short code and change three words', 'Make a copy', 'NVF Apps Script Practice', 'last_month_summary_by_hand' if False else 'hand_summary', 'between 7:00 and 8:00', 'start plus review', 'IT approval', 'runs as its owner'):
                if must not in body:
                    bad(f'{n}: lacks "{must}"')
        if n == 'Zapier Build Guide':
            if body.lower().count('six parts') < 3 or re.search(r'\bfive (main )?steps\b', low):
                bad(f'{n}: must say six parts everywhere and never five steps')
            for must in ('Before Session 6', 'Zapier Practice', 'Make a copy', 'trial NOT started' if False else 'Do not start the free trial', 'Fallback A needs no card', 'FLAG', 'stop condition'):
                if must not in body:
                    bad(f'{n}: lacks "{must}"')
        if n == 'Apps Script Rehearsal Checklist' and 'hand_summary' not in body:
            bad(f'{n}: lacks the sheet preparation steps')
        if n == 'Zapier Rehearsal Checklist' and 'Make a copy' not in body:
            bad(f'{n}: lacks the sheet preparation steps')
        print(f'OK  {n}.docx: opens, footer ok, wording checks done')


def check_dates_and_columns():
    """Follow-up kit dates, tracker and test log columns."""
    wb = load_workbook(TEMPLATES / 'Automation Test Log.xlsx')
    heads = [c.value for c in wb['Test log'][3]]
    if 'Minutes to review' not in heads or 'Minutes to start' not in heads:
        bad('Automation Test Log: lacks Minutes to start / Minutes to review')
    wb = load_workbook(FOLLOWUP / 'Results Tracker.xlsx')
    heads = ' '.join(str(c.value) for c in wb['Monthly results'][3])
    if 'Incidents' not in heads:
        bad('Results Tracker: no Incidents column')
    ws = wb['Monthly results']
    mins = [ws.cell(r, 6).value for r in (4, 5, 6)]
    if mins != [35, 35, 35] or [ws.cell(r, 5).value for r in (4, 5, 6)] != [25, 25, 25] or [ws.cell(r, 4).value for r in (4, 5, 6)] != [90, 90, 90]:
        bad('Results Tracker: example minutes must be 35 now, 25 planned, 90 by hand')
    wb = load_workbook(TEMPLATES / '90-Day Roadmap.xlsx')
    import datetime as dt
    want = ['Phase', 'Action', 'Owner', 'Start', 'Due', 'Effort (hours)', 'Depends on', 'Success measure', 'Status']
    got = [c.value for c in wb['Roadmap'][3]][:9]
    if got != want:
        bad(f'90-Day Roadmap: columns {got} differ from {want}')
    blocks = {'Protect and clean': (dt.date(2027, 2, 1), dt.date(2027, 3, 3)), 'Describe and prepare': (dt.date(2027, 3, 4), dt.date(2027, 4, 2)), 'Test and decide': (dt.date(2027, 4, 3), dt.date(2027, 5, 2))}
    slide = {'1': ('Sarah Namukasa', dt.date(2027, 2, 26), 4), '2': ('Joseph Mugisha', dt.date(2027, 2, 19), 6), '3': ('Peter Okello', dt.date(2027, 3, 26), 8),
             '4': ('David Kato', dt.date(2027, 4, 2), 5), '5': ('Grace Akello', dt.date(2027, 4, 23), 10), '6': ('Sarah Namukasa', dt.date(2027, 4, 30), 2)}
    n = 0
    for row in wb['Roadmap'].iter_rows(min_row=4, max_col=9):
        tag, act, own, st, due, eff = (row[i].value for i in range(6))
        if act and tag:
            n += 1
            d0 = due.date() if hasattr(due, 'date') else due
            s0 = st.date() if hasattr(st, 'date') else st
            blk = blocks.get(tag)
            if blk is None:
                bad(f'90-Day Roadmap: Phase "{tag}" is not one of the three Session 14 phase names'); continue
            if not (blk[0] <= d0 <= blk[1]):
                bad(f'90-Day Roadmap: example due date {d0} is outside phase {tag}')
            if s0 > d0:
                bad(f'90-Day Roadmap: start {s0} is after due {d0}')
            k = act.split()[0]
            if k not in slide or slide[k] != (own, d0, eff):
                bad(f'90-Day Roadmap: row "{act}" differs from the Session 14 slide: {own}, {d0}, {eff}')
    if n != 6:
        bad(f'90-Day Roadmap: expected 6 example rows, found {n}')
    r = wb['Roadmap']
    if r['L4'].value != dt.datetime(2027, 2, 1):
        bad('90-Day Roadmap: example start date must be 1 February 2027')
    if [r['L5'].value, r['L6'].value, r['L7'].value] != ['=IF(L4="","",L4+30)', '=IF(L4="","",L4+60)', '=IF(L4="","",L4+90)']:
        bad('90-Day Roadmap: check-in formulas must be start + 30, 60, 90')
    # the Risk Register columns (Session 13) and the Information Inventory (Session 14)
    wr = load_workbook(TEMPLATES / 'Risk Register.xlsx')
    hr = [c.value for c in wr['Register'][3]]
    for must in ('Risk', 'Score', 'Level', 'Owner', 'Control'):
        if must not in hr:
            bad(f'Risk Register: lacks column {must}')
    if sum(1 for r_ in range(4, 12) if wr['Register'].cell(r_, 2).value) != 8:
        bad('Risk Register: expected eight typical rows')
    wi = load_workbook(TEMPLATES / 'Information Inventory.xlsx')
    hi = [c.value for c in wi['Inventory'][3]]
    for must in ('Source (what it is)', 'Owner', 'Format', 'Where it lives', 'Who may see it', 'Sensitivity', 'Ready for AI'):
        if must not in hi:
            bad(f'Information Inventory: lacks column {must}')
    if 'Readiness scorecard' not in wi.sheetnames:
        bad('Information Inventory: lacks the sheet Readiness scorecard')
    else:
        sc = wi['Readiness scorecard']
        areas = [sc.cell(r_, 1).value for r_ in range(4, 10)]
        if areas != ['Inventory', 'Readable', 'Complete and unique', 'Metadata', 'Rights', 'Current']:
            bad(f'Readiness scorecard: areas {areas}')
        pts = {'Green': 2, 'Amber': 1, 'Red': 0}
        if sum(pts[sc.cell(r_, 4).value] for r_ in range(4, 10)) != 6:
            bad('Readiness scorecard: NVF example must total 6 of 12')
        if sc['G10'].value != '=IF(COUNT(G4:G9)=6,SUM(G4:G9),"")':
            bad('Readiness scorecard: total formula missing')
    # Business case defaults come from the Session 12 Task Card
    wbk = load_workbook(TEMPLATES / 'Business Case Workbook.xlsx')
    inp = wbk['Inputs']
    vals = {inp.cell(r_, 1).value: inp.cell(r_, 2).value for r_ in range(4, 15)}
    if (vals['Times a month'], vals['Minutes each time today'], vals['Share of runs with an error today'], vals['Cost of one error']) != (4, 90, 0.4, 150000):
        bad('Business Case Workbook: baseline defaults differ from the Session 12 Task Card (4, 90, 0.4, 150000)')
    if inp['B12'].value != 10 or inp['B13'].value != 20:
        bad('Business Case Workbook: own minutes B12 must be 10 and review B13 20 (Session 12 slides)')
    if 'Stop rules' not in wbk.sheetnames:
        bad('Business Case Workbook: lacks the sheet Stop rules')
    print('OK  follow-up dates and new columns')


def main():
    for n in XLSX:
        p = TEMPLATES / f'{n}.xlsx'
        if not p.exists(): bad(f'missing {p.name}'); continue
        wv = check_xlsx(p)
        if n == 'Business Case Workbook' and wv:
            r = wv['Result']
            print('   Result sheet values:', {r.cell(i, 1).value: r.cell(i, 2).value for i in range(4, 17)})
            s = wv['Sensitivity']
            print('   Sensitivity base check:', s['C14'].value)
    for n in DOCX:
        p = TEMPLATES / f'{n}.docx'
        if not p.exists(): bad(f'missing {p.name}'); continue
        check_docx(p)
    for n in KIT_X:
        p = FOLLOWUP / f'{n}.xlsx'
        if not p.exists(): bad(f'missing {p.name}'); continue
        check_xlsx(p)
    for n in KIT_D:
        p = FOLLOWUP / f'{n}.docx'
        if not p.exists(): bad(f'missing {p.name}'); continue
        check_docx(p)
    check_guides()
    check_dates_and_columns()
    print('\nTotal problems:', len(problems))
    sys.exit(1 if problems else 0)


if __name__ == '__main__':
    main()
