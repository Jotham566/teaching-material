# Session 1 recorded runs: Seeing (pixels, features and neurons)

Date: 5 November 2026. Tool: Python 3.12.10, scikit-learn 1.9.1, numpy 2.5.4, on a Mac laptop. No internet needed.
Scripts and outputs: `demo_runs/s01/` (`digits_run.py`, `rgb_image.py`, `run_output.txt`, `rgb_output.txt`, `results_s01.npz`, `results_s01.json`). Re-run live with `python digits_run.py`.

## Run 1: handwritten digits (`digits_run.py`)
- Input: the 1,797 8 x 8 grey digit images bundled with scikit-learn (`load_digits`, pixel values 0 to 16). Split with `train_test_split(test_size=0.25, random_state=0, stratify)`: 1,347 train, 450 test.
- Model: `MLPClassifier(hidden_layer_sizes=(16,), activation='relu', solver='adam', random_state=0)`, trained for 200 passes, inputs divided by 16. 64 inputs, 16 hidden neurons, 10 outputs, 1,210 parameters.
- Number of runs: 1 main run (deterministic with the fixed seed, run twice with identical output) plus 5 runs with random_state 0 to 4 for the spread.
- Output (exact, from `run_output.txt`): test accuracy after 1, 2, 3, 5, 10, 20, 50, 100, 200 passes = 0.1733, 0.1778, 0.1978, 0.2378, 0.3667, 0.6644, 0.9222, 0.9556, 0.9689. Final: 0.9837 on the training images; 0.9689 on the 450 unseen test images (436 right, 14 wrong). Five random starts: 0.9689, 0.9689, 0.9622, 0.9644, 0.9689.
- Image 918 (a handwritten 3) printed as 64 numbers; hidden activations and output probabilities for it: probability 0.958 for digit 3.
- Fragility: the 450 test images moved 0, 1 and 2 pixels to the right (zero fill): 0.9689, 0.4578, 0.1422.
- Favourite digit of each hidden neuron (digit shown by most of the neuron's 30 strongest training images): neuron 13 = 0 (30 of 30), neuron 8 = 9 (27 of 30), neurons 10 and 16 = 4 (25 of 30), and so on (see `run_output.txt`).
- Slides: pixels, features (0 and 1 only, one threshold rule: 352 of 360 right, computed in `kit/diagrams_t01.py` from the same dataset), layers, neurons, forward pass, learning curve, gallery (first 8 test images and first 4 mistakes), 97% stat, shift.
- Honest limits: tidy 8 x 8 research images, not real forms. The dataset is, per the scikit-learn documentation, a copy of the test set of the UCI optical recognition of handwritten digits data.

## Run 2: a colour picture as RGB (`rgb_image.py`)
- A sunrise over a hill, 8 x 8 pixels, made by the script (own work, no licence issue). Printed as (R, G, B) triples; 8 x 8 x 3 = 192 numbers; a 1,000 x 1,000 photo would have 3,000,000 numbers.

## Not run
- Dog-or-cat with a pretrained image model: NOT run and NOT claimed in the slides. Optional live extra only if the lecturer runs it beforehand with an image licensed for use.
- The payment-risk checklist (weights 3, 2, 1, cut-off 4) is a hand calculation on the slides, not a model.
