"""Excel templates, part 2: vendor list, business case, roadmap, results tracker."""
import datetime
from xlsx_kit import *
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.chart.shapes import GraphicalProperties

NVF_NOTE = 'Grey italic entries are examples from the fictional company Nile Valley Foods Ltd (NVF): type your own over them.'

GROUPS = ['Data and privacy', 'Security', 'Accuracy evidence', 'Pricing drivers', 'Contract and exit', 'Support and references']
QUESTIONS = [
    ('Data and privacy', 'Where is our data stored and processed, and in which countries?', 'Personal data that leaves Uganda can carry legal duties. You need to know where it goes.', 'Anywhere we choose. No list of countries. Will not name sub-processors.'),
    ('Data and privacy', 'Do you use our data to train or improve your models or anyone else\'s?', 'Your contracts, prices and customer details could become part of a product other companies use.', 'Yes by default. Opt-out only by email request. Vague wording about "improving services".'),
    ('Data and privacy', 'Which of your staff and sub-suppliers can see our data, and for what purpose?', 'Every extra party is another place where data can leak or be misused.', 'Cannot say who. No list of sub-suppliers. "Only when needed" with no detail.'),
    ('Data and privacy', 'How long do you keep our data, and how do we delete it?', 'Data kept after you leave is still your risk, and personal data should not be kept longer than needed.', 'No fixed period. Deletion only on request after months. No proof of deletion.'),
    ('Data and privacy', 'Will you sign a data processing agreement and tell us within a set time if there is a breach?', 'The company stays responsible for personal data it hands to a vendor.', 'Refuses a data agreement. No breach notice time. Standard terms only.'),
    ('Security', 'Which independent audits or certifications do you hold, and can we see the report?', 'A certificate or audit report is evidence. A claim is not.', '"We are very secure." No report. Certificates that belong to a parent company or are out of date.'),
    ('Security', 'How do our staff sign in, and can we turn on two-step sign-in and set who sees what?', 'Shared logins and no roles are how most small-company breaches start.', 'Shared logins. No roles. Two-step sign-in costs extra or is missing.'),
    ('Security', 'Is our data kept apart from other customers\' data, and is it encrypted in transit and at rest?', 'A mistake in another customer\'s account must not expose yours.', 'Cannot explain how data is separated. No encryption detail.'),
    ('Security', 'How does the tool defend against prompt injection: hidden instructions in the emails and documents it reads?', 'An incoming email can contain text that tricks a tool into acting. It is the top-ranked risk for AI applications in the OWASP list for 2025.', '"That is not a risk." Cannot describe any defence. The tool acts on incoming text without a person.'),
    ('Security', 'What can the tool do in our systems, and can we limit it to read-only or require approval for each action?', 'The wider the permission, the larger the damage from one mistake.', 'Needs full administrator access. No approval step. No activity log.'),
    ('Accuracy evidence', 'What evidence shows it works on tasks like ours, and how was it measured?', 'Demonstrations are chosen to look good. Measured results on similar work are evidence.', 'Only a demo. Only the vendor\'s own examples. No numbers. "Customers love it."'),
    ('Accuracy evidence', 'Can we run a pilot on our own data, with our own success measure, before we sign?', 'A pilot on your own data is the only test that matters for your task.', 'Refuses a pilot. Pilot only after payment. Vendor chooses the data.'),
    ('Accuracy evidence', 'What error rate do you see, and what kinds of mistakes does it make?', 'Every AI tool makes mistakes. A vendor who knows its mistakes can help you catch them.', 'Claims it is nearly always right. Cannot name any failure.'),
    ('Accuracy evidence', 'How does the tool show where an answer came from, so a person can check it?', 'A result you cannot trace cannot be checked quickly.', 'No sources shown. No log of inputs and outputs.'),
    ('Accuracy evidence', 'What happens to results when the underlying AI model changes, and will you tell us first?', 'A silent change can break a process that passed your tests.', 'Models change without notice. No way to keep an older version.'),
    ('Pricing drivers', 'What exactly do we pay for (users, volume, usage, features), and which of these grows as we grow?', 'Price follows a driver. Know which one, so you can forecast the bill.', 'A custom price only after you commit. Units that are unclear or keep changing.'),
    ('Pricing drivers', 'What costs are not in the quote: setup, training, connections to our systems, extra environments, support?', 'Extras can double the first-year cost.', 'A long list of extras. "We will scope that later."'),
    ('Pricing drivers', 'Can we cap usage costs and see usage as it happens?', 'Loops and heavy use can produce a large bill before anyone looks.', 'No cap. No alerts. Usage visible only on the invoice.'),
    ('Pricing drivers', 'How much can the price rise at renewal, and in which currency are we billed?', 'A price in a foreign currency or with no cap can change your business case without warning.', 'No cap on increases. Currency changes passed on in full.'),
    ('Pricing drivers', 'What does a realistic first-year total look like for a company of our size, in writing?', 'It lets you compare vendors on the same basis and test your business case.', 'Will not estimate. Gives only the lowest plan price.'),
    ('Contract and exit', 'Can we export all our data and settings in a usable format, and at what cost?', 'If you cannot take your data out, you cannot leave.', 'Own format only. Export fees. Export only on request after notice.'),
    ('Contract and exit', 'What are the minimum term and notice period, and does the contract renew automatically?', 'Auto-renewal with a long notice period is the commonest trap.', 'Multi-year lock-in. Renewal with 90 days or more notice. No early exit.'),
    ('Contract and exit', 'What happens to our data and access when we end the contract, and how fast?', 'You need a date by which your data is gone and proof of it.', 'No deletion date. Access cut immediately with no export window.'),
    ('Contract and exit', 'What are you liable for if you cause a loss or a data breach, and what is the cap?', 'A low cap means you carry most of the loss.', 'Liability excluded. Cap far below the value of what you put at risk.'),
    ('Contract and exit', 'What happens if you are bought, close down or change your terms?', 'Small AI vendors change owners and rules often.', 'Can change terms at any time. No continuity plan. No copy of your configuration.'),
    ('Support and references', 'What support do we get, in which hours and time zone, and how fast do you answer?', 'Problems on a Monday morning need an answer on Monday morning.', 'Email only. No stated response time. Support hours in another time zone only.'),
    ('Support and references', 'Who is our named contact, and do you have staff or partners in East Africa?', 'A person who knows your account saves days. Local presence helps with training and law.', 'Ticket system only. No local partner. Contact changes often.'),
    ('Support and references', 'Can we speak to two customers of similar size, ideally in our region?', 'A customer in your position will tell you what the sales deck does not.', 'Refuses. Logos only. Only customers chosen and prepared by the vendor.'),
    ('Support and references', 'What training do you provide for our staff, and what must we do ourselves?', 'A tool that staff cannot use produces no benefit.', 'Documentation only. Training at extra cost not in the quote.'),
    ('Support and references', 'What do customers struggle with most in the first 90 days?', 'An honest vendor knows where new customers fail.', '"Nothing." "Everyone loves it." No example.'),
]


def vendor():
    name = 'Vendor Question List'
    wb = new_wb(name)
    ws = wb.active; ws.title = 'Questions'
    H = ['#', 'Group', 'Question to ask the vendor', 'Why it matters', 'Vendor\'s answer (their words, in writing if possible)', 'Red-flag answers', 'Score 0-2']
    setup(ws, 'Vendor Question List: 30 questions in six groups',
          'Ask every question of every vendor, in writing where you can. Write the answer in their words. Compare it with the red-flag answers. Score each answer: 0 = a red flag, no answer or a refusal; 1 = partly clear; 2 = clear and in writing. '
          'The sheet Summary adds up each group. A 0 in Data and privacy, Security or Contract and exit is a reason to stop. Grey italic text in the first answer is an example: type over it.',
          H, [5, 20, 46, 44, 40, 46, 9], 32)
    for i, (g, q, why, red) in enumerate(QUESTIONS):
        r = 4 + i
        style_row(ws, r, 7, False, (1, 7)); fill_values(ws, r, [i + 1, g, q, why, None, red, None])
        ws.cell(r, 6).font = f(10, False, False, '404040')
    ws.cell(4, 5).value = 'Example: "Stored in the EU and the US. Sub-processors are listed in appendix B of the data agreement."'
    ws.cell(4, 5).font = F_EX
    add_whole(ws, 'G4:G33', 0, 2, 'Enter 0, 1 or 2.')
    cf_red(ws, 'G4:G33', 'AND(ISNUMBER($G4),$G4=0)')
    ws2 = wb.create_sheet('Summary')
    setup(ws2, 'Summary by group', 'Calculated from the sheet Questions. Type the vendor name and date in the two input cells.', ['Group', 'Questions', 'Answered', 'Points (max 10)', 'Zeros (red flags)'], [34, 14, 14, 16, 18], 22)
    for i, g in enumerate(GROUPS, 4):
        style_row(ws2, i, 5, False, (2, 3, 4, 5)); ws2.cell(i, 1).value = g; ws2.cell(i, 1).font = f(10, True)
        ws2.cell(i, 2).value = f'=COUNTIF(Questions!$B$4:$B$33,A{i})'
        ws2.cell(i, 3).value = f'=SUMPRODUCT((Questions!$B$4:$B$33=A{i})*ISNUMBER(Questions!$G$4:$G$33))'
        ws2.cell(i, 4).value = f'=SUMIF(Questions!$B$4:$B$33,A{i},Questions!$G$4:$G$33)'
        ws2.cell(i, 5).value = f'=COUNTIFS(Questions!$B$4:$B$33,A{i},Questions!$G$4:$G$33,0)'
    style_row(ws2, 10, 5, False, (2, 3, 4, 5))
    ws2.cell(10, 1).value = 'Total'; ws2.cell(10, 1).font = f(10, True)
    for c in range(2, 6):
        ws2.cell(10, c).value = f'=SUM({L(c)}4:{L(c)}9)'; ws2.cell(10, c).font = f(10, True)
    style_row(ws2, 12, 2); ws2.cell(12, 1).value = 'Share of the maximum score (60 points)'; ws2.cell(12, 2).value = '=IF(C10=0,"",D10/60)'; ws2.cell(12, 2).number_format = '0%'
    style_row(ws2, 13, 2); ws2.cell(13, 1).value = 'Vendor name'; style_row(ws2, 14, 2); ws2.cell(14, 1).value = 'Date of the answers'
    ws2.cell(13, 2).value = 'OrbitDesk (fictional)'; ws2.cell(14, 2).value = datetime.date(2026, 12, 3)
    for r in (13, 14):
        ws2.cell(r, 2).font = F_EX; ws2.cell(r, 2).border = INPUT_BORDER; ws2.cell(r, 1).font = f(10, True)
    ws2.cell(14, 2).number_format = 'dd mmm yyyy'
    ws2.column_dimensions['B'].width = 24
    cf_red(ws2, 'E4:E10', 'E4>0')
    save(wb, TEMPLATES / 'Vendor Question List.xlsx')


# ------------------------------------------------------ Business case
def business_case():
    name = 'Business Case Workbook'
    wb = new_wb(name)
    UGX = '#,##0;(#,##0);-'
    def inp(ws, cell, example):
        c = ws[cell]; c.border = INPUT_BORDER; c.font = F_NORM
        col = cell
        if isinstance(example, str):
            fm = f'{cell}="{example}"'
        else:
            fm = f'{cell}={example}'
        ws.conditional_formatting.add(cell, FormulaRule(formula=[fm], font=Font(name=FONT, italic=True, color=GREY)))
    # Inputs
    ws = wb.active; ws.title = 'Inputs'
    setup(ws, 'Business Case: step 1, inputs',
          'Session 12. Describe your own task in the boxed cells in column B. Every grey italic value is an example to overwrite: type your own over it and it turns black. Money is in UGX. Every other sheet is calculated from these cells, so change them here only. '
          'Where the examples come from: times a month, minutes today, share of runs with an error and cost of one error are the Session 12 Task Card numbers of the fictional company Nile Valley Foods Ltd (NVF) for the Monday sales email (4 times, 90 minutes, 4 runs in 10, UGX 150,000). '
          'The hourly cost, the licence price and the plan numbers (minutes with the new routine, review minutes, share of errors removed) are invented NVF estimates that nobody has measured. Estimates are fine: say which ones in the Note column, and replace them with your own timing or a pilot result when you have one.',
          ['Item', 'Your value', 'Unit', 'Note'], [52, 26, 16, 70], 24)
    items = [
        ('Task', 'Monday sales summary email', '', 'The task from your Task Card (Session 12)', '@'),
        ('Who does it today', 'Sales Manager', '', '', '@'),
        ('Times a month', 4, 'times', 'Session 12 Task Card (NVF: measured). How many times the task is done in a month', '0.0'),
        ('Minutes each time today', 90, 'minutes', 'Session 12 Task Card baseline (NVF: estimate)', '0'),
        ('People involved each time', 1, 'people', '', '0'),
        ('Loaded hourly cost of staff time', 30000, 'UGX per hour', 'Pay plus employer contributions and benefits, divided by hours worked. NVF: (4,500,000 + 500,000) / 160 = about 31,250, rounded to 30,000. Invented figure.', UGX),
        ('Share of runs with an error today', 0.4, 'share of runs', 'Session 12 Task Card (NVF: estimate). 0.4 means 4 runs in 10 contain an error', '0%'),
        ('Cost of one error', 150000, 'UGX', 'Session 12 Task Card (NVF: estimate). Staff time to fix it plus any loss. Say how you got it.', UGX),
        ('Minutes each time with the new routine (your own work, before review)', 10, 'minutes', 'Nile Valley Foods example: overwrite with your numbers. Plan only, nothing measured yet. NVF: the Task Card target is a draft in 10 minutes, so 10 of your own minutes. Review is counted separately below.', '0'),
        ('Review minutes each time (checking the result)', 20, 'minutes', 'Plan. The Task Card target is checked in 20 minutes. Never set this to 0: a person checks every result', '0'),
        ('Share of errors the new routine removes', 0.6, 'share of errors', 'Plan only, nothing measured yet. Use a pilot or your own checks when you have them. Be cautious.', '0%'),
    ]
    for i, (a, b, c, d, nf) in enumerate(items, 4):
        style_row(ws, i, 4); ws.cell(i, 1).value = a; ws.cell(i, 1).font = f(10, True)
        ws.cell(i, 2).value = b; ws.cell(i, 3).value = c; ws.cell(i, 4).value = d
        inp(ws, f'B{i}', b); ws.cell(i, 2).number_format = nf; ws.cell(i, 2).alignment = Alignment(horizontal='right', vertical='top', wrap_text=True)
    style_row(ws, 15, 4); ws.cell(15, 1).value = 'Minutes saved each time before review (computed)'; ws.cell(15, 1).font = f(10, True)
    ws.cell(15, 2).value = '=IF(OR(B7="",B12=""),"",B7-B12)'; ws.cell(15, 2).number_format = '0'; ws.cell(15, 2).alignment = Alignment(horizontal='right', vertical='top')
    ws.cell(15, 3).value = 'minutes'; ws.cell(15, 4).value = 'Minutes today minus your own minutes with the new routine. Review minutes are a cost and are counted on the Costs sheet. Calculated: do not type here.'
    add_decimal(ws, 'B6:B9', 0); add_decimal(ws, 'B10', 0, 1); add_decimal(ws, 'B11', 0); add_decimal(ws, 'B12:B13', 0); add_decimal(ws, 'B14', 0, 1)
    # Costs
    wc = wb.create_sheet('Costs')
    setup(wc, 'Business Case: step 2, costs',
          'List what the change costs. One-off costs happen once; monthly costs repeat. Rates come from the Inputs sheet. Boxed cells are inputs (grey italic = NVF example to overwrite). Tool prices change: write the current price you were quoted and avoid guessing. If you buy or partner, use the vendor\'s first-year total in these lines. '
          'Review time is worked out from the review minutes on the Inputs sheet.',
          ['Cost item', 'Quantity (hours)', 'Rate (UGX per hour)', 'One-off (UGX)', 'Monthly (UGX)', 'Note'], [46, 14, 18, 16, 16, 60], 32)
    rows = [
        ('Tool licence', None, None, None, 60000, 'Monthly price quoted by the vendor, converted to UGX. The NVF figure is invented.'),
        ('Set-up and data preparation (hours)', 12, '=Inputs!$B$9', '=B5*C5', None, 'Your hours to prepare the data, write the prompt and test it'),
        ('Training (hours, everyone involved)', 4, '=Inputs!$B$9', '=B6*C6', None, 'Time for staff to learn the new routine'),
        ('Review (hours a month)', '=Inputs!$B$6*Inputs!$B$13/60', '=Inputs!$B$9', None, '=B7*C7', 'Times a month x review minutes / 60, from the Inputs sheet'),
        ('Upkeep (hours a month)', 1.5, '=Inputs!$B$9', None, '=B8*C8', 'Fixing, updating, answering questions'),
        ('Other cost (describe in the note)', None, None, None, None, 'For example an outside adviser or a new subscription'),
    ]
    for i, row in enumerate(rows, 4):
        style_row(wc, i, 6, False, (), {2: '0.0', 3: UGX, 4: UGX, 5: UGX})
        fill_values(wc, i, row)
        wc.cell(i, 1).font = f(10, True)
    for cell, ex in (('E4', 60000), ('B5', 12), ('B6', 4), ('B8', 1.5)):
        inp(wc, cell, ex)
    for cell in ('D4', 'D9', 'E9', 'B9', 'C9'):
        wc[cell].border = INPUT_BORDER
    for cell in ('D4', 'B4', 'C4'):
        wc[cell].border = INPUT_BORDER if cell == 'D4' else BORDER
    style_row(wc, 10, 6, False, (), {4: UGX, 5: UGX}); wc.cell(10, 1).value = 'Total costs'; wc.cell(10, 1).font = f(10, True)
    wc.cell(10, 4).value = '=SUM(D4:D9)'; wc.cell(10, 5).value = '=SUM(E4:E9)'
    for c in (4, 5):
        wc.cell(10, c).font = f(10, True)
    # Benefits
    wbn = wb.create_sheet('Benefits')
    setup(wbn, 'Business Case: step 3, benefits',
          'Time saved and errors avoided are worked out from the Inputs sheet. Add other benefits only when you can show them with a number (fewer late payments, an extra sale). Do not count the same benefit twice.',
          ['Benefit', 'Quantity a month', 'Rate (UGX)', 'Value a month (UGX)', 'How it is worked out'], [42, 16, 16, 20, 70], 32)
    brow = [
        ('Time saved (hours a month)', '=Inputs!$B$6*Inputs!$B$8*(Inputs!$B$7-Inputs!$B$12)/60', '=Inputs!$B$9', '=B4*C4',
         'Times a month x people x (minutes today minus your own minutes with the new routine) / 60 x hourly cost. Review time is counted under costs.'),
        ('Errors avoided (a month)', '=Inputs!$B$6*Inputs!$B$10*Inputs!$B$14', '=Inputs!$B$11', '=B5*C5', 'Times a month x error rate x share removed x cost of one error'),
        ('Other benefit (describe in the note)', None, None, 0, 'For example fewer late supplier payments. Leave at 0 unless you can show it.'),
    ]
    for i, row in enumerate(brow, 4):
        style_row(wbn, i, 5, False, (), {2: '0.00', 3: UGX, 4: UGX}); fill_values(wbn, i, row); wbn.cell(i, 1).font = f(10, True)
    wbn['D6'].border = INPUT_BORDER; wbn['D6'].font = F_NORM
    style_row(wbn, 7, 5, False, (), {4: UGX}); wbn.cell(7, 1).value = 'Total benefit a month'; wbn.cell(7, 1).font = f(10, True)
    wbn.cell(7, 4).value = '=SUM(D4:D6)'; wbn.cell(7, 4).font = f(10, True)
    # Result
    wr = wb.create_sheet('Result')
    setup(wr, 'Business Case: step 4, result',
          'Everything here is calculated. The only input is the haircut in the boxed cell: the share of the benefit you choose not to count because estimates are usually too hopeful (a common starting point is 30%). '
          'A case that is still positive after the haircut is a stronger case.',
          ['Measure', 'Value', 'What it means'], [48, 22, 78], 22)
    res = [
        ('Monthly benefit', '=Benefits!D7', UGX, 'Time saved plus errors avoided plus other benefits'),
        ('Monthly cost', '=Costs!E10', UGX, 'Licence, review, upkeep and other monthly costs'),
        ('Monthly net', '=B4-B5', UGX, 'Benefit minus cost, each month'),
        ('One-off cost', '=Costs!D10', UGX, 'Set-up, data preparation, training and other one-off costs'),
        ('Payback (months)', '=IF(B6<=0,"No payback",B7/B6)', '0.0', 'One-off cost divided by monthly net'),
        ('12-month net', '=B6*12-B7', UGX, 'Twelve months of net benefit minus the one-off cost'),
        ('Haircut (share of the benefit you do not count)', 0.3, '0%', 'Input. Type your own figure. 0.3 means count 70% of the benefit.'),
        ('Risk-adjusted monthly benefit', '=B4*(1-B10)', UGX, 'Monthly benefit after the haircut'),
        ('Risk-adjusted monthly net', '=B11-B5', UGX, 'After the haircut'),
        ('Risk-adjusted payback (months)', '=IF(B12<=0,"No payback",B7/B12)', '0.0', ''),
        ('Risk-adjusted 12-month net', '=B12*12-B7', UGX, 'The number to take to the owner or the board'),
        ('Break-even haircut', '=IF(B4<=0,"",1-(B5*12+B7)/(B4*12))', '0%', 'The haircut at which the 12-month net is zero. A negative figure means the case is negative even if every benefit is real.'),
        ('Reading', '=IF(B14>0,"Positive after the haircut: go to a pilot with a review date and the stop rules.","Negative after the haircut: revise the case, or stop.")', '@', 'What would change my mind: a higher error cost, fewer review minutes, a lower tool price, or a measured test that beats these estimates.'),
    ]
    for i, (a, b, nf, d) in enumerate(res, 4):
        style_row(wr, i, 3, False, (), {2: nf}); wr.cell(i, 1).value = a; wr.cell(i, 1).font = f(10, True); wr.cell(i, 2).value = b; wr.cell(i, 3).value = d
        wr.cell(i, 2).alignment = Alignment(horizontal='right', vertical='top', wrap_text=True); wr.cell(i, 3).alignment = Alignment(vertical='top', wrap_text=True, indent=1)
    wr['B10'].border = INPUT_BORDER; inp(wr, 'B10', 0.3)
    wr['B16'].alignment = Alignment(horizontal='left', vertical='top', wrap_text=True)
    wr.row_dimensions[16].height = 44
    cf_red(wr, 'B6:B6', 'AND(ISNUMBER($B$6),$B$6<0)'); cf_red(wr, 'B14:B14', 'AND(ISNUMBER($B$14),$B$14<0)')
    # Sensitivity
    wsn = wb.create_sheet('Sensitivity')
    setup(wsn, 'Business Case: step 5, three scenarios',
          'Each scenario changes four factors. A factor of 1 leaves the base value as it is; 0.6 keeps 60% of it. Edit the boxed factors to suit your task. '
          'Volume changes the benefit only: review time stays at the base figure, which keeps the low case cautious. Read the low case first: can you live with it?',
          ['Factor or result', 'Low', 'Base', 'High', 'How to read it'], [52, 16, 16, 16, 70], 22)
    fac = [('Volume factor (share of base volume)', 0.7, 1, 1.1, 'Benefit scales with volume'),
           ('Time saved factor (share of the saving that really happens)', 0.6, 1, 1.2, '0.6 means only 60% of the planned saving'),
           ('Errors avoided factor', 0.4, 1, 1.2, '0.4 means the new routine removes 40% of what you planned'),
           ('Cost factor (1.3 means costs are 30% higher)', 1.3, 1, 0.9, 'Applies to monthly and one-off costs')]
    for i, row in enumerate(fac, 4):
        style_row(wsn, i, 5, False, (), {2: '0.00', 3: '0.00', 4: '0.00'}); fill_values(wsn, i, row); wsn.cell(i, 1).font = f(10, True)
        for c in 'BCD':
            inp(wsn, f'{c}{i}', row['BCD'.index(c) + 1])
    out = [('Monthly benefit (UGX)', '=(Benefits!$D$4*{c}5+Benefits!$D$5*{c}6)*{c}4+Benefits!$D$6', UGX, ''),
           ('Monthly cost (UGX)', '=Costs!$E$10*{c}7', UGX, ''),
           ('One-off cost (UGX)', '=Costs!$D$10*{c}7', UGX, ''),
           ('Monthly net (UGX)', '={c}8-{c}9', UGX, ''),
           ('Payback (months)', '=IF({c}11<=0,"No payback",{c}10/{c}11)', '0.0', ''),
           ('12-month net (UGX)', '={c}11*12-{c}10', UGX, 'Positive in all three scenarios is a robust case')]
    for i, (a, fm, nf, d) in enumerate(out, 8):
        style_row(wsn, i, 5, False, (), {2: nf, 3: nf, 4: nf}); wsn.cell(i, 1).value = a; wsn.cell(i, 1).font = f(10, True); wsn.cell(i, 5).value = d
        for c in 'BCD':
            wsn[f'{c}{i}'].value = fm.format(c=c); wsn[f'{c}{i}'].alignment = Alignment(horizontal='right', vertical='top')
    style_row(wsn, 14, 5); wsn['A14'].value = 'Check: the Base column equals the Result sheet'; wsn['A14'].font = f(10, True)
    wsn['C14'].value = '=IF(ABS(C11-Result!B6)<0.5,"Matches","Check the factors in the Base column")'
    cf_red(wsn, 'B13:D13', 'AND(ISNUMBER(B13),B13<0)')
    # Stop rules
    wst = wb.create_sheet('Stop rules')
    setup(wst, 'Business Case: step 6, what would stop it',
          'Write your stop rules now, before you start, while you are calm. Each rule is a number somebody can check, and says Stop or Revise. Then record the decision you will take to your sponsor: go to a pilot, revise or stop, and the number that decided it. '
          'Grey italic rules are NVF examples: type over them. In Session 14 these rules become part of your 90-day plan, so choose numbers you can read from your own records.',
          ['#', 'Stop rule (a number you can check)', 'Stop or revise?', 'Where I will read the number', 'Owner'], [5, 62, 14, 40, 22], 28)
    rules = [('Stop if one error reaches a customer or the bank, until the cause is fixed.', 'Stop', 'Error log', 'Peter Okello'),
             ('Revise if review minutes rise above 30 a run.', 'Revise', 'Results Tracker', 'Peter Okello'),
             ('Revise if the 12-month net after the haircut turns negative.', 'Revise', 'Result sheet, Risk-adjusted 12-month net', 'Joseph Mugisha'),
             ('Stop if the saving is under half the plan after four weeks.', 'Stop', 'Results Tracker', 'Sarah Namukasa'),
             ('Scale only after the base case holds for two months.', 'Revise', 'Results Tracker', 'Sarah Namukasa')]
    for i, (a_, b_, c_, d_) in enumerate(rules):
        style_row(wst, 4 + i, 5, True, (1, 3)); fill_values(wst, 4 + i, ['Ex', a_, b_, c_, d_])
    for r in range(9, 15):
        style_row(wst, r, 5, False, (1, 3)); wst.cell(r, 1).value = r - 8
    add_list(wst, 'C4:C14', ['Stop', 'Revise'])
    for i, (lab, val) in enumerate([('Sponsor (the person who owns the result and asks for the decision)', 'Sarah Namukasa, Managing Director'),
                                    ('Decision: go to a pilot, revise or stop', 'Go to a pilot'),
                                    ('The number that decided it', 'Base 12-month net UGX 1,428,000; UGX 333,600 after a 30% haircut')], 16):
        style_row(wst, i, 5); wst.merge_cells(start_row=i, start_column=1, end_row=i, end_column=2)
        wst.cell(i, 1).value = lab; wst.cell(i, 1).font = f(10, True); wst.cell(i, 3).value = val; wst.merge_cells(start_row=i, start_column=3, end_row=i, end_column=5)
        wst.cell(i, 3).font = F_EX; wst.cell(i, 3).border = INPUT_BORDER; wst.row_dimensions[i].height = 28
    add_list(wst, 'C17', ['Go to a pilot', 'Revise', 'Stop'])
    save(wb, TEMPLATES / 'Business Case Workbook.xlsx')


# ------------------------------------------------------------ Roadmap
def roadmap():
    name = '90-Day Roadmap'
    wb = new_wb(name)
    ws = wb.active; ws.title = 'Roadmap'
    H = ['Phase', 'Action', 'Owner', 'Start', 'Due', 'Effort (hours)', 'Depends on', 'Success measure', 'Status']
    PH = ['Protect and clean', 'Describe and prepare', 'Test and decide']
    setup(ws, '90-Day Roadmap: your data roadmap in three phases',
          'Session 14. Turn each gap from your readiness scorecard into one line: one action a person can finish, one owner, a start and a due date, the hours (your estimate), what it waits for, and a success measure that is a number someone else can check (a number, a date and a checker). '
          'Number each action at the start of its text (1, 2, 3) and write those numbers in Depends on, so nothing is tested before the data is ready and allowed. Aim for three to six actions in each phase (Protect and clean is days 1 to 30, Describe and prepare days 31 to 60, Test and decide days 61 to 90). Update the status every week. '
          'Type your plan start date in the boxed cell at the right: the day 30, 60 and 90 check-in dates are worked out for you. The NVF example starts on 1 February 2027, so day 30 is 3 March 2027, day 60 is 2 April 2027 and day 90 is 2 May 2027. '
          'Decisions, risks and check-ins have their own sheets. In the example the lawyer\'s time is not counted in the hours. ' + NVF_NOTE,
          H, [28, 44, 18, 13, 13, 11, 13, 40, 13], 32)
    D = datetime.date
    exrows = [
        (PH[0], '1 Write the data-sharing rule', 'Sarah Namukasa', D(2027, 2, 1), D(2027, 2, 26), 4, 'None', 'Rule signed and filed', 'Not started'),
        (PH[0], '2 Fix the invoice file', 'Joseph Mugisha', D(2027, 2, 1), D(2027, 2, 19), 6, 'None', '0 faults on recheck', 'Not started'),
        (PH[1], '3 Write the data dictionary', 'Peter Okello', D(2027, 2, 6), D(2027, 3, 26), 8, 'None', 'Every column defined', 'Not started'),
        (PH[1], '4 Mask phones in the export', 'David Kato', D(2027, 2, 26), D(2027, 4, 2), 5, '1', '0 phones in the copy', 'Not started'),
        (PH[2], '5 Test retrieval', 'Grace Akello', D(2027, 4, 2), D(2027, 4, 23), 10, '2, 3, 4', '16 of 20 right, none invented', 'Not started'),
        (PH[2], '6 Decide', 'Sarah Namukasa', D(2027, 4, 23), D(2027, 4, 30), 2, '5', 'Decision recorded', 'Not started'),
    ]
    fm = {4: 'dd mmm yyyy', 5: 'dd mmm yyyy', 6: '0.0'}
    for i, row in enumerate(exrows):
        r = 4 + i; style_row(ws, r, 9, True, (4, 5, 6, 7, 9), fm); fill_values(ws, r, list(row))
    last = 33
    for r in range(10, last + 1):
        style_row(ws, r, 9, False, (4, 5, 6, 7, 9), fm)
    add_list(ws, f'A4:A{last}', PH)
    add_list(ws, f'I4:I{last}', ['Not started', 'In progress', 'Done', 'Blocked', 'Dropped']); add_date(ws, f'D4:E{last}'); add_decimal(ws, f'F4:F{last}', 0)
    cf_red(ws, f'I4:I{last}', '$I4="Blocked"')
    ws.conditional_formatting.add(f'I4:I{last}', FormulaRule(formula=['$I4="Done"'], font=Font(name=FONT, bold=True, color='000000')))
    ws.conditional_formatting.add(f'E4:E{last}', FormulaRule(formula=['AND(ISNUMBER($E4),$E4<TODAY(),$I4<>"Done",$I4<>"Dropped",$I4<>"")'], font=Font(name=FONT, bold=True, color=RED)))
    # side panel: start date and check-in dates
    ws.column_dimensions['J'].width = 3; ws.column_dimensions['K'].width = 30; ws.column_dimensions['L'].width = 16
    for c, h in ((11, 'Plan dates'), (12, 'Date')):
        cell = ws.cell(3, c); cell.value = h; cell.font = F_HEAD; cell.fill = BLACKFILL; cell.alignment = Alignment(wrap_text=True, vertical='center')
    panel = [('Plan start date', D(2027, 2, 1)), ('Day 30 check-in', '=IF(L4="","",L4+30)'), ('Day 60 check-in', '=IF(L4="","",L4+60)'), ('Day 90 check-in', '=IF(L4="","",L4+90)')]
    for i, (a, b) in enumerate(panel, 4):
        for c in (11, 12):
            ws.cell(i, c).border = BORDER; ws.cell(i, c).font = F_NORM; ws.cell(i, c).alignment = WRAP
        ws.cell(i, 11).value = a; ws.cell(i, 11).font = f(10, True); ws.cell(i, 12).value = b; ws.cell(i, 12).number_format = 'dd mmm yyyy'
    ws.cell(4, 12).font = F_EX; ws.cell(4, 12).border = INPUT_BORDER
    for i, (a, b, nf) in enumerate([('Actions listed', f'=COUNTA(B4:B{last})', '0'), ('Total effort (hours, estimate)', f'=SUM(F4:F{last})', '0.0'),
                                    ('Actions done', f'=COUNTIF(I4:I{last},"Done")', '0')], 8):
        for c in (11, 12):
            ws.cell(i, c).border = BORDER; ws.cell(i, c).font = F_NORM; ws.cell(i, c).alignment = WRAP
        ws.cell(i, 11).value = a; ws.cell(i, 11).font = f(10, True); ws.cell(i, 12).value = b; ws.cell(i, 12).number_format = nf
    add_date(ws, 'L4')
    # decisions
    wd = wb.create_sheet('Decisions')
    setup(wd, 'Decisions list', 'Write each decision the company must make during the 90 days: who decides, by when, and what was decided. ' + NVF_NOTE,
          ['#', 'Decision needed', 'Why it matters', 'Who decides', 'Needed by', 'What was decided', 'Date decided'], [5, 46, 44, 20, 14, 40, 14], 28)
    ex = [['Ex', 'Approve the data-sharing rule and name one approved tool', 'Rights is the only Red area: nothing else is safe to do until it is settled', 'Sarah Namukasa', datetime.date(2027, 2, 26), '', None],
          ['Ex', 'Continue, expand, pause or stop after the retrieval test', 'Sets the plan for the next quarter', 'Sarah Namukasa', datetime.date(2027, 4, 30), '', None]]
    for i, row in enumerate(ex):
        style_row(wd, 4 + i, 7, True, (1, 5, 7), {5: 'dd mmm yyyy', 7: 'dd mmm yyyy'}); fill_values(wd, 4 + i, row)
    for rr in range(6, 16):
        style_row(wd, rr, 7, False, (1, 5, 7), {5: 'dd mmm yyyy', 7: 'dd mmm yyyy'}); wd.cell(rr, 1).value = rr - 5
    add_date(wd, 'E4:E15'); add_date(wd, 'G4:G15')
    # risks
    wk = wb.create_sheet('Risks')
    setup(wk, 'Risks list', 'Write the risks to the roadmap itself: what could stop the plan, including risks that are not about AI. List at least three, one about people (an owner who is away or leaves). Rate likelihood and impact High, Medium or Low. The full AI risk list lives in your Risk Register. ' + NVF_NOTE,
          ['#', 'Risk to the plan', 'Likelihood', 'Impact', 'What we will do', 'Owner', 'Status'], [5, 46, 12, 12, 52, 20, 14], 28)
    ex = [['Ex', 'Peter is away in week 3 and nobody can write the data dictionary', 'Medium', 'Medium', 'Train Mary Nabirye as a second owner for the dictionary', 'Sarah Namukasa', 'Open'],
          ['Ex', 'Sarah is away and nobody can sign the data-sharing rule', 'Low', 'High', 'Mary Nabirye covers and signs for the Managing Director', 'Sarah Namukasa', 'Open'],
          ['Ex', 'The files change before the retrieval test', 'Medium', 'High', 'Keep a dated copy of the files at day 60 and run the same 20 questions on it', 'Grace Akello', 'Open']]
    for i, row in enumerate(ex):
        style_row(wk, 4 + i, 7, True, (1, 3, 4, 7)); fill_values(wk, 4 + i, row)
    for rr in range(7, 17):
        style_row(wk, rr, 7, False, (1, 3, 4, 7)); wk.cell(rr, 1).value = rr - 6
    add_list(wk, 'C4:D16', ['High', 'Medium', 'Low']); add_list(wk, 'G4:G16', ['Open', 'Controlled', 'Happened', 'Closed'])
    cf_red(wk, 'C4:D16', 'C4="High"')
    # check-ins
    wc = wb.create_sheet('Check-ins')
    setup(wc, 'Check-ins: day 30, day 60 and day 90',
          'Session 14. The dates come from your plan start date on the sheet Roadmap. Your lecturer contacts you by message or call at day 30, day 60 and day 90. At each check-in you bring the 30-60-90 Check-in Form and the test below. Nobody is scored: the check-in reports what happened so that the plan can change. ' + NVF_NOTE,
          ['Day', 'Date', 'You bring', 'The test', 'What I found'], [10, 16, 40, 56, 50], 28)
    cks = [(30, '=Roadmap!L5', 'Check-in Form, roadmap', 'Are the Session 13 controls in place? Is gap 1 closed?'),
           (60, '=Roadmap!L6', 'Form and a Results Tracker row', 'Is any Session 12 stop rule met? Are actions on time?'),
           (90, '=Roadmap!L7', 'Form and Sponsor Briefing', 'Re-score the six areas. Continue, expand, pause or stop.')]
    for i, (dday, dt, bring, test) in enumerate(cks, 4):
        style_row(wc, i, 5, False, (1, 2), {2: 'dd mmm yyyy'}); fill_values(wc, i, [f'Day {dday}', dt, bring, test]); wc.row_dimensions[i].height = 30
        wc.cell(i, 1).font = f(10, True)
    save(wb, TEMPLATES / '90-Day Roadmap.xlsx')


# ------------------------------------------------------ Results Tracker
def tracker():
    name = 'Results Tracker'
    wb = new_wb(name)
    ws = wb.active; ws.title = 'Monthly results'
    H = ['Month (first day)', 'Workflow or task', 'Runs', 'Minutes by hand per run (baseline)', 'Minutes planned per run', 'Minutes now per run (measured, with checking)', 'Hours saved (computed)',
         'Errors caught before release', 'Errors that got through', 'Incidents (any time the work broke a boundary or was stopped)', 'Cost this month (UGX)', 'Cumulative hours saved (this workflow)', 'Notes']
    setup(ws, 'Results Tracker: one row for each workflow each month',
          'Use it for the workflow you mapped in Session 12. Each month add one row for each workflow you changed. Type the first day of the month (for example 01/02/2027). Baseline minutes come from your Task Card; planned minutes come from your business case; minutes now are measured by timing the real work and include the time spent checking. Leave the measured columns empty until you have a measurement. Hours saved use the baseline and the measured minutes. Count an incident whenever the work went outside its boundary sheet or you had to stop it. Record roadmap actions closed in the Notes column. '
          'Hours saved and the running total are calculated. The sheet Summary adds the months together and draws the chart. The three grey rows are NVF examples (fictional): delete them when you add your first real month.',
          H, [15, 32, 8, 17, 14, 17, 14, 15, 15, 20, 16, 20, 36], 60)
    ex = [(datetime.date(2027, 2, 1), 4, 90, 25, 35, 1, 0, 0, 145000), (datetime.date(2027, 3, 1), 4, 90, 25, 35, 0, 0, 1, 145000), (datetime.date(2027, 4, 1), 4, 90, 25, 35, 0, 0, 0, 145000)]
    fm = {1: 'dd mmm yyyy', 7: '0.0', 11: '#,##0;(#,##0);-', 12: '0.0'}
    for i, (m, runs, base, plan, now, e1, e2, inc, cost) in enumerate(ex):
        r = 4 + i; style_row(ws, r, 13, True, (1, 3, 4, 5, 6, 7, 8, 9, 10, 12), fm)
        fill_values(ws, r, [m, 'Monday sales email', runs, base, plan, now, None, e1, e2, inc, cost, None, 'Example: delete this row'])
    for r in range(7, 60):
        style_row(ws, r, 13, False, (1, 3, 4, 5, 6, 7, 8, 9, 10, 12), fm)
    for r in range(4, 60):
        ws.cell(r, 7).value = f'=IF(OR(C{r}="",D{r}="",F{r}=""),"",C{r}*(D{r}-F{r})/60)'
        ws.cell(r, 12).value = f'=IF(OR(G{r}="",B{r}=""),"",SUMIFS($G$4:G{r},$B$4:B{r},B{r}))'
    add_date(ws, 'A4:A59'); add_decimal(ws, 'C4:F59', 0); add_decimal(ws, 'H4:K59', 0)
    ws2 = wb.create_sheet('Summary')
    setup(ws2, 'Summary and chart: hours saved by month',
          'Type the first month and the hourly cost of staff time in the two boxed cells. The table and chart update from the sheet Monthly results. Twelve months are shown.',
          ['Setting', 'Value', '', '', ''], [28, 22, 22, 26, 24], 22)
    ws2.cell(4, 1).value = 'First month (first day)'; ws2.cell(4, 2).value = datetime.date(2027, 2, 1); ws2.cell(4, 2).number_format = 'dd mmm yyyy'
    ws2.cell(5, 1).value = 'Hourly cost of staff time (UGX)'; ws2.cell(5, 2).value = 30000; ws2.cell(5, 2).number_format = '#,##0'
    ws2.cell(6, 1).value = 'Grey example rows still in the tracker?'
    ws2.cell(6, 2).value = ("=IF(COUNTIF('Monthly results'!M4:M59,\"Example*\")>0,\"Yes: delete \"&COUNTIF('Monthly results'!M4:M59,\"Example*\")&\" rows\",\"No\")")
    for r in (4, 5, 6):
        style_row(ws2, r, 2); ws2.cell(r, 1).font = f(10, True)
    for r in (4, 5):
        ws2.cell(r, 2).font = F_EX; ws2.cell(r, 2).border = INPUT_BORDER; ws2.cell(r, 2).alignment = Alignment(horizontal='right')
    ws2.cell(4, 2).number_format = 'dd mmm yyyy'; ws2.cell(5, 2).number_format = '#,##0'
    cf_red(ws2, 'B6', 'LEFT($B$6,3)="Yes"')
    hdr = ['Month', 'Hours saved in the month', 'Cumulative hours saved', 'Value of time saved in the month (UGX)', 'Cumulative value (UGX)']
    for i, h in enumerate(hdr, 1):
        c = ws2.cell(8, i); c.value = h; c.font = F_HEAD; c.fill = BLACKFILL; c.alignment = Alignment(wrap_text=True, vertical='center')
    ws2.row_dimensions[8].height = 32
    for k in range(12):
        r = 9 + k
        style_row(ws2, r, 5, False, (), {1: 'mmm yyyy', 2: '0.0', 3: '0.0', 4: '#,##0;(#,##0);-', 5: '#,##0;(#,##0);-'})
        ws2.cell(r, 1).value = '=$B$4' if k == 0 else f'=EDATE(A{r - 1},1)'
        ws2.cell(r, 2).value = (f"=SUMIFS('Monthly results'!$G$4:$G$59,'Monthly results'!$A$4:$A$59,\">=\"&A{r},'Monthly results'!$A$4:$A$59,\"<\"&EDATE(A{r},1))")
        ws2.cell(r, 3).value = f'=SUM($B$9:B{r})'
        ws2.cell(r, 4).value = f'=B{r}*$B$5'
        ws2.cell(r, 5).value = f'=SUM($D$9:D{r})'
        ws2.cell(r, 1).alignment = Alignment(horizontal='left')
    bar = BarChart(); bar.type = 'col'; bar.title = 'Hours saved: each month and running total'
    bar.add_data(Reference(ws2, min_col=2, min_row=8, max_row=20), titles_from_data=True)
    bar.set_categories(Reference(ws2, min_col=1, min_row=9, max_row=20))
    bar.series[0].graphicalProperties = GraphicalProperties(solidFill='A6A6A6'); bar.series[0].graphicalProperties.line.solidFill = '767676'
    line = LineChart()
    line.add_data(Reference(ws2, min_col=3, min_row=8, max_row=20), titles_from_data=True)
    line.series[0].graphicalProperties.line.solidFill = RED; line.series[0].graphicalProperties.line.width = 28000
    line.series[0].smooth = False
    line.series[0].marker.symbol = 'circle'; line.series[0].marker.size = 6
    line.series[0].marker.graphicalProperties = GraphicalProperties(solidFill=RED); line.series[0].marker.graphicalProperties.line.solidFill = RED
    bar.y_axis.title = 'Hours saved'; bar.x_axis.title = 'Month'
    bar.x_axis.number_format = 'mmm yy'; bar.x_axis.delete = False; bar.y_axis.delete = False
    bar.y_axis.majorGridlines.spPr = GraphicalProperties(); bar.y_axis.majorGridlines.spPr.line.solidFill = 'D9D9D9'
    bar.height = 9.5; bar.width = 22; bar.legend.position = 'b'
    bar += line
    ws2.add_chart(bar, 'A23'); ws2.page_setup.fitToHeight = 1; ws2.page_setup.orientation = 'portrait'
    ws2.freeze_panes = None
    save(wb, FOLLOWUP / 'Results Tracker.xlsx')


def run():
    vendor(); business_case(); roadmap(); tracker()
