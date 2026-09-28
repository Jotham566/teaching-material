# CML3112 Week03 Design Infrastructure

Lecturer companion to the revised PowerPoint. Slide numbers match this edition. Explain the worked examples directly; revision checks are for individual study.

## Slide 1 — Python calculations and reusable functions

PURPOSE
Python calculations and reusable functions

CONNECT
Build on the preceding week. Explain why this example is needed before running it.

EXPLAIN
Civil Engineering and Architecture

LECTURER DETAIL
TEACHING PURPOSE
Python calculations and reusable functions

LECTURER CUE
Use PowerPoint Presenter View for these notes. Teach one example, pause for every learner to predict, then work an analogous example together. The practice notebook is a learning aid, not an extra graded upload.

EXPLAIN IN ORDINARY WORDS
A function is a named set of instructions. def defines it; a call runs it with inputs. Parameters are input names, arguments are supplied values, and return sends the result back.

CHECK AND EXPECTED ANSWER
Does print(8) return the number 8 to the caller? No; it displays 8 and returns None. A function needing a numeric result should return it.

IF LEARNERS ARE STUCK
Trace one call: bind input names, run the indented body, reach return, then put the returned result back into the calling expression.

NEXT
Today’s learning. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Today’s learning.

## Slide 2 — Today’s learning

PURPOSE
Today’s learning

CONNECT
Build on Python calculations and reusable functions. Explain why this example is needed before running it.

EXPLAIN
Read Python values and arithmetic symbols.

Define a function, call it and check its inputs.

LECTURER DETAIL
TEACHING PURPOSE
Today’s learning

CONNECT
Build on the preceding slide: Python calculations and reusable functions.

LECTURER CUE
Ask learners to explain this goal in ordinary language. The first successful attempt matters more than covering optional extensions. Defer: Five-function libraries, module imports, scope details, debugger setup and six independent bug hunts can wait. Demonstrate one ordinary traceback and one unit mistake now.

EXPLAIN IN ORDINARY WORDS
A function is a named set of instructions. def defines it; a call runs it with inputs. Parameters are input names, arguments are supplied values, and return sends the result back.

CHECK AND EXPECTED ANSWER
Does print(8) return the number 8 to the caller? No; it displays 8 and returns None. A function needing a numeric result should return it.

IF LEARNERS ARE STUCK
Trace one call: bind input names, run the indented body, reach return, then put the returned result back into the calling expression.

NEXT
Recall and a first attempt. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Recall and a first attempt.

## Slide 3 — Recall and a first attempt

PURPOSE
Recall and a first attempt

CONNECT
Build on Today’s learning. Explain why this example is needed before running it.

EXPLAIN
Run print(2 + 3). Which part is the instruction, and which part is the output?

LECTURER DETAIL
TEACHING PURPOSE
Recall and a first attempt

CONNECT
Build on the preceding slide: Today’s learning.

LECTURER CUE

EXPLAIN IN ORDINARY WORDS
Name the positive class first. Actual is what happened; predicted is the model decision. Precision asks how many predicted positives were right. Recall asks how many actual positives were found.

CHECK AND EXPECTED ANSWER
With TP=2, FP=1, FN=2: precision=2/3 and recall=2/4. A missed actual positive is a false negative.

IF LEARNERS ARE STUCK
Draw actual/predicted headings. Place one case at a time before calculating a fraction. Explain the task rule for a zero denominator.

NEXT
The engineering context. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
The engineering context.

## Slide 4 — The engineering context

PURPOSE
The engineering context

CONNECT
Build on Recall and a first attempt. Explain why this example is needed before running it.

EXPLAIN
A building team records indoor temperature to investigate comfort.

Civil students can discuss construction and inspection; architecture students can discuss shading and ventilation.

A measurement includes a number and its unit.

LECTURER DETAIL
TEACHING PURPOSE
The engineering context

CONNECT
Build on the preceding slide: Recall and a first attempt.

LECTURER CUE
A building team records indoor temperature to investigate comfort. Civil students can discuss construction and inspection; architecture students can discuss shading and ventilation. Explain the quantities before using them.

EXPLAIN IN ORDINARY WORDS
A calculated column stores a result for each row at refresh. A measure is evaluated under the filters of the current visual. SUMX evaluates an expression for each row before adding it.

CHECK AND EXPECTED ANSWER
Should revenue respond to a selected region? Yes; test the measure with that filter and reconcile it to known data.

IF LEARNERS ARE STUCK
Work one order line by hand, then two lines. Name the numerator and denominator populations before an average-order-value measure.

NEXT
Start with numbers and values. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Start with numbers and values.

## Slide 5 — Start with numbers and values

PURPOSE
Start with numbers and values

CONNECT
Build on The engineering context. Explain why this example is needed before running it.

EXPLAIN
Number: A number expresses how much or how many: 3 items or 2.5 metres. Whole numbers count; decimal numbers can describe a part of a unit.
Value and unit: A value is one piece of information. The number 2.5 is a value. A measurement also needs a unit, such as metres. Python does not attach that unit automatically.

LECTURER DETAIL
TEACHING PURPOSE
Start with numbers and values

CONNECT
Build on the preceding slide: The engineering context.

EXPLAIN IN ORDINARY WORDS
A value is a piece of information. A variable is a name referring to a value. In length_m = 5, Python evaluates the right side and binds that result to the name on the left.

CHECK AND EXPECTED ANSWER
After x=3 then x=5, what does print(x) display? 5. The earlier value is not added automatically.

IF LEARNERS ARE STUCK
Write the name on a card and the current value beside it. Distinguish number 3 from quoted text "3".

POINT TO THE DEFINITION
Number: A number expresses how much or how many: 3 items or 2.5 metres. Whole numbers count; decimal numbers can describe a part of a unit.
Value and unit: A value is one piece of information. The number 2.5 is a value. A measurement also needs a unit, such as metres. Python does not attach that unit automatically.

NEXT
Words we will use. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Words we will use.

## Slide 6 — Words we will use

PURPOSE
Words we will use

CONNECT
Build on Start with numbers and values. Explain why this example is needed before running it.

EXPLAIN
Variable: A name referring to a value. In length_m = 5, the right side is evaluated and assigned to length_m.
int, float, str, bool: int represents whole numbers; float represents approximate real numbers such as 2.5; str is text in quotes; bool is True or False.

LECTURER DETAIL
TEACHING PURPOSE
Words we will use

CONNECT
Build on the preceding slide: Start with numbers and values.

EXPLAIN IN ORDINARY WORDS
A value is a piece of information. A variable is a name referring to a value. In length_m = 5, Python evaluates the right side and binds that result to the name on the left.

CHECK AND EXPECTED ANSWER
After x=3 then x=5, what does print(x) display? 5. The earlier value is not added automatically.

IF LEARNERS ARE STUCK
Write the name on a card and the current value beside it. Distinguish number 3 from quoted text "3".

POINT TO THE DEFINITION
Variable: A name referring to a value. In length_m = 5, the right side is evaluated and assigned to length_m.
int, float, str, bool: int represents whole numbers; float represents approximate real numbers such as 2.5; str is text in quotes; bool is True or False.

NEXT
A variable refers to its current value. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
A variable refers to its current value.

## Slide 7 — A variable refers to its current value

PURPOSE
A variable refers to its current value

CONNECT
Build on Words we will use. Explain why this example is needed before running it.

EXPLAIN
After reassignment, thickness refers to 0.20.

LECTURER DETAIL
TEACHING PURPOSE
A variable refers to its current value

CONNECT
Build on the preceding slide: Words we will use.

LECTURER CUE
This box is a simplified model of a name referring to a value. Other names could still refer to an earlier object.
Source: existing course illustration figs/variable_box.png. These are illustrative examples, not this cohort’s assessed results.

EXPLAIN IN ORDINARY WORDS
A value is a piece of information. A variable is a name referring to a value. In length_m = 5, Python evaluates the right side and binds that result to the name on the left.

CHECK AND EXPECTED ANSWER
After x=3 then x=5, what does print(x) display? 5. The earlier value is not added automatically.

IF LEARNERS ARE STUCK
Write the name on a card and the current value beside it. Distinguish number 3 from quoted text "3".

NEXT
Python values have types. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Python values have types.

## Slide 8 — Python values have types

PURPOSE
Python values have types

CONNECT
Build on A variable refers to its current value. Explain why this example is needed before running it.

EXPLAIN
3.5 + 2 gives 5.5. "3.5" + "2" joins text into "3.52".

LECTURER DETAIL
TEACHING PURPOSE
Python values have types

CONNECT
Build on the preceding slide: A variable refers to its current value.

LECTURER CUE
3.5 + 2 gives 5.5. "3.5" + "2" joins text into "3.52".

EXPLAIN IN ORDINARY WORDS
A value is a piece of information. A variable is a name referring to a value. In length_m = 5, Python evaluates the right side and binds that result to the name on the left.

CHECK AND EXPECTED ANSWER
After x=3 then x=5, what does print(x) display? 5. The earlier value is not added automatically.

IF LEARNERS ARE STUCK
Write the name on a card and the current value beside it. Distinguish number 3 from quoted text "3".

READ THE VISUAL
Start with the title and labels. Read one row or mark aloud, including its unit. Let a learner read a second one before discussing the pattern. Do not infer a numerical value from an unlabelled drawing.

NEXT
Operator. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Operator.

## Slide 9 — Operator

PURPOSE
Operator

CONNECT
Build on Python values have types. Explain why this example is needed before running it.

EXPLAIN
Operator: A symbol for an operation: + adds, - subtracts, * multiplies, / divides, ** raises to a power. // floors a quotient, so -5 // 2 is -3.

LECTURER DETAIL
TEACHING PURPOSE
Operator

CONNECT
Build on the preceding slide: Python values have types.

EXPLAIN IN ORDINARY WORDS
Read each quantity and unit before using a formula. Python calculates numbers but does not enforce physical units. Parentheses specify which operation happens first.

CHECK AND EXPECTED ANSWER
What is 5 m times 3 m? 15 square metres. What is 7/2 in Python? 3.5; 7//2 is 3.

IF LEARNERS ARE STUCK
Write the formula and units on paper, substitute small values, then translate it to Python. Check zero denominators and the issued sign convention.

POINT TO THE DEFINITION
Operator: A symbol for an operation: + adds, - subtracts, * multiplies, / divides, ** raises to a power. // floors a quotient, so -5 // 2 is -3.

NEXT
Read a function call before using it. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Read a function call before using it.

## Slide 10 — Read a function call before using it

PURPOSE
Read a function call before using it

CONNECT
Build on Operator. Explain why this example is needed before running it.

EXPLAIN
A built-in function: Python already provides tools such as print, type and float. A function call asks a named tool to do its work: print(3) displays 3.
Parentheses, quotes and comments: Parentheses hold the inputs to a call. Quotes make text: "3.5" is text; float("3.5") converts it to a number. # starts a comment that Python does not run.

LECTURER DETAIL
TEACHING PURPOSE
Read a function call before using it

CONNECT
Build on the preceding slide: Operator.

EXPLAIN IN ORDINARY WORDS
A function is a named set of instructions. def defines it; a call runs it with inputs. Parameters are input names, arguments are supplied values, and return sends the result back.

CHECK AND EXPECTED ANSWER
Does print(8) return the number 8 to the caller? No; it displays 8 and returns None. A function needing a numeric result should return it.

IF LEARNERS ARE STUCK
Trace one call: bind input names, run the indented body, reach return, then put the returned result back into the calling expression.

POINT TO THE DEFINITION
A built-in function: Python already provides tools such as print, type and float. A function call asks a named tool to do its work: print(3) displays 3.
Parentheses, quotes and comments: Parentheses hold the inputs to a call. Quotes make text: "3.5" is text; float("3.5") converts it to a number. # starts a comment that Python does not run.

NEXT
Reading Python symbols. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Reading Python symbols.

## Slide 11 — Reading Python symbols

PURPOSE
Reading Python symbols

CONNECT
Build on Read a function call before using it. Explain why this example is needed before running it.

EXPLAIN
= assigns a value to a name. == compares two values.

* multiplies. / divides. ** raises to a power.

Parentheses pass inputs when we call a function.

Indented lines belong to the block above them.

LECTURER DETAIL
TEACHING PURPOSE
Reading Python symbols

CONNECT
Build on the preceding slide: Read a function call before using it.

EXPLAIN IN ORDINARY WORDS
Read each quantity and unit before using a formula. Python calculates numbers but does not enforce physical units. Parentheses specify which operation happens first.

CHECK AND EXPECTED ANSWER
What is 5 m times 3 m? 15 square metres. What is 7/2 in Python? 3.5; 7//2 is 3.

IF LEARNERS ARE STUCK
Write the formula and units on paper, substitute small values, then translate it to Python. Check zero denominators and the issued sign convention.

NEXT
Names, conversion and comments. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Names, conversion and comments.

## Slide 12 — Names, conversion and comments

PURPOSE
Names, conversion and comments

CONNECT
Build on Reading Python symbols. Explain why this example is needed before running it.

EXPLAIN
type(...) reports the kind of value. <class 'float'> means a floating-point number.

LECTURER DETAIL
TEACHING PURPOSE
Names, conversion and comments

CONNECT
Build on the preceding slide: Reading Python symbols.

LECTURER CUE
Read each symbol before running. Ask everyone to predict. Expected output: 7.0 then <class 'float'>

EXPLAIN IN ORDINARY WORDS
Read each quantity and unit before using a formula. Python calculates numbers but does not enforce physical units. Parentheses specify which operation happens first.

CHECK AND EXPECTED ANSWER
What is 5 m times 3 m? 15 square metres. What is 7/2 in Python? 3.5; 7//2 is 3.

IF LEARNERS ARE STUCK
Write the formula and units on paper, substitute small values, then translate it to Python. Check zero denominators and the issued sign convention.

WALK THROUGH THIS CODE
float converts numeric text into a decimal number.
type reports the kind of value: for example, float.
print displays a value below the cell.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Arithmetic that needs care. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Week 3 continuation.

## Slide 13 — Week 3 continuation

PURPOSE
Week 3 continuation

CONNECT
Build on Names, conversion and comments. Explain why this example is needed before running it.

EXPLAIN
From slides 1–12: values have types, variables name values, = assigns, and print displays a result. float("3.5") converts text to a number. We now use those ideas in calculations and functions.

Next: arithmetic, decisions, functions, then lists and the A3 brief.

LECTURER DETAIL
For CML3112 resume here after teaching original slides 1–12. Briefly show the output from the previous example: 7.0 and <class 'float'>. No need to reteach all twelve slides.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Arithmetic that needs care.

## Slide 14 — Arithmetic that needs care

PURPOSE
Arithmetic that needs care

CONNECT
Build on Week 3 continuation. Explain why this example is needed before running it.

EXPLAIN
Parentheses run first: (2 + 4) / 2 is 3.0. Without them, division runs before addition: 2 + 4 / 2 is 4.0.

/ gives a quotient. // rounds that quotient down: 7 // 2 is 3 and -7 // 2 is -4.

Many decimal fractions are approximate in a computer. A tolerance is an allowed difference, for example 0.01 m when checking two calculated lengths.

LECTURER DETAIL
TEACHING PURPOSE
Arithmetic that needs care

CONNECT
Build on the preceding slide: Names, conversion and comments.

LECTURER CUE
Floor division rounds down. Use parentheses to state the intended calculation. Keep units in variable names.

EXPLAIN IN ORDINARY WORDS
Read each quantity and unit before using a formula. Python calculates numbers but does not enforce physical units. Parentheses specify which operation happens first.

CHECK AND EXPECTED ANSWER
What is 5 m times 3 m? 15 square metres. What is 7/2 in Python? 3.5; 7//2 is 3.

IF LEARNERS ARE STUCK
Write the formula and units on paper, substitute small values, then translate it to Python. Check zero denominators and the issued sign convention.

NEXT
Read the quantities in your programme example. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Read the quantities in your programme example.

## Slide 15 — Read the quantities in your programme example

PURPOSE
Read the quantities in your programme example

CONNECT
Build on Arithmetic that needs care. Explain why this example is needed before running it.

EXPLAIN
Length, width and area: Length and width are distances in metres (m). A rectangle’s area is length × width, measured in square metres (m²).
Thickness and density: Thickness is the third distance. Area × thickness gives volume in m³. Density is mass per volume, in kg/m³; volume × density gives mass in kg.

LECTURER DETAIL
TEACHING PURPOSE
Read the quantities in your programme example

CONNECT
Build on the preceding slide: Arithmetic that needs care.

EXPLAIN IN ORDINARY WORDS
Read each quantity and unit before using a formula. Python calculates numbers but does not enforce physical units. Parentheses specify which operation happens first.

CHECK AND EXPECTED ANSWER
What is 5 m times 3 m? 15 square metres. What is 7/2 in Python? 3.5; 7//2 is 3.

IF LEARNERS ARE STUCK
Write the formula and units on paper, substitute small values, then translate it to Python. Check zero denominators and the issued sign convention.

POINT TO THE DEFINITION
Length, width and area: Length and width are distances in metres (m). A rectangle’s area is length × width, measured in square metres (m²).
Thickness and density: Thickness is the third distance. Area × thickness gives volume in m³. Density is mass per volume, in kg/m³; volume × density gives mass in kg.

NEXT
A calculation for your programme. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
A calculation for your programme.

## Slide 16 — A calculation for your programme

PURPOSE
A calculation for your programme

CONNECT
Build on Read the quantities in your programme example. Explain why this example is needed before running it.

EXPLAIN
A rectangular floor is 5 m long and 3 m wide.

Area = length × width = 15 m².

LECTURER DETAIL
TEACHING PURPOSE
A calculation for your programme

CONNECT
Build on the preceding slide: Read the quantities in your programme example.

LECTURER CUE
A rectangular floor is 5 m long and 3 m wide. Area = length × width = 15 m².

NEXT
The calculation in Python. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
The calculation in Python.

## Slide 17 — The calculation in Python

PURPOSE
The calculation in Python

CONNECT
Build on A calculation for your programme. Explain why this example is needed before running it.

EXPLAIN
Read top to bottom. Run the complete example in the matching practice notebook.

LECTURER DETAIL
TEACHING PURPOSE
The calculation in Python

CONNECT
Build on the preceding slide: A calculation for your programme.

LECTURER CUE
Read each name and unit. = assigns the number, * multiplies and / divides. print displays the result. A rectangular floor is 5 m long and 3 m wide. Area = length × width = 15 m².

Complete practice code:
length_m = 5
width_m = 3
area_m2 = length_m * width_m
print(area_m2)

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

WALK THROUGH THIS CODE
print displays a value below the cell.
= assigns the value on the right to the name on the left.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
A change to predict. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Reading an error message.

## Slide 18 — Reading an error message

PURPOSE
Reading an error message

CONNECT
Build on The calculation in Python. Explain why this example is needed before running it.

EXPLAIN
The last line names the error. The indicated line shows where Python noticed it.

LECTURER DETAIL
TEACHING PURPOSE
Reading an error message

CONNECT
Build on the preceding slide: The practice result.

LECTURER CUE
Read one row at a time and use a changed value. This is a syntax reference for the worked examples.

READ THE VISUAL
Start with the title and labels. Read one row or mark aloud, including its unit. Let a learner read a second one before discussing the pattern. Do not infer a numerical value from an unlabelled drawing.

NEXT
Condition. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Condition.

## Slide 19 — Condition

PURPOSE
Condition

CONNECT
Build on Reading an error message. Explain why this example is needed before running it.

EXPLAIN
Condition: A True/False question. == compares equality; = assigns. if selects a branch; else handles the other case. A colon starts an indented block.

LECTURER DETAIL
TEACHING PURPOSE
Condition

CONNECT
Build on the preceding slide: Reading an error message.

EXPLAIN IN ORDINARY WORDS
A condition is a True/False question. Python executes the matching indented branch. = assigns; == compares. >= includes the boundary, while > excludes it.

CHECK AND EXPECTED ANSWER
With value 30, is value >= 30 true? Yes. Is value > 30 true? No.

IF LEARNERS ARE STUCK
Try one value below, at and above the boundary before running the code.

POINT TO THE DEFINITION
Condition: A True/False question. == compares equality; = assigns. if selects a branch; else handles the other case. A colon starts an indented block.

NEXT
Comparison and logic. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Comparison and logic.

## Slide 20 — Comparison and logic

PURPOSE
Comparison and logic

CONNECT
Build on Condition. Explain why this example is needed before running it.

EXPLAIN
> means greater than; < means less than; <= means at most. = assigns, while == compares. True and False are Boolean values.

LECTURER DETAIL
TEACHING PURPOSE
Comparison and logic

CONNECT
Build on the preceding slide: Condition.

LECTURER CUE
Read one row at a time and use a changed value. This is a syntax reference for the worked examples.

EXPLAIN IN ORDINARY WORDS
A condition is a True/False question. Python executes the matching indented branch. = assigns; == compares. >= includes the boundary, while > excludes it.

CHECK AND EXPECTED ANSWER
With value 30, is value >= 30 true? Yes. Is value > 30 true? No.

IF LEARNERS ARE STUCK
Try one value below, at and above the boundary before running the code.

READ THE VISUAL
Start with the title and labels. Read one row or mark aloud, including its unit. Let a learner read a second one before discussing the pattern. Do not infer a numerical value from an unlabelled drawing.

NEXT
A decision needs a colon and indentation. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
A decision needs a colon and indentation.

## Slide 21 — A decision needs a colon and indentation

PURPOSE
A decision needs a colon and indentation

CONNECT
Build on Comparison and logic. Explain why this example is needed before running it.

EXPLAIN
>= compares values. Only the chosen indented block runs.

LECTURER DETAIL
TEACHING PURPOSE
A decision needs a colon and indentation

CONNECT
Build on the preceding slide: Comparison and logic.

LECTURER CUE
Read each symbol before running. Ask everyone to predict. Expected output: below 30. Change 28 to 30 and predict warm. This is a toy threshold, not an engineering limit.

EXPLAIN IN ORDINARY WORDS
A condition is a True/False question. Python executes the matching indented branch. = assigns; == compares. >= includes the boundary, while > excludes it.

CHECK AND EXPECTED ANSWER
With value 30, is value >= 30 true? Yes. Is value > 30 true? No.

IF LEARNERS ARE STUCK
Try one value below, at and above the boundary before running the code.

WALK THROUGH THIS CODE
if tests a condition. The chosen indented block runs.
print displays a value below the cell.
= assigns the value on the right to the name on the left.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Function. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
More than two branches.

## Slide 22 — More than two branches

PURPOSE
More than two branches

CONNECT
Build on A decision needs a colon and indentation. Explain why this example is needed before running it.

EXPLAIN
if tests the first condition. elif means “otherwise, if” and tests another condition only if the earlier one was false. else handles the remaining case.

Python runs only the first matching branch. Put a narrower condition before a broader one that would also match. A colon and indentation mark each body.

LECTURER DETAIL
TEACHING PURPOSE
Units branches and error messages continued

CONNECT
Build on the preceding slide: Units branches and error messages.

LECTURER CUE
Teach these concepts before the weekly quiz. Use changed numbers for practice. This slide supplies concepts, not the quiz key.

EXPLAIN IN ORDINARY WORDS
A condition is a True/False question. Python executes the matching indented branch. = assigns; == compares. >= includes the boundary, while > excludes it.

CHECK AND EXPECTED ANSWER
With value 30, is value >= 30 true? Yes. Is value > 30 true? No.

IF LEARNERS ARE STUCK
Try one value below, at and above the boundary before running the code.

NEXT
Units branches and error messages continued. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Tracing an if elif else chain.

## Slide 23 — Tracing an if elif else chain

PURPOSE
Tracing an if elif else chain

CONNECT
Build on More than two branches. Explain why this example is needed before running it.

EXPLAIN
Output: medium. The first condition is false; the second is true.

LECTURER DETAIL
Output: medium. The first condition is false; the second is true.

level = 7
if level >= 10:
    print("high")
elif level >= 5:
    print("medium")
else:
    print("low")

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Function.

## Slide 24 — Function

PURPOSE
Function

CONNECT
Build on Tracing an if elif else chain. Explain why this example is needed before running it.

EXPLAIN
Function: A named, reusable calculation or procedure. def introduces its definition. Parameters are the names for its inputs; arguments are the values supplied when calling it.

LECTURER DETAIL
TEACHING PURPOSE
Function

CONNECT
Build on the preceding slide: A decision needs a colon and indentation.

EXPLAIN IN ORDINARY WORDS
A function is a named set of instructions. def defines it; a call runs it with inputs. Parameters are input names, arguments are supplied values, and return sends the result back.

CHECK AND EXPECTED ANSWER
Does print(8) return the number 8 to the caller? No; it displays 8 and returns None. A function needing a numeric result should return it.

IF LEARNERS ARE STUCK
Trace one call: bind input names, run the indented body, reach return, then put the returned result back into the calling expression.

POINT TO THE DEFINITION
Function: A named, reusable calculation or procedure. def introduces its definition. Parameters are the names for its inputs; arguments are the values supplied when calling it.

NEXT
Indentation and return. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Indentation and return.

## Slide 25 — Indentation and return

PURPOSE
Indentation and return

CONNECT
Build on Function. Explain why this example is needed before running it.

EXPLAIN
Indentation and return: Spaces at the start of a line group the function body. return hands a result to the calling code. print displays a value and returns None.

LECTURER DETAIL
TEACHING PURPOSE
Indentation and return

CONNECT
Build on the preceding slide: Function.

EXPLAIN IN ORDINARY WORDS
A function is a named set of instructions. def defines it; a call runs it with inputs. Parameters are input names, arguments are supplied values, and return sends the result back.

CHECK AND EXPECTED ANSWER
Does print(8) return the number 8 to the caller? No; it displays 8 and returns None. A function needing a numeric result should return it.

IF LEARNERS ARE STUCK
Trace one call: bind input names, run the indented body, reach return, then put the returned result back into the calling expression.

POINT TO THE DEFINITION
Indentation and return: Spaces at the start of a line group the function body. return hands a result to the calling code. print displays a value and returns None.

NEXT
A function definition and a call. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
A function definition and a call.

## Slide 26 — A function definition and a call

PURPOSE
A function definition and a call

CONNECT
Build on Indentation and return. Explain why this example is needed before running it.

EXPLAIN
def gives a reusable calculation a name and inputs.

Defining a function remembers the instructions.

Calling the function runs those instructions with values.

return sends the result back to the caller.

LECTURER DETAIL
TEACHING PURPOSE
A function definition and a call

CONNECT
Build on the preceding slide: Indentation and return.

EXPLAIN IN ORDINARY WORDS
A function is a named set of instructions. def defines it; a call runs it with inputs. Parameters are input names, arguments are supplied values, and return sends the result back.

CHECK AND EXPECTED ANSWER
Does print(8) return the number 8 to the caller? No; it displays 8 and returns None. A function needing a numeric result should return it.

IF LEARNERS ARE STUCK
Trace one call: bind input names, run the indented body, reach return, then put the returned result back into the calling expression.

NEXT
A calculation has inputs and an answer. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Inputs, instructions and a returned result.

## Slide 27 — Inputs, instructions and a returned result

PURPOSE
Inputs, instructions and a returned result

CONNECT
Build on A function definition and a call. Explain why this example is needed before running it.

EXPLAIN
The illustration uses slab_volume: length × width × thickness. The next function uses the same input/body/return pattern.

LECTURER DETAIL
TEACHING PURPOSE
Inputs, instructions and a returned result

CONNECT
Build on the preceding slide: A reusable calculation.

LECTURER CUE
Read def, the name, parameters, colon, indentation, return and call. Definition creates the function. Its body waits for a call. Distinguish print, which displays, from return, which passes a value back.
Source: existing course illustration figs/function_anatomy.png. These are illustrative examples, not this cohort’s assessed results.

EXPLAIN IN ORDINARY WORDS
A function is a named set of instructions. def defines it; a call runs it with inputs. Parameters are input names, arguments are supplied values, and return sends the result back.

CHECK AND EXPECTED ANSWER
Does print(8) return the number 8 to the caller? No; it displays 8 and returns None. A function needing a numeric result should return it.

IF LEARNERS ARE STUCK
Trace one call: bind input names, run the indented body, reach return, then put the returned result back into the calling expression.

NEXT
Following a function call. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Defining and calling double_value.

## Slide 28 — Defining and calling double_value

PURPOSE
Defining and calling double_value

CONNECT
Build on Inputs, instructions and a returned result. Explain why this example is needed before running it.

EXPLAIN
Output: 8. Calling passes 4 to x; return sends 8 back; print displays it.

LECTURER DETAIL
TEACHING PURPOSE
Worked example

CONNECT
Build on the preceding slide: Following a function call.

LECTURER CUE
Work the cohort formula by hand before opening Python. State every unit. Use the four-line cohort calculation first; do not begin with formatting, imports or a long function. Introduce one reusable calculation using the example below. Read def, the function name, parentheses, parameter, colon, indentation and return separately. Defining the function does not run its body. Calling double_value(4) supplies 4 for x, calculates 8 and returns 8. The outer print displays it. Then teach an if/else guard with a separate small example.

Complete practice code:
def double_value(x):
    return x * 2

EXPLAIN IN ORDINARY WORDS
A function is a named set of instructions. def defines it; a call runs it with inputs. Parameters are input names, arguments are supplied values, and return sends the result back.

CHECK AND EXPECTED ANSWER
Does print(8) return the number 8 to the caller? No; it displays 8 and returns None. A function needing a numeric result should return it.

IF LEARNERS ARE STUCK
Trace one call: bind input names, run the indented body, reach return, then put the returned result back into the calling expression.

WALK THROUGH THIS CODE
def names the function. Inputs go inside parentheses.
return sends the result back to the caller.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Worked example continued. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Positional and named inputs.

## Slide 29 — Positional and named inputs

PURPOSE
Positional and named inputs

CONNECT
Build on Defining and calling double_value. Explain why this example is needed before running it.

EXPLAIN
Both calls supply the same inputs. return makes the result reusable.

LECTURER DETAIL
TEACHING PURPOSE
Positional and named inputs

CONNECT
Build on the preceding slide: Worked example continued.

LECTURER CUE
Read each symbol before running. Ask everyone to predict. Expected output: 6 then 6

EXPLAIN IN ORDINARY WORDS
A function is a named set of instructions. def defines it; a call runs it with inputs. Parameters are input names, arguments are supplied values, and return sends the result back.

CHECK AND EXPECTED ANSWER
Does print(8) return the number 8 to the caller? No; it displays 8 and returns None. A function needing a numeric result should return it.

IF LEARNERS ARE STUCK
Trace one call: bind input names, run the indented body, reach return, then put the returned result back into the calling expression.

WALK THROUGH THIS CODE
def names the function. Inputs go inside parentheses.
return sends the result back to the caller.
print displays a value below the cell.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Worked example continued. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
An input check before division.

## Slide 30 — An input check before division

PURPOSE
An input check before division

CONNECT
Build on Positional and named inputs. Explain why this example is needed before running it.

EXPLAIN
Division by zero raises ZeroDivisionError. We choose to return None when people is zero, so there is no calculated share.

The check belongs inside the function, before the division. return ends that call immediately. A valid input follows the later return line.

LECTURER DETAIL


TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
A function with a zero-input check.

## Slide 31 — A function with a zero-input check

PURPOSE
A function with a zero-input check

CONNECT
Build on An input check before division. Explain why this example is needed before running it.

EXPLAIN
Output: 4.0. safe_share(12, 0) returns None before any division.

LECTURER DETAIL
TEACHING PURPOSE
Worked example continued

CONNECT
Build on the preceding slide: Positional and named inputs.

LECTURER CUE
Work the cohort formula by hand before opening Python. State every unit. Use the four-line cohort calculation first; do not begin with formatting, imports or a long function. Introduce one reusable calculation using the example below. Read def, the function name, parentheses, parameter, colon, indentation and return separately. Defining the function does not run its body. Calling double_value(4) supplies 4 for x, calculates 8 and returns 8. The outer print displays it. Then teach an if/else guard with a separate small example.

Complete practice code:
def safe_share(total, people):
    if people == 0:
        return None
    return total / people

EXPLAIN IN ORDINARY WORDS
A function is a named set of instructions. def defines it; a call runs it with inputs. Parameters are input names, arguments are supplied values, and return sends the result back.

CHECK AND EXPECTED ANSWER
Does print(8) return the number 8 to the caller? No; it displays 8 and returns None. A function needing a numeric result should return it.

IF LEARNERS ARE STUCK
Trace one call: bind input names, run the indented body, reach return, then put the returned result back into the calling expression.

WALK THROUGH THIS CODE
def names the function. Inputs go inside parentheses.
if tests a condition. The chosen indented block runs.
return sends the result back to the caller.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Worked example continued. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
A branch with a clear boundary.

## Slide 32 — A branch with a clear boundary

PURPOSE
A branch with a clear boundary

CONNECT
Build on A function with a zero-input check. Explain why this example is needed before running it.

EXPLAIN
Read from the top. >= includes the boundary.

Only the selected branch runs.

Try the value exactly at 10 as well as 9 and 11.

LECTURER DETAIL
TEACHING PURPOSE
A branch with a clear boundary

CONNECT
Build on the preceding slide: Expected output.

LECTURER CUE
Read from the top. >= includes the boundary. Only the selected branch runs. Try the value exactly at 10 as well as 9 and 11.

EXPLAIN IN ORDINARY WORDS
A condition is a True/False question. Python executes the matching indented branch. = assigns; == compares. >= includes the boundary, while > excludes it.

CHECK AND EXPECTED ANSWER
With value 30, is value >= 30 true? Yes. Is value > 30 true? No.

IF LEARNERS ARE STUCK
Try one value below, at and above the boundary before running the code.

NEXT
A branch with a clear boundary in Python. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
A branch with a clear boundary in Python.

## Slide 33 — A branch with a clear boundary in Python

PURPOSE
A branch with a clear boundary in Python

CONNECT
Build on A branch with a clear boundary. Explain why this example is needed before running it.

EXPLAIN
Read top to bottom. Run the complete example in the matching practice notebook.

LECTURER DETAIL
TEACHING PURPOSE
A branch with a clear boundary in Python

CONNECT
Build on the preceding slide: A branch with a clear boundary.

LECTURER CUE
Read from the top. >= includes the boundary. Only the selected branch runs. Try the value exactly at 10 as well as 9 and 11.

Complete practice code:
def check_level(value):
    if value >= 10:
        return "high"
    return "low"

print(check_level(10))
print(check_level(9))

EXPLAIN IN ORDINARY WORDS
A condition is a True/False question. Python executes the matching indented branch. = assigns; == compares. >= includes the boundary, while > excludes it.

CHECK AND EXPECTED ANSWER
With value 30, is value >= 30 true? Yes. Is value > 30 true? No.

IF LEARNERS ARE STUCK
Try one value below, at and above the boundary before running the code.

WALK THROUGH THIS CODE
def names the function. Inputs go inside parentheses.
if tests a condition. The chosen indented block runs.
return sends the result back to the caller.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Selecting a largest error without loops. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
One value and a collection of values.

## Slide 34 — One value and a collection of values

PURPOSE
One value and a collection of values

CONNECT
Build on A branch with a clear boundary in Python. Explain why this example is needed before running it.

EXPLAIN
A variable can refer to one value: reading = 98. A collection stores several related values under one name.

Python has several collection types. Choose one according to how you need to find, change or organise its contents.

LECTURER DETAIL


TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Lists dictionaries tuples and sets.

## Slide 35 — Lists dictionaries tuples and sets

PURPOSE
Lists dictionaries tuples and sets

CONNECT
Build on One value and a collection of values. Explain why this example is needed before running it.

EXPLAIN
List and tuple positions start at zero. Dictionaries use keys. Sets have no positional index.

LECTURER DETAIL
List and tuple positions start at zero. Dictionaries use keys. Sets have no positional index.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
A list stores values in positions.

## Slide 36 — A list stores values in positions

PURPOSE
A list stores values in positions

CONNECT
Build on Lists dictionaries tuples and sets. Explain why this example is needed before running it.

EXPLAIN
readings = [98, 105, 92] creates a list. Square brackets enclose the items; commas separate them.

An index is an item’s position. Python starts counting at zero: readings[0] is 98, readings[1] is 105, readings[2] is 92.

Three items have positions 0, 1 and 2. readings[3] raises IndexError because there is no fourth item.

LECTURER DETAIL


TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Creating and reading a list.

## Slide 37 — Creating and reading a list

PURPOSE
Creating and reading a list

CONNECT
Build on A list stores values in positions. Explain why this example is needed before running it.

EXPLAIN
Output: [98, 105, 92], then 98, then 3.

LECTURER DETAIL
Output: [98, 105, 92], then 98, then 3.

readings = [98, 105, 92]
print(readings)
print(readings[0])
print(len(readings))

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Choosing the right collection.

## Slide 38 — Choosing the right collection

PURPOSE
Choosing the right collection

CONNECT
Build on Creating and reading a list. Explain why this example is needed before running it.

EXPLAIN
A dictionary connects a key to a value: {"reading": 98}. The colon connects them; record["reading"] finds the value by its key.

A tuple such as (2, 3) stores ordered items whose positions cannot be reassigned. A set such as {"A", "B"} stores distinct items without positions.

We use a list for today’s readings because their order matters. Week 4 develops dictionary, tuple and set operations before we use them with records.

LECTURER DETAIL


TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
A method belongs to a value.

## Slide 39 — A method belongs to a value

PURPOSE
A method belongs to a value

CONNECT
Build on Choosing the right collection. Explain why this example is needed before running it.

EXPLAIN
A function is called by name: len(readings). A method is called through a value with a dot: readings.index(105).

index searches a list for a value and returns its first position. Here readings.index(105) returns 1. A missing value raises ValueError.

The parentheses contain inputs to the operation. The square brackets in readings[1] select an item; they do a different job.

LECTURER DETAIL


TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Selecting a largest error without loops.

## Slide 40 — Selecting a largest error without loops

PURPOSE
Selecting a largest error without loops

CONNECT
Build on A method belongs to a value. Explain why this example is needed before running it.

EXPLAIN
An error is measured − expected. Its sign shows the direction. abs gives its magnitude: abs(-8) is 8.

max finds the largest supplied value: max(2, 5, 8) is 8. Compare magnitudes when the task asks for the largest error by size.

Keep the original signed error as well, because the magnitude alone loses direction.

LECTURER DETAIL
TEACHING PURPOSE
Selecting a largest error without loops

CONNECT
Build on the preceding slide: A branch with a clear boundary in Python.

LECTURER CUE
A list holds several values. abs removes the sign when measuring the SIZE of an error. max returns the largest supplied value. Keep the original signed error when the task asks for direction.

EXPLAIN IN ORDINARY WORDS
The size of an error is its absolute value. Keep the original sign and the matching reading. Find the position of the largest size, then use that same position in both original lists.

CHECK AND EXPECTED ANSWER
For errors [-2,5,-8], sizes are [2,5,8]. The maximum size is 8 at position 2; the original signed error is -8.

IF LEARNERS ARE STUCK
Draw the readings, signed errors and sizes in aligned columns. Circle the position rather than replacing the signed error with its absolute value.

NEXT
Reading a short list. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Selecting a largest error without loops in Python.

## Slide 41 — Selecting a largest error without loops in Python

PURPOSE
Selecting a largest error without loops in Python

CONNECT
Build on Selecting a largest error without loops. Explain why this example is needed before running it.

EXPLAIN
Read top to bottom. Run the complete example in the matching practice notebook.

LECTURER DETAIL
TEACHING PURPOSE
Selecting a largest error without loops in Python

CONNECT
Build on the preceding slide: Reading a short list.

LECTURER CUE
A list holds several values. abs removes the sign when measuring the SIZE of an error. max returns the largest supplied value. Keep the original signed error when the task asks for direction.

Complete practice code:
errors = [-2, 5, -8]
largest = max(abs(errors[0]), abs(errors[1]), abs(errors[2]))
print(largest)

EXPLAIN IN ORDINARY WORDS
The size of an error is its absolute value. Keep the original sign and the matching reading. Find the position of the largest size, then use that same position in both original lists.

CHECK AND EXPECTED ANSWER
For errors [-2,5,-8], sizes are [2,5,8]. The maximum size is 8 at position 2; the original signed error is -8.

IF LEARNERS ARE STUCK
Draw the readings, signed errors and sizes in aligned columns. Circle the position rather than replacing the signed error with its absolute value.

WALK THROUGH THIS CODE
print displays a value below the cell.
Square brackets create a list or select an item.
= assigns the value on the right to the name on the left.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Keep the reading beside its signed error. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Keep the reading beside its signed error.

## Slide 42 — Keep the reading beside its signed error

PURPOSE
Keep the reading beside its signed error

CONNECT
Build on Selecting a largest error without loops in Python. Explain why this example is needed before running it.

EXPLAIN
These paired lists use the same positions: the first error belongs to the first reading. The sign tells the direction; abs gives only the size.

index(value) finds the first position containing that value. Use that position in the original lists. An exact tie selects the first here; follow the issued task’s rule.

LECTURER DETAIL
TEACHING PURPOSE
Keep the reading beside its signed error

CONNECT
Build on the preceding slide: Selecting a largest error without loops in Python.

EXPLAIN IN ORDINARY WORDS
The size of an error is its absolute value. Keep the original sign and the matching reading. Find the position of the largest size, then use that same position in both original lists.

CHECK AND EXPECTED ANSWER
For errors [-2,5,-8], sizes are [2,5,8]. The maximum size is 8 at position 2; the original signed error is -8.

IF LEARNERS ARE STUCK
Draw the readings, signed errors and sizes in aligned columns. Circle the position rather than replacing the signed error with its absolute value.

NEXT
Find a position, then recover the original values. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Find a position, then recover the original values.

## Slide 43 — Find a position, then recover the original values

PURPOSE
Find a position, then recover the original values

CONNECT
Build on Keep the reading beside its signed error. Explain why this example is needed before running it.

EXPLAIN
Expected: 92 -8. The largest size is 8; the signed error is -8.

LECTURER DETAIL
TEACHING PURPOSE
Find a position, then recover the original values

CONNECT
Build on the preceding slide: Keep the reading beside its signed error.

LECTURER CUE
Expected: 92 -8. The largest size is 8; the signed error is -8.

Complete practice code:
readings = [98, 105, 92]
errors = [-2, 5, -8]
sizes = [abs(errors[0]), abs(errors[1]), abs(errors[2])]
position = sizes.index(max(sizes))
print(readings[position], errors[position])

EXPLAIN IN ORDINARY WORDS
The size of an error is its absolute value. Keep the original sign and the matching reading. Find the position of the largest size, then use that same position in both original lists.

CHECK AND EXPECTED ANSWER
For errors [-2,5,-8], sizes are [2,5,8]. The maximum size is 8 at position 2; the original signed error is -8.

IF LEARNERS ARE STUCK
Draw the readings, signed errors and sizes in aligned columns. Circle the position rather than replacing the signed error with its absolute value.

WALK THROUGH THIS CODE
print displays a value below the cell.
Square brackets create a list or select an item.
= assigns the value on the right to the name on the left.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
You are the function. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Revision example and answer.

## Slide 44 — Revision example and answer

PURPOSE
Revision example and answer

CONNECT
Build on Find a position, then recover the original values. Explain why this example is needed before running it.

EXPLAIN
Example: Write triple_value(x). Predict triple_value(5). Then predict safe_share(12, 0).

Answer: triple_value returns x * 3. The calls give 15 and None respectively. The guard returns before division when people is zero.

LECTURER DETAIL
TEACHING PURPOSE
Your turn

CONNECT
Build on the preceding slide: What the activity shows.

LECTURER CUE
Give silent thinking time, then let pairs discuss. Rotate who types. This is practice, not a graded quiz. Expected response: triple_value returns x * 3. The calls give 15 and None respectively. The guard returns before division when people is zero.

DISCUSSION KEY FOR THIS SLIDE
DISCUSS THE REASONING
Practice discussion
triple_value returns x * 3. The calls give 15 and None respectively. The guard returns before division when people is zero.
Which step produced this result? What changes if one input changes?
CML3112   Week 3   46
Let learners attempt first; use this to explain the reasoning, not just reveal the answer.

NEXT
Practice discussion. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Read the quantities before the formulas.

## Slide 45 — Read the quantities before the formulas

PURPOSE
Read the quantities before the formulas

CONNECT
Build on Revision example and answer. Explain why this example is needed before running it.

EXPLAIN
Mass measures matter in kilograms (kg). Weight is a force in newtons (N): mass × gravitational acceleration. The assignment uses g = 9.81 m/s².

Power is energy transferred per second, in watts (W). Efficiency in percent = 100 × useful output power / input power.

A named constant stores a value kept fixed in the calculation. Uppercase names such as G are a convention, not a Python restriction.

LECTURER DETAIL
TEACHING PURPOSE
Read the quantities before the formulas

CONNECT
Build on the preceding slide: Practice discussion.

EXPLAIN IN ORDINARY WORDS
Read each quantity and unit before using a formula. Python calculates numbers but does not enforce physical units. Parentheses specify which operation happens first.

CHECK AND EXPECTED ANSWER
What is 5 m times 3 m? 15 square metres. What is 7/2 in Python? 3.5; 7//2 is 3.

IF LEARNERS ARE STUCK
Write the formula and units on paper, substitute small values, then translate it to Python. Check zero denominators and the issued sign convention.

NEXT
Quantities and units. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Your programme formula.

## Slide 46 — Your programme formula

PURPOSE
Your programme formula

CONNECT
Build on Read the quantities before the formulas. Explain why this example is needed before running it.

EXPLAIN
Slab mass = area × thickness × density. Use metres and 2400 kg/m³ as specified.

LECTURER DETAIL
TEACHING PURPOSE
Your programme formula

CONNECT
Build on the preceding slide: Quantities and units.

EXPLAIN IN ORDINARY WORDS
Read each quantity and unit before using a formula. Python calculates numbers but does not enforce physical units. Parentheses specify which operation happens first.

CHECK AND EXPECTED ANSWER
What is 5 m times 3 m? 15 square metres. What is 7/2 in Python? 3.5; 7//2 is 3.

IF LEARNERS ARE STUCK
Write the formula and units on paper, substitute small values, then translate it to Python. Check zero denominators and the issued sign convention.

NEXT
Short explainer and discussion. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Preparing for the assignment.

## Slide 47 — Preparing for the assignment

PURPOSE
Preparing for the assignment

CONNECT
Build on Your programme formula. Explain why this example is needed before running it.

EXPLAIN
A3 has five named tasks, not five additional projects.

Read each public prompt and its exact output name.

Signed percentage error = 100 × (measured − expected) / expected.

Use a nonzero expected value.

LECTURER DETAIL
TEACHING PURPOSE
Preparing for the assignment

CONNECT
Build on the preceding slide: After the video.

LECTURER CUE
A3 has five named tasks, not five additional projects. Read each public prompt and its exact output name. Signed percentage error = 100 × (measured − expected) / expected. Use a nonzero expected value. For the cohort task: resistive loss = current² × resistance; slab mass = area × thickness × 2400; hydrostatic pressure in kPa = density × 9.81 × depth / 1000. The brief determines which formula you implement. q4 specifies the zero-input behaviour. q5 uses the supplied six readings; trace them on paper, and use your own percentage-error function. Loops are not required yet.

EXPLAIN IN ORDINARY WORDS
Signed percentage error compares a measurement with its expected reference: (measured - expected) / expected times 100. Positive means above the reference; negative means below it.

CHECK AND EXPECTED ANSWER
For measured 90 and expected 100, the signed error is -10%. Its size is 10%.

IF LEARNERS ARE STUCK
Calculate the difference first, divide by the reference, then multiply by 100. The formula needs a nonzero reference; follow the issued task contract for exceptional inputs.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
Preparing for the assignment continued. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Preparing for the assignment continued.

## Slide 48 — Preparing for the assignment continued

PURPOSE
Preparing for the assignment continued

CONNECT
Build on Preparing for the assignment. Explain why this example is needed before running it.

EXPLAIN
Use the formula for your programme shown earlier. q4 specifies the zero-input behaviour. q5 uses the supplied six readings; trace them on paper, and use your own percentage-error function.

Loops are not required yet.

LECTURER DETAIL
TEACHING PURPOSE
Preparing for the assignment continued

CONNECT
Build on the preceding slide: Preparing for the assignment.

LECTURER CUE
A3 has five named tasks, not five additional projects. Read each public prompt and its exact output name. Signed percentage error = 100 × (measured − expected) / expected. Use a nonzero expected value. For the cohort task: resistive loss = current² × resistance; slab mass = area × thickness × 2400; hydrostatic pressure in kPa = density × 9.81 × depth / 1000. The brief determines which formula you implement. q4 specifies the zero-input behaviour. q5 uses the supplied six readings; trace them on paper, and use your own percentage-error function. Loops are not required yet.

EXPLAIN IN ORDINARY WORDS
A loop repeats its indented instructions for each item. A running total must be initialised before the loop and updated inside it.

CHECK AND EXPECTED ANSWER
For values 2,4,6 and total initially 0, what are the successive totals? 2,6,12.

IF LEARNERS ARE STUCK
Use a trace table with current item and total. Resetting total inside the loop loses earlier additions.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
Units branches and error messages. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Unit conversions for the assignment.

## Slide 49 — Unit conversions for the assignment

PURPOSE
Unit conversions for the assignment

CONNECT
Build on Preparing for the assignment continued. Explain why this example is needed before running it.

EXPLAIN
Millimetres become metres by dividing by 1000: 200 mm is 0.2 m.

Percent becomes a fraction by dividing by 100: 75% is 0.75.

Only for rotational-speed questions: rpm means revolutions per minute. One revolution is 2π radians and one minute is 60 seconds, so multiply rpm by 2π/60.

LECTURER DETAIL
TEACHING PURPOSE
Units branches and error messages

CONNECT
Build on the preceding slide: Preparing for the assignment continued.

LECTURER CUE
Teach these concepts before the weekly quiz. Use changed numbers for practice. This slide supplies concepts, not the quiz key.

EXPLAIN IN ORDINARY WORDS
A condition is a True/False question. Python executes the matching indented branch. = assigns; == compares. >= includes the boundary, while > excludes it.

CHECK AND EXPECTED ANSWER
With value 30, is value >= 30 true? Yes. Is value > 30 true? No.

IF LEARNERS ARE STUCK
Try one value below, at and above the boundary before running the code.

NEXT
Units branches and error messages continued. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Your issued assignment.

## Slide 50 — Your issued assignment

PURPOSE
Your issued assignment

CONNECT
Build on Unit conversions for the assignment. Explain why this example is needed before running it.

EXPLAIN
Open W03_student.ipynb.

Read every task and its input units before coding.

Keep the required function names and returned outputs.

Run the supplied visible checks, then restart and run all.

LECTURER DETAIL
TEACHING PURPOSE
Your issued assignment

CONNECT
Build on the preceding slide: Units branches and error messages continued.

LECTURER CUE
# W03: variables and functions
CML3112. Complete each named output. Save as STUDENT_ID_W03.ipynb.
## q1: 3 marks
A 40 kg motor sits on a bench. Set weight_n to its weight in newtons, taking g = 9.81.
## q2: 4 marks
Write percent_error(measured, expected) returning the signed percent error.
## q3: 3 marks
Write slab_mass(area_m2, thickness_m) returning the mass of the concrete slab in kg, taking concrete as 2400 kg/m3.
## q4: 5 marks
Write efficiency(out_w, in_w) returning the percentage, and returning None when in_w is zero or negative.
## q5: 5 marks
READINGS is given in the notebook. Using your own percent_error against a nominal of 100, set worst_reading to the reading with the largest error by size, and worst_error to that reading's signed percent error.
You may compare these six readings directly; a loop is not required this week.
Restart and Run All, then save your named notebook. Practice check results are feedback; the submitted notebook is graded independently.

EXPLAIN IN ORDINARY WORDS
A function is a named set of instructions. def defines it; a call runs it with inputs. Parameters are input names, arguments are supplied values, and return sends the result back.

CHECK AND EXPECTED ANSWER
Does print(8) return the number 8 to the caller? No; it displays 8 and returns None. A function needing a numeric result should return it.

IF LEARNERS ARE STUCK
Trace one call: bind input names, run the indented body, reach return, then put the returned result back into the calling expression.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
q1: 3 marks. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
q1: 3 marks.

## Slide 51 — q1: 3 marks

PURPOSE
q1: 3 marks

CONNECT
Build on Your issued assignment. Explain why this example is needed before running it.

EXPLAIN
A 40 kg motor sits on a bench.

Set weight_n to its weight in newtons, taking g = 9.81.

LECTURER DETAIL
TEACHING PURPOSE
q1: 3 marks

CONNECT
Build on the preceding slide: Your issued assignment.

LECTURER CUE
Read the specific public requirement shown on this slide. Explain the input, output and evidence before independent work; do not work the assessed answer for the class.

EXPLAIN IN ORDINARY WORDS
Read each quantity and unit before using a formula. Python calculates numbers but does not enforce physical units. Parentheses specify which operation happens first.

CHECK AND EXPECTED ANSWER
What is 5 m times 3 m? 15 square metres. What is 7/2 in Python? 3.5; 7//2 is 3.

IF LEARNERS ARE STUCK
Write the formula and units on paper, substitute small values, then translate it to Python. Check zero denominators and the issued sign convention.

NEXT
q2: 4 marks. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
q2: 4 marks.

## Slide 52 — q2: 4 marks

PURPOSE
q2: 4 marks

CONNECT
Build on q1: 3 marks. Explain why this example is needed before running it.

EXPLAIN
Write percent_error(measured, expected) returning the signed percent error.

LECTURER DETAIL
TEACHING PURPOSE
q2: 4 marks

CONNECT
Build on the preceding slide: q1: 3 marks.

LECTURER CUE
Read the specific public requirement shown on this slide. Explain the input, output and evidence before independent work; do not work the assessed answer for the class.

EXPLAIN IN ORDINARY WORDS
Signed percentage error compares a measurement with its expected reference: (measured - expected) / expected times 100. Positive means above the reference; negative means below it.

CHECK AND EXPECTED ANSWER
For measured 90 and expected 100, the signed error is -10%. Its size is 10%.

IF LEARNERS ARE STUCK
Calculate the difference first, divide by the reference, then multiply by 100. The formula needs a nonzero reference; follow the issued task contract for exceptional inputs.

NEXT
q3: 3 marks. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
q3: 3 marks.

## Slide 53 — q3: 3 marks

PURPOSE
q3: 3 marks

CONNECT
Build on q2: 4 marks. Explain why this example is needed before running it.

EXPLAIN
Write slab_mass(area_m2, thickness_m) returning the mass of the concrete slab in kg, taking concrete as 2400 kg/m3.

LECTURER DETAIL
TEACHING PURPOSE
q3: 3 marks

CONNECT
Build on the preceding slide: q2: 4 marks.

LECTURER CUE
Read the specific public requirement shown on this slide. Explain the input, output and evidence before independent work; do not work the assessed answer for the class.

EXPLAIN IN ORDINARY WORDS
A function is a named set of instructions. def defines it; a call runs it with inputs. Parameters are input names, arguments are supplied values, and return sends the result back.

CHECK AND EXPECTED ANSWER
Does print(8) return the number 8 to the caller? No; it displays 8 and returns None. A function needing a numeric result should return it.

IF LEARNERS ARE STUCK
Trace one call: bind input names, run the indented body, reach return, then put the returned result back into the calling expression.

NEXT
q4: 5 marks. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
q4: 5 marks.

## Slide 54 — q4: 5 marks

PURPOSE
q4: 5 marks

CONNECT
Build on q3: 3 marks. Explain why this example is needed before running it.

EXPLAIN
Write efficiency(out_w, in_w) returning the percentage, and returning None when in_w is zero or negative.

LECTURER DETAIL
TEACHING PURPOSE
q4: 5 marks

CONNECT
Build on the preceding slide: q3: 3 marks.

LECTURER CUE
Read the specific public requirement shown on this slide. Explain the input, output and evidence before independent work; do not work the assessed answer for the class.

EXPLAIN IN ORDINARY WORDS
A function is a named set of instructions. def defines it; a call runs it with inputs. Parameters are input names, arguments are supplied values, and return sends the result back.

CHECK AND EXPECTED ANSWER
Does print(8) return the number 8 to the caller? No; it displays 8 and returns None. A function needing a numeric result should return it.

IF LEARNERS ARE STUCK
Trace one call: bind input names, run the indented body, reach return, then put the returned result back into the calling expression.

NEXT
q5: 5 marks. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
q5: 5 marks.

## Slide 55 — q5: 5 marks

PURPOSE
q5: 5 marks

CONNECT
Build on q4: 5 marks. Explain why this example is needed before running it.

EXPLAIN
READINGS is given in the notebook.

Using your own percent_error against a nominal of 100, set worst_reading to the reading with the largest error by size, and worst_error to that reading's signed percent error.

LECTURER DETAIL
TEACHING PURPOSE
q5: 5 marks

CONNECT
Build on the preceding slide: q4: 5 marks.

LECTURER CUE
Read the specific public requirement shown on this slide. Explain the input, output and evidence before independent work; do not work the assessed answer for the class.

EXPLAIN IN ORDINARY WORDS
Signed percentage error compares a measurement with its expected reference: (measured - expected) / expected times 100. Positive means above the reference; negative means below it.

CHECK AND EXPECTED ANSWER
For measured 90 and expected 100, the signed error is -10%. Its size is 10%.

IF LEARNERS ARE STUCK
Calculate the difference first, divide by the reference, then multiply by 100. The formula needs a nonzero reference; follow the issued task contract for exceptional inputs.

NEXT
Engineering functions submission. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Engineering functions submission.

## Slide 56 — Engineering functions submission

PURPOSE
Engineering functions submission

CONNECT
Build on q5: 5 marks. Explain why this example is needed before running it.

EXPLAIN
Opens: 22 Sep 2026, 10:55 Kampala

Deadline: 29 Sep 2026, 11:00 Kampala

Use your full Student Registration Number in the form.

Keep the submitted files and confirmation.

LECTURER DETAIL
TEACHING PURPOSE
Engineering functions submission

CONNECT
Build on the preceding slide: q5: 5 marks.

LECTURER CUE
The form link is cohort-specific. Recheck the live form and release status before class. These scheduled assignment dates are separate from the quiz activation window. The issued brief defines the required files, even if the form accepts additional formats. Source: data/submission_links.json

EXPLAIN IN ORDINARY WORDS
A function is a named set of instructions. def defines it; a call runs it with inputs. Parameters are input names, arguments are supplied values, and return sends the result back.

CHECK AND EXPECTED ANSWER
Does print(8) return the number 8 to the caller? No; it displays 8 and returns None. A function needing a numeric result should return it.

IF LEARNERS ARE STUCK
Trace one call: bind input names, run the indented body, reach return, then put the returned result back into the calling expression.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
Week 3 quiz. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Week 3 quiz.

## Slide 57 — Week 3 quiz

PURPOSE
Week 3 quiz

CONNECT
Build on Engineering functions submission. Explain why this example is needed before running it.

EXPLAIN
Answer individually after the lecturer activates the quiz.

Available for 24 hours from activation.

Use your Student Registration Number and registered account.

The lecturer will confirm the exact closing time.

LECTURER DETAIL
TEACHING PURPOSE
Week 3 quiz

CONNECT
Build on the preceding slide: Engineering functions submission.

LECTURER CUE
Activate the matching open_W3_CML3112 function in Quiz Controls, then confirm the 24-hour close time. Opening this slide or clicking its link does not activate the form. The 24 hours is the availability window. Keep existing quiz scoring and form rules. Do not show private answer keys.

QUIZ OPERATION
Opening the student link does not activate the quiz. In Quiz Controls run the matching open_W<week>_<cohort> function once when ready. Announce the logged closing time: 24 hours after activation. Five minutes describes expected answering time, not the availability window. Quiz 1 and Quiz 2 require separate activation when collecting catch-up work.

NEXT
Before you leave. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Before you leave.

## Slide 58 — Revision and submission checklist

PURPOSE
Revision and submission checklist

CONNECT
Build on Week 3 quiz. Explain why this example is needed before running it.

EXPLAIN
You can explain each input, the returned answer and its engineering unit.

Save your work and check the required submission files.

LECTURER DETAIL
TEACHING PURPOSE
Before you leave

CONNECT
Build on the preceding slide: Week 3 quiz.

LECTURER CUE
Ask every learner for an individual response. Record one misconception to revisit at the start of the next class. If a deadline changed, announce the exact Kampala date and update the source registry before rebuilding slides.

EXPLAIN IN ORDINARY WORDS
A function is a named set of instructions. def defines it; a call runs it with inputs. Parameters are input names, arguments are supplied values, and return sends the result back.

CHECK AND EXPECTED ANSWER
Does print(8) return the number 8 to the caller? No; it displays 8 and returns None. A function needing a numeric result should return it.

IF LEARNERS ARE STUCK
Trace one call: bind input names, run the indented body, reach return, then put the returned result back into the calling expression.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Optional revision video.

## Slide 59 — Optional revision video

PURPOSE
Optional revision video

CONNECT
Build on Revision and submission checklist. Explain why this example is needed before running it.

EXPLAIN
For revision after class.

Corey Schafer
Python Tutorial for Beginners 3: Integers and Floats

Opening 00:00–04:00, suggested four-minute excerpt; preview before class

Listening question: How are numbers written and how do arithmetic operators change them?

LECTURER DETAIL
TEACHING PURPOSE
Short explainer and discussion

CONNECT
Build on the preceding slide: Your programme formula.

LECTURER CUE
Title/channel and subject confirmed from the original YouTube listing. Exact excerpt content has not been fully watched; keep the local worked example as the fallback.
After viewing: Calculate 7 / 2 and 7 // 2 in Colab and explain the difference.
Preview before class and stop after the selected short excerpt. If playback fails, teach the worked example. Video is optional. Source: https://www.youtube.com/watch?v=khKv-8q7YmY

EXPLAIN IN ORDINARY WORDS
A list keeps items in order. Python positions start at zero. In [2,4,6], position 0 contains 2 and position 2 contains 6. A slice excludes its stop position.

CHECK AND EXPECTED ANSWER
What is [2,4,6][1]? 4. Is there a position 3? No.

IF LEARNERS ARE STUCK
Draw three numbered boxes starting at zero. Keep the position separate from the value stored in it.

VIDEO ROUTINE
Preview the exact link and stated excerpt before class. State the viewing question first, pause after the example, and ask a learner to explain it. If access fails, use the adjacent worked example and discussion rather than spend class time troubleshooting streaming.

NEXT
After the video. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
independent revision and the issued task.
