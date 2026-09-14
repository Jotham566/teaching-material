# -*- coding: utf-8 -*-
"""Student Setup Guide — student-facing, printable."""
import sys
import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_HERE)
sys.path.insert(0, _HERE)
from docx.enum.text import WD_ALIGN_PARAGRAPH as AL
from docxkit import *      # noqa
from docxkit import _border

OUT = _ROOT + "/IUEA_Teaching_Plan/IUEA_ML_Student_Setup_Guide.docx"

d = new_doc(margin_cm=2.1)
header_footer(d, "IUEA · Introduction to Machine Learning · CML3111 / CML3112 / CML3113 · Student Setup Guide")
first_page_different(d)

# ---------------------------------------------------------------- cover
spacer(d, 40)
para(d, "INTERNATIONAL UNIVERSITY OF EAST AFRICA · FACULTY OF ENGINEERING",
     size=10.5, bold=True, colour=MID, align=AL.CENTER, after=20)
para(d, "Setting Up Your Computer", size=26, bold=True, colour=NAVY, align=AL.CENTER, after=4)
para(d, "Everything you need before Week 2", size=15, colour=MID, align=AL.CENTER, after=18)
p = para(d, "CML3111  ·  CML3112  ·  CML3113        INTRODUCTION TO MACHINE LEARNING",
         size=10.5, bold=True, align=AL.CENTER, after=8, before=8)
_border(p, "top", NAVY_H, 10)
_border(p, "bottom", NAVY_H, 10)
spacer(d, 20)

callout(d, "Read this first — it will save you an hour",
        "You will do all of this together, in class, in Week 2, with help in the room. You are not expected to do "
        "it alone tonight. What you ARE asked to do before Week 2 takes about fifteen minutes and is on the next "
        "page.\n\n"
        "Nothing here can break your laptop. You will see error messages. Everyone does. An error message is the "
        "computer telling you what it needs — it is information, not a telling-off.", MID_H, LIGHT_H)

spacer(d, 10)
callout(d, "SUPERSEDED IN PART — read this before issuing (lecturer note)",
        "The course has since moved to Google Colab as the primary environment, so most students will NOT install "
        "anything and Sections 3, 4 and 6 of this guide do not apply to them. Section 8, the Colab route, is now "
        "the main path rather than the fallback.\n\n"
        "This guide remains correct and needed for: the laboratory machines used in the Week 7 and Week 14 offline "
        "tests, any student who prefers a local setup, and as the fallback if Colab is unreachable. Revise it "
        "Colab-first before issuing it to students.", "C00000", RED_H)
spacer(d, 10)
para(d, "PRINT THIS AND BRING IT. The campus network will be busy in Week 2, and paper works when wifi does not.",
     size=10, bold=True, colour=RGBColor(0xC0, 0x00, 0x00), align=AL.CENTER)
spacer(d, 12)
para(d, "If you do not have a laptop, that is fine and you are not behind. Turn to Section 8.",
     size=10, italic=True, colour=GREY, align=AL.CENTER)
page_break(d)

# ---------------------------------------------------------------- 1
h1(d, "1. Before you come to Week 2")
para(d, "Four things, about fifteen minutes in total. Do them wherever your internet is best — at home, in the "
        "library, at a friend's place. Not in the Week 2 class, because two hundred people will be trying to use "
        "the network at once.")

table(d, ["#", "Do this", "How long", "Why"],
      [["1", "Create a GitHub account at github.com. Use the username format the lecturer gives you in Week 1, so "
             "your work can be found. Write your username on this page.", "5 min",
        "This is where all your work for the year will live, and how you prove it is yours."],
       ["2", "Create a Kaggle account at kaggle.com.", "3 min",
        "This is where you will find engineering datasets from Week 5 onwards."],
       ["3", "Charge your laptop fully, and find out your administrator password. If someone else set up your "
             "laptop, ask them for it now.", "—",
        "Installing software needs that password. Without it you will be stuck five minutes in, and nobody in the "
        "room can help you."],
       ["4", "Bring your laptop, your charger, and this printed guide.", "—",
        "Sockets are limited. A charged battery means you are not fighting for one."]],
      [4, 46, 10, 40], bold_first=True)
spacer(d, 10)

para(d, "My GitHub username is: ______________________________          "
        "My laptop is:   Windows  /  Mac  /  Linux  /  I don't have one", size=10.5, bold=True)
spacer(d, 8)
callout(d, "One warning that matters more than it looks",
        "Do NOT install Python at home before the class unless you are told to. The course installs one specific "
        "version of Python, and all the other software on the course USB is built to match it exactly. If you "
        "install a different version, none of it will fit, and there is no way to fix that during the session. "
        "Wait for Week 2. It takes ten minutes there.", "C00000", RED_H)

# ---------------------------------------------------------------- 2
h1(d, "2. What we are installing, and what each thing is for")
para(d, "Six pieces of software. That sounds like a lot; it is not, because each one answers a different question "
        "and you will meet them one at a time. Nobody memorises tools. You just need to know which one to reach "
        "for.")

table(d, ["Software", "The question it answers", "You will use it"],
      [["Python", "What actually runs the instructions I write?", "Every week, all year"],
       ["VS Code", "Where do I write, run and fix code?", "Every week"],
       ["Jupyter (inside VS Code)", "Where can I try things out on data and see the answer immediately?",
        "Every week from Week 5"],
       ["Git and GitHub", "How do I keep my work safe, see what I changed, and prove it is mine?",
        "Every week — every piece of assessed work is submitted through it"],
       ["The course packages\n(numpy, pandas, matplotlib, seaborn, scikit-learn)",
        "How do I handle thousands of measurements, draw them, and build a model?", "From Week 5 onwards"],
       ["A terminal (Command Prompt, Git Bash or Terminal)",
        "How do I tell the computer where things are and run things?", "A few commands only — about four"]],
      [24, 46, 30], bold_first=True)
spacer(d, 10)
para(d, "That is the whole toolkit for Semester 1. We are deliberately not installing anything else. Six tools "
        "learned properly beat twenty met once.")

# ---------------------------------------------------------------- 3
h1(d, "3. Stage 1 — Install Python")
para(d, "Python is the language. Installing it is the one step where a small mistake costs you the whole session, "
        "so read the two warnings.")

h3(d, "Windows")
para(d, "Open the course USB or the network share folder the lecturer names. Inside the 'installers' folder, find "
        "the Python installer and double-click it.")
callout(d, "The one box everybody misses",
        "On the FIRST screen of the Python installer there is a small tick-box near the bottom that says "
        "\"Add python.exe to PATH\" (older versions say \"Add Python to PATH\"). TICK IT. Then click Install Now.\n\n"
        "If you miss it, Python installs but your computer cannot find it, and every command afterwards fails with "
        "'python is not recognized'. The fix is to run the installer again and tick the box.", "C00000", RED_H)

h3(d, "macOS")
para(d, "Open the installers folder on the USB, double-click the Python .pkg file, and follow the prompts. There is "
        "no PATH box to tick on macOS.")

h3(d, "Linux")
para(d, "Most Linux laptops already have a suitable Python. Skip to Stage 2 and let the verification in Stage 5 "
        "tell you whether you need anything. If it says your version is too old, ask a helper — the command "
        "depends on which Linux you have.")

h3(d, "Check it worked")
para(d, "Open a terminal. On Windows press the Start key, type cmd and press Enter. On macOS press Command and "
        "Space, type terminal and press Enter. Then type this and press Enter:")
para(d, "        python --version", size=10.5, bold=True)
para(d, "You should see a version number printed back. If Windows says 'python is not recognized', try 'py "
        "--version' instead; if that works, use 'py' wherever this guide says 'python'. If neither works, re-run "
        "the installer and tick the PATH box.")

# ---------------------------------------------------------------- 4
h1(d, "4. Stage 2 — Install VS Code and two extensions")
para(d, "VS Code is where you will write code. It is a text editor that knows about Python: it colours your code, "
        "points at your mistakes before you run them, and lets you run things without leaving the window.")
para(d, "From the installers folder, run the VS Code installer and accept the defaults. On Windows, if it offers "
        "\"Add to PATH\" or \"Open with Code\", accept those too.")
para(d, "Then two extensions, which are the parts that make it understand Python. They are large downloads, so "
        "they are on the USB as files ending in .vsix and you install them from there:")
table(d, ["Step", "What to do"],
      [["1", "Open VS Code."],
       ["2", "Click the Extensions icon in the left-hand bar — it looks like four small squares, one detached."],
       ["3", "At the top of that panel click the '...' menu, then choose 'Install from VSIX...'."],
       ["4", "Select the Python .vsix file from the USB. Wait for it to finish."],
       ["5", "Repeat for the Jupyter .vsix file."],
       ["6", "Close VS Code and open it again."]],
      [8, 92], bold_first=True)

# ---------------------------------------------------------------- 5
h1(d, "5. Stage 3 — Install Git and tell it who you are")
para(d, "Git records every version of your work. GitHub is the website that stores it. Together they are how you "
        "submit everything this year, and how a marker sees that you did the work rather than one teammate.")

h3(d, "Windows")
para(d, "Run the Git installer from the USB and accept the defaults throughout. This also gives you a terminal "
        "called Git Bash, which we will use in class — it understands the same commands as the Mac and Linux "
        "machines, so everyone in the room can follow one set of instructions.")

h3(d, "macOS and Linux")
para(d, "Type 'git --version' in a terminal. If it prints a version, you already have it. On macOS, if it offers "
        "to install developer tools, accept.")

h3(d, "Now tell Git who you are — everybody must do this")
para(d, "Git refuses to record a change without a name attached. Type these two commands, replacing the name and "
        "email with your own. Keep the quotation marks.")
para(d, '        git config --global user.name "Your Full Name"', size=10.5, bold=True, after=2)
para(d, '        git config --global user.email "your.email@example.com"', size=10.5, bold=True)
para(d, "Use the same email address as your GitHub account. Nothing is printed when these work — silence means "
        "success. You only ever do this once.")

# ---------------------------------------------------------------- 6
h1(d, "6. Stage 4 — Install the course packages, offline")
para(d, "These five packages are what turn Python into an engineering tool. They are already downloaded onto the "
        "course USB, so this step needs no internet at all.")

callout(d, "Do not try to install these from the internet during class",
        "You will see instructions online telling you to run 'pip install pandas'. Do not do that in Week 2. A "
        "hundred people downloading the same few hundred megabytes over one campus connection does not work — it "
        "will time out and you will lose the session. Install from the USB. It takes about a minute and needs no "
        "network.", "C55A11", AMBER_H)

para(d, "Copy the whole course folder from the USB or the network share onto your own laptop first — put it "
        "somewhere you will find again, such as Documents. Work from your copy, not from the USB. Then:")
table(d, ["If you are on", "Do this"],
      [["Windows", "Open the copied folder, go into 'setup', and double-click install_offline_windows.bat. A black "
                   "window opens and prints what it is doing. Let it finish."],
       ["macOS or Linux", "Open a terminal in the copied 'setup' folder and run:    bash install_offline_unix.sh"]],
      [18, 82], bold_first=True)
spacer(d, 8)
para(d, "When it finishes it automatically runs the check in Stage 5, so you will see straight away whether it "
        "worked. If the script says it cannot find the wheels folder, you have probably copied only part of the "
        "course folder — copy it again.")

# ---------------------------------------------------------------- 7
page_break(d)
h1(d, "7. Stage 5 — Prove it works")
para(d, "This is the part that counts. One command tells you whether your computer is ready for the rest of the "
        "year, and it tells you in plain language what to do about anything that is not.")
para(d, "In a terminal, in the 'setup' folder, run:")
para(d, "        python check_setup.py", size=10.5, bold=True)
para(d, "It prints a line per item — PASS, WARN or FAIL. A WARN is fine. A FAIL comes with a sentence telling you "
        "exactly what to do; read it and do that, then run the command again. Keep going until it says READY.")
para(d, "At the end it prints a block between the lines 'BEGIN COPY' and 'END COPY'. Copy that block. You need it "
        "for your first assignment, and it is the evidence that your environment works.")

h3(d, "Then run your first program")
para(d, "In the 'setup/first_code' folder there is a file named for your course. Open it in VS Code and read it "
        "before you run it — most of it is comments written for you. Then run it:")
para(d, "        python first_code/hello_engineering_CML3112.py", size=10.5, bold=True)
para(d, "using your own course code in place of CML3112. It will greet you and work out something from your own "
        "discipline. Then do what the comments at the bottom tell you: change a number, run it again, and watch "
        "the answers move. Then break it on purpose and read the error. That last instruction is not a joke — "
        "being unafraid of error messages is most of learning to program.")

h3(d, "Then open your first notebook")
para(d, "In VS Code, open setup/week02_first_notebook.ipynb. Click the first cell and press Shift and Enter "
        "together. Work through it. It is short, and it deliberately shows you the single most common way "
        "notebooks confuse people, so that you meet it now rather than in a test in December.")
para(d, "If VS Code asks you to 'Select Kernel', choose the Python you just installed. If you are not sure which, "
        "ask — picking the wrong one is a very common and very confusing mistake.")

h3(d, "Then put it on GitHub")
para(d, "The lecturer will walk the room through this together, because the first time is fiddly. Four commands, "
        "run in your course folder:")
para(d, "        git init", size=10.5, bold=True, after=1)
para(d, "        git add .", size=10.5, bold=True, after=1)
para(d, '        git commit -m "First commit: environment working"', size=10.5, bold=True, after=1)
para(d, "        then the two lines GitHub shows you on your new empty repository page", size=10.5, bold=True)
para(d, "When you can see your files on the github.com website, you are done, and you have submitted your first "
        "piece of work for the year.")

# ---------------------------------------------------------------- 8
h1(d, "8. If you do not have a laptop — the Colab route")
para(d, "This is a supported route, not a lesser one. Several students take it every year and it is used in "
        "professional practice. You will do the whole course in a web browser instead, using Google Colab, which "
        "is free and needs only a Google account.")
para(d, "Say so in Week 1 when the laptop survey goes round, so that a laboratory machine is booked for you where "
        "one is needed and so that the lecturer knows to check on you in Week 2.")
table(d, ["What changes", "What does not"],
      [["You open colab.research.google.com instead of VS Code. Notebooks run on Google's computers.",
        "Everything you learn. Same Python, same packages, same notebooks, same assessment."],
       ["The packages are already installed — you skip Stages 1, 2, 4 and 6 entirely.",
        "You still need GitHub, and you still need Git configured. Colab can save straight to GitHub."],
       ["You need a connection while you are working, so plan where you will work.",
        "You still get the same marks and sit the same tests."]],
      [50, 50], bold_first=True)
spacer(d, 8)
callout(d, "The one real limitation, so it does not surprise you",
        "The two practical tests in Weeks 7 and 14 are sat offline, on laboratory machines, with no internet. That "
        "is the same for everyone in the class, including students with their own laptops. So make sure you have "
        "used a laboratory machine at least once before Week 7 — the lecturer will arrange a session. Do not let "
        "the first time be the test.", "C55A11", AMBER_H)

# ---------------------------------------------------------------- 9
page_break(d)
h1(d, "9. When something goes wrong")
para(d, "It will, for about a third of the room, and that is normal. Find your error message below. If you cannot, "
        "raise your hand — but first read the message properly, because it very often says exactly what is wrong.")

table(d, ["What you see", "What it means", "What to do"],
      [["'python' is not recognized as an internal or external command",
        "Windows cannot find Python. Almost always the PATH tick-box was missed.",
        "Try 'py --version'. If that works, use 'py' everywhere instead. Otherwise run the Python installer again "
        "and tick 'Add python.exe to PATH'."],
       ["command not found: python  (macOS/Linux)",
        "Same thing, different wording.",
        "Try 'python3 --version'. If that works, use 'python3' everywhere in this guide."],
       ["ModuleNotFoundError: No module named 'pandas'",
        "Python is working, but the package is not installed — or is installed for a different Python than the one "
        "running.",
        "Re-run the offline installer from Stage 4, then check_setup.py. If check_setup says READY but your "
        "notebook still fails, you have the wrong kernel selected — see the next row."],
       ["It works in the terminal but not in the notebook",
        "The notebook is using a different Python from your terminal.",
        "In VS Code, click the kernel name at the top right of the notebook and choose the same Python that "
        "check_setup.py reported. This is the single most common confusion of Week 2."],
       ["Please tell me who you are  (from Git)",
        "You have not set your Git name and email.",
        "Run the two 'git config --global' commands in Stage 3. Then try again."],
       ["No matching distribution found  /  ERROR: Could not find a version",
        "Your Python version does not match the packages on the USB. This is the one problem that cannot be fixed "
        "quickly in class.",
        "Tell a helper immediately, do not keep trying. You will be moved onto Colab for the session and sorted "
        "out afterwards. This is why the guide says not to install Python at home."],
       ["Permission denied  /  Access is denied",
        "You are trying to write somewhere you are not allowed, or you do not have the administrator password.",
        "Move the course folder into your own Documents folder and work there. If the installer itself is refused, "
        "you need the administrator password."],
       ["FileNotFoundError: ... .csv",
        "Python is looking in a different folder from the one the file is in.",
        "Check the terminal is in the right folder. Type 'pwd' (or 'cd' alone on Windows) to see where you are."],
       ["The installer window flashes and disappears",
        "It ran and closed too fast to read, or it crashed instantly.",
        "Open a terminal in the setup folder and run the installer from there instead, so the output stays on "
        "screen where you can read it."],
       ["Nothing happens at all when I press Shift+Enter",
        "No kernel is running, or no cell is selected.",
        "Click directly on the cell first. If VS Code asks to Select Kernel, choose your Python."]],
      [24, 33, 43], bold_first=True)
spacer(d, 10)

callout(d, "The five-minute rule",
        "If you are stuck on the same thing for more than five minutes in Week 2, put your hand up. Do not sit "
        "quietly watching a progress bar and do not restart your laptop hoping. There are trained helpers in the "
        "room whose whole job that session is to unstick people, and the session is only three hours long.\n\n"
        "When you ask, say three things: what you were trying to do, what you typed, and what it said back. That "
        "is not a hurdle put in front of help — it is the actual skill, and you will use it for the rest of your "
        "career.", MID_H, LIGHT_H)

# ---------------------------------------------------------------- 10
h1(d, "10. What you submit, and by when")
para(d, "Assignment A2 is due at the start of your Week 3 session. It is small, and it is the gate for Week 3 — "
        "you cannot do Week 3's work on a computer that is not set up.")
table(d, ["What", "Detail"],
      [["A GitHub repository", "Named as the lecturer specifies. It must contain the 'BEGIN COPY' block from "
                               "check_setup.py, your notebook, and your first_code file."],
       ["A README file", "Three short things: your name and course code, one engineering problem in your own "
                         "discipline that you think data could help with, and one sentence on what data that would "
                         "need."],
       ["One sentence of honesty", "What you had to fix to get set up, or 'nothing' if it worked first time. This "
                                   "is worth marks. What went wrong for you is useful information — it is how next "
                                   "year's guide gets better."],
       ["How to submit", "Paste your repository URL where the lecturer tells you. That is all."]],
      [22, 78], bold_first=True)
spacer(d, 10)
para(d, "If you cannot get set up by the end of Week 2, you are not in trouble — but you must come to office hours "
        "that week. Do not wait until Week 4 and hope it resolves itself. It will not, and by then you will be two "
        "sessions behind on work that builds on itself every week.")

# ---------------------------------------------------------------- cheat sheet
page_break(d)
h1(d, "Command cheat sheet — keep this page")
para(d, "These are all the terminal commands you need for the whole of Semester 1. There are eleven. On Windows, "
        "use Git Bash so these work exactly as written.", after=12)

table(d, ["Command", "What it does"],
      [["python --version", "Which Python am I using? (Windows: try 'py' or Mac/Linux 'python3' if this fails)"],
       ["pwd", "Which folder am I in right now? (Windows Command Prompt: type 'cd' alone)"],
       ["ls", "What is in this folder? (Windows Command Prompt: 'dir')"],
       ["cd foldername", "Go into that folder"],
       ["cd ..", "Go back up one folder"],
       ["python myfile.py", "Run a Python file"],
       ["python check_setup.py", "Check my environment is still healthy"],
       ["git status", "What have I changed since my last commit? Run this constantly."],
       ["git add .", "Mark everything I changed as ready to record"],
       ["git commit -m \"message\"", "Record it, with a note saying what you did"],
       ["git push", "Send it up to GitHub"]],
      [30, 70], bold_first=True, font=9.5)
spacer(d, 14)

callout(d, "Three habits worth more than any command",
        "Run 'git status' before and after everything until it becomes automatic. It answers 'what is going on?' "
        "and it is the single most useful command in this list.\n\n"
        "In notebooks, use Restart & Run All before you submit anything. If it fails, your marker's copy will fail "
        "too — and from Week 5 your work is checked by a machine that does exactly that.\n\n"
        "Read the last line of an error message first. That is where Python says what it actually wanted.",
        NAVY_H, LIGHT_H)

spacer(d, 12)
para(d, "Setup Guide version 1.0 · issued Week 1 · IUEA Faculty of Engineering",
     size=9, italic=True, colour=GREY, align=AL.CENTER)

d.save(OUT)
print("saved", OUT)
