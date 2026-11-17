"""Kitara document corpus, part B: circulars, committee minutes, regulatory notices, scan source texts. All fictional."""
from kitara_docs_a import doc, DOCS, ALL

FICT = "FICTIONAL NOTICE FOR TRAINING USE. The regulator named in this notice does not exist."

# ======================================================================= (e) CIRCULARS
def circ(tag, file, ref, title, date, status, dept, body, fmt="text_pdf", groups=ALL, sens="internal", lang="en", **kw):
    head = f"Ref: {ref}\nDate: {date}\nSubject: {title}\n\n" if lang == "en" else ""
    doc(tag, file, f"Circular {ref}: {title}" if lang == "en" else f"Mzunguko {ref}: {title}", "circular", ref, status, date, dept, sens, groups,
        head + body, fmt=fmt, lang=lang, **kw)


circ("c_mile23", "circulars/Circular 2023-017 Mileage Rate.pdf", "2023/017", "Mileage rate for private vehicles", "2023-09-01", "superseded", "Finance", """
To: All staff
From: Chief Finance Officer

From 1 September 2023 the mileage rate paid to staff who use a private vehicle on official business is UGX 1,900 per kilometre. The rate applies to journeys approved in advance by the Head of Department. Staff record the start and end of each journey on the mileage form and attach it to the expense claim.

Mileage is not paid for the journey between home and the normal place of work.
""")

circ("c_mile25", "circulars/Circular 2025-006 Mileage Rate.pdf", "2025/006", "Mileage rate for private vehicles", "2025-07-01", "current", "Finance", """
To: All staff
From: Chief Finance Officer

This circular replaces Circular 2023/017. From 1 July 2025 the mileage rate paid to staff who use a private vehicle on official business is UGX 2,200 per kilometre. The increase follows the rise in the pump price of fuel. The other rules in the Expense Policy are unchanged: the journey is approved in advance and the mileage form is attached to the claim.
""")

circ("c_hours22", "circulars/Circular 2022-004 Branch Opening Hours.pdf", "2022/004", "Branch opening hours", "2022-02-01", "superseded", "Branch Operations", """
To: All Branch Managers
From: Head of Branch Operations

From 1 March 2022 all Uganda branches open from 8:30 am to 4:30 pm, Monday to Friday. On Saturday branches open from 9:00 am to 12:00 noon. Branches are closed on Sundays and public holidays. Managers must display the hours at the entrance.
""")

circ("c_hours25", "circulars/Circular 2025-002 Branch Opening Hours.pdf", "2025/002", "Branch opening hours", "2025-01-06", "current", "Branch Operations", """
To: All Branch Managers
From: Head of Branch Operations

This circular replaces Circular 2022/004. From 1 February 2025 all Uganda branches open from 8:30 am to 5:00 pm, Monday to Friday. On Saturday branches open from 9:00 am to 1:00 pm. Branches stay closed on Sundays and public holidays.

Customers who are inside the branch at closing time are served before the doors are locked. The new hours are displayed at the entrance and on the mobile app by 24 January 2025.
""")

circ("c_float24", "circulars/Circular 2024-010 Agent Float Limit.pdf", "2024/010", "Daily float cap for mobile money agents", "2024-05-02", "superseded", "Branch Operations", """
To: Agent Network Managers
From: Head of Branch Operations

From 1 June 2024 the daily float cap for each mobile money agent is UGX 20,000,000. An agent who needs more float for market days writes to the Agent Network Manager at least two days before.
""", groups="branch_ops;executive")

circ("c_float25", "circulars/Circular 2025-015 Agent Float Limit.pdf", "2025/015", "Daily float cap for mobile money agents", "2025-04-14", "current", "Branch Operations", """
To: Agent Network Managers
From: Head of Branch Operations

This circular replaces Circular 2024/010. From 1 May 2025 the daily float cap for each mobile money agent is UGX 30,000,000. The cap was raised because agents in trading towns were turning customers away on market days.

Agents above UGX 30,000,000 of float in a day are monitored weekly under the Anti-Money-Laundering Policy. Agent Network Managers report agents who exceed the cap to Branch Operations.
""", groups="branch_ops;executive")

circ("c_mfa", "circulars/Circular 2025-009 Multi-Factor Authentication.pdf", "2025/009", "Multi-factor authentication for all staff", "2025-06-10", "current", "IT", """
To: All staff
From: Head of IT

All staff must register for multi-factor authentication by 31 March 2026. After that date accounts without a registered device will be locked. Register on the IT self-service page using your phone or a hardware token supplied by IT.

Staff without a smartphone can ask the IT service desk for a token. Bring your staff card. The service desk is open from 8:00 am to 5:00 pm.
""")

circ("c_permit", "circulars/Circular 2025-020 Identification Documents.pdf", "2025/020", "Identification documents for new accounts", "2025-10-06", "current", "Legal and Compliance", """
To: All Branch Managers and Agent Network Managers
From: Head of Compliance

Compliance audits found that a driving permit was accepted as the only identification for new savings accounts in eleven branches. This is not allowed. A driving permit is accepted only for opening a Mobile Wallet. For savings and current accounts the customer must show a national identity card, a valid passport or a refugee identity card, as the KYC Procedure says.

Branches that opened accounts in this way must contact the customers and collect the correct identification by 30 November 2025.
""")

circ("c_procure", "circulars/Circular 2025-011 Procurement Thresholds.pdf", "2025/011", "Procurement quotation thresholds", "2025-01-20", "current", "Finance", """
To: All Heads of Department
From: Chief Finance Officer

The quotation threshold has been raised from UGX 2,000,000 to UGX 5,000,000. Purchases above UGX 5,000,000 need three written quotations. The Tender Committee threshold of UGX 50,000,000 does not change. The change is included in the Procurement Policy of 2025.
""")

circ("c_ai", "circulars/Circular 2026-011 Generative AI Tools.pdf", "2026/011", "Use of generative AI tools", "2026-05-25", "current", "IT", """
To: All staff
From: Head of IT and Head of Legal and Compliance

The Acceptable Use of Generative AI Tools policy takes effect on 1 June 2026. Two staff members pasted customer complaint emails into a public chatbot in April. The emails held names and phone numbers. We treated both cases as security incidents and the customers were not harmed.

From 1 June do not paste customer data, claim files, loan files or salary data into any public AI tool. Staff who want to use AI for work can register for the internal AI sandbox with IT Security. Register through the IT service desk. Training sessions are held on the first Wednesday of each month.
""")

circ("c_holidays", "circulars/Circular 2025-021 December Opening.pdf", "2025/021", "Branch opening over the December holidays", "2025-11-17", "current", "Branch Operations", """
To: All Branch Managers
From: Head of Branch Operations

Branches close at 1:00 pm on 24 December 2025 and 31 December 2025. All branches are closed on 25 December and 26 December and on 1 January 2026. Branches in Kampala and Entebbe open on Saturday 27 December for school fees payments from 9:00 am to 1:00 pm. Agents continue to operate under their own licences.
""")

circ("c_backlog", "circulars/Circular 2026-009 Claims Backlog.pdf", "2026/009", "Motor claims backlog in the third quarter", "2026-09-14", "current", "Claims", """
To: Claims Department and Branch Managers
From: Head of Claims

On 31 August 2026 there were 412 open motor claims older than 30 days. The main causes are missing police reports and late assessor reports. Six claims officers from Underwriting and Customer Service are placed in Claims until 30 November 2026 to clear the backlog.

Branch Managers must send the police report with the claim form and not after. Branches that send incomplete files will receive them back with a checklist. Customers with claims older than 45 days are called by a claims officer every week.
""", groups="claims;branch_ops;executive", sens="restricted")

circ("c_disc", "circulars/Circular 2025-018 Disciplinary Procedure.pdf", "2025/018", "Changes to the disciplinary procedure", "2025-08-12", "current", "HR", """
To: Heads of Department and Human Resources
From: Head of Human Resources
Confidential: not for display or forwarding

The disciplinary procedure changes from 1 September 2025. A disciplinary hearing is held within 10 working days of the charge letter. A written warning stays on the file for 12 months and a final written warning for 24 months. A manager may suspend a staff member on full pay for up to 30 days while an allegation of gross misconduct is investigated.

Cases involving fraud are passed to the Special Investigations Unit before any hearing is set. Human Resources keeps the register of cases. Managers must not discuss a case outside the people named in the file.
""", groups="hr;executive", sens="confidential")

circ("c_phish", "circulars/Circular 2026-004 Phishing Emails.txt", "2026/004", "Phishing emails: what to do", "2026-02-09", "current", "IT", """
To: All staff
From: IT Security

In January we received 214 phishing emails that got past the filter. Five staff clicked the link. No money was lost.

If an email asks for your password, a payment, or to open an attachment you did not expect, do not click it. Forward it to phishing@kitaragroup.example and delete it. If you have already clicked, switch off your wifi and call the IT service desk on extension 4100 at once.

IT will never ask for your password by email or phone.
""", fmt="txt")

circ("c_yearend", "circulars/Circular 2026-002 Year-End Close.txt", "2026/002", "Year-end close timetable", "2026-01-12", "current", "Finance", """
To: All Heads of Department
From: Chief Finance Officer

The Finance ledger closes for the 2025 year on 31 December. Departments post accruals by 5 January. The trial balance is shared on 12 January. Branch managers confirm cash and suspense account balances by 7 January. Audit fieldwork starts on 19 January.

Late journals after 5 January need the written approval of the Chief Finance Officer.
""", fmt="txt")

circ("c_wellness", "circulars/Circular 2025-013 Staff Wellness Day.txt", "2025/013", "Staff wellness day", "2025-08-25", "current", "HR", """
To: All staff
From: Head of Human Resources

Staff may take a half day on the first Friday of March, June, September and December for the wellness programme. Branches stay open and managers will roster staff. Choose from health screening, financial coaching and exercise sessions. Register on the HR portal one week before.
""", fmt="txt")

circ("c_mfa2", "circulars/Circular 2026-007 MFA Re-registration.txt", "2026/007", "Re-registration of multi-factor devices", "2026-08-03", "current", "IT", """
To: All staff
From: Head of IT

Staff who changed their phone since registering for multi-factor authentication must register the new phone by 30 November 2026. A lost phone is reported to the IT service desk within two hours, as the Information Security Policy requires. IT will remove the old device and issue a temporary code valid for 24 hours.
""", fmt="txt")

# --- Swahili circulars from Kitara Kenya
circ("sw_hours", "circulars/Mzunguko KK-2026-003 Saa za Kazi.pdf", "KK/2026/003", "Saa za kazi za matawi ya Kitara Kenya", "2026-01-12", "current", "Branch Operations", """
Kwa: Wafanyakazi wote wa Kitara Kenya
Kutoka: Meneja Mkuu wa Matawi, Nairobi
Tarehe: 12 Januari 2026
Kuhusu: Saa mpya za kazi za matawi

Tunawajulisha wafanyakazi wote kuwa kuanzia tarehe 1 Februari 2026, matawi yote tisa ya Kitara Kenya yatafunguliwa kuanzia saa 2:30 asubuhi hadi saa 11:00 jioni, Jumatatu hadi Ijumaa. Siku ya Jumamosi, matawi yatafunguliwa kuanzia saa 3:00 asubuhi hadi saa 7:00 mchana. Matawi yatafungwa siku ya Jumapili na siku za sikukuu za kitaifa.

Meneja wa tawi atahakikisha kuwa wafanyakazi wawili wanafika dakika thelathini kabla ya kufungua. Wateja wote wanaofika kabla ya saa za kufunga watahudumiwa. Tafadhali weka tangazo la saa hizi mlangoni mwa kila tawi kabla ya tarehe 25 Januari 2026.

Kwa maswali, wasiliana na ofisi ya Uendeshaji wa Matawi, Nairobi.
""", lang="sw")

circ("sw_fraud", "circulars/Mzunguko KK-2026-005 Ulaghai wa Pesa kwa Simu.pdf", "KK/2026/005", "Kuripoti ulaghai wa pesa kwa simu", "2026-03-02", "current", "Risk", """
Kwa: Wafanyakazi wote wa matawi ya Kitara Kenya
Kutoka: Mkuu wa Usalama wa Mifumo, Nairobi
Tarehe: 2 Machi 2026
Kuhusu: Ulaghai wa pesa kwa simu

Wateja wengi wamepokea ujumbe wa uongo wa simu unaodai kuwa wametumiwa pesa kwa makosa. Wateja wanaombwa kurudisha pesa hizo kwa namba wasiyoifahamu. Huu ni ulaghai.

Kila mfanyakazi wa tawi anapaswa kufanya yafuatayo:
- Kumwambia mteja asitume pesa kwa mtu asiyemjua.
- Kuandika jina la mteja, namba ya simu na saa ya tukio.
- Kuripoti tukio kwa Idara ya Usalama wa Mifumo ndani ya saa mbili.
- Kumwomba mteja apige simu kwa huduma kwa wateja, namba 0800 100 300, ili pochi yake izuiwe ikiwa ni lazima.

Mfanyakazi hapaswi kamwe kuuliza PIN ya mteja. Idara ya Usalama itatuma muhtasari wa matukio kila mwezi.
""", lang="sw")

circ("sw_leave", "circulars/Mzunguko KK-2026-008 Likizo ya Mwaka.pdf", "KK/2026/008", "Likizo ya mwaka kwa wafanyakazi wa Kitara Kenya", "2026-04-20", "current", "HR", """
Kwa: Wafanyakazi wote wa Kitara Kenya
Kutoka: Mkuu wa Rasilimali Watu, Nairobi
Tarehe: 20 Aprili 2026
Kuhusu: Likizo ya mwaka

Wafanyakazi wa Kitara Kenya wana haki ya siku 26 za kazi za likizo ya mwaka. Siku zisizozidi nane ambazo hazijatumika zinaweza kuhamishiwa mwaka unaofuata hadi tarehe 31 Machi. Likizo ya uzazi ni miezi mitatu kwa malipo kamili, na likizo ya baba ni siku 14.

Maombi ya likizo yatumwe kupitia mfumo wa Rasilimali Watu angalau siku 14 kabla ya likizo kuanza. Meneja wa tawi ataidhinisha au kukataa ombi ndani ya siku tatu za kazi. Mfanyakazi aliye mgonjwa anapaswa kumjulisha meneja wake siku hiyo hiyo.
""", lang="sw")

# ======================================================================= (f) MINUTES
def minutes(tag, file, title, date, dept, sens, groups, body, fmt="text_pdf", **kw):
    doc(tag, file, title, "minutes", "1", "current", date, dept, sens, groups, body, fmt=fmt, **kw)


minutes("m_board", "minutes/Board Minutes Extract March 2026.pdf", "Board of Directors: Minutes Extract, 26 March 2026", "2026-03-26",
        "Company Secretary", "restricted", "executive", """
Kitara Group Board of Directors. Extract of the minutes of the meeting held on 26 March 2026 at Kampala. Present: nine directors and the Company Secretary.

## Item 4: Core banking upgrade
The Board approved capital expenditure of UGX 4.2 billion for the core banking upgrade, to be paid over two years. The Chief Operating Officer will report progress each quarter. The Board asked that the contract include a data export clause so that Kitara can move its data to another vendor without a fee.

## Item 5: Kitara Kenya expansion
The Board approved two new branches for Kitara Kenya, in Mombasa and Kisumu, to open before the end of 2026. This brings the Kenya network to nine branches.

## Item 6: External auditors
The Board approved the re-appointment of the external auditors for one more year, subject to the Annual General Meeting.

## Item 7: Dividend
The Board recommended a dividend of UGX 38 per share.
""")

minutes("m_audit", "minutes/Audit Committee Minutes Extract February 2026.pdf", "Audit Committee: Minutes Extract, 18 February 2026", "2026-02-18",
        "Internal Audit", "confidential", "executive;legal_compliance", """
Audit Committee of the Board. Extract of the minutes of 18 February 2026. Confidential to the Committee, the Executive Committee and Legal and Compliance.

## Item 3: Internal audit findings
Internal Audit reported 14 open findings. Three are rated high. The high rated findings are: no owner for the shared drive that holds branch reports, 312 leavers with active access to the shared drive, and claims documents stored without a retention date.

## Item 5: Special investigation
The Special Investigations Unit reported on the investigation into a payment of UGX 86,000,000 made to a supplier that does not exist. Two members of Finance staff are suspended on full pay. The Committee asked Legal and Compliance to report the matter to the police and to the regulator.

## Item 7: Management actions
Management will name an owner for each of the 14 sources in the data inventory by 30 June 2026.
""")

minutes("m_risk", "minutes/Risk Committee Minutes Extract April 2026.pdf", "Risk Committee: Minutes Extract, 14 April 2026", "2026-04-14",
        "Risk", "restricted", "risk;executive;legal_compliance", """
Risk Committee. Extract of the minutes of 14 April 2026.

## Item 2: Complaints report for March
Customer Service reported 612 complaints in March. 71 percent were resolved within 14 days. The slowest category was motor claims, with an average of 38 days to resolve.

## Item 4: Top risks
The Committee ranked the top three risks: failure of the mobile money switch, fraud by insiders, and poor quality of customer data that feeds the regulatory returns. The Committee noted that two regulatory returns in the first quarter were corrected after submission because of duplicate customer records.

## Item 6: Data quality
The Head of Risk will propose six data quality rules for the customer table and a monthly report to this Committee.
""")

minutes("m_credit", "minutes/Credit Committee Minutes Extract January 2026.pdf", "Head Office Credit Committee: Minutes Extract, 13 January 2026", "2026-01-13",
        "Risk", "restricted", "risk;finance;executive;branch_ops", """
Head Office Credit Committee. Extract of the minutes of the meeting held on the second Tuesday, 13 January 2026.

## Item 1: Approvals
The Committee approved an SME loan of UGX 180,000,000 to a fictional agro-processing company, over 48 months at 19 percent a year, secured by a title valued at UGX 250,000,000. The collateral cover is 139 percent.

## Item 2: Declined
The Committee declined an application for UGX 320,000,000 because the monthly repayment would be 52 percent of net income, above the limit of 40 percent.

## Item 3: Write-offs
The Committee approved the write-off of 38 school fees loans, total UGX 61,400,000, after two years of recovery efforts.
""")

minutes("m_claims", "minutes/Claims Committee Minutes Extract May 2026.pdf", "Claims Committee: Minutes Extract, 21 May 2026", "2026-05-21",
        "Claims", "restricted", "claims;executive", """
Claims Committee. Extract of the minutes of 21 May 2026. Claims above UGX 100,000,000 are decided by this Committee under the Claims Handling SOP v4.

## Item 1: Fire claim
The Committee approved a fire claim of UGX 240,000,000 on a commercial building in Jinja. The adjuster's report was received within seven working days.

## Item 2: Declined claim
The Committee confirmed the decline of a life claim of UGX 120,000,000. The insured had not declared a heart condition on the application.

## Item 3: Suspected fraud
Three motor claims from the same garage were referred to the Special Investigations Unit. The Committee asked that the garage be removed from the approved list until the review ends.
""")

minutes("m_hr", "minutes/Remuneration Committee Minutes Extract February 2026.pdf", "Remuneration Committee: Minutes Extract, 24 February 2026", "2026-02-24",
        "HR", "confidential", "hr;executive", """
Board Human Resources and Remuneration Committee. Extract of the minutes of 24 February 2026. Confidential. Not for circulation.

## Item 2: Director fees
The Committee recommended that the fee for each non-executive director be raised from UGX 2,800,000 to UGX 3,500,000 for each Board sitting, from 1 April 2026.

## Item 3: Executive bonus
The Committee approved a performance bonus equal to 4 months of basic salary for the Chief Executive Officer, based on the 2025 results.

## Item 4: Staff review
The Committee noted the 6.5 percent average salary increase given in July 2025 and asked for a market comparison before the next review.
""")

minutes("m_it", "minutes/IT Steering Committee Minutes Extract June 2026.txt", "IT Steering Committee: Minutes Extract, 9 June 2026", "2026-06-09",
        "IT", "internal", ALL, """
IT Steering Committee. Extract of the minutes of 9 June 2026.

Item 2: Multi-factor authentication. 1,420 of 1,800 staff have registered. Accounts without a registered device are locked. Staff who change phones must register the new phone by 30 November 2026.

Item 3: AI sandbox pilot. The Committee approved a pilot of an internal search over policy documents, limited to 120 documents and 40 users. The pilot will test whether the search shows staff only documents they are allowed to see. A budget of UGX 38,000,000 was approved for the pilot.

Item 4: Data catalogue. The Committee asked for a list of data sources with an owner for each. Fourteen sources were identified. None is yet in a catalogue.
""", fmt="txt")

minutes("m_exco", "minutes/Executive Committee Minutes Extract July 2026.pdf", "Executive Committee: Minutes Extract, 7 July 2026", "2026-07-07",
        "Company Secretary", "restricted", "executive", """
Executive Committee. Extract of the minutes of 7 July 2026.

## Item 1: Results for the second quarter
The Committee noted a claims ratio of 58 percent for Kitara Assurance, against a budget of 55 percent. Mobile wallet users grew to 412,000. Cost to income ratio for the Bank was 61 percent.

## Item 3: Staff survey
The staff survey showed that staff cannot find the current version of policies. 63 percent of respondents said they had once used an old policy by mistake.

## Item 4: Data and AI
The Committee agreed that a readiness assessment for AI use cases will be done before any AI project is funded.
""")

minutes("m_kenya", "minutes/Kitara Kenya Board Minutes Extract April 2026.pdf", "Kitara Kenya Board: Minutes Extract, 16 April 2026", "2026-04-16",
        "Company Secretary", "restricted", "executive;finance", """
Board of Kitara Kenya Limited. Extract of the minutes of 16 April 2026, held in Nairobi.

## Item 2: Capital expenditure
The Board approved KES 62 million for fitting out the Mombasa and Kisumu branches.

## Item 3: Staff
The Board approved the recruitment of 24 staff for the two new branches. Kenya staff keep 26 working days of annual leave under the Kenya supplement.

## Item 5: Regulatory notice
The Board noted the notice on customer complaints from the Kenya regulator and asked management to report complaint times each quarter.
""")

minutes("m_cx", "minutes/Customer Experience Forum Minutes Extract August 2026.txt", "Customer Experience Forum: Minutes Extract, 19 August 2026", "2026-08-19",
        "Customer Service", "internal", ALL, """
Customer Experience Forum. Extract of the minutes of 19 August 2026.

Item 1: Call centre. The average time to answer fell from 94 seconds in May to 71 seconds in July. The target in the Customer Charter is 60 seconds.

Item 2: Branch queues. Customers at Kampala Road branch waited an average of 22 minutes on Fridays. The branch will add a third teller on Fridays from September.

Item 3: Tariff in Swahili. The Forum agreed that Kitara Kenya will publish the tariff schedule in Swahili.
""", fmt="txt")

# ======================================================================= (h) REGULATORY NOTICE SUMMARIES (fictional)
def reg(tag, file, ref, title, date, body, sens="public", groups=ALL, **kw):
    doc(tag, file, f"Regulatory Notice {ref}: {title}", "regulatory_notice", ref, "current", date, "Legal and Compliance", sens, groups,
        FICT + "\n\n" + body, **kw)


reg("r_cash", "regulatory/Regulatory Notice UFSA 2025-03 Cash Reporting.pdf", "UFSA/2025/03", "Cash transaction reporting", "2025-02-17", """
Issued by the Uganda Financial Supervision Authority (UFSA), a fictional regulator. Summary for banks and mobile money providers.

From 1 April 2025 a regulated institution must report to the Authority every cash transaction of UGX 20,000,000 or more, or the foreign currency equivalent, within one working day. Institutions must keep the records for ten years. A failure to report is punished with a penalty of up to UGX 25,000,000 for each missed report.
""")

reg("r_claims", "regulatory/Regulatory Notice IRO 2025-01 Claims Settlement.pdf", "IRO/2025/01", "Time to settle insurance claims", "2025-01-13", """
Issued by the Insurance Regulatory Office (IRO), a fictional regulator. Summary for insurers.

An insurer must acknowledge a claim within seven days and must pay an accepted claim within 60 days of receiving the last document it asked for. An insurer that needs more than 60 days must tell the customer why in writing. A customer whose claim is not paid after 60 days may complain to the Office. Insurers report the average days to settle each quarter.
""")

reg("r_breach", "regulatory/Regulatory Notice PDPO 2025-02 Breach Notification.pdf", "PDPO/2025/02", "Personal data breach notification", "2025-03-03", """
Issued by the Personal Data Protection Office (PDPO), a fictional regulator. Summary for data controllers.

A controller must tell the Office within 72 hours of becoming aware of a personal data breach that is likely to harm the people affected. Where the risk is high the controller must also tell the people affected without delay. Every controller renews its registration with the Office by 31 January each year. A controller that processes personal data of more than 100,000 people must name a data protection officer.
""")

reg("r_agents", "regulatory/Regulatory Notice UFSA 2024-07 Mobile Money Agents.pdf", "UFSA/2024/07", "Mobile money agent identification", "2024-07-08", """
Issued by the Uganda Financial Supervision Authority (UFSA), a fictional regulator. Summary for mobile money providers.

A provider must make sure that every agent checks an original identity document before opening a wallet. A provider must be able to show, for any wallet, the date, the agent and the type of identity document used. Providers that cannot show this for at least 95 percent of new wallets in a quarter will be inspected.
""")

reg("r_kenya", "regulatory/Regulatory Notice CSAK 2026-01 Customer Complaints.pdf", "CSAK/2026/01", "Customer complaints in Kenya", "2026-01-19", """
Issued by the Central Supervisory Authority of Kenya (CSAK), a fictional regulator. Summary for banks and insurers licensed in Kenya.

A licensed institution must resolve a customer complaint within 30 days. It must keep a complaints register and send a quarterly complaints return to the Authority within 15 days after the end of each quarter. Institutions must publish the complaints procedure in English and in Swahili.
""")

reg("r_enforce", "regulatory/Regulatory Letter UFSA Late Returns Penalty.pdf", "UFSA/ENF/2026/02", "Penalty for late filing of returns", "2026-03-30", """
Letter from the Uganda Financial Supervision Authority (UFSA), a fictional regulator, to the Managing Director of Kitara Bank. Confidential: enforcement correspondence.

The Authority has found that the regulatory returns for the quarter ended 31 December 2025 were filed 9 days late and were corrected after submission. A penalty of UGX 12,000,000 is imposed. Kitara Bank must show within 60 days how it will make sure that customer data used in the returns is accurate and complete, and who is responsible for each return.
""", sens="confidential", groups="legal_compliance;executive")

# ======================================================================= (i) SCANNED DOCUMENTS (source texts, rendered to image later)
def scan(tag, file, title, family, version, status, eff, dept, sens, groups, body, personal="N", degrade="normal", lang="en", **kw):
    doc(tag, file, title, family, version, status, eff, dept, sens, groups, body, fmt="scanned_pdf", personal=personal, meta_note=degrade, **kw)


scan("s_claimform", "scans/Scan Motor Claim Form Signed.pdf", "Motor Claim Form (signed scan)", "claims_form", "1", "current", "2026-03-11", "Claims", "restricted", "claims", """
KITARA ASSURANCE LIMITED
MOTOR CLAIM FORM

Policy number: MP-2025-01874        Claim reference: CL-2026-0388
Name of insured: Ruth Nankya Kasozi
Customer ID: KT-0041872
National ID: KX482910554237
Phone: +256 700 051 944
Vehicle: Toyota Premio, registration UBM 417K
Date of loss: 8 March 2026       Place: Jinja Road, near Mukwano roundabout
Time of loss: about 7:40 pm

Description of loss
A taxi overtook on the left and hit the rear right door of my
car while I was stopped at the junction. The driver of the taxi
did not stop. I reported the matter at Kira Road police station
on 9 March 2026 (police report number OB 114/09/03/2026).

Damage estimate from garage: UGX 4,850,000
Documents attached: police report, driving permit, 4 photographs,
garage estimate.

I declare that the information above is true.

Signed: R. N. Kasozi                    Date: 11 March 2026

For office use: received by Claims Officer M. Atim on 11 March 2026.
""", personal="Y")

scan("s_circ2016", "scans/Scan Circular 2016-021 Annual Leave.pdf", "Circular 2016/021: Annual leave from 2017", "circular", "2016/021", "superseded", "2016-11-15", "HR", "internal", ALL, """
KITARA BANK LIMITED
STAFF CIRCULAR No. 2016/021
Date: 15 November 2016

To: All staff
From: Head of Human Resources
Subject: Annual leave entitlement from 1 January 2017

The Board has approved an increase in annual leave for all
permanent staff. From 1 January 2017 annual leave rises from
18 working days to 21 working days in each leave year.

Leave must still be approved by the line manager. Staff may
carry forward up to five days of unused leave into the next year.
Leave not taken by 31 March will lapse.

The medical cover for staff and one spouse is raised from
UGX 4,000,000 to UGX 5,000,000 a year from the same date.

Heads of Department should update their leave registers and tell
their staff before the end of November.

Signed: Head of Human Resources
""")

scan("s_inspect", "scans/Scan Branch Inspection Note Mbarara.pdf", "Branch Inspection Note: Mbarara Branch, 2024", "branch_note", "1", "current", "2024-08-22", "Branch Operations", "internal", "branch_ops;executive", """
KITARA BANK LIMITED - BRANCH OPERATIONS
INSPECTION NOTE: MBARARA BRANCH
Date of visit: 22 August 2024
Inspector: Operations Auditor, Branch Operations

Findings
1. The vault log was not signed on three days in July (4, 11 and 26).
2. The fire extinguisher near the vault expired in May 2024.
3. Cash held by one teller reached UGX 19,500,000 on 15 August,
   above the limit of UGX 15,000,000.
4. Customer files for 14 closed accounts were found in an
   unlocked cupboard in the back office.
5. The branch complaints register was up to date.

Actions agreed
The Branch Manager will replace the extinguisher by 31 August,
lock the cupboard and move the 14 files to the records room,
and retrain all tellers on the cash limit by 15 September 2024.

Next visit: November 2024.
""")

scan("s_posted", "scans/Scan Customer Complaint Letter by Post.pdf", "Customer complaint letter received by post", "claims_letter", "1", "current", "2026-05-06", "Customer Service", "restricted", "claims;legal_compliance", """
Mr Robert Ochieng Wafula
P. O. Box 2214, Mbale
Phone: +256 700 063 281

6 May 2026

The Manager
Kitara Bank, Mbale Branch

Dear Sir,

COMPLAINT ABOUT SCHOOL FEES LOAN SF-2026-3319

On 20 January 2026 I took a school fees loan of UGX 2,400,000
for my daughter at Mbale Girls Secondary School. The school
received only UGX 2,350,000. My statement shows that you took
a fee of UGX 50,000 that nobody told me about.

I am asking for an explanation and a refund. I have been to the
branch twice and was told to come back. My customer number is
KT-0077315.

Yours faithfully,
Robert Ochieng Wafula
""", personal="Y")

scan("s_board2019", "scans/Scan Board Resolution Extract 2019.pdf", "Board resolution extract, 2019", "minutes", "2019", "superseded", "2019-09-18", "Company Secretary", "confidential", "executive;legal_compliance", """
KITARA GROUP BOARD OF DIRECTORS
EXTRACT FROM THE RESOLUTIONS OF 18 SEPTEMBER 2019
CONFIDENTIAL

Resolution 4/2019. IT IS RESOLVED that the Group will
open a subsidiary company in Nairobi, Kenya, to be called
Kitara Kenya Limited, with an initial paid up capital of
KES 450,000,000.

Resolution 5/2019. IT IS RESOLVED that Mr J. Byaruhanga
is appointed Managing Director of Kitara Kenya Limited
for an initial term of three years.

Resolution 6/2019. IT IS RESOLVED that the Group will
adopt the Staff Handbook 2019 with effect from 1 January
2019 and that the Head of Human Resources will report on
its use each year.

Certified true copy. Company Secretary.
""")

scan("s_loannote", "scans/Scan Loan Committee Note 2018.pdf", "Loan committee approval note, 2018", "branch_note", "1", "superseded", "2018-04-10", "Risk", "restricted", "risk;branch_ops;executive", """
KITARA BANK LIMITED
REGIONAL CREDIT COMMITTEE: GULU
NOTE OF DECISION, 10 April 2018

Application: working capital loan, Gulu Market Traders Group
Amount requested: UGX 35,000,000
Amount approved: UGX 28,000,000
Tenor: 24 months     Interest: 24 percent a year, reducing balance

Conditions
1. Six months of group savings statements to be attached.
2. Collateral: title deed for plot 14, Cemetery Road, valued
   at UGX 40,000,000.
3. Three signatories to confirm the repayment plan in writing.

Members present: Regional Credit Manager, Branch Manager Gulu,
Senior Loan Officer.

Approved by the Regional Credit Committee within its limit of
UGX 30,000,000 at that date.
""", degrade="heavy")

scan("s_fax2017", "scans/Scan Regulator Notice Fax 2017.pdf", "Regulator notice received by fax, 2017", "regulatory_notice", "UFSA/2017/11", "superseded", "2017-06-02", "Legal and Compliance", "internal", ALL, """
FAX  FICTIONAL NOTICE FOR TRAINING USE
FROM: Uganda Financial Supervision Authority (fictional)
TO: Managing Director, Kitara Bank
DATE: 2 June 2017      PAGES: 1

NOTICE UFSA/2017/11: RETURN OF BRANCH LISTS

All banks must file an updated list of branches and
agents with the Authority by 30 June 2017. The list must
show the physical address of each branch, the name of
the manager and the opening hours.

A bank that has not filed by 30 June 2017 will pay a
penalty of UGX 1,000,000 for each week of delay.

This notice replaces notice UFSA/2014/03.
""", degrade="heavy")

scan("s_policy2015", "scans/Scan Motor Policy Schedule 2015.pdf", "Motor policy schedule, 2015", "policy_schedule", "1", "superseded", "2015-03-20", "Underwriting", "restricted", "underwriting;claims", """
KITARA INSURANCE LIMITED
MOTOR POLICY SCHEDULE
Policy No: MP-2015-00531
Period of insurance: 20 March 2015 to 19 March 2016
Insured: Fictional Haulage Company Ltd
Vehicle: Isuzu truck, registration UAB 220C
Class of use: Commercial goods carrying
Sum insured: UGX 62,000,000
Cover: Comprehensive
Premium: UGX 3,100,000     Stamp duty: UGX 35,000
Excess: 10 percent of each claim, minimum UGX 150,000

Special conditions
1. Cover applies only within Uganda, Kenya and Rwanda.
2. The vehicle must be fitted with a working tracking device.
3. Claims must be reported within 48 hours of the loss.
""", degrade="heavy")
