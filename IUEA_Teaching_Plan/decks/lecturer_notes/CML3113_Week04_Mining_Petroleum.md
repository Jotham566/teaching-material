# CML3113 Week 4

Each slide shows its text, then the spoken script the lecturer reads aloud.

## Slide 1: Lists loops and reading a table

Mining and Petroleum Engineering

Friday 02 October 2026
Friday 08:00–11:00, Room 105

**Spoken script**

Welcome to week four. This week we learn how to handle many readings at once instead of one number at a time.

We start with lists, which hold values in order. Then we learn loops, which repeat a step for every value. After that we meet dictionaries, tuples and sets. We finish by reading a table of measurements from a CSV file and calculating averages for each group.

This session is for the mining and petroleum engineering group. Check the slide for the date, time and room.

## Slide 2: Today’s learning

Read lists and dictionary fields.

Trace a loop, read CSV rows and calculate summaries.

You can show how the total and count change for each record.

**Spoken script**

This slide tells us where we are going today. There are two parts.

The first part is what we will do. We will read lists and dictionary fields. A dictionary is a way to store a value under a name, such as a reading under the word reading. We will also trace a loop, which means following it one step at a time. Then we will read the rows of a CSV file and calculate summaries from them.

The second part is how you will show it. You will show how the total and the count change as each record is processed. If you can say what the two numbers are after every record, you have understood the main idea of today.

## Slide 3: Connection to the previous lesson

Week 3 introduced values, function inputs and results, conditions and list positions.

Now we repeat a calculation across records, then organise those records by keys.

**Spoken script**

Last week we met values, function inputs and results, conditions, and list positions. A value is a piece of data such as a number. A function takes inputs and gives back a result. A condition is a true or false question that decides which path the program takes.

Today we build on those. First we repeat a calculation across many records, so that we do not have to write the same line again and again. Then we organise each record using keys. A key is a name that labels one piece of information in a record. Both steps start from the lists and conditions you already used.

## Slide 4: Why this week’s tools are needed

Sensor readings arrive as records in a CSV file.

We first learn the Python collections and loops needed to read those records and summarise them.

**Spoken script**

Think about a sensor that measures something every minute and writes the results to a file. That file is a CSV file. Each line is one record, and the values on a line are separated by commas.

A real file can hold hundreds or thousands of records. We cannot type each one into our program by hand. We need a way to read them in, visit each one, and add them up.

So first we learn the Python tools for that job. Lists hold the readings. Loops visit them one by one. Dictionaries label the fields of a record. With those in place, we can read a whole file and summarise it in a few lines.

## Slide 5: List and index

A list holds values in order: [2, 4, 6]. Square brackets select a position. readings[0] selects the first item, 2.

**Spoken script**

A list holds several values in order. We write it with square brackets and commas between the values. Our example is the list two, four, six, and we give it the name readings.

Every item in a list has a position, and Python calls this position the index. The first item sits at position zero, the second at position one, and the third at position two. We count from zero.

To pick one item, we write the list name followed by square brackets with the position inside. So readings, open square bracket, zero, close square bracket, selects the first item, which is two.

Notice that square brackets appear in two jobs. Around values they build a list. After a name they select an item.

## Slide 6: A list position starts at zero

01

In [2, 4, 6], position 0 holds 2.

02

Position 1 holds 4. Position 2 holds 6.

03

There is no position 3 in this three-item list.

**Spoken script**

Let us look at the list two, four, six one position at a time.

Position zero holds the value two. This is the first item in the list. Many people expect the first position to be one, so it takes practice to count from zero.

Position one holds four, and position two holds six.

This list has three items, so there is no position three. If we ask for position three, Python stops with an error message. The last position is always one less than the number of items. In this list the last position is two.

Keep this picture of positions zero, one and two in mind, because every list in this course works the same way.

## Slide 7: Read list operations

append and len

readings.append(8) adds 8 to the end of the list. len(readings) counts its items. The dot selects an operation belonging to that object; parentheses call it.

Slice

readings[1:3] selects positions 1 and 2. The stop position 3 is excluded. A slice produces a new list; it does not remove items from the original.

**Spoken script**

This slide shows three things we can do with a list.

First, append. We write readings, dot, append, and put the new value in parentheses. For example, append eight adds eight to the end of the list. The dot means we are using an operation that belongs to the list. The parentheses mean we are calling that operation, in other words asking it to run.

Second, len. Writing len of readings counts the items in the list.

Third, a slice. A slice picks a range of positions. Readings, open bracket, one, colon, three, close bracket, picks positions one and two. It stops before position three. The stop position is always left out.

A slice makes a new list. The original list stays as it was.

## Slide 8: A list stores items in order

print displays a value below the cell.

append adds one item to the end of a list.

Square brackets create a list or select an item.

[] builds a list. Positions start at zero. The slice stops before position 3.

```python
readings = [2, 4, 6]
print(readings[0])
readings.append(8)
print(len(readings))
print(readings[1:3])
```

**Spoken script**

We read this example one line at a time.

The first line builds a list called readings with the values two, four and six.

The second line prints readings at position zero. Print shows a value below the cell. Position zero is the first item, so this shows two.

The third line appends eight. Append adds one item to the end, so the list becomes two, four, six, eight.

The fourth line prints len of readings, which counts the items. There are now four, so this shows four.

The last line prints readings from position one up to, but excluding, position three. That means positions one and two, which hold four and six. The output is the small list four, six.

## Slide 9: Trace the list changes

len reports 4 after append. A slice excludes its stop position and leaves the original list intact.

**Spoken script**

This table follows the list after each instruction, so we can see exactly when it changes.

After the first line the list is two, four, six, and nothing is displayed yet because we only created it.

The second line prints the item at position zero. It shows two, and the list stays the same.

The third line appends eight. The list becomes two, four, six, eight. Nothing is displayed, because append changes the list but prints nothing.

The fourth line prints len, which shows four. The fifth line prints a slice from position one up to, but not including, position three, which shows four, six. It shows four, six. The list is still two, four, six, eight.

Len reports four after the append, because there are four items. The slice leaves the original list intact.

## Slide 10: A loop repeats instructions

01

A loop runs a block more than once. One execution of the block is called an iteration.

02

for takes one item at a time from a collection. Use it when each item needs the same action.

03

while repeats while a condition stays True. Use it when a condition controls repetition.

**Spoken script**

A loop runs a block of instructions more than once. One run through the block is called an iteration.

Python gives us two kinds of loop. The first is the for loop. It takes one item at a time from a collection, such as a list, and runs the same action on each item. We use it when every item needs the same treatment.

The second is the while loop. It keeps repeating as long as a condition stays true. A condition is a true or false question. We use while when a condition decides how long the repetition lasts.

Today we begin with for, because summing a list of readings is a job where every item gets the same treatment.

## Slide 11: Read every part of a for header

01

In for reading in readings:, for introduces repetition, reading names the current item, and readings is the collection to visit.

02

in connects the current-item name to that collection. The colon begins the loop body. Four spaces mark each instruction that repeats.

03

reading is a name we choose; it is assigned the next item automatically. It is not the same name as readings. After the last item, execution leaves the loop.

**Spoken script**

We take apart the first line of a for loop, which reads for reading in readings, colon.

The word for tells Python we are starting a repetition.

Reading is a name for the current item. Python gives this name the next item automatically each time round. We choose the name ourselves. Readings with an s is the list we are visiting. These are two different names. One is a single item and the other is the whole collection.

The word in links the item name to the collection.

The colon begins the loop body. The body is the set of lines that repeat, and we mark them with four spaces at the start of each line.

After the last item has been visited, Python leaves the loop and carries on below it.

## Slide 12: Visit each item without calculating

The body runs once for each item.

The final line is outside the loop, so it runs once.

Output: 2; 4; 6; finished

```python
readings = [2, 4, 6]
for reading in readings:
    print(reading)
print("finished")
```

**Spoken script**

We read this loop line by line.

The first line makes the list two, four, six.

The second line starts the loop. Python takes the first item, two, and calls it reading.

The third line is indented by four spaces, so it belongs to the loop body. It prints the current reading. On the first pass it prints two. Python then goes back, takes four, and prints four. On the third pass it takes six and prints six.

The last line prints the word finished. It has no indentation, so it sits outside the loop. It runs once, after the loop is done.

The output is two, four, six, finished. The body ran three times because the list has three items.

## Slide 13: Trace the for loop item by item

An empty list runs the body zero times. It still reaches the outside line.

**Spoken script**

This table traces the same loop step by step.

In the first step, the current reading is two, and the action is to print two.

In the second step, the current reading is four, and we print four.

In the third step, the current reading is six, and we print six.

Then there are no items left, so there is no new reading. Python leaves the loop and prints finished.

The slide also tells us what happens with an empty list, which is a list with nothing in it. The body runs zero times, because there is no item to visit. Python still reaches the outside line and prints finished.

## Slide 14: Updating a counter inside a loop

01

A counter records how many times an event happens. Set count = 0 before the loop, then count = count + 1 inside it.

02

count += 1 is a shorter spelling for that numeric update. Similarly, total += reading means total = total + reading.

03

The initial value belongs outside the loop. Resetting count to zero inside every iteration loses the earlier count.

**Spoken script**

A counter records how many times something happens. We build one in two steps.

First, before the loop, we write count equals zero. This gives the counter a starting value.

Second, inside the loop, we write count equals count plus one. Python reads the right side first, takes the current count and adds one, and then stores the answer back in count.

There is a shorter way to write the same update. Count plus equals one means the same as count equals count plus one. In the same way, total plus equals reading means total equals total plus reading.

The starting value must be set outside the loop. If we reset count to zero inside the loop, it goes back to zero on every pass, and we lose the earlier count.

## Slide 15: Count the visited items

Updates: 0 to 1, 1 to 2, then 2 to 3.

Output: 3

```python
count = 0
for reading in [2, 4, 6]:
    count += 1
print(count)
```

**Spoken script**

This example counts how many items a list has by visiting each one.

The first line sets count to zero, before the loop starts.

The second line starts a for loop over the list two, four, six. On each pass, reading holds the current item.

The third line is inside the loop. It adds one to count. We never use the value of reading here, because we only want to know how many items we visited.

The count changes from zero to one on the first pass, from one to two on the second pass, and from two to three on the third.

The last line is outside the loop and prints count. The output is three, which matches the three items in the list.

## Slide 16: Accumulator

A running total. Set it to zero before the loop, add inside the loop, and read the final total afterward.

**Spoken script**

An accumulator is a running total. It is a variable that collects a result a little at a time as a loop visits each item.

We build it in three steps. Before the loop, we set it to zero. Inside the loop, we add the current item to it. After the loop finishes, we read the final total.

Think of a cashier adding up a customer's items. The till starts at zero, each item adds to the total, and the last number on the screen is the answer.

The counter we saw a moment ago is an accumulator too. It adds one each time instead of adding the item's value.

## Slide 17: A loop repeats an indented block

01

for reading in readings: takes one item at a time.

02

The colon starts the block. Four spaces show which lines repeat.

03

A running total must start at zero before the loop.

**Spoken script**

We pull the loop ideas together before we use them for adding.

The line for reading in readings, colon, takes one item at a time from the list and gives it the name reading.

The colon starts the block, which is the group of lines that repeat. Four spaces at the start of a line show that the line belongs to the block. A line without those spaces is outside the loop.

The last idea is about running totals. A running total must start at zero before the loop. If we forget this, Python does not know what to add to, and we get an error. If we start it inside the loop, it resets on every pass.

## Slide 18: A mean uses a total and a count

01

Start the total at 0. Add 2, then 4, then 6.

02

The final total is 12. The count is 3.

03

12 / 3 gives the mean 4. An empty list needs a separate rule.

**Spoken script**

A mean is the total of the values divided by how many values there are. To find it for our list, we need two numbers from the loop, a total and a count.

In the first step we start the total at zero and add two, then four, then six.

In the second step we look at the results. The final total is twelve, and the count is three because we visited three items.

In the third step we divide. Twelve divided by three gives a mean of four.

The slide also warns that an empty list needs a separate rule. An empty list has a count of zero, and dividing by zero is an error, so we must decide what the program does in that case before we divide.

## Slide 19: A loop changes the running total

This illustration uses six separate readings. Next we trace the smaller list [2, 4, 6] using the same running-total rule.

**Spoken script**

This picture shows a loop changing a running total. It uses six separate readings, so we can see the total grow as each reading is added.

Before the first reading, the total is zero. Each time the loop visits a reading, it adds that reading to the total, and the total gets bigger.

Next we trace a smaller list, two, four, six, using the same rule. With only three readings, we can follow every number on the table and check each step ourselves.

## Slide 20: Tracing the loop

There are three readings.

**Spoken script**

This table traces the running total through the list two, four, six.

Before the loop starts, there is no reading yet, and the total is zero.

On the first pass the reading is two. We add it, and the total becomes two.

On the second pass the reading is four. We add it to the two already in the total, and the total becomes six.

On the third pass the reading is six. We add it, and the total becomes twelve.

There are three readings, so the count is three. The total of twelve and the count of three are the two numbers we need for the mean. Twelve divided by three is four.

## Slide 21: Lists loops and records in Python

for takes the next item. The indented block repeats.

print displays a value below the cell.

Square brackets create a list or select an item.

Read top to bottom. Run the complete example in the matching practice notebook.

```python
readings = [2, 4, 6]
total = 0
for reading in readings:
    total = total + reading
mean = total / len(readings)
print(mean)
```

**Spoken script**

This is the full program that puts together everything we have seen so far. We read it from top to bottom.

The first line builds the list of readings, two, four, six.

The second line sets total to zero. This is the accumulator, and it starts before the loop.

The third line starts the for loop. Each pass gives us the next item, called reading.

The fourth line is indented, so it is in the loop body. It sets total to the old total plus the current reading.

The fifth line is outside the loop. It divides the total by len of readings, which is the number of items, and stores the answer in mean.

The last line prints the mean. We should run this complete example in the matching practice notebook and check the result.

## Slide 22: Lists loops and records results

Which step produced this result? What changes if one input changes?

```python
4.0
```

**Spoken script**

This is the output of the program we just read. It shows four point zero.

That is the mean of two, four and six. The total of twelve divided by the count of three gives four. Python shows it as four point zero because dividing with the slash always gives a decimal number, even when the answer is whole.

Look back at the code and say which step produced this result. The answer is the last division, total divided by len of readings.

Then think about what changes if one input changes. If we changed six to nine, the total would change, so the mean would change too. The count would stay the same, because we still have three readings.

## Slide 23: The built-in summary functions

These functions already exist in Python. min and max need at least one item unless an explicit default is supplied.

**Spoken script**

Python already has built-in functions for the most common summaries, so we do not always need to write a loop ourselves.

Len answers how many items there are. For our list two, four, six, it gives three.

Sum answers what the total is. It gives twelve.

Min answers which item is smallest. It gives two.

Max answers which item is largest. It gives six.

There is one condition. Min and max need at least one item in the list. If the list is empty, they have nothing to choose from, so Python reports an error, unless we supply an explicit default value to use instead.

## Slide 24: Built-in summaries of a list

These functions are built into Python.

min and max require a nonempty list here.

Output: 12, 3, 2, 6. sum totals; len counts; min and max select the smallest and largest.

```python
readings = [2, 4, 6]
print(sum(readings))
print(len(readings))
print(min(readings))
print(max(readings))
```

**Spoken script**

This example uses the built-in summary functions on our list.

The first line makes the list two, four, six.

The second line prints sum of readings. Sum adds all the items, so it shows twelve.

The third line prints len of readings, which counts the items. It shows three.

The fourth line prints min of readings, the smallest item. It shows two.

The last line prints max of readings, the largest item. It shows six.

The output is twelve, three, two, six. These functions are built into Python, so we can use them without any setup. Min and max need a list with at least one item, and our list has three, so both work here.

## Slide 25: A while loop checks before each repetition

01

while count < 3: tests the condition before entering its indented block. True enters the block; False skips it and continues after the loop.

02

At the end of the body, return to the condition and test again. Unlike for, while does not automatically move to the next list item.

03

Something must make the condition become False, or the loop may continue indefinitely. In our example, count increases on every iteration.

**Spoken script**

A while loop checks a condition before each repetition. The condition here is count is less than three.

In the first step, Python tests the condition before entering the block. If the answer is true, it enters the block. If the answer is false, it skips the block and continues after the loop.

In the second step, at the end of the body, Python returns to the condition and tests it again. A for loop moves to the next item in a list by itself. A while loop does not do that. It only repeats the test.

The third step is about stopping. Something inside the loop must make the condition become false, or the loop may continue forever. In our example, count goes up by one on every iteration, so it eventually reaches three.

## Slide 26: A while loop with a stopping condition

Initialise, test, run the body, update, test again.

When count becomes 3, the condition is False.

Output: 0; 1; 2; finished

```python
count = 0
while count < 3:
    print(count)
    count = count + 1
print("finished")
```

**Spoken script**

We read this while loop line by line.

The first line sets count to zero. This is the starting value.

The second line is the test. While count is less than three, the loop body runs.

The third line prints the current count.

The fourth line adds one to count. This update is what eventually ends the loop.

The last line has no indentation, so it runs once, after the loop ends.

The order is to set up, test, run the body, update, and test again. When count reaches three, the test is false and the loop stops. The output is zero, one, two, finished.

## Slide 27: Trace the while condition and update

If count starts at 3, the body runs zero times. The condition is tested first.

**Spoken script**

This table follows the while loop by the value of count at each test.

When count is zero, the test count less than three is true. We print zero and update count to one.

When count is one, the test is true again. We print one and update count to two.

When count is two, the test is still true. We print two and update count to three.

When count is three, the test is false. Python skips the body and goes on to print finished.

The slide also says what happens if count starts at three. The test is made first, and it is false right away, so the body runs zero times.

## Slide 28: Preventing an endless loop

01

If the update is missing, count remains 0. The question 0 < 3 stays True, so the body keeps running.

02

In Colab, click the running cell’s stop button or use Runtime → Interrupt execution. Fix the condition or update before running again.

03

Do not run an intentionally endless example. Trace the unchanged value on the slide to see why it would fail.

**Spoken script**

An endless loop is one that never stops. Here is how it happens with our example.

Suppose we forget the update line. Then count stays at zero for ever. The question zero less than three stays true on every test, so the body keeps running and never finishes.

If that happens in Colab, click the stop button on the running cell, or use the Runtime menu and choose Interrupt execution. Then fix the condition or the update before you run the cell again.

Please do not run an endless example on purpose. Instead, trace the unchanged value on the slide. Count is zero, the test is true, count is still zero, and the test is true again. That tells us the loop would never end.

## Slide 29: Choosing if for or while

A condition alone does not imply repetition: if tests once; while tests again after its body.

**Spoken script**

We now have three ways to control a program, and this table compares them.

An if statement chooses a path once. When the chosen block is done, the program moves on.

A for loop visits supplied items, such as the items of a list. It finishes when the items run out.

A while loop repeats as long as its condition is true. It finishes when the condition becomes false.

The key difference is between if and while. Both test a condition, but if tests it a single time. A while loop tests it again after each run of its body. So a condition alone does not mean a program repeats.

## Slide 30: range supplies a sequence of integers

01

range(3) supplies 0, 1 and 2. The stop value 3 is excluded. range(1, 4) supplies 1, 2 and 3.

02

Use range with for when a numbered repetition is useful. The loop still works by taking the next supplied item.

03

range(0, 6, 2) uses a step of 2 and supplies 0, 2, 4. A step is the change between successive numbers; it cannot be zero.

**Spoken script**

Range gives us a sequence of whole numbers, which is useful when we want a loop to repeat a set number of times.

In the first step, range of three supplies zero, one and two. The stop value, three, is left out. Range of one, comma, four supplies one, two and three, because it starts at one and stops before four.

In the second step, we use range with a for loop. The loop still works the same way. It takes the next supplied number each time.

In the third step, a third value is the step. Range of zero, six, two supplies zero, two and four. The step is the amount we move between one number and the next. The step can never be zero.

## Slide 31: Repeat with range

Start at 1; stop before 4.

Output: 1; 2; 3

```python
for attempt in range(1, 4):
    print(attempt)
```

**Spoken script**

This example repeats an action using range.

The first line says for attempt in range of one, comma, four. Attempt is the name we give to the current number. Range of one to four starts at one and stops before four, so it supplies one, two and three.

The second line is indented, so it is the loop body. It prints the current attempt.

The loop runs three times. The output is one, two, three.

If we wanted it to start at zero we could write range of 3 on its own, with no start value. Here we chose to start at one, which suits counting attempts the way people count them.

## Slide 32: continue and break change a loop’s path

01

continue skips the rest of the current iteration, then starts the next iteration. It does not end the whole loop.

02

break exits the nearest enclosing loop immediately. Execution resumes after that loop.

03

Put the condition inside the loop with four spaces. Its action is inside that condition with eight spaces: an indented block inside another block.

**Spoken script**

Sometimes we need to change the normal path of a loop. Python has two words for this.

The first is continue. It skips the rest of the current iteration and starts the next one. The loop carries on with the next item.

The second is break. It exits the loop immediately. Python resumes with the line after the loop. If there are loops inside loops, break exits only the nearest one.

The third point is about layout. The if condition sits inside the loop with four spaces. Its action, continue or break, sits inside the condition with eight spaces. That is an indented block inside another block. Each level of indentation tells Python what belongs to what.

## Slide 33: Skip one item using continue

-1 takes continue, so its print is skipped.

2 and 6 reach print.

Output: 2; 6

```python
for reading in [2, -1, 6]:
    if reading < 0:
        continue
    print(reading)
```

**Spoken script**

This example skips one item using continue.

The first line loops over the list two, minus one, six. Each pass, reading holds the current item.

The second line is an if statement. It asks whether reading is less than zero, in other words whether it is negative.

The third line has eight spaces. It runs only when the condition is true, and it says continue. This sends Python straight to the next item.

The last line prints the reading, and it has four spaces, so it is part of the loop body.

The reading two is positive, so it is printed. The reading minus one is negative, so continue skips its print. The reading six is printed. The output is two, six.

## Slide 34: Stop at one item using break

-1 triggers break. The loop never visits 6.

Output: 2

```python
for reading in [2, -1, 6]:
    if reading < 0:
        break
    print(reading)
```

**Spoken script**

This example is almost the same as the last one, but it uses break instead of continue.

The loop goes over the list two, minus one, six. For each item, the if line asks whether reading is less than zero.

For two, the answer is false, so the print line runs and shows two.

For minus one, the answer is true, so break runs. The loop ends immediately.

The loop never visits six, because it has already finished.

The output is just two.

The only change from the last slide is one word, and it changes the result from two and six to two alone.

## Slide 35: Trace the two loop controls

Use continue only when skipping is justified by the stated data rule; do not silently discard evidence.

**Spoken script**

This table compares the two loop controls on the same input, the list two, minus one, six.

For the item two, both versions print two.

For minus one, the continue version skips its print and goes on. The break version exits the loop.

For six, the continue version prints six. The break version never reaches it.

The slide gives a rule for using these. Use continue only when the data rule we were given justifies skipping an item. An example is a rule that says negative readings are invalid. We should avoid quietly throwing away data, because we might lose evidence that something is wrong.

## Slide 36: A dictionary is a record with named fields

01

record = {"unit": "A", "reading": 4} stores two key–value pairs. Keys name fields; values hold the information.

02

Braces enclose the dictionary. A colon separates each key from its value and a comma separates pairs. Each key is unique.

03

record["reading"] returns 4. Unlike a list position, "reading" names the field we want.

**Spoken script**

A dictionary is a record with named fields. In a list we find items by position. In a dictionary we find them by name.

Our example is record equals braces, with the word unit, a colon, and the letter A, then a comma, then the word reading, a colon and four. This stores two key and value pairs. The keys are the names of the fields, and the values hold the information.

The braces enclose the dictionary. A colon separates each key from its value, and a comma separates one pair from the next. Each key can appear only once.

To read a value, we write record, then square brackets with the key in quotation marks. Record with the key reading gives four. We ask for the field by its name, so we do not need to remember a position.

## Slide 37: A missing dictionary key and get

01

record["reading"] requests a known field. If that key does not exist, square-bracket lookup raises KeyError.

02

record.get("missing", 0) asks for that key with a fallback: return 0 if it is absent. This does not add a new key.

03

The second input is the fallback value. Use a fallback only when the task defines what missing information should mean.

**Spoken script**

Sometimes we ask a dictionary for a key that is not there. Take a record that holds a unit and a reading. When we write record, then square brackets with the word reading in quotes, Python looks for the key called reading and gives back its value. If that key does not exist, Python stops with an error called KeyError.

There is a gentler way to ask. Record dot get, with the word missing in quotes and then zero, asks for the key called missing and says, if it is absent, give me zero instead. This call does not add a new key to the dictionary. It only hands back the fallback.

The second input to get is the fallback value. We use a fallback only when the task tells us what missing information should mean. In a count, for example, a missing key can sensibly mean zero so far.

## Slide 38: Reading and updating a dictionary

["reading"] selects a key, not a position.

Assigning through the key updates its value.

Output: 4, then 6, then 0. get uses the fallback only when that key is absent.

```python
record = {"unit": "A", "reading": 4}
print(record["reading"])
record["reading"] = 6
print(record["reading"])
print(record.get("missing", 0))
```

**Spoken script**

We build a record with two fields, a unit with the value A and a reading with the value 4. The curly brackets hold pairs, and each pair is a key, a colon, and its value.

The first print asks for the key reading, so we see 4. The square brackets select a key. They pick out the field by its name.

The next line assigns through the key. Record, reading in square brackets, equals 6, replaces the old value stored under that key. The second print now shows 6.

The last print uses get with the key missing and a fallback of zero. The record has no key called missing, so get gives back zero. If the key had been present, get would have returned its real value.

The output is 4, then 6, then 0.

## Slide 39: Tuples and unpacking

01

A tuple stores items in order. point = (2, 3) stores two coordinates; point[0] is 2. You cannot reassign point[0].

02

x, y = point gives the first item to x and the second to y. This is unpacking; the number of names must match the number of items.

03

A tuple prevents replacing its positions. It does not freeze the contents of a mutable object stored inside it.

**Spoken script**

A tuple stores items in order, like a list, but its positions cannot be reassigned. We write one with round brackets. Point equals open bracket 2, comma, 3, close bracket stores two coordinates. Point with zero in square brackets is 2, because counting starts at zero. If we try to put a new value into point at position zero, Python refuses.

Unpacking means giving the items of a tuple to separate names in one line. X comma y equals point gives the first item to x and the second to y. The number of names must match the number of items, otherwise Python reports an error.

A tuple stops us replacing its positions. If a tuple holds a list inside it, the items of that list can still change, because the tuple only fixes which object sits at each position.

## Slide 40: Unpacking a pair

Two names receive the two items in order.

Output: 2, then 3.

```python
point = (2, 3)
x, y = point
print(x)
print(y)
```

**Spoken script**

We create a tuple called point holding 2 and 3. Then x comma y equals point is the unpacking line. There are two names on the left and two items on the right, so they match. Python gives the first item to x and the second item to y, in order.

The first print shows x, which is 2. The second print shows y, which is 3.

The original tuple still exists after unpacking. We have only copied its items into two names so that we can use them separately.

The output is 2, then 3.

## Slide 41: A set remembers distinct items

01

A set is useful when the question is “Have we seen this ID?” It keeps one instance of each distinct item.

02

seen = set() creates an empty set. seen.add("A") adds an item. "A" in seen asks whether it is present.

03

Do not use a set when position or repeated readings matter. Sets cannot be indexed. {} creates an empty dictionary, not an empty set.

**Spoken script**

A set is a collection that keeps one copy of each distinct item. It is useful when the question is, have we seen this ID before? A sensor ID might appear fifty times in a file, and the set keeps it once.

To make an empty set we write seen equals set with empty brackets. Seen dot add with the letter A in quotes puts A into the set. To ask whether something is inside, we write the item, then the word in, then the set. Python answers True or False.

A set is the wrong tool when position or repeated readings matter, because a set has no positions and we cannot index it. One trap to remember is that empty curly brackets create an empty dictionary. For an empty set we always write set with brackets.

## Slide 42: Set membership and repeated IDs

in returns True or False.

A set answers membership questions.

Output: 1, True, False. Adding the same ID twice keeps one distinct ID.

```python
seen = set()
seen.add("A")
seen.add("A")
print(len(seen))
print("A" in seen)
print("B" in seen)
```

**Spoken script**

We start with an empty set called seen. Then we add the letter A. We add the letter A a second time. A set keeps only one copy of each item, so the second add changes nothing.

The first print shows len of seen, which counts the items. The answer is 1, because only one distinct ID is stored.

The second print asks whether A is in seen. The word in gives back True or False, and here it is True.

The third print asks about B. We never added B, so the answer is False.

The output is 1, True, False. This is how a set answers membership questions.

## Slide 43: How the four collections differ

Choose by the question: ordered readings, named fields, fixed positions, or distinct IDs.

**Spoken script**

We now have four collections, and each answers a different kind of question. We choose by the question we are asking.

If we have ordered readings, we use a list. We find items by position and the list can change.

If we have named fields, such as a unit and a reading belonging to one record, we use a dictionary. We find items by their key.

If we have fixed positions, such as a pair of coordinates, we use a tuple. Its positions cannot be reassigned.

If we only need to know which IDs we have already seen, we use a set. It keeps each distinct item once and answers yes or no.

Before writing code, we say the question aloud and pick the collection that fits it.

## Slide 44: Dictionary items and two loop names

record.items() provides each key with its value as a pair. The loop unpacks each pair into the names key and value.

for key, value in record.items(): repeats the indented body for each field. Use .items() when both the label and its value are needed.

**Spoken script**

Often we need both the label and the value of every field in a dictionary. For that we use dot items. Record dot items gives each key together with its value as a pair.

The for line has two names after the word for, key and value, separated by a comma. Python takes each pair and unpacks it, exactly like unpacking a tuple. The first name receives the key and the second name receives the value.

The line ends with a colon, and the indented lines below it run once for every field in the record.

We use dot items when we need both the label and its value.

## Slide 45: Looping through named fields

.items() supplies pairs.

key and value are names chosen for this loop.

Output: unit A, then reading 6. The dictionary preserves insertion order.

```python
record = {"unit": "A", "reading": 6}
for key, value in record.items():
    print(key, value)
```

**Spoken script**

The record has a unit with the value A and a reading with the value 6. The for line says, for key comma value in record dot items. Dot items hands over one pair at a time.

Inside the loop, print key value prints the two names side by side. On the first pass, key holds the word unit and value holds A. On the second pass, key holds the word reading and value holds 6.

The names key and value were chosen by us for this loop. We could pick other names, as long as there are two of them, one for each part of the pair.

The output is unit A, then reading 6. The dictionary keeps its fields in the order we inserted them, so the loop visits them in that order.

## Slide 46: A position and a key find different things

Both examples return 4. Explain how each lookup finds it.

**Spoken script**

Here are two ways to reach the same number, 4. One uses a position and one uses a key, and they find it differently.

A list keeps items in order and numbers them starting at zero. When we ask for a position, Python counts along the list and returns whatever sits there. We need to know where the item is.

A dictionary keeps labels. When we ask for a key, Python looks up that label and returns the value stored under it. The place where the field was written does not matter. We need to know the label.

Both examples return 4. If a new item were added to the front of a list, the positions would shift. The label in a dictionary keeps pointing at its own value.

## Slide 47: CSV and header

CSV means comma-separated values. One line usually represents one record; a header names the columns. CSV numbers arrive as text and may need float conversion.

**Spoken script**

CSV stands for comma-separated values. It is a plain text file where each line is usually one record, and the commas separate the fields on that line.

The first line is the header. It gives a name to each column, for example unit and reading. Every line after the header is data.

There is one important detail. Everything we read from a CSV file arrives as text, even a cell that looks like a number. The text two point five is not yet a number we can add. We have to convert it with float.

So when we read a CSV, we remember two things. The header gives us names for the columns, and every cell starts out as text.

## Slide 48: One record at a time

01

A CSV is a text table with a header row.

02

DictReader uses that header for dictionary keys.

03

CSV cells begin as text, even when they look numeric.

04

float("2.5") converts text into the number 2.5.

**Spoken script**

We read a CSV file one record at a time, and there are four small ideas.

First, a CSV file is a text table, and its first line is the header row.

Second, DictReader is a tool from the csv library. It uses the header to build a dictionary for each data row, so each column name becomes a key.

Third, the cells begin as text, even when they look like numbers. If a cell holds two point five, Python holds the text, which is the characters two, a dot, and five.

Fourth, float with the text two point five in quotes converts it into the number 2.5. After that we can add it, compare it and average it.

## Slide 49: A CSV file has a header and text values

An empty field is empty text. Check the task’s rule before converting it.

**Spoken script**

A CSV file has a header and text values. The header gives the column names, and each cell below it is a piece of text.

A cell can also be empty. An empty field is empty text, which is a string with nothing in it. A blank cell means that no reading was recorded, and it holds no number at all.

If we ask float to convert empty text, Python stops with an error. So before converting we check the rule in the task. The task tells us whether to skip blank cells or treat them in some other way.

We carry this habit into the assignment. We look at the value as text first and decide what to do with it before converting.

## Slide 50: A CSV row becomes a dictionary

01

The header gives field names, such as unit and reading.

02

csv.DictReader returns one dictionary for each data row.

03

The value "2.5" starts as text. float("2.5") makes the number 2.5.

**Spoken script**

A CSV row becomes a dictionary through three steps.

The header gives the field names. If the header line says unit comma reading, then unit and reading are the names for the two columns.

Then csv dot DictReader returns one dictionary for each data row. For a row holding A and 2.5, we get a dictionary with the key unit holding A and the key reading holding 2.5.

The value 2.5 starts out as text. It sits in the dictionary in quotes. To use it as a number we write float with that text inside brackets, and we receive the number 2.5.

Once a row is a dictionary, we can ask it for any field by its key.

## Slide 51: with and import

import makes library tools available. with open(...) opens a file for a block and closes it afterward. A filename must match an existing file in the working folder.

**Spoken script**

Two small words appear in nearly every file-reading program, import and with.

Import makes a library's tools available to our program. When we write import csv, we can then use the tools of the csv library, such as DictReader.

With open, followed by the file name, opens a file for the indented block that follows. When Python leaves that block, the file is closed automatically, so we never forget to close it.

The file name in the quotes must match an existing file in the working folder. If the spelling is different, or the file has not been uploaded, Python cannot find it and reports an error. Whenever a file fails to open, the first thing we check is the exact name.

## Slide 52: Your cohort data

01

drill_shift_log.csv

02

Summarise rate_of_penetration (m/hour); group by bit_type.

03

Read the issued task’s blank-value and threshold rules before calculating.

**Spoken script**

Now we look at the data that your cohort will use. The file is drill underscore shift underscore log dot csv.

We will summarise the column rate underscore of underscore penetration, which is measured in metres per hour. We will group the rows by bit underscore type. Grouping means that we calculate one summary for each distinct label in that column.

Before calculating anything, read the issued task. It states what to do with blank values and which threshold to use. We follow those rules exactly.

## Slide 53: Read the supplied CSV in four steps

01

Place drill_shift_log.csv beside the notebook, or upload it in Colab’s Files panel.

02

import csv loads the CSV tools. newline="" lets the reader handle line endings. DictReader uses the header as dictionary keys.

03

list(...) collects the rows while the file is open. We inspect the first row and the count; the later assignment calculations are your work.

**Spoken script**

We read the supplied CSV in steps.

First, place drill underscore shift underscore log dot csv in the same folder as the notebook, or upload it in the Files panel in Colab.

Second, import csv loads the CSV tools. The newline equals empty quotes part lets the reader handle line endings correctly. DictReader then uses the header row as the dictionary keys.

Third, list with the reader inside collects all the rows into one list while the file is still open. We then inspect the first row and the count of rows.

The later calculations belong to the assignment, and they are your work.

## Slide 54: What with open as source does

01

open("file.csv", newline="") opens a text file for reading. Use the actual supplied filename, including its .csv extension.

02

with manages the open file. as source gives that file object a name. Indented lines use it while it is open; leaving the block closes it.

03

csv.DictReader(source) reads rows using the header names as keys. list(...) collects those rows into memory before the file closes.

**Spoken script**

This slide explains the line with open, as source.

Open, with the file name in quotes and newline equals empty quotes, opens a text file for reading. We write the real file name, including the dot csv ending.

The word with manages the open file. As source gives the file a name that we can use, here source. The indented lines below use the file while it is open. When we leave that block, Python closes the file for us.

Inside, csv dot DictReader with source reads the rows, using the header names as keys. List around it collects all the rows into memory. We collect them before the file closes, because after that the reader can no longer read from it.

## Slide 55: Open a real CSV and inspect its first row

with open(...) as source opens the file. as gives the open file the name source.

Read the actual keys and text values. Check the uploaded filename if Python reports FileNotFoundError.

```python
import csv
with open("drill_shift_log.csv", newline="") as source:
    rows = list(csv.DictReader(source))
print(rows[0])
print(len(rows))
```

**Spoken script**

This is the complete code for opening a real file.

Import csv loads the CSV tools. The with line opens drill underscore shift underscore log dot csv for reading and calls the open file source.

The indented line builds a list called rows. DictReader turns every data row into a dictionary, and list collects them all while the file is open.

Print rows with zero in square brackets shows the first row. Since counting starts at zero, this is the first data row. We read the actual keys, and notice that the values are still text.

Print len of rows shows how many records were read.

If Python reports FileNotFoundError, we check that the uploaded file name matches the one in the code.

## Slide 56: Numbers read from CSV

DictReader reads each row as a dictionary. CSV field values start as text. float converts a recorded numeric field to a number.

Check for an empty string before converting a blank cell.

**Spoken script**

DictReader reads each row as a dictionary. The values in those dictionaries begin as text. When a field holds a recorded number, we use float to convert it into a number.

Some cells are blank. A blank cell is an empty string, and float cannot convert an empty string. So before converting, we check for an empty string and skip the blank cell.

The list called rows from the previous example already holds all the records from the supplied file. We use the real header names we saw there as our keys.

The pattern is the same each time. We take the text from the field, check that it is not empty, and then convert it.

## Slide 57: Recorded values from the supplied rows

Each retained number comes directly from a CSV row.

Run this cell on the supplied CSV. Read the output below the cell.

```python
values = []
for row in rows:
    text = row["rate_of_penetration"]
    if text != "":
        values.append(float(text))
print(len(values))
print(values[:5])
```

**Spoken script**

We now collect the recorded numbers from the supplied rows.

Values equals empty square brackets starts an empty list. The for line visits each row in rows. Inside the loop, text equals row with rate underscore of underscore penetration in square brackets takes that row's reading, still as text.

The if line checks that the text is not equal to an empty string. A blank cell fails this check and is skipped. When a cell passes, float turns the text into a number, and values dot append adds it to the list.

After the loop, print len of values shows how many numbers were kept. Leaving out the number before the colon means start at the beginning, so values with colon 5 takes positions zero to four, and it shows fewer than five items if the list is shorter.

Run this cell on your own file and read the output below the cell. Each number comes directly from a row in your CSV.

## Slide 58: One summary for each group

Keep a totals dictionary and a counts dictionary. Initialise a new group before adding its first reading.

Add the recorded value and increment its count. Divide each total by its count to obtain the group mean.

**Spoken script**

To get one summary for each group, we keep two dictionaries. One is a totals dictionary and the other is a counts dictionary. The keys are the group labels.

When a group appears for the first time, it has no entry yet. We start it at zero before adding its first reading. The get function helps us do this in one step.

For every valid row we do two things. We add the recorded value to that group's total, and we add one to that group's count.

When all the rows are done, we divide each group's total by its own count. That gives the mean for each group. Every group uses its own count as the divisor.

## Slide 59: Grouped means from the supplied rows (1/2)

get(group, 0) returns the existing value or zero for a new group.

Run this cell on the supplied CSV. Read the output below the cell.

```python
totals = {}
counts = {}
for row in rows:
    group = row["bit_type"]
    if row["rate_of_penetration"] != "":
        value = float(row["rate_of_penetration"])
        totals[group] = totals.get(group, 0) + value
        counts[group] = counts.get(group, 0) + 1
```

**Spoken script**

This is the first half of the grouped mean calculation. We make two empty dictionaries, totals and counts.

The loop visits each row. The line group equals row with bit underscore type in square brackets picks the group label of this row.

The if line skips rows where rate underscore of underscore penetration is blank. For every other row, value equals float of that field turns the text into a number.

The next line updates the total. Totals with group in square brackets equals totals dot get of group and zero, plus value. If this group has no total yet, get returns zero, so a new group starts from zero. Otherwise it returns the running total, and we add the new value.

The count line works the same way and adds one each time.

Run this cell on your own file. It prints nothing yet.

## Slide 60: Grouped means from the supplied rows (2/2)

get(group, 0) returns the existing value or zero for a new group.

Continue the same cell with the indentation shown.

```python
means = {}
for group in totals:
    means[group] = totals[group] / counts[group]
print(means)
```

**Spoken script**

This is the second half of the grouped mean calculation, and we continue in the same cell with the same indentation.

Means equals empty curly brackets starts a new dictionary for the answers. The for line goes through the keys of totals, which are the group labels, one at a time. For each group, means with the group in square brackets receives that group's total divided by that group's count.

Each group uses its own count as the divisor. Each group's total is divided by its own count.

Print means shows the finished dictionary. It has one entry for every group, with the group label as the key and the mean as the value.

This is the pattern we use for the group means task in the assignment.

## Slide 61: Your issued assignment

01

Open W04_student.ipynb.

02

Read every task and its input units before coding.

03

Keep the required function names and returned outputs.

04

Restart and run all cells, then save the completed notebook.

**Spoken script**

This slide describes your issued assignment.

First, open the notebook called W04 underscore student dot ipynb.

Second, read every task and its input units before you start coding. Knowing what goes in and what should come out saves time.

Third, keep the required function names and the returned outputs exactly as they are in the starter code. The checks look for those names.

Fourth, when you finish, restart the notebook and run all cells from the top, to confirm that everything works in order. Then save the completed notebook.

## Slide 62: valid_count (5 marks)

Store an integer count of rows whose rate_of_penetration field is nonblank.

Skip blank readings before numeric conversion.

**Spoken script**

The first output is valid underscore count, worth five marks.

It must be an integer, a whole number. It counts the rows where the rate underscore of underscore penetration field is nonblank.

Valid means a recorded reading exists. A blank cell is a missing reading. It is no measured zero, so it is left out of the count.

We skip blank readings before any numeric conversion. If we try to convert a blank, Python raises an error.

For a small example, a column holding two, blank, four has a valid count of two.

## Slide 63: mean_reading (5 marks)

01

Store the arithmetic mean of the nonblank rate_of_penetration values as a number.

02

Add the valid readings and divide by their count.

03

Keep full precision.

**Spoken script**

The second output is mean underscore reading, worth five marks.

It is the arithmetic mean of the nonblank rate underscore of underscore penetration values, stored as a number.

First we add up the valid readings. Then we divide that total by the number of valid readings. Blank cells are left out of both the total and the count.

Keep full precision. This means we do not round the answer ourselves.

For a small example, readings two and four have a mean of three.

## Slide 64: above_limit (5 marks)

Store an integer count of valid rate_of_penetration readings strictly greater than 8.0.

A reading equal to the threshold is not counted.

**Spoken script**

The third output is above underscore limit, worth five marks.

It is an integer count of valid rate underscore of underscore penetration readings that are strictly greater than 8.0.

Strictly greater than means that a reading equal to the threshold is left out of the count. We use the greater-than sign, with no equals sign next to it.

Blank cells are not valid readings, so they are skipped.

For a small example, with readings nine, ten and eleven and a limit of ten, only eleven is above the limit, so the count is one. If we used greater than or equal to, we would count two, which would be wrong.

## Slide 65: group_means (5 marks)

01

Store a dictionary whose keys are the bit_type labels and whose values are the mean valid rate_of_penetration readings within each group.

02

Divide each group total by its own valid count.

03

Keep full precision.

**Spoken script**

The fourth output is group underscore means, worth five marks.

It is a dictionary. Its keys are the bit underscore type labels, and each value is the mean of the valid rate underscore of underscore penetration readings within that group.

Each group has its own total and its own count. We divide each group's total by that group's valid count.

Keep full precision, which means we do not round.

For a small example, group A with readings two and four has a mean of three. Group B with a single reading of nine has a mean of nine. Dividing both totals by the overall count would give wrong answers.

## Slide 66: Week 4 rules

01

Fictional teaching data.

02

300 records.

03

Three blank rate_of_penetration values must be skipped in numerical summaries.

04

Threshold 8.0 is a teaching assumption.

**Spoken script**

These are the rules for the Week 4 assignment.

The data is fictional teaching data. It does not come from a real drilling shift.

The file has 300 records.

Three rate underscore of underscore penetration values are blank. Those must be skipped in any numerical summary, so they are left out of the totals and of the counts.

The threshold of 8.0 is a teaching assumption. It is a value chosen for this exercise. We use it exactly as the task states.

## Slide 67: Week 4 rules continued

01

Compute valid_count, mean_reading, above_limit (strictly greater than 8.0) and group_means keyed by bit_type.

02

Use standard-library csv and collections.

03

Save a copy using your Student Registration Number with / replaced by _, followed by _W04.ipynb.

04

STUDENT_ID in the starter code means Student Registration Number.

**Spoken script**

These are the remaining rules for the assignment.

Compute valid underscore count, mean underscore reading, above underscore limit and group underscore means. The above limit count uses strictly greater than 8.0, and the group means are keyed by bit underscore type.

The csv module is the toolbox for reading the file, and it comes with Python. The collections module is another built-in toolbox that you may use, though nothing this week requires it. They come with Python, so nothing needs installing.

Save a copy of the notebook named with your Student Registration Number, where the forward slash is replaced by an underscore, followed by underscore W04 dot ipynb.

In the starter code, STUDENT underscore ID means your Student Registration Number. Enter your own number there.

## Slide 68: Week 4 rules continued

01

Four checks carry five marks each.

02

Explain the interesting pattern separately as formative practice.

03

For beginner step-by-step help, open ASSIGNMENT_INSTRUCTIONS.txt and STUDENT_HOW_TO.md in this folder.

04

The first names your required files and hand-in checklist; the second explains accounts, Colab, saving and uploads.

**Spoken script**

Here are the last rules for the assignment.

There are four checks, and each carries five marks.

Explaining the interesting pattern you find in the data is separate. It is formative practice, so it helps your learning, and it sits outside the four marked checks.

If you want step-by-step help as a beginner, open the two files in this folder, ASSIGNMENT underscore INSTRUCTIONS dot txt and STUDENT underscore HOW underscore TO dot md.

The first one names your required files and the hand-in checklist. The second explains accounts, Colab, saving and uploads.

## Slide 69: Reading report submission

01

Opens: 02 Oct 2026, 08:00 Kampala

02

Deadline: 09 Oct 2026, 08:00 Kampala

03

Use your full Student Registration Number in the form.

04

Keep the submitted files and confirmation.

Open W04 assignment form

https://docs.google.com/forms/d/e/1FAIpQLSenqAHKxNgzxWHIR41scC7h5WAxcs8D9wOyXYjIQ_ulbGpPCw/viewform

**Spoken script**

This slide is for submitting your Week 4 assignment. Check the opening time and the deadline shown on the slide, and use the button to open the form.

In the form, type your full Student Registration Number. Then upload your completed notebook.

Keep the files you submitted and the confirmation the form gives you. If something goes wrong, they are your evidence of what you handed in.

## Slide 70: Week 4 quiz

01

Answer individually after the lecturer activates the quiz.

02

Available for 24 hours from activation.

03

Use your Student Registration Number and registered account.

04

Check the announced quiz closing time.

Open this week’s quiz

https://forms.gle/YbPS4yzALy4tB1YM7

**Spoken script**

This is the Week 4 quiz. You answer it individually, and you open it using the link on the slide.

The quiz opens when the lecturer activates it. It then stays open for 24 hours. The closing time is the one the lecturer announces.

Use your Student Registration Number and your registered account when you enter your answers.

The quiz stays available for the full 24 hours, so you do not need to rush.

## Slide 71: Revision and submission checklist

You can show how the total and count change for each record.

Save your work and check the required submission files.

Point to your evidence. Save your work.

**Spoken script**

We close with a checklist for revising this week and for submitting your work.

You can explain how the total and the count change for each record. Take readings two, four and six. The running total goes two, then six, then twelve. The count reaches three, and the mean is twelve divided by three, which is four. With groups, each group has its own total and its own count.

You can say what each collection is for. Lists keep ordered values. Loops visit them. Dictionaries label the fields. CSV files store the observations.

Save your work. Then check that you have the required submission files, and point to them as evidence that the work is done.
