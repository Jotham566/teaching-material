# Review of the OrbitDesk AI proposal (OD-2026-117) for Nile Valley Foods

(The proposal says it is a fictional teaching document. I reviewed it as if it were real.)

**Bottom line:** Do not sign, and do not share bank login details. The proposal has several serious red flags. The most dangerous are uncapped autonomous payments, a request for your bank login, and a 36-month lock-in with a deadline to rush you. Treat it as unproven until the vendor answers the questions below in writing and passes a controlled trial.

## Claims I would question, and why

1. **"Replaces your accounts team from week one."** Nobody can replace a finance team in a week. It also removes the people who check the work. The proposal itself describes only invoices, matching, payments and reports. It does not cover tax filings, audit support, disputes, judgement calls or exceptions. Who handles those?
2. **"Connects to your email, accounting package and bank in under one day."** This is unlikely, and unsafe if true. Real integrations need testing, access approvals and bank authorisation. "Our team will find a way to connect it" means unlisted systems are unproven. No actual systems are named. Is a Ugandan or East African accounting package and mobile money provider really supported?
3. **"Industry-leading accuracy on every document" and "gets smarter every day."** There is no number, no test method, no benchmark and no error rate. "Every document" is impossible for any tool. "Gets smarter every day" suggests the system changes without notice, which raises the risk of silent errors and makes testing harder. Combined with section 5, it may mean it learns from your data.
4. **"Our customers love the results" and "Customers recoup the cost in 60 days."** No customer, no case study, no data. The 60 days is stated as a fact, while "up to 90% savings" is hedged with "depending on your business". "Up to" is not a typical result. A 90% cut in finance processing cost conflicts with the vendor's own pricing and with the need for human review.
5. **"Fast-growing company with a world-class team... used in many countries and industries."** None of this can be checked. There are no customer counts, founding date, ownership, financials or named staff. The registered address is "40 Example Street, Nairobi", and a sales email is the only contact.
6. **"Security built on the same principles as the best in the world. Engineers are trained and systems are monitored."** This is empty. There is no certification (such as ISO 27001 or SOC 2), no pen-test report, no encryption description, no breach history, no access controls. For a tool that touches your bank, this is not acceptable.
7. **"Your data is handled with care and is available to the Agent wherever it is needed."** Vague. Where is the data stored, in which country, who can see it, how long is it kept, and can it be deleted?
8. **"Customer inputs help OrbitDesk models improve for everyone, enabled on all plans."** Your invoices, supplier names, prices and bank details would train a product also used by your competitors and suppliers. It is on for every plan, so apparently you cannot opt out. This may conflict with data protection law and your supplier confidentiality obligations.
9. **"Speaks English, French and Swahili."** Fine as a claim, but untested on your documents. Real supplier invoices are often scans, photos, handwritten or mixed-language. Ask for evidence on your own samples.
10. **"Fully autonomous operation is what makes the savings possible."** This presents removing controls as a benefit. The savings come from removing human oversight, which is exactly where the risk sits.
11. **"You can review the activity log whenever you like."** A log is not a control. It shows what already happened after money has left. It does not say whether the log is complete, tamper-proof or exportable.
12. **"Set-up and onboarding included"** against **"share your bank login details with our onboarding team."** The first is a selling point, and the second is a security failure (see red flags).
13. **"This price is available until 15 November 2026."** There is no stated list price, so the "discount" cannot be judged. The deadline is only days away, which is classic pressure to skip due diligence.

## Red flags

**Critical (stop-level)**
- **Payments with no approval step, up to the full balance of the bank account.** One error, one fake invoice, one prompt-injection or one compromised login could empty the account. This breaks basic segregation of duties: the same system reads the invoice, books it, and pays it. There is no limit, no dual approval and no supplier whitelist.
- **"Share your bank login details."** Never give anyone your bank credentials. Banks forbid it, it likely breaches your bank mandate and terms, and it would make you liable for losses. Legitimate tools use bank-approved integrations or read-only access with separate approvals.
- **Payment fraud exposure.** Invoice fraud and changed-bank-detail scams are the main attack on finance teams. The proposal says nothing about detecting them, verifying changed supplier bank details, or catching duplicate invoices.
- **No stated accountability.** There is nothing on who pays if the Agent pays the wrong supplier, pays twice or is hacked. No liability terms, no insurance, no indemnity.

**Serious**
- **No references, no proof.** "Customers prefer to stay private" cannot be verified. Only a demo on sample data is offered, which proves nothing about your real documents.
- **Contract lock-in.** 36-month initial term, billed annually in advance, auto-renewal at "then-current rate" (uncapped increase), and "subscriptions end only at renewal". There is no exit for poor performance, no termination right and no refund. That is roughly USD 86,400 committed over the term before any usage charges.
- **Uncapped usage billing.** USD 0.40 per action over plan, "no monthly cap", with "action" undefined and the plan allowance not stated. A busy month or a software loop could produce a very large bill. The "tens of thousands of invoices" can quickly add up if each invoice triggers several actions.
- **Data used to train models for everyone,** with no opt-out.
- **Vague ROI.** The claim of 60-day payback is not backed by any assumptions, and cannot be reconciled with a USD 2,400-a-month fee plus usage charges.
- **Support only on weekdays** and premium support costs extra, for a system that pays money 24 hours a day. Who do you call at the weekend if it misfires? No service levels, no response times and no uptime commitment.
- **Pressure tactics.** Deadline pricing, "sign now, start tomorrow", and a one-day set-up promise all push you to skip checks.
- **Unclear compliance.** Nothing about tax (for example VAT/withholding handling), audit trail standards, local data protection law, or whether a regulated payments licence is required for initiating payments.
- **Role confusion.** It is addressed to the Finance Manager, yet says it replaces his team. Decision-makers (MD, board, auditors, bank) are not mentioned.

## The eight most important questions to ask the vendor

1. **Payment controls.** Can payments be limited by amount, supplier list and daily total, and require human approval (ideally two people) above a threshold? Why does the proposal say no approval step and access up to the full balance? Will you commit to approval-required and read-only defaults in writing?
2. **Bank access.** Why do you need our bank login? What bank-approved integration, API or limited-permission access do you use instead? Which banks and mobile money providers in Uganda are already live, with named examples?
3. **Accuracy evidence.** What are your measured error rates (extraction, matching, coding, payment), how were they measured, and by whom? Will you run a paid or free pilot on a month of our own real invoices, in parallel with our team, with agreed pass marks before any payment access?
4. **References and track record.** Give us at least three paying customers of our size and sector, in East Africa if possible, whom we can call. How many customers and invoices do you process today, and how long have you operated?
5. **Security and compliance.** Do you hold ISO 27001 or SOC 2 (send the reports), and the latest penetration test summary? How are credentials stored and access controlled? What is your breach history and notification process? What data protection registration and compliance do you have for Uganda?
6. **Data use.** Where is our data stored and who can access it? Can you switch off training on our data, in writing, on our plan? How long do you keep it and how is it deleted when we leave? Can we export everything?
7. **Liability and errors.** If the Agent pays the wrong party, pays twice or is compromised, who is liable? What is your liability cap, what insurance do you carry, and how fast can payments be stopped or recovered? What is the process for fraud, such as altered supplier bank details?
8. **Contract and costs.** What exactly is an "action", how many are included, and what would our typical month cost in total? Can we have a usage cap, a 12-month term (or a 30-90 day paid pilot) with termination for poor performance, a renewal price cap, and a refund right? What is the standard list price behind the 15 November "deadline"?

## Suggested next step

Reply that Nile Valley Foods is interested only on these terms: a written answer to the eight questions, a pilot in read-only mode on real documents in parallel with the current team, all payments human-approved, no bank credentials shared, and a short contract with an exit. Ignore the 15 November date, as a fair vendor will extend it. Involve your bank, your auditor and the MD before any decision.
