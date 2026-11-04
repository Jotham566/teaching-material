# Build system

The pack is generated. Edit the lessons, then rebuild.

| Path | What it is |
|---|---|
| lessons/da.py, da_weeks_1_2.py to da_weeks_7_8.py | The 24 Python for Data Analysis sessions. |
| lessons/ml.py | The 24 Machine Learning sessions, four labs and the extension. |
| lessons/hooks.py | The 53 "Where this is used" hooks (24 DA, 24 ML, four labs, ML25). Merged into each lesson as the `hook` field. |
| common.py | The lesson schema, the session clock, folder paths, the badge names and shared constants. |
| content.py | Loads the lessons. |
| build_camp.py | Writes sheets, notebooks, guides, curricula, plans, glossaries and labs. |
| verify_camp.py | Runs every code block and check, and enforces structure and house style. |
| package_camp.py | Builds the two student ZIPs and checks they hold no instructor files. Strips the instructor-only parts of HYBRID_DELIVERY.md from the student copy. |
| build_progress_map.py | Draws My_Progress_Map.pdf for each track (called by build_pdfs.py student). |
| build_pdfs.py | Renders the guides and the student sheets to PDF, with the Where this is used box. |
| build_parent_outlines.py | Draws the two-page parent outlines. |
| build_marketing.py | Draws the two flyers and the one-pager (PDF and DOCX). Needs reportlab and python-docx. |

Run from the repository root:

```
python Schools_ML_Track/camp_2026/build/build_camp.py
python Schools_ML_Track/camp_2026/build/verify_camp.py
python Schools_ML_Track/camp_2026/build/package_camp.py
```

A session has a question, a hook (2 to 3 short sentences, at most 60 words, no digits, ending in a question or invitation, checked by the verifier), at most six words, up to two blocks, a Make task, two error cards and an exit ticket. A python block must carry a `check` expression that the verifier evaluates, so a number on a sheet cannot drift from the data. A word is defined once per track.
