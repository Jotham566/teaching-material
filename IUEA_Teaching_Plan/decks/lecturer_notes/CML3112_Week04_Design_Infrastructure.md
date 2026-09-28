# CML3112 Week04 Design Infrastructure

Lecturer companion to the revised PowerPoint. Slide numbers match this edition. Explain the worked examples directly; revision checks are for individual study.

## Slide 1 — Lists loops and reading a table

PURPOSE
Lists loops and reading a table

CONNECT
Previous slide: the preceding week.

EXPLAIN
Civil Engineering and Architecture

LECTURER CUE
Use PowerPoint Presenter View for these notes. Teach one example, pause for every learner to predict, then work an analogous example together. The practice notebook is a learning aid, not an extra graded upload.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Today’s learning.

REFERENCES


## Slide 2 — Today’s learning

PURPOSE
Today’s learning

CONNECT
Previous slide: Lists loops and reading a table.

EXPLAIN
Read lists and dictionary fields.

Trace a loop, read CSV rows and calculate summaries.

LECTURER CUE
Ask learners to explain this goal in ordinary language. The first successful attempt matters more than covering optional extensions. Defer: Nested comprehensions, arbitrary exception handling, a blank-page investigation and data-source hunting are later practice. Never use except: pass to silently erase evidence.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Connection to the previous lesson.

REFERENCES


## Slide 3 — Connection to the previous lesson

PURPOSE
Connection to the previous lesson

CONNECT
Previous slide: Today’s learning.

EXPLAIN
Week 3 introduced values, function inputs and results, conditions and list positions. Now we repeat a calculation across records, then organise those records by keys.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Why this week’s tools are needed.

REFERENCES


## Slide 4 — Why this week’s tools are needed

PURPOSE
Why this week’s tools are needed

CONNECT
Previous slide: Connection to the previous lesson.

EXPLAIN
Sensor readings arrive as records in a CSV file. We first learn the Python collections and loops needed to read those records and summarise them.

LECTURER CUE
A building team records indoor temperature to investigate comfort. Civil students can discuss construction and inspection; architecture students can discuss shading and ventilation. Explain the quantities before using them.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
List and index.

REFERENCES


## Slide 5 — List and index

PURPOSE
List and index

CONNECT
Previous slide: Why this week’s tools are needed.

EXPLAIN
List and index: A list holds values in order: [2, 4, 6]. Square brackets select a position. readings[0] selects the first item, 2.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A list position starts at zero.

REFERENCES


## Slide 6 — A list position starts at zero

PURPOSE
A list position starts at zero

CONNECT
Previous slide: List and index.

EXPLAIN
In [2, 4, 6], position 0 holds 2.

Position 1 holds 4. Position 2 holds 6.

There is no position 3 in this three-item list.

LECTURER CUE
Draw three boxes labelled 0, 1 and 2 holding 2, 4 and 6. Read the first item aloud, then trace the loop by hand.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Read list operations.

REFERENCES


## Slide 7 — Read list operations

PURPOSE
Read list operations

CONNECT
Previous slide: A list position starts at zero.

EXPLAIN
append and len: readings.append(8) adds 8 to the end of the list. len(readings) counts its items. The dot selects an operation belonging to that object; parentheses call it.

Slice: readings[1:3] selects positions 1 and 2. The stop position 3 is excluded. A slice produces a new list; it does not remove items from the original.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A list stores items in order.

REFERENCES


## Slide 8 — A list stores items in order

PURPOSE
A list stores items in order

CONNECT
Previous slide: Read list operations.

EXPLAIN
Read the code in this order:
readings = [2, 4, 6]
print(readings[0])
readings.append(8)
print(len(readings))
print(readings[1:3])

print displays a value below the cell.

append adds one item to the end of a list.

Square brackets create a list or select an item.

[] builds a list. Positions start at zero. The slice stops before position 3.

LECTURER CUE
Read each symbol before running. Ask everyone to predict. Expected output: 2 then 4 then [4, 6]. readings[4] would raise IndexError.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Trace the list changes.

REFERENCES


## Slide 9 — Trace the list changes

PURPOSE
Trace the list changes

CONNECT
Previous slide: A list stores items in order.

EXPLAIN
Instruction | List afterwards | Displayed output

readings = [2, 4, 6] | [2, 4, 6] | Nothing yet

print(readings[0]) | [2, 4, 6] | 2

readings.append(8) | [2, 4, 6, 8] | Nothing yet

print(readings[1:3]) | [2, 4, 6, 8] | [4, 6]

len reports 4 after append. A slice excludes its stop position and leaves the original list intact.

Read the rows in order. len reports 4 after append. A slice excludes its stop position and leaves the original list intact.

Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A loop repeats instructions.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 10 — A loop repeats instructions

PURPOSE
A loop repeats instructions

CONNECT
Previous slide: Trace the list changes.

EXPLAIN
A loop runs a block more than once. One execution of the block is called an iteration.

for takes one item at a time from a collection. Use it when each item needs the same action.

while repeats while a condition stays True. Use it when a condition controls repetition. We will trace each kind before using it in a calculation.



Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Read every part of a for header.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 11 — Read every part of a for header

PURPOSE
Read every part of a for header

CONNECT
Previous slide: A loop repeats instructions.

EXPLAIN
In for reading in readings:, for introduces repetition, reading names the current item, and readings is the collection to visit.

in connects the current-item name to that collection. The colon begins the loop body. Four spaces mark each instruction that repeats.

reading is a name we choose; it is assigned the next item automatically. It is not the same name as readings. After the last item, execution leaves the loop.



Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Visit each item without calculating.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 12 — Visit each item without calculating

PURPOSE
Visit each item without calculating

CONNECT
Previous slide: Read every part of a for header.

EXPLAIN
Read the code in this order:
readings = [2, 4, 6]
for reading in readings:
    print(reading)
print("finished")

The body runs once for each item.

The final line is outside the loop, so it runs once.

Output: 2; 4; 6; finished

Expected printed output:
2
4
6
finished

Run the complete cell, then trace each line. Expected output:
2
4
6
finished

Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Trace the for loop item by item.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 13 — Trace the for loop item by item

PURPOSE
Trace the for loop item by item

CONNECT
Previous slide: Visit each item without calculating.

EXPLAIN
Step | Current reading | Action

First item | 2 | Print 2

Second item | 4 | Print 4

Third item | 6 | Print 6

No items left | No new item | Leave loop; print finished

An empty list runs the body zero times. It still reaches the outside line.

Read the rows in order. An empty list runs the body zero times. It still reaches the outside line.

Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Updating a counter inside a loop.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 14 — Updating a counter inside a loop

PURPOSE
Updating a counter inside a loop

CONNECT
Previous slide: Trace the for loop item by item.

EXPLAIN
A counter records how many times an event happens. Set count = 0 before the loop, then count = count + 1 inside it.

count += 1 is a shorter spelling for that numeric update. Similarly, total += reading means total = total + reading.

The initial value belongs outside the loop. Resetting count to zero inside every iteration loses the earlier count.



Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Count the visited items.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 15 — Count the visited items

PURPOSE
Count the visited items

CONNECT
Previous slide: Updating a counter inside a loop.

EXPLAIN
Read the code in this order:
count = 0
for reading in [2, 4, 6]:
    count += 1
print(count)

Updates: 0 to 1, 1 to 2, then 2 to 3.

Output: 3

Expected printed output:
3

Run the complete cell, then trace each line. Expected output:
3

Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Accumulator.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 16 — Accumulator

PURPOSE
Accumulator

CONNECT
Previous slide: Count the visited items.

EXPLAIN
Accumulator: A running total. Set it to zero before the loop, add inside the loop, and read the final total afterward.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A loop repeats an indented block.

REFERENCES


## Slide 17 — A loop repeats an indented block

PURPOSE
A loop repeats an indented block

CONNECT
Previous slide: Accumulator.

EXPLAIN
for reading in readings: takes one item at a time.

The colon starts the block. Four spaces show which lines repeat.

A running total must start at zero before the loop.

LECTURER CUE
Trace the native loop table that follows. Predict total after each item. An empty list needs a guard before dividing by its length.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A mean uses a total and a count.

REFERENCES


## Slide 18 — A mean uses a total and a count

PURPOSE
A mean uses a total and a count

CONNECT
Previous slide: A loop repeats an indented block.

EXPLAIN
Start the total at 0. Add 2, then 4, then 6.

The final total is 12. The count is 3.

12 / 3 gives the mean 4. An empty list needs a separate rule.

LECTURER CUE
Make a table with columns reading and total: (2,2), (4,6), (6,12). len(readings) counts three items. 12 / 3 is 4.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A loop changes the running total.

REFERENCES


## Slide 19 — A loop changes the running total

PURPOSE
A loop changes the running total

CONNECT
Previous slide: A mean uses a total and a count.

EXPLAIN
This illustration uses six separate readings. Next we trace the smaller list [2, 4, 6] using the same running-total rule.

LECTURER CUE
The displayed mean is rounded to two decimals. Keep full precision in calculations. This larger illustration follows the same rule as our smaller 2, 4, 6 example.
Source: existing course illustration figs/accumulator_trace.png. These are illustrative examples, not this cohort’s assessed results.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Tracing the loop.

REFERENCES
Source: existing course illustration figs/accumulator_trace.png. These are illustrative examples, not this cohort’s assessed results.

## Slide 20 — Tracing the loop

PURPOSE
Tracing the loop

CONNECT
Previous slide: A loop changes the running total.

EXPLAIN
Step | reading | total after addition

Before loop | — | 0

First | 2 | 2

Second | 4 | 6

Third | 6 | 12

There are three readings.

LECTURER CUE
There are three readings. The mean is 12 / 3 = 4. Reset total before repeating the calculation.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Worked example.

REFERENCES


## Slide 21 — Lists loops and records in Python

PURPOSE
Lists loops and records in Python

CONNECT
Previous slide: Tracing the loop.

EXPLAIN
Read the code in this order:
readings = [2, 4, 6]
total = 0
for reading in readings:
    total = total + reading
mean = total / len(readings)
print(mean)

for takes the next item. The indented block repeats.

print displays a value below the cell.

Square brackets create a list or select an item.

Read top to bottom. Run the complete example in the matching practice notebook.

LECTURER CUE
Draw three boxes labelled 0, 1 and 2 holding 2, 4 and 6. Read the first item aloud, then trace the loop by hand. Make a table with columns reading and total: (2,2), (4,6), (6,12). len(readings) counts three items. 12 / 3 is 4. Before a real CSV, show a two-line text extract and name its header. Open the issued CSV together. Explain csv.DictReader as one dictionary per row. Convert only the numeric column and state what should happen to an invalid value.

Complete practice code:
readings = [2, 4, 6]
total = 0
for reading in readings:
    total = total + reading
mean = total / len(readings)
print(mean)

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Expected output.

REFERENCES


## Slide 22 — Lists loops and records results

PURPOSE
Lists loops and records results

CONNECT
Previous slide: Lists loops and records in Python.

EXPLAIN
4.0

LECTURER CUE
Compare the actual output character by character with this practice result. If it differs, read the first error and check the input, units, names and execution order. Do not copy this practice output into a graded answer.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
The built-in summary functions.

REFERENCES


## Slide 23 — The built-in summary functions

PURPOSE
The built-in summary functions

CONNECT
Previous slide: Lists loops and records results.

EXPLAIN
Function | Question it answers | For [2, 4, 6]

len | How many items? | 3

sum | What is their total? | 12

min | Which is smallest? | 2

max | Which is largest? | 6

These functions already exist in Python. min and max need at least one item unless an explicit default is supplied.

Read the rows in order. These functions already exist in Python. min and max need at least one item unless an explicit default is supplied.

Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Built-in summaries of a list.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 24 — Built-in summaries of a list

PURPOSE
Built-in summaries of a list

CONNECT
Previous slide: The built-in summary functions.

EXPLAIN
Read the code in this order:
readings = [2, 4, 6]
print(sum(readings))
print(len(readings))
print(min(readings))
print(max(readings))

These functions are built into Python.

min and max require a nonempty list here.

Output: 12, 3, 2, 6. sum totals; len counts; min and max select the smallest and largest.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A while loop checks before each repetition.

REFERENCES


## Slide 25 — A while loop checks before each repetition

PURPOSE
A while loop checks before each repetition

CONNECT
Previous slide: Built-in summaries of a list.

EXPLAIN
while count < 3: tests the condition before entering its indented block. True enters the block; False skips it and continues after the loop.

At the end of the body, return to the condition and test again. Unlike for, while does not automatically move to the next list item.

Something must make the condition become False, or the loop may continue indefinitely. In our example, count increases on every iteration.



Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A while loop with a stopping condition.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 26 — A while loop with a stopping condition

PURPOSE
A while loop with a stopping condition

CONNECT
Previous slide: A while loop checks before each repetition.

EXPLAIN
Read the code in this order:
count = 0
while count < 3:
    print(count)
    count = count + 1
print("finished")

Initialise, test, run the body, update, test again.

When count becomes 3, the condition is False.

Output: 0; 1; 2; finished

Expected printed output:
0
1
2
finished

Run the complete cell, then trace each line. Expected output:
0
1
2
finished

Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Trace the while condition and update.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 27 — Trace the while condition and update

PURPOSE
Trace the while condition and update

CONNECT
Previous slide: A while loop with a stopping condition.

EXPLAIN
count before test | count < 3 | Body and next count

0 | True | Print 0; update to 1

1 | True | Print 1; update to 2

2 | True | Print 2; update to 3

3 | False | Skip body; print finished

If count starts at 3, the body runs zero times. The condition is tested first.

Read the rows in order. If count starts at 3, the body runs zero times. The condition is tested first.

Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Preventing an endless loop.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 28 — Preventing an endless loop

PURPOSE
Preventing an endless loop

CONNECT
Previous slide: Trace the while condition and update.

EXPLAIN
If the update is missing, count remains 0. The question 0 < 3 stays True, so the body keeps running.

In Colab, click the running cell’s stop button or use Runtime → Interrupt execution. Fix the condition or update before running again.

Do not run an intentionally endless example. Trace the unchanged value on the slide to see why it would fail.



Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Choosing if for or while.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 29 — Choosing if for or while

PURPOSE
Choosing if for or while

CONNECT
Previous slide: Preventing an endless loop.

EXPLAIN
Construct | Purpose | When it finishes

if / else | Choose a path once | After the chosen block

for | Visit supplied items | When items are exhausted

while | Repeat while True | When condition becomes False

A condition alone does not imply repetition: if tests once; while tests again after its body.

Read the rows in order. A condition alone does not imply repetition: if tests once; while tests again after its body.

Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
range supplies a sequence of integers.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 30 — range supplies a sequence of integers

PURPOSE
range supplies a sequence of integers

CONNECT
Previous slide: Choosing if for or while.

EXPLAIN
range(3) supplies 0, 1 and 2. The stop value 3 is excluded. range(1, 4) supplies 1, 2 and 3.

Use range with for when a numbered repetition is useful. The loop still works by taking the next supplied item.

range(0, 6, 2) uses a step of 2 and supplies 0, 2, 4. A step is the change between successive numbers; it cannot be zero.



Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Repeat with range.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 31 — Repeat with range

PURPOSE
Repeat with range

CONNECT
Previous slide: range supplies a sequence of integers.

EXPLAIN
Read the code in this order:
for attempt in range(1, 4):
    print(attempt)

Start at 1; stop before 4.

Output: 1; 2; 3

Expected printed output:
1
2
3

Run the complete cell, then trace each line. Expected output:
1
2
3

Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
continue and break change a loop’s path.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 32 — continue and break change a loop’s path

PURPOSE
continue and break change a loop’s path

CONNECT
Previous slide: Repeat with range.

EXPLAIN
continue skips the rest of the current iteration, then starts the next iteration. It does not end the whole loop.

break exits the nearest enclosing loop immediately. Execution resumes after that loop.

Put the condition inside the loop with four spaces. Its action is inside that condition with eight spaces: an indented block inside another block.



Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Skip one item using continue.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 33 — Skip one item using continue

PURPOSE
Skip one item using continue

CONNECT
Previous slide: continue and break change a loop’s path.

EXPLAIN
Read the code in this order:
for reading in [2, -1, 6]:
    if reading < 0:
        continue
    print(reading)

-1 takes continue, so its print is skipped.

2 and 6 reach print.

Output: 2; 6

Expected printed output:
2
6

Run the complete cell, then trace each line. Expected output:
2
6

Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Stop at one item using break.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 34 — Stop at one item using break

PURPOSE
Stop at one item using break

CONNECT
Previous slide: Skip one item using continue.

EXPLAIN
Read the code in this order:
for reading in [2, -1, 6]:
    if reading < 0:
        break
    print(reading)

-1 triggers break. The loop never visits 6.

Output: 2

Expected printed output:
2

Run the complete cell, then trace each line. Expected output:
2

Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Trace the two loop controls.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 35 — Trace the two loop controls

PURPOSE
Trace the two loop controls

CONNECT
Previous slide: Stop at one item using break.

EXPLAIN
Input | continue version | break version

2 | Print 2 | Print 2

-1 | Skip its print | Exit loop

6 | Print 6 | Never visited

Use continue only when skipping is justified by the stated data rule; do not silently discard evidence.

Read the rows in order. Use continue only when skipping is justified by the stated data rule; do not silently discard evidence.

Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A dictionary is a record with named fields.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 36 — A dictionary is a record with named fields

PURPOSE
A dictionary is a record with named fields

CONNECT
Previous slide: Trace the two loop controls.

EXPLAIN
record = {"unit": "A", "reading": 4} stores two key–value pairs. Keys name fields; values hold the information.

Braces enclose the dictionary. A colon separates each key from its value and a comma separates pairs. Each key is unique.

record["reading"] returns 4. Unlike a list position, "reading" names the field we want.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A missing dictionary key and get.

REFERENCES


## Slide 37 — A missing dictionary key and get

PURPOSE
A missing dictionary key and get

CONNECT
Previous slide: A dictionary is a record with named fields.

EXPLAIN
record["reading"] requests a known field. If that key does not exist, square-bracket lookup raises KeyError.

record.get("missing", 0) asks for that key with a fallback: return 0 if it is absent. This does not add a new key.

The second input is the fallback value. Use a fallback only when the task defines what missing information should mean.



Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Reading and updating a dictionary.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 38 — Reading and updating a dictionary

PURPOSE
Reading and updating a dictionary

CONNECT
Previous slide: A missing dictionary key and get.

EXPLAIN
Read the code in this order:
record = {"unit": "A", "reading": 4}
print(record["reading"])
record["reading"] = 6
print(record["reading"])
print(record.get("missing", 0))

["reading"] selects a key, not a position.

Assigning through the key updates its value.

Output: 4, then 6, then 0. get uses the fallback only when that key is absent.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Tuples and unpacking.

REFERENCES


## Slide 39 — Tuples and unpacking

PURPOSE
Tuples and unpacking

CONNECT
Previous slide: Reading and updating a dictionary.

EXPLAIN
A tuple stores items in order. point = (2, 3) stores two coordinates; point[0] is 2. You cannot reassign point[0].

x, y = point gives the first item to x and the second to y. This is unpacking; the number of names must match the number of items.

A tuple prevents replacing its positions. It does not freeze the contents of a mutable object stored inside it.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Unpacking a pair.

REFERENCES


## Slide 40 — Unpacking a pair

PURPOSE
Unpacking a pair

CONNECT
Previous slide: Tuples and unpacking.

EXPLAIN
Read the code in this order:
point = (2, 3)
x, y = point
print(x)
print(y)

Two names receive the two items in order.

Output: 2, then 3.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A set remembers distinct items.

REFERENCES


## Slide 41 — A set remembers distinct items

PURPOSE
A set remembers distinct items

CONNECT
Previous slide: Unpacking a pair.

EXPLAIN
A set is useful when the question is “Have we seen this ID?” It keeps one instance of each distinct item.

seen = set() creates an empty set. seen.add("A") adds an item. "A" in seen asks whether it is present.

Do not use a set when position or repeated readings matter. Sets cannot be indexed. {} creates an empty dictionary, not an empty set.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Set membership and repeated IDs.

REFERENCES


## Slide 42 — Set membership and repeated IDs

PURPOSE
Set membership and repeated IDs

CONNECT
Previous slide: A set remembers distinct items.

EXPLAIN
Read the code in this order:
seen = set()
seen.add("A")
seen.add("A")
print(len(seen))
print("A" in seen)
print("B" in seen)

in returns True or False.

A set answers membership questions.

Output: 1, True, False. Adding the same ID twice keeps one distinct ID.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
How the four collections differ.

REFERENCES


## Slide 43 — How the four collections differ

PURPOSE
How the four collections differ

CONNECT
Previous slide: Set membership and repeated IDs.

EXPLAIN
Collection | Find an item by | Repeats / changes

list | Position: values[0] | Repeats allowed; items change

dict | Key: record["reading"] | Keys unique; values change

tuple | Position: point[0] | Repeats allowed; positions fixed

set | Membership: "A" in seen | Distinct items; add or remove

Choose by the question: ordered readings, named fields, fixed positions, or distinct IDs.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Dictionary items and two loop names.

REFERENCES


## Slide 44 — Dictionary items and two loop names

PURPOSE
Dictionary items and two loop names

CONNECT
Previous slide: How the four collections differ.

EXPLAIN
record.items() provides each key with its value as a pair. The loop unpacks each pair into the names key and value.

for key, value in record.items(): repeats the indented body for each field. Use .items() when both the label and its value are needed.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Looping through named fields.

REFERENCES


## Slide 45 — Looping through named fields

PURPOSE
Looping through named fields

CONNECT
Previous slide: Dictionary items and two loop names.

EXPLAIN
Read the code in this order:
record = {"unit": "A", "reading": 6}
for key, value in record.items():
    print(key, value)

.items() supplies pairs.

key and value are names chosen for this loop.

Output: unit A, then reading 6. The dictionary preserves insertion order.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A position and a key find different things.

REFERENCES


## Slide 46 — A position and a key find different things

PURPOSE
A position and a key find different things

CONNECT
Previous slide: Looping through named fields.

EXPLAIN
Both examples return 4. Explain how each lookup finds it.

LECTURER CUE
Ask students to describe what they see before introducing terminology. Generated conceptual teaching illustration.  Source: figs/experiential/ASSET_SOURCES.md.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
CSV and header.

REFERENCES


## Slide 47 — CSV and header

PURPOSE
CSV and header

CONNECT
Previous slide: A position and a key find different things.

EXPLAIN
CSV and header: CSV means comma-separated values. One line usually represents one record; a header names the columns. CSV numbers arrive as text and may need float conversion.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
One record at a time.

REFERENCES


## Slide 48 — One record at a time

PURPOSE
One record at a time

CONNECT
Previous slide: CSV and header.

EXPLAIN
A CSV is a text table with a header row.

DictReader uses that header for dictionary keys.

CSV cells begin as text, even when they look numeric.

float("2.5") converts text into the number 2.5.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A CSV file has a header and text values.

REFERENCES


## Slide 49 — A CSV file has a header and text values

PURPOSE
A CSV file has a header and text values

CONNECT
Previous slide: One record at a time.

EXPLAIN
CSV line | Dictionary meaning

unit,reading | Two field names

A,2.5 | {"unit": "A", "reading": "2.5"}

B, | {"unit": "B", "reading": ""}

An empty field is empty text. Check the task’s rule before converting it.

LECTURER CUE
Read one row at a time and use a changed value. This is a syntax reference for the worked examples.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A CSV row becomes a dictionary.

REFERENCES


## Slide 50 — A CSV row becomes a dictionary

PURPOSE
A CSV row becomes a dictionary

CONNECT
Previous slide: A CSV file has a header and text values.

EXPLAIN
The header gives field names, such as unit and reading.

csv.DictReader returns one dictionary for each data row.

The value "2.5" starts as text. float("2.5") makes the number 2.5.

LECTURER CUE
Before a real CSV, show a two-line text extract and name its header. Open the issued CSV together. Explain csv.DictReader as one dictionary per row. Convert only the numeric column and state what should happen to an invalid value.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
with and import.

REFERENCES


## Slide 51 — with and import

PURPOSE
with and import

CONNECT
Previous slide: A CSV row becomes a dictionary.

EXPLAIN
with and import: import makes library tools available. with open(...) opens a file for a block and closes it afterward. A filename must match an existing file in the working folder.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Your cohort data.

REFERENCES


## Slide 52 — Your cohort data

PURPOSE
Your cohort data

CONNECT
Previous slide: with and import.

EXPLAIN
site_inspection_log.csv

Summarise crack_width_mm (millimetres); group by structure_id.

Read the issued task’s blank-value and threshold rules before calculating.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Read the supplied CSV in four steps.

REFERENCES


## Slide 53 — Read the supplied CSV in four steps

PURPOSE
Read the supplied CSV in four steps

CONNECT
Previous slide: Your cohort data.

EXPLAIN
Place site_inspection_log.csv beside the notebook, or upload it in Colab’s Files panel.

import csv loads the CSV tools. newline="" lets the reader handle line endings. DictReader uses the header as dictionary keys.

list(...) collects the rows while the file is open. We inspect the first row and the count; the later assignment calculations are your work.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
What with open as source does.

REFERENCES


## Slide 54 — What with open as source does

PURPOSE
What with open as source does

CONNECT
Previous slide: Read the supplied CSV in four steps.

EXPLAIN
open("file.csv", newline="") opens a text file for reading. Use the actual supplied filename, including its .csv extension.

with manages the open file. as source gives that file object a name. Indented lines use it while it is open; leaving the block closes it.

csv.DictReader(source) reads rows using the header names as keys. list(...) collects those rows into memory before the file closes.



Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Open a real CSV and inspect its first row.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 55 — Open a real CSV and inspect its first row

PURPOSE
Open a real CSV and inspect its first row

CONNECT
Previous slide: What with open as source does.

EXPLAIN
Read the code in this order:
import csv
with open("site_inspection_log.csv", newline="") as source:
    rows = list(csv.DictReader(source))
print(rows[0])
print(len(rows))

import loads a library. from selects a tool from it.

print displays a value below the cell.

Square brackets create a list or select an item.

Read the actual keys and text values. Check the uploaded filename if Python reports FileNotFoundError.

LECTURER CUE
Read the actual keys and text values. Check the uploaded filename if Python reports FileNotFoundError.

Complete practice code:
import csv
with open("site_inspection_log.csv", newline="") as source:
    rows = list(csv.DictReader(source))
print(rows[0])
print(len(rows))

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A list of dictionaries.

REFERENCES


## Slide 56 — A list of dictionaries

PURPOSE
A list of dictionaries

CONNECT
Previous slide: Open a real CSV and inspect its first row.

EXPLAIN
A record holds named fields for one observation. A list of records holds several observations in order.

records[0] selects the first dictionary. records[0]["reading"] then selects that dictionary’s reading field.

for row in records takes one dictionary at a time. row["reading"] retrieves that observation’s field; float converts numeric text when needed.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A record and a growing list.

REFERENCES


## Slide 57 — A record and a growing list

PURPOSE
A record and a growing list

CONNECT
Previous slide: A list of dictionaries.

EXPLAIN
Braces pair a key with its value. append adds one value to the end of a list.

The same pattern works after reading a CSV row.

LECTURER CUE
Braces pair a key with its value. append adds one value to the end of a list. The same pattern works after reading a CSV row.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A record and a growing list in Python.

REFERENCES


## Slide 58 — A record and a growing list in Python

PURPOSE
A record and a growing list in Python

CONNECT
Previous slide: A record and a growing list.

EXPLAIN
Read the code in this order:
records = [{"sensor": "A", "reading": "2.5"},
           {"sensor": "B", "reading": "3.5"}]
values = []
for row in records:
    values.append(float(row["reading"]))
print(values)

for takes the next item. The indented block repeats.

float converts numeric text into a decimal number.

print displays a value below the cell.

Read top to bottom. Run the complete example in the matching practice notebook.

LECTURER CUE
Braces pair a key with its value. append adds one value to the end of a list. The same pattern works after reading a CSV row.

Complete practice code:
records = [{"sensor": "A", "reading": "2.5"},
           {"sensor": "B", "reading": "3.5"}]
values = []
for row in records:
    values.append(float(row["reading"]))
print(values)

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Skip a blank before converting text.

REFERENCES


## Slide 59 — Skip a blank before converting text

PURPOSE
Skip a blank before converting text

CONNECT
Previous slide: A record and a growing list in Python.

EXPLAIN
An empty text field is "". The comparison != means “not equal to”. Only convert a value after the blank check passes.

In this example, values records valid numbers only. Its length is the valid count; the group summaries must use the same valid-record policy.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Collect only the recorded numbers.

REFERENCES


## Slide 60 — Collect only the recorded numbers

PURPOSE
Collect only the recorded numbers

CONNECT
Previous slide: Skip a blank before converting text.

EXPLAIN
Read the code in this order:
text_values = ["2.5", "", "3.5"]
values = []
for text in text_values:
    if text != "":
        values.append(float(text))
print(len(values), values)

for takes the next item. The indented block repeats.

if tests a condition. The chosen indented block runs.

float converts numeric text into a decimal number.

Expected: 2 [2.5, 3.5]. A blank is missing, not a recorded zero.

LECTURER CUE
Expected: 2 [2.5, 3.5]. A blank is missing, not a recorded zero.

Complete practice code:
text_values = ["2.5", "", "3.5"]
values = []
for text in text_values:
    if text != "":
        values.append(float(text))
print(len(values), values)

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Membership in a dictionary.

REFERENCES


## Slide 61 — Membership in a dictionary

PURPOSE
Membership in a dictionary

CONNECT
Previous slide: Collect only the recorded numbers.

EXPLAIN
group in totals asks whether group is already a dictionary key. group not in totals asks whether that key is absent.

Before adding to a new group, create its total with totals[group] = 0. Then add the current record’s reading.

The outer for visits records. The inner if runs only for a new group. The addition after the if runs for every record.



Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Summaries for separate groups.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 62 — Summaries for separate groups

PURPOSE
Summaries for separate groups

CONNECT
Previous slide: Membership in a dictionary.

EXPLAIN
A dictionary can hold one running total for each group.

An absent key needs an initial zero.

Then add the reading to that group.

To calculate group means, keep a matching count and divide each group total by its own count.

LECTURER CUE
A dictionary can hold one running total for each group. An absent key needs an initial zero. Then add the reading to that group. To calculate group means, keep a matching count and divide each group total by its own count.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Summaries for separate groups in Python (1/2).

REFERENCES


## Slide 63 — Summaries for separate groups in Python (1/2)

PURPOSE
Summaries for separate groups in Python (1/2)

CONNECT
Previous slide: Summaries for separate groups.

EXPLAIN
Read the code in this order:
records = [{"group": "A", "reading": 2},
           {"group": "A", "reading": 4},
           {"group": "B", "reading": 9}]
totals = {}
for row in records:
    group = row["group"]
    if group not in totals:
        totals[group] = 0
    totals[group] = totals[group] + row["reading"]

for takes the next item. The indented block repeats.

if tests a condition. The chosen indented block runs.

Square brackets create a list or select an item.

Read top to bottom. Run the complete example in the matching practice notebook.

LECTURER CUE
A dictionary can hold one running total for each group. An absent key needs an initial zero. Then add the reading to that group. To calculate group means, keep a matching count and divide each group total by its own count.

Complete practice code:
records = [{"group": "A", "reading": 2},
           {"group": "A", "reading": 4},
           {"group": "B", "reading": 9}]
totals = {}
for row in records:
    group = row["group"]
    if group not in totals:
        totals[group] = 0
    totals[group] = totals[group] + row["reading"]
print(totals)

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Summaries for separate groups in Python (2/2).

REFERENCES


## Slide 64 — Summaries for separate groups in Python (2/2)

PURPOSE
Summaries for separate groups in Python (2/2)

CONNECT
Previous slide: Summaries for separate groups in Python (1/2).

EXPLAIN
Read the code in this order:
print(totals)

print displays a value below the cell.

Continue the SAME cell; keep indentation. Run after all parts are entered.

LECTURER CUE
A dictionary can hold one running total for each group. An absent key needs an initial zero. Then add the reading to that group. To calculate group means, keep a matching count and divide each group total by its own count.

Complete practice code:
records = [{"group": "A", "reading": 2},
           {"group": "A", "reading": 4},
           {"group": "B", "reading": 9}]
totals = {}
for row in records:
    group = row["group"]
    if group not in totals:
        totals[group] = 0
    totals[group] = totals[group] + row["reading"]
print(totals)

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A group mean needs its own count.

REFERENCES


## Slide 65 — A group mean needs its own count

PURPOSE
A group mean needs its own count

CONNECT
Previous slide: Summaries for separate groups in Python (2/2).

EXPLAIN
The preceding loop calculated a total for each group. Count records in those same groups, then divide each group total by its own count.

items() supplies the group name and its total together. We use small invented records, not the assignment’s answers.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
From group totals to group means.

REFERENCES


## Slide 66 — From group totals to group means

PURPOSE
From group totals to group means

CONNECT
Previous slide: A group mean needs its own count.

EXPLAIN
Read the code in this order:
counts = {}
for row in records:
    group = row["group"]
    counts[group] = counts.get(group, 0) + 1
means = {}
for group, total in totals.items():
    means[group] = total / counts[group]
print(means)

for takes the next item. The indented block repeats.

print displays a value below the cell.

Square brackets create a list or select an item.

Expected: A has mean 3.0 and B has mean 9.0. Each group uses its own denominator.

LECTURER CUE
Expected: A has mean 3.0 and B has mean 9.0. Each group uses its own denominator.

Complete practice code:
counts = {}
for row in records:
    group = row["group"]
    counts[group] = counts.get(group, 0) + 1
means = {}
for group, total in totals.items():
    means[group] = total / counts[group]
print(means)

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
When numeric text cannot be converted.

REFERENCES


## Slide 67 — When numeric text cannot be converted

PURPOSE
When numeric text cannot be converted

CONNECT
Previous slide: From group totals to group means.

EXPLAIN
float("bad") raises ValueError: the text does not represent a number. An exception interrupts ordinary execution.

try contains the operation that might fail. except ValueError runs only for that named failure. Indentation shows the two blocks.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Catch one expected conversion failure.

REFERENCES


## Slide 68 — Catch one expected conversion failure

PURPOSE
Catch one expected conversion failure

CONNECT
Previous slide: When numeric text cannot be converted.

EXPLAIN
Read the code in this order:
text = "bad"
try:
    reading = float(text)
except ValueError:
    reading = None
print(reading)

float converts numeric text into a decimal number.

print displays a value below the cell.

= assigns the value on the right to the name on the left.

Expected: None. The assignment specifies which invalid records to skip; do not invent a replacement number.

LECTURER CUE
Expected: None. The assignment specifies which invalid records to skip; do not invent a replacement number.

Complete practice code:
text = "bad"
try:
    reading = float(text)
except ValueError:
    reading = None
print(reading)

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Trace conversion success and failure.

REFERENCES


## Slide 69 — Trace conversion success and failure

PURPOSE
Trace conversion success and failure

CONNECT
Previous slide: Catch one expected conversion failure.

EXPLAIN
Text supplied | try block | Result after except

"2.5" | float succeeds; skip except | 2.5

"bad" | float raises ValueError | None assigned by except

Only the named conversion failure is handled. Do not use except: pass to hide unrelated errors.

Read the rows in order. Only the named conversion failure is handled. Do not use except: pass to hide unrelated errors.

Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Revision example and answer.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 70 — Revision example and answer

PURPOSE
Revision example and answer

CONNECT
Previous slide: Trace conversion success and failure.

EXPLAIN
Example: Add 8 to the list. Trace the new total and count before running. What happens if total = 0 is moved inside the loop?

Answer: Total 20, count 4, mean 5.0. Resetting inside the loop discards previous additions and leaves only the last value in total.

LECTURER CUE
Give silent thinking time, then let pairs discuss. Rotate who types. This is practice, not a graded quiz. Expected response: Total 20, count 4, mean 5.0. Resetting inside the loop discards previous additions and leaves only the last value in total.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Preparing for the assignment.

REFERENCES


## Slide 71 — Preparing for the assignment

PURPOSE
Preparing for the assignment

CONNECT
Previous slide: Revision example and answer.

EXPLAIN
Open the issued W04 notebook and its cohort CSV.

Compute the requested valid_count, mean_reading, above_limit and group_means using the exact names in the notebook.

First identify the correct field and its unit.

Keep the CSV beside the notebook locally or upload it into the Colab runtime.

LECTURER CUE
Open the issued W04 notebook and its cohort CSV. Compute the requested valid_count, mean_reading, above_limit and group_means using the exact names in the notebook. First identify the correct field and its unit. Keep the CSV beside the notebook locally or upload it into the Colab runtime. The written interpretation is practice.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Preparing for the assignment continued.

REFERENCES


## Slide 72 — Preparing for the assignment continued

PURPOSE
Preparing for the assignment continued

CONNECT
Previous slide: Preparing for the assignment.

EXPLAIN
The written interpretation is practice.

LECTURER CUE
Open the issued W04 notebook and its cohort CSV. Compute the requested valid_count, mean_reading, above_limit and group_means using the exact names in the notebook. First identify the correct field and its unit. Keep the CSV beside the notebook locally or upload it into the Colab runtime. The written interpretation is practice.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Counting every record honestly.

REFERENCES


## Slide 73 — Counting every record honestly

PURPOSE
Counting every record honestly

CONNECT
Previous slide: Preparing for the assignment continued.

EXPLAIN
DictReader already consumes the header; skipping its first yielded row skips real data.

A string such as "unknown" cannot be converted to float.

Catch the expected conversion error, count and record it, then continue under a stated policy.

Inspect whether skipped rows share a source before reporting a mean.

LECTURER CUE
Teach these concepts before the weekly quiz. Use changed numbers for practice. This slide supplies concepts, not the quiz key.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Counting every record honestly continued.

REFERENCES


## Slide 74 — Counting every record honestly continued

PURPOSE
Counting every record honestly continued

CONNECT
Previous slide: Counting every record honestly.

EXPLAIN
A sample summary describes observed records, not every possible operating condition.

LECTURER CUE
Teach these concepts before the weekly quiz. Use changed numbers for practice. This slide supplies concepts, not the quiz key.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Your issued assignment.

REFERENCES


## Slide 75 — Your issued assignment

PURPOSE
Your issued assignment

CONNECT
Previous slide: Counting every record honestly continued.

EXPLAIN
Open W04_student.ipynb.

Read every task and its input units before coding.

Keep the required function names and returned outputs.

Run the supplied visible checks, then restart and run all.

LECTURER CUE
# Week 4 reading report
Read README.md. Keep units in your explanation.

## valid_count (5 marks)
Store an integer count of rows whose crack_width_mm field is nonblank. Skip blank readings before numeric conversion.

## mean_reading (5 marks)
Store the arithmetic mean of the nonblank crack_width_mm values as a number. Add the valid readings and divide by their count. Keep full precision.

## above_limit (5 marks)
Store an integer count of valid crack_width_mm readings strictly greater than 0.3. A reading equal to the threshold is not counted.

## group_means (5 marks)
Store a dictionary whose keys are the structure_id labels and whose values are the mean valid crack_width_mm readings within each group. Divide each group total by its own valid count. Keep full precision.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
valid_count (5 marks).

REFERENCES


## Slide 76 — valid_count (5 marks)

PURPOSE
valid_count (5 marks)

CONNECT
Previous slide: Your issued assignment.

EXPLAIN
Store an integer count of rows whose crack_width_mm field is nonblank.

Skip blank readings before numeric conversion.

LECTURER CUE
# Week 4 reading report
Read README.md. Keep units in your explanation.

## valid_count (5 marks)
Store an integer count of rows whose crack_width_mm field is nonblank. Skip blank readings before numeric conversion.

## mean_reading (5 marks)
Store the arithmetic mean of the nonblank crack_width_mm values as a number. Add the valid readings and divide by their count. Keep full precision.

## above_limit (5 marks)
Store an integer count of valid crack_width_mm readings strictly greater than 0.3. A reading equal to the threshold is not counted.

## group_means (5 marks)
Store a dictionary whose keys are the structure_id labels and whose values are the mean valid crack_width_mm readings within each group. Divide each group total by its own valid count. Keep full precision.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
mean_reading (5 marks).

REFERENCES


## Slide 77 — mean_reading (5 marks)

PURPOSE
mean_reading (5 marks)

CONNECT
Previous slide: valid_count (5 marks).

EXPLAIN
Store the arithmetic mean of the nonblank crack_width_mm values as a number.

Add the valid readings and divide by their count.

Keep full precision.

LECTURER CUE
# Week 4 reading report
Read README.md. Keep units in your explanation.

## valid_count (5 marks)
Store an integer count of rows whose crack_width_mm field is nonblank. Skip blank readings before numeric conversion.

## mean_reading (5 marks)
Store the arithmetic mean of the nonblank crack_width_mm values as a number. Add the valid readings and divide by their count. Keep full precision.

## above_limit (5 marks)
Store an integer count of valid crack_width_mm readings strictly greater than 0.3. A reading equal to the threshold is not counted.

## group_means (5 marks)
Store a dictionary whose keys are the structure_id labels and whose values are the mean valid crack_width_mm readings within each group. Divide each group total by its own valid count. Keep full precision.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
above_limit (5 marks).

REFERENCES


## Slide 78 — above_limit (5 marks)

PURPOSE
above_limit (5 marks)

CONNECT
Previous slide: mean_reading (5 marks).

EXPLAIN
Store an integer count of valid crack_width_mm readings strictly greater than 0.3.

A reading equal to the threshold is not counted.

LECTURER CUE
# Week 4 reading report
Read README.md. Keep units in your explanation.

## valid_count (5 marks)
Store an integer count of rows whose crack_width_mm field is nonblank. Skip blank readings before numeric conversion.

## mean_reading (5 marks)
Store the arithmetic mean of the nonblank crack_width_mm values as a number. Add the valid readings and divide by their count. Keep full precision.

## above_limit (5 marks)
Store an integer count of valid crack_width_mm readings strictly greater than 0.3. A reading equal to the threshold is not counted.

## group_means (5 marks)
Store a dictionary whose keys are the structure_id labels and whose values are the mean valid crack_width_mm readings within each group. Divide each group total by its own valid count. Keep full precision.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
group_means (5 marks).

REFERENCES


## Slide 79 — group_means (5 marks)

PURPOSE
group_means (5 marks)

CONNECT
Previous slide: above_limit (5 marks).

EXPLAIN
Store a dictionary whose keys are the structure_id labels and whose values are the mean valid crack_width_mm readings within each group.

Divide each group total by its own valid count.

Keep full precision.

LECTURER CUE
# Week 4 reading report
Read README.md. Keep units in your explanation.

## valid_count (5 marks)
Store an integer count of rows whose crack_width_mm field is nonblank. Skip blank readings before numeric conversion.

## mean_reading (5 marks)
Store the arithmetic mean of the nonblank crack_width_mm values as a number. Add the valid readings and divide by their count. Keep full precision.

## above_limit (5 marks)
Store an integer count of valid crack_width_mm readings strictly greater than 0.3. A reading equal to the threshold is not counted.

## group_means (5 marks)
Store a dictionary whose keys are the structure_id labels and whose values are the mean valid crack_width_mm readings within each group. Divide each group total by its own valid count. Keep full precision.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Week 4 rules.

REFERENCES


## Slide 80 — Week 4 rules

PURPOSE
Week 4 rules

CONNECT
Previous slide: group_means (5 marks).

EXPLAIN
Fictional teaching data.

300 records.

Three blank crack_width_mm values must be skipped in numerical summaries.

Threshold 0.3 is a teaching assumption.

LECTURER CUE
Fictional teaching data. 300 records. Three blank crack_width_mm values must be skipped in numerical summaries. Threshold 0.3 is a teaching assumption.

Compute valid_count, mean_reading, above_limit (strictly greater than 0.3) and group_means keyed by structure_id. Use standard-library csv and collections. Save a copy using your Student Registration Number with / replaced by _, followed by _W04.ipynb. STUDENT_ID in the starter code means Student Registration Number. Four checks carry five marks each. Explain the interesting pattern separately as formative practice.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Week 4 rules continued.

REFERENCES


## Slide 81 — Week 4 rules continued

PURPOSE
Week 4 rules continued

CONNECT
Previous slide: Week 4 rules.

EXPLAIN
Compute valid_count, mean_reading, above_limit (strictly greater than 0.3) and group_means keyed by structure_id.

Use standard-library csv and collections.

Save a copy using your Student Registration Number with / replaced by _, followed by _W04.ipynb.

STUDENT_ID in the starter code means Student Registration Number.

LECTURER CUE
Fictional teaching data. 300 records. Three blank crack_width_mm values must be skipped in numerical summaries. Threshold 0.3 is a teaching assumption.

Compute valid_count, mean_reading, above_limit (strictly greater than 0.3) and group_means keyed by structure_id. Use standard-library csv and collections. Save a copy using your Student Registration Number with / replaced by _, followed by _W04.ipynb. STUDENT_ID in the starter code means Student Registration Number. Four checks carry five marks each. Explain the interesting pattern separately as formative practice.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Week 4 rules continued.

REFERENCES


## Slide 82 — Week 4 rules continued

PURPOSE
Week 4 rules continued

CONNECT
Previous slide: Week 4 rules continued.

EXPLAIN
Four checks carry five marks each.

Explain the interesting pattern separately as formative practice.

For beginner step-by-step help, open ASSIGNMENT_INSTRUCTIONS.txt and STUDENT_HOW_TO.md in this folder.

The first names your required files and hand-in checklist; the second explains accounts, Colab, saving and uploads.

LECTURER CUE
Fictional teaching data. 300 records. Three blank crack_width_mm values must be skipped in numerical summaries. Threshold 0.3 is a teaching assumption.

Compute valid_count, mean_reading, above_limit (strictly greater than 0.3) and group_means keyed by structure_id. Use standard-library csv and collections. Save a copy using your Student Registration Number with / replaced by _, followed by _W04.ipynb. STUDENT_ID in the starter code means Student Registration Number. Four checks carry five marks each. Explain the interesting pattern separately as formative practice.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Reading report submission.

REFERENCES


## Slide 83 — Reading report submission

PURPOSE
Reading report submission

CONNECT
Previous slide: Week 4 rules continued.

EXPLAIN
Opens: 29 Sep 2026, 11:00 Kampala

Deadline: 06 Oct 2026, 11:00 Kampala

Use your full Student Registration Number in the form.

Keep the submitted files and confirmation.

LECTURER CUE
The form link is cohort-specific. Recheck the live form and release status before class. These scheduled assignment dates are separate from the quiz activation window. The issued brief defines the required files, even if the form accepts additional formats. Source: data/submission_links.json

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Week 4 quiz.

REFERENCES


## Slide 84 — Week 4 quiz

PURPOSE
Week 4 quiz

CONNECT
Previous slide: Reading report submission.

EXPLAIN
Answer individually after the lecturer activates the quiz.

Available for 24 hours from activation.

Use your Student Registration Number and registered account.

The lecturer will confirm the exact closing time.

LECTURER CUE
Activate the matching open_W4_CML3112 function in Quiz Controls, then confirm the 24-hour close time. Opening this slide or clicking its link does not activate the form. The 24 hours is the availability window. Keep existing quiz scoring and form rules. Do not show private answer keys.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Before you leave.

REFERENCES


## Slide 85 — Revision and submission checklist

PURPOSE
Revision and submission checklist

CONNECT
Previous slide: Week 4 quiz.

EXPLAIN
You can show how the total and count change for each record.

Save your work and check the required submission files.

LECTURER CUE
Ask every learner for an individual response. Record one misconception to revisit at the start of the next class. If a deadline changed, announce the exact Kampala date and update the source registry before rebuilding slides.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
independent revision and the issued task.

REFERENCES
