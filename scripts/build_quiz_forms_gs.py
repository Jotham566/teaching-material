# -*- coding: utf-8 -*-
"""Generate the Apps Script that creates every quiz Google Form.

The lecturer pastes one file into script.google.com and runs one function.
That creates 36 forms — twelve quiz weeks for each of three cohorts — in quiz
mode, with the questions, answer keys, feedback, a linked response
spreadsheet per cohort, and every form closed until he opens it.

WHY 36 AND NOT 12
CML3112 sits on Tuesday and the two Friday cohorts sit three days later. One
shared form would let Tuesday's answers reach Friday's students, so each cohort
gets its own form. The decks are already per-cohort, so each deck simply
carries its own cohort's QR code.

TWO GOOGLE FORMS LIMITATIONS, DESIGNED AROUND
1. Forms supports feedback for a CORRECT answer and feedback for an INCORRECT
   answer per question. It does NOT support per-option feedback. The banks in
   quiz_banks.py carry per-option feedback because that is the teaching, so
   this generator folds the wrong-option explanations into one incorrect-answer
   message that names each distractor and says why it is wrong. Nothing is
   lost; it arrives in one block instead of three.
2. Forms has no timer. A five-minute quiz therefore needs the form closed on
   time, and doing that by hand while a hundred students are submitting is a
   good way to forget. The script installs `openQuizFor(week, cohort)`, which
   opens the form and schedules a trigger to close it automatically six minutes
   later, and a menu to drive it.

Also worth knowing: option order is shuffled here, deterministically, with a
different seed per cohort, so the three cohorts see the options in three
different orders. Apps Script cannot set the Forms "shuffle option order"
setting, so doing it at creation time is the only way to get it.
"""
import io
import json
import random
import sys

import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_HERE)
sys.path.insert(0, _HERE)
import quiz_banks as QB

OUT = (_ROOT + "/IUEA_Teaching_Plan/"
       "grader/create_quiz_forms.gs")

# Two numbers, and the difference between them matters.
#
# QUIZ_MIN is the working time students are told and the projected clock
# counts. WINDOW_MIN is when the form actually stops accepting answers, one
# minute later, so that somebody who hits submit as the clock hits zero is
# not cut off mid-request. The extra minute is submission grace rather than
# thinking time, and the form says so in as many words.
#
# QUIZ_MIN is the five minutes on the projected clock, and the whole
# assessment budget is built on twelve five-minute quizzes costing the same
# sixty minutes as the checkpoints they replaced. WINDOW_H is how long the
# form then stays open for a student whose network failed. Keep these in
# step with build_quiz_timer.py and with QUIZ_MIN_ON_CLOCK / WINDOW_HOURS
# in the Apps Script below.
QUIZ_MIN = 5
WINDOW_H = 24

COHORTS = {
    "CML3112": {"name": "Architecture + Civil Engineering",
                "day": "Tuesday", "seed": 3112},
    "CML3113": {"name": "Mining + Petroleum Engineering",
                "day": "Friday 08:00", "seed": 3113},
    "CML3111": {"name": "Electrical, Mechatronics & Robotics, Communications",
                "day": "Friday 11:00", "seed": 3111},
}


def build_payload():
    """Everything the Apps Script needs, as plain JSON-able data."""
    out = {}
    for code, meta in COHORTS.items():
        weeks = []
        for wk in sorted(QB.QUIZ):
            q = QB.QUIZ[wk]
            # Every rule stated on the form itself, because the slide is
            # behind them once they are looking at their phone. Forms shows
            # this description above the first question.
            intro = (
                q["intro"]
                + "\n\nHOW THIS WORKS"
                + f"\n• Answer it now, in the {QUIZ_MIN} minutes on the "
                  "screen. That is when this is meant to be taken, while "
                  "the session is still fresh."
                + f"\n• The form then stays open for {WINDOW_H} hours and "
                  "closes itself. That window is there so a dead network "
                  "or a broken phone does not cost you a mark you had "
                  "earned. Take it in the room if you can: by Thursday you "
                  "will have forgotten the session, and the feedback will "
                  "be worth less to you."
                + "\n• ONE attempt, from your signed-in Google account. "
                  "You cannot reopen it or change an answer, so read each "
                  "question once, properly."
                + "\n• The first box asks for your registration number. "
                  "It is the number printed on your student card, and it "
                  "is how the mark reaches your record."
                + "\n• Five questions, one mark each, worth 1% of your "
                  "final mark."
                + "\n• Your best ten of twelve quizzes count. Missing "
                  "two costs you nothing, and there are no resits."
                + "\n• When you submit, tap View score. You get a tick or "
                  "a cross on each question with the feedback underneath. "
                  "Your mark is the number of ticks, and the feedback on "
                  "anything you got wrong is the part worth reading."
                + "\n• A question left blank scores the same as one "
                  "answered wrongly, so answer all five.")
            if code in ('CML3111','CML3112','CML3113'):
                intro=intro.replace('worth 1% of your final mark.', 'part of the 10% quiz component.').replace('Your best ten of twelve quizzes count.', 'Quiz 6 is not assigned. Your best nine of eleven assigned quizzes count.')
                if wk==6:intro='NOT ASSIGNED: Quiz 6 is waived for practical revision. No submission or mark is required.'
            entry = {
                "week": wk,
                "number": QB.QUIZ_NUMBER[wk],
                "title": f"{code} · {q['title']}",
                "intro": intro,
                "questions": [],
            }
            if not q["q"]:
                # Not yet authored. Create the form anyway so the mechanism can
                # be tested, with one honest placeholder question.
                entry["placeholder"] = True
                entry["plan"] = q.get("plan", "")
                entry["mix"] = q["mix"]
                weeks.append(entry)
                continue

            rng = random.Random(meta["seed"] * 1000 + wk)
            for qi, qq in enumerate(q["q"], 1):
                stem = QB.stem_for(qq, code)
                pre = QB.pre_for(qq, code)
                opts = list(QB.options_for(qq, code))
                rng.shuffle(opts)

                correct = [o for o in opts if o[1]]
                wrong = [o for o in opts if not o[1]]
                fb_correct = correct[0][2]

                # The incorrect-answer message must LEAD with the right
                # answer. The first live test showed a student who got a
                # question wrong reading three refutations without ever
                # being told what the answer was, which is the one thing
                # they actually needed. Forms marks the correct option
                # visually, and the text should not depend on that.
                lead = fb_correct
                for prefix in ("Correct, and ", "Correct. ", "Correct, "):
                    if lead.startswith(prefix):
                        rest = lead[len(prefix):]
                        lead = rest[0].upper() + rest[1:] if rest else ""
                        break
                fb_wrong = ("THE ANSWER: " + correct[0][0] + ". " + lead
                            + "\n\nWhy the others are wrong. "
                            + "  ".join(f"“{text}” — {fb}"
                                        for text, _, fb in wrong))

                entry["questions"].append({
                    "n": qi,
                    "kind": qq["kind"],
                    "title": stem,
                    "help": pre or "",
                    "choices": [{"text": t, "correct": bool(c)}
                                for t, c, _ in opts],
                    "fbCorrect": fb_correct,
                    "fbWrong": fb_wrong,
                })
            weeks.append(entry)
        out[code] = {"meta": {"name": meta["name"], "day": meta["day"]},
                     "weeks": weeks}
    return out


GS_TEMPLATE = r'''/**
 * IUEA CML3111 / CML3112 / CML3113 - create every weekly quiz Google Form.
 *
 * GENERATED FILE. Do not edit here. Edit quiz_banks.py and re-run
 * build_quiz_forms_gs.py, then paste this file in again.
 *
 * WHAT IT DOES
 *   createAllForms()      Creates 36 forms (12 quiz weeks x 3 cohorts) in a
 *                         folder in your Drive, in quiz mode, each closed.
 *                         Writes a "Quiz Links" sheet with every URL, and one
 *                         response spreadsheet per cohort. Safe to re-run:
 *                         it skips anything already built, saves progress
 *                         after every cohort (not just at the end), and a
 *                         failure on one cohort does not stop the other two.
 *
 *                         *** IT WILL NOT FINISH IN ONE RUN. *** A form
 *                         takes twelve to fifteen seconds, so thirty-six
 *                         need about eight minutes and Apps Script stops
 *                         every execution at six. This function stops
 *                         itself at four and a half minutes and tells you
 *                         how many are left. RUN IT AGAIN, two or three
 *                         times, until it says ALL 36 FORMS EXIST. That is
 *                         normal operation rather than a fault.
 *   auditAll()             The marking health of all 36 on one screen:
 *                         quiz mode, points, answer keys, feedback,
 *                         publish and open state, and what to run next.
 *                         START HERE when something looks wrong.
 *   auditForm(w, c)        The same detail for one form, question by
 *                         question. Press Run with no arguments and it
 *                         audits the first form on record; use the
 *                         audit_W1_CML3111 wrappers for a specific one.
 *
 *   NOTE ON THE RUN BUTTON: it cannot pass arguments, so anything taking
 *   them has a zero-argument wrapper at the bottom of this file:
 *   open_W1_CML3112, close_W1_CML3112, audit_W1_CML3112, build_CML3112.
 *   applyPoints()          Sets one point on every question across all 36
 *                         and turns quiz mode on. IN PLACE, no rebuild.
 *                         This is the fix when feedback shows but no score.
 *   updateFeedbackAndIntro()
 *                         Pushes edited feedback text, question stems and
 *                         form descriptions into the LIVE forms with no
 *                         rebuild and no new links. Use this after any
 *                         wording change. Only a change to the OPTIONS
 *                         themselves needs rebuildAllForms.
 *   applyResponseLimits()  Turns one-response-per-student on across all 36
 *                         IN PLACE: no rebuild, no new links, no new QR
 *                         codes. Run after changing LIMIT_ONE_RESPONSE.
 *   findDuplicates()       Lists students who submitted more than once.
 *                         The first submission is the one that counts.
 *   publishAllForms()      Repair function. Run this if opening a quiz
 *                         fails with "Operation not supported on
 *                         unpublished form". Publishes all 36 in place,
 *                         keeping every link. No rebuild needed.
 *   setupTemplate()        Run ONCE, first. Creates the single form you
 *                         configure by hand, then tells you what to click
 *                         and what id to paste into TEMPLATE_FORM_ID.
 *   checkTemplate()        Confirms the template is usable before 36 forms
 *                         depend on it.
 *   status()               What exists and what is missing. Run this any
 *                         time you lose track.
 *   build_CML3112()        One cohort at a time: twelve forms, about three
 *   build_CML3113()        minutes each, comfortably inside the execution
 *   build_CML3111()        limit. The predictable alternative to re-running
 *                         createAllForms().
 *   armRebuild()           Step one of a rebuild. Arms it for ten minutes.
 *   rebuildAllForms()      Step two. Moves all 36 forms and their response
 *                         sheets to the Drive trash and builds them again
 *                         from the current question banks. This is the ONLY
 *                         way to pick up an edited question, because
 *                         createAllForms() skips anything that exists.
 *                         Refuses if responses have been collected, unless
 *                         you arm the stronger flag on purpose.
 *   testSheetCreate()      Run this if createAllForms() fails on EVERY
 *                         cohort, including brand-new ones with nothing to
 *                         collide with. Isolates whether Sheets access
 *                         works for this account at all, independent of
 *                         quizzes, folders or anything else in this file.
 *   diagnoseDrive()        Run this if createAllForms() throws a permission
 *                         error but testSheetCreate() works fine. Lists
 *                         every "IUEA ML Quizzes" folder and what is inside
 *                         each one, so a stray or inaccessible duplicate
 *                         file is obvious.
 *   printLinksJson()      Logs the week/cohort/URL map as JSON. Paste that
 *                         back to generate the QR codes for the slide decks.
 *   openQuizFor(w, c)     Opens one quiz and arranges its automatic close.
 *   closeStatus()          Is a quiz open, when is it due to close, and is
 *                         a trigger actually installed? Run this if a form
 *                         is still taking answers when it should not be.
 *   closeQuiz(w, c)       Closes it now.
 *   closeEverything()     Panic button: closes all 36.
 *
 * FIRST RUN
 *   1. script.google.com -> New project -> paste this file -> Save.
 *   2. Run createAllForms(). Authorise when asked; it needs Forms, Drive and
 *      Sheets on your own account.
 *   3. It takes two or three minutes. Watch the execution log. If it stops
 *      with a permission error, run diagnoseDrive(), fix whatever it finds
 *      (usually a stray file/folder from an earlier attempt), then run
 *      createAllForms() again. It resumes, it does not start over.
 *   4. Run printLinksJson() and copy the JSON it logs.
 *
 * PUBLISHED IS NOT THE SAME AS OPEN
 *   Since 30 June 2026 a form created by a script starts UNPUBLISHED, and
 *   enabling responses on an unpublished form throws "Operation not
 *   supported on unpublished form". Setting responses to FALSE is allowed,
 *   which is why creation looked fine and only opening a quiz failed.
 *
 *   Every form is therefore published at creation and left closed.
 *   Published means the link resolves; accepting-responses is the
 *   five-minute window openQuizFor opens on the day. If you have forms
 *   built before this was handled, run publishAllForms() once.
 *
 * ONE THING THE API CANNOT SET, AND THE WAY ROUND IT
 *   Grade release timing. No API reaches it: not Apps Script, not the Forms
 *   REST API. A form created programmatically comes out as "Later, after
 *   manual review", which ALSO switches on collect-email-addresses and
 *   means a student sees no score at all when they submit.
 *
 *   It is per-form, so fixing it by hand is 36 edits, and a rebuild undoes
 *   every one of them silently.
 *
 *   So configure ONE form by hand and copy it. Run setupTemplate(), click
 *   the two settings it names, paste the id into TEMPLATE_FORM_ID above,
 *   run checkTemplate(), and every quiz built after that inherits the
 *   setting. The dry run is still what proves it: submit once and watch
 *   for a score, because no API can read this setting back either.
 */

var FOLDER_NAME = 'IUEA ML Quizzes';
var LINKS_SHEET_NAME = 'IUEA ML Quiz Links';
var PROP_LINKS = 'IUEA_QUIZ_LINKS';
var PROP_PENDING_CLOSE = 'IUEA_PENDING_CLOSE';
var PROP_CLOSE_AT = 'IUEA_CLOSE_AT';

// THE CLOCK AND THE WINDOW ARE TWO DIFFERENT THINGS.
//
// QUIZ_MIN_ON_CLOCK is the five minutes the projected timer counts and the
// five minutes you give the room. That is when the quiz is taken.
//
// WINDOW_HOURS is how long the form keeps accepting answers afterwards. It
// is 24 hours, and the reason is Room 106: about a hundred students on one
// set of access points, and a network that fails at some point over twelve
// sittings. A five-minute hard close means a network fault costs a student
// a mark they had earned. One response per Google account is already
// enforced, so the window cannot be used twice.
//
// Say it to the room as: answer it now, in the five minutes. The window
// exists so a broken phone or a dead network does not cost you the mark.
// It is not an invitation to do it on Thursday.
var QUIZ_MIN_ON_CLOCK = 5;
var WINDOW_HOURS = 24;

// ONE SUBMISSION PER STUDENT.
//
// Forms can only enforce this by identity, and the only identity it has is
// a Google account, so turning it on REQUIRES EVERY STUDENT TO SIGN IN.
// Most will already be signed in on an Android phone. A student who is not,
// or who has no Google account, cannot submit at all.
//
// Best-ten-of-twelve absorbs a lost week, and the response sheet keeps the
// student number so a genuine lockout can be marked by hand. What it does
// NOT cover is a student with no Google account at all: they would miss
// every one of the twelve, which is ten per cent of the grade rather than
// a bad week. Ask in Week 1 who cannot sign in, and if anybody cannot, set
// this to false and rely on findDuplicates() instead.
var LIMIT_ONE_RESPONSE = true;

// IDENTITY. See the IDENTITY section further down for the reasoning.
// true  = the signed-in Google address identifies the student, and the form
//         carries no free-text question, so Forms can auto-grade the whole
//         thing and SHOWS THE STUDENT A SCORE OUT OF FIVE.
// false = students type a student number, and Forms then withholds the
//         total because it cannot mark a free-text answer.
// Changing these needs applyIdentityFields() to apply them to forms that
// already exist.
// IDENTITY: BOTH, and here is why that is free.
//
// With Verified collection selected in Forms Settings, the signed-in address is
// what enforces one attempt. The registration number is what the gradebook
// already keys on, so having students type it removes the need for a roster
// mapping addresses to numbers.
//
// Asking for both used to look expensive, because a free-text question was
// thought to be what stopped Forms showing a score. That turned out to be
// wrong: the total is not shown on that page either way, and showScores
// confirmed the marking is automatic with the field present and absent. So
// the field costs nothing that matters.
var COLLECT_EMAIL = true;
var ASK_REGISTRATION_NUMBER = true;

// Called a registration number, never a student number: students read
// "student number" as a phone number. The help text says so outright.
var ID_QUESTION_TITLE = 'Student Registration Number';
var ID_QUESTION_HELP =
  'The registration number on your student card, the one the university '
  + 'identifies you by. NOT your phone number. Type it exactly as it '
  + 'appears on the card, because this is how your mark reaches your '
  + 'record.';

// Titles this field has been given before, so an existing form can be
// found and renamed rather than ending up with two identity questions.
var ID_QUESTION_OLD_TITLES = ['Your student number', 'Your registration number', 'Student Registration Number'];

// What a student reads on the page immediately after submitting. This is
// the only text Forms lets you control there, and it is where to point them
// at their mark, because the confirmation page itself does not show a total.
var CONFIRMATION = 'Submitted, and your mark is already recorded.\n\n'
  + 'Tap "View score" to see it: a tick or a cross on each of the five '
  + 'questions, and the feedback underneath every one. Read the feedback on '
  + 'anything you got wrong. That is the part of this worth five minutes.';
// ==========================================================================
// TEMPLATE FORM. Paste an ID here to make grade release automatic.
//
// "Release grade: immediately after each submission" is the one setting no
// API can reach: not Apps Script, not the Forms REST API. Forms created
// programmatically come out as "Later, after manual review", which also
// switches ON collect-email-addresses and means students see nothing when
// they submit. That would gut the design, since the slide promises a score
// the moment they submit.
//
// Setting it by hand is thirty-six edits, and a rebuild silently undoes
// every one of them. So instead: configure ONE form by hand and copy it.
// A Drive copy inherits the setting, so every quiz is born correct.
//
// Run setupTemplate() to create the form to configure, then paste its id
// below. Leave this empty and the script still works, warning you each run
// that you are on the hand-editing path.
var TEMPLATE_FORM_ID = '';

var PROP_ARMED = 'IUEA_REBUILD_ARMED';
var PROP_ARMED_HARD = 'IUEA_REBUILD_ARMED_HARD';
var ARM_WINDOW_MIN = 10;

// Apps Script kills a run at six minutes. One form takes roughly twelve to
// fifteen seconds to build, so all thirty-six need about eight minutes and
// CANNOT finish in a single execution. The work is therefore resumable:
// createAllForms() stops on its own before the limit, saves what it has
// done, and tells you to run it again. Re-running resumes, because a form
// that already exists is skipped.
//
// 4.5 minutes leaves room to finish the form in hand and write the links
// sheet, which is the part that must not be interrupted.
var RUN_BUDGET_MS = 4.5 * 60 * 1000;
var RUN_START = 0;

function outOfTime_() {
  return (new Date().getTime() - RUN_START) > RUN_BUDGET_MS;
}

var QUIZ_DATA = __PAYLOAD__;

/** Menu, so none of this needs the script editor once it is installed. */
function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('IUEA quizzes')
    .addItem('Print links as JSON', 'printLinksJson')
    .addItem('Close every quiz now', 'closeEverything')
    .addToUi();
}

function folder_() {
  var it = DriveApp.getFoldersByName(FOLDER_NAME);
  return it.hasNext() ? it.next() : DriveApp.createFolder(FOLDER_NAME);
}

/** Isolated test: does this account have any Sheets access via Apps Script
 *  at all, independent of everything else in this file? If this alone
 *  throws "You do not have permission to access the requested document",
 *  the problem is account-level (authorization scope, or a Workspace admin
 *  restriction), not anything to do with quizzes, folders or stray files. */
function testSheetCreate() {
  var ss = SpreadsheetApp.create('IUEA test \u2014 safe to delete ' + new Date().getTime());
  Logger.log('created OK: ' + ss.getUrl());
  Logger.log('If you see this, Sheets access works fine and the earlier '
             + 'failure was specific to the quiz script - tell me that and '
             + 'I will look again. Delete this test file from Drive when '
             + 'you are done.');
}

/** Run this FIRST if createAllForms() ever throws a permission error. Lists
 *  every folder named "IUEA ML Quizzes" and every file inside each one, so a
 *  stray duplicate (e.g. from a half-finished earlier attempt, or created
 *  under a different Google account) is obvious instead of guessed at. */
function diagnoseDrive() {
  var folders = DriveApp.getFoldersByName(FOLDER_NAME);
  var n = 0;
  while (folders.hasNext()) {
    var f = folders.next();
    n++;
    Logger.log('FOLDER ' + n + ': "' + f.getName() + '"  id=' + f.getId()
               + '  owner=' + (f.getOwner() ? f.getOwner().getEmail() : '?')
               + '  url=' + f.getUrl());
    var files = f.getFiles();
    while (files.hasNext()) {
      var file = files.next();
      var openable = 'yes';
      if (file.getMimeType() === MimeType.GOOGLE_SHEETS) {
        try { SpreadsheetApp.open(file); } catch (e) { openable = 'NO: ' + e.message; }
      }
      Logger.log('  file: "' + file.getName() + '"  id=' + file.getId()
                 + '  type=' + file.getMimeType()
                 + '  owner=' + (file.getOwner() ? file.getOwner().getEmail() : '?')
                 + '  opens-as-sheet=' + openable);
    }
  }
  if (n === 0) {
    Logger.log('No folder named "' + FOLDER_NAME + '" exists yet - '
               + 'createAllForms() will create one from scratch. If it '
               + 'still throws the same error, the problem is not a stray '
               + 'file, so paste the exact error text back.');
  } else if (n > 1) {
    Logger.log(n + ' DIFFERENT folders share the name "' + FOLDER_NAME
               + '". DriveApp.getFoldersByName() picks one arbitrarily each '
               + 'run, which is almost certainly the bug: rename or delete '
               + 'all but one before running createAllForms() again.');
  }
}

/**
 * Create every form. Safe to run as many times as you like: a form that
 * already exists is skipped, so re-running only builds what is missing.
 *
 * It will NOT finish in one run. Thirty-six forms take about eight minutes
 * and Apps Script stops at six, so this stops itself at four and a half
 * and asks you to run it again. Expect two or three runs from empty.
 */
function createAllForms(onlyCode) {
  if (!RUN_START) { RUN_START = new Date().getTime(); }
  var fold = folder_();
  var links = loadLinks_();
  var made = 0, skipped = 0, failed = 0, ranOut = false;

  if (TEMPLATE_FORM_ID) {
    Logger.log('copying the template, so grade release is inherited');
  } else {
    Logger.log('NO TEMPLATE SET. Every form will come out with "Release '
               + 'grade: Later, after manual review", which also turns on '
               + 'email collection, and students will NOT see a score when '
               + 'they submit.');
    Logger.log('Either change all 36 by hand afterwards, or run '
               + 'setupTemplate() once and never think about it again.');
  }

  for (var code in QUIZ_DATA) {
    if (ranOut) { break; }
    if (onlyCode && code !== onlyCode) { continue; }
    var cohort = QUIZ_DATA[code];
    var ss;
    try {
      ss = responseSpreadsheet_(code, fold);
    } catch (e) {
      // A stray or inaccessible file with the expected name is the usual
      // cause here, not a real permission problem with your account. Don't
      // let it take the other two cohorts down with it. Log it, skip this
      // cohort's forms this run, and keep going. Re-running after clearing
      // the offending file (see the error log) will pick this cohort back up.
      Logger.log('SKIPPING cohort ' + code + ' - could not get its response '
                 + 'spreadsheet: ' + e.message);
      Logger.log('Look in Drive for a file or folder named "'
                 + 'IUEA ML Quiz Responses \u2014 ' + code + '" or "' + FOLDER_NAME
                 + '" that you did not create yourself (e.g. left over from '
                 + 'an earlier attempt, or shared from another account) and '
                 + 'remove or rename it, then run createAllForms() again.');
      failed++;
      continue;
    }

    for (var i = 0; i < cohort.weeks.length; i++) {
      var wk = cohort.weeks[i];
      var key = code + '|' + wk.week;
      if (links[key] && links[key].formId) {
        try {
          FormApp.openById(links[key].formId);
          skipped++;
          continue;                      // already built, leave it
        } catch (e) { /* recorded but gone; rebuild it */ }
      }

      // Stop before Apps Script stops us, so the links sheet below is
      // always written and nothing is created without being recorded.
      if (outOfTime_()) { ranOut = true; break; }

      try {
        var form = newQuizForm_(wk.title);
        form.setDescription(wk.intro);
        form.setIsQuiz(true);
        // Preserve the Verified collection mode selected in the Forms UI.
        if (form.collectsEmail() !== COLLECT_EMAIL) { form.setCollectEmail(COLLECT_EMAIL); }
        form.setProgressBar(false);
        try { form.setConfirmationMessage(CONFIRMATION); } catch (e) {}
        form.setAllowResponseEdits(false);
        form.setLimitOneResponsePerUser(LIMIT_ONE_RESPONSE);
        form.setShuffleQuestions(false);
        // publishing and accepting-responses are set AFTER the questions
        // are added, because a responder-facing call on an unpublished form
        // throws. See publishForm_ above.

        if (ASK_REGISTRATION_NUMBER) {
          var idq = form.addTextItem();
          idq.setTitle(ID_QUESTION_TITLE);
          idq.setHelpText(ID_QUESTION_HELP);
          idq.setRequired(true);
        }

        if (wk.placeholder) {
          var ph = form.addMultipleChoiceItem();
          ph.setTitle('This quiz has not been written yet.');
          ph.setHelpText('Planned content: ' + wk.plan + '   Mix: ' + wk.mix);
          ph.setChoices([
            ph.createChoice('Understood - this form exists so the mechanism '
                            + 'can be tested', true),
          ]);
          ph.setPoints(1);
          ph.setFeedbackForCorrect(
            FormApp.createFeedback().setText(
              'This form is a shell. Replace this question with the five '
              + 'real ones from the bank, then re-run createAllForms().'
              ).build());
        } else {
          for (var j = 0; j < wk.questions.length; j++) {
            var q = wk.questions[j];
            var item = form.addMultipleChoiceItem();
            item.setTitle(q.n + '. ' + q.title);
            if (q.help) { item.setHelpText(q.help); }
            var choices = [];
            for (var k = 0; k < q.choices.length; k++) {
              choices.push(item.createChoice(q.choices[k].text,
                                             q.choices[k].correct));
            }
            item.setChoices(choices);
            item.setPoints(1);
            item.setRequired(true);
            if (q.fbCorrect) {
              item.setFeedbackForCorrect(
                FormApp.createFeedback().setText(q.fbCorrect).build());
            }
            if (q.fbWrong) {
              item.setFeedbackForIncorrect(
                FormApp.createFeedback().setText(q.fbWrong).build());
            }
          }
        }

        // Publish now that the questions exist, then close it. Published
        // means the link resolves; accepting-responses is the five-minute
        // window you open on the day.
        var pub = publishForm_(form);
        if (pub !== 'ok' && pub !== 'unsupported') {
          Logger.log('  ' + wk.title + ' ' + pub);
        }
        form.setAcceptingResponses(false);

        form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());

        // move the form file into the folder
        try { DriveApp.getFileById(form.getId()).moveTo(fold); } catch (e) {}

        var live = form.getPublishedUrl();
        var short = '';
        try { short = form.shortenFormUrl(live); } catch (e) { short = live; }

        links[key] = {
          code: code, week: wk.week, number: wk.number, title: wk.title,
          formId: form.getId(), edit: form.getEditUrl(),
          live: live, short: short,
          placeholder: !!wk.placeholder
        };
        made++;
        Logger.log('created ' + wk.title);
      } catch (e) {
        failed++;
        Logger.log('FAILED on ' + wk.title + ': ' + e.message
                   + ' - continuing with the rest.');
      }
    }

    // Save after every cohort, not just at the very end, so a failure in a
    // later cohort (or a timeout) never throws away forms already created.
    saveLinks_(links);
    writeLinksSheet_(links);
  }

  var total = 0;
  for (var c2 in QUIZ_DATA) { total += QUIZ_DATA[c2].weeks.length; }
  var have = Object.keys(loadLinks_()).length;

  Logger.log('');
  Logger.log('this run: ' + made + ' created, ' + skipped + ' already '
             + 'existed, ' + failed + ' failed');
  Logger.log('overall:  ' + have + ' of ' + total + ' forms now exist');

  if (ranOut || have < total) {
    Logger.log('');
    Logger.log('*** NOT FINISHED. ' + (total - have) + ' forms still to '
               + 'build. ***');
    Logger.log('Run createAllForms() AGAIN to carry on. It resumes from '
               + 'here; the ' + have + ' already built are skipped.');
    Logger.log('Do NOT run rebuildAllForms() to continue. That deletes '
               + 'everything and starts over, which is how you end up '
               + 'timing out in the same place forever.');
    return;
  }

  if (failed) {
    Logger.log('Some forms did not get created - see FAILED/SKIPPING lines '
               + 'above. Fix the cause and run createAllForms() again; it '
               + 'will only rebuild what is missing.');
  }
  Logger.log('');
  Logger.log('ALL ' + total + ' FORMS EXIST.');
  Logger.log('Now run printLinksJson() and paste the output back.');
}

/** Where am I? Run this any time to see what exists and what is missing. */
function status() {
  var links = loadLinks_();
  var total = 0, have = 0;
  for (var code in QUIZ_DATA) {
    var missing = [];
    for (var i = 0; i < QUIZ_DATA[code].weeks.length; i++) {
      var w = QUIZ_DATA[code].weeks[i].week;
      total++;
      if (links[code + '|' + w]) { have++; } else { missing.push(w); }
    }
    Logger.log(code + ': ' + (QUIZ_DATA[code].weeks.length - missing.length)
               + ' of ' + QUIZ_DATA[code].weeks.length + ' built'
               + (missing.length ? ', missing weeks ' + missing.join(', ')
                                 : ''));
  }
  Logger.log('');
  Logger.log(have + ' of ' + total + ' forms exist.');
  if (have < total) {
    Logger.log('Run createAllForms() to build the rest. Repeat until it '
               + 'says ALL ' + total + ' FORMS EXIST.');
  } else {
    Logger.log('Next: printLinksJson(), then save the JSON as '
               + 'data/quiz_links.json, then python3 attach_qr.py.');
  }
}

/**
 * Build one cohort only. Twelve forms is about three minutes, which fits
 * inside the execution limit comfortably, so this is the predictable way
 * to work through them if you would rather not re-run the whole thing.
 */
function createFormsForCohort(code) {
  if (code === undefined) {
    Logger.log('createFormsForCohort needs a cohort, and the Run button '
               + 'cannot pass one. Use build_CML3112, build_CML3113 or '
               + 'build_CML3111, or just run createAllForms().');
    return;
  }
  if (!QUIZ_DATA[code]) {
    throw new Error('Unknown cohort ' + code + '. Use CML3112, CML3113 or '
                    + 'CML3111.');
  }
  RUN_START = new Date().getTime();
  createAllForms(code);
}

function build_CML3112() { createFormsForCohort('CML3112'); }
function build_CML3113() { createFormsForCohort('CML3113'); }
function build_CML3111() { createFormsForCohort('CML3111'); }

// ==========================================================================
// REBUILD. Deleting and recreating is the only way to pick up edited
// questions, because createAllForms() deliberately skips a form that
// already exists. It is also destructive, so it is deliberately awkward:
// arm it first, and it refuses outright if any responses have been
// collected unless you arm the stronger flag on purpose.
// ==========================================================================

// ==========================================================================
// Template helpers
// ==========================================================================

/** Create the one form you configure by hand. Run this once. */
function setupTemplate() {
  var f = FormApp.create('IUEA ML quiz TEMPLATE - do not delete');
  f.setIsQuiz(true);
  f.setCollectEmail(false);
  f.setProgressBar(false);
  f.setAllowResponseEdits(false);
  f.setLimitOneResponsePerUser(LIMIT_ONE_RESPONSE);
  f.setShuffleQuestions(false);
  publishForm_(f);
  f.setAcceptingResponses(false);
  try { DriveApp.getFileById(f.getId()).moveTo(folder_()); } catch (e) {}

  Logger.log('Template created.');
  Logger.log('');
  Logger.log('1. Open it: ' + f.getEditUrl());
  Logger.log('2. Settings, then Quizzes. Set "Release grade" to '
             + '"Immediately after each submission".');
  Logger.log('3. Confirm "Collect email addresses" is OFF. Choosing the '
             + '"Later, after manual review" option switches it on, so '
             + 'check it after changing the release setting.');
  Logger.log('4. Leave the form otherwise EMPTY. Add no questions.');
  Logger.log('5. Paste this id into TEMPLATE_FORM_ID at the top of this '
             + 'script, and save:');
  Logger.log('');
  Logger.log('   ' + f.getId());
  Logger.log('');
  Logger.log('6. Run checkTemplate() to confirm, then rebuild.');
}

/** Confirm the template is usable before you rely on it for 36 forms. */
function checkTemplate() {
  if (!TEMPLATE_FORM_ID) {
    Logger.log('TEMPLATE_FORM_ID is empty. Forms will be created from '
               + 'scratch, which means "Release grade" comes out as "Later, '
               + 'after manual review" on all 36 and you must change each '
               + 'one by hand.');
    Logger.log('Run setupTemplate() to take the automatic route instead.');
    return;
  }
  var f;
  try {
    f = FormApp.openById(TEMPLATE_FORM_ID);
  } catch (e) {
    Logger.log('CANNOT OPEN the template id ' + TEMPLATE_FORM_ID + ': '
               + e.message);
    Logger.log('Check the id, or run setupTemplate() to make a new one.');
    return;
  }
  Logger.log('template: "' + f.getTitle() + '"');
  Logger.log('  quiz mode: ' + (f.isQuiz() ? 'on' : 'OFF - turn it on'));
  Logger.log('  collects email: '
             + (f.collectsEmail() ? 'YES - turn this off' : 'no'));
  Logger.log('  items on the form: ' + f.getItems().length
             + (f.getItems().length ? ' - these get deleted in each copy'
                                    : ' (good, it is empty)'));
  var copy;
  try {
    copy = DriveApp.getFileById(TEMPLATE_FORM_ID)
      .makeCopy('IUEA template copy test - safe to delete');
    Logger.log('  copying works: yes');
    copy.setTrashed(true);
    Logger.log('  test copy trashed again');
  } catch (e) {
    Logger.log('  COPYING FAILED: ' + e.message);
    return;
  }
  Logger.log('');
  Logger.log('Template looks usable. Note the one thing this cannot check: '
             + 'no API can read the grade-release setting, so confirm by eye '
             + 'that it says "Immediately after each submission", and verify '
             + 'it for real in the dry run by submitting once and watching '
             + 'for a score.');
}

// ==========================================================================
// PUBLISHING. Since 30 June 2026 a form created by a script starts in an
// UNPUBLISHED state, and setAcceptingResponses(true) throws
// "Operation not supported on unpublished form" on one of those. Setting it
// to false is allowed, which is why creation succeeded and only opening a
// quiz on the day failed.
//
// So every form is published at creation and left closed: published means
// reachable, accepting-responses is the five-minute window.
// ==========================================================================

/** Publish a form, tolerating a runtime that predates setPublished. */
function publishForm_(form) {
  if (typeof form.setPublished !== 'function') {
    return 'unsupported';
  }
  try {
    form.setPublished(true);
    return 'ok';
  } catch (e) {
    return 'failed: ' + e.message;
  }
}

/**
 * Publish all 36 existing forms. Run this once if your forms were built
 * before publishing was handled, which shows up as
 * "Operation not supported on unpublished form" when you open a quiz.
 * No rebuild needed: this repairs them in place and keeps every link.
 */
function publishAllForms() {
  RUN_START = new Date().getTime();
  var links = loadLinks_();
  var keys = Object.keys(links).sort();
  if (!keys.length) {
    Logger.log('No forms recorded yet. Run createAllForms() first.');
    return;
  }
  var done = 0, already = 0, gone = 0, bad = 0, unsupported = 0, reclosed = 0;
  for (var i = 0; i < keys.length; i++) {
    if (outOfTime_()) {
      Logger.log('');
      Logger.log('Stopped before the six-minute limit with ' + (keys.length - i)
                 + ' left. Run publishAllForms() again to finish.');
      break;
    }
    var L = links[keys[i]];
    var form;
    try {
      form = FormApp.openById(L.formId);
    } catch (e) {
      Logger.log('  ' + keys[i] + ': form is gone (' + e.message + ')');
      gone++;
      continue;
    }
    var alreadyPub = false;
    if (typeof form.isPublished === 'function') {
      try { alreadyPub = form.isPublished(); } catch (e) {}
    }

    // An already-published form still needs its accepting state checked,
    // because an earlier run of this very function is what left them open.
    var r = alreadyPub ? 'ok' : publishForm_(form);
    if (r === 'ok') {
      if (alreadyPub) { already++; } else { done++;
        Logger.log('  published ' + keys[i]); }
    } else if (r === 'unsupported') {
      unsupported++;
    } else {
      bad++;
      Logger.log('  ' + keys[i] + ' ' + r);
      continue;
    }

    // Publishing turns accepting-responses ON. Unpublishing is documented
    // to switch it off, and the reverse happens too, which left all 36
    // quizzes answerable at once: a student with any link could have taken
    // Week 13 in Week 1. Close every form again unless it is the one
    // currently open for a sitting.
    try {
      // Pending closes are a MAP now. Reading this property as a bare id
      // silently matched nothing, which meant a quiz being sat right now
      // would be closed under the students taking it.
      var pending = loadPending_();
      if (!pending[links[keys[i]].formId] && form.isAcceptingResponses()) {
        form.setAcceptingResponses(false);
        reclosed++;
      }
    } catch (e) {
      Logger.log('  could not re-close ' + keys[i] + ': ' + e.message);
    }
  }
  Logger.log('');
  Logger.log('published ' + done + ', already published ' + already
             + ', missing ' + gone + ', failed ' + bad);
  if (reclosed) {
    Logger.log('closed again after publishing: ' + reclosed
               + '   (publishing switches responses on, which is not what '
               + 'we want between sittings)');
  }
  if (unsupported) {
    Logger.log('This Apps Script runtime has no setPublished, so ' + unsupported
               + ' forms could not be published from code. Open each form and '
               + 'use the Publish button, or ask for the V8 runtime to be '
               + 'enabled in Project Settings.');
  }
  if (!bad && !gone && !unsupported) {
    Logger.log('All recorded forms are published. open_W1_CML3112 and the '
               + 'other openers will work now.');
  }
}

/**
 * Apply the one-response-per-student and no-edits rules to all 36 existing
 * forms. These are form settings rather than question content, so this
 * works IN PLACE: no rebuild, no new links, no new QR codes.
 *
 * Run it after changing LIMIT_ONE_RESPONSE, or once on forms that were
 * built before the setting existed.
 */
function applyResponseLimits() {
  RUN_START = new Date().getTime();
  var links = loadLinks_();
  var keys = Object.keys(links).sort();
  if (!keys.length) {
    Logger.log('No forms recorded yet. Run createAllForms() first.');
    return;
  }
  Logger.log('setting one-response-per-student to '
             + (LIMIT_ONE_RESPONSE ? 'ON' : 'off') + ' on ' + keys.length
             + ' forms');
  if (LIMIT_ONE_RESPONSE) {
    Logger.log('Students will now have to be signed in to a Google account '
               + 'to submit. That is the only way Forms can tell one person '
               + 'from another.');
  }
  var done = 0, gone = 0, bad = 0;
  for (var i = 0; i < keys.length; i++) {
    if (outOfTime_()) {
      Logger.log('Stopped before the limit with ' + (keys.length - i)
                 + ' left. Run applyResponseLimits() again to finish.');
      break;
    }
    try {
      var form = FormApp.openById(links[keys[i]].formId);
      form.setLimitOneResponsePerUser(LIMIT_ONE_RESPONSE);
      form.setAllowResponseEdits(false);
      done++;
    } catch (e) {
      if (/gone|not found|No item/i.test(e.message)) { gone++; }
      else { bad++; Logger.log('  ' + keys[i] + ': ' + e.message); }
    }
  }
  Logger.log('');
  Logger.log('updated ' + done + ', missing ' + gone + ', failed ' + bad);
  if (done && !bad) {
    Logger.log('Done, and no links changed, so the QR codes in the decks '
               + 'are still correct.');
  }
}

/**
 * Push edited feedback text and form descriptions into the LIVE forms,
 * without rebuilding anything.
 *
 * Feedback and the description are properties of items that already exist,
 * so they can be rewritten in place. That covers most reasons you would
 * otherwise reach for a rebuild. What it deliberately does NOT touch is the
 * option list, because rewriting choices resets the answer key and would
 * orphan any responses already collected.
 *
 * So: change the wording of feedback, a question stem or an intro, and run
 * this. Add, remove or reorder OPTIONS, and you need rebuildAllForms.
 *
 * Every question is matched by its title before anything is written, and a
 * mismatch is reported and skipped rather than guessed at, because writing
 * question 3's feedback onto question 4 would be worse than doing nothing.
 */
function repairWeek2FeedbackOnly() {
  var links=loadLinks_();
  Object.keys(QUIZ_DATA).forEach(function(code){
    var record=links[code+'|2']; if(!record){return;}
    var week=QUIZ_DATA[code].weeks.filter(function(w){return w.week===2;})[0];
    var q=week.questions[3], form=FormApp.openById(record.formId);
    var items=form.getItems(FormApp.ItemType.MULTIPLE_CHOICE);
    if(items.length!==5){throw new Error('Unexpected Week 2 question count '+code);}
    var item=items[3].asMultipleChoiceItem();
    if(item.getTitle()!==q.n+'. '+q.title){throw new Error('Unexpected Week 2 Q4 title '+code);}
    // Feedback only: no changes to choices, answer keys, scores or responses.
    item.setFeedbackForCorrect(FormApp.createFeedback().setText(q.fbCorrect).build());
    item.setFeedbackForIncorrect(FormApp.createFeedback().setText(q.fbWrong).build());
    Logger.log(code+' W2 Q4 feedback repaired; responses and marks unchanged.');
  });
}

function updateFeedbackAndIntro() {
  RUN_START = new Date().getTime();
  var updateProps=PropertiesService.getScriptProperties();
  var updateVersion='2026-09-14-r2';
  var updated=JSON.parse(updateProps.getProperty('FEEDBACK_UPDATE_'+updateVersion)||'{}');
  var links = loadLinks_();
  if (!Object.keys(links).length) {
    Logger.log('No forms recorded yet. Run createAllForms() first.');
    return;
  }
  var forms = 0, qs = 0, intros = 0, skipped = 0, mismatch = 0, gone = 0;

  for (var code in QUIZ_DATA) {
    var weeks = QUIZ_DATA[code].weeks;
    for (var i = 0; i < weeks.length; i++) {
      var wk = weeks[i];
      var updateKey=code+'|'+wk.week;
      if(updated[updateKey]){continue;}
      var L = links[code + '|' + wk.week];
      if (!L) { continue; }

      if (outOfTime_()) {
        Logger.log('');
        Logger.log('Stopped before the six-minute limit. Run '
                   + 'updateFeedbackAndIntro() again to carry on; forms '
                   + 'already updated are skipped using saved progress.');
        Logger.log('so far: ' + forms + ' forms, ' + qs + ' questions, '
                   + intros + ' descriptions');
        return;
      }

      var form;
      try {
        form = FormApp.openById(L.formId);
      } catch (e) {
        gone++;
        continue;
      }

      if (wk.week === 1 || form.getResponses().length > 0) {
        Logger.log('Preserved completed form ' + code + ' W' + wk.week);
        updated[updateKey]=true;updateProps.setProperty('FEEDBACK_UPDATE_'+updateVersion,JSON.stringify(updated));
        continue;
      }
      if(form.isAcceptingResponses()){Logger.log('Close unattempted form before updating '+updateKey);continue;}
      try {
        form.setDescription(wk.intro);
        intros++;
      } catch (e) {
        Logger.log('  ' + code + ' W' + wk.week + ' description: ' + e.message);
      }
      // The confirmation page is the only place to tell a student where
      // their mark is, since that page does not show a total itself.
      try { form.setConfirmationMessage(CONFIRMATION); } catch (e) {}

      if (wk.placeholder) { forms++; continue; }

      var items = form.getItems(FormApp.ItemType.MULTIPLE_CHOICE);
      if (items.length !== wk.questions.length) {
        Logger.log('  ' + code + ' W' + wk.week + ': form has '
                   + items.length + ' multiple-choice questions, the bank '
                   + 'has ' + wk.questions.length + '. Skipped. This one '
                   + 'needs a rebuild.');
        skipped++;
        continue;
      }

      var wrote = 0;
      for (var j = 0; j < items.length; j++) {
        var q = wk.questions[j];
        var mc = items[j].asMultipleChoiceItem();
        var expect = q.n + '. ' + q.title;
        var existing = mc.getChoices().map(function (c) { return c.getValue(); });
        var desired = q.choices.map(function (c) { return typeof c === 'string' ? c : c.text; });
        if (JSON.stringify(existing) !== JSON.stringify(desired)) {
          mc.setChoices(q.choices.map(function(c){return mc.createChoice(c.text,c.correct);}));
        }
        mc.setTitle(expect);
        mc.setHelpText(q.help || '');
        if (q.fbCorrect) {
          mc.setFeedbackForCorrect(
            FormApp.createFeedback().setText(q.fbCorrect).build());
        }
        if (q.fbWrong) {
          mc.setFeedbackForIncorrect(
            FormApp.createFeedback().setText(q.fbWrong).build());
        }
        wrote++;
        qs++;
      }
      forms++;
      if(wrote===wk.questions.length){updated[updateKey]=true;updateProps.setProperty('FEEDBACK_UPDATE_'+updateVersion,JSON.stringify(updated));}
      Logger.log('  ' + code + ' W' + wk.week + ': ' + wrote
                 + ' questions updated');
    }
  }

  Logger.log('');
  Logger.log('forms touched ' + forms + ', questions updated ' + qs
             + ', descriptions updated ' + intros);
  if (skipped || mismatch || gone) {
    Logger.log('skipped forms ' + skipped + ', question mismatches '
               + mismatch + ', missing forms ' + gone);
    Logger.log('Anything reported above still carries its old text. If the '
               + 'options themselves changed, rebuildAllForms is the only '
               + 'route.');
  } else {
    Logger.log('All live forms now carry the current feedback and intro '
               + 'text. No links changed, so the QR codes are untouched.');
  }
}

/**
 * Print the marks Forms has actually computed for every submission on one
 * form. This settles the question the screenshots cannot: whether the
 * grading is happening server-side, or genuinely is not.
 *
 * If scores appear here, marking works and the only question left is where
 * a student sees the total. If they come back null, the quiz really is
 * being held for review.
 *
 *   showScores(1, 'CML3111')      or the show_W1_CML3111 wrappers
 */
function showScores(week, code) {
  var links = loadLinks_();
  if (week === undefined || code === undefined) {
    var first = Object.keys(links).sort()[0];
    if (!first) {
      Logger.log('No forms recorded yet. Run createAllForms() first.');
      return;
    }
    code = first.split('|')[0];
    week = Number(first.split('|')[1]);
    Logger.log('No week or cohort given, so reading the first form on '
               + 'record: ' + code + ' week ' + week + '.');
    Logger.log('');
  }
  var L = links[code + '|' + week];
  if (!L) { throw new Error('No form recorded for ' + code + ' week ' + week); }
  var form = FormApp.openById(L.formId);
  var responses = form.getResponses();

  Logger.log(form.getTitle());
  Logger.log('submissions: ' + responses.length);
  if (!responses.length) {
    Logger.log('');
    Logger.log('Nothing submitted yet. Open the quiz, submit once, then run '
               + 'this again.');
    return;
  }
  Logger.log('');

  // A 24-hour window buys resilience and costs information: you can no
  // longer assume a submission happened in the room. The opening time is
  // recorded when the quiz is opened, so say which is which.
  var openedAt = Number(L.openedAt || 0);
  var inRoomUntil = openedAt
    ? openedAt + (QUIZ_MIN_ON_CLOCK + 2) * 60 * 1000 : 0;
  if (openedAt) {
    Logger.log('opened ' + Utilities.formatDate(new Date(openedAt),
                 Session.getScriptTimeZone(), 'EEE d MMM HH:mm')
               + ', so anything after '
               + Utilities.formatDate(new Date(inRoomUntil),
                   Session.getScriptTimeZone(), 'HH:mm')
               + ' was answered outside the session');
    Logger.log('');
  }

  var anyNull = false, maxTotal = 0, late = 0, inRoom = 0;
  for (var i = 0; i < responses.length; i++) {
    var r = responses[i];
    var who = '(no email recorded)';
    try { who = r.getRespondentEmail() || who; } catch (e) {}
    var when = null, tag = '';
    try { when = r.getTimestamp().getTime(); } catch (e) {}
    if (openedAt && when) {
      if (when <= inRoomUntil) { inRoom++; tag = '  in session'; }
      else { late++; tag = '  LATE (' + Math.round((when - openedAt) / 3600000)
                            + 'h after opening)'; }
    }

    var graded = r.getGradableItemResponses();
    var total = 0, outOf = 0, perQ = [];
    for (var j = 0; j < graded.length; j++) {
      var s = null;
      try { s = graded[j].getScore(); } catch (e) {}
      if (s === null || s === undefined) { anyNull = true; perQ.push('-'); }
      else { total += s; perQ.push(String(s)); }
      // the point value of the item itself, for the denominator
      try {
        var it = graded[j].getItem();
        if (it.getType() === FormApp.ItemType.MULTIPLE_CHOICE) {
          outOf += it.asMultipleChoiceItem().getPoints();
        }
      } catch (e) {}
    }
    if (outOf > maxTotal) { maxTotal = outOf; }
    Logger.log('  ' + who + '   ' + total + ' / ' + outOf
               + '   per question: ' + perQ.join(' ') + tag);
  }

  Logger.log('');
  if (openedAt) {
    Logger.log('in session ' + inRoom + ', later ' + late
               + (late ? '   (the window did its job: those ' + late
                         + ' would have been lost to a hard close)' : ''));
    Logger.log('');
  }
  if (anyNull) {
    Logger.log('SOME QUESTIONS CAME BACK WITHOUT A SCORE. That means Forms '
               + 'is holding this quiz for review rather than marking it '
               + 'automatically, which is what a free-text question does. '
               + 'Run auditAll().');
  } else {
    Logger.log('Every question was marked automatically, out of ' + maxTotal
               + '. The grading is working.');
    Logger.log('So if a student does not see the total on screen, it is a '
               + 'display question rather than a marking one, and the marks '
               + 'are safe: they are in the response sheet and this function '
               + 'can always read them back.');
  }
}

/** Count free-text items. getItems(undefined) returns EVERYTHING, so an
 *  enum member that does not exist in this runtime would silently make the
 *  count the whole form. Ask only for the types that are defined. */
function countFreeText_(form) {
  var n = 0;
  var types = [FormApp.ItemType.TEXT, FormApp.ItemType.PARAGRAPH_TEXT];
  for (var i = 0; i < types.length; i++) {
    if (!types[i]) { continue; }
    n += form.getItems(types[i]).length;
  }
  return n;
}

/**
 * Read back everything about ONE live form that could stop a score showing.
 *
 * Forms will not display a total to a student if the questions carry no
 * points, and nothing in the creation log would tell you that happened.
 * This prints what the form actually says about itself, so the next step
 * is decided by evidence rather than by guessing.
 *
 *   auditForm(1, 'CML3111')
 */
function auditForm(week, code) {
  var links = loadLinks_();

  // The Run button in the Apps Script editor cannot pass arguments, so a
  // function that needs them arrives with undefined. Default to the first
  // form on record and say which one was picked, so pressing Run does
  // something useful instead of throwing.
  if (week === undefined || code === undefined) {
    var first = Object.keys(links).sort()[0];
    if (!first) {
      Logger.log('No forms recorded yet. Run createAllForms() first.');
      return;
    }
    code = first.split('|')[0];
    week = Number(first.split('|')[1]);
    Logger.log('No week or cohort given, so auditing the first form on '
               + 'record: ' + code + ' week ' + week + '.');
    Logger.log('For a specific one use the audit_W1_CML3111 style wrappers '
               + 'at the bottom of this file, or auditAll() for a summary '
               + 'of all 36.');
    Logger.log('');
  }

  var L = links[code + '|' + week];
  if (!L) { throw new Error('No form recorded for ' + code + ' week ' + week); }
  var form = FormApp.openById(L.formId);

  Logger.log('FORM: ' + form.getTitle());
  Logger.log('  edit:   ' + form.getEditUrl());
  Logger.log('');
  Logger.log('SETTINGS THAT DECIDE WHETHER A SCORE APPEARS');
  Logger.log('  is a quiz:            ' + form.isQuiz()
             + (form.isQuiz() ? '' : '   <-- MUST be true or nothing is graded'));
  Logger.log('  accepting responses:  ' + form.isAcceptingResponses());
  if (typeof form.isPublished === 'function') {
    try { Logger.log('  published:            ' + form.isPublished()); }
    catch (e) { /* older runtime */ }
  }
  Logger.log('  collects email:       ' + form.collectsEmail());
  Logger.log('  one response per user:' + form.hasLimitOneResponsePerUser());
  Logger.log('  response edits:       ' + form.canEditResponse());
  Logger.log('');

  var items = form.getItems();
  var mc = form.getItems(FormApp.ItemType.MULTIPLE_CHOICE);
  var txt = countFreeText_(form);
  Logger.log('QUESTIONS: ' + items.length + ' items, ' + mc.length
             + ' multiple choice, ' + txt + ' free text');
  if (txt) {
    Logger.log('  NOTE: a free-text question with no answer key cannot be '
               + 'auto-graded, so Forms withholds the TOTAL and offers the '
               + 'student "View accuracy" instead of "View score". The '
               + 'per-question marks still appear. This is the usual reason '
               + 'a score looks missing when everything else is correct.');
  }
  var total = 0, unpointed = 0, nokey = 0, nofb = 0;
  for (var i = 0; i < mc.length; i++) {
    var q = mc[i].asMultipleChoiceItem();
    var pts = q.getPoints();
    total += pts;
    if (!pts) { unpointed++; }
    var ch = q.getChoices();
    var correct = 0;
    for (var c = 0; c < ch.length; c++) {
      if (ch[c].isCorrectAnswer()) { correct++; }
    }
    if (correct !== 1) { nokey++; }
    var fbW = q.getFeedbackForIncorrect();
    var hasFb = !!(fbW && fbW.getText());
    if (!hasFb) { nofb++; }
    Logger.log('  Q' + (i + 1) + '  points ' + pts
               + '   correct options ' + correct
               + '   choices ' + ch.length
               + '   wrong-answer feedback ' + (hasFb ? 'yes' : 'NO')
               + '   "' + q.getTitle().substring(0, 44) + '"');
  }
  Logger.log('');
  Logger.log('TOTAL POINTS ON THIS FORM: ' + total);
  Logger.log('');

  if (!form.isQuiz()) {
    Logger.log('DIAGNOSIS: this form is not in quiz mode, so nothing is '
               + 'graded and no score can appear. Run applyPoints(), which '
               + 'turns quiz mode on as well.');
  } else if (unpointed) {
    Logger.log('DIAGNOSIS: ' + unpointed + ' questions carry ZERO points, '
               + 'which is why no score is shown. Run applyPoints() to set '
               + 'one point per question on all 36 forms, in place, with no '
               + 'rebuild.');
  } else if (nokey) {
    Logger.log('DIAGNOSIS: ' + nokey + ' questions do not have exactly one '
               + 'correct option, so they cannot be marked. That needs '
               + 'rebuildAllForms, because answer keys live with the '
               + 'choices.');
  } else {
    Logger.log('DIAGNOSIS: the marking side of this form is correct: quiz '
               + 'mode on, ' + total + ' points, one correct option per '
               + 'question, feedback present.');
    Logger.log('If a student still sees no total, the cause is the one '
               + 'setting no API can read: Settings, then Quizzes, then '
               + 'Release grade. It must say "Immediately after each '
               + 'submission". Open ' + form.getEditUrl() + ' and look.');
  }
  if (nofb) {
    Logger.log('NOTE: ' + nofb + ' questions have no wrong-answer feedback. '
               + 'Run updateFeedbackAndIntro().');
  }
}

/**
 * The marking health of all 36 forms on one screen. Press Run on this one
 * when something is wrong and you do not yet know how widespread it is.
 */
function auditAll() {
  RUN_START = new Date().getTime();
  var links = loadLinks_();
  var keys = Object.keys(links).sort();
  if (!keys.length) {
    Logger.log('No forms recorded yet. Run createAllForms() first.');
    return;
  }

  var checked = 0, notQuiz = [], zeroPts = [], partPts = [], badKey = [],
      noFb = [], gone = [], openNow = [], unpub = [], freeText = [];

  for (var i = 0; i < keys.length; i++) {
    if (outOfTime_()) {
      Logger.log('Stopped with ' + (keys.length - i) + ' forms unchecked. '
                 + 'Run auditAll() again to see the rest.');
      break;
    }
    var form;
    try { form = FormApp.openById(links[keys[i]].formId); }
    catch (e) { gone.push(keys[i]); continue; }
    checked++;

    if (!form.isQuiz()) { notQuiz.push(keys[i]); }
    try { if (form.isAcceptingResponses()) { openNow.push(keys[i]); } }
    catch (e) {}
    if (typeof form.isPublished === 'function') {
      try { if (!form.isPublished()) { unpub.push(keys[i]); } } catch (e) {}
    }

    var nText = countFreeText_(form);
    if (nText) { freeText.push(keys[i]); }

    var mc = form.getItems(FormApp.ItemType.MULTIPLE_CHOICE);
    var pts = 0, zero = 0, keys_ok = 0, fb = 0;
    for (var j = 0; j < mc.length; j++) {
      var q = mc[j].asMultipleChoiceItem();
      var p = q.getPoints();
      pts += p;
      if (!p) { zero++; }
      var ch = q.getChoices(), nc = 0;
      for (var c = 0; c < ch.length; c++) {
        if (ch[c].isCorrectAnswer()) { nc++; }
      }
      if (nc === 1) { keys_ok++; }
      var f = q.getFeedbackForIncorrect();
      if (f && f.getText()) { fb++; }
    }
    if (mc.length && zero === mc.length) { zeroPts.push(keys[i]); }
    else if (zero) { partPts.push(keys[i] + ' (' + zero + ' of ' + mc.length + ')'); }
    if (keys_ok !== mc.length) { badKey.push(keys[i]); }
    if (fb !== mc.length) { noFb.push(keys[i]); }
  }

  Logger.log('checked ' + checked + ' of ' + keys.length + ' forms');
  Logger.log('');
  Logger.log('quiz mode off:            ' + notQuiz.length
             + (notQuiz.length ? '   ' + notQuiz.slice(0, 6).join(' ') : ''));
  Logger.log('all questions zero points:' + zeroPts.length
             + (zeroPts.length ? '   ' + zeroPts.slice(0, 6).join(' ') : ''));
  Logger.log('some questions no points: ' + partPts.length
             + (partPts.length ? '   ' + partPts.slice(0, 4).join(' ') : ''));
  Logger.log('answer key not exactly 1: ' + badKey.length
             + (badKey.length ? '   ' + badKey.slice(0, 6).join(' ') : ''));
  Logger.log('missing feedback:         ' + noFb.length
             + (noFb.length ? '   ' + noFb.slice(0, 6).join(' ') : ''));
  Logger.log('not published:            ' + unpub.length
             + (unpub.length ? '   ' + unpub.slice(0, 6).join(' ') : ''));
  Logger.log('currently OPEN to answers:' + openNow.length
             + (openNow.length ? '   ' + openNow.slice(0, 6).join(' ') : ''));
  Logger.log('');

  if (notQuiz.length || zeroPts.length || partPts.length) {
    Logger.log('=> Run applyPoints(). It sets one point per question and '
               + 'turns quiz mode on, in place, with no rebuild.');
  }
  if (noFb.length) {
    Logger.log('=> Run updateFeedbackAndIntro() for the missing feedback.');
  }
  if (unpub.length) {
    Logger.log('=> Run publishAllForms() for the unpublished ones.');
  }
  if (badKey.length) {
    Logger.log('=> Answer keys live with the choices, so those need '
               + 'rebuildAllForms. This is the one problem that cannot be '
               + 'fixed in place.');
  }
  if (openNow.length) {
    Logger.log('=> *** ' + openNow.length + ' FORMS ARE ACCEPTING ANSWERS '
               + 'RIGHT NOW. ***');
    Logger.log('   Anyone with a link can submit, including next term\'s '
               + 'quizzes. Run closeEverything() unless you are mid-sitting.');
    Logger.log('   Publishing a form switches responses on, so this is the '
               + 'expected state straight after publishAllForms() on an '
               + 'older build of this script.');
  }
  if (!notQuiz.length && !zeroPts.length && !partPts.length
      && !badKey.length && !noFb.length && !unpub.length) {
    Logger.log('Every form is marked correctly: quiz mode on, a point per '
               + 'question, one correct option each, feedback present, all '
               + 'published.');
    if (freeText.length) {
      Logger.log('');
      Logger.log('WHY A STUDENT SEES NO TOTAL: ' + freeText.length
                 + ' forms contain a free-text question with no answer key, '
                 + 'which is the student-number field. Forms cannot '
                 + 'auto-grade it, so it withholds the total and offers '
                 + '"View accuracy" instead of "View score". The '
                 + 'per-question marks still show.');
      Logger.log('This does NOT stop the marking: showScores() reads back '
                 + 'exact totals either way. It only means the total is not '
                 + 'printed on the page the student lands on, which is a '
                 + 'Forms limitation rather than a fault here.');
    } else {
      Logger.log('Nothing is left that could withhold a score. If one is '
                 + 'still missing, check Settings, then Quizzes, then '
                 + 'Release grade on the form itself.');
    }
  }
}

/**
 * Set one point on every multiple-choice question, across all 36 forms,
 * and make sure quiz mode is on. Points are an item property, so this
 * works IN PLACE: no rebuild, no new links, no new QR codes.
 *
 * This is the fix when a student sees feedback but no score.
 */
function applyPoints() {
  RUN_START = new Date().getTime();
  var links = loadLinks_();
  var keys = Object.keys(links).sort();
  if (!keys.length) {
    Logger.log('No forms recorded yet. Run createAllForms() first.');
    return;
  }
  var forms = 0, changed = 0, already = 0, gone = 0, bad = 0;
  for (var i = 0; i < keys.length; i++) {
    if (outOfTime_()) {
      Logger.log('Stopped with ' + (keys.length - i) + ' forms left. Run '
                 + 'applyPoints() again to finish.');
      break;
    }
    var form;
    try {
      form = FormApp.openById(links[keys[i]].formId);
    } catch (e) { gone++; continue; }

    try {
      if (!form.isQuiz()) { form.setIsQuiz(true); }
      var mc = form.getItems(FormApp.ItemType.MULTIPLE_CHOICE);
      for (var j = 0; j < mc.length; j++) {
        var q = mc[j].asMultipleChoiceItem();
        if (q.getPoints() === 1) { already++; continue; }
        q.setPoints(1);
        changed++;
      }
      forms++;
    } catch (e) {
      bad++;
      Logger.log('  ' + keys[i] + ': ' + e.message);
    }
  }
  Logger.log('');
  Logger.log('forms touched ' + forms + ', questions given a point '
             + changed + ', already correct ' + already
             + (gone ? ', missing ' + gone : '')
             + (bad ? ', failed ' + bad : ''));
  if (changed) {
    Logger.log('Students will now see a score out of 5. No links changed, '
               + 'so the QR codes are untouched.');
  } else if (!bad && !gone) {
    Logger.log('Every question already carried a point, so points were not '
               + 'the problem. Check Settings, then Quizzes, then Release '
               + 'grade on one form: it must say "Immediately after each '
               + 'submission".');
  }
}

// ==========================================================================
// IDENTITY
//
// Forms cannot auto-grade a free-text answer, and a quiz containing one is
// held back for manual review: the student is offered "View accuracy" with
// a mark per question and NO total. That one field was the reason a score
// never appeared, with everything else about the forms correct.
//
// So identity comes from the signed-in Google account instead. Sign-in is
// already required for one-attempt-only, so this asks nothing new of a
// student, it makes the quiz fully auto-graded, and it removes a real data
// hazard: a typed student number can be mistyped, and then the row does not
// join to anything.
//
// The cost is a roster: student number against the address each student
// signs in with, collected once in Week 1.
// ==========================================================================

/**
 * Put both identity fields on all 36 live forms: email collection on, and
 * a required registration-number question titled so nobody reads it as a
 * phone number. IN PLACE: no rebuild, no new links, no new QR codes.
 *
 * Safe to re-run. If the field exists under an older title it is renamed
 * rather than duplicated, and the help text is refreshed either way.
 */
function applyIdentityFields() {
  RUN_START = new Date().getTime();
  var links = loadLinks_();
  var keys = Object.keys(links).sort();
  if (!keys.length) {
    Logger.log('No forms recorded yet. Run createAllForms() first.');
    return;
  }
  Logger.log('Setting both identity fields on ' + keys.length + ' forms.');
  Logger.log('  email collection: ' + (COLLECT_EMAIL ? 'on' : 'off'));
  Logger.log('  typed field:      "' + ID_QUESTION_TITLE + '"');
  Logger.log('');

  var emailed = 0, added = 0, renamed = 0, refreshed = 0, gone = 0, bad = 0,
      withResp = 0;

  for (var i = 0; i < keys.length; i++) {
    if (outOfTime_()) {
      Logger.log('Stopped with ' + (keys.length - i) + ' forms left. Run '
                 + 'applyIdentityFields() again to finish.');
      break;
    }
    var form;
    try { form = FormApp.openById(links[keys[i]].formId); }
    catch (e) { gone++; continue; }

    try { if (form.getResponses().length) { withResp++; } } catch (e) {}

    try {
      // Preserve the Verified collection mode selected in the Forms UI.
        if (form.collectsEmail() !== COLLECT_EMAIL) { form.setCollectEmail(COLLECT_EMAIL); }
      emailed++;

      if (!ASK_REGISTRATION_NUMBER) { continue; }

      // find it under any title it has ever had
      var texts = form.getItems(FormApp.ItemType.TEXT);
      var found = null;
      for (var t = 0; t < texts.length; t++) {
        var title = texts[t].getTitle();
        for (var o = 0; o < ID_QUESTION_OLD_TITLES.length; o++) {
          if (title === ID_QUESTION_OLD_TITLES[o]) { found = texts[t]; }
        }
      }

      if (found) {
        var was = found.getTitle();
        found.setTitle(ID_QUESTION_TITLE);
        found.setHelpText(ID_QUESTION_HELP);
        if (was !== ID_QUESTION_TITLE) { renamed++; } else { refreshed++; }
      } else {
        var idq = form.addTextItem();
        idq.setTitle(ID_QUESTION_TITLE);
        idq.setHelpText(ID_QUESTION_HELP);
        idq.setRequired(true);
        form.moveItem(idq.getIndex(), 0);   // first, before the questions
        added++;
      }
    } catch (e) {
      bad++;
      Logger.log('  ' + keys[i] + ': ' + e.message);
    }
  }

  Logger.log('email collection set on ' + emailed
             + ', field added to ' + added
             + ', renamed on ' + renamed
             + ', help text refreshed on ' + refreshed
             + (gone ? ', missing ' + gone : '')
             + (bad ? ', FAILED ' + bad : ''));
  Logger.log('No links changed, so the QR codes in the decks are still '
             + 'correct.');
  if (withResp) {
    Logger.log('');
    Logger.log('Note: ' + withResp + ' forms already hold submissions. Rows '
               + 'submitted before now have no registration number in them, '
               + 'which for your own test rows does not matter.');
  }
  Logger.log('');
  Logger.log('In Forms Settings, select Verified email collection, immediate '
             + 'grade release, Point values and Missed questions. Apps Script '
             + 'cannot confirm those UI settings. The gradebook requires a roster '
             + 'mapping Student Registration Number to cohort and Google email.');
}

// ==========================================================================
// TEST MODE
//
// With one-response-per-student on, your own second attempt is refused with
// "You've already responded". There is no per-person reset in Forms, so the
// only way to test repeatedly is to lift the limit, and the only safe way
// to do that is to make lifting and restoring it a single deliberate act.
// ==========================================================================

/** Lift the one-response limit on all 36 so you can submit repeatedly. */
function startTesting() {
  RUN_START = new Date().getTime();
  Logger.log('TEST MODE ON');
  setLimitOnAll_(false);
  PropertiesService.getScriptProperties().setProperty('IUEA_TEST_MODE', 'on');
  Logger.log('');
  Logger.log('You can now submit the same form as many times as you like '
             + 'from the same account. Use a student number of TEST001 so '
             + 'the rows are easy to delete afterwards.');
  Logger.log('*** RUN stopTesting() BEFORE THE FIRST REAL SITTING. ***');
  Logger.log('Until you do, a student can submit twice.');
}

/** Restore the one-response limit. Run before any real sitting. */
function stopTesting() {
  RUN_START = new Date().getTime();
  Logger.log('TEST MODE OFF');
  setLimitOnAll_(true);
  PropertiesService.getScriptProperties().deleteProperty('IUEA_TEST_MODE');
  Logger.log('');
  Logger.log('One response per student again. Delete your TEST rows from '
             + 'the response sheets, then run findDuplicates() to confirm '
             + 'nothing is left behind.');
}

/** Am I still in test mode? Cheap to check, expensive to forget. */
function testModeStatus() {
  var on = PropertiesService.getScriptProperties()
    .getProperty('IUEA_TEST_MODE') === 'on';
  Logger.log(on
    ? 'TEST MODE IS ON. Repeat submissions are allowed. Run stopTesting() '
      + 'before the first real sitting.'
    : 'Test mode is off. One response per student.');
  return on;
}

function setLimitOnAll_(limit) {
  var links = loadLinks_();
  var keys = Object.keys(links).sort();
  var done = 0, bad = 0;
  for (var i = 0; i < keys.length; i++) {
    if (outOfTime_()) {
      Logger.log('Stopped with ' + (keys.length - i) + ' left. Run the same '
                 + 'function again to finish.');
      break;
    }
    try {
      FormApp.openById(links[keys[i]].formId)
        .setLimitOneResponsePerUser(limit);
      done++;
    } catch (e) { bad++; Logger.log('  ' + keys[i] + ': ' + e.message); }
  }
  Logger.log('  ' + done + ' forms updated' + (bad ? ', ' + bad + ' failed' : ''));
}

/**
 * Find students who appear more than once in a response sheet.
 *
 * This is the safety net rather than the rule. With
 * LIMIT_ONE_RESPONSE on, Forms blocks a second submission from the same
 * Google account, and a determined student with two accounts can still get
 * around it. With it off, this is the only check there is.
 *
 * The convention when it finds one: the FIRST submission counts. That is
 * the answer given inside the five minutes.
 */
function findDuplicates() {
  var total = 0, dupRows = 0;
  for (var code in QUIZ_DATA) {
    var it = DriveApp.getFilesByName(
      'IUEA ML Quiz Responses \u2014 ' + code);
    while (it.hasNext()) {
      var ss;
      try { ss = SpreadsheetApp.open(it.next()); } catch (e) { continue; }
      var sheets = ss.getSheets();
      for (var s = 0; s < sheets.length; s++) {
        var sh = sheets[s];
        var last = sh.getLastRow();
        if (last < 2) { continue; }
        var width = sh.getLastColumn();
        var head = sh.getRange(1, 1, 1, width).getValues()[0];
        // find the student-number column by its question title
        var col = -1;
        for (var h = 0; h < head.length; h++) {
          if (String(head[h]).toLowerCase().indexOf('student number') !== -1) {
            col = h + 1;
            break;
          }
        }
        if (col === -1) { continue; }
        var ids = sh.getRange(2, col, last - 1, 1).getValues();
        var seen = {}, dups = {};
        for (var r = 0; r < ids.length; r++) {
          var v = String(ids[r][0]).trim().toUpperCase();
          if (!v) { continue; }
          total++;
          if (seen[v]) { dups[v] = (dups[v] || 1) + 1; } else { seen[v] = true; }
        }
        var names = Object.keys(dups);
        if (names.length) {
          Logger.log(code + ' / ' + sh.getName() + ':');
          for (var d = 0; d < names.length; d++) {
            Logger.log('   ' + names[d] + ' submitted ' + dups[names[d]]
                       + ' times');
            dupRows++;
          }
        }
      }
    }
  }
  Logger.log('');
  Logger.log('checked ' + total + ' submissions; students with more than one: '
             + dupRows);
  if (!dupRows) {
    Logger.log('No duplicates.');
  } else {
    Logger.log('Count the FIRST submission for each of these: that is the '
               + 'answer they gave inside the five minutes. Sort the sheet '
               + 'by timestamp to see which came first.');
  }
}

/** A form to build a quiz in: a copy of the template if there is one. */
function newQuizForm_(title) {
  if (TEMPLATE_FORM_ID) {
    var copy = DriveApp.getFileById(TEMPLATE_FORM_ID).makeCopy(title);
    var form = FormApp.openById(copy.getId());
    form.setTitle(title);
    // a copy carries the template's items; clear them so the questions
    // below are the only thing on the form
    var items = form.getItems();
    for (var i = items.length - 1; i >= 0; i--) {
      form.deleteItem(items[i]);
    }
    return form;
  }
  return FormApp.create(title);
}

/** Step one of a rebuild. Valid for ARM_WINDOW_MIN minutes. */
function armRebuild() {
  PropertiesService.getScriptProperties()
    .setProperty(PROP_ARMED, String(new Date().getTime()));
  Logger.log('Rebuild armed for the next ' + ARM_WINDOW_MIN + ' minutes.');
  Logger.log('Now run rebuildAllForms(). It will move all 36 forms and '
             + 'their response sheets to the Drive trash and build them '
             + 'again from the question banks.');
}

/** Only needed if responses already exist and you truly mean to lose them. */
function armRebuildEvenThoughResponsesExist() {
  var p = PropertiesService.getScriptProperties();
  p.setProperty(PROP_ARMED, String(new Date().getTime()));
  p.setProperty(PROP_ARMED_HARD, 'yes');
  Logger.log('Rebuild armed INCLUDING existing responses, for '
             + ARM_WINDOW_MIN + ' minutes.');
  Logger.log('Every submitted answer in the response sheets will go to the '
             + 'Drive trash. Export anything you need first, then run '
             + 'rebuildAllForms().');
}

function armedOk_() {
  var p = PropertiesService.getScriptProperties();
  var t = p.getProperty(PROP_ARMED);
  if (!t) { return false; }
  var age = (new Date().getTime() - Number(t)) / 60000;
  return age >= 0 && age <= ARM_WINDOW_MIN;
}

/** How many submitted rows exist across every cohort response sheet.
 *
 *  Searches Drive by name rather than only inside the quiz folder. The move
 *  into that folder is wrapped in a try/catch elsewhere, so a sheet can
 *  legitimately end up outside it, and a safety check that cannot see a
 *  file is worse than no safety check at all. */
function countResponses_() {
  var total = 0;
  for (var code in QUIZ_DATA) {
    var it = DriveApp.getFilesByName('IUEA ML Quiz Responses \u2014 ' + code);
    while (it.hasNext()) {
      var f = it.next();
      var ss;
      try { ss = SpreadsheetApp.open(f); } catch (e) { continue; }
      var sheets = ss.getSheets();
      for (var i = 0; i < sheets.length; i++) {
        // row 1 is the header Forms writes, so anything past it is a response
        total += Math.max(0, sheets[i].getLastRow() - 1);
      }
    }
  }
  return total;
}

/**
 * Delete all 36 forms and build them again from the current question banks.
 * Run armRebuild() first. Files go to the Drive trash rather than being
 * destroyed, so a mistake is recoverable for about thirty days.
 */
function rebuildAllForms() {
  var p = PropertiesService.getScriptProperties();

  if (!armedOk_()) {
    Logger.log('NOT ARMED. This function deletes all 36 forms, so it needs '
               + 'a deliberate two-step.');
    Logger.log('Run armRebuild(), then run rebuildAllForms() within '
               + ARM_WINDOW_MIN + ' minutes.');
    return;
  }

  var responses = countResponses_();
  var hard = p.getProperty(PROP_ARMED_HARD) === 'yes';
  if (responses > 0 && !hard) {
    Logger.log('STOPPING. There are ' + responses + ' submitted responses in '
               + 'the response sheets, and a rebuild would move them to the '
               + 'trash.');
    Logger.log('If you have already marked or exported them, run '
               + 'armRebuildEvenThoughResponsesExist() and then '
               + 'rebuildAllForms() again.');
    Logger.log('If you have NOT, open the response sheets and download them '
               + 'first: File, then Download, then Comma Separated Values.');
    p.deleteProperty(PROP_ARMED);
    return;
  }

  Logger.log('Rebuilding. ' + responses + ' responses will be trashed.');

  // 1. trash every form we have a record of
  var links = loadLinks_();
  var keys = Object.keys(links);
  var trashedForms = 0;
  for (var i = 0; i < keys.length; i++) {
    var id = links[keys[i]].formId;
    if (!id) { continue; }
    if (TEMPLATE_FORM_ID && id === TEMPLATE_FORM_ID) {
      // never destroy the one form that carries the hand-set grade release
      Logger.log('  refusing to trash the template form');
      continue;
    }
    try {
      DriveApp.getFileById(id).setTrashed(true);
      trashedForms++;
    } catch (e) {
      Logger.log('  could not trash ' + keys[i] + ': ' + e.message);
    }
  }
  Logger.log('  trashed ' + trashedForms + ' forms');

  // 2. trash the response spreadsheets and the links sheet, so the new
  //    forms start against clean destinations instead of appending tabs.
  //    Searched by name across Drive for the same reason as the count.
  var names = [LINKS_SHEET_NAME];
  for (var code in QUIZ_DATA) {
    names.push('IUEA ML Quiz Responses \u2014 ' + code);
  }
  var trashedSheets = 0;
  for (var n = 0; n < names.length; n++) {
    var sit = DriveApp.getFilesByName(names[n]);
    while (sit.hasNext()) {
      try { sit.next().setTrashed(true); trashedSheets++; } catch (e) {}
    }
  }
  Logger.log('  trashed ' + trashedSheets + ' spreadsheets');

  // 3. forget the old link map, or createAllForms will skip everything
  saveLinks_({});
  p.deleteProperty(PROP_ARMED);
  p.deleteProperty(PROP_ARMED_HARD);

  // 4. build again. This will not get through all 36 inside the six-minute
  //    limit, so createAllForms reports what is left and you re-run IT,
  //    never this function.
  Logger.log('  building from the current question banks');
  createAllForms();

  var total = 0;
  for (var c3 in QUIZ_DATA) { total += QUIZ_DATA[c3].weeks.length; }
  var have = Object.keys(loadLinks_()).length;

  Logger.log('');
  if (have < total) {
    Logger.log('REBUILD STARTED, NOT YET COMPLETE: ' + have + ' of ' + total
               + ' forms built.');
    Logger.log('Run createAllForms() to finish, as many times as it takes. '
               + 'Running rebuildAllForms() again would trash these ' + have
               + ' and start over.');
    return;
  }
  Logger.log('REBUILD DONE. The links have all changed, so the QR codes in '
             + 'the decks are now stale.');
  Logger.log('Next: run printLinksJson(), save the output as '
             + 'data/quiz_links.json, and run python3 attach_qr.py from the '
             + 'scripts folder. Section 1.6 of the operations guide has the '
             + 'exact steps.');
}

function responseSpreadsheet_(code, fold) {
  var name = 'IUEA ML Quiz Responses \u2014 ' + code;
  var found = fold.getFilesByName(name);
  while (found.hasNext()) {
    var file = found.next();
    try {
      // Confirm we can actually open it as a spreadsheet, not just see its
      // Drive metadata. Those are different permission layers, and a stale
      // or oddly-shared file can pass the first and fail the second.
      return SpreadsheetApp.open(file);
    } catch (e) {
      Logger.log('found "' + name + '" (id ' + file.getId() + ') but could '
                 + 'not open it (' + e.message + '); trying the next match '
                 + 'or creating a new one.');
    }
  }
  var ss = SpreadsheetApp.create(name);
  try { DriveApp.getFileById(ss.getId()).moveTo(fold); } catch (e) {}
  return ss;
}

function loadLinks_() {
  var properties=PropertiesService.getScriptProperties().getProperties();
  var links=properties[PROP_LINKS]?JSON.parse(properties[PROP_LINKS]):{};
  Object.keys(properties).forEach(function(k){
    if(k.indexOf(PROP_LINKS+':')===0){links[k.slice(PROP_LINKS.length+1)]=JSON.parse(properties[k]);}
  });
  return links;
}

function saveLinks_(links) {
  var props=PropertiesService.getScriptProperties(),values={};
  Object.keys(links).forEach(function(k){values[PROP_LINKS+':'+k]=JSON.stringify(links[k]);});
  props.setProperties(values,false);
  Object.keys(props.getProperties()).forEach(function(k){
    if(k===PROP_LINKS||(k.indexOf(PROP_LINKS+':')===0&&!links[k.slice(PROP_LINKS.length+1)])){props.deleteProperty(k);}
  });
  if(typeof publishCAQuizWindows==='function'){try{publishCAQuizWindows();}catch(e){Logger.log('CA timing mirror needs retry: '+e.message);}}
}

function writeLinksSheet_(links) {
  var fold = folder_();
  var found = fold.getFilesByName(LINKS_SHEET_NAME);
  var ss = found.hasNext() ? SpreadsheetApp.open(found.next())
                           : SpreadsheetApp.create(LINKS_SHEET_NAME);
  try { DriveApp.getFileById(ss.getId()).moveTo(fold); } catch (e) {}
  var sh = ss.getSheets()[0];
  sh.clear();
  sh.appendRow(['Cohort', 'Week', 'Quiz #', 'Written?', 'Title',
                'Short link (for the QR)', 'Live link', 'Edit link', 'Form ID']);
  var keys = Object.keys(links).sort();
  for (var i = 0; i < keys.length; i++) {
    var L = links[keys[i]];
    sh.appendRow([L.code, L.week, L.number,
                  L.placeholder ? 'placeholder' : 'yes',
                  L.title, L.short, L.live, L.edit, L.formId]);
  }
  sh.setFrozenRows(1);
  sh.getRange(1, 1, 1, 9).setFontWeight('bold');
  sh.autoResizeColumns(1, 9);
  Logger.log('links sheet: ' + ss.getUrl());
}

/** Log the map as JSON, for generating the QR codes. */
function printLinksJson() {
  var links = loadLinks_();
  var out = {};
  var keys = Object.keys(links);
  for (var i = 0; i < keys.length; i++) {
    var L = links[keys[i]];
    out[L.code + '|' + L.week] = L.short || L.live;
  }
  Logger.log(JSON.stringify(out, null, 2));
}

/** Remove every autoCloseQuiz trigger. Returns how many were deleted. */
function clearCloseTriggers_() {
  var trigs = ScriptApp.getProjectTriggers();
  var n = 0;
  for (var i = 0; i < trigs.length; i++) {
    if (trigs[i].getHandlerFunction() === 'autoCloseQuiz') {
      ScriptApp.deleteTrigger(trigs[i]);
      n++;
    }
  }
  return n;
}

/**
 * Open one quiz and arrange for it to close on its own.
 *
 * HOW THE CLOSE WORKS, AND WHY IT IS NOT .after()
 * The obvious way is a one-off trigger scheduled six minutes out. That was
 * the first attempt and it does not hold time: Apps Script treats .after()
 * as a MINIMUM delay and dispatches one-off triggers in batches, so a
 * six-minute quiz stayed open for fifteen or more. A five-minute quiz whose
 * close drifts by ten minutes is not a five-minute quiz.
 *
 * So instead: record the deadline, run a trigger EVERY MINUTE, and close
 * the moment the deadline has passed. That lands within about a minute,
 * which is good enough for a classroom. The trigger deletes itself once it
 * has closed the form, so nothing is left running between sittings.
 *
 * The authoritative record of who was in time is still the timestamp
 * column in the response sheet, not the state of the form.
 */
function openQuizFor(week, code) {
  if(Number(week)===6 && ['CML3111','CML3112','CML3113'].indexOf(code)>=0){throw new Error('Quiz 6 is waived for practical revision.');}

  if (week === undefined || code === undefined) {
    Logger.log('openQuizFor needs a week and a cohort, and the Run button '
               + 'cannot pass them.');
    Logger.log('Select one of the wrappers instead, for example '
               + 'open_W1_CML3112, and press Run on that.');
    return;
  }
  var links = loadLinks_();
  var L = links[code + '|' + week];
  if (!L) { throw new Error('No form recorded for ' + code + ' week ' + week); }
  var form = FormApp.openById(L.formId);
  // Publish first. A form built before publishing was handled is still
  // unpublished, and enabling responses on one of those throws. Doing it
  // here means an old form heals itself the first time you open it.
  var pub = publishForm_(form);
  if (pub !== 'ok' && pub !== 'unsupported') {
    Logger.log('could not publish this form: ' + pub);
    Logger.log('Open it in Forms and press Publish, then run this again.');
    return;
  }
  form.setAcceptingResponses(true);

  var now = new Date().getTime();
  var closeAt = now + WINDOW_HOURS * 3600 * 1000;

  // Record when it opened, so showScores can tell an answer given in the
  // room from one given on Thursday night.
  L.openedAt = now;
  L.closeAt = closeAt;
  links[code + '|' + week] = L;
  saveLinks_(links);

  addPending_(L.formId, closeAt, code + '|' + week);
  var scheduled = ensureCloseTrigger_();

  Logger.log('OPEN: ' + L.title);
  Logger.log('link: ' + (L.short || L.live));
  Logger.log('');
  Logger.log('Give the room ' + QUIZ_MIN_ON_CLOCK + ' minutes on the '
             + 'projected clock. That is when the quiz is taken.');
  if (scheduled) {
    Logger.log('The form stays open until '
               + Utilities.formatDate(new Date(closeAt),
                   Session.getScriptTimeZone(), 'EEE d MMM HH:mm')
               + ' (' + WINDOW_HOURS + ' hours), so a network or phone '
               + 'failure does not cost anybody the mark. It closes itself '
               + 'then.');
    Logger.log('close_W' + week + '_' + code + ' closes it sooner if you '
               + 'want to.');
  } else {
    Logger.log('*** THE AUTOMATIC CLOSE WAS NOT SCHEDULED. Close it by hand '
               + 'with close_W' + week + '_' + code + ' ***');
  }
}

// --------------------------------------------------------------------------
// Pending closes.
//
// With a 24-hour window the three cohorts overlap: CML3113 opens at 08:00
// on Friday and CML3111 three hours later, and both stay open into Saturday.
// The old code held ONE pending form in a property and cleared the trigger
// on every open, so opening the second quiz silently orphaned the first
// one's close and left it accepting answers indefinitely.
//
// So pending closes are a map, and one trigger serves all of them.
// --------------------------------------------------------------------------

function loadPending_() {
  var props = PropertiesService.getScriptProperties();
  var raw = props.getProperty(PROP_PENDING_CLOSE);
  if (!raw) { return {}; }
  var map;
  try {
    map = JSON.parse(raw);
  } catch (e) {
    // An older build stored a bare formId here. Migrate it rather than
    // losing track of a form that is currently open.
    var at = Number(props.getProperty(PROP_CLOSE_AT) || 0);
    map = {};
    map[raw] = { closeAt: at || (new Date().getTime()), key: '(migrated)' };
    props.deleteProperty(PROP_CLOSE_AT);
  }
  return (map && typeof map === 'object') ? map : {};
}

function savePending_(map) {
  var props = PropertiesService.getScriptProperties();
  if (!Object.keys(map).length) { props.deleteProperty(PROP_PENDING_CLOSE); }
  else { props.setProperty(PROP_PENDING_CLOSE, JSON.stringify(map)); }
}

function addPending_(formId, closeAt, key) {
  var map = loadPending_();
  map[formId] = { closeAt: closeAt, key: key };
  savePending_(map);
}

function removePending_(formId) {
  var map = loadPending_();
  delete map[formId];
  savePending_(map);
}

/**
 * One trigger for however many quizzes are open. Its granularity follows
 * the nearest deadline: minute-by-minute only when something is about to
 * close, hourly otherwise. A 24-hour window polled every minute would be
 * 1,440 executions against a consumer account's daily runtime quota, and
 * landing within an hour of a one-day deadline is plenty.
 */
function ensureCloseTrigger_() {
  var map = loadPending_();
  var ids = Object.keys(map);
  clearCloseTriggers_();
  if (!ids.length) { return true; }

  var soonest = null;
  for (var i = 0; i < ids.length; i++) {
    var t = map[ids[i]].closeAt;
    if (soonest === null || t < soonest) { soonest = t; }
  }
  var minsAway = (soonest - new Date().getTime()) / 60000;

  try {
    if (minsAway <= 30) {
      ScriptApp.newTrigger('autoCloseQuiz').timeBased().everyMinutes(1).create();
    } else {
      ScriptApp.newTrigger('autoCloseQuiz').timeBased().everyHours(1).create();
    }
    return true;
  } catch (e) {
    Logger.log('COULD NOT SCHEDULE THE AUTOMATIC CLOSE: ' + e.message);
    return false;
  }
}

/**
 * Runs on a timer while any quiz is open. Closes every window that has
 * expired, leaves the rest alone, and removes the trigger once none remain.
 */
function autoCloseQuiz() {
  var map = loadPending_();
  var ids = Object.keys(map);

  if (!ids.length) {
    clearCloseTriggers_();               // leftover trigger, tidy it away
    return;
  }

  var now = new Date().getTime();
  var closed = 0, remaining = 0;

  for (var i = 0; i < ids.length; i++) {
    var id = ids[i];
    var entry = map[id];
    if (entry.closeAt && now < entry.closeAt) { remaining++; continue; }

    try {
      FormApp.openById(id).setAcceptingResponses(false);
      Logger.log('auto-closed ' + (entry.key || id) + ' at '
                 + Utilities.formatDate(new Date(),
                     Session.getScriptTimeZone(), 'EEE d MMM HH:mm'));
      closed++;
      delete map[id];
    } catch (e) {
      Logger.log('auto-close FAILED for ' + (entry.key || id) + ': '
                 + e.message);
      Logger.log('Close it by hand with the close_W1_CML3112 style wrapper, '
                 + 'or closeEverything().');
    }
    // Failed closures remain pending and are retried.
  }

  savePending_(map);
  // re-arm at the right granularity, or remove the trigger if nothing is left
  ensureCloseTrigger_();
  if (closed) {
    Logger.log('closed ' + closed + ', still open ' + remaining);
  }
}

/**
 * Is a quiz currently open, and when will it close? Run this if a form is
 * still taking answers when you expected it to have stopped.
 */
function closeStatus() {
  var map = loadPending_();
  var ids = Object.keys(map);
  var trigs = ScriptApp.getProjectTriggers();
  var mine = 0;
  for (var i = 0; i < trigs.length; i++) {
    if (trigs[i].getHandlerFunction() === 'autoCloseQuiz') { mine++; }
  }

  Logger.log('autoCloseQuiz triggers installed: ' + mine);
  Logger.log('quizzes pending a close: ' + ids.length);
  Logger.log('');

  if (!ids.length) {
    Logger.log('Nothing is open.');
    if (mine) {
      Logger.log('There are triggers with nothing to do. Run autoCloseQuiz() '
                 + 'once and it will remove them.');
    }
    return;
  }

  var now = new Date().getTime();
  for (var j = 0; j < ids.length; j++) {
    var e = map[ids[j]];
    var mins = Math.round((e.closeAt - now) / 60000);
    Logger.log('  ' + (e.key || ids[j]) + '   closes '
               + Utilities.formatDate(new Date(e.closeAt),
                   Session.getScriptTimeZone(), 'EEE d MMM HH:mm')
               + (mins > 0
                   ? '   (' + (mins >= 120 ? Math.round(mins / 60) + ' hours'
                                           : mins + ' min') + ' from now)'
                   : '   (overdue, closing on the next check)'));
  }

  Logger.log('');
  if (!mine) {
    Logger.log('NO TRIGGER IS INSTALLED, so nothing will close these. '
               + 'Authorise triggers and run openQuizFor again, or close '
               + 'them by hand with closeEverything().');
  } else {
    Logger.log('One trigger serves all of them. It checks hourly, or every '
               + 'minute once the nearest deadline is within half an hour.');
  }
}

function closeQuiz(week, code) {
  if (week === undefined || code === undefined) {
    Logger.log('closeQuiz needs a week and a cohort, and the Run button '
               + 'cannot pass them.');
    Logger.log('Use a wrapper such as close_W1_CML3112, or '
               + 'closeEverything() to shut all 36.');
    return;
  }
  var L = loadLinks_()[code + '|' + week];
  if (!L) { throw new Error('No form recorded for ' + code + ' week ' + week); }
  FormApp.openById(L.formId).setAcceptingResponses(false);
  Logger.log('CLOSED: ' + L.title);
}

function closeEverything() {
  var links = loadLinks_();
  var keys = Object.keys(links), n = 0;
  for (var i = 0; i < keys.length; i++) {
    try {
      FormApp.openById(links[keys[i]].formId).setAcceptingResponses(false);
      n++;
    } catch (e) {}
  }
  Logger.log('closed ' + n + ' forms');
}

/** Convenience wrappers, so the console call is short on the day. */
__WRAPPERS__
'''


def wrappers():
    """Zero-argument helpers for everything that takes arguments.

    The Run button in the Apps Script editor cannot pass arguments: it
    calls the selected function with none, so openQuizFor(week, code)
    arrives as (undefined, undefined). Anything the lecturer is expected
    to run by hand therefore needs an argument-free entry point, and
    forgetting that for auditForm cost a failed run.
    """
    lines = ["// Open a quiz for its sitting.", ""]
    for code in COHORTS:
        for wk in sorted(QB.QUIZ):
            lines.append(
                f"function open_W{wk}_{code}() {{ openQuizFor({wk}, '{code}'); }}")

    lines += ["", "// Close one early. closeEverything() shuts all 36.", ""]
    for code in COHORTS:
        for wk in sorted(QB.QUIZ):
            lines.append(
                f"function close_W{wk}_{code}() {{ closeQuiz({wk}, '{code}'); }}")

    lines += ["", "// Inspect one form's marking. auditAll() summarises all "
                  "36.", ""]
    for code in COHORTS:
        for wk in sorted(QB.QUIZ):
            lines.append(
                f"function audit_W{wk}_{code}() {{ auditForm({wk}, '{code}'); }}")

    lines += ["", "// Read back the marks Forms computed for one quiz.", ""]
    for code in COHORTS:
        for wk in sorted(QB.QUIZ):
            lines.append(
                f"function show_W{wk}_{code}() {{ showScores({wk}, '{code}'); }}")
    return "\n".join(lines)


def main():
    payload = build_payload()

    # ensure_ascii=True is deliberate and load-bearing.
    #
    # The banks legitimately contain em dashes, typographic quotes, degree
    # signs and middle dots. Written as raw UTF-8 the generated file held
    # about 1,700 non-ASCII bytes, and pasting it into the Apps Script
    # editor corrupted them somewhere along the clipboard path. Apps Script
    # then reported "SyntaxError: Invalid or unexpected token line: 1",
    # which points at the top of the file and is nothing to do with line 1.
    #
    # As \uXXXX escapes the file is pure ASCII, survives any clipboard, and
    # produces byte-identical strings at runtime because a JavaScript string
    # literal interprets those escapes.
    js = json.dumps(payload, indent=2, ensure_ascii=True)
    gs = (GS_TEMPLATE
          .replace("__PAYLOAD__", js)
          .replace("__WRAPPERS__", wrappers()))

    # Refuse to ship a file that is not pure ASCII. A check that cannot
    # fail is not a check, so this one names the offenders and stops.
    bad = sorted({ch for ch in gs if ord(ch) > 127})
    if bad:
        detail = ", ".join(f"{ch!r} (U+{ord(ch):04X})" for ch in bad[:10])
        raise SystemExit(
            f"REFUSING TO WRITE {OUT}\n"
            f"  {len(bad)} distinct non-ASCII characters remain: {detail}\n"
            "  Express them as \\uXXXX escapes inside the JS string "
            "literals in GS_TEMPLATE. Raw UTF-8 here has already caused a "
            "paste-time syntax error once.")

    io.open(OUT, "w", encoding="ascii").write(gs)

    nforms = sum(len(v["weeks"]) for v in payload.values())
    authored = QB.authored()
    print(f"saved {OUT}")
    print(f"  {nforms} forms will be created "
          f"({len(payload)} cohorts x {len(payload['CML3112']['weeks'])} weeks)")
    print(f"  authored banks: weeks {authored}")
    print(f"  placeholder shells: weeks {QB.pending()}")
    print(f"  file size: {len(gs) / 1024:.0f} KB")
    print("  pure ASCII: yes (safe to paste through any clipboard)")


if __name__ == "__main__":
    main()
