import prep.movie_vector.vector_utils_y_changed as utils_y
from MovieVector import MovieVectorGenerator
from prep.IMDB import IMDB
from vector_utils_4 import get_movie_features

HEADER = [
    'Year',
    'Star_1 Is Male',
    'Star_1 Years of Acting',
    'Star_1 Number of Movies',
    'Star_1 Avg',
    'Star_1 - Director Avg',
    'Star_2 Is Male',
    'Star_2 Years of Acting',
    'Star_2 Number of Movies',
    'Star_2 Avg',
    'Star_2 - Director Avg',
    'Star_3 Is Male',
    'Star_3 Years of Acting',
    'Star_3 Number of Movies',
    'Star_3 Avg',
    'Star_3 - Director Avg',
    'director avg rating',
    'writer avg rating',
    'composer avg rating',
    'Is Drama',
    'Is Short',
    'Is Comedy',
    'Is Mystery',
    'Is Documentary',
    'Is Romance',
    'Is Thriller',
    'Is Action',
    'Is Crime',
    'Is Horror',
    'Is Animation',
    'Is Family',
    'Is Adventure',
    'Is Fantasy',
    'Is Mystery',
    'Is Sci-Fi',
    'Is Musical',
    'Is War',
    'Is Music',
    'Is Western',
    'Is History',
    'Is Biography',
    'Is Adult',
    'Is Sport',
    'Is News'
]

class MovieVectorGenerator_y(MovieVectorGenerator):
    def __init__(self, imdb_conn=None):
        self.version = 4
        self.imdb_conn = IMDB() if imdb_conn is None else imdb_conn

        self.header = HEADER

    def get_vector(self, movie):
        """
        :param movie: Instance of an object derived from Movie
        :return: A vector representation of the movie. The first value is
                the classification
        """
        return [x[1] for x in get_movie_features  (self.imdb_conn, movie['id'], movie=movie)]
