"""Generate the operational architecture for the implemented local grader."""
from pathlib import Path
from docxkit import *
ROOT=Path(__file__).resolve().parents[1]
d=new_doc(margin_cm=2.2)
header_footer(d,'IUEA · Assessment architecture · Lecturer only · September 2026')
h1(d,'Assessment architecture')
para(d,'Collection, automatic assessment and private grade import',size=15,colour=MID)
para(d,'This describes the implemented system. Current passing calibrations and remaining release requirements are recorded in review/2026-09-14/REWORK_STATUS.md. A form existing, or a model being installed, does not make an assessment ready.')
h2(d,'1. The complete submission path')
table(d,['Stage','What happens'],[
 ['Student work','Students use the issued Colab notebook or documented offline setup. Visible practice checks give feedback. Students submit the actual notebook and required report or slides.'],
 ['Timed collection','Lecturer-owned Google Forms collect verified email, Student Registration Number and attachments. Shared opening and closing timestamps govern eligibility. The latest on-time response replaces the complete previous packet.'],
 ['Local preparation','prepare_submissions.py matches registration number, cohort and verified email to the roster. It retains the audit trail, prepares eligible packets and reports missing submissions only for the assigned cohort.'],
 ['Executed checks','Notebook and SQL work runs in restricted Docker containers without network access. Hidden checks remain separate from student execution. Time and resource limits prevent a single packet from occupying the batch indefinitely.'],
 ['Local reasoning','Ollama runs on this Mac at loopback only, with cloud features disabled. A current passing known-answer calibration is required for each rubric, model and evaluator.'],
 ['Private results','The combined workflow writes results, individual feedback and import-ready files. Import validates identities and marks before writing. Unresolved results remain blank.']],[25,75],font=10)
h2(d,'Practice feedback is not a final mark')
para(d,'A practice receipt or signed token is diagnostic only. Its key is available to students, so the receipt is not trusted as a mark. Final numerical marks come from the independently executed submission. Do not import practice scores, manually copy row-ordered marks, or substitute a sampled batch for the complete eligible set.')
page_break(d)
h1(d,'Evidence and release')
h2(d,'2. How reasoning marks are controlled')
para(d,'The grader extracts accessible text from supported DOCX, PDF and PPTX files in an isolated document container. For supported notebooks it reads only the designated student-written evidence cells. Prompts, starter answers and code comments do not supply explanation marks.')
para(d,'Two evaluations must agree within the configured criterion tolerance. Positive marks require an exact excerpt from the submitted text. Invalid output, stale calibration or disagreement produces an exception with no final mark. Agreement alone is not a calibrated confidence probability or proof of correctness.')
para(d,'Calibration is bound to the rubric, evaluator, source evidence, installed model digest and Ollama version. Keep failed reports as evidence. Do not lower authored expected marks just to make a model pass. Recheck after changes that invalidate those bindings.')
h2(d,'3. Release and upload readiness are separate')
para(d,'The live assignment system has 52 forms. Upload folders and verified email settings were checked. A separate release gate keeps draft assessments closed even during a scheduled window. Release requires checked student tasks, numerical reference checks, the current reasoning calibration where needed, and a complete-packet rehearsal.')
para(d,'Week 2 has a verified whole-packet route: 14 executed marks plus 6 explanation marks. Later assessment coverage is reported individually in the status file. S13 currently has a 40/100 numerical component; S15 has a 20/100 reported-value component. Partial components are not final grades. The four independent-track dates remain unset.')
para(d,'Text extraction cannot establish chart layout, an interactive Power BI filter, spoken delivery or repository history. These require their own verified evidence route. Major-project, exam and presentation criteria remain held where that route or calibration is incomplete.')
h2(d,'4. Submission limits and exceptions')
para(d,'The live upload template accepts up to ten files, each up to 10 MB. The assignment brief narrows the required formats and number of artifacts. Use accessible, selectable-text reports; image-only reports cannot be assessed through text extraction. The local parser also rejects unsupported formats, excessive text and oversized packets rather than silently truncating them.')
para(d,'Keep every required attachment in the same response when resubmitting. A missing attachment leaves that learner pending while other complete packets proceed. Missing submissions, identity mismatches and technical failures are not automatically converted to zero. Resolve the underlying evidence or documented submission issue before a final mark is imported.')
page_break(d)
h1(d,'Running and maintaining the system')
h2(d,'5. The lecturer workstation')
para(d,'Use the pinned Python 3.12 environment .iuea-grader-env and the Docker images described in grader/README.md. The old Python 3.9 environment is retained. Start the local model with grader/start_local_model.command; it checks whether the service is already running.')
para(d,'Run model inference serially on this 8 GB Mac. Queue work after teaching and retain resumable results. Model inference can take minutes per submission; the old notebook-only benchmark is not a forecast for reasoning or document grading. Verify free disk space, Docker readiness and model health before a batch.')
para(d,'Use assessment_readiness.py to inspect calibration coverage, then grade_assessment.py for a supported complete notebook packet. S05 uses da_sql_grade.py. The exact commands, flags and import workflow live in grader/README.md so operational instructions have one maintained source.')
h2(d,'6. Records and identity')
para(d,'The official IUEA label is Student Registration Number. Store the full value, using a fictional illustration 99/TEST/000/DEMO-X, in the roster and STUDENT_ID. Replace slashes with underscores only in filenames. Internal CSV headers retain student_id for compatibility. Do not infer a programme from the registration suffix.')
para(d,'Use the actual registration number, name, cohort and verified-account email roster before production import. The independent track uses its own DA learner IDs and separate 15/15/30/40 aggregation. Existing Week 1 earned marks remain protected. Faculty letter bands are withheld until the approved policy is supplied.')
para(d,'Google Forms attachments are stored in the lecturer’s Google Drive before download. Only AI inference stays local. Keep lecturer guides, answer keys, hidden checks, rosters, model evidence excerpts and grade exports in restricted records locations. Distribute only intended student-facing materials. Feedback is generated privately; it is not automatically emailed or published.')
h2(d,'7. Recovery and final rehearsal')
para(d,'Retain original uploads and the response audit. Correct an input or configuration problem and rerun the affected packet; never alter a student answer to make it grade. An outage extension must be explicit and recorded, with an equivalent opportunity for affected students. A non-owner student-account rehearsal, production roster, actual DA dates and Faculty policy remain operational inputs.')
para(d,'Generated from scripts/build_platform_docx.py. See REWORK_STATUS.md for dated evidence and unresolved work.',size=9,italic=True)
d.save(ROOT/'IUEA_Teaching_Plan/IUEA_ML_Platform_Architecture_Note.docx')
