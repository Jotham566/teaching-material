# CML3113 Week 2

Each slide shows its text, then the spoken script the lecturer reads aloud.

## Slide 1: Running and saving your first notebook

Mining and Petroleum Engineering

Friday 18 September 2026
Friday 08:00–11:00, Room 105

**Spoken script**

Welcome to week two. Today we run our first notebook and learn how to save it. A notebook is a document where we write small pieces of computer instructions and see the results directly underneath them. We use Google Colab, which opens in a web browser, so nothing needs installing.

This session is for mining and petroleum engineering. By the end, each of us will have run code, saved a notebook and recorded it in an online repository. Check the date, time and room on the slide.

## Slide 2: Today’s learning

Run a code cell and find its output.

Restart, save and reopen your main notebook.

You can explain why running the same cell again may change its output.

**Spoken script**

We have two jobs today. The first is to run a code cell and find its output. A code cell is one block that holds computer instructions, and the output is the result that appears underneath it after we run it.

The second job is to restart our session, save the notebook, and open it again. Restarting means wiping the computer's temporary memory and starting fresh. Saving and reopening proves that our work survives.

At the end we show we understood by explaining one puzzle. Why can running the same cell a second time give a different answer? By the end of the lesson we can answer that in our own words.

## Slide 3: Week 2 includes your Week 1 catch-up

01

Complete A1, the Week 1 three-problems assignment, and submit it using the A1 link.

02

Take Quiz 1 when your lecturer activates it. It is separate from the A1 upload.

03

Also complete today’s A2 notebook and README, and take Quiz 2 when activated. These are four separate tasks.

**Spoken script**

Week two contains four separate tasks, and each one has its own link.

First, finish A one, the week one assignment about three engineering problems, and upload it with the A one link.

Second, take Quiz one when the lecturer activates it. It is a separate form from the A one upload.

Third and fourth, complete today's A two notebook and README, and take Quiz two once it is activated. Each quiz stays open for twenty four hours after activation. Check the deadlines on the slides that follow, and keep every confirmation message.

## Slide 4: Recall and a first attempt

A desk is 1.2 metres long. The number is 1.2 and the unit is metres. What other measurements can you describe this way?

Read the question, then follow the lecturer’s worked explanation.

**Spoken script**

Let us start with something familiar. A desk is one point two metres long. That description has two parts. The number is one point two, and the unit is metres. The number says how much, and the unit says what we are counting.

Now think of other measurements we can describe in the same way. A motor draws two amperes of current. A water tank holds five hundred litres. A steel beam has a mass of forty kilograms. A room is at twenty eight degrees Celsius. Each one is a number followed by a unit.

Hold on to this idea, because every reading we handle in notebooks has the same two parts.

## Slide 5: The engineering context

01

A pump team records temperature to investigate operation.

02

Mining students can relate this to a dewatering pump; petroleum students to a transfer pump.

03

These are teaching examples, not operating limits.

**Spoken script**

Every notebook needs a real situation behind it. Imagine a pump team that records temperature to investigate how the pump is operating. Mining students can picture a dewatering pump, which removes water from a mine. Petroleum students can picture a transfer pump, which moves fluid from one place to another.

If the temperature keeps climbing, something may be wrong with the pump. The team writes down readings over time and studies them. Our notebooks will hold readings like these.

These are teaching examples. Please do not treat any number we use in class as a real operating limit.

## Slide 6: Measurements become observations

Which object was measured? Which quantity was recorded?

**Spoken script**

A measurement becomes useful once we record it with its context. Suppose a technician reads the temperature of a motor casing and writes down forty seven degrees Celsius at ten in the morning. That single recorded reading is one observation.

Two questions help us describe any observation. Which object was measured? In our example it is the motor casing. Which quantity was recorded? It is temperature, with the unit degrees Celsius.

When many observations are collected, we get a table of data. Each row of that table is one observation. In week one we called the measured quantities features, and we will meet them again in this form.

## Slide 7: Words we will use

File

A saved item with a name. Its extension tells us the kind: .ipynb is a notebook, .csv a table, .py a Python script and .md a text document.

Folder

A container that helps you keep related files together. Extracting a ZIP restores the files inside it.

**Spoken script**

Let us fix two everyday words first. A file is a saved item that has a name. The ending of the name, after the dot, is called the extension, and it tells us the kind of file. The extension i p y n b means a notebook. C s v means a table of data. P y means a Python script, which is a text file of instructions. M d means a text document.

A folder is a container that keeps related files together. Today we receive a ZIP file. A ZIP is one package that holds many files squeezed together. When we extract it, the files inside come back out, and they sit in a folder that we can open.

## Slide 8: The files in your ZIP

01

proof_of_life.ipynb is the main class notebook.

02

Notebooks 01–04 contain errors to identify and fix.

03

hello_engineering.py shows the same idea as a script.

04

Return to proof_of_life.ipynb to finish the assignment.

**Spoken script**

Let us look at what is inside the ZIP for our course code.

The first file is proof underscore of underscore life dot i p y n b. This is the main class notebook, and it is the one we finish and submit.

Next come notebooks zero one to zero four. Each of them contains errors on purpose. Our job is to find each error and fix it, and this gives us practice reading problems.

Then there is hello underscore engineering dot p y. It shows the same idea as a script.

When the practice is done, we return to proof of life to finish the assignment.

## Slide 9: A script and a notebook

01

A .py script stores Python instructions in a text file.

02

A notebook stores code cells, explanations and saved outputs.

03

We use the notebook in Colab for this class.

04

The script is an optional comparison, not an extra upload.

**Spoken script**

There are two ways to keep Python instructions. Python is a programming language, a way of writing instructions that a computer can follow.

A script is a plain text file ending in dot p y. It holds a list of instructions, and the computer carries them out from top to bottom.

A notebook holds those instructions in cells, and it also holds our written explanations and the saved results. This makes it easy to read like a lab record.

In this class we work in the notebook, using Colab. The script is there for comparison if you are curious. It is optional, and it is not an extra upload.

## Slide 10: Opening the main notebook

01

Download the ZIP for your course code. Extract it into one folder; leave the supplied files together.

02

Open Google Colab. Choose Open notebook → Upload and select proof_of_life.ipynb.

03

Wait for the notebook page. Find one text block and one code block before clicking Run.

**Spoken script**

Now we open the notebook. There are three steps.

First, download the ZIP for your own course code. Extract it into one folder and keep the supplied files together in that folder.

Second, open Google Colab in your browser. Choose Open notebook, then Upload, and select the file proof underscore of underscore life dot i p y n b from the folder you extracted.

Third, wait for the notebook page to load. Before we click Run, we look for two things. One is a text block with explanations. The other is a code block with instructions. Finding them first tells us the notebook opened correctly.

## Slide 11: Words we will use

Python and code

Python is the language. Code is the instructions written in that language. Running asks the computer to carry them out.

Cell and output

A cell is one notebook block. A code cell runs instructions; a text cell explains them. Output is the result shown below a code cell.

**Spoken script**

Four more words will appear all day. Python is the language. Code is the set of instructions written in that language. Running means asking the computer to carry out those instructions.

A cell is one block of a notebook. A code cell holds instructions that can run. A text cell holds an explanation written for a human reader, and it runs no instructions.

Output is the result that appears just below a code cell after it runs. Suppose a code cell asks the computer to add two and two. Underneath we will see four. That four is the output.

## Slide 12: A notebook has two kinds of cell

01

A code cell contains Python instructions and a run button.

02

A text cell contains an explanation. It does not run Python.

03

The output appears below the code cell that produced it.

**Spoken script**

Every notebook is built from cells, and cells come in two kinds.

A code cell holds Python instructions. It has a small run button beside it. When we press the button, the computer reads the instructions and carries them out.

A text cell holds an explanation. We use it to tell the reader what the code is for, why we chose a certain approach, or what the result means. A text cell does not run Python, so pressing run on it only displays the formatted text.

The output always appears directly below the code cell that produced it. This keeps each result next to its cause.

## Slide 13: Cells share one Python session

A code cell runs instructions. A text cell explains them.

**Spoken script**

All the code cells in a notebook share one Python session. A session is one running period of the computer working on our notebook. Think of it as a single shared whiteboard. Whatever one cell writes on the board, every other cell can read afterwards.

This matters because cells depend on each other. If the first cell stores a number, the second cell can use that number without writing it again.

It also means that the order in which we run cells decides what is on the board at any moment. We will see this with a small example. Remember the short rule on the slide. A code cell runs instructions, and a text cell explains them.

## Slide 14: Start with numbers and values

Number

A number expresses how much or how many: 3 items or 2.5 metres. Whole numbers count; decimal numbers can describe a part of a unit.

Value and unit

A value is one piece of information. The number 2.5 is a value. A measurement also needs a unit, such as metres. Python does not attach that unit automatically.

**Spoken script**

Before we write code, let us be clear about numbers. A number says how much or how many. Three items is a count, and two point five metres is a length. Whole numbers are used for counting. Decimal numbers, with a point in them, can describe part of a unit. Two point five metres is two whole metres and half a metre more.

A value is one piece of information, and the number two point five is a value. A measurement also needs a unit, such as metres. Python stores the number only. It does not attach the unit for us, so we must remember the unit ourselves, and a good habit is to write it in a name or a comment.

## Slide 15: Give a value a name

Variable

A variable is a name referring to a value. In readings = 12, readings is the name and 12 is its initial number.

Assignment

Read = as “assign”, not “is equal to”. Python calculates the right side first, then gives that value to the name on the left. A later assignment replaces its previous value.

**Spoken script**

Computers become useful when we can give a value a name and reuse it. A name that refers to a value is called a variable.

Look at the line readings equals twelve. Here readings is the name, and twelve is the number it refers to.

The act of attaching a name to a value is called assignment. In Python the equals sign is read as assign. In Python the equals sign stores a value in a name. Python works out the right side first, then gives the result to the name on the left.

If we assign again later, the new value replaces the old one. The name keeps only the latest value.

## Slide 16: Four symbols in our first program

01

= assigns the value on the right to the name on the left.

02

+ adds numbers. print(...) displays a value.

03

# starts a comment for the person reading the code.

**Spoken script**

Our first program uses four small symbols, and each one has a simple job.

The equals sign assigns. The value on its right goes to the name on its left. So total equals six plus two stores eight under the name total.

The plus sign adds numbers. The word print followed by brackets displays a value. We write the value we want to see inside the brackets, and it appears below the cell.

The hash symbol starts a comment. A comment is a note for the person reading the code. The computer ignores everything after the hash on that line, so we can write explanations freely.

## Slide 17: The session remembers earlier values

01

The first cell assigns 12 to readings.

02

The next cell adds 5 to the value currently stored.

03

Running only the second cell again adds another 5.

**Spoken script**

Here is how the session keeps values. In the first cell we assign twelve to the name readings. The session now holds twelve under that name.

In the next cell we write an instruction that adds five to the value currently stored. The session reads twelve, adds five, and stores seventeen as the new value for readings.

Now suppose we run only that second cell again. The session reads the current value, which is seventeen, and adds five once more, giving twenty two. The session does not go back to twelve by itself. It always works from whatever value is stored at that moment, and only running the first cell again puts twelve back.

## Slide 18: Worked example

print displays a value below the cell.

= assigns the value on the right to the name on the left.

Read the code, then predict its output before running it.

```python
readings = 12
# Run the next two lines in a SECOND cell.
readings = readings + 5
print(readings)
```

**Spoken script**

Let us read this example line by line. It uses two cells.

The first cell holds one line, readings equals twelve. It stores twelve under the name readings.

The second cell has a comment first. A comment starts with the hash symbol, and it reminds us to put the next two lines in a second cell.

The next line is readings equals readings plus five. Python works out the right side first. It takes the current value of readings, twelve, and adds five to make seventeen. Then it stores seventeen under readings.

The last line is print, open bracket, readings, close bracket. It displays the current value below the cell.

So the output on the first run of the second cell is seventeen. Predict first, then run.

## Slide 19: Expected output

Which step produced this result? What changes if one input changes?

```python
17 on the first run of the second cell; 22 on its second run; 27 on its third.
```

**Spoken script**

Here is the output we should see. When we run the second cell for the first time, it displays seventeen. Run only that cell a second time, and it displays twenty two. A third run displays twenty seven.

The reason is the shared session. Each run of the second cell takes the stored value, adds five, and stores the result. So the value grows by five each time.

To check your understanding, try to say which step produced each number. Then ask what would change if the starting value were different, or if we added a different amount. If the start were ten, the first result would be fifteen.

## Slide 20: Runtime

The running Python session and its current memory. Restarting clears variables. Downloading the notebook saves the document, not the whole running computer.

**Spoken script**

The word runtime describes the running Python session together with its current memory. It is the place where our names and values live while the notebook is open.

This memory is temporary. When we restart the runtime, every variable is cleared, and we start with an empty board.

There is one more point about saving. When we download the notebook, we save the document itself, meaning the cells, the text and the outputs shown. We do not save the running computer or the values inside its memory. After reopening a notebook, we need to run the cells again to rebuild those values.

## Slide 21: Execution order changes the result

Restart, then run all cells in order before submission.

**Spoken script**

Because cells share memory, the order we run them in changes the result. Imagine we run the update cell three times and then run the setup cell. The value goes back to twelve, because the setup cell assigns twelve again.

This is why a notebook that looks fine on the page can give a different answer when someone else runs it.

The reliable check is simple. Before we submit, we restart the session, and then we run all cells in order from the top. This clears old values and follows the page order. The results we see after that are the ones a marker will see too.

## Slide 22: Tracing stored values

01

Write 12 on paper. This is the current value.

02

Add 5 and replace the old number with the result.

03

Repeat only that addition once. What value remains?

Follow the worked example and explain the result.

**Spoken script**

Let us trace the stored value with pen and paper, the same way the computer does it.

First, write twelve on your paper. This is the current value.

Second, add five, and replace the old number with the result. Cross out twelve and write seventeen.

Third, repeat only that addition once. Take the number on your paper, add five, and replace it again. What value remains on the paper?

Follow the worked example while you do this, then explain the result in your own words. Say which number was replaced at each step, and why only one number is ever on the paper.

## Slide 23: What the activity shows

22. Re-running the setup first would replace the value with 12 again.

Which step produced this result? What changes if one input changes?

**Spoken script**

The number left on the paper is twenty two. We started at twelve, added five to get seventeen, and added five again to get twenty two.

The paper holds only one number at a time, just like a variable. Each new value replaces the old one.

Now look at the second sentence on the slide. If we had run the setup cell first, the value would go back to twelve. A fresh start always begins from the setup line.

When you explain this to a neighbour, name the step that produced the result. Then say what would change if one input changed, such as starting at ten.

## Slide 24: Your turn

Restart, run the first cell once, and run the second cell twice. Write down the final number and explain why it changed.

Read the question, then follow the lecturer’s worked explanation.

**Spoken script**

It is your turn to predict. Here is the task. First restart the session. Then run the first cell once. Then run the second cell twice.

Before you press anything, work out on paper what the final number will be. Write it down. After that, run the cells and compare the screen with your prediction.

Then write one or two sentences that explain why the number changed. Use the idea that the session remembers values and each run of the second cell adds five to whatever is stored.

If your prediction and the screen disagree, trace the steps again one at a time until you find the difference.

## Slide 25: Practice discussion

22. Running the entire example from the top resets readings to 12, so a complete run ends at 17 every time.

Which step produced this result? What changes if one input changes?

**Spoken script**

The answer to the last task is twenty two. The first cell stores twelve. The second cell runs twice, so we add five twice, and we reach twenty two.

There is a second lesson on this slide. If we run the entire example from the top, the first cell runs again and puts twelve back. After that the second cell runs once, and the result is seventeen. A complete run from the top ends at seventeen every time.

So the same code can give twenty two or seventeen. The difference lies in which cells we ran and in what order. Being able to explain that is the skill we are practising.

## Slide 26: Save a copy you can find again

01

In Colab choose File → Download → Download .ipynb. Find the downloaded notebook on your computer.

02

Use File → Open notebook → Upload to reopen that file. Check your changes are present.

03

Restart the session, upload the supplied CSV again if needed, and Run all. Save the notebook again after this check.

**Spoken script**

Now we make sure our work is safe. There are three steps.

First, in Colab choose File, then Download, then Download dot i p y n b. Then find the downloaded notebook on your computer, so you know exactly where it went.

Second, use File, then Open notebook, then Upload to open that file again. Check that your changes are present.

Third, restart the session. Upload the supplied C S V file again if the notebook needs it, then choose Run all. This proves the notebook works from a clean start. Afterwards, save the notebook again so the saved version includes this check.

## Slide 27: The words in the repair exercises

Module and version

A module is a collection of Python tools. import asks for it. A version identifies a software release; different releases can behave differently.

Path and working folder

A path tells Python where a file is. A bare filename is looked up in the current working folder. The runtime Files panel shows uploaded files.

**Spoken script**

The repair exercises use four new words.

A module is a collection of ready made Python tools. The word import asks Python to load one. A version is a number that identifies a release of software. Different releases can behave differently, so the version matters.

A path tells Python where a file is stored. When we give only a file name, Python looks for it in the current working folder, which is the folder where it is working right now.

On the left of the Colab screen there is a Files panel. It shows the files we have uploaded to the session, so we can check that our file is where the code expects it.

## Slide 28: Your cohort data

01

drill_shift_log.csv

02

Reading column: depth_m

03

Keep the data file beside the notebook or upload it into the current Colab runtime.

**Spoken script**

Each cohort works with its own data file. Ours is called drill underscore shift underscore log dot c s v. It is a table of readings recorded during drilling shifts.

The reading column is called depth underscore m. The m at the end stands for metres, the unit of depth. Putting the unit in the column name reminds us what each number means, since Python will not add the unit for us.

The data file must be reachable by the notebook. Keep it in the same folder as the notebook, or upload it into the current Colab session using the Files panel.

## Slide 29: The supplied CSV-reading cell

01

The main notebook already contains the CSV-reading code. Upload the four-row Week 2 CSV, then run the cell.

02

import loads Python’s CSV tools. open opens the named file; DictReader uses its header as field names. list collects the rows; len counts them.

03

Keep the supplied code. Weeks 3–4 explain how to write these operations yourself.

**Spoken script**

The main notebook already contains a cell that reads the data file. A C S V file is a plain table where values are separated by commas. We upload the four row Week 2 file first, and then run the cell.

Let us read what the code does in words. Import loads Python's C S V tools. Open opens the file we name. Dict reader reads the file and uses the first row, the header, as the names of the fields. List gathers the rows into one collection, and len counts how many there are.

We keep this supplied code as it is. In weeks three and four we learn how to write these operations ourselves.

## Slide 30: The four repair exercises

01

Identify the deliberately unavailable module.

02

Compare the required and actual Python versions.

03

Locate the CSV and correct its file path.

04

Trace the values and remove the unwanted reset.

**Spoken script**

There are four repair exercises, and each one teaches a different habit for fixing a problem.

Exercise one asks us to find the module that is deliberately unavailable. Python will tell us it cannot find a module, and we must spot which one.

Exercise two asks us to compare the Python version the notebook requires with the version we actually have.

Exercise three asks us to locate the C S V file and correct its path, so Python looks in the right place.

Exercise four asks us to trace the values and remove an unwanted reset, which is a line that puts a value back to its starting number at the wrong time.

## Slide 31: Repository and commit

A repository stores a project and its recorded changes. A commit records a change with a message. Git tracks history; GitHub hosts repositories online.

**Spoken script**

Two more words belong to this part of the lesson. A repository is a place that stores a project together with a record of its changes. Think of it as a project folder that remembers its history.

A commit is one recorded change, saved with a short message that says what changed. If we edit a file and commit it, the repository keeps both the old version and the new one.

Git is the tool that tracks this history. GitHub is the website that hosts repositories online. So Git does the remembering, and GitHub gives that memory a home on the internet.

## Slide 32: Record a change in your repository

01

Sign into GitHub. Create a repository: the project folder with recorded history. Use an appropriate private setting for personal work.

02

Choose Add file → Upload files. Add the notebook, supplied CSV and README.md. A README is a text file containing your run instructions.

03

Write a short message describing the change and choose Commit changes. A commit records this version of the files.

04

Open the file list to confirm the files arrived. Copy the repository page URL for the assignment form.

**Spoken script**

We now record our work in a repository using only the browser. There are four steps.

First, sign in to GitHub and create a repository. Choose a private setting, which keeps personal work visible only to you.

Second, choose Add file, then Upload files. Add the notebook, the supplied C S V and your README dot m d. A README is a text file that tells a reader how to run your project.

Third, write a short message describing the change, and choose Commit changes. This commit records this version of the files.

Fourth, open the file list to confirm the files arrived. Then copy the address of the repository page, because the assignment form asks for it.

## Slide 33: Short explainer and discussion

01

CodeWithChris
GitHub Tutorial for Beginners (2025)

02

00:00–02:10, then 03:35–06:08 (4 min 43 sec total)

03

Listening question: Why keep history, and what is a repository?

Open explainer video

https://www.youtube.com/watch?v=v5gnvDUWqFM

**Spoken script**

We now watch a short video from CodeWithChris called GitHub Tutorial for Beginners. We watch two parts only. The first runs from the start to two minutes ten seconds. The second runs from three minutes thirty five seconds to six minutes eight seconds. Together they last about four minutes forty three seconds.

While it plays, keep one question in mind. Why do we keep history, and what is a repository? After the video we answer it together. The link is on the slide if you want to watch again later.

## Slide 34: After the video

Explain the difference between saving a file and recording a commit. Then make one browser-based commit.

Read the question, then follow the lecturer’s worked explanation.

**Spoken script**

Let us use what we saw. The task has two parts.

First, explain the difference between saving a file and recording a commit. Saving a file writes its current content to a place on a disk or online. A commit goes further. It records that version together with a message, and the repository keeps it in its history alongside earlier versions.

Second, make one browser based commit yourself, following the steps on the earlier slide. Use a short message that says what changed, such as adding the notebook.

When you finish, look at your repository page and find the commit you made in the list.

## Slide 35: Preparing for the assignment

01

Use proof_of_life.ipynb for A2.

02

Upload the cohort CSV into the runtime Files area and show the filename before reading it.

03

Follow repair 01, then try the same approach in 02–04.

04

Submit the completed main notebook and your own README.md together, plus the repository URL.

**Spoken script**

Here is how to prepare for assignment A two.

First, use the file proof underscore of underscore life dot i p y n b as your notebook.

Second, upload the C S V for your cohort into the Files area of the session. Show the file name there before the code reads it, so we can see that the file is present.

Third, follow repair exercise one, then try the same approach in exercises two to four. The method is the same each time. Read the error, find the line, and fix the first cause.

Fourth, submit the completed main notebook and your own README dot m d together, plus the repository address.

## Slide 36: Preparing for the assignment continued

01

Repairs 01–04 and hello_engineering.py are practice, not extra submissions.

**Spoken script**

One more point about what to submit. The four repair notebooks and the hello underscore engineering script are practice material. They help us learn, and they are never extra submissions.

The only files that go in the A two form are the completed main notebook and your own README, plus the repository address. If you are unsure whether a file belongs in the form, check the previous slide for the list.

## Slide 37: Execution order and saved changes

01

The number beside a code cell records when it ran in that session, not its position on the page.

02

Restart clears memory; Run All follows page order.

03

A fresh run tests the run order, not whether the engineering formula is valid.

04

A commit is a recorded change.

**Spoken script**

Four ideas close this section.

The small number beside a code cell records the order in which cells ran during this session. Position on the page is a separate matter, so a cell near the bottom may carry a lower number if we ran it earlier.

Restart clears the memory. Run all then runs every cell in page order, from top to bottom.

A fresh run tests whether the order of the cells works. It does not tell us whether an engineering formula is valid. We need to check that separately.

Finally, a commit is a recorded change. It is our history of the work.

## Slide 38: Execution order and saved changes continued

In terminal reference material, git status describes local changes; it does not itself save or upload them.

**Spoken script**

Some guides show commands typed into a terminal. A terminal is a window where we type instructions as text. We do not use one today.

One of those commands is git status. It describes the local changes in your folder, meaning which files have been edited since the last commit. It only reports. It does not save your files, and it does not upload them.

So seeing a list of changed files from git status is a description of the situation. To record the changes we still need a commit, and to place them online we need to send them to GitHub. Today the browser upload takes care of both.

## Slide 39: A1 — what to write and submit

01

Describe three engineering problems. For each, state what you would measure or classify and whether machine learning is suitable.

02

List possible inputs, the target where appropriate, a data source and one limitation for each problem. Choose one problem and dataset and justify your choice.

03

Write one complete report in DOCX or selectable-text PDF. PPTX with narration notes or notebook evidence is also accepted. Upload through the A1 form; keep its confirmation.

**Spoken script**

Assignment A one is a short report that frames problems. We are proposing a study, and we do not train any model.

First, describe three engineering problems. For each one, say what you would measure or classify, and whether machine learning suits it.

Second, for each problem list possible inputs, the target where it applies, a source of data, and one limitation. Then choose one problem and its dataset, and justify the choice.

Third, write one complete report. A Word document or a P D F with selectable text is accepted. A PowerPoint with narration notes or notebook evidence is also accepted. Upload it through the A one form, and keep the confirmation.

## Slide 40: Week 1 Assignment A1 catch-up upload

01

Submit A1 separately from the A2 notebook and README.

02

Deadline: 25 Sep 2026, 08:00 Kampala.

03

Enter your own Student Registration Number; the required field accepts any format.

Open Week 1 A1 assignment form

https://docs.google.com/forms/d/e/1FAIpQLSc7TlczqFeKIMIT4fVxzIp5iZqi07l4b1tGOavTzBN5-nna4A/viewform

**Spoken script**

This slide is the upload point for the week one report. Submit A one separately from the A two notebook and README. They use different forms.

Check the deadline on the slide. When you open the form, enter your own Student Registration Number. The field is required and accepts any format.

Wait until the file names appear in the form, then press Submit. Keep the confirmation you receive.

## Slide 41: Week 1 Quiz 1 catch-up

01

Quiz 1 is required catch-up work, separate from A1.

02

Complete it individually after lecturer activation.

03

It closes 24 hours after activation, not at the assignment deadline.

04

Press Submit and keep your confirmation.

Open Week 1 Quiz 1

https://forms.gle/yMVr6wzmyFqNUESv8

**Spoken script**

Quiz one is required catch-up work from week one. It is separate from A one, so finishing one does not complete the other.

Answer it individually. The quiz opens when the lecturer activates it, and it then stays open for twenty four hours. That window is the closing rule for this quiz, and it is unrelated to the assignment deadline.

When you finish, press Submit and keep the confirmation. The link is on the slide.

## Slide 42: Week 2 assignment

01

Complete proof_of_life.ipynb and write your own README.md.

02

The README states your programme, file list and run instructions.

03

Include the repository URL in the form.

04

Upload the renamed notebook and README, not the ZIP or 01–04 repair notebooks.

**Spoken script**

This slide lists what assignment A two requires.

First, complete proof underscore of underscore life dot i p y n b, and write your own README dot m d.

Second, the README states your programme, lists your files, and gives instructions for running the notebook. A reader who has never seen your work should be able to follow it.

Third, include the repository address in the form.

Fourth, upload the renamed notebook and your README. The ZIP and the four repair notebooks stay out of the upload.

## Slide 43: Proof of life submission

01

Opens: 18 Sep 2026, 08:00 Kampala

02

Deadline: 25 Sep 2026, 08:00 Kampala

03

Use your full Student Registration Number in the form.

04

Keep the submitted files and confirmation.

Open W02 assignment form

https://docs.google.com/forms/d/e/1FAIpQLSf5sCKyFfSZ0Xxo8bU_bQCVYDZ5ESgeGf3logWsIfJ9y5PUIg/viewform

**Spoken script**

This is the upload point for assignment A two. Check the opening time and the deadline on the slide.

In the form, use your full Student Registration Number. Attach the completed notebook and your README, and paste the repository address.

When the file names appear, press Submit. Keep the submitted files and the confirmation message, since they are your proof that the work was received.

## Slide 44: Week 2 quiz

01

Answer individually after the lecturer activates the quiz.

02

Available for 24 hours from activation.

03

Use your Student Registration Number and registered account.

04

Check the announced quiz closing time.

Open this week’s quiz

https://forms.gle/98nRi1kV2tLjPzZw7

**Spoken script**

The week two quiz opens when the lecturer activates it. After activation it stays open for twenty four hours, so check the announced closing time.

Answer it individually. Use your Student Registration Number and the Google account you registered with. The link is on the slide.

## Slide 45: Before you leave

You can explain why running the same cell again may change its output.

Check that the required files are in place.

Point to your evidence. Save your work.

**Spoken script**

Before you leave, we check two things on our own.

First, can you explain why running the same cell again may change its output? Use the idea of shared session memory. Each run uses whatever value is stored at that moment.

Second, save your work and check the files that the submission needs. That means the notebook you completed and your own README. Open the folder and make sure they are there, and that the saved notebook is the latest one.

Point to your evidence on screen and be ready to say what each file is for.
