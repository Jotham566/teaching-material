"""The final practical project: a short memo to the Dean's office (all three courses).

Plain document in the lecturer's own voice, no company branding. The facts that can drift (window, rehearsal dates, marks,
support hours, results date, citation) are checked against project_content and the contracts, so the memo cannot disagree
with what students receive. Run:  python3 IUEA_Teaching_Plan/Weeks_08-12/Project/tools/build_dean_summary.py
Writes Project/Dean_Summary_ML_Project.docx and .pdf.
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import project_content as PC  # noqa: E402

FONT = 'Lato'
OUT = PC.PROJECT / 'Dean_Summary_ML_Project.docx'

PART_A = [('Question 1 (house prices): clean the table, removing duplicates, rows with no price and impossible values', 3),
          ('Question 1: split into training, validation and test sets (60, 20 and 20 percent; the code is given)', 1),
          ('Question 1: train linear regression and a decision tree, with missing values filled from training rows', 4),
          ('Question 1: measure the error, MAE and RMSE', 3),
          ('Question 1: no data leakage (anything learned from the data comes from training rows only)', 2),
          ('Question 1: two labelled charts', 2),
          ('Question 1: do the text columns help? One-hot encoding (shown in the revision class)', 2),
          ('Question 1: choose the model with the given rule, then use the test set once', 1),
          ('Question 2 (machine failure): clean the table', 3),
          ('Question 2: split into training, validation and test sets', 1),
          ('Question 2: train logistic regression and a decision tree classifier', 3),
          ('Question 2: confusion matrix counts, precision, recall and F1 for both', 2),
          ('Question 2: choose the model with the higher F1, then use the test set once', 1),
          ('Results on the data, a fixed random seed, all required results present', 2)]
PART_B = [('Recommended house model', 2), ('Validation error of the two house models', 2), ('Recommended warning model', 2),
          ('Validation F1 of the two warning models', 1), ('Test results of both questions', 2), ('Three true limits of the study, chosen from ten statements', 3),
          ('Best next step, chosen from five', 1), ('Two short written answers: why this model, and why the test set is used only once', 2)]


def proof_count():
    import json
    data = json.loads((PC.PROJECT / 'grader_spec/proof_results.json').read_text())
    assert all(c['ok'] for c in data['cases']), 'a proof case fails: run grader_spec/run_proofs.py first'
    return len(data['cases'])


def check_facts():
    assert sum(m for _, m in PART_A) == PC.AUTO_MARKS == 30 and len(PART_A) == 14
    assert sum(m for _, m in PART_B) == PC.PART_B == 15
    assert PC.WINDOW['opens'] == 'Monday 23 November 2026, 00:00' and PC.WINDOW['closes'] == 'Wednesday 25 November 2026, 23:59'
    assert PC.WINDOW['last_full_start'] == 'Wednesday 25 November 2026, 20:59'
    assert PC.RESULTS_BY == 'Wednesday 2 December 2026' and PC.MINUTES == 180
    assert PC.SUPPORT_HOURS.startswith('08:00 to 20:00')
    assert '10.24432/C5HS5C' in PC.CITATION and 'De Cock' in PC.CITATION
    return {c: PC.COHORT[c]['class3'] for c in ('CML3112', 'CML3113', 'CML3111')}


def run(p, text, bold=False, italic=False, size=10, color=None):
    r = p.add_run(text)
    r.bold, r.italic = bold, italic
    r.font.size = Pt(size)
    r.font.name = FONT
    r._element.get_or_add_rPr().get_or_add_rFonts().set(qn('w:eastAsia'), FONT)
    if color:
        r.font.color.rgb = RGBColor.from_string(color)
    return r


def para(d, text='', bold=False, size=10, before=0, after=6, italic=False):
    p = d.add_paragraph()
    p.paragraph_format.space_before, p.paragraph_format.space_after = Pt(before), Pt(after)
    p.paragraph_format.line_spacing = 1.15
    if text:
        run(p, text, bold, italic, size)
    return p


def heading(d, text):
    p = para(d, text, True, 12, before=10, after=4)
    p.paragraph_format.keep_with_next = True
    return p


def bullet(d, text, lead=None):
    p = para(d, after=3)
    p.paragraph_format.left_indent = Cm(0.6)
    p.paragraph_format.first_line_indent = Cm(-0.4)
    run(p, '•  ')
    if lead:
        run(p, lead + ' ', True)
    run(p, text)


def borders(table):
    b = OxmlElement('w:tblBorders')
    for side in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        e = OxmlElement(f'w:{side}')
        e.set(qn('w:val'), 'single'); e.set(qn('w:sz'), '4'); e.set(qn('w:color'), '999999')
        b.append(e)
    table._tbl.tblPr.append(b)


def table(d, rows, widths, header):
    t = d.add_table(rows=0, cols=len(widths))
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    t.autofit = False
    borders(t)
    grid = t._tbl.tblGrid
    for j, w in enumerate(widths):
        grid.gridCol_lst[j].set(qn('w:w'), str(int(w * 567)))
    for i, row in enumerate([header] + rows):
        cells = t.add_row().cells
        for j, (c, w) in enumerate(zip(cells, widths)):
            c.width = Cm(w)
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(1)
            run(p, str(row[j]), bold=(i == 0 or row[0] == 'Total'), size=9.5)
            if i == 0:
                sh = OxmlElement('w:shd'); sh.set(qn('w:val'), 'clear'); sh.set(qn('w:fill'), 'E8E8E8')
                c._tc.get_or_add_tcPr().append(sh)
    para(d, after=2)
    return t


def build():
    rehearsal = check_facts()
    d = Document()
    sec = d.sections[0]
    sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
    sec.left_margin = sec.right_margin = Cm(2.2)
    sec.top_margin, sec.bottom_margin = Cm(2.0), Cm(2.0)
    st = d.styles['Normal']; st.font.name = FONT; st.font.size = Pt(10)
    d.core_properties.title = 'Final practical project: questions, instructions and conduct'
    d.core_properties.author = 'Jotham Martin Wambi'

    para(d, 'International University of East Africa, Faculty of Engineering', True, 10.5, after=10)
    for k, v in [('To', 'The Dean, Faculty of Engineering'), ('From', 'Jotham Martin Wambi, lecturer, Machine Learning for Engineers'),
                 ('Courses', 'CML3111, CML3112 and CML3113 (Year 3)'), ('Date', '16 November 2026'),
                 ('Subject', 'Final practical project for Semester 1: the questions, the instructions and how it will be taken')]:
        p = para(d, after=2)
        run(p, f'{k}: ', True); run(p, v)
    para(d, after=6)

    para(d, 'This note sets out the final assessment for my three machine learning courses. The project counts for 40 percent of the course mark. '
            'There is no written examination. The other 60 percent comes from the five assignments A1 to A5 (20), the five quizzes Q1 to Q5 (20) '
            'and Practical Test 1 (20), which have already been marked.')

    heading(d, '1. When and how it is taken')
    bullet(d, 'All three courses sit it online in the same window, from Monday 23 November 2026, 00:00 to Wednesday 25 November 2026, 23:59 '
              '(Kampala time). There is no room booking.', 'Window.')
    bullet(d, 'Each student works alone for 3 hours, counted on our server from the moment they press Start. The clock cannot be paused. '
              'A student who starts after 20:59 on Wednesday only has the time left before 23:59.', 'Time.')
    bullet(d, 'Students use their own laptop and Google account and work in Google Colab. On the entry page they choose their course, '
              'type their registration number and their Google email twice. A number that belongs to another course is refused, so no '
              'student can sit another class\'s paper. A student missing from my list can still start, and I confirm their enrolment '
              'afterwards. Pressing Start creates their own copy of the notebook in my Google Drive and shares it with them.', 'Setup.')
    bullet(d, 'There is no submit button to forget. At each student\'s deadline their access ends and the work saved by then is '
              'collected automatically. The notebook also keeps a backup every five minutes, so a student who runs out of time, loses '
              'power or works in a copy of the file still has their work marked. Nothing saved after the deadline counts.', 'Collection.')
    bullet(d, 'I answer questions about wording and technical problems on the class channel from 08:00 to 20:00 on each day of the window. '
              'If a student\'s laptop or connection fails, they report it at once with a screenshot and I can give one fresh attempt, still '
              'ending at the window\'s close.', 'Support.')
    bullet(d, f'Next week is a revision class for each course (CML3112 on {rehearsal["CML3112"]}, CML3113 and CML3111 on {rehearsal["CML3111"]}). '
              'I work through a rehearsal of the project on the projector: the same tasks on the same data, split differently so every number '
              'differs. Students watch and take notes; only I can open the rehearsal. Many students are still finding their feet with the code, '
              'so this is where I take them through it step by step.', 'Rehearsal.')

    heading(d, '2. The data')
    para(d, 'Every student gets the same two tables, built from published data and stored inside the notebook, so nothing is downloaded '
            'during the window. I have organised both before students see them: plain column names, metric units and only the columns '
            'that matter. A notebook cell explains every column.', after=3)
    bullet(d, '2,935 rows of house sales in Ames, Iowa (2006 to 2010) from the city assessor, published for teaching by Dean De Cock '
              '(Journal of Statistics Education, 2011), with 18 columns such as neighbourhood, quality rating, year built, living area '
              'in square metres and the sale price in US dollars.', 'House prices.')
    bullet(d, '10,012 runs of a metal-cutting machine (temperatures, speed, torque, tool wear) with whether it failed, from the UCI Machine '
              'Learning Repository (Matzka, 2020, CC BY 4.0). This table is synthetic, built to mirror real machine records, and the '
              'notebook says so. About 3 percent of runs are failures, which is why precision and recall matter more than accuracy.', 'Machine failure.')
    bullet(d, 'To give students real cleaning to do, I added a few duplicate rows, rows with no target value and impossible values '
              '(for example a negative area) to both tables. The notebook tells students these were added for the exercise. Some real '
              'values are also missing.', 'Cleaning.')

    heading(d, '3. The questions')
    para(d, 'The project is two separate questions. Students finish the first, on the house table only, before they start the second, '
            'on the machine table only. Each question runs the same steps: clean, split, compare two models, choose one, then test it once.', after=3)
    bullet(d, 'What will a house sell for? Students compare linear regression with a decision tree and report the errors in US dollars. '
              'A short extra task asks whether the text columns, such as neighbourhood, improve the prediction when they are encoded as numbers.', 'Question 1.')
    bullet(d, 'Will a machine run fail? Students compare logistic regression with a decision tree classifier and report, for each, how many '
              'failures it catches, misses and raises wrongly, with precision, recall and F1.', 'Question 2.')
    para(d, 'Students split each table themselves into training, validation and test sets (60, 20 and 20 percent) with the code given and a '
            'fixed random seed. A rule given in the notebook chooses each model from the validation results: for the houses, the smaller error '
            'within a client limit (25,000 US dollars and 50 ms, my teaching numbers, stated as such); for the machines, the higher F1. The test '
            'set may be used only once, after the choice. Students finish with a short decision memo.', before=3)

    heading(d, '4. Tasks and marks')
    para(d, 'Part A is the coded notebook, 30 marks. Students write ordinary code under each task and store the results it names; no functions are needed.', after=3)
    table(d, [[t, m] for t, m in PART_A] + [['Total', 30]], [13.6, 2.6], ['Part A task', 'Marks'])
    para(d, 'Part B is the decision memo, 15 marks, written as a short form inside the notebook.', after=3)
    table(d, [[t, m] for t, m in PART_B] + [['Total', 15]], [13.6, 2.6], ['Part B field', 'Marks'])
    para(d, 'The 45 marks are scaled to 40 percent. The project rests on what all three classes have been taught: Python and data handling '
            '(Weeks 1 to 7) and the regression workflow of Week 8. Question 2 uses Week 9 (logistic regression and the decision tree classifier), which two classes had as a lecture, '
            'and CML3112 meets in the revision class. The text-column task uses one-hot encoding, which no class had as a lecture; it carries 2 marks '
            'and I show it in the revision class. There is no simple average (baseline) model: the classes learned that the average is a poor '
            'predictor, so they now compare two real models in each question. I have left out cross-validation and the later topics.')

    heading(d, '5. Rules for students')
    bullet(d, 'Colab, the course slides, their lab notebooks, the revision guide and their own notes.', 'Allowed:')
    bullet(d, 'Any AI tool (ChatGPT, Gemini, Copilot or similar) and any help from another person. By starting, students declare that the '
              'work will be their own.', 'Not allowed:')
    bullet(d, 'Students may write their answers in cells of their own. A correct answer earns its marks wherever it is in the notebook. '
              'I applied the same rule when re-checking Practical Test 1 and the coding assignments.', 'Own cells:')

    heading(d, '6. Marking')
    para(d, 'I have built a grading system for this project: the computer does the marking, and I stay in the loop to check its results '
            'and decide every case it cannot settle.', after=3)
    bullet(d, 'Each notebook is marked as it arrives, in a locked-down copy of the Colab setup. Each student\'s code for every task is '
              'run again on rows they have never seen, so typed or copied numbers earn nothing, and a mistake in one task does not cost '
              'marks in the next. Before the deadline a student can press Check my work to see that the notebook runs and has every '
              'required part. No mark is shown until the window closes.', 'Automatic marking.')
    bullet(d, 'The system flags anything unusual: copied written answers, a notebook that does not match the identity used at entry, '
              'work saved late, or results that were typed rather than calculated. A flag never changes a mark by itself. I review every '
              'flagged case, decide it, and record my decision.', 'Me in the loop.')
    bullet(d, 'Marks will be final by Wednesday 2 December 2026, after my checks and any student questions are settled. Each student '
              'receives written feedback for each task.', 'Results.')

    para(d, 'This note is for your information. I will share the results with the faculty once marking is complete.', before=6)
    para(d, 'Jotham Martin Wambi', bold=True, before=4, after=0)
    para(d, 'Lecturer, Machine Learning for Engineers', after=0)

    d.save(str(OUT))
    prof = Path(tempfile.gettempdir()) / 'iuea_dean_lo'
    (prof / 'user' / 'fonts').mkdir(parents=True, exist_ok=True)
    for f in (PC.PLAN / 'Weeks_08-12/Build/brand/fonts').glob('Lato-*.ttf'):
        shutil.copy2(f, prof / 'user' / 'fonts' / f.name)
    subprocess.run(['soffice', f'-env:UserInstallation=file://{prof}', '--headless', '--convert-to', 'pdf', '--outdir', str(OUT.parent), str(OUT)],
                   capture_output=True)
    print('wrote', OUT.name, 'and', OUT.with_suffix('.pdf').name)


if __name__ == '__main__':
    build()
