"""Render figures of one module at slide sizes for a visual check:  python figtest_s9s10.py diagrams_t09 '{"t09_name": "idea"}'  (writes figures/_test_s9s10/*.png)"""
import sys, os, json, importlib
B = os.environ['B']
sys.path.insert(0, B + '/kit')
import figkit, diagrams
importlib.import_module(sys.argv[1])
SIZES = {'idea': (7.7, 4.8), 'wide': (11.9, 4.25), 'demo': (7.3, 3.9), 'ex': (5.5, 3.55), 'keep': (4.1, 4.5)}
out = B + '/figures/_test_s9s10'
os.makedirs(out, exist_ok=True)
for name, size in json.loads(sys.argv[2]).items():
    w, h = SIZES[size]
    try:
        figkit.fig_registry()['x_' + name](w, h).save(f'{out}/{name}.png', name=name)
        print('ok', name, size)
    except Exception as e:
        print('FAIL', name, size, str(e)[:400])
