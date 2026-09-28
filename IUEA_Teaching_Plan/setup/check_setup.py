"""Lab preflight. Run with Python 3.11 or newer before teaching."""
import importlib
import sys
failed=[]
if sys.version_info < (3,11): failed.append('Python 3.11 or newer required')
for name in ('pandas','numpy','matplotlib','sklearn','nbformat'):
    try: importlib.import_module(name)
    except ImportError: failed.append('Missing '+name)
print('\n'.join(failed) if failed else 'READY: Python and teaching packages import successfully')
sys.exit(bool(failed))
