"""Master timetable: the ML and DA calendars and the evening professional trainings on one page, with a clash check.

Run from build/ after make_calendar.py has written student_calendars/data/*.json for both tracks:
  python3 make_master_timetable.py --pro "tue,wed,fri@17:00-23:00;mon@10:00-13:00" --holidays 2026-12-25,2026-12-26,2027-01-01,2027-01-26
Output: ../student_calendars/KLAi_Master_Timetable_Dec_2026_Jan_2027.pdf (instructor only). Exits with an error if two classes overlap, a class
runs into a professional training, or a class falls on a public holiday that is not a class day for that track.
"""
import argparse, datetime as dt, json, sys
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

CAMP = Path(__file__).resolve().parents[1]
for n, f in [('Lato', 'Lato-Regular.ttf'), ('LatoB', 'Lato-Bold.ttf'), ('LatoBlack', 'Lato-Black.ttf')]:
    pdfmetrics.registerFont(TTFont(n, str(CAMP / 'brand' / 'fonts' / f)))
INK = HexColor('#111111'); MUTE = HexColor('#666666'); HAIR = HexColor('#CFCFCF'); RED = HexColor('#AE2525'); GOLD = HexColor('#E0BE36')
WD = {'mon': 0, 'tue': 1, 'wed': 2, 'thu': 3, 'fri': 4, 'sat': 5, 'sun': 6}
DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def mins(s):
    h, m = s.split(':')
    return int(h) * 60 + int(m)


def short(s):
    h, m = [int(x) for x in s.split(':')]
    ap = 'pm' if h >= 12 else 'am'
    return f'{h if h <= 12 else h - 12}:{m:02d}{ap}' if m else f'{h if h <= 12 else h - 12}{ap}'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pro', default='mon,wed,fri@10:00-13:30;tue,wed,fri@17:00-23:00', help='professional trainings: days@HH:MM-HH:MM, separated by semicolons')
    ap.add_argument('--holidays', default='2026-12-25,2026-12-26,2027-01-01,2027-01-26')
    ap.add_argument('--teach-on', default='2027-01-26', help='public holidays the owner has decided to teach on')
    ap.add_argument('--gap', type=int, default=30, help='minimum minutes between two classes or before a training')
    ap.add_argument('--out', default=str(CAMP / 'student_calendars' / 'KLAi_Master_Timetable_Dec_2026_Jan_2027.pdf'))
    a = ap.parse_args()
    pro = []  # (weekday, start, end)
    for part in a.pro.split(';'):
        ds, rng = part.split('@')
        s_, e_ = rng.split('-')
        for dd in ds.split(','):
            pro.append((WD[dd.strip()], mins(s_), mins(e_)))
    hol = {dt.date.fromisoformat(x) for x in a.holidays.split(',') if x}
    teach_on = {dt.date.fromisoformat(x) for x in a.teach_on.split(',') if x}
    data = {}
    for f in sorted((CAMP / 'student_calendars' / 'data').glob('KLAi_*_Study_Calendar_*.json')):
        j = json.loads(f.read_text())
        data[j['track']] = j['rows']
    items = []  # (date, start, end, track, label, where)
    for track, rows in data.items():
        for r in rows:
            if r['kind'] == 'spare':
                continue
            s, e = r['time'].split('-')
            items.append((dt.date.fromisoformat(r['date']), mins(s), mins(e), track, r['code'], r['where']))
    items.sort()
    problems = []
    for i, x in enumerate(items):
        d, s, e, tr, code, wh = x
        if d in hol and d not in teach_on:
            problems.append(f'{d} {code}: class on a public holiday')
        for pw, ps, pe in pro:
            if d.weekday() == pw and s < pe + a.gap and e + a.gap > ps and not (d in hol and d not in teach_on):
                problems.append(f'{d} {code}: {short(str(s // 60) + ":" + str(s % 60).zfill(2))}-{short(str(e // 60) + ":" + str(e % 60).zfill(2))} is too close to the professional training')
        for y in items[i + 1:]:
            if y[0] != d:
                break
            if y[1] < e + a.gap and y[2] + a.gap > s:
                problems.append(f'{d} {code} and {y[4]} are less than {a.gap} minutes apart or overlap')
    W, H = landscape(A4)
    c = canvas.Canvas(a.out, pagesize=(W, H))
    c.setTitle('KLAi master timetable, December 2026 to January 2027')
    M = 28
    c.setFillColor(HexColor('#000000')); c.rect(0, H - 54, W, 54, stroke=0, fill=1)
    c.drawImage(str(CAMP / 'brand' / 'logos' / 'klai_logo_on_black_cropped.png'), M, H - 42, width=70, height=70 * 736 / 2310, mask='auto')
    c.setFillColor(white); c.setFont('LatoB', 15); c.drawRightString(W - M, H - 30, 'Master timetable: ML and Python for Data Analysis')
    c.setFillColor(GOLD); c.setFont('Lato', 9); c.drawRightString(W - M, H - 44, 'Instructor only. Classes, labs and evening professional trainings on one page.')
    y0 = H - 72
    legend = [(GOLD, 'ML'), (INK, 'DA'), (RED, 'Professional training (evening)'), (HAIR, 'Public holiday')]
    x = M
    c.setFont('Lato', 8.5)
    for col, lab in legend:
        c.setFillColor(col); c.rect(x, y0 - 8, 9, 9, stroke=0, fill=1); c.setFillColor(INK); c.drawString(x + 13, y0 - 6, lab)
        x += 24 + c.stringWidth(lab, 'Lato', 8.5) + 12
    c.setFillColor(MUTE); c.drawString(x + 10, y0 - 6, 'Gold or black bar on the left: in person. No bar fill: online.')
    first = min(i[0] for i in items); last = max(i[0] for i in items)
    mon = first - dt.timedelta(first.weekday())
    weeks = []
    d = mon
    while d <= last:
        weeks.append(d); d += dt.timedelta(7)
    top = y0 - 18
    colw = (W - 2 * M - 40) / 7
    hdr_h = 14
    rowh = (top - 30 - hdr_h) / len(weeks)
    c.setFont('LatoB', 8.5)
    for k, nm in enumerate(DAYS):
        c.setFillColor(MUTE); c.drawString(M + 40 + k * colw + 4, top - 10, nm)
    for wi, wm in enumerate(weeks):
        ytop = top - hdr_h - wi * rowh
        c.setStrokeColor(HAIR); c.setLineWidth(0.6); c.line(M, ytop, W - M, ytop)
        c.setFillColor(INK); c.setFont('LatoB', 8); c.drawString(M, ytop - 11, f'{wm.day} {MON[wm.month - 1]}')
        for k in range(7):
            day = wm + dt.timedelta(k)
            xx = M + 40 + k * colw
            c.setStrokeColor(HAIR); c.line(xx, ytop, xx, ytop - rowh)
            if day < first - dt.timedelta(0) and day < first:
                pass
            c.setFont('Lato', 7); c.setFillColor(MUTE); c.drawRightString(xx + colw - 3, ytop - 8, f'{day.day}')
            yy = ytop - 13
            if day in hol:
                lab_ = 'Holiday, class on' if day in teach_on else 'Public holiday'
                c.setFillColor(HAIR); c.rect(xx + 2, yy - 9, colw - 4, 11, stroke=0, fill=1); c.setFillColor(INK); c.setFont('LatoB', 7); c.drawString(xx + 5, yy - 6, lab_)
                yy -= 11
            for it in [i for i in items if i[0] == day]:
                _, s, e, tr, code, wh = it
                col = GOLD if tr == 'ML' else INK
                c.setFillColor(col)
                c.rect(xx + 2, yy - 9, 3, 11, stroke=0, fill=1 if wh == 'person' else 0)
                if wh != 'person':
                    c.setStrokeColor(col); c.setLineWidth(0.8); c.rect(xx + 2, yy - 9, 3, 11, stroke=1, fill=0)
                c.setFillColor(INK); c.setFont('LatoB', 7.2); c.drawString(xx + 8, yy - 6.5, f'{code}')
                c.setFont('Lato', 6.8); c.setFillColor(MUTE); c.drawString(xx + 8 + c.stringWidth(code, 'LatoB', 7.2) + 3, yy - 6.5, f'{short(str(s // 60) + ":" + str(s % 60).zfill(2))}-{short(str(e // 60) + ":" + str(e % 60).zfill(2))}')
                yy -= 10.5
            labs_ = []
            for pw, ps, pe in pro:
                if day.weekday() == pw and first <= day <= last and (day not in hol or day in teach_on):
                    f_ = lambda m_: short(str(m_ // 60) + ':' + str(m_ % 60).zfill(2))
                    labs_.append(f'{f_(ps)}+' if pe >= 22 * 60 else f'{f_(ps)}-{f_(pe)}')
            if labs_:
                c.setFillColor(RED); c.setFont('LatoB', 6.8)
                c.drawRightString(xx + colw - 4, ytop - rowh + 3, 'Pro ' + ' and '.join(labs_))
    c.setStrokeColor(HAIR); c.line(M, top - hdr_h - len(weeks) * rowh, W - M, top - hdr_h - len(weeks) * rowh)
    c.setFont('Lato', 8); c.setFillColor(MUTE)
    c.drawString(M, 14, 'Clash check: ' + ('no overlaps, no class within %d minutes of another or of a professional training, no class on a public holiday except 26 January, which is a planned class day.' % a.gap if not problems else 'PROBLEMS FOUND, see the terminal output.'))
    c.showPage(); c.save()
    print('wrote', a.out)
    for p in problems:
        print('CLASH:', p)
    sys.exit(1 if problems else 0)


if __name__ == '__main__':
    main()
