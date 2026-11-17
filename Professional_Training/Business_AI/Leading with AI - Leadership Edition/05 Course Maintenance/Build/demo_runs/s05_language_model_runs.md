# Session 5 recorded run: tokens, next-word probabilities, temperature, attention

Date: 6 November 2026. Run by the course author on a MacBook, CPU only, 8 GB memory. Script: `s05/run_s05.py` (seeded, so it can be re-run live; raw numbers in `s05/results.json`).
Model: GPT-2 small, 124M parameters, OpenAI 2019, MIT licence (huggingface.co/openai-community/gpt2). Tools: transformers 5.22.1, torch 2.15.0, tiktoken 0.14.0. Number of runs: one pass for tokens, probabilities and attention; 6 sampled completions at each of 3 temperatures (seeds 100 to 105).

## 1. Tokenisation (GPT-2 tokenizer in transformers; tiktoken 'gpt2' encoding gave identical ids, checked in the script)

- Input: `Nile Valley Foods delivers maize flour to Mbale.`  (8 words, 11 tokens)
  Pieces: 'N' | 'ile' | ' Valley' | ' Foods' | ' delivers' | ' maize' | ' flour' | ' to' | ' Mb' | 'ale' | '.'
- Input: `Invoice INV-2041 for UGX 1,250,000 is overdue.`  (7 words, 18 tokens)
  Pieces: 'Inv' | 'oice' | ' INV' | '-' | '20' | '41' | ' for' | ' U' | 'G' | 'X' | ' 1' | ',' | '250' | ',' | '000' | ' is' | ' overdue' | '.'
- Input: `Busoga Oils Ltd renewed the supply agreement automatically.`  (8 words, 11 tokens)
  Pieces: 'Bus' | 'oga' | ' O' | 'ils' | ' Ltd' | ' renewed' | ' the' | ' supply' | ' agreement' | ' automatically' | '.'
- Input: `Unbelievably, the warehouse was reorganised.`  (5 words, 11 tokens)
  Pieces: 'Un' | 'bel' | 'iev' | 'ably' | ',' | ' the' | ' warehouse' | ' was' | ' reorgan' | 'ised' | '.'
- Input: `Habari, tunataka sukari magunia kumi.`  (5 words, 14 tokens)
  Pieces: 'H' | 'ab' | 'ari' | ',' | ' tun' | 'ataka' | ' su' | 'k' | 'ari' | ' mag' | 'unia' | ' k' | 'umi' | '.'

## 2. Top 10 next tokens (probability, raw softmax at temperature 1)

Prompt: `The capital of Uganda is`  (top 10 together: 41.6 percent)

- ' the': 9.1 percent
- ' a': 6.4 percent
- ' located': 5.5 percent
- ' now': 4.7 percent
- ' home': 4.3 percent
- ' in': 3.0 percent
- ' Kamp': 2.3 percent
- ' known': 2.2 percent
- ' also': 2.2 percent
- ' under': 1.8 percent

Prompt: `Please pay the invoice within thirty`  (top 10 together: 98.7 percent)

- ' (': 69.3 percent
- ' days': 17.8 percent
- '-': 10.2 percent
- ' minutes': 0.4 percent
- ' business': 0.4 percent
- ' calendar': 0.2 percent
- ' working': 0.1 percent
- ' seconds': 0.1 percent
- ' day': 0.1 percent
- ' six': 0.1 percent

Prompt: `Nile Valley Foods is a food distributor based in`  (top 10 together: 17.3 percent)

- ' the': 5.4 percent
- ' San': 3.2 percent
- ' Los': 1.7 percent
- ' Salt': 1.3 percent
- ' California': 1.2 percent
- ' New': 1.2 percent
- ' South': 0.9 percent
- ' Chicago': 0.8 percent
- ' Seattle': 0.8 percent
- ' Austin': 0.8 percent

Prompt: `The customer was angry because the delivery was`  (top 10 together: 41.7 percent)

- ' delayed': 11.4 percent
- ' not': 8.7 percent
- ' late': 5.2 percent
- ' too': 3.8 percent
- ' so': 3.6 percent
- ' a': 3.0 percent
- ' delivered': 1.7 percent
- ' slow': 1.7 percent
- ' in': 1.4 percent
- ' very': 1.2 percent

## 3. Temperature, prompt: `The customer was angry because the delivery was`

### Temperature 0.2
Top 8 after rescaling: ' delayed' 77.9%, ' not' 20.0%, ' late' 1.5%, ' too' 0.3%, ' so' 0.3%, ' a' 0.1%, ' delivered' 0.0%, ' slow' 0.0%
Six sampled completions (14 new tokens each):
- ` delayed, and the customer was angry because the delivery was delayed. `
- ` delayed. He said he was told by the customer that he could not`
- ` delayed.  "We're not going to be able to deliver`
- ` delayed. He said he was told that the delivery was delayed because the`
- ` not delivered. The customer was angry because the delivery was not delivered.`
- ` delayed.  "I was angry because I was told to wait`

### Temperature 1.0
Top 8 after rescaling: ' delayed' 11.4%, ' not' 8.7%, ' late' 5.2%, ' too' 3.8%, ' so' 3.6%, ' a' 3.0%, ' delivered' 1.7%, ' slow' 1.7%
Six sampled completions (14 new tokens each):
- ` delayed 3-4 days and the delivery was delayed by several hours due`
- ` legally required to changing the delivery address and it had not happened. `
- ` denied because they didn't pay the rent. That didn't sit well`
- ` so expensive.A vice801 customer says the first thing you should file`
- ` so late, and the customer asked what the order was, and when`
- ` very extremely fast and arrived in a timely manner. The service was excellent`

### Temperature 1.8
Top 8 after rescaling: ' delayed' 1.2%, ' not' 1.0%, ' late' 0.8%, ' too' 0.7%, ' so' 0.6%, ' a' 0.6%, ' delivered' 0.4%, ' slow' 0.4%
Six sampled completions (14 new tokens each):
- ` vibrant stingam modern such fired across tone Tony Quinn Cannonhand serve him`
- ` legally prepared out changingperson intology bi convertible (65yr-folder`
- ` denied or came weighing 250 cer dark wood fed touch pod marked PseTerm`
- `/is very rout vice801!! CheckmateiiiQL : standpoint file`
- ` asked late 30 seizures ranked 9 distilled classics And doses and length downward seriously`
- ` very extremely uncertain and Chap Reno matters lolasting flowering lighting centres week nineteen`

## 4. Attention
Sentence: `The supplier sent the invoice to the manager because she needed it` (12 tokens, each one word).
Chosen head: layer 5 of 12, head 4 of 12 (counting from 1). I searched all 144 heads for one where the last word 'it' puts most attention on 'invoice'. In this head 'it' gives 85 percent to 'invoice'. Across all 144 heads, 78 put more than half of the last word's attention on the first word 'The' (a resting place), and only 1 put more than 30 percent on 'invoice'. Real models have many layers and many heads; this one head shows one pattern, not 'what the model thinks'.
Matrix (row = the word looking, column = earlier word, each row sums to 1):

| |The| supplier| sent| the| invoice| to| the| manager| because| she| needed| it|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|The|1.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|
| supplier|0.87|0.13|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|
| sent|0.13|0.84|0.02|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|
| the|0.53|0.35|0.08|0.04|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|
| invoice|0.70|0.07|0.01|0.13|0.09|0.00|0.00|0.00|0.00|0.00|0.00|0.00|
| to|0.02|0.02|0.01|0.07|0.85|0.02|0.00|0.00|0.00|0.00|0.00|0.00|
| the|0.21|0.07|0.05|0.04|0.53|0.07|0.04|0.00|0.00|0.00|0.00|0.00|
| manager|0.57|0.01|0.00|0.04|0.09|0.02|0.16|0.11|0.00|0.00|0.00|0.00|
| because|0.15|0.06|0.04|0.10|0.36|0.03|0.04|0.19|0.04|0.00|0.00|0.00|
| she|0.39|0.26|0.01|0.01|0.04|0.01|0.01|0.21|0.03|0.03|0.00|0.00|
| needed|0.16|0.10|0.01|0.00|0.04|0.01|0.00|0.10|0.07|0.46|0.04|0.00|
| it|0.05|0.01|0.00|0.01|0.85|0.02|0.01|0.01|0.01|0.00|0.01|0.02|