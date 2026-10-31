# Machine Learning: class error glossary

Start list, one row per error card. Students add the errors they meet.

| You see | It means | Fix | Session |
|---|---|---|---|
| SyntaxError or invalid character | A quotation mark is curly, usually from copying out of a document. | Retype the quote marks with the keyboard so they are straight. | ML01 |
| ModuleNotFoundError: No module named 'sklearn' | This laptop is not using the prepared camp environment. | Tell the instructor. Do not install anything yourself. | ML01 |
| NameError: name 'price' is not defined | Python has not run a line that creates that name in this session. | Run the cell that creates the name first, and check the spelling and capital letters. | ML02 |
| TypeError: can't multiply sequence by non-int of type 'str' | You tried to multiply two pieces of text. | Remove the quotation marks around the number. | ML02 |
| ValueError: could not convert string to float | The text has letters, a comma or a currency symbol inside it. | Remove everything except digits and one decimal point. | ML03 |
| ZeroDivisionError: division by zero | The calculation divides by zero. | Check the number you divide by; it must not be 0. | ML03 |
| IndentationError: expected an indented block | The line after if, elif or else does not start with spaces. | Add four spaces at the start of each line inside the block. | ML04 |
| SyntaxError: invalid syntax | A colon is missing at the end of an if, elif or else line. | Put a colon at the end of the line. | ML04 |
| IndexError: list index out of range | You asked for a position the list does not have. | A list of 3 items has positions 0, 1 and 2. | ML05 |
| KeyError: 'price' | The dictionary has no key spelled like that. | Check the exact spelling and capital letters of the key. | ML05 |
| TypeError: total() missing 1 required positional argument | You gave the function fewer values than it has parameters. | Give one argument for each parameter. | ML06 |
| The answer shows None | The function has no return line, so nothing came back. | Add return before the value you want back. | ML06 |
| FileNotFoundError: No such file or directory | The CSV file is not beside the notebook. | Move the file into the same folder as the notebook, or ask the instructor. | ML07 |
| ModuleNotFoundError: No module named 'pandas' | The prepared camp environment is not active. | Tell the instructor. Do not install packages. | ML07 |
| KeyError: 'unit' | The column name is spelled differently from the header. | Print the headers with list(shop.columns) and copy the exact name. | ML08 |
| The filter returns an empty table | The comparison matches no rows, often because of a typo in a text value. | Check the spelling and capital letters of the value you compare with. | ML08 |
| NameError: name 'np' is not defined | numpy was not imported in this notebook session. | Run import numpy as np first. | ML09 |
| The proportion is above 1 | You divided the whole by the part. | Divide the part by the whole. | ML09 |
| FileNotFoundError when reading the log back | to_csv did not run, or ran in another folder. | Run the to_csv line again and check the file list in Jupyter. | ML10 |
| KeyError: 'price' | The column name has a different spelling in this table. | Print list(raw.columns) and copy the exact name. | ML10 |
| NameError: name 'sns' is not defined | seaborn was not imported in this session. | Run import seaborn as sns first. | ML11 |
| The chart does not appear | The cell that draws it has not run, or plt.show() is missing. | Run the import cell, then run the drawing cell again. | ML11 |
| The notebook works only until I restart it | A later cell uses a name that an earlier cell created and you deleted. | Restart the kernel and run all cells from the top to find the missing step. | ML12 |
| The totals do not agree | A filter or a typo dropped rows before grouping. | Compare the row counts before and after each step. | ML12 |
| NameError: name 'X' is not defined | The cell that creates X has not run yet. | Run the cells in order from the top. | ML13 |
| KeyError: 'area' | The column is called area_m2 in this file. | Print homes.columns and copy the exact name. | ML13 |
| ValueError: Expected 2D array, got 1D array instead | The model needs a table of inputs, with rows and columns, and got a flat list. | Use double brackets, such as [[35]], or select with homes[["area_m2"]]. | ML14 |
| ModuleNotFoundError: No module named 'sklearn' | The prepared camp environment is not active. | Tell the instructor. Do not install packages. | ML14 |
| KeyError: "['rooms'] not in index" | The column name is spelled differently from the header. | Print homes.columns and copy the exact name. | ML15 |
| The two errors are the same | The model and baseline were scored on the same predictions, or the wrong table was used. | Check that each uses its own predict call on X_test. | ML15 |
| ValueError: could not convert string to float | A category name was passed where numbers are needed. | Use iris.target for the labels and iris.data for the inputs. | ML16 |
| NameError: name 'iris' is not defined | The cell that loads iris has not run. | Run the cells in order from the top. | ML16 |
| The two kinds of mistake sit in the wrong cells | The axes were read the wrong way round: rows are actual, columns are predicted. | Label both axes before reading any cell. | ML17 |
| The matrix has actual and predicted swapped | The two lists were passed to confusion_matrix in the wrong order. It expects the actual values first and the predicted values second. | Write confusion_matrix(actual, predicted) and check that the row totals match the real class counts. | ML17 |
| The final accuracy was calculated before the choice | The final test was used while deciding the depth. | Mark that result as validation and use the instructor's alternate holdout for the final. | ML18 |
| ValueError: The least populated class in y has only 1 members | stratify was given labels that are too few. | Check that y is the full label list. | ML18 |
| KeyError: 'tip' | The column is called tip_ugx. | Print fares.columns and copy the exact names. | ML19 |
| The plan promises too much | It asks for real people's data, an app or a neural network. | Reduce it to one supplied table, one target and one baseline. | ML19 |
| Baseline and model score exactly the same | Both scores were computed from the same predictions, so the baseline is not a separate guess. | Build the baseline from the training mean alone and score the model with its own predict, both on X_val and y_val. | ML20 |
| ValueError: Found input variables with inconsistent numbers of samples | X and y have different lengths because one was filtered and not the other. | Create X and y from the same table at the same step. | ML20 |
| The with-tip score looks like the best | A leakage column made the model look better. | Remove the column that is only known after the answer. | ML21 |
| The comparison changes every time I run it | The split uses different random_state values or none at all. | Use the same split settings for every model. | ML21 |
| NameError after restarting the kernel | A cell used a name that was only created in a deleted or skipped cell. | Run all cells from the top and add the missing step. | ML22 |
| The final score differs from last time | The split or the model settings changed. | Use the same random_state and settings as in validation. | ML22 |
| The slides run over five minutes | There are more than five ideas. | Keep one idea per slide and cut the rest. | ML23 |
| The demonstration does not run | The notebook was not restarted or the data file was moved. | Show the screenshot backup and explain the steps. | ML23 |
| The change breaks the notebook | A name or a cell order changed. | Restart, run all cells, then read the last line of the error. | ML24 |
| The demonstration is too long | More than one idea per slide. | Use the five slides and leave the extra detail for questions. | ML24 |
