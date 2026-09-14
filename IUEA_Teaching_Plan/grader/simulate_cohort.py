#!/usr/bin/env python3
"""simulate_cohort.py - make a fake cohort so you can load-test the grader.

Run this before the semester, and again after you edit a spec. It writes N
notebooks with a realistic mix of right, wrong, broken and unreadable work,
plus a token CSV shaped like a Google Forms export, and it deliberately plants
the failure cases you need to know the grader catches:

    a token corrupted by a partial paste
    a token signed with the wrong key (someone else's copy of the module)
    a token whose scores were inflated but whose signature is valid, which is
        what a student who reads SIGNING_KEY out of iuea_grader.py can do
    a Form row with no code in it at all
    a student who submitted twice

    python3 simulate_cohort.py --n 195 --out /tmp/fake_W05
    python3 batch_grade.py -a W05 -n /tmp/fake_W05/notebooks \
        -t /tmp/fake_W05/form_responses.csv --data-dir data \
        --sample 20 --seed 7 -o /tmp/fake_W05/results

Standard library only.
"""

import argparse
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import iuea_grader as ig                                            # noqa: E402

SOLUTIONS = {
    # (label, weight, cell source appended to the notebook, visible marks)
    "perfect": '''
df = pd.read_csv(CSV)
n_meters = df["meter_id"].nunique()
df["cost_per_kwh"] = df["cost_ugx"] / df["kwh"]
high_use = df[df["kwh"] > 5000]
mean_cost_per_kwh = df["cost_per_kwh"].mean()
peak_building = df.groupby("building")["kwh"].sum().idxmax()
''',
    "good_visible_weak_hidden": '''
df = pd.read_csv(CSV)
n_meters = df["meter_id"].nunique()
df["cost_per_kwh"] = df["cost_ugx"] / df["kwh"]
high_use = df[df["kwh"] >= 5000]
mean_cost_per_kwh = df["cost_per_kwh"].sum()
peak_building = df.groupby("block")["kwh"].sum().idxmax()
''',
    "counted_rows": '''
df = pd.read_csv(CSV)
n_meters = len(df)
df["cost_per_kwh"] = df["cost_ugx"] / df["kwh"]
high_use = df[df["kwh"] > 5000]
mean_cost_per_kwh = df["cost_per_kwh"].mean()
peak_building = df.groupby("building")["kwh"].sum().idxmax()
''',
    "inverted_ratio": '''
df = pd.read_csv(CSV)
n_meters = df["meter_id"].nunique()
df["cost_per_kwh"] = df["kwh"] / df["cost_ugx"]
high_use = df[df["kwh"] > 5000]
mean_cost_per_kwh = df["cost_per_kwh"].mean()
peak_building = df.groupby("building")["kwh"].sum().idxmax()
''',
    "filtered_too_early": '''
df = pd.read_csv(CSV)
n_meters = df["meter_id"].nunique()
high_use = df[df["kwh"] > 5000].copy()
df["cost_per_kwh"] = df["cost_ugx"] / df["kwh"]
mean_cost_per_kwh = df["cost_per_kwh"].mean()
peak_building = df.groupby("building")["kwh"].sum()
''',
    "raises_nameerror": '''
df = pd.read_csv(CSV)
n_meters = df["meter_id"].nunique()
df["cost_per_kwh"] = df["cost_ugx"] / df["kwhh"]
high_use = df[df["kwh"] > 5000]
mean_cost_per_kwh = df["cost_per_kwh"].mean()
peak_building = df.groupby("building")["kwh"].sum().idxmax()
''',
    "infinite_loop": '''
df = pd.read_csv(CSV)
n_meters = df["meter_id"].nunique()
while True:
    pass
''',
    "blank": '''
# I did not do it
''',
}

WEIGHTS = [("perfect", 46), ("good_visible_weak_hidden", 20),
           ("counted_rows", 10), ("inverted_ratio", 9),
           ("filtered_too_early", 9), ("raises_nameerror", 4),
           ("infinite_loop", 1), ("blank", 1)]

COHORTS = ["CML3111", "CML3112", "CML3113"]


def build_notebook(template, solution_src, cohort):
    nb = json.loads(json.dumps(template))
    # Set the cohort in the setup cell, exactly as the handed-out notebook does.
    for c in nb["cells"]:
        if c["cell_type"] == "code":
            src = "".join(c["source"])
            if "COHORT =" in src:
                c["source"] = [
                    l.replace('COHORT = "CML3112"', 'COHORT = "%s"' % cohort)
                    for l in c["source"]]
    # Replace the placeholder answer cells with one cell of real work, so the
    # rest of the notebook (setup, check cells, plot) is exercised unchanged.
    kept = []
    for c in nb["cells"]:
        src = "".join(c.get("source", []))
        if c["cell_type"] == "code" and "### START CODE HERE ###" in src:
            continue
        kept.append(c)
    work = {"cell_type": "code", "execution_count": None, "metadata": {},
            "outputs": [], "source": [l + "\n" for l in
                                      solution_src.strip().split("\n")]}
    # Immediately AFTER the cell that imports pandas and builds the Grader.
    # Inserting it before that cell is a mistake that makes every simulated
    # student fail on NameError: pd, which then reads as a grader bug.
    at = len(kept)
    for i, c in enumerate(kept):
        if c["cell_type"] == "code" and "from iuea_grader import Grader" in \
                "".join(c["source"]):
            at = i + 1
            break
    kept.insert(at, work)
    nb["cells"] = kept
    return nb


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=195)
    ap.add_argument("--out", default="/tmp/fake_W05")
    ap.add_argument("--template", default=os.path.join(
        HERE, "student_template.ipynb"))
    ap.add_argument("--assignment", default="W05")
    ap.add_argument("--spec", default=None)
    ap.add_argument("--data-dir", default=os.path.join(HERE, "data"))
    ap.add_argument("--seed", type=int, default=2026)
    args = ap.parse_args(argv)

    rng = random.Random(args.seed)
    nb_dir = os.path.join(args.out, "notebooks")
    os.makedirs(nb_dir, exist_ok=True)
    template = json.load(open(args.template))

    spec = ig.load_spec(args.assignment, args.spec)
    pool = []
    for label, w in WEIGHTS:
        pool.extend([label] % () if False else [label] * w)

    plan, rows = [], []
    for i in range(args.n):
        sid = "S24%03d" % (i + 1)
        label = rng.choice(pool)
        cohort = COHORTS[i % 3]
        plan.append((sid, label, cohort))

    # ---- notebooks ------------------------------------------------------- #
    for sid, label, cohort in plan:
        nb = build_notebook(template, SOLUTIONS[label], cohort)
        path = os.path.join(nb_dir, "%s_%s.ipynb" % (sid, args.assignment))
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(nb, fh, indent=1)

    # one file that is not a notebook at all
    with open(os.path.join(nb_dir, "S24%03d_%s.ipynb"
                           % (args.n + 1, args.assignment)), "w") as fh:
        fh.write("this is a screenshot, not a notebook\n")
    plan.append(("S24%03d" % (args.n + 1), "corrupt_file", COHORTS[0]))

    # ---- tokens: run each solution in-process to get honest visible scores #
    import importlib
    data_dir = args.data_dir
    csv_path = os.path.join(data_dir, "campus_energy.csv")
    questions_by_cohort = {c: ig.resolve_questions(spec, c) for c in COHORTS}

    def score(label, cohort):
        ns = {"__name__": "__main__", "__builtins__": __builtins__,
              "CSV": csv_path}
        try:
            exec("import pandas as pd", ns)
            if label != "infinite_loop":
                exec(SOLUTIONS[label], ns)
        except Exception:                              # noqa: BLE001
            pass
        qs = questions_by_cohort[cohort]
        vis = [(qid, ig.run_check(qid, q, ns).awarded)
               for qid, q in qs if q.get("visible", True)]
        return vis, ig.answer_fingerprint(qs, ns)

    plant = {}
    for sid, label, cohort in plan:
        if label == "corrupt_file":
            continue
        if label == "infinite_loop":
            # this student never got a code, because their notebook hangs
            continue
        vis, fp = score(label, cohort)
        tok = ig.make_token(sid, args.assignment, cohort, vis, fp)
        rows.append([sid, tok, cohort])

    # ---- plant the failure cases ----------------------------------------- #
    if len(rows) > 12:
        # 1. partial paste
        victim = rows[3]
        plant["corrupted_paste"] = victim[0]
        victim[1] = victim[1][:len(victim[1]) - 12]
        # 2. signed with the wrong key
        v2 = rows[5]
        plant["wrong_key"] = v2[0]
        vis, fp = score("perfect", v2[2])
        v2[1] = ig.make_token(v2[0], args.assignment, v2[2], vis, fp,
                              key=b"a-different-key-entirely")
        # 3. inflated but validly signed: full marks claimed on a blank notebook
        v3 = rows[7]
        plant["inflated"] = v3[0]
        real_vis, real_fp = score("blank", v3[2])
        full = [(qid, q["marks"]) for qid, q in questions_by_cohort[v3[2]]
                if q.get("visible", True)]
        v3[1] = ig.make_token(v3[0], args.assignment, v3[2], full, real_fp)
        # overwrite that student's notebook with the blank one so the
        # discrepancy is real and not an artefact of the simulation
        nb = build_notebook(template, SOLUTIONS["blank"], v3[2])
        with open(os.path.join(nb_dir, "%s_%s.ipynb"
                               % (v3[0], args.assignment)), "w") as fh:
            json.dump(nb, fh, indent=1)
        # 4. a Form row with no code
        rows.insert(9, [rows[9][0], "", rows[9][2]])
        plant["no_code_row"] = rows[9][0]
        # 5. a resubmission: same student, two rows
        again = list(rows[11])
        rows.append(again)
        plant["duplicate"] = again[0]

    csv_out = os.path.join(args.out, "form_responses.csv")
    with open(csv_out, "w", encoding="utf-8") as fh:
        fh.write("Timestamp,Student number,Paste your submission code here,Cohort\n")
        for i, (sid, tok, cohort) in enumerate(rows):
            fh.write("2026/10/12 %02d:%02d:00,%s,%s,%s\n"
                     % (8 + i % 12, i % 60, sid, tok, cohort))

    with open(os.path.join(args.out, "PLANTED.json"), "w") as fh:
        json.dump({"planted": plant,
                   "mix": {lab: sum(1 for _, l, _ in plan if l == lab)
                           for lab, _ in WEIGHTS}}, fh, indent=2)

    print("notebooks : %d in %s" % (len(plan), nb_dir))
    print("form rows : %d in %s" % (len(rows), csv_out))
    print("mix       : %s" % json.dumps(
        {lab: sum(1 for _, l, _ in plan if l == lab) for lab, _ in WEIGHTS}))
    print("planted   : %s" % json.dumps(plant, indent=12))
    return 0


if __name__ == "__main__":
    sys.exit(main())
