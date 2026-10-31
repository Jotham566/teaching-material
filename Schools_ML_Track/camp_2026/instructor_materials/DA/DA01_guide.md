# DA01 Instructor guide: Open a notebook and read your first table

Private. Keep this file out of the student folder.

**Objective.** By the end: you can open, run, save and reopen a notebook, and read a table of shop sales into it.

**Question of the day.** What does one week of sales in a small shop look like?

Prerequisite: START_HERE.md.

## The 180 minutes

| Minutes | Activity |
|---|---|
| 20 | welcome, laptop check, folders and the AI policy |
| 40 | Block A |
| 15 | break away from screens |
| 45 | Block B |
| 40 | Make |
| 20 | exit ticket, save and an individual check with each learner |

Where it overruns: Opening the notebook and finding the data file takes longer than the code. Walk every learner through the folder before the first run.

## Block A. Run your first cell

Read AI_USE_POLICY.md with your instructor now. It explains when AI tools are used in this camp and when they are not. Then click the code cell below and press Shift and Enter. Python is a language for giving a computer instructions. The word print tells it to show something. The brackets hold what to show.

Ask for the prediction first: Predict the two lines that will appear under the cell.

```python
print("Hello, data")
print(3 + 2)
```

Correct result: The output is Hello, data on the first line and 5 on the second. Text sits between matching quotation marks. A number such as 3 is an amount.

Investigate, with answers:

- Why does the first line keep its quotation marks in the code and lose them in the output? Answer: The quotation marks tell Python that the words are text. They are part of the instruction and not part of the message.
- What would print(3 + 2) show if the 3 were written as "3"? Answer: It would stop with an error, because Python cannot add text to a number.

Modify: Change Hello, data to your nickname and run the cell again. Answer: The first line now shows the nickname.

```python
print("Nyanzi")
print(3 + 2)
```

## Block B. Read the shop table

The file camp_shop.csv holds 60 sales from a practice shop. It has to sit in the same folder as this notebook. The three lines below are ready-made. You will learn how each part works in session 7. For now, read what comes out. The word head means the first rows.

Ask for the prediction first: Predict how many rows the table shows and which columns it has.

```python
import pandas as pd
shop = pd.read_csv("camp_shop.csv")
print(shop.head())
```

Correct result: The output shows the first five sales as a table. The columns are sale_id, date, item, units and unit_price_ugx. Sale 1 is one Book at 3000 shillings.

Investigate, with answers:

- How many columns does the table have, and what does each one record? Answer: Five. The sale number, the date, the item sold, the units sold and the price of one unit in Uganda shillings.
- Why does the first row show a sale of only 1 unit while the fourth shows 7? Answer: Different customers buy different amounts. The table records each sale as it happened.

Modify: Change head() to head(10) and run it again. Answer: Ten rows appear.

```python
ten = shop.head(10)
```

## Make: reference

```python
print("Nyanzi")
print(7 + 4)
import pandas as pd
shop = pd.read_csv("camp_shop.csv")
print(shop.head(3))
# The numerical result is 11.
```

Evidence to collect: DA01.ipynb that reopens with the nickname, 11 and three table rows.

## Misconceptions to listen for

- A notebook is a Word document.
- A text cell can run code.
- Pressing Enter runs a cell. Shift and Enter does.

## Questions to ask, with expected answers

- What is the difference between a text cell and a code cell? Expected: A text cell holds words for people. A code cell holds instructions that Python runs.
- Where does the output appear? Expected: Directly under the cell that produced it.

## Evidence and feedback

Record complete, needs repair or absent for each of the five learners, with one concrete repair action. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and live demonstrations need your judgement and are not auto-graded.
