# Week 2 repair notebook walkthrough

Lecturer only. Use the issued notebooks; keep these worked answers out of the student ZIP. Open proof_of_life.ipynb first. During the notebook practical, demonstrate 01, let students attempt 02–03 with support, guide 04, then return to the main notebook. Allow about 5 minutes per exercise, adapting to the class.

For every exercise: ask students to predict, run the original, read the result/error, identify the cause, make one repair and rerun. Ask for a one-sentence explanation. The repairs are practice; only the main notebook and the student's own README are uploaded for marking.

## 01 Missing module

Original:
```python
import course_package_not_installed
```
It raises ModuleNotFoundError because this is a deliberately unavailable module. An import asks Python to find and load a module; it does not install it.

Ask: “What is the last line of the error telling us? Do we actually need this module?” Remove that import. To demonstrate a valid import, replace it with:
```python
import csv
print(csv.__name__)
```
Expected: `csv`. It is part of Python's standard library, so no pip installation is required. Do not ask students to install the fictional module. In a real project, first verify the intended package and whether it belongs in the current environment.

## 02 Python version mismatch

Original:
```python
import sys
assert sys.version_info.major == 2, "Notebook expects Python 2, but the course uses Python 3"
```
On the course's Python 3 runtime it raises AssertionError. This notebook deliberately contains a wrong version expectation; this error does not mean Colab is broken.

Ask: “Which version are we running, and which version does this line demand?” Repair it:
```python
import sys
print(sys.version_info.major)
assert sys.version_info.major == 3, "Use Python 3"
```
Expected: `3`, with no assertion error. Keep the Python 3 runtime. An assertion checks a condition; it does not switch or install a Python version.

## 03 Wrong file path

For CML3112 the original opens `missing_folder/site_inspection_log.csv`. It raises FileNotFoundError because the requested location does not exist. A file on the laptop is not automatically inside Colab.

Ask: “Where does this path tell Python to look? Where did we upload the file?” Upload the CSV through Colab's Files sidebar. Use the exact name:

| Cohort | CSV | First line |
|---|---|---|
| CML3112 | site_inspection_log.csv | reading_id,crack_width_mm |
| CML3113 | drill_shift_log.csv | reading_id,depth_m |
| CML3111 | motor_test_bench.csv | reading_id,current_a |

CML3112 correction:
```python
with open("site_inspection_log.csv") as f:
    print(f.readline().strip())
```
Expected: `reading_id,crack_width_mm`. Substitute the corresponding filename for other cohorts. Explain that `with` closes the file afterwards. If the corrected path still fails, check the Files sidebar, exact spelling and current location. Re-upload the CSV if a runtime reset removed it.

## 04 Variable state and execution order

Original:
```python
readings = 12
readings = readings + 5
readings = 12
print(readings)
```
It prints `12` without an exception. Trace the stored value line by line: 12, then 17, then 12. The third line overwrites the result. A program can run successfully and still produce the wrong answer.

Ask: “Which line discards the addition?” Remove the second initialization:
```python
readings = 12
readings = readings + 5
print(readings)
```
Expected: `17`. Rerunning this WHOLE cell still prints 17, because its first line resets the value every time.

Now return to proof_of_life.ipynb: initialization and increment are in SEPARATE cells. Run the initialization once, then the increment cell three times: 17, 22, 27. Restarting clears the stored state; Run All runs initialization and increment once, giving 17. Ask students to explain this distinction in their own words in the main notebook.

## Optional script and final check

hello_engineering.py is a standalone-script example, not another assessment. If useful, upload it to Colab and run `!python hello_engineering.py` in a code cell. It prints a greeting and the dataset name; it does not read or verify the CSV. Otherwise omit this demonstration.

Students finish the main notebook, restart/run all, save it using their own Student Registration Number with slashes replaced by underscores in the filename, write their own README and upload those two files together. Retain repaired practice copies; do not upload them as additional graded notebooks.
