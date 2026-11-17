# NOTE (4 November 2026): Its output was written for the 15-week plan (Test 2, Demo Day, Weeks 13 to 15, old weights); the live files were patched IN PLACE on 2 to 4 November 2026 (see patch_*_2026110*.py). Running this generator overwrites those patches. Do not run it for the current semester without re-applying them.
"""Build the current Colab-first student guide."""
from build_week2_docs import student
if __name__ == '__main__': student()
