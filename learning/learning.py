from scipy.stats._discrete_distns import skellam_gen

__author__ = 'Danny'

from sklearn import tree, cross_validation, neighbors
from sklearn.metrics import euclidean_distances as l2_dist
import numpy as np
from learning_utils import load_data
from numpy import correlate
from scipy.stats.stats import pearsonr
from math import sqrt

min_leaf_size = 5  # Too small = overfitting, too large = no extrapolation
threshold = 7.5


data, rtags, btags = load_data()
pred = lambda x: 1 if x > threshold else 0
btags = map(pred, rtags)


def kfcv(classifier, data, tags, k=2):
    classifier.fit(data[:len(data) / 2], rtags[:len(data) / 2])

    real = rtags[len(data) / 2:]
    pred = [classifier.predict(item)[0] for item in data[len(data) / 2:]]

    return pearsonr(real, pred)

    sum_errs = 0
    sum_tag = 0
    max_err = 0
    num = 0
    sum_squares_err = 0
    sum_squares_tag = 0
    for item, tag in zip(data[len(data) / 2:], rtags[len(data) / 2:]):
        p = float(classifier.predict(item)[0])
        err = abs(p - tag)
        sum_squares_err += err * err
        sum_squares_tag += tag * tag
        sum_tag += tag
        sum_errs += err
        num += 1
        max_err = max(max_err, err)

    return max_err, sum_errs / num, \
           sum_squares_err / num - (sum_errs / num) * (sum_errs / num), \
           sum_squares_tag / num - (sum_tag / num) * (sum_tag / num)


# print kfcv(data, rtags)

def avg_err(vec1, vec2):
    if len(vec1) != len(vec2):
        raise ValueError(
            'cannot calculate distance on vectors of different dimensions')
    return sum(abs(vec1 - vec2)) / len(vec1)


def bin_stats(pred,real):
    false_positive=float(sum([x for x in pred-real if x>0]))/len(pred)
    false_negative=float(abs(sum([x for x in pred-real if x<0])))/len(pred)
    success_rate=1-float(sum(abs(pred-real)))/len(pred)

    return false_positive,false_negative,success_rate

def kfold(classifier):
    cv = cross_validation.KFold(len(data), 10)
    results = []
    for traincv, testcv in cv:
        probas = classifier.fit([data[i] for i in traincv],
                                [btags[i] for i in traincv]).predict(
            [data[i] for i in testcv])
        results.append(bin_stats([btags[i] for i in testcv], probas))

    return results


def better_inv_dist(dist):
    c = 1.
    return 1. / (c + dist)


def best_k():
    min_err = 1
    min_k = 0

    for k in xrange(19, 20):
        knn_classifier = neighbors.KNeighborsRegressor(k,
                                                       weights=better_inv_dist)
        res = kfold(knn_classifier)
        err = sum(res) / len(res)
        if err < min_err:
            min_k = k
            min_err = err
        print "k = {} : avg err = {}\n".format(k, err)

    print "Min avg is {} for k={}".format(min_err, min_k)


if __name__ == "__main__":
    classifier_tree = tree.DecisionTreeRegressor(min_samples_leaf=min_leaf_size,
                                                 random_state=0)

    k = 19  # best
    knn_classifier = neighbors.KNeighborsRegressor(k, weights=better_inv_dist)

    knn_bin_classifier = neighbors.KNeighborsClassifier(k)

    res= kfold(knn_bin_classifier)

    avg=lambda x: sum(x)/10
    print res
    print [avg([x[i] for x in res]) for i in xrange(0,3)]
