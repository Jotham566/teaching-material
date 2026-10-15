# CML3113 Week04 Mining Petroleum

Lecturer companion. The same explanations are embedded in the PowerPoint speaker notes. Open Presenter View, or expand the Notes pane when preparing.

## Slide 1 — Lists loops and reading a table

Lists loops and reading a table
CML3113, Week 4, slide 1

Explanation to give
Move from one calculation to many records. Lists supply ordered values, loops visit them, dictionaries label fields and CSV files store the observations.

Worked illustration / lecturer answer
For readings 2, 4 and 6, the running total is 2, then 6, then 12. Count 3 gives mean 4.0. A group needs its own total and count.

Misconception to address
Use this as an orientation to the lesson. Terms and syntax will be unpacked on their own slides; students do not need to know them in advance.

On this slide
Mining and Petroleum Engineering

Continue to
Today’s learning

## Slide 2 — Today’s learning

Today’s learning
CML3113, Week 4, slide 2

Explanation to give
Move from one calculation to many records. Lists supply ordered values, loops visit them, dictionaries label fields and CSV files store the observations.

Worked illustration / lecturer answer
For readings 2, 4 and 6, the running total is 2, then 6, then 12. Count 3 gives mean 4.0. A group needs its own total and count.

Misconception to address
At the end, check the specific outcome shown here using a small previously demonstrated example. A completed file without an explanation is not evidence of understanding.

On this slide
Read lists and dictionary fields.

Trace a loop, read CSV rows and calculate summaries.

Continue to
Connection to the previous lesson

## Slide 3 — Connection to the previous lesson

Connection to the previous lesson
CML3113, Week 4, slide 3

Explanation to give
Move from one calculation to many records. Lists supply ordered values, loops visit them, dictionaries label fields and CSV files store the observations.

Worked illustration / lecturer answer
For readings 2, 4 and 6, the running total is 2, then 6, then 12. Count 3 gives mean 4.0. A group needs its own total and count.

Misconception to address
Connect this to the previous result named on this slide. Demonstrate the first step again if necessary; there is no requirement for partner work before the explanation.

On this slide
Week 3 introduced values, function inputs and results, conditions and list positions. Now we repeat a calculation across records, then organise those records by keys.

Continue to
Why this week’s tools are needed

## Slide 4 — Why this week’s tools are needed

Why this week’s tools are needed
CML3113, Week 4, slide 4

Explanation to give
Move from one calculation to many records. Lists supply ordered values, loops visit them, dictionaries label fields and CSV files store the observations.

Worked illustration / lecturer answer
For readings 2, 4 and 6, the running total is 2, then 6, then 12. Count 3 gives mean 4.0. A group needs its own total and count.

Misconception to address
Connect this to the previous result named on this slide. Demonstrate the first step again if necessary; there is no requirement for partner work before the explanation.

On this slide
Sensor readings arrive as records in a CSV file. We first learn the Python collections and loops needed to read those records and summarise them.

Continue to
List and index

## Slide 5 — List and index

List and index
CML3113, Week 4, slide 5

Explanation to give
A list is an ordered collection. Draw labelled positions 0, 1 and 2 above three values. The position is the address, not the value stored there. A list may contain repeated values.

Worked illustration / lecturer answer
For [2, 4, 6], position 0 contains 2 and position 2 contains 6. len returns 3. There is no position 3. append(8) adds a new final item and the count becomes 4.

Misconception to address
Square brackets create a list when enclosing values, but select an item when placed after its name. Python counts list positions from zero.

On this slide
List and index: A list holds values in order: [2, 4, 6]. Square brackets select a position. readings[0] selects the first item, 2.

Continue to
A list position starts at zero

## Slide 6 — A list position starts at zero

A list position starts at zero
CML3113, Week 4, slide 6

Explanation to give
A list is an ordered collection. Draw labelled positions 0, 1 and 2 above three values. The position is the address, not the value stored there. A list may contain repeated values.

Worked illustration / lecturer answer
For [2, 4, 6], position 0 contains 2 and position 2 contains 6. len returns 3. There is no position 3. append(8) adds a new final item and the count becomes 4.

Misconception to address
Square brackets create a list when enclosing values, but select an item when placed after its name. Python counts list positions from zero.

On this slide
In [2, 4, 6], position 0 holds 2.

Position 1 holds 4. Position 2 holds 6.

There is no position 3 in this three-item list.

Continue to
Read list operations

## Slide 7 — Read list operations

Read list operations
CML3113, Week 4, slide 7

Explanation to give
Walk through append, replacement and selection separately. append adds a new last item; values[1] = 9 replaces the item at position 1; values[1] retrieves it.

Worked illustration / lecturer answer
Starting with [2, 4], append(6) gives [2, 4, 6]. Assigning values[1] = 9 then gives [2, 9, 6], still three items.

Misconception to address
append changes the list and returns None. Do not write values = values.append(6), which would replace the list name with None.

On this slide
append and len: readings.append(8) adds 8 to the end of the list. len(readings) counts its items. The dot selects an operation belonging to that object; parentheses call it.
Slice: readings[1:3] selects positions 1 and 2. The stop position 3 is excluded. A slice produces a new list; it does not remove items from the original.

Continue to
A list stores items in order

## Slide 8 — A list stores items in order

A list stores items in order
CML3113, Week 4, slide 8

Explanation to give
A list is an ordered collection. Draw labelled positions 0, 1 and 2 above three values. The position is the address, not the value stored there. A list may contain repeated values.

Worked illustration / lecturer answer
For [2, 4, 6], position 0 contains 2 and position 2 contains 6. len returns 3. There is no position 3. append(8) adds a new final item and the count becomes 4.

Misconception to address
Square brackets create a list when enclosing values, but select an item when placed after its name. Python counts list positions from zero.

Read the displayed code line by line
readings = [2, 4, 6]
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

print(readings[0])
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

readings.append(8)
Evaluate the argument and add it as one new item at the end of this list.

print(len(readings))
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

print(readings[1:3])
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
[] builds a list. Positions start at zero. The slice stops before position 3.

Continue to
Trace the list changes

## Slide 9 — Trace the list changes

Trace the list changes
CML3113, Week 4, slide 9

Explanation to give
A list is an ordered collection. Draw labelled positions 0, 1 and 2 above three values. The position is the address, not the value stored there. A list may contain repeated values.

Worked illustration / lecturer answer
For [2, 4, 6], position 0 contains 2 and position 2 contains 6. len returns 3. There is no position 3. append(8) adds a new final item and the count becomes 4.

Misconception to address
Square brackets create a list when enclosing values, but select an item when placed after its name. Python counts list positions from zero.

On this slide
Instruction | List afterwards | Displayed output
readings = [2, 4, 6] | [2, 4, 6] | Nothing yet
print(readings[0]) | [2, 4, 6] | 2
readings.append(8) | [2, 4, 6, 8] | Nothing yet
print(readings[1:3]) | [2, 4, 6, 8] | [4, 6]
len reports 4 after append. A slice excludes its stop position and leaves the original list intact.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
A loop repeats instructions

## Slide 10 — A loop repeats instructions

A loop repeats instructions
CML3113, Week 4, slide 10

Explanation to give
Read for item in values as “take one value, call it item, execute the indented body, then take the next value”. The loop name temporarily refers to the current item.

Worked illustration / lecturer answer
For values [2, 4, 6], print(item) produces 2, then 4, then 6. With count initially zero and one increment per visit, the final count is 3.

Misconception to address
The loop variable does not refer to the whole list. A statement after the indentation ends runs after the loop, not once per item.

On this slide
A loop runs a block more than once. One execution of the block is called an iteration.

for takes one item at a time from a collection. Use it when each item needs the same action.

while repeats while a condition stays True. Use it when a condition controls repetition.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Read every part of a for header

## Slide 11 — Read every part of a for header

Read every part of a for header
CML3113, Week 4, slide 11

Explanation to give
Read for item in values as “take one value, call it item, execute the indented body, then take the next value”. The loop name temporarily refers to the current item.

Worked illustration / lecturer answer
For values [2, 4, 6], print(item) produces 2, then 4, then 6. With count initially zero and one increment per visit, the final count is 3.

Misconception to address
The loop variable does not refer to the whole list. A statement after the indentation ends runs after the loop, not once per item.

On this slide
In for reading in readings:, for introduces repetition, reading names the current item, and readings is the collection to visit.

in connects the current-item name to that collection. The colon begins the loop body. Four spaces mark each instruction that repeats.

reading is a name we choose; it is assigned the next item automatically. It is not the same name as readings. After the last item, execution leaves the loop.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Visit each item without calculating

## Slide 12 — Visit each item without calculating

Visit each item without calculating
CML3113, Week 4, slide 12

Explanation to give
Read for item in values as “take one value, call it item, execute the indented body, then take the next value”. The loop name temporarily refers to the current item.

Worked illustration / lecturer answer
For values [2, 4, 6], print(item) produces 2, then 4, then 6. With count initially zero and one increment per visit, the final count is 3.

Misconception to address
The loop variable does not refer to the whole list. A statement after the indentation ends runs after the loop, not once per item.

Read the displayed code line by line
readings = [2, 4, 6]
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

for reading in readings:
Take each item or pair in turn, assign the loop name(s), and repeat the indented body.

print(reading)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

print("finished")
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Output: 2; 4; 6; finished

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Trace the for loop item by item

## Slide 13 — Trace the for loop item by item

Trace the for loop item by item
CML3113, Week 4, slide 13

Explanation to give
Read for item in values as “take one value, call it item, execute the indented body, then take the next value”. The loop name temporarily refers to the current item.

Worked illustration / lecturer answer
For values [2, 4, 6], print(item) produces 2, then 4, then 6. With count initially zero and one increment per visit, the final count is 3.

Misconception to address
The loop variable does not refer to the whole list. A statement after the indentation ends runs after the loop, not once per item.

On this slide
Step | Current reading | Action
First item | 2 | Print 2
Second item | 4 | Print 4
Third item | 6 | Print 6
No items left | No new item | Leave loop; print finished
An empty list runs the body zero times. It still reaches the outside line.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Updating a counter inside a loop

## Slide 14 — Updating a counter inside a loop

Updating a counter inside a loop
CML3113, Week 4, slide 14

Explanation to give
Read the right-hand occurrence of the name as its old value. Calculate the new value, then replace the old association. This is why an update works in programming even though count = count + 1 is not an algebraic equality.

Worked illustration / lecturer answer
Start at count = 2. The update computes 2 + 1 and count becomes 3. Another execution of the update gives 4. Re-executing the initialisation first returns the sequence to 2, then 3.

Misconception to address
Initialise a running counter before the loop. Resetting it inside the loop throws away earlier progress.

On this slide
A counter records how many times an event happens. Set count = 0 before the loop, then count = count + 1 inside it.

count += 1 is a shorter spelling for that numeric update. Similarly, total += reading means total = total + reading.

The initial value belongs outside the loop. Resetting count to zero inside every iteration loses the earlier count.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Count the visited items

## Slide 15 — Count the visited items

Count the visited items
CML3113, Week 4, slide 15

Explanation to give
Read for item in values as “take one value, call it item, execute the indented body, then take the next value”. The loop name temporarily refers to the current item.

Worked illustration / lecturer answer
For values [2, 4, 6], print(item) produces 2, then 4, then 6. With count initially zero and one increment per visit, the final count is 3.

Misconception to address
The loop variable does not refer to the whole list. A statement after the indentation ends runs after the loop, not once per item.

Read the displayed code line by line
count = 0
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

for reading in [2, 4, 6]:
Take each item or pair in turn, assign the loop name(s), and repeat the indented body.

count += 1
Add the right-hand amount to the current stored value, then keep the updated value.

print(count)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Output: 3

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Accumulator

## Slide 16 — Accumulator

Accumulator
CML3113, Week 4, slide 16

Explanation to give
An accumulator keeps the result built so far. Initialise total before the loop, add the current reading during each visit, and calculate the mean only after all readings have been counted.

Worked illustration / lecturer answer
For [2, 4, 6], total changes 0 to 2 to 6 to 12. The count is 3, so the mean is 12 / 3 = 4.0. sum, len, min and max report 12, 3, 2 and 6.

Misconception to address
An empty list has count zero, so dividing by its count fails. The issued task must define the empty-data behaviour; do not silently invent a reading.

On this slide
Accumulator: A running total. Set it to zero before the loop, add inside the loop, and read the final total afterward.

Continue to
A loop repeats an indented block

## Slide 17 — A loop repeats an indented block

A loop repeats an indented block
CML3113, Week 4, slide 17

Explanation to give
Read for item in values as “take one value, call it item, execute the indented body, then take the next value”. The loop name temporarily refers to the current item.

Worked illustration / lecturer answer
For values [2, 4, 6], print(item) produces 2, then 4, then 6. With count initially zero and one increment per visit, the final count is 3.

Misconception to address
The loop variable does not refer to the whole list. A statement after the indentation ends runs after the loop, not once per item.

On this slide
for reading in readings: takes one item at a time.

The colon starts the block. Four spaces show which lines repeat.

A running total must start at zero before the loop.

Continue to
A mean uses a total and a count

## Slide 18 — A mean uses a total and a count

A mean uses a total and a count
CML3113, Week 4, slide 18

Explanation to give
An accumulator keeps the result built so far. Initialise total before the loop, add the current reading during each visit, and calculate the mean only after all readings have been counted.

Worked illustration / lecturer answer
For [2, 4, 6], total changes 0 to 2 to 6 to 12. The count is 3, so the mean is 12 / 3 = 4.0. sum, len, min and max report 12, 3, 2 and 6.

Misconception to address
An empty list has count zero, so dividing by its count fails. The issued task must define the empty-data behaviour; do not silently invent a reading.

On this slide
Start the total at 0. Add 2, then 4, then 6.

The final total is 12. The count is 3.

12 / 3 gives the mean 4. An empty list needs a separate rule.

Continue to
A loop changes the running total

## Slide 19 — A loop changes the running total

A loop changes the running total
CML3113, Week 4, slide 19

Explanation to give
An accumulator keeps the result built so far. Initialise total before the loop, add the current reading during each visit, and calculate the mean only after all readings have been counted.

Worked illustration / lecturer answer
For [2, 4, 6], total changes 0 to 2 to 6 to 12. The count is 3, so the mean is 12 / 3 = 4.0. sum, len, min and max report 12, 3, 2 and 6.

Misconception to address
An empty list has count zero, so dividing by its count fails. The issued task must define the empty-data behaviour; do not silently invent a reading.

On this slide
This illustration uses six separate readings. Next we trace the smaller list [2, 4, 6] using the same running-total rule.

Continue to
Tracing the loop

## Slide 20 — Tracing the loop

Tracing the loop
CML3113, Week 4, slide 20

Explanation to give
An accumulator keeps the result built so far. Initialise total before the loop, add the current reading during each visit, and calculate the mean only after all readings have been counted.

Worked illustration / lecturer answer
For [2, 4, 6], total changes 0 to 2 to 6 to 12. The count is 3, so the mean is 12 / 3 = 4.0. sum, len, min and max report 12, 3, 2 and 6.

Misconception to address
An empty list has count zero, so dividing by its count fails. The issued task must define the empty-data behaviour; do not silently invent a reading.

On this slide
Step | reading | total after addition
Before loop | — | 0
First | 2 | 2
Second | 4 | 6
Third | 6 | 12
There are three readings.

Continue to
Lists loops and records in Python

## Slide 21 — Lists loops and records in Python

Lists loops and records in Python
CML3113, Week 4, slide 21

Explanation to give
An accumulator keeps the result built so far. Initialise total before the loop, add the current reading during each visit, and calculate the mean only after all readings have been counted.

Worked illustration / lecturer answer
For [2, 4, 6], total changes 0 to 2 to 6 to 12. The count is 3, so the mean is 12 / 3 = 4.0. sum, len, min and max report 12, 3, 2 and 6.

Misconception to address
An empty list has count zero, so dividing by its count fails. The issued task must define the empty-data behaviour; do not silently invent a reading.

Read the displayed code line by line
readings = [2, 4, 6]
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

total = 0
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

for reading in readings:
Take each item or pair in turn, assign the loop name(s), and repeat the indented body.

total = total + reading
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

mean = total / len(readings)
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

print(mean)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Read top to bottom. Run the complete example in the matching practice notebook.

Continue to
Lists loops and records results

## Slide 22 — Lists loops and records results

Lists loops and records results
CML3113, Week 4, slide 22

Explanation to give
An accumulator keeps the result built so far. Initialise total before the loop, add the current reading during each visit, and calculate the mean only after all readings have been counted.

Worked illustration / lecturer answer
For [2, 4, 6], total changes 0 to 2 to 6 to 12. The count is 3, so the mean is 12 / 3 = 4.0. sum, len, min and max report 12, 3, 2 and 6.

Misconception to address
An empty list has count zero, so dividing by its count fails. The issued task must define the empty-data behaviour; do not silently invent a reading.

On this slide
4.0

Continue to
The built-in summary functions

## Slide 23 — The built-in summary functions

The built-in summary functions
CML3113, Week 4, slide 23

Explanation to give
An accumulator keeps the result built so far. Initialise total before the loop, add the current reading during each visit, and calculate the mean only after all readings have been counted.

Worked illustration / lecturer answer
For [2, 4, 6], total changes 0 to 2 to 6 to 12. The count is 3, so the mean is 12 / 3 = 4.0. sum, len, min and max report 12, 3, 2 and 6.

Misconception to address
An empty list has count zero, so dividing by its count fails. The issued task must define the empty-data behaviour; do not silently invent a reading.

On this slide
Function | Question it answers | For [2, 4, 6]
len | How many items? | 3
sum | What is their total? | 12
min | Which is smallest? | 2
max | Which is largest? | 6
These functions already exist in Python. min and max need at least one item unless an explicit default is supplied.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Built-in summaries of a list

## Slide 24 — Built-in summaries of a list

Built-in summaries of a list
CML3113, Week 4, slide 24

Explanation to give
An accumulator keeps the result built so far. Initialise total before the loop, add the current reading during each visit, and calculate the mean only after all readings have been counted.

Worked illustration / lecturer answer
For [2, 4, 6], total changes 0 to 2 to 6 to 12. The count is 3, so the mean is 12 / 3 = 4.0. sum, len, min and max report 12, 3, 2 and 6.

Misconception to address
An empty list has count zero, so dividing by its count fails. The issued task must define the empty-data behaviour; do not silently invent a reading.

Read the displayed code line by line
readings = [2, 4, 6]
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

print(sum(readings))
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

print(len(readings))
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

print(min(readings))
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

print(max(readings))
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Output: 12, 3, 2, 6. sum totals; len counts; min and max select the smallest and largest.

Continue to
A while loop checks before each repetition

## Slide 25 — A while loop checks before each repetition

A while loop checks before each repetition
CML3113, Week 4, slide 25

Explanation to give
while tests a condition before each iteration. Unlike for over a fixed list, it needs a route that eventually makes the condition False. Trace both the test and the state update.

Worked illustration / lecturer answer
With count = 0 and while count < 3, print then increment yields 0, 1 and 2. The next test sees count 3 and stops before printing it.

Misconception to address
If count is never updated, the condition stays True. Interrupt a stuck runtime rather than waiting indefinitely, then identify the missing update.

On this slide
while count < 3: tests the condition before entering its indented block. True enters the block; False skips it and continues after the loop.

At the end of the body, return to the condition and test again. Unlike for, while does not automatically move to the next list item.

Something must make the condition become False, or the loop may continue indefinitely. In our example, count increases on every iteration.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
A while loop with a stopping condition

## Slide 26 — A while loop with a stopping condition

A while loop with a stopping condition
CML3113, Week 4, slide 26

Explanation to give
while tests a condition before each iteration. Unlike for over a fixed list, it needs a route that eventually makes the condition False. Trace both the test and the state update.

Worked illustration / lecturer answer
With count = 0 and while count < 3, print then increment yields 0, 1 and 2. The next test sees count 3 and stops before printing it.

Misconception to address
If count is never updated, the condition stays True. Interrupt a stuck runtime rather than waiting indefinitely, then identify the missing update.

Read the displayed code line by line
count = 0
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

while count < 3:
Test this condition before each repetition. Stop when it becomes False.

print(count)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

count = count + 1
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

print("finished")
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Output: 0; 1; 2; finished

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Trace the while condition and update

## Slide 27 — Trace the while condition and update

Trace the while condition and update
CML3113, Week 4, slide 27

Explanation to give
while tests a condition before each iteration. Unlike for over a fixed list, it needs a route that eventually makes the condition False. Trace both the test and the state update.

Worked illustration / lecturer answer
With count = 0 and while count < 3, print then increment yields 0, 1 and 2. The next test sees count 3 and stops before printing it.

Misconception to address
If count is never updated, the condition stays True. Interrupt a stuck runtime rather than waiting indefinitely, then identify the missing update.

On this slide
count before test | count < 3 | Body and next count
0 | True | Print 0; update to 1
1 | True | Print 1; update to 2
2 | True | Print 2; update to 3
3 | False | Skip body; print finished
If count starts at 3, the body runs zero times. The condition is tested first.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Preventing an endless loop

## Slide 28 — Preventing an endless loop

Preventing an endless loop
CML3113, Week 4, slide 28

Explanation to give
while tests a condition before each iteration. Unlike for over a fixed list, it needs a route that eventually makes the condition False. Trace both the test and the state update.

Worked illustration / lecturer answer
With count = 0 and while count < 3, print then increment yields 0, 1 and 2. The next test sees count 3 and stops before printing it.

Misconception to address
If count is never updated, the condition stays True. Interrupt a stuck runtime rather than waiting indefinitely, then identify the missing update.

On this slide
If the update is missing, count remains 0. The question 0 < 3 stays True, so the body keeps running.

In Colab, click the running cell’s stop button or use Runtime → Interrupt execution. Fix the condition or update before running again.

Do not run an intentionally endless example. Trace the unchanged value on the slide to see why it would fail.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Choosing if for or while

## Slide 29 — Choosing if for or while

Choosing if for or while
CML3113, Week 4, slide 29

Explanation to give
if makes a decision once, for visits members of a collection, and while repeats while a condition remains True. Choose the construct by the job before writing syntax.

Worked illustration / lecturer answer
For three recorded temperatures, for visits all three. Inside it, if reading > 30 decides whether to count that observation. while is appropriate when repetition depends on a changing condition.

Misconception to address
A loop and a condition can appear together. They answer different questions: how often to repeat, and whether this item qualifies.

On this slide
Construct | Purpose | When it finishes
if / else | Choose a path once | After the chosen block
for | Visit supplied items | When items are exhausted
while | Repeat while True | When condition becomes False
A condition alone does not imply repetition: if tests once; while tests again after its body.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
range supplies a sequence of integers

## Slide 30 — range supplies a sequence of integers

range supplies a sequence of integers
CML3113, Week 4, slide 30

Explanation to give
range supplies integers in order. Its stop value is excluded. Say the sequence out loud before executing the loop so the boundary is visible.

Worked illustration / lecturer answer
range(3) supplies 0, 1, 2. range(1, 4) supplies 1, 2, 3. Both provide three integers but different starting points.

Misconception to address
The stop value itself is not visited. range counts steps and does not automatically retrieve values from a separate list.

On this slide
range(3) supplies 0, 1 and 2. The stop value 3 is excluded. range(1, 4) supplies 1, 2 and 3.

Use range with for when a numbered repetition is useful. The loop still works by taking the next supplied item.

range(0, 6, 2) uses a step of 2 and supplies 0, 2, 4. A step is the change between successive numbers; it cannot be zero.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Repeat with range

## Slide 31 — Repeat with range

Repeat with range
CML3113, Week 4, slide 31

Explanation to give
range supplies integers in order. Its stop value is excluded. Say the sequence out loud before executing the loop so the boundary is visible.

Worked illustration / lecturer answer
range(3) supplies 0, 1, 2. range(1, 4) supplies 1, 2, 3. Both provide three integers but different starting points.

Misconception to address
The stop value itself is not visited. range counts steps and does not automatically retrieve values from a separate list.

Read the displayed code line by line
for attempt in range(1, 4):
Take each item or pair in turn, assign the loop name(s), and repeat the indented body.

print(attempt)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Output: 1; 2; 3

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
continue and break change a loop’s path

## Slide 32 — continue and break change a loop’s path

continue and break change a loop’s path
CML3113, Week 4, slide 32

Explanation to give
continue ends the current iteration and proceeds to the next item. break ends the nearest enclosing loop completely. Trace the same data twice to show the distinction.

Worked illustration / lecturer answer
Over [1, 2, 3], skipping 2 with continue still allows 3 to be processed. Breaking when 2 is reached prevents both 2's remaining work and the later visit to 3.

Misconception to address
Statements below continue or break in that iteration are skipped. Neither word means “restart the whole notebook”.

On this slide
continue skips the rest of the current iteration, then starts the next iteration. It does not end the whole loop.

break exits the nearest enclosing loop immediately. Execution resumes after that loop.

Put the condition inside the loop with four spaces. Its action is inside that condition with eight spaces: an indented block inside another block.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Skip one item using continue

## Slide 33 — Skip one item using continue

Skip one item using continue
CML3113, Week 4, slide 33

Explanation to give
continue ends the current iteration and proceeds to the next item. break ends the nearest enclosing loop completely. Trace the same data twice to show the distinction.

Worked illustration / lecturer answer
Over [1, 2, 3], skipping 2 with continue still allows 3 to be processed. Breaking when 2 is reached prevents both 2's remaining work and the later visit to 3.

Misconception to address
Statements below continue or break in that iteration are skipped. Neither word means “restart the whole notebook”.

Read the displayed code line by line
for reading in [2, -1, 6]:
Take each item or pair in turn, assign the loop name(s), and repeat the indented body.

if reading < 0:
Evaluate this yes/no condition. Execute its indented body only on the matching path.

continue
Skip the rest of this iteration and proceed to the next item.

print(reading)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Output: 2; 6

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Stop at one item using break

## Slide 34 — Stop at one item using break

Stop at one item using break
CML3113, Week 4, slide 34

Explanation to give
continue ends the current iteration and proceeds to the next item. break ends the nearest enclosing loop completely. Trace the same data twice to show the distinction.

Worked illustration / lecturer answer
Over [1, 2, 3], skipping 2 with continue still allows 3 to be processed. Breaking when 2 is reached prevents both 2's remaining work and the later visit to 3.

Misconception to address
Statements below continue or break in that iteration are skipped. Neither word means “restart the whole notebook”.

Read the displayed code line by line
for reading in [2, -1, 6]:
Take each item or pair in turn, assign the loop name(s), and repeat the indented body.

if reading < 0:
Evaluate this yes/no condition. Execute its indented body only on the matching path.

break
Exit this loop immediately; later items will not be visited.

print(reading)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Output: 2

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Trace the two loop controls

## Slide 35 — Trace the two loop controls

Trace the two loop controls
CML3113, Week 4, slide 35

Explanation to give
continue ends the current iteration and proceeds to the next item. break ends the nearest enclosing loop completely. Trace the same data twice to show the distinction.

Worked illustration / lecturer answer
Over [1, 2, 3], skipping 2 with continue still allows 3 to be processed. Breaking when 2 is reached prevents both 2's remaining work and the later visit to 3.

Misconception to address
Statements below continue or break in that iteration are skipped. Neither word means “restart the whole notebook”.

On this slide
Input | continue version | break version
2 | Print 2 | Print 2
-1 | Skip its print | Exit loop
6 | Print 6 | Never visited
Use continue only when skipping is justified by the stated data rule; do not silently discard evidence.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
A dictionary is a record with named fields

## Slide 36 — A dictionary is a record with named fields

A dictionary is a record with named fields
CML3113, Week 4, slide 36

Explanation to give
A dictionary labels fields with keys. A list organises records by position. Explain each lookup in a nested expression separately rather than saying it all at once.

Worked illustration / lecturer answer
records[0]["reading"] first selects the first record, then finds its reading field. In {"unit": "A", "reading": 4}, the key reading retrieves 4 regardless of its visual position.

Misconception to address
Using a missing key with square brackets raises KeyError. get("missing", 0) uses 0 only if the key is absent, not when its existing value is None.

On this slide
record = {"unit": "A", "reading": 4} stores two key–value pairs. Keys name fields; values hold the information.

Braces enclose the dictionary. A colon separates each key from its value and a comma separates pairs. Each key is unique.

record["reading"] returns 4. Unlike a list position, "reading" names the field we want.

Continue to
A missing dictionary key and get

## Slide 37 — A missing dictionary key and get

A missing dictionary key and get
CML3113, Week 4, slide 37

Explanation to give
A dictionary labels fields with keys. A list organises records by position. Explain each lookup in a nested expression separately rather than saying it all at once.

Worked illustration / lecturer answer
records[0]["reading"] first selects the first record, then finds its reading field. In {"unit": "A", "reading": 4}, the key reading retrieves 4 regardless of its visual position.

Misconception to address
Using a missing key with square brackets raises KeyError. get("missing", 0) uses 0 only if the key is absent, not when its existing value is None.

On this slide
record["reading"] requests a known field. If that key does not exist, square-bracket lookup raises KeyError.

record.get("missing", 0) asks for that key with a fallback: return 0 if it is absent. This does not add a new key.

The second input is the fallback value. Use a fallback only when the task defines what missing information should mean.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Reading and updating a dictionary

## Slide 38 — Reading and updating a dictionary

Reading and updating a dictionary
CML3113, Week 4, slide 38

Explanation to give
A dictionary labels fields with keys. A list organises records by position. Explain each lookup in a nested expression separately rather than saying it all at once.

Worked illustration / lecturer answer
records[0]["reading"] first selects the first record, then finds its reading field. In {"unit": "A", "reading": 4}, the key reading retrieves 4 regardless of its visual position.

Misconception to address
Using a missing key with square brackets raises KeyError. get("missing", 0) uses 0 only if the key is absent, not when its existing value is None.

Read the displayed code line by line
record = {"unit": "A", "reading": 4}
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

print(record["reading"])
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

record["reading"] = 6
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

print(record["reading"])
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

print(record.get("missing", 0))
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Output: 4, then 6, then 0. get uses the fallback only when that key is absent.

Continue to
Tuples and unpacking

## Slide 39 — Tuples and unpacking

Tuples and unpacking
CML3113, Week 4, slide 39

Explanation to give
A tuple keeps positions that cannot be reassigned. Unpacking assigns the items to several names in the same order. Show the number of items and names before running it.

Worked illustration / lecturer answer
point = (2, 3), then x, y = point gives x = 2 and y = 3. The original tuple still exists. record.items() similarly supplies key/value pairs to two loop names.

Misconception to address
Two names need two items. A tuple containing a mutable object does not freeze that object's contents.

On this slide
A tuple stores items in order. point = (2, 3) stores two coordinates; point[0] is 2. You cannot reassign point[0].

x, y = point gives the first item to x and the second to y. This is unpacking; the number of names must match the number of items.

A tuple prevents replacing its positions. It does not freeze the contents of a mutable object stored inside it.

Continue to
Unpacking a pair

## Slide 40 — Unpacking a pair

Unpacking a pair
CML3113, Week 4, slide 40

Explanation to give
A tuple keeps positions that cannot be reassigned. Unpacking assigns the items to several names in the same order. Show the number of items and names before running it.

Worked illustration / lecturer answer
point = (2, 3), then x, y = point gives x = 2 and y = 3. The original tuple still exists. record.items() similarly supplies key/value pairs to two loop names.

Misconception to address
Two names need two items. A tuple containing a mutable object does not freeze that object's contents.

Read the displayed code line by line
point = (2, 3)
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

x, y = point
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

print(x)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

print(y)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Output: 2, then 3.

Continue to
A set remembers distinct items

## Slide 41 — A set remembers distinct items

A set remembers distinct items
CML3113, Week 4, slide 41

Explanation to give
A set answers whether an item is present and stores each distinct item once. It has no numeric positions. Use it to remember IDs already encountered.

Worked illustration / lecturer answer
Add "A" twice to an empty set: len is still 1. "A" in seen is True and "B" in seen is False. Adding "B" makes the count 2.

Misconception to address
{} creates an empty dictionary. Use set() for an empty set. Sets are unsuitable when duplicate measurements or a particular order must be retained.

On this slide
A set is useful when the question is “Have we seen this ID?” It keeps one instance of each distinct item.

seen = set() creates an empty set. seen.add("A") adds an item. "A" in seen asks whether it is present.

Do not use a set when position or repeated readings matter. Sets cannot be indexed. {} creates an empty dictionary, not an empty set.

Continue to
Set membership and repeated IDs

## Slide 42 — Set membership and repeated IDs

Set membership and repeated IDs
CML3113, Week 4, slide 42

Explanation to give
A set answers whether an item is present and stores each distinct item once. It has no numeric positions. Use it to remember IDs already encountered.

Worked illustration / lecturer answer
Add "A" twice to an empty set: len is still 1. "A" in seen is True and "B" in seen is False. Adding "B" makes the count 2.

Misconception to address
{} creates an empty dictionary. Use set() for an empty set. Sets are unsuitable when duplicate measurements or a particular order must be retained.

Read the displayed code line by line
seen = set()
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

seen.add("A")
Remember this item in the set. Adding the same item again does not create a duplicate.

seen.add("A")
Remember this item in the set. Adding the same item again does not create a duplicate.

print(len(seen))
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

print("A" in seen)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

print("B" in seen)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Output: 1, True, False. Adding the same ID twice keeps one distinct ID.

Continue to
How the four collections differ

## Slide 43 — How the four collections differ

How the four collections differ
CML3113, Week 4, slide 43

Explanation to give
Compare the access rule for each collection. Lists and tuples use positions; dictionaries use keys; sets answer membership questions. Lists can change their items, while tuple positions cannot be reassigned.

Worked illustration / lecturer answer
For readings use an ordered list. For a record with unit and reading fields use a dictionary. For a coordinate pair use a tuple. For IDs already seen use a set.

Misconception to address
A set cannot be indexed. Dictionary keys are unique, but values may repeat. {} is an empty dictionary; set() is an empty set.

On this slide
Collection | Find an item by | Repeats / changes
list | Position: values[0] | Repeats allowed; items change
dict | Key: record["reading"] | Keys unique; values change
tuple | Position: point[0] | Repeats allowed; positions fixed
set | Membership: "A" in seen | Distinct items; add or remove
Choose by the question: ordered readings, named fields, fixed positions, or distinct IDs.

Continue to
Dictionary items and two loop names

## Slide 44 — Dictionary items and two loop names

Dictionary items and two loop names
CML3113, Week 4, slide 44

Explanation to give
A dictionary labels fields with keys. A list organises records by position. Explain each lookup in a nested expression separately rather than saying it all at once.

Worked illustration / lecturer answer
records[0]["reading"] first selects the first record, then finds its reading field. In {"unit": "A", "reading": 4}, the key reading retrieves 4 regardless of its visual position.

Misconception to address
Using a missing key with square brackets raises KeyError. get("missing", 0) uses 0 only if the key is absent, not when its existing value is None.

On this slide
record.items() provides each key with its value as a pair. The loop unpacks each pair into the names key and value.

for key, value in record.items(): repeats the indented body for each field. Use .items() when both the label and its value are needed.

Continue to
Looping through named fields

## Slide 45 — Looping through named fields

Looping through named fields
CML3113, Week 4, slide 45

Explanation to give
A dictionary labels fields with keys. A list organises records by position. Explain each lookup in a nested expression separately rather than saying it all at once.

Worked illustration / lecturer answer
records[0]["reading"] first selects the first record, then finds its reading field. In {"unit": "A", "reading": 4}, the key reading retrieves 4 regardless of its visual position.

Misconception to address
Using a missing key with square brackets raises KeyError. get("missing", 0) uses 0 only if the key is absent, not when its existing value is None.

Read the displayed code line by line
record = {"unit": "A", "reading": 6}
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

for key, value in record.items():
Take each item or pair in turn, assign the loop name(s), and repeat the indented body.

print(key, value)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Output: unit A, then reading 6. The dictionary preserves insertion order.

Continue to
A position and a key find different things

## Slide 46 — A position and a key find different things

A position and a key find different things
CML3113, Week 4, slide 46

Explanation to give
A dictionary labels fields with keys. A list organises records by position. Explain each lookup in a nested expression separately rather than saying it all at once.

Worked illustration / lecturer answer
records[0]["reading"] first selects the first record, then finds its reading field. In {"unit": "A", "reading": 4}, the key reading retrieves 4 regardless of its visual position.

Misconception to address
Using a missing key with square brackets raises KeyError. get("missing", 0) uses 0 only if the key is absent, not when its existing value is None.

On this slide
Both examples return 4. Explain how each lookup finds it.

Continue to
CSV and header

## Slide 47 — CSV and header

CSV and header
CML3113, Week 4, slide 47

Explanation to give
A CSV file stores rows as text separated into fields. Its header provides column names. csv.DictReader turns each data row into a dictionary using those names; numeric-looking cells initially remain strings.

Worked illustration / lecturer answer
A CSV row with reading 2.5 yields the text "2.5". float converts that field to the number 2.5. with open(...) keeps the file available inside the indented block and closes it afterwards.

Misconception to address
Use the exact file from the current week's package and its exact header. A correct formula cannot repair a wrong file, misspelled column or wrong unit.

On this slide
CSV and header: CSV means comma-separated values. One line usually represents one record; a header names the columns. CSV numbers arrive as text and may need float conversion.

Continue to
One record at a time

## Slide 48 — One record at a time

One record at a time
CML3113, Week 4, slide 48

Explanation to give
A CSV file stores rows as text separated into fields. Its header provides column names. csv.DictReader turns each data row into a dictionary using those names; numeric-looking cells initially remain strings.

Worked illustration / lecturer answer
A CSV row with reading 2.5 yields the text "2.5". float converts that field to the number 2.5. with open(...) keeps the file available inside the indented block and closes it afterwards.

Misconception to address
Use the exact file from the current week's package and its exact header. A correct formula cannot repair a wrong file, misspelled column or wrong unit.

On this slide
A CSV is a text table with a header row.

DictReader uses that header for dictionary keys.

CSV cells begin as text, even when they look numeric.

float("2.5") converts text into the number 2.5.

Continue to
A CSV file has a header and text values

## Slide 49 — A CSV file has a header and text values

A CSV file has a header and text values
CML3113, Week 4, slide 49

Explanation to give
A CSV file stores rows as text separated into fields. Its header provides column names. csv.DictReader turns each data row into a dictionary using those names; numeric-looking cells initially remain strings.

Worked illustration / lecturer answer
A CSV row with reading 2.5 yields the text "2.5". float converts that field to the number 2.5. with open(...) keeps the file available inside the indented block and closes it afterwards.

Misconception to address
Use the exact file from the current week's package and its exact header. A correct formula cannot repair a wrong file, misspelled column or wrong unit.

On this slide
CSV line | Dictionary meaning
unit,reading | Two field names
A,2.5 | {"unit": "A", "reading": "2.5"}
B, | {"unit": "B", "reading": ""}
An empty field is empty text. Check the task’s rule before converting it.

Continue to
A CSV row becomes a dictionary

## Slide 50 — A CSV row becomes a dictionary

A CSV row becomes a dictionary
CML3113, Week 4, slide 50

Explanation to give
A dictionary labels fields with keys. A list organises records by position. Explain each lookup in a nested expression separately rather than saying it all at once.

Worked illustration / lecturer answer
records[0]["reading"] first selects the first record, then finds its reading field. In {"unit": "A", "reading": 4}, the key reading retrieves 4 regardless of its visual position.

Misconception to address
Using a missing key with square brackets raises KeyError. get("missing", 0) uses 0 only if the key is absent, not when its existing value is None.

On this slide
The header gives field names, such as unit and reading.

csv.DictReader returns one dictionary for each data row.

The value "2.5" starts as text. float("2.5") makes the number 2.5.

Continue to
with and import

## Slide 51 — with and import

with and import
CML3113, Week 4, slide 51

Explanation to give
A CSV file stores rows as text separated into fields. Its header provides column names. csv.DictReader turns each data row into a dictionary using those names; numeric-looking cells initially remain strings.

Worked illustration / lecturer answer
A CSV row with reading 2.5 yields the text "2.5". float converts that field to the number 2.5. with open(...) keeps the file available inside the indented block and closes it afterwards.

Misconception to address
Use the exact file from the current week's package and its exact header. A correct formula cannot repair a wrong file, misspelled column or wrong unit.

On this slide
with and import: import makes library tools available. with open(...) opens a file for a block and closes it afterward. A filename must match an existing file in the working folder.

Continue to
Your cohort data

## Slide 52 — Your cohort data

Your cohort data
CML3113, Week 4, slide 52

Explanation to give
Use fluid moving through a system as the physical reference. Volume in litres divided by elapsed seconds gives a flow rate in L/s. Density and depth belong to a later pressure calculation.

Worked illustration / lecturer answer
Show drill_shift_log.csv in the runtime Files panel. The Week 2 file has four rows for setup; Week 4 uses its own 300-row file. Inspect the header to locate this cohort’s reading field and group field.

Misconception to address
Flow rate and pressure are different physical quantities. Keep litres/seconds separate from the SI units specified for mud_pressure.

On this slide
drill_shift_log.csv

Summarise rate_of_penetration (m/hour); group by bit_type.

Read the issued task’s blank-value and threshold rules before calculating.

Continue to
Read the supplied CSV in four steps

## Slide 53 — Read the supplied CSV in four steps

Read the supplied CSV in four steps
CML3113, Week 4, slide 53

Explanation to give
A CSV file stores rows as text separated into fields. Its header provides column names. csv.DictReader turns each data row into a dictionary using those names; numeric-looking cells initially remain strings.

Worked illustration / lecturer answer
A CSV row with reading 2.5 yields the text "2.5". float converts that field to the number 2.5. with open(...) keeps the file available inside the indented block and closes it afterwards.

Misconception to address
Use the exact file from the current week's package and its exact header. A correct formula cannot repair a wrong file, misspelled column or wrong unit.

On this slide
Place drill_shift_log.csv beside the notebook, or upload it in Colab’s Files panel.

import csv loads the CSV tools. newline="" lets the reader handle line endings. DictReader uses the header as dictionary keys.

list(...) collects the rows while the file is open. We inspect the first row and the count; the later assignment calculations are your work.

Continue to
What with open as source does

## Slide 54 — What with open as source does

What with open as source does
CML3113, Week 4, slide 54

Explanation to give
A CSV file stores rows as text separated into fields. Its header provides column names. csv.DictReader turns each data row into a dictionary using those names; numeric-looking cells initially remain strings.

Worked illustration / lecturer answer
A CSV row with reading 2.5 yields the text "2.5". float converts that field to the number 2.5. with open(...) keeps the file available inside the indented block and closes it afterwards.

Misconception to address
Use the exact file from the current week's package and its exact header. A correct formula cannot repair a wrong file, misspelled column or wrong unit.

On this slide
open("file.csv", newline="") opens a text file for reading. Use the actual supplied filename, including its .csv extension.

with manages the open file. as source gives that file object a name. Indented lines use it while it is open; leaving the block closes it.

csv.DictReader(source) reads rows using the header names as keys. list(...) collects those rows into memory before the file closes.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Open a real CSV and inspect its first row

## Slide 55 — Open a real CSV and inspect its first row

Open a real CSV and inspect its first row
CML3113, Week 4, slide 55

Explanation to give
A CSV file stores rows as text separated into fields. Its header provides column names. csv.DictReader turns each data row into a dictionary using those names; numeric-looking cells initially remain strings.

Worked illustration / lecturer answer
A CSV row with reading 2.5 yields the text "2.5". float converts that field to the number 2.5. with open(...) keeps the file available inside the indented block and closes it afterwards.

Misconception to address
Use the exact file from the current week's package and its exact header. A correct formula cannot repair a wrong file, misspelled column or wrong unit.

Read the displayed code line by line
import csv
Load this library. An alias after as is the shorter name used below.

with open("drill_shift_log.csv", newline="") as source:
Open the named resource for the indented block and close it when leaving the block.

rows = list(csv.DictReader(source))
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

print(rows[0])
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

print(len(rows))
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Read the actual keys and text values. Check the uploaded filename if Python reports FileNotFoundError.

Continue to
A list of dictionaries

## Slide 56 — A list of dictionaries

A list of dictionaries
CML3113, Week 4, slide 56

Explanation to give
A dictionary labels fields with keys. A list organises records by position. Explain each lookup in a nested expression separately rather than saying it all at once.

Worked illustration / lecturer answer
records[0]["reading"] first selects the first record, then finds its reading field. In {"unit": "A", "reading": 4}, the key reading retrieves 4 regardless of its visual position.

Misconception to address
Using a missing key with square brackets raises KeyError. get("missing", 0) uses 0 only if the key is absent, not when its existing value is None.

On this slide
A record holds named fields for one observation. A list of records holds several observations in order.

records[0] selects the first dictionary. records[0]["reading"] then selects that dictionary’s reading field.

for row in records takes one dictionary at a time. row["reading"] retrieves that observation’s field; float converts numeric text when needed.

Continue to
A record and a growing list

## Slide 57 — A record and a growing list

A record and a growing list
CML3113, Week 4, slide 57

Explanation to give
A dictionary labels fields with keys. A list organises records by position. Explain each lookup in a nested expression separately rather than saying it all at once.

Worked illustration / lecturer answer
records[0]["reading"] first selects the first record, then finds its reading field. In {"unit": "A", "reading": 4}, the key reading retrieves 4 regardless of its visual position.

Misconception to address
Using a missing key with square brackets raises KeyError. get("missing", 0) uses 0 only if the key is absent, not when its existing value is None.

On this slide
Braces pair a key with its value. append adds one value to the end of a list.

The same pattern works after reading a CSV row.

Continue to
A record and a growing list in Python

## Slide 58 — A record and a growing list in Python

A record and a growing list in Python
CML3113, Week 4, slide 58

Explanation to give
A dictionary labels fields with keys. A list organises records by position. Explain each lookup in a nested expression separately rather than saying it all at once.

Worked illustration / lecturer answer
records[0]["reading"] first selects the first record, then finds its reading field. In {"unit": "A", "reading": 4}, the key reading retrieves 4 regardless of its visual position.

Misconception to address
Using a missing key with square brackets raises KeyError. get("missing", 0) uses 0 only if the key is absent, not when its existing value is None.

Read the displayed code line by line
records = [{"sensor": "A", "reading": "2.5"},
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

{"sensor": "B", "reading": "3.5"}]
This line continues the surrounding expression or block; read it together with the preceding line rather than running it alone.

values = []
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

for row in records:
Take each item or pair in turn, assign the loop name(s), and repeat the indented body.

values.append(float(row["reading"]))
Evaluate the argument and add it as one new item at the end of this list.

print(values)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Read top to bottom. Run the complete example in the matching practice notebook.

Continue to
Skip a blank before converting text

## Slide 59 — Skip a blank before converting text

Skip a blank before converting text
CML3113, Week 4, slide 59

Explanation to give
Inspect a field before converting it. A blank string represents no recorded number here. Converting that blank with float raises ValueError, so handle the missing case explicitly.

Worked illustration / lecturer answer
For text values ["2", "", "4"], skip the blank and convert the other two to 2.0 and 4.0. Their mean is 3.0 using count 2, not count 3.

Misconception to address
Do not convert blank to zero merely to silence an error. Zero is a measurement. Catch only the expected conversion failure so unrelated coding errors remain visible.

On this slide
An empty text field is "". The comparison != means “not equal to”. Only convert a value after the blank check passes.

In this example, values records valid numbers only. Its length is the valid count; the group summaries must use the same valid-record policy.

Continue to
Collect only the recorded numbers

## Slide 60 — Collect only the recorded numbers

Collect only the recorded numbers
CML3113, Week 4, slide 60

Explanation to give
Inspect a field before converting it. A blank string represents no recorded number here. Converting that blank with float raises ValueError, so handle the missing case explicitly.

Worked illustration / lecturer answer
For text values ["2", "", "4"], skip the blank and convert the other two to 2.0 and 4.0. Their mean is 3.0 using count 2, not count 3.

Misconception to address
Do not convert blank to zero merely to silence an error. Zero is a measurement. Catch only the expected conversion failure so unrelated coding errors remain visible.

Read the displayed code line by line
text_values = ["2.5", "", "3.5"]
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

values = []
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

for text in text_values:
Take each item or pair in turn, assign the loop name(s), and repeat the indented body.

if text != "":
Evaluate this yes/no condition. Execute its indented body only on the matching path.

values.append(float(text))
Evaluate the argument and add it as one new item at the end of this list.

print(len(values), values)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Expected: 2 [2.5, 3.5]. A blank is missing, not a recorded zero.

Continue to
Membership in a dictionary

## Slide 61 — Membership in a dictionary

Membership in a dictionary
CML3113, Week 4, slide 61

Explanation to give
A dictionary labels fields with keys. A list organises records by position. Explain each lookup in a nested expression separately rather than saying it all at once.

Worked illustration / lecturer answer
records[0]["reading"] first selects the first record, then finds its reading field. In {"unit": "A", "reading": 4}, the key reading retrieves 4 regardless of its visual position.

Misconception to address
Using a missing key with square brackets raises KeyError. get("missing", 0) uses 0 only if the key is absent, not when its existing value is None.

On this slide
group in totals asks whether group is already a dictionary key. group not in totals asks whether that key is absent.

Before adding to a new group, create its total with totals[group] = 0. Then add the current record’s reading.

The outer for visits records. The inner if runs only for a new group. The addition after the if runs for every record.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Summaries for separate groups

## Slide 62 — Summaries for separate groups

Summaries for separate groups
CML3113, Week 4, slide 62

Explanation to give
Each group needs its own total and count. Identify the group label before updating its stored summary. A total divided by the overall count gives the wrong group mean.

Worked illustration / lecturer answer
Records A:2, A:4 and B:10 give A total 6 and count 2, so A mean 3. B total 10 and count 1 give mean 10.

Misconception to address
Start a new group's total and count once, when first encountered. Resetting them on every record loses earlier observations for that group.

On this slide
A dictionary can hold one running total for each group.

An absent key needs an initial zero.

Then add the reading to that group.

To calculate group means, keep a matching count and divide each group total by its own count.

Continue to
Summaries for separate groups in Python (1/2)

## Slide 63 — Summaries for separate groups in Python (1/2)

Summaries for separate groups in Python (1/2)
CML3113, Week 4, slide 63

Explanation to give
Each group needs its own total and count. Identify the group label before updating its stored summary. A total divided by the overall count gives the wrong group mean.

Worked illustration / lecturer answer
Records A:2, A:4 and B:10 give A total 6 and count 2, so A mean 3. B total 10 and count 1 give mean 10.

Misconception to address
Start a new group's total and count once, when first encountered. Resetting them on every record loses earlier observations for that group.

Read the displayed code line by line
records = [{"group": "A", "reading": 2},
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

{"group": "A", "reading": 4},
This line continues the surrounding expression or block; read it together with the preceding line rather than running it alone.

{"group": "B", "reading": 9}]
This line continues the surrounding expression or block; read it together with the preceding line rather than running it alone.

totals = {}
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

for row in records:
Take each item or pair in turn, assign the loop name(s), and repeat the indented body.

group = row["group"]
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

if group not in totals:
Evaluate this yes/no condition. Execute its indented body only on the matching path.

totals[group] = 0
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

totals[group] = totals[group] + row["reading"]
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

Result / continuity
Read top to bottom. Run the complete example in the matching practice notebook.

Continue to
Summaries for separate groups in Python (2/2)

## Slide 64 — Summaries for separate groups in Python (2/2)

Summaries for separate groups in Python (2/2)
CML3113, Week 4, slide 64

Explanation to give
Each group needs its own total and count. Identify the group label before updating its stored summary. A total divided by the overall count gives the wrong group mean.

Worked illustration / lecturer answer
Records A:2, A:4 and B:10 give A total 6 and count 2, so A mean 3. B total 10 and count 1 give mean 10.

Misconception to address
Start a new group's total and count once, when first encountered. Resetting them on every record loses earlier observations for that group.

Read the displayed code line by line
print(totals)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Continue the SAME cell; keep indentation. Run after all parts are entered.

Continue to
A group mean needs its own count

## Slide 65 — A group mean needs its own count

A group mean needs its own count
CML3113, Week 4, slide 65

Explanation to give
Each group needs its own total and count. Identify the group label before updating its stored summary. A total divided by the overall count gives the wrong group mean.

Worked illustration / lecturer answer
Records A:2, A:4 and B:10 give A total 6 and count 2, so A mean 3. B total 10 and count 1 give mean 10.

Misconception to address
Start a new group's total and count once, when first encountered. Resetting them on every record loses earlier observations for that group.

On this slide
The preceding loop calculated a total for each group. Count records in those same groups, then divide each group total by its own count.

items() supplies the group name and its total together. We use small invented records, not the assignment’s answers.

Continue to
From group totals to group means

## Slide 66 — From group totals to group means

From group totals to group means
CML3113, Week 4, slide 66

Explanation to give
Each group needs its own total and count. Identify the group label before updating its stored summary. A total divided by the overall count gives the wrong group mean.

Worked illustration / lecturer answer
Records A:2, A:4 and B:10 give A total 6 and count 2, so A mean 3. B total 10 and count 1 give mean 10.

Misconception to address
Start a new group's total and count once, when first encountered. Resetting them on every record loses earlier observations for that group.

Read the displayed code line by line
counts = {}
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

for row in records:
Take each item or pair in turn, assign the loop name(s), and repeat the indented body.

group = row["group"]
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

counts[group] = counts.get(group, 0) + 1
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

means = {}
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

for group, total in totals.items():
Take each item or pair in turn, assign the loop name(s), and repeat the indented body.

means[group] = total / counts[group]
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

print(means)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Expected: A has mean 3.0 and B has mean 9.0. Each group uses its own denominator.

Continue to
When numeric text cannot be converted

## Slide 67 — When numeric text cannot be converted

When numeric text cannot be converted
CML3113, Week 4, slide 67

Explanation to give
Inspect a field before converting it. A blank string represents no recorded number here. Converting that blank with float raises ValueError, so handle the missing case explicitly.

Worked illustration / lecturer answer
For text values ["2", "", "4"], skip the blank and convert the other two to 2.0 and 4.0. Their mean is 3.0 using count 2, not count 3.

Misconception to address
Do not convert blank to zero merely to silence an error. Zero is a measurement. Catch only the expected conversion failure so unrelated coding errors remain visible.

On this slide
float("bad") raises ValueError: the text does not represent a number. An exception interrupts ordinary execution.

try contains the operation that might fail. except ValueError runs only for that named failure. Indentation shows the two blocks.

Continue to
Catch one expected conversion failure

## Slide 68 — Catch one expected conversion failure

Catch one expected conversion failure
CML3113, Week 4, slide 68

Explanation to give
Inspect a field before converting it. A blank string represents no recorded number here. Converting that blank with float raises ValueError, so handle the missing case explicitly.

Worked illustration / lecturer answer
For text values ["2", "", "4"], skip the blank and convert the other two to 2.0 and 4.0. Their mean is 3.0 using count 2, not count 3.

Misconception to address
Do not convert blank to zero merely to silence an error. Zero is a measurement. Catch only the expected conversion failure so unrelated coding errors remain visible.

Read the displayed code line by line
text = "bad"
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

try:
Attempt the indented conversion while allowing the specified failure to be handled.

reading = float(text)
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

except ValueError:
Handle only the named exception from the preceding try block.

reading = None
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

print(reading)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Expected: None. The assignment specifies which invalid records to skip; do not invent a replacement number.

Continue to
Trace conversion success and failure

## Slide 69 — Trace conversion success and failure

Trace conversion success and failure
CML3113, Week 4, slide 69

Explanation to give
Inspect a field before converting it. A blank string represents no recorded number here. Converting that blank with float raises ValueError, so handle the missing case explicitly.

Worked illustration / lecturer answer
For text values ["2", "", "4"], skip the blank and convert the other two to 2.0 and 4.0. Their mean is 3.0 using count 2, not count 3.

Misconception to address
Do not convert blank to zero merely to silence an error. Zero is a measurement. Catch only the expected conversion failure so unrelated coding errors remain visible.

On this slide
Text supplied | try block | Result after except
"2.5" | float succeeds; skip except | 2.5
"bad" | float raises ValueError | None assigned by except
Only the named conversion failure is handled. Do not use except: pass to hide unrelated errors.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Revision example and answer

## Slide 70 — Revision example and answer

Revision example and answer
CML3113, Week 4, slide 70

Explanation to give
Use the displayed example as a short individual revision question, then explain the reasoning behind its answer.

Worked illustration / lecturer answer
Example: Add 8 to the list. Trace the new total and count before running. What happens if total = 0 is moved inside the loop?

Answer: Total 20, count 4, mean 5.0. Resetting inside the loop discards previous additions and leaves only the last value in total.

Misconception to address
Trace the operation that changes the value rather than accepting a memorised output. For notebook-state examples, specify which cell is repeated and whether the initialisation ran again.

Continue to
Preparing for the assignment

## Slide 71 — Preparing for the assignment

Preparing for the assignment
CML3113, Week 4, slide 71

Explanation to give
A4 uses the Week 4 300-row cohort CSV. The required outputs are valid_count, mean_reading, above_limit and group_means. Work only with the rows admitted by the published blank-reading rules.

Worked illustration / lecturer answer
Trace a smaller unrelated dataset first: A readings 2 and 4 yield A mean 3; B reading 9 yields B mean 9. Each group needs its own denominator.

Misconception to address
Despite “Reading report” in the title, A4 is one completed Python notebook, not a separate Word report. Do not use Week 2’s four-row CSV.

On this slide
Open the issued W04 notebook and its cohort CSV.

Compute the requested valid_count, mean_reading, above_limit and group_means using the exact names in the notebook.

First identify the correct field and its unit.

Keep the CSV beside the notebook locally or upload it into the Colab runtime.

Continue to
Preparing for the assignment continued

## Slide 72 — Preparing for the assignment continued

Preparing for the assignment continued
CML3113, Week 4, slide 72

Explanation to give
A4 uses the Week 4 300-row cohort CSV. The required outputs are valid_count, mean_reading, above_limit and group_means. Work only with the rows admitted by the published blank-reading rules.

Worked illustration / lecturer answer
Trace a smaller unrelated dataset first: A readings 2 and 4 yield A mean 3; B reading 9 yields B mean 9. Each group needs its own denominator.

Misconception to address
Despite “Reading report” in the title, A4 is one completed Python notebook, not a separate Word report. Do not use Week 2’s four-row CSV.

On this slide
The written interpretation is practice.

Continue to
Counting every record

## Slide 73 — Counting every record

Counting every record
CML3113, Week 4, slide 73

Explanation to give
An audit describes the difference between the received data and the retained data. State what was counted and why a record was removed or a field filled. Return named counts so another reader can verify the accounting.

Worked illustration / lecturer answer
If 5 raw records become 4 after one duplicate removal, raw_count is 5 and cleaned_count is 4. A filled field changes a value but does not by itself remove a record.

Misconception to address
Several defect counts can overlap on the same record. Do not add them as if they were mutually exclusive removals unless your counting rule guarantees that.

On this slide
DictReader already consumes the header; skipping its first yielded row skips real data.

A string such as "unknown" cannot be converted to float.

Catch the expected conversion error, count and record it, then continue under a stated policy.

Inspect whether skipped rows share a source before reporting a mean.

Continue to
Counting every record continued

## Slide 74 — Counting every record continued

Counting every record continued
CML3113, Week 4, slide 74

Explanation to give
An audit describes the difference between the received data and the retained data. State what was counted and why a record was removed or a field filled. Return named counts so another reader can verify the accounting.

Worked illustration / lecturer answer
If 5 raw records become 4 after one duplicate removal, raw_count is 5 and cleaned_count is 4. A filled field changes a value but does not by itself remove a record.

Misconception to address
Several defect counts can overlap on the same record. Do not add them as if they were mutually exclusive removals unless your counting rule guarantees that.

On this slide
A sample summary describes observed records, not every possible operating condition.

Continue to
Your issued assignment

## Slide 75 — Your issued assignment

Your issued assignment
CML3113, Week 4, slide 75

Explanation to give
A4 uses the Week 4 300-row cohort CSV. The required outputs are valid_count, mean_reading, above_limit and group_means. Work only with the rows admitted by the published blank-reading rules.

Worked illustration / lecturer answer
Trace a smaller unrelated dataset first: A readings 2 and 4 yield A mean 3; B reading 9 yields B mean 9. Each group needs its own denominator.

Misconception to address
Despite “Reading report” in the title, A4 is one completed Python notebook, not a separate Word report. Do not use Week 2’s four-row CSV.

On this slide
Open W04_student.ipynb.

Read every task and its input units before coding.

Keep the required function names and returned outputs.

Restart and run all cells, then save the completed notebook.

Continue to
valid_count (5 marks)

## Slide 76 — valid_count (5 marks)

valid_count (5 marks)
CML3113, Week 4, slide 76

Explanation to give
Count records with a nonblank reading after applying the published rules. A blank is not a measured zero.

Worked illustration / lecturer answer
For numeric text "2", blank, "4", there are two recorded numbers. The assignment uses the current Week 4 300-row CSV.

Misconception to address
Keep the exact output names and required types. Use the task text for the learner’s own assessed answer; the alternate example explains the method without replacing their work.

On this slide
Store an integer count of rows whose rate_of_penetration field is nonblank.

Skip blank readings before numeric conversion.

Continue to
mean_reading (5 marks)

## Slide 77 — mean_reading (5 marks)

mean_reading (5 marks)
CML3113, Week 4, slide 77

Explanation to give
Add only the readings admitted by the stated validity rule, then divide by their count. Keep the requested numeric return or variable.

Worked illustration / lecturer answer
For recorded readings 2 and 4, mean is 3. The skipped blank does not belong in the denominator.

Misconception to address
Keep the exact output names and required types. Use the task text for the learner’s own assessed answer; the alternate example explains the method without replacing their work.

On this slide
Store the arithmetic mean of the nonblank rate_of_penetration values as a number.

Add the valid readings and divide by their count.

Keep full precision.

Continue to
above_limit (5 marks)

## Slide 78 — above_limit (5 marks)

above_limit (5 marks)
CML3113, Week 4, slide 78

Explanation to give
Compare each valid numeric reading against the specified threshold using the exact strict or inclusive relation in the task.

Worked illustration / lecturer answer
For readings 9,10,11 and a strictly-greater-than 10 limit, the count is 1. Using >= would incorrectly count 2.

Misconception to address
Keep the exact output names and required types. Use the task text for the learner’s own assessed answer; the alternate example explains the method without replacing their work.

On this slide
Store an integer count of valid rate_of_penetration readings strictly greater than 8.0.

A reading equal to the threshold is not counted.

Continue to
group_means (5 marks)

## Slide 79 — group_means (5 marks)

group_means (5 marks)
CML3113, Week 4, slide 79

Explanation to give
Produce a dictionary from each group label to its own mean, using each group’s valid count.

Worked illustration / lecturer answer
Group A with readings 2 and 4 has mean 3. Group B with a single 9 has mean 9. Dividing both by the overall count would be wrong.

Misconception to address
Keep the exact output names and required types. Use the task text for the learner’s own assessed answer; the alternate example explains the method without replacing their work.

On this slide
Store a dictionary whose keys are the bit_type labels and whose values are the mean valid rate_of_penetration readings within each group.

Divide each group total by its own valid count.

Keep full precision.

Continue to
Week 4 rules

## Slide 80 — Week 4 rules

Week 4 rules
CML3113, Week 4, slide 80

Explanation to give
A4 uses the Week 4 300-row cohort CSV. The required outputs are valid_count, mean_reading, above_limit and group_means. Work only with the rows admitted by the published blank-reading rules.

Worked illustration / lecturer answer
Trace a smaller unrelated dataset first: A readings 2 and 4 yield A mean 3; B reading 9 yields B mean 9. Each group needs its own denominator.

Misconception to address
Despite “Reading report” in the title, A4 is one completed Python notebook, not a separate Word report. Do not use Week 2’s four-row CSV.

On this slide
Fictional teaching data.

300 records.

Three blank rate_of_penetration values must be skipped in numerical summaries.

Threshold 8.0 is a teaching assumption.

Continue to
Week 4 rules continued

## Slide 81 — Week 4 rules continued

Week 4 rules continued
CML3113, Week 4, slide 81

Explanation to give
A4 uses the Week 4 300-row cohort CSV. The required outputs are valid_count, mean_reading, above_limit and group_means. Work only with the rows admitted by the published blank-reading rules.

Worked illustration / lecturer answer
Trace a smaller unrelated dataset first: A readings 2 and 4 yield A mean 3; B reading 9 yields B mean 9. Each group needs its own denominator.

Misconception to address
Despite “Reading report” in the title, A4 is one completed Python notebook, not a separate Word report. Do not use Week 2’s four-row CSV.

On this slide
Compute valid_count, mean_reading, above_limit (strictly greater than 8.0) and group_means keyed by bit_type.

Use standard-library csv and collections.

Save a copy using your Student Registration Number with / replaced by _, followed by _W04.ipynb.

STUDENT_ID in the starter code means Student Registration Number.

Continue to
Week 4 rules continued

## Slide 82 — Week 4 rules continued

Week 4 rules continued
CML3113, Week 4, slide 82

Explanation to give
A4 uses the Week 4 300-row cohort CSV. The required outputs are valid_count, mean_reading, above_limit and group_means. Work only with the rows admitted by the published blank-reading rules.

Worked illustration / lecturer answer
Trace a smaller unrelated dataset first: A readings 2 and 4 yield A mean 3; B reading 9 yields B mean 9. Each group needs its own denominator.

Misconception to address
Despite “Reading report” in the title, A4 is one completed Python notebook, not a separate Word report. Do not use Week 2’s four-row CSV.

On this slide
Four checks carry five marks each.

Explain the interesting pattern separately as formative practice.

For beginner step-by-step help, open ASSIGNMENT_INSTRUCTIONS.txt and STUDENT_HOW_TO.md in this folder.

The first names your required files and hand-in checklist; the second explains accounts, Colab, saving and uploads.

Continue to
Reading report submission

## Slide 83 — Reading report submission

Reading report submission
CML3113, Week 4, slide 83

Explanation to give
This slide hands over CML3113 W04. Show the exact form title before uploading. The required packet is one completed .ipynb notebook.

Worked illustration / lecturer answer
The recorded cutoff for this form is 2026-10-09T08:00:00+03:00. Check the live form for later changes. A replacement must contain the complete required file set, not just the changed file.

Misconception to address
Students enter their own Student Registration Number as required freeform text. They wait for filenames to appear, press Submit and keep the confirmation. A file saved in Drive or GitHub is not itself a form submission.

On this slide
Opens: 02 Oct 2026, 08:00 Kampala

Deadline: 09 Oct 2026, 08:00 Kampala

Use your full Student Registration Number in the form.

Keep the submitted files and confirmation.

Continue to
Week 4 quiz

## Slide 84 — Week 4 quiz

Week 4 quiz
CML3113, Week 4, slide 84

Explanation to give
This is the CML3113 Week 4 quiz. The student link opens the response form; it does not activate its window. In Quiz Controls use open_W4_CML3113 when ready and read the logged closing time.

Worked illustration / lecturer answer
Explain the distinction between the expected answering time and availability: five minutes of questions can still be available for 24 hours after activation. Enter the learner’s own Student Registration Number and use the registered Google account.

Misconception to address
Read the exact live cutoff before announcing it. Do not promise a new attempt to somebody who already submitted. Quiz catch-up and assignment uploads are separate forms.

On this slide
Answer individually after the lecturer activates the quiz.

Available for 24 hours from activation.

Use your Student Registration Number and registered account.

Check the announced quiz closing time.

Continue to
Revision and submission checklist

## Slide 85 — Revision and submission checklist

Revision and submission checklist
CML3113, Week 4, slide 85

Explanation to give
Move from one calculation to many records. Lists supply ordered values, loops visit them, dictionaries label fields and CSV files store the observations.

Worked illustration / lecturer answer
For readings 2, 4 and 6, the running total is 2, then 6, then 12. Count 3 gives mean 4.0. A group needs its own total and count.

Misconception to address
Close by identifying the actual saved file and its correct submission route. Read the live deadline. For current weekly notebook tasks, students upload their own work, not the practice notebook, ZIP or grading files.

On this slide
You can show how the total and count change for each record.

Save your work and check the required submission files.
