# -*- coding: utf-8 -*-
"""Curriculum benchmark against the roadmap.sh Machine Learning roadmap."""
import sys
import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_HERE)
sys.path.insert(0, _HERE)
from docx.enum.text import WD_ALIGN_PARAGRAPH as AL
from docx.shared import Inches
from docxkit import *      # noqa
from docxkit import _border

OUT = _ROOT + "/IUEA_Teaching_Plan/IUEA_ML_Roadmap_Benchmark.docx"
FIG = _ROOT + "/figs/"

S1 = "SEMESTER 1"
S2 = "SEMESTER 2"
NO = "NOT COVERED"
HV = "ALREADY HAVE"

d = new_doc(margin_cm=2.2)
header_footer(d, "IUEA Faculty of Engineering · CML3111 / CML3112 / CML3113 · roadmap.sh Benchmark")
first_page_different(d)

spacer(d, 48)
para(d, "INTERNATIONAL UNIVERSITY OF EAST AFRICA · FACULTY OF ENGINEERING",
     size=10.5, bold=True, colour=MID, align=AL.CENTER, after=20)
para(d, "Benchmarked Against the Field", size=25, bold=True, colour=NAVY, align=AL.CENTER, after=4)
para(d, "The two-semester course mapped node by node onto the roadmap.sh Machine Learning roadmap",
     size=13, colour=MID, align=AL.CENTER, after=18)
p = para(d, "WHAT WE TEACH  ·  WHAT WE DEFER  ·  WHAT WE DO NOT TEACH AT ALL", size=11, bold=True,
         align=AL.CENTER, after=8, before=8)
_border(p, "top", NAVY_H, 10)
_border(p, "bottom", NAVY_H, 10)
spacer(d, 18)
para(d, "Source: roadmap.sh/machine-learning · Machine Learning Roadmap, retrieved September 2026",
     size=9.5, colour=GREY, align=AL.CENTER, after=3)
para(d, "Version 1.0 · September 2026", size=9.5, italic=True, colour=GREY, align=AL.CENTER)
page_break(d)

h1(d, "Contents")
toc(d)
page_break(d)

# ================================================================
h1(d, "1. Why benchmark against a public roadmap")
para(d, "A syllabus written in isolation is impossible for a student to place. They cannot tell whether what "
        "they are being taught is the whole field, a sensible subset of it, or an idiosyncratic selection. "
        "Benchmarking the course against roadmap.sh answers that question honestly and in public.")
para(d, "It does three useful things. It shows students where they are on a map the profession actually uses, "
        "rather than one their lecturer invented. It makes the gaps explicit, so nobody finishes the year "
        "believing they have covered reinforcement learning or MLOps when they have not. And it gives the "
        "self-directed students a route onwards, because roadmap.sh publishes separate roadmaps for the AI "
        "engineer, the data scientist, MLOps and AI agents.")
callout(d, "The finding that matters most for this cohort",
        "The roadmap places mathematical foundations — calculus, linear algebra, statistics, probability — as "
        "a major early stage, and for people entering machine learning from computing it is the hardest one. "
        "These students completed it in Years 1 and 2 of an engineering degree. They are not beginning at the "
        "start of the roadmap; they are beginning at stage 3 with stage 2 already behind them. That is worth "
        "telling them in Week 1, because it inverts the assumption that this field belongs to computer "
        "scientists.", MID_H, LIGHT_H)

h1(d, "2. The roadmap, and where the course sits on it")
para(d, "The figure below is issued to students in Week 1 as part of the opening session. Orange is Semester 1, "
        "green is Semester 2, dark blue is the stage they already hold from their degree, and grey is what the "
        "course does not teach.")
d.add_picture(FIG + "roadmap_journey.png", width=Inches(6.9))
spacer(d, 6)
para(d, "Figure 1 — the fifteen teaching stages, grouped from the roadmap.sh Machine Learning roadmap and "
        "colour-coded by when this course reaches them.", size=9.5, italic=True, colour=GREY)

spacer(d, 10)
d.add_picture(FIG + "roadmap_coverage.png", width=Inches(6.9))
spacer(d, 6)
para(d, "Figure 2 — proportional coverage by roadmap section. The grey is the honest gap.",
     size=9.5, italic=True, colour=GREY)

# ================================================================
page_break(d)
h1(d, "3. Node-by-node mapping")
para(d, "The roadmap's own headings are used verbatim in the left column so the mapping can be checked against "
        "the source. Where a node is covered only in part, the part we cover is named.")

h2(d, "Prerequisites and introduction")
table(d, ["roadmap.sh node", "Status", "Where, and what we actually do"],
      [["Python Roadmap (prerequisite)", S1,
        "Weeks 2–4 build Python from zero using engineering formulas the students already know. We do not "
        "attempt the full Python roadmap — no decorators, generators, async or packaging."],
       ["What is an ML Engineer? · ML vs AI Engineer · Skills and responsibilities", S1,
        "Week 1, the new roadmap segment. All four career tracks are shown and the course's position is stated "
        "explicitly: ML applied inside your own engineering discipline."]],
      [30, 14, 56], bold_first=True)

h2(d, "Mathematical foundations")
para(d, "This whole section is the students' existing strength rather than a gap, which is the single most "
        "important observation in this benchmark. We do not re-teach it; we use it and name it when it appears.")
table(d, ["roadmap.sh node", "Status", "Where, and what we actually do"],
      [["Calculus — derivatives, partial derivatives, chain rule, gradient, Jacobian, Hessian", HV,
        "Held from Years 1–2. Referenced in Semester 2 when gradient descent and back-propagation appear. We "
        "never derive it from scratch."],
       ["Linear algebra — matrices and operations, scalars/vectors/tensors, SVD, determinants, eigenvalues", HV,
        "Held from Years 1–2. Matrix shape is used constantly from Week 5 onwards. SVD and eigen-decomposition "
        "are used implicitly inside PCA in Semester 2 but not derived."],
       ["Statistics — descriptive, inferential, graphs and charts", HV,
        "Held, and reinforced practically in Week 6 (distributions, outliers, correlation) rather than taught "
        "as theory."],
       ["Probability — basics, Bayes theorem, random variables, PDFs, distributions", HV,
        "Held. Used when class imbalance and probability outputs appear in Week 9. Bayes is not taught as a "
        "topic and no naive Bayes classifier is covered."],
       ["Discrete mathematics", NO,
        "Not needed for anything in this course."]],
      [30, 14, 56], bold_first=True)

h2(d, "Programming fundamentals and libraries")
table(d, ["roadmap.sh node", "Status", "Where, and what we actually do"],
      [["Basic syntax · variables and data types · data structures · loops · conditionals · exceptions · "
        "functions", S1,
        "Weeks 3 and 4, in that order, each introduced through an engineering calculation rather than an "
        "abstract exercise."],
       ["Object-oriented programming", NO,
        "Deliberately excluded from Semester 1. Beginners do not need classes to do data work, and the time is "
        "better spent on data handling. Students meet objects only as things they use, never as things they "
        "define."],
       ["NumPy · pandas", S1, "Week 5. pandas is the single most heavily weighted tool in the semester."],
       ["Matplotlib · seaborn", S1,
        "Week 6, taught as instruments of detection rather than decoration — every chart must answer a stated "
        "question."]],
      [30, 14, 56], bold_first=True)

h2(d, "Data collection and preprocessing")
table(d, ["roadmap.sh node", "Status", "Where, and what we actually do"],
      [["Data sources — databases (SQL, NoSQL), internet, APIs, mobile apps, IoT", "PART · " + S1,
        "Week 5 covers finding and judging a dataset on Kaggle and the UCI repository, and reading a dataset "
        "card for provenance and licence. SQL, APIs and IoT ingestion are NOT taught — a real gap, and the "
        "most defensible candidate for adding to Semester 2."],
       ["Data formats — CSV, Excel, JSON, Parquet", "PART · " + S1,
        "CSV throughout, Excel in passing. JSON and Parquet are not covered."],
       ["Data cleaning", S1,
        "Week 6 in depth: missingness, duplicates, impossible values, dtype repair, outlier judgement, with "
        "marks awarded for the justification rather than the fix."],
       ["Feature engineering · feature selection", S1,
        "Week 11, framed as the place where the students' domain knowledge beats a better programmer."],
       ["Feature scaling and normalisation", S1,
        "Week 11, always inside a scikit-learn Pipeline so that leakage is structurally prevented."],
       ["Dimensionality reduction", S2, "With PCA in Semester 2."]],
      [30, 14, 56], bold_first=True)

page_break(d)
h2(d, "Machine learning core")
table(d, ["roadmap.sh node", "Status", "Where, and what we actually do"],
      [["What is machine learning? · types of machine learning", S1,
        "Week 1 for the framing, Week 8 for the formal treatment. Supervised, unsupervised and reinforcement "
        "are all NAMED in Week 1 so the vocabulary exists early."],
       ["Semi-supervised · self-supervised learning", NO,
        "Named in passing only. Neither is teachable at this level in the time available."],
       ["scikit-learn — data loading, train-test split, data preparation, model selection, tuning, prediction",
        S1, "Weeks 8 to 12. The fit / predict / score pattern is named explicitly in Week 8 as the pattern "
            "every later model reuses."],
       ["Supervised learning — regression: linear, polynomial", S1,
        "Week 8 for linear regression. Polynomial is demonstrated but not examined."],
       ["Regularisation — Lasso, Ridge, ElasticNet", "PART · " + S2,
        "Not in Semester 1. Introduced in Semester 2 alongside overfitting control. A genuine gap in the first "
        "semester and stated as such."],
       ["Classification — logistic regression, decision trees, random forest", S1, "Week 9."],
       ["Classification — K-nearest neighbours, support vector machines", "PART · " + S2,
        "Not in Semester 1. KNN is a good teaching algorithm and its omission is a deliberate time trade, not "
        "an oversight."],
       ["Gradient boosting machines", S2,
        "Demonstrated for sixty seconds in Week 12 and then explicitly deferred, with the students told why: "
        "the tool is not the lesson."],
       ["Unsupervised learning — clustering (exclusive, overlapping, hierarchical, probabilistic)", S2,
        "Semester 2. Only k-means and hierarchical clustering are realistically reachable."],
       ["Unsupervised learning — PCA, autoencoders", S2,
        "PCA in Semester 2. Autoencoders only if the deep learning block runs ahead of schedule."],
       ["Reinforcement learning — Q-learning, deep-Q networks, policy gradient, actor-critic", NO,
        "Not covered anywhere in either semester. It needs a simulator and a different mental model, and there "
        "is no honest way to fit it. Students are told this in Week 1."]],
      [30, 14, 56], bold_first=True)

h2(d, "Model evaluation — the course's centre of gravity")
para(d, "This is the section where the course goes deeper than the roadmap implies, deliberately. Engineering "
        "students will be asked to sign their name under a prediction, so 'how do I know I can trust this' "
        "carries more weight here than in a general course.")
table(d, ["roadmap.sh node", "Status", "Where, and what we actually do"],
      [["What is model evaluation? Why is it important?", S1,
        "Week 10, an entire three-hour session, plus the concept is seeded in Week 1 through the hand-prediction "
        "exercise where students measure their own error."],
       ["Metrics — accuracy, precision, recall, F1, ROC-AUC, log loss, confusion matrix", S1,
        "Week 9 and Week 10. Accuracy, precision, recall, F1 and the confusion matrix in full. ROC-AUC is "
        "introduced; log loss is named but not examined."],
       ["Validation techniques — k-fold cross-validation", S1,
        "Week 10, reported as a mean with a spread rather than a single number."],
       ["Leave-one-out cross-validation", NO, "Mentioned only. Rarely the right choice at these dataset sizes."],
       ["Data leakage", "S1 — BEYOND THE ROADMAP",
        "The roadmap does not list leakage as a node. We give it half of Week 10, because it is the defect most "
        "likely to appear in a student project and in professional practice, and it produces a model that looks "
        "excellent and is useless."]],
      [30, 14, 56], bold_first=True)

page_break(d)
h2(d, "Deep learning and beyond — Semester 2")
table(d, ["roadmap.sh node", "Status", "Where, and what we actually do"],
      [["Neural network basics — perceptron, MLP, forward and back propagation, activation and loss functions",
        S2, "Semester 2. The engineering cohort's calculus makes back-propagation teachable rather than "
            "hand-waved."],
       ["Deep learning libraries — TensorFlow, Keras, PyTorch", "PART · " + S2,
        "PyTorch only. Teaching two frameworks to beginners halves the depth in both."],
       ["Convolutional neural networks — convolution, pooling, padding, strides", S2,
        "Semester 2, with transfer learning, because training from scratch is not realistic on the available "
        "hardware."],
       ["Applications of CNNs — image classification, segmentation, recommendation systems", "PART · " + S2,
        "Image classification yes; segmentation and recommenders no."],
       ["Recurrent neural networks — RNN, GRU, LSTM", "PART · " + S2,
        "Semester 2 time-series block. Classical time-series methods come first because they are more often the "
        "right answer on engineering sensor data."],
       ["Attention mechanisms — self-attention, transformers, multi-head attention", "PART · " + S2,
        "Conceptually only, in the generative AI block. Students will use transformers; they will not implement "
        "one."],
       ["Autoencoders · generative adversarial networks", NO, "Neither is reachable in the time."],
       ["Explainable AI", S2,
        "Semester 2, and treated as a professional requirement rather than a curiosity — a model that cannot be "
        "explained often cannot be used, whatever its accuracy."],
       ["NLP — tokenisation, stemming, lemmatisation, embeddings, attention models", "PART · " + S2,
        "Tokenisation and embeddings conceptually, in service of retrieval over engineering documentation. "
        "Stemming and lemmatisation are not covered."],
       ["MLOps", "PART · " + S2,
        "Reproducibility, environment capture and a simple deployed interface. Not CI/CD, monitoring, "
        "registries or serving infrastructure — roadmap.sh has a separate MLOps roadmap and that is the honest "
        "answer."]],
      [30, 14, 56], bold_first=True)

# ================================================================
h1(d, "4. The four gaps I would defend, and the two I would not")
para(d, "Every course omits things. The distinction worth drawing is between an omission that is a considered "
        "trade and one that is simply a shortfall.")
h3(d, "Defensible")
para(d, "Reinforcement learning is absent because it needs a simulator, a different mental model and a term of "
        "its own. Object-oriented programming is absent because beginners do not need to define classes to do "
        "data work. TensorFlow and Keras are absent because teaching two frameworks halves the depth in both. "
        "Generative adversarial networks and autoencoders are absent because they would displace something the "
        "students will actually use.")
h3(d, "Harder to defend, and worth revisiting")
para(d, "The first is data ingestion. The roadmap lists databases, APIs and IoT as data sources; we teach CSV "
        "files from a course share. Real engineering data lives in historians, SCADA systems and databases, and "
        "a graduate who can only read a CSV will be stuck on their first day. A single session on SQL and one "
        "API call would close most of this, and Semester 2 is the place for it.")
para(d, "The second is regularisation, and K-nearest neighbours and support vector machines alongside it. "
        "Semester 1 teaches linear regression, logistic regression, trees and forests, which is enough to work "
        "with — but Ridge and Lasso are the natural companions to the overfitting session in Week 10, and "
        "leaving them out means the students meet the problem without one of its standard answers.")

h1(d, "5. How this is used with students")
table(d, ["When", "How the roadmap is used"],
      [["Week 1, segment 2", "Fifteen minutes walking the whole field, start to finish, so that every later "
                             "topic has somewhere to sit. Students are pointed at roadmap.sh/machine-learning "
                             "to explore the interactive version themselves."],
       ["Week 1, same segment", "The stage-2 observation: they already hold the mathematics. This is the most "
                                "motivating thing they hear all week and it is true."],
       ["Week 1, coverage figure", "The gaps are shown deliberately. Being honest about what is not taught buys "
                                   "credibility for everything that is."],
       ["Start of each block", "One slide re-showing the roadmap with the current stage highlighted, so "
                               "progress is visible rather than assumed."],
       ["Week 15", "The roadmap returns beside the capability ladder. Students see how far along a public "
                   "professional map they have travelled in fifteen weeks, and where to go next."],
       ["Semester 2, final session", "The related roadmaps — AI engineer, data scientist, MLOps, AI agents — are "
                                     "issued as the route onwards for anyone who wants to continue."]],
      [22, 78], bold_first=True)

spacer(d, 12)
callout(d, "One caution on using any roadmap with beginners",
        "A roadmap shows the territory; it does not teach it, and a student who mistakes reading the map for "
        "walking it will feel productive and learn nothing. Show it, let them see the shape of the field, then "
        "close it and go back to the twelve rows of data on the desk. The roadmap is orientation at the start "
        "of a session, never the substance of one.", "C55A11", AMBER_H)

spacer(d, 10)
para(d, "Benchmark version 1.0 · September 2026 · roadmap.sh content retrieved September 2026 and worth "
        "re-checking each year, as the roadmap is actively maintained.",
     size=9, italic=True, colour=GREY, align=AL.CENTER)

d.save(OUT)
print("saved", OUT)
