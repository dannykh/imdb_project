import numpy as np

import prep.movie_vector.vector_utils_2 as utils2
from MovieVector import MovieVectorGenerator
from prep.IMDB import IMDB


def get_field(movie, field):
    if movie.has_key(field):
        return np.nan if movie[field] is None or not movie[field] else movie[
            field]

    return np.nan


def get_ith_star_avg(conn, movie, i):
    print i
    return utils2.get_actor_avg(conn, movie['stars'][i],
        to_year=movie['year'])


def get_star_avg_funcs(conn):
    res = []
    for i in xrange(0, 5):
        print "#%s" % i
        res.append(
            ("star_avg_%s" % i,
             lambda movie, i=i: get_ith_star_avg(conn, movie, i)))
    return res


class MovieVectorGenerator3(MovieVectorGenerator):
    def __init__(self, imdb_conn=None):
        self.version = 3
        self.imdb_conn = IMDB() if imdb_conn is None else imdb_conn

        self._vectorizer = [
            ("id", lambda mov: get_field(mov, 'id')),
            ("year", lambda mov: get_field(mov, 'year')),
            ("rating", lambda mov: get_field(mov, 'rating')),
            ("budget", lambda mov: get_field(mov, 'budget')),
            ("actors", lambda mov: get_field(mov, 'actors')),
            ("directors", lambda mov: get_field(mov, 'directors')),
            ("producers", lambda mov: get_field(mov, 'producers')),
            ("stars", lambda mov: get_field(mov, 'stars')),
            ("gross", lambda mov: get_field(mov, 'gross')),
            ('genres', lambda mov: get_field(mov, 'genres')),
            ('taglines', lambda mov: get_field(mov, 'taglines'))
        ]
        self._vectorizer += (get_star_avg_funcs(self.imdb_conn))

        self.header = [x[0] for x in self._vectorizer]
