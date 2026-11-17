# Build Tools

The shared engine that builds and checks the teaching material for all three programmes. Run every command from the repository root.

| Folder | What is in it |
|---|---|
| `scripts/` | Generators for decks, notebooks, Word documents, student packages and QR codes, plus the verifiers (`verify_*.py`, `validation/`). |
| `tests/` | Automated tests for the grader, test portal, gateway and builds (`python3 Build_Tools/tests/...`, `node Build_Tools/tests/...`). |
| `data/` | Notes, links and assessment settings the builders and the grader read (for example `assessments.json`, `test_portal_config.json`). |
| `figs/` | Figures used in the decks and guides. |
| `qr/` | QR code images for quizzes and assignments. |
| `requirements.txt` | Pinned Python packages: `python -m pip install -r Build_Tools/requirements.txt`. |

The IUEA course and the data analysis course share `scripts/pptxkit.py` and `scripts/docxkit.py`, so run both courses' validators after changing either.
