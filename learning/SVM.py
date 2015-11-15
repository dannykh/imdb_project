from Model import Model
import numpy as np
from sklearn import svm, preprocessing, cross_validation
from sklearn.pipeline import make_pipeline
from sklearn.grid_search import GridSearchCV
from copy import deepcopy


class SVR(Model):
    def __init__(self, feat_range=(-1, 1)):
        super(SVR, self).__init__()
        self.pipeline = (preprocessing.MinMaxScaler((-1, 1)),
                         svm.SVR())
        # GridSearch is an exhaustive search on classifier parameters
        # i.e tries all options to find best classifier
        self.classifier = GridSearchCV(make_pipeline(*self.pipeline),
            param_grid={})
        self.classifier_copy = deepcopy(self.classifier)

    def evaluate(self, eval_methods=None):
        pass
