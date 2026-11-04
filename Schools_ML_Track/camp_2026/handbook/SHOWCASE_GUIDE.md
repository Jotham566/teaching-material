# What a great project shows

This guide describes a project that is a pleasure to present. Use it while you build, as a checklist before the showcase, and as the base for the instructor's friendly feedback. It gives no scores and has no weights. A project does not have to tick every box to be worth showing. Choose the next box you can reach.

## The checklist

| What the project shows | What to look for |
|---|---|
| A clear question | One narrow question, a named reader or use, and units that match the question. |
| Where the data came from | The source is named. Invented or teaching data is described as invented. Real data is used with its licence read and with permission. |
| Careful preparation | The raw file is kept unchanged. Missing values, duplicates and types were checked and each decision is written down. A line saying "no changes needed" is a good entry when it is true. |
| A notebook that reruns | Restart the kernel and run all cells from the top. The notebook gives the same answers with no hidden steps. |
| A fair comparison (Machine Learning) | A plain-guess baseline fitted on training rows only. Candidate models compared on the same validation rows with the same measure. The held-back set used once, at the end, and reported next to validation. Inputs known before the answer, with no leakage column. |
| Checks you can show (Data Analysis) | Each headline total confirmed a second way, for example pandas against NumPy, or a merged total against the unmerged one. A merge uses a unique key and the row count is unchanged or explained. Charts have labels and units. |
| Honest limits | At least one clear limit of the data or method, written next to the result. A cautious conclusion with no claim about cause that the data cannot support. |
| An easy handover | Files open. The report ties the question to results that can be traced to a notebook cell. The data dictionary and AI_USE_LOG.md are complete. |
| A clear talk | Five slides, about five minutes, one idea on each. A listener can say what was compared, the biggest finding and the limit. |

## Things that are fine

- A model that does not beat the baseline, when the method is sound and the result is reported plainly. It is an honest finding.
- A small project that is finished and clear.
- A talk with a nervous start. Confidence and accent are not part of the project.

## Things that are not needed

- A high model score, a large model or an interactive dashboard.
- Fancy slide design.
- Any tool that was not taught in the camp.
- AI help. A short AI_USE_LOG.md that says what you used and what you checked is enough. It shows honest working.

## For the instructor

Use the checklist to find one strength and one next step for each learner. Point to the file, cell or chart that you mean. If an explanation is unclear, ask the learner to explain and rerun a small part, and offer a catch-up chat. Do not infer misconduct from writing style or from an AI detector. Where a numeric result comes from the supplied data, check it against instructor_materials/reference_values.json. The values apply to the supplied camp_shop and Sunrise Shops data only.

Offer accessible ways to show the same work. Keep the notes private.
