import numpy as np
from sklearn import cross_validation


class Model(object):
    def __init__(self):
        self.pipeline = None
        self.classifier = None

    def train(self, data, tags):
        self.classifier.fit(data, tags)

    def load_and_train(self, load_from, delimiter=','):
        loaded = np.genfromtxt(load_from, dtype=float, delimiter=delimiter)
        self.train(loaded[:, 1:], loaded[:, 0])

    def evaluate(self, eval_methods=None):
        raise NotImplementedError

    def classify(self, vector):
        return self.classifier.predict(vector)

    def kfcv(self, data, tags, k=5):
        return cross_validation.cross_val_score(self.pipeline, data, tags)

    def load_and_kfvc(self, load_from, delimiter=',', k=5):
        loaded = np.genfromtxt(load_from, dtype=float, delimiter=delimiter)
        return self.kfcv(loaded[:, 1:], loaded[:, 0], k)
