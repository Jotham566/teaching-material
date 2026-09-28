"""Rebuild the 41 revised IUEA teaching decks with Artifact Tool.
Completed Week 1 teaching and CML3112 Week 2 stay intact.
"""
from pathlib import Path
from datetime import datetime, timezone
import subprocess,os,sys
ROOT=Path(__file__).resolve().parents[1]
RUNTIME=Path.home()/'.cache/codex-runtimes/codex-primary-runtime/dependencies'
def main():
 node=RUNTIME/'node/bin/node';python=RUNTIME/'python/bin/python3'
 if not node.is_file() or not python.is_file():raise RuntimeError('Load the bundled workspace dependencies first.')
 env=os.environ.copy();env['PPT_EDITION']='build-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')
 subprocess.run([str(python),'scripts/prepare_beginner_ppt_content.py'],cwd=ROOT,check=True)
 subprocess.run([str(node),'scripts/build_beginner_decks.mjs'],cwd=ROOT,env=env,check=True)
 subprocess.run([str(python),'scripts/publish_beginner_decks.py'],cwd=ROOT,check=True)
 print('Updated the revised PowerPoints. No separate QR insertion step is needed.')
 return 0
if __name__=='__main__':sys.exit(main())
