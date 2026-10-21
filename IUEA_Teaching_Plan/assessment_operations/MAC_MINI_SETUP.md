# Moving grading to another Mac

The public teaching repository contains code and teaching materials. Student submissions, marks, hidden checks and local calibration evidence are separate private data. Do not force-add the ignored private folders to the public repository.

The authorized private snapshot is in `Jotham566/IUEA-Grading-Private`. On the new Mac, sign into GitHub with access to it and run:

```sh
mkdir -p ~/Projects
cd ~/Projects
git clone https://github.com/Jotham566/teaching-material.git IUEA-Teaching-Resources
git clone https://github.com/Jotham566/IUEA-Grading-Private.git
python3 IUEA-Grading-Private/sync_snapshot.py restore IUEA-Teaching-Resources
```

Use existing checkouts instead of cloning twice. The private repository README explains how to capture results and restore subsequent updates. Restore verifies file hashes and refuses to overwrite differing local results unless explicitly requested. Complete the runtime setup below before executing grading.

## Install once

1. Clone the teaching repository and check out `main`.
2. Install Python 3.12 and Docker Desktop for Apple silicon. Install Ollama natively using the instructions below; no Ollama Docker container is needed. Start Docker Desktop for notebook grading and document extraction.
3. From the repository root, run:

   ```sh
   python3.12 -m venv .iuea-grader-env
   .iuea-grader-env/bin/python -m pip install -r requirements.txt
   docker build -t iuea-notebooks:2026.09 IUEA_Teaching_Plan/grader
   docker build -t iuea-document-renderer:2026.09 IUEA_Teaching_Plan/grader/document_renderer
   ```

4. Restore the private grading snapshot in the same relative directories. It must include the submissions and manifests, completed results, workbook, hidden assessment checks and required calibration reports with their `.complete.json` companions. Preserve source bytes and hashes. Do not copy Python virtual environments, Docker state, browser profiles or credentials.
5. Install/open Codex on the new Mac and initialize its bundled workspace dependencies. Excel generation uses its `@oai/artifact-tool` package; ordinary Node alone is insufficient. The default dependency location is under `~/.cache/codex-runtimes/codex-primary-runtime/dependencies/node`. If the supported runtime is elsewhere, set `IUEA_NODE` to its Node executable and `IUEA_ARTIFACT_NODE_MODULES` to its `node_modules` directory. Never commit those dependencies.
6. Set up native Ollama as follows before running written grading. Practical-test code grading does not require Ollama.

## Native Ollama: written grading

Ollama runs directly on macOS. Docker runs student notebook code in isolation and extracts document text. The Python grader connects to native Ollama at `http://127.0.0.1:11434`.

1. With Homebrew installed, install the native command-line version:

   ```sh
   brew install ollama
   ```

2. Open a separate Terminal window and start the local server:

   ```sh
   OLLAMA_NO_CLOUD=1 OLLAMA_HOST=127.0.0.1:11434 ollama serve
   ```

   Leave this window open during written grading. These settings keep the server on this Mac and disable Ollama cloud features. Do not also start an Ollama Docker container or a second server.

   If the port is already in use, an Ollama app or service may already be running. Quit the Ollama menu-bar app, or run `brew services stop ollama` if you previously started the Homebrew service, then retry the command above. Setting environment variables in a different Terminal does not change an already-running server.

3. In your original Terminal window, download the two local models:

   ```sh
   ollama pull qwen3.5:4b
   ollama pull qwen3:4b
   ollama list
   curl --fail --silent --show-error http://127.0.0.1:11434/api/tags
   ```

   The list should contain both model names and the last command should return JSON. Internet is needed for the model downloads; grading uses the local server.

4. Before awarding written marks, let the grader validate the installed models against the saved calibration reports. A1 uses `qwen3.5:4b`; A2 uses `qwen3:4b`. Matching names alone do not establish matching model digests. If validation fails, stop and obtain a new passing calibration or restore the validated model; do not bypass the check. Avoid model/server upgrades during a batch.

5. During grading, `ollama ps` shows loaded models and processor usage. An empty list when idle is normal. After grading finishes, press **Control-C** in the server Terminal to stop a manually started server. This does not remove the models or saved marks.

Keep Docker available for code grading and document extraction. It can be stopped during the written-only phase to free memory; Ollama continues running natively.

References: [native Homebrew install](https://formulae.brew.sh/formula/ollama) and [Ollama server configuration and processor checks](https://docs.ollama.com/faq).

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
