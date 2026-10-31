"""Build the Holiday Data and AI Camp pack (revision 2).

Everything under camp_2026/{student_materials,instructor_materials,curriculum} is generated
from build/lessons/. Edit those, then rebuild. Never edit a generated sheet by hand.

    python Schools_ML_Track/camp_2026/build/build_camp.py
    python Schools_ML_Track/camp_2026/build/verify_camp.py
    python Schools_ML_Track/camp_2026/build/package_camp.py
"""
import csv
import json
import random
import re
import shutil
from pathlib import Path

from common import (ROOT, CURRICULUM, SUNRISE_DIR, DEFAULT_CLOCK, SUNRISE_FILES, DATA_DA, DATA_ML, TRACK_NAMES)
from content import ML, DA, LABS, EXTENSION

WEEK_THEMES = {
    'DA': ['Meet the data', 'Python you need', 'Tables in pandas', 'Clean and chart',
           'Explore with NumPy and seaborn', 'Messy data and two tables', 'Show it', 'Hand over'],
    'ML': ['Python and a first prediction', 'Python you need', 'Tables and statistics', 'Clean, chart, question',
           'Baselines and a line', 'Trees and fair tests', 'Your project', 'Hand over'],
}
WEEKLY_PRODUCT = {
    'DA': ['A notebook that reads the shop table and an error log',
           'Three small Python programs with checks that pass',
           'Revenue by item and by branch, checked against the hand total',
           'Checkpoint one: a cleaned table, three labelled charts, findings',
           'Spread, distributions and relationships explored, with what each shows',
           'Checkpoint two: clean, merge and reconcile, with the residual named',
           'An approved project plan and a rerunnable notebook',
           'The report, the five-minute talk and the unaided demonstration'],
    'ML': ['A first prediction run, a small calculation notebook and F01',
           'A flower rule, a loop and a checked function, plus F02',
           'A described table, a revenue column and summary numbers, plus F03',
           'Checkpoint one with a chart and a project question, plus F04',
           'A baseline and a fitted line with their errors compared',
           'Checkpoint two: a tree compared fairly with a locked final test',
           'An approved plan, a baseline and a compared model',
           'The final test, the report and the unaided demonstration'],
}
PRACTICE = {
    'DA': ['Change two quantities in the revenue calculation, predict the result on paper, run it and explain it.',
           'Change a function input, test zero and one ordinary value, and trace a loop over three items.',
           'Rerun the grouped total on a different column and reconcile it with a hand count of five rows.',
           'Finish the cleaning log and the labelled charts. Rerun checkpoint one from a restarted kernel.',
           'Explain one chart and one correlation in your own words, with its limit.',
           'Finish checkpoint two. Find the residual difference and name its cause.',
           'Build the approved project incrementally. Save your independent attempt before any supervised AI critique.',
           'Rerun and hand in the project at session 22; rehearse an unaided explanation and a small code change.'],
    'ML': ['Change two quantities in the arithmetic example, predict the result on paper, run it and explain it.',
           'Change the function inputs, test zero and one ordinary value, and trace a loop over three items.',
           'Compare mean and median before and after an extreme value. Keep a note on the units.',
           'Finish the cleaning log and labelled charts. Rerun checkpoint one; write two findings and one limitation.',
           'Explain the baseline and check one prediction error by hand.',
           'Finish checkpoint two. Explain one split or model mistake and repair the method, not the number.',
           'Build the approved project incrementally. Save your independent attempt before any supervised AI critique.',
           'Rerun and hand in the project at session 22; rehearse an unaided explanation and a small code change.'],
}
LAB_AFTER = {3: 'F01', 6: 'F02', 9: 'F03', 12: 'F04'}


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8', newline='\n')


def code_block(src):
    return '```python\n' + src.rstrip('\n') + '\n```'


def md_table(head, rows):
    out = ['| ' + ' | '.join(head) + ' |', '|' + '|'.join(['---'] * len(head)) + '|']
    for r in rows:
        out.append('| ' + ' | '.join(str(c).replace('|', '/').replace('\n', ' ') for c in r) + ' |')
    return '\n'.join(out)


def clock_table(lesson):
    p = lesson.get('pacing')
    if p:
        rows = []
        for part in [x.strip() for x in p.split(';') if x.strip()]:
            m = re.match(r'(\d+)\s*minutes?\s*(.*)', part)
            rows.append((m.group(1), m.group(2)))
    else:
        rows = [(str(m), label) for label, m in DEFAULT_CLOCK]
    return md_table(['Minutes', 'Activity'], rows), sum(int(m) for m, _ in rows)


# ------------------------------------------------------------------ data
def build_data():
    data = ROOT / 'data'
    rng = random.Random(19)
    products = [('Book', 'Stationery', 3000), ('Pen', 'Stationery', 1000), ('Juice', 'Refreshment', 2000)]
    rows = []
    for i in range(60):
        item, category, price = products[i % 3]
        rows.append(dict(sale_id=i + 1, date=f'2026-12-{1 + i // 3:02}', item=item, units=rng.randint(1, 8), unit_price_ugx=price))

    def savecsv(name, values):
        with (data / name).open('w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=list(values[0]), lineterminator='\n')
            w.writeheader()
            w.writerows(values)
    savecsv('camp_shop.csv', rows)
    homes = []
    for i in range(120):
        area = rng.randint(20, 180)
        rooms = rng.randint(1, 5)
        homes.append(dict(home_id=i + 1, area_m2=area, rooms=rooms, rent_ugx=100000 + area * 3000 + rooms * 20000 + rng.randint(-25000, 25000)))
    savecsv('synthetic_homes.csv', homes)
    return rows


def reference_values(rows):
    key = json.loads((SUNRISE_DIR / 'answer_key.json').read_text())
    by_item = {}
    for r in rows:
        d = by_item.setdefault(r['item'], [0, 0, 0])
        d[0] += r['units']
        d[1] += r['units'] * r['unit_price_ugx']
        d[2] += 1
    ref = {'camp_shop': {'row_count': len(rows), 'total_units': sum(r['units'] for r in rows),
                         'revenue_ugx': sum(r['units'] * r['unit_price_ugx'] for r in rows),
                         'units_ge_5': sum(r['units'] >= 5 for r in rows),
                         'by_item_units_revenue_rows': {k: v for k, v in sorted(by_item.items())}},
           'sunrise_answer_key': key}
    write(ROOT / 'instructor_materials' / 'reference_values.json', json.dumps(ref, indent=2) + '\n')


# ------------------------------------------------------------------ sheets
def week_of(i):
    return (i - 1) // 3 + 1


def render_sheet(code, i, l, lessons):
    ident = f'{code}{i:02}'
    week = week_of(i)
    prereq = 'START_HERE.md. No subject knowledge is assumed.' if i == 1 else f'{code}{i - 1:02} {lessons[i - 2]["title"]}'
    lab = LAB_AFTER.get(i) if code == 'ML' else None
    parts = [f'# {ident} {l["title"]}', '',
             f'Week {week}, {WEEK_THEMES[code][week - 1]} | Session {i} of 24 | {TRACK_NAMES[code]}'
             + (f' | New library: {", ".join(l["libs"])}' if l.get('libs') else ''), '',
             f'**Today\'s question.** {l["question"]}', '',
             f'**Objective.** {l["objective"]}', '',
             f'Before this session: {prereq.rstrip(".")}. If you cannot explain the last example, use its error card with the instructor first.', '']
    if l['words']:
        parts += ['## Words for today', '',
                  md_table(['Word', 'What it means', 'Think of it like this'], [(w[0], w[1], w[2]) for w in l['words']]), '']
    for b, blk in zip('AB', l['blocks']):
        parts += [f'## Block {b}. {blk["idea"]}', '', blk['intro'], '', f'**Predict.** {blk["predict"]}' + ('' if 'paper' in blk['predict'].lower() else ' Write your guess on paper first.'), '']
        if blk.get('code'):
            parts += [code_block(blk['code']), '']
        parts += ['**Run it, then compare.** ' + blk['shows'], '', '**Investigate.**', '']
        parts += [f'{n}. {q}' for n, (q, _a) in enumerate(blk['investigate'], 1)]
        parts += ['', f'**Modify.** {blk["modify"]["instruction"]}', '']
    mk = l['make']
    parts += ['## Make', '', mk['task'], '',
              f'Save your work as {ident}. Keep the worked example and put your own attempt below it. Write two sentences: what you changed and how you checked it.', '']
    parts += ['## Error card', '', md_table(['You see', 'It means', 'Fix'], l['errors']), '',
              '## Exit ticket', '', l['exit_ticket'], '',
              f'AI use follows AI_USE_POLICY.md. In weeks 1 to 6 no AI-generated solutions are used for exercises, labs or assessments. '
              f'Practise for 20 to 30 minutes between classes by repeating the Make task with one value changed. If you are stuck for 30 minutes, '
              f'save the error and bring it to class. A file saved on your laptop has not been submitted until you use the route in START_HERE.md.']
    if lab:
        parts += ['', f'After this session: foundation lab {lab} on the fourth day of the week.']
    return '\n'.join(parts) + '\n'


def cell(kind, text):
    d = {'cell_type': kind, 'metadata': {}, 'source': text.splitlines(keepends=True)}
    if kind == 'code':
        d.update(execution_count=None, outputs=[])
    return d


def notebook_from_cells(ident, cells):
    for j, c in enumerate(cells):
        c['id'] = f'{ident.lower()}-{j}'
    return json.dumps({'cells': cells, 'metadata': {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
                                                      'language_info': {'name': 'python'}}, 'nbformat': 4, 'nbformat_minor': 5}, indent=2) + '\n'


def render_notebook(code, i, l):
    ident = f'{code}{i:02}'
    head = f'# {ident} {l["title"]}\n\n**Today\'s question.** {l["question"]}\n\n**Objective.** {l["objective"]}\n'
    if l['words']:
        head += '\n## Words for today\n\n' + md_table(['Word', 'What it means', 'Think of it like this'], [(w[0], w[1], w[2]) for w in l['words']]) + '\n'
    cells = [cell('markdown', head)]
    for b, blk in zip('AB', l['blocks']):
        cells.append(cell('markdown', f'## Block {b}. {blk["idea"]}\n\n{blk["intro"]}\n\n**Predict.** {blk["predict"]} Write your guess in the cell below before you run anything.'))
        cells.append(cell('markdown', 'My prediction:\n'))
        if blk.get('code'):
            cells.append(cell('code', blk['code'].rstrip('\n') + '\n'))
        cells.append(cell('markdown', '**Run it, then compare.** ' + blk['shows'] + '\n\n**Investigate.**\n\n' + '\n'.join(f'{n}. {q}' for n, (q, _a) in enumerate(blk['investigate'], 1))))
        cells.append(cell('markdown', f'**Modify.** {blk["modify"]["instruction"]}'))
        cells.append(cell('code', '# Your Modify code here\n'))
    cells.append(cell('markdown', '## Make\n\n' + l['make']['task']))
    cells.append(cell('code', '# Your Make code here\n'))
    cells.append(cell('markdown', '## Error card\n\n' + md_table(['You see', 'It means', 'Fix'], l['errors']) + '\n\n## Exit ticket\n\n' + l['exit_ticket']))
    cells.append(cell('markdown', '## My explanation\n\nWhat I changed:\n\nHow I checked it:\n\nOne question or limitation:\n'))
    return notebook_from_cells(ident, cells)


def render_guide(code, i, l, lessons):
    ident = f'{code}{i:02}'
    table, total = clock_table(l)
    assert total == 180, (ident, total)
    parts = [f'# {ident} Instructor guide: {l["title"]}', '',
             'Private. Keep this file out of the student folder.', '',
             f'**Objective.** {l["objective"]}', '', f'**Question of the day.** {l["question"]}', '',
             f'Prerequisite: ' + ('START_HERE.md' if i == 1 else f"{code}{i - 1:02} {lessons[i - 2]['title']}") + '.', '',
             '## The 180 minutes', '', table, '']
    if l.get('time_note'):
        parts += [f'Where it overruns: {l["time_note"]}', '']
    for b, blk in zip('AB', l['blocks']):
        parts += [f'## Block {b}. {blk["idea"]}', '', blk['intro'], '',
                  f'Ask for the prediction first: {blk["predict"]}', '']
        if blk.get('code'):
            parts += [code_block(blk['code']), '']
        parts += [f'Correct result: {blk["shows"]}', '', 'Investigate, with answers:', '']
        parts += [f'- {q} Answer: {a}' for q, a in blk['investigate']]
        mod = blk['modify']
        parts += ['', f'Modify: {mod["instruction"]} Answer: {mod["answer"]}']
        if mod.get('code'):
            parts += ['', code_block(mod['code'])]
        parts += ['']
    mk = l['make']
    parts += ['## Make: reference', '']
    parts += [code_block(mk['reference']) if mk.get('reference_is_code') else mk['reference'], '']
    parts += [f'Evidence to collect: {mk["evidence"]}', '', '## Misconceptions to listen for', '']
    parts += [f'- {m}' for m in l['misconceptions']]
    parts += ['', '## Questions to ask, with expected answers', '']
    parts += [f'- {q} Expected: {a}' for q, a in l['questions']]
    parts += ['', '## Evidence and feedback', '',
              'Record complete, needs repair or absent for each of the five learners, with one concrete repair action. '
              'Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; '
              'explanations and live demonstrations need your judgement and are not auto-graded.']
    return '\n'.join(parts) + '\n'


# ------------------------------------------------------------------ track-level documents
def glossary(code, lessons):
    seen = {}
    rows = []
    for i, l in enumerate(lessons, 1):
        for w in l['words']:
            k = w[0].strip().lower()
            if k in seen:
                raise ValueError(f'{code}: term "{w[0]}" defined in session {seen[k]} and again in session {i}')
            seen[k] = i
            rows.append((w[0], w[1], w[2], f'{code}{i:02}'))
    rows.sort(key=lambda r: r[0].lower())
    text = (f'# {TRACK_NAMES[code]}: glossary\n\nEvery word in the course, with the session where it first appears. '
            f'This list is generated from the "Words for today" cards, so a word cannot be taught without reaching this handout.\n\n'
            + md_table(['Word', 'What it means', 'Think of it like this', 'Session'], rows) + '\n')
    errs = []
    for i, l in enumerate(lessons, 1):
        for e in l['errors']:
            errs.append((e[0], e[1], e[2], f'{code}{i:02}'))
    err_text = (f'# {TRACK_NAMES[code]}: class error glossary\n\nStart list, one row per error card. Students add the errors they meet.\n\n'
                + md_table(['You see', 'It means', 'Fix', 'Session'], errs) + '\n')
    return text, err_text, len(rows)


def curriculum(code, lessons):
    out = [f'# {TRACK_NAMES[code]}: curriculum\n',
           'Eight weeks, three core sessions a week, 24 core sessions, each proposed at three hours including a 15-minute break. '
           + ('Four two-hour foundation labs (F01 to F04) sit on a fourth day in weeks 1 to 4, and an optional extension follows session 24. '
              if code == 'ML' else '')
           + 'Audience: S.4 to S.6 students and school leavers. No programming, spreadsheet or statistics experience is assumed. '
             'Confirm session length and dates before advertising hour totals.\n']
    for w in range(8):
        out.append(f'\n## Week {w + 1}. {WEEK_THEMES[code][w]}\n')
        out.append(f'Product of the week: {WEEKLY_PRODUCT[code][w]}.\n')
        for i in range(w * 3 + 1, w * 3 + 4):
            l = lessons[i - 1]
            out.append(f'### Session {i}. {l["title"]}\n')
            out.append(f'Question: {l["question"]}\n')
            out.append(f'{l["objective"]}\n')
            if l.get('libs'):
                out.append(f'New library: {", ".join(l["libs"])}.\n')
            if l['words']:
                out.append('Words: ' + ', '.join(x[0] for x in l['words']) + '.\n')
            out.append(f'Evidence: {l["make"]["evidence"]}\n')
            if code == 'ML' and i in LAB_AFTER:
                lab = LABS[list(LAB_AFTER).index(i)]
                out.append(f'Then lab {LAB_AFTER[i]}, {lab["title"]}.\n')
    return '\n'.join(out)


def class_plan(code, lessons):
    out = [f'# {TRACK_NAMES[code]}: eight-week plan\n',
           'Relative plan. Exact dates and holiday breaks are not confirmed. Core sessions propose 180 minutes including a 15-minute break'
           + ('; each ML lab proposes 120 minutes including a 10-minute break. Insert each lab after that week\'s third core session.\n' if code == 'ML' else '.\n'),
           'Two 45 to 60 minute practice blocks on non-class days are the starting allowance. The repeat-and-change task in each session is part of these blocks, not extra homework. Weeks 1 to 6 portfolios carry the existing 20% weight; checkpoints and the project keep their own weights.\n',
           f'Default clock for every session unless its guide says otherwise: ' + '; '.join(f'{m} minutes {label.lower()}' for label, m in DEFAULT_CLOCK) + '.\n']
    for w in range(8):
        a = w * 3 + 1
        out.append(f'\n## Week {w + 1}. {WEEK_THEMES[code][w]}: sessions {a:02} to {a + 2:02}\n')
        out.append(f'Product of the week: {WEEKLY_PRODUCT[code][w]}.\n')
        out.append(f'Practice between classes: {PRACTICE[code][w]}\n')
        if code == 'ML' and w < 4:
            out.append(f'Lab: {LABS[w]["after"]} then F0{w + 1}, {LABS[w]["title"]}.\n')
        for i in range(a, a + 3):
            l = lessons[i - 1]
            out.append(f'### {code}{i:02}. {l["title"]}\n')
            out.append(f'{l["objective"]}\n')
            out.append(f'Exercise and evidence: {l["make"]["task"]}\n')
    out.append('\n## Supporting material and delivery gates\n')
    out.append('Data: see data/DATA_DICTIONARY.md and data/sunrise/DATA_DICTIONARY.md. Policies in handbook/: AI_USE_POLICY.md, ASSESSMENT_AND_SHOWCASE.md, PROJECT_RUBRIC.md. '
               'Run programme/preflight_stack.py on every laptop before day one. Pilot a Python foundations session and a pandas session with a beginner first. '
               'No school submission platform or automatic end-to-end marking is deployed by this pack.\n')
    return '\n'.join(out)


# ------------------------------------------------------------------ labs and extension
def build_labs():
    seq = ['# Machine Learning foundation labs\n',
           'Four two-hour guided labs, one on a fourth teaching day in each of weeks 1 to 4. They are guided practice, not extra homework. '
           'Each lab follows its week\'s third core session and precedes the next week. Keep two 45 to 60 minute practice blocks on non-class days.\n']
    for i, lab in enumerate(LABS, 1):
        name = f'F{i:02}'
        intro = f'# {name} {lab["title"]}\n\nWeek {i}, fourth teaching day. Complete {lab["after"]} first.\n\n**Today\'s question.** {lab["question"]}\n\n'
        words = ('## Words for today\n\n' + md_table(['Word', 'What it means', 'Think of it like this'], [(w[0], w[1], w[2]) for w in lab['words']]) + '\n\n') if lab['words'] else ''
        body = (intro + words + f'## Learn the idea\n\n{lab["explain"]}\n\n## Start on paper\n\n{lab["hand"]}\n\n## Worked example\n\n```python\n{lab["code"].rstrip(chr(10))}\n```\n\n'
                f'Run it, then compare: {lab["output"]}\n\n## Your turn\n\n{lab["task"]}\n\nRun all cells from the top, save, close and reopen. Show the instructor your output and explanation.\n')
        sd = ROOT / 'student_materials' / 'ML'
        write(sd / f'{name}.md', body)
        cells = [cell('markdown', intro + words + lab['explain'] + '\n\n' + lab['hand']), cell('code', lab['code'].rstrip('\n') + '\n'),
                 cell('markdown', 'Run it, then compare: ' + lab['output'] + '\n\n## Your turn\n' + lab['task']), cell('code', '# Your code here\n')]
        write(sd / f'{name}.ipynb', notebook_from_cells(name, cells))
        write(ROOT / 'instructor_materials' / 'ML' / f'{name}_guide.md',
              body + f'\n## Tutor pacing\n\n10 minutes recall; 20 minutes paper example; 20 minutes run the code slowly together; 10 minutes break; 30 minutes learner variation; '
                     f'20 minutes individual explanation and repair; 10 minutes save and exit check. Total 120. Visit all five learners and ask what each symbol and unit means before asking them to change it.\n\n'
                     f'Reference: {lab["answer"]}\n\nRepair: {lab["repair"]}\n\nRecord complete, needs repair or absent. Carry unfinished repair into the next core session. Lab evidence goes in that week\'s portfolio with no second mark.\n')
        seq.append(f'## Week {i}: {lab["after"]}, then {name}\n\n{lab["title"]}. Output: {name}.ipynb with a worked result, an individual variation and a plain-language explanation.\n')
    seq.append('## Readiness before ML13\n\nEach learner explains a variable, indexes a list and an array, reads a row/column table, calculates a mean and a proportion, and works one weighted sum with units. '
               'Check individually. Use a repair example if a skill is missing. Attendance is not understanding.\n')
    text = '\n'.join(seq)
    write(CURRICULUM / 'FOUNDATION_LABS.md', text)
    write(ROOT / 'student_materials' / 'ML' / 'FOUNDATION_LABS.md', text)


def build_extension():
    e = EXTENSION
    sd = ROOT / 'student_materials' / 'ML'
    md = (f'# ML25 {e["title"]}\n\nOptional extension after session 24. Not assessed, no extra class, no extra install.\n\n{e["intro"]}\n\n'
          f'```python\n{e["code"].rstrip(chr(10))}\n```\n\n{e["honest_note"]}\n')
    write(sd / 'ML25_Extension.md', md)
    write(sd / 'ML25_Extension.ipynb', notebook_from_cells('ml25', [cell('markdown', f'# ML25 {e["title"]}\n\n{e["intro"]}'), cell('code', e['code'].rstrip('\n') + '\n'), cell('markdown', e['honest_note'])]))
    write(ROOT / 'instructor_materials' / 'ML' / 'ML25_keras_demo_instructor.py',
          '"""Instructor laptop only. Not in the student pack and not run by the verifier.\n' + e['requirements_note'] + '\n"""\n' + e['instructor_keras_demo'].rstrip('\n') + '\n')


# ------------------------------------------------------------------ main
def build():
    rows = build_data()
    reference_values(rows)
    for code, lessons, files in (('DA', DA, DATA_DA), ('ML', ML, DATA_ML)):
        sd = ROOT / 'student_materials' / code
        td = ROOT / 'instructor_materials' / code
        sd.mkdir(parents=True, exist_ok=True)
        td.mkdir(parents=True, exist_ok=True)
        for f in files:
            if f.startswith('sunrise_'):
                src = SUNRISE_DIR / {v: k for k, v in SUNRISE_FILES.items()}[f]
            else:
                src = ROOT / 'data' / f
            shutil.copy2(src, sd / f)
        dd = (ROOT / 'data' / 'DATA_DICTIONARY.md').read_text()
        marker = '## Sunrise Shops (Python for Data Analysis)'
        if code == 'ML':
            dd = dd[:dd.index(marker)].rstrip('\n') + '\n'
        else:
            dd = dd.replace('(sunrise/DATA_DICTIONARY.md)', '(SUNRISE_DATA_DICTIONARY.md)')
            shutil.copy2(SUNRISE_DIR / 'DATA_DICTIONARY.md', sd / 'SUNRISE_DATA_DICTIONARY.md')
        write(sd / 'DATA_DICTIONARY.md', dd)
        for i, l in enumerate(lessons, 1):
            ident = f'{code}{i:02}'
            write(sd / f'{ident}.md', render_sheet(code, i, l, lessons))
            write(sd / f'{ident}.ipynb', render_notebook(code, i, l))
            write(td / f'{ident}_guide.md', render_guide(code, i, l, lessons))
        g, eg, n_terms = glossary(code, lessons)
        write(CURRICULUM / f'GLOSSARY_{code}.md', g)
        write(sd / 'GLOSSARY.md', g)
        write(sd / 'ERROR_GLOSSARY.md', eg)
        write(CURRICULUM / f'CURRICULUM_{code}.md', curriculum(code, lessons))
        write(CURRICULUM / f'CLASS_PLAN_{code}.md', class_plan(code, lessons))
        print(code, '24 sheets, 24 notebooks, 24 guides,', n_terms, 'glossary terms')
    build_labs()
    build_extension()
    write(ROOT / 'instructor_materials' / 'ml18_reference.py', '''from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
X, y = load_iris(return_X_y=True)
X_dev, X_test, y_dev, y_test = train_test_split(X, y, test_size=.2, random_state=7, stratify=y)
X_train, X_val, y_train, y_val = train_test_split(X_dev, y_dev, test_size=.25, random_state=7, stratify=y_dev)
assert (len(X_train), len(X_val), len(X_test)) == (90, 30, 30)
baseline = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
print("Validation baseline", accuracy_score(y_val, baseline.predict(X_val)))
models = [DecisionTreeClassifier(max_depth=d, random_state=7).fit(X_train, y_train) for d in [1, 3]]
scores = [accuracy_score(y_val, m.predict(X_val)) for m in models]
chosen = max(range(len(models)), key=lambda i: scores[i])
print("Validation scores", scores, "Chosen depth", [1, 3][chosen])
print("Final test accuracy", accuracy_score(y_test, models[chosen].predict(X_test)))
print(confusion_matrix(y_test, models[chosen].predict(X_test)))
''')
    print('Built camp pack, revision 2.')


if __name__ == '__main__':
    build()
