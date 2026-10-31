# Python for Data Analysis: class error glossary

Start list, one row per error card. Students add the errors they meet.

| You see | It means | Fix | Session |
|---|---|---|---|
| SyntaxError: invalid character | A curly quotation mark was pasted in. Python only accepts straight quotation marks. | Delete the quotation marks and type them again from the keyboard. | DA01 |
| FileNotFoundError: camp_shop.csv | The notebook cannot find the file because it sits in a different folder. | Move the notebook into the folder that holds camp_shop.csv, or ask the instructor to help. | DA01 |
| NameError: name 'price' is not defined | Python has not run a line that creates that name in this session. | Run the cell that creates the name first, and check the spelling and capital letters. | DA02 |
| TypeError: can't multiply sequence by non-int of type 'float' | You tried to multiply text by a decimal. | Convert the text with float() or remove the quotation marks. | DA02 |
| ZeroDivisionError: division by zero | You divided by zero, which has no answer. | Check the number you divide by. Change it or guard against zero in a later session. | DA03 |
| NameError: name 'units' is not defined | The name was never created in this session or is spelled differently. | Run the cell that creates it and compare the spelling letter by letter. | DA03 |
| IndentationError: expected an indented block | The line under if or else has no spaces in front of it. | Add four spaces to every line that belongs to the if. | DA04 |
| SyntaxError: invalid syntax at if budget = 5000 | A single = was used where a question needs ==. | Use == or >= to ask a question. Use = only to store a value. | DA04 |
| IndexError: list index out of range | You asked for a position beyond the end of the list. | A list of six values has positions 0 to 5. Check len(). | DA05 |
| KeyError: 'Price' | The key is not in the dictionary, often because of a capital letter. | Check the exact spelling and capitals of the key. | DA05 |
| AssertionError | The statement after assert was False, so the function gave a different answer from the one you expected. | Print the function result for that input and compare it with your hand calculation. | DA06 |
| The function shows None | The function has no return line, so it gives nothing back. | Add return in front of the value you want back. | DA06 |
| FileNotFoundError: [Errno 2] No such file: 'sunrise_sales.csv' | Python cannot find the file where it looks. | Put the notebook and the CSV in the same folder, and check the spelling of the file name. | DA07 |
| ModuleNotFoundError: No module named 'pandas' | This laptop is not using the prepared environment. | Ask the instructor. Do not install random packages. | DA07 |
| KeyError: 'unit' | The column name is spelled differently from the header. | Print list(shop.columns) and copy the exact name. | DA08 |
| The filter returns an empty table | The comparison matched no rows, often because of a typing slip in a text value. | Check the spelling and capital letters of the value you compare with. | DA08 |
| KeyError: 'revenue_ugx' | You grouped a column that has not been created yet in this session. | Run the cell that creates the revenue column before the cell that groups it. | DA09 |
| The totals do not add to the overall total | Rows were lost or counted twice before grouping. | Compare len() before and after each step to find where rows changed. | DA09 |
| SettingWithCopyWarning | You changed a slice of another table, so pandas is not sure which table you meant. | Make a real copy with .copy() before you change a table. | DA10 |
| Row counts differ between steps | A step removed or added rows without you noticing. | Print len() after every step and write the numbers in the log. | DA10 |
| The chart appears empty | plt.show() ran before the data was added, or the data was empty. | Run the cell that creates the table first and print its length. | DA11 |
| The labels on the dates overlap | There are too many labels to fit side by side. | Rotate them with plt.xticks(rotation=90) or plot fewer dates. | DA11 |
| The numbers differ after a restart | A cell relies on a value that was created in a cell that no longer runs first. | Restart the kernel and run all cells from the top. Fix the first cell that fails. | DA12 |
| The total does not match 6375900 | A filter, copy or merge changed the number of rows. | Print len() after each step and find where the count changes. | DA12 |
| TypeError: 'tuple' object is not callable | shape is a value you read. It takes no brackets, and brackets try to call it like a function. | Remove the brackets after shape. | DA13 |
| The mean from NumPy and pandas differ in the last digits | Decimals are stored with tiny rounding differences. | Compare with np.allclose, or round both to the same number of places. | DA13 |
| NameError: name 'sns' is not defined | seaborn was not imported in this session. | Run import seaborn as sns in the first cell, then run the chart cell. | DA14 |
| ValueError: Could not interpret value for x | The column name in x= or y= is not in the DataFrame. | Print list(daily.columns) and copy the exact name. | DA14 |
| KeyError: "hue" | The hue column name is not in the table. | Print list(daily.columns) and use the exact name. | DA15 |
| The heatmap shows all one colour | vmin and vmax were not set, or only one column was used. | Pass the four numeric columns and set vmin=-1 and vmax=1. | DA15 |
| ValueError: time data does not match format | A date is written in a form the format string does not describe. | Use errors="coerce" for one format and fill the gaps with the other format. | DA16 |
| The clean table has 1538 rows, not 1513 or 1473 | The duplicates were not removed before the other steps. | Call drop_duplicates() first and print len() after every step. | DA16 |
| pandas.errors.MergeError: Merge keys are not unique | validate found a key that appears more than once in the table you look up. | Find the repeated key with duplicated, fix the table, and merge again. | DA17 |
| The merged table has more rows than the sales table | A key appears twice in the second table, so rows were copied. | Compare len() before and after every merge and check the key is unique. | DA17 |
| The category totals add to 6375900, not 6250500 | The clean table was not used, or the excluded rows were put back by a merge. | Total from the cleaned table and compare with len() at each step. | DA18 |
| MergeError or a larger row count after the merge | The key is repeated in the products table. | Check is_unique on the lookup table before you merge. | DA18 |
| The plan promises profit | The data has no costs, so profit cannot be worked out. | Change the measure to revenue and say so in the limitations. | DA19 |
| A question needs a column that does not exist | The question asks for something the data never recorded. | Narrow the question to the columns you have, or choose another dataset. | DA19 |
| A calculation changes when the notebook is restarted | It depends on a value from a cell that no longer runs first. | Restart and run all. Move the first failing cell's dependency above it. | DA20 |
| The partner gets a different answer | A step uses a file path or setting that only works on your laptop. | Use paths that sit beside the notebook and state them in the first cell. | DA20 |
| The saved picture cuts off the labels | The figure was saved without room for the labels. | Add bbox_inches="tight" to plt.savefig. | DA21 |
| The picture is saved blank | plt.show() ran before plt.savefig, which clears the figure. | Call plt.savefig before plt.show. | DA21 |
| A claim in the report has no number behind it | The sentence was written from memory and not from an output. | Find the output cell that supports it, or remove the claim. | DA22 |
| The report opens but the charts are missing | The PNG was not saved in the same folder, or the picture was linked and not inserted. | Insert the saved PNG into the document and export to PDF again. | DA22 |
| The talk runs over five minutes | There are too many slides or too much code on screen. | Keep one idea per slide and cut the slide that explains the method in detail. | DA23 |
| The projector fails | The demonstration depends on a live notebook or the internet. | Use the PDF and the screenshots, and explain the workflow aloud. | DA23 |
| The notebook will not open on the day | The file or environment was not tested on the showcase laptop. | Use the PDF and screenshots, explain the workflow, and arrange a short live rerun afterwards. | DA24 |
| A question about the code cannot be answered | The student has not traced that line since they wrote it. | Say what the line is meant to do, then run it on a small input to show it. | DA24 |
