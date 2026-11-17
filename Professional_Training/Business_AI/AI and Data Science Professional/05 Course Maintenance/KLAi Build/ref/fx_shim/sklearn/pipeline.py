class Pipeline:
    def __init__(self, steps):
        self.steps = steps
        self.named_steps = dict(steps)

    def __getitem__(self, i):
        return self.steps[i][1]

    def fit(self, X, y=None, **kw):
        for _, s in self.steps[:-1]:
            X = s.fit_transform(X, y)
        self.steps[-1][1].fit(X, y, **kw)
        return self

    def _t(self, X):
        for _, s in self.steps[:-1]:
            X = s.transform(X)
        return X

    def predict(self, X):
        return self.steps[-1][1].predict(self._t(X))

    def predict_proba(self, X):
        return self.steps[-1][1].predict_proba(self._t(X))

    def score(self, X, y):
        return self.steps[-1][1].score(self._t(X), y)


def make_pipeline(*steps):
    return Pipeline([(type(s).__name__.lower(), s) for s in steps])
