# Test revision materials to share in advance

Latest Test 1 revision: 19 October 2026. Use the current 68-slide Week 7 decks. They now include returned records, summary dictionaries, Figure objects, ten-bin histograms, findings with units, and interpretation limits. Replace earlier copies when sharing. The matching practice CSV filenames and values are unchanged.

Send the matching **PDF slides and practice CSV together**, a few days before each test. For WhatsApp, attach the PDF and CSV as two documents so students do not need to unzip anything. The optional ZIP bundles those same files with START_HERE.txt. It contains no test notebook, grader or assessment answer key.

Students create a blank Colab notebook, upload the CSV and follow the deck in order. Worked examples include expected outputs and practice answers. No practice submission is required. The later test-day section explains the separate timed test files and submission.

| Programme | Test week | Slides | Practice CSV | Optional bundle |
|---|---|---|---|---|
| CML3111 | Week 7 / Test 1 | [PDF](CML3111/Test1/CML3111_Week07_Engineering.pdf) | [CSV](CML3111/Test1/CML3111_Test1_practice.csv) | [ZIP](CML3111/Test1/CML3111_Test1_revision.zip) |
| CML3111 | Week 14 / Test 2 | [PDF](CML3111/Test2/CML3111_Week14_Engineering.pdf) | [CSV](CML3111/Test2/CML3111_Test2_practice.csv) | [ZIP](CML3111/Test2/CML3111_Test2_revision.zip) |
| CML3112 | Week 7 / Test 1 | [PDF](CML3112/Test1/CML3112_Week07_Design_Infrastructure.pdf) | [CSV](CML3112/Test1/CML3112_Test1_practice.csv) | [ZIP](CML3112/Test1/CML3112_Test1_revision.zip) |
| CML3112 | Week 14 / Test 2 | [PDF](CML3112/Test2/CML3112_Week14_Design_Infrastructure.pdf) | [CSV](CML3112/Test2/CML3112_Test2_practice.csv) | [ZIP](CML3112/Test2/CML3112_Test2_revision.zip) |
| CML3113 | Week 7 / Test 1 | [PDF](CML3113/Test1/CML3113_Week07_Mining_Petroleum.pdf) | [CSV](CML3113/Test1/CML3113_Test1_practice.csv) | [ZIP](CML3113/Test1/CML3113_Test1_revision.zip) |
| CML3113 | Week 14 / Test 2 | [PDF](CML3113/Test2/CML3113_Week14_Mining_Petroleum.pdf) | [CSV](CML3113/Test2/CML3113_Test2_practice.csv) | [ZIP](CML3113/Test2/CML3113_Test2_revision.zip) |

Suggested message:

> Please download both the revision slides and the practice CSV. Open a new Colab notebook, upload the CSV using the folder icon, and follow the examples in slide order. Try each practice question before checking its answer. Keep your work for revision; you do not need to submit it. On test day, you will receive different files through the test entry link.

Revision ZIPs contain PDF slides, the matching practice CSV and START_HERE.txt. Editable PowerPoint masters remain in the lecturer decks directory. To rebuild: run `node scripts/export_test_revision_pdfs.mjs`, then `python3 scripts/build_test_revision_resources.py --package`.
