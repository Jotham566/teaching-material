"""Recompute every worked number on the Session 12 money slides (kettle, invented round numbers; NVF plan from the workbook inputs).
Run from Build/:  python demo_runs/s12/teaching_numbers_check.py   (added 11 November 2026)."""
# kettle
base, after, kettle = 30000, 10000, 60000
save = base - after
print('kettle net saving a month', save, '| cumulative', [save * m for m in (1, 2, 3, 4)], '| payback months', kettle / save)
ben, cost = 12 * base, kettle + 12 * after
print('kettle first year benefits', ben, 'costs', cost, 'net', ben - cost, '(check 12 x saving - kettle =', 12 * save - kettle, ') ROI', (ben - cost) / cost)
# NVF
n, t0, t1, rev, rate = 4, 90, 10, 20, 30000
print('NVF minutes saved', n * (t0 - t1), 'hours', round(n * (t0 - t1) / 60, 2), '| after review minutes', n * (t0 - t1 - rev), 'hours', n * (t0 - t1 - rev) / 60)
time_b = n * (t0 - t1) / 60 * rate; err_b = 4 * 0.4 * 0.6 * 150000
oneoff = (12 + 4) * rate; monthly = 60000 + n * rev / 60 * rate + 1.5 * rate
net = time_b + err_b - monthly
print('NVF benefits', round(time_b), round(err_b), round(time_b + err_b), '| one-off', oneoff, '| monthly', round(monthly), '| net a month', round(net))
print('NVF payback', round(oneoff / net, 2), '| 12-month net', round(12 * net - oneoff), '| 12-month costs', round(oneoff + 12 * monthly), '| ROI', round((12 * net - oneoff) / (oneoff + 12 * monthly), 3))
