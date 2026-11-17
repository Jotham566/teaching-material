# Sources checked for Session 4 (6 November 2026)

- Model card, sentence-transformers/all-MiniLM-L6-v2, https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2 (read 6 Nov 2026): maps sentences and paragraphs to a 384 dimensional dense vector space; intended for clustering and semantic search; fine-tuned on a dataset of more than one billion sentence pairs; input over 256 word pieces is truncated by default. Used for "384 numbers", "trained on more than a billion sentences" (notes only) and the purpose.
- The module list of the model was read from the installed package (Transformer, Pooling, Normalize), so "its last step makes every vector length 1" is from this run (`model_modules` and the measured lengths in `results.json`).
- The model's language coverage was not verified: no slide or note claims it works for Luganda or any other language; the facilitator probe says to check the model card and test.
- Definitions of Euclidean distance, Manhattan distance, dot product and cosine similarity are standard mathematics and are demonstrated by hand with toy vectors; no external statistic is quoted.
- The 2D map uses scikit-learn PCA; the "keeps 18 percent" figure is the measured explained variance of this run.
- Nothing is claimed about the internals, data or size of any closed model.
