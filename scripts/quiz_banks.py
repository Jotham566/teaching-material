# -*- coding: utf-8 -*-
"""Question banks for the twelve weekly quizzes.

Single source of truth. `build_quiz_forms_gs.py` embeds this into the Apps
Script that creates the Google Forms, and the same data drives the printed
paper fallback used when the room network is down.

STRUCTURE
  QUIZ[week] = {
    "title":  the form title students see,
    "intro":  the form description,
    "mix":    a note on the question mix for this week,
    "q":      list of questions. A question is a dict:
                stem       the question text, shown to every cohort
                stem_by    optional {code: text} to replace stem per cohort
                pre        optional monospace block shown above the options
                pre_by     optional {code: text} per cohort
                options    list of (text, is_correct, feedback)
                kind       diagnosis | traceback | interpretation | judgement
  }

THE MIX RULE, AND WHY WEEKS 1 AND 2 DIFFER
The standing rule is two diagnosis / one traceback / one interpretation / one
judgement per quiz. That rule assumes the students have written code. In Week 1
they have not: the session is entirely on paper and nobody has opened a
notebook. Week 2 is their first notebook, so a traceback question is fair but a
"silently wrong answer" question is not yet.

So Weeks 1 and 2 carry a different mix, stated per quiz below, and the standing
rule applies from Week 3 onward. Pretending otherwise would mean writing Week 1
questions about code the class has never seen, which is exactly the kind of
question the design rule exists to forbid.

EVERY OPTION CARRIES FEEDBACK. The wrong options are the plausible
misdiagnoses, not throwaways, and each one explains why it is wrong. That
feedback is the teaching, and it is the reason the quiz is worth five minutes.
"""

# Cohort codes, for the per-cohort stems
CODES = ("CML3112", "CML3113", "CML3111")

QUIZ = {}

# ==========================================================================
# QUIZ 1 — Week 1. No code yet: the class has not opened a notebook.
# Mix: 3 interpretation, 1 diagnosis of a mis-framed problem, 1 judgement.
# ==========================================================================
QUIZ[1] = {
    "title": "Weekly Quiz 1 — What machine learning is",
    # The mechanics (time, marks, attempts) are appended by
    # build_quiz_forms_gs.py as a HOW THIS WORKS block, so saying them here
    # too just repeated the same facts twice on the student's screen.
    "intro": ("Nothing here can be answered without reading what it shows "
              "you."),
    "mix": ("3 interpretation, 1 diagnosis, 1 judgement. No code questions this "
            "week, because the class has not written any code yet."),
    "q": [
        # ---- 1. read the table: which column is the target
        {
            "kind": "interpretation",
            "stem": "In the table below, which column is the TARGET?",
            "pre_by": {
                "CML3112":
                    "mix_id  cement  water  age_days  strength_mpa\n"
                    "M-001     380     190        28          41.2\n"
                    "M-002     420     185        28          46.8\n"
                    "M-003     310     200        28          32.5",
                "CML3113":
                    "sample_id  iron_feed  starch_flow  pulp_ph  silica_pct\n"
                    "S-001           56.3          3180      9.4        2.11\n"
                    "S-002           58.1          3320      9.6        1.84\n"
                    "S-003           54.7          2980      9.1        2.63",
                "CML3111":
                    "hour_id  air_temp  rot_speed  torque_nm  failed\n"
                    "H-001        298.4       1551       42.8       0\n"
                    "H-002        299.1       1408       46.3       0\n"
                    "H-003        300.2       1379       61.7       1",
            },
            "options_by": {
                "CML3112": [
                    ("strength_mpa", True,
                     "Correct. It is the quantity you want to predict, and it is the "
                     "one you would not have at the moment of prediction."),
                    ("mix_id", False,
                     "That is an identifier. It labels the row and predicts nothing. "
                     "Feed it to a model and the model will memorise it."),
                    ("cement", False,
                     "That is a feature. You know it when you batch the mix, which is "
                     "before you know the strength."),
                    ("age_days", False,
                     "That is a feature, and in this table it is the same for every "
                     "row, which makes it useless as well as a feature."),
                ],
                "CML3113": [
                    ("silica_pct", True,
                     "Correct. It is the assay you are waiting an hour for, and the "
                     "reason for predicting it at all."),
                    ("sample_id", False,
                     "That is an identifier. It labels the row and predicts nothing."),
                    ("iron_feed", False,
                     "That is a feature. You measure it as the feed goes in, before "
                     "the assay comes back."),
                    ("pulp_ph", False,
                     "That is a feature: a process variable you already measure "
                     "continuously."),
                ],
                "CML3111": [
                    ("failed", True,
                     "Correct. It is what you want to know in advance, and the only "
                     "column here you would not have before the fact."),
                    ("hour_id", False,
                     "That is an identifier. It labels the row and predicts nothing."),
                    ("torque_nm", False,
                     "That is a feature: a sensor reading available while the machine "
                     "is running."),
                    ("air_temp", False,
                     "That is a feature, measured continuously by the plant."),
                ],
            },
        },
        # ---- 2. regression or classification
        {
            "kind": "interpretation",
            "stem_by": {
                "CML3112": "You want to predict, for a mix that has not been cast "
                           "yet, whether it will fall into the class 'below 25 MPa', "
                           "'25 to 40 MPa' or 'above 40 MPa'. What kind of problem "
                           "is this?",
                "CML3113": "You want to predict, for each sample, whether the "
                           "material is 'ore' or 'waste' against a stated cut-off "
                           "grade. What kind of problem is this?",
                "CML3111": "You want to predict, for the next shift, whether a "
                           "machine will fail or not. What kind of problem is this?",
            },
            "options": [
                ("Classification, because the answer is one of a fixed set of "
                 "categories", True,
                 "Correct. The answer is a label from a fixed list, so it is "
                 "classification, and it is scored with a confusion matrix rather "
                 "than an average error."),
                ("Regression, because the underlying quantity is a number", False,
                 "The underlying quantity is a number, but the question asked is not. "
                 "You are asked which band or class it falls into, and a band is a "
                 "category. What decides this is the question you were asked rather "
                 "than the quantity the sensor happens to record."),
                ("Regression, because there are more than two possible answers", False,
                 "The number of possible answers does not decide this. Classification "
                 "with three classes is still classification."),
                ("Neither, because it can be written as a rule with thresholds", False,
                 "If you already have the strength or the grade then yes, a rule is "
                 "the right tool and there is nothing to learn. The point here is that "
                 "you do not have it yet."),
            ],
        },
        # ---- 3. diagnosis of a mis-framed problem
        {
            "kind": "diagnosis",
            "stem": ("A team proposes to predict the target using the list of "
                     "columns below. One column makes the whole exercise "
                     "meaningless. Which one, and why?"),
            "pre_by": {
                "CML3112": "target:   whether the cylinder passed the 28-day test\n"
                           "features: cement, water, age_days,\n"
                           "          strength_mpa_measured_at_28_days",
                "CML3113": "target:   whether the concentrate met specification\n"
                           "features: iron_feed, starch_flow, pulp_ph,\n"
                           "          laboratory_silica_assay",
                "CML3111": "target:   whether the machine failed in the next shift\n"
                           "features: air_temp, rot_speed, torque_nm,\n"
                           "          maintenance_action_taken",
            },
            "options_by": {
                "CML3112": [
                    ("strength_mpa_measured_at_28_days — it IS the answer, recorded "
                     "at the moment the answer becomes known", True,
                     "Correct. Ask the timing question: at the moment I need this "
                     "prediction, would I have this number? You would not. A model "
                     "given it scores near-perfectly and predicts nothing in service."),
                    ("age_days — every row has the same value so it carries no "
                     "information", False,
                     "A constant column is useless, and that is worth spotting. But "
                     "useless is not the same as fatal: it wastes a column rather than "
                     "invalidating the result."),
                    ("water — it is already implied by the cement content", False,
                     "Water and cement are related through the mix design, but both "
                     "are legitimately known before casting. Correlated features are "
                     "a modelling nuisance and this one is not fatal."),
                    ("None of them; the list is fine", False,
                     "One of these columns is only recorded once the outcome is known. "
                     "Go back and ask the timing question of each one."),
                ],
                "CML3113": [
                    ("laboratory_silica_assay — it IS the answer, and it is the thing "
                     "you were waiting an hour for", True,
                     "Correct. Ask the timing question: at the moment I need the "
                     "prediction, would I have this number? The assay is exactly what "
                     "you do not have yet, which was the whole point."),
                    ("pulp_ph — it is controlled to a set point so it barely varies",
                     False,
                     "A column with little variation contributes little, and that is "
                     "worth noticing. It does not invalidate the exercise."),
                    ("starch_flow — reagent flow is set by the operator, not measured",
                     False,
                     "A set value is still a legitimate input known at prediction "
                     "time. Provenance matters, but this one is not fatal."),
                    ("None of them; the list is fine", False,
                     "One of these columns is the laboratory result you are trying to "
                     "predict. Ask the timing question of each one."),
                ],
                "CML3111": [
                    ("maintenance_action_taken — it is recorded in response to the "
                     "failure, so it only exists once the answer is known", True,
                     "Correct. Ask the timing question: at the moment I need this "
                     "prediction, would I have this? The maintenance action follows "
                     "the failure, so it cannot precede the prediction."),
                    ("rot_speed — it is set by the controller rather than measured",
                     False,
                     "A commanded value is still available at prediction time. That "
                     "raises a provenance question and it is not a fatal one."),
                    ("air_temp — ambient temperature does not cause a bearing to fail",
                     False,
                     "A weak feature is not a fatal feature. It may contribute little "
                     "and the ablation table in Week 11 is how you find that out."),
                    ("None of them; the list is fine", False,
                     "One of these columns is only recorded after the outcome. Ask the "
                     "timing question of each one."),
                ],
            },
        },
        # ---- 4. interpretation: rule or learned model
        {
            "kind": "interpretation",
            "stem_by": {
                "CML3112": "A durability code states that a crack wider than 0.30 mm "
                           "must be flagged for repair. You have the crack widths. "
                           "What should you build?",
                "CML3113": "An economic calculation gives the cut-off grade, and you "
                           "have the assayed grade for every block. What should you "
                           "build?",
                "CML3111": "The motor datasheet gives a 130 °C alarm limit, and you "
                           "have the winding temperature. What should you build?",
            },
            "options": [
                ("A rule with a threshold, written directly in code", True,
                 "Correct. You have the input and you have the threshold, so there is "
                 "nothing to learn. Training a model to rediscover a published limit "
                 "adds error and removes the audit trail."),
                ("A classifier trained on past decisions", False,
                 "It would work, and that is what makes this tempting. It would also "
                 "be less accurate than the rule, harder to defend and impossible to "
                 "audit against the code of practice."),
                ("A regression model to predict the threshold", False,
                 "The threshold is given. There is nothing to predict about it."),
                ("Either; the choice is a matter of preference", False,
                 "The choice follows from whether you already have the input and the "
                 "threshold. Here you have both, so the rule wins on every axis."),
            ],
        },
        # ---- 5. judgement under a stated constraint
        {
            "kind": "judgement",
            "stem": ("A client will only accept a system if every decision it makes "
                     "can be explained line by line to a regulator. Two candidate "
                     "approaches perform identically on your data. Which do you "
                     "recommend, and on what grounds?"),
            "options": [
                ("The one whose decisions can be read out and traced, because the "
                 "constraint decides it once performance is equal", True,
                 "Correct. When performance is equal the constraint is the deciding "
                 "criterion, and explainability was stated as a condition of "
                 "acceptance rather than a preference."),
                ("Whichever scored fractionally higher on the test set", False,
                 "A fractional difference on one test set is usually inside the noise, "
                 "and Week 10 shows you how to measure that. Even a real difference "
                 "would not override a stated condition of acceptance."),
                ("The more sophisticated one, because it will generalise better", False,
                 "Sophistication does not imply generalisation, and on equal "
                 "performance there is no evidence for the claim. It also ignores the "
                 "constraint you were given."),
                ("Neither; tell the client the constraint is unreasonable", False,
                 "Regulatory explainability is a normal engineering constraint. Part "
                 "of the job is delivering within it."),
            ],
        },
    ],
}

# ==========================================================================
# QUIZZES 2 to 12 — topics fixed, questions still to author.
# The Apps Script creates each form with its real title, description and
# question mix note, and one placeholder question, so the whole mechanism can
# be tested end to end before the content exists. Replace the placeholder with
# five real questions bank by bank.
# ==========================================================================
_TOPICS = {
    2:  ("Notebooks and version control",
         "1 traceback, 3 interpretation, 1 judgement. No silent-wrong-answer "
         "question yet: this is their first notebook.",
         "Out-of-order execution diagnosed from a cell-numbering trace, what "
         "Restart and Run All proves, reading one git status output, and the "
         "setup-readiness question."),
    3:  ("Python as an engineering calculator", None,
         "A unit error that returns a plausible wrong number, a function that "
         "prints instead of returning, an if-chain with its branches in the "
         "wrong order, and one traceback."),
    4:  ("Collections, loops and files", None,
         "An accumulator reset inside the loop, a range off by one, a value "
         "read from a file as a string, and a skipped-row count never "
         "reported."),
    5:  ("pandas, and judging a dataset", None,
         "A mask confused with a filtered frame, a groupby result whose shape "
         "is misread, a numeric column with dtype 'object', and provenance."),
    6:  ("Dirty data, and seeing it", None,
         "A zero-coded missing value, a chart that does not answer its stated "
         "question, and an extreme value to judge as error or reality."),
    8:  ("Learning from data: the first model", None,
         "A score quoted on the training rows, a residual plot read the wrong "
         "way round, MAE against RMSE on the same data, and a missing "
         "baseline."),
    9:  ("Classification", None,
         "A confusion matrix read for what the model does badly, an accuracy "
         "figure quoted without the class balance, and a threshold moved with "
         "its effect on each cell."),
    10: ("Can I trust this model?", None,
         "Train and test scores matched to one of the three error stories, "
         "four pipelines with one that leaks, and a cross-validated score "
         "quoted without its spread."),
    11: ("Features", None,
         "An ablation table read for which feature earned its place, a one-hot "
         "encoding on a high-cardinality column, and a scaler that made no "
         "difference to a tree."),
    12: ("Model comparison (integrative)", None,
         "Whether a difference between two models is real given the fold "
         "spread, and which model a stated client constraint selects. TWO of "
         "the five are drawn from the Week 1-10 banks."),
    13: ("Reproducibility (integrative)", None,
         "A notebook that will not run on another machine, a hard-coded path, "
         "and a seed that was never set. TWO of the five are drawn from "
         "earlier banks."),
}

_DEFAULT_MIX = ("2 diagnosis of a silently wrong answer, 1 traceback, "
                "1 interpretation, 1 judgement.")

for _wk, (_title, _mix, _plan) in _TOPICS.items():
    QUIZ[_wk] = {
        "title": f"Weekly Quiz {'1' if _wk == 1 else ''}"
                 f"{[1,2,3,4,5,6,None,7,8,9,10,11,12][_wk-1]} — {_title}",
        "intro": ("Read what each question shows you. None of them can be "
                  "answered without it."),
        "mix": _mix or _DEFAULT_MIX,
        "plan": _plan,
        "q": [],           # empty means: create the form with a placeholder
    }

# Quiz number as students see it: Weeks 1-6 are quizzes 1-6, Weeks 8-13 are 7-12.
QUIZ_NUMBER = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6,
               8: 7, 9: 8, 10: 9, 11: 10, 12: 11, 13: 12}

for _wk, _n in QUIZ_NUMBER.items():
    if _wk in _TOPICS:
        QUIZ[_wk]["title"] = f"Weekly Quiz {_n} — {_TOPICS[_wk][0]}"

# The eleven remaining banks live in their own module to keep this file
# readable. Merging them here keeps QUIZ the single thing every consumer
# reads, so nothing downstream needs to know the banks are split in two.
from quiz_bank_weeks import BANKS as _BANKS       # noqa: E402

for _wk, _qs in _BANKS.items():
    if _wk not in QUIZ:
        raise KeyError(f"quiz_bank_weeks defines week {_wk}, which is not a "
                       f"quiz week. Quiz weeks are {sorted(QUIZ)}.")
    QUIZ[_wk]["q"] = _qs


def authored():
    """Weeks whose five questions are written."""
    return sorted(w for w, q in QUIZ.items() if q["q"])


def pending():
    """Weeks still needing their five questions."""
    return sorted(w for w, q in QUIZ.items() if not q["q"])


def stem_for(q, code):
    return q.get("stem_by", {}).get(code, q.get("stem", ""))


def pre_for(q, code):
    return q.get("pre_by", {}).get(code, q.get("pre"))


def options_for(q, code):
    return q.get("options_by", {}).get(code, q.get("options", []))


if __name__ == "__main__":
    print(f"weeks with quizzes: {sorted(QUIZ)}")
    print(f"authored: {authored()}")
    print(f"pending : {pending()}")
    for w in authored():
        for code in CODES:
            for i, q in enumerate(QUIZ[w]["q"], 1):
                opts = options_for(q, code)
                ncorrect = sum(1 for _, c, _ in opts if c)
                assert len(opts) == 4, f"W{w} Q{i} {code}: {len(opts)} options"
                assert ncorrect == 1, f"W{w} Q{i} {code}: {ncorrect} correct"
                assert all(fb.strip() for _, _, fb in opts), \
                    f"W{w} Q{i} {code}: an option has no feedback"
                assert stem_for(q, code).strip(), f"W{w} Q{i} {code}: no stem"
        print(f"  Week {w}: {len(QUIZ[w]['q'])} questions, "
              f"4 options each, 1 correct each, all options carry feedback — OK")
