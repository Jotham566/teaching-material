"""Excel templates, part 1. Run: python3 gen_xlsx.py (calls part 2 as well)."""
from xlsx_kit import *
from openpyxl.chart import ScatterChart, Reference, Series
from openpyxl.chart.marker import Marker
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.chart.layout import Layout, ManualLayout

SENS = ['Public', 'Internal', 'Confidential', 'Internal + Personal', 'Confidential + Personal']
KINDS = ['Rules', 'Patterns', 'Drafting', 'Judgement']
NVF_NOTE = 'Grey italic rows are examples from the fictional company Nile Valley Foods Ltd (NVF): type your own entries in the rows below them (or over them).'


# ------------------------------------------------------------ Scorecard
def scorecard():
    name = 'Use-Case Scorecard'
    wb = new_wb(name)
    # sheet 1
    ws = wb.active; ws.title = 'Ten tasks'
    H = ['#', 'Task', 'Owner', 'How often', 'Kind of work', 'Minutes each time', 'Minutes a month (computed)']
    setup(ws, 'Use-Case Scorecard: step 1 of 3, list ten tasks',
          'List ten recurring tasks from your own company, one per row, in rows 5 to 14. Choose how often and the kind of work from the lists (Rules, Patterns, Drafting, Judgement). '
          'If a task needs only a rule, a formula or a better spreadsheet, it is a Rules task: AI is probably not the answer. Then go to the sheet Score. ' + NVF_NOTE,
          H, [5, 46, 22, 13, 16, 14, 18], 32)
    style_row(ws, 4, 7, True, (1, 4, 5, 6, 7))
    fill_values(ws, 4, ['Ex', 'Draft the Monday sales summary email to the directors', 'Sales Manager', 'Weekly', 'Drafting', 90])
    for r in range(5, 15):
        style_row(ws, r, 7, False, (1, 4, 5, 6, 7)); ws.cell(r, 1).value = r - 4
    for r in range(4, 15):
        ws.cell(r, 7).value = (f'=IF(OR(D{r}="",F{r}=""),"",ROUND(F{r}*IF(D{r}="Daily",22,IF(D{r}="Weekly",4,IF(D{r}="Monthly",1,'
                               f'IF(D{r}="Quarterly",1/3,IF(D{r}="Yearly",1/12,0))))),0))')
    add_list(ws, 'D4:D14', ['Daily', 'Weekly', 'Monthly', 'Quarterly', 'Yearly'])
    add_list(ws, 'E4:E14', KINDS, 'Rules, Patterns, Drafting or Judgement')
    add_whole(ws, 'F4:F14', 0, 100000, 'Enter minutes as a whole number.')
    note(ws, 16, 'Kinds of work. Rules: a fixed answer (add up invoices). Patterns: sorting or finding in messy text. Drafting: writing or summarising. Judgement: a person decides (refunds, hiring). '
                 'Minutes a month assumes 22 working days, 4 weeks, 12 months, 4 quarters.', 7, 30)
    # sheet 2
    ws2 = wb.create_sheet('Score')
    H2 = ['#', 'Task (from sheet Ten tasks)', 'Value 1-5', 'Risk 1-5', 'Checkability 1-5', 'Happens at least weekly', 'Inputs exist as text or files',
          'I can check it in minutes', 'A mistake is caught before harm', 'One person owns it', 'I can measure it today',
          'Passes tests (of 6)', 'Priority (of 21)', 'Rank', 'Call']
    setup(ws2, 'Use-Case Scorecard: step 2 of 3, score each task',
          'Score each task: Value (5 = saves a lot or matters a lot), Risk (5 = a mistake would reach a customer, the bank or a person before anyone checks) and Checkability (5 = I can confirm a result in minutes). '
          'Then answer the six tests Yes or No. Gold highlights a task that passes at least five tests. Priority = value + checkability + (6 minus risk) + tests passed. Be honest about risk.',
          H2, [5, 40, 9, 9, 13, 12, 12, 12, 13, 10, 12, 11, 11, 7, 28], 54)
    style_row(ws2, 4, 15, True, tuple(range(3, 15)))
    fill_values(ws2, 4, [None, None, 4, 2, 5, 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes'])
    for r in range(5, 15):
        style_row(ws2, r, 15, False, tuple(range(3, 15)))
    for r in range(4, 15):
        ws2.cell(r, 1).value = 'Ex' if r == 4 else r - 4
        ws2.cell(r, 2).value = f"=IF('Ten tasks'!B{r}=\"\",\"\",'Ten tasks'!B{r})"
        ws2.cell(r, 12).value = f'=IF(B{r}="","",COUNTIF(F{r}:K{r},"Yes"))'
        ws2.cell(r, 13).value = f'=IF(OR(B{r}="",C{r}="",D{r}="",E{r}=""),"",C{r}+E{r}+(6-D{r})+L{r})'
        ws2.cell(r, 14).value = '-' if r == 4 else f'=IF(M{r}="","",RANK(M{r},$M$5:$M$14))'
        ws2.cell(r, 15).value = (f'=IF(M{r}="","",IF(L{r}<5,"Weak first choice",IF(AND(D{r}<=3,C{r}>=3),"Strong candidate","Possible: needs a stronger check")))')
    add_whole(ws2, 'C4:E14', 1, 5, 'Enter a whole number from 1 to 5.')
    add_list(ws2, 'F4:K14', ['Yes', 'No'])
    cf_gold(ws2, 'B4:B14', 'AND(ISNUMBER($L4),$L4>=5)')
    cf_gold(ws2, 'L4:L14', 'AND(ISNUMBER($L4),$L4>=5)')
    cf_red(ws2, 'D4:D14', 'AND(ISNUMBER($D4),$D4>=4)')
    cf_red(ws2, 'O4:O14', '$O4="Weak first choice"')
    note(ws2, 16, 'Tests in order: 1 happens at least weekly; 2 inputs exist as text, files or a sheet; 3 I can check a result in a few minutes; 4 a mistake is caught before a customer or the bank sees it; '
                  '5 one person owns it and will use the result; 6 I can measure it today (time, volume, errors). The example row is not ranked.', 15, 30)
    # sheet 3
    ws3 = wb.create_sheet('Picture')
    setup(ws3, 'Use-Case Scorecard: step 3 of 3, value against risk',
          'Each dot is a task you scored. Across: risk if the result is wrong. Up: value if it works. Start in the top left (high value, low risk). Dots move right when risk is higher; '
          'only go there when you can check results. The grey dot is the NVF example; your tasks appear as black dots when you fill the sheet Score.',
          ['Measure', 'Result'], [34, 56], 22, freeze=False)
    ws3.freeze_panes = None
    for r, (a, b) in enumerate([('Tasks scored', '=COUNT(Score!M5:M14)'),
                                ('Highest priority task', '=IFERROR(INDEX(Score!B5:B14,MATCH(MAX(Score!M5:M14),Score!M5:M14,0)),"No tasks scored yet")'),
                                ('Tasks that pass five or more tests', '=COUNTIF(Score!L5:L14,">=5")')], 4):
        style_row(ws3, r, 2); ws3.cell(r, 1).value = a; ws3.cell(r, 1).font = f(10, True); ws3.cell(r, 2).value = b
    ch = ScatterChart(); ch.style = 2; ch.height = 11.5; ch.width = 20
    ch.title = 'Value against risk for your tasks'
    ch.x_axis.title = 'Risk if the result is wrong (1 = low, 5 = high)'
    ch.y_axis.title = 'Value if it works (1 = low, 5 = high)'
    for ax in (ch.x_axis, ch.y_axis):
        ax.scaling.min = 0; ax.scaling.max = 5; ax.majorUnit = 1; ax.delete = False
        ax.majorGridlines.spPr = GraphicalProperties(); ax.majorGridlines.spPr.line.solidFill = 'D9D9D9'
    ex = Series(Reference(ws2, min_col=3, min_row=4, max_row=4), Reference(ws2, min_col=4, min_row=4, max_row=4), title='NVF example (Monday sales email)')
    ex.marker = Marker('circle', size=10); ex.marker.graphicalProperties = GraphicalProperties(solidFill='A6A6A6'); ex.marker.graphicalProperties.line.solidFill = '767676'
    ex.graphicalProperties = GraphicalProperties(); ex.graphicalProperties.line.noFill = True
    me = Series(Reference(ws2, min_col=3, min_row=5, max_row=14), Reference(ws2, min_col=4, min_row=5, max_row=14), title='My tasks')
    me.marker = Marker('circle', size=10); me.marker.graphicalProperties = GraphicalProperties(solidFill='000000'); me.marker.graphicalProperties.line.solidFill = RED
    me.graphicalProperties = GraphicalProperties(); me.graphicalProperties.line.noFill = True
    # scatter x = risk (col D), y = value (col C)
    ch.series.append(ex); ch.series.append(me)
    ch.legend.position = 'b'
    ws3.add_chart(ch, 'A8'); ws3.page_setup.fitToHeight = 1; ws3.page_setup.orientation = 'portrait'
    save(wb, TEMPLATES / 'Use-Case Scorecard.xlsx')


# ------------------------------------------------ Information Inventory
def inventory():
    name = 'Information Inventory'
    wb = new_wb(name)
    ws = wb.active; ws.title = 'Inventory'
    H = ['#', 'Source (what it is)', 'Owner', 'Format', 'Where it lives', 'Who may see it', 'Sensitivity', 'Ready for AI', 'What to fix first']
    setup(ws, 'Information Inventory: what your task needs to know, and who may see it',
          'Session 14. List every source of information your own task uses, one per row, from row 7. Include the awkward ones: WhatsApp messages, paper files, a spreadsheet on one laptop. If you do not know the owner, write unknown: that is a finding. Aim for at least six sources. '
          'Sensitivity: Public (published), Internal (staff only), Confidential (would hurt if it leaked). Add "+ Personal" to any level when the information names a living person. '
          'Ready for AI: Yes, Fix first (write what to fix) or No (keep it away from AI tools). Then rate the six areas on the sheet Readiness scorecard. See the sheet Key. ' + NVF_NOTE,
          H, [5, 34, 18, 14, 28, 30, 22, 13, 44], 32)
    ex = [
        ['Ex', 'weekly_sales sheet (units and revenue by week, region, product)', 'Sales Manager', 'Spreadsheet', 'Google Drive, folder Sales', 'Directors and sales team', 'Internal', 'Yes', ''],
        ['Ex', 'Supplier agreement with Busoga Oils Ltd', 'Finance Manager', 'Document', 'Drive, folder Contracts (restricted)', 'MD and Finance Manager only', 'Confidential', 'Fix first', 'Nothing says which copy is the signed one. Remove bank details before a copy goes to an AI tool'],
        ['Ex', 'CV pack for the dispatch clerk post', 'HR Officer', 'Text or PDF', 'HR laptop and email', 'HR Officer and hiring manager', 'Confidential + Personal', 'No', 'Keep out of AI tools unless the tool is approved for personal data'],
    ]
    for i, row in enumerate(ex):
        style_row(ws, 4 + i, 9, True, (1, 8)); fill_values(ws, 4 + i, row)
    for r in range(7, 32):
        style_row(ws, r, 9, False, (1, 8)); ws.cell(r, 1).value = r - 6
    add_list(ws, 'D4:D31', ['Spreadsheet', 'Document', 'Text or PDF', 'Scan or photo', 'Email', 'Messages', 'Database', 'Paper', 'Other'])
    add_list(ws, 'G4:G31', SENS)
    add_list(ws, 'H4:H31', ['Yes', 'Fix first', 'No'])
    cf_red(ws, 'G4:G31', 'ISNUMBER(SEARCH("Personal",$G4))')
    cf_red(ws, 'H4:H31', '$H4="No"')
    cf_gold(ws, 'H4:H31', '$H4="Fix first"')
    # readiness scorecard
    wr = wb.create_sheet('Readiness scorecard')
    setup(wr, 'Readiness scorecard: six areas, each Green, Amber or Red',
          'Session 14. Look at your Inventory rows for each area, rate it Green, Amber or Red by the rule in the table, and write one line of evidence that names the file or fact behind the rating. '
          'Green scores 2, Amber 1, Red 0, so the total is out of 12. Amber means usable after a named fix. Be strict on rights: if you do not know who may see a source, or whether it holds personal data, it is Red until someone confirms. '
          'The total is a conversation starter. Then choose your top three data gaps below. The NVF columns show the worked example from the Session 14 slides. ' + NVF_NOTE,
          ['Area', 'Green when', 'Red when', 'NVF example rating', 'NVF example reason', 'My rating', 'Points', 'My reason (evidence)'],
          [22, 32, 32, 12, 40, 11, 9, 46], 32)
    areas = [
        ('Inventory', 'A written list with owners', 'No list; files on personal phones', 'Amber', 'Files are known. Assumed: no list covers WhatsApp orders or the accounting package.'),
        ('Readable', 'Text can be selected and copied', 'Paper, photos, faint scans', 'Green', 'Everything is text or CSV. No scans.'),
        ('Complete and unique', 'One current copy, no gaps', 'Copies disagree; rows missing', 'Amber', 'Sales grid is complete. Invoices have 8 faults in 60 rows.'),
        ('Metadata', 'Date, owner and version on each file', 'Names such as "final2"', 'Amber', 'Handbook has version, date, owner. The data files have none.'),
        ('Rights', 'Who may use it is written down', 'Unknown; personal data unchecked', 'Red', 'Phones and CVs are personal data. Handbook 4.4 needs written tool approval; assumed none on file.'),
        ('Current', 'Updated on a set schedule', 'Nobody knows the latest version', 'Amber', 'Handbook is dated. Two agreement copies; market notes differ.'),
    ]
    for i, (a, g, rd, rt, why) in enumerate(areas, 4):
        style_row(wr, i, 8, False, (4, 6, 7)); fill_values(wr, i, [a, g, rd, rt, why])
        wr.cell(i, 1).font = f(10, True)
        for c in (4, 5):
            wr.cell(i, c).font = F_EX
        wr.cell(i, 7).value = f'=IF(F{i}="Green",2,IF(F{i}="Amber",1,IF(F{i}="Red",0,"")))'
        wr.row_dimensions[i].height = 30
    style_row(wr, 10, 8, False, (4, 6, 7))
    wr.cell(10, 1).value = 'Total (Green 2, Amber 1, Red 0)'; wr.cell(10, 1).font = f(10, True)
    wr.cell(10, 4).value = '6 of 12'; wr.cell(10, 4).font = F_EX
    wr.cell(10, 5).value = 'NVF example total, with one Red on rights.'; wr.cell(10, 5).font = F_EX
    wr.cell(10, 7).value = '=IF(COUNT(G4:G9)=6,SUM(G4:G9),"")'; wr.cell(10, 7).font = f(10, True)
    wr.cell(10, 8).value = '=IF(G10="","Rate all six areas to see your total of 12.","My total: "&G10&" of 12. Red areas: "&COUNTIF(F4:F9,"Red")&". Amber areas: "&COUNTIF(F4:F9,"Amber")&".")'
    wr.row_dimensions[10].height = 30
    add_list(wr, 'F4:F9', ['Green', 'Amber', 'Red'])
    cf_red(wr, 'F4:F9', '$F4="Red"'); cf_gold(wr, 'F4:F9', '$F4="Amber"')
    wr.conditional_formatting.add('F4:F9', FormulaRule(formula=['$F4="Green"'], font=Font(name=FONT, bold=True, color='000000')))
    # top three gaps
    wr.cell(12, 1).value = 'My top three data gaps'; wr.cell(12, 1).font = f(11, True)
    wr.cell(13, 1).value = 'Pick the three Red or Amber areas that block your task most. For each write the evidence, one first fix that a person could finish in days, and who could own it. Session 14 turns these lines into your data roadmap.'
    wr.merge_cells(start_row=13, start_column=1, end_row=13, end_column=8)
    wr.cell(13, 1).font = f(9.5); wr.cell(13, 1).alignment = Alignment(wrap_text=True, vertical='top'); wr.row_dimensions[13].height = 28
    for i, h in enumerate(['Gap', 'Evidence', 'First fix', 'Possible owner'], 1):
        c = wr.cell(14, i); c.value = h; c.font = F_HEAD; c.fill = BLACKFILL; c.alignment = Alignment(wrap_text=True, vertical='center')
    wr.row_dimensions[14].height = 22
    gaps = [('1 Rights', 'Customer phones and CVs; no tool approval on file', 'Managing Director names one approved tool; the lawyer checks the 2019 Act duties', 'Managing Director'),
            ('2 Faulty invoices', '8 faults in 60 rows', 'Finance Manager fixes the file and keeps one current copy', 'Finance Manager'),
            ('3 No definitions', 'The CSV files carry no definitions or owner', 'Sales Manager writes a one-page data dictionary', 'Sales Manager')]
    for k, row in enumerate(gaps):
        r = 15 + k; style_row(wr, r, 4, True); fill_values(wr, r, list(row)); wr.row_dimensions[r].height = 30
    for k in range(3):
        r = 18 + k; style_row(wr, r, 4, False); wr.cell(r, 1).value = None; wr.row_dimensions[r].height = 30
    style_row(wr, 21, 4); wr.cell(21, 1).value = 'The gap I will fix first, and why'; wr.cell(21, 1).font = f(10, True)
    wr.merge_cells(start_row=21, start_column=2, end_row=21, end_column=4); wr.cell(21, 2).border = INPUT_BORDER; wr.row_dimensions[21].height = 30
    # counts from the inventory
    wr.cell(23, 1).value = 'From the Inventory sheet'; wr.cell(23, 1).font = f(11, True)
    style_row(wr, 24, 2); wr.cell(24, 1).value = 'Sources listed (number)'; wr.cell(24, 2).value = '=COUNTA(Inventory!B7:B31)'
    style_row(wr, 25, 2); wr.cell(25, 1).value = 'Sources labelled Confidential or + Personal (number)'; wr.cell(25, 2).value = '=SUMPRODUCT(--((ISNUMBER(SEARCH("Confidential",Inventory!G7:G31))+ISNUMBER(SEARCH("Personal",Inventory!G7:G31)))>0))'
    style_row(wr, 26, 2); wr.cell(26, 1).value = 'Sources marked Ready for AI: No (number)'; wr.cell(26, 2).value = '=COUNTIF(Inventory!H7:H31,"No")'
    for r in (24, 25, 26):
        wr.cell(r, 1).font = f(10, True); wr.cell(r, 2).alignment = Alignment(horizontal='left'); wr.row_dimensions[r].height = 28
    wr.freeze_panes = None
    # samples
    ws2 = wb.create_sheet('Sample inputs')
    H2 = ['#', 'Sample input (a small piece you may paste into an AI tool)', 'Taken from source', 'Sensitivity', 'Real or invented', 'Identifiers removed?', 'Where saved']
    setup(ws2, 'Sample inputs: three safe pieces to test with (optional)',
          'Optional, for learners who finish early. Prepare three small sample inputs for your own task. Mark the sensitivity of each. Replace names, numbers and contact details with invented ones before any AI tool sees them. ' + NVF_NOTE,
          H2, [5, 50, 30, 14, 16, 16, 30], 32)
    style_row(ws2, 4, 7, True, (1, 4, 5, 6)); fill_values(ws2, 4, ['Ex', 'Two weeks of weekly_sales rows for the Jinja and Mbale regions (24 rows)', 'weekly_sales sheet', 'Internal', 'Invented', 'Not needed', 'Drive, folder Samples'])
    for r in range(5, 8):
        style_row(ws2, r, 7, False, (1, 4, 5, 6)); ws2.cell(r, 1).value = r - 4
    add_list(ws2, 'D4:D7', SENS); add_list(ws2, 'E4:E7', ['Real', 'Invented', 'Real, edited']); add_list(ws2, 'F4:F7', ['Yes', 'No', 'Not needed'])
    cf_red(ws2, 'D4:D7', 'ISNUMBER(SEARCH("Personal",$D4))')
    # key
    ws3 = wb.create_sheet('Key')
    setup(ws3, 'Key: what the levels mean', 'Use these meanings so that everyone in the company labels information the same way.', ['Term', 'Meaning', 'Example'], [22, 70, 50], 22)
    rows = [('Public', 'Already published or meant for anyone.', 'Price list on the website'), ('Internal', 'For staff. Little harm if it leaks, but not for outsiders.', 'Weekly sales summary'),
            ('Confidential', 'Would harm the company if it leaked: contracts, finances, plans.', 'Supplier agreement, bank details'),
            ('+ Personal', 'A flag added to any level when the information identifies a living person. In Uganda the Data Protection and Privacy Act, 2019 applies. Treat it by the stricter rule. Not legal advice: ask your lawyer.', 'CVs and payroll (Confidential + Personal), customer phone numbers (Internal + Personal)'),
            ('Ready: Yes', 'Safe and good enough to use with an approved AI tool today.', ''), ('Ready: Fix first', 'Usable after a named fix (clean, remove identifiers, agree one version).', ''),
            ('Ready: No', 'Keep away from AI tools for now.', ''),
            ('Green', 'The rule for that area is met today. Scores 2.', 'Readable: text can be selected and copied'),
            ('Amber', 'Usable after a named fix. Scores 1.', 'Metadata: only the handbook is dated'),
            ('Red', 'The rule is not met, or nobody can say. Scores 0.', 'Rights: no tool approval on file')]
    for i, r in enumerate(rows, 4):
        style_row(ws3, i, 3); fill_values(ws3, i, r); ws3.cell(i, 1).font = f(10, True)
    save(wb, TEMPLATES / 'Information Inventory.xlsx')


# --------------------------------------------------- Document Review
def review():
    name = 'Document Review Table'
    wb = new_wb(name)
    ws = wb.active; ws.title = 'Review'
    H = ['#', 'Issue', 'Document', 'Clause or line', 'What the document says', 'What our rule says', 'Risk (H/M/L)', 'Source quote (word for word)', 'Decision', 'Owner', 'Reason or next step']
    setup(ws, 'Document Review Table: every issue linked to its source',
          'One row for each issue the AI or you find in a document. Copy the source quote word for word from the document (search for it with Ctrl+F: if you cannot find it, do not rely on it). '
          'Risk: H = could cost money or break the law, M = needs a change, L = acceptable. Decision: Accept, Negotiate or Escalate (a person with more authority decides). Counts appear on the sheet Summary. '
          'The example rows are for the NVF agreement with Busoga Oils (supplier_agreement_busoga_oils) and the NVF review playbook: the quotes are the exact words of the agreement. ' + NVF_NOTE,
          H, [5, 24, 22, 12, 36, 36, 9, 44, 12, 16, 34], 32)
    ex = [
        ['Ex', 'Automatic renewal', 'Busoga Oils supply agreement', 'Clause 8', 'Renews for 12 months unless written notice of non-renewal is given at least 90 days before the end of the period. Playbook P6 allows 30 days at most.', 'P6: notice to stop renewal of no more than 30 days. Diary the notice date.', 'H',
         '"It then renews automatically for further periods of 12 months unless one party gives the other written notice of non-renewal at least 90 days before the end of the current period."', 'Negotiate', 'Finance Manager', 'Ask for 30 days or less. Diary the notice date.'],
        ['Ex', 'Price change', 'Busoga Oils supply agreement', 'Clause 3', 'The Supplier decides price changes alone, and they reach orders already confirmed. Playbook P3 needs 30 days notice and a cap of 5% in 12 months.', 'P3: at least 30 days written notice, a cap of 5% in any 12 months, no effect on confirmed orders.', 'H',
         '"The Supplier may change any price at its sole discretion by telling NVF in writing, and the new price applies to every order not yet delivered, including orders NVF has already confirmed."', 'Negotiate', 'Finance Manager', 'Ask for 30 days notice, a 5% yearly cap and no change to confirmed orders.'],
        ['Ex', 'Liability cap', 'Busoga Oils supply agreement', 'Clause 10', 'Supplier liability is capped at 3 months of fees, including for contaminated or unsafe goods. Playbook P8 needs at least 12 months of fees and no cap for unsafe goods.', 'P8: cap of at least 12 months of fees. No cap for unsafe or contaminated goods, fraud or data breach.', 'H',
         '"The total liability of the Supplier to NVF under or in connection with this agreement, for any cause, is limited to the fees NVF paid in the 3 months before the claim arose."', 'Escalate', 'Managing Director', 'Needs the MD and a lawyer.'],
    ]
    for i, row in enumerate(ex):
        style_row(ws, 4 + i, 11, True, (1, 4, 7, 9)); fill_values(ws, 4 + i, row)
    for r in range(7, 32):
        style_row(ws, r, 11, False, (1, 4, 7, 9)); ws.cell(r, 1).value = r - 6
    add_list(ws, 'G4:G31', ['H', 'M', 'L']); add_list(ws, 'I4:I31', ['Accept', 'Negotiate', 'Escalate'])
    cf_red(ws, 'G4:G31', '$G4="H"'); cf_gold(ws, 'I4:I31', '$I4="Escalate"')
    ws2 = wb.create_sheet('Summary')
    setup(ws2, 'Summary of the review', 'Counts update from the sheet Review. The three grey example rows are not counted.', ['Measure', 'Count'], [40, 14], 22)
    items = [('Issues recorded', '=COUNTA(Review!B7:B31)'), ('Risk H', '=COUNTIF(Review!G7:G31,"H")'), ('Risk M', '=COUNTIF(Review!G7:G31,"M")'), ('Risk L', '=COUNTIF(Review!G7:G31,"L")'),
             ('Decision Accept', '=COUNTIF(Review!I7:I31,"Accept")'), ('Decision Negotiate', '=COUNTIF(Review!I7:I31,"Negotiate")'), ('Decision Escalate', '=COUNTIF(Review!I7:I31,"Escalate")'),
             ('Issues with no source quote (fix these)', '=COUNTA(Review!B7:B31)-COUNTA(Review!H7:H31)'),
             ('High risk issues with no decision yet', '=COUNTIFS(Review!G7:G31,"H",Review!I7:I31,"")')]
    for i, (a, b) in enumerate(items, 4):
        style_row(ws2, i, 2, False, (2,)); ws2.cell(i, 1).value = a; ws2.cell(i, 2).value = b
    cf_red(ws2, 'B11:B12', 'B11>0')
    save(wb, TEMPLATES / 'Document Review Table.xlsx')


# --------------------------------------------------- Automation Test Log
def testlog():
    name = 'Automation Test Log'
    wb = new_wb(name)
    ws = wb.active; ws.title = 'Test log'
    H = ['Test id', 'Date', 'Input (what I gave it)', 'Expected result', 'Actual result', 'Result (computed)', 'Error type', 'Minutes by hand', 'Minutes to start', 'Minutes to review', 'Minutes with the new routine (computed)', 'Minutes saved (computed)', 'Notes']
    setup(ws, 'Test Log: record each check of your chosen workflow',
          'Optional, for any workflow you choose to try after the course. Run each test, then write the input, what you expected and what you got. Keep the expected and actual results short (a category, a number, Yes or No) so the sheet can compare them: Pass when they match, Fail when they differ. '
          'If a test fails, pick the error type. Write how long the same job takes by hand, how long it takes you to start the new routine, and how long you take to review its result. Minutes with the new routine is start plus review, and the sheet works it out. The sheet Summary shows the pass rate, the review time and the minutes saved. Rows 4 and 5 are grey examples and are not counted. ' + NVF_NOTE,
          H, [9, 12, 38, 22, 22, 13, 20, 12, 11, 12, 15, 14, 38], 32)
    ex = [['Ex1', '2026-11-16', 'Message 14: "Thank you, the oil arrived on time. Please do not be late next Friday."', 'Order', 'Order', None, 'None', 2, 0.1, 0.1, None, None, 'Rule would have said Complaint'],
          ['Ex2', '2026-11-16', 'Invoice INV-0031, total UGX 1,180,000 (qty 20 x UGX 50,000 plus 18% VAT)', 'Flag: wrong total', 'No flag', None, 'Missed item', 3, 0.1, 0.2, None, None, 'VAT was added twice; the check missed it. Add a rule.']]
    for i, row in enumerate(ex):
        style_row(ws, 4 + i, 13, True, (1, 2, 6, 8, 9, 10, 11, 12), {2: 'yyyy-mm-dd', 8: '0.0', 9: '0.0', 10: '0.0', 11: '0.0', 12: '0.0'}); fill_values(ws, 4 + i, row)
    import datetime
    ws.cell(4, 2).value = datetime.date(2026, 11, 16); ws.cell(5, 2).value = datetime.date(2026, 11, 16)
    for r in range(6, 36):
        style_row(ws, r, 13, False, (1, 2, 6, 8, 9, 10, 11, 12), {2: 'yyyy-mm-dd', 8: '0.0', 9: '0.0', 10: '0.0', 11: '0.0', 12: '0.0'}); ws.cell(r, 1).value = f'T{r - 5:02d}'
    for r in range(4, 36):
        ws.cell(r, 6).value = f'=IF(OR(D{r}="",E{r}=""),"",IF(LOWER(TRIM(D{r}))=LOWER(TRIM(E{r})),"Pass","Fail"))'
        ws.cell(r, 11).value = f'=IF(OR(I{r}="",J{r}=""),"",I{r}+J{r})'
        ws.cell(r, 12).value = f'=IF(OR(H{r}="",K{r}=""),"",H{r}-K{r})'
    types = ['None', 'Wrong answer', 'Missing item', 'Invented item', 'Wrong format', 'Wrong recipient', 'Blocked by permission', 'Timeout or quota', 'Other']
    add_list(ws, 'G4:G35', types); add_decimal(ws, 'H4:J35', 0); add_date(ws, 'B4:B35')
    cf_red(ws, 'F4:F35', '$F4="Fail"')
    ws2 = wb.create_sheet('Summary')
    setup(ws2, 'Summary: pass rate, minutes saved, errors found',
          'Everything here is calculated from the sheet Test log (rows 6 to 35; the two grey examples are not counted). Type your target in the one input cell before you test, so that you cannot move the goalposts afterwards.',
          ['Measure', 'Value', 'How it is worked out'], [44, 16, 70], 22)
    rows = [
        ('Tests run', "=COUNTIF('Test log'!F6:F35,\"Pass\")+COUNTIF('Test log'!F6:F35,\"Fail\")", 'Tests with both an expected and an actual result', '0'),
        ('Tests passed', "=COUNTIF('Test log'!F6:F35,\"Pass\")", '', '0'),
        ('Tests failed', "=COUNTIF('Test log'!F6:F35,\"Fail\")", '', '0'),
        ('Pass rate', '=IF(B4=0,"",B5/B4)', 'Passed divided by run', '0%'),
        ('Average minutes saved per test', "=IF(COUNT('Test log'!L6:L35)=0,\"\",AVERAGE('Test log'!L6:L35))", 'Minutes by hand minus minutes with the new routine (start plus review)', '0.0'),
        ('Total minutes saved in these tests', "=IF(COUNT('Test log'!L6:L35)=0,\"\",SUM('Test log'!L6:L35))", '', '0.0'),
        ('Average minutes to review per test', "=IF(COUNT('Test log'!J6:J35)=0,\"\",AVERAGE('Test log'!J6:J35))", 'The time you spend checking each result. Review time is a cost, so it is inside minutes with the new routine', '0.0'),
        ('Time cut compared with doing it by hand', "=IF(SUM('Test log'!H6:H35)=0,\"\",1-SUM('Test log'!K6:K35)/SUM('Test log'!H6:H35))", 'Minutes with the new routine (start plus review) as a share of minutes by hand', '0%'),
        ('Errors found', "=COUNTA('Test log'!G6:G35)-COUNTIF('Test log'!G6:G35,\"None\")", 'Tests where an error type other than None was recorded', '0'),
        ('Pass rate I need before relying on it', 0.9, 'Your target. Type it before you start testing.', '0%'),
        ('Do we meet the target?', '=IF(B4=0,"",IF(B7>=B13,"Yes","Not yet"))', '', '@'),
    ]
    for i, (a, b, c, nf) in enumerate(rows, 4):
        style_row(ws2, i, 3, False, (2,)); ws2.cell(i, 1).value = a; ws2.cell(i, 2).value = b; ws2.cell(i, 3).value = c; ws2.cell(i, 2).number_format = nf
        ws2.cell(i, 1).font = f(10, True)
    ws2.cell(13, 2).font = F_EX; ws2.cell(13, 2).border = INPUT_BORDER
    cf_red(ws2, 'B14', '$B$14="Not yet"')
    ws2.cell(16, 1).value = 'Errors by type'; ws2.cell(16, 1).font = f(11, True)
    for j, t in enumerate(types[1:]):
        r = 17 + j; style_row(ws2, r, 2, False, (2,)); ws2.cell(r, 1).value = t
        ws2.cell(r, 2).value = f"=COUNTIF('Test log'!G6:G35,A{r})"
    save(wb, TEMPLATES / 'Automation Test Log.xlsx')


# ------------------------------------------------------- Risk Register
def risk():
    name = 'Risk Register'
    wb = new_wb(name)
    ws = wb.active; ws.title = 'Register'
    H = ['#', 'Risk', 'Cause', 'Effect', 'Likelihood 1-5', 'Impact 1-5', 'Score', 'Level', 'Owner', 'Control', 'Residual risk (after the control)']
    setup(ws, 'Risk Register: what could go wrong with your own task',
          'Session 13. The eight grey rows are typical AI risks. Edit each one for your own task, delete what does not apply, then add a ninth row for over-reliance (trusting results because they are usually right, and checking less and less) and any risk of your own. Likelihood: how likely in the next year (1 rare, 5 almost certain). Impact: how bad if it happens (1 small, 5 severe). '
          'Score is Likelihood x Impact; Level is High from 15, Medium from 8 to 14, Low below 8. Name one owner and one real control for every row: a control is an action a person does, and a row without an owner and a control is only a worry. Scales are on the sheet Scale.',
          H, [5, 24, 36, 36, 11, 10, 10, 10, 20, 46, 14], 34)
    seeds = [
        ('Data leakage', 'Staff paste customer or contract data into a free AI account.', 'Personal or confidential data leaves the company and the provider may keep it.', 3, 5, 'Managing Director',
         'Approved tools only, and a data table in the policy. No personal data in free or personal accounts.', 'Medium'),
        ('Wrong answer', 'The AI misreads or invents a figure or fact.', 'A wrong number reaches a customer, the bank or the board.', 4, 4, 'Task owner',
         'A named reviewer checks figures and quotes against the source before anything is released.', 'Medium'),
        ('Prompt injection', 'Prompt injection: an incoming email or document hides an instruction that the tool follows.', 'The tool shares data or takes an action nobody approved.', 3, 4, 'Operations Manager',
         'The tool drafts, and a person approves every send. Treat incoming text as data.', 'Medium'),
        ('Over-broad permission', 'A tool or assistant is connected with full access to a mailbox or drive.', 'One fault or stolen key exposes everything in that account.', 3, 5, 'Finance Manager',
         'Give each tool its own narrow access, read-only where possible. Record it on the Tool Boundary Sheet.', 'Low'),
        ('Cost runaway', 'A loop or repeated retry calls a paid service again and again.', 'An unexpected bill.', 3, 3, 'Finance Manager',
         'Limit the number of calls and the monthly spend. Alerts on usage. One run a day at most.', 'Low'),
        ('Bias', 'The tool learned patterns from past data, for example when it shortlists people.', 'Unfair treatment of candidates or customers; legal and trust damage.', 3, 4, 'HR Officer',
         'A person decides on people. Check results by group. No decision about a person from AI alone.', 'Medium'),
        ('Vendor lock-in', 'Workflows are built in one vendor format and data cannot be moved.', 'A price rise or closure leaves us unable to leave.', 3, 3, 'Finance Manager',
         'Keep exports of data and settings. Describe each process in plain words. Ask about exit before signing.', 'Medium'),
        ('Staff leave with the only knowledge', 'One person knows how the AI workflow is set up.', 'It breaks and nobody can fix or stop it.', 4, 3, 'Managing Director',
         'Written runbook. A second named owner. Two people know where the off switch is.', 'Low'),
    ]
    for i, (a, b, c, l, im, o, ctl, res) in enumerate(seeds):
        r = 4 + i; style_row(ws, r, 11, True, (1, 5, 6, 7, 8, 11)); fill_values(ws, r, [i + 1, a, b, c, l, im, None, None, o, ctl, res])
    for r in range(12, 32):
        style_row(ws, r, 11, False, (1, 5, 6, 7, 8, 11)); ws.cell(r, 1).value = r - 3
    for r in range(4, 32):
        ws.cell(r, 7).value = f'=IF(OR(E{r}="",F{r}=""),"",E{r}*F{r})'
        ws.cell(r, 8).value = f'=IF(G{r}="","",IF(G{r}>=15,"High",IF(G{r}>=8,"Medium","Low")))'
    add_whole(ws, 'E4:F31', 1, 5); add_list(ws, 'K4:K31', ['High', 'Medium', 'Low'])
    cf_red(ws, 'H4:H31', '$H4="High"'); cf_gold(ws, 'H4:H31', '$H4="Medium"'); cf_red(ws, 'K4:K31', '$K4="High"')
    ws2 = wb.create_sheet('Scale')
    setup(ws2, 'Scale: how to score', 'Use the same scales every time so that scores can be compared between risks and between months.', ['Score', 'Likelihood (in the next 12 months)', 'Impact (if it happens)'], [10, 52, 62], 22)
    sc = [(1, 'Rare: we cannot see how it would happen', 'Small: a few minutes of rework'), (2, 'Unlikely: could happen once in several years', 'Minor: a wrong item caught inside the team'),
          (3, 'Possible: could happen this year', 'Moderate: a customer or supplier notices; money lost but recoverable'),
          (4, 'Likely: has happened to similar companies', 'Major: significant money, a customer lost, or a regulator contacted'),
          (5, 'Almost certain: expect it without a control', 'Severe: serious harm to people, a large loss, or legal action')]
    for i, row in enumerate(sc, 4):
        style_row(ws2, i, 3, False, (1,)); fill_values(ws2, i, row)
    ws2.cell(10, 1).value = 'Level'; ws2.cell(10, 1).font = f(11, True)
    for i, (a, b) in enumerate([('High', 'Score 15 to 25. Needs a control and the owner reports it to the MD.'), ('Medium', 'Score 8 to 14. Needs a control and a review date.'), ('Low', 'Score 1 to 7. Accept and watch.')], 11):
        style_row(ws2, i, 3); ws2.cell(i, 1).value = a; ws2.cell(i, 2).value = b
    ws2.cell(15, 1).value = 'Count'; ws2.cell(15, 1).font = f(11, True)
    for i, lv in enumerate(['High', 'Medium', 'Low'], 16):
        style_row(ws2, i, 3); ws2.cell(i, 1).value = lv; ws2.cell(i, 2).value = f'=COUNTIF(Register!H4:H31,A{i})'; ws2.cell(i, 2).alignment = Alignment(horizontal='left')
    save(wb, TEMPLATES / 'Risk Register.xlsx')


if __name__ == '__main__':
    scorecard(); inventory(); review(); testlog(); risk()
    import gen_xlsx2
    gen_xlsx2.run()
