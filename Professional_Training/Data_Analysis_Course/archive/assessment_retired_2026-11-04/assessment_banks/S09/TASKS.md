# Session 9 — reconciliation and cleaning log

Use the supplied fictional Riverside data. Submit one notebook and one accessible DOCX or selectable-text PDF cleaning log together through the S09 form. The log is assessed separately from code, so copying task prompts or code comments does not supply written evidence.

The checkpoint remains 15% of the independent track. It is marked out of 100: 50 executed marks and 50 written marks. The original criterion totals remain Cleaning log 40, Reconciliation 40, Reproducibility 20. The checked cleaning function contributes 10 to Cleaning log; the report contributes 30 to Reconciliation; order normalisation contributes 10 to Reproducibility. The written criteria below supply the remainder.

Implement these functions in the notebook. Their unseen inputs use the same documented schema and rules; exchange rates, customer aliases and product categories can vary. You may use pandas internally. Never hardcode the supplied totals.

## normalise_orders(rows, customer_aliases)

10 executed marks. Return copied order dictionaries in the same order. Convert order_id and rep_id to integers; customer_id is an integer or None for a blank walk-in ID. Apply the supplied customer-ID alias map. Parse dates explicitly as ISO YYYY-MM-DD or day/month/year and return ISO dates. Preserve all other fields and the input. Never drop a missing-customer order.

## clean_line_items(rows, products, usd_ugx)

10 executed marks. Remove exact duplicate raw rows, not every repeated line_no. Separate negative quantities into returns with positive quantity_returned. Convert Imported appliances unit_price to UGX at the supplied rate; other prices are already UGX. Divide discounts above 1 by 100. Return a dictionary with sales (order_id,line_no,product_id,quantity,unit_price_ugx,discount), returns (line_no,quantity_returned), and duplicates_removed. Retain source order within each list; preserve inputs.

## rep_month_report(orders, sales, returns, reps, year)

30 executed marks. Return one row per delivered-order rep/month for the supplied year. Columns in order: region,rep_name,month,gross_ugx,returned_ugx,net_ugx. Return a list of six-element rows or a pandas DataFrame with those columns. Missing customer IDs must not remove sales. Aggregate multiple return events per line before joining, so gross is counted once. Extra/missing rows fail the contract; each amount allows 1 UGX after rounding.

## Supplied business rules

Slash dates are day/month/year. Imported appliances were entered in USD; the teaching conversion is 3780 UGX/USD. The documented duplicate customer is 1999, mapped to 1007. Missing walk-in customer IDs remain missing. Exact duplicate export rows can be removed, but a negative return and a positive sale sharing line_no are distinct records. Multiple return events must not multiply gross sales.

First reproduce the 2025 delivered rep/month report from the clean database tables in pandas and reconcile it against SQL (1 UGX after rounding). Then run the same workflow from the raw CSVs and explain the separate currency-rounding residual. The raw USD prices were rounded to cents; changing results just to equal the database is not a valid cleaning operation.

## Written log — at most 900 words

- Duplicates (5 marks): Award 5 if the written log explains that exact duplicate exported rows are removed to avoid double-counting. Otherwise award zero.

- Returns (5 marks): Award 5 if the written log explains that negative-quantity return rows are retained separately and deducted, rather than treated as errors or additional sales. Otherwise award zero.

- Currency (5 marks): Award 5 if the written log uses the documented 3780 UGX per USD for Imported appliances and explains that other prices are already UGX. Otherwise award zero.

- Discount (5 marks): Award 5 if the written log explains converting percentage discounts above one to fractions by dividing by 100. Otherwise award zero.

- Dates (5 marks): Award 5 if the written log explicitly interprets slash dates as day/month/year and standardises dates without changing which month an order belongs to. Otherwise award zero.

- Customers (5 marks): Award 5 if the written log keeps missing-customer walk-in orders in the sales population and applies the documented customer alias without inventing an identity. Otherwise award zero.

- Reconciliation (5 marks): Award 5 if the written log compares the same 2025 delivered-order rep/month population and checks gross, returned and net amounts against SQL using a stated 1 UGX rounding tolerance for the clean-table report. Otherwise award zero.

- Rounding (5 marks): Award 5 if the written log explains that raw USD prices rounded to cents cannot recover exact original UGX prices, so residual differences must be explained rather than overwritten to match SQL. Otherwise award zero.

- Raw (5 marks): Award 5 if the written log retains original raw inputs unchanged and documents the ordered cleaning steps. Otherwise award zero.

- Run (5 marks): Award 5 if the written log names the required input files and gives a clean top-to-bottom run procedure that regenerates the report. Otherwise award zero.

## Files and execution

Input files: orders_raw.csv, order_items_raw.csv, customers_raw.csv, products.csv, reps.csv and riverside.db; the clean CSVs support reconciliation. Start from raw copies, inspect defects, normalise orders, clean line items, generate the report, and compare to SQL. Preserve the raw files. Set STUDENT_ID to your DA roster ID (for example S10001) and COHORT to DA. Save the notebook as S10001_S09.ipynb. Keep private answer keys out of your repository.

## Release status

DRAFT until the local rubric calibration passes. The S09 form remains closed until the lecturer supplies the actual session dates.
