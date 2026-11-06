"""Recompute the NVF example in Templates/Business Case Workbook.xlsx from its grey input values, using the workbook's own formulas.
Run from Build/:  python demo_runs/s12/business_case_check.py   (reads the template; nothing is written)."""
from pathlib import Path
import openpyxl
T = Path(__file__).resolve().parents[4] / '03 Learner Materials' / 'Templates' / 'Business Case Workbook.xlsx'
ws = openpyxl.load_workbook(T)['Inputs']
v = {r: ws[f'B{r}'].value for r in range(5, 15)}
times, mins, people, rate, err, ecost, new, review, removed = v[6], v[7], v[8], v[9], v[10], v[11], v[12], v[13], v[14]
time_saved = times * people * (mins - new) / 60 * rate
errors = times * err * removed * ecost
benefit = time_saved + errors
monthly_cost = 60000 + times * review / 60 * rate + 1.5 * rate
one_off = 12 * rate + 4 * rate
net = benefit - monthly_cost
print('inputs', times, mins, new, review, rate, err, ecost, removed)
print('hours saved a month', round(times * people * (mins - new) / 60, 2))
print('time saved UGX', round(time_saved), 'errors avoided UGX', round(errors), 'benefit', round(benefit))
print('monthly cost', round(monthly_cost), 'one-off', round(one_off), 'monthly net', round(net))
print('payback months', round(one_off / net, 2), '12-month net', round(net * 12 - one_off))
hc = 0.3
print('after 30% haircut 12-month net', round((benefit * (1 - hc) - monthly_cost) * 12 - one_off))
print('break-even haircut', round(1 - (monthly_cost * 12 + one_off) / (benefit * 12), 3))
