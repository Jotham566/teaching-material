# CML3111 Week03 Engineering

Private lecturer companion. These same notes are embedded in the PowerPoint. Use Presenter View; keep the student display on slides only.

## Slide 1 — Python calculations and reusable functions

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

## Slide 2 — Today’s learning

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

## Slide 3 — Recall and a first attempt

TEACHING PURPOSE
Recall and a first attempt

CONNECT
Build on the preceding slide: Today’s learning.

LECTURER CUE
Allow two minutes for everyone to try. Ask pairs to compare. If many cannot begin, show the first step and repeat with changed values. Checkpoint for today: Students explain the difference between defining and calling a function, and between return and print. Re-model with double_value if these are confused.

EXPLAIN IN ORDINARY WORDS
Name the positive class first. Actual is what happened; predicted is the model decision. Precision asks how many predicted positives were right. Recall asks how many actual positives were found.

CHECK AND EXPECTED ANSWER
With TP=2, FP=1, FN=2: precision=2/3 and recall=2/4. A missed actual positive is a false negative.

IF LEARNERS ARE STUCK
Draw actual/predicted headings. Place one case at a time before calculating a fraction. Explain the task rule for a zero denominator.

NEXT
The engineering context. Move on after a learner can explain the current example or required action.

## Slide 4 — The engineering context

TEACHING PURPOSE
The engineering context

CONNECT
Build on the preceding slide: Recall and a first attempt.

LECTURER CUE
A team records device temperature to investigate cooling. Use a communications cabinet, an electrical enclosure or a robot controller as the physical example. No specialist hardware knowledge is assumed.

EXPLAIN IN ORDINARY WORDS
A list keeps items in order. Python positions start at zero. In [2,4,6], position 0 contains 2 and position 2 contains 6. A slice excludes its stop position.

CHECK AND EXPECTED ANSWER
What is [2,4,6][1]? 4. Is there a position 3? No.

IF LEARNERS ARE STUCK
Draw three numbered boxes starting at zero. Keep the position separate from the value stored in it.

NEXT
Start with numbers and values. Move on after a learner can explain the current example or required action.

## Slide 5 — Start with numbers and values

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

## Slide 6 — Words we will use

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

## Slide 7 — A variable refers to its current value

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

## Slide 8 — Python values have types

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

## Slide 9 — Operator

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

## Slide 10 — Read a function call before using it

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

## Slide 11 — Reading Python symbols

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

## Slide 12 — Names, conversion and comments

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

## Slide 13 — Arithmetic that needs care

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

## Slide 14 — Read the quantities in your programme example

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
Voltage and current: Voltage describes electrical potential difference in volts (V). Current is the rate of charge flow in amperes (A). This example uses direct current (DC).
Power: Power is energy transferred each second, measured in watts (W). For this DC example, power = voltage × current. Resistive heating later uses current squared × resistance.

NEXT
A calculation for your programme. Move on after a learner can explain the current example or required action.

## Slide 15 — A calculation for your programme

TEACHING PURPOSE
A calculation for your programme

CONNECT
Build on the preceding slide: Read the quantities in your programme example.

LECTURER CUE
A DC test circuit has 12 volts and 2 amperes. Power = voltage × current = 24 watts. This example assumes DC; AC real power needs additional information.

NEXT
The calculation in Python. Move on after a learner can explain the current example or required action.

## Slide 16 — The calculation in Python

TEACHING PURPOSE
The calculation in Python

CONNECT
Build on the preceding slide: A calculation for your programme.

LECTURER CUE
Read each name and unit. = assigns the number, * multiplies and / divides. print displays the result. A DC test circuit has 12 volts and 2 amperes. Power = voltage × current = 24 watts. This example assumes DC; AC real power needs additional information.

Complete practice code:
voltage_v = 12
current_a = 2
power_w = voltage_v * current_a
print(power_w)

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

## Slide 17 — A change to predict

TEACHING PURPOSE
A change to predict

CONNECT
Build on the preceding slide: The calculation in Python.

LECTURER CUE
Expected practice answer: 36 watts

DISCUSSION KEY FOR THIS SLIDE
DISCUSS THE REASONING
The practice result
36 watts
Which step produced this result? What changes if one input changes?
CML3111   Week 3   18
Let learners attempt first; use this to explain the reasoning, not just reveal the answer.

NEXT
The practice result. Move on after a learner can explain the current example or required action.

## Slide 18 — The practice result

TEACHING PURPOSE
The practice result

CONNECT
Build on the preceding slide: A change to predict.

DELIVER THIS SLIDE
Read the stated purpose, then point to the named example or action on the slide. Ask learners to describe what they will do before moving on. For a break slide, announce the return time; for a section divider, name the next concrete task.

NEXT
Reading an error message. Move on after a learner can explain the current example or required action.

## Slide 19 — Reading an error message

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

## Slide 20 — Condition

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

## Slide 21 — Comparison and logic

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

## Slide 22 — A decision needs a colon and indentation

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

## Slide 23 — Function

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

## Slide 24 — Indentation and return

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

## Slide 25 — A function definition and a call

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

## Slide 26 — A calculation has inputs and an answer

TEACHING PURPOSE
A calculation has inputs and an answer

CONNECT
Build on the preceding slide: A function definition and a call.

LECTURER CUE
Work the cohort formula by hand before opening Python. State every unit. Use the four-line cohort calculation first; do not begin with formatting, imports or a long function.

EXPLAIN IN ORDINARY WORDS
Read each quantity and unit before using a formula. Python calculates numbers but does not enforce physical units. Parentheses specify which operation happens first.

CHECK AND EXPECTED ANSWER
What is 5 m times 3 m? 15 square metres. What is 7/2 in Python? 3.5; 7//2 is 3.

IF LEARNERS ARE STUCK
Write the formula and units on paper, substitute small values, then translate it to Python. Check zero denominators and the issued sign convention.

NEXT
A reusable calculation. Move on after a learner can explain the current example or required action.

## Slide 27 — A reusable calculation

TEACHING PURPOSE
A reusable calculation

CONNECT
Build on the preceding slide: A calculation has inputs and an answer.

LECTURER CUE
Introduce one reusable calculation using the example below. Read def, the function name, parentheses, parameter, colon, indentation and return separately. Defining the function does not run its body.

EXPLAIN IN ORDINARY WORDS
A function is a named set of instructions. def defines it; a call runs it with inputs. Parameters are input names, arguments are supplied values, and return sends the result back.

CHECK AND EXPECTED ANSWER
Does print(8) return the number 8 to the caller? No; it displays 8 and returns None. A function needing a numeric result should return it.

IF LEARNERS ARE STUCK
Trace one call: bind input names, run the indented body, reach return, then put the returned result back into the calling expression.

NEXT
Inputs, instructions and a returned result. Move on after a learner can explain the current example or required action.

## Slide 28 — Inputs, instructions and a returned result

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

## Slide 29 — Following a function call

TEACHING PURPOSE
Following a function call

CONNECT
Build on the preceding slide: Inputs, instructions and a returned result.

LECTURER CUE
Calling double_value(4) supplies 4 for x, calculates 8 and returns 8. The outer print displays it. Then teach an if/else guard with a separate small example.

EXPLAIN IN ORDINARY WORDS
A function is a named set of instructions. def defines it; a call runs it with inputs. Parameters are input names, arguments are supplied values, and return sends the result back.

CHECK AND EXPECTED ANSWER
Does print(8) return the number 8 to the caller? No; it displays 8 and returns None. A function needing a numeric result should return it.

IF LEARNERS ARE STUCK
Trace one call: bind input names, run the indented body, reach return, then put the returned result back into the calling expression.

NEXT
Worked example. Move on after a learner can explain the current example or required action.

## Slide 30 — Worked example

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

## Slide 31 — Worked example continued

TEACHING PURPOSE
Worked example continued

CONNECT
Build on the preceding slide: Worked example.

LECTURER CUE
Work the cohort formula by hand before opening Python. State every unit. Use the four-line cohort calculation first; do not begin with formatting, imports or a long function. Introduce one reusable calculation using the example below. Read def, the function name, parentheses, parameter, colon, indentation and return separately. Defining the function does not run its body. Calling double_value(4) supplies 4 for x, calculates 8 and returns 8. The outer print displays it. Then teach an if/else guard with a separate small example.

Complete practice code:
print(double_value(4))

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

WALK THROUGH THIS CODE
print displays a value below the cell.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Positional and named inputs. Move on after a learner can explain the current example or required action.

## Slide 32 — Positional and named inputs

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

## Slide 33 — Worked example continued

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

## Slide 34 — Worked example continued

TEACHING PURPOSE
Worked example continued

CONNECT
Build on the preceding slide: Worked example continued.

LECTURER CUE
Work the cohort formula by hand before opening Python. State every unit. Use the four-line cohort calculation first; do not begin with formatting, imports or a long function. Introduce one reusable calculation using the example below. Read def, the function name, parentheses, parameter, colon, indentation and return separately. Defining the function does not run its body. Calling double_value(4) supplies 4 for x, calculates 8 and returns 8. The outer print displays it. Then teach an if/else guard with a separate small example.

Complete practice code:
print(safe_share(12, 3))

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

WALK THROUGH THIS CODE
print displays a value below the cell.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Expected output. Move on after a learner can explain the current example or required action.

## Slide 35 — Expected output

TEACHING PURPOSE
Expected output

CONNECT
Build on the preceding slide: Worked example continued.

LECTURER CUE
Compare the actual output character by character with this practice result. If it differs, read the first error and check the input, units, names and execution order. Do not copy this practice output into a graded answer.

NEXT
A branch with a clear boundary. Move on after a learner can explain the current example or required action.

## Slide 36 — A branch with a clear boundary

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

## Slide 37 — A branch with a clear boundary in Python

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

## Slide 38 — Selecting a largest error without loops

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

## Slide 39 — Reading a short list

TEACHING PURPOSE
Reading a short list

CONNECT
Build on the preceding slide: Selecting a largest error without loops.

LECTURER CUE
Trace positions 0, 1 and 2. abs(-8) is 8. Use a new list for a prediction before running the example.

EXPLAIN IN ORDINARY WORDS
A list keeps items in order. Python positions start at zero. In [2,4,6], position 0 contains 2 and position 2 contains 6. A slice excludes its stop position.

CHECK AND EXPECTED ANSWER
What is [2,4,6][1]? 4. Is there a position 3? No.

IF LEARNERS ARE STUCK
Draw three numbered boxes starting at zero. Keep the position separate from the value stored in it.

READ THE VISUAL
Start with the title and labels. Read one row or mark aloud, including its unit. Let a learner read a second one before discussing the pattern. Do not infer a numerical value from an unlabelled drawing.

NEXT
Selecting a largest error without loops in Python. Move on after a learner can explain the current example or required action.

## Slide 40 — Selecting a largest error without loops in Python

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

## Slide 41 — Keep the reading beside its signed error

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

## Slide 42 — Find a position, then recover the original values

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

## Slide 43 — You are the function

TEACHING PURPOSE
You are the function

CONNECT
Build on the preceding slide: Find a position, then recover the original values.

LECTURER CUE
Do this before revealing the discussion slide. One learner moves or writes the items, the other checks. Swap roles. Every student explains one step. Expected: The returned answers are 8 and 14. The same instructions accept different inputs.
Wait for an individual prediction before inviting pair discussion. Give a first-step hint if needed.

EXPLAIN IN ORDINARY WORDS
A function is a named set of instructions. def defines it; a call runs it with inputs. Parameters are input names, arguments are supplied values, and return sends the result back.

CHECK AND EXPECTED ANSWER
Does print(8) return the number 8 to the caller? No; it displays 8 and returns None. A function needing a numeric result should return it.

IF LEARNERS ARE STUCK
Trace one call: bind input names, run the indented body, reach return, then put the returned result back into the calling expression.

NEXT
What the activity shows. Move on after a learner can explain the current example or required action.

## Slide 44 — What the activity shows

TEACHING PURPOSE
What the activity shows

CONNECT
Build on the preceding slide: You are the function.

LECTURER CUE
Ask which step produced this answer. Return to the concrete action if a learner cannot explain it. This is practice feedback, never a quiz key.

EXPLAIN IN ORDINARY WORDS
A function is a named set of instructions. def defines it; a call runs it with inputs. Parameters are input names, arguments are supplied values, and return sends the result back.

CHECK AND EXPECTED ANSWER
Does print(8) return the number 8 to the caller? No; it displays 8 and returns None. A function needing a numeric result should return it.

IF LEARNERS ARE STUCK
Trace one call: bind input names, run the indented body, reach return, then put the returned result back into the calling expression.

NEXT
Your turn. Move on after a learner can explain the current example or required action.

## Slide 45 — Your turn

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
CML3111   Week 3   46
Let learners attempt first; use this to explain the reasoning, not just reveal the answer.

NEXT
Practice discussion. Move on after a learner can explain the current example or required action.

## Slide 46 — Practice discussion

TEACHING PURPOSE
Practice discussion

CONNECT
Build on the preceding slide: Your turn.

LECTURER CUE
Ask how the result was obtained. Reteach the smallest missing step instead of giving a longer lecture.

EXPLAIN IN ORDINARY WORDS
A function is a named set of instructions. def defines it; a call runs it with inputs. Parameters are input names, arguments are supplied values, and return sends the result back.

CHECK AND EXPECTED ANSWER
Does print(8) return the number 8 to the caller? No; it displays 8 and returns None. A function needing a numeric result should return it.

IF LEARNERS ARE STUCK
Trace one call: bind input names, run the indented body, reach return, then put the returned result back into the calling expression.

NEXT
Read the quantities before the formulas. Move on after a learner can explain the current example or required action.

## Slide 47 — Read the quantities before the formulas

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

## Slide 48 — Quantities and units

TEACHING PURPOSE
Quantities and units

CONNECT
Build on the preceding slide: Read the quantities before the formulas.

EXPLAIN IN ORDINARY WORDS
Read each quantity and unit before using a formula. Python calculates numbers but does not enforce physical units. Parentheses specify which operation happens first.

CHECK AND EXPECTED ANSWER
What is 5 m times 3 m? 15 square metres. What is 7/2 in Python? 3.5; 7//2 is 3.

IF LEARNERS ARE STUCK
Write the formula and units on paper, substitute small values, then translate it to Python. Check zero denominators and the issued sign convention.

NEXT
Your programme formula. Move on after a learner can explain the current example or required action.

## Slide 49 — Your programme formula

TEACHING PURPOSE
Your programme formula

CONNECT
Build on the preceding slide: Quantities and units.

DELIVER THIS SLIDE
Read the stated purpose, then point to the named example or action on the slide. Ask learners to describe what they will do before moving on. For a break slide, announce the return time; for a section divider, name the next concrete task.

NEXT
Short explainer and discussion. Move on after a learner can explain the current example or required action.

## Slide 50 — Short explainer and discussion

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

## Slide 51 — After the video

TEACHING PURPOSE
After the video

CONNECT
Build on the preceding slide: Short explainer and discussion.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

NEXT
Preparing for the assignment. Move on after a learner can explain the current example or required action.

## Slide 52 — Preparing for the assignment

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

## Slide 53 — Preparing for the assignment continued

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

## Slide 54 — Units branches and error messages

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

## Slide 55 — Units branches and error messages continued

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

## Slide 56 — Units branches and error messages continued

TEACHING PURPOSE
Units branches and error messages continued

CONNECT
Build on the preceding slide: Units branches and error messages continued.

LECTURER CUE
Teach these concepts before the weekly quiz. Use changed numbers for practice. This slide supplies concepts, not the quiz key.

EXPLAIN IN ORDINARY WORDS
A condition is a True/False question. Python executes the matching indented branch. = assigns; == compares. >= includes the boundary, while > excludes it.

CHECK AND EXPECTED ANSWER
With value 30, is value >= 30 true? Yes. Is value > 30 true? No.

IF LEARNERS ARE STUCK
Try one value below, at and above the boundary before running the code.

NEXT
Your issued assignment. Move on after a learner can explain the current example or required action.

## Slide 57 — Your issued assignment

TEACHING PURPOSE
Your issued assignment

CONNECT
Build on the preceding slide: Units branches and error messages continued.

LECTURER CUE
# W03: variables and functions
CML3111. Complete each named output. Save as STUDENT_ID_W03.ipynb.
## q1: 3 marks
A 40 kg motor sits on a bench. Set weight_n to its weight in newtons, taking g = 9.81.
## q2: 4 marks
Write percent_error(measured, expected) returning the signed percent error.
## q3: 3 marks
Write power_loss(current, resistance) returning the power lost in watts (I squared R).
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

## Slide 58 — q1: 3 marks

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

## Slide 59 — q2: 4 marks

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

## Slide 60 — q3: 3 marks

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

## Slide 61 — q4: 5 marks

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

## Slide 62 — q5: 5 marks

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

## Slide 63 — Engineering functions submission

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

## Slide 64 — Week 3 quiz

TEACHING PURPOSE
Week 3 quiz

CONNECT
Build on the preceding slide: Engineering functions submission.

LECTURER CUE
Activate the matching open_W3_CML3111 function in Quiz Controls, then confirm the 24-hour close time. Opening this slide or clicking its link does not activate the form. The 24 hours is the availability window. Keep existing quiz scoring and form rules. Do not show private answer keys.

QUIZ OPERATION
Opening the student link does not activate the quiz. In Quiz Controls run the matching open_W<week>_<cohort> function once when ready. Announce the logged closing time: 24 hours after activation. Five minutes describes expected answering time, not the availability window. Quiz 1 and Quiz 2 require separate activation when collecting catch-up work.

NEXT
Before you leave. Move on after a learner can explain the current example or required action.

## Slide 65 — Before you leave

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

