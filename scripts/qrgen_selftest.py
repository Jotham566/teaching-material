# -*- coding: utf-8 -*-
"""Self-test for qrgen.py.

Four independent checks, because a QR code that is subtly wrong still looks
like a QR code and the only other way to find out is to point a phone at it in
front of a hundred students.

1. Reed-Solomon generator polynomials against published coefficients.
2. All 32 format-information strings against the published table in
   ISO/IEC 18004 Annex C.
3. Structural checks on the finished matrix: finder patterns, separators,
   timing patterns, the always-dark module, alignment patterns.
4. A round-trip through a decoder written below that re-derives the module
   order from the geometry and reverses the mask, the interleaving and the
   bitstream. It shares data_module_order with the encoder, which is why
   check 3 tests the geometry that function depends on.
"""
import sys

import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_HERE)
sys.path.insert(0, _HERE)
import qrgen as Q

FAILED = []


def check(name, got, want):
    if got == want:
        print(f"  pass  {name}")
    else:
        print(f"  FAIL  {name}\n          got  {got}\n          want {want}")
        FAILED.append(name)


def ok(name, cond, detail=""):
    if cond:
        print(f"  pass  {name}")
    else:
        print(f"  FAIL  {name}  {detail}")
        FAILED.append(name)


# --------------------------------------------------------------- 1. RS
print("\nReed-Solomon generator polynomials")
check("gen(7)", Q._rs_generator(7),
      [1, 127, 122, 154, 164, 11, 68, 117])
check("gen(10)", Q._rs_generator(10),
      [1, 216, 194, 159, 111, 199, 94, 95, 113, 157, 193])
check("gen(13)", Q._rs_generator(13),
      [1, 137, 73, 227, 17, 177, 17, 52, 13, 46, 43, 83, 132, 120])
check("gen(17)", Q._rs_generator(17),
      [1, 119, 66, 83, 120, 119, 22, 197, 83, 249, 41, 143, 134, 85, 53,
       125, 99, 79])

# GF(256) round trip
ok("GF exp/log round trip",
   all(Q._EXP[Q._LOG[x]] == x for x in range(1, 256)))
ok("GF multiply is commutative",
   all(Q._gf_mul(a, b) == Q._gf_mul(b, a)
       for a in range(0, 256, 17) for b in range(0, 256, 23)))

# --------------------------------------------------- 2. format information
print("\nFormat information, all 32 combinations")
PUBLISHED = {
    "L": [0x77C4, 0x72F3, 0x7DAA, 0x789D, 0x662F, 0x6318, 0x6C41, 0x6976],
    "M": [0x5412, 0x5125, 0x5E7C, 0x5B4B, 0x45F9, 0x40CE, 0x4F97, 0x4AA0],
    "Q": [0x355F, 0x3068, 0x3F31, 0x3A06, 0x24B4, 0x2183, 0x2EDA, 0x2BED],
    "H": [0x1689, 0x13BE, 0x1CE7, 0x19D0, 0x0762, 0x0255, 0x0D0C, 0x083B],
}
bad = []
for ec, row in PUBLISHED.items():
    for mask, want in enumerate(row):
        got = Q._format_bits(ec, mask)
        if got != want:
            bad.append(f"{ec}/mask{mask}: got {got:#06x} want {want:#06x}")
ok("all 32 format strings match the published table", not bad, "; ".join(bad))

# ------------------------------------------------------ 3. structure
print("\nMatrix structure")


def structure_checks(m, version):
    n = len(m)
    problems = []
    # finder patterns at three corners
    for (r0, c0) in [(0, 0), (0, n - 7), (n - 7, 0)]:
        for dr in range(7):
            for dc in range(7):
                ring = max(abs(dr - 3), abs(dc - 3))
                want = 1 if ring != 2 else 0
                if m[r0 + dr][c0 + dc] != want:
                    problems.append(f"finder at {r0},{c0} module {dr},{dc}")
    # separators are light
    for i in range(8):
        for (r, c) in [(7, i), (i, 7), (7, n - 8 + i), (i, n - 8),
                       (n - 8, i), (n - 8 + i, 7)]:
            if 0 <= r < n and 0 <= c < n and m[r][c] != 0:
                problems.append(f"separator at {r},{c}")
    # timing patterns alternate
    for i in range(8, n - 8):
        want = 1 if i % 2 == 0 else 0
        if m[6][i] != want:
            problems.append(f"h-timing at col {i}")
        if m[i][6] != want:
            problems.append(f"v-timing at row {i}")
    # the always-dark module
    if m[n - 8][8] != 1:
        problems.append("dark module")
    # alignment patterns
    for r in Q._ALIGN[version]:
        for c in Q._ALIGN[version]:
            if (r < 9 and c < 9) or (r < 9 and c > n - 10) or \
               (r > n - 10 and c < 9):
                continue
            for dr in range(-2, 3):
                for dc in range(-2, 3):
                    ring = max(abs(dr), abs(dc))
                    want = 1 if ring != 1 else 0
                    if m[r + dr][c + dc] != want:
                        problems.append(f"alignment at {r},{c}")
    # every module decided
    if any(v is None for row in m for v in row):
        problems.append("undecided modules remain")
    return problems


for text, ec in [("https://forms.gle/abcdEFGH1234", "M"),
                 ("https://example.com", "L"),
                 ("x" * 100, "Q"),
                 ("https://docs.google.com/forms/d/e/"
                  "1FAIpQLSdVeryLongLookingFormIdentifier12345/viewform", "M")]:
    m = Q.encode(text, ec)
    v = (len(m) - 17) // 4
    probs = structure_checks(m, v)
    ok(f"structure v{v}/{ec} for {len(text)} bytes", not probs,
       "; ".join(probs[:3]))

# ------------------------------------------------------ 4. round trip
print("\nRound trip through an independent decoder")


def decode(m):
    """Read a matrix back to text, reversing the encoder's steps."""
    n = len(m)
    version = (n - 17) // 4

    # read the format information from copy one and undo the XOR mask.
    # MSB first: cell k carries bit (14 - k). See Q.format_cells.
    c1, _ = Q.format_cells(n)
    bits = 0
    for k, (r, c) in enumerate(c1):
        bits |= m[r][c] << (14 - k)
    raw = bits ^ 0x5412
    ec_field = (raw >> 13) & 0b11
    mask = (raw >> 10) & 0b111
    ec = {0b01: "L", 0b00: "M", 0b11: "Q", 0b10: "H"}[ec_field]

    # unmask the data modules and read them in placement order
    order = Q.data_module_order(version)
    stream = []
    for (r, c) in order:
        stream.append(m[r][c] ^ (1 if Q._MASKS[mask](r, c) else 0))

    codewords = []
    for i in range(0, len(stream) - 7, 8):
        byte = 0
        for b in stream[i:i + 8]:
            byte = (byte << 1) | b
        codewords.append(byte)

    # undo the interleave to recover the data codewords in order
    ec_per, blocks = Q._SPEC[(version, ec)]
    lens = []
    for cnt, total in blocks:
        lens += [total - ec_per] * cnt
    nblocks = len(lens)
    data = [[] for _ in range(nblocks)]
    pos = 0
    for i in range(max(lens)):
        for b in range(nblocks):
            if i < lens[b]:
                data[b].append(codewords[pos])
                pos += 1
    flat = [cw for blk in data for cw in blk]

    # parse the bitstream
    bitstr = "".join(f"{cw:08b}" for cw in flat)
    mode = int(bitstr[:4], 2)
    if mode != 0b0100:
        raise ValueError(f"expected byte mode, got {mode:04b}")
    cbits = 8 if version <= 9 else 16
    count = int(bitstr[4:4 + cbits], 2)
    start = 4 + cbits
    out = bytearray()
    for i in range(count):
        out.append(int(bitstr[start + i * 8:start + i * 8 + 8], 2))
    return out.decode("utf-8"), ec, mask


CASES = [
    ("https://forms.gle/abcdEFGH1234", "M"),
    ("https://forms.gle/xY7kQ2mNpRs9", "M"),
    ("https://example.com", "L"),
    ("https://example.com", "M"),
    ("https://example.com", "Q"),
    ("https://example.com", "H"),
    ("CML3112 Week 1 quiz", "M"),
    ("a", "M"),
    ("x" * 50, "M"),
    ("x" * 100, "Q"),
    ("x" * 150, "M"),
    ("https://docs.google.com/forms/d/e/"
     "1FAIpQLSdVeryLongLookingFormIdentifier12345/viewform", "M"),
    ("unicode: café µm °C", "M"),
]
for text, ec in CASES:
    m = Q.encode(text, ec)
    got, got_ec, mask = decode(m)
    v = (len(m) - 17) // 4
    ok(f"round trip v{v}/{ec} mask{mask} {len(text)}B", got == text and got_ec == ec,
       f"got {got[:40]!r} / {got_ec}")


# ---------------------------------------------------------------------------
# The check that actually matters: an EXTERNAL decoder.
#
# Every test above this line passed while the format information was written
# backwards, because the encoder and this file's decoder shared the same
# wrong convention and therefore agreed with each other. The codes were
# structurally perfect and scanned as nothing at all. A round trip through
# your own code proves self-consistency, never correctness — only an
# independent implementation can do that.
# ---------------------------------------------------------------------------
print("\nExternal decoder (OpenCV) — the only test that proves correctness")
try:
    import numpy as np
    import cv2
except ImportError:
    print("  SKIPPED: OpenCV not installed here. Run this on a machine with")
    print("  opencv-python before trusting any change to qrgen.py.")
else:
    det = cv2.QRCodeDetector()

    def render(matrix, quiet=4, px=8):
        n = len(matrix)
        img = np.full(((n + 2 * quiet) * px,) * 2, 255, np.uint8)
        for r in range(n):
            for c in range(n):
                if matrix[r][c]:
                    img[(r + quiet) * px:(r + quiet + 1) * px,
                        (c + quiet) * px:(c + quiet + 1) * px] = 0
        return img

    for text, ec in CASES:
        m = Q.encode(text, ec)
        got, _, _ = det.detectAndDecode(render(m))
        v = (len(m) - 17) // 4
        ok(f"opencv reads v{v}/{ec} {len(text)}B", got == text,
           f"got {got[:40]!r}")

    # And the reverse direction: this file's decoder must read a QR built by
    # OpenCV. That is what caught the format-order bug.
    try:
        enc = cv2.QRCodeEncoder_create()
        # Lowercase/mixed text so OpenCV picks BYTE mode. Uppercase-only
        # ASCII makes it choose ALPHANUMERIC mode, which this encoder does
        # not implement by design, so such a case would test nothing here.
        for text in ("https://forms.gle/kQkyUTGXMjGVnUq17",
                     "https://iuea.ac.ug/quiz", "cml3112 week 1"):
            arr = enc.encode(text)
            n = arr.shape[0]
            full = [[1 if arr[r][c] == 0 else 0 for c in range(n)]
                    for r in range(n)]
            # OpenCV includes a quiet zone in its output; strip it.
            rows = [r for r in range(n) if any(full[r])]
            cols = [c for c in range(n) if any(full[r][c] for r in range(n))]
            g = [row[cols[0]:cols[-1] + 1] for row in full[rows[0]:rows[-1] + 1]]
            try:
                got, _, _ = decode(g)
            except ValueError as e:
                if "byte mode" in str(e):
                    print(f"  note: OpenCV chose a non-byte mode for "
                          f"{text[:20]!r}, outside this encoder's scope")
                    continue
                raise
            ok(f"our decoder reads an OpenCV-built QR ({len(text)}B)",
               got == text, f"got {got[:40]!r}")
    except AttributeError:
        print("  note: this OpenCV build has no QR encoder, reverse check skipped")

print()
if FAILED:
    print(f"  {len(FAILED)} FAILED: {FAILED}")
    sys.exit(1)
print("  all checks passed")
