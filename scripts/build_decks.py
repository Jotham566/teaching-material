# -*- coding: utf-8 -*-
"""Build all 45 IUEA decks by running the five real deck builders.

WHY THIS FILE IS A WRAPPER
--------------------------
It used to BE a deck builder: an earlier implementation that produced weeks
1 to 4 for three cohorts, writing to exactly the same filenames as the
current decks. The README documented it as "all 45 decks", so the documented
command silently replaced twelve live decks with an older version of
themselves. An independent review on 2026-09-14 caught it.

The old implementation is in _quarantine/, which is gitignored, and this is
now what the README always claimed: a sequence of the five builders that
actually produce the current decks.

Each builder runs in its own process, because they share module-level state
in pptxkit (the lecturer-notes collector and the segment counter) and
importing them together would interleave it.
"""
import os
import subprocess
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)

BUILDERS = [
    ("build_week1.py", "Week 1, three cohorts"),
    ("build_w23.py", "Weeks 2 and 3"),
    ("build_w456.py", "Weeks 4, 5 and 6"),
    ("build_w78910.py", "Weeks 7 to 10"),
    ("build_w1115.py", "Weeks 11 to 15"),
]


def main():
    failed = []
    for script, what in BUILDERS:
        print("  {:<18} {}".format(script, what), flush=True)
        r = subprocess.run([sys.executable, os.path.join(_HERE, script)],
                           capture_output=True, text=True)
        if r.returncode != 0:
            failed.append(script)
            print("    FAILED:\n" + (r.stderr or r.stdout)[-1500:])

    decks = sorted(f for f in os.listdir(
        os.path.join(_ROOT, "IUEA_Teaching_Plan", "decks"))
        if f.endswith(".pptx") and not f.startswith("~$"))
    print("\n{} decks in IUEA_Teaching_Plan/decks/".format(len(decks)))
    if len(decks) != 45:
        print("*** expected 45 (15 weeks x 3 cohorts)")
        failed.append("deck count")

    print("\nNow run, in this order:")
    print("  python3 attach_qr.py            # QR codes back into the decks")
    print("  python3 build_teaching_guide.py # reads the lecturer notes")
    print("  python3 validation/overflow_scan.py")
    if failed:
        print("\nFAILED: " + ", ".join(failed))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
