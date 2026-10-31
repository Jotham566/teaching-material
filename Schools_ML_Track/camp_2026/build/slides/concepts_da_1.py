"""Python for Data Analysis, sessions 1 to 6: authored concept slides, hero illustrations and speaker notes.

Figures come from figs_common.py. `at` places a slide: 0 before Block A, 1 before Block B, 2 after Block B.
"""

CONCEPTS = {}

# ------------------------------------------------------------------ session 1
CONCEPTS[1] = {
    'question': {'fig': 'c_hero_week_of_sales', 'alt': 'Bars showing the money a small shop took on each of its first seven days',
                 'say': 'Picture a small shop. Every sale goes onto a till roll, one line at a time. At the end of the week the owner asks a simple question: which days were busy and which were quiet? '
                        'Look at the bars. Each bar adds up one day of sales. Today we open a notebook and read the table of sixty sales that these bars come from. '
                        'By the end of the session you will be able to open a table like this yourself and look at it.'},
    'word_icons': {'notebook': 'notebook', 'cell': ('c_icon_cell',), 'run': ('c_icon_run',), 'output': ('c_icon_output',), 'file': 'folder', 'table': ('c_icon_grid',)},
    'slides': [
        {'at': 0, 'kind': 'concept', 'title': 'A notebook has text cells, code cells and output', 'fig': 'c_notebook_anatomy',
         'points': ['Text cells hold words for people.', 'Code cells hold instructions for Python.', 'Shift and Enter runs the cell you clicked.'],
         'say': 'This is the page we will work on for the whole camp. It is called a notebook. A notebook is built from boxes called cells. '
                'A text cell holds words, like a heading or a note to yourself. A code cell holds instructions that Python can carry out. '
                'When you click a code cell and press Shift and Enter together, Python runs it and the answer appears right underneath. That answer is called the output.\n\n'
                'Find the three parts on the picture. Which one does Python read, and which one is only for people?'},
        {'at': 0, 'kind': 'concept', 'title': 'print shows whatever sits inside its brackets', 'fig': 'c_print_anatomy',
         'points': ['Words go between quotation marks.', 'Without quotation marks Python works it out.', 'The result shows up under the cell.'],
         'say': 'Your first instruction is print. The word tells Python to show something, and the brackets hold what to show. '
                'Look at the first line. Hello, data sits between quotation marks, so Python treats it as plain words and shows them exactly as they are. '
                'Now look at the second line. There are no quotation marks, so Python sees a sum, works out three plus two and shows five.\n\n'
                'Before we run them, what do you expect to see under each cell? Write it down.'},
        {'at': 1, 'kind': 'concept', 'title': 'The notebook finds a data file in its own folder', 'fig': 'c_folder_files',
         'points': ['A file is saved work with a name.', 'A folder keeps files together.', 'Keep the notebook and the data side by side.'],
         'say': 'Now we move to the data. A file is a piece of saved work with a name, and a folder is a place that keeps files together. '
                'Our notebook is a file and the shop sales are a file, so each one needs a home. When Python looks for camp_shop.csv it first looks in the same folder as the notebook. '
                'If the two sit side by side, it finds the data straight away.\n\n'
                'Before you open the notebook today, check where your camp folder is, and tell me what files are inside it.'},
        {'at': 1, 'kind': 'wide', 'title': 'read_csv turns a text file into a table', 'fig': 'c_csv_to_table',
         'points': ['Each row is one sale and each column is one kind of fact.'],
         'say': 'On the left is the file exactly as it is stored. It is plain text, with commas between the values. It is hard to read, and nobody wants to count sales that way. '
                'The instruction read_csv reads the file and builds a table for us. The first line of the file becomes the column names. Every other line becomes one row.\n\n'
                'The gold row is sale number two: two pens at one thousand shillings each. Find the same numbers in the text on the left.'},
        {'at': 2, 'kind': 'pair', 'title': 'A file Python cannot find is a folder problem', 'figs': [('c_folder_files',), ('c_folder_files', {'mismatch': True})],
         'captions': ['Notebook and data side by side: Python finds the file.', 'Notebook in one folder, data in another: FileNotFoundError.'],
         'say': 'Here is the most common problem on day one. On the left, the notebook and the data are in the same folder and everything works. '
                'On the right, the notebook is in Downloads and the data is in Documents, so Python looks in the wrong place and stops with a FileNotFoundError.\n\n'
                'Notice that the message is not about your code at all. The fix is to move one file so the two sit together. If this happens to you, show me before you try anything else.'},
    ],
}

# ------------------------------------------------------------------ session 2
CONCEPTS[2] = {
    'question': {'fig': 'c_sale_parts_types', 'alt': 'One sale in the shop table with a type under each part',
                 'say': 'Here is one sale from the shop table: a bottle of juice, four units, two thousand shillings each, sold on the first of December. Each part is a different kind of thing. '
                        'The name Juice and the date are text. The number four is a count and two thousand is an amount of money. Python needs to know which kind it is dealing with, '
                        'because each kind behaves in its own way. That is what we are sorting out today.'},
    'word_icons': {'variable': ('c_icon_box',), 'string': ('c_icon_quotes',), 'value': 'coin', 'type': 'tag'},
    'slides': [
        {'at': 0, 'kind': 'concept', 'title': 'A variable is a labelled box that holds a value', 'fig': 'c_labelled_boxes',
         'points': ['The name goes on the label.', 'The value sits inside the box.', 'The equals sign stores it there.'],
         'say': 'Think of the stock boxes in a shop storeroom. Each box has a label, and inside is what you counted. A variable works the same way. '
                'The label is the name, such as price. The thing inside is the value, such as two thousand. The equals sign is the instruction that puts a value into a labelled box.\n\n'
                'Look at the third line. Python works out the right side first, price times units, and then stores the answer in a new box called revenue. What will be inside that box?'},
        {'at': 0, 'kind': 'concept', 'title': 'A value\'s type decides what you can do with it', 'fig': 'c_types_bins',
         'points': ['A whole number is an integer.', 'A number with a decimal point is a float.', 'Text in quotation marks is a string.'],
         'say': 'Python sorts every value into a type. A whole number with no decimal point is an integer. A number with a decimal point, like twenty five hundred and a half, is a float. '
                'Anything written between quotation marks is a string, which means text. Look at the three bins and notice that the string bin has the number three in it, but with quotation marks around it.\n\n'
                'If we ask Python for the type, it tells us which bin a value belongs to. Try it on your own laptop in a minute.'},
        {'at': 1, 'kind': 'concept', 'title': 'Quotation marks turn an amount into text', 'fig': 'c_text_vs_number',
         'points': ['2000 is an amount Python can calculate with.', '"2000" is only characters, like a name.', 'The type tells you which one you have.'],
         'say': 'These two look almost the same, but Python treats them very differently. Two thousand without quotation marks is an amount. You can multiply it, add it and compare it. '
                'Two thousand with quotation marks is just four characters in a row, the way a name is a few letters in a row.\n\n'
                'Why does this matter in a shop table? Because data often arrives as text, and a price that is text cannot be added up until we change it. We fix that next.'},
        {'at': 1, 'kind': 'wide', 'title': 'float() turns number-like text into a number', 'fig': ('c_text_to_number', {'text': '2500.5', 'mult': 2}),
         'points': ['Convert first, then calculate.'],
         'say': 'Here the price arrived as text, with quotation marks. Python cannot multiply text. The word float, followed by brackets, converts it into a real number with a decimal point. '
                'After that we can multiply by two and get five thousand and one.\n\n'
                'Follow the arrows from left to right. Where do the quotation marks disappear?'},
        {'at': 2, 'kind': 'concept', 'title': 'A calculated value waits until you calculate again', 'fig': 'c_stale_total',
         'points': ['Changing quantity does not change total.', 'The line that calculates total must run again.', 'Python reads from the top down.'],
         'say': 'This is a trap for almost every beginner. In the first column total is five thousand and one. In the second column we changed quantity to four, but total still says five thousand and one. '
                'Python does not update an earlier answer behind your back. Only when we run the line that calculates total again does it become ten thousand and two.\n\n'
                'Remember this when your numbers look wrong after an edit. Ask yourself which line you forgot to run again.'},
    ],
}

# ------------------------------------------------------------------ session 3
CONCEPTS[3] = {
    'question': {'fig': 'c_first_three_sales', 'alt': 'Three sales with their revenue worked out and added to 13,000 shillings',
                 'say': 'Here are the first three sales in the shop table. A book, a pen and a bottle of juice. Revenue for each sale is the number of units times the price of one unit. '
                        'You can work these out on paper in under a minute. Today we teach Python to do the same sums, and then we check that its answers agree with our paper answers.'},
    'word_icons': {'operator': 'calculator', 'error message': ('c_icon_output',), 'comment': 'notebook', 'line number': 'magnifier'},
    'slides': [
        {'at': 0, 'kind': 'concept', 'title': 'Four symbols do the arithmetic', 'fig': 'c_operators',
         'points': ['Plus adds and minus subtracts.', 'The star multiplies.', 'The slash divides.'],
         'say': 'Python uses the same four sums you know from school, but two of the symbols look different. Plus and minus are the same. '
                'Multiplication is written with a star, because a cross would be confused with the letter x. Division is written with a slash.\n\n'
                'Look at the last column. Every answer is worked out by Python the moment the cell runs. Which answer has a decimal point, and why do you think it does?'},
        {'at': 0, 'kind': 'concept', 'title': 'Multiplication goes before addition, brackets go first', 'fig': ('c_precedence', {'left': ['2 + 3 * 4', '3 * 4', 'multiply first'], 'right': ['(2 + 3) * 4', '(2 + 3)', 'brackets first']}),
         'points': ['Python multiplies and divides first.', 'Brackets always go first.', 'Check by hand before you trust a long sum.'],
         'say': 'The same numbers can give two different answers. On the left there are no brackets, so Python multiplies three times four first and then adds two. The answer is fourteen. '
                'On the right the brackets force the addition to happen first. Five times four gives twenty.\n\n'
                'When you write a long sum in your notebook, use brackets to say exactly what you mean. Then check the answer on paper.'},
        {'at': 1, 'kind': 'concept', 'title': 'The last line of an error message names the problem', 'fig': 'c_error_anatomy',
         'points': ['Read the last line first.', 'It names the error and says what happened.', 'The line number tells you where to look.'],
         'say': 'Errors are not a sign that you are bad at this. They are Python telling you what it could not do. An error message has a clear shape. '
                'At the top is a long heading that you can ignore for now. Near the middle is the line number and the instruction that failed. At the bottom is the part that matters most, the name of the error and a few words about what went wrong.\n\n'
                'Always read the bottom line first. What is the name of the error in this picture?'},
        {'at': 1, 'kind': 'concept', 'title': 'A NameError means Python has never met that name', 'fig': ('c_error_anatomy', {'error': 'NameError', 'message': "name 'units' is not defined", 'code': 'print(units)', 'hint': 'the name was never created in this session'}),
         'points': ['The name was spelled differently, or never created.', 'Run the cell that creates it first.', 'Check capital letters and spelling.'],
         'say': 'This is the error you will see most often. NameError says that Python has never been told what units means. Either you never ran the cell that creates it, or you spelled it a little differently, perhaps with a capital letter.\n\n'
                'Python is strict about spelling. Units with a capital U is a different name from units. Can you think of two quick things to check when you see this message?'},
        {'at': 2, 'kind': 'concept', 'title': 'Nothing can be shared among zero people', 'fig': 'c_divide_by_zero',
         'points': ['Ten coins among five people gives two each.', 'Ten coins among nobody has no answer.', 'Python stops with a ZeroDivisionError.'],
         'say': 'On the left, ten coins are shared among five people and everyone gets two. On the right, ten coins are shared among nobody. Who gets the coins? There is no answer, so there is nothing for Python to calculate.\n\n'
                'That is why Python stops with a ZeroDivisionError instead of guessing. In the practice task you explain this in your own words, so think of your own picture for it.'},
    ],
}

# ------------------------------------------------------------------ session 4
CONCEPTS[4] = {
    'question': {'fig': 'c_large_order_bars', 'alt': 'Units sold in each of the first twelve sales with a line at five units',
                 'say': 'Here are the units sold in the first twelve sales. A shopkeeper wants to treat any sale of five or more units as a large order. '
                        'The dashed line marks that rule, and the gold bars are the ones that pass it. Looking at the bars takes a second. '
                        'Python has no eyes, so we have to give it the rule in words it understands. Today we learn how to write that rule.'},
    'word_icons': {'comparison': 'magnifier', 'Boolean': 'check', 'if': ('c_icon_branch',), 'else': 'cross', 'indentation': ('c_icon_cell',), 'and, or': ('r1_icon_venn',)},
    'slides': [
        {'at': 0, 'kind': 'concept', 'title': 'A comparison answers True or False', 'fig': 'c_edge_numberline',
         'points': ['Three budgets meet the same rule.', 'The edge value counts when you write >=.', 'Always test just below, on and just above the edge.'],
         'say': 'A comparison is a question that can only be answered with True or False. The ticket costs five thousand. Is the budget at least five thousand? '
                'With four thousand nine hundred and ninety nine the answer is False. With exactly five thousand it is True, because the symbol greater than or equal to includes the edge itself. With five thousand and one it is also True.\n\n'
                'The edge is where mistakes hide, so we always test just below it, on it and just above it. Which of the three would you have forgotten to test?'},
        {'at': 0, 'kind': 'concept', 'title': 'An if sends the program down one of two paths', 'fig': 'c_decision_flow',
         'points': ['True follows the if lines.', 'False follows the else lines.', 'Only one path runs each time.'],
         'say': 'The if instruction is a fork in the road. Python asks the question in the box. If the answer is True it takes the path to Buy. If the answer is False it goes down to Save. '
                'It never does both. The code above the flow chart is the same decision written for Python.\n\n'
                'Trace the path with a budget of four thousand nine hundred and ninety nine. Which box do you reach?'},
        {'at': 1, 'kind': 'concept', 'title': 'Four spaces show which lines belong to the if', 'fig': 'c_indentation',
         'points': ['Lines pushed in by four spaces belong to the if or else.', 'The unindented line runs every time.', 'A colon ends each if and else line.'],
         'say': 'Python uses spaces to understand your code. The two lines that start with four spaces belong to the if and the else above them. They are inside the fork. '
                'The last line has no spaces, so it sits outside the fork and runs every time, whichever path was taken.\n\n'
                'If you forget the spaces, Python stops with an IndentationError. Check the gold boxes and tell me which lines run when the answer is True.'},
        {'at': 1, 'kind': 'concept', 'title': 'and needs both conditions, or needs just one', 'fig': 'c_and_or_table',
         'points': ['and is True only when both sides are True.', 'or is True when at least one side is True.', 'The gold row is the sale we are testing.'],
         'say': 'Sometimes one question is not enough. A sale can be large, expensive, both or neither. The word and joins two questions and is True only when both are True. The word or is True when at least one is True.\n\n'
                'Our example has six units at one thousand shillings. It is large but not expensive, so and gives False and or gives True. Find the gold row. Why does and fail there?'},
        {'at': 2, 'kind': 'concept', 'title': 'An elif adds a second question after a False answer', 'fig': ('c_decision_flow', {'conds': [['large and expensive', '"Large and expensive"'], ['large', '"Large only"']], 'else_text': '"Small"', 'code': None}),
         'points': ['Python asks the questions from the top down.', 'It stops at the first True answer.', 'else catches everything that is left.'],
         'say': 'Real decisions often have more than two outcomes. This ladder asks its first question. If the answer is True we stop and report a large and expensive sale. If it is False we drop to the next question. '
                'Only when every question has said False do we reach the last box. That last box is the else.\n\n'
                'Run the ladder in your head for six units at one thousand shillings. Which outcome do you reach?'},
    ],
}

# ------------------------------------------------------------------ session 5
CONCEPTS[5] = {
    'question': {'fig': 'c_six_sales_total', 'alt': 'The units of the first six sales added to 25',
                 'say': 'Here are the first six sales, each with its number of units. Adding six numbers by hand is easy. '
                        'But imagine sixty sales, or six thousand. Nobody wants to type a plus sign six thousand times. Today we learn how to store many values together and how to make Python add them up for us.'},
    'word_icons': {'list': ('c_icon_list',), 'index': ('r1_icon_index',), 'dictionary': ('r1_icon_dict',), 'key': ('c_icon_key',), 'loop': ('c_icon_loop',), 'running total': ('r1_icon_running',)},
    'slides': [
        {'at': 0, 'kind': 'concept', 'title': 'A list numbers its seats from zero', 'fig': 'c_bus_seats',
         'points': ['A list keeps values in order.', 'The first seat is number 0.', 'Square brackets pick one seat.'],
         'say': 'Imagine a bus where each seat has a number painted on it. A list is like that. The values sit in order, and each seat has a number called an index. '
                'The surprise is that counting starts at zero. The first seat is seat zero, the second is seat one, and so on.\n\n'
                'In the picture we ask for units with a three in brackets. Which value comes back? Count the seats from zero, and watch out, because most people say four.'},
        {'at': 0, 'kind': 'concept', 'title': 'A dictionary finds a value by its key', 'fig': 'c_dict_board',
         'points': ['Each key has a value beside it.', 'Ask for the key to get its value.', 'A list uses numbers, a dictionary uses names.'],
         'say': 'A dictionary works like the price board outside a shop. You do not ask for the second row. You ask for Pen, and the board tells you one thousand. The name you ask for is called the key. The answer is the value.\n\n'
                'If you write a key that is not on the board, Python stops with a KeyError. Which spelling mistake would cause that?'},
        {'at': 1, 'kind': 'concept', 'title': 'A loop repeats the same lines for every value', 'fig': 'c_loop_anatomy',
         'points': ['u stands for one value at a time.', 'The indented line repeats for every value.', 'The last line runs once, after the loop.'],
         'say': 'A loop is a way of saying do this for each one. The first line sets a counter to zero. The second line says take the values one at a time and call the current one u. '
                'The indented line below it is the work that repeats. The last line has no indent, so it waits until the loop is finished.\n\n'
                'Read the code aloud, in plain English, as if you were telling a friend. Can you do it without looking at the notes on the right?'},
        {'at': 1, 'kind': 'concept', 'title': 'The running total grows one value at a time', 'fig': 'c_loop_trace',
         'points': ['Each pass adds the current value.', 'The total after one pass is the total before the next.', 'The last total is the answer.'],
         'say': 'Here is what the loop actually does, pass by pass. On pass one the total is zero and we add one. On pass two it is one and we add two. '
                'The total after each pass becomes the total before the next. The bars on the right show it growing until it reaches twenty five, the same answer we got by adding the six numbers by hand.\n\n'
                'Cover the last column and predict pass five. Then uncover it.'},
        {'at': 2, 'kind': 'pair', 'title': 'Where the counter starts decides the answer', 'figs': [('c_reset_pair',), ('c_reset_pair', {'inside': True})],
         'captions': ['Counter set to 0 once, before the loop: the total keeps growing.', 'Counter set to 0 inside the loop: it restarts every pass.'],
         'say': 'The two programs differ by one line, and the answers are very different. On the left the counter is set to zero once, before the loop starts, and it grows to twenty five. '
                'On the right the line total equals zero sits inside the loop, so the counter restarts on every pass and finishes with only the last value.\n\n'
                'If your total is the same as your last value, look for a line that resets it inside the loop.'},
    ],
}

# ------------------------------------------------------------------ session 6
CONCEPTS[6] = {
    'question': {'fig': ('c_assert_checks', {}), 'alt': 'A table of known cases for the revenue function with passes and one failure',
                 'say': 'Before you trust a calculation, check it on cases where you already know the answer. Three units at two thousand is six thousand. No units is zero. Five units at one thousand is five thousand. '
                        'If your code agrees with all three, you can trust it more. If it disagrees with one, you have found a bug before it cost anyone money. '
                        'Today we package a calculation into a reusable machine and write the checks that test it.'},
    'word_icons': {'function': ('c_icon_function',), 'return': 'receipt', 'assert': 'check', 'edge case': 'magnifier', 'parameter': 'tag', 'argument': 'coin'},
    'slides': [
        {'at': 0, 'kind': 'concept', 'title': 'A function turns arguments into an answer', 'fig': 'c_function_machine',
         'points': ['The machine has a name.', 'Each input has a name, such as units.', 'The answer comes back out.'],
         'say': 'A function is a machine you build once and use as often as you like. Our machine is called revenue. It has two slots for inputs, called units and price. '
                'You drop in the numbers three and two thousand, the machine multiplies them, and out comes six thousand. The code at the bottom describes the machine in two lines.\n\n'
                'What would come out if you dropped in five and one thousand?'},
        {'at': 0, 'kind': 'concept', 'title': 'Each word in a function has its own job', 'fig': 'c_function_anatomy',
         'points': ['Parameters are the names inside the machine.', 'Arguments are the real values you give it.', 'return sends the answer back.'],
         'say': 'Four words matter here. The word def starts the description of the machine. The names in brackets on that line, units and price, are the parameters. They are the labels on the input slots. '
                'The word return says what comes out. Later, when we use the machine, the real numbers we give it, three and two thousand, are called arguments.\n\n'
                'A parameter is the label on the slot and an argument is what you put in the slot. Say that sentence once to your neighbour.'},
        {'at': 1, 'kind': 'concept', 'title': 'return hands the answer back, print only shows it', 'fig': 'c_return_vs_print',
         'points': ['return gives the value to the rest of the program.', 'print writes on the screen and gives back nothing.', 'A function with no return holds None.'],
         'say': 'These two functions look similar and behave very differently. On the left, the function returns the answer, so the variable a holds eight and we can use it later. '
                'On the right, the function prints the answer. Eight appears on the screen, but nothing is handed back, so the variable b holds None.\n\n'
                'If your function shows None where you expected a number, look for a missing return.'},
        {'at': 1, 'kind': 'concept', 'title': 'A guard stops the program dividing by zero', 'fig': ('c_decision_flow', {'conds': [['whole == 0', 'return 0']], 'else_text': 'return part / whole', 'code': ['def share(part, whole):', '    if whole == 0:', '        return 0', '    return part / whole']}),
         'points': ['Ask the risky question first.', 'Return early when the answer is True.', 'Only divide when it is safe.'],
         'say': 'We learned that dividing by zero stops the program. A function can protect itself with a guard. Before dividing, it asks whether the whole is zero. '
                'If it is, the function returns zero straight away and never reaches the division. If it is not, the function goes on and divides.\n\n'
                'Is returning zero always the right answer for a share of nothing? Think about it, because a guard is a choice and you should be able to explain it.'},
        {'at': 2, 'kind': 'wide', 'title': 'assert checks the machine on known answers', 'fig': 'r1_assert_demo',
         'points': ['Silence is the sign that every check passed.'],
         'say': 'The table lists three checks and a faulty version of the function. For each call we write the answer we expect, run the function, and compare. '
                'The assert instruction does the comparing for us. When the answer matches it stays silent, and silence means pass. When it does not match, Python stops and tells you.\n\n'
                'In the last row the faulty function added instead of multiplying. Which numbers would have shown that problem straight away?'},
    ],
}
