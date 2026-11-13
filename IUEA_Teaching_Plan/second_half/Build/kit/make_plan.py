"""The plan document for the second half of Semester 1 (Weeks 8 to 12). python3 kit/make_plan.py"""
import subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
BUILD = HERE.parent
sys.path.insert(0, str(BUILD / 'templates_gen'))
from docx_kit import *  # noqa

def bullets(d, items, size=10, after=2):
    for it in items:
        p = para(d, '', size, after=after)
        p.paragraph_format.left_indent = Cm(0.5); p.paragraph_format.first_line_indent = Cm(-0.4)
        add_run(p, '•  ', size, True)
        if isinstance(it, tuple):
            add_run(p, it[0] + ' ', size, True); add_run(p, it[1], size)
        else:
            add_run(p, it, size)

d = new_doc('Plan for Weeks 8 to 12', 'IUEA Machine Learning for Engineers')
title(d, 'Weeks 8 to 12: four classes, concepts first, then the lab', 'CML3111, CML3112 and CML3113  |  Written 2 November 2026  |  Updated 3 and 4 November 2026, and on 13 November 2026: the Engineering ML project is now one online window, Monday 23 to Wednesday 25 November, after Class 3')
h2(d, 'Where we are', 0)
para(d, 'Weeks 1 to 7 are done. Week 7 was Practical Test 1. The Week 8 theory was taught to CML3111 and CML3113 on Friday 30 October without the lab. CML3112 starts Week 8 tomorrow, Tuesday 3 November. The semester now ends at Week 12, and Practical Test 2 is dropped, so the remaining teaching fits four classes and the Engineering ML project (3 hours, individual, online, marked by computer), which since 13 November runs in one online window after Class 3. Topics we cannot reach (support vector machines, random forests, boosting, clustering, neural networks and more) move to next semester. They are named in the decks so nobody is surprised.', 10, after=4)
h2(d, 'Calendar')
grid(d, [['Class 1: your first model', 'Tue 3 Nov', 'Fri 6 Nov (concepts recap, then the lab)', 'Week 8 content'], ['Class 2: classification', 'Tue 10 Nov', 'Fri 13 Nov', 'Week 9 content'],
         ['Class 3: can I trust this model; project announced, rehearsal released after the class', 'Tue 17 Nov', 'Fri 20 Nov', 'Week 10 content'],
         ['Engineering ML project, online (3 hours from Start, individual, auto-graded)', 'Mon 23 Nov 00:00 to Wed 25 Nov 23:59', 'Mon 23 Nov 00:00 to Wed 25 Nov 23:59', 'Project window'],
         ['Class 4: features, choosing a model (not in the project)', 'Tue 24 Nov (window still open)', 'Fri 27 Nov (window closed)', 'Week 11 content']], [5.6, 3.4, 5.8, 2.6], header=['Class', 'CML3112', 'CML3113 and CML3111', 'Label'], size=9, label_cols=(0,))
para(d, 'All times are Kampala time. The project dates are confirmed (decision of 13 November 2026). Project marks are final by Wednesday 2 December. The week number names the content, as in the Week 6 waiver note. The Friday cohorts are one week behind the Tuesday cohort in date, and they catch up because Class 1 for them is a recap and a long lab, not a full teaching of the theory.', 9.5, italic=True, before=3, after=4)
h2(d, 'How each class runs')
bullets(d, [('Concepts first, no laptops.', 'Fourteen to eighteen slides, each with a drawn picture, plain words and one small example you can follow by hand. Spoken script in the notes of every slide.'),
            ('One switch.', 'A black divider slide, "Part 2: the lab", marks the move to the notebook. After it the deck has four short slides: the lab map, the numbers to check, the error cards and how the class counts.'),
            ('A lab that explains itself.', 'One notebook per class and cohort. Each step is PREDICT, RUN, READ, CHANGE, in plain words, with the data and units of the cohort. The numbers it prints are checked against a NumPy reference that was compared with scikit-learn.'),
            ('Cohort overlay.', 'Same structure for all. CML3112 uses building cooling load (kW), CML3113 crusher energy demand (kWh/t), CML3111 motor winding temperature (deg C).')], 10)
h2(d, 'What each class teaches')
grid(d, [['1 First model', 'Features and target; baseline; error, MAE, RMSE; gradient descent in plain words; hidden rows (train, validation, test by equipment group); filling blanks from training rows; a line and a tree; the scoreboard'],
         ['2 Classification', 'Yes or no from a limit; why accuracy misleads (always-say-no baseline); scaling; logistic regression and the S curve; a tree that classifies; confusion matrix; precision, recall, F1; the threshold; ROC and AUC'],
         ['3 Trust', 'Underfitting, good fit and memorising (the depth curve); K-fold and group folds with an average and a spread; leakage and its three routes; reproducibility; functions on records; the project announcement (online window, how to sit it, the AI rule)'],
         ['4 Choosing', 'Building and testing a feature (ablation); not using equipment_id; ridge and nearest neighbours as previews; a fair comparison of five candidates; latency and the client\'s rule; the decision memo; the test set (opened once). Not in the project']],
     [3.0, 14.4], header=['Class', 'Ideas, in the order they are taught'], size=9)
h2(d, 'Assessment from now on')
para(d, 'Two blocks of two classes. The graded notebooks, graders and quiz banks for A7 to A11 and Q7 to Q12 already existed, so they are re-used. The source files, syllabi, master plan, quiz banks, student guides and Apps Script helpers are patched (originals kept in _backup_2026-11-02 folders). The live Google Forms and sheets change only when you run the steps in Block_Assessment_By_Hand_Checklist_2026-11-02.md.', 10, after=4)
grid(d, [['Block 1 (Classes 1 and 2)', 'A7 Regression and baseline (20) + A8 Classification and cost (20) = 40', 'Q7 + Q8, five questions each = 10', 'Last 20 minutes of Class 2'],
         ['Block 2 (Classes 3 and 4)', 'A9 Validation and trust (20) + A10 Features and ablation (20) + A11 Model recommendation (20) = 60', 'Q9 + Q10, five questions each = 10', 'Last 20 minutes of Class 4'],
         ['Retired', 'Weeks 12 and 13 assignment and quiz slots as separate events: A11 is folded into Block 2, Q11 and Q12 are not sat', '', '']],
     [3.6, 6.8, 3.9, 3.1], header=['Block', 'Assignment', 'Quiz', 'Sitting'], size=9, label_cols=(0,))
para(d, 'Applied (option A): Q10 currently tests Week 11 features. Class 4 also teaches model comparison (the Q11 topic). Option A: swap two Q10 questions for two Q11 questions. Option B: keep Q10 as it is. The bank is edited and replaceWeek11Questions() swaps the questions on the live forms when you run it.', 9.5, before=4, after=3)
para(d, 'Applied: deadlines. Same pattern as before, a week after the quiz class. Proposed Block 1 assignment: CML3112 Tue 17 Nov 11:00, CML3113 Fri 20 Nov 08:00, CML3111 Fri 20 Nov 11:00. Proposed Block 2 assignment: CML3112 Tue 1 Dec 11:00, CML3113 Fri 4 Dec 08:00, CML3111 Fri 4 Dec 11:00. Block 1 matches your current dates for CML3112 and CML3113 and CML3111. Block 2 moves earlier by about a week because the semester ends at Week 12.', 9.5, after=3)
para(d, 'Course weights (policy of 10 November 2026, Grading_Policy_2026-11-10.md): assignments 20 (A1 to A5, all five count equally), quizzes 20 (Q1 to Q5, all five count equally), Practical Test 1 20, Engineering ML project 40. The Block 1 and Block 2 assignments (A7 to A11) and quizzes (Q7 to Q10) above are practice: they are still set, collected and given feedback, but they do not count toward the final mark. The machine learning project counts 40 percent of the course (Part A 30 + Part B 15 = 45 marks, scaled to 40; see the next section). Results are provisional out of 60 until the project is marked. Check the full set of weights against IUEA regulations before it is published to students.', 9.5, after=3)
h2(d, 'The Engineering ML project: online, 23 to 25 November')
para(d, 'Decision of 13 November 2026 (it replaces the Week 12 class-slot sittings of 4 November): the project is one online window for all three cohorts, Monday 23 November 2026 00:00 to Wednesday 25 November 2026 23:59, Kampala time. Each student has 3 hours from pressing Start, capped at the close of the window, so a student should start by 20:59 on Wednesday to get the full time. It is sat online from anywhere, on the student\'s own laptop and own Google account; there is no room and no in-person invigilation. The lecturer answers wording and technical questions on the class channel from 08:00 to 20:00 each day of the window (hours to confirm). A student whose laptop or connection fails reports it at once on the class channel with a screenshot, and the lecturer can authorise one fresh attempt, still capped at the close of the window. The AI rule and the declaration stay; copy and identity checks run, and any student may be asked after the window, on an online call, to explain or change their code.', 10, after=4)
para(d, 'It is individual and fully automatic, and it counts 40 percent of the course: Part A, the coded notebook, 30 marks; Part B, the decision memo form inside the notebook, 15 marks; 45 marks scaled to 40. It covers Weeks 1 to 7 and Classes 1 to 3. Class 4 is not in it, so there is no feature ablation, and the rule for choosing a model is given in the notebook as an instruction. The data are one real dataset for every student: the energy use (kWh) of a steel plant, split by month, so the model is judged on months it has not seen. Class 3 announces the project and the unmarked rehearsal (practice notebook and practice data) is released right after it: CML3112 Tuesday 17 November, CML3113 and CML3111 Friday 20 November. Marks are final by Wednesday 2 December. Everything for it is in second_half/Project/: the student briefs, the rehearsal and the marked notebook, the grader specification with its proofs, the deployment bundle for the portal and collector, the gradebook export, and a marking guide.', 10, after=4)
h2(d, 'What is built and where')
grid(d, [['Class decks (12)', 'second_half/Slides/<cohort>/', 'KLAi branded, concepts then lab, spoken script in notes, drawn diagrams'], ['Lab notebooks (12)', 'second_half/Lab Notebooks/<cohort>/', 'PREDICT, RUN, READ, CHANGE; run end to end against a NumPy stand-in'],
         ['Student slides as PDF (12)', 'second_half/Student Slides PDF/', 'Slides only, no speaker notes, for revision'], ['Student packs (12)', 'second_half/Student Packages/', 'Notebook, CSV and a one-page START_HERE per class and cohort'], ['Lecturer guides (4)', 'second_half/Lecturer Guides/', 'Clock for Tuesday and Friday, slide map, probes, lab numbers per cohort, rescue plans'],
         ['Engineering ML project (40 percent of the course)', 'second_half/Project/', 'Briefs, rehearsal and project notebook, grader specification with proofs, portal and collector bundle, gradebook export, marking guide, README'], ['Rebuild kit', 'second_half/Build/', 'AUTHORING_GUIDE.md, content/, kit/, ref/']], [3.4, 6.0, 8.0], header=['What', 'Where', 'Notes'], size=9, label_cols=(0,))
h2(d, 'What you still have to do by hand')
bullets(d, ['Open each notebook once in real Colab and run all cells. I could only run them against a NumPy stand-in for scikit-learn, so the one risk is a small difference in a tree split or in the logistic weights. The guides list the numbers to look at.',
            'Tell the Friday cohorts that Class 1 is a recap and a long lab, and that Week numbers describe content.',
            'Send each class pack ZIP to the cohort after the class (or before, if you prefer).',
            'Run the Apps Script steps in Block_Assessment_By_Hand_Checklist_2026-11-02.md, in order, to change the live forms and deadlines.',
            'For the project, follow Project/deploy/DEPLOYMENT_STEPS.md and the Lecturer_Marking_Guide.pdf: confirm the support hours, run the rehearsal and the project notebook once in real Colab with real scikit-learn, deploy the portal and collector bundle, set the window (Monday 23 November 00:00 to Wednesday 25 November 23:59), and after it closes run the grading and read the spot-check list.',
            'Old decks for Weeks 8 to 15 and their ZIPs are untouched. Use the new decks from now on.'], 10)
h2(d, 'Risks I want you to know')
bullets(d, ['Four classes is tight for the whole of regression, classification, trust and choosing. If a class runs over, the guide says what to cut. The lab is never cut.',
            'Validation sets have 15 rows and three positives in Class 2, so every score is shaky. The decks say so, because it is the honest message.',
            'The Week 8 assignment notebook the students already have asks for the same two functions as before. Nothing changes there.'], 10)
save(d, BUILD.parent / 'Plan_Weeks_8-12.docx')
subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', str(BUILD.parent), str(BUILD.parent / 'Plan_Weeks_8-12.docx')], capture_output=True)
