#!/usr/bin/env python3
"""Build 'Company Profile.pdf' (one A4 page, KLAi branded) for Nile Valley Foods Ltd (fictional)."""
from pathlib import Path

from reportlab.lib.colors import Color, HexColor, black, white
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Table, TableStyle

HERE = Path(__file__).resolve().parent
BUILD = HERE.parent
EDITION = HERE.parents[2]
OUT = EDITION / "03 Learner Materials" / "Practice Files" / "01 Case Company" / "Company Profile.pdf"
FONTS = BUILD / "brand" / "fonts"
LOGO = BUILD / "brand" / "logos" / "klai_logo_on_black_cropped.png"

for name, f in (("Lato", "Lato-Regular.ttf"), ("Lato-Bold", "Lato-Bold.ttf"),
                ("Lato-Italic", "Lato-Italic.ttf"), ("Lato-Black", "Lato-Black.ttf")):
    pdfmetrics.registerFont(TTFont(name, str(FONTS / f)))
pdfmetrics.registerFontFamily("Lato", normal="Lato", bold="Lato-Bold", italic="Lato-Italic", boldItalic="Lato-Bold")

RED = HexColor("#AE2525")
GREY = Color(0.35, 0.35, 0.35)
HAIR = Color(0.72, 0.72, 0.72)
W, H = A4
M = 18 * mm

body = ParagraphStyle("body", fontName="Lato", fontSize=9.6, leading=13.2, textColor=black)
small = ParagraphStyle("small", parent=body, fontSize=8.6, leading=11.4)
cell = ParagraphStyle("cell", parent=body, fontSize=8.6, leading=11)
cellb = ParagraphStyle("cellb", parent=cell, fontName="Lato-Bold")
head = ParagraphStyle("head", fontName="Lato-Bold", fontSize=11.5, leading=14, textColor=black)
th = ParagraphStyle("th", parent=cell, fontName="Lato-Bold", textColor=white)


def draw(c):
    # black band with logo
    band = 31 * mm
    c.setFillColor(black)
    c.rect(0, H - band, W, band, stroke=0, fill=1)
    lh = 17 * mm
    lw = lh * 2310 / 736
    c.drawImage(str(LOGO), M, H - band + (band - lh) / 2, width=lw, height=lh, mask=None)
    c.setFillColor(white)
    c.setFont("Lato", 9)
    c.drawRightString(W - M, H - band / 2 - 3, "Applied AI and Automation for Executives")

    y = H - band - 13 * mm
    c.setFillColor(black)
    c.setFont("Lato-Black", 22)
    c.drawString(M, y, "Company Profile")
    c.setFont("Lato-Bold", 13)
    c.drawString(M, y - 7.5 * mm, "Nile Valley Foods Ltd (NVF)")
    c.setFillColor(RED)
    c.setFont("Lato-Bold", 9)
    c.drawRightString(W - M, y, "FICTIONAL TEACHING COMPANY")
    c.setFillColor(GREY)
    c.setFont("Lato", 9)
    c.drawRightString(W - M, y - 5 * mm, "Used for examples and practice in this course")
    c.setStrokeColor(HAIR)
    c.setLineWidth(0.5)
    c.line(M, y - 11 * mm, W - M, y - 11 * mm)
    return y - 15 * mm


def main():
    from reportlab.pdfgen import canvas
    c = canvas.Canvas(str(OUT), pagesize=A4)
    c.setTitle("Company Profile: Nile Valley Foods Ltd (fictional)")
    c.setAuthor("KLAi Professional Learning")
    top = draw(c)
    cw = W - 2 * M

    def put(flow, y, width=cw, x=M):
        w, h = flow.wrap(width, 1000)
        flow.drawOn(c, x, y - h)
        return y - h

    y = top
    y = put(Paragraph(
        "Nile Valley Foods Ltd is a food distributor in Jinja, Uganda, founded in 2014. It has about 85 staff. "
        "It distributes maize flour, cooking oil, rice, sugar and beans to about 320 shops and 14 supermarkets "
        "across Eastern Uganda, from depots in Jinja and Mbale. It runs 9 trucks.", body), y)
    y -= 5 * mm

    # facts table
    facts = [
        ("Founded", "2014"), ("Head office", "Jinja"), ("Depots", "Jinja and Mbale"),
        ("Staff", "About 85"), ("Customers", "About 320 shops and 14 supermarkets"), ("Fleet", "9 trucks"),
        ("Products", "Maize flour, cooking oil, rice, sugar, beans"),
        ("Sales regions", "Jinja, Mbale, Iganga, Tororo, Soroti, Kamuli"),
    ]
    data = []
    for i in range(0, len(facts), 2):
        a, b = facts[i], facts[i + 1]
        data.append([Paragraph(a[0], cellb), Paragraph(a[1], cell), Paragraph(b[0], cellb), Paragraph(b[1], cell)])
    t = Table(data, colWidths=[24 * mm, 56 * mm, 26 * mm, cw - 106 * mm])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEABOVE", (0, 0), (-1, 0), 0.5, black),
                           ("LINEBELOW", (0, 0), (-1, -1), 0.4, HAIR), ("TOPPADDING", (0, 0), (-1, -1), 3),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 3), ("LEFTPADDING", (0, 0), (-1, -1), 2)]))
    y = put(Paragraph("At a glance", head), y)
    y -= 2 * mm
    w, h = t.wrap(cw, 1000)
    t.drawOn(c, M, y - h)
    y -= h + 6 * mm

    # departments and systems
    y = put(Paragraph("Departments, leaders and systems", head), y)
    y -= 2 * mm
    dep = [
        ("Management", "Sarah Namukasa, Managing Director", "Google Workspace (Gmail, Sheets, Drive)"),
        ("Sales", "Peter Okello, Sales Manager", "WhatsApp Business for orders, order sheet in Google Sheets"),
        ("Finance", "Joseph Mugisha, Finance Manager", "Accounting package, MTN MoMo, Airtel Money, Sheets"),
        ("Operations", "Grace Akello, Operations Manager", "Gmail, Sheets, delivery schedules, supplier contracts in Drive"),
        ("Warehouse and dispatch", "Ibrahim Ssemwogerere, Warehouse Supervisor", "Stock and delivery sheets, delivery notes"),
        ("Customer Service", "David Kato, Customer Service Lead", "WhatsApp Business, Gmail"),
        ("Human Resources", "Mary Nabirye, HR Officer", "Gmail, Drive"),
    ]
    rows = [[Paragraph("Department", th), Paragraph("Leader", th), Paragraph("Main systems", th)]]
    for d in dep:
        rows.append([Paragraph(d[0], cellb), Paragraph(d[1], cell), Paragraph(d[2], cell)])
    t = Table(rows, colWidths=[36 * mm, 56 * mm, cw - 92 * mm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), black), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("LINEBELOW", (0, 1), (-1, -1), 0.4, HAIR), ("TOPPADDING", (0, 0), (-1, -1), 3),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 3), ("LEFTPADDING", (0, 0), (-1, -1), 4)]))
    w, h = t.wrap(cw, 1000)
    t.drawOn(c, M, y - h)
    y -= h + 6 * mm

    # suppliers
    y = put(Paragraph("Main suppliers", head), y)
    y -= 2 * mm
    sup = [
        ("Busoga Oils Ltd", "Cooking oil"), ("Elgon Millers Ltd", "Maize flour"),
        ("Tororo Rice Growers Cooperative", "Rice"), ("Lakeside Logistics Ltd", "Transport"),
        ("Pearl Packaging Ltd", "Packaging"),
    ]
    rows = [[Paragraph("Supplier", th), Paragraph("Supplies", th)]]
    for s in sup:
        rows.append([Paragraph(s[0], cellb), Paragraph(s[1], cell)])
    t = Table(rows, colWidths=[70 * mm, 40 * mm], hAlign="LEFT")
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), black), ("LINEBELOW", (0, 1), (-1, -1), 0.4, HAIR),
                           ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
                           ("LEFTPADDING", (0, 0), (-1, -1), 4)]))
    w, h = t.wrap(cw, 1000)
    t.drawOn(c, M, y - h)
    # how the company works, right of the supplier table
    note = Paragraph(
        "<b>How work flows.</b> Shops order on WhatsApp Business. Staff copy each order into a Google Sheet. "
        "The depot loads and dispatches, drivers or boda riders deliver, and customers pay by MTN MoMo, "
        "Airtel Money or cash. Finance records payments and pays suppliers from the accounting package.", small)
    nx = M + 116 * mm
    nw, nh = note.wrap(cw - 116 * mm, 1000)
    note.drawOn(c, nx, y - nh)
    y -= max(h, nh) + 8 * mm

    # fictional statement
    c.setStrokeColor(black)
    c.setLineWidth(0.6)
    c.line(M, y, W - M, y)
    y -= 4 * mm
    y = put(Paragraph(
        "<b>All content in this course is fictional.</b> Nile Valley Foods Ltd, its people, suppliers, customers, "
        "figures and documents are invented for teaching. Any resemblance to a real person or firm is accidental.",
        ParagraphStyle("f", parent=body, textColor=RED, fontSize=9.4)), y)

    # footer
    c.setFillColor(GREY)
    c.setFont("Lato", 8)
    c.drawString(M, 12 * mm, "KLAi Professional Learning, Kampala")
    c.drawRightString(W - M, 12 * mm, "Applied AI and Automation, Executive Edition. Fictional case company.")
    c.showPage()
    c.save()
    print("wrote", OUT.name)


if __name__ == "__main__":
    main()
