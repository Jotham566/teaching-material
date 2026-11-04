# Data Analysis course: getting started

This course has no exam and no marks. You build projects and keep them. At the end you receive a certificate of completion from KLAi Professional Learning for completing the course and its project.

## Accounts and files

1. Use your existing Google account for Colab. If you do not have one, go to https://accounts.google.com, choose Create account and follow the prompts. Never share a password or verification code.
2. GitHub is optional. It is only useful if you want to keep your projects in a repository, which is a project folder with saved history. A free account at https://github.com is enough.
3. Download the session files from your lecturer. A ZIP is a compressed folder: on Windows right-click > Extract All; on Mac double-click it in Finder. Work in the extracted folder and keep the raw data unchanged.

## SQL in Sessions 3 to 5

Install DB Browser for SQLite from https://sqlitebrowser.org/dl/ for your operating system, or use the prepared installation. No SQL account or database server is needed. Open the app, choose Open Database, select the supplied riverside.db and choose Execute SQL. Type a query and use Execute to see the result table.

For Project 1, save your final query as a plain-text .sql file with the SQL editor's save command. Reopen it and run it to check it still works, and check that it did not acquire an extra .txt extension. The lab shows the right numbers, so you can check yourself.

## Colab in the Python sessions

1. Open https://colab.research.google.com. Choose File > Open notebook > Upload and select the notebook. Save your own copy with File > Save a copy in Drive.
2. Click Connect if needed. In the left Files sidebar click Upload and select the data files named in the lab. Upload them again if a disconnected runtime loses them.
3. Run each cell with Shift+Enter. Read the first error message and fix it before continuing.
4. Before you keep a notebook, choose Runtime > Restart session and then Run all. Download it with File > Download > Download .ipynb and reopen it to check it holds your final work.

## Your projects

| Project | Session | What you keep |
|---|---|---|
| 1. SQL revenue report | 5 | One .sql file |
| 2. Cleaned dataset and cleaning log | 9 | The cleaned file, the log and the pandas report reconciled to SQL |
| 3. Statistics notes page | 11 | One page of notes |
| 4. Investigation write-up | 13 | Five findings and the notebook behind them |
| 5. Power BI dashboard | 15 | The dashboard file |

The investigation and the dashboard together are the final project. You show it in Session 15 in five minutes, and your peers say what they would act on and what they doubt.

## Power BI access before Session 14

Windows users obtain Power BI Desktop from https://learn.microsoft.com/en-us/power-bi/fundamentals/desktop-get-the-desktop. Follow the installation prompts, open the app and check that you can load the supplied CSVs. Desktop is a Windows application and does not install on macOS.

For a Mac, use the lecturer-provisioned browser workspace at https://app.powerbi.com only after testing its model-editing permissions with your authorised teaching account. Sign in and check that you can open the designated semantic model. A personal Gmail sign-in does not give those permissions. If access fails, the lecturer arranges a prepared Windows lab machine before class. Do not buy a licence or start a trial to solve a classroom access problem.

Follow lab_powerbi.md to load the tables into one model, build the relationships, create measures and check your totals against the numbers you already have from SQL and pandas.
