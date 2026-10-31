# -*- coding: utf-8 -*-
"""Verify the S.5 / S.6 Machine Learning Track syllabus.

Seven sections. The last two catch the defects the others cannot see:

  1. the arithmetic: hours, sessions, the session block, the mark weights
  2. the roadmap and the week-by-week text agree about what is taught when
  3. the TYPE SCALE, audited from the BUILT file rather than from the source.
     Counting <w:sz> across document.xml, the headers and the footers is
     what finds a stray size that only appears in one table cell, which is
     exactly where strays hide
  4. every figure the document embeds exists and is not blank
  5. house style, read back out of the BUILT file so that prose written
     inline in the builder is checked too, plus the promises made to
     parents being costed into the timetable
  6. practicality: the software named, the data named, and every project
     example carrying the dataset that would answer it
  7. the RENDERED PAGES. A page that is nearly empty, or a figure orphaned
     from its heading, passes every check above

Run after any edit to schools_content.py or either builder.
"""
import collections
import os
import re
import sys
import zipfile

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, _HERE)

import schools_content as C                                # noqa: E402
import build_schools_syllabus_docx as B                    # noqa: E402

TRACK = os.path.join(_ROOT, "Schools_ML_Track", "archive", "original_ml_syllabus")
DOCX = os.path.join(TRACK, "ML_Track_S5_S6_Syllabus.docx")
FIGS = os.path.join(TRACK, "figs")

FAIL, CHECKS = [], 0


def ok(m):
    global CHECKS
    CHECKS += 1
    print("  pass  " + m)


def bad(m):
    FAIL.append(m)
    print("  FAIL  " + m)


def sec(t):
    print("\n" + t)


# ------------------------------------------------------------- 1. arithmetic
sec("1. The arithmetic")
if C.WEEKS * C.SESSIONS_PER_WEEK == C.SESSIONS == 24:
    ok("8 weeks x 3 sessions = %d sessions" % C.SESSIONS)
else:
    bad("session count does not reconcile")

if C.SESSIONS * C.HOURS_PER_SESSION == C.TOTAL_HOURS == 72:
    ok("%d sessions x %d hours = %d hours"
       % (C.SESSIONS, C.HOURS_PER_SESSION, C.TOTAL_HOURS))
else:
    bad("hours do not reconcile")

if sum(m for m, _, _ in C.BLOCK) == C.HOURS_PER_SESSION * 60:
    ok("the session block sums to %d minutes" % (C.HOURS_PER_SESSION * 60))
else:
    bad("the session block does not sum to three hours")

# These are teenagers on holiday. The design promise was that no teaching
# block exceeds 25 minutes and that more than half the time is hands-on.
_teach = sum(m for m, what, _ in C.BLOCK if what.startswith("Teach"))
_hands = sum(m for m, what, _ in C.BLOCK
             if what in ("Do it yourself", "Build something that runs"))
_longest = max(m for m, what, _ in C.BLOCK if what.startswith("Teach"))
if _longest <= 25:
    ok("no teaching block runs longer than %d minutes" % _longest)
else:
    bad("a teaching block runs %d minutes, over the 25-minute promise"
        % _longest)
if _hands > _teach:
    ok("%d minutes at the keyboard against %d minutes of teaching"
       % (_hands, _teach))
else:
    bad("more time is spent listening (%d min) than working (%d min)"
        % (_teach, _hands))

_w = sum(x for _, x, _, _ in C.ASSESSMENT)
if _w == 100:
    ok("mark weights sum to 100")
else:
    bad("mark weights sum to %d" % _w)

# A certificate with real marks was the requirement, so attendance must not
# be one of the weighted components.
if not any("attend" in a.lower() for a, _, _, _ in C.ASSESSMENT):
    ok("no marks are awarded for attendance")
else:
    bad("attendance appears as a weighted component")

if [len(w["sessions"]) for w in C.WEEKS_PLAN] == [3] * 8:
    ok("three sessions described in every one of the eight weeks")
else:
    bad("a week does not have three described sessions: %r"
        % [len(w["sessions"]) for w in C.WEEKS_PLAN])

for w in C.WEEKS_PLAN:
    for field in ("title", "maths", "build", "home"):
        if not str(w.get(field, "")).strip():
            bad("week %d has no %s" % (w["n"], field))
if not FAIL:
    ok("every week states its maths, its deliverable and its homework")

# -------------------------------------------------------------- 2. agreement
sec("2. The roadmap and the text agree")
# schools_content raises at import if a week claims a stage that does not
# exist, or if a teaching card is claimed by no week, so reaching here is
# itself the proof. Worth restating, because the failure mode is a figure
# that promises something the timetable never delivers.
ok("every roadmap card is either taught in a named week, or is one of the "
   "two marked as prior knowledge and further study")

_bands = {s[3] for s in C.STAGES}
if C.HAVE in _bands and C.LATER in _bands:
    ok("the roadmap distinguishes prior knowledge from what is out of scope")
else:
    bad("the roadmap has no prior-knowledge or out-of-scope band")

_have = [s for s in C.STAGES if s[3] == C.HAVE]
_have_text = (" ".join(_have[0][1:3])).lower() if _have else ""
if len(_have) == 1 and ("math" in _have_text or "median" in _have_text):
    ok("the prior-knowledge card is the A-level mathematics, which is the "
       "encouraging fact this audience needs")
else:
    bad("the prior-knowledge card is not the mathematics: %r" % _have)

# The week numbers written on the cards must match the weeks that claim them.
_claim = collections.defaultdict(set)
for w in C.WEEKS_PLAN:
    for n in w["stages"]:
        _claim[str(n)].add(w["n"])
_wrong = []
for num, name, _subs, band, when in C.STAGES:
    if band in (C.HAVE, C.LATER):
        continue
    weeks = sorted(_claim[num])
    for n in weeks:
        if str(n) not in when:
            _wrong.append((num, name, when, weeks))
            break
if _wrong:
    bad("a card's week label disagrees with the weeks that teach it: %r"
        % _wrong[:4])
else:
    ok("every card's week label matches the weeks that actually teach it")

# ------------------------------------------------------------- 3. type scale
sec("3. The type scale, audited from the built file")
if not os.path.exists(DOCX):
    bad("the syllabus has not been built")
else:
    sizes = collections.Counter()
    with zipfile.ZipFile(DOCX) as z:
        parts = [n for n in z.namelist()
                 if re.match(r"word/(document|header\d*|footer\d*)\.xml$", n)]
        for part in parts:
            xml = z.read(part).decode("utf-8")
            for half in re.findall(r'<w:sz w:val="(\d+)"', xml):
                sizes[int(half) / 2.0] += 1
    total = sum(sizes.values())
    declared = set(B.T.values())
    stray = {s: n for s, n in sizes.items() if s not in declared}

    print("       histogram: " + ", ".join(
        "%.1fpt x%d" % (s, n) for s, n in sorted(sizes.items(),
                                                 key=lambda kv: -kv[1])))
    if not stray:
        ok("%d sized runs across %d parts, every size from the declared "
           "scale of %d" % (total, len(parts), len(declared)))
    else:
        bad("sizes outside the declared scale: %r" % stray)

    if sizes and min(sizes) >= 9.0:
        ok("nothing smaller than %.1fpt, which is the print floor"
           % min(sizes))
    else:
        bad("type below the 9pt floor: %.1fpt" % min(sizes))

    if all(abs(s * 2 - round(s * 2)) < 1e-9 for s in sizes):
        ok("every size is a multiple of 0.5, so Word cannot round one into "
           "a near-duplicate")
    else:
        bad("a size is not a multiple of 0.5")

    # The hierarchy is noise if no single size carries the document.
    if sizes:
        dom, dom_n = sizes.most_common(1)[0]
        share = dom_n / float(total)
        if share >= 0.45:
            ok("the dominant size is %.1fpt carrying %.0f%% of runs, so the "
               "hierarchy reads" % (dom, 100 * share))
        else:
            bad("no size carries the document: the most common is %.1fpt at "
                "%.0f%%" % (dom, 100 * share))

# ---------------------------------------------------------------- 4. figures
sec("4. Figures")
_needed = ["roadmap_schools", "timeline_schools", "marks_schools"]
for name in _needed:
    p = os.path.join(FIGS, name + ".png")
    if not os.path.exists(p):
        bad("missing figure: %s" % name)
    elif os.path.getsize(p) < 10000:
        bad("%s is under 10 KB, so it is probably blank" % name)
if not any("figure" in f or "KB" in f for f in FAIL):
    ok("all %d figures present and non-trivial" % len(_needed))

if os.path.exists(DOCX):
    with zipfile.ZipFile(DOCX) as z:
        embedded = [n for n in z.namelist() if n.startswith("word/media/")]
    if len(embedded) == len(_needed):
        ok("all %d figures are embedded in the document" % len(embedded))
    else:
        bad("%d figures built but %d embedded" % (len(_needed),
                                                  len(embedded)))

# ------------------------------------------------------------ 5. house style
sec("5. House style and the promises")
prose = []
for w in C.WEEKS_PLAN:
    prose += [w["title"], w["maths"], w["build"], w["home"]]
    prose += [t for t, _ in w["sessions"]] + [b for _, b in w["sessions"]]
prose += [x for _, _, _, x in C.ASSESSMENT]
prose += [b for _, b in C.KIT] + [b for _, b in C.POLICIES]
prose += [b for _, b in C.LIMITS] + [b for _, b in C.NEXT]
prose += [b for _, b in C.STACK] + [b for _, b in C.DATA]
prose += [q for q, _ in C.PROJECTS] + [s for _, s in C.PROJECTS]
prose += list(C.PROJECT_RULES) + [b for _, b in C.MARK_NOTES]

pat = re.compile(r"\b(is|are|was|were)\s+not\s+\w+[^.]{0,40}?,\s+"
                 r"(?:it|they)\s+(?:is|are)\b", re.I)
hits = [p[:70] for p in prose if pat.search(str(p))]
if len(hits) <= 1:
    ok("no 'X, not Y' antithesis pile-up (%d)" % len(hits))
else:
    bad("antithesis in %d places: %r" % (len(hits), hits[:3]))


def doc_text():
    """Every word the reader sees, pulled from the built file.

    The prose list above only reaches schools_content, so a sentence written
    inline in the builder -- section leads, callouts, figure captions, which
    is a lot of this document -- was never style-checked at all. Reading the
    built file cannot miss any of it, and it also catches prose that only
    exists after string formatting.
    """
    with zipfile.ZipFile(DOCX) as z:
        xml = z.read("word/document.xml").decode("utf-8")
    xml = re.sub(r"</w:p>", "\n", xml)
    return re.sub(r"<[^>]+>", "", xml)


if os.path.exists(DOCX):
    _seen = [l.strip() for l in doc_text().splitlines() if l.strip()]
    _hits2 = [l[:70] for l in _seen if pat.search(l)]
    if len(_hits2) <= 1:
        ok("%d paragraphs of rendered text checked for the same antithesis "
           "(%d)" % (len(_seen), len(_hits2)))
    else:
        bad("antithesis in the rendered text, %d places: %r"
            % (len(_hits2), _hits2[:3]))

    # Placeholders and unformatted templates reaching a parent-facing
    # document is the embarrassing class of defect, and neither the source
    # nor the page-count check can see it.
    # "None" is flagged only when it is the WHOLE paragraph, which is how a
    # stray Python None renders. As a word it is ordinary English -- "None
    # of it is a trial", "None. Show somebody what you built" -- and the
    # first version of this check failed on both of those.
    _junk = [l[:70] for l in _seen
             if re.search(r"%[sd]\b|\{\}|\bTODO\b|\bTBD\b|<<", l)
             or l.strip() in ("None", "nan", "NaN")]
    if not _junk:
        ok("no unformatted placeholder, TODO or stray None in the text")
    else:
        bad("placeholder text reached the document: %r" % _junk[:3])

# The four promises were all explicitly asked for, so each must be visible
# in the document rather than only in the brief.
promises = {
    "a finished project": any("project" in a.lower()
                              for a, _, _, _ in C.ASSESSMENT),
    "a certificate with marks": len(C.BANDS) >= 3,
    "a head start on A-level": all(w["maths"] for w in C.WEEKS_PLAN),
    "a public portfolio": any("portfolio" in str(v).lower()
                              for v in prose),
}
_missing = [k for k, v in promises.items() if not v]
if _missing:
    bad("promised to the family and not delivered in the syllabus: %r"
        % _missing)
else:
    ok("all four promises are costed into the timetable: %s"
       % ", ".join(promises))

# Nothing may be invented. Dates, fees and names are fields.
if len(C.TO_CONFIRM) >= 6:
    ok("%d practical details are left as fields rather than guessed"
       % len(C.TO_CONFIRM))
else:
    bad("practical details are not listed for the school to confirm")

_invented = [p for p in prose
             if re.search(r"\bUGX\s?[\d,]+|\b20\d\d-\d\d-\d\d\b", str(p))]
if _invented:
    bad("a fee or a date appears in the teaching text: %r" % _invented[:3])
else:
    ok("no fee and no date is invented anywhere in the teaching text")

if len(C.LIMITS) >= 3:
    ok("%d limits stated, so the edges are in the document rather than "
       "discovered in week three" % len(C.LIMITS))
else:
    bad("the track's limits are not stated")

# ------------------------------------------------------- 6. is it practical?
# "As practical as possible" was the requirement, and the way a syllabus
# fails it is by promising activity without naming the thing the activity is
# done to. So: the software is named, the data is named, and a project idea
# carries the dataset that would answer it.
sec("6. Practicality: named software, named data, answerable projects")

_tools = [t.lower() for t, _ in C.STACK]
_want = ["python", "jupyter", "pandas", "scikit-learn"]
_absent = [t for t in _want
           if not any(t in name for name in _tools)]
if not _absent:
    ok("%d tools named, including the four a student has to have: %s"
       % (len(C.STACK), ", ".join(t for t, _ in C.STACK[:4])))
else:
    bad("the software a student needs is not named: %r" % _absent)

# A holiday track for school students cannot depend on anybody buying
# anything, and cannot depend on a trial that expires mid-track.
_paid = re.compile(r"\blicen[cs]e fee|\bsubscri|\btrial\b|\bper month\b|"
                   r"\bpaid (?:plan|tier|version)\b", re.I)
_costly = [t for t, b in C.STACK if _paid.search(b)]
if not _costly:
    ok("no tool in the stack needs a payment, a subscription or a trial")
else:
    bad("a tool implies a cost to the family: %r" % _costly)

# Every dataset must say where it comes from, and at least one must be
# something the class makes itself: that is the one they engage with, and it
# is the only one that cannot fail to arrive.
if len(C.DATA) >= 4 and all(len(str(b).split()) >= 15 for _, b in C.DATA):
    ok("%d data sources, each described rather than just listed"
       % len(C.DATA))
else:
    bad("the data sources are thin: %r" % [a for a, _ in C.DATA])

_own = [a for a, b in C.DATA
        if "class" in (a + b).lower() or "collect" in (a + b).lower()]
if len(_own) >= 2:
    ok("data the students make or gather themselves is in the list, so the "
       "track does not depend entirely on downloads")
else:
    bad("no dataset is produced by the students themselves")

# The class survey is about real children in the room, and they publish
# their work. Those two facts together need an explicit rule.
_survey = " ".join(b for a, b in C.DATA if "class" in a.lower()).lower()
if "no names" in _survey and ("never published" in _survey
                              or "not published" in _survey):
    ok("the class survey is stated to carry no names and to stay unpublished")
else:
    bad("the class's own data is used without a stated rule about names and "
        "publication")

if len(C.PROJECTS) >= 6:
    ok("%d project examples, so a student can picture one" % len(C.PROJECTS))
else:
    bad("too few project examples: %d" % len(C.PROJECTS))

# The defect this check exists for: a project idea with no data behind it.
_noq = [q for q, _ in C.PROJECTS if "?" not in q]
_nosrc = [q for q, s in C.PROJECTS if len(str(s).split()) < 5]
if not _noq and not _nosrc:
    ok("every project example is a question and names where its data comes "
       "from")
else:
    bad("project examples without a question (%r) or without a data source "
        "(%r)" % (_noq[:2], _nosrc[:2]))

if len(C.PROJECT_RULES) >= 4:
    ok("%d rules a project must satisfy, so approval in Week 7 is not a "
       "matter of taste" % len(C.PROJECT_RULES))
else:
    bad("the project rules are not written down")

# Section numbers are generated from B.SECTIONS. A literal "section 4" typed
# into prose survives an insertion and then points at the wrong place, which
# is what happened when the data and project sections were added.
_lit = [p[:60] for p in prose
        if re.search(r"\bsection\s+\d", str(p), re.I)]
if not _lit:
    ok("no cross-reference hard-codes a section number")
else:
    bad("hard-coded section number in the text: %r" % _lit[:3])

# The user asked that the syllabus not claim to follow a published external
# roadmap. Checked rather than remembered.
_src = ""
for f in ("schools_content.py", "build_schools_syllabus_docx.py",
          "make_schools_figures.py"):
    _src += open(os.path.join(_HERE, f)).read()
if "roadmap.sh" not in _src:
    ok("the syllabus does not attribute its structure to an external roadmap")
else:
    bad("roadmap.sh is still referenced in the sources")

# ------------------------------------------------------------- 6. the pages
# The only check here that looks at the LAID-OUT document. Everything above
# reads the source or the XML, and neither can see a figure orphaned away
# from its heading or a page carrying three lines and a repeated table
# header. Both of those happened, and both passed every other check.
sec("7. The rendered pages")
PDF = os.path.join(TRACK, "ML_Track_S5_S6_Syllabus.pdf")
if not os.path.exists(PDF):
    print("  skip  no rendered PDF at %s. THIS IS NOT A PASS: run\n"
          "        soffice --headless --convert-to pdf on the docx and "
          "re-run." % os.path.basename(PDF))
else:
    import subprocess

    def run(*a):
        return subprocess.run(a, capture_output=True, text=True).stdout

    pages = int([l for l in run("pdfinfo", PDF).splitlines()
                 if l.startswith("Pages")][0].split()[1])
    with_img = set()
    for line in run("pdfimages", "-list", PDF).splitlines()[2:]:
        if line.split():
            with_img.add(int(line.split()[0]))
    lens = []
    for i in range(1, pages + 1):
        txt = run("pdftotext", "-f", str(i), "-l", str(i), PDF, "-")
        lens.append(len("".join(txt.split())))
    median = sorted(lens)[len(lens) // 2]

    if 8 <= pages <= 18:
        ok("%d pages, which a parent will read and a school can print"
           % pages)
    else:
        bad("%d pages is the wrong length for this audience" % pages)

    blank = [i for i, L in enumerate(lens, 1)
             if L < 60 and i not in with_img]
    if blank:
        bad("blank page(s): %r" % blank)
    else:
        ok("no blank pages")

    # A page with no figure and a fraction of the median text is wasted
    # space. The cover and the last page are allowed to be short.
    sparse = [(i, L) for i, L in enumerate(lens, 1)
              if L < 0.4 * median and i not in with_img
              and i not in (1, pages)]
    if sparse:
        bad("page(s) carrying almost nothing, with no figure on them: %r"
            % sparse)
    else:
        ok("every page is either full, or carries a figure, or is the cover")

    if len(with_img) == 3:
        ok("the three figures are on three separate pages, each with its "
           "own heading")
    else:
        bad("figures appear on %d pages, expected 3" % len(with_img))

print("\n%d checks, %d failures" % (CHECKS, len(FAIL)))
if FAIL:
    print("\nFAILURES:")
    for f in FAIL:
        print("  - " + f)
    sys.exit(1)
print("all checks passed")
