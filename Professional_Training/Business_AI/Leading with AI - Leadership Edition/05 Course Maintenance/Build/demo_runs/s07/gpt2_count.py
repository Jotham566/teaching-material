"""Session 5 and 7: count the numbers inside GPT-2 small and show a few real ones. Run: python gpt2_count.py. Writes gpt2_count.json next to this file.
Model: openai-community/gpt2 (GPT-2 small, MIT). Needs the model in the Hugging Face cache (see demo_runs/s05/download.py)."""
import json
from pathlib import Path
from transformers import GPT2LMHeadModel, AutoTokenizer

m = GPT2LMHeadModel.from_pretrained('gpt2')
c = m.config
tot = sum(p.numel() for p in m.parameters())
blk = sum(p.numel() for p in m.transformer.h[0].parameters())
blk_attn = sum(p.numel() for p in m.transformer.h[0].attn.parameters())
blk_mlp = sum(p.numel() for p in m.transformer.h[0].mlp.parameters())
blk_ln = sum(p.numel() for p in list(m.transformer.h[0].ln_1.parameters()) + list(m.transformer.h[0].ln_2.parameters()))
wte = m.transformer.wte.weight.numel()
wpe = m.transformer.wpe.weight.numel()
w = m.transformer.h[0].mlp.c_fc.weight  # shape (768, 3072): 768 numbers in, 3072 small neurons
b = m.transformer.h[0].mlp.c_fc.bias
tok = AutoTokenizer.from_pretrained('gpt2')
ids = tok('Please pay the invoice within thirty')['input_ids']
emb = m.transformer.wte.weight
out = dict(sentence_pieces=[tok.decode([i]) for i in ids], sentence_ids=ids,
           first_piece_numbers=[round(float(v), 3) for v in emb[ids[0]][:4]], invoice_piece_numbers=[round(float(v), 3) for v in emb[ids[3]][:4]],
           total=tot, blocks=c.n_layer, heads=c.n_head, numbers_per_token=c.n_embd, vocab=c.vocab_size, context=c.n_positions,
           per_block=blk, block_attention=blk_attn, block_neuron_layers=blk_mlp, block_other=blk_ln,
           all_blocks=blk * c.n_layer, piece_table=wte, position_table=wpe, final_norm=sum(p.numel() for p in m.transformer.ln_f.parameters()),
           block0_neuron_layer_shape=list(w.shape), block0_neuron_layer_first_5x6=[[round(float(v), 3) for v in row[:6]] for row in w[:5]],
           block0_neuron_layer_first_bias=[round(float(v), 3) for v in b[:6]])
Path(__file__).with_name('gpt2_count.json').write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
