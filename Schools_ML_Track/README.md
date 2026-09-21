# Machine Learning Track for S.5 and S.6

A December holiday programme: **eight weeks, twenty-four sessions of three
hours, seventy-two hours**, for Senior 5 and Senior 6 students whose
computing background is Subsidiary ICT. Nobody has programmed. They bring
their own laptops.

## What is here

| File | What it is |
|---|---|
| `ML_Track_S5_S6_Syllabus.docx` | The syllabus, for students and parents. 13 pages: the roadmap, all eight weeks session by session, how a session runs, marks and the certificate, what to bring, the questions parents ask, and what the track does not do. |
| `ML_Track_S5_S6_Syllabus.pdf` | The same document, for sending. Most parents will open this on a phone. |
| `figs/roadmap_schools.png` | The fifteen-stage roadmap. |
| `figs/timeline_schools.png` | The eight weeks, and what exists on the laptop at the end of each. |
| `figs/marks_schools.png` | Where the hundred marks come from. |

## The design, in four decisions

**Excel and A-level maths are the starting point, and the maths is the
encouraging part.** Stage 2 of the roadmap is marked as something students
already have, because the mean, the median, spread, correlation, the line of
best fit, probability and gradients are all on the A-level syllabus. A
student doing Subsidiary or Principal Mathematics is holding half of what
machine learning is built on and has never been told so. Week 5 turns
`y = mx + c` into a working model.

**Every session ends with something that runs.** The last forty-five minutes
of each session exists so there is a file on the laptop that does something
before the student goes home, and the twenty minutes after that is show and
tell on the projector. Fifty minutes of teaching against eighty at the
keyboard, and no teaching block longer than twenty-five minutes.

**Marks come from work.** Attendance is expected and is not a grade. Seven
weekly practicals, two marked checkpoints, a final project and a five-minute
presentation. A student below 50 gets a certificate of attendance that does
not claim a skill they do not have.

**The limits are in the document.** Section 7 says plainly that seventy-two
hours makes a confident beginner rather than a professional, that this is not
A-level revision, that deep learning is a first look only, and that nobody is
promised a job or a scholarship.

## Rebuild

```bash
python3 ../scripts/make_schools_figures.py        # the three figures
python3 ../scripts/build_schools_syllabus_docx.py # the syllabus
python3 ../scripts/verify_schools_track.py        # 28 checks; must be green
soffice --headless --convert-to pdf ML_Track_S5_S6_Syllabus.docx
python3 ../scripts/verify_schools_track.py        # again, for the page checks
```

`scripts/schools_content.py` is the single source of truth: the weeks, the
session block, the roadmap cards, the marks, the kit, the policies and the
limits. Change a week there and the figure, the document and the verifier all
follow. Weeks claim roadmap card NUMBERS, and the module refuses to import if
a week claims a card that does not exist or if a teaching card is taught in
no week.

## Two things the verifier exists to catch

**A figure drawn for a slide is illegible on paper.** The roadmap started as
a port of the projected version, 13 inches wide. Placed in a document at 7
inches, every size in it halved and the annotation landed under 4pt. Figures
are now drawn close to the width they are placed at,
`schools_content.FIG_PLACEMENT` holds those widths, and the generator refuses
to save a figure whose smallest type would land under 8pt or whose height
would push it off its own page.

**Only the rendered pages show a layout fault.** Section 6 of the verifier
reads the PDF: it caught the roadmap orphaned away from its heading, and a
page carrying three lines and a repeated table header. Every other check
passed on both. Render it and look, every time.

## Still to fill in

The teaching content is settled. Section 8 of the syllabus lists eight
practical details for the school to confirm: dates, days, times, venue, fee,
instructor, contact and group size. They are blank rather than guessed,
because a syllabus that goes home with a wrong date is worse than one with a
gap.
