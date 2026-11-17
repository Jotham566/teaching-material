# Case research: Healthcare & insurance, and Public sector (accessed 11 Nov 2026)

## Summary
This file holds 28 named, dated cases: 14 in healthcare and insurance (HLT) and 14 in the public sector (PUB). Every figure below comes from a page that was opened and read on 11 November 2026. Where a page could not be opened (paywall or blocked), the figure was dropped. Eleven cases are East African (Kenya, Uganda, Rwanda; PUB-06 also covers Nigeria), six are from the rest of Africa (Nigeria, South Africa, Togo) and eleven are global benchmarks (US, UK, Sweden, Netherlands, Australia, Thailand). Fourteen are failures or mixed results: Kenya SHA, Babyl, the South African schemes, Google in Thailand, Epic sepsis, Optum bias, nH Predict, Lemonade, Uganda national ID, Mavundla, Dutch childcare benefits, Robodebt, MiDAS and Ofqual. They cluster on one lesson: automated decisions about people with no human review and no explanation. The strongest measured successes are Penda Health (Kenya), MASAI (Sweden), the Edo State tutoring pilot (Nigeria), SARS auto-assessment and the Togo Novissi targeting. Several cases are not AI in the strict sense (Robodebt, MiDAS, Ndaga Muntu). They are flagged and kept on purpose, because a leader needs to see that rule-based automation fails in the same ways.

## Coverage table (case x theme)

| ID | Organisation | S1 | S2 | S3 | S4 | S5 | S6 | S7 | S8 | S9 | S10 | S11 | S12 | S13 | S14 | PEOPLE |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| HLT-01 | Penda Health (KE) | | | x | | x | x | | | x | | | x | | | x |
| HLT-02 | Jacaranda Health (KE) | | x | x | | x | | | | | | | x | | | x |
| HLT-03 | Kinondo Kwetu clinic (KE) | x | | x | | | | | | | | | | | | x |
| HLT-04 | Makerere AI Health Lab (UG) | x | | | | | | x | | | | | | | x | x |
| HLT-05 | Social Health Authority (KE) | | x | x | | | | | | | x | x | | x | | x |
| HLT-06 | Babyl / Babylon Health (RW) | | | | | | x | x | | | x | | | x | | x |
| HLT-07 | Qure.ai qXR in NE Nigeria + WHO | x | | x | | | x | | | | | | | x | | x |
| HLT-08 | Discovery, GEMS, Medscheme (ZA) | | x | x | | | | | | | x | | x | x | | x |
| HLT-09 | Google Health, Thailand MoPH | x | | x | | | | | | | x | | | | x | x |
| HLT-10 | MASAI trial (Sweden) | x | | x | | | | | | | | | x | | | x |
| HLT-11 | Epic Sepsis Model (US) | | x | x | | | x | | | | x | | | x | | x |
| HLT-12 | Optum Impact Pro (US) | | x | x | | | | | | | x | | | | x | |
| HLT-13 | UnitedHealth / naviHealth (US) | | x | | | | | | | | x | x | | x | | |
| HLT-14 | Lemonade (US/UK) | x | x | | | | | | | | x | x | x | x | | |
| PUB-01 | Uganda Revenue Authority | | x | | | | | x | | | | | x | | x | x |
| PUB-02 | Kenya Revenue Authority | x | x | | | | | | | | | x | | x | x | |
| PUB-03 | South African Revenue Service | | x | | | | | | | | | x | x | | x | x |
| PUB-04 | Judiciary of Kenya | x | | x | | x | | | | | | | x | x | | x |
| PUB-05 | Uganda national ID (NIRA) | x | | | | | | | | | x | | | x | x | x |
| PUB-06 | National AI policies (RW, KE, UG, NG) | | | | | | x | x | | | | | | x | x | x |
| PUB-07 | Togo Novissi | x | x | x | | | | | | | | | | x | x | |
| PUB-08 | Edo State / World Bank (NG) | | | x | | x | | | x | | | | x | | | x |
| PUB-09 | Mavundla case, KZN High Court (ZA) | | | | x | x | | | x | | x | | | x | | x |
| PUB-10 | UK Government (GDS) Copilot trial | | | x | | x | | x | x | | | | x | | | x |
| PUB-11 | Dutch Tax Administration | | x | | | | | | | | x | x | | x | x | x |
| PUB-12 | Robodebt (Australia) | | x | | | | | | | | x | x | | x | x | x |
| PUB-13 | Michigan UIA MiDAS (US) | | x | x | | | | x | | | x | x | | | | |
| PUB-14 | Ofqual (UK) | | x | x | | | | | | | x | | | x | x | |

---

# Part A: Healthcare and insurance

### HLT-01 Penda Health "AI Consult" clinical copilot
- **Organisation / country / industry / years:** Penda Health (with OpenAI), Kenya (Nairobi), primary care, 2024-2025
- **What the AI does:** While a clinician sees a patient, a large language model reads the clinical notes in the background. It flags possible errors in history-taking, investigations, diagnosis or treatment as a traffic-light alert, and the clinician keeps the decision.
- **Result:** The study covered 39,849 patient visits in 15 clinics, comparing clinicians with and without AI Consult. Clinicians with the tool made "16% fewer diagnostic errors and 13% fewer treatment errors". The authors estimate that at Penda alone this would avert diagnostic errors in 22,000 visits and treatment errors in 29,000 visits a year. All clinicians surveyed said it improved the quality of their care, and 75% said the effect was "substantial".
- **Themes:** S5, S9, S3, S6, S12, PEOPLE. People angle: the clinical officers are the users, and the tool works as a safety net rather than a replacement. Clinician adoption and attitude were measured.
- **Source(s):** "AI-based Clinical Decision Support for Primary Care: A Real-World Study", arXiv:2507.16947, https://arxiv.org/abs/2507.16947, submitted 22 Jul 2025; accessed 11 Nov 2026.
- **Confidence:** Medium. This is a primary source, but it is a preprint and the study was funded by the vendor.
- **Caution:** OpenAI funded the study and co-developed the tool. It is a quality-improvement study inside one health network, not a randomised trial across systems. The error reductions are relative, not absolute. Check whether a peer-reviewed version has since been published.

### HLT-02 Jacaranda Health PROMPTS: AI triage of mothers' SMS messages
- **Organisation / country / industry / years:** Jacaranda Health (with Penn State University), Kenya, maternal health, deployed June 2022
- **What the AI does:** Pregnant women and new mothers text questions in English, Swahili or a mix of both. A language model (TRIM-AI) scores each message for danger signs, so that a small help-desk team answers the urgent ones first and calls flagged mothers within an hour.
- **Result:** TRIM-AI is "roughly 17%" more accurate than Jacaranda's earlier baseline AI model at predicting high-risk conditions. It cut help-desk workload by about 12%. PROMPTS had more than 350,000 active users and received 1.1 million messages a month (Feb 2023).
- **Themes:** S5, S2, S3, S12, PEOPLE. People angle: the help-desk agents now spend their time on high-risk cases, and the AI sorts the queue.
- **Source(s):** "New AI tool helps provide better care for pregnant women", Penn State News, https://www.psu.edu/news/information-sciences-and-technology/story/new-ai-tool-helps-provide-better-care-pregnant-women, 6 Feb 2023; accessed 11 Nov 2026. The underlying paper is at AAAI 2023 ("A Continual Pre-Training Approach to Tele-Triaging Pregnant Women in Kenya").
- **Confidence:** Medium
- **Caution:** The 17% gain is measured against Jacaranda's own earlier model, not against human agents. User numbers come from the organisation itself. This is not an independent outcome evaluation.

### HLT-03 AI-read Pap smears at a rural Kenyan clinic
- **Organisation / country / industry / years:** Kinondo Kwetu Health Services Clinic, Kwale County, with University of Helsinki and Karolinska researchers, Kenya, cervical screening, published 2021
- **What the AI does:** A portable scanner photographs Pap smear slides at the clinic and uploads them over the mobile network. A deep-learning model then flags slides with abnormal cells, so that the scarce pathologist reviews only the suspicious ones.
- **Result:** The study took smears from 740 HIV-positive women. Measured against pathologists reading the digital slides, the AI found general atypia with 95.7% sensitivity and 84.7% specificity. Against the physical glass slides it reached 100% sensitivity and 78.4% specificity. The authors suggest pathologists could skip about 70% of slides.
- **Themes:** S1, S3, PEOPLE. People angle: it addresses the shortage of pathologists. A cytotechnologist screens first and a pathologist verifies flagged slides.
- **Source(s):** Holmström O. et al., "Point-of-Care Digital Cytology With Artificial Intelligence for Cervical Cancer Screening in a Resource-Limited Setting", JAMA Network Open 2021;4(3):e211740, https://pmc.ncbi.nlm.nih.gov/articles/PMC7970338, 17 Mar 2021; accessed 11 Nov 2026.
- **Confidence:** High (peer-reviewed)
- **Caution:** This is a single-site proof of concept. Specificity is lower than sensitivity, which means more false alarms (a good S3 teaching point). A later Kenyan news figure of "up to 99%" accuracy is not peer-reviewed; do not use it.

### HLT-04 Makerere AI Health Lab: smartphone malaria microscopy
- **Organisation / country / industry / years:** Makerere University AI Health Lab (Ocular project), with Ministry of Health support and Mulago National Referral Hospital, Uganda, 2019-2025
- **What the AI does:** A 3D-printed adapter clips a smartphone onto an ordinary lab microscope. AI then marks malaria parasites in the blood-smear image for a technician to confirm.
- **Result:** No published accuracy result was found. The lab says results come in under 60 seconds, compared with about 15 minutes for rapid tests and 25 to 30 minutes for microscopy. The tool is "still in the testing phase" (May 2025).
- **Themes:** S1, S14, S7, PEOPLE. People angle: Uganda is short of qualified lab technologists. The article cites a 2020 study that found nearly 50% of lab technologists absent from post, and many facilities rely on lab assistants. Data angle: the model is trained mainly on P. falciparum and needs more labelled local images.
- **Source(s):** "AI Tool to Revolutionize Malaria Diagnosis in Uganda", Makerere University CoCIS, https://cocis.mak.ac.ug/ai-tool-to-revolutionize-malaria-diagnosis-in-uganda-a-leap-toward-faster-more-accurate-detection/, 2 May 2025; accessed 11 Nov 2026.
- **Confidence:** Medium
- **Caution:** It is a pilot, and the speed figures are the lab's own claims. Use it as a home-grown build example, not as proven impact.

### HLT-05 Kenya Social Health Authority (SHA): AI fraud engine, and wrongly rejected claims (MIXED / FAILURE)
- **Organisation / country / industry / years:** Social Health Authority and Ministry of Health, Kenya, public health insurance, 2024-2026
- **What the AI does:** SHA's claims system uses an AI-driven engine to spot unusual patterns in hospital claims and member records in real time. Flagged claims are rejected or sent for investigation.
- **Result:**
  - **Government claim (Jan 2026):** Health CS Aden Duale told the Senate that the engine flagged one parent in Kwale registered with 381 dependants, and patients recorded as dialysed up to ten times a day. A ministry audit (Oct 2024 to Apr 2025) found Sh11 billion lost to fraudulent claims. In Sep 2025, 1,188 case files went to the DCI, 190 of them from SHA.
  - **Failure side:** the National Assembly Health Committee (report tabled Oct 2025) found that heavy reliance on AI-driven claim processing "with insufficient human oversight" led to unjust denials and financial strain on facilities.
  - **One hospital's figures:** at Kigumo Sub-County Hospital, 8.8% of Ksh 10 million in claims (Ksh 880,000) were rejected entirely for clerical errors, with no way to resubmit (Kenya Medical Association president, Mar 2026).
- **Themes:** S2, S3, S10, S11, S13, PEOPLE. People angle: hospital finance staff and clinicians absorb the cost of false alarms, and some private facilities reportedly opted out.
- **Source(s):**
  - "AI detects SHA fraud after member registered with 381 children", Capital FM, https://capitalfm.africa/ai-detects-sha-fraud-after-member-registered-with-381-children/, 29 Jan 2026
  - "MPs lay bare SHA flaws as Duale defends programme", The Star, https://www.the-star.co.ke/news/2025-10-15-mps-lay-bare-sha-flaws-as-duale-defends-programme, 15 Oct 2025
  - "How clerical errors being mislabelled by SHA as fraud are undermining healthcare in Kenya", HapaKenya, https://hapakenya.com/2026/03/09/how-clerical-errors-being-mislabelled-by-sha-as-fraud-are-undermining-healthcare-in-kenya/, 9 Mar 2026
  - All accessed 11 Nov 2026.
- **Confidence:** High (several independent outlets, a parliamentary committee and a minister's statement)
- **Caution:** The 381-dependant and dialysis examples are the minister's own statements. The Kigumo figures come from one hospital and were posted on social media by the Kenya Medical Association president. This is an excellent S3 case: the same engine is praised for catching fraud and blamed for false alarms.

### HLT-06 Babyl (Babylon Health) in Rwanda: when the vendor collapses (FAILURE)
- **Organisation / country / industry / years:** Babyl Rwanda, a unit of UK-based Babylon Health, Rwanda, digital health, about 2016-2023
- **What the AI does:** Babyl ran a national telemedicine service, integrated with national insurance schemes, under a 10-year partnership with the government. Its UK parent marketed AI symptom-checking. The sources read do not describe AI triage in the Rwandan service, which was mainly phone consultation.
- **Result:** The service had more than 2.5 million registered users, about 18% of Rwanda's population. After the parent company's take-private deal collapsed and it went bankrupt in August 2023, Babyl Rwanda ceased operations (reported 24 Sep 2023). The parent had a net loss of $221.4 million on $1.1 billion revenue in 2022.
- **Themes:** S7, S6, S10, S13, PEOPLE. People angle: local staff lost jobs, and patients lost a service. The lesson is about depending on a foreign platform.
- **Source(s):**
  - "Digital Success Cannot Beat Corporate Failure", ICTworks, https://www.ictworks.org/digital-success-cannot-beat-corporate-failure/, 4 Dec 2025
  - "UK Firm Babylon's Woes Impact Rwandan Healthcare", NextBillion, https://nextbillion.net/news/uk-firm-babylons-woes-impact-rwandan-healthcare, 21 Aug 2023
  - "Babyl Rwanda reportedly ceases operations", The New Times, https://www.newtimes.co.rw/article/11008/news/rwanda/babyl-rwanda-reportedly-ceases-operations, 24 Sep 2023
  - All accessed 11 Nov 2026.
- **Confidence:** Medium
- **Caution:** Teach this as a buy-versus-build and vendor-continuity case, not as an AI-accuracy failure. User figures vary between 2.5 and 2.8 million across sources.

### HLT-07 AI chest X-ray reading for TB in north-east Nigeria (and WHO guidance)
- **Organisation / country / industry / years:** TB screening camps in north-east Nigeria using an ultra-portable X-ray with Qure.ai's qXR v3 (authors include Stop TB Partnership staff), 2023. WHO screening guidance, 2021.
- **What the AI does:** Software reads each chest X-ray in seconds and scores how likely TB is. Only people above the threshold are sent for the confirmatory sputum test, which replaces a radiologist the camps do not have.
- **Result:** The camps screened 5,297 people across 66 camps. Of 1,021 Xpert tests, 85 people (8%) had confirmed TB. At a score of 0.50 or more, qXR identified 89.4% of TB cases with 62.8% specificity. Screening on "any symptom" caught 90.6% of cases but with only 11.4% specificity, and asking about prolonged cough found only 40%. In March 2021 WHO updated its TB screening guidance using evidence on computer-aided detection, noting that "close to three million" people with TB go undiagnosed or unreported each year.
- **Themes:** S1, S3, S6, S13, PEOPLE. People angle: the AI stands in for scarce human X-ray readers.
- **Source(s):**
  - "Comparing tuberculosis symptom screening to chest X-ray with artificial intelligence in an active case finding campaign in Northeast Nigeria" (John S. et al., BMC Global and Public Health, 6 Oct 2023), summary at https://qure.ai/evidence/comparing-tuberculosis-symptom-screening-to-chest-x-ray-with-artificial-intelligence-in-an-active-case-finding-campaign-in-northeast-nigeria
  - "WHO announces updated guidance on the systematic screening for tuberculosis", WHO, https://www.who.int/news/item/22-03-2021-who-announces-updated-guidance-on-the-systematic-screening-for-tuberculosis, 22 Mar 2021
  - Both accessed 11 Nov 2026.
- **Confidence:** Medium. The figures were read on the vendor's page summarising a peer-reviewed paper, because the journal page was blocked.
- **Caution:** Check the figures against the BMC paper before teaching. The WHO news page did not itself state the exact wording of the CAD recommendation (conditional, ages 15 and over, according to secondary sources); quote it only after reading WHO Module 2. A good S3 teaching pair: similar sensitivity, very different specificity.

### HLT-08 South African medical schemes: fraud-detection algorithms and the Section 59 racial-bias finding (MIXED / FAILURE)
- **Organisation / country / industry / years:** Discovery Health, Government Employees Medical Scheme (GEMS) and Medscheme, South Africa, health insurance, 2012-2025
- **What the AI does:** Scheme administrators run software that analyses claims data to flag doctors whose billing looks irregular. Investigators then pursue those doctors and claw back money.
- **Result:**
  - **Success side:** Discovery Health recovered R555m for client schemes from fraud, waste and abuse in 2018. That year 5,443 cases were reported, and about 75% of investigations confirmed concerns. Its in-house forensic system uses "continually updated algorithms", alongside a team of over 100 analysts and investigators.
  - **Failure side:** the Section 59 Investigation Panel's final report (April 2025, handed over July 2025) found that between 2012 and 2019 the fraud, waste and abuse processes discriminated against Black practitioners. Examples: Black psychiatrists at Discovery in 2017 were about 3.44 to 3.77 times more likely to be found guilty, and Black anaesthetists at Medscheme in 2018 about 6.5 times. The panel called the detection tools "black boxes" and recommended that the regulator get full access to the algorithms and their inputs.
- **Themes:** S2, S3, S10, S12, S13, PEOPLE. People angle: the affected doctors are the insurer's own provider network, and investigators' workflow is shaped by what the algorithm flags.
- **Source(s):**
  - "Discovery Health recovers R555m in fraud, waste and abuse savings for 2018", Discovery press release, https://www.mynewsdesk.com/za/discovery-holdings-ltd/pressreleases/discovery-health-recovers-r555m-in-fraud-waste-and-abuse-savings-for-2018-2845814, 11 Mar 2019
  - "Panel upholds findings of racial bias in medical scheme fraud investigations", Moonstone, https://www.moonstone.co.za/panel-upholds-findings-of-racial-bias-in-medical-scheme-fraud-investigations/, 10 Jul 2025
  - Final report PDF (not read in full): https://ndohwebsite.azurewebsites.net/wp-content/uploads/2025/07/Final-Report-Section-59-Investigations-25042025.pdf
  - All accessed 11 Nov 2026.
- **Confidence:** High
- **Caution:** Discovery and the Board of Healthcare Funders publicly reject the findings as methodologically flawed (Business Day, 8 Jul 2025). The panel itself says it made findings of fact, not legal rulings. Present both sides.

### HLT-09 Google Health diabetic eye screening in Thai clinics (FAILURE in the field)
- **Organisation / country / industry / years:** Google Health with Thailand's Ministry of Public Health, Thailand, eye screening, field study published April 2020
- **What the AI does:** Nurses photograph the back of a diabetic patient's eye, and the AI grades it for diabetic retinopathy in about a minute. Patients who need a specialist are referred on the spot.
- **Result:** In internal tests the system showed 90% accuracy. In 11 real clinics it rejected images that were blurred or dark (only some clinics had a room that could be darkened). Slow internet made some uploads take 60 to 90 seconds. Some nurses discouraged patients from joining because of the burden of on-the-spot referral. No overall rejection rate is quoted here, because the page read did not state one.
- **Themes:** S1, S3, S10, S14, PEOPLE. People angle: the nurses' workflow, workarounds and frustration decided success more than accuracy did.
- **Source(s):**
  - "Google medical researchers humbled when AI screening tool falls short in real-life testing", TechCrunch, https://techcrunch.com/2020/04/27/google-medical-researchers-humbled-when-ai-screening-tool-falls-short-in-real-life-testing/, 27 Apr 2020
  - Beede E. et al., "A Human-Centered Evaluation of a Deep Learning System Deployed in Clinics for the Detection of Diabetic Retinopathy", CHI 2020, https://research.google/pubs/pub48768/
  - Both accessed 11 Nov 2026.
- **Confidence:** High (Google's own peer-reviewed paper plus a major outlet)
- **Caution:** This was an early deployment. Do not imply the product later failed. The lesson is the gap between lab accuracy and the clinic.

### HLT-10 MASAI trial: AI-supported mammography screening, Sweden
- **Organisation / country / industry / years:** Lund University / Swedish national screening programme (MASAI trial, Lång et al., The Lancet Oncology), Sweden, published Aug 2023
- **What the AI does:** AI scores each mammogram for cancer risk. Low-risk exams get one radiologist instead of the usual two, and high-risk exams get two radiologists.
- **Result:** The interim safety analysis covered 80,033 women. The AI arm found 41 more cancers (about 20% more) than standard double reading, with no increase in false positives reported. Screen readings fell from 83,231 to 46,345, which is 44% less radiologist reading work.
- **Themes:** S1, S3, S12, PEOPLE. People angle: radiologist workload, at a time when radiologists are scarce.
- **Source(s):** "AI supported mammography screening could save lives and reduce workload for radiologists", News-Medical (reporting The Lancet Oncology), https://www.news-medical.net/news/20230801/AI-supported-mammography-screening-could-save-lives-and-reduce-workload-for-radiologists.aspx, 1 Aug 2023; accessed 11 Nov 2026.
- **Confidence:** High (randomised controlled trial; widely reported)
- **Caution:** These are interim results from one site. The primary endpoint (interval cancers, after at least two years of follow-up of 100,000 women) was pending at the time. Check for the final results before teaching. The authors warn that finding more cancers can also mean overdiagnosis.

### HLT-11 Epic Sepsis Model: vendor accuracy versus real-world accuracy (FAILURE)
- **Organisation / country / industry / years:** Epic Systems' sepsis prediction model, independently validated at Michigan Medicine, USA, published June 2021
- **What the AI does:** The model sits inside the hospital's electronic record and scores every inpatient's risk of sepsis. Above a threshold, it alerts the care team.
- **Result:** Across 38,455 hospitalisations, the area under the curve (AUC, a standard accuracy measure) was 0.63, against the 0.76 to 0.83 that had been reported. The model missed 67% of sepsis patients, yet it alerted on 18% of all inpatients, "creating a considerable burden of alert fatigue".
- **Themes:** S2, S3, S6, S10, S13, PEOPLE. People angle: nurses and doctors flooded with alerts.
- **Source(s):** "Epic Sepsis Model Has Poor Discrimination of Sepsis", HealthDay (reporting Wong A. et al., JAMA Internal Medicine, 21 Jun 2021), https://www.healthday.com/healthpro-news/infectious-disease/epic-sepsis-model-has-poor-discrimination-of-sepsis-2653467079.html, 22 Jun 2021; accessed 11 Nov 2026.
- **Confidence:** High (peer-reviewed; widely reported)
- **Caution:** Epic disputed the method, saying the two sides define sepsis onset differently. The lesson is to validate a vendor model on your own data.

### HLT-12 Optum "Impact Pro": cost used as a stand-in for need (FAILURE: bias)
- **Organisation / country / industry / years:** Optum (UnitedHealth Group) risk algorithm, studied by Obermeyer et al. in Science, USA, 2019
- **What the AI does:** The algorithm predicts which patients will cost the most next year. Hospitals and insurers used that score to choose who gets extra care-management support.
- **Result:** Black patients made up 17.7% of those above the 97th percentile when ranked by predicted cost. When ranked by number of chronic illnesses, the share was 46.5%. Retraining with health measures alongside cost cut the disparity at each risk score by 84%.
- **Themes:** S2, S3, S10, S14. Data angle: a convenient proxy (spending) carried historical inequality into the model.
- **Source(s):** "Bias in a common health care algorithm disproportionately hurts black patients", Science News, https://www.sciencenews.org/article/bias-common-health-care-algorithm-hurts-black-patients, 24 Oct 2019; accessed 11 Nov 2026. The paper is Obermeyer Z. et al., Science 366(6464):447-453, 25 Oct 2019.
- **Confidence:** High
- **Caution:** Optum cooperated with the researchers and retrained the model. Present it as a fixable design flaw, not malice.

### HLT-13 UnitedHealth / naviHealth "nH Predict" lawsuit (FAILURE: alleged)
- **Organisation / country / industry / years:** UnitedHealth Group and naviHealth, USA, Medicare Advantage health insurance, lawsuit filed Nov 2023
- **What the AI does:** The tool predicts how long an elderly patient should need care after a hospital stay. The lawsuit alleges the insurer used those predictions to cut off covered care.
- **Result:** These are allegations, not findings. The lawsuit claims the tool had a "90% error rate", with more than 90% of appealed denials reversed, and that the insurer counted on only about 0.2% of policyholders appealing. UnitedHealth says the tool "is not used to make coverage determinations" and calls the suit meritless.
- **Themes:** S10, S11, S13, S2
- **Source(s):** "UnitedHealthcare used AI to deny patients health insurance coverage, lawsuit says", Medical Economics, https://www.medicaleconomics.com/view/unitedhealthcare-used-ai-to-deny-patients-health-insurance-coverage-lawsuit-says, Nov 2023; accessed 11 Nov 2026.
- **Confidence:** Medium
- **Caution:** Always say "alleged". The case status after 2023 was not checked. It is useful for showing how the share of appeals reversed reveals error rates.

### HLT-14 Lemonade: automated claims, and an AI claim that backfired (MIXED)
- **Organisation / country / industry / years:** Lemonade Inc., USA and UK, home and contents insurance, 2016-2021
- **What the AI does:** A chatbot ("AI Jim") takes the first notice of a claim in the app, checks it against the policy and runs anti-fraud checks. It then pays simple claims instantly or hands the claim to a human.
- **Result:** Lemonade's 2020 SEC filing (as cited in coverage) says the bot handled first notice of loss for 96% of claims as of 30 Sep 2020, and resolved about a third of claims with no human involvement. In May 2021 Lemonade tweeted that its AI picks up "non-verbal clues" in claim videos. After public backlash it deleted the tweets, said AI never auto-denies claims, and called the wording a poor choice.
- **Themes:** S11, S12, S10, S13, S1
- **Source(s):** "Lemonade's Tweet About AI-Driven Fraud Detection Sparks Public Relations Crisis", Claims Journal, https://www.claimsjournal.com/news/national/2021/05/28/303993.htm, 28 May 2021; accessed 11 Nov 2026.
- **Confidence:** Medium
- **Caution:** The 96% and one-third figures were read second-hand from the SEC filing; check the 10-K before quoting. The "2-second claim" records are company publicity. The key lesson is that claiming more than the AI does is a reputational risk in its own right.

---

# Part B: Public sector

### PUB-01 Uganda Revenue Authority: AI on revenue leakage, built on a messy taxpayer register
- **Organisation / country / industry / years:** Uganda Revenue Authority (URA), Uganda, tax administration, 2019-2025
- **What the AI does:** URA uses AI and data analytics to spot tax evasion, such as undeclared imports and false VAT claims, by cross-checking records. It is also moving taxpayer registration from TIN to the national ID number (NIN).
- **Result:** Commissioner General John Rujoki Musinguzi said: "Last year alone, URA recovered 200 billion shillings in revenue leakages uncovered through the use of AI" (April 2025). An earlier URA staff study (2019) found "considerable problems of inaccurate data" in the taxpayer register: duplicated phone numbers and emails, and taxpayers holding several TINs.
- **Themes:** S2, S14, S7, S12, PEOPLE. Data angle: clean the register before AI. People angle: URA's own staff wrote the data-quality study, and URA funds a university AI lab.
- **Source(s):**
  - "URA CG launches University AI and Robotics Laboratory", URA, https://ura.go.ug/en/ura-cg-launches-university-ai-and-robotics-laboratory/, 8 Apr 2025
  - Mayega J. et al., "How Clean is our Taxpayer Register? Data Management in the Uganda Revenue Authority", ICTD African Tax Administration Paper 12, https://www.ictd.ac/publication/how-clean-is-our-taxpayer-register-data-management-in-the-uganda-revenue-authority/, 15 Jul 2019
  - Both accessed 11 Nov 2026.
- **Confidence:** Medium
- **Caution:** The UGX 200bn figure is a speech claim with no published method or audit. The 2019 data-quality findings may have improved since then. Daily Monitor coverage of URA's AI use exists but could not be opened.

### PUB-02 Kenya Revenue Authority: AI risk engines and automatic return checks
- **Organisation / country / industry / years:** Kenya Revenue Authority (KRA), Kenya, tax and customs, 2021-2026
- **What the AI does:** From 10 January 2026, iTax automatically checks declared income and expenses against electronic invoices (eTIMS), withholding-tax records and customs import data. Mismatches trigger audits, delayed refunds or rejected returns. Customs has piloted AI-powered risk engines.
- **Result:** No published result specific to AI was found. Reported context: customs revenue reached a record Sh85 billion in one month, and VAT rose from Sh20bn to Sh28bn a month since 2021/22 (President Ruto, 20 Nov 2025). Economist David Ndii said: "In a year or two, most of our taxes will be collected by algorithms and not by people."
- **Themes:** S2, S11, S13, S14, S1 (KRA has tendered for AI analysis of cargo scanner images; tender not read in detail)
- **Source(s):**
  - "EXPLAINER: How KRA will use AI tools to validate taxes, detect fraudulent returns", Citizen Digital, https://citizen.digital/article/explainer-how-kra-will-use-ai-tools-to-validate-taxes-detect-fraudulent-returns-n372684, 8 Nov 2025
  - "Ruto lauds KRA's AI reforms as Kenya targets Sh3 trillion revenue", The Star, https://www.the-star.co.ke/news/2025-11-20-ruto-lauds-kras-ai-reforms-as-kenya-targets-sh3-trillion-revenue, 20 Nov 2025
  - Both accessed 11 Nov 2026.
- **Confidence:** High for what is deployed. There is no measured result.
- **Caution:** The revenue growth cannot be attributed to AI. The legal basis is Section 23A of the Tax Procedures Act. Small and informal firms may be flagged because their records are incomplete (a fairness and people point).

### PUB-03 South African Revenue Service: auto-assessment and AI fraud detection
- **Organisation / country / industry / years:** SARS, South Africa, tax administration, 2023-2025
- **What the AI does:** SARS uses third-party data (employers, banks, medical schemes) with machine learning to issue tax assessments without the taxpayer filing a return. The same models flag suspicious refund claims before money leaves.
- **Result:**
  - In July 2025, nine days into the filing season, 65% of taxpayers had been assessed without filing. People who chose to file got an assessment "in under five seconds".
  - R5.5 billion in fraudulent or impermissible refunds was prevented (2025 season, early figure).
  - In 2023/24 the compliance programme yielded R293.7 billion, up 26.7% year on year.
- **Themes:** S2, S11, S12, S14, PEOPLE. People angle: Commissioner Kieswetter: "we are augmenting the work of our employees". SARS also announced recruitment in IT, data, legal and audit.
- **Source(s):**
  - "AI powers SARS efficiencies, says Kieswetter at G20 Zimbali meet", The Citizen, https://www.citizen.co.za/business/ai-powers-sars-efficiencies-says-kieswetter-at-g20-zimbali-meet, 18 Jul 2025
  - "SARS doubles down on AI, machine learning after revenue gains", ITWeb, https://itweb.co.za/article/sars-doubles-down-on-ai-machine-learning-after-revenue-gains/rxP3jqBEyeoMA2ye, 3 Apr 2024
  - Both accessed 11 Nov 2026.
- **Confidence:** High
- **Caution:** The figures are SARS's own, reported by media. The compliance yield is not all from AI. A widely quoted R444bn "outflows prevented" figure (2024/25 annual report) was not read here; do not use it without opening the report.

### PUB-04 Judiciary of Kenya: AI transcription and an AI policy for courts
- **Organisation / country / industry / years:** Judiciary of Kenya, Kenya, courts, 2024-2025
- **What the AI does:** Speech-to-text software transcribes court proceedings. The judiciary is drafting a policy that keeps AI as decision support (transcription, organising information, research) and not for writing judgments.
- **Result:** Chief Justice Martha Koome said transcription is now "majorly done by AI". She put accuracy at about 80%, up from about 30% when testing began (Aug 2025).
- **Themes:** S1 (speech), S5, S3, S12, S13, PEOPLE. People angle: court transcribers and clerks, plus a human check on AI output.
- **Source(s):** "AI court transcriptions in Kenya", Tech-ish, https://tech-ish.com/2025/08/13/ai-court-transcriptions-in-kenya/, 13 Aug 2025; accessed 11 Nov 2026.
- **Confidence:** Medium
- **Caution:** The accuracy figures come from a speech and have not been independently measured. A draft "AI Policy for the Judiciary of Kenya" v2.0 appeared online (2026); its adoption status was not confirmed.

### PUB-05 Uganda's national digital ID (Ndaga Muntu): exclusion when ID becomes the gate (FAILURE: data and ID)
- **Organisation / country / industry / years:** National Identification and Registration Authority (NIRA), Uganda, national ID, 2015-2021
- **What the system does:** A biometric national ID is required to access public health centres (since 2019), the Senior Citizens' Grant and many other services. This is not AI. It is the identity and data layer that every public AI service depends on.
- **Result:** Based on official sources, up to one third of Ugandan adults had not received an ID card. At least 50,000 Ugandans over 80 had ID errors or no ID, making them ineligible for the Senior Citizens' Grant. More than USD 200 million had been spent on the system over the previous decade. Older people's worn fingerprints are often rejected by the scanners.
- **Themes:** S14, S13, S10, S1 (biometrics), PEOPLE. People angle: health workers turned away patients without ID, and NIRA's enrolment staff and resources were stretched.
- **Source(s):** "Chased Away and Left to Die" (press release and report), Center for Human Rights and Global Justice (NYU), ISER and Unwanted Witness, https://chrgj.org/2021-06-08-report-finds-uganda-national-digital-id-system-leads-to-mass-exclusion/, 8 Jun 2021; accessed 11 Nov 2026.
- **Confidence:** High for the report's findings, which are an advocacy report drawing on official data.
- **Caution:** These are 2021 figures. Present it as data-readiness and governance context, not as an AI failure. It ties to URA's TIN-to-NIN move (PUB-01). Check the current figures and the status of the 2022 lawsuit.

### PUB-06 National AI policies: Rwanda, Kenya, Uganda, Nigeria
- **Organisation / country / industry / years:** Rwanda MINICT (2023, 2026), Kenya Ministry of Information, Communications and the Digital Economy (2025), Uganda Ministry of ICT and National Guidance (2025-2026), Nigeria Federal Ministry of Communications, Innovation and Digital Economy with NITDA and NCAIR (2024-2025)
- **What it does:** Each government sets national priorities, ethics rules and institutions for AI. Leaders will meet these documents as procurement and compliance requirements.
- **Result:** No measured result (these are policies).
  - **Rwanda:** Cabinet approved a National AI Policy on 20 April 2023, with six priorities including skills, compute, a data strategy and "trustworthy AI adoption in the public sector". Cabinet approved a National AI Agency on 8 June 2026.
  - **Kenya:** AI Strategy 2025-2030, with three pillars (infrastructure, data, research and innovation) and four enablers including governance and ethics. Priority sectors include healthcare, public service delivery and financial services.
  - **Uganda:** no final strategy yet. The Permanent Secretary said a National Strategy for AI and Emerging Technologies would be ready by June 2026, with priorities in agriculture, healthcare and public administration, plus a "sovereign data" concept aligned to the Data Protection and Privacy Act 2019.
  - **Nigeria:** draft National AI Strategy released August 2024 with five pillars, including an independent AI governance regulatory body. Analysts noted it had no timelines or funding sources.
- **Themes:** S13, S7, S6, S14, PEOPLE (skills pillars in all four)
- **Source(s):**
  - "Access Alert: Rwandan government approves National AI Policy", Access Partnership, https://accesspartnership.com/access-alert-rwandan-government-approves-national-ai-policy (2023)
  - "Govt to set up National Artificial Intelligence Agency", The New Times, https://www.newtimes.co.rw/article/36357/news/technology/govt-to-set-up-national-artificial-intelligence-agency, 8 Jun 2026
  - "Kenya Artificial Intelligence Strategy 2025-2030", OECD.AI Policy Navigator, https://oecd.ai/en/dashboards/policy-initiatives/kenya-artificial-intelligence-strategy-2025-2030
  - "Shaping Uganda's AI future", Ministry of ICT and National Guidance, https://ict.go.ug/media/news/shaping-ugandas-ai-future, 19 Mar 2025
  - "Uganda to Unveil Comprehensive AI and Emerging Tech Roadmap by June", PC Tech Magazine, https://pctechmag.com/2026/04/uganda-to-unveil-comprehensive-ai-and-emerging-tech-roadmap-by-june/, 2 Apr 2026
  - "Analysis of Nigeria's National Artificial Intelligence Strategy", Legal500/Mondaq, https://www.legal500.com/intelligence/nigeria/technology/analysis-of-nigeria%27s-national-artificial-intelligence-strategy, 19 Aug 2024
  - All accessed 11 Nov 2026.
- **Confidence:** High for dates and contents. Uganda's status is moving.
- **Caution:**
  - Uganda: whether the June 2026 target was met is unconfirmed; check ict.go.ug.
  - Nigeria: secondary sources say a final strategy came out in September 2025; this was not verified.
  - Kenya: the exact launch date is reported as 27 March 2025 by secondary sources.

### PUB-07 Togo Novissi: machine learning to target emergency cash
- **Organisation / country / industry / years:** Government of Togo with GiveDirectly and UC Berkeley researchers, Togo, social protection, 2020-2021
- **What the AI does:** Satellite images were used to find the poorest areas. Mobile-phone usage patterns were then used to predict which subscribers in those areas were poorest, so cash could be sent to their phones without a social register.
- **Result:** The approach identified and enrolled 138,500 recipients for the rural expansion. Compared with giving to everyone in selected villages, it reduced exclusion errors (poor people missed) by 4 to 21%. Households without a phone, about 15%, would be missed.
- **Themes:** S2, S1 (satellite), S3, S13, S14
- **Source(s):** "Using machine learning and mobile phone data to improve the speed and cost-effectiveness of social protection", J-PAL, https://www.povertyactionlab.org/case-study/using-machine-learning-and-mobile-phone-data-improve-speed-and-cost-effectiveness-social, updated Jun 2026; accessed 11 Nov 2026. The paper is Aiken, Bellue, Blumenstock, Karlan, Udry, "Machine learning and phone data can improve targeting of humanitarian aid", Nature 603 (2022): 864-870.
- **Confidence:** High
- **Caution:** The researchers say it should complement, not replace, a proper registry when time and data allow. The working paper also reports that, against a full registry (which Togo did not have), exclusion errors would be higher.

### PUB-08 Edo State, Nigeria: GPT-4-based after-school tutoring (World Bank pilot)
- **Organisation / country / industry / years:** Edo State Government with the World Bank, Nigeria, secondary education, June-July 2024
- **What the AI does:** First-year senior secondary students worked in pairs with Microsoft Copilot (GPT-4-based) as an English tutor, twice a week for six weeks. Teachers set the topic, the prompts and the reflection.
- **Result:** Students scored about 0.3 standard deviations higher than the control group, which the World Bank equates to "nearly two years of typical learning" in six weeks. The pilot outperformed 80% of education interventions in a database of randomised trials in developing countries. Girls, who started behind, gained more.
- **Themes:** S5, S8, S3, S12, PEOPLE. People angle: teachers acted as "orchestra conductors", and success depended on them.
- **Source(s):**
  - "From chalkboards to chatbots: Transforming learning in Nigeria, one prompt at a time", World Bank Blogs, https://blogs.worldbank.org/en/education/From-chalkboards-to-chatbots-Transforming-learning-in-Nigeria, 9 Jan 2025
  - "AI tutoring helps Nigerian students gain two years of learning in six weeks", The Decoder, https://the-decoder.com/ai-tutoring-helps-nigerian-students-gain-two-years-of-learning-in-six-weeks/, 8 Feb 2025
  - Both accessed 11 Nov 2026.
- **Confidence:** High
- **Caution:** It was a six-week pilot, and the full paper was "soon to be published" when the blog appeared. Attendance was hit by floods, strikes and power outages. Long-term effects are unknown.

### PUB-09 Mavundla v MEC (KwaZulu-Natal High Court): fake AI-generated case law (FAILURE)
- **Organisation / country / industry / years:** High Court of South Africa, KwaZulu-Natal Division (Pietermaritzburg), courts and legal profession, January 2025
- **What happened:** Lawyers filed submissions citing court cases produced by an AI research tool without checking them. The judge checked them.
- **Result:** Only 2 of 9 authorities cited were genuine. The court called the conduct "irresponsible and unprofessional" and referred the lawyers to the Legal Practice Council. A June 2025 Gauteng case (Northbound Processing) followed the same approach.
- **Themes:** S5, S10, S4, S8, S13, PEOPLE. People angle: junior staff used the tool and senior staff did not supervise. Pressure of work was no defence.
- **Source(s):** "South African lawyers learn hard lesson in AI fiction", TechCentral, https://techcentral.co.za/south-african-lawyers-learn-hard-lesson-in-ai-fiction/273932/, 7 Nov 2025; accessed 11 Nov 2026. Judgment: Mavundla v MEC: Department of Co-operative Government and Traditional Affairs KwaZulu-Natal and Others [2025] ZAKZPHC 2.
- **Confidence:** Medium
- **Caution:** Which tool was used is disputed. TechCentral names ChatGPT, the candidate attorney denied using it, and some law-firm notes name "Legal Genius". Say "an AI tool".

### PUB-10 UK Government Microsoft 365 Copilot experiment
- **Organisation / country / industry / years:** Government Digital Service (GDS), UK civil service, September-December 2024, published June 2025
- **What the AI does:** More than 20,000 civil servants in government organisations got an AI assistant inside Word, Outlook and Teams. They used it to draft documents, summarise meetings and handle email.
- **Result:** Average self-reported time saving was 26 minutes per user per day, or "nearly 2 working weeks" per person per year (3-month experiment).
- **Themes:** S8, S5, S12, S7, S3, PEOPLE. People angle: everyday staff adoption at scale.
- **Source(s):** "Landmark government trial shows AI could save civil servants nearly 2 weeks a year", GOV.UK, https://www.gov.uk/government/news/landmark-government-trial-shows-ai-could-save-civil-servants-nearly-2-weeks-a-year, 2 Jun 2025; accessed 11 Nov 2026.
- **Confidence:** High (primary)
- **Caution:** The savings are self-reported survey estimates, not measured time. Secondary coverage (The Register) says 17% of respondents reported no time saved. It is a good S3 case on how a productivity number is built.

### PUB-11 Dutch childcare benefits scandal (toeslagenaffaire) (FAILURE)
- **Organisation / country / industry / years:** Dutch Tax and Customs Administration, Netherlands, welfare and benefits, 2013-2021
- **What the AI does:** A self-learning risk model scored childcare-benefit applications for likely fraud. Non-Dutch nationality was one risk factor, and flagged families had benefits stopped and were investigated.
- **Result:**
  - Tens of thousands of parents were wrongly told to repay benefits, and ethnic minorities were disproportionately affected.
  - The Rutte cabinet resigned in early 2021.
  - The Dutch Data Protection Authority fined the tax administration EUR 2.75 million (Dec 2021) for discriminatory processing of nationality data.
  - Victims were promised EUR 30,000 compensation each.
  - Amnesty notes that civil servants reviewing flags were not told why a case scored high.
- **Themes:** S2, S10, S11, S13, S14, PEOPLE. People angle: staff "rubber-stamped" black-box flags, and an incentive to recover money drove behaviour.
- **Source(s):**
  - "Dutch childcare benefit scandal an urgent wake-up call to ban racist algorithms", Amnesty International, https://www.amnesty.org/en/?p=141886, 25 Oct 2021
  - "Childcare benefits scandal: Dutch government to pay million euro fine over racist data discrimination", netzpolitik.org, https://netzpolitik.org/2022/childcare-benefits-scandal-dutch-government-to-pay-million-euro-fine-over-racist-data-discrimination/, 6 Jan 2022
  - Both accessed 11 Nov 2026.
- **Confidence:** High
- **Caution:** Exact numbers of families vary by source (about 26,000 is often quoted, but it was not read here). Say "tens of thousands".

### PUB-12 Robodebt, Australia (FAILURE: automation, not AI)
- **Organisation / country / industry / years:** Department of Human Services / Services Australia, Australia, welfare debt recovery, 2015-2020; Royal Commission report 7 Jul 2023
- **What the system did:** It matched tax-office annual income data against welfare records, averaged annual income evenly across fortnights, and automatically raised a debt wherever the averaged figure differed from what the person had reported. Human checking was largely removed.
- **Result:**
  - The Royal Commission found it "a crude and cruel mechanism, neither fair nor legal".
  - 526,000 people received debt notices (the PM's statement says more than 500,000 victims).
  - The Commission found that automation and the removal of human intervention were "a key factor in the harm".
  - It made 57 recommendations, including a legal framework for automated decision-making, plain-language disclosure, independent scrutiny of business rules and algorithms, and an oversight body. A sealed chapter referred individuals for possible prosecution.
- **Themes:** S10, S11, S13, S2, S14, PEOPLE. People angle: staff concerns were overridden. The scheme was linked to known suicides.
- **Source(s):**
  - "Final report of the Royal Commission into the Robodebt Scheme", Prime Minister of Australia media statement, https://www.pm.gov.au/media/final-report-royal-commission-robodebt-scheme, 7 Jul 2023
  - "'Crude and cruel': Shameful Robodebt findings laid bare", Information Age (ACS), https://ia.acs.org.au/article/2023/crude-and-cruel-shameful-robodebt-findings-laid-bare.html, 10 Jul 2023
  - Both accessed 11 Nov 2026.
- **Confidence:** High
- **Caution:** This was not machine learning; it was a simple automated rule. That is exactly the point: rules without humans fail like AI does. Dollar figures (for example the A$1.8bn settlement) were not read on an opened page; do not quote them.

### PUB-13 Michigan MiDAS unemployment-fraud system (FAILURE)
- **Organisation / country / industry / years:** Michigan Unemployment Insurance Agency, USA, benefits administration, 2013-2017
- **What the system did:** An automated system (MiDAS) judged unemployment claimants guilty of fraud. In many cases no human was involved, and penalties, wage garnishment and seized tax refunds followed.
- **Result:**
  - A review reversed at least 44,000 fraud cases over two years, and the state refunded $20.8 million.
  - Of 40,000 cases decided solely by the computer, 85% were reversed. Of 22,000 cases referred to a human, 44% were overturned.
  - The article also cites a "93 percent error rate" from an earlier examination.
- **Themes:** S10, S11, S3, S2, S7
- **Source(s):** Insurance Journal (AP), "Michigan to refund $21M after unemployment fraud cases reversed", https://www.insurancejournal.com/news/midwest/2017/08/14/461016.htm, 14 Aug 2017; accessed 11 Nov 2026.
- **Confidence:** Medium
- **Caution:** Different sources describe the 93% and 85% figures differently. Quote the 85% (computer-only) versus 44% (human) comparison, which this page states clearly. A later $20m class settlement (Bauserman) was seen only in search results.

### PUB-14 Ofqual 2020 exam-grade algorithm (FAILURE)
- **Organisation / country / industry / years:** Ofqual (exams regulator) and the Department for Education, England, school examinations, August 2020
- **What the system did:** With exams cancelled during COVID, a statistical model adjusted teachers' predicted A-level grades using each school's past results. Teacher grades were used only for very small classes.
- **Result:** 39% of teacher-assessed A-level grades were marked down. Private schools increased their share of A and A* grades by 4.7 percentage points, more than double any other school type. After protests, on 17 Aug 2020 Ofqual reversed the decision and used teacher grades.
- **Themes:** S2, S3, S10, S13, S14
- **Source(s):** "U-turn will mean A-level and GCSE teacher grades stand", Tes, https://www.tes.com/news/u-turn-will-see-A-level-and-gcse-teacher-grades-stand, 17 Aug 2020; accessed 11 Nov 2026.
- **Confidence:** Medium
- **Caution:** This was a statistical standardisation model, not machine learning. It is a good public-legitimacy lesson: a model that is fair "on average" fails individuals.

---

## Gaps
- **East African private health insurers** (Jubilee, AAR, Britam, CIC, Sanlam, Old Mutual Kenya/Uganda): no named, sourced AI case with a result was found. NHIF and SHA (HLT-05) is the only East African insurance case.
- **URA and KRA measured AI results:** only leadership claims (URA's UGX 200bn) or totals not attributable to AI. Nothing independent or audited.
- **Measured results for the East African AI pilots** (Makerere malaria, Kenya judiciary transcription): none independently published.
- **Zipline:** the Rwanda blood-delivery study (51% fewer in-hospital postpartum-haemorrhage maternal deaths; Wharton / Manufacturing & Service Operations Management) is strong, but the sources describe drone logistics, not AI. It was left out for that reason; use it only as an "is this AI?" discussion.
- **IBM Watson for Oncology:** the STAT 2018 report and its secondary coverage were all paywalled or blocked, so the case was dropped.
- **Themes:**
  - S4 SEARCH and S9 KNOWLEDGE (grounded assistants) are thin in both sectors. Mavundla and Penda are partial fits only.
  - S6 MODELS has no clear local-language public-sector case. Jacaranda's Swahili model (UlizaLlama) has no published outcome.
- **City services** (KCCA, Nairobi, Kigali, Lagos) and **East African education ministries:** no reliable AI case found.
- **National ID and AI** (NIRA, Kenya Maisha Namba, Rwanda Irembo): only the 2021 Ndaga Muntu exclusion evidence; nothing on AI use.
- **Country gaps:** no Tanzania, Ethiopia or Ghana case was verified in these sectors.
