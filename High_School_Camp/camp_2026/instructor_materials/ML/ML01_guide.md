# ML01 Instructor guide: Your first instruction and your first prediction

Private. Keep this file out of the student folder.

**Objective.** By the end: you can run, save and reopen a notebook, and you can say what a prediction is using the rent example.

**Question of the day.** Can a computer guess a rent after seeing 120 homes?

**Where this is used.** Property apps and agents guess a fair rent from the size and area of a home. A model does the same after studying homes that were already rented, and today you build the smallest version. What rent would you guess for a home you know?

Prerequisite: START_HERE.md.

## The 180 minutes

| Minutes | Activity |
|---|---|
| 10 | Recall: retrieve yesterday, three questions on paper |
| 50 | Block A: predict, run, investigate, modify |
| 15 | Break away from screens |
| 50 | Block B: predict, run, investigate, modify |
| 40 | Make: the independent task and the project journal |
| 15 | Exit ticket, save, and an individual check with each learner |

Where it overruns: Laptop and environment problems can use the first 20 minutes. Keep block B short and finish with the rent estimate for 80 square metres.

## Block A. Run your first instruction

Open ML01.ipynb in Jupyter. Click the first code cell and press Shift+Enter.

Ask for the prediction first: Write on paper what you think these two lines will show.

```python
print("Hello, data")
print(3 + 2)
```

Correct result: The first line shows Hello, data and the second shows 5. A notebook is a page of text cells and code cells. Shift+Enter runs a code cell and its output appears underneath. print is a ready-made instruction, and the brackets hold what it shows.

Investigate, with answers:

- What happens if you click a text cell and press Shift+Enter? Answer: Nothing runs. A text cell only explains; only a code cell runs Python.
- Why does Hello, data sit inside quotation marks while 3 + 2 does not? Answer: Quotation marks tell Python the characters are text. Without them Python calculates.

Modify: Change Hello, data to your own nickname and run the cell again. Answer: The first line now shows your nickname.

## Block B. Run a ready-made prediction

This model has looked at 120 invented homes and learned how rent follows floor area. You do not need to understand it yet. Session 13 opens it up.

Ask for the prediction first: Before you run it, write the monthly rent in UGX you expect for a home of 50 square metres.

```python
import pandas as pd
from sklearn.linear_model import LinearRegression
homes = pd.read_csv("synthetic_homes.csv")
model = LinearRegression().fit(homes[["area_m2"]], homes["rent_ugx"])
pred = model.predict(pd.DataFrame({"area_m2": [50]}))[0]
print("Estimated rent for 50 square metres:", round(pred))
```

Correct result: The model estimates about UGX 309,260 a month. It drew a line through the 120 homes and read the rent at 50 square metres. Guessing a number from examples is called regression, and you will build one yourself in session 14. The homes are invented, so the estimate says nothing about real rents.

Investigate, with answers:

- The home grows from 50 to 100 square metres. What do you expect the estimate to do? Answer: It rises. A 50 square metre increase adds about UGX 150,000 here.
- Is the estimate certain? Answer: No. It is a guess from 120 invented homes and can be wrong for any real home.
- Does this model know anything about Kampala? Answer: No. It only knows the 120 invented rows in the file.

Modify: Change 50 to 100 and run the cell again. Answer: The estimate becomes about UGX 459,084.

```python
pred100 = model.predict(pd.DataFrame({"area_m2": [100]}))[0]
```

## Make: reference

```python
import pandas as pd
from sklearn.linear_model import LinearRegression
print("Amina")
print(7 + 4)
homes = pd.read_csv("synthetic_homes.csv")
model = LinearRegression().fit(homes[["area_m2"]], homes["rent_ugx"])
pred80 = model.predict(pd.DataFrame({"area_m2": [80]}))[0]
print(round(pred80))
```

Build log entry to look for: ML01.ipynb with a nickname, 11, and a rent estimate for 80 square metres, reopened and saved.

## Misconceptions to listen for

- A model that gives a number must be correct.
- An error message means I broke the computer.
- The notebook runs by itself when I type.

## Questions to ask, with expected answers

- What did the model need before it could guess a rent? Expected: Examples: the 120 homes with their areas and rents.
- Why should we distrust the estimate? Expected: The homes are invented, and nobody has tested the model yet.

## Online version

For a hybrid group. The live class is 90 minutes on video with screen sharing. The learner finishes the build in their own time, about an hour. The full rules are in handbook/HYBRID_DELIVERY.md.

### Live clock, 90 minutes

| Minutes | Activity |
|---|---|
| 5 | Welcome, camera and sound check, and a notebook that opens |
| 35 | Block A, Run your first instruction: predict, run, investigate. The Modify step moves to the build task. |
| 5 | Break away from the screen |
| 35 | Block B, Run a ready-made prediction: predict, run, investigate. The Modify step moves to the build task. |
| 10 | Close: say the exit sentence aloud, then the build task is set |

### After-class build task, about an hour

1. Modify, Block A (Run your first instruction): Change Hello, data to your own nickname and run the cell again.
2. Modify, Block B (Run a ready-made prediction): Change 50 to 100 and run the cell again.
3. Make: In a new code cell print your nickname and the result of 7 + 4. In another cell estimate the rent for 80 square metres. Save as ML01.ipynb, close it and reopen it. On your progress map, write one topic you love, such as football, music or farming. It will grow into your project. With the instructor, read AI_USE_POLICY.md: in weeks 1 to 6 all core work is your own, with no AI-generated solutions.

When you finish, write two sentences: what you changed and how you checked it. Add a build log entry. Send a photo of your work or the notebook by the route the organiser sets, before the next class.

### Next class

In the next class recall, ask: What did the model need before it could guess a rent? Expected: Examples: the 120 homes with their areas and rents.

## Build log and feedback

Look at what each of the five learners saved and note one strength and one next step for each. Share them kindly and privately. Nothing is scored or ranked. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and show-and-tells need your judgement.
