"""KLAi training flyer v3: adds when and where, fees, certificate, in-house option and LinkedIn.   python3 make_flyer_v3.py [dark|light|both]
Flow layout: every block is measured, and the script says how many points a layout overflows."""
import json, sys
from pathlib import Path
from reportlab.pdfgen import canvas
import make_flyer as F
from make_flyer import sw, wrap, GOLD, RED, BLACK, WHITE, WHITE80, RULE, BODY, HexColor, HERE, OUT, THEMES, to_png
CFG = json.load(open(HERE / 'flyer_config_v3.json', encoding='utf-8')); F.CFG = CFG
INK, MUTE = HexColor('#111111'), HexColor('#555555'); PORTRAIT = HERE / 'portrait_circle.png'

MODES = {
 'a4': dict(W=595.28, H=841.89, M=38, s=0.95, logo_w=108, logo_y=26, head=28, sub=12.4, sub_key='sub', gap=13,
   row_h=65, name=17.5, who=10.6, desc=12, hrsw=90, big=14, small=10.4, leave=11.2, leave_key='leave_line',
   fact_t=9.6, fact_x=10.2, fact_key='long', tut_h=74, photo=54, tut_name=13, tut_lab=9, tut_txt=9.8, tut_key='tutor_long', foot_h=112, qs=70, cap=8.6, pad=14),
 'square': dict(W=1080, H=1080, M=44, s=1.5, logo_w=118, logo_y=30, head=44, sub=23, sub_key='sub_short', gap=10,
   row_h=80, name=34, who=20, desc=0, hrsw=190, big=27, small=20, leave=21, leave_key='leave_line_short',
   fact_t=17, fact_x=20.5, fact_key='short', tut_h=84, photo=64, tut_name=24, tut_lab=15, tut_txt=18.5, tut_key='tutor_short', foot_h=146, qs=92, cap=14, pad=24),
 'status': dict(W=1080, H=1920, M=70, s=1.9, logo_w=210, logo_y=56, head=68, sub=27, sub_key='sub', gap=16,
   row_h=156, name=42, who=25, desc=24.5, hrsw=200, big=32, small=25, leave=27, leave_key='leave_line',
   fact_t=23, fact_x=25, fact_key='short', tut_h=146, photo=100, tut_name=32, tut_lab=21, tut_txt=24, tut_key='tutor_mid', foot_h=236, qs=134, cap=19, pad=26),
}
def draw(c, mode, theme):
    K = MODES[mode]; W, H, M, s = K['W'], K['H'], K['M'], K['s']; TH = THEMES[theme]; F.TH = TH; dark = TH['hdr'] is not None
    c.setFillColor(WHITE); c.rect(0, 0, W, H, stroke=0, fill=1)
    # --- measure header
    lw = K['logo_w'] * (1 if dark else 1.15); lh = lw / F.LOGO_AR
    y = K['logo_y'] + lh + (K['head'] * 0.35 if dark else K['head'] * 0.5)
    hl = wrap(CFG['headline'], 'Lato-Black', K['head'], W - 2 * M)
    sl = wrap(CFG[K['sub_key']], 'Lato-Regular', K['sub'], W - 2 * M)[:3]
    y_head = y + K['head']; y_sub = y_head + K['head'] * 1.08 * (len(hl) - 1) + K['gap'] + K['sub']
    hdr_end = y_sub + K['sub'] * 1.38 * (len(sl) - 1) + K['pad']
    if dark: c.setFillColor(TH['hdr']); c.rect(0, H - hdr_end, W, hdr_end, stroke=0, fill=1); c.setFillColor(GOLD); c.rect(0, H - hdr_end - 0.007 * W, W, 0.007 * W, stroke=0, fill=1)
    else: c.setFillColor(GOLD); c.rect(0, H - 0.012 * W, W, 0.012 * W, stroke=0, fill=1)
    F.logo(c, H, M - 3, K['logo_y'] + (0 if dark else 8), lw)
    c.setFillColor(TH['hsub']); c.setFont('Lato-Medium', K['sub'] * 0.8); c.drawRightString(W - M, H - (K['logo_y'] + lh * 0.6 + (0 if dark else 8)), CFG['org'])
    off = 0 if dark else 8
    c.setFillColor(TH['htxt']); c.setFont('Lato-Black', K['head']); yy = y_head + off
    for ln in hl: c.drawString(M, H - yy, ln); yy += K['head'] * 1.08
    c.setFillColor(TH['hsub']); c.setFont('Lato-Regular', K['sub']); yy = y_sub + off
    for ln in sl: c.drawString(M, H - yy, ln); yy += K['sub'] * 1.38
    top = hdr_end + (K['pad'] if dark else K['pad'] + off)
    # --- rows
    rh = K['row_h']; nw = W - 2 * M - K['hrsw']
    for i, co in enumerate(CFG['courses']):
        t = top + i * rh
        c.setStrokeColor(INK if i == 0 else RULE); c.setLineWidth((1.6 if i == 0 else 0.8) * s); c.line(M, H - t, W - M, H - t)
        dl = wrap(co['line'], 'Lato-Regular', K['desc'], nw) if K['desc'] else []
        block = K['name'] * 1.1 + 4 * s + K['who'] * 1.2 + (5 * s + len(dl) * K['desc'] * 1.28 if dl else 0)
        yy = t + (rh - block) / 2 + K['name'] * 0.88
        c.setFillColor(INK); c.setFont('Lato-Black', K['name']); c.drawString(M, H - yy, co['name'])
        yy += 4 * s + K['who'] * 1.05; c.setFillColor(RED); c.setFont('Lato-Bold', K['who']); c.drawString(M, H - yy, co['who'])
        if dl:
            yy += 5 * s + K['desc'] * 0.95; c.setFillColor(BODY); c.setFont('Lato-Regular', K['desc'])
            for ln in dl: c.drawString(M, H - yy, ln); yy += K['desc'] * 1.28
        mid = t + rh / 2
        c.setFillColor(INK); c.setFont('Lato-Bold', K['big']); c.drawRightString(W - M, H - (mid - 1 * s), co['hours'])
        c.setFillColor(MUTE); c.setFont('Lato-Medium', K['small']); c.drawRightString(W - M, H - (mid + K['small'] + 3 * s), co['sessions'])
    yb = top + len(CFG['courses']) * rh
    c.setStrokeColor(INK); c.setLineWidth(1.6 * s); c.line(M, H - yb, W - M, H - yb)
    # --- leave line
    y = yb + K['leave'] + 8 * s
    c.setFillColor(INK); c.setFont('Lato-Bold', K['leave']); c.drawString(M, H - y, CFG[K['leave_key']])
    # --- facts
    y += 12 * s; cw = (W - 2 * M - 24 * s) / 2; fh = 0
    cols = CFG['facts'][K['fact_key']]
    for j, col in enumerate(cols):
        x = M + j * (cw + 24 * s); yy = y + K['fact_t'] + 2 * s
        c.setFillColor(RED); c.setFont('Lato-Bold', K['fact_t']); c.drawString(x, H - yy, col['title']); yy += K['fact_t'] * 0.35
        c.setFillColor(BODY); c.setFont('Lato-Regular', K['fact_x'])
        for ln in col['lines']:
            for sub in wrap(ln, 'Lato-Regular', K['fact_x'], cw):
                yy += K['fact_x'] * 1.3; c.drawString(x, H - yy, sub)
        fh = max(fh, yy - y)
    y += fh + 10 * s
    c.setStrokeColor(RULE); c.setLineWidth(0.8 * s); c.line(M, H - y, W - M, H - y)
    # --- tutor
    th, ph = K['tut_h'], K['photo']; ty = y + 6 * s
    c.drawImage(str(PORTRAIT), M, H - (ty + (th - ph) / 2 + ph), ph, ph, mask='auto')
    tx = M + ph + 14 * s; tw = W - M - tx
    tl = wrap(CFG[K['tut_key']], 'Lato-Regular', K['tut_txt'], tw)
    total = K['tut_lab'] * 1.4 + K['tut_name'] * 1.25 + len(tl) * K['tut_txt'] * 1.28
    yy = ty + max(0, (th - total) / 2) + K['tut_lab']
    c.setFillColor(RED); c.setFont('Lato-Bold', K['tut_lab']); c.drawString(tx, H - yy, CFG['tutor_label'] + '  ·  ' + CFG['contact']['linkedin_tutor'])
    yy += K['tut_name'] * 1.2; c.setFillColor(INK); c.setFont('Lato-Black', K['tut_name']); c.drawString(tx, H - yy, CFG['tutor_name'])
    yy += K['tut_txt'] * 1.4; c.setFillColor(BODY); c.setFont('Lato-Regular', K['tut_txt'])
    for ln in tl: c.drawString(tx, H - yy, ln); yy += K['tut_txt'] * 1.28
    tut_end = ty + th
    # --- footer
    fh_ = K['foot_h']; ft = H - fh_
    over = tut_end - ft + 4
    c.setFillColor(TH['foot']); c.rect(0, 0, W, fh_, stroke=0, fill=1)
    qs = K['qs']; k = CFG['contact']
    items = [('Call or WhatsApp', k['whatsapp']), ('Email', k['email']), ('KLAi on LinkedIn', k['linkedin_klai'])]
    c.setFillColor(WHITE); c.setFont('Lato-Black', 20 * s); c.drawString(M, H - (ft + 14 * s + 20 * s * 0.85), CFG['cta'])
    yy = ft + 14 * s + 20 * s + 14 * s; xx = M; maxw = W - 2 * M - qs - 20 * s
    for lab, v in items:
        kw = sw(lab, 'Lato-Medium', 10.5 * s) + 6 * s; iw = kw + sw(v, 'Lato-Bold', 12.5 * s)
        if xx > M and xx + iw > M + maxw: xx = M; yy += 19 * s
        c.setFont('Lato-Medium', 10.5 * s); c.setFillColor(GOLD); c.drawString(xx, H - yy, lab)
        c.setFont('Lato-Bold', 12.5 * s); c.setFillColor(WHITE); c.drawString(xx + kw, H - yy, v); xx += iw + 20 * s
    foot_text_end = yy + 8 * s
    if foot_text_end > H: over = max(over, foot_text_end - H)
    F.qr(c, H, W - M, ft + (fh_ - qs - 16 * s) / 2, qs, K['cap'] / 9.5)
    return over

def render(name, mode, theme):
    K = MODES[mode]; pdf = OUT / f'{name}.pdf'
    c = canvas.Canvas(str(pdf), pagesize=(K['W'], K['H'])); c.setTitle(CFG['title']); c.setAuthor(CFG['org']); over = draw(c, mode, theme); c.showPage(); c.save()
    return pdf, over
if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'both'
    for theme in (['dark', 'light'] if which == 'both' else [which]):
        tag = 'black' if theme == 'dark' else 'light'
        a4, o1 = render(f'KLAi Flyer v3 {tag} (A4)', 'a4', theme); sq, o2 = render('_sq', 'square', theme); st, o3 = render('_st', 'status', theme)
        to_png(sq, OUT / f'KLAi Flyer v3 {tag} (square 1080x1080).png', 1080); to_png(st, OUT / f'KLAi Flyer v3 {tag} (status 1080x1920).png', 1080); to_png(a4, OUT / f'KLAi Flyer v3 {tag} (A4 preview).png', 1240)
        for p in (sq, st): p.unlink()
        print(tag, 'overflow pts  a4 %.0f  square %.0f  status %.0f' % (o1, o2, o3))
