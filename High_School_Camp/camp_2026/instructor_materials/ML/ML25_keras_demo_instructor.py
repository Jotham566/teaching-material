"""Instructor laptop only. Not in the student pack and not run by the verifier.
TensorFlow and Keras are installed only on the instructor laptop, never in the student environment. Check that the camp Python version has a TensorFlow build before the camp. The official install page for release 2.21 lists Python 3.10 to 3.13 wheels, but other pages disagree, so run programme/preflight_stack.py --tf on the instructor laptop first.
"""
# Instructor laptop only. Not executed by the verifier. Requires TensorFlow (see requirements_note).
import numpy as np
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
X, y = load_iris(return_X_y=True)
X = StandardScaler().fit_transform(X)
model = keras.Sequential([keras.layers.Input((4,)), keras.layers.Dense(8, activation="relu"), keras.layers.Dense(3, activation="softmax")])
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
model.fit(X, y, epochs=30, verbose=0)
print(model.evaluate(X, y, verbose=0))
# Say aloud: this score is on the training flowers, so it proves nothing about new flowers.
