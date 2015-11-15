import numpy as np
from sklearn import cross_validation
from utils import load_data


class Model(object):
    def __init__(self):
        self.classifier_copy = None
        self.classifier = None

    def train(self, data, tags):
        self.classifier.fit(data, tags)

    def load_and_train(self, load_from, tag_transform=lambda x: x,
            delimiter=','):
        loaded = load_data(load_from, tag_transform, delimiter)
        self.train(loaded['data'], loaded['tags'])

    def evaluate(self, eval_methods=None):
        raise NotImplementedError

    def classify(self, vector):
        return self.classifier.predict(vector)

    def kfcv(self, data, tags, k=5):
        return cross_validation.cross_val_score(self.classifier_copy, data,
            tags)

    def load_and_kfvc(self, load_from, tag_transform=lambda x: x, delimiter=',',
            k=5):
        loaded = load_data(load_from, tag_transform, delimiter)
        return self.kfcv(loaded['data'], loaded['tags'], k)
