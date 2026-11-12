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
title(d, 'Weeks 8 to 12: four classes, concepts first, then the lab', 'CML3111, CML3112 and CML3113  |  Written 2 November 2026  |  Updated 3 and 4 November 2026: the recommendations below were approved and applied, and the project is now an individual, timed, auto-graded sitting in Week 12')
h2(d, 'Where we are', 0)
para(d, 'Weeks 1 to 7 are done. Week 7 was Practical Test 1. The Week 8 theory was taught to CML3111 and CML3113 on Friday 30 October without the lab. CML3112 starts Week 8 tomorrow, Tuesday 3 November. The semester now ends at Week 12, and Practical Test 2 is dropped, so the remaining teaching fits four classes and a project sitting in Week 12 (3 hours, individual, timed and marked by computer). Topics we cannot reach (support vector machines, random forests, boosting, clustering, neural networks and more) move to next semester. They are named in the decks so nobody is surprised.', 10, after=4)
h2(d, 'Calendar')
grid(d, [['Class 1: your first model', 'Tue 3 Nov', 'Fri 6 Nov (concepts recap, then the lab)', 'Week 8 content'], ['Class 2: classification', 'Tue 10 Nov', 'Fri 13 Nov', 'Week 9 content'],
         ['Class 3: can I trust this model', 'Tue 17 Nov', 'Fri 20 Nov', 'Week 10 content'], ['Class 4: features, choosing a model, project rehearsal released', 'Tue 24 Nov', 'Fri 27 Nov', 'Week 11 content'],
         ['Week 12: Project sitting (3 hours, individual, timed, auto-graded)', 'Tue 1 Dec, 11:00 to 14:00', 'Fri 4 Dec: CML3113 08:00 to 11:00, CML3111 11:00 to 14:00', 'Project sitting']], [5.6, 3.4, 5.8, 2.6], header=['Class', 'CML3112', 'CML3113 and CML3111', 'Label'], size=9, label_cols=(0,))
para(d, 'The Week 12 times are proposed, lecturer to confirm. The week number names the content, as in the Week 6 waiver note. The Friday cohorts are one week behind the Tuesday cohort in date, and they catch up because Class 1 for them is a recap and a long lab, not a full teaching of the theory.', 9.5, italic=True, before=3, after=4)
h2(d, 'How each class runs')
bullets(d, [('Concepts first, no laptops.', 'Fourteen to eighteen slides, each with a drawn picture, plain words and one small example you can follow by hand. Spoken script in the notes of every slide.'),
            ('One switch.', 'A black divider slide, "Part 2: the lab", marks the move to the notebook. After it the deck has four short slides: the lab map, the numbers to check, the error cards and how the class counts.'),
            ('A lab that explains itself.', 'One notebook per class and cohort. Each step is PREDICT, RUN, READ, CHANGE, in plain words, with the data and units of the cohort. The numbers it prints are checked against a NumPy reference that was compared with scikit-learn.'),
            ('Cohort overlay.', 'Same structure for all. CML3112 uses building cooling load (kW), CML3113 crusher energy demand (kWh/t), CML3111 motor winding temperature (deg C).')], 10)
h2(d, 'What each class teaches')
grid(d, [['1 First model', 'Features and target; baseline; error, MAE, RMSE; gradient descent in plain words; hidden rows (train, validation, test by equipment group); filling blanks from training rows; a line and a tree; the scoreboard'],
         ['2 Classification', 'Yes or no from a limit; why accuracy misleads (always-say-no baseline); scaling; logistic regression and the S curve; a tree that classifies; confusion matrix; precision, recall, F1; the threshold; ROC and AUC'],
         ['3 Trust', 'Underfitting, good fit and memorising (the depth curve); K-fold and group folds with an average and a spread; leakage and its three routes; reproducibility'],
         ['4 Choosing', 'Building and testing a feature (ablation); not using equipment_id; ridge and nearest neighbours as previews; a fair comparison of five candidates; the decision memo; the test set (opened once); the project rehearsal']],
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
h2(d, 'The project sitting in Week 12')
para(d, 'Decision of 4 November 2026 (it replaces the decision of 3 November): there is no demonstration, no take-home and no clinic. The project is an individual, timed, fully automatic practical, like Practical Test 1, and it covers only what was taught in Weeks 1 to 11. It counts 40 percent of the course in two parts. Part A is the coded notebook (30 marks): 24 marks of hidden tests on unseen data and 6 marks of automatic process checks (the test set opened once, preprocessing fitted on the training set only, the same result with the seed, readable charts). Part B is the decision memo (15 marks), written as a form inside the notebook and also marked automatically: the model you recommend, your validation and test numbers, three limits chosen from a list, one next step, and two short written answers checked by keyword and length rules. Nobody marks by hand; you read a short spot-check list of flagged cases. The sitting is 3 hours in the Week 12 class slot, in Google Colab, with the same timed entry and Submit test flow as Test 1: CML3112 Tuesday 1 December 11:00 to 14:00, CML3113 Friday 4 December 08:00 to 11:00, CML3111 Friday 4 December 11:00 to 14:00 (all proposed, lecturer to confirm). Each student gets one of three data variants. An unmarked rehearsal (a practice notebook and a practice data file, same structure, no solved walk-through) is released right after Class 4: CML3112 Tuesday 24 November, CML3113 and CML3111 Friday 27 November. Everything for it is in second_half/Project/: three student briefs, the rehearsal and the marked notebooks, the grader specification with its proofs, the deployment bundle for the portal and collector, the gradebook export, and a marking guide.', 10, after=4)
h2(d, 'What is built and where')
grid(d, [['Class decks (12)', 'second_half/Slides/<cohort>/', 'KLAi branded, concepts then lab, spoken script in notes, drawn diagrams'], ['Lab notebooks (12)', 'second_half/Lab Notebooks/<cohort>/', 'PREDICT, RUN, READ, CHANGE; run end to end against a NumPy stand-in'],
         ['Student slides as PDF (12)', 'second_half/Student Slides PDF/', 'Slides only, no speaker notes, for revision'], ['Student packs (12)', 'second_half/Student Packages/', 'Notebook, CSV and a one-page START_HERE per class and cohort'], ['Lecturer guides (4)', 'second_half/Lecturer Guides/', 'Clock for Tuesday and Friday, slide map, probes, lab numbers per cohort, rescue plans'],
         ['Project sitting (40 percent of the course)', 'second_half/Project/', 'Briefs, rehearsal and sitting notebooks, grader specification with proofs, portal and collector bundle, gradebook export, marking guide, README'], ['Rebuild kit', 'second_half/Build/', 'AUTHORING_GUIDE.md, content/, kit/, ref/']], [3.4, 6.0, 8.0], header=['What', 'Where', 'Notes'], size=9, label_cols=(0,))
h2(d, 'What you still have to do by hand')
bullets(d, ['Open each notebook once in real Colab and run all cells. I could only run them against a NumPy stand-in for scikit-learn, so the one risk is a small difference in a tree split or in the logistic weights. The guides list the numbers to look at.',
            'Tell the Friday cohorts that Class 1 is a recap and a long lab, and that Week numbers describe content.',
            'Send each class pack ZIP to the cohort after the class (or before, if you prefer).',
            'Run the Apps Script steps in Block_Assessment_By_Hand_Checklist_2026-11-02.md, in order, to change the live forms and deadlines.',
            'For the project, follow Project/deploy/DEPLOYMENT_STEPS.md and the Lecturer_Marking_Guide.pdf: confirm the sitting times, run the rehearsal and a sitting notebook once in real Colab with real scikit-learn, deploy the portal and collector bundle, set the three form windows, and after each sitting run the Docker grading and read the spot-check list.',
            'Old decks for Weeks 8 to 15 and their ZIPs are untouched. Use the new decks from now on.'], 10)
h2(d, 'Risks I want you to know')
bullets(d, ['Four classes is tight for the whole of regression, classification, trust and choosing. If a class runs over, the guide says what to cut. The lab is never cut.',
            'Validation sets have 15 rows and three positives in Class 2, so every score is shaky. The decks say so, because it is the honest message.',
            'The Week 8 assignment notebook the students already have asks for the same two functions as before. Nothing changes there.'], 10)
save(d, BUILD.parent / 'Plan_Weeks_8-12.docx')
subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', str(BUILD.parent), str(BUILD.parent / 'Plan_Weeks_8-12.docx')], capture_output=True)
