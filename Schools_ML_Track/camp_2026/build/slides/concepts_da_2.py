"""Python for Data Analysis concept slides, sessions 13 to 24."""
CONCEPTS = {13: {'question': {'fig': 'da_hero_numpy',
                   'alt': 'Dots for each of the 180 daily customer counts, with the mean and the median marked',
                   'say': 'Two questions today. How spread out are the daily customer counts, and which sales are unusually large? Over the sixty '
                          'days the shops counted on average one hundred and forty three customers, but some days were much quieter and some much '
                          'busier. And among the sales, a handful are far larger than the rest. To measure spread and spot the outliers we use '
                          'NumPy, the number tools that pandas is built on.'},
      'word_icons': {'NumPy': 'calculator',
                     'array': ('da_icon_grid', {'mode': 'row'}),
                     'element-wise': ('da_icon_elementwise', {}),
                     'percentile': ('da_icon_percentile', {}),
                     'standard deviation': ('da_icon_sd', {}),
                     'outlier': 'magnifier'},
      'slides': [{'at': 0,
                  'kind': 'concept',
                  'title': 'NumPy works on a whole array of numbers at once',
                  'fig': 'da_array_strip',
                  'points': ['Each box holds one number.', 'One instruction acts on every box.', 'Every element changes by the same rule.'],
                  'say': 'An array is a row of numbers, like a strip of boxes on a ruler. NumPy can act on the whole strip with one instruction. If '
                         'we add fifty customers to every day in the array, every box rises by fifty. We do not write a loop. NumPy does the work '
                         'box by box, and it does it fast.\n'
                         '\n'
                         'The word for this is element-wise. Each element is changed by the same rule, and you see it in the picture: seven boxes go '
                         'in, seven changed boxes come out.'},
                 {'at': 0,
                  'kind': 'concept',
                  'title': 'NumPy and pandas reach the same answer two ways',
                  'fig': 'da_two_routes',
                  'points': ['pandas works on named columns.', 'NumPy works on bare arrays.', 'Both must agree on the mean and the median.'],
                  'say': 'pandas columns are built on top of NumPy arrays, so the two can reach the same answer by different routes. With pandas we '
                         'name the column and ask for the mean. With NumPy we turn the column into an array and call the NumPy function.\n'
                         '\n'
                         'The two numbers should agree. If they differ only in the last decimal places, that is rounding, and it is nothing to worry '
                         'about.'},
                 {'at': 1,
                  'kind': 'wide',
                  'title': 'Percentiles split the sorted values into parts',
                  'fig': 'da_percentiles_line',
                  'points': ['For customers, the quartiles are 86.75 and 203.75 and the median is 131.5.'],
                  'say': 'Line up the daily customer counts from smallest to largest. The twenty fifth percentile is the value that a quarter of the '
                         'days fall below. For us that is eighty six point seven five customers. The median is the middle, one hundred and thirty '
                         'one point five. The seventy fifth percentile is two hundred and three point seven five, the value that three quarters of '
                         'the days fall below.\n'
                         '\n'
                         'The gap between the first and third quartile holds the middle half of the days. That gap is a fair measure of the usual '
                         'spread.'},
                 {'at': 1,
                  'kind': 'concept',
                  'title': 'Standard deviation is the typical gap to the mean',
                  'fig': 'da_std_dev',
                  'points': ['Each day sits some distance from the mean.',
                             'The standard deviation is the typical size of that distance.',
                             'For customers it is 73.7.'],
                  'say': 'The standard deviation answers a plain question. How far, on a typical day, is the customer count from the mean? The mean '
                         'is one hundred and forty three. The standard deviation is seventy three point seven, so a typical day is about seventy '
                         'four customers above or below the mean.\n'
                         '\n'
                         'A small standard deviation means the days are all alike. A big one means the days vary a lot.'},
                 {'at': 2,
                  'kind': 'wide',
                  'title': 'A fence at 9,450 flags 137 unusually large sales',
                  'fig': 'da_outlier_fence',
                  'points': ['Fence: the third quartile plus one and a half times the quartile gap.'],
                  'say': 'How big is unusually big? We use a fence. Take the third quartile, four thousand five hundred shillings, and add one and a '
                         'half times the distance between the quartiles. That puts the fence at nine thousand four hundred and fifty shillings. One '
                         'hundred and thirty seven sales land above it, and the largest is one hundred and eight thousand.\n'
                         '\n'
                         'An outlier is a value to look at before you decide anything. Check whether the sale is real.'}]},
 14: {'question': {'fig': 'da_hero_dist',
                   'alt': 'A histogram of Sunrise sale values with a box plot for each of the three shops',
                   'say': 'What does a typical sale look like, and does it differ between the three shops? A single average cannot answer that, '
                          'because sales come in many sizes. We need to see the whole shape of the values, and then see it again for each shop. '
                          'Today we draw histograms and box plots with a library called seaborn, which makes these pictures in one line, and we look '
                          'for the differences.'},
      'word_icons': {'exploratory analysis': 'magnifier',
                     'distribution': ('da_icon_hist', {'mode': 'bell'}),
                     'box plot': ('da_icon_box', {}),
                     'skewed': ('da_icon_hist', {'mode': 'skew'}),
                     'group comparison': ('da_icon_boxes', {})},
      'slides': [{'at': 0,
                  'kind': 'pair',
                  'title': 'The bin count decides how much shape you see',
                  'figs': [('da_hist_bins', {'bins': 8}), ('da_hist_bins', {'bins': 60})],
                  'captions': ['8 bins: wide bars give a rough shape.', '60 bins: narrow bars give more detail.'],
                  'say': 'A histogram sorts the values into ranges called bins. On the left we used eight wide bins, so we only see a rough shape. '
                         'On the right we used sixty narrow bins, and we see much more detail, including some jumps that the wide bars hid.\n'
                         '\n'
                         'There is no single right number of bins. Try a few, and pick the one that shows the shape clearly without turning it into '
                         'noise.'},
                 {'at': 0,
                  'kind': 'pair',
                  'title': 'A skewed distribution has a long tail on one side',
                  'figs': [('da_skew_pair', {'kind': 'balanced'}), ('da_skew_pair', {'kind': 'skewed'})],
                  'captions': ['Balanced: the mean and median are close together.', 'Skewed: a long tail pulls the mean away from the median.'],
                  'say': 'Two distributions. On the left the values spread about equally on both sides of the middle, and the mean and the median '
                         'are close. We call it balanced. On the right most values are small and a few are very large. That long tail pulls the mean '
                         'away from the median.\n'
                         '\n'
                         'The line value of a sale is skewed, with a skewness of about seven. When you see this shape, choose the median.'},
                 {'at': 1,
                  'kind': 'concept',
                  'title': 'A box plot packs the median and quartiles into a box',
                  'fig': 'da_boxplot_anatomy',
                  'points': ['The box holds the middle half of the values.',
                             'The line inside the box is the median.',
                             'Dots beyond the whiskers are outliers.'],
                  'say': 'A box plot is a histogram folded into a small shape. The box runs from the first quartile to the third, so it holds the '
                         'middle half of the values. The line inside the box is the median. The whiskers reach out toward the smallest and largest '
                         'values that are not outliers, and any dots beyond the whiskers are the unusual ones.\n'
                         '\n'
                         'Find the median, the box and one outlier on the picture.'},
                 {'at': 1,
                  'kind': 'wide',
                  'title': 'Box plots put the three shops side by side',
                  'fig': 'da_box_branches',
                  'points': ['One box for each shop makes the comparison in one glance.'],
                  'say': 'Now we draw one box for each shop on the same axis. The reader can compare the three medians, the three spreads and the '
                         'outliers in a single glance, without reading a table. The median sale is two thousand five hundred at Central Market, two '
                         'thousand at Campus Gate and two thousand five hundred at Roadside.\n'
                         '\n'
                         'Look at where the lines in the boxes sit, and at how tall the boxes are. A taller box means more variety in that shop. A '
                         'few very large sales are drawn as dots above the boxes, and the largest is one hundred and eight thousand.'},
                 {'at': 2,
                  'kind': 'concept',
                  'title': 'Each shop median is a fair way to compare shops',
                  'fig': 'da_median_branches',
                  'points': ['Compute the median for each shop.', 'Check it against the line in its box.', 'Write the finding in one sentence.'],
                  'say': 'The last step is to turn the picture into a sentence. We group by shop and ask for the median of the customers counted. '
                         'The three medians should match the lines inside the three boxes.\n'
                         '\n'
                         'Then you write one sentence that names the shops and quotes the numbers. A finding without a number is only an opinion. '
                         'Roadside has the lowest median, eighty seven customers a day.'}]},
 15: {'question': {'fig': 'da_hero_relation',
                   'alt': 'A scatter of customers against revenue, and rain against customers',
                   'say': 'Do busier days bring in more money, and does rain keep customers away? Both questions ask whether two columns move '
                          'together. Today we measure how strongly they move together with a number called the correlation. We will find that busier '
                          'days do bring in more money, and rain barely matters at all. And we will learn why a link between two columns never '
                          'proves that one causes the other.'},
      'word_icons': {'correlation': ('da_icon_corr', {}),
                     'strength': ('da_icon_strength', {}),
                     'heatmap': ('da_icon_heat', {}),
                     'hue': ('da_icon_hue', {}),
                     'cause': ('da_icon_cause', {})},
      'slides': [{'at': 0,
                  'kind': 'concept',
                  'title': 'Colour adds a third fact to a scatter plot',
                  'fig': 'da_scatter_hue',
                  'points': ['Across is one column, up is another.', 'The hue is a third column.', 'Each shop gets its own colour.'],
                  'say': 'We can add a third fact to a scatter plot without a third axis. We give each dot a colour that depends on a column, and '
                         'seaborn calls that the hue. Here each dot is a day, and the colour says which shop it belongs to. Central Market is black, '
                         'Campus Gate is red and Roadside is gold, and we keep those three colours for the rest of the course.\n'
                         '\n'
                         'Does each shop show the same upward drift? Look for a colour whose dots sit away from the others.'},
                 {'at': 0,
                  'kind': 'wide',
                  'title': 'Correlation runs from minus one to plus one',
                  'fig': 'da_corr_examples',
                  'points': ['Plus one rises together, zero shows no link, minus one moves opposite.'],
                  'say': 'The correlation squeezes the link between two columns into one number between minus one and plus one. Close to plus one, '
                         'the two rise together. Close to zero, there is no straight line link. Close to minus one, one rises while the other '
                         'falls.\n'
                         '\n'
                         'For customers and revenue in the daily summary, the correlation is zero point six two three. That is a fairly strong '
                         'upward link, though the dots do not all fall on one line.'},
                 {'at': 1,
                  'kind': 'concept',
                  'title': 'A heatmap colours every pair of columns',
                  'fig': 'da_heatmap',
                  'points': ['Each square is one pair of columns.', 'Darker means a stronger link.', 'The diagonal is always one.'],
                  'say': 'When we have many columns, a heatmap shows all the correlations at once. Each square is one pair of columns, and the '
                         'colour says how strong the link is. The diagonal is each column compared with itself, so it is always one.\n'
                         '\n'
                         'Scan for the darkest squares away from the diagonal. Those are the pairs worth a closer look with a scatter plot.'},
                 {'at': 1,
                  'kind': 'concept',
                  'title': 'Rain is weakly linked to customers (−0.16 at most)',
                  'fig': 'da_rain_corr_bars',
                  'points': ['Overall, rain and customers correlate at −0.013.',
                             'Roadside is the strongest, at −0.159, and still weak.',
                             'Central Market and Campus Gate are close to zero.'],
                  'say': 'Do customers stay home when it rains? Across all the days the correlation between rainfall and customers counted is minus '
                         'zero point zero one three. That is almost exactly zero. The bars show the same check shop by shop. Roadside is the '
                         'strongest at minus zero point one five nine, and the other two sit near zero. None of them is a strong link in either '
                         'direction.\n'
                         '\n'
                         'So in this data, rain did little to keep customers away. In your own words, say that and nothing more.'},
                 {'at': 2,
                  'kind': 'wide',
                  'title': 'Moving together does not prove one causes the other',
                  'fig': 'da_cause_umbrella',
                  'points': ['Umbrellas and wet roads both follow the rain.'],
                  'say': 'Here is a famous example. On rainy days more people open umbrellas, and the roads get wet. If we only looked at the '
                         'umbrellas and the wet roads, they would move together. But umbrellas do not wet the roads. The rain does both.\n'
                         '\n'
                         'A correlation tells you that two columns move together. It cannot tell you why. In your report, write that the columns are '
                         'linked, and leave the cause for a better experiment.'}]},
 16: {'question': {'fig': 'da_hero_clean_export',
                   'alt': 'The raw export flowing through cleaning steps into a clean table that is compared with the true revenue',
                   'say': 'If we clean the raw export carefully, does it give back the true revenue? The true revenue is six million three hundred '
                          'and seventy five thousand nine hundred shillings. We know it because we built this data ourselves. The raw file has one '
                          'thousand five hundred and thirty eight rows, with repeats, mixed dates, messy names and blanks. Today we clean it step by '
                          'step and see how close we get.'},
      'word_icons': {'parse': 'magnifier',
                     'lookup': 'book',
                     'exclude': 'cross',
                     'residual': ('da_icon_residual', {}),
                     'pipeline': ('da_icon_pipeline', {})},
      'slides': [{'at': 0,
                  'kind': 'wide',
                  'title': 'Two date styles are parsed one at a time',
                  'fig': 'da_date_formats',
                  'points': ['60 dates use slashes. The rest use year, month and day.'],
                  'say': 'The date column has two styles. Most dates are written year, month, day with dashes. Sixty are written day, month, year '
                         'with slashes. To parse a date is to read the text and turn it into a real date. A single format cannot read both styles.\n'
                         '\n'
                         'So we parse with the first format and let the failures come back as empty. Then we parse those with the second format. '
                         'Every date ends up a real date.'},
                 {'at': 0,
                  'kind': 'wide',
                  'title': 'Normalised names let one lookup match them all',
                  'fig': 'da_name_normalise',
                  'points': ['Strip spaces and fix capital letters, then look the name up.'],
                  'say': 'The product names are messy. Some have extra spaces, and some have capital letters in the wrong places. To the computer, '
                         'pen and Pen are different words. Normalising means putting every name into one agreed shape, here with spaces trimmed and '
                         'the first letters capitalised. Then a lookup against the products table finds each one.\n'
                         '\n'
                         'Compare the names before and after on the picture. How many different spellings turned into one?'},
                 {'at': 1,
                  'kind': 'wide',
                  'title': 'Words become numbers; blank units are left out',
                  'fig': 'da_units_fix',
                  'points': ['12 units written as words are converted. 40 blank units are excluded and counted.'],
                  'say': 'Twelve units are written as words, like two or three. We convert them using a small lookup, so two becomes the number two. '
                         'Forty units are blank. We cannot guess how many were sold, so we exclude those rows from the clean table and keep them in '
                         'a separate table.\n'
                         '\n'
                         'The excluded rows stay available, so we can report how many there were.'},
                 {'at': 1,
                  'kind': 'wide',
                  'title': 'A pipeline shows the row count after every step',
                  'fig': 'da_pipeline',
                  'points': ['The raw file has 1,538 rows. The clean table keeps 1,473.'],
                  'say': 'A pipeline is the cleaning steps in order. After each step we print the number of rows. The raw file starts at one '
                         'thousand five hundred and thirty eight. Dropping the twenty five repeats gives one thousand five hundred and thirteen. '
                         'Leaving out the forty blank units leaves one thousand four hundred and seventy three.\n'
                         '\n'
                         'Each count in the pipeline can be checked against the fault counts from session ten. If a number surprises you, the step '
                         'before it is where to look.'},
                 {'at': 2,
                  'kind': 'wide',
                  'title': 'The clean total is 125,400 short of the truth',
                  'fig': 'da_residual_bar',
                  'points': ['Clean: 6,250,500. True: 6,375,900. Residual: 125,400.'],
                  'say': 'After cleaning, the revenue totals six million two hundred and fifty thousand five hundred. The true figure is six million '
                         'three hundred and seventy five thousand nine hundred. The gap is one hundred and twenty five thousand four hundred '
                         'shillings, and it is called the residual.\n'
                         '\n'
                         'The residual is the revenue of the forty rows that had blank units. We left them out on purpose, so a small gap is the '
                         'honest result. Report the gap in your findings.'},
                 {'at': 2,
                  'kind': 'concept',
                  'title': 'A function lets anyone rerun the cleaning steps',
                  'fig': 'da_function_wrap',
                  'points': ['The function takes the raw table in.',
                             'It returns the clean table and the excluded rows.',
                             'Calling it twice gives the same answer.'],
                  'say': 'We wrap the whole pipeline in a function called clean sales. It takes the raw table, runs every step in order, and hands '
                         'back two tables: the clean rows and the excluded rows.\n'
                         '\n'
                         'Now cleaning is one line. A partner can run it on the same file and get the same one thousand four hundred and seventy '
                         'three rows. We check that with an assert, which stops the notebook if the number is wrong.'}]},
 17: {'question': {'fig': 'da_hero_merge',
                   'alt': 'Sales linked to a products table by a product key, with a warning about rows that multiply',
                   'say': 'Which product category earns the most, and can we trust the table that tells us? The sales table lists products by an id '
                          'number. The category lives in a different table, the products table. To answer the question we have to join the two '
                          'tables together with a merge. A merge is powerful, and it can also go wrong without any error message. Today you learn to '
                          'merge, and to check the merge before you believe it.'},
      'word_icons': {'merge key': ('da_icon_mergekey', {}),
                     'merge': ('da_icon_merge', {'mode': 'merge'}),
                     'left merge': ('da_icon_merge', {'mode': 'left'}),
                     'unique': 'check',
                     'fan-out': ('da_icon_fanout', {}),
                     'reconcile': 'calculator'},
      'slides': [{'at': 0,
                  'kind': 'concept',
                  'title': 'A merge key must pick out exactly one row',
                  'fig': 'da_unique_key',
                  'points': ['The key is the column both tables share.',
                             'In the lookup table each key appears once.',
                             'A repeated key causes trouble.'],
                  'say': 'To join two tables we need a column they share, and we call it the merge key. For sales and products the key is the '
                         'product id. The products table works like a phone book. Each id should appear once, so that each lookup gives exactly one '
                         'answer.\n'
                         '\n'
                         'Count the ids on the picture. Does any id appear twice? If it does, the merge cannot decide which row to attach.'},
                 {'at': 0,
                  'kind': 'wide',
                  'title': 'A left merge keeps every sale and adds columns',
                  'fig': 'da_merge_result',
                  'points': ['1,513 sales go in and 1,513 rows come out.'],
                  'say': 'A left merge keeps every row from the left table, the sales, and attaches the matching columns from the right table, the '
                         'products. If a sale has no match it stays, with empty cells for the new columns.\n'
                         '\n'
                         'Because every sale is kept once, the number of rows that comes out should equal the number that went in. One thousand five '
                         'hundred and thirteen in, one thousand five hundred and thirteen out. That is the first check.'},
                 {'at': 1,
                  'kind': 'wide',
                  'title': 'Repeated keys give 1,628 rows instead of 1,513',
                  'fig': 'da_fan_out',
                  'points': ['The revenue grows from 6,375,900 to 7,079,900, which is 704,000 too much.'],
                  'say': 'Here is the trap. If the products table lists one product twice, every sale of that product is attached to both copies, so '
                         'the sale appears twice. We call this a fan-out. The merged table grows to one thousand six hundred and twenty eight rows, '
                         'and the revenue climbs to seven million seventy nine thousand nine hundred shillings. That is seven hundred and four '
                         'thousand too much.\n'
                         '\n'
                         'No error appears. The only warning is that the numbers have changed, and that is why we check.'},
                 {'at': 1,
                  'kind': 'concept',
                  'title': 'A merge check stops a bad merge before it spreads',
                  'fig': 'da_validate_stop',
                  'points': ['Tell pandas how the keys should match.',
                             'If the keys break the rule, pandas stops with a MergeError.',
                             'Fix the lookup table, then merge again.'],
                  'say': 'pandas can check the merge for us. When we merge we tell it the shape we expect, which here is many sales to one product. '
                         'If a key turns out to repeat, pandas stops at once with a MergeError, instead of quietly multiplying our rows.\n'
                         '\n'
                         'An error that stops you is a gift. Read the message, fix the products table, and run the merge again.'},
                 {'at': 2,
                  'kind': 'concept',
                  'title': 'Category totals show which category earns the most',
                  'fig': 'da_category_totals',
                  'points': ['Household: 2,082,700.', 'Drinks: 1,863,200 and Stationery: 1,686,500.', 'Snacks: 743,500.'],
                  'say': 'With a safe merge we can finally answer the question. We group the merged table by category and add up the line values. '
                         'Household leads with two million eighty two thousand seven hundred shillings. Drinks follow with one million eight hundred '
                         'and sixty three thousand two hundred. Stationery has one million six hundred and eighty six thousand five hundred, and '
                         'Snacks has seven hundred and forty three thousand five hundred.\n'
                         '\n'
                         'Add the four categories. Does the total match the grand total of the sales?'},
                 {'at': 2,
                  'kind': 'wide',
                  'title': 'Rows and revenue must match after a merge',
                  'fig': 'da_rowcount_check',
                  'points': ['Same rows and same revenue before and after means the merge is safe.'],
                  'say': 'After every merge we make two checks. First, the number of rows. Second, the total revenue. We compare them with the '
                         'numbers from before the merge.\n'
                         '\n'
                         'If both are the same, we can trust the merge. If either is different, we stop, find the repeated key and fix it. '
                         'Reconciling means making two sets of numbers agree, and it is a habit worth keeping for your whole career.'}]},
 18: {'question': {'fig': 'da_hero_cp2',
                   'alt': 'One workflow: load 1,538 raw rows, clean to 1,473, merge, total by category and reconcile with the true total',
                   'say': 'Second checkpoint. Which category earns the most in the cleaned data, and by how much do our totals fall short of the '
                          'truth? You clean the raw export, merge it with the products table, and add up the categories. Then you reconcile. You '
                          'already know the pieces. Today you put them in one notebook and show that every number agrees.'},
      'slides': [{'at': 0,
                  'kind': 'concept',
                  'title': 'Checkpoint two ends with five checks that all pass',
                  'fig': 'da_cp2_checks',
                  'points': ['Count the rows kept and the rows left out.',
                             'Check the key and the merged row count.',
                             'Check the totals and name the gap.'],
                  'say': 'There are five checks, and they are the same kind of checks you would use at work. The key in the products table must be '
                         'unique. The rows kept and the rows left out must be counted. The merge must keep the same number of rows. The category '
                         'totals must add up to the clean total. And the gap to the true total must have a name, which is the revenue of the '
                         'excluded rows.\n'
                         '\n'
                         'Write each check as an assert so the notebook stops if one fails.'},
                 {'at': 2,
                  'kind': 'wide',
                  'title': 'Clean category totals fall short of the true ones',
                  'fig': 'da_category_clean_vs_true',
                  'points': ['Clean total 6,250,500 against a true total of 6,375,900.'],
                  'say': 'This chart compares each category in the cleaned data with the true value. The clean bars are a little lower, and the '
                         'whole gap is one hundred and twenty five thousand four hundred shillings.\n'
                         '\n'
                         'If your category totals add to six million three hundred and seventy five thousand nine hundred, the merge has probably '
                         'gone wrong. If they add to six million two hundred and fifty thousand five hundred, you cleaned correctly.'},
                 {'at': 2,
                  'kind': 'wide',
                  'title': 'Every step has a row count that you can explain',
                  'fig': 'da_pipeline',
                  'points': ['Raw 1,538, repeats removed 1,513, blanks excluded 1,473.'],
                  'say': 'Finish by reading your pipeline from top to bottom. Each row count has a reason. We start with one thousand five hundred '
                         'and thirty eight raw rows. Twenty five repeats come out, which leaves one thousand five hundred and thirteen. Forty blank '
                         'rows are excluded, which leaves one thousand four hundred and seventy three, and the merge changes nothing.\n'
                         '\n'
                         'If you can explain every number in that list, you have understood the checkpoint, and you are ready to start your own '
                         'project next session.'}]},
 19: {'question': {'fig': 'da_hero_plan',
                   'alt': 'Three project questions, two that the data can answer and one that it cannot',
                   'say': 'Now the project begins. Which three questions can our data answer, and how will we show the answers? Not every question '
                          'can be answered. Look at the four cards. The first three need columns that exist, so a merge, a division or a comparison '
                          'of two averages will answer them. The fourth asks why people like a shop, and no column holds an opinion. Today you '
                          'choose questions that your data can answer, and write a safe plan.'},
      'word_icons': {'project question': 'magnifier',
                     'scope': ('da_icon_scope', {}),
                     'data dictionary': 'book',
                     'limitation': 'cross',
                     'licence': ('da_icon_licence', {})},
      'slides': [{'at': 0,
                  'kind': 'wide',
                  'title': 'A good question uses columns that exist',
                  'fig': 'da_question_ladder',
                  'points': ['Start vague, then name the columns and the calculation.'],
                  'say': 'A project question gets better in steps. We start vague, such as which shop is good. Then we say what good means, for '
                         'example earning the most money. Then we name the columns we would use and the calculation, which here is total revenue by '
                         'shop.\n'
                         '\n'
                         'The final version is a question that someone could answer from the table in a few lines of code.'},
                 {'at': 0,
                  'kind': 'concept',
                  'title': 'The plan has seven headings on one page',
                  'fig': 'da_plan_page',
                  'points': ['The question, the data and its licence.', 'The columns, the charts and the checks.', 'The limitations and the risks.'],
                  'say': 'The plan lives in a file called PROJECT PLAN. It has seven headings, and it fits on one page. It names the data file and '
                         'says where it came from. It lists your three questions and, for each, the columns it needs and the chart you will draw.\n'
                         '\n'
                         'It also says what could go wrong. Your instructor approves the plan before you start, which saves you from building the '
                         'wrong thing.'},
                 {'at': 1,
                  'kind': 'concept',
                  'title': 'A data dictionary gives each column a meaning',
                  'fig': 'da_data_dictionary_card',
                  'points': ['One line for each column you use.', 'Say what it means in plain words.', 'Give the unit, such as shillings.'],
                  'say': 'A data dictionary is a short list that explains the table. For each column we write its name, what it means in plain words '
                         'and its unit. For example, units is the number of items sold in one sale, and unit price is the price of one item in '
                         'Uganda shillings.\n'
                         '\n'
                         'If you cannot write the meaning of a column, you should not build a finding on it.'},
                 {'at': 1,
                  'kind': 'concept',
                  'title': 'Read the licence at the source before using data',
                  'fig': 'da_licence_check',
                  'points': ['Read the licence at the source.',
                             'The instructor approves it and checks for personal details.',
                             'Write where it came from in your plan.'],
                  'say': 'Real data belongs to someone. The licence says how we may use it. Before using a public dataset, we go to the page where '
                         'it was published and read the licence. We check that it allows study, and we note the source and the date we downloaded '
                         'it.\n'
                         '\n'
                         'If the data is invented, like Sunrise Shops, we say so in the plan. Either way, a reader should know where the numbers '
                         'came from.'},
                 {'at': 2,
                  'kind': 'concept',
                  'title': 'Log every AI use and explain the lines you keep',
                  'fig': 'da_ai_log_card',
                  'points': ['Write what you asked and what it gave.', 'Say what you kept and why.', 'Or write: No AI assistance used.'],
                  'say': 'You may use an AI assistant for hints, as long as you keep a log. Each entry records what you asked, what came back, and '
                         'what you kept or rejected. You must be able to explain every line you keep. If you did not use an assistant, you write '
                         'that in the log in plain words.\n'
                         '\n'
                         'The log is part of your submission. It shows that the work and the understanding are yours.'}]},
 20: {'question': {'fig': 'da_hero_reliable',
                   'alt': 'The path from the raw file through the cleaning log and a calculation to a number in the report',
                   'say': 'Can a stranger follow my steps from the raw file to my numbers? Look at the path. A raw file goes in. A cleaning log '
                          'records what changed. A calculation produces a number, and a check confirms it. Only then does the number go in the '
                          'report. If any arrow is missing, a reader has to take your word for it. Today we build the analysis so that every arrow '
                          'is visible.'},
      'slides': [{'at': 0,
                  'kind': 'concept',
                  'title': 'Check one calculation against a hand example',
                  'fig': 'da_hand_check',
                  'points': ['Pick five rows.', 'Work the answer out on paper.', 'The code must give the same number.'],
                  'say': 'Before you trust a calculation on fifteen hundred rows, test it on five. Take the first five sales and work out the line '
                         'value for each by hand, units times price, then add them up. Then run the code on the same five rows. The two answers must '
                         'agree.\n'
                         '\n'
                         'If they agree, you can trust the code on the full table. If they do not, you found the mistake on a small example, where '
                         'it is easy to see.'},
                 {'at': 0,
                  'kind': 'wide',
                  'title': 'Two routes reach the same total, 6,375,900',
                  'fig': 'da_second_route',
                  'points': ['Route one adds the branch totals. Route two adds every sale.'],
                  'say': 'A second route gives you a second chance to catch a mistake. Route one adds the three branch totals. Route two adds every '
                         'sale at once. Both reach six million three hundred and seventy five thousand nine hundred.\n'
                         '\n'
                         'When two independent routes agree, the chance that both are wrong in the same way is small. That is how a second route '
                         'protects you from one slip in the first.'},
                 {'at': 2,
                  'kind': 'concept',
                  'title': 'A partner reruns your notebook from the top',
                  'fig': 'da_partner_rerun',
                  'points': ['Send the notebook and the data file.', 'The partner restarts and runs all.', 'A different number means a hidden step.'],
                  'say': 'A partner is the best test of your notebook. You send the notebook and the data file. Your partner restarts the kernel and '
                         'runs all the cells. If the numbers match yours, the notebook is reliable.\n'
                         '\n'
                         'If a number is different, the first cell where it differs is the problem. Perhaps you used a file that only exists on your '
                         'laptop. Find it and fix it.'},
                 {'at': 2,
                  'kind': 'wide',
                  'title': 'A cleaning log counts removed rows, even zero',
                  'fig': 'da_cleaning_log_card',
                  'points': ['If no change was needed, the log says so.'],
                  'say': 'The cleaning log has a line for every step you took, with the rows before and after. If your data needed no cleaning, the '
                         'log still exists. It says that you checked for repeats and blanks, and found none. The sales file from session seven has '
                         'one thousand five hundred and thirteen rows, no blanks and no repeats, so its log says no change. The raw export in '
                         'session sixteen was different, with twenty five repeats and forty blank units.\n'
                         '\n'
                         'A reader should never have to wonder whether you looked.'}]},
 21: {'question': {'fig': 'da_hero_report',
                   'alt': 'A one page chart report with its labelled parts',
                   'say': 'Does my report answer my questions without a verbal tour? Picture handing your report to someone, then leaving the room. '
                          'Everything they need has to be on the page: what is shown, which bar is largest, and what the data cannot show. Today you '
                          'build the chart report and then test it on a peer, who will tell you where they hesitated.'},
      'word_icons': {'chart report': 'bars', 'caption': ('da_icon_caption', {}), 'data source note': 'book'},
      'slides': [{'at': 0,
                  'kind': 'concept',
                  'title': 'A chart report has a title, chart, findings, limit',
                  'fig': 'da_report_anatomy',
                  'points': ['Findings sit next to their evidence.', 'A limitation says what the data cannot show.', 'A source note names the data.'],
                  'say': 'Here is the layout. At the top, a title that says what the chart shows. The chart has labelled axes with units. Beside or '
                         'below it, two findings, each with its number. Then a limitation in plain words, and finally a note that names the data '
                         'source.\n'
                         '\n'
                         'Few charts, clearly labelled, are better than many crowded ones. Keep the layout the same every time, so a reader knows '
                         'where to look.'},
                 {'at': 2,
                  'kind': 'wide',
                  'title': 'Can a peer find the largest bar in 30 seconds?',
                  'fig': 'da_30_second_test',
                  'points': ['Central Market is the largest bar, with 2,997,000.'],
                  'say': 'Give your report to a peer for thirty seconds and ask one question: which is the largest bar, and what is its total? If '
                         'your peer finds it fast, keep your headings. If your peer hesitates, write down where they looked and change that heading '
                         'or label.\n'
                         '\n'
                         'For the Sunrise report the answer is Central Market, with two million nine hundred and ninety seven thousand shillings.'},
                 {'at': 2,
                  'kind': 'concept',
                  'title': 'Save the figure before show, or it is blank',
                  'fig': 'da_savefig_flow',
                  'points': ['Draw the chart.', 'Save it with bbox inches tight.', 'Then show it.'],
                  'say': 'This is the order that works. First draw the chart. Second, call savefig with a file name. Third, call show. The show '
                         'instruction clears the figure after it displays it, so a save that comes after is saving an empty page.\n'
                         '\n'
                         'Add bbox inches equals tight to the save, and the labels stay inside the picture instead of being cut off at the edge.'},
                 {'at': 2,
                  'kind': 'concept',
                  'title': 'Take hints from an assistant, then test them',
                  'fig': 'da_ai_critique_loop',
                  'points': ['Try it yourself first.', 'Ask for a hint and keep the thinking.', 'Predict, run and test what comes back.'],
                  'say': 'An assistant can help you get unstuck, but only if you keep the thinking. Try the problem yourself first. If you are '
                         'stuck, ask for a hint. When you get an answer, predict what it will do, run it, and test it against a case you know.\n'
                         '\n'
                         'Then decide whether to keep or reject it, and say why. Write each turn in your AI log.'}]},
 22: {'question': {'fig': 'da_hero_handover',
                   'alt': 'The project folder with the notebook, report and logs inside',
                   'say': 'Does everything I submit open, rerun and agree with itself? Look at the project folder. The notebook, the cleaning log, '
                          'the data dictionary, the report and the AI log all have to open, and they all have to tell the same story. Today we check '
                          'each one against the others, and then we hand the project in. Nothing is handed in until all of them agree.'},
      'slides': [{'at': 0,
                  'kind': 'concept',
                  'title': 'Six checks decide if a project is ready to hand in',
                  'fig': 'da_handover_checklist',
                  'points': ['The notebook reruns from a restarted kernel.',
                             'Every number in the report is in an output.',
                             'Every file opens after you reopen it.'],
                  'say': 'Here are the six checks. The notebook reruns after a restart. Every number in the report appears in an output cell. The '
                         'cleaning log counts every row removed. The data dictionary covers every column you used. The AI log is filled in, or it '
                         'says that no assistance was used. And every file opens after you close it and open it again.\n'
                         '\n'
                         'Tick them one at a time. Do not tick a box you have not tested.'},
                 {'at': 2,
                  'kind': 'wide',
                  'title': 'One page holds the question, method and numbers',
                  'fig': 'da_report_page',
                  'points': ['Question, data, method, findings, recommendation and limit.'],
                  'say': 'The one page report has a fixed order. First the question. Then the data and where it came from. Then the method in a '
                         'sentence. Then your findings, each with its value. Then one recommendation. In the example it is to compare revenue per '
                         'customer counted before any decision. Last, the limit.\n'
                         '\n'
                         'The limit says there are no costs in the data, so we cannot talk about profit. A good report always closes with what it '
                         'cannot say.'},
                 {'at': 2,
                  'kind': 'concept',
                  'title': 'You have submitted when the confirmation arrives',
                  'fig': 'da_submit_route',
                  'points': ['Save, export the PDF and reopen both.', 'Upload to the folder you were given.', 'Keep the confirmation.'],
                  'say': 'Submitting has a route. Save the notebook. Export the report to PDF. Reopen both files to check they work. Upload them to '
                         'the place you were told. Then wait for the confirmation and keep it.\n'
                         '\n'
                         'A file on your laptop is not a submission. A submission is complete when the confirmation arrives, so do not close the '
                         'page until it does.'}]},
 23: {'question': {'fig': 'da_hero_talk',
                   'alt': 'A learner presenting five slides to a parent',
                   'say': 'Can a parent say what I found, how I know, and what the data cannot tell us? That is the test for your talk. Parents are '
                          'not data analysts, and they do not need to be. They need to leave knowing one clear finding and trusting it. Today you '
                          'plan the talk, you rehearse it with a timer, and you prepare for the questions you will be asked.'},
      'slides': [{'at': 0,
                  'kind': 'wide',
                  'title': 'Five slides tell the whole project',
                  'fig': 'da_talk_storyboard',
                  'points': ['One idea on each slide.'],
                  'say': 'The storyboard has five frames. My question. My data, with the number of sales, the shops and the days. What I did, in '
                         'four short words: cleaned, merged, added up and checked. What I found, with one chart. And what it cannot show. One idea '
                         'on each slide.\n'
                         '\n'
                         'If a parent can repeat the finding and the limit after your talk, the talk worked.'},
                 {'at': 2,
                  'kind': 'wide',
                  'title': 'Five minutes of talk and three of questions',
                  'fig': 'da_talk_timeline',
                  'points': ['Practise twice with a timer.'],
                  'say': 'The talk is five minutes, followed by three minutes of questions. Most of your time belongs to the finding. The question '
                         'and the data get half a minute each. What you did gets one minute. The finding gets two. The limit and the next step get '
                         'one.\n'
                         '\n'
                         'Put a timer in the corner of the room when you practise. If you run over, cut words, and keep the finding.'},
                 {'at': 2,
                  'kind': 'wide',
                  'title': 'Each parent question points to your evidence',
                  'fig': 'da_three_questions',
                  'points': ['Point to the evidence. Do not read the number from memory.'],
                  'say': 'You will get three kinds of question. Where did this number come from? You open the output cell. What did you clean? You '
                         'show the cleaning log. What can this data not tell us? You read your limitation.\n'
                         '\n'
                         'Rehearse all three with a partner. Pointing at evidence is stronger than answering from memory. Practise pointing, not '
                         'remembering.'},
                 {'at': 2,
                  'kind': 'wide',
                  'title': 'Keep a PDF and screenshots for a laptop failure',
                  'fig': 'da_backup_plan',
                  'points': ['Save the backup before the day.'],
                  'say': 'Technology fails at the worst moment. The projector might not connect, or the laptop might freeze. So you keep a backup: a '
                         'PDF of your slides and screenshots of your key outputs.\n'
                         '\n'
                         'If the live notebook fails, you explain the workflow aloud while the pictures stay on the screen. Save the backup the day '
                         'before, and test that it opens.'}]},
 24: {'question': {'fig': 'da_hero_showcase',
                   'alt': 'The showcase session as a timeline with parents attending',
                   'say': 'What can I show and explain, and what will I learn next? Today is the showcase. Parents and guardians join for the '
                          'welcome, the presentations and the certificates. You present, you answer questions, and you show that the work is yours. '
                          'Look at the bars: the presentations are the longest part before the final reflection, and that is where you shine.'},
      'slides': [{'at': 0,
                  'kind': 'concept',
                  'title': 'You make one small change unaided',
                  'fig': 'da_unaided_change',
                  'points': ['Close the assistant windows first.', 'Make the change and run it.', 'Say what changed and how you checked.'],
                  'say': 'Part of the showcase is a short live change. The instructor chooses one small change, for example filter one branch, or '
                         'change five units to ten. You close every assistant window. You make the change, run it, and say what changed and how you '
                         'checked it.\n'
                         '\n'
                         'This is the best proof that you understand your own project. Stay calm, and say your steps aloud as you go.'},
                 {'at': 2,
                  'kind': 'wide',
                  'title': 'If the notebook will not open, use the PDF backup',
                  'fig': 'da_backup_plan',
                  'points': ['The backup is part of the presentation.'],
                  'say': 'If the notebook will not open on the day, you stay calm and use the backup. Open the PDF and the screenshots, and explain '
                         'the workflow from there, step by step, while the pictures stay on the screen.\n'
                         '\n'
                         'The instructor can arrange a short live rerun afterwards if evidence is missing. Having a backup is part of doing the job '
                         'properly.'},
                 {'at': 2,
                  'kind': 'concept',
                  'title': 'Write your next goal with a first step and a date',
                  'fig': 'da_next_goal',
                  'points': ['One goal in your own words.', 'One first step you can do this week.', 'A date to do it by.'],
                  'say': 'Finish with a card. Write one goal, for example to analyse real data from a public source. Then write a first step that '
                         'you can do this week. And write by when. Use your own words and your own handwriting.\n'
                         '\n'
                         'Keep the card with your project folder. A goal with a date is far more likely to happen than a wish.'}]}}
