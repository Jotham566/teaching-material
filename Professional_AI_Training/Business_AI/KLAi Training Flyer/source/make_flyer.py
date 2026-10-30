"""KLAi training flyer: A4 print PDF, 1080x1080 post and 1080x1920 status.   python3 make_flyer.py
Edit flyer_config.json (course lines, hours, contact details) and run again.
Brand: black and white, red #AE2525 and gold #E0BE36 from the KLAi logo. Lato throughout."""
import json, subprocess, sys
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, Color
from PIL import Image

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
CFG = json.load(open(HERE / 'flyer_config.json', encoding='utf-8'))
FD = Path('/usr/share/fonts/truetype/lato')
for n in ('Black', 'Bold', 'Semibold', 'Regular', 'Light', 'Medium'):
    pdfmetrics.registerFont(TTFont(f'Lato-{n}', str(FD / f'Lato-{n}.ttf')))

BLACK, WHITE = HexColor('#000000'), HexColor('#FFFFFF')
RED, GOLD = HexColor('#AE2525'), HexColor('#E0BE36')
BODY, SOFT, RULE = HexColor('#2B2B2B'), HexColor('#6A6A6A'), HexColor('#D8D6D2')
WHITE80 = Color(1, 1, 1, alpha=0.82)
LOGO_LIGHT, LOGO_DARK = HERE / 'logo_light.png', HERE / 'logo_dark.png'
LR = Image.open(LOGO_DARK).size; LOGO_AR = LR[0] / LR[1]

CHAR = HexColor('#1F2328')
THEMES = {
 'dark':  dict(hdr=BLACK, htxt=WHITE, hsub=WHITE80, logo_dark=True, foot=BLACK, cap=True, gold_rule='below', sep=None),
 'light': dict(hdr=None, htxt=HexColor('#111111'), hsub=HexColor('#4A4A4A'), logo_dark=False, foot=CHAR, cap=True, gold_rule='top', sep=BLACK),
}
TH = THEMES['dark']

def sw(t, f, s): return pdfmetrics.stringWidth(t, f, s)
def wrap(t, f, s, w):
    out, cur = [], ''
    for word in t.split():
        trial = (cur + ' ' + word).strip()
        if sw(trial, f, s) <= w: cur = trial
        else: out.append(cur); cur = word
    if cur: out.append(cur)
    return out
def para(c, x, y, t, f, s, w, color, lead=1.28, align='l'):
    """draw wrapped text with its first baseline at y (y grows downward from page top); returns y after the block"""
    c.setFillColor(color); c.setFont(f, s)
    for ln in wrap(t, f, s, w):
        if align == 'r': c.drawRightString(x + w, y, ln)
        else: c.drawString(x, y, ln)
        y += s * lead
    return y
def logo(c, H, x, ytop, w, dark=None):
    dark = TH['logo_dark'] if dark is None else dark
    h = w / LOGO_AR
    c.drawImage(str(LOGO_DARK if dark else LOGO_LIGHT), x, H - ytop - h, w, h, mask=None)
    return h

def contact_lines():
    k = CFG['contact']; lines = []
    if k.get('whatsapp'): lines.append(('Call or WhatsApp', k['whatsapp']))
    if k.get('email'): lines.append(('Email', k['email']))
    if k.get('website'): lines.append(('Web', k['website']))
    return lines

def rows(c, H, x, y0, y1, w, s, ruled_first=True):
    """five course rows between y0 and y1 (top-down coordinates)"""
    n = len(CFG['courses']); rh = (y1 - y0) / n
    nw = w - 104 * s                    # text width, leaving room for the hours column
    for i, co in enumerate(CFG['courses']):
        top = y0 + i * rh
        c.setStrokeColor(RULE if i else BLACK); c.setLineWidth((0.6 if i else 1.4) * s); c.line(x, H - top, x + w, H - top)
        # measure the block and centre it in the row
        name_s, desc_s = 19 * s, 12.2 * s
        dl = wrap(co['line'], 'Lato-Regular', desc_s, nw)
        block = name_s * 1.1 + 5 * s + len(dl) * desc_s * 1.3
        yy = top + (rh - block) / 2 + name_s * 0.95
        c.setFillColor(BLACK); c.setFont('Lato-Black', name_s); c.drawString(x, H - yy, co['name'])
        para(c, x, H - 0 and 0, '', 'Lato-Regular', 1, 1, BLACK)   # no-op keeps helper imports honest
        yy2 = yy + 6 * s + desc_s
        c.setFillColor(BODY); c.setFont('Lato-Regular', desc_s)
        for ln in dl: c.drawString(x, H - yy2, ln); yy2 += desc_s * 1.3
        # hours column
        big, small = co['big'], co['small']
        cx = x + w
        c.setFillColor(RED); c.setFont('Lato-Black', 30 * s); c.drawRightString(cx, H - (top + rh / 2 - 5 * s), big)
        c.setFillColor(SOFT); c.setFont('Lato-Medium', 10.5 * s)
        for j, part in enumerate(small.split('\n')): c.drawRightString(cx, H - (top + rh / 2 - 5 * s + (15 + 13 * j) * s), part)
    c.setStrokeColor(BLACK); c.setLineWidth(1.4 * s); c.line(x, H - y1, x + w, H - y1)
    c.setFillColor(SOFT); c.setFont('Lato-Regular', 10.5 * s); c.drawString(x, H - (y1 + 17 * s), CFG['schedule_note'])

def cta(c, H, x, y0, w, h, s, maxw=None, color=WHITE):
    maxw = maxw or w
    lines = contact_lines()
    c.setFillColor(color); c.setFont('Lato-Black', 22 * s)
    c.drawString(x, H - (y0 + 28 * s), CFG['cta'])
    yy = y0 + 28 * s + 25 * s
    if lines:
        xx = x
        for k, v in lines:
            kw = sw(k, 'Lato-Medium', 11 * s) + 6 * s; iw = kw + sw(v, 'Lato-Bold', 13.5 * s)
            if xx > x and xx + iw > x + maxw: xx = x; yy += 21 * s
            c.setFont('Lato-Medium', 11 * s); c.setFillColor(GOLD); c.drawString(xx, H - yy, k)
            c.setFont('Lato-Bold', 13.5 * s); c.setFillColor(color); c.drawString(xx + kw, H - yy, v)
            xx += iw + 26 * s
    else:
        c.setFont('Lato-Regular', 13 * s); c.setFillColor(color); c.drawString(x, H - yy, CFG['cta_fallback'])
    k = CFG['contact']
    extra = ' · '.join(v for v in (k.get('next_start'), k.get('venue')) if v)
    if extra:
        c.setFont('Lato-Regular', 11.5 * s); c.setFillColor(WHITE80); c.drawString(x, H - (yy + 22 * s), extra)

def qr(c, H, xr, ytop, size, s):
    """white square QR with a caption underneath; xr is the right edge"""
    c.setFillColor(WHITE); c.rect(xr - size, H - ytop - size, size, size, stroke=0, fill=1)
    c.drawImage(str(HERE / 'qr_whatsapp.png'), xr - size, H - ytop - size, size, size)
    c.setFillColor(WHITE80); c.setFont('Lato-Medium', 9.5 * s); c.drawRightString(xr, H - (ytop + size + 13 * s), 'Scan to chat on WhatsApp')

def stack(c, W, H):
    s = W / 595.0; M = 42 * s
    c.setFillColor(WHITE); c.rect(0, 0, W, H, stroke=0, fill=1)
    tall = H / W > 1.6
    Hb = (330 if not tall else 700) * s if not tall else 760 * s * 0.0 + 0
    Hb = 330 * s if not tall else 430 * s
    if TH['hdr'] is not None: c.setFillColor(TH['hdr']); c.rect(0, H - Hb, W, Hb, stroke=0, fill=1)
    if TH['gold_rule'] == 'top': c.setFillColor(GOLD); c.rect(0, H - 7 * s, W, 7 * s, stroke=0, fill=1)
    lw = (140 if TH['hdr'] is not None else 170) * s; lh = logo(c, H, M - 4 * s, (34 if TH['hdr'] is not None else 46) * s, lw)
    c.setFillColor(TH['hsub']); c.setFont('Lato-Medium', 11 * s); c.drawRightString(W - M, H - (34 * s + lh * 0.62), CFG['org'])
    y = (34 if TH['hdr'] is not None else 46) * s + lh + ((50 if not tall else 62) + (0 if TH['hdr'] is not None else 26)) * s
    hs = (40 if not tall else 46) * s
    c.setFillColor(TH['htxt']); c.setFont('Lato-Black', hs)
    for ln in wrap(CFG['headline'], 'Lato-Black', hs, W - 2 * M):
        c.drawString(M, H - y, ln); y += hs * 1.08
    y += 10 * s
    y = para(c, M, H - y, CFG['sub'], 'Lato-Light', 15 * s, W - 2 * M - 40 * s, WHITE, lead=1.38) if False else y
    c.setFillColor(TH['hsub']); c.setFont('Lato-Light' if TH['hdr'] is not None else 'Lato-Regular', 15 * s)
    for ln in wrap(CFG['sub'], 'Lato-Light', 15 * s, W - 2 * M - 30 * s):
        c.drawString(M, H - y, ln); y += 15 * s * 1.4
    # audience line pinned to the bottom of the black block
    ay = Hb - 30 * s
    c.setFont('Lato-Bold', 12.5 * s); xx = M
    for i, t in enumerate(CFG['audience']):
        if i:
            c.setFillColor(GOLD); c.circle(xx + 9 * s, H - (ay - 4.2 * s), 2.4 * s, stroke=0, fill=1); xx += 22 * s
        c.setFillColor(TH['htxt']); c.drawString(xx, H - ay, t); xx += sw(t, 'Lato-Bold', 12.5 * s)
    if TH['gold_rule'] == 'below': c.setFillColor(GOLD); c.rect(0, H - Hb - 4 * s, W, 4 * s, stroke=0, fill=1)
    Hf = (112 if not tall else 130) * s
    rows(c, H, M, Hb + 22 * s, H - Hf - 40 * s, W - 2 * M, s)
    c.setFillColor(TH['foot']); c.rect(0, 0, W, Hf, stroke=0, fill=1)
    qs = (74 if not tall else 90) * s
    cta(c, H, M, H - Hf + 14 * s, W - 2 * M, Hf, s, maxw=W - 2 * M - qs - 24 * s)
    qr(c, H, W - M, H - Hf + (Hf - qs - 18 * s) / 2, qs, s)

def side(c, W, H):
    s = W / 1080.0 * 1.75                 # same visual scale as the A4 layout at 595 wide
    c.setFillColor(WHITE); c.rect(0, 0, W, H, stroke=0, fill=1)
    Lw = W * 0.385; Hf = 150 * (W / 1080)
    if TH['hdr'] is not None: c.setFillColor(TH['hdr']); c.rect(0, H - (H - Hf), Lw, H - Hf, stroke=0, fill=1)
    if TH['gold_rule'] == 'top': c.setFillColor(GOLD); c.rect(0, H - 7 * (W / 1080), W, 7 * (W / 1080), stroke=0, fill=1)
    M = 52 * (W / 1080)
    lw = Lw - 2 * M - 70 * (W / 1080); lh = logo(c, H, M, M, lw)
    hs = 47 * (W / 1080)
    y = M + lh + 118 * (W / 1080)
    c.setFillColor(TH['htxt']); c.setFont('Lato-Black', hs)
    for ln in wrap(CFG['headline'], 'Lato-Black', hs, Lw - 2 * M):
        c.drawString(M, H - y, ln); y += hs * 1.08
    y += 14 * (W / 1080)
    ss = 17.5 * (W / 1080); c.setFillColor(TH['hsub']); c.setFont('Lato-Light' if TH['hdr'] is not None else 'Lato-Regular', ss)
    for ln in wrap(CFG['sub'], 'Lato-Light', ss, Lw - 2 * M):
        c.drawString(M, H - y, ln); y += ss * 1.42
    # audience, one per line, at the bottom of the panel
    ay = H - Hf - 56 * (W / 1080) - (len(CFG['audience']) - 1) * 30 * (W / 1080)
    c.setFont('Lato-Bold', 17 * (W / 1080))
    for t in CFG['audience']:
        c.setFillColor(GOLD); c.circle(M + 4 * (W / 1080), H - (ay - 5.5 * (W / 1080)), 3.4 * (W / 1080), stroke=0, fill=1)
        c.setFillColor(TH['htxt']); c.drawString(M + 20 * (W / 1080), H - ay, t); ay += 30 * (W / 1080)
    if TH['sep'] is not None: c.setStrokeColor(RULE); c.setLineWidth(1); c.line(Lw, H - 7 * (W / 1080), Lw, Hf)
    else: c.setFillColor(GOLD); c.rect(Lw, Hf, 4 * (W / 1080), H - Hf, stroke=0, fill=1)
    k = W / 1080 * 1.0
    x0 = Lw + 52 * k; wr = W - x0 - 52 * k
    rows(c, H, x0, 52 * k, H - Hf - 62 * k, wr, 1.45 * k)
    c.setFillColor(TH['foot']); c.rect(0, 0, W, Hf, stroke=0, fill=1)
    qs = 98 * k
    cta(c, H, M, H - Hf + 18 * k, W - 2 * M, Hf, 1.58 * k, maxw=W - 2 * M - qs - 40 * k)
    qr(c, H, W - M, H - Hf + (Hf - qs - 22 * k) / 2, qs, 1.58 * k)

def render(name, W, H, fn, raster_to=None):
    pdf = OUT / f'{name}.pdf'
    c = canvas.Canvas(str(pdf), pagesize=(W, H)); c.setTitle(CFG['title']); c.setAuthor(CFG['org']); fn(c, W, H); c.showPage(); c.save()
    return pdf
def to_png(pdf, dest, px_w):
    tmp = str(dest.with_suffix('')) + '_tmp'
    subprocess.run(['pdftoppm', '-r', '216', '-png', '-singlefile', str(pdf), tmp], check=True)
    im = Image.open(tmp + '.png').convert('RGB'); h = round(im.size[1] * px_w / im.size[0]); im.resize((px_w, h), Image.LANCZOS).save(dest, optimize=True)
    Path(tmp + '.png').unlink()

if __name__ == '__main__':
    theme = sys.argv[1] if len(sys.argv) > 1 else 'dark'
    TH = THEMES[theme]; tag = '' if theme == 'dark' else ' (light)'
    a4 = render(f'KLAi Training Flyer{tag} (A4)', 595.28, 841.89, stack)
    sq = render('_square', 1080, 1080, side)
    st = render('_status', 1080, 1920, stack)
    to_png(sq, OUT / f'KLAi Training Flyer{tag} (square 1080x1080).png', 1080)
    to_png(st, OUT / f'KLAi Training Flyer{tag} (status 1080x1920).png', 1080)
    to_png(a4, OUT / f'KLAi Training Flyer{tag} (A4 preview).png', 1240)
    for p in (sq, st): p.unlink()
    print('written', theme)
