"""Study calendar for one learner (A4 PDF + editable Word), KLAi branded.

Run from build/:
  python3 make_calendar.py --track ML --start 2026-12-03 --days tue,thu,sat --physical sat --lab-day fri \
      --holidays 2026-12-25:Christmas Day,2026-12-26:Boxing Day,2027-01-01:New Year's Day --showcase 2027-01-30 \
      --out ../student_calendars

Rules: core sessions fall on the class days in order, skipping the holidays. The first class and every class on the physical
weekday are in person (3 hours, 2:00 to 5:00 pm); the other classes are online (90 minutes, 2:00 to 3:30 pm). ML labs (F01 to F04)
go on the first lab-day after their session, move to the next free weekday when it is a holiday, and are online (2 hours).
If --showcase is later than the natural date of session 24, session 24 is pinned to it (in person) and its natural date
is shown as an optional catch-up and rehearsal slot. Needs node with the docx package and LibreOffice (soffice) for the PDF.
"""
import argparse, datetime as dt, json, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CAMP = HERE.parent
sys.path.insert(0, str(HERE))
from lessons import da, ml  # noqa: E402
import common  # noqa: E402

WD = {'mon': 0, 'tue': 1, 'wed': 2, 'thu': 3, 'fri': 4, 'sat': 5, 'sun': 6}
BUILD = {
    'ML': ['a computer that guesses the rent of a home', 'a price calculator that knows numbers from text', 'a calculator that tells you where you slipped',
           'a flower-sorting rule that you write by hand', 'a loop that reads a whole price list', 'a function that checks its own answers',
           'your first table: open a shop sales file', 'a revenue column that you calculate yourself', 'a summary card: typical, spread and chance',
           'a clean dataset with a log of every change', 'three charts that tell the story of the sales', 'a mini report and your own project question',
           'a plain-guess baseline your model must beat', 'a line that predicts a rent', 'a full prediction experiment, start to finish',
           'a decision tree that sorts flowers', 'a fair comparison that spots overfitting', 'your model against data it has never seen',
           'your project plan and your data', 'your project baseline', 'your best model, explained in plain words',
           'your finished project, ready to share', 'a three-minute talk about what you built', 'showcase day: you show your family what you made'],
    'DA': ['your first table, opened and read in a notebook', 'a note that shows the type of every value', 'a revenue calculator that explains its errors',
           'a rule that treats big orders differently', 'a loop that totals a whole week of sales', 'a function that checks its own answers',
           'a real table loaded from a CSV file', 'a revenue column, filtered to the sales you ask for', 'a summary of the best seller and the typical sale',
           'a clean table with a log of every fix', 'two charts that make one clear point', 'a first report: a table, a chart and honest sentences',
           'a NumPy check that agrees with pandas', 'a chart that shows how sales are spread', 'a heatmap, and an honest answer about rain',
           'a cleaned export you can rerun next month', 'a merged table with its row count checked', 'a total that matches the true total',
           'your project question and plan', 'a reliable analysis, checked two ways', 'a chart report people can read alone',
           'a report and a handover folder', 'a three-minute talk about what you built', 'showcase day: you show your family what you made'],
}
LAB_BUILD = ['a warm-up: guess what Python prints, then check', 'a first tour of NumPy arrays', 'quick maths for data: spread and chance', 'the weighted sum behind a prediction']
THEMES = {
    'DA': ['Meet the data', 'Python you need', 'Tables in pandas', 'Clean and chart', 'Explore with NumPy and seaborn', 'Messy data and two tables', 'Show it', 'Hand over'],
    'ML': ['Python and a first prediction', 'Python you need', 'Tables and statistics', 'Clean, chart, question', 'Baselines and a line', 'Trees and fair comparisons', 'Your project', 'Hand over'],
}
NAMES = {'ML': 'Machine Learning', 'DA': 'Python for Data Analysis'}
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
LONG = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
DAYN = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


def _t(s):
    h, m = [int(x) for x in s.split(':')]
    return h, m


def time_text(rng):
    """'14:00-17:00' -> '2:00 to 5:00 pm'; '09:00-12:00' -> '9:00 am to 12:00 noon'; '10:00-11:30' -> '10:00 to 11:30 am'."""
    a, b = [_t(x) for x in rng.split('-')]
    def one(h, m, meridiem=True):
        suffix = 'noon' if (h, m) == (12, 0) else ('pm' if h >= 12 else 'am')
        hh = h if h <= 12 else h - 12
        return f'{hh}:{m:02d}', suffix
    (ta, sa), (tb, sb) = one(*a), one(*b)
    if sa == sb or (sb == 'noon' and sa == 'am' and False):
        return f'{ta} to {tb} {sb}'
    return f'{ta} {sa} to {tb} {sb}'


def long_date(d):
    return f'{DAYN[d.weekday()]} {d.day} {LONG[d.month - 1]}'


def join_list(xs):
    return xs[0] if len(xs) == 1 else ', '.join(xs[:-1]) + ' and ' + xs[-1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--track', required=True, choices=['ML', 'DA'])
    ap.add_argument('--start', required=True)
    ap.add_argument('--days', default='tue,thu,sat')
    ap.add_argument('--physical', default='sat')
    ap.add_argument('--lab-day', default='fri')
    ap.add_argument('--holidays', default='')
    ap.add_argument('--showcase', default='')
    ap.add_argument('--in-time', default='14:00-17:00', help='in-person class, 24-hour HH:MM-HH:MM')
    ap.add_argument('--on-time', default='14:00-15:30', help='online class')
    ap.add_argument('--lab-time', default='14:00-16:00', help='online lab (ML)')
    ap.add_argument('--out', default=str(CAMP / 'student_calendars'))
    ap.add_argument('--name', default='')
    a = ap.parse_args()
    track = a.track
    start = dt.date.fromisoformat(a.start)
    days = [WD[x.strip()] for x in a.days.split(',')]
    phys_wd = WD[a.physical]
    hol = {}
    for x in [h for h in a.holidays.split(',') if h]:
        d, n = x.split(':', 1)
        hol[dt.date.fromisoformat(d)] = n
    lessons = ml.ML if track == 'ML' else da.DA
    core, d = [], start
    while len(core) < 24:
        if d.weekday() in days and d not in hol:
            core.append(d)
        d += dt.timedelta(1)
    spare = None
    if a.showcase:
        sc = dt.date.fromisoformat(a.showcase)
        if sc > core[-1]:
            spare = core[-1]  # the natural date of the last session becomes a catch-up and rehearsal slot
            core[-1] = sc
    rows = []
    for i, (d, l) in enumerate(zip(core, lessons), 1):
        phys = d.weekday() == phys_wd or d == start or i == 24
        rows.append(dict(date=d.isoformat(), kind='core', code=f'{track}{i:02d}', title=l['title'], build=BUILD[track][i - 1], where='person' if phys else 'online',
                         time=a.in_time if phys else a.on_time, timeText=time_text(a.in_time if phys else a.on_time)))
    if spare:
        rows.append(dict(date=spare.isoformat(), kind='spare', code='', title='Catch-up and showcase rehearsal (optional)', build='', where='online', time=a.on_time, timeText=time_text(a.on_time)))
    moved = []
    if track == 'ML':
        for k, lab in enumerate(ml.LABS):
            n = int(lab['after'][2:])
            d = core[n - 1] + dt.timedelta(1)
            while d.weekday() != WD[a.lab_day]:
                d += dt.timedelta(1)
            orig = d
            while d in hol or d.weekday() > 4:
                d += dt.timedelta(1)
            if d != orig:
                moved.append((orig, d))
            rows.append(dict(date=d.isoformat(), kind='lab', code=f'F{k + 1:02d}', title=lab['title'], build=LAB_BUILD[k], where='online', time=a.lab_time, timeText=time_text(a.lab_time)))
    rows.sort(key=lambda r: (r['date'], r['kind'] != 'core'))
    # weeks
    weeks = []
    for w in range(8):
        weeks.append(dict(theme=THEMES[track][w], badge=common.BADGES[track][w], codes=[f'{track}{3 * w + j:02d}' for j in (1, 2, 3)] + ([f'F{w + 1:02d}'] if track == 'ML' and w < 4 else [])))
    end = core[-1]
    hol_in = sorted(h for h in hol if start <= h <= end + dt.timedelta(7))
    hol_text = join_list([f'{DAYN[h.weekday()]} {h.day} {LONG[h.month - 1]}' for h in hol_in])
    moved_text = ''
    if moved:
        moved_text = (f' The online lab' + ('s that fall' if len(moved) > 1 else ' that falls') + ' on ' + join_list([f'{m[0].day} {LONG[m[0].month - 1]}' for m in moved]) +
                      ' move' + ('' if len(moved) > 1 else 's') + ' to ' + join_list([long_date(m[1]) for m in moved]) + '.')
    cfg = dict(track=track, trackName=NAMES[track], learner=a.name, start=long_date(start) + f' {start.year}', end=long_date(end) + f' {end.year}',
               endIs='parent showcase' if i == 24 else 'last class', weeks=weeks, rows=rows, hasLabs=track == 'ML', startIso=start.isoformat(),
               holidayText=hol_text, movedText=moved_text, physicalName=DAYN[phys_wd], logo=str(CAMP / 'brand' / 'logos' / 'klai_logo_on_black_cropped.png'),
               lastClassText=long_date(end), hasSpare=bool(spare), inTime=time_text(a.in_time), onTime=time_text(a.on_time), labTime=time_text(a.lab_time),
               holidayHits=any(h.weekday() in days or (track == 'ML' and h.weekday() == WD[a.lab_day]) for h in hol_in))
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    stem = f'KLAi_{track}_Study_Calendar_from_{start.day}_{MONTHS[start.month - 1]}_{start.year}' + (f'_{a.name.replace(" ", "_")}' if a.name else '')
    import tempfile
    cfgp = Path(tempfile.mkdtemp()) / 'calendar.json'
    cfgp.write_text(json.dumps(cfg, indent=1))
    (out / 'data').mkdir(exist_ok=True)
    (out / 'data' / f'{stem}.json').write_text(json.dumps(dict(track=track, learner=a.name, rows=rows), indent=1))
    docx = out / f'{stem}.docx'
    r = subprocess.run(['node', str(HERE / 'calendar_docx.js'), str(cfgp), str(docx)], capture_output=True, text=True)
    print(r.stdout.strip(), r.stderr.strip()[:400])
    subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', str(out), str(docx)], capture_output=True)
    print('wrote', docx.name, 'and PDF; ends', end.isoformat())
    for r_ in rows:
        print(r_['date'], dt.date.fromisoformat(r_['date']).strftime('%a'), r_['where'][:3], r_['code'], r_['title'][:45])


if __name__ == '__main__':
    main()
