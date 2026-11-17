"""Tabular teaching data for Kitara Group: sources, readiness evidence, customers, mobile money log, users, lineage, branch reports.

Seeded numpy. Every defect count is chosen first, injected exactly, and measured again from the finished file by the caller.
"""
import hashlib, re
import numpy as np
import pandas as pd
from kitara_names import GIVEN_F, GIVEN_M, FAMILY, DISTRICTS_UG, national_id

LEVELS = ["Ad hoc", "Developing", "Defined", "Managed", "Optimised"]
DIMS = ["Use cases and sponsorship", "Data: inventory, quality and metadata", "Platform and pipelines", "Protection and law", "People and governance"]


# ============================================================= 1. sources.csv
def build_sources():
    cols = ["source_id", "name", "system_type", "format", "approx_records", "refresh", "owner", "steward", "sensitivity", "personal_data",
            "in_catalogue", "last_quality_check", "ai_use_case_candidates", "notes"]
    R = [
        ("S01", "Core banking system", "Database", "Relational tables", 640000, "daily", "Head of Retail Banking Operations", "Core Banking Data Analyst", "confidential", "Y", "N", "2026-03-14", "Customer 360; churn and dormancy prediction", ""),
        ("S02", "Mobile money switch log", "Log files and database", "CSV and database", 46000000, "daily", "IT", "", "restricted", "Y", "N", "", "Agent fraud and anomaly detection", "Owner recorded as IT. Digital Channels also says it owns this source."),
        ("S03", "Loan origination system", "Workflow application", "Database and scanned attachments", 58000, "daily", "Head of SME Lending", "Credit Operations Analyst", "internal", "Y", "N", "2025-11-20", "Loan document search; credit memo drafting", "Holds scanned national ID copies."),
        ("S04", "Policy administration system", "Database", "Relational tables", 210000, "daily", "Head of Underwriting", "Underwriting Systems Analyst", "restricted", "Y", "N", "2026-01-30", "Renewal prediction; underwriting assistant", ""),
        ("S05", "Claims system", "Database", "Relational tables", 96000, "daily", "Head of Claims", "", "restricted", "Y", "N", "2026-02-10", "Claims triage; days-to-settle prediction", ""),
        ("S06", "Claims documents archive", "File store", "PDF and scanned images", 310000, "ad hoc", "IT", "", "", "Y", "N", "", "Claims document search and summary", "Owner recorded as IT. Claims Department also says it owns this source."),
        ("S07", "CRM and tickets", "Software as a service", "Application database and exports", 1200000, "daily", "Head of Customer Service", "Customer Service Analyst", "restricted", "Y", "N", "2026-01-15", "Complaint classification; response drafting", ""),
        ("S08", "Call centre transcripts", "Audio and text files", "Text and audio", 380000, "weekly", "", "", "", "", "N", "", "Call summaries; complaint themes", "Nobody has reviewed what the transcripts contain."),
        ("S09", "Shared drive: policies and procedures", "File shares", "Word, PDF and text", 14000, "unknown", "", "", "", "", "N", "", "Staff policy question answering", "Several versions of the same policy sit in one folder."),
        ("S10", "HR system", "Software as a service", "Application database", 1800, "monthly", "Head of Human Resources", "HR Systems Officer", "restricted", "Y", "N", "2025-12-05", "HR policy assistant (not staff records)", "Holds salary data."),
        ("S11", "Finance ledger", "Enterprise resource planning", "Relational tables", 8400000, "daily", "Chief Finance Officer", "Finance Systems Accountant", "restricted", "N", "N", "2026-04-02", "Anomaly detection in journals", ""),
        ("S12", "Email archive", "Mail archive", "Email messages", 22000000, "daily", "", "", "", "", "N", "", "Not proposed. Too broad.", "No owner. Holds mixed personal and business content."),
        ("S13", "Branch report spreadsheets", "File shares", "Excel workbooks", 2300, "ad hoc", "", "", "", "N", "N", "", "Branch performance summary", "Six layouts seen in a sample of six branches."),
        ("S14", "Regulatory returns archive", "File store", "PDF and Excel", 1900, "monthly", "Head of Regulatory Reporting", "Compliance Officer", "restricted", "N", "N", "2026-02-27", "Return preparation checks", ""),
    ]
    df = pd.DataFrame(R, columns=cols)
    # what the sensitivity policy says each source should be (kept in the answer key, not in the file)
    expected = {"S01": "confidential", "S02": "restricted", "S03": "confidential", "S04": "restricted", "S05": "restricted", "S06": "confidential",
                "S07": "restricted", "S08": "confidential", "S09": "internal", "S10": "confidential", "S11": "restricted", "S12": "confidential",
                "S13": "internal", "S14": "restricted"}
    return df, expected


# ============================================================= 2. readiness_evidence.csv
def build_readiness():
    rows = [
        # dimension, item, what exists, who could verify, score, self_reported
        (DIMS[0], "Named executive sponsor", "The chief executive says in interviews that AI is a board priority. No written mandate or budget owner.", "Company Secretary (board papers)", 4, "Y"),
        (DIMS[0], "List of candidate use cases", "Eleven ideas were listed on one workshop slide in May 2026. No owners or data needs.", "Head of IT", 4, "Y"),
        (DIMS[0], "Business case for the first use", "A one-page case for document search over policies, with a pilot budget approved by IT Steering on 9 June 2026.", "Chair of IT Steering Committee", 3, "N"),
        (DIMS[0], "Funded budget", "UGX 38,000,000 pilot budget approved. No multi-year budget.", "Chief Finance Officer", 2, "N"),
        (DIMS[0], "Success measures", "No baseline for time to find an answer or days to settle a claim. Only the claims ratio is reported.", "Head of Claims", 2, "N"),
        (DIMS[1], "Source inventory", "A spreadsheet of 14 sources compiled for IT Steering. Four have no owner, five have no sensitivity class, none is in a catalogue.", "IT Steering Committee secretary", 2, "N"),
        (DIMS[1], "Quality monitoring", "Finance says customer data is checked every month. No rule list or result log was provided.", "Head of Retail Banking Operations", 3, "Y"),
        (DIMS[1], "Metadata and catalogue", "No catalogue. Column meanings are in two PDF files from the core banking vendor.", "Core Banking Data Analyst", 1, "N"),
        (DIMS[1], "Document version control", "The shared drive holds about 14,000 files. Three editions of the staff handbook sit in one folder.", "Head of Legal and Compliance", 1, "N"),
        (DIMS[1], "Customer master data", "The head of retail says one customer ID is used across systems. The Risk Committee noted two regulatory returns corrected because of duplicate customer records.", "Head of Risk", 3, "Y"),
        (DIMS[2], "Core data extract", "Nightly extract from core banking to a reporting database. Run log kept for 90 days.", "IT operations lead", 3, "N"),
        (DIMS[2], "Backup and recovery", "Business Continuity Plan sets four hours for core banking. A recovery test is held each March.", "Head of Risk", 3, "N"),
        (DIMS[2], "Analytics platform", "IT reports a reporting database and a data lake 'in progress'. No access was shown to the assessor.", "Head of IT", 3, "Y"),
        (DIMS[2], "Pipeline orchestration", "Scheduled jobs on two servers using cron. No dependency, retry or alert logic.", "IT operations lead", 2, "N"),
        (DIMS[2], "Monitoring of data freshness", "No freshness or volume alerts. A six-hour gap in the mobile money log was found by hand.", "IT operations lead", 2, "N"),
        (DIMS[2], "Environment for AI work", "An internal AI sandbox pilot is approved. It is not yet built.", "Head of IT", 2, "N"),
        (DIMS[3], "Registration and data protection officer", "Kitara says it is registered with the data protection regulator and has named an officer. The certificate was not seen.", "Head of Legal and Compliance", 4, "Y"),
        (DIMS[3], "Breach procedure", "The Information Security Policy sets one hour to report internally and 72 hours to report to the regulator.", "Head of IT Security", 3, "N"),
        (DIMS[3], "Classification scheme", "The Data Classification Standard has four classes. Two sources in the inventory carry the wrong class.", "Head of Legal and Compliance", 3, "N"),
        (DIMS[3], "Retention schedule", "A retention schedule exists. Legal says it is applied. No destruction list was provided.", "Head of Legal and Compliance", 3, "Y"),
        (DIMS[3], "Cross-border data flows", "Kitara Kenya data is processed in Kampala. No transfer assessment is on file.", "Head of Legal and Compliance", 2, "N"),
        (DIMS[4], "Named data owners", "Ten of 14 sources have an owner. Two owners are recorded as IT while a business unit also claims the source.", "Head of IT", 1, "N"),
        (DIMS[4], "Data governance forum", "The heads say a data council meets informally. There are no minutes.", "Company Secretary", 2, "Y"),
        (DIMS[4], "Policies for data and AI", "Classification, retention and acceptable AI use policies exist and were published in 2024 to 2026.", "Head of Legal and Compliance", 2, "N"),
        (DIMS[4], "Data and AI skills", "Two analysts in Finance and Risk. No data engineer. No AI training for staff.", "Head of Human Resources", 1, "N"),
    ]
    df = pd.DataFrame(rows, columns=["dimension", "item", "what_exists", "who_could_verify", "proposed_score", "self_reported"])
    df.insert(2, "level_name", [LEVELS[s - 1] for s in df.proposed_score])
    df.insert(0, "evidence_id", [f"E{i:02d}" for i in range(1, len(df) + 1)])
    return df


def readiness_expected(df):
    out = {}
    for d in DIMS:
        x = df[df.dimension == d]
        base = float(x.proposed_score.mean())
        adj = float(x[x.self_reported == "N"].proposed_score.mean())
        out[d] = dict(items=int(len(x)), baseline_mean=round(base, 2), mean_without_self_reported=round(adj, 2), change=round(adj - base, 2),
                      self_reported_items=int((x.self_reported == "Y").sum()))
    return out


# ============================================================= 3. customers.csv
BRANCH_DISTRICTS = ["Kampala"] * 9 + ["Wakiso"] * 6 + ["Mukono"] * 3 + ["Jinja"] * 3 + ["Mbarara"] * 3 + ["Gulu"] * 2 + ["Mbale"] * 2 + \
                   ["Masaka"] * 2 + ["Lira"] * 2 + ["Arua", "Kabale", "Hoima", "Soroti"] + ["Fort Portal"] * 2
assert len(BRANCH_DISTRICTS) == 38
PRODUCTS = ["Savings Account", "Current Account", "Fixed Deposit", "Salary Account", "Student Account", "Group Savings", "SME Loan", "School Fees Loan", "Mortgage", "Mobile Wallet"]
SEGMENTS = ["Mass market", "Affluent", "SME", "Student", "Corporate"]


def phone_fmt(num9, k):
    n = f"{num9:09d}"
    return [f"+256{n}", f"0{n}", f"256{n}", f"+256 {n[:3]} {n[3:6]} {n[6:]}" if k % 2 == 0 else f"0{n[:3]}-{n[3:6]}-{n[6:]}"]


def classify_phone(p):
    p = str(p)
    if re.fullmatch(r"\+256\d{9}", p): return "+256xxxxxxxxx"
    if re.fullmatch(r"0\d{9}", p): return "0xxxxxxxxx"
    if re.fullmatch(r"256\d{9}", p): return "256xxxxxxxxx"
    return "spaces or dashes"


def build_customers(seed=20261101):
    g = np.random.default_rng(seed)
    N, ND, N0 = 5000, 150, 4850
    bw = np.array([3.0 if d == "Kampala" else 2.2 if d == "Wakiso" else 1.0 for d in BRANCH_DISTRICTS])
    bidx = g.choice(38, N0, p=bw / bw.sum())
    branch = [f"KB{b + 1:03d}" for b in bidx]
    district = [BRANCH_DISTRICTS[b] for b in bidx]
    female = g.random(N0) < 0.52
    names = []
    for f in female:
        pool = GIVEN_F if f else GIVEN_M
        names.append(f"{pool[g.integers(0, len(pool))]} {FAMILY[g.integers(0, len(FAMILY))]}")
    # make sure the (name, dob) pairs are unique among real people so duplicates are the injected ones
    dob = pd.to_datetime("1946-01-01") + pd.to_timedelta(g.integers(0, 365 * 62, N0), unit="D")  # ages about 18 to 80 in 2026
    opened = pd.to_datetime("2011-01-01") + pd.to_timedelta(g.integers(0, 365 * 15 + 280, N0), unit="D")
    opened = np.minimum(opened.values, np.datetime64("2026-10-20"))
    num = g.choice(100000, N0, replace=False)
    fmt_k = g.choice(4, N0, p=[0.50, 0.28, 0.14, 0.08])
    nums9 = [7000_00000 + int(n) for n in num]
    phones = [phone_fmt(n, i)[k] for i, (n, k) in enumerate(zip(nums9, fmt_k))]
    gender_code = np.where(female, "F", "M").astype(object)
    gk = g.choice(4, N0, p=[0.70, 0.15, 0.10, 0.05])
    gender = []
    for f, k in zip(female, gk):
        gender.append(["F" if f else "M", "Female" if f else "Male", "f" if f else "m", "2" if f else "1"][k])
    emails = []
    for nm, i in zip(names, range(N0)):
        if g.random() < 0.68:
            dom = ["example.com", "example.org", "example.net"][g.integers(0, 3)]
            emails.append(f"{nm.lower().replace(' ', '.')}{g.integers(1, 99)}@{dom}")
        else:
            emails.append("")
    nid = [national_id(g) for _ in range(N0)]
    product = g.choice(PRODUCTS, N0, p=[.30, .10, .05, .17, .07, .06, .08, .06, .02, .09])
    segment = np.where(np.isin(product, ["SME Loan"]), "SME", np.where(product == "Student Account", "Student", g.choice(SEGMENTS[:2] + ["Corporate"], N0, p=[.82, .15, .03])))
    status = g.choice(["Active", "Dormant", "Closed", "Blocked"], N0, p=[.78, .13, .08, .01])
    stu = product == "Student Account"
    dob = pd.DatetimeIndex(np.where(stu, pd.to_datetime("2000-01-01") + pd.to_timedelta(g.integers(0, 365 * 8, N0), unit="D"), dob))
    df = pd.DataFrame(dict(full_name=names, gender=gender, date_of_birth=dob.strftime("%Y-%m-%d"), phone=phones, email=emails,
                           national_id=nid, district=district, branch_code=branch, product=product,
                           opened_date=pd.to_datetime(opened).strftime("%Y-%m-%d"), status=status, segment=segment))
    df["_phone_fmt"] = fmt_k

    # ---- exact defect slices, all disjoint
    perm = g.permutation(N0)
    cuts = dict(missing_nid=550, missing_dob=300, bad_dob=25, bad_opened=15, lower_branch=400, test=25)
    pos = 0
    sl = {}
    for k, v in cuts.items():
        sl[k] = perm[pos:pos + v]
        pos += v
    clean_pool = perm[pos:]  # rows with none of the exact-count defects
    df.loc[sl["missing_nid"], "national_id"] = ""
    df.loc[sl["missing_dob"], "date_of_birth"] = ""
    bad_dob_vals = ["2031-04-12", "2029-11-30", "2034-01-01", "2027-06-18", "2030-09-09", "2028-02-14", "2033-07-07", "2032-03-21", "2035-05-05", "2026-12-31", "2029-01-15", "2030-12-12",
                    "1850-01-01", "1888-06-15", "1899-12-31", "1805-03-03", "1870-10-10", "1890-02-28", "1875-07-04", "1862-09-19", "1899-01-01", "1840-08-08", "1895-05-20", "1881-11-11", "1866-04-04"]
    assert len(bad_dob_vals) == 25
    df.loc[sl["bad_dob"], "date_of_birth"] = bad_dob_vals
    fut = ["2027-02-03", "2026-12-15", "2028-08-08", "2027-11-11", "2029-03-03", "2030-01-01", "2026-11-30", "2027-05-05", "2031-10-10", "2026-12-01", "2028-12-12", "2027-07-07", "2029-09-09", "2026-11-15", "2032-02-02"]
    df.loc[sl["bad_opened"], "opened_date"] = fut
    df.loc[sl["lower_branch"], "branch_code"] = df.loc[sl["lower_branch"], "branch_code"].str.lower()
    t = sl["test"]
    df.loc[t[:13], "full_name"] = ["TEST ACCOUNT", "Test Account", "TEST", "test user", "TEST CUSTOMER", "Test Customer 2", "TEST ACCOUNT 3", "TEST", "Test", "TEST BRANCH", "test account", "TEST USER 4", "Test Customer"]
    df.loc[t[13:], "full_name"] = ["Demo Customer"] * 8 + ["Demo Customer 2", "DEMO CUSTOMER", "Demo Customer 3", "Demo customer"]
    # district spelling (Kampala 3 ways, Wakiso 3 ways); applied after the exact defects, to rows outside the duplicate pool
    kam = df.index[(df.district == "Kampala")].to_numpy()
    wak = df.index[(df.district == "Wakiso")].to_numpy()
    kk = g.choice(3, len(kam), p=[0.80, 0.12, 0.08])
    df.loc[kam, "district"] = np.array(["Kampala", "KAMPALA", "Kla"])[kk]
    wk = g.choice(3, len(wak), p=[0.85, 0.09, 0.06])
    df.loc[wak, "district"] = np.array(["Wakiso", "WAKISO", "Wak"])[wk]

    # ---- duplicates: copy rows from the clean pool
    src = g.choice(clean_pool, ND, replace=False)
    exact_src, near_src = src[:75], src[75:]
    dup = df.loc[src].copy()
    orig_idx = list(src)
    near = dup.iloc[75:].copy()
    new_names, new_phone = [], []
    for j, (idx, row) in enumerate(near.iterrows()):
        nm = row.full_name
        nm2 = [nm.upper(), nm.lower(), nm.title().replace(" ", "  "), nm.upper() + " "][j % 4]
        k_old = int(row._phone_fmt)
        k_new = (k_old + 1 + (j % 3)) % 4
        n9 = int(re.sub(r"\D", "", row.phone)[-9:])
        new_names.append(nm2)
        new_phone.append(phone_fmt(n9, j)[k_new])
    near["full_name"], near["phone"] = new_names, new_phone
    dup.iloc[75:] = near
    all_df = pd.concat([df, dup], ignore_index=True)
    ids = g.choice(np.arange(1000000, 9000000), N, replace=False)
    all_df.insert(0, "customer_id", [f"KT-{i:07d}" for i in ids])
    all_df["_orig"] = list(range(N0)) + orig_idx
    all_df["_is_dup"] = [0] * N0 + [1] * ND
    all_df["_dup_kind"] = [""] * N0 + ["exact"] * 75 + ["near"] * 75
    all_df["national_id_present"] = np.where(all_df.national_id.str.len() > 0, "Y", "N")
    all_df = all_df.sort_values("customer_id").reset_index(drop=True)
    cid_by_row = dict(zip(range(N), all_df.customer_id))
    # map original row index -> customer_id (original rows only)
    orig_cid = {}
    base = all_df[all_df._is_dup == 0]
    for i, r in zip(base._orig, base.customer_id):
        orig_cid[int(i)] = r
    pairs = [(orig_cid[int(o)], c, k) for o, c, k in zip(all_df[all_df._is_dup == 1]._orig, all_df[all_df._is_dup == 1].customer_id, all_df[all_df._is_dup == 1]._dup_kind)]
    hidden = all_df[["customer_id", "_is_dup", "_dup_kind"]].copy()
    cols = ["customer_id", "full_name", "gender", "date_of_birth", "phone", "email", "national_id_present", "national_id", "district", "branch_code",
            "product", "opened_date", "status", "segment"]
    return all_df[cols], hidden, pairs


def measure_customers(c):
    """Defect counts measured from the finished table, using only what a learner's rule would see."""
    today = pd.Timestamp("2026-10-29")
    dob = pd.to_datetime(c.date_of_birth.replace("", np.nan), errors="coerce")
    op = pd.to_datetime(c.opened_date, errors="coerce")
    m = {}
    m["rows"] = int(len(c))
    m["missing_national_id"] = int((c.national_id == "").sum())
    m["missing_date_of_birth"] = int((c.date_of_birth == "").sum())
    m["impossible_dob"] = int(((dob > today) | (dob < pd.Timestamp("1900-01-01"))).sum())
    m["impossible_opened_date"] = int(((op > today) | (op < pd.Timestamp("1900-01-01"))).sum())
    m["impossible_dates_total"] = m["impossible_dob"] + m["impossible_opened_date"]
    m["lowercase_branch_code"] = int((c.branch_code != c.branch_code.str.upper()).sum())
    nm = c.full_name.str.strip().str.lower()
    m["test_accounts"] = int(nm.str.match(r"^(test\b|demo customer)").sum())
    m["phone_formats"] = {k: int(v) for k, v in c.phone.map(classify_phone).value_counts().items()}
    m["gender_codes"] = {k: int(v) for k, v in c.gender.value_counts().items()}
    m["district_kampala_spellings"] = {k: int(v) for k, v in c.district[c.district.str.lower().isin(["kampala", "kla"])].value_counts().items()}
    m["district_wakiso_spellings"] = {k: int(v) for k, v in c.district[c.district.str.lower().isin(["wakiso", "wak"])].value_counts().items()}
    return m


# ============================================================= 4. mobile_money_log.csv
def build_mobile(seed=20261102):
    g = np.random.default_rng(seed)
    N, ND, NBAD, NZERO = 20000, 300, 160, 60
    nbase = N - ND
    start = pd.Timestamp("2026-09-01")
    hours = np.arange(30 * 24)
    hod = hours % 24
    prof = np.array([.12, .08, .06, .06, .08, .15, .35, .60, .85, 1.0, 1.0, .95, .95, .9, .85, .9, .95, 1.0, .85, .6, .45, .32, .22, .16])
    dow = ((hours // 24) + start.dayofweek) % 7
    w = prof[hod] * np.where(dow == 6, 0.65, np.where(dow == 5, 1.1, 1.0)) * np.where((hours // 24) % 30 > 24, 1.15, 1.0)
    gap_day = 16  # 17 September, zero based
    gap = (hours >= gap_day * 24 + 9) & (hours < gap_day * 24 + 15)
    w = np.where(gap, 0.0, w)
    hr = g.choice(hours, nbase, p=w / w.sum())
    sec = hr * 3600 + g.integers(0, 3600, nbase)
    ts = start + pd.to_timedelta(sec, unit="s")
    order = np.argsort(sec, kind="stable")
    ts = ts[order]
    nagents = 120
    aw = g.lognormal(0, 0.7, nagents)
    agent = g.choice(nagents, nbase, p=aw / aw.sum())
    agent_id = [f"AG{a + 1:04d}" for a in agent]
    pool = [hashlib.sha256(f"kitara-teaching-{i}".encode()).hexdigest()[:12] for i in range(3000)]
    sw = g.pareto(1.4, 3000) + 1
    msisdn = [pool[i] for i in g.choice(3000, nbase, p=sw / sw.sum())]
    typ = g.choice(["cash_in", "cash_out", "transfer", "bill_pay", "airtime"], nbase, p=[.30, .35, .15, .12, .08])
    amt = np.round(np.exp(g.normal(np.log(65000), 0.95, nbase)) / 500) * 500
    amt = np.clip(amt, 1000, 5000000).astype(np.int64)
    typ_airtime = typ == "airtime"
    amt = np.where(typ_airtime, np.minimum(amt, 50000), amt)
    status = g.choice(["success", "failed", "pending", "reversed"], nbase, p=[.955, .03, .01, .005])
    seq = {}
    ids = []
    for t in ts:
        d = t.strftime("%y%m%d")
        seq[d] = seq.get(d, 0) + 1
        ids.append(f"TX{d}{seq[d]:05d}")
    df = pd.DataFrame(dict(txn_id=ids, ts=ts, msisdn_hash=msisdn, agent_id=agent_id, amount_ugx=amt, type=typ, status=status))
    bad = g.choice(nbase, NBAD, replace=False)
    df.loc[bad[:NBAD - NZERO], "amount_ugx"] = -df.loc[bad[:NBAD - NZERO], "amount_ugx"]
    df.loc[bad[NBAD - NZERO:], "amount_ugx"] = 0
    good = np.setdiff1d(np.arange(nbase), bad)
    src = g.choice(good, ND, replace=False)
    dup = df.loc[src].copy()
    dup["ts"] = dup.ts + pd.to_timedelta(g.integers(1, 6, ND), unit="s")
    all_df = pd.concat([df, dup], ignore_index=True).sort_values(["ts", "txn_id"], kind="stable").reset_index(drop=True)
    alt = all_df.agent_id.isin([f"AG{a:04d}" for a in range(101, 113)])
    stamp = all_df.ts.dt.strftime("%Y-%m-%d %H:%M:%S")
    stamp_alt = all_df.ts.dt.strftime("%d/%m/%Y %H:%M")
    all_df["timestamp"] = np.where(alt, stamp_alt, stamp)
    out = all_df[["txn_id", "timestamp", "msisdn_hash", "agent_id", "amount_ugx", "type", "status"]]
    return out, all_df


def measure_mobile(m):
    ts = pd.to_datetime(m.timestamp.where(~m.timestamp.str.contains("/"), None), errors="coerce")
    alt = m.timestamp.str.contains("/")
    ts2 = pd.to_datetime(m.timestamp[alt], format="%d/%m/%Y %H:%M")
    full = pd.concat([ts.dropna(), ts2]).sort_index()
    gaps = full.sort_values().diff().dropna()
    srt = full.sort_values().reset_index(drop=True)
    gi = srt.diff().sort_values(ascending=False)
    top = float(gi.iloc[0].total_seconds() / 3600)
    second = float(gi.iloc[1].total_seconds() / 3600)
    i = int(gi.index[0])
    return dict(rows=int(len(m)), duplicate_txn_id_rows=int(m.txn_id.duplicated().sum()),
                negative_amounts=int((m.amount_ugx < 0).sum()), zero_amounts=int((m.amount_ugx == 0).sum()),
                largest_gap_hours=round(top, 2), second_largest_gap_hours=round(second, 2),
                gap_starts=str(srt[i - 1]), gap_ends=str(srt[i]), rows_in_slash_format=int(alt.sum()),
                agents_in_slash_format=int(m.agent_id[alt].nunique()))


# ============================================================= users, lineage
def build_users():
    rows = [
        ("U01", "Brian Opio", "Claims", "all_staff;claims", "Claims Officer"),
        ("U02", "Agnes Namukasa", "Claims", "all_staff;claims;underwriting", "Senior Claims Officer"),
        ("U03", "Esther Mutesi", "Human Resources", "all_staff;hr", "HR Officer"),
        ("U04", "Samuel Kyalo", "Branch Operations", "all_staff;branch_ops", "Branch Manager, Mbarara"),
        ("U05", "Winnie Atim", "Customer Service", "all_staff", "Customer Service Agent (general staff)"),
        ("U06", "Moses Ssali", "Legal and Compliance", "all_staff;legal_compliance;risk", "Internal Auditor"),
        ("U07", "Patricia Lubega", "Executive Office", "all_staff;executive", "General Manager, Strategy"),
        ("U08", "Charles Mwangi", "Finance", "all_staff;finance", "Finance Officer"),
        ("U09", "Doreen Nabirye", "Underwriting", "all_staff;underwriting", "Underwriter"),
        ("U10", "Hassan Kigozi", "Risk", "all_staff;risk", "Risk Analyst"),
        ("U11", "Faith Wambui", "Branch Operations", "all_staff;branch_ops", "Branch Officer, Kitara Kenya"),
        ("U12", "Denis Waiswa", "IT", "all_staff", "IT Security Analyst"),
    ]
    return pd.DataFrame(rows, columns=["user_id", "name", "department", "groups", "role"])


def build_lineage():
    E = [
        ("claims_system.claims", "staging.claims_raw", "Nightly extract at 01:00"),
        ("claims_system.claim_payments", "staging.payments_raw", "Nightly extract at 01:10"),
        ("policy_admin.policies", "staging.policies_raw", "Nightly extract at 01:20"),
        ("staging.claims_raw", "clean.claims", "Remove test claims; standardise dates"),
        ("staging.payments_raw", "clean.claim_payments", "Drop re-sent payment records"),
        ("staging.policies_raw", "clean.policies", "Standardise vehicle class and sum insured"),
        ("clean.claims", "mart.claims_fact", "Join to policy; compute days_to_settle"),
        ("clean.claim_payments", "mart.claims_fact", "Sum payments per claim"),
        ("clean.policies", "mart.claims_fact", "Join on policy number"),
        ("mart.claims_fact", "report.claims_turnaround_dashboard", "Daily refresh at 06:00"),
        ("mart.claims_fact", "report.monthly_claims_ratio", "Monthly query run by Finance"),
        ("report.monthly_claims_ratio", "regulatory.insurance_quarterly_return", "Copied by hand into the return workbook"),
        ("claims_doc_archive.files", "ocr.claims_text", "OCR on scanned pages; text read from PDFs"),
        ("ocr.claims_text", "search.claims_index", "Chunk, attach metadata and index"),
        ("core_banking.customer", "staging.customer_raw", "Nightly extract at 00:30"),
        ("staging.customer_raw", "clean.customer", "Fix phone format; remove test accounts; merge duplicates"),
        ("clean.customer", "mart.customer_360", "Join customer to products"),
        ("crm.contacts", "mart.customer_360", "Match on phone number"),
        ("mobile_money.switch_log", "staging.mm_raw", "Hourly file drop"),
        ("staging.mm_raw", "clean.mm_transactions", "Remove duplicate txn_id; parse both timestamp formats"),
        ("clean.mm_transactions", "mart.customer_360", "Monthly activity per customer"),
        ("mart.customer_360", "report.customer_base_dashboard", "Daily refresh at 06:30"),
        ("mart.customer_360", "regulatory.bank_quarterly_return", "Quarterly query run by Regulatory Reporting"),
        ("report.claims_turnaround_dashboard", "board.quarterly_pack", "Screenshot pasted into the pack"),
        ("report.customer_base_dashboard", "board.quarterly_pack", "Screenshot pasted into the pack"),
    ]
    assert len(E) == 25
    return pd.DataFrame(E, columns=["from_asset", "to_asset", "step"])


# ============================================================= 10. branch_reports (six messy layouts)
def build_branch_reports(outdir, seed=20261103):
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment
    g = np.random.default_rng(seed)
    outdir.mkdir(parents=True, exist_ok=True)
    cal = Font(name="Calibri", size=11)
    bold = Font(name="Calibri", size=11, bold=True)
    center = Alignment(horizontal="center", vertical="center")
    prods = ["Savings", "Current", "Salary", "Student", "Group savings", "School fees loan", "SME loan"]
    made = []

    def vals(scale=1.0):
        return dict(new=[int(g.integers(20, 140) * scale) for _ in prods], dep=[int(g.integers(30, 400) * 1e6 * scale / 1) for _ in prods])

    # 1 Kampala Road: title merged, header row 4, totals row in the middle, note rows
    wb = Workbook(); ws = wb.active; ws.title = "Sep"
    ws.merge_cells("A1:F1"); ws["A1"] = "KITARA BANK - KAMPALA ROAD BRANCH - MONTHLY REPORT SEPTEMBER 2026"; ws["A1"].font = bold; ws["A1"].alignment = center
    ws["A2"] = "Prepared by: Operations Officer"; ws["E2"] = "Date:"; ws["F2"] = "2026-10-02"
    for j, h in enumerate(["Product", "New accounts", "Closed", "Deposits mobilised (UGX)", "Loans disbursed (UGX)", "Remarks"], 1):
        ws.cell(4, j, h).font = bold
    v = vals()
    r = 5
    for i, p in enumerate(prods):
        ws.cell(r, 1, p); ws.cell(r, 2, v["new"][i]); ws.cell(r, 3, int(g.integers(0, 12))); ws.cell(r, 4, v["dep"][i]); ws.cell(r, 5, int(g.integers(0, 90) * 1e6) if "loan" in p else 0)
        if i == 3: r += 1; ws.cell(r, 1, "SUB-TOTAL (first four)"); ws.cell(r, 2, f"=SUM(B5:B8)"); ws.cell(r, 4, "=SUM(D5:D8)")
        r += 1
    ws.cell(r + 1, 1, "TOTAL"); ws.cell(r + 1, 2, "=SUM(B5:B12)-B9"); ws.cell(r + 1, 4, "=SUM(D5:D12)-D9")
    ws.cell(r + 3, 1, "Note: figures for school fees loan include Sept 28-30 estimates."); ws.column_dimensions["A"].width = 26
    for c in "BCDEF": ws.column_dimensions[c].width = 22
    wb.save(outdir / "Branch Report - Kampala Road - Sep 2026.xlsx"); made.append(("Branch Report - Kampala Road - Sep 2026.xlsx", "title merged over six columns; header on row 4; sub-total row inside the data; formulas; a note under the table"))

    # 2 Ntinda: month columns with merged group headers, header on row 6
    wb = Workbook(); ws = wb.active; ws.title = "Return"
    ws["A1"] = "Ntinda Branch"; ws["A2"] = "Quarterly return Q3 2026 (July to September)"; ws["A3"] = "Branch code: kb004"
    ws.merge_cells("B5:D5"); ws["B5"] = "New accounts"; ws.merge_cells("E5:G5"); ws["E5"] = "Deposits (UGX millions)"
    for c in ("B5", "E5"): ws[c].alignment = center; ws[c].font = bold
    for j, h in enumerate(["Product", "Jul", "Aug", "Sep", "Jul", "Aug", "Sep"], 1): ws.cell(6, j, h).font = bold
    for i, p in enumerate(prods[:6]):
        ws.cell(7 + i, 1, p)
        for j in range(2, 5): ws.cell(7 + i, j, int(g.integers(10, 90)))
        for j in range(5, 8): ws.cell(7 + i, j, round(float(g.uniform(20, 300)), 1))
    ws.cell(14, 1, "Complaints received"); ws.cell(14, 2, 14); ws.cell(14, 3, 9); ws.cell(14, 4, 11)
    wb.save(outdir / "Ntinda Branch Quarterly Return Q3.xlsx"); made.append(("Ntinda Branch Quarterly Return Q3.xlsx", "months across the columns; merged group headers over three columns each; header on row 6; branch code in lower case"))

    # 3 Entebbe: numbers stored as text with currency, mixed date formats, two sheets
    wb = Workbook(); ws = wb.active; ws.title = "Accounts"
    for j, h in enumerate(["Date", "Product", "Opened", "Deposit"], 1): ws.cell(1, j, h)
    for i in range(14):
        d = pd.Timestamp("2026-09-01") + pd.Timedelta(days=int(g.integers(0, 29)))
        ws.cell(2 + i, 1, d.strftime(["%d/%m/%Y", "%Y-%m-%d", "%d %b %Y"][i % 3]))
        ws.cell(2 + i, 2, prods[i % 7]); ws.cell(2 + i, 3, int(g.integers(1, 15))); ws.cell(2 + i, 4, f"UGX {int(g.integers(2, 90) * 1e6):,}")
    ws2 = wb.create_sheet("Loans")
    for j, h in enumerate(["Loan type", "Amount disbursed", "PAR30 %"], 1): ws2.cell(1, j, h)
    for i, p in enumerate(["School fees loan", "SME loan", "Mortgage"]):
        ws2.cell(2 + i, 1, p); ws2.cell(2 + i, 2, f"UGX {int(g.integers(20, 400) * 1e6):,}"); ws2.cell(2 + i, 3, f"{g.uniform(2, 11):.1f}%")
    wb.save(outdir / "Entebbe Sep26.xlsx"); made.append(("Entebbe Sep26.xlsx", "two sheets; amounts stored as text with the UGX prefix; three date formats in one column"))

    # 4 Jinja: transposed layout, units in column B, blank rows between sections
    wb = Workbook(); ws = wb.active; ws.title = "report"
    ws["A1"] = "JINJA MAIN BRANCH"; ws["A2"] = "Report month:"; ws["B2"] = "2026-09"
    rows = [("SECTION A: CUSTOMERS", None, None), ("New accounts", "count", int(g.integers(120, 400))), ("Closed accounts", "count", int(g.integers(5, 40))),
            ("Active customers", "count", int(g.integers(6000, 12000))), (None, None, None), ("SECTION B: MONEY", None, None),
            ("Deposits mobilised", "UGX m", round(float(g.uniform(900, 3000)), 1)), ("Loans disbursed", "UGX m", round(float(g.uniform(200, 1200)), 1)),
            ("Portfolio at risk 30 days", "%", round(float(g.uniform(3, 9)), 1)), (None, None, None), ("SECTION C: SERVICE", None, None),
            ("Complaints received", "count", int(g.integers(20, 90))), ("Average queue time", "minutes", int(g.integers(9, 30))), ("Staff on duty", "count", 24)]
    for i, (a, b, c) in enumerate(rows, start=4):
        ws.cell(i, 1, a); ws.cell(i, 2, b); ws.cell(i, 3, c)
        if a and a.startswith("SECTION"): ws.cell(i, 1).font = bold
    ws.cell(20, 1, "* queue time measured on Fridays only")
    wb.save(outdir / "Jinja_main_branch_report_2026-09.xlsx"); made.append(("Jinja_main_branch_report_2026-09.xlsx", "metrics down the rows with units in column B; blank rows and section headings; a footnote in the cells"))

    # 5 Mbarara: different header names, N/A and dashes, comments
    from openpyxl.comments import Comment
    wb = Workbook(); ws = wb.active; ws.title = "KPI"
    for j, h in enumerate(["Item", "Target", "Actual", "Variance", "Acct opened", "Cust complaints"], 1): ws.cell(1, j, h).font = bold
    k = [("Savings", 120, 134), ("Current", 25, 19), ("Salary", 60, "N/A"), ("Student", 40, 52), ("Group savings", 8, 9), ("School fees loan", 30, "-"), ("SME loan", 22, 18)]
    for i, (p, t, a) in enumerate(k, start=2):
        ws.cell(i, 1, p); ws.cell(i, 2, t); ws.cell(i, 3, a); ws.cell(i, 4, f'=IF(ISNUMBER(C{i}),C{i}-B{i},"")'); ws.cell(i, 5, int(g.integers(5, 60))); ws.cell(i, 6, int(g.integers(0, 6)))
    ws["C4"].comment = Comment("System was down 2 days, figure to follow.", "Branch Manager")
    wb.save(outdir / "Mbarara Branch KPI.xlsx"); made.append(("Mbarara Branch KPI.xlsx", "different header names for the same measures; N/A and dash in numeric cells; a cell comment; formulas that return blank"))

    # 6 Nairobi Westlands: KES, merged branch name, hidden column, header row 3
    wb = Workbook(); ws = wb.active; ws.title = "Sep 2026"
    ws.merge_cells("A1:E1"); ws["A1"] = "KITARA KENYA - WESTLANDS BRANCH - SEPTEMBER 2026 (amounts in KES)"; ws["A1"].font = bold
    for j, h in enumerate(["Product", "Internal code", "New accounts", "Deposits (KES)", "Loans (KES)"], 1): ws.cell(3, j, h).font = bold
    for i, p in enumerate(["Savings", "Current", "Salary", "Student", "Mobile wallet", "SME loan"], start=4):
        ws.cell(i, 1, p); ws.cell(i, 2, f"P-{int(g.integers(100, 999))}"); ws.cell(i, 3, int(g.integers(15, 120))); ws.cell(i, 4, int(g.integers(4, 90) * 1e6)); ws.cell(i, 5, int(g.integers(0, 40) * 1e6) if p == "SME loan" else 0)
    ws.column_dimensions["B"].hidden = True
    ws.cell(12, 1, "Prepared by"); ws.cell(12, 3, "Branch Officer"); ws.cell(13, 1, "Checked by"); ws.cell(13, 3, "")
    wb.save(outdir / "Nairobi Westlands - Branch Report Sept 2026.xlsx"); made.append(("Nairobi Westlands - Branch Report Sept 2026.xlsx", "Kenya shillings; a hidden column; header on row 3; unsigned check line"))
    return made
