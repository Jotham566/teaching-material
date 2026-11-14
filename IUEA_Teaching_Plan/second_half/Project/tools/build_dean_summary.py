"""The final practical project: a short memo to the Dean's office (all three courses).

Plain document in the lecturer's own voice, no company branding. The facts that can drift (window, rehearsal dates, marks,
support hours, results date, citation) are checked against project_content and the contracts, so the memo cannot disagree
with what students receive. Run:  python3 IUEA_Teaching_Plan/second_half/Project/tools/build_dean_summary.py
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

PART_A = [('Clean the real data (dates, an all-zero reading, a column that leaks the answer, impossible values)', 7),
          ('Two labelled charts of the data', 2),
          ('Split the year by month into training, validation and test sets (the rule is given)', 2),
          ('Train a baseline model, linear regression and a decision tree, each with missing values filled from training rows', 6),
          ('Measure the error: MAE and RMSE', 3),
          ('No data leakage: anything learned from the data comes from training rows only', 2),
          ('Warning question: logistic regression, with the confusion matrix, precision and recall at a cut-off of 0.5', 3),
          ('Test set opened once, after the model is chosen, and its result', 2),
          ('Results on the data file, a fixed random seed, the required functions present', 3)]
PART_B = [('Recommended model', 3), ('Validation error of the three models', 3), ('Test-set error and warning recall', 2),
          ('How much better the recommended model is than the baseline', 1), ('Three true limits of the study, chosen from ten statements', 3),
          ('Best next step, chosen from five', 1), ('Two short written answers: why this model, and why the test set is opened only once', 2)]


def check_facts():
    assert sum(m for _, m in PART_A) == PC.AUTO_MARKS == 30 and len(PART_A) == 9
    assert sum(m for _, m in PART_B) == PC.PART_B == 15
    assert PC.WINDOW['opens'] == 'Monday 23 November 2026, 00:00' and PC.WINDOW['closes'] == 'Wednesday 25 November 2026, 23:59'
    assert PC.WINDOW['last_full_start'] == 'Wednesday 25 November 2026, 20:59'
    assert PC.RESULTS_BY == 'Wednesday 2 December 2026' and PC.MINUTES == 180
    assert PC.SUPPORT_HOURS.startswith('08:00 to 20:00')
    assert '10.24432/C52G8C' in PC.CITATION
    return {c: PC.COHORT[c]['class3'] for c in ('CML3112', 'CML3113', 'CML3111')}


def run(p, text, bold=False, italic=False, size=10.5, color=None):
    r = p.add_run(text)
    r.bold, r.italic = bold, italic
    r.font.size = Pt(size)
    r.font.name = FONT
    r._element.get_or_add_rPr().get_or_add_rFonts().set(qn('w:eastAsia'), FONT)
    if color:
        r.font.color.rgb = RGBColor.from_string(color)
    return r


def para(d, text='', bold=False, size=10.5, before=0, after=6, italic=False):
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
    st = d.styles['Normal']; st.font.name = FONT; st.font.size = Pt(10.5)
    d.core_properties.title = 'Final practical project: questions, instructions and conduct'
    d.core_properties.author = 'Jotham Martin Wambi'

    para(d, 'International University of East Africa, Faculty of Engineering', True, 10.5, after=10)
    for k, v in [('To', 'The Dean, Faculty of Engineering'), ('From', 'Jotham Martin Wambi, lecturer, Machine Learning for Engineers'),
                 ('Courses', 'CML3111, CML3112 and CML3113 (Year 3)'), ('Date', '14 November 2026'),
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
    bullet(d, 'Students use their own laptop and Google account and work in Google Colab. They sign in on an entry page that checks their '
              'registration number against the class list. Pressing Start creates their own copy of the notebook in my Google Drive and '
              'shares it with them.', 'Setup.')
    bullet(d, 'There is no submit button to forget. At each student\'s deadline their access ends and the work saved by then is '
              'collected automatically. The notebook also keeps a backup every five minutes, so a student who runs out of time, loses '
              'power or works in a copy of the file still has their work marked. Nothing saved after the deadline counts.', 'Collection.')
    bullet(d, 'I answer questions about wording and technical problems on the class channel from 08:00 to 20:00 on each day of the window. '
              'If a student\'s laptop or connection fails, they report it at once with a screenshot and I can give one fresh attempt, still '
              'ending at the window\'s close.', 'Support.')
    bullet(d, f'Students get an unmarked practice version right after Class 3: CML3112 on {rehearsal["CML3112"]}, CML3113 and CML3111 on '
              f'{rehearsal["CML3111"]}. It uses the same file with a different target, so it does not give away the real questions. I will work through it with each class in that week\'s revision class.', 'Rehearsal.')

    heading(d, '2. The data')
    para(d, 'Every student gets the same real dataset: one year (2018) of electricity readings from a steel plant in Gwangyang, South Korea, '
            'taken every 15 minutes, 35,040 rows in all. It is published on the UCI Machine Learning Repository under a CC BY 4.0 licence '
            '(Sathishkumar V E, Shin and Cho, 2021, doi:10.24432/C52G8C). The file is stored inside each student\'s notebook and checked when '
            'it is written out, so nothing needs to be downloaded during the window.')
    para(d, 'I chose real data on purpose. Students have to deal with the things real data does: the last reading of each day is stamped with '
            'the wrong date, one reading is all zeros because the meter recorded nothing, and one column is calculated from the very quantity '
            'they are asked to predict, so using it would be cheating without knowing it. I checked the file myself and nothing has been added '
            'to it or changed.')

    heading(d, '3. The questions')
    para(d, 'Students act as analysts for the plant\'s energy manager and answer two questions.', after=3)
    bullet(d, 'How much energy will the plant use in each 15-minute period, in kWh, for months the model has not seen? Students compare three '
              'models (a simple baseline that predicts the average, linear regression and a decision tree) and report the errors.', 'Question 1.')
    bullet(d, 'Should a reading raise a warning? A reading at or above 60 kWh in a quarter hour is a warning, since that is when peak-demand '
              'charges build up. Students estimate a probability for each reading with logistic regression and, at a cut-off of 0.5, report how '
              'many warnings they catch, miss and raise wrongly. This question carries only 3 of the 30 marks.', 'Question 2.')
    para(d, 'They train on January to August, check on September and October, and keep November and December as a test set that they may '
            'open only once, after they have chosen their model. They finish with a short decision memo for the manager. The 60 kWh limit '
            'and the manager\'s limits on error (10 kWh) and response time (50 ms) are set by me for teaching and are stated as such in the '
            'brief. The rule for choosing the model is given to them in the notebook.', before=3)

    heading(d, '4. Tasks and marks')
    para(d, 'Part A is the coded notebook, 30 marks. Students write the code for each step as a function.', after=3)
    table(d, [[t, m] for t, m in PART_A] + [['Total', 30]], [13.6, 2.6], ['Part A task', 'Marks'])
    para(d, 'Part B is the decision memo, 15 marks, written as a short form inside the notebook.', after=3)
    table(d, [[t, m] for t, m in PART_B] + [['Total', 15]], [13.6, 2.6], ['Part B field', 'Marks'])
    para(d, 'The 45 marks are scaled to 40 percent. The project rests on what all three classes have been taught: Python and data handling '
            '(Weeks 1 to 7) and the regression workflow of Week 8. The warning question uses Week 9, which two classes had as a lecture; '
            'all three meet it again in next week\'s revision class. I have left out cross-validation and the later topics, which there was '
            'no time to teach before the window.')

    heading(d, '5. Rules for students')
    bullet(d, 'Colab, the course slides, their lab notebooks, the revision guide and their own notes.', 'Allowed:')
    bullet(d, 'Any AI tool (ChatGPT, Gemini, Copilot or similar) and any help from another person. Students sign a declaration when they '
              'submit that the work is their own.', 'Not allowed:')
    bullet(d, 'Students may write their answers in cells of their own. A correct answer earns its marks wherever it is in the notebook. '
              'I applied the same rule when re-checking Practical Test 1 and the coding assignments.', 'Own cells:')

    heading(d, '6. Marking')
    bullet(d, 'The notebooks are marked by computer, as Practical Test 1 was, but now as each one arrives, in a locked-down copy of the '
              'Colab setup. Each student\'s functions are run on rows they have never seen, so they need working code, and copying another '
              'student\'s printed numbers earns almost nothing (1 mark of 30). On submitting, a student sees at once that the notebook arrived, '
              'runs from the top and has every required part. The marks are released after the window closes.', 'Automatic.')
    bullet(d, 'Before release I ran the marking on 161 prepared notebooks, correct, partly correct, wrong and dishonest ones, and each received '
              'the mark it should.', 'Tested.')
    bullet(d, 'The computer compares all notebooks for copied code and copied written answers, and checks each notebook against the identity '
              'used at entry. I look at every flagged case myself. Because the project is unsupervised, I may also ask any student to explain or '
              'change their code in a short online call after the window.', 'Honesty.')
    bullet(d, 'Marks will be final by Wednesday 2 December 2026, after questions and checks are settled. Each student receives written '
              'feedback for each task.', 'Results.')

    heading(d, '7. Still to be done before the window')
    bullet(d, 'Switch on the automatic marking and the submission page, then run the whole process once in Colab myself, from entry to marked result.')
    bullet(d, 'Confirm the 08:00 to 20:00 support hours with the three classes.')
    bullet(d, 'Any student with approved extra time or another arrangement: I would be grateful to know by 20 November so it can be set up.')

    para(d, after=14)
    t = d.add_table(rows=2, cols=3); borders(t)
    for j, lab in enumerate(['Course lecturer', 'Head of Department', 'Dean, Faculty of Engineering']):
        c = t.rows[0].cells[j]; c.width = Cm(5.4); run(c.paragraphs[0], lab, size=9.5)
        c2 = t.rows[1].cells[j]; run(c2.paragraphs[0], '\n\nSignature and date', size=8.5, color='777777')

    d.save(str(OUT))
    prof = Path(tempfile.gettempdir()) / 'iuea_dean_lo'
    (prof / 'user' / 'fonts').mkdir(parents=True, exist_ok=True)
    for f in (PC.PLAN / 'second_half/Build/brand/fonts').glob('Lato-*.ttf'):
        shutil.copy2(f, prof / 'user' / 'fonts' / f.name)
    subprocess.run(['soffice', f'-env:UserInstallation=file://{prof}', '--headless', '--convert-to', 'pdf', '--outdir', str(OUT.parent), str(OUT)],
                   capture_output=True)
    print('wrote', OUT.name, 'and', OUT.with_suffix('.pdf').name)


if __name__ == '__main__':
    build()
