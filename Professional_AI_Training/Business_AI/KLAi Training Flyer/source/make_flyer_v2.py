"""KLAi training flyer, version 2.   python3 make_flyer_v2.py [dark|light|both]
Larger type for phones, an audience line per course, hours as a quiet detail, a tutor strip.
Edit flyer_config_v2.json and run again."""
import json, sys, subprocess
from pathlib import Path
from reportlab.pdfgen import canvas
import make_flyer as F
from make_flyer import (sw, wrap, GOLD, RED, BLACK, WHITE, WHITE80, RULE, SOFT, BODY, CHAR, HexColor, HERE, OUT, THEMES, to_png, Image)

CFG = json.load(open(HERE / 'flyer_config_v2.json', encoding='utf-8'))
F.CFG = CFG                                   # contact_lines() and cta() read this
INK = HexColor('#111111'); MUTE = HexColor('#555555')
PORTRAIT = HERE / 'portrait_circle.png'

MODES = {
 'a4':     dict(W=595.28, H=841.89, M=40, hdr_h=232, logo_w=118, logo_y=30, head=29.5, head_y=112, sub=13.2, sub_lines=2, gap_sub=8,
                rows_y0=250, row_h=74, name=18.5, who=11, desc=12.6, hrsw=96, big=14.5, small=10.8, note=10, tut_h=98, photo=62, tut_name=14, tut_lab=9.5, tut_txt=10.4, tut_key='tutor_long',
                foot_h=100, s=1.0, qs=72, sub_key='sub'),
 'square': dict(W=1080, H=1080, M=44, hdr_h=262, logo_w=150, logo_y=34, head=52, head_y=150, sub=25, sub_lines=1, gap_sub=14,
                rows_y0=296, row_h=94, name=38, who=22, desc=0, hrsw=214, big=29, small=22, note=20, tut_h=100, photo=72, tut_name=27, tut_lab=18, tut_txt=21, tut_key='tutor_short',
                foot_h=146, s=1.5, qs=96, sub_key='sub_short'),
 'status': dict(W=1080, H=1920, M=70, hdr_h=540, logo_w=250, logo_y=64, head=78, head_y=250, sub=30, sub_lines=3, gap_sub=18,
                rows_y0=556, row_h=172, name=44, who=27, desc=25, hrsw=200, big=34, small=27, note=24, tut_h=176, photo=112, tut_name=34, tut_lab=22, tut_txt=25, tut_key='tutor_mid',
                foot_h=236, s=1.9, qs=134, sub_key='sub'),
}

def draw(c, mode, theme):
    K = MODES[mode]; W, H, M = K['W'], K['H'], K['M']; TH = THEMES[theme]; F.TH = TH
    dark = TH['hdr'] is not None
    c.setFillColor(WHITE); c.rect(0, 0, W, H, stroke=0, fill=1)
    if dark: c.setFillColor(TH['hdr']); c.rect(0, H - K['hdr_h'], W, K['hdr_h'], stroke=0, fill=1)
    else: c.setFillColor(GOLD); c.rect(0, H - 0.012 * W, W, 0.012 * W, stroke=0, fill=1)
    lw = K['logo_w'] * (1 if dark else 1.2)
    lh = F.logo(c, H, M - 3, K['logo_y'] if dark else K['logo_y'] + 12, lw)
    c.setFillColor(TH['hsub']); c.setFont('Lato-Medium', K['sub'] * 0.8)
    c.drawRightString(W - M, H - (K['logo_y'] + lh * 0.6 + (0 if dark else 12)), CFG['org'])
    # headline
    hs = K['head']; y = K['head_y'] if dark else K['head_y'] + 26
    c.setFillColor(TH['htxt']); c.setFont('Lato-Black', hs)
    for ln in wrap(CFG['headline'], 'Lato-Black', hs, W - 2 * M):
        c.drawString(M, H - y, ln); y += hs * 1.08
    y += K['gap_sub'] + K['sub']
    sub = CFG[K['sub_key']]; c.setFillColor(TH['hsub']); c.setFont('Lato-Regular', K['sub'])
    for ln in wrap(sub, 'Lato-Regular', K['sub'], W - 2 * M)[:K['sub_lines']]:
        c.drawString(M, H - y, ln); y += K['sub'] * 1.38
    if dark: c.setFillColor(GOLD); c.rect(0, H - K['hdr_h'] - 0.007 * W, W, 0.007 * W, stroke=0, fill=1)

    # rows
    n = len(CFG['courses']); y0 = K['rows_y0']; rh = K['row_h']; nw = W - 2 * M - K['hrsw']
    for i, co in enumerate(CFG['courses']):
        top = y0 + i * rh
        c.setStrokeColor(INK if i == 0 else RULE); c.setLineWidth((1.6 if i == 0 else 0.8) * K['s']); c.line(M, H - top, W - M, H - top)
        dl = wrap(co['line'], 'Lato-Regular', K['desc'], nw) if K['desc'] else []
        block = K['name'] * 1.1 + 5 * K['s'] + K['who'] * 1.2 + (6 * K['s'] + len(dl) * K['desc'] * 1.28 if dl else 0)
        yy = top + (rh - block) / 2 + K['name'] * 0.88
        c.setFillColor(INK); c.setFont('Lato-Black', K['name']); c.drawString(M, H - yy, co['name'])
        yy += 5 * K['s'] + K['who'] * 1.05
        c.setFillColor(RED); c.setFont('Lato-Bold', K['who']); c.drawString(M, H - yy, co['who'])
        if dl:
            yy += 6 * K['s'] + K['desc'] * 0.95; c.setFillColor(BODY); c.setFont('Lato-Regular', K['desc'])
            for ln in dl: c.drawString(M, H - yy, ln); yy += K['desc'] * 1.28
        mid = top + rh / 2
        c.setFillColor(INK); c.setFont('Lato-Bold', K['big']); c.drawRightString(W - M, H - (mid - 1 * K['s']), co['hours'])
        c.setFillColor(MUTE); c.setFont('Lato-Medium', K['small']); c.drawRightString(W - M, H - (mid + K['small'] + 3 * K['s']), co['sessions'])
    yb = y0 + n * rh
    c.setStrokeColor(INK); c.setLineWidth(1.6 * K['s']); c.line(M, H - yb, W - M, H - yb)
    c.setFillColor(MUTE); c.setFont('Lato-Regular', K['note']); c.drawString(M, H - (yb + K['note'] + 7 * K['s']), CFG['schedule_note'])

    # tutor strip
    ty = yb + K['note'] + 7 * K['s'] + 14 * K['s']
    if mode == 'status': ty += 8
    th = K['tut_h']; ph = K['photo']
    c.drawImage(str(PORTRAIT), M, H - (ty + (th - ph) / 2 + ph), ph, ph, mask='auto')
    tx = M + ph + 18 * K['s']; tw = W - M - tx
    yy = ty + (th - (K['tut_lab'] + K['tut_name'] + 8 * K['s'] + 3 * K['tut_txt'] * 1.3)) / 2 + K['tut_lab']
    tl = wrap(CFG[K['tut_key']], 'Lato-Regular', K['tut_txt'], tw)
    total = K['tut_lab'] * 1.5 + K['tut_name'] * 1.3 + len(tl) * K['tut_txt'] * 1.3
    yy = ty + (th - total) / 2 + K['tut_lab']
    c.setFillColor(RED); c.setFont('Lato-Bold', K['tut_lab']); c.drawString(tx, H - yy, CFG['tutor_label'])
    yy += K['tut_name'] * 1.2
    c.setFillColor(INK); c.setFont('Lato-Black', K['tut_name']); c.drawString(tx, H - yy, CFG['tutor_name'])
    yy += K['tut_txt'] * 1.45; c.setFillColor(BODY); c.setFont('Lato-Regular', K['tut_txt'])
    for ln in tl: c.drawString(tx, H - yy, ln); yy += K['tut_txt'] * 1.3

    # footer
    fh = K['foot_h']; c.setFillColor(TH['foot']); c.rect(0, 0, W, fh, stroke=0, fill=1)
    qs = K['qs']
    F.cta(c, H, M, H - fh + 12 * K['s'], W - 2 * M, fh, K['s'], maxw=W - 2 * M - qs - 24 * K['s'])
    F.qr(c, H, W - M, H - fh + (fh - qs - 18 * K['s']) / 2, qs, K['s'] * 0.95)

def render(name, mode, theme):
    K = MODES[mode]; pdf = OUT / f'{name}.pdf'
    c = canvas.Canvas(str(pdf), pagesize=(K['W'], K['H'])); c.setTitle(CFG['title']); c.setAuthor(CFG['org']); draw(c, mode, theme); c.showPage(); c.save()
    return pdf

if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'both'
    for theme in (['dark', 'light'] if which == 'both' else [which]):
        tag = 'black' if theme == 'dark' else 'light'
        a4 = render(f'KLAi Flyer v2 {tag} (A4)', 'a4', theme)
        sq = render('_sq', 'square', theme); st = render('_st', 'status', theme)
        to_png(sq, OUT / f'KLAi Flyer v2 {tag} (square 1080x1080).png', 1080)
        to_png(st, OUT / f'KLAi Flyer v2 {tag} (status 1080x1920).png', 1080)
        to_png(a4, OUT / f'KLAi Flyer v2 {tag} (A4 preview).png', 1240)
        for p in (sq, st): p.unlink()
        print('written', tag)
