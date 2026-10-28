"""Canonical course paths. No dated-folder assumptions."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
MAINTENANCE = ROOT / '05 Course Maintenance'
SOURCE = Path(__file__).resolve().parent
PRACTICE = ROOT / '03 Learner Materials' / 'Practice Files'
TEACHING_RESOURCES = ROOT / '04 Facilitator Materials' / 'Teaching Resources'
DOCUMENTS = {
 'Course_Overview.docx': ROOT / '01 Course Overview' / 'Course Overview.docx',
 'Applied_AI_Learner_Workbook.docx': ROOT / '03 Learner Materials' / 'Learner Workbook.docx',
 'Applied_AI_Facilitator_Guide.docx': ROOT / '04 Facilitator Materials' / 'Facilitator Guide.docx',
 'Law_Firm_AI_Implementation_Playbook.docx': ROOT / '04 Facilitator Materials' / 'Law Firm Implementation Playbook.docx',
}
