/**
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

var QUIZ_DATA = {
  "CML3112": {
    "meta": {
      "name": "Architecture + Civil Engineering",
      "day": "Tuesday"
    },
    "weeks": [
      {
        "week": 1,
        "number": 1,
        "title": "CML3112 \u00b7 Weekly Quiz 1 \u2014 What machine learning is",
        "intro": "Nothing here can be answered without reading what it shows you.\n\nHOW THIS WORKS\n\u2022 Answer it now, in the 5 minutes on the screen. That is when this is meant to be taken, while the session is still fresh.\n\u2022 The form then stays open for 24 hours and closes itself. That window is there so a dead network or a broken phone does not cost you a mark you had earned. Take it in the room if you can: by Thursday you will have forgotten the session, and the feedback will be worth less to you.\n\u2022 ONE attempt, from your signed-in Google account. You cannot reopen it or change an answer, so read each question once, properly.\n\u2022 The first box asks for your registration number. It is the number printed on your student card, and it is how the mark reaches your record.\n\u2022 Five questions, one mark each, worth 1% of your final mark.\n\u2022 Your best ten of twelve quizzes count. Missing two costs you nothing, and there are no resits.\n\u2022 When you submit, tap View score. You get a tick or a cross on each question with the feedback underneath. Your mark is the number of ticks, and the feedback on anything you got wrong is the part worth reading.\n\u2022 A question left blank scores the same as one answered wrongly, so answer all five.",
        "questions": [
          {
            "n": 1,
            "kind": "interpretation",
            "title": "In the table below, which column is the TARGET?",
            "help": "mix_id  cement  water  age_days  strength_mpa\nM-001     380     190        28          41.2\nM-002     420     185        28          46.8\nM-003     310     200        28          32.5",
            "choices": [
              {
                "text": "cement",
                "correct": false
              },
              {
                "text": "age_days",
                "correct": false
              },
              {
                "text": "strength_mpa",
                "correct": true
              },
              {
                "text": "mix_id",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. It is the quantity you want to predict, and it is the one you would not have at the moment of prediction.",
            "fbWrong": "THE ANSWER: strength_mpa. It is the quantity you want to predict, and it is the one you would not have at the moment of prediction.\n\nWhy the others are wrong. \u201ccement\u201d \u2014 That is a feature. You know it when you batch the mix, which is before you know the strength.  \u201cage_days\u201d \u2014 That is a feature, and in this table it is the same for every row, which makes it useless as well as a feature.  \u201cmix_id\u201d \u2014 That is an identifier. It labels the row and predicts nothing. Feed it to a model and the model will memorise it."
          },
          {
            "n": 2,
            "kind": "interpretation",
            "title": "You want to predict, for a mix that has not been cast yet, whether it will fall into the class 'below 25 MPa', '25 to 40 MPa' or 'above 40 MPa'. What kind of problem is this?",
            "help": "",
            "choices": [
              {
                "text": "Regression, because the underlying quantity is a number",
                "correct": false
              },
              {
                "text": "Classification, because the answer is one of a fixed set of categories",
                "correct": true
              },
              {
                "text": "Neither, because it can be written as a rule with thresholds",
                "correct": false
              },
              {
                "text": "Regression, because there are more than two possible answers",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. The answer is a label from a fixed list, so it is classification, and it is scored with a confusion matrix rather than an average error.",
            "fbWrong": "THE ANSWER: Classification, because the answer is one of a fixed set of categories. The answer is a label from a fixed list, so it is classification, and it is scored with a confusion matrix rather than an average error.\n\nWhy the others are wrong. \u201cRegression, because the underlying quantity is a number\u201d \u2014 The underlying quantity is a number, but the question asked is not. You are asked which band or class it falls into, and a band is a category. What decides this is the question you were asked rather than the quantity the sensor happens to record.  \u201cNeither, because it can be written as a rule with thresholds\u201d \u2014 If you already have the strength or the grade then yes, a rule is the right tool and there is nothing to learn. The point here is that you do not have it yet.  \u201cRegression, because there are more than two possible answers\u201d \u2014 The number of possible answers does not decide this. Classification with three classes is still classification."
          },
          {
            "n": 3,
            "kind": "diagnosis",
            "title": "A team proposes to predict the target using the list of columns below. One column makes the whole exercise meaningless. Which one, and why?",
            "help": "target:   whether the cylinder passed the 28-day test\nfeatures: cement, water, age_days,\n          strength_mpa_measured_at_28_days",
            "choices": [
              {
                "text": "water \u2014 it is already implied by the cement content",
                "correct": false
              },
              {
                "text": "None of them; the list is fine",
                "correct": false
              },
              {
                "text": "age_days \u2014 every row has the same value so it carries no information",
                "correct": false
              },
              {
                "text": "strength_mpa_measured_at_28_days \u2014 it IS the answer, recorded at the moment the answer becomes known",
                "correct": true
              }
            ],
            "fbCorrect": "Correct. Ask the timing question: at the moment I need this prediction, would I have this number? You would not. A model given it scores near-perfectly and predicts nothing in service.",
            "fbWrong": "THE ANSWER: strength_mpa_measured_at_28_days \u2014 it IS the answer, recorded at the moment the answer becomes known. Ask the timing question: at the moment I need this prediction, would I have this number? You would not. A model given it scores near-perfectly and predicts nothing in service.\n\nWhy the others are wrong. \u201cwater \u2014 it is already implied by the cement content\u201d \u2014 Water and cement are related through the mix design, but both are legitimately known before casting. Correlated features are a modelling nuisance and this one is not fatal.  \u201cNone of them; the list is fine\u201d \u2014 One of these columns is only recorded once the outcome is known. Go back and ask the timing question of each one.  \u201cage_days \u2014 every row has the same value so it carries no information\u201d \u2014 A constant column is useless, and that is worth spotting. But useless is not the same as fatal: it wastes a column rather than invalidating the result."
          },
          {
            "n": 4,
            "kind": "interpretation",
            "title": "A durability code states that a crack wider than 0.30 mm must be flagged for repair. You have the crack widths. What should you build?",
            "help": "",
            "choices": [
              {
                "text": "A regression model to predict the threshold",
                "correct": false
              },
              {
                "text": "A classifier trained on past decisions",
                "correct": false
              },
              {
                "text": "A rule with a threshold, written directly in code",
                "correct": true
              },
              {
                "text": "Either; the choice is a matter of preference",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. You have the input and you have the threshold, so there is nothing to learn. Training a model to rediscover a published limit adds error and removes the audit trail.",
            "fbWrong": "THE ANSWER: A rule with a threshold, written directly in code. You have the input and you have the threshold, so there is nothing to learn. Training a model to rediscover a published limit adds error and removes the audit trail.\n\nWhy the others are wrong. \u201cA regression model to predict the threshold\u201d \u2014 The threshold is given. There is nothing to predict about it.  \u201cA classifier trained on past decisions\u201d \u2014 It would work, and that is what makes this tempting. It would also be less accurate than the rule, harder to defend and impossible to audit against the code of practice.  \u201cEither; the choice is a matter of preference\u201d \u2014 The choice follows from whether you already have the input and the threshold. Here you have both, so the rule wins on every axis."
          },
          {
            "n": 5,
            "kind": "judgement",
            "title": "A client will only accept a system if every decision it makes can be explained line by line to a regulator. Two candidate approaches perform identically on your data. Which do you recommend, and on what grounds?",
            "help": "",
            "choices": [
              {
                "text": "The more sophisticated one, because it will generalise better",
                "correct": false
              },
              {
                "text": "Neither; tell the client the constraint is unreasonable",
                "correct": false
              },
              {
                "text": "The one whose decisions can be read out and traced, because the constraint decides it once performance is equal",
                "correct": true
              },
              {
                "text": "Whichever scored fractionally higher on the test set",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. When performance is equal the constraint is the deciding criterion, and explainability was stated as a condition of acceptance rather than a preference.",
            "fbWrong": "THE ANSWER: The one whose decisions can be read out and traced, because the constraint decides it once performance is equal. When performance is equal the constraint is the deciding criterion, and explainability was stated as a condition of acceptance rather than a preference.\n\nWhy the others are wrong. \u201cThe more sophisticated one, because it will generalise better\u201d \u2014 Sophistication does not imply generalisation, and on equal performance there is no evidence for the claim. It also ignores the constraint you were given.  \u201cNeither; tell the client the constraint is unreasonable\u201d \u2014 Regulatory explainability is a normal engineering constraint. Part of the job is delivering within it.  \u201cWhichever scored fractionally higher on the test set\u201d \u2014 A fractional difference on one test set is usually inside the noise, and Week 10 shows you how to measure that. Even a real difference would not override a stated condition of acceptance."
          }
        ]
      },
      {
        "week": 2,
        "number": 2,
        "title": "CML3112 \u00b7 Weekly Quiz 2 \u2014 Notebooks and version control",
        "intro": "Read what each question shows you. None of them can be answered without it.\n\nHOW THIS WORKS\n\u2022 Answer it now, in the 5 minutes on the screen. That is when this is meant to be taken, while the session is still fresh.\n\u2022 The form then stays open for 24 hours and closes itself. That window is there so a dead network or a broken phone does not cost you a mark you had earned. Take it in the room if you can: by Thursday you will have forgotten the session, and the feedback will be worth less to you.\n\u2022 ONE attempt, from your signed-in Google account. You cannot reopen it or change an answer, so read each question once, properly.\n\u2022 The first box asks for your registration number. It is the number printed on your student card, and it is how the mark reaches your record.\n\u2022 Five questions, one mark each, worth 1% of your final mark.\n\u2022 Your best ten of twelve quizzes count. Missing two costs you nothing, and there are no resits.\n\u2022 When you submit, tap View score. You get a tick or a cross on each question with the feedback underneath. Your mark is the number of ticks, and the feedback on anything you got wrong is the part worth reading.\n\u2022 A question left blank scores the same as one answered wrongly, so answer all five.",
        "questions": [
          {
            "n": 1,
            "kind": "interpretation",
            "title": "The numbers in the square brackets are the order the cells were actually run. The notebook now reads as shown. Why does it print 10?",
            "help": "In [1]:  readings = 40\nIn [2]:  limit = 30\nIn [5]:  readings = 55\nIn [3]:  over = readings - limit\nIn [4]:  print(over)\n         10",
            "choices": [
              {
                "text": "Python read the cells from the top of the page downwards",
                "correct": false
              },
              {
                "text": "The subtraction ran while the first value was still in memory, and the cell that replaced it ran afterwards",
                "correct": true
              },
              {
                "text": "The notebook cached the printed output and did not refresh it",
                "correct": false
              },
              {
                "text": "The variable was never given the second value at all",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. Read the bracket numbers as a timeline: 1, 2, 3, 4, then 5. The subtraction happened at step 3 on the old value, and the replacement only happened at step 5. What you see on screen is the code; what produced the 10 is the order it ran.",
            "fbWrong": "THE ANSWER: The subtraction ran while the first value was still in memory, and the cell that replaced it ran afterwards. Read the bracket numbers as a timeline: 1, 2, 3, 4, then 5. The subtraction happened at step 3 on the old value, and the replacement only happened at step 5. What you see on screen is the code; what produced the 10 is the order it ran.\n\nWhy the others are wrong. \u201cPython read the cells from the top of the page downwards\u201d \u2014 That is the assumption this question exists to break. A notebook runs cells in whatever order you click them, and the bracket numbers are the record of that order.  \u201cThe notebook cached the printed output and did not refresh it\u201d \u2014 Notebooks do keep an old output on screen after you edit a cell, but the value here was genuinely computed from the earlier number. Nothing is stale about the 10 itself.  \u201cThe variable was never given the second value at all\u201d \u2014 It was, at step 5. That is precisely why the code on screen and the number underneath it disagree."
          },
          {
            "n": 2,
            "kind": "interpretation",
            "title": "Read the two states below. What has Restart and Run All established?",
            "help": "before:  In [7]  In [3]  In [12]  In [4]  In [9]\n         (outputs on screen, run in some past order)\n\nafter:   In [1]  In [2]  In [3]   In [4]  In [5]\n         (no errors, and the same outputs as before)",
            "choices": [
              {
                "text": "That it produces those outputs from an empty memory, in page order",
                "correct": true
              },
              {
                "text": "That the notebook will run on a classmate's machine",
                "correct": false
              },
              {
                "text": "That the code is correct",
                "correct": false
              },
              {
                "text": "That the results are statistically reliable",
                "correct": false
              }
            ],
            "fbCorrect": "Correct, and that is a narrow claim worth having. The counts now run 1 to 5 in page order, which rules out the out-of-order trap and any variable that only survived because of a cell you later deleted.",
            "fbWrong": "THE ANSWER: That it produces those outputs from an empty memory, in page order. That is a narrow claim worth having. The counts now run 1 to 5 in page order, which rules out the out-of-order trap and any variable that only survived because of a cell you later deleted.\n\nWhy the others are wrong. \u201cThat the notebook will run on a classmate's machine\u201d \u2014 That needs the same packages, the same Python version and the data file reachable at the same relative path. Week 13 is about exactly this gap.  \u201cThat the code is correct\u201d \u2014 It establishes that the code runs and reproduces its own outputs. Code can run cleanly from top to bottom and still compute the wrong quantity, which is what the diagnosis questions from Week 3 onwards are about.  \u201cThat the results are statistically reliable\u201d \u2014 Reproducing an output says nothing about whether the number was worth computing. A notebook can faithfully reproduce a meaningless average every time you run it."
          },
          {
            "n": 3,
            "kind": "traceback",
            "title": "You have been working for an hour, the variable is plainly assigned in a cell further up the page, and running the cell at the bottom gives this. What is the most likely cause?",
            "help": "Traceback (most recent call last):\n  File \"<ipython-input-2-a1b2c3>\", line 1, in <module>\n    print(mean_width)\nNameError: name 'mean_width' is not defined",
            "choices": [
              {
                "text": "The name is a reserved word in Python",
                "correct": false
              },
              {
                "text": "The variable holds nothing, so printing it fails",
                "correct": false
              },
              {
                "text": "The notebook needs a library imported before it can print",
                "correct": false
              },
              {
                "text": "The cell that creates it has not actually been run in this session, whatever the page shows",
                "correct": true
              }
            ],
            "fbCorrect": "Correct. Being written on the page and having been executed are different things: the kernel only knows what it has run. Either that cell was never run, or the kernel was restarted since. Restart and Run All settles it in one step.",
            "fbWrong": "THE ANSWER: The cell that creates it has not actually been run in this session, whatever the page shows. Being written on the page and having been executed are different things: the kernel only knows what it has run. Either that cell was never run, or the kernel was restarted since. Restart and Run All settles it in one step.\n\nWhy the others are wrong. \u201cThe name is a reserved word in Python\u201d \u2014 It is an ordinary name. A reserved word would be reported as a SyntaxError while the cell was being read, before it ran.  \u201cThe variable holds nothing, so printing it fails\u201d \u2014 A variable holding nothing still exists and prints happily as None. This error says the name itself is unknown to Python.  \u201cThe notebook needs a library imported before it can print\u201d \u2014 print is built in and needs no import. A missing library reports itself as ModuleNotFoundError."
          },
          {
            "n": 4,
            "kind": "interpretation",
            "title": "Read this output. Which statement is true?",
            "help": "$ git status\nOn branch main\nChanges not staged for commit:\n        modified:   analysis.ipynb\nUntracked files:\n        data/site_inspection_log.csv",
            "choices": [
              {
                "text": "The repository is broken and needs to be created again",
                "correct": false
              },
              {
                "text": "Both files will be saved by the next commit",
                "correct": false
              },
              {
                "text": "The notebook has been committed and the CSV has been deleted",
                "correct": false
              },
              {
                "text": "The notebook is tracked and edited; the CSV was never added",
                "correct": true
              }
            ],
            "fbCorrect": "Correct. Git reports a tracked file as modified and a file it has never seen as untracked. Stage the notebook edit with git add before committing. A bare commit saves neither file here.",
            "fbWrong": "THE ANSWER: The notebook is tracked and edited; the CSV was never added. Git reports a tracked file as modified and a file it has never seen as untracked. Stage the notebook edit with git add before committing. A bare commit saves neither file here.\n\nWhy the others are wrong. \u201cThe repository is broken and needs to be created again\u201d \u2014 This is the ordinary output of a healthy repository with work in progress. It is the state you should expect to see most of the time.  \u201cBoth files will be saved by the next commit\u201d \u2014 Neither will. The notebook change is unstaged and the CSV is untracked, so a bare commit captures nothing from this list.  \u201cThe notebook has been committed and the CSV has been deleted\u201d \u2014 A committed file with no further edits does not appear in this output at all, and a deletion is reported as deleted."
          },
          {
            "n": 5,
            "kind": "judgement",
            "title": "It is twenty minutes before the session. The Python install on your laptop fails with an error you have not seen before. What is the right move?",
            "help": "",
            "choices": [
              {
                "text": "Ask for the session to be repeated later in the week",
                "correct": false
              },
              {
                "text": "Spend the session fixing the install so the rest of the semester is smooth",
                "correct": false
              },
              {
                "text": "Open Colab in the browser and work there for the session",
                "correct": true
              },
              {
                "text": "Copy a classmate's notebook afterwards and read through it",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. Colab needs a browser and nothing else, which is why this course is built on it. Your install can be repaired at a time when it is not costing you a three-hour session.",
            "fbWrong": "THE ANSWER: Open Colab in the browser and work there for the session. Colab needs a browser and nothing else, which is why this course is built on it. Your install can be repaired at a time when it is not costing you a three-hour session.\n\nWhy the others are wrong. \u201cAsk for the session to be repeated later in the week\u201d \u2014 There is no second slot: each cohort meets once a week. A working browser removes the problem in under a minute.  \u201cSpend the session fixing the install so the rest of the semester is smooth\u201d \u2014 This trades a guaranteed three hours of teaching for a repair of unknown length. Install problems are often version mismatches with no quick fix, which is why the browser route exists.  \u201cCopy a classmate's notebook afterwards and read through it\u201d \u2014 Reading someone else's finished notebook skips the part that does the teaching. You would arrive at Week 3 without having run a single cell yourself."
          }
        ]
      },
      {
        "week": 3,
        "number": 3,
        "title": "CML3112 \u00b7 Weekly Quiz 3 \u2014 Python as an engineering calculator",
        "intro": "Read what each question shows you. None of them can be answered without it.\n\nHOW THIS WORKS\n\u2022 Answer it now, in the 5 minutes on the screen. That is when this is meant to be taken, while the session is still fresh.\n\u2022 The form then stays open for 24 hours and closes itself. That window is there so a dead network or a broken phone does not cost you a mark you had earned. Take it in the room if you can: by Thursday you will have forgotten the session, and the feedback will be worth less to you.\n\u2022 ONE attempt, from your signed-in Google account. You cannot reopen it or change an answer, so read each question once, properly.\n\u2022 The first box asks for your registration number. It is the number printed on your student card, and it is how the mark reaches your record.\n\u2022 Five questions, one mark each, worth 1% of your final mark.\n\u2022 Your best ten of twelve quizzes count. Missing two costs you nothing, and there are no resits.\n\u2022 When you submit, tap View score. You get a tick or a cross on each question with the feedback underneath. Your mark is the number of ticks, and the feedback on anything you got wrong is the part worth reading.\n\u2022 A question left blank scores the same as one answered wrongly, so answer all five.",
        "questions": [
          {
            "n": 1,
            "kind": "diagnosis",
            "title": "This runs without any error and prints the number shown. What is wrong?",
            "help": "def slab_volume(length_m, width_m, thickness_m):\n    return length_m * width_m * thickness_m\n\nvolume = slab_volume(6.0, 4.0, 250)\nprint(f\"{volume:.2f} m3 of concrete\")\n\n6000.00 m3 of concrete",
            "choices": [
              {
                "text": "Nothing is wrong; 6000 m3 is a reasonable slab",
                "correct": false
              },
              {
                "text": "The thickness was passed in millimetres to a parameter measured in metres",
                "correct": true
              },
              {
                "text": "The result needs rounding to two decimal places",
                "correct": false
              },
              {
                "text": "The multiplication should have been a division somewhere",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. 250 mm is 0.25 m, and the right answer is 6.00 m3. The parameter name says thickness_m and nothing in Python enforces that. A slab 250 metres thick would be absurd on site, and that absurdity is the only thing protecting you here.",
            "fbWrong": "THE ANSWER: The thickness was passed in millimetres to a parameter measured in metres. 250 mm is 0.25 m, and the right answer is 6.00 m3. The parameter name says thickness_m and nothing in Python enforces that. A slab 250 metres thick would be absurd on site, and that absurdity is the only thing protecting you here.\n\nWhy the others are wrong. \u201cNothing is wrong; 6000 m3 is a reasonable slab\u201d \u2014 A transit mixer carries six to eight cubic metres, so 6000 m3 is around eight hundred truck loads for one slab of six metres by four. Always sanity-check the size of an answer against something physical you know.  \u201cThe result needs rounding to two decimal places\u201d \u2014 It is already formatted to two decimals. Presentation is not the problem; the magnitude is.  \u201cThe multiplication should have been a division somewhere\u201d \u2014 Volume is length times width times thickness, and that is what the function computes. The formula is right and the input is wrong."
          },
          {
            "n": 2,
            "kind": "diagnosis",
            "title": "This function runs without error. The printed answer is wrong and dangerous. Why?",
            "help": "def crack_action(width_mm, exposure):\n    if width_mm > 0.10:\n        return \"monitor\"\n    elif width_mm > 0.30:\n        return \"flag for repair\"\n    elif exposure == \"marine\" and width_mm > 0.20:\n        return \"seal now\"\n    else:\n        return \"no action\"\n\nprint(crack_action(0.45, \"marine\"))\nmonitor",
            "choices": [
              {
                "text": "The function should not take exposure as an argument",
                "correct": false
              },
              {
                "text": "The loosest test is first, so it catches the crack and the rest never run",
                "correct": true
              },
              {
                "text": "The comparisons should be greater-than-or-equal",
                "correct": false
              },
              {
                "text": "The marine condition needs to use or rather than and",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. 0.45 is above 0.10, so the first branch returns and nothing below it is ever consulted. A 0.45 mm crack in a marine exposure should return seal now. Order the branches from the most severe condition downwards.",
            "fbWrong": "THE ANSWER: The loosest test is first, so it catches the crack and the rest never run. 0.45 is above 0.10, so the first branch returns and nothing below it is ever consulted. A 0.45 mm crack in a marine exposure should return seal now. Order the branches from the most severe condition downwards.\n\nWhy the others are wrong. \u201cThe function should not take exposure as an argument\u201d \u2014 Exposure is exactly what makes 0.45 mm urgent rather than routine. Removing it would lose the most important part of the rule.  \u201cThe comparisons should be greater-than-or-equal\u201d \u2014 At 0.45 mm none of these boundaries is touched exactly, so that change would not alter this answer. The ordering is what decides it.  \u201cThe marine condition needs to use or rather than and\u201d \u2014 The marine rule genuinely requires both a marine exposure and a width above 0.20, so and is right. The branch is correct and simply never reached."
          },
          {
            "n": 3,
            "kind": "traceback",
            "title": "What does this tell you about the variable?",
            "help": "Traceback (most recent call last):\n  File \"<ipython-input-5-9f8e7d>\", line 2, in <module>\n    total_span = span + 2.5\nTypeError: can only concatenate str (not \"float\") to str",
            "choices": [
              {
                "text": "The 2.5 should have been written as an integer",
                "correct": false
              },
              {
                "text": "It holds text, so the plus sign was read as joining strings and a number cannot be joined to text",
                "correct": true
              },
              {
                "text": "The variable was never assigned a value",
                "correct": false
              },
              {
                "text": "It holds a number that is too large for the addition",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. The word concatenate is the clue: Python was trying to stick things together rather than add them. Values typed in or read from a file arrive as text, and float() converts them.",
            "fbWrong": "THE ANSWER: It holds text, so the plus sign was read as joining strings and a number cannot be joined to text. The word concatenate is the clue: Python was trying to stick things together rather than add them. Values typed in or read from a file arrive as text, and float() converts them.\n\nWhy the others are wrong. \u201cThe 2.5 should have been written as an integer\u201d \u2014 Adding an integer to text fails in exactly the same way. The type of the variable is what has to change.  \u201cThe variable was never assigned a value\u201d \u2014 That reports itself as a NameError. This variable exists and holds something; the something is text.  \u201cIt holds a number that is too large for the addition\u201d \u2014 Python integers grow as large as memory allows, and floats would report an overflow differently. The message names the type as str."
          },
          {
            "n": 4,
            "kind": "interpretation",
            "title": "Reading this function as written, what does the call return?",
            "help": "def crack_action(width_mm, exposure):\n    if exposure == \"marine\" and width_mm > 0.20:\n        return \"seal now\"\n    elif width_mm > 0.30:\n        return \"flag for repair\"\n    elif width_mm > 0.10:\n        return \"monitor\"\n    else:\n        return \"no action\"\n\ncrack_action(0.25, \"marine\")",
            "choices": [
              {
                "text": "flag for repair",
                "correct": false
              },
              {
                "text": "no action",
                "correct": false
              },
              {
                "text": "monitor",
                "correct": false
              },
              {
                "text": "seal now",
                "correct": true
              }
            ],
            "fbCorrect": "Correct. The exposure is marine and 0.25 is above 0.20, so the first branch matches and returns immediately. The 0.30 mm limit is never consulted.",
            "fbWrong": "THE ANSWER: seal now. The exposure is marine and 0.25 is above 0.20, so the first branch matches and returns immediately. The 0.30 mm limit is never consulted.\n\nWhy the others are wrong. \u201cflag for repair\u201d \u2014 That branch needs a width above 0.30. This crack is 0.25 mm.  \u201cno action\u201d \u2014 The final branch is only reached when every test above it fails. Two of them match here.  \u201cmonitor\u201d \u2014 That is what you get by reading only the width and skipping the marine branch above it. In a marine exposure the threshold that matters is 0.20."
          },
          {
            "n": 5,
            "kind": "judgement",
            "title": "A teammate has written the 0.30 mm action limit directly into three different cells. The code works. What should you do?",
            "help": "",
            "choices": [
              {
                "text": "Put it in one named constant and refer to that everywhere",
                "correct": true
              },
              {
                "text": "Ask each teammate to remember which cells contain it",
                "correct": false
              },
              {
                "text": "Leave it, because the code produces the right answers today",
                "correct": false
              },
              {
                "text": "Write a function that looks the limit up online each time",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. When the standard is revised you change one line and can point to it. Three copies means three chances to update two of them and ship a notebook that applies two different limits in the same analysis.",
            "fbWrong": "THE ANSWER: Put it in one named constant and refer to that everywhere. When the standard is revised you change one line and can point to it. Three copies means three chances to update two of them and ship a notebook that applies two different limits in the same analysis.\n\nWhy the others are wrong. \u201cAsk each teammate to remember which cells contain it\u201d \u2014 Relying on memory across a fifteen-week project with several people is how the two-out-of-three update happens.  \u201cLeave it, because the code produces the right answers today\u201d \u2014 It does work today. The cost arrives on the day the figure changes, and it arrives as an inconsistency nobody notices because every cell still runs.  \u201cWrite a function that looks the limit up online each time\u201d \u2014 That makes the notebook depend on a network and on somebody else's page layout. A named constant with a comment citing the clause is auditable and works offline."
          }
        ]
      },
      {
        "week": 4,
        "number": 4,
        "title": "CML3112 \u00b7 Weekly Quiz 4 \u2014 Collections, loops and files",
        "intro": "Read what each question shows you. None of them can be answered without it.\n\nHOW THIS WORKS\n\u2022 Answer it now, in the 5 minutes on the screen. That is when this is meant to be taken, while the session is still fresh.\n\u2022 The form then stays open for 24 hours and closes itself. That window is there so a dead network or a broken phone does not cost you a mark you had earned. Take it in the room if you can: by Thursday you will have forgotten the session, and the feedback will be worth less to you.\n\u2022 ONE attempt, from your signed-in Google account. You cannot reopen it or change an answer, so read each question once, properly.\n\u2022 The first box asks for your registration number. It is the number printed on your student card, and it is how the mark reaches your record.\n\u2022 Five questions, one mark each, worth 1% of your final mark.\n\u2022 Your best ten of twelve quizzes count. Missing two costs you nothing, and there are no resits.\n\u2022 When you submit, tap View score. You get a tick or a cross on each question with the feedback underneath. Your mark is the number of ticks, and the feedback on anything you got wrong is the part worth reading.\n\u2022 A question left blank scores the same as one answered wrongly, so answer all five.",
        "questions": [
          {
            "n": 1,
            "kind": "diagnosis",
            "title": "This runs cleanly and prints the mean shown. The mean is wrong. What causes it?",
            "help": "widths = [0.12, 0.35, 0.41, 0.08]\ntotal = 0.0\nfor w in widths:\n    total = 0.0\n    total = total + w\n\nprint(f\"mean width {total / len(widths):.3f} mm\")\nmean width 0.020 mm",
            "choices": [
              {
                "text": "The list should have been a dictionary",
                "correct": false
              },
              {
                "text": "The reset to zero sits inside the loop, so only the last value survives",
                "correct": true
              },
              {
                "text": "The division should use the number of readings above the limit",
                "correct": false
              },
              {
                "text": "Adding floats accumulates rounding error",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. Every pass throws away the running total, so the loop leaves 0.08 behind and 0.08 divided by 4 is 0.020. The true mean is 0.240 mm. Move the reset above the loop.",
            "fbWrong": "THE ANSWER: The reset to zero sits inside the loop, so only the last value survives. Every pass throws away the running total, so the loop leaves 0.08 behind and 0.08 divided by 4 is 0.020. The true mean is 0.240 mm. Move the reset above the loop.\n\nWhy the others are wrong. \u201cThe list should have been a dictionary\u201d \u2014 A list of readings is the right structure for a mean. The fault is one misplaced line.  \u201cThe division should use the number of readings above the limit\u201d \u2014 A mean over all readings divides by all of them, so len(widths) is right. The numerator is what has been destroyed.  \u201cAdding floats accumulates rounding error\u201d \u2014 Float rounding here would show up somewhere past the third decimal. This answer is out by a factor of twelve."
          },
          {
            "n": 2,
            "kind": "diagnosis",
            "title": "This prints a count that is one too low on this file. Why?",
            "help": "widths = [0.44, 0.35, 0.41, 0.08]\nLIMIT = 0.30\nover = 0\nfor i in range(1, len(widths)):\n    if widths[i] > LIMIT:\n        over = over + 1\n\nprint(f\"{over} readings above the limit\")\n2 readings above the limit",
            "choices": [
              {
                "text": "The range starts at 1, so the first reading is never tested",
                "correct": true
              },
              {
                "text": "The range stops one short of the end of the list",
                "correct": false
              },
              {
                "text": "The comparison should be greater-than-or-equal",
                "correct": false
              },
              {
                "text": "The counter should start at 1",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. Python indexes from 0, so range(1, 4) visits positions 1, 2 and 3 and skips 0.44 entirely. Three readings exceed 0.30. Use range(len(widths)), or better, loop over the values directly.",
            "fbWrong": "THE ANSWER: The range starts at 1, so the first reading is never tested. Python indexes from 0, so range(1, 4) visits positions 1, 2 and 3 and skips 0.44 entirely. Three readings exceed 0.30. Use range(len(widths)), or better, loop over the values directly.\n\nWhy the others are wrong. \u201cThe range stops one short of the end of the list\u201d \u2014 range(1, 4) does reach position 3, which is the last of four. The miss is at the start.  \u201cThe comparison should be greater-than-or-equal\u201d \u2014 No reading here sits exactly on 0.30, so that change would not alter the count.  \u201cThe counter should start at 1\u201d \u2014 A count of things starts at nothing. Starting at 1 would hide this bug behind a second one and give the right answer for the wrong reason."
          },
          {
            "n": 3,
            "kind": "traceback",
            "title": "You are reading a 300-row file and it stops partway through with this. What has happened, and what should the loop do about it?",
            "help": "Traceback (most recent call last):\n  File \"<ipython-input-7-4c5d6e>\", line 4, in <module>\n    if float(row[\"crack_width_mm\"]) > LIMIT:\nValueError: could not convert string to float: ''",
            "choices": [
              {
                "text": "The column name is spelled wrongly",
                "correct": false
              },
              {
                "text": "The whole file is corrupted and cannot be used",
                "correct": false
              },
              {
                "text": "The empty value should be replaced with zero so the loop can continue",
                "correct": false
              },
              {
                "text": "That field is empty in one row, so the loop should skip that row and count how many it skipped",
                "correct": true
              }
            ],
            "fbCorrect": "Correct. The two quote marks with nothing between them are an empty string. Skipping is the right response and the count of skips belongs in your report, because it tells the reader how much of the file the answer actually covers.",
            "fbWrong": "THE ANSWER: That field is empty in one row, so the loop should skip that row and count how many it skipped. The two quote marks with nothing between them are an empty string. Skipping is the right response and the count of skips belongs in your report, because it tells the reader how much of the file the answer actually covers.\n\nWhy the others are wrong. \u201cThe column name is spelled wrongly\u201d \u2014 A wrong column name raises a KeyError before any conversion is attempted. The column was found; its content was empty.  \u201cThe whole file is corrupted and cannot be used\u201d \u2014 One blank field in one row says nothing about the other 299. Handle the gap and carry on.  \u201cThe empty value should be replaced with zero so the loop can continue\u201d \u2014 This is the trap. Zero is a real measurement, so substituting it silently drags every average downwards. Week 6 is largely about the damage this does."
          },
          {
            "n": 4,
            "kind": "interpretation",
            "title": "Your script prints this summary. Which statement does it support?",
            "help": "rows in file      300\nrows used         287\nrows skipped       13\nmean crack width 0.21 mm",
            "choices": [
              {
                "text": "The 13 skipped rows were duplicates",
                "correct": false
              },
              {
                "text": "The mean describes all 300 rows in the file",
                "correct": false
              },
              {
                "text": "The mean describes the 287 usable rows, and the other 13 need explaining",
                "correct": true
              },
              {
                "text": "Losing 13 rows out of 300 is too small to mention",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. A mean is only ever a mean of what went into it. If the 13 gaps are scattered at random the figure is probably fine; if they share a cause the figure is biased and the count is your only warning.",
            "fbWrong": "THE ANSWER: The mean describes the 287 usable rows, and the other 13 need explaining. A mean is only ever a mean of what went into it. If the 13 gaps are scattered at random the figure is probably fine; if they share a cause the figure is biased and the count is your only warning.\n\nWhy the others are wrong. \u201cThe 13 skipped rows were duplicates\u201d \u2014 The summary says they were skipped and does not say why. Duplicates are a separate problem, and one you meet in Week 6.  \u201cThe mean describes all 300 rows in the file\u201d \u2014 Thirteen rows contributed nothing to it. Reporting it as a figure for the file overstates what you measured.  \u201cLosing 13 rows out of 300 is too small to mention\u201d \u2014 The size of the loss is not what matters; the reason is. Thirteen gaps from one source can move a mean further than fifty scattered at random."
          },
          {
            "n": 5,
            "kind": "judgement",
            "title": "You look at the 13 skipped rows and every one of them comes from the same inspector. What should you do before reporting the mean?",
            "help": "",
            "choices": [
              {
                "text": "Fill the gaps with that source's own average so no rows are lost",
                "correct": false
              },
              {
                "text": "Drop that source entirely and report the rest",
                "correct": false
              },
              {
                "text": "Report the mean and mention the 13 skips in a footnote",
                "correct": false
              },
              {
                "text": "Investigate the shared cause first, because gaps that cluster in one source point at how the data was collected",
                "correct": true
              }
            ],
            "fbCorrect": "Correct. Thirteen blanks spread across the file is untidiness. Thirteen blanks from one source is a finding, and it may matter more than the mean you were asked for.",
            "fbWrong": "THE ANSWER: Investigate the shared cause first, because gaps that cluster in one source point at how the data was collected. Thirteen blanks spread across the file is untidiness. Thirteen blanks from one source is a finding, and it may matter more than the mean you were asked for.\n\nWhy the others are wrong. \u201cFill the gaps with that source's own average so no rows are lost\u201d \u2014 That invents readings from the one source you have reason to distrust, and it hides the pattern you just found.  \u201cDrop that source entirely and report the rest\u201d \u2014 That might end up being right, and it is a decision to take after you understand the cause. Removing a source before knowing why it failed can delete the very thing under investigation.  \u201cReport the mean and mention the 13 skips in a footnote\u201d \u2014 Reporting the count is necessary and it is not sufficient here. A footnote presents a systematic gap as though it were random noise."
          }
        ]
      },
      {
        "week": 5,
        "number": 5,
        "title": "CML3112 \u00b7 Weekly Quiz 5 \u2014 pandas, and judging a dataset",
        "intro": "Read what each question shows you. None of them can be answered without it.\n\nHOW THIS WORKS\n\u2022 Answer it now, in the 5 minutes on the screen. That is when this is meant to be taken, while the session is still fresh.\n\u2022 The form then stays open for 24 hours and closes itself. That window is there so a dead network or a broken phone does not cost you a mark you had earned. Take it in the room if you can: by Thursday you will have forgotten the session, and the feedback will be worth less to you.\n\u2022 ONE attempt, from your signed-in Google account. You cannot reopen it or change an answer, so read each question once, properly.\n\u2022 The first box asks for your registration number. It is the number printed on your student card, and it is how the mark reaches your record.\n\u2022 Five questions, one mark each, worth 1% of your final mark.\n\u2022 Your best ten of twelve quizzes count. Missing two costs you nothing, and there are no resits.\n\u2022 When you submit, tap View score. You get a tick or a cross on each question with the feedback underneath. Your mark is the number of ticks, and the feedback on anything you got wrong is the part worth reading.\n\u2022 A question left blank scores the same as one answered wrongly, so answer all five.",
        "questions": [
          {
            "n": 1,
            "kind": "diagnosis",
            "title": "You wanted the number of records above the threshold. This prints the whole row count instead. Why?",
            "help": "mask = df[\"strength\"] > 40\nprint(len(mask))\n1030\nprint(mask.sum())\n289",
            "choices": [
              {
                "text": "The threshold is too low, so every row qualifies",
                "correct": false
              },
              {
                "text": "The mask holds one True or False per row, so its length is the row count",
                "correct": true
              },
              {
                "text": "len() does not work on pandas objects",
                "correct": false
              },
              {
                "text": "The comparison was written the wrong way round",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. A comparison on a column answers the question for every row and hands back all the answers, so it is always as long as the frame. mask.sum() counts the True entries, as the second line shows, and len(df[mask]) counts the rows you keep.",
            "fbWrong": "THE ANSWER: The mask holds one True or False per row, so its length is the row count. A comparison on a column answers the question for every row and hands back all the answers, so it is always as long as the frame. mask.sum() counts the True entries, as the second line shows, and len(df[mask]) counts the rows you keep.\n\nWhy the others are wrong. \u201cThe threshold is too low, so every row qualifies\u201d \u2014 The second line rules this out: the sum is well below the row count, so most rows do not qualify. Notice also that the length would have been the row count either way, which is what makes it the wrong thing to measure.  \u201clen() does not work on pandas objects\u201d \u2014 It works and it reported the truth. The truth it reported answers a different question from the one you asked.  \u201cThe comparison was written the wrong way round\u201d \u2014 Reversing it would produce a different set of True entries and the same length. Length is the wrong measurement to be taking."
          },
          {
            "n": 2,
            "kind": "diagnosis",
            "title": "The maximum below is far too small and no error was raised. What has happened?",
            "help": "print(df[\"strength\"].dtype)\nobject\n\nprint(df[\"strength\"].max())\n9.9\n\n# the file contains values such as 32.5, 41.2, 9.9, 28.0",
            "choices": [
              {
                "text": "max() needs the column sorted first",
                "correct": false
              },
              {
                "text": "The column holds text, so the maximum was decided alphabetically and a value starting with 9 wins",
                "correct": true
              },
              {
                "text": "The column contains missing values that max() skipped",
                "correct": false
              },
              {
                "text": "The largest values are stored in a different column",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. object dtype means the column is text. Compared as text, \"9.9\" beats \"41.2\" because the character 9 comes after 4. Convert with pd.to_numeric and the real maximum appears. One stray value with a unit or a stray space is usually what forced the whole column to text.",
            "fbWrong": "THE ANSWER: The column holds text, so the maximum was decided alphabetically and a value starting with 9 wins. Object dtype means the column is text. Compared as text, \"9.9\" beats \"41.2\" because the character 9 comes after 4. Convert with pd.to_numeric and the real maximum appears. One stray value with a unit or a stray space is usually what forced the whole column to text.\n\nWhy the others are wrong. \u201cmax() needs the column sorted first\u201d \u2014 max() never needs sorting. It compared correctly by the rules for text, which are the wrong rules for measurements.  \u201cThe column contains missing values that max() skipped\u201d \u2014 max() does skip missing values, and skipping them cannot produce a maximum below most of the data. The ordering itself is what has gone wrong.  \u201cThe largest values are stored in a different column\u201d \u2014 The comment shows the values are in this column. The problem is how they are being compared."
          },
          {
            "n": 3,
            "kind": "traceback",
            "title": "What is the first thing to check?",
            "help": "Traceback (most recent call last):\n  File \"<ipython-input-4-7a8b9c>\", line 1, in <module>\n    df[\"strength_mpa\"].mean()\nKeyError: 'strength_mpa'",
            "choices": [
              {
                "text": "Print df.columns and compare the exact spelling, case and any stray spaces",
                "correct": true
              },
              {
                "text": "Whether the file loaded at all",
                "correct": false
              },
              {
                "text": "Whether the column contains missing values",
                "correct": false
              },
              {
                "text": "Whether mean() works on that data type",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. A KeyError on a frame means no column carries that exact label. Trailing spaces from a spreadsheet export are a common cause and they are invisible until you print the list.",
            "fbWrong": "THE ANSWER: Print df.columns and compare the exact spelling, case and any stray spaces. A KeyError on a frame means no column carries that exact label. Trailing spaces from a spreadsheet export are a common cause and they are invisible until you print the list.\n\nWhy the others are wrong. \u201cWhether the file loaded at all\u201d \u2014 That is worth confirming, and a frame that failed to load would raise on the read or on len(df) first. The message names one specific label.  \u201cWhether the column contains missing values\u201d \u2014 Missing values inside a column never stop you selecting it. This error happened before any value was read.  \u201cWhether mean() works on that data type\u201d \u2014 The error came from the selection, before mean() was reached. A type problem would name the type."
          },
          {
            "n": 4,
            "kind": "interpretation",
            "title": "What does this shape tell you?",
            "help": "g = df.groupby(\"age_band\")[\"strength\"].mean()\nprint(g.shape)\n(4,)",
            "choices": [
              {
                "text": "Four rows had a missing value in the grouping column",
                "correct": false
              },
              {
                "text": "Four rows of the original data survived the operation",
                "correct": false
              },
              {
                "text": "There are four groups, and the result holds one mean for each of them",
                "correct": true
              },
              {
                "text": "The result has four columns",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. Grouping collapses the frame to one row per group, so the length of the result is the number of distinct values in the grouping column. The original frame is untouched.",
            "fbWrong": "THE ANSWER: There are four groups, and the result holds one mean for each of them. Grouping collapses the frame to one row per group, so the length of the result is the number of distinct values in the grouping column. The original frame is untouched.\n\nWhy the others are wrong. \u201cFour rows had a missing value in the grouping column\u201d \u2014 Rows with a missing group label are left out of the result rather than counted into it, and that would not set the length to four.  \u201cFour rows of the original data survived the operation\u201d \u2014 Grouping summarises rows rather than removing them. Every row contributed to one of the four means.  \u201cThe result has four columns\u201d \u2014 A shape written with one number describes one dimension. Four columns would appear as a second number."
          },
          {
            "n": 5,
            "kind": "judgement",
            "title": "A colleague sends you concrete_strength.csv as an email attachment with no other information, and you are asked to quote the mean strength in a report. What do you do first?",
            "help": "",
            "choices": [
              {
                "text": "Establish where the file came from, what licence it carries and how many rows it holds, and record all three alongside the figure",
                "correct": true
              },
              {
                "text": "Compute the mean and quote it, since the file is the data you were given",
                "correct": false
              },
              {
                "text": "Compare it against a published dataset and use whichever looks cleaner",
                "correct": false
              },
              {
                "text": "Ask for the file in a different format to be safe",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. A number in a report is only as defensible as the file behind it. Source, licence, date and row count are the minimum you need to be able to answer the question every reader eventually asks, which is where this came from.",
            "fbWrong": "THE ANSWER: Establish where the file came from, what licence it carries and how many rows it holds, and record all three alongside the figure. A number in a report is only as defensible as the file behind it. Source, licence, date and row count are the minimum you need to be able to answer the question every reader eventually asks, which is where this came from.\n\nWhy the others are wrong. \u201cCompute the mean and quote it, since the file is the data you were given\u201d \u2014 The arithmetic is the easy part and the least of your obligations. A figure whose origin you cannot state is one you cannot defend when it is challenged.  \u201cCompare it against a published dataset and use whichever looks cleaner\u201d \u2014 Choosing data by how tidy it looks selects for convenience over relevance. Find out what this file is before reaching for another one.  \u201cAsk for the file in a different format to be safe\u201d \u2014 The format is not the risk. An unsourced spreadsheet is exactly as unsourced after conversion."
          }
        ]
      },
      {
        "week": 6,
        "number": 6,
        "title": "CML3112 \u00b7 Weekly Quiz 6 \u2014 Dirty data, and seeing it",
        "intro": "Read what each question shows you. None of them can be answered without it.\n\nHOW THIS WORKS\n\u2022 Answer it now, in the 5 minutes on the screen. That is when this is meant to be taken, while the session is still fresh.\n\u2022 The form then stays open for 24 hours and closes itself. That window is there so a dead network or a broken phone does not cost you a mark you had earned. Take it in the room if you can: by Thursday you will have forgotten the session, and the feedback will be worth less to you.\n\u2022 ONE attempt, from your signed-in Google account. You cannot reopen it or change an answer, so read each question once, properly.\n\u2022 The first box asks for your registration number. It is the number printed on your student card, and it is how the mark reaches your record.\n\u2022 Five questions, one mark each, worth 1% of your final mark.\n\u2022 Your best ten of twelve quizzes count. Missing two costs you nothing, and there are no resits.\n\u2022 When you submit, tap View score. You get a tick or a cross on each question with the feedback underneath. Your mark is the number of ticks, and the feedback on anything you got wrong is the part worth reading.\n\u2022 A question left blank scores the same as one answered wrongly, so answer all five.",
        "questions": [
          {
            "n": 1,
            "kind": "diagnosis",
            "title": "The mean below is lower than every real reading in the list. What went wrong?",
            "help": "# the survey tool writes 0 when the area field is left blank\nfloor_area = [120, 0, 95, 110]\nprint(f\"mean {sum(floor_area) / len(floor_area):.2f} m2\")\nmean 81.25 m2",
            "choices": [
              {
                "text": "The division should exclude the last value",
                "correct": false
              },
              {
                "text": "The list is too short for a mean to be meaningful",
                "correct": false
              },
              {
                "text": "One entry is a zero standing in for a missing area",
                "correct": true
              },
              {
                "text": "A floor area of zero is possible for an unbuilt unit",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. A zero-coded gap is the most dangerous kind, because zero is a legal number and nothing looks wrong. The mean of the three real areas is 108.33 m2. Convert these zeros to missing values first.",
            "fbWrong": "THE ANSWER: One entry is a zero standing in for a missing area. A zero-coded gap is the most dangerous kind, because zero is a legal number and nothing looks wrong. The mean of the three real areas is 108.33 m2. Convert these zeros to missing values first.\n\nWhy the others are wrong. \u201cThe division should exclude the last value\u201d \u2014 The position of the offending entry is incidental. Treating a placeholder as data is the fault.  \u201cThe list is too short for a mean to be meaningful\u201d \u2014 Three real values give a usable mean. A fourth entry that is not a measurement is what moved it.  \u201cA floor area of zero is possible for an unbuilt unit\u201d \u2014 The comment settles it: this tool writes 0 for a blank field, so this zero records an absence of data rather than an absence of floor. Without that comment the option would be arguable, which is why a column like this needs its coding documented before you touch it."
          },
          {
            "n": 2,
            "kind": "diagnosis",
            "title": "This runs with no error and no warning. What has it done to your data?",
            "help": "# one strength was typed as \"32.5 MPa\" instead of 32.5\ndf[\"strength\"] = pd.to_numeric(df[\"strength\"],\n                                 errors=\"coerce\")\nprint(df[\"strength\"].mean())",
            "choices": [
              {
                "text": "It replaced the unreadable value with the column mean",
                "correct": false
              },
              {
                "text": "It stripped the unit and kept the number",
                "correct": false
              },
              {
                "text": "It raised the error but carried on to the next row",
                "correct": false
              },
              {
                "text": "It turned every unreadable value into a missing value, and the mean then quietly skipped those rows",
                "correct": true
              }
            ],
            "fbCorrect": "Correct. Coercing is often the right move and it is never free: it converts a loud failure into a silent one. Count the missing values it created and report that count, otherwise your mean covers fewer rows than you believe.",
            "fbWrong": "THE ANSWER: It turned every unreadable value into a missing value, and the mean then quietly skipped those rows. Coercing is often the right move and it is never free: it converts a loud failure into a silent one. Count the missing values it created and report that count, otherwise your mean covers fewer rows than you believe.\n\nWhy the others are wrong. \u201cIt replaced the unreadable value with the column mean\u201d \u2014 No substitution happens. Filling gaps is a separate decision you have to make deliberately, and doing it before a split leaks information, as Week 10 shows.  \u201cIt stripped the unit and kept the number\u201d \u2014 Nothing here parses units. A value with a unit attached is unreadable as a number and becomes missing.  \u201cIt raised the error but carried on to the next row\u201d \u2014 That is what errors=\"raise\" would do, minus the carrying on. Coercing suppresses the error entirely."
          },
          {
            "n": 3,
            "kind": "traceback",
            "title": "You convert the column without coercing and get this. What is the useful thing about this message?",
            "help": "Traceback (most recent call last):\n  File \"<ipython-input-6-2b3c4d>\", line 1, in <module>\n    df[\"strength\"] = pd.to_numeric(df[\"strength\"])\nValueError: Unable to parse string \"32.5 MPa\" at position 417",
            "choices": [
              {
                "text": "It means the column is the wrong data type for pandas",
                "correct": false
              },
              {
                "text": "It proves the column cannot be converted",
                "correct": false
              },
              {
                "text": "It should be suppressed so the analysis can continue",
                "correct": false
              },
              {
                "text": "It names the offending value and the row it sits in, so you can look at it and decide what it should be",
                "correct": true
              }
            ],
            "fbCorrect": "Correct. This is more useful than a silent conversion, because it hands you the exact value and position. Look at row 417, decide whether to repair the entry or drop it, and write down which you chose.",
            "fbWrong": "THE ANSWER: It names the offending value and the row it sits in, so you can look at it and decide what it should be. This is more useful than a silent conversion, because it hands you the exact value and position. Look at row 417, decide whether to repair the entry or drop it, and write down which you chose.\n\nWhy the others are wrong. \u201cIt means the column is the wrong data type for pandas\u201d \u2014 The column is text because of this value. Conversion is the cure and the message is telling you what stands in the way.  \u201cIt proves the column cannot be converted\u201d \u2014 It proves one value cannot. Fix or remove that value and the column converts.  \u201cIt should be suppressed so the analysis can continue\u201d \u2014 Suppressing it is available and it costs you the position and the value. Read the message first, then decide."
          },
          {
            "n": 4,
            "kind": "interpretation",
            "title": "Read the question you set yourself against the chart you produced. Does the chart answer it?",
            "help": "question:  Does mean strength differ between mixes\n           with and without fly ash?\n\nchart:     one histogram\n           x = compressive strength (MPa)\n           y = number of mixes\n           all 1,030 mixes, no grouping applied",
            "choices": [
              {
                "text": "Yes, because the shape of the distribution reveals the two groups",
                "correct": false
              },
              {
                "text": "No, because a histogram is never the right chart",
                "correct": false
              },
              {
                "text": "No, because the two groups are mixed together in one distribution and cannot be compared",
                "correct": true
              },
              {
                "text": "Yes, provided the sample is large enough",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. The question asks for a comparison, so the chart has to separate the groups: two distributions side by side, or a mean for each with its spread. A single pooled histogram cannot show a difference between halves it never divided.",
            "fbWrong": "THE ANSWER: No, because the two groups are mixed together in one distribution and cannot be compared. The question asks for a comparison, so the chart has to separate the groups: two distributions side by side, or a mean for each with its spread. A single pooled histogram cannot show a difference between halves it never divided.\n\nWhy the others are wrong. \u201cYes, because the shape of the distribution reveals the two groups\u201d \u2014 Two clear humps would hint at something and would not tell you which group each hump belongs to. A distribution with one hump can still hide a real difference between the groups.  \u201cNo, because a histogram is never the right chart\u201d \u2014 A histogram is a good way to show one distribution. The fault is the missing split rather than the choice of chart type.  \u201cYes, provided the sample is large enough\u201d \u2014 Sample size cannot rescue a chart that never made the comparison. Twenty thousand pooled records answer the question no better than two hundred."
          },
          {
            "n": 5,
            "kind": "judgement",
            "title": "You find a 28-day compressive strength of 91 MPa in a file where most mixes sit between 20 and 50 MPa. What do you do with it?",
            "help": "",
            "choices": [
              {
                "text": "Replace it with the mean of the column",
                "correct": false
              },
              {
                "text": "Keep it and check the mix design",
                "correct": true
              },
              {
                "text": "Cap it at the highest ordinary value so it stops distorting the mean",
                "correct": false
              },
              {
                "text": "Delete it, because it is far outside the normal range",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. 91 MPa is unusual and entirely possible for a high-performance mix. Verify it against the mix design and the test record, and keep it. An extreme value is a question to answer rather than a row to delete.",
            "fbWrong": "THE ANSWER: Keep it and check the mix design. 91 MPa is unusual and entirely possible for a high-performance mix. Verify it against the mix design and the test record, and keep it. An extreme value is a question to answer rather than a row to delete.\n\nWhy the others are wrong. \u201cReplace it with the mean of the column\u201d \u2014 That substitutes an invented average for a real result and makes the data look tidier than the world it came from.  \u201cCap it at the highest ordinary value so it stops distorting the mean\u201d \u2014 Capping fabricates a measurement that was never taken and hides the very behaviour you might be trying to predict.  \u201cDelete it, because it is far outside the normal range\u201d \u2014 Distance from the mean is not evidence of error. Deleting real high-strength mixes teaches your model that such mixes do not exist."
          }
        ]
      },
      {
        "week": 8,
        "number": 7,
        "title": "CML3112 \u00b7 Weekly Quiz 7 \u2014 Learning from data: the first model",
        "intro": "Read what each question shows you. None of them can be answered without it.\n\nHOW THIS WORKS\n\u2022 Answer it now, in the 5 minutes on the screen. That is when this is meant to be taken, while the session is still fresh.\n\u2022 The form then stays open for 24 hours and closes itself. That window is there so a dead network or a broken phone does not cost you a mark you had earned. Take it in the room if you can: by Thursday you will have forgotten the session, and the feedback will be worth less to you.\n\u2022 ONE attempt, from your signed-in Google account. You cannot reopen it or change an answer, so read each question once, properly.\n\u2022 The first box asks for your registration number. It is the number printed on your student card, and it is how the mark reaches your record.\n\u2022 Five questions, one mark each, worth 1% of your final mark.\n\u2022 Your best ten of twelve quizzes count. Missing two costs you nothing, and there are no resits.\n\u2022 When you submit, tap View score. You get a tick or a cross on each question with the feedback underneath. Your mark is the number of ticks, and the feedback on anything you got wrong is the part worth reading.\n\u2022 A question left blank scores the same as one answered wrongly, so answer all five.",
        "questions": [
          {
            "n": 1,
            "kind": "diagnosis",
            "title": "A teammate reports this as the accuracy of the model. What does the number actually describe?",
            "help": "model.fit(X, y)\nprint(model.score(X, y))\n0.91",
            "choices": [
              {
                "text": "How well the model reproduces the rows it was fitted on, which tells you nothing about a new case",
                "correct": true
              },
              {
                "text": "Nothing useful, because score() is the wrong function",
                "correct": false
              },
              {
                "text": "How well the model will do on new data, give or take a little",
                "correct": false
              },
              {
                "text": "The proportion of the data used for training",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. The same rows appear in fit and in score, so the model is being marked on the answers it was shown. Hold rows back with train_test_split and score on those.",
            "fbWrong": "THE ANSWER: How well the model reproduces the rows it was fitted on, which tells you nothing about a new case. The same rows appear in fit and in score, so the model is being marked on the answers it was shown. Hold rows back with train_test_split and score on those.\n\nWhy the others are wrong. \u201cNothing useful, because score() is the wrong function\u201d \u2014 score() is the right function used on the wrong rows. Give it held-out data and the number becomes meaningful.  \u201cHow well the model will do on new data, give or take a little\u201d \u2014 There is no basis for that reading. A model with enough freedom can score near one on its training rows and fail completely on anything new, which is the whole subject of Week 10.  \u201cThe proportion of the data used for training\u201d \u2014 score() returns a measure of fit. The train and test proportions are whatever you chose when you split, and here nothing was split."
          },
          {
            "n": 2,
            "kind": "diagnosis",
            "title": "This predicts a plausible-looking value and raises no error, and the value is wrong. Why?",
            "help": "feats = [\"cement\", \"water\", \"age\"]\nmodel.fit(df[feats], df[\"strength\"])\n\n# a new mix: 380 kg/m3 cement, 190 kg/m3 water, 28 days\nprint(model.predict([[190, 380, 28]]))",
            "choices": [
              {
                "text": "The new values should have been scaled first",
                "correct": false
              },
              {
                "text": "The model was fitted on too few features to predict anything",
                "correct": false
              },
              {
                "text": "predict() needs a two-dimensional input",
                "correct": false
              },
              {
                "text": "The values were supplied in a different order from the fitted columns",
                "correct": true
              }
            ],
            "fbCorrect": "Correct. A fitted model knows only that its first input is whatever its first training column was. Swap two and it happily applies the wrong coefficient to each. Build the row as a frame with named columns and this class of error disappears.",
            "fbWrong": "THE ANSWER: The values were supplied in a different order from the fitted columns. A fitted model knows only that its first input is whatever its first training column was. Swap two and it happily applies the wrong coefficient to each. Build the row as a frame with named columns and this class of error disappears.\n\nWhy the others are wrong. \u201cThe new values should have been scaled first\u201d \u2014 Scaling would matter for some model types and it would not repair a swap. Scaled or raw, the values are in the wrong positions.  \u201cThe model was fitted on too few features to predict anything\u201d \u2014 Three or four features is enough to produce a prediction. The count is fine and the order is not.  \u201cpredict() needs a two-dimensional input\u201d \u2014 It does, and it was given one. The doubled brackets are correct here."
          },
          {
            "n": 3,
            "kind": "traceback",
            "title": "What is the most likely cause?",
            "help": "Traceback (most recent call last):\n  File \"<ipython-input-9-5e6f7a>\", line 1, in <module>\n    model.fit(X, y)\nValueError: Found input variables with inconsistent numbers\nof samples: [824, 1030]",
            "choices": [
              {
                "text": "The features were filtered or had rows dropped and the target was not, so the two no longer line up",
                "correct": true
              },
              {
                "text": "There are too few rows to fit a model",
                "correct": false
              },
              {
                "text": "The features and the target need to be the same data type",
                "correct": false
              },
              {
                "text": "The target column contains missing values",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. Dropping missing values from the feature frame without applying the same selection to the target is the usual cause. Filter the frame first and take X and y from the filtered frame so they can never drift apart.",
            "fbWrong": "THE ANSWER: The features were filtered or had rows dropped and the target was not, so the two no longer line up. Dropping missing values from the feature frame without applying the same selection to the target is the usual cause. Filter the frame first and take X and y from the filtered frame so they can never drift apart.\n\nWhy the others are wrong. \u201cThere are too few rows to fit a model\u201d \u2014 Both counts here are ample. The problem is that they are not equal.  \u201cThe features and the target need to be the same data type\u201d \u2014 They routinely differ, and that is fine. The error counts rows and says nothing about types.  \u201cThe target column contains missing values\u201d \u2014 Missing values in the target give a different complaint about NaN. This message is purely about the row counts disagreeing."
          },
          {
            "n": 4,
            "kind": "interpretation",
            "title": "A teammate shows you this plot and this conclusion. How should you read it?",
            "help": "plot:        y = residual (actual - predicted), MPa\n             x = ACTUAL 28-day strength, MPa\n             a clear upward slope, left to right\n\nconclusion:  \"the model under-predicts strong mixes\"",
            "choices": [
              {
                "text": "A slope in the residuals always means the model is broken",
                "correct": false
              },
              {
                "text": "The slope appears by construction; plot residuals against the predicted value",
                "correct": true
              },
              {
                "text": "The residuals should have been squared before plotting",
                "correct": false
              },
              {
                "text": "The conclusion is right, and the model needs an extra feature to fix it",
                "correct": false
              }
            ],
            "fbCorrect": "Correct, and this catches almost everybody once. The actual value equals the prediction plus the residual, so the residual is built into the quantity on the horizontal axis and rises with it. Against the predicted value the slope disappears and any real pattern becomes visible.",
            "fbWrong": "THE ANSWER: The slope appears by construction; plot residuals against the predicted value. This catches almost everybody once. The actual value equals the prediction plus the residual, so the residual is built into the quantity on the horizontal axis and rises with it. Against the predicted value the slope disappears and any real pattern becomes visible.\n\nWhy the others are wrong. \u201cA slope in the residuals always means the model is broken\u201d \u2014 A slope against the predicted value would be worth investigating. A slope against the actual value is arithmetic rather than a finding.  \u201cThe residuals should have been squared before plotting\u201d \u2014 Squaring throws away the sign, which is the most useful part of a residual. The pairing of axes is what is wrong here.  \u201cThe conclusion is right, and the model needs an extra feature to fix it\u201d \u2014 The conclusion may happen to be true and this plot cannot establish it. Redraw against the predicted value before changing the model."
          },
          {
            "n": 5,
            "kind": "judgement",
            "title": "Your model reaches a mean absolute error of 4.2 MPa. The client asks whether that is good. What do you need before you can answer?",
            "help": "",
            "choices": [
              {
                "text": "Nothing further; 4.2 MPa is a small number",
                "correct": false
              },
              {
                "text": "The error of predicting the mean, and the cylinder test's own repeatability",
                "correct": true
              },
              {
                "text": "A larger dataset",
                "correct": false
              },
              {
                "text": "A second model to compare it against",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. Both comparisons are needed. Predicting the mean is the score to beat, and a cylinder test repeats to about 2 MPa between specimens, so 4.2 MPa is roughly twice as uncertain as the measurement it stands in for. That is the sentence the client actually needs.",
            "fbWrong": "THE ANSWER: The error of predicting the mean, and the cylinder test's own repeatability. Both comparisons are needed. Predicting the mean is the score to beat, and a cylinder test repeats to about 2 MPa between specimens, so 4.2 MPa is roughly twice as uncertain as the measurement it stands in for. That is the sentence the client actually needs.\n\nWhy the others are wrong. \u201cNothing further; 4.2 MPa is a small number\u201d \u2014 Small against what? A number with no reference is not yet a result.  \u201cA larger dataset\u201d \u2014 More data may lower the error and does not tell you whether the current figure is useful. That judgement needs a reference point.  \u201cA second model to compare it against\u201d \u2014 Two models with no baseline tell you which is better and leave you unable to say whether either is worth having."
          }
        ]
      },
      {
        "week": 9,
        "number": 8,
        "title": "CML3112 \u00b7 Weekly Quiz 8 \u2014 Classification",
        "intro": "Read what each question shows you. None of them can be answered without it.\n\nHOW THIS WORKS\n\u2022 Answer it now, in the 5 minutes on the screen. That is when this is meant to be taken, while the session is still fresh.\n\u2022 The form then stays open for 24 hours and closes itself. That window is there so a dead network or a broken phone does not cost you a mark you had earned. Take it in the room if you can: by Thursday you will have forgotten the session, and the feedback will be worth less to you.\n\u2022 ONE attempt, from your signed-in Google account. You cannot reopen it or change an answer, so read each question once, properly.\n\u2022 The first box asks for your registration number. It is the number printed on your student card, and it is how the mark reaches your record.\n\u2022 Five questions, one mark each, worth 1% of your final mark.\n\u2022 Your best ten of twelve quizzes count. Missing two costs you nothing, and there are no resits.\n\u2022 When you submit, tap View score. You get a tick or a cross on each question with the feedback underneath. Your mark is the number of ticks, and the feedback on anything you got wrong is the part worth reading.\n\u2022 A question left blank scores the same as one answered wrongly, so answer all five.",
        "questions": [
          {
            "n": 1,
            "kind": "diagnosis",
            "title": "A teammate is pleased with this result. What has the model actually learned?",
            "help": "accuracy                     0.966\npours predicted to fail          0\n\n# in this register 3.4 in 100 pours fail specification",
            "choices": [
              {
                "text": "A genuinely strong rule, since 96.6 per cent is a high score",
                "correct": false
              },
              {
                "text": "That more features are needed to raise accuracy",
                "correct": false
              },
              {
                "text": "To answer with the majority class every time, which scores the majority-class share and finds nothing",
                "correct": true
              },
              {
                "text": "That the two classes are equally easy to separate",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. Since 96.6 in 100 cases are negative, always saying negative scores 0.966. The model has found the base rate and no signal. Recall on the class you care about is zero, and that is the number to report.",
            "fbWrong": "THE ANSWER: To answer with the majority class every time, which scores the majority-class share and finds nothing. Since 96.6 in 100 cases are negative, always saying negative scores 0.966. The model has found the base rate and no signal. Recall on the class you care about is zero, and that is the number to report.\n\nWhy the others are wrong. \u201cA genuinely strong rule, since 96.6 per cent is a high score\u201d \u2014 The score is exactly what you get for free by ignoring the data. A rule that never fires cannot be strong at the job it was built for.  \u201cThat more features are needed to raise accuracy\u201d \u2014 Accuracy is already near its ceiling and is the wrong instrument. Change the metric before changing the model.  \u201cThat the two classes are equally easy to separate\u201d \u2014 It never attempted the separation. It predicted one class throughout."
          },
          {
            "n": 2,
            "kind": "diagnosis",
            "title": "This model was tested against a precast yard's quality register of ten thousand pours. Read the confusion matrix. Which statement does it support?",
            "help": "                      pred: meets    pred: fails\nactual: meets                9620             36\nactual: fails                 310             34\n\n10,000 pours in total; accuracy 0.965",
            "choices": [
              {
                "text": "Accuracy of 0.965 shows it is fit for use",
                "correct": false
              },
              {
                "text": "Its main weakness is false alarms",
                "correct": false
              },
              {
                "text": "It is well balanced between the two kinds of error",
                "correct": false
              },
              {
                "text": "It misses about nine in ten of the cases it exists to catch",
                "correct": true
              }
            ],
            "fbCorrect": "Correct. Recall on the class of interest is 34 out of 344, which is 0.099. The high accuracy comes almost entirely from the 9,620 easy negatives. This is the number the matrix exists to expose.",
            "fbWrong": "THE ANSWER: It misses about nine in ten of the cases it exists to catch. Recall on the class of interest is 34 out of 344, which is 0.099. The high accuracy comes almost entirely from the 9,620 easy negatives. This is the number the matrix exists to expose.\n\nWhy the others are wrong. \u201cAccuracy of 0.965 shows it is fit for use\u201d \u2014 Predicting the majority class throughout would score 0.966, which is higher. Accuracy cannot see this failure.  \u201cIts main weakness is false alarms\u201d \u2014 There are only 36 false alarms against 310 misses. The costly error here is the one being made nearly ten times as often.  \u201cIt is well balanced between the two kinds of error\u201d \u2014 310 against 36 is close to a nine-to-one imbalance in the errors."
          },
          {
            "n": 3,
            "kind": "traceback",
            "title": "What does this tell you to change?",
            "help": "Traceback (most recent call last):\n  File \"<ipython-input-11-8b9c0d>\", line 1, in <module>\n    print(recall_score(y_test, pred))\nValueError: Target is multiclass but average='binary'.\nPlease choose another average setting, one of [None, 'micro', 'macro', 'weighted'].",
            "choices": [
              {
                "text": "The test set is too small for recall to be defined",
                "correct": false
              },
              {
                "text": "The target has more than two classes, so you must say how recall should be combined across them",
                "correct": true
              },
              {
                "text": "Recall cannot be computed for more than two classes",
                "correct": false
              },
              {
                "text": "The predictions are the wrong data type",
                "correct": false
              }
            ],
            "fbCorrect": "Correct, and the choice matters. average=None gives you recall per class, which is usually what you want, because a single combined figure can hide a class the model never predicts.",
            "fbWrong": "THE ANSWER: The target has more than two classes, so you must say how recall should be combined across them. The choice matters. average=None gives you recall per class, which is usually what you want, because a single combined figure can hide a class the model never predicts.\n\nWhy the others are wrong. \u201cThe test set is too small for recall to be defined\u201d \u2014 Size is not mentioned and is not the issue. The class count is.  \u201cRecall cannot be computed for more than two classes\u201d \u2014 It can, once you state how to aggregate it. The error offers you the options.  \u201cThe predictions are the wrong data type\u201d \u2014 The types are acceptable. The message is about the number of classes in the target."
          },
          {
            "n": 4,
            "kind": "interpretation",
            "title": "You lower the decision threshold from 0.5 to 0.2 and re-score the same model on the same test set. What has changed?",
            "help": "threshold 0.5   recall 0.099   false alarms  36\nthreshold 0.2   recall 0.439   false alarms 290",
            "choices": [
              {
                "text": "The result is invalid because the threshold should stay at 0.5",
                "correct": false
              },
              {
                "text": "The model has been improved by better tuning",
                "correct": false
              },
              {
                "text": "The model now overfits, because recall rose sharply",
                "correct": false
              },
              {
                "text": "Nothing about the model; you moved along its trade-off, buying recall by accepting eight times as many false alarms",
                "correct": true
              }
            ],
            "fbCorrect": "Correct. The model and its scores are untouched: only the cut-off you apply to them changed. Which threshold is right depends on what a false alarm costs against a miss, and that is a question about the work rather than the model.",
            "fbWrong": "THE ANSWER: Nothing about the model; you moved along its trade-off, buying recall by accepting eight times as many false alarms. The model and its scores are untouched: only the cut-off you apply to them changed. Which threshold is right depends on what a false alarm costs against a miss, and that is a question about the work rather than the model.\n\nWhy the others are wrong. \u201cThe result is invalid because the threshold should stay at 0.5\u201d \u2014 0.5 is a default rather than a rule. On a problem where a miss costs far more than a false alarm, moving it is exactly the right thing to do.  \u201cThe model has been improved by better tuning\u201d \u2014 No retraining took place. The same probabilities are being cut in a different place.  \u201cThe model now overfits, because recall rose sharply\u201d \u2014 Overfitting is about the gap between training and unseen data. This is one model on one test set at two thresholds."
          },
          {
            "n": 5,
            "kind": "judgement",
            "title": "Accepting a substandard pour means it goes into the structure and somebody finds out later. Rejecting a sound pour costs one panel and some programme. Which metric should govern your model, and why?",
            "help": "",
            "choices": [
              {
                "text": "Whichever metric gives the highest number, so the result reads well",
                "correct": false
              },
              {
                "text": "Recall on the class you cannot afford to miss, with the false-alarm rate beside it",
                "correct": true
              },
              {
                "text": "Precision, because false alarms annoy the operators",
                "correct": false
              },
              {
                "text": "Accuracy, because it summarises overall performance",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. The expensive error is the miss, so recall is the quantity to drive up. Quoting the false-alarm rate beside it keeps you honest, because recall can always be bought and somebody has to pay for it.",
            "fbWrong": "THE ANSWER: Recall on the class you cannot afford to miss, with the false-alarm rate beside it. The expensive error is the miss, so recall is the quantity to drive up. Quoting the false-alarm rate beside it keeps you honest, because recall can always be bought and somebody has to pay for it.\n\nWhy the others are wrong. \u201cWhichever metric gives the highest number, so the result reads well\u201d \u2014 Choosing a metric to flatter the model is how a system that misses nine failures in ten gets signed off.  \u201cPrecision, because false alarms annoy the operators\u201d \u2014 Precision alone rewards a model that fires only when certain, which is a model that misses most of the cases. It belongs in the report next to recall rather than in charge of it.  \u201cAccuracy, because it summarises overall performance\u201d \u2014 At a base rate near 3 per cent, accuracy is dominated by easy negatives and a useless model scores 0.966. It cannot see the error that matters here."
          }
        ]
      },
      {
        "week": 10,
        "number": 9,
        "title": "CML3112 \u00b7 Weekly Quiz 9 \u2014 Can I trust this model?",
        "intro": "Read what each question shows you. None of them can be answered without it.\n\nHOW THIS WORKS\n\u2022 Answer it now, in the 5 minutes on the screen. That is when this is meant to be taken, while the session is still fresh.\n\u2022 The form then stays open for 24 hours and closes itself. That window is there so a dead network or a broken phone does not cost you a mark you had earned. Take it in the room if you can: by Thursday you will have forgotten the session, and the feedback will be worth less to you.\n\u2022 ONE attempt, from your signed-in Google account. You cannot reopen it or change an answer, so read each question once, properly.\n\u2022 The first box asks for your registration number. It is the number printed on your student card, and it is how the mark reaches your record.\n\u2022 Five questions, one mark each, worth 1% of your final mark.\n\u2022 Your best ten of twelve quizzes count. Missing two costs you nothing, and there are no resits.\n\u2022 When you submit, tap View score. You get a tick or a cross on each question with the feedback underneath. Your mark is the number of ticks, and the feedback on anything you got wrong is the part worth reading.\n\u2022 A question left blank scores the same as one answered wrongly, so answer all five.",
        "questions": [
          {
            "n": 1,
            "kind": "diagnosis",
            "title": "This reports a good test score. Why can that score not be trusted?",
            "help": "scaler = StandardScaler()\nX_scaled = scaler.fit_transform(X)     # whole file\n\nX_tr, X_te, y_tr, y_te = train_test_split(X_scaled, y)\nmodel.fit(X_tr, y_tr)\nprint(model.score(X_te, y_te))",
            "choices": [
              {
                "text": "The split should come before the features are selected",
                "correct": false
              },
              {
                "text": "StandardScaler is the wrong scaler for this data",
                "correct": false
              },
              {
                "text": "Nothing is wrong; scaling does not use the target",
                "correct": false
              },
              {
                "text": "The scaler was fitted on the whole file, so the test rows helped set the scaling",
                "correct": true
              }
            ],
            "fbCorrect": "Correct. The test rows are supposed to stand in for cases you have never seen, and here they helped set the scaling. Put the scaler in a Pipeline and fit it after the split, so it only ever sees training rows.",
            "fbWrong": "THE ANSWER: The scaler was fitted on the whole file, so the test rows helped set the scaling. The test rows are supposed to stand in for cases you have never seen, and here they helped set the scaling. Put the scaler in a Pipeline and fit it after the split, so it only ever sees training rows.\n\nWhy the others are wrong. \u201cThe split should come before the features are selected\u201d \u2014 Selecting which columns to use is fine either side. Measuring something from the data is what has to wait until after the split.  \u201cStandardScaler is the wrong scaler for this data\u201d \u2014 The choice of scaler is a separate question. Any scaler fitted before the split leaks in the same way.  \u201cNothing is wrong; scaling does not use the target\u201d \u2014 Leakage does not require the target. Borrowing the test rows' mean and spread means the test set is no longer a clean estimate, and how far the number is distorted is not something you can work out from the outside, which is the real cost."
          },
          {
            "n": 2,
            "kind": "diagnosis",
            "title": "Which of the three error stories does this pattern match?",
            "help": "training score   0.98\ntest score       0.61",
            "choices": [
              {
                "text": "The two scores are measuring different quantities",
                "correct": false
              },
              {
                "text": "The model has memorised its training rows and does not generalise",
                "correct": true
              },
              {
                "text": "Information has leaked from the test set into training",
                "correct": false
              },
              {
                "text": "The model is too simple to capture the pattern",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. A high training score with a much lower test score is the signature of a model with too much freedom for the data. Simplify it, constrain it, or get more rows.",
            "fbWrong": "THE ANSWER: The model has memorised its training rows and does not generalise. A high training score with a much lower test score is the signature of a model with too much freedom for the data. Simplify it, constrain it, or get more rows.\n\nWhy the others are wrong. \u201cThe two scores are measuring different quantities\u201d \u2014 Both are the same measure on different rows. That is what makes the comparison meaningful.  \u201cInformation has leaked from the test set into training\u201d \u2014 Leakage usually makes both scores look good, since the model has effectively seen the answers. A large gap points the other way.  \u201cThe model is too simple to capture the pattern\u201d \u2014 A model that is too simple scores poorly on both, because it cannot even fit the rows it was given. Here it fits them almost perfectly."
          },
          {
            "n": 3,
            "kind": "traceback",
            "title": "A teammate has already tried to deal with the gaps, in the cell shown above the traceback. Read both, then say what you would change.",
            "help": "imp = SimpleImputer(strategy=\"mean\")\nX[[\"slump\"]] = imp.fit_transform(X[[\"slump\"]])\n\nX_tr, X_te, y_tr, y_te = train_test_split(X, y)\npipe = Pipeline([(\"model\", Ridge())])\npipe.fit(X_tr, y_tr)\n\nTraceback (most recent call last):\n  File \"<ipython-input-13-1a2b3c>\", line 6, in <module>\n    pipe.fit(X_tr, y_tr)\nValueError: Input X contains NaN.",
            "choices": [
              {
                "text": "Drop the rows that still contain gaps",
                "correct": false
              },
              {
                "text": "Impute the remaining columns the same way, before the split",
                "correct": false
              },
              {
                "text": "Replace the remaining gaps with zero so the model can fit",
                "correct": false
              },
              {
                "text": "Move the imputer inside the Pipeline, and cover every column",
                "correct": true
              }
            ],
            "fbCorrect": "Correct on both counts. Only one column was imputed, so the gaps in the others are still there, which is why the error still fires. And fitting it on the whole frame before the split measures the test rows, which is the leak from question one wearing different clothes. Inside the pipeline both problems go away at once.",
            "fbWrong": "THE ANSWER: Move the imputer inside the Pipeline, and cover every column. Correct on both counts. Only one column was imputed, so the gaps in the others are still there, which is why the error still fires. And fitting it on the whole frame before the split measures the test rows, which is the leak from question one wearing different clothes. Inside the pipeline both problems go away at once.\n\nWhy the others are wrong. \u201cDrop the rows that still contain gaps\u201d \u2014 It would run, and it discards data and can bias what is left if the gaps cluster in one source, which Week 4 showed they often do.  \u201cImpute the remaining columns the same way, before the split\u201d \u2014 That silences the error and keeps the leak. Every value the imputer learns before the split has been measured partly from the test rows.  \u201cReplace the remaining gaps with zero so the model can fit\u201d \u2014 Zero is a real value on these columns, so this quietly invents low readings. Week 6 covers the damage that does."
          },
          {
            "n": 4,
            "kind": "interpretation",
            "title": "You run five-fold cross-validation and get these scores. What should you report, and what should you look at?",
            "help": "fold scores: 0.71, 0.68, 0.74, 0.52, 0.70\nmean 0.67",
            "choices": [
              {
                "text": "Nothing yet; five folds is too few to report",
                "correct": false
              },
              {
                "text": "The mean alone, since averaging is the purpose of cross-validation",
                "correct": false
              },
              {
                "text": "The mean with its spread, and look into the 0.52 fold",
                "correct": true
              },
              {
                "text": "The best fold, since it shows what the model can achieve",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. Four folds sit close together and one sits well below, which suggests that fold contains something the others do not. Group structure in the rows is the usual explanation, and it is the subject of the next question.",
            "fbWrong": "THE ANSWER: The mean with its spread, and look into the 0.52 fold. Four folds sit close together and one sits well below, which suggests that fold contains something the others do not. Group structure in the rows is the usual explanation, and it is the subject of the next question.\n\nWhy the others are wrong. \u201cNothing yet; five folds is too few to report\u201d \u2014 Five folds is a standard choice and perfectly reportable. The spread is part of the report rather than a reason to withhold it.  \u201cThe mean alone, since averaging is the purpose of cross-validation\u201d \u2014 A bare mean hides the thing worth knowing. Reporting 0.67 with no spread conceals a fold that scored 0.52 and the reason behind it.  \u201cThe best fold, since it shows what the model can achieve\u201d \u2014 Quoting the best fold is selecting the most flattering result from your own experiment."
          },
          {
            "n": 5,
            "kind": "judgement",
            "title": "You discover that several specimens from the same mix batch are split across your training and test sets. Specimens from one batch are near-copies of each other. What should you do?",
            "help": "",
            "choices": [
              {
                "text": "Increase the size of the test set",
                "correct": false
              },
              {
                "text": "Split by batch, so every specimen from one batch sits entirely in training or entirely in test",
                "correct": true
              },
              {
                "text": "Leave it, because a random split is unbiased by definition",
                "correct": false
              },
              {
                "text": "Remove the duplicate-looking specimens",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. Otherwise the model can recognise a batch it has already been trained on, and your test score measures recall of batches rather than prediction of strength. GroupShuffleSplit and GroupKFold exist for this.",
            "fbWrong": "THE ANSWER: Split by batch, so every specimen from one batch sits entirely in training or entirely in test. Otherwise the model can recognise a batch it has already been trained on, and your test score measures recall of batches rather than prediction of strength. GroupShuffleSplit and GroupKFold exist for this.\n\nWhy the others are wrong. \u201cIncrease the size of the test set\u201d \u2014 A larger test set built the same way carries the same flaw at greater scale.  \u201cLeave it, because a random split is unbiased by definition\u201d \u2014 Random assignment of rows is unbiased about rows and blind to the fact that these rows come in near-identical families.  \u201cRemove the duplicate-looking specimens\u201d \u2014 They are genuine separate tests rather than duplicates, and discarding them throws away real information about within-batch variation."
          }
        ]
      },
      {
        "week": 11,
        "number": 10,
        "title": "CML3112 \u00b7 Weekly Quiz 10 \u2014 Features",
        "intro": "Read what each question shows you. None of them can be answered without it.\n\nHOW THIS WORKS\n\u2022 Answer it now, in the 5 minutes on the screen. That is when this is meant to be taken, while the session is still fresh.\n\u2022 The form then stays open for 24 hours and closes itself. That window is there so a dead network or a broken phone does not cost you a mark you had earned. Take it in the room if you can: by Thursday you will have forgotten the session, and the feedback will be worth less to you.\n\u2022 ONE attempt, from your signed-in Google account. You cannot reopen it or change an answer, so read each question once, properly.\n\u2022 The first box asks for your registration number. It is the number printed on your student card, and it is how the mark reaches your record.\n\u2022 Five questions, one mark each, worth 1% of your final mark.\n\u2022 Your best ten of twelve quizzes count. Missing two costs you nothing, and there are no resits.\n\u2022 When you submit, tap View score. You get a tick or a cross on each question with the feedback underneath. Your mark is the number of ticks, and the feedback on anything you got wrong is the part worth reading.\n\u2022 A question left blank scores the same as one answered wrongly, so answer all five.",
        "questions": [
          {
            "n": 1,
            "kind": "diagnosis",
            "title": "A teammate adds a scaler expecting an improvement and the score does not budge. Why not?",
            "help": "before:  DecisionTreeRegressor(random_state=0)\n                                                MAE 5.1\nafter:   Pipeline([(\"scale\", StandardScaler()),\n                   (\"model\", DecisionTreeRegressor(\n                                 random_state=0))])\n                                                MAE 5.1",
            "choices": [
              {
                "text": "The tree needs a greater depth before scaling helps",
                "correct": false
              },
              {
                "text": "The scaler was placed after the model in the pipeline",
                "correct": false
              },
              {
                "text": "A tree splits on the order of the values, and scaling preserves that order",
                "correct": true
              },
              {
                "text": "The features were already on the same scale",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. Rescaling moves the numbers and leaves their ranking untouched, and a threshold split only cares about ranking. Scaling earns its keep for models that measure distances or fit coefficients.",
            "fbWrong": "THE ANSWER: A tree splits on the order of the values, and scaling preserves that order. Rescaling moves the numbers and leaves their ranking untouched, and a threshold split only cares about ranking. Scaling earns its keep for models that measure distances or fit coefficients.\n\nWhy the others are wrong. \u201cThe tree needs a greater depth before scaling helps\u201d \u2014 Depth changes how the tree fits and never makes it sensitive to a monotonic rescaling.  \u201cThe scaler was placed after the model in the pipeline\u201d \u2014 It is first, which is the correct position. The order in the pipeline is not the issue.  \u201cThe features were already on the same scale\u201d \u2014 Even if they were, that would not be the reason. A tree is unaffected by this kind of rescaling whatever the starting scales happen to be."
          },
          {
            "n": 2,
            "kind": "diagnosis",
            "title": "The score on your own test split improves after this change, and the model is worse. What has happened?",
            "help": "print(df.shape)\n(1030, 10)\n\nprint(df[\"batch_id\"].nunique())\n240\n\nX = pd.get_dummies(df, columns=[\"batch_id\"])\nprint(X.shape)\n(1030, 249)",
            "choices": [
              {
                "text": "It added one column per identifier, so the model can now recognise individual units",
                "correct": true
              },
              {
                "text": "The identifiers should have been numbered 1 to 847 instead",
                "correct": false
              },
              {
                "text": "get_dummies should have been given the whole frame",
                "correct": false
              },
              {
                "text": "It made the frame too wide for the model to fit",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. An identifier expanded this way hands the model a lookup table for the units in your file. It scores well wherever the same units appear on both sides of the split and carries nothing to a new one. Drop the identifier and keep the columns that describe the thing.",
            "fbWrong": "THE ANSWER: It added one column per identifier, so the model can now recognise individual units. An identifier expanded this way hands the model a lookup table for the units in your file. It scores well wherever the same units appear on both sides of the split and carries nothing to a new one. Drop the identifier and keep the columns that describe the thing.\n\nWhy the others are wrong. \u201cThe identifiers should have been numbered 1 to 847 instead\u201d \u2014 That is worse: it tells a straight-line model that unit 800 is a hundred times unit 8. Neither encoding rescues a column that is only a label.  \u201cget_dummies should have been given the whole frame\u201d \u2014 It was given the whole frame with one column named for expansion, which is the normal usage. The choice of column is the fault.  \u201cIt made the frame too wide for the model to fit\u201d \u2014 A few hundred columns is unremarkable and fits without complaint. The problem is what those columns mean."
          },
          {
            "n": 3,
            "kind": "traceback",
            "title": "What has happened, and what is the catch in the obvious fix?",
            "help": "enc = OneHotEncoder(drop=\"first\")\n# ... fitted on exposure_class values XC1, XC3, XD2, XS1\n\nTraceback (most recent call last):\n  File \"<ipython-input-15-6d7e8f>\", line 1, in <module>\n    pipe.predict(new_rows)\nValueError: Found unknown categories ['XS3'] in column 0\nduring transform",
            "choices": [
              {
                "text": "The category column should be dropped from the model",
                "correct": false
              },
              {
                "text": "Refitting the encoder on the new rows as well will fix it properly",
                "correct": false
              },
              {
                "text": "Adding handle_unknown=\"ignore\" solves it cleanly, with no side effect worth worrying about",
                "correct": false
              },
              {
                "text": "handle_unknown=\"ignore\" clears it, and with drop=\"first\" an unseen category then encodes as the dropped one",
                "correct": true
              }
            ],
            "fbCorrect": "Correct, and the second half is the part almost nobody is told. An ignored unknown category is encoded as all zeros, which is exactly how the dropped reference category is encoded, so every new category silently becomes the baseline. Choose one of the two options deliberately and count how often an unknown value arrives.",
            "fbWrong": "THE ANSWER: handle_unknown=\"ignore\" clears it, and with drop=\"first\" an unseen category then encodes as the dropped one. The second half is the part almost nobody is told. An ignored unknown category is encoded as all zeros, which is exactly how the dropped reference category is encoded, so every new category silently becomes the baseline. Choose one of the two options deliberately and count how often an unknown value arrives.\n\nWhy the others are wrong. \u201cThe category column should be dropped from the model\u201d \u2014 It may be carrying real signal. The task is to encode it so it survives a value you have not seen before.  \u201cRefitting the encoder on the new rows as well will fix it properly\u201d \u2014 Fitting anything on rows you are about to predict is the leakage pattern from Week 10. It also cannot work in service, where the new value arrives after the model is deployed.  \u201cAdding handle_unknown=\"ignore\" solves it cleanly, with no side effect worth worrying about\u201d \u2014 It does clear the error. The side effect is that the unknown category is encoded as all zeros, and because drop=\"first\" is set, that is the same encoding as the dropped category."
          },
          {
            "n": 4,
            "kind": "interpretation",
            "title": "Each row removes one feature and refits. Which feature has earned its place least?",
            "help": "features                        MAE (MPa)\nall five                              3.9\nminus water/cement ratio              6.8\nminus curing age                      7.4\nminus total binder                    4.0\nminus superplasticiser                4.1\nminus fly ash                         4.6",
            "choices": [
              {
                "text": "Total binder, because removing it moves the error by 0.1 MPa",
                "correct": true
              },
              {
                "text": "Curing age, because it has the largest error when removed",
                "correct": false
              },
              {
                "text": "None of them; every feature earns its place",
                "correct": false
              },
              {
                "text": "Water/cement ratio, because 6.8 is a poor result",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. Curing age and the water/cement ratio each cost you around 3 MPa when removed, and total binder costs 0.1 MPa. It is very likely saying the same thing as the cement column already in the model.",
            "fbWrong": "THE ANSWER: Total binder, because removing it moves the error by 0.1 MPa. Curing age and the water/cement ratio each cost you around 3 MPa when removed, and total binder costs 0.1 MPa. It is very likely saying the same thing as the cement column already in the model.\n\nWhy the others are wrong. \u201cCuring age, because it has the largest error when removed\u201d \u2014 That reading is inverted. A large error without a feature means the model badly needs it.  \u201cNone of them; every feature earns its place\u201d \u2014 A feature whose removal changes the error by 0.1 MPa is carrying almost nothing the others do not already carry.  \u201cWater/cement ratio, because 6.8 is a poor result\u201d \u2014 6.8 is the error you suffer without it, which is why it belongs in the model."
          },
          {
            "n": 5,
            "kind": "judgement",
            "title": "Two teams reach almost the same error. One uses a random forest on the raw columns; the other uses linear regression on the water/cement ratio and four other engineered features. Every rejection has to be explained in writing to a paying client. Which do you recommend?",
            "help": "",
            "choices": [
              {
                "text": "Either, since the error is what matters",
                "correct": false
              },
              {
                "text": "The random forest, because ensembles generalise better in general",
                "correct": false
              },
              {
                "text": "The engineered features with the simpler model, whose reasoning can be read off and defended",
                "correct": true
              },
              {
                "text": "The random forest, and add an importance chart to explain it",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. On equal performance the stated constraint decides it, and a coefficient on a quantity with physical meaning is something you can put in front of the person who has to sign. The engineering went into the features rather than the algorithm.",
            "fbWrong": "THE ANSWER: The engineered features with the simpler model, whose reasoning can be read off and defended. On equal performance the stated constraint decides it, and a coefficient on a quantity with physical meaning is something you can put in front of the person who has to sign. The engineering went into the features rather than the algorithm.\n\nWhy the others are wrong. \u201cEither, since the error is what matters\u201d \u2014 The error was stated as a condition to meet rather than the only criterion. Explainability was given as a requirement.  \u201cThe random forest, because ensembles generalise better in general\u201d \u2014 It may well generalise better on some problems, and here the two are level while only one of them satisfies the constraint you were given.  \u201cThe random forest, and add an importance chart to explain it\u201d \u2014 Feature importance tells you which columns the model leaned on overall. It does not tell the client why this particular case was rejected, which is the question they will ask."
          }
        ]
      },
      {
        "week": 12,
        "number": 11,
        "title": "CML3112 \u00b7 Weekly Quiz 11 \u2014 Model comparison (integrative)",
        "intro": "Read what each question shows you. None of them can be answered without it.\n\nHOW THIS WORKS\n\u2022 Answer it now, in the 5 minutes on the screen. That is when this is meant to be taken, while the session is still fresh.\n\u2022 The form then stays open for 24 hours and closes itself. That window is there so a dead network or a broken phone does not cost you a mark you had earned. Take it in the room if you can: by Thursday you will have forgotten the session, and the feedback will be worth less to you.\n\u2022 ONE attempt, from your signed-in Google account. You cannot reopen it or change an answer, so read each question once, properly.\n\u2022 The first box asks for your registration number. It is the number printed on your student card, and it is how the mark reaches your record.\n\u2022 Five questions, one mark each, worth 1% of your final mark.\n\u2022 Your best ten of twelve quizzes count. Missing two costs you nothing, and there are no resits.\n\u2022 When you submit, tap View score. You get a tick or a cross on each question with the feedback underneath. Your mark is the number of ticks, and the feedback on anything you got wrong is the part worth reading.\n\u2022 A question left blank scores the same as one answered wrongly, so answer all five.",
        "questions": [
          {
            "n": 1,
            "kind": "diagnosis",
            "title": "A teammate concludes the forest is the better model. What does this table actually support?",
            "help": "fold                  1      2      3      4      5   mean\nrandom forest      0.78   0.70   0.76   0.71   0.75   0.74\nlogistic reg.      0.75   0.73   0.72   0.68   0.72   0.72\ndifference        +0.03  -0.03  +0.04  +0.03  +0.03",
            "choices": [
              {
                "text": "The forest is better, since it has the stronger mean",
                "correct": false
              },
              {
                "text": "Very little: the difference changes sign between folds, so on this evidence the two cannot be separated",
                "correct": true
              },
              {
                "text": "The forest is better, because it wins the majority of folds",
                "correct": false
              },
              {
                "text": "The comparison is invalid because the models share folds",
                "correct": false
              }
            ],
            "fbCorrect": "Correct, and reading the per-fold differences is what settles it. The sign of the difference flips from fold to fold, so the mean gap of 0.02 is not a consistent advantage. Report them as level on this data and let the stated constraints decide. Note what makes this readable at all: both models were scored on the SAME five folds, so the differences can be paired up.",
            "fbWrong": "THE ANSWER: Very little: the difference changes sign between folds, so on this evidence the two cannot be separated. Reading the per-fold differences is what settles it. The sign of the difference flips from fold to fold, so the mean gap of 0.02 is not a consistent advantage. Report them as level on this data and let the stated constraints decide. Note what makes this readable at all: both models were scored on the SAME five folds, so the differences can be paired up.\n\nWhy the others are wrong. \u201cThe forest is better, since it has the stronger mean\u201d \u2014 A mean hides the fold-by-fold picture. Here the sign of the difference flips, which is the pattern of two models that are level rather than one that is ahead.  \u201cThe forest is better, because it wins the majority of folds\u201d \u2014 Winning more folds than it loses is worth noticing and is weak evidence at this margin, because the fold it loses it loses by as much as the others are won. With only five folds this pattern arises easily between two models of equal ability.  \u201cThe comparison is invalid because the models share folds\u201d \u2014 Sharing folds is what makes the comparison valid. Scoring each model on its own random split is the mistake, and it is the subject of the next question."
          },
          {
            "n": 2,
            "kind": "diagnosis",
            "title": "Two models, two scores, no error anywhere. Why can these numbers not be compared?",
            "help": "# model A\nX_tr, X_te, y_tr, y_te = train_test_split(X, y,\n                              random_state=1)\n# ... fit A ...      score 0.78\n\n# model B\nX_tr, X_te, y_tr, y_te = train_test_split(X, y,\n                              random_state=7)\n# ... fit B ...      score 0.81",
            "choices": [
              {
                "text": "They were scored on different test sets, so the gap may be the split rather than the model",
                "correct": true
              },
              {
                "text": "Model B had the advantage of a later random state",
                "correct": false
              },
              {
                "text": "The scores need to be averaged together",
                "correct": false
              },
              {
                "text": "Nothing is wrong, since both used the same data file",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. Changing the seed changes the split, and split-to-split variation on this kind of data is often larger than the gap you are trying to measure. Score every model on identical folds, which is what cross_val_score with a fixed splitter gives you.",
            "fbWrong": "THE ANSWER: They were scored on different test sets, so the gap may be the split rather than the model. Changing the seed changes the split, and split-to-split variation on this kind of data is often larger than the gap you are trying to measure. Score every model on identical folds, which is what cross_val_score with a fixed splitter gives you.\n\nWhy the others are wrong. \u201cModel B had the advantage of a later random state\u201d \u2014 The number in random_state is a label for a shuffle and carries no ordering. Seed 7 is not later or better than seed 1.  \u201cThe scores need to be averaged together\u201d \u2014 Averaging two figures measured on different test sets produces a number that describes neither model.  \u201cNothing is wrong, since both used the same data file\u201d \u2014 The same file cut two different ways gives two different test sets. The comparison needs the cuts to match."
          },
          {
            "n": 3,
            "kind": "traceback",
            "title": "You have run this notebook for an hour and now get this. What is the most likely history behind it?",
            "help": "Traceback (most recent call last):\n  File \"<ipython-input-31-9a8b7c>\", line 1, in <module>\n    print(forest.predict(X_te)[:5])\nNotFittedError: This RandomForestClassifier instance is not\nfitted yet. Call 'fit' with appropriate arguments before\nusing this estimator.",
            "choices": [
              {
                "text": "The test features contain missing values",
                "correct": false
              },
              {
                "text": "The forest needs more trees before it can predict",
                "correct": false
              },
              {
                "text": "The cell that creates the model was re-run after the one that fitted it",
                "correct": true
              },
              {
                "text": "The model does not support predict on a test set",
                "correct": false
              }
            ],
            "fbCorrect": "Correct, and this is the Week 2 out-of-order trap arriving in a much more expensive place. Re-running the constructor throws away an hour of fitting. Restart and Run All is how you find out whether your notebook still tells a straight story.",
            "fbWrong": "THE ANSWER: The cell that creates the model was re-run after the one that fitted it. This is the Week 2 out-of-order trap arriving in a much more expensive place. Re-running the constructor throws away an hour of fitting. Restart and Run All is how you find out whether your notebook still tells a straight story.\n\nWhy the others are wrong. \u201cThe test features contain missing values\u201d \u2014 That reports itself as an error about NaN, and it would only arise once the model was fitted.  \u201cThe forest needs more trees before it can predict\u201d \u2014 The number of trees is set at construction and any number can be fitted and used. This one was never fitted.  \u201cThe model does not support predict on a test set\u201d \u2014 It does. The message is specifically that this instance has never been fitted."
          },
          {
            "n": 4,
            "kind": "interpretation",
            "title": "Two outputs from the same forest. The quality manager needs to know why THIS batch was rejected. Which output answers that, and what does the other one tell you?",
            "help": "A   feature_importances_ over the whole training set\n      w_c ratio        0.41\n      curing age       0.29\n      total binder     0.18\n      superplasticiser 0.12\n\nB   contribution to the prediction for batch 812\n      w_c ratio 0.61   pushed toward reject  +0.22\n      curing age 3 d   pushed toward reject  +0.15\n      total binder     pushed toward accept  -0.04",
            "choices": [
              {
                "text": "Both answer it equally well, since they rank the same features",
                "correct": false
              },
              {
                "text": "A answers it, because the highest-importance feature is the reason for any given decision",
                "correct": false
              },
              {
                "text": "B answers it, because it is specific to this case; A describes the model's average behaviour across all cases",
                "correct": true
              },
              {
                "text": "Neither answers it, because a forest can never be explained at all",
                "correct": false
              }
            ],
            "fbCorrect": "Correct, and the distinction is worth holding on to. A global importance chart says what the model relies on in general and can never say why one case came out as it did. A per-case breakdown is what a client's question actually needs.",
            "fbWrong": "THE ANSWER: B answers it, because it is specific to this case; A describes the model's average behaviour across all cases. The distinction is worth holding on to. A global importance chart says what the model relies on in general and can never say why one case came out as it did. A per-case breakdown is what a client's question actually needs.\n\nWhy the others are wrong. \u201cBoth answer it equally well, since they rank the same features\u201d \u2014 They do not even rank them the same way, and more importantly they answer different questions. One is about the model, the other about a case.  \u201cA answers it, because the highest-importance feature is the reason for any given decision\u201d \u2014 That does not follow. The most important feature overall can be unremarkable in this particular case, and here B shows a different feature leading for batch-level reasons.  \u201cNeither answers it, because a forest can never be explained at all\u201d \u2014 Too pessimistic. Per-case attributions like B are exactly how you interrogate one prediction from an ensemble. The honest caveat is that they are estimates of the contribution rather than a rule you can read off."
          },
          {
            "n": 5,
            "kind": "judgement",
            "title": "The quality manager points at one batch and asks: show the exact, directly readable decision rule that rejected batch 812; post-hoc attributions do not meet this audit requirement. You chose the forest. What is the honest position?",
            "help": "",
            "choices": [
              {
                "text": "Show the feature importance chart as the explanation",
                "correct": false
              },
              {
                "text": "Explain that the model is accurate and ask them to trust the result",
                "correct": false
              },
              {
                "text": "Offer to retrain the forest with fewer trees so it is simpler",
                "correct": false
              },
              {
                "text": "Recommend a readable-rule model that meets the stated acceptance requirement",
                "correct": true
              }
            ],
            "fbCorrect": "Correct. The professional answer is to name the limitation and change the recommendation. A stated condition of acceptance that your chosen model cannot meet is a reason to change the model rather than to talk around it.",
            "fbWrong": "THE ANSWER: Recommend a readable-rule model that meets the stated acceptance requirement. The professional answer is to name the limitation and change the recommendation. A stated condition of acceptance that your chosen model cannot meet is a reason to change the model rather than to talk around it.\n\nWhy the others are wrong. \u201cShow the feature importance chart as the explanation\u201d \u2014 Importance describes the model's behaviour across the whole dataset. It cannot say why one case was decided as it was, which is the question you were asked.  \u201cExplain that the model is accurate and ask them to trust the result\u201d \u2014 They told you at the outset that they cannot act on an unexplained call. Asking for trust instead is not an answer.  \u201cOffer to retrain the forest with fewer trees so it is simpler\u201d \u2014 A smaller forest still does not meet this stated requirement for a directly readable rule. This concedes accuracy without gaining explainability."
          }
        ]
      },
      {
        "week": 13,
        "number": 12,
        "title": "CML3112 \u00b7 Weekly Quiz 12 \u2014 Reproducibility (integrative)",
        "intro": "Read what each question shows you. None of them can be answered without it.\n\nHOW THIS WORKS\n\u2022 Answer it now, in the 5 minutes on the screen. That is when this is meant to be taken, while the session is still fresh.\n\u2022 The form then stays open for 24 hours and closes itself. That window is there so a dead network or a broken phone does not cost you a mark you had earned. Take it in the room if you can: by Thursday you will have forgotten the session, and the feedback will be worth less to you.\n\u2022 ONE attempt, from your signed-in Google account. You cannot reopen it or change an answer, so read each question once, properly.\n\u2022 The first box asks for your registration number. It is the number printed on your student card, and it is how the mark reaches your record.\n\u2022 Five questions, one mark each, worth 1% of your final mark.\n\u2022 Your best ten of twelve quizzes count. Missing two costs you nothing, and there are no resits.\n\u2022 When you submit, tap View score. You get a tick or a cross on each question with the feedback underneath. Your mark is the number of ticks, and the feedback on anything you got wrong is the part worth reading.\n\u2022 A question left blank scores the same as one answered wrongly, so answer all five.",
        "questions": [
          {
            "n": 1,
            "kind": "diagnosis",
            "title": "This runs perfectly on the machine it was written on. What is wrong with it?",
            "help": "df = pd.read_csv(\n    \"C:/Users/Jotham/Desktop/concrete_final_v3.csv\")",
            "choices": [
              {
                "text": "It names a location that exists on exactly one computer, so the notebook cannot run anywhere else",
                "correct": true
              },
              {
                "text": "Backslashes should have been used for a Windows path",
                "correct": false
              },
              {
                "text": "The file should be read with a different pandas function",
                "correct": false
              },
              {
                "text": "Nothing, as long as you send the file with the notebook",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. Keep the data inside the project and read it by a relative path such as data/\u2026 so the notebook works for anyone who has the folder. The version marker in the file name is a second warning: it suggests there are other copies and no record of which is current.",
            "fbWrong": "THE ANSWER: It names a location that exists on exactly one computer, so the notebook cannot run anywhere else. Keep the data inside the project and read it by a relative path such as data/\u2026 so the notebook works for anyone who has the folder. The version marker in the file name is a second warning: it suggests there are other copies and no record of which is current.\n\nWhy the others are wrong. \u201cBackslashes should have been used for a Windows path\u201d \u2014 Forward slashes work on Windows in Python and avoid the escape problems backslashes cause. This is the better of the two styles and the location is still wrong.  \u201cThe file should be read with a different pandas function\u201d \u2014 read_csv is the right function for a CSV. The path is the problem.  \u201cNothing, as long as you send the file with the notebook\u201d \u2014 The recipient would have to recreate your user name and your desktop for the path to resolve. A relative path inside the project removes the problem entirely."
          },
          {
            "n": 2,
            "kind": "diagnosis",
            "title": "You run the same notebook twice, changing nothing, and get these two numbers. What is going on, and what should you do?",
            "help": "run 1:   MAE 4.1 MPa\nrun 2:   MAE 4.6 MPa",
            "choices": [
              {
                "text": "The data file is being modified between runs",
                "correct": false
              },
              {
                "text": "The second run is the more trustworthy of the two",
                "correct": false
              },
              {
                "text": "The split and the model involve randomness that was never pinned down",
                "correct": true
              },
              {
                "text": "Report the average of the two runs",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. Without a seed, the rows that land in the test set and the internal choices a forest makes change every run. Set random_state on the split and on the model, and write the number in the notebook so a reader can reproduce your figure exactly.",
            "fbWrong": "THE ANSWER: The split and the model involve randomness that was never pinned down. Without a seed, the rows that land in the test set and the internal choices a forest makes change every run. Set random_state on the split and on the model, and write the number in the notebook so a reader can reproduce your figure exactly.\n\nWhy the others are wrong. \u201cThe data file is being modified between runs\u201d \u2014 Nothing here writes to the file. Unseeded randomness explains this without needing the data to change.  \u201cThe second run is the more trustworthy of the two\u201d \u2014 Neither is more trustworthy. That two runs differ by this much is itself the finding, and it says your single reported figure carries this much uncertainty.  \u201cReport the average of the two runs\u201d \u2014 An average of two arbitrary draws is still arbitrary. Seed the randomness, and if you want a figure with a spread, cross-validate deliberately."
          },
          {
            "n": 3,
            "kind": "traceback",
            "title": "A classmate clones your repository and gets this on the first cell. What is the cause?",
            "help": "Traceback (most recent call last):\n  File \"<ipython-input-1-3e4f5a>\", line 1, in <module>\n    df = pd.read_csv(\"concrete_strength.csv\")\nFileNotFoundError: [Errno 2] No such file or directory:\n'concrete_strength.csv'",
            "choices": [
              {
                "text": "The classmate is missing a package",
                "correct": false
              },
              {
                "text": "The repository was cloned incorrectly",
                "correct": false
              },
              {
                "text": "The data file was never committed, or sits elsewhere",
                "correct": true
              },
              {
                "text": "The file name has the wrong extension",
                "correct": false
              }
            ],
            "fbCorrect": "Correct, and both halves are worth checking. Data is often left out of a repository deliberately because of size or licence, in which case the README has to say where to get it and where to put it. Otherwise the path needs to match the folder layout.",
            "fbWrong": "THE ANSWER: The data file was never committed, or sits elsewhere. Both halves are worth checking. Data is often left out of a repository deliberately because of size or licence, in which case the README has to say where to get it and where to put it. Otherwise the path needs to match the folder layout.\n\nWhy the others are wrong. \u201cThe classmate is missing a package\u201d \u2014 A missing package reports itself as ModuleNotFoundError. This message is about a file.  \u201cThe repository was cloned incorrectly\u201d \u2014 A clone that failed would leave you with no notebook to run. The notebook arrived and its data did not.  \u201cThe file name has the wrong extension\u201d \u2014 The extension matches a CSV read. The file is simply not at that location."
          },
          {
            "n": 4,
            "kind": "interpretation",
            "title": "Two captions for the same chart. Which one does the job a caption exists to do, and why?",
            "help": "A:  Figure 3: strength against cement content.\n\nB:  Figure 3: strength rises with cement content and\n    flattens above 400 kg/m3, so going from 450 to\n    500 kg/m3 buys about 1 MPa.",
            "choices": [
              {
                "text": "Neither; captions should give the data source instead",
                "correct": false
              },
              {
                "text": "A, because a caption should describe the chart and let the reader draw the conclusion",
                "correct": false
              },
              {
                "text": "A, because B might be wrong and the caption would then be misleading",
                "correct": false
              },
              {
                "text": "B, because it states the finding and its size, so a reader who only reads the captions still learns the result",
                "correct": true
              }
            ],
            "fbCorrect": "Correct. A caption is often the only part of your work that gets read. B carries the conclusion and the magnitude, which is what makes it useful and also what makes it checkable against the chart.",
            "fbWrong": "THE ANSWER: B, because it states the finding and its size, so a reader who only reads the captions still learns the result. A caption is often the only part of your work that gets read. B carries the conclusion and the magnitude, which is what makes it useful and also what makes it checkable against the chart.\n\nWhy the others are wrong. \u201cNeither; captions should give the data source instead\u201d \u2014 The source belongs in the caption or nearby and does not replace the finding. B plus a source is the target.  \u201cA, because a caption should describe the chart and let the reader draw the conclusion\u201d \u2014 A describes the axes, which the axis labels already do. It leaves the reader to rediscover something you already know.  \u201cA, because B might be wrong and the caption would then be misleading\u201d \u2014 A claim you can check is a feature. If B is wrong the chart will show it, whereas A cannot be wrong because it says nothing."
          },
          {
            "n": 5,
            "kind": "judgement",
            "title": "Your notebook has three separate cells that each assign df, and nobody wrote down the order they should run in. Submission is tomorrow. What do you do?",
            "help": "",
            "choices": [
              {
                "text": "Leave it, since you know the right order",
                "correct": false
              },
              {
                "text": "Add a comment above each cell saying what order to run them in",
                "correct": false
              },
              {
                "text": "Restart and Run All, then fix whatever breaks until it runs clean from top to bottom",
                "correct": true
              },
              {
                "text": "Delete two of the three cells and hope the notebook still runs",
                "correct": false
              }
            ],
            "fbCorrect": "Correct, and do it before you are tired. That single action converts a notebook that works on your screen into one that works from an empty memory, which is the only version anyone else can use. Consolidating the three assignments into one clear sequence is usually the fix.",
            "fbWrong": "THE ANSWER: Restart and Run All, then fix whatever breaks until it runs clean from top to bottom. Do it before you are tired. That single action converts a notebook that works on your screen into one that works from an empty memory, which is the only version anyone else can use. Consolidating the three assignments into one clear sequence is usually the fix.\n\nWhy the others are wrong. \u201cLeave it, since you know the right order\u201d \u2014 That knowledge is not in the file, so it does not survive you. It also will not survive next week for you either.  \u201cAdd a comment above each cell saying what order to run them in\u201d \u2014 Instructions to run cells out of order are a description of the problem. Anyone who follows them slightly differently gets a different answer.  \u201cDelete two of the three cells and hope the notebook still runs\u201d \u2014 Each of them may be doing something needed. Running from a clean state tells you what is required rather than leaving you to guess."
          }
        ]
      }
    ]
  },
  "CML3113": {
    "meta": {
      "name": "Mining + Petroleum Engineering",
      "day": "Friday 08:00"
    },
    "weeks": [
      {
        "week": 1,
        "number": 1,
        "title": "CML3113 \u00b7 Weekly Quiz 1 \u2014 What machine learning is",
        "intro": "Nothing here can be answered without reading what it shows you.\n\nHOW THIS WORKS\n\u2022 Answer it now, in the 5 minutes on the screen. That is when this is meant to be taken, while the session is still fresh.\n\u2022 The form then stays open for 24 hours and closes itself. That window is there so a dead network or a broken phone does not cost you a mark you had earned. Take it in the room if you can: by Thursday you will have forgotten the session, and the feedback will be worth less to you.\n\u2022 ONE attempt, from your signed-in Google account. You cannot reopen it or change an answer, so read each question once, properly.\n\u2022 The first box asks for your registration number. It is the number printed on your student card, and it is how the mark reaches your record.\n\u2022 Five questions, one mark each, worth 1% of your final mark.\n\u2022 Your best ten of twelve quizzes count. Missing two costs you nothing, and there are no resits.\n\u2022 When you submit, tap View score. You get a tick or a cross on each question with the feedback underneath. Your mark is the number of ticks, and the feedback on anything you got wrong is the part worth reading.\n\u2022 A question left blank scores the same as one answered wrongly, so answer all five.",
        "questions": [
          {
            "n": 1,
            "kind": "interpretation",
            "title": "In the table below, which column is the TARGET?",
            "help": "sample_id  iron_feed  starch_flow  pulp_ph  silica_pct\nS-001           56.3          3180      9.4        2.11\nS-002           58.1          3320      9.6        1.84\nS-003           54.7          2980      9.1        2.63",
            "choices": [
              {
                "text": "silica_pct",
                "correct": true
              },
              {
                "text": "sample_id",
                "correct": false
              },
              {
                "text": "iron_feed",
                "correct": false
              },
              {
                "text": "pulp_ph",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. It is the assay you are waiting an hour for, and the reason for predicting it at all.",
            "fbWrong": "THE ANSWER: silica_pct. It is the assay you are waiting an hour for, and the reason for predicting it at all.\n\nWhy the others are wrong. \u201csample_id\u201d \u2014 That is an identifier. It labels the row and predicts nothing.  \u201ciron_feed\u201d \u2014 That is a feature. You measure it as the feed goes in, before the assay comes back.  \u201cpulp_ph\u201d \u2014 That is a feature: a process variable you already measure continuously."
          },
          {
            "n": 2,
            "kind": "interpretation",
            "title": "You want to predict, for each sample, whether the material is 'ore' or 'waste' against a stated cut-off grade. What kind of problem is this?",
            "help": "",
            "choices": [
              {
                "text": "Classification, because the answer is one of a fixed set of categories",
                "correct": true
              },
              {
                "text": "Regression, because the underlying quantity is a number",
                "correct": false
              },
              {
                "text": "Neither, because it can be written as a rule with thresholds",
                "correct": false
              },
              {
                "text": "Regression, because there are more than two possible answers",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. The answer is a label from a fixed list, so it is classification, and it is scored with a confusion matrix rather than an average error.",
            "fbWrong": "THE ANSWER: Classification, because the answer is one of a fixed set of categories. The answer is a label from a fixed list, so it is classification, and it is scored with a confusion matrix rather than an average error.\n\nWhy the others are wrong. \u201cRegression, because the underlying quantity is a number\u201d \u2014 The underlying quantity is a number, but the question asked is not. You are asked which band or class it falls into, and a band is a category. What decides this is the question you were asked rather than the quantity the sensor happens to record.  \u201cNeither, because it can be written as a rule with thresholds\u201d \u2014 If you already have the strength or the grade then yes, a rule is the right tool and there is nothing to learn. The point here is that you do not have it yet.  \u201cRegression, because there are more than two possible answers\u201d \u2014 The number of possible answers does not decide this. Classification with three classes is still classification."
          },
          {
            "n": 3,
            "kind": "diagnosis",
            "title": "A team proposes to predict the target using the list of columns below. One column makes the whole exercise meaningless. Which one, and why?",
            "help": "target:   whether the concentrate met specification\nfeatures: iron_feed, starch_flow, pulp_ph,\n          laboratory_silica_assay",
            "choices": [
              {
                "text": "laboratory_silica_assay \u2014 it IS the answer, and it is the thing you were waiting an hour for",
                "correct": true
              },
              {
                "text": "None of them; the list is fine",
                "correct": false
              },
              {
                "text": "starch_flow \u2014 reagent flow is set by the operator, not measured",
                "correct": false
              },
              {
                "text": "pulp_ph \u2014 it is controlled to a set point so it barely varies",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. Ask the timing question: at the moment I need the prediction, would I have this number? The assay is exactly what you do not have yet, which was the whole point.",
            "fbWrong": "THE ANSWER: laboratory_silica_assay \u2014 it IS the answer, and it is the thing you were waiting an hour for. Ask the timing question: at the moment I need the prediction, would I have this number? The assay is exactly what you do not have yet, which was the whole point.\n\nWhy the others are wrong. \u201cNone of them; the list is fine\u201d \u2014 One of these columns is the laboratory result you are trying to predict. Ask the timing question of each one.  \u201cstarch_flow \u2014 reagent flow is set by the operator, not measured\u201d \u2014 A set value is still a legitimate input known at prediction time. Provenance matters, but this one is not fatal.  \u201cpulp_ph \u2014 it is controlled to a set point so it barely varies\u201d \u2014 A column with little variation contributes little, and that is worth noticing. It does not invalidate the exercise."
          },
          {
            "n": 4,
            "kind": "interpretation",
            "title": "An economic calculation gives the cut-off grade, and you have the assayed grade for every block. What should you build?",
            "help": "",
            "choices": [
              {
                "text": "Either; the choice is a matter of preference",
                "correct": false
              },
              {
                "text": "A regression model to predict the threshold",
                "correct": false
              },
              {
                "text": "A classifier trained on past decisions",
                "correct": false
              },
              {
                "text": "A rule with a threshold, written directly in code",
                "correct": true
              }
            ],
            "fbCorrect": "Correct. You have the input and you have the threshold, so there is nothing to learn. Training a model to rediscover a published limit adds error and removes the audit trail.",
            "fbWrong": "THE ANSWER: A rule with a threshold, written directly in code. You have the input and you have the threshold, so there is nothing to learn. Training a model to rediscover a published limit adds error and removes the audit trail.\n\nWhy the others are wrong. \u201cEither; the choice is a matter of preference\u201d \u2014 The choice follows from whether you already have the input and the threshold. Here you have both, so the rule wins on every axis.  \u201cA regression model to predict the threshold\u201d \u2014 The threshold is given. There is nothing to predict about it.  \u201cA classifier trained on past decisions\u201d \u2014 It would work, and that is what makes this tempting. It would also be less accurate than the rule, harder to defend and impossible to audit against the code of practice."
          },
          {
            "n": 5,
            "kind": "judgement",
            "title": "A client will only accept a system if every decision it makes can be explained line by line to a regulator. Two candidate approaches perform identically on your data. Which do you recommend, and on what grounds?",
            "help": "",
            "choices": [
              {
                "text": "The more sophisticated one, because it will generalise better",
                "correct": false
              },
              {
                "text": "Whichever scored fractionally higher on the test set",
                "correct": false
              },
              {
                "text": "The one whose decisions can be read out and traced, because the constraint decides it once performance is equal",
                "correct": true
              },
              {
                "text": "Neither; tell the client the constraint is unreasonable",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. When performance is equal the constraint is the deciding criterion, and explainability was stated as a condition of acceptance rather than a preference.",
            "fbWrong": "THE ANSWER: The one whose decisions can be read out and traced, because the constraint decides it once performance is equal. When performance is equal the constraint is the deciding criterion, and explainability was stated as a condition of acceptance rather than a preference.\n\nWhy the others are wrong. \u201cThe more sophisticated one, because it will generalise better\u201d \u2014 Sophistication does not imply generalisation, and on equal performance there is no evidence for the claim. It also ignores the constraint you were given.  \u201cWhichever scored fractionally higher on the test set\u201d \u2014 A fractional difference on one test set is usually inside the noise, and Week 10 shows you how to measure that. Even a real difference would not override a stated condition of acceptance.  \u201cNeither; tell the client the constraint is unreasonable\u201d \u2014 Regulatory explainability is a normal engineering constraint. Part of the job is delivering within it."
          }
        ]
      },
      {
        "week": 2,
        "number": 2,
        "title": "CML3113 \u00b7 Weekly Quiz 2 \u2014 Notebooks and version control",
        "intro": "Read what each question shows you. None of them can be answered without it.\n\nHOW THIS WORKS\n\u2022 Answer it now, in the 5 minutes on the screen. That is when this is meant to be taken, while the session is still fresh.\n\u2022 The form then stays open for 24 hours and closes itself. That window is there so a dead network or a broken phone does not cost you a mark you had earned. Take it in the room if you can: by Thursday you will have forgotten the session, and the feedback will be worth less to you.\n\u2022 ONE attempt, from your signed-in Google account. You cannot reopen it or change an answer, so read each question once, properly.\n\u2022 The first box asks for your registration number. It is the number printed on your student card, and it is how the mark reaches your record.\n\u2022 Five questions, one mark each, worth 1% of your final mark.\n\u2022 Your best ten of twelve quizzes count. Missing two costs you nothing, and there are no resits.\n\u2022 When you submit, tap View score. You get a tick or a cross on each question with the feedback underneath. Your mark is the number of ticks, and the feedback on anything you got wrong is the part worth reading.\n\u2022 A question left blank scores the same as one answered wrongly, so answer all five.",
        "questions": [
          {
            "n": 1,
            "kind": "interpretation",
            "title": "The numbers in the square brackets are the order the cells were actually run. The notebook now reads as shown. Why does it print 10?",
            "help": "In [1]:  holes_logged = 40\nIn [2]:  target = 30\nIn [5]:  holes_logged = 55\nIn [3]:  ahead = holes_logged - target\nIn [4]:  print(ahead)\n         10",
            "choices": [
              {
                "text": "The variable was never given the second value at all",
                "correct": false
              },
              {
                "text": "Python read the cells from the top of the page downwards",
                "correct": false
              },
              {
                "text": "The notebook cached the printed output and did not refresh it",
                "correct": false
              },
              {
                "text": "The subtraction ran while the first value was still in memory, and the cell that replaced it ran afterwards",
                "correct": true
              }
            ],
            "fbCorrect": "Correct. Read the bracket numbers as a timeline: 1, 2, 3, 4, then 5. The subtraction happened at step 3 on the old value, and the replacement only happened at step 5. What you see on screen is the code; what produced the 10 is the order it ran.",
            "fbWrong": "THE ANSWER: The subtraction ran while the first value was still in memory, and the cell that replaced it ran afterwards. Read the bracket numbers as a timeline: 1, 2, 3, 4, then 5. The subtraction happened at step 3 on the old value, and the replacement only happened at step 5. What you see on screen is the code; what produced the 10 is the order it ran.\n\nWhy the others are wrong. \u201cThe variable was never given the second value at all\u201d \u2014 It was, at step 5. That is precisely why the code on screen and the number underneath it disagree.  \u201cPython read the cells from the top of the page downwards\u201d \u2014 That is the assumption this question exists to break. A notebook runs cells in whatever order you click them, and the bracket numbers are the record of that order.  \u201cThe notebook cached the printed output and did not refresh it\u201d \u2014 Notebooks do keep an old output on screen after you edit a cell, but the value here was genuinely computed from the earlier number. Nothing is stale about the 10 itself."
          },
          {
            "n": 2,
            "kind": "interpretation",
            "title": "Read the two states below. What has Restart and Run All established?",
            "help": "before:  In [7]  In [3]  In [12]  In [4]  In [9]\n         (outputs on screen, run in some past order)\n\nafter:   In [1]  In [2]  In [3]   In [4]  In [5]\n         (no errors, and the same outputs as before)",
            "choices": [
              {
                "text": "That the notebook will run on a classmate's machine",
                "correct": false
              },
              {
                "text": "That the code is correct",
                "correct": false
              },
              {
                "text": "That it produces those outputs from an empty memory, in page order",
                "correct": true
              },
              {
                "text": "That the results are statistically reliable",
                "correct": false
              }
            ],
            "fbCorrect": "Correct, and that is a narrow claim worth having. The counts now run 1 to 5 in page order, which rules out the out-of-order trap and any variable that only survived because of a cell you later deleted.",
            "fbWrong": "THE ANSWER: That it produces those outputs from an empty memory, in page order. That is a narrow claim worth having. The counts now run 1 to 5 in page order, which rules out the out-of-order trap and any variable that only survived because of a cell you later deleted.\n\nWhy the others are wrong. \u201cThat the notebook will run on a classmate's machine\u201d \u2014 That needs the same packages, the same Python version and the data file reachable at the same relative path. Week 13 is about exactly this gap.  \u201cThat the code is correct\u201d \u2014 It establishes that the code runs and reproduces its own outputs. Code can run cleanly from top to bottom and still compute the wrong quantity, which is what the diagnosis questions from Week 3 onwards are about.  \u201cThat the results are statistically reliable\u201d \u2014 Reproducing an output says nothing about whether the number was worth computing. A notebook can faithfully reproduce a meaningless average every time you run it."
          },
          {
            "n": 3,
            "kind": "traceback",
            "title": "You have been working for an hour, the variable is plainly assigned in a cell further up the page, and running the cell at the bottom gives this. What is the most likely cause?",
            "help": "Traceback (most recent call last):\n  File \"<ipython-input-2-a1b2c3>\", line 1, in <module>\n    print(mean_rop)\nNameError: name 'mean_rop' is not defined",
            "choices": [
              {
                "text": "The name is a reserved word in Python",
                "correct": false
              },
              {
                "text": "The notebook needs a library imported before it can print",
                "correct": false
              },
              {
                "text": "The variable holds nothing, so printing it fails",
                "correct": false
              },
              {
                "text": "The cell that creates it has not actually been run in this session, whatever the page shows",
                "correct": true
              }
            ],
            "fbCorrect": "Correct. Being written on the page and having been executed are different things: the kernel only knows what it has run. Either that cell was never run, or the kernel was restarted since. Restart and Run All settles it in one step.",
            "fbWrong": "THE ANSWER: The cell that creates it has not actually been run in this session, whatever the page shows. Being written on the page and having been executed are different things: the kernel only knows what it has run. Either that cell was never run, or the kernel was restarted since. Restart and Run All settles it in one step.\n\nWhy the others are wrong. \u201cThe name is a reserved word in Python\u201d \u2014 It is an ordinary name. A reserved word would be reported as a SyntaxError while the cell was being read, before it ran.  \u201cThe notebook needs a library imported before it can print\u201d \u2014 print is built in and needs no import. A missing library reports itself as ModuleNotFoundError.  \u201cThe variable holds nothing, so printing it fails\u201d \u2014 A variable holding nothing still exists and prints happily as None. This error says the name itself is unknown to Python."
          },
          {
            "n": 4,
            "kind": "interpretation",
            "title": "Read this output. Which statement is true?",
            "help": "$ git status\nOn branch main\nChanges not staged for commit:\n        modified:   analysis.ipynb\nUntracked files:\n        data/drill_shift_log.csv",
            "choices": [
              {
                "text": "The repository is broken and needs to be created again",
                "correct": false
              },
              {
                "text": "The notebook has been committed and the CSV has been deleted",
                "correct": false
              },
              {
                "text": "Both files will be saved by the next commit",
                "correct": false
              },
              {
                "text": "The notebook is tracked and edited; the CSV was never added",
                "correct": true
              }
            ],
            "fbCorrect": "Correct. Git reports a tracked file as modified and a file it has never seen as untracked. Stage the notebook edit with git add before committing. A bare commit saves neither file here.",
            "fbWrong": "THE ANSWER: The notebook is tracked and edited; the CSV was never added. Git reports a tracked file as modified and a file it has never seen as untracked. Stage the notebook edit with git add before committing. A bare commit saves neither file here.\n\nWhy the others are wrong. \u201cThe repository is broken and needs to be created again\u201d \u2014 This is the ordinary output of a healthy repository with work in progress. It is the state you should expect to see most of the time.  \u201cThe notebook has been committed and the CSV has been deleted\u201d \u2014 A committed file with no further edits does not appear in this output at all, and a deletion is reported as deleted.  \u201cBoth files will be saved by the next commit\u201d \u2014 Neither will. The notebook change is unstaged and the CSV is untracked, so a bare commit captures nothing from this list."
          },
          {
            "n": 5,
            "kind": "judgement",
            "title": "It is twenty minutes before the session. The Python install on your laptop fails with an error you have not seen before. What is the right move?",
            "help": "",
            "choices": [
              {
                "text": "Open Colab in the browser and work there for the session",
                "correct": true
              },
              {
                "text": "Copy a classmate's notebook afterwards and read through it",
                "correct": false
              },
              {
                "text": "Spend the session fixing the install so the rest of the semester is smooth",
                "correct": false
              },
              {
                "text": "Ask for the session to be repeated later in the week",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. Colab needs a browser and nothing else, which is why this course is built on it. Your install can be repaired at a time when it is not costing you a three-hour session.",
            "fbWrong": "THE ANSWER: Open Colab in the browser and work there for the session. Colab needs a browser and nothing else, which is why this course is built on it. Your install can be repaired at a time when it is not costing you a three-hour session.\n\nWhy the others are wrong. \u201cCopy a classmate's notebook afterwards and read through it\u201d \u2014 Reading someone else's finished notebook skips the part that does the teaching. You would arrive at Week 3 without having run a single cell yourself.  \u201cSpend the session fixing the install so the rest of the semester is smooth\u201d \u2014 This trades a guaranteed three hours of teaching for a repair of unknown length. Install problems are often version mismatches with no quick fix, which is why the browser route exists.  \u201cAsk for the session to be repeated later in the week\u201d \u2014 There is no second slot: each cohort meets once a week. A working browser removes the problem in under a minute."
          }
        ]
      },
      {
        "week": 3,
        "number": 3,
        "title": "CML3113 \u00b7 Weekly Quiz 3 \u2014 Python as an engineering calculator",
        "intro": "Read what each question shows you. None of them can be answered without it.\n\nHOW THIS WORKS\n\u2022 Answer it now, in the 5 minutes on the screen. That is when this is meant to be taken, while the session is still fresh.\n\u2022 The form then stays open for 24 hours and closes itself. That window is there so a dead network or a broken phone does not cost you a mark you had earned. Take it in the room if you can: by Thursday you will have forgotten the session, and the feedback will be worth less to you.\n\u2022 ONE attempt, from your signed-in Google account. You cannot reopen it or change an answer, so read each question once, properly.\n\u2022 The first box asks for your registration number. It is the number printed on your student card, and it is how the mark reaches your record.\n\u2022 Five questions, one mark each, worth 1% of your final mark.\n\u2022 Your best ten of twelve quizzes count. Missing two costs you nothing, and there are no resits.\n\u2022 When you submit, tap View score. You get a tick or a cross on each question with the feedback underneath. Your mark is the number of ticks, and the feedback on anything you got wrong is the part worth reading.\n\u2022 A question left blank scores the same as one answered wrongly, so answer all five.",
        "questions": [
          {
            "n": 1,
            "kind": "diagnosis",
            "title": "This runs without any error and prints the number shown. What is wrong?",
            "help": "def contained_metal(tonnes, grade_pct):\n    return tonnes * grade_pct / 100.0\n\nmetal = contained_metal(250000.0, 1800)\nprint(f\"{metal:,.0f} t of contained metal\")\n\n4,500,000 t of contained metal",
            "choices": [
              {
                "text": "The grade was passed in grams per tonne to a parameter measured in per cent",
                "correct": true
              },
              {
                "text": "The division by 100 should not be there",
                "correct": false
              },
              {
                "text": "Nothing is wrong; high-grade ore gives large tonnages",
                "correct": false
              },
              {
                "text": "The thousands separator in the format string is wrong",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. 1800 g/t is 0.18 per cent, and the right answer is 450 t. The output claims more metal than the ore tonnage that contains it, which is impossible and is the tell.",
            "fbWrong": "THE ANSWER: The grade was passed in grams per tonne to a parameter measured in per cent. 1800 g/t is 0.18 per cent, and the right answer is 450 t. The output claims more metal than the ore tonnage that contains it, which is impossible and is the tell.\n\nWhy the others are wrong. \u201cThe division by 100 should not be there\u201d \u2014 The division by 100 is what converts a percentage into a fraction, and it belongs there. The value handed in was never a percentage.  \u201cNothing is wrong; high-grade ore gives large tonnages\u201d \u2014 You cannot recover 4.5 million tonnes of metal from 250,000 tonnes of rock. Compare the answer with the input before believing it.  \u201cThe thousands separator in the format string is wrong\u201d \u2014 The formatting is fine. A correctly formatted impossible number is still impossible."
          },
          {
            "n": 2,
            "kind": "diagnosis",
            "title": "This function runs without error. The printed answer is wrong and dangerous. Why?",
            "help": "def grade_action(grade_pct, cutoff_pct):\n    if grade_pct >= cutoff_pct * 0.8:\n        return \"stockpile\"\n    elif grade_pct >= cutoff_pct * 1.5:\n        return \"mill now\"\n    elif grade_pct >= cutoff_pct:\n        return \"mill\"\n    else:\n        return \"waste\"\n\nprint(grade_action(1.2, 0.5))\nstockpile",
            "choices": [
              {
                "text": "The comparisons should be strictly greater than",
                "correct": false
              },
              {
                "text": "Cut-off grade should be a fixed number in the function",
                "correct": false
              },
              {
                "text": "The multipliers 0.8 and 1.5 are the wrong way round",
                "correct": false
              },
              {
                "text": "The lowest threshold is tested first, so high-grade ore matches the stockpile branch and never reaches mill now",
                "correct": true
              }
            ],
            "fbCorrect": "Correct. 1.2 is above 0.4, so the first branch returns and ore worth milling immediately gets sent to a stockpile. At a cut-off of 0.5 this material is above 1.5 times cut-off and should return mill now.",
            "fbWrong": "THE ANSWER: The lowest threshold is tested first, so high-grade ore matches the stockpile branch and never reaches mill now. 1.2 is above 0.4, so the first branch returns and ore worth milling immediately gets sent to a stockpile. At a cut-off of 0.5 this material is above 1.5 times cut-off and should return mill now.\n\nWhy the others are wrong. \u201cThe comparisons should be strictly greater than\u201d \u2014 At 1.2 against a cut-off of 0.5 no boundary is hit exactly, so this would change nothing here.  \u201cCut-off grade should be a fixed number in the function\u201d \u2014 Passing it in is the better design, because cut-off moves with the metal price. That is unrelated to this wrong answer.  \u201cThe multipliers 0.8 and 1.5 are the wrong way round\u201d \u2014 Those multipliers describe the intended bands correctly: 0.8 of cut-off for marginal material, 1.5 for high grade. The sequence of the tests is the fault."
          },
          {
            "n": 3,
            "kind": "traceback",
            "title": "What does this tell you about the variable?",
            "help": "Traceback (most recent call last):\n  File \"<ipython-input-5-9f8e7d>\", line 2, in <module>\n    total_depth = depth + 2.5\nTypeError: can only concatenate str (not \"float\") to str",
            "choices": [
              {
                "text": "The 2.5 should have been written as an integer",
                "correct": false
              },
              {
                "text": "It holds a number that is too large for the addition",
                "correct": false
              },
              {
                "text": "The variable was never assigned a value",
                "correct": false
              },
              {
                "text": "It holds text, so the plus sign was read as joining strings and a number cannot be joined to text",
                "correct": true
              }
            ],
            "fbCorrect": "Correct. The word concatenate is the clue: Python was trying to stick things together rather than add them. Values typed in or read from a file arrive as text, and float() converts them.",
            "fbWrong": "THE ANSWER: It holds text, so the plus sign was read as joining strings and a number cannot be joined to text. The word concatenate is the clue: Python was trying to stick things together rather than add them. Values typed in or read from a file arrive as text, and float() converts them.\n\nWhy the others are wrong. \u201cThe 2.5 should have been written as an integer\u201d \u2014 Adding an integer to text fails in exactly the same way. The type of the variable is what has to change.  \u201cIt holds a number that is too large for the addition\u201d \u2014 Python integers grow as large as memory allows, and floats would report an overflow differently. The message names the type as str.  \u201cThe variable was never assigned a value\u201d \u2014 That reports itself as a NameError. This variable exists and holds something; the something is text."
          },
          {
            "n": 4,
            "kind": "interpretation",
            "title": "Reading this function as written, what does the call return?",
            "help": "def grade_action(grade_pct, cutoff_pct):\n    if grade_pct >= cutoff_pct * 1.5:\n        return \"mill now\"\n    elif grade_pct >= cutoff_pct:\n        return \"mill\"\n    elif grade_pct >= cutoff_pct * 0.8:\n        return \"stockpile\"\n    else:\n        return \"waste\"\n\ngrade_action(0.45, 0.50)",
            "choices": [
              {
                "text": "waste",
                "correct": false
              },
              {
                "text": "mill",
                "correct": false
              },
              {
                "text": "mill now",
                "correct": false
              },
              {
                "text": "stockpile",
                "correct": true
              }
            ],
            "fbCorrect": "Correct. 0.45 is below the 0.50 cut-off so it is not ore, and it is above 0.8 of cut-off which is 0.40, so it is marginal material worth keeping rather than dumping.",
            "fbWrong": "THE ANSWER: stockpile. 0.45 is below the 0.50 cut-off so it is not ore, and it is above 0.8 of cut-off which is 0.40, so it is marginal material worth keeping rather than dumping.\n\nWhy the others are wrong. \u201cwaste\u201d \u2014 Waste is what falls below 0.8 of cut-off, which is 0.40. At 0.45 this material clears that test.  \u201cmill\u201d \u2014 That branch needs the grade to reach the cut-off of 0.50. This grade is 0.45.  \u201cmill now\u201d \u2014 That branch needs 1.5 times cut-off, which is 0.75."
          },
          {
            "n": 5,
            "kind": "judgement",
            "title": "A teammate has written the 3 per cent silica specification directly into three different cells. The code works. What should you do?",
            "help": "",
            "choices": [
              {
                "text": "Ask each teammate to remember which cells contain it",
                "correct": false
              },
              {
                "text": "Leave it, because the code produces the right answers today",
                "correct": false
              },
              {
                "text": "Write a function that looks the limit up online each time",
                "correct": false
              },
              {
                "text": "Put it in one named constant and refer to that everywhere",
                "correct": true
              }
            ],
            "fbCorrect": "Correct. When the standard is revised you change one line and can point to it. Three copies means three chances to update two of them and ship a notebook that applies two different limits in the same analysis.",
            "fbWrong": "THE ANSWER: Put it in one named constant and refer to that everywhere. When the standard is revised you change one line and can point to it. Three copies means three chances to update two of them and ship a notebook that applies two different limits in the same analysis.\n\nWhy the others are wrong. \u201cAsk each teammate to remember which cells contain it\u201d \u2014 Relying on memory across a fifteen-week project with several people is how the two-out-of-three update happens.  \u201cLeave it, because the code produces the right answers today\u201d \u2014 It does work today. The cost arrives on the day the figure changes, and it arrives as an inconsistency nobody notices because every cell still runs.  \u201cWrite a function that looks the limit up online each time\u201d \u2014 That makes the notebook depend on a network and on somebody else's page layout. A named constant with a comment citing the clause is auditable and works offline."
          }
        ]
      },
      {
        "week": 4,
        "number": 4,
        "title": "CML3113 \u00b7 Weekly Quiz 4 \u2014 Collections, loops and files",
        "intro": "Read what each question shows you. None of them can be answered without it.\n\nHOW THIS WORKS\n\u2022 Answer it now, in the 5 minutes on the screen. That is when this is meant to be taken, while the session is still fresh.\n\u2022 The form then stays open for 24 hours and closes itself. That window is there so a dead network or a broken phone does not cost you a mark you had earned. Take it in the room if you can: by Thursday you will have forgotten the session, and the feedback will be worth less to you.\n\u2022 ONE attempt, from your signed-in Google account. You cannot reopen it or change an answer, so read each question once, properly.\n\u2022 The first box asks for your registration number. It is the number printed on your student card, and it is how the mark reaches your record.\n\u2022 Five questions, one mark each, worth 1% of your final mark.\n\u2022 Your best ten of twelve quizzes count. Missing two costs you nothing, and there are no resits.\n\u2022 When you submit, tap View score. You get a tick or a cross on each question with the feedback underneath. Your mark is the number of ticks, and the feedback on anything you got wrong is the part worth reading.\n\u2022 A question left blank scores the same as one answered wrongly, so answer all five.",
        "questions": [
          {
            "n": 1,
            "kind": "diagnosis",
            "title": "This runs cleanly and prints the mean shown. The mean is wrong. What causes it?",
            "help": "rates = [7.2, 9.5, 8.1, 6.4]\ntotal = 0.0\nfor r in rates:\n    total = 0.0\n    total = total + r\n\nprint(f\"mean rate {total / len(rates):.3f} m/h\")\nmean rate 1.600 m/h",
            "choices": [
              {
                "text": "The reset to zero sits inside the loop, so only the last value survives",
                "correct": true
              },
              {
                "text": "The loop variable has the same name as one of the rates",
                "correct": false
              },
              {
                "text": "Adding floats accumulates rounding error",
                "correct": false
              },
              {
                "text": "The list should have been a dictionary",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. The running total is wiped on every pass, leaving 6.4, and 6.4 divided by 4 is 1.600. The true mean is 7.800 m/h. Move the reset above the loop.",
            "fbWrong": "THE ANSWER: The reset to zero sits inside the loop, so only the last value survives. The running total is wiped on every pass, leaving 6.4, and 6.4 divided by 4 is 1.600. The true mean is 7.800 m/h. Move the reset above the loop.\n\nWhy the others are wrong. \u201cThe loop variable has the same name as one of the rates\u201d \u2014 The loop variable is r and the list is rates, so nothing is shadowed. Even if it were, that would not empty the running total on every pass.  \u201cAdding floats accumulates rounding error\u201d \u2014 Float rounding would appear in the far decimals. This answer is out by a factor of nearly five.  \u201cThe list should have been a dictionary\u201d \u2014 A list is the right structure for a sequence of readings."
          },
          {
            "n": 2,
            "kind": "diagnosis",
            "title": "This prints a count that is one too low on this file. Why?",
            "help": "rates = [9.1, 8.6, 7.2, 8.3]\nTARGET = 8.0\nover = 0\nfor i in range(1, len(rates)):\n    if rates[i] > TARGET:\n        over = over + 1\n\nprint(f\"{over} holes above target rate\")\n2 holes above target rate",
            "choices": [
              {
                "text": "The range starts at 1, so the first hole is never tested",
                "correct": true
              },
              {
                "text": "The counter should start at 1",
                "correct": false
              },
              {
                "text": "The comparison should be greater-than-or-equal",
                "correct": false
              },
              {
                "text": "The range stops one short of the end of the list",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. range(1, 4) skips position 0, which holds 9.1. Three holes beat the 8.0 m/h target. Loop over the values directly and the question of where to start disappears.",
            "fbWrong": "THE ANSWER: The range starts at 1, so the first hole is never tested. Range(1, 4) skips position 0, which holds 9.1. Three holes beat the 8.0 m/h target. Loop over the values directly and the question of where to start disappears.\n\nWhy the others are wrong. \u201cThe counter should start at 1\u201d \u2014 A count starts at nothing. Pre-loading it to 1 would mask this bug rather than fix it.  \u201cThe comparison should be greater-than-or-equal\u201d \u2014 No rate here equals 8.0 exactly, so that would change nothing.  \u201cThe range stops one short of the end of the list\u201d \u2014 It reaches position 3, the last of four. The skipped element is the first one."
          },
          {
            "n": 3,
            "kind": "traceback",
            "title": "You are reading a 300-row file and it stops partway through with this. What has happened, and what should the loop do about it?",
            "help": "Traceback (most recent call last):\n  File \"<ipython-input-7-4c5d6e>\", line 4, in <module>\n    if float(row[\"rate_of_penetration\"]) > TARGET:\nValueError: could not convert string to float: ''",
            "choices": [
              {
                "text": "That field is empty in one row, so the loop should skip that row and count how many it skipped",
                "correct": true
              },
              {
                "text": "The whole file is corrupted and cannot be used",
                "correct": false
              },
              {
                "text": "The empty value should be replaced with zero so the loop can continue",
                "correct": false
              },
              {
                "text": "The column name is spelled wrongly",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. The two quote marks with nothing between them are an empty string. Skipping is the right response and the count of skips belongs in your report, because it tells the reader how much of the file the answer actually covers.",
            "fbWrong": "THE ANSWER: That field is empty in one row, so the loop should skip that row and count how many it skipped. The two quote marks with nothing between them are an empty string. Skipping is the right response and the count of skips belongs in your report, because it tells the reader how much of the file the answer actually covers.\n\nWhy the others are wrong. \u201cThe whole file is corrupted and cannot be used\u201d \u2014 One blank field in one row says nothing about the other 299. Handle the gap and carry on.  \u201cThe empty value should be replaced with zero so the loop can continue\u201d \u2014 This is the trap. Zero is a real measurement, so substituting it silently drags every average downwards. Week 6 is largely about the damage this does.  \u201cThe column name is spelled wrongly\u201d \u2014 A wrong column name raises a KeyError before any conversion is attempted. The column was found; its content was empty."
          },
          {
            "n": 4,
            "kind": "interpretation",
            "title": "Your script prints this summary. Which statement does it support?",
            "help": "rows in file      300\nrows used         287\nrows skipped       13\nmean rate         8.40 m/h",
            "choices": [
              {
                "text": "The mean describes the 287 usable rows, and the other 13 need explaining",
                "correct": true
              },
              {
                "text": "Losing 13 rows out of 300 is too small to mention",
                "correct": false
              },
              {
                "text": "The 13 skipped rows were duplicates",
                "correct": false
              },
              {
                "text": "The mean describes all 300 rows in the file",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. A mean is only ever a mean of what went into it. If the 13 gaps are scattered at random the figure is probably fine; if they share a cause the figure is biased and the count is your only warning.",
            "fbWrong": "THE ANSWER: The mean describes the 287 usable rows, and the other 13 need explaining. A mean is only ever a mean of what went into it. If the 13 gaps are scattered at random the figure is probably fine; if they share a cause the figure is biased and the count is your only warning.\n\nWhy the others are wrong. \u201cLosing 13 rows out of 300 is too small to mention\u201d \u2014 The size of the loss is not what matters; the reason is. Thirteen gaps from one source can move a mean further than fifty scattered at random.  \u201cThe 13 skipped rows were duplicates\u201d \u2014 The summary says they were skipped and does not say why. Duplicates are a separate problem, and one you meet in Week 6.  \u201cThe mean describes all 300 rows in the file\u201d \u2014 Thirteen rows contributed nothing to it. Reporting it as a figure for the file overstates what you measured."
          },
          {
            "n": 5,
            "kind": "judgement",
            "title": "You look at the 13 skipped rows and every one of them comes from the same shift. What should you do before reporting the mean?",
            "help": "",
            "choices": [
              {
                "text": "Report the mean and mention the 13 skips in a footnote",
                "correct": false
              },
              {
                "text": "Fill the gaps with that source's own average so no rows are lost",
                "correct": false
              },
              {
                "text": "Drop that source entirely and report the rest",
                "correct": false
              },
              {
                "text": "Investigate the shared cause first, because gaps that cluster in one source point at how the data was collected",
                "correct": true
              }
            ],
            "fbCorrect": "Correct. Thirteen blanks spread across the file is untidiness. Thirteen blanks from one source is a finding, and it may matter more than the mean you were asked for.",
            "fbWrong": "THE ANSWER: Investigate the shared cause first, because gaps that cluster in one source point at how the data was collected. Thirteen blanks spread across the file is untidiness. Thirteen blanks from one source is a finding, and it may matter more than the mean you were asked for.\n\nWhy the others are wrong. \u201cReport the mean and mention the 13 skips in a footnote\u201d \u2014 Reporting the count is necessary and it is not sufficient here. A footnote presents a systematic gap as though it were random noise.  \u201cFill the gaps with that source's own average so no rows are lost\u201d \u2014 That invents readings from the one source you have reason to distrust, and it hides the pattern you just found.  \u201cDrop that source entirely and report the rest\u201d \u2014 That might end up being right, and it is a decision to take after you understand the cause. Removing a source before knowing why it failed can delete the very thing under investigation."
          }
        ]
      },
      {
        "week": 5,
        "number": 5,
        "title": "CML3113 \u00b7 Weekly Quiz 5 \u2014 pandas, and judging a dataset",
        "intro": "Read what each question shows you. None of them can be answered without it.\n\nHOW THIS WORKS\n\u2022 Answer it now, in the 5 minutes on the screen. That is when this is meant to be taken, while the session is still fresh.\n\u2022 The form then stays open for 24 hours and closes itself. That window is there so a dead network or a broken phone does not cost you a mark you had earned. Take it in the room if you can: by Thursday you will have forgotten the session, and the feedback will be worth less to you.\n\u2022 ONE attempt, from your signed-in Google account. You cannot reopen it or change an answer, so read each question once, properly.\n\u2022 The first box asks for your registration number. It is the number printed on your student card, and it is how the mark reaches your record.\n\u2022 Five questions, one mark each, worth 1% of your final mark.\n\u2022 Your best ten of twelve quizzes count. Missing two costs you nothing, and there are no resits.\n\u2022 When you submit, tap View score. You get a tick or a cross on each question with the feedback underneath. Your mark is the number of ticks, and the feedback on anything you got wrong is the part worth reading.\n\u2022 A question left blank scores the same as one answered wrongly, so answer all five.",
        "questions": [
          {
            "n": 1,
            "kind": "diagnosis",
            "title": "You wanted the number of records above the threshold. This prints the whole row count instead. Why?",
            "help": "mask = df[\"silica_concentrate\"] > 3\nprint(len(mask))\n20000\nprint(mask.sum())\n4120",
            "choices": [
              {
                "text": "The comparison was written the wrong way round",
                "correct": false
              },
              {
                "text": "len() does not work on pandas objects",
                "correct": false
              },
              {
                "text": "The mask holds one True or False per row, so its length is the row count",
                "correct": true
              },
              {
                "text": "The threshold is too low, so every row qualifies",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. A comparison on a column answers the question for every row and hands back all the answers, so it is always as long as the frame. mask.sum() counts the True entries, as the second line shows, and len(df[mask]) counts the rows you keep.",
            "fbWrong": "THE ANSWER: The mask holds one True or False per row, so its length is the row count. A comparison on a column answers the question for every row and hands back all the answers, so it is always as long as the frame. mask.sum() counts the True entries, as the second line shows, and len(df[mask]) counts the rows you keep.\n\nWhy the others are wrong. \u201cThe comparison was written the wrong way round\u201d \u2014 Reversing it would produce a different set of True entries and the same length. Length is the wrong measurement to be taking.  \u201clen() does not work on pandas objects\u201d \u2014 It works and it reported the truth. The truth it reported answers a different question from the one you asked.  \u201cThe threshold is too low, so every row qualifies\u201d \u2014 The second line rules this out: the sum is well below the row count, so most rows do not qualify. Notice also that the length would have been the row count either way, which is what makes it the wrong thing to measure."
          },
          {
            "n": 2,
            "kind": "diagnosis",
            "title": "The maximum below is far too small and no error was raised. What has happened?",
            "help": "print(df[\"iron_feed\"].dtype)\nobject\n\nprint(df[\"iron_feed\"].max())\n9.9\n\n# the file contains values such as 56.3, 41.2, 9.9, 28.0",
            "choices": [
              {
                "text": "The largest values are stored in a different column",
                "correct": false
              },
              {
                "text": "The column holds text, so the maximum was decided alphabetically and a value starting with 9 wins",
                "correct": true
              },
              {
                "text": "max() needs the column sorted first",
                "correct": false
              },
              {
                "text": "The column contains missing values that max() skipped",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. object dtype means the column is text. Compared as text, \"9.9\" beats \"41.2\" because the character 9 comes after 4. Convert with pd.to_numeric and the real maximum appears. One stray value with a unit or a stray space is usually what forced the whole column to text.",
            "fbWrong": "THE ANSWER: The column holds text, so the maximum was decided alphabetically and a value starting with 9 wins. Object dtype means the column is text. Compared as text, \"9.9\" beats \"41.2\" because the character 9 comes after 4. Convert with pd.to_numeric and the real maximum appears. One stray value with a unit or a stray space is usually what forced the whole column to text.\n\nWhy the others are wrong. \u201cThe largest values are stored in a different column\u201d \u2014 The comment shows the values are in this column. The problem is how they are being compared.  \u201cmax() needs the column sorted first\u201d \u2014 max() never needs sorting. It compared correctly by the rules for text, which are the wrong rules for measurements.  \u201cThe column contains missing values that max() skipped\u201d \u2014 max() does skip missing values, and skipping them cannot produce a maximum below most of the data. The ordering itself is what has gone wrong."
          },
          {
            "n": 3,
            "kind": "traceback",
            "title": "What is the first thing to check?",
            "help": "Traceback (most recent call last):\n  File \"<ipython-input-4-7a8b9c>\", line 1, in <module>\n    df[\"silica_pct\"].mean()\nKeyError: 'silica_pct'",
            "choices": [
              {
                "text": "Whether the file loaded at all",
                "correct": false
              },
              {
                "text": "Print df.columns and compare the exact spelling, case and any stray spaces",
                "correct": true
              },
              {
                "text": "Whether the column contains missing values",
                "correct": false
              },
              {
                "text": "Whether mean() works on that data type",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. A KeyError on a frame means no column carries that exact label. Trailing spaces from a spreadsheet export are a common cause and they are invisible until you print the list.",
            "fbWrong": "THE ANSWER: Print df.columns and compare the exact spelling, case and any stray spaces. A KeyError on a frame means no column carries that exact label. Trailing spaces from a spreadsheet export are a common cause and they are invisible until you print the list.\n\nWhy the others are wrong. \u201cWhether the file loaded at all\u201d \u2014 That is worth confirming, and a frame that failed to load would raise on the read or on len(df) first. The message names one specific label.  \u201cWhether the column contains missing values\u201d \u2014 Missing values inside a column never stop you selecting it. This error happened before any value was read.  \u201cWhether mean() works on that data type\u201d \u2014 The error came from the selection, before mean() was reached. A type problem would name the type."
          },
          {
            "n": 4,
            "kind": "interpretation",
            "title": "What does this shape tell you?",
            "help": "g = df.groupby(\"ph_band\")[\"silica_concentrate\"].mean()\nprint(g.shape)\n(4,)",
            "choices": [
              {
                "text": "Four rows had a missing value in the grouping column",
                "correct": false
              },
              {
                "text": "Four rows of the original data survived the operation",
                "correct": false
              },
              {
                "text": "The result has four columns",
                "correct": false
              },
              {
                "text": "There are four groups, and the result holds one mean for each of them",
                "correct": true
              }
            ],
            "fbCorrect": "Correct. Grouping collapses the frame to one row per group, so the length of the result is the number of distinct values in the grouping column. The original frame is untouched.",
            "fbWrong": "THE ANSWER: There are four groups, and the result holds one mean for each of them. Grouping collapses the frame to one row per group, so the length of the result is the number of distinct values in the grouping column. The original frame is untouched.\n\nWhy the others are wrong. \u201cFour rows had a missing value in the grouping column\u201d \u2014 Rows with a missing group label are left out of the result rather than counted into it, and that would not set the length to four.  \u201cFour rows of the original data survived the operation\u201d \u2014 Grouping summarises rows rather than removing them. Every row contributed to one of the four means.  \u201cThe result has four columns\u201d \u2014 A shape written with one number describes one dimension. Four columns would appear as a second number."
          },
          {
            "n": 5,
            "kind": "judgement",
            "title": "A colleague sends you flotation_subset.csv as an email attachment with no other information, and you are asked to quote the mean concentrate silica in a report. What do you do first?",
            "help": "",
            "choices": [
              {
                "text": "Compute the mean and quote it, since the file is the data you were given",
                "correct": false
              },
              {
                "text": "Establish where the file came from, what licence it carries and how many rows it holds, and record all three alongside the figure",
                "correct": true
              },
              {
                "text": "Ask for the file in a different format to be safe",
                "correct": false
              },
              {
                "text": "Compare it against a published dataset and use whichever looks cleaner",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. A number in a report is only as defensible as the file behind it. Source, licence, date and row count are the minimum you need to be able to answer the question every reader eventually asks, which is where this came from.",
            "fbWrong": "THE ANSWER: Establish where the file came from, what licence it carries and how many rows it holds, and record all three alongside the figure. A number in a report is only as defensible as the file behind it. Source, licence, date and row count are the minimum you need to be able to answer the question every reader eventually asks, which is where this came from.\n\nWhy the others are wrong. \u201cCompute the mean and quote it, since the file is the data you were given\u201d \u2014 The arithmetic is the easy part and the least of your obligations. A figure whose origin you cannot state is one you cannot defend when it is challenged.  \u201cAsk for the file in a different format to be safe\u201d \u2014 The format is not the risk. An unsourced spreadsheet is exactly as unsourced after conversion.  \u201cCompare it against a published dataset and use whichever looks cleaner\u201d \u2014 Choosing data by how tidy it looks selects for convenience over relevance. Find out what this file is before reaching for another one."
          }
        ]
      },
      {
        "week": 6,
        "number": 6,
        "title": "CML3113 \u00b7 Weekly Quiz 6 \u2014 Dirty data, and seeing it",
        "intro": "Read what each question shows you. None of them can be answered without it.\n\nHOW THIS WORKS\n\u2022 Answer it now, in the 5 minutes on the screen. That is when this is meant to be taken, while the session is still fresh.\n\u2022 The form then stays open for 24 hours and closes itself. That window is there so a dead network or a broken phone does not cost you a mark you had earned. Take it in the room if you can: by Thursday you will have forgotten the session, and the feedback will be worth less to you.\n\u2022 ONE attempt, from your signed-in Google account. You cannot reopen it or change an answer, so read each question once, properly.\n\u2022 The first box asks for your registration number. It is the number printed on your student card, and it is how the mark reaches your record.\n\u2022 Five questions, one mark each, worth 1% of your final mark.\n\u2022 Your best ten of twelve quizzes count. Missing two costs you nothing, and there are no resits.\n\u2022 When you submit, tap View score. You get a tick or a cross on each question with the feedback underneath. Your mark is the number of ticks, and the feedback on anything you got wrong is the part worth reading.\n\u2022 A question left blank scores the same as one answered wrongly, so answer all five.",
        "questions": [
          {
            "n": 1,
            "kind": "diagnosis",
            "title": "The mean below is impossible. Read the values and say what went wrong.",
            "help": "# the laboratory system writes -999 when no result came back\nsilica = [2.1, 2.4, -999, 2.8, 2.2]\nprint(f\"mean {sum(silica) / len(silica):.2f} % silica\")\nmean -197.90 % silica",
            "choices": [
              {
                "text": "The list is too short for a mean to be meaningful",
                "correct": false
              },
              {
                "text": "The division should exclude the last value",
                "correct": false
              },
              {
                "text": "Silica cannot be negative, so the sensor is faulty",
                "correct": false
              },
              {
                "text": "One entry is a code standing in for a missing assay",
                "correct": true
              }
            ],
            "fbCorrect": "Correct. -999 is a marker meaning no result, and arithmetic has no way to know that. The mean of the four real assays is 2.38 per cent. Replace the code with a proper missing value before any arithmetic touches the column.",
            "fbWrong": "THE ANSWER: One entry is a code standing in for a missing assay. -999 is a marker meaning no result, and arithmetic has no way to know that. The mean of the four real assays is 2.38 per cent. Replace the code with a proper missing value before any arithmetic touches the column.\n\nWhy the others are wrong. \u201cThe list is too short for a mean to be meaningful\u201d \u2014 Four real values give a perfectly usable mean. The arithmetic was poisoned by a fifth entry that is not a measurement at all.  \u201cThe division should exclude the last value\u201d \u2014 The problem is not which position is excluded. It is that a placeholder is being treated as data.  \u201cSilica cannot be negative, so the sensor is faulty\u201d \u2014 Silica certainly cannot be negative, and no sensor produced -999. It is a convention for absent data, which is why it is such a reliable trap."
          },
          {
            "n": 2,
            "kind": "diagnosis",
            "title": "This runs with no error and no warning. What has it done to your data?",
            "help": "# one grade was typed as \"1.8 %\" instead of 1.8\ndf[\"iron_feed\"] = pd.to_numeric(df[\"iron_feed\"],\n                                  errors=\"coerce\")\nprint(df[\"iron_feed\"].mean())",
            "choices": [
              {
                "text": "It turned every unreadable value into a missing value, and the mean then quietly skipped those rows",
                "correct": true
              },
              {
                "text": "It stripped the unit and kept the number",
                "correct": false
              },
              {
                "text": "It raised the error but carried on to the next row",
                "correct": false
              },
              {
                "text": "It replaced the unreadable value with the column mean",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. Coercing is often the right move and it is never free: it converts a loud failure into a silent one. Count the missing values it created and report that count, otherwise your mean covers fewer rows than you believe.",
            "fbWrong": "THE ANSWER: It turned every unreadable value into a missing value, and the mean then quietly skipped those rows. Coercing is often the right move and it is never free: it converts a loud failure into a silent one. Count the missing values it created and report that count, otherwise your mean covers fewer rows than you believe.\n\nWhy the others are wrong. \u201cIt stripped the unit and kept the number\u201d \u2014 Nothing here parses units. A value with a unit attached is unreadable as a number and becomes missing.  \u201cIt raised the error but carried on to the next row\u201d \u2014 That is what errors=\"raise\" would do, minus the carrying on. Coercing suppresses the error entirely.  \u201cIt replaced the unreadable value with the column mean\u201d \u2014 No substitution happens. Filling gaps is a separate decision you have to make deliberately, and doing it before a split leaks information, as Week 10 shows."
          },
          {
            "n": 3,
            "kind": "traceback",
            "title": "You convert the column without coercing and get this. What is the useful thing about this message?",
            "help": "Traceback (most recent call last):\n  File \"<ipython-input-6-2b3c4d>\", line 1, in <module>\n    df[\"iron_feed\"] = pd.to_numeric(df[\"iron_feed\"])\nValueError: Unable to parse string \"1.8 %\" at position 417",
            "choices": [
              {
                "text": "It names the offending value and the row it sits in, so you can look at it and decide what it should be",
                "correct": true
              },
              {
                "text": "It proves the column cannot be converted",
                "correct": false
              },
              {
                "text": "It means the column is the wrong data type for pandas",
                "correct": false
              },
              {
                "text": "It should be suppressed so the analysis can continue",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. This is more useful than a silent conversion, because it hands you the exact value and position. Look at row 417, decide whether to repair the entry or drop it, and write down which you chose.",
            "fbWrong": "THE ANSWER: It names the offending value and the row it sits in, so you can look at it and decide what it should be. This is more useful than a silent conversion, because it hands you the exact value and position. Look at row 417, decide whether to repair the entry or drop it, and write down which you chose.\n\nWhy the others are wrong. \u201cIt proves the column cannot be converted\u201d \u2014 It proves one value cannot. Fix or remove that value and the column converts.  \u201cIt means the column is the wrong data type for pandas\u201d \u2014 The column is text because of this value. Conversion is the cure and the message is telling you what stands in the way.  \u201cIt should be suppressed so the analysis can continue\u201d \u2014 Suppressing it is available and it costs you the position and the value. Read the message first, then decide."
          },
          {
            "n": 4,
            "kind": "interpretation",
            "title": "Read the question you set yourself against the chart you produced. Does the chart answer it?",
            "help": "question:  Does concentrate silica differ between\n           high and low iron feed grade?\n\nchart:     one histogram\n           x = concentrate silica (%)\n           y = number of records\n           all 20,000 records, no grouping applied",
            "choices": [
              {
                "text": "Yes, provided the sample is large enough",
                "correct": false
              },
              {
                "text": "Yes, because the shape of the distribution reveals the two groups",
                "correct": false
              },
              {
                "text": "No, because the two groups are mixed together in one distribution and cannot be compared",
                "correct": true
              },
              {
                "text": "No, because a histogram is never the right chart",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. The question asks for a comparison, so the chart has to separate the groups: two distributions side by side, or a mean for each with its spread. A single pooled histogram cannot show a difference between halves it never divided.",
            "fbWrong": "THE ANSWER: No, because the two groups are mixed together in one distribution and cannot be compared. The question asks for a comparison, so the chart has to separate the groups: two distributions side by side, or a mean for each with its spread. A single pooled histogram cannot show a difference between halves it never divided.\n\nWhy the others are wrong. \u201cYes, provided the sample is large enough\u201d \u2014 Sample size cannot rescue a chart that never made the comparison. Twenty thousand pooled records answer the question no better than two hundred.  \u201cYes, because the shape of the distribution reveals the two groups\u201d \u2014 Two clear humps would hint at something and would not tell you which group each hump belongs to. A distribution with one hump can still hide a real difference between the groups.  \u201cNo, because a histogram is never the right chart\u201d \u2014 A histogram is a good way to show one distribution. The fault is the missing split rather than the choice of chart type."
          },
          {
            "n": 5,
            "kind": "judgement",
            "title": "You find a gold assay of 45 grams per tonne in a file where most assays sit between 0.5 and 3 grams per tonne. What do you do with it?",
            "help": "",
            "choices": [
              {
                "text": "Keep it and verify it against the assay record",
                "correct": true
              },
              {
                "text": "Replace it with the mean of the column",
                "correct": false
              },
              {
                "text": "Cap it at the highest ordinary value so it stops distorting the mean",
                "correct": false
              },
              {
                "text": "Delete it, because it is far outside the normal range",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. A 45 g/t intersection is exactly what a drilling programme exists to find. Confirm it in the laboratory register and keep it. Deleting it removes the discovery.",
            "fbWrong": "THE ANSWER: Keep it and verify it against the assay record. A 45 g/t intersection is exactly what a drilling programme exists to find. Confirm it in the laboratory register and keep it. Deleting it removes the discovery.\n\nWhy the others are wrong. \u201cReplace it with the mean of the column\u201d \u2014 That erases a genuine high-grade result and replaces it with a number nobody measured.  \u201cCap it at the highest ordinary value so it stops distorting the mean\u201d \u2014 Capping a high-grade result understates the resource and would be indefensible in a technical report.  \u201cDelete it, because it is far outside the normal range\u201d \u2014 This is the single most expensive mistake available in this dataset. The outlier is the ore body."
          }
        ]
      },
      {
        "week": 8,
        "number": 7,
        "title": "CML3113 \u00b7 Weekly Quiz 7 \u2014 Learning from data: the first model",
        "intro": "Read what each question shows you. None of them can be answered without it.\n\nHOW THIS WORKS\n\u2022 Answer it now, in the 5 minutes on the screen. That is when this is meant to be taken, while the session is still fresh.\n\u2022 The form then stays open for 24 hours and closes itself. That window is there so a dead network or a broken phone does not cost you a mark you had earned. Take it in the room if you can: by Thursday you will have forgotten the session, and the feedback will be worth less to you.\n\u2022 ONE attempt, from your signed-in Google account. You cannot reopen it or change an answer, so read each question once, properly.\n\u2022 The first box asks for your registration number. It is the number printed on your student card, and it is how the mark reaches your record.\n\u2022 Five questions, one mark each, worth 1% of your final mark.\n\u2022 Your best ten of twelve quizzes count. Missing two costs you nothing, and there are no resits.\n\u2022 When you submit, tap View score. You get a tick or a cross on each question with the feedback underneath. Your mark is the number of ticks, and the feedback on anything you got wrong is the part worth reading.\n\u2022 A question left blank scores the same as one answered wrongly, so answer all five.",
        "questions": [
          {
            "n": 1,
            "kind": "diagnosis",
            "title": "A teammate reports this as the accuracy of the model. What does the number actually describe?",
            "help": "model.fit(X, y)\nprint(model.score(X, y))\n0.91",
            "choices": [
              {
                "text": "How well the model will do on new data, give or take a little",
                "correct": false
              },
              {
                "text": "Nothing useful, because score() is the wrong function",
                "correct": false
              },
              {
                "text": "The proportion of the data used for training",
                "correct": false
              },
              {
                "text": "How well the model reproduces the rows it was fitted on, which tells you nothing about a new case",
                "correct": true
              }
            ],
            "fbCorrect": "Correct. The same rows appear in fit and in score, so the model is being marked on the answers it was shown. Hold rows back with train_test_split and score on those.",
            "fbWrong": "THE ANSWER: How well the model reproduces the rows it was fitted on, which tells you nothing about a new case. The same rows appear in fit and in score, so the model is being marked on the answers it was shown. Hold rows back with train_test_split and score on those.\n\nWhy the others are wrong. \u201cHow well the model will do on new data, give or take a little\u201d \u2014 There is no basis for that reading. A model with enough freedom can score near one on its training rows and fail completely on anything new, which is the whole subject of Week 10.  \u201cNothing useful, because score() is the wrong function\u201d \u2014 score() is the right function used on the wrong rows. Give it held-out data and the number becomes meaningful.  \u201cThe proportion of the data used for training\u201d \u2014 score() returns a measure of fit. The train and test proportions are whatever you chose when you split, and here nothing was split."
          },
          {
            "n": 2,
            "kind": "diagnosis",
            "title": "This predicts a plausible-looking value and raises no error, and the value is wrong. Why?",
            "help": "feats = [\"iron_feed\", \"starch_flow\", \"pulp_ph\"]\nmodel.fit(df[feats], df[\"silica_concentrate\"])\n\n# a new record: 56.3 % iron feed, 3180 g/min starch, pH 9.4\nprint(model.predict([[3180, 56.3, 9.4]]))",
            "choices": [
              {
                "text": "The model was fitted on too few features to predict anything",
                "correct": false
              },
              {
                "text": "The new values should have been scaled first",
                "correct": false
              },
              {
                "text": "predict() needs a two-dimensional input",
                "correct": false
              },
              {
                "text": "The values were supplied in a different order from the fitted columns",
                "correct": true
              }
            ],
            "fbCorrect": "Correct. A fitted model knows only that its first input is whatever its first training column was. Swap two and it happily applies the wrong coefficient to each. Build the row as a frame with named columns and this class of error disappears.",
            "fbWrong": "THE ANSWER: The values were supplied in a different order from the fitted columns. A fitted model knows only that its first input is whatever its first training column was. Swap two and it happily applies the wrong coefficient to each. Build the row as a frame with named columns and this class of error disappears.\n\nWhy the others are wrong. \u201cThe model was fitted on too few features to predict anything\u201d \u2014 Three or four features is enough to produce a prediction. The count is fine and the order is not.  \u201cThe new values should have been scaled first\u201d \u2014 Scaling would matter for some model types and it would not repair a swap. Scaled or raw, the values are in the wrong positions.  \u201cpredict() needs a two-dimensional input\u201d \u2014 It does, and it was given one. The doubled brackets are correct here."
          },
          {
            "n": 3,
            "kind": "traceback",
            "title": "What is the most likely cause?",
            "help": "Traceback (most recent call last):\n  File \"<ipython-input-9-5e6f7a>\", line 1, in <module>\n    model.fit(X, y)\nValueError: Found input variables with inconsistent numbers\nof samples: [16000, 20000]",
            "choices": [
              {
                "text": "The features were filtered or had rows dropped and the target was not, so the two no longer line up",
                "correct": true
              },
              {
                "text": "The features and the target need to be the same data type",
                "correct": false
              },
              {
                "text": "There are too few rows to fit a model",
                "correct": false
              },
              {
                "text": "The target column contains missing values",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. Dropping missing values from the feature frame without applying the same selection to the target is the usual cause. Filter the frame first and take X and y from the filtered frame so they can never drift apart.",
            "fbWrong": "THE ANSWER: The features were filtered or had rows dropped and the target was not, so the two no longer line up. Dropping missing values from the feature frame without applying the same selection to the target is the usual cause. Filter the frame first and take X and y from the filtered frame so they can never drift apart.\n\nWhy the others are wrong. \u201cThe features and the target need to be the same data type\u201d \u2014 They routinely differ, and that is fine. The error counts rows and says nothing about types.  \u201cThere are too few rows to fit a model\u201d \u2014 Both counts here are ample. The problem is that they are not equal.  \u201cThe target column contains missing values\u201d \u2014 Missing values in the target give a different complaint about NaN. This message is purely about the row counts disagreeing."
          },
          {
            "n": 4,
            "kind": "interpretation",
            "title": "A teammate shows you this plot and this conclusion. How should you read it?",
            "help": "plot:        y = residual (actual - predicted), % silica\n             x = ACTUAL concentrate silica, %\n             a clear upward slope, left to right\n\nconclusion:  \"the model under-predicts high-silica\n             records\"",
            "choices": [
              {
                "text": "The residuals should have been squared before plotting",
                "correct": false
              },
              {
                "text": "The conclusion is right, and the model needs an extra feature to fix it",
                "correct": false
              },
              {
                "text": "The slope appears by construction; plot residuals against the predicted value",
                "correct": true
              },
              {
                "text": "A slope in the residuals always means the model is broken",
                "correct": false
              }
            ],
            "fbCorrect": "Correct, and this catches almost everybody once. The actual value equals the prediction plus the residual, so the residual is built into the quantity on the horizontal axis and rises with it. Against the predicted value the slope disappears and any real pattern becomes visible.",
            "fbWrong": "THE ANSWER: The slope appears by construction; plot residuals against the predicted value. This catches almost everybody once. The actual value equals the prediction plus the residual, so the residual is built into the quantity on the horizontal axis and rises with it. Against the predicted value the slope disappears and any real pattern becomes visible.\n\nWhy the others are wrong. \u201cThe residuals should have been squared before plotting\u201d \u2014 Squaring throws away the sign, which is the most useful part of a residual. The pairing of axes is what is wrong here.  \u201cThe conclusion is right, and the model needs an extra feature to fix it\u201d \u2014 The conclusion may happen to be true and this plot cannot establish it. Redraw against the predicted value before changing the model.  \u201cA slope in the residuals always means the model is broken\u201d \u2014 A slope against the predicted value would be worth investigating. A slope against the actual value is arithmetic rather than a finding."
          },
          {
            "n": 5,
            "kind": "judgement",
            "title": "Your model reaches a mean absolute error of 0.4 percentage points of silica. The client asks whether that is good. What do you need before you can answer?",
            "help": "",
            "choices": [
              {
                "text": "Nothing further; 0.4 percentage points is a small number",
                "correct": false
              },
              {
                "text": "The error of predicting the mean, and the assay's own repeatability",
                "correct": true
              },
              {
                "text": "A second model to compare it against",
                "correct": false
              },
              {
                "text": "A larger dataset",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. Both are needed. The assay repeats to about 0.1 percentage points, so 0.4 is around four times looser than the measurement it replaces, and predicting the mean gives you the floor. Those two numbers turn a metric into an answer.",
            "fbWrong": "THE ANSWER: The error of predicting the mean, and the assay's own repeatability. Both are needed. The assay repeats to about 0.1 percentage points, so 0.4 is around four times looser than the measurement it replaces, and predicting the mean gives you the floor. Those two numbers turn a metric into an answer.\n\nWhy the others are wrong. \u201cNothing further; 0.4 percentage points is a small number\u201d \u2014 Small compared with what? Against a specification of 3 per cent it may matter a great deal.  \u201cA second model to compare it against\u201d \u2014 That ranks two options without telling you whether either beats doing nothing.  \u201cA larger dataset\u201d \u2014 More rows might help and cannot answer the question of whether 0.4 points is useful to a metallurgist."
          }
        ]
      },
      {
        "week": 9,
        "number": 8,
        "title": "CML3113 \u00b7 Weekly Quiz 8 \u2014 Classification",
        "intro": "Read what each question shows you. None of them can be answered without it.\n\nHOW THIS WORKS\n\u2022 Answer it now, in the 5 minutes on the screen. That is when this is meant to be taken, while the session is still fresh.\n\u2022 The form then stays open for 24 hours and closes itself. That window is there so a dead network or a broken phone does not cost you a mark you had earned. Take it in the room if you can: by Thursday you will have forgotten the session, and the feedback will be worth less to you.\n\u2022 ONE attempt, from your signed-in Google account. You cannot reopen it or change an answer, so read each question once, properly.\n\u2022 The first box asks for your registration number. It is the number printed on your student card, and it is how the mark reaches your record.\n\u2022 Five questions, one mark each, worth 1% of your final mark.\n\u2022 Your best ten of twelve quizzes count. Missing two costs you nothing, and there are no resits.\n\u2022 When you submit, tap View score. You get a tick or a cross on each question with the feedback underneath. Your mark is the number of ticks, and the feedback on anything you got wrong is the part worth reading.\n\u2022 A question left blank scores the same as one answered wrongly, so answer all five.",
        "questions": [
          {
            "n": 1,
            "kind": "diagnosis",
            "title": "A teammate is pleased with this result. What has the model actually learned?",
            "help": "accuracy                     0.966\nsamples predicted as ore         0\n\n# in this register 3.4 in 100 samples are above cut-off",
            "choices": [
              {
                "text": "That more features are needed to raise accuracy",
                "correct": false
              },
              {
                "text": "A genuinely strong rule, since 96.6 per cent is a high score",
                "correct": false
              },
              {
                "text": "To answer with the majority class every time, which scores the majority-class share and finds nothing",
                "correct": true
              },
              {
                "text": "That the two classes are equally easy to separate",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. Since 96.6 in 100 cases are negative, always saying negative scores 0.966. The model has found the base rate and no signal. Recall on the class you care about is zero, and that is the number to report.",
            "fbWrong": "THE ANSWER: To answer with the majority class every time, which scores the majority-class share and finds nothing. Since 96.6 in 100 cases are negative, always saying negative scores 0.966. The model has found the base rate and no signal. Recall on the class you care about is zero, and that is the number to report.\n\nWhy the others are wrong. \u201cThat more features are needed to raise accuracy\u201d \u2014 Accuracy is already near its ceiling and is the wrong instrument. Change the metric before changing the model.  \u201cA genuinely strong rule, since 96.6 per cent is a high score\u201d \u2014 The score is exactly what you get for free by ignoring the data. A rule that never fires cannot be strong at the job it was built for.  \u201cThat the two classes are equally easy to separate\u201d \u2014 It never attempted the separation. It predicted one class throughout."
          },
          {
            "n": 2,
            "kind": "diagnosis",
            "title": "This model was tested against a grade-control register of ten thousand samples. Read the confusion matrix. Which statement does it support?",
            "help": "                      pred: waste    pred: ore\nactual: waste                9620             36\nactual: ore                   310             34\n\n10,000 samples in total; accuracy 0.965",
            "choices": [
              {
                "text": "It misses about nine in ten of the cases it exists to catch",
                "correct": true
              },
              {
                "text": "Accuracy of 0.965 shows it is fit for use",
                "correct": false
              },
              {
                "text": "It is well balanced between the two kinds of error",
                "correct": false
              },
              {
                "text": "Its main weakness is false alarms",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. Recall on the class of interest is 34 out of 344, which is 0.099. The high accuracy comes almost entirely from the 9,620 easy negatives. This is the number the matrix exists to expose.",
            "fbWrong": "THE ANSWER: It misses about nine in ten of the cases it exists to catch. Recall on the class of interest is 34 out of 344, which is 0.099. The high accuracy comes almost entirely from the 9,620 easy negatives. This is the number the matrix exists to expose.\n\nWhy the others are wrong. \u201cAccuracy of 0.965 shows it is fit for use\u201d \u2014 Predicting the majority class throughout would score 0.966, which is higher. Accuracy cannot see this failure.  \u201cIt is well balanced between the two kinds of error\u201d \u2014 310 against 36 is close to a nine-to-one imbalance in the errors.  \u201cIts main weakness is false alarms\u201d \u2014 There are only 36 false alarms against 310 misses. The costly error here is the one being made nearly ten times as often."
          },
          {
            "n": 3,
            "kind": "traceback",
            "title": "What does this tell you to change?",
            "help": "Traceback (most recent call last):\n  File \"<ipython-input-11-8b9c0d>\", line 1, in <module>\n    print(recall_score(y_test, pred))\nValueError: Target is multiclass but average='binary'.\nPlease choose another average setting, one of [None, 'micro', 'macro', 'weighted'].",
            "choices": [
              {
                "text": "The test set is too small for recall to be defined",
                "correct": false
              },
              {
                "text": "The target has more than two classes, so you must say how recall should be combined across them",
                "correct": true
              },
              {
                "text": "The predictions are the wrong data type",
                "correct": false
              },
              {
                "text": "Recall cannot be computed for more than two classes",
                "correct": false
              }
            ],
            "fbCorrect": "Correct, and the choice matters. average=None gives you recall per class, which is usually what you want, because a single combined figure can hide a class the model never predicts.",
            "fbWrong": "THE ANSWER: The target has more than two classes, so you must say how recall should be combined across them. The choice matters. average=None gives you recall per class, which is usually what you want, because a single combined figure can hide a class the model never predicts.\n\nWhy the others are wrong. \u201cThe test set is too small for recall to be defined\u201d \u2014 Size is not mentioned and is not the issue. The class count is.  \u201cThe predictions are the wrong data type\u201d \u2014 The types are acceptable. The message is about the number of classes in the target.  \u201cRecall cannot be computed for more than two classes\u201d \u2014 It can, once you state how to aggregate it. The error offers you the options."
          },
          {
            "n": 4,
            "kind": "interpretation",
            "title": "You lower the decision threshold from 0.5 to 0.2 and re-score the same model on the same test set. What has changed?",
            "help": "threshold 0.5   recall 0.099   false alarms  36\nthreshold 0.2   recall 0.439   false alarms 290",
            "choices": [
              {
                "text": "The model has been improved by better tuning",
                "correct": false
              },
              {
                "text": "The result is invalid because the threshold should stay at 0.5",
                "correct": false
              },
              {
                "text": "Nothing about the model; you moved along its trade-off, buying recall by accepting eight times as many false alarms",
                "correct": true
              },
              {
                "text": "The model now overfits, because recall rose sharply",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. The model and its scores are untouched: only the cut-off you apply to them changed. Which threshold is right depends on what a false alarm costs against a miss, and that is a question about the work rather than the model.",
            "fbWrong": "THE ANSWER: Nothing about the model; you moved along its trade-off, buying recall by accepting eight times as many false alarms. The model and its scores are untouched: only the cut-off you apply to them changed. Which threshold is right depends on what a false alarm costs against a miss, and that is a question about the work rather than the model.\n\nWhy the others are wrong. \u201cThe model has been improved by better tuning\u201d \u2014 No retraining took place. The same probabilities are being cut in a different place.  \u201cThe result is invalid because the threshold should stay at 0.5\u201d \u2014 0.5 is a default rather than a rule. On a problem where a miss costs far more than a false alarm, moving it is exactly the right thing to do.  \u201cThe model now overfits, because recall rose sharply\u201d \u2014 Overfitting is about the gap between training and unseen data. This is one model on one test set at two thresholds."
          },
          {
            "n": 5,
            "kind": "judgement",
            "title": "Sending ore to the waste dump throws away metal you have already paid to mine, and you never find out. Sending waste to the mill costs the processing of worthless rock. Which metric should govern your model, and why?",
            "help": "",
            "choices": [
              {
                "text": "Whichever metric gives the highest number, so the result reads well",
                "correct": false
              },
              {
                "text": "Recall on the class you cannot afford to miss, with the false-alarm rate beside it",
                "correct": true
              },
              {
                "text": "Accuracy, because it summarises overall performance",
                "correct": false
              },
              {
                "text": "Precision, because false alarms annoy the operators",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. The expensive error is the miss, so recall is the quantity to drive up. Quoting the false-alarm rate beside it keeps you honest, because recall can always be bought and somebody has to pay for it.",
            "fbWrong": "THE ANSWER: Recall on the class you cannot afford to miss, with the false-alarm rate beside it. The expensive error is the miss, so recall is the quantity to drive up. Quoting the false-alarm rate beside it keeps you honest, because recall can always be bought and somebody has to pay for it.\n\nWhy the others are wrong. \u201cWhichever metric gives the highest number, so the result reads well\u201d \u2014 Choosing a metric to flatter the model is how a system that misses nine failures in ten gets signed off.  \u201cAccuracy, because it summarises overall performance\u201d \u2014 At a base rate near 3 per cent, accuracy is dominated by easy negatives and a useless model scores 0.966. It cannot see the error that matters here.  \u201cPrecision, because false alarms annoy the operators\u201d \u2014 Precision alone rewards a model that fires only when certain, which is a model that misses most of the cases. It belongs in the report next to recall rather than in charge of it."
          }
        ]
      },
      {
        "week": 10,
        "number": 9,
        "title": "CML3113 \u00b7 Weekly Quiz 9 \u2014 Can I trust this model?",
        "intro": "Read what each question shows you. None of them can be answered without it.\n\nHOW THIS WORKS\n\u2022 Answer it now, in the 5 minutes on the screen. That is when this is meant to be taken, while the session is still fresh.\n\u2022 The form then stays open for 24 hours and closes itself. That window is there so a dead network or a broken phone does not cost you a mark you had earned. Take it in the room if you can: by Thursday you will have forgotten the session, and the feedback will be worth less to you.\n\u2022 ONE attempt, from your signed-in Google account. You cannot reopen it or change an answer, so read each question once, properly.\n\u2022 The first box asks for your registration number. It is the number printed on your student card, and it is how the mark reaches your record.\n\u2022 Five questions, one mark each, worth 1% of your final mark.\n\u2022 Your best ten of twelve quizzes count. Missing two costs you nothing, and there are no resits.\n\u2022 When you submit, tap View score. You get a tick or a cross on each question with the feedback underneath. Your mark is the number of ticks, and the feedback on anything you got wrong is the part worth reading.\n\u2022 A question left blank scores the same as one answered wrongly, so answer all five.",
        "questions": [
          {
            "n": 1,
            "kind": "diagnosis",
            "title": "This reports a good test score. Why can that score not be trusted?",
            "help": "scaler = StandardScaler()\nX_scaled = scaler.fit_transform(X)     # whole file\n\nX_tr, X_te, y_tr, y_te = train_test_split(X_scaled, y)\nmodel.fit(X_tr, y_tr)\nprint(model.score(X_te, y_te))",
            "choices": [
              {
                "text": "Nothing is wrong; scaling does not use the target",
                "correct": false
              },
              {
                "text": "The scaler was fitted on the whole file, so the test rows helped set the scaling",
                "correct": true
              },
              {
                "text": "The split should come before the features are selected",
                "correct": false
              },
              {
                "text": "StandardScaler is the wrong scaler for this data",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. The test rows are supposed to stand in for cases you have never seen, and here they helped set the scaling. Put the scaler in a Pipeline and fit it after the split, so it only ever sees training rows.",
            "fbWrong": "THE ANSWER: The scaler was fitted on the whole file, so the test rows helped set the scaling. The test rows are supposed to stand in for cases you have never seen, and here they helped set the scaling. Put the scaler in a Pipeline and fit it after the split, so it only ever sees training rows.\n\nWhy the others are wrong. \u201cNothing is wrong; scaling does not use the target\u201d \u2014 Leakage does not require the target. Borrowing the test rows' mean and spread means the test set is no longer a clean estimate, and how far the number is distorted is not something you can work out from the outside, which is the real cost.  \u201cThe split should come before the features are selected\u201d \u2014 Selecting which columns to use is fine either side. Measuring something from the data is what has to wait until after the split.  \u201cStandardScaler is the wrong scaler for this data\u201d \u2014 The choice of scaler is a separate question. Any scaler fitted before the split leaks in the same way."
          },
          {
            "n": 2,
            "kind": "diagnosis",
            "title": "Which of the three error stories does this pattern match?",
            "help": "training score   0.98\ntest score       0.61",
            "choices": [
              {
                "text": "Information has leaked from the test set into training",
                "correct": false
              },
              {
                "text": "The model has memorised its training rows and does not generalise",
                "correct": true
              },
              {
                "text": "The two scores are measuring different quantities",
                "correct": false
              },
              {
                "text": "The model is too simple to capture the pattern",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. A high training score with a much lower test score is the signature of a model with too much freedom for the data. Simplify it, constrain it, or get more rows.",
            "fbWrong": "THE ANSWER: The model has memorised its training rows and does not generalise. A high training score with a much lower test score is the signature of a model with too much freedom for the data. Simplify it, constrain it, or get more rows.\n\nWhy the others are wrong. \u201cInformation has leaked from the test set into training\u201d \u2014 Leakage usually makes both scores look good, since the model has effectively seen the answers. A large gap points the other way.  \u201cThe two scores are measuring different quantities\u201d \u2014 Both are the same measure on different rows. That is what makes the comparison meaningful.  \u201cThe model is too simple to capture the pattern\u201d \u2014 A model that is too simple scores poorly on both, because it cannot even fit the rows it was given. Here it fits them almost perfectly."
          },
          {
            "n": 3,
            "kind": "traceback",
            "title": "A teammate has already tried to deal with the gaps, in the cell shown above the traceback. Read both, then say what you would change.",
            "help": "imp = SimpleImputer(strategy=\"mean\")\nX[[\"pulp_ph\"]] = imp.fit_transform(X[[\"pulp_ph\"]])\n\nX_tr, X_te, y_tr, y_te = train_test_split(X, y)\npipe = Pipeline([(\"model\", Ridge())])\npipe.fit(X_tr, y_tr)\n\nTraceback (most recent call last):\n  File \"<ipython-input-13-1a2b3c>\", line 6, in <module>\n    pipe.fit(X_tr, y_tr)\nValueError: Input X contains NaN.",
            "choices": [
              {
                "text": "Impute the remaining columns the same way, before the split",
                "correct": false
              },
              {
                "text": "Replace the remaining gaps with zero so the model can fit",
                "correct": false
              },
              {
                "text": "Drop the rows that still contain gaps",
                "correct": false
              },
              {
                "text": "Move the imputer inside the Pipeline, and cover every column",
                "correct": true
              }
            ],
            "fbCorrect": "Correct on both counts. Only one column was imputed, so the gaps in the others are still there, which is why the error still fires. And fitting it on the whole frame before the split measures the test rows, which is the leak from question one wearing different clothes. Inside the pipeline both problems go away at once.",
            "fbWrong": "THE ANSWER: Move the imputer inside the Pipeline, and cover every column. Correct on both counts. Only one column was imputed, so the gaps in the others are still there, which is why the error still fires. And fitting it on the whole frame before the split measures the test rows, which is the leak from question one wearing different clothes. Inside the pipeline both problems go away at once.\n\nWhy the others are wrong. \u201cImpute the remaining columns the same way, before the split\u201d \u2014 That silences the error and keeps the leak. Every value the imputer learns before the split has been measured partly from the test rows.  \u201cReplace the remaining gaps with zero so the model can fit\u201d \u2014 Zero is a real value on these columns, so this quietly invents low readings. Week 6 covers the damage that does.  \u201cDrop the rows that still contain gaps\u201d \u2014 It would run, and it discards data and can bias what is left if the gaps cluster in one source, which Week 4 showed they often do."
          },
          {
            "n": 4,
            "kind": "interpretation",
            "title": "You run five-fold cross-validation and get these scores. What should you report, and what should you look at?",
            "help": "fold scores: 0.71, 0.68, 0.74, 0.52, 0.70\nmean 0.67",
            "choices": [
              {
                "text": "The best fold, since it shows what the model can achieve",
                "correct": false
              },
              {
                "text": "Nothing yet; five folds is too few to report",
                "correct": false
              },
              {
                "text": "The mean with its spread, and look into the 0.52 fold",
                "correct": true
              },
              {
                "text": "The mean alone, since averaging is the purpose of cross-validation",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. Four folds sit close together and one sits well below, which suggests that fold contains something the others do not. Group structure in the rows is the usual explanation, and it is the subject of the next question.",
            "fbWrong": "THE ANSWER: The mean with its spread, and look into the 0.52 fold. Four folds sit close together and one sits well below, which suggests that fold contains something the others do not. Group structure in the rows is the usual explanation, and it is the subject of the next question.\n\nWhy the others are wrong. \u201cThe best fold, since it shows what the model can achieve\u201d \u2014 Quoting the best fold is selecting the most flattering result from your own experiment.  \u201cNothing yet; five folds is too few to report\u201d \u2014 Five folds is a standard choice and perfectly reportable. The spread is part of the report rather than a reason to withhold it.  \u201cThe mean alone, since averaging is the purpose of cross-validation\u201d \u2014 A bare mean hides the thing worth knowing. Reporting 0.67 with no spread conceals a fold that scored 0.52 and the reason behind it."
          },
          {
            "n": 5,
            "kind": "judgement",
            "title": "Working with the well-log dataset, you discover that samples from the same drill hole are split across your training and test sets. Samples from one hole are far more alike than samples from different holes. What should you do?",
            "help": "",
            "choices": [
              {
                "text": "Split by hole, so every sample from one hole sits entirely in training or entirely in test",
                "correct": true
              },
              {
                "text": "Increase the size of the test set",
                "correct": false
              },
              {
                "text": "Remove the samples that look most similar",
                "correct": false
              },
              {
                "text": "Leave it, because a random split is unbiased by definition",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. A random split lets the model learn a hole and then be tested on the same hole, which flatters it badly. The question you actually face is prediction in a hole you have not drilled.",
            "fbWrong": "THE ANSWER: Split by hole, so every sample from one hole sits entirely in training or entirely in test. A random split lets the model learn a hole and then be tested on the same hole, which flatters it badly. The question you actually face is prediction in a hole you have not drilled.\n\nWhy the others are wrong. \u201cIncrease the size of the test set\u201d \u2014 The same flaw simply appears in a bigger test set.  \u201cRemove the samples that look most similar\u201d \u2014 Those samples are real observations, and downhole similarity is a property of the ore body rather than an error.  \u201cLeave it, because a random split is unbiased by definition\u201d \u2014 It is unbiased with respect to rows and takes no account of the strong similarity within a hole."
          }
        ]
      },
      {
        "week": 11,
        "number": 10,
        "title": "CML3113 \u00b7 Weekly Quiz 10 \u2014 Features",
        "intro": "Read what each question shows you. None of them can be answered without it.\n\nHOW THIS WORKS\n\u2022 Answer it now, in the 5 minutes on the screen. That is when this is meant to be taken, while the session is still fresh.\n\u2022 The form then stays open for 24 hours and closes itself. That window is there so a dead network or a broken phone does not cost you a mark you had earned. Take it in the room if you can: by Thursday you will have forgotten the session, and the feedback will be worth less to you.\n\u2022 ONE attempt, from your signed-in Google account. You cannot reopen it or change an answer, so read each question once, properly.\n\u2022 The first box asks for your registration number. It is the number printed on your student card, and it is how the mark reaches your record.\n\u2022 Five questions, one mark each, worth 1% of your final mark.\n\u2022 Your best ten of twelve quizzes count. Missing two costs you nothing, and there are no resits.\n\u2022 When you submit, tap View score. You get a tick or a cross on each question with the feedback underneath. Your mark is the number of ticks, and the feedback on anything you got wrong is the part worth reading.\n\u2022 A question left blank scores the same as one answered wrongly, so answer all five.",
        "questions": [
          {
            "n": 1,
            "kind": "diagnosis",
            "title": "A teammate adds a scaler expecting an improvement and the score does not budge. Why not?",
            "help": "before:  DecisionTreeRegressor(random_state=0)\n                                               MAE 0.42\nafter:   Pipeline([(\"scale\", StandardScaler()),\n                   (\"model\", DecisionTreeRegressor(\n                                 random_state=0))])\n                                               MAE 0.42",
            "choices": [
              {
                "text": "The scaler was placed after the model in the pipeline",
                "correct": false
              },
              {
                "text": "A tree splits on the order of the values, and scaling preserves that order",
                "correct": true
              },
              {
                "text": "The features were already on the same scale",
                "correct": false
              },
              {
                "text": "The tree needs a greater depth before scaling helps",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. Rescaling moves the numbers and leaves their ranking untouched, and a threshold split only cares about ranking. Scaling earns its keep for models that measure distances or fit coefficients.",
            "fbWrong": "THE ANSWER: A tree splits on the order of the values, and scaling preserves that order. Rescaling moves the numbers and leaves their ranking untouched, and a threshold split only cares about ranking. Scaling earns its keep for models that measure distances or fit coefficients.\n\nWhy the others are wrong. \u201cThe scaler was placed after the model in the pipeline\u201d \u2014 It is first, which is the correct position. The order in the pipeline is not the issue.  \u201cThe features were already on the same scale\u201d \u2014 Even if they were, that would not be the reason. A tree is unaffected by this kind of rescaling whatever the starting scales happen to be.  \u201cThe tree needs a greater depth before scaling helps\u201d \u2014 Depth changes how the tree fits and never makes it sensitive to a monotonic rescaling."
          },
          {
            "n": 2,
            "kind": "diagnosis",
            "title": "The score on your own test split improves after this change, and the model is worse. What has happened?",
            "help": "print(df.shape)\n(20000, 24)\n\nprint(df[\"assay_batch_id\"].nunique())\n847\n\nX = pd.get_dummies(df, columns=[\"assay_batch_id\"])\nprint(X.shape)\n(20000, 870)",
            "choices": [
              {
                "text": "It added one column per identifier, so the model can now recognise individual units",
                "correct": true
              },
              {
                "text": "get_dummies should have been given the whole frame",
                "correct": false
              },
              {
                "text": "It made the frame too wide for the model to fit",
                "correct": false
              },
              {
                "text": "The identifiers should have been numbered 1 to 847 instead",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. An identifier expanded this way hands the model a lookup table for the units in your file. It scores well wherever the same units appear on both sides of the split and carries nothing to a new one. Drop the identifier and keep the columns that describe the thing.",
            "fbWrong": "THE ANSWER: It added one column per identifier, so the model can now recognise individual units. An identifier expanded this way hands the model a lookup table for the units in your file. It scores well wherever the same units appear on both sides of the split and carries nothing to a new one. Drop the identifier and keep the columns that describe the thing.\n\nWhy the others are wrong. \u201cget_dummies should have been given the whole frame\u201d \u2014 It was given the whole frame with one column named for expansion, which is the normal usage. The choice of column is the fault.  \u201cIt made the frame too wide for the model to fit\u201d \u2014 A few hundred columns is unremarkable and fits without complaint. The problem is what those columns mean.  \u201cThe identifiers should have been numbered 1 to 847 instead\u201d \u2014 That is worse: it tells a straight-line model that unit 800 is a hundred times unit 8. Neither encoding rescues a column that is only a label."
          },
          {
            "n": 3,
            "kind": "traceback",
            "title": "What has happened, and what is the catch in the obvious fix?",
            "help": "enc = OneHotEncoder(drop=\"first\")\n# ... fitted on ore_source values pit 1, pit 3,\n#     stockpile, blend\n\nTraceback (most recent call last):\n  File \"<ipython-input-15-6d7e8f>\", line 1, in <module>\n    pipe.predict(new_rows)\nValueError: Found unknown categories ['pit 7'] in column 0\nduring transform",
            "choices": [
              {
                "text": "The category column should be dropped from the model",
                "correct": false
              },
              {
                "text": "Refitting the encoder on the new rows as well will fix it properly",
                "correct": false
              },
              {
                "text": "handle_unknown=\"ignore\" clears it, and with drop=\"first\" an unseen category then encodes as the dropped one",
                "correct": true
              },
              {
                "text": "Adding handle_unknown=\"ignore\" solves it cleanly, with no side effect worth worrying about",
                "correct": false
              }
            ],
            "fbCorrect": "Correct, and the second half is the part almost nobody is told. An ignored unknown category is encoded as all zeros, which is exactly how the dropped reference category is encoded, so every new category silently becomes the baseline. Choose one of the two options deliberately and count how often an unknown value arrives.",
            "fbWrong": "THE ANSWER: handle_unknown=\"ignore\" clears it, and with drop=\"first\" an unseen category then encodes as the dropped one. The second half is the part almost nobody is told. An ignored unknown category is encoded as all zeros, which is exactly how the dropped reference category is encoded, so every new category silently becomes the baseline. Choose one of the two options deliberately and count how often an unknown value arrives.\n\nWhy the others are wrong. \u201cThe category column should be dropped from the model\u201d \u2014 It may be carrying real signal. The task is to encode it so it survives a value you have not seen before.  \u201cRefitting the encoder on the new rows as well will fix it properly\u201d \u2014 Fitting anything on rows you are about to predict is the leakage pattern from Week 10. It also cannot work in service, where the new value arrives after the model is deployed.  \u201cAdding handle_unknown=\"ignore\" solves it cleanly, with no side effect worth worrying about\u201d \u2014 It does clear the error. The side effect is that the unknown category is encoded as all zeros, and because drop=\"first\" is set, that is the same encoding as the dropped category."
          },
          {
            "n": 4,
            "kind": "interpretation",
            "title": "Each row removes one feature and refits. Which feature has earned its place least?",
            "help": "features                    MAE (pts silica)\nall five                                0.31\nminus starch dose per tonne             0.68\nminus iron feed grade                   0.74\nminus amina-to-starch ratio             0.32\nminus air flow                         0.39\nminus pulp density                     0.44",
            "choices": [
              {
                "text": "None of them; every feature earns its place",
                "correct": false
              },
              {
                "text": "Starch dose per tonne, because 0.68 is a poor result",
                "correct": false
              },
              {
                "text": "The amina-to-starch ratio, because removing it moves the error by 0.01 percentage points",
                "correct": true
              },
              {
                "text": "Iron feed grade, because it has the largest error when removed",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. Iron feed grade and starch dose each cost you around 0.4 points when removed, and this one costs 0.01. It is close to redundant given the dose feature.",
            "fbWrong": "THE ANSWER: The amina-to-starch ratio, because removing it moves the error by 0.01 percentage points. Iron feed grade and starch dose each cost you around 0.4 points when removed, and this one costs 0.01. It is close to redundant given the dose feature.\n\nWhy the others are wrong. \u201cNone of them; every feature earns its place\u201d \u2014 A change of 0.01 percentage points is well inside the noise you would see between folds.  \u201cStarch dose per tonne, because 0.68 is a poor result\u201d \u2014 0.68 is the error without it. That is the case for keeping it.  \u201cIron feed grade, because it has the largest error when removed\u201d \u2014 That is the reading reversed. The largest degradation marks the most valuable feature."
          },
          {
            "n": 5,
            "kind": "judgement",
            "title": "Two teams reach almost the same error. One uses a random forest on the raw columns; the other uses linear regression on reagent dose per tonne and four other engineered features. The operator has to see which reading drove the call. Which do you recommend?",
            "help": "",
            "choices": [
              {
                "text": "The engineered features with the simpler model, whose reasoning can be read off and defended",
                "correct": true
              },
              {
                "text": "Either, since the error is what matters",
                "correct": false
              },
              {
                "text": "The random forest, because ensembles generalise better in general",
                "correct": false
              },
              {
                "text": "The random forest, and add an importance chart to explain it",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. On equal performance the stated constraint decides it, and a coefficient on a quantity with physical meaning is something you can put in front of the person who has to sign. The engineering went into the features rather than the algorithm.",
            "fbWrong": "THE ANSWER: The engineered features with the simpler model, whose reasoning can be read off and defended. On equal performance the stated constraint decides it, and a coefficient on a quantity with physical meaning is something you can put in front of the person who has to sign. The engineering went into the features rather than the algorithm.\n\nWhy the others are wrong. \u201cEither, since the error is what matters\u201d \u2014 The error was stated as a condition to meet rather than the only criterion. Explainability was given as a requirement.  \u201cThe random forest, because ensembles generalise better in general\u201d \u2014 It may well generalise better on some problems, and here the two are level while only one of them satisfies the constraint you were given.  \u201cThe random forest, and add an importance chart to explain it\u201d \u2014 Feature importance tells you which columns the model leaned on overall. It does not tell the client why this particular case was rejected, which is the question they will ask."
          }
        ]
      },
      {
        "week": 12,
        "number": 11,
        "title": "CML3113 \u00b7 Weekly Quiz 11 \u2014 Model comparison (integrative)",
        "intro": "Read what each question shows you. None of them can be answered without it.\n\nHOW THIS WORKS\n\u2022 Answer it now, in the 5 minutes on the screen. That is when this is meant to be taken, while the session is still fresh.\n\u2022 The form then stays open for 24 hours and closes itself. That window is there so a dead network or a broken phone does not cost you a mark you had earned. Take it in the room if you can: by Thursday you will have forgotten the session, and the feedback will be worth less to you.\n\u2022 ONE attempt, from your signed-in Google account. You cannot reopen it or change an answer, so read each question once, properly.\n\u2022 The first box asks for your registration number. It is the number printed on your student card, and it is how the mark reaches your record.\n\u2022 Five questions, one mark each, worth 1% of your final mark.\n\u2022 Your best ten of twelve quizzes count. Missing two costs you nothing, and there are no resits.\n\u2022 When you submit, tap View score. You get a tick or a cross on each question with the feedback underneath. Your mark is the number of ticks, and the feedback on anything you got wrong is the part worth reading.\n\u2022 A question left blank scores the same as one answered wrongly, so answer all five.",
        "questions": [
          {
            "n": 1,
            "kind": "diagnosis",
            "title": "A teammate concludes the forest is the better model. What does this table actually support?",
            "help": "fold                  1      2      3      4      5   mean\nrandom forest      0.28   0.36   0.29   0.34   0.28   0.31\nlinear reg.        0.31   0.33   0.36   0.32   0.33   0.33\ndifference        -0.03  +0.03  -0.07  +0.02  -0.05",
            "choices": [
              {
                "text": "The forest is better, because it wins the majority of folds",
                "correct": false
              },
              {
                "text": "The forest is better, since it has the stronger mean",
                "correct": false
              },
              {
                "text": "The comparison is invalid because the models share folds",
                "correct": false
              },
              {
                "text": "Very little: the difference changes sign between folds, so on this evidence the two cannot be separated",
                "correct": true
              }
            ],
            "fbCorrect": "Correct, and reading the per-fold differences is what settles it. The sign of the difference flips from fold to fold, so the mean gap of 0.02 is not a consistent advantage. Report them as level on this data and let the stated constraints decide. Note what makes this readable at all: both models were scored on the SAME five folds, so the differences can be paired up.",
            "fbWrong": "THE ANSWER: Very little: the difference changes sign between folds, so on this evidence the two cannot be separated. Reading the per-fold differences is what settles it. The sign of the difference flips from fold to fold, so the mean gap of 0.02 is not a consistent advantage. Report them as level on this data and let the stated constraints decide. Note what makes this readable at all: both models were scored on the SAME five folds, so the differences can be paired up.\n\nWhy the others are wrong. \u201cThe forest is better, because it wins the majority of folds\u201d \u2014 Winning more folds than it loses is worth noticing and is weak evidence at this margin, because the fold it loses it loses by as much as the others are won. With only five folds this pattern arises easily between two models of equal ability.  \u201cThe forest is better, since it has the stronger mean\u201d \u2014 A mean hides the fold-by-fold picture. Here the sign of the difference flips, which is the pattern of two models that are level rather than one that is ahead.  \u201cThe comparison is invalid because the models share folds\u201d \u2014 Sharing folds is what makes the comparison valid. Scoring each model on its own random split is the mistake, and it is the subject of the next question."
          },
          {
            "n": 2,
            "kind": "diagnosis",
            "title": "Two models, two scores, no error anywhere. Why can these numbers not be compared?",
            "help": "# model A\nX_tr, X_te, y_tr, y_te = train_test_split(X, y,\n                              random_state=1)\n# ... fit A ...      score 0.78\n\n# model B\nX_tr, X_te, y_tr, y_te = train_test_split(X, y,\n                              random_state=7)\n# ... fit B ...      score 0.81",
            "choices": [
              {
                "text": "The scores need to be averaged together",
                "correct": false
              },
              {
                "text": "They were scored on different test sets, so the gap may be the split rather than the model",
                "correct": true
              },
              {
                "text": "Model B had the advantage of a later random state",
                "correct": false
              },
              {
                "text": "Nothing is wrong, since both used the same data file",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. Changing the seed changes the split, and split-to-split variation on this kind of data is often larger than the gap you are trying to measure. Score every model on identical folds, which is what cross_val_score with a fixed splitter gives you.",
            "fbWrong": "THE ANSWER: They were scored on different test sets, so the gap may be the split rather than the model. Changing the seed changes the split, and split-to-split variation on this kind of data is often larger than the gap you are trying to measure. Score every model on identical folds, which is what cross_val_score with a fixed splitter gives you.\n\nWhy the others are wrong. \u201cThe scores need to be averaged together\u201d \u2014 Averaging two figures measured on different test sets produces a number that describes neither model.  \u201cModel B had the advantage of a later random state\u201d \u2014 The number in random_state is a label for a shuffle and carries no ordering. Seed 7 is not later or better than seed 1.  \u201cNothing is wrong, since both used the same data file\u201d \u2014 The same file cut two different ways gives two different test sets. The comparison needs the cuts to match."
          },
          {
            "n": 3,
            "kind": "traceback",
            "title": "You have run this notebook for an hour and now get this. What is the most likely history behind it?",
            "help": "Traceback (most recent call last):\n  File \"<ipython-input-31-9a8b7c>\", line 1, in <module>\n    print(forest.predict(X_te)[:5])\nNotFittedError: This RandomForestRegressor instance is not\nfitted yet. Call 'fit' with appropriate arguments before\nusing this estimator.",
            "choices": [
              {
                "text": "The cell that creates the model was re-run after the one that fitted it",
                "correct": true
              },
              {
                "text": "The model does not support predict on a test set",
                "correct": false
              },
              {
                "text": "The test features contain missing values",
                "correct": false
              },
              {
                "text": "The forest needs more trees before it can predict",
                "correct": false
              }
            ],
            "fbCorrect": "Correct, and this is the Week 2 out-of-order trap arriving in a much more expensive place. Re-running the constructor throws away an hour of fitting. Restart and Run All is how you find out whether your notebook still tells a straight story.",
            "fbWrong": "THE ANSWER: The cell that creates the model was re-run after the one that fitted it. This is the Week 2 out-of-order trap arriving in a much more expensive place. Re-running the constructor throws away an hour of fitting. Restart and Run All is how you find out whether your notebook still tells a straight story.\n\nWhy the others are wrong. \u201cThe model does not support predict on a test set\u201d \u2014 It does. The message is specifically that this instance has never been fitted.  \u201cThe test features contain missing values\u201d \u2014 That reports itself as an error about NaN, and it would only arise once the model was fitted.  \u201cThe forest needs more trees before it can predict\u201d \u2014 The number of trees is set at construction and any number can be fitted and used. This one was never fitted."
          },
          {
            "n": 4,
            "kind": "interpretation",
            "title": "Two outputs from the same forest. The operator needs to know which reading drove THIS call. Which output answers that, and what does the other one tell you?",
            "help": "A   feature_importances_ over the whole training set\n      starch dose      0.41\n      iron feed grade  0.29\n      pulp pH          0.18\n      air flow         0.12\n\nB   contribution to the prediction for record 14:20\n      starch dose low  pushed silica up      +0.22\n      iron feed 52 %   pushed silica up      +0.15\n      pulp pH 9.4      pushed silica down    -0.04",
            "choices": [
              {
                "text": "B answers it, because it is specific to this case; A describes the model's average behaviour across all cases",
                "correct": true
              },
              {
                "text": "A answers it, because the highest-importance feature is the reason for any given decision",
                "correct": false
              },
              {
                "text": "Both answer it equally well, since they rank the same features",
                "correct": false
              },
              {
                "text": "Neither answers it, because a forest can never be explained at all",
                "correct": false
              }
            ],
            "fbCorrect": "Correct, and the distinction is worth holding on to. A global importance chart says what the model relies on in general and can never say why one case came out as it did. A per-case breakdown is what a client's question actually needs.",
            "fbWrong": "THE ANSWER: B answers it, because it is specific to this case; A describes the model's average behaviour across all cases. The distinction is worth holding on to. A global importance chart says what the model relies on in general and can never say why one case came out as it did. A per-case breakdown is what a client's question actually needs.\n\nWhy the others are wrong. \u201cA answers it, because the highest-importance feature is the reason for any given decision\u201d \u2014 That does not follow. The most important feature overall can be unremarkable in this particular case, and here B shows a different feature leading for batch-level reasons.  \u201cBoth answer it equally well, since they rank the same features\u201d \u2014 They do not even rank them the same way, and more importantly they answer different questions. One is about the model, the other about a case.  \u201cNeither answers it, because a forest can never be explained at all\u201d \u2014 Too pessimistic. Per-case attributions like B are exactly how you interrogate one prediction from an ensemble. The honest caveat is that they are estimates of the contribution rather than a rule you can read off."
          },
          {
            "n": 5,
            "kind": "judgement",
            "title": "The metallurgist asks: your model says lower the amina flow. Our acceptance requirement is an exact, directly readable rule; post-hoc attribution is insufficient. Can this model meet it? You chose the forest. What is the honest position?",
            "help": "",
            "choices": [
              {
                "text": "Explain that the model is accurate and ask them to trust the result",
                "correct": false
              },
              {
                "text": "Offer to retrain the forest with fewer trees so it is simpler",
                "correct": false
              },
              {
                "text": "Show the feature importance chart as the explanation",
                "correct": false
              },
              {
                "text": "Recommend a readable-rule model that meets the stated acceptance requirement",
                "correct": true
              }
            ],
            "fbCorrect": "Correct. The professional answer is to name the limitation and change the recommendation. A stated condition of acceptance that your chosen model cannot meet is a reason to change the model rather than to talk around it.",
            "fbWrong": "THE ANSWER: Recommend a readable-rule model that meets the stated acceptance requirement. The professional answer is to name the limitation and change the recommendation. A stated condition of acceptance that your chosen model cannot meet is a reason to change the model rather than to talk around it.\n\nWhy the others are wrong. \u201cExplain that the model is accurate and ask them to trust the result\u201d \u2014 They told you at the outset that they cannot act on an unexplained call. Asking for trust instead is not an answer.  \u201cOffer to retrain the forest with fewer trees so it is simpler\u201d \u2014 A smaller forest still does not meet this stated requirement for a directly readable rule. This concedes accuracy without gaining explainability.  \u201cShow the feature importance chart as the explanation\u201d \u2014 Importance describes the model's behaviour across the whole dataset. It cannot say why one case was decided as it was, which is the question you were asked."
          }
        ]
      },
      {
        "week": 13,
        "number": 12,
        "title": "CML3113 \u00b7 Weekly Quiz 12 \u2014 Reproducibility (integrative)",
        "intro": "Read what each question shows you. None of them can be answered without it.\n\nHOW THIS WORKS\n\u2022 Answer it now, in the 5 minutes on the screen. That is when this is meant to be taken, while the session is still fresh.\n\u2022 The form then stays open for 24 hours and closes itself. That window is there so a dead network or a broken phone does not cost you a mark you had earned. Take it in the room if you can: by Thursday you will have forgotten the session, and the feedback will be worth less to you.\n\u2022 ONE attempt, from your signed-in Google account. You cannot reopen it or change an answer, so read each question once, properly.\n\u2022 The first box asks for your registration number. It is the number printed on your student card, and it is how the mark reaches your record.\n\u2022 Five questions, one mark each, worth 1% of your final mark.\n\u2022 Your best ten of twelve quizzes count. Missing two costs you nothing, and there are no resits.\n\u2022 When you submit, tap View score. You get a tick or a cross on each question with the feedback underneath. Your mark is the number of ticks, and the feedback on anything you got wrong is the part worth reading.\n\u2022 A question left blank scores the same as one answered wrongly, so answer all five.",
        "questions": [
          {
            "n": 1,
            "kind": "diagnosis",
            "title": "This runs perfectly on the machine it was written on. What is wrong with it?",
            "help": "df = pd.read_csv(\n    \"C:/Users/Jotham/Desktop/flotation_final_v3.csv\")",
            "choices": [
              {
                "text": "Nothing, as long as you send the file with the notebook",
                "correct": false
              },
              {
                "text": "It names a location that exists on exactly one computer, so the notebook cannot run anywhere else",
                "correct": true
              },
              {
                "text": "The file should be read with a different pandas function",
                "correct": false
              },
              {
                "text": "Backslashes should have been used for a Windows path",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. Keep the data inside the project and read it by a relative path such as data/\u2026 so the notebook works for anyone who has the folder. The version marker in the file name is a second warning: it suggests there are other copies and no record of which is current.",
            "fbWrong": "THE ANSWER: It names a location that exists on exactly one computer, so the notebook cannot run anywhere else. Keep the data inside the project and read it by a relative path such as data/\u2026 so the notebook works for anyone who has the folder. The version marker in the file name is a second warning: it suggests there are other copies and no record of which is current.\n\nWhy the others are wrong. \u201cNothing, as long as you send the file with the notebook\u201d \u2014 The recipient would have to recreate your user name and your desktop for the path to resolve. A relative path inside the project removes the problem entirely.  \u201cThe file should be read with a different pandas function\u201d \u2014 read_csv is the right function for a CSV. The path is the problem.  \u201cBackslashes should have been used for a Windows path\u201d \u2014 Forward slashes work on Windows in Python and avoid the escape problems backslashes cause. This is the better of the two styles and the location is still wrong."
          },
          {
            "n": 2,
            "kind": "diagnosis",
            "title": "You run the same notebook twice, changing nothing, and get these two numbers. What is going on, and what should you do?",
            "help": "run 1:   MAE 0.31 pts\nrun 2:   MAE 0.36 pts",
            "choices": [
              {
                "text": "The data file is being modified between runs",
                "correct": false
              },
              {
                "text": "Report the average of the two runs",
                "correct": false
              },
              {
                "text": "The split and the model involve randomness that was never pinned down",
                "correct": true
              },
              {
                "text": "The second run is the more trustworthy of the two",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. Without a seed, the rows that land in the test set and the internal choices a forest makes change every run. Set random_state on the split and on the model, and write the number in the notebook so a reader can reproduce your figure exactly.",
            "fbWrong": "THE ANSWER: The split and the model involve randomness that was never pinned down. Without a seed, the rows that land in the test set and the internal choices a forest makes change every run. Set random_state on the split and on the model, and write the number in the notebook so a reader can reproduce your figure exactly.\n\nWhy the others are wrong. \u201cThe data file is being modified between runs\u201d \u2014 Nothing here writes to the file. Unseeded randomness explains this without needing the data to change.  \u201cReport the average of the two runs\u201d \u2014 An average of two arbitrary draws is still arbitrary. Seed the randomness, and if you want a figure with a spread, cross-validate deliberately.  \u201cThe second run is the more trustworthy of the two\u201d \u2014 Neither is more trustworthy. That two runs differ by this much is itself the finding, and it says your single reported figure carries this much uncertainty."
          },
          {
            "n": 3,
            "kind": "traceback",
            "title": "A classmate clones your repository and gets this on the first cell. What is the cause?",
            "help": "Traceback (most recent call last):\n  File \"<ipython-input-1-3e4f5a>\", line 1, in <module>\n    df = pd.read_csv(\"flotation_subset.csv\")\nFileNotFoundError: [Errno 2] No such file or directory:\n'flotation_subset.csv'",
            "choices": [
              {
                "text": "The repository was cloned incorrectly",
                "correct": false
              },
              {
                "text": "The data file was never committed, or sits elsewhere",
                "correct": true
              },
              {
                "text": "The classmate is missing a package",
                "correct": false
              },
              {
                "text": "The file name has the wrong extension",
                "correct": false
              }
            ],
            "fbCorrect": "Correct, and both halves are worth checking. Data is often left out of a repository deliberately because of size or licence, in which case the README has to say where to get it and where to put it. Otherwise the path needs to match the folder layout.",
            "fbWrong": "THE ANSWER: The data file was never committed, or sits elsewhere. Both halves are worth checking. Data is often left out of a repository deliberately because of size or licence, in which case the README has to say where to get it and where to put it. Otherwise the path needs to match the folder layout.\n\nWhy the others are wrong. \u201cThe repository was cloned incorrectly\u201d \u2014 A clone that failed would leave you with no notebook to run. The notebook arrived and its data did not.  \u201cThe classmate is missing a package\u201d \u2014 A missing package reports itself as ModuleNotFoundError. This message is about a file.  \u201cThe file name has the wrong extension\u201d \u2014 The extension matches a CSV read. The file is simply not at that location."
          },
          {
            "n": 4,
            "kind": "interpretation",
            "title": "Two captions for the same chart. Which one does the job a caption exists to do, and why?",
            "help": "A:  Figure 3: silica against starch flow.\n\nB:  Figure 3: concentrate silica falls as starch dose\n    rises to about 900 g per tonne of feed and flattens\n    after that.",
            "choices": [
              {
                "text": "A, because a caption should describe the chart and let the reader draw the conclusion",
                "correct": false
              },
              {
                "text": "A, because B might be wrong and the caption would then be misleading",
                "correct": false
              },
              {
                "text": "B, because it states the finding and its size, so a reader who only reads the captions still learns the result",
                "correct": true
              },
              {
                "text": "Neither; captions should give the data source instead",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. A caption is often the only part of your work that gets read. B carries the conclusion and the magnitude, which is what makes it useful and also what makes it checkable against the chart.",
            "fbWrong": "THE ANSWER: B, because it states the finding and its size, so a reader who only reads the captions still learns the result. A caption is often the only part of your work that gets read. B carries the conclusion and the magnitude, which is what makes it useful and also what makes it checkable against the chart.\n\nWhy the others are wrong. \u201cA, because a caption should describe the chart and let the reader draw the conclusion\u201d \u2014 A describes the axes, which the axis labels already do. It leaves the reader to rediscover something you already know.  \u201cA, because B might be wrong and the caption would then be misleading\u201d \u2014 A claim you can check is a feature. If B is wrong the chart will show it, whereas A cannot be wrong because it says nothing.  \u201cNeither; captions should give the data source instead\u201d \u2014 The source belongs in the caption or nearby and does not replace the finding. B plus a source is the target."
          },
          {
            "n": 5,
            "kind": "judgement",
            "title": "Your notebook has three separate cells that each assign df, and nobody wrote down the order they should run in. Submission is tomorrow. What do you do?",
            "help": "",
            "choices": [
              {
                "text": "Leave it, since you know the right order",
                "correct": false
              },
              {
                "text": "Restart and Run All, then fix whatever breaks until it runs clean from top to bottom",
                "correct": true
              },
              {
                "text": "Delete two of the three cells and hope the notebook still runs",
                "correct": false
              },
              {
                "text": "Add a comment above each cell saying what order to run them in",
                "correct": false
              }
            ],
            "fbCorrect": "Correct, and do it before you are tired. That single action converts a notebook that works on your screen into one that works from an empty memory, which is the only version anyone else can use. Consolidating the three assignments into one clear sequence is usually the fix.",
            "fbWrong": "THE ANSWER: Restart and Run All, then fix whatever breaks until it runs clean from top to bottom. Do it before you are tired. That single action converts a notebook that works on your screen into one that works from an empty memory, which is the only version anyone else can use. Consolidating the three assignments into one clear sequence is usually the fix.\n\nWhy the others are wrong. \u201cLeave it, since you know the right order\u201d \u2014 That knowledge is not in the file, so it does not survive you. It also will not survive next week for you either.  \u201cDelete two of the three cells and hope the notebook still runs\u201d \u2014 Each of them may be doing something needed. Running from a clean state tells you what is required rather than leaving you to guess.  \u201cAdd a comment above each cell saying what order to run them in\u201d \u2014 Instructions to run cells out of order are a description of the problem. Anyone who follows them slightly differently gets a different answer."
          }
        ]
      }
    ]
  },
  "CML3111": {
    "meta": {
      "name": "Electrical, Mechatronics & Robotics, Communications",
      "day": "Friday 11:00"
    },
    "weeks": [
      {
        "week": 1,
        "number": 1,
        "title": "CML3111 \u00b7 Weekly Quiz 1 \u2014 What machine learning is",
        "intro": "Nothing here can be answered without reading what it shows you.\n\nHOW THIS WORKS\n\u2022 Answer it now, in the 5 minutes on the screen. That is when this is meant to be taken, while the session is still fresh.\n\u2022 The form then stays open for 24 hours and closes itself. That window is there so a dead network or a broken phone does not cost you a mark you had earned. Take it in the room if you can: by Thursday you will have forgotten the session, and the feedback will be worth less to you.\n\u2022 ONE attempt, from your signed-in Google account. You cannot reopen it or change an answer, so read each question once, properly.\n\u2022 The first box asks for your registration number. It is the number printed on your student card, and it is how the mark reaches your record.\n\u2022 Five questions, one mark each, worth 1% of your final mark.\n\u2022 Your best ten of twelve quizzes count. Missing two costs you nothing, and there are no resits.\n\u2022 When you submit, tap View score. You get a tick or a cross on each question with the feedback underneath. Your mark is the number of ticks, and the feedback on anything you got wrong is the part worth reading.\n\u2022 A question left blank scores the same as one answered wrongly, so answer all five.",
        "questions": [
          {
            "n": 1,
            "kind": "interpretation",
            "title": "In the table below, which column is the TARGET?",
            "help": "hour_id  air_temp  rot_speed  torque_nm  failed\nH-001        298.4       1551       42.8       0\nH-002        299.1       1408       46.3       0\nH-003        300.2       1379       61.7       1",
            "choices": [
              {
                "text": "air_temp",
                "correct": false
              },
              {
                "text": "torque_nm",
                "correct": false
              },
              {
                "text": "hour_id",
                "correct": false
              },
              {
                "text": "failed",
                "correct": true
              }
            ],
            "fbCorrect": "Correct. It is what you want to know in advance, and the only column here you would not have before the fact.",
            "fbWrong": "THE ANSWER: failed. It is what you want to know in advance, and the only column here you would not have before the fact.\n\nWhy the others are wrong. \u201cair_temp\u201d \u2014 That is a feature, measured continuously by the plant.  \u201ctorque_nm\u201d \u2014 That is a feature: a sensor reading available while the machine is running.  \u201chour_id\u201d \u2014 That is an identifier. It labels the row and predicts nothing."
          },
          {
            "n": 2,
            "kind": "interpretation",
            "title": "You want to predict, for the next shift, whether a machine will fail or not. What kind of problem is this?",
            "help": "",
            "choices": [
              {
                "text": "Regression, because there are more than two possible answers",
                "correct": false
              },
              {
                "text": "Regression, because the underlying quantity is a number",
                "correct": false
              },
              {
                "text": "Neither, because it can be written as a rule with thresholds",
                "correct": false
              },
              {
                "text": "Classification, because the answer is one of a fixed set of categories",
                "correct": true
              }
            ],
            "fbCorrect": "Correct. The answer is a label from a fixed list, so it is classification, and it is scored with a confusion matrix rather than an average error.",
            "fbWrong": "THE ANSWER: Classification, because the answer is one of a fixed set of categories. The answer is a label from a fixed list, so it is classification, and it is scored with a confusion matrix rather than an average error.\n\nWhy the others are wrong. \u201cRegression, because there are more than two possible answers\u201d \u2014 The number of possible answers does not decide this. Classification with three classes is still classification.  \u201cRegression, because the underlying quantity is a number\u201d \u2014 The underlying quantity is a number, but the question asked is not. You are asked which band or class it falls into, and a band is a category. What decides this is the question you were asked rather than the quantity the sensor happens to record.  \u201cNeither, because it can be written as a rule with thresholds\u201d \u2014 If you already have the strength or the grade then yes, a rule is the right tool and there is nothing to learn. The point here is that you do not have it yet."
          },
          {
            "n": 3,
            "kind": "diagnosis",
            "title": "A team proposes to predict the target using the list of columns below. One column makes the whole exercise meaningless. Which one, and why?",
            "help": "target:   whether the machine failed in the next shift\nfeatures: air_temp, rot_speed, torque_nm,\n          maintenance_action_taken",
            "choices": [
              {
                "text": "maintenance_action_taken \u2014 it is recorded in response to the failure, so it only exists once the answer is known",
                "correct": true
              },
              {
                "text": "rot_speed \u2014 it is set by the controller rather than measured",
                "correct": false
              },
              {
                "text": "None of them; the list is fine",
                "correct": false
              },
              {
                "text": "air_temp \u2014 ambient temperature does not cause a bearing to fail",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. Ask the timing question: at the moment I need this prediction, would I have this? The maintenance action follows the failure, so it cannot precede the prediction.",
            "fbWrong": "THE ANSWER: maintenance_action_taken \u2014 it is recorded in response to the failure, so it only exists once the answer is known. Ask the timing question: at the moment I need this prediction, would I have this? The maintenance action follows the failure, so it cannot precede the prediction.\n\nWhy the others are wrong. \u201crot_speed \u2014 it is set by the controller rather than measured\u201d \u2014 A commanded value is still available at prediction time. That raises a provenance question and it is not a fatal one.  \u201cNone of them; the list is fine\u201d \u2014 One of these columns is only recorded after the outcome. Ask the timing question of each one.  \u201cair_temp \u2014 ambient temperature does not cause a bearing to fail\u201d \u2014 A weak feature is not a fatal feature. It may contribute little and the ablation table in Week 11 is how you find that out."
          },
          {
            "n": 4,
            "kind": "interpretation",
            "title": "The motor datasheet gives a 130 \u00b0C alarm limit, and you have the winding temperature. What should you build?",
            "help": "",
            "choices": [
              {
                "text": "A classifier trained on past decisions",
                "correct": false
              },
              {
                "text": "A rule with a threshold, written directly in code",
                "correct": true
              },
              {
                "text": "Either; the choice is a matter of preference",
                "correct": false
              },
              {
                "text": "A regression model to predict the threshold",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. You have the input and you have the threshold, so there is nothing to learn. Training a model to rediscover a published limit adds error and removes the audit trail.",
            "fbWrong": "THE ANSWER: A rule with a threshold, written directly in code. You have the input and you have the threshold, so there is nothing to learn. Training a model to rediscover a published limit adds error and removes the audit trail.\n\nWhy the others are wrong. \u201cA classifier trained on past decisions\u201d \u2014 It would work, and that is what makes this tempting. It would also be less accurate than the rule, harder to defend and impossible to audit against the code of practice.  \u201cEither; the choice is a matter of preference\u201d \u2014 The choice follows from whether you already have the input and the threshold. Here you have both, so the rule wins on every axis.  \u201cA regression model to predict the threshold\u201d \u2014 The threshold is given. There is nothing to predict about it."
          },
          {
            "n": 5,
            "kind": "judgement",
            "title": "A client will only accept a system if every decision it makes can be explained line by line to a regulator. Two candidate approaches perform identically on your data. Which do you recommend, and on what grounds?",
            "help": "",
            "choices": [
              {
                "text": "The one whose decisions can be read out and traced, because the constraint decides it once performance is equal",
                "correct": true
              },
              {
                "text": "Neither; tell the client the constraint is unreasonable",
                "correct": false
              },
              {
                "text": "Whichever scored fractionally higher on the test set",
                "correct": false
              },
              {
                "text": "The more sophisticated one, because it will generalise better",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. When performance is equal the constraint is the deciding criterion, and explainability was stated as a condition of acceptance rather than a preference.",
            "fbWrong": "THE ANSWER: The one whose decisions can be read out and traced, because the constraint decides it once performance is equal. When performance is equal the constraint is the deciding criterion, and explainability was stated as a condition of acceptance rather than a preference.\n\nWhy the others are wrong. \u201cNeither; tell the client the constraint is unreasonable\u201d \u2014 Regulatory explainability is a normal engineering constraint. Part of the job is delivering within it.  \u201cWhichever scored fractionally higher on the test set\u201d \u2014 A fractional difference on one test set is usually inside the noise, and Week 10 shows you how to measure that. Even a real difference would not override a stated condition of acceptance.  \u201cThe more sophisticated one, because it will generalise better\u201d \u2014 Sophistication does not imply generalisation, and on equal performance there is no evidence for the claim. It also ignores the constraint you were given."
          }
        ]
      },
      {
        "week": 2,
        "number": 2,
        "title": "CML3111 \u00b7 Weekly Quiz 2 \u2014 Notebooks and version control",
        "intro": "Read what each question shows you. None of them can be answered without it.\n\nHOW THIS WORKS\n\u2022 Answer it now, in the 5 minutes on the screen. That is when this is meant to be taken, while the session is still fresh.\n\u2022 The form then stays open for 24 hours and closes itself. That window is there so a dead network or a broken phone does not cost you a mark you had earned. Take it in the room if you can: by Thursday you will have forgotten the session, and the feedback will be worth less to you.\n\u2022 ONE attempt, from your signed-in Google account. You cannot reopen it or change an answer, so read each question once, properly.\n\u2022 The first box asks for your registration number. It is the number printed on your student card, and it is how the mark reaches your record.\n\u2022 Five questions, one mark each, worth 1% of your final mark.\n\u2022 Your best ten of twelve quizzes count. Missing two costs you nothing, and there are no resits.\n\u2022 When you submit, tap View score. You get a tick or a cross on each question with the feedback underneath. Your mark is the number of ticks, and the feedback on anything you got wrong is the part worth reading.\n\u2022 A question left blank scores the same as one answered wrongly, so answer all five.",
        "questions": [
          {
            "n": 1,
            "kind": "interpretation",
            "title": "The numbers in the square brackets are the order the cells were actually run. The notebook now reads as shown. Why does it print 10?",
            "help": "In [1]:  motors_tested = 40\nIn [2]:  quota = 30\nIn [5]:  motors_tested = 55\nIn [3]:  spare = motors_tested - quota\nIn [4]:  print(spare)\n         10",
            "choices": [
              {
                "text": "Python read the cells from the top of the page downwards",
                "correct": false
              },
              {
                "text": "The variable was never given the second value at all",
                "correct": false
              },
              {
                "text": "The subtraction ran while the first value was still in memory, and the cell that replaced it ran afterwards",
                "correct": true
              },
              {
                "text": "The notebook cached the printed output and did not refresh it",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. Read the bracket numbers as a timeline: 1, 2, 3, 4, then 5. The subtraction happened at step 3 on the old value, and the replacement only happened at step 5. What you see on screen is the code; what produced the 10 is the order it ran.",
            "fbWrong": "THE ANSWER: The subtraction ran while the first value was still in memory, and the cell that replaced it ran afterwards. Read the bracket numbers as a timeline: 1, 2, 3, 4, then 5. The subtraction happened at step 3 on the old value, and the replacement only happened at step 5. What you see on screen is the code; what produced the 10 is the order it ran.\n\nWhy the others are wrong. \u201cPython read the cells from the top of the page downwards\u201d \u2014 That is the assumption this question exists to break. A notebook runs cells in whatever order you click them, and the bracket numbers are the record of that order.  \u201cThe variable was never given the second value at all\u201d \u2014 It was, at step 5. That is precisely why the code on screen and the number underneath it disagree.  \u201cThe notebook cached the printed output and did not refresh it\u201d \u2014 Notebooks do keep an old output on screen after you edit a cell, but the value here was genuinely computed from the earlier number. Nothing is stale about the 10 itself."
          },
          {
            "n": 2,
            "kind": "interpretation",
            "title": "Read the two states below. What has Restart and Run All established?",
            "help": "before:  In [7]  In [3]  In [12]  In [4]  In [9]\n         (outputs on screen, run in some past order)\n\nafter:   In [1]  In [2]  In [3]   In [4]  In [5]\n         (no errors, and the same outputs as before)",
            "choices": [
              {
                "text": "That the notebook will run on a classmate's machine",
                "correct": false
              },
              {
                "text": "That the results are statistically reliable",
                "correct": false
              },
              {
                "text": "That the code is correct",
                "correct": false
              },
              {
                "text": "That it produces those outputs from an empty memory, in page order",
                "correct": true
              }
            ],
            "fbCorrect": "Correct, and that is a narrow claim worth having. The counts now run 1 to 5 in page order, which rules out the out-of-order trap and any variable that only survived because of a cell you later deleted.",
            "fbWrong": "THE ANSWER: That it produces those outputs from an empty memory, in page order. That is a narrow claim worth having. The counts now run 1 to 5 in page order, which rules out the out-of-order trap and any variable that only survived because of a cell you later deleted.\n\nWhy the others are wrong. \u201cThat the notebook will run on a classmate's machine\u201d \u2014 That needs the same packages, the same Python version and the data file reachable at the same relative path. Week 13 is about exactly this gap.  \u201cThat the results are statistically reliable\u201d \u2014 Reproducing an output says nothing about whether the number was worth computing. A notebook can faithfully reproduce a meaningless average every time you run it.  \u201cThat the code is correct\u201d \u2014 It establishes that the code runs and reproduces its own outputs. Code can run cleanly from top to bottom and still compute the wrong quantity, which is what the diagnosis questions from Week 3 onwards are about."
          },
          {
            "n": 3,
            "kind": "traceback",
            "title": "You have been working for an hour, the variable is plainly assigned in a cell further up the page, and running the cell at the bottom gives this. What is the most likely cause?",
            "help": "Traceback (most recent call last):\n  File \"<ipython-input-2-a1b2c3>\", line 1, in <module>\n    print(mean_temp)\nNameError: name 'mean_temp' is not defined",
            "choices": [
              {
                "text": "The variable holds nothing, so printing it fails",
                "correct": false
              },
              {
                "text": "The name is a reserved word in Python",
                "correct": false
              },
              {
                "text": "The notebook needs a library imported before it can print",
                "correct": false
              },
              {
                "text": "The cell that creates it has not actually been run in this session, whatever the page shows",
                "correct": true
              }
            ],
            "fbCorrect": "Correct. Being written on the page and having been executed are different things: the kernel only knows what it has run. Either that cell was never run, or the kernel was restarted since. Restart and Run All settles it in one step.",
            "fbWrong": "THE ANSWER: The cell that creates it has not actually been run in this session, whatever the page shows. Being written on the page and having been executed are different things: the kernel only knows what it has run. Either that cell was never run, or the kernel was restarted since. Restart and Run All settles it in one step.\n\nWhy the others are wrong. \u201cThe variable holds nothing, so printing it fails\u201d \u2014 A variable holding nothing still exists and prints happily as None. This error says the name itself is unknown to Python.  \u201cThe name is a reserved word in Python\u201d \u2014 It is an ordinary name. A reserved word would be reported as a SyntaxError while the cell was being read, before it ran.  \u201cThe notebook needs a library imported before it can print\u201d \u2014 print is built in and needs no import. A missing library reports itself as ModuleNotFoundError."
          },
          {
            "n": 4,
            "kind": "interpretation",
            "title": "Read this output. Which statement is true?",
            "help": "$ git status\nOn branch main\nChanges not staged for commit:\n        modified:   analysis.ipynb\nUntracked files:\n        data/motor_test_bench.csv",
            "choices": [
              {
                "text": "Both files will be saved by the next commit",
                "correct": false
              },
              {
                "text": "The notebook has been committed and the CSV has been deleted",
                "correct": false
              },
              {
                "text": "The notebook is tracked and edited; the CSV was never added",
                "correct": true
              },
              {
                "text": "The repository is broken and needs to be created again",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. Git reports a tracked file as modified and a file it has never seen as untracked. Stage the notebook edit with git add before committing. A bare commit saves neither file here.",
            "fbWrong": "THE ANSWER: The notebook is tracked and edited; the CSV was never added. Git reports a tracked file as modified and a file it has never seen as untracked. Stage the notebook edit with git add before committing. A bare commit saves neither file here.\n\nWhy the others are wrong. \u201cBoth files will be saved by the next commit\u201d \u2014 Neither will. The notebook change is unstaged and the CSV is untracked, so a bare commit captures nothing from this list.  \u201cThe notebook has been committed and the CSV has been deleted\u201d \u2014 A committed file with no further edits does not appear in this output at all, and a deletion is reported as deleted.  \u201cThe repository is broken and needs to be created again\u201d \u2014 This is the ordinary output of a healthy repository with work in progress. It is the state you should expect to see most of the time."
          },
          {
            "n": 5,
            "kind": "judgement",
            "title": "It is twenty minutes before the session. The Python install on your laptop fails with an error you have not seen before. What is the right move?",
            "help": "",
            "choices": [
              {
                "text": "Copy a classmate's notebook afterwards and read through it",
                "correct": false
              },
              {
                "text": "Open Colab in the browser and work there for the session",
                "correct": true
              },
              {
                "text": "Ask for the session to be repeated later in the week",
                "correct": false
              },
              {
                "text": "Spend the session fixing the install so the rest of the semester is smooth",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. Colab needs a browser and nothing else, which is why this course is built on it. Your install can be repaired at a time when it is not costing you a three-hour session.",
            "fbWrong": "THE ANSWER: Open Colab in the browser and work there for the session. Colab needs a browser and nothing else, which is why this course is built on it. Your install can be repaired at a time when it is not costing you a three-hour session.\n\nWhy the others are wrong. \u201cCopy a classmate's notebook afterwards and read through it\u201d \u2014 Reading someone else's finished notebook skips the part that does the teaching. You would arrive at Week 3 without having run a single cell yourself.  \u201cAsk for the session to be repeated later in the week\u201d \u2014 There is no second slot: each cohort meets once a week. A working browser removes the problem in under a minute.  \u201cSpend the session fixing the install so the rest of the semester is smooth\u201d \u2014 This trades a guaranteed three hours of teaching for a repair of unknown length. Install problems are often version mismatches with no quick fix, which is why the browser route exists."
          }
        ]
      },
      {
        "week": 3,
        "number": 3,
        "title": "CML3111 \u00b7 Weekly Quiz 3 \u2014 Python as an engineering calculator",
        "intro": "Read what each question shows you. None of them can be answered without it.\n\nHOW THIS WORKS\n\u2022 Answer it now, in the 5 minutes on the screen. That is when this is meant to be taken, while the session is still fresh.\n\u2022 The form then stays open for 24 hours and closes itself. That window is there so a dead network or a broken phone does not cost you a mark you had earned. Take it in the room if you can: by Thursday you will have forgotten the session, and the feedback will be worth less to you.\n\u2022 ONE attempt, from your signed-in Google account. You cannot reopen it or change an answer, so read each question once, properly.\n\u2022 The first box asks for your registration number. It is the number printed on your student card, and it is how the mark reaches your record.\n\u2022 Five questions, one mark each, worth 1% of your final mark.\n\u2022 Your best ten of twelve quizzes count. Missing two costs you nothing, and there are no resits.\n\u2022 When you submit, tap View score. You get a tick or a cross on each question with the feedback underneath. Your mark is the number of ticks, and the feedback on anything you got wrong is the part worth reading.\n\u2022 A question left blank scores the same as one answered wrongly, so answer all five.",
        "questions": [
          {
            "n": 1,
            "kind": "diagnosis",
            "title": "This runs without any error and prints the number shown. What is wrong?",
            "help": "def mechanical_power(torque_nm, rpm):\n    return torque_nm * rpm * 2 * 3.14159 / 60.0\n\np_out = mechanical_power(8.5, 151.8)\nprint(f\"shaft power {p_out:.0f} W\")\n\nshaft power 135 W",
            "choices": [
              {
                "text": "Torque and speed were given in the wrong order",
                "correct": false
              },
              {
                "text": "The speed was passed in radians per second to a parameter measured in revolutions per minute",
                "correct": true
              },
              {
                "text": "Nothing is wrong; 135 W is normal for a small motor",
                "correct": false
              },
              {
                "text": "The constant should be 3.14159 divided by two",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. 1450 rpm is 151.8 rad/s, so the value handed in had already been converted once. Passing 1450 gives 1291 W, which is the right answer for this motor.",
            "fbWrong": "THE ANSWER: The speed was passed in radians per second to a parameter measured in revolutions per minute. 1450 rpm is 151.8 rad/s, so the value handed in had already been converted once. Passing 1450 gives 1291 W, which is the right answer for this motor.\n\nWhy the others are wrong. \u201cTorque and speed were given in the wrong order\u201d \u2014 Multiplication gives the same product either way, so a swap of these two would not change the number. Check the units instead.  \u201cNothing is wrong; 135 W is normal for a small motor\u201d \u2014 It is a plausible-looking figure, which is what makes this dangerous. Check it against the inputs on the line above: 8.5 N\u00b7m at 1450 rpm is about 1.3 kW, so 135 W means the torque or the speed is out by roughly a factor of ten.  \u201cThe constant should be 3.14159 divided by two\u201d \u2014 The 2 pi over 60 converts revolutions per minute into radians per second inside the function. That algebra is correct."
          },
          {
            "n": 2,
            "kind": "diagnosis",
            "title": "This function runs without error. The printed answer is wrong and dangerous. Why?",
            "help": "def temp_action(winding_c, ambient_c):\n    rise = winding_c - ambient_c\n    if rise > 80:\n        return \"investigate cooling\"\n    elif winding_c > 155:\n        return \"trip\"\n    elif winding_c > 130:\n        return \"alarm\"\n    else:\n        return \"normal\"\n\nprint(temp_action(162.0, 25.0))\ninvestigate cooling",
            "choices": [
              {
                "text": "Ambient temperature should not affect the decision",
                "correct": false
              },
              {
                "text": "The temperature rise is tested first, so a winding hot enough to trip only returns the cooling message",
                "correct": true
              },
              {
                "text": "The rise should be compared against the winding temperature",
                "correct": false
              },
              {
                "text": "The trip and alarm limits have been swapped",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. The rise of 137 K clears the 80 K test, so the function returns before it can look at 155. A winding at 162 \u00b0C should trip. Order the branches with the most severe outcome first.",
            "fbWrong": "THE ANSWER: The temperature rise is tested first, so a winding hot enough to trip only returns the cooling message. The rise of 137 K clears the 80 K test, so the function returns before it can look at 155. A winding at 162 \u00b0C should trip. Order the branches with the most severe outcome first.\n\nWhy the others are wrong. \u201cAmbient temperature should not affect the decision\u201d \u2014 A rise test catches a cooling fault that an absolute limit misses, so it earns its place. It simply must not be consulted before the trip limit.  \u201cThe rise should be compared against the winding temperature\u201d \u2014 A temperature rise is the winding temperature minus ambient, which is what the code computes. That line is right.  \u201cThe trip and alarm limits have been swapped\u201d \u2014 155 for trip and 130 for alarm is the correct way round for this insulation class. Both branches are correct and neither is reached."
          },
          {
            "n": 3,
            "kind": "traceback",
            "title": "What does this tell you about the variable?",
            "help": "Traceback (most recent call last):\n  File \"<ipython-input-5-9f8e7d>\", line 2, in <module>\n    total_load = load + 2.5\nTypeError: can only concatenate str (not \"float\") to str",
            "choices": [
              {
                "text": "It holds text, so the plus sign was read as joining strings and a number cannot be joined to text",
                "correct": true
              },
              {
                "text": "The 2.5 should have been written as an integer",
                "correct": false
              },
              {
                "text": "The variable was never assigned a value",
                "correct": false
              },
              {
                "text": "It holds a number that is too large for the addition",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. The word concatenate is the clue: Python was trying to stick things together rather than add them. Values typed in or read from a file arrive as text, and float() converts them.",
            "fbWrong": "THE ANSWER: It holds text, so the plus sign was read as joining strings and a number cannot be joined to text. The word concatenate is the clue: Python was trying to stick things together rather than add them. Values typed in or read from a file arrive as text, and float() converts them.\n\nWhy the others are wrong. \u201cThe 2.5 should have been written as an integer\u201d \u2014 Adding an integer to text fails in exactly the same way. The type of the variable is what has to change.  \u201cThe variable was never assigned a value\u201d \u2014 That reports itself as a NameError. This variable exists and holds something; the something is text.  \u201cIt holds a number that is too large for the addition\u201d \u2014 Python integers grow as large as memory allows, and floats would report an overflow differently. The message names the type as str."
          },
          {
            "n": 4,
            "kind": "interpretation",
            "title": "Reading this function as written, what does the call return?",
            "help": "def temp_action(winding_c, ambient_c):\n    rise = winding_c - ambient_c\n    if winding_c > 155:\n        return \"trip\"\n    elif winding_c > 130:\n        return \"alarm\"\n    elif rise > 80:\n        return \"investigate cooling\"\n    else:\n        return \"normal\"\n\ntemp_action(120.0, 25.0)",
            "choices": [
              {
                "text": "investigate cooling",
                "correct": true
              },
              {
                "text": "alarm",
                "correct": false
              },
              {
                "text": "normal",
                "correct": false
              },
              {
                "text": "trip",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. 120 \u00b0C is under both the trip and alarm limits, and the rise of 95 K is above 80, so the third branch matches. This is the case an absolute limit alone would miss.",
            "fbWrong": "THE ANSWER: investigate cooling. 120 \u00b0C is under both the trip and alarm limits, and the rise of 95 K is above 80, so the third branch matches. This is the case an absolute limit alone would miss.\n\nWhy the others are wrong. \u201calarm\u201d \u2014 The alarm branch needs a winding above 130 \u00b0C. This one is at 120 \u00b0C.  \u201cnormal\u201d \u2014 That is what you get by checking only the two absolute limits. The rise of 95 K says this machine is not shedding heat properly.  \u201ctrip\u201d \u2014 The trip branch needs a winding above 155 \u00b0C."
          },
          {
            "n": 5,
            "kind": "judgement",
            "title": "A teammate has written the 130 \u00b0C alarm limit directly into three different cells. The code works. What should you do?",
            "help": "",
            "choices": [
              {
                "text": "Leave it, because the code produces the right answers today",
                "correct": false
              },
              {
                "text": "Put it in one named constant and refer to that everywhere",
                "correct": true
              },
              {
                "text": "Write a function that looks the limit up online each time",
                "correct": false
              },
              {
                "text": "Ask each teammate to remember which cells contain it",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. When the standard is revised you change one line and can point to it. Three copies means three chances to update two of them and ship a notebook that applies two different limits in the same analysis.",
            "fbWrong": "THE ANSWER: Put it in one named constant and refer to that everywhere. When the standard is revised you change one line and can point to it. Three copies means three chances to update two of them and ship a notebook that applies two different limits in the same analysis.\n\nWhy the others are wrong. \u201cLeave it, because the code produces the right answers today\u201d \u2014 It does work today. The cost arrives on the day the figure changes, and it arrives as an inconsistency nobody notices because every cell still runs.  \u201cWrite a function that looks the limit up online each time\u201d \u2014 That makes the notebook depend on a network and on somebody else's page layout. A named constant with a comment citing the clause is auditable and works offline.  \u201cAsk each teammate to remember which cells contain it\u201d \u2014 Relying on memory across a fifteen-week project with several people is how the two-out-of-three update happens."
          }
        ]
      },
      {
        "week": 4,
        "number": 4,
        "title": "CML3111 \u00b7 Weekly Quiz 4 \u2014 Collections, loops and files",
        "intro": "Read what each question shows you. None of them can be answered without it.\n\nHOW THIS WORKS\n\u2022 Answer it now, in the 5 minutes on the screen. That is when this is meant to be taken, while the session is still fresh.\n\u2022 The form then stays open for 24 hours and closes itself. That window is there so a dead network or a broken phone does not cost you a mark you had earned. Take it in the room if you can: by Thursday you will have forgotten the session, and the feedback will be worth less to you.\n\u2022 ONE attempt, from your signed-in Google account. You cannot reopen it or change an answer, so read each question once, properly.\n\u2022 The first box asks for your registration number. It is the number printed on your student card, and it is how the mark reaches your record.\n\u2022 Five questions, one mark each, worth 1% of your final mark.\n\u2022 Your best ten of twelve quizzes count. Missing two costs you nothing, and there are no resits.\n\u2022 When you submit, tap View score. You get a tick or a cross on each question with the feedback underneath. Your mark is the number of ticks, and the feedback on anything you got wrong is the part worth reading.\n\u2022 A question left blank scores the same as one answered wrongly, so answer all five.",
        "questions": [
          {
            "n": 1,
            "kind": "diagnosis",
            "title": "This runs cleanly and prints the mean shown. The mean is wrong. What causes it?",
            "help": "temps = [118, 131, 126, 141]\ntotal = 0.0\nfor t in temps:\n    total = 0.0\n    total = total + t\n\nprint(f\"mean temp {total / len(temps):.2f} C\")\nmean temp 35.25 C",
            "choices": [
              {
                "text": "The temperatures are integers and the total is a float",
                "correct": false
              },
              {
                "text": "Adding floats accumulates rounding error",
                "correct": false
              },
              {
                "text": "The list should have been a dictionary",
                "correct": false
              },
              {
                "text": "The reset to zero sits inside the loop, so only the last value survives",
                "correct": true
              }
            ],
            "fbCorrect": "Correct. Each pass discards the total, leaving 141, and 141 divided by 4 is 35.25. The true mean is 129.00 \u00b0C. Move the reset above the loop.",
            "fbWrong": "THE ANSWER: The reset to zero sits inside the loop, so only the last value survives. Each pass discards the total, leaving 141, and 141 divided by 4 is 35.25. The true mean is 129.00 \u00b0C. Move the reset above the loop.\n\nWhy the others are wrong. \u201cThe temperatures are integers and the total is a float\u201d \u2014 Python handles that mixture without trouble and the division is correct. The numerator is the problem.  \u201cAdding floats accumulates rounding error\u201d \u2014 Rounding error at this scale is invisible. A mean of 35 \u00b0C for readings between 118 and 141 is a structural error.  \u201cThe list should have been a dictionary\u201d \u2014 A list is the right structure here."
          },
          {
            "n": 2,
            "kind": "diagnosis",
            "title": "This prints a count that is one too low on this file. Why?",
            "help": "temps = [134, 131, 128, 126]\nALARM = 130\nover = 0\nfor i in range(1, len(temps)):\n    if temps[i] > ALARM:\n        over = over + 1\n\nprint(f\"{over} readings above the alarm limit\")\n1 readings above the alarm limit",
            "choices": [
              {
                "text": "The counter should start at 1",
                "correct": false
              },
              {
                "text": "The range stops one short of the end of the list",
                "correct": false
              },
              {
                "text": "The comparison should be greater-than-or-equal",
                "correct": false
              },
              {
                "text": "The range starts at 1, so the first reading is never tested",
                "correct": true
              }
            ],
            "fbCorrect": "Correct. range(1, 4) skips position 0, which holds 134. Two readings exceed 130. Loop over the values themselves and the off-by-one cannot happen.",
            "fbWrong": "THE ANSWER: The range starts at 1, so the first reading is never tested. Range(1, 4) skips position 0, which holds 134. Two readings exceed 130. Loop over the values themselves and the off-by-one cannot happen.\n\nWhy the others are wrong. \u201cThe counter should start at 1\u201d \u2014 That would give the right total here by accident, while leaving the real fault in place and breaking every other file.  \u201cThe range stops one short of the end of the list\u201d \u2014 It reaches position 3, the last of four. The problem is at the beginning.  \u201cThe comparison should be greater-than-or-equal\u201d \u2014 No reading equals 130 exactly here, so that change would not affect the count."
          },
          {
            "n": 3,
            "kind": "traceback",
            "title": "You are reading a 300-row file and it stops partway through with this. What has happened, and what should the loop do about it?",
            "help": "Traceback (most recent call last):\n  File \"<ipython-input-7-4c5d6e>\", line 4, in <module>\n    if float(row[\"winding_temp_c\"]) > ALARM:\nValueError: could not convert string to float: ''",
            "choices": [
              {
                "text": "The column name is spelled wrongly",
                "correct": false
              },
              {
                "text": "That field is empty in one row, so the loop should skip that row and count how many it skipped",
                "correct": true
              },
              {
                "text": "The whole file is corrupted and cannot be used",
                "correct": false
              },
              {
                "text": "The empty value should be replaced with zero so the loop can continue",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. The two quote marks with nothing between them are an empty string. Skipping is the right response and the count of skips belongs in your report, because it tells the reader how much of the file the answer actually covers.",
            "fbWrong": "THE ANSWER: That field is empty in one row, so the loop should skip that row and count how many it skipped. The two quote marks with nothing between them are an empty string. Skipping is the right response and the count of skips belongs in your report, because it tells the reader how much of the file the answer actually covers.\n\nWhy the others are wrong. \u201cThe column name is spelled wrongly\u201d \u2014 A wrong column name raises a KeyError before any conversion is attempted. The column was found; its content was empty.  \u201cThe whole file is corrupted and cannot be used\u201d \u2014 One blank field in one row says nothing about the other 299. Handle the gap and carry on.  \u201cThe empty value should be replaced with zero so the loop can continue\u201d \u2014 This is the trap. Zero is a real measurement, so substituting it silently drags every average downwards. Week 6 is largely about the damage this does."
          },
          {
            "n": 4,
            "kind": "interpretation",
            "title": "Your script prints this summary. Which statement does it support?",
            "help": "rows in file      300\nrows used         287\nrows skipped       13\nmean temp rise   62.5 K",
            "choices": [
              {
                "text": "Losing 13 rows out of 300 is too small to mention",
                "correct": false
              },
              {
                "text": "The mean describes all 300 rows in the file",
                "correct": false
              },
              {
                "text": "The mean describes the 287 usable rows, and the other 13 need explaining",
                "correct": true
              },
              {
                "text": "The 13 skipped rows were duplicates",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. A mean is only ever a mean of what went into it. If the 13 gaps are scattered at random the figure is probably fine; if they share a cause the figure is biased and the count is your only warning.",
            "fbWrong": "THE ANSWER: The mean describes the 287 usable rows, and the other 13 need explaining. A mean is only ever a mean of what went into it. If the 13 gaps are scattered at random the figure is probably fine; if they share a cause the figure is biased and the count is your only warning.\n\nWhy the others are wrong. \u201cLosing 13 rows out of 300 is too small to mention\u201d \u2014 The size of the loss is not what matters; the reason is. Thirteen gaps from one source can move a mean further than fifty scattered at random.  \u201cThe mean describes all 300 rows in the file\u201d \u2014 Thirteen rows contributed nothing to it. Reporting it as a figure for the file overstates what you measured.  \u201cThe 13 skipped rows were duplicates\u201d \u2014 The summary says they were skipped and does not say why. Duplicates are a separate problem, and one you meet in Week 6."
          },
          {
            "n": 5,
            "kind": "judgement",
            "title": "You look at the 13 skipped rows and every one of them comes from the same test day. What should you do before reporting the mean?",
            "help": "",
            "choices": [
              {
                "text": "Fill the gaps with that source's own average so no rows are lost",
                "correct": false
              },
              {
                "text": "Report the mean and mention the 13 skips in a footnote",
                "correct": false
              },
              {
                "text": "Investigate the shared cause first, because gaps that cluster in one source point at how the data was collected",
                "correct": true
              },
              {
                "text": "Drop that source entirely and report the rest",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. Thirteen blanks spread across the file is untidiness. Thirteen blanks from one source is a finding, and it may matter more than the mean you were asked for.",
            "fbWrong": "THE ANSWER: Investigate the shared cause first, because gaps that cluster in one source point at how the data was collected. Thirteen blanks spread across the file is untidiness. Thirteen blanks from one source is a finding, and it may matter more than the mean you were asked for.\n\nWhy the others are wrong. \u201cFill the gaps with that source's own average so no rows are lost\u201d \u2014 That invents readings from the one source you have reason to distrust, and it hides the pattern you just found.  \u201cReport the mean and mention the 13 skips in a footnote\u201d \u2014 Reporting the count is necessary and it is not sufficient here. A footnote presents a systematic gap as though it were random noise.  \u201cDrop that source entirely and report the rest\u201d \u2014 That might end up being right, and it is a decision to take after you understand the cause. Removing a source before knowing why it failed can delete the very thing under investigation."
          }
        ]
      },
      {
        "week": 5,
        "number": 5,
        "title": "CML3111 \u00b7 Weekly Quiz 5 \u2014 pandas, and judging a dataset",
        "intro": "Read what each question shows you. None of them can be answered without it.\n\nHOW THIS WORKS\n\u2022 Answer it now, in the 5 minutes on the screen. That is when this is meant to be taken, while the session is still fresh.\n\u2022 The form then stays open for 24 hours and closes itself. That window is there so a dead network or a broken phone does not cost you a mark you had earned. Take it in the room if you can: by Thursday you will have forgotten the session, and the feedback will be worth less to you.\n\u2022 ONE attempt, from your signed-in Google account. You cannot reopen it or change an answer, so read each question once, properly.\n\u2022 The first box asks for your registration number. It is the number printed on your student card, and it is how the mark reaches your record.\n\u2022 Five questions, one mark each, worth 1% of your final mark.\n\u2022 Your best ten of twelve quizzes count. Missing two costs you nothing, and there are no resits.\n\u2022 When you submit, tap View score. You get a tick or a cross on each question with the feedback underneath. Your mark is the number of ticks, and the feedback on anything you got wrong is the part worth reading.\n\u2022 A question left blank scores the same as one answered wrongly, so answer all five.",
        "questions": [
          {
            "n": 1,
            "kind": "diagnosis",
            "title": "You wanted the number of records above the threshold. This prints the whole row count instead. Why?",
            "help": "mask = df[\"output\"] > 450\nprint(len(mask))\n9568\nprint(mask.sum())\n3702",
            "choices": [
              {
                "text": "len() does not work on pandas objects",
                "correct": false
              },
              {
                "text": "The mask holds one True or False per row, so its length is the row count",
                "correct": true
              },
              {
                "text": "The threshold is too low, so every row qualifies",
                "correct": false
              },
              {
                "text": "The comparison was written the wrong way round",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. A comparison on a column answers the question for every row and hands back all the answers, so it is always as long as the frame. mask.sum() counts the True entries, as the second line shows, and len(df[mask]) counts the rows you keep.",
            "fbWrong": "THE ANSWER: The mask holds one True or False per row, so its length is the row count. A comparison on a column answers the question for every row and hands back all the answers, so it is always as long as the frame. mask.sum() counts the True entries, as the second line shows, and len(df[mask]) counts the rows you keep.\n\nWhy the others are wrong. \u201clen() does not work on pandas objects\u201d \u2014 It works and it reported the truth. The truth it reported answers a different question from the one you asked.  \u201cThe threshold is too low, so every row qualifies\u201d \u2014 The second line rules this out: the sum is well below the row count, so most rows do not qualify. Notice also that the length would have been the row count either way, which is what makes it the wrong thing to measure.  \u201cThe comparison was written the wrong way round\u201d \u2014 Reversing it would produce a different set of True entries and the same length. Length is the wrong measurement to be taking."
          },
          {
            "n": 2,
            "kind": "diagnosis",
            "title": "The maximum below is far too small and no error was raised. What has happened?",
            "help": "print(df[\"output\"].dtype)\nobject\n\nprint(df[\"output\"].max())\n9.9\n\n# the file contains values such as 32.5, 41.2, 9.9, 28.0",
            "choices": [
              {
                "text": "max() needs the column sorted first",
                "correct": false
              },
              {
                "text": "The largest values are stored in a different column",
                "correct": false
              },
              {
                "text": "The column holds text, so the maximum was decided alphabetically and a value starting with 9 wins",
                "correct": true
              },
              {
                "text": "The column contains missing values that max() skipped",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. object dtype means the column is text. Compared as text, \"9.9\" beats \"41.2\" because the character 9 comes after 4. Convert with pd.to_numeric and the real maximum appears. One stray value with a unit or a stray space is usually what forced the whole column to text.",
            "fbWrong": "THE ANSWER: The column holds text, so the maximum was decided alphabetically and a value starting with 9 wins. Object dtype means the column is text. Compared as text, \"9.9\" beats \"41.2\" because the character 9 comes after 4. Convert with pd.to_numeric and the real maximum appears. One stray value with a unit or a stray space is usually what forced the whole column to text.\n\nWhy the others are wrong. \u201cmax() needs the column sorted first\u201d \u2014 max() never needs sorting. It compared correctly by the rules for text, which are the wrong rules for measurements.  \u201cThe largest values are stored in a different column\u201d \u2014 The comment shows the values are in this column. The problem is how they are being compared.  \u201cThe column contains missing values that max() skipped\u201d \u2014 max() does skip missing values, and skipping them cannot produce a maximum below most of the data. The ordering itself is what has gone wrong."
          },
          {
            "n": 3,
            "kind": "traceback",
            "title": "What is the first thing to check?",
            "help": "Traceback (most recent call last):\n  File \"<ipython-input-4-7a8b9c>\", line 1, in <module>\n    df[\"power_output\"].mean()\nKeyError: 'power_output'",
            "choices": [
              {
                "text": "Whether the column contains missing values",
                "correct": false
              },
              {
                "text": "Print df.columns and compare the exact spelling, case and any stray spaces",
                "correct": true
              },
              {
                "text": "Whether mean() works on that data type",
                "correct": false
              },
              {
                "text": "Whether the file loaded at all",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. A KeyError on a frame means no column carries that exact label. Trailing spaces from a spreadsheet export are a common cause and they are invisible until you print the list.",
            "fbWrong": "THE ANSWER: Print df.columns and compare the exact spelling, case and any stray spaces. A KeyError on a frame means no column carries that exact label. Trailing spaces from a spreadsheet export are a common cause and they are invisible until you print the list.\n\nWhy the others are wrong. \u201cWhether the column contains missing values\u201d \u2014 Missing values inside a column never stop you selecting it. This error happened before any value was read.  \u201cWhether mean() works on that data type\u201d \u2014 The error came from the selection, before mean() was reached. A type problem would name the type.  \u201cWhether the file loaded at all\u201d \u2014 That is worth confirming, and a frame that failed to load would raise on the read or on len(df) first. The message names one specific label."
          },
          {
            "n": 4,
            "kind": "interpretation",
            "title": "What does this shape tell you?",
            "help": "g = df.groupby(\"temp_band\")[\"output\"].mean()\nprint(g.shape)\n(4,)",
            "choices": [
              {
                "text": "The result has four columns",
                "correct": false
              },
              {
                "text": "Four rows of the original data survived the operation",
                "correct": false
              },
              {
                "text": "There are four groups, and the result holds one mean for each of them",
                "correct": true
              },
              {
                "text": "Four rows had a missing value in the grouping column",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. Grouping collapses the frame to one row per group, so the length of the result is the number of distinct values in the grouping column. The original frame is untouched.",
            "fbWrong": "THE ANSWER: There are four groups, and the result holds one mean for each of them. Grouping collapses the frame to one row per group, so the length of the result is the number of distinct values in the grouping column. The original frame is untouched.\n\nWhy the others are wrong. \u201cThe result has four columns\u201d \u2014 A shape written with one number describes one dimension. Four columns would appear as a second number.  \u201cFour rows of the original data survived the operation\u201d \u2014 Grouping summarises rows rather than removing them. Every row contributed to one of the four means.  \u201cFour rows had a missing value in the grouping column\u201d \u2014 Rows with a missing group label are left out of the result rather than counted into it, and that would not set the length to four."
          },
          {
            "n": 5,
            "kind": "judgement",
            "title": "A colleague sends you power_plant.csv as an email attachment with no other information, and you are asked to quote the mean power output in a report. What do you do first?",
            "help": "",
            "choices": [
              {
                "text": "Compare it against a published dataset and use whichever looks cleaner",
                "correct": false
              },
              {
                "text": "Ask for the file in a different format to be safe",
                "correct": false
              },
              {
                "text": "Compute the mean and quote it, since the file is the data you were given",
                "correct": false
              },
              {
                "text": "Establish where the file came from, what licence it carries and how many rows it holds, and record all three alongside the figure",
                "correct": true
              }
            ],
            "fbCorrect": "Correct. A number in a report is only as defensible as the file behind it. Source, licence, date and row count are the minimum you need to be able to answer the question every reader eventually asks, which is where this came from.",
            "fbWrong": "THE ANSWER: Establish where the file came from, what licence it carries and how many rows it holds, and record all three alongside the figure. A number in a report is only as defensible as the file behind it. Source, licence, date and row count are the minimum you need to be able to answer the question every reader eventually asks, which is where this came from.\n\nWhy the others are wrong. \u201cCompare it against a published dataset and use whichever looks cleaner\u201d \u2014 Choosing data by how tidy it looks selects for convenience over relevance. Find out what this file is before reaching for another one.  \u201cAsk for the file in a different format to be safe\u201d \u2014 The format is not the risk. An unsourced spreadsheet is exactly as unsourced after conversion.  \u201cCompute the mean and quote it, since the file is the data you were given\u201d \u2014 The arithmetic is the easy part and the least of your obligations. A figure whose origin you cannot state is one you cannot defend when it is challenged."
          }
        ]
      },
      {
        "week": 6,
        "number": 6,
        "title": "CML3111 \u00b7 Weekly Quiz 6 \u2014 Dirty data, and seeing it",
        "intro": "Read what each question shows you. None of them can be answered without it.\n\nHOW THIS WORKS\n\u2022 Answer it now, in the 5 minutes on the screen. That is when this is meant to be taken, while the session is still fresh.\n\u2022 The form then stays open for 24 hours and closes itself. That window is there so a dead network or a broken phone does not cost you a mark you had earned. Take it in the room if you can: by Thursday you will have forgotten the session, and the feedback will be worth less to you.\n\u2022 ONE attempt, from your signed-in Google account. You cannot reopen it or change an answer, so read each question once, properly.\n\u2022 The first box asks for your registration number. It is the number printed on your student card, and it is how the mark reaches your record.\n\u2022 Five questions, one mark each, worth 1% of your final mark.\n\u2022 Your best ten of twelve quizzes count. Missing two costs you nothing, and there are no resits.\n\u2022 When you submit, tap View score. You get a tick or a cross on each question with the feedback underneath. Your mark is the number of ticks, and the feedback on anything you got wrong is the part worth reading.\n\u2022 A question left blank scores the same as one answered wrongly, so answer all five.",
        "questions": [
          {
            "n": 1,
            "kind": "diagnosis",
            "title": "The mean below is lower than every real reading in the list. What went wrong?",
            "help": "# the logger writes 0.0 when the accelerometer drops out\nvibration = [2.41, 0.0, 2.38, 2.44]\nprint(f\"mean {sum(vibration) / len(vibration):.4f} mm/s\")\nmean 1.8075 mm/s",
            "choices": [
              {
                "text": "The division should exclude the last value",
                "correct": false
              },
              {
                "text": "One entry is a sensor dropout recorded as zero",
                "correct": true
              },
              {
                "text": "Zero vibration is possible when the machine is stopped",
                "correct": false
              },
              {
                "text": "The list is too short for a mean to be meaningful",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. A dropout written as 0.0 is indistinguishable from a real reading by arithmetic alone. The mean of the three real readings is 2.4100 mm/s. Convert dropouts to missing values before averaging.",
            "fbWrong": "THE ANSWER: One entry is a sensor dropout recorded as zero. A dropout written as 0.0 is indistinguishable from a real reading by arithmetic alone. The mean of the three real readings is 2.4100 mm/s. Convert dropouts to missing values before averaging.\n\nWhy the others are wrong. \u201cThe division should exclude the last value\u201d \u2014 Which position is dropped is beside the point. A placeholder is being counted as a measurement.  \u201cZero vibration is possible when the machine is stopped\u201d \u2014 The comment settles it: this logger writes 0.0 for a dropout, so this reading records a lost signal rather than a still machine. Without that comment the option would be arguable, and a genuine zero from a stopped machine still has no place in an average of running vibration.  \u201cThe list is too short for a mean to be meaningful\u201d \u2014 Three real readings give a usable mean. The fourth entry is not a reading."
          },
          {
            "n": 2,
            "kind": "diagnosis",
            "title": "This runs with no error and no warning. What has it done to your data?",
            "help": "# one current was typed as \"12.5 A\" instead of 12.5\ndf[\"current_a\"] = pd.to_numeric(df[\"current_a\"],\n                                  errors=\"coerce\")\nprint(df[\"current_a\"].mean())",
            "choices": [
              {
                "text": "It raised the error but carried on to the next row",
                "correct": false
              },
              {
                "text": "It turned every unreadable value into a missing value, and the mean then quietly skipped those rows",
                "correct": true
              },
              {
                "text": "It stripped the unit and kept the number",
                "correct": false
              },
              {
                "text": "It replaced the unreadable value with the column mean",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. Coercing is often the right move and it is never free: it converts a loud failure into a silent one. Count the missing values it created and report that count, otherwise your mean covers fewer rows than you believe.",
            "fbWrong": "THE ANSWER: It turned every unreadable value into a missing value, and the mean then quietly skipped those rows. Coercing is often the right move and it is never free: it converts a loud failure into a silent one. Count the missing values it created and report that count, otherwise your mean covers fewer rows than you believe.\n\nWhy the others are wrong. \u201cIt raised the error but carried on to the next row\u201d \u2014 That is what errors=\"raise\" would do, minus the carrying on. Coercing suppresses the error entirely.  \u201cIt stripped the unit and kept the number\u201d \u2014 Nothing here parses units. A value with a unit attached is unreadable as a number and becomes missing.  \u201cIt replaced the unreadable value with the column mean\u201d \u2014 No substitution happens. Filling gaps is a separate decision you have to make deliberately, and doing it before a split leaks information, as Week 10 shows."
          },
          {
            "n": 3,
            "kind": "traceback",
            "title": "You convert the column without coercing and get this. What is the useful thing about this message?",
            "help": "Traceback (most recent call last):\n  File \"<ipython-input-6-2b3c4d>\", line 1, in <module>\n    df[\"current_a\"] = pd.to_numeric(df[\"current_a\"])\nValueError: Unable to parse string \"12.5 A\" at position 417",
            "choices": [
              {
                "text": "It should be suppressed so the analysis can continue",
                "correct": false
              },
              {
                "text": "It means the column is the wrong data type for pandas",
                "correct": false
              },
              {
                "text": "It proves the column cannot be converted",
                "correct": false
              },
              {
                "text": "It names the offending value and the row it sits in, so you can look at it and decide what it should be",
                "correct": true
              }
            ],
            "fbCorrect": "Correct. This is more useful than a silent conversion, because it hands you the exact value and position. Look at row 417, decide whether to repair the entry or drop it, and write down which you chose.",
            "fbWrong": "THE ANSWER: It names the offending value and the row it sits in, so you can look at it and decide what it should be. This is more useful than a silent conversion, because it hands you the exact value and position. Look at row 417, decide whether to repair the entry or drop it, and write down which you chose.\n\nWhy the others are wrong. \u201cIt should be suppressed so the analysis can continue\u201d \u2014 Suppressing it is available and it costs you the position and the value. Read the message first, then decide.  \u201cIt means the column is the wrong data type for pandas\u201d \u2014 The column is text because of this value. Conversion is the cure and the message is telling you what stands in the way.  \u201cIt proves the column cannot be converted\u201d \u2014 It proves one value cannot. Fix or remove that value and the column converts."
          },
          {
            "n": 4,
            "kind": "interpretation",
            "title": "Read the question you set yourself against the chart you produced. Does the chart answer it?",
            "help": "question:  Does power output differ between the\n           coldest and the hottest hours?\n\nchart:     one histogram\n           x = net power output (MW)\n           y = number of hours\n           all 9,568 hours, no grouping applied",
            "choices": [
              {
                "text": "No, because a histogram is never the right chart",
                "correct": false
              },
              {
                "text": "Yes, because the shape of the distribution reveals the two groups",
                "correct": false
              },
              {
                "text": "Yes, provided the sample is large enough",
                "correct": false
              },
              {
                "text": "No, because the two groups are mixed together in one distribution and cannot be compared",
                "correct": true
              }
            ],
            "fbCorrect": "Correct. The question asks for a comparison, so the chart has to separate the groups: two distributions side by side, or a mean for each with its spread. A single pooled histogram cannot show a difference between halves it never divided.",
            "fbWrong": "THE ANSWER: No, because the two groups are mixed together in one distribution and cannot be compared. The question asks for a comparison, so the chart has to separate the groups: two distributions side by side, or a mean for each with its spread. A single pooled histogram cannot show a difference between halves it never divided.\n\nWhy the others are wrong. \u201cNo, because a histogram is never the right chart\u201d \u2014 A histogram is a good way to show one distribution. The fault is the missing split rather than the choice of chart type.  \u201cYes, because the shape of the distribution reveals the two groups\u201d \u2014 Two clear humps would hint at something and would not tell you which group each hump belongs to. A distribution with one hump can still hide a real difference between the groups.  \u201cYes, provided the sample is large enough\u201d \u2014 Sample size cannot rescue a chart that never made the comparison. Twenty thousand pooled records answer the question no better than two hundred."
          },
          {
            "n": 5,
            "kind": "judgement",
            "title": "You find a current reading six times the running current, lasting a fraction of a second at the moment a motor starts. What do you do with it?",
            "help": "",
            "choices": [
              {
                "text": "Keep it and label it as a start-up sample",
                "correct": true
              },
              {
                "text": "Replace it with the mean of the column",
                "correct": false
              },
              {
                "text": "Cap it at the highest running value so it stops distorting the mean",
                "correct": false
              },
              {
                "text": "Delete it, because it is far outside the normal range",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. Starting current runs six to eight times the running value and it is expected behaviour. Keep it, mark it as a start-up sample, and decide separately whether start-up hours belong in the analysis you are doing.",
            "fbWrong": "THE ANSWER: Keep it and label it as a start-up sample. Starting current runs six to eight times the running value and it is expected behaviour. Keep it, mark it as a start-up sample, and decide separately whether start-up hours belong in the analysis you are doing.\n\nWhy the others are wrong. \u201cReplace it with the mean of the column\u201d \u2014 That substitutes an invented value for a correct measurement of a real phenomenon.  \u201cCap it at the highest running value so it stops distorting the mean\u201d \u2014 Capping invents a reading and removes the signature of an ordinary event.  \u201cDelete it, because it is far outside the normal range\u201d \u2014 Deleting inrush hides a normal operating state. A model that has never seen a start-up will treat every start-up as a fault."
          }
        ]
      },
      {
        "week": 8,
        "number": 7,
        "title": "CML3111 \u00b7 Weekly Quiz 7 \u2014 Learning from data: the first model",
        "intro": "Read what each question shows you. None of them can be answered without it.\n\nHOW THIS WORKS\n\u2022 Answer it now, in the 5 minutes on the screen. That is when this is meant to be taken, while the session is still fresh.\n\u2022 The form then stays open for 24 hours and closes itself. That window is there so a dead network or a broken phone does not cost you a mark you had earned. Take it in the room if you can: by Thursday you will have forgotten the session, and the feedback will be worth less to you.\n\u2022 ONE attempt, from your signed-in Google account. You cannot reopen it or change an answer, so read each question once, properly.\n\u2022 The first box asks for your registration number. It is the number printed on your student card, and it is how the mark reaches your record.\n\u2022 Five questions, one mark each, worth 1% of your final mark.\n\u2022 Your best ten of twelve quizzes count. Missing two costs you nothing, and there are no resits.\n\u2022 When you submit, tap View score. You get a tick or a cross on each question with the feedback underneath. Your mark is the number of ticks, and the feedback on anything you got wrong is the part worth reading.\n\u2022 A question left blank scores the same as one answered wrongly, so answer all five.",
        "questions": [
          {
            "n": 1,
            "kind": "diagnosis",
            "title": "A teammate reports this as the accuracy of the model. What does the number actually describe?",
            "help": "model.fit(X, y)\nprint(model.score(X, y))\n0.91",
            "choices": [
              {
                "text": "How well the model will do on new data, give or take a little",
                "correct": false
              },
              {
                "text": "How well the model reproduces the rows it was fitted on, which tells you nothing about a new case",
                "correct": true
              },
              {
                "text": "Nothing useful, because score() is the wrong function",
                "correct": false
              },
              {
                "text": "The proportion of the data used for training",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. The same rows appear in fit and in score, so the model is being marked on the answers it was shown. Hold rows back with train_test_split and score on those.",
            "fbWrong": "THE ANSWER: How well the model reproduces the rows it was fitted on, which tells you nothing about a new case. The same rows appear in fit and in score, so the model is being marked on the answers it was shown. Hold rows back with train_test_split and score on those.\n\nWhy the others are wrong. \u201cHow well the model will do on new data, give or take a little\u201d \u2014 There is no basis for that reading. A model with enough freedom can score near one on its training rows and fail completely on anything new, which is the whole subject of Week 10.  \u201cNothing useful, because score() is the wrong function\u201d \u2014 score() is the right function used on the wrong rows. Give it held-out data and the number becomes meaningful.  \u201cThe proportion of the data used for training\u201d \u2014 score() returns a measure of fit. The train and test proportions are whatever you chose when you split, and here nothing was split."
          },
          {
            "n": 2,
            "kind": "diagnosis",
            "title": "This predicts a plausible-looking value and raises no error, and the value is wrong. Why?",
            "help": "feats = [\"AT\", \"V\", \"AP\", \"RH\"]\nmodel.fit(df[feats], df[\"output\"])\n\n# a new hour: 14.6 C, 41.7 cm Hg, 1019 mbar, 76 % humidity\nprint(model.predict([[41.7, 14.6, 1019, 76]]))",
            "choices": [
              {
                "text": "The new values should have been scaled first",
                "correct": false
              },
              {
                "text": "The model was fitted on too few features to predict anything",
                "correct": false
              },
              {
                "text": "The values were supplied in a different order from the fitted columns",
                "correct": true
              },
              {
                "text": "predict() needs a two-dimensional input",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. A fitted model knows only that its first input is whatever its first training column was. Swap two and it happily applies the wrong coefficient to each. Build the row as a frame with named columns and this class of error disappears.",
            "fbWrong": "THE ANSWER: The values were supplied in a different order from the fitted columns. A fitted model knows only that its first input is whatever its first training column was. Swap two and it happily applies the wrong coefficient to each. Build the row as a frame with named columns and this class of error disappears.\n\nWhy the others are wrong. \u201cThe new values should have been scaled first\u201d \u2014 Scaling would matter for some model types and it would not repair a swap. Scaled or raw, the values are in the wrong positions.  \u201cThe model was fitted on too few features to predict anything\u201d \u2014 Three or four features is enough to produce a prediction. The count is fine and the order is not.  \u201cpredict() needs a two-dimensional input\u201d \u2014 It does, and it was given one. The doubled brackets are correct here."
          },
          {
            "n": 3,
            "kind": "traceback",
            "title": "What is the most likely cause?",
            "help": "Traceback (most recent call last):\n  File \"<ipython-input-9-5e6f7a>\", line 1, in <module>\n    model.fit(X, y)\nValueError: Found input variables with inconsistent numbers\nof samples: [7654, 9568]",
            "choices": [
              {
                "text": "The features and the target need to be the same data type",
                "correct": false
              },
              {
                "text": "The target column contains missing values",
                "correct": false
              },
              {
                "text": "There are too few rows to fit a model",
                "correct": false
              },
              {
                "text": "The features were filtered or had rows dropped and the target was not, so the two no longer line up",
                "correct": true
              }
            ],
            "fbCorrect": "Correct. Dropping missing values from the feature frame without applying the same selection to the target is the usual cause. Filter the frame first and take X and y from the filtered frame so they can never drift apart.",
            "fbWrong": "THE ANSWER: The features were filtered or had rows dropped and the target was not, so the two no longer line up. Dropping missing values from the feature frame without applying the same selection to the target is the usual cause. Filter the frame first and take X and y from the filtered frame so they can never drift apart.\n\nWhy the others are wrong. \u201cThe features and the target need to be the same data type\u201d \u2014 They routinely differ, and that is fine. The error counts rows and says nothing about types.  \u201cThe target column contains missing values\u201d \u2014 Missing values in the target give a different complaint about NaN. This message is purely about the row counts disagreeing.  \u201cThere are too few rows to fit a model\u201d \u2014 Both counts here are ample. The problem is that they are not equal."
          },
          {
            "n": 4,
            "kind": "interpretation",
            "title": "A teammate shows you this plot and this conclusion. How should you read it?",
            "help": "plot:        y = residual (actual - predicted), MW\n             x = ACTUAL power output, MW\n             a clear upward slope, left to right\n\nconclusion:  \"the model under-predicts high-output\n             hours\"",
            "choices": [
              {
                "text": "The residuals should have been squared before plotting",
                "correct": false
              },
              {
                "text": "The conclusion is right, and the model needs an extra feature to fix it",
                "correct": false
              },
              {
                "text": "A slope in the residuals always means the model is broken",
                "correct": false
              },
              {
                "text": "The slope appears by construction; plot residuals against the predicted value",
                "correct": true
              }
            ],
            "fbCorrect": "Correct, and this catches almost everybody once. The actual value equals the prediction plus the residual, so the residual is built into the quantity on the horizontal axis and rises with it. Against the predicted value the slope disappears and any real pattern becomes visible.",
            "fbWrong": "THE ANSWER: The slope appears by construction; plot residuals against the predicted value. This catches almost everybody once. The actual value equals the prediction plus the residual, so the residual is built into the quantity on the horizontal axis and rises with it. Against the predicted value the slope disappears and any real pattern becomes visible.\n\nWhy the others are wrong. \u201cThe residuals should have been squared before plotting\u201d \u2014 Squaring throws away the sign, which is the most useful part of a residual. The pairing of axes is what is wrong here.  \u201cThe conclusion is right, and the model needs an extra feature to fix it\u201d \u2014 The conclusion may happen to be true and this plot cannot establish it. Redraw against the predicted value before changing the model.  \u201cA slope in the residuals always means the model is broken\u201d \u2014 A slope against the predicted value would be worth investigating. A slope against the actual value is arithmetic rather than a finding."
          },
          {
            "n": 5,
            "kind": "judgement",
            "title": "Your model reaches a root-mean-square error of 4.1 MW. The client asks whether that is good. What do you need before you can answer?",
            "help": "",
            "choices": [
              {
                "text": "A larger dataset",
                "correct": false
              },
              {
                "text": "A second model to compare it against",
                "correct": false
              },
              {
                "text": "The error of predicting the mean, and the published figures",
                "correct": true
              },
              {
                "text": "Nothing further; 4.1 MW is a small number",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. Published work on this dataset reaches roughly 3 to 4 MW, so 4.1 MW puts you at the edge of the literature rather than adrift. Predicting the mean gives you the floor. Together they let you say what the number means.",
            "fbWrong": "THE ANSWER: The error of predicting the mean, and the published figures. Published work on this dataset reaches roughly 3 to 4 MW, so 4.1 MW puts you at the edge of the literature rather than adrift. Predicting the mean gives you the floor. Together they let you say what the number means.\n\nWhy the others are wrong. \u201cA larger dataset\u201d \u2014 The dataset is already nearly ten thousand hours. Size is not what is missing.  \u201cA second model to compare it against\u201d \u2014 That tells you which of two is better and not whether either is worth deploying.  \u201cNothing further; 4.1 MW is a small number\u201d \u2014 On a plant output of several hundred megawatts it sounds small, and the judgement still needs a stated reference."
          }
        ]
      },
      {
        "week": 9,
        "number": 8,
        "title": "CML3111 \u00b7 Weekly Quiz 8 \u2014 Classification",
        "intro": "Read what each question shows you. None of them can be answered without it.\n\nHOW THIS WORKS\n\u2022 Answer it now, in the 5 minutes on the screen. That is when this is meant to be taken, while the session is still fresh.\n\u2022 The form then stays open for 24 hours and closes itself. That window is there so a dead network or a broken phone does not cost you a mark you had earned. Take it in the room if you can: by Thursday you will have forgotten the session, and the feedback will be worth less to you.\n\u2022 ONE attempt, from your signed-in Google account. You cannot reopen it or change an answer, so read each question once, properly.\n\u2022 The first box asks for your registration number. It is the number printed on your student card, and it is how the mark reaches your record.\n\u2022 Five questions, one mark each, worth 1% of your final mark.\n\u2022 Your best ten of twelve quizzes count. Missing two costs you nothing, and there are no resits.\n\u2022 When you submit, tap View score. You get a tick or a cross on each question with the feedback underneath. Your mark is the number of ticks, and the feedback on anything you got wrong is the part worth reading.\n\u2022 A question left blank scores the same as one answered wrongly, so answer all five.",
        "questions": [
          {
            "n": 1,
            "kind": "diagnosis",
            "title": "A teammate is pleased with this result. What has the model actually learned?",
            "help": "accuracy                     0.966\nhours predicted to fail          0\n\n# in this log 3.4 in 100 machine-hours end in a failure",
            "choices": [
              {
                "text": "That more features are needed to raise accuracy",
                "correct": false
              },
              {
                "text": "That the two classes are equally easy to separate",
                "correct": false
              },
              {
                "text": "A genuinely strong rule, since 96.6 per cent is a high score",
                "correct": false
              },
              {
                "text": "To answer with the majority class every time, which scores the majority-class share and finds nothing",
                "correct": true
              }
            ],
            "fbCorrect": "Correct. Since 96.6 in 100 cases are negative, always saying negative scores 0.966. The model has found the base rate and no signal. Recall on the class you care about is zero, and that is the number to report.",
            "fbWrong": "THE ANSWER: To answer with the majority class every time, which scores the majority-class share and finds nothing. Since 96.6 in 100 cases are negative, always saying negative scores 0.966. The model has found the base rate and no signal. Recall on the class you care about is zero, and that is the number to report.\n\nWhy the others are wrong. \u201cThat more features are needed to raise accuracy\u201d \u2014 Accuracy is already near its ceiling and is the wrong instrument. Change the metric before changing the model.  \u201cThat the two classes are equally easy to separate\u201d \u2014 It never attempted the separation. It predicted one class throughout.  \u201cA genuinely strong rule, since 96.6 per cent is a high score\u201d \u2014 The score is exactly what you get for free by ignoring the data. A rule that never fires cannot be strong at the job it was built for."
          },
          {
            "n": 2,
            "kind": "diagnosis",
            "title": "This model was tested against a maintenance log of ten thousand machine-hours. Read the confusion matrix. Which statement does it support?",
            "help": "                      pred: runs     pred: fails\nactual: runs                 9620             36\nactual: fails                 310             34\n\n10,000 machine-hours in total; accuracy 0.965",
            "choices": [
              {
                "text": "Its main weakness is false alarms",
                "correct": false
              },
              {
                "text": "It is well balanced between the two kinds of error",
                "correct": false
              },
              {
                "text": "Accuracy of 0.965 shows it is fit for use",
                "correct": false
              },
              {
                "text": "It misses about nine in ten of the cases it exists to catch",
                "correct": true
              }
            ],
            "fbCorrect": "Correct. Recall on the class of interest is 34 out of 344, which is 0.099. The high accuracy comes almost entirely from the 9,620 easy negatives. This is the number the matrix exists to expose.",
            "fbWrong": "THE ANSWER: It misses about nine in ten of the cases it exists to catch. Recall on the class of interest is 34 out of 344, which is 0.099. The high accuracy comes almost entirely from the 9,620 easy negatives. This is the number the matrix exists to expose.\n\nWhy the others are wrong. \u201cIts main weakness is false alarms\u201d \u2014 There are only 36 false alarms against 310 misses. The costly error here is the one being made nearly ten times as often.  \u201cIt is well balanced between the two kinds of error\u201d \u2014 310 against 36 is close to a nine-to-one imbalance in the errors.  \u201cAccuracy of 0.965 shows it is fit for use\u201d \u2014 Predicting the majority class throughout would score 0.966, which is higher. Accuracy cannot see this failure."
          },
          {
            "n": 3,
            "kind": "traceback",
            "title": "What does this tell you to change?",
            "help": "Traceback (most recent call last):\n  File \"<ipython-input-11-8b9c0d>\", line 1, in <module>\n    print(recall_score(y_test, pred))\nValueError: Target is multiclass but average='binary'.\nPlease choose another average setting, one of [None, 'micro', 'macro', 'weighted'].",
            "choices": [
              {
                "text": "The predictions are the wrong data type",
                "correct": false
              },
              {
                "text": "The target has more than two classes, so you must say how recall should be combined across them",
                "correct": true
              },
              {
                "text": "Recall cannot be computed for more than two classes",
                "correct": false
              },
              {
                "text": "The test set is too small for recall to be defined",
                "correct": false
              }
            ],
            "fbCorrect": "Correct, and the choice matters. average=None gives you recall per class, which is usually what you want, because a single combined figure can hide a class the model never predicts.",
            "fbWrong": "THE ANSWER: The target has more than two classes, so you must say how recall should be combined across them. The choice matters. average=None gives you recall per class, which is usually what you want, because a single combined figure can hide a class the model never predicts.\n\nWhy the others are wrong. \u201cThe predictions are the wrong data type\u201d \u2014 The types are acceptable. The message is about the number of classes in the target.  \u201cRecall cannot be computed for more than two classes\u201d \u2014 It can, once you state how to aggregate it. The error offers you the options.  \u201cThe test set is too small for recall to be defined\u201d \u2014 Size is not mentioned and is not the issue. The class count is."
          },
          {
            "n": 4,
            "kind": "interpretation",
            "title": "You lower the decision threshold from 0.5 to 0.2 and re-score the same model on the same test set. What has changed?",
            "help": "threshold 0.5   recall 0.099   false alarms  36\nthreshold 0.2   recall 0.439   false alarms 290",
            "choices": [
              {
                "text": "The result is invalid because the threshold should stay at 0.5",
                "correct": false
              },
              {
                "text": "The model now overfits, because recall rose sharply",
                "correct": false
              },
              {
                "text": "Nothing about the model; you moved along its trade-off, buying recall by accepting eight times as many false alarms",
                "correct": true
              },
              {
                "text": "The model has been improved by better tuning",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. The model and its scores are untouched: only the cut-off you apply to them changed. Which threshold is right depends on what a false alarm costs against a miss, and that is a question about the work rather than the model.",
            "fbWrong": "THE ANSWER: Nothing about the model; you moved along its trade-off, buying recall by accepting eight times as many false alarms. The model and its scores are untouched: only the cut-off you apply to them changed. Which threshold is right depends on what a false alarm costs against a miss, and that is a question about the work rather than the model.\n\nWhy the others are wrong. \u201cThe result is invalid because the threshold should stay at 0.5\u201d \u2014 0.5 is a default rather than a rule. On a problem where a miss costs far more than a false alarm, moving it is exactly the right thing to do.  \u201cThe model now overfits, because recall rose sharply\u201d \u2014 Overfitting is about the gap between training and unseen data. This is one model on one test set at two thresholds.  \u201cThe model has been improved by better tuning\u201d \u2014 No retraining took place. The same probabilities are being cut in a different place."
          },
          {
            "n": 5,
            "kind": "judgement",
            "title": "A false alarm costs a four-hour stop. A missed failure costs a gearbox and a week of production. Which metric should govern your model, and why?",
            "help": "",
            "choices": [
              {
                "text": "Whichever metric gives the highest number, so the result reads well",
                "correct": false
              },
              {
                "text": "Recall on the class you cannot afford to miss, with the false-alarm rate beside it",
                "correct": true
              },
              {
                "text": "Accuracy, because it summarises overall performance",
                "correct": false
              },
              {
                "text": "Precision, because false alarms annoy the operators",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. The expensive error is the miss, so recall is the quantity to drive up. Quoting the false-alarm rate beside it keeps you honest, because recall can always be bought and somebody has to pay for it.",
            "fbWrong": "THE ANSWER: Recall on the class you cannot afford to miss, with the false-alarm rate beside it. The expensive error is the miss, so recall is the quantity to drive up. Quoting the false-alarm rate beside it keeps you honest, because recall can always be bought and somebody has to pay for it.\n\nWhy the others are wrong. \u201cWhichever metric gives the highest number, so the result reads well\u201d \u2014 Choosing a metric to flatter the model is how a system that misses nine failures in ten gets signed off.  \u201cAccuracy, because it summarises overall performance\u201d \u2014 At a base rate near 3 per cent, accuracy is dominated by easy negatives and a useless model scores 0.966. It cannot see the error that matters here.  \u201cPrecision, because false alarms annoy the operators\u201d \u2014 Precision alone rewards a model that fires only when certain, which is a model that misses most of the cases. It belongs in the report next to recall rather than in charge of it."
          }
        ]
      },
      {
        "week": 10,
        "number": 9,
        "title": "CML3111 \u00b7 Weekly Quiz 9 \u2014 Can I trust this model?",
        "intro": "Read what each question shows you. None of them can be answered without it.\n\nHOW THIS WORKS\n\u2022 Answer it now, in the 5 minutes on the screen. That is when this is meant to be taken, while the session is still fresh.\n\u2022 The form then stays open for 24 hours and closes itself. That window is there so a dead network or a broken phone does not cost you a mark you had earned. Take it in the room if you can: by Thursday you will have forgotten the session, and the feedback will be worth less to you.\n\u2022 ONE attempt, from your signed-in Google account. You cannot reopen it or change an answer, so read each question once, properly.\n\u2022 The first box asks for your registration number. It is the number printed on your student card, and it is how the mark reaches your record.\n\u2022 Five questions, one mark each, worth 1% of your final mark.\n\u2022 Your best ten of twelve quizzes count. Missing two costs you nothing, and there are no resits.\n\u2022 When you submit, tap View score. You get a tick or a cross on each question with the feedback underneath. Your mark is the number of ticks, and the feedback on anything you got wrong is the part worth reading.\n\u2022 A question left blank scores the same as one answered wrongly, so answer all five.",
        "questions": [
          {
            "n": 1,
            "kind": "diagnosis",
            "title": "This reports a good test score. Why can that score not be trusted?",
            "help": "scaler = StandardScaler()\nX_scaled = scaler.fit_transform(X)     # whole file\n\nX_tr, X_te, y_tr, y_te = train_test_split(X_scaled, y)\nmodel.fit(X_tr, y_tr)\nprint(model.score(X_te, y_te))",
            "choices": [
              {
                "text": "The scaler was fitted on the whole file, so the test rows helped set the scaling",
                "correct": true
              },
              {
                "text": "The split should come before the features are selected",
                "correct": false
              },
              {
                "text": "StandardScaler is the wrong scaler for this data",
                "correct": false
              },
              {
                "text": "Nothing is wrong; scaling does not use the target",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. The test rows are supposed to stand in for cases you have never seen, and here they helped set the scaling. Put the scaler in a Pipeline and fit it after the split, so it only ever sees training rows.",
            "fbWrong": "THE ANSWER: The scaler was fitted on the whole file, so the test rows helped set the scaling. The test rows are supposed to stand in for cases you have never seen, and here they helped set the scaling. Put the scaler in a Pipeline and fit it after the split, so it only ever sees training rows.\n\nWhy the others are wrong. \u201cThe split should come before the features are selected\u201d \u2014 Selecting which columns to use is fine either side. Measuring something from the data is what has to wait until after the split.  \u201cStandardScaler is the wrong scaler for this data\u201d \u2014 The choice of scaler is a separate question. Any scaler fitted before the split leaks in the same way.  \u201cNothing is wrong; scaling does not use the target\u201d \u2014 Leakage does not require the target. Borrowing the test rows' mean and spread means the test set is no longer a clean estimate, and how far the number is distorted is not something you can work out from the outside, which is the real cost."
          },
          {
            "n": 2,
            "kind": "diagnosis",
            "title": "Which of the three error stories does this pattern match?",
            "help": "training score   0.98\ntest score       0.61",
            "choices": [
              {
                "text": "The model has memorised its training rows and does not generalise",
                "correct": true
              },
              {
                "text": "The two scores are measuring different quantities",
                "correct": false
              },
              {
                "text": "Information has leaked from the test set into training",
                "correct": false
              },
              {
                "text": "The model is too simple to capture the pattern",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. A high training score with a much lower test score is the signature of a model with too much freedom for the data. Simplify it, constrain it, or get more rows.",
            "fbWrong": "THE ANSWER: The model has memorised its training rows and does not generalise. A high training score with a much lower test score is the signature of a model with too much freedom for the data. Simplify it, constrain it, or get more rows.\n\nWhy the others are wrong. \u201cThe two scores are measuring different quantities\u201d \u2014 Both are the same measure on different rows. That is what makes the comparison meaningful.  \u201cInformation has leaked from the test set into training\u201d \u2014 Leakage usually makes both scores look good, since the model has effectively seen the answers. A large gap points the other way.  \u201cThe model is too simple to capture the pattern\u201d \u2014 A model that is too simple scores poorly on both, because it cannot even fit the rows it was given. Here it fits them almost perfectly."
          },
          {
            "n": 3,
            "kind": "traceback",
            "title": "A teammate has already tried to deal with the gaps, in the cell shown above the traceback. Read both, then say what you would change.",
            "help": "imp = SimpleImputer(strategy=\"mean\")\nX[[\"RH\"]] = imp.fit_transform(X[[\"RH\"]])\n\nX_tr, X_te, y_tr, y_te = train_test_split(X, y)\npipe = Pipeline([(\"model\", Ridge())])\npipe.fit(X_tr, y_tr)\n\nTraceback (most recent call last):\n  File \"<ipython-input-13-1a2b3c>\", line 6, in <module>\n    pipe.fit(X_tr, y_tr)\nValueError: Input X contains NaN.",
            "choices": [
              {
                "text": "Impute the remaining columns the same way, before the split",
                "correct": false
              },
              {
                "text": "Replace the remaining gaps with zero so the model can fit",
                "correct": false
              },
              {
                "text": "Move the imputer inside the Pipeline, and cover every column",
                "correct": true
              },
              {
                "text": "Drop the rows that still contain gaps",
                "correct": false
              }
            ],
            "fbCorrect": "Correct on both counts. Only one column was imputed, so the gaps in the others are still there, which is why the error still fires. And fitting it on the whole frame before the split measures the test rows, which is the leak from question one wearing different clothes. Inside the pipeline both problems go away at once.",
            "fbWrong": "THE ANSWER: Move the imputer inside the Pipeline, and cover every column. Correct on both counts. Only one column was imputed, so the gaps in the others are still there, which is why the error still fires. And fitting it on the whole frame before the split measures the test rows, which is the leak from question one wearing different clothes. Inside the pipeline both problems go away at once.\n\nWhy the others are wrong. \u201cImpute the remaining columns the same way, before the split\u201d \u2014 That silences the error and keeps the leak. Every value the imputer learns before the split has been measured partly from the test rows.  \u201cReplace the remaining gaps with zero so the model can fit\u201d \u2014 Zero is a real value on these columns, so this quietly invents low readings. Week 6 covers the damage that does.  \u201cDrop the rows that still contain gaps\u201d \u2014 It would run, and it discards data and can bias what is left if the gaps cluster in one source, which Week 4 showed they often do."
          },
          {
            "n": 4,
            "kind": "interpretation",
            "title": "You run five-fold cross-validation and get these scores. What should you report, and what should you look at?",
            "help": "fold scores: 0.71, 0.68, 0.74, 0.52, 0.70\nmean 0.67",
            "choices": [
              {
                "text": "Nothing yet; five folds is too few to report",
                "correct": false
              },
              {
                "text": "The mean with its spread, and look into the 0.52 fold",
                "correct": true
              },
              {
                "text": "The mean alone, since averaging is the purpose of cross-validation",
                "correct": false
              },
              {
                "text": "The best fold, since it shows what the model can achieve",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. Four folds sit close together and one sits well below, which suggests that fold contains something the others do not. Group structure in the rows is the usual explanation, and it is the subject of the next question.",
            "fbWrong": "THE ANSWER: The mean with its spread, and look into the 0.52 fold. Four folds sit close together and one sits well below, which suggests that fold contains something the others do not. Group structure in the rows is the usual explanation, and it is the subject of the next question.\n\nWhy the others are wrong. \u201cNothing yet; five folds is too few to report\u201d \u2014 Five folds is a standard choice and perfectly reportable. The spread is part of the report rather than a reason to withhold it.  \u201cThe mean alone, since averaging is the purpose of cross-validation\u201d \u2014 A bare mean hides the thing worth knowing. Reporting 0.67 with no spread conceals a fold that scored 0.52 and the reason behind it.  \u201cThe best fold, since it shows what the model can achieve\u201d \u2014 Quoting the best fold is selecting the most flattering result from your own experiment."
          },
          {
            "n": 5,
            "kind": "judgement",
            "title": "You discover that consecutive hours are split at random across your training and test sets, and that one hour is almost the same reading as the hour before it. What should you do?",
            "help": "",
            "choices": [
              {
                "text": "Leave it, because a random split is unbiased by definition",
                "correct": false
              },
              {
                "text": "Split on time: train on an earlier stretch, test on a later one",
                "correct": true
              },
              {
                "text": "Remove the near-identical consecutive rows",
                "correct": false
              },
              {
                "text": "Increase the size of the test set",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. The structure here is time, so the split has to respect time. A random split puts the hour before and the hour after into training while testing on the hour between, which is close to handing over the answer. It also matches the real task, which is predicting forward rather than filling in gaps. TimeSeriesSplit does this.",
            "fbWrong": "THE ANSWER: Split on time: train on an earlier stretch, test on a later one. The structure here is time, so the split has to respect time. A random split puts the hour before and the hour after into training while testing on the hour between, which is close to handing over the answer. It also matches the real task, which is predicting forward rather than filling in gaps. TimeSeriesSplit does this.\n\nWhy the others are wrong. \u201cLeave it, because a random split is unbiased by definition\u201d \u2014 Random over rows takes no account of the fact that consecutive hours are nearly the same reading. Unbiased selection of rows is not the same as an honest test.  \u201cRemove the near-identical consecutive rows\u201d \u2014 They are genuine samples of a continuing state, and thinning them changes what the model sees without fixing the fact that neighbouring hours straddle the split.  \u201cIncrease the size of the test set\u201d \u2014 A bigger test set assembled the same way is optimistic in the same way."
          }
        ]
      },
      {
        "week": 11,
        "number": 10,
        "title": "CML3111 \u00b7 Weekly Quiz 10 \u2014 Features",
        "intro": "Read what each question shows you. None of them can be answered without it.\n\nHOW THIS WORKS\n\u2022 Answer it now, in the 5 minutes on the screen. That is when this is meant to be taken, while the session is still fresh.\n\u2022 The form then stays open for 24 hours and closes itself. That window is there so a dead network or a broken phone does not cost you a mark you had earned. Take it in the room if you can: by Thursday you will have forgotten the session, and the feedback will be worth less to you.\n\u2022 ONE attempt, from your signed-in Google account. You cannot reopen it or change an answer, so read each question once, properly.\n\u2022 The first box asks for your registration number. It is the number printed on your student card, and it is how the mark reaches your record.\n\u2022 Five questions, one mark each, worth 1% of your final mark.\n\u2022 Your best ten of twelve quizzes count. Missing two costs you nothing, and there are no resits.\n\u2022 When you submit, tap View score. You get a tick or a cross on each question with the feedback underneath. Your mark is the number of ticks, and the feedback on anything you got wrong is the part worth reading.\n\u2022 A question left blank scores the same as one answered wrongly, so answer all five.",
        "questions": [
          {
            "n": 1,
            "kind": "diagnosis",
            "title": "A teammate adds a scaler expecting an improvement and the score does not budge. Why not?",
            "help": "before:  DecisionTreeClassifier(random_state=0)\n                                             recall 0.61\nafter:   Pipeline([(\"scale\", StandardScaler()),\n                   (\"model\", DecisionTreeClassifier(\n                                 random_state=0))])\n                                             recall 0.61",
            "choices": [
              {
                "text": "A tree splits on the order of the values, and scaling preserves that order",
                "correct": true
              },
              {
                "text": "The scaler was placed after the model in the pipeline",
                "correct": false
              },
              {
                "text": "The tree needs a greater depth before scaling helps",
                "correct": false
              },
              {
                "text": "The features were already on the same scale",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. Rescaling moves the numbers and leaves their ranking untouched, and a threshold split only cares about ranking. Scaling earns its keep for models that measure distances or fit coefficients.",
            "fbWrong": "THE ANSWER: A tree splits on the order of the values, and scaling preserves that order. Rescaling moves the numbers and leaves their ranking untouched, and a threshold split only cares about ranking. Scaling earns its keep for models that measure distances or fit coefficients.\n\nWhy the others are wrong. \u201cThe scaler was placed after the model in the pipeline\u201d \u2014 It is first, which is the correct position. The order in the pipeline is not the issue.  \u201cThe tree needs a greater depth before scaling helps\u201d \u2014 Depth changes how the tree fits and never makes it sensitive to a monotonic rescaling.  \u201cThe features were already on the same scale\u201d \u2014 Even if they were, that would not be the reason. A tree is unaffected by this kind of rescaling whatever the starting scales happen to be."
          },
          {
            "n": 2,
            "kind": "diagnosis",
            "title": "The score on your own test split improves after this change, and the model is worse. What has happened?",
            "help": "print(df.shape)\n(10000, 14)\n\nprint(df[\"product_id\"].nunique())\n847\n\nX = pd.get_dummies(df, columns=[\"product_id\"])\nprint(X.shape)\n(10000, 860)",
            "choices": [
              {
                "text": "It added one column per identifier, so the model can now recognise individual units",
                "correct": true
              },
              {
                "text": "get_dummies should have been given the whole frame",
                "correct": false
              },
              {
                "text": "It made the frame too wide for the model to fit",
                "correct": false
              },
              {
                "text": "The identifiers should have been numbered 1 to 847 instead",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. An identifier expanded this way hands the model a lookup table for the units in your file. It scores well wherever the same units appear on both sides of the split and carries nothing to a new one. Drop the identifier and keep the columns that describe the thing.",
            "fbWrong": "THE ANSWER: It added one column per identifier, so the model can now recognise individual units. An identifier expanded this way hands the model a lookup table for the units in your file. It scores well wherever the same units appear on both sides of the split and carries nothing to a new one. Drop the identifier and keep the columns that describe the thing.\n\nWhy the others are wrong. \u201cget_dummies should have been given the whole frame\u201d \u2014 It was given the whole frame with one column named for expansion, which is the normal usage. The choice of column is the fault.  \u201cIt made the frame too wide for the model to fit\u201d \u2014 A few hundred columns is unremarkable and fits without complaint. The problem is what those columns mean.  \u201cThe identifiers should have been numbered 1 to 847 instead\u201d \u2014 That is worse: it tells a straight-line model that unit 800 is a hundred times unit 8. Neither encoding rescues a column that is only a label."
          },
          {
            "n": 3,
            "kind": "traceback",
            "title": "What has happened, and what is the catch in the obvious fix?",
            "help": "enc = OneHotEncoder(drop=\"first\")\n# ... fitted on product_type values L, M, H\n\nTraceback (most recent call last):\n  File \"<ipython-input-15-6d7e8f>\", line 1, in <module>\n    pipe.predict(new_rows)\nValueError: Found unknown categories ['X'] in column 0\nduring transform",
            "choices": [
              {
                "text": "The category column should be dropped from the model",
                "correct": false
              },
              {
                "text": "Refitting the encoder on the new rows as well will fix it properly",
                "correct": false
              },
              {
                "text": "handle_unknown=\"ignore\" clears it, and with drop=\"first\" an unseen category then encodes as the dropped one",
                "correct": true
              },
              {
                "text": "Adding handle_unknown=\"ignore\" solves it cleanly, with no side effect worth worrying about",
                "correct": false
              }
            ],
            "fbCorrect": "Correct, and the second half is the part almost nobody is told. An ignored unknown category is encoded as all zeros, which is exactly how the dropped reference category is encoded, so every new category silently becomes the baseline. Choose one of the two options deliberately and count how often an unknown value arrives.",
            "fbWrong": "THE ANSWER: handle_unknown=\"ignore\" clears it, and with drop=\"first\" an unseen category then encodes as the dropped one. The second half is the part almost nobody is told. An ignored unknown category is encoded as all zeros, which is exactly how the dropped reference category is encoded, so every new category silently becomes the baseline. Choose one of the two options deliberately and count how often an unknown value arrives.\n\nWhy the others are wrong. \u201cThe category column should be dropped from the model\u201d \u2014 It may be carrying real signal. The task is to encode it so it survives a value you have not seen before.  \u201cRefitting the encoder on the new rows as well will fix it properly\u201d \u2014 Fitting anything on rows you are about to predict is the leakage pattern from Week 10. It also cannot work in service, where the new value arrives after the model is deployed.  \u201cAdding handle_unknown=\"ignore\" solves it cleanly, with no side effect worth worrying about\u201d \u2014 It does clear the error. The side effect is that the unknown category is encoded as all zeros, and because drop=\"first\" is set, that is the same encoding as the dropped category."
          },
          {
            "n": 4,
            "kind": "interpretation",
            "title": "Each row removes one feature and refits. Which feature has earned its place least?",
            "help": "features                   recall (failures)\nall five                                0.78\nminus mechanical power                  0.51\nminus temperature rise                  0.46\nminus tool wear                         0.77\nminus rotational speed                  0.72\nminus torque                            0.68",
            "choices": [
              {
                "text": "Tool wear, because removing it moves recall by one percentage point",
                "correct": true
              },
              {
                "text": "Temperature rise, because it has the lowest recall when removed",
                "correct": false
              },
              {
                "text": "None of them; every feature earns its place",
                "correct": false
              },
              {
                "text": "Mechanical power, because 0.51 is a poor result",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. Mechanical power and temperature rise each cost you around 30 points of recall when removed, and tool wear costs one. On this evidence it is nearly redundant.",
            "fbWrong": "THE ANSWER: Tool wear, because removing it moves recall by one percentage point. Mechanical power and temperature rise each cost you around 30 points of recall when removed, and tool wear costs one. On this evidence it is nearly redundant.\n\nWhy the others are wrong. \u201cTemperature rise, because it has the lowest recall when removed\u201d \u2014 Lowest recall without a feature means the model depends on it most. The reading is inverted.  \u201cNone of them; every feature earns its place\u201d \u2014 One point of recall is within the fold-to-fold spread you would expect.  \u201cMechanical power, because 0.51 is a poor result\u201d \u2014 0.51 is the recall you are left with when it is gone, which is the argument for keeping it."
          },
          {
            "n": 5,
            "kind": "judgement",
            "title": "Two teams reach almost the same recall. One uses a random forest on the raw columns; the other uses logistic regression on mechanical power and four other engineered features. The maintenance planner has to justify every four-hour stop. Which do you recommend?",
            "help": "",
            "choices": [
              {
                "text": "The engineered features with the simpler model, whose reasoning can be read off and defended",
                "correct": true
              },
              {
                "text": "Either, since the error is what matters",
                "correct": false
              },
              {
                "text": "The random forest, because ensembles generalise better in general",
                "correct": false
              },
              {
                "text": "The random forest, and add an importance chart to explain it",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. On equal performance the stated constraint decides it, and a coefficient on a quantity with physical meaning is something you can put in front of the person who has to sign. The engineering went into the features rather than the algorithm.",
            "fbWrong": "THE ANSWER: The engineered features with the simpler model, whose reasoning can be read off and defended. On equal performance the stated constraint decides it, and a coefficient on a quantity with physical meaning is something you can put in front of the person who has to sign. The engineering went into the features rather than the algorithm.\n\nWhy the others are wrong. \u201cEither, since the error is what matters\u201d \u2014 The error was stated as a condition to meet rather than the only criterion. Explainability was given as a requirement.  \u201cThe random forest, because ensembles generalise better in general\u201d \u2014 It may well generalise better on some problems, and here the two are level while only one of them satisfies the constraint you were given.  \u201cThe random forest, and add an importance chart to explain it\u201d \u2014 Feature importance tells you which columns the model leaned on overall. It does not tell the client why this particular case was rejected, which is the question they will ask."
          }
        ]
      },
      {
        "week": 12,
        "number": 11,
        "title": "CML3111 \u00b7 Weekly Quiz 11 \u2014 Model comparison (integrative)",
        "intro": "Read what each question shows you. None of them can be answered without it.\n\nHOW THIS WORKS\n\u2022 Answer it now, in the 5 minutes on the screen. That is when this is meant to be taken, while the session is still fresh.\n\u2022 The form then stays open for 24 hours and closes itself. That window is there so a dead network or a broken phone does not cost you a mark you had earned. Take it in the room if you can: by Thursday you will have forgotten the session, and the feedback will be worth less to you.\n\u2022 ONE attempt, from your signed-in Google account. You cannot reopen it or change an answer, so read each question once, properly.\n\u2022 The first box asks for your registration number. It is the number printed on your student card, and it is how the mark reaches your record.\n\u2022 Five questions, one mark each, worth 1% of your final mark.\n\u2022 Your best ten of twelve quizzes count. Missing two costs you nothing, and there are no resits.\n\u2022 When you submit, tap View score. You get a tick or a cross on each question with the feedback underneath. Your mark is the number of ticks, and the feedback on anything you got wrong is the part worth reading.\n\u2022 A question left blank scores the same as one answered wrongly, so answer all five.",
        "questions": [
          {
            "n": 1,
            "kind": "diagnosis",
            "title": "A teammate concludes the forest is the better model. What does this table actually support?",
            "help": "fold                  1      2      3      4      5   mean\nrandom forest      0.78   0.70   0.76   0.71   0.75   0.74\nlogistic reg.      0.75   0.73   0.72   0.68   0.72   0.72\ndifference        +0.03  -0.03  +0.04  +0.03  +0.03",
            "choices": [
              {
                "text": "The comparison is invalid because the models share folds",
                "correct": false
              },
              {
                "text": "Very little: the difference changes sign between folds, so on this evidence the two cannot be separated",
                "correct": true
              },
              {
                "text": "The forest is better, because it wins the majority of folds",
                "correct": false
              },
              {
                "text": "The forest is better, since it has the stronger mean",
                "correct": false
              }
            ],
            "fbCorrect": "Correct, and reading the per-fold differences is what settles it. The sign of the difference flips from fold to fold, so the mean gap of 0.02 is not a consistent advantage. Report them as level on this data and let the stated constraints decide. Note what makes this readable at all: both models were scored on the SAME five folds, so the differences can be paired up.",
            "fbWrong": "THE ANSWER: Very little: the difference changes sign between folds, so on this evidence the two cannot be separated. Reading the per-fold differences is what settles it. The sign of the difference flips from fold to fold, so the mean gap of 0.02 is not a consistent advantage. Report them as level on this data and let the stated constraints decide. Note what makes this readable at all: both models were scored on the SAME five folds, so the differences can be paired up.\n\nWhy the others are wrong. \u201cThe comparison is invalid because the models share folds\u201d \u2014 Sharing folds is what makes the comparison valid. Scoring each model on its own random split is the mistake, and it is the subject of the next question.  \u201cThe forest is better, because it wins the majority of folds\u201d \u2014 Winning more folds than it loses is worth noticing and is weak evidence at this margin, because the fold it loses it loses by as much as the others are won. With only five folds this pattern arises easily between two models of equal ability.  \u201cThe forest is better, since it has the stronger mean\u201d \u2014 A mean hides the fold-by-fold picture. Here the sign of the difference flips, which is the pattern of two models that are level rather than one that is ahead."
          },
          {
            "n": 2,
            "kind": "diagnosis",
            "title": "Two models, two scores, no error anywhere. Why can these numbers not be compared?",
            "help": "# model A\nX_tr, X_te, y_tr, y_te = train_test_split(X, y,\n                              random_state=1)\n# ... fit A ...      score 0.78\n\n# model B\nX_tr, X_te, y_tr, y_te = train_test_split(X, y,\n                              random_state=7)\n# ... fit B ...      score 0.81",
            "choices": [
              {
                "text": "Nothing is wrong, since both used the same data file",
                "correct": false
              },
              {
                "text": "Model B had the advantage of a later random state",
                "correct": false
              },
              {
                "text": "The scores need to be averaged together",
                "correct": false
              },
              {
                "text": "They were scored on different test sets, so the gap may be the split rather than the model",
                "correct": true
              }
            ],
            "fbCorrect": "Correct. Changing the seed changes the split, and split-to-split variation on this kind of data is often larger than the gap you are trying to measure. Score every model on identical folds, which is what cross_val_score with a fixed splitter gives you.",
            "fbWrong": "THE ANSWER: They were scored on different test sets, so the gap may be the split rather than the model. Changing the seed changes the split, and split-to-split variation on this kind of data is often larger than the gap you are trying to measure. Score every model on identical folds, which is what cross_val_score with a fixed splitter gives you.\n\nWhy the others are wrong. \u201cNothing is wrong, since both used the same data file\u201d \u2014 The same file cut two different ways gives two different test sets. The comparison needs the cuts to match.  \u201cModel B had the advantage of a later random state\u201d \u2014 The number in random_state is a label for a shuffle and carries no ordering. Seed 7 is not later or better than seed 1.  \u201cThe scores need to be averaged together\u201d \u2014 Averaging two figures measured on different test sets produces a number that describes neither model."
          },
          {
            "n": 3,
            "kind": "traceback",
            "title": "You have run this notebook for an hour and now get this. What is the most likely history behind it?",
            "help": "Traceback (most recent call last):\n  File \"<ipython-input-31-9a8b7c>\", line 1, in <module>\n    print(forest.predict(X_te)[:5])\nNotFittedError: This RandomForestClassifier instance is not\nfitted yet. Call 'fit' with appropriate arguments before\nusing this estimator.",
            "choices": [
              {
                "text": "The forest needs more trees before it can predict",
                "correct": false
              },
              {
                "text": "The model does not support predict on a test set",
                "correct": false
              },
              {
                "text": "The cell that creates the model was re-run after the one that fitted it",
                "correct": true
              },
              {
                "text": "The test features contain missing values",
                "correct": false
              }
            ],
            "fbCorrect": "Correct, and this is the Week 2 out-of-order trap arriving in a much more expensive place. Re-running the constructor throws away an hour of fitting. Restart and Run All is how you find out whether your notebook still tells a straight story.",
            "fbWrong": "THE ANSWER: The cell that creates the model was re-run after the one that fitted it. This is the Week 2 out-of-order trap arriving in a much more expensive place. Re-running the constructor throws away an hour of fitting. Restart and Run All is how you find out whether your notebook still tells a straight story.\n\nWhy the others are wrong. \u201cThe forest needs more trees before it can predict\u201d \u2014 The number of trees is set at construction and any number can be fitted and used. This one was never fitted.  \u201cThe model does not support predict on a test set\u201d \u2014 It does. The message is specifically that this instance has never been fitted.  \u201cThe test features contain missing values\u201d \u2014 That reports itself as an error about NaN, and it would only arise once the model was fitted."
          },
          {
            "n": 4,
            "kind": "interpretation",
            "title": "Two outputs from the same forest. The planner needs to know why THIS machine was flagged today. Which output answers that, and what does the other one tell you?",
            "help": "A   feature_importances_ over the whole training set\n      mechanical power 0.41\n      temp rise        0.29\n      tool wear        0.18\n      rot speed        0.12\n\nB   contribution to the prediction for machine 14\n      temp rise 96 K   pushed toward fail    +0.22\n      power 4.8 kW     pushed toward fail    +0.15\n      tool wear 40 min pushed toward normal  -0.04",
            "choices": [
              {
                "text": "A answers it, because the highest-importance feature is the reason for any given decision",
                "correct": false
              },
              {
                "text": "Both answer it equally well, since they rank the same features",
                "correct": false
              },
              {
                "text": "Neither answers it, because a forest can never be explained at all",
                "correct": false
              },
              {
                "text": "B answers it, because it is specific to this case; A describes the model's average behaviour across all cases",
                "correct": true
              }
            ],
            "fbCorrect": "Correct, and the distinction is worth holding on to. A global importance chart says what the model relies on in general and can never say why one case came out as it did. A per-case breakdown is what a client's question actually needs.",
            "fbWrong": "THE ANSWER: B answers it, because it is specific to this case; A describes the model's average behaviour across all cases. The distinction is worth holding on to. A global importance chart says what the model relies on in general and can never say why one case came out as it did. A per-case breakdown is what a client's question actually needs.\n\nWhy the others are wrong. \u201cA answers it, because the highest-importance feature is the reason for any given decision\u201d \u2014 That does not follow. The most important feature overall can be unremarkable in this particular case, and here B shows a different feature leading for batch-level reasons.  \u201cBoth answer it equally well, since they rank the same features\u201d \u2014 They do not even rank them the same way, and more importantly they answer different questions. One is about the model, the other about a case.  \u201cNeither answers it, because a forest can never be explained at all\u201d \u2014 Too pessimistic. Per-case attributions like B are exactly how you interrogate one prediction from an ensemble. The honest caveat is that they are estimates of the contribution rather than a rule you can read off."
          },
          {
            "n": 5,
            "kind": "judgement",
            "title": "The planner asks: your model called a stop on machine 14 this morning, why that machine and why today? The acceptance requirement is an exact, directly readable rule; post-hoc attribution is insufficient. You chose the forest. What is the honest position?",
            "help": "",
            "choices": [
              {
                "text": "Show the feature importance chart as the explanation",
                "correct": false
              },
              {
                "text": "Recommend a readable-rule model that meets the stated acceptance requirement",
                "correct": true
              },
              {
                "text": "Offer to retrain the forest with fewer trees so it is simpler",
                "correct": false
              },
              {
                "text": "Explain that the model is accurate and ask them to trust the result",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. The professional answer is to name the limitation and change the recommendation. A stated condition of acceptance that your chosen model cannot meet is a reason to change the model rather than to talk around it.",
            "fbWrong": "THE ANSWER: Recommend a readable-rule model that meets the stated acceptance requirement. The professional answer is to name the limitation and change the recommendation. A stated condition of acceptance that your chosen model cannot meet is a reason to change the model rather than to talk around it.\n\nWhy the others are wrong. \u201cShow the feature importance chart as the explanation\u201d \u2014 Importance describes the model's behaviour across the whole dataset. It cannot say why one case was decided as it was, which is the question you were asked.  \u201cOffer to retrain the forest with fewer trees so it is simpler\u201d \u2014 A smaller forest still does not meet this stated requirement for a directly readable rule. This concedes accuracy without gaining explainability.  \u201cExplain that the model is accurate and ask them to trust the result\u201d \u2014 They told you at the outset that they cannot act on an unexplained call. Asking for trust instead is not an answer."
          }
        ]
      },
      {
        "week": 13,
        "number": 12,
        "title": "CML3111 \u00b7 Weekly Quiz 12 \u2014 Reproducibility (integrative)",
        "intro": "Read what each question shows you. None of them can be answered without it.\n\nHOW THIS WORKS\n\u2022 Answer it now, in the 5 minutes on the screen. That is when this is meant to be taken, while the session is still fresh.\n\u2022 The form then stays open for 24 hours and closes itself. That window is there so a dead network or a broken phone does not cost you a mark you had earned. Take it in the room if you can: by Thursday you will have forgotten the session, and the feedback will be worth less to you.\n\u2022 ONE attempt, from your signed-in Google account. You cannot reopen it or change an answer, so read each question once, properly.\n\u2022 The first box asks for your registration number. It is the number printed on your student card, and it is how the mark reaches your record.\n\u2022 Five questions, one mark each, worth 1% of your final mark.\n\u2022 Your best ten of twelve quizzes count. Missing two costs you nothing, and there are no resits.\n\u2022 When you submit, tap View score. You get a tick or a cross on each question with the feedback underneath. Your mark is the number of ticks, and the feedback on anything you got wrong is the part worth reading.\n\u2022 A question left blank scores the same as one answered wrongly, so answer all five.",
        "questions": [
          {
            "n": 1,
            "kind": "diagnosis",
            "title": "This runs perfectly on the machine it was written on. What is wrong with it?",
            "help": "df = pd.read_csv(\n    \"C:/Users/Jotham/Desktop/motor_log_FINAL.csv\")",
            "choices": [
              {
                "text": "It names a location that exists on exactly one computer, so the notebook cannot run anywhere else",
                "correct": true
              },
              {
                "text": "Nothing, as long as you send the file with the notebook",
                "correct": false
              },
              {
                "text": "Backslashes should have been used for a Windows path",
                "correct": false
              },
              {
                "text": "The file should be read with a different pandas function",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. Keep the data inside the project and read it by a relative path such as data/\u2026 so the notebook works for anyone who has the folder. The version marker in the file name is a second warning: it suggests there are other copies and no record of which is current.",
            "fbWrong": "THE ANSWER: It names a location that exists on exactly one computer, so the notebook cannot run anywhere else. Keep the data inside the project and read it by a relative path such as data/\u2026 so the notebook works for anyone who has the folder. The version marker in the file name is a second warning: it suggests there are other copies and no record of which is current.\n\nWhy the others are wrong. \u201cNothing, as long as you send the file with the notebook\u201d \u2014 The recipient would have to recreate your user name and your desktop for the path to resolve. A relative path inside the project removes the problem entirely.  \u201cBackslashes should have been used for a Windows path\u201d \u2014 Forward slashes work on Windows in Python and avoid the escape problems backslashes cause. This is the better of the two styles and the location is still wrong.  \u201cThe file should be read with a different pandas function\u201d \u2014 read_csv is the right function for a CSV. The path is the problem."
          },
          {
            "n": 2,
            "kind": "diagnosis",
            "title": "You run the same notebook twice, changing nothing, and get these two numbers. What is going on, and what should you do?",
            "help": "run 1:   recall 0.74\nrun 2:   recall 0.69",
            "choices": [
              {
                "text": "The second run is the more trustworthy of the two",
                "correct": false
              },
              {
                "text": "The split and the model involve randomness that was never pinned down",
                "correct": true
              },
              {
                "text": "The data file is being modified between runs",
                "correct": false
              },
              {
                "text": "Report the average of the two runs",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. Without a seed, the rows that land in the test set and the internal choices a forest makes change every run. Set random_state on the split and on the model, and write the number in the notebook so a reader can reproduce your figure exactly.",
            "fbWrong": "THE ANSWER: The split and the model involve randomness that was never pinned down. Without a seed, the rows that land in the test set and the internal choices a forest makes change every run. Set random_state on the split and on the model, and write the number in the notebook so a reader can reproduce your figure exactly.\n\nWhy the others are wrong. \u201cThe second run is the more trustworthy of the two\u201d \u2014 Neither is more trustworthy. That two runs differ by this much is itself the finding, and it says your single reported figure carries this much uncertainty.  \u201cThe data file is being modified between runs\u201d \u2014 Nothing here writes to the file. Unseeded randomness explains this without needing the data to change.  \u201cReport the average of the two runs\u201d \u2014 An average of two arbitrary draws is still arbitrary. Seed the randomness, and if you want a figure with a spread, cross-validate deliberately."
          },
          {
            "n": 3,
            "kind": "traceback",
            "title": "A classmate clones your repository and gets this on the first cell. What is the cause?",
            "help": "Traceback (most recent call last):\n  File \"<ipython-input-1-3e4f5a>\", line 1, in <module>\n    df = pd.read_csv(\"ai4i2020.csv\")\nFileNotFoundError: [Errno 2] No such file or directory:\n'ai4i2020.csv'",
            "choices": [
              {
                "text": "The data file was never committed, or sits elsewhere",
                "correct": true
              },
              {
                "text": "The repository was cloned incorrectly",
                "correct": false
              },
              {
                "text": "The classmate is missing a package",
                "correct": false
              },
              {
                "text": "The file name has the wrong extension",
                "correct": false
              }
            ],
            "fbCorrect": "Correct, and both halves are worth checking. Data is often left out of a repository deliberately because of size or licence, in which case the README has to say where to get it and where to put it. Otherwise the path needs to match the folder layout.",
            "fbWrong": "THE ANSWER: The data file was never committed, or sits elsewhere. Both halves are worth checking. Data is often left out of a repository deliberately because of size or licence, in which case the README has to say where to get it and where to put it. Otherwise the path needs to match the folder layout.\n\nWhy the others are wrong. \u201cThe repository was cloned incorrectly\u201d \u2014 A clone that failed would leave you with no notebook to run. The notebook arrived and its data did not.  \u201cThe classmate is missing a package\u201d \u2014 A missing package reports itself as ModuleNotFoundError. This message is about a file.  \u201cThe file name has the wrong extension\u201d \u2014 The extension matches a CSV read. The file is simply not at that location."
          },
          {
            "n": 4,
            "kind": "interpretation",
            "title": "Two captions for the same chart. Which one does the job a caption exists to do, and why?",
            "help": "A:  Figure 3: failures against tool wear.\n\nB:  Figure 3: the failure rate rises sharply above 200\n    minutes of tool wear, from 2 per cent to 11 per cent.",
            "choices": [
              {
                "text": "A, because a caption should describe the chart and let the reader draw the conclusion",
                "correct": false
              },
              {
                "text": "Neither; captions should give the data source instead",
                "correct": false
              },
              {
                "text": "B, because it states the finding and its size, so a reader who only reads the captions still learns the result",
                "correct": true
              },
              {
                "text": "A, because B might be wrong and the caption would then be misleading",
                "correct": false
              }
            ],
            "fbCorrect": "Correct. A caption is often the only part of your work that gets read. B carries the conclusion and the magnitude, which is what makes it useful and also what makes it checkable against the chart.",
            "fbWrong": "THE ANSWER: B, because it states the finding and its size, so a reader who only reads the captions still learns the result. A caption is often the only part of your work that gets read. B carries the conclusion and the magnitude, which is what makes it useful and also what makes it checkable against the chart.\n\nWhy the others are wrong. \u201cA, because a caption should describe the chart and let the reader draw the conclusion\u201d \u2014 A describes the axes, which the axis labels already do. It leaves the reader to rediscover something you already know.  \u201cNeither; captions should give the data source instead\u201d \u2014 The source belongs in the caption or nearby and does not replace the finding. B plus a source is the target.  \u201cA, because B might be wrong and the caption would then be misleading\u201d \u2014 A claim you can check is a feature. If B is wrong the chart will show it, whereas A cannot be wrong because it says nothing."
          },
          {
            "n": 5,
            "kind": "judgement",
            "title": "Your notebook has three separate cells that each assign df, and nobody wrote down the order they should run in. Submission is tomorrow. What do you do?",
            "help": "",
            "choices": [
              {
                "text": "Add a comment above each cell saying what order to run them in",
                "correct": false
              },
              {
                "text": "Delete two of the three cells and hope the notebook still runs",
                "correct": false
              },
              {
                "text": "Restart and Run All, then fix whatever breaks until it runs clean from top to bottom",
                "correct": true
              },
              {
                "text": "Leave it, since you know the right order",
                "correct": false
              }
            ],
            "fbCorrect": "Correct, and do it before you are tired. That single action converts a notebook that works on your screen into one that works from an empty memory, which is the only version anyone else can use. Consolidating the three assignments into one clear sequence is usually the fix.",
            "fbWrong": "THE ANSWER: Restart and Run All, then fix whatever breaks until it runs clean from top to bottom. Do it before you are tired. That single action converts a notebook that works on your screen into one that works from an empty memory, which is the only version anyone else can use. Consolidating the three assignments into one clear sequence is usually the fix.\n\nWhy the others are wrong. \u201cAdd a comment above each cell saying what order to run them in\u201d \u2014 Instructions to run cells out of order are a description of the problem. Anyone who follows them slightly differently gets a different answer.  \u201cDelete two of the three cells and hope the notebook still runs\u201d \u2014 Each of them may be doing something needed. Running from a clean state tells you what is required rather than leaving you to guess.  \u201cLeave it, since you know the right order\u201d \u2014 That knowledge is not in the file, so it does not survive you. It also will not survive next week for you either."
          }
        ]
      }
    ]
  }
};

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
// Open a quiz for its sitting.

function open_W1_CML3112() { openQuizFor(1, 'CML3112'); }
function open_W2_CML3112() { openQuizFor(2, 'CML3112'); }
function open_W3_CML3112() { openQuizFor(3, 'CML3112'); }
function open_W4_CML3112() { openQuizFor(4, 'CML3112'); }
function open_W5_CML3112() { openQuizFor(5, 'CML3112'); }
function open_W6_CML3112() { openQuizFor(6, 'CML3112'); }
function open_W8_CML3112() { openQuizFor(8, 'CML3112'); }
function open_W9_CML3112() { openQuizFor(9, 'CML3112'); }
function open_W10_CML3112() { openQuizFor(10, 'CML3112'); }
function open_W11_CML3112() { openQuizFor(11, 'CML3112'); }
function open_W12_CML3112() { openQuizFor(12, 'CML3112'); }
function open_W13_CML3112() { openQuizFor(13, 'CML3112'); }
function open_W1_CML3113() { openQuizFor(1, 'CML3113'); }
function open_W2_CML3113() { openQuizFor(2, 'CML3113'); }
function open_W3_CML3113() { openQuizFor(3, 'CML3113'); }
function open_W4_CML3113() { openQuizFor(4, 'CML3113'); }
function open_W5_CML3113() { openQuizFor(5, 'CML3113'); }
function open_W6_CML3113() { openQuizFor(6, 'CML3113'); }
function open_W8_CML3113() { openQuizFor(8, 'CML3113'); }
function open_W9_CML3113() { openQuizFor(9, 'CML3113'); }
function open_W10_CML3113() { openQuizFor(10, 'CML3113'); }
function open_W11_CML3113() { openQuizFor(11, 'CML3113'); }
function open_W12_CML3113() { openQuizFor(12, 'CML3113'); }
function open_W13_CML3113() { openQuizFor(13, 'CML3113'); }
function open_W1_CML3111() { openQuizFor(1, 'CML3111'); }
function open_W2_CML3111() { openQuizFor(2, 'CML3111'); }
function open_W3_CML3111() { openQuizFor(3, 'CML3111'); }
function open_W4_CML3111() { openQuizFor(4, 'CML3111'); }
function open_W5_CML3111() { openQuizFor(5, 'CML3111'); }
function open_W6_CML3111() { openQuizFor(6, 'CML3111'); }
function open_W8_CML3111() { openQuizFor(8, 'CML3111'); }
function open_W9_CML3111() { openQuizFor(9, 'CML3111'); }
function open_W10_CML3111() { openQuizFor(10, 'CML3111'); }
function open_W11_CML3111() { openQuizFor(11, 'CML3111'); }
function open_W12_CML3111() { openQuizFor(12, 'CML3111'); }
function open_W13_CML3111() { openQuizFor(13, 'CML3111'); }

// Close one early. closeEverything() shuts all 36.

function close_W1_CML3112() { closeQuiz(1, 'CML3112'); }
function close_W2_CML3112() { closeQuiz(2, 'CML3112'); }
function close_W3_CML3112() { closeQuiz(3, 'CML3112'); }
function close_W4_CML3112() { closeQuiz(4, 'CML3112'); }
function close_W5_CML3112() { closeQuiz(5, 'CML3112'); }
function close_W6_CML3112() { closeQuiz(6, 'CML3112'); }
function close_W8_CML3112() { closeQuiz(8, 'CML3112'); }
function close_W9_CML3112() { closeQuiz(9, 'CML3112'); }
function close_W10_CML3112() { closeQuiz(10, 'CML3112'); }
function close_W11_CML3112() { closeQuiz(11, 'CML3112'); }
function close_W12_CML3112() { closeQuiz(12, 'CML3112'); }
function close_W13_CML3112() { closeQuiz(13, 'CML3112'); }
function close_W1_CML3113() { closeQuiz(1, 'CML3113'); }
function close_W2_CML3113() { closeQuiz(2, 'CML3113'); }
function close_W3_CML3113() { closeQuiz(3, 'CML3113'); }
function close_W4_CML3113() { closeQuiz(4, 'CML3113'); }
function close_W5_CML3113() { closeQuiz(5, 'CML3113'); }
function close_W6_CML3113() { closeQuiz(6, 'CML3113'); }
function close_W8_CML3113() { closeQuiz(8, 'CML3113'); }
function close_W9_CML3113() { closeQuiz(9, 'CML3113'); }
function close_W10_CML3113() { closeQuiz(10, 'CML3113'); }
function close_W11_CML3113() { closeQuiz(11, 'CML3113'); }
function close_W12_CML3113() { closeQuiz(12, 'CML3113'); }
function close_W13_CML3113() { closeQuiz(13, 'CML3113'); }
function close_W1_CML3111() { closeQuiz(1, 'CML3111'); }
function close_W2_CML3111() { closeQuiz(2, 'CML3111'); }
function close_W3_CML3111() { closeQuiz(3, 'CML3111'); }
function close_W4_CML3111() { closeQuiz(4, 'CML3111'); }
function close_W5_CML3111() { closeQuiz(5, 'CML3111'); }
function close_W6_CML3111() { closeQuiz(6, 'CML3111'); }
function close_W8_CML3111() { closeQuiz(8, 'CML3111'); }
function close_W9_CML3111() { closeQuiz(9, 'CML3111'); }
function close_W10_CML3111() { closeQuiz(10, 'CML3111'); }
function close_W11_CML3111() { closeQuiz(11, 'CML3111'); }
function close_W12_CML3111() { closeQuiz(12, 'CML3111'); }
function close_W13_CML3111() { closeQuiz(13, 'CML3111'); }

// Inspect one form's marking. auditAll() summarises all 36.

function audit_W1_CML3112() { auditForm(1, 'CML3112'); }
function audit_W2_CML3112() { auditForm(2, 'CML3112'); }
function audit_W3_CML3112() { auditForm(3, 'CML3112'); }
function audit_W4_CML3112() { auditForm(4, 'CML3112'); }
function audit_W5_CML3112() { auditForm(5, 'CML3112'); }
function audit_W6_CML3112() { auditForm(6, 'CML3112'); }
function audit_W8_CML3112() { auditForm(8, 'CML3112'); }
function audit_W9_CML3112() { auditForm(9, 'CML3112'); }
function audit_W10_CML3112() { auditForm(10, 'CML3112'); }
function audit_W11_CML3112() { auditForm(11, 'CML3112'); }
function audit_W12_CML3112() { auditForm(12, 'CML3112'); }
function audit_W13_CML3112() { auditForm(13, 'CML3112'); }
function audit_W1_CML3113() { auditForm(1, 'CML3113'); }
function audit_W2_CML3113() { auditForm(2, 'CML3113'); }
function audit_W3_CML3113() { auditForm(3, 'CML3113'); }
function audit_W4_CML3113() { auditForm(4, 'CML3113'); }
function audit_W5_CML3113() { auditForm(5, 'CML3113'); }
function audit_W6_CML3113() { auditForm(6, 'CML3113'); }
function audit_W8_CML3113() { auditForm(8, 'CML3113'); }
function audit_W9_CML3113() { auditForm(9, 'CML3113'); }
function audit_W10_CML3113() { auditForm(10, 'CML3113'); }
function audit_W11_CML3113() { auditForm(11, 'CML3113'); }
function audit_W12_CML3113() { auditForm(12, 'CML3113'); }
function audit_W13_CML3113() { auditForm(13, 'CML3113'); }
function audit_W1_CML3111() { auditForm(1, 'CML3111'); }
function audit_W2_CML3111() { auditForm(2, 'CML3111'); }
function audit_W3_CML3111() { auditForm(3, 'CML3111'); }
function audit_W4_CML3111() { auditForm(4, 'CML3111'); }
function audit_W5_CML3111() { auditForm(5, 'CML3111'); }
function audit_W6_CML3111() { auditForm(6, 'CML3111'); }
function audit_W8_CML3111() { auditForm(8, 'CML3111'); }
function audit_W9_CML3111() { auditForm(9, 'CML3111'); }
function audit_W10_CML3111() { auditForm(10, 'CML3111'); }
function audit_W11_CML3111() { auditForm(11, 'CML3111'); }
function audit_W12_CML3111() { auditForm(12, 'CML3111'); }
function audit_W13_CML3111() { auditForm(13, 'CML3111'); }

// Read back the marks Forms computed for one quiz.

function show_W1_CML3112() { showScores(1, 'CML3112'); }
function show_W2_CML3112() { showScores(2, 'CML3112'); }
function show_W3_CML3112() { showScores(3, 'CML3112'); }
function show_W4_CML3112() { showScores(4, 'CML3112'); }
function show_W5_CML3112() { showScores(5, 'CML3112'); }
function show_W6_CML3112() { showScores(6, 'CML3112'); }
function show_W8_CML3112() { showScores(8, 'CML3112'); }
function show_W9_CML3112() { showScores(9, 'CML3112'); }
function show_W10_CML3112() { showScores(10, 'CML3112'); }
function show_W11_CML3112() { showScores(11, 'CML3112'); }
function show_W12_CML3112() { showScores(12, 'CML3112'); }
function show_W13_CML3112() { showScores(13, 'CML3112'); }
function show_W1_CML3113() { showScores(1, 'CML3113'); }
function show_W2_CML3113() { showScores(2, 'CML3113'); }
function show_W3_CML3113() { showScores(3, 'CML3113'); }
function show_W4_CML3113() { showScores(4, 'CML3113'); }
function show_W5_CML3113() { showScores(5, 'CML3113'); }
function show_W6_CML3113() { showScores(6, 'CML3113'); }
function show_W8_CML3113() { showScores(8, 'CML3113'); }
function show_W9_CML3113() { showScores(9, 'CML3113'); }
function show_W10_CML3113() { showScores(10, 'CML3113'); }
function show_W11_CML3113() { showScores(11, 'CML3113'); }
function show_W12_CML3113() { showScores(12, 'CML3113'); }
function show_W13_CML3113() { showScores(13, 'CML3113'); }
function show_W1_CML3111() { showScores(1, 'CML3111'); }
function show_W2_CML3111() { showScores(2, 'CML3111'); }
function show_W3_CML3111() { showScores(3, 'CML3111'); }
function show_W4_CML3111() { showScores(4, 'CML3111'); }
function show_W5_CML3111() { showScores(5, 'CML3111'); }
function show_W6_CML3111() { showScores(6, 'CML3111'); }
function show_W8_CML3111() { showScores(8, 'CML3111'); }
function show_W9_CML3111() { showScores(9, 'CML3111'); }
function show_W10_CML3111() { showScores(10, 'CML3111'); }
function show_W11_CML3111() { showScores(11, 'CML3111'); }
function show_W12_CML3111() { showScores(12, 'CML3111'); }
function show_W13_CML3111() { showScores(13, 'CML3111'); }
