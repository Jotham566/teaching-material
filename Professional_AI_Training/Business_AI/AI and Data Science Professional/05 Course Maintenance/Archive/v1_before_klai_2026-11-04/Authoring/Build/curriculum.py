"""Single source of truth for the AI and Data Science Professional course.

24 sessions x 2 hours = 48 hours. Students: working professionals, confident in Excel, no code, no statistics.
Tools: every tool is free for learner and tutor (see TOOLS). Mixed Windows and Mac laptops; browser first.

Every other file (roadmap, plan, decks, notebooks, verification) reads this module.
"""

COURSE = dict(
    title="AI and Data Science Professional",
    sessions=24, hours_per_session=2, total_hours=48,
    start="Confident in Excel or Google Sheets. No code. No statistics.",
    end="Can take a business question from raw data to a tested model or analysis, explain it to a manager, and run it as a small app, using only free tools.",
)

# The 2-hour session shape. Minutes sum to 120.
SESSION_SHAPE = [("Recall and warm-up", 10), ("Concepts and explanation", 30), ("Live demonstration", 25), ("Break", 5), ("Guided lab", 40), ("Check and wrap-up", 10)]

MODULES = [
    ("A", "Think with data", range(1, 5), "No code. Sheets and reasoning."),
    ("B", "Python for data", range(5, 10), "Python, pandas and first SQL in the browser."),
    ("C", "Analyse and explain", range(10, 14), "SQL, charts, inference and regression."),
    ("D", "Machine learning", range(14, 20), "Build, test and judge models."),
    ("E", "Neural networks and text", range(20, 23), "Neural networks, text, embeddings and language models."),
    ("F", "Ship it and present", range(23, 25), "Save a model, publish a small app, govern it and present."),
]

# Free tools, standard in industry. 'verified' = licence or free-use terms confirmed by search on 28 Oct 2026; 'check' = to confirm before class.
TOOLS = [
    dict(name="Google Colab", use="Run Python notebooks in the browser. Nothing to install.", cost="Free tier. Needs a free Google account. GPU not needed for this course.", status="verified", note="Google does not publish its limits; reports give an idle disconnect of about 90 minutes and a longest session of about 12 hours. Save to Drive or GitHub."),
    dict(name="Google Sheets (or Excel, or LibreOffice Calc)", use="Sessions 1 to 4 and every Excel comparison.", cost="Free. Any spreadsheet works.", status="verified", note="Excel is used if students already own it."),
    dict(name="Python 3 with pandas, NumPy, SciPy, statsmodels, scikit-learn, matplotlib, seaborn", use="The data science stack.", cost="Free, open source (BSD or PSF licences).", status="verified", note="All preinstalled in Colab."),
    dict(name="SQLite (inside Python)", use="SQL practice with no server.", cost="Free, public domain.", status="verified", note="Included in Python. DB Browser for SQLite is optional."),
    dict(name="Git and GitHub Free", use="Save work, share a portfolio, deploy the app.", cost="Free account.", status="verified", note="Public repositories for the course."),
    dict(name="Streamlit and Streamlit Community Cloud", use="Turn a model into a small web app.", cost="Free for public apps.", status="verified", note="Apps sleep after 12 hours without visitors."),
    dict(name="TensorFlow Playground", use="See a neural network learn, in the browser.", cost="Free, Apache licence, no login.", status="verified", note="Web page only."),
    dict(name="sentence-transformers (all-MiniLM-L6-v2)", use="Turn text into vectors for search and similarity.", cost="Free. Apache 2.0.", status="verified", note="Downloads about 90 MB once in Colab. No API key, no hosted service."),
    dict(name="A small open language model run inside Colab (for example Qwen2.5-0.5B-Instruct)", use="Show how a language model answers, with nothing sent to a vendor.", cost="Free.", status="check", note="Confirm the licence on the model card before class. Optional; the session still works with embeddings alone."),
    dict(name="Any free chat assistant the student already has", use="Explain errors, suggest code, critique drafts.", cost="Free tiers; limits change.", status="check", note="Never required. Every lab runs without one."),
    dict(name="Visual Studio Code (optional local setup)", use="Local editing once students outgrow Colab.", cost="Free to use.", status="verified", note="Optional only."),
]
AVOIDED = [
    ("Anaconda Distribution and Miniconda", "Free for individuals, but organisations with 200 or more staff need a paid licence under the 2024 terms, which includes government and non-profits. Miniconda's installer is free, but its default package channel falls under the same terms. Use Colab, or python.org with venv, or Miniforge."),
    ("Hugging Face hosted inference", "Free accounts stopped receiving included monthly inference credits on 7 October 2026 (reported by several sources). Models are downloaded and run inside Colab instead."),
    ("Power BI Desktop", "Windows only, which fails on mixed laptops. Charts are made in Python and Sheets; a free browser dashboard tool is optional."),
    ("Docker Desktop and paid cloud GPUs", "Not needed. Deployment uses Streamlit Community Cloud."),
    ("Paid AI APIs", "Any lab needing a paid key would break the no-cost rule."),
]

# Roadmap.sh AI and Data Scientist stages (from the roadmap PDF and aligned curricula) -> sessions that cover them, and how deeply.
ROADMAP_COVERAGE = [
    ("Mathematics", "Intuition only: slope, area, vectors, matrices as tables. No proofs, no hand calculation.", [4, 13, 20], "light"),
    ("Statistics", "Distributions, sampling, confidence intervals, hypothesis tests, A/B tests, correlation.", [3, 4, 12], "core"),
    ("Econometrics", "Linear and logistic regression, time series and forecasting basics.", [13, 15, 19], "core"),
    ("Coding", "Python, pandas, SQL. Data structures and interview algorithms are left out on purpose.", [5, 6, 7, 8, 9, 10], "core"),
    ("Exploratory data analysis", "Cleaning, charts, summary, communication.", [2, 3, 8, 11], "core"),
    ("Machine learning", "Supervised, unsupervised, ensembles, evaluation, leakage.", [14, 15, 16, 17, 18], "core"),
    ("Deep learning", "Neural networks, one pretrained model. No training from scratch on images.", [20], "light"),
    ("MLOps", "Save a model, version code, deploy an app, watch for drift. No Docker or cloud.", [23], "light"),
    ("AI engineering", "Text vectors, search, a retrieval pattern with a small local model.", [21, 22], "core"),
    ("AI-assisted coding", "An assistant is used and its code is checked in Sessions 5, 6 and 22. It is never required.", [5, 6, 22], "core"),
]

# Each session. 'topics' are the planned concept and demo slides (the content authors expand them).
S = []
def add(**k): S.append(k)

add(no=1, module="A", title="What data science is and how to think in it",
    question="What does a data scientist do, and what will you be able to do after 24 sessions?",
    result="A working Colab account, a mapped lifecycle and one business question of your own.",
    dataset="Lakeside Mart", tools=["Google Sheets", "Google Colab"], code=False,
    outcomes=["Describe the data science lifecycle from question to decision.", "Separate data science, machine learning and AI by what each produces.", "Open Colab and run one cell."],
    topics=["Roles: analyst, scientist, ML engineer", "The lifecycle: question, data, clean, explore, model, deliver, monitor", "AI, machine learning and data science, one picture", "A business question worth asking", "Free toolset tour", "First Colab cell: run, read, save"],
    lab="Write your own question; open Colab; run a cell that prints a sentence and a sum.",
    maps=dict(roadmap="Intro", ibm="What is Data Science? and Tools for Data Science", google="Foundations of Data Science", other="AI for Everyone weeks 1 and 2"))
add(no=2, module="A", title="Data as tables: rows, columns and grain",
    question="What exactly is one row, and how does one table connect to another?",
    result="A data dictionary for the Lakeside Mart tables and one grain statement per table.",
    dataset="Lakeside Mart", tools=["Google Sheets"], code=False,
    outcomes=["State the grain of a table.", "Tell numeric, category, date and text columns apart.", "Link two tables through a key."],
    topics=["Row, column, cell, table", "Grain: what one row means", "Variable types and why they matter", "Keys and relationships", "Messy data you will meet", "Reading a data dictionary"],
    lab="Open the six Lakeside Mart tables in Sheets; write the grain and key for each; spot three problems.",
    maps=dict(roadmap="EDA", ibm="Data Science Methodology", google="Ask Questions to Make Data-Driven Decisions", other="Kaggle Learn: Data Cleaning (concepts)"))
add(no=3, module="A", title="Summarising and showing data honestly",
    question="How do we describe thousands of rows in one sentence and one chart without misleading anyone?",
    result="A pivot table and two clear charts from Lakeside Mart sales.",
    dataset="Lakeside Mart", tools=["Google Sheets"], code=False,
    outcomes=["Choose mean or median and say why.", "Read a histogram, a box plot and a line chart.", "Spot a misleading axis."],
    topics=["Count, sum, mean, median", "Spread: range, quartiles, standard deviation", "Distribution shapes and skew", "Pivot tables as GROUP BY", "Choosing a chart", "Axis honesty"],
    lab="Pivot revenue by branch and month; build a histogram of basket size; fix a deliberately bad chart.",
    maps=dict(roadmap="Statistics, EDA", ibm="What is Data Science? (analysis)", google="Share Data Through the Art of Visualization", other="Kaggle Learn: Data Visualization (ideas)"))
add(no=4, module="A", title="Uncertainty, samples and cause",
    question="How sure can we be, and when does a pattern mean one thing caused another?",
    result="A simulation in Sheets that shows sample error, and three sentences on cause versus correlation.",
    dataset="Lakeside Mart", tools=["Google Sheets"], code=False,
    outcomes=["Explain why a sample differs from the whole.", "Read a correlation and say what it does not show.", "Name two sources of bias."],
    topics=["Probability as long-run frequency", "Sampling and sampling error", "Simulation with RAND in Sheets", "Correlation and its limits", "Confounding and bias", "Survivorship and selection"],
    lab="Draw 200 samples of 30 baskets; plot the spread of their means; discuss an ice-cream and drowning style trap in sales data.",
    maps=dict(roadmap="Mathematics, Statistics", ibm="Data Science Methodology", google="The Power of Statistics (first weeks)", other="Elements of AI chapters 3 and 4"))
add(no=5, module="B", title="Your first Python, next to the spreadsheet",
    question="What does the same task look like in Excel and in Python?",
    result="A notebook that stores values, makes lists and does sums, with an Excel comparison.",
    dataset="Lakeside Mart", tools=["Google Colab"], code=True,
    outcomes=["Run, edit and save a notebook.", "Use variables, numbers, text and lists.", "Read the last line of an error message."],
    topics=["Notebook: code cells and text cells", "Variables are named cells", "Numbers, text, true or false", "Lists and dictionaries", "Errors: read the last line first", "Using an AI assistant to explain an error"],
    lab="Rebuild a small price list calculation in Python; break it on purpose; fix it from the error.",
    maps=dict(roadmap="Coding", ibm="Python for Data Science, AI and Development", google="Introduction to Data Analysis Using Python", other="CS50P week 0; Kaggle Learn: Python"))
add(no=6, module="B", title="Decisions, repeats and functions",
    question="How do we make Python repeat and decide so we never copy a formula down 5,000 rows?",
    result="A notebook with a loop, a condition and one function you wrote.",
    dataset="Lakeside Mart", tools=["Google Colab"], code=True,
    outcomes=["Write an if and a for.", "Wrap steps in a function.", "Test a function with three cases."],
    topics=["If as IF()", "For loop as fill-down", "Functions as named formulas", "Testing with examples", "Reading others' code", "Asking an assistant for a review, and checking it"],
    lab="Write a function that gives a loyalty tier from spend; test it on edge cases.",
    maps=dict(roadmap="Coding", ibm="Python Project for Data Science", google="Introduction to Data Analysis Using Python", other="CS50P weeks 1 to 3"))
add(no=7, module="B", title="pandas I: load, look and filter",
    question="How do we open a file of 30,229 rows and ask the first questions of it?",
    result="A notebook that loads Lakeside Mart, inspects it and answers six filter questions.",
    dataset="Lakeside Mart", tools=["Google Colab"], code=True,
    outcomes=["Load a CSV into a DataFrame.", "Inspect shape, types and missing values.", "Select columns and filter rows."],
    topics=["DataFrame as a sheet", "read_csv, head, info, describe", "Columns and rows: selecting", "Filtering as AutoFilter", "Sorting and top N", "Counting and value_counts"],
    lab="Answer six questions about orders using filters; compare each with the Sheets answer.",
    maps=dict(roadmap="Coding, EDA", ibm="Data Analysis with Python", google="Introduction to Data Analysis Using Python", other="Kaggle Learn: Pandas"))
add(no=8, module="B", title="pandas II: cleaning the mess",
    question="How do we make a raw export trustworthy, and prove what we changed?",
    result="A cleaning notebook with a log of every change and a before and after row count. Checkpoint 1.",
    dataset="Lakeside Mart raw exports", tools=["Google Colab"], code=True,
    outcomes=["Fix types, dates and text.", "Handle missing values and duplicates with a stated rule.", "Write a cleaning log."],
    topics=["Types and dates", "Missing values: drop, fill, flag", "Duplicates and keys", "Text clean-up", "Outliers: check before remove", "The cleaning log"],
    lab="Clean the raw orders file with eight seeded defects; reconcile revenue to the answer within a stated residual.",
    maps=dict(roadmap="EDA", ibm="Data Analysis with Python", google="Process Data from Dirty to Clean", other="Kaggle Learn: Data Cleaning"))
add(no=9, module="B", title="pandas III: group, join and reshape",
    question="How do we answer questions that need several tables and several groups?",
    result="A notebook that joins orders to customers and products and reports revenue by group.",
    dataset="Lakeside Mart", tools=["Google Colab"], code=True,
    outcomes=["Group and aggregate.", "Join tables on a key and check row counts.", "Make a pivot table in code."],
    topics=["groupby as PivotTable", "Several aggregations", "merge as VLOOKUP that returns every match", "Join traps: lost and doubled rows", "pivot_table", "Dates: month and weekday"],
    lab="Revenue by branch, category and month; find the join that silently doubled revenue.",
    maps=dict(roadmap="Coding, EDA", ibm="Data Analysis with Python", google="Introduction to Data Analysis Using Python", other="Kaggle Learn: Pandas"))
add(no=10, module="C", title="SQL for analysts",
    question="How do we ask a database the same questions in the language every employer uses?",
    result="Ten SQL queries against an SQLite copy of Lakeside Mart, each checked against pandas.",
    dataset="Lakeside Mart (SQLite)", tools=["Google Colab", "SQLite"], code=True,
    outcomes=["Write SELECT, WHERE, GROUP BY and ORDER BY.", "Write a JOIN and say what it keeps.", "Check a SQL result against pandas."],
    topics=["A database is several tables", "SELECT and WHERE", "GROUP BY and HAVING", "JOIN types", "Subqueries and CASE", "SQL beside pandas"],
    lab="Ten queries; for three, reproduce the answer in pandas and compare.",
    maps=dict(roadmap="Coding", ibm="Databases and SQL for Data Science with Python", google="Ask Questions; Prepare Data for Exploration (SQL)", other="Kaggle Learn: Intro to SQL"))
add(no=11, module="C", title="Exploring and visualising with Python",
    question="How do we explore an unfamiliar dataset in one sitting and find what is worth reporting?",
    result="An exploration notebook with six charts and three findings written in plain words.",
    dataset="Lakeside Mart", tools=["Google Colab"], code=True,
    outcomes=["Run a repeatable EDA routine.", "Make histograms, scatter, bar and line charts with matplotlib and seaborn.", "Write a finding that states a number and a limit."],
    topics=["The EDA routine", "matplotlib basics", "seaborn for distributions and relationships", "Rates versus counts", "Seasonality in a line chart", "Writing the finding"],
    lab="Explore returns and basket size; find a rate-versus-count reversal between branches.",
    maps=dict(roadmap="EDA", ibm="Data Visualization with Python", google="Share Data Through the Art of Visualization", other="Kaggle Learn: Data Visualization"))
add(no=12, module="C", title="Inference: is the difference real?",
    question="When two groups differ, how do we know it is not just luck?",
    result="A confidence interval and an A/B test on a Lakeside Mart promotion, with a decision.",
    dataset="Lakeside Mart promotions", tools=["Google Colab"], code=True,
    outcomes=["Build and read a confidence interval.", "Run and read a t test and a proportion test.", "State a decision with effect size and uncertainty."],
    topics=["Standard error by simulation", "Confidence intervals", "The null idea and the p-value", "t test and proportion test", "Effect size and practical meaning", "Multiple testing and peeking"],
    lab="Did the shelf promotion lift basket size? Report the lift, the interval and the decision.",
    maps=dict(roadmap="Statistics", ibm="Machine Learning with Python (foundations)", google="The Power of Statistics", other="Khan-style intuition; CS50 Data Science ideas"))
add(no=13, module="C", title="Regression: explaining and predicting a number",
    question="How much does one thing change when another changes, and how well can we predict?",
    result="A regression with a plain-language interpretation and a one-page analysis report. Checkpoint 2.",
    dataset="Lakeside Mart", tools=["Google Colab"], code=True,
    outcomes=["Fit a linear regression and read each coefficient.", "Check residuals.", "Say what the model does not prove."],
    topics=["A line through a cloud", "Least squares by picture", "Coefficients and R squared", "Several predictors and categories", "Residual checks", "Prediction versus explanation"],
    lab="Model branch weekly orders from footfall, promotion and rainfall, see why weekly sales is noisier, and interpret each term in a sentence.",
    maps=dict(roadmap="Econometrics, Statistics", ibm="Machine Learning with Python (regression)", google="Regression Analysis", other="DeepLearning.AI ML Specialization course 1 week 1 to 2"))
add(no=14, module="D", title="Machine learning: the workflow",
    question="What does it mean for a computer to learn from examples, and how do we know it did?",
    result="A first model on Nile Microfinance loans with a train and test split.",
    dataset="Nile Microfinance", tools=["Google Colab", "scikit-learn"], code=True,
    outcomes=["Name features, target, training and test data.", "Split data and fit a model with scikit-learn.", "Compare a model to a naive baseline."],
    topics=["Learning from examples", "Features and target", "Train and test split and why", "fit and predict", "Baselines", "The ML workflow in one picture"],
    lab="Predict loan default with a first model; beat the baseline or explain why not.",
    maps=dict(roadmap="Machine learning", ibm="Machine Learning with Python", google="The Nuts and Bolts of Machine Learning", other="DeepLearning.AI ML Spec course 1; Google MLCC"))
add(no=15, module="D", title="Classification: yes or no questions",
    question="How do we predict a category, and what does the model's confidence mean?",
    result="Logistic regression and a decision tree on loan default, compared.",
    dataset="Nile Microfinance", tools=["Google Colab", "scikit-learn"], code=True,
    outcomes=["Fit logistic regression and a decision tree.", "Read predicted probabilities.", "Choose a threshold from costs."],
    topics=["From a line to a probability", "Logistic regression", "Decision trees as rules", "Probabilities and thresholds", "Categorical features", "Reading a tree"],
    lab="Fit both models; draw the tree; pick a threshold using the cost of a missed default.",
    maps=dict(roadmap="Machine learning, Econometrics", ibm="Machine Learning with Python", google="Regression Analysis (logistic)", other="DeepLearning.AI ML Spec course 1 week 3"))
add(no=16, module="D", title="Judging a model: metrics, leakage and imbalance",
    question="How do we tell a model that works from one that merely looks good?",
    result="A confusion matrix, precision, recall and ROC for the loan model, and a leaked column found and removed.",
    dataset="Nile Microfinance", tools=["Google Colab", "scikit-learn"], code=True,
    outcomes=["Read a confusion matrix.", "Choose precision, recall or AUC for a business cost.", "Find and remove leakage; use cross-validation."],
    topics=["Why accuracy fails on rare events", "Confusion matrix", "Precision and recall", "ROC and AUC", "Leakage: the too-good model", "Cross-validation"],
    lab="Find the column that leaks the answer; compare metrics before and after; cross-validate.",
    maps=dict(roadmap="Machine learning", ibm="Machine Learning with Python", google="The Nuts and Bolts of Machine Learning", other="Google MLCC: classification and data modules"))
add(no=17, module="D", title="Forests, boosting and overfitting",
    question="How do we get a stronger model without fooling ourselves?",
    result="A random forest and a gradient boosting model tuned with cross-validation; feature importance read with care.",
    dataset="Nile Microfinance", tools=["Google Colab", "scikit-learn"], code=True,
    outcomes=["Explain bias, variance and overfitting from a curve.", "Fit a forest and a boosted model.", "Read feature importance without over-claiming."],
    topics=["Overfitting from a curve", "Bagging and forests", "Boosting", "Tuning a few settings", "Feature importance and its limits", "Simple beats clever when equal"],
    lab="Tune a forest; plot train versus test score; decide whether complexity paid.",
    maps=dict(roadmap="Machine learning", ibm="Machine Learning with Python", google="The Nuts and Bolts of Machine Learning", other="DeepLearning.AI ML Spec course 2 week 4"))
add(no=18, module="D", title="Finding structure without labels",
    question="How do we group customers or spot odd cases when nobody gave us the answers?",
    result="Customer segments from Lakeside Mart and a short list of anomalies, each described in business words.",
    dataset="Lakeside Mart customers", tools=["Google Colab", "scikit-learn"], code=True,
    outcomes=["Build recency, frequency and spend features.", "Run k-means and choose k with evidence.", "Describe each segment for a manager."],
    topics=["Supervised versus unsupervised", "RFM features", "Scaling: why it matters", "k-means and the elbow", "PCA as a flat picture of many columns", "Anomalies and what to do with them"],
    lab="Segment customers; name and describe each segment; flag unusual baskets.",
    maps=dict(roadmap="Machine learning", ibm="Machine Learning with Python (clustering)", google="The Nuts and Bolts of Machine Learning", other="DeepLearning.AI ML Spec course 3 week 1"))
add(no=19, module="D", title="Forecasting and a first end-to-end model",
    question="How do we predict next month, and how do we package a whole modelling job?",
    result="A seasonal baseline forecast and a scikit-learn pipeline on clinic visits or Lakeside sales. Checkpoint 3.",
    dataset="Clinic visits and Lakeside Mart", tools=["Google Colab", "scikit-learn"], code=True,
    outcomes=["Split time series by time, never at random.", "Beat a seasonal naive forecast.", "Build a Pipeline that cleans, encodes and models."],
    topics=["Trend, season and noise", "Seasonal naive baseline", "Time-based split", "Lag features", "Pipelines and ColumnTransformer", "Error in the units of the business"],
    lab="Hold back 2025, forecast it from the earlier years, report the error in cases and decide if the model beats the baseline.",
    maps=dict(roadmap="Econometrics, Machine learning", ibm="Applied Data Science Capstone", google="Capstone", other="DeepLearning.AI ML Spec course 2 week 3"))
add(no=20, module="E", title="Neural networks and deep learning, without the maths wall",
    question="What is a neural network, and when is one the right tool?",
    result="A small network trained in TensorFlow Playground and in scikit-learn, and one pretrained image model used in Colab.",
    dataset="Playground and small image sample", tools=["TensorFlow Playground", "Google Colab"], code=True,
    outcomes=["Describe layers, weights and training in plain words.", "Train a small network and see it overfit.", "Say when a simpler model is better."],
    topics=["Neurons as weighted sums", "Layers and activation", "Training as repeated small corrections", "Playground: watch it learn", "A network in scikit-learn", "Pretrained models: use, do not train"],
    lab="Playground challenges; MLPClassifier on the loan data; compare with the forest.",
    maps=dict(roadmap="Deep learning", ibm="Machine Learning with Python (overview)", google="(not covered)", other="fast.ai lesson 1 idea; DeepLearning.AI ML Spec course 2 weeks 1 and 2"))
add(no=21, module="E", title="Text as data and meaning as numbers",
    question="How can a computer compare customer messages when it only understands numbers?",
    result="A bag-of-words sentiment classifier and a meaning-based search over customer feedback using embeddings.",
    dataset="Lakeside feedback messages", tools=["Google Colab", "scikit-learn", "sentence-transformers"], code=True,
    outcomes=["Turn text into counts and into embeddings.", "Train a sentiment classifier and read its mistakes.", "Search by meaning."],
    topics=["Cleaning text", "Bag of words and TF-IDF", "A sentiment classifier", "Embeddings: meaning as position", "Similarity search", "Where each method fails"],
    lab="Classify feedback; search 'long queue at the till' and find messages with different words.",
    maps=dict(roadmap="AI engineering", ibm="Generative AI: Elevate Your Data Science Career", google="Accelerate Your Job Search with AI (tools)", other="Hugging Face NLP course ideas; Google MLCC embeddings"))
add(no=22, module="E", title="Language models and building with them",
    question="What does a language model do, how do we test one, and how do we make it answer from our own documents?",
    result="A retrieval pattern: embed the documents, find the closest passages, and ask a small local model to answer from them, with a test sheet.",
    dataset="Lakeside policy documents", tools=["Google Colab", "sentence-transformers", "small local model"], code=True,
    outcomes=["Explain tokens, context and next-word prediction.", "Build retrieval over a handful of documents.", "Test answers against a checked list and record failures."],
    topics=["Next-word prediction and tokens", "Prompts as instructions", "Why models invent", "Retrieval before answering", "Testing with a question list", "AI-assisted coding: use, check, record"],
    lab="Build the pipeline; write twelve test questions; score the answers; list failures.",
    maps=dict(roadmap="AI engineering, AI-assisted coding", ibm="Generative AI: Elevate Your Data Science Career", google="Google AI Essentials", other="DeepLearning.AI short courses; Google MLCC LLM module"))
add(no=23, module="F", title="Ship it: reproducible work, a small app and responsible use",
    question="How do we turn a notebook into something a colleague can use and trust?",
    result="A GitHub repository, a saved model and a Streamlit app, with a model card and a data-protection checklist.",
    dataset="Capstone data", tools=["GitHub", "Streamlit", "Google Colab"], code=True,
    outcomes=["Save and reload a model.", "Publish code and a small app for free.", "Write a model card and check data-protection duties."],
    topics=["Reproducibility: seeds, versions, order", "Save and load a model", "Git and GitHub in five commands", "Streamlit app", "Monitoring and drift", "Uganda Data Protection and Privacy Act 2019 and fairness checks"],
    lab="Deploy the capstone model as an app; write the model card.",
    maps=dict(roadmap="MLOps", ibm="Data Scientist Career Guide", google="Capstone", other="fast.ai lesson 2 (deploy)"))
add(no=24, module="F", title="Capstone presentations and your path from here",
    question="Can you explain what you built, what it can and cannot do, and what you will learn next?",
    result="A ten-minute presentation and a personal 6-month learning path.",
    dataset="Capstone data", tools=["Google Colab", "GitHub"], code=False,
    outcomes=["Present a result with its limits.", "Answer questions on method and risk.", "Choose next free courses from a gap list."],
    topics=["Story: question, evidence, decision", "Limits and risks, said first", "Presenting to a manager", "Portfolio and GitHub", "What this course did not cover", "Your 6-month path"],
    lab="Present; give and receive structured feedback.",
    maps=dict(roadmap="Portfolio", ibm="Capstone and career", google="Capstone", other="Free next courses: Kaggle Learn, Google MLCC, fast.ai, CS50P"))

SESSIONS = {s["no"]: s for s in S}
assert len(S) == 24 and sorted(SESSIONS) == list(range(1, 25))

CHECKPOINTS = {8: "Checkpoint 1: clean a raw file and reconcile", 13: "Checkpoint 2: an analysis report", 19: "Checkpoint 3: a tested model"}
ASSESSMENT = [("Weekly check at the end of each session", "ungraded, instant feedback"), ("Three checkpoints (sessions 8, 13, 19)", "15% each = 45%"), ("Capstone (scoped in session 13, built through sessions 19 to 23, presented in session 24)", "40%"), ("Notebook completion and participation", "15%")]
