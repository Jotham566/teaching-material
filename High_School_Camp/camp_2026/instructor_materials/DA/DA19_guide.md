# DA19 Instructor guide: Project question and a safe plan

Private. Keep this file out of the student folder.

**Objective.** By the end: you can write a narrow project plan with a question, the data, the measures, the charts and the limits, and have it approved.

**Question of the day.** Which three questions can our data answer, and how will we show the answers?

**Where this is used.** Data teams write a short plan before any code: the question, the data, the charts and what the data cannot say. Which three questions about a topic you love could a table answer?

Prerequisite: DA18 Does your total match the true total? Clean, merge and reconcile.

## The 180 minutes

| Minutes | Activity |
|---|---|
| 10 | Recall: retrieve yesterday, three questions on paper |
| 50 | Block A: predict, run, investigate, modify |
| 15 | Break away from screens |
| 50 | Block B: predict, run, investigate, modify |
| 40 | Make: the independent task and the project journal |
| 15 | Exit ticket, save, and an individual check with each learner |

Where it overruns: Approve plans one at a time. A plan that is too big is the most common reason a project fails in week 8.

## Block A. From a topic to three questions

A project serves a reader. Start with the topic on your progress map. Decide who needs the answer and what choice it could help with. Review AI_USE_POLICY.md now. Any permitted supervised AI help is written in AI_USE_LOG.md, and your own attempt always comes first. No forecasting or model training is required.

Ask for the prediction first: Predict which of these questions the Sunrise Shops data can answer with the taught methods: (a) Which category earns the most at each branch? (b) Why do people like Campus Gate? (c) What will sales be next month?

Correct result: Question (a) can be answered: it needs the sales, products and branches tables, a merge and a group total. Question (b) asks for reasons, and the data has no opinions. Question (c) asks for a forecast, which this course does not teach. A narrow descriptive question with named columns is the right size.

Investigate, with answers:

- What makes question (a) answerable? Answer: Every column it needs exists, and the method is one we have used.
- How would you narrow question (b) so the data can answer it? Answer: Ask something countable, such as which shop has the highest revenue per customer.

Modify: Write one more question the Sunrise data can answer, and name the columns it needs. Answer: Any narrow question with named columns, for example: did the Sugar price rise change its units sold? It needs product_id, units and sale_date.

## Block B. The plan and the data

Your PROJECT_PLAN.md has seven headings: question, reader and use, data source and licence, measures and columns, method, charts, limitations. Start with Sunrise Shops, which is invented and needs no permission. You may use a public real dataset, for example from the Uganda Bureau of Statistics or the World Bank, once the licence has been read at the source, the instructor has approved it, and it holds no personal information.

Ask for the prediction first: Predict which heading is hardest to write, and why.

Correct result: Most learners find limitations hardest, because it means saying what the data cannot show. A good limitation names a missing column or a kind of conclusion the project will not draw: no costs means no profit, invented data means no claim about real shops.

Investigate, with answers:

- Why must the licence be read at the source? Answer: The licence says what you may do with the data. Only the owner of the data can tell you.
- What goes in the data dictionary? Answer: Each column you use, its meaning and its unit.

Modify: Write the limitations heading for your own plan in two sentences. Answer: Two sentences naming what the data cannot show.

## Make: reference

An acceptable plan names Sunrise Shops (invented) or an approved public dataset with its licence read at the source. Its three questions are descriptive and name their columns. Example: (1) Which category earns the most at each branch? Needs sales, products, branches. (2) Which branch earns the most per customer counted? Needs sales and daily_summary. (3) Did the Sugar price rise on day 31 change its units sold? Needs product_id, units, sale_date. Limitations: invented data, no costs so no profit, no claim about real shops. If the plan promises profit, change the measure to revenue. If it promises a forecast, make it descriptive.

Build log entry to look for: PROJECT_PLAN.md approved by the instructor, with a data dictionary for the columns used.

## Misconceptions to listen for

- A bigger question is a better project.
- Real data is always better than invented data.
- Limitations make the project look weak.

## Questions to ask, with expected answers

- Which columns does your first question need? Expected: Each one is named, and each is in the data dictionary.
- Who is the reader and what could they decide? Expected: A named reader and a concrete choice.

## Online version

For a hybrid group. The live class is 90 minutes on video with screen sharing. The learner finishes the build in their own time, about an hour. The full rules are in handbook/HYBRID_DELIVERY.md.

### Live clock, 90 minutes

| Minutes | Activity |
|---|---|
| 5 | Recall: three questions on paper, then say the answers aloud |
| 35 | Block A, From a topic to three questions: predict, run, investigate. The Modify step moves to the build task. |
| 5 | Break away from the screen |
| 35 | Block B, The plan and the data: predict, run, investigate. The Modify step moves to the build task. |
| 10 | Close: say the exit sentence aloud, then the build task is set |

### After-class build task, about an hour

1. Modify, Block A (From a topic to three questions): Write one more question the Sunrise data can answer, and name the columns it needs.
2. Modify, Block B (The plan and the data): Write the limitations heading for your own plan in two sentences.
3. Make: Write PROJECT_PLAN.md with the seven headings. Start from the topic on your progress map and choose the supplied data file that fits it best. Real public data is used only after you and the instructor have read its licence. Name the data file and its licence or its invented status. List the three questions, the columns each needs, the charts and the limitations. Ask the instructor to approve a narrow scope before you build.

When you finish, write two sentences: what you changed and how you checked it. Add a build log entry. Send a photo of your work or the notebook by the route the organiser sets, before the next class.

### Next class

In the next class recall, ask: Which columns does your first question need? Expected: Each one is named, and each is in the data dictionary.

## Build log and feedback

Look at what each of the five learners saved and note one strength and one next step for each. Share them kindly and privately. Nothing is scored or ranked. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and show-and-tells need your judgement.
