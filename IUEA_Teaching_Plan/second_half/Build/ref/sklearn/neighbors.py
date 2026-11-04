"""k-nearest neighbours (k-NN) regression, as scikit-learn's KNeighborsRegressor with the defaults (Euclidean distance, uniform weights). Ties in distance are broken by row order."""
import numpy as np


class KNeighborsRegressor:
    def __init__(self, n_neighbors=5): self.n_neighbors = n_neighbors
    def fit(self, X, y): self._X, self._y = np.asarray(X, float), np.asarray(y, float); return self
    def kneighbors(self, X, n_neighbors=None):
        k = n_neighbors or self.n_neighbors; X = np.asarray(X, float); dist, ind = [], []
        for q in X:
            d = np.sqrt(((self._X - q) ** 2).sum(axis=1)); i = np.argsort(d, kind='stable')[:k]; dist.append(d[i]); ind.append(i)
        return np.array(dist), np.array(ind)
    def predict(self, X):
        _, ind = self.kneighbors(X); return self._y[ind].mean(axis=1)
