"""Session 1: a peek inside one neuron of the trained digit network.  Run:  python neuron_peek.py   (about 20 seconds; numpy and scikit-learn only)
Re-trains the same network as digits_run.py (same data split, same seed, 200 passes), then opens neuron 1 and neuron 2 for the handwritten 3
(dataset index 918) and prints every multiplication, the sum, the bias and the activation. Saves neuron_peek.npz, which the slide figures read.
Check: the 'output' printed for each neuron equals the 16 activations printed by digits_run.py.
"""
import warnings
from pathlib import Path
import numpy as np
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

warnings.filterwarnings('ignore')
HERE = Path(__file__).resolve().parent
d = load_digits()
X, y = d.data, d.target
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)
net = MLPClassifier(hidden_layer_sizes=(16,), activation='relu', solver='adam', random_state=0, max_iter=1, warm_start=True)
for epoch in range(1, 201):
    net.partial_fit(Xtr / 16.0, ytr, classes=np.arange(10)) if epoch > 1 else net.fit(Xtr / 16.0, ytr)
pick = int(np.where(yte == 3)[0][0])
raw = Xte[pick]
x = raw / 16.0                       # the 64 inputs, each between 0 and 1
W, b = net.coefs_[0], net.intercepts_[0]      # 64 x 16 weights, 16 biases
total = x @ W + b
out = np.maximum(0, total)
print('The 3 as 64 inputs (ink / 16), neuron 1 and neuron 2 opened up:\n')
keep = {}
for k in (0, 1):
    prod = x * W[:, k]
    top = np.argsort(-np.abs(prod))[:3]
    print(f'Neuron {k + 1}')
    for i in top:
        print(f'  pixel {i:2d}: ink {raw[i]:4.0f} -> input {x[i]:.3f}  x weight {W[i, k]:+.3f}  = {prod[i]:+.3f}')
    rest = prod.sum() - prod[top].sum()
    print(f'  the other 61 pixels added together: {rest:+.3f}')
    print(f'  sum of all 64 products: {prod.sum():+.3f}   bias: {b[k]:+.3f}   total: {total[k]:+.3f}   activation (ReLU) output: {out[k]:.3f}\n')
    keep[f'top{k}'] = top
    keep[f'rest{k}'] = rest
print('All 16 outputs:', np.round(out, 2))
np.savez(HERE / 'neuron_peek.npz', raw=raw, x=x, W=W, b=b, total=total, out=out, pick=pick, **keep)
