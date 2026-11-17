"""The 60 evaluation questions for Session 7. gold is a document tag, resolved to a doc_id by the build script."""
from kitara_names import fmt_ugx


def questions(LF):
    """LF: dict tag -> letter facts (from kitara_docs_c.LETTER_FACTS)."""
    Q = []

    def q(text, gold, hint, ans, kind="plain", asker="all_staff", cur="N", lang="en", note=""):
        Q.append(dict(question=text, gold=gold, hint=hint, answer=ans, kind=kind, asker=asker, cur=cur, lang=lang, note=note))

    # ------------------------------------------------------------------ 40 plain factual
    # 34 questions about policies, guides, circulars, minutes and notices, then 3 about scanned pages and 3 about letters.
    # Wording was chosen so that some are found by keyword search, some only by the meaning search, some by neither (see answer_key.json).
    q("What check happens on each borrower before a decision?", "loan", "Every application is checked against the credit reference bureau", "A credit reference bureau check on every application", asker="branch_ops", note="paraphrase")
    q("Who must approve an account for a politician?", "kyc", "written approval of the Head of Compliance before it is opened", "The Head of Compliance, in writing, before the account is opened (a politically exposed person)", asker="branch_ops", note="paraphrase")
    q("How long is CCTV retained in the branch?", "retention", "CCTV footage in branches: 90 days", "90 days")
    q("For how long can a home loan be taken?", "g_mortgage", "The loan runs for up to 20 years", "Up to 20 years")
    q("What is the ceiling on the amount a customer can take to pay tuition?", "g_fees", "Loans from UGX 500,000 up to UGX 15,000,000", "UGX 15,000,000")
    q("How much is deducted at the time the loan money is released?", "g_sme", "The processing fee is 1.5 percent of the loan", "A processing fee of 1.5 percent of the loan, paid at disbursement")
    q("How much does the customer contribute on a motor claim?", "g_motor", "excess of 10 percent of each claim", "10 percent of each claim, with a minimum of UGX 200,000 (15 percent for a driver under 23)")
    q("How many months before dying of sickness counts on a life policy?", "g_life", "Death from illness is covered after a waiting period of six months", "Six months")
    q("How is the rate for a house structure calculated?", "g_home", "premium for buildings cover is 0.25 percent of the sum insured", "0.25 percent of the sum insured a year")
    q("Which people have to authorise removing funds from the club account?", "g_group", "Any withdrawal needs two of the three signatories", "Two of the three signatories")
    q("Can a shopkeeper change a customer's secret number?", "g_wallet", "Agents cannot reset a PIN", "No. Only a branch can reset a PIN, with the customer's original identity card.", note="paraphrase")
    q("How much cash can a cashier keep at the counter?", "cash", "A teller may hold up to UGX 15,000,000 in the drawer", "UGX 15,000,000", asker="branch_ops")
    q("What does an agent earn when customers withdraw?", "agentguide", "0.5 percent of the value of each cash-out", "0.5 percent of the value of each cash-out", asker="branch_ops")
    q("What should I do with a scam message?", "c_phish", "Forward it to phishing@kitaragroup.example and delete it", "Do not click anything. Forward it to phishing@kitaragroup.example and delete it.", note="paraphrase")
    q("Can I paste client details into a free online assistant to summarise a letter?", "aiuse", "Do not enter customer names, account numbers, national identity numbers", "No. Customer data must not be entered into a public AI tool.", note="paraphrase")
    q("By when must a stolen device be declared to IT?", "infosec", "reported to the IT service desk within two hours", "Within two hours")
    q("By when must an insurance company pay an agreed claim, by law?", "r_claims", "must pay an accepted claim within 60 days", "Within 60 days of receiving the last document it asked for (notice IRO/2025/01, a fictional notice)")
    q("When did everyone have to register for two-step sign-in?", "c_mfa", "register for multi-factor authentication by 31 March 2026", "By 31 March 2026", note="paraphrase")
    q("How many written quotes are needed for a medium-sized purchase?", "procure", "need at least three written quotations", "At least three written quotations for a purchase above UGX 5,000,000", note="paraphrase")
    q("After how long does an account become inactive with no deposits or withdrawals?", "dormant", "no deposit or withdrawal for 12 months", "12 months", note="paraphrase")
    q("How much is the allowance for overnight lodging when travelling for work?", "expense", "Hotel: UGX 350,000 per night, bed and breakfast included", "UGX 350,000 per night, bed and breakfast included", note="paraphrase")
    q("How early must a holiday request be lodged?", "leaveproc", "at least 14 days before the first day of leave", "At least 14 days before the first day of leave", note="paraphrase")
    q("Who looks again at an outcome when the client disputes the result?", "complaints", "ask the Head of Customer Service to review the decision", "The Head of Customer Service", note="paraphrase")
    q("How soon should the main banking platform be back after an outage?", "bcp", "Core banking system: restored within four hours", "Within four hours (data loss no more than 15 minutes)", note="paraphrase")
    q("Who receives the report first when staff suspect theft by a colleague?", "fraudplan", "reported to the Head of Risk within 24 hours", "The Head of Risk, within 24 hours", asker="risk", note="paraphrase")
    q("What was the reason for declining the large loan request?", "m_credit", "because the monthly repayment would be 52 percent of net income", "The repayment would have been 52 percent of net income, above the 40 percent limit", asker="risk", note="paraphrase")
    q("What share of premiums was paid out as claims in Q2?", "m_exco", "claims ratio of 58 percent for Kitara Assurance", "58 percent (budget 55 percent)", asker="executive", note="paraphrase")
    q("When does the bank shut on Christmas Eve?", "c_holidays", "Branches close at 1:00 pm on 24 December 2025", "At 1:00 pm", asker="branch_ops", note="paraphrase")
    q("Which towns will the Kenyan subsidiary open new outlets in?", "m_board", "approved two new branches for Kitara Kenya, in Mombasa and Kisumu", "Mombasa and Kisumu", asker="executive", note="paraphrase")
    q("Can a person raise a concern without giving their name?", "whistle", "Reports can be anonymous", "Yes. Reports can be anonymous.", note="paraphrase")
    q("In which languages must a Kenyan institution publish how to complain?", "r_kenya", "publish the complaints procedure in English and in Swahili", "English and Swahili (notice CSAK/2026/01, a fictional notice)", asker="legal_compliance")
    q("Which staff were lent to Claims to clear the motor backlog?", "c_backlog", "Six claims officers from Underwriting and Customer Service", "Six claims officers from Underwriting and Customer Service", asker="claims")
    q("Can a teller inform the person that a laundering report is being sent?", "aml", "Staff must not tell the customer that a report has been made", "No. Staff must not tell the customer that a report has been made.", asker="branch_ops")
    q("How soon do investigators begin looking into a report of wrongdoing?", "whistle", "starts the review within seven working days", "Within seven working days")
    q("Since which year has annual leave been 21 days?", "s_circ2016", "rises from 18 working days to 21 working days", "From 1 January 2017 (Circular 2016/021, a scanned page)", note="scan")
    q("What did the inspector find wrong in the Mbarara vault and cash handling?", "s_inspect", "The vault log was not signed on three days", "Vault log unsigned on three days; teller cash over the limit; expired fire extinguisher", asker="branch_ops", note="scan")
    q("What is the garage estimate on the signed motor claim form for the Toyota Premio?", "s_claimform", "Damage estimate from garage", "UGX 4,850,000 (claim CL-2026-0388, a scanned form)", asker="claims", note="scan")
    L = LF["L01"]
    q(f"What repair cost did the customer report in motor claim {L['ref']}?", "L01", f"the repair at {fmt_ugx(L['amount'])}", fmt_ugx(L["amount"]), asker="claims")
    L = LF["L14"]
    q(f"Within how many days did Kitara promise to pay claim {L['ref']}?", "L14", f"within {L['days']} days of the date of this letter", f"{L['days']} days", asker="claims")
    L = LF["L21"]
    q(f"How much did the customer say was deducted twice from the wallet in complaint {L['ref']}?", "L21", f"Please refund {fmt_ugx(L['amount'])}", fmt_ugx(L["amount"]), asker="claims")

    # ------------------------------------------------------------------ 8 stale-version questions (the current document is the gold)
    q("How many days of annual leave am I entitled to each year?", "hb2025", "Staff earn 28 working days of annual leave", "28 working days (2019 edition: 21; 2022 edition: 24)", kind="stale", cur="Y", note="stale: 2019 and 2022 handbooks give a different number")
    q("How long is the probation period for a new permanent employee?", "hb2025", "probation period of three months", "Three months (2019: six months; 2022: four months)", kind="stale", cur="Y", note="stale: older handbooks differ")
    q("How many days a week may staff work remotely?", "hb2025", "may work remotely for up to three days a week", "Three days a week (2022: two days; 2019: not allowed)", kind="stale", cur="Y", note="stale: 2022 handbook says two days")
    q("How much can a member of staff claim as a single expense without written approval?", "hb2025", "A single expense claim above UGX 500,000 needs the written approval", "UGX 500,000 (2022: 350,000; 2019: 200,000)", kind="stale", cur="Y", note="stale: older handbooks have lower limits")
    q("What is the settlement timeframe for an accepted claim?", "sop4", "settles an accepted claim within 30 calendar days", "30 calendar days (SOP v3: 45 days)", kind="stale", cur="Y", asker="claims", note="stale: SOP v3 says 45 days")
    q("Up to what amount can a Claims Officer approve a claim?", "sop4", "Claims Officer: up to UGX 8,000,000", "UGX 8,000,000 (SOP v3: UGX 5,000,000)", kind="stale", cur="Y", asker="claims", note="stale: SOP v3 says UGX 5,000,000")
    q("What is the mileage rate for using a private vehicle on work?", "c_mile25", "mileage rate paid to staff who use a private vehicle on official business is UGX 2,200 per kilometre", "UGX 2,200 per kilometre (Circular 2023/017: UGX 1,900)", kind="stale", cur="Y", note="stale: Circular 2023/017 is superseded")
    q("What are the Saturday opening hours of the branches?", "c_hours25", "On Saturday branches open from 9:00 am to 1:00 pm", "9:00 am to 1:00 pm (Circular 2022/004: to 12:00 noon)", kind="stale", cur="Y", note="stale: Circular 2022/004 is superseded")

    # ------------------------------------------------------------------ 6 Swahili
    q("Matawi ya Kitara Kenya hufunguliwa saa ngapi siku ya Jumamosi?", "sw_hours", "saa 3:00 asubuhi hadi saa 7:00 mchana", "Saa 3:00 asubuhi hadi saa 7:00 mchana (9:00 am to 1:00 pm)", kind="swahili", lang="sw")
    q("Mfanyakazi aripoti ulaghai wa pesa kwa simu kwa idara gani, na ndani ya muda gani?", "sw_fraud", "Idara ya Usalama wa Mifumo ndani ya saa mbili", "Idara ya Usalama wa Mifumo, ndani ya saa mbili", kind="swahili", lang="sw")
    q("Wafanyakazi wa Kenya wana siku ngapi za likizo ya mwaka?", "sw_leave", "siku 26 za kazi za likizo ya mwaka", "Siku 26 za kazi", kind="swahili", lang="sw")
    q("Mteja anaweza kuweka kiasi gani cha juu kwenye pochi ya simu?", "g_wallet", "The most you can hold in the wallet is UGX 10,000,000", "UGX 10,000,000", kind="swahili", lang="sw", note="Swahili question about an English document")
    q("Neno la siri linapaswa kuwa na herufi ngapi angalau?", "infosec", "Passwords have at least 12 characters", "Herufi 12 (12 characters)", kind="swahili", lang="sw", note="Swahili question about an English document")
    q("Dai la bima ya gari hulipwa baada ya siku ngapi?", "sop4", "settles an accepted claim within 30 calendar days", "Siku 30 (30 calendar days)", kind="swahili", lang="sw", cur="Y", asker="claims", note="Swahili question about an English document")

    # ------------------------------------------------------------------ 6 the asker must not see the gold document
    q("What are the monthly salary bands for each grade?", "hb2025_salary", "Grade G5 (branch manager, senior claims officer)", "G5 is UGX 3,400,000 to 5,200,000", kind="restricted", asker="all_staff", note="gold is confidential to hr and executive")
    q("How much does a non-executive director get paid for each board sitting?", "m_hr", "UGX 3,500,000 for each Board sitting", "UGX 3,500,000 from 1 April 2026", kind="restricted", asker="branch_ops", note="gold is confidential to hr and executive")
    q("What penalty did the regulator impose on Kitara Bank for filing its returns late?", "r_enforce", "A penalty of UGX 12,000,000 is imposed", "UGX 12,000,000", kind="restricted", asker="claims", note="gold is confidential to legal_compliance and executive")
    q("How much of each risk does Kitara keep under the reinsurance programme?", "reinsure", "Kitara retains the first UGX 500,000,000 on any one risk", "The first UGX 500,000,000", kind="restricted", asker="hr", note="gold is confidential to underwriting, finance and executive")
    q("Which customer's relative had dialysis and what was claimed under the life policy?", "L11", "kidney failure and had been on dialysis", "Health detail in a confidential life claim letter", kind="restricted", asker="branch_ops", note="gold is a confidential life claim letter, claims only")
    q("What was the payment of UGX 86,000,000 to a supplier that does not exist?", "m_audit", "payment of UGX 86,000,000 made to a supplier that does not exist", "A suspected fraud investigated by the Special Investigations Unit", kind="restricted", asker="hr", note="gold is confidential to executive and legal_compliance")
    return Q
