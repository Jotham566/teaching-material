"""Real-world hooks: the 'Where this is used' text for every session (31 Oct 2026).

One hook per lesson: DA (24), ML (24), the four ML labs and the ML25 extension. Each is 2 to 3 short sentences,
concrete and true, with no figures, company claims or statistics. It ties to what the session teaches and ends with a
question or an invitation. The verifier checks: non-empty, at most 60 words, no digits, house style, ends with a
question mark or an invitation.

Merged into the lesson dicts by lessons/da.py and lessons/ml.py (field name: hook).
"""

HOOKS_DA = [
    "Supermarkets, mobile money agents and clinics all start the day by opening a table of what happened yesterday. Today you open your first one, from a small shop. What would you most want to know about a shop after seeing one week of its sales?",
    "A till keeps a product name as text, a price as a number and a date as a date. If the types get mixed up, the totals go wrong. Which one is a phone number: text or a number?",
    "Revenue is units times price, added up. A shop owner does it by hand, and a program does it for every sale in a blink. Which error message have you seen on your phone, and what did it mean?",
    "Shops and delivery businesses often treat big orders differently, with free delivery, a discount or a call from the manager. A program makes that choice with if and else. What rule would you set for the big orders of your own shop?",
    "A shop has many sales, a league has many matches and a tailor has many orders. A loop handles every one of them without you typing each by hand. What would you loop over in your favourite sport?",
    "Payment and tax software relies on functions that must give the right answer on cases where the answer is already known. A check that fails loudly protects every customer. What known case would you use to test a discount function?",
    "Till exports, clinic registers and school timetables all become tables in Python. This is the table every data analyst works with. Which exported file would you most like to open?",
    "A shop owner asks which sales were big and how much money they brought in. Picking out rows and adding a new column is how analysts answer that on their own data. Which rows of a shop table would you pick out first?",
    "Retail chains compare their branches by grouping sales and finding the best sellers. A typical sale and an unusually large one tell different stories. Which branch would you visit first, and why?",
    "Exports from tills often hold duplicates, blanks and typing slips. Good analysts keep a log of every fix so the owner can trust the result. How many problems can you find before you fix a single one?",
    "Weather pages, football stats and mobile money summaries all lean on a chart to make one point quickly. A busy shop owner has a minute at most. Which chart would you show an owner who has only one minute?",
    "Every analyst sends someone a first report: a table, one chart and a few honest sentences. Today you make yours. Who would you most like to send it to?",
    "Weather offices and football analysts work with long rows of numbers, such as daily rainfall or distance run. They check how spread out the numbers are and spot unusual days. Which day in a shop would you call unusual?",
    "A histogram shows what a typical day looks like, and a box plot shows how groups differ. Club analysts compare players and teams with plots like these. Which two shops would you compare first?",
    "Taxi parks, shops and farms all ask whether rain changes demand. Two things moving together do not prove that one causes the other. Do rainy days keep customers away, or is something else going on?",
    "A raw export from a real system is rarely tidy. Analysts clean it with a function so the same steps run again on next month's file. Could you clean a file you have never seen?",
    "Customers, products and sales usually live in separate tables, and analysts join them. A careless join can count one sale twice. How would you check that your total is still right after a join?",
    "Accountants and auditors compare two totals and explain the gap. Banks and tax teams do this every month. Can you explain why your total is a little short of the true one?",
    "Data teams write a short plan before any code: the question, the data, the charts and what the data cannot say. Which three questions about a topic you love could a table answer?",
    "A result is only useful if someone else can repeat it. Analysts log each step and check each number two ways. Who could rerun your analysis and get the same numbers?",
    "A report that needs its author in the room has not done its job. Clear titles, labels and units let a farmer, a manager or a parent read it alone. Could your report speak for itself?",
    "Before a team hands work over, they restart everything and run it from the top to prove it works. A tidy handover saves other people days. Does your notebook run from the first cell to the last?",
    "Analysts explain their findings to busy people who do not write code. They say what they found, how they know, and what the data cannot tell. How would you say it to a parent in one minute?",
    "Start-ups and tech hubs hold demo days where builders show what they made and answer questions. Today is your demo day. What do you want your family to remember about your work?",
]

HOOKS_ML = [
    "Property apps and agents guess a fair rent from the size and area of a home. A model does the same after studying homes that were already rented, and today you build the smallest version. What rent would you guess for a home you know?",
    "A mobile money app keeps the amount as a number and the phone number as text. Mixing them up would cause real mistakes. What would go wrong if an app added two phone numbers together?",
    "Anything you type into a form arrives as text. The app has to turn it into a number before it can add, compare or charge. Where in the apps you use does text quietly become a number?",
    "Apps decide with rules such as: if the balance is too low, refuse the payment. Botanists also tell flowers apart by measuring petals, and today you write a three-line rule that does it. Can your rule beat a guess?",
    "A football league table is a list of teams with points, and a program loops over it to add up every match. Your mobile money statement works the same way. What would you loop over in your favourite sport?",
    "A fee calculator is a function: write it once and use it for every payment. Software teams also write checks with known answers, so a mistake shows up before a customer finds it. What check would you write for a fee calculator?",
    "A shop till, a clinic register and a school timetable are all tables with rows and columns. Programs read such tables from files before they can learn anything. Which table in your life would you like to open in Python?",
    "A shopkeeper asks which item earned the most this week. Answering needs a filter and a new column: units times price. What would you ask of the sales of your own shop?",
    "News reports quote the average income or the share of people who did something. One very large value can drag the mean up, while the median stays calm. Which would you quote for what most boda-boda rides on your road cost?",
    "Clinics, schools and banks collect data typed by busy people, so duplicates and blanks are normal. Data scientists clean the table and write down every change they make. What would you check first in a messy register?",
    "Weather forecasts, football stats and mobile money summaries all use charts so people can see a pattern fast. A good chart makes one clear point. What is the one point you want your chart to make?",
    "Every data job starts with one clear question and a table. A coffee trader, a football analyst and a clinic manager each begin that way. Which question would you like your own project to answer?",
    "Banks and mobile lenders use models to flag unusual payments, and they first ask whether the model beats a plain rule. That plain rule is the baseline. What plain guess would you make for tomorrow's weather?",
    "Rents, fares and crop prices often rise in a steady way with size, distance or season, and a straight line is the simplest model of that. Ride-hailing apps show a fare estimate before the trip starts. How far can one line take you?",
    "A model can look perfect on the homes it learned from and still fail on a new one. Teams that build tools for lending, fares or weather test on cases kept aside. Would you trust a model that was only tested on its own homework?",
    "Doctors and farm advisers sort cases into groups by asking questions in order: is there a fever, are the leaves spotted? A decision tree learns which questions to ask. Can your tree out-guess your own rule?",
    "A fraud alert that blocks a real payment upsets a customer, and one that misses fraud costs money. Teams count both kinds of mistake. When would a very high score make you suspicious?",
    "A football coach tests two formations on matches the team has not practised for. You do the same with two tree depths. Would you pick a formation after one lucky match?",
    "Real projects start with a written plan: the question, the data, and the column that would give the answer away. Data teams also protect private information. Which question could your data answer fairly?",
    "A trader guessing next week's maize price might simply repeat this week's price. A model has to do better than that plain guess to be useful. What is the plain guess for your project?",
    "When a model helps decide something about people, such as a loan, others ask why. The team must explain which inputs it used and defend them. Can you defend every input in your model?",
    "Before a model goes live, a team freezes it, tests it once on untouched data and packs the work so someone else can rerun it. Today you do the same. Could a stranger rerun your project tomorrow?",
    "Part of every data job is explaining results to people who do not code, such as managers, farmers or clinic staff. Can you explain your model to a parent in words a ten-year-old would follow?",
    "Start-ups and tech hubs hold demo days where builders show what they made in a few minutes and answer questions. Today is your demo day. What do you want your family to remember?",
]

HOOKS_LABS = [
    "A good programmer reads code and predicts its output before pressing run. A mobile money app keeps an amount, a name and a date in named boxes, and each one must be right. Can you predict every line before it runs?",
    "A row of daily temperatures or match scores only makes sense in a fixed order, with a unit. Weather stations and football analysts keep their numbers that way. What would break if the order of a list changed?",
    "Forecasts speak in chances, and clinics report the share of patients with a problem. Two groups can have the same average and still look very different. How would you tell two football teams apart if both score the same average?",
    "A model turns measurements into one number by giving each a weight, like a rent that grows with size and rooms. A ride fare grows with distance and time. Which input would you give the biggest weight when pricing a ride?",
]

HOOK_EXT = ("Many phones recognise speech with neural networks, which are big stacks of small calculations. For a small table, a tree or a line is often enough. "
            "Would you reach for the big model first?")
