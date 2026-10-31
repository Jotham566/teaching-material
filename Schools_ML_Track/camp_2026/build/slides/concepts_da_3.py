"""Python for Data Analysis concept slides, sessions 7 to 12."""
CONCEPTS = {7: {'question': {'fig': 'da_tables_hero',
                  'alt': 'Three tables from the camp data folder, each with rows and columns',
                  'say': 'Open the camp folder and you will find several files. Each one holds a table. A table is the most common shape that data '
                         'takes, and every question we ask this term starts by looking inside one. Look at the three tables on the screen. One has '
                         'sixty rows, one has fifteen and the biggest has more than fifteen hundred. Today we learn to open a table in Python and say what is in it: '
                         'how many rows, which columns and what kind of fact each column holds.'},
     'word_icons': {'row': ('da_icon_grid', {'mode': 'row'}),
                    'column': ('da_icon_grid', {'mode': 'col'}),
                    'header': 'tag',
                    'CSV': 'folder',
                    'DataFrame': 'notebook',
                    'library': 'book'},
     'slides': [{'at': 0,
                 'kind': 'concept',
                 'title': 'A table has rows across, columns down and a header',
                 'fig': 'da_table_anatomy',
                 'points': ['One row is one record, such as one sale.', 'One column holds one kind of fact.', 'The header names each column.'],
                 'say': 'Here is a table with the parts named. A row runs across the page, and each row is one record. In our shop data one row is '
                        'one sale. A column runs down the page, and each column holds one kind of fact, such as the number of units or the price of '
                        'one unit. The names along the top are called the header. They are how we ask for a column later.\n'
                        '\n'
                        'Point to one row and one column on your own sheet. Which fact sits where they cross?'},
                {'at': 0,
                 'kind': 'concept',
                 'title': 'read_csv turns a text file into a DataFrame',
                 'fig': 'da_csv_to_df',
                 'points': ['A CSV file is plain text with commas between values.',
                            'pandas is the library that reads it.',
                            'The result is a DataFrame.'],
                 'say': 'On the left is a CSV file. CSV stands for comma separated values, which means the table is stored as plain text with a '
                        'comma between each value. On the right is what we get after one line of Python. The instruction read_csv, from a library '
                        'called pandas, reads the text and builds a table object called a DataFrame. The first line of the file becomes the header. '
                        'Every other line becomes a row.\n'
                        '\n'
                        'Match one line of text on the left with one row of the table on the right.'},
                {'at': 1,
                 'kind': 'concept',
                 'title': 'A dictionary of columns builds a DataFrame by hand',
                 'fig': 'da_df_from_dict',
                 'points': ['Each key is a column name.', "Each list holds that column's values.", 'The lists must be the same length.'],
                 'say': 'We can also build a small table ourselves. In Python a dictionary pairs a name with a list of values. If each name is a '
                        'column and each list is the values in that column, pandas stitches them into a DataFrame.\n'
                        '\n'
                        'There is one rule. Every list has to be the same length, because each row needs a value in every column. If one list is '
                        'shorter, pandas will stop and tell you. Check the picture and count the values in each list before we run it.'},
                {'at': 1,
                 'kind': 'wide',
                 'title': 'shape gives rows first and columns second',
                 'fig': 'da_shape_rule',
                 'points': ['The Sunrise sales table has 1,513 rows and 6 columns.'],
                 'say': 'The attribute called shape tells you the size of a table in one go. It always reports two numbers, and the rows come first. '
                        'For the Sunrise sales file the answer is one thousand five hundred and thirteen rows and six columns. That means one '
                        'thousand five hundred and thirteen sales, with six facts about each.\n'
                        '\n'
                        'Notice there are no brackets after shape. It is a fact about the table, so we only read it. Rows first, columns second.'},
                {'at': 2,
                 'kind': 'concept',
                 'title': 'Every column has a dtype that decides what it can do',
                 'fig': 'da_dtypes',
                 'points': ['int64 holds whole numbers.', 'float64 holds numbers with decimals.', 'object holds text.'],
                 'say': 'When pandas reads a file it guesses what kind of value each column holds, and the guess is called the dtype. Whole numbers '
                        'become int64. Numbers with a decimal point become float64. Text becomes object. The dtype matters because it decides what '
                        'we may do. You can add up a column of numbers, and you cannot add up a column of names.\n'
                        '\n'
                        'Look at the units column and the item column. Which dtype does each one have, and why?'}]},
 8: {'question': {'fig': 'da_hero_takings',
                  'alt': 'A small shop with sales piling up, and three items whose takings we want to find',
                  'say': 'A practice shop sold pens, books and juice over sixty sales. At the end of the period the owner wants two numbers. How '
                         'much money did the shop take in, and which item brought it in? The table does not have a money column yet. It has units '
                         'and a price, and money is units times price. Today we select the columns we need, filter the rows we want, and calculate '
                         'the money column ourselves.'},
     'word_icons': {'select': 'magnifier', 'filter': ('r1_icon_funnel',), 'mask': 'check', 'new column': 'tag', 'revenue': 'coin', 'sum': 'calculator'},
     'slides': [{'at': 0,
                 'kind': 'concept',
                 'title': 'Square brackets and a name select one column',
                 'fig': 'da_select_column',
                 'points': ['One name gives one column.', 'A list of names gives a smaller table.', 'The name must match the header exactly.'],
                 'say': 'To look at one column, write the table name and then the column name inside square brackets. In quotation marks, because '
                        'the name is text. You get back that single column and nothing else. If you want two columns, put the names in a list, which '
                        'means a second pair of square brackets inside the first.\n'
                        '\n'
                        'The spelling has to match the header exactly. Units with a capital letter is a different name from units without one. That '
                        'is where the KeyError in your errors list comes from.'},
                {'at': 0,
                 'kind': 'concept',
                 'title': 'A filter keeps only the rows where the mask says True',
                 'fig': 'da_filter_mask',
                 'points': ['A comparison gives True or False for every row.',
                            'That column of True and False is the mask.',
                            'Only the True rows survive.'],
                 'say': 'Filtering has two steps, and they happen in one line. First Python compares every row with your rule, for example item '
                        'equals Pen. That gives a column of True and False answers, one for each row. We call that column the mask. Then the table '
                        'keeps the rows where the mask is True and drops the rest.\n'
                        '\n'
                        'Look at the gold rows. They are the ones the mask let through. How many rows will be left if the mask has four True '
                        'answers?'},
                {'at': 1,
                 'kind': 'concept',
                 'title': 'A new column is calculated for every row at once',
                 'fig': 'da_new_column',
                 'points': ['Write the new column name on the left.',
                            'Calculate on the right from existing columns.',
                            'Every row gets its own answer.'],
                 'say': 'Here we make the money column. On the left of the equals sign we write a name that does not exist yet, revenue underscore '
                        'ugx. On the right we multiply the units column by the price column. Python does the multiplication row by row, so each sale '
                        'gets its own revenue, and the new column joins the table.\n'
                        '\n'
                        'Check the first gold row by hand. Units times price should match the revenue in the new column.'},
                {'at': 1,
                 'kind': 'concept',
                 'title': 'Revenue is units times price, summed over all sales',
                 'fig': 'da_revenue_card',
                 'points': ['Revenue for one sale is units times price.',
                            'Add the column to get total revenue.',
                            'The practice shop took in 550,000 shillings.'],
                 'say': 'Revenue is the money that came in from selling. For one sale it is the units multiplied by the price of one unit. To get '
                        'the shop total we add up the whole revenue column, and pandas does that with sum. For the practice shop the answer is five '
                        'hundred and fifty thousand shillings, from two hundred and seventy seven units.\n'
                        '\n'
                        'Notice that the answer is one number. We started with sixty rows and boiled them down to a single total.'},
                {'at': 2,
                 'kind': 'concept',
                 'title': 'Revenue is not profit, because the table has no costs',
                 'fig': 'da_profit_unknown',
                 'points': ['Profit is revenue minus what the shop paid.', 'Our table has no cost column.', 'We can say revenue and stop there.'],
                 'say': 'It is tempting to call the total our profit. It is not. Profit is the money left after the shop pays for stock, rent and '
                        'wages. Our table only records what customers paid. It has no cost column, so the profit is unknown, and any number we gave '
                        'for it would be a guess.\n'
                        '\n'
                        'This is the first limitation you will write in your own reports. Say what the data shows, and say what it cannot show.'},
                {'at': 2,
                 'kind': 'wide',
                 'title': 'A filtered table is a copy of the original',
                 'fig': 'da_filter_copy',
                 'points': ['Save the filtered rows under a new name before you change them.'],
                 'say': 'When you filter, you get a smaller table. It is a copy. The original table still holds all sixty rows and is safe. Give the '
                        'copy its own name, such as pens, and you can change it without touching the original.\n'
                        '\n'
                        'If you ever see a warning about setting a value on a copy of a slice, this is the reason. Make the copy on purpose, with '
                        'copy, and the warning goes away.'}]},
 9: {'question': {'fig': 'da_hero_piles',
                  'alt': 'Sales sorted into piles by item, with a typical sale marked',
                  'say': 'The Sunrise Shops sold thousands of items over sixty days. The owner has two questions. Which item earns the most money, '
                         'and what does a typical sale look like? A single total cannot answer either one. We need to sort the sales into piles, one '
                         'pile for each item, and then measure each pile. That is what group, sort, mean and median are for, and today you will use '
                         'all four.'},
     'word_icons': {'group': 'bag', 'sort': ('r1_icon_sort',), 'mean': 'calculator', 'median': ('r1_icon_median',), 'proportion': ('r1_icon_pie',), 'denominator': ('r1_icon_fraction',)},
     'slides': [{'at': 0,
                 'kind': 'wide',
                 'title': 'Group splits rows, adds each pile, then combines',
                 'fig': 'da_split_apply_combine',
                 'points': ['Split by item, add each pile, combine into one small table.'],
                 'say': 'Grouping happens in three moves. Split means the rows are sorted into piles by the column you name, for example one pile '
                        'for each item. Apply means we calculate on each pile separately, for example the sum of revenue. Combine means the answers '
                        'come back together as one small table with one row per pile.\n'
                        '\n'
                        'Follow the picture from left to right. Where did the Pen pile go, and what number came out of it?'},
                {'at': 0,
                 'kind': 'pair',
                 'title': 'The best seller by units is not the top earner',
                 'figs': [('da_units_bar', {'which': 'units'}), ('da_units_bar', {'which': 'rev'})],
                 'captions': ['By units: Pen sells 103, Book 99, Juice 75.', 'By revenue: Book earns 297,000, Juice 150,000, Pen 103,000.'],
                 'say': 'Here are the same sixty sales grouped by item, drawn two ways. On the left each bar counts units. Pen sells the most, one '
                        'hundred and three. On the right each bar adds up money. Now Book is on top with two hundred and ninety seven thousand '
                        'shillings, because each book costs far more than a pen.\n'
                        '\n'
                        'So which item is the best seller? It depends on the question. Before you answer anything, decide whether you are counting '
                        'units or counting money.'},
                {'at': 1,
                 'kind': 'concept',
                 'title': 'One huge sale lifts the mean but not the median',
                 'fig': 'da_mean_pulled',
                 'points': ['The mean adds everything and divides by the count.',
                            'The median is the middle value in sorted order.',
                            'A big value drags the mean along, and the median holds still.'],
                 'say': 'The mean is the total divided by how many values there are. The median is the middle value once the values are lined up in '
                        'order. On the picture the mean sits like a balance point, and when one very large value joins the line, the balance point '
                        'slides toward it. The middle value hardly moves.\n'
                        '\n'
                        'In the Sunrise sales the mean sale is four thousand two hundred and fourteen shillings but the median is two thousand four '
                        'hundred. Which one describes a typical sale better?'},
                {'at': 1,
                 'kind': 'wide',
                 'title': 'A skewed histogram puts the mean right of the median',
                 'fig': 'da_hist_mean_median',
                 'points': ['Most sales are small, and a few are very large.'],
                 'say': 'This histogram counts how many sales fall in each range of value. Most of the bars crowd on the left, where the small sales '
                        'are. A few sales reach out to the right, up to one hundred and eight thousand shillings. That long tail drags the mean to '
                        'the right of the median.\n'
                        '\n'
                        'When a distribution looks like this we call it skewed. For a typical sale, quote the median, and mention the mean as the '
                        'number the big sales push up.'},
                {'at': 2,
                 'kind': 'concept',
                 'title': 'A proportion divides a part by its whole',
                 'fig': 'da_proportion_grid',
                 'points': ['The part goes on top.', 'The whole, the denominator, goes underneath.', 'Say which whole you divided by.'],
                 'say': 'A proportion tells you how big a part is compared with the whole. The part goes on top. The whole goes underneath, and that '
                        'bottom number is called the denominator. In the picture the gold squares are the part and all the squares together are the '
                        'whole.\n'
                        '\n'
                        'The denominator is where mistakes hide. Central Market earns two million nine hundred and ninety seven thousand shillings '
                        'out of six million three hundred and seventy five thousand nine hundred. Divide the first by the second to get its share.'},
                {'at': 2,
                 'kind': 'wide',
                 'title': 'Branch totals must add up to the grand total',
                 'fig': 'da_totals_check',
                 'points': ['Add the pieces and compare with the total before grouping.'],
                 'say': 'After any grouping, add the pieces and compare with the total you got without grouping. The three branch totals are two '
                        'million nine hundred and ninety seven thousand, one million nine hundred and eighty five thousand four hundred, and one '
                        'million three hundred and ninety three thousand five hundred. They add up to six million three hundred and seventy five '
                        'thousand nine hundred, which is the grand total.\n'
                        '\n'
                        'If your pieces do not add up to the whole, something went wrong, and it is better to find that now than after the report is '
                        'written.'}]},
 10: {'question': {'fig': 'da_hero_cleaning',
                   'alt': 'A raw sales file with repeated rows, blank cells and mixed date styles marked',
                   'say': 'This is the raw export of the Sunrise sales, exactly as the shop system produced it. It has one thousand five hundred and '
                          'thirty eight rows. Some rows are repeated. Some cells are empty. Some dates are written in a different style from the '
                          'others. Before we can trust any total, we need to know what is wrong and how many rows each problem touches. Today we '
                          'count the faults and write them down, and we do not delete anything in secret.'},
      'word_icons': {'raw data': 'folder',
                     'missing value': ('r1_icon_blank',),
                     'duplicate': ('r1_icon_dup',),
                     'data type': 'tag',
                     'copy': 'notebook',
                     'cleaning log': 'book'},
      'slides': [{'at': 0,
                  'kind': 'concept',
                  'title': 'Keep the raw file untouched and clean a copy',
                  'fig': 'da_raw_copy',
                  'points': ['The raw file is the evidence.', 'Work on a copy with a new name.', 'You can always start again from the raw file.'],
                  'say': 'The first rule of cleaning is to protect the original. The raw file is your evidence of what the shop system really '
                         'produced. We read it once, make a copy inside Python, and do all the changes on the copy. The file on disk never changes.\n'
                         '\n'
                         'If a step goes wrong, we throw the copy away and start again from the raw file. If we had changed the original, we could '
                         'not do that.'},
                 {'at': 0,
                  'kind': 'concept',
                  'title': 'Missing values and repeated rows are two problems',
                  'fig': 'da_missing_dup',
                  'points': ['A missing value is an empty cell.', 'A duplicate is a row that appears twice.', 'Each problem needs its own check.'],
                  'say': 'Two faults look alike but they are not the same. A missing value is a cell with nothing in it, so we do not know the '
                         'answer. A duplicate is a whole row that appears more than once, which means a sale could be counted twice. pandas has a '
                         'separate check for each one, and each gives you a count.\n'
                         '\n'
                         'Look at the gold cells on the picture. Which are missing, and which row has been repeated?'},
                 {'at': 1,
                  'kind': 'wide',
                  'title': 'Counting each fault shows how big the clean-up is',
                  'fig': 'da_raw_counts',
                  'points': ['25 repeated rows, 40 blank units, 60 slash dates, 12 units written as words.'],
                  'say': 'We counted every fault in the raw file. Twenty five rows are exact repeats. Forty rows have a blank in the units column. '
                         'Sixty dates use slashes instead of the standard style, and twelve units are written as words, like two or three, instead '
                         'of digits.\n'
                         '\n'
                         'These counts go into the cleaning log. Anyone who reads our report can see how much the file needed, and they can judge '
                         'for themselves whether we were careful.'},
                 {'at': 1,
                  'kind': 'concept',
                  'title': 'A cleaning log records what changed and how much',
                  'fig': 'da_cleaning_log',
                  'points': ['One line for each step.', 'Each line states the rows before and after.', 'The log is saved with to_csv.'],
                  'say': 'A cleaning log is a small table. Each line says what we did, how many rows we had before and how many we had after. '
                         'Reading it from top to bottom, you can follow the file from the raw state to the clean state without having to guess.\n'
                         '\n'
                         'We save it as a CSV so it travels with the project. The log is what lets a stranger trust the clean table.'},
                 {'at': 2,
                  'kind': 'wide',
                  'title': 'A zero is a fact and a blank is an unknown',
                  'fig': 'da_zero_vs_missing',
                  'points': ['Filling a blank with zero changes the totals and the averages.'],
                  'say': 'It is tempting to replace every blank price with zero, so that the table looks complete. That is a mistake. A zero says '
                         'the item was free. A blank says we do not know the price.\n'
                         '\n'
                         'If we turn blanks into zeros, the average price drops, the totals drop, and nobody can tell that it happened. Leave the '
                         'blank, count it, write it in the log, and decide on purpose what to do.'}]},
 11: {'question': {'fig': 'da_hero_chart_choice',
                   'alt': 'Four questions about data, each paired with the chart that answers it',
                   'say': 'Here are four kinds of question, and the chart that answers each one. Which is bigger? A bar chart. How does something '
                          'change? A line chart. How are values spread out? A histogram. Do two things go together? A scatter plot. The right chart '
                          'depends on the comparison you want the reader to make. Today we meet these four charts and practise choosing among them.'},
      'word_icons': {'matplotlib': 'book',
                     'bar chart': ('r1_icon_bar',),
                     'line chart': ('r1_icon_line',),
                     'histogram': ('r1_icon_hist',),
                     'scatter plot': ('r1_icon_scatter',),
                     'axis label': ('r1_icon_axes',)},
      'slides': [{'at': 0,
                  'kind': 'concept',
                  'title': 'A chart needs a title, labelled axes and a source',
                  'fig': 'da_chart_anatomy',
                  'points': ['The title states what is shown.', 'Each axis says what it measures and the unit.', 'A note names the data source.'],
                  'say': 'Look at the parts of a chart. The title tells the reader what they are looking at. Each axis has a label, and the label '
                         'includes the unit, such as shillings or units sold. At the bottom a small note names where the data came from, which for '
                         'us is the invented Sunrise Shops data.\n'
                         '\n'
                         'A reader who gets all of that does not need you standing next to the chart. Check your own charts for all three before you '
                         'show them.'},
                 {'at': 0,
                  'kind': 'pair',
                  'title': 'Cutting the axis makes a small gap look huge',
                  'figs': [('da_axis_honesty', {'kind': 'zero'}), ('da_axis_honesty', {'kind': 'cut'})],
                  'captions': ['The axis starts at zero: the bars are fairly compared.',
                               'The axis starts higher up: the gap looks bigger than it is.'],
                  'say': 'Both pictures show the same three numbers. On the left the vertical axis starts at zero, so a bar twice as tall means '
                         'twice as much. On the right the axis starts partway up, and the tallest bar looks several times bigger than the shortest, '
                         'even though the numbers have not changed.\n'
                         '\n'
                         'For bar charts we always start the axis at zero. A reader should be able to trust the heights.'},
                 {'at': 1,
                  'kind': 'concept',
                  'title': 'A histogram counts how many values fall in each range',
                  'fig': 'da_hist_tail',
                  'points': ['Each bar is a range of values.',
                             'Its height counts the sales in that range.',
                             'A long tail shows a few very large values.'],
                  'say': 'A bar chart compares groups. A histogram shows the spread of one column of numbers. We cut the values into ranges, and '
                         'each bar counts how many values land in a range. On this one, most sales are small, so the tall bars are on the left, and '
                         'a few large sales stretch out a thin tail to the right.\n'
                         '\n'
                         'Which range holds the most sales, and where does the tail end?'},
                 {'at': 1,
                  'kind': 'concept',
                  'title': 'A scatter plot shows one dot for each pair',
                  'fig': 'da_scatter_cr',
                  'points': ['One dot is one day.', 'Across is customers, up is revenue.', 'A pattern in the dots shows a link.'],
                  'say': 'A scatter plot compares two columns. Each dot is one row. How far across it sits shows the first value, and how far up it '
                         'sits shows the second. Here one dot is one day, with customers counted across the bottom and revenue up the side. The dots '
                         'drift upward from left to right, so busier days tend to bring in more money.\n'
                         '\n'
                         'We say tend to, because the dots do not sit on a perfect line.'},
                 {'at': 2,
                  'kind': 'concept',
                  'title': 'A line chart joins values over time',
                  'fig': 'da_line_dates',
                  'points': ['Time runs along the bottom.', 'The line joins one day to the next.', 'Crowded date labels can be rotated or thinned.'],
                  'say': 'A line chart is the right choice when the horizontal axis is time. The line joins each day to the next, so the eye follows '
                         'the rise and the fall. If the dates are crowded and overlap, rotate them or show fewer of them. That fixes the second item '
                         'in your errors list.\n'
                         '\n'
                         'Use a line only when the order matters. Joining three shops with a line would suggest they follow each other, and they do '
                         'not.'}]},
 12: {'question': {'fig': 'da_hero_checkpoint_one',
                   'alt': 'The Sunrise Shops sales table summarised for three shops',
                   'say': 'This is the first checkpoint. You have the Sunrise sales, one thousand five hundred and thirteen rows, and you have the '
                          'tools to load, summarise and chart them. The question is a big one. What do the sales tell us about the three shops? '
                          'Today you answer it on your own, in a notebook that someone else can restart and rerun, and I will mark what you wrote, '
                          'and how you checked it.'},
      'slides': [{'at': 0,
                  'kind': 'wide',
                  'title': 'Checkpoint one has five steps, from file to finding',
                  'fig': 'da_cp1_flow',
                  'points': ['Load, check, total, chart, then write what you found.'],
                  'say': 'The checkpoint has a clear order. We load the file. We check it, looking for missing values and repeats. We total the '
                         'revenue and group it by branch. We draw a chart. And only then do we write what we found.\n'
                         '\n'
                         'Keep the steps in this order in your notebook. If the order is clear, the marking is easy, and so is the rerun.'},
                 {'at': 0,
                  'kind': 'concept',
                  'title': 'A notebook that reads top to bottom is easy to rerun',
                  'fig': 'da_notebook_layout',
                  'points': ['A heading names each step.', 'Code sits below its heading.', 'A sentence under the output says what it shows.'],
                  'say': 'Here is a layout that works. Each step begins with a heading in a text cell. Under it comes the code, and under the code '
                         'comes the output. Then you add one sentence in your own words that says what the output means.\n'
                         '\n'
                         'When the notebook reads like this, a reader can follow it without asking you anything.'},
                 {'at': 2,
                  'kind': 'concept',
                  'title': 'Restart and run all before you trust a single number',
                  'fig': 'da_rerun_top',
                  'points': ['Restart the kernel to clear the memory.', 'Run all cells from the top.', 'Compare every number with your notes.'],
                  'say': 'A notebook can hide a mistake. You might have run a cell, changed it, and forgotten that a later cell still uses the old '
                         'value. The test is simple. Restart the kernel, which clears everything Python remembers, and run all the cells from the '
                         'top. If every number comes out the same, the notebook is honest.\n'
                         '\n'
                         'Do this at the end of the checkpoint. If a number changes, find the first cell that differs.'},
                 {'at': 2,
                  'kind': 'concept',
                  'title': 'Every finding points back to its output cell',
                  'fig': 'da_finding_trace',
                  'points': ['Write the number exactly as the output shows it.',
                             'Name the cell that produced it.',
                             'The total should match 6,375,900.'],
                  'say': 'A finding is a sentence with a number in it. Each one needs a trail back to the cell that produced the number. For '
                         'example, the total revenue of six million three hundred and seventy five thousand nine hundred comes from the cell that '
                         'sums the line value column.\n'
                         '\n'
                         'If a number in your sentences does not match any output, fix the sentence or find the mistake. Both are better than '
                         'leaving them different.'}]}}
