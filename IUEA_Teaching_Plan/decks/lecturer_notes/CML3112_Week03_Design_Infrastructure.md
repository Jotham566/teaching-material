# CML3112 Week 3

## Slide 1: Python calculations and reusable functions

Python calculations and reusable functions
CML3112, Week 3, slide 1

Explanation to give
Build calculations from values and operators, then decisions and functions, then collections. Define each symbol before using it in the program.

Worked illustration / lecturer answer
A definition stores instructions. double_value(4) runs them with x = 4 and returns 8. Printing that return value is a separate action.

Misconception to address
Use this as an orientation to the lesson. Terms and syntax will be unpacked on their own slides; students do not need to know them in advance.

On this slide
Civil Engineering and Architecture

Continue to
Today’s learning

## Slide 2: Today’s learning

Today’s learning
CML3112, Week 3, slide 2

Explanation to give
Build calculations from values and operators, then decisions and functions, then collections. Define each symbol before using it in the program.

Worked illustration / lecturer answer
A definition stores instructions. double_value(4) runs them with x = 4 and returns 8. Printing that return value is a separate action.

Misconception to address
At the end, check the specific outcome shown here using a small previously demonstrated example. A completed file without an explanation is not evidence of understanding.

On this slide
Read Python values and arithmetic symbols.

Define a function, call it and check its inputs.

Continue to
How to read the examples

## Slide 3: How to read the examples

How to read the examples
CML3112, Week 3, slide 3

Explanation to give
Point out the code block, the explanatory text and the displayed result as different objects. The learner types the code only.

Worked illustration / lecturer answer
For print(2 + 3), the typed instruction contains print and parentheses. The result underneath is 5; the learner should not type the label Output or the explanatory sentence into the Python cell.

Misconception to address
For a program split over consecutive slides, keep its setup and indentation together. A later fragment may use a name created on the preceding slide.

On this slide
Code contains the instructions. Output shows the result.

Type the code shown in the example. Run it, then compare your output with the result below.

Continue to
The engineering context

## Slide 4: The engineering context

The engineering context
CML3112, Week 3, slide 4

Explanation to give
Use a room or floor as the physical reference. Length and width are distances in metres. Multiplying them produces area in m²; multiplying by thickness produces volume in m³.

Worked illustration / lecturer answer
For the displayed rectangle, 5 m × 3 m = 15 m². Density connects volume to mass. Indoor temperature, energy and cooling load are different quantities and should retain their own units.

Misconception to address
The later assignment uses slab_mass(area_m2, thickness_m). Explain its two inputs before introducing density. A number without its unit can be ambiguous.

On this slide
A building team records indoor temperature to investigate comfort.

Civil students can discuss construction and inspection; architecture students can discuss shading and ventilation.

A measurement includes a number and its unit.

Continue to
Start with numbers and values

## Slide 5: Start with numbers and values

Start with numbers and values
CML3112, Week 3, slide 5

Explanation to give
Begin with a physical quantity: how many objects, or how much length? A number is the amount; a unit says what that amount measures. Python stores the number but does not automatically know the engineering unit.

Worked illustration / lecturer answer
Put 3 bolts beside 3 metres on the board. Both use the number 3, but adding them would make no physical sense. A length of 2.5 m is two whole metres plus half a metre.

Misconception to address
A decimal point does not supply a unit. Read the variable suffix, axis label or task definition before calculating.

On this slide
Number: A number expresses how much or how many: 3 items or 2.5 metres. Whole numbers count; decimal numbers can describe a part of a unit.
Value and unit: A value is one piece of information. The number 2.5 is a value. A measurement also needs a unit, such as metres. Python does not attach that unit automatically.

Continue to
Words we will use

## Slide 6: Words we will use

Words we will use
CML3112, Week 3, slide 6

Explanation to give
Explain assignment as evaluating the right side and attaching the name on the left to that result. The name can later refer to a different value. Read the equals sign as “assign”, rather than as a mathematical claim that lasts forever.

Worked illustration / lecturer answer
length_m = 4 makes length_m refer to 4. length_m = 6 replaces that association. Printing length_m now displays 6; the name does not remember a history of both values.

Misconception to address
Changing text in a notebook cell changes the instructions. The runtime value changes only when that cell executes.

On this slide
Variable: A name referring to a value. In length_m = 5, the right side is evaluated and assigned to length_m.
int, float, str, bool: int represents whole numbers; float represents approximate real numbers such as 2.5; str is text in quotes; bool is True or False.

Continue to
A variable refers to its current value

## Slide 7: A variable refers to its current value

A variable refers to its current value
CML3112, Week 3, slide 7

Explanation to give
Explain assignment as evaluating the right side and attaching the name on the left to that result. The name can later refer to a different value. Read the equals sign as “assign”, rather than as a mathematical claim that lasts forever.

Worked illustration / lecturer answer
length_m = 4 makes length_m refer to 4. length_m = 6 replaces that association. Printing length_m now displays 6; the name does not remember a history of both values.

Misconception to address
Changing text in a notebook cell changes the instructions. The runtime value changes only when that cell executes.

On this slide
After reassignment, thickness refers to 0.20.

Continue to
Python values have types

## Slide 8: Python values have types

Python values have types
CML3112, Week 3, slide 8

Explanation to give
Explain a type as the kind of information and the operations allowed on it. Quotes make a string, even when every character is a digit. int is a whole number; float is an approximation used for decimal-valued calculations; bool is a truth value.

Worked illustration / lecturer answer
4 + 5 produces 9. "4" + "5" produces the text "45". int("4") + int("5") produces 9 because conversion occurs before addition. None represents the absence of a result in our examples.

Misconception to address
int("2.5") is invalid integer text. float("2.5") works. Converting a value is a deliberate action, not something Python always guesses.

On this slide
Type | Example | Meaning
int | 3 | Whole number
float | 3.5 | Decimal approximation
str | "3.5" | Text in quotes
bool | True / False | Logical value
NoneType | None | No value supplied
3.5 + 2 gives 5.5. "3.5" + "2" joins text into "3.52".

Continue to
Operator

## Slide 9: Operator

Operator
CML3112, Week 3, slide 9

Explanation to give
Translate the familiar written arithmetic signs into keyboard characters. Addition and subtraction look familiar; multiplication uses * and division uses /. Explain each operation on two small numbers before discussing variables.

Worked illustration / lecturer answer
With 8 and 2: 8 + 2 is 10, 8 - 2 is 6, 8 * 2 is 16, and 8 / 2 is 4.0. Python 3 division produces a floating-point result even here.

Misconception to address
The letter x and the printed multiplication sign × are not Python's multiplication operator. Division by zero raises an error.

On this slide
Operator: A symbol for an operation: + adds, - subtracts, * multiplies, / divides, ** raises to a power. // floors a quotient, so -5 // 2 is -3.

Continue to
Read a function call before using it

## Slide 10: Read a function call before using it

Read a function call before using it
CML3112, Week 3, slide 10

Explanation to give
A function call asks an existing tool to do a job. Read its name first, then the values between parentheses. The comma separates inputs when more than one is supplied. The returned result can become input to another call.

Worked illustration / lecturer answer
In print(float("4.5")), the inner float call converts text to 4.5, then print displays it. In print("length", 4), print receives two inputs and normally separates them with a space.

Misconception to address
Parentheses used for a call differ from parentheses used only to group arithmetic. Identify the preceding function name.

On this slide
A built-in function: Python already provides tools such as print, type and float. A function call asks a named tool to do its work: print(3) displays 3.
Parentheses, quotes and comments: Parentheses hold the inputs to a call. Quotes make text: "3.5" is text; float("3.5") converts it to a number. # starts a comment that Python does not run.

Continue to
Reading Python symbols

## Slide 11: Reading Python symbols

Reading Python symbols
CML3112, Week 3, slide 11

Explanation to give
Separate a value-producing expression from the instruction that uses it. Evaluate the calculation first, assign it second, and display it only if a print call asks for output. Explain parentheses, quotes and the comment symbol when pointing to them.

Worked illustration / lecturer answer
total = 6 + 2 first calculates 8, then stores it under total. print(total) displays 8. total == 8 asks a question and produces True; it does not assign anything.

Misconception to address
Do not read = and == interchangeably. A bare assignment normally produces no printed line in a notebook.

On this slide
= assigns a value to a name. == compares two values.

* multiplies. / divides. ** raises to a power.

Parentheses pass inputs when we call a function.

Indented lines belong to the block above them.

Continue to
Names, conversion and comments

## Slide 12: Names, conversion and comments

Names, conversion and comments
CML3112, Week 3, slide 12

Explanation to give
Read the displayed program as five separate actions. float("3.5") turns numeric text into a float. width_m receives the integer 2. Multiplication calculates area_m2. The two print calls display the area and then the type of length_m.

Worked illustration / lecturer answer
Trace the actual values: length_m is 3.5, width_m is 2, area_m2 is 7.0. The displayed lines are 7.0 and <class 'float'>. The comment beginning with # explains the line but does not execute.

Misconception to address
The text inside quotes is initially a string. The name length_m becomes numeric because the conversion result is assigned to it.

Read the displayed code line by line
length_m = float("3.5")  # text to number
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

width_m = 2
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

area_m2 = length_m * width_m
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

print(area_m2)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

print(type(length_m))
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
type(...) reports the kind of value. <class 'float'> means a floating-point number.

Continue to
Week 3 continuation

Result from the supplied example
7.0
<class 'float'>

## Slide 13: Week 3 continuation

Week 3 continuation
CML3112, Week 3, slide 13

Explanation to give
This is now a recap point for CML3112, whose full Week 3 lesson was completed on 29 September. For CML3111/CML3113, begin the Week 3 deck at slide 1.

Worked illustration / lecturer answer
Revisit the preceding result: float("3.5") gives 3.5 and multiplying by 2 gives 7.0. The printed type is <class 'float'>. Next extend these values into arithmetic and decisions.

Misconception to address
Do not treat slide 13 as an instruction to skip the foundations in a cohort that has not covered them.

On this slide
From slides 1–12: values have types, variables name values, = assigns, and print displays a result. float("3.5") converts text to a number. We now use those ideas in calculations and functions.

Next: arithmetic, decisions, functions, then lists and the A3 brief.

Continue to
Reading a Python expression

## Slide 14: Reading a Python expression

Reading a Python expression
CML3112, Week 3, slide 14

Explanation to give
Separate a value-producing expression from the instruction that uses it. Evaluate the calculation first, assign it second, and display it only if a print call asks for output. Explain parentheses, quotes and the comment symbol when pointing to them.

Worked illustration / lecturer answer
total = 6 + 2 first calculates 8, then stores it under total. print(total) displays 8. total == 8 asks a question and produces True; it does not assign anything.

Misconception to address
Do not read = and == interchangeably. A bare assignment normally produces no printed line in a notebook.

On this slide
An expression is code that produces a value. In 7 + 2, the inputs are 7 and 2; the operator + tells Python to add them.

A statement is an instruction. total = 7 + 2 calculates 9, then gives it the name total. print(total) displays the stored value.

Read each symbol before running. Code is what you type; output is what Python displays. Do not type the word “Output”.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Addition subtraction multiplication and division

## Slide 15: Addition subtraction multiplication and division

Addition subtraction multiplication and division
CML3112, Week 3, slide 15

Explanation to give
Translate the familiar written arithmetic signs into keyboard characters. Addition and subtraction look familiar; multiplication uses * and division uses /. Explain each operation on two small numbers before discussing variables.

Worked illustration / lecturer answer
With 8 and 2: 8 + 2 is 10, 8 - 2 is 6, 8 * 2 is 16, and 8 / 2 is 4.0. Python 3 division produces a floating-point result even here.

Misconception to address
The letter x and the printed multiplication sign × are not Python's multiplication operator. Division by zero raises an error.

On this slide
Operator | Meaning | Example and result
+ | Add | 7 + 2 gives 9
- | Subtract | 7 - 2 gives 5
* | Multiply | 7 * 2 gives 14
/ | Divide | 7 / 2 gives 3.5
Python uses * for multiplication, not ×. / can produce a fractional result.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Run the four arithmetic operations

## Slide 16: Run the four arithmetic operations

Run the four arithmetic operations
CML3112, Week 3, slide 16

Explanation to give
Translate the familiar written arithmetic signs into keyboard characters. Addition and subtraction look familiar; multiplication uses * and division uses /. Explain each operation on two small numbers before discussing variables.

Worked illustration / lecturer answer
With 8 and 2: 8 + 2 is 10, 8 - 2 is 6, 8 * 2 is 16, and 8 / 2 is 4.0. Python 3 division produces a floating-point result even here.

Misconception to address
The letter x and the printed multiplication sign × are not Python's multiplication operator. Division by zero raises an error.

Read the displayed code line by line
print(7 + 2)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

print(7 - 2)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

print(7 * 2)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

print(7 / 2)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Output: 9; 5; 14; 3.5

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Floor division remainder and powers

Result from the supplied example
9
5
14
3.5

## Slide 17: Floor division remainder and powers

Floor division remainder and powers
CML3112, Week 3, slide 17

Explanation to give
Explain // as taking the floor of a quotient, % as the remainder and ** as repeated multiplication for a positive integer exponent. “Floor” means the greatest integer no larger than the quotient.

Worked illustration / lecturer answer
9 = 2 × 4 + 1, so 9 // 4 is 2 and 9 % 4 is 1. 3 ** 2 is 9. For a negative example, -9 / 4 is -2.25, so -9 // 4 is -3.

Misconception to address
% does not mean percentage. To turn 60% into a fraction, use 60 / 100. Negative floor division does not simply remove the decimal digits.

On this slide
Operator | Meaning | Example and result
// | Floor the quotient | 7 // 2 gives 3
% | Remainder | 7 % 2 gives 1
** | Raise to a power | 2 ** 3 gives 8
7 contains three groups of 2 with 1 left over: 7 = 3 × 2 + 1.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Reading powers signs and remainders

## Slide 18: Reading powers signs and remainders

Reading powers signs and remainders
CML3112, Week 3, slide 18

Explanation to give
Explain // as taking the floor of a quotient, % as the remainder and ** as repeated multiplication for a positive integer exponent. “Floor” means the greatest integer no larger than the quotient.

Worked illustration / lecturer answer
9 = 2 × 4 + 1, so 9 // 4 is 2 and 9 % 4 is 1. 3 ** 2 is 9. For a negative example, -9 / 4 is -2.25, so -9 // 4 is -3.

Misconception to address
% does not mean percentage. To turn 60% into a fraction, use 60 / 100. Negative floor division does not simply remove the decimal digits.

On this slide
2 ** 3 means 2 × 2 × 2. It does not mean 2 × 3. The left value is the base; the right value is the exponent.

A leading minus makes a number negative: -7. Floor division rounds the quotient down: -7 / 2 is -3.5, so -7 // 2 is -4.

% is remainder, not percentage. To turn 75% into a fraction, calculate 75 / 100. Do not divide by zero.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Run floor division remainder and powers

## Slide 19: Run floor division remainder and powers

Run floor division remainder and powers
CML3112, Week 3, slide 19

Explanation to give
Explain // as taking the floor of a quotient, % as the remainder and ** as repeated multiplication for a positive integer exponent. “Floor” means the greatest integer no larger than the quotient.

Worked illustration / lecturer answer
9 = 2 × 4 + 1, so 9 // 4 is 2 and 9 % 4 is 1. 3 ** 2 is 9. For a negative example, -9 / 4 is -2.25, so -9 // 4 is -3.

Misconception to address
% does not mean percentage. To turn 60% into a fraction, use 60 / 100. Negative floor division does not simply remove the decimal digits.

Read the displayed code line by line
print(7 // 2)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

print(7 % 2)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

print(2 ** 3)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

print(-7 // 2)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

print(75 / 100)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Output: 3; 1; 8; -4; 0.75

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Which operation happens first

Result from the supplied example
3
1
8
-4
0.75

## Slide 20: Which operation happens first

Which operation happens first
CML3112, Week 3, slide 20

Explanation to give
Work from grouped subexpressions outward. Powers precede multiplication and division, which precede addition and subtraction. At the same multiplication/division level, work left to right.

Worked illustration / lecturer answer
2 + 3 * 4 becomes 2 + 12 = 14. (2 + 3) * 4 becomes 5 * 4 = 20. 12 / 3 * 2 becomes 4.0 * 2 = 8.0.

Misconception to address
Parentheses can change the meaning. For a negative base, (-2) ** 2 is 4, while -(2 ** 2) is -4. Use a tolerance for approximate decimal results.

On this slide
Parentheses group a calculation: do (2 + 3) before multiplying it by 4.

Powers come before multiplication and division. Multiplication, /, // and % come before addition and subtraction. Equal-level * and / run left to right.

Use parentheses when the intended grouping might be unclear. For a negative base, write (-2) ** 2. This gives 4; -(2 ** 2) gives -4.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Trace an expression before its output

## Slide 21: Trace an expression before its output

Trace an expression before its output
CML3112, Week 3, slide 21

Explanation to give
Work from grouped subexpressions outward. Powers precede multiplication and division, which precede addition and subtraction. At the same multiplication/division level, work left to right.

Worked illustration / lecturer answer
2 + 3 * 4 becomes 2 + 12 = 14. (2 + 3) * 4 becomes 5 * 4 = 20. 12 / 3 * 2 becomes 4.0 * 2 = 8.0.

Misconception to address
Parentheses can change the meaning. For a negative base, (-2) ** 2 is 4, while -(2 ** 2) is -4. Use a tolerance for approximate decimal results.

On this slide
Expression | First calculation | Result
2 + 3 * 4 | 3 * 4 gives 12 | 2 + 12 gives 14
(2 + 3) * 4 | 2 + 3 gives 5 | 5 * 4 gives 20
12 / 3 * 2 | 12 / 3 gives 4.0 | 4.0 * 2 gives 8.0
Changing parentheses can change the answer even when the numbers stay the same.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Check operation order

## Slide 22: Check operation order

Check operation order
CML3112, Week 3, slide 22

Explanation to give
Work from grouped subexpressions outward. Powers precede multiplication and division, which precede addition and subtraction. At the same multiplication/division level, work left to right.

Worked illustration / lecturer answer
2 + 3 * 4 becomes 2 + 12 = 14. (2 + 3) * 4 becomes 5 * 4 = 20. 12 / 3 * 2 becomes 4.0 * 2 = 8.0.

Misconception to address
Parentheses can change the meaning. For a negative base, (-2) ** 2 is 4, while -(2 ** 2) is -4. Use a tolerance for approximate decimal results.

Read the displayed code line by line
print(2 + 3 * 4)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

print((2 + 3) * 4)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

print(12 / 3 * 2)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Output: 14; 20; 8.0

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Assigning and updating a named value

Result from the supplied example
14
20
8.0

## Slide 23: Assigning and updating a named value

Assigning and updating a named value
CML3112, Week 3, slide 23

Explanation to give
Read the right-hand occurrence of the name as its old value. Calculate the new value, then replace the old association. This is why an update works in programming even though count = count + 1 is not an algebraic equality.

Worked illustration / lecturer answer
Start at count = 2. The update computes 2 + 1 and count becomes 3. Another execution of the update gives 4. Re-executing the initialisation first returns the sequence to 2, then 3.

Misconception to address
Initialise a running counter before the loop. Resetting it inside the loop throws away earlier progress.

On this slide
count = 2 gives the name count the value 2. = means assignment; it does not ask whether two values are equal.

count = count + 1 first reads the old value 2, calculates 3, then assigns 3 back to count.

After the update, print(count) displays 3. Re-running only the update cell changes count again; restart and run from the beginning for the shown result.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Trace one update

## Slide 24: Trace one update

Trace one update
CML3112, Week 3, slide 24

Explanation to give
Read the right-hand occurrence of the name as its old value. Calculate the new value, then replace the old association. This is why an update works in programming even though count = count + 1 is not an algebraic equality.

Worked illustration / lecturer answer
Start at count = 2. The update computes 2 + 1 and count becomes 3. Another execution of the update gives 4. Re-executing the initialisation first returns the sequence to 2, then 3.

Misconception to address
Initialise a running counter before the loop. Resetting it inside the loop throws away earlier progress.

Read the displayed code line by line
count = 2
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

print(count)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

count = count + 1
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

print(count)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Output: 2; 3

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Numbers text and conversion

Result from the supplied example
2
3

## Slide 25: Numbers text and conversion

Numbers text and conversion
CML3112, Week 3, slide 25

Explanation to give
Explain a type as the kind of information and the operations allowed on it. Quotes make a string, even when every character is a digit. int is a whole number; float is an approximation used for decimal-valued calculations; bool is a truth value.

Worked illustration / lecturer answer
4 + 5 produces 9. "4" + "5" produces the text "45". int("4") + int("5") produces 9 because conversion occurs before addition. None represents the absence of a result in our examples.

Misconception to address
int("2.5") is invalid integer text. float("2.5") works. Converting a value is a deliberate action, not something Python always guesses.

On this slide
7 is an integer. 7.0 is a decimal-valued float. "7" is text because it is inside quotes. Both single and double quotes can enclose text.

"7" + "2" joins text into "72". To add those digits as numbers, convert each first: int("7") + int("2") gives 9.

int converts valid integer text; float converts valid decimal text. str turns a value into text. print displays a value; type reports its Python type.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Compare numeric addition with text joining

## Slide 26: Compare numeric addition with text joining

Compare numeric addition with text joining
CML3112, Week 3, slide 26

Explanation to give
Explain a type as the kind of information and the operations allowed on it. Quotes make a string, even when every character is a digit. int is a whole number; float is an approximation used for decimal-valued calculations; bool is a truth value.

Worked illustration / lecturer answer
4 + 5 produces 9. "4" + "5" produces the text "45". int("4") + int("5") produces 9 because conversion occurs before addition. None represents the absence of a result in our examples.

Misconception to address
int("2.5") is invalid integer text. float("2.5") works. Converting a value is a deliberate action, not something Python always guesses.

Read the displayed code line by line
print(7 + 2)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

print("7" + "2")
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

print(int("7") + int("2"))
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

print(float("2.5"))
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Output: 9; 72; 9; 2.5

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Arithmetic that needs care

Result from the supplied example
9
72
9
2.5

## Slide 27: Arithmetic that needs care

Arithmetic that needs care
CML3112, Week 3, slide 27

Explanation to give
Work from grouped subexpressions outward. Powers precede multiplication and division, which precede addition and subtraction. At the same multiplication/division level, work left to right.

Worked illustration / lecturer answer
2 + 3 * 4 becomes 2 + 12 = 14. (2 + 3) * 4 becomes 5 * 4 = 20. 12 / 3 * 2 becomes 4.0 * 2 = 8.0.

Misconception to address
Parentheses can change the meaning. For a negative base, (-2) ** 2 is 4, while -(2 ** 2) is -4. Use a tolerance for approximate decimal results.

On this slide
Parentheses run first: (2 + 4) / 2 is 3.0. Without them, division runs before addition: 2 + 4 / 2 is 4.0.

/ gives a quotient. // rounds that quotient down: 7 // 2 is 3 and -7 // 2 is -4.

Many decimal fractions are approximate in a computer. A tolerance is an allowed difference, for example 0.01 m when checking two calculated lengths.

Continue to
Read the quantities in your programme example

## Slide 28: Read the quantities in your programme example

Read the quantities in your programme example
CML3112, Week 3, slide 28

Explanation to give
Use a room or floor as the physical reference. Length and width are distances in metres. Multiplying them produces area in m²; multiplying by thickness produces volume in m³.

Worked illustration / lecturer answer
For the displayed rectangle, 5 m × 3 m = 15 m². Density connects volume to mass. Indoor temperature, energy and cooling load are different quantities and should retain their own units.

Misconception to address
The later assignment uses slab_mass(area_m2, thickness_m). Explain its two inputs before introducing density. A number without its unit can be ambiguous.

On this slide
Length, width and area: Length and width are distances in metres (m). A rectangle’s area is length × width, measured in square metres (m²).
Thickness and density: Thickness is the third distance. Area × thickness gives volume in m³. Density is mass per volume, in kg/m³; volume × density gives mass in kg.

Continue to
A calculation for your programme

## Slide 29: A calculation for your programme

A calculation for your programme
CML3112, Week 3, slide 29

Explanation to give
Use a room or floor as the physical reference. Length and width are distances in metres. Multiplying them produces area in m²; multiplying by thickness produces volume in m³.

Worked illustration / lecturer answer
For the displayed rectangle, 5 m × 3 m = 15 m². Density connects volume to mass. Indoor temperature, energy and cooling load are different quantities and should retain their own units.

Misconception to address
The later assignment uses slab_mass(area_m2, thickness_m). Explain its two inputs before introducing density. A number without its unit can be ambiguous.

On this slide
A rectangular floor is 5 m long and 3 m wide.

Area = length × width = 15 m².

Continue to
The calculation in Python

## Slide 30: The calculation in Python

The calculation in Python
CML3112, Week 3, slide 30

Explanation to give
Use a room or floor as the physical reference. Length and width are distances in metres. Multiplying them produces area in m²; multiplying by thickness produces volume in m³.

Worked illustration / lecturer answer
For the displayed rectangle, 5 m × 3 m = 15 m². Density connects volume to mass. Indoor temperature, energy and cooling load are different quantities and should retain their own units.

Misconception to address
The later assignment uses slab_mass(area_m2, thickness_m). Explain its two inputs before introducing density. A number without its unit can be ambiguous.

Read the displayed code line by line
length_m = 5
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

width_m = 3
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

area_m2 = length_m * width_m
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

print(area_m2)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Read top to bottom. Run the complete example in the matching practice notebook.

Continue to
Reading an error message

Result from the supplied example
15

## Slide 31: Reading an error message

Reading an error message
CML3112, Week 3, slide 31

Explanation to give
Teach a diagnosis sequence: read the final error line, locate the indicated instruction, compare the expected input with what actually exists, and fix the first cause. Explain the error type rather than treating all red output alike.

Worked illustration / lecturer answer
NameError often means a misspelled or not-yet-created name. FileNotFoundError means the named path was not found. TypeError can result from adding text and a number. A wrong answer can occur with no exception at all.

Misconception to address
The highlighted line is where Python noticed a problem, not always its original cause. Do not install an unrelated package when the exercise deliberately names a nonexistent module.

On this slide
Message | Meaning | First check
NameError | A name is unavailable | Spelling and run order
TypeError | Wrong kind of value | Text versus number
SyntaxError | Python cannot parse a line | Quotes, brackets, colon
IndentationError | Block spacing is invalid | Consistent spaces
The last line names the error. The indicated line shows where Python noticed it.

Continue to
A comparison produces a Boolean value

## Slide 32: A comparison produces a Boolean value

A comparison produces a Boolean value
CML3112, Week 3, slide 32

Explanation to give
A comparison produces a Boolean value, True or False. Read the whole comparison aloud, including whether the threshold itself counts. Explain equality and inequality before introducing a branch.

Worked illustration / lecturer answer
With reading = 30, reading > 30 is False while reading >= 30 is True. reading == 30 is True and reading != 30 is False.

Misconception to address
The boundary is a deliberate choice. Test below, exactly at and above it. "False" in quotes is text, not the Boolean False.

On this slide
A comparison asks a yes/no question about values. Its Python result is True or False, written with capital first letters and no quotes.

30 >= 30 asks “Is 30 at least 30?” The answer is True. 28 >= 30 gives False.

True and False have type bool. "False" is text, not the Boolean value False. Conditions use Boolean results to choose what happens next.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Equality and difference

## Slide 33: Equality and difference

Equality and difference
CML3112, Week 3, slide 33

Explanation to give
A comparison produces a Boolean value, True or False. Read the whole comparison aloud, including whether the threshold itself counts. Explain equality and inequality before introducing a branch.

Worked illustration / lecturer answer
With reading = 30, reading > 30 is False while reading >= 30 is True. reading == 30 is True and reading != 30 is False.

Misconception to address
The boundary is a deliberate choice. Test below, exactly at and above it. "False" in quotes is text, not the Boolean False.

On this slide
Symbol | Question | Example and result
== | Equal values? | 3 == 3 gives True
!= | Different values? | 3 != 4 gives True
= assigns a value. == compares values. They have different jobs.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Comparing sizes and boundaries

## Slide 34: Comparing sizes and boundaries

Comparing sizes and boundaries
CML3112, Week 3, slide 34

Explanation to give
A comparison produces a Boolean value, True or False. Read the whole comparison aloud, including whether the threshold itself counts. Explain equality and inequality before introducing a branch.

Worked illustration / lecturer answer
With reading = 30, reading > 30 is False while reading >= 30 is True. reading == 30 is True and reading != 30 is False.

Misconception to address
The boundary is a deliberate choice. Test below, exactly at and above it. "False" in quotes is text, not the Boolean False.

On this slide
Symbol | Question | Example and result
> | Greater than? | 3 > 3 gives False
>= | Greater than or equal? | 3 >= 3 gives True
< | Less than? | 2 < 3 gives True
<= | Less than or equal? | 3 <= 3 gives True
The = part of >= and <= includes the boundary value.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Display comparison results

## Slide 35: Display comparison results

Display comparison results
CML3112, Week 3, slide 35

Explanation to give
A comparison produces a Boolean value, True or False. Read the whole comparison aloud, including whether the threshold itself counts. Explain equality and inequality before introducing a branch.

Worked illustration / lecturer answer
With reading = 30, reading > 30 is False while reading >= 30 is True. reading == 30 is True and reading != 30 is False.

Misconception to address
The boundary is a deliberate choice. Test below, exactly at and above it. "False" in quotes is text, not the Boolean False.

Read the displayed code line by line
reading = 30
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

print(reading == 30)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

print(reading != 30)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

print(reading > 30)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

print(reading >= 30)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

print(reading < 30)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

print(reading <= 30)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Output: True; False; False; True; False; True

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
A condition and an if block

Result from the supplied example
True
False
False
True
False
True

## Slide 36: A condition and an if block

A condition and an if block
CML3112, Week 3, slide 36

Explanation to give
Explain an if block as a gate. Python evaluates the condition once when it reaches the header. If True, it executes the indented statements; otherwise it skips them. The colon introduces the block.

Worked illustration / lecturer answer
For reading = 28 and a condition reading >= 30, the “warm” line is skipped. The unindented “check finished” line still runs. At 30, both lines run.

Misconception to address
Indentation is part of the program, not decoration. Moving the last print four spaces right changes which path can execute it.

On this slide
A condition is the question tested by an if statement. if reading >= 30: checks whether reading is at least 30.

The colon ends the header. The next line starts with four spaces; those spaces place it inside the block controlled by if.

If the condition is True, run the block. If it is False, skip it. The next line without those four spaces is outside the block and runs afterwards.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
An if statement without else

## Slide 37: An if statement without else

An if statement without else
CML3112, Week 3, slide 37

Explanation to give
Explain an if block as a gate. Python evaluates the condition once when it reaches the header. If True, it executes the indented statements; otherwise it skips them. The colon introduces the block.

Worked illustration / lecturer answer
For reading = 28 and a condition reading >= 30, the “warm” line is skipped. The unindented “check finished” line still runs. At 30, both lines run.

Misconception to address
Indentation is part of the program, not decoration. Moving the last print four spaces right changes which path can execute it.

Read the displayed code line by line
reading = 28
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

if reading >= 30:
Evaluate this yes/no condition. Execute its indented body only on the matching path.

print("warm")
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

print("check finished")
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Output: check finished

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Trace both paths through if

Result from the supplied example
check finished

## Slide 38: Trace both paths through if

Trace both paths through if
CML3112, Week 3, slide 38

Explanation to give
Explain an if block as a gate. Python evaluates the condition once when it reaches the header. If True, it executes the indented statements; otherwise it skips them. The colon introduces the block.

Worked illustration / lecturer answer
For reading = 28 and a condition reading >= 30, the “warm” line is skipped. The unindented “check finished” line still runs. At 30, both lines run.

Misconception to address
Indentation is part of the program, not decoration. Moving the last print four spaces right changes which path can execute it.

On this slide
Value of reading | reading >= 30 | Displayed lines
28 | False | check finished
30 | True | warm; check finished
31 | True | warm; check finished
Only the indented line is conditional. The outside line runs on either path.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
else gives the other path

## Slide 39: else gives the other path

else gives the other path
CML3112, Week 3, slide 39

Explanation to give
else is the alternative to the matching if. It has no new test. The two headers align vertically and their bodies sit one indentation level farther right.

Worked illustration / lecturer answer
At temperature 28, the displayed example prints “below 30”. At 30 it prints “warm”. Exactly one branch runs in this if/else decision.

Misconception to address
else is not an independent statement and cannot stand alone. Explain where the block ends before continuing to the next line.

On this slide
else means “otherwise”. It has a colon but no extra condition. Align else with its matching if.

The if block runs when its condition is True. The else block runs when that same condition is False. Only one of these blocks runs.

Both branch bodies are indented by four spaces. Returning to the left margin ends the whole decision.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
A decision needs a colon and indentation

## Slide 40: A decision needs a colon and indentation

A decision needs a colon and indentation
CML3112, Week 3, slide 40

Explanation to give
else is the alternative to the matching if. It has no new test. The two headers align vertically and their bodies sit one indentation level farther right.

Worked illustration / lecturer answer
At temperature 28, the displayed example prints “below 30”. At 30 it prints “warm”. Exactly one branch runs in this if/else decision.

Misconception to address
else is not an independent statement and cannot stand alone. Explain where the block ends before continuing to the next line.

Read the displayed code line by line
temperature = 28
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

if temperature >= 30:
Evaluate this yes/no condition. Execute its indented body only on the matching path.

print("warm")
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

else:
Use this remaining path when the matching earlier condition did not succeed.

print("below 30")
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
>= compares values. Only the chosen indented block runs.

Continue to
Trace both paths through if else

Result from the supplied example
below 30

## Slide 41: Trace both paths through if else

Trace both paths through if else
CML3112, Week 3, slide 41

Explanation to give
else is the alternative to the matching if. It has no new test. The two headers align vertically and their bodies sit one indentation level farther right.

Worked illustration / lecturer answer
At temperature 28, the displayed example prints “below 30”. At 30 it prints “warm”. Exactly one branch runs in this if/else decision.

Misconception to address
else is not an independent statement and cannot stand alone. Explain where the block ends before continuing to the next line.

On this slide
temperature | temperature >= 30 | Selected output
28 | False | below 30
30 | True | warm
31 | True | warm
Re-run the complete previous example for each value. Exactly one branch prints.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
More than two branches

## Slide 42: More than two branches

More than two branches
CML3112, Week 3, slide 42

Explanation to give
Read an if/elif/else chain from top to bottom. Stop checking the chain as soon as a condition matches. elif means “otherwise, test this next condition”.

Worked illustration / lecturer answer
In the displayed level example, 7 fails >= 10, passes >= 5 and prints medium. A level of 10 prints high immediately. A level of 3 reaches low.

Misconception to address
Putting >= 5 before >= 10 would classify 12 as medium. Two separate if statements can both run, unlike this single chain.

On this slide
if tests the first condition. elif means “otherwise, if” and tests another condition only if the earlier one was false. else handles the remaining case.

Python runs only the first matching branch. Put a narrower condition before a broader one that would also match. A colon and indentation mark each body.

Continue to
Tracing an if elif else chain

## Slide 43: Tracing an if elif else chain

Tracing an if elif else chain
CML3112, Week 3, slide 43

Explanation to give
Read an if/elif/else chain from top to bottom. Stop checking the chain as soon as a condition matches. elif means “otherwise, test this next condition”.

Worked illustration / lecturer answer
In the displayed level example, 7 fails >= 10, passes >= 5 and prints medium. A level of 10 prints high immediately. A level of 3 reaches low.

Misconception to address
Putting >= 5 before >= 10 would classify 12 as medium. Two separate if statements can both run, unlike this single chain.

Read the displayed code line by line
level = 7
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

if level >= 10:
Evaluate this yes/no condition. Execute its indented body only on the matching path.

print("high")
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

elif level >= 5:
Evaluate this yes/no condition. Execute its indented body only on the matching path.

print("medium")
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

else:
Use this remaining path when the matching earlier condition did not succeed.

print("low")
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Output: medium. The first condition is false; the second is true.

Continue to
Trace the if elif else chain

Result from the supplied example
medium

## Slide 44: Trace the if elif else chain

Trace the if elif else chain
CML3112, Week 3, slide 44

Explanation to give
Read an if/elif/else chain from top to bottom. Stop checking the chain as soon as a condition matches. elif means “otherwise, test this next condition”.

Worked illustration / lecturer answer
In the displayed level example, 7 fails >= 10, passes >= 5 and prints medium. A level of 10 prints high immediately. A level of 3 reaches low.

Misconception to address
Putting >= 5 before >= 10 would classify 12 as medium. Two separate if statements can both run, unlike this single chain.

On this slide
level | Tests in order | Output
7 | 7 >= 10: False; 7 >= 5: True | medium
10 | 10 >= 10: True; stop testing | high
3 | 3 >= 10: False; 3 >= 5: False | low
Python stops at the first True branch. else runs when neither test passes.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Combining and reversing conditions

## Slide 45: Combining and reversing conditions

Combining and reversing conditions
CML3112, Week 3, slide 45

Explanation to give
Evaluate each comparison before combining the resulting truth values. and needs both True, or needs at least one True, and not reverses a Boolean.

Worked illustration / lecturer answer
For reading 25, (reading >= 20) and (reading <= 30) is True. Neither outside-range comparison is True, so (reading < 20) or (reading > 30) is False.

Misconception to address
Saying “between” leaves boundary inclusion ambiguous. State whether 20 and 30 count, then test those values explicitly.

On this slide
and asks for both conditions to be True. or asks for at least one to be True. not reverses a Boolean answer.

Use parentheses to make each comparison readable: (reading >= 20) and (reading <= 30). This is an inclusive range check.

For these lessons we combine comparisons, so their results are Boolean. Python also permits other operand types; those are not needed for the shown checks.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
and and or with Boolean inputs

## Slide 46: and and or with Boolean inputs

and and or with Boolean inputs
CML3112, Week 3, slide 46

Explanation to give
Evaluate each comparison before combining the resulting truth values. and needs both True, or needs at least one True, and not reverses a Boolean.

Worked illustration / lecturer answer
For reading 25, (reading >= 20) and (reading <= 30) is True. Neither outside-range comparison is True, so (reading < 20) or (reading > 30) is False.

Misconception to address
Saying “between” leaves boundary inclusion ambiguous. State whether 20 and 30 count, then test those values explicitly.

On this slide
Inputs | and result | or result
True, True | True | True
True, False | False | True
False, True | False | True
False, False | False | False
not True gives False; not False gives True.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Check a permitted range

## Slide 47: Check a permitted range

Check a permitted range
CML3112, Week 3, slide 47

Explanation to give
Evaluate each comparison before combining the resulting truth values. and needs both True, or needs at least one True, and not reverses a Boolean.

Worked illustration / lecturer answer
For reading 25, (reading >= 20) and (reading <= 30) is True. Neither outside-range comparison is True, so (reading < 20) or (reading > 30) is False.

Misconception to address
Saying “between” leaves boundary inclusion ambiguous. State whether 20 and 30 count, then test those values explicitly.

Read the displayed code line by line
reading = 25
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

inside = (reading >= 20) and (reading <= 30)
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

print(inside)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

print((reading < 20) or (reading > 30))
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

print(not inside)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Output: True; False; False

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Why a zero check comes first

Result from the supplied example
True
False
False

## Slide 48: Why a zero check comes first

Why a zero check comes first
CML3112, Week 3, slide 48

Explanation to give
A guard handles an input that would make the main calculation invalid. Put it before the dangerous operation. return ends the function call immediately, so later lines do not execute on that path.

Worked illustration / lecturer answer
safe_share(12, 3) reaches 12 / 3 and returns 4.0. safe_share(12, 0) takes the guard and returns None before division.

Misconception to address
Returning None communicates no calculated share, not a zero share. Test for that case before doing further arithmetic with the result.

On this slide
Python evaluates and from left to right. When the first Boolean comparison is False, it does not need to evaluate the second.

For a simple zero guard, use if denominator == 0: before the division and return or handle that case explicitly.

A guard checks an input before a calculation. The function example below uses def and return.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Function

## Slide 49: Function

Function
CML3112, Week 3, slide 49

Explanation to give
Describe a function as instructions saved under a name. def stores the recipe. A call supplies ingredients and executes it. Parameters are the recipe's input names; arguments are the actual supplied values.

Worked illustration / lecturer answer
For double_value(4), x receives 4, x * 2 produces 8 and return sends 8 back. answer receives that 8 and print displays it. The definition alone displays nothing.

Misconception to address
Students often run only the definition and expect an answer. Point to the separate call. Changing the function body requires rerunning its definition before another call uses it.

On this slide
Function: A named, reusable calculation or procedure. def introduces its definition. Parameters are the names for its inputs; arguments are the values supplied when calling it.

Continue to
Indentation and return

## Slide 50: Indentation and return

Indentation and return
CML3112, Week 3, slide 50

Explanation to give
Distinguish delivering a result to another line of code from displaying it on the screen. return ends a function call and hands back a value. print displays information and itself returns None.

Worked illustration / lecturer answer
If double_value returns 8, result = double_value(4) stores 8. If its body only prints 8, the screen shows 8 but result receives None. This difference matters when another calculation uses result.

Misconception to address
A function that reaches its end without a return value also returns None. None is a real Python value, not the text "None" or the number zero.

On this slide
Indentation and return: Spaces at the start of a line group the function body. return hands a result to the calling code. print displays a value and returns None.

Continue to
A function definition and a call

## Slide 51: A function definition and a call

A function definition and a call
CML3112, Week 3, slide 51

Explanation to give
Describe a function as instructions saved under a name. def stores the recipe. A call supplies ingredients and executes it. Parameters are the recipe's input names; arguments are the actual supplied values.

Worked illustration / lecturer answer
For double_value(4), x receives 4, x * 2 produces 8 and return sends 8 back. answer receives that 8 and print displays it. The definition alone displays nothing.

Misconception to address
Students often run only the definition and expect an answer. Point to the separate call. Changing the function body requires rerunning its definition before another call uses it.

On this slide
def gives a reusable calculation a name and inputs.

Defining a function remembers the instructions.

Calling the function runs those instructions with values.

return sends the result back to the caller.

Continue to
Inputs, instructions and a returned result

## Slide 52: Inputs, instructions and a returned result

Inputs, instructions and a returned result
CML3112, Week 3, slide 52

Explanation to give
Describe a function as instructions saved under a name. def stores the recipe. A call supplies ingredients and executes it. Parameters are the recipe's input names; arguments are the actual supplied values.

Worked illustration / lecturer answer
For double_value(4), x receives 4, x * 2 produces 8 and return sends 8 back. answer receives that 8 and print displays it. The definition alone displays nothing.

Misconception to address
Students often run only the definition and expect an answer. Point to the separate call. Changing the function body requires rerunning its definition before another call uses it.

On this slide
The illustration uses slab_volume: length × width × thickness. The next function uses the same input/body/return pattern.

Continue to
Defining and calling double_value

## Slide 53: Defining and calling double_value

Defining and calling double_value
CML3112, Week 3, slide 53

Explanation to give
Describe a function as instructions saved under a name. def stores the recipe. A call supplies ingredients and executes it. Parameters are the recipe's input names; arguments are the actual supplied values.

Worked illustration / lecturer answer
For double_value(4), x receives 4, x * 2 produces 8 and return sends 8 back. answer receives that 8 and print displays it. The definition alone displays nothing.

Misconception to address
Students often run only the definition and expect an answer. Point to the separate call. Changing the function body requires rerunning its definition before another call uses it.

Read the displayed code line by line
def double_value(x):
Store these instructions under this function name. Names in parentheses are its inputs; the body waits until a call.

return x * 2
Evaluate this result and send it to the caller, ending this function call.

answer = double_value(4)
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

print(answer)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Output: 8. Calling passes 4 to x; return sends 8 back; print displays it.

Continue to
Trace one function call

Result from the supplied example
8

## Slide 54: Trace one function call

Trace one function call
CML3112, Week 3, slide 54

Explanation to give
Describe a function as instructions saved under a name. def stores the recipe. A call supplies ingredients and executes it. Parameters are the recipe's input names; arguments are the actual supplied values.

Worked illustration / lecturer answer
For double_value(4), x receives 4, x * 2 produces 8 and return sends 8 back. answer receives that 8 and print displays it. The definition alone displays nothing.

Misconception to address
Students often run only the definition and expect an answer. Point to the separate call. Changing the function body requires rerunning its definition before another call uses it.

On this slide
Step | What Python does | Value
Define | Store the body; do not run it | No printed output
Call double_value(4) | Give parameter x the argument | x is 4
return x * 2 | Calculate and return | 8
Assign and print | Store returned 8 in answer; display | 8
return sends a value back to the caller. print displays it. These are different actions.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Passing inputs by position or by name

## Slide 55: Passing inputs by position or by name

Passing inputs by position or by name
CML3112, Week 3, slide 55

Explanation to give
Match each supplied argument to the parameter that receives it. Positional arguments match from left to right; keyword arguments name the destination directly.

Worked illustration / lecturer answer
rectangle_area(3, 2) and rectangle_area(width=2, length=3) both use length 3 and width 2, returning 6. Say the parameter names aloud as you bind the values.

Misconception to address
The equals sign in width=2 labels a call argument. It does not create a general width variable outside that call.

On this slide
In def rectangle_area(length, width):, length and width are parameter names. A call supplies an argument value for each.

rectangle_area(3, 2) binds 3 to length and 2 to width by position. rectangle_area(width=2, length=3) binds them by name.

The = inside a named argument labels an input for the call. Both calls run the same function body with the same two values.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Positional and named inputs

## Slide 56: Positional and named inputs

Positional and named inputs
CML3112, Week 3, slide 56

Explanation to give
Match each supplied argument to the parameter that receives it. Positional arguments match from left to right; keyword arguments name the destination directly.

Worked illustration / lecturer answer
rectangle_area(3, 2) and rectangle_area(width=2, length=3) both use length 3 and width 2, returning 6. Say the parameter names aloud as you bind the values.

Misconception to address
The equals sign in width=2 labels a call argument. It does not create a general width variable outside that call.

Read the displayed code line by line
def rectangle_area(length, width):
Store these instructions under this function name. Names in parentheses are its inputs; the body waits until a call.

return length * width
Evaluate this result and send it to the caller, ending this function call.

print(rectangle_area(3, 2))
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

print(rectangle_area(width=2, length=3))
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Both calls supply the same inputs. return makes the result reusable.

Continue to
None means there is no result value

Result from the supplied example
6
6

## Slide 57: None means there is no result value

None means there is no result value
CML3112, Week 3, slide 57

Explanation to give
Distinguish delivering a result to another line of code from displaying it on the screen. return ends a function call and hands back a value. print displays information and itself returns None.

Worked illustration / lecturer answer
If double_value returns 8, result = double_value(4) stores 8. If its body only prints 8, the screen shows 8 but result receives None. This difference matters when another calculation uses result.

Misconception to address
A function that reaches its end without a return value also returns None. None is a real Python value, not the text "None" or the number zero.

On this slide
None is a Python value used here to mean “no calculated answer”. It is not zero, an empty string, or the word "None".

A function returns None explicitly with return None. A function also returns None if it reaches its end without a return value.

A caller must handle None before trying arithmetic with the result. The next example returns it for division by zero.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
An input check before division

## Slide 58: An input check before division

An input check before division
CML3112, Week 3, slide 58

Explanation to give
A guard handles an input that would make the main calculation invalid. Put it before the dangerous operation. return ends the function call immediately, so later lines do not execute on that path.

Worked illustration / lecturer answer
safe_share(12, 3) reaches 12 / 3 and returns 4.0. safe_share(12, 0) takes the guard and returns None before division.

Misconception to address
Returning None communicates no calculated share, not a zero share. Test for that case before doing further arithmetic with the result.

On this slide
Division by zero raises ZeroDivisionError. We choose to return None when people is zero, so there is no calculated share.

The check belongs inside the function, before the division. return ends that call immediately. A valid input follows the later return line.

Continue to
A function with a zero-input check

## Slide 59: A function with a zero-input check

A function with a zero-input check
CML3112, Week 3, slide 59

Explanation to give
A guard handles an input that would make the main calculation invalid. Put it before the dangerous operation. return ends the function call immediately, so later lines do not execute on that path.

Worked illustration / lecturer answer
safe_share(12, 3) reaches 12 / 3 and returns 4.0. safe_share(12, 0) takes the guard and returns None before division.

Misconception to address
Returning None communicates no calculated share, not a zero share. Test for that case before doing further arithmetic with the result.

Read the displayed code line by line
def safe_share(total, people):
Store these instructions under this function name. Names in parentheses are its inputs; the body waits until a call.

if people == 0:
Evaluate this yes/no condition. Execute its indented body only on the matching path.

return None
Evaluate this result and send it to the caller, ending this function call.

return total / people
Evaluate this result and send it to the caller, ending this function call.

print(safe_share(12, 3))
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Output: 4.0. safe_share(12, 0) returns None before any division.

Continue to
Trace the division guard

Result from the supplied example
4.0

## Slide 60: Trace the division guard

Trace the division guard
CML3112, Week 3, slide 60

Explanation to give
A guard handles an input that would make the main calculation invalid. Put it before the dangerous operation. return ends the function call immediately, so later lines do not execute on that path.

Worked illustration / lecturer answer
safe_share(12, 3) reaches 12 / 3 and returns 4.0. safe_share(12, 0) takes the guard and returns None before division.

Misconception to address
Returning None communicates no calculated share, not a zero share. Test for that case before doing further arithmetic with the result.

On this slide
Call | First test | Returned result
safe_share(12, 3) | 3 == 0 is False | 12 / 3 gives 4.0
safe_share(12, 0) | 0 == 0 is True | None; division is skipped
return ends this function call immediately. Later lines inside it do not run.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
A branch with a clear boundary

## Slide 61: A branch with a clear boundary

A branch with a clear boundary
CML3112, Week 3, slide 61

Explanation to give
Trace the equality case first because it exposes whether the threshold is inclusive. In this function, return prevents execution from reaching the later return once the high condition is satisfied.

Worked illustration / lecturer answer
check_level(10) returns high; check_level(9) returns low; check_level(11) returns high. Show which return line each call reaches.

Misconception to address
An explicit else is unnecessary here because the first return already exits the call. That would change if the first branch only printed.

On this slide
Read from the top. >= includes the boundary.

Only the selected branch runs.

Try the value exactly at 10 as well as 9 and 11.

Continue to
A branch with a clear boundary in Python

## Slide 62: A branch with a clear boundary in Python

A branch with a clear boundary in Python
CML3112, Week 3, slide 62

Explanation to give
Trace the equality case first because it exposes whether the threshold is inclusive. In this function, return prevents execution from reaching the later return once the high condition is satisfied.

Worked illustration / lecturer answer
check_level(10) returns high; check_level(9) returns low; check_level(11) returns high. Show which return line each call reaches.

Misconception to address
An explicit else is unnecessary here because the first return already exits the call. That would change if the first branch only printed.

Read the displayed code line by line
def check_level(value):
Store these instructions under this function name. Names in parentheses are its inputs; the body waits until a call.

if value >= 10:
Evaluate this yes/no condition. Execute its indented body only on the matching path.

return "high"
Evaluate this result and send it to the caller, ending this function call.

return "low"
Evaluate this result and send it to the caller, ending this function call.

print(check_level(10))
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

print(check_level(9))
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Read top to bottom. Run the complete example in the matching practice notebook.

Continue to
One value and a collection of values

Result from the supplied example
high
low

## Slide 63: One value and a collection of values

One value and a collection of values
CML3112, Week 3, slide 63

Explanation to give
Compare the access rule for each collection. Lists and tuples use positions; dictionaries use keys; sets answer membership questions. Lists can change their items, while tuple positions cannot be reassigned.

Worked illustration / lecturer answer
For readings use an ordered list. For a record with unit and reading fields use a dictionary. For a coordinate pair use a tuple. For IDs already seen use a set.

Misconception to address
A set cannot be indexed. Dictionary keys are unique, but values may repeat. {} is an empty dictionary; set() is an empty set.

On this slide
A variable can refer to one value: reading = 98. A collection stores several related values under one name.

Python has several collection types. Choose one according to how you need to find, change or organise its contents.

Continue to
Lists dictionaries tuples and sets

## Slide 64: Lists dictionaries tuples and sets

Lists dictionaries tuples and sets
CML3112, Week 3, slide 64

Explanation to give
Compare the access rule for each collection. Lists and tuples use positions; dictionaries use keys; sets answer membership questions. Lists can change their items, while tuple positions cannot be reassigned.

Worked illustration / lecturer answer
For readings use an ordered list. For a record with unit and reading fields use a dictionary. For a coordinate pair use a tuple. For IDs already seen use a set.

Misconception to address
A set cannot be indexed. Dictionary keys are unique, but values may repeat. {} is an empty dictionary; set() is an empty set.

On this slide
Type | Example | Choose it for
list | [98, 105, 92] | Values in a changeable order
dict | {"reading": 98} | Values found by named keys
tuple | (2, 3) | Positions you will not reassign
set | {"A", "B"} | Distinct items and membership
List and tuple positions start at zero. Dictionaries use keys. Sets have no positional index.

Continue to
A list stores values in positions

## Slide 65: A list stores values in positions

A list stores values in positions
CML3112, Week 3, slide 65

Explanation to give
A list is an ordered collection. Draw labelled positions 0, 1 and 2 above three values. The position is the address, not the value stored there. A list may contain repeated values.

Worked illustration / lecturer answer
For [2, 4, 6], position 0 contains 2 and position 2 contains 6. len returns 3. There is no position 3. append(8) adds a new final item and the count becomes 4.

Misconception to address
Square brackets create a list when enclosing values, but select an item when placed after its name. Python counts list positions from zero.

On this slide
readings = [98, 105, 92] creates a list. Square brackets enclose the items; commas separate them.

An index is an item’s position. Python starts counting at zero: readings[0] is 98, readings[1] is 105, readings[2] is 92.

Three items have positions 0, 1 and 2. readings[3] raises IndexError because there is no fourth item.

Continue to
Count items before choosing a position

## Slide 66: Count items before choosing a position

Count items before choosing a position
CML3112, Week 3, slide 66

Explanation to give
A list is an ordered collection. Draw labelled positions 0, 1 and 2 above three values. The position is the address, not the value stored there. A list may contain repeated values.

Worked illustration / lecturer answer
For [2, 4, 6], position 0 contains 2 and position 2 contains 6. len returns 3. There is no position 3. append(8) adds a new final item and the count becomes 4.

Misconception to address
Square brackets create a list when enclosing values, but select an item when placed after its name. Python counts list positions from zero.

On this slide
len(readings) is a built-in function call that returns how many items the list contains. len([98, 105, 92]) is 3.

A count and an index are different: the count is 3, while the valid positions are 0, 1 and 2.

print(readings) displays the whole list. print(readings[0]) displays only the value at its first position.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Creating and reading a list

## Slide 67: Creating and reading a list

Creating and reading a list
CML3112, Week 3, slide 67

Explanation to give
A list is an ordered collection. Draw labelled positions 0, 1 and 2 above three values. The position is the address, not the value stored there. A list may contain repeated values.

Worked illustration / lecturer answer
For [2, 4, 6], position 0 contains 2 and position 2 contains 6. len returns 3. There is no position 3. append(8) adds a new final item and the count becomes 4.

Misconception to address
Square brackets create a list when enclosing values, but select an item when placed after its name. Python counts list positions from zero.

Read the displayed code line by line
readings = [98, 105, 92]
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

print(readings)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

print(readings[0])
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

print(len(readings))
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Output: [98, 105, 92], then 98, then 3.

Continue to
Choosing the right collection

Result from the supplied example
[98, 105, 92]
98
3

## Slide 68: Choosing the right collection

Choosing the right collection
CML3112, Week 3, slide 68

Explanation to give
Compare the access rule for each collection. Lists and tuples use positions; dictionaries use keys; sets answer membership questions. Lists can change their items, while tuple positions cannot be reassigned.

Worked illustration / lecturer answer
For readings use an ordered list. For a record with unit and reading fields use a dictionary. For a coordinate pair use a tuple. For IDs already seen use a set.

Misconception to address
A set cannot be indexed. Dictionary keys are unique, but values may repeat. {} is an empty dictionary; set() is an empty set.

On this slide
A dictionary connects a key to a value: {"reading": 98}. The colon connects them; record["reading"] finds the value by its key.

A tuple such as (2, 3) stores ordered items whose positions cannot be reassigned. A set such as {"A", "B"} stores distinct items without positions.

We use a list for today’s readings because their order matters. Week 4 develops dictionary, tuple and set operations before we use them with records.

Continue to
A method belongs to a value

## Slide 69: A method belongs to a value

A method belongs to a value
CML3112, Week 3, slide 69

Explanation to give
A method is an operation accessed through an object with a dot. The object tells us which data the operation acts on. Contrast that syntax with a standalone function receiving the object as an input.

Worked illustration / lecturer answer
len(readings) counts the list. readings.index(105) searches that list and returns the first matching position. readings[1] retrieves the item at position 1.

Misconception to address
index returns a position, not the item. An absent search value raises ValueError; it does not return a spare valid position.

On this slide
A function is called by name: len(readings). A method is called through a value with a dot: readings.index(105).

index searches a list for a value and returns its first position. Here readings.index(105) returns 1. A missing value raises ValueError.

The parentheses contain inputs to the operation. The square brackets in readings[1] select an item; they do a different job.

Continue to
Selecting a largest error without loops

## Slide 70: Selecting a largest error without loops

Selecting a largest error without loops
CML3112, Week 3, slide 70

Explanation to give
Separate error direction from error size. A negative error means the reading is below the reference. abs removes the sign for size comparisons, but keep the original signed number for reporting.

Worked illustration / lecturer answer
Errors [-2, 5, -8] have sizes [2, 5, 8]. The largest size is 8 at position 2. The corresponding reading is 92 and its signed error is -8.

Misconception to address
max(errors) would select 5, the largest signed value, rather than the largest error by size. Match the selected position back to both original lists.

On this slide
An error is measured − expected. Its sign shows the direction. abs gives its magnitude: abs(-8) is 8.

max finds the largest supplied value: max(2, 5, 8) is 8. Compare magnitudes when the task asks for the largest error by size.

Keep the original signed error as well, because the magnitude alone loses direction.

Continue to
Selecting a largest error without loops in Python

## Slide 71: Selecting a largest error without loops in Python

Selecting a largest error without loops in Python
CML3112, Week 3, slide 71

Explanation to give
Separate error direction from error size. A negative error means the reading is below the reference. abs removes the sign for size comparisons, but keep the original signed number for reporting.

Worked illustration / lecturer answer
Errors [-2, 5, -8] have sizes [2, 5, 8]. The largest size is 8 at position 2. The corresponding reading is 92 and its signed error is -8.

Misconception to address
max(errors) would select 5, the largest signed value, rather than the largest error by size. Match the selected position back to both original lists.

Read the displayed code line by line
errors = [-2, 5, -8]
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

largest = max(abs(errors[0]), abs(errors[1]), abs(errors[2]))
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

print(largest)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Read top to bottom. Run the complete example in the matching practice notebook.

Continue to
Keep the reading beside its signed error

Result from the supplied example
8

## Slide 72: Keep the reading beside its signed error

Keep the reading beside its signed error
CML3112, Week 3, slide 72

Explanation to give
Separate error direction from error size. A negative error means the reading is below the reference. abs removes the sign for size comparisons, but keep the original signed number for reporting.

Worked illustration / lecturer answer
Errors [-2, 5, -8] have sizes [2, 5, 8]. The largest size is 8 at position 2. The corresponding reading is 92 and its signed error is -8.

Misconception to address
max(errors) would select 5, the largest signed value, rather than the largest error by size. Match the selected position back to both original lists.

On this slide
These paired lists use the same positions: the first error belongs to the first reading. The sign tells the direction; abs gives only the size.

index(value) finds the first position containing that value. Use that position in the original lists. An exact tie selects the first here; follow the issued task’s rule.

Continue to
Find a position, then recover the original values

## Slide 73: Find a position, then recover the original values

Find a position, then recover the original values
CML3112, Week 3, slide 73

Explanation to give
Separate error direction from error size. A negative error means the reading is below the reference. abs removes the sign for size comparisons, but keep the original signed number for reporting.

Worked illustration / lecturer answer
Errors [-2, 5, -8] have sizes [2, 5, 8]. The largest size is 8 at position 2. The corresponding reading is 92 and its signed error is -8.

Misconception to address
max(errors) would select 5, the largest signed value, rather than the largest error by size. Match the selected position back to both original lists.

Read the displayed code line by line
readings = [98, 105, 92]
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

errors = [-2, 5, -8]
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

sizes = [abs(errors[0]), abs(errors[1]), abs(errors[2])]
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

position = sizes.index(max(sizes))
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

print(readings[position], errors[position])
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Expected: 92 -8. The largest size is 8; the signed error is -8.

Continue to
Revision example and answer

Result from the supplied example
92 -8

## Slide 74: Revision example and answer

Revision example and answer
CML3112, Week 3, slide 74

Explanation to give
Use the displayed example as a short individual revision question, then explain the reasoning behind its answer.

Worked illustration / lecturer answer
Example: Write triple_value(x). Predict triple_value(5). Then predict safe_share(12, 0).

Answer: triple_value returns x * 3. The calls give 15 and None respectively. The guard returns before division when people is zero.

Misconception to address
Trace the operation that changes the value rather than accepting a memorised output. For notebook-state examples, specify which cell is repeated and whether the initialisation ran again.

Continue to
Read the quantities before the formulas

## Slide 75: Read the quantities before the formulas

Read the quantities before the formulas
CML3112, Week 3, slide 75

Explanation to give
Track the meaning and unit before substituting values. Mass is in kg, weight is in N, area in m² and volume in m³. Power is energy transferred per second, in W.

Worked illustration / lecturer answer
Convert 200 mm to 0.2 m by dividing by 1000. A separate 2 kg mass has weight 19.62 N using g = 9.81 m/s². A percentage 75 becomes fraction 0.75.

Misconception to address
Do not mix area, volume, mass and force. The name G is an uppercase convention for a fixed value, not an automatic unit system. Only introduce rpm conversion when that quantity is actually needed.

On this slide
Mass measures matter in kilograms (kg). Weight is a force in newtons (N): mass × gravitational acceleration. The assignment uses g = 9.81 m/s².

Power is energy transferred per second, in watts (W). Efficiency in percent = 100 × useful output power / input power.

A named constant stores a value kept fixed in the calculation. Uppercase names such as G are a convention, not a Python restriction.

Continue to
Your programme formula

## Slide 76: Your programme formula

Your programme formula
CML3112, Week 3, slide 76

Explanation to give
Use a room or floor as the physical reference. Length and width are distances in metres. Multiplying them produces area in m²; multiplying by thickness produces volume in m³.

Worked illustration / lecturer answer
For the displayed rectangle, 5 m × 3 m = 15 m². Density connects volume to mass. Indoor temperature, energy and cooling load are different quantities and should retain their own units.

Misconception to address
The later assignment uses slab_mass(area_m2, thickness_m). Explain its two inputs before introducing density. A number without its unit can be ambiguous.

On this slide
Slab mass = area × thickness × density. Use metres and 2400 kg/m³ as specified.

Continue to
Preparing for the assignment

## Slide 77: Preparing for the assignment

Preparing for the assignment
CML3112, Week 3, slide 77

Explanation to give
A3 has five tasks in one notebook: a weight value, signed percentage-error function, programme-specific function, guarded efficiency function and the largest-error reading.

Worked illustration / lecturer answer
Explain the required names and return values. Compare a signed error by magnitude only for choosing the worst reading, then keep its original sign. Loops are not required for this six-reading task.

Misconception to address
The latest notebook needs no grading scripts. Submit one .ipynb, with no separate report. Keep any work already completed in an older notebook.

On this slide
A3 has five named tasks, not five additional projects.

Read each public prompt and its exact output name.

Signed percentage error = 100 × (measured − expected) / expected.

Use a nonzero expected value.

Current notebook workflow
The latest student package contains no grader scripts or g.check cells. Restart and run the completed notebook, then submit it. Existing older submissions remain valid.

Continue to
Preparing for the assignment continued

## Slide 78: Preparing for the assignment continued

Preparing for the assignment continued
CML3112, Week 3, slide 78

Explanation to give
A3 has five tasks in one notebook: a weight value, signed percentage-error function, programme-specific function, guarded efficiency function and the largest-error reading.

Worked illustration / lecturer answer
Explain the required names and return values. Compare a signed error by magnitude only for choosing the worst reading, then keep its original sign. Loops are not required for this six-reading task.

Misconception to address
The latest notebook needs no grading scripts. Submit one .ipynb, with no separate report. Keep any work already completed in an older notebook.

On this slide
Use the formula for your programme shown earlier. q4 specifies the zero-input behaviour. q5 uses the supplied six readings; trace them on paper, and use your own percentage-error function.

Loops are not required yet.

Current notebook workflow
The latest student package contains no grader scripts or g.check cells. Restart and run the completed notebook, then submit it. Existing older submissions remain valid.

Continue to
Unit conversions for the assignment

## Slide 79: Unit conversions for the assignment

Unit conversions for the assignment
CML3112, Week 3, slide 79

Explanation to give
Track the meaning and unit before substituting values. Mass is in kg, weight is in N, area in m² and volume in m³. Power is energy transferred per second, in W.

Worked illustration / lecturer answer
Convert 200 mm to 0.2 m by dividing by 1000. A separate 2 kg mass has weight 19.62 N using g = 9.81 m/s². A percentage 75 becomes fraction 0.75.

Misconception to address
Do not mix area, volume, mass and force. The name G is an uppercase convention for a fixed value, not an automatic unit system. Only introduce rpm conversion when that quantity is actually needed.

On this slide
Millimetres become metres by dividing by 1000: 200 mm is 0.2 m.

Percent becomes a fraction by dividing by 100: 75% is 0.75.

Only for rotational-speed questions: rpm means revolutions per minute. One revolution is 2π radians and one minute is 60 seconds, so multiply rpm by 2π/60.

Current notebook workflow
The latest student package contains no grader scripts or g.check cells. Restart and run the completed notebook, then submit it. Existing older submissions remain valid.

Continue to
Your issued assignment

## Slide 80: Your issued assignment

Your issued assignment
CML3112, Week 3, slide 80

Explanation to give
A3 has five tasks in one notebook: a weight value, signed percentage-error function, programme-specific function, guarded efficiency function and the largest-error reading.

Worked illustration / lecturer answer
Explain the required names and return values. Compare a signed error by magnitude only for choosing the worst reading, then keep its original sign. Loops are not required for this six-reading task.

Misconception to address
The latest notebook needs no grading scripts. Submit one .ipynb, with no separate report. Keep any work already completed in an older notebook.

On this slide
Open W03_student.ipynb.

Read every task and its input units before coding.

Keep the required function names and returned outputs.

Restart and run all cells, then save the completed notebook.

Current notebook workflow
The latest student package contains no grader scripts or g.check cells. Restart and run the completed notebook, then submit it. Existing older submissions remain valid.

Continue to
q1: 3 marks

## Slide 81: q1: 3 marks

Required interface: q1: 3 marks

A 40 kg motor sits on a bench.

Set weight_n to its weight in newtons, taking g = 9.81.

Keep these exact output keys and the function name. You may use descriptive local variable names, such as true_positive_count, but the returned dictionary must use the published key, such as tp. The grader checks keys and values; changing a key changes the interface.

## Slide 82: q2: 4 marks

Required interface: q2: 4 marks

Write percent_error(measured, expected) returning the signed percent error.

Keep these exact output keys and the function name. You may use descriptive local variable names, such as true_positive_count, but the returned dictionary must use the published key, such as tp. The grader checks keys and values; changing a key changes the interface.

## Slide 83: q3: 3 marks

Required interface: q3: 3 marks

Write slab_mass(area_m2, thickness_m) returning the mass of the concrete slab in kg, taking concrete as 2400 kg/m3.

Keep these exact output keys and the function name. You may use descriptive local variable names, such as true_positive_count, but the returned dictionary must use the published key, such as tp. The grader checks keys and values; changing a key changes the interface.

## Slide 84: q4: 5 marks

Required interface: q4: 5 marks

Write efficiency(out_w, in_w) returning the percentage, and returning None when in_w is zero or negative.

Keep these exact output keys and the function name. You may use descriptive local variable names, such as true_positive_count, but the returned dictionary must use the published key, such as tp. The grader checks keys and values; changing a key changes the interface.

## Slide 85: q5: 5 marks

Required interface: q5: 5 marks

READINGS is given in the notebook.

Using your own percent_error against a nominal of 100, set worst_reading to the reading with the largest error by size, and worst_error to that reading's signed percent error.

Keep these exact output keys and the function name. You may use descriptive local variable names, such as true_positive_count, but the returned dictionary must use the published key, such as tp. The grader checks keys and values; changing a key changes the interface.

## Slide 86: Engineering functions submission

Engineering functions submission
CML3112, Week 3, slide 86

Explanation to give
This slide hands over CML3112 W03. Show the exact form title before uploading. The required packet is one completed .ipynb notebook.

Worked illustration / lecturer answer
The recorded cutoff for this form is 2026-09-30T08:27:44.528Z. Check the live form for later changes. A replacement must contain the complete required file set, not just the changed file.

Misconception to address
Students enter their own Student Registration Number as required freeform text. They wait for filenames to appear, press Submit and keep the confirmation. A file saved in Drive or GitHub is not itself a form submission.

On this slide
Opens: 22 Sep 2026, 10:55 Kampala

Deadline: 29 Sep 2026, 11:00 Kampala

Use your full Student Registration Number in the form.

Keep the submitted files and confirmation.

Continue to
Week 3 quiz

## Slide 87: Week 3 quiz

Week 3 quiz
CML3112, Week 3, slide 87

Explanation to give
This is the CML3112 Week 3 quiz. The student link opens the response form; it does not activate its window. In Quiz Controls use open_W3_CML3112 when ready and read the logged closing time.

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

## Slide 88: Revision and submission checklist

Revision and submission checklist
CML3112, Week 3, slide 88

Explanation to give
Build calculations from values and operators, then decisions and functions, then collections. Define each symbol before using it in the program.

Worked illustration / lecturer answer
A definition stores instructions. double_value(4) runs them with x = 4 and returns 8. Printing that return value is a separate action.

Misconception to address
Close by identifying the actual saved file and its correct submission route. Read the live deadline. For current weekly notebook tasks, students upload their own work, not the practice notebook, ZIP or grading files.

On this slide
You can explain each input, the returned answer and its engineering unit.

Save your work and check the required submission files.

Continue to
Optional revision video

## Slide 89: Optional revision video

Optional revision video
CML3112, Week 3, slide 89

Explanation to give
Give the viewing question before playing the excerpt: How are numbers written and how do arithmetic operators change them?

Worked illustration / lecturer answer
Use the adjacent worked example as the explanation if the video cannot load. Pause after the relevant example and connect its terms to the names and units already used in this lesson. Preview the displayed link and excerpt before class.

Misconception to address
The video is supporting revision, not a replacement for defining the symbols or a requirement to watch a full tutorial during limited class time.

On this slide
For revision after class.

Corey Schafer
Python Tutorial for Beginners 3: Integers and Floats

Opening 00:00–04:00, suggested four-minute excerpt; preview before class

Listening question: How are numbers written and how do arithmetic operators change them?

Reference / existing resource
https://www.youtube.com/watch?v=khKv-8q7YmY