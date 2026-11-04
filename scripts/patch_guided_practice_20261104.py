"""Patch the Block text in the Week 8 to Week 12 guided_practice notebooks (student-facing) to the two-block arrangement of 2 to 4 November 2026.

Old text (30 October arrangement): Block 1 = Weeks 8, 9, 10 (A7 + A8 + A9, 60 marks, 15 quiz questions sat after the Week 10 class);
Block 2 = Weeks 11, 12, 13 (A10 + A11, 40 marks, quiz after the Week 13 class, closing 7 December 23:59).
Current (data/assessment_blocks_20261103.json): Block 1 = A7 + A8 (40 marks) with quizzes Q7 + Q8 (10 marks) sat together in the last 20 minutes of Class 2;
Block 2 = A9 + A10 + A11 (60 marks) with quizzes Q9 + Q10 (10 marks) sat together in the last 20 minutes of Class 4. Closing times differ by cohort.

Changes: markdown cells 76 (W08), 52 (W09), 52 and 57 (W10), 36 (W11), 44 and 49 (W12) of guided_practice/<cohort>/W08..W12/guided_practice.ipynb, then the
same file inside each student_packages/<cohort>_W08..W12_student.zip, and the unzipped working copy student_packages/CML3113_W08_student/.
Backups: sibling _backup_2026-11-04 folders. Asserts the old text is present; idempotent. The notebooks keep their other cells.
Usage: python3 scripts/patch_guided_practice_20261104.py
"""
import json, shutil, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "IUEA_Teaching_Plan"
BK = "_backup_2026-11-04"
pol = json.loads((ROOT / "data/assessment_blocks_20261103.json").read_text())
DAYS = {"2026-11-17T11:00:00+03:00": "Tuesday 17 November 2026, 11:00", "2026-11-20T08:00:00+03:00": "Friday 20 November 2026, 08:00",
        "2026-11-20T11:00:00+03:00": "Friday 20 November 2026, 11:00", "2026-12-01T11:00:00+03:00": "Tuesday 1 December 2026, 11:00",
        "2026-12-04T08:00:00+03:00": "Friday 4 December 2026, 08:00", "2026-12-04T11:00:00+03:00": "Friday 4 December 2026, 11:00"}
close = {b["id"]: {c: DAYS[v] + " Kampala time" for c, v in b["assignment_closes"].items()} for b in pol["blocks"]}
assert set(close) == {"B1", "B2"}


def first_line_after(src, marker):
    return src


def cells(c):
    c1, c2 = close["B1"][c], close["B2"][c]
    q1 = "The Block 1 quiz is two short quizzes (Q7 and Q8), 10 marks in all. You sit both together in the last 20 minutes of Class 2 (the Week 9 class)."
    q2 = "The Block 2 quiz is two short quizzes (Q9 and Q10), 10 marks in all. You sit both together in the last 20 minutes of Class 4 (the Week 11 class)."
    return {
        "W08": {76: ("## Block 1: how Weeks 8, 9 and 10 are assessed",
                     "## Block 1: how Weeks 8 and 9 are assessed\n\n*PowerPoint slide 64*\n\nOne assignment pack and one quiz sitting for every two classes.\n\n"
                     "Today's tasks are part A of the Block 1 pack (A7), worth 20 of its 40 marks. Part B (A8) follows in the Week 9 class.\n"
                     f"Nothing is submitted and there is no quiz after today's class. You hand in both parts together by {c1}.\n{q1}")},
        "W09": {52: ("## Block 1, part B: this week's tasks",
                     "## Block 1, part B: this week's tasks\n\n*PowerPoint slide 44*\n\nPart B of 2. 20 marks.\n\n"
                     "Today's tasks are part B of the Block 1 pack (A8), worth 20 of its 40 marks. They use classification_metrics.\n"
                     f"Part A (A7) was last week. Both parts are handed in together by {c1}.\n"
                     "The Block 1 quiz is sat in the last 20 minutes of today's class: two short quizzes (Q7 and Q8), 10 marks in all.")},
        "W10": {52: ("## Block 1, part C: this week's tasks",
                     "## Block 2, part A: this week's tasks\n\n*PowerPoint slide 41*\n\nPart A of 3. 20 marks.\n\n"
                     "Today's tasks are part A of the Block 2 pack (A9), worth 20 of its 60 marks. They use group_split and predict_regression.\n"
                     f"Parts B (A10) and C (A11) follow. All three parts are handed in together by {c2}.\n"
                     "There is no quiz after today's class. The Block 2 quiz is sat in the last 20 minutes of Class 4."),
                57: ("## Submit the Block 1 assignment pack",
                     "## Submit the Block 1 assignment pack\n\n*PowerPoint slide 46*\n\n01\n\nPart A: Regression and baseline (A7, Week 8)\n\nOpen the A7 form\n\n"
                     "02\n\nPart B: Classification and cost (A8, Week 9)\n\nOpen the A8 form\n\n"
                     f"Closes {c1}. Submit each notebook to its own form, with your full Student Registration Number. The Block 2 pack (A9, A10, A11) closes {c2}.")},
        "W11": {36: ("## Block 2: how Weeks 11, 12 and 13 are assessed",
                     "## Block 2: how Weeks 10 and 11 are assessed\n\n*PowerPoint slide 32*\n\nOne assignment pack and one quiz sitting for every two classes.\n\n"
                     "Today's tasks are part B of the Block 2 pack (A10), worth 20 of its 60 marks. Part A (A9) was last week and part C (A11, model recommendation) follows.\n"
                     f"Nothing is submitted and there is no quiz after today's class. You hand in all 3 parts together by {c2}.\n"
                     f"{q2}")},
        "W12": {44: ("## Block 2, part B: this week's tasks",
                     "## Block 2, part C: this week's tasks\n\n*PowerPoint slide 36*\n\nPart C of 3. 20 marks.\n\n"
                     "Today's tasks are part C of the Block 2 pack (A11), worth 20 of its 60 marks. They use select_model and regression_errors.\n"
                     f"The pack closes {c2}. There is no separate Week 12 class: Week 12 is the project sitting.\n"
                     "There is no quiz after this notebook. The Block 2 quiz is sat in the last 20 minutes of Class 4."),
                49: ("## Submit the Block 2 assignment pack",
                     "## Submit the Block 2 assignment pack\n\n*PowerPoint slide 43*\n\n01\n\nPart A: Validation and trust (A9, Week 10)\n\nOpen the A9 form\n\n"
                     "02\n\nPart B: Features and ablation (A10, Week 11)\n\nOpen the A10 form\n\n03\n\nPart C: Model recommendation (A11, Week 12)\n\nOpen the A11 form\n\n"
                     f"Closes {c2}. Submit each notebook to its own form, with your full Student Registration Number.")},
    }


def patched(raw, cohort, week):
    nb = json.loads(raw)
    assert json.dumps(nb, indent=1, ensure_ascii=False) == raw, "unexpected notebook formatting"
    changed = False
    for idx, (old_head, new_text) in cells(cohort)[week].items():
        c = nb["cells"][idx]; src = "".join(c["source"])
        if src == new_text:
            continue
        assert src.startswith(old_head), (cohort, week, idx, src[:80])
        lines = new_text.split("\n")
        c["source"] = [l + "\n" for l in lines[:-1]] + [lines[-1]]
        changed = True
    return json.dumps(nb, indent=1, ensure_ascii=False), changed


def backup(p, sub=None):
    d = p.parent / BK; d.mkdir(exist_ok=True)
    dest = d / (sub or p.name)
    if not dest.exists():
        shutil.copy2(p, dest)


def main():
    done = []
    for cohort in ("CML3111", "CML3112", "CML3113"):
        for week in ("W08", "W09", "W10", "W11", "W12"):
            p = BASE / "guided_practice" / cohort / week / "guided_practice.ipynb"
            raw = p.read_text(encoding="utf-8")
            new, ch = patched(raw, cohort, week)
            if ch:
                backup(p); p.write_text(new, encoding="utf-8"); done.append(str(p.relative_to(ROOT)))
            # the same notebook inside the assignment ZIP
            z = BASE / "student_packages" / f"{cohort}_{week}_student.zip"
            zin = zipfile.ZipFile(z)
            inner = zin.read("guided_practice.ipynb").decode("utf-8")
            newz, chz = patched(inner, cohort, week)
            if chz:
                zin.close(); backup(z)
                tmp = z.with_suffix(".zip.tmp")
                with zipfile.ZipFile(z) as src, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as dst:
                    for info in src.infolist():
                        data = src.read(info.filename)
                        if info.filename == "guided_practice.ipynb":
                            data = newz.encode("utf-8")
                        dst.writestr(info, data, compress_type=info.compress_type)
                tmp.replace(z); done.append(str(z.relative_to(ROOT)))
    # unzipped working copy of CML3113 W08 (it still carried the 30 October block text in both notebooks)
    folder = BASE / "student_packages/CML3113_W08_student"
    z = zipfile.ZipFile(BASE / "student_packages/CML3113_W08_student.zip")
    for name in ("W08_student.ipynb", "guided_practice.ipynb", "START_HERE.md"):
        data = z.read(name)
        tgt = folder / name
        if tgt.read_bytes() != data:
            backup(tgt); tgt.write_bytes(data); done.append(str(tgt.relative_to(ROOT)))
    print("changed:", *done, sep="\n  ") if done else print("nothing to change (already patched)")


if __name__ == "__main__":
    main()
