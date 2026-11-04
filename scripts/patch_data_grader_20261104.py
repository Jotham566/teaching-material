"""Audit patch of 4 November 2026 (stale-statement sweep): data, grader text, submission scripts and two link indexes.

Brings these files in step with the 4 November decision (Engineering ML project = INDIVIDUAL, TIMED 3-hour Colab sitting in Week 12, fully
AUTO-GRADED, Part A /30 + Part B /15; no demo, no clinic, no take-home, no Practical Test 2, no upload form):

  data/assessments.json                         ML_PROJECT (3 rows) and DEMO delivery notes
  data/iuea_assignment_form_briefs.json         ML_PROJECT / DEMO / TEST2 student briefs (9 rows)
  grader/concise_assignment_briefs.gs           regenerated from the briefs (pure ASCII)
  grader/submission_forms.gs                    embedded registry rows for TEST2, ML_PROJECT, DEMO (pure ASCII)
  student_guides/<cohort>/TEST2.md, DEMO.md     two stale sentences each
  Assignment_Submission_Links.md, Assignment_Instructions_Index.md
  grader/README.md, gradebook.gs (comments only), continuous_assessment.py (comment only)
  tests/test_continuous_assessment.py           the project row check (sitting instead of a due date)

Rules: every original is copied once into a sibling _backup_2026-11-04 folder (or <name>.pre_audit if that name is taken); every replacement
asserts its match count; running twice changes nothing. Usage: python3 scripts/patch_data_grader_20261104.py
"""
import json, re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "IUEA_Teaching_Plan"
BK = "_backup_2026-11-04"
CODES = ("CML3111", "CML3112", "CML3113")
SIT = {"CML3112": ("2026-12-01", "11:00", "14:00", "Tuesday 1 December 2026", "Tue 1 Dec"),
       "CML3113": ("2026-12-04", "08:00", "11:00", "Friday 4 December 2026", "Fri 4 Dec"),
       "CML3111": ("2026-12-04", "11:00", "14:00", "Friday 4 December 2026", "Fri 4 Dec")}
changed = []


def backup(p):
    p = Path(p); d = p.parent / BK; d.mkdir(exist_ok=True)
    dest = d / p.name
    if dest.exists():
        dest = d / (p.name + ".pre_audit")
    if not dest.exists():
        shutil.copy2(p, dest)


def write(p, text, enc="utf-8"):
    p = Path(p)
    if p.read_text(encoding=enc) != text:
        backup(p); p.write_text(text, encoding=enc); changed.append(str(p.relative_to(ROOT)))


def rep(t, old, new, n=1, where=""):
    c = t.count(old)
    if c == 0 and new in t:
        return t          # already patched
    assert c == n, f"{where}: expected {n} of {old[:70]!r}, found {c}"
    return t.replace(old, new)


# ---------------------------------------------------------------- 1. student guides TEST2 / DEMO (retired notices)
def patch_guides():
    for c in CODES:
        p = BASE / "student_guides" / c / "TEST2.md"; t = p.read_text()
        t = t.replace("The semester now ends at Week 12 with a short project demo, and the weights have changed",
                      "The semester now ends at Week 12 with the Engineering ML project, a timed individual sitting (no demo), and the weights have changed")
        assert "short project demo" not in t, p
        write(p, t)
        p = BASE / "student_guides" / c / "DEMO.md"; t = p.read_text()
        d = SIT[c]
        if "there is no demo and the 15 December date no longer applies" in t:
            continue
        t = rep(t, "The semester now ends at Week 12 (demo day Tuesday 1 December); the 15 December date no longer applies." if c == "CML3112" else
                re.search(r"The semester now ends at Week 12 \(demo day [^)]*\); the 15 December date no longer applies\.", t).group(0),
                f"The semester now ends at Week 12 (project sitting {d[3].split(' 2026')[0]}, proposed); there is no demo and the 15 December date no longer applies.", where=str(p))
        write(p, t)


# ---------------------------------------------------------------- 2. data/assessments.json
def project_notes(code):
    d = SIT[code]
    return (f"Individual, timed and fully auto-graded Engineering ML project: one supervised 3-hour sitting in Google Colab in the Week 12 class slot, entered and submitted like Practical Test 1 "
            f"(update of 4 November 2026; there is no take-home and no demo). One notebook with two parts: Part A coded project notebook (30), Part B decision memo form inside the notebook (15). "
            f"Covers Weeks 1 to 11 only. Proposed sitting (lecturer to confirm): {d[3]} {d[1]} to {d[2]} Kampala. Unmarked rehearsal released after Class 4. "
            f"It is collected by the Colab test collector under the key {code}|ML_PROJECT (second_half/Project/deploy), not by an upload form in the submission project: keep this entry's upload form closed. "
            f"opens_at and closes_at stay null until the lecturer sets the Test windows row.")


def patch_assessments():
    p = ROOT / "data/assessments.json"; rows = json.loads(p.read_text()); pol = json.loads((ROOT / "data/assessment_blocks_20261103.json").read_text())["engineering_ml_project"]
    n = 0
    for r in rows:
        c = r["cohort"]
        if r["id"] == "ML_PROJECT":
            sl = pol["sitting"]["slots"][c]
            r["formats"] = ["ipynb"]; r["grading"] = "automatic"
            r["status"] = "SITTING_TO_BE_CONFIRMED"
            r["delivery_note"] = project_notes(c)
            r["mode"] = "individual, timed (180 minutes), fully auto-graded"
            for part in r["parts"]:
                if part["part"] == "B": part["title"] = "Structured decision memo (a form inside the notebook)"
                part["marking"] = ("Fully automatic: hidden checks on unseen data (24) and automatic process checks (6)." if part["part"] == "A"
                                   else "Fully automatic: the memo form inside the notebook, marked by key and keyword and length rules (15).")
            r["scope"] = "Only what was taught this semester, Weeks 1 to 11 (Classes 1 to 4 of the second half included)."
            r.pop("proposed_closes_at", None)
            r["proposed_sitting"] = dict(date=sl["date"], start=sl["start"], end=sl["end"], timezone="Africa/Kampala", duration_minutes=180)
            r["proposed_status"] = "proposed, lecturer to confirm"
            n += 1
        elif r["id"] == "DEMO":
            old = r["delivery_note"]
            r["delivery_note"] = old.replace("Week 12 is a project clinic.", "Week 12 is the individual timed project sitting; nobody presents.")
            assert "clinic" not in r["delivery_note"]; n += 1
        elif r["id"] == "TEST2":
            assert r.get("retired") is True
    assert n == 6, n
    write(p, json.dumps(rows, indent=2, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------- 3. briefs (iuea_assignment_form_briefs.json, concise_assignment_briefs.gs)
def brief_project(code):
    d = SIT[code]
    return (f"{code} ML_PROJECT — Engineering ML project (one timed sitting)\n\nWHAT TO UPLOAD\n\nNothing is uploaded to this page. The project is one individual, timed 3-hour sitting in Google Colab. "
            f"You hand in ONE notebook with the memo form inside it, using the Submit your test cell and the test form, as in Practical Test 1.\n\nWHERE TO DO THE WORK\n\n"
            f"Use the entry link your lecturer gives you on the day: {d[3]}, {d[1]} to {d[2]} Kampala (proposed, lecturer to confirm). Your 3 hours start when you press Start.\n\n"
            f"BEFORE SUBMITTING\n\nPart A is the coded notebook (30 marks) and Part B the decision memo (15 marks); both are marked automatically. No AI or outside help. Allow 20 minutes to submit. Enter your own Student Registration Number exactly as on your university record.\n\n"
            f"NEED HELP?\n\nRead student_guides/{code}/ML_PROJECT.md, or ask the lecturer. If access fails, keep your work and contact the lecturer.")


def brief_retired(code, aid):
    what = "Practical Test 2" if aid == "TEST2" else "the demo"
    why = ("The semester now ends at Week 12, so there is no Practical Test 2." if aid == "TEST2"
           else "There is no demo this semester. Week 12 is the Engineering ML project sitting and nobody presents.")
    return (f"{code} {aid} — RETIRED\n\nWHAT TO UPLOAD\n\nNothing. This form is retired and stays closed: {why}\n\nWHERE TO DO THE WORK\n\n"
            f"Nothing to do for {what}. The Engineering ML project is a timed individual sitting; read student_guides/{code}/ML_PROJECT.md.\n\n"
            f"NEED HELP?\n\nAsk the lecturer.")


def ascii_js(s):
    """Escape every non-ASCII character as a JS/JSON \\uXXXX escape (valid inside string literals)."""
    out = []
    for ch in s:
        o = ord(ch)
        if o < 128: out.append(ch)
        elif o < 0x10000: out.append("\\u%04x" % o)
        else:
            o -= 0x10000; out.append("\\u%04x\\u%04x" % (0xD800 + (o >> 10), 0xDC00 + (o & 0x3FF)))
    return "".join(out)


def patch_briefs():
    p = ROOT / "data/iuea_assignment_form_briefs.json"; d = json.loads(p.read_text())
    for c in CODES:
        d[f"{c}|ML_PROJECT"] = dict(brief=brief_project(c), maximum=45)
        d[f"{c}|DEMO"] = dict(brief=brief_retired(c, "DEMO"), maximum=d[f"{c}|DEMO"]["maximum"])
        d[f"{c}|TEST2"] = dict(brief=brief_retired(c, "TEST2"), maximum=d[f"{c}|TEST2"]["maximum"])
    write(p, json.dumps(d, ensure_ascii=False, indent=2) + "\n")
    g = BASE / "grader/concise_assignment_briefs.gs"; t = g.read_text(encoding="utf-8")
    head = "// Generated by build_assignment_instructions.py. IUEA only.\n// Rows for TEST2, DEMO and ML_PROJECT were updated by scripts/patch_data_grader_20261104.py (do not regenerate with the old build script).\nvar IUEA_CONCISE_BRIEFS = "
    if not t.startswith("// Generated by build_assignment_instructions.py. IUEA only.\n"): raise SystemExit("unexpected header in concise_assignment_briefs.gs")
    new = head + ascii_js(json.dumps(d, ensure_ascii=False, separators=(",", ":"))) + ";\n"
    assert new.encode("ascii") and new.endswith(";\n")
    write(g, new)


# ---------------------------------------------------------------- 4. submission_forms.gs embedded registry (surgical)
def patch_submission_forms():
    g = BASE / "grader/submission_forms.gs"; s = g.read_text(encoding="utf-8")
    a = s.index("var ASSESSMENTS = ") + len("var ASSESSMENTS = "); b = s.index("\n", a)
    assert s[b - 1] == ";"
    reg = json.loads(s[a:b - 1]); by = {r["key"]: r for r in reg}
    new = {r["key"]: r for r in json.loads((ROOT / "data/assessments.json").read_text())}
    briefs = json.loads((ROOT / "data/iuea_assignment_form_briefs.json").read_text())
    guides = {}
    for k in by:
        r = by[k]
        if r["id"] in ("TEST2", "ML_PROJECT", "DEMO"):
            src = dict(new[k]); src["brief"] = (BASE / "student_guides" / r["cohort"] / (r["id"] + ".md")).read_text()
            by[k].clear(); by[k].update(src)
    out = "var ASSESSMENTS = " + ascii_js(json.dumps(reg, ensure_ascii=False, separators=(",", ":"))) + ";"
    s2 = s[:a - len("var ASSESSMENTS = ")] + out + s[b:]
    if "COLLECTION ONLY \u2014 GRADING HELD" in s2:
        s2 = rep(s2, "COLLECTION ONLY \u2014 GRADING HELD", "COLLECTION ONLY \\u2014 GRADING HELD", where="submission_forms.gs")
    assert all(ord(c) < 128 for c in s2)
    write(g, s2)


# ---------------------------------------------------------------- 5. markdown indexes
PROJ_OPEN = "rehearsal after Class 4 (proposed)"
def patch_links():
    p = BASE / "Assignment_Submission_Links.md"; t = p.read_text()
    if "**Update of 4 November 2026:**" in t:
        return patch_index()
    t = rep(t, "The project and the practical test remain held pending complete grading validation.",
            "The Engineering ML project is not an upload form: it is a timed individual sitting that needs the portal and collector deployed. There is no second practical test.", where=str(p))
    t = rep(t, "The Engineering ML project is submitted as a take-home (Part A notebook, 30 marks; Part B one-page memo, 15 marks), proposed due Friday 11 December 2026, 23:59 Kampala (proposed, lecturer to confirm). Its form stays closed until the lecturer sets a window.",
            "**Update of 4 November 2026:** the Engineering ML project is an individual, timed, auto-graded sitting of 3 hours in Google Colab in the Week 12 class slot (Part A coded notebook, 30 marks; Part B decision memo form inside the notebook, 15 marks), entered and submitted like Practical Test 1. Proposed sittings (lecturer to confirm): CML3112 Tue 1 Dec 11:00 to 14:00, CML3113 Fri 4 Dec 08:00 to 11:00, CML3111 Fri 4 Dec 11:00 to 14:00. No upload form is used and none is open; the table rows below show the sitting.", where=str(p))
    t, n = re.subn(r"(?m)^\| ML_PROJECT: Engineering ML project \(Part A notebook /30, Part B memo /15\) \| after Class 4 \(proposed, lecturer to confirm\) \| Fri 11 Dec 2026 23:59 \(proposed, lecturer to confirm\) \| \[Submit\]\([^)]*\) \|$",
                   lambda m: "@@", t)
    assert n == 3, n
    sit = iter([SIT[c] for c in CODES])
    def fill(m):
        d = next(sit)
        return (f"| ML_PROJECT: Engineering ML project (individual, timed 3-hour sitting; Part A /30, Part B /15) | rehearsal after Class 4 (proposed) | sitting {d[4]} {d[1]} to {d[2]} (proposed, lecturer to confirm) | no upload form: entry link issued on the day |")
    t = t.replace("@@", "@@")  # no-op, keeps the intent explicit
    t = re.sub(r"(?m)^@@$", fill, t)
    t, n = re.subn(r"(?m)^\| DEMO: RETIRED on 3 November 2026 \(no demo\) \| retired \| retired \| \[Submit\]\([^)]*\) \|$",
                   "| DEMO: RETIRED on 3 November 2026 (no demo) | retired | retired | retired (form closed) |", t)
    assert n == 3, n
    write(p, t)
    patch_index()


def patch_index():
    p = BASE / "Assignment_Instructions_Index.md"; t = p.read_text()
    if "a timed individual sitting in Week 12" in t:
        return
    t = rep(t, "the Engineering ML project is submitted, Part A /30 and Part B /15; the 2 November note is superseded)",
            "the Engineering ML project is a timed individual sitting in Week 12, Part A /30 and Part B /15, both automatic; the 2 November note is superseded)", where=str(p))
    write(p, t)


# ---------------------------------------------------------------- 6. grader README, gradebook.gs comments, continuous_assessment.py comment
def patch_grader_text():
    p = BASE / "grader/README.md"; t = p.read_text()
    t = rep(t, "The same command can grade the Part B decision memo once its rubric exists.)",
            "The Part B decision memo is graded by the project grader in `second_half/Project/grader_spec/grade_project.py`, not by this command.)", where=str(p))
    t = rep(t, "Take-home, Weeks 1 to 11 only. Due date proposed Friday 11 December 2026 23:59 Kampala, lecturer to confirm |",
            "Individual, timed 3-hour Colab sitting in the Week 12 class slot (proposed: CML3112 Tue 1 Dec, CML3113 and CML3111 Fri 4 Dec; lecturer to confirm), fully automatic, Weeks 1 to 11 only; graded by `second_half/Project/grader_spec/grade_project.py` |", where=str(p))
    t = rep(t, "both practical tests and both major projects.", "Practical Test 1 (Practical Test 2 is retired) and the major projects (the DA project and the Engineering ML project; the ML project sitting is now built in `../second_half/Project/`, and `assessment_banks/ML_PROJECT` is the superseded older bank).", where=str(p))
    t = rep(t, "Both exams, both major IUEA projects, DEMO, S13 and S15 remain held for incomplete assessment coverage.",
            "(Audit of 21 October 2026, kept as a record.) At that date both exams, both major IUEA projects, DEMO, S13 and S15 were held for incomplete assessment coverage. Practical Test 2 and DEMO are since retired; the ML project sitting is graded by `second_half/Project/grader_spec/grade_project.py`.", where=str(p))
    write(p, t)
    p = BASE / "grader/gradebook.gs"; t = p.read_text(encoding="utf-8")
    t = rep(t, " * The Engineering ML project stays: students SUBMIT it (take-home, graded like Practical Test 1) and it covers Weeks 1 to 11.",
            " * The Engineering ML project stays: one individual, timed 3-hour Colab sitting in Week 12 (like Practical Test 1), fully auto-graded, Weeks 1 to 11 only.", where=str(p))
    t = rep(t, "Part A coded project notebook /30 (auto-graded plus rubric, like Test 1)", "Part A coded project notebook /30 (fully automatic)", where=str(p))
    t = rep(t, "+ Part B one-page decision memo /15 (rubric). Two columns.", "+ Part B decision memo form /15 (fully automatic). Two columns.", where=str(p))
    t = rep(t, "// marks for the coded project notebook (auto-graded plus rubric, like Practical Test 1)", "// marks for the coded project notebook (fully automatic)", where=str(p))
    t = rep(t, "// marks for the one-page decision memo (rubric)", "// marks for the decision memo form (fully automatic)", where=str(p))
    write(p, t, "utf-8")
    p = BASE / "grader/continuous_assessment.py"; t = p.read_text()
    t = rep(t, "# The Engineering ML project is a take-home submission graded like Practical Test 1: Part A coded notebook /30 + Part B decision memo /15.",
            "# The Engineering ML project is an individual, timed, fully auto-graded Colab sitting (Week 12) like Practical Test 1: Part A coded notebook /30 + Part B decision memo form /15.", where=str(p))
    write(p, t)


# ---------------------------------------------------------------- 7. test follows the data
def patch_test():
    p = ROOT / "tests/test_continuous_assessment.py"; t = p.read_text()
    old = "   self.assertEqual(m['proposed_closes_at'],pol['engineering_ml_project']['due']['all_cohorts']);self.assertIn('proposed',m['proposed_status'])\n"
    new = ("   sl=pol['engineering_ml_project']['sitting']['slots'][code];self.assertNotIn('proposed_closes_at',m);self.assertEqual((m['proposed_sitting']['date'],m['proposed_sitting']['start'],m['proposed_sitting']['end']),(sl['date'],sl['start'],sl['end']));self.assertIn('proposed',m['proposed_status'])\n"
           "   self.assertEqual(m['grading'],'automatic');self.assertEqual(m['formats'],['ipynb']);self.assertNotIn('take-home',m['delivery_note'].lower().replace('no take-home',''))\n")
    t = rep(t, old, new, where=str(p))
    write(p, t)


def main():
    patch_guides(); patch_assessments(); patch_briefs(); patch_submission_forms(); patch_links(); patch_grader_text(); patch_test()
    print("changed:", *changed, sep="\n  ") if changed else print("nothing to change (already patched)")


if __name__ == "__main__":
    main()
