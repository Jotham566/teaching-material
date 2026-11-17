# -*- coding: utf-8 -*-
"""A QR encoder in pure Python, byte mode, versions 1 to 10.

Written from scratch because neither `qrcode` nor `segno` is installed and pip
cannot reach the index from this environment. That turns out to be the right
answer anyway: QR generation for this course now has no third-party dependency
and no network call, so the same script will still work in three years.

Scope is deliberately narrow. Byte mode only, which covers URLs; versions 1-10,
which covers up to 271 bytes at error-correction level M; the four standard
error-correction levels. Kanji, numeric and alphanumeric modes are not
implemented, and neither are versions 11-40, because nothing here needs them.

Verified three ways in qrgen_selftest.py: the GF(256) arithmetic and the
Reed-Solomon generator polynomials against published values, the finished
matrix against the ISO/IEC 18004 worked example, and a round-trip through an
independently written decoder that re-derives the module placement order rather
than reusing the encoder's.
"""
from PIL import Image

# --------------------------------------------------------------------------
# GF(256) arithmetic, the field QR uses. Primitive polynomial 0x11d.
# --------------------------------------------------------------------------
_EXP = [0] * 512
_LOG = [0] * 256


def _init_tables():
    x = 1
    for i in range(255):
        _EXP[i] = x
        _LOG[x] = i
        x <<= 1
        if x & 0x100:
            x ^= 0x11D
    for i in range(255, 512):
        _EXP[i] = _EXP[i - 255]


_init_tables()


def _gf_mul(a, b):
    if a == 0 or b == 0:
        return 0
    return _EXP[_LOG[a] + _LOG[b]]


def _rs_generator(n):
    """Generator polynomial for n error-correction codewords."""
    g = [1]
    for i in range(n):
        # multiply g by (x - alpha^i)
        nxt = [0] * (len(g) + 1)
        for j, c in enumerate(g):
            nxt[j] ^= _gf_mul(c, 1)
            nxt[j + 1] ^= _gf_mul(c, _EXP[i])
        g = nxt
    return g


def _rs_encode(data, n):
    """Return the n Reed-Solomon codewords for these data codewords."""
    gen = _rs_generator(n)
    rem = [0] * n
    for d in data:
        factor = d ^ rem[0]
        rem = rem[1:] + [0]
        for i, g in enumerate(gen[1:]):
            rem[i] ^= _gf_mul(g, factor)
    return rem


# --------------------------------------------------------------------------
# Version tables. For each version 1-10 and each EC level, the number of EC
# codewords per block and the block structure (count, total codewords).
# Taken from ISO/IEC 18004 table 9.
# --------------------------------------------------------------------------
# (ec_per_block, [(num_blocks, total_codewords_in_block), ...])
_SPEC = {
    (1, "L"): (7,  [(1, 26)]),
    (1, "M"): (10, [(1, 26)]),
    (1, "Q"): (13, [(1, 26)]),
    (1, "H"): (17, [(1, 26)]),
    (2, "L"): (10, [(1, 44)]),
    (2, "M"): (16, [(1, 44)]),
    (2, "Q"): (22, [(1, 44)]),
    (2, "H"): (28, [(1, 44)]),
    (3, "L"): (15, [(1, 70)]),
    (3, "M"): (26, [(1, 70)]),
    (3, "Q"): (18, [(2, 35)]),
    (3, "H"): (22, [(2, 35)]),
    (4, "L"): (20, [(1, 100)]),
    (4, "M"): (18, [(2, 50)]),
    (4, "Q"): (26, [(2, 50)]),
    (4, "H"): (16, [(4, 25)]),
    (5, "L"): (26, [(1, 134)]),
    (5, "M"): (24, [(2, 67)]),
    (5, "Q"): (18, [(2, 33), (2, 34)]),
    (5, "H"): (22, [(2, 33), (2, 34)]),
    (6, "L"): (18, [(2, 86)]),
    (6, "M"): (16, [(4, 43)]),
    (6, "Q"): (24, [(4, 43)]),
    (6, "H"): (28, [(4, 43)]),
    (7, "L"): (20, [(2, 98)]),
    (7, "M"): (18, [(4, 49)]),
    (7, "Q"): (18, [(2, 32), (4, 33)]),
    (7, "H"): (26, [(4, 39), (1, 40)]),
    (8, "L"): (24, [(2, 121)]),
    (8, "M"): (22, [(2, 60), (2, 61)]),
    (8, "Q"): (22, [(4, 40), (2, 41)]),
    (8, "H"): (26, [(4, 40), (2, 41)]),
    (9, "L"): (30, [(2, 146)]),
    (9, "M"): (22, [(3, 58), (2, 59)]),
    (9, "Q"): (20, [(4, 36), (4, 37)]),
    (9, "H"): (24, [(4, 36), (4, 37)]),
    (10, "L"): (18, [(2, 86), (2, 87)]),
    (10, "M"): (26, [(4, 69), (1, 70)]),
    (10, "Q"): (24, [(6, 43), (2, 44)]),
    (10, "H"): (28, [(6, 43), (2, 44)]),
}

# Alignment pattern centre coordinates per version.
_ALIGN = {1: [], 2: [6, 18], 3: [6, 22], 4: [6, 26], 5: [6, 30], 6: [6, 34],
          7: [6, 22, 38], 8: [6, 24, 42], 9: [6, 26, 46], 10: [6, 28, 50]}

# Version information bit strings for versions 7 and above (18 bits).
_VERSION_INFO = {7: 0x07C94, 8: 0x085BC, 9: 0x09A99, 10: 0x0A4D3}

_EC_BITS = {"L": 0b01, "M": 0b00, "Q": 0b11, "H": 0b10}


def _data_capacity_bytes(version, ec):
    ec_per, blocks = _SPEC[(version, ec)]
    total = sum(n * t for n, t in blocks)
    ec_total = sum(n for n, _ in blocks) * ec_per
    return total - ec_total


def _choose_version(nbytes, ec):
    for v in range(1, 11):
        # 4 bits mode + count indicator + data, must fit the data capacity
        count_bits = 8 if v <= 9 else 16
        need_bits = 4 + count_bits + nbytes * 8
        if need_bits <= _data_capacity_bytes(v, ec) * 8:
            return v
    raise ValueError(
        f"{nbytes} bytes will not fit in versions 1-10 at level {ec}. "
        "Shorten the URL or extend the version tables.")


# --------------------------------------------------------------------------
# Bit stream and codeword assembly
# --------------------------------------------------------------------------
def _make_codewords(data, version, ec):
    count_bits = 8 if version <= 9 else 16
    bits = []

    def put(value, n):
        for i in range(n - 1, -1, -1):
            bits.append((value >> i) & 1)

    put(0b0100, 4)                 # byte mode
    put(len(data), count_bits)
    for b in data:
        put(b, 8)

    cap_bits = _data_capacity_bytes(version, ec) * 8
    put(0, min(4, cap_bits - len(bits)))          # terminator
    while len(bits) % 8:
        bits.append(0)
    pads = [0xEC, 0x11]
    i = 0
    while len(bits) < cap_bits:
        put(pads[i % 2], 8)
        i += 1

    codewords = [int("".join(str(b) for b in bits[i:i + 8]), 2)
                 for i in range(0, len(bits), 8)]

    # split into blocks, compute ECC per block, then interleave
    ec_per, blocks = _SPEC[(version, ec)]
    data_blocks, ec_blocks = [], []
    pos = 0
    for n, total in blocks:
        dlen = total - ec_per
        for _ in range(n):
            blk = codewords[pos:pos + dlen]
            pos += dlen
            data_blocks.append(blk)
            ec_blocks.append(_rs_encode(blk, ec_per))

    out = []
    for i in range(max(len(b) for b in data_blocks)):
        for b in data_blocks:
            if i < len(b):
                out.append(b[i])
    for i in range(ec_per):
        for b in ec_blocks:
            out.append(b[i])
    return out


# --------------------------------------------------------------------------
# Module placement
# --------------------------------------------------------------------------
def _size(version):
    return version * 4 + 17


def _blank(version):
    n = _size(version)
    return [[None] * n for _ in range(n)]


def _place_function_patterns(m, version):
    n = len(m)

    def finder(r, c):
        for dr in range(-1, 8):
            for dc in range(-1, 8):
                rr, cc = r + dr, c + dc
                if not (0 <= rr < n and 0 <= cc < n):
                    continue
                if dr in (-1, 7) or dc in (-1, 7):
                    m[rr][cc] = 0            # separator
                else:
                    ring = max(abs(dr - 3), abs(dc - 3))
                    m[rr][cc] = 1 if ring != 2 else 0

    finder(0, 0)
    finder(0, n - 7)
    finder(n - 7, 0)

    for i in range(8, n - 8):                 # timing patterns
        bit = 1 if i % 2 == 0 else 0
        if m[6][i] is None:
            m[6][i] = bit
        if m[i][6] is None:
            m[i][6] = bit

    for r in _ALIGN[version]:                 # alignment patterns
        for c in _ALIGN[version]:
            if (r < 9 and c < 9) or (r < 9 and c > n - 10) or \
               (r > n - 10 and c < 9):
                continue
            for dr in range(-2, 3):
                for dc in range(-2, 3):
                    ring = max(abs(dr), abs(dc))
                    m[r + dr][c + dc] = 1 if ring != 1 else 0

    m[n - 8][8] = 1                           # the always-dark module

    for i in range(9):                        # reserve format areas
        if m[8][i] is None:
            m[8][i] = 0
        if m[i][8] is None:
            m[i][8] = 0
    for i in range(8):
        if m[8][n - 1 - i] is None:
            m[8][n - 1 - i] = 0
        if m[n - 1 - i][8] is None:
            m[n - 1 - i][8] = 0

    if version >= 7:                          # reserve version areas
        for i in range(6):
            for j in range(3):
                m[n - 11 + j][i] = 0
                m[i][n - 11 + j] = 0
    return m


def data_module_order(version):
    """The order data modules are filled, derived from the version geometry.

    Kept public and free of any encoder state so the self-test decoder can
    re-derive it independently.
    """
    n = _size(version)
    reserved = _place_function_patterns(_blank(version), version)
    order = []
    col = n - 1
    upward = True
    while col > 0:
        if col == 6:                          # skip the vertical timing column
            col -= 1
        rows = range(n - 1, -1, -1) if upward else range(n)
        for row in rows:
            for c in (col, col - 1):
                if reserved[row][c] is None:
                    order.append((row, c))
        upward = not upward
        col -= 2
    return order


_MASKS = [
    lambda r, c: (r + c) % 2 == 0,
    lambda r, c: r % 2 == 0,
    lambda r, c: c % 3 == 0,
    lambda r, c: (r + c) % 3 == 0,
    lambda r, c: (r // 2 + c // 3) % 2 == 0,
    lambda r, c: (r * c) % 2 + (r * c) % 3 == 0,
    lambda r, c: ((r * c) % 2 + (r * c) % 3) % 2 == 0,
    lambda r, c: ((r + c) % 2 + (r * c) % 3) % 2 == 0,
]


def _penalty(m):
    n = len(m)
    score = 0

    # rule 1: runs of five or more same-colour modules in a row or column
    for line in list(m) + [list(col) for col in zip(*m)]:
        run, prev = 1, line[0]
        for v in line[1:]:
            if v == prev:
                run += 1
            else:
                if run >= 5:
                    score += 3 + (run - 5)
                run, prev = 1, v
        if run >= 5:
            score += 3 + (run - 5)

    # rule 2: 2x2 blocks of one colour
    for r in range(n - 1):
        for c in range(n - 1):
            if m[r][c] == m[r][c + 1] == m[r + 1][c] == m[r + 1][c + 1]:
                score += 3

    # rule 3: the 1:1:3:1:1 finder-like pattern with four light modules
    pat_a = [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0]
    pat_b = [0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1]
    for line in list(m) + [list(col) for col in zip(*m)]:
        for i in range(n - 10):
            seg = line[i:i + 11]
            if seg == pat_a or seg == pat_b:
                score += 40

    # rule 4: deviation of the dark-module proportion from one half
    dark = sum(sum(row) for row in m)
    pct = dark * 100 // (n * n)
    score += 10 * (abs(pct - 50) // 5)
    return score


def _format_bits(ec, mask):
    data = (_EC_BITS[ec] << 3) | mask
    # long division by the BCH generator 0x537
    rem = data << 10
    for i in range(4, -1, -1):
        if rem & (1 << (i + 10)):
            rem ^= 0x537 << i
    return ((data << 10) | rem) ^ 0x5412


# Format information placement, copy one, in MSB-to-LSB order: the cell at
# FORMAT_C1[k] carries format bit (14 - k). Getting this backwards is
# invisible to a round-trip test (encoder and decoder agree with each other)
# but makes every real scanner read the EC level and mask wrong, which is
# exactly what happened: the codes looked perfect and scanned as nothing.
FORMAT_C1 = [(8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 7), (8, 8),
             (7, 8), (5, 8), (4, 8), (3, 8), (2, 8), (1, 8), (0, 8)]


def format_cells(n):
    """The two format-info copies as cell lists, each MSB first.

    Public so the self-test can check placement against an external
    reference implementation rather than against this module's own encoder.
    """
    c1 = list(FORMAT_C1)
    # copy two: bits 14..8 run UP the left edge in column 8 (rows n-1 to
    # n-7), then bits 7..0 run along row 8 from column n-8 to n-1. Module
    # (n-8, 8) is the always-dark module and is not part of the format area.
    c2 = [(n - 1 - i, 8) for i in range(7)] + [(8, n - 8 + i) for i in range(8)]
    return c1, c2


def _place_format(m, ec, mask):
    n = len(m)
    bits = _format_bits(ec, mask)
    c1, c2 = format_cells(n)

    # MSB first: cell k of each copy carries bit (14 - k).
    for k, (r, c) in enumerate(c1):
        m[r][c] = (bits >> (14 - k)) & 1
    for k, (r, c) in enumerate(c2):
        m[r][c] = (bits >> (14 - k)) & 1

    return m


def _place_version(m, version):
    if version < 7:
        return m
    n = len(m)
    v = _VERSION_INFO[version]
    for i in range(18):
        b = (v >> i) & 1
        m[n - 11 + i % 3][i // 3] = b
        m[i // 3][n - 11 + i % 3] = b
    return m


def encode(text, ec="M"):
    """Return the QR matrix for `text` as a list of rows of 0/1."""
    data = text.encode("utf-8")
    version = _choose_version(len(data), ec)
    codewords = _make_codewords(data, version, ec)

    base = _place_function_patterns(_blank(version), version)
    order = data_module_order(version)

    bits = []
    for cw in codewords:
        for i in range(7, -1, -1):
            bits.append((cw >> i) & 1)
    # remainder bits stay light
    while len(bits) < len(order):
        bits.append(0)

    best, best_score = None, None
    for mask in range(8):
        m = [row[:] for row in base]
        for (r, c), b in zip(order, bits):
            m[r][c] = b ^ (1 if _MASKS[mask](r, c) else 0)
        _place_format(m, ec, mask)
        _place_version(m, version)
        s = _penalty(m)
        if best_score is None or s < best_score:
            best, best_score = m, s
    return best


def png(text, path, ec="M", module_px=10, quiet=4):
    """Write `text` as a QR code PNG."""
    m = encode(text, ec)
    n = len(m)
    side = (n + quiet * 2) * module_px
    img = Image.new("L", (side, side), 255)
    px = img.load()
    for r in range(n):
        for c in range(n):
            if m[r][c]:
                x0 = (c + quiet) * module_px
                y0 = (r + quiet) * module_px
                for y in range(y0, y0 + module_px):
                    for x in range(x0, x0 + module_px):
                        px[x, y] = 0
    img.save(path)
    return path
