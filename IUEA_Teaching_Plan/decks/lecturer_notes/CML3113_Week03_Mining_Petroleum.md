# CML3113 Week03 Mining Petroleum

Lecturer companion to the revised PowerPoint. Slide numbers match this edition. Explain the worked examples directly; revision checks are for individual study.

## Slide 1 — Python calculations and reusable functions

PURPOSE
Python calculations and reusable functions

CONNECT
Previous slide: the preceding week.

EXPLAIN
Mining and Petroleum Engineering

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
Previous slide: Python calculations and reusable functions.

EXPLAIN
Read Python values and arithmetic symbols.

Define a function, call it and check its inputs.

LECTURER CUE
Ask learners to explain this goal in ordinary language. The first successful attempt matters more than covering optional extensions. Defer: Five-function libraries, module imports, scope details, debugger setup and six independent bug hunts can wait. Demonstrate one ordinary traceback and one unit mistake now.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
How to read the examples.

REFERENCES


## Slide 3 — How to read the examples

PURPOSE
How to read the examples

CONNECT
Previous slide: Today’s learning.

EXPLAIN
Each example separates the instructions you type from the output Python displays.

The lecturer explains the symbols first, then runs the example and traces its result. Keep the displayed output for revision.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
The engineering context.

REFERENCES


## Slide 4 — The engineering context

PURPOSE
The engineering context

CONNECT
Previous slide: How to read the examples.

EXPLAIN
A pump team records temperature to investigate operation.

Mining students can relate this to a dewatering pump; petroleum students to a transfer pump.

These are teaching examples, not operating limits.

LECTURER CUE
A pump team records temperature to investigate operation. Mining students can relate this to a dewatering pump; petroleum students to a transfer pump. These are teaching examples, not operating limits.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Start with numbers and values.

REFERENCES


## Slide 5 — Start with numbers and values

PURPOSE
Start with numbers and values

CONNECT
Previous slide: The engineering context.

EXPLAIN
Number: A number expresses how much or how many: 3 items or 2.5 metres. Whole numbers count; decimal numbers can describe a part of a unit.

Value and unit: A value is one piece of information. The number 2.5 is a value. A measurement also needs a unit, such as metres. Python does not attach that unit automatically.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Words we will use.

REFERENCES


## Slide 6 — Words we will use

PURPOSE
Words we will use

CONNECT
Previous slide: Start with numbers and values.

EXPLAIN
Variable: A name referring to a value. In length_m = 5, the right side is evaluated and assigned to length_m.

int, float, str, bool: int represents whole numbers; float represents approximate real numbers such as 2.5; str is text in quotes; bool is True or False.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A variable refers to its current value.

REFERENCES


## Slide 7 — A variable refers to its current value

PURPOSE
A variable refers to its current value

CONNECT
Previous slide: Words we will use.

EXPLAIN
After reassignment, thickness refers to 0.20.

LECTURER CUE
This box is a simplified model of a name referring to a value. Other names could still refer to an earlier object.
Source: existing course illustration figs/variable_box.png. These are illustrative examples, not this cohort’s assessed results.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Python values have types.

REFERENCES
Source: existing course illustration figs/variable_box.png. These are illustrative examples, not this cohort’s assessed results.

## Slide 8 — Python values have types

PURPOSE
Python values have types

CONNECT
Previous slide: A variable refers to its current value.

EXPLAIN
Type | Example | Meaning

int | 3 | Whole number

float | 3.5 | Decimal approximation

str | "3.5" | Text in quotes

bool | True / False | Logical value

NoneType | None | No value supplied

3.5 + 2 gives 5.5. "3.5" + "2" joins text into "3.52".

LECTURER CUE
3.5 + 2 gives 5.5. "3.5" + "2" joins text into "3.52".

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Operator.

REFERENCES


## Slide 9 — Operator

PURPOSE
Operator

CONNECT
Previous slide: Python values have types.

EXPLAIN
Operator: A symbol for an operation: + adds, - subtracts, * multiplies, / divides, ** raises to a power. // floors a quotient, so -5 // 2 is -3.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Read a function call before using it.

REFERENCES


## Slide 10 — Read a function call before using it

PURPOSE
Read a function call before using it

CONNECT
Previous slide: Operator.

EXPLAIN
A built-in function: Python already provides tools such as print, type and float. A function call asks a named tool to do its work: print(3) displays 3.

Parentheses, quotes and comments: Parentheses hold the inputs to a call. Quotes make text: "3.5" is text; float("3.5") converts it to a number. # starts a comment that Python does not run.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Reading Python symbols.

REFERENCES


## Slide 11 — Reading Python symbols

PURPOSE
Reading Python symbols

CONNECT
Previous slide: Read a function call before using it.

EXPLAIN
= assigns a value to a name. == compares two values.

* multiplies. / divides. ** raises to a power.

Parentheses pass inputs when we call a function.

Indented lines belong to the block above them.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Names, conversion and comments.

REFERENCES


## Slide 12 — Names, conversion and comments

PURPOSE
Names, conversion and comments

CONNECT
Previous slide: Reading Python symbols.

EXPLAIN
Read the code in this order:
length_m = float("3.5")  # text to number
width_m = 2
area_m2 = length_m * width_m
print(area_m2)
print(type(length_m))

float converts numeric text into a decimal number.

type reports the kind of value: for example, float.

print displays a value below the cell.

type(...) reports the kind of value. <class 'float'> means a floating-point number.

LECTURER CUE
Read each symbol before running. Ask everyone to predict. Expected output: 7.0 then <class 'float'>

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Week 3 continuation.

REFERENCES


## Slide 13 — Week 3 continuation

PURPOSE
Week 3 continuation

CONNECT
Previous slide: Names, conversion and comments.

EXPLAIN
From slides 1–12: values have types, variables name values, = assigns, and print displays a result. float("3.5") converts text to a number. We now use those ideas in calculations and functions.

Next: arithmetic, decisions, functions, then lists and the A3 brief.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Reading a Python expression.

REFERENCES


## Slide 14 — Reading a Python expression

PURPOSE
Reading a Python expression

CONNECT
Previous slide: Week 3 continuation.

EXPLAIN
An expression is code that produces a value. In 7 + 2, the inputs are 7 and 2; the operator + tells Python to add them.

A statement is an instruction. total = 7 + 2 calculates 9, then gives it the name total. print(total) displays the stored value.

Read each symbol before running. Code is what you type; output is what Python displays. Do not type the word “Output”.



Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Addition subtraction multiplication and division.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 15 — Addition subtraction multiplication and division

PURPOSE
Addition subtraction multiplication and division

CONNECT
Previous slide: Reading a Python expression.

EXPLAIN
Operator | Meaning | Example and result

+ | Add | 7 + 2 gives 9

- | Subtract | 7 - 2 gives 5

* | Multiply | 7 * 2 gives 14

/ | Divide | 7 / 2 gives 3.5

Python uses * for multiplication, not ×. / can produce a fractional result.

Read the rows in order. Python uses * for multiplication, not ×. / can produce a fractional result.

Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Run the four arithmetic operations.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 16 — Run the four arithmetic operations

PURPOSE
Run the four arithmetic operations

CONNECT
Previous slide: Addition subtraction multiplication and division.

EXPLAIN
Read the code in this order:
print(7 + 2)
print(7 - 2)
print(7 * 2)
print(7 / 2)

Each print call displays one calculated result.

The numbers have no units until we assign a meaning to them.

Output: 9; 5; 14; 3.5

Expected printed output:
9
5
14
3.5

Run the complete cell, then trace each line. Expected output:
9
5
14
3.5

Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Floor division remainder and powers.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 17 — Floor division remainder and powers

PURPOSE
Floor division remainder and powers

CONNECT
Previous slide: Run the four arithmetic operations.

EXPLAIN
Operator | Meaning | Example and result

// | Floor the quotient | 7 // 2 gives 3

% | Remainder | 7 % 2 gives 1

** | Raise to a power | 2 ** 3 gives 8

7 contains three groups of 2 with 1 left over: 7 = 3 × 2 + 1.

Read the rows in order. 7 contains three groups of 2 with 1 left over: 7 = 3 × 2 + 1.

Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Reading powers signs and remainders.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 18 — Reading powers signs and remainders

PURPOSE
Reading powers signs and remainders

CONNECT
Previous slide: Floor division remainder and powers.

EXPLAIN
2 ** 3 means 2 × 2 × 2. It does not mean 2 × 3. The left value is the base; the right value is the exponent.

A leading minus makes a number negative: -7. Floor division rounds the quotient down: -7 / 2 is -3.5, so -7 // 2 is -4.

% is remainder, not percentage. To turn 75% into a fraction, calculate 75 / 100. Do not divide by zero.



Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Run floor division remainder and powers.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 19 — Run floor division remainder and powers

PURPOSE
Run floor division remainder and powers

CONNECT
Previous slide: Reading powers signs and remainders.

EXPLAIN
Read the code in this order:
print(7 // 2)
print(7 % 2)
print(2 ** 3)
print(-7 // 2)
print(75 / 100)

** repeats multiplication.

A negative floor result rounds toward the smaller integer.

Output: 3; 1; 8; -4; 0.75

Expected printed output:
3
1
8
-4
0.75

Run the complete cell, then trace each line. Expected output:
3
1
8
-4
0.75

Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Which operation happens first.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 20 — Which operation happens first

PURPOSE
Which operation happens first

CONNECT
Previous slide: Run floor division remainder and powers.

EXPLAIN
Parentheses group a calculation: do (2 + 3) before multiplying it by 4.

Powers come before multiplication and division. Multiplication, /, // and % come before addition and subtraction. Equal-level * and / run left to right.

Use parentheses when the intended grouping might be unclear. For a negative base, write (-2) ** 2. This gives 4; -(2 ** 2) gives -4.



Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Trace an expression before its output.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 21 — Trace an expression before its output

PURPOSE
Trace an expression before its output

CONNECT
Previous slide: Which operation happens first.

EXPLAIN
Expression | First calculation | Result

2 + 3 * 4 | 3 * 4 gives 12 | 2 + 12 gives 14

(2 + 3) * 4 | 2 + 3 gives 5 | 5 * 4 gives 20

12 / 3 * 2 | 12 / 3 gives 4.0 | 4.0 * 2 gives 8.0

Changing parentheses can change the answer even when the numbers stay the same.

Read the rows in order. Changing parentheses can change the answer even when the numbers stay the same.

Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Check operation order.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 22 — Check operation order

PURPOSE
Check operation order

CONNECT
Previous slide: Trace an expression before its output.

EXPLAIN
Read the code in this order:
print(2 + 3 * 4)
print((2 + 3) * 4)
print(12 / 3 * 2)

Read the calculation from the trace table.

Run first; then compare with the shown outputs.

Output: 14; 20; 8.0

Expected printed output:
14
20
8.0

Run the complete cell, then trace each line. Expected output:
14
20
8.0

Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Assigning and updating a named value.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 23 — Assigning and updating a named value

PURPOSE
Assigning and updating a named value

CONNECT
Previous slide: Check operation order.

EXPLAIN
count = 2 gives the name count the value 2. = means assignment; it does not ask whether two values are equal.

count = count + 1 first reads the old value 2, calculates 3, then assigns 3 back to count.

After the update, print(count) displays 3. Re-running only the update cell changes count again; restart and run from the beginning for the shown result.



Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Trace one update.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 24 — Trace one update

PURPOSE
Trace one update

CONNECT
Previous slide: Assigning and updating a named value.

EXPLAIN
Read the code in this order:
count = 2
print(count)
count = count + 1
print(count)

The right side is calculated before the left side changes.

Output: 2; 3

Expected printed output:
2
3

Run the complete cell, then trace each line. Expected output:
2
3

Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Numbers text and conversion.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 25 — Numbers text and conversion

PURPOSE
Numbers text and conversion

CONNECT
Previous slide: Trace one update.

EXPLAIN
7 is an integer. 7.0 is a decimal-valued float. "7" is text because it is inside quotes. Both single and double quotes can enclose text.

"7" + "2" joins text into "72". To add those digits as numbers, convert each first: int("7") + int("2") gives 9.

int converts valid integer text; float converts valid decimal text. str turns a value into text. print displays a value; type reports its Python type.



Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Compare numeric addition with text joining.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 26 — Compare numeric addition with text joining

PURPOSE
Compare numeric addition with text joining

CONNECT
Previous slide: Numbers text and conversion.

EXPLAIN
Read the code in this order:
print(7 + 2)
print("7" + "2")
print(int("7") + int("2"))
print(float("2.5"))

Quotes change the type and therefore what + does.

Conversion happens before the addition.

Output: 9; 72; 9; 2.5

Expected printed output:
9
72
9
2.5

Run the complete cell, then trace each line. Expected output:
9
72
9
2.5

Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Arithmetic that needs care.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 27 — Arithmetic that needs care

PURPOSE
Arithmetic that needs care

CONNECT
Previous slide: Compare numeric addition with text joining.

EXPLAIN
Parentheses run first: (2 + 4) / 2 is 3.0. Without them, division runs before addition: 2 + 4 / 2 is 4.0.

/ gives a quotient. // rounds that quotient down: 7 // 2 is 3 and -7 // 2 is -4.

Many decimal fractions are approximate in a computer. A tolerance is an allowed difference, for example 0.01 m when checking two calculated lengths.

LECTURER CUE
Floor division rounds down. Use parentheses to state the intended calculation. Keep units in variable names.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Read the quantities in your programme example.

REFERENCES


## Slide 28 — Read the quantities in your programme example

PURPOSE
Read the quantities in your programme example

CONNECT
Previous slide: Arithmetic that needs care.

EXPLAIN
Volume, time and flow: Volume is how much space fluid occupies, here in litres. Time is measured in seconds. Flow is volume divided by time, in litres per second.

Density and pressure: Density is mass per volume in kg/m³. Pressure is force per area, measured in pascals (Pa). 1000 Pa = 1 kPa. Fluid density and depth determine the hydrostatic contribution.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A calculation for your programme.

REFERENCES


## Slide 29 — A calculation for your programme

PURPOSE
A calculation for your programme

CONNECT
Previous slide: Read the quantities in your programme example.

EXPLAIN
A pump moves 18 litres in 3 seconds.

Flow = volume ÷ time = 6 litres per second.

LECTURER CUE
A pump moves 18 litres in 3 seconds. Flow = volume ÷ time = 6 litres per second.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
The calculation in Python.

REFERENCES


## Slide 30 — The calculation in Python

PURPOSE
The calculation in Python

CONNECT
Previous slide: A calculation for your programme.

EXPLAIN
Read the code in this order:
volume_l = 18
time_s = 3
flow_l_s = volume_l / time_s
print(flow_l_s)

print displays a value below the cell.

= assigns the value on the right to the name on the left.

Read top to bottom. Run the complete example in the matching practice notebook.

LECTURER CUE
Read each name and unit. = assigns the number, * multiplies and / divides. print displays the result. A pump moves 18 litres in 3 seconds. Flow = volume ÷ time = 6 litres per second.

Complete practice code:
volume_l = 18
time_s = 3
flow_l_s = volume_l / time_s
print(flow_l_s)

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Reading an error message.

REFERENCES


## Slide 31 — Reading an error message

PURPOSE
Reading an error message

CONNECT
Previous slide: The calculation in Python.

EXPLAIN
Message | Meaning | First check

NameError | A name is unavailable | Spelling and run order

TypeError | Wrong kind of value | Text versus number

SyntaxError | Python cannot parse a line | Quotes, brackets, colon

IndentationError | Block spacing is invalid | Consistent spaces

The last line names the error. The indicated line shows where Python noticed it.

LECTURER CUE
Read one row at a time and use a changed value. This is a syntax reference for the worked examples.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A comparison produces a Boolean value.

REFERENCES


## Slide 32 — A comparison produces a Boolean value

PURPOSE
A comparison produces a Boolean value

CONNECT
Previous slide: Reading an error message.

EXPLAIN
A comparison asks a yes/no question about values. Its Python result is True or False, written with capital first letters and no quotes.

30 >= 30 asks “Is 30 at least 30?” The answer is True. 28 >= 30 gives False.

True and False have type bool. "False" is text, not the Boolean value False. Conditions use Boolean results to choose what happens next.



Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Equality and difference.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 33 — Equality and difference

PURPOSE
Equality and difference

CONNECT
Previous slide: A comparison produces a Boolean value.

EXPLAIN
Symbol | Question | Example and result

== | Equal values? | 3 == 3 gives True

!= | Different values? | 3 != 4 gives True

= assigns a value. == compares values. They have different jobs.

Read the rows in order. = assigns a value. == compares values. They have different jobs.

Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Comparing sizes and boundaries.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 34 — Comparing sizes and boundaries

PURPOSE
Comparing sizes and boundaries

CONNECT
Previous slide: Equality and difference.

EXPLAIN
Symbol | Question | Example and result

> | Greater than? | 3 > 3 gives False

>= | Greater than or equal? | 3 >= 3 gives True

< | Less than? | 2 < 3 gives True

<= | Less than or equal? | 3 <= 3 gives True

The = part of >= and <= includes the boundary value.

Read the rows in order. The = part of >= and <= includes the boundary value.

Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Display comparison results.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 35 — Display comparison results

PURPOSE
Display comparison results

CONNECT
Previous slide: Comparing sizes and boundaries.

EXPLAIN
Read the code in this order:
reading = 30
print(reading == 30)
print(reading != 30)
print(reading > 30)
print(reading >= 30)
print(reading < 30)
print(reading <= 30)

Each comparison produces a Boolean.

No branch has run yet; print only displays the answers.

Output: True; False; False; True; False; True

Expected printed output:
True
False
False
True
False
True

Run the complete cell, then trace each line. Expected output:
True
False
False
True
False
True

Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A condition and an if block.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 36 — A condition and an if block

PURPOSE
A condition and an if block

CONNECT
Previous slide: Display comparison results.

EXPLAIN
A condition is the question tested by an if statement. if reading >= 30: checks whether reading is at least 30.

The colon ends the header. The next line starts with four spaces; those spaces place it inside the block controlled by if.

If the condition is True, run the block. If it is False, skip it. The next line without those four spaces is outside the block and runs afterwards.



Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
An if statement without else.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 37 — An if statement without else

PURPOSE
An if statement without else

CONNECT
Previous slide: A condition and an if block.

EXPLAIN
Read the code in this order:
reading = 28
if reading >= 30:
    print("warm")
print("check finished")

28 >= 30 is False, so the indented print is skipped.

The final print is outside the block.

Output: check finished

Expected printed output:
check finished

Run the complete cell, then trace each line. Expected output:
check finished

Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Trace both paths through if.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 38 — Trace both paths through if

PURPOSE
Trace both paths through if

CONNECT
Previous slide: An if statement without else.

EXPLAIN
Value of reading | reading >= 30 | Displayed lines

28 | False | check finished

30 | True | warm; check finished

31 | True | warm; check finished

Only the indented line is conditional. The outside line runs on either path.

Read the rows in order. Only the indented line is conditional. The outside line runs on either path.

Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
else gives the other path.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 39 — else gives the other path

PURPOSE
else gives the other path

CONNECT
Previous slide: Trace both paths through if.

EXPLAIN
else means “otherwise”. It has a colon but no extra condition. Align else with its matching if.

The if block runs when its condition is True. The else block runs when that same condition is False. Only one of these blocks runs.

Both branch bodies are indented by four spaces. Returning to the left margin ends the whole decision.



Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A decision needs a colon and indentation.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 40 — A decision needs a colon and indentation

PURPOSE
A decision needs a colon and indentation

CONNECT
Previous slide: else gives the other path.

EXPLAIN
Read the code in this order:
temperature = 28
if temperature >= 30:
    print("warm")
else:
    print("below 30")

if tests a condition. The chosen indented block runs.

print displays a value below the cell.

= assigns the value on the right to the name on the left.

>= compares values. Only the chosen indented block runs.

LECTURER CUE
Read each symbol before running. Ask everyone to predict. Expected output: below 30. Change 28 to 30 and predict warm. This is a toy threshold, not an engineering limit.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Trace both paths through if else.

REFERENCES


## Slide 41 — Trace both paths through if else

PURPOSE
Trace both paths through if else

CONNECT
Previous slide: A decision needs a colon and indentation.

EXPLAIN
temperature | temperature >= 30 | Selected output

28 | False | below 30

30 | True | warm

31 | True | warm

Re-run the complete previous example for each value. Exactly one branch prints.

Read the rows in order. Re-run the complete previous example for each value. Exactly one branch prints.

Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
More than two branches.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 42 — More than two branches

PURPOSE
More than two branches

CONNECT
Previous slide: Trace both paths through if else.

EXPLAIN
if tests the first condition. elif means “otherwise, if” and tests another condition only if the earlier one was false. else handles the remaining case.

Python runs only the first matching branch. Put a narrower condition before a broader one that would also match. A colon and indentation mark each body.

LECTURER CUE
Teach these concepts before the weekly quiz. Use changed numbers for practice. This slide supplies concepts, not the quiz key.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Tracing an if elif else chain.

REFERENCES


## Slide 43 — Tracing an if elif else chain

PURPOSE
Tracing an if elif else chain

CONNECT
Previous slide: More than two branches.

EXPLAIN
Read the code in this order:
level = 7
if level >= 10:
    print("high")
elif level >= 5:
    print("medium")
else:
    print("low")

elif is checked only after the earlier condition fails.

Output: medium. The first condition is false; the second is true.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Trace the if elif else chain.

REFERENCES


## Slide 44 — Trace the if elif else chain

PURPOSE
Trace the if elif else chain

CONNECT
Previous slide: Tracing an if elif else chain.

EXPLAIN
level | Tests in order | Output

7 | 7 >= 10: False; 7 >= 5: True | medium

10 | 10 >= 10: True; stop testing | high

3 | 3 >= 10: False; 3 >= 5: False | low

Python stops at the first True branch. else runs when neither test passes.

Read the rows in order. Python stops at the first True branch. else runs when neither test passes.

Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Combining and reversing conditions.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 45 — Combining and reversing conditions

PURPOSE
Combining and reversing conditions

CONNECT
Previous slide: Trace the if elif else chain.

EXPLAIN
and asks for both conditions to be True. or asks for at least one to be True. not reverses a Boolean answer.

Use parentheses to make each comparison readable: (reading >= 20) and (reading <= 30). This is an inclusive range check.

For these lessons we combine comparisons, so their results are Boolean. Python also permits other operand types; those are not needed for the shown checks.



Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
and and or with Boolean inputs.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 46 — and and or with Boolean inputs

PURPOSE
and and or with Boolean inputs

CONNECT
Previous slide: Combining and reversing conditions.

EXPLAIN
Inputs | and result | or result

True, True | True | True

True, False | False | True

False, True | False | True

False, False | False | False

not True gives False; not False gives True.

Read the rows in order. not True gives False; not False gives True.

Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Check a permitted range.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 47 — Check a permitted range

PURPOSE
Check a permitted range

CONNECT
Previous slide: and and or with Boolean inputs.

EXPLAIN
Read the code in this order:
reading = 25
inside = (reading >= 20) and (reading <= 30)
print(inside)
print((reading < 20) or (reading > 30))
print(not inside)

Both range comparisons are True.

The outside-range comparisons are both False.

Output: True; False; False

Expected printed output:
True
False
False

Run the complete cell, then trace each line. Expected output:
True
False
False

Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Why a zero check comes first.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 48 — Why a zero check comes first

PURPOSE
Why a zero check comes first

CONNECT
Previous slide: Check a permitted range.

EXPLAIN
Python evaluates and from left to right. When the first Boolean comparison is False, it does not need to evaluate the second.

For a simple zero guard, use if denominator == 0: before the division and return or handle that case explicitly.

We will demonstrate that guard inside a function after learning how def and return work.



Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Function.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 49 — Function

PURPOSE
Function

CONNECT
Previous slide: Why a zero check comes first.

EXPLAIN
Function: A named, reusable calculation or procedure. def introduces its definition. Parameters are the names for its inputs; arguments are the values supplied when calling it.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Indentation and return.

REFERENCES


## Slide 50 — Indentation and return

PURPOSE
Indentation and return

CONNECT
Previous slide: Function.

EXPLAIN
Indentation and return: Spaces at the start of a line group the function body. return hands a result to the calling code. print displays a value and returns None.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A function definition and a call.

REFERENCES


## Slide 51 — A function definition and a call

PURPOSE
A function definition and a call

CONNECT
Previous slide: Indentation and return.

EXPLAIN
def gives a reusable calculation a name and inputs.

Defining a function remembers the instructions.

Calling the function runs those instructions with values.

return sends the result back to the caller.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Inputs, instructions and a returned result.

REFERENCES


## Slide 52 — Inputs, instructions and a returned result

PURPOSE
Inputs, instructions and a returned result

CONNECT
Previous slide: A function definition and a call.

EXPLAIN
The illustration uses slab_volume: length × width × thickness. The next function uses the same input/body/return pattern.

LECTURER CUE
Read def, the name, parameters, colon, indentation, return and call. Definition creates the function. Its body waits for a call. Distinguish print, which displays, from return, which passes a value back.
Source: existing course illustration figs/function_anatomy.png. These are illustrative examples, not this cohort’s assessed results.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Defining and calling double_value.

REFERENCES
Source: existing course illustration figs/function_anatomy.png. These are illustrative examples, not this cohort’s assessed results.

## Slide 53 — Defining and calling double_value

PURPOSE
Defining and calling double_value

CONNECT
Previous slide: Inputs, instructions and a returned result.

EXPLAIN
Read the code in this order:
def double_value(x):
    return x * 2

answer = double_value(4)
print(answer)

def names the function. Inputs go inside parentheses.

return sends the result back to the caller.

Output: 8. Calling passes 4 to x; return sends 8 back; print displays it.

LECTURER CUE
Work the cohort formula by hand before opening Python. State every unit. Use the four-line cohort calculation first; do not begin with formatting, imports or a long function. Introduce one reusable calculation using the example below. Read def, the function name, parentheses, parameter, colon, indentation and return separately. Defining the function does not run its body. Calling double_value(4) supplies 4 for x, calculates 8 and returns 8. The outer print displays it. Then teach an if/else guard with a separate small example.

Complete practice code:
def double_value(x):
    return x * 2

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Trace one function call.

REFERENCES


## Slide 54 — Trace one function call

PURPOSE
Trace one function call

CONNECT
Previous slide: Defining and calling double_value.

EXPLAIN
Step | What Python does | Value

Define | Store the body; do not run it | No printed output

Call double_value(4) | Give parameter x the argument | x is 4

return x * 2 | Calculate and return | 8

Assign and print | Store returned 8 in answer; display | 8

return sends a value back to the caller. print displays it. These are different actions.

Read the rows in order. return sends a value back to the caller. print displays it. These are different actions.

Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Passing inputs by position or by name.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 55 — Passing inputs by position or by name

PURPOSE
Passing inputs by position or by name

CONNECT
Previous slide: Trace one function call.

EXPLAIN
In def rectangle_area(length, width):, length and width are parameter names. A call supplies an argument value for each.

rectangle_area(3, 2) binds 3 to length and 2 to width by position. rectangle_area(width=2, length=3) binds them by name.

The = inside a named argument labels an input for the call. Both calls run the same function body with the same two values.



Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Positional and named inputs.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 56 — Positional and named inputs

PURPOSE
Positional and named inputs

CONNECT
Previous slide: Passing inputs by position or by name.

EXPLAIN
Read the code in this order:
def rectangle_area(length, width):
    return length * width

print(rectangle_area(3, 2))
print(rectangle_area(width=2, length=3))

def names the function. Inputs go inside parentheses.

return sends the result back to the caller.

print displays a value below the cell.

Both calls supply the same inputs. return makes the result reusable.

LECTURER CUE
Read each symbol before running. Ask everyone to predict. Expected output: 6 then 6

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
None means there is no result value.

REFERENCES


## Slide 57 — None means there is no result value

PURPOSE
None means there is no result value

CONNECT
Previous slide: Positional and named inputs.

EXPLAIN
None is a Python value used here to mean “no calculated answer”. It is not zero, an empty string, or the word "None".

A function returns None explicitly with return None. A function also returns None if it reaches its end without a return value.

A caller must handle None before trying arithmetic with the result. The next example returns it for division by zero.



Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
An input check before division.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 58 — An input check before division

PURPOSE
An input check before division

CONNECT
Previous slide: None means there is no result value.

EXPLAIN
Division by zero raises ZeroDivisionError. We choose to return None when people is zero, so there is no calculated share.

The check belongs inside the function, before the division. return ends that call immediately. A valid input follows the later return line.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A function with a zero-input check.

REFERENCES


## Slide 59 — A function with a zero-input check

PURPOSE
A function with a zero-input check

CONNECT
Previous slide: An input check before division.

EXPLAIN
Read the code in this order:
def safe_share(total, people):
    if people == 0:
        return None
    return total / people

print(safe_share(12, 3))

def names the function. Inputs go inside parentheses.

if tests a condition. The chosen indented block runs.

return sends the result back to the caller.

Output: 4.0. safe_share(12, 0) returns None before any division.

LECTURER CUE
Work the cohort formula by hand before opening Python. State every unit. Use the four-line cohort calculation first; do not begin with formatting, imports or a long function. Introduce one reusable calculation using the example below. Read def, the function name, parentheses, parameter, colon, indentation and return separately. Defining the function does not run its body. Calling double_value(4) supplies 4 for x, calculates 8 and returns 8. The outer print displays it. Then teach an if/else guard with a separate small example.

Complete practice code:
def safe_share(total, people):
    if people == 0:
        return None
    return total / people

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Trace the division guard.

REFERENCES


## Slide 60 — Trace the division guard

PURPOSE
Trace the division guard

CONNECT
Previous slide: A function with a zero-input check.

EXPLAIN
Call | First test | Returned result

safe_share(12, 3) | 3 == 0 is False | 12 / 3 gives 4.0

safe_share(12, 0) | 0 == 0 is True | None; division is skipped

return ends this function call immediately. Later lines inside it do not run.

Read the rows in order. return ends this function call immediately. Later lines inside it do not run.

Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A branch with a clear boundary.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 61 — A branch with a clear boundary

PURPOSE
A branch with a clear boundary

CONNECT
Previous slide: Trace the division guard.

EXPLAIN
Read from the top. >= includes the boundary.

Only the selected branch runs.

Try the value exactly at 10 as well as 9 and 11.

LECTURER CUE
Read from the top. >= includes the boundary. Only the selected branch runs. Try the value exactly at 10 as well as 9 and 11.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A branch with a clear boundary in Python.

REFERENCES


## Slide 62 — A branch with a clear boundary in Python

PURPOSE
A branch with a clear boundary in Python

CONNECT
Previous slide: A branch with a clear boundary.

EXPLAIN
Read the code in this order:
def check_level(value):
    if value >= 10:
        return "high"
    return "low"

print(check_level(10))
print(check_level(9))

def names the function. Inputs go inside parentheses.

if tests a condition. The chosen indented block runs.

return sends the result back to the caller.

Read top to bottom. Run the complete example in the matching practice notebook.

LECTURER CUE
Read from the top. >= includes the boundary. Only the selected branch runs. Try the value exactly at 10 as well as 9 and 11.

Complete practice code:
def check_level(value):
    if value >= 10:
        return "high"
    return "low"

print(check_level(10))
print(check_level(9))

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
One value and a collection of values.

REFERENCES


## Slide 63 — One value and a collection of values

PURPOSE
One value and a collection of values

CONNECT
Previous slide: A branch with a clear boundary in Python.

EXPLAIN
A variable can refer to one value: reading = 98. A collection stores several related values under one name.

Python has several collection types. Choose one according to how you need to find, change or organise its contents.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Lists dictionaries tuples and sets.

REFERENCES


## Slide 64 — Lists dictionaries tuples and sets

PURPOSE
Lists dictionaries tuples and sets

CONNECT
Previous slide: One value and a collection of values.

EXPLAIN
Type | Example | Choose it for

list | [98, 105, 92] | Values in a changeable order

dict | {"reading": 98} | Values found by named keys

tuple | (2, 3) | Positions you will not reassign

set | {"A", "B"} | Distinct items and membership

List and tuple positions start at zero. Dictionaries use keys. Sets have no positional index.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A list stores values in positions.

REFERENCES


## Slide 65 — A list stores values in positions

PURPOSE
A list stores values in positions

CONNECT
Previous slide: Lists dictionaries tuples and sets.

EXPLAIN
readings = [98, 105, 92] creates a list. Square brackets enclose the items; commas separate them.

An index is an item’s position. Python starts counting at zero: readings[0] is 98, readings[1] is 105, readings[2] is 92.

Three items have positions 0, 1 and 2. readings[3] raises IndexError because there is no fourth item.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Count items before choosing a position.

REFERENCES


## Slide 66 — Count items before choosing a position

PURPOSE
Count items before choosing a position

CONNECT
Previous slide: A list stores values in positions.

EXPLAIN
len(readings) is a built-in function call that returns how many items the list contains. len([98, 105, 92]) is 3.

A count and an index are different: the count is 3, while the valid positions are 0, 1 and 2.

print(readings) displays the whole list. print(readings[0]) displays only the value at its first position.



Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Creating and reading a list.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 67 — Creating and reading a list

PURPOSE
Creating and reading a list

CONNECT
Previous slide: Count items before choosing a position.

EXPLAIN
Read the code in this order:
readings = [98, 105, 92]
print(readings)
print(readings[0])
print(len(readings))

[ ] creates a list or selects a position.

len counts the items; it is a built-in function.

Output: [98, 105, 92], then 98, then 3.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Choosing the right collection.

REFERENCES


## Slide 68 — Choosing the right collection

PURPOSE
Choosing the right collection

CONNECT
Previous slide: Creating and reading a list.

EXPLAIN
A dictionary connects a key to a value: {"reading": 98}. The colon connects them; record["reading"] finds the value by its key.

A tuple such as (2, 3) stores ordered items whose positions cannot be reassigned. A set such as {"A", "B"} stores distinct items without positions.

We use a list for today’s readings because their order matters. Week 4 develops dictionary, tuple and set operations before we use them with records.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A method belongs to a value.

REFERENCES


## Slide 69 — A method belongs to a value

PURPOSE
A method belongs to a value

CONNECT
Previous slide: Choosing the right collection.

EXPLAIN
A function is called by name: len(readings). A method is called through a value with a dot: readings.index(105).

index searches a list for a value and returns its first position. Here readings.index(105) returns 1. A missing value raises ValueError.

The parentheses contain inputs to the operation. The square brackets in readings[1] select an item; they do a different job.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Selecting a largest error without loops.

REFERENCES


## Slide 70 — Selecting a largest error without loops

PURPOSE
Selecting a largest error without loops

CONNECT
Previous slide: A method belongs to a value.

EXPLAIN
An error is measured − expected. Its sign shows the direction. abs gives its magnitude: abs(-8) is 8.

max finds the largest supplied value: max(2, 5, 8) is 8. Compare magnitudes when the task asks for the largest error by size.

Keep the original signed error as well, because the magnitude alone loses direction.

LECTURER CUE
A list holds several values. abs removes the sign when measuring the SIZE of an error. max returns the largest supplied value. Keep the original signed error when the task asks for direction.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Selecting a largest error without loops in Python.

REFERENCES


## Slide 71 — Selecting a largest error without loops in Python

PURPOSE
Selecting a largest error without loops in Python

CONNECT
Previous slide: Selecting a largest error without loops.

EXPLAIN
Read the code in this order:
errors = [-2, 5, -8]
largest = max(abs(errors[0]), abs(errors[1]), abs(errors[2]))
print(largest)

print displays a value below the cell.

Square brackets create a list or select an item.

= assigns the value on the right to the name on the left.

Read top to bottom. Run the complete example in the matching practice notebook.

LECTURER CUE
A list holds several values. abs removes the sign when measuring the SIZE of an error. max returns the largest supplied value. Keep the original signed error when the task asks for direction.

Complete practice code:
errors = [-2, 5, -8]
largest = max(abs(errors[0]), abs(errors[1]), abs(errors[2]))
print(largest)

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Keep the reading beside its signed error.

REFERENCES


## Slide 72 — Keep the reading beside its signed error

PURPOSE
Keep the reading beside its signed error

CONNECT
Previous slide: Selecting a largest error without loops in Python.

EXPLAIN
These paired lists use the same positions: the first error belongs to the first reading. The sign tells the direction; abs gives only the size.

index(value) finds the first position containing that value. Use that position in the original lists. An exact tie selects the first here; follow the issued task’s rule.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Find a position, then recover the original values.

REFERENCES


## Slide 73 — Find a position, then recover the original values

PURPOSE
Find a position, then recover the original values

CONNECT
Previous slide: Keep the reading beside its signed error.

EXPLAIN
Read the code in this order:
readings = [98, 105, 92]
errors = [-2, 5, -8]
sizes = [abs(errors[0]), abs(errors[1]), abs(errors[2])]
position = sizes.index(max(sizes))
print(readings[position], errors[position])

print displays a value below the cell.

Square brackets create a list or select an item.

= assigns the value on the right to the name on the left.

Expected: 92 -8. The largest size is 8; the signed error is -8.

LECTURER CUE
Expected: 92 -8. The largest size is 8; the signed error is -8.

Complete practice code:
readings = [98, 105, 92]
errors = [-2, 5, -8]
sizes = [abs(errors[0]), abs(errors[1]), abs(errors[2])]
position = sizes.index(max(sizes))
print(readings[position], errors[position])

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Revision example and answer.

REFERENCES


## Slide 74 — Revision example and answer

PURPOSE
Revision example and answer

CONNECT
Previous slide: Find a position, then recover the original values.

EXPLAIN
Example: Write triple_value(x). Predict triple_value(5). Then predict safe_share(12, 0).

Answer: triple_value returns x * 3. The calls give 15 and None respectively. The guard returns before division when people is zero.

LECTURER CUE
Give silent thinking time, then let pairs discuss. Rotate who types. This is practice, not a graded quiz. Expected response: triple_value returns x * 3. The calls give 15 and None respectively. The guard returns before division when people is zero.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Read the quantities before the formulas.

REFERENCES


## Slide 75 — Read the quantities before the formulas

PURPOSE
Read the quantities before the formulas

CONNECT
Previous slide: Revision example and answer.

EXPLAIN
Mass measures matter in kilograms (kg). Weight is a force in newtons (N): mass × gravitational acceleration. The assignment uses g = 9.81 m/s².

Power is energy transferred per second, in watts (W). Efficiency in percent = 100 × useful output power / input power.

A named constant stores a value kept fixed in the calculation. Uppercase names such as G are a convention, not a Python restriction.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Your programme formula.

REFERENCES


## Slide 76 — Your programme formula

PURPOSE
Your programme formula

CONNECT
Previous slide: Read the quantities before the formulas.

EXPLAIN
Hydrostatic pressure (kPa) = density (kg/m³) × 9.81 (m/s²) × depth (m) / 1000. This is the pressure contribution of the fluid column.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Preparing for the assignment.

REFERENCES


## Slide 77 — Preparing for the assignment

PURPOSE
Preparing for the assignment

CONNECT
Previous slide: Your programme formula.

EXPLAIN
A3 has five named tasks, not five additional projects.

Read each public prompt and its exact output name.

Signed percentage error = 100 × (measured − expected) / expected.

Use a nonzero expected value.

LECTURER CUE
A3 has five named tasks, not five additional projects. Read each public prompt and its exact output name. Signed percentage error = 100 × (measured − expected) / expected. Use a nonzero expected value. For the cohort task: resistive loss = current² × resistance; slab mass = area × thickness × 2400; hydrostatic pressure in kPa = density × 9.81 × depth / 1000. The brief determines which formula you implement. q4 specifies the zero-input behaviour. q5 uses the supplied six readings; trace them on paper, and use your own percentage-error function. Loops are not required yet.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Preparing for the assignment continued.

REFERENCES


## Slide 78 — Preparing for the assignment continued

PURPOSE
Preparing for the assignment continued

CONNECT
Previous slide: Preparing for the assignment.

EXPLAIN
Use the formula for your programme shown earlier. q4 specifies the zero-input behaviour. q5 uses the supplied six readings; trace them on paper, and use your own percentage-error function.

Loops are not required yet.

LECTURER CUE
A3 has five named tasks, not five additional projects. Read each public prompt and its exact output name. Signed percentage error = 100 × (measured − expected) / expected. Use a nonzero expected value. For the cohort task: resistive loss = current² × resistance; slab mass = area × thickness × 2400; hydrostatic pressure in kPa = density × 9.81 × depth / 1000. The brief determines which formula you implement. q4 specifies the zero-input behaviour. q5 uses the supplied six readings; trace them on paper, and use your own percentage-error function. Loops are not required yet.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Unit conversions for the assignment.

REFERENCES


## Slide 79 — Unit conversions for the assignment

PURPOSE
Unit conversions for the assignment

CONNECT
Previous slide: Preparing for the assignment continued.

EXPLAIN
Millimetres become metres by dividing by 1000: 200 mm is 0.2 m.

Percent becomes a fraction by dividing by 100: 75% is 0.75.

Only for rotational-speed questions: rpm means revolutions per minute. One revolution is 2π radians and one minute is 60 seconds, so multiply rpm by 2π/60.

LECTURER CUE
Teach these concepts before the weekly quiz. Use changed numbers for practice. This slide supplies concepts, not the quiz key.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Your issued assignment.

REFERENCES


## Slide 80 — Your issued assignment

PURPOSE
Your issued assignment

CONNECT
Previous slide: Unit conversions for the assignment.

EXPLAIN
Open W03_student.ipynb.

Read every task and its input units before coding.

Keep the required function names and returned outputs.

Run the supplied visible checks, then restart and run all.

LECTURER CUE
# W03: variables and functions
CML3113. Complete each named output. Save as STUDENT_ID_W03.ipynb.
## q1: 3 marks
A 40 kg motor sits on a bench. Set weight_n to its weight in newtons, taking g = 9.81.
## q2: 4 marks
Write percent_error(measured, expected) returning the signed percent error.
## q3: 3 marks
Write mud_pressure(depth_m, density) returning the hydrostatic pressure in kPa.
## q4: 5 marks
Write efficiency(out_w, in_w) returning the percentage, and returning None when in_w is zero or negative.
## q5: 5 marks
READINGS is given in the notebook. Using your own percent_error against a nominal of 100, set worst_reading to the reading with the largest error by size, and worst_error to that reading's signed percent error.
You may compare these six readings directly; a loop is not required this week.
Restart and Run All, then save your named notebook. Practice check results are feedback; the submitted notebook is graded independently.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
q1: 3 marks.

REFERENCES


## Slide 81 — q1: 3 marks

PURPOSE
q1: 3 marks

CONNECT
Previous slide: Your issued assignment.

EXPLAIN
A 40 kg motor sits on a bench.

Set weight_n to its weight in newtons, taking g = 9.81.

LECTURER CUE
Read the specific public requirement shown on this slide. Explain the input, output and evidence before independent work; do not work the assessed answer for the class.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
q2: 4 marks.

REFERENCES


## Slide 82 — q2: 4 marks

PURPOSE
q2: 4 marks

CONNECT
Previous slide: q1: 3 marks.

EXPLAIN
Write percent_error(measured, expected) returning the signed percent error.

LECTURER CUE
Read the specific public requirement shown on this slide. Explain the input, output and evidence before independent work; do not work the assessed answer for the class.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
q3: 3 marks.

REFERENCES


## Slide 83 — q3: 3 marks

PURPOSE
q3: 3 marks

CONNECT
Previous slide: q2: 4 marks.

EXPLAIN
Write mud_pressure(depth_m, density) returning the hydrostatic pressure in kPa.

LECTURER CUE
Read the specific public requirement shown on this slide. Explain the input, output and evidence before independent work; do not work the assessed answer for the class.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
q4: 5 marks.

REFERENCES


## Slide 84 — q4: 5 marks

PURPOSE
q4: 5 marks

CONNECT
Previous slide: q3: 3 marks.

EXPLAIN
Write efficiency(out_w, in_w) returning the percentage, and returning None when in_w is zero or negative.

LECTURER CUE
Read the specific public requirement shown on this slide. Explain the input, output and evidence before independent work; do not work the assessed answer for the class.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
q5: 5 marks.

REFERENCES


## Slide 85 — q5: 5 marks

PURPOSE
q5: 5 marks

CONNECT
Previous slide: q4: 5 marks.

EXPLAIN
READINGS is given in the notebook.

Using your own percent_error against a nominal of 100, set worst_reading to the reading with the largest error by size, and worst_error to that reading's signed percent error.

LECTURER CUE
Read the specific public requirement shown on this slide. Explain the input, output and evidence before independent work; do not work the assessed answer for the class.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Engineering functions submission.

REFERENCES


## Slide 86 — Engineering functions submission

PURPOSE
Engineering functions submission

CONNECT
Previous slide: q5: 5 marks.

EXPLAIN
Opens: 25 Sep 2026, 08:00 Kampala

Deadline: 02 Oct 2026, 08:00 Kampala

Use your full Student Registration Number in the form.

Keep the submitted files and confirmation.

LECTURER CUE
The form link is cohort-specific. Recheck the live form and release status before class. These scheduled assignment dates are separate from the quiz activation window. The issued brief defines the required files, even if the form accepts additional formats. Source: data/submission_links.json

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Week 3 quiz.

REFERENCES


## Slide 87 — Week 3 quiz

PURPOSE
Week 3 quiz

CONNECT
Previous slide: Engineering functions submission.

EXPLAIN
Answer individually after the lecturer activates the quiz.

Available for 24 hours from activation.

Use your Student Registration Number and registered account.

The lecturer will confirm the exact closing time.

LECTURER CUE
Activate the matching open_W3_CML3113 function in Quiz Controls, then confirm the 24-hour close time. Opening this slide or clicking its link does not activate the form. The 24 hours is the availability window. Keep existing quiz scoring and form rules. Do not show private answer keys.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Before you leave.

REFERENCES


## Slide 88 — Revision and submission checklist

PURPOSE
Revision and submission checklist

CONNECT
Previous slide: Week 3 quiz.

EXPLAIN
You can explain each input, the returned answer and its engineering unit.

Save your work and check the required submission files.

LECTURER CUE
Ask every learner for an individual response. Record one misconception to revisit at the start of the next class. If a deadline changed, announce the exact Kampala date and update the source registry before rebuilding slides.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Optional revision video.

REFERENCES


## Slide 89 — Optional revision video

PURPOSE
Optional revision video

CONNECT
Previous slide: Revision and submission checklist.

EXPLAIN
For revision after class.

Corey Schafer
Python Tutorial for Beginners 3: Integers and Floats

Opening 00:00–04:00, suggested four-minute excerpt; preview before class

Listening question: How are numbers written and how do arithmetic operators change them?

LECTURER CUE
Title/channel and subject confirmed from the original YouTube listing. Exact excerpt content has not been fully watched; keep the local worked example as the fallback.
After viewing: Calculate 7 / 2 and 7 // 2 in Colab and explain the difference.
Preview before class and stop after the selected short excerpt. If playback fails, teach the worked example. Video is optional. Source: https://www.youtube.com/watch?v=khKv-8q7YmY

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
independent revision and the issued task.

REFERENCES
