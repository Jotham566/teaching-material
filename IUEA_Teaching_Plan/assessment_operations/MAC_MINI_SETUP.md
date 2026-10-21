# Moving grading to another Mac

The public teaching repository contains code and teaching materials. Student submissions, marks, hidden checks and local calibration evidence are separate private data. Do not force-add the ignored private folders to the public repository.

## Folder layout and where to start

These commands use Git's default teaching-folder name, `teaching-material`, matching your Mac mini. Both repositories are siblings:

```text
~/Projects/
├── teaching-material/
└── IUEA-Grading-Private/
```

If you previously chose `IUEA-Teaching-Resources` as the teaching folder name, substitute that name in the commands. Do not clone a second copy or rename a working checkout just to match this guide.

**Your confirmed progress on 21 October:** both repositories are cloned, all 5,395 private files are restored, and the Python environment and requirements are installed. **Skip the cloning, restoration and Python-install steps below. Continue at “Build Docker images”.** The prepared-text-path notice is expected and does not mean marks were lost.

For a fresh machine only, sign into GitHub with access to the private repository and run:

```sh
mkdir -p ~/Projects
cd ~/Projects
git clone https://github.com/Jotham566/teaching-material.git
git clone https://github.com/Jotham566/IUEA-Grading-Private.git
python3 ~/Projects/IUEA-Grading-Private/sync_snapshot.py restore ~/Projects/teaching-material
```

Use existing checkouts instead of cloning twice. The private repository README explains how to capture results and restore subsequent updates. Restore verifies file hashes and refuses to overwrite differing local results unless explicitly requested. Complete the runtime setup below before executing grading.

The restore command uses full home-directory paths, so it works from either repository. A bare `teaching-material` argument is relative to your current directory and fails when you are inside `IUEA-Grading-Private`.

## Python environment — already completed on your Mac mini

For a fresh setup, install Python 3.12, then run:

   ```sh
   cd ~/Projects/teaching-material
   python3.12 -m venv .iuea-grader-env
   .iuea-grader-env/bin/python -m pip install -r requirements.txt
   ```

## Build Docker images — continue here

Install Docker Desktop for Apple silicon if needed. Open it and finish its first-run setup:

```sh
open -a Docker
```

Wait until Docker is running, then run the following. `docker info` must succeed before building the images:

   ```sh
   cd ~/Projects/teaching-material
   docker info
   docker build -t iuea-notebooks:2026.09 IUEA_Teaching_Plan/grader
   docker build -t iuea-document-renderer:2026.09 IUEA_Teaching_Plan/grader/document_renderer
   ```

Docker is for isolated notebook grading and document extraction. Set up native Ollama below for written grading; no Ollama Docker container is needed. Practical-test code grading does not require Ollama.

## Excel-generation runtime

Install/open Codex on the new Mac and initialize its bundled workspace dependencies. Excel generation uses its `@oai/artifact-tool` package; ordinary Node alone is insufficient. The default dependency location is under `~/.cache/codex-runtimes/codex-primary-runtime/dependencies/node`. If the supported runtime is elsewhere, set `IUEA_NODE` to its Node executable and `IUEA_ARTIFACT_NODE_MODULES` to its `node_modules` directory. Never commit those dependencies. The restored Excel file can be opened before this runtime is configured.

## Native Ollama: written grading

Ollama runs directly on macOS. Docker runs student notebook code in isolation and extracts document text. The Python grader connects to native Ollama at `http://127.0.0.1:11434`.

1. With Homebrew installed, install the native command-line version:

   ```sh
   brew install ollama
   ```

2. Open a separate Terminal window and start the local server:

   ```sh
   OLLAMA_NO_CLOUD=1 OLLAMA_HOST=127.0.0.1:11434 \
     OLLAMA_MAX_LOADED_MODELS=1 OLLAMA_NUM_PARALLEL=1 ollama serve
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

## Separate Docker work from local AI work

Finish notebook grading and document extraction first, with Docker running. **Stop Docker Desktop before loading a model for written grading or calibration.** This also stops other containers, so finish any unrelated container work first.

```sh
cd ~/Projects/teaching-material
.iuea-grader-env/bin/python IUEA_Teaching_Plan/grader/local_ai_resources.py
```

On macOS this command checks the local Docker Desktop processes, requests a graceful shutdown if needed, and verifies that they have exited. If it cannot verify shutdown, it fails and tells you to quit Docker Desktop manually. It does not stop a remote Docker daemon.

The A1/A2 written grader and the two calibration commands below also run this check before each uncached submission/case. A failed resource check stops the batch instead of assigning a student zero. Keep Docker closed throughout inference; do not reopen it while a model request is running. These checks do not prevent you or another application from restarting Docker between checks.

Before returning to Docker work, unload any models shown by `ollama ps`. For the models used here:

```sh
ollama stop qwen3.5:9b
ollama stop qwen3.5:4b
ollama stop qwen3:4b
open -a Docker
```

Wait for Docker to finish starting before extracting documents or grading notebook code. The native Ollama server can remain idle; model weights need not remain loaded.

## Trial a larger model on the 16GB Mac mini

Trial `qwen3.5:9b` before considering it for production marks. It is a candidate, not an already-validated replacement. Keep the 4B models and existing calibration reports. Downloading the candidate does not change the active grading configuration.

With the native Ollama server running, download the model and create a new private trial folder:

```sh
ollama pull qwen3.5:9b
cd ~/Projects/teaching-material
.iuea-grader-env/bin/python IUEA_Teaching_Plan/grader/local_ai_resources.py
trial_dir="IUEA_Teaching_Plan/assessment_operations/private/model_trials/qwen35_9b_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$trial_dir"
```

In that same Terminal window, run the A1 calibration:

```sh
.iuea-grader-env/bin/python IUEA_Teaching_Plan/grader/calibrate_rubric.py \
  --rubric IUEA_Teaching_Plan/grader/rubrics/W01.json \
  --cases IUEA_Teaching_Plan/grader/calibration_cases/W01.json \
  --model qwen3.5:9b \
  --out "$trial_dir/W01.json"
```

Then run the A2 calibration:

```sh
.iuea-grader-env/bin/python IUEA_Teaching_Plan/grader/calibrate_local_grader.py \
  --model qwen3.5:9b \
  --out "$trial_dir/W02.json"
ollama ps
```

All cases for each assessment must pass. These commands use authored examples and save separate evidence; they do not regrade student submissions, replace existing marks or select the new model for production. If a run fails or is interrupted, retain its evidence and use a new trial folder for another full run. Compare accuracy, disagreements, elapsed times and Activity Monitor memory pressure before adopting the candidate. Passing this small calibration is necessary but does not by itself establish better grading on real submissions. Any subsequent trial on unresolved work must also use separate results and preserve the current workbook until reviewed.

References: [native Homebrew install](https://formulae.brew.sh/formula/ollama) and [Ollama server configuration and processor checks](https://docs.ollama.com/faq).

## Before grading

- The 21 October automatic batch is already complete. Do not rerun `finish_ca_refresh.py`: it is a one-time snapshot refresh with a backup guard.
- Prepared written-text metadata contains absolute paths from the original Mac. Regenerate it with `prepare_ca_written.py` against the restored source snapshot before a new written batch; do not alter student files or checksums to bypass validation.
- Use the immutable raw-identity grading input for the selected snapshot, not the reconciled cumulative ledger. For the latest snapshot this is `private/grading_input_20261021.json`.
- Import new submissions through the refresh steps in `README.md`. Keep existing results; do not replace the full results set with only a new batch.
- Resolve identity/file/written-review cases separately. More RAM does not resolve ambiguous identity evidence or grader disagreements.

To regenerate text paths for the restored 21 October snapshot, with Docker running:

```sh
cd ~/Projects/teaching-material
.iuea-grader-env/bin/python IUEA_Teaching_Plan/grader/prepare_ca_written.py \
  --source IUEA_Teaching_Plan/assessment_operations/private/reconciled \
  --ledger IUEA_Teaching_Plan/assessment_operations/private/grading_input_20261021.json \
  --out IUEA_Teaching_Plan/assessment_operations/private/written_text_macmini
```

This creates a separate prepared-text directory; it does not award marks or replace the workbook. Use its `prepared.json` for a subsequent written batch against this same snapshot. Extraction problems stay flagged. New submissions require a fresh source snapshot and matching grading input, following `README.md`; do not reuse the dated input for them.

## Updating safely

Stop grading before pulling changes to grader code or checks. Pull the teaching repository, then synchronize the private snapshot. Run only one grading writer at a time: do not grade into the same shared results on both Macs. Commit/synchronize private results after the batch finishes, then pull them on the other machine. Excel is a generated output; manual edits are not automatically imported into the grading ledger.

Run the relevant checks after setup:

```sh
cd ~/Projects/teaching-material
.iuea-grader-env/bin/python -m unittest tests.test_continuous_assessment tests.test_ca_written tests.test_ca_export tests.test_ca_reconciliation tests.test_ca_format_recovery tests.test_ca_review_links tests.test_local_ai_resources
```

No student marks are published by these local commands.
