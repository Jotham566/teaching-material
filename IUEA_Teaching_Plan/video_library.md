# Video Library — Introduction to Machine Learning (Year 3 Engineering, IUEA)
Cohorts CML3111 / CML3112 / CML3113 · 3 hrs/week · ~195 students · zero programming background

**Verification rule used:** every entry below was surfaced by a web search I actually ran. The URL is reproduced exactly as it came back in the search results, and the surfacing query is recorded with it. Nothing here was reconstructed from memory. Where a video was described in prose by a search engine but its URL did **not** come back in the results, it is listed in the "Could NOT verify" section and must not be used.

**Runtime rule:** runtime is given only where a search result stated it. Everything else says "not stated" — do not assume.

---

## Week 1 — What AI / ML / data science are; programming vs learning from data; limits of ML; ML in engineering

### 1. IBM Technology — "AI, Machine Learning, Deep Learning and Generative AI Explained"
- **VERIFIED** · URL: https://www.youtube.com/watch?v=qYNweeDHiyU
- Surfacing query: `IBM Technology YouTube "AI vs Machine Learning vs Deep Learning vs Data Science"`
- Runtime: **verified 2026-09-08 as roughly 8-9 minutes** (Class Central rounds it to 10; a
  reviewer times it at about 8:30). Published 5 Aug 2024. The deck says "under 10 minutes",
  which is true on every figure reported.
- Serves: the nesting-doll relationship — AI ⊃ ML ⊃ deep learning, plus where generative AI and foundation models sit.
- Watch FOR: write down, in order, which box sits inside which — you will be asked to draw that diagram from memory.
- Use: **pre-work** before session 1.
- Confidence: high on existence. Presenter is Jeff Crume per the result description.

### 2. IBM Technology — "What is Machine Learning?"
- **VERIFIED** · URL: https://www.youtube.com/watch?v=9gGnTQTYNaE
- Surfacing query: `youtube.com/watch "What is Machine Learning?" IBM Technology Martin Keen`
- Runtime: not stated
- Serves: the core definition of ML, plus a first pass at supervised / unsupervised / reinforcement learning.
- Watch FOR: the moment he says the model was never given explicit instructions for each case — that sentence is the whole course.
- Use: **pre-work**.
- Confidence: **medium on channel attribution.** The title+URL pair came back in results; the IBM MediaCenter listing in the same results describes the same Martin Keen presentation under a different title ("Machine Learning Explained: A Guide to ML, AI, & Deep Learning"). Open it once before assigning to confirm it is the IBM upload.

### 3. StatQuest with Josh Starmer — "A Gentle Introduction to Machine Learning"
- **VERIFIED** · URL: https://www.youtube.com/watch?v=Gv9_4yMHFhI
- Surfacing query: `StatQuest "A Gentle Introduction to Machine Learning" youtube.com/watch`
- Runtime: not stated (results date it to ~Nov 2018)
- Serves: cutting through jargon; sets up "training data vs testing data" which you will reuse in Week 8.
- Watch FOR: the point where he insists you cannot judge a method by how well it fits the data it was trained on — flag it, you are coming back to it.
- Use: **pre-work**, and re-watch as **consolidation** before the overfitting week.
- Confidence: high. Official StatQuest page also returned: https://statquest.org/a-gentle-introduction-to-machine-learning/

### 4. IBM Technology — "Supervised vs. Unsupervised Learning"
- **VERIFIED** · URL: https://www.youtube.com/watch?v=W01tIRP_Rqs
- Surfacing query: `"Supervised vs. Unsupervised Learning" IBM Technology youtube.com/watch?v= Martin Keen`
- Runtime: **7 min 8 sec** (stated in results)
- Serves: labelled vs unlabelled data; the distinction that decides which half of the course a problem belongs to.
- Watch FOR: the cost he attaches to labelling — that cost is why unsupervised methods exist at all.
- Use: **during the session** (short enough to play in class and discuss immediately).
- Confidence: high. Note the URL as returned carried a tracking suffix (`&pp=...`); the bare watch?v=W01tIRP_Rqs form is what to circulate.

### 5. Computerphile — "Machine Learning Methods"
- **VERIFIED** · URL: https://www.youtube.com/watch?v=qDbpYUbf3e0
- Surfacing query: `Computerphile youtube "machine learning" introduction video watch?v=`
- Runtime: not stated (results date it to Sept 2015)
- Serves: a second voice on supervised vs unsupervised, from an academic (Prof. Uwe Aickelin) rather than a vendor.
- Watch FOR: how he frames the question "can a computer work things out with no labels at all?" — that framing is the exam-style version of the concept.
- Use: **consolidation** after session 1.
- Confidence: high on existence. It is 2015, so no mention of modern tooling. Fine for concepts.

### 6. Fireship — "Machine Learning Explained in 100 Seconds"
- **VERIFIED** · URL: https://www.youtube.com/watch?v=PeMlggyqz0Y
- Surfacing query: `Computerphile youtube "machine learning" introduction video watch?v=`
- Runtime: not stated, but titled 100 seconds
- Serves: cheapest possible bandwidth hit for a first orientation. Ideal for the students who will watch on phone data.
- Watch FOR: he moves fast — pause on the words you do not recognise and bring that list to class.
- Use: **pre-work**, as the low-bandwidth fallback for anyone who cannot load a longer video.
- Confidence: medium. Channel attribution (Fireship) came from result prose, not the returned title.

### 7. IBM — "What is Data Science?"
- **VERIFIED** · URL: https://www.youtube.com/watch?v=RBSUwFGa6Fk
- Surfacing query: `IBM Technology "What is Data Science?" youtube.com/watch?v= explainer`
- Runtime: not stated
- Serves: the third term in the Week 1 triangle — how data science differs from ML.
- Watch FOR: what a data scientist does that a machine learning engineer does not.
- Use: **pre-work**.
- Confidence: medium on channel. Results also returned a separate course-intro video, "What is Data Science? - Introduction by IBM #1" at https://www.youtube.com/watch?v=f9AqD83qHGg (also VERIFIED, same query) — that one is a Coursera course trailer, so prefer RBSUwFGa6Fk.

### 8. Google Developers — "Hello World - Machine Learning Recipes #1"
- **VERIFIED** · URL: https://www.youtube.com/watch?v=cKxRvEZd3Mw
- Surfacing query: `Google Developers "Machine Learning Recipes with Josh Gordon" "Hello World" youtube.com/watch`
- Runtime: not stated (description quoted as "six lines of Python is all it takes")
- Serves: the traditional-programming-vs-learning-from-data contrast, made concrete in six lines of code.
- Watch FOR: count how many rules he writes by hand, then count how many the program figures out itself.
- Use: **during the session** as the demo that ends Week 1.
- Confidence: high on existence. It is an older series (TensorFlow-era Google Developers) so library versions on screen will be dated — the concept survives.
- **VERIFIED PLAYLIST** (10 episodes): https://www.youtube.com/playlist?list=PLOU2XLYxmsIIuiBfYad6rFYQU_jL2ryal — cite the playlist, not scattered episodes.

### 9. "Traditional Programming vs Machine Learning"
- **VERIFIED** · URL: https://www.youtube.com/watch?v=N6vC7MqYxtA
- Surfacing query: `"Traditional Programming vs Machine Learning" youtube video explained`
- Runtime: not stated (results date it Nov 2019)
- Serves: the exact Week 1 framing — rules+data→answers versus data+answers→rules.
- Watch FOR: the direction of the arrows in his diagram. That flip is the definition of machine learning.
- Use: **pre-work**.
- Confidence: **LOW on channel quality.** No recognised channel was identified; results describe it as one episode of a larger TensorFlow/Keras course. Preview it before assigning to ~195 students. A very short alternative also verified from the same query: https://www.youtube.com/shorts/FwvsSBijpyY (YouTube Short, Oct 2025) — same rules/answers flip, ~1 min, minimal data cost, but unknown channel.

### 10. "Artificial Intelligence (AI) vs Machine Learning vs Deep Learning vs Data Science"
- **VERIFIED** · URL: https://www.youtube.com/watch?v=xucm6_BQPJU
- Surfacing query: `IBM Technology YouTube "AI vs Machine Learning vs Deep Learning vs Data Science"`
- Runtime: not stated
- Serves: all four Week 1 terms in one video.
- Use: **backup only.**
- Confidence: **LOW.** Search results explicitly state this is **not** the IBM Technology channel and did not identify the uploader. Use entry 1 instead unless you have previewed this.

### 11. DeepLearning.AI — "AI for Everyone by Andrew Ng"
- **VERIFIED** · URL: https://www.youtube.com/watch?v=JPcx9qHzzgk
- Surfacing query: `"AI For Everyone" Andrew Ng youtube playlist DeepLearningAI list=`
- Runtime: not stated
- Serves: potentially the "what ML can and cannot do" concept, including Ng's one-second rule.
- Confidence: **LOW on content.** Search results indicate this video points to the course landing page, so it may be a promo rather than a lecture. See "Could NOT verify" — the free YouTube lecture playlist for AI for Everyone did not return a playlist URL in any search I ran.

**Week 1 verified count: 11 (of which 8 I would put in front of students without previewing first).**

---

## Week 2 — Development environments, Git/GitHub, version control, Jupyter notebooks, the terminal

### 1. freeCodeCamp — "Git and GitHub for Beginners - Crash Course"
- **VERIFIED** · URL: https://www.youtube.com/watch?v=RGOj5yH7evk
- Surfacing query: `"Git and GitHub for Beginners" youtube.com/watch freeCodeCamp crash course`
- Runtime: not officially stated; results infer **roughly one hour** from viewer comments.
- Serves: the whole Week 2 Git/GitHub block — repositories, commits, push, branches, forking, plus VS Code integration.
- Watch FOR: the commit step. Everything before it is setup; the commit is the idea.
- Use: **pre-work, chaptered.** At ~1 hour this exceeds the 25-minute bandwidth guideline, so assign it as named timestamp segments (Intro 0:00, What is git? 1:10, What is version control? 1:30) rather than "watch the whole thing". The full-length watch is only justified for students who intend to use Git beyond this course.
- Confidence: high on existence. **Two known staleness traps flagged in results:** the ssh-agent section trips learners up, and Git's default branch renaming means students will see both `main` and `master`. Warn them in advance or they will lose an evening.

### 2. Fireship — "Git Explained in 100 Seconds"
- **VERIFIED** · URL: https://www.youtube.com/watch?v=hwP7WQkmECE
- Surfacing query: `"Git Explained in 100 Seconds" Fireship youtube.com/watch`
- Runtime: not stated, titled 100 seconds. Chapters returned: 0:09 init, 0:33 stage, 0:39 commit, 1:12 branch, 1:30 merge.
- Serves: the minimum viable mental model of Git before the long crash course.
- Watch FOR: the three-step rhythm — change, stage, commit. Memorise that rhythm and the commands stop feeling arbitrary.
- Use: **pre-work.** Best bandwidth-to-value ratio in Week 2.
- Confidence: high.

### 3. GitHub (official) — "What is GitHub?"
- **VERIFIED** · URL: https://www.youtube.com/watch?v=pBy1zgt0XPc
- Surfacing query: `"GitHub" official channel "What is GitHub?" youtube.com/watch beginner 2 minutes`
- Runtime: **not stated** — results explicitly could not confirm the "~2 minute" figure. Do not advertise a runtime.
- Serves: the Git-vs-GitHub distinction, which every cohort confuses.
- Watch FOR: what GitHub adds that Git alone does not — that difference is the exam answer.
- Use: **during the session**, immediately after the Fireship clip.
- Confidence: high on existence; channel identified as GitHub official in result prose.

### 4. Software Carpentry — "Version Control - Episode 1 - Introduction"
- **VERIFIED** · URL: https://www.youtube.com/watch?v=gY2JwRfin1M
- Surfacing query: `"version control" explained youtube.com/watch why version control exists short`
- Runtime: not stated
- Serves: **why version control exists** — the conceptual half of Week 2, taught by a research-software-training organisation rather than a vendor.
- Watch FOR: the failure it is designed to prevent, not the commands it uses.
- Use: **pre-work.**
- Confidence: medium. Channel identified as Software Carpentry in result prose only.

### 5. "What Is Version Control?"
- **VERIFIED** · URL: https://www.youtube.com/watch?v=X2W1dUM3bu8
- Surfacing query: `"version control" explained youtube.com/watch why version control exists short`
- Runtime: not stated
- Serves: version control as recording changes over time.
- Confidence: **LOW on channel** — uploader not identified. Backup only.

### 6. "What is Version Control? Git & GitHub Basics for Beginners"
- **VERIFIED** · URL: https://www.youtube.com/watch?v=vKh1Jgs3VxQ
- Surfacing query: same as above
- Runtime: not stated
- Serves: vocabulary drill — Git, repository, commit.
- Confidence: **LOW on channel.** Backup only.

### 7. Corey Schafer — "Jupyter Notebook Tutorial: Introduction, Setup, and Walkthrough"
- **VERIFIED** · URL: https://www.youtube.com/watch?v=HW29067qVWk
- Surfacing query: `"Jupyter Notebook" tutorial for beginners youtube.com/watch Corey Schafer`
- Runtime: **roughly 30 minutes** (stated in results)
- Serves: what a notebook is; cells; markdown; export; kernels.
- Watch FOR: the difference between a cell that computes and a cell that explains — that is why notebooks exist in teaching.
- Use: **pre-work**, segmented. At ~30 min it is over the bandwidth guideline; the justification is that this single video covers four Week 2 learning outcomes and students will re-open it all semester. Point them at the "Creating a New Notebook" and "Adding Markdown" sections if data is tight.
- Confidence: medium-high. The URL came back embedded in a returned GitHub result title rather than as a standalone YouTube result; the accompanying prose and Class Central listing both name the same video. Open it once to confirm. Note it dates from Sept 2016, so the install/setup portion is stale — **skip installation entirely if you are teaching in Colab.**
- Companion notebooks (verified in same results): https://github.com/AppleMango23/JupyterNotebook

### 8. Coding TensorFlow (Google) — "Get started with Google Colaboratory"
- **VERIFIED** · URL: https://www.youtube.com/watch?v=inN8seMm7UI
- Surfacing query: `"Google Colab" tutorial for beginners youtube.com/watch introduction`
- Runtime: not stated (results date it 2019)
- Serves: the environment your students will actually use. Presented by Jake VanderPlas.
- Watch FOR: that nothing is installed on their own machine — this is the single biggest anxiety reliever for a cohort with no programming background.
- Use: **during the session** on the day you first open Colab together.
- Confidence: high on existence; Google-affiliated per result prose.

### 9. "Introduction to Google Colab: A Beginner's Guide"
- **VERIFIED** · URL: https://www.youtube.com/watch?v=C3YK8WO8JSI
- Surfacing query: `"Google Colab" tutorial for beginners youtube.com/watch introduction`
- Runtime: not stated
- Serves: short orientation to Colab as a free cloud platform.
- Confidence: **LOW on channel.** Preview first.

### 10. "Google Colab Tutorial for Beginners | Get Started with Google Colab"
- **VERIFIED** · URL: https://www.youtube.com/watch?v=RLYoEyIHL6A
- Surfacing query: same as above
- Runtime: not stated
- Serves: basics with no setup required.
- Confidence: **LOW on channel.** Preview first.
- Also verified from this query, longer-form: Amit Thinks 17-lesson Colab course https://www.youtube.com/watch?v=iMlMfrXJYSg · GeeksforGeeks Colab guide https://www.youtube.com/watch?v=TqqkZLHoY0o · Colab playlist https://www.youtube.com/playlist?list=PLA83b1JHN4ly56Y7o6vDAT8Szxc3_EdRH · "Getting Started with Google Colab" (Utah Tech University) https://www.youtube.com/watch?v=zi5r9zXcUYA — the Utah Tech one is the only institutionally-attributed option among these.

### 11. "What is Terminal / CMD / Command line for beginners"
- **VERIFIED** · URL: https://www.youtube.com/watch?v=J2jvpnwt1jU
- Surfacing query: `"command line" OR terminal "for beginners" explained youtube.com/watch what is the terminal`
- Runtime: not stated
- Serves: the terminal as "a tool for talking to your computer" — conceptual, not command drill.
- Watch FOR: that the terminal is not a different computer, just a different door into the same one.
- Use: **pre-work.**
- Confidence: **LOW on channel.** Preview.

### 12. "Learn the Command Line: What's a Terminal? | Part 1"
- **VERIFIED** · URL: https://www.youtube.com/watch?v=xUyu_hmChdI
- Surfacing query: same as above · Runtime: not stated
- Serves: same concept, framed around why coders need the CLI.
- Confidence: **LOW on channel.** Preview.

### 13. "A Gentle Introduction to the Terminal"
- **VERIFIED** · URL: https://www.youtube.com/watch?v=2crrFuIqQMQ
- Surfacing query: same as above · Runtime: not stated
- Confidence: **LOW on channel.** Preview.

### 14. freeCodeCamp — "The 50 Most Popular Linux & Terminal Commands - Full Course for Beginners"
- **VERIFIED** · URL: https://www.youtube.com/watch?v=ZtqBQ68cfJc
- Surfacing query: same as above · Runtime: not stated, but described as a full course
- Serves: reference only.
- Use: **do not assign.** Full-course length against unreliable bandwidth, and 50 commands is far beyond what this course needs. Cite it as an optional reference for the two or three students who go further.

Also verified, same query: "Terminal Tutorial for Beginners: Command Line Basics & Navigation" https://www.youtube.com/watch?v=qN9lNgs6wJ0 · "Beginner's Guide To The Linux Terminal" https://www.youtube.com/watch?v=s3ii48qYBxA · "Command Line Basics for Beginners - Full Course" https://www.youtube.com/watch?v=mABpAI-pCw0 — all LOW on channel identification.

**Week 2 verified count: 14 named entries plus 7 additional verified alternates. Only 5 come from channels I can name with confidence (freeCodeCamp ×2, Fireship, GitHub official, Corey Schafer, Coding TensorFlow) — see the "poor fit" section on the terminal topic.**

---

## Week 3 — Python basics: variables, data types, functions, why functions matter, reading an error message

### 1. Corey Schafer — "Python Programming Beginner Tutorials" (PLAYLIST)
- **VERIFIED PLAYLIST** · URL: https://www.youtube.com/playlist?list=PL-osiE80TeTskrapNbzXhwoFUiLCjGgY7
- Surfacing query: `Corey Schafer "Python Tutorial for Beginners" variables strings integers youtube.com/watch`
- Runtime: results describe the series as **~9 hours total** across the episodes.
- **Cite this playlist rather than individual episodes** — the ordering is the pedagogy, and students who lose one URL can recover the rest.
- Confidence: high. A second playlist ID also came back for the same series (`PL-osiE80TeTskrapNbzXhwoFUiLCjGgY7`); note that results at one point associated the series with a differently-formatted playlist link, so verify the playlist opens before circulating.

### 2. Corey Schafer — "Python Tutorial for Beginners 2: Strings - Working with Textual Data"
- **VERIFIED** · URL: https://www.youtube.com/watch?v=k9TUPpGqYTo
- Surfacing query: `Corey Schafer "Python Tutorial for Beginners" variables strings integers youtube.com/watch`
- Runtime: not stated
- Serves: **variables and the string data type.** Results note Corey has no standalone "variables" episode — variable assignment is introduced here via `message = 'Hello World'`.
- Watch FOR: the very first line he types. That is variable assignment, and it is the single most important line in Week 3.
- Use: **pre-work.**
- Confidence: high.

### 3. Corey Schafer — "Python Tutorial for Beginners 8: Functions"
- **VERIFIED** · URL: https://www.youtube.com/watch?v=9Os0o3wzS_I
- Surfacing query: `"Python Tutorial for Beginners 8: Functions" Corey Schafer youtube`
- Runtime: not stated (published May 2017)
- Serves: defining functions, passing arguments, returning values — the "why functions matter" outcome.
- Watch FOR: the moment he replaces repeated code with one call. Ask yourself how many lines he just deleted.
- Use: **pre-work**, then repeat the same refactor live in class.
- Confidence: high.

### 4. Real Python — "How Do You Read a Python Traceback?"
- **VERIFIED** · URL: https://www.youtube.com/watch?v=3p3p6kp39to
- Surfacing query: `"how to read Python error messages" OR "read a traceback" beginners youtube.com/watch`
- Runtime: not stated
- Serves: the "reading an error message" outcome — the highest-value skill for a cohort with zero programming background.
- Watch FOR: which end of the traceback he reads first. Copy that habit exactly — bottom line first, every time.
- Use: **during the session.** Break something live, then play this.
- Confidence: medium-high. Channel identified as Real Python in result prose; the URL as returned carried a tracking suffix, so circulate the bare `watch?v=3p3p6kp39to` form.

**Week 3 verified count: 4 (1 playlist + 3 videos). This is the thinnest of the priority weeks — see gaps.**

---

## Week 4 — Loops and iteration; lists and dictionaries; debugging; decomposing a problem

### 1. Corey Schafer — "Python Tutorial for Beginners 7: Loops and Iterations - For/While Loops"
- **VERIFIED** · URL: https://www.youtube.com/watch?v=6iF8Xb7Z3wQ
- Surfacing query: `"Python Tutorial for Beginners 7: Loops and Iterations" Corey Schafer youtube`
- Runtime: not stated (published May 2017)
- Serves: for loops, while loops, iteration.
- Watch FOR: what changes on each pass through the loop. Track that one variable and loops stop being mysterious.
- Use: **pre-work.**
- Confidence: high.

### 2. Corey Schafer — "Python Tutorial for Beginners 4: Lists, Tuples, and Sets"
- **VERIFIED** · URL: https://www.youtube.com/watch?v=W8KRzm-HUcc
- Surfacing query: `"Python Tutorial for Beginners 4: Lists, Tuples, and Sets" Corey Schafer youtube`
- Runtime: not stated (published May 2017)
- Serves: lists as the container you will loop over all semester.
- Watch FOR: the difference between a list and a tuple. One you can change; one you cannot. Note which is which.
- Use: **pre-work.**
- Confidence: high.

### 3. Corey Schafer — "Python Tutorial for Beginners 5: Dictionaries - Working with Key-Value Pairs"
- **VERIFIED** · URL: https://www.youtube.com/watch?v=daefaLgNkw0
- Surfacing query: `"Python Tutorial for Beginners 5: Dictionaries" Corey Schafer youtube`
- Runtime: not stated (published May 2017)
- Serves: dictionaries and key-value lookup.
- Watch FOR: how he looks a value up by name rather than by position — that is the whole reason dictionaries exist.
- Use: **pre-work.**
- Confidence: high.

### 4. "Debug Python the right way"
- **VERIFIED** · URL: https://www.youtube.com/watch?v=LJcPCSoeH0M
- Surfacing query: `"how to debug" Python beginners youtube.com/watch debugging tutorial print statements`
- Runtime: not stated
- Serves: debugging beyond scattered print statements; walks through a real KeyError.
- Watch FOR: the actual bug, not the tooling. Pause before he finds it and try to spot it yourself.
- Use: **during the session.**
- Confidence: **LOW on channel** — uploader not identified. Preview before showing.

### 5. "Python Debugging with print statement | Part 1"
- **VERIFIED** · URL: https://m.youtube.com/watch?v=cHZpNwDCqvo
- Surfacing query: same as above
- Runtime: not stated
- Serves: print-statement debugging, which is the right first technique for absolute beginners.
- Watch FOR: where he chooses to place each print. Placement is the skill; printing is trivial.
- Use: **pre-work.**
- Confidence: **LOW on channel.** URL was returned in the mobile `m.youtube.com` form — that is what the search gave, so I have not rewritten it. Preview before assigning.

### 6. "Computational Thinking: Decomposition and Abstraction"
- **VERIFIED** · URL: https://www.youtube.com/watch?v=GN5q9WHzK6c
- Surfacing query: `"computational thinking" decomposition explained youtube.com/watch how to break down a problem programming beginners`
- Runtime: not stated
- Serves: the "how to decompose a problem" outcome.
- Watch FOR: how he splits one problem into sub-problems before writing anything. Copy that habit into your first assignment.
- Use: **pre-work.**
- Confidence: **MEDIUM-LOW.** Results identify it as part of a GCSE Computer Science (Edexcel) series — i.e. UK secondary school level. The concept is right for your cohort but the register is below university. Preview and decide whether the level insults or reassures a class with zero programming background. This was the **only** decomposition video that surfaced.

**Week 4 verified count: 6 (3 high-confidence Corey Schafer, 3 needing a preview).**

---

## Weeks 5-15 map

### Data cleaning
- **VERIFIED** · Corey Schafer — "Python Pandas Tutorial (Part 9): Cleaning Data - Casting Datatypes and Handling Missing Values" · https://www.youtube.com/watch?v=KdmPHEnPJPs · query: `pandas data cleaning tutorial youtube.com/watch beginners missing values Corey Schafer` · runtime not stated. Watch FOR: what he does with a missing value rather than what he does about it — the decision, not the code.
- **VERIFIED** · Corey Schafer — "Python Pandas Tutorial (Part 1): Getting Started with Data Analysis" · https://www.youtube.com/watch?v=ZyhVh-qRZPA · query: `Corey Schafer "Python Pandas Tutorial" playlist youtube.com/playlist data analysis`
- **VERIFIED PLAYLIST** · Corey Schafer "Pandas Tutorials" (11 parts) · https://m.youtube.com/playlist?list=PL-osiE80TeTsWmV9i9c58mdDCSskIFdDS · same query. Returned in the mobile form; the `list=` ID is what matters. **Cite the playlist.** Uses the Stack Overflow Developer Survey dataset — students must download it to follow along, which is a bandwidth cost worth planning for.
- **VERIFIED** · "Complete Python Pandas Data Cleaning Tutorial | Handle Missing Data, Null Values & Duplicates" · https://www.youtube.com/watch?v=49MwmVFiOV0 · same query · LOW on channel.
- Use: **pre-work** for the pandas mechanics; do the judgement calls in class.

### Data visualisation
- **VERIFIED** · Corey Schafer — "Matplotlib Tutorial (Part 1): Creating and Customizing Our First Plots" · https://www.youtube.com/watch?v=UO98lJQ3QGI · query: `Corey Schafer "Matplotlib Tutorial" part 1 creating and customizing plots youtube.com/watch` · runtime not stated (June 2019). Watch FOR: how much of the plot is default and how much he chose — every choice is a decision about what the reader should notice.
- **VERIFIED PLAYLIST** · Corey Schafer "Matplotlib Tutorials" (10 parts: line, bar, pie, stack, fill, histogram, scatter, time series, live data, subplots) · https://www.youtube.com/playlist?list=PL-osiE80TeTvipOqomVEeZ1HRrcEvtZB_ · same query. **Cite the playlist** and assign only the chart types your cohort needs — Part 6 (histograms) and Part 7 (scatter) are the two that matter for ML.
- Companion code repo verified in same results: https://github.com/manjusv/Matplotlib_tutorial
- Use: **pre-work.**

### What a model is / fitting a line · Linear regression
- **VERIFIED** · StatQuest — "Linear Regression, Clearly Explained!!!" · https://www.youtube.com/watch?v=7ArmBVF2dCs · query: `"Linear Regression, Clearly Explained" StatQuest youtube.com/watch?v= 2022` · **runtime 27 minutes (stated)**. Watch FOR: why he squares the residuals instead of taking absolute values — he tells you, and it is the reason least squares looks the way it does.
- Use: **pre-work, segmented.** 27 min is over the guideline; the justification is that this one video delivers "what a model is", "fitting a line", and R-squared. Chapters returned in results: The Main Ideas · fitting a line review · R-squared review · R-squared for a multivariable model · why adding variables never reduces R-squared · p-value for R-squared · the F-distribution. Assign the first three chapters only for a Year 3 non-programming cohort; the F-distribution material is beyond scope.
- Results also flagged an in-video correction regarding Pfit − Pmean — mention it so students do not think they have misunderstood.

### Train-test split and overfitting
- **VERIFIED** · StatQuest — "Machine Learning Fundamentals: Bias and Variance" · https://www.youtube.com/watch?v=EuBBz3bI-aA · query: `"Machine Learning Fundamentals: Bias and Variance" StatQuest youtube.com/watch?v=` · runtime not stated (Sept 2018). Watch FOR: his warning not to be impressed by how well a method fits its training data. That warning is the entire week.
- **VERIFIED** · StatQuest — "Machine Learning Fundamentals: Cross Validation" · https://www.youtube.com/watch?v=fSytzGwwBVw · query: `"Machine Learning Fundamentals: Cross Validation" StatQuest youtube.com/watch` · runtime not stated (April 2018). Watch FOR: why he refuses to judge a method on the data it was trained on — this is also your best available substitute for a dedicated train-test-split video.
- **VERIFIED** · Veritasium — "Is Most Published Research Wrong?" · https://www.youtube.com/watch?v=42QuXLucH3Q · query: `"Is Most Published Research Wrong" Veritasium video site:youtube.com` · **runtime ~10 minutes per the description; a university course listing gives 12:21** — the two sources disagree, so state "about 10-12 minutes". Watch FOR: his count of false positives among published results. Then ask yourself what a model reporting 99% accuracy on its own training data has in common with that. Use: **during the session**, as the discussion opener for the validation week. This is the one genuine Veritasium fit in the whole course.
- **Gap:** no dedicated train-test-split video from a channel I can name. See gaps section.

### Classification
- **VERIFIED** · StatQuest — "StatQuest: Logistic Regression" · https://www.youtube.com/watch?v=yIYKR4sgzI8 · query: `StatQuest "Logistic Regression" clearly explained youtube.com/watch classification` · runtime not stated (March 2018). Watch FOR: the shape change — a straight line becomes an S-curve. Ask why a straight line cannot output a probability.
- **VERIFIED** · StatQuest — "Odds and Log(Odds), Clearly Explained!!!" · https://www.youtube.com/watch?v=ARfXDSkQf1Y · same query · prerequisite, assign only if the S-curve maths is going to be examined.
- **VERIFIED PLAYLIST** · StatQuest Logistic Regression series (~1.5 hrs) · https://www.youtube.com/playlist?list=PLblh5JKOoLUKxzEP5HA2d-Li7IJkHfXSe · same query.
- Note from results worth repeating to students: logistic regression models a probability and is not itself a classifier until you pick a cutoff. That distinction leads directly into the confusion-matrix week.

### Decision trees and random forests
- **VERIFIED** · StatQuest — "Decision and Classification Trees, Clearly Explained!!!" · https://www.youtube.com/watch?v=_L39rN6gz7Y · query: `StatQuest "Decision and Classification Trees, Clearly Explained" youtube.com/watch` · runtime not stated (April 2021). Watch FOR: how he picks which question to ask first. That choice — lowest impurity — is the only algorithm in the video. **This is the 2021 revision of his 2018 tree video, so prefer this URL over any older tree link.**
- **VERIFIED** · StatQuest — "StatQuest: Random Forests Part 1 - Building, Using and Evaluating" · https://www.youtube.com/watch?v=J4Wdy0Wc_xQ · query: `StatQuest "Random Forests Part 1" Building, Using and Evaluating youtube.com/watch` · runtime not stated (Feb 2018). Watch FOR: why each tree is deliberately given less information than the full dataset. The handicap is the point.
- **VERIFIED** · StatQuest — "StatQuest: Random Forests in R" · https://www.youtube.com/watch?v=6EXPYzbfLCE · same query · **do not assign** — this course is Python/Colab, and an R walkthrough will confuse a zero-background cohort. Listed only so it is not mistaken for the Part 1 video.
- Official page verified: https://statquest.org/decision-and-classification-trees-clearly-explained/

### Confusion matrix, precision and recall
- **VERIFIED** · StatQuest — "Machine Learning Fundamentals: The Confusion Matrix" · https://www.youtube.com/watch?v=Kdsp6soqA7o · query: `"Machine Learning Fundamentals: The Confusion Matrix" StatQuest youtube.com/watch` · runtime not stated (Oct 2018). Watch FOR: how the size of the matrix is set by the number of things you are predicting — then draw the 2×2 case yourself before he does.
- **VERIFIED** · StatQuest — "Machine Learning Fundamentals: Sensitivity and Specificity" · https://www.youtube.com/watch?v=vP06aMoz4v8 · query: `"Machine Learning Fundamentals: Sensitivity and Specificity" StatQuest youtube video link` · runtime not stated. Watch FOR: which of the four cells each metric ignores. Every metric in this week is defined by what it throws away.
- **VERIFIED** · StatQuest — "ROC and AUC, Clearly Explained!" · https://www.youtube.com/watch?v=4jRBRDbJemM · query: `StatQuest "ROC and AUC, Clearly Explained" youtube.com/watch` · runtime not stated (2019.07.11 revision). Watch FOR: the threshold sliding. Each position of that threshold is one confusion matrix, and the curve is all of them at once.
- Order matters: confusion matrix → sensitivity/specificity → ROC/AUC. Results confirm the ROC video assumes the first two.
- **Note on precision and recall specifically:** results referenced a StatQuest video "The Sensitivity, Specificity, Precision, Recall Sing-a-Long!!!" but **no URL for it was returned**, so it is not listed. See "Could NOT verify".

### Cross-validation
- Covered by the verified StatQuest cross-validation video above (https://www.youtube.com/watch?v=fSytzGwwBVw). No second source needed.

### Data leakage
All of the following are **VERIFIED** from query `"data leakage" machine learning explained youtube.com/watch video`, runtimes not stated:
- "Data Leakage Explained Visually | How Models Cheat Without You Realizing" · https://www.youtube.com/watch?v=xzCXqYlV2HE
- "Data Leakage in ML | Target Leakage | Temporal Leakage | Train Test Contamination | Explained" · https://www.youtube.com/watch?v=6pP9meuusNw
- "What is Data Leakage in Machine Learning Explained with Examples | ML Concepts" · https://www.youtube.com/watch?v=YkpeXxzWEH8
- "Understanding the different kinds of Data Leakage in Machine Learning" · https://www.youtube.com/watch?v=2D9EfiEE06Y
- "What is Data Leakage In Machine Learning?" · https://www.youtube.com/watch?v=n9jz7G68pVg
- "Why Is Data Leakage A Problem In Machine Learning?" (The Friendly Statistician) · https://www.youtube.com/watch?v=w6niZDQdTzo
- Short (~1 min): https://www.youtube.com/shorts/j9X8m5KSQAc
- **Confidence: LOW across the board on channel.** Not one of these is from a channel I can vouch for. The videos exist; the quality is unverified. Watch FOR (if you use the taxonomy one): the four named leakage types — target, temporal, train-test contamination, group.
- **Recommendation: teach this yourself.** Use the group-leakage example that surfaced in results — Andrew Ng's group had 100k x-rays from 30k patients and split them randomly, so the same patient appeared in both train and test. That example lands with engineering students in one minute and needs no video.

### Feature engineering
- **VERIFIED** · IBM Technology — "Feature Engineering for AI: Transforming Raw Data into Predictions" · https://www.youtube.com/watch?v=Bg3CjiJ67Cc · query: `"feature engineering" explained youtube.com/watch IBM Technology OR StatQuest what is feature engineering` · runtime not stated. Watch FOR: which raw column he decides is useless and why. Deciding what to throw away is the job.
- **VERIFIED** · Google Developers — "What Makes a Good Feature?" is episode #3 of the Machine Learning Recipes playlist verified above (https://www.youtube.com/playlist?list=PLOU2XLYxmsIIuiBfYad6rFYQU_jL2ryal). Episode titles came back in results but **individual episode URLs beyond #1 did not** — cite the playlist and let students navigate to episode 3.
- Note: results explicitly state StatQuest does not cover feature engineering as a standalone topic. Do not go looking.

### Model comparison
- No dedicated video verified. Use the two StatQuest videos that results describe as jointly answering "which method is best for our dataset": Cross Validation (https://www.youtube.com/watch?v=fSytzGwwBVw) and ROC and AUC (https://www.youtube.com/watch?v=4jRBRDbJemM), whose description explicitly covers using AUC to compare classification methods. See gaps.

### Reproducibility
- **No video verified.** See gaps.

### Bonus — intuition and visual mathematics (3Blue1Brown)
- **VERIFIED** · 3Blue1Brown — "But what is a neural network? | Deep learning chapter 1" · https://www.youtube.com/watch?v=aircAruvnKk · query: `3Blue1Brown "But what is a neural network" youtube.com/watch chapter 1` · **runtime ~18 minutes** (per a reviewer quoted in results, not the official listing — treat as approximate). Watch FOR: his definition of a neuron as nothing more than a thing that holds a number between 0 and 1. Everything else in the video is built on that.
- **VERIFIED** · 3Blue1Brown — "Gradient descent, how neural networks learn | Deep learning, chapter 2" · https://www.youtube.com/watch?v=IHZwWFHWa-w · query: `3Blue1Brown "Gradient descent, how neural networks learn" chapter 2 youtube.com/watch` · **runtime 21 minutes** (stated). Chapters returned: 0:00 intro · 0:30 recap · 1:49 using training data · 3:01 cost functions · 6:55 gradient descent · 11:18 gradient vectors · 13:01 analysing the network · 17:38 Lisha Li interview. Watch FOR: what "learning" actually means in his account — changing weights to make one number smaller. That is the whole of training.
- Use: **consolidation only**, late in the semester, and only if you reach neural networks. Both exceed the 25-minute guideline; the justification is that no shorter source builds the same intuition, and chapter timestamps let you assign 5-minute slices. Written versions exist for low-bandwidth students: https://www.3blue1brown.com/lessons/neural-networks/ and https://www.3blue1brown.com/lessons/gradient-descent/
- Typo corrections flagged in results (mention them so students do not doubt themselves): chapter 1 at 14:45 shows index n where it should be k.

### Platform orientation (Kaggle, if you use it for datasets or the capstone)
- **VERIFIED** · Kaggle (official) — "Getting Started on Kaggle: A quick tour" · https://www.youtube.com/watch?v=O1P4r0Iy55U · query: `Kaggle official youtube channel "Kaggle" data science video watch?v= how to get started notebooks` · runtime not stated. Presented by Kaggle data scientist Rachael.
- **VERIFIED** · Kaggle (official) — "How to use Kaggle Notebooks" · https://www.youtube.com/watch?v=BPQDZLPtgDc · same query · runtime not stated.
- **VERIFIED PLAYLIST** · "Getting Started on Kaggle" · https://www.youtube.com/playlist?list=PLqFaTIg4myu8gbDh6oBl7XRYNBlthpDEW · same query.
- Official channel verified: https://www.youtube.com/@kaggle
- Caveat: the quick-tour video refers to "Kernels", which Kaggle has since renamed to Notebooks. Warn students about the terminology drift.

---

## Verified playlists (prefer these over individual video links)

| Playlist | URL | Surfacing query |
|---|---|---|
| StatQuest — Machine Learning (the core of Weeks 5-15) | https://www.youtube.com/playlist?list=PLblh5JKOoLUICTaGLRoHQDuF_7q2GfuJF | `StatQuest machine learning playlist "PLblh5JKOoLUICTaGLRoHQDuF_7q2GfuJF"` |
| StatQuest — Logistic Regression | https://www.youtube.com/playlist?list=PLblh5JKOoLUKxzEP5HA2d-Li7IJkHfXSe | `StatQuest "Logistic Regression" clearly explained youtube.com/watch classification` |
| Corey Schafer — Python Programming Beginner Tutorials (Weeks 3-4) | https://www.youtube.com/playlist?list=PL-osiE80TeTskrapNbzXhwoFUiLCjGgY7 | `Corey Schafer "Python Tutorial for Beginners" variables strings integers youtube.com/watch` |
| Corey Schafer — Pandas Tutorials (11 parts) | https://m.youtube.com/playlist?list=PL-osiE80TeTsWmV9i9c58mdDCSskIFdDS | `Corey Schafer "Python Pandas Tutorial" playlist youtube.com/playlist data analysis` |
| Corey Schafer — Matplotlib Tutorials (10 parts) | https://www.youtube.com/playlist?list=PL-osiE80TeTvipOqomVEeZ1HRrcEvtZB_ | `Corey Schafer "Matplotlib Tutorial" part 1 creating and customizing plots youtube.com/watch` |
| Google Developers — Machine Learning Recipes with Josh Gordon (10 eps) | https://www.youtube.com/playlist?list=PLOU2XLYxmsIIuiBfYad6rFYQU_jL2ryal | `Google Developers "Machine Learning Recipes with Josh Gordon" "Hello World" youtube.com/watch` |
| Kaggle — Getting Started on Kaggle | https://www.youtube.com/playlist?list=PLqFaTIg4myu8gbDh6oBl7XRYNBlthpDEW | `Kaggle official youtube channel "Kaggle" data science video watch?v= how to get started notebooks` |
| Complete Google Colab Tutorial (third party, unverified channel) | https://www.youtube.com/playlist?list=PLA83b1JHN4ly56Y7o6vDAT8Szxc3_EdRH | `"Google Colab" tutorial for beginners youtube.com/watch introduction` |

**Also verified and worth bookmarking, not a playlist:** the official StatQuest video index, organised by category (Statistics, Statistical Tests, Machine Learning, Neural Networks, Deep Learning, AI) — https://statquest.org/video_index.html · surfaced by `"Machine Learning Fundamentals: Sensitivity and Specificity" StatQuest youtube video link`. For a bandwidth-constrained cohort this index page is a cheaper way to distribute the whole StatQuest curriculum than 20 separate YouTube links.

---

## Could NOT verify — do NOT use these links

These were described in search-result prose but **no URL came back**, or the URL returned was for a different channel. They are recorded so nobody reconstructs them later.

1. **StatQuest — "The Sensitivity, Specificity, Precision, Recall Sing-a-Long!!!"** — referenced twice in results as existing on the channel. No URL returned. This is the most annoying miss, because it is the one StatQuest video aimed squarely at precision and recall. Find it manually on the channel or teach precision/recall from the confusion-matrix video.
2. **StatQuest — "Fitting a line to data, aka least squares, aka linear regression"** — confirmed to exist and catalogued by Class Central, but the search explicitly reported that it could not surface the watch URL. Use "Linear Regression, Clearly Explained!!!" (7ArmBVF2dCs) instead, which covers the same least-squares material.
3. **Corey Schafer — "Python Tutorial for Beginners 3: Integers and Floats"** — a URL appeared in result prose only, never in a returned result. Left out deliberately. Reach it via the verified playlist.
4. **Corey Schafer — "Python Tutorial for Beginners 1: Install and Setup"** and **"6: Conditionals and Booleans"** — titles confirmed in the series listing, no URLs returned. Reach them via the verified playlist.
5. **IBM Technology — a dedicated "What is Git?" video** — searched for directly; results returned no IBM URL. The nearest verified result was "What is Git? Explained in 2 Minutes!" at https://www.youtube.com/watch?v=2ReR1YJrNOM, which results state is **not** IBM and whose channel is unidentified. Treat as unvetted.
6. **IBM Technology — a dedicated "Overfitting / Underfitting" video** — searched directly; the search returned IBM's written explainers but no IBM Technology video URL, and explicitly noted it did not appear. Use StatQuest bias/variance instead.
7. **IBM Technology — a "predictive maintenance" concept explainer** — searched directly. Results returned only IBM **product marketing** videos (IBM Maximo, PMQ solution demos, a customer story, a German trailer) and explicitly stated no IBM Technology concept explainer surfaced. Do not use marketing videos as teaching material. This leaves "ML in engineering practice" without a good video.
8. **Andrew Ng / DeepLearning.AI — "AI for Everyone" free YouTube lecture playlist** — third-party sources assert the course is free on YouTube, but **no playlist URL was returned by any query I ran.** The only verified URL (JPcx9qHzzgk) appears to point at the course landing page. Do not promise students a free YouTube version until you have found the playlist yourself.
9. **Veritasium — "We're Building Computers Wrong (for artificial intelligence)"** and **"AlphaFold - The Most Useful Thing AI Has Ever Done"** — both confirmed to exist (IMDb entry, veritasium.com page), but **neither returned a YouTube URL.** Not listed above for that reason.
10. **A dedicated train-test-split video** — two searches returned only written tutorials. Results named StatQuest, Codebasics and sentdex as likely sources but surfaced no URLs.
11. **A reproducibility video suitable for this course** — see gaps.

---

## Topics with NO good verified video — you must teach these yourself

Ranked by how much it costs you.

1. **Reproducibility.** Nothing usable. The only video resources that surfaced were the Riffomonas channel (R-focused, 20-30 min Code Club sessions, wrong language for this course) and a Microsoft AI Show episode tied to Azure ML — a vendor pitch. Neither is right for Year 3 engineers in Colab. Teach it yourself, and teach it as a habit rather than a concept: fixed random seed, requirements pinned, notebook runs top to bottom from a fresh kernel.
2. **ML in engineering practice** (Week 1). The obvious hook — predictive maintenance — has no concept explainer from a channel I can name. Every IBM result was product marketing. This matters because it is your credibility moment with CML3111 and CML3113. Build it yourself from your own domain examples, one per cohort.
3. **Train-test split as its own topic.** No verified video. StatQuest's cross-validation video is the closest and is good, but it presents the split as a step inside cross-validation rather than the standalone idea. Teach the split on the board first, then play the video.
4. **Data leakage.** Seven videos exist and are verified, but not one is from a channel I can vouch for, and leakage is precisely the topic where a subtly wrong explanation does damage. Teach it with the x-ray/patient example.
5. **Model comparison.** No dedicated video. Assemble it from cross-validation plus ROC/AUC.
6. **"What ML cannot do."** No standalone verified video. Andrew Ng's one-second heuristic is the best framing available and it came from written sources, not a verified video. Deliver it yourself.
7. **Problem decomposition.** One verified video only, pitched at UK secondary school level. Thin enough that you should plan to carry this yourself.
8. **Precision and recall specifically.** The confusion matrix and sensitivity/specificity videos are verified and excellent; the video that names precision and recall directly could not be verified. Bridge the vocabulary yourself in one slide.
9. **Reading an error message.** One verified video (Real Python). Adequate, but a single point of failure for the highest-value skill in the course. Do it live as well — break something in front of them.

---

## Channels that turned out to be a poor fit

- **Veritasium.** See the verdict below. Thin on ML, and the one usable video is usable for a reason unrelated to ML.
- **3Blue1Brown.** Not a poor fit in quality — it is a poor fit in *placement*. Both verified videos are 18 and 21 minutes of dense visual mathematics about neural networks, a topic that sits at the very end of your syllabus if it appears at all. For a cohort with zero programming background in Weeks 1-4 it would be actively demoralising. Hold it back to consolidation, late, optional.
- **IBM Technology.** Excellent for Week 1 "what is X" framing and verified for four of those. But it collapsed on every applied topic I tried: no verified Git video, no verified overfitting video, and the predictive-maintenance search returned nothing but product marketing. Use it for definitions in Week 1 and stop.
- **Computerphile.** One verified hit, from 2015, and its catalogue skews to computer-science-theory topics for people who already program. Good as a second voice in Week 1; not a spine.
- **freeCodeCamp.** The full-course format is the problem, not the teaching. A one-hour Git course and a 50-command terminal course are both wrong shapes for unreliable, expensive bandwidth. Use the Git crash course as timestamped segments and skip the terminal course entirely.
- **Andrew Ng / DeepLearning.AI.** Conceptually the best fit for "what ML can and cannot do", but I could not verify a free YouTube lecture playlist. Currently unusable as an assigned resource.
- **StatQuest.** The opposite of a poor fit — see below. One caveat: several videos are R-based (e.g. "Random Forests in R", "Logistic Regression in R"). Filter those out before circulating anything, because a zero-background cohort cannot tell R from Python and will assume they are missing something.
- **The generic "what is X" tutorial channels** that dominated the terminal, version-control, data-leakage and debugging searches. Collectively these produced ~20 verified URLs from channels nobody can name. They are not fabricated and they may be fine, but at 195 students you should preview any of them before assigning. That is the honest state of those four topics.

---

## Honest verdict on Veritasium

You asked for it, so I searched for it properly — four separate queries, including one restricted to youtube.com. Here is what I actually found.

Veritasium is not a machine learning channel and there is no way to make it one. Across all my searching, exactly **one** Veritasium video came back with a verifiable YouTube URL that is worth a minute of your students' bandwidth:

**"Is Most Published Research Wrong?"** — https://www.youtube.com/watch?v=42QuXLucH3Q — about 10-12 minutes (sources disagree).

And it is genuinely, non-tokenistically good — but not for the reason you might hope. It is not about ML. It is about the fact that a result which looks significant can be an artefact of how you searched for it. That is exactly the intuition your students need in the overfitting and validation week: a model reporting 99% accuracy on the data it was trained on is committing the same error as a researcher publishing a p < .05 result they went fishing for. Play it in the session where you introduce train-test split, ask the class what the model's "publication bias" is, and it will do more work than any of the low-confidence data-leakage videos.

Its other AI-adjacent content did not hold up:
- "We're Building Computers Wrong (for artificial intelligence)" — confirmed to exist via an IMDb entry, but **no YouTube URL was returned**, so I am not giving you a link. It is also about analog computing hardware, which is orthogonal to your syllabus.
- "AlphaFold - The Most Useful Thing AI Has Ever Done" — confirmed on veritasium.com, but again **no YouTube URL returned**. It is also a story about a result rather than an explanation of a method — inspiring, not instructive.
- "What Everyone Gets Wrong About AI and Learning" — https://www.youtube.com/watch?v=0xS68sl2D70 (VERIFIED, query: `Veritasium video about artificial intelligence OR machine learning OR algorithm youtube.com/watch`). This is Derek Muller lecturing at the Perimeter Institute, on the Perimeter channel, not Veritasium's. **1 hour 15 minutes.** Against unreliable, expensive bandwidth that is indefensible for a required course, and its subject is AI's effect on learning rather than how ML works. Leave it out.
- Two further verified URLs are collaborations where Muller is a guest, not the teacher: https://www.youtube.com/watch?v=Fe2adi-OWV0 (Demis Hassabis Q&A) and https://www.youtube.com/watch?v=Fh_h5Txndxg (a Rhett & Link episode). Neither belongs in a syllabus.

**Bottom line:** use exactly one Veritasium video, in exactly one week, for a reason that is about scientific validity rather than machine learning. Anything more would be forcing it, and your students' data bundles will notice.
