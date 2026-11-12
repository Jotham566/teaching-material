"""Formula Sheet: every formula taught in the course, in standard notation, with each symbol named, a worked example (computed here) and the session that teaches it.
Run from Build/:  python kit/make_formulas.py   (also called by make_docs.py). Writes 03 Learner Materials/Formula Sheet.docx and .pdf."""
import math, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
BUILD = HERE.parent
EDITION = BUILD.parent.parent
sys.path.insert(0, str(BUILD / 'templates_gen'))
from docx_kit import *  # noqa


def f(x, n=2):
    return f'{x:,.{n}f}'.rstrip('0').rstrip('.') if n else f'{x:,.0f}'


def entries():
    E = []
    # --- neuron and learning
    ws = 2 * 100 + 10 * 3 + 30
    E.append(('Neurons and learning', 'Weighted sum of a neuron', 'z = w₁x₁ + w₂x₂ + … + wₙxₙ + b   =   Σ wᵢxᵢ + b   =   w · x + b',
              'x: inputs. w: weights, how much each input counts. b: bias, shifts when the neuron switches on. z: the weighted sum.',
              f'House: 2×100 m² + 10×3 bedrooms + 30 = {ws} (UGX million).', '1'))
    E.append(('Neurons and learning', 'Activation functions', 'ReLU(z) = max(0, z)      sigmoid σ(z) = 1 / (1 + e^(−z))',
              'f(z) is applied to the weighted sum. ReLU gives 0 for negative values and z otherwise. Sigmoid squeezes any number into 0 to 1.',
              f'ReLU(−0.71) = 0; ReLU(4.58) = 4.58. σ(0) = 0.5; σ(4.58) = {1/(1+math.exp(-4.58)):.2f}.', '1'))
    E.append(('Neurons and learning', 'A layer of neurons', 'a = f(W x + b)',
              'x: input vector. W: a matrix with one row of weights per neuron. b: one bias per neuron. a: the layer output (one number per neuron).',
              'Digit network: 64 inputs, 16 neurons: W is 16 × 64 = 1,024 weights, plus 16 biases.', '1'))
    E.append(('Neurons and learning', 'Loss (squared error and MSE)', 'L = ½ (y − ŷ)²      MSE = (1/n) Σ (yᵢ − ŷᵢ)²',
              'y: the true value. ŷ: the prediction (y-hat). n: number of examples. The ½ makes the derivative tidy; many texts omit it.',
              f'Prices 220, 150, 310 against predictions 230, 150, 300: MSE = (100 + 0 + 100) / 3 = {200/3:.1f}.', '0, 1'))
    E.append(('Neurons and learning', 'Cross-entropy loss (language models)', 'L = −ln p(correct token)',
              'p: the probability the model gave to the right next token. Smaller loss means a better guess.',
              f'"days" got 18%: L = −ln 0.18 = {-math.log(0.18):.2f}. A perfect guess (p = 1) gives 0.', '5'))
    E.append(('Neurons and learning', 'Gradient descent', 'w ← w − η · ∂L/∂w',
              'η (eta): learning rate, the step size. ∂L/∂w: the gradient, how much the loss changes when w changes. ← means "is replaced by".',
              'x = 2, y = 3, w = 0.5, L = ½(y − wx)²: gradient = −x(y − wx) = −4. With η = 0.1: w = 0.5 + 0.4 = 0.9.', '0, 1'))
    E.append(('Neurons and learning', 'Backpropagation (chain rule)', '∂L/∂w = ∂L/∂ŷ · ∂ŷ/∂z · ∂z/∂w',
              'The chain rule: the effect of a weight on the loss is the product of the effects along the path (weight to sum, sum to prediction, prediction to loss), computed backwards from the output.',
              'For ŷ = z = wx and L = ½(y − ŷ)²: (−(y − ŷ)) · 1 · x = −2 × 2 = −4 at w = 0.5 (y − ŷ = 2, x = 2).', '0, 1'))
    # --- trees and neighbours
    E.append(('Examples and measuring', 'Gini impurity (decision trees)', 'G = 1 − Σ pₖ²',
              'pₖ: the share of examples of class k in a group. 0 is a pure group.', 'A group with 50% yes and 50% no: G = 1 − (0.25 + 0.25) = 0.5. A group of all yes: G = 0.', '2'))
    E.append(('Examples and measuring', 'Entropy and information gain', 'H = − Σ pₖ log₂ pₖ      gain = H(parent) − weighted average H(children)',
              'The same idea as Gini: how mixed a group is. A split is chosen to maximise the gain.', f'A 50/50 group: H = 1 bit. A 90/10 group: H = {-(0.9*math.log2(0.9)+0.1*math.log2(0.1)):.2f} bits.', '2'))
    E.append(('Examples and measuring', 'k-nearest neighbours and scaling', 'ŷ = (1/k) Σ yᵢ (regression)      majority vote (classification)      x′ = (x − min) / (max − min)',
              'The k closest training examples decide. Scaling puts every feature on 0 to 1 so no feature dominates the distance.',
              'House prices of the 3 nearest sold houses 250, 270, 190: ŷ = 710 / 3 = 237. 80 m² on a 40 to 120 range: (80 − 40) / 80 = 0.5.', '2'))
    E.append(('Examples and measuring', 'Confusion-matrix measures', 'accuracy = (TP + TN) / (TP + TN + FP + FN)      precision = TP / (TP + FP)      recall = TP / (TP + FN)',
              'TP: true positives, FP: false positives, FN: false negatives, TN: true negatives. Recall is also called sensitivity or true positive rate.',
              'Smoke alarm TP 16, FP 34, FN 4, TN 946: accuracy 962/1000 = 96.2%; precision 16/50 = 32%; recall 16/20 = 80%.', '0, 3'))
    E.append(('Examples and measuring', 'F1, false positive rate, ROC and AUC', 'F1 = 2PR / (P + R) = 2 / (1/P + 1/R)      FPR = FP / (FP + TN)',
              'F1 is the harmonic mean of precision (P) and recall (R). The ROC curve plots TPR (recall) against FPR for every threshold; AUC is the area under that curve (1 is perfect, 0.5 is a coin flip).',
              f'P = 0.32, R = 0.80: F1 = {2*0.32*0.8/(0.32+0.8):.2f}. FPR = 34 / 980 = {34/980*100:.1f}%.', '0, 3'))
    E.append(('Examples and measuring', 'k-fold cross-validation', 'score = (1/k) Σ scoreᵢ',
              'Split the data into k parts; train on k − 1 parts, test on the held-out part; rotate; average the k scores.', 'Session 2 claims: fold scores 44/48, 44/48, 45/48, 45/48, 45/48 (0.917, 0.917, 0.938, 0.938, 0.938) give 4.646 / 5 = 0.929.', '2'))
    # --- words as numbers
    E.append(('Words and language models', 'TF-IDF', 'tf-idf(t, d) = tf(t, d) × log(N / df(t))      scikit-learn: idf = ln[(1 + N) / (1 + df)] + 1',
              't: a term. d: a document. tf: how often t appears in d. N: number of documents. df: how many documents contain t.',
              'N = 40, a term in 4 messages: idf (textbook) = log(40/4) = log 10; a term in 22 messages: log(40/22) = 0.6. Rare terms weigh more.', '4'))
    a, b = (3, 4), (6, 8)
    E.append(('Words and language models', 'Distances and similarity', 'Euclidean d = √Σ(aᵢ − bᵢ)²   Manhattan d = Σ|aᵢ − bᵢ|   dot a·b = Σ aᵢbᵢ   cos θ = a·b / (‖a‖ ‖b‖)',
              'a, b: vectors (lists of numbers). ‖a‖ = √Σ aᵢ² is the length. Cosine ignores length and compares direction; cosine distance = 1 − cos θ. Also called L2 and L1 distance and inner product.',
              f'a = (3, 4), b = (6, 8): Euclidean = 5; Manhattan = 7; dot = {3*6+4*8}; cos θ = 50 / (5 × 10) = 1.00.', '4, 9'))
    z = [3, 2, 0]
    sm = lambda zz, T=1: [math.exp(v / T) / sum(math.exp(u / T) for u in zz) for v in zz]
    E.append(('Words and language models', 'Softmax and temperature', 'pᵢ = e^(zᵢ/T) / Σⱼ e^(zⱼ/T)',
              'z: the logits (raw scores) for every token. T: temperature (T = 1 is plain softmax; lower T sharpens, higher T flattens). The p sum to 1.',
              'Logits 3, 2, 0: p = ' + ', '.join(f'{100*p:.1f}%' for p in sm(z)) + '. At T = 2: ' + ', '.join(f'{100*p:.0f}%' for p in sm(z, 2)) + '.', '5'))
    E.append(('Words and language models', 'Language model and embeddings', 'P(x₁ … xₙ) = Π P(xₜ | x₁ … xₜ₋₁)      xₜ = E[tokenₜ] + positionₜ',
              'The model gives each next token a probability given the earlier ones; the sequence probability is the product. E: the embedding matrix (one row of numbers per token). Position information is added.',
              'GPT-2 small: E has 50,257 rows of 768 numbers (38,597,376 numbers).', '5'))
    E.append(('Words and language models', 'Scaled dot-product attention', 'Attention(Q, K, V) = softmax( Q Kᵀ / √dₖ ) V',
              'Q (queries), K (keys), V (values): matrices made from the token vectors. dₖ: the key length. Each token scores every other token (QKᵀ), softmax turns scores into weights, and the output is a weighted blend of the values.',
              'See the Session 5 toy: scores turn into shares 9%, 67%, 24%; the output blends the values with those shares.', '5'))
    E.append(('Words and language models', 'Perplexity', 'perplexity = exp( average cross-entropy per token )',
              'A standard way to report how well a language model predicts text; lower is better.', f'An average loss of 1.71 gives perplexity {math.exp(1.71):.1f}.', '6'))
    # --- size, adaptation
    E.append(('Size and adaptation', 'Model memory', 'memory ≈ parameters × bytes per parameter',
              'FP32 = 4 bytes, FP16 = 2, INT8 = 1, 4-bit = 0.5. Weights only; running a model needs more memory for working data.',
              'GPT-2 small: 124,439,808 × 4 bytes ≈ 498 MB in FP32; 7 billion parameters at FP16 = 14 GB, at 4-bit = 3.5 GB.', '7'))
    E.append(('Size and adaptation', 'Quantisation', 'q = round(x / s) + z      x̂ = s · (q − z)',
              'x: the original number. s: scale. z: zero point. q: the stored whole number. x̂: the value recovered (close to x, not identical).',
              'x = 0.37, s = 0.01, z = 0: q = 37, x̂ = 0.37. x = 0.374: q = 37, x̂ = 0.37 (a small rounding error).', '7'))
    E.append(('Size and adaptation', 'LoRA (low-rank adaptation)', "W′ = W + B A      trainable numbers = r (d + k) instead of d × k",
              'W: a frozen d × k weight matrix. B: d × r. A: r × k. r: the rank (small). Only B and A are trained. The real method scales BA by a constant.',
              f'd = 768, k = 2,304, r = 8: r(d + k) = {8*(768+2304):,} against d × k = {768*2304:,}.', '9'))
    E.append(('Size and adaptation', 'Retrieval and the context budget', 'retrieve the k chunks with the largest cos θ      prompt + retrieved + answer ≤ context window',
              'Each chunk and the question are embedded; the k most similar chunks go into the prompt. The total tokens must fit the model’s context window.',
              'Question 94 + 3 chunks 104 + answer limit 300 = 498 tokens, against 94 + 1,074 + 300 = 1,468 for the whole handbook.', '9'))
    E.append(('Size and adaptation', 'Evaluation accuracy and expected cost', 'accuracy = correct / total      expected cost = P(error) × cost of an error',
              'Score a model or a prompt on a fixed evaluation set; weigh how often it errs by how much an error costs.', 'Baseline answering "not stated" scores 2 / 10 = 20%.', '8, 10'))
    # --- agents, governance, plan
    E.append(('Agents, governance and plan', 'Risk score and approval time', 'risk = likelihood × impact      approval time T = n × t',
              'Likelihood and impact are each rated (for example 1 to 5). n: number of approvals, t: minutes per approval. Least privilege: granted permissions ⊆ needed permissions.',
              'Flat tyre: 4 × 2 = 8. Data leakage: 3 × 5 = 15. Three approvals at 2 minutes: 3 × 2 = 6 minutes.', '11, 13'))
    E.append(('Agents, governance and plan', 'Hours saved, net benefit, payback and ROI', 'H = n × (t₀ − t₁) / 60      net benefit = benefits − costs      payback = set-up cost / net benefit per month      ROI = net benefit / cost × 100%',
              'n: runs a month. t₀, t₁: minutes before and after. Payback is in months.',
              'n = 4, t₀ = 90, t₁ = 10: H = 5.3 hours. Kettle: saving 20,000 a month, cost 60,000: payback 3 months; first-year net 180,000; first-year costs 180,000; ROI 100%.', '12'))
    E.append(('Agents, governance and plan', 'Total cost of ownership', 'TCO = set-up + months × monthly fee',
              'All the money over the whole contract, not only the first month.', 'Set-up 0, 36 months at USD 2,400: 36 × 2,400 = USD 86,400.', '13'))
    E.append(('Agents, governance and plan', 'Data quality and readiness', 'completeness = filled / all × 100%      uniqueness = distinct / all      readiness = Σ points (Green 2, Amber 1, Red 0)      change = (new − old) / old',
              'Completeness counts non-missing values; uniqueness counts distinct records; readiness sums six area ratings out of 12.',
              'NVF: (60 − 2) / 60 = 96.7% complete; 59 / 60 = 0.983 unique; 2+1+1+1+0+1 = 6 of 12; score 6 to 9: +50%.', '14'))
    return E


def build():
    name = 'Formula Sheet'
    d = new_doc(name)
    title(d, 'Formula Sheet', 'Applied AI and Automation for Executives. The formulas you will meet in books, papers and vendor documents, with every symbol named.')
    box(d, 'How to use this sheet', ['Each row gives the standard name, the formula in standard notation, what each symbol means, a worked example with the numbers used in class, and the session that teaches it.',
                                     'Different books use slightly different symbols. When you meet a formula elsewhere, look for the same pieces: the inputs, the weights, the loss and the step.',
                                     'The worked numbers come from the course examples and recorded runs; the Session numbers refer to the slides and the Take-away Sheets.'], size=9.5)
    sect = None
    for sec, nm, fm, sym, ex, ses in entries():
        if sec != sect:
            sect = sec
            h2(d, sec, before=10)
        para(d, nm, 10.5, True, before=5, after=0, keep=True)
        para(d, fm, 11, False, False, color='AE2525', after=1, keep=True)
        para(d, 'Symbols: ' + sym, 9, after=1, keep=True)
        para(d, 'Worked example: ' + ex, 9, after=1, keep=True)
        para(d, 'Session ' + ses, 8.5, color='767676', after=3)
    out = EDITION / '03 Learner Materials' / (name + '.docx')
    save(d, out)
    subprocess.run(['soffice', '-env:UserInstallation=file:///tmp/lo_formulas', '--headless', '--convert-to', 'pdf', '--outdir', str(out.parent), str(out)], capture_output=True)
    print('wrote', out.name)


if __name__ == '__main__':
    build()
