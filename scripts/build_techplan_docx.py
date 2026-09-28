"""Rebuild the assessment operations plan from the implemented architecture."""
from pathlib import Path
from build_week2_docs import document
ROOT=Path(__file__).resolve().parents[1]
d=document('Assessment operations plan')
d.add_paragraph('IUEA engineering and independent Data Analyst track | 14 September 2026')
PAGES=[
 ('1. Assessment architecture',[
 ('Objective','One lecturer should not have to read every submission manually. Code and numerical answers use deterministic checks. Reasoning in accessible reports and slide notes uses a local, calibrated rubric model. The two teaching tracks keep separate grade records.'),
 ('Authoritative notebook marks','batch_grade.py executes every submitted notebook in a restricted Docker container. The trusted parent process retains hidden tests and computes marks. The container has no network, a read-only system, limited temporary storage, an unprivileged user, memory/process limits and a hard timeout. Student practice tokens are receipts only.'),
 ('Current deterministic coverage','W02: 14 points for identity and fresh-run outputs, plus a 6-point local reasoning rubric. W03: five engineering tasks, 20 points. W04: four cohort CSV summaries, 20 points. W05: six pandas tasks, 20 points. DA Session 5: rep/month keys, gross, returns and net amounts, 100 points.'),
 ('Reasoning coverage and limits','artifact_grade.py reads DOCX, selectable-text PDF and PPTX text/notes. It groups files from one response, quotes supporting evidence and retains two rubric passes. It rejects out-of-range marks, fabricated quotes and unresolved disagreement. Reading source code does not prove execution correctness. Images, spoken delivery and interactive dashboard behaviour need separate evidence and are not verified by this text pipeline.')]),
 ('2. Submission and timed expiry',[
 ('Create the upload template','The Google account owner creates one private Form with exactly one required file-upload question, multiple files enabled, up to 10 attachments and 10 MB per file. File uploads require Google sign-in. Apps Script cannot create this question type, so the template is copied.'),
 ('Create the assignment forms','Paste grader/submission_forms.gs into a standalone Apps Script project. Authorize its Forms, Drive, Sheets and trigger access, configure the template ID, then run buildSubmissionForms until all 52 entries are ready. Existing quiz responses and Week 1 marks remain intact. Newly created forms start closed.'),
 ('Schedule and deadline rule','The registry stores cohort windows in Kampala time. Friday Week 5 follows the recorded-session plan. DA windows remain unset until actual dates are supplied. One five-minute trigger opens/closes scheduled forms. The server response timestamp determines eligibility even if closure runs late. This is a shared deadline, not an individual countdown.'),
 ('Selection and export','syncSubmissions records identity, timestamp, deadline, status and original file IDs. exportSubmissionFiles creates a private folder for download. prepare_submissions.py checks the roster and selects the latest on-time response as a whole. It rejects unknown IDs, email/cohort mismatches and ambiguous files. Keep originals and the audit CSV.')]),
 ('3. Local grading and mark import',[
 ('Local model','Use Ollama on 127.0.0.1:11434 with OLLAMA_NO_CLOUD=1. The candidate model is qwen3:4b for this 8 GB Mac. A running service, downloaded weights and passed calibration are separate readiness checks. Student work is never sent to a cloud grading provider.'),
 ('Calibration before live marks','Test known strong, weak, incorrect and instruction-injection examples against each rubric family. Two agreeing model passes are not calibrated confidence. Verify that marks reflect the substantive answer and that unsupported evidence produces zero or an exception. Record model and rubric versions.'),
 ('Batch operation','Run notebook grading for the whole selected cohort. W02 merges its deterministic results with the 6-point local rubric into one mark out of 20. The artifact grader caches successful results only when the files, rubric, model and code component match. Exceptions retain blank scores and actionable feedback.'),
 ('Gradebook import','Use Grades_template.csv and the bound gradebook.gs. importMarkedResults imports by student registration number and validates all rows before writing. Week 1 existing marks are protected. Quiz imports use Google Forms scores and explicit closing times. Letter bands remain disabled until verified against Faculty rules. Team components expand using registered membership; individual reflection stays individual.')]),
 ('4. Release checks and workload',[
 ('Before Week 2','Use the cohort student ZIP, concise setup guide and lecturer runsheet. Rehearse Colab CSV upload, GitHub save, README upload and the prepared lab fallback. Test Forms from a non-owner student account, including two attachments, a replacement response and expiry. The operational checklist is in grader/README.md.'),
 ('Before later assessments','Finalize each practical exam task and its deterministic checks before release. A generic rubric is not an exam answer key. Match every published task, dataset, named output and mark to its checker. Require accessible report exports and narration notes where the local text grader needs them.'),
 ('Failure handling','Never turn a failed extraction, timeout or infrastructure error into an invented zero. Resolve format/access problems through documented resubmission or an explicit deadline extension. Retain the original server timestamp and record the decision. Substantive model disagreement needs calibration or an objective assessment redesign.'),
 ('Measure the actual workload','Earlier fixed claims about hours saved were estimates. Measure batch duration, exception rates, resubmission handling and model calibration on representative work. The aim is automated routine assessment with targeted exception handling. See review/2026-09-14 for test evidence and the current deployment status.')]),
]
for index,(title,sections) in enumerate(PAGES):
 if index:d.add_page_break()
 d.add_paragraph(title,'Heading 1')
 for heading,text in sections:
  d.add_paragraph(heading,'Heading 2');d.add_paragraph(text)
out=ROOT/'IUEA_Teaching_Plan/IUEA_ML_Assessment_Technology_Build_Plan.docx'
d.save(out);print('saved',out)
