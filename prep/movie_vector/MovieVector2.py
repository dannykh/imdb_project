import numpy as np

import prep.movie_vector.vector_utils_2 as utils2
from movievector import MovieVectorGenerator, MISSING_FEAT
from prep.IMDB import IMDB


class MovieVectorGenerator2(MovieVectorGenerator):
    def __init__(self, imdb_conn=None):
        self.version = 2
        self.imdb_conn = IMDB() if imdb_conn is None else imdb_conn
        # Following are prep vector parameters
        self.all_genres = utils2.get_all_genres(self.imdb_conn)
        self.VECTOR_DESC = "[rating,[stars1-5 simple avg],directors simple " \
                           "avg,[binary genres]]"
        self.NUM_ACTORS_AVGS = 5
        self.VECTOR_FORMAT = [2] + [2] * self.NUM_ACTORS_AVGS + [2] + \
                             [0] * len(self.all_genres)

    def get_vector(self, movie):
        movie.update()
        # rating
        movie_vec = [movie.get_imdb_rating()]

        # stars avg ratings
        simple_avg_count = self.NUM_ACTORS_AVGS
        if len(movie.get_stars()) < self.NUM_ACTORS_AVGS:
            simple_avg_count = self.NUM_ACTORS_AVGS - len(movie.get_stars())
        movie_vec += [utils2.star_movie_average(self.imdb_conn,
            actor_id, to_year=movie.year) for actor_id in
                      movie.get_stars()[:simple_avg_count]]
        movie_vec += [MISSING_FEAT] * (self.NUM_ACTORS_AVGS - simple_avg_count)

        # avg of directors avgs
        movie_vec += [np.average(
            map(lambda dir_id: utils2.director_average(self.imdb_conn,
                dir_id, to_year=movie.year), movie.get_directors()))]

        # genres binarized
        movie_vec += utils2.get_genre_vec(movie, self.all_genres)

        #
        assert len(movie_vec) == len(self.VECTOR_FORMAT)
        return np.array(movie_vec, dtype=float)
