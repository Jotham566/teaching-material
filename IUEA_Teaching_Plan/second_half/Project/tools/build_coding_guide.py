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
            run(p, ' ', 3.5, font=CODE_FONT)
            continue
        if '#' in line and not line.lstrip().startswith(('"', "'")) and '"#' not in line:
            i = line.index('#')
            if line[:i].strip():
                run(p, line[:i], 7.0, color=INK, font=CODE_FONT)
            run(p, line[i:], 7.0, color=COMMENT, font=CODE_FONT)
        else:
            run(p, line, 7.0, color=INK, font=CODE_FONT)
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
        run(p, label + ': ', 8, bold=True, color=TEAL)
        run(p, text, 8)


def heading(d, text, right):
    p = d.add_paragraph()
    tight(p, before=5, after=1.5)
    run(p, text, 10, bold=True, color=TEAL)
    run(p, '   ' + right, 8, color=GREY)


def main():
    cfg = P.REHEARSAL
    p = P.pipeline(cfg)
    n, vm, vr, w = p['n'], p['validation_mae'], p['validation_rmse'], p['warning_scores']
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
    p1 = d.add_paragraph(); tight(p1, after=3)
    run(p1, 'Lecturer copy, do not post. CML3112 Tuesday 17, CML3113 and CML3111 Friday 20 November. ', 8.5, bold=True, color=GREY)
    run(p1, f'The rehearsal notebook, split random_state={seed} (the project uses 17, so its numbers differ). Type each block under its task, run it, '
            'and read the printout with the class. Rehearsal_Answers_<course>.ipynb has all of it if you need to catch up (Runtime > Run all). '
            'Enter with 26/DEMO/001/LECTURER. Run Setup first, then read "The data" together: one row is one sale, or one machine run; '
            'sale_price_usd and failure are the targets.', 8.5, color=GREY)

    heading(d, 'Task 1. Clean the two tables', '6 marks, about 20 minutes')
    code_block(d, WA.answer('clean', seed))
    notes(d, 'Look before you clean. A duplicate counts one sale twice; a row with no price teaches nothing; an area of 0 or a house built in 2108 is a typing slip. '
             'Other gaps stay: the imputer fills them from the training rows only.',
          f'10 and 12 duplicates; 6 and 8 rows with no target. {n["houses_raw"]:,} to {n["houses"]:,} houses; {n["machines_raw"]:,} to {n["machines"]:,} machines.',
          'Why not drop every row that has any gap?')

    heading(d, 'Task 2. Split into training, validation and test sets', '2 marks, 10 minutes')
    code_block(d, WA.answer('split', seed))
    notes(d, 'Test first, then validation from the rest: 60/20/20. The seed gives everyone the same rows. The test rows stay sealed until Task 6.',
          f'Houses {n["houses_train"]:,}, {n["houses_valid"]:,}, {n["houses_test"]:,}. Machines {n["machines_train"]:,}, {n["machines_valid"]:,}, {n["machines_test"]:,}.',
          'What goes wrong if we pick the model on the test rows?')

    heading(d, 'Task 3. Question 1: predict the sale price', '13 marks with the chart, about 25 minutes')
    code_block(d, WA.answer('regression', seed))
    notes(d, 'Create, fit on train, predict valid. The pipeline learns the medians from train only, so nothing leaks. The baseline (the training mean) is the bar every model must beat.',
          f'MAE {f(vm["baseline"])}, {f(vm["linear"])}, {f(vm["tree"])} USD. RMSE {f(vr["baseline"])}, {f(vr["linear"])}, {f(vr["tree"])}.',
          'Why is RMSE always at least as big as MAE?')

    heading(d, 'Task 3b. Do the text columns help?', '2 marks, 10 minutes')
    code_block(d, WA.answer('encoded', seed))
    notes(d, 'One-hot: one 0 or 1 column per category, learned from train. handle_unknown="ignore" gives a category train never saw all zeros instead of an error. A comparison only.',
          f'{f(enc)} USD against {f(vm["linear"])}: the text columns help.',
          'A neighbourhood the training rows never saw: what happens without "ignore"?')

    heading(d, 'Task 4. Question 2: warn of a machine failure', '3 marks, 15 to 30 minutes')
    code_block(d, WA.answer('warning', seed))
    notes(d, 'Logistic regression gives a probability; warn at 0.5 or more. Failures are rare (3 runs in 100), so at 0.5 most are missed. '
             'CML3112 has not had Class 2: draw the 2 by 2 table on the board first.',
          f'TP {w["tp"]}, FP {w["fp"]}, FN {w["fn"]}, TN {w["tn"]:,}. Precision 0.62, recall {w["recall"]:.2f}.',
          'For the maintenance manager, which costs more: a false alarm or a missed failure?')

    heading(d, 'Tasks 5 and 6. Choose one model, then use the test set once', '2 marks, 15 minutes')
    code_block(d, WA.answer('choose', seed) + '\n' + WA.answer('test', seed))
    notes(d, 'The rule chooses on validation numbers only. Then refit on train and valid together (more data) and score the test rows once. Report what comes out.',
          f'{p["chosen_model"]} (the tree, {f(vm["tree"])}, is over the {cfg["max_mae"]:,} limit). Test MAE {f(test["mae"])} USD, recall {test["warning"]["recall"]:.2f}.',
          'The test MAE is lower than validation. Is the model better than we thought?')

    heading(d, 'Task 7. The MEMO form', '15 marks, 10 minutes')

    notes(d, 'Fill each number from a variable, for example "test_mae": round(test_mae, 2); never type it. Show how to judge a limit, but do not give the letters: the project uses the same lists.',
          'True letters (yours only): ' + '; '.join(f'{c[-4:]} limits {", ".join(l)}, next {x}' for c, (l, x) in letters.items()) + '.',
          'Why is the test set used only once, at the end?')

    heading(d, 'Finish, and the mistakes to watch for', '10 minutes')
    pm = d.add_paragraph(); tight(pm, after=1)
    run(pm, 'Runtime > Restart session and run all, Ctrl+S, then Check my work on the entry page (one to three minutes). No Submit button: at the deadline the work is collected. ', 8.5)
    run(pm, 'Watch for: ', 8.5, bold=True, color=TEAL)
    run(pm, 'changing houses_raw itself; filling every gap in Task 1 (that is the imputer\'s job); another split seed or order; the imputer or the mean fitted on '
            'train and valid together; RMSE without the square root; > 0.5 instead of >= 0.5; reading houses_test before Task 6; typed numbers (the marking re-runs '
            'every task on hidden rows, so only calculated results count); editing Setup (it is put back before marking).', 8.5)

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
