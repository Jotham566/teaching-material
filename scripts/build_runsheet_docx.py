# -*- coding: utf-8 -*-
"""Week 2 Lecturer Runsheet — the highest-risk session."""
import sys
import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_HERE)
sys.path.insert(0, _HERE)
from docx.enum.text import WD_ALIGN_PARAGRAPH as AL
from docxkit import *      # noqa
from docxkit import _border

OUT = _ROOT + "/IUEA_Teaching_Plan/IUEA_ML_Week2_Lecturer_Runsheet.docx"

d = new_doc(margin_cm=2.1)
header_footer(d, "IUEA Faculty of Engineering · Week 2 Lecturer Runsheet · CML3111 / CML3112 / CML3113")
first_page_different(d)

# ---------------------------------------------------------------- cover
spacer(d, 44)
para(d, "INTERNATIONAL UNIVERSITY OF EAST AFRICA · FACULTY OF ENGINEERING",
     size=10.5, bold=True, colour=MID, align=AL.CENTER, after=20)
para(d, "Week 2 Lecturer Runsheet", size=26, bold=True, colour=NAVY, align=AL.CENTER, after=4)
para(d, "The development environment session", size=15, colour=MID, align=AL.CENTER, after=18)
p = para(d, "TUESDAY 15 SEPTEMBER / FRIDAY 18 SEPTEMBER 2026   ·   THREE HOURS PER COHORT",
         size=10.5, bold=True, align=AL.CENTER, after=8, before=8)
_border(p, "top", NAVY_H, 10)
_border(p, "bottom", NAVY_H, 10)
spacer(d, 20)

callout(d, "Why this session has its own document",
        "This is the highest-risk three hours of the semester, and the risk has almost nothing to do with teaching. "
        "Roughly 195 students across three cohorts install Python, VS Code, Git and five packages, on their own "
        "hardware, in one sitting, on a campus network that cannot carry it. If Week 2 fails, Week 3 has no "
        "foundation and the failure compounds every week after it.\n\n"
        "Everything in here is operational. The pedagogy is in the master plan; this is the logistics that decide "
        "whether the pedagogy gets a chance.", "C00000", RED_H)

spacer(d, 16)
para(d, "Companions:  the Student Setup Guide (issue in Week 1)  ·  setup/README.md  ·  setup/ scripts",
     size=9.5, colour=GREY, align=AL.CENTER)
page_break(d)

h1(d, "Contents")
toc(d)
page_break(d)

# ================================================================
h1(d, "1. The one thing most likely to sink the session")
para(d, "It is not installing. It is copying.")
para(d, "The offline bundle is several hundred megabytes. Getting it onto a hundred laptops is the bottleneck, and "
        "it is a physical one — a couple of USB sticks passed around a hundred students will consume the entire "
        "three hours and the session will end with half the room unfinished. The installation itself takes about a "
        "minute per laptop once the files are local.")
para(d, "So the distribution plan is the plan. Three routes running simultaneously, in this order of preference:")
table(d, ["Route", "How", "Covers"],
      [["1 · Network share", "Put the bundle on the local file share and give the path on the first slide. A local "
        "share is not the internet — it is fast and it does not leave the building. Confirm with IT in Week 1 that "
        "you have a writable share and that student machines can reach it.", "Most of the room, if it exists"],
       ["2 · USB sticks", "Four minimum, ideally six or eight, per cohort. Hand them out in the first five "
        "minutes, before you say anything else.", "20–30 students per stick per session"],
       ["3 · Peer-to-peer", "Tell students explicitly that once they have the folder they should copy it to the "
        "person next to them. Say it out loud; most will not think of it. This is the route that actually scales.",
        "Everyone else"]],
      [16, 62, 22], bold_first=True)
spacer(d, 10)
callout(d, "Start the copying before you start teaching",
        "The first five minutes of the session are: sticks out, share path on screen, everybody starts copying. "
        "Then you teach the tool map for twenty minutes while the copying happens in the background. Do not teach "
        "first and copy afterwards — that sequence is what runs out of time.", MID_H, LIGHT_H)

# ================================================================
h1(d, "2. The other thing that cannot be fixed in the room")
para(d, "Python packages are compiled against a specific Python minor version. A wheel built for 3.12 will not "
        "install on 3.13. If a student turns up having installed a different Python at home, the offline bundle "
        "will refuse with 'No matching distribution found', and there is no offline fix during the session.")
table(d, ["Action", "When"],
      [["Choose ONE Python minor version for the whole course. Write it down.", "Now, before building the bundle"],
       ["Make three things agree: the installer on the USB, the PY_TARGET setting in build_offline_bundle.sh, and "
        "the NEWER_THAN_TESTED warning threshold in check_setup.py.", "Before building the bundle"],
       ["Tell students in Week 1, in the Setup Guide and out loud, NOT to install Python at home.",
        "Week 1 — it is already written into the guide"],
       ["Brief helpers: a student hitting 'No matching distribution' is moved onto Colab for the session and "
        "sorted out in office hours. Do not let anyone spend forty minutes on it.", "Helper briefing"]],
      [72, 28], bold_first=True)
spacer(d, 8)
para(d, "A practical note on the choice: do not take the newest Python release. The scientific packages lag new "
        "releases by months, and a version that is one or two behind current will have wheels for everything on "
        "every platform. Verify that the packages you need have wheels for your chosen version at bundle-build "
        "time — build_offline_bundle.sh will fail loudly if they do not, which is exactly when you want to find out.")

# ================================================================
h1(d, "3. Preparation timeline")
para(d, "Ordered backwards from the session. The items marked CRITICAL are the ones that cannot be recovered on "
        "the day.")

table(d, ["When", "Task", "Time"],
      [["Week 1, in the session", "Issue the printed Student Setup Guide. Run the laptop survey on paper — paper "
        "gets a 100% return, a form does not. Collect GitHub usernames onto the roster sheet.", "10 min"],
       ["Week 1", "CRITICAL: ask IT for (a) a writable network share, (b) confirmation of socket count in the "
        "teaching room, (c) whether lab machines can be pre-provisioned. Put it in writing.", "20 min"],
       ["Week 1", "CRITICAL: choose the Python minor version. Update PY_TARGET and NEWER_THAN_TESTED to match.",
        "10 min"],
       ["Week 1", "Download by hand: the Python installers (Windows and macOS), VS Code installers, Git for "
        "Windows, and the Python and Jupyter .vsix extension files. Official pages only — the script prints the "
        "list.", "40 min"],
       ["Week 1", "Run build_offline_bundle.sh with a good connection, then run it again with --check. Read "
        "MANIFEST.txt and note the real total size — you need it to plan the copying.", "30 min"],
       ["Week 1–2", "CRITICAL: run install_offline_windows.bat once on a real Windows machine. It has never been "
        "executed. This is the single highest-value ten minutes in this list.", "10 min"],
       ["Week 1–2", "CRITICAL: full dry run on a laptop that has never had Python installed. Borrow one. Follow "
        "the Student Setup Guide exactly as written, and time yourself. Fix whatever you trip over — you will trip "
        "over something.", "45 min"],
       ["Week 2 minus 3 days", "Copy the bundle to the network share and to every USB stick. Verify one stick on a "
        "different machine.", "40 min"],
       ["Week 2 minus 3 days", "Add screenshots to the Student Setup Guide from your own machine — especially the "
        "Python PATH tick-box, the VSIX install menu, and the VS Code kernel picker. The guide describes these in "
        "words; a picture is worth more to a beginner.", "40 min"],
       ["Week 2 minus 2 days", "Recruit and brief 6–8 floor helpers per cohort from the Week 1 survey. Give them "
        "the briefing in Section 6 and have them complete the setup themselves first.", "30 min"],
       ["Week 2 minus 2 days", "Build the four Break and Fix notebooks (Section 7). Prepare CP0 in Google Forms "
        "and generate its QR codes.", "60 min"],
       ["Week 2 minus 1 day", "Print: the one-page cheat sheet per student, the roster sheets, 20 paper copies of "
        "CP0 in case the network fails.", "20 min"],
       ["Week 2, 20 min before", "Arrive early. Test the projector, the share path from a student account, and one "
        "USB stick. Lay the sticks out on separate tables.", "20 min"]],
      [17, 68, 15], bold_first=True,
      shade_fn=lambda i, r: AMBER_H if "CRITICAL" in r[1] else None)

# ================================================================
h1(d, "4. Room requirements — check these, do not assume")
table(d, ["Requirement", "Why it matters", "If it is not there"],
      [["Seats for the whole cohort with desk space for a laptop",
        "A hundred students balancing laptops on their knees for three hours will not finish",
        "Split the cohort across two rooms with a helper in each, or run the session twice"],
       ["Power sockets — count them",
        "Three hours of installing drains a battery. A room with eight sockets and a hundred students has a "
        "problem you cannot solve on the day",
        "Tell students in advance to arrive fully charged, which the Setup Guide already does. Bring extension "
        "leads. Prioritise sockets for the students who need longest"],
       ["A projector that works with your laptop",
        "The share path, the commands and the kernel picker all need to be visible",
        "Fall back to the printed cheat sheet, which is why it is printed. Write commands on the board"],
       ["Access to the network share from a STUDENT account",
        "Working from your own account proves nothing — permissions differ",
        "USB and peer-to-peer only. Add two more sticks"],
       ["Lab machines for students without laptops",
        "From the Week 1 survey you know exactly how many",
        "Colab in a browser on any available machine, or pair them with a laptop owner for this session only"]],
      [26, 40, 34], bold_first=True)

# ================================================================
page_break(d)
h1(d, "5. Running the session")
para(d, "Three hours. The shape is deliberate: get the copying started, teach while it happens, then install in "
        "waves with the room helping itself.")

table(d, ["Time", "What happens", "Notes"],
      [["0:00–0:05", "Sticks out. Share path on screen. Everybody starts copying, now, before anything else.",
        "Say the peer-to-peer instruction here and repeat it twice during the session."],
       ["0:05–0:25", "The tool map. Six tools, each introduced by the question it answers, not by its name. No "
        "installation talk yet.", "This is the only real teaching in the session, so protect it. It is what stops "
        "the six tools feeling like six arbitrary chores."],
       ["0:25–1:05", "Install clinic, run as a relay. Everyone follows the Setup Guide. As each student reaches "
        "READY on check_setup.py they get a helper badge and join the floor.",
        "The relay is the mechanism that makes 100 students tractable. By 0:45 you should have twenty helpers, not "
        "eight."],
       ["1:05–1:35", "Terminal basics and the first script. Four commands only: pwd, ls, cd, python. Then run "
        "hello_engineering for their own course code, change a number, run it again.",
        "Resist teaching more shell. Four commands is the syllabus."],
       ["1:35–2:10", "First notebook. Cells, Shift+Enter, markdown versus code, and the out-of-order execution "
        "trap, which the notebook triggers on purpose.",
        "Watch for the kernel-selection question — it will be the commonest confusion in the room."],
       ["2:10–2:35", "Git and GitHub together, walked through on the projector line by line. Everyone ends with a "
        "live repository URL.", "Do this as a whole room in lockstep. Individually it takes three times as long."],
       ["2:35–2:45", "Break and Fix (Section 7). Four deliberately broken notebooks; teams diagnose and name the "
        "cause in one sentence each.", "This is the pedagogical point of the session, not a filler."],
       ["2:45–3:00", "CP0 diagnostic by QR — 8 questions, ungraded, ten minutes. Then A2 issued and the roster "
        "check.", "Say clearly that CP0 does not count. Its job is to show you who is not ready before Week 3."]],
      [12, 55, 33], bold_first=True)
spacer(d, 10)
callout(d, "The judgement call you will have to make around 1:05",
        "If a substantial part of the room is still not installed by 1:05, do not push on and leave them behind. "
        "Split: send the students who are READY into the terminal and notebook work with a written task sheet and "
        "two helpers, and stay with the stuck group yourself. A cohort where sixty per cent are set up and forty "
        "per cent are lost is a much worse Week 3 than a cohort where everyone is set up and slightly behind on "
        "notebooks. The notebook material can be recovered in twenty minutes at the start of Week 3. A broken "
        "environment cannot.", MID_H, LIGHT_H)

# ================================================================
h1(d, "6. Floor helper briefing")
para(d, "Six to eight per cohort, identified from the Week 1 survey — students with any prior exposure to a "
        "computer beyond a phone. They must complete their own setup before the session, in office hours the week "
        "before, so they have already met the problems.")
para(d, "Brief them on exactly four things.")
table(d, ["Rule", "Why"],
      [["Ask, do not type. Never touch another student's keyboard. Ask them what they typed and what it said.",
        "A helper who fixes it leaves the student unable to fix it next time. A helper who asks leaves them able."],
       ["Read the error message out loud, together, to the last line.",
        "Most beginners do not read errors at all. Modelling that once teaches more than the fix."],
       ["Three specific escalations come straight to the lecturer: 'No matching distribution found', a missing "
        "administrator password, and any hardware that is clearly not going to run this.",
        "These three cannot be solved by a peer, and a helper spending twenty minutes on one is worse than useless."],
       ["Enforce the five-minute rule on other people. If you see someone quiet and stuck, go to them.",
        "The students who most need help are the least likely to raise a hand. This is the helper's most valuable "
        "function."]],
      [56, 44], bold_first=True)

# ================================================================
page_break(d)
h1(d, "7. Break and Fix — the four broken notebooks")
para(d, "Build these before the session and distribute them offline. Teams get all four and must name the cause of "
        "each in one sentence. Nothing is being installed or repaired for real; the point is to meet four error "
        "messages under controlled conditions, so that meeting them alone in Week 5 is not frightening.")
table(d, ["#", "The fault to plant", "What they should see", "The sentence you are listening for"],
      [["1", "A notebook that imports a package which is not installed — use a plausible name that is genuinely "
             "absent, e.g. an import of a package the course does not use.",
        "ModuleNotFoundError: No module named '...'",
        "'The package is not installed for the Python this notebook is using.'"],
       ["2", "A notebook saved with a kernel that does not exist on their machine, or pointed at the wrong Python.",
        "Kernel selection prompt, or imports failing that work fine in the terminal",
        "'The notebook and the terminal are using two different Pythons.'"],
       ["3", "A notebook that reads a CSV by a path that is correct only if you are in a different folder.",
        "FileNotFoundError with the path in the message",
        "'Python is looking in the folder it was started in, not the one the file is in.'"],
       ["4", "A notebook whose cells produce the WRONG answer when run top to bottom, because it was saved after "
             "being run out of order — the classic accumulator run twice.",
        "No error at all. A plausible but wrong number.",
        "'It ran without complaining and the answer is still wrong.'"]],
      [4, 34, 28, 34], bold_first=True)
spacer(d, 10)
callout(d, "Number four is the one that matters",
        "The first three throw an error, and an error is a gift — it tells you something is wrong. The fourth "
        "produces a clean, confident, wrong answer, and that is the failure mode that will destroy their Week 10 "
        "model and their Week 14 test. Spend the last three minutes of the exercise on it, and name the habit that "
        "prevents it: Restart & Run All before you believe anything.\n\n"
        "This is also the moment to tell them that from Week 5 their submitted work is checked by a machine that "
        "does exactly that, from a clean start. It lands much better here, as a helpful warning, than in Week 5 as "
        "a rule.", "C00000", RED_H)

# ================================================================
h1(d, "8. Contingencies")
table(d, ["If this happens", "Do this"],
      [["The network is down entirely",
        "Nothing in the session actually needs the internet except creating GitHub repositories. Run everything "
        "else from USB. Move the Git and GitHub block to the start of Week 3 and use the recovered time on the "
        "notebook. Run CP0 on the paper copies you printed."],
       ["The power is out",
        "Students arrive charged because the Setup Guide told them to, which buys you the session. Teach the tool "
        "map from the printed cheat sheet and the board. If it is a scheduled outage, swap this session with "
        "Week 3 — Python fundamentals need far less machine time."],
       ["The share exists but students cannot reach it",
        "Switch entirely to USB plus peer-to-peer and announce it immediately rather than letting people keep "
        "trying. This is why you test the share from a student account beforehand."],
       ["A student's laptop cannot run this at all",
        "Move them to Colab for the session, note it on the roster, and book a lab machine. Do not spend session "
        "time diagnosing old hardware — it is the least recoverable use of your attention in the room."],
       ["More than about a fifth of the cohort is still stuck at 1:05",
        "Split the room as described at the end of Section 5. Then hold an extra clinic in office hours that week "
        "and make it explicit that Week 3 assumes a working environment."],
       ["You run out of time before Git and GitHub",
        "Acceptable. Move it to the first twenty minutes of Week 3. A2's deadline is the start of Week 3, so shift "
        "it to the end of Week 3 and say so in writing."],
       ["You run out of time before the notebook",
        "Also acceptable, and better than leaving people uninstalled. Recover it at the start of Week 3."],
       ["You run out of time before the installs are done",
        "Not acceptable. Everything else in this session can move; this cannot. Protect it by starting the copying "
        "at 0:00 and by having enough helpers."]],
      [30, 70], bold_first=True)

# ================================================================
page_break(d)
h1(d, "9. After the session")
table(d, ["When", "Task"],
      [["Immediately after", "Note on the roster who is NOT set up. That list is the office-hours priority for the "
        "week, and it is much easier to write down in the room than to reconstruct later."],
       ["Same day", "Run collect_roster.py over the roster to catch duplicate IDs, GitHub URLs pasted instead of "
        "usernames, and any student recorded as having neither a laptop nor a Colab route. Fix those before Week 3."],
       ["Same day", "Export the roster for the grading tools with collect_roster.py --export-assessment-roster, so "
        "pull_submissions.sh works from Week 3 onwards."],
       ["Within 2 days", "Look at the CP0 responses by question. It is ungraded, so read it purely as a map of who "
        "and what is not ready. A question most of the room got wrong is a five-minute reteach at the start of "
        "Week 3."],
       ["Within 2 days", "Write down what went wrong in the session, while it is fresh. Two cohorts have not sat it "
        "yet — the Friday cohorts get the benefit of what you learn on Tuesday, and next year gets a much better "
        "guide."],
       ["Before Week 3", "Confirm every student has either READY from check_setup.py or a Colab route. Week 3 "
        "teaches Python on the assumption that Python runs."]],
      [16, 84], bold_first=True)

spacer(d, 14)
h1(d, "10. The measure of success")
para(d, "Not that everybody finished. That is unlikely with a hundred beginners and it is not the right target. The "
        "session has succeeded if three things are true at the end of it.")
para(d, "Every student either has a working environment or a named, written route to one by the end of the week. "
        "Every student has seen four error messages and understands that an error message is information rather "
        "than a verdict. And every student has run one line of code that produced a number from their own "
        "discipline — because that is the moment a beginner stops believing this is not for them.")

spacer(d, 12)
callout(d, "One sentence worth saying out loud, twice",
        "\"Everything you are about to see go wrong has gone wrong for every engineer in this building, including "
        "me, this week.\"", NAVY_H, LIGHT_H)

spacer(d, 10)
para(d, "Runsheet version 1.0 · IUEA Faculty of Engineering · to be revised the same day it is first used",
     size=9, italic=True, colour=GREY, align=AL.CENTER)

d.save(OUT)
print("saved", OUT)
