"""Generate the guide for the existing, audited weekly quiz deployment."""
from pathlib import Path
from docxkit import *
ROOT=Path(__file__).resolve().parents[1]
d=new_doc(margin_cm=2.2)
header_footer(d,'IUEA · Weekly quiz operations · Lecturer only · September 2026')
h1(d,'Weekly quiz operations')
para(d,'Use the existing forms and preserve earned marks',size=15,colour=MID)
para(d,'The deployment contains 36 quizzes: twelve teaching weeks for each of CML3111, CML3112 and CML3113. Each quiz has five scored multiple-choice questions worth one mark each. Existing Week 1 responses and earned marks must be preserved.')
h2(d,'1. Identity and student experience')
para(d,'Each form collects verified Google-account email and a required Student Registration Number. Students enter the full number from their university record, fictional example 99/TEST/000/DEMO-X. It is not a phone number. The roster must map that number to the correct cohort and verified-account email; a typed identifier does not remove the need for a roster.')
para(d,'The form limits responses by signed-in account. This is an account control, not proof that a learner has only one account; roster matching remains essential. The registration field is unscored. Only the five one-point multiple-choice items contribute to the quiz mark.')
para(d,'The audited settings release scores immediately after submission, show point values and missed-question feedback, and hide correct-answer display. Students use View score after submitting. Google may show a cosmetic Final score pending label for the unscored registration field; the importer excludes that field from arithmetic.')
h2(d,'2. Locate the existing quiz')
para(d,'Use data/quiz_links.json and the existing quiz Apps Script project recorded in the review evidence. The generated script is grader/create_quiz_forms.gs. Do not rebuild forms as a routine weekly action: rebuilding changes links and risks losing the connection to existing responses.')
para(d,'The audited Week 2 feedback repair changes feedback only. Keep options, answer keys and earned marks stable for assessments already taken. A future content correction must be checked against the local bank and recorded before that quiz is opened.')
h2(d,'Before class')
para(d,'Confirm the correct week and cohort, read all five questions and explanations, check the actual roster, and preview the student link. Confirm the form is still a quiz with verified email, one response per account and immediate score release. Prepare the projected five-minute classroom timer and the QR/link fallback.')
page_break(d)
h1(d,'Open, close and import')
h2(d,'3. Opening starts the shared 24-hour window')
para(d,'Exception for CML3112 Week 1: the catch-up quiz was activated 15 September at 06:31:20 and closes 16 September at 06:31:20 Kampala. Its assignment upload stays open until 22 September at 11:00. Do not run open_W1_CML3112. The catch-up timer is managed in the assignment project. Use IUEA_ML_Quick_Class_Checklist.docx for clickable project links and the short activation steps.')
para(d,'In the existing Apps Script project select the matching wrapper and run it once. Week 2 wrappers are open_W2_CML3112, open_W2_CML3113 and open_W2_CML3111. The wrapper calls openQuizFor with the week and cohort, publishes the existing form, records the opening and closing times, and schedules closure.')
para(d,'The five-minute classroom timer is a teaching target. The form stays available for a shared 24-hour window; it is not a five-minute timer for each student. Tell students the actual closing date and time in Africa/Kampala (UTC+03:00). Retain the recorded closeAt value for grade import.')
para(d,'Do not rerun the opening wrapper just to inspect status: it starts a fresh 24-hour window. Use closeStatus() to inspect pending closure instead. If an extension is needed, record the reason and revised deadline explicitly; do not silently accept late marks.')
h2(d,'4. After expiry')
para(d,'Check closeStatus() and the respondent link. A time trigger may run after the exact deadline. Eligibility uses the server-recorded response timestamp and the configured closing time, so a response arriving after expiry does not become eligible merely because the page still accepted it.')
para(d,'auditForm(2, "CML3112") inspects a selected form, while auditAll() inspects the set. Functions with arguments need a small wrapper when run through the Apps Script Run menu. showScores(2, "CML3112") is a private diagnostic of the stored response marks; its output contains assessment records and should not be projected.')
h2(d,'5. Import the authoritative marks')
para(d,'Use the bound gradebook.gs in the intended production gradebook. Fill the real roster first: student_id stores the full Student Registration Number, with name, cohort and email in their required columns. The private synthetic QA gradebook is not the production class record.')
para(d,'configureQuizImports(sourcesJson) accepts a JSON object keyed by cohort|teachingWeek. Each value must contain the existing formId and an explicit ISO closing timestamp. Supply the actual recorded deadline, including the +03:00 offset. Configuration replaces the source map, so retain every source intended for that import.')
para(d,'Then run importQuizScores(). It checks registration number, cohort, verified email, exactly five one-point scored items and the deadline before writing. Quiz teaching weeks are 1–6 and 8–13; the gradebook maps them to Q1–Q12 and applies best ten of twelve. Existing Week 1 marks are protected. Unknown identities or invalid scores stop the import instead of guessing a match.')
page_break(d)
h1(d,'Troubleshooting and continuity')
table(d,['Observation','Action'],[
 ['Student cannot access the form','Check the correct cohort link, signed-in Google account, publishing state and current window. Rehearse with a non-owner account before relying on a changed setup.'],
 ['Student cannot see a total','Ask the student to use View score. Privately check showScores and the immediate-release setting. Do not type a manual total merely because an unscored field displays pending.'],
 ['Registration number or email mismatch','Compare with the actual roster and original response. Correct a documented roster mistake or resolve the respondent’s identity; do not match by row order or guess from a name.'],
 ['Submission appears after closing','Use its server timestamp against the recorded deadline. A delayed closure trigger does not extend eligibility. An authorized outage extension must be recorded explicitly.'],
 ['Import reports an ungraded item','Check the quiz item type, point value and stored mark. The importer intentionally rejects missing or invalid scored answers. Keep the grade pending until the configuration or evidence issue is resolved.'],
 ['Question is found to be defective','Preserve original responses and marks. Record the defect and apply a consistent Faculty-approved remedy; do not silently edit the answer key after learners have taken it.']],[30,70],font=10)
h2(d,'Keep the two assessment routes distinct')
para(d,'Weekly quizzes use the existing quiz project and immediate Google Forms scoring. Notebook, DOCX/PDF and presentation assignments use the separate submission project, upload readiness checks, a release gate and local grading after download. Opening a weekly quiz does not release an assignment.')
h2(d,'Block quiz sittings from Week 8')
para(d,'From Week 8 the weekly quiz is replaced by one sitting after every three classes. Block 1 uses the Q7, Q8 and Q9 forms (Weeks 8 to 10) and Block 2 uses Q10, Q11 and Q12 (Weeks 11 to 13). The forms, answer keys and gradebook columns are unchanged. Each form is worth 5 marks, so a block quiz is out of 15.')
para(d,'In the last twenty minutes of the Week 10 or Week 13 class, run open_Block1_CML31xx or open_Block2_CML31xx from grader/block_quiz_sittings_20261030.gs. It opens the three forms together; each stays open for 24 hours from activation. Show one QR code per form, or share the three links.')
para(d,'Run applyBlockWindows() from grader/apply_block_windows_20261030.gs once, in the submission project, to move the A7 to A11 closing times to the block deadlines in data/assessments.json.')
para(d,'Gradebook: Weeks 1 to 5 keep the best 3 of 5, because Week 6 is waived for all three cohorts. The two blocks are never dropped. Quizzes are out of 45 marks and assignments out of 160. The Week 13 form (Q12) was rewritten for ridge, nearest neighbours and reproducibility; change the live forms with replaceWeek13Questions() in create_quiz_forms.gs, not with rebuildAllForms().')
h2(d,'What has and has not been rehearsed')
para(d,'The owner-account rehearsal displayed 5/5, imported by registration number and verified email, and preserved control and Week 1 marks. All 36 quiz settings were audited. The separate student-account rehearsal also passed: upload, replacement, timed closure, immediate quiz score and local assignment grading. The actual production roster is still required; this does not prove every institutional account can access the form.')
para(d,'Keep response exports, score diagnostics and the gradebook private. Feedback shown to a student should concern their own work. Do not publish a class-wide response sheet or share lecturer answer keys with the student deck.')
para(d,'Generated from scripts/build_quizops_docx.py. Operational source: grader/create_quiz_forms.gs and grader/gradebook.gs. Dated evidence: review/2026-09-14/REWORK_STATUS.md.',size=9,italic=True)
d.save(ROOT/'IUEA_Teaching_Plan/IUEA_ML_Weekly_Quiz_Operations_Guide.docx')
