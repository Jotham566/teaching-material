"""Slide-specific teacher support and reviewed wording, shared with deck builders.

Notes are private teaching support. Do not include these files in student ZIPs.
The public task sheets remain authoritative for assessed deliverables.
"""
import re

# Short explanations, a diagnostic question with its answer, and a recovery move.
# Ordered from specific to general; match the actual slide, not the whole week.
SUPPORT = [
(r'module and version|repair exercises|break and fix', 'A module supplies Python tools; import asks Python to load it. A version identifies a software release. A path identifies a file. A state error happens when stored values differ from what we expected.', 'Notebook 04 starts at 12, adds 5 to get 17, then resets to 12. Why does it print 12? The final assignment overwrites 17.', '01: the named module is deliberately unavailable; remove the unused import instead of trying to install a made-up package. 02: the exercise asserts Python 2 but the course uses Python 3; inspect sys.version_info and correct that deliberate mismatch. 03: upload the issued CSV and replace the nonexistent folder path with its real filename. 04: remove the unwanted reset, restart and run all for 17; repeat only the increment to see 22, then 27.'),

(r'percent.error|signed percent', 'Signed percentage error compares a measurement with its expected reference: (measured - expected) / expected times 100. Positive means above the reference; negative means below it.', 'For measured 90 and expected 100, the signed error is -10%. Its size is 10%.', 'Calculate the difference first, divide by the reference, then multiply by 100. The formula needs a nonzero reference; follow the issued task contract for exceptional inputs.'),
(r'original values|largest error|signed error|largest size', 'The size of an error is its absolute value. Keep the original sign and the matching reading. Find the position of the largest size, then use that same position in both original lists.', 'For errors [-2,5,-8], sizes are [2,5,8]. The maximum size is 8 at position 2; the original signed error is -8.', 'Draw the readings, signed errors and sizes in aligned columns. Circle the position rather than replacing the signed error with its absolute value.'),

(r'percentage point', 'A percentage is out of one hundred. Moving from 10% to 15% is an increase of 5 percentage points, but 50% relative to the original 10%.', 'From 20% to 25%: how many percentage points? 5. Relative increase? 25%.', 'Write the subtraction and the division separately; label their different units.'),
(r'precision|recall|confusion matrix|false negative|true positive', 'Name the positive class first. Actual is what happened; predicted is the model decision. Precision asks how many predicted positives were right. Recall asks how many actual positives were found.', 'With TP=2, FP=1, FN=2: precision=2/3 and recall=2/4. A missed actual positive is a false negative.', 'Draw actual/predicted headings. Place one case at a time before calculating a fraction. Explain the task rule for a zero denominator.'),
(r'cross.validation|standard deviation|folds', 'Cross-validation repeats training and validation on different partitions. Each fold gets a newly fitted model and preprocessing. Variation across fold scores shows sensitivity to the partition.', 'May preprocessing learn from all rows before the folds? No, that would give each validation fold information from outside its training portion.', 'Draw three small partitions and label who learns and who is evaluated. Fold spread is not automatically a confidence interval.'),
(r'leakage|training.validation|training.only|group.split|data.split|sealed|validation and final', 'Training fits rules. Validation helps choose among rules. The final test estimates performance after choices are fixed. Information that would be unavailable at the real prediction time must stay out of the inputs.', 'May two readings of the same machine appear on both sides when evaluating new machines? No; split by machine. For forecasting, train on the past and evaluate later time.', 'Use three envelopes. Keep the final-test envelope closed while selecting features or settings.'),
(r'mae|rmse|error measures|regression.errors', 'An error compares prediction with measured truth. Absolute error ignores direction. MAE averages absolute errors; RMSE squares, averages, then takes a square root. Both use the target unit.', 'Actual [4,8], predicted [5,6]: prediction-minus-actual errors [1,-2], MAE=1.5, RMSE=sqrt(2.5), about 1.58.', 'Calculate one pair by hand first. For signed percentage error follow the precise sign convention in the issued task.'),
(r'r²|r-squared', 'R-squared compares squared prediction errors with using the evaluation targets’ mean. One is perfect; zero matches that reference. A negative value is possible.', 'Does R-squared=0.8 mean 80% of predictions are correct? No; it concerns variation and squared errors, not a count of correct answers.', 'Compare errors against a mean predictor on the same evaluation rows. MAE remains useful for a result in physical units.'),
(r'ablation|interaction|combined input|feature reviewer|make_features', 'A feature is information supplied to a model. An interaction combines inputs, for example area times thickness gives volume. Ablation compares a model with and without a feature using the same evaluation protocol.', 'Does a lower validation error prove the feature is physically causal? No. It supports prediction under this comparison, subject to leakage and data limitations.', 'State when each input becomes available, write its unit, then compare the same rows and metric.'),
(r'model select|model choice|eligibility|tie.break|ranking|practical constraints|recommendation needs', 'First remove models that fail the stated error or speed limits. Then apply the stated ranking and tie-break rules to eligible models. The smallest error alone need not decide.', 'If a model has the lowest error but exceeds the maximum latency, is it eligible? No.', 'Write an eligibility column and a separate ranking column. Check the exact boundary rule before sorting.'),
(r'baseline|mean prediction', 'A baseline is a deliberately simple reference. For numeric prediction, one example always predicts the training target mean. A more complicated model must earn its complexity by improving a fair comparison.', 'Why compute the constant from training targets? Evaluation answers must not influence a deployed prediction rule.', 'Use training targets 2,4,6: the mean baseline predicts 4 for every new row, whatever its inputs.'),
(r'fit and predict|creating, fitting|fitted state|model object|linear model|fitted line|regression tree', 'Creating a model chooses the kind of rule. fit learns from training inputs and known answers. predict applies the fitted rule to new inputs without receiving their answers.', 'Does creating a model object train it? No. It must be fitted before prediction.', 'Point to inputs, training answers, fit, then new inputs. Keep each input row paired with its own target.'),
(r'one.hot|indicator|categor(y|ies).*column|encoding', 'A category is a label, not an amount. Indicator columns record whether a row belongs to each category, usually with 0 or 1. Fit the encoding on training data and reuse it.', 'Does assigning red=1 and blue=2 mean blue is twice red? No, those are labels.', 'Make two rows and two category columns by hand before showing the encoder.'),
(r'threshold|warning decision|probability', 'A probability-like score and a class decision are different outputs. A threshold turns a score into an action. Lowering a warning threshold usually raises both detections and false alarms.', 'At a rule of score >= 0.5, what happens at 0.5? It is positive. With > 0.5 it would not be.', 'Mark three scores below, at and above the boundary. Do not promise the score is well calibrated without checking.'),
(r'average an average|weighted|group mean|total and a count', 'A combined mean is the combined total divided by the combined count. Averaging group means equally gives each group equal influence regardless of size.', 'Group A: one value 10; group B: three values 2. Overall mean is 16/4=4, not (10+2)/2=6.', 'Recover each group total as mean times count, add totals, then divide by all observations.'),
(r'mean, median|typical|distribution|percentile|skew', 'Mean is total divided by count. Median is the middle of sorted values. A percentile locates a position in that ordered distribution; interpolation conventions can differ. Match the summary to the question.', 'For [2,3,4,5,100], median=4 and mean=22.8. The large value pulls the mean up.', 'Sort five values by hand. A skewed distribution does not make the mean wrong if the question concerns totals or expected cost.'),
(r'count.*rate|rate.*count|return rate|a rate', 'A count says how much work there is. A rate divides events by the relevant opportunities or population. Both numerator and denominator must describe the same period and group.', '10 returns from 100 orders versus 20 from 1,000: rates are 10% and 2%. The second group has more returns but a lower rate.', 'Write numerator and denominator in words before putting numbers into the fraction.'),
(r'seasonality|year on year|calendar|trend', 'A seasonal pattern repeats at calendar intervals. Compare like periods before calling a change growth; compare counts, coverage and definitions as well.', 'Does a rise from November to December prove underlying growth? No; compare comparable Decembers and inspect the wider series.', 'Draw a two-year timeline and match the same months. Separate description from an explanation of cause.'),
(r'join|merge|fan.out|relationships|star schema|primary key|foreign key|grain', 'Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.', 'One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.', 'Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.'),
(r'groupby|group by|having|aggregation', 'Grouping puts rows sharing a key into buckets, then computes a result for each bucket. WHERE filters rows before SQL grouping; HAVING filters grouped results.', 'Which condition keeps only groups with more than five rows? HAVING COUNT(*) > 5.', 'Draw two buckets and count by hand. Name the intended output grain before writing the aggregation.'),
(r'null|missing|nan|blank|imput', 'Missing means not recorded, not automatically zero. Decide why it is missing and document the rule. Fitted fill values must come from training data when evaluating a model.', 'Is an unrecorded energy reading evidence of zero consumption? No.', 'Use three rows: a recorded zero, a recorded positive value and a blank. Explain their different meanings before cleaning.'),
(r'duplicate|cleaning|reconciliation|residual', 'A cleaning decision needs evidence, a stated rule and a before/after check. Similar rows may be genuine repeated events. Reconciliation compares totals built under the same definitions.', 'May we delete every repeated amount? No. Check the row identifier and the table grain first.', 'Keep raw data, record counts before and after each action, then explain any remaining difference instead of forcing totals to agree.'),
(r'calculated column|a measure|filter context|dax|sumx|distinctcount', 'A calculated column stores a result for each row at refresh. A measure is evaluated under the filters of the current visual. SUMX evaluates an expression for each row before adding it.', 'Should revenue respond to a selected region? Yes; test the measure with that filter and reconcile it to known data.', 'Work one order line by hand, then two lines. Name the numerator and denominator populations before an average-order-value measure.'),
(r'dataframe|series|dtype|pandas|profiling', 'A DataFrame is a labelled table. A Series is a single labelled sequence, often one column. A dtype describes stored values, but the import may infer something unsuitable.', 'Does a price that looks numeric prove the column is numeric? No. Inspect its dtype and troublesome values before conversion.', 'Use head, shape and dtypes to locate the table, count rows/columns and inspect storage. Check units and missing values before calculating.'),
(r'csv|dictreader|file path|file.*not found|path names', 'A CSV is a text table. The header supplies column names. With csv.DictReader, values start as text, even if they look like numbers. A path tells Python where the file is.', 'Can "2.5" from csv.DictReader be added as a number without conversion? No; convert valid numeric text first.', 'Show the file in the runtime folder and compare its exact filename, case and column headers. Upload data again after a fresh Colab runtime.'),
(r'dictionary|key and lookup|key.*value', 'A dictionary pairs a key with a value. For {"unit":"A", "reading":4}, record["reading"] looks up the key and gives 4. The key is not a list position.', 'What happens if the key is spelled "Reading" instead? It is a different key; direct lookup can raise KeyError.', 'Point to each key and its value. Read the colon as associates-with, then do one exact lookup.'),
(r'list|index|slice|tuple|collection', 'A list keeps items in order. Python positions start at zero. In [2,4,6], position 0 contains 2 and position 2 contains 6. A slice excludes its stop position.', 'What is [2,4,6][1]? 4. Is there a position 3? No.', 'Draw three numbered boxes starting at zero. Keep the position separate from the value stored in it.'),
(r'loop|iteration|accumulator', 'A loop repeats its indented instructions for each item. A running total must be initialised before the loop and updated inside it.', 'For values 2,4,6 and total initially 0, what are the successive totals? 2,6,12.', 'Use a trace table with current item and total. Resetting total inside the loop loses earlier additions.'),
(r'function|return|parameter|argument', 'A function is a named set of instructions. def defines it; a call runs it with inputs. Parameters are input names, arguments are supplied values, and return sends the result back.', 'Does print(8) return the number 8 to the caller? No; it displays 8 and returns None. A function needing a numeric result should return it.', 'Trace one call: bind input names, run the indented body, reach return, then put the returned result back into the calling expression.'),
(r'condition|comparison|branch|if/else|boundary', 'A condition is a True/False question. Python executes the matching indented branch. = assigns; == compares. >= includes the boundary, while > excludes it.', 'With value 30, is value >= 30 true? Yes. Is value > 30 true? No.', 'Try one value below, at and above the boundary before running the code.'),
(r'variable|numbers and values|values have types|assignment syntax', 'A value is a piece of information. A variable is a name referring to a value. In length_m = 5, Python evaluates the right side and binds that result to the name on the left.', 'After x=3 then x=5, what does print(x) display? 5. The earlier value is not added automatically.', 'Write the name on a card and the current value beside it. Distinguish number 3 from quoted text "3".'),
(r'arithmetic|operator|symbols|conversion|quantities|unit|slab|weight|efficiency', 'Read each quantity and unit before using a formula. Python calculates numbers but does not enforce physical units. Parentheses specify which operation happens first.', 'What is 5 m times 3 m? 15 square metres. What is 7/2 in Python? 3.5; 7//2 is 3.', 'Write the formula and units on paper, substitute small values, then translate it to Python. Check zero denominators and the issued sign convention.'),
(r'notebook|kernel|cell|colab|execution|restart', 'A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.', 'Does editing a cell update a value already stored in memory? No; the cell must run.', 'Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.'),
(r'git|repository|commit|readme|reproducib|handover|version control', 'A repository is the project folder and recorded history. A commit records a chosen change; uploading or pushing shares it. A README tells someone else how to run the work.', 'Does saving to GitHub hand in the assignment? No; submission requires the correct form and its confirmation.', 'Ask a partner to follow only the README. It should identify the data, files, run order and expected result. Keep secrets out of the repository.'),
(r'chart|histogram|axis|visual|dashboard', 'Begin with the question and intended comparison. Identify what an axis, bar, point or colour represents, including its unit. A chart summarises data and may hide variation.', 'For a bar chart comparing amounts, why normally start the value axis at zero? Bar length encodes magnitude; truncation can exaggerate differences.', 'Read one mark aloud as a sentence. Check the population, period, filters and units before stating the finding.'),
(r'feature|target|machine learning|regression|classification|artificial intelligence', 'A feature is an input available when predicting. The target is the answer to learn from. Regression predicts a number; classification predicts a category. Learning patterns does not by itself establish cause.', 'Predicting concrete strength: regression. Predicting pass/fail: classification. Is a later test result available before that test? No.', 'Describe the engineering decision in everyday language, then label one row, an input and its answer. Compare with a rule you could write directly.'),
(r'finding|observation|recommendation|question|evidence|limitation', 'An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.', 'Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.', 'Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.'),
]

REPLACEMENTS = {

 'GITHUB IN THE BROWSER: UPLOAD AND COMMIT':'GITHUB: UPLOAD AND COMMIT',

 'What a good README is not':'Keep the README practical',
 '01: identify the deliberately unavailable module.':'Identify the deliberately unavailable module.',
 '02: compare the required and actual Python versions.':'Compare the required and actual Python versions.',
 '03: locate the CSV and correct its file path.':'Locate the CSV and correct its file path.',
 '04: trace the values and remove the unwanted reset.':'Trace the values and remove the unwanted reset.',

 '04: restart and run in order to expose missing setup.':'Trace the values and remove the unwanted reset.',

 '# The menu route, which is what we use today:':'# Browser route used today:',
 '#   File  ->  Save a copy in GitHub':'#   Colab: download your completed .ipynb',
 '#   create the repository on github.com first':'#   GitHub: create a private repo with README',
 '#   name it exactly as given on the next slide':'#   Add file -> Upload files: notebook and CSV',
 '#   write a commit message, then OK':'#   Commit changes, then edit your README',

 '# The menu route, which is what we use today:\n#   File  ->  Save a copy in GitHub\n#   create the repository on github.com first\n#   name it exactly as given on the next slide\n#   write a commit message, then OK':'# Browser route used today:\n#   Colab: download your completed .ipynb\n#   GitHub: create a private repo with README\n#   Add file -> Upload files: notebook and CSV\n#   Commit changes, then edit your README',

 'Open for 24 hours if the network fails, then it closes itself.':'Open for 24 hours from lecturer activation, then it closes.',
 'Scan the code. First box is your registration number, off your card.':'Enter your own Student Registration Number exactly as recorded.',
 'Include the supplied CSV and a README with your program, file list, run instructions and one engineering problem.':'Keep the CSV in your repository. Upload only your notebook and README.md.',
 'Repository name: cml3112-yourstudentnumber Paste the repository URL into the A2 form.':'Use a private repository, e.g. cml3112-practice. Paste its URL into the A2 form.',
 'One engineering problem from your own discipline that you think data could help with. Real and yours.':'The exact notebook and CSV filenames in your repository.',
 'One sentence on what data that would need: who measures it, how often, and whether anyone keeps it.':'How to open the notebook, upload the CSV and run cells from the top.',
 "One sentence on what you had to fix today, or 'nothing' if it worked first time.":'How to restart, Run all, save and download the finished notebook.',
 'Long. Six sentences is plenty for A2. By Week 13 yours will also say how to run the project and what the results were, and it will still fit on one screen.':'Keep it short, but include the file list and run instructions. A new reader should be able to repeat your steps.',
 'Why the honesty sentence carries marks':'Why the run instructions matter',
 'What went wrong for you tells me where this session needs fixing, and being able to say plainly what broke and how you fixed it is a professional skill this course keeps asking for.':'A new reader should be able to open your files and reproduce the result. Test your README instructions before submitting.',
 'Run git status BEFORE and AFTER git add. The same filenames move from red to green, which is the staging area doing its one job: holding the changes you have chosen for the next commit.':'Use GitHub in the browser today: upload your files and commit the changes. The commands above are optional local-terminal reference, not Python cells.',
 'COLAB: FILE → SAVE A COPY IN GITHUB':'GITHUB: UPLOAD AND COMMIT',

 'Marked on whether a decision maker could act on it. Not on the code, not on the number of visuals.':'Marks reward a supported decision and the required evidence.',

 'For each one: what data it would need, and where that data might actually come from — who measures it, how often, and whether anyone has kept it.':'For each: state inputs, target, data source and one limitation.',
 'One of the three must be a problem you think is NOT solvable with the data that exists. Say why.':'Choose one problem and dataset. Explain why it is feasible.',
 'Marked pass or redo. What is being checked is engagement.':'Marks: framing 6, data 8, judgement 6. Submit one DOCX or text PDF.',
 'What kind of value a column holds: whole number, decimal, text, date, or true/false. A column has ONE type, all the way down.':'A column’s intended type: integer, decimal, text, date or Boolean. Check imported values.',
 'The rule: sum the top, sum the bottom, then divide. Never average an average unless the groups are the same size.':'Combined mean: total sum divided by total count.',

 'Excel stops at 1,048,576 rows. This file has more than that, which means tonight is the first time the new tool does something the old one cannot.':'A worksheet has a row limit. This workbook spans sheets; inspect all sheets before combining them. pandas makes the preparation repeatable.',
 'A column has ONE type, all the way down.':'Choose a suitable column type; imported values may need checking.',
 'Assignment A1 — one page, due at the start of Week 2':'Assignment A1 — use the current form deadline',

 'Save both required files':'Save the complete notebook',
 'Save the notebook and the separate typed Part B document.':'Type Part B under My written evidence in the notebook.',
 'Locate both files in the designated local folder.':'Locate the complete notebook in the designated local folder.',
 'Reopen them to check that your latest work was saved.':'Reopen it to check that code and written answers were saved.',
 'Save a separate typed practice explanation.':'Type a practice explanation in the notebook text cell.',
 'Close both files and locate them again without help.':'Close the notebook and locate it again without help.',
 'Save the typed Part B evidence as a separate file.':'Type Part B under My written evidence in the notebook.',
 'Locate and reopen both files without internet.':'Locate and reopen the complete notebook without internet.',
 'Save the notebook and a separate explanation of which data may fit preprocessing.':'Save the notebook with a text cell explaining which data may fit preprocessing.',
 'Locate both saved files in the required folder.':'Locate the complete notebook in the required folder.',
 'You can locate both your notebook and typed reasoning document without help.':'You can reopen your notebook and find code and typed reasoning without help.',
 'Include concise captions and an accessible report.':'Include captions and readable written evidence in the notebook.',
 'Save the notebook and the typed Part B evidence as instructed by the invigilator.':'Save one notebook with Part B under My written evidence.',
 'Tonight\'s file will not open in Excel':'A large workbook to inspect with pandas',
 'Why you must never average an average':'When averaging averages gives a wrong result',
 'is a function, two arguments, a condition and a result.':'is a function with three arguments: a condition and two possible results.',
 'The dashboard, or the notebook, whichever carries the work.':'Upload PPTX with narration notes and numerical evidence.',
 'One page: question, answer, how you know, the trade, and what would change it.':'Add a DOCX/PDF appendix if needed. Keep PBIX as supporting material.',
}

def correct(text, deck_path=''):
 if 'CML3112_Week02' in deck_path:text=text.replace('NOW BREAK IT ON PURPOSE','TRY IT, THEN EXPLAIN')
 if re.search(r'Week(08|15)',deck_path):
  text=text.replace('Include concise captions and an accessible report.','Include captions and a separate readable DOCX/PDF report.').replace('Include captions and readable written evidence in the notebook.','Include captions and a separate readable DOCX/PDF report.')
 for a,b in REPLACEMENTS.items():text=text.replace(a,b)
 return text

def title(text):
 lines=text.splitlines()
 return lines[1] if len(lines)>1 and (lines[0].isupper() or 'WEEK' in lines[0]) else lines[0]

def clean_notes(notes, deck_path=''):
 notes=notes.split('\n\nTeaching context:')[0].split('\nTeaching rhythm:')[0]
 notes=notes.split('\n\nSequence:')[0]
 return correct(notes.strip(),deck_path)

def make_notes(slide,previous=None,following=None,source=None,deck_path=''):
 text=correct(slide['text'],deck_path); heading=(source or {}).get('title') or title(text)
 old=clean_notes(slide.get('notes',''),deck_path)
 if len(old.split())>220:
  first=old.split('\n\n')[0]
  old=(first if len(first.split())<=160 else '')+'\nFull assessment requirements belong in the current public task guide; explain only the criterion or task shown on this slide.'
 if re.search(r'Week(07|14)',deck_path) or (re.match(r'q\d+:',heading) and '## q' in old):
  old='Read the specific public requirement shown on this slide. Explain the input, output and evidence before independent work; do not work the assessed answer for the class.'
 if 'CML3112_Week02' in deck_path:
  overrides={
   30:'Use the browser route in STUDENT_HOW_TO.md: download the completed notebook from Colab; create a private GitHub repository with a README; choose Add file, Upload files; add the notebook and supplied CSV; commit the changes. Edit and commit your own README. The displayed Git commands are optional reference for a local terminal, not instructions to type into a Python cell.',
   31:'A2 is marked out of 20: identity 2, proof_sum 4, fresh-run readings 4, correct CSV records 4, execution-order explanation 3, README 3. Keep My explanation: in the notebook text cell. Submit exactly the completed renamed notebook and your own README.md together, plus the repository URL in its form field. The CSV stays in the runtime and repository. Use the current cohort form deadline; do not promise an automatic redo or extra attempt. A1, Quiz 1, A2 and Quiz 2 are separate tasks.',
   32:'The README is required now. Include the programme, exact file list, instructions to open the notebook, upload the CSV, restart and run from the top, then save/download. Demonstrate editing README.md on GitHub and downloading the raw file. Ask a partner to follow the instructions literally. Do not submit the instruction README supplied in the ZIP.',
   33:'Guide repairs 01–04 in class, one at a time. 01: identify the deliberately unavailable module and remove the unused import; do not install the made-up package. 02: compare the required and actual Python versions. 03: locate the CSV and correct its path. 04: trace 12, then 17, then the unwanted reset to 12. Remove the reset; restart and Run all for 17. Ask learners to state the cause before showing a repair. These notebooks and hello_engineering.py are practice only; return to proof_of_life.ipynb for the assessed work.'}
  old=overrides.get(slide['number'],old)
 parts=[f'TEACHING PURPOSE\n{heading}']
 if previous:parts.append('CONNECT\nBuild on the preceding slide: '+title(correct(previous['text']))+'.')
 # Preserve specific existing teaching instructions; discard repeated whole-week boilerplate.
 generic=('Give the everyday meaning first.','Explain this before the next worked example.','Explain each word with the nearby worked example.','Demonstrate the terms on screen,')
 if old and not old.startswith(generic):parts.append('LECTURER CUE\n'+old)
 focus=heading+' '+text
 matches=[row for row in SUPPORT if re.search(row[0],focus,re.I)]
 # Prefer the heading when several concepts appear in a dense task slide.
 preferred=[row for row in matches if re.search(row[0],heading,re.I)]
 selected=(preferred or matches)[:1]
 if 'github' in heading.lower():selected=[row for row in SUPPORT if row[1].startswith('A repository is')]
 for _,explain,check,recover in selected:
  parts.append('EXPLAIN IN ORDINARY WORDS\n'+explain)
  parts.append('CHECK AND EXPECTED ANSWER\n'+check)
  parts.append('IF LEARNERS ARE STUCK\n'+recover)
 if source and source.get('concepts'):
  parts.append('POINT TO THE DEFINITION\n'+'\n'.join(c['term']+': '+c['meaning'] for c in source['concepts']))
 if source and source.get('code'):
  parts.append('WALK THROUGH THIS CODE\n'+ '\n'.join(source.get('explain',[]))+'\nRead the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.')
 if ('PREDICT BEFORE RUNNING' in text or 'CHECK YOUR UNDERSTANDING' in text or 'YOUR TURN' in text) and following:
  nxt=correct(following['text'])
  if any(x in nxt for x in ('DISCUSS THE REASONING','ANSWERS','CHECK THE OUTPUT')):
   parts.append('DISCUSSION KEY FOR THIS SLIDE\n'+nxt+'\nLet learners attempt first; use this to explain the reasoning, not just reveal the answer.')
 if 'READ THE EXAMPLE' in text or 'LOOK AT THIS' in text:
  parts.append('READ THE VISUAL\nStart with the title and labels. Read one row or mark aloud, including its unit. Let a learner read a second one before discussing the pattern. Do not infer a numerical value from an unlabelled drawing.')
 if 'WATCH' in text or 'VIDEO' in text:
  parts.append('VIDEO ROUTINE\nPreview the exact link and stated excerpt before class. State the viewing question first, pause after the example, and ask a learner to explain it. If access fails, use the adjacent worked example and discussion rather than spend class time troubleshooting streaming.')
 if 'QUIZ' in text and ('ACCESS' in text or 'END-OF-SESSION' in text or 'catch-up' in text):
  parts.append('QUIZ OPERATION\nOpening the student link does not activate the quiz. In Quiz Controls run the matching open_W<week>_<cohort> function once when ready. Announce the logged closing time: 24 hours after activation. Five minutes describes expected answering time, not the availability window. Quiz 1 and Quiz 2 require separate activation when collecting catch-up work.')
 if 'ASSIGNMENT' in text or 'WHAT TO DO' in text or 'CHECKPOINT' in text or 'CAPSTONE' in text:
  parts.append('ASSIGNMENT HANDOVER\nOpen the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.')
 if re.search(r'Week(07|14)',deck_path):
  parts.append('TEST COLLECTION RULE\nThis deck is for rehearsal before the timed assessment. Preserve the invigilated timetable and Part A snapshot. During Part B, type answers in the notebook cell headed ## My written evidence without executing code. Collect one complete .ipynb offline; later Google upload only transports the collected work. Do not require internet or AI during the test.')
 if re.search(r'Week(08|15)',deck_path) and 'project' in text.lower():
  parts.append('PROJECT UPLOAD SET\nFor the DA_PROJECT or ML_PROJECT, submit the completed project .ipynb together with one readable DOCX or selectable-text PDF report. This differs from the single-notebook test packet. The current public project guide defines the evidence and rubric; do not substitute weekly practice for the project.')
 if 'DA_S15' in deck_path and any(w in text for w in ['CAPSTONE','LAB','PRACTICAL NOTE']):
  parts.append('CAPSTONE FILES\nThe S15 guide requires PPTX with narration in speaker notes, plus DOCX or selectable-text PDF if evidence is separate. Include all five S15CHECK lines from NUMERICAL_EVIDENCE.md as text. Keep PBIX or an authorised report link as supporting material; the upload form does not accept PBIX or ZIP. Release remains subject to grading checks.')
 if 'DA_S07' in deck_path and ('Retail' in text or 'file' in heading.lower()):
  parts.append('WORKBOOK CLARIFICATION\nDo not say an Excel workbook cannot open solely because the combined row count exceeds one worksheet limit. Check its sheet names. pandas.read_excel uses the first sheet by default; sheet_name=None returns a dictionary of all sheets. Select or combine compatible sheets deliberately and check the resulting date range. Source: https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html')
 if 'dtype' in text.lower():
  parts.append('TYPE NUANCE\nAn object dtype alone does not prove that a column contains bad numeric values; it can hold Python objects, including numbers. Inspect values and conversion results. Missing values may display as NaN, None, NaT or pandas NA depending on dtype.')
 if re.search(r'Week01',deck_path) and 'ASSIGNMENT' in text:
  parts.append('A1 CATCH-UP\nThe original Week 1 schedule has been superseded for catch-up collection. Use the current cohort A1 form deadline, aligned with its Week 2 assignment upload. Quiz 1 is separate and gets 24 hours from its own activation.')
 if not selected and not old:
  parts.append('DELIVER THIS SLIDE\nRead the stated purpose, then point to the named example or action on the slide. Ask learners to describe what they will do before moving on. For a break slide, announce the return time; for a section divider, name the next concrete task.')
 if following:parts.append('NEXT\n'+title(correct(following['text']))+'. Move on after a learner can explain the current example or required action.')
 return '\n\n'.join(parts)
