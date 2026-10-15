"""Prepare notes tied to actual slide content; no generic weekly note fallback."""
from pathlib import Path
import ast,copy,hashlib,json,re
from slide_note_explanations import explanation
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'review/2026-09-29/slide-specific-notes'
INVENTORY=json.loads((OUT/'inventory.json').read_text())
SOURCES={d['filename']:d for d in json.loads((ROOT/'data/iuea_deck_content.json').read_text())}
LINKS=json.loads((ROOT/'data/submission_links.json').read_text())
AIMS={
1:('Start with an engineering decision, then introduce learning from examples. No code is needed today.','A numerical quantity such as days until servicing is a regression target. A label such as service due is a classification target.'),
2:('Today the learner creates, runs, saves and submits a notebook. Separate those actions so a successful run is not mistaken for a saved or submitted file.','The runtime remembers readings = 12. One update adding 5 gives 17; repeating only that update gives 22. A fresh run starts at 12 again.'),
3:('Build calculations from values and operators, then decisions and functions, then collections. Define each symbol before using it in the program.','A definition stores instructions. double_value(4) runs them with x = 4 and returns 8. Printing that return value is a separate action.'),
4:('Move from one calculation to many records. Lists supply ordered values, loops visit them, dictionaries label fields and CSV files store the observations.','For readings 2, 4 and 6, the running total is 2, then 6, then 12. Count 3 gives mean 4.0. A group needs its own total and count.'),
5:('pandas performs table operations that build on the lists, records and loops already taught. Explain the row, column and unit before using an operation.','A filter retains matching rows. groupby gathers matching labels. For A:2, A:3, B:4, the totals are A:5 and B:4.'),
6:('Inspect quality before interpreting a chart. Preserve raw records and justify each removal or estimated value.','A blank is not a measured zero. With observed values 20 and 24, median filling would insert an estimate of 22, which must be recorded as estimated.'),
7:('This is preparation for Test 1. Rehearse opening and saving offline before the assessed period. During the test, follow the issued invigilation rules.','The published schedule has 15 minutes of setup, 120 of practical work, 25 of typed reasoning without code execution and 20 of collection.'),
8:('Introduce a fitted predictor only after identifying its inputs and known answers. Compare it with a simple baseline and explain its errors in target units.','The teaching line through (1,12), (2,14), (3,16), (4,18) predicts 15 at input 2.5. One neat example does not establish real-world accuracy.'),
9:('Move from a numerical prediction to a category decision. Name the positive class before counting correct warnings, false alarms and missed warnings.','Actual 1 with predicted 0 is a false negative. If 1 means warning, this is a missed warning, not merely a wrong number.'),
10:('Connect evaluation to intended use. Decide how to hold out observations before fitting either preprocessing or the model.','When testing new equipment, all observations from equipment A stay in one partition. Training must not learn its missing-value replacements from held-out equipment.'),
11:('Explain why a calculated input may help and test the idea under an unchanged validation protocol.','If validation MAE falls from 5 to 4 after adding one feature, the reduction is 1 target unit, or 20%. A comparison on a different split cannot isolate that change.'),
12:('A recommendation must satisfy the practical limits before it wins on a ranking metric. Explain eligibility and tie-breaking separately.','A model at 4 error units and 12 ms fails a 10 ms limit even if its error is attractive. Test exact boundaries before ranking eligible candidates.'),
13:('The handover should reproduce the result using the files and instructions alone. Saved output is insufficient evidence.','Restart, load the stated data and follow the README literally. A mismatch between a documented filename and the actual file is a handover defect to fix.'),
14:('Prepare for Test 2 by rehearsing the previously taught modelling decisions and the offline evidence workflow. Do not turn the assessed period into a worked lesson.','Part B is typed reasoning in the same notebook, with code execution prohibited. The invigilated collection is authoritative; a later upload only transports that snapshot.'),
15:('Explain a supported finding, its limitation and the individual work behind it. The team project and each learner’s defence are distinct evidence.','A claim should point to a named plot or result, its target unit, the evaluated sample and the decision it supports. “Our model is good” supplies none of these.')}

def title(s):
    lines=s['text'].splitlines()
    return lines[1] if len(lines)>1 and (lines[0].isupper() or lines[0].startswith(('CML','SEGMENT'))) else lines[0]

def clean_body(s,src):
    if src:
        if src.get('concepts'):return '\n'.join(c['term']+': '+c['meaning'] for c in src['concepts'])
        if src.get('table'):return '\n'.join(' | '.join(map(str,row)) for row in src['table'])+'\n'+src.get('caption','')
        return src.get('body','') or src.get('caption','')
    lines=s['text'].splitlines()[2:]
    return '\n'.join(x for x in lines if x and not re.fullmatch(r'\d+|[A-E]',x))

def code_walk(program):
    """Explain actual syntax lines without executing untrusted notebook input."""
    result=[]
    for raw in program.splitlines():
        line=raw.strip()
        if not line or line.startswith('#'):continue
        if line.startswith('from '):meaning='Bring the named tool from this library into the current Python session.'
        elif line.startswith('import '):meaning='Load this library. An alias after as is the shorter name used below.'
        elif line.startswith('def '):meaning='Store these instructions under this function name. Names in parentheses are its inputs; the body waits until a call.'
        elif line.startswith('return '):meaning='Evaluate this result and send it to the caller, ending this function call.'
        elif line.startswith('for '):meaning='Take each item or pair in turn, assign the loop name(s), and repeat the indented body.'
        elif line.startswith('while '):meaning='Test this condition before each repetition. Stop when it becomes False.'
        elif line.startswith(('if ','elif ')):meaning='Evaluate this yes/no condition. Execute its indented body only on the matching path.'
        elif line=='else:':meaning='Use this remaining path when the matching earlier condition did not succeed.'
        elif line=='continue':meaning='Skip the rest of this iteration and proceed to the next item.'
        elif line=='break':meaning='Exit this loop immediately; later items will not be visited.'
        elif line.startswith('with '):meaning='Open the named resource for the indented block and close it when leaving the block.'
        elif line=='try:':meaning='Attempt the indented conversion while allowing the specified failure to be handled.'
        elif line.startswith('except '):meaning='Handle only the named exception from the preceding try block.'
        elif line.startswith('print('):meaning='Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.'
        elif '.fit(' in line:meaning='Learn from the supplied training rows and their aligned targets. This changes the fitted object’s state.'
        elif '.predict(' in line:meaning='Apply the already fitted rule to these input rows without passing their true targets.'
        elif '.append(' in line:meaning='Evaluate the argument and add it as one new item at the end of this list.'
        elif '.set_xlabel(' in line:meaning='Label the horizontal axis with the named quantity and unit.'
        elif '.set_ylabel(' in line:meaning='Label the vertical axis with the named quantity and unit.'
        elif '.scatter(' in line:meaning='Plot one point for each aligned x/y pair.'
        elif '.bar(' in line:meaning='Draw one bar for each named category with the supplied height.'
        elif '.hist(' in line:meaning='Count numerical observations into intervals and display those counts.'
        elif '.add(' in line:meaning='Remember this item in the set. Adding the same item again does not create a duplicate.'
        elif '+=' in line:meaning='Add the right-hand amount to the current stored value, then keep the updated value.'
        elif re.match(r'[\w\[\]"\', .]+\s*=',line) and '==' not in line.split('=',1)[0]:meaning='Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.'
        else:meaning='This line continues the surrounding expression or block; read it together with the preceding line rather than running it alone.'
        result.append(f'{line}\n{meaning}')
    return '\n\n'.join(result)

# Assignment concepts, with alternate teaching values rather than issued answers.
TASKS={
'weight_n':('Weight is a force. Multiply the supplied mass by gravitational acceleration and store a numeric result with the required name.','A separate 2 kg practice object weighs 2 × 9.81 = 19.62 N. The assessed object has its own mass.'),
'percent_error':('The signed difference is measured minus expected. Divide by the nonzero reference and multiply by 100. A negative result means the measurement is below the reference.','For a separate example, measured 18 and expected 20 give -10%. Returning the string "-10%" would prevent later numeric calculations.'),
'slab_mass':('First multiply area by thickness to obtain volume. Multiply that volume by the stated density to obtain mass. Both distance units must be metres.','For a separate material at density 1000 kg/m³, area 2 m² and thickness 0.1 m give volume 0.2 m³ and mass 200 kg. Use the assignment’s concrete density for its own task.'),
'power_loss':('Current squared means current multiplied by itself. Multiply that square by resistance to obtain power loss in watts.','With a separate practice current of 3 A and resistance 2 ohms, loss is 3² × 2 = 18 W. ^ is not Python exponentiation; ** is.'),
'mud_pressure':('Multiply density, gravitational acceleration and depth to obtain pressure in pascals, then divide by 1000 for kilopascals.','Check the units aloud: kg/m³ × m/s² × m gives Pa. Returning the Pa number when the task requests kPa produces a factor-of-1000 error.'),
'efficiency':('The specified guard covers zero and negative input power. Handle that before dividing useful output power by input power.','A separate practice case with output 30 W and input 50 W gives 60%. For an invalid input the task requires None, not 0 or an error message string.'),
'worst_reading':('The task asks for two related outputs: the original measurement and its signed percentage error. Compare magnitudes to choose the position, then retrieve both originals.','In a separate example with readings 98, 105, 92 against 100, magnitudes 2, 5, 8 select reading 92 with signed error -8. The assessed six readings differ.'),
'valid_count':('Count records with a nonblank reading after applying the published rules. A blank is not a measured zero.','For numeric text "2", blank, "4", there are two recorded numbers. The assignment uses the current Week 4 300-row CSV.'),
'mean_reading':('Add only the readings admitted by the stated validity rule, then divide by their count. Keep the requested numeric return or variable.','For recorded readings 2 and 4, mean is 3. The skipped blank does not belong in the denominator.'),
'above_limit':('Compare each valid numeric reading against the specified threshold using the exact strict or inclusive relation in the task.','For readings 9,10,11 and a strictly-greater-than 10 limit, the count is 1. Using >= would incorrectly count 2.'),
'group_means':('Produce a dictionary from each group label to its own mean, using each group’s valid count.','Group A with readings 2 and 4 has mean 3. Group B with a single 9 has mean 9. Dividing both by the overall count would be wrong.'),
'clean_records':('Follow the stated cleaning order and record-ID policy on copied records. Preserve the caller’s input and keep legitimate repeated equipment observations.','An estimated replacement belongs only in the specified field. A row dropped earlier must not influence a later training or cleaning statistic.'),
'summarize_records':('Return the published named summary values, including the dictionary of means by equipment. Explain the meaning and unit of each numeric result.','The overall mean weights every retained observation, while an unweighted average of equipment means can give a different result when group counts differ.'),
'audit_cleaning':('Inspect the two lists actually passed in. Report their counts and any specified defects still present after cleaning; do not assume the cleaned input is flawless.','If an independently supplied cleaned list still contains one repeated record ID, the audit must report that remaining defect rather than return zero by assumption.'),
'predict_regression':('Build feature rows using only the specified input fields and preserve their order. Fit preprocessing and the three requested models using training records only.','The returned dictionary contains baseline, linear and tree, each with one prediction per feature record. A feature record deliberately contains no target answer.'),
'regression_errors':('Pair actual and predicted values by position. Return mae and rmse with full numerical precision.','On separate teaching pairs with errors 2 and 4, MAE is 3 and RMSE is sqrt(10). Rounding is for a labelled display, not for the returned metric.'),
'classification_metrics':('Count the four mutually exclusive actual/predicted cases, then calculate the specified fractions and cost from those counts.','Verify TP+TN+FP+FN equals the number of paired observations. Read the cost weights and zero-denominator convention from the issued brief.'),
'group_split':('Choose groups using the task’s deterministic rule, then return record IDs in the required train, validation and test lists.','Check that each equipment ID appears in only one partition and that every record is accounted for. A random row split does not satisfy this interface.'),
'make_features':('Create the requested numeric feature rows in the same order as the input records. Use only information available at prediction time.','Distinguish load_pct from load_pct/100. The task’s named interaction uses its exact published formula; a mathematically related alternative would still violate the interface.'),
'ablation_metrics':('Compare the original and extended feature sets with the same training and validation observations and the same model protocol.','Return the specified metrics and improvement calculation. A reduction from MAE 5 to 4 is improvement 1, not -1, when the contract defines before minus after.'),
'select_model':('Filter by both published limits, then apply the full tie-break rule. Return the requested model identifier or the specified no-candidate result.','Check an exactly-on-limit candidate, a tied pair and an empty eligible list. These are ordinary contract cases rather than optional extensions.'),
}

UNMATCHED=[]
def notes_for(d,s,src,previous,following):
    name=Path(d['path']).name;week=int(re.search(r'Week(\d+)',name)[1]);cohort=name[:7]
    heading=src['title'] if src else title(s);body=clean_body(s,src);kind=(src or {}).get('kind','');text=s['text'];low=heading.lower()
    parts=[f'{heading}\n{cohort}, Week {week}, slide {s["number"]}']
    p=None
    lookup=heading
    if src and src.get('concepts'):lookup+=' '+ ' and '.join(c['term'] for c in src['concepts'])
    # Operational notes use the specific assessment, never a topic guessed from the week.
    if 'QUIZ ACCESS' in text or 'END-OF-SESSION QUIZ' in text or re.search(r'Week \d+.*[Qq]uiz|Week \d+ quiz',heading):
        qweek=1 if 'Week 1' in heading else week
        p=[f'This is the {cohort} Week {qweek} quiz. The student link opens the response form; it does not activate its window. In Quiz Controls use open_W{qweek}_{cohort} when ready and read the logged closing time.',
           'Explain the distinction between the expected answering time and availability: five minutes of questions can still be available for 24 hours after activation. Enter the learner’s own Student Registration Number and use the registered Google account.',
           'Read the exact live cutoff before announcing it. Do not promise a new attempt to somebody who already submitted. Quiz catch-up and assignment uploads are separate forms.']
    elif 'ASSIGNMENT SUBMISSION' in text or 'catch-up upload' in low or low.endswith(' submission'):
        m=re.search(r'Open (W\d+|DA_PROJECT|ML_PROJECT|TEST1|TEST2|DEMO) assignment',text);aid=m[1] if m else 'W01' if 'A1' in heading else f'W{week:02}'
        entry=LINKS.get(cohort+'|'+aid,{})
        uploads='one completed .ipynb notebook'
        if aid=='W01':uploads='one DOCX or selectable-text PDF report'
        if aid=='W02':uploads='the completed proof_of_life notebook and the learner’s own README.md, with the repository URL in its form field'
        if aid in ('DA_PROJECT','ML_PROJECT'):uploads='the completed project notebook together with one readable DOCX or selectable-text PDF report'
        if aid=='DEMO':uploads='the presentation with narration notes and the required written defence/reflection document, as listed in the DEMO guide'
        p=[f'This slide hands over {cohort} {aid}. Show the exact form title before uploading. The required packet is {uploads}.',
           ('For TEST1/TEST2, save Part B under My written evidence. Collect the complete notebook offline under invigilation; the later form upload only transports that collected version.' if aid.startswith('TEST') else f'The recorded cutoff for this form is {entry.get("closeAt","not yet scheduled")}. Check the live form for later changes. A replacement must contain the complete required file set, not just the changed file.'),
           'Students enter their own Student Registration Number as required freeform text. They wait for filenames to appear, press Submit and keep the confirmation. A file saved in Drive or GitHub is not itself a form submission.']
    elif s['number']==1 or heading=='Today’s learning':
        p=[AIMS[week][0],AIMS[week][1],('Use this as an orientation to the lesson. Terms and syntax will be unpacked on their own slides; students do not need to know them in advance.' if s['number']==1 else 'At the end, check the specific outcome shown here using a small previously demonstrated example. A completed file without an explanation is not evidence of understanding.')]
    elif 'Your required task'.upper() in text or re.match(r'q\d+:|valid_count \(|mean_reading \(|above_limit \(|group_means \(',heading) or (src and kind=='task'):
        key=next((k for k in TASKS if re.search(r'\b'+re.escape(k)+r'\b',heading+' '+body)),None)
        if key:p=[TASKS[key][0],TASKS[key][1],'Keep the exact output names and required types. Use the task text for the learner’s own assessed answer; the alternate example explains the method without replacing their work.']
        elif week==5:
            q=int(re.search(r'q(\d+)',heading)[1]);a={1:('Load the named CSV into df. Reading the file is different from constructing a new table with copied example values.','Inspect the header and 24-row file before analysis.'),2:('Count distinct meter_id values, not rows. A meter can contribute several monthly observations.','Two readings from M-001 count as one distinct meter.'),3:('Create cost_per_kwh by dividing each row’s cost_ugx by its kwh.','For 6000 UGX and 10 kWh the rate is 600 UGX/kWh.'),4:('Filter whole rows using the strict kwh > 5000 comparison, after creating the rate column.','A reading exactly 5000 does not pass this condition.'),5:('Find the mean of the created cost_per_kwh column, following the task’s stated table scope.','Mean of rates is not generally total cost divided by total energy.'),6:('Sum kwh by building and return the label with the greatest total.','max gives a total; idxmax gives the label attached to that total.')}[q]
            p=[*a,'The student submits the completed notebook only. Grading runs on the lecturer’s side; the current package needs no grading scripts.']
    elif 'Optional revision video'==heading or 'explainer' in low or heading=='After the video' or ('VIDEO' in text.splitlines()[:1]):
        question=next((x.split('Listening question:',1)[1].strip() for x in body.splitlines() if 'Listening question:' in x),'Explain the distinction or mechanism named on this video slide using one example from today.')
        p=[f'Give the viewing question before playing the excerpt: {question}',
           'Use the adjacent worked example as the explanation if the video cannot load. Pause after the relevant example and connect its terms to the names and units already used in this lesson. Preview the displayed link and excerpt before class.',
           'The video is supporting revision, not a replacement for defining the symbols or a requirement to watch a full tutorial during limited class time.']
    elif heading in ('Revision and submission checklist','Before you leave'):
        p=[AIMS[week][0],AIMS[week][1],'Close by identifying the actual saved file and its correct submission route. Read the live deadline. For current weekly notebook tasks, students upload their own work, not the practice notebook, ZIP or grading files.']
    elif heading in ('Connection to the previous lesson','Why this week’s tools are needed','Recall and a first attempt'):
        p=[AIMS[week][0],AIMS[week][1],'Connect this to the previous result named on this slide. Demonstrate the first step again if necessary; there is no requirement for partner work before the explanation.']
    elif heading in ('Revision example and answer','Your turn','Practice discussion','Expected output'):
        answer=body
        if heading=='Your turn' and following:answer=clean_body(following.get('slide',{}),following.get('source'))
        p=['Use the displayed example as a short individual revision question, then explain the reasoning behind its answer.',answer,'Trace the operation that changes the value rather than accepting a memorised output. For notebook-state examples, specify which cell is repeated and whether the initialisation ran again.']
    elif week in (7,14) and not (src or {}).get('code'):
        if 'submission' not in low:
            if 'Test session'==heading or 'Timing and Part B' in body:p=[AIMS[week][0],AIMS[week][1],'At the Part A boundary, follow the official snapshot procedure. During the 25-minute Part B period, students type reasoning but must not execute code. Do not change the published timing during an explanation.']
            elif any(t in low for t in ['save','rehearse','preparation','your evidence','procedure']):p=['Show the offline save location and reopen the file before test day. Identify both the code cells and the markdown cell headed My written evidence.','Use a separate practice notebook for rehearsal. Students should locate the actual .ipynb on disk rather than rely on a browser tab or cloud link.','During the assessed period, report technical failures immediately and follow the invigilator’s instructions. Do not introduce new modelling code or online resources.']
            else:p=assessment_explanation(body,week)
    elif any(t in heading for t in ['Data analysis project','Engineering ML project','Written evidence','Preparing for the assignment','Project preparation','Your issued task','Your issued assignment','Week 4 rules','Your evidence','Week 2 assignment','A1 —']):
        p=assessment_explanation(body,week)
    elif heading in ('The engineering context','Measurements become observations','Your cohort data','Read the quantities in your programme example','A calculation for your programme','The calculation in Python','Your programme formula'):
        p=context_explanation(cohort,week,heading)
    elif 'Read the quantities before' in heading or 'Unit conversions' in heading:
        p=['Track the meaning and unit before substituting values. Mass is in kg, weight is in N, area in m² and volume in m³. Power is energy transferred per second, in W.','Convert 200 mm to 0.2 m by dividing by 1000. A separate 2 kg mass has weight 19.62 N using g = 9.81 m/s². A percentage 75 becomes fraction 0.75.','Do not mix area, volume, mass and force. The name G is an uppercase convention for a fixed value, not an automatic unit system. Only introduce rpm conversion when that quantity is actually needed.']
    elif heading=='Week 3 continuation':p=['This is now a recap point for CML3112, whose full Week 3 lesson was completed on 29 September. For CML3111/CML3113, begin the Week 3 deck at slide 1.','Revisit the preceding result: float("3.5") gives 3.5 and multiplying by 2 gives 7.0. The printed type is <class \'float\'>. Next extend these values into arithmetic and decisions.','Do not treat slide 13 as an instruction to skip the foundations in a cohort that has not covered them.']
    elif heading=='How to read the examples':p=['Point out the code block, the explanatory text and the displayed result as different objects. The learner types the code only.','For print(2 + 3), the typed instruction contains print and parentheses. The result underneath is 5; the learner should not type the label Output or the explanatory sentence into the Python cell.','For a program split over consecutive slides, keep its setup and indentation together. A later fragment may use a name created on the preceding slide.']
    if p is None:p=explanation(heading) or explanation(lookup)
    if not src and week==2 and s['number'] in LEGACY_W2:
        p=[LEGACY_W2[s['number']], 'Point to the particular code cell or answer on this slide while explaining the reasoning.', 'The current assignment guide and live form take precedence over historical logistics printed in this deck.']
    if p is None:
        p=legacy_special(week,s,heading,body,following)
    if p is None:
        UNMATCHED.append((name,s['number'],heading,body))
        return ''
    labels=['Explanation to give','Worked illustration / lecturer answer','Misconception to address']
    parts += [label+'\n'+value for label,value in zip(labels,p) if value]
    # The actual slide anchor distinguishes similar concepts, traces and continuations.
    if src and body and body not in p and not src.get('code'):
        anchor=body.strip()
        parts.append('On this slide\n'+anchor)
    if src and src.get('code'):
        parts.append('Read the displayed code line by line\n'+code_walk(src['code']))
        if src.get('caption'):parts.append('Result / continuity\n'+src['caption'])
    if week in (3,5) and ('assignment' in low or re.match(r'q\d+:',heading)):
        parts.append('Current notebook workflow\nThe latest student package contains no grader scripts or g.check cells. Restart and run the completed notebook, then submit it. Existing older submissions remain valid.')
    refs=re.findall(r'https?://[^\s<>]+',s.get('notes',''))
    refs=[r for r in refs if not any(x in r for x in ['docs.google.com','forms.gle'])]
    if refs:parts.append('Reference / existing resource\n'+'\n'.join(dict.fromkeys(refs)))
    if following:
        nxt=following['source']['title'] if following.get('source') else title(following['slide'])
        parts.append('Continue to\n'+nxt)
    return '\n\n'.join(parts)

def context_explanation(cohort,week,heading):
    if cohort=='CML3112':p=['Use a room or floor as the physical reference. Length and width are distances in metres. Multiplying them produces area in m²; multiplying by thickness produces volume in m³.','For the displayed rectangle, 5 m × 3 m = 15 m². Density connects volume to mass. Indoor temperature, energy and cooling load are different quantities and should retain their own units.','The later assignment uses slab_mass(area_m2, thickness_m). Explain its two inputs before introducing density. A number without its unit can be ambiguous.']
    elif cohort=='CML3111':p=['Use an electrical device as the physical reference. Voltage is measured in volts, current in amperes and power in watts. State what each quantity describes before multiplying them.','In the displayed introductory calculation, 12 V × 2 A = 24 W. The later resistive-loss formula uses current squared times resistance; it is a different calculation with a different input pair.','Do not confuse input voltage with resistance or energy with power. Read the exact programme task and its units before substituting numbers.']
    else:p=['Use fluid moving through a system as the physical reference. Volume in litres divided by elapsed seconds gives a flow rate in L/s. Density and depth belong to a later pressure calculation.','In the displayed introductory calculation, 18 L / 3 s = 6 L/s. For the later pressure task, density × g × depth yields Pa, then division by 1000 converts to kPa.','Flow rate and pressure are different physical quantities. Keep litres/seconds separate from the SI units specified for mud_pressure.']
    if week in (2,4):
        files={'CML3112':'site_inspection_log.csv','CML3111':'motor_test_bench.csv','CML3113':'drill_shift_log.csv'}
        p[1]=f'Show {files[cohort]} in the runtime Files panel. The Week 2 file has four rows for setup; Week 4 uses its own 300-row file. Inspect the header to locate this cohort’s reading field and group field.'
    return p

def assessment_explanation(body,week):
    b=body.lower()
    if 'synthetic teaching records' in b:
        return ['Name this cohort’s target and its unit exactly as displayed. Each row is one operating observation, while equipment_id can repeat across several observations.','Explain record_id as the identifier of an observation, load_pct as load expressed in percent and ambient_c as temperature in degrees Celsius. The target records the known answer in training data.','These are synthetic examples for learning. They do not establish a calibrated physical relationship or justify operation of real equipment.']
    if 'same equipment' in b:
        return ['Keep related equipment observations together so the validation really represents equipment the model has not seen.','The written question may supply a comparison scenario. Label those numbers as supplied scenario evidence; do not claim they came from a run of your own notebook.','A supplied scenario and an observed experimental result have different provenance. Both can be interpreted, but should not be confused.']
    if 'classification_case' in b or 'teaching assumptions' in b or 'claimed benefits' in b:
        return ['The warning labels and costs belong to this teaching scenario. Name what positive means before discussing benefit or harm.','Compute the confusion counts from aligned actual/predicted labels, then apply the published cost weights. A false alarm and a missed warning can have different costs.','These illustrative costs are not approved operational thresholds. Claimed benefits need evaluation on relevant real observations before use in engineering decisions.']
    if 'validation_mae' in b or 'graded interfaces' in b:
        return ['For W12, read the candidate fields exactly: name, validation_mae and latency_ms. Enforce both inclusive limits before ranking by error, latency and alphabetical name.','A candidate exactly at both limits is eligible. If the eligible list is empty, return None. The simpler error/ms names on practice slides must be adapted to the assignment’s published field names.','A sensible general recommendation does not replace the exact graded return interface. Keep the function contract and the wider project discussion distinct.']
    if 'no new weekly assignment' in b:
        return ['Week 13 adds no new weekly assignment notebook. Use the time to make the existing project reproducible and prepare for the offline test.','Open the project README, restart and follow its steps. Then rehearse locating and reopening the complete test notebook on the prepared offline computer.','Quiz 13 is a separate activity when activated. Do not invent an A13 upload or require students to submit an extra weekly report.']
    if 'defence' in b or 'reflection' in b:
        return ['The team project and the individual DEMO evidence have separate purposes. Each learner submits their own explanation of decisions and reflection on learning.','A defence points to specific cells or results in the project. A reflection describes changed understanding, remaining difficulties and the required Semester 2 goals.','Do not submit one generic team reflection for everybody. Follow the DEMO guide’s presentation and written-document requirements.']
    if 'problem definition' in b:
        return ['Bound the proposed engineering problem: identify the decision, intended users, operating setting and quantity or class to predict. Explain why the target supports that decision.','A target should be chosen because knowing it helps the decision, not merely because it is a convenient numeric column in the file.','A broad theme such as “AI for buildings” does not yet specify a model task. The project report must make the target and intended use explicit.']
    if week==2:
        if 'a1' in b and ('problem' in b or 'week 1' in b):return ['A1 is a short problem-framing report, separate from A2. Explain the four sections: three proposed problems, then the selected problem and dataset rationale.','For each proposed problem, identify the decision, available inputs, target, plausible data source and one limitation. Students are proposing a study; they are not training a model.','Submit one DOCX or selectable-text PDF through A1. A2 is the notebook and README, and Quiz 1 and Quiz 2 each have their own link.']
        return ['For A2, the main working file is proof_of_life.ipynb. The student completes it, writes the execution-order explanation and creates their own README.','A fresh successful run should show proof_sum 4, readings 17 and the four rows from the cohort CSV. The repository keeps the notebook and CSV, while the form receives the notebook and README plus its repository URL.','Repair notebooks 01–04 and hello_engineering.py are practice only. Do not turn them into extra submissions or mistake the supplied package README for the student’s own README.']
    if week==3:return ['A3 has five tasks in one notebook: a weight value, signed percentage-error function, programme-specific function, guarded efficiency function and the largest-error reading.','Explain the required names and return values. Compare a signed error by magnitude only for choosing the worst reading, then keep its original sign. Loops are not required for this six-reading task.','The latest notebook needs no grading scripts. Submit one .ipynb, with no separate report. Keep any work already completed in an older notebook.']
    if week==4:return ['A4 uses the Week 4 300-row cohort CSV. The required outputs are valid_count, mean_reading, above_limit and group_means. Work only with the rows admitted by the published blank-reading rules.','Trace a smaller unrelated dataset first: A readings 2 and 4 yield A mean 3; B reading 9 yields B mean 9. Each group needs its own denominator.','Despite “Reading report” in the title, A4 is one completed Python notebook, not a separate Word report. Do not use Week 2’s four-row CSV.']
    if week==5 and 'project' not in b:return ['A5 uses the supplied campus_energy.csv and six named pandas outputs. Start with the loaded table, then create the rate column before taking the filtered subset.','Distinguish distinct meter count, a mean rate and the building with greatest total energy. These are three different questions about the same table.','Return the exact requested values in one completed notebook. The learner does not upload data, ZIPs, helper scripts or a separate report for A5.']
    if 'my written evidence' in b:return ['Show the actual markdown answer cell headed My written evidence. This is where the learner explains the choices and the supplied scenario in their own words.','A useful explanation connects a decision to a named result and its limitation: for example, why a training-only median avoids using evaluation information. Describe supplied scenario figures as supplied, not as measurements the learner produced.','Prompts and copied code comments do not substitute for the learner’s reasoning. Weekly work and tests use the notebook; projects also require their separate readable report.']
    if 'contribution' in b or 'seeds' in b:return ['Make contribution evidence specific enough to check. A seed records the starting state of random choices; a contribution log records who produced and explained which work.','Name a file, function or chart and the decision behind it. Match that entry to meaningful repository history. Disclose AI assistance according to the assessment policy.','Many commits do not necessarily mean substantial work, and a seed does not establish accuracy. Both are supporting evidence, not replacements for the analysis.']
    if 'chart' in b or 'visualisation' in b:return ['A chart must answer a stated question and show the actual data result. Explain what one mark represents and label both the quantity and unit before stating the finding.','A useful caption names the group or sample, the observed difference and the relevant unit. A limitation states what the plotted observations cannot establish, such as causation or performance at a new site.','Text claiming “a chart was made” is not the required chart. Check the exact number and kinds required on this slide and in the assessment guide.']
    if 'leakage' in b or 'pipeline' in b or 'split' in b:return ['Explain the order: partition data using the stated protocol, fit preparation on training data, fit models, compare on validation data and leave final test data untouched until choices are fixed.','Compare models on identical held-out observations with the same metric and preprocessing rules. Each cross-validation training fold learns its own preparation values.','A written claim of no leakage must agree with the executable split and fitting code. Follow the published execution requirement for any criterion linked to the split check.']
    if 'reasoning' in b or 'what further data' in b or 'what evidence' in b:return ['Explain the decision, the evidence supporting it and what would change that decision. The reader should be able to find the result cited in the notebook.','For example, a model may justify further testing at a second site while not yet justifying deployment. Name the missing operating range or equipment group that the next data collection should cover.','During test Part B, type the explanation offline without executing code. Save it in the collected notebook; later upload must not extend the assessed work period.']
    if 'licence' in b or 'provenance' in b or 'question' in b:return ['Problem framing begins with a bounded engineering decision and a defined target. Provenance explains where observations came from; a licence states what reuse is allowed.','State the population, measurement period, units and who collected the data. Explain how those observations could answer the chosen question rather than merely describing an interesting file.','Synthetic teaching data must be labelled as synthetic. A plausible story does not establish that a dataset contains the information or permissions the proposed project needs.']
    if 'cleaning' in b or 'profiling' in b:return ['Describe the received table before changing it: its rows, columns, units and defects. Then explain each cleaning rule and preserve the original data.','A duplicate record ID and repeated equipment ID are different situations. Removing the former under a stated rule may be correct while removing the latter could discard legitimate observations.','A correct output without a justification may not satisfy the reasoning criterion. Use the task’s exact rules rather than choosing whichever cleaning makes results look attractive.']
    if 'metric' in b or 'score' in b or 'interpretation' in b:return ['Read the metric with its unit and evaluation population. Explain why that error measure matches the cost of a wrong decision in the stated engineering setting.','MAE 3 kW describes an average absolute error on named observations; it does not guarantee every prediction lies within 3 kW. Report baseline comparison and the evaluation protocol.','Avoid a deployment claim based only on a score. State genuine limitations involving data coverage, measurement quality or future operating conditions.']
    if 'reproduc' in b or 'readme' in b or 'runs' in b:return ['Reproducibility means a clean run using the delivered files, documented dependencies and stated instructions produces the reported results.','Use an actual fresh-runtime check. Correct a path or missing setup step that the check reveals, then save the successful notebook and instructions.','Saved figures can remain visible after code breaks. Their presence alone is not a successful rerun.']
    return ['Connect this requirement to a concrete piece of submitted evidence rather than reading the rubric as a list of abstract words.','For this slide, identify the named function, written section or project file in the issued notebook/guide and point to the location where the learner should provide it. Weekly W06–W12 tasks put required reasoning in My written evidence; project rubrics require the separate readable report too.','Keep the requirement shown here distinct from the weekly practice. Do not add extra files or activities beyond the issued assessment.']

LEGACY_W2={
5:'Recall features as information known beforehand and target as the answer to predict. Days until servicing is a quantity, so regression. A fixed verified formula may make ML unnecessary. Use the following answer slide to explain why, without requiring partner discussion.',
11:'Read the three cells separately. Cell 1 prints the cohort greeting and 4. Cell 2 assigns readings = 12 and the f-string inserts 12 into the text. Repeating only cell 3 gives 17,22,27. Repeating cells 2 and 3 resets to 12 and ends at 17. Braces inside an f-string request the current value; they are not printed literally.',
14:'Enter creates a new line; Shift+Enter executes. hello appears below its code cell. Values 17 and 27 can both result from the shown update if it has run different numbers of times. The difference exposes shared runtime state, not different arithmetic.',
21:'Counters [4],[1],[5],[2] show nonsequential execution, but do not alone prove an incorrect answer. Restart and run in the written order to check. Failure after a restart may reveal a stale variable, missing input file or missing setup; diagnose the actual first exception.',
23:'Counters [2],[7],[3] reveal execution order, not a complete history. A blank counter usually means a cell has not executed in the current session or its execution information was cleared. It does not establish that every later result is wrong. Restart, load the required data and run all to test the dependency chain.',
31:'A2 requires the completed main notebook and the student’s own README.md, with a repository URL in the form. Keep the CSV in the runtime/repository. The current guide is authoritative about the required execution-order explanation; repair exercises are practice. Read the live form cutoff rather than the old “start of Week 3” label.',
34:'There are separate submission actions: activate the Week 2 quiz for a 24-hour window, and use the A2 form for the completed notebook plus README. Five minutes is expected quiz effort, not a five-minute opening. Where catching up, A1 and Quiz 1 have separate links.',
37:'A: restart and run with required data available, then diagnose the first error. B: counters record actual execution sequence. C: git add naming two files stages those two, not all five. D: GitHub records project history; the current course collects graded files through the assignment form. E: Tests 1 and 2 use the prepared offline environment with invigilated collection.',
38:'Clarify the old GitHub wording: repositories preserve work and contribution history, but the current grader receives uploaded assessment files. Students still need the appropriate submission form. A notebook that fails after restarting may lack variables, files or setup; do not assert stale memory is the only possible cause.',
42:'Use this as a reference, not a command drill. Today’s browser GitHub route does not require the terminal commands. Before submission, load the correct data, restart, run all and save. For an error, read its type and the indicated operation, then describe what was expected and what happened.',
44:'Close with a precise correction: some wrong results produce no exception, so reading errors is only part of checking work. Verify run order, the input file, units and whether the result is plausible. Next week explains the Python values and operators used in the first notebook.'}

def legacy_special(week,s,heading,body,following):
    if heading in ('By the end of today you can…','What you should take away','Where we got to, and where we are going'):
        return [AIMS[week][0],AIMS[week][1],'Use the outcomes listed on this slide to check understanding through the small examples, rather than asking only whether everybody understands.']
    if heading in ('One value and a collection of values','Lists dictionaries tuples and sets','Choosing the right collection','How the four collections differ'):
        return ['Compare the access rule for each collection. Lists and tuples use positions; dictionaries use keys; sets answer membership questions. Lists can change their items, while tuple positions cannot be reassigned.','For readings use an ordered list. For a record with unit and reading fields use a dictionary. For a coordinate pair use a tuple. For IDs already seen use a set.','A set cannot be indexed. Dictionary keys are unique, but values may repeat. {} is an empty dictionary; set() is an empty set.']
    if heading=='Feature, and target':return explanation('Feature and target')
    if week==1 and s['number']==21:return explanation('question this course')
    if heading in ('Gallery walk, and what you owe me','Before Week 2'):
        return ['Use this handover to state A1 clearly: three candidate problems and one justified selection, written as a short report.','Each problem identifies its inputs, target, possible data source and limitation. Submit one DOCX or selectable-text PDF through the A1 form. Account setup prepares for Week 2 and is separate from the report.','Read the live deadline, including any catch-up extension. The historical gallery walk is optional; explain one sample problem directly when class time is limited.']
    if heading in ('Four questions, four tools','The four questions'):
        return ['Give each tool one job: Python expresses instructions, a notebook combines code and explanations, Colab runs the notebook in a browser, and Git/GitHub records and hosts project versions.','A saved .ipynb can move between notebook environments. Moving the document does not necessarily move the running session or its uploaded CSV.','Do not imply students must master all tools at once or that no other tool can ever be needed. Demonstrate the browser workflow used for this assessment.']
    if week==2 and heading=='Worked example':return explanation('Execution order')
    if heading=='Week 5 support':
        return ['This is a scheduling notice for the Friday cohorts. Confirm the faculty-approved replacement teaching arrangement before announcing details.','Provide a supported explanation of the pandas examples and an opportunity to ask questions. Begin the following session by revisiting column selection, masks and group summaries.','A published upload deadline is separate from a replacement teaching session. Do not invent a session time or treat video-only homework as sufficient replacement support.']
    if heading=='Practice before test day':
        return (['Rehearse this small calculation before the assessed session. The list has three values, so len returns 3. Add 3+5+7 to obtain 15, then divide by 3.','The displayed output is 3 followed by 5.0. Explain why the mean is a floating-point result even though the inputs are integers.','This is a preparation example, not a test answer. During Part B of the actual test, code execution is prohibited.'] if week==7 else ['Pair the actual and predicted values in order. The first absolute error is abs(4-5)=1; the second is abs(8-6)=2.','Their mean is (1+2)/2=1.5. The unit is the target unit. Both observations contribute once to the numerator and denominator.','Use the practice values only before the assessed session. MAE 1.5 is an average, not a maximum error guarantee.'])
    if week==15 and heading=='Preparation checkpoint':return ['Each learner should be able to explain one decision they personally worked on and point to its evidence in the project.','Ask for the relevant cell, chart or contribution entry, then a reason for that choice and a limitation. This connects authorship to understanding.','Live discussion is formative. Collect the individual written evidence required by DEMO so the automatic assessment has the explanation in an accessible form.']
    if week==2 and s['number'] in LEGACY_W2:return [LEGACY_W2[s['number']],'Use the actual cell, filename or answer choices displayed on this slide to anchor the explanation.','Treat the published current assignment guide and live form as authoritative where a historical slide shows older logistics.']
    if week==2 and heading=='Week 2 includes your Week 1 catch-up':return ['Separate the four tasks so students do not combine unrelated uploads: A1 report, Quiz 1, A2 notebook and README, and Quiz 2.','Show each matching title and link. A1 and A2 are assignment forms; the quizzes record responses separately and have their own 24-hour activations.','A1 catch-up is still required even though the class is now studying Week 2. Read the current live deadlines rather than calculating from an old slide date.']
    if heading=='Jotham Martin Wambi':return ['Introduce your applied data and teaching work briefly, then link it to what beginners will learn in this course.','Use the formally accurate affiliation: incoming PhD student in Applied Informatics, Osaka Metropolitan University, Japan, April 2027 intake. The acceptance precedes enrolment. The master’s institution is Yamaguchi University, Japan.','The older visible “PhD student” wording predates the clarified enrolment status. Do not describe yourself as already enrolled for the December 2026 period.']
    if 'CHECK YOUR UNDERSTANDING' in s['text'] or heading.startswith('Self-test'):
        answer=following['slide']['text'] if following else body
        return ['Explain each answer in relation to the question rather than giving only its letter or label.',answer,'Use a short lecturer-led walkthrough or individual thought time. Do not require partner work to unlock the explanation.']
    if s['text'].startswith('ANSWERS'):
        return ['For each answer on this slide, identify the deciding feature of the question: timing of the input, kind of target, run order or operation requested.',body,'If a student gives a different engineering example, check its reasoning and timing rather than requiring identical wording to the printed example.']
    if s['text'].startswith('GLOSSARY'):
        terms=body.splitlines();matched=[]
        for term in terms:
            e=explanation(term)
            if e and e not in matched:matched.append(e)
        if matched:return ['\n\n'.join(e[0] for e in matched[:3]),'\n\n'.join(e[1] for e in matched[:3]),'Use this page for revision. Connect each word to the concrete example just taught; do not introduce all the definitions as new material in one block.']
    if heading=='Break':return ['Announce the actual return time based on the clock now, rather than leaving “ten minutes” ambiguous.','Save the current notebook before the break. On return, continue at the next topic named in the deck.','No new assessment or group task is assigned by this divider.']
    if s['text'].startswith('SEGMENT'):
        next_title=title(following['slide']) if following else heading
        e=explanation(next_title)
        if e:return [f'This divider introduces {next_title}. '+e[0],e[1],'Keep this transition brief. The detailed demonstration follows; do not add another activity before students have seen it.']
    return None

def main():
    plans=[]
    for d in INVENTORY:
        srcdeck=SOURCES.get(Path(d['path']).name)
        if srcdeck:assert len(srcdeck['slides'])==len(d['slides']),d['path']
        slides=[]
        for i,s in enumerate(d['slides']):
            src=srcdeck['slides'][i] if srcdeck else None
            nxt={'slide':d['slides'][i+1],'source':srcdeck['slides'][i+1] if srcdeck else None} if i+1<len(d['slides']) else None
            note=notes_for(d,s,src,d['slides'][i-1] if i else None,nxt)
            slides.append(dict(s,heading=src['title'] if src else title(s),notes=note))
        plans.append(dict(path=d['path'],sha256=hashlib.sha256((ROOT/d['path']).read_bytes()).hexdigest(),slides=slides))
    (OUT/'notes-plan.json').write_text(json.dumps(plans,ensure_ascii=False,indent=2)+'\n')
    unique={(x[0].split('_Week')[1][:2],x[2]):x for x in UNMATCHED}
    (OUT/'unmatched.json').write_text(json.dumps(list(unique.values()),ensure_ascii=False,indent=2))
    print('Slides',sum(len(d['slides']) for d in plans),'unmatched',len(UNMATCHED),'unique',len(unique))
    for (w,t),x in unique.items():print(w,t)
if __name__=='__main__':main()
