"""Session 14 demonstration: look inside the NVF practice files and count what an assessor would find.
Run:  python nvf_file_check.py "<path to 01 Case Company folder>"
Plain Python 3, pandas. No AI model is used. Every number on the Session 14 slides about NVF files comes from this output."""
import sys, re
import pandas as pd
from pathlib import Path

d = Path(sys.argv[1])
inv = pd.read_csv(d / 'supplier_invoices.csv')
msg = pd.read_csv(d / 'customer_messages.csv')
sal = pd.read_csv(d / 'weekly_sales.csv')

print('supplier_invoices.csv rows:', len(inv))
calc = (inv.qty * inv.unit_price_ugx * (1 + inv.vat_pct / 100)).round()
wrong = inv[(calc - inv.total_ugx).abs() > 0.5]
print('rows where qty x price x (1+VAT) does not equal the total (includes the zero-VAT row if its total matches 0 percent):', len(wrong))
print(wrong[['invoice_id', 'vat_pct', 'total_ugx']].assign(calculated=calc[wrong.index]).to_string())
print('missing PO number:', inv.po_number.isna().sum(), list(inv[inv.po_number.isna()].invoice_id))
print('rows with VAT 0 percent:', (inv.vat_pct == 0).sum(), list(inv[inv.vat_pct == 0].invoice_id))
dup = inv[inv.duplicated('invoice_id', keep=False)]
print('rows sharing an invoice_id:', len(dup), list(dup.invoice_id.unique()))
print()
print('customer_messages.csv rows:', len(msg))
ph = msg.sender.str.contains(r'\(0\d{3} \d{3} \d{3}\)', regex=True)
print('sender cells holding a phone number (personal data):', int(ph.sum()))
print()
print('weekly_sales.csv rows:', len(sal), 'from', sal.week_start.min(), 'to', sal.week_start.max())
print('columns:', list(sal.columns), '(no definition of revenue: VAT included or not is not stated anywhere in the file)')
