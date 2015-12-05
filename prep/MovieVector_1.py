from MovieVector import MovieVectorError, MovieVectorGenerator
from IMDB import IMDB
import imdb_sql_consts
from utils import vec_for_movie


class MovieVectorGenerator1(MovieVectorGenerator):
    def __init__(self, imdb_conn=None):
        self.version=1
        self.imdb_conn = IMDB() if imdb_conn is None else imdb_conn
        self.header=['rating']

    def get_vector(self, movie):
        return [movie['rating']]

