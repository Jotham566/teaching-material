"""Generate the Kitara Group teaching data for Enterprise Data Readiness for AI.

  python3 build_teaching_data.py [COURSE_ROOT] [--no-assert] [--skip-lo]

Writes, under COURSE_ROOT/03 Learner Materials/:
  Practice Files/data/        sources, readiness evidence, customers, mobile money log, ~120 documents, metadata, users,
                              evaluation questions, lineage edges, branch reports, answer_key.json, DATA DICTIONARY.txt
  Practice Files/data.zip     the data folder without answer_key.json (learners get the zip)
  Workpiece Templates/        nine workbooks, a Kitara example scorecard and a board paper outline

Deterministic: fixed seeds everywhere and fixed file dates, so a re-run gives identical bytes. Runs in under a minute (OCR of the eight scans is the slowest step). Everything is fictional.
Helper modules in this folder: kitara_search.py (chunking and search, imported by later sessions), kitara_docs_a/b/c.py (document
text), kitara_render.py, kitara_tables.py, kitara_templates.py, kitara_questions.py, kitara_names.py.
Packages: numpy, pandas, openpyxl, reportlab, python-docx, pypdf, pdfplumber, PIL, pytesseract, the tesseract and pdftoppm programs.
"""
import sys, os, re, json, time, shutil, zipfile, subprocess, tempfile, datetime as dt
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import numpy as np
import pandas as pd
from reportlab import rl_config
rl_config.invariant = 1
from openpyxl import Workbook, load_workbook

T0 = time.time()
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
NO_ASSERT = "--no-assert" in sys.argv
SKIP_LO = "--skip-lo" in sys.argv or os.environ.get("SKIP_LO") == "1"
ROOT = Path(ARGS[0]) if ARGS else HERE.parents[2]
LEARN = ROOT / "03 Learner Materials"
DATA = LEARN / "Practice Files" / "data"
TEMPL = LEARN / "Workpiece Templates"
FIXED = dt.datetime(2026, 10, 29, 9, 0, 0)

# fixed file properties so a re-run gives the same workbooks
_orig_save = Workbook.save


def _save(self, fn):
    from openpyxl.worksheet.properties import PageSetupProperties
    for _ws in self.worksheets:
        _ws.page_setup.orientation = "landscape"
        _ws.page_setup.fitToWidth = 1
        _ws.page_setup.fitToHeight = 0
        _ws.sheet_properties.pageSetUpPr = PageSetupProperties(fitToPage=True)
    self.properties.created = self.properties.modified = FIXED
    self.properties.creator = "Kitara course build"
    _orig_save(self, fn)


Workbook.save = _save

import kitara_docs_a, kitara_docs_b, kitara_docs_c
from kitara_docs_a import DOCS
import kitara_tables as KT
import kitara_render as KR
import kitara_search as KS
import kitara_templates as TP
from kitara_questions import questions
from kitara_names import fmt_ugx

FAILS = []


def check(cond, msg):
    if not cond:
        FAILS.append(msg)
        print("  ASSERTION FAILED:", msg)
    return cond


def log(msg):
    print(f"[{time.time() - T0:6.1f}s] {msg}", flush=True)


# ============================================================================ reset output
if DATA.exists():
    shutil.rmtree(DATA)
(DATA / "docs").mkdir(parents=True)
TEMPL.mkdir(parents=True, exist_ok=True)
KEY = {"generated": "2026-10-29", "case": "Kitara Group (fictional bank and insurer, Kampala, with Kitara Kenya in Nairobi)"}

# ============================================================================ 1. sources
src, expected_class = KT.build_sources()
src.to_csv(DATA / "sources.csv", index=False)
blank = lambda c: int((src[c].fillna("") == "").sum())
KEY["sources"] = dict(
    count=int(len(src)), no_owner=blank("owner"), no_steward=blank("steward"), no_sensitivity_class=blank("sensitivity"),
    personal_data_blank=blank("personal_data"), in_catalogue_Y=int((src.in_catalogue == "Y").sum()), in_catalogue_N=int((src.in_catalogue == "N").sum()),
    no_quality_check_on_record=blank("last_quality_check"),
    no_owner_ids=list(src.source_id[src.owner.fillna("") == ""]), no_steward_ids=list(src.source_id[src.steward.fillna("") == ""]),
    no_sensitivity_ids=list(src.source_id[src.sensitivity.fillna("") == ""]), personal_data_blank_ids=list(src.source_id[src.personal_data.fillna("") == ""]),
    owner_recorded_as_IT_but_business_unit_also_claims=list(src.source_id[src.notes.str.contains("also says it owns")]),
    wrong_sensitivity=[dict(source_id="S03", recorded="internal", should_be="confidential", why="holds scanned national ID copies"),
                       dict(source_id="S10", recorded="restricted", should_be="confidential", why="holds salary data; the Data Classification Standard puts salary data in confidential")],
    expected_sensitivity_by_source=expected_class,
    sources_with_no_owner_and_no_class=list(src.source_id[(src.owner.fillna("") == "") & (src.sensitivity.fillna("") == "")]),
    rows_with_any_blank_key_field=int(((src[["owner", "steward", "sensitivity", "personal_data"]].fillna("") == "").any(axis=1)).sum()),
)
assert KEY["sources"]["no_owner"] == 4 and KEY["sources"]["no_steward"] == 7 and KEY["sources"]["no_sensitivity_class"] == 5 and KEY["sources"]["personal_data_blank"] == 3
log("sources.csv")

# ============================================================================ 2. readiness evidence
rd = KT.build_readiness()
rd.to_csv(DATA / "readiness_evidence.csv", index=False)
rx = KT.readiness_expected(rd)
target = {KT.DIMS[0]: 3.0, KT.DIMS[1]: 2.0, KT.DIMS[2]: 2.5, KT.DIMS[3]: 3.0, KT.DIMS[4]: 1.5}
for d, t in target.items():
    check(abs(rx[d]["baseline_mean"] - t) < 1e-9, f"baseline for {d} is {rx[d]['baseline_mean']}, expected {t}")
check(sum(abs(v["change"]) >= 0.5 for v in rx.values()) >= 2, "discounting self-reported items must move at least two dimensions by 0.5")
check(all(4 <= v["items"] <= 6 for v in rx.values()), "each dimension needs 4 to 6 items")
KEY["readiness"] = dict(by_dimension=rx, overall_baseline=round(float(np.mean([v["baseline_mean"] for v in rx.values()])), 2),
                        overall_without_self_reported=round(float(np.mean([v["mean_without_self_reported"] for v in rx.values()])), 2),
                        weakest_dimension=min(rx, key=lambda d: rx[d]["baseline_mean"]),
                        weakest_dimension_without_self_reported=min(rx, key=lambda d: rx[d]["mean_without_self_reported"]),
                        dimensions_moved_by_0_5_or_more=[d for d, v in rx.items() if abs(v["change"]) >= 0.5],
                        evidence_items=int(len(rd)), self_reported_items=int((rd.self_reported == "Y").sum()))
log("readiness_evidence.csv")

# ============================================================================ 3. customers
cust, hidden, pairs = KT.build_customers()
cust.to_csv(DATA / "customers.csv", index=False)
cm = KT.measure_customers(cust)
exact_n = sum(1 for p in pairs if p[2] == "exact")
cm.update(duplicate_rows=int(len(pairs)), duplicate_exact=exact_n, duplicate_near=int(len(pairs) - exact_n),
          duplicate_percent=round(100 * len(pairs) / len(cust), 2), unique_people=int(len(cust) - len(pairs)),
          missing_national_id_percent=round(100 * cm["missing_national_id"] / len(cust), 2), missing_dob_percent=round(100 * cm["missing_date_of_birth"] / len(cust), 2),
          lowercase_branch_percent=round(100 * cm["lowercase_branch_code"] / len(cust), 2),
          duplicate_pairs_first_10=[list(p) for p in pairs[:10]], duplicate_pairs_all=[list(p) for p in pairs],
          national_id_present_N=int((cust.national_id_present == "N").sum()),
          rule_hints=dict(phone_valid_after_cleaning="digits only, 9 digits after 256, starts with 7", impossible_date_rule="date_of_birth between 1900-01-01 and 2026-10-29; opened_date not after 2026-10-29",
                          duplicate_rule="same national_id (when present), or same lower-case name with the same date_of_birth, different customer_id"))
check(cm["rows"] == 5000, "customers must have 5000 rows")
check(cm["missing_national_id"] == 550 and cm["missing_date_of_birth"] == 300, "missing counts")
check(cm["impossible_dates_total"] == 40, f"impossible dates {cm['impossible_dates_total']}")
check(cm["lowercase_branch_code"] == 400 and cm["test_accounts"] == 25, "lowercase branch or test account counts")
check(len(cm["phone_formats"]) == 4 and len(cm["gender_codes"]) == 8, "four phone formats and eight gender code values")
check(cm["duplicate_rows"] == 150, "150 duplicate rows")
# verify the duplicate rule a learner would write finds exactly the injected pairs
nm = cust.full_name.str.strip().str.lower().str.replace(r"\s+", " ", regex=True)
key = nm + "|" + cust.date_of_birth
ok_rows = cust.national_id != ""
found_by_nid = cust[ok_rows].national_id.duplicated(keep="first").sum()
cm["duplicates_found_by_national_id_rule"] = int(found_by_nid)
check(int(found_by_nid) == 150, f"duplicate rule on national_id finds {found_by_nid}, expected 150")
KEY["customers"] = cm
log("customers.csv")

# ============================================================================ 4. mobile money
mm, mm_full = KT.build_mobile()
mm.to_csv(DATA / "mobile_money_log.csv", index=False)
mmm = KT.measure_mobile(mm)
check(mmm["rows"] == 20000 and mmm["duplicate_txn_id_rows"] == 300, "mobile money rows or duplicates")
check(mmm["negative_amounts"] + mmm["zero_amounts"] == 160, "mobile money bad amounts")
check(6.0 <= mmm["largest_gap_hours"] <= 6.5 and mmm["second_largest_gap_hours"] < 3, f"gap {mmm['largest_gap_hours']} / {mmm['second_largest_gap_hours']}")
mmm.update(duplicate_percent=round(100 * mmm["duplicate_txn_id_rows"] / mmm["rows"], 2), bad_amount_percent=round(100 * (mmm["negative_amounts"] + mmm["zero_amounts"]) / mmm["rows"], 2),
           slash_format_agents="AG0101 to AG0112", period="2026-09-01 to 2026-09-30")
KEY["mobile_money_log"] = mmm
log("mobile_money_log.csv")

# ============================================================================ 9. users, lineage
users = KT.build_users()
users.to_csv(DATA / "users.csv", index=False)
lin = KT.build_lineage()
lin.to_csv(DATA / "lineage_edges.csv", index=False)
KEY["lineage"] = dict(edges=int(len(lin)), claims_chain_edges=14, customer_chain_edges=11,
                      assets=int(len(set(lin.from_asset) | set(lin.to_asset))),
                      upstream_of_claims_turnaround_dashboard=["mart.claims_fact", "clean.claims", "clean.claim_payments", "clean.policies", "staging.claims_raw", "staging.payments_raw",
                                                                "staging.policies_raw", "claims_system.claims", "claims_system.claim_payments", "policy_admin.policies"],
                      downstream_of_core_banking_customer=["staging.customer_raw", "clean.customer", "mart.customer_360", "report.customer_base_dashboard", "regulatory.bank_quarterly_return", "board.quarterly_pack"])
KEY["users"] = dict(count=int(len(users)))
check(len(lin) == 25 and len(users) == 12, "lineage 25 edges and 12 users")
log("users.csv, lineage_edges.csv")

# ============================================================================ 10. branch reports
made = KT.build_branch_reports(DATA / "branch_reports")
KEY["branch_reports"] = [dict(file=f, layout=d) for f, d in made]
log("branch_reports")

# ============================================================================ 5. documents
kitara_docs_c.build_letters()
LF = {f["tag"]: f for f in kitara_docs_c.LETTER_FACTS}
TWO_COL = {"g_home", "retention", "infosec", "g_group", "complaints"}
for i, d in enumerate(DOCS, start=1):
    d["doc_id"] = f"D{i:03d}"
    if d["tag"] in TWO_COL:
        d["cols"] = 2
tag2id = {d["tag"]: d["doc_id"] for d in DOCS}
check(len(set(d["file"] for d in DOCS)) == len(DOCS), "file names must be unique")
n_docs = len(DOCS)
HEAVY_SEEDS = {"s_loannote": 105, "s_fax2017": 109, "s_policy2015": 109}
SERIF = {"s_circ2016", "s_board2019"}
ocr_cache, scan_report = {}, []
DOCDIR = DATA / "docs"
for i, d in enumerate(DOCS):
    p = DOCDIR / d["file"]
    p.parent.mkdir(parents=True, exist_ok=True)
    f = d["format"]
    if f == "text_pdf":
        KR.render_text_pdf(d, p)
    elif f == "docx":
        KR.render_docx(d, p)
    elif f == "txt":
        KR.render_txt(d, p)
    elif f == "scanned_pdf":
        heavy = d["meta_note"] == "heavy"
        seed0 = HEAVY_SEEDS.get(d["tag"], 100 + i)
        for attempt in range(14):
            KR.render_scan(d, p, seed0 + attempt, serif=d["tag"] in SERIF)
            txt = KR.ocr_pdf(p)
            c = KR.cer(d["body"], txt)
            good = (0.05 <= c <= 0.8) if heavy else (c <= 0.05)
            if good:
                break
        ocr_cache[p.name] = txt
        scan_report.append(dict(doc_id=d["doc_id"], file=d["file"], degradation="heavy" if heavy else "normal", character_error_rate=round(c, 4), seed=seed0 + attempt,
                                ocr_characters=len(" ".join(txt.split())), source_characters=len(" ".join(d["body"].split()))))
log(f"{n_docs} documents rendered")

# ---- metadata
def pages_of(d):
    p = DOCDIR / d["file"]
    if d["format"] in ("text_pdf", "scanned_pdf"):
        from pypdf import PdfReader
        return len(PdfReader(str(p)).pages)
    words = len(d["body"].split())
    return max(1, int(np.ceil(words / 450)))


meta = pd.DataFrame([dict(doc_id=d["doc_id"], file=d["file"], title=d["title"], family=d["family"], version=d["version"], status=d["status"],
                          effective_date=d["effective_date"], owner_department=d["owner_department"], sensitivity=d["sensitivity"],
                          access_groups=d["access_groups"], language=d["language"], format=d["format"], pages=pages_of(d),
                          contains_personal_data=d["contains_personal_data"]) for d in DOCS])
meta.to_csv(DATA / "docs_metadata.csv", index=False)
check(n_docs >= 115, f"about 120 documents, got {n_docs}")
fmt_counts = meta.format.value_counts().to_dict()
check(fmt_counts.get("docx") == 10 and fmt_counts.get("txt") == 6 and fmt_counts.get("scanned_pdf") == 8, f"format counts {fmt_counts}")
check(int((meta.sensitivity == "confidential").sum()) >= 6, "at least 6 confidential documents")
check(set(";".join(meta.access_groups).split(";")) <= {"all_staff", "claims", "underwriting", "hr", "finance", "legal_compliance", "risk", "branch_ops", "executive"}, "access group names")

# ---- extraction checks (what a learner sees with pypdf)
from pypdf import PdfReader
import pdfplumber
ext_ok, ext_empty = [], []
for d in DOCS:
    if d["format"] == "text_pdf":
        t = "\n".join((pg.extract_text() or "") for pg in PdfReader(str(DOCDIR / d["file"])).pages)
        ext_ok.append(len(t.strip()))
    elif d["format"] == "scanned_pdf":
        t = "\n".join((pg.extract_text() or "") for pg in PdfReader(str(DOCDIR / d["file"])).pages)
        ext_empty.append(len(t.strip()))
check(min(ext_ok) > 200, f"every text PDF returns text through pypdf (shortest {min(ext_ok)} characters)")
check(max(ext_empty) < 20, f"scanned PDFs return near-empty text through pypdf (longest {max(ext_empty)})")
table_report = []
for d in DOCS:
    if d.get("table"):
        p = DOCDIR / d["file"]
        txt = "\n".join((pg.extract_text() or "") for pg in PdfReader(str(p)).pages)
        lines = txt.splitlines()
        rows = d["table"][1:]
        same = sum(any(r[0] in ln and r[1] in ln for ln in lines) for r in rows)
        with pdfplumber.open(str(p)) as pl:
            tb = pl.pages[0].extract_tables()
        tb = tb[0] if tb else []
        recovered = sum(1 for r in d["table"] if any([c.strip() for c in x] == [str(v) for v in r] for x in tb))
        table_report.append(dict(file=d["file"], rows=len(rows), rows_kept_together_by_pypdf=int(same), rows_recovered_by_pdfplumber=int(recovered - 1 if recovered else 0),
                                 pdfplumber_table_found=bool(tb)))
        check(same == 0, f"{d['file']}: pypdf keeps {same} table rows together; expected the columns to be scrambled")
        check(recovered == len(d["table"]), f"{d['file']}: pdfplumber recovered {recovered} of {len(d['table'])} table rows")
log("extraction checks")

# ---- scans
cer_normal = [s["character_error_rate"] for s in scan_report if s["degradation"] == "normal"]
cer_heavy = [s["character_error_rate"] for s in scan_report if s["degradation"] == "heavy"]
check(len(cer_heavy) >= 2 and min(cer_heavy) >= 0.05 and max(cer_normal) <= 0.05 and min(cer_heavy) > 2 * max(cer_normal), f"scan error rates normal {cer_normal} heavy {cer_heavy}")
KEY["scans"] = dict(count=len(scan_report), tool="tesseract via pytesseract at 150 dpi, English", per_scan=scan_report,
                    normal_max_cer=max(cer_normal), heavy_min_cer=min(cer_heavy), heavy_documents=[s["file"] for s in scan_report if s["degradation"] == "heavy"],
                    note="Character error rate = edit distance between OCR text and the known source text, after collapsing white space, divided by source length. Another Tesseract version can give slightly different values.")
KEY["table_pdfs"] = table_report

# ============================================================================ 6/8 search evaluation
corpus = KS.load_corpus(DATA, ocr_cache=ocr_cache)
corpus["n_words"] = corpus.text.str.split().str.len()
chunks = KS.build_chunks(corpus)
S = KS.Searcher(chunks, depth=50)
log(f"search index: {len(chunks)} chunks over {len(corpus)} documents")
norm = lambda s: " ".join(str(s).lower().split())
Q = questions(LF)
status_of = dict(zip(meta.doc_id, meta.status))
groups_of = dict(zip(meta.doc_id, meta.access_groups))
users_by_group = {g: " ".join(users.loc[users.groups.str.contains(g), "user_id"]) for g in ["claims", "hr", "branch_ops", "legal_compliance", "executive", "underwriting", "all_staff"]}
rows = []
for n, q in enumerate(Q, start=1):
    gold = tag2id[q["gold"]]
    ctext = norm(corpus.loc[corpus.doc_id == gold, "text"].iloc[0])
    in_doc = norm(q["hint"]) in ctext
    ch = chunks[(chunks.doc_id == gold) & chunks.text.map(lambda t: norm(q["hint"]) in norm(t))]
    permitted = "Y" if ({q["asker"], "all_staff"} & set(groups_of[gold].split(";"))) else "N"
    rows.append(dict(q_id=f"Q{n:02d}", question=q["question"], gold_doc_id=gold, gold_chunk_hint=q["hint"], answer=q["answer"], language=q["lang"],
                     needs_current_version="Y" if q["cur"] == "Y" else "N", asker_group=q["asker"], permitted=permitted,
                     note=(q["kind"] + ("; " + q["note"] if q["note"] else "")), kind_=q["kind"], hint_ok_=in_doc, hint_in_chunk_=len(ch) > 0))
ev = pd.DataFrame(rows)
check(len(ev) == 60, f"60 evaluation questions, got {len(ev)}")
vc = ev.kind_.value_counts().to_dict()
check(vc == {"plain": 40, "stale": 8, "swahili": 6, "restricted": 6}, f"question kinds {vc}")
check(bool(ev.hint_ok_.all()), "gold_chunk_hint missing from gold document: " + str(ev[~ev.hint_ok_].q_id.tolist()))
check(bool(ev.hint_in_chunk_.all()), "gold_chunk_hint split across chunks: " + str(ev[~ev.hint_in_chunk_].q_id.tolist()))
check(int((ev.permitted == "N").sum()) == 6 and bool((ev[ev.kind_ == "restricted"].permitted == "N").all()), "exactly the six restricted questions are not permitted")

res = {m: [] for m in ("bm25", "meaning", "hybrid")}
rank_of = {m: [] for m in res}
top_status = []
para_flag, ov_list = [], []
for r in ev.itertuples():
    gold = r.gold_doc_id
    for m in res:
        top = S.search(r.question, m, k=10)
        docs10 = list(top.doc_id)
        rk = next((i for i, dd in enumerate(docs10, 1) if dd == gold), 0)
        rank_of[m].append(rk)
        res[m].append(int(0 < rk <= 5))
        if m == "bm25":
            top_status.append(top.status.iloc[0] if len(top) else "")
    ch = chunks[(chunks.doc_id == gold) & chunks.text.map(lambda t: norm(r.gold_chunk_hint) in norm(t))].iloc[0]
    ov = len(set(KS.tokenise(r.question)) & set(KS.tokenise(ch.text)))
    ov_list.append(ov)
ev["bm25_rank"], ev["meaning_rank"], ev["hybrid_rank"] = rank_of["bm25"], rank_of["meaning"], rank_of["hybrid"]
ev["bm25_hit5"], ev["meaning_hit5"], ev["hybrid_hit5"] = res["bm25"], res["meaning"], res["hybrid"]
ev["words_shared_with_gold_passage"] = ov_list
ev["paraphrase"] = ev.words_shared_with_gold_passage <= 1
ev["note"] = [r.kind_ + ("; paraphrase" if r.paraphrase else "") + (("; " + q["note"]) if q["note"] and q["note"] != "paraphrase" else "")
              for r, q in zip(ev.itertuples(), Q)]
rec = {m: float(np.mean(res[m])) for m in res}
mrr = {m: float(np.mean([1 / r if r else 0 for r in rank_of[m]])) for m in res}
best = max(rec["bm25"], rec["meaning"])
log(f"recall@5 bm25 {rec['bm25']:.3f} meaning {rec['meaning']:.3f} hybrid {rec['hybrid']:.3f}")
check(0.55 <= rec["bm25"] <= 0.75, f"BM25 recall@5 {rec['bm25']:.3f} outside 0.55 to 0.75")
check(0.40 <= rec["meaning"] <= 0.65, f"meaning recall@5 {rec['meaning']:.3f} outside 0.40 to 0.65")
check(rec["hybrid"] >= best + 0.08 - 1e-9, f"hybrid recall@5 {rec['hybrid']:.3f} is not 0.08 above the better single method {best:.3f}")
st = ev[ev.kind_ == "stale"]
stale_top1 = int(sum(1 for i in st.index if top_status[i] == "superseded"))
check(stale_top1 >= 4, f"BM25 rank-1 chunk is a superseded version for {stale_top1} of 8 stale questions; need 4")
# permission test
rest = ev[ev.kind_ == "restricted"]
unf, fil = [], []
for r in rest.itertuples():
    ug = ";".join(users.loc[users.groups.str.contains(r.asker_group), "groups"].iloc[0:1]) if r.asker_group != "all_staff" else "all_staff"
    unf.append({m: r.gold_doc_id in set(S.search(r.question, m, k=5).doc_id) for m in ("bm25", "hybrid")})
    fil.append({m: r.gold_doc_id in set(S.search(r.question, m, k=10, user_groups=r.asker_group).doc_id) for m in ("bm25", "meaning", "hybrid")})
unf_bm = sum(u["bm25"] for u in unf)
unf_hy = sum(u["hybrid"] for u in unf)
check(unf_bm >= 4 and unf_hy >= 4, f"without permission filtering the restricted gold is in the top 5 for bm25 {unf_bm}, hybrid {unf_hy} of 6; need 4")
check(not any(any(f.values()) for f in fil), "with permission filtering the restricted gold document must never appear (top 10 checked)")
# paraphrase rates
pf = ev[ev.paraphrase]
check(len(pf) >= 15, f"paraphrase questions (sharing at most one word with the gold passage) {len(pf)}; need 15")
sw = ev[ev.kind_ == "swahili"]
perm_ev = ev[ev.permitted == "Y"]
rec_perm_filtered = {}
for m in res:
    hits = 0
    for r in perm_ev.itertuples():
        hits += int(r.gold_doc_id in set(S.search(r.question, m, k=5, user_groups=r.asker_group).doc_id))
    rec_perm_filtered[m] = round(hits / len(perm_ev), 3)
# near-duplicate side effect: which questions each method misses
miss = {m: list(ev.q_id[ev[m + "_hit5"] == False]) for m in res}
kinds = {}
for k in ["plain", "stale", "swahili", "restricted"]:
    sub = ev[ev.kind_ == k]
    kinds[k] = {m: round(float(sub[m + "_hit5"].mean()), 3) for m in res}
KEY["search_evaluation"] = dict(
    method=dict(chunks="about 200 words, 40 word overlap", chunk_count=int(len(chunks)), documents=int(len(corpus)), text_source="pypdf for text PDFs, python-docx for .docx, plain read for .txt, Tesseract OCR for scans",
                bm25="k1 1.5, b 0.75, lowercase tokens, short stopword list, chunks with no matching word are not returned",
                meaning="stand-in: TF-IDF on word unigrams and character 4-grams, SVD to 64 dimensions, cosine similarity", hybrid="reciprocal rank fusion, k 60, top 50 of each list",
                hit_rule="a question is a hit at k when any of the top k chunks comes from the gold document (doc_id)"),
    questions=60, recall_at_5=dict((m, round(rec[m], 3)) for m in rec), hits_at_5=dict((m, int(sum(res[m]))) for m in res),
    mrr_at_10=dict((m, round(mrr[m], 3)) for m in mrr),
    recall_at_3=dict((m, round(float(np.mean([0 < r <= 3 for r in rank_of[m]])), 3)) for m in rank_of),
    hybrid_minus_better_single_method=round(rec["hybrid"] - best, 3),
    recall_at_5_by_question_kind=kinds,
    recall_at_5_permitted_questions_with_permission_filter=rec_perm_filtered,
    stale_questions=dict(count=8, bm25_rank1_chunk_is_superseded=stale_top1,
                         per_question=[dict(q_id=r.q_id, question=r.question, bm25_top1_status=top_status[r.Index], bm25_rank_of_current=r.bm25_rank, hybrid_rank_of_current=r.hybrid_rank) for r in st.itertuples()]),
    permission_test=dict(questions=6, without_filter_gold_in_top5=dict(bm25=int(unf_bm), hybrid=int(unf_hy)), with_filter_gold_in_top10=0,
                         per_question=[dict(q_id=r.q_id, asker_group=r.asker_group, gold_doc_id=r.gold_doc_id, found_without_filter_bm25=unf[i]["bm25"], found_without_filter_hybrid=unf[i]["hybrid"]) for i, r in enumerate(rest.itertuples())]),
    paraphrase=dict(definition="question shares at most one word (after lowercasing and removing stopwords) with the passage that holds the answer", count=int(len(pf)),
                    bm25_recall_at_5=round(float(pf.bm25_hit5.mean()), 3), meaning_recall_at_5=round(float(pf.meaning_hit5.mean()), 3), hybrid_recall_at_5=round(float(pf.hybrid_hit5.mean()), 3),
                    question_ids=list(pf.q_id)),
    swahili=dict(count=6, bm25_hits=int(sw.bm25_hit5.sum()), meaning_hits=int(sw.meaning_hit5.sum()), hybrid_hits=int(sw.hybrid_hit5.sum()),
                 note=f"Three questions are about Swahili circulars and every method finds them. Three are Swahili questions about English documents: keyword search finds {int(sw[sw.language=='sw'].iloc[3:].bm25_hit5.sum())} of them and the stand-in meaning search finds {int(sw.iloc[3:].meaning_hit5.sum())}."),
    questions_missed=miss,
    per_question=[dict(q_id=r.q_id, kind=r.kind_, gold_doc_id=r.gold_doc_id, bm25_rank=r.bm25_rank, meaning_rank=r.meaning_rank, hybrid_rank=r.hybrid_rank,
                       words_shared_with_gold_passage=r.words_shared_with_gold_passage) for r in ev.itertuples()],
    note="Rank 0 means the gold document is not in the top 10 chunks.")
out_ev = ev[["q_id", "question", "gold_doc_id", "gold_chunk_hint", "answer", "language", "needs_current_version", "asker_group", "permitted", "note"]]
out_ev.to_csv(DATA / "eval_questions.csv", index=False)
log("eval_questions.csv")

# ---- document-level facts for the key
sup = meta[meta.status == "superseded"]
body_by_id = {d["doc_id"]: d["body"] for d in DOCS}
no_notice = [r.doc_id for r in sup.itertuples() if not re.search(r"supersed|replaced by|replaces|no longer in force", body_by_id[r.doc_id], re.I)]
check(len([x for x in no_notice if x in (tag2id["hb2019"], tag2id["hb2022"])]) == 2, "two handbook versions are superseded in metadata only")
KEY["documents"] = dict(
    total=int(len(meta)), by_format=meta.format.value_counts().to_dict(), by_family=meta.family.value_counts().to_dict(), by_status=meta.status.value_counts().to_dict(),
    by_sensitivity=meta.sensitivity.value_counts().to_dict(), by_language=meta.language.value_counts().to_dict(), confidential_documents=list(meta.doc_id[meta.sensitivity == "confidential"]),
    containing_personal_data=int((meta.contains_personal_data == "Y").sum()), total_pages=int(meta.pages.sum()),
    superseded_documents=list(sup.doc_id), superseded_with_no_notice_in_text=no_notice,
    handbook_versions={k: tag2id[k] for k in ("hb2019", "hb2022", "hb2025")}, claims_sop_versions={k: tag2id[k] for k in ("sop3", "sop4")},
    two_column_pdfs=[d["file"] for d in DOCS if d.get("cols") == 2], table_pdfs=[d["file"] for d in DOCS if d.get("table")],
    pdfs_with_header_footer_and_page_numbers=int(sum(1 for d in DOCS if d["format"] == "text_pdf" and d["hf"])),
    text_pdfs_all_return_text_with_pypdf=True, scanned_pdfs_return_near_empty_text_with_pypdf=True,
    claims_letters=30, swahili_documents=[d["doc_id"] for d in DOCS if d["language"] == "sw"],
    stale_pairs=dict(annual_leave_days={"2019": 21, "2022": 24, "2025": 28}, probation_months={"2019": 6, "2022": 4, "2025": 3}, remote_days_per_week={"2019": 0, "2022": 2, "2025": 3},
                     expense_limit_ugx={"2019": 200000, "2022": 350000, "2025": 500000}, settlement_days={"SOP v3": 45, "SOP v4": 30},
                     claims_officer_limit_ugx={"SOP v3": 5000000, "SOP v4": 8000000}, mileage_ugx_per_km={"2023/017": 1900, "2025/006": 2200},
                     saturday_hours={"2022/004": "9:00 am to 12:00 noon", "2025/002": "9:00 am to 1:00 pm"}),
    letter_facts=kitara_docs_c.LETTER_FACTS)
KEY["evaluation_questions"] = dict(total=60, plain=40, stale=8, swahili=6, restricted=6, permitted_N=int((ev.permitted == "N").sum()), needs_current_version_Y=int((ev.needs_current_version == "Y").sum()))
log("document facts")

# ============================================================================ 11. templates
tools = [("Google Colab", "Run notebooks in the browser"), ("Python with pandas, pypdf, pdfplumber, matplotlib", "Profile data, extract text, score searches"), ("Tesseract OCR", "Read scanned pages"),
         ("sentence-transformers", "Embeddings for meaning search"), ("Chroma", "Store and search vectors"), ("PostgreSQL with pgvector", "Store and search vectors"),
         ("DuckDB and Parquet", "Fast analytical SQL on files"), ("Pandera", "Quality rules a machine checks"), ("Great Expectations Core", "Quality rules a machine checks"),
         ("DataHub", "Data catalogue and lineage"), ("OpenMetadata", "Data catalogue and lineage"), ("Dagster or Apache Airflow", "Schedule pipeline steps"), ("Microsoft Presidio", "Find and mask personal data"), ("Ragas", "Optional retrieval metrics")]
TP.readiness_scorecard(TEMPL / "Readiness Scorecard.xlsx")
TP.readiness_scorecard(TEMPL / "Readiness Scorecard (Kitara example).xlsx", filled=rd, title="Readiness Scorecard (Kitara example)")
TP.use_case_canvas(TEMPL / "Use Case Canvas.xlsx")
TP.data_inventory(TEMPL / "Data Inventory.xlsx")
TP.data_contract(TEMPL / "Data Contract Template.xlsx")
TP.search_test_sheet(TEMPL / "Search Test Sheet.xlsx")
TP.risk_register(TEMPL / "Risk Register.xlsx")
TP.hosting_cost_model(TEMPL / "Hosting Cost Model.xlsx")
TP.licence_register(TEMPL / "Licence Register.xlsx", tools)
TP.roadmap_planner(TEMPL / "Roadmap Planner.xlsx")
TP.board_paper_outline(TEMPL / "Board Paper Outline.docx")
log("templates written")


def normalize_zips(paths):
    """Rewrite .xlsx and .docx files with fixed entry dates so that a re-run gives identical bytes."""
    for p in paths:
        tmp = Path(str(p) + ".tmp")
        with zipfile.ZipFile(p) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
            for info in sorted(zin.infolist(), key=lambda i: i.filename):
                zi = zipfile.ZipInfo(info.filename, date_time=(2026, 10, 29, 9, 0, 0))
                zi.compress_type = zipfile.ZIP_DEFLATED
                zi.external_attr = 0o644 << 16
                data = zin.read(info.filename)
                if info.filename == "docProps/core.xml":
                    data = re.sub(rb"(<dcterms:(?:created|modified)[^>]*>)[^<]*", rb"\g<1>2026-10-29T09:00:00Z", data)
                zout.writestr(zi, data)
        tmp.replace(p)


normalize_zips(sorted(list(TEMPL.glob("*.xlsx")) + list(TEMPL.glob("*.docx")) + list((DATA / "branch_reports").glob("*.xlsx")) + list(DOCDIR.rglob("*.docx"))))


def verify_templates():
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice or SKIP_LO:
        return dict(status="skipped", reason="LibreOffice not found or --skip-lo")
    files = sorted(TEMPL.glob("*.xlsx")) + sorted((DATA / "branch_reports").glob("*.xlsx"))
    out = Path(tempfile.mkdtemp(prefix="kitara_lo_"))
    prof = Path(tempfile.mkdtemp(prefix="kitara_lo_profile_"))
    cmd = [soffice, f"-env:UserInstallation=file://{prof}", "--headless", "--convert-to", "xlsx", "--outdir", str(out)] + [str(f) for f in files]
    subprocess.run(cmd, check=True, capture_output=True, timeout=400)
    errs, nform = [], 0
    for f in files:
        r = out / f.name
        if not r.exists():
            errs.append(f"{f.name}: no output")
            continue
        wf = load_workbook(f)
        for ws in wf:
            for row in ws.iter_rows():
                for c in row:
                    if isinstance(c.value, str) and c.value.startswith("="):
                        nform += 1
        wv = load_workbook(r, data_only=True)
        for ws in wv:
            for row in ws.iter_rows():
                for c in row:
                    if isinstance(c.value, str) and (c.value.startswith("#") or c.value.startswith("Err:")):
                        errs.append(f"{f.name}!{ws.title}!{c.coordinate}: {c.value}")
    # the Kitara example must recalculate to the numbers in the key
    wv = load_workbook(out / "Readiness Scorecard (Kitara example).xlsx", data_only=True)["Scorecard"]
    vals = {}
    for row in wv.iter_rows(min_row=1, max_row=60):
        if row[0].value in KT.DIMS and row[2].value is not None and isinstance(row[2].value, (int, float)):
            vals[row[0].value] = (round(row[2].value, 2), round(row[3].value, 2) if isinstance(row[3].value, (int, float)) else None)
    for d in KT.DIMS:
        exp = (rx[d]["baseline_mean"], rx[d]["mean_without_self_reported"])
        if vals.get(d) != exp:
            errs.append(f"Kitara example scorecard {d}: LibreOffice {vals.get(d)} expected {exp}")
    # a docx round trip as well
    subprocess.run([soffice, f"-env:UserInstallation=file://{prof}", "--headless", "--convert-to", "pdf", "--outdir", str(out), str(TEMPL / "Board Paper Outline.docx")], check=True, capture_output=True, timeout=200)
    ok_docx = (out / "Board Paper Outline.pdf").exists()
    shutil.rmtree(out, ignore_errors=True)
    shutil.rmtree(prof, ignore_errors=True)
    return dict(status="verified with LibreOffice", workbooks=len(files), formulas=nform, errors=errs, board_paper_opens=ok_docx,
                kitara_example_recalculated=vals)


lo = verify_templates()
check(not lo.get("errors"), f"LibreOffice found problems: {lo.get('errors')}")
KEY["templates"] = dict(files=sorted(p.name for p in TEMPL.iterdir()), libreoffice_check=lo)
log(f"LibreOffice check: {lo.get('status')} {('(%d formulas, %d errors)' % (lo.get('formulas', 0), len(lo.get('errors', [])))) if lo.get('formulas') is not None else ''}")

# ============================================================================ 12. answer key, dictionary, zip
KEY["generator"] = dict(script="05 Course Maintenance/Authoring/Build/build_teaching_data.py", seeds=dict(customers=20261101, mobile_money=20261102, branch_reports=20261103, letters=7731),
                        search_module="05 Course Maintenance/Authoring/Build/kitara_search.py", failed_assertions=FAILS)
DICT = """DATA DICTIONARY: Kitara Group teaching data
Enterprise Data Readiness for AI. Everything here is fictional: Kitara Group, its staff, customers, phone numbers, identity numbers and regulators do not exist.
Phone numbers sit in a block (+256 700 0xx xxx, +254 700 0xx xxx) that we treat as reserved for this course. Identity numbers are 'KX' followed by 12 digits, a format that is not used by any real card.
The files are generated by build_teaching_data.py with fixed seeds. The numbers in this folder do not change between runs.

THE CASE
Kitara Group is a bank and insurer headquartered in Kampala with a subsidiary in Nairobi. About 1,800 staff, 38 branches in Uganda, 9 in Kenya.
Units: Kitara Bank (retail and SME), Kitara Assurance (general and life insurance), Kitara Kenya. Departments: Retail Banking, SME Lending, Claims, Underwriting,
Customer Service, Finance, HR, Legal and Compliance, IT, Risk, Branch Operations. Currency is UGX; Kenya figures are in KES.

----------------------------------------------------------------------------------------------------
sources.csv   14 rows. The inventory of Kitara's data sources.   Sessions 1, 3 (and 8 for owners of alerts)
  source_id, name, system_type, format, approx_records
  refresh              daily, weekly, monthly, ad hoc or unknown
  owner                role that answers for the data. Blank when nobody is named. 'IT' on two rows where a business unit also claims the source
  steward              role that looks after quality day to day. Blank on seven rows
  sensitivity          public, internal, restricted or confidential. Blank on five rows. Two rows are wrong against the Data Classification Standard (S03 and S10)
  personal_data        Y, N or blank (not yet decided)
  in_catalogue         N on every row. There is no catalogue yet
  last_quality_check   date or blank
  ai_use_case_candidates, notes
  Use: find the gaps, then complete the Data Inventory workbook.

readiness_evidence.csv   25 rows. The Kitara evidence pack for the baseline scorecard.   Session 2
  evidence_id, dimension (five dimensions), item, level_name (Ad hoc, Developing, Defined, Managed, Optimised), what_exists,
  who_could_verify, proposed_score (1 to 5), self_reported (Y when the score rests on what someone said and nobody outside the team has seen the evidence)
  Use: score Kitara in the Readiness Scorecard, then compare with the discounted version that leaves out self-reported rows.

customers.csv   5,000 rows. A table of core-banking customers with deliberate defects.   Sessions 3, 4, 9
  customer_id (KT- and seven digits), full_name, gender, date_of_birth, phone, email, national_id_present (Y or N), national_id (KX and 12 digits; blank when missing),
  district, branch_code, product, opened_date, status, segment
  Defects: duplicates, four phone formats, missing national_id and date_of_birth, impossible dates, district spelled three ways for Kampala and Wakiso, lower-case branch codes,
  test accounts, gender coded eight ways (F, Female, f, 2 and M, Male, m, 1). Exact counts are in answer_key.json.
  Use: profile the table and run six quality rules in Session 4. Mask personal data in Session 9.

mobile_money_log.csv   20,000 rows. A month of agent and mobile money transactions.   Sessions 4, 8
  txn_id, timestamp (two formats), msisdn_hash (hashed pseudo identifier), agent_id, amount_ugx, type, status
  Defects: re-sent transactions with the same txn_id, negative and zero amounts, a six hour gap with no records on one day, and a second timestamp format for one agent group.
  Use: uniqueness, validity and timeliness rules; freshness monitoring in the pipeline lab.

docs/   121 documents, in subfolders by family: policies/, product guides/, circulars/, minutes/, claims letters/, regulatory/, scans/.   Sessions 1, 5, 6, 7, 9
  Text PDFs (some with headers, footers and page numbers, some in two columns, two with a table), 10 Word files, 6 text files, and 8 scanned PDFs that contain only images.
  Three editions of the Staff Handbook (2019, 2022, 2025), two versions of the Claims Handling SOP, pairs of circulars where a newer one replaces an older one,
  three Swahili circulars from Kitara Kenya, 30 claims and complaint letters with fictional personal data, six regulatory notices (labelled fictional).
  Use: Session 1 (conflicting versions), Session 5 (extract, OCR, chunk), Sessions 6 and 7 (search, test, permissions), Session 9 (personal data in the letters).

docs_metadata.csv   one row per document.   Sessions 5, 7
  doc_id (D001 and up), file (path under docs/), title, family, version, status (current or superseded), effective_date, owner_department,
  sensitivity, access_groups (semicolon list from: all_staff, claims, underwriting, hr, finance, legal_compliance, risk, branch_ops, executive),
  language (en or sw), format (text_pdf, scanned_pdf, docx, txt), pages, contains_personal_data (Y or N)
  Status is superseded only in this file for some documents. The text of the document does not say so. A search that ignores status can return an old answer.

users.csv   12 test users.   Session 7
  user_id, name, department, groups (semicolon list), role. Includes a claims officer, an HR officer, a branch manager, a general staff member, an internal auditor in legal_compliance and an executive.
  Use: permission tests. A user sees a document when it is open to all_staff or shares a group with the user.

eval_questions.csv   60 questions.   Sessions 6, 7
  q_id, question, gold_doc_id, gold_chunk_hint (a phrase that appears in the right passage), answer, language (en or sw),
  needs_current_version (Y when a superseded version holds a different answer), asker_group, permitted (Y or N: would that asker be allowed to see the gold document), note
  The note starts with the kind: plain (40), stale (8), swahili (6) or restricted (6). Many plain questions are paraphrases that use none of the words in the answer passage.

lineage_edges.csv   25 edges.   Sessions 3, 8
  from_asset, to_asset, step. The claims reporting chain from the claims system to the board pack, and the customer table to the customer dashboard.

branch_reports/   6 Excel files.   Sessions 3, 5
  Branch reports that differ in layout: merged title cells, headers on different rows, months across or down, numbers stored as text, hidden columns, N/A in number cells.
  Use: the shared drive discussion. How many different layouts can one analyst read?

answer_key.json   Tutors only. Every number a slide may quote: defect counts, readiness baseline, scan error rates, recall values and per-question search ranks.
  This file is not included in data.zip.

Related code (in 05 Course Maintenance/Authoring/Build/): kitara_search.py chunks text and runs keyword (BM25), stand-in meaning (TF-IDF with SVD) and hybrid (reciprocal rank fusion) search.
  Learners may copy it into a notebook. The meaning search here is a stand-in for an embedding model.

WORKPIECE TEMPLATES (03 Learner Materials/Workpiece Templates/)
  Readiness Scorecard.xlsx (Session 2), Readiness Scorecard (Kitara example).xlsx (Session 2), Use Case Canvas.xlsx (Session 1), Data Inventory.xlsx (Session 3),
  Data Contract Template.xlsx (Session 4), Search Test Sheet.xlsx (Session 7), Hosting Cost Model.xlsx (Session 10), Licence Register.xlsx (Session 10),
  Risk Register.xlsx (Session 11), Roadmap Planner.xlsx and Board Paper Outline.docx (Session 12).
  Cells with a light cream tint are for your input. The Hosting Cost Model contains no prices.
"""
(DATA / "DATA DICTIONARY.txt").write_text(DICT, encoding="utf-8")
(DATA / "answer_key.json").write_text(json.dumps(KEY, indent=2, default=lambda o: o.item() if hasattr(o, "item") else str(o)), encoding="utf-8")
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
log(f"data.zip written ({ZIP.stat().st_size / 1e6:.1f} MB)")
print()
print(f"documents {n_docs}; recall@5 bm25 {rec['bm25']:.3f}, meaning {rec['meaning']:.3f}, hybrid {rec['hybrid']:.3f}; stale rank-1 superseded {stale_top1}/8; permission test unfiltered {unf_bm}/6 bm25 {unf_hy}/6 hybrid; paraphrase questions {len(pf)}")
print(f"scan CER normal max {max(cer_normal)}, heavy min {min(cer_heavy)}")
if FAILS:
    print(f"\n{len(FAILS)} assertion(s) failed:")
    for f in FAILS:
        print(" -", f)
    if not NO_ASSERT:
        sys.exit(1)
print(f"done in {time.time() - T0:.0f}s")
