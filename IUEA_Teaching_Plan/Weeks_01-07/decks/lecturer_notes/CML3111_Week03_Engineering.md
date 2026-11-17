# CML3111 Week 3

Each slide shows its text, then the spoken script the lecturer reads aloud.

## Slide 1: Python calculations and reusable functions

Communications, Electrical, Mechatronics and Robotics Engineering

Friday 25 September 2026
Friday 11:00–14:00, Room 115

**Spoken script**

Welcome to Week 3 of machine learning for Communications, Electrical, Mechatronics and Robotics Engineering. Today is Python calculations and reusable functions. We build calculations from numbers and symbols, then we make decisions, then we package a calculation as a function. Check the slide for the date, time and room of this session.

## Slide 2: Today’s learning

Read Python values and arithmetic symbols.

Define a function, call it and check its inputs.

You can explain each input, the returned answer and its engineering unit.

**Spoken script**

Today we learn to make Python do calculations for us, and then to package a calculation so we can reuse it.

First we read Python values and the symbols used for arithmetic. These are the plus and minus signs you already know, plus a few new ones. Then we write a function. A function is a small named piece of code that takes inputs, does a calculation and gives back an answer. We define it once, call it whenever we need it, and check that its inputs make sense.

At the end of the session you should be able to explain three things about any function we write. What goes in, what comes back, and what engineering unit the answer has. If a function returns a power, we say the answer is in watts. If it returns an area, we say square metres.

## Slide 3: How to read the examples

Code contains the instructions. Output shows the result.

Type the code shown in the example. Run it, then compare your output with the result below.

**Spoken script**

Every example in today's session follows the same pattern, so let us agree how to read it.

The code is the set of instructions. It is the only part you type into a Colab cell. The output is what Python shows after it runs those instructions. You never type the output. You use it to check yourself.

So the routine is simple. We type the code exactly as it appears on the slide. We run the cell. Then we compare what appeared under our cell with the result on the slide. If the two match, we move on. If they differ, we look for a small typing mistake, such as a missing bracket or a wrong capital letter.

We take one idea at a time, so each slide adds only a little to the last one.

## Slide 4: The engineering context

01

A team records device temperature to investigate cooling.

02

Use a communications cabinet, an electrical enclosure or a robot controller as the physical example.

03

No specialist hardware knowledge is assumed.

**Spoken script**

Every example today comes from a real engineering situation, so let us set the scene.

A team records the temperature of a device because they want to investigate cooling. Choose whichever physical example is closest to your own area. It might be a communications cabinet full of equipment, an electrical enclosure, or a robot controller. All of these produce heat, and engineers measure it to keep equipment safe.

For our purposes, the temperature is just a number that we read and store in Python. Then we write code that compares it with a limit and decides what to do.

You need no specialist hardware knowledge for this. If you can read a thermometer, you can follow the examples.

## Slide 5: Start with numbers and values

Number

A number expresses how much or how many: 3 items or 2.5 metres. Whole numbers count; decimal numbers can describe a part of a unit.

Value and unit

A value is one piece of information. The number 2.5 is a value. A measurement also needs a unit, such as metres. Python does not attach that unit automatically.

**Spoken script**

We begin with the most basic ingredient, the number.

A number tells us how much or how many. Three items is a count. Two point five metres is a length. Whole numbers are good for counting. Numbers with a decimal point can describe part of a unit, such as half a metre.

A value is one piece of information. The number two point five is a value. In engineering, a measurement needs more than a number. It also needs a unit, such as metres or volts. Three bolts and three metres both use the number three, but they describe very different things.

Python stores the number. It does not attach the unit for us. That is why we will often put the unit in the name we choose, for example length underscore m, so that whoever reads the code knows the answer is in metres.

## Slide 6: Words we will use

Variable

A name referring to a value. In length_m = 5, the right side is evaluated and assigned to length_m.

int, float, str, bool

int represents whole numbers; float represents approximate real numbers such as 2.5; str is text in quotes; bool is True or False.

**Spoken script**

Here are four words you will hear all day, so we define them now.

A variable is a name that refers to a value. Look at length underscore m equals five. Python works out the right side first, which is five, and then attaches the name length underscore m to it. The equals sign here means assign, or store. It is an instruction to Python.

Next, four types of value. An int is a whole number such as three. A float is a number with a decimal part such as two point five. We call it approximate because the computer stores many decimals with tiny rounding. A str, short for string, is text inside quotes. And a bool, short for Boolean, is one of two values, True or False.

Each type of value allows different operations. Keeping the type in mind will help us read errors later.

## Slide 7: A variable refers to its current value

After reassignment, thickness refers to 0.20.

**Spoken script**

A variable can be given a new value at any time, and it then refers to the newest one.

Think of a name tag. We first stick the tag thickness on one value. Later we run a new assignment that gives thickness a different value. The tag moves to the new value. Python does not keep a history of the old one under that name.

After the reassignment on this slide, thickness refers to zero point two zero. If we print thickness now, we see zero point two zero.

This is why the order of the lines in a cell matters. Python reads from the top down, and each assignment replaces the earlier one. When a result surprises us, a good first check is to ask which assignment ran most recently for that name.

## Slide 8: Python values have types

3.5 + 2 gives 5.5. "3.5" + "2" joins text into "3.52".

**Spoken script**

Every value in Python has a type. The type is the kind of information, and it decides which operations are allowed.

The table lists five. An int is a whole number, like three. A float is a decimal number, like three point five. A str is text in quotes, such as the characters three, point, five inside quotation marks. A bool is True or False. And None is a special value that means no value was supplied.

The example shows why this matters. Three point five plus two is a number sum, and it gives five point five. But if both are in quotes, they are text, and plus now joins the text. The text three point five joined with the text two gives three point five two.

So quotes change the type, and the type changes what plus does. When a result looks odd, check the type first.

## Slide 9: Operator

A symbol for an operation: + adds, - subtracts, * multiplies, / divides, ** raises to a power. // floors a quotient, so -5 // 2 is -3.

**Spoken script**

An operator is a symbol that tells Python which operation to carry out.

You already know most of them. Plus adds. Minus subtracts. The star, which we write with the asterisk key, multiplies. The forward slash divides. Two stars in a row raise to a power, so two star star three means two to the power three.

There is one more, written as two slashes together. It divides and then rounds the answer down to a whole number. The word for that is floor division. As an example, minus five floor divided by two gives minus three, because the exact answer is minus two point five and rounding down takes us to minus three.

We will practise each of these on small numbers on the next few slides, so you do not need to memorise them now.

## Slide 10: Read a function call before using it

A built-in function

Python already provides tools such as print, type and float. A function call asks a named tool to do its work: print(3) displays 3.

Parentheses, quotes and comments

Parentheses hold the inputs to a call. Quotes make text: "3.5" is text; float("3.5") converts it to a number. # starts a comment that Python does not run.

**Spoken script**

A function is a ready-made tool with a name. Python comes with many built in. Three we will use today are print, type and float.

To use a tool we call it. We write its name, then brackets, and inside the brackets we put the input. Print, bracket, three, bracket tells print to display the number three.

Quotes make text. So three point five inside quotes is text, and we cannot do arithmetic with it. If we call float on that text, float converts it into a real number.

Finally, the hash symbol starts a comment. Python ignores everything after the hash on that line. Comments are notes to the human reader, such as a reminder of what a line does.

Read a call from the name outwards. First the name of the tool, then what we handed to it.

## Slide 11: Reading Python symbols

01

= assigns a value to a name. == compares two values.

02

* multiplies. / divides. ** raises to a power.

03

Parentheses pass inputs when we call a function.

04

Indented lines belong to the block above them.

**Spoken script**

Before we write more code, we read four kinds of symbol so that none of them surprises us.

First, a single equals sign assigns a value to a name. Two equals signs in a row compare two values and ask whether they are the same. These are different jobs, and mixing them up is a common early error.

Second, the star multiplies, the slash divides, and two stars raise to a power.

Third, brackets after a name pass inputs to a function. When we write print, bracket, total, bracket, the word total is the input we hand to print.

Fourth, indentation. When a line starts a few spaces in from the left, Python treats it as belonging to the line above. We will see this soon with decisions and with functions.

Keep these four in mind as we go through the examples.

## Slide 12: Names, conversion and comments

float converts numeric text into a decimal number.

type reports the kind of value: for example, float.

print displays a value below the cell.

type(...) reports the kind of value. <class 'float'> means a floating-point number.

```python
length_m = float("3.5")  # text to number
width_m = 2
area_m2 = length_m * width_m
print(area_m2)
print(type(length_m))
```

**Spoken script**

Let us read this program one line at a time.

The first line takes the text three point five and passes it to float. Float converts that text into a number. We store the result under the name length underscore m. The hash and the words after it are a comment for the reader.

The second line stores the whole number two under the name width underscore m.

The third line multiplies length by width and stores the answer under area underscore m two. The name ends in m two to remind us the unit is square metres.

The fourth line prints the area. The fifth line asks Python for the type of length underscore m and prints it.

The output is seven point zero, because three point five times two is seven. The second output says class float, which means length underscore m is a floating point number. The word class is just how Python names a type.

## Slide 13: Week 3 continuation

From slides 1–12: values have types, variables name values, = assigns, and print displays a result. float("3.5") converts text to a number. We now use those ideas in calculations and functions.

Next: arithmetic, decisions, functions, then lists and the A3 brief.

**Spoken script**

Let us pause and collect what we have covered so far.

Values have types, so a whole number, a decimal and a piece of text behave differently. Variables are names that refer to values. A single equals sign assigns a value to a name. Print displays a result. And float of the text three point five converts text into a number we can calculate with.

From here we use those ideas in real calculations and in functions.

The plan for the rest of the session is as follows. First arithmetic in more depth. Then decisions, where the program chooses between paths. Then functions, which let us reuse a calculation. After that, lists, which hold several values together, and finally the brief for assignment A three. Check the slide for the details of what that brief asks.

## Slide 14: Reading a Python expression

01

An expression is code that produces a value. In 7 + 2, the inputs are 7 and 2; the operator + tells Python to add them.

02

A statement is an instruction. total = 7 + 2 calculates 9, then gives it the name total. print(total) displays the stored value.

03

Read each symbol before running. Code is what you type; output is what Python displays. Do not type the word “Output”.

**Spoken script**

Two words will help us describe code precisely. Expression and statement.

An expression is a piece of code that produces a value. Take seven plus two. The inputs are seven and two, and the plus sign tells Python to add them. The whole thing produces nine.

A statement is a complete instruction. Total equals seven plus two is a statement. Python works out the expression on the right, which is nine, and then gives it the name total. After that, print of total displays the stored value, nine.

So the order is always the same. Calculate first, store second, display only if we ask for it with print.

When you run examples, read each symbol before you press run. Remember the code is what you type. The output is what Python displays. Please do not type the word output into your cell.

## Slide 15: Addition subtraction multiplication and division

Python uses * for multiplication, not ×. / can produce a fractional result.

**Spoken script**

Now we look at the four basic operations in Python, and the slide gives a small table of each.

Seven plus two gives nine. Seven minus two gives five. Seven times two gives fourteen. Seven divided by two gives three point five.

Two points about the keyboard. The multiplication sign you write by hand, the little cross, does not exist in Python. We use the star key, the asterisk, instead. If you type the letter x, Python will report an error.

The second point is division. The slash gives a fractional result when the numbers do not divide evenly. Seven divided by two gives three point five. Even when they do divide evenly, such as eight divided by two, Python returns four point zero, a float.

In the next example we will run all four and check each answer.

## Slide 16: Run the four arithmetic operations

Each print call displays one calculated result.

The numbers have no units until we assign a meaning to them.

Output: 9; 5; 14; 3.5

```python
print(7 + 2)
print(7 - 2)
print(7 * 2)
print(7 / 2)
```

**Spoken script**

Let us run the four operations. We type four print lines, one for each calculation.

The first prints seven plus two. The second prints seven minus two. The third prints seven times two, using the star. The fourth prints seven divided by two, using the slash.

Each print call displays one result on its own line. So we expect nine, then five, then fourteen, and finally three point five.

Notice that among these four lines only the division gave a decimal. Adding, subtracting and multiplying whole numbers gives whole numbers. Division can give a fraction.

Also notice that these are bare numbers. They have no units yet. A seven could be seven metres, seven volts or seven bolts. The meaning comes from what we decide the numbers stand for, and we will put that meaning into our variable names soon.

## Slide 17: Floor division remainder and powers

7 contains three groups of 2 with 1 left over: 7 = 3 × 2 + 1.

**Spoken script**

Three more operators complete the arithmetic set. Floor division, remainder and power.

Think about seven sweets shared into groups of two. We can make three full groups, and one sweet is left over. In arithmetic we write that as seven equals three times two plus one.

Floor division, written with two slashes, gives the number of full groups. So seven floor divided by two is three.

Remainder, written with the percent sign, gives what is left over. So seven percent two is one.

Power, written with two stars, repeats multiplication. Two star star three means two times two times two, which is eight.

The table on the slide shows exactly these three examples with their answers. In the next slides we look more closely at how each one behaves.

## Slide 18: Reading powers signs and remainders

01

2 ** 3 means 2 × 2 × 2. It does not mean 2 × 3. The left value is the base; the right value is the exponent.

02

A leading minus makes a number negative: -7. Floor division rounds the quotient down: -7 / 2 is -3.5, so -7 // 2 is -4.

03

% is remainder, not percentage. To turn 75% into a fraction, calculate 75 / 100. Do not divide by zero.

**Spoken script**

Three details need care.

First, powers. Two star star three means two times two times two. The left number is the base, and the right number is the exponent, which says how many times to multiply the base. The answer is eight.

Second, negative numbers. A leading minus sign makes a number negative, like minus seven. Floor division rounds the exact answer down, towards the smaller number. Minus seven divided by two is minus three point five. Rounding down gives minus four, so minus seven floor divided by two is minus four. Down on the number line means towards the more negative side.

Third, the percent sign. In Python it is the remainder operator. If we want seventy five percent as a fraction, we calculate seventy five divided by one hundred.

And one last rule. Never divide by zero. Python stops with an error.

## Slide 19: Run floor division remainder and powers

** repeats multiplication.

A negative floor result rounds toward the smaller integer.

Output: 3; 1; 8; -4; 0.75

```python
print(7 // 2)
print(7 % 2)
print(2 ** 3)
print(-7 // 2)
print(75 / 100)
```

**Spoken script**

Let us run five print lines and predict each answer before we look.

The first is seven floor divided by two. Seven holds three full twos, so the answer is three.

The second is seven percent two, the remainder. After taking three twos, one is left over. The answer is one.

The third is two star star three. That is two times two times two, which is eight.

The fourth is minus seven floor divided by two. The exact answer is minus three point five. Floor division rounds down to the smaller whole number, which is minus four.

The fifth is seventy five divided by one hundred. This is how we turn seventy five percent into a fraction. The answer is zero point seven five.

If your cell shows the same five outputs in the same order, the operators are working as expected.

## Slide 20: Which operation happens first

01

Parentheses group a calculation: do (2 + 3) before multiplying it by 4.

02

Powers come before multiplication and division. Multiplication, /, // and % come before addition and subtraction. Equal-level * and / run left to right.

03

Use parentheses when the intended grouping might be unclear. For a negative base, write (-2) ** 2. This gives 4; -(2 ** 2) gives -4.

**Spoken script**

When one line contains several operations, Python needs a rule for which one to do first. The rule is the same order you may remember from school mathematics.

Brackets come first. Anything inside brackets is calculated before the rest. So for two plus three, in brackets, times four, we first get five and then multiply by four.

Next come powers. After that, multiplication, division, floor division and remainder. After those, addition and subtraction. When two operations are at the same level, such as a star and a slash, Python works from left to right.

When the grouping might be unclear to a reader, add brackets. They cost nothing and make the intention obvious.

One special case concerns negative numbers. Writing bracket minus two bracket star star two gives four, because we square the negative number. Writing minus, bracket, two star star two, bracket gives minus four, because we square two first and then apply the minus.

## Slide 21: Trace an expression before its output

Changing parentheses can change the answer even when the numbers stay the same.

**Spoken script**

To trace an expression means to work through it step by step, writing down what happens, before we look at the final answer.

The table has three rows. In the first, two plus three times four. Multiplication comes before addition, so we do three times four first, which gives twelve. Then two plus twelve gives fourteen.

In the second row, the numbers are the same, but we put brackets around two plus three. Now the addition goes first and gives five. Five times four is twenty.

In the third row, twelve divided by three times two. The slash and the star are at the same level, so we go left to right. Twelve divided by three gives four point zero. Then four point zero times two gives eight point zero.

So the brackets changed the answer from fourteen to twenty, even though the numbers stayed the same.

## Slide 22: Check operation order

Read the calculation from the trace table.

Run first; then compare with the shown outputs.

Output: 14; 20; 8.0

```python
print(2 + 3 * 4)
print((2 + 3) * 4)
print(12 / 3 * 2)
```

**Spoken script**

Let us check the order of operations by running three print lines. Before we run, read the trace table from the previous slide and predict each answer.

The first line is two plus three times four. We expect the multiplication first, which gives fourteen.

The second line is two plus three in brackets, times four. We expect the bracket first, which gives twenty.

The third line is twelve divided by three, times two. We go left to right, so we expect eight point zero. Notice the decimal point. It appears because the slash always returns a float.

Run the cell first, and then compare your output with the three values on the slide. If one of them differs, go back to the trace table and find which step you did in a different order from Python.

## Slide 23: Assigning and updating a named value

01

count = 2 gives the name count the value 2. = means assignment; it does not ask whether two values are equal.

02

count = count + 1 first reads the old value 2, calculates 3, then assigns 3 back to count.

03

After the update, print(count) displays 3. Re-running only the update cell changes count again; restart and run from the beginning for the shown result.

**Spoken script**

Here is a pattern you will use constantly, updating a value.

Count equals two gives the name count the value two. Remember, the equals sign means assign.

Now the update, count equals count plus one. This looks odd in mathematics, because no number equals itself plus one. In Python it is an instruction. Python first reads the old value of count, which is two. It calculates two plus one, which is three. Then it assigns three back to count.

After that, print of count displays three.

A warning about notebooks. If you run only the update cell again, count becomes four, then five. The numbers on the slide assume we run from the top. If your result looks different, restart the notebook and run all cells in order from the beginning.

## Slide 24: Trace one update

The right side is calculated before the left side changes.

Output: 2; 3

```python
count = 2
print(count)
count = count + 1
print(count)
```

**Spoken script**

We trace the update line by line.

The first line sets count to two. The second line prints count, so we see two.

The third line is the update. Python looks at the right side first, count plus one. At this moment count is two, so the right side is three. Only then does Python change the name on the left, so count now refers to three.

The fourth line prints count again, and this time we see three.

So the output is two, then three. The same name, count, shows two values at different times, because we replaced the value in between.

The rule to remember is that the right side is calculated completely before the left side changes.

## Slide 25: Numbers text and conversion

01

7 is an integer. 7.0 is a decimal-valued float. "7" is text because it is inside quotes. Both single and double quotes can enclose text.

02

"7" + "2" joins text into "72". To add those digits as numbers, convert each first: int("7") + int("2") gives 9.

03

int converts valid integer text; float converts valid decimal text. str turns a value into text. print displays a value; type reports its Python type.

**Spoken script**

Python can tell the difference between numbers and text, and we need to as well.

Seven with no quotes is an integer. Seven point zero is a float, a decimal number. Seven inside quotes is text, because quotes always make text. Either single or double quotes work.

Now what does plus do? On text, it joins. The text seven plus the text two gives the text seventy two. To add the digits as numbers, we convert each first. Int of the text seven plus int of the text two gives nine.

There are three conversion tools. Int converts text holding a whole number. Float converts text holding a decimal number. Str turns any value into text.

And two tools for checking. Print displays a value, and type tells us what type a value has. When an answer looks wrong, we can use type to see whether we have text or a number.

## Slide 26: Compare numeric addition with text joining

Quotes change the type and therefore what + does.

Conversion happens before the addition.

Output: 9; 72; 9; 2.5

```python
print(7 + 2)
print("7" + "2")
print(int("7") + int("2"))
print(float("2.5"))
```

**Spoken script**

Let us run four lines that show the difference between numbers and text.

The first prints seven plus two, both numbers. We expect nine.

The second prints the text seven plus the text two. Because of the quotes, plus joins them, and we see seventy two.

The third converts each piece to an integer first, using int, and then adds. Conversion happens before the addition, so we get nine again.

The fourth calls float on the text two point five, which gives the number two point five.

So the four outputs are nine, seventy two, nine, and two point five.

The quotes are what change the type, and the type decides what plus does. When we read data from a file or a keyboard, it often arrives as text. We convert it before we calculate.

## Slide 27: Arithmetic that needs care

01

Parentheses run first: (2 + 4) / 2 is 3.0. Without them, division runs before addition: 2 + 4 / 2 is 4.0.

02

/ gives a quotient. // rounds that quotient down: 7 // 2 is 3 and -7 // 2 is -4.

03

Many decimal fractions are approximate in a computer. A tolerance is an allowed difference, for example 0.01 m when checking two calculated lengths.

**Spoken script**

Three situations call for extra care.

First, brackets. Two plus four, in brackets, divided by two gives three point zero, since we add first. Without brackets, division goes before addition. Four divided by two is two, and two plus two gives four point zero.

Second, the slash against the double slash. The slash gives the exact quotient. The double slash rounds that quotient down. Seven floor divided by two is three. Minus seven floor divided by two is minus four, because we round down on the number line.

Third, decimals. Many decimal fractions cannot be stored exactly by a computer, so a result can differ from the textbook answer by a tiny amount. So when we compare calculated decimals, we accept a small allowed difference. That allowed difference is called a tolerance. For example, we might accept two calculated lengths as equal if they are within zero point zero one metres.

## Slide 28: Read the quantities in your programme example

Voltage and current

Voltage describes electrical potential difference in volts (V). Current is the rate of charge flow in amperes (A). This example uses direct current (DC).

Power

Power is energy transferred each second, measured in watts (W). For this DC example, power = voltage × current. Resistive heating later uses current squared × resistance.

**Spoken script**

Before we calculate, we define the quantities in our programme example. We first say what each quantity describes, and then we multiply.

Voltage is the electrical potential difference, the push that drives charge around a circuit. We measure it in volts, written capital V.

Current is the rate at which charge flows. We measure it in amperes, written capital A. This example uses direct current, or DC, where the current flows steadily in one direction.

Power is the energy transferred each second. We measure it in watts, written capital W. For this DC example, power equals voltage times current.

Later we will meet resistive heating, which uses current squared times resistance. That is a different calculation with different inputs, so keep the two apart.

## Slide 29: A calculation for your programme

01

A DC test circuit has 12 volts and 2 amperes.

02

Power = voltage × current = 24 watts.

03

This example assumes DC; AC real power needs additional information.

**Spoken script**

Here is the calculation we will turn into Python.

A DC test circuit has twelve volts and two amperes. Power equals voltage times current. So twelve times two gives twenty four, and the unit is watts.

Say it with units, and the formula checks itself. Volts times amperes gives watts.

One condition goes with this. The example assumes direct current. With alternating current, real power needs additional information, so this simple multiplication would not be enough there.

On the next slide we write exactly this calculation in Python, using names that carry the unit.

## Slide 30: The calculation in Python

print displays a value below the cell.

= assigns the value on the right to the name on the left.

Read top to bottom. Run the complete example in the matching practice notebook.

```python
voltage_v = 12
current_a = 2
power_w = voltage_v * current_a
print(power_w)
```

**Spoken script**

Now we write the power calculation in Python and read it line by line.

The first line stores twelve under the name voltage underscore v. The v at the end reminds us the unit is volts. The second line stores two under current underscore a, where a stands for amperes.

The third line multiplies the two names and stores the answer under power underscore w, for watts. The fourth line prints power underscore w. Print displays the result below the cell.

Read the cell from the top down. The equals sign assigns the value on the right to the name on the left. When you are ready, run the complete example in the matching practice notebook.

The output is twenty four, which matches our hand calculation of twelve volts times two amperes.

## Slide 31: Reading an error message

The last line names the error. The indicated line shows where Python noticed it.

**Spoken script**

Errors are normal, and Python tells us what went wrong if we read the message.

The last line of an error message names the kind of error. The line above it shows where Python noticed the problem.

The table lists four common ones. A NameError means a name is not available. First check the spelling, and check that you ran the cell that creates it. A TypeError means a wrong kind of value, for example adding text to a number. Check text versus number. A SyntaxError means Python cannot read a line. Check quotes, brackets and colons. An IndentationError means the spacing at the start of a line is invalid. Use consistent spaces.

The routine is to read the last line, look at the indicated line, compare what you expected with what is there, and fix the first problem. Then run again.

Sometimes the code runs with no error and still gives a wrong answer. Checking against a hand calculation catches those.

## Slide 32: A comparison produces a Boolean value

01

A comparison asks a yes/no question about values. Its Python result is True or False, written with capital first letters and no quotes.

02

30 >= 30 asks “Is 30 at least 30?” The answer is True. 28 >= 30 gives False.

03

True and False have type bool. "False" is text, not the Boolean value False. Conditions use Boolean results to choose what happens next.

**Spoken script**

Next we teach the program to ask questions.

A comparison asks a yes or no question about values. The answer is always one of two values, True or False. In Python we write them with a capital first letter and no quotes.

Take thirty greater than or equal to thirty. In words, is thirty at least thirty? Yes, so the result is True. Now twenty eight greater than or equal to thirty. Is twenty eight at least thirty? No, so the result is False.

True and False have the type bool. Writing False inside quotes gives text, which is a different thing. Python will not treat that text as the Boolean value.

Why does this matter? Because soon we will use these answers to decide what the program does next. A condition is simply a comparison whose True or False answer chooses a path.

## Slide 33: Equality and difference

= assigns a value. == compares values. They have different jobs.

**Spoken script**

We now meet two comparison symbols for same and different.

Two equals signs in a row ask whether two values are equal. Three equals three gives True, because they are the same.

An exclamation mark followed by an equals sign asks whether two values are different. Three not equal four gives True, because three and four differ.

Now the key point. A single equals sign assigns a value to a name. It stores something. Two equals signs compare two values. They ask a question and give back True or False. These are different jobs.

If you write one equals sign inside a condition, Python reports an error. The usual fix is to type the second equals sign.

## Slide 34: Comparing sizes and boundaries

The = part of >= and <= includes the boundary value.

**Spoken script**

Four more comparison symbols let us compare sizes.

Greater than asks whether the left value is larger. Three greater than three is False, because they are equal.

Greater than or equal asks whether the left value is larger or the same. Three greater than or equal to three is True.

Less than asks whether the left value is smaller. Two less than three is True.

Less than or equal asks whether the left is smaller or the same. Three less than or equal to three is True.

The extra equals sign in the longer symbols is what includes the boundary value. This is a deliberate choice that engineers make. If a limit is thirty, we must decide whether thirty itself is allowed. That decision is the difference between the short symbol and the long one.

## Slide 35: Display comparison results

Each comparison produces a Boolean.

No branch has run yet; print only displays the answers.

Output: True; False; False; True; False; True

```python
reading = 30
print(reading == 30)
print(reading != 30)
print(reading > 30)
print(reading >= 30)
print(reading < 30)
print(reading <= 30)
```

**Spoken script**

We set reading to thirty and print six comparisons. Let us go through them in order.

Reading equals thirty is True, since they are the same. Reading not equal to thirty is False, since they are not different. Reading greater than thirty is False, since thirty is not larger than itself. Reading greater than or equal to thirty is True. Reading less than thirty is False. Reading less than or equal to thirty is True.

So the output reads True, False, False, True, False, True.

Look at how the boundary behaves. Exactly at thirty, the symbols with an equals part give True and the strict ones give False.

No decision has been made yet. Print simply shows us the answers. In the next slides we will use these answers to choose which code runs.

## Slide 36: A condition and an if block

01

A condition is the question tested by an if statement. if reading >= 30: checks whether reading is at least 30.

02

The colon ends the header. The next line starts with four spaces; those spaces place it inside the block controlled by if.

03

If the condition is True, run the block. If it is False, skip it. The next line without those four spaces is outside the block and runs afterwards.

**Spoken script**

Now we let a comparison control the program. We do this with an if statement.

A condition is the question that if tests. In if reading greater than or equal to thirty, followed by a colon, the condition checks whether reading is at least thirty.

The colon ends that header line. The next line starts with four spaces. Those spaces place it inside the block that if controls.

If the condition is True, Python runs the indented block. If the condition is False, Python skips it.

A line that starts back at the left margin, without the four spaces, is outside the block. It runs afterwards, whichever way the condition went.

So indentation is part of the program. Four spaces mean this line belongs to the if. No spaces mean it comes after the decision.

## Slide 37: An if statement without else

28 >= 30 is False, so the indented print is skipped.

The final print is outside the block.

Output: check finished

```python
reading = 28
if reading >= 30:
    print("warm")
print("check finished")
```

**Spoken script**

Let us trace this program. It has four lines.

The first sets reading to twenty eight. The second line is the if header, asking whether reading is greater than or equal to thirty. The third line, indented by four spaces, prints the word warm. The fourth line, back at the left margin, prints check finished.

Python tests the condition. Twenty eight at least thirty is False. So the indented print of warm is skipped.

Then Python moves on to the last line. It has no indentation, so it is outside the block and always runs.

The output is just one line, check finished.

If we changed reading to thirty, the condition would be True. We would see warm first and then check finished.

## Slide 38: Trace both paths through if

Only the indented line is conditional. The outside line runs on either path.

**Spoken script**

The table checks the program for three values of reading.

When reading is twenty eight, the condition is False. The block is skipped. The only displayed line is check finished.

When reading is thirty, the condition is True. The indented line runs, so we see warm, and then check finished.

When reading is thirty one, the condition is again True, so the output is again warm and then check finished.

Only the indented line is conditional. The line outside the block runs on either path.

It is good practice to test a decision at three places: just below the boundary, exactly on it, and just above it. Those three tests catch most mistakes in comparison symbols.

## Slide 39: else gives the other path

01

else means “otherwise”. It has a colon but no extra condition. Align else with its matching if.

02

The if block runs when its condition is True. The else block runs when that same condition is False. Only one of these blocks runs.

03

Both branch bodies are indented by four spaces. Returning to the left margin ends the whole decision.

**Spoken script**

Sometimes we want something to happen when the condition is False as well. For that we add else.

Else means otherwise. It has a colon, and it has no condition of its own. It simply covers the case where the if condition was False.

We line up else with its matching if, at the same position from the left. Both the if block and the else block are indented four spaces.

The rule is that the if block runs when its condition is True, and the else block runs when that same condition is False. Exactly one of the two blocks runs. Exactly one block runs.

When we return to the left margin, the whole decision has ended. Code from there on runs every time.

Else always belongs to an if directly above it.

## Slide 40: A decision needs a colon and indentation

if tests a condition. The chosen indented block runs.

print displays a value below the cell.

= assigns the value on the right to the name on the left.

>= compares values. Only the chosen indented block runs.

```python
temperature = 28
if temperature >= 30:
    print("warm")
else:
    print("below 30")
```

**Spoken script**

Here is a full decision. We read it line by line.

Temperature equals twenty eight stores the value. Then if temperature greater than or equal to thirty, with a colon at the end. The line under it, indented four spaces, prints warm. Then else, with a colon, lined up with the if. Under it, indented again, print below thirty.

The if line tests the condition. Python then runs one of the indented blocks. The equals sign in the first line assigns. The greater than or equal symbol compares.

For twenty eight, the condition is False, so Python skips the warm block and runs the else block. The output is below thirty.

If we changed the temperature to thirty, the condition would be True, and we would see warm.

Colons and indentation are required. Leave one out, and Python reports an error.

## Slide 41: Trace both paths through if else

Re-run the complete previous example for each value. Exactly one branch prints.

**Spoken script**

Let us trace the if else program for three temperatures. To do it, we run the full previous example again for each value.

At twenty eight, the condition twenty eight at least thirty is False. The else block runs, and the output is below thirty.

At thirty, the condition is True. The if block runs, and the output is warm.

At thirty one, the condition is True, so the output is warm again.

In every row, exactly one branch prints. We never see both messages, and we never see neither.

Whatever the input, the program takes one clear path. When you write your own decisions, use a table like this one to check them before you trust them.

## Slide 42: More than two branches

if tests the first condition. elif means “otherwise, if” and tests another condition only if the earlier one was false. else handles the remaining case.

Python runs only the first matching branch. Put a narrower condition before a broader one that would also match. A colon and indentation mark each body.

**Spoken script**

Many decisions have more than two outcomes. For these we add elif, which is short for else if.

Python first tests the if condition. If that is False, it moves down to the elif and tests the next condition. This test only happens because the earlier one failed. Finally else handles whatever remains, with no test of its own.

The key rule is that Python runs only the first branch that matches. Once one condition is True, the rest are skipped.

Because of this, the order matters. We put the narrower condition first. Suppose we are classifying a level as high at ten or more, and medium at five or more. If we tested at least five first, a level of twelve would be called medium, because twelve is at least five. So test the high level first.

Each branch needs a colon and indented body, as before.

## Slide 43: Tracing an if elif else chain

elif is checked only after the earlier condition fails.

Output: medium. The first condition is false; the second is true.

```python
level = 7
if level >= 10:
    print("high")
elif level >= 5:
    print("medium")
else:
    print("low")
```

**Spoken script**

We read this chain from the top down.

Level is set to seven. The first test asks whether level is at least ten. Seven is below ten, so that is False and Python skips the print of high.

Next the elif asks whether level is at least five. Seven is at least five, so this is True. Python runs the block under it and prints medium.

The else is never reached, because a branch already matched.

So the output is medium.

Try other values in your head. A level of ten makes the first test True, so it prints high immediately. A level of three fails both tests and falls to else, which prints low.

One chain gives one output. Two separate if statements could both run, but an if elif else chain runs only one branch.

## Slide 44: Trace the if elif else chain

Python stops at the first True branch. else runs when neither test passes.

**Spoken script**

The table traces the chain for three levels. For each, we list the tests in the order Python makes them.

For level seven, the first test, seven at least ten, is False. The second test, seven at least five, is True. The output is medium.

For level ten, the first test, ten at least ten, is True. Python stops testing at once. The output is high.

For level three, the first test is False. The second test, three at least five, is also False. Neither test passed, so else runs. The output is low.

The rule is that Python stops at the first True branch. The else branch runs only when no test passes.

This is a good template for checking your own chains. Choose one value that lands in each branch and write down the tests in order.

## Slide 45: Combining and reversing conditions

01

and asks for both conditions to be True. or asks for at least one to be True. not reverses a Boolean answer.

02

Use parentheses to make each comparison readable: (reading >= 20) and (reading <= 30). This is an inclusive range check.

03

For these lessons we combine comparisons, so their results are Boolean. Python also permits other operand types; those are not needed for the shown checks.

**Spoken script**

Sometimes one comparison is not enough, so we combine them with three words.

And asks for both conditions to be True. Or asks for at least one to be True. Not reverses a Boolean answer, so True becomes False and False becomes True.

Take a range check. Reading at least twenty, in brackets, and reading at most thirty, in brackets. Both must hold. This checks that reading is inside the range from twenty to thirty, with both ends included. With reading equal to twenty five, both comparisons are True, so the whole is True.

The brackets keep each comparison easy to read.

For these lessons we combine comparisons, so each piece gives True or False. Python allows other kinds of values with these words, but we do not need that for the checks we write.

When someone says between twenty and thirty, always ask whether twenty and thirty themselves count, and then test those two values.

## Slide 46: and and or with Boolean inputs

not True gives False; not False gives True.

**Spoken script**

This slide is a reminder of three small words that combine True and False answers. A True or False value is called a Boolean. The word and gives True only when both sides are True. The word or gives True when at least one side is True. The word not flips a value to its opposite.

The slide shows the last one. Not True gives False, and not False gives True.

Think of a gate that opens only for staff who carry a badge and wear a helmet. With and, you need both. With or, either one is enough. With not, we ask for the opposite of the test.

In the next slide we use these three words to check whether a sensor reading sits inside a permitted range.

## Slide 47: Check a permitted range

Both range comparisons are True.

The outside-range comparisons are both False.

Output: True; False; False

```python
reading = 25
inside = (reading >= 20) and (reading <= 30)
print(inside)
print((reading < 20) or (reading > 30))
print(not inside)
```

**Spoken script**

We check whether a sensor reading is inside a permitted range. The first line stores the number twenty-five in the name reading.

The second line asks two questions and joins them with and. Is reading greater than or equal to twenty? Is reading less than or equal to thirty? Both answers are True for twenty-five, so inside becomes True. The signs greater than or equal to and less than or equal to include the boundary values twenty and thirty themselves.

The third line prints inside, which shows True. The fourth line prints the outside check. It asks whether reading is below twenty or above thirty. Twenty-five is neither, so both questions are False, and or gives False.

The fifth line prints not inside. Inside is True, so not inside is False.

The output is True, then False, then False. Python works out each comparison first and then combines the answers.

## Slide 48: Why a zero check comes first

01

Python evaluates and from left to right. When the first Boolean comparison is False, it does not need to evaluate the second.

02

For a simple zero guard, use if denominator == 0: before the division and return or handle that case explicitly.

03

A guard checks an input before a calculation. The function example below uses def and return.

**Spoken script**

Here we look at why a zero check comes first, before a division. Dividing by zero has no answer, and Python stops with an error called ZeroDivisionError.

The first card says Python reads an and test from left to right. If the first part is False, the whole test must be False, so Python skips the second part.

The second card gives the simple remedy. Before the division, write if denominator equals equals zero, with a colon. The double equals sign asks a question. Inside that if, we return or handle that case clearly.

The third card names this idea. A guard is a check on an input that runs before the calculation. Guarding means the dangerous step never sees a bad value.

On the next slides we write a real function with a guard, using def and return.

## Slide 49: Function

A named, reusable calculation or procedure. def introduces its definition. Parameters are the names for its inputs; arguments are the values supplied when calling it.

**Spoken script**

A function is a calculation that we save under a name so we can use it again and again. Think of a recipe card. You write it once, and every time someone brings ingredients, you follow the same steps.

The word def starts the definition. It is short for define. After def we write the function name, then brackets that hold the inputs.

The names inside those brackets are called parameters. They are placeholders waiting for values. The actual values we supply when we use the function are called arguments.

So a parameter is the empty label, and an argument is what we put into it on a given day. If a function has a parameter called x and we call it with the number four, then x holds four for that run.

Writing the definition alone shows nothing on the screen. The steps run when we call the function.

## Slide 50: Indentation and return

Spaces at the start of a line group the function body. return hands a result to the calling code. print displays a value and returns None.

**Spoken script**

Two ideas matter in this slide. The first is indentation. Indentation means leaving spaces at the start of a line. Every line that is indented under the def line belongs to the function body. The first line that returns to the left edge is outside the function.

The second idea is return. The word return hands a result back to the line of code that called the function. That line can then store the result in a name or use it in a further calculation.

The word print is different. Print shows a value on the screen so that we can read it. Print itself gives back None, which means no value.

Suppose a function prints eight but never returns it. We would see eight on the screen, yet a name that stored the call would hold None. If we want to use the answer later, we use return.

## Slide 51: A function definition and a call

01

def gives a reusable calculation a name and inputs.

02

Defining a function remembers the instructions.

03

Calling the function runs those instructions with values.

04

return sends the result back to the caller.

**Spoken script**

We build the idea of a function in four steps. The first card says def gives a reusable calculation a name and a list of inputs. We write the name once and use it many times.

The second card says that defining a function only remembers the instructions. Python stores them and does nothing else yet. No answer appears at this point.

The third card says that calling the function runs those instructions with real values. We write the function name followed by brackets holding the values.

The fourth card says return sends the result back to the place that made the call.

A good picture is a calculator button that you program yourself. You decide what it is called and what it needs. Then you press it with different numbers whenever you wish. On the next slide we see this with a very small function that doubles a number.

## Slide 52: Inputs, instructions and a returned result

The illustration uses slab_volume: length × width × thickness. The next function uses the same input/body/return pattern.

**Spoken script**

This diagram shows the shape of every function we write. Inputs go in, instructions work on them, and a result comes out.

The picture uses a worked example, slab volume. Its volume is length times width times thickness. The three inputs are length, width and thickness. The instruction is to multiply them together. The returned result is the volume.

The next function we meet is much smaller, but it follows the same pattern. It has an input, a body and a return. When you meet any new function in this course, ask three questions. What goes in? What does the body do with it? What comes back out? Those three questions let you read a function you have never seen before.

## Slide 53: Defining and calling double_value

def names the function. Inputs go inside parentheses.

return sends the result back to the caller.

Output: 8. Calling passes 4 to x; return sends 8 back; print displays it.

```python
def double_value(x):
    return x * 2

answer = double_value(4)
print(answer)
```

**Spoken script**

Let us read this function line by line. The first line is def double underscore value, then x in brackets, then a colon. The def says we are defining a function. The name is double underscore value. The x is the parameter, a placeholder for the number we will give it.

The second line is indented. It says return x times two. The star sign means multiply. So the function takes x, multiplies it by two and hands the answer back.

The third line is outside the function. It writes answer equals double underscore value of four. This is the call. The number four goes into x, the body works out eight, and return sends eight back. The name answer then holds eight.

The last line prints answer, and the output on the slide is eight. Defining the function showed nothing. The print line is what displays the result.

## Slide 54: Trace one function call

return sends a value back to the caller. print displays it. These are different actions.

**Spoken script**

We now trace one function call slowly. Follow the number four through the code.

First we call the function with four. Python gives four to the parameter x. Next the body runs and works out x times two, which is eight. Then return sends eight back to the line that made the call. That line stores eight in the name answer. Finally print shows what answer holds.

The sentence on the slide explains the key difference. Return sends a value back to the caller so that the program can keep using it. Print displays it for a person to read.

These are separate actions. A function can return a value and show nothing. It can also print a value and give nothing back to the caller. Ask yourself which one the task needs.

## Slide 55: Passing inputs by position or by name

01

In def rectangle_area(length, width):, length and width are parameter names. A call supplies an argument value for each.

02

rectangle_area(3, 2) binds 3 to length and 2 to width by position. rectangle_area(width=2, length=3) binds them by name.

03

The = inside a named argument labels an input for the call. Both calls run the same function body with the same two values.

**Spoken script**

Here we see two ways to supply inputs to a function. Suppose we define rectangle underscore area with two parameters, length and width. Parameters are the names in the definition. A call supplies an argument value for each name.

The first way is by position. In rectangle underscore area of three, two, the first value goes to the first parameter, so length is three. The second value goes to the second parameter, so width is two.

The second way is by name. In rectangle underscore area of width equals two, length equals three, we say directly which parameter receives each value. The order then makes no difference.

The equals sign inside the brackets is a label for an input in this call.

Both calls run the same body with the same two values, so they give the same answer.

## Slide 56: Positional and named inputs

def names the function. Inputs go inside parentheses.

return sends the result back to the caller.

print displays a value below the cell.

Both calls supply the same inputs. return makes the result reusable.

```python
def rectangle_area(length, width):
    return length * width

print(rectangle_area(3, 2))
print(rectangle_area(width=2, length=3))
```

**Spoken script**

Let us read the code. The first line defines a function called rectangle underscore area with two parameters, length and width. The second line is indented and says return length times width. The star means multiply, and return sends the product back.

The third line prints a call by position. We write rectangle underscore area of three, two. Three goes to length and two goes to width. The product is six, and print displays six below the cell.

The fourth line prints a call by name. We write width equals two, length equals three. The values are given in the other order, but each lands in the parameter we named. The product is again six.

Both calls supply the same inputs, so they give the same result. Because the function uses return, we could also store that result and use it in another calculation.

## Slide 57: None means there is no result value

01

None is a Python value used here to mean “no calculated answer”. It is not zero, an empty string, or the word "None".

02

A function returns None explicitly with return None. A function also returns None if it reaches its end without a return value.

03

A caller must handle None before trying arithmetic with the result. The next example returns it for division by zero.

**Spoken script**

This slide introduces a special Python value called None. None means there is no result value. We use it when a function has no calculated answer to give.

The first card clears up what None is. It is a value of its own. It is different from zero, because zero is a number and a real answer. It is different from an empty piece of text. And it is different from the word None written in quotation marks.

The second card says how a function gives None. We can write return None. A function also gives None when it reaches its end without any return value.

The third card gives a warning. Before doing arithmetic on a result, check whether it is None. The next example returns None when someone tries to divide by zero.

## Slide 58: An input check before division

Division by zero raises ZeroDivisionError. We choose to return None when people is zero, so there is no calculated share.

The check belongs inside the function, before the division. return ends that call immediately. A valid input follows the later return line.

**Spoken script**

We now build an input check before a division. In Python, dividing by zero raises an error called ZeroDivisionError, and the program stops. We choose a safer plan. When the number of people is zero, the function returns None, meaning there is no calculated share.

The check belongs inside the function and must come before the division. Python reads the lines from top to bottom. If people equals zero, the function reaches return None. Return ends that call at once, so the division line below never runs.

If people is any other value, the if test fails and Python skips its block. Python then arrives at the later return line, which does the division and sends back the share.

So the function protects itself. Anyone who calls it with a bad input gets a clear None and no crash.

## Slide 59: A function with a zero-input check

def names the function. Inputs go inside parentheses.

if tests a condition. The chosen indented block runs.

return sends the result back to the caller.

Output: 4.0. safe_share(12, 0) returns None before any division.

```python
def safe_share(total, people):
    if people == 0:
        return None
    return total / people

print(safe_share(12, 3))
```

**Spoken script**

Let us read this function, safe underscore share. It has two parameters, total and people.

The first line is def, the name, and the two parameters. The second line is if people equals equals zero, followed by a colon. The double equals sign asks whether people is zero. If the answer is True, Python runs the indented line below it.

That indented line is return None. It ends the call straight away and gives back None.

The last line of the function is return total divided by people. The slash means divide. Python reaches it only when people is a nonzero value.

The final line of the cell prints safe underscore share of twelve, three. Twelve divided by three is four, and Python shows it as four point zero because a slash division gives a decimal number. If we called it with twelve and zero, the guard would return None before any division.

## Slide 60: Trace the division guard

return ends this function call immediately. Later lines inside it do not run.

**Spoken script**

We now trace the division guard with two calls. The sentence on the slide gives the main rule. Return ends the function call immediately, and later lines inside it do not run.

First call, safe underscore share of twelve, three. Python checks whether people equals zero. Three is nonzero, so the guard does not fire. Python carries on to the last line, divides twelve by three and returns four point zero.

Second call, safe underscore share of twelve, zero. Python checks the guard. People is zero, so it returns None. At that point the call is finished. The division line is never reached, so no error occurs.

Trace code in this way whenever a function behaves in a surprising manner. Pick one input, move down the lines in order, and mark the return line that ends the call.

## Slide 61: A branch with a clear boundary

01

Read from the top. >= includes the boundary.

02

Only the selected branch runs.

03

Try the value exactly at 10 as well as 9 and 11.

**Spoken script**

This slide is about a branch with a clear boundary. A branch is a point where the program chooses between two paths, using if.

The first card says to read from the top. The test is value greater than or equal to ten. The sign greater than or equal to includes the boundary, so a value of exactly ten counts as high.

The second card says only the selected branch runs. If the test is True, the function returns high and the call ends. If it is False, Python skips that block and reaches the next return, which gives low.

The third card gives a habit for testing. Try the value exactly at ten as well as nine and eleven. Nine is just below the boundary, ten sits on it and eleven is just above it. The boundary value is where mistakes usually hide. We would expect low, high and high.

## Slide 62: A branch with a clear boundary in Python

def names the function. Inputs go inside parentheses.

if tests a condition. The chosen indented block runs.

return sends the result back to the caller.

Read top to bottom. Run the complete example in the matching practice notebook.

```python
def check_level(value):
    if value >= 10:
        return "high"
    return "low"

print(check_level(10))
print(check_level(9))
```

**Spoken script**

Let us read this function, check underscore level. It has one parameter called value.

The first line defines the function. The second line is the test, if value is greater than or equal to ten, followed by a colon. The indented line under it says return the text high. The text sits in quotation marks because it is words and a number would need no quotation marks.

The next line is back at the same level as the if. It says return low. Python reaches it only when the if test was False, because a return inside the if ends the call at once.

The last two lines print the results of two calls. Check level of ten meets the boundary, so it prints high. Check level of nine is below ten, so it prints low.

Read the code from top to bottom, then run the complete example in the matching practice notebook.

## Slide 63: One value and a collection of values

A variable can refer to one value: reading = 98. A collection stores several related values under one name.

Python has several collection types. Choose one according to how you need to find, change or organise its contents.

**Spoken script**

So far a name such as reading has held one value. For example, reading equals ninety-eight stores a single number.

Real engineering work often has many related values. A day of sensor readings, a list of student marks or a set of coordinates are examples. A collection stores several related values under one name, so we do not need a separate name for each.

Python has several kinds of collection. The second card says we choose one according to how we need to find, change or organise the contents. Some are found by position. Some are found by a label. Some are used to ask whether something is present.

Over the next slides we study the list in detail, because it is the most common. Then we meet the dictionary, the tuple and the set, and see what each is good for.

## Slide 64: Lists dictionaries tuples and sets

List and tuple positions start at zero. Dictionaries use keys. Sets have no positional index.

**Spoken script**

This slide gives a quick rule for how we find items in each collection.

A list is a row of items. Each item has a position number, and counting starts at zero. A tuple works the same way for positions. So the first item sits at position zero, the second at position one, and so on.

A dictionary uses keys. A key is a label that we choose, such as the text reading, and we use the label to find the value stored under it.

A set has no positions at all. It holds distinct items, and it is used to ask whether something is in it.

Starting at zero feels strange at first. Think of a floor number in a building where the ground floor is zero. The first floor you climb to is floor one, and the pattern follows from there.

## Slide 65: A list stores values in positions

01

readings = [98, 105, 92] creates a list. Square brackets enclose the items; commas separate them.

02

An index is an item’s position. Python starts counting at zero: readings[0] is 98, readings[1] is 105, readings[2] is 92.

03

Three items have positions 0, 1 and 2. readings[3] raises IndexError because there is no fourth item.

**Spoken script**

A list stores values in positions. We create one with square brackets. The first card shows readings equals square bracket ninety-eight, one hundred and five, ninety-two, closing bracket. The square brackets enclose the items, and commas separate them.

The second card introduces the index, which is the position of an item. Python starts counting at zero. So readings with zero in square brackets gives ninety-eight. Readings with one gives one hundred and five. Readings with two gives ninety-two.

The third card follows from this. Three items have positions zero, one and two. If we ask for readings with three in square brackets, Python finds no fourth item and raises an error called IndexError.

When you meet an IndexError, check the number inside the square brackets against the length of the list. The last position is always one less than the number of items.

## Slide 66: Count items before choosing a position

01

len(readings) is a built-in function call that returns how many items the list contains. len([98, 105, 92]) is 3.

02

A count and an index are different: the count is 3, while the valid positions are 0, 1 and 2.

03

print(readings) displays the whole list. print(readings[0]) displays only the value at its first position.

**Spoken script**

We now count the items in a list. The built-in function len returns how many items a list holds. Built-in means Python already provides it. Len of the list ninety-eight, one hundred and five, ninety-two is three.

The second card separates two ideas that students often mix up. The count is how many items there are, which is three here. The positions are labels for where each item sits, which are zero, one and two. The largest valid position is one smaller than the count.

The third card compares two print lines. Print of readings shows the whole list with its brackets. Print of readings with zero in square brackets shows only the single value stored at the first position, which is ninety-eight.

Before choosing a position, count the items first. That keeps us from asking for a position that does not exist.

## Slide 67: Creating and reading a list

[ ] creates a list or selects a position.

len counts the items; it is a built-in function.

Output: [98, 105, 92], then 98, then 3.

```python
readings = [98, 105, 92]
print(readings)
print(readings[0])
print(len(readings))
```

**Spoken script**

Let us read the code line by line. The first line creates a list called readings holding ninety-eight, one hundred and five and ninety-two. Square brackets make the list.

The second line prints readings. Python shows the entire list, with its brackets and commas.

The third line prints readings with zero in square brackets. Here the square brackets select a position. Position zero holds ninety-eight, so that is what appears.

The fourth line prints len of readings. Len is a built-in function that counts the items. It gives three.

So the output is the whole list, then ninety-eight, then three. Notice that square brackets do two jobs in this code. When they follow an equals sign and hold items, they create a list. When they follow a list name and hold a number, they select a position.

## Slide 68: Choosing the right collection

01

A dictionary connects a key to a value: {"reading": 98}. The colon connects them; record["reading"] finds the value by its key.

02

A tuple such as (2, 3) stores ordered items whose positions cannot be reassigned. A set such as {"A", "B"} stores distinct items without positions.

03

We use a list for today’s readings because their order matters. Week 4 develops dictionary, tuple and set operations before we use them with records.

**Spoken script**

This slide shows how to choose the right collection. We meet three more types, and Week 4 develops them in detail.

The first card describes the dictionary. It connects a key to a value, for example curly brackets with the text reading, a colon and ninety-eight. The colon joins the key to its value. To find the value we write record with the key in square brackets.

The second card describes the tuple and the set. A tuple such as two, three in round brackets stores ordered items, and the items cannot be replaced once the tuple is made. A set such as the letters A and B in curly brackets stores distinct items and has no positions.

The third card tells us what we use today. We use a list for the readings, because their order matters. Week 4 develops dictionary, tuple and set operations before we use them with records. For now, focus on lists.

## Slide 69: A method belongs to a value

01

A function is called by name: len(readings). A method is called through a value with a dot: readings.index(105).

02

index searches a list for a value and returns its first position. Here readings.index(105) returns 1. A missing value raises ValueError.

03

The parentheses contain inputs to the operation. The square brackets in readings[1] select an item; they do a different job.

**Spoken script**

We have met functions such as len. A function is called by writing its name and putting the value inside the brackets, as in len of readings.

A method is a related idea. A method belongs to a value and is called through that value with a dot. For example readings dot index of one hundred and five. We read it as readings, dot, index, then one hundred and five in brackets.

The second card explains what index does. It searches the list for a value and returns its first position. Here it returns one, because one hundred and five sits at position one. If the value is missing, Python raises a ValueError.

The third card separates two uses of symbols. The brackets after a method hold inputs to the operation. Square brackets, as in readings with one, select an item. They do different jobs, so read each one in context.

## Slide 70: Selecting a largest error without loops

01

An error is measured − expected. Its sign shows the direction. abs gives its magnitude: abs(-8) is 8.

02

max finds the largest supplied value: max(2, 5, 8) is 8. Compare magnitudes when the task asks for the largest error by size.

03

Keep the original signed error as well, because the magnitude alone loses direction.

**Spoken script**

We now find the largest error without using loops. First we define an error. Here it is measured minus expected. The sign shows the direction. A negative error means the measured value is below the expected one.

The built-in function abs gives the magnitude, which is the size of a number with its sign removed. Abs of minus eight is eight.

The second card introduces max. Max finds the largest of the values we supply. Max of two, five, eight is eight. When a task asks for the largest error by size, we compare the magnitudes, so we take abs first and then max.

The third card gives a warning. Keep the original signed error as well. A size of eight alone does not tell us whether the reading was too high or too low, and the direction often matters when we report the result.

## Slide 71: Selecting a largest error without loops in Python

print displays a value below the cell.

Read top to bottom. Run the complete example in the matching practice notebook.

```python
errors = [-2, 5, -8]
largest = max(abs(errors[0]), abs(errors[1]), abs(errors[2]))
print(largest)
```

**Spoken script**

Let us read this code. The first line creates a list called errors holding minus two, five and minus eight.

The second line builds one long expression. Abs of errors with zero in square brackets takes the first error and removes its sign, giving two. Abs of errors with one gives five. Abs of errors with two gives eight. Max then picks the largest of those three sizes, and the name largest stores it.

Working from the inside out helps here. Python first selects the item, then applies abs, then max.

The last line prints largest, and we expect eight. We wrote one abs for each position, so no loop was needed. The result tells us the biggest size of error, but it has lost the sign, which is why the next slides keep the original values too.

## Slide 72: Keep the reading beside its signed error

These paired lists use the same positions: the first error belongs to the first reading. The sign tells the direction; abs gives only the size.

index(value) finds the first position containing that value. Use that position in the original lists. An exact tie selects the first here; follow the issued task’s rule.

**Spoken script**

When we find the largest error, we usually also want the reading that caused it. The slide describes two paired lists, readings and errors. They line up by position. The first error belongs to the first reading, the second error to the second reading, and so on.

The first card reminds us that the sign shows direction, while abs gives only the size.

The second card gives the method. We make a list of sizes in the same order. We find the largest size with max. Then index of that value gives its position. We use that same position in the original lists to recover the reading and its signed error.

If two sizes tie exactly, index returns the first one it finds. Here we follow that rule, but when the issued task states a different rule, we follow the task.

## Slide 73: Find a position, then recover the original values

print displays a value below the cell.

Expected: 92 -8. The largest size is 8; the signed error is -8.

```python
readings = [98, 105, 92]
errors = [-2, 5, -8]
sizes = [abs(errors[0]), abs(errors[1]), abs(errors[2])]
position = sizes.index(max(sizes))
print(readings[position], errors[position])
```

**Spoken script**

Let us read this code carefully. The first two lines create two lists. Readings holds ninety-eight, one hundred and five, ninety-two. Errors holds minus two, five, minus eight. They line up by position.

The third line builds a list called sizes. Each item is abs of an item in errors, so sizes is two, five, eight.

The fourth line finds the position. Max of sizes is eight. Then sizes dot index of that value returns the position where eight sits, which is two. The name position stores two.

The last line prints readings at position and errors at position. Position is two, so we get ninety-two from readings and minus eight from errors.

The expected output is ninety-two, minus eight. The largest size is eight, and the signed error is minus eight, so the reading was below the reference.

## Slide 74: Revision example and answer

Example: Write triple_value(x). Predict triple_value(5). Then predict safe_share(12, 0).

Answer: triple_value returns x * 3. The calls give 15 and None respectively. The guard returns before division when people is zero.

**Spoken script**

This slide is a short revision question. Try it by yourself before we go through the answer.

The example has three parts. First, write a function called triple underscore value with parameter x. Second, predict what triple underscore value of five gives. Third, predict what safe underscore share of twelve, zero gives.

Here is the reasoning. Triple underscore value returns x times three, so the first call sends back fifteen. For safe underscore share of twelve, zero, the guard checks whether people equals zero. It does, so the function returns None before it ever divides.

The answers are fifteen and None. If you got the second one wrong, trace the call line by line and find the return that ends it. Tracing is the habit that settles most questions in this week's work.

## Slide 75: Read the quantities before the formulas

01

Mass measures matter in kilograms (kg). Weight is a force in newtons (N): mass × gravitational acceleration. The assignment uses g = 9.81 m/s².

02

Power is energy transferred per second, in watts (W). Efficiency in percent = 100 × useful output power / input power.

03

A named constant stores a value kept fixed in the calculation. Uppercase names such as G are a convention, not a Python restriction.

**Spoken script**

Before we use formulas, we make sure we know what each quantity means and what unit it carries.

The first card covers mass and weight. Mass measures how much matter an object has, in kilograms. Weight is a force, in newtons. We find it as mass times gravitational acceleration. The assignment uses g equals nine point eight one metres per second squared.

The second card covers power and efficiency. Power is the energy transferred each second, in watts. Efficiency in percent equals one hundred times useful output power divided by input power.

The third card introduces a named constant. A named constant is a name that holds a value we keep fixed during the calculation. By convention we write such names in capital letters, so G for gravity. That is a habit among programmers, and Python does not force it.

Always write down the unit of each value before you substitute numbers.

## Slide 76: Your programme formula

Resistive power loss (W) = current (A) squared × resistance (ohms).

In Python, current ** 2 means current multiplied by itself.

**Spoken script**

This slide gives the formula for your programme. For electrical, mechatronics and communications engineering, it is resistive power loss.

Resistive power loss in watts equals the current in amperes, squared, times the resistance in ohms. Current is how much electric charge flows each second. Resistance is how strongly a part opposes that flow. When current flows through a resistance, some power is lost as heat.

The second card shows the Python form. Current followed by two stars and the number two means current multiplied by itself. So current star star two times resistance gives the power lost.

Say the current is three amperes and the resistance is two ohms. Three times three is nine, and nine times two is eighteen watts. The current is squared first, and then multiplied by resistance.

## Slide 77: Preparing for the assignment

01

A3 has five named tasks, not five additional projects.

02

Read each public prompt and its exact output name.

03

Signed percentage error = 100 × (measured − expected) / expected.

04

Use a nonzero expected value.

**Spoken script**

Here we prepare for the assignment. The first card tells us the assignment has five named tasks, and they all sit in one notebook. All five tasks are parts of one notebook.

The second card says to read each public prompt carefully and note its exact output name. Your code must use that name, because the checker looks for it.

The third card gives a formula we need. Signed percentage error equals one hundred times measured minus expected, divided by expected. The word signed means we keep the plus or minus sign, which shows the direction of the error.

The fourth card gives a safety rule. Use a nonzero expected value, because dividing by zero has no answer.

Next we look at the rest of the preparation.

## Slide 78: Preparing for the assignment continued

01

Use the formula for your programme shown earlier. q4 specifies the zero-input behaviour. q5 uses the supplied six readings; trace them on paper, and use your own percentage-error function.

02

Loops are not required yet.

**Spoken script**

We continue preparing for the assignment. The first card has three parts.

First, use the formula for your own programme, which we saw earlier on the slide called your programme formula. Second, question four states what the function should do when its input is zero. Follow that rule exactly. Third, question five uses the six supplied readings. Trace them on paper first, so you know what answer to expect. Then use your own percentage-error function from question two.

The second card says loops are not required yet. A loop repeats steps for each item in a list, and we meet loops later. For now we write out the steps one by one, as in the examples from this lesson.

Doing the arithmetic by hand first gives you a check on your code.

## Slide 79: Unit conversions for the assignment

01

Millimetres become metres by dividing by 1000: 200 mm is 0.2 m.

02

Percent becomes a fraction by dividing by 100: 75% is 0.75.

03

Only for rotational-speed questions: rpm means revolutions per minute. One revolution is 2π radians and one minute is 60 seconds, so multiply rpm by 2π/60.

**Spoken script**

Some assignment tasks need unit conversions, so let us practise three.

The first card is millimetres to metres. We divide by one thousand. Two hundred millimetres becomes zero point two metres.

The second card is percent to a fraction. We divide by one hundred. Seventy-five percent becomes zero point seven five.

The third card applies only to rotational-speed questions. The unit rpm means revolutions per minute. One revolution is two pi radians, and one minute is sixty seconds. So to change rpm into radians per second, we multiply by two pi over sixty.

Conversions are a common source of lost marks. Before you multiply or divide, write down the unit you have and the unit you need. Then choose the factor that moves you from one to the other.

## Slide 80: Your issued assignment

01

Open W03_student.ipynb.

02

Read every task and its input units before coding.

03

Keep the required function names and returned outputs.

04

Restart and run all cells, then save the completed notebook.

**Spoken script**

This slide explains how to work on your issued assignment. Follow the four cards in order.

First, open the notebook called W zero three underscore student dot i p y n b. That is your starting file.

Second, read every task and the units of its inputs before you start to code. A value in millimetres and a value in metres need different handling.

Third, keep the required function names and the returned outputs exactly as they are given. The checker looks for those names, so changing one can cost you marks.

Fourth, restart and run all cells, then save the completed notebook. Restarting clears old values from memory, and running everything from the top confirms that your notebook works from start to finish. Then save it before you submit.

## Slide 81: q1: 3 marks

A 40 kg motor sits on a bench.

Set weight_n to its weight in newtons, taking g = 9.81.

Keep the exact names and outputs. Check types, units and the issued brief.

**Spoken script**

Question one is worth three marks. A forty kilogram motor sits on a bench. We must set a name called weight underscore n to its weight in newtons.

Recall that weight is a force, found as mass times g. The slide tells us to take g equals nine point eight one. So weight underscore n is forty times nine point eight one.

This question asks for a value, so there is no function to write. Use the exact name weight underscore n, written in small letters with the underscore.

The last line of the slide is a reminder. Keep the exact names and outputs. Check types, units and the issued brief. Types means whether you have a number or text. The unit here is newtons, and the answer should be a plain number.

## Slide 82: q2: 4 marks

Write percent_error(measured, expected) returning the signed percent error.

Keep the exact names and outputs. Check types, units and the issued brief.

**Spoken script**

Question two is worth four marks. We write a function called percent underscore error with two parameters, measured and expected. It must return the signed percent error.

This is the formula from the preparation slide. Take measured minus expected, divide by expected, and multiply by one hundred. Signed means we keep the sign, so a measured value below the expected one gives a negative answer.

The word return is important. The function must hand the answer back to the caller, because question five uses this function again.

Keep the function name and the two parameter names exactly as written on the slide. Then check the issued brief in the notebook for any detail not shown here.

## Slide 83: q3: 3 marks

Write power_loss(current, resistance) returning the power lost in watts (I squared R).

Keep the exact names and outputs. Check types, units and the issued brief.

**Spoken script**

Question three is worth three marks. We write a function called power underscore loss with two parameters, current and resistance.

It must return the power lost in watts. The slide gives the formula as I squared R. I is the current in amperes, and R is the resistance in ohms. So the function squares the current, multiplies by the resistance, and returns the result.

In Python, current star star two squares the current. Then we multiply by resistance and return the answer.

The word return is important. The function hands the number back, so other code can use it. Keep the exact function name and the parameter names shown on the slide, and check that your inputs are in amperes and ohms.

## Slide 84: q4: 5 marks

Write efficiency(out_w, in_w) returning the percentage, and returning None when in_w is zero or negative.

Keep the exact names and outputs. Check types, units and the issued brief.

**Spoken script**

Question four is worth five marks. We write a function called efficiency with two parameters, out underscore w and in underscore w. These are the output power and the input power, both in watts.

The function must return the efficiency as a percentage. That is one hundred times the useful output power divided by the input power.

There is one special case. When in underscore w is zero or negative, the function must return None. A zero input would cause a division by zero. So we put a guard at the top of the function, as in our safe underscore share example, and return None there.

Otherwise the function returns the percentage. Keep the exact name and parameter names shown on the slide.

## Slide 85: q5: 5 marks

READINGS is given in the notebook.

Using your own percent_error against a nominal of 100, set worst_reading to the reading with the largest error by size, and worst_error to that reading's signed percent error.

Keep the exact names and outputs. Check types, units and the issued brief.

**Spoken script**

Question five is worth five marks. It uses the six readings supplied in the notebook, stored in a list called READINGS.

We use our own percent underscore error function from question two, with a nominal value of one hundred. Nominal means the intended or expected value. So for each reading we work out the percent error against one hundred.

Then we set two names. Worst underscore reading is the reading whose error is largest by size. Worst underscore error is the signed percent error of that same reading, with its sign kept.

This is the method from the earlier slides. Use abs to get the sizes, max to find the largest, and index to find its position. Then use that position to pick out the reading and its signed error. Loops are not required, so trace the six readings on paper first to know what to expect.

## Slide 86: Engineering functions submission

01

Opens: 25 Sep 2026, 11:00 Kampala

02

Deadline: 02 Oct 2026, 11:00 Kampala

03

Use your full Student Registration Number in the form.

04

Keep the submitted files and confirmation.

Open W03 assignment form

https://docs.google.com/forms/d/e/1FAIpQLSfKemYzDIRelE0iDCo_KsJvzw0jyw--Fy8lyJHvm-XpNoEQkQ/viewform

**Spoken script**

This slide is for submitting your Week 3 assignment, Engineering functions. Complete your notebook first, then use the form button on the slide.

Check the opening and closing times on the slide. They are shown in Kampala time.

In the form, enter your full Student Registration Number. A shortened number can cause your work to be matched to the wrong person.

Keep the files you submitted and the confirmation that the form gives you. They are your proof that you submitted. Before you press submit, confirm that the notebook is the version you restarted, ran from the top and saved.

## Slide 87: Week 3 quiz

01

Answer individually after the lecturer activates the quiz.

02

Available for 24 hours from activation.

03

Use your Student Registration Number and registered account.

04

Check the announced quiz closing time.

Open this week’s quiz

https://forms.gle/vyTpTEpJUaAbAFbM9

**Spoken script**

This is the Week 3 quiz. It opens when the lecturer activates it, and it then stays open for twenty-four hours. The slide shows a twenty-four hour label for this reason.

Answer the quiz by yourself. Use your Student Registration Number and the account you registered with, so that your result goes to the right person.

Plan to complete it early in that window.

Check the announced closing time on the slide and from the lecturer, and use the link on the slide to open the quiz.

## Slide 88: Revision and submission checklist

You can explain each input, the returned answer and its engineering unit.

Check that the required files are in place.

Point to your evidence. Save your work.

**Spoken script**

This checklist closes the week. The slide asks you to explain your work. For each function, can you say what the inputs are, what answer comes back, and which engineering unit that answer carries?

You can check yourself in a simple way. Take double underscore value of four. Say that four goes into x, that the body works out eight, and that return sends eight back. Printing that value is a separate action.

The second part is about submission. Save your work and check the required submission files. Make sure the file you submit is the notebook you actually saved and completed.

Finally, point to your evidence. Your saved notebook shows the work you have done, so make sure that you can find it.

## Slide 89: Optional revision video

01

For revision after class.

02

Corey Schafer
Python Tutorial for Beginners 3: Integers and Floats

03

Opening 00:00–04:00, suggested four-minute excerpt; preview before class

04

Listening question: How are numbers written and how do arithmetic operators change them?

Open explainer video

https://www.youtube.com/watch?v=khKv-8q7YmY

**Spoken script**

This is an optional revision video for after class. It is a short lesson from Corey Schafer, Python Tutorial for Beginners 3, about integers and floats. An integer is a whole number, and a float is a number with a decimal point.

The slide suggests the opening four minutes of the video. Preview the excerpt before you watch it in full.

Watch with a question in mind. The listening question on the slide asks how numbers are written and how the arithmetic operators change them. Try to answer it in your own words afterwards, using terms from this week such as operator, value and type.

If the video does not load, the worked examples earlier in this lesson cover the same ideas. The link is on the slide.
