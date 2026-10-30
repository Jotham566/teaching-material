"""Update the syllabi, master teaching plan and quiz operations guide for the block arrangement (idempotent)."""
import json, docx
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; B = ROOT / "IUEA_Teaching_Plan"
POL = json.loads((ROOT / "data" / "assessment_blocks_20261030.json").read_text())
MARK = "From Week 8 "

def setp(p, text):
    runs = p.runs
    if not runs: p.add_run(text); return
    runs[0].text = text
    for r in runs[1:]: r.text = ""

def app(p, text):
    if p.runs: p.runs[-1].text += text
    else: p.add_run(text)

def cell_set(c, text):
    ps = c.paragraphs; setp(ps[0], text)
    for p in ps[1:]: setp(p, "")

def cell_app(c, text):
    if text.strip() in c.text: return
    app(c.paragraphs[-1], text)

QZ = {8: "No quiz (Block 1 quiz in Week 10)", 9: "No quiz (Block 1 quiz in Week 10)", 10: "Block 1 quiz: Q7, Q8, Q9 (one sitting)",
      11: "No quiz (Block 2 quiz in Week 13)", 12: "No quiz (Block 2 quiz in Week 13)", 13: "Block 2 quiz: Q10, Q11, Q12 (one sitting)"}
PART = {8: " · Block 1, part A", 9: " · Block 1, part B", 10: " · Block 1, part C", 11: " · Block 2, part A", 12: " · Block 2, part B"}

def syllabus(f, code, weeks6):
    d = docx.Document(B / f); wk = d.tables[2]
    for r in wk.rows:
        t = r.cells[0].text.strip()
        if not t.isdigit() or int(t) not in QZ: continue
        w = int(t); cell_set(r.cells[4], QZ[w])
        if w in PART: cell_app(r.cells[5], PART[w])
    cl = {b["id"]: b["assignment_closes"][code] for b in POL["blocks"]}
    from datetime import datetime
    fmt = lambda s: (lambda d: f"{d.day} {d.strftime('%B')}")(datetime.fromisoformat(s))
    pre = "Weeks 1–6 weekly; Weeks 8–13 in two blocks"
    asm = d.tables[4]
    for r in asm.rows:
        n = r.cells[0].text.strip()
        if n == "Weekly quizzes" or n.startswith("Weekly quizzes"):
            cell_set(r.cells[0], "Quizzes: weekly, then one per block")
            cell_set(r.cells[1], "Weekly quizzes in Weeks 1–6; one sitting at the end of Week 10 and one at the end of Week 13")
            n6 = "Best 4 of the six weekly quizzes count" if weeks6 else "Week 6 is not assigned to your cohort, so the best 3 of the five weekly quizzes count"
            cell_set(r.cells[4], f"A five-minute quiz of five multiple-choice questions on your phone, auto-marked with immediate feedback. From Week 8 the quizzes of three classes are taken together in one sitting (Block 1: Q7 to Q9; Block 2: Q10 to Q12), each form open for 24 hours. {n6}; both blocks always count. The total is {'50' if weeks6 else '45'} marks and the component is worth 10%.")
        elif n.startswith("Practical challenges"):
            cell_set(r.cells[0], "Practical challenges and assignments")
            cell_set(r.cells[1], f"Weekly in Weeks 1–6; Block 1 pack closes {fmt(cl['B1'])}; Block 2 pack closes {fmt(cl['B2'])}")
            n6 = "Best 4 of the six weekly assignments count" if weeks6 else "Week 6 is not assigned to your cohort, so the best 3 of the five weekly assignments count"
            cell_set(r.cells[4], f"{n6}. Block 1 is three parts (A7, A8, A9) and Block 2 is two parts (A10, A11); each part uses the same assignment form as before, and a part not submitted scores zero. Both blocks always count. The total is {'180' if weeks6 else '160'} marks and the component is worth 10%. Upload the required notebook and report through the assignment form. Visible checks provide practice feedback; final marks use the submitted files.")
    d.save(B / f)

def master():
    f = "IUEA_ML_Semester1_Master_Teaching_Plan.docx"; d = docx.Document(B / f)
    for r in d.tables[5].rows:
        n = r.cells[0].text
        if n.startswith("Weekly quizzes"):
            cell_set(r.cells[0], "Quizzes (weekly in Weeks 1–6; one sitting per block from Week 8)"); cell_set(r.cells[1], "W1–W6 weekly; end of W10 (Block 1) and W13 (Block 2)")
        elif n.startswith("Practical challenges"):
            cell_set(r.cells[0], "Practical challenges and assignments (weekly in Weeks 1–6; two block packs from Week 8)"); cell_set(r.cells[1], "Weeks 1–6; Block 1 (W8–W10); Block 2 (W11–W12, W13 content in the quiz)")
    for i, p in enumerate(d.paragraphs):
        if p.text.startswith("Every teaching session closes with a five-minute quiz") and MARK not in p.text:
            app(p, " From Week 8 the arrangement changes: the quizzes and assignments of three classes are combined into one sitting and one pack. Block 1 covers Weeks 8 to 10 and Block 2 covers Weeks 11 to 13. Each quiz form is still five questions and five marks, the three forms of a block are opened together in the last twenty minutes of the Week 10 or Week 13 class, and neither block can be dropped. Best 4 of the six weekly quizzes count from Weeks 1 to 6 (best 3 of five where Week 6 is not assigned), so the quiz total is 50 marks (45), written to 10% of the course. Assignments follow the same rule with a total of 180 marks (160). Full details: Block_Assessment_Arrangement_2026-10-30.md.")
        if p.text.startswith("Two features are worth noting") and MARK not in p.text:
            app(p, " After Week 6 the lowest scores are no longer dropped; the block structure keeps the safety margin by giving each quiz sitting a full 24-hour window and by allowing the block assignment parts to be submitted at any time before the shared close.")
    wk = None
    for t in d.tables:
        if t.rows and len(t.rows[0].cells) >= 5 and t.rows[0].cells[4].text.strip().lower().startswith("quiz") if False else False: wk = t
    for t in d.tables:
        for r in t.rows:
            c = r.cells
            if len(c) >= 5 and c[0].text.strip().isdigit() and int(c[0].text.strip()) in QZ and c[4].text.strip().startswith("Quiz"):
                cell_set(c[4], QZ[int(c[0].text.strip())].replace(" (one sitting)", ""))
    d.save(B / f)

def quizops():
    f = "IUEA_ML_Weekly_Quiz_Operations_Guide.docx"; d = docx.Document(B / f)
    if any("Block quiz sittings from Week 8" in p.text for p in d.paragraphs): return
    last = d.paragraphs[-1]
    h = d.add_paragraph("Block quiz sittings from Week 8"); h.style = d.paragraphs[28].style
    for txt in [
        "From Week 8 the weekly quiz is replaced by one sitting after every three classes. Block 1 uses the Q7, Q8 and Q9 forms (Weeks 8 to 10) and Block 2 uses Q10, Q11 and Q12 (Weeks 11 to 13). The forms, the answer keys and the gradebook are unchanged.",
        "In the last twenty minutes of the Week 10 or Week 13 class, run open_Block1_CML31xx or open_Block2_CML31xx from grader/block_quiz_sittings_20261030.gs. It opens the three forms together; each stays open for 24 hours from activation. Show one QR code per form, or share the three links.",
        "Run applyBlockWindows() from grader/apply_block_windows_20261030.gs once to move the A7 to A11 assignment forms to the block closing times in data/assessments.json.",
        "Gradebook: Weeks 1 to 6 keep the best 4 of 6 (best 3 of 5 where Week 6 is not assigned). The two blocks are never dropped. Quizzes are out of 50 (45) marks and assignments out of 180 (160). Open item: the Q12 bank was written for the old Week 13 and needs a new bank for regularisation and nearest neighbours before the Block 2 sitting.",
    ]: d.add_paragraph(txt)
    d.save(B / f)

if __name__ == "__main__":
    syllabus("IUEA_ML_Syllabus_CohortA_Design_and_Infrastructure.docx", "CML3111", False)
    syllabus("IUEA_ML_Syllabus_CohortB_Mining_and_Petroleum.docx", "CML3112", False)
    syllabus("IUEA_ML_Syllabus_CohortC_Engineering.docx", "CML3113", False)
    master(); quizops(); print("done")
