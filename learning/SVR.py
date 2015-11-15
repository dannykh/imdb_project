from LearningAlgorithm import LearningAlgorithm
import numpy as np
from sklearn import svm, preprocessing, cross_validation
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.grid_search import GridSearchCV
from copy import deepcopy


class SVR(LearningAlgorithm):
    def __init__(self, feat_range=(-1, 1)):
        super(SVR, self).__init__()
        self.pipeline = Pipeline(
            [("scale", preprocessing.MinMaxScaler(feat_range)),
             ("SVR", svm.SVR())])
        # GridSearch is an exhaustive search on classifier parameters
        # i.e tries all options to find best classifier
        kernels = ['linear', 'rbf']
        self.classifier = GridSearchCV(self.pipeline,
            param_grid={"SVR__kernel": kernels})
        self.classifier_copy = deepcopy(self.classifier)

    def evaluate(self, eval_methods=None):
        pass
