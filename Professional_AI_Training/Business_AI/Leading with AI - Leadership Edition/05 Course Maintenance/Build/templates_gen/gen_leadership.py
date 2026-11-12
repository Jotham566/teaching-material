"""Leadership Edition templates (12 November 2026): AI Opportunity Portfolio.xlsx and People and Skills Plan.docx.
Run from templates_gen/: python3 gen_leadership.py"""
from xlsx_kit import *  # noqa
import docx_kit as DK

JOBS = ['See and read', 'Predict', 'Understand language', 'Write (generative)', 'Act (agent)']
NVF_NOTE = 'Grey italic rows are examples from the fictional company Nile Valley Foods Ltd (NVF). Type your own entries in the rows below them.'
N = 20


def portfolio():
    wb = new_wb('AI Opportunity Portfolio')
    # 1 entries
    ws = wb.active; ws.title = 'Entries'
    H = ['#', 'Added in session', 'The use', 'What goes in', 'What comes out', 'Who uses it', 'How we would know it works', 'AI job', 'Session note']
    setup(ws, 'AI Opportunity Portfolio: step 1, your candidate uses',
          'Add one or two entries in each session from 1 to 10, using that session\'s idea. One row per use in your own organisation. '
          'The AI job is one of the five jobs from Session 0 (see and read, predict, understand language, write, act). Session note: the column the session asks for, '
          'for example the kind of prediction (Session 2), the cost of a mistake (Session 3) or the route: rent, host or build (Session 6). ' + NVF_NOTE,
          H, [5, 10, 34, 26, 26, 20, 30, 18, 30], 34)
    style_row(ws, 4, 9, True, (1, 2))
    fill_values(ws, 4, ['Ex', 2, 'Rank shops by risk of ordering less next month', 'Two years of orders for each shop', 'A ranked list every Monday',
                        'Area sales reps', 'Of the 20 shops ranked top, how many ordered less', 'Predict', 'A ranking'])
    for r in range(5, 5 + N):
        style_row(ws, r, 9, False, (1, 2)); ws.cell(r, 1).value = r - 4
    add_whole(ws, f'B4:B{4 + N}', 0, 14, 'The session number, 0 to 14.')
    add_list(ws, f'H4:H{4 + N}', JOBS)
    # 2 score (Session 11)
    ws2 = wb.create_sheet('Score')
    H2 = ['#', 'The use (from Entries)', 'Value 1-5', 'Feasibility 1-5', 'Priority (value plus feasibility)', 'Rank', 'Why this value']
    setup(ws2, 'AI Opportunity Portfolio: step 2, value and feasibility (Session 11)',
          'Value: 5 = saves a lot of time or money, or matters a lot to customers. Feasibility: 5 = the data exists, the task is easy to check and a team can start now. '
          'Priority adds the two (the most is 10). Start with the highest priority that is also cheap to get wrong.',
          H2, [5, 40, 11, 13, 16, 8, 40], 40)
    for r in range(4, 5 + N):
        style_row(ws2, r, 7, r == 4, (3, 4, 5, 6))
        ws2.cell(r, 1).value = 'Ex' if r == 4 else r - 4
        ws2.cell(r, 2).value = f'=IF(Entries!C{r}="","",Entries!C{r})'
        ws2.cell(r, 5).value = f'=IF(OR(C{r}="",D{r}=""),"",C{r}+D{r})'
        ws2.cell(r, 6).value = '-' if r == 4 else f'=IF(E{r}="","",RANK(E{r},$E$5:$E${4 + N}))'
    fill_values(ws2, 4, [None, None, 4, 4], 1)
    ws2.cell(4, 7).value = 'Fewer lost orders; reps already visit these shops'
    add_whole(ws2, f'C4:D{4 + N}', 1, 5, 'A whole number from 1 to 5.')
    cf_gold(ws2, f'B5:B{4 + N}', f'AND(ISNUMBER($E5),$E5>=8)')
    # 3 people, risk, data (Sessions 12 to 14)
    ws3 = wb.create_sheet('People, risk, data')
    H3 = ['#', 'The use (from Entries)', 'Roles it touches (Session 12)', 'Tasks that change', 'Likelihood 1-5 (Session 13)', 'Impact 1-5', 'Risk score (likelihood times impact)',
          'Data ready? (Session 14)', 'Decision for the next 90 days', 'Owner']
    setup(ws3, 'AI Opportunity Portfolio: step 3, people, risk and data (Sessions 12 to 14)',
          'For each use: who it touches and how their work changes; the worst realistic risk scored for likelihood and impact (15 or more is High); whether the data is ready '
          '(Green, Amber or Red, as in Session 14); then the decision: Start now, Prepare first, Later or Drop, with one named owner.',
          H3, [5, 34, 22, 26, 13, 10, 14, 13, 18, 20], 46)
    for r in range(4, 5 + N):
        style_row(ws3, r, 10, r == 4, (5, 6, 7, 8, 9))
        ws3.cell(r, 1).value = 'Ex' if r == 4 else r - 4
        ws3.cell(r, 2).value = f'=IF(Entries!C{r}="","",Entries!C{r})'
        ws3.cell(r, 7).value = f'=IF(OR(E{r}="",F{r}=""),"",E{r}*F{r})'
    fill_values(ws3, 4, [None, None, 'Area sales reps, sales manager', 'Reps plan visits from the list', 3, 2, None, 'Amber', 'Prepare first', 'Peter Okello (fictional)'])
    add_whole(ws3, f'E4:F{4 + N}', 1, 5, 'A whole number from 1 to 5.')
    add_list(ws3, f'H4:H{4 + N}', ['Green', 'Amber', 'Red'])
    add_list(ws3, f'I4:I{4 + N}', ['Start now', 'Prepare first', 'Later', 'Drop'])
    cf_red(ws3, f'G4:G{4 + N}', 'AND(ISNUMBER($G4),$G4>=15)')
    save(wb, TEMPLATES / 'AI Opportunity Portfolio.xlsx')


def people_plan():
    d = DK.new_doc('People and Skills Plan')
    DK.title(d, 'People and Skills Plan', 'Session 12. One plan for the first AI use you will start: whose work changes, the skills they need, how you tell them, and who champions it.')
    DK.box(d, 'How to use this plan', [
        'Fill it for the use you rank first in your AI Opportunity Portfolio. Work task by task: tasks change before jobs do.',
        'Grey italic text is an example from the fictional company Nile Valley Foods Ltd (NVF), a customer-message assistant. Type over it.'], size=8.5)
    DK.grid(d, [['AI use', '~Sort and draft replies to customer messages', 'Sponsor', '~Sarah Namukasa, Managing Director'],
                ['Plan owner', '~David Kato, Customer Service Lead', 'Date', '~1 February 2027']],
            [3.0, 7.4, 2.4, 4.6], label_cols=(0, 2), min_h=0.9)
    DK.spacer(d, 2)
    DK.h2(d, '1. The role, task by task', before=2, after=1)
    DK.grid(d, [['~Read and sort each message', '~AI sorts; the officer checks doubtful ones', '~Less', '~Checking the AI\'s doubtful cases'],
                ['~Draft a reply', '~AI drafts; the officer edits and sends', '~Less', '~Editing, tone, knowing the policy'],
                ['~Handle angry or unusual customers', '~Person only', '~More', '~Judgement, calm, authority to settle'],
                ['', '', '', '']],
            [4.6, 4.8, 2.0, 6.0], header=['Task today', 'With AI', 'Time on it', 'Skill it needs'], min_h=0.8, size=9)
    DK.spacer(d, 2)
    DK.h2(d, '2. Skills by level', before=2, after=1)
    DK.grid(d, [['Everyone', '~What the tool may and may not do; the use policy; how to report an error'],
                ['Power users', '~Writing and testing briefs; checking outputs against the source'],
                ['Builders', '~Setting up the tool, its permissions and the log (IT or the vendor)'],
                ['Leaders', '~Reading the monthly results; deciding to widen, pause or stop']],
            [3.4, 14.0], header=['Who', 'What they learn, and how'], min_h=0.8, size=9)
    DK.spacer(d, 2)
    DK.h2(d, '3. Fears and answers', before=2, after=1)
    DK.grid(d, [['~Will I lose my job?', '~No role is cut in this pilot. Time saved goes to the backlog of callbacks. We review in 90 days with you.'],
                ['~Will I be blamed for the AI\'s mistakes?', '~The officer who sends owns the reply; the AI only drafts. Reporting an AI error is praised.'],
                ['~Is my work being watched?', '~The log records the tool, not your speed. We do not use it to rate people.']],
            [5.4, 12.0], header=['What people fear', 'What we say and do'], min_h=0.8, size=9)
    DK.spacer(d, 2)
    DK.h2(d, '4. Communication and champions', before=2, after=1)
    DK.grid(d, [['Why we are doing this (one sentence)', '~Customers wait too long; the assistant drafts so you can answer faster and better.'],
                ['What is approved, and what is not', '~Approved: the company assistant for sorting and drafts. Not approved: pasting customer data into personal AI tools.'],
                ['Champions (names)', '~Two officers who tried it first, one per shift'],
                ['How people give feedback', '~A weekly 15-minute review and a shared error log'],
                ['Check-ins', '~Day 30, 60 and 90, with the Follow-up Kit']],
            [5.4, 12.0], min_h=0.8, size=9)
    DK.spacer(d, 2)
    DK.signoff(d, ['Plan owner (name and signature)', 'Sponsor (name and signature)', 'Date'], [6.4, 6.4, 4.6], height=1.0)
    DK.save(d, TEMPLATES / 'People and Skills Plan.docx')


if __name__ == '__main__':
    portfolio(); people_plan()
