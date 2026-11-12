# Session 14 recorded run: counting the faults in the NVF practice files

- What was run: demo_runs/s14/nvf_file_check.py (plain Python 3.12.10 with pandas 3.1.1). No AI model.
- Date: 6 November 2026. One run (deterministic).
- Input: the three files in Practice Files/01 Case Company: supplier_invoices.csv, customer_messages.csv, weekly_sales.csv.
- Command: python nvf_file_check.py "<path to 01 Case Company>"
- Exact output: demo_runs/s14/nvf_file_check_output.txt. Summary: 60 invoice rows with 4 wrong totals (LL-2026-0449, PP-2026-0159, EM-2026-0250, PP-2026-0174), 2 missing PO numbers, 1 line with VAT 0 percent, 1 duplicated invoice id (TR-2026-0093): 8 faults. 40 customer messages, 32 sender cells holding a phone number. 360 weekly sales rows from 2026-08-03 to 2026-10-19; no definition of revenue.
- Agrees with Answer Keys/invoice_errors_key.csv (8 planted faults).
- The NVF readiness scorecard (6 of 12), the roadmap lines, owners and hours are from Templates/Information Inventory.xlsx and 90-Day Roadmap.xlsx (invented teaching values). The day 90 re-score of 9 of 12 is a teaching example, not a result.
