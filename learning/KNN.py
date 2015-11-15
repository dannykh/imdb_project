from LearningAlgorithm import LearningAlgorithm
from sklearn import neighbors, preprocessing
from sklearn import pipeline
from copy import deepcopy
from sklearn.grid_search import GridSearchCV
import numpy as np
from sklearn.metrics import euclidean_distances as l2_dist


def l2_dist_fixed(vec1, vec2):
    dist = l2_dist(vec1, vec2)
    return dist if dist != 0 else 1e-30


class KNN(LearningAlgorithm):
    def __init__(self, feat_range=(-1, 1)):
        super(KNN, self).__init__()
        self.pipeline = pipeline.Pipeline(
            [("scale", preprocessing.MinMaxScaler(feat_range)),
             ("KNN", neighbors.KNeighborsRegressor(metric=l2_dist_fixed))])
        # GridSearch is an exhaustive search on classifier parameters
        # i.e tries all options to find best classifier
        k_range = range(10, 20)
        self.classifier = GridSearchCV(self.pipeline,
            param_grid={"KNN__n_neighbors": k_range,
                        "KNN__weights": ['uniform', 'distance']})
        self.classifier_copy = deepcopy(self.classifier)

    def evaluate(self, eval_methods=None):
        pass
