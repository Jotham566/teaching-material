# CML3111 Week 4

## Slide 1: Lists loops and reading a table

Lists loops and reading a table
CML3111, Week 4, slide 1

Explanation to give
Move from one calculation to many records. Lists supply ordered values, loops visit them, dictionaries label fields and CSV files store the observations.

Worked illustration / lecturer answer
For readings 2, 4 and 6, the running total is 2, then 6, then 12. Count 3 gives mean 4.0. A group needs its own total and count.

Misconception to address
Use this as an orientation to the lesson. Terms and syntax will be unpacked on their own slides; students do not need to know them in advance.

On this slide
Communications, Electrical, Mechatronics and Robotics Engineering

Continue to
Today’s learning

## Slide 2: Today’s learning

Today’s learning
CML3111, Week 4, slide 2

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

## Slide 3: Connection to the previous lesson

Connection to the previous lesson
CML3111, Week 4, slide 3

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

## Slide 4: Why this week’s tools are needed

Why this week’s tools are needed
CML3111, Week 4, slide 4

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

## Slide 5: List and index

List and index
CML3111, Week 4, slide 5

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

## Slide 6: A list position starts at zero

A list position starts at zero
CML3111, Week 4, slide 6

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

## Slide 7: Read list operations

Read list operations
CML3111, Week 4, slide 7

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

## Slide 8: A list stores items in order

A list stores items in order
CML3111, Week 4, slide 8

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

Output from the supplied CSV (this cohort):
2
4
[4, 6]


Result from the supplied example
2
4
[4, 6]

## Slide 9: Trace the list changes

Trace the list changes
CML3111, Week 4, slide 9

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

## Slide 10: A loop repeats instructions

A loop repeats instructions
CML3111, Week 4, slide 10

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

## Slide 11: Read every part of a for header

Read every part of a for header
CML3111, Week 4, slide 11

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

## Slide 12: Visit each item without calculating

Visit each item without calculating
CML3111, Week 4, slide 12

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

Output from the supplied CSV (this cohort):
2
4
6
finished


Result from the supplied example
2
4
6
finished

## Slide 13: Trace the for loop item by item

Trace the for loop item by item
CML3111, Week 4, slide 13

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

## Slide 14: Updating a counter inside a loop

Updating a counter inside a loop
CML3111, Week 4, slide 14

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

## Slide 15: Count the visited items

Count the visited items
CML3111, Week 4, slide 15

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

Output from the supplied CSV (this cohort):
3


Result from the supplied example
3

## Slide 16: Accumulator

Accumulator
CML3111, Week 4, slide 16

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

## Slide 17: A loop repeats an indented block

A loop repeats an indented block
CML3111, Week 4, slide 17

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

## Slide 18: A mean uses a total and a count

A mean uses a total and a count
CML3111, Week 4, slide 18

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

## Slide 19: A loop changes the running total

A loop changes the running total
CML3111, Week 4, slide 19

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

## Slide 20: Tracing the loop

Tracing the loop
CML3111, Week 4, slide 20

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

## Slide 21: Lists loops and records in Python

Lists loops and records in Python
CML3111, Week 4, slide 21

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

Output from the supplied CSV (this cohort):
4.0


Result from the supplied example
4.0

## Slide 22: Lists loops and records results

Lists loops and records results
CML3111, Week 4, slide 22

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

## Slide 23: The built-in summary functions

The built-in summary functions
CML3111, Week 4, slide 23

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

## Slide 24: Built-in summaries of a list

Built-in summaries of a list
CML3111, Week 4, slide 24

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

Output from the supplied CSV (this cohort):
12
3
2
6


Result from the supplied example
12
3
2
6

## Slide 25: A while loop checks before each repetition

A while loop checks before each repetition
CML3111, Week 4, slide 25

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

## Slide 26: A while loop with a stopping condition

A while loop with a stopping condition
CML3111, Week 4, slide 26

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

Output from the supplied CSV (this cohort):
0
1
2
finished


Result from the supplied example
0
1
2
finished

## Slide 27: Trace the while condition and update

Trace the while condition and update
CML3111, Week 4, slide 27

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

## Slide 28: Preventing an endless loop

Preventing an endless loop
CML3111, Week 4, slide 28

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

## Slide 29: Choosing if for or while

Choosing if for or while
CML3111, Week 4, slide 29

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

## Slide 30: range supplies a sequence of integers

range supplies a sequence of integers
CML3111, Week 4, slide 30

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

## Slide 31: Repeat with range

Repeat with range
CML3111, Week 4, slide 31

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

Output from the supplied CSV (this cohort):
1
2
3


Result from the supplied example
1
2
3

## Slide 32: continue and break change a loop’s path

continue and break change a loop’s path
CML3111, Week 4, slide 32

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

## Slide 33: Skip one item using continue

Skip one item using continue
CML3111, Week 4, slide 33

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

Output from the supplied CSV (this cohort):
2
6


Result from the supplied example
2
6

## Slide 34: Stop at one item using break

Stop at one item using break
CML3111, Week 4, slide 34

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

Output from the supplied CSV (this cohort):
2


Result from the supplied example
2

## Slide 35: Trace the two loop controls

Trace the two loop controls
CML3111, Week 4, slide 35

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

## Slide 36: A dictionary is a record with named fields

A dictionary is a record with named fields
CML3111, Week 4, slide 36

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

## Slide 37: A missing dictionary key and get

A missing dictionary key and get
CML3111, Week 4, slide 37

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

## Slide 38: Reading and updating a dictionary

Reading and updating a dictionary
CML3111, Week 4, slide 38

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

Output from the supplied CSV (this cohort):
4
6
0


Result from the supplied example
4
6
0

## Slide 39: Tuples and unpacking

Tuples and unpacking
CML3111, Week 4, slide 39

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

## Slide 40: Unpacking a pair

Unpacking a pair
CML3111, Week 4, slide 40

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

Output from the supplied CSV (this cohort):
2
3


Result from the supplied example
2
3

## Slide 41: A set remembers distinct items

A set remembers distinct items
CML3111, Week 4, slide 41

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

## Slide 42: Set membership and repeated IDs

Set membership and repeated IDs
CML3111, Week 4, slide 42

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

Output from the supplied CSV (this cohort):
1
True
False


Result from the supplied example
1
True
False

## Slide 43: How the four collections differ

How the four collections differ
CML3111, Week 4, slide 43

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

## Slide 44: Dictionary items and two loop names

Dictionary items and two loop names
CML3111, Week 4, slide 44

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

## Slide 45: Looping through named fields

Looping through named fields
CML3111, Week 4, slide 45

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

Output from the supplied CSV (this cohort):
unit A
reading 6


Result from the supplied example
unit A
reading 6

## Slide 46: A position and a key find different things

A position and a key find different things
CML3111, Week 4, slide 46

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

## Slide 47: CSV and header

CSV and header
CML3111, Week 4, slide 47

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

## Slide 48: One record at a time

One record at a time
CML3111, Week 4, slide 48

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

## Slide 49: A CSV file has a header and text values

A CSV file has a header and text values
CML3111, Week 4, slide 49

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

## Slide 50: A CSV row becomes a dictionary

A CSV row becomes a dictionary
CML3111, Week 4, slide 50

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

## Slide 51: with and import

with and import
CML3111, Week 4, slide 51

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

## Slide 52: Your cohort data

Your cohort data
CML3111, Week 4, slide 52

Explanation to give
Use an electrical device as the physical reference. Voltage is measured in volts, current in amperes and power in watts. State what each quantity describes before multiplying them.

Worked illustration / lecturer answer
Show motor_test_bench.csv in the runtime Files panel. The Week 2 file has four rows for setup; Week 4 uses its own 300-row file. Inspect the header to locate this cohort’s reading field and group field.

Misconception to address
Do not confuse input voltage with resistance or energy with power. Read the exact programme task and its units before substituting numbers.

On this slide
motor_test_bench.csv

Summarise winding_temp_c (degrees C); group by motor_id.

Read the issued task’s blank-value and threshold rules before calculating.

Continue to
Read the supplied CSV in four steps

## Slide 53: Read the supplied CSV in four steps

Read the supplied CSV in four steps
CML3111, Week 4, slide 53

Explanation to give
A CSV file stores rows as text separated into fields. Its header provides column names. csv.DictReader turns each data row into a dictionary using those names; numeric-looking cells initially remain strings.

Worked illustration / lecturer answer
A CSV row with reading 2.5 yields the text "2.5". float converts that field to the number 2.5. with open(...) keeps the file available inside the indented block and closes it afterwards.

Misconception to address
Use the exact file from the current week's package and its exact header. A correct formula cannot repair a wrong file, misspelled column or wrong unit.

On this slide
Place motor_test_bench.csv beside the notebook, or upload it in Colab’s Files panel.

import csv loads the CSV tools. newline="" lets the reader handle line endings. DictReader uses the header as dictionary keys.

list(...) collects the rows while the file is open. We inspect the first row and the count; the later assignment calculations are your work.

Continue to
What with open as source does

## Slide 54: What with open as source does

What with open as source does
CML3111, Week 4, slide 54

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

## Slide 55: Open a real CSV and inspect its first row

Open a real CSV and inspect its first row
CML3111, Week 4, slide 55

Explanation to give
A CSV file stores rows as text separated into fields. Its header provides column names. csv.DictReader turns each data row into a dictionary using those names; numeric-looking cells initially remain strings.

Worked illustration / lecturer answer
A CSV row with reading 2.5 yields the text "2.5". float converts that field to the number 2.5. with open(...) keeps the file available inside the indented block and closes it afterwards.

Misconception to address
Use the exact file from the current week's package and its exact header. A correct formula cannot repair a wrong file, misspelled column or wrong unit.

Read the displayed code line by line
import csv
Load this library. An alias after as is the shorter name used below.

with open("motor_test_bench.csv", newline="") as source:
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

Output from the supplied CSV (this cohort):
{'motor_id': 'M1', 'supply_v': '230', 'current_a': '5.41', 'rpm': '1400', 'winding_temp_c': '81.7', 'vibration_rms': '0.503', 'pass_fail': 'pass', 'test_date': '2026-03-01', 'ambient_temp_c': '25'}
300


Result from the supplied example
{'motor_id': 'M1', 'supply_v': '230', 'current_a': '5.41', 'rpm': '1400', 'winding_temp_c': '81.7', 'vibration_rms': '0.503', 'pass_fail': 'pass', 'test_date': '2026-03-01', 'ambient_temp_c': '25'}
300

## Slide 56: Numbers read from CSV

Use the real header shown in the previous example. The list rows already contains the supplied file records.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 57: Recorded values from the supplied rows

Each retained number comes directly from a CSV row. [:5] previews up to five entries.

Complete worked example:
values = []
for row in rows:
    text = row["winding_temp_c"]
    if text != "":
        values.append(float(text))
print(len(values))
print(values[:5])

Output from the supplied CSV (this cohort):
297
[81.7, 81.75, 84.17, 86.34, 82.43]


Result from the supplied example
297
[81.7, 81.75, 84.17, 86.34, 82.43]

## Slide 58: One summary for each group

Every retained row contributes once. Use the actual group and measurement names in this cohort’s CSV.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 59: Grouped means from the supplied rows (1/2)

get(group, 0) returns the existing value or zero for a new group. The measurement and grouping labels match the supplied CSV.

Complete worked example:
totals = {}
counts = {}
for row in rows:
    group = row["motor_id"]
    if row["winding_temp_c"] != "":
        value = float(row["winding_temp_c"])
        totals[group] = totals.get(group, 0) + value
        counts[group] = counts.get(group, 0) + 1
means = {}
for group in totals:
    means[group] = totals[group] / counts[group]
print(means)

Output from the supplied CSV (this cohort):
{'M1': 84.87526315789471, 'M2': 85.19885714285714, 'M3': 112.97368421052634, 'M4': 84.91842105263157, 'M5': 84.84891891891888, 'M6': 85.25189189189189, 'M7': 84.7543243243243, 'M8': 84.85756756756756}


Result from the supplied example
{'M1': 84.87526315789471, 'M2': 85.19885714285714, 'M3': 112.97368421052634, 'M4': 84.91842105263157, 'M5': 84.84891891891888, 'M6': 85.25189189189189, 'M7': 84.7543243243243, 'M8': 84.85756756756756}

## Slide 60: Grouped means from the supplied rows (2/2)

get(group, 0) returns the existing value or zero for a new group. The measurement and grouping labels match the supplied CSV.

Complete worked example:
totals = {}
counts = {}
for row in rows:
    group = row["motor_id"]
    if row["winding_temp_c"] != "":
        value = float(row["winding_temp_c"])
        totals[group] = totals.get(group, 0) + value
        counts[group] = counts.get(group, 0) + 1
means = {}
for group in totals:
    means[group] = totals[group] / counts[group]
print(means)

Result from the supplied example
{'M1': 84.87526315789471, 'M2': 85.19885714285714, 'M3': 112.97368421052634, 'M4': 84.91842105263157, 'M5': 84.84891891891888, 'M6': 85.25189189189189, 'M7': 84.7543243243243, 'M8': 84.85756756756756}

## Slide 61: Your issued assignment

Your issued assignment
CML3111, Week 4, slide 75

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

## Slide 62: valid_count (5 marks)

valid_count (5 marks)
CML3111, Week 4, slide 76

Explanation to give
Count records with a nonblank reading after applying the published rules. A blank is not a measured zero.

Worked illustration / lecturer answer
For numeric text "2", blank, "4", there are two recorded numbers. The assignment uses the current Week 4 300-row CSV.

Misconception to address
Keep the exact output names and required types. Use the task text for the learner’s own assessed answer; the alternate example explains the method without replacing their work.

On this slide
Store an integer count of rows whose winding_temp_c field is nonblank.

Skip blank readings before numeric conversion.

Continue to
mean_reading (5 marks)

## Slide 63: mean_reading (5 marks)

mean_reading (5 marks)
CML3111, Week 4, slide 77

Explanation to give
Add only the readings admitted by the stated validity rule, then divide by their count. Keep the requested numeric return or variable.

Worked illustration / lecturer answer
For recorded readings 2 and 4, mean is 3. The skipped blank does not belong in the denominator.

Misconception to address
Keep the exact output names and required types. Use the task text for the learner’s own assessed answer; the alternate example explains the method without replacing their work.

On this slide
Store the arithmetic mean of the nonblank winding_temp_c values as a number.

Add the valid readings and divide by their count.

Keep full precision.

Continue to
above_limit (5 marks)

## Slide 64: above_limit (5 marks)

above_limit (5 marks)
CML3111, Week 4, slide 78

Explanation to give
Compare each valid numeric reading against the specified threshold using the exact strict or inclusive relation in the task.

Worked illustration / lecturer answer
For readings 9,10,11 and a strictly-greater-than 10 limit, the count is 1. Using >= would incorrectly count 2.

Misconception to address
Keep the exact output names and required types. Use the task text for the learner’s own assessed answer; the alternate example explains the method without replacing their work.

On this slide
Store an integer count of valid winding_temp_c readings strictly greater than 130.0.

A reading equal to the threshold is not counted.

Continue to
group_means (5 marks)

## Slide 65: group_means (5 marks)

group_means (5 marks)
CML3111, Week 4, slide 79

Explanation to give
Produce a dictionary from each group label to its own mean, using each group’s valid count.

Worked illustration / lecturer answer
Group A with readings 2 and 4 has mean 3. Group B with a single 9 has mean 9. Dividing both by the overall count would be wrong.

Misconception to address
Keep the exact output names and required types. Use the task text for the learner’s own assessed answer; the alternate example explains the method without replacing their work.

On this slide
Store a dictionary whose keys are the motor_id labels and whose values are the mean valid winding_temp_c readings within each group.

Divide each group total by its own valid count.

Keep full precision.

Continue to
Week 4 rules

## Slide 66: Week 4 rules

Week 4 rules
CML3111, Week 4, slide 80

Explanation to give
A4 uses the Week 4 300-row cohort CSV. The required outputs are valid_count, mean_reading, above_limit and group_means. Work only with the rows admitted by the published blank-reading rules.

Worked illustration / lecturer answer
Trace a smaller unrelated dataset first: A readings 2 and 4 yield A mean 3; B reading 9 yields B mean 9. Each group needs its own denominator.

Misconception to address
Despite “Reading report” in the title, A4 is one completed Python notebook, not a separate Word report. Do not use Week 2’s four-row CSV.

On this slide
Fictional teaching data.

300 records.

Three blank winding_temp_c values must be skipped in numerical summaries.

Threshold 130.0 is a teaching assumption.

Continue to
Week 4 rules continued

## Slide 67: Week 4 rules continued

Week 4 rules continued
CML3111, Week 4, slide 81

Explanation to give
A4 uses the Week 4 300-row cohort CSV. The required outputs are valid_count, mean_reading, above_limit and group_means. Work only with the rows admitted by the published blank-reading rules.

Worked illustration / lecturer answer
Trace a smaller unrelated dataset first: A readings 2 and 4 yield A mean 3; B reading 9 yields B mean 9. Each group needs its own denominator.

Misconception to address
Despite “Reading report” in the title, A4 is one completed Python notebook, not a separate Word report. Do not use Week 2’s four-row CSV.

On this slide
Compute valid_count, mean_reading, above_limit (strictly greater than 130.0) and group_means keyed by motor_id.

Use standard-library csv and collections.

Save a copy using your Student Registration Number with / replaced by _, followed by _W04.ipynb.

STUDENT_ID in the starter code means Student Registration Number.

Continue to
Week 4 rules continued

## Slide 68: Week 4 rules continued

Week 4 rules continued
CML3111, Week 4, slide 82

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

## Slide 69: Reading report submission

Reading report submission
CML3111, Week 4, slide 83

Explanation to give
This slide hands over CML3111 W04. Show the exact form title before uploading. The required packet is one completed .ipynb notebook.

Worked illustration / lecturer answer
The recorded cutoff for this form is 2026-10-09T11:00:00+03:00. Check the live form for later changes. A replacement must contain the complete required file set, not just the changed file.

Misconception to address
Students enter their own Student Registration Number as required freeform text. They wait for filenames to appear, press Submit and keep the confirmation. A file saved in Drive or GitHub is not itself a form submission.

On this slide
Opens: 02 Oct 2026, 11:00 Kampala

Deadline: 09 Oct 2026, 11:00 Kampala

Use your full Student Registration Number in the form.

Keep the submitted files and confirmation.

Continue to
Week 4 quiz

## Slide 70: Week 4 quiz

Week 4 quiz
CML3111, Week 4, slide 84

Explanation to give
This is the CML3111 Week 4 quiz. The student link opens the response form; it does not activate its window. In Quiz Controls use open_W4_CML3111 when ready and read the logged closing time.

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

## Slide 71: Revision and submission checklist

Revision and submission checklist
CML3111, Week 4, slide 85

Explanation to give
Move from one calculation to many records. Lists supply ordered values, loops visit them, dictionaries label fields and CSV files store the observations.

Worked illustration / lecturer answer
For readings 2, 4 and 6, the running total is 2, then 6, then 12. Count 3 gives mean 4.0. A group needs its own total and count.

Misconception to address
Close by identifying the actual saved file and its correct submission route. Read the live deadline. For current weekly notebook tasks, students upload their own work, not the practice notebook, ZIP or grading files.

On this slide
You can show how the total and count change for each record.

Save your work and check the required submission files.