#!/usr/bin/env python3
"""Patch stale statements in the IUEA ML teaching Word documents (4 Nov 2026).

Why: the semester now ends at Week 12. Weeks 8 to 11 are four classes (concepts
first, then a lab) and Week 12 is an individual, timed, auto-graded Engineering
ML project sitting. Practical Test 2, Demo Day, viva, reflection, Weeks 13 to 15
and the team ML project are gone. This script edits only the stale statements in:

  IUEA_Teaching_Plan/IUEA_ML_Lecturer_Teaching_Guide_W1-W15.docx   (Weeks 8-15 replaced)
  IUEA_Teaching_Plan/IUEA_ML_Beginner_Teaching_Quick_Guide.docx
  IUEA_Teaching_Plan/IUEA_ML_Roadmap_Benchmark.docx
  IUEA_Teaching_Plan/IUEA_ML_Week1_PreFlight_Checklist.docx
  IUEA_Teaching_Plan/IUEA_ML_Student_Setup_Guide.docx
  IUEA_Teaching_Plan/IUEA_ML_Assessment_Technology_Build_Plan.docx
  IUEA_Teaching_Plan/test_operations/Student_Colab_Test_Guide.docx
  IUEA_Teaching_Plan/test_operations/Test_Grading_Checklist.docx

Not changed (nothing stale): IUEA_ML_Quick_Class_Checklist.docx,
IUEA_ML_Platform_Architecture_Note.docx.

Rules: a file is backed up to a sibling folder _backup_2026-11-04 before its first
change (if a file of that name is already there, the copy is saved as
<name>.pre_audit; an existing backup is never overwritten). Every replacement
asserts its occurrence count. The script is idempotent: a file that is already
patched is left untouched (no backup, no save).

Run:  python3 patch_stale_docx_20261104.py [repo_root]
"""
import copy
import os
import shutil
import sys

import docx
from docx.oxml.ns import qn

W_P, W_T = qn("w:p"), qn("w:t")
XML_SPACE = "{http://www.w3.org/XML/1998/namespace}space"
BACKUP_DIR = "_backup_2026-11-04"


# ---------------------------------------------------------------- helpers
def roots(document):
    """All XML roots that hold text: body, headers, footers (deduplicated)."""
    out, seen = [document.element.body], set()
    for s in document.sections:
        for part in (s.header, s.footer, s.first_page_header, s.first_page_footer,
                     s.even_page_header, s.even_page_footer):
            if part.is_linked_to_previous:  # no own definition; do not create one
                continue
            el = part._element
            if id(el) not in seen:
                seen.add(id(el))
                out.append(el)
    return out


def ptext(p):
    return "".join(t.text or "" for t in p.iter(W_T))


def all_paras(document):
    for r in roots(document):
        for p in r.iter(W_P):
            yield p


def _sub_in_para(p, old, new):
    """Replace every occurrence of old in paragraph p across w:t elements."""
    n = 0
    while True:
        ts = list(p.iter(W_T))
        joined = "".join(t.text or "" for t in ts)
        s = joined.find(old)
        if s < 0:
            return n
        e = s + len(old)
        pos, first = 0, True
        for t in ts:
            txt = t.text or ""
            a, b = pos, pos + len(txt)
            pos = b
            if b <= s or a >= e:
                continue
            ls, le = max(s, a) - a, min(e, b) - a
            if first:
                t.text = txt[:ls] + new + txt[le:]
                first = False
            else:
                t.text = txt[:ls] + txt[le:]
            t.set(XML_SPACE, "preserve")
        n += 1
        if new and old in new:  # avoid infinite loops on self-containing text
            return n


def rep(document, old, new, expected=1):
    """Replace old by new; assert the count. Already-patched text is skipped."""
    if old in new and any(new in ptext(p) for p in all_paras(document)):
        return 0  # already patched
    found = sum(ptext(p).count(old) for p in all_paras(document))
    if found == 0:
        have_new = any(new in ptext(p) for p in all_paras(document))
        assert have_new, "neither old nor new text found: %r" % old[:80]
        return 0
    assert found == expected, "expected %d of %r, found %d" % (expected, old[:80], found)
    done = 0
    for p in list(all_paras(document)):
        if old in ptext(p):
            done += _sub_in_para(p, old, new)
    assert done == expected
    return done


def rep_par(document, old_full, new_full):
    """Replace a paragraph whose whole text equals old_full."""
    hits = [p for p in all_paras(document) if ptext(p) == old_full]
    if not hits:
        assert any(ptext(p) == new_full for p in all_paras(document)), old_full[:80]
        return 0
    assert len(hits) == 1, (old_full[:60], len(hits))
    set_text(hits[0], new_full)
    return 1


def set_text(p, text):
    """Set paragraph text, keeping the first run's formatting."""
    ts = list(p.iter(W_T))
    ts[0].text = text
    ts[0].set(XML_SPACE, "preserve")
    for t in ts[1:]:
        t.text = ""


def style_of(p):
    ps = p.find(qn("w:pPr"))
    if ps is not None and ps.find(qn("w:pStyle")) is not None:
        return ps.find(qn("w:pStyle")).get(qn("w:val"))
    return ""


def body_paras(document):
    return [e for e in document.element.body.iterchildren() if e.tag == W_P]


def find_para(document, text, style=None, startswith=False):
    for p in body_paras(document):
        t = ptext(p)
        if (t.startswith(text) if startswith else t == text) and (style is None or style_of(p) == style):
            return p
    return None


def remove(el):
    el.getparent().remove(el)


def backup_then_save(document, path, original_bytes):
    d = os.path.join(os.path.dirname(path), BACKUP_DIR)
    os.makedirs(d, exist_ok=True)
    name = os.path.basename(path)
    target = os.path.join(d, name)
    if os.path.exists(target):
        target = target + ".pre_audit"
    if os.path.exists(target):
        raise RuntimeError("backups already exist for " + name + "; refusing to overwrite")
    with open(target, "wb") as f:
        f.write(original_bytes)
    document.save(path)
    return target


def process(path, fn):
    with open(path, "rb") as f:
        original = f.read()
    document = docx.Document(path)
    before = [ptext(p) for p in all_paras(document)]
    fn(document)
    after = [ptext(p) for p in all_paras(document)]
    if before == after:
        print("unchanged (already patched):", os.path.basename(path))
        return
    target = backup_then_save(document, path, original)
    print("patched:", os.path.basename(path), "| backup:", target)


# ---------------------------------------------------------------- lecturer guide
def new_par(tpl, text, label=None):
    """Copy a template paragraph; optional bold label run then the text."""
    p = copy.deepcopy(tpl)
    runs = p.findall(qn("w:r"))
    for r in runs[1:]:
        p.remove(r)
    r0 = runs[0]
    for child in list(r0):
        if child.tag != qn("w:rPr"):
            r0.remove(child)
    def add_t(run, s):
        t = run.makeelement(W_T, {})
        t.text = s
        t.set(XML_SPACE, "preserve")
        run.append(t)
    if label:
        lab = copy.deepcopy(r0)
        rpr = lab.find(qn("w:rPr"))
        b = rpr.find(qn("w:b")) if rpr is not None else None
        if b is not None:
            for k in list(b.attrib):
                del b.attrib[k]
        add_t(lab, label + " ")
        p.append(lab)
        r0.getparent().remove(r0)
        p.append(r0)
        add_t(r0, text)
    else:
        add_t(r0, text)
    return p


def make_heading(tpl, style, text):
    p = copy.deepcopy(tpl)
    for r in p.findall(qn("w:r")):
        p.remove(r)
    ppr = p.find(qn("w:pPr"))
    ppr.find(qn("w:pStyle")).set(qn("w:val"), style)
    r = p.makeelement(qn("w:r"), {})
    t = r.makeelement(W_T, {})
    t.text = text
    r.append(t)
    p.append(r)
    return p


NEW_W811 = "Weeks 8 to 11 — four classes, concepts first, then the lab"
NEW_W12 = "Week 12 — Engineering ML project sitting (individual, timed, auto-graded)"

CLASSES = [
    ("Class 1 — Your first model (Week 8 content)",
     "CML3112 Tuesday 3 November (Room 106); CML3113 Friday 6 November, 08:00 (Room 105); CML3111 Friday 6 November, 11:00 (Room 115).",
     "For the Friday cohorts this class is a recap of the concepts followed by a long lab, because they had the Week 8 theory on Friday 30 October without the lab.",
     "Features and target; a baseline; error, MAE and RMSE; gradient descent in plain words; hidden rows (train, validation and test, split by equipment group); filling blanks from training rows only; a line and a tree; the scoreboard.",
     "Each student fits a baseline, a line and a tree on the cohort's data, reads the error in the cohort's own unit and changes one thing at a time. The W08 graded assignment notebook the students already hold is not used in class.",
     "second_half/Lecturer Guides/Class1_Week8_Lecturer_Guide (docx and pdf): clock for Tuesday and Friday, slide map, probes, the numbers each cohort should see in the lab, rescue plan."),
    ("Class 2 — Classification (Week 9 content)",
     "CML3112 Tuesday 10 November; CML3113 and CML3111 Friday 13 November (same times and rooms).",
     "Block 1 sitting: A7 and A8, and the Q7 and Q8 quizzes, are sat together in the last 20 minutes of this class.",
     "Yes or no from a limit; why accuracy misleads (the always-say-no baseline); scaling; logistic regression and the S curve; a tree that classifies; confusion matrix; precision, recall and F1; the threshold; ROC and AUC.",
     "Seven steps in five stages, each stage ending with a check: prepare, label, logistic regression, tree, confusion matrix, threshold, ROC and AUC. The validation set has 15 rows and three positives, so every score is shaky; the deck says so on purpose.",
     "second_half/Lecturer Guides/Class2_Week9_Lecturer_Guide. If the quiz time is short, the guide says to drop the decision tree from the lab."),
    ("Class 3 — Can I trust this model? (Week 10 content)",
     "CML3112 Tuesday 17 November; CML3113 and CML3111 Friday 20 November.",
     "Underfitting, good fit and memorising (the depth curve); K-fold and group folds, reported as an average and a spread; leakage and its three routes; reproducibility (the seed and the pipeline rule).",
     "Six steps: prepare, validation curve, cross-validation, data leakage (the honest and the leaky score side by side), seeds and run record, then three written sentences and a saved copy.",
     "Proposed Block 1 assignment deadlines (A7 and A8): CML3112 Tue 17 Nov 11:00, CML3113 Fri 20 Nov 08:00, CML3111 Fri 20 Nov 11:00.",
     "second_half/Lecturer Guides/Class3_Week10_Lecturer_Guide."),
    ("Class 4 — Choosing a model (Week 11 content)",
     "CML3112 Tuesday 24 November; CML3113 and CML3111 Friday 27 November.",
     "Building and testing a feature (an ablation); not using equipment_id; ridge and nearest neighbours as previews; a fair comparison of five candidates; the decision memo; the test set opened once; the project rehearsal.",
     "Nine notebook steps in five groups: prepare, a first loop with three models, features, one-hot encoding, scaling and ridge, k-NN, then the model table and the decision memo. Support vector machines, random forests, boosting, clustering and neural networks are named in the deck as next semester.",
     "Block 2 sitting: A9, A10 and A11, and the Q9 and Q10 quizzes, in the last 20 minutes. Proposed Block 2 assignment deadlines: CML3112 Tue 1 Dec 11:00, CML3113 Fri 4 Dec 08:00, CML3111 Fri 4 Dec 11:00. The unmarked project rehearsal is released right after this class.",
     "second_half/Lecturer Guides/Class4_Week11_Lecturer_Guide."),
]


def build_lecturer_section(tpls):
    h1, date_t, body_t, brk = tpls
    els = []
    els.append(make_heading(h1, "Heading1", NEW_W811))
    els.append(new_par(date_t, "Tue 3 November to Fri 27 November 2026"))
    els.append(new_par(body_t,
        "Weeks 1 to 7 are done. Week 7 was Practical Test 1 and Week 6 was waived. The semester ends at Week 12, so Weeks 8 to 11 are four classes of three hours. Each class has two parts. Concepts come first with no laptops: 14 to 18 slides, each with a drawn picture, plain words and one small example you can follow by hand, with a spoken script in the notes. A black divider slide, “Part 2: the lab”, then moves the class to a notebook where every step is PREDICT, RUN, READ, CHANGE. The week number names the content; the Friday cohorts meet one week later in date than CML3112.",
        label="How the classes run."))
    els.append(new_par(body_t,
        "CML3112 uses building cooling load (kW), CML3113 crusher energy demand (kWh/t) and CML3111 motor winding temperature (deg C). The structure is the same for all three.",
        label="Cohort overlays."))
    els.append(new_par(body_t,
        "Weeks 1 to 5 stay weekly (best 3 of 5). Block 1 is A7 (Regression and baseline) plus A8 (Classification and cost) with Q7 and Q8, sat together in the last 20 minutes of Class 2. Block 2 is A9, A10 and A11 with Q9 and Q10, sat in the last 20 minutes of Class 4. Weights: quizzes 15, assignments 15, Data Analysis Project 10 (still a team project, teams of 4 to 5 formed in Week 1), Practical Test 1 15, Engineering ML project 45. Semester 1 results can be published provisionally out of 55 with the project pending. Detail: Block_Assessment_Arrangement_2026-11-03.md.",
        label="Assessment."))
    els.append(new_par(body_t,
        "second_half/Lecturer Guides/ holds one guide per class (the clock for Tuesday and Friday, the slide map, probe questions, the lab numbers for each cohort and the rescue plans). second_half/Plan_Weeks_8-12.pdf is the plan for Weeks 8 to 12. Decks, lab notebooks and student packs are in second_half/Slides, Lab Notebooks and Student Packages. The old Week 8 to 15 decks and their ZIPs are superseded; use the new decks. Everything in second_half/ is private to the lecturer except the student packs and the student slide PDFs.",
        label="Where the detail lives."))
    for title, dates, l2, ideas, lab, point in CLASSES:
        els.append(make_heading(h1, "Heading2", title))
        els.append(new_par(body_t, dates, label="Dates."))
        if title.startswith("Class 1"):
            els.append(new_par(body_t, l2, label="Friday cohorts."))
            els.append(new_par(body_t, ideas, label="Ideas, in order."))
            els.append(new_par(body_t, lab, label="The lab."))
            els.append(new_par(body_t, point, label="Pointers."))
        elif title.startswith("Class 2"):
            els.append(new_par(body_t, ideas, label="Ideas, in order."))
            els.append(new_par(body_t, lab, label="The lab."))
            els.append(new_par(body_t, l2, label="Assessment."))
            els.append(new_par(body_t, point, label="Pointers."))
        elif title.startswith("Class 3"):
            els.append(new_par(body_t, l2, label="Ideas, in order."))
            els.append(new_par(body_t, ideas, label="The lab."))
            els.append(new_par(body_t, lab, label="Assessment."))
            els.append(new_par(body_t, point, label="Pointers."))
        else:
            els.append(new_par(body_t, l2, label="Ideas, in order."))
            els.append(new_par(body_t, ideas, label="The lab."))
            els.append(new_par(body_t, lab, label="Assessment."))
            els.append(new_par(body_t, point, label="Pointers."))
    els.append(copy.deepcopy(brk))
    els.append(make_heading(h1, "Heading1", NEW_W12))
    els.append(new_par(date_t, "Proposed: Tue 1 December (CML3112) and Fri 4 December 2026 (CML3113, CML3111). Lecturer to confirm."))
    els.append(new_par(body_t,
        "One supervised 3-hour sitting in Google Colab in the Week 12 class slot, entered and submitted like Practical Test 1 (same timed entry and Submit test flow), fully auto-graded. It covers Weeks 1 to 11 only and counts 45 percent of the course. Each student gets one of three data variants (A, B, C), allocated at random by the portal. There is no demonstration, viva, reflection, take-home or clinic, and there are no teams for this project.",
        label="What it is."))
    els.append(new_par(body_t,
        "Part A, the coded notebook, is 30 marks: 24 for hidden tests on unseen data and 6 for automatic process checks (the test set opened once, preprocessing fitted on the training set only, the same result with the seed, readable charts). Part B, the decision memo, is 15 marks, written as a form inside the notebook and marked automatically (the recommended model, the validation and test numbers, three limits chosen from a list, one next step, two short answers checked by keyword and length). No mark is entered by hand.",
        label="Marks."))
    els.append(new_par(body_t,
        "CML3112 Tuesday 1 December, 11:00 to 14:00. CML3113 Friday 4 December, 08:00 to 11:00. CML3111 Friday 4 December, 11:00 to 14:00. All proposed; confirm them in writing.",
        label="Proposed times."))
    els.append(new_par(body_t,
        "An unmarked rehearsal (a practice notebook and a practice data file, same structure, no solved walk-through) is released right after Class 4: CML3112 Tuesday 24 November, CML3113 and CML3111 Friday 27 November.",
        label="Rehearsal."))
    els.append(new_par(body_t,
        "Before: confirm the times, run the rehearsal and one sitting notebook once in real Colab, deploy the portal and collector bundle (Project/deploy/DEPLOYMENT_STEPS.md) and set the three form windows. On the day: supervise as for Test 1, state the rules from the student brief aloud and keep a visible clock. After: run the Docker grading, read the short spot-check list (a flag never changes a mark), then export to the gradebook and import Part A and Part B.",
        label="What the lecturer does."))
    els.append(new_par(body_t,
        "second_half/Project/Lecturer_Marking_Guide.pdf (time limit, timeline, grading commands, day-of checklist, spot-check list, worked example, what is not proven), second_half/Project/Student_Brief_<cohort>.pdf, second_half/Project/README.md and second_half/Plan_Weeks_8-12.pdf.",
        label="Pointers."))
    return els


def patch_lecturer_guide(d):
    # --- front matter and contents
    rep(d, "Weeks 1–15 ·", "Weeks 1–12 ·", expected=2)  # title line + running header
    old_entries = {
        "Week 8 — Learning from data: the first model": NEW_W811,
        "Week 9 — Classification: predicting a category": NEW_W12,
    }
    drop_entries = [
        "Week 10 — Can I trust this model?",
        "Week 11 — Features: where engineering knowledge enters",
        "Week 12 — Model comparison and engineering judgement",
        "Week 13 — Project studio: reproducibility and peer review",
        "Week 14 — Practical Test 2 — End-to-End Engineering ML",
        "Week 15 — Engineering ML Demo Day, viva and reflection",
    ]
    body = body_paras(d)
    how = find_para(d, "How to use this guide", "Heading1")
    cidx = body.index(how)
    for p in body[:cidx]:
        t = ptext(p)
        if style_of(p) == "" and t in old_entries:
            set_text(p, old_entries[t])
        elif style_of(p) == "" and t in drop_entries:
            remove(p)
    # the contents entry for the new Week 12 text: set after drops (idempotent)
    # --- tiny phrases in Weeks 1-7
    rep(d, "Eight activities depend on students NOT knowing the answer: the Break and Fix notebooks in Week 2, the Wrong Answer Hunt in Week 3, Investigation Lab 1 in Week 4, the Outlier Argument in Week 6, the 97 Per Cent Trap in Week 9, the Too Good To Be True leakage notebooks in Week 10, the unlabelled model comparison in Week 12, and the Week 15 viva bank. Their answer keys are in this document and nowhere else. Distributing this file to a class group would invalidate all eight.",
        "Four activities depend on students NOT knowing the answer: the Break and Fix notebooks in Week 2, the Wrong Answer Hunt in Week 3, Investigation Lab 1 in Week 4 and the Outlier Argument in Week 6. Their answer keys are in this document and nowhere else. Distributing this file to a class group would invalidate all four. The Weeks 8 to 12 lecturer guides and the project marking guide in second_half/ are private in the same way.")
    rep(d, "Each week below lists its slides in order.", "Each week below (Weeks 1 to 7) lists its slides in order.")
    rep(d, "Slides with no entry need nothing beyond what is on them.",
        "Slides with no entry need nothing beyond what is on them. Weeks 8 to 12 were rebuilt as four classes and a project sitting; they are described briefly at the end, and the detailed guides are in second_half/Lecturer Guides/.")
    rep(d, "so say it now and Week 9 will not be a surprise.", "so say it now and the project will not be a surprise.")
    rep(d, "you need the team list for the Week 9 project registration anyway.", "you need the team list for the Data Analysis Project anyway.")
    rep(d, "that otherwise arrive in Week 12.", "that otherwise arrive late in the semester.")
    rep(d, "Note that the Week 7 and Week 14 tests run in Colab, so students need no local setup for them.",
        "Note that the Week 7 test and the Week 12 project sitting run in Colab, so students need no local setup for them.")
    rep(d, "It is what stops the Week 9 projects being built on unusable data.", "It is what stops the team projects being built on unusable data.")
    rep(d, "that requirement is what prevents a Week 9 disaster.", "that requirement is what prevents a late-semester disaster.")
    rep(d, "· regenerate after any change to the decks.",
        "· regenerate after any change to the Weeks 1 to 7 decks. Weeks 8 to 12 were replaced by hand on 4 November 2026.")
    # --- replace Weeks 8-15 body
    old_h8 = find_para(d, "Week 8 — Learning from data: the first model", "Heading1")
    if old_h8 is None:
        assert find_para(d, NEW_W811, "Heading1") is not None
    else:
        last = None
        for p in body_paras(d):
            if ptext(p).startswith("16 slides in Week 15 need something from you"):
                last = p
        assert last is not None
        h7 = find_para(d, "Week 7 — Practical Test 1 — Data Investigation", "Heading1")
        kids = list(d.element.body.iterchildren())
        i7 = kids.index(h7)
        h1_t, date_t, body_t = kids[i7], kids[i7 + 1], kids[i7 + 3]
        assert style_of(kids[i7 + 2]) == "Heading3" and ptext(date_t).startswith("Tue 20")
        i8, il = kids.index(old_h8), kids.index(last)
        brk = kids[i8 - 1]
        assert ptext(brk) == "" and brk.find(".//" + qn("w:br")) is not None
        for el in kids[i8:il + 1]:
            d.element.body.remove(el)
        anchor = brk
        for el in build_lecturer_section((h1_t, date_t, body_t, brk)):
            anchor.addnext(el)
            anchor = el
    rep(d, "Five stages, each ending with a check: label, logistic regression, tree, confusion matrix, threshold, ROC. The validation set",
        "Seven steps in five stages, each stage ending with a check: prepare, label, logistic regression, tree, confusion matrix, threshold, ROC and AUC. The validation set")
    rep(d, "Everything in second_half/ is private to the lecturer except the student packs.",
        "Everything in second_half/ is private to the lecturer except the student packs and the student slide PDFs.")
    # contents safety: make sure entries match the headings that exist
    assert find_para(d, NEW_W12, "Heading1") is not None


# ---------------------------------------------------------------- beginner quick guide
def patch_quick_guide(d):
    rep_par(d, "Lecturer quick guide | Revised 15 October 2026", "Lecturer quick guide | Revised 15 October 2026 | Weeks 8 to 12 updated 4 November 2026")
    rep(d, "Week 8  A first prediction model", "Class 1, Week 8 content  A first prediction model")
    rep(d, "Week 9  Classification and the cost of mistakes", "Class 2, Week 9 content  Classification and the cost of mistakes")
    rep(d, "Week 10  Honest validation and leakage", "Class 3, Week 10 content  Honest validation and leakage")
    rep(d, "Week 11  Creating and testing a useful feature", "Class 4, Week 11 content  Creating a feature and choosing a model")
    p12 = find_para(d, "Week 12  Choosing and explaining a model", "Heading1")
    if p12 is not None:
        remove(p12)
    # intro line under the modelling sequence title
    intro = ("From Week 8 each class has two parts: the ideas first with no laptops, then a lab notebook "
             "(predict, run, read, change). The four classes are Weeks 8 to 11 content. The Friday cohorts take "
             "Class 1 one week later as a recap and a long lab.")
    if find_para(d, intro) is None:
        title = find_para(d, "The modelling sequence", "Title")
        tpl = find_para(d, "Select named feature columns", startswith=True)
        blank = title.getnext()
        assert ptext(blank) == ""
        newp = new_par(tpl, intro)
        blank.addnext(newp)
    # Projects and revision -> Week 12 sitting
    rep(d, "Projects and revision", "The Week 12 project sitting")
    rep(d, "Week 13  Making the project understandable and runnable", "Week 12  The project sitting")
    set_if(d, "Reproduce the pandas notebook from a fresh session using documented data paths, dependencies and run order.",
           "The Engineering ML project is one individual, timed 3-hour sitting in Google Colab in the Week 12 class slot, entered and submitted like Practical Test 1 and marked automatically. Part A is a coded notebook (30 marks) and Part B is a decision memo form inside the notebook (15 marks); together they are 45 percent of the course. It covers Weeks 1 to 11 only.")
    set_if(d, "Use pandas inside the published functions.",
           "Release the unmarked rehearsal right after Class 4. Proposed sittings, lecturer to confirm: CML3112 Tuesday 1 December 11:00 to 14:00, CML3113 Friday 4 December 08:00 to 11:00, CML3111 Friday 4 December 11:00 to 14:00. See second_half/Project/Lecturer_Marking_Guide.pdf and second_half/Plan_Weeks_8-12.pdf.",
           startswith=True, first_only=True)
    for t in ("Week 14  Preparing for Practical Test 2", "Week 15  Presenting the project and individual contribution"):
        h = find_para(d, t, "Heading1")
        if h is not None:
            # remove heading and the paragraphs that follow until the next heading
            nxt = h.getnext()
            remove(h)
            while nxt is not None and style_of(nxt) not in ("Heading1", "Title"):
                n2 = nxt.getnext()
                remove(nxt)
                nxt = n2
    rep(d, "Major projects, tests and demos still require", "The Week 12 project sitting and the practical test still require")


def set_if(d, old_prefix, new_text, startswith=False, first_only=False):
    """Set whole-paragraph text for the first paragraph that starts with old_prefix."""
    hits = [p for p in body_paras(d) if ptext(p).startswith(old_prefix)]
    if not hits:
        assert find_para(d, new_text, startswith=True) is not None, old_prefix
        return
    if not first_only:
        assert len(hits) == 1, (old_prefix, len(hits))
    set_text(hits[0], new_text)


# ---------------------------------------------------------------- the other documents
def patch_roadmap(d):
    rep(d, "Weeks 8 to 12. The fit / predict / score pattern", "Weeks 8 to 11. The fit / predict / score pattern")
    rep_par(d, "Week 9.", "Week 9: logistic regression and a classification tree. Random forests move to Semester 2.")
    rep(d, "Not in Semester 1. KNN is a good teaching algorithm and its omission is a deliberate time trade, not an oversight.",
        "Nearest neighbours is only previewed in Class 4 (Week 11); the full treatment and support vector machines are not in Semester 1. KNN is a good teaching algorithm and leaving it out is a deliberate time trade, not an oversight.")
    rep(d, "Not in Semester 1. Introduced in Semester 2 alongside overfitting control.",
        "Ridge is previewed in Class 4 (Week 11) and nothing more. Lasso, ElasticNet and the full treatment come in Semester 2 alongside overfitting control.")
    rep(d, "Demonstrated for sixty seconds in Week 12 and then explicitly deferred, with the students told why: the tool is not the lesson.",
        "Named in the Weeks 8 to 11 decks and then explicitly deferred to next semester, with the students told why: the tool is not the lesson.")
    rep(d, "Week 9 and Week 10. Accuracy, precision", "Week 9. Accuracy, precision")
    rep(d, "Semester 1 teaches linear regression, logistic regression, trees and forests, which is enough to work with",
        "Semester 1 teaches linear regression, logistic regression and decision trees, which is enough to work with")
    rep(d, "Ridge and Lasso are the natural companions to the overfitting session in Week 10, and leaving them out means",
        "Ridge and Lasso are the natural companions to the overfitting session in Week 10 (Ridge is only previewed in Week 11), and leaving them out means")
    rep(d, "Week 11, always inside a scikit-learn Pipeline", "Introduced in Week 8 and made the rule in Week 10, always inside a scikit-learn Pipeline")
    rep_par(d, "Week 15", "Week 11 (last class)")
    rep(d, "travelled in fifteen weeks", "travelled in twelve weeks")


def patch_preflight(d):
    rep(d, "The teaching material for all fifteen weeks is written and checked.",
        "The teaching material for all twelve weeks is written and checked.")
    rep(d, "that both tests run in Colab and are taken unaided.",
        "that Practical Test 1 and the Week 12 project sitting both run in Colab and are taken unaided.")


def patch_setup_guide(d):
    rep(d, "Both tests are taken in Colab with your own Google account.",
        "Practical Test 1 and the Week 12 project sitting are taken in Colab with your own Google account.")


def patch_build_plan(d):
    rep(d, "individual reflection stays individual.", "the individual contribution log stays individual.")


def patch_colab_guide(d):
    rep(d, "Test 1 and Test 2 • CML3111", "Practical Test 1 and the Week 12 project sitting • CML3111")
    rep(d, "select TEST1_student.ipynb or TEST2_student.ipynb from your Downloads folder",
        "select TEST1_student.ipynb or ML_PROJECT_student.ipynb from your Downloads folder")


def patch_grading_checklist(d):
    rep(d, "Test 1 and Test 2 • CML3111", "Practical Test 1 and the Week 12 project sitting • CML3111")
    rep(d, "send the Week 7 or Week 14 revision PDF and its matching practice CSV.",
        "send the Week 7 revision PDF and its matching practice CSV (for the project: the rehearsal notebook and practice data file released after Class 4).")
    rep(d, "from the Week 7 or Week 14 deck.", "from the Week 7 deck (for the project sitting, from second_half/Project/deploy).")
    rep(d, "It includes both tests across all three programmes", "It includes every test and the project sitting across all three programmes")
    rep(d, "Test 1 contributes 15 semester points; Test 2 contributes 20.",
        "Test 1 contributes 15 semester points. The Engineering ML project sitting contributes 45 (Part A 30, Part B 15) and is graded with second_half/Project/grader_spec/grade_project.py; see second_half/Project/Lecturer_Marking_Guide.pdf.")


FILES = [
    ("IUEA_Teaching_Plan/IUEA_ML_Lecturer_Teaching_Guide_W1-W15.docx", patch_lecturer_guide),
    ("IUEA_Teaching_Plan/IUEA_ML_Beginner_Teaching_Quick_Guide.docx", patch_quick_guide),
    ("IUEA_Teaching_Plan/IUEA_ML_Roadmap_Benchmark.docx", patch_roadmap),
    ("IUEA_Teaching_Plan/IUEA_ML_Week1_PreFlight_Checklist.docx", patch_preflight),
    ("IUEA_Teaching_Plan/IUEA_ML_Student_Setup_Guide.docx", patch_setup_guide),
    ("IUEA_Teaching_Plan/IUEA_ML_Assessment_Technology_Build_Plan.docx", patch_build_plan),
    ("IUEA_Teaching_Plan/test_operations/Student_Colab_Test_Guide.docx", patch_colab_guide),
    ("IUEA_Teaching_Plan/test_operations/Test_Grading_Checklist.docx", patch_grading_checklist),
]


def main(root=None):
    root = root or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    for rel, fn in FILES:
        process(os.path.join(root, rel), fn)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
