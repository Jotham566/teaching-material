const fs = require('fs'), path = require('path');
const D = require('docx');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle, HeadingLevel, AlignmentType, LevelFormat, PageBreak, Footer, PageNumber } = D;
const ROOT = path.resolve(__dirname, '..', '..', '..');
const INK = '1F2328', BODYC = '3B4046', SOFT = '6A6F75', LAKE = 'B04A2B', LINE = 'C9C5BC';   // one ink, one accent (used for links only), hairlines; no fills
const W = 9638;          // A4 with 1.5 cm side margins: 11906 - 2*1134

const run = (t, o = {}) => new TextRun({ text: t, font: 'Calibri', size: 22, color: BODYC, ...o });
const P = (t, o = {}) => new Paragraph({ spacing: { after: 120, line: 276 }, ...o, children: Array.isArray(t) ? t : [run(t)] });
const H1 = t => new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 360, after: 160 }, children: [new TextRun({ text: t, font: 'Cambria', bold: true, size: 36, color: INK })] });
const H2 = t => new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 240, after: 100 }, children: [new TextRun({ text: t, font: 'Cambria', bold: true, size: 28, color: INK })] });
const H3 = t => new Paragraph({ heading: HeadingLevel.HEADING_3, spacing: { before: 160, after: 60 }, children: [new TextRun({ text: t, font: 'Calibri', bold: true, size: 24, color: INK })] });
const B = (t, lvl = 0) => new Paragraph({ numbering: { reference: 'bul', level: lvl }, spacing: { after: 60, line: 264 }, children: Array.isArray(t) ? t : [run(t)] });
const N = t => new Paragraph({ numbering: { reference: 'num', level: 0 }, spacing: { after: 60, line: 264 }, children: Array.isArray(t) ? t : [run(t)] });
const bold = t => run(t, { bold: true });
const none = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
const hair = { style: BorderStyle.SINGLE, size: 4, color: LINE };
const heavy = { style: BorderStyle.SINGLE, size: 12, color: INK };
function cell(t, w, o = {}) {
  const paras = (Array.isArray(t) ? t : [t]).map(x => new Paragraph({ spacing: { after: 40, line: 252 }, children: typeof x === 'string' ? [run(x, { size: o.size || 20, bold: o.bold, color: o.bold ? INK : BODYC })] : x }));
  return new TableCell({ width: { size: w, type: WidthType.DXA }, borders: { top: none, left: none, right: none, bottom: o.head ? heavy : hair }, margins: { top: 80, bottom: 80, left: o.first ? 0 : 120, right: 100 }, children: paras });
}
function table(header, rows, widths, o = {}) {
  const tot = widths.reduce((a, b) => a + b, 0);
  return new Table({ width: { size: tot, type: WidthType.DXA }, columnWidths: widths, rows: [
    new TableRow({ tableHeader: true, children: header.map((h, i) => cell(h, widths[i], { head: true, bold: true, first: i === 0, size: o.size || 20 })) }),
    ...rows.map((r, ri) => new TableRow({ cantSplit: true, children: r.map((c, i) => cell(c, widths[i], { first: i === 0, size: o.size || 20, bold: (i === 0 && o.boldFirst) || (o.hl && o.hl(ri, r)) })) }))] });
}
function callout(t) {
  return new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: [W], rows: [new TableRow({ children: [new TableCell({ width: { size: W, type: WidthType.DXA }, borders: { top: heavy, bottom: hair, left: none, right: none }, margins: { top: 140, bottom: 120, left: 0, right: 0 }, children: (Array.isArray(t) ? t : [t]).map(x => new Paragraph({ spacing: { after: 70, line: 264 }, children: typeof x === 'string' ? [run(x)] : x })) })] })] });
}
const gap = () => new Paragraph({ spacing: { after: 100 }, children: [] });
function doc(title, children, footerText) {
  return new Document({
    creator: 'Jotham Martin Wambi', title,
    styles: { default: { document: { run: { font: 'Calibri', size: 22 } } } },
    numbering: { config: [
      { reference: 'bul', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 270 } } } }, { level: 1, format: LevelFormat.BULLET, text: '–', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 1000, hanging: 270 } } } }] },
      { reference: 'num', levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 340 } } } }] }] },
    sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1134, bottom: 1134, left: 1134, right: 1134 } } },
      footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [run(`${footerText}   Page `, { size: 18, color: SOFT }), new TextRun({ children: [PageNumber.CURRENT], font: 'Calibri', size: 18, color: SOFT })] })] }) },
      children }] });
}
const save = async (d, rel) => { const p = path.join(ROOT, rel); fs.mkdirSync(path.dirname(p), { recursive: true }); fs.writeFileSync(p, await Packer.toBuffer(d)); console.log('wrote', rel); };

// ============================================================ 1. BENCHMARK AND DESIGN REPORT
const CUR = JSON.parse(fs.readFileSync(path.join(__dirname, 'curriculum.json'), 'utf8'));
const DD = JSON.parse(fs.readFileSync(path.join(__dirname, 'docs_data.json'), 'utf8'));
const TT = DD.totals;
const lead = (a, b) => B([bold(a + ' '), run(b)]);

async function report() {
  const c = [];
  c.push(new Paragraph({ spacing: { before: 400, after: 80 }, children: [new TextRun({ text: 'Enterprise Data Readiness for AI', font: 'Cambria', bold: true, size: 52, color: INK })] }));
  c.push(new Paragraph({ spacing: { after: 240 }, children: [new TextRun({ text: 'Benchmark and design report', font: 'Calibri', size: 32, color: SOFT })] }));
  c.push(P('Prepared 29 October 2026 for Jotham Martin Wambi, KLAi Professional Learning. The research, benchmark and design are followed by the built course: ' + TT.slides + ' slides in 12 decks, 12 team notebooks with solutions, the Kitara Group case data, the workpiece templates and the handouts.'));

  c.push(H1('1. Summary'));
  c.push(callout([[bold('A 24-hour programme for a leader and a data or IT colleague from the same organisation. It ends with a scored baseline, a tested search over their own documents and a twelve-month plan.')],
    'Most published material falls into two groups. Vendor guides (Microsoft, AWS, Google, Databricks, Snowflake) describe adoption on one platform. Executive courses (MIT, Oxford, Stanford, Google, Microsoft, AWS, DeepLearning.AI) teach strategy or product awareness and cost USD 99 to 3,850. Data management frameworks (DAMA, DCAM, CMMI DMM) are vendor-neutral but built before generative AI or only recently extended. None of the offers found tests a participant\'s own documents, uses East African law, or ends with a readiness plan, and no East African offer of that kind turned up in search. That is a negative search result and does not prove none exists.']));
  c.push(gap());
  c.push(P('The course is built on five readiness dimensions that recur across the frameworks compared, a five-level scale, three workpieces, and a stack of free, open tools whose licences are read in class. It follows the Applied AI and Automation course, which treats preparing information and retrieval at the scale of one legal firm. This course takes the same ideas to systems, pipelines, four national laws and hosting cost.'));

  c.push(H1('2. What the evidence says about data and AI projects'));
  c.push(P('Four figures are quoted everywhere. Each measures something different and none was read from the primary document in this research, so the course teaches what each one measures and treats the headline number as an estimate.'));
  c.push(table(['Figure', 'Source', 'What it measures', 'Caution'], [
    ['60% of AI projects without AI-ready data abandoned through 2026', 'Gartner press release, 26 February 2025', 'A prediction. The same release reports a Q3 2024 survey of 248 data management leaders, 63% of whom lack or are unsure they have the right data practices for AI.', 'Forecast, repeated widely with no new evidence behind it.'],
    ['30% of generative AI projects abandoned after proof of concept by end of 2025', 'Gartner, 29 July 2024', 'A forecast. Causes named: poor data quality, inadequate risk controls, escalating cost, unclear business value.', 'No source found that checks whether it happened.'],
    ['42% of companies abandoned most AI initiatives before production; 46% of proofs of concept scrapped', 'S&P Global Market Intelligence, 451 Research, 1,006 respondents in North America and Europe, fielded Oct to Nov 2024', 'A survey of companies. Top obstacles: cost, data privacy and security risk.', 'Secondary sources often misreport it as 42% abandoning AI altogether.'],
    ['95% of organisations see no return on generative AI', 'MIT NANDA, The GenAI Divide, July 2025', 'Preliminary research: 153 survey responses from conference attendees, 52 interviews, 300 public initiatives.', 'Critics say it conflates "no P&L impact" with failure. Teach it as preliminary research.'],
    ['80 to 90% of enterprise data is unstructured', 'Attributed to Gartner and IDC in many pages', 'An estimate. IDC models all data generated worldwide, not data held by organisations.', 'No primary source found. Nobody counts files, so participants count their own document stores in Session 5.'],
  ], [2300, 2000, 3100, 2238], { size: 18, boldFirst: true }));
  c.push(P(''));
  c.push(P('Survey evidence on the state of practice is more useful for teaching. Cisco\'s 2025 AI Readiness Index (8,000 leaders in companies of over 500 staff) found 19% with fully centralised data infrastructure and four tiers from Laggard to Pacesetter, where Pacesetters are about four times as likely to move pilots into production. Accenture\'s 2024 research found 61% of companies saying their data assets are not ready for generative AI. Snowflake and Enterprise Strategy Group (April 2025, 1,900 leaders) found 58% calling AI-ready data a challenge. Deloitte\'s 2026 enterprise survey found 21% with proper governance for AI agents. These are vendor and consultancy surveys with their own samples, and Cisco and Deloitte results are self-rated.'));

  c.push(H1('3. How the frameworks measure readiness'));
  c.push(table(['Framework', 'Dimensions', 'Scale', 'Use in this course'], [
    ['Cisco AI Readiness Index', 'Strategy, infrastructure, data, governance, talent, culture', 'Score 0 to 100 into four tiers', 'Model for a scored profile and peer comparison.'],
    ['AWS Cloud Adoption Framework for AI', 'Business, people, governance, platform, security, operations', 'Four stages: envision, align, launch, scale (third-party summary)', 'Check that the five dimensions cover all six perspectives.'],
    ['Microsoft Cloud Adoption Framework for AI', 'Plan, ready, govern, secure, manage', 'No scored model', 'Sequence of work in Session 12.'],
    ['Google AI Adoption Framework (older white paper)', 'People, process, technology, data', 'Three levels: tactical, strategic, transformational', 'Context only. Current status of the paper is unconfirmed.'],
    ['EDM Council DCAM v3', 'Eight components, 34 capabilities', 'Six levels, not initiated to enhanced', 'Source for the capability checklist in Sessions 3 and 4. Training costs USD 1,370 and is for members.'],
    ['CMMI Data Management Maturity (ISACA)', 'Six categories, 25 process areas', 'Five levels, performed to optimised', 'Source for the five-level scale.'],
    ['DAMA-DMBOK2', 'Eleven knowledge areas with governance at the centre', 'A body of knowledge with no maturity scale', 'Shared vocabulary for the inventory and glossary.'],
    ['Databricks AI Governance Maturity Model', 'Data, process, people', 'Five levels, ad hoc to optimised', 'Names of the levels in the scale below.'],
    ['Snowflake AI-Ready Data Framework (open repository)', 'Clean, contextual, consumable, current (four of six factors confirmed)', 'Scored per data asset', 'Asset-level test in Session 5.'],
    ['FAIR principles (Wilkinson et al., 2016)', 'Findable, accessible, interoperable, reusable', 'Principles without a scale', 'Metadata checklist in Session 4. Origin is research data.'],
  ], [2300, 2700, 2300, 2338], { size: 18, boldFirst: true }));
  c.push(P(''));
  c.push(P('Three levels, five levels and six levels all appear, and the sources give no standard. The course uses five because CMMI DMM and the Databricks model both use five. The five dimensions are use cases and sponsorship, data (inventory, quality and metadata), platform and pipelines, protection and law, and people and governance. Each of the recurring Cisco, AWS, Google, Microsoft and DCAM dimensions maps onto one of them, and search over documents is scored inside the data and platform dimensions.'));
  c.push(callout([[bold('Scale used in the course. ')], 'Level 1 ad hoc, level 2 developing, level 3 defined, level 4 managed, level 5 optimised. Every score needs one piece of evidence that someone outside the team could check, such as a policy document, a catalogue entry or a test result.']));

  c.push(H1('4. Standards and law'));
  c.push(H2('Standards'));
  c.push(P('NIST AI Risk Management Framework 1.0 (January 2023, voluntary) has four functions: govern, map, measure and manage. Its Generative AI Profile (NIST AI 600-1, July 2024) adds generative AI risks without new functions. ISO/IEC 42001:2023 is the first AI management system standard and uses the same clause structure as ISO/IEC 27001, so firms already certified in security can extend it. The ISO/IEC 5259 series covers data quality for analytics and machine learning (Parts 1 and 2 published in 2024, later parts reported through 2025 and 2026). ISO 8000 covers data quality management and master data exchange. The course reads these in class and does not ask participants to buy them.'));
  c.push(H2('European exposure'));
  c.push(P('Article 10 of the EU AI Act sets data and data governance duties for high-risk systems: documented practices for data collection, labelling and cleaning, checks for bias, and data sets that are relevant, representative and as complete and error-free as possible. As reported in October 2026, the Digital Omnibus on AI (reported as Regulation (EU) 2026/1744, in force 27 July 2026) moves the Annex III high-risk obligations, which include Article 10, to 2 December 2027, and Annex I product systems to 2 August 2028. These dates come from secondary sources and a search snippet of the EUR-Lex page. Read the Official Journal text before teaching them.'));
  c.push(H2('East African law'));
  c.push(table(['Country', 'Law', 'Rule on moving data abroad', 'Notes'], [
    ['Uganda', 'Data Protection and Privacy Act 2019; Regulations 2021', 'Section 19 allows processing or storage outside Uganda if the destination offers at least equivalent protection or the data subject consents. No blanket localisation rule.', 'Regulator is the Personal Data Protection Office under NITA-U. In July 2025 it found Google in breach for not registering and rejected the argument that section 19 covers only Ugandan controllers (CIPESA, DLA Piper). Breaches are reported to it immediately.'],
    ['Kenya', 'Data Protection Act 2019; General Regulations 2021', 'Targeted localisation for some categories, set in section 50 and Regulation 26. Exact categories unconfirmed.', 'The Office of the Data Protection Commissioner issued cross-border guidance in 2026 (full text not read).'],
    ['Rwanda', 'Law 058/2021', 'Transfers abroad need authorisation from the National Cyber Security Authority or another listed ground. Offshore storage needs a registration certificate.', 'The authority can suspend transfers.'],
    ['Tanzania', 'Personal Data Protection Act 2022', 'Adequacy or safeguards plus a permit from the Commission.', 'Registration is mandatory. Reports of closure of the registration window in April 2026 are unconfirmed. Bank of Tanzania cloud guidelines add approval and in-country rules for mission-critical systems.'],
  ], [1100, 2200, 3300, 3038], { size: 18, boldFirst: true }));
  c.push(P(''));
  c.push(P('Uganda launched its National Data Strategy 2026/27 to 2030/31 on 20 October 2026, with UNDP and UN Global Pulse, reported at about UGX 1.663 trillion. The Uganda Bureau of Statistics has publicly said the strategy overlaps its statutory mandate. The Ministry of ICT held consultations on a national AI and emerging technologies strategy in March 2026, and no published national AI strategy was found. No AI-specific rule from the Bank of Uganda, the Insurance Regulatory Authority or the Uganda Communications Commission was found. Bank of Uganda\'s Cyber and Technology Risk Management Guidelines took effect on 1 December 2024, and whether they address cloud or AI is unconfirmed. Kenya published a National AI Strategy 2025 to 2030 in March 2025, and the Central Bank of Kenya was reported in November 2025 to be finalising an AI guidance note.'));
  c.push(callout([[bold('Every law row above comes from secondary sources. ')], 'The Act, regulations and regulator guidance must be read in the original before Session 9 is taught, and the session should be framed as a teaching summary with no legal advice, as in the other courses.']));

  c.push(H1('5. Technical practice for searchable, AI-ready data'));
  c.push(P('Practice has converged on a short chain: find and own the data, check its quality, parse documents to clean text, split them into chunks with metadata, embed the chunks, store them in a search index, combine keyword and meaning search, attach each user\'s permissions to every result, and test the whole chain against questions with known answers. Vector search itself has become a commodity. The hard parts are parsing, metadata, permission-aware retrieval and an evaluation set, and these are what the course spends its time on.'));
  c.push(lead('Chunking.', 'Azure AI Search documentation suggests starting near 512 tokens with 25% overlap, and Weaviate suggests 512 tokens with 50 to 100 tokens of overlap. Both say to test on your own questions.'));
  c.push(lead('Hybrid search.', 'Reciprocal rank fusion (Cormack, Clarke and Buttcher, SIGIR 2009) adds 1 divided by (60 plus rank) across the keyword list and the meaning list. The BEIR benchmark (NeurIPS 2021) found BM25 a strong baseline, so keyword search stays in the design.'));
  c.push(lead('Permissions.', 'The common pattern attaches access labels such as group and sensitivity to each chunk when it is indexed, turns the user\'s identity into a filter inside the search, and re-syncs when source permissions change. Vendor documents disagree on filtering before or after the search. Session 7 tests both on the same data.'));
  c.push(lead('Evaluation.', 'A set of real questions with the right passage marked, scored by whether the right passage appears in the top few results. Ragas, TruLens and DeepEval offer metrics. The definitions of recall at k and mean reciprocal rank were not sourced in this research and are taught from first principles.'));
  c.push(lead('Languages.', 'No evaluation of Luganda, Swahili or Kinyarwanda retrieval was found. The course tests multilingual embedding models on the participants\' own text and does not claim results in advance.'));

  c.push(H2('Tool licences'));
  c.push(P('Free tools are changing terms quickly. Several popular names moved to source-available licences or stopped being maintained during 2025 and 2026, so a licence check is a taught skill in Session 10 and a handout. Licences below come from search summaries and third-party pages, because primary pages and licence files could not be fetched. Open each repository\'s LICENSE file before relying on them.'));
  c.push(table(['Tool', 'Use in course', 'Licence as reported', 'Status'], [
    ['PostgreSQL with pgvector', 'Vector search inside a normal database', 'PostgreSQL licence, permissive', 'Use'],
    ['Chroma, Qdrant, FAISS, OpenSearch', 'Alternative vector stores and search', 'Apache-2.0 (FAISS: MIT)', 'Use'],
    ['Docling, Apache Tika', 'Parse PDFs and office files to text', 'MIT (Docling; model weights carry their own licences), Apache-2.0 (Tika)', 'Use'],
    ['sentence-transformers and open embedding models', 'Embeddings', 'Apache-2.0 library. Each model card has its own licence; bge-m3 and multilingual-e5 reported MIT', 'Check each model'],
    ['Ragas', 'Test the search', 'Apache-2.0', 'Use'],
    ['DataHub', 'Data catalogue and lineage', 'Apache-2.0', 'Use'],
    ['OpenMetadata', 'Data catalogue', 'Apache-2.0 at the root. One review reports the ingestion and UI folders under the Collate Community Licence, which bars offering it as a competing hosted service', 'Check repository'],
    ['Pandera, Great Expectations Core', 'Data quality checks', 'MIT; Apache-2.0. Great Expectations ownership and cloud product reported changing in 2026', 'Use, confirm ownership'],
    ['DuckDB, Parquet', 'Analytical SQL and file format', 'MIT; Apache-2.0', 'Use'],
    ['Dagster, Apache Airflow', 'Pipeline scheduling', 'Apache-2.0', 'Use'],
    ['Microsoft Presidio', 'Find and mask personal data', 'MIT. One source says it moved out of Microsoft; detection is model-based and never complete', 'Use, confirm repository'],
    ['Keycloak, OpenFGA', 'Identity and permissions', 'Apache-2.0', 'Use'],
    ['Apache Superset', 'Dashboards', 'Apache-2.0, no paid feature tier', 'Use'],
    ['Metabase', 'Dashboards', 'Open edition AGPLv3; embedding and some controls need a paid licence', 'Avoid for embedding'],
    ['MinIO', 'Object storage', 'AGPLv3. Reported unmaintained or archived between February and April 2026', 'Avoid. Teach "any S3-compatible store"'],
    ['Soda Core 4, Airbyte', 'Quality checks, data movement', 'Elastic License 2.0, source-available', 'Avoid as a core dependency'],
    ['dbt v2', 'SQL transformation', 'Free binary under the dbt product licence with some proprietary code. The Apache-2.0 distribution is called dbt OSS', 'Check artefact'],
    ['Amundsen', 'Data discovery', 'Repository reported archived in September 2026', 'Avoid'],
    ['Docker Desktop', 'Running services on a laptop', 'Free for individuals, education and businesses under 250 staff and USD 10 million revenue. Paid for larger firms and for government bodies (Docker pricing pages)', 'Avoid. Use Python packages, Colab, or Podman'],
    ['Llama community licence models', 'Local language model', 'Meta licence required above 700 million monthly users; the Open Source Initiative says it is not open source', 'Prefer Apache-2.0 models and read each card'],
  ], [2300, 2200, 3700, 1438], { size: 17, boldFirst: true, hl: (i, r) => /^Avoid/.test(r[3]) }));
  c.push(P(''));

  c.push(H1('6. East African infrastructure and context'));
  c.push(P('Uganda has no hyperscale cloud region. The closest are in South Africa: AWS Cape Town, Azure Johannesburg and Cape Town, and Google Johannesburg (opened January 2024). Modern GPU availability in those regions is unclear and a single June 2026 analysis found little outside Azure. The Microsoft and G42 data centre at Olkaria in Kenya, planned at about USD 1 billion, was reported stalled in May 2026 over power. The Oracle cloud region in Nairobi, with iXAfrica as host, still showed as coming soon in July 2026. Raxio\'s Kampala facility at Namanve opened in 2021 as Tier III with 1.5 MW of IT power, and a February 2026 report describes a shortage of Tier III capacity in Uganda. NITA-U runs the national data centre in Jinja that hosts the government cloud, and commissioned a market study toward a third, AI-ready centre. In Kenya, Airtel Africa\'s Nxtra is building a 44 MW GPU-ready hub due in early 2027.'));
  c.push(P('GSMA reports a 66% mobile internet usage gap in sub-Saharan Africa at the end of 2025. Mobile money is a large source of enterprise data: MTN Uganda MoMo reported 14.7 million active fintech users and UGX 195.5 trillion in transaction value for 2025 (via a news report; the results PDF was not opened). The Oxford Insights Government AI Readiness Index 2025 puts Uganda at 35.8 against a world average of 42.5 and a regional average of 29.1. The index method changed, so the score is not comparable with 2024. Kenya and Rwanda ranks conflict across sources and are not quoted.'));
  c.push(P('The consequence for teaching is direct. Demonstrations must run on a laptop or in Colab, because participants cannot rely on a local cloud region or a GPU. Hosting becomes a decision with real trade-offs: keep data on site, rent space in a local data centre, use a South African region subject to transfer rules, or run small open models locally.'));

  c.push(H1('7. Courses and certifications for leaders'));
  c.push(table(['Offer', 'Length and price', 'Covers', 'Gap against this course'], [
    ['MIT Sloan, AI: Implications for Business Strategy', '6 weeks online, 6 to 8 hours a week, USD 3,850', 'Strategy for managers and executives', 'Strategy level, not centred on data readiness'],
    ['Oxford Said, Oxford Artificial Intelligence Programme', '6 weeks online, 7 to 10 hours a week, GBP 2,450', 'General AI strategy for leaders', 'No data readiness or hands-on work'],
    ['Stanford Online AI Professional Program', '10 weeks per course; price per course reported between USD 1,595 and 2,045', 'Technical AI courses', 'Not an executive programme'],
    ['Google Cloud Generative AI Leader', 'USD 99 exam, 90 minutes', 'Conceptual, Google products', 'Single vendor, no data readiness assessment'],
    ['Microsoft AI Business School', 'Free, with INSEAD; duration unconfirmed', 'Strategy, culture, responsible AI, technology', 'Microsoft-oriented, not hands-on'],
    ['AWS Certified AI Practitioner', 'USD 100 exam', 'AWS services and AI basics', 'AWS-specific, wider than executives'],
    ['DeepLearning.AI, AI for Everyone and Generative AI for Everyone', 'About 7 hours and 5 hours, Coursera pricing', 'Awareness for non-technical staff', 'No governance or data content'],
    ['DAMA CDMP', 'About USD 311 per exam; Practitioner about USD 933 in total', 'Data management knowledge exams', 'Exam-based, practitioner audience, no AI retrieval'],
    ['EDM Council DCAM v3 training', 'Two days with exam, USD 1,370, members only', 'Maturity assessment for data governance teams', 'Price tied to membership, no AI retrieval'],
    ['Coursera, IBM Data Management Professional Certificate', '3 to 6 months, with a 9-hour governance course', 'Practitioner data management', 'Self-paced, no executive framing'],
    ['East Africa: Strathmore iLabAfrica AI Essentials; ESAMI short courses; CMU-Africa AI certificate', 'KSh 27,500 for 3 weeks (Strathmore); ESAMI fees not found; CMU-Africa free, by invitation', 'AI basics, AI for fraud, policy and technical AI', 'No leader-and-team data readiness programme found'],
  ], [2700, 2300, 2200, 2438], { size: 18, boldFirst: true }));
  c.push(P(''));
  c.push(P('Prices and dates come from search results on 29 October 2026 and several are third-party figures. Confirm each against the provider before quoting it in marketing.'));

  c.push(H1('8. Positioning'));
  c.push(P('The offer is a working programme for a mixed room. Leaders take the decision questions in each session, and their data or IT colleagues run the demonstration steps. Both work on one case and then on their own organisation. The strongest claims the research supports are that the course uses open tools only, runs on a laptop, tests search on the participant\'s own documents, teaches four East African laws and the cost of local and regional hosting, and ends with a scored plan. The course makes no claim to certify data management competence. DAMA CDMP and DCAM remain the recognised credentials, and the final session points to them for the data team members who want one.'));

  c.push(H1('9. Course design'));
  c.push(H2('Audience and seats'));
  c.push(P('Two or three people from one organisation attend together: a decision maker (CIO, CTO, chief data officer, head of operations or a business owner) and one or two colleagues from data, IT or information management. Cohorts of eight to twelve organisations suit the room. Technical steps are shown live on the tutor\'s screen, and teams repeat them on their own laptops with a notebook that contains the code. Leaders are not asked to run code. Each session ends with a decision question that only the leader can answer, for example who owns a data source.'));
  c.push(H2('Sessions'));
  c.push(table(['No.', 'Session', 'Question for the room', 'Team notebook', 'What you make'], DD.sessions.map(s => [String(s.no), s.title, s.question, s.lab.split('Team notebook: ')[1] || '', s.result.replace(/ Workpiece \d\.$/, '')]), [500, 1700, 2300, 2900, 2238], { size: 17, boldFirst: true, hl: (i, r) => /Workpiece|workpiece/.test(DD.sessions[i].result) }));
  c.push(P(''));
  c.push(H2('Session shape'));
  c.push(P('Case 10 minutes, teach 30, live demonstration 25, break 5, workshop on your own organisation 40, decide 10. The shape matches the other courses so that tutor notes and slides share one pattern. Decks follow the same design system, with read-aloud notes for every slide.'));
  c.push(H2('Case and data'));
  c.push(P('Kitara Group is a fictional bank and insurer with offices in Kampala and Nairobi. Its sources include a core banking database, a customer table with seeded defects, about 200 policy and claims PDFs (some scanned), shared-drive spreadsheets, a mobile money log and a staff handbook that exists in three versions. All data is generated, with an answer key, in the same way as the other courses. It exists: 121 documents in the document set, 14 sources in the inventory, 5,000 customers, a mobile money log of 20,000 rows and 60 test questions.'));
  c.push(H2('Workpieces'));
  c.push(P('The programme has no exams. Three workpieces carry the learning: the baseline scorecard in Session 2, the search pilot report in Session 7 with at least 30 test questions, and the roadmap and board presentation in Session 12. Participants work on their own organisation for these. Documents must not be confidential or must carry the organisation\'s written approval. The Course Plan and Tutor Guide has a checklist for each workpiece, and a tutor marks each as complete or needing revision. The Participant Workbook holds the task pages, and Workpiece Templates holds ' + DD.templates.length + ' files, the workbooks and the board paper outline that the sessions use.'));
  c.push(H2('Fit with Applied AI and Automation'));
  c.push(P('Session 5 of that course prepares one firm\'s information, Session 6 builds internal search over it and Session 11 covers governance and risk. This course takes participants who completed those or who have equivalent understanding, but it does not require them. Session 1 defines its terms in plain words as it goes, and Sessions 5 to 7 move from one folder to a pipeline, from one firm to many sources, and from a demonstration to a tested pilot.'));
  c.push(H2('Delivery tools'));
  c.push(P('The demonstrations run in Google Colab or on the tutor\'s machine using Python packages and files. The pgvector example is shown as code to read and is not run in class. Docker Desktop is avoided because a large organisation or government body would need a paid subscription. The spreadsheet scorecard is the main working document for leaders. Nothing in the programme sends participants\' documents to a hosted model. The team notebooks work on the Kitara files, and the search compares keyword search, a stand-in for embeddings and, optionally, a small open model downloaded once in Colab.'));

  c.push(H1('10. Open items'));
  c.push(P('The research used search summaries and third-party pages because primary sites were blocked. Before the course is taught, open and read these primary sources: the Gartner 60% wording, the MIT NANDA 95% wording, the Uganda Data Protection and Privacy Act sections 19 and 23 and its regulations, the Kenya cross-border guidance note, the Official Journal text of Regulation 2026/1744, the LICENSE file of every tool in section 5, the Oxford Insights ranks for Kenya and Rwanda, and the definitions of recall at k and mean reciprocal rank. The Colab and pgvector demonstrations have not been tested, and no note has been rehearsed aloud.'));
  c.push(P('Decisions answered by the owner: the course is delivered either as a cohort of organisations or in house, and both are acceptable; pairing a decision maker with a data colleague is preferred; KLAi issues no certificate for the course; and the build went ahead. The built course has ' + TT.slides + ' slides (' + TT.animated + ' animated, with ' + TT.clicks + ' click reveals), ' + TT.vocab + ' vocabulary terms and ' + TT.workshop_tasks + ' workshop tasks. The code that needs sentence-transformers, chromadb, pgvector, pandera, great_expectations, presidio, dagster, duckdb or docling has not been run, and the Verification Record lists what else remains unchecked.'));

  c.push(H1('Sources'));
  [['Gartner, Lack of AI-Ready Data Puts AI Projects at Risk (26 Feb 2025)', 'https://www.gartner.com/en/newsroom/press-releases/2025-02-26-lack-of-ai-ready-data-puts-ai-projects-at-risk'],
   ['Gartner, 30% of Generative AI Projects Will Be Abandoned After Proof of Concept (29 Jul 2024)', 'https://www.gartner.com/en/newsroom/press-releases/2024-07-29-gartner-predicts-30-percent-of-generative-ai-projects-will-be-abandoned-after-proof-of-concept-by-end-of-2025'],
   ['S&P Global Market Intelligence, generative AI shows rapid growth but yields mixed results', 'https://www.spglobal.com/market-intelligence/en/news-insights/research/2025/10/generative-ai-shows-rapid-growth-but-yields-mixed-results'],
   ['Cisco AI Readiness Index 2025', 'https://investor.cisco.com/news/news-details/2025/Cisco-AI-Research-The-Most-AI-ready-Companies-Outpace-Peers-in-the-Race-to-Value/default.aspx'],
   ['Deloitte, State of AI in the Enterprise 2026', 'https://www.deloitte.com/content/dam/assets-shared/docs/about/2025/state-of-ai-2026-global.pdf'],
   ['Accenture, Reinventing Enterprise Operations (2024)', 'https://www.accenture.com/content/dam/accenture/final/accenture-com/document-3/Reinventing_Enterprise_Operations.pdf'],
   ['Snowflake and ESG, Radical ROI of Generative AI (Apr 2025)', 'https://www.snowflake.com/en/news/press-releases/snowflake-research-reveals-that-92-percent-of-early-adopters-see-roi-from-ai-investments/'],
   ['NIST AI Risk Management Framework', 'https://www.nist.gov/itl/ai-risk-management-framework'],
   ['EU AI Act Article 10', 'https://ai-act-law.eu/article/10/'],
   ['Regulation (EU) 2026/1744, Digital Omnibus on AI', 'https://eur-lex.europa.eu/eli/reg/2026/1744/oj/eng'],
   ['Uganda data protection, DLA Piper Privacy Matters (Aug 2025)', 'https://privacymatters.dlapiper.com/2025/08/uganda-data-protection-regulator-clarifies-compliance-requirements-for-offshore-entities/'],
   ['CIPESA, Ugandan regulator finds Google in breach (Jul 2025)', 'https://cipesa.org/2025/07/ugandan-regulator-finds-google-in-breach-of-countrys-data-protection-law-orders-local-registration/'],
   ['Uganda Broadcasting Corporation, National Data Strategy launch (20 Oct 2026)', 'https://ubc.go.ug/2026/10/20/uganda-launches-ugx-1-663-trillion-national-data-strategy-to-drive-digital-economy-and-public-planning'],
   ['Rwanda Law 058/2021 (RwandaLII)', 'https://rwandalii.org/akn/rw/act/law/2021/58/eng@2021-10-15'],
   ['Kenya ODPC guidance note on cross-border data transfers (2026)', 'https://www.odpc.go.ke/wp-content/uploads/2026/04/Guidance-Note-on-Cross-border-Data-Transfers.pdf'],
   ['Raxio Uganda data centre', 'https://www.raxiogroup.com/data-centres/uganda/'],
   ['DCD, Microsoft and G42 Kenya data centre stalled', 'https://www.datacenterdynamics.com/en/news/microsoft-and-g42-data-center-in-kenya-stalled-due-to-lack-of-power-capacity/'],
   ['Oxford Insights, Government AI Readiness Index 2025', 'https://oxfordinsights.com/ai-readiness/government-ai-readiness-index-2025/'],
   ['EDM Council DCAM v3 training', 'https://edmcouncil.org/trainings/the-dcam-v3-framework-virtual-training-with-certification-amer-2/'],
   ['MIT Sloan, AI: Implications for Business Strategy', 'https://executive.mit.edu/course/artificial-intelligence/a056g00000URaa3AAD.html'],
   ['Oxford Said, Oxford Artificial Intelligence Programme', 'https://www.sbs.ox.ac.uk/programmes/online-learning/oxford-artificial-intelligence-programme'],
   ['Google Cloud Generative AI Leader', 'https://cloud.google.com/blog/topics/training-certifications/new-google-cloud-certification-in-generative-ai/'],
   ['Docker Desktop installation and licence terms', 'https://docs.docker.com/desktop/setup/install/windows-install/'],
   ['Soda Core licence update', 'https://soda.io/blog/soda-core-license-update-moving-to-elastic-license'],
   ['dbt Core v2', 'https://docs.getdbt.com/blog/dbt-core-v2-is-here'],
   ['Airbyte licences', 'https://docs.airbyte.com/platform/developer-guides/licenses/'],
   ['OpenMetadata repository', 'https://github.com/open-metadata/openmetadata'],
   ['Azure AI Search, chunk documents for vector search', 'https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-chunk-documents'],
   ['Full research notes with dates seen and unconfirmed items', '05 Course Maintenance/Research/Research Notes.txt']]
    .forEach(([a, u]) => c.push(new Paragraph({ spacing: { after: 50, line: 252 }, children: [run(a + '. ', { size: 19 }), run(u, { size: 19, color: SOFT })] })));
  await save(doc('Enterprise Data Readiness for AI: Benchmark and design report', c, 'Enterprise Data Readiness for AI. Benchmark and design report'), '04 Facilitator Materials/Benchmark and Design Report.docx');
}
report();
