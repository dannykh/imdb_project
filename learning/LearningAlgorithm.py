import numpy as np
from sklearn import cross_validation, metrics
from sklearn.cross_validation import KFold
from utils import load_data
from copy import deepcopy
from enum import Enum
import utils


class ClassificationType(Enum):
    BINARY = 0
    CONTINUOUS = 1
    CATEGORICAL = 2


def get_evaluation(classifier, pred_X, y_true, eval_method):
    """
    :param classifier: An estimator implementing .predict, Which is already
    trained ! i.e classifier.fit was done
    :param pred_X: Set to predict
    :param y_true: True tags of examples in pred_X, order is important !
    :param eval_method: function with which to evaluate. Must be of the form
    eval(y_true,y_pred)
    :return: result of evaluation, probably a float
    """
    y_pred = map(classifier.predict, pred_X)

    return eval_method(y_true, y_pred)


class LearningAlgorithm(object):
    def __init__(self, classifier=None):
        self.classifier = classifier
        self.classifier_copy = deepcopy(classifier)
        self.classification_type = ClassificationType.CONTINUOUS

    def train(self, data, tags):
        self.classifier.fit(data, tags)

    def load_and_train(self, load_from, tag_transform=lambda x: x,
            delimiter=','):
        loaded = load_data(load_from, tag_transform, delimiter)
        self.train(loaded['data'], loaded['tags'])

    def evaluate_comprehensive(self, data, tags, class_type=None, **kwargs):
        class_type = self.classification_type if class_type is None else \
            class_type
        eval_methods = {} if kwargs is None else kwargs
        if class_type == ClassificationType.CONTINUOUS:
            eval_methods.update({
                "mean_absolute_error": metrics.mean_absolute_error#,
                #"mean_squared_error": metrics.mean_squared_error,
                #"r2_score": metrics.r2_score,
                #"median_absolute_error": metrics.median_absolute_error
            })
        if class_type == ClassificationType.BINARY:
            raise NotImplementedError
        if class_type == ClassificationType.CATEGORICAL:
            raise NotImplementedError

        kf = KFold(len(tags), 3)

        results = {}
        for method in eval_methods:
            results.update({method: {"results": []}})

        for train_i, test_i in kf:
            train_set = utils.select_rows(data, train_i)
            train_tags = [tags[i] for i in train_i]
            test_set = utils.select_rows(data, test_i)
            test_tags = [tags[i] for i in test_i]
            self.classifier_copy.fit(train_set, train_tags)
            for method, method_func in eval_methods.iteritems():
                results[method]["results"] += [get_evaluation(
                    self.classifier_copy,
                    test_set, test_tags, method_func)]

        for method in eval_methods:
            results[method].update({"Average": np.average(
                results[method]["results"])})

        return results

    def evaluate(self):
        raise NotImplementedError

    def classify(self, vector):
        return self.classifier.predict(vector)

    def kfcv(self, data, tags, k=5):
        return cross_validation.cross_val_score(self.classifier, data,
            tags)

    def load_and_kfvc(self, load_from, tag_transform=lambda x: x,
            delimiter=',',
            k=5):
        loaded = load_data(load_from, tag_transform, delimiter)
        return self.kfcv(loaded['data'], loaded['tags'], k)
