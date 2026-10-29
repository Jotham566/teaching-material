"""Workpiece templates for Enterprise Data Readiness for AI. openpyxl with live formulas, Calibri 11, hairline borders,
frozen headers, drop-downs, and one light tint for cells the learner fills in. No other fills."""
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter as L

F = Font(name="Calibri", size=11)
FB = Font(name="Calibri", size=11, bold=True)
FT = Font(name="Calibri", size=14, bold=True)
FI = Font(name="Calibri", size=11, italic=True, color="595959")
HAIR = Side(style="hair", color="808080")
THIN = Side(style="thin", color="404040")
INPUT = PatternFill("solid", fgColor="FFF8E5")
WRAP = Alignment(wrap_text=True, vertical="top")
LEVELS = ["Ad hoc", "Developing", "Defined", "Managed", "Optimised"]
DIMS = ["Use cases and sponsorship", "Data: inventory, quality and metadata", "Platform and pipelines", "Protection and law", "People and governance"]


def cell(ws, ref, value=None, font=F, wrap=False, fmt=None, inp=False, align=None):
    c = ws[ref]
    if value is not None:
        c.value = value
    c.font = font
    if wrap:
        c.alignment = WRAP
    if align:
        c.alignment = align
    if fmt:
        c.number_format = fmt
    if inp:
        c.fill = INPUT
    return c


def header_row(ws, row, labels, start_col=1):
    for j, h in enumerate(labels, start=start_col):
        c = ws.cell(row, j, h)
        c.font = FB
        c.alignment = Alignment(wrap_text=True, vertical="bottom")
        c.border = Border(bottom=THIN)


def hair(ws, r1, r2, c1, c2):
    for r in range(r1, r2 + 1):
        for c in range(c1, c2 + 1):
            x = ws.cell(r, c)
            x.border = Border(bottom=HAIR)
            if x.font is None or x.font.name != "Calibri":
                x.font = F


def widths(ws, ws_widths):
    for i, w in enumerate(ws_widths, start=1):
        ws.column_dimensions[L(i)].width = w


def dv_list(ws, items, rng, allow_blank=True, title=None, msg=None):
    d = DataValidation(type="list", formula1='"' + ",".join(items) + '"', allow_blank=allow_blank, showDropDown=False)
    if msg:
        d.error = msg
        d.errorTitle = title or "Not allowed"
    ws.add_data_validation(d)
    d.add(rng)
    return d


def instructions(wb, title, lines):
    ws = wb.active
    ws.title = "Instructions"
    ws.sheet_view.showGridLines = False
    cell(ws, "A1", title, FT)
    r = 3
    for ln in lines:
        c = cell(ws, f"A{r}", ln, F, wrap=True)
        r += 1
    cell(ws, f"A{r + 1}", "Cells with a light cream tint are for your input. All other cells are formulas or fixed text.", FI, wrap=True)
    ws.column_dimensions["A"].width = 100
    for rr in range(3, r + 2):
        ws.row_dimensions[rr].height = None
    return ws


def base_wb(title, lines):
    wb = Workbook()
    instructions(wb, title, lines)
    return wb


# ------------------------------------------------------------------ Readiness Scorecard
def readiness_scorecard(path, filled=None, title="Readiness Scorecard"):
    """filled: DataFrame with dimension, item, what_exists, who_could_verify, proposed_score, self_reported (for the Kitara copy)."""
    wb = base_wb(f"{title}: Enterprise Data Readiness for AI", [
        "Score your organisation on five dimensions. Each dimension has up to six evidence rows.",
        "1. Write one piece of evidence per row (a document, a report, a system screen) and name the person who could verify it.",
        "2. Give the item a score from 1 to 5. The Levels guide sheet describes each level.",
        "3. Set Evidence seen to Y only when someone outside your team has seen the evidence. Leave it N when the score rests on what someone told you.",
        "4. Read the summary under the table. The evidence-adjusted mean counts only the rows with Evidence seen = Y.",
        "5. Set a target level for each dimension. The gap shows how far each dimension has to move.",
        "Do not score a row without evidence. A blank row is better than a guess.",
    ])
    lv = wb.create_sheet("Levels guide")
    header_row(lv, 1, ["Level", "Name", "What it looks like", "Evidence you would expect"])
    guide = [
        (1, "Ad hoc", "Done by individuals when needed. Nothing written down. Different answers from different people.", "A person's account only. No documents."),
        (2, "Developing", "Some written practice in some places. Not applied across the organisation.", "A document or list that covers part of the organisation, with gaps you can name."),
        (3, "Defined", "A standard exists and most units know it. Owners are named. Gaps are known.", "An approved policy, a complete list, a named owner, one report that uses them."),
        (4, "Managed", "The standard is measured. Someone reviews the numbers and acts on them.", "Monthly figures, a log of actions, minutes showing decisions."),
        (5, "Optimised", "The measures drive regular improvement. Changes are tested before they are rolled out.", "A year of trend data and a record of improvements made from it."),
    ]
    for i, r in enumerate(guide, start=2):
        for j, v in enumerate(r, start=1):
            c = lv.cell(i, j, v)
            c.font = F
            c.alignment = WRAP
            c.border = Border(bottom=HAIR)
    widths(lv, [8, 14, 60, 60])
    lv.freeze_panes = "A2"

    ws = wb.create_sheet("Scorecard", 1)
    ws.sheet_view.showGridLines = False
    cell(ws, "A1", f"{title}", FT)
    cell(ws, "A2", "Organisation:", FB)
    cell(ws, "B2", "Kitara Group (fictional)" if filled is not None else None, inp=True)
    cell(ws, "D2", "Date scored:", FB)
    cell(ws, "E2", "2026-10-29" if filled is not None else None, inp=True)
    hdr = ["Dimension", "Evidence item", "What exists (the evidence)", "Who could verify it", "Score (1 to 5)", "Evidence seen (Y/N)", "Level name"]
    header_row(ws, 4, hdr)
    ROWS = 6
    r = 5
    first = r
    for d in DIMS:
        sub = None if filled is None else filled[filled.dimension == d].reset_index(drop=True)
        for k in range(ROWS):
            ws.cell(r, 1, d).font = F
            ws.cell(r, 1).alignment = WRAP
            vals = [None, None, None, None, None]
            if sub is not None and k < len(sub):
                x = sub.loc[k]
                vals = [x["item"], x["what_exists"], x["who_could_verify"], int(x["proposed_score"]), "N" if x["self_reported"] == "Y" else "Y"]
            for j, v in enumerate(vals, start=2):
                c = ws.cell(r, j, v)
                c.font = F
                c.fill = INPUT
                c.alignment = WRAP
            g = ws.cell(r, 7, f'=IF(E{r}="","",INDEX(\'Levels guide\'!$B$2:$B$6,E{r}))')
            g.font = F
            for j in range(1, 8):
                ws.cell(r, j).border = Border(bottom=HAIR)
            r += 1
    last = r - 1
    dv_list(ws, ["1", "2", "3", "4", "5"], f"E{first}:E{last}", msg="Enter a whole number from 1 to 5.", title="Score")
    dv_list(ws, ["Y", "N"], f"F{first}:F{last}", msg="Enter Y or N.", title="Evidence seen")
    # summary
    s0 = last + 3
    cell(ws, f"A{s0 - 1}", "Summary", FB)
    header_row(ws, s0, ["Dimension", "Items scored", "Mean score", "Evidence-adjusted mean", "Target level (1 to 5)", "Gap to target (adjusted)", "Weakest?"])
    for i, d in enumerate(DIMS):
        rr = s0 + 1 + i
        ws.cell(rr, 1, d).font = F
        ws.cell(rr, 2, f'=COUNTIFS($A${first}:$A${last},A{rr},$E${first}:$E${last},">0")').font = F
        c = ws.cell(rr, 3, f'=IFERROR(AVERAGEIFS($E${first}:$E${last},$A${first}:$A${last},A{rr}),"")')
        c.number_format = "0.00"
        c.font = F
        c = ws.cell(rr, 4, f'=IFERROR(AVERAGEIFS($E${first}:$E${last},$A${first}:$A${last},A{rr},$F${first}:$F${last},"Y"),"")')
        c.number_format = "0.00"
        c.font = F
        t = ws.cell(rr, 5, 3)
        t.font = F
        t.fill = INPUT
        c = ws.cell(rr, 6, f'=IF(D{rr}="","",MAX(0,E{rr}-D{rr}))')
        c.number_format = "0.00"
        c.font = F
        ws.cell(rr, 7, f'=IF(AND(D{rr}<>"",D{rr}=MIN($D${s0 + 1}:$D${s0 + 5})),"Weakest","")').font = F
        for j in range(1, 8):
            ws.cell(rr, j).border = Border(bottom=HAIR)
    a, b = s0 + 1, s0 + 5
    dv_list(ws, ["1", "2", "3", "4", "5"], f"E{a}:E{b}", msg="Enter a whole number from 1 to 5.", title="Target level")
    o = b + 2
    cell(ws, f"A{o}", "Overall mean score", FB)
    c = cell(ws, f"C{o}", f'=IFERROR(AVERAGE(C{a}:C{b}),"")', fmt="0.00")
    cell(ws, f"A{o + 1}", "Overall evidence-adjusted mean", FB)
    cell(ws, f"D{o + 1}", f'=IFERROR(AVERAGE(D{a}:D{b}),"")', fmt="0.00")
    cell(ws, f"A{o + 2}", "Overall level (adjusted, rounded)", FB)
    cell(ws, f"D{o + 2}", f'=IFERROR(INDEX(\'Levels guide\'!$B$2:$B$6,ROUND(D{o + 1},0)),"")')
    cell(ws, f"A{o + 3}", "Weakest dimension (adjusted mean)", FB)
    cell(ws, f"D{o + 3}", f'=IFERROR(INDEX(A{a}:A{b},MATCH(MIN(D{a}:D{b}),D{a}:D{b},0)),"")')
    cell(ws, f"A{o + 4}", "Largest gap to target", FB)
    cell(ws, f"D{o + 4}", f'=IFERROR(INDEX(A{a}:A{b},MATCH(MAX(F{a}:F{b}),F{a}:F{b},0)),"")')
    widths(ws, [36, 30, 52, 30, 14, 16, 14])
    ws.freeze_panes = "C5"
    wb.save(path)
    return dict(first=first, last=last, s0=s0, overall_row=o)


# ------------------------------------------------------------------ Use Case Canvas
def use_case_canvas(path):
    wb = base_wb("Use Case Canvas", [
        "Fill one column for each AI use case. Start with the problem and the person who feels it, then list the data it needs.",
        "Priority is value divided by effort. A high number means a good first use.",
        "Ask two questions of every data line: where does it live, and who owns it?",
    ])
    ws = wb.create_sheet("Canvas", 1)
    ws.sheet_view.showGridLines = False
    cell(ws, "A1", "Use Case Canvas", FT)
    header_row(ws, 3, ["Field", "Use case 1", "Use case 2", "Use case 3", "Prompt"])
    fields = [
        ("Use case name", "A short name your board would recognise."),
        ("Business owner", "The person who will answer for the result."),
        ("Problem today", "What goes wrong now, in one sentence, with a number if you have one."),
        ("Who feels the problem", "Staff, customers or regulators, and how many."),
        ("AI task type", "Predict, search, generate, classify or summarise."),
        ("Data it needs", "Name each data set. One line each."),
        ("Where the data lives", "System or folder."),
        ("Data owner", "Role, not a team."),
        ("Highest sensitivity of the data", "Public, internal, restricted or confidential."),
        ("Contains personal data", "Y or N. If you are not sure, write Y."),
        ("Data quality needed", "What must be true for the answer to be right?"),
        ("Success measure", "One measure with a unit."),
        ("Baseline today", "The number today."),
        ("Target", "The number you want and by when."),
        ("Effort (1 low to 5 high)", "People, time and money."),
        ("Value (1 low to 5 high)", "Benefit to customers, staff or the balance sheet."),
        ("Priority (value / effort)", "Calculated."),
        ("Main risk", "What could make this fail or cause harm?"),
        ("Decision needed", "What do you need from your sponsor?"),
    ]
    for i, (f, p) in enumerate(fields, start=4):
        cell(ws, f"A{i}", f, FB, wrap=True)
        for col in "BCD":
            cell(ws, f"{col}{i}", None, wrap=True, inp=True)
        cell(ws, f"E{i}", p, FI, wrap=True)
        for j in range(1, 6):
            ws.cell(i, j).border = Border(bottom=HAIR)
    rE = 4 + [x[0] for x in fields].index("Effort (1 low to 5 high)")
    rV = rE + 1
    rP = rE + 2
    for col in "BCD":
        c = ws[f"{col}{rP}"]
        c.value = f'=IF(OR({col}{rE}="",{col}{rV}="",{col}{rE}=0),"",ROUND({col}{rV}/{col}{rE},2))'
        c.fill = PatternFill(fill_type=None)
        c.number_format = "0.00"
    dv_list(ws, ["1", "2", "3", "4", "5"], f"B{rE}:D{rV}", msg="Enter 1 to 5.", title="Rating")
    rT = 4 + [x[0] for x in fields].index("AI task type")
    dv_list(ws, ["Predict", "Search", "Generate", "Classify", "Summarise"], f"B{rT}:D{rT}")
    rS = 4 + [x[0] for x in fields].index("Highest sensitivity of the data")
    dv_list(ws, ["public", "internal", "restricted", "confidential"], f"B{rS}:D{rS}")
    rPd = rS + 1
    dv_list(ws, ["Y", "N"], f"B{rPd}:D{rPd}")
    widths(ws, [32, 34, 34, 34, 52])
    ws.freeze_panes = "B4"
    wb.save(path)


# ------------------------------------------------------------------ Data Inventory
def data_inventory(path, sample=None):
    wb = base_wb("Data Inventory", [
        "List every data source. One row per source. Use the drop-downs where they exist.",
        "A blank owner, steward or sensitivity cell is a finding. The Missing fields column counts the blanks in the key columns.",
        "The summary under the table counts the gaps. Run it again after each review.",
        "Owner is the role that answers for the data. Steward looks after quality day to day. Custodian (IT) runs the system.",
    ])
    ws = wb.create_sheet("Inventory", 1)
    ws.sheet_view.showGridLines = False
    cell(ws, "A1", "Data Inventory", FT)
    cols = ["source_id", "name", "system_type", "format", "approx_records", "refresh", "owner", "steward", "sensitivity", "personal_data", "in_catalogue",
            "last_quality_check", "ai_use_case_candidates", "notes", "Missing fields (owner, steward, sensitivity, personal data)"]
    header_row(ws, 3, cols)
    N = 30
    for i in range(N):
        r = 4 + i
        for j in range(1, 15):
            c = ws.cell(r, j)
            c.fill = INPUT
            c.font = F
            c.alignment = WRAP
        if sample is not None and i < len(sample):
            for j, k in enumerate(cols[:14], start=1):
                v = sample.iloc[i][k]
                ws.cell(r, j, None if (isinstance(v, float) and v != v) or v == "" else v)
        ws.cell(r, 15, f'=IF(A{r}="","",COUNTBLANK(G{r}:J{r}))').font = F
        for j in range(1, 16):
            ws.cell(r, j).border = Border(bottom=HAIR)
    last = 3 + N
    ws2 = wb.create_sheet("Lists")
    lists = {"refresh": ["daily", "weekly", "monthly", "ad hoc", "unknown"], "sensitivity": ["public", "internal", "restricted", "confidential"], "yn": ["Y", "N"]}
    for j, (k, v) in enumerate(lists.items(), start=1):
        ws2.cell(1, j, k).font = FB
        for i, x in enumerate(v, start=2):
            ws2.cell(i, j, x).font = F
    dv_list(ws, lists["refresh"], f"F4:F{last}")
    dv_list(ws, lists["sensitivity"], f"I4:I{last}")
    dv_list(ws, lists["yn"], f"J4:K{last}")
    s = last + 2
    cell(ws, f"A{s}", "Summary", FB)
    items = [("Sources listed", f'=COUNTA(A4:A{last})'),
             ("Sources with no owner", f'=COUNTIFS(A4:A{last},"<>",G4:G{last},"")'),
             ("Sources with no steward", f'=COUNTIFS(A4:A{last},"<>",H4:H{last},"")'),
             ("Sources with no sensitivity class", f'=COUNTIFS(A4:A{last},"<>",I4:I{last},"")'),
             ("Sources with personal data not yet decided", f'=COUNTIFS(A4:A{last},"<>",J4:J{last},"")'),
             ("Sources in a catalogue", f'=COUNTIF(K4:K{last},"Y")'),
             ("Sources with no quality check on record", f'=COUNTIFS(A4:A{last},"<>",L4:L{last},"")')]
    for i, (lab, f) in enumerate(items, start=1):
        cell(ws, f"A{s + i}", lab)
        cell(ws, f"E{s + i}", f)
    widths(ws, [10, 30, 22, 24, 14, 11, 28, 26, 14, 13, 12, 16, 36, 36, 20])
    ws.freeze_panes = "C4"
    wb.save(path)


# ------------------------------------------------------------------ Data Contract
def data_contract(path):
    wb = base_wb("Data Contract Template", [
        "A data contract is an agreement between the team that produces a data set and the teams that use it.",
        "Complete one contract per data set. Name an owner who can say yes or no to a change.",
        "Write quality rules so that a machine can check them: a column, a test and a threshold.",
        "Review the contract every year or when the schema changes, whichever comes first.",
    ])
    ws = wb.create_sheet("Contract", 1)
    ws.sheet_view.showGridLines = False
    cell(ws, "A1", "Data Contract", FT)
    r = 3
    cell(ws, f"A{r}", "1. Identity", FB)
    for lab in ["Data set name", "Version", "Effective date", "Owner (role)", "Steward (role)", "Producing system", "Consumers (teams and tools)", "Purpose", "Sensitivity class", "Contains personal data (Y/N)"]:
        r += 1
        cell(ws, f"A{r}", lab)
        cell(ws, f"B{r}", None, wrap=True, inp=True)
        ws.merge_cells(f"B{r}:F{r}")
        if lab.startswith("Sensitivity"):
            dv_list(ws, ["public", "internal", "restricted", "confidential"], f"B{r}")
        if lab.startswith("Contains"):
            dv_list(ws, ["Y", "N"], f"B{r}")
    r += 2
    cell(ws, f"A{r}", "2. Schema", FB)
    r += 1
    header_row(ws, r, ["Column name", "Type", "Description", "Allowed null (Y/N)", "Example value", "Sensitivity"])
    s1 = r + 1
    for i in range(12):
        r += 1
        for j in range(1, 7):
            c = ws.cell(r, j)
            c.fill = INPUT
            c.font = F
            c.border = Border(bottom=HAIR)
    dv_list(ws, ["Y", "N"], f"D{s1}:D{r}")
    dv_list(ws, ["public", "internal", "restricted", "confidential"], f"F{s1}:F{r}")
    r += 2
    cell(ws, f"A{r}", "3. Quality rules", FB)
    r += 1
    header_row(ws, r, ["Rule id", "Dimension", "Rule (column, test, threshold)", "Check frequency", "Action on failure", "Owner of the action"])
    q1 = r + 1
    for i in range(8):
        r += 1
        ws.cell(r, 1, f"QR{i + 1:02d}").font = F
        for j in range(2, 7):
            c = ws.cell(r, j)
            c.fill = INPUT
            c.font = F
        for j in range(1, 7):
            ws.cell(r, j).border = Border(bottom=HAIR)
    dv_list(ws, ["completeness", "validity", "uniqueness", "consistency", "timeliness", "accuracy"], f"B{q1}:B{r}")
    dv_list(ws, ["each load", "daily", "weekly", "monthly"], f"D{q1}:D{r}")
    r += 2
    cell(ws, f"A{r}", "4. Freshness and volume", FB)
    for lab in ["Refresh schedule", "Latest acceptable delay (hours)", "Expected rows per load (range)", "Alert goes to (role)"]:
        r += 1
        cell(ws, f"A{r}", lab)
        cell(ws, f"B{r}", None, inp=True)
        ws.merge_cells(f"B{r}:F{r}")
    r += 2
    cell(ws, f"A{r}", "5. Change policy", FB)
    for lab in ["What counts as a breaking change", "Notice before a breaking change (days)", "How consumers are told", "Who approves a change"]:
        r += 1
        cell(ws, f"A{r}", lab)
        cell(ws, f"B{r}", None, wrap=True, inp=True)
        ws.merge_cells(f"B{r}:F{r}")
    r += 2
    cell(ws, f"A{r}", "6. Support and sign-off", FB)
    for lab in ["Contact for questions", "Escalation contact", "Owner signature and date", "Consumer signature and date", "Next review date"]:
        r += 1
        cell(ws, f"A{r}", lab)
        cell(ws, f"B{r}", None, inp=True)
        ws.merge_cells(f"B{r}:F{r}")
    widths(ws, [34, 20, 40, 20, 24, 18])
    wb.save(path)


# ------------------------------------------------------------------ Search Test Sheet
def search_test_sheet(path):
    wb = base_wb("Search Test Sheet", [
        "Write 30 questions that your staff really ask. For each, find the document that holds the right answer and copy its document id and a distinctive phrase.",
        "Run each question through the search. Write the rank at which the right document first appears (1 is best). Leave rank blank if it is not in the top ten.",
        "The sheet counts a hit at 3 and a hit at 5, then works out recall at 3, recall at 5 and mean reciprocal rank (MRR).",
        "Record the reason for each miss in the Failure type column. Group the misses before you propose a fix.",
        "On the Permission test sheet list questions that a given user must not be able to answer. A pass means the restricted document did not appear.",
    ])
    ws = wb.create_sheet("Tests", 1)
    ws.sheet_view.showGridLines = False
    cell(ws, "A1", "Search Test Sheet", FT)
    cell(ws, "A2", "Search method tested:", FB)
    cell(ws, "C2", None, inp=True)
    dv_list(ws, ["keyword", "meaning", "hybrid"], "C2")
    header_row(ws, 4, ["Q id", "Question (as staff would ask it)", "Gold document id", "Distinctive phrase in the right passage", "Rank found (blank if not in top 10)", "Hit at 3", "Hit at 5", "Reciprocal rank", "Failure type", "Note"])
    N = 30
    for i in range(N):
        r = 5 + i
        ws.cell(r, 1, f"Q{i + 1:02d}").font = F
        for j in (2, 3, 4, 5, 9, 10):
            c = ws.cell(r, j)
            c.fill = INPUT
            c.font = F
            c.alignment = WRAP
        ws.cell(r, 6, f'=IF(B{r}="","",IF(AND(ISNUMBER(E{r}),E{r}<=3),1,0))').font = F
        ws.cell(r, 7, f'=IF(B{r}="","",IF(AND(ISNUMBER(E{r}),E{r}<=5),1,0))').font = F
        c = ws.cell(r, 8, f'=IF(B{r}="","",IF(ISNUMBER(E{r}),1/E{r},0))')
        c.font = F
        c.number_format = "0.000"
        for j in range(1, 11):
            ws.cell(r, j).border = Border(bottom=HAIR)
    last = 4 + N
    dv_list(ws, ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], f"E5:E{last}", msg="Enter a rank from 1 to 10, or leave blank.", title="Rank")
    dv_list(ws, ["stale version", "wrong chunk", "missing document", "permission", "scan or OCR", "language", "table or layout", "other"], f"I5:I{last}")
    s = last + 2
    cell(ws, f"A{s}", "Results", FB)
    lab = [("Questions", f'=COUNTA(B5:B{last})', "0"),
           ("Hits at 3", f"=SUM(F5:F{last})", "0"), ("Hits at 5", f"=SUM(G5:G{last})", "0"),
           ("Recall at 3", f'=IFERROR(SUM(F5:F{last})/COUNT(F5:F{last}),"")', "0.00"),
           ("Recall at 5", f'=IFERROR(SUM(G5:G{last})/COUNT(G5:G{last}),"")', "0.00"),
           ("Mean reciprocal rank (MRR)", f'=IFERROR(AVERAGE(H5:H{last}),"")', "0.000")]
    for i, (a, f, nf) in enumerate(lab, start=1):
        cell(ws, f"A{s + i}", a)
        cell(ws, f"E{s + i}", f, fmt=nf)
    widths(ws, [7, 46, 14, 40, 18, 9, 9, 12, 18, 30])
    ws.freeze_panes = "C5"
    p = wb.create_sheet("Permission test")
    p.sheet_view.showGridLines = False
    header_row(p, 1, ["User", "User groups", "Question", "Restricted document id", "Appeared in top 5 (Y/N)", "Result"])
    for i in range(10):
        r = 2 + i
        for j in range(1, 6):
            c = p.cell(r, j)
            c.fill = INPUT
            c.font = F
            c.border = Border(bottom=HAIR)
        p.cell(r, 6, f'=IF(E{r}="","",IF(E{r}="N","PASS","FAIL"))').font = F
        p.cell(r, 6).border = Border(bottom=HAIR)
    dv_list(p, ["Y", "N"], "E2:E11")
    cell(p, "A14", "Passes", FB)
    cell(p, "C14", '=COUNTIF(F2:F11,"PASS")')
    cell(p, "A15", "Failures", FB)
    cell(p, "C15", '=COUNTIF(F2:F11,"FAIL")')
    widths(p, [16, 24, 48, 22, 22, 10])
    p.freeze_panes = "A2"
    wb.save(path)


# ------------------------------------------------------------------ Risk Register
def risk_register(path):
    wb = base_wb("Risk Register", [
        "List up to 20 risks for your first AI use. Score likelihood and impact from 1 (low) to 5 (high).",
        "Score = likelihood x impact. Rating: 15 or more is High, 8 to 14 is Medium, below 8 is Low. Rank 1 is the highest score.",
        "Every risk needs one named owner and one action with a date.",
        "The grid on the right counts how many risks sit in each likelihood and impact cell.",
    ])
    ws = wb.create_sheet("Register", 1)
    ws.sheet_view.showGridLines = False
    cell(ws, "A1", "Risk Register", FT)
    header_row(ws, 3, ["Risk id", "Risk (cause, event, effect)", "Category", "Likelihood (1-5)", "Impact (1-5)", "Score", "Rating", "Rank", "Owner (role)", "Action", "Due date", "Status"])
    N = 20
    for i in range(N):
        r = 4 + i
        ws.cell(r, 1, f"R{i + 1:02d}").font = F
        for j in (2, 3, 4, 5, 9, 10, 11, 12):
            c = ws.cell(r, j)
            c.fill = INPUT
            c.font = F
            c.alignment = WRAP
        ws.cell(r, 6, f'=IF(OR(D{r}="",E{r}=""),"",D{r}*E{r})').font = F
        ws.cell(r, 7, f'=IF(F{r}="","",IF(F{r}>=15,"High",IF(F{r}>=8,"Medium","Low")))').font = F
        ws.cell(r, 8, f'=IF(F{r}="","",RANK(F{r},$F$4:$F${3 + N},0)+COUNTIF($F$4:F{r},F{r})-1)').font = F
        ws.cell(r, 11).number_format = "yyyy-mm-dd"
        for j in range(1, 13):
            ws.cell(r, j).border = Border(bottom=HAIR)
    last = 3 + N
    dv_list(ws, ["1", "2", "3", "4", "5"], f"D4:E{last}", msg="Enter 1 to 5.", title="Rating")
    dv_list(ws, ["Data quality", "Privacy and law", "Security", "Model or search quality", "Vendor and cost", "People and skills", "Operations"], f"C4:C{last}")
    dv_list(ws, ["Open", "Mitigating", "Accepted", "Closed"], f"L4:L{last}")
    s = last + 2
    for i, rt in enumerate(["High", "Medium", "Low"], start=1):
        cell(ws, f"A{s + i - 1}", f"{rt} risks", FB)
        cell(ws, f"C{s + i - 1}", f'=COUNTIF(G4:G{last},"{rt}")')
    # grid at N..R
    gc = 14
    cell(ws, f"{L(gc)}3", "Likelihood \\ Impact", FB)
    for k in range(1, 6):
        c = ws.cell(3, gc + k, k)
        c.font = FB
        c.border = Border(bottom=THIN)
    for i, lk in enumerate(range(5, 0, -1)):
        r = 4 + i
        ws.cell(r, gc, lk).font = FB
        for k in range(1, 6):
            c = ws.cell(r, gc + k, f"=COUNTIFS($D$4:$D${last},${L(gc)}{r},$E$4:$E${last},{L(gc + k)}$3)")
            c.font = F
            c.border = Border(bottom=HAIR)
    widths(ws, [8, 48, 22, 12, 12, 8, 10, 8, 22, 36, 12, 12, 3, 18, 6, 6, 6, 6, 6])
    ws.freeze_panes = "C4"
    wb.save(path)


# ------------------------------------------------------------------ Hosting Cost Model
def hosting_cost_model(path):
    wb = base_wb("Hosting Cost Model", [
        "This model has no prices in it. Every cost cell marked YOUR INPUT is blank. Fill it from quotes you have received, or from your own invoices.",
        "Do not copy list prices from a web page. They change, and they differ by country and by contract.",
        "Choose the basis for each line: One-off, Per month or Per year. The model turns every line into a total for the number of years you set.",
        "The total for each option sits at the bottom of the Model sheet. Lines you leave blank count as zero, so the total is a lower bound until Inputs missing shows 0.",
        "Compare options on more than cost. Fill in the residency and latency rows too.",
    ])
    ws = wb.create_sheet("Model", 1)
    ws.sheet_view.showGridLines = False
    cell(ws, "A1", "Hosting Cost Model", FT)
    cell(ws, "A2", "Currency", FB)
    cell(ws, "B2", "UGX", inp=True)
    cell(ws, "A3", "Years in the comparison", FB)
    cell(ws, "B3", 3, inp=True)
    options = ["Option A: on-site", "Option B: local data centre", "Option C: regional cloud", "Option D: software as a service"]
    header_row(ws, 5, ["Cost line", "Basis"] + [o + " (YOUR INPUT)" for o in options] + [""] + [o + " total" for o in options])
    lines = [("Hardware and set-up", "One-off"), ("Hosting or rent", "Per month"), ("Connectivity", "Per month"), ("Licences and subscriptions", "Per year"),
             ("Engineers (salary and benefits)", "Per month"), ("Evaluation and testing", "One-off"), ("Support and maintenance", "Per year"),
             ("Training", "One-off"), ("Backup and recovery", "Per year"), ("Security review", "One-off"), ("Exit and data return", "One-off"), ("Other (name it)", "One-off")]
    first = 6
    for i, (ln, basis) in enumerate(lines):
        r = first + i
        ws.cell(r, 1, ln).font = F
        b = ws.cell(r, 2, basis)
        b.font = F
        b.fill = INPUT
        for j in range(3, 7):
            c = ws.cell(r, j)
            c.fill = INPUT
            c.number_format = "#,##0"
            c.font = F
        for j in range(3, 7):
            col = L(j)
            c = ws.cell(r, j + 5, f'=IF({col}{r}="",0,IF($B{r}="One-off",{col}{r},IF($B{r}="Per month",{col}{r}*12*$B$3,{col}{r}*$B$3)))')
            c.number_format = "#,##0"
            c.font = F
        for j in range(1, 11):
            ws.cell(r, j).border = Border(bottom=HAIR)
    last = first + len(lines) - 1
    dv_list(ws, ["One-off", "Per month", "Per year"], f"B{first}:B{last}")
    t = last + 2
    cell(ws, f"A{t}", "Total for the years chosen", FB)
    cell(ws, f"A{t + 1}", "Inputs missing (blank cost cells)", FB)
    cell(ws, f"A{t + 2}", "Average cost per year", FB)
    for j in range(3, 7):
        col = L(j)
        tot = L(j + 5)
        cell(ws, f"{tot}{t}", f"=SUM({tot}{first}:{tot}{last})", FB, fmt="#,##0")
        cell(ws, f"{col}{t + 1}", f"=COUNTBLANK({col}{first}:{col}{last})", fmt="0")
        cell(ws, f"{tot}{t + 2}", f'=IFERROR({tot}{t}/$B$3,"")', fmt="#,##0")
    r = t + 4
    cell(ws, f"A{r}", "Other things to compare", FB)
    for k, lab in enumerate(["Data stays in the country (Y/N)", "Round-trip latency to users (ms)", "Capacity in 12 months (users, documents)", "Who can see the data (vendor staff, cloud operator)", "Lock-in and exit route"]):
        ws.cell(r + 1 + k, 1, lab).font = F
        for j in range(3, 7):
            c = ws.cell(r + 1 + k, j)
            c.fill = INPUT
            c.font = F
            c.alignment = WRAP
        for j in range(1, 7):
            ws.cell(r + 1 + k, j).border = Border(bottom=HAIR)
    dv_list(ws, ["Y", "N"], f"C{r + 1}:F{r + 1}")
    widths(ws, [38, 12, 22, 22, 22, 22, 3, 20, 20, 20, 20])
    ws.freeze_panes = "C6"
    wb.save(path)


# ------------------------------------------------------------------ Licence Register
def licence_register(path, tools):
    wb = base_wb("Licence Register", [
        "List every tool, library or model you would use. Read the licence file in the project itself, not a summary on a web page.",
        "Write the licence name exactly as the file gives it. Choose a class from the drop-down.",
        "Open source (permissive) and Open source (copyleft) are open licences. Source-available means you can read the code but there are limits on use. Restricted or commercial means you need to pay or ask.",
        "Review due is one year after the date checked. Status shows Review due when that date has passed.",
        "For a model, record the licence on the model card, not only the licence of the library that runs it.",
    ])
    ws = wb.create_sheet("Register", 1)
    ws.sheet_view.showGridLines = False
    cell(ws, "A1", "Licence Register", FT)
    header_row(ws, 3, ["Tool or model", "Used for", "Version", "Licence (as written in the file)", "Licence class", "Where you read it", "Date checked (yyyy-mm-dd)", "Checked by",
                       "Allowed for internal use (Y/N/Ask)", "Allowed to include in a product (Y/N/Ask)", "Notes", "Review due", "Status"])
    N = 25
    for i in range(N):
        r = 4 + i
        for j in range(1, 12):
            c = ws.cell(r, j)
            c.fill = INPUT
            c.font = F
            c.alignment = WRAP
        if i < len(tools):
            ws.cell(r, 1, tools[i][0])
            ws.cell(r, 2, tools[i][1])
        ws.cell(r, 7).number_format = "yyyy-mm-dd"
        c = ws.cell(r, 12, f'=IF(G{r}="","",EDATE(G{r},12))')
        c.number_format = "yyyy-mm-dd"
        c.font = F
        ws.cell(r, 13, f'=IF(A{r}="","",IF(G{r}="","Not checked",IF(TODAY()>L{r},"Review due","OK")))').font = F
        for j in range(1, 14):
            ws.cell(r, j).border = Border(bottom=HAIR)
    last = 3 + N
    dv_list(ws, ["Open source (permissive)", "Open source (copyleft)", "Source-available", "Restricted or commercial", "Unknown"], f"E4:E{last}")
    dv_list(ws, ["Y", "N", "Ask"], f"I4:J{last}")
    s = last + 2
    cell(ws, f"A{s}", "Tools listed", FB)
    cell(ws, f"E{s}", f"=COUNTA(A4:A{last})")
    cell(ws, f"A{s + 1}", "Not checked yet", FB)
    cell(ws, f"E{s + 1}", f'=COUNTIF(M4:M{last},"Not checked")')
    cell(ws, f"A{s + 2}", "Source-available or restricted", FB)
    cell(ws, f"E{s + 2}", f'=COUNTIF(E4:E{last},"Source-available")+COUNTIF(E4:E{last},"Restricted or commercial")')
    cell(ws, f"A{s + 3}", "Unknown licence", FB)
    cell(ws, f"E{s + 3}", f'=COUNTIF(E4:E{last},"Unknown")')
    widths(ws, [34, 36, 10, 26, 24, 28, 16, 14, 16, 18, 30, 12, 12])
    ws.freeze_panes = "B4"
    wb.save(path)


# ------------------------------------------------------------------ Roadmap Planner
def roadmap_planner(path):
    wb = base_wb("Roadmap Planner", [
        "List up to 20 work items. For each give effort in person-days, value from 1 to 5, a start month from 1 to 12 and a duration in months.",
        "Effort is spread evenly over the duration. The total effort per month appears under the table so you can see where the plan is overloaded.",
        "Use Depends on to name the id of an item that must finish first. The check column warns when an item starts before its dependency ends.",
        "Priority is value divided by effort in person-days times 10. Use it to choose between quick wins, not to override a dependency.",
    ])
    ws = wb.create_sheet("Roadmap", 1)
    ws.sheet_view.showGridLines = False
    cell(ws, "A1", "Roadmap Planner (12 months)", FT)
    cell(ws, "A2", "Plan starts", FB)
    cell(ws, "B2", None, inp=True, fmt="yyyy-mm-dd")
    base_h = ["Id", "Work item", "Dimension", "Owner (role)", "Effort (person-days)", "Value (1-5)", "Depends on (id)", "Start month (1-12)", "Duration (months)", "Dependency check", "Priority"]
    header_row(ws, 4, base_h)
    m0 = len(base_h) + 1
    for k in range(12):
        c = ws.cell(4, m0 + k, f'=IF($B$2="","M{k + 1}",TEXT(EDATE($B$2,{k}),"mmm yy"))')
        c.font = FB
        c.border = Border(bottom=THIN)
        c.alignment = Alignment(horizontal="right", wrap_text=True, vertical="bottom")
    N = 20
    first, last = 5, 4 + N
    for i in range(N):
        r = first + i
        ws.cell(r, 1, f"W{i + 1:02d}").font = F
        for j in (2, 3, 4, 5, 6, 7, 8, 9):
            c = ws.cell(r, j)
            c.fill = INPUT
            c.font = F
            c.alignment = WRAP
        ws.cell(r, 10, f'=IF(G{r}="","",IFERROR(IF(INDEX($H${first}:$H${last},MATCH(G{r},$A${first}:$A${last},0))+INDEX($I${first}:$I${last},MATCH(G{r},$A${first}:$A${last},0))<=H{r},"OK","Starts before dependency ends"),"Unknown id"))').font = F
        c = ws.cell(r, 11, f'=IF(OR(E{r}="",F{r}="",E{r}=0),"",ROUND(F{r}/E{r}*10,2))')
        c.number_format = "0.00"
        c.font = F
        for k in range(12):
            col = L(m0 + k)
            c = ws.cell(r, m0 + k, f'=IF(OR($E{r}="",$H{r}="",$I{r}="",$I{r}=0),0,IF(AND({k + 1}>=$H{r},{k + 1}<$H{r}+$I{r}),$E{r}/$I{r},0))')
            c.number_format = "0.0;-0.0;"
            c.font = F
        for j in range(1, m0 + 12):
            ws.cell(r, j).border = Border(bottom=HAIR)
    dv_list(ws, ["1", "2", "3", "4", "5"], f"F{first}:F{last}", msg="Enter 1 to 5.", title="Value")
    dv_list(ws, [str(x) for x in range(1, 13)], f"H{first}:H{last}", msg="Enter a month from 1 to 12.", title="Start month")
    dv_list(ws, DIMS, f"C{first}:C{last}")
    t = last + 1
    cell(ws, f"A{t}", "Total effort per month (person-days)", FB)
    for k in range(12):
        col = L(m0 + k)
        c = cell(ws, f"{col}{t}", f"=SUM({col}{first}:{col}{last})", FB, fmt="0.0")
        c.border = Border(top=THIN)
    cell(ws, f"A{t + 1}", "Total effort in the plan", FB)
    cell(ws, f"E{t + 1}", f"=SUM(E{first}:E{last})", fmt="0")
    cell(ws, f"A{t + 2}", "Busiest month (person-days)", FB)
    cell(ws, f"E{t + 2}", f"=MAX({L(m0)}{t}:{L(m0 + 11)}{t})", fmt="0.0")
    widths(ws, [7, 38, 30, 20, 12, 9, 12, 12, 12, 26, 10] + [8] * 12)
    ws.freeze_panes = "C5"
    wb.save(path)


# ------------------------------------------------------------------ Board Paper Outline (docx)
def board_paper_outline(path):
    import docx
    from docx.shared import Pt
    D = docx.Document()
    st = D.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(11)
    D.core_properties.title = "Board Paper Outline: AI Data Readiness Roadmap"
    import datetime as _dt
    D.core_properties.created = D.core_properties.modified = D.core_properties.last_printed = _dt.datetime(2026, 10, 29, 9, 0, 0)
    D.core_properties.author = "Kitara course build"
    D.add_heading("Board Paper: Data Readiness for AI", level=1)
    P = D.add_paragraph
    P("Organisation: ____________   Date: ____________   Paper owner: ____________   Meeting: ____________").runs[0].italic = True
    sections = [
        ("1. Decision requested", "State in one sentence what the board is asked to approve, and the amount and period. Example format: approve a budget of UGX __ over 12 months to move data readiness from level __ to level __."),
        ("2. Why now", "Name the business problem, one number that shows its size, and what happens if the board waits a year. Keep to five lines."),
        ("3. Where we stand", "Show the baseline scorecard: five dimensions, each with its score and one piece of evidence. Name the weakest dimension and what it blocks."),
        ("4. What we propose", "Show the twelve-month roadmap on one page. Say what is done in the first 30 days, 90 days and 365 days, and which items depend on others."),
        ("5. Cost and funding", "List cost lines: people, hosting, licences, evaluation, support. Say which are one-off and which recur. State what is already funded."),
        ("6. Benefits and measures", "Give three measures with a baseline and a target, for example days to settle a claim or minutes to find a policy answer. Say how and when they will be measured."),
        ("7. Risks and how we manage them", "List the five highest risks from the risk register with an owner for each. Include at least one risk about personal data."),
        ("8. Law and data protection", "State which data protection laws apply, where personal data sits, what leaves the country, and who is the accountable officer."),
        ("9. Governance and owners", "Name the executive sponsor, the data owners, the forum that decides, and how often it meets."),
        ("10. Next steps and dates", "List the next three actions, who does them and by when. Say when the board will see the rescored baseline."),
        ("Annexes", "Baseline scorecard. Roadmap. Risk register. Licence register. Hosting cost comparison."),
    ]
    for h, prompt in sections:
        D.add_heading(h, level=2)
        p = P(prompt)
        p.runs[0].italic = True
    D.save(str(path))
