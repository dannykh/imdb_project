__author__ = 'Danny'

from prep.IMDB import IMDB
from prep.SqlMovie import SqlMovie
from prep.MovieVector2 import MovieVectorGenerator2
from sklearn import svm, preprocessing, cross_validation, linear_model
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.grid_search import GridSearchCV
import learning.utils as utils
from prep.MovieVector_y import MovieVectorGenerator_y


def test(id='3062729'):
    cn = IMDB()
    mov = SqlMovie(imdb_conn=cn, sql_id=id, mode=1)
    # gen = MovieVectorGenerator2(imdb_conn=cn)
    mov.update()

    gen = MovieVectorGenerator_y(cn)
    return gen.get_vector(mov)


if __name__ == "__main__":
    pass