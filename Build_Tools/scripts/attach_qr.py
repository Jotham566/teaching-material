# -*- coding: utf-8 -*-
"""Generate the quiz QR codes and put them in the decks.

INPUT   quiz_links.json — the map the Apps Script prints, keyed "CODE|WEEK":

          {
            "CML3112|1": "https://forms.gle/xxxxxxxx",
            "CML3113|1": "https://forms.gle/yyyyyyyy",
            ...
          }

OUTPUT  qr/quiz_CODE_WWW.png for every entry, then a full deck rebuild so each
        cohort's quiz slide carries that cohort's own code.

Any week missing from the file keeps the labelled placeholder square, so this
is safe to run when only some forms exist. Run it again as more are created.

    python3 attach_qr.py            generate and rebuild
    python3 attach_qr.py --check    report coverage without touching anything
    python3 attach_qr.py --demo     write a throwaway map of fake links, to
                                    prove the pipeline before real ones exist
"""
import io
import json
import os
import subprocess
import sys

import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_HERE)
sys.path.insert(0, _HERE)
import qrgen

BASE = _ROOT
SCRIPTS = _HERE
LINKS = os.path.join(BASE, "data", "quiz_links.json")
QRDIR = os.path.join(BASE, "qr")
CODES = ("CML3112", "CML3113", "CML3111")
WEEKS = (1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13)
BUILDERS = ["build_week1.py", "build_w23.py", "build_w456.py",
            "build_w78910.py", "build_w1115.py"]


def load():
    if not os.path.exists(LINKS):
        return {}
    with io.open(LINKS, encoding="utf-8") as fh:
        return json.load(fh)


def qr_path(code, week):
    return os.path.join(QRDIR, f"quiz_{code}_W{week:02d}.png")


def generate(links):
    os.makedirs(QRDIR, exist_ok=True)
    made, skipped = [], []
    for code in CODES:
        for wk in WEEKS:
            url = links.get(f"{code}|{wk}")
            if not url:
                skipped.append((code, wk))
                continue
            if not url.startswith(("http://", "https://")):
                raise ValueError(f"{code}|{wk} is not a URL: {url!r}")
            p = qr_path(code, wk)
            # level Q: a projected code gets photographed at an angle from the
            # back of a lecture room, so the extra error correction is worth
            # the slightly denser grid.
            #
            # quiet=8. The spec minimum is 4 and this was originally 2, which
            # was one of two reasons the first batch would not scan. It is 8
            # rather than 4 because at 4 an independent decoder failed on two
            # of the thirty-six codes; at 8 all thirty-six read cleanly. The
            # border is white space on a white card, so it costs nothing.
            qrgen.png(url, p, ec="Q", module_px=12, quiet=8)
            made.append((code, wk, url))
    return made, skipped


def report(links):
    print(f"link map: {len(links)} entries, {len(CODES) * len(WEEKS)} needed\n")
    print(f"{'week':>5}  " + "  ".join(f"{c:>9}" for c in CODES))
    for wk in WEEKS:
        cells = []
        for code in CODES:
            url = links.get(f"{code}|{wk}")
            cells.append("     yes " if url else "       — ")
        print(f"{wk:>5}  " + "  ".join(cells))
    missing = [(c, w) for c in CODES for w in WEEKS
               if not links.get(f"{c}|{w}")]
    print(f"\nmissing: {len(missing)} of {len(CODES) * len(WEEKS)}")
    return missing


def rebuild():
    for b in BUILDERS:
        r = subprocess.run([sys.executable, os.path.join(SCRIPTS, b)],
                           capture_output=True, text=True, cwd=SCRIPTS)
        if r.returncode != 0:
            print(f"  FAILED {b}\n{r.stderr[-1200:]}")
            return False
        print(f"  rebuilt {b}")
    return True


def demo():
    """A throwaway map, so the pipeline can be proven before Forms exist."""
    fake = {}
    for i, code in enumerate(CODES):
        for wk in WEEKS:
            fake[f"{code}|{wk}"] = (
                f"https://forms.gle/DEMO{code[-4:]}w{wk:02d}")
    path = os.path.join(BASE, "quiz_links.demo.json")
    with io.open(path, "w", encoding="utf-8") as fh:
        json.dump(fake, fh, indent=2)
    print(f"wrote {path} with {len(fake)} fake links")
    print("These are NOT real forms. They exist only to prove that the QR "
          "codes reach the right slide in the right deck.")
    return fake


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    if arg == "--check":
        report(load())
        sys.exit(0)
    if arg == "--demo":
        links = demo()
    else:
        links = load()
        if not links:
            print(f"No {LINKS}.\n\n"
                  "Run createAllForms() then printLinksJson() in the Apps "
                  "Script, save the JSON it logs as quiz_links.json, and run "
                  "this again. Or run with --demo to prove the pipeline with "
                  "fake links first.")
            sys.exit(1)

    made, skipped = generate(links)
    print(f"\ngenerated {len(made)} QR codes into qr/")
    for code, wk, url in made[:4]:
        print(f"   {code} W{wk:02d}  {url}")
    if len(made) > 4:
        print(f"   ... and {len(made) - 4} more")
    if skipped:
        print(f"{len(skipped)} weeks have no link yet and keep the placeholder")

    print("\nrebuilding the decks")
    if rebuild():
        print("\ndone. Each cohort's quiz slide now carries its own code.")
