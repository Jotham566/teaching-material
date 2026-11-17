"""Corpus for Session 4: three skins (contract clauses, finance terms, HR policy paragraphs), 10 passages each, and 4 plain-words queries per skin.
Everything is invented for teaching (Nile Valley Foods Ltd is fictional). Each query names the passage (by id) that a reader would call the right answer."""

TEXTS = [  # bag of words and TF-IDF demo: four short invented customer messages
    ('A', 'Please send 20 bags of maize flour to Mbale'),
    ('B', 'The maize flour was late and the invoice is wrong'),
    ('C', 'Please send the invoice for the rice order'),
    ('D', 'Rice delivery was late again, please call me'),
]

SKINS = {
 'contracts': dict(
  title='Contract clauses',
  passages=[
   ('K1', 'Force majeure', 'Neither party is liable for delay or failure caused by events beyond its reasonable control, including flood, fire, strike or government action.'),
   ('K2', 'Indemnity', 'The Supplier shall compensate the Buyer for any loss, claim or cost that arises from the Supplier\'s breach of this Agreement.'),
   ('K3', 'Limitation of liability', 'The Supplier\'s total liability under this Agreement shall not exceed the fees paid in the twelve months before the claim.'),
   ('K4', 'Termination for convenience', 'Either party may end this Agreement by giving ninety days\' written notice. No reason is required.'),
   ('K5', 'Confidentiality', 'Each party shall keep the other\'s business information secret and use it only for the purpose of this Agreement.'),
   ('K6', 'Automatic renewal', 'This Agreement continues for successive terms of one year unless a party gives written notice sixty days before the term ends.'),
   ('K7', 'Price adjustment', 'The Supplier may change the unit prices once in each quarter by giving thirty days\' written notice to the Buyer.'),
   ('K8', 'Governing law', 'This Agreement is governed by the laws of Uganda and the courts of Uganda have exclusive jurisdiction.'),
   ('K9', 'Assignment', 'Neither party may transfer its rights or duties under this Agreement to another person without the written consent of the other party.'),
   ('K10', 'Data protection', 'Each party shall handle any personal data received under this Agreement in line with the Data Protection and Privacy Act, 2019.')],
  queries=[
   ('Q1', 'What happens if heavy rain floods the road and the delivery cannot get through?', 'K1'),
   ('Q2', 'Who pays us back if the supplier\'s mistake costs us money?', 'K2'),
   ('Q3', 'Can we walk away from the deal without giving any reason?', 'K4'),
   ('Q4', 'The contract keeps running every year unless we say something in time.', 'K6')]),
 'finance': dict(
  title='Finance and invoice terms',
  passages=[
   ('F1', 'Accounts payable', 'Money the company owes to suppliers for goods and services it has received but not yet paid for.'),
   ('F2', 'Accounts receivable', 'Money that customers owe the company for goods sold on credit.'),
   ('F3', 'Accrual', 'A cost recorded in the month it was incurred, even if the invoice has not yet arrived or been paid.'),
   ('F4', 'Credit note', 'A document that cancels or reduces an earlier invoice, for example when goods are returned.'),
   ('F5', 'Bank reconciliation', 'Comparing the company\'s own records with the bank statement to find and explain any differences.'),
   ('F6', 'Depreciation', 'Spreading the cost of a truck or a machine over the years in which it will be used.'),
   ('F7', 'Petty cash', 'A small float kept in the office for minor cash expenses, with a receipt for each one.'),
   ('F8', 'Purchase order', 'A document sent to a supplier that states what the company will buy, how many, and at what price.'),
   ('F9', 'Three-way match', 'Checking that the purchase order, the goods received note and the supplier invoice agree before payment is released.'),
   ('F10', 'Bad debt write-off', 'Removing from the books an amount that a customer will not pay.')],
  queries=[
   ('Q5', 'The money we still have to pay the maize miller for flour already delivered.', 'F1'),
   ('Q6', 'The shop sent back damaged bags and we want to reduce what they owe.', 'F4'),
   ('Q7', 'Make sure our books match what the bank says.', 'F5'),
   ('Q8', 'Before we pay a bill, check that the order, the delivery and the bill all agree.', 'F9')]),
 'hr': dict(
  title='HR policy paragraphs',
  passages=[
   ('H1', 'Probation', 'New staff are on probation for the first three months. Their manager reviews their work before the job is confirmed.'),
   ('H2', 'Annual leave', 'Employees earn paid leave each month. Leave dates are agreed with the line manager in advance.'),
   ('H3', 'Sick leave', 'An employee who is too ill to work must tell their manager on the first day and bring a medical note after three days.'),
   ('H4', 'Grievance procedure', 'An employee who has a complaint about their treatment at work may raise it first with their manager and then in writing with the HR Officer.'),
   ('H5', 'Disciplinary procedure', 'Misconduct is handled with a verbal warning, then a written warning, then a hearing before any dismissal.'),
   ('H6', 'Whistleblowing', 'A staff member who reports suspected fraud or danger in good faith will be protected from any punishment.'),
   ('H7', 'Overtime', 'Work beyond normal hours must be approved in advance and is paid or taken back as time off.'),
   ('H8', 'Expense claims', 'Staff may claim approved travel costs by submitting receipts within seven days of the trip.'),
   ('H9', 'Resignation and notice', 'An employee who wishes to leave must give one month\'s written notice to the HR Officer.'),
   ('H10', 'Staff records', 'Personnel files are confidential and are seen only by the HR Officer and the Managing Director.')],
  queries=[
   ('Q9', 'I saw a colleague stealing stock and I am afraid to say so.', 'H6'),
   ('Q10', 'I am unhappy with how my supervisor speaks to me and want to complain.', 'H4'),
   ('Q11', 'I have malaria and cannot come to work tomorrow.', 'H3'),
   ('Q12', 'I want to quit. How much warning do I have to give?', 'H9')]),
}
