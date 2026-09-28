"""Measurable goals and weekly delivery map for the existing camp lessons."""
from schools_camp_content import ROOT,ML,DA
COMMON=[
'Open, run, save and reopen a notebook; distinguish a text cell from a code cell.',
'Create and identify integer, float, string and Boolean values; predict how an assignment changes a variable.',
'Calculate with taught operators, convert a numerical input and explain a simple error.',
'Trace an if/else decision and change its condition without breaking indentation.',
'Read list positions and dictionary keys; trace a loop and explain each output.',
'Write a function with a return value and check three known inputs using assert.',
'Build a small DataFrame, identify rows/columns and round-trip it through CSV.',
'Filter records, group totals and distinguish a total from an average; calculate a derived column.',
'Calculate mean, median and range and explain the effect of an extreme observation.',
'Identify missing data and a known accidental duplicate while preserving raw data and a cleaning log.',
'Create a labelled bar chart from a table and state a supported finding and a limitation.'
]
OBJECTIVES={'ML':COMMON+[
'Combine taught table, calculation and chart skills; state one feasible prediction question.',
'Name features and target, separate training/validation/test roles and calculate a simple baseline error.',
'Fit the demonstrated regression and explain its numerical prediction and limitation.',
'Compare a regression model with a training-only baseline using the same held-out records and error measure.',
'Train a small classification tree and connect category codes with their actual names.',
'Read a confusion matrix and distinguish validation choices from a final test.',
'Produce an auditable train/validation/test comparison and explain the frozen final choice.',
'Write a narrow project plan with source, target, available inputs, baseline and evaluation method.',
'Implement the project baseline and demonstrate that test answers were not used during training.',
'Compare the candidate with its baseline, inspect errors and critique a separate coding-assistant hint.',
'Rerun the complete notebook from a fresh kernel and hand over final-test evidence and a report.',
'Explain the project to a nontechnical listener in five minutes using five clear slides.',
'Demonstrate, explain and modify a small part of the project without AI assistance.'
], 'DA':COMMON+[
'Produce a reproducible sales analysis with reconciled totals, a labelled chart and cautious findings.',
'Run SELECT/FROM on the supplied database and save a query with chosen columns.',
'Use WHERE, AND, ORDER BY and LIMIT and explain which rows remain.',
'Group SQL results and reconcile SUM and COUNT with corresponding pandas totals.',
'Join on a key, check row counts and explain how duplicate keys could inflate revenue.',
'Check NULLs and row counts and save repeatable validation queries.',
'Compare labelled SQL and pandas results, reconcile grand totals and explain a join risk.',
'Define three descriptive questions answerable from the approved dataset and name their measures.',
'Build a reproducible Python analysis with SQL evidence and a justified cleaning log.',
'Produce a readable chart report and critique a separate coding-assistant hint with tests.',
'Hand over a cleanly rerunnable notebook, SQL, source data reference, dictionary and findings report.',
'Explain a chart, its calculation and a limitation to a nontechnical listener in five minutes.',
'Demonstrate, explain and modify a small calculation or query without AI assistance.'
]}
PRACTICE=[
('1','Change two quantities in the arithmetic example, predict the result on paper, then run and explain it. Save the notebook and a short note about one error you repaired.','F01 after ML03'),
('2','Change the function inputs, test zero and one ordinary value, then trace a loop over three items. Explain one list index and one dictionary key.','F02 after ML06'),
('3','Create a small table with the taught columns, filter one condition and reconcile its grouped total. Compare mean and median before and after an extreme value. DA also calculates a percentage with its denominator.','F03 after ML09'),
('4','Finish the taught cleaning log and labelled chart. Rerun checkpoint one; write two traceable findings and one limitation. Keep a copy of the submission.','F04 after ML12'),
('5','ML: explain the baseline and check one prediction error by hand. DA: write and save a filter and grouped SQL query, then compare labelled totals with pandas.','No extra lab'),
('6','Finish checkpoint two. Explain one model/split mistake (ML) or join/count discrepancy (DA). Repair the method rather than replacing a number by hand.','No extra lab'),
('7','Build the approved project incrementally. Save the independent attempt before any supervised AI critique. Keep the separate assistance log; reconcile every reported number.','Supervised AI literacy in Session 21'),
('8','Rerun and hand in the project at Session 22; prepare five slides and a backup. Rehearse an unaided explanation and a small code change before Session 24.','Optional modern-AI orientation in Session 23')]

def build_delivery_plan():
 lines=['# Eight week teaching and practice plan\n','Each track has 24 core classes. ML adds four foundation labs on separate days in weeks 1–4. Keep the three core classes in numbered order and insert each ML lab after that week’s third core class. This is a relative plan; exact dates and holiday breaks are not confirmed.\n','Core classes propose 180 minutes including a 15-minute break; ML labs propose 120 minutes including a 10-minute break. Confirm session lengths before booking. Do not increase contact-hour claims by counting homework.\n','## Weekly rhythm and practice\n','Two 45–60 minute practice blocks on non-class days are the starting allowance. The short repeat-and-change exercise in each lesson is part of these blocks, not additional homework. If stuck for 30 minutes, record the attempted step and question. Weeks 1–6 portfolios use the existing 20% total weight; checkpoints and projects retain their separate weights.\n']
 for week,task,extra in PRACTICE:
  start=(int(week)-1)*3+1
  lines += [f'### Week {week}: core sessions {start:02}–{start+2:02}\n',task+'\n',extra+'.\n']
 lines+=['## Class objectives and evidence\n','Open the matching student sheet and instructor guide for the definition, worked example, expected output, independent task, repair cue and full pacing. The independent task is the exit evidence for each objective below. For SQL sessions, run SQL in DB Browser, not a Python code cell.\n']
 for code,lessons in [('ML',ML),('DA',DA)]:
  assert len(OBJECTIVES[code])==len(lessons)==24
  lines += [f'## {code} core classes\n']
  for i,(lesson,goal) in enumerate(zip(lessons,OBJECTIVES[code]),1):
   lines += [f'### {code}{i:02} — {lesson["title"]}\n',f'By the end: {goal}\n',f'In-class exercise and evidence: {lesson["task"]}\n']
 lines+=['## Supporting material and delivery gates\n','Use the supplied synthetic CSV/SQLite files and DATA_DICTIONARY.md; ML additionally uses the bundled iris teaching dataset. See FOUNDATION_LABS.md for F01–F04, ASSESSMENT_AND_SHOWCASE.md for weights and PROJECT_RUBRIC.md for marking anchors. AI_USE_POLICY.md applies from the first class.\n','Before teaching, pilot a Python foundations session and a pandas session with a beginner, preflight the actual laptops, test the private hand-in route and calibrate grading on sample submissions. Existing executable reference checks cover numerical work, but a deployed school submission/autograding service and finished PowerPoint course are still outstanding. Do not claim automatic end-to-end marking is operational.\n']
 (ROOT/'teaching/CLASS_BY_CLASS_PLAN.md').write_text('\n'.join(lines))
