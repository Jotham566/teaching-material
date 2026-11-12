"""Session 1 demonstration script (the lecturer can re-run it live).  Run:  python digits_run.py
Needs: python 3, numpy, scikit-learn.  No internet: the digits data ships inside scikit-learn.
Prints every number shown on the Session 1 slides and saves them to results_s01.json / results_s01.npz in this folder.
"""
import json, warnings
from pathlib import Path
import numpy as np
import sklearn
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

warnings.filterwarnings('ignore')
HERE = Path(__file__).resolve().parent
np.set_printoptions(linewidth=200)

d = load_digits()
X, y = d.data, d.target            # X: 1797 x 64 numbers from 0 (white) to 16 (black ink); y: the digit
print('scikit-learn', sklearn.__version__, 'numpy', np.__version__)
print('images:', X.shape[0], ' numbers per image:', X.shape[1], ' (8 x 8)')
Xtr, Xte, ytr, yte, itr, ite = train_test_split(X, y, np.arange(len(y)), test_size=0.25, random_state=0, stratify=y)
print('train', len(ytr), 'test', len(yte))

# 1. one image as numbers
pick = int(np.where(yte == 3)[0][0])          # the first '3' in the test set
img_i = int(ite[pick])
print('\nImage shown as numbers: dataset index', img_i, 'true digit', y[img_i])
print(d.images[img_i].astype(int))

# 2. the network: 64 inputs -> 16 hidden neurons -> 10 outputs, trained with the loop from Session 0
net = MLPClassifier(hidden_layer_sizes=(16,), activation='relu', solver='adam', random_state=0, max_iter=1, warm_start=True)
curve = []                                       # test accuracy after each pass over the training data
checkpoints = {}
for epoch in range(1, 201):
    net.partial_fit(Xtr / 16.0, ytr, classes=np.arange(10)) if epoch > 1 else net.fit(Xtr / 16.0, ytr)
    if epoch in (1, 2, 3, 5, 10, 20, 50, 100, 200):
        acc = float((net.predict(Xte / 16.0) == yte).mean())
        curve.append((epoch, acc))
        checkpoints[epoch] = net.coefs_[0].copy()
        print(f'after {epoch:3d} passes: accuracy on the 450 unseen test images = {acc:.4f}')
acc_train = float((net.predict(Xtr / 16.0) == ytr).mean())
pred = net.predict(Xte / 16.0)
acc = float((pred == yte).mean())
print(f'\nFinal: accuracy on training images {acc_train:.4f}; on {len(yte)} unseen test images {acc:.4f} ({int((pred == yte).sum())} right, {int((pred != yte).sum())} wrong)')
n_par = sum(c.size for c in net.coefs_) + sum(b.size for b in net.intercepts_)
print('number of parameters (weights + biases):', n_par, ' = 64*16 + 16 + 16*10 + 10 =', 64 * 16 + 16 + 16 * 10 + 10)

# 3. one prediction in detail
x = Xte[pick:pick + 1] / 16.0
hidden = np.maximum(0, x @ net.coefs_[0] + net.intercepts_[0])[0]
proba = net.predict_proba(x)[0]
print('\nHidden layer: 16 neuron activations for the 3 above:', np.round(hidden, 2))
print('Output probabilities for digits 0..9:', np.round(proba, 3), '-> predicts', int(proba.argmax()))

# 4. mistakes and a 12-image gallery
wrong = np.where(pred != yte)[0]
print('\nMistakes (true -> predicted):', [(int(yte[i]), int(pred[i])) for i in wrong])
gallery = list(range(0, 12))
print('Gallery (first 12 test images) true:', [int(yte[i]) for i in gallery], 'predicted:', [int(pred[i]) for i in gallery])

# 5. fragility: shift every test image by 1 and 2 pixels to the right (zero fill) and ask again
def shift(imgs, k):
    a = imgs.reshape(-1, 8, 8)
    out = np.zeros_like(a)
    out[:, :, k:] = a[:, :, :8 - k]
    return out.reshape(len(imgs), 64)
shift_acc = {}
for k in (0, 1, 2):
    a = float((net.predict(shift(Xte, k) / 16.0) == yte).mean())
    shift_acc[k] = a
    print(f'test images shifted {k} pixel(s) right: accuracy {a:.4f}')

# 6. run it 5 times with other random starts, to show how much the result moves
seeds = {}
for s in range(5):
    n2 = MLPClassifier(hidden_layer_sizes=(16,), activation='relu', solver='adam', random_state=s, max_iter=200).fit(Xtr / 16.0, ytr)
    seeds[s] = float((n2.predict(Xte / 16.0) == yte).mean())
print('\nTest accuracy with five different random starts (200 passes each):', {k: round(v, 4) for k, v in seeds.items()})

# 7. what each of the 16 first-layer neurons likes: the digit that most of its 30 strongest training images show
act = np.maximum(0, (Xtr / 16.0) @ net.coefs_[0] + net.intercepts_[0])      # 1347 x 16
fav = []
print('\nFavourite digit of each hidden neuron (among the 30 training images that make it fire hardest):')
for k in range(16):
    top = np.argsort(-act[:, k])[:30]
    vals, cnt = np.unique(ytr[top], return_counts=True)
    j = int(cnt.argmax())
    fav.append((int(vals[j]), int(cnt[j])))
    print(f'  neuron {k + 1:2d}: digit {vals[j]} ({cnt[j]} of 30)')

np.savez(HERE / 'results_s01.npz', images=d.images, target=y, img_i=img_i, ite=ite, yte=yte, pred=pred, w1_final=net.coefs_[0], w1_pass1=checkpoints[1],
         w1_pass10=checkpoints[10], hidden=hidden, proba=proba, pick=pick, xte=Xte)
json.dump(dict(fav=fav, curve=curve, acc=acc, acc_train=acc_train, n_par=n_par, shift=shift_acc, seeds=seeds, wrong=[(int(yte[i]), int(pred[i])) for i in wrong]), open(HERE / 'results_s01.json', 'w'), indent=1)
