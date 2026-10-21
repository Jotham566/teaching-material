"""Validate the lecturer's self-contained CA export before importing it."""
import hashlib
import json
from pathlib import Path
import zipfile


def bundle_header(path):
    with zipfile.ZipFile(path) as z:
        if 'ca_bundle.json' not in z.namelist(): return None
        if z.getinfo('ca_bundle.json').file_size>2_000_000: raise ValueError('Bundle metadata too large')
        return json.loads(z.read('ca_bundle.json'))


def verify_bundle(path):
    meta=bundle_header(path)
    if not meta or meta.get('format')!='IUEA_CA_BUNDLE' or meta.get('version')!=1 or meta.get('complete') is not True:
        raise ValueError('This is not a completed one-ZIP grading export')
    with zipfile.ZipFile(path) as z:
        names=z.namelist();entries=meta['files']
        expected=[x['name'] for x in entries]+['ca_bundle.json']
        if len(names)!=len(set(names)) or len(expected)!=len(set(expected)) or set(names)!=set(expected):
            raise ValueError('Bundle inventory mismatch or duplicate member')
        if sum(x.file_size for x in z.infolist())>500_000_000:raise ValueError('Bundle exceeds extraction limit')
        for entry in entries:
            name=entry['name']
            if Path(name).name!=name or '\\' in name:raise ValueError('Unsafe bundle member')
            content=z.read(name)
            if len(content)!=entry['bytes'] or hashlib.sha256(content).hexdigest()!=entry['sha256']:
                raise ValueError('Bundle checksum mismatch: '+name)
    return meta
