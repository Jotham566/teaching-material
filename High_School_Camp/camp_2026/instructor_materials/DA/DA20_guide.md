# DA20 Instructor guide: Build a reliable analysis

Private. Keep this file out of the student folder.

**Objective.** By the end: you can build the calculations for your project so that each one is checked by hand and by a second route, and a partner can rerun them.

**Question of the day.** Can a stranger follow my steps from the raw file to my numbers?

**Where this is used.** A result is only useful if someone else can repeat it. Analysts log each step and check each number two ways. Who could rerun your analysis and get the same numbers?

Prerequisite: DA19 Project question and a safe plan.

## The 180 minutes

| Minutes | Activity |
|---|---|
| 15 | recall, then plan check |
| 50 | build calculations with hand checks |
| 15 | break away from screens |
| 50 | build second routes and reconcile |
| 35 | partner reruns one calculation and returns feedback |
| 15 | exit ticket, save and individual check |

Where it overruns: Each learner needs the instructor for a few minutes. Plan the order of visits before the session.

## Make: reference

Check that: the raw file is untouched; the cleaning log counts every row removed or excluded; each calculation has a hand check on a five-row sample; each total reconciles with a second route; row counts are printed after every merge; the partner can rerun the notebook from a restarted kernel.

Build log entry to look for: A notebook that reruns from the top, a cleaning log, and a partner note recording one rerun and the first discrepancy fixed.

## Misconceptions to listen for

- If the code runs, the numbers are right.
- A cleaning log is only needed when something was changed.
- A partner rerun is a test of the partner.

## Questions to ask, with expected answers

- How do you check a total you cannot count by hand? Expected: Take five rows, work them out on paper, and compare with the code on the same five rows.
- What does your row count show after the merge? Expected: It matches the count before the merge, or you can explain every extra row.

## Online version

For a hybrid group. The live class is 90 minutes on video with screen sharing. The learner finishes the build in their own time, about an hour. The full rules are in handbook/HYBRID_DELIVERY.md.

### Live clock, 90 minutes

| Minutes | Activity |
|---|---|
| 5 | Recall: three questions on paper, then say the answers aloud |
| 35 | Read the brief together on the shared screen, then the first build step. Each learner shares their screen in turn. |
| 5 | Break away from the screen |
| 35 | Learners keep building. The instructor visits each learner by screen share, about seven minutes each. |
| 10 | Close: say the exit sentence aloud, then the rest of the build task is set |

### After-class build task, about an hour

1. Make: Work from a protected copy of the raw data. Write the cleaning log, including a log that says no change was needed if that is true. Build one calculation at a time. For each, compare with a small hand-worked example and with a second route (pandas against NumPy, or a merged total against an unmerged one). Ask a partner to rerun one calculation from your notebook. Write down the first discrepancy they find and fix it.

When you finish, write two sentences: what you changed and how you checked it. Add a build log entry. Send a photo of your work or the notebook by the route the organiser sets, before the next class.

### Next class

In the next class recall, ask: How do you check a total you cannot count by hand? Expected: Take five rows, work them out on paper, and compare with the code on the same five rows.

This is a work session. Keep the live part for the brief and for individual check-ins. The learner builds in the live time and after class.

## Build log and feedback

Look at what each of the five learners saved and note one strength and one next step for each. Share them kindly and privately. Nothing is scored or ranked. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and show-and-tells need your judgement.
