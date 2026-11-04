"""Copy a file into a sibling `_backup_2026-11-02` folder before it is changed.

Rule from the lecturer: never delete or overwrite an original without a copy first.
The first copy wins. If the backup already exists it is NOT overwritten, so running a patch
twice never replaces the true original with an already-patched file.
Usage in a script:  from backup_20261102 import backup;  backup(path)   (returns the backup path)
"""
import shutil
from pathlib import Path

NAME = "_backup_2026-11-02"


def backup(path):
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"cannot back up, not a file: {path}")
    dest_dir = path.parent / NAME
    dest_dir.mkdir(exist_ok=True)
    dest = dest_dir / path.name
    if not dest.exists():
        shutil.copy2(path, dest)
    return dest
