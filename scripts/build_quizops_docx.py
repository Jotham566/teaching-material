# -*- coding: utf-8 -*-
"""The quiz operations guide: how to set it up, and how to run it on the day."""
import sys

import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_HERE)
sys.path.insert(0, _HERE)
from docx.enum.text import WD_ALIGN_PARAGRAPH as AL
from docxkit import *      # noqa
from docxkit import _border

OUT = (_ROOT + "/IUEA_Teaching_Plan/"
       "IUEA_ML_Weekly_Quiz_Operations_Guide.docx")

d = new_doc(margin_cm=2.0)
header_footer(d, "IUEA Faculty of Engineering · Weekly quizzes · "
                 "setup and run guide")
first_page_different(d)

spacer(d, 26)
para(d, "INTERNATIONAL UNIVERSITY OF EAST AFRICA · FACULTY OF ENGINEERING",
     size=10, bold=True, colour=MID, align=AL.CENTER, after=14)
para(d, "Weekly Quizzes: Setup and Run Guide", size=24, bold=True, colour=NAVY,
     align=AL.CENTER, after=4)
para(d, "Twelve quizzes · three cohorts · 36 Google Forms", size=12,
     colour=MID, align=AL.CENTER, after=18)

callout(d, "Read part 1 once, on your own, before a class ever sees this",
        "Part 1 is the one-off build and a dry run you do alone: create the forms, "
        "scan your own QR, submit as a fake student, and confirm the mark reaches the "
        "gradebook. It takes about an hour and it is the only way to find out that "
        "something is wrong while it still costs nothing.\n\n"
        "Part 2 is the ten minutes before a session and the five minutes of the quiz "
        "itself. It is short on purpose. Once part 1 is done, running a quiz is three "
        "clicks.\n\n"
        "Part 3 is what to do when the network fails, which over twelve sittings it "
        "will at least once.",
        "2E5C8A", LIGHT_H)

# ==========================================================================
page_break(d)
h1(d, "Part 1 · One-off setup and dry run")

h2(d, "1.1 What you are building")
para(d, "Thirty-six Google Forms: twelve quiz weeks for each of three cohorts. Each "
        "cohort gets its own form for each week because CML3112 sits on Tuesday and "
        "the two Friday cohorts sit three days later, so a shared form would let "
        "Tuesday's answers reach Friday's students. The slide decks are already "
        "per-cohort, so each deck simply carries its own code.")
para(d, "You do not create these by hand. One Apps Script creates all of them.")

table(d, ["File", "What it is", "Where it lives"],
      [["create_quiz_forms.gs", "The Apps Script that creates the 36 forms",
        "IUEA_Teaching_Plan/grader/"],
       ["quiz_banks.py", "The schema, Week 1 and the helpers. All twelve "
        "banks are written", "scripts/"],
       ["quiz_bank_weeks.py", "The banks for Weeks 2 to 13, sixty questions "
        "in all", "scripts/"],
       ["verify_quiz_arithmetic.py", "Re-executes every code snippet in the "
        "banks and checks the mix, style and cohort rules. Run it after any "
        "edit to a question", "scripts/"],
       ["attach_qr.py", "Generates the QR codes and puts them in the decks",
        "scripts/"],
       ["quiz_links.json", "The map of week and cohort to form URL. You create "
        "this from what the script prints", "data/"],
       ["gradebook.gs", "Already implements best ten of twelve",
        "IUEA_Teaching_Plan/grader/"]],
      [22, 50, 28], font=8.6)

spacer(d, 6)
callout(d, "How a student is identified: two keys, and why both",
        "Every response carries two identifiers. The first is the Google account the "
        "student is signed in to, which Forms collects on its own. That is the key that "
        "makes one attempt per student enforceable, because Forms recognises a returning "
        "account and refuses it.\n\n"
        "The second is a required short-answer field, 'Your registration number', which "
        "is the first item on every form. It is deliberately not called a student number: "
        "students read that phrase as a phone number, and the help text under the field "
        "says so outright. This is the key the gradebook joins on, so it arrives with the "
        "response instead of being reconstructed later from a roster you have to build "
        "and maintain.\n\n"
        "A typed field does not cost you the auto-marking. That was an early theory and "
        "it was wrong: the registration field is marked out of zero points, every scored "
        "question is multiple choice, and showScores prints the exact marks straight off "
        "the responses. What Forms does not do is print a running total on the student's "
        "confirmation page, and that is true with or without a typed field. Students see "
        "a tick or a cross per question and the feedback under anything they got wrong, "
        "which is the part worth reading anyway.\n\n"
        "Two keys also means two ways to find a student who claims a missing mark: by "
        "address in the response sheet, or by the number they typed.",
        "2E5C8A", LIGHT_H)

h2(d, "1.0 The template — do this before creating anything")
para(d, "One setting decides whether this whole design works, and no API can reach it. "
        "A quiz created programmatically comes out with 'Release grade: Later, after "
        "manual review', which also switches on 'Collect email addresses'. A student "
        "who submits then sees no score and no feedback, which removes the reason the "
        "quiz is worth five minutes of a three-hour session.")
para(d, "The setting is per-form, so correcting it by hand means thirty-six edits, and "
        "a rebuild silently undoes all of them. Configure one form instead and let the "
        "script copy it.")

table(d, ["#", "Do this", "What you should see"],
      [["1", "In the Apps Script, run setupTemplate.",
        "It creates one empty quiz form and logs its edit URL and its id."],
       ["2", "Open that URL. Settings, then Quizzes. Set 'Release grade' to "
             "'Immediately after each submission'.",
        "The option is selected. This is the only place this setting can be "
        "changed."],
       ["3", "Leave 'Collect email addresses' alone. The script sets it "
             "on every form.",
        "Students are identified by their signed-in account, which is what "
        "lets Forms show them a score. See the identity note in 1.1."],
       ["4", "Add no questions. Leave the form empty and close it.",
        "An empty form. Anything left on it would appear on all 36 copies, "
        "though the script does delete inherited items as a safeguard."],
       ["5", "Copy the id from the log into TEMPLATE_FORM_ID at the top of "
             "the script. Save.",
        "var TEMPLATE_FORM_ID = '1AbC...';"],
       ["6", "Run checkTemplate.",
        "It confirms quiz mode is on and that copying works. It cannot "
        "read the grade-release setting back, "
        "because no API can, so that one is on your eyes and on the dry "
        "run."]],
      [4, 46, 50], font=8.4)

spacer(d, 6)
callout(d, "If you skip this",
        "The script still runs and will tell you on every execution that no template "
        "is set. You then have to open all thirty-six forms and change the setting by "
        "hand, and repeat that after every rebuild. The five minutes spent on the "
        "template is the better trade.",
        "C55A11", AMBER_H)

spacer(d, 8)
callout(d, "Creating the forms takes two or three runs, and that is normal",
        "One form takes twelve to fifteen seconds to build, so thirty-six need about "
        "eight minutes. Apps Script stops every execution at six. createAllForms "
        "therefore stops itself at four and a half minutes, saves what it has done, "
        "and reports how many are left. Run it again. It skips everything already "
        "built, so each run gets further, and it announces ALL 36 FORMS EXIST when it "
        "is finished. Run status() at any point to see where you are. If you would "
        "rather work in predictable chunks, build_CML3112, build_CML3113 and "
        "build_CML3111 each do one cohort in about three minutes.",
        "1F6F8B", "DDEAF0")

h2(d, "1.2 Create the forms")
table(d, ["#", "Do this", "What you should see"],
      [["1", "Go to script.google.com, sign in with the Google account that "
             "will own the marks for the whole semester, and create a new "
             "project. Name it 'IUEA ML quizzes'.",
        "An empty Code.gs."],
       ["2", "Delete what is in Code.gs. Paste the whole of "
             "create_quiz_forms.gs. Save.",
        "Around 370 KB of script. No errors. If it reports a syntax error, "
        "see the note at the end of section 1.6."],
       ["3", "Choose createAllForms in the function dropdown and press Run.",
        "An authorisation prompt. It asks for Forms, Drive and Sheets on your "
        "own account, which is what it needs to create the forms and the "
        "response sheets."],
       ["4", "Wait about four and a half minutes. It will stop partway "
             "through and tell you how many forms are left.",
        "The log lists each form as it is created, then says NOT FINISHED "
        "with a count remaining. This is expected: see the note above."],
       ["5", "Run createAllForms again. Repeat until it says ALL 36 FORMS "
             "EXIST. Two or three runs in total.",
        "Each run skips what is already built and gets further. Run status() "
        "if you lose track."],
       ["6", "Look in Drive for a folder called 'IUEA ML Quizzes'.",
        "36 forms, one response spreadsheet per cohort, and a sheet called "
        "'IUEA ML Quiz Links' with every URL in it."],
       ["7", "Open ONE form. Settings, then Quizzes. Confirm 'Release grade' "
             "says 'Immediately after each submission', and that 'Collect "
             "email addresses' is off.",
        "If you set up the template in section 1.0 this will already be "
        "right, because each form is a copy of it. If it says 'Later, after "
        "manual review', go back to 1.0."]],
      [4, 46, 50], font=8.4)

spacer(d, 6)
callout(d, "Running it twice is safe",
        "createAllForms remembers what it built. Run it again and it skips every form "
        "that already exists and only creates what is missing, so it is the right thing "
        "to run after you author a new question bank. It will not duplicate anything or "
        "wipe a response.",
        "2E7D6F", GREEN_H)

h2(d, "1.3 Get the QR codes into the decks")
table(d, ["#", "Do this", "What you should see"],
      [["1", "In the Apps Script, run printLinksJson.",
        "The execution log prints a JSON block with 36 entries, keyed like "
        "\"CML3112|1\"."],
       ["2", "Copy that JSON and save it as quiz_links.json in the build "
             "folder, replacing the empty {} that is there now.",
        "A file with 36 links."],
       ["3", "Run: python3 attach_qr.py",
        "It generates 36 QR codes into qr/ and rebuilds all five deck "
        "builders. It ends with 'Each cohort's quiz slide now carries its own "
        "code.'"],
       ["4", "Open any deck and go to the last slide.",
        "A real QR where the placeholder square was. Scan it with your phone: "
        "it must open that cohort's form for that week."],
       ["5", "Run: python3 attach_qr.py --check",
        "A coverage table showing which weeks have links and which do not. "
        "Any week without one keeps the placeholder, so this is safe to run "
        "at any stage."]],
      [4, 46, 50], font=8.4)

spacer(d, 6)
para(d, "The QR codes are generated by qrgen.py, a QR encoder written for this course "
        "because no QR library was installable. Run python3 qrgen_selftest.py after "
        "any change to it. That self-test checks the Reed-Solomon arithmetic and all "
        "thirty-two format strings against published values, checks the finder, timing "
        "and alignment patterns of the finished matrix, round-trips strings through a "
        "decoder written separately, and then decodes every code with OpenCV, an "
        "outside implementation.")
callout(d, "Why that last step exists",
        "The first batch of QR codes produced for these decks did not scan at all. They "
        "were structurally perfect, the published-value checks passed, and the round "
        "trip through this project's own decoder passed, because the encoder and that "
        "decoder shared the same wrong convention for the format information and so "
        "agreed with each other. The bug was found only by decoding with an outside "
        "implementation. Treat a round trip through your own code as evidence of "
        "self-consistency and nothing more, and keep the phone scan as the final word.",
        "1F6F8B", "DDEAF0")

h2(d, "1.35 The clock: quiz_timer.html")
para(d, "Google Forms has no countdown and no auto-submit, and it still does not in "
        "2026. Every add-on that adds one works by hosting your form on the add-on's "
        "own site, which would break the forms.gle links your QR codes point at, put "
        "a graded assessment behind a third party, and meter it. A hundred students "
        "across twelve sittings is well past any free tier.")
para(d, "A projected clock also fits how this quiz actually runs. The class starts "
        "together on your word, so one clock everybody can see is the honest model. "
        "Per-student timers would only matter if the quiz were asynchronous.")
para(d, "Open IUEA_Teaching_Plan/quiz_timer.html in any browser. It needs no network "
        "and nothing installed. Press F for full screen, then Space to start when the "
        "room has scanned.")

table(d, ["What it does", "Detail"],
      [["Counts five minutes",
        "The working time. Buttons for 5, 6 and 10 minutes are there if you "
        "want a different length for a particular week."],
       ["Turns amber at two minutes",
        "And says that a blank scores the same as a wrong answer, which is "
        "the single most useful thing to tell a room with two minutes left."],
       ["Turns red at thirty seconds, then flashes at zero",
        "With a short beep at each of those points, so it works even when "
        "you are facing the class rather than the screen."],
       ["Space to start or pause, R to reset, F for full screen",
        "The clock is driven from the wall clock rather than by counting "
        "ticks, so a busy laptop cannot make it drift."],
       ["The form closes a minute after zero",
        "That minute is submission grace, so somebody who presses submit as "
        "the clock hits zero is not cut off. It is not extra thinking time "
        "and the form says so."]],
      [34, 66], font=8.4)

spacer(d, 6)
callout(d, "Keep the three numbers in step",
        "The working time appears in three places: WINDOW_MIN in "
        "build_quiz_timer.py, QUIZ_MIN in build_quiz_forms_gs.py, and "
        "QUIZ_WINDOW_MIN in the Apps Script, which is the closing time rather than "
        "the working time. Change one and change the others, or the clock on the "
        "wall, the text on the form and the moment it actually closes will disagree "
        "with each other in front of a class.",
        "C55A11", AMBER_H)

spacer(d, 8)
h2(d, "1.4 The dry run — do this before any class")
para(d, "Twenty minutes, alone, and it exercises every part of the chain. Do it on the "
        "Week 1 quiz, and repeat it on one later week once you have edited a bank.")

callout(d, "Submitting more than once while you test",
        "With one response per student switched on, your own second attempt is refused "
        "with \"You've already responded\". Forms has no per-person reset, so the only "
        "way to test repeatedly is to lift the limit.\n\n"
        "Run startTesting in the Apps Script. It lifts the limit on all thirty-six "
        "forms and reminds you on every run that it is off. Submit as often as you "
        "like. Your own address identifies the rows, so they are easy to find. When "
        "you are finished, run stopTesting, delete the TEST rows from the response "
        "sheets, and run findDuplicates to confirm nothing is left behind.\n\n"
        "testModeStatus tells you which state you are in. Run it before the first "
        "real sitting: if test mode is still on, a student can submit twice.",
        "2E5C8A", LIGHT_H)

spacer(d, 6)
table(d, ["#", "Do this", "Pass looks like"],
      [["0", "Run startTesting, so your own repeat submissions are allowed.",
        "'TEST MODE ON' and a count of forms updated."],
       ["1", "In the Apps Script, run open_W1_CML3112.",
        "The log says OPEN and prints the link. The form now accepts "
        "responses, and a trigger is set to close it 48 hours from now."],
       ["2", "Project the Week 1 CML3112 deck, go to the last slide, and scan "
             "the QR with your own phone.",
        "The form opens on your phone, titled 'CML3112 · Weekly Quiz 1 — What "
        "machine learning is'."],
       ["3", "Fill it in as a fake student. "
             "Get some questions right and some wrong on purpose.",
        "It submits."],
       ["4", "Look at your score. THIS IS THE STEP THAT MATTERS MOST.",
        "A score out of 5 appears immediately, with feedback under each "
        "question you got wrong. Read one: that feedback is the teaching. "
        "If instead you see only 'your response has been recorded', the "
        "grade-release setting is wrong on this form and section 1.0 is the "
        "fix. No API can read that setting, so this submission is the only "
        "way to know."],
       ["5", "Run closeStatus.",
        "It lists the quiz as open with its closing time about 48 hours "
        "away, and confirms one trigger is installed. If it says no trigger "
        "is installed, nothing will close the form and you must use "
        "close_W1_CML3112 by hand."],
       ["5b", "Run stopTesting, then try to submit a second time.",
        "Forms now refuses: one response per Google account. If it still "
        "lets you through, run applyResponseLimits, which fixes all 36 in "
        "place without new links."],
       ["6", "Open the response spreadsheet for CML3112 in the Drive folder.",
        "A sheet for Quiz 1 with a row for your own address, a timestamp and "
        "a score out of five."],
       ["7", "Delete your own test rows, then run testModeStatus and "
             "findDuplicates.",
        "Test mode off, no duplicates, and none of your own attempts left "
        "in the real marks."]],
      [4, 46, 50], font=8.4)

spacer(d, 6)
callout(d, "\"Operation not supported on unpublished form\"",
        "Google changed the rules on 30 June 2026: a form created by a script starts "
        "unpublished, and turning on responses is refused until it is published. "
        "Closing a form is still allowed, which is why creating all thirty-six looked "
        "fine and only opening one for a sitting failed. Run publishAllForms once and "
        "it repairs every form in place, keeping all the links, so no rebuild and no "
        "new QR codes are needed. Forms built from now on are published as they are "
        "created, and openQuizFor publishes anything it finds unpublished, so this "
        "should not recur. Note that published and open are different states: "
        "published means the link resolves, and the 48-hour window is the "
        "accepting-responses setting openQuizFor toggles.",
        "C55A11", AMBER_H)

spacer(d, 6)
callout(d, "What to do if step 2 fails",
        "If the QR will not scan, first check it is not a focus problem: scan the same "
        "code from QR_encoder_acceptance_test.png, which encodes example.com. If that "
        "scans and the quiz code does not, the URL in quiz_links.json is wrong. If "
        "neither scans, print the codes larger, or send the plain link to the class "
        "group as a fallback while you look into it. A quiz that students reach by a "
        "typed link still works.",
        "C55A11", AMBER_H)

spacer(d, 8)
h2(d, "1.5 What needs a rebuild, and what does not")
para(d, "Most changes do not need one. A rebuild replaces all thirty-six forms, which "
        "means new links and new QR codes in every deck, so it is worth knowing which "
        "changes actually require it before paying that cost.")

table(d, ["You changed", "What to run", "Rebuild?"],
      [["Feedback wording, a question stem, or the form description",
        "updateFeedbackAndIntro",
        "No. These live on items that already exist, so they can be "
        "rewritten in place. Links unchanged."],
       ["One-response-per-student, or the no-edits rule",
        "applyResponseLimits",
        "No. Form settings, applied in place."],
       ["How students identify themselves: email collection, or the wording "
        "of the registration-number field",
        "applyIdentityFields",
        "No. It adds the field if it is missing, renames it if it was called "
        "something else, keeps it worth zero points and first on the form, "
        "and switches on email collection. Links unchanged."],
       ["Nothing on the forms, only the script logic (the automatic close, "
        "the openers, a diagnostic)",
        "Nothing. Paste the new script and save.",
        "No. The forms are untouched."],
       ["A form will not open: 'Operation not supported on unpublished form'",
        "publishAllForms",
        "No. Publishes in place."],
       ["Deck wording, or the QR codes themselves",
        "python3 attach_qr.py",
        "No forms involved at all. Decks only."],
       ["THE OPTIONS on a question: added, removed, reordered, or a "
        "different answer marked correct",
        "armRebuild, then rebuildAllForms, then the sequence in 1.6",
        "YES. Rewriting choices resets the answer key, so the form has to "
        "be built again."],
       ["A whole new question, or a question deleted",
        "armRebuild, then rebuildAllForms, then the sequence in 1.6",
        "YES."]],
      [30, 30, 40], font=8.2)

spacer(d, 6)
callout(d, "The one-line rule",
        "Wording and settings can be changed in place. Only a change to the set of "
        "options, or to which option is correct, needs the forms rebuilt. "
        "updateFeedbackAndIntro checks every question title against the bank before "
        "it writes anything, and skips with a warning rather than risk putting one "
        "question's feedback onto another.",
        "1F6F8B", "DDEAF0")

spacer(d, 8)
h2(d, "1.6 Rebuilding, when you do need it")
para(d, "This is the section to come back to. Editing a question in the bank does not "
        "change the live form, and re-running createAllForms will not either: it skips "
        "any form that already exists, which is what makes it safe to re-run and also "
        "what stops it picking up your edit. Rebuilding is the way through, and it "
        "replaces all thirty-six forms, so every link changes and the QR codes in the "
        "decks go stale in the same moment.")

callout(d, "Do this before the semester starts, or between quizzes",
        "A rebuild moves the existing forms and their response sheets to the Drive "
        "trash. Anything students have already submitted goes with them. The script "
        "refuses to run if it finds submitted responses, and it can be overridden "
        "deliberately, so read what it tells you rather than working around it. If "
        "marks have been collected, export them first.",
        "C00000", RED_H)

para(d, "The full sequence, from editing a question to a working QR code on a slide:",
     after=6)

table(d, ["#", "Where", "Do this", "What you should see"],
      [["1", "scripts/",
        "Edit the question in quiz_bank_weeks.py. Week 1 lives in "
        "quiz_banks.py.",
        "Nothing yet. This file is the source of truth and nothing "
        "downstream has been touched."],
       ["2", "scripts/",
        "Run: python3 verify_quiz_arithmetic.py",
        "It ends with 'all checks passed'. If it does not, fix what it "
        "names before going further. It re-executes the code in every "
        "snippet, so it catches a claimed output that the code does not "
        "actually produce."],
       ["3", "scripts/",
        "Run: python3 build_quiz_forms_gs.py",
        "It saves create_quiz_forms.gs and prints how many forms will be "
        "created and which banks are authored."],
       ["4", "script.google.com",
        "Open the project, select all in Code.gs, and paste the new "
        "create_quiz_forms.gs over it. Save. Paste the whole file: a "
        "partial paste is the usual cause of a syntax error.",
        "It saves without complaint, and searching QUIZ_DATA finds your "
        "edited question text."],
       ["5", "script.google.com",
        "Run armRebuild.",
        "'Rebuild armed for the next 10 minutes.'"],
       ["6", "script.google.com",
        "Run rebuildAllForms, within those ten minutes.",
        "It trashes the old forms and response sheets, then starts building. "
        "It will run out of time partway and say REBUILD STARTED, NOT YET "
        "COMPLETE with a count."],
       ["7", "script.google.com",
        "Run createAllForms, repeatedly, until it says ALL 36 FORMS EXIST. "
        "Do NOT run rebuildAllForms again.",
        "Each run continues from where the last stopped. Two or three runs. "
        "Running rebuildAllForms again would trash the progress and loop "
        "forever."],
       ["8", "script.google.com",
        "Run printLinksJson.",
        "A JSON block with 36 entries. These are new links; the old ones are "
        "dead."],
       ["9", "data/",
        "Save that JSON over data/quiz_links.json.",
        "36 links in the file."],
       ["10", "scripts/",
        "Run: python3 attach_qr.py",
        "36 QR codes regenerated and all five deck builders re-run. Ends "
        "with 'Each cohort's quiz slide now carries its own code.'"],
       ["11", "IUEA_Teaching_Plan/decks/",
        "Open the deck for the week you changed and scan the QR on the quiz "
        "slide.",
        "It opens that cohort's form for that week, and the question you "
        "edited reads correctly. This is the step that proves the whole "
        "chain."],
       ["12", "script.google.com",
        "Open any one form and check Settings, then Quizzes, then Release "
        "grade.",
        "'Immediately after each submission'. With the template from "
        "section 1.0 in place this is inherited and needs only a glance. "
        "Without it, all 36 need changing by hand again."]],
      [4, 17, 38, 41], font=8.0)

spacer(d, 6)
para(d, "If step 6 says NOT ARMED, the ten minutes lapsed: run armRebuild again. If it "
        "says STOPPING and reports a number of responses, it has found submitted "
        "answers. Download those response sheets first, and only then run "
        "armRebuildEvenThoughResponsesExist followed by rebuildAllForms.")

callout(d, "If Apps Script reports a syntax error on line 1",
        "That message points at the top of the file and almost never means the top of "
        "the file is wrong. It happened once here because the generated script "
        "contained about seventeen hundred non-ASCII characters, the em dashes and "
        "typographic quotes the questions legitimately use, and something on the "
        "clipboard path corrupted them. build_quiz_forms_gs.py now writes those as "
        "\\uXXXX escapes and refuses to save a file that is not pure ASCII, so the "
        "text students read is unchanged and nothing in the file can be mangled by a "
        "copy and paste. If you do see the error, regenerate with "
        "build_quiz_forms_gs.py, then select all in Code.gs and paste the whole file "
        "again.",
        "C55A11", AMBER_H)
para(d, "Steps 7 to 11 are not optional. A rebuild that stops at step 6 leaves every "
        "deck pointing at a trashed form, which fails silently: the code scans, the "
        "browser opens, and the student sees a page saying the form is not available. "
        "Finish the sequence in one sitting.")

# ==========================================================================
page_break(d)
h1(d, "Part 2 · Running a quiz on the day")

para(d, "Once part 1 is done this is the whole procedure, and it fits in the last five "
        "minutes of the session.")

h2(d, "Ten minutes before the session")
table(d, ["#", "Do this"],
      [["1", "Open the Apps Script project on the teaching machine and leave the "
             "tab open. You will need it once, at the end."],
       ["2", "Have the deck open. The quiz is the last slide, so you do not need "
             "to find it."],
       ["3", "If this is a week whose questions you have not authored, the form is "
             "still a shell. Either author it now or tell the class plainly that "
             "this week's quiz is postponed, which costs nobody anything because "
             "the best ten of twelve count."]],
      [4, 96], font=8.6)

h2(d, "The last five minutes")
table(d, ["#", "Do this", "Why"],
      [["1", "Go to the quiz slide.",
        "The standing rules are on it, so you do not have to remember them."],
       ["2", "In the Apps Script, run the wrapper for this session — for "
             "example open_W4_CML3112.",
        "It opens the form and schedules the automatic close 48 hours from "
        "now. You do not have to remember to close it."],
       ["2b", "Put quiz_timer.html on the projector, full screen, and press "
              "Space as the last phone finishes scanning.",
        "The clock starts at five minutes. It turns amber at two and red at "
        "thirty seconds, so you do not have to watch it. At zero it tells "
        "anyone who had a problem that the form is open for 48 hours."],
       ["3", "Say: five questions, five minutes, one per cent. The first box "
             "wants the registration number from your student card. Tap View "
             "score once you have submitted.",
        "Students who know the stakes are low answer honestly, and an honest "
        "wrong answer is worth more to you than a guess. Saying the words "
        "'registration number' out loud saves the handful who would otherwise "
        "type a phone number, and the View score prompt is the only reason "
        "anybody reads the feedback."],
       ["4", "Watch the room rather than the screen, and say once that "
             "anyone who cannot get on now has until the day after tomorrow.",
        "It stops the two or three students with a dead phone or no data "
        "from spending the rest of the session worrying about one mark."],
       ["5", "At five minutes, stop talking about it and move on.",
        "The form stays open 48 hours for anyone whose network failed. You "
        "do not need to do anything: it closes itself."]],
      [4, 48, 48], font=8.4)

spacer(d, 6)
h2(d, "Immediately afterwards, before you leave the room")
para(d, "Open the form's responses and switch to the per-question view. Any question "
        "most of the room got wrong is a five-minute reteach at the start of next "
        "week, and you now know that before anybody has forgotten the session. Do it "
        "while the students who answered in the five minutes are still the majority: "
        "after two days the picture is muddied by late submissions.")

# ==========================================================================
page_break(d)
h1(d, "Part 3 · When it goes wrong")
para(d, "Over twelve sittings the network will fail at least once. None of these "
        "situations costs more than a few minutes, and most cost nothing, because the "
        "48-hour window and the best-ten-of-twelve rule between them absorb almost "
        "everything.")

table(d, ["What happened", "What to do", "What it costs"],
      [["The room network is down",
        "Nothing to announce and nothing to change: the window is already 48 "
        "hours and it is printed on the form. Open the quiz when you have "
        "signal and post the link in the group, and tell the class before "
        "they leave that it is coming.",
        "Nothing."],
       ["A student has no phone",
        "They use yours at the front, or they take it that evening. Both are "
        "on the slide.",
        "Nothing."],
       ["A student's phone will not scan",
        "Read the short link out. It is on the links sheet, and forms.gle "
        "links are short enough to type.",
        "A minute."],
       ["You forget to open the form",
        "Open it whenever you remember and post the link in the group. The "
        "window runs 48 hours from the moment you open it, so a quiz opened "
        "the evening after the session is still a full-length window.",
        "Nothing."],
       ["You forget to close the form",
        "You will not, because opening it schedules the close. If the trigger "
        "fails, run closeEverything, which shuts all 36.",
        "Nothing, if caught the same day."],
       ["A student submits twice",
        "The first submission from that account counts. Say so once, in "
        "Week 1.",
        "Nothing."],
       ["A whole cohort misses a sitting",
        "Nothing to arrange. Best ten of twelve absorbs two, and this is the "
        "main reason that rule exists rather than a resit window.",
        "Nothing, for up to two weeks."],
       ["You need to change a question after students have answered",
        "Do not edit a live form. Fix quiz_banks.py, delete that one form in "
        "Drive, and run createAllForms again to rebuild just that one.",
        "Five minutes, and the responses to the old version are lost."]],
      [24, 52, 24], font=8.4)

spacer(d, 8)
h2(d, "Every form is open when it should not be")
para(d, "Publishing a form switches accepting-responses ON. That is the opposite of "
        "what is wanted between sittings, and it means a run of publishAllForms on an "
        "older build of the script left all thirty-six quizzes answerable at once. A "
        "student with any link could have taken Week 13 in Week 1.")
para(d, "Run auditAll. The line to read is 'currently OPEN to answers'. It should be 0 "
        "between sittings, or 1 while a quiz is being sat. If it is 36, run "
        "closeEverything. The current script closes each form again straight after "
        "publishing it, and leaves alone whichever quiz is mid-sitting, so this should "
        "not recur.")

spacer(d, 8)
h2(d, "Where the mark actually is")
para(d, "Google Forms does not put a total on the page a student lands on after "
        "submitting. It gives them a tick or a cross on each of the five questions "
        "with the feedback underneath, and that is all. Verified on the live account: "
        "the marking itself is correct, and showScores reads back exact totals such "
        "as 3 out of 5 for every submission.")
para(d, "So say it in the room once, in Week 1, and it stops being a question: your "
        "mark is the number of ticks, out of five. The feedback under anything you got "
        "wrong is the part worth reading. Nobody needs to write a number down, because "
        "the real figure goes to the gradebook from the response sheet.")
para(d, "If you want the totals for a week at any point, run showScores or the "
        "show_W1_CML3111 wrapper. It prints every submission with its score per "
        "question and its total, straight from Forms.")

spacer(d, 8)
h2(d, "A student sees no marks at all")
para(d, "Run auditForm(1, 'CML3111'), replacing the week and cohort with the one you "
        "are testing. It reads the live form back and prints everything that could "
        "stop a total appearing, then names the cause. There are only three, and the "
        "first two are repairable in place.")

table(d, ["What the audit says", "What to do"],
      [["Questions carry ZERO points",
        "Run applyPoints. It sets one point on every question across all 36 "
        "forms and turns quiz mode on. No rebuild, no new links, no new QR "
        "codes."],
       ["This form is not in quiz mode",
        "Also applyPoints: it turns quiz mode on as part of the same pass."],
       ["The marking side of this form is correct",
        "Then the cause is the one setting no API can read. Open the form, "
        "Settings, then Quizzes, then Release grade. It must say "
        "'Immediately after each submission'. If it says 'Later, after "
        "manual review', the template in section 1.0 was not in place when "
        "these forms were built."],
       ["Questions do not have exactly one correct option",
        "That one does need rebuildAllForms, because an answer key lives "
        "with the choices and cannot be rewritten in place."]],
      [34, 66], font=8.4)

spacer(d, 6)
para(d, "Worth knowing the difference between the two things a student sees. The "
        "per-question feedback appears because feedback is attached to the question. "
        "The total out of five appears only if the questions carry points AND grades "
        "are released immediately. Seeing feedback without a total therefore tells "
        "you the release setting is probably fine and the points are probably not.")

spacer(d, 8)
h2(d, "The honest limitations")
para(d, "Three things this design does not do, stated plainly so they are not "
        "discovered at an inconvenient moment.")
para(d, "Google Forms cannot enforce a timer. The automatic close is a scheduled "
        "trigger, and Apps Script schedules it within about a minute rather than to "
        "the second. Six minutes is set deliberately so the margin falls on the "
        "students' side.")
para(d, "It cannot stop a student answering from outside the room. The signed-in "
        "account is what joins a response to a person. Three parallel option orders "
        "and a "
        "five-minute window make coordination hard, and the mark is one per cent, so "
        "the incentive is small. Unaided capability is certified in the two offline "
        "tests, which is where thirty-five per cent of the mark sits.")
para(d, "One response per student is enforced by Google sign-in, which is the only "
        "identity Forms has. The cost is that a student who is not signed in, or has "
        "no Google account, cannot submit at all. Most will already be signed in on "
        "an Android phone. If that trade looks wrong for your cohort, set "
        "LIMIT_ONE_RESPONSE to false at the top of the script, run "
        "applyResponseLimits, and rely on findDuplicates instead: it lists any "
        "account appearing twice, and the convention is that the first "
        "submission counts.")
para(d, "Ask in Week 1 whether anybody cannot sign in to a Google account, and do it "
        "then rather than in week four. A student who has no account misses all "
        "twelve quizzes, which is ten per cent of the grade, and the two dropped "
        "scores do not cover that. One question to the room settles it, and if "
        "anybody says yes the switch above is the answer.")
para(d, "The form stays open for forty-eight hours after you open it, then closes "
        "itself. The five minutes on the projected clock is when the quiz is meant to "
        "be taken; the window exists so that a failed network in Room 106, or one "
        "broken phone, does not cost a student a mark they had earned. One response "
        "per Google account is enforced, so a longer window cannot be used twice.")
para(d, "What the window costs is information: you can no longer assume a submission "
        "happened in the room. showScores records when each quiz was opened and marks "
        "every response either in session or late, with how many hours late, so you "
        "can see at a glance whether the window was used as intended or as a way of "
        "putting the quiz off.")
para(d, "Say it to the room in Week 1, once: answer it now, in the five minutes. "
        "The window exists for a dead network or a phone that will not scan, and "
        "the feedback is worth far less two days after the session it belongs to.")
para(d, "All twelve banks are now written, which is sixty questions across the three "
        "cohorts. What that does not mean is that they have been taught. A question "
        "reads differently in a room than it does on a page, and the first sitting of "
        "each quiz is the real test of it. Keep the two dropped scores in mind as the "
        "margin that absorbs a question which turns out to be ambiguous, and edit the "
        "bank rather than defending a weak question.")
para(d, "One structural note on the banks. Weeks 1 and 2 carry a different question "
        "mix from the rest: three interpretation questions and no silently-wrong-answer "
        "question, because in Week 1 nobody has written code and in Week 2 they have "
        "just opened their first notebook. The standing mix of two diagnosis, one "
        "traceback, one interpretation and one judgement applies from Week 3 onwards, "
        "and verify_quiz_arithmetic.py enforces it.")

spacer(d, 12)
para(d, "Weekly quiz operations guide · regenerate from build_quizops_docx.py "
        "after any change to the quiz design.",
     size=8.5, italic=True, colour=GREY, align=AL.CENTER)

d.save(OUT)
print("saved", OUT)
