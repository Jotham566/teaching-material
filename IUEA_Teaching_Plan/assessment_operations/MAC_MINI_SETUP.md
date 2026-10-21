# Moving grading to another Mac

The public teaching repository contains code and teaching materials. Student submissions, marks, hidden checks and local calibration evidence are separate private data. Do not force-add the ignored private folders to the public repository.

## Install once

1. Clone the teaching repository and check out `main`.
2. Install Python 3.12, Docker Desktop for Apple silicon, and Ollama. Start Docker Desktop.
3. From the repository root, run:

   ```sh
   python3.12 -m venv .iuea-grader-env
   .iuea-grader-env/bin/python -m pip install -r requirements.txt
   docker build -t iuea-notebooks:2026.09 IUEA_Teaching_Plan/grader
   docker build -t iuea-document-renderer:2026.09 IUEA_Teaching_Plan/grader/document_renderer
   ```

4. Restore the private grading snapshot in the same relative directories. It must include the submissions and manifests, completed results, workbook, hidden assessment checks and required calibration reports with their `.complete.json` companions. Preserve source bytes and hashes. Do not copy Python virtual environments, Docker state, browser profiles or credentials.
5. Install/open Codex on the new Mac and initialize its bundled workspace dependencies. Excel generation uses its `@oai/artifact-tool` package; ordinary Node alone is insufficient. The default dependency location is under `~/.cache/codex-runtimes/codex-primary-runtime/dependencies/node`. If the supported runtime is elsewhere, set `IUEA_NODE` to its Node executable and `IUEA_ARTIFACT_NODE_MODULES` to its `node_modules` directory. Never commit those dependencies.
6. For written grading, install the exact model versions identified by the private calibration reports. The current reports use `qwen3.5:4b` for A1 and `qwen3:4b` for A2. Matching names alone are not proof of matching model digests: calibration validation must pass on the new machine. Set `OLLAMA_NO_CLOUD=1` when starting the local server. A changed model requires a new passing calibration before student grading.

## Before grading

- The 21 October automatic batch is already complete. Do not rerun `finish_ca_refresh.py`: it is a one-time snapshot refresh with a backup guard.
- Prepared written-text metadata contains absolute paths from the original Mac. Regenerate it with `prepare_ca_written.py` against the restored source snapshot before a new written batch; do not alter student files or checksums to bypass validation.
- Use the immutable raw-identity grading input for the selected snapshot, not the reconciled cumulative ledger. For the latest snapshot this is `private/grading_input_20261021.json`.
- Import new submissions through the refresh steps in `README.md`. Keep existing results; do not replace the full results set with only a new batch.
- Resolve identity/file/written-review cases separately. More RAM does not resolve ambiguous identity evidence or grader disagreements.

## Updating safely

Stop grading before pulling changes to grader code or checks. Pull the teaching repository, then synchronize the private snapshot. Run only one grading writer at a time: do not grade into the same shared results on both Macs. Commit/synchronize private results after the batch finishes, then pull them on the other machine. Excel is a generated output; manual edits are not automatically imported into the grading ledger.

Run the relevant checks after setup:

```sh
.iuea-grader-env/bin/python -m unittest tests.test_continuous_assessment tests.test_ca_written tests.test_ca_export tests.test_ca_reconciliation tests.test_ca_format_recovery tests.test_ca_review_links
```

No student marks are published by these local commands.
