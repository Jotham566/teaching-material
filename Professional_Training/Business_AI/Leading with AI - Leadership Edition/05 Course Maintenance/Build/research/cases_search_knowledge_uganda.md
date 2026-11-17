# Case research: search and knowledge assistants, models and sovereignty, and Uganda (accessed 11 Nov 2026)

## Summary
This file fills two gaps left by the industry files. Part A covers assistants that answer from an organisation's own documents (S4 SEARCH, S9 KNOWLEDGE), with measured results where they exist: Telstra, McKinsey, the UK government's Consult tool, a large field study of a support-agent assistant, Standard Bank, Absa, Webber Wentzel and Uganda's ULII and Judiciary. Part B covers model choice, local-language models and compute sovereignty (S6, S7): Sunbird's Sunflower evaluation, Lelapa AI, Masakhane, Jacaranda's UlizaLlama, Nigeria's N-ATLaS, Cassava and Nvidia's GPU "AI factory", and the stalled Microsoft and G42 data centre in Kenya. Part C covers Uganda: AirQo and KCCA, the Data Protection Office's ruling against Google, the National Data Strategy and the AI strategy process, Centenary Bank and Huawei, MTN MoMo fraud monitoring, and a Mbale pest app. There are 21 cases in all: 8 East African (6 Ugandan, 2 Kenyan), 7 from the rest of Africa and 6 global benchmarks. I left out cases the other files already cover: Morgan Stanley (BNK-12), A&O Harvey (LGL-05), the Sunflower launch (AGR-09), Jacaranda PROMPTS triage (HLT-02), Makerere malaria microscopy (HLT-04), Makerere cassava (AGR-02), URA (PUB-01), NIRA (PUB-05), Numida (BNK-03), Bank of Uganda (BNK-04), Airtel Uganda (TEL-05, TEL-06) and the national AI policies (PUB-06). Several Ugandan items have no measured results. They are labelled as such and are best used as discussion cases.

## Coverage table (case ID x themes)

| ID | Org | Region | S1 | S2 | S3 | S4 | S5 | S6 | S7 | S8 | S9 | S10 | S11 | S12 | S13 | S14 | PEOPLE |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GAP-01 | Telstra (Ask Telstra) | Global | | | x | x | x | | | | x | | | x | | x | x |
| GAP-02 | McKinsey (Lilli) | Global | | | | x | x | | x | x | x | | x | | | | x |
| GAP-03 | UK Government (Consult) | Global | | | x | x | x | | x | | | | | x | x | | x |
| GAP-04 | NBER support-agent field study | Global | | | x | | x | | | x | x | | | x | | | x |
| GAP-05 | Standard Bank | Rest of Africa | | | | x | x | | | x | x | | | x | x | | x |
| GAP-06 | Absa Group | Rest of Africa | | | | | x | x | | x | | | x | x | x | | x |
| GAP-07 | Webber Wentzel (Legora) | Rest of Africa | | | | x | x | x | x | | x | | | | | | |
| GAP-08 | ULII and Uganda Judiciary | Uganda | x | | | x | x | | | | x | x | | | x | x | x |
| GAP-09 | Sunbird AI (Sunflower evaluation) | Uganda | | | x | | x | x | x | | | | | | | x | |
| GAP-10 | Lelapa AI (InkubaLM, Vulavula) | Rest of Africa | x | | x | | x | x | x | | | | | | | | |
| GAP-11 | Masakhane | Rest of Africa | | | x | | x | x | | | | | | | | x | x |
| GAP-12 | Jacaranda Health (UlizaLlama) | Kenya | | | x | | x | x | x | | x | | | | | | x |
| GAP-13 | Nigeria FMCIDE, NCAIR, Awarri (N-ATLaS) | Rest of Africa | | | | | x | x | x | | | | | | x | x | |
| GAP-14 | Cassava Technologies and Nvidia | Rest of Africa | | | | | | | x | | | | | | x | | |
| GAP-15 | Microsoft and G42 (Kenya) | Kenya | | | | | | x | x | | | x | | | x | | |
| GAP-16 | AirQo (Makerere) and KCCA | Uganda | x | x | x | | | | x | | | | | | x | x | |
| GAP-17 | Uganda PDPO v Google LLC | Uganda | | | | | | | x | | | x | | | x | | |
| GAP-18 | Uganda MoICT&NG (data and AI strategies) | Uganda | | | | | | | x | | | | | | x | x | x |
| GAP-19 | Centenary Group and Huawei | Uganda | | x | | | | x | x | | | | x | | | | x |
| GAP-20 | MTN MoMo Uganda | Uganda | | x | x | | | | | | | | | | x | | |
| GAP-21 | Farmers Companion App (Mbale) | Uganda | x | | | | | | x | | | | | | | | |

---

# Part A: Search and knowledge assistants (S4, S9)

### GAP-01 Telstra: "Ask Telstra", a search assistant over the company's own knowledge bases
- **Organisation / country / industry / years:** Telstra, Australia, telecom (contact centres and stores), pilot late 2023, scaled 2024 to 2026
- **What the AI does:** Frontline staff type a question, and Ask Telstra searches Telstra's internal knowledge bases and writes an answer, using Azure OpenAI and Azure AI Search. A second tool, One Sentence Summary, condenses a customer's recent notes and transactions so the agent does not have to read the whole history.
- **Result:**
  - Pilot (Feb 2024 release): Ask Telstra went first to 200 frontline staff in late 2023. Over 80% of them agreed it had a positive effect on customer interactions. In the 2023 trial of One Sentence Summary, 90% of users said it saved time and made them more effective, and follow-up contact fell by 20%.
  - At scale (April 2026): AskTelstra supports more than 8,000 frontline staff and cuts average customer call time by over one minute. Telstra also reports over 18,000 Microsoft Copilot licences with more than 80% used weekly, more than 20,000 staff through its Data & AI Academy, and its data platforms reduced from about 80 to about 20.
- **Themes:** S4, S9, S5, S12, S3 (agent-survey satisfaction versus measured call time), S14 (platform consolidation), PEOPLE (frontline agents and store staff)
- **Source(s):**
  - "Telstra scales up AI adoption following promising pilots of generative AI solutions improving customer experience", Telstra media release, https://www.telstra.com.au/aboutus/media/media-releases/telstra-scales-up-ai-adoption, 7 Feb 2024
  - "How Telstra is reinventing itself with AI", Telstra Exchange (Dayle Stevens), https://www.telstra.com.au/exchange/telstra-s-ai-transformation--strategy--partnerships-and-real-wor, 20 Apr 2026
  - Both accessed 11 Nov 2026.
- **Confidence:** High for what Telstra states (two primary documents two years apart).
- **Caution:** These are company figures and no independent audit was found. The pilot measures are survey agreement, not productivity. The "over a minute" call-time figure has no published baseline.

### GAP-02 McKinsey: "Lilli", an assistant over the firm's own knowledge
- **Organisation / country / industry / years:** McKinsey & Company, global, professional services, launched 2023, figures June 2025
- **What the AI does:** Lilli searches and summarises McKinsey's internal knowledge base (past work, research and experts) for consultants. Its add-ons draft slides from a prompt and check that documents use the firm's tone of voice.
- **Result:** Over 75% of the firm's employees use it on an ongoing monthly basis (Kate Smaje, global leader of technology and AI, June 2025). No time-saved figure is published.
- **Themes:** S4, S9, S8, S5, S11 (agents that draft slides), S7 (built in-house), PEOPLE (junior consultants)
- **Source(s):** "McKinsey is using AI to create PowerPoints and take over junior employee tasks", Fortune, https://fortune.com/2025/06/02/mckinsey-ai-consulting-powerpoints-proposal-technology/, 2 Jun 2025; accessed 11 Nov 2026.
- **Confidence:** Medium (one major outlet, quoting the firm).
- **Caution:** Usage is not value. Fortune reports that the tool takes over some tasks typically done by junior staff. McKinsey's position is that headcount need not fall, because staff move to client work. Other outlets give "over 70%" and "about 17 uses a week"; I did not verify those, so do not quote them.

### GAP-03 UK Government "Consult": AI that reads public consultation responses
- **Organisation / country / industry / years:** Government Digital Service / i.AI ("Humphrey" suite), United Kingdom, public sector; first live use 2025 (Scottish Government), Independent Water Commission review published Oct 2025
- **What the AI does:** It reads thousands of free-text replies to a public consultation, groups them into themes and counts them. Civil servants then check and correct the themes.
- **Result (Independent Water Commission review):** More than 50,000 responses were categorised in about 2 hours for £240 of compute, and experts spent 22 hours checking the output. The AI agreed with one or both expert groups almost 83% of the time. The two human groups agreed with each other only 55% of the time (F1 0.79 and 0.82 for the AI, versus 0.74 between the human groups). The government projects up to 75,000 days of manual analysis saved a year across government, which it values at £20 million in staff costs.
- **Themes:** S4, S5, S3 (comparing the AI with humans who also disagree with each other), S12, S13, S7 (government built it itself), PEOPLE (policy analysts check the work rather than code every response)
- **Source(s):** "Ground-breaking use of AI saves taxpayers' money and delivers greater government efficiency", GOV.UK press release, https://www.gov.uk/government/news/ground-breaking-use-of-ai-saves-taxpayers-money-and-delivers-greater-government-efficiency, 16 Oct 2025; accessed 11 Nov 2026.
- **Confidence:** High for the reported trial figures (official primary source).
- **Caution:** The 75,000 days and £20 million are government projections, not audited savings. Experts quoted in the trade press warn that themes can miss nuance. Teaching point: the right benchmark is how often humans agree with each other (55%), not 100%.

### GAP-04 A generative AI assistant for 5,179 support agents (field study)
- **Organisation / country / industry / years:** National Bureau of Economic Research working paper by Brynjolfsson, Li and Raymond; a Fortune 500 software firm's customer-support operation (the firm is not named); NBER w31161, April 2023, revised November 2023
- **What the AI does:** While agents chat with customers, the assistant suggests replies and links to relevant internal documentation. It was rolled out to agents in stages, which let researchers compare agents with and without it.
- **Result:** Issues resolved per hour rose 14% on average. Novice and low-skilled agents improved 34%, with minimal impact on experienced, highly skilled agents.
- **Themes:** S9, S5, S8, S12, S3 (a staggered rollout gives a fair comparison), PEOPLE (the tool spreads the know-how of the best agents to new staff)
- **Source(s):** "Generative AI at Work", NBER Working Paper 31161, https://www.nber.org/papers/w31161, Apr 2023 (rev. Nov 2023); accessed 11 Nov 2026.
- **Confidence:** High (peer-reviewed research series, large sample).
- **Caution:** The firm is unnamed, so present it as research evidence, not a named company case. The gains go mostly to newer staff, which matters for how leaders design training and pay.

### GAP-05 Standard Bank: an employee service-desk bot, then generative AI at scale
- **Organisation / country / industry / years:** Standard Bank Group, South Africa (pan-African), banking, 2024 to 2026
- **What the AI does:** "Karabo", built on Microsoft Copilot Studio, answers employees' IT and technology questions; it replaced two older custom-coded bots. Since then, generative AI tools are being used across the group under a list of approved use cases.
- **Result:**
  - Microsoft (Jan 2024): Karabo "resolves 99% of all employee queries directed at her". No volumes or period are given.
  - ITWeb (Aug 2026): 72% of group employees actively use generative AI tools, and 87 use cases have been approved. The CEO said AI-enabled recommendations supported more than 10 million personalised client interactions.
- **Themes:** S9, S4, S8, S5, S12, S13 (approved use-case list), PEOPLE (staff adoption)
- **Source(s):**
  - "Standard Bank of South Africa" customer story, Microsoft, https://www.microsoft.com/en/customers/story/1721508916179227001-standard-bank-of-south-africa-banking-power-platform-south-africa, 25 Jan 2024
  - "AI tool usage reaches 72% at Standard Bank", ITWeb Africa, https://itweb.africa/article/ai-tool-usage-reaches-72-at-standard-bank/kLgB1MezYrPq59N4, 13 Aug 2026
  - Both accessed 11 Nov 2026.
- **Confidence:** Medium. The 99% figure is a vendor customer story, and the ITWeb 72% figure is not attributed to a named speaker.
- **Caution:** The 99% figure is a vendor claim with no stated measure; it may mean "answered without human handover", not "answered correctly". A September 2026 Business Day piece reportedly gives a different headcount, which I did not read, so quote the percentage only. Stanbic Bank Uganda is part of this group, but no Uganda-specific AI figures were found.

### GAP-06 Absa: Copilot for 30,000 staff, staff-built agents, and contact-centre gains
- **Organisation / country / industry / years:** Absa Group, South Africa (pan-African, including Absa Bank Uganda), banking; Copilot experiment 2024, figures H1 2026
- **What the AI does:** Staff use Microsoft Copilot in everyday Office work, and some build their own small automation agents. The contact centre runs on Amazon Connect with AI features, and a customer chatbot answers routine queries.
- **Result (H1 2026, company statement):** More than 30,000 employees use Copilot each month. 4,400 staff with Copilot Pro licences build agents, and more than 3,800 agents are in production. More than 1,400 developers use AI coding tools. In the contact centre, response times fell by up to 21%, handling time by 14% per call and holding time by 44%. The chatbot handles more than 100,000 queries a month from about 1.6 million users.
- **Themes:** S8, S11, S12, S5, S6 (multiple vendors: Microsoft, Amazon, Salesforce), S13, PEOPLE
- **Source(s):** "Absa's AI is writing its code and answering its calls", TechCentral, https://techcentral.co.za/absas-ai-is-writing-its-code-and-answering-its-calls/285065/, 19 Aug 2026; accessed 11 Nov 2026.
- **Confidence:** Medium (one credible outlet reporting the bank's own H1 statement).
- **Caution:** These are company figures. The contact-centre gains may come from the new platform as a whole, not AI alone. Search results also mention an "AI gateway" with more than 120 models and more than 40 guardrails; I could not open that page, so do not quote it. No Absa Bank Uganda figures were found.

### GAP-07 Webber Wentzel: firm-wide rollout of the Legora legal AI platform
- **Organisation / country / industry / years:** Webber Wentzel (with its Fusion subsidiary), South Africa, law; announced 26 Aug 2025
- **What the AI does:** Legora is a legal AI workspace for reviewing, researching and drafting across a firm's documents. Webber Wentzel rolled it out across the firm and made it the anchor technology of an innovation lab that builds tools for African legal markets.
- **Result:** No published result. The firm says it chose Legora after a year-long evaluation against other platforms.
- **Themes:** S6 (comparing vendors over a year), S7, S9, S4, S5
- **Source(s):** "Leading SA firm Webber Wentzel rolls out Legora as part of 'multi-faceted partnership'", Legal IT Insider, https://legaltechnology.com/leading-sa-firm-webber-wentzel-rolls-out-legora-as-part-of-multi-faceted-partnership/, 26 Aug 2025; accessed 11 Nov 2026.
- **Confidence:** Medium.
- **Caution:** An announcement, not results. Pair it with A&O Shearman and Harvey (LGL-05) and the fake-citation cases (LGL-01 to LGL-03) to discuss vendor choice in law.

### GAP-08 Uganda: ULII's AI case summaries and the Judiciary's AI transcription push
- **Organisation / country / industry / years:** Uganda Legal Information Institute (ULII) and the Judiciary of Uganda, courts and legal research, Nov 2025 to Mar 2026
- **What the AI does:** ULII, Uganda's free online library of laws and judgments, added AI summaries of long judgments, automatic links to the laws and cases a judgment cites, and alerts when relevant new decisions appear. Separately, the Judiciary bought AI transcription software to produce court records faster.
- **Result:** No published result on accuracy or time saved. Scale and context:
  - ULII hosts more than 41,000 decisions and averages 350,000 monthly users across 45 countries; some judgments run past 50 pages (The Observer, Mar 2026).
  - The Judiciary acquired 70 licences for AI transcription software after a benchmarking visit to Tanzania. The case-management system ECCMIS had reached 35 of 279 operational courts. A recent assessment rated the Judiciary at "Level 1 (Initial)" on ICT service maturity (Nov 2025).
  - Commercial Division judges and registrars were trained on the ULII AI tools in February 2026. The trainer said ULII remains the authoritative database for checking case citations.
  - The Judiciary set 1 July 2026 as the date to end paper-based processes.
- **Themes:** S4, S9, S5, S1 (speech to text), S14 (only 35 of 279 courts digitised), S13, S10 (risk of invented citations), PEOPLE (judges, registrars, research magistrates)
- **Source(s):**
  - "Judiciary goes paperless, rolls out AI systems", The Observer (Uganda), https://observer.ug/news/judiciary-goes-paperless-rolls-out-ai-systems/, 26 Mar 2026
  - "Judiciary ICT and Documentation Committee Begins Two-Day Retreat to Shape Digital Transformation Agenda", Judiciary of Uganda, https://www.judiciary.go.ug/data/news/1772/2845/Judiciary%20ICT%20and%20Documentation%20Committee%20Begins%20Two-Day%20Retreat%20to%20Shape%20Digital%20Transformation%20Agenda.html, 18 Nov 2025
  - "Commercial Court Judicial Officers Tipped on AI-Powered Legal Research Tools", Judiciary of Uganda, https://www.judiciary.go.ug/data/news/1817/3747/Commercial%20Court%20Judicial%20Officers%20Tipped%20on%20AI-Powered%20Legal%20Research%20Tools.html, 19 Feb 2026
  - All accessed 11 Nov 2026.
- **Confidence:** High for the facts (the Judiciary's own posts plus an independent newspaper).
- **Caution:** Whether the 1 July 2026 paperless deadline was met is unconfirmed. There is no accuracy figure for the summaries or the transcription. A good discussion: grounding AI in an authoritative local source (ULII) is the defence against invented citations, compared with the failures in LGL-01 to LGL-03.

---

# Part B: Models, local languages, compute and sovereignty (S6, S7)

### GAP-09 Sunbird AI "Sunflower": how a Ugandan model was built and how it scores against GPT-4o and Gemini
- **Organisation / country / industry / years:** Sunbird AI, Uganda, language technology (cross-sector), paper 8 Oct 2025
- **What the AI does:** Sunflower 14B and 32B are language models for Ugandan languages. Sunbird built them by further training an open model from China's Alibaba (Qwen 3) rather than training from scratch. The training data came from existing corpora, OCR of printed books, dictionaries and proverbs, and more than 500 hours of radio talk-show audio transcribed with Simba FM.
- **Result:** Sunbird reports "state of the art" comprehension in most Ugandan languages; the paper claims the best accuracy in 24 of 31 languages evaluated. Mean chrF translation scores (higher is better):
  - Into English: Sunflower-32B 0.435, Gemini 2.5 Pro 0.408, GPT-4o 0.354.
  - From English into local languages: Sunflower-14B 0.366, Gemini 2.5 Pro 0.301, GPT-4o 0.235.
- **Themes:** S6 (adapt an open model, or use a global one?), S7 (sovereignty when the base model is foreign), S3 (benchmarks set by the builder), S5, S14 (digitising books and radio)
- **Source(s):** "Sunflower: A New Approach To Expanding Coverage of African Languages in Large Language Models", Sunbird AI, arXiv:2510.07203, https://arxiv.org/html/2510.07203v1, 8 Oct 2025; accessed 11 Nov 2026. (Launch with the Ministry of ICT: see AGR-09.)
- **Confidence:** High that the paper says this (primary). The scores are the builder's own evaluation.
- **Caution:** The scores were self-reported and not independently replicated. The paper is inconsistent on whether the 14B or the 32B model wins the 24 of 31 languages. A "home-grown" model built on a Chinese open model is a good sovereignty debate. No user or impact figures are published.

### GAP-10 Lelapa AI: a small model for African languages (InkubaLM) and a paid language API (Vulavula)
- **Organisation / country / industry / years:** Lelapa AI, South Africa, language technology, founded 2022; InkubaLM paper Aug 2024; Vulavula reported Oct 2024
- **What the AI does:** InkubaLM is a deliberately small, open model for Swahili, Hausa, isiZulu, isiXhosa and Yoruba, built to run cheaply. Vulavula is a paid service that businesses plug into their apps for transcription, translation and text analysis in African languages.
- **Result:** InkubaLM has 0.4 billion parameters and was pre-trained on 2.4 billion tokens. The authors say it achieves "performance comparable to models with significantly larger parameter counts" and outperforms many larger models in sentiment analysis. The same paper shows it trailing larger models such as LLaMA 3-8B on several tasks, especially African-to-English translation. Vulavula has no published usage or accuracy figures; start-ups built on it were shown at a demo day.
- **Themes:** S6 (small and cheap versus large), S7, S3 (read past the headline claim), S5, S1 (speech)
- **Source(s):**
  - "InkubaLM: A small language model for low-resource African languages", Lelapa AI et al., arXiv:2408.17024, https://arxiv.org/html/2408.17024v2, Aug 2024
  - "SA AI start-up in push to meet diverse linguistic needs", ITWeb, https://itweb.co.za/article/sa-ai-start-up-in-push-to-meet-diverse-linguistic-needs/xA9PO7NED8Wvo4J8, 21 Oct 2024
  - Both accessed 11 Nov 2026.
- **Confidence:** High.
- **Caution:** "Comparable" is the authors' summary, and the detailed tables are mixed. Training compute was donated by Microsoft's AI for Good Lab (per search results; not opened).

### GAP-11 Masakhane: a volunteer research community builds African-language translation
- **Organisation / country / industry / years:** Masakhane (grassroots research community), pan-African, 2019 to 2020 paper
- **What the AI does:** Volunteers, many without formal research training, built translation datasets and models for their own languages and published them openly. The method is "participatory research": the speakers of a language take part in building the AI for it.
- **Result:** More than 400 participants from at least 20 countries. 46 published translation benchmarks (English into 39 African languages, French into two more, and three languages into English), with human evaluation for about a third.
- **Themes:** S6, S14 (data is the bottleneck), S5, S3, PEOPLE (building local skills is part of the method)
- **Source(s):** "Participatory Research for Low-resourced Machine Translation: A Case Study in African Languages", Masakhane (Nekoto et al.), arXiv 2010.02353, https://huggingface.co/papers/2010.02353, late 2020 (acknowledges EMNLP reviewers); accessed 11 Nov 2026.
- **Confidence:** High (primary research paper; venue not confirmed from the page read).
- **Caution:** These are research benchmarks, not business deployments. The value for leaders is the model of building data and talent together. Many later African language projects drew on this community, including people now at Lelapa AI and Sunbird; that link is not documented here, so say it loosely.

### GAP-12 Jacaranda Health "UlizaLlama": an open Swahili health model built on Llama 3
- **Organisation / country / industry / years:** Jacaranda Health, Kenya, maternal health; built 2024, reported 2024 to 2025
- **What the AI does:** UlizaLlama is an open-source language model for health questions in Kiswahili. Jacaranda built it on Meta's Llama 3 and trained it on messages from its PROMPTS SMS service, so it can write tailored replies to pregnant women and new mothers instead of pre-written ones.
- **Result:**
  - Scale (IDRC, May 2025): 650,000 mothers were registered in 2024, and 4,000 to 15,000 messages arrive each day.
  - Accuracy: Jacaranda estimates the service still makes errors in 30% of cases. If a mother is not satisfied, a human takes over. Messages showing danger signs (about 7%) trigger an automatic call from one of 13 staff.
  - Target (June 2024): Jacaranda's director of technology said the goal was about 85% accuracy to start, and replies in under a minute instead of a few minutes.
- **Themes:** S6 (fine-tune an open model on your own data), S7, S9, S5, S3 (an honest 30% error estimate, with human escalation), PEOPLE (the 13 nurses and staff who handle escalations)
- **Source(s):**
  - "Technology in support of maternity", IDRC, https://idrc-crdi.ca/en/stories/technology-support-maternity, 20 May 2025
  - "From Swahili to Zulu, African techies develop AI language tools", Context (Thomson Reuters Foundation), https://www.context.news/ai/african-techies-develop-ai-language-tools-from-swahili-to-zulu, 17 Jun 2024
  - Both accessed 11 Nov 2026.
- **Confidence:** High (two independent sources).
- **Caution:** The 30% error figure is Jacaranda's own estimate, with no published method; ask "error compared with what?" HLT-02 covers the earlier PROMPTS triage model; this case is about building the language model. A NeurIPS 2025 demo reportedly mentions "UlizaMama" serving over 12,000 queries a day; I did not open it, so do not quote it.

### GAP-13 Nigeria N-ATLaS: a government-backed open multilingual model
- **Organisation / country / industry / years:** Federal Ministry of Communications, Innovation and Digital Economy (FMCIDE), with the National Centre for AI and Robotics (NCAIR), NITDA and Awarri Technologies, Nigeria, national AI infrastructure; unveiled at UNGA80, Sept 2025
- **What the AI does:** An open-source model meant to understand and generate Nigerian languages and Nigerian-accented English, offered as a free "digital public good" for builders in education, health, commerce and government.
- **Result:** No published usage result. Awarri built it; more than 7,000 fellows from the 3MTT Nigeria programme support the project (Nairametrics). NCAIR's director called it strategic infrastructure for Nigeria's AI future.
- **Themes:** S6, S7 (sovereign model as public infrastructure), S13 (national strategy), S14 (data collection), S5
- **Source(s):**
  - "Nigeria Launches Landmark AI Model Powered by Awarri to Advance Languages and AI at Scale", FMCIDE, https://fmcide.gov.ng/?p=3786, 21 Sep 2025
  - "Nigeria's N-ATLaS shows Africa is shaping global AI, says Minister Tijani", Nairametrics, https://nairametrics.com/2025/09/25/nigerias-n-atlas-shows-africa-is-shaping-global-ai-says-minister-tijani/, 25 Sep 2025
  - Both accessed 11 Nov 2026.
- **Confidence:** Medium-High for the facts of the launch (government plus press); there are no results.
- **Caution:** The pages I read do not name the languages, base model or licence. Search results say Yoruba, Hausa, Igbo and Nigerian English, built on Llama; check the Hugging Face model card (NCAIR1/N-ATLaS) before quoting. Commentators describe it as a foundation, not a finished product.

### GAP-14 Cassava Technologies and Nvidia: Africa's first "AI factory" (rented GPUs on the continent)
- **Organisation / country / industry / years:** Cassava Technologies (Zimbabwean-founded, pan-African) with Nvidia, South Africa first; announced March 2025, first phase June 2025
- **What it is:** A GPU computing centre in Africa that universities, start-ups, banks and government can rent for training and running AI, instead of sending the work to data centres abroad.
- **Result:**
  - Plan: up to US$720 million; 3,000 Nvidia GPUs in South Africa first, then about 12,000 across Egypt, Nigeria, Kenya and Morocco over three to four years. Spare capacity can be sold to Nvidia cloud customers worldwide (TechCentral, Apr 2025).
  - Status (Nov 2025): the first 3,000 GPUs were delivered to a Cassava-built facility in South Africa, launched June 2025. An MoU with the South African AI Association gives more than 3,000 AI professionals access to GPU clusters (Intelligent CIO, which puts the deal at US$700 million).
- **Themes:** S7 (rent local compute or use foreign cloud), S13 (data location)
- **Source(s):**
  - "Cassava's African 'AI factory' to cost up to $720-million", TechCentral, https://techcentral.co.za/cassava-african-ai-factory-720-million/261991/, 8 Apr 2025
  - "Nvidia and Cassava Technologies launch $700m AI data centre rollout across Africa", Intelligent CIO Africa, https://www.intelligentcio.com/africa/2025/11/27/nvidia-and-cassava-technologies-launch-700m-ai-data-centre-rollout-across-africa/, 27 Nov 2025
  - Both accessed 11 Nov 2026.
- **Confidence:** High for the plan and the first phase (two outlets); medium for the current status.
- **Caution:** The sources differ on the investment figure (US$700 million versus US$720 million). No utilisation or customer figures are published. Kenya and Nigeria are planned, not live. No Uganda site is announced.

### GAP-15 Microsoft and G42 in Kenya: a US$1 billion geothermal AI data centre that stalled over power
- **Organisation / country / industry / years:** Microsoft and G42 (UAE), with the Government of Kenya, data centres and cloud; announced 22 May 2024, stalled or suspended 2025 to 2026
- **What it was:** A data centre at Olkaria, run on geothermal power, to host a new Microsoft Azure "East Africa Cloud Region". The package also promised a Swahili and English open model, skills for all government employees, and an innovation lab in Nairobi.
- **Result:**
  - Plan (Microsoft, May 2024): an initial US$1 billion package, operational "within 24 months" of definitive agreements.
  - What happened: President Ruto said one data centre would need 1,000 MW when Kenya had 2,300 MW, which would mean switching off "half the country"; Kenya was load-shedding daily from 5 pm to 10 pm (Citizen Digital, May 2026). ThinkGeoEnergy (8 May 2026) reports Kenya suspended the project after Treasury declined to fund a concept note, and that officials knew by August 2025 the May 2026 date would be missed. Kenya's technology envoy said the remarks stressed the need for more power and did not signal cancellation.
- **Themes:** S7 (local data centre versus offshore cloud), S13, S10 (a flagship deal that stalled), S6 (vendor partnerships)
- **Source(s):**
  - "Microsoft and G42 announce $1 billion comprehensive digital ecosystem initiative for Kenya", Microsoft Source, https://news.microsoft.com/source/2024/05/22/microsoft-and-g42-announce-1-billion-comprehensive-digital-ecosystem-initiative-for-kenya, 22 May 2024
  - "Kenya's $1B Microsoft data centre project in limbo over power concerns", Citizen Digital, https://citizen.digital/article/kenyas-1b-microsoft-data-centre-project-in-limbo-over-power-concerns-n383281, 23 May 2026
  - "Kenya suspends plans for Microsoft's geothermal-powered data centre", ThinkGeoEnergy, https://www.thinkgeoenergy.com/kenya-suspends-plans-for-microsofts-geothermal-powered-data-centre/, 8 May 2026
  - All accessed 11 Nov 2026.
- **Confidence:** High for the announcement and the stall. Its exact status ("suspended" or "in limbo") differs between sources.
- **Caution:** Say "stalled; the government says it is not abandoned". The capacity figures do not match (Ruto's 2,300 MW versus peak demand above 3,000 MW in the same article). Teaching point: compute sovereignty depends on electricity first.

---

# Part C: Uganda

### GAP-16 AirQo (Makerere University) and KCCA: low-cost sensors and machine learning for Kampala's air
- **Organisation / country / industry / years:** AirQo project, Makerere University, with Kampala Capital City Authority (KCCA), Uganda, urban environment and public health, 2019 to 2025
- **What the AI does:** Cheap locally built sensors (on buildings and some boda bodas) measure fine dust. Machine learning corrects ("calibrates") their readings against expensive reference monitors, and KCCA uses an AI air-quality index to spot the most polluted areas.
- **Result:**
  - Calibration (peer-reviewed, 2022): the models were deployed across a network of more than 120 AirQo devices. Per the catalogue records, a random forest model cut the error of raw PM2.5 readings from 18.6 to 7.2 µg/m³ (RMSE), against an average reference concentration of 37.8 µg/m³.
  - Use by the city (SciDev.Net, Jan 2025): more than 65 sensors at about US$150 each across Kampala. KCCA's head of air quality monitoring said the data helps identify hotspots and has prompted traffic-management policies and public-health initiatives; the Health Ministry plans to use it on non-communicable diseases.
- **Themes:** S2, S1 (sensing), S3 (calibrating cheap sensors against reference ones), S14 (building a data network first), S7 (build locally), S13 (KCCA Clean Air Action Plan 2025 to 2030)
- **Source(s):**
  - "Applying machine learning for large scale field calibration of low-cost PM2.5 and PM10 air pollution sensors", Adong, Bainomugisha, Okure and Sserunjogi, Applied AI Letters 3(3) e76, 2022, DOI 10.1002/ail2.76 (record: https://doaj.org/article/d2a40331a1ce4f41b84fb5895b60c115)
  - "AI monitors help Uganda tackle air pollution crisis", SciDev.Net, https://www.scidev.net/global/news/ai-monitors-help-uganda-tackle-air-pollution-crisis/, 30 Jan 2025
  - Both accessed 11 Nov 2026.
- **Confidence:** High for the existence and scale of the network and calibration. Medium for the RMSE figures: I read the catalogue and search summaries, because the publisher page blocked automated reading.
- **Caution:** Check the RMSE numbers in the full paper before putting them on a slide. Sensor counts vary by date (65 to more than 100). There is no measured health outcome. The SciDev article does not name AirQo, though other sources link KCCA's network to it.

### GAP-17 Uganda's Personal Data Protection Office rules against Google
- **Organisation / country / industry / years:** Personal Data Protection Office (PDPO, under NITA-U), Uganda; complaint by four Ugandan citizens against Google LLC, filed 8 Nov 2024, decided 18 Jul 2025
- **What happened:** Four Ugandans complained that Google processed their data without registering with the PDPO and moved it abroad without safeguards. Google argued Uganda's law did not apply because it is not based there. The PDPO rejected that argument.
- **Result (regulatory outcome):** Google was found to be a data controller and collector under Ugandan law, in breach of the registration requirement, and to have transferred personal data outside Uganda without showing adequate safeguards. It was ordered to register within 30 days and to submit evidence of a compliant cross-border transfer framework. No compensation was reported.
- **Themes:** S13, S7 (any AI or cloud vendor processing Ugandans' data, wherever it sits, falls under the Act), S10 (regulatory action)
- **Source(s):** "Uganda's Data Protection Office finds Google in breach of privacy", Uganda Registration Services Bureau, https://ursb.go.ug/2025/08/12/ugandas-data-protection-office-finds-google-in-breach-of-privacy/, Aug 2025; accessed 11 Nov 2026. Also reported by New Vision ("Google declared in breach of Uganda's data protection laws") and CIPESA; I did not open those.
- **Confidence:** High (government agency source; widely reported).
- **Caution:** This is not an AI case as such. Use it for the vendor and cloud question: an offshore AI tool that handles customer data must still meet Uganda's registration and transfer rules. Google could appeal to the Minister of ICT; the outcome of any appeal was not found. Search results mention a similar PDPO finding against WhatsApp and Meta, which was not verified.

### GAP-18 Uganda's Ministry of ICT: a National Data Strategy before the National AI Strategy
- **Organisation / country / industry / years:** Ministry of ICT and National Guidance (MoICT&NG), with UN Global Pulse Uganda and UNDP, Uganda, public sector, 2026
- **What it is:** A five-year National Data Strategy to fix how government bodies collect, store and share data, explicitly as groundwork for the national AI strategy. In parallel, the ministry hired a Kenyan firm, led by University of Nairobi professor Timothy Waema, to draft a national strategy for AI and emerging technologies (reported March 2026).
- **Result:** The baseline survey found data for only 36% of the indicators in the Fourth National Development Plan (NDP IV); the target is 80% within five years. Agencies such as UBOS, NIRA and DCIC run isolated databases with different standards, so citizens resubmit the same records. The strategy has three pillars (governance, infrastructure, use), oversight by a National Data Steering Committee and a National Data Office, and anonymisation aligned to the Data Protection and Privacy Act 2019. The Permanent Secretary, Dr Aminah Zawedde, said AI depends on the quality of the data used to build and run it.
- **Themes:** S14, S13, S7, PEOPLE (training public servants; data focal points in each institution)
- **Source(s):**
  - "Government launches five-year data strategy ahead of AI adoption", Daily Monitor, https://www.monitor.co.ug/uganda/news/national/government-launches-five-year-data-strategy-ahead-of-ai-adoption-5639746, 21 Oct 2026
  - "Uganda taps Kenyan firm to shape national AI roadmap", NTV Kenya, https://ntvkenya.co.ke/?p=84568, Mar 2026 (search summary only; not opened)
  - Accessed 11 Nov 2026.
- **Confidence:** High for the data strategy (Daily Monitor, read in full). Medium for the Kenyan-firm contract (search summaries of two outlets; not opened).
- **Caution:** As of 11 Nov 2026 I found no confirmation that the national AI strategy has been published (PUB-06 recorded a June 2026 target). The 36% figure is the cleanest Ugandan "data before AI" number found.

### GAP-19 Centenary Group and Huawei: an AI and "agentic banking" partnership
- **Organisation / country / industry / years:** Centenary Group (Centenary Bank), Uganda, banking; MoU signed in Shanghai, 21 May 2026
- **What it is:** A memorandum of understanding under which Huawei will support Centenary on AI to automate routine banking tasks, improve fraud detection and risk management, and speed up loan approvals using alternative customer data. It also covers cloud, data-centre upgrades, cybersecurity and staff training.
- **Result:** No published result (an MoU only). Centenary serves more than 4 million customers. The chairman, Prof. John Ddumba-Ssentamu, called it the most significant agreement the group has signed in a generation.
- **Themes:** S6 and S7 (choosing a strategic vendor; Chinese versus US technology stacks), S2 (credit and fraud), S11, PEOPLE (staff training)
- **Source(s):** "Centenary Bank partners with Huawei in AI drive to break rural banking barriers in Uganda", Business Times Uganda, https://businesstimesug.com/centenary-group-huawei-ai-banking-uganda/, 23 May 2026; accessed 11 Nov 2026. Also covered by New Vision and The Observer (not opened).
- **Confidence:** Medium (one outlet read; others corroborate the headline).
- **Caution:** An intention, not a deployment. Alternative-data lending raises consent and data-protection questions under the 2019 Act (see GAP-17). It is the only named Ugandan-bank AI commitment found with any detail.

### GAP-20 MTN MoMo Uganda: AI transaction monitoring against fraud (claims without figures)
- **Organisation / country / industry / years:** MTN Uganda / MTN Mobile Money Uganda, mobile money, Oct 2025
- **What the AI does:** MTN says AI systems watch mobile-money transactions, learn normal patterns, and flag abnormal ones and possible fraud in real time. This is paired with customer education on PINs and one-time codes.
- **Result:** No published result for AI. MTN Uganda's CFO, Andrew John Bugembe, said AI "doesn't sleep or take weekends off" and becomes the strongest defence against fraud when used responsibly.
- **Themes:** S2 (fraud detection), S3 (no figures to judge accuracy or false alarms), S13
- **Source(s):** "How MTN MoMo is championing cybersecurity and AI to crush mobile money fraud", Publicist East Africa, https://publicisteastafrica.com/?p=13719, 16 Oct 2025; accessed 11 Nov 2026.
- **Confidence:** Medium (trade outlet quoting named executives).
- **Caution:** Use as a "measure it" exercise: ask what figures a board should demand. Do NOT attribute the widely quoted 85% fraud reduction to AI; MTN links it to awareness campaigns (see the caution on TEL-05). A Daily Monitor piece on the same theme blocked automated reading.

### GAP-21 Farmers Companion App, Mbale: a phone app that spots fall armyworm
- **Organisation / country / industry / years:** Nazirini Siraji (independent developer, Google Developer Group Mbale), Uganda, agriculture (maize); reported 13 Nov 2019
- **What the AI does:** A free phone app uses a TensorFlow image model to detect fall armyworm on a maize plant from a photo and identify the worm's life stage, which shows how serious the infestation is. It then suggests treatments.
- **Result:** No published result. Google reported it was "already working in the field" around Mbale.
- **Themes:** S1, S7 (built on free tools by a local developer)
- **Source(s):** "Machine learning meets African agriculture", Google Blog, https://blog.google/technology/ai/machine-learning-meets-african-agriculture, 13 Nov 2019; accessed 11 Nov 2026.
- **Confidence:** Medium (vendor blog about its own tools).
- **Caution:** Old, small and unmeasured. Use it only to show Ugandan grassroots building, alongside AGR-02 (Makerere cassava). Akorion's EzyAgric "EzyArmyWorm" diagnostic won a prize (reported in search results); its impact is unverified.

---

## Gaps
- **Ugandan banks:** still no measured AI result for Stanbic Uganda, dfcu, Absa Uganda, Equity Uganda or Centenary. Only the Centenary-Huawei MoU (GAP-19) has detail. UBA Uganda's "Leo" chatbot is real, but its Uganda launch date and results could not be confirmed. Centenary's WhatsApp banking is digital, not AI.
- **MTN Uganda and MoKash:** no figures (GAP-20). The Daily Monitor article was blocked.
- **URA, NIRA, NITA-U:** nothing new beyond PUB-01 and PUB-05. NITA-U has an MoU with Presight (UAE) for "AI-powered" services and a National AI Framework in development, but no deployment or result was found.
- **Uganda national AI strategy:** no evidence it was published by 11 Nov 2026.
- **Ugandan agritech with results:** none found. EzyAgric (Akorion), the PeDD app and university crop-disease apps describe aims, not measured outcomes.
- **East African enterprise knowledge assistants:** no Ugandan or Kenyan bank, telco or ministry has published results for an internal document-search assistant. The best African examples are South African (Standard Bank, Absa). Ecobank has a Google Cloud partnership (Jul 2025) but no named assistant or results.
- **Telecom knowledge bases in Africa:** no named African operator has published results for an agent-assist or knowledge tool. Telstra (GAP-01) is the benchmark. Vendor case studies for unnamed telcos (20 to 35% shorter handling times) were excluded.
- **Government document search in Africa:** only the ULII summaries (GAP-08). No African equivalent of UK Consult with results was found.
- **Figures seen only in search snippets and therefore excluded:** Standard Bank's "39,000 employees", Absa's "120+ LLMs and 40+ guardrails", McKinsey's "17 uses a week", JPMorgan LLM Suite's "200,000 users", the UlizaMama "12,000 daily queries" (NeurIPS demo), and Sunflower v2's "67 languages".
