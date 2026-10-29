"""Extra Kitara teaching files for sessions 10, 11 and 12 (risk register, roadmap, hosting options, licence register, projected scorecard).

  python3 build_extra_data.py

Writes five CSV files into 03 Learner Materials/Practice Files/data/, adds them to DATA DICTIONARY.txt, adds an 'extra' entry to answer_key.json
and rebuilds data.zip (answer_key.json is left out of the zip). Nothing here is random: the content is fixed text, so a re-run gives identical files.
Run it again after build_teaching_data.py, because that script rewrites the dictionary, the key and the zip without these files.
"""
import csv, json, re, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LEARN = ROOT / "03 Learner Materials"
DATA = LEARN / "Practice Files" / "data"
MARK = "EXTRA FILES (added by build_extra_data.py)"


def write_csv(name, header, rows):
    with open(DATA / name, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)


def check(cond, msg):
    if not cond:
        raise AssertionError(msg)


# ------------------------------------------------------------------------------------------------ risk register
RISKS = [
    ("R01", "Personal data enters the search index", 4, 5, "Data protection officer", "Masking rule drafted; not yet run on the claims letters", "Open"),
    ("R02", "Stale policy returned as the current answer", 5, 3, "Head of Human Resources", "None. Superseded status is held only in the metadata file", "Open"),
    ("R03", "Restricted documents exposed through search", 3, 5, "Head of IT", "Permission filter built in the pilot; not tested on all groups", "Mitigating"),
    ("R04", "Vendor lock-in to one hosting or search supplier", 2, 3, "Head of IT", "Exit plan requested in the supplier questions", "Open"),
    ("R05", "Model licence changes after we build on it", 2, 4, "Head of IT", "Licence register started; no model checked yet", "Open"),
    ("R06", "Scanned documents unreadable by the text reader", 4, 2, "Head of Claims", "OCR run on a sample of eight scans", "Mitigating"),
    ("R07", "No owner for claims data", 3, 4, "Steering council", "Owner named on paper for the claims system; archive still unowned", "Open"),
    ("R08", "Shadow use of public chatbots with customer data", 4, 3, "Head of Risk", "Circular on generative AI tools issued; no monitoring", "Mitigating"),
    ("R09", "Cross-border transfer without a legal basis", 2, 5, "Head of Legal and Compliance", "Legal review planned before any foreign hosting", "Open"),
    ("R10", "Pipeline fails silently and the index goes stale", 2, 3, "Head of IT", "Nightly extracts exist; no freshness alert", "Open"),
    ("R11", "Embedding model weak on Swahili", 3, 2, "Head of Kitara Kenya operations", "Six Swahili test questions kept in the test set", "Accepted"),
    ("R12", "Staff leave with the knowledge of how the data fits together", 3, 2, "Head of Human Resources", "Lineage drawn for two chains; nothing written for the rest", "Open"),
]
risk_scores = [r[2] * r[3] for r in RISKS]
n_high = sum(s >= 15 for s in risk_scores)
n_mid = sum(8 <= s <= 14 for s in risk_scores)
n_low = sum(s < 8 for s in risk_scores)
check(len(RISKS) == 12 and (n_high, n_mid, n_low) == (3, 5, 4), f"risk bands {n_high}/{n_mid}/{n_low}")
check(all(1 <= r[2] <= 5 and 1 <= r[3] <= 5 for r in RISKS), "risk scale")
write_csv("risk_register.csv", ["id", "risk", "likelihood", "impact", "owner_role", "current_control", "status"], RISKS)

# ------------------------------------------------------------------------------------------------ roadmap
# start_month and duration_months count whole months. An item that starts in month 4 and lasts 2 months occupies months 4 and 5.
ROAD = [
    ("W01", "Name the steering council and an owner for every source", 1, 1, 6, 5, "", "Chief Executive"),
    ("W02", "Complete the data inventory and classify every source", 2, 2, 20, 4, "W01", "Data steward lead"),
    ("W03", "Approve the data classification and acceptable AI use policies", 2, 2, 12, 4, "W01", "Head of Legal and Compliance"),
    ("W04", "Choose the hosting option and write the exit plan", 2, 2, 10, 3, "W01", "Head of IT"),
    ("W05", "Fix the quality defects in the customer and claims tables", 4, 2, 30, 4, "W02", "Data steward lead"),
    ("W06", "Write data contracts for the three main datasets", 4, 2, 15, 3, "W02", "Data owner, claims"),
    ("W07", "Set up raw, cleaned and serving zones", 4, 3, 40, 4, "W02;W04", "Head of IT"),
    ("W08", "Read and repair the claims and policy documents", 4, 2, 25, 4, "W02", "Data custodian"),
    ("W09", "Train staff and publish the acceptable use guidance", 4, 2, 10, 3, "W03", "Head of Human Resources"),
    ("W10", "Build the 60 question test set and track recall", 6, 2, 12, 4, "W08", "Data steward lead"),
    ("W11", "Midyear rescore of the baseline", 6, 1, 5, 3, "W05;W06", "Steering council"),
    ("W12", "Mask personal data before indexing", 6, 2, 18, 5, "W03;W08", "Data protection officer"),
    ("W13", "Add permission filters and query logging", 7, 1, 14, 5, "W07", "Head of IT"),
    ("W14", "Add freshness, volume and schema alerts", 7, 2, 16, 4, "W07", "Head of IT"),
    ("W15", "Run the staff policy assistant pilot", 8, 3, 35, 5, "W12;W13;W07", "Head of Human Resources"),
    ("W16", "Second rescore and board report", 11, 2, 8, 4, "W15;W14", "Steering council"),
]
by_id = {r[0]: r for r in ROAD}
check(len(ROAD) == 16 and len(by_id) == 16, "16 roadmap items")
for r in ROAD:
    start, dur = r[2], r[3]
    check(1 <= start <= 12 and dur >= 1 and start + dur - 1 <= 12, f"{r[0]} outside the 12 months")
    check(1 <= r[5] <= 5, f"{r[0]} value")
    for d in [x for x in r[6].split(";") if x]:
        check(d in by_id, f"{r[0]} depends on unknown {d}")
        pre = by_id[d]
        check(start >= pre[2] + pre[3], f"{r[0]} starts in month {start} before {d} ends in month {pre[2] + pre[3] - 1}")


def chain_months(i, memo={}):
    """Longest chain of whole months ending at item i, counting each duration once along a dependency path."""
    if i in memo:
        return memo[i]
    r = by_id[i]
    best, prev = 0, None
    for d in [x for x in r[6].split(";") if x]:
        c, p = chain_months(d)
        if c > best:
            best, prev = c, d
    memo[i] = (best + r[3], prev)
    return memo[i]


end_item = max(by_id, key=lambda i: (chain_months(i)[0], by_id[i][2] + by_id[i][3]))
critical_months = chain_months(end_item)[0]
path, cur = [], end_item
while cur:
    path.append(cur)
    cur = chain_months(cur)[1]
path.reverse()
check(critical_months >= 9, f"critical path {critical_months} months")
check(max(r[2] + r[3] - 1 for r in ROAD) == 12, "plan ends in month 12")
write_csv("roadmap_items.csv", ["id", "item", "start_month", "duration_months", "effort_days", "value", "depends_on", "owner_role"], ROAD)

# ------------------------------------------------------------------------------------------------ hosting options (no prices anywhere)
HOST = [
    ("On-site data centre", "Uganda, on Kitara premises", "low", "High: power, cooling and spare hardware are Kitara's own problem", "Highest: Kitara runs everything", "Medium: the hardware is owned but the skills are scarce",
     "Check regulator rules on where bank and insurance data may be held, and the Personal Data Protection Office registration"),
    ("Local colocation in Kampala", "Uganda, in a provider's building on Kitara's own hardware", "low", "Medium: depends on the free rack space and power the provider has", "High: Kitara runs the machines, the provider runs the building",
     "Medium: contract notice period and moving the hardware", "Check access, audit and breach notice terms in the colocation contract"),
    ("Regional cloud in South Africa", "Outside Uganda and Kenya, in South Africa", "medium", "Low: capacity can be added when needed", "Medium: Kitara sets up the services and the provider runs the platform",
     "Medium to high: services are built on provider features", "Check the legal basis and safeguards for sending Ugandan and Kenyan personal data abroad"),
    ("Managed software service", "Set by the provider, often outside the region", "medium", "Low: the provider carries the capacity", "Low: Kitara sees the product and not the platform beneath it",
     "High: data and workflows sit in the provider's format", "Check where documents are processed, who the sub-processors are and whether Kitara's data trains the provider's models"),
]
check(len(HOST) == 4 and all(h[2] in ("low", "medium", "high") for h in HOST), "hosting options")
check(not any(re.search(r"\d|USD|UGX|\$", " ".join(h)) for h in HOST), "hosting file must hold no numbers or prices")
write_csv("hosting_options.csv", ["option", "data_residency", "latency_to_kampala", "capacity_risk", "control", "exit_difficulty", "main_legal_check"], HOST)

# ------------------------------------------------------------------------------------------------ licence register sample (facts from Research Notes section 3 and curriculum.py; checked_on left blank for learners)
LIC = [
    ("Google Colab", "Run notebooks in the browser", "Google terms of service for the free tier", "proprietary", "Check", "Free tier limits are not published. Read the terms before using it for client work."),
    ("Python with pandas, pypdf, pdfplumber, matplotlib", "Profile data, extract text, score searches", "Open source; each package's licence file was not read in the research", "permissive", "Check", "Course notes call these free and open source. Open each licence file and record it."),
    ("Tesseract OCR", "Read scanned pages", "Apache-2.0", "permissive", "Y", "Accuracy falls on faded scans. Licence says nothing about quality."),
    ("sentence-transformers", "Embeddings for meaning search", "Apache-2.0 for the library", "permissive", "Y", "Each model has its own licence on its model card. Fine-tuned copies can differ from the base model."),
    ("Chroma", "Store and search vectors", "Apache-2.0 per third-party summaries", "permissive", "Y", "Chroma Cloud is a separate paid service. The licence file itself was not read."),
    ("PostgreSQL with pgvector", "Store and search vectors in the main database", "PostgreSQL License", "permissive", "Y", "GitHub shows NOASSERTION for pgvector because it does not recognise the licence text. Read the file."),
    ("DuckDB and Parquet", "Fast analytical SQL on files", "MIT for DuckDB; Apache-2.0 for Parquet", "permissive", "Y", "The DuckDB Foundation holds the trademarks. No enterprise edition."),
    ("Great Expectations Core", "Quality rules a machine checks", "Apache-2.0 per the official site", "permissive", "Check", "Reports of a change of owner and of GX Cloud closing come from third-party sites and are unconfirmed."),
    ("OpenMetadata", "Data catalogue and lineage, shown by the tutor", "Apache-2.0 per the README", "permissive", "Check", "One comparison says parts ship under a Collate Community Licence that bars running a competing hosted service. Single source. Read the licence files."),
    ("Dagster or Apache Airflow", "Schedule pipeline steps, shown by the tutor", "Apache-2.0", "permissive", "Y", "Dagster+ is a paid product. A report that Prefect bought Dagster Labs is unconfirmed."),
    ("Microsoft Presidio", "Find and mask personal data", "MIT", "permissive", "Check", "One source says the project moved out of Microsoft. Confirm the current repository. Detection is not guaranteed complete."),
    ("Soda Core 4", "Data quality checks (not used in the labs)", "Elastic License 2.0 from version 4", "source-available", "Check", "Free for internal use, not open source, cannot be offered as a managed service. Sources disagree on the current text."),
    ("MinIO", "S3-compatible object store (not used in the labs)", "AGPLv3 server code; community builds stopped", "archived", "Check", "Reported no longer maintained in 2026. Teach any S3-compatible store instead. Sources differ on the dates."),
    ("Metabase open edition", "Dashboards (not used in the labs)", "AGPLv3, with a separate commercial licence", "copyleft", "Check", "Embedding the open edition means meeting the AGPL or buying a licence. Read Metabase's own licence page."),
    ("Docker Desktop", "Run containers on a laptop (not used in the labs)", "Docker subscription terms", "proprietary", "Check", "Free for individuals, education and small businesses. A group of Kitara's size needs a paid subscription. Use Python packages, Colab or Podman."),
]
LIC_ROWS = [(*r, "") for r in LIC]
check(len(LIC) == 15, "15 tools")
check({r[3] for r in LIC} == {"permissive", "copyleft", "source-available", "proprietary", "archived"}, "licence types")
write_csv("licence_register_sample.csv", ["tool", "use", "licence", "licence_type", "free_for_commercial_use", "caution", "checked_on"], LIC_ROWS)

# ------------------------------------------------------------------------------------------------ projected scorecard (baselines are read from the evidence file)
import pandas as pd
ev = pd.read_csv(DATA / "readiness_evidence.csv")
dims = list(dict.fromkeys(ev.dimension))
base = ev.groupby("dimension").proposed_score.mean()
adj = ev[ev.self_reported == "N"].groupby("dimension").proposed_score.mean()
TARGET = [3.5, 3.0, 3.5, 3.5, 3.0]
ACTION = [
    ("Board approves a written mandate and a budget owner for the first use case", "W01;W15"),
    ("Every source has an owner, a steward and a class, and six quality rules run on the customer table", "W02;W05;W06"),
    ("Raw, cleaned and serving zones run with freshness and schema alerts", "W07;W14"),
    ("Personal data is masked before indexing and permission filters are tested", "W12;W13"),
    ("A steering council meets monthly and every dataset in the plan has a named owner", "W01;W11"),
]
check(len(dims) == 5 and dims == ["Use cases and sponsorship", "Data: inventory, quality and metadata", "Platform and pipelines", "Protection and law", "People and governance"], f"dimension order {dims}")
SC = []
for d, t, (a, links) in zip(dims, TARGET, ACTION):
    SC.append((d, round(float(base[d]), 2), round(float(adj[d]), 2), t, round(t - float(base[d]), 2), a, links))
check(all(s[3] >= s[1] for s in SC), "targets must not fall below the baseline")
write_csv("scorecard_after.csv", ["dimension", "baseline_score", "evidence_adjusted_score", "projected_score_month_12", "change_from_baseline", "driving_action", "roadmap_items"], SC)

# ------------------------------------------------------------------------------------------------ dictionary, key, zip
DICT_ADD = f"""

{MARK}
Sessions 10 to 12 and their figures. All fictional. None of these files holds a price.

risk_register.csv   12 rows. Kitara's risks around data and AI.   Session 11
  id, risk, likelihood (1 to 5), impact (1 to 5), owner_role, current_control, status
  Score = likelihood x impact. The score is not stored: learners compute it. Bands used in the course: 15 and above high, 8 to 14 medium, below 8 low.
  Use: score, rank and plot the risks, then add an owner and a next action for each high one.

roadmap_items.csv   16 rows. Work items for Kitara over twelve months.   Session 12
  id, item, start_month (1 to 12), duration_months, effort_days, value (1 to 5), depends_on (ids, semicolon list, blank when none), owner_role
  An item that starts in month 4 and lasts 2 months occupies months 4 and 5. No item starts before the items it depends on have ended.
  Use: sequence by dependency, find the longest chain, chart as a Gantt, mark the rescore.

hosting_options.csv   4 rows. Four ways to host the search system, described in words only.   Session 10
  option, data_residency, latency_to_kampala (low, medium or high), capacity_risk, control, exit_difficulty, main_legal_check
  Use: compare options before any price is asked for. The Hosting Cost Model workbook holds the cost lines and no prices.

licence_register_sample.csv   15 rows. Tools named in the course and what the research found about their licences.   Session 10
  tool, use, licence, licence_type (permissive, copyleft, source-available, proprietary or archived), free_for_commercial_use (Y, N or Check), caution, checked_on (blank)
  The facts come from the course research notes of 29 October 2026, taken from search summaries and third-party pages. No licence file was read.
  Use: open each licence file, fill checked_on, and change Check to Y or N only after reading the file.

scorecard_after.csv   5 rows. Kitara's projected scores after twelve months.   Session 12
  dimension, baseline_score, evidence_adjusted_score (self reported items removed), projected_score_month_12, change_from_baseline, driving_action, roadmap_items
  The projection is a target set for planning, not a measurement. Rescoring in month 6 and month 12 tests it.
"""
dtxt = (DATA / "DATA DICTIONARY.txt").read_text(encoding="utf-8")
if MARK in dtxt:
    dtxt = dtxt[: dtxt.index(MARK)].rstrip("\n") + "\n"
(DATA / "DATA DICTIONARY.txt").write_text(dtxt.rstrip("\n") + "\n" + DICT_ADD, encoding="utf-8")

levels = {}
for lt in ("permissive", "copyleft", "source-available", "proprietary", "archived"):
    levels[lt] = sum(r[3] == lt for r in LIC)
risk_sorted = sorted(RISKS, key=lambda r: (-r[2] * r[3], r[0]))
EXTRA = dict(
    note="Added by build_extra_data.py. Every number here is computed from the five extra CSV files.",
    risk_register=dict(rows=12, high_ge_15=n_high, medium_8_to_14=n_mid, low_below_8=n_low,
                       high_ids=[r[0] for r in RISKS if r[2] * r[3] >= 15], medium_ids=[r[0] for r in RISKS if 8 <= r[2] * r[3] <= 14], low_ids=[r[0] for r in RISKS if r[2] * r[3] < 8],
                       scores={r[0]: r[2] * r[3] for r in RISKS}, top_risk=dict(id=risk_sorted[0][0], risk=risk_sorted[0][1], score=risk_sorted[0][2] * risk_sorted[0][3]),
                       mean_score=round(sum(risk_scores) / 12, 2)),
    roadmap=dict(items=16, critical_path_months=critical_months, critical_path_ids=path, last_month_used=12,
                 total_effort_days=sum(r[4] for r in ROAD), items_with_dependencies=sum(bool(r[6]) for r in ROAD),
                 no_dependency_starts_before_prerequisite_ends=True,
                 cannot_start_before_example=dict(item="W15", waits_for=["W12", "W13", "W07"], earliest_start_month=max(by_id[d][2] + by_id[d][3] for d in ("W12", "W13", "W07")),
                                                  planned_start_month=by_id["W15"][2]),
                 rescore_items=["W11 (month 6)", "W16 (months 11 and 12)"]),
    hosting=dict(options=4, prices_in_file=False, latency_low=[h[0] for h in HOST if h[2] == "low"], latency_medium=[h[0] for h in HOST if h[2] == "medium"], latency_high=[h[0] for h in HOST if h[2] == "high"]),
    licences=dict(tools=15, by_type=levels, free_Y=sum(r[4] == "Y" for r in LIC), free_N=sum(r[4] == "N" for r in LIC), free_Check=sum(r[4] == "Check" for r in LIC),
                  checked_on_filled=0, source="Research Notes.txt section 3 and curriculum.py TOOLS and AVOIDED; no licence file was read"),
    scorecard_after=dict(targets={s[0]: s[3] for s in SC}, baseline={s[0]: s[1] for s in SC}, evidence_adjusted={s[0]: s[2] for s in SC},
                         change={s[0]: s[4] for s in SC}, projected_overall=round(sum(TARGET) / 5, 2), baseline_overall=round(sum(s[1] for s in SC) / 5, 2),
                         evidence_adjusted_overall=round(sum(s[2] for s in SC) / 5, 2), biggest_gain=max(SC, key=lambda s: s[4])[0]),
)
kp = DATA / "answer_key.json"
key = json.loads(kp.read_text(encoding="utf-8"))
key["extra"] = EXTRA
kp.write_text(json.dumps(key, indent=2), encoding="utf-8")

ZIP = LEARN / "Practice Files" / "data.zip"
if ZIP.exists():
    ZIP.unlink()
with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
    for p in sorted(DATA.rglob("*")):
        if p.is_file() and p.name != "answer_key.json":
            zi = zipfile.ZipInfo(str(Path("data") / p.relative_to(DATA)), date_time=(2026, 10, 29, 9, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, p.read_bytes())
print(f"risks {n_high}/{n_mid}/{n_low}; critical path {critical_months} months via {'>'.join(path)}; data.zip {ZIP.stat().st_size / 1e6:.1f} MB")
