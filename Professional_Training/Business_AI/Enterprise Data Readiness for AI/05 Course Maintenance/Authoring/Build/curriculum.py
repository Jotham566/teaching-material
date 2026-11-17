"""Single source of truth for Enterprise Data Readiness for AI.

12 sessions x 2 hours = 24 hours. Participants: a decision maker plus a data or IT colleague from the same organisation, East African enterprises.
Teaching pattern: leaders take the decision questions, the team repeats the technical steps in a notebook. Every tool is free and open to use at work.
Every other file (decks, notebooks, workbook, plan) reads this module. The roadmap and report read curriculum.json (same sessions, shorter wording).
"""

COURSE = dict(
    title="Enterprise Data Readiness for AI",
    sessions=12, hours_per_session=2, total_hours=24,
    start="A leader and a data or IT colleague from one organisation. No coding needed for leaders. Teams should be comfortable with spreadsheets and databases.",
    end="A scored baseline, a tested search over the organisation's own documents, and a twelve-month plan presented as a board paper.",
)

SESSION_SHAPE = [("Case and recall", 10), ("Teaching", 30), ("Live demonstration", 25), ("Break", 5), ("Workshop on your organisation", 40), ("Decision and wrap-up", 10)]

DIMENSIONS = ["Use cases and sponsorship", "Data: inventory, quality and metadata", "Platform and pipelines", "Protection and law", "People and governance"]
LEVELS = ["Ad hoc", "Developing", "Defined", "Managed", "Optimised"]
WORKPIECES = {2: "Baseline scorecard", 7: "Search pilot report", 12: "Roadmap and board presentation"}

MODULES = [
    ("A", "Start with a baseline", range(1, 3), "Use cases, data needs and a scored baseline."),
    ("B", "Know your data", range(3, 5), "Inventory, ownership, quality and contracts."),
    ("C", "Make it searchable", range(5, 8), "Parse documents, search by meaning, test and secure the search."),
    ("D", "Platform, law and cost", range(8, 11), "Pipelines, privacy law, hosting, cost and licences."),
    ("E", "Govern and plan", range(11, 13), "Roles, policy, risk and the twelve-month plan."),
]

# 'code' = a team notebook exists (leaders watch the demonstration and use the workshop sheet).
# 'min_code' = the least number of code slides in the deck.
SESSIONS = {
 1: dict(no=1, module="A", code=True, min_code=2, title="What AI-ready data means",
   question="Which AI uses do we want, and what data does each one need?",
   result="Three use cases, each with the data it needs, where that data lives and who owns it.",
   outcomes=["Name an AI use and the data it depends on", "Explain how stale, missing or unreachable data produces a wrong answer", "Say where structured and unstructured data live in your organisation"],
   topics=["what AI does with data: predict, search, generate", "analytics-ready data compared with AI-ready data", "four ways data fails an AI use: missing, stale, unowned, unreachable", "structured, semi-structured and unstructured data", "what published surveys and forecasts say about stalled AI projects, and what each one measures", "Kitara Group introduced", "the use case canvas"],
   lab="Workshop: write three AI use cases on the canvas and list the data each needs. Team notebook: find three conflicting versions of one policy in the Kitara document set."),
 2: dict(no=2, module="A", code=True, min_code=2, title="Score your readiness",
   question="Where do we stand today?",
   result="A baseline scorecard: five dimensions scored one to five, each with one piece of evidence. Workpiece 1.",
   outcomes=["Score an organisation on five dimensions and five levels", "Back each score with evidence that someone outside the team could check", "Find the weakest dimension and say what it blocks"],
   topics=["why a scale needs evidence rules", "five dimensions and five levels", "where the scales come from: Cisco, DCAM, CMMI DMM and Databricks, and how they differ", "scoring one dimension step by step", "self-assessment bias and how to reduce it", "weakest dimension against average", "the scorecard spreadsheet", "setting a target level"],
   lab="Workshop (workpiece 1): score Kitara from its evidence pack, then score your own organisation. Team notebook: compute the scorecard in pandas and chart it."),
 3: dict(no=3, module="B", code=True, min_code=3, title="Find, own and catalogue your data",
   question="Who owns each source, and who may see it?",
   result="An inventory of ten sources, each with an owner, a steward and a sensitivity class.",
   outcomes=["List data sources with the fields an inventory needs", "Tell an owner from a steward and a custodian", "Classify sources by sensitivity and spot personal data"],
   topics=["inventory fields", "owner, steward and custodian", "sensitivity classes: public, internal, restricted, confidential", "personal data and where it hides", "business, technical and operational metadata", "catalogue compared with a spreadsheet", "lineage in one picture", "DataHub and OpenMetadata overview", "shadow data and shared drives"],
   lab="Workshop: complete the Kitara source list, then list ten of your own sources. Team notebook: scan a folder tree and find sources with no owner or no class."),
 4: dict(no=4, module="B", code=True, min_code=3, title="Quality, metadata and data contracts",
   question="How do we know a dataset is fit for AI use?",
   result="Six quality rules and one data contract for a dataset of your choice.",
   outcomes=["Measure completeness, validity and uniqueness on a real table", "Write a quality rule that a machine can check", "Write a data contract with an owner and a change rule"],
   topics=["quality dimensions: completeness, validity, uniqueness, consistency, timeliness, accuracy", "profiling a table", "rules and thresholds", "Pandera and Great Expectations Core", "the cost of a defect downstream", "data contract fields: schema, quality, freshness, owner, change policy", "Open Data Contract Standard", "metadata that makes data findable and reusable"],
   lab="Workshop: write six rules and a contract for one dataset. Team notebook: profile the Kitara customer table and run your rules."),
 5: dict(no=5, module="C", code=True, min_code=4, title="From documents to clean text",
   question="Which of our documents can AI read, and what must be repaired first?",
   result="A readiness table for 50 to 100 documents: format, text quality, version status, sensitivity and chunk plan.",
   outcomes=["Tell a text PDF from a scan and extract text from each", "Split a document into chunks that keep their meaning", "Attach metadata that lets a search filter by version and access"],
   topics=["document types in an enterprise", "text PDF, scan and office file", "extraction with pypdf and pdfplumber", "OCR with Tesseract and what it gets wrong", "tables, columns, headers and footers", "versions and duplicates", "chunk size and overlap", "structure-aware chunking", "metadata to attach to every chunk", "counting your own unstructured data"],
   lab="Workshop: sample 50 of your own documents and fill the readiness table. Team notebook: extract, OCR and chunk the Kitara documents."),
 6: dict(no=6, module="C", code=True, min_code=4, title="Search by meaning",
   question="What does search by meaning add to the keyword search we already have?",
   result="A working search over the Kitara documents that combines keyword and meaning search.",
   outcomes=["Explain keyword search, embeddings and vector search in plain words", "Run a keyword search and a meaning search on the same question and compare", "Combine two ranked lists with reciprocal rank fusion"],
   topics=["keyword search and BM25", "what an embedding is", "vector distance and nearest neighbours", "vector stores: pgvector, Chroma, Qdrant, FAISS, OpenSearch", "hybrid search and reciprocal rank fusion", "re-ranking in one slide", "multilingual text and Swahili queries", "choosing an embedding model and checking its licence", "when keyword search is enough"],
   lab="Workshop: write ten questions your staff ask and note where the answer lives. Team notebook: build keyword, meaning and hybrid search over the Kitara documents."),
 7: dict(no=7, module="C", code=True, min_code=4, title="Test the search and control who sees what",
   question="Can we trust the results, and does the search respect permissions?",
   result="A search pilot report with at least 30 test questions, recall at k, a failure list and a permissions test. Workpiece 2.",
   outcomes=["Build a test set with the right passage marked for every question", "Score a search with recall at k and mean reciprocal rank", "Apply permission filters and prove a restricted document stays hidden"],
   topics=["test set design", "recall at k", "mean reciprocal rank", "error analysis: stale versions, wrong chunks, missing documents", "permission-aware retrieval", "filtering before and after the search", "personal data inside chunks", "logging queries and results", "reporting a pilot honestly with its limits"],
   lab="Workshop (workpiece 2): test your own search on 30 questions and write the pilot report. Team notebook: score three searches and run the permissions test."),
 8: dict(no=8, module="D", code=True, min_code=3, title="Pipelines and platform design",
   question="How does data travel from source to search, and who is told when it breaks?",
   result="A reference architecture drawing with a check at every step and an owner for every alert.",
   outcomes=["Describe the path from source to search as ordered steps with checks", "Explain batch, incremental loads and why a step must be safe to re-run", "Say what to monitor: freshness, volume and schema change"],
   topics=["ETL and ELT", "zones: raw, cleaned, serving", "Parquet and DuckDB", "orchestration with Airflow or Dagster: dependencies, retries, alerts", "idempotent and incremental loads", "lineage and OpenLineage", "monitoring freshness, volume and schema drift", "a failure drill", "reference architecture layers"],
   lab="Workshop: draw your pipeline from source to search and mark each check and owner. Team notebook: run a three-step pipeline with checks and break it on purpose."),
 9: dict(no=9, module="D", code=True, min_code=3, title="Privacy and East African law",
   question="What does the law require when AI reads personal data?",
   result="A data protection map for your organisation: where personal data sits, which law applies, what moves abroad.",
   outcomes=["Name the principles and rights in the Uganda Data Protection and Privacy Act, 2019", "Compare transfer and registration rules in Uganda, Kenya, Rwanda and Tanzania", "Find and mask personal data before it enters a search index"],
   topics=["personal data and special categories", "the Uganda Act: principles, rights, the regulator and registration", "breach notification", "cross-border transfers", "Kenya, Rwanda and Tanzania compared", "data minimisation for AI", "deleting data from an index when someone asks", "automated decisions", "finding and masking personal data with patterns and Presidio", "the EU AI Act and Article 10 for firms with European customers", "a teaching summary and no legal advice"],
   lab="Workshop: map where your personal data sits, which law applies and what leaves the country. Team notebook: find and mask personal data in the Kitara claims letters."),
 10: dict(no=10, module="D", code=True, min_code=3, title="Hosting, cost and licences",
   question="Where should this run, and what will it cost?",
   result="A costed hosting option and a licence register for the tools you would use.",
   outcomes=["Compare hosting options on residency, latency, capacity and cost", "List the cost lines of a search system beyond the licence", "Read a licence file and classify a tool as open, source-available or restricted"],
   topics=["on-site, local data centre, regional cloud and software as a service", "what exists in East Africa and what is still planned", "connectivity and latency", "cost lines: people, hardware, hosting, licences, evaluation, support", "build compared with buy", "open-weight models and their licences", "reading a licence: permissive, copyleft, source-available, archived", "vendor lock-in and an exit plan", "the tool licence register"],
   lab="Workshop: price one hosting option from your own quotes and complete the licence register. Team notebook: compute total cost for three options and check licences from a list."),
 11: dict(no=11, module="E", code=True, min_code=2, title="Governance and AI risk",
   question="Who decides, who answers for it, and what happens when it goes wrong?",
   result="Roles, a short policy set and a scored risk register for your first AI use.",
   outcomes=["Set up owners, stewards and a decision forum for data and AI", "Walk an incident through the four NIST AI RMF functions", "Score risks by likelihood and impact and assign an owner to each"],
   topics=["governance operating model", "policies: data classification, acceptable AI use, retention", "NIST AI Risk Management Framework: govern, map, measure, manage", "ISO/IEC 42001 in one slide", "risk register", "shadow AI", "vendor questions for AI suppliers", "human oversight", "incident drill: personal data found in an index", "review cycle"],
   lab="Workshop: draft your roles, three policies and ten risks. Team notebook: score and rank the Kitara risk register."),
 12: dict(no=12, module="E", code=True, min_code=2, title="Your twelve-month roadmap",
   question="What do we do first, and what do we ask the board for?",
   result="A sequenced twelve-month roadmap, a budget line, a rescoring target and a board presentation. Workpiece 3.",
   outcomes=["Sequence work by dependency, value and effort", "Turn the baseline gaps into a costed plan with measures", "Present the plan to a board in ten minutes"],
   topics=["quick wins and foundations", "dependencies", "thirty, ninety and three hundred and sixty five days", "the business case and how to measure it", "rescoring as the measure of progress", "the board paper", "risks to the plan", "what to do next and which credentials exist"],
   lab="Workshop (workpiece 3): build your roadmap and present it in ten minutes. Team notebook: chart a roadmap and compute the projected rescored baseline."),
}

TOOLS = [
 dict(name="Google Colab", use="Run notebooks in the browser. Nothing to install.", cost="Free tier with a free Google account. Limits are not published.", status="verified"),
 dict(name="Spreadsheet (Google Sheets, Excel or LibreOffice)", use="The scorecard, inventory, risk register and roadmap templates.", cost="Free. Any spreadsheet works.", status="verified"),
 dict(name="Python with pandas, pypdf, pdfplumber, matplotlib", use="Profile data, extract text, score searches.", cost="Free, open source.", status="verified"),
 dict(name="Tesseract OCR", use="Read scanned pages.", cost="Free, Apache-2.0.", status="verified"),
 dict(name="sentence-transformers", use="Embeddings for meaning search.", cost="Library Apache-2.0. Read the model card licence for each model.", status="check"),
 dict(name="Chroma and PostgreSQL with pgvector", use="Store and search vectors.", cost="Free. Apache-2.0 and PostgreSQL licence.", status="check"),
 dict(name="DuckDB and Parquet", use="Fast analytical SQL on files.", cost="Free. MIT and Apache-2.0.", status="check"),
 dict(name="Pandera and Great Expectations Core", use="Quality rules a machine checks.", cost="Free. MIT and Apache-2.0.", status="check"),
 dict(name="DataHub and OpenMetadata", use="Data catalogue and lineage, shown by the tutor.", cost="Free. DataHub Apache-2.0. Read the OpenMetadata licence files.", status="check"),
 dict(name="Dagster or Apache Airflow", use="Schedule pipeline steps, shown by the tutor.", cost="Free. Apache-2.0.", status="check"),
 dict(name="Microsoft Presidio", use="Find and mask personal data.", cost="Free. MIT. Confirm the current repository.", status="check"),
 dict(name="Ragas", use="Optional retrieval metrics.", cost="Free. Apache-2.0.", status="check"),
]
AVOIDED = [
 ("Docker Desktop", "Free for individuals, education and businesses under 250 staff and USD 10 million revenue. Larger firms and government bodies need a paid subscription. Use Python packages, Colab or Podman."),
 ("MinIO", "Reported unmaintained or archived in 2026. Teach any S3-compatible object store."),
 ("Soda Core 4 and Airbyte", "Source-available under the Elastic License 2.0. Free to run internally and not open source."),
 ("dbt v2", "The free binary carries some proprietary code. Check which artefact is installed."),
 ("Amundsen", "Repository reported archived in September 2026."),
 ("Metabase for embedding", "The open edition is AGPLv3, and embedding needs a paid licence."),
 ("Paid AI APIs and hosted inference", "Any lab needing a key would break the no-cost rule, and documents would leave the organisation."),
]
