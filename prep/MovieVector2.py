from MovieVector import MovieVectorGenerator, MovieVectorError

from IMDB import IMDB
import vector_utils_2 as utils2
import numpy as np

"""""
 - All continuous input that are bounded, rescale them to [-1, 1]
  through x = (2x - max - min)/(max - min).

 - for every continuous feature, compute its mean (u) and standard deviation
 (s) and do x = (x - u)/s.

 - binarize catagorical
"""""


def get_genre_vec(movie, all_genres=None, conn=None):
    if all_genres is None:
        if conn is None:
            raise MovieVectorError("Bad parameters")
        all_genres = utils2.get_all_genres(conn)
    return map(lambda genre: 1.0 if genre in movie.get_genres() else -1.0,
        all_genres)


def normalize_continuous_var(val, max, min, mean, std_dev):
    val = float((2.0 * val - max - min)) / float((max - min))
    return float((val - mean)) / float(std_dev)


def get_normalization_params(query):
    raise NotImplementedError


class MovieVectorGenerator2(MovieVectorGenerator):
    def __init__(self, imdb_conn=None):
        self.version = 2
        self.imdb_conn = IMDB() if imdb_conn is None else imdb_conn
        # Following are prep vector parameters
        self.all_genres = utils2.get_all_genres(self.imdb_conn)
        self.VECTOR_DESC = "[rating,[stars1-3 simple avg],directors simple " \
                           "avg,[binary genres]]"
        self.VECTOR_FORMAT = [2, 2, 2, 2, 2] + [0] * len(self.all_genres)

    def get_vector(self, movie):
        movie.update()
        # rating
        movie_vec = [movie.get_imdb_rating()]

        # stars avg ratings
        movie_vec += [utils2.actor_movie_average(self.imdb_conn,
            actor_id, to_year=movie.year) for actor_id in movie.get_stars()[:3]]

        # avg of directors avgs
        movie_vec += [np.average(
            map(lambda dir_id: utils2.director_average(self.imdb_conn,
                dir_id, to_year=movie.year), movie.get_directors()))]

        # genres binarized
        movie_vec += get_genre_vec(movie, self.all_genres)

        #
        assert len(movie_vec) == len(self.VECTOR_FORMAT)
        return np.array(movie_vec,dtype=float)
