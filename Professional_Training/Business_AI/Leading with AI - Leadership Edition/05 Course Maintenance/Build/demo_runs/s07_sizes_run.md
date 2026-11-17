# Session 7 recorded run: file sizes of one small open model at 32, 16, 8 and 4 bits

- Date: 6 November 2026 (first run). Machine: lecturer's Mac, CPU only. Tools: Python venv of the course, torch 2.15.0, transformers 5.22.1, safetensors 0.8.0.
- Model: HuggingFaceTB/SmolLM2-135M-Instruct (Apache 2.0 per its Hugging Face card). Its published model.safetensors is 269,060,552 bytes (16-bit).
- Script: `demo_runs/s07/measure_sizes.py` (re-run it live; first run downloads about 270 MB). Output: `demo_runs/s07/sizes_result.json`. One run; the numbers are deterministic file sizes. The converted files were deleted after measuring (2 GB), re-created by the script.
- What the script does: loads the model, counts 134,515,008 stored numbers (the shared embedding table is stored once), and writes four safetensors files with plain round-to-nearest quantisation written for teaching: fp32 (4 bytes each), fp16 (2 bytes), int8 (one signed byte each plus one 16-bit scale per matrix row), int4 (two numbers per byte plus one 16-bit scale per 32 numbers). Norm vectors stay 16-bit in the int8 and int4 files.

## Measured file sizes (bytes on disk)
| Form | Bytes | MB (decimal) | Share of 32-bit |
|---|---|---|---|
| 32-bit | 538,090,376 | 538.1 | 100% |
| 16-bit | 269,060,248 | 269.1 | 50% |
| 8-bit | 135,012,040 | 135.0 | 25% |
| 4-bit | 75,768,008 | 75.8 | 14% |

Check by hand: 134,515,008 x 4 bytes = 538,060,032, and the file is 538,090,376 (the 30 KB extra is the file header and tensor names). 4-bit would be 67 MB with no scales; the scales and the 16-bit norm vectors add about 8 MB.

## Quality check, same script, same machine
Average next-word loss (lower is better) over three fixed sentences listed in the script, run with the converted numbers turned back into ordinary floats:
32-bit 4.5715; 16-bit 4.5715; 8-bit 4.5588; 4-bit 5.0855.
Top three next words after "The capital city of Uganda is":
- 32-bit and 16-bit: " U" 0.1129, " known" 0.1045, " the" 0.0751
- 8-bit: " U" 0.1145, " known" 0.1018, " a" 0.0707
- 4-bit: " the" 0.5609, " a" 0.0623, " U" 0.0345
Reading: 8-bit changed almost nothing; our crude 4-bit conversion changed the answer list of this very small model visibly. It is a teaching conversion; published 4-bit methods are smarter and keep important parts at higher precision. Three sentences is a tiny test and one run: say so on the slide.

## Published file listings read through the Hugging Face API (6 November 2026)
See sources_s07.md. GGUF (bartowski/SmolLM2-135M-Instruct-GGUF): f16 270,885,952; Q8_0 144,811,360; Q4_K_M 105,454,432 bytes. ONNX (HuggingFaceTB/SmolLM2-135M-Instruct, onnx/ folder): model.onnx 540,345,794 (32-bit); model_fp16 270,267,067; model_int8 137,147,867; model_q4 182,068,553; model_q4f16 117,691,126. Safetensors: model.safetensors 269,060,552 (16-bit).
Reading: the same model in three containers has the same size at the same precision (about 270 MB at 16-bit in safetensors, GGUF and ONNX). The size follows the precision, not the container. A 4-bit GGUF (Q4_K_M, 105 MB) is not one eighth of the 32-bit size: some parts stay at higher precision, and for a small model that matters more.

## Local run
Ollama and llama.cpp are NOT installed on this machine, and nothing was installed. A live local run is OPTIONAL: if the lecturer has Ollama, `ollama run` of a small model shows the same trade. Nothing on the slides depends on it.
