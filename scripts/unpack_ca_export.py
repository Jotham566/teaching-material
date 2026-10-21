"""Extract a private Drive export, verify attachment hashes, never execute files."""
import argparse
import hashlib
import io
import json
import re
import stat
import zipfile
from pathlib import Path, PurePosixPath

from ca_bundle import bundle_header, verify_bundle

MAX_BYTES = 500_000_000


def unpack(archive, destination):
    if bundle_header(archive): verify_bundle(archive)
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    files = destination/'files'
    files.mkdir(exist_ok=True)
    budget = 0

    def extract(zipped, nested=False):
        nonlocal budget
        for entry in zipped.infolist():
            path = PurePosixPath(entry.filename)
            if path.is_absolute() or '..' in path.parts or stat.S_ISLNK(entry.external_attr >> 16):
                raise ValueError('Unsafe ZIP entry')
            if entry.is_dir():
                continue
            budget += entry.file_size
            if budget > MAX_BYTES:
                raise ValueError('Export exceeds extraction limit')
            name = path.name
            content = zipped.read(entry)
            if not nested and re.fullmatch(r'CML311[123]_W0[1-5]_files_\d+\.zip', name):
                with zipfile.ZipFile(io.BytesIO(content)) as inner:
                    extract(inner, True)
            elif nested and re.fullmatch(r'[A-Za-z0-9_-]+\.[A-Za-z0-9]+', name):
                save(files/name, content)
            elif not nested and name in ('ca_bundle.json','quiz_deadlines.json'):
                save(destination/name, content)
            elif not nested and re.fullmatch(r'CML311[123]_(?:W0[1-5]_manifest|Q[1-5]_quiz)\.json', name):
                save(destination/name, content)
            else:
                raise ValueError('Unexpected export file: '+name)

    def save(path, content):
        if path.exists() and path.read_bytes() != content:
            raise ValueError('Conflicting export file: '+path.name)
        path.write_bytes(content)

    with zipfile.ZipFile(archive) as zipped:
        extract(zipped)
    issues = []
    checked = 0
    for manifest in destination.glob('*_manifest.json'):
        meta = json.loads(manifest.read_text())
        issues.extend(meta.get('errors', []))
        for attachment in meta['files']:
            path = files/attachment['export_name']
            if not path.exists():
                issues.append(dict(file_id=attachment['id'], error='DOWNLOAD_MISSING'))
            elif hashlib.sha256(path.read_bytes()).hexdigest() != attachment['sha256']:
                raise ValueError('Attachment checksum mismatch')
            else:
                checked += 1
    (destination/'download_check.json').write_text(json.dumps(dict(verified=checked, issues=issues), indent=2))
    return checked, issues


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive')
    parser.add_argument('destination')
    args = parser.parse_args()
    checked, issues = unpack(args.archive, args.destination)
    print(f'Verified attachments: {checked}; unresolved downloads: {len(issues)}')
