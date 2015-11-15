__author__ = 'Danny'

from prep.IMDB import IMDB
from prep.SqlMovie import SqlMovie
from prep.MovieVector2 import MovieVectorGenerator2


def test(id='3062729'):
    cn = IMDB()
    mov = SqlMovie(imdb_conn=cn, sql_id=id, mode=1)
    gen = MovieVectorGenerator2(imdb_conn=cn)

    return gen.get_vector(mov)


from learning.SVM import SVR


def test_learning(data_path="data/MovieVector2/1/data_raw.csv"):
    model = SVR()

    return model.load_and_kfvc(data_path)


import petl as etl
import numpy as np
