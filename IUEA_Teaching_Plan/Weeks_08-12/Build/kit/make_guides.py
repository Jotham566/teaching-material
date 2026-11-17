"""Lecturer guide for each class (one Word file and PDF per class, all three cohorts). python3 kit/make_guides.py [1 2 3 4]

Built from the class files so the guide's slide numbers, numbers and clocks always match the decks and notebooks."""
import importlib.util
import subprocess
import tempfile
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUILD = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(BUILD / 'templates_gen'))
sys.path.insert(0, str(BUILD / 'content'))
import deck  # noqa: E402
import common as C  # noqa: E402
import lo_fonts  # noqa: E402
from docx_kit import *  # noqa: E402,F401,F403

OUT = BUILD.parent / 'Lecturer Guides'
W = CONTENT_CM
CODES = ['CML3112', 'CML3113', 'CML3111']


def bullets(d, items, size=10, after=2):
    for it in items:
        p = para(d, '', size, after=after)
        p.paragraph_format.left_indent = Cm(0.5)
        p.paragraph_format.first_line_indent = Cm(-0.4)
        add_run(p, '•  ', size, True)
        if isinstance(it, tuple):
            add_run(p, it[0] + ' ', size, True)
            add_run(p, it[1], size)
        else:
            add_run(p, it, size)


def clock_rows(s):
    t, rows = 0, []
    for m, lab in s['clock']:
        rows.append([f'{t // 60}:{t % 60:02d}', str(m), lab])
        t += m
    return rows


def main(argv):
    nums = [int(a) for a in argv if a.isdigit()] or [n for n in (1, 2, 3, 4) if (BUILD / 'content' / f'c{n}.py').exists()]
    for n in nums:
        spec = importlib.util.spec_from_file_location(f'c{n}', BUILD / 'content' / f'c{n}.py')
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        S = {c: m.build(c) for c in CODES}
        s = S['CML3112']
        fa = s['facilitator']
        specs = {c: deck.build_spec(S[c]) for c in CODES}
        titles = [x['title']['text'] if x.get('title') else (x.get('title_raw') or '') for x in specs['CML3112']['slides']]
        titles = [t.replace('\n', ' ') for t in titles]
        d = new_doc(f'Lecturer Guide, Class {n}', 'IUEA Machine Learning for Engineers')
        title(d, f'Class {n}, Week {s["week"]}: {s["title"]}', 'Lecturer guide for CML3112, CML3113 and CML3111. Keep it private.')
        h2(d, 'The class in one paragraph', 0)
        para(d, s['question'], 10.5, italic=True, after=4)
        para(d, s['cover_note'], 10, after=6)
        h2(d, 'When each cohort meets')
        grid(d, [[c, C.COHORTS[c]['name'].split('|')[1].strip(), C.COHORTS[c]['dates'][n], C.COHORTS[c]['slot'] + ', ' + C.COHORTS[c]['room']] for c in CODES], [2.2, 7.0, 4.4, 3.8],
             header=['Cohort', 'Programmes', 'Date', 'Time and room'], size=9)
        if fa.get('prep'):
            h2(d, 'Before the class')
            bullets(d, fa['prep'])
        h2(d, 'The clock')
        para(d, 'Tuesday cohort (CML3112): the first full teaching of this class. Friday cohorts (CML3113, CML3111): ' + s.get('friday_note', 'the concepts were taught last Friday, so the deck is used as a recap.'), 10, after=4)
        for c, label in (('CML3112', 'CML3112, Tuesday'), ('CML3113', 'CML3113 and CML3111, Friday')):
            para(d, label, 10, True, before=4, after=2, keep=True)
            grid(d, clock_rows(S[c]), [2.0, 2.0, 13.4], header=['Starts', 'Minutes', 'What happens'], size=9, label_cols=(0,))
        h2(d, 'Slide map')
        para(d, 'The deck has two halves. Slides up to the divider are concepts: no laptops. After the divider come the lab slides and the notebook. You switch once. The titles below are from the CML3112 deck. The other two decks have the same slides in the same order; where a title carries a number, their own number replaces it (see the per-cohort table).', 10, after=3)
        rows, sec = [], 'Concepts'
        short = []
        for i, t in enumerate(titles, 1):
            if t.startswith('Part 2'):
                sec = 'Lab'
            rec = 'recap' if any(k.lower() in t.lower() for k in fa.get('recap_path', [])) else ''
            rows.append([str(i), t, sec, rec])
        grid(d, rows, [1.2, 11.2, 2.2, 2.8], header=['Slide', 'Title', 'Part', 'Friday recap'], size=8.5, label_cols=(0,))
        if fa.get('recap_path'):
            para(d, 'Friday recap: show the slides marked "recap" and pass quickly over the others in one sentence each. The learners met the ideas last Friday; the aim is to refresh them with the pictures before the lab.', 9.5, italic=True, before=3, after=4)
        if fa.get('probes'):
            h2(d, 'Questions to ask, and a good answer')
            grid(d, [[q, a] for q, a in fa['probes']], [7.0, 10.4], header=['Ask', 'A good answer'], size=9, label_cols=())
        if fa.get('misconceptions'):
            h2(d, 'Ideas learners often get wrong')
            grid(d, [[a, b] for a, b in fa['misconceptions']], [7.0, 10.4], header=['What a learner may say', 'What to say back'], size=9, label_cols=())
        if fa.get('lab_steps'):
            h2(d, 'Walking the lab')
            grid(d, [[a, b] for a, b in fa['lab_steps']], [4.4, 13.0], header=['Step', 'What to look for'], size=9)
        if hasattr(m, 'numbers'):
            h2(d, 'The numbers each cohort should see')
            F = {c: C.facts(c) for c in CODES}
            grid(d, m.numbers(F), [6.0, 3.8, 3.8, 3.8], header=['Check'] + [f'{c} ({F[c]["unit"]})' for c in CODES], size=9, label_cols=(0,))
        if fa.get('rescue'):
            h2(d, 'If things go wrong')
            bullets(d, fa['rescue'])
        if fa.get('after'):
            h2(d, 'After the class')
            bullets(d, fa['after'])
        h2(d, 'Speaker script')
        para(d, 'Every slide carries its spoken script in the PowerPoint notes (open Presenter View). The scripts are first person and are meant to be read or paraphrased. Pauses are marked by questions.', 10, after=4)
        path = OUT / f'Class{n}_Week{s["week"]}_Lecturer_Guide.docx'
        save(d, path)
        lo = '-env:UserInstallation=file://' + str(Path(tempfile.gettempdir()) / 'iuea_second_half_lo')
        lo_fonts.seed(lo)
        subprocess.run(['soffice', lo, '--headless', '--convert-to', 'pdf', '--outdir', str(OUT), str(path)], capture_output=True)


if __name__ == '__main__':
    main(sys.argv[1:])
