# Practical AI and Automation for Finance

## Files to share

- [Course roadmap PDF](output/client/Practical_AI_for_Finance_Roadmap.pdf) — two pages, with the online assessment link and QR code.
- [Editable roadmap](output/client/Practical_AI_for_Finance_Roadmap.docx).
- [Offline needs assessment](output/client/Finance_Training_Needs_Assessment.docx) — an alternative to the Google Form.
- [Management discussion proposal](output/proposals/BIK_Capital_MD_Discussion_Proposal.docx) — for the separate organisation-wide training discussion.

The [facilitator guide](output/internal/Finance_AI_Facilitator_Guide.docx) is for teaching preparation. It includes exercises, expected answers, assessment and follow-up notes; it is not part of the client handout.

## Online assessment

- Respondent link: https://forms.gle/FGdVz8Eswpc1nvRD8
- Account: jothammartin.wambi@gmail.com
- [Form metadata](forms/assessment_form.json) records the respondent and editor URLs. The editor still requires the owner's Google permissions.
- [QR code](assets/finance_needs_assessment_qr.png) points to the respondent link.

The live form has 16 questions. Session duration and attendance format are separate questions online and combined in the offline questionnaire. Responses are held in Google Forms and are not stored in this repository.

## Directory layout

```text
output/client/       Current learner documents
output/proposals/    Organisation proposal
output/internal/     Teaching notes
source/              Document builders
assets/              QR image used by the roadmap
forms/               Form URLs and ownership metadata
archive/             Superseded files retained for reference
.qa/                 Local render checks, ignored by Git
.local/              Local dependencies, ignored by Git
```

## Editing and rebuilding

Edit the text in `source/build_roadmap.py` for the roadmap and `source/build_documents.py` for the other documents. Both require Python 3.11+ and `python-docx` from the repository requirements. Run from any directory:

```sh
python source/build_roadmap.py
python source/build_documents.py
```

The second command also rebuilds the roadmap. Render and inspect every changed document before sharing. Re-export the roadmap PDF after editing the DOCX; the builder does not update the PDF automatically. Keep QR images square and verify the link after changing it. Creating a new form requires updating the QR image, form metadata and link in the roadmap source together.

Archived files are not current course offers. Personal tuition and any future company engagement are separate.
