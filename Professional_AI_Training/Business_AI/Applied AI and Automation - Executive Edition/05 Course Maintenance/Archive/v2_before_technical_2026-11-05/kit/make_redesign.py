import subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
BUILD = HERE.parent
EDITION = BUILD.parent.parent
sys.path.insert(0, str(BUILD / 'templates_gen'))
from docx_kit import *  # noqa

def bullets(d, items, size=10, after=2):
    for it in items:
        p = para(d, '', size, after=after)
        p.paragraph_format.left_indent = Cm(0.5); p.paragraph_format.first_line_indent = Cm(-0.4)
        add_run(p, '•  ', size, True)
        if isinstance(it, tuple):
            add_run(p, it[0] + ' ', size, True); add_run(p, it[1], size)
        else:
            add_run(p, it, size)

d = new_doc('Course map for approval', 'Applied AI and Automation, Executive Edition')
title(d, 'Course map for approval: scenarios, two demonstrated automations, four practicals', '4 November 2026  |  still 12 sessions and 24 hours')
h2(d, 'What you asked for', 0)
para(d, 'Keep the use cases and scenarios. Show only two automations across the whole course, one rule-based and one using AI, both on the same customer messages. Keep the hands-on work for four things: finding the right workflow, the AI use policy, the organisation data readiness assessment, and the data roadmap. The Zapier and Apps Script builds are no longer learner builds.', 10, after=4)
h2(d, 'The two demonstrated automations')
bullets(d, [('Rule-based (Session 6).', 'Customer messages are routed by plain rules in a spreadsheet and shown in a no-code automation tool. Exact, fast, cannot read meaning. Same twelve messages as Session 1.'),
            ('AI-based (Session 8).', 'The same messages are sorted by an AI assistant, a reply is drafted, and a person approves it. Time and accuracy are measured against the Session 1 baseline and the rule. The results are recorded in advance, so nobody switches tools in class.')], 10)
h2(d, 'The twelve sessions')
rows = [['1', 'Where AI fits in your business', 'PRACTICAL: workflow identification', 'Scorecard and task card. The rule, person and AI results are shown on the slides.'],
        ['2', 'How AI works and where it fails', 'Scenarios', 'Five failure cases with the results shown: made-up facts, sarcasm, bias, injected instructions, drift.'],
        ['3', 'Working with AI tools', 'Scenarios', 'Good and weak briefs side by side with results shown. A reusable brief template to take home.'],
        ['4', 'Your information: is your data ready?', 'PRACTICAL: data readiness assessment', 'Inventory and readiness scorecard from Session 0, applied to your own company.'],
        ['5', 'Reviewing documents with AI', 'Scenarios', 'Contract and CV review cases, what the AI found, what it missed, how a person checks.'],
        ['6', 'Automation 1: a rule-based workflow', 'DEMONSTRATION', 'Customer messages routed by rules. What rules do well and where they stop.'],
        ['7', 'Agents and controlled actions', 'Scenarios', 'What an agent is, what permissions it needs, where a person must approve.'],
        ['8', 'Automation 2: an AI workflow', 'DEMONSTRATION', 'The same messages with AI and a human check. The measured comparison.'],
        ['9', 'Your AI use policy', 'PRACTICAL: AI use policy', 'Write the policy from the template, with the risk register and the law (hedged, check with your lawyer).'],
        ['10', 'Buying and oversight', 'Scenarios', 'Vendor claims taken apart. A question list to keep.'],
        ['11', 'The business case', 'Worked example', 'Costs, savings and the baseline from Session 1, shown on the case company. A template to take home.'],
        ['12', 'Your data roadmap and 90-day plan', 'PRACTICAL: data roadmap', 'Turn the Session 4 assessment into a roadmap, with owners and dates. Share in pairs.']]
grid(d, rows, [0.9, 4.6, 3.8, 8.1], header=['#', 'Session', 'Type', 'What happens'], size=8.5, label_cols=(0,))
h2(d, 'What changes in the materials')
bullets(d, ['Sessions 6 and 8 become demonstrations. The Zapier and Apps Script build guides and code move to an optional appendix folder and are kept, not deleted.',
            'Sessions 2, 3, 5, 7, 10 and 11 become scenario sessions with results shown on the slides. Fewer learner steps, more discussion.',
            'Session 4, 9 and 12 become the main practicals. The templates for the use-case scorecard, task card, information inventory, AI use policy, risk register and 90-day roadmap stay. The Zapier test log, the Apps Script files and the automation test log are optional.',
            'The Course Handbook, Course Overview, Learner Workbook and Start Here need rewriting. Learners already hold the first handbook, which says they build with Zapier and Apps Script, so I would send them the updated version.',
            'No learner needs a Zapier trial, so the trial advice is removed from the preparation message and from Session 0.',
            'Flyer line for the course: now "Identify and automate a repetitive workflow in your job". I suggest "Decide where AI fits, write your AI policy and get your data ready."'], 10)
h2(d, 'Order of work if you approve')
para(d, 'Session 1 (done) and Session 0 (done). Then Sessions 4, 9 and 12, the practicals. Then 6 and 8, the demonstrations, with the measured results. Then the scenario sessions. Then the handbook, overview, workbook, guides and flyer line. I check each deck with a fresh reader before it is final.', 10, after=4)
h2(d, 'Please confirm')
bullets(d, ['The session map above, or tell me which session types to change.', 'That Session 11 (business case) stays as a worked example.', 'The suggested flyer line.'], 10)
save(d, EDITION / '01 Course Overview' / 'Course Map for Approval (4 Nov 2026).docx')
subprocess.run(['soffice', '-env:UserInstallation=file:///tmp/lo_rd', '--headless', '--convert-to', 'pdf', '--outdir', str(EDITION / '01 Course Overview'), str(EDITION / '01 Course Overview' / 'Course Map for Approval (4 Nov 2026).docx')], capture_output=True, timeout=200)
