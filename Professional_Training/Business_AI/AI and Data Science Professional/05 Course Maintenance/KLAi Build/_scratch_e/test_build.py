import sys, importlib.util
from pathlib import Path
B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(B / 'kit'))
import deck
sp = importlib.util.spec_from_file_location('scratch_e', B / '_scratch_e' / 'diagrams_ds_e.py')
m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
def wrap(k, f):
    def g(d, sl):
        try:
            return f(d, sl)
        except Exception as e:
            print('SLIDE FAILED:', sl.get('title'), type(e).__name__, str(e)[:200])
            raise
    return g
for k in list(deck.KINDS):
    deck.KINDS[k] = wrap(k, deck.KINDS[k])
deck.main(sys.argv[1:])
