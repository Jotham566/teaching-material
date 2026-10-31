"""Machine Learning, sessions 1 to 6 and labs F01 and F02: authored concept slides, hero illustrations and speaker notes.

Figures come from figs_common.py. `at` places a slide: 0 before Block A, 1 before Block B, 2 after Block B.
"""

CONCEPTS = {}

FLOWER_LADDER = {'conds': [['petal_length < 2.5', 'guess = "setosa"'], ['petal_length < 4.8', 'guess = "versicolor"']], 'else_text': 'guess = "virginica"', 'code': None}

# ------------------------------------------------------------------ session 1
CONCEPTS[1] = {
    'question': {'fig': 'ml_r3_pipeline', 'alt': 'Homes we know, a line learned from them, and a guess for a new home',
                 'say': 'Here is the whole camp in one picture. On the left are one hundred and twenty homes. For each one we know the floor area and the rent. '
                        'In the middle the computer draws a line through those dots. On the right a new home appears, fifty square metres, and we ask the line to guess its rent. '
                        'That guess is a prediction. By the end of today you will have run it yourself, in your own notebook. You do not need to understand it yet. Session thirteen opens it up.'},
    'word_icons': {'file': 'folder', 'notebook': 'notebook', 'code cell': ('c_icon_cell',), 'output': ('c_icon_output',), 'print': ('c_icon_run',), 'prediction': ('ml_icon', {'kind': 'line'})},
    'slides': [
        {'at': 0, 'kind': 'concept', 'title': 'A notebook has text cells, code cells and output', 'fig': 'c_notebook_anatomy',
         'points': ['Text cells hold words for people.', 'Code cells hold instructions for Python.', 'Shift and Enter runs the cell you clicked.'],
         'say': 'Everything we do this term happens in a notebook. It is a page made of boxes called cells. '
                'A text cell holds words, like a title or a note to yourself. A code cell holds instructions for Python. Click a code cell, press Shift and Enter together, and the answer appears underneath it.\n\n'
                'Which part of this page can Python read, and which part is only for you?'},
        {'at': 0, 'kind': 'concept', 'title': 'The notebook needs its data file in the same folder', 'fig': ('c_folder_files', {'files': [['ML01.ipynb', 'notebook'], ['synthetic_homes.csv', 'table']]}),
         'points': ['A file is saved work with a name.', 'A folder keeps files together.', 'Keep the notebook and the homes data in one folder.'],
         'say': 'Before we run anything, find your camp folder. Inside it you should see this notebook and a file called synthetic_homes.csv. A file is saved work with a name, and a folder is where files are kept together. '
                'Python looks for data files in the same folder as the notebook, so keep them side by side.\n\n'
                'Open your folder now and check that both files are there. Put your hand up if one is missing.'},
        {'at': 0, 'kind': 'concept', 'title': 'print shows whatever sits inside its brackets', 'fig': 'ml_r3_print',
         'points': ['Words go between quotation marks.', 'A sum with no quotation marks is worked out.', 'The result appears under the cell.'],
         'say': 'The first instruction you will use is print. It shows something on the screen. Whatever you want shown goes inside the brackets. '
                'Words need quotation marks around them, so Hello, data comes out exactly as written. Three plus two has no quotation marks, so Python does the sum and shows five.\n\n'
                'Write down what you expect under each cell before you press Shift and Enter. A guess that turns out wrong is useful, because it shows you what to look at.'},
        {'at': 1, 'kind': 'concept', 'title': 'A prediction is a guess about a home we have not seen', 'fig': 'c_prediction_guess',
         'points': ['We know the rent of these homes.', 'The new home has an area but no rent yet.', 'The computer looks for a pattern to guess it.'],
         'say': 'A prediction is an informed guess about something that has not happened or has not been measured. On the left we have homes whose rents we know. '
                'On the right is a new home of fifty square metres, and nobody has told us its rent. The computer studies the homes it knows, looks for a pattern between area and rent, and uses that pattern to guess.\n\n'
                'Before we run the model, write your own guess for the rent of a fifty square metre home. We will compare it with the computer.'},
        {'at': 1, 'kind': 'concept', 'title': 'The computer draws a line through 120 homes', 'fig': 'c_scatter_line',
         'points': ['Each grey dot is one home.', 'The red line is the pattern the computer found.', 'The gold dot is its guess for 50 square metres.'],
         'say': 'Each grey dot is one home, placed by its area across the bottom and its rent up the side. Larger homes cost more, so the dots climb. The computer draws one straight line that runs as close as it can to all the dots.\n\n'
                'To guess for a new home, we go up from fifty square metres until we hit the line, then across to the rent axis. That gold dot is the prediction: about three hundred and nine thousand shillings a month. '
                'These homes are invented, so the number tells us nothing about real rents.'},
        {'at': 2, 'kind': 'wide', 'title': 'Six lines of code do five jobs', 'fig': 'c_model_code_map',
         'points': ['You do not need to understand every word yet.'],
         'say': 'Here is the code you just ran, with the jobs of each line marked on the left. The first two lines fetch the tools we need. The third line reads the homes file. '
                'The fourth line is where the learning happens: the computer fits a line to the homes. The fifth line asks that line for a guess at fifty square metres. The last line shows the answer.\n\n'
                'In session thirteen we take this apart one job at a time. For now, notice that five jobs fit in six lines.'},
    ],
}

# ------------------------------------------------------------------ session 2
CONCEPTS[2] = {
    'question': {'fig': 'c_sale_parts_types', 'alt': 'One sale in the shop table with a type under each part',
                 'say': 'Here is one sale from a practice shop: a bottle of juice, four units, two thousand shillings each. Each part is a different kind of thing. '
                        'The name is words. The count is a whole number. A price might have a decimal point. Python needs to know which kind it has, because each kind behaves differently. '
                        'Today we learn the kinds and how to store them.'},
    'word_icons': {'variable': ('c_icon_box',), 'string': ('c_icon_quotes',), 'value': ('ml_r3_wicon', {'kind': 'value'}), 'integer': ('ml_r3_wicon', {'kind': 'integer'}), 'float': ('ml_r3_wicon', {'kind': 'float'}), 'type': ('ml_r3_wicon', {'kind': 'type'})},
    'slides': [
        {'at': 0, 'kind': 'concept', 'title': 'A variable is a labelled box that holds a value', 'fig': ('c_labelled_boxes', {'code': ['price = 2000', 'quantity = 3', 'cost = price * quantity'], 'names': ['price', 'quantity', 'cost']}),
         'points': ['The name is the label on the box.', 'The value is what sits inside.', 'The equals sign stores a value in a box.'],
         'say': 'Picture the boxes in a storeroom. Every box has a label, and inside is what you counted. A variable is exactly that. The label is the name, like price. The contents are the value, like two thousand.\n\n'
                'The equals sign puts a value into a labelled box. In the last line, Python works out price times quantity first, and then stores the answer in a new box called cost. What number ends up inside cost?'},
        {'at': 0, 'kind': 'concept', 'title': 'The type of a value decides what you can do with it', 'fig': 'c_types_bins',
         'points': ['A whole number is an integer.', 'A number with a decimal point is a float.', 'Text in quotation marks is a string.'],
         'say': 'Python sorts every value into a type. Whole numbers are integers. Numbers with a decimal point are floats. Anything inside quotation marks is a string, which is a word for text.\n\n'
                'Look at the string bin. The last example is the character three in quotation marks. It looks like a number, but Python treats it as text. Asking Python for the type tells you which bin a value is in.'},
        {'at': 1, 'kind': 'concept', 'title': 'Python runs the lines from the top, one at a time', 'fig': 'ml_r3_trace',
         'points': ['Each row is one line running.', 'Gold marks the value that just changed.', 'total changes only when its own line runs again.'],
         'say': 'This table follows the notebook line by line. Gold marks the number that changed on that line. First price and quantity are stored. Then total is calculated and printed as five thousand and one.\n\n'
                'Next, quantity becomes four. Look at the total column on that row. It has not moved, because the line that calculates total has not run again. Only when we run it again does total become ten thousand and two. Where would you expect surprises like this in your own notebooks?'},
        {'at': 1, 'kind': 'concept', 'title': 'A calculated value waits until you calculate again', 'fig': 'ml_r3_stale',
         'points': ['Changing quantity does not change total.', 'The line that calculates total must run again.', 'Python reads from the top down.'],
         'say': 'Here is the same idea as three snapshots. In the first, total is five thousand and one. In the second we changed quantity, and total still says five thousand and one. '
                'In the third we ran the calculating line again and total caught up.\n\n'
                'If a number in your notebook looks wrong after an edit, ask which line you forgot to run again.'},
        {'at': 2, 'kind': 'concept', 'title': 'Quotation marks turn an amount into text', 'fig': ('c_text_vs_number', {'number': 2000}),
         'points': ['2000 is an amount Python can calculate with.', '"2000" is characters, like a name.', 'The type tells you which one you have.'],
         'say': 'To finish, look at these two values side by side. Both look like two thousand. The left one is an integer you can add and multiply. The right one has quotation marks, so Python sees four characters, like a name.\n\n'
                'In the practice task you write one sentence about this difference. Use the word type in it.'},
    ],
}

# ------------------------------------------------------------------ session 3
CONCEPTS[3] = {
    'question': {'fig': ('c_text_to_number', {'text': '12.5', 'mult': 4}), 'alt': 'The text 12.5 is converted with float and multiplied by four to give 50.0',
                 'say': 'Data often arrives as text. A price might be stored as the characters one, two, a point and five, with quotation marks around them. Python cannot multiply text. '
                        'The picture shows the fix: convert the text into a number first, then calculate with it. Today you learn that conversion, the four arithmetic symbols, and how to read the error message when something goes wrong.'},
    'word_icons': {'operator': 'calculator', 'parentheses': ('ml_r3_wicon', {'kind': 'parens'}), 'comment': ('ml_r3_wicon', {'kind': 'comment'}), 'convert': ('ml_r3_wicon', {'kind': 'convert'}), 'error message': ('ml_r3_wicon', {'kind': 'error'}), 'traceback': ('ml_r3_wicon', {'kind': 'trace'})},
    'slides': [
        {'at': 0, 'kind': 'concept', 'title': 'Four symbols do the arithmetic', 'fig': 'c_operators',
         'points': ['Plus adds and minus subtracts.', 'The star multiplies.', 'The slash divides.'],
         'say': 'Python uses the same four sums you know from school, but two of the symbols look different. Multiplication is a star, because a cross looks too much like the letter x. Division is a slash.\n\n'
                'Python works out each answer the moment the cell runs. Which answer in the last column has a decimal point, and why do you think it does?'},
        {'at': 0, 'kind': 'concept', 'title': 'Brackets change the order in which Python calculates', 'fig': 'c_precedence',
         'points': ['Python multiplies before it subtracts.', 'Brackets always go first.', 'Check a long sum by hand before you trust it.'],
         'say': 'On the left there are no brackets. Python multiplies five hundred by two first, which gives one thousand, and then takes that from three thousand. The answer is two thousand. '
                'On the right the brackets force the subtraction first. Twenty five hundred times two is five thousand.\n\n'
                'The same numbers give two different answers, so brackets are how you tell Python exactly what you mean. Which of these is the discount applied to each item? Check with the shop owner in your head.'},
        {'at': 1, 'kind': 'concept', 'title': 'A comment is a note for people that Python ignores', 'fig': 'ml_r3_comment',
         'points': ['A comment starts with a hash sign.', 'Python skips everything after it.', 'A good comment says why you did it.'],
         'say': 'The first line starts with a hash sign. That makes it a comment. Python reads straight past it. Comments are for the people who read your code, including you in a month when you have forgotten what the code was for.\n\n'
                'The remaining lines convert the text twelve point five into a number, multiply it by four and print fifty. Write one comment in your own notebook today.'},
        {'at': 1, 'kind': 'concept', 'title': 'A NameError means Python has never met that name', 'fig': ('ml_r3_error', {'error': 'NameError', 'message': "name 'price' is not defined", 'code': 'print(price)', 'hint': 'the name was never created in this session'}),
         'points': ['Read the last line first.', 'The line number says where to look.', 'Run the cell that creates the name, or fix its spelling.'],
         'say': 'An error message looks long, but only two parts matter. At the bottom is the name of the error and a few words about what went wrong. Above it is the line number where Python gave up.\n\n'
                'Here the bottom line says that price is not defined. Python has never been told what price means. What are the two quick things to check?'},
        {'at': 2, 'kind': 'concept', 'title': 'Nothing can be shared among zero people', 'fig': 'c_divide_by_zero',
         'points': ['Ten coins among five people gives two each.', 'Ten coins among nobody has no answer.', 'Python stops with a ZeroDivisionError.'],
         'say': 'This is the picture behind one of the practice questions. Share ten coins among five people and everybody gets two. Share ten coins among nobody and the question stops making sense. There is no person to hand a coin to.\n\n'
                'Python refuses to guess and stops with a ZeroDivisionError. Say it again in your own words in your notebook.'},
    ],
}

# ------------------------------------------------------------------ session 4
CONCEPTS[4] = {
    'question': {'fig': 'ml_r3_zones', 'alt': 'Eight flowers placed on a petal length scale with two cut points',
                 'say': 'These dots are eight flowers. Each sits at its petal length. White dots are one kind of flower, grey another and black the third. '
                        'The red dashed lines are two cut points. A flower to the left of the first line is called setosa, between the lines is called versicolor, and to the right of the second is called virginica. '
                        'That is a rule written with three questions. Today you write the rule in Python, and then count how often it names the right flower.'},
    'word_icons': {'comparison': ('ml_r3_wicon', {'kind': 'compare'}), 'Boolean': ('ml_r3_wicon', {'kind': 'bool'}), 'if': ('ml_r3_wicon', {'kind': 'if'}), 'else': ('ml_r3_wicon', {'kind': 'else'}), 'elif': ('ml_r3_wicon', {'kind': 'elif'}), 'indentation': ('ml_r3_wicon', {'kind': 'indent'})},
    'slides': [
        {'at': 0, 'kind': 'concept', 'title': 'A comparison answers True or False', 'fig': 'ml_r3_edge',
         'points': ['Three budgets meet the same rule.', 'The edge value counts when you write >=.', 'Test just below, on and just above the edge.'],
         'say': 'A comparison is a yes or no question. The ticket costs five thousand. Is the budget at least five thousand? For four thousand nine hundred and ninety nine the answer is False. For exactly five thousand it is True, because the symbol includes the edge itself. For five thousand and one it is True.\n\n'
                'The edge is where mistakes hide, so we always test one value below it, the value on it and one above it.'},
        {'at': 0, 'kind': 'concept', 'title': 'An if sends the program down one of two paths', 'fig': ('ml_r3_flow', {'conds': [['cost <= budget', 'message = "Within budget"']], 'else_text': 'message = "Over budget"', 'code': ['if cost <= budget:', '    message = "Within budget"', 'else:', '    message = "Over budget"']}),
         'points': ['True follows the indented if lines.', 'False follows the else lines.', 'Only one path runs each time.'],
         'say': 'The if instruction is a fork in the road. Python asks the question in the box. If the answer is True it takes the path to the right. If the answer is False it goes down to the else. It never takes both paths.\n\n'
                'The code above the flow chart is the same decision written for Python. With a cost of eight thousand and a budget of ten thousand, which box do you reach?'},
        {'at': 1, 'kind': 'concept', 'title': 'Four spaces tell Python which lines belong to the if', 'fig': 'c_indentation',
         'points': ['Lines pushed in by four spaces belong to the if or else.', 'The unindented line runs every time.', 'A colon ends each if and else line.'],
         'say': 'Python uses spaces to understand your code. The two lines that start with four spaces belong to the if and the else above them. They sit inside the fork. '
                'The last line has no spaces, so it sits outside the fork and runs every time.\n\n'
                'If you forget the spaces, Python stops with an IndentationError. Which lines run when the answer is True?'},
        {'at': 1, 'kind': 'concept', 'title': 'An elif asks a second question when the first is False', 'fig': ('ml_r3_flow', FLOWER_LADDER),
         'points': ['Python asks the questions from the top down.', 'It stops at the first True answer.', 'else catches every flower that is left.'],
         'say': 'This is the flower rule as a ladder of questions. First: is the petal shorter than two and a half? If yes, the guess is setosa and we stop. If no, we drop to the next question: is it shorter than four point eight? If yes, versicolor. '
                'Only when both answers are no do we reach the last box, virginica.\n\n'
                'Try a petal of four point seven. Which box do you reach?'},
        {'at': 2, 'kind': 'wide', 'title': 'The rule names seven of the eight flowers correctly', 'fig': ('ml_r3_zones', {'verdict': True}),
         'points': ['A red ring marks a flower the rule gets wrong.'],
         'say': 'Here is the same picture again, now with a verdict. Seven of the eight flowers sit in the zone that carries their own name. One does not. A versicolor with a petal of four point nine falls just past the second cut, so the rule calls it virginica.\n\n'
                'A rule that is right most of the time is useful, and it is also honest to say how often it is wrong. Where would you move the second cut to fix this one flower, and what might that break?'},
    ],
}

# ------------------------------------------------------------------ session 5
CONCEPTS[5] = {
    'question': {'fig': 'c_repeat_machine', 'alt': 'Three prices go one at a time through a doubling machine',
                 'say': 'Here are three prices. We want every one of them doubled. We could write the sum three times, but with three hundred prices that would be tiring. '
                        'The picture shows the trick. Feed the prices one at a time through the same machine, and collect the answers. In Python that idea is called a loop. Today you learn to store many values together and to loop over them.'},
    'word_icons': {'list': ('ml_r3_wicon', {'kind': 'list'}), 'index': ('ml_r3_wicon', {'kind': 'index'}), 'dictionary': ('ml_r3_wicon', {'kind': 'dict'}), 'key': ('c_icon_key',), 'loop': ('ml_r3_wicon', {'kind': 'repeat'}), 'item': ('ml_r3_wicon', {'kind': 'item'})},
    'slides': [
        {'at': 0, 'kind': 'concept', 'title': 'A list numbers its seats from zero', 'fig': ('c_bus_seats', {'values': [1000, 2000, 3000], 'name': 'prices', 'pointer': 0}),
         'points': ['A list keeps values in order.', 'The first seat is number 0.', 'Square brackets pick one seat.'],
         'say': 'Imagine a bus where every seat has a number painted on it. A list is like that. The values sit in order, and each seat has a number called an index. The surprise is that counting starts at zero.\n\n'
                'So prices with a zero in brackets gives the first price, one thousand. What would prices with a two in brackets give?'},
        {'at': 0, 'kind': 'concept', 'title': 'A dictionary finds a value by its key', 'fig': ('c_dict_board', {'mapping': {'name': '"Juice"', 'price': 2000}, 'key': 'price', 'name': 'product'}),
         'points': ['Each key has a value beside it.', 'Ask for the key to get its value.', 'A list uses seat numbers, a dictionary uses names.'],
         'say': 'A dictionary is a board of labelled facts. This board describes one product. It has a name and a price. You do not ask for the second row. You ask for price, and the board answers two thousand. The name you ask for is called the key.\n\n'
                'If you ask for a key that is not on the board, Python stops with a KeyError. Which small spelling slip would cause that?'},
        {'at': 1, 'kind': 'concept', 'title': 'A loop repeats the same lines for every item', 'fig': ('c_loop_anatomy', {'code': ['total = 0', 'for price in prices:', '    total = total + price', 'print(total)'], 'var': 'price'}),
         'points': ['price stands for one item at a time.', 'The indented lines repeat for every item.', 'The last line runs once, after the loop.'],
         'say': 'A loop is a way of saying do this for each one. The second line takes the prices one at a time and calls the current one price. Everything indented below it is the work that repeats. '
                'The last line has no indent, so it waits until the loop has finished.\n\n'
                'Say the code in plain English to your neighbour: for each price, add it to the total. Then say what the last line does.'},
        {'at': 1, 'kind': 'concept', 'title': 'The running total grows one item at a time', 'fig': ('ml_r3_loop_trace', {'values': [1000, 2000, 3000], 'var': 'price'}),
         'points': ['Each pass adds the current price.', 'The total after one pass is the total before the next.', 'The last total is the answer.'],
         'say': 'This table follows the loop pass by pass. On pass one the total is zero and we add one thousand. On pass two the total is one thousand and we add two thousand. On pass three we add three thousand and reach six thousand.\n\n'
                'The bars on the right show the growth. Cover the last row and predict the final total before you look.'},
        {'at': 2, 'kind': 'pair', 'title': 'Where the counter starts decides the answer', 'figs': [('ml_r3_reset_pair', {'values': [1000, 2000, 3000]}), ('ml_r3_reset_pair', {'inside': True, 'values': [1000, 2000, 3000]})],
         'captions': ['Counter set to 0 once, before the loop: the total keeps growing.', 'Counter set to 0 inside the loop: it restarts every pass.'],
         'say': 'One line moved and the answer changed completely. On the left the counter is set to zero once, before the loop, and the total reaches six thousand. On the right the zero sits inside the loop, so it resets on every pass and ends with just the last price.\n\n'
                'If your total looks like only the last value, look for a line that resets it inside the loop.'},
    ],
}

# ------------------------------------------------------------------ session 6
CONCEPTS[6] = {
    'question': {'fig': ('ml_r3_machine', {'name': 'guess_species', 'params': ['petal_length'], 'args': [4.7], 'body': 'the flower rule', 'result': '"versicolor"', 'show_code': False}),
                 'alt': 'The flower rule drawn as a machine: a petal length goes in and a species comes out',
                 'say': 'Last session you wrote a rule that names a flower from its petal length. Every time you wanted to use it, you had to retype the questions. '
                        'A function packages the rule as a machine. You drop in a petal length, four point seven, and out comes a name. Today you build that machine, and then write the checks that test it on flowers whose names we already know.'},
    'word_icons': {'function': ('ml_r3_wicon', {'kind': 'func'}), 'return': ('ml_r3_wicon', {'kind': 'return'}), 'assert': ('ml_r3_wicon', {'kind': 'assert'}), 'check': 'check', 'parameter': ('ml_r3_wicon', {'kind': 'slot'}), 'argument': ('ml_r3_wicon', {'kind': 'arg'})},
    'slides': [
        {'at': 0, 'kind': 'concept', 'title': 'A function is a machine: values in, answer out', 'fig': ('ml_r3_machine', {'name': 'total', 'params': ['price', 'quantity'], 'args': [2000, 3], 'body': 'price * quantity', 'code': ['def total(price, quantity):', '    return price * quantity']}),
         'points': ['The machine has a name.', 'Each input slot has a name.', 'The answer comes back out.'],
         'say': 'A function is a machine you build once and use as often as you like. This one is called total. It has two input slots called price and quantity. '
                'Drop in two thousand and three, the machine multiplies them, and out comes six thousand. The two lines at the bottom describe the machine to Python.\n\n'
                'What would come out if you dropped in one thousand and five?'},
        {'at': 0, 'kind': 'concept', 'title': 'Parameters, arguments and return each have a job', 'fig': ('c_function_anatomy', {'name': 'total', 'params': ['price', 'quantity'], 'args': [2000, 3], 'body': 'price * quantity'}),
         'points': ['Parameters are the names inside the machine.', 'Arguments are the real values you give it.', 'return sends the answer back.'],
         'say': 'The word def starts the description of the machine. The names in brackets on that line are the parameters. They are the labels on the input slots. The word return says what comes out.\n\n'
                'Later, when we use the machine, the real values we give it are called arguments. A parameter is the label on the slot. An argument is what you put in the slot. Can you point to each one in the code?'},
        {'at': 1, 'kind': 'concept', 'title': 'return hands the answer back, and print only shows it', 'fig': 'c_return_vs_print',
         'points': ['return gives the value to the rest of the program.', 'print writes on the screen and gives back nothing.', 'A function with no return holds None.'],
         'say': 'Two functions that look alike behave differently. On the left, the function returns its answer, so the variable a holds eight and we can use it later. On the right, the function prints. Eight appears on the screen, but nothing is handed back, so the variable b holds None.\n\n'
                'If your function shows None where you wanted a number, look for a missing return.'},
        {'at': 1, 'kind': 'concept', 'title': 'The flower rule becomes a function of three questions', 'fig': ('ml_r3_flow', {'conds': [['petal_length < 2.5', 'return "setosa"'], ['petal_length < 4.8', 'return "versicolor"']], 'else_text': 'return "virginica"', 'code': None}),
         'points': ['The function asks the same questions as before.', 'return ends the function as soon as it runs.', 'One argument in, one name out.'],
         'say': 'This is last session\'s ladder, now living inside a function. The questions are the same. The difference is that each box says return, so as soon as one question is True the function hands back that name and stops.\n\n'
                'Because it is a function, you can call it for any petal length without retyping the questions. Call it for one point four in your head. What does it hand back?'},
        {'at': 2, 'kind': 'wide', 'title': 'The function names seven of eight flowers right', 'fig': 'c_flower_scoreboard',
         'points': ['Checking every flower by loop gives the same count as checking by hand.'],
         'say': 'Here is every flower, scored by the function. The first row is the petal length. The second is the true species. The third is what our function says. The last row shows a tick when they agree.\n\n'
                'Seven ticks and one cross. The loop in your notebook counts them for you and prints seven. Does that match the count you made by hand last session?'},
        {'at': 2, 'kind': 'concept', 'title': 'assert tests the machine on known answers', 'fig': ('c_assert_checks', {'name': 'total', 'argnames': ['price', 'quantity'], 'cases': [[[2000, 3], 6000], [[1000, 0], 0], [[1000, 1], 1000]], 'good': 'price * quantity', 'bad': 'price + quantity'}),
         'points': ['A passing assert prints nothing.', 'A failing assert stops with AssertionError.', 'Test the edges, such as zero.'],
         'say': 'Each row is a check. We write down the answer we expect, run the function, and compare. The assert instruction compares for us. When the answers match, it stays silent, and silence means pass.\n\n'
                'The last row is a faulty function that adds instead of multiplying. It gives twenty oh three where we expected six thousand, and the assert would stop the program. Why is a zero quantity a good test to include?'},
    ],
}

# ------------------------------------------------------------------ foundation labs
CONCEPTS['F01'] = {
    'question': {'fig': ('ml_r3_predict_paper',), 'alt': 'Code on the left and a paper for predicted output on the right',
                 'say': 'In this lab you work like a computer. On the left is a short program. On the right is a sheet of paper with numbered lines, one for each thing the program will print. '
                        'Your job is to fill in the paper before you run anything. The numbers on the paper mark one line for each thing the program prints. Then run the code and check your paper. A wrong guess is the best kind of lesson.'},
    'word_icons': {'scalar': ('c_icon_box',), 'name': 'tag', 'top to bottom': ('ml_r3_wicon', {'kind': 'topdown'}), 'update': ('ml_r3_wicon', {'kind': 'update'}), 'string': ('c_icon_quotes',), 'prediction on paper': 'notebook'},
    'slides': [
        {'at': 0, 'kind': 'concept', 'title': 'Multiplying adds the same number again, quickly', 'fig': 'ml_r3_three_pens',
         'points': ['Three pens at UGX 1,000 add up to 3,000.', '3 * 1000 gives the same total.', 'Check Python against paper.'],
         'say': 'Start on paper, before any code. Draw three pens and write one thousand shillings on each. Add them: one thousand plus one thousand plus one thousand is three thousand. '
                'Now notice that three times one thousand gives the same answer. Multiplication is addition done quickly.\n\n'
                'Python will do the same sum. If the paper answer and the Python answer ever disagree, one of them has a mistake, and finding it is the point of the lab.'},
        {'at': 0, 'kind': 'concept', 'title': 'Names are boxes that hold values', 'fig': ('c_labelled_boxes', {'code': ['units = 3', 'price = 1000', 'total = units * price'], 'names': ['units', 'price', 'total']}),
         'points': ['units and price hold the inputs.', 'total holds the answer to a sum.', 'Each name points to one value.'],
         'say': 'In the program, three names are created. Units holds three. Price holds one thousand. Total is worked out from the other two, so it holds three thousand.\n\n'
                'Look at the picture and say each box aloud: units holds three, price holds one thousand, total holds three thousand. You will need this picture when you predict the printed lines.'},
        {'at': 1, 'kind': 'concept', 'title': 'Python runs lines from the top; total waits to be recalculated', 'fig': ('ml_r3_trace', {'code': ['units = 3', 'price = 1000', 'total = units * price', 'print(total)', 'print(total / units)', 'print("1000")', 'units = 4', 'print(total)', 'total = units * price', 'print(total)'], 'names': ['units', 'price', 'total']}),
         'points': ['Gold marks the value that changed on each line.', 'total stays 3000 after units becomes 4.', 'total changes only when its own line runs again.'],
         'say': 'Here is every line running in order. Gold marks the value that changed. Print shows a value on the screen without changing anything.\n\n'
                'Find the row where units becomes four. The total column does not change on that row, so the next print still shows three thousand. Only the line that calculates total again changes it to four thousand. Use this table to check your paper prediction.'},
        {'at': 1, 'kind': 'concept', 'title': 'Quotation marks make text, so the string 1000 is no amount', 'fig': ('c_text_vs_number', {'number': 1000}),
         'points': ['print("1000") shows the characters 1000.', 'The number 1000 can be multiplied.', 'The quotes decide which one you have.'],
         'say': 'One of the lines prints one thousand in quotation marks. It looks the same on the screen as the number one thousand, but it is a string. Python is showing four characters and has no amount to calculate with.\n\n'
                'On paper, how would you show the difference between the two? Write one sentence in your notebook that uses the word string.'},
    ],
}

CONCEPTS['F02'] = {
    'question': {'fig': 'c_vector_order', 'alt': 'A home with 40 square metres and 2 rooms, and the same two numbers swapped',
                 'say': 'Here are two numbers, forty and two. In the first order they describe a home with forty square metres and two rooms. Swap them and the numbers describe two square metres and forty rooms, which is not a home at all. '
                        'The order of the numbers gives them their meaning. Today we store such numbers in a list and in an array, and we see how each behaves when we do sums with it.'},
    'word_icons': {'scalar': ('c_icon_box',), 'vector': ('ml_r3_wicon', {'kind': 'vector'}), 'NumPy array': ('ml_r3_wicon', {'kind': 'array'}), 'shape': ('ml_icon', {'kind': 'shape'}), 'element-wise': ('ml_r3_wicon', {'kind': 'elementwise'}), 'unit': ('ml_r3_wicon', {'kind': 'unit'})},
    'slides': [
        {'at': 0, 'kind': 'concept', 'title': 'A vector is a list whose order carries meaning', 'fig': ('c_bus_seats', {'values': [40, 2], 'name': 'home', 'pointer': 0}),
         'points': ['Seat 0 holds the area in square metres.', 'Seat 1 holds the number of rooms.', 'Swap the seats and the meaning changes.'],
         'say': 'A list of numbers where the order matters is called a vector. Here seat zero holds the area and seat one holds the rooms. Python does not know that. You do. '
                'The only way to keep the meaning straight is to remember, and write down, what each position stands for.\n\n'
                'Home with a zero in brackets gives forty. What does home with a one in brackets give?'},
        {'at': 0, 'kind': 'concept', 'title': 'Add area to area and rooms to rooms', 'fig': 'ml_r3_units',
         'points': ['Every number carries a unit.', 'Square metres plus rooms makes no sense.', 'Write the unit beside the number you store.'],
         'say': 'Every number in a home vector carries a unit. Forty has a unit, square metres. Two has a unit, rooms. If you add them you get forty two of nothing in particular. A calculation only makes sense when the units match.\n\n'
                'That is why the second number in a home vector must never be added to the first. In the lab you write the unit in a comment or a column name every time.'},
        {'at': 1, 'kind': 'pair', 'title': 'Plus joins two lists but adds two arrays place by place', 'figs': [('c_list_vs_array_add',), ('c_list_vs_array_add', {'mode': 'array'})],
         'captions': ['Lists: plus joins them end to end. Nothing is added.', 'NumPy arrays: plus adds matching places.'],
         'say': 'The same plus sign does two different things. With ordinary lists it glues them together, so forty, two, ten, one becomes a list of four values. No sum has happened. '
                'With NumPy arrays the plus sign adds the numbers in matching places. Forty plus ten is fifty, and two plus one is three.\n\n'
                'Predict both results on paper first. Which one would you want for adding two homes together?'},
        {'at': 1, 'kind': 'concept', 'title': 'An array does the same calculation to every number at once', 'fig': 'c_array_scale',
         'points': ['Multiplying an array by 2 doubles every number.', 'shape (2,) means one row of two numbers.', 'This is called element-wise arithmetic.'],
         'say': 'A NumPy array can be calculated with all at once. Multiply the array by two and every number inside is doubled, so forty becomes eighty and two becomes four. This is called element-wise arithmetic, because it works on one element at a time.\n\n'
                'The shape tells you how the numbers are arranged. Shape two followed by a comma means a single row of two numbers. You will see shapes again when we feed data to a model.'},
    ],
}
