# -*- coding: utf-8 -*-
"""Platform architecture and benchmark note."""
import sys
import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_HERE)
sys.path.insert(0, _HERE)
from docx.enum.text import WD_ALIGN_PARAGRAPH as AL
from docxkit import *      # noqa
from docxkit import _border

OUT = _ROOT + "/IUEA_Teaching_Plan/IUEA_ML_Platform_Architecture_Note.docx"

d = new_doc(margin_cm=2.3)
header_footer(d, "IUEA Faculty of Engineering · CML3111 / CML3112 / CML3113 · Platform Architecture Note")
first_page_different(d)

spacer(d, 52)
para(d, "INTERNATIONAL UNIVERSITY OF EAST AFRICA · FACULTY OF ENGINEERING",
     size=10.5, bold=True, colour=MID, align=AL.CENTER, after=20)
para(d, "One System, Not Five", size=26, bold=True, colour=NAVY, align=AL.CENTER, after=4)
para(d, "Auto-grading architecture, benchmarked against Coursera, DeepLearning.AI and IBM",
     size=13, colour=MID, align=AL.CENTER, after=18)
p = para(d, "COLAB-FIRST  ·  NO SERVER  ·  FREE TOOLS ONLY", size=11, bold=True,
         align=AL.CENTER, after=8, before=8)
_border(p, "top", NAVY_H, 10)
_border(p, "bottom", NAVY_H, 10)
spacer(d, 18)
para(d, "Companion to the Assessment Technology Build Plan · working code in grader/",
     size=9.5, colour=GREY, align=AL.CENTER, after=3)
para(d, "Version 1.0 · September 2026", size=9.5, italic=True, colour=GREY, align=AL.CENTER)
page_break(d)

h1(d, "1. What was asked for")
para(d, "A single system rather than a collection of scripts: end-of-session weekly quizzes reached by QR code and "
        "auto-marked, notebooks that grade themselves the moment a student clicks submit, the two practical "
        "tests marked automatically, and one gradebook that computes a correctly weighted final score. "
        "Benchmarked, explicitly, against the way learning works on Coursera, DeepLearning.AI and IBM's courses.")
para(d, "That is the right instinct. Five loosely-coupled scripts is more for one person to hold in their head "
        "than one tool, and the student experience on those platforms is better than anything a set of "
        "command-line utilities produces. This note sets out what those platforms actually do, what of it "
        "transfers to a course with no server and no budget, and what the resulting single system is.")

h1(d, "2. What Coursera and DeepLearning.AI actually do")
para(d, "The Submit button in a DeepLearning.AI notebook is not a notebook feature. It is a client for a "
        "grading service. The sequence is: the notebook file is packaged and sent to Coursera's backend; the "
        "backend renames it to the filename the assignment expects; it mounts that file into a freshly started "
        "Docker container built from an image the instructional team uploaded; the container runs the grader "
        "and returns a score and feedback, which the platform writes into its own gradebook. Coursera publishes "
        "a command-line tool whose entire job is uploading those grader containers.")
para(d, "IBM's courses work the same way in principle, on their own hosted JupyterLab environment. Published "
        "descriptions of comparable systems show the same shape: a submission queue, a horizontally scalable "
        "container service, and each test executed inside a sandbox so that student code cannot damage the "
        "platform or reach other students' work.")
callout(d, "The consequence, stated plainly",
        "Instant grading on click requires a server, a container runtime, a queue and a database. There is no "
        "configuration of a notebook that produces it. What can be reproduced without a server is the "
        "EXPERIENCE — instant, specific feedback and a single accumulating grade — but not the enforcement. "
        "That distinction runs through every decision below.", MID_H, LIGHT_H)

h1(d, "3. What was considered and rejected, with reasons")
table(d, ["Option", "What it would give", "Why not"],
      [["JupyterHub + nbgrader",
        "The academic equivalent of Coursera: browser notebooks with no student installs, a Validate button, "
        "fetch and submit, a real gradebook. Used by universities at this scale.",
        "Needs a Linux server, which has been confirmed unavailable. Its own documentation also warns that "
        "autograding runs student code unsandboxed and a capable student may read other submissions or alter "
        "grades — unacceptable for the 35% sitting in the two tests."],
       ["A custom web application",
        "Full control, exactly the Coursera flow.",
        "Weeks of work, a server, uptime during class, authentication, backups, and the security problem of "
        "executing untrusted code. Building this while teaching nine hours a week and authoring eighteen test "
        "datasets is how the semester fails."],
       ["otter-grader",
        "Excellent, generates the student notebook and the grader from one master file.",
        "Its containerised batch mode needs Docker installed and an image pulled. Its local mode does not, but "
        "then it offers little the purpose-built module here does not."],
       ["Colab + in-notebook grader + signed token  (ADOPTED)",
        "Instant specific feedback, no installs for students, one accumulating gradebook, works with zero "
        "infrastructure.",
        "Cannot be made tamper-proof. Accepted deliberately, and mitigated — see Section 6."]],
      [22, 39, 39], bold_first=True)

page_break(d)
h1(d, "4. The system")
para(d, "One Python module, `iuea_grader.py`, standard library only, no installation. It behaves identically in "
        "Google Colab, in a local Jupyter notebook, in a plain script, and on an offline lab machine with no "
        "network at all. Three calls are the entire student-facing surface.")
table(d, ["The student runs", "What happens"],
      [["g = Grader(\"W05\")", "Loads the assignment's visible test specification."],
       ["g.check(\"q2\")", "Instant PASS or FAIL on one question, with a sentence that teaches the fix rather "
                           "than saying 'incorrect'. Only visible tests ever run here."],
       ["g.check_all()", "Every visible question, plus a progress line: 'you have passed 3 of 3 checks, 10 of "
                         "10 visible marks'. Hidden marks are named but not revealed."],
       ["g.submit(\"S24001\")", "Prints a ~100-character signed code containing the student id, assignment, "
                                "visible scores, a hash of their answers, a timestamp and an HMAC signature. "
                                "They paste it into a Google Form."]],
      [26, 74], bold_first=True)
spacer(d, 10)
para(d, "On the lecturer's side there is one command. `batch_grade.py` takes the folder of submitted notebooks, "
        "executes each from a clean state in a subprocess, grades against all tests including the hidden ones, "
        "and writes one results CSV plus a feedback file per student. It separately ingests the token CSV "
        "exported from the Form, verifies every signature, and flags any token whose answer-hash disagrees with "
        "the notebook actually submitted. Measured: 196 notebooks in 84 seconds.")
para(d, "The gradebook is a Google Sheet driven by an Apps Script that applies the current weights, the "
        "best-ten-of-twelve weekly quiz rule and the best-eight-of-eleven challenge rule, flags missing work, and "
        "produces a student-facing progress line. Its pure functions carry 73 unit tests, including one that "
        "verifies a real token generated by the Python module.")

h2(d, "One point of substance: the token is not the mark")
para(d, "This is the design decision that makes a client-side system defensible. The submitted code is a "
        "receipt, not a grade. What goes into the gradebook is the score `batch_grade.py` computes by running "
        "the student's actual notebook against the hidden tests. The token's job is to give the student "
        "certainty in the moment, to prove which version they intended to submit, and to let the lecturer spot "
        "a mismatch. A forged token buys nothing unless a week is accepted with no notebook behind it.")

h1(d, "5. Which industry patterns transferred, and which did not")
table(d, ["Pattern", "Status here"],
      [["Instant, specific feedback rather than a bare pass/fail",
        "ADOPTED, and improved on. Published critiques of the Coursera experience note students often see only "
        "whether a test passed. Every failure message here names the cause and the fix."],
       ["Practice unlimited, graded attempts limited",
        "ADOPTED. `check()` is unlimited; each weekly quiz is a single sitting with no resit, and the two "
        "lowest of the twelve scores are dropped instead; the two tests are single-sitting."],
       ["Validate before submit",
        "ADOPTED. `check_all()` is the validate step, and it runs offline."],
       ["An ungraded lab before every graded one",
        "ADOPTED as a recommendation. DeepLearning.AI's strongest structural habit. Cheap to add: ship each "
        "week's practical as an ungraded walkthrough plus a graded task."],
       ["Visible cumulative progress",
        "ADOPTED. The gradebook emails a standing line; the notebook prints one after check_all()."],
       ["Sandboxed execution of student code",
        "NOT POSSIBLE. Needs containers and therefore a server. `batch_grade.py` runs student code with the "
        "lecturer's own permissions — grade on a machine that is not the only home of the gradebook."],
       ["Server-side enforcement of the grade",
        "NOT POSSIBLE, and the honest cost of the constraint. See Section 6."],
       ["Short video then immediate practice",
        "ADOPTED in the teaching design rather than the software. The Week 1–4 decks carry verified video links "
        "with an explicit 'watch for' instruction, positioned before or after the session by intent."]],
      [34, 66], bold_first=True)

page_break(d)
h1(d, "6. The integrity limit, stated without softening")
para(d, "A student who wants to can forge a valid submission token. The signing key must be present in a file "
        "the student is able to read, because the grader runs on their machine. No client-side design fixes "
        "this; the only fix is a server.")
para(d, "What the design buys instead is that forgery is not worth doing. Four things stack up:")
table(d, ["Mitigation", "What it actually achieves"],
      [["The notebook is the mark, not the token",
        "A forged token inflates a receipt. The gradebook is written from the notebook. The two only diverge if "
        "a week is accepted with no notebook."],
       ["Sample re-grading (`--sample`)",
        "Re-runs a random percentage of real notebooks and compares against token claims. Tested: it caught a "
        "planted inflated token at 20% sampling on one seed and missed it on another — which is the honest "
        "behaviour. Over eleven weeks, repeated forging is caught with probability around 0.91 at that rate."],
       ["Weekly work is only 10% of the course",
        "The maximum available by cheating the weekly mechanism is small."],
       ["35% sits in two offline invigilated tests",
        "Unaided capability is certified where integrity can actually be enforced. A student whose weekly "
        "scores and test scores diverge sharply is visible in the gradebook by Week 7."]],
      [30, 70], bold_first=True)
spacer(d, 10)
callout(d, "Say this to students in Week 1",
        "The weekly checks and the weekly quizzes exist to tell you, and me, whether you are keeping up. They are "
        "not what certifies you — the two offline tests do that. Stated openly, most students stop treating the "
        "mechanism as something to beat. Concealing the limitation would be both dishonest and less effective.",
        MID_H, LIGHT_H)

h1(d, "7. Other limits worth knowing before you rely on it")
table(d, ["Limit", "Consequence and response"],
      [["Colab needs internet",
        "The primary environment is unusable in an outage. The same module runs locally and offline, which is "
        "why the local route and the lab machines are kept alive rather than retired."],
       ["The per-cell timeout is Unix-only",
        "On Windows a hanging notebook costs the whole per-notebook budget rather than one cell. Grade on macOS "
        "or Linux."],
       ["The answer-hash can flag an honest student",
        "Someone who re-runs or edits after submitting will mismatch. Zero false positives across 189 "
        "comparisons in testing, which is not a guarantee. Treat a mismatch as a question, not a finding."],
       ["Nothing detects plagiarism",
        "Near-identical notebooks will occur on shared wifi. The viva and the offline tests are the detection "
        "mechanism; 'marked on what you can explain' is the sanction."],
       ["Two files must be kept in step by hand",
        "The visible spec students receive and the hidden spec you keep. A drift test exists; run it after every "
        "spec edit."],
       ["Untested on the real platforms",
        "Two specific things could not be executed in the build environment: Colab's file-upload call, and Apps "
        "Script's HMAC function (the equivalent JavaScript path is tested). Ten minutes each on the real thing "
        "before Week 3."],
       ["Grade bands are a placeholder",
        "Must be set against IUEA regulations before any mark is published."]],
      [28, 72], bold_first=True)

h1(d, "8. If a server ever becomes available")
para(d, "The architecture is deliberately layered so this is not a rewrite. Migrating to JupyterHub with "
        "nbgrader would replace how assignments are distributed and collected, and would remove student "
        "installs entirely — but the test specifications, the feedback text, the weights and the gradebook "
        "logic all carry across. The right trigger to revisit it is a Linux machine on the campus LAN with "
        "someone other than the lecturer able to keep it running.")
para(d, "One caution for that day: nbgrader's own documentation warns that its autograding is unsandboxed. Even "
        "with a hub, the two high-stakes tests should stay offline, collected, and graded locally. That is what "
        "universities do with examinations, and it is what Coursera does with its own graded attempts.")

h1(d, "9. What this supersedes")
table(d, ["Old", "Now"],
      [["autograde.py + a separate self-check path", "One module. `check()` for the student, `batch_grade.py` "
                                                     "for the lecturer, one specification format."],
       ["pull_submissions.sh over GitHub repositories", "Google Form upload plus the token CSV. GitHub remains "
                                                        "taught and used for the project, but is no longer the "
                                                        "grading pipeline."],
       ["check_setup.py and the offline installer bundle", "Largely retired for students, who now use Colab. "
                                                           "Still needed for lab machines and the offline tests."],
       ["Five scripts and two READMEs", "grader/ with one README, one module, one batch command, one gradebook, "
                                        "and a regression harness."]],
      [40, 60], bold_first=True)
spacer(d, 12)
callout(d, "The honest summary",
        "This reproduces the Coursera feel — instant, specific, encouraging feedback and one accumulating "
        "grade — on no infrastructure and no budget. What it cannot reproduce is enforcement, because "
        "enforcement is the part that costs money. The design responds by putting the low-stakes work where "
        "tampering does not pay and the high-stakes work where tampering is not possible.",
        NAVY_H, LIGHT_H)

spacer(d, 10)
para(d, "Architecture note version 1.0 · September 2026 · platform behaviour verified at that date and worth "
        "re-checking each year.", size=9, italic=True, colour=GREY, align=AL.CENTER)

d.save(OUT)
print("saved", OUT)
