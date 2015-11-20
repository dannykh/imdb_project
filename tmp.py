__author__ = 'Danny'

from prep.IMDB import IMDB
from prep.SqlMovie import SqlMovie
from prep.MovieVector2 import MovieVectorGenerator2
from learning.LearningAlgorithm import LearningAlgorithm
from sklearn import svm, preprocessing, cross_validation, linear_model
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.grid_search import GridSearchCV
import learning.utils as utils
import mwparserfromhell as mw
import pywikibot
import wikipedia as wiki

def test(id='3062729'):
    cn = IMDB()
    mov = SqlMovie(imdb_conn=cn, sql_id=id, mode=1)
    # gen = MovieVectorGenerator2(imdb_conn=cn)
    mov.update()

    return mov


from learning.SVR import SVR
from learning.KNN import KNN


def test_learning(data_path="data/MovieVector2/1/data_raw.csv"):
    model = SVR()
    dat = utils.load_data(data_path)
    data, tags = dat['data'], dat['tags']

    print model.evaluate_comprehensive(data, tags)


def test_lasso(data_path="data/MovieVector2/1/data_raw.csv"):
    pipe = Pipeline([("scale", preprocessing.MinMaxScaler((-1, 1))),
                     ("Lasso", linear_model.Lasso())])
    alphas = [0.1, 1, 10]
    classifier = GridSearchCV(pipe,
        param_grid={"Lasso__alpha": alphas})

    alg = LearningAlgorithm(classifier)
    print(alg.classifier.estimator)
    return alg.load_and_kfvc(data_path)


def test_ridge(data_path="data/MovieVector2/1/data_raw.csv"):
    pipe = Pipeline([("scale", preprocessing.MinMaxScaler((-1, 1))),
                     ("ridge", linear_model.Ridge())])
    alphas = [0.1]

    classifier = GridSearchCV(pipe,
        param_grid={"ridge__alpha": alphas})
    alg = LearningAlgorithm(classifier)

    res = utils.load_data(data_path)
    data, tags = res['data'], res['tags']

    print(alg.classifier.estimator)
    rng = [2]
    return alg.kfcv(utils.select_cols(data, rng), tags)


import petl as etl
import numpy as np

if __name__ == "__main__":
    test_learning()
    # print test_ridge()
