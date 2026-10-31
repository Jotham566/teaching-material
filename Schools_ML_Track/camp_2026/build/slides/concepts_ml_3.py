"""Machine Learning concept slides, sessions 7 to 12."""
CONCEPTS = {7: {'question': {'fig': 'ml_csv_to_table',
                  'alt': 'A CSV file of sales turned into a table of 60 rows and 5 columns',
                  'say': 'Look at the black box at the top. It is a plain text file, and each line is one sale of a book, a pen or a juice. The '
                         'first line holds the names of the columns. Python reads that file and turns it into a table with rows and columns. At the '
                         'bottom right is the size of the table: sixty rows and five columns. Today you learn to read this picture. The question is '
                         'how many sales are in the file and what each one records.'},
     'word_icons': {'row and column': ('ml_icon', {'kind': 'grid'}),
                    'header': ('ml_icon', {'kind': 'header'}),
                    'CSV file': ('ml_icon', {'kind': 'csv'}),
                    'library and import': 'book',
                    'DataFrame': ('ml_icon', {'kind': 'matrix'}),
                    'shape': ('ml_icon', {'kind': 'shape'})},
     'slides': [{'at': 0,
                 'kind': 'concept',
                 'title': 'One row is one record, one column one kind of fact',
                 'fig': 'ml_table_anatomy',
                 'points': ['Headers name the columns.', 'Each row records one sale.', 'Every cell sits in one row and one column.'],
                 'say': 'A table is a grid. Each row across is one record, so here one row is one sale. Each column down is one kind of fact, such '
                        'as the item or the number of units. The headers on top name the columns, so you never have to guess what a column holds.\n'
                        '\n'
                        'Pick any cell in the picture. Say which row it is in and which column.'},
                {'at': 0,
                 'kind': 'concept',
                 'title': 'Three short lists become a table with one line of code',
                 'fig': 'ml_code_to_table',
                 'points': ['Each list becomes one column.', 'Python fills in the row numbers.', 'The table is called a DataFrame.'],
                 'say': 'In Python a table is called a DataFrame. You can build a small one by hand. Give it a list for each column, and the first '
                        'item of every list lands in the first row.\n'
                        '\n'
                        'Look at the code and predict how many rows the table will have. Count the items in one list.'},
                {'at': 1,
                 'kind': 'wide',
                 'title': 'A CSV file is a table written as plain text',
                 'fig': 'ml_three_files',
                 'points': ['One line is one row.', 'Commas separate the columns.', 'Our files hold shop sales and invented homes.'],
                 'say': 'A CSV file stores a table as simple text. Each line is one row and a comma separates the columns. Because it is plain text, '
                        'any program can open it.\n'
                        '\n'
                        'This term you will meet three of them. The shop file holds one sale on each row. The homes file holds one home on each row. '
                        'Both are invented for practice, so they say nothing about real shops or real rents.'},
                {'at': 1,
                 'kind': 'concept',
                 'title': 'Shape gives rows first and columns second',
                 'fig': 'ml_shape_grid',
                 'points': ['The shop file has shape 60 by 5.',
                            'Check the shape straight after reading a file.',
                            'A wrong shape means a wrong file.'],
                 'say': 'After you read a file, ask for its shape. It gives two numbers. The first is the number of rows and the second is the '
                        'number of columns.\n'
                        '\n'
                        'For the shop file you should see sixty and five. If you see something else, you may have opened the wrong file, and it is '
                        'better to find out now than after an hour of work.'},
                {'at': 2,
                 'kind': 'wide',
                 'title': 'The file, the code and the table show the same sales',
                 'fig': 'ml_csv_to_table',
                 'points': ['Read the headers first, then the shape.'],
                 'say': 'Here is the whole path again. A text file holds the sales. One line of pandas reads it into a table. One more line reports '
                        'the shape.\n'
                        '\n'
                        'In the next session you will ask this table questions, starting with which item earns the most.'}]},
 8: {'question': {'fig': 'ml_who_earns_most',
                  'alt': 'Book, pen and juice with their prices and units sold, and a question mark where the money earned belongs',
                  'say': 'Three items, three prices, three counts of how many were sold. The book has the highest price, but the pen and the juice '
                         'sold more. Which one brought in the most money? Make a guess now. By the end of this session you will have the answer from '
                         'the data, and you will know how to get it with code.'},
     'word_icons': {'select a column': ('ml_icon', {'kind': 'grid_col'}),
                    'filter': ('ml_r3_wicon', {'kind': 'funnel'}),
                    'new column': ('ml_icon', {'kind': 'newcol'}),
                    'sum': ('ml_r3_wicon', {'kind': 'sum'}),
                    'group': ('ml_icon', {'kind': 'pie'}),
                    'revenue': 'coin'},
     'slides': [{'at': 0,
                 'kind': 'concept',
                 'title': 'Selecting a column pulls one list out of the table',
                 'fig': 'ml_select_col',
                 'points': ['Square brackets and a name pick a column.', 'The result is one column of values.', 'The table itself stays the same.'],
                 'say': 'To look at one column, write the table name, then square brackets, then the column name in quotation marks. Python hands '
                        'back just that column.\n'
                        '\n'
                        'Nothing is removed from the table. You have only taken a look at one part of it. What would you write to see the units '
                        'column?'},
                {'at': 0,
                 'kind': 'concept',
                 'title': 'A filter keeps the rows that pass a test',
                 'fig': 'ml_filter_rows',
                 'points': ['The test is written inside the brackets.', 'Rows that pass are kept.', 'Rows that fail are left out of the result.'],
                 'say': 'A filter asks a yes or no question about every row. Is units five or more? Rows that answer yes are kept. Rows that answer '
                        'no are left out of the new table.\n'
                        '\n'
                        'Predict how many of the first few rows would stay if we only kept sales of five units or more.'},
                {'at': 0,
                 'kind': 'concept',
                 'title': 'The filter makes a True or False for every row first',
                 'fig': 'ml_mask_steps',
                 'points': ['True keeps a row.', 'False drops it.', 'Read the mask before you trust the filter.'],
                 'say': 'Behind the filter is a list of True and False, one for each row. Python builds this list first, then keeps the rows marked '
                        'True.\n'
                        '\n'
                        'If a filter gives a surprising result, print the True and False list on its own. It tells you exactly which rows passed and '
                        'why.'},
                {'at': 1,
                 'kind': 'concept',
                 'title': 'A new column is worked out one row at a time',
                 'fig': 'ml_new_column',
                 'points': ['Revenue is units times unit price.', 'Every row gets its own revenue.', 'The five rows shown add up to 40,000.'],
                 'say': 'Money earned is called revenue. For each sale it is the units multiplied by the price of one unit. Python does this for '
                        'every row at once and stores the answers in a new column.\n'
                        '\n'
                        'The five rows on the slide add up to forty thousand shillings. Add up the whole column of sixty rows and you get the revenue of the shop: five hundred and fifty thousand shillings in this practice '
                        'file.'},
                {'at': 1,
                 'kind': 'wide',
                 'title': 'More units sold does not always mean more money',
                 'fig': 'ml_units_vs_money',
                 'points': ['Book: 297,000 UGX.', 'Juice: 150,000 UGX.', 'Pen: 103,000 UGX.'],
                 'say': 'Group the sales by item and add up the revenue. The book earned two hundred and ninety seven thousand shillings. The juice '
                        'earned one hundred and fifty thousand. The pen earned one hundred and three thousand.\n'
                        '\n'
                        'The pen sold the most units, yet it earned the least, because each pen costs so little. Units and money tell different '
                        'stories.'},
                {'at': 2,
                 'kind': 'concept',
                 'title': 'A filter gives a new, smaller table and keeps the original',
                 'fig': 'ml_filter_copy',
                 'points': ['The big table keeps all 60 rows.', 'The filtered table is a separate copy.', 'Name it so you can find it later.'],
                 'say': 'When you filter, Python builds a second table and leaves the first one untouched. That is why you give the result its own '
                        'name.\n'
                        '\n'
                        'If you ever want all sixty rows back, they are still there in the original table.'}]},
 9: {'question': {'fig': 'ml_units_dotplot',
                  'alt': 'A dot plot of units in 60 sales, with the median at 4.5 and the mean at 4.62',
                  'say': 'Every circle here is one sale, stacked on the number of units it had. You can see that two units is very common, and so '
                         'are seven and eight. The dashed line is the median and the red line is the mean. They are almost the same here. Today we '
                         'ask what a typical sale looks like and how spread out the sales are, and we learn when these two numbers stop agreeing.'},
     'word_icons': {'mean': ('ml_icon', {'kind': 'level'}),
                    'median': ('ml_icon', {'kind': 'median'}),
                    'range': ('ml_icon', {'kind': 'range'}),
                    'percentile': ('ml_r3_wicon', {'kind': 'percentile'}),
                    'proportion': ('ml_icon', {'kind': 'pie'}),
                    'outlier': ('ml_icon', {'kind': 'outlier'})},
     'slides': [{'at': 0,
                 'kind': 'concept',
                 'title': 'The mean shares the total out equally',
                 'fig': 'ml_mean_level',
                 'points': ['Four piles of 10, 12, 14 and 16 add up to 52.', 'Share 52 among 4 piles and each gets 13.', 'The mean of all 60 sales is 4.62 units.'],
                 'say': 'The mean is the amount each sale would have if the units were shared out equally. Add every value, then divide by how many '
                        'values there are.\n'
                        '\n'
                        'In the picture, four piles hold 10, 12, 14 and 16. That is 52 altogether. Share the 52 equally among the four piles and each one holds 13. '
                        'That 13 is the mean. For the sixty sales in the shop file the same sum gives four point six two units.'},
                {'at': 0,
                 'kind': 'concept',
                 'title': 'The median is the middle value after sorting',
                 'fig': 'ml_median_middle',
                 'points': ['Put the values in order.', 'Pick the middle one.', 'With two middle values, take their midpoint.'],
                 'say': 'The median is found by sorting the values and taking the one in the middle. With nine values there is one middle value. '
                        'With an even number there are two, so you take the point halfway between them.\n'
                        '\n'
                        'Try it with these values on paper before you look at the answer.'},
                {'at': 1,
                 'kind': 'concept',
                 'title': 'Sorting the sales shows the range and percentiles',
                 'fig': 'ml_sorted_staircase',
                 'points': ['The smallest sale has 1 unit and the largest has 8.', 'The range is 8 minus 1, which is 7.', 'The 75th percentile is 7 units.'],
                 'say': 'Line up the sixty sales from smallest to largest and the staircase shows the whole spread. The smallest sale had one unit. '
                        'The largest had eight. The range is the difference, which is seven.\n'
                        '\n'
                        'The red marks show percentiles. A quarter of the sales sit at 2 units or fewer, half at 4.5 or fewer, and three quarters at 7 or fewer. The range tells you how wide the data is. The percentiles tell you how the values are spread inside it.'},
                {'at': 1,
                 'kind': 'wide',
                 'title': 'An outlier moves the mean far more than the median',
                 'fig': 'ml_outlier_lines',
                 'points': ['Add one very large value.', 'The mean jumps from 13 to 30.4.', 'The median moves from 13 to 14.'],
                 'say': 'An outlier is a value far away from the rest. Add one huge sale to a small list and watch what happens. The mean leaps from '
                        'thirteen to thirty point four. The median only moves from thirteen to fourteen.\n'
                        '\n'
                        'When a few extreme values are possible, which number would you quote as the typical one?'},
                {'at': 2,
                 'kind': 'concept',
                 'title': 'A proportion counts a part against the whole',
                 'fig': ('ml_counters', {'n': 20, 'k': 12, 'cols': 5}),
                 'points': ['12 gold counters out of 20.', '12 divided by 20 is 0.6.', 'Times 100, that is 60 percent.'],
                 'say': 'A proportion is a part divided by the whole. Twelve of twenty counters are gold, so the proportion is twelve over twenty, '
                        'which is zero point six. Multiply by a hundred and it becomes sixty percent.\n'
                        '\n'
                        'Use the same idea on the shop data: what share of the sales had five units or more?'}]},
 10: {'question': {'fig': 'ml_raw_problems',
                   'alt': 'A small table with two blank prices and a repeated row, and three counting commands',
                   'say': 'This is a tiny table with trouble in it. Two prices are blank, and the row for id two appears twice. On the right are '
                          'three lines of code that count the problems for us. The first counts blank prices, the second counts repeated rows and '
                          'the third counts the rows left after cleaning. Today you learn to find problems like these and to fix them without hiding '
                          'what you did.'},
      'word_icons': {'missing value': ('ml_r3_wicon', {'kind': 'missing'}),
                     'duplicate': ('ml_icon', {'kind': 'copy'}),
                     'raw data': 'folder',
                     'cleaning log': 'notebook',
                     'to_csv': ('ml_icon', {'kind': 'csv'}),
                     'index=False': ('ml_r3_wicon', {'kind': 'noindex'})},
      'slides': [{'at': 0,
                  'kind': 'concept',
                  'title': 'Keep the raw file untouched and clean a copy',
                  'fig': 'ml_copy_raw',
                  'points': ['Read the raw file once.', 'Work on a copy with a new name.', 'The raw file is your proof.'],
                  'say': 'Never change the original file. Read it, make a copy in your notebook, and clean the copy. If something goes wrong, the '
                         'raw file is still there for you to start again.\n'
                         '\n'
                         'Why do you think a scientist keeps the original measurements, even after tidying them?'},
                 {'at': 0,
                  'kind': 'concept',
                  'title': 'Filling a blank with zero changes the average',
                  'fig': 'ml_zero_changes_mean',
                  'points': ['Zero says the item was free.', 'Nobody wrote the price down.', 'Leaving it blank keeps the mean honest.'],
                  'say': 'A missing value is a blank, which is different from a zero. If you replace the blank with zero, the table now says the '
                         'item cost nothing, and the average price falls.\n'
                         '\n'
                         'In the picture the average of the two real prices is two thousand. Fill the blank with zero and the average drops to one '
                         'thousand three hundred and thirty three.'},
                 {'at': 1,
                  'kind': 'concept',
                  'title': 'A cleaning log names each change and its row count',
                  'fig': 'ml_cleaning_log',
                  'points': ['One line per change.', 'Write how many rows changed.', 'A reader could repeat each step.'],
                  'say': 'The cleaning log is a short table. Each line says what you did, such as removed a duplicate, and how many rows it '
                         'touched.\n'
                         '\n'
                         'Someone reading your log should be able to repeat every step and reach the same table. That is what makes your work '
                         'trustworthy.'},
                 {'at': 1,
                  'kind': 'wide',
                  'title': 'index=False keeps row numbers out of the saved file',
                  'fig': 'ml_save_roundtrip',
                  'points': ['to_csv writes the table to a file.', 'index=False leaves out the extra numbers.', 'Read it back to check.'],
                  'say': 'To save the cleaned table, use to underscore csv. Without a small extra setting, Python adds a column of row numbers that '
                         'nobody asked for. Writing index equals False leaves it out.\n'
                         '\n'
                         'After saving, read the file back and look at the shape. If it matches, your save worked.'}]},
 11: {'question': {'fig': 'ml_chart_trio',
                   'alt': 'A bar chart, a histogram and a box plot, each with a label for its job',
                   'say': 'Here are three charts of the same shop. A bar chart compares amounts. A histogram shows how values are spread. A box plot '
                          'compares the spread of several groups. Each chart answers a different question, so choosing the right one is half the '
                          'job. Today you draw all three and write one careful sentence about each.'},
      'word_icons': {'bar chart': 'bars',
                     'histogram': ('ml_icon', {'kind': 'bars_hist'}),
                     'box plot': ('ml_icon', {'kind': 'box'}),
                     'axis label': ('ml_r3_wicon', {'kind': 'axis'}),
                     'title': ('ml_r3_wicon', {'kind': 'title'}),
                     'finding': 'magnifier'},
      'slides': [{'at': 0,
                  'kind': 'wide',
                  'title': 'Match the chart to the question you are asking',
                  'fig': 'ml_pick_chart',
                  'points': ['Which is largest? Use a bar chart.',
                             'How are values spread? Use a histogram.',
                             'Do groups differ in spread? Use a box plot.'],
                  'say': 'Do not start with the chart. Start with the question. If you ask which item earns the most, you want bars. If you ask how '
                         'the units in a sale are spread, you want a histogram. If you want to compare groups, a box plot puts them side by side.\n'
                         '\n'
                         'Look at the three questions and say which chart you would choose for each.'},
                 {'at': 0,
                  'kind': 'concept',
                  'title': 'A chart needs a title, axis labels and a zero start',
                  'fig': 'ml_chart_anatomy',
                  'points': ['The title says what the chart shows.', 'Axis labels give the unit.', 'Bars start at zero.'],
                  'say': 'Every chart needs a title, and each axis needs a label with its unit. Bars must start at zero. If they start higher, a '
                         'small difference looks enormous.\n'
                         '\n'
                         'Find the axis label and the zero line in the picture. Could a stranger read this chart without asking you anything?'},
                 {'at': 1,
                  'kind': 'concept',
                  'title': 'A histogram counts how many values fall in each bin',
                  'fig': 'ml_hist_bins',
                  'points': ['Each bar is a bin.', 'The height counts the sales in it.', 'Change the bins and the shape changes.'],
                  'say': 'A histogram cuts the number line into bins and counts how many values land in each. The taller the bar, the more sales had '
                         'that number of units.\n'
                         '\n'
                         'The shape depends on the bins you choose, so try two or three settings before you describe it.'},
                 {'at': 1,
                  'kind': 'concept',
                  'title': 'A box holds the middle half of the values',
                  'fig': 'ml_boxplot_anatomy',
                  'points': ['The line in the box is the median.', 'The box spans the middle half.', 'The whiskers show the rest of the spread.'],
                  'say': 'A box plot packs the spread of a column into one small drawing. The line inside the box is the median. The box itself '
                         'holds the middle half of the values. The whiskers reach out towards the smallest and largest.\n'
                         '\n'
                         'Compare two boxes. Which one has the higher median, and which one is more spread out?'},
                 {'at': 2,
                  'kind': 'wide',
                  'title': 'A finding is one careful sentence next to the chart',
                  'fig': 'ml_finding_card',
                  'points': ['Say what the chart shows.', 'Quote one number from it.', 'Add one limit.'],
                  'say': 'A chart on its own invites guesses. Add one sentence that says what it shows, with a number, and one sentence that says '
                         'what it cannot show.\n'
                         '\n'
                         'Here the practice data has no costs, so we cannot say anything about profit. Write a finding for your own chart in the '
                         'same shape.'}]},
 12: {'question': {'fig': 'ml_checkpoint_flow',
                   'alt': 'Six steps: read, check, calculate, chart, explain and rerun',
                   'say': 'Checkpoint one is these six steps, done on your own in one notebook. Read the file, check it, calculate something, draw a '
                          'labelled chart, explain what you found, and rerun everything from the top. The notebook must work the same way for anyone '
                          'who opens it. Today you also choose the question for your project.'},
      'word_icons': {'checkpoint': 'check',
                     'reproducible': ('ml_r3_wicon', {'kind': 'repeat'}),
                     'data dictionary': 'book',
                     'target': ('ml_icon', {'kind': 'target'}),
                     'input': ('ml_r3_wicon', {'kind': 'input'}),
                     'limitation': ('ml_r3_wicon', {'kind': 'limit'})},
      'slides': [{'at': 0,
                  'kind': 'concept',
                  'title': 'Restart and run all proves a notebook works',
                  'fig': 'ml_restart_run_all',
                  'points': ['A notebook can remember cells you deleted.', 'Restart clears that memory.', 'Run all checks every cell in order.'],
                  'say': 'A notebook can seem fine because it remembers a cell you have since deleted. On another laptop it fails. Restart and run '
                         'all clears the memory and runs every cell from the top, so it shows the truth.\n'
                         '\n'
                         'Do this before you hand anything in. What do you expect to find?'},
                 {'at': 1,
                  'kind': 'concept',
                  'title': 'A project question names an input, a target and a test',
                  'fig': 'ml_question_target_input',
                  'points': ['The target is the answer you want.', 'Inputs must be known before the answer.', 'The question ends with a mark.'],
                  'say': 'A good project question says what you will predict and from what. Can area and rooms predict monthly rent? The rent is the '
                         'target. Area and rooms are the inputs. Every input has to be known before the rent is.\n'
                         '\n'
                         'Write your own question in this shape before the end of the session.'},
                 {'at': 1,
                  'kind': 'wide',
                  'title': 'Three sentences set up a project',
                  'fig': 'ml_three_sentences',
                  'points': ['Sentence one is the question.', 'Sentence two names the data.', 'Sentence three names the target.'],
                  'say': 'Your project starts with three short sentences. The question, the data you will use, and the target. If you can write '
                         'these clearly, you are ready to start.\n'
                         '\n'
                         'Read your three sentences to a neighbour. Can they say back what you will predict?'},
                 {'at': 2,
                  'kind': 'concept',
                  'title': 'A data dictionary lets a stranger read your file',
                  'fig': 'ml_data_dictionary',
                  'points': ['One line for each column.', 'Say what each column means.', 'Mark which column is a label only.'],
                  'say': 'A data dictionary is a short list that explains every column. It means someone who has never seen the file can still read '
                         'it. Note that home underscore id is only a label, so it is never used as an input.\n'
                         '\n'
                         'Write the dictionary once, and it saves everybody time later.'}]}}
