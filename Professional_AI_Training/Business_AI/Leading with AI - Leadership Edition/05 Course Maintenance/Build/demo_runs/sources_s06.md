# Sources verified for Session 6 (6 November 2026)
- Qwen2.5-1.5B-Instruct model card, https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct : Apache-2.0; 1.54B parameters; context "Full 32,768 tokens and generation 8192 tokens"; over 29 languages; "Training Stage: Pretraining & Post-training"; sections: Introduction, Requirements, Quickstart, Evaluation & Performance, Citation. No dedicated limitations section.
- GPT-2 model card, https://huggingface.co/openai-community/gpt2 : see sources_s05.md. Has "Limitations and bias" content.
- MMLU, https://arxiv.org/abs/2009.03300 : Hendrycks et al., Sept 2020; 57 tasks (elementary mathematics, US history, computer science, law and more).
- GSM8K, https://arxiv.org/abs/2110.14168 : Cobbe et al., Oct 2021; about 8.5K grade school math word problems.
- HumanEval, https://arxiv.org/abs/2107.03374 : Chen et al., July 2021; evaluation set to measure functional correctness of programs synthesised from docstrings.
- Chatbot Arena, https://arxiv.org/abs/2403.04132 : Chiang et al., March 2024; open platform ranking LLMs from human pairwise preference votes; over 240,000 votes at the time of the paper.
- InstructGPT, https://arxiv.org/abs/2203.02155 : Ouyang et al., March 2022; supervised fine-tuning on labeller demonstrations, then reinforcement learning from human feedback; 1.3B InstructGPT outputs preferred to 175B GPT-3.
- Mixtral of Experts, https://arxiv.org/abs/2401.04088 : Jan 2024; 8 feedforward blocks per layer, router picks 2 per token per layer; about 47B parameters, about 13B active per token; Apache 2.0.
- DeepSeek-R1, https://arxiv.org/abs/2501.12948 : Jan 2025 (Nature 2025); reasoning encouraged through reinforcement learning without human-labelled reasoning traces.
- DDPM, https://arxiv.org/abs/2006.11239 : Ho, Jain, Abbeel, June 2020; diffusion models for high quality image synthesis.
Not stated on any slide: sizes, training data or internals of closed commercial models.
- Re-verified 6 Nov 2026: Qwen2.5-1.5B-Instruct card: Apache-2.0; 1.54B parameters (1.31B non-embedding); context 32,768, generation 8,192; over 29 languages. GPT-2 card: MIT, 124M. Slide claims match.
