# Student study calendars

One A4 PDF and an editable Word file per learner. Generate a new one from `build/make_calendar.py` (see its header for the options), for example:

```
cd Schools_ML_Track/camp_2026/build
python3 make_calendar.py --track DA --start 2027-01-05 --days tue,thu,sat --physical sat \
    --holidays "2027-01-26:NRM Liberation Day" --showcase 2027-03-06 --name "Learner Name"
```

Titles, week themes and badges come from the lessons, so the calendar follows any later change to the course. Check the public holidays for the dates you use.
