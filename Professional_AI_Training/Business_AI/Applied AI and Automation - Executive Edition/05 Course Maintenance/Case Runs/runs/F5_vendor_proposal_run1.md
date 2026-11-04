# Review of the OrbitDesk AI proposal (OD-2026-117) for Nile Valley Foods

Note: the proposal says it is a fictional teaching document. I reviewed it as if it were real.

## Bottom line

Do not sign this as written, and do not share bank login details under any circumstances. The proposal has several serious red flags, offers almost no evidence, and its terms put nearly all the risk on Nile Valley Foods. If the company wants to explore the idea, it should start with a small, supervised pilot on a narrow task, on terms it controls.

## Red flags (most serious first)

1. **Payments with no approval step, up to the full bank balance (section 4).** The agent could send money to any supplier, including a wrong, fake or fraudulent one, with no human check. One mistaken, manipulated or fraudulent invoice could drain the account. The activity log only lets you see the loss after it has happened. This is a basic internal-control failure.
2. **"Share your bank login details" (section 10).** Sharing credentials breaks bank terms and removes your audit trail, because actions look like they came from you. A legitimate provider would use a restricted, read-only or limited-permission integration. This one request is enough to stop the process.
3. **"Replaces your accounts team from week one" (section 2).** This is unrealistic and risky. It removes the people who check the work, hold supplier relationships and know your business, before the tool has proven anything. It also raises staffing and legal questions.
4. **Your data trains their models for everyone, on all plans (section 5).** Supplier prices, bank details and payment history could be used to improve products your competitors also use. The proposal says it is enabled on all plans, which suggests you may not be able to opt out. "Handled with care" and "available wherever needed" say nothing about where data is stored, who sees it, or what happens when you leave.
5. **No references (section 7).** "Customers prefer to stay private" is unverifiable. Every customer being unwilling to speak is unusual. The only proof offered is a demo on sample data, which proves nothing about your invoices.
6. **Pressure tactics (section 9).** A deadline of 15 November 2026 is days away. Real finance-system decisions need a proper review. Urgency is used to stop you doing that.
7. **Contract terms that trap you (section 8).** A 36-month initial term, annual billing in advance, auto-renewal at the "then-current rate" with no cap on the increase, and "subscriptions end only at renewal" means no exit if it does not work. Combined with the uncapped per-action charge, the cost is open-ended.
8. **No accountability.** Nothing says who pays if the agent makes a wrong payment, books wrong entries or causes a data breach. There is no liability, indemnity, insurance, service level or error-correction process described.

## Claims I would question, and why

| Claim | Why I question it |
|---|---|
| "Does this work for you, around the clock, so your people can think about the future" (section 1) | Marketing language. Finance work needs judgement, exceptions handling and sign-off. Nothing shows the agent can do these reliably. |
| "Connects to email, accounting package and bank in under one day" (section 2) | Integrations normally need testing, access approvals, mapping to your chart of accounts and bank-side authorisation. One day suggests either shallow integration or ignored controls. |
| "Handles invoices, supplier statements, payment runs and month-end reports", including a trial balance (section 2) | A very wide scope with no detail on how each task works, what it cannot do, or how mistakes are caught. The trial balance and management report depend on correct accruals, adjustments and judgement that someone must own. |
| "English, French and Swahili" | No evidence of quality, especially for scanned or handwritten invoices, local tax invoice formats (such as EFRIS or VAT rules in your countries), or mixed-language documents. |
| "World-class team", "fast-growing", "used in many countries and industries" (section 2) | Pure assertion. No customer numbers, company age, funding, ownership, team names, or financial strength. A new vendor with weak finances could disappear with your data and prepaid fees. |
| "Industry-leading accuracy on every document, and gets smarter every day" (section 3) | No accuracy figure, no test method, no benchmark, no error rate. "Every document" is impossible. "Smarter every day" implies the system changes without notice, which can break behaviour you tested, and may link back to training on your data. |
| "Our customers love the results" | Unsupported, and contradicted by the refusal to give references. |
| "Works with the most popular accounting packages, banks, mobile money providers... if your system is not listed, our team will find a way to connect it" (Integrations) | No list is given. "Find a way" may mean screen scraping, credential sharing or unsupported workarounds. Your actual accounting package and banks are not named. |
| "Security built on the same principles as the best in the world. Engineers are trained and systems monitored" (section 6) | Empty. No certification (such as ISO 27001 or SOC 2), no penetration test, no incident history, no encryption, access-control, or breach-notification detail. |
| "Customers recoup the cost in 60 days" and "savings up to 90%" (ROI) | No basis, no case study, and "up to" and "depending on your business" make it meaningless. 90% savings would mean almost no finance function is needed, which is not credible. Pay-back in 60 days against a 36-month commitment also does not fit with the cost structure. |
| "Fully autonomous operation is what makes the savings possible" (section 4) | This frames removing controls as a feature. The savings argument is used to justify the biggest risk. |
| "Set-up and onboarding are included" | Probably true as a price line, but check what it covers (data migration, training, parallel running) and what is extra. |
| "Support replies on weekdays; premium costs extra" | A tool that touches payments needs fast escalation for errors and fraud. No response times are stated. Month-end and weekend failures are not covered. |
| "Price available until 15 November 2026" | Probably an artificial deadline. Standard list price is not stated, so you cannot tell if there is any real discount. |

## Other gaps

- The standard rate per action is USD 0.40 with no monthly cap, and "action" is not defined. A single invoice may involve several actions (read, match, book, pay, chase). The bill could greatly exceed the USD 2,400 fee. Ask for a worked example using your monthly invoice volume.
- Total commitment: USD 2,400 x 36 = USD 86,400 minimum, before usage, premium support or price rises, with the first year paid up front.
- The registered address and phone number are placeholders. Verify the company is registered and who owns it.
- Nothing on data location, regulation (data protection laws in your countries), audit rights, or what happens to data at exit.
- Nothing on what happens when the agent is unsure, wrong, or unavailable.
- The proposal is addressed to the Finance Manager only. A tool with bank access should involve the Managing Director, the auditors and IT or security.

## The eight most important questions to ask the vendor

1. **Payment controls:** Can payments require human approval, with limits per payment and per day, a supplier whitelist, and dual authorisation? Can the agent be set to prepare payments only? Why does the proposal offer none of this?
2. **Bank access:** Why do you need our bank login details? Can you integrate through a restricted, auditable, bank-approved connection with no shared credentials and no ability to change payee details?
3. **Accuracy evidence:** What is the measured accuracy (for example, per field and per document type), how was it tested, on whose data, and by whom? Will you run a pilot on our own real invoices and let us measure the results before we commit?
4. **Our data and model training:** Can we opt out of our data being used to train your models, in writing, on our plan? Where is our data stored, who can access it, how long is it kept, and how do we get it back and have it deleted when we leave?
5. **Security and assurance:** Which independent certifications and audits do you hold (ISO 27001, SOC 2), can we see the reports and latest penetration test, and what is your breach history and notification process?
6. **References and track record:** Can we speak with at least two paying customers of similar size and sector, ideally in East Africa? How many customers do you have, how long have you operated, who owns and funds the company?
7. **Liability and errors:** If the agent pays the wrong supplier, books wrong entries or causes a breach, who is liable and for how much? What insurance do you carry, and what is the process to reverse and recover errors?
8. **Cost and exit:** What exactly counts as an "action", what would our bill have been last year at our volumes, and can usage be capped? Why a 36-month term with auto-renewal at uncapped rates, and can we have a 3 to 6 month pilot with a termination right if targets are missed, a price-rise cap, and data export on exit?

## Suggested next steps

- Do not accept the 15 November deadline. Say you will decide after a proper review.
- Do not sign the order form or share bank credentials.
- Ask for written answers to the eight questions above and check them against the contract.
- Have the Managing Director, IT and your auditors or a lawyer review it.
- If you proceed, run a limited pilot in read-only mode on one task (for example, invoice capture and matching), with a human approving every entry and payment, compare results to your team's work, and only then consider expanding.
