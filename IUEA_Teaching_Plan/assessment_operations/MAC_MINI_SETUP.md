# Mac mini: finish setup

**Already done:** both repositories cloned, private files restored, Python environment and requirements installed. Do not repeat those steps.

Your folders are `~/Projects/teaching-material` and `~/Projects/IUEA-Grading-Private`. Copy each command block separately. Stop if a command reports an error.

## 1. Get the latest code

```sh
git -C ~/Projects/teaching-material pull --ff-only
git -C ~/Projects/IUEA-Grading-Private pull --ff-only
```

## 2. Build Docker images once

Open Docker Desktop and wait until it is running. Then:

```sh
cd ~/Projects/teaching-material
docker build -t iuea-notebooks:2026.09 IUEA_Teaching_Plan/grader
docker build -t iuea-document-renderer:2026.09 IUEA_Teaching_Plan/grader/document_renderer
```

Docker is for student code and reading documents. Ollama runs natively on the Mac.

## 3. Prepare native Ollama

If it is not installed, run `brew install ollama`.

In a separate Terminal window, start the server and leave it open:

```sh
OLLAMA_NO_CLOUD=1 OLLAMA_HOST=127.0.0.1:11434 \
  OLLAMA_MAX_LOADED_MODELS=1 OLLAMA_NUM_PARALLEL=1 ollama serve
```

In your original Terminal, download the current grading models:

```sh
ollama pull qwen3.5:4b
ollama pull qwen3:4b
```

If the port is already in use, see the [reference guide](MAC_MINI_REFERENCE.md#native-ollama-written-grading). The 9B model is an optional [separate calibration trial](MAC_MINI_REFERENCE.md#trial-a-larger-model-on-the-16gb-mac-mini), not a required step or an approved replacement yet.

## 4. Check the setup

```sh
cd ~/Projects/teaching-material
.iuea-grader-env/bin/python -m unittest tests.test_continuous_assessment tests.test_ca_written tests.test_ca_export tests.test_ca_reconciliation tests.test_ca_format_recovery tests.test_ca_review_links tests.test_local_ai_resources
```

The checks should end with **OK**. They do not prove the installed models pass grading calibration.

Open the teaching repository in Codex on the Mac mini and ask:

> Finish the Mac mini preflight: initialize the bundled workbook runtime, regenerate prepared-text paths for the restored snapshot in a separate folder, and validate both installed models against the saved A1/A2 calibration reports. Do not change student marks. Report any failed checks before grading.

This is needed because workbook generation uses Codex's bundled runtime, and prepared-text paths refer to the old Mac. Technical details are in the [reference guide](MAC_MINI_REFERENCE.md).

## 5. Continue grading

The imported 21 October batch is already complete. Do not restart the old refresh script.

For new submissions, follow **[New submissions: repeat checklist](CONTINUE_GRADING.md)**. For existing unresolved records, use the workbook's **Review needed** sheet.

**One Mac grades at a time. Finish Docker work before written grading. The written grader stops Docker before inference and refuses to proceed if shutdown cannot be verified; keep Docker closed during the run.**
