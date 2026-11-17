"""Kitara document corpus, part A: handbooks, claims SOPs, policies, product guides, procedures.

Every document is a dict made by doc(). Body markup: blank line between paragraphs, '## ' heading, '- ' bullet.
All content is fictional. Kitara Group, its staff, customers and regulators do not exist.
"""
DOCS = []
ALL = "all_staff"


def doc(tag, file, title, family, version, status, eff, dept, sens, groups, body, fmt="text_pdf", lang="en", personal="N",
        hf=True, cols=1, table=None, table_mode=None, meta_note=""):
    DOCS.append(dict(tag=tag, file=file, title=title, family=family, version=version, status=status, effective_date=eff,
                     owner_department=dept, sensitivity=sens, access_groups=groups, language=lang, format=fmt,
                     contains_personal_data=personal, body=body.strip(), hf=hf, cols=cols, table=table,
                     table_mode=table_mode, meta_note=meta_note))


# ======================================================================= (a) STAFF HANDBOOK, three versions
doc("hb2019", "policies/Staff Handbook 2019.docx", "Kitara Group Staff Handbook 2019", "staff_handbook", "2019", "superseded",
    "2019-01-01", "HR", "internal", ALL, """
Kitara Group Staff Handbook, 2019 edition

## 1. Working hours
Normal working hours are 8:00 am to 5:00 pm, Monday to Friday, with a one-hour lunch break. Branch staff also work a Saturday roster from 9:00 am to 1:00 pm.

## 2. Probation
Every new permanent employee serves a probation period of six months. The line manager reviews performance at the end of the third month and again at the end of the sixth month. Confirmation is in writing from Human Resources.

## 3. Annual leave
Every member of staff is entitled to 21 working days of annual leave in each leave year. Annual leave is approved by the line manager. Up to five days of unused annual leave may be carried forward to the next year.

## 4. Other leave
Maternity leave is 60 working days on full pay. Paternity leave is four working days. Sick leave is up to 30 working days in a year on full pay, with a medical certificate for any absence longer than two days.

## 5. Place of work
Staff are expected to work from their assigned office or branch. Working from home is not allowed, except in an emergency and with the written approval of the Head of Department.

## 6. Expenses
A member of staff may not claim a single expense above UGX 200,000 without the written approval of the Head of Department before the cost is incurred. A receipt is needed for every claim above UGX 10,000.

## 7. Gifts
Gifts worth more than UGX 50,000 offered by customers or suppliers must be declared to Human Resources within seven days.

## 8. Notice and medical cover
Staff give one month of notice. Managers give three months. The group medical scheme pays inpatient costs up to UGX 6,000,000 per person per year.
""", fmt="docx")

doc("hb2022", "policies/Staff Handbook 2022.docx", "Kitara Group Staff Handbook 2022", "staff_handbook", "2022", "superseded",
    "2022-03-01", "HR", "internal", ALL, """
Kitara Group Staff Handbook, 2022 edition

## 1. Working hours
Normal working hours are 8:00 am to 5:00 pm, Monday to Friday, with a one-hour lunch break. Branch staff also work a Saturday roster from 9:00 am to 1:00 pm.

## 2. Probation
New permanent employees serve a probation period of four months. The line manager reviews performance at the end of the second month and at the end of the fourth month.

## 3. Annual leave
Staff earn 24 working days of annual leave in each leave year. Up to eight days of unused leave may be carried forward until 31 March of the next year. Leave requests go through the HR portal.

## 4. Other leave
Maternity leave is 60 working days on full pay. Paternity leave is four working days. Sick leave is up to 30 working days in a year on full pay.

## 5. Remote work
Since the 2020 lockdown many head office roles have worked from home. Staff in head office departments may work remotely for up to two days a week with the approval of the line manager. Branch staff must be at the branch. This arrangement will be reviewed in 2024.

## 6. Expenses
A single expense claim above UGX 350,000 needs the written approval of the Head of Department before the cost is incurred. A receipt is needed for every claim above UGX 15,000.

## 7. Gifts
Gifts worth more than UGX 80,000 must be declared to Human Resources.

## 8. Notice and medical cover
Staff give one month of notice. Managers give three months. The group medical scheme pays inpatient costs up to UGX 10,000,000 per person per year.
""", fmt="docx")

doc("hb2025", "policies/Staff Handbook 2025.pdf", "Kitara Group Staff Handbook 2025", "staff_handbook", "2025", "current",
    "2025-07-01", "HR", "internal", ALL, """
This handbook applies to all employees of Kitara Bank, Kitara Assurance and the head office of Kitara Group from 1 July 2025. Kitara Kenya staff follow their local supplement where Kenyan law requires a different rule.

## 1. Working hours
Normal working hours are 8:00 am to 5:00 pm, Monday to Friday, with a one-hour lunch break. Branch staff also work a Saturday roster from 9:00 am to 1:00 pm and take a day off in lieu during the following week.

## 2. Probation
New permanent employees serve a probation period of three months. Probation may be extended once, in writing, by no more than three months. A manager who wants to extend probation must tell Human Resources before the end of the third month.

## 3. Annual leave
Staff earn 28 working days of annual leave in each leave year, which runs from 1 January to 31 December. Up to 10 days of unused leave may be carried forward until 31 March of the next year. Leave beyond that date lapses unless the Head of Human Resources agrees otherwise.

## 4. Other leave
Maternity leave is 60 working days on full pay. Paternity leave is seven working days. Sick leave is up to 45 working days in a year on full pay. A medical certificate is needed for any absence longer than two days.

## 5. Remote work
Staff in head office roles may work remotely for up to three days a week with the written approval of the line manager. Branch, teller and agent-support roles are not eligible. The Remote Work Policy sets out the equipment and security rules.

## 6. Expenses
A single expense claim above UGX 500,000 needs the written approval of the Head of Department before the cost is incurred. A receipt is needed for every claim above UGX 20,000. See the Expense Policy for daily limits.

## 7. Gifts and conflicts of interest
Gifts worth more than UGX 100,000 must be declared to Human Resources within seven days. Staff must declare any financial interest in a supplier or borrower.

## 8. Notice and medical cover
Staff give one month of notice. Managers give three months. The group medical scheme pays inpatient costs up to UGX 15,000,000 per person per year.

## 9. Grievances
A grievance is raised first with the line manager. If it is not settled within 14 days the staff member may write to the Head of Human Resources, who replies within 14 days.
""", hf=True)

doc("hb2025_salary", "policies/Staff Handbook 2025 Appendix B Salary Bands.pdf", "Staff Handbook 2025, Appendix B: Salary Bands",
    "staff_handbook", "2025", "current", "2025-07-01", "HR", "confidential", "hr;executive", """
Appendix B to the Staff Handbook 2025. Confidential to Human Resources and the Executive Committee. Do not forward.

Monthly gross salary bands in UGX, effective 1 July 2025. Placement within a band depends on experience and the annual appraisal.

- Grade G1 (clerk, teller trainee): 650,000 to 900,000
- Grade G2 (teller, customer service agent): 900,000 to 1,300,000
- Grade G3 (loan officer, claims officer): 1,300,000 to 2,100,000
- Grade G4 (senior officer, underwriter): 2,100,000 to 3,400,000
- Grade G5 (branch manager, senior claims officer): 3,400,000 to 5,200,000
- Grade G6 (head of unit): 5,200,000 to 8,000,000
- Grade G7 (head of department): 8,000,000 to 12,500,000
- Grade G8 (general manager): 12,500,000 to 18,000,000

The 2025 salary review gave an average increase of 6.5 percent from 1 July 2025. Staff in grades G1 and G2 received a minimum increase of UGX 60,000. A staff member who thinks they are placed in the wrong band writes to the Head of Human Resources.
""")

# ======================================================================= (b) CLAIMS HANDLING SOP
doc("sop3", "policies/Claims Handling SOP v3.pdf", "Claims Handling SOP, Version 3", "claims_sop", "3", "superseded",
    "2021-06-01", "Claims", "internal", "claims;underwriting;legal_compliance;executive", """
Kitara Assurance, Claims Department. Standard operating procedure for general insurance claims.

## 1. Acknowledgement
Every claim notification is acknowledged in writing within five working days. The claims officer opens the file in the claims system and records the policy number and the date of loss.

## 2. Documents
For a motor claim the customer provides the claim form, a copy of the police report, the driving permit and photographs of the damage. For a home claim the customer provides the claim form and an inventory of the items lost. The claim is complete when the last required document is received.

## 3. Assessment
A loss adjuster is appointed for any claim above UGX 3,000,000. The adjuster reports within ten working days.

## 4. Settlement timeframe
Kitara settles an accepted claim within 45 calendar days of receiving the last required document. The settlement timeframe for an accepted claim runs from the day the last required document is received. Payment is made by bank transfer or cheque.

## 5. Approval limits
A claim is approved by an officer whose approval limit covers the claim amount. The approval limit of a Claims Officer and of each higher level is:
- Claims Officer: up to UGX 5,000,000
- Senior Claims Officer: up to UGX 20,000,000
- Head of Claims: up to UGX 60,000,000
- Claims Committee: above UGX 60,000,000

## 6. Fraud indicators
A claim with two or more fraud indicators is referred to the Special Investigations Unit before any payment.

## 7. Repudiation
A claim that is declined is declined in writing, with the reason.

Version 3, June 2021. Superseded by Version 4 from 1 March 2025.
""")

doc("sop4", "policies/Claims Handling SOP v4.pdf", "Claims Handling SOP, Version 4", "claims_sop", "4", "current",
    "2025-03-01", "Claims", "internal", "claims;underwriting;legal_compliance;executive", """
Kitara Assurance, Claims Department. Standard operating procedure for general insurance claims. This version replaces Version 3.

## 1. Acknowledgement
Every claim notification is acknowledged within 48 hours, by SMS and by letter or email. The claims officer opens the file in the claims system and records the policy number, the date of loss and the customer phone number.

## 2. Documents
For a motor claim the customer provides the claim form, a copy of the police report, the driving permit and photographs of the damage. For a home claim the customer provides the claim form and an inventory of the items lost. The claim is complete when the last required document is received. The claims officer lists missing documents in one message, not several.

## 3. Assessment
A loss adjuster is appointed within three working days for any claim above UGX 3,000,000. The adjuster reports within seven working days.

## 4. Settlement timeframe
Kitara settles an accepted claim within 30 calendar days of receiving the last required document. Payment is made by bank transfer only. Cheques are no longer issued for claims.

## 5. Approval limits
- Claims Officer: up to UGX 8,000,000
- Senior Claims Officer: up to UGX 30,000,000
- Head of Claims: up to UGX 100,000,000
- Claims Committee: above UGX 100,000,000

## 6. Fraud indicators
A claim with two or more fraud indicators is referred to the Special Investigations Unit before any payment. The customer is told only that the claim is under review.

## 7. Repudiation
A claim that is declined is declined in writing. The letter gives the policy clause relied on and tells the customer how to complain and that the matter can go to the insurance regulator after 30 days.

## 8. Records
The claim file is kept for seven years after settlement. Life claim files are kept for 15 years.
""")

# ======================================================================= (c) CORE POLICIES AND PROCEDURES
doc("loan", "policies/Loan Approval Policy.pdf", "Loan Approval Policy", "policy", "2025", "current", "2025-01-01",
    "Risk", "restricted", "branch_ops;risk;finance;executive", """
Kitara Bank, Credit Risk. This policy sets who may approve a loan and on what conditions.

## 1. Approval authority
- Loan Officer: up to UGX 10,000,000
- Branch Manager: up to UGX 50,000,000
- Regional Credit Committee: up to UGX 250,000,000
- Head Office Credit Committee: above UGX 250,000,000 and up to UGX 1,000,000,000. It meets on the second Tuesday of every month.
- Board Credit Committee: above UGX 1,000,000,000

No officer approves a loan to a relative, a business partner or a company in which they hold shares.

## 2. Lending conditions
- The monthly repayment may not exceed 40 percent of the borrower's net monthly income.
- A secured loan needs collateral worth at least 125 percent of the loan amount, valued by an approved valuer.
- The maximum tenor for an SME loan is 60 months. The maximum tenor for a school fees loan is 12 months.
- The borrower must have held an account with Kitara for at least six months, except for a school fees loan to a salaried customer whose employer pays into Kitara.

## 3. Credit checks
Every application is checked against the credit reference bureau. A borrower with a loan more than 30 days overdue elsewhere is declined unless the Head of Credit approves an exception in writing.

## 4. Documents
The file holds the signed application, identification verified under the KYC Procedure, three months of statements, the valuation report and the credit memo.
""")

doc("kyc", "policies/KYC Procedure.pdf", "Know Your Customer (KYC) Procedure", "policy", "2024", "current", "2024-09-01",
    "Legal and Compliance", "internal", ALL, """
This procedure applies to every branch and agent that opens an account for a new customer.

## 1. Identification
A new customer shows one original photo identification: a national identity card, a valid passport or a refugee identity card. A driving permit is accepted only for opening a Mobile Wallet. It is not accepted for savings or current accounts. The officer records the identity number, checks the photograph against the customer and scans the document.

## 2. Proof of address
The customer provides a utility bill, a tenancy agreement or a letter from the Local Council chairperson. The document must not be older than three months.

## 3. Politically exposed persons
An account for a politically exposed person, or a close family member, needs the written approval of the Head of Compliance before it is opened. These accounts are treated as high risk.

## 4. Customer information refresh
Customer details are refreshed every two years. For high risk customers the refresh is every year. A branch that cannot reach the customer after two attempts flags the account for restricted use.

## 5. Enhanced checks
Enhanced checks apply when a customer deposits cash above UGX 20,000,000 in one day, when the customer lives outside Uganda or Kenya, and when the source of funds is unclear.

## 6. Records
Identification copies are kept for ten years after the account is closed.
""")

doc("retention", "policies/Data Retention Schedule.pdf", "Data Retention Schedule", "policy", "2024", "current", "2024-04-01",
    "Legal and Compliance", "internal", ALL, """
Kitara Group keeps records for the periods below. After the period ends the record is destroyed unless Legal and Compliance has placed a hold on it. The periods follow the Data Protection and Privacy Act, 2019 and the sector rules.

## Schedule
- Customer account records: 10 years after the account is closed
- Loan files: seven years after the final repayment
- Claims files, general insurance: seven years after settlement
- Claims files, life insurance: 15 years after settlement
- Suspicious transaction reports and supporting records: 10 years
- Mobile money transaction logs: 10 years
- Staff personnel files: seven years after the employee leaves
- Recruitment records of unsuccessful candidates: 12 months
- Call centre recordings: 24 months
- CCTV footage in branches: 90 days
- Email: five years
- Board and committee minutes: permanent

## Responsibilities
Each head of department names a records owner. The records owner signs the annual destruction list. IT removes backups on the same schedule. A customer who asks for deletion of personal data is told which records must be kept by law and for how long.
""")

doc("infosec", "policies/Information Security Policy.pdf", "Information Security Policy", "policy", "2025", "current", "2025-02-01",
    "IT", "internal", ALL, """
This policy applies to all staff, contractors and agents who use Kitara systems.

## 1. Passwords and access
Passwords have at least 12 characters. Multi-factor authentication is required for email, remote access and every system that holds customer data. A leaver's access is removed within 24 hours of the last working day. Access rights are reviewed every quarter by the system owner.

## 2. Devices
Laptops are encrypted. USB storage ports are disabled except with written approval from IT Security. A lost or stolen device must be reported to the IT service desk within two hours.

## 3. Data classification
Information is public, internal, restricted or confidential. Confidential information, such as salary data, national identity numbers and investigation files, is shared only with named people.

## 4. Incidents
A suspected security incident is reported to IT Security within one hour. IT Security tells the Head of Legal and Compliance within four hours if personal data may be affected. A breach of personal data is reported to the Data Protection Office within 72 hours.

## 5. Email and the internet
Staff do not send customer data to personal email addresses. Staff do not paste customer data into public websites or public AI tools.

## 6. Suppliers
A supplier that handles Kitara data signs the data processing schedule before work starts.
""")

doc("complaints", "policies/Complaints Handling Procedure.pdf", "Complaints Handling Procedure", "policy", "2024", "current", "2024-11-01",
    "Customer Service", "internal", ALL, """
A complaint is any expression of dissatisfaction about a Kitara product, service or member of staff. A request for information is an enquiry and is not logged as a complaint.

## 1. Receiving a complaint
A complaint may be made at any branch, by phone, by email or through the mobile app. The person who receives it records it in the complaints register on the same day. The customer receives a reference number.

## 2. Acknowledgement
Every complaint is acknowledged within 24 hours. The acknowledgement gives the reference number and the name of the officer handling the complaint.

## 3. Resolution
A simple complaint is resolved within 14 days. A complex complaint, such as a disputed claim decision or a disputed loan balance, is resolved within 30 days. If more time is needed the customer is told why and given a new date.

## 4. Escalation
A customer who is not satisfied can ask the Head of Customer Service to review the decision. If the complaint is not resolved after 30 days the customer may take it to the sector regulator. Staff must give the customer the regulator's contact details when asked.

## 5. Reporting
Customer Service sends the monthly complaints report to the Risk Committee. The report lists complaints by product, by branch and by days to resolve.
""")

doc("aml", "policies/Anti-Money-Laundering Summary.pdf", "Anti-Money-Laundering Policy: Summary", "policy", "2025", "current", "2025-05-01",
    "Legal and Compliance", "restricted", "legal_compliance;branch_ops;risk;executive", """
Summary for branch managers and compliance officers. The full policy is held by the Money Laundering Reporting Officer (MLRO).

## 1. Cash transaction reports
A cash deposit or withdrawal of UGX 20,000,000 or more, or the equivalent in foreign currency, in one day is reported to the MLRO by the end of the next working day.

## 2. Suspicious transactions
Any member of staff who suspects money laundering reports it to the MLRO within 24 hours using the internal suspicion form. The MLRO decides whether to file a report with the Financial Intelligence Authority. Staff must not tell the customer that a report has been made.

## 3. Customer risk rating
Every customer is rated low, medium or high at account opening and again at each information refresh. High risk customers include politically exposed persons and cash-intensive businesses.

## 4. Mobile money agents
An agent who handles more than UGX 30,000,000 of float in a day is monitored weekly. Agents who split large transactions into small ones to avoid reports are suspended.

## 5. Training and records
Every employee completes AML training once a year. Reports and supporting records are kept for 10 years.
""")

doc("remote", "policies/Remote Work Policy.docx", "Remote Work Policy", "policy", "2025", "current", "2025-07-01",
    "HR", "internal", ALL, """
Remote Work Policy

## Who may work remotely
Staff in head office roles may work remotely up to three days a week with the written approval of the line manager. Branch, teller and agent-support roles are not eligible. Approval is reviewed every six months.

## Availability
A remote worker is reachable between 9:00 am and 3:00 pm on remote days and attends team meetings by video when asked.

## Security
- Work only on a Kitara laptop with the VPN switched on and multi-factor authentication.
- Do not work on customer files in a cafe, hotel lobby or any public place.
- Do not print customer documents at home.

## Support
Approved remote workers receive an internet allowance of UGX 80,000 per month. IT supplies one laptop and one headset. A remote worker who loses the connection for more than one working day tells the line manager and works from the office.
""", fmt="docx")

doc("expense", "policies/Expense Policy.docx", "Expense Policy", "policy", "2025", "current", "2025-07-01",
    "Finance", "internal", ALL, """
Expense Policy

## Approval limits
A single expense claim above UGX 500,000 needs the written approval of the Head of Department before the cost is incurred. Claims above UGX 5,000,000 also need the approval of the Chief Finance Officer.

## Daily limits for official travel
- Meals and incidentals: UGX 80,000 per day in Kampala and UGX 100,000 per day in other towns
- Hotel: UGX 350,000 per night, bed and breakfast included
- Mileage for a private vehicle used on official business: UGX 2,200 per kilometre

## Receipts and timing
A receipt is needed for every item above UGX 20,000. Claims are submitted within 30 days of the expense. Claims older than 90 days are not paid.

## Not reimbursed
Alcohol, fines, personal phone credit and any item bought for a private purpose.
""", fmt="docx")

doc("whistle", "policies/Whistleblowing Policy.docx", "Whistleblowing Policy", "policy", "2023", "current", "2023-10-01",
    "Legal and Compliance", "internal", ALL, """
Whistleblowing Policy

## What to report
Fraud, bribery, theft, falsified records, harassment, breaches of the law or of Kitara policy, and any danger to customers or staff.

## How to report
Report to the Head of Internal Audit, to the Head of Legal and Compliance, or through the Speak-Up line. The Speak-Up line is an external service that takes calls in English, Luganda and Swahili. Reports can be anonymous. The email address is speakup@kitaragroup.example.

## What happens next
Internal Audit confirms receipt within two working days and starts the review within seven working days. The reporter is told the outcome within 60 days if their identity is known.

## Protection
A person who reports in good faith is protected against dismissal, demotion and harassment. A manager who retaliates faces disciplinary action. A report made in bad faith, knowing it to be false, is a disciplinary matter.
""", fmt="docx")

doc("bcp", "policies/Business Continuity Plan Summary.pdf", "Business Continuity Plan: Summary", "policy", "2025", "current", "2025-08-01",
    "Risk", "internal", ALL, """
Summary of the Kitara Group Business Continuity Plan for all staff.

## Recovery targets
- Core banking system: restored within four hours. Data loss no more than 15 minutes.
- Mobile money switch: restored within two hours.
- Claims system: restored within 24 hours.
- Email and the shared drive: restored within eight hours.

## Recovery site
The disaster recovery site is at the Mukono data centre. Data is copied there every 15 minutes. A full recovery test is held every year in March.

## If your branch cannot open
The Branch Manager phones the Branch Operations duty officer within 30 minutes. Customers are directed to the nearest open branch. Tellers carry cash to the alternative branch only with a security escort.

## Staff contact tree
Each head of department keeps a printed contact tree. In a major incident the Chief Operating Officer leads the Crisis Team, which meets at 8:00 am and 2:00 pm each day until normal service returns.
""")

# ======================================================================= (d) PRODUCT GUIDES
doc("g_motor", "product guides/Motor Insurance Guide.pdf", "Motor Insurance Product Guide", "product_guide", "2025", "current", "2025-01-01",
    "Underwriting", "public", ALL, """
Kitara Assurance motor insurance for private cars, pickups and commercial vehicles.

## Covers
- Third party only: covers injury to other people and damage to their property.
- Comprehensive: third party cover plus damage to your own vehicle, fire and theft.

## Premium
The comprehensive premium is 4.5 percent of the sum insured, with a minimum of UGX 350,000 a year. Third party only is UGX 220,000 a year for a private car. A no-claim discount of 10 percent applies after one claim-free year, rising to 30 percent after three.

## Excess
The customer pays an excess of 10 percent of each claim, with a minimum of UGX 200,000. The excess for a driver under 23 is 15 percent.

## Not covered
Driving without a valid permit, driving under the influence of alcohol, racing, and use of a private car for hire without cover for hire.

## Making a claim
Call 0800 100 200 or tell your branch within 24 hours of an accident. Keep the police report. We acknowledge every claim within 48 hours.
""")

doc("g_home", "product guides/Home Insurance Guide.pdf", "Home Insurance Product Guide", "product_guide", "2025", "current", "2025-01-01",
    "Underwriting", "public", ALL, """
Kitara Assurance home insurance for houses, flats and household contents.

## Covers
Fire, lightning, explosion, storm, flood, burglary and malicious damage to the building and the contents. Contents cover includes electronics, furniture and clothing.

## Premium
The premium for buildings cover is 0.25 percent of the sum insured each year. Contents cover is 0.6 percent of the sum insured. The minimum premium is UGX 120,000 a year.

## Sum insured
Insure the building for the cost of rebuilding it, not the market price of the land and house. Contents are insured for replacement value. Items worth more than UGX 3,000,000, such as jewellery, must be listed separately.

## Waiting period
Cover for flood starts 14 days after the policy begins.

## Exclusions
War, wear and tear, damage caused by pests, and loss when the house has been empty for more than 60 days.
""")

doc("g_life", "product guides/Life Insurance Guide.pdf", "Life Insurance Product Guide", "product_guide", "2025", "current", "2025-01-01",
    "Underwriting", "public", ALL, """
Kitara Assurance term life insurance pays a lump sum to your family if you die during the term.

## Cover
Cover starts at UGX 10,000,000 and goes up to UGX 500,000,000. Terms run from 5 to 25 years. Cover above UGX 100,000,000 needs a medical examination.

## Waiting periods
Death from an accident is covered from the first day. Death from illness is covered after a waiting period of six months. A pre-existing condition that was not declared when you applied can lead to the claim being declined.

## Premium
The premium depends on age, smoking and health. As an example, a healthy non-smoker aged 35 pays about UGX 48,000 a month for UGX 100,000,000 of cover over 20 years.

## Claims
The family needs the policy number, a certified death certificate, the identity card of the person who died and the identity cards of the beneficiaries. We settle a valid claim within 30 days of receiving the last document. Life claims are paid to the named beneficiaries, not to the estate.

## Grace period
A missed premium may be paid within 30 days without losing cover.
""")

doc("g_sme", "product guides/SME Loan Guide.pdf", "SME Loan Product Guide", "product_guide", "2025", "current", "2025-01-01",
    "SME Lending", "public", ALL, """
Kitara Bank SME Loan for registered and unregistered small businesses.

## Amount and tenor
Loans from UGX 2,000,000 up to UGX 150,000,000. Repayment over 6 to 60 months.

## Cost
The interest rate is 19 percent a year on the reducing balance. The processing fee is 1.5 percent of the loan, paid at disbursement. Insurance on the loan is 0.5 percent of the loan, paid once.

## What you need
A business that has traded for at least 12 months, six months of bank or mobile money statements, a valid trading licence for businesses above UGX 20,000,000, and collateral worth at least 125 percent of the loan.

## Decision time
Loans up to UGX 10,000,000 are decided within three working days of a complete application. Larger loans take up to 10 working days.

## Early repayment
You may repay early. There is no penalty after the first six months. Before that a fee of 2 percent of the amount repaid applies.
""")

doc("g_mortgage", "product guides/Mortgage Guide.pdf", "Mortgage Product Guide", "product_guide", "2025", "current", "2025-01-01",
    "Retail Banking", "public", ALL, """
Kitara Bank mortgage for buying or building a home in Uganda.

## Amount and tenor
We lend up to 80 percent of the valuation, so the customer pays a deposit of at least 20 percent. The loan runs for up to 20 years. The maximum amount is UGX 800,000,000.

## Cost
The interest rate is 16.5 percent a year, variable. The rate may change when the Kitara base rate changes, and we write to you one month before. The arrangement fee is 1 percent of the loan. Valuation and legal fees are paid by the customer.

## Requirements
Land title in the name of the seller or the buyer, a sale agreement, three months of payslips or six months of business statements, and life cover on the borrower for the length of the loan.

## Repayment
The repayment may not be more than 40 percent of net monthly income. Salaried customers repay by standing order from their Kitara account.
""")

doc("g_fees", "product guides/School Fees Loan Guide.pdf", "School Fees Loan Product Guide", "product_guide", "2025", "current", "2025-01-01",
    "Retail Banking", "public", ALL, """
Kitara Bank School Fees Loan helps parents and guardians pay fees at the start of term.

## Amount and tenor
Loans from UGX 500,000 up to UGX 15,000,000. Repayment is over up to 12 months. Many parents choose three instalments, one for each term.

## Cost
The interest rate is 18 percent a year on the reducing balance. The processing fee is 1 percent of the loan.

## Who can apply
Salaried customers whose employer pays into a Kitara account, and customers who have held a Kitara savings account for at least six months. The borrower must be a parent or legal guardian of the pupil.

## How the money is paid
We pay the money directly to the school account, not to the borrower. The school confirms the pupil's admission and the fee amount in writing. The money is sent within two working days of approval.

## Timing
Apply at least two weeks before the term starts. Applications in the first week of term are processed, but the school may charge a late fee.
""")

doc("g_group", "product guides/Savings Group Account Guide.pdf", "Savings Group Account Product Guide", "product_guide", "2025", "current", "2025-01-01",
    "Retail Banking", "public", ALL, """
The Kitara Savings Group Account is for village savings and credit groups, burial societies and cooperative groups.

## Who can open one
A group of 10 to 30 members that has met regularly for at least three months. The group provides its constitution, the minutes of the meeting that elected the signatories, and the identity cards of the signatories.

## Signatories
The account has three signatories. Any withdrawal needs two of the three signatories. The group chairperson cannot be the only signatory on a withdrawal.

## Cost and interest
There is no monthly fee. The minimum opening balance is UGX 50,000. Interest is 6 percent a year, paid every six months at the end of June and December.

## Share-out
The group may withdraw its whole balance for the annual share-out with five working days of notice, and without a fee.

## Loans to members
Kitara does not lend to individual group members through this account. Members who want a loan apply separately.
""")

doc("g_wallet", "product guides/Mobile Wallet Guide.pdf", "Kitara Mobile Wallet Guide", "product_guide", "2025", "current", "2025-01-01",
    "Retail Banking", "public", ALL, """
The Kitara Mobile Wallet lets you hold money on your phone, send it, pay bills and cash out at any Kitara agent.

## Opening a wallet
Open a wallet at a branch or an agent with your national identity card, passport or driving permit. Your phone number must be registered in your own name.

## Limits
The most you can hold in the wallet is UGX 10,000,000. The most you can send or withdraw in one day is UGX 5,000,000. Limits for new wallets in the first 30 days are half of these.

## Fees
Sending to another Kitara wallet is free. Sending to your Kitara bank account is free. Cash out at an agent is charged by amount, as shown in the Tariff Schedule.

## Lost phone or forgotten PIN
Call 0800 100 200 straight away and we will block the wallet. A PIN can be reset only at a branch, with your original identity card. Agents cannot reset a PIN.

## Dormancy
A wallet with no customer transaction for 12 months is marked dormant.
""")

doc("t_tariff", "product guides/Tariff Schedule 2025.pdf", "Kitara Bank Tariff Schedule 2025", "product_guide", "2025", "current", "2025-01-01",
    "Retail Banking", "public", ALL, """
Kitara Bank tariff of charges, effective 1 January 2025. Amounts in UGX. The table on this page shows the main retail charges. Value added tax is extra where it applies.
""", table=[["Service", "Charge (UGX)", "Notes"],
            ["Savings account monthly fee", "0", "Minimum balance UGX 20,000"],
            ["Current account monthly fee", "15,000", "Per month"],
            ["Cash withdrawal at branch", "2,500", "Per withdrawal"],
            ["Wallet cash out up to 50,000", "900", "Agent"],
            ["Wallet cash out 50,001 to 500,000", "2,400", "Agent"],
            ["Wallet cash out above 500,000", "5,500", "Agent"],
            ["Statement, printed", "5,000", "Per statement"],
            ["Cheque book, 50 leaves", "30,000", "Per book"]], table_mode="columnwise")

doc("t_motorrates", "product guides/Motor Premium Rates 2025.pdf", "Motor Premium Rates 2025", "product_guide", "2025", "current", "2025-01-01",
    "Underwriting", "internal", "underwriting;branch_ops;executive", """
Motor premium rates for 2025. The table shows the annual premium as a percentage of the sum insured, by vehicle class, and the minimum premium in UGX. Agents use the table at quotation.
""", table=[["Vehicle class", "Rate on sum insured", "Minimum premium"],
            ["Private car comprehensive", "4.5%", "350,000"],
            ["Pickup and van comprehensive", "5.0%", "420,000"],
            ["Commercial truck comprehensive", "5.8%", "900,000"],
            ["Motorcycle taxi", "6.5%", "180,000"],
            ["Bus and minibus", "6.0%", "1,200,000"],
            ["Private car third party only", "flat", "220,000"]], table_mode="columnwise")

# ======================================================================= OTHER POLICIES AND PROCEDURES
doc("coc", "policies/Code of Conduct.docx", "Code of Conduct", "policy", "2024", "current", "2024-01-01", "HR", "internal", ALL, """
Code of Conduct

## Our standards
We deal honestly with customers and with each other. We keep customer information private. We do not use our position for private gain.

## Gifts
A gift worth more than UGX 100,000 from a customer or supplier is declared to Human Resources. Cash gifts are never accepted.

## Conflicts of interest
Declare any interest in a supplier, borrower or competitor. A staff member does not approve a loan, a claim or a contract in which they have a personal interest.

## Social media
Do not post customer information or internal documents. Do not speak for Kitara unless authorised by Corporate Affairs.

## Breaches
Breaches are handled under the disciplinary procedure. Serious breaches may lead to dismissal and a report to the police.


## Speaking up
A staff member who sees conduct that breaks this Code reports it to their line manager, the Head of Human Resources or through the Whistleblowing Policy. Nobody is punished for a report made in good faith.

## Customers and fair treatment
We explain products and fees in plain words and in a language the customer understands. We do not pressure a customer to buy a product, and we do not sell a loan or a policy that the customer cannot afford. We keep a record of the advice we give.

## Use of company property
Kitara laptops, phones, vehicles and systems are for work. Limited personal use is allowed when it does not affect work or security. Software that has not been approved by IT is not installed. Staff return all property on their last working day.

## Political activity
Staff may take part in politics in their own time. Staff do not use Kitara premises, vehicles, email or branding for political activity, and do not speak for Kitara on political matters.

## Declarations
Each year every member of staff signs a declaration that they have read this Code and have declared any gift, interest or outside work that could conflict with their duties.""", fmt="docx")

doc("procure", "policies/Procurement Policy.docx", "Procurement Policy", "policy", "2025", "current", "2025-01-01", "Finance", "internal", ALL, """
Procurement Policy

## Quotations
Purchases up to UGX 5,000,000 need one written quotation. Purchases above UGX 5,000,000 need at least three written quotations. The cheapest quotation is not always chosen but the reason for the choice is written down.

## Tender committee
Purchases above UGX 50,000,000 go to the Tender Committee. Purchases above UGX 500,000,000 need Board approval.

## Suppliers
New suppliers are registered by Finance after a tax clearance check and a due diligence form. A supplier that handles customer data must also pass the information security review.

## Payment
Invoices are paid within 30 days of receipt of goods and a correct invoice. No payment is made against a verbal order.
""", fmt="docx")

doc("records", "policies/Records Management Procedure.pdf", "Records Management Procedure", "policy", "2024", "current", "2024-04-01", "Legal and Compliance", "internal", ALL, """
## Purpose
This procedure tells staff where records are kept, how they are named and when they are destroyed.

## Where to keep records
Official records are kept in the document management system or in the departmental folder on the shared drive. Customer files are never kept on a personal drive, a desktop or a phone. Scanned customer documents go into the customer's file in the core banking system.

## Naming
Name a file with the department, the title, the version and the date. Example: Claims_Settlement_Letter_v02_2026-03-14. A final version is saved as PDF.

## Versions
When a document is replaced, move the old version to the Archive folder of the same department and write the replacement date in the document properties. Do not leave two versions in the same folder.

## Destruction
Records are destroyed according to the Data Retention Schedule. The records owner signs the destruction list each year in April.


## Scanned records
A paper record that is scanned for the file is scanned at 300 dots per inch in black and white or grey. The scan is saved as PDF with the customer number in the file name. The paper original is kept for 12 months after scanning in the branch records room and is then destroyed, unless the law requires the original.

## Shared drives
Each department has one folder tree on the shared drive. The head of department names a folder owner. The folder owner removes access for leavers each month, deletes duplicate files and moves replaced documents to the Archive folder. Folders with no owner are reported to Legal and Compliance every quarter.

## Email
Email is not a records system. A staff member who receives a decision, an approval or a customer instruction by email saves it to the customer's file or to the departmental folder the same day. Mailboxes are archived after 12 months and deleted after five years.

## Legal holds
When Legal and Compliance places a hold on a record, nobody destroys it, even if the retention period has ended. The hold stays until Legal and Compliance releases it in writing. The records owner keeps a list of the records under hold.

## Audit
Internal Audit tests records management once a year. The test covers naming, location, destruction lists and the Archive folder. The results go to the Audit Committee.""")

doc("cash", "policies/Branch Cash Handling Procedure.pdf", "Branch Cash Handling Procedure", "policy", "2024", "current", "2024-06-01", "Branch Operations", "internal", "branch_ops;executive", """
## Teller limits
A teller may hold up to UGX 15,000,000 in the drawer. Cash above that amount is moved to the vault in the presence of a second person.

## Dual control
The vault is opened by two officers holding separate keys. The vault log is signed at each opening. Cash counts are done at opening, at midday and at closing.

## Cash in transit
Cash is moved between branches only by the approved security company. Branch staff do not carry cash in private vehicles.

## Differences
A cash difference above UGX 50,000 is reported to the Branch Manager the same day and to Branch Operations within 24 hours. A teller with three differences in a month is retrained.
""")

doc("fraudplan", "policies/Fraud Response Plan.pdf", "Fraud Response Plan", "policy", "2025", "current", "2025-03-01", "Risk", "restricted", "legal_compliance;risk;executive", """
## Reporting
Any suspected fraud is reported to the Head of Risk within 24 hours. Staff do not confront the person or open an investigation themselves.

## The Special Investigations Unit
The Special Investigations Unit (SIU) decides whether to investigate. It secures the evidence, including email, system logs and CCTV, before the person suspected is told.

## Loss and recovery
Losses above UGX 10,000,000 are reported to the Audit Committee. The SIU recommends whether to report to the police and to the regulator. Recovery steps are agreed with Legal and Compliance.

## Staff involved
A member of staff under investigation may be suspended on full pay. Access to systems is removed on the day of suspension.
""")

doc("agentguide", "policies/Agent Banking Guidelines.pdf", "Agent Banking Guidelines", "policy", "2025", "current", "2025-04-01", "Branch Operations", "internal", "branch_ops;executive", """
## Appointing an agent
An agent must have traded for 12 months, hold a trading licence and keep a separate float account. The agent signs the agent agreement and attends one day of training.

## Services
Agents open Mobile Wallets, take cash in and cash out, pay bills and receive loan repayments. Agents do not open savings accounts and do not approve loans.

## Commission
The agent earns 0.5 percent of the value of each cash-out and UGX 300 for each wallet opened with verified identification. Commission is paid on the 5th of the next month.

## Float
The daily float cap is set by circular. Agents reconcile their float register each day by 6:00 pm.

## Suspension
An agent who opens wallets without checking identification is suspended pending review.
""")

doc("agentmanual", "policies/Mobile Money Agent Manual.pdf", "Mobile Money Agent Manual", "policy", "2025", "current", "2025-04-01", "Branch Operations", "internal", "branch_ops;executive", """
## Daily routine
Open the float register in the morning. Record the opening float. After each transaction check that the confirmation message matches the amount. Reconcile and sign the register at 6:00 pm.

## Customer identification
Check the original identity document for every wallet opening. A customer who cannot show an identity document is sent away without a wallet.

## Receipts and disputes
If the customer says money was not received, ask for the transaction number and call the agent support line at once. Do not reverse a transaction yourself.

## Failed or repeated messages
When the network is slow the switch may send a confirmation twice. Tell the customer to wait ten minutes before trying again. A repeated message does not mean the money was sent twice.

## Security
Never share your agent PIN, not even with a Kitara officer. Kitara staff never ask for it.
""")

doc("underwrite", "policies/Motor Underwriting Guidelines.pdf", "Motor Underwriting Guidelines", "policy", "2025", "current", "2025-01-01", "Underwriting", "restricted", "underwriting;executive", """
## Vehicle age
A vehicle older than 15 years needs an inspection report before comprehensive cover. Vehicles older than 25 years are offered third party only.

## Driver loadings
A driver under 23 years carries a premium loading of 25 percent. A driver with two or more claims in three years carries a loading of 15 percent.

## Commercial use
Taxi, delivery and hire vehicles are rated at commercial rates. A private policy used for hire is not covered.

## Authority
An underwriter may accept risks up to a sum insured of UGX 150,000,000. Higher risks go to the Head of Underwriting.


## Inspection
A vehicle that needs an inspection is inspected at an approved garage. The report must be dated within 14 days before the start of cover. The underwriter records the chassis number, the mileage and any existing damage, and attaches photographs.

## Referral
The following risks are referred to the Head of Underwriting whatever the sum insured: vehicles registered abroad, vehicles with a modified engine, a customer with a cancelled policy in the last three years, and any risk with a total loss claim in the last two years.

## Renewals
A renewal is offered at least 21 days before expiry. The underwriter reviews the claims record and updates the no-claim discount. A renewal with a premium increase above 15 percent is explained to the customer in writing.

## Cancellation
A customer may cancel at any time. Premium for the unused period is returned, less a charge of 10 percent of the annual premium and any claim paid. Kitara may cancel for non-payment after 14 days of written notice.""")

doc("reinsure", "policies/Reinsurance Programme Summary.pdf", "Reinsurance Programme Summary", "policy", "2025", "current", "2025-01-01", "Underwriting", "confidential", "underwriting;finance;executive", """
Summary of the 2025 reinsurance programme. Confidential to Underwriting, Finance and the Executive Committee.

## Motor and property
Kitara retains the first UGX 500,000,000 on any one risk. Losses above that are shared with the reinsurers under a surplus treaty, and Kitara keeps 40 percent of the surplus.

## Catastrophe cover
A catastrophe excess of loss treaty covers UGX 8,000,000,000 above a retention of UGX 2,000,000,000 for a single event such as a flood affecting many policies.

## Life
Life policies with a sum assured above UGX 300,000,000 are reinsured at 50 percent.

## Reporting
Finance reports reinsurance recoveries to the Audit Committee every quarter. The treaty is renewed each year on 1 January.
""")

doc("charter", "policies/Customer Charter.pdf", "Customer Charter", "policy", "2024", "current", "2024-01-01", "Customer Service", "public", ALL, """
Kitara Customer Charter

## Our promises
We will answer the phone within 60 seconds in office hours. We will acknowledge every complaint within 24 hours. We will tell you the fee before you pay it. We will settle valid insurance claims within 30 days of receiving your last document.

## Your part
Keep your PIN private. Tell us quickly when your phone or card is lost. Give us correct and complete information.

## Contact
Call 0800 100 200, visit any of our 38 branches in Uganda or our 9 branches in Kenya, or write to customercare@kitaragroup.example.
""")

doc("pwd", "policies/Password and Access Standard.pdf", "Password and Access Standard", "policy", "2025", "current", "2025-02-01", "IT", "internal", ALL, """
## Passwords
A password has at least 12 characters and is not a dictionary word, a name or a date of birth. Passwords are not changed on a fixed calendar, but must be changed at once if there is a suspicion that they are known to someone else. The same password is never used for Kitara and for personal accounts.

## Privileged access
Administrator accounts are separate from daily accounts, protected by a hardware token and reviewed every month by IT Security.

## Joiners, movers and leavers
Access is given on a written request from the line manager. When a staff member changes department, old access is removed within five working days. A leaver loses access within 24 hours.


## Multi-factor authentication
Multi-factor authentication is required for email, remote access and every system that holds customer data. Kitara supports an authenticator application on a phone or a hardware token. A text message is used only as a fallback. A staff member who changes phone registers the new device before returning the old one.

## Shared and service accounts
Shared accounts are not allowed for people. A service account used by a system has a named owner, a password of at least 20 characters stored in the password vault, and a review every quarter.

## Remote access
Remote access is by the Kitara VPN on a Kitara laptop. A staff member working outside Uganda tells IT Security before travelling. Access from a country on the restricted list is blocked.

## Reviews
System owners review who has access every quarter and confirm the list in writing to IT Security. Access that nobody can justify is removed. IT Security reports the number of accounts removed to the IT Steering Committee.""")

doc("aiuse", "policies/Acceptable Use of Generative AI Tools.pdf", "Acceptable Use of Generative AI Tools", "policy", "2026", "current", "2026-06-01", "IT", "internal", ALL, """
## Scope
This policy applies to public chatbots, writing assistants and any other tool that sends text to an outside service.

## What you may not enter
Do not enter customer names, account numbers, national identity numbers, phone numbers, claim details, loan files, salary data or any document marked restricted or confidential into a public AI tool.

## What you may do
You may use a public AI tool for general drafting, translation and learning, using text that contains no Kitara data. You must check every result before you use it in work.

## Approved sandbox
IT will provide an internal AI sandbox that runs inside Kitara systems. Staff register with IT Security before use. Prompts and results in the sandbox are logged and kept for 12 months.

## Breach
Entering restricted data into a public tool is reported to IT Security within one hour and handled as a security incident.
""")

doc("vendor", "policies/Vendor Management Procedure.pdf", "Vendor Management Procedure", "policy", "2024", "current", "2024-08-01", "Finance", "internal", "finance;risk;legal_compliance;executive", """
## Onboarding
Each new vendor completes the due diligence form, a tax clearance check and a conflicts declaration. Vendors that handle customer data complete the information security questionnaire.

## Contracts
Contracts above UGX 50,000,000 are reviewed by Legal and Compliance. Every contract names a Kitara contract owner, the service levels, the exit terms and how data is returned or destroyed.

## Review
The contract owner reviews each vendor every year against service levels. A vendor with two service failures in a quarter is placed on a watch list.


## Payment
Finance pays a vendor only against a purchase order, a signed delivery note or service report, and a correct invoice. The contract owner confirms the service report before payment. Advance payments above UGX 10,000,000 need the approval of the Chief Finance Officer.

## Data and security
A vendor that handles customer data may process it only for the purpose written in the contract. The vendor tells Kitara within 24 hours of any security incident that affects Kitara data. When the contract ends the vendor returns the data in a standard format and then destroys its copies, and signs a certificate of destruction.

## Subcontractors
A vendor may use a subcontractor only with the written consent of the contract owner. The vendor stays responsible for the subcontractor's work and for its handling of data.

## Termination
Kitara may end a contract for repeated service failures, a breach of data protection duties or loss of a licence. The contract owner tells Legal and Compliance before notice is given. The exit plan in the contract is followed so that service to customers continues.""")

doc("itchange", "policies/IT Change Management Procedure.pdf", "IT Change Management Procedure", "policy", "2024", "current", "2024-05-01", "IT", "internal", ALL, """
## Changes
Every change to a production system is requested in the IT service desk system with a description, a risk rating, a test result and a rollback plan.

## Approval
A low risk change is approved by the IT team lead. A medium or high risk change is approved by the Change Board, which meets every Tuesday and Thursday at 10:00 am.

## Freeze periods
No changes to the core banking system or the mobile money switch are made during month-end close, which runs from the last working day to the third working day of the next month, or during the December freeze from 15 December to 5 January.


## Emergency changes
An emergency change is made to restore service or close a serious security hole. The IT duty manager may approve it alone. The change is recorded in the service desk system within one working day and reviewed by the Change Board at its next meeting.

## Testing and rollback
Every change is tested in the test environment first. The rollback plan says who reverses the change, how long it takes and what data would be lost. A change without a tested rollback plan is not approved.

## Communication
The change owner tells affected departments at least two working days before a medium or high risk change. Branches are told by the Branch Operations duty officer. The message says the date, the time, the expected effect and who to call.

## Review after the change
The change owner confirms within one working day that the change worked. A change that caused an incident is reviewed in a post-incident meeting within five working days, and the lessons are added to the change checklist.""")

doc("training", "policies/Training and Development Policy.docx", "Training and Development Policy", "policy", "2024", "current", "2024-01-01", "HR", "internal", ALL, """
Training and Development Policy

## Budget
Kitara sets aside 1.5 percent of annual payroll for training.

## Study leave
Staff on approved courses may take up to 10 working days of study leave a year, in addition to annual leave.

## Bonding
A course that costs more than UGX 5,000,000 carries a bond of 12 months. A staff member who leaves before the bond ends repays a share of the fees.

## Mandatory training
All staff complete AML training and information security training every year.
""", fmt="docx")

doc("appraisal", "policies/Performance Appraisal Procedure.docx", "Performance Appraisal Procedure", "policy", "2024", "current", "2024-01-01", "HR", "internal", ALL, """
Performance Appraisal Procedure

## Cycle
Objectives are agreed by 31 January. A mid-year review is held by 31 July. The annual appraisal is completed by 15 January of the following year.

## Ratings
Ratings run from 1 (does not meet expectations) to 5 (outstanding). A rating of 1 or 2 leads to a written improvement plan of 90 days.

## Moderation
Heads of department moderate ratings so that no more than 15 percent of their staff receive a 5.
""", fmt="docx")

doc("leaveproc", "policies/Leave Application Procedure.docx", "Leave Application Procedure", "policy", "2025", "current", "2025-07-01", "HR", "internal", ALL, """
Leave Application Procedure

## How to apply
Apply through the HR portal at least 14 days before the first day of leave, except for sick leave and compassionate leave. The line manager approves or declines within three working days.

## Compassionate leave
Up to five working days are granted on the death of a spouse, child, parent or sibling.

## Balance
Staff can see their leave balance on the HR portal. Leave not taken and not carried forward lapses on 31 March.
""", fmt="docx")

doc("branchopen", "policies/Branch Opening and Closing Procedure.pdf", "Branch Opening and Closing Procedure", "policy", "2024", "current", "2024-06-01", "Branch Operations", "internal", "branch_ops;executive", """
## Opening
Two staff arrive together. The alarm is switched off by the Branch Manager or the Operations Officer. Systems are checked before the doors open. Doors open to customers at the time in the current opening hours circular.

## Closing
The last customer is served before the doors close. Tellers balance and the vault is locked under dual control. The alarm is set and the closing log is sent to Branch Operations by 6:30 pm.

## Emergencies
In a robbery staff follow the instructions of the robbers, press the silent alarm only if safe, and do not give chase.
""")

doc("dormant", "policies/Dormant Accounts Procedure.pdf", "Dormant Accounts Procedure", "policy", "2024", "current", "2024-04-01", "Retail Banking", "internal", ALL, """
## Definition
An account is dormant when the customer has made no deposit or withdrawal for 12 months. Interest paid and automatic charges do not count as customer activity.

## Notice
The branch writes to the customer 30 days before an account is marked dormant. A dormant account cannot be used until the customer shows identification at a branch.

## Unclaimed balances
A balance that has been dormant for five years is transferred to the unclaimed funds register. The customer or the heirs can still claim it with identification.
""")

doc("classify", "policies/Data Classification Standard.pdf", "Data Classification Standard", "policy", "2025", "current", "2025-02-01", "IT", "internal", ALL, """
Kitara uses four classes. The owner of a data set chooses the class. When in doubt, choose the higher class.

## Public
Information already published or meant for the public, such as product guides, the Customer Charter and annual reports.

## Internal
Information for staff only, such as circulars, procedures and the staff directory.

## Restricted
Information limited to named departments, such as customer account data, claims files, loan files, committee minutes and personal data of customers.

## Confidential
Information limited to named people. This includes salary data, national identity numbers held in bulk, investigation files, board remuneration papers, regulator enforcement correspondence and the reinsurance programme.

## Marking
Documents carry the class in the header or footer. Data sets carry it in the data catalogue entry. A data set with no class is treated as restricted until the owner decides.


## Examples by department
- Retail Banking: product guides are public. Customer account data is restricted. A bulk list of national identity numbers is confidential.
- Claims: claim forms and claim letters are restricted. A life claim with a medical report is confidential.
- Human Resources: the staff directory is internal. Personnel files are restricted. Salary bands and disciplinary cases are confidential.
- Finance: published accounts are public. The general ledger is restricted. Board remuneration papers are confidential.
- Legal and Compliance: regulatory notices are internal or public. Enforcement correspondence is confidential.

## Handling rules
Public and internal documents may be shared by email inside Kitara. Restricted documents are shared only with the departments named in the document properties, and only through the shared drive link. Confidential documents are shared only with named people, are never printed without the owner's approval, and are encrypted when sent outside Kitara.

## Changing a class
The owner may raise a class at any time. Lowering a class needs the written agreement of Legal and Compliance. A data set that mixes classes takes the highest class of any field in it.

## Review
The owner reviews each data set's class every year, and again whenever the content of the data set changes.""")

doc("naming", "policies/Document Naming and Versioning Guide.pdf", "Document Naming and Versioning Guide", "policy", "2024", "current", "2024-04-01", "Legal and Compliance", "internal", ALL, """
## File names
Use Department_Title_vNN_YYYY-MM-DD. Do not use words such as final, new, latest or copy in a file name.

## Version history
Every policy has a version table on its last page with the version number, the date, the author and a one-line summary of the change.

## Replacing a document
Publish the new version, then move the old one to the department's Archive folder within five working days. Tell staff by circular when a policy is replaced.
""")
