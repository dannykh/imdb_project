from MovieVector import MovieVectorError, MovieVectorGenerator
from IMDB import IMDB
import imdb_sql_consts
from utils import vec_for_movie


class MovieVectorGenerator1(MovieVectorGenerator):
    def __init__(self, imdb_conn=None):
        self.version=1
        self.imdb_conn = IMDB() if imdb_conn is None else imdb_conn

    def get_vector(self, movie):
        return [movie.get_imdb_rating()] + vec_for_movie(self.imdb_conn, '0',
            movie)

