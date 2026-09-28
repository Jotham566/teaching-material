"""Five-page quick guide to the revised beginner teaching route."""
from pathlib import Path
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.oxml.ns import qn
from beginner_pathway import WEEKS, VIDEOS
ROOT=Path(__file__).resolve().parents[1]
d=Document();s=d.sections[0];s.page_width=Cm(21);s.page_height=Cm(29.7)
s.top_margin=s.bottom_margin=Cm(1.7);s.left_margin=s.right_margin=Cm(2)
for name in ('Normal','Title','Heading 1','Heading 2'):
 d.styles[name].font.name='Calibri';d.styles[name].font.color.rgb=RGBColor(0,0,0)
d.styles['Normal'].font.size=Pt(10.5);d.styles['Normal'].paragraph_format.space_after=Pt(7)
d.styles['Title'].font.size=Pt(24);d.styles['Heading 1'].font.size=Pt(15);d.styles['Heading 2'].font.size=Pt(12)
for element in list(d.styles.element.iter()):
 if element.tag==qn('w:pBdr'):element.getparent().remove(element)
def p(t):d.add_paragraph(t)
def h(t):d.add_paragraph(t,'Heading 1')
def page(title):d.add_page_break();d.add_paragraph(title,'Title')
def week(w):
 x=WEEKS[w];h(f'Week {w}  {x["title"]}');p('Teach: '+x['core']);p('Check: '+x['gate']);p('Defer: '+x['stretch'])
d.add_paragraph('Teaching complete beginners','Title')
p('Lecturer quick guide | Revised 21 September 2026')
p('Use this route for CML3111 and CML3113 from Week 2, and CML3112 from Week 3. Students need an explanation and a small successful attempt before independent work. Completed teaching and existing marks are preserved. The Week 2 checklist states the catch-up deadlines.')
h('Open one place before class')
p('In IUEA_Teaching_Plan/decks, open the PowerPoint for your cohort and week. Use Slide Show for teaching and Presenter View for the explanation prompts in the speaker notes. The filenames are unchanged.')
p('Teach from the updated PowerPoint. Use its pictures, annotated code and five-minute pair activity. Reveal the discussion answer after students try. Place the activity inside guided-practice time; rehearse test activities before the assessed period.')
h('What to share')
p('Share the current cohort student ZIP. From Week 3 where relevant, it includes guided_practice.ipynb for the examples shown in the PowerPoint. It follows the revised slide order, with matching slide numbers. The issued Wxx_student.ipynb remains the assignment notebook. For Week 2, proof_of_life.ipynb remains the main notebook and the four repairs stay practice.')
h('Repeat this teaching routine')
for t in ['1. Explain the physical question without coding words. State every quantity and unit.', '2. Define numbers, values and variables before assignment syntax; define every new word before use. Say what each symbol in the code does.', '3. Work one tiny example. Ask everyone to predict a changed value before running it.', '4. Work an analogous example together. In pairs, rotate the person typing.', '5. Give an individual attempt. If many learners struggle, repeat the example and defer stretch content.', '6. Explain the exact assignment output names, required files, checks and deadline. Students save their own work.']:
 p(t)
h('Support without extra marking')
p('Use ungraded predictions, pair explanations and visible practice checks. Hint in stages: restate the question, trace a smaller example, supply the first step, then model an analogous solution. Keep the existing automatic assessment workflow; do not add manually marked worksheets.')
page('The next two teaching weeks')
week(2)
p('For the remaining Week 2 classes, explicitly assign A1 and Quiz 1 as catch-up, alongside A2 and Quiz 2. A1 and A2 use separate forms but the same cohort upload deadline. Each quiz lasts 24 hours from its own activation. The Quick Class Checklist contains all links and controls.')
p('Use the private Week2 Repair Walkthrough for the exact corrections. Add the GitHub concept clips before saving a repository: 00:00–02:10 and 03:35–06:08 of the CodeWithChris video you shared. Desktop installation is optional; the course browser workflow remains the default.')
week(3)
p('After values, variables, types and operators, use each cohort’s simple formula: floor area for CML3112, pump flow for CML3113, DC electrical power for CML3111. Explain all quantities rather than assuming discipline knowledge. Then introduce reusable functions using double_value, return and a guarded division.')
p('A3 is five named tasks. Explain the published formulas, signed percentage error and zero-input rule before independent attempts. A five-function library and six bug hunts are not additional core assignments.')
h('Three-hour teaching rhythm')
p('00–15 recall/access; 15–30 plain explanation; 30–50 worked example and optional short clip; 50–80 guided attempt; 80–90 break; 90–125 supported practice; 125–140 assignment bridge; 140–165 individual attempt/recovery; 165–170 quiz; 170–180 save and submission instructions.')
p('Quizzes still open manually for 24 hours from activation. Scheduled, released assignment uploads still open automatically. Use the Quick Class Checklist for controls and links. Assignment forms now accept any Student Registration Number format; the field is still required.')
page('Tables cleaning and the first test')
for w in (4,5,6):week(w)
h('Week 7 preparation')
p('Rehearse the offline environment, public interfaces and saving both notebook and typed Part B before the test. Keep the official assessment timetable. Confirm lab readiness and the separate grading release checks.')
p('Friday 9 October is a holiday. CML3111/CML3113 need a supported Week 5 replacement. Announce the actual recording/clinic or approved make-up arrangement; retain 30 minutes of consolidation at the start of Week 6. A video alone is not the replacement lesson.')
page('The modelling sequence')
for w in (8,9,10,11,12):
 x=WEEKS[w];h(f'Week {w}  {x["title"]}');p(x['core']);p('Before independent work: '+x['gate'])
h('Correct these ideas explicitly')
p('MAE is an average error, not a ± guarantee. Teach the required regression tree in Week 8 before it is assessed. Keep repeated equipment groups together and fit preprocessing only on training data. Select models on validation data, reserving the final test. Lowering a classification threshold does not guarantee precision falls at every step.')
page('Projects videos and the weekly check')
for w in (13,14,15):
 x=WEEKS[w];h(f'Week {w}  {x["title"]}');p(x['core']);p(x['bridge'])
h('Short video use')
p('The PowerPoints contain clickable choices for Git, Python arithmetic, boxplots, regression, confusion matrices and cross-validation. Preview before class, state one listening question, play about four minutes at most, pause and do the related exercise. Optional entries still marked preview-required have not had a complete audiovisual review.')
p('Your GitHub link originally starts at 02:47, during installation. Your Colab link starts at 17:14 of a 22:23 tutorial. Share the un-timestamped links for optional revision. GPUs, TPUs and extra installations in tutorials are not Week 2 requirements.')
h('Before each class')
p('Open the actual cohort PowerPoint and run its practice notebook. Read the assignment brief and quiz privately. Rehearse any syntax used by the quiz, including the examples in the slides and speaker notes. Check the student ZIP and submission link. Preview the chosen clip, or use the local example if video access fails.')
p('Beginner_Lecturer_Guide.md gives weekly guidance. Curriculum_Benchmark_and_Teaching_Map.md lists the research and activities. Major projects, tests and demos still require their separate grading-readiness checks before release.')
d.save(ROOT/'IUEA_Teaching_Plan/IUEA_ML_Beginner_Teaching_Quick_Guide.docx')
