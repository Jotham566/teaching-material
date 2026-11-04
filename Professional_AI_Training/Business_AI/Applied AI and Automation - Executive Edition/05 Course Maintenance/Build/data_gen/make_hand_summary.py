#!/usr/bin/env python3
"""Regenerate the hand-made weekly summary (with two planted errors) and the Pearl Packaging quote.

Run:  python3 make_hand_summary.py      (after make_case_data.py, which writes weekly_sales.csv)
Writes:
  03 Learner Materials/Practice Files/03 Apps Script Build/last_month_summary_by_hand.csv
  04 Facilitator Materials/Answer Keys/hand_summary_errors_key.txt
  03 Learner Materials/Practice Files/01 Case Company/supplier_quote_pearl_packaging.txt

The hand summary holds the 12 true weekly revenue totals from weekly_sales.csv except for
EXACTLY TWO planted errors: one transposed-digit total and one wrong week selected
(the total of the week before was typed instead). All figures are fictional.
"""
import csv
from collections import OrderedDict
from pathlib import Path

HERE = Path(__file__).resolve().parent
EDITION = HERE.parents[2]
CASE = EDITION / "03 Learner Materials" / "Practice Files" / "01 Case Company"
BUILD = EDITION / "03 Learner Materials" / "Practice Files" / "03 Apps Script Build"
KEYS = EDITION / "04 Facilitator Materials" / "Answer Keys"

TRANSPOSED_WEEK = "2026-08-24"   # two neighbouring digits swapped
WRONG_WEEK = "2026-10-12"        # the total of the week before was typed in
HAND_FILE = BUILD / "last_month_summary_by_hand.csv"


def true_totals():
    tot = OrderedDict()
    with open(CASE / "weekly_sales.csv", newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            tot[r["week_start"]] = tot.get(r["week_start"], 0) + int(r["revenue_ugx"])
    return tot


def swap_digits(n):
    """Swap the first pair of neighbouring different digits after the leading three."""
    s = str(n)
    for i in range(3, len(s) - 1):
        if s[i] != s[i + 1]:
            return int(s[:i] + s[i + 1] + s[i] + s[i + 2:])
    raise ValueError("no digits to swap")


def hand_totals(true):
    weeks = list(true)
    hand = OrderedDict(true)
    hand[TRANSPOSED_WEEK] = swap_digits(true[TRANSPOSED_WEEK])
    prev = weeks[weeks.index(WRONG_WEEK) - 1]
    hand[WRONG_WEEK] = true[prev]
    return hand


def write_hand_summary():
    true = true_totals()
    hand = hand_totals(true)
    with open(HAND_FILE, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["week_start", "total_revenue_ugx"])
        for wk, v in hand.items():
            w.writerow([wk, v])
    weeks = list(true)
    prev = weeks[weeks.index(WRONG_WEEK) - 1]
    key = """KEY: errors in last_month_summary_by_hand.csv (facilitator only)
Source files: last_month_summary_by_hand.csv and weekly_sales.csv. The verifier checks every figure below.

The file is the Sales Manager's hand-made weekly summary. It holds 12 weekly totals. Exactly two differ from the true totals.

ERROR 1 | Week %(w1)s | Transposed digits | In the file: %(h1)d | True total: %(t1)d | Difference: %(d1)d
Two neighbouring digits were swapped when the figure was typed. The total looks right at a glance.

ERROR 2 | Week %(w2)s | Wrong week selected | In the file: %(h2)d | True total: %(t2)d | Difference: %(d2)d
The figure in the file is the true total of the week starting %(pw)s. The Sales Manager picked the wrong week.

The other 10 weeks match the script's totals exactly.

How the learner uses it (Session 8): run the digest and read the line for each week under "Total for every week in the sheet". An error is any figure in the hand-made summary that differs from the script's total for the same week. The learner counts the errors first. This key gives the answer afterwards: 2 errors in 12 weeks.
""" % dict(w1=TRANSPOSED_WEEK, h1=hand[TRANSPOSED_WEEK], t1=true[TRANSPOSED_WEEK], d1=hand[TRANSPOSED_WEEK] - true[TRANSPOSED_WEEK],
         w2=WRONG_WEEK, h2=hand[WRONG_WEEK], t2=true[WRONG_WEEK], d2=hand[WRONG_WEEK] - true[WRONG_WEEK], pw=prev)
    (KEYS / "hand_summary_errors_key.txt").write_text(key, encoding="utf-8")


QUOTE = """FICTIONAL TEACHING DOCUMENT
Not a real quotation. All names, firms and figures are invented for training.

QUOTATION PP-Q-2026-0042
Pearl Packaging Ltd, Plot 21 Industrial Area, Jinja, Uganda
Date of quotation: 12 October 2026
Prepared for: Nile Valley Foods Ltd, Plot 12 Industrial Road, Jinja (Attention: Grace Akello, Operations Manager)
Contact at Pearl Packaging: Sales Desk, sales@pearlpackaging.example.com, 0700 000 190

Subject: Printed labels and cartons for the 5L cooking oil bottle

Items quoted
1. Printed labels for 5L oil bottles, full colour, roll of 1,000. Quantity 10 rolls. Unit price UGX 95,000. Line total UGX 950,000.
2. Cartons for 5L oil, printed on two sides, bundle of 100. Quantity 20 bundles. Unit price UGX 185,000. Line total UGX 3,700,000.

Subtotal (before VAT): UGX 4,650,000
VAT at 18%: UGX 837,000
Total (including VAT): UGX 5,487,000

Terms
Price validity: prices are valid for 14 days from the date of this quotation.
Delivery time: delivery within 10 working days after you approve the printed proof, to the NVF depot in Jinja.
Returns: a 5% restocking fee applies to returned cartons. Printed labels cannot be returned once printed.
Payment: 50% with the order and the balance on delivery, by bank transfer or mobile money.
Artwork: NVF supplies the artwork. One proof is included. Each extra proof costs UGX 30,000.

To accept, sign below and send the signed copy to the contact named above.

Signed for Pearl Packaging Ltd: Rose Atieno, Sales Executive.
Accepted for Nile Valley Foods Ltd: ______________________  Date: ______________
"""


def write_quote():
    (CASE / "supplier_quote_pearl_packaging.txt").write_text(QUOTE, encoding="utf-8")


if __name__ == "__main__":
    write_hand_summary()
    write_quote()
    print("Wrote last_month_summary_by_hand.csv, hand_summary_errors_key.txt and supplier_quote_pearl_packaging.txt")
