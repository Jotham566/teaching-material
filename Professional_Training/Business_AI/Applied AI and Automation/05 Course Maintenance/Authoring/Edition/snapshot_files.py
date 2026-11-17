"""Refresh Edition/files from the live edition (run after hand-editing practice files or teaching resources).

  python3 snapshot_files.py

Copies the hand-written, non-generated parts of the live edition into Edition/files, so the staging build can reproduce
them: 00 Start Here.txt, 02 Class Slides/Animation Guide.txt, 03 Learner Materials/Practice Files and 04 Facilitator
Materials/Teaching Resources. Caches are skipped. Edit either side, then snapshot before building.
"""
import shutil
from pathlib import Path
HERE = Path(__file__).resolve().parent; LIVE = HERE.parents[2]
dst = HERE / 'files'
if dst.exists(): shutil.rmtree(dst)
base_ignore = shutil.ignore_patterns('__pycache__', '.DS_Store', '~$*', '.~lock.*#', 'Presenter Notes Backup.txt', 'Playback and Rehearsal Checklist.txt')
def ign(path, names):
    ignored = set(base_ignore(path, names))
    if Path(path).name == 'Rehearsal Audio':
        ignored.update(n for n in names if Path(n).suffix.lower() in ('.m4a', '.aiff'))
    return ignored  # the backup is generated from the notes sources
for rel in ('00 Start Here.txt', '02 Class Slides/Animation Guide.txt'):
    (dst / rel).parent.mkdir(parents=True, exist_ok=True); shutil.copy2(LIVE / rel, dst / rel)
for rel in ('03 Learner Materials/Practice Files', '04 Facilitator Materials/Teaching Resources'):
    shutil.copytree(LIVE / rel, dst / rel, ignore=ign)
print('snapshot written to', dst, sum(1 for _ in dst.rglob('*') if _.is_file()), 'files')
