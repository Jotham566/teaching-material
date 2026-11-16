"""The lecturer's coding guide for the revision class (16 November 2026): two A4 pages, Word and PDF.
python3 tools/build_coding_guide.py

The code is the code of tools/worked_answers.py with the rehearsal seed (the same code as Lecturer Guides/Rehearsal_Answers_<course>.ipynb).
Every number on the page is computed by the reference (project_numpy_reference.py) for the rehearsal split, so the guide and the notebook agree.
"""
import subprocess
import sys
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import project_content as PC  # noqa: E402
import project_numpy_reference as P  # noqa: E402
import memo_spec as M  # noqa: E402
import worked_answers as WA  # noqa: E402
from build_project_docs import lato_profile, soffice, pdf_fonts  # noqa: E402

OUT = PC.PLAN / 'second_half/Lecturer Guides/Revision_Coding_Guide.docx'
TEAL, INK, GREY, COMMENT, PALE = RGBColor(0x12, 0x65, 0x73), RGBColor(0x17, 0x2C, 0x40), RGBColor(0x52, 0x65, 0x77), RGBColor(0x2E, 0x7D, 0x32), 'EEF3F6'
CODE_FONT, TEXT_FONT = 'Courier New', 'Lato'


def shade(cell, hex_fill):
    tc = cell._tc.get_or_add_tcPr()
    sh = OxmlElement('w:shd')
    sh.set(qn('w:val'), 'clear'); sh.set(qn('w:color'), 'auto'); sh.set(qn('w:fill'), hex_fill)
    tc.append(sh)


def no_borders(table):
    tbl = table._tbl.tblPr
    borders = OxmlElement('w:tblBorders')
    for side in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        e = OxmlElement(f'w:{side}'); e.set(qn('w:val'), 'nil'); borders.append(e)
    tbl.append(borders)


def cell_margins(cell, cm=0.12):
    tc = cell._tc.get_or_add_tcPr()
    mar = OxmlElement('w:tcMar')
    for side in ('top', 'bottom', 'left', 'right'):
        e = OxmlElement(f'w:{side}'); e.set(qn('w:w'), str(int(cm * 567))); e.set(qn('w:type'), 'dxa'); mar.append(e)
    tc.append(mar)


def run(p, text, size=8.5, bold=False, italic=False, color=INK, font=TEXT_FONT):
    r = p.add_run(text)
    r.bold, r.italic = bold, italic
    r.font.size, r.font.name, r.font.color.rgb = Pt(size), font, color
    r._element.rPr.rFonts.set(qn('w:eastAsia'), font)
    return r


def tight(p, before=0, after=0, line=1.0):
    pf = p.paragraph_format
    pf.space_before, pf.space_after, pf.line_spacing = Pt(before), Pt(after), line


def code_block(d, code):
    """Full-width shaded box; comments in green, code in ink, one paragraph per line."""
    t = d.add_table(rows=1, cols=1)
    no_borders(t)
    c = t.rows[0].cells[0]
    shade(c, PALE); cell_margins(c, 0.15)
    first = True
    for line in code.rstrip('\n').split('\n'):
        p = c.paragraphs[0] if first else c.add_paragraph()
        first = False
        tight(p, line=0.92)
        if not line.strip():                      # a blank line between steps: a half-height gap
            run(p, ' ', 2.5, font=CODE_FONT)
            continue
        if '#' in line and not line.lstrip().startswith(('"', "'")) and '"#' not in line:
            i = line.index('#')
            if line[:i].strip():
                run(p, line[:i], 6.7, color=INK, font=CODE_FONT)
            run(p, line[i:], 6.7, color=COMMENT, font=CODE_FONT)
        else:
            run(p, line, 6.7, color=INK, font=CODE_FONT)
    return t


def notes(d, say, expect, ask):
    t = d.add_table(rows=1, cols=3)
    no_borders(t)
    widths = (8.4, 5.4, 4.6)
    for cell, (label, text), w in zip(t.rows[0].cells, (('Say', say), ('Expect', expect), ('Ask', ask)), widths):
        cell.width = Cm(w)
        cell_margins(cell, 0.08)
        p = cell.paragraphs[0]
        tight(p, before=1, after=1, line=1.0)
        run(p, label + ': ', 7.6, bold=True, color=TEAL)
        run(p, text, 7.6)


def heading(d, text, right):
    p = d.add_paragraph()
    tight(p, before=3.5, after=1)
    run(p, text, 9.5, bold=True, color=TEAL)
    run(p, '   ' + right, 8, color=GREY)


def main():
    cfg = P.REHEARSAL
    p = P.pipeline(cfg)
    n, vm, vr, w, wt = p['n'], p['validation_mae'], p['validation_rmse'], p['warning_scores'], p['tree_warning_scores']
    test = P.test_expected(p['chosen_model'], cfg)
    enc = P.errors([r[P.H_TARGET] for r in p['houses_valid']], P.encoded_regression(p['houses_train'], P.strip(p['houses_valid'], P.H_TARGET), cfg))['mae']
    seed = cfg['split_seed']
    f = lambda x: f'{x:,.0f}'
    letters = {}
    for code in ('CML3111', 'CML3112', 'CML3113'):
        lim, nxt = M.options(code)
        letters[code] = (''.join(l for l, _, ok, _ in lim if ok)[:3], [l for l, _, ok, _ in nxt if ok][0])

    d = Document()
    s = d.sections[0]
    s.page_width, s.page_height = Cm(21.0), Cm(29.7)
    s.left_margin = s.right_margin = Cm(1.3)
    s.top_margin, s.bottom_margin = Cm(1.0), Cm(0.9)
    st = d.styles['Normal']
    st.font.name, st.font.size = TEXT_FONT, Pt(9)

    p0 = d.add_paragraph(); tight(p0, after=1)
    run(p0, 'Revision class: the coding guide', 15, bold=True, color=INK)
    p1 = d.add_paragraph(); tight(p1, after=2)
    run(p1, 'Lecturer copy, do not post. CML3112 Tuesday 17, CML3113 and CML3111 Friday 20 November. ', 8.5, bold=True, color=GREY)
    run(p1, f'Rehearsal, random_state={seed} (project: 17). Enter with 26/DEMO/001/LECTURER, run Setup, read "The data". Type each block, run it, read the '
            'printout together. Backup: Rehearsal_Answers_<course>.ipynb, Run all. Finish Question 1 before opening Question 2.', 8.5, color=GREY)

    def question(text):
        pq = d.add_paragraph(); tight(pq, before=5, after=0)
        run(pq, text, 11.5, bold=True, color=INK)

    question('Question 1: what will a house sell for? (regression, houses only)')
    heading(d, 'Task 1. Clean the house table', '3 marks + chart, 15 minutes')
    code_block(d, WA.answer('clean_h', seed))
    notes(d, 'Look first. A duplicate counts a sale twice; no price teaches nothing; an area of 0 or a 2108 build year is a slip. Other gaps stay for the imputer.',
          f'10 duplicates, 6 with no price. {n["houses_raw"]:,} to {n["houses"]:,} houses.',
          'Why not drop every row that has any gap?')
    heading(d, 'Task 2. Split the houses', '1 mark, 5 minutes')
    code_block(d, WA.answer('split_h', seed))
    notes(d, 'Test first, then validation from the rest: 60/20/20. Same seed, same rows for everyone. Test stays sealed until Task 4.',
          f'{n["houses_train"]:,}, {n["houses_valid"]:,}, {n["houses_test"]:,}.',
          'What goes wrong if we pick the model on the test rows?')
    heading(d, 'Task 3. Linear regression and a decision tree', '11 marks with Chart 2, 20 minutes')
    code_block(d, WA.answer('regression', seed))
    notes(d, 'Create, fit on train, predict valid. Medians come from train only, so nothing leaks. RMSE punishes big misses.',
          f'MAE {f(vm["linear"])} and {f(vm["tree"])} USD. RMSE {f(vr["linear"])} and {f(vr["tree"])}.',
          'Why is RMSE always at least as big as MAE?')
    heading(d, 'Task 3b. Do the text columns help?', '2 marks, 10 minutes')
    code_block(d, WA.answer('encoded', seed))
    notes(d, 'One 0/1 column per category, learned from train; "ignore" gives an unseen category all zeros. A comparison only.',
          f'{f(enc)} USD against {f(vm["linear"])}: the text columns help.',
          'A neighbourhood train never saw: what happens without "ignore"?')
    heading(d, 'Task 4. Choose the house model, then use the test set once', '1 mark, 10 minutes')
    code_block(d, WA.answer('test_h', seed))
    notes(d, 'Choose on validation numbers only; refit on train + valid; score the test rows once and report what comes out.',
          f'{p["chosen_model"]} (the tree, {f(vm["tree"])}, is over the {cfg["max_mae"]:,} limit). Test MAE {f(test["mae"])} USD.',
          'The test MAE is lower than validation. Is the model better than we thought?')

    question('Question 2: will this machine run fail? (classification, machines only)')
    heading(d, 'Tasks 5 and 6. Clean and split the machine table', '4 marks, 10 minutes')
    code_block(d, WA.answer('clean_m', seed) + '\n' + WA.answer('split_m', seed))
    notes(d, 'The same steps as Question 1, on a new table. product_type becomes a number: a model needs numbers.',
          f'12 duplicates, 8 with no label. {n["machines_raw"]:,} to {n["machines"]:,}; {n["machines_train"]:,}, {n["machines_valid"]:,}, {n["machines_test"]:,}.',
          'Which steps were the same as for the houses?')
    heading(d, 'Task 7. Logistic regression and a decision tree', '5 marks, 25 minutes')
    code_block(d, WA.answer('classify', seed))
    notes(d, 'Logistic gives a probability (warn at 0.5 or more); the tree answers 0 or 1. Failures are rare, so both miss most. CML3112: draw the 2 by 2 table first.',
          f'Logistic TP {w["tp"]}, FP {w["fp"]}, FN {w["fn"]}, F1 {w["f1"]:.3f}. Tree TP {wt["tp"]}, FP {wt["fp"]}, FN {wt["fn"]}, F1 {wt["f1"]:.3f}.',
          'For the maintenance manager, which costs more: a false alarm or a missed failure?')
    heading(d, 'Task 8. Choose the warning model, then use the test set once', '1 mark, 10 minutes')
    code_block(d, WA.answer('test_m', seed))
    notes(d, 'The higher validation F1 wins; refit on train + valid; score the test runs once.',
          f'{p["chosen_warning"]} (F1 {wt["f1"]:.3f} against {w["f1"]:.3f}). Test F1 {test["warning"]["f1"]:.3f}.',
          'The two F1 values are very close. Would you trust this choice?')

    heading(d, 'Task 9. The MEMO form', '15 marks, 10 minutes')
    notes(d, 'Each number from a variable, e.g. round(test_mae, 2); never typed. Show how to judge a limit; never give the letters (the project uses the same lists).',
          'True letters (yours only): ' + '; '.join(f'{c[-4:]} limits {", ".join(l)}, next {x}' for c, (l, x) in letters.items()) + '.',
          'Why is the test set used only once, at the end?')
    heading(d, 'Finish, and the mistakes to watch for', '10 minutes')
    pm = d.add_paragraph(); tight(pm, after=1)
    run(pm, 'Restart and run all, Ctrl+S, Check my work. No Submit button. ', 8.5)
    run(pm, 'Watch for: ', 8.5, bold=True, color=TEAL)
    run(pm, 'changing a raw table; filling every gap in cleaning; another split seed; the imputer fitted on train and valid; RMSE without the root; '
            '> 0.5 for >= 0.5; F1 as a plain average; a test table read before its choice; typed numbers or choices (hidden rows catch them).', 8.5)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    d.save(str(OUT))
    r = subprocess.run([soffice(), f'-env:UserInstallation=file://{lato_profile()}', '--headless', '--convert-to', 'pdf', '--outdir', str(OUT.parent), str(OUT)],
                       capture_output=True, text=True, timeout=300)
    pdf = OUT.with_suffix('.pdf')
    if r.returncode or not pdf.exists():
        raise SystemExit('PDF conversion failed: ' + r.stderr[-300:])
    if not any('Lato' in x for x in pdf_fonts(pdf)):
        raise SystemExit('the PDF does not embed Lato')
    print('wrote', OUT.name, 'and', pdf.name)


if __name__ == '__main__':
    main()
