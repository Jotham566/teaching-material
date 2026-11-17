"""Registration-number handling; the roster is authoritative for identity."""
import base64
import re

REGISTRATION_PATTERN = r'[0-9]{2}/[A-Z]{2,8}/[0-9]{1,10}/[A-Z0-9]+(?:-[A-Z0-9]+)*'

def normalize(value):
    return value.strip().upper() if isinstance(value,str) else ''

def valid(value, allow_legacy=False):
    """Accept nonempty text; identity is verified against the roster and email.

    allow_legacy remains for compatibility with callers. No institutional
    number format is imposed. Control characters are not registration text.
    """
    value = normalize(value)
    return bool(value) and all(c.isprintable() for c in value)

def filename_id(value):
    value = normalize(value)
    if not valid(value, allow_legacy=True):
        raise ValueError('Invalid Student Registration Number')
    # Keep already issued filenames compatible. Encode every other format,
    # including underscores and punctuation, so identity text is never a path.
    if re.fullmatch(REGISTRATION_PATTERN,value) or re.fullmatch(r'S[0-9]{4,8}',value):
        return value.replace('/', '_')
    return 'REG-'+base64.b32encode(value.encode('utf-8')).decode('ascii').rstrip('=')

def registration_from_filename(name):
    encoded=re.match(r'^REG-([A-Z2-7]+)(?=_|\.|$)',name.upper())
    if encoded:
        token=encoded.group(1)
        try:
            value=base64.b32decode(token+'='*((-len(token))%8)).decode('utf-8')
        except (ValueError,UnicodeDecodeError):
            return None
        return value if valid(value) else None
    match = re.match(r'^([0-9]{2}_[A-Z]{2,8}_[0-9]{1,10}_[A-Z0-9]+(?:-[A-Z0-9]+)*)(?=_|\.|$)', name.upper())
    return match.group(1).replace('_', '/') if match else None
